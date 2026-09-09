"""§9.4.2: whole-curve availability, with independent raw-value oracles."""
from datetime import date, timedelta
from statistics import mean, stdev

import numpy as np
import pandas as pd
import pytest

from delu_forecast.features import build_base_features
from conftest import synthetic_snapshot

PRICE_COLUMNS = (
    'price_lag_24h', 'price_lag_48h', 'price_lag_168h',
    'price_roll_mean_168h', 'price_roll_std_168h',
    'price_roll_mean_720h', 'price_roll_std_720h',
    'price_roll_q05_168h', 'price_roll_q50_168h', 'price_roll_q95_168h',
    'negative_price_count_168h',
)
ROLLING_COLUMNS = PRICE_COLUMNS[3:]


def expected_prices(raw: pd.DataFrame, target: date) -> pd.DataFrame:
    # Independent source selection: enumerate the raw calendar identities;
    # never call a feature helper, shift, rolling window or production lag.
    rows = raw.loc[raw.delivery_date.eq(target)]
    expected = pd.DataFrame(index=pd.DatetimeIndex(rows.timestamp_utc))
    for hours, days in ((24, 1), (48, 2), (168, 7)):
        source_day = target - timedelta(days=days)
        assert source_day < target
        source = raw.loc[raw.delivery_date.eq(source_day)]
        values = []
        for hour in rows.local_hour:
            matches = source.loc[source.local_hour.eq(hour), 'price_eur_mwh']
            values.append(matches.iloc[0] if len(matches) == 1 else np.nan)
        expected[f'price_lag_{hours}h'] = values
    history = raw.loc[raw.delivery_date.lt(target)].sort_values('timestamp_utc')
    for size in (168, 720):
        values = history.price_eur_mwh.iloc[-size:].tolist()
        assert len(values) == size
        expected[f'price_roll_mean_{size}h'] = mean(values)
        expected[f'price_roll_std_{size}h'] = stdev(values)
        if size == 168:
            # Explicit linear interpolation of order statistics (default quantile).
            ordered = sorted(values)
            for q, label in ((0.05, '05'), (0.50, '50'), (0.95, '95')):
                rank = (size - 1) * q
                lower = int(rank)
                expected[f'price_roll_q{label}_168h'] = ordered[lower] + (rank-lower)*(ordered[lower+1]-ordered[lower])
            expected['negative_price_count_168h'] = float(sum(value < 0 for value in values))
    return expected.loc[:, PRICE_COLUMNS]


@pytest.mark.parametrize('target', [date(2025, 2, 15), date(2025, 3, 30), date(2025, 10, 26)])
def test_whole_delivery_day_price_mutation_sweep_and_positive_control(target: date) -> None:
    raw = synthetic_snapshot(target - timedelta(days=35), target + timedelta(days=1))
    before = build_base_features(raw).loc[raw.delivery_date.eq(target).to_numpy(), PRICE_COLUMNS]
    pd.testing.assert_frame_equal(before, expected_prices(raw, target), check_exact=False, atol=1e-10, rtol=1e-12)
    assert before.loc[:, ROLLING_COLUMNS].notna().all().all()
    assert before.loc[:, ROLLING_COLUMNS].nunique(dropna=False).eq(1).all()
    # Every possible mutated hour, including first/last and both repeated rows.
    for row in raw.index[raw.delivery_date.eq(target)]:
        changed = raw.copy()
        changed.loc[row, 'price_eur_mwh'] = -999_999.0
        after = build_base_features(changed).loc[before.index, PRICE_COLUMNS]
        pd.testing.assert_frame_equal(before, after)
    # D-1's last (largest) price moves below all others: every rolling
    # statistic, including all three quantiles and the negative count, changes.
    changed = raw.copy()
    eligible = changed.index[changed.delivery_date.eq(target - timedelta(days=1))][-1]
    changed.loc[eligible, 'price_eur_mwh'] = -999_999.0
    after = build_base_features(changed).loc[before.index, PRICE_COLUMNS]
    pd.testing.assert_frame_equal(after, expected_prices(changed, target), check_exact=False, atol=1e-10, rtol=1e-12)
    assert after.loc[:, ROLLING_COLUMNS].ne(before.loc[:, ROLLING_COLUMNS]).all().all()
    assert after.loc[:, ROLLING_COLUMNS].nunique(dropna=False).eq(1).all()


@pytest.mark.parametrize('source_day', [date(2025, 3, 30), date(2025, 10, 26)])
@pytest.mark.parametrize('days', [1, 2, 7])
def test_lag_source_day_itself_is_dst_and_fails_closed(source_day: date, days: int) -> None:
    target = source_day + timedelta(days=days)
    raw = synthetic_snapshot(target - timedelta(days=35), target + timedelta(days=1))
    actual = build_base_features(raw).loc[raw.delivery_date.eq(target).to_numpy(), PRICE_COLUMNS]
    pd.testing.assert_frame_equal(actual, expected_prices(raw, target), check_exact=False, atol=1e-10, rtol=1e-12)
    repeated_or_absent = actual.index.tz_convert('Europe/Berlin').hour == 2
    assert actual.loc[repeated_or_absent, f'price_lag_{days*24}h'].isna().all()
    assert actual.loc[~repeated_or_absent, f'price_lag_{days*24}h'].notna().all()
    if source_day.month == 10:
        # Calendar ambiguity remains even when one of the two rows is missing.
        missing = raw.index[raw.delivery_date.eq(source_day) & raw.local_hour.eq(2)][0]
        incomplete = build_base_features(raw.drop(index=missing))
        assert incomplete.loc[actual.index[repeated_or_absent], f'price_lag_{days*24}h'].isna().all()


def test_missing_price_hour_cannot_shrink_or_extend_a_rolling_window() -> None:
    target = date(2025, 2, 15)
    raw = synthetic_snapshot(target - timedelta(days=35), target + timedelta(days=1))
    missing = raw.index[raw.delivery_date.eq(target - timedelta(days=1))][0]
    for damaged in (raw.drop(index=missing), raw.assign(price_eur_mwh=raw.price_eur_mwh.mask(raw.index == missing))):
        actual = build_base_features(damaged)
        assert actual.loc[actual.index.tz_convert('Europe/Berlin').date == target, ROLLING_COLUMNS].isna().all().all()
