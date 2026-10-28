"""CP-17 item 1, the A1 GFS check: the committed table and rule recomputed, and rebuilt from the ledger.

The first tests are CI-safe: they read only the committed daily rows. The last rebuilds the rows from
CP-26's stored ledger (the local-only `evidence/cp-26` extract in `.local/artifacts/cp-17/inputs/`) and
skips with that reason where it is absent, as on CI.
"""
from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path

import numpy as np
import pytest

from cp17.tools import gfs_check, ledger

ROOT = Path(__file__).resolve().parents[2]
RECORD = ROOT / 'reports/cp17/gfs-check.json'
DAILY = ROOT / 'reports/cp17/gfs-check-daily.csv'


@pytest.fixture(scope='module')
def record():
    return json.loads(RECORD.read_text())


@pytest.fixture(scope='module')
def table():
    return gfs_check.read_daily_csv(DAILY)


def test_daily_rows_are_the_recorded_ones(record, table):
    assert hashlib.sha256(DAILY.read_bytes()).hexdigest() == record['daily_rows_sha256']
    assert gfs_check.daily_csv(table).encode() == DAILY.read_bytes()


def test_summary_and_rule_recompute(record, table):
    summary = gfs_check.summarize(table)
    assert summary == record['summary']
    assert gfs_check.rule(summary) == record['rule']
    assert gfs_check.unpaired_sensitivity(table) == record['sensitivity_unpaired_affected']


def test_population_and_boundary(record, table):
    assert table.day.min() == date(2020, 12, 29) and table.day.max() == date(2026, 9, 6)
    assert len(table) == 2068 and table.day.is_unique and table.truth_finite.all()
    assert int(table.affected.sum()) == record['summary']['affected']['dates_eligible'] == 1358
    for stream in ('A1_gfs6', 'v2_nominal'):
        assert table[f'{stream}:native'].all()
    assert int((~table['A1_nominal:native']).sum()) == 18


def test_rule_is_the_briefs(record):
    # More than 2% worse on both MAE and WIS on the affected dates returns BLOCKED; either one alone does not.
    def cell(mae, wis):
        return {'affected': {m: {'ratio_v2_to_A1_gfs6': r} for m, r in (('MAE', mae), ('WIS', wis))}}
    assert gfs_check.rule(cell(1.021, 1.021))['blocked']
    assert not gfs_check.rule(cell(1.02, 1.5))['blocked']
    assert not gfs_check.rule(cell(1.5, 1.019))['blocked']
    assert record['rule']['blocked'] is True and record['rule']['outcome'] == 'BLOCKED'


def test_losses_match_the_stored_ones(record):
    check = record['crosscheck']
    for name, item in check.items():
        if not isinstance(item, dict):
            continue
        assert item['dates_compared'] >= 2050
        assert item['max_abs_difference'] <= 1e-13, name
        if name.endswith(':MAE') or name.startswith('A1_nominal:cp28_A1'):
            assert item['bitwise_equal'] == item['dates_compared'], name


@pytest.mark.skipif(not ledger.available(ROOT), reason="CP-26's local-only forecast ledger (evidence/cp-26 extract) is absent")
def test_rebuilt_from_the_ledger(table):
    rebuilt = gfs_check.daily_table(ROOT)
    assert gfs_check.daily_csv(rebuilt) == gfs_check.daily_csv(table)
    assert np.array_equal(rebuilt['A1_gfs6:WIS'].to_numpy(), table['A1_gfs6:WIS'].to_numpy())
