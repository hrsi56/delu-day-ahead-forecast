"""Add the finite operational close allowance to an existing completion price."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

from cp26 import budget as B, costing as C, execution as E, gates as G
from cp26.limits import STARTUP_GRACE_SECONDS, LEDGER_TIMEOUT_SECONDS, POLL_SECONDS
from cp26.supervisor import process_identity

root = Path.cwd()
label = sys.argv[1]
if label not in ('g05g06', 'g07g08', 'g09g10', 'closure'):
    raise ValueError('unregistered completion-pricing boundary')
directory = root / G.RUN_EVIDENCE
b = B.Budget()
descendant_proof = None
if label == 'g05g06':
    # One ordinary finite metadata descendant exercises the actual ending union.
    # The parent waits; no second model/fit/pool worker is started.
    child = subprocess.Popen(['/bin/cat'], stdin=subprocess.PIPE,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    identity = process_identity(child.pid)
    assert identity is not None
    seen = False
    limit = time.monotonic() + 3
    try:
        while time.monotonic() < limit:
            job = b.resource_read()['jobs'][int(os.environ['CP26_JOB_INDEX'])]
            if identity in job.get('worker_identities', []):
                seen = True
                break
            time.sleep(POLL_SECONDS)
    finally:
        child.stdin.close()
    child.wait(timeout=2)
    assert seen and child.returncode == 0
    descendant_proof = {'identity': identity, 'observed_in_authoritative_job': True,
                        'ended_before_pricing': True, 'exit_code': child.returncode}

base_path = G.OUTPUT / f'cost-projection-state-growth-v21-r16-{label}.json'
base = E._read(root / base_path)
C._verify(base, C.SCHEMA)
remaining = copy.deepcopy(base['remaining'])
bound = STARTUP_GRACE_SECONDS + LEDGER_TIMEOUT_SECONDS + POLL_SECONDS
remaining['bounded_caller_closing_handshakes'] = {
    'classification': 'conservative', 'machine_seconds': 24 * bound,
    'basis': 'Twenty-four remaining one-worker exit handshakes, each bounded by14s '
             'plus one existing3s ledger read and0.2s poll. Covers nine native windows, '
             'six replay prefixes, four analysis/report stages, three pricing calls '
             'and two review/closure calls. Retains every prior margin, failure and '
             'operational allowance. No timeout/heartbeat/termination limit changes.',
    'maximum_calls': 24, 'seconds_per_call': bound}
raw = b.path.read_bytes()
state = json.loads(raw)
priced = B.projected_cost(state, base['searches'], remaining, run_id=G.RUN_ID)
value = {k: v for k, v in copy.deepcopy(base).items() if k != 'content_sha256'}
value.update(priced)
value.update(remaining=remaining, ledger_seconds_at_pricing=B.total_seconds(state),
             ledger_sha256_at_pricing=hashlib.sha256(raw).hexdigest(),
             closing_allowance_source={'path': str(base_path),
                                       'content_sha256': base['content_sha256']},
             operational_wrapper_sha256=hashlib.sha256((directory/'quiescent-exit-v21-r16.py').read_bytes()).hexdigest(),
             pricing_job_id=os.environ['CP26_JOB_ID'], priced_epoch=time.time())
projection = C._signed(value)
path = G.OUTPUT / f'cost-projection-state-growth-v21-r16-{label}-close.json'
C.persist_projection(root, projection, output=path)
live = C.require_projection(projection, b.read())
run = B.scientific_run_summary(b.read(), G.RUN_ID)
prior_admission = E._read(directory / f'admission-state-growth-v21-r16-{label}.json')
admission = E._signed({
    'run_id': G.RUN_ID, 'status': 'PASS', 'projection_path': str(path),
    'projection_sha256': projection['content_sha256'],
    'cumulative_actual_hours': live['machine_hours'], 'new_run_actual': run,
    'projected_cumulative_completion_hours': live['projected_total_hours'],
    'projected_new_run_completion_hours': run['machine_hours']
        + (live['remaining_search_seconds'] + live['remaining_other_seconds']) / 3600,
    'component_hours': {k: v['machine_seconds']/3600 for k, v in remaining.items()},
    'remaining_wall_hours_three_native_workers':
        prior_admission['remaining_wall_hours_three_native_worker_fallback'] + 24*bound/3600,
    'historical_baseline_hours': run['historical_baseline_hours'],
    'admission_hours': 440., 'actual_hard_ceiling_hours': 500.,
    'real_descendant_observation': descendant_proof,
    'basis': 'Existing complete production-state-growth forecast plus a new finite '
             'closing allowance only. No old charge, reserve, cost factor, scientific '
             'source, frozen protocol, cache identity or successful probe is changed.'})
E._immutable(directory / f'admission-state-growth-v21-r16-{label}-close.json', admission)
print(json.dumps(admission), flush=True)
