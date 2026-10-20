"""Three fixed interrupted jobs: retain negative receipts and bound their tails.

Uses the existing ledger/reserve representation and the same ending-supplement
procedure already recorded for job402. Never run during another owned job.
This observes later endings; it does not rewrite the first negative clocks.
"""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

BEGAN = time.monotonic()
root = Path.cwd().resolve()
sys.path.insert(0, str(root / 'src'))
from cp26 import budget as B, costing as C
from cp26.supervisor import ending_evidence, identity_status, process_identity

JOBS = {
    '190ee23d827149708a4bb2fd4cc91062': (418, 'db5bfd875beca684b9815cf061659eb781050fba09f461d9800cb14a51b4af29', 1961),
    '34c0d7c5f9f8455e9a1c788fc731b3ce': (424, '038496e48dc9bbf7002e497f37574b67094cad53b8386474074303e60cb6c931', 284),
    '622ad72156ee4092951ed20c8e84a127': (426, '4090c2a88de3e85d7a46a1241f0d63b346dc9893165fe76223b21064a1e128c1', 71),
}
directory = root / 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15'
self_path = Path(__file__).resolve()
assert subprocess.check_output(['git', 'show', f'HEAD:{self_path.relative_to(root)}']) == self_path.read_bytes()
budget = B.Budget()
state = budget.read()
assert all(not j.get('running') for j in state['jobs'] if j.get('job_id') not in JOBS)
authority = directory / 'issued-continuation-v21-r16.md'
authority_sha = hashlib.sha256(authority.read_bytes()).hexdigest()
keys = ('job_id', 'job_index', 'request_sha256', 'started_epoch', 'workers',
        'accounting_began_monotonic', 'child_identity', 'worker_pgid',
        'supervisor_identity', 'watchdog_identity', 'monitor_identity')
proofs = []
for job_id, (index, clock_sha, count) in JOBS.items():
    job = state['jobs'][index]
    assert job['job_id'] == job_id and job['run_id'] == B.COLD_RUN_ID
    raw = Path(job['completion_clock']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == clock_sha
    clock = json.loads(raw)
    assert clock['job_id'] == job_id and clock['request_sha256'] == job['request_sha256']
    assert clock['workers'] == job['workers'] == 1 and clock['exit_code'] == 70
    assert clock['workers_stopped'] is False and clock['group_empty'] is False
    known = {(i['pid'], i['create_time']): i for i in job['worker_identities']}
    assert len(known) == count
    statuses = {}
    for identity in known.values():
        status = identity_status(identity)
        assert status in ('gone', 'reused'), 'recorded worker remains alive or unknown'
        statuses[status] = statuses.get(status, 0) + 1
    roles = {role: identity_status(job[role + '_identity'])
             for role in ('monitor', 'supervisor', 'watchdog', 'child')}
    assert all(v in ('gone', 'reused') for v in roles.values())
    ending = ending_evidence(job['worker_pgid'], job['child_identity'], known, True)
    assert ending == {'workers_stopped': True, 'group_empty': True, 'ending_error': None}
    binding = {key: job.get(key) for key in keys}
    worker_sha = C.digest(job['worker_identities'])
    path = directory / f'clock-stop-{index}-ending-supplement-v21-r16.json'
    if path.exists():
        proof = json.loads(path.read_bytes())
        assert proof['content_sha256'] == C.digest({k:v for k,v in proof.items() if k != 'content_sha256'})
        assert proof['job_binding'] == binding and proof['original_clock_sha256'] == clock_sha
    else:
        observed = time.monotonic()
        upper = max(observed - job['accounting_began_monotonic'], clock['wall_seconds'])
        body = {'schema': 'cp26-one-job-ending-supplement-v1', 'run_id': B.COLD_RUN_ID,
                'issuer': 'Lead later ending observation; not a supervisor completion',
                'observer_identity': process_identity(), 'observed_epoch': time.time(),
                'observed_monotonic': observed, 'job_binding': binding,
                'original_clock_path': job['completion_clock'], 'original_clock_sha256': clock_sha,
                'recorded_worker_identities_sha256': worker_sha,
                'recorded_worker_identity_count': count, 'worker_statuses': statuses,
                'role_statuses': roles, 'ending_observation': ending,
                'measured_wall_seconds_preserved': job['charged_wall_seconds'],
                'elapsed_wall_upper_bound_seconds': upper,
                'additional_retained_reserve_seconds': upper - job['charged_wall_seconds'],
                'reserve_basis': 'Entire unmeasured interval through this verified empty-group observation, '
                                'including idle time, retained conservatively; never labelled measured runtime.',
                'authority': {'path': str(authority.relative_to(root)), 'sha256': authority_sha,
                              'scope': 'Existing ordinary operational-ledger and failed-job accounting grant; '
                                       'no new Owner decision or Integration PASS.'}}
        proof = {**body, 'content_sha256': C.digest(body)}
        path.write_text(json.dumps(proof, sort_keys=True, indent=1) + '\n')
    proofs.append((job_id, index, clock_sha, clock, binding, worker_sha, path, proof))

with budget.transaction(timeout_seconds=3.0) as current:
    assert all(not j.get('running') for j in current['jobs'] if j.get('job_id') not in JOBS)
    for job_id, index, clock_sha, clock, binding, worker_sha, path, proof in proofs:
        row = current['jobs'][index]
        assert {key: row.get(key) for key in keys} == binding
        assert C.digest(row['worker_identities']) == worker_sha
        assert hashlib.sha256(Path(row['completion_clock']).read_bytes()).hexdigest() == clock_sha
        charge_id = f'cold-r16-clock-stop-{index}-bounded-ending-reserve'
        source = {'run_id': B.COLD_RUN_ID, 'ending_supplement_path': str(path.relative_to(root)),
                  'ending_supplement_sha256': proof['content_sha256'],
                  'original_negative_clock_sha256': clock_sha,
                  'authority_document_sha256': authority_sha,
                  'basis': 'Bounded original-worker shutdown uncertainty through independently verified later ending.'}
        reserve = {'id': charge_id, 'seconds': proof['additional_retained_reserve_seconds'],
                   'kind': 'reserved', 'source': source, 'status': 'authorized'}
        matches = [c for c in current['charges'] if c['id'] == charge_id]
        if matches:
            assert len(matches) == 1 and all(matches[0][k] == v for k,v in reserve.items())
            assert not row['running'] and row['ending_evidence_supplement']['sha256'] == proof['content_sha256']
            continue
        assert row['running'] and row['charged_wall_seconds'] == proof['measured_wall_seconds_preserved']
        B.add_seconds(current, reserve['seconds'], 'reserved')
        current['charges'].append({**reserve, 'epoch': time.time()})
        current['reserves'].append(reserve.copy())
        row.update(running=False, phase='closed_after_verified_ending_supplement', live_rss_bytes=0,
                   exit_code=clock['exit_code'], abort_reason=clock['abort_reason'],
                   wall_seconds=row['charged_wall_seconds'], workers_stopped=True, group_empty=True,
                   ending_observed_epoch=proof['observed_epoch'],
                   ending_evidence_supplement={'path': str(path.relative_to(root)),
                       'sha256': proof['content_sha256'], 'original_negative_clock_sha256': clock_sha,
                       'retained_reserve_charge_id': charge_id})
after = budget.read()
assert not any(j.get('running') for j in after['jobs'])
B.require_compute_ready(after)
print(json.dumps({'status': 'THREE_FIXED_ENDINGS_RECONCILED',
                  'new_retained_reserve_seconds': sum(p[-1]['additional_retained_reserve_seconds'] for p in proofs),
                  'supplements': [{'index': p[1], 'sha256': p[-1]['content_sha256']} for p in proofs],
                  'resources': B.resource_summary(after),
                  'new_run': B.scientific_run_summary(after, B.COLD_RUN_ID),
                  'process_seconds': time.monotonic() - BEGAN}), flush=True)
