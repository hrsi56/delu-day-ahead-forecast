"""Baseline source-day resolution, including the DST trap that broke CP-1.

The similar-day naive takes D-1 for Tue-Fri. Resolved as a fixed 24-row UTC
offset, that lands on a price of the *same* delivery day on the 25-hour fall-back
day -- the §5.2 availability violation. These tests assert the source delivery
date directly, and the positive control proves the assertion can fail.
"""

from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

from delu_forecast.baselines import SIMILAR_DAY_LAG_BY_WEEKDAY, seasonal_naive_168h, similar_day_naive
from delu_forecast.ingest import BERLIN
from conftest import synthetic_snapshot

FALL_BACK = date(2025, 10, 26)
SPRING_FORWARD = date(2025, 3, 30)


def _frame(start: date, end_exclusive: date) -> pd.DataFrame:
    snapshot = synthetic_snapshot(start, end_exclusive)
    # A price that encodes its own (delivery date, local hour), so a prediction
    # can be decoded back to the row it was taken from.
    local = pd.DatetimeIndex(snapshot["timestamp_utc"]).tz_convert(BERLIN)
    ordinal = np.array([value.toordinal() for value in local.date], dtype="float64")
    snapshot["price_eur_mwh"] = ordinal * 100.0 + local.hour.to_numpy()
    return snapshot


def _decode(values: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    days = np.floor(values / 100.0)
    return days, values - days * 100.0


def test_similar_day_takes_d_minus_1_on_tue_to_fri_and_d_minus_7_otherwise() -> None:
    snapshot = _frame(date(2025, 3, 1), date(2025, 11, 15))
    prediction = similar_day_naive(snapshot).to_numpy()
    local = pd.DatetimeIndex(snapshot["timestamp_utc"]).tz_convert(BERLIN)
    usable = np.isfinite(prediction)
    source_days, source_hours = _decode(prediction[usable])
    target_dates = np.array([value.toordinal() for value in local.date])[usable]
    weekday = local.dayofweek.to_numpy()[usable]
    expected_lag = np.array([SIMILAR_DAY_LAG_BY_WEEKDAY[int(value)] for value in weekday])
    assert np.array_equal(target_dates - source_days, expected_lag)
    assert np.array_equal(source_hours, local.hour.to_numpy()[usable])
    assert np.all(source_days < target_dates)  # never the delivery day itself


def test_no_baseline_ever_sources_its_own_delivery_day_across_both_dst_days() -> None:
    for transition in (FALL_BACK, SPRING_FORWARD):
        snapshot = _frame(transition - timedelta(days=30), transition + timedelta(days=3))
        local = pd.DatetimeIndex(snapshot["timestamp_utc"]).tz_convert(BERLIN)
        on_day = np.array([value == transition for value in local.date])
        assert on_day.sum() == (25 if transition == FALL_BACK else 23)
        for series in (similar_day_naive(snapshot), seasonal_naive_168h(snapshot)):
            values = series.to_numpy()[on_day]
            usable = np.isfinite(values)
            source_days, _ = _decode(values[usable])
            assert np.all(source_days < transition.toordinal())


def test_a_fixed_24_row_utc_offset_would_have_been_caught() -> None:
    """Positive control: the forbidden implementation must fail this assertion."""
    snapshot = _frame(FALL_BACK - timedelta(days=10), FALL_BACK + timedelta(days=2))
    local = pd.DatetimeIndex(snapshot["timestamp_utc"]).tz_convert(BERLIN)
    on_day = np.array([value == FALL_BACK for value in local.date])
    wrong = snapshot["price_eur_mwh"].shift(24).to_numpy()[on_day]
    source_days, _ = _decode(wrong[np.isfinite(wrong)])
    assert np.any(source_days == FALL_BACK.toordinal()), "control is inert; it must reproduce the leak"
    right = similar_day_naive(snapshot).to_numpy()[on_day]
    right_days, _ = _decode(right[np.isfinite(right)])
    assert not np.any(right_days == FALL_BACK.toordinal())


def test_ambiguous_or_absent_source_hour_fails_closed() -> None:
    """Both EU transitions fall on a Sunday, so the reachable case is the D-7 arm.

    A Sunday takes D-7. Seven days after the spring-forward Sunday the source hour
    02:00 does not exist; seven days after the fall-back Sunday it is ambiguous.
    Both must be null, and the neighbouring hour must still resolve -- otherwise
    "fails closed" would be indistinguishable from "returns null everywhere".
    """
    for transition in (SPRING_FORWARD, FALL_BACK):
        target = transition + timedelta(days=7)
        assert target.weekday() == 6 and SIMILAR_DAY_LAG_BY_WEEKDAY[6] == 7
        snapshot = _frame(transition - timedelta(days=2), target + timedelta(days=1))
        local = pd.DatetimeIndex(snapshot["timestamp_utc"]).tz_convert(BERLIN)
        on_target = np.array([value == target for value in local.date])
        prediction = similar_day_naive(snapshot).to_numpy()[on_target]
        hours = local.hour.to_numpy()[on_target]
        assert np.isnan(prediction[hours == 2]).all()
        assert np.isfinite(prediction[hours == 1]).all()
        assert np.isfinite(prediction[hours == 3]).all()
