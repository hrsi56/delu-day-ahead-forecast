"""Run one existing CP-26 entry point, then settle its ending observations.

The entry point runs in this same registered worker. No scheduler, resource
writer, fit/cache identity override or replacement completion receipt is used.
The existing supervisor/watchdog retain all enforcement and ending authority.
"""
from pathlib import Path
import hashlib
import json
import os
import runpy
import subprocess
import sys
import time


def committed(root, path):
    raw = path.read_bytes()
    relative = str(path.relative_to(root))
    if subprocess.check_output(['git', 'show', f'HEAD:{relative}'], cwd=root) != raw:
        raise RuntimeError('CP-26 operational caller must be committed')
    return hashlib.sha256(raw).hexdigest()


def settle_observers(budget=None):
    """Read-only, finite drain of late descendant observations before exit.

    A stable worker union must outlast one entire existing ledger deadline,
    plus two polls, and both observers must have sampled after that deadline.
    The supervisor's public progress must cover that same union. No subprocess
    is created here. Timeout is14s; a final ledger read/poll can add at most3.2s.
    Neither a timeout nor an unknown/replaced binding is treated as success.
    """
    from cp26.budget import Budget
    from cp26.gates import RUN_ID
    from cp26.limits import LEDGER_TIMEOUT_SECONDS, POLL_SECONDS, STARTUP_GRACE_SECONDS
    from cp26.supervisor import process_identity, require_fresh_supervision
    import psutil

    if os.environ.get('CP26_RUN_ID') != RUN_ID or not os.environ.get('CP26_MONITORED_JOB'):
        raise RuntimeError('closing handshake requires the existing registered run')
    index, job_id = int(os.environ['CP26_JOB_INDEX']), os.environ['CP26_JOB_ID']
    budget = budget or Budget()
    began = time.monotonic()
    deadline = began + STARTUP_GRACE_SECONDS
    own = process_identity()
    stable_since, previous, binding = began, None, None
    fields = ('job_id', 'job_index', 'request_sha256', 'child_identity',
              'supervisor_identity', 'watchdog_identity', 'monitor_identity')
    while True:
        if time.monotonic() >= deadline:
            raise RuntimeError('CP-26 closing observations did not settle within14seconds')
        job = budget.resource_read()['jobs'][index]
        if not job['running'] or job.get('job_id') != job_id or job.get('run_id') != RUN_ID:
            raise RuntimeError('CP-26 closing job is no longer the registered owner')
        if job.get('child_identity') != own:
            raise RuntimeError('CP-26 closing child identity changed')
        current_binding = {key: job.get(key) for key in fields}
        if binding is None:
            binding = current_binding
        elif binding != current_binding:
            raise RuntimeError('CP-26 closing supervision binding changed')
        require_fresh_supervision(job)
        workers = frozenset((i['pid'], i['create_time']) for i in job.get('worker_identities', []))
        now = time.monotonic()
        if workers != previous:
            previous, stable_since = workers, now
        progress = json.loads(Path(job['progress_clock']).read_bytes())
        progress_workers = frozenset((i['pid'], i['create_time'])
                                     for i in progress.get('worker_identities', []))
        matching = all(progress.get(key) == job.get(key)
                       for key in ('job_id', 'job_index', 'request_sha256'))
        settled = (now - stable_since >= LEDGER_TIMEOUT_SECONDS + 2 * POLL_SECONDS
                   and all(job.get(f'{role}_observed_monotonic', 0)
                           >= stable_since + LEDGER_TIMEOUT_SECONDS
                           for role in ('supervisor', 'watchdog')))
        children = [p for p in psutil.Process().children(recursive=True)
                    if p.is_running() and p.status() != psutil.STATUS_ZOMBIE]
        if matching and settled and progress_workers == workers and not children:
            return {'status': 'CLOSING_OBSERVERS_SETTLED', 'job_id': job_id,
                    'job_index': index, 'worker_identity_count': len(workers),
                    'quiet_seconds': now - stable_since, 'wall_seconds': now - began,
                    'maximum_wait_with_read_and_poll_seconds':
                        STARTUP_GRACE_SECONDS + LEDGER_TIMEOUT_SECONDS + POLL_SECONDS}
        time.sleep(POLL_SECONDS)


def main():
    root, own_path = Path.cwd().resolve(), Path(__file__).resolve()
    sys.path.insert(0, str(root / 'src'))
    own_sha = committed(root, own_path)
    if len(sys.argv) < 2:
        raise ValueError('supply one existing CP-26 Python entry point and its arguments')
    target = (root / sys.argv[1]).resolve()
    allowed = (target == root / 'scripts/cp26_rebaseline.py'
               or target.is_relative_to(root / 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15'))
    if not allowed or target.suffix != '.py' or target == own_path:
        raise ValueError('unregistered operational entry-point scope')
    target_sha = committed(root, target)
    sys.argv = [str(target), *sys.argv[2:]]
    try:
        runpy.run_path(str(target), run_name='__main__')
    except SystemExit as exc:
        if exc.code not in (None, 0):
            raise
    if hashlib.sha256(own_path.read_bytes()).hexdigest() != own_sha:
        raise RuntimeError('CP-26 operational wrapper changed during the job')
    proof = settle_observers()
    print(json.dumps({**proof, 'wrapper_sha256': own_sha,
                      'entry_point': str(target.relative_to(root)),
                      'entry_point_sha256': target_sha}), flush=True)


if __name__ == '__main__':
    main()
