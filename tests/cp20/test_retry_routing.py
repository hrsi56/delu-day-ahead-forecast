"""Per-lead routing under O2: integrity/object failures use the one alternate endpoint then
retry, a network error (raised only after a stop request) abandons the run uncounted, and an
exhausted counted allowance records a non-imputable failure."""
import argparse
import json

import numpy as np

from cp20 import extract
from cp20.budget import Budget
from cp20.gfs import FIELDS, IntegrityError, LEADS
from cp20.net import NetworkError, ObjectError


def make(tmp_path):
    b = Budget(tmp_path / 'ledger.json')
    b.initialise({})
    args = argparse.Namespace(out=str(tmp_path / 'out'), stop_transfer_gib=1.0, admission='reports/weather-admission')
    return extract.Extractor(args, b)


REC = {'run_00z': '2022-01-10', 'delivery_day': '2022-01-11', 'primary_endpoint': 'aws', 'alternate_endpoint': 'ncar',
       'retain_raw': False, 'object_bytes': {}}


def scripted(ex, script, calls):
    def body(run, lead, rec, endpoint, purpose):
        calls.append((lead, endpoint, purpose))
        outcome = script.get((lead, len([c for c in calls if c[0] == lead])))
        if outcome is not None:
            raise outcome
        return {f: (b'x', np.zeros((34, 41)), {'field': f, 'lead': lead, 'endpoint': endpoint, 'meta': {}}) for f in FIELDS}, None
    ex._lead_body = body


def test_object_and_integrity_failures_use_alternate_then_count(tmp_path):
    ex = make(tmp_path)
    calls = []
    scripted(ex, {(24, 1): ObjectError('HTTP 404'), (27, 1): IntegrityError('no 7777')}, calls)
    ex.run(REC)
    assert (24, 'ncar', 'alternate_endpoint') in calls and (27, 'ncar', 'alternate_endpoint') in calls
    assert json.loads((tmp_path / 'out/runs/2022-01-10.json').read_text())['status'] == 'complete'
    assert ex.attempts.used('2022-01-10', 24) == 1 and ex.attempts.used('2022-01-10', 21) == 0


def test_network_error_after_stop_abandons_run_without_counting(tmp_path):
    ex = make(tmp_path)
    calls = []
    scripted(ex, {(27, 1): NetworkError('stop requested during backoff')}, calls)
    ex.run(REC)
    assert not (tmp_path / 'out/runs/2022-01-10.json').exists()
    assert max(ex.attempts.used('2022-01-10', l) for l in LEADS) == 0
    outcomes = [json.loads(l)['outcome'] for l in (tmp_path / 'out/attempt-outcomes.jsonl').read_text().splitlines()]
    assert 'interrupted_by_stop' in outcomes and 'discarded_with_run' in outcomes


def test_two_counted_failures_exhaust_and_record_nonimputable_failure(tmp_path):
    ex = make(tmp_path)
    calls = []
    scripted(ex, {(21, 1): IntegrityError('bad'), (21, 2): IntegrityError('bad again')}, calls)
    ex.run(REC)
    failed = json.loads((tmp_path / 'out/failures.jsonl').read_text().splitlines()[0])
    assert failed['imputable'] is False and 'allowance exhausted' in failed['failures'][-1]['error']
    assert ex.attempts.used('2022-01-10', 21) == 2
