"""Real ledger refresh with three useful native jobs and one accounting slot."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp26 import budget as B, execution as E, gates as G

path = Path(__file__).resolve()
relative = str(path.relative_to(ROOT))
assert subprocess.check_output(['git', 'show', f'HEAD:{relative}']) == path.read_bytes()
G.authorize_consuming_process(ROOT)
job_id = os.environ.get('CP26_JOB_ID')
assert job_id and os.environ.get('CP26_RUN_ID') == G.RUN_ID
b = B.Budget()
state = b.read()
running = [j for j in state['jobs'] if j['running']]
native = [j for j in running if j['name'].startswith('cold-r16-fit-')]
assert len(native) == 3 and sum(j['workers'] for j in running) == 4
assert all(j['workers'] == 1 for j in native)

def healthy():
    for job in native:
        assert not Path(job['completion_clock']).exists()
        progress = json.loads(Path(job['progress_clock']).read_bytes())
        assert progress['job_id'] == job['job_id']
        assert progress['job_index'] == job['job_index']
        assert progress['request_sha256'] == job['request_sha256']
        assert time.time() - progress['observed_epoch'] < 8.

def observe_refresh():
    for _ in range(50):
        healthy()
        time.sleep(.2)

healthy()
source = {'run_id': G.RUN_ID, 'job_id': job_id,
          'basis': 'Zero-duration validation marker forcing a real canonical ledger '
                   'rewrite. This job duration is charged only by its supervisor.'}
began = time.monotonic()
assert b.record_charge('cold-r16-three-worker-canonical-refresh-marker', 0., 'reported', source)
assert not b.record_charge('cold-r16-three-worker-canonical-refresh-marker', 0., 'reported', source)
rewrite_seconds = time.monotonic() - began
observe_refresh()
evidence = {'run_id': G.RUN_ID, 'job_id': job_id,
            'native_job_ids': [j['job_id'] for j in native]}
assert E.record_evidence_once(b, 'cold-r16-three-worker-refresh-proof', evidence,
                            {'operational_three_worker_refresh_checks': 1})
assert not E.record_evidence_once(b, 'cold-r16-three-worker-refresh-proof', evidence,
                                {'operational_three_worker_refresh_checks': 1})
observe_refresh()
state = b.read()
for job in native:
    row = state['jobs'][job['job_index']]
    assert row['job_id'] == job['job_id'] and row['running']
    assert row['supervisor_ledger_lock_telemetry']['timeouts'] == 0
    assert row['watchdog_ledger_lock_telemetry']['timeouts'] == 0
assert len([c for c in state['charges'] if c['id'] ==
            'cold-r16-three-worker-canonical-refresh-marker']) == 1
assert state['counts']['operational_three_worker_refresh_checks'] == 1
healthy()
B.atomic(ROOT / 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/'
         'three-worker-refresh-check-v21-r16.json', {
    'validation_status': 'PASS', 'run_id': G.RUN_ID, 'job_id': job_id,
    'job_index': int(os.environ.get('CP26_JOB_INDEX', '-1')),
    'caller_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    'native_job_ids': [j['job_id'] for j in native],
    'ledger_bytes': b.path.stat().st_size, 'canonical_rewrite_seconds': rewrite_seconds,
    'duplicate_charge_imported': False, 'duplicate_task_imported': False,
    'operational_counter_value': 1, 'native_observer_timeouts': 0,
    'ledger_limit_seconds': 3., 'heartbeat_limit_seconds': 8.,
    'allocation': 'Three independent native workers plus one registered accounting/check worker.',
    'scope': 'Real full canonical rewrite and cold evidence append,20seconds of '
             'fresh native clocks, exactly-once charge/task/counter; no model fits '
             'in this checker, source change, timeout increase or synthetic ledger.'})
print('Three-worker real-ledger refresh and exactly-once checks PASS', flush=True)
