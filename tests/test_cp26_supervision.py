"""Dedicated-process freshness/fail-safe tests; never signal an unrelated process."""
import copy
import json
import os
from pathlib import Path
import signal
import sys
import time

import pytest

from cp26 import budget as B
from cp26 import supervisor as S
from test_cp26_monitor import active_child, job_and_receipt, real_monitor, wait_until


def fresh_job(now=100.0):
    _, job, _ = job_and_receipt()
    job.update(phase='supervising', supervision_policy=S.SUPERVISION_POLICY.copy(),
               reserved_monotonic=80.0, accounting_began_monotonic=80.0,
               accounting_observed_monotonic=now, accounting_sample_sequence=2,
               charged_wall_seconds=now - 80.0, live_rss_bytes=10,
               watchdog_identity={'pid': 13, 'create_time': 4.0})
    for role in ('supervisor', 'watchdog'):
        job.update({f'{role}_observed_monotonic': now,
                    f'{role}_sample_sequence': 1,
                    f'{role}_sample_child_identity': job['child_identity'],
                    f'{role}_sample_wall_seconds': now - 80.0})
    return job


def test_hour_old_live_supervisor_cannot_admit_more_compute():
    job = fresh_job()
    state = {'jobs': [job]}
    with pytest.raises(RuntimeError, match='stale or unmeasured'):
        S.reconcile_running(state, status=lambda _: 'same', now=3700.0)
    assert job['running'] and job['charged_wall_seconds'] == 20.0


@pytest.mark.parametrize('field,value', [
    ('supervisor_sample_sequence', 0), ('watchdog_sample_sequence', 0),
    ('accounting_sample_sequence', 0), ('live_rss_bytes', None),
    ('supervisor_sample_wall_seconds', 1.0), ('charged_wall_seconds', 0.0),
    ('accounting_observed_monotonic', 90.0), ('watchdog_observed_monotonic', 90.0),
])
def test_fresh_epoch_without_time_rss_progress_fails_closed(field, value):
    job = fresh_job()
    job[field] = value
    with pytest.raises(RuntimeError):
        S.require_fresh_supervision(job, status=lambda _: 'same', now=100.0)


def test_startup_grace_reserves_workers_only_and_expires():
    job = fresh_job()
    job.update(phase='reserved', child_identity=None, supervisor_identity=None,
               watchdog_identity=None, reserved_monotonic=100.0)
    assert S.startup_is_fresh(job, now=105.0)
    S.reconcile_running({'jobs': [job]}, status=lambda identity: 'same' if identity else 'unknown', now=105.0)
    with pytest.raises(RuntimeError, match='supervisor identity'):
        S.reconcile_running({'jobs': [job]}, status=lambda identity: 'same' if identity else 'unknown',
                            now=100.0 + S.STARTUP_GRACE_SECONDS + 1.0)
    job['child_identity'] = {'pid': 12, 'create_time': 3.0}
    assert not S.startup_is_fresh(job, now=105.0)


def test_worker_exec_gate_refuses_stale_supervision(monkeypatch, tmp_path):
    job = fresh_job(now=time.monotonic() - 3600)
    own = job['child_identity']
    class Snapshot:
        def read(self):
            return {'jobs': [job]}
    request = {'job_index': 0, 'job_id': job['job_id'], 'command': ['forbidden']}
    monkeypatch.setattr(S, 'load_request', lambda _: (request, 'a' * 64, Snapshot()))
    monkeypatch.setattr(S, 'process_identity', lambda: own)
    monkeypatch.setattr(S, 'identity_status', lambda _: 'same')
    executions = []
    monkeypatch.setattr(S.os, 'execvpe', lambda *args: executions.append(args))
    with pytest.raises(RuntimeError, match='stale or unmeasured'):
        S.worker_gate(tmp_path / 'unused.json')
    assert executions == []


def long_worker(marker):
    return [sys.executable, '-B', '-c',
            f'from pathlib import Path; import time; Path({str(marker)!r}).write_text("active"); time.sleep(30)']


@pytest.mark.parametrize('lose_launcher', [False, True])
@pytest.mark.stress
def test_sigstop_supervisor_stops_verified_worker_even_after_launcher_loss(tmp_path, monkeypatch, lose_launcher):
    marker = tmp_path / 'active.marker'
    with real_monitor(tmp_path, long_worker(marker)) as (proc, budget):
        job = wait_until(lambda: active_child(budget) if marker.exists() else None)
        if lose_launcher:
            proc.kill()
            proc.wait(timeout=5)
        assert S.signal_identity(job['supervisor_identity'], signal.SIGSTOP)
        wait_until(lambda: not budget.read()['jobs'][-1]['running'])
        terminal = budget.read()['jobs'][-1]
        receipt = json.loads(Path(terminal['completion_clock']).read_text())
        assert receipt['completion_issuer'] == 'watchdog'
        assert 'supervisor_heartbeat_stale' in receipt['abort_reason']
        assert terminal['workers_stopped'] and terminal['group_empty']
        assert S.identity_status(job['child_identity']) in ('gone', 'reused')
        assert S.identity_status(job['supervisor_identity']) in ('gone', 'reused')
        assert receipt['wall_seconds'] > 0
        assert B.total_seconds(budget.read()) == pytest.approx(receipt['wall_seconds'])
        # Restart imports only the independently observed terminal duration,
        # regardless of how much time passes after worker termination.
        state = budget.read()
        before = B.total_seconds(state)
        restarted = copy.deepcopy(state)
        monkeypatch.setattr(S, 'art', lambda: tmp_path / '.local' / 'artifacts' / 'cp-26')
        S.reconcile_running(restarted, now=time.monotonic() + 3600)
        S.apply_completion(restarted, restarted['jobs'][-1], receipt)
        assert B.total_seconds(restarted) == before
        if not lose_launcher:
            proc.wait(timeout=5)
            assert proc.returncode == 70


@pytest.mark.stress
def test_supervisor_stopped_inside_ledger_lock_is_killed_before_receipt(tmp_path):
    marker = tmp_path / 'worker.marker'
    lock_marker = tmp_path / 'supervisor-lock.marker'
    patch = ('from pathlib import Path; import os, signal, sys, time; '
             'from cp26 import supervisor as S; original=S.tick; '
             f'marker=Path({str(lock_marker)!r}); '
             f'active_marker=Path({str(marker)!r}); '
             '\ndef blocked_tick(budget, index, job_id, wall, rss, **kwargs):\n'
             '    job=budget.read()["jobs"][index]\n'
             '    if active_marker.exists() and not marker.exists():\n'
             '        with budget.transaction():\n'
             '            marker.write_text("supervisor owns lock")\n'
             '            os.kill(os.getpid(), signal.SIGSTOP)\n'
             '            time.sleep(30)\n'
             '    return original(budget, index, job_id, wall, rss, **kwargs)\n'
             'S.tick=blocked_tick; raise SystemExit(S.run(Path(sys.argv[1])))')
    with real_monitor(tmp_path, long_worker(marker), supervisor_code=patch) as (proc, budget):
        wait_until(lambda: lock_marker.exists())
        job = budget.read()['jobs'][-1]
        wait_until(lambda: not budget.read()['jobs'][-1]['running'])
        terminal = budget.read()['jobs'][-1]
        receipt = json.loads(Path(terminal['completion_clock']).read_text())
        assert receipt['completion_issuer'] == 'watchdog'
        assert 'ledger accounting lock did not progress' in receipt['abort_reason']
        assert S.identity_status(job['supervisor_identity']) in ('gone', 'reused')
        assert S.identity_status(job['child_identity']) in ('gone', 'reused')
        assert receipt['wall_seconds'] >= job['charged_wall_seconds'] > 0
        assert B.total_seconds(budget.read()) == pytest.approx(receipt['wall_seconds'])
        proc.wait(timeout=5)
        assert proc.returncode == 70


@pytest.mark.stress
def test_stopped_watchdog_is_detected_by_supervisor(tmp_path):
    marker = tmp_path / 'active.marker'
    with real_monitor(tmp_path, long_worker(marker)) as (proc, budget):
        job = wait_until(lambda: active_child(budget) if marker.exists() else None)
        began = time.monotonic()
        assert S.signal_identity(job['watchdog_identity'], signal.SIGSTOP)
        from cp26.limits import shutdown_exposure_seconds
        proc.wait(timeout=shutdown_exposure_seconds(1))
        terminal = budget.read()['jobs'][-1]
        assert not terminal['running'] and terminal['workers_stopped']
        # SIGSTOP can catch the watchdog while it owns flock. In that case
        # the independent monitor retires both stale accounting writers.
        assert ('watchdog_heartbeat_stale' in terminal['abort_reason']
                or 'ledger accounting lock did not progress' in terminal['abort_reason'])
        assert time.monotonic() - began <= shutdown_exposure_seconds(1)
        receipt = json.loads(Path(terminal['completion_clock']).read_text())
        assert receipt['completion_issuer'] in ('supervisor', 'monitor')
        assert receipt['completion_issuer_identity'] == terminal[receipt['completion_issuer'] + '_identity']
        assert S.identity_status(job['child_identity']) in ('gone', 'reused')
        assert S.identity_status(job['watchdog_identity']) in ('gone', 'reused')
        assert proc.returncode == 70


@pytest.mark.stress
def test_launcher_shutdown_receipts_workers_and_watchdog(tmp_path):
    marker = tmp_path / 'active.marker'
    with real_monitor(tmp_path, long_worker(marker)) as (proc, budget):
        job = wait_until(lambda: active_child(budget) if marker.exists() else None)
        proc.terminate()
        proc.wait(timeout=12)
        terminal = budget.read()['jobs'][-1]
        assert not terminal['running'] and terminal['workers_stopped']
        assert terminal['abort_reason'] == f'signal_{signal.SIGTERM}'
        assert S.identity_status(job['child_identity']) in ('gone', 'reused')
        assert S.identity_status(job['watchdog_identity']) in ('gone', 'reused')
        assert proc.returncode == 70


def test_watchdog_pid_reuse_cannot_certify_fresh_supervision_or_receive_signals(monkeypatch):
    job = fresh_job()
    with pytest.raises(RuntimeError, match='watchdog identity'):
        S.require_fresh_supervision(job, now=100.0,
                                   status=lambda identity: 'reused' if identity == job['watchdog_identity'] else 'same')
    signals = []
    class Replacement:
        def __init__(self, pid):
            self.pid = pid
        def create_time(self):
            return 99.0
        def send_signal(self, sig):
            signals.append(sig)
    monkeypatch.setattr(S.psutil, 'Process', Replacement)
    assert not S.signal_identity(job['watchdog_identity'], signal.SIGKILL)
    assert signals == []


def test_watchdog_receipt_rejects_identity_or_request_substitution():
    state, job, receipt = job_and_receipt()
    job['watchdog_identity'] = {'pid': 13, 'create_time': 4.0}
    receipt.update(watchdog_identity=job['watchdog_identity'], completion_issuer='watchdog',
                   completion_issuer_identity=job['watchdog_identity'])
    S.check_completion(job, receipt)
    for field, wrong in [('watchdog_identity', {'pid': 13, 'create_time': 99.0}),
                         ('completion_issuer_identity', {'pid': 13, 'create_time': 99.0}),
                         ('request_sha256', 'b' * 64), ('child_identity', {'pid': 12, 'create_time': 99.0})]:
        invalid = {**receipt, field: wrong}
        with pytest.raises(RuntimeError):
            S.apply_completion(state, job, invalid)
        assert job['running'] and B.total_seconds(state) == 80.0


def test_serialized_sampler_ticks_do_not_regress_or_double_charge(tmp_path):
    budget = B.Budget(tmp_path / 'ledger.json')
    budget.initialise()
    job = fresh_job()
    job.update(charged_wall_seconds=0.0, live_rss_bytes=0,
               supervisor_sample_wall_seconds=0.0, watchdog_sample_wall_seconds=0.0)
    with budget.transaction() as state:
        state['jobs'].append(job)
    S.tick(budget, 0, job['job_id'], 2.0, 100, sample_role='watchdog')
    S.tick(budget, 0, job['job_id'], 1.0, 50, sample_role='supervisor')
    observed = budget.read()
    assert B.total_seconds(observed) == 8.0
    assert observed['jobs'][0]['charged_wall_seconds'] == 2.0
    assert observed['jobs'][0]['live_rss_bytes'] == 100
    assert observed['jobs'][0]['supervisor_sample_sequence'] == 2
    with pytest.raises(RuntimeError, match='observer elapsed clock regressed'):
        S.tick(budget, 0, job['job_id'], 0.5, 50, sample_role='supervisor')
    assert B.total_seconds(budget.read()) == 8.0


@pytest.mark.stress
def test_launcher_enforces_when_both_accounting_loops_are_stopped(tmp_path):
    marker = tmp_path / 'active.marker'
    with real_monitor(tmp_path, long_worker(marker)) as (proc, budget):
        job = wait_until(lambda: active_child(budget) if marker.exists() else None)
        assert S.signal_identity(job['watchdog_identity'], signal.SIGSTOP)
        assert S.signal_identity(job['supervisor_identity'], signal.SIGSTOP)
        proc.wait(timeout=12)
        terminal = budget.read()['jobs'][-1]
        receipt = json.loads(Path(terminal['completion_clock']).read_text())
        assert receipt['completion_issuer'] == 'monitor'
        assert receipt['abort_reason'].startswith('monitor_failsafe:')
        assert terminal['workers_stopped'] and not terminal['running']
        assert all(S.identity_status(job[f'{role}_identity']) in ('gone', 'reused')
                   for role in ('child', 'supervisor', 'watchdog'))
        assert B.total_seconds(budget.read()) == pytest.approx(receipt['wall_seconds'])
