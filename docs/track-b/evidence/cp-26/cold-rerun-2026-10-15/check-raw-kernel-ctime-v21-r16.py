"""Focused real-machine checks; no model fits, market reads or OS clock edits."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import psutil

root = Path.cwd()
sys.path.insert(0, str(root / 'src'))
from cp26 import budget as B, execution as E, gates as G
from cp26 import supervisor as S

assert os.environ.get('CP26_MONITORED_JOB') and os.environ.get('CP26_RUN_ID') == B.COLD_RUN_ID
directory = root / G.RUN_EVIDENCE
self_path = Path(__file__).resolve()
assert subprocess.check_output(['git', 'show', f'HEAD:{self_path.relative_to(root)}']) == self_path.read_bytes()
payload = json.loads(Path(sys.argv[1]).read_bytes())
bootstrap = directory / 'raw-kernel-ctime-v21-r16.py'
bootstrap_sha = hashlib.sha256(bootstrap.read_bytes()).hexdigest()
assert bootstrap_sha == payload['bootstrap_sha256']
prepared = json.loads((root / G.OUTPUT / 'preparation-tests-v21-r16.json').read_bytes())
assert prepared['status'] == 'PASS' and G.code_identity(root) == prepared['code_sha256']
assert (S.LEDGER_TIMEOUT_SECONDS, S.HEARTBEAT_TIMEOUT_SECONDS,
        S.STARTUP_GRACE_SECONDS, S.POLL_SECONDS) == (3.0, 8.0, 14.0, 0.2)
assert B.CAPS['machine_seconds'] == 500 * 3600 and B.CAPS['rss_bytes'] == 12000000000

budget = B.Budget()
before = budget.read()['accounting']['reported_seconds']
charge = payload['reported_charge']
assert budget.record_charge(charge['charge_id'], charge['seconds'], 'reported', charge['source'])
assert not budget.record_charge(charge['charge_id'], charge['seconds'], 'reported', charge['source'])
after = budget.read()
assert sum(c['id'] == charge['charge_id'] for c in after['charges']) == 1
assert abs(after['accounting']['reported_seconds'] - before - charge['seconds']) < 1e-8

own = S.process_identity()
assert own['create_time'] == psutil.Process()._get_ident()[1]
backend = psutil._psplatform
original_boot = backend.boot_time
clock_cases = []
try:
    for delta in (-2.0, 2.0):
        backend.boot_time = lambda delta=delta: backend.INIT_BOOT_TIME + delta
        legacy = backend.Process(os.getpid()).create_time()
        stable = psutil.Process().create_time()
        assert legacy != own['create_time'], 'legacy clock-sensitive path was not reproduced'
        assert stable == own['create_time'] and S.identity_status(own) == 'same'
        assert psutil.Process().is_running()
        wrong = {**own, 'create_time': own['create_time'] + 17.0}
        assert S.identity_status(wrong) == 'reused'
        assert S.signal_identity(wrong, signal.SIGTERM) is False
        clock_cases.append({'simulated_boot_offset_seconds': delta,
                            'legacy_birth_changed': True, 'raw_birth_unchanged': True,
                            'real_process_still_owned': True, 'wrong_birth_signal_refused': True})
finally:
    backend.boot_time = original_boot

probe_name = 'cold-r16-raw-clock-stop-probe-1'
assert not any(j.get('name') == probe_name for j in budget.read()['jobs'])
local = B.art() / 'cold-rerun-2026-10-15/r16'
log = local / (probe_name + '.log')
code = ("import json,time,psutil; "
        "assert psutil.Process().create_time()==psutil.Process()._get_ident()[1]; "
        "print(json.dumps({'status':'RAW_CLOCK_PROBE_READY'}),flush=True); time.sleep(120)")
command = [sys.executable, '-B', str(bootstrap), '--sha', bootstrap_sha, 'code', code]
args = [sys.executable, '-B', str(bootstrap), '--sha', bootstrap_sha, 'script',
        'scripts/cp26_rebaseline.py', 'monitor', '--name', probe_name,
        '--workers', '1', '--log', str(log), '--', *command]
probe_job = None
probe = None
try:
    with log.with_suffix('.launcher.log').open('ab') as output:
        probe = subprocess.Popen(args, cwd=root, env=os.environ.copy(), stdin=subprocess.DEVNULL,
                                 stdout=output, stderr=subprocess.STDOUT, start_new_session=True)
    startup_deadline = time.monotonic() + 14.0
    while not log.exists() or 'RAW_CLOCK_PROBE_READY' not in log.read_text():
        assert probe.poll() is None and time.monotonic() < startup_deadline
        time.sleep(0.2)
    state = budget.read()
    probe_job = next(j for j in state['jobs'] if j.get('name') == probe_name)
    assert sum(j['workers'] for j in state['jobs'] if j.get('running')) == 2
    S.require_fresh_supervision(probe_job)
    # Stop at a known non-lock-holding boundary; this is the focused heartbeat
    # check. Existing actual-ledger-expiry checks remain applicable unchanged.
    lock_deadline = time.monotonic() + 3.0
    with budget.path.with_suffix('.lock').open('a') as lock:
        while True:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                assert time.monotonic() < lock_deadline
                time.sleep(0.025)
        stopped_at = time.monotonic()
        assert S.signal_identity(probe_job['supervisor_identity'], signal.SIGSTOP)
        stop_deadline = stopped_at + 0.2
        while psutil.Process(probe_job['supervisor_pid']).status() != psutil.STATUS_STOPPED:
            assert time.monotonic() < stop_deadline
            time.sleep(0.01)
    deadline = stopped_at + 38.4
    clock_path = Path(probe_job['completion_clock'])
    while not clock_path.exists():
        assert time.monotonic() < deadline, 'stopped-observer ending exceeded existing38.4second bound'
        time.sleep(0.2)
    latency = time.monotonic() - stopped_at
    assert latency <= 38.4
    probe.wait(timeout=5)
    state = budget.read()
    probe_job = state['jobs'][probe_job['job_index']]
    receipt = S.completion_receipt(probe_job)
    S.check_completion(probe_job, receipt)
    assert not probe_job['running'] and receipt['workers_stopped'] and receipt['group_empty']
    assert receipt['exit_code'] == 70 and receipt['abort_reason'] == 'supervisor_heartbeat_stale'
    assert S.identity_status(probe_job['child_identity']) in ('gone', 'reused')
finally:
    if probe is not None and probe.poll() is None and probe_job is not None:
        # Only these controlled test identities may be signalled on test failure.
        for role in ('child', 'supervisor', 'watchdog', 'monitor'):
            S.signal_identity(probe_job.get(role + '_identity'), signal.SIGKILL)
        probe.wait(timeout=5)

result = E._signed({'status': 'PASS', 'run_id': B.COLD_RUN_ID,
                   'bootstrap_sha256': bootstrap_sha, 'scientific_code_sha256': prepared['code_sha256'],
                   'scientific_core_files_unchanged': True, 'clock_adjustment_cases': clock_cases,
                   'os_clock_changed': False, 'installed_dependency_files_changed': False,
                   'reported_charge_id': charge['charge_id'], 'reported_charge_occurrences': 1,
                   'probe_job_id': probe_job['job_id'], 'probe_job_index': probe_job['job_index'],
                   'probe_clock_sha256': hashlib.sha256(clock_path.read_bytes()).hexdigest(),
                   'probe_wall_seconds': receipt['wall_seconds'],
                   'stopped_observer_ending_seconds': latency, 'existing_bound_seconds': 38.4,
                   'probe_abort_reason': receipt['abort_reason'], 'probe_workers_stopped': True,
                   'probe_group_empty': True,
                   'scope': 'Focused clock/ownership/once-only-accounting checks and one real stopped-observer '
                            'probe. Controller reserves one slot and probe one slot. No scientific fit or '
                            'pilot rerun, no PID-only/tolerant identity match, and no resource-limit change.'})
path = directory / 'raw-kernel-ctime-checks-v21-r16.json'
assert not path.exists()
path.write_text(json.dumps(result, sort_keys=True, indent=1) + '\n')
print(json.dumps({'status': 'RAW_KERNEL_CTIME_CHECKS_PASS', 'content_sha256': result['content_sha256'],
                  'probe_job_id': probe_job['job_id'], 'probe_job_index': probe_job['job_index'],
                  'stopped_observer_ending_seconds': latency}), flush=True)
