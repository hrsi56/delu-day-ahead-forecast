"""§9.4.9: positive controls precede missing-hour fail-closed checks."""
from datetime import date, timedelta

import numpy as np
import pytest

from delu_forecast.features import build_base_features
from conftest import synthetic_snapshot


@pytest.mark.parametrize('day,hours', [(date(2025, 3, 30), 23), (date(2025, 2, 15), 24), (date(2025, 10, 26), 25)])
def test_a65_daily_statistic_requires_every_expected_hour(day: date, hours: int) -> None:
    raw = synthetic_snapshot(day, day + timedelta(days=1))
    assert len(raw) == hours
    raw['load_forecast_mw'] = np.arange(hours, dtype=float) ** 2 + 100
    complete = build_base_features(raw)['load_forecast_day_mean_mw']
    assert complete.notna().all()
    np.testing.assert_allclose(complete, sum(raw.load_forecast_mw) / hours)
    # Every hour absent or null; this explicitly includes each repeated 02 row.
    for row in raw.index:
        absent = raw.drop(index=row)
        null = raw.copy()
        null.loc[row, 'load_forecast_mw'] = np.nan
        for damaged in (absent, null):
            result = build_base_features(damaged)['load_forecast_day_mean_mw']
            assert result.isna().all()
            assert np.isfinite(damaged.load_forecast_mw.mean())  # The forbidden partial mean would be finite.
