"""CP-26 information-boundary, window and declared-variant controls (no model fits)."""
from datetime import date, timedelta
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from cp25.guard import BoundaryRefused
from cp26 import harness as H
from cp26.members import v1r_windows


def test_issue_time_uses_previous_days_berlin_offset():
    # The day immediately after a transition uses the transition day's 11:00 offset.
    assert H.issue_instant(date(2026, 3, 29), H.NEW).hour == 10
    assert H.issue_instant(date(2026, 3, 30), H.NEW).hour == 9
    assert H.issue_instant(date(2025, 10, 26), H.NEW).hour == 9
    assert H.issue_instant(date(2025, 10, 27), H.NEW).hour == 10
    assert H.issue_instant(date(2026, 3, 30), H.OLD).hour == 11


def test_v1r_both_embargoes_and_bounded_head_history():
    day = date(2025, 5, 1)
    dates = np.arange(np.datetime64(day-timedelta(days=730)), np.datetime64(day+timedelta(days=1)))
    data = SimpleNamespace(dates=dates, eligible=np.ones(len(dates), dtype=bool))
    lower, train, cal = v1r_windows(data, day)
    assert lower == day-timedelta(days=728)
    assert dates[train[0]] == np.datetime64(lower)
    assert dates[train[-1]] == np.datetime64(day-timedelta(days=63))
    assert dates[cal[0]] == np.datetime64(day-timedelta(days=61))
    assert dates[cal[-1]] == np.datetime64(day-timedelta(days=2))
    assert len(cal) == 60
    assert not np.intersect1d(train, cal).size
    excluded = {np.datetime64(day-timedelta(days=i)) for i in (62, 1, 0)}
    assert not excluded.intersection(dates[np.r_[train, cal]])


def test_weather_read_filters_before_materialisation_and_refuses_misdated_rows(monkeypatch):
    calls = []

    def read(path, **kwargs):
        calls.append(kwargs)
        return pd.DataFrame({'timestamp_utc': [pd.Timestamp('2026-09-06T21:00Z')],
                             'delivery_date': [date(2026, 9, 6)]})
    monkeypatch.setattr(pd, 'read_parquet', read)
    frame = H.guarded_weather('unused.parquet', H.NEW_BOUNDARY)
    assert len(frame) == 1
    assert calls == [{'filters': [('delivery_date', '<=', H.NEW_BOUNDARY)]}]
    with pytest.raises(BoundaryRefused):
        H.guarded_weather('unused.parquet', date(2026, 9, 7))
    assert len(calls) == 1

    def forbidden(path, **kwargs):
        return pd.DataFrame({'timestamp_utc': [pd.Timestamp('2026-09-06T22:00Z')],
                             'delivery_date': [date(2026, 9, 6)]})
    monkeypatch.setattr(pd, 'read_parquet', forbidden)
    with pytest.raises(BoundaryRefused):
        H.guarded_weather('unused.parquet', H.NEW_BOUNDARY)


def test_variant_load_column_contract_fails_closed():
    p = {'lear': {'features': ['price']*96 + [f'load_{i}' for i in range(72)] + ['weekday']*7},
         'lgbm': {'features': ['price']*10 + ['load_forecast_mw', 'load_forecast_day_mean_mw'] + ['calendar']*11}}
    assert H.load_columns(p) == (list(range(96, 168)), [10, 11])
    p['lear']['features'][95] = 'load_unexpected'
    with pytest.raises(H.HarnessError):
        H.load_columns(p)
