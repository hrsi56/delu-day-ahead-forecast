"""Sealed persistence timing and one prospective forecast in the existing CP-26 account."""
from datetime import date
from pathlib import Path
import hashlib
import json
import os
import sys
import time

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp25 import guard
from cp26.budget import atomic
from cp26.gates import RUN_ID, RUN_EVIDENCE, OUTPUT

LOCAL = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/cold-rerun-2026-10-15')
OLD = ROOT / 'reports/rebaseline/continuation-v21-r14-accounting-3'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def persistence_probe():
    # Resource metadata only. Never instantiate an old replay/H/learning object,
    # create a serving cache, or retain any old scientific payload in the new run.
    guard.admit_delivery_day(date(2021, 7, 28))
    path = OLD / 'replay-state.json'
    preserved = json.loads((ROOT / RUN_EVIDENCE / 'namespace-and-population.json').read_text())
    began = time.perf_counter()
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != preserved['old_hashes'][str(path.relative_to(ROOT))]:
        raise RuntimeError('historical resource sample changed')
    document = json.loads(raw)
    read_parse_seconds = time.perf_counter() - began
    if document['last_origin'] != '2021-07-28':
        raise RuntimeError('persistence size sample differs from the preserved 575-origin record')
    passes = []
    for _ in range(3):
        began = time.perf_counter()
        encoded = (json.dumps(document, sort_keys=True, allow_nan=False) + '\n').encode()
        hashlib.sha256(encoded).hexdigest()
        passes.append(time.perf_counter() - began)
    temporary = LOCAL / f'resource-serialization-{os.getpid()}.tmp'
    began = time.perf_counter()
    try:
        with temporary.open('xb') as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        write_seconds = time.perf_counter() - began
    finally:
        temporary.unlink(missing_ok=True)
    result = {'schema': 'cp26-cold-persistence-timing-v1', 'run_id': RUN_ID,
              'source': str(path.relative_to(ROOT)), 'source_sha256': sha(path),
              'source_origins': 575, 'source_bytes': len(raw), 'encoded_bytes': len(encoded),
              'read_parse_seconds': read_parse_seconds, 'encode_hash_seconds': passes,
              'write_flush_fsync_seconds': write_seconds, 'old_scientific_state_imported': False,
              'old_payload_retained_in_new_run': False, 'forecast_or_score_computed': False}
    atomic(ROOT / OUTPUT / 'persistence-timing.json', result)
    print(json.dumps(result), flush=True)



if __name__ == '__main__':
    if os.environ.get('CP26_RUN_ID') != RUN_ID or not os.environ.get('CP26_MONITORED_JOB'):
        raise RuntimeError('registered cold-run monitor required')
    persistence_probe()
