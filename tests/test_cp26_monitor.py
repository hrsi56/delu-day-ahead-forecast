"""A restart must never represent a dead worker's later idle gap as measured compute."""
import importlib.util
import contextlib
import copy
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import pytest

from cp26 import budget as B
from cp26 import supervisor as S


@pytest.fixture
def driver():
    path = Path(__file__).resolve().parents[1] / 'scripts/cp26_rebaseline.py'
    spec = importlib.util.spec_from_file_location('cp26_resource_driver', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_dead_monitor_without_end_evidence_stops_without_charging_idle_time(driver, tmp_path, monkeypatch):
    monkeypatch.setattr(driver, 'art', lambda: tmp_path)
    job = {'started_epoch': 100.0, 'last_charge_epoch': 120.0, 'charged_wall_seconds': 20.0,
           'workers': 4, 'job_index': 0}
    with pytest.raises(RuntimeError, match='runtime is uncertain'):
        driver.reconciled_tail(job)
    assert job['charged_wall_seconds'] == 20.0


def test_completion_clock_reconciles_only_actual_duration_and_binds_the_job(driver, tmp_path, monkeypatch):
    monkeypatch.setattr(driver, 'art', lambda: tmp_path)
    clock = tmp_path / 'clock.json'
    job = {'job_index': 3, 'started_epoch': 100.0, 'charged_wall_seconds': 20.0, 'workers': 4,
           'completion_clock': str(clock)}
    receipt = {'job_index': 3, 'started_epoch': 100.0, 'wall_seconds': 25.0}
    clock.write_text(json.dumps(receipt))
    assert driver.reconciled_tail(job) == 20.0
    receipt['job_index'] = 2
    clock.write_text(json.dumps(receipt))
    with pytest.raises(RuntimeError, match='does not identify'):
        driver.reconciled_tail(job)
    receipt['job_index'] = 3
    receipt['wall_seconds'] = 19.0
    clock.write_text(json.dumps(receipt))
    with pytest.raises(RuntimeError, match='already measured'):
        driver.reconciled_tail(job)


def test_clock_outside_project_artifacts_is_refused(driver, tmp_path, monkeypatch):
    monkeypatch.setattr(driver, 'art', lambda: tmp_path / 'artifacts')
    with pytest.raises(ValueError, match='inside primary'):
        driver.reconciled_tail({'completion_clock': str(tmp_path / 'outside.json')})


def job_and_receipt():
    job = {'job_id': 'example-job', 'job_index': 0, 'started_epoch': 100.0,
           'request_sha256': 'a' * 64, 'workers': 4, 'running': True,
           'charged_wall_seconds': 20.0, 'monitor_identity': {'pid': 10, 'create_time': 1.0},
           'supervisor_identity': {'pid': 11, 'create_time': 2.0},
           'child_identity': {'pid': 12, 'create_time': 3.0},
           'worker_identities': [{'pid': 12, 'create_time': 3.0}], 'live_rss_bytes': 1}
    receipt = {'schema': 'cp26-completion-v2', 'job_id': 'example-job', 'job_index': 0,
               'started_epoch': 100.0, 'request_sha256': 'a' * 64, 'workers': 4,
               'supervisor_identity': job['supervisor_identity'], 'child_identity': job['child_identity'],
               'worker_identities': job['worker_identities'],
               'workers_stopped': True, 'group_empty': True, 'wall_seconds': 25.0,
               'ended_epoch': 125.0, 'exit_code': 7, 'abort_reason': None, 'peak_rss_bytes': 10}
    state = {'counts': {'machine_seconds': 80.0}, 'jobs': [job], 'peaks': {},
             'accounting': {'measured_seconds': 80.0, 'reported_seconds': 0.0, 'reserved_seconds': 0.0}}
    return state, job, receipt


def test_supervisor_receipt_reconciles_failed_work_exactly_once_without_idle_time():
    state, job, receipt = job_and_receipt()
    S.apply_completion(state, job, receipt)
    assert B.total_seconds(state) == 100.0
    assert job['exit_code'] == 7 and not job['running']
    # A later restart can repeat the import; neither its wall clock nor a second
    # receipt import charges the prefix or the idle gap again.
    S.apply_completion(state, job, receipt)
    assert B.total_seconds(state) == 100.0


@pytest.mark.parametrize('field,value', [('workers_stopped', False), ('group_empty', False),
                                         ('request_sha256', 'b' * 64), ('job_id', 'other'),
                                         ('worker_identities', [])])
def test_insufficient_or_wrong_end_evidence_blocks_without_charging(field, value):
    state, job, receipt = job_and_receipt()
    receipt[field] = value
    with pytest.raises(RuntimeError):
        S.apply_completion(state, job, receipt)
    assert B.total_seconds(state) == 80.0 and job['running']


def test_pid_reuse_does_not_count_new_process_as_old_worker(monkeypatch):
    class Replacement:
        def __init__(self, pid):
            self.pid = pid

        def create_time(self):
            return 200.0

        def status(self):
            return 'running'

    monkeypatch.setattr(S.psutil, 'Process', Replacement)
    assert S.identity_status({'pid': 12, 'create_time': 3.0}) == 'reused'
    assert S.identity_status({'pid': 12}) == 'unknown'
    state, job, receipt = job_and_receipt()
    S.reconcile_running(state, status=S.identity_status, load_receipt=lambda _: receipt)
    assert B.total_seconds(state) == 100.0 and not job['running']


def test_live_orphan_blocks_and_does_not_skip_declared_workers():
    state, job, _ = job_and_receipt()
    status = lambda identity: 'same' if identity == job['child_identity'] else 'gone'
    with pytest.raises(RuntimeError, match='orphaned CP-26 worker'):
        S.reconcile_running(state, status=status)
    assert B.total_seconds(state) == 80.0 and job['workers'] == 4 and job['running']


def test_legacy_monitor_pid_without_identity_cannot_hide_a_dead_worker():
    state, job, _ = job_and_receipt()
    del job['monitor_identity']
    job['monitor_pid'] = 10
    with pytest.raises(RuntimeError, match='legacy/unknown'):
        S.reconcile_running(state, status=lambda identity: 'unknown' if identity is None else 'gone')
    assert B.total_seconds(state) == 80.0


def test_hard_dead_supervisor_without_clock_blocks_even_after_workers_die(tmp_path, monkeypatch):
    state, job, _ = job_and_receipt()
    monkeypatch.setattr(S, 'art', lambda: tmp_path)
    with pytest.raises(RuntimeError, match='runtime is uncertain'):
        S.reconcile_running(state, status=lambda _: 'gone')
    assert B.total_seconds(state) == 80.0 and job['running']


def test_total_cap_and_repair_limit_include_reported_and_reserved_time(tmp_path):
    budget = B.Budget(tmp_path / 'ledger.json')
    budget.initialise()
    budget.record_charge('reported', B.CAPS['machine_seconds'] - 1, 'reported', {'source': 'test'})
    budget.record_charge('reserve', 1, 'reserved', {'source': 'bound'}, reserve_status='authorized')
    with pytest.raises(B.CapExceeded):
        B.require_compute_ready(budget.read())
    state = {'counts': {'machine_seconds': 0}, 'repair_scope': {'active': True, 'baseline_seconds': 0,
                                                               'limit_seconds': B.REPAIR_SECONDS}}
    B.add_seconds(state, B.REPAIR_SECONDS, 'reported')
    assert B.limit_reason(state) == 'repair_machine_hours_cap'


def test_unreconciled_reserve_is_charged_and_blocks_compute_idempotently(tmp_path):
    budget = B.Budget(tmp_path / 'ledger.json')
    budget.initialise()
    assert budget.record_charge('unknown-duration', 60, 'reserved', {'missing': 'receipt'})
    assert not budget.record_charge('unknown-duration', 60, 'reserved', {'missing': 'receipt'})
    assert B.total_seconds(budget.read()) == 60
    with pytest.raises(RuntimeError, match='unreconciled'):
        B.require_compute_ready(budget.read())
    with pytest.raises(ValueError, match='different evidence'):
        budget.record_charge('unknown-duration', 15.01, 'reserved', {'missing': 'receipt'})


def historical_ledger():
    return {'schema': 'cp26-ledger-v1', 'caps': B.CAPS.copy(),
            'counts': {'machine_seconds': B.HISTORICAL_SECONDS}, 'peaks': {},
            'jobs': [{'name': 'parity', 'running': False, 'workers': 1,
                      'wall_seconds': B.HISTORICAL_SECONDS - B.EARLY_REPORTED_SECONDS,
                      'ended_epoch': B.PARITY_END_EPOCH}],
            'events': [{'event': 'builder_lightweight_tests_before_monitor', 'workers': 1,
                        'observed_wall_seconds': [4.13, 1.995]}]}


def audit_bound():
    return {'schema': 'cp26-audit-time-bound-v1', 'thread_id': 'independent-audit',
            'turn_started_epoch': 1791907417, 'turn_completed_epoch': 1791908415}


def test_historical_reconciliation_preserves_old_spend_and_separates_reserve(tmp_path):
    path = tmp_path / 'ledger.json'
    B.atomic(path, historical_ledger())
    budget = B.Budget(path)
    preservation = 0.05587495904183015
    first = budget.reconcile_repair_history(audit_bound(), evidence_sha256='a' * 64,
                                            preservation_seconds=preservation)
    assert first['measured_seconds'] == pytest.approx(B.HISTORICAL_SECONDS - 6.125 + preservation)
    assert first['reported_seconds'] == pytest.approx(6.125 + 90.127)
    assert first['reserved_seconds'] == 2826
    assert first['total_seconds'] == pytest.approx(B.HISTORICAL_SECONDS + 90.127 + 2826 + preservation)
    assert first['repair_seconds_used'] == pytest.approx(preservation)
    assert not first['unreconciled_reserves']
    second = budget.reconcile_repair_history(audit_bound(), evidence_sha256='a' * 64,
                                             preservation_seconds=preservation)
    assert first == second
    charges = budget.read()['charges']
    assert sum(c['id'] == 'independent-audit-successful-tests' for c in charges) == 1
    reserve = next(c for c in charges if c['id'] == 'independent-audit-failed-test')
    assert not reserve['source']['exact_runtime_recovered']
    assert reserve['source']['failed_test_lower_bound_seconds'] == 15.01


def test_unbounded_historical_failure_refuses_reconciliation_without_mutation(tmp_path):
    path = tmp_path / 'ledger.json'
    B.atomic(path, historical_ledger())
    before = path.read_bytes()
    bound = audit_bound()
    bound['turn_started_epoch'] = B.PARITY_END_EPOCH - 1
    with pytest.raises(RuntimeError, match='does not bound'):
        B.Budget(path).reconcile_repair_history(bound, evidence_sha256='a' * 64)
    assert path.read_bytes() == before


def test_projection_prices_42_searches_and_every_prior_classification():
    state = {'counts': {'machine_seconds': 0}}
    B.add_seconds(state, 100, 'measured')
    B.add_seconds(state, 50, 'reported')
    B.add_seconds(state, 200, 'reserved')
    searches = [{'run': run, 'k': k, 'machine_seconds': 10, 'classification': 'conservative',
                 'basis': 'synthetic explicit bound'} for run in ('nominal', 'gfs6', 'noload') for k in range(14)]
    remaining = {name: {'machine_seconds': 20, 'classification': 'conservative', 'basis': 'synthetic bound'}
                 for name in ('daily_fits', 'parity', 'tests', 'bootstrap', 'diagnostics', 'failed_jobs_and_resume')}
    result = B.projected_cost(state, searches, remaining)
    assert result['projected_total_seconds'] == 100 + 50 + 200 + 420 + 120
    assert result['searches_priced'] == 42
    with pytest.raises(ValueError, match='42'):
        B.projected_cost(state, searches[:14], remaining)
    wrong_runs = copy.deepcopy(searches)
    for row in wrong_runs:
        row['run'] = {'nominal': 'foo', 'gfs6': 'bar', 'noload': 'baz'}[row['run']]
    with pytest.raises(ValueError, match='three runs'):
        B.projected_cost(state, wrong_runs, remaining)
    expensive = copy.deepcopy(searches)
    expensive[0]['machine_seconds'] = 436.5 * B.HOUR
    assert not B.projected_cost(state, expensive, remaining)['within_pilot_stop']


def wait_until(predicate, timeout=12):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        result = predicate()
        if result:
            return result
        time.sleep(0.025)
    raise AssertionError('monitored test process did not reach its expected state')


@contextlib.contextmanager
def real_monitor(tmp_path, command, workers=1, supervisor_code=None):
    root = Path(__file__).resolve().parents[1]
    artifacts = tmp_path / '.local' / 'artifacts' / 'cp-26'
    budget = B.Budget(artifacts / 'ledger' / 'budget.json')
    budget.initialise()
    child_env = os.environ.copy()
    child_env.update(CP26_PROJECT_ROOT=str(tmp_path), CP26_LEDGER=str(budget.path),
                     PYTHONPATH=str(root / 'src'), PYTHONDONTWRITEBYTECODE='1')
    launch = [sys.executable, '-B', str(root / 'scripts' / 'cp26_rebaseline.py'),
              'monitor', '--name', 'synthetic-monitor', '--workers', str(workers), '--', *command]
    if supervisor_code is not None:
        # Patch only the dedicated launcher's supervisor invocation. Its detached
        # watchdog imports the unmodified production implementation independently.
        launch_code = ('import importlib.util, subprocess, sys; '
                       f'spec=importlib.util.spec_from_file_location("driver", {str(root / "scripts" / "cp26_rebaseline.py")!r}); '
                       'driver=importlib.util.module_from_spec(spec); spec.loader.exec_module(driver); '
                       'original=subprocess.Popen; '
                       f'patch={supervisor_code!r}; '
                       '\ndef spawn(args, *pos, **kwargs):\n'
                       '    if args[2:4] == ["-m", "cp26.supervisor"]:\n'
                       '        args=[args[0], "-B", "-c", patch, args[-1]]\n'
                       '    return original(args, *pos, **kwargs)\n'
                       'driver.subprocess.Popen=spawn; '
                       f'sys.argv={launch[2:]!r}; raise SystemExit(driver.main())')
        launch = [sys.executable, '-B', '-c', launch_code]
    proc = subprocess.Popen(launch,
                            cwd=root, env=child_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, start_new_session=True)
    try:
        yield proc, budget
    finally:
        # Cleanup only processes these tests created, binding every signal to a
        # stored PID/create_time. Hard-death cases must leave no detached worker.
        state = budget.read()
        for job in state['jobs']:
            identities = [job.get('child_identity'), *job.get('worker_identities', []),
                          job.get('supervisor_identity'), job.get('watchdog_identity')]
            for identity in identities:
                if S.identity_status(identity) == 'same':
                    try:
                        os.kill(identity['pid'], signal.SIGKILL)
                    except ProcessLookupError:
                        pass
        if proc.poll() is None:
            proc.kill()
        proc.communicate(timeout=5)


def active_child(budget):
    jobs = budget.read()['jobs']
    return jobs[-1] if jobs and jobs[-1].get('child_identity') and jobs[-1]['charged_wall_seconds'] > 0 else None


def test_outer_monitor_hard_death_retains_independent_failed_job_receipt(tmp_path):
    command = [sys.executable, '-B', '-c', 'import time; time.sleep(1.0); raise SystemExit(7)']
    with real_monitor(tmp_path, command, workers=2) as (proc, budget):
        active_child(budget)
        wait_until(lambda: active_child(budget))
        proc.kill()
        proc.wait(timeout=5)
        wait_until(lambda: budget.read()['jobs'] and not budget.read()['jobs'][-1]['running'])
        state = budget.read()
        job = state['jobs'][-1]
        receipt = json.loads(Path(job['completion_clock']).read_text())
        assert receipt['workers_stopped'] and receipt['group_empty']
        assert job['exit_code'] == 7
        assert B.total_seconds(state) == pytest.approx(job['wall_seconds'] * 2)
        before = B.total_seconds(state)
        S.apply_completion(state, job, receipt)
        assert B.total_seconds(state) == before


def test_supervisor_hard_death_gets_independent_bound_ending_receipt(tmp_path, monkeypatch):
    command = [sys.executable, '-B', '-c', 'import time; time.sleep(30)']
    with real_monitor(tmp_path, command) as (proc, budget):
        job = wait_until(lambda: active_child(budget))
        assert S.identity_status(job['supervisor_identity']) == 'same'
        os.kill(job['supervisor_identity']['pid'], signal.SIGKILL)
        proc.wait(timeout=12)
        state = budget.read()
        measured = B.total_seconds(state)
        job = state['jobs'][-1]
        monkeypatch.setattr(S, 'art', lambda: tmp_path / '.local' / 'artifacts' / 'cp-26')
        S.reconcile_running(state)
        assert B.total_seconds(state) == measured
        assert S.identity_status(job['child_identity']) in ('gone', 'reused')
        receipt = json.loads(Path(job['completion_clock']).read_text())
        assert receipt['completion_issuer'] == 'watchdog'
        assert receipt['abort_reason'] == 'supervisor_identity_lost'
        assert receipt['workers_stopped'] and not job['running']
        assert receipt['wall_seconds'] > 0
        assert measured == pytest.approx(receipt['wall_seconds'])
        assert proc.returncode == 70


def test_registered_detached_worker_is_not_lost_when_parent_exits(tmp_path):
    marker = tmp_path / 'registered-worker.ready'
    worker = ('from cp26.supervisor import register_worker; from pathlib import Path; import time; '
              f'register_worker(); Path({str(marker)!r}).write_text("ready"); time.sleep(30)')
    parent = ('import subprocess, sys, time; from pathlib import Path; '
              f'p = subprocess.Popen([sys.executable, "-B", "-c", {worker!r}], start_new_session=True); '
              f'marker = Path({str(marker)!r}); '
              'deadline=time.monotonic()+10; '
              '\nwhile not marker.exists() and time.monotonic()<deadline: time.sleep(0.01)\n'
              'assert marker.exists()\n')
    # The root coordinator is conservatively one compute slot; the registered
    # detached worker needs a second declared slot.
    with real_monitor(tmp_path, [sys.executable, '-B', '-c', parent], workers=2) as (proc, budget):
        proc.wait(timeout=15)
        state = budget.read()
        job = state['jobs'][-1]
        assert not job['running'] and job['workers_stopped']
        assert job['abort_reason'] == 'orphaned_descendants'
        assert job.get('registered_worker_identities')
        assert all(S.identity_status(identity) in ('gone', 'reused')
                   for identity in job['registered_worker_identities'])
        assert proc.returncode == 70


def test_reused_root_and_group_are_never_adopted_signaled_or_certified(monkeypatch):
    original = {'pid': 77, 'create_time': 1.0}
    replacement = {'pid': 77, 'create_time': 2.0}
    signals = []
    class Replacement:
        def __init__(self, pid):
            self.pid = pid

        def create_time(self):
            return 2.0

        def status(self):
            return 'running'

        def send_signal(self, sig):
            signals.append((self.pid, sig))

    monkeypatch.setattr(S.psutil, 'Process', Replacement)
    monkeypatch.setattr(S, 'group_members', lambda _: [replacement])
    monkeypatch.setattr(S.os, 'killpg', lambda *args: signals.append(('group', args)))
    known = {}
    with pytest.raises(RuntimeError, match='unowned numeric'):
        S.worker_members(77, original, known)
    assert known == {}
    with pytest.raises(RuntimeError, match='unowned numeric'):
        S.terminate_workers(77, original, known)
    assert known == {} and signals == []
    end = S.ending_evidence(77, original, known, previously_stopped=True)
    assert not end['workers_stopped'] and not end['group_empty']
    assert 'unowned numeric' in end['ending_error']


def test_group_owner_exit_during_discovery_cannot_adopt_replacement(monkeypatch):
    original = {'pid': 77, 'create_time': 1.0}
    replacement = {'pid': 77, 'create_time': 2.0}
    checks = iter([True, False])
    monkeypatch.setattr(S, 'identity_status', lambda _: 'reused')
    monkeypatch.setattr(S, 'root_owns_group', lambda *args: next(checks))
    monkeypatch.setattr(S, 'group_members', lambda _: [replacement])
    known = {}
    with pytest.raises(RuntimeError, match='unowned numeric'):
        S.worker_members(77, original, known)
    assert known == {}


def test_known_escaped_worker_can_be_stopped_without_signaling_reused_group(monkeypatch):
    original = {'pid': 77, 'create_time': 1.0}
    replacement = {'pid': 77, 'create_time': 2.0}
    escaped = {'pid': 88, 'create_time': 3.0}
    live = {77: 2.0, 88: 3.0}
    signals = []
    class BoundProcess:
        def __init__(self, pid):
            if pid not in live:
                raise S.psutil.NoSuchProcess(pid)
            self.pid = pid

        def create_time(self):
            return live[self.pid]

        def status(self):
            return 'running'

        def children(self, recursive=False):
            return []

        def send_signal(self, sig):
            signals.append((self.pid, sig))
            del live[self.pid]

    monkeypatch.setattr(S.psutil, 'Process', BoundProcess)
    monkeypatch.setattr(S, 'group_members', lambda _: [replacement])
    monkeypatch.setattr(S.os, 'killpg', lambda *args: signals.append(('group', args)))
    known = {(88, 3.0): escaped}
    with pytest.raises(RuntimeError, match='unowned numeric'):
        S.terminate_workers(77, original, known)
    assert signals == [(88, signal.SIGTERM)]
    assert live == {77: 2.0}
    assert (77, 2.0) not in known


def registration_budget(tmp_path, workers=1, other_workers=0):
    budget = B.Budget(tmp_path / 'registration-ledger.json')
    budget.initialise()
    root = {'pid': 10, 'create_time': 1.0}
    with budget.transaction() as state:
        now = time.monotonic()
        state['jobs'].append({'job_id': 'registration-test', 'job_index': 0, 'running': True,
                              'phase': 'supervising', 'workers': workers, 'child_identity': root,
                              'charged_wall_seconds': 0.0, 'live_rss_bytes': 0,
                              'supervision_policy': S.SUPERVISION_POLICY.copy(),
                              'accounting_began_monotonic': now, 'accounting_observed_monotonic': now,
                              'accounting_sample_sequence': 1,
                              **{f'{role}_{key}': value for role in ('supervisor', 'watchdog')
                                 for key, value in {'identity': {'pid': 30 if role == 'supervisor' else 40,
                                                                 'create_time': 3.0},
                                                    'observed_monotonic': now, 'sample_sequence': 1,
                                                    'sample_wall_seconds': 0.0}.items()}})
        if other_workers:
            state['jobs'].append({'job_id': 'other', 'running': True, 'workers': other_workers,
                                  'child_identity': {'pid': 20, 'create_time': 2.0},
                                  'live_rss_bytes': 0})
    return budget


def setup_registration(monkeypatch, identity):
    monkeypatch.setenv('CP26_JOB_ID', 'registration-test')
    monkeypatch.setenv('CP26_JOB_INDEX', '0')
    monkeypatch.setattr(S, 'process_identity', lambda: identity)
    monkeypatch.setattr(S, 'identity_status', lambda _: 'same')


def test_denied_registration_persists_worker_and_explicit_budget_failure(tmp_path, monkeypatch):
    budget = registration_budget(tmp_path, workers=1)
    identity = {'pid': 11, 'create_time': 1.1}
    setup_registration(monkeypatch, identity)
    with pytest.raises(B.CapExceeded, match='before computation'):
        S.register_worker(budget)
    state = budget.read()
    job = state['jobs'][0]
    assert identity in job['worker_identities'] and identity in job['denied_worker_identities']
    assert identity not in job.get('registered_worker_identities', [])
    assert job['worker_ceiling_error']['job_active_compute_workers'] == 2
    assert job['worker_ceiling_error']['job_allocation'] == 1
    assert state['events'][-1]['event'] == 'worker_registration_denied'
    assert S.tick(budget, 0, 'registration-test', 0.1, 0) == 'registered_worker_ceiling'


def test_registered_worker_limit_counts_root_and_deduplicates_identity(tmp_path, monkeypatch):
    budget = registration_budget(tmp_path, workers=2)
    identity = {'pid': 11, 'create_time': 1.1}
    setup_registration(monkeypatch, identity)
    assert S.register_worker(budget) == identity
    assert S.register_worker(budget) == identity
    assert budget.read()['jobs'][0]['registered_worker_identities'] == [identity]
    second = {'pid': 12, 'create_time': 1.2}
    monkeypatch.setattr(S, 'process_identity', lambda: second)
    with pytest.raises(B.CapExceeded, match='before computation'):
        S.register_worker(budget)
    job = budget.read()['jobs'][0]
    assert job['worker_ceiling_error']['job_active_compute_workers'] == 3
    assert second in job['denied_worker_identities']


def test_global_four_worker_allocation_is_enforced_during_registration(tmp_path, monkeypatch):
    # Malformed/concurrent ledger state must not bypass the global check simply
    # because this job has spare individual slots.
    budget = registration_budget(tmp_path, workers=4, other_workers=1)
    identity = {'pid': 11, 'create_time': 1.1}
    setup_registration(monkeypatch, identity)
    with pytest.raises(B.CapExceeded, match='before computation'):
        S.register_worker(budget)
    job = budget.read()['jobs'][0]
    assert job['worker_ceiling_error']['global_declared_workers'] == 5
    assert identity in job['denied_worker_identities']


def test_real_denied_detached_worker_never_reaches_computation(tmp_path):
    marker = tmp_path / 'forbidden-computation.marker'
    worker = ('from cp26.supervisor import register_worker; from pathlib import Path; '
              f'register_worker(); Path({str(marker)!r}).write_text("computation started")')
    parent = ('import subprocess, sys; '
              f'p = subprocess.Popen([sys.executable, "-B", "-c", {worker!r}], start_new_session=True); '
              'p.wait()')
    with real_monitor(tmp_path, [sys.executable, '-B', '-c', parent], workers=1) as (proc, budget):
        proc.wait(timeout=15)
        job = budget.read()['jobs'][-1]
        assert not marker.exists()
        assert job.get('denied_worker_identities')
        assert job['worker_ceiling_error']['job_allocation'] == 1
        assert job['abort_reason'] == 'registered_worker_ceiling'
        assert not job['running'] and job['workers_stopped']
        assert proc.returncode == 70
