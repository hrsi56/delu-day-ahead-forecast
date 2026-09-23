"""O2 attempt ledger: only responses that fail integrity/decoding/validation (or 4xx/wrong size)
count; network failures, stops and discarded tries are logged separately; O1 stays as recorded."""
import json

import pytest

from cp20 import extract
from cp20.budget import Budget
from cp20.gfs import FIELDS, IntegrityError


@pytest.fixture
def ledger(tmp_path):
    b = Budget(tmp_path / 'ledger.json')
    b.initialise({})
    return b


def test_only_failed_responses_count_and_uncounted_are_logged_separately(tmp_path, ledger):
    a = extract.Attempts(tmp_path / 'attempts.jsonl', ledger)
    for outcome in ('interrupted_by_stop', 'discarded_with_run', 'success', 'interrupted_by_cap'):
        a.end('2021-01-09', 21, 'aws', a.begin('2021-01-09', 21, 'aws', 'production'), outcome)
    assert a.used('2021-01-09', 21) == 0
    a.end('2021-01-09', 21, 'aws', a.begin('2021-01-09', 21, 'aws', 'production'), 'integrity_failure')
    a.end('2021-01-09', 21, 'ncar', a.begin('2021-01-09', 21, 'ncar', 'alternate_endpoint'), 'object_failure')
    with pytest.raises(IntegrityError, match='allowance exhausted'):
        a.begin('2021-01-09', 21, 'aws', 'integrity_retry')
    counts = ledger.read()['counts']
    assert counts['message_attempts'] == 10 and counts['message_tries'] == 30
    assert counts['uncounted_message_tries'] == 15
    unc = [json.loads(l) for l in (tmp_path / 'uncounted-attempts.jsonl').read_text().splitlines()]
    assert len(unc) == 15 and {u['owner_decision'] for u in unc} == {'O2'}
    # Reloading reproduces the allowance state from the outcome log.
    assert extract.Attempts(tmp_path / 'attempts.jsonl', ledger).used('2021-01-09', 21) == 2


@pytest.mark.parametrize('prerun,extra_allowed', [(0, 0), (1, 1), (2, 2), (3, 2)])
def test_o1_extra_counted_attempts_for_prerun_consumption(tmp_path, ledger, prerun, extra_allowed):
    path = tmp_path / 'attempts.jsonl'
    with path.open('w') as fh:
        for _ in range(prerun):
            for f in FIELDS:
                fh.write(json.dumps({'run': '2021-01-04', 'lead': 21, 'field': f, 'epoch': extract.PRERUN_CUTOFF_EPOCH - 5}) + '\n')
    a = extract.Attempts(path, ledger)
    for _ in range(extract.PRODUCTION_ATTEMPTS + extra_allowed):
        a.end('2021-01-04', 21, 'aws', a.begin('2021-01-04', 21, 'aws', 'production'), 'integrity_failure')
    with pytest.raises(IntegrityError):
        a.begin('2021-01-04', 21, 'aws', 'production')
    replaced = tmp_path / 'prerun_replacement_attempts.jsonl'
    assert (len(replaced.read_text().splitlines()) if replaced.exists() else 0) == 5 * extra_allowed
