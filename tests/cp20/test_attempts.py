"""Attempt allowance: 2 production per message (third kept for review); Owner decision O1 adds
up to two production attempts only where pre-run testing consumed attempts, logged separately."""
import json

import pytest

from cp20 import extract
from cp20.budget import Budget
from cp20.gfs import FIELDS, IntegrityError


def seed(path, run, lead, n, epoch):
    with path.open('a') as fh:
        for k in range(n):
            for f in FIELDS:
                fh.write(json.dumps({'run': run, 'lead': lead, 'field': f, 'endpoint': 'aws', 'attempt': k + 1,
                                     'purpose': 'production', 'epoch': epoch}) + '\n')


@pytest.fixture
def ledger(tmp_path):
    b = Budget(tmp_path / 'ledger.json')
    b.initialise({})
    return b


@pytest.mark.parametrize('prerun,post,allowed', [(0, 0, 2), (1, 0, 2), (2, 0, 2), (0, 1, 1), (1, 1, 1), (2, 1, 1), (2, 2, 0), (0, 2, 0)])
def test_production_allowance_with_owner_prerun_replacements(tmp_path, ledger, prerun, post, allowed):
    path = tmp_path / 'attempts.jsonl'
    seed(path, '2021-01-04', 21, prerun, extract.PRERUN_CUTOFF_EPOCH - 100)
    seed(path, '2021-01-04', 21, post, extract.PRERUN_CUTOFF_EPOCH + 100)
    a = extract.Attempts(path, ledger)
    for _ in range(allowed):
        a.begin('2021-01-04', 21, 'aws', 'production')
    with pytest.raises(IntegrityError, match='allowance exhausted'):
        a.begin('2021-01-04', 21, 'aws', 'production')
    total = prerun + post + allowed
    assert total == extract.PRODUCTION_ATTEMPTS + min(2, prerun)
    replacements = max(0, total - extract.PRODUCTION_ATTEMPTS) - max(0, prerun + post - extract.PRODUCTION_ATTEMPTS)
    counts = ledger.read()['counts']
    assert counts.get('message_attempts', 0) == 5 * allowed
    assert counts.get('prerun_replacement_attempts', 0) == 5 * replacements
    logged = path.with_name('prerun_replacement_attempts.jsonl')
    lines = logged.read_text().splitlines() if logged.exists() else []
    assert len(lines) == 5 * replacements
    assert all(json.loads(l)['owner_decision'] == 'O1' and json.loads(l)['purpose'].startswith('owner_approved_prerun_replacement')
               for l in lines)


def test_review_attempt_is_never_consumed_by_ordinary_production(tmp_path, ledger):
    path = tmp_path / 'attempts.jsonl'
    a = extract.Attempts(path, ledger)
    a.begin('2025-01-01', 24, 'aws', 'production')
    a.begin('2025-01-01', 24, 'ncar', 'alternate_endpoint')
    with pytest.raises(IntegrityError):
        a.begin('2025-01-01', 24, 'aws', 'transient_retry')
    assert a.used('2025-01-01', 24) == 2 < 3
