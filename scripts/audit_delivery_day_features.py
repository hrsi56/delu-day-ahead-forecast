#!/usr/bin/env python3
"""Recompute §5.2 from raw snapshot identities and compare the public SQL artifact.

This is an offline acceptance audit, not an EDA/selection/model-fitting step.
No outcomes are used to choose features, partitions, windows, or thresholds.
"""
from __future__ import annotations

from datetime import timedelta
import json
from pathlib import Path
from statistics import mean, stdev

import duckdb
import numpy as np
import pandas as pd

from delu_forecast.features import build_base_features

ROOT = Path(__file__).resolve().parents[1]
LAGS = {'price_lag_24h': 1, 'price_lag_48h': 2, 'price_lag_168h': 7}
ROLLING = (
    'price_roll_mean_168h', 'price_roll_std_168h',
    'price_roll_mean_720h', 'price_roll_std_720h',
    'price_roll_q05_168h', 'price_roll_q50_168h', 'price_roll_q95_168h',
    'negative_price_count_168h',
)


def main() -> None:
    raw = pd.read_parquet(ROOT / 'data/snapshot.parquet')
    local = pd.DatetimeIndex(raw.timestamp_utc).tz_convert('Europe/Berlin')
    dates = local.date
    assert (dates == raw.delivery_date).all()
    assert (local.hour == raw.local_hour).all()
    actual = build_base_features(raw)
    assert actual.index.as_unit('ns').equals(pd.DatetimeIndex(raw.timestamp_utc).as_unit('ns'))
    prices = raw.price_eur_mwh.to_numpy()
    assert np.isfinite(prices).all()
    # This oracle uses observed raw calendar keys, not production localization.
    sources = raw.groupby(['delivery_date', 'local_hour']).price_eur_mwh.agg(list).to_dict()
    expected = pd.DataFrame(index=actual.index)
    null_lags = {}
    for column, days in LAGS.items():
        values = []
        for target, hour in zip(dates, local.hour, strict=True):
            source_day = target - timedelta(days=days)
            assert source_day < target
            matches = sources.get((source_day, hour), [])
            values.append(matches[0] if len(matches) == 1 else np.nan)
        expected[column] = values
        np.testing.assert_allclose(actual[column], values, rtol=0, atol=0, equal_nan=True)
        null_lags[column] = int(np.isnan(values).sum())

    invalid_load_days = []
    days_checked = 0
    for target, rows in raw.groupby('delivery_date', sort=True):
        positions = rows.index.to_numpy()
        start = int(positions[0])
        assert (dates[:start] < target).all()
        for size in (168, 720):
            values = prices[max(0, start - size):start].tolist()
            oracle = {
                f'price_roll_mean_{size}h': mean(values) if len(values) == size else np.nan,
                f'price_roll_std_{size}h': stdev(values) if len(values) == size else np.nan,
            }
            if size == 168:
                ordered = sorted(values)
                for q, label in ((0.05, '05'), (0.50, '50'), (0.95, '95')):
                    rank = (size-1)*q
                    low = int(rank)
                    oracle[f'price_roll_q{label}_168h'] = (
                        ordered[low] + (rank-low)*(ordered[low+1]-ordered[low]) if len(values) == size else np.nan
                    )
                oracle['negative_price_count_168h'] = float(sum(value < 0 for value in values)) if len(values) == size else np.nan
            for column, value in oracle.items():
                # Every row must equal the oracle, including null at archive head.
                observed = actual[column].iloc[positions]
                assert observed.nunique(dropna=False) == 1
                np.testing.assert_allclose(observed, value, rtol=1e-12, atol=1e-9, equal_nan=True)
                expected.loc[observed.index, column] = value
        start_local = pd.Timestamp(target, tz='Europe/Berlin')
        end_local = pd.Timestamp(target + timedelta(days=1), tz='Europe/Berlin')
        hours = int((end_local - start_local).total_seconds() / 3600)
        assert len(rows) == hours
        load = rows.load_forecast_mw
        complete = load.notna().sum() == hours
        load_oracle = mean(load.tolist()) if complete else np.nan
        np.testing.assert_allclose(actual.load_forecast_day_mean_mw.iloc[positions], load_oracle, equal_nan=True)
        if not complete:
            invalid_load_days.append({'delivery_date': str(target), 'expected_hours': hours, 'available_hours': int(load.notna().sum())})
        days_checked += 1

    con = duckdb.connect(':memory:')
    con.execute((ROOT / 'sql/feature_queries.sql').read_text())
    lag_sql = con.execute('SELECT * FROM lag_features ORDER BY timestamp_utc').fetchdf()
    rolling_sql = con.execute('SELECT * FROM rolling_features ORDER BY delivery_date').fetchdf()
    assert len(lag_sql) == len(raw)
    assert len(rolling_sql) == days_checked
    sql_daily = rolling_sql.set_index(pd.to_datetime(rolling_sql.delivery_date).dt.date)
    max_sql_error = 0.0
    for column in LAGS:
        np.testing.assert_allclose(lag_sql[column], expected[column], rtol=0, atol=0, equal_nan=True)
    for column in ROLLING:
        broadcast = sql_daily[column].reindex(dates).to_numpy(dtype=float)
        np.testing.assert_allclose(broadcast, expected[column], rtol=1e-12, atol=1e-9, equal_nan=True)
        max_sql_error = max(max_sql_error, float(np.nanmax(np.abs(broadcast - expected[column].to_numpy()))))
    for view in ('data_quality_checks', 'source_bin_checks'):
        assert not con.execute(f'SELECT * FROM {view}').fetchdf().to_numpy().any()

    old_roll_exposure = sum(dates[index-1] == dates[index] for index in range(1, len(raw)))
    old_lag_same_day = sum(dates[index-24] == dates[index] for index in range(24, len(raw)))
    print(json.dumps({
        'raw_rows_checked': len(raw), 'delivery_days_checked': days_checked,
        'price_columns_checked': len(LAGS) + len(ROLLING),
        'same_day_price_sources_in_repaired_features': 0,
        'null_calendar_lags': null_lags,
        'sql_rolling_delivery_days': len(rolling_sql),
        'sql_max_absolute_error_vs_raw_oracle': max_sql_error,
        'null_a65_daily_statistics': invalid_load_days,
        'retired_rowwise_rolling_exposed_rows': int(old_roll_exposure),
        'retired_utc_24h_lag_same_day_rows': int(old_lag_same_day),
    }, indent=2))


if __name__ == '__main__':
    main()
