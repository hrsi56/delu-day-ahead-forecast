"""Calendar-support refusal with positive controls; restricted reader contract."""
from datetime import date
from pathlib import Path
import sys

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'src'))
from cp15.preflight import canonical_hours, load_admissible, window_support


def test_missing_archive_and_supplied_prehistory_positive_control():
    bad = window_support(date(2020, 7, 1), 728, date(2019, 1, 1))
    assert bad['required_start'] == '2018-07-04'
    assert bad['absent_leading_calendar_days'] == 181
    assert bad['absent_leading_canonical_hours'] == 4345
    assert not bad['archive_reaches_required_start']
    good = window_support(date(2020, 7, 1), 728, date(2018, 7, 4))
    assert good['archive_reaches_required_start']
    assert good['absent_leading_calendar_days'] == good['absent_leading_canonical_hours'] == 0
    # A4's actual 84-day history has archive support at this same origin.
    assert window_support(date(2020, 7, 1), 84, date(2019, 1, 1))['archive_reaches_required_start']


@pytest.mark.parametrize('start,end,expected', [
    (date(2020, 3, 29), date(2020, 3, 30), 23),
    (date(2020, 10, 25), date(2020, 10, 26), 25),
    (date(2020, 7, 1), date(2020, 7, 2), 24),
])
def test_canonical_hours_respect_dst(start, end, expected):
    assert canonical_hours(start, end) == expected


def test_reader_filters_before_materialization_and_refuses_bad_reader(monkeypatch):
    root = Path(__file__).resolve().parents[2]
    seen = []
    def reader(path, *, columns, filters):
        seen.append((columns, filters))
        return pd.DataFrame({'delivery_date': [date(2026, 4, 7)]})
    monkeypatch.setattr(pd, 'read_parquet', reader)
    frame, _ = load_admissible(root)
    assert len(frame) == 1
    assert seen[0][1] == [('delivery_date', '<=', date(2026, 4, 7))]
    assert seen[0][0] == ['timestamp_utc', 'delivery_date', 'price_eur_mwh', 'load_forecast_mw']
    monkeypatch.setattr(pd, 'read_parquet', lambda *a, **k: pd.DataFrame({'delivery_date': [date(2026, 4, 8)]}))
    with pytest.raises(ValueError, match='reserved outcomes'):
        load_admissible(root)


def test_unratified_history_refused_with_allowed_control():
    with pytest.raises(ValueError, match='ratified'):
        window_support(date(2020, 7, 1), 547, date(2019, 1, 1))
    assert window_support(date(2020, 7, 1), 728, date(2019, 1, 1))['history_days'] == 728
