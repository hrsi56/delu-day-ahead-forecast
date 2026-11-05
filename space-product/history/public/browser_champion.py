"""The champion, re-expressed for the browser (M3.5/CP-3B, §9.2 as amended).

`mlflow.pyfunc` does not load under Pyodide, so the WASM showcase cannot run the
packaged artifact. It runs this instead: the same nine boosters, the same base
catalog computed from the same rows, the same four CQR thresholds, the same
isotonic step. Nothing about the model changes -- only where it executes.

**This file is the thing under test.** `tests/test_22_wasm_equivalence.py`
imports it on the host and requires its output to equal the frozen
`mlflow.pyfunc` champion bitwise across the committed fixture; the notebook
fetches the identical bytes and executes them in Pyodide. A claim that "the
shipped model is exactly the model the holdout evaluated" survives only as long
as that comparison does, so the comparison is the artifact, not the assertion.

Deliberately dependency-light: numpy only. No pandas, no timezone conversion, no
`holidays` package. Every calendar fact the frozen pipeline derived from
`Europe/Berlin` or from `holidays.country_holidays("DE")` is shipped as data in
`series.json` and `calendar.json` -- the snapshot already computed
`delivery_date` and `local_hour` from exactly that conversion -- while the
feature *logic* that consumes those facts is re-expressed here and proved equal.
"""

from __future__ import annotations

import datetime as _dt

import numpy as np

QUANTILE_LABELS = ("p025", "p05", "p10", "p25", "p50", "p75", "p90", "p95", "p975")
SYMMETRIC_PAIRS = (("p025", "p975"), ("p05", "p95"), ("p10", "p90"), ("p25", "p75"))

#: §4.1's frozen `base` catalog, in the order the boosters were fit on. Read from
#: champion.json at runtime and asserted against this tuple: a silent reordering
#: would feed every tree the wrong column and still produce plausible numbers.
BASE_FEATURES = (
    "local_hour", "day_of_week", "month", "is_federal_holiday", "is_day_after_holiday",
    "is_bridge_day", "day_type", "dst_transition_day", "summer_peak", "winter_peak",
    "load_forecast_mw", "load_forecast_day_mean_mw", "price_lag_24h", "price_lag_48h",
    "price_lag_168h", "price_roll_mean_168h", "price_roll_std_168h", "price_roll_mean_720h",
    "price_roll_std_720h", "price_roll_q05_168h", "price_roll_q50_168h", "price_roll_q95_168h",
    "negative_price_count_168h", "crisis_period", "post_crisis",
)

_CRISIS_START = _dt.date(2021, 9, 1)
_CRISIS_END = _dt.date(2022, 12, 31)
_POST_CRISIS = _dt.date(2023, 1, 1)


def _date(value: str) -> _dt.date:
    year, month, day = value.split("-")
    return _dt.date(int(year), int(month), int(day))


class BrowserChampion:
    """Nine boosters + the base catalog + CQR + isotonic, over shipped rows."""

    def __init__(self, boosters, meta, series, calendar):
        self.boosters = boosters
        self.meta = meta
        self.features = tuple(meta["features"])
        if self.features != BASE_FEATURES:
            raise ValueError(
                f"catalog order changed: champion.json has {self.features}, expected {BASE_FEATURES}"
            )
        self.labels = tuple(meta["quantile_labels"])
        if self.labels != QUANTILE_LABELS:
            raise ValueError("quantile label order changed")
        self.thresholds = {
            tuple(key.split("|")): float(value) for key, value in meta["cqr_thresholds"].items()
        }

        self.epoch = np.asarray(series["epoch_hour"], dtype="int64")
        self.price = np.asarray(series["price_eur_mwh"], dtype="float64")
        self.load = np.asarray(series["load_forecast_mw"], dtype="float64")
        self.local_hour = np.asarray(series["local_hour"], dtype="int64")
        self.day_of = list(series["delivery_date"])

        #: epoch hour -> row. The frozen pipeline indexes canonical UTC hours; so
        #: does this, which is why no timezone maths is needed here.
        self._by_epoch = {int(h): i for i, h in enumerate(self.epoch)}

        #: (delivery date, local hour) -> rows. A list, not a row: on the
        #: fall-back day two UTC rows share one local hour, and the frozen
        #: `tz_localize(..., ambiguous="NaT")` yields null there. Two candidates
        #: therefore mean null, exactly as a missing key does.
        self._by_local = {}
        for index, (day, hour) in enumerate(zip(self.day_of, self.local_hour)):
            self._by_local.setdefault((day, int(hour)), []).append(index)

        self._rows_for_day = {}
        for index, day in enumerate(self.day_of):
            self._rows_for_day.setdefault(day, []).append(index)

        self._boundary = {k: int(v) for k, v in calendar["berlin_midnight_epoch_hour"].items()}
        self._holidays = set(calendar["federal_holidays"])

    # -- calendar-day lag -------------------------------------------------
    def _lag(self, day: str, hour: int, days_back: int) -> float:
        source_day = (_date(day) - _dt.timedelta(days=days_back)).isoformat()
        rows = self._by_local.get((source_day, hour), ())
        if len(rows) != 1:
            # Zero rows: the spring-forward gap, or off the edge of the shipped
            # slice. Two rows: the fall-back repeated hour. Both fail closed.
            return float("nan")
        return float(self.price[rows[0]])

    # -- D-1-frozen rolling statistics ------------------------------------
    def _rolling(self, day: str) -> dict[str, float]:
        boundary = self._boundary[day]
        hours = np.arange(boundary - 720, boundary, dtype="int64")
        long = np.array(
            [self.price[self._by_epoch[int(h)]] if int(h) in self._by_epoch else np.nan for h in hours],
            dtype="float64",
        )
        short = long[-168:]
        quantiles = np.quantile(short, [0.05, 0.50, 0.95])
        return {
            "price_roll_mean_168h": float(np.mean(short)),
            "price_roll_std_168h": float(np.std(short, ddof=1)),
            "price_roll_mean_720h": float(np.mean(long)),
            "price_roll_std_720h": float(np.std(long, ddof=1)),
            "price_roll_q05_168h": float(quantiles[0]),
            "price_roll_q50_168h": float(quantiles[1]),
            "price_roll_q95_168h": float(quantiles[2]),
            "negative_price_count_168h": (
                float(np.sum(short < 0)) if not np.isnan(short).any() else float("nan")
            ),
        }

    # -- the base catalog for one delivery day ----------------------------
    def features_for_day(self, day: str, load_scale: float = 1.0):
        """`(n x 25)` feature matrix and the local hours, for delivery day `day`.

        `load_scale` multiplies **this delivery day's** A65 vector only, and
        `load_forecast_day_mean_mw` follows from it. It touches no price-derived
        feature and no other day, which is what keeps the §9.2 scenario control a
        ceteris-paribus probe rather than a second model.
        """
        indices = self._rows_for_day[day]
        target = _date(day)
        rolling = self._rolling(day)
        loads = np.array([self.load[i] for i in indices], dtype="float64") * float(load_scale)
        # skipna=False in the frozen pipeline: one missing hour invalidates the day.
        day_mean = float(np.mean(loads)) if not np.isnan(loads).any() else float("nan")
        # The frozen pipeline reindexes the day's expected Berlin hours; a
        # complete shipped day has exactly those rows, and a short day is caught
        # by the equivalence fixture rather than assumed away.
        dst_transition = 1 if len(indices) != 24 else 0
        weekday = target.weekday()
        is_holiday = 1 if day in self._holidays else 0
        day_before = (target - _dt.timedelta(days=1)).isoformat()
        day_after = (target + _dt.timedelta(days=1)).isoformat()
        is_day_after_holiday = 1 if day_before in self._holidays else 0
        is_bridge = 1 if (
            (weekday == 4 and day_before in self._holidays)
            or (weekday == 0 and day_after in self._holidays)
        ) else 0
        day_type = 2 if (is_holiday or weekday == 6) else (1 if weekday == 5 else 0)

        rows, hours = [], []
        for position, index in enumerate(indices):
            hour = int(self.local_hour[index])
            hours.append(hour)
            values = {
                "local_hour": float(hour),
                "day_of_week": float(weekday),
                "month": float(target.month),
                "is_federal_holiday": float(is_holiday),
                "is_day_after_holiday": float(is_day_after_holiday),
                "is_bridge_day": float(is_bridge),
                "day_type": float(day_type),
                "dst_transition_day": float(dst_transition),
                "summer_peak": float(target.month in (6, 7, 8)),
                "winter_peak": float(target.month in (12, 1, 2)),
                "load_forecast_mw": float(loads[position]),
                "load_forecast_day_mean_mw": day_mean,
                "price_lag_24h": self._lag(day, hour, 1),
                "price_lag_48h": self._lag(day, hour, 2),
                "price_lag_168h": self._lag(day, hour, 7),
                "crisis_period": float(_CRISIS_START <= target <= _CRISIS_END),
                "post_crisis": float(target >= _POST_CRISIS),
                **rolling,
            }
            rows.append([values[name] for name in self.features])
        return np.asarray(rows, dtype="float64"), hours

    # -- inference --------------------------------------------------------
    def predict_day(self, day: str, load_scale: float = 1.0):
        """Nine calibrated, monotone quantiles per row — NaN where incomplete."""
        matrix, hours = self.features_for_day(day, load_scale=load_scale)
        complete = ~np.isnan(matrix).any(axis=1)
        final = np.full((len(matrix), len(self.labels)), np.nan)
        if complete.any():
            raw = np.column_stack(
                [self.boosters[label].predict(matrix[complete]) for label in self.labels]
            )
            final[complete] = isotonic_last(apply_cqr_thresholds(raw, self.thresholds))
        return final, hours


def apply_cqr_thresholds(raw, thresholds):
    values = np.asarray(raw, dtype="float64").copy()
    positions = {label: index for index, label in enumerate(QUANTILE_LABELS)}
    for pair in SYMMETRIC_PAIRS:
        threshold = thresholds[pair]
        values[:, positions[pair[0]]] -= threshold
        values[:, positions[pair[1]]] += threshold
    return values


def _pava(values):
    levels, weights = [], []
    for value in values:
        levels.append(float(value))
        weights.append(1)
        while len(levels) >= 2 and levels[-2] > levels[-1]:
            weight = weights[-2] + weights[-1]
            level = (levels[-2] * weights[-2] + levels[-1] * weights[-1]) / weight
            levels[-2:] = [level]
            weights[-2:] = [weight]
    return np.repeat(np.asarray(levels), np.asarray(weights))


def isotonic_last(values):
    matrix = np.asarray(values, dtype="float64")
    return np.vstack([_pava(row) for row in matrix])
