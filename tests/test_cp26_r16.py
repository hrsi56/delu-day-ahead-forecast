"""Affected r16 absolute resource boundaries and stopped-account cap transition."""
import copy
import hashlib
import json

import pytest

from cp26 import budget as B, harness as H
from cp26.limits import shutdown_exposure_seconds


def state(seconds=0.):
    return {'caps': B.CAPS.copy(), 'counts': {'machine_seconds': seconds},
            'accounting': {'measured_seconds': seconds, 'reported_seconds': 0.,
                           'reserved_seconds': 0.}, 'jobs': [], 'reserves': [],
            'charges': [{'id': 'historical', 'source': {'original': True}}],
            'execution_tasks': [{'id': 'original-probe'}],
            'repair_scope': {'active': False, 'limit_seconds': 36000.,
                             'terminal_snapshot': {'repair_seconds_used': 0., 'total_seconds': 0.}},
            'scientific_runs': {}}


def costs():
    searches = [{'run': r, 'k': k, 'classification': 'conservative', 'basis': 'fixture',
                 'machine_seconds': 1.} for r in ('nominal', 'noload', 'gfs6') for k in range(14)]
    remaining = {k: {'classification': 'conservative', 'basis': 'fixture', 'machine_seconds': 1.}
                 for k in ('daily_fits', 'parity', 'tests', 'bootstrap', 'diagnostics', 'failed_jobs_and_resume')}
    return searches, remaining


def test_absolute_admission_boundary_never450():
    searches, remaining = costs()
    s = state(440 * 3600 - 48)
    assert B.projected_cost(s, searches, remaining, run_id=B.COLD_RUN_ID)['within_pilot_stop']
    assert not B.projected_cost(s, searches, remaining)['within_pilot_stop']
    B.add_seconds(s, .001)
    assert not B.projected_cost(s, searches, remaining, run_id=B.COLD_RUN_ID)['within_pilot_stop']
    assert B.admission_hours('different-run') == 436.5
    assert B.admission_hours(B.COLD_RUN_ID) == 440
    assert B.CAPS['machine_seconds'] == 500 * 3600


def test500_ceiling_preserves_shutdown_headroom():
    s = state(500 * 3600 - shutdown_exposure_seconds(4))
    s['jobs'] = [{'running': True, 'workers': 4}]
    original = copy.deepcopy(s)
    assert B.limit_reason(s) == 'machine_hours_cap' and s == original
    s['accounting']['measured_seconds'] -= .01
    s['counts']['machine_seconds'] -= .01
    assert B.limit_reason(s) is None


def test_locked_cap_transition_preserves_history_and_is_once(tmp_path, monkeypatch):
    monkeypatch.setattr(H, 'art', lambda: tmp_path)
    monkeypatch.setattr(H, 'continuation_authority', lambda root: {
        'actual_ceiling_hours': 500, 'run_id': B.COLD_RUN_ID, 'admission_hours': 440})
    s = state(123.)
    s['caps']['machine_seconds'] = 485 * 3600
    p, backup = tmp_path / 'budget.json', tmp_path / 'before.json'
    B.atomic(p, s)
    raw = p.read_bytes()
    b = B.Budget(p)
    receipt = b.transition_r16_cap(tmp_path, backup)
    after = json.loads(p.read_bytes())
    assert backup.read_bytes() == raw
    assert receipt['before_sha256'] == hashlib.sha256(raw).hexdigest()
    assert after.pop('cap_transitions') == [receipt]
    after['caps'] = s['caps']
    assert after == s
    transitioned = p.read_bytes()
    assert b.transition_r16_cap(tmp_path, backup) == receipt
    assert p.read_bytes() == transitioned
    s['jobs'] = [{'running': True}]
    B.atomic(p, s)
    with pytest.raises(RuntimeError, match='stopped'):
        b.transition_r16_cap(tmp_path, backup)
    assert json.loads(p.read_bytes()) == s
