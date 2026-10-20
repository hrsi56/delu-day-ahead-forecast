"""One-job ending supplement; preserve the negative clock and bound its tail.

This is an ordinary operational-ledger reconciliation under the issued r16
grant, not a replacement supervisor receipt or a new Owner decision. It uses
the existing locked ledger, charge/reserve representation and both run views.
No source guard, worker binding, first receipt or historical charge is changed.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

root = Path.cwd().resolve()
sys.path.insert(0, str(root / 'src'))
from cp26 import budget as B, costing as C
from cp26.supervisor import ending_evidence, identity_status, process_identity

JOB_ID = '7c245a27b8894a13b9ea59d159e46707'
CLOCK_SHA = '6f321e20744145fdca08e52b1ddca0d7109d2612301e6e4f80e12c01f8147cc4'
CHARGE_ID = 'cold-r16-gfs6-402-bounded-ending-reserve'
directory = root / 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15'
path = Path(__file__).resolve()
assert subprocess.check_output(['git', 'show', f'HEAD:{path.relative_to(root)}']) == path.read_bytes()
budget = B.Budget()
state = budget.read()
job = next(j for j in state['jobs'] if j.get('job_id') == JOB_ID)
raw_clock = Path(job['completion_clock']).read_bytes()
assert hashlib.sha256(raw_clock).hexdigest() == CLOCK_SHA
clock = json.loads(raw_clock)
assert clock['job_id'] == JOB_ID and clock['request_sha256'] == job['request_sha256']
assert clock['workers'] == job['workers'] == 1
assert clock['workers_stopped'] is False and clock['group_empty'] is False
assert clock['exit_code'] == 70
assert all(not j.get('running') for j in state['jobs'] if j.get('job_id') != JOB_ID)
known = {(i['pid'], i['create_time']): i for i in job['worker_identities']}
assert len(known) == 1725
statuses = {}
for identity in known.values():
    status = identity_status(identity)
    assert status in ('gone', 'reused'), 'a worker ending remains unknown or alive'
    statuses[status] = statuses.get(status, 0) + 1
roles = {role: identity_status(job[f'{role}_identity'])
         for role in ('monitor', 'supervisor', 'watchdog', 'child')}
assert all(status in ('gone', 'reused') for status in roles.values())
ending = ending_evidence(job['worker_pgid'], job['child_identity'], known,
                         previously_stopped=True)
assert ending == {'workers_stopped': True, 'group_empty': True, 'ending_error': None}
binding_keys = ('job_id', 'job_index', 'request_sha256', 'started_epoch', 'workers',
                'accounting_began_monotonic', 'child_identity', 'worker_pgid',
                'supervisor_identity', 'watchdog_identity', 'monitor_identity')
binding = {key: job.get(key) for key in binding_keys}
workers_sha = C.digest(job['worker_identities'])
proof_path = directory / 'gfs6-402-ending-supplement-v21-r16.json'
authority_path = directory / 'issued-continuation-v21-r16.md'
authority_sha = hashlib.sha256(authority_path.read_bytes()).hexdigest()
if proof_path.exists():
    proof = json.loads(proof_path.read_bytes())
    assert proof['content_sha256'] == C.digest({k:v for k,v in proof.items() if k!='content_sha256'})
    assert proof['job_binding'] == binding and proof['original_clock_sha256'] == CLOCK_SHA
else:
    observed = time.monotonic()
    upper = max(observed - job['accounting_began_monotonic'], clock['wall_seconds'])
    assert upper >= job['charged_wall_seconds']
    body = {'schema': 'cp26-one-job-ending-supplement-v1', 'run_id': B.COLD_RUN_ID,
            'issuer': 'Lead ending observation; not a supervisor completion',
            'observer_identity': process_identity(), 'observed_epoch': time.time(),
            'observed_monotonic': observed, 'job_binding': binding,
            'original_clock_path': job['completion_clock'], 'original_clock_sha256': CLOCK_SHA,
            'recorded_worker_identities_sha256': workers_sha,
            'recorded_worker_identity_count': len(known), 'worker_statuses': statuses,
            'role_statuses': roles, 'ending_observation': ending,
            'measured_wall_seconds_preserved': job['charged_wall_seconds'],
            'elapsed_wall_upper_bound_seconds': upper,
            'additional_retained_reserve_seconds': upper - job['charged_wall_seconds'],
            'reserve_basis': 'Entire unmeasured interval through this verified empty-group '
                            'observation, including any idle portion, is retained as a '
                            'conservative reserve, never relabelled measured runtime.',
            'authority': {'path': str(authority_path.relative_to(root)), 'sha256': authority_sha,
                          'scope': 'Existing ordinary operational-ledger writes and failure '
                                   'accounting under the issued r16 execution grant. This '
                                   'supplement is not a new Owner grant or Integration PASS.'}}
    proof = {**body, 'content_sha256': C.digest(body)}
    proof_path.write_text(json.dumps(proof, sort_keys=True, indent=1) + chr(10))
source = {'run_id': B.COLD_RUN_ID, 'ending_supplement_path': str(proof_path.relative_to(root)),
          'ending_supplement_sha256': proof['content_sha256'],
          'original_negative_clock_sha256': CLOCK_SHA,
          'authority_document_sha256': authority_sha,
          'basis': 'One bounded shutdown uncertainty interval after all1725 recorded '
                   'identities and every original observer were verified gone/reused. '
                   'Retained conservatively under existing ordinary failure-accounting authority.'}
reserve = {'id': CHARGE_ID, 'seconds': proof['additional_retained_reserve_seconds'],
           'kind': 'reserved', 'source': source, 'status': 'authorized'}
with budget.transaction(timeout_seconds=3.0) as current:
    row = next(j for j in current['jobs'] if j.get('job_id') == JOB_ID)
    assert {key: row.get(key) for key in binding_keys} == binding
    assert C.digest(row['worker_identities']) == workers_sha
    assert hashlib.sha256(Path(row['completion_clock']).read_bytes()).hexdigest() == CLOCK_SHA
    matches = [c for c in current.get('charges', []) if c['id'] == CHARGE_ID]
    if matches:
        assert len(matches) == 1 and all(matches[0][k] == v for k,v in reserve.items())
        assert not row['running'] and row['ending_evidence_supplement']['sha256'] == proof['content_sha256']
    else:
        assert row['running'] and row['charged_wall_seconds'] == proof['measured_wall_seconds_preserved']
        B.add_seconds(current, reserve['seconds'], 'reserved')
        current.setdefault('charges', []).append({**reserve, 'epoch': time.time()})
        current.setdefault('reserves', []).append(reserve.copy())
        row.update(running=False, phase='closed_after_verified_ending_supplement',
                   live_rss_bytes=0, exit_code=clock['exit_code'], abort_reason=clock['abort_reason'],
                   wall_seconds=row['charged_wall_seconds'], workers_stopped=True, group_empty=True,
                   ending_observed_epoch=proof['observed_epoch'],
                   ending_evidence_supplement={'path': str(proof_path.relative_to(root)),
                                               'sha256': proof['content_sha256'],
                                               'original_negative_clock_sha256': CLOCK_SHA,
                                               'retained_reserve_charge_id': CHARGE_ID})
after = budget.read()
assert sum(c['id'] == CHARGE_ID for c in after['charges']) == 1
assert not any(j.get('running') for j in after['jobs'])
B.require_compute_ready(after)
print(json.dumps({'status': 'ONE_JOB_ENDING_RECONCILED', 'supplement_sha256': proof['content_sha256'],
                  'original_clock_sha256_preserved': CLOCK_SHA,
                  'new_retained_reserve_seconds': reserve['seconds'],
                  'resources': B.resource_summary(after),
                  'new_run': B.scientific_run_summary(after, B.COLD_RUN_ID)}), flush=True)
