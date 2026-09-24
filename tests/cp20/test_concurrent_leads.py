"""O4 (r12): concurrent leads inside one worker keep every per-message path unchanged."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import threading
import time

import numpy as np

from cp20 import extract
from cp20.budget import Budget
from cp20.gfs import FIELDS, IntegrityError, LEADS

REC = {'run_00z': '2022-01-10', 'delivery_day': '2022-01-11', 'primary_endpoint': 'aws', 'alternate_endpoint': 'ncar',
       'retain_raw': False, 'object_bytes': {}}


def make(tmp_path, name):
    b = Budget(tmp_path / f'{name}-ledger.json')
    b.initialise({})
    args = argparse.Namespace(out=str(tmp_path / name), stop_transfer_gib=1.0, admission='reports/weather-admission')
    return extract.Extractor(args, b)


def body_factory(delay=0.0, fail=None, live=None):
    def body(run, lead, rec, endpoint, purpose):
        if live is not None:
            with live['lock']:
                live['now'] += 1
                live['max'] = max(live['max'], live['now'])
        time.sleep(delay)
        if live is not None:
            with live['lock']:
                live['now'] -= 1
        if fail and lead in fail:
            raise IntegrityError('bad bytes')
        box = np.full((34, 41), float(lead))
        return {f: (b'x', box, {'field': f, 'lead': lead, 'endpoint': endpoint, 'sha256': f'{lead}{f}',
                                'meta': {'k': lead}}) for f in FIELDS}, None
    return body


def saved(ex, tmp_path, name):
    rec = json.loads((tmp_path / name / 'runs' / '2022-01-10.json').read_text())
    with np.load(tmp_path / name / 'runs' / '2022-01-10.npz') as z:
        return rec['messages'], z['data'].copy()


def test_leads_run_concurrently_up_to_the_pool_size(tmp_path):
    ex = make(tmp_path, 'c')
    live = {'now': 0, 'max': 0, 'lock': threading.Lock()}
    ex._lead_body = body_factory(0.2, live=live)
    began = time.time()
    with ThreadPoolExecutor(4) as pool:
        ex.run(REC, pool)
    assert live['max'] == 4 and time.time() - began < 1.5          # 10 leads x 0.2 s in 3 waves, not 2 s
    assert json.loads((tmp_path / 'c/runs/2022-01-10.json').read_text())['status'] == 'complete'


def test_concurrent_and_sequential_save_identical_records_and_arrays(tmp_path):
    seq, con = make(tmp_path, 's'), make(tmp_path, 'k')
    seq._lead_body = body_factory()
    con._lead_body = body_factory(0.01)
    seq.run(REC)
    with ThreadPoolExecutor(4) as pool:
        con.run(REC, pool)
    (ms, ds), (mc, dc) = saved(seq, tmp_path, 's'), saved(con, tmp_path, 'k')
    assert ms == mc and np.array_equal(ds, dc)
    assert [m['lead'] for m in mc] == [l for l in LEADS for _ in FIELDS]


def test_a_failing_lead_discards_successful_siblings_uncounted(tmp_path):
    ex = make(tmp_path, 'f')
    ex._lead_body = body_factory(0.01, fail={30})
    with ThreadPoolExecutor(4) as pool:
        ex.run(REC, pool)
    assert not (tmp_path / 'f/runs/2022-01-10.json').exists()
    failed = json.loads((tmp_path / 'f/failures.jsonl').read_text().splitlines()[0])
    assert failed['imputable'] is False and {x['lead'] for x in failed['failures']} == {30}
    assert ex.attempts.used('2022-01-10', 30) == 2 and ex.attempts.used('2022-01-10', 21) == 0
    outcomes = [json.loads(l) for l in (tmp_path / 'f/attempt-outcomes.jsonl').read_text().splitlines()]
    assert any(o['outcome'] == 'discarded_with_run' for o in outcomes)


def test_stop_mid_run_discards_everything(tmp_path):
    ex = make(tmp_path, 'x')
    body = body_factory(0.05)

    def stopping(run, lead, rec, endpoint, purpose):
        if lead == 33:
            ex.stop.set()
        return body(run, lead, rec, endpoint, purpose)
    ex._lead_body = stopping
    with ThreadPoolExecutor(2) as pool:
        ex.run(REC, pool)
    assert not (tmp_path / 'x/runs/2022-01-10.json').exists()
    assert not (tmp_path / 'x/failures.jsonl').exists()
