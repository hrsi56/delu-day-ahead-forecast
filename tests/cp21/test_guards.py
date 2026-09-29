"""CP-21 §17.1/§17.7/§17.8: the 2026-04-07 boundary guard, the strict raw schema, the ledger's
charge-before-use and the Friday/Shabbat calendar, each with a positive control."""
from __future__ import annotations

from datetime import date, datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import pytest

from cp15.data import RAW_COLUMNS, prepare
from cp21 import budget as B
from cp21.inputs import BOUNDARY, BoundaryViolation, guard_boundary, load

ROOT = Path(__file__).resolve().parents[2]


def test_boundary_guard_refuses_after_2026_04_07_and_accepts_up_to_it():
    ok = pd.DataFrame({'delivery_date': [date(2026, 4, 6), BOUNDARY]})
    assert guard_boundary(ok) is ok  # positive control
    with pytest.raises(BoundaryViolation):
        guard_boundary(pd.DataFrame({'delivery_date': [date(2026, 4, 8)]}))
    with pytest.raises(BoundaryViolation):
        guard_boundary(pd.DataFrame({'delivery_date': [date(2018, 12, 31)]}))


def test_loader_materialises_nothing_after_the_boundary_and_honours_before():
    data = load(ROOT)
    assert str(data.dates.max()) == '2026-04-07' and str(data.dates.min()) >= '2019-01-01'
    early = load(ROOT, before=date(2025, 5, 1))
    assert str(early.dates.max()) == '2025-04-30'


def test_raw_schema_refuses_post_gate_and_actual_columns():
    p = json.loads((ROOT / 'reports/cp15/protocol.json').read_text())
    frame = pd.read_parquet(ROOT / 'data/snapshot.parquet', columns=RAW_COLUMNS,
                            filters=[('delivery_date', '>=', date(2025, 1, 1)), ('delivery_date', '<=', date(2025, 3, 1))])
    prepare(frame, p)  # positive control: the strict raw schema passes
    for extra in ('a69_generation_actual_mw', 'actual_load_mw'):
        bad = frame.assign(**{extra: 1.0})
        with pytest.raises(ValueError, match='strict raw schema'):
            prepare(bad, p)


def test_ledger_refuses_before_a_cap_and_never_resets(tmp_path):
    ledger = B.Budget(tmp_path / 'budget.json')
    ledger.initialise({'git_bytes': 0})
    with pytest.raises(FileExistsError):
        ledger.initialise({'git_bytes': 0})
    ledger.reserve(lgbm_fits=B.CAPS['lgbm_fits'] - 1)
    ledger.reserve(lgbm_fits=1)  # positive control: exactly at the cap is allowed
    with pytest.raises(B.CapExceeded):
        ledger.reserve(lgbm_fits=1)
    assert ledger.read()['counts']['lgbm_fits'] == B.CAPS['lgbm_fits']
    with pytest.raises(ValueError):
        ledger.reserve(unknown_counter=1)
    assert B.CAPS['download_bytes'] == 0 and B.CAPS['remote_writes'] == 0
    with pytest.raises(B.CapExceeded):
        ledger.reserve(remote_writes=1)


def test_calendar_window_is_friday_and_saturday_in_jerusalem():
    tz = ZoneInfo('Asia/Jerusalem')
    thursday = datetime(2026, 10, 1, 23, 0, tzinfo=tz).timestamp()
    inside, until = B.calendar_stop(thursday)
    assert not inside and until == 3600
    assert B.calendar_stop(datetime(2026, 10, 2, 0, 0, tzinfo=tz).timestamp())[0]
    assert B.calendar_stop(datetime(2026, 10, 3, 23, 59, tzinfo=tz).timestamp())[0]
    assert not B.calendar_stop(datetime(2026, 10, 4, 0, 0, tzinfo=tz).timestamp())[0]
