"""Per-lead retry routing: network stalls retry the same endpoint on a fresh connection, object
failures use the one alternate endpoint, bursts halt resumably; attempts stay within the ledger."""
import argparse
import json

import numpy as np
import pytest

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
    def lead(run, lead, rec, endpoint, purpose):
        ex.attempts.begin(run.isoformat(), lead, endpoint, purpose)
        calls.append((lead, endpoint, purpose))
        outcome = script.get((lead, len([c for c in calls if c[0] == lead])))
        if outcome is not None:
            raise outcome
        box = np.zeros((34, 41))
        return {f: (b'x', box, {'field': f, 'lead': lead, 'endpoint': endpoint, 'meta': {}}) for f in FIELDS}, None
    ex._lead = lead


def test_network_stall_retries_same_endpoint_object_error_uses_alternate(tmp_path):
    ex = make(tmp_path)
    calls = []
    scripted(ex, {(21, 1): NetworkError('stalled'), (24, 1): ObjectError('HTTP 404'), (27, 1): IntegrityError('no 7777')}, calls)
    ex.run(REC)
    assert (21, 'aws', 'transient_retry') in calls and (24, 'ncar', 'alternate_endpoint') in calls
    assert (27, 'ncar', 'alternate_endpoint') in calls
    assert json.loads((tmp_path / 'out/runs/2022-01-10.json').read_text())['status'] == 'complete'
    assert max(ex.attempts.used('2022-01-10', l) for l in LEADS) == 2


def test_two_failures_exhaust_production_and_record_nonimputable_failure(tmp_path):
    ex = make(tmp_path)
    calls = []
    scripted(ex, {(21, 1): NetworkError('stalled'), (21, 2): NetworkError('stalled again')}, calls)
    ex.run(REC)
    assert not (tmp_path / 'out/runs/2022-01-10.json').exists()
    failed = json.loads((tmp_path / 'out/failures.jsonl').read_text().splitlines()[0])
    assert failed['imputable'] is False and 'allowance exhausted' in failed['failures'][-1]['error']
    assert ex.attempts.used('2022-01-10', 21) == 2


def test_network_failure_burst_halts_resumably(tmp_path):
    ex = make(tmp_path)
    for _ in range(4):
        assert not ex._network_failure()
    assert ex._network_failure() and ex.reason == 'network_degraded' and ex.stop.is_set()
