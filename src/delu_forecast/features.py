"""Frozen CP-1 feature catalogs and their leakage-safe construction."""

from __future__ import annotations

from datetime import date, timedelta

import holidays
import numpy as np
import pandas as pd

from .ingest import BERLIN

BASE_FEATURES: tuple[str, ...] = (
    "local_hour",
    "day_of_week",
    "month",
    "is_federal_holiday",
    "is_day_after_holiday",
    "is_bridge_day",
    "day_type",
    "dst_transition_day",
    "summer_peak",
    "winter_peak",
    "load_forecast_mw",
    "load_forecast_day_mean_mw",
    "price_lag_24h",
    "price_lag_48h",
    "price_lag_168h",
    "price_roll_mean_168h",
    "price_roll_std_168h",
    "price_roll_mean_720h",
    "price_roll_std_720h",
    "price_roll_q05_168h",
    "price_roll_q50_168h",
    "price_roll_q95_168h",
    "negative_price_count_168h",
    "crisis_period",
    "post_crisis",
)
AUGMENTED_FEATURES: tuple[str, ...] = BASE_FEATURES + ("residual_load_proxy",)


def _utc_index(frame: pd.DataFrame) -> pd.DataFrame:
    if "timestamp_utc" in frame.columns:
        result = frame.set_index("timestamp_utc").copy()
    else:
        result = frame.copy()
    result.index = pd.DatetimeIndex(result.index)
    if result.index.tz is None:
        raise ValueError("timestamps must be timezone-aware")
    result.index = result.index.tz_convert("UTC")
    if result.index.has_duplicates or not result.index.is_monotonic_increasing:
        raise ValueError("timestamps must be unique and increasing")
    return result


def _time_lag(series: pd.Series, hours: int) -> pd.Series:
    source_index = series.index - pd.Timedelta(hours=hours)
    return pd.Series(series.reindex(source_index).to_numpy(), index=series.index)


def build_base_features(snapshot: pd.DataFrame) -> pd.DataFrame:
    """Build the frozen strict-gate base catalog on the canonical UTC index."""
    frame = _utc_index(snapshot)
    if not {"price_eur_mwh", "load_forecast_mw"}.issubset(frame.columns):
        raise ValueError("snapshot lacks price or load forecast")
    local = frame.index.tz_convert(BERLIN)
    delivery_dates = pd.Index(local.date)
    years = range(min(value.year for value in delivery_dates), max(value.year for value in delivery_dates) + 1)
    federal_holidays = holidays.country_holidays("DE", years=years)
    holiday_dates = set(federal_holidays.keys())

    result = pd.DataFrame(index=frame.index)
    result["local_hour"] = local.hour.astype("int8")
    result["day_of_week"] = local.dayofweek.astype("int8")
    result["month"] = local.month.astype("int8")
    result["is_federal_holiday"] = np.fromiter((value in holiday_dates for value in delivery_dates), dtype="int8")
    result["is_day_after_holiday"] = np.fromiter(
        ((value - timedelta(days=1)) in holiday_dates for value in delivery_dates), dtype="int8"
    )
    result["is_bridge_day"] = np.fromiter(
        (
            (value.weekday() == 4 and value - timedelta(days=1) in holiday_dates)
            or (value.weekday() == 0 and value + timedelta(days=1) in holiday_dates)
            for value in delivery_dates
        ),
        dtype="int8",
    )
    result["day_type"] = np.select(
        [result["is_federal_holiday"].eq(1) | result["day_of_week"].eq(6), result["day_of_week"].eq(5)],
        [2, 1],
        default=0,
    ).astype("int8")
    day_counts = pd.Series(1, index=frame.index).groupby(delivery_dates).transform("sum")
    result["dst_transition_day"] = day_counts.ne(24).astype("int8")
    result["summer_peak"] = result["month"].isin((6, 7, 8)).astype("int8")
    result["winter_peak"] = result["month"].isin((12, 1, 2)).astype("int8")
    result["load_forecast_mw"] = frame["load_forecast_mw"]
    result["load_forecast_day_mean_mw"] = frame["load_forecast_mw"].groupby(delivery_dates).transform("mean")

    price = frame["price_eur_mwh"]
    for hours in (24, 48, 168):
        result[f"price_lag_{hours}h"] = _time_lag(price, hours)
    closed_left = price.shift(1)
    result["price_roll_mean_168h"] = closed_left.rolling(168, min_periods=168).mean()
    result["price_roll_std_168h"] = closed_left.rolling(168, min_periods=168).std()
    result["price_roll_mean_720h"] = closed_left.rolling(720, min_periods=720).mean()
    result["price_roll_std_720h"] = closed_left.rolling(720, min_periods=720).std()
    result["price_roll_q05_168h"] = closed_left.rolling(168, min_periods=168).quantile(0.05)
    result["price_roll_q50_168h"] = closed_left.rolling(168, min_periods=168).quantile(0.50)
    result["price_roll_q95_168h"] = closed_left.rolling(168, min_periods=168).quantile(0.95)
    result["negative_price_count_168h"] = price.lt(0).shift(1).rolling(168, min_periods=168).sum()

    result["crisis_period"] = np.fromiter(
        (date(2021, 9, 1) <= value <= date(2022, 12, 31) for value in delivery_dates), dtype="int8"
    )
    result["post_crisis"] = np.fromiter((value >= date(2023, 1, 1) for value in delivery_dates), dtype="int8")
    result.index.name = "timestamp_utc"
    return result.loc[:, BASE_FEATURES]


def residual_proxy_details(snapshot: pd.DataFrame) -> pd.DataFrame:
    """Compute the D-2-bounded, 42-complete-delivery-day proxy provenance."""
    frame = _utc_index(snapshot)
    required = {"vre_actual_mw", "load_forecast_mw"}
    if not required.issubset(frame.columns):
        raise ValueError(f"snapshot lacks {sorted(required - set(frame.columns))}")
    local = frame.index.tz_convert(BERLIN)
    row_dates = pd.Index(local.date)
    row_hours = pd.Index(local.hour)
    calendar = pd.date_range(min(row_dates), max(row_dates), freq="D").date

    observed_rows = pd.Series(1, index=row_dates).groupby(level=0).sum().reindex(calendar, fill_value=0)
    non_null_rows = frame["vre_actual_mw"].notna().groupby(row_dates).sum().reindex(calendar, fill_value=0)
    expected_rows = pd.Series(
        [
            int(
                (
                    pd.Timestamp(value + timedelta(days=1), tz=BERLIN).tz_convert("UTC")
                    - pd.Timestamp(value, tz=BERLIN).tz_convert("UTC")
                ).total_seconds()
                // 3600
            )
            for value in calendar
        ],
        index=calendar,
    )
    complete_day = observed_rows.eq(expected_rows) & non_null_rows.eq(expected_rows)

    observations = pd.DataFrame(
        {"delivery_date": row_dates, "local_hour": row_hours, "value": frame["vre_actual_mw"].to_numpy()}
    )
    day_hour = observations.groupby(["delivery_date", "local_hour"])["value"].agg(["sum", "count"])
    norms: dict[tuple[date, int], float] = {}
    obs_counts: dict[tuple[date, int], int] = {}
    complete_in_window = complete_day.astype("int8").shift(2).rolling(42, min_periods=42).sum()
    for hour in range(24):
        try:
            hourly = day_hour.xs(hour, level="local_hour")
        except KeyError:
            hourly = pd.DataFrame(columns=["sum", "count"])
        daily_sum = hourly["sum"].reindex(calendar, fill_value=0.0)
        daily_count = hourly["count"].reindex(calendar, fill_value=0)
        rolling_sum = daily_sum.shift(2).rolling(42, min_periods=42).sum()
        rolling_count = daily_count.shift(2).rolling(42, min_periods=42).sum()
        valid = complete_in_window.eq(42) & rolling_count.gt(0)
        values = (rolling_sum / rolling_count).where(valid)
        for value_date, norm, count in zip(calendar, values, rolling_count, strict=True):
            norms[(value_date, hour)] = float(norm) if pd.notna(norm) else np.nan
            obs_counts[(value_date, hour)] = int(count) if pd.notna(count) else 0

    keys = list(zip(row_dates, row_hours, strict=True))
    vre_norm = np.array([norms[key] for key in keys], dtype="float64")
    details = pd.DataFrame(index=frame.index)
    details["vre_norm"] = vre_norm
    details["residual_load_proxy"] = frame["load_forecast_mw"].to_numpy() - vre_norm
    details["window_observation_count"] = np.array([obs_counts[key] for key in keys], dtype="int16")
    details["window_start_delivery_date"] = [value - timedelta(days=43) for value in row_dates]
    details["window_end_delivery_date"] = [value - timedelta(days=2) for value in row_dates]
    details.index.name = "timestamp_utc"
    return details


def build_feature_catalog(snapshot: pd.DataFrame, catalog: str = "base") -> pd.DataFrame:
    base = build_base_features(snapshot)
    if catalog == "base":
        return base
    if catalog == "base_plus_residual_load_proxy":
        result = base.copy()
        result["residual_load_proxy"] = residual_proxy_details(snapshot)["residual_load_proxy"]
        return result.loc[:, AUGMENTED_FEATURES]
    raise ValueError(f"unknown frozen catalog: {catalog}")
