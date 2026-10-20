"""Closed repair usage and continuation accounting are distinct, immutable scopes."""
import copy
import hashlib
import json

import pytest

from cp26 import budget as B


def closed_evidence(tmp_path):
    budget = B.Budget(tmp_path / 'live.json')
    budget.initialise()
    budget.record_charge('old-measured', 70, 'measured', {'receipt': 'old'})
    budget.record_charge('old-reported', 5, 'reported', {'report': 'old'})
    budget.record_charge('old-reserve', 25, 'reserved', {'bound': 'old'}, reserve_status='authorized')
    with budget.transaction() as state:
        state['repair_scope'] = {'id': 'repair-v21-r14', 'active': False,
            'baseline_seconds': 60, 'limit_seconds': 36000,
            'terminal_candidate_sha': 'a' * 40}
    historical = budget.read()
    ledger = tmp_path / 'terminal-ledger.json'
    resources = tmp_path / 'terminal-resources.json'
    B.atomic(ledger, historical)
    B.atomic(resources, {'repair_scope_active': False, 'total_seconds': 100,
                         'repair_seconds_used': 40})
    return budget, resources, ledger


def test_closed_scope_requires_original_evidence_before_summary(tmp_path):
    budget, _, _ = closed_evidence(tmp_path)
    with pytest.raises(RuntimeError, match='hash-bound terminal snapshot'):
        B.resource_summary(budget.read())
    with pytest.raises(RuntimeError, match='new compute is stopped'):
        B.require_compute_ready(budget.read())


def test_continuation_and_later_review_cannot_change_terminal_repair_usage(tmp_path):
    budget, resources, ledger = closed_evidence(tmp_path)
    # A review performed after closure remains cumulative and is not repair usage.
    budget.record_charge('later-review', 8, 'measured', {'receipt': 'review'})
    before = budget.read()
    first = budget.freeze_closed_repair(resources, ledger, authority_sha256='b' * 64)
    assert first['repair_seconds_used'] == 40
    assert first['repair_seconds_remaining'] == 35960
    assert first['continuation_seconds_used'] == 0
    assert first['post_repair_seconds'] == 8
    frozen = copy.deepcopy(budget.read()['repair_scope'])
    assert frozen['terminal_snapshot']['ledger_sha256'] == hashlib.sha256(ledger.read_bytes()).hexdigest()
    budget.record_charge('continuation', 12, 'measured', {'receipt': 'continuation'})
    after = budget.read()
    assert after['charges'][:len(before['charges'])] == before['charges']
    assert after['reserves'] == before['reserves']
    assert after['repair_scope'] == frozen
    summary = B.resource_summary(after)
    assert summary['repair_seconds_used'] == 40
    assert summary['continuation_seconds_used'] == 12
    assert summary['post_repair_seconds'] == 20
    assert summary['total_seconds'] == 120
    assert summary['reserved_seconds'] == 25
    assert budget.freeze_closed_repair(resources, ledger, authority_sha256='b' * 64) == summary
    assert B.total_seconds(budget.read()) == 120


@pytest.mark.parametrize('mutate', [
    lambda s: s['repair_scope'].update(active=True),
    lambda s: s['repair_scope']['terminal_snapshot'].update(repair_seconds_used=0),
    lambda s: s['repair_scope'].update(limit_seconds=72000),
])
def test_terminal_scope_mutation_is_rejected_without_writing(tmp_path, mutate):
    budget, resources, ledger = closed_evidence(tmp_path)
    budget.freeze_closed_repair(resources, ledger, authority_sha256='b' * 64)
    before = budget.path.read_bytes()
    with pytest.raises(ValueError, match='immutable'):
        with budget.transaction() as state:
            mutate(state)
    assert budget.path.read_bytes() == before


def test_wrong_terminal_evidence_or_authority_never_reclassifies_charges(tmp_path):
    budget, resources, ledger = closed_evidence(tmp_path)
    bad = json.loads(resources.read_text())
    bad['repair_seconds_used'] = 1
    B.atomic(resources, bad)
    before = budget.path.read_bytes()
    with pytest.raises(ValueError, match='disagree'):
        budget.freeze_closed_repair(resources, ledger, authority_sha256='b' * 64)
    assert budget.path.read_bytes() == before
    bad['repair_seconds_used'] = 40
    B.atomic(resources, bad)
    budget.freeze_closed_repair(resources, ledger, authority_sha256='b' * 64)
    before = budget.path.read_bytes()
    with pytest.raises(ValueError, match='authority identity'):
        budget.freeze_closed_repair(resources, ledger, authority_sha256='c' * 64)
    assert budget.path.read_bytes() == before
