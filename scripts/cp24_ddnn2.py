"""CP-24 driver (capstone v21-r11 §23). Every compute job runs under ``monitor``.

    python scripts/cp24_ddnn2.py init-ledger
    python scripts/cp24_ddnn2.py status
    python scripts/cp24_ddnn2.py pause|resume --reason <text>
    python scripts/cp24_ddnn2.py raise --counter <name> --to <value> --steering <committed path>
    python scripts/cp24_ddnn2.py monitor --name <job> --workers <n> --log <path> [--expected-minutes m] -- \
        python scripts/cp24_ddnn2.py job <job-name> [options]

The monitor owns the job's resource accounting (§23.11): it charges machine time as wall-clock x
declared workers, samples the process-tree RSS and the aggregate of all running CP-24 jobs, measures
added disk, refuses a duplicate instance or a fifth concurrent worker, terminates a job at any
hard cap (with every committed §23.6 raise applied), and writes a
completion marker. A job whose monitor died is reconciled on the next start with a conservative tail
charge; accounting is never reset.
"""
from __future__ import annotations

import argparse
import fcntl
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path(os.environ.get('CP24_PROJECT_ROOT', '/Users/djourno/Downloads/PJM'))
LOCAL = PROJECT / '.local'
ART = LOCAL / 'artifacts' / 'cp-24'
PY = PROJECT / '.venv' / 'bin' / 'python'
sys.path.insert(0, str(ROOT / 'src'))
BLAS = ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
        'NUMEXPR_NUM_THREADS')
for _name in BLAS:
    os.environ[_name] = '1'
from cp24.budget import (CAPS, TIMEBOX_ACTIVE_SECONDS, Budget, atomic, dir_bytes,  # noqa: E402
                         effective_caps, ledger_path, pid_alive)

TICK = 1.0
DISK_EVERY = 60.0
RECONCILE_TAIL_SECONDS = 60.0


def disk_paths():
    return {'git': PROJECT / '.git',
            'cp24_local': [LOCAL / 'worktrees' / 'cp-24', ART, LOCAL / 'tmp' / 'cp-24', LOCAL / 'mlruns' / 'cp24']}


def measure_disk(baseline):
    """Added = growth of the shared .git + every byte under the CP-24 local paths, which include the
    Lead and Critic worktrees in full (their whole checkout counts as added disk)."""
    paths = disk_paths()
    git = dir_bytes([paths['git']])
    local = dir_bytes(paths['cp24_local'])
    added = max(0, git - baseline['git_bytes']) + local
    return added, {'git_bytes': git, 'cp24_local_bytes': local}


def init_ledger():
    paths = disk_paths()
    baseline = {'git_bytes': dir_bytes([paths['git']]), 'cp24_local_bytes_at_init': dir_bytes(paths['cp24_local']),
                'measured_epoch': time.time(),
                'rule': 'added = growth(.git) + all .local/{worktrees,artifacts,tmp}/cp-24 and .local/mlruns/cp24 bytes, '
                        'including the full Lead/Critic worktree checkouts (counted from the ledger\'s creation, so the '
                        'Lead worktree created before it is inside the measured added disk)'}
    Budget(ledger_path()).initialise(baseline)
    print(json.dumps(baseline, indent=1))


def tree_rss(pid):
    import psutil
    try:
        parent = psutil.Process(pid)
        procs = [parent, *parent.children(recursive=True)]
    except psutil.NoSuchProcess:
        return 0, 0.0
    total, cpu = 0, 0.0
    for p in procs:
        try:
            total += p.memory_info().rss
            t = p.cpu_times()
            cpu += t.user + t.system
        except psutil.NoSuchProcess:
            pass
    return total, cpu


def reconcile(state):
    for job in state['jobs']:
        if job.get('running') and not pid_alive(job.get('monitor_pid', -1)):
            tail = RECONCILE_TAIL_SECONDS * job.get('workers', 1)
            state['counts']['machine_seconds'] = state['counts'].get('machine_seconds', 0) + tail
            job.update(running=False, exit_code=None, abort_reason='reconciled_dead_monitor',
                       reconciled_tail_seconds=tail, reconciled_epoch=time.time())
            state['events'].append({'event': 'reconciled_dead_job', 'epoch': time.time(), 'job': job['name'],
                                    'job_index': job['index'], 'tail_seconds': tail})


def monitor(args):
    budget = Budget(ledger_path())
    command = args.command[1:] if args.command and args.command[0] == '--' else args.command
    if not command:
        raise ValueError('missing command')
    locks = ART / 'locks'
    locks.mkdir(parents=True, exist_ok=True)
    lock = (locks / f'{args.name}.lock').open('a')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        raise SystemExit(f'duplicate {args.name} job refused: another instance holds the lock')
    markers = ART / 'markers'
    markers.mkdir(parents=True, exist_ok=True)
    with budget.transaction() as state:
        reconcile(state)
        caps = effective_caps(state)
        running = [j for j in state['jobs'] if j.get('running')]
        if any(j['name'] == args.name for j in running):
            raise SystemExit(f'duplicate {args.name} job refused by ledger')
        if sum(j['workers'] for j in running) + args.workers > CAPS['workers']:
            raise SystemExit('refused: concurrent CPU workers would exceed 4')
        if state['counts'].get('machine_seconds', 0) >= caps['machine_seconds']:
            raise SystemExit('machine-hour cap exhausted')
        if Budget.active_seconds(state) >= caps['active_seconds']:
            raise SystemExit('active-hour hard stop reached')
        index = len(state['jobs'])
        state['jobs'].append({'index': index, 'name': args.name, 'command': command, 'workers': args.workers,
                              'monitor_pid': os.getpid(), 'start_epoch': time.time(), 'running': True,
                              'live_rss_bytes': 0, 'log': str(args.log),
                              'blas_environment': {k: os.environ[k] for k in BLAS}})
        baseline = state['disk_baseline']
    for stale in (markers / f'{args.name}.DONE.json', markers / f'{args.name}.FAILED.json'):
        if stale.exists():
            stale.rename(stale.with_name(f'{stale.stem}.superseded-{index}.json'))
    caffeinate = subprocess.Popen(['/usr/bin/caffeinate', '-i', '-w', str(os.getpid())],
                                  stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    args.log.parent.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if k != 'MLFLOW_TRACKING_URI'}  # local tracking only
    env.update({'PYTHONPATH': str(ROOT / 'src'), 'PYTHONDONTWRITEBYTECODE': '1', 'CP24_LEDGER': str(ledger_path()),
                'CP24_JOB_INDEX': str(index), 'CP24_JOB_NAME': args.name, 'CP24_PROJECT_ROOT': str(PROJECT),
                'CP23_PROJECT_ROOT': str(PROJECT), 'CP22_PROJECT_ROOT': str(PROJECT), 'CP21_PROJECT_ROOT': str(PROJECT),
                'CP24_WORKERS': str(args.workers), 'MLFLOW_DISABLE_AGENT_HINT': '1',
                'MLFLOW_DISABLE_TELEMETRY': 'true', 'DO_NOT_TRACK': '1'})
    # Earlier checkpoints' ledgers are read-only (§23.14): any reused code that tried to charge one
    # would find an uninitialised ledger under CP-24's tmp and fail, never write CP-20..CP-23's.
    forbidden = LOCAL / 'tmp' / 'cp-24' / 'forbidden-ledgers'
    env.update({f'CP{n}_LEDGER': str(forbidden / f'cp{n}' / 'budget.json') for n in (16, 20, 21, 22, 23)})
    reason, supervisor_error, proc = None, None, None
    peak_rss = peak_agg = peak_disk = 0
    cpu_seconds = 0.0
    began = last = time.monotonic()
    last_disk = -DISK_EVERY
    stop = {'signal': None}

    def on_signal(signum, _frame):
        stop['count'] = stop.get('count', 0) + 1
        stop['signal'] = signum
        if stop['count'] > 1 and proc is not None and proc.poll() is None:
            os.killpg(proc.pid, signal.SIGTERM)
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig, on_signal)
    try:
        with args.log.open('a') as log:
            log.write(f'# CP-24 job {args.name} index {index} start {time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}\n')
            log.flush()
            proc = subprocess.Popen(command, cwd=ROOT, env=env, stdin=subprocess.DEVNULL, stdout=log,
                                    stderr=subprocess.STDOUT, start_new_session=True)
            with budget.transaction() as state:
                state['jobs'][index]['child_pid'] = proc.pid
            while True:
                time.sleep(TICK)
                now = time.monotonic()
                delta, last = now - last, now
                rss, cpu = tree_rss(proc.pid)
                cpu_seconds = max(cpu_seconds, cpu)
                peak_rss = max(peak_rss, rss)
                measure = now - last_disk >= DISK_EVERY
                if measure:
                    disk, parts = measure_disk(baseline)
                    peak_disk = max(peak_disk, disk)
                    last_disk = now
                with budget.transaction() as state:
                    caps = effective_caps(state)
                    counts = state['counts']
                    counts['machine_seconds'] = counts.get('machine_seconds', 0) + delta * args.workers
                    job = state['jobs'][index]
                    job['charged_seconds'] = job.get('charged_seconds', 0) + delta * args.workers
                    job['elapsed_seconds'] = now - began
                    job['live_rss_bytes'] = rss
                    job['cpu_seconds_observed'] = cpu_seconds
                    agg = sum(j.get('live_rss_bytes', 0) for j in state['jobs'] if j.get('running'))
                    peak_agg = max(peak_agg, agg)
                    state['peaks']['rss_bytes'] = max(state['peaks'].get('rss_bytes', 0), agg)
                    if measure:
                        state['peaks']['additional_disk_bytes'] = max(state['peaks'].get('additional_disk_bytes', 0), disk)
                        state['last_disk'] = {'epoch': time.time(), 'added_bytes': disk, **parts}
                    active = Budget.active_seconds(state)
                    if counts['machine_seconds'] >= caps['machine_seconds']:
                        reason = 'machine_seconds_cap'
                    elif active >= caps['active_seconds']:
                        reason = 'active_seconds_hard_stop'
                    elif agg >= caps['rss_bytes']:
                        reason = 'aggregate_rss_cap'
                    elif measure and disk >= caps['additional_disk_bytes']:
                        reason = 'additional_disk_cap'
                    elif stop['signal'] is not None:
                        reason = f'monitor_signal_{stop["signal"]}'
                if reason or proc.poll() is not None:
                    break
            if reason and proc.poll() is None:
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=60)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
    except BaseException as exc:
        supervisor_error = repr(exc)
        if proc is not None and proc.poll() is None:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.wait(timeout=30)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
        raise
    finally:
        tail = time.monotonic() - last
        exit_code = proc.returncode if proc is not None else None
        final_disk, parts = measure_disk(baseline)
        peak_disk = max(peak_disk, final_disk)
        with budget.transaction() as state:
            state['counts']['machine_seconds'] = state['counts'].get('machine_seconds', 0) + tail * args.workers
            state['peaks']['additional_disk_bytes'] = max(state['peaks'].get('additional_disk_bytes', 0), peak_disk)
            state['last_disk'] = {'epoch': time.time(), 'added_bytes': final_disk, **parts}
            job = state['jobs'][index]
            job.update(running=False, live_rss_bytes=0, exit_code=exit_code, abort_reason=reason,
                       supervisor_error=supervisor_error, end_epoch=time.time(), elapsed_seconds=time.monotonic() - began,
                       charged_seconds=job.get('charged_seconds', 0) + tail * args.workers,
                       peak_process_tree_rss_bytes=peak_rss, peak_aggregate_rss_bytes=peak_agg,
                       peak_added_disk_bytes=peak_disk, cpu_seconds_observed=cpu_seconds)
            summary = {k: state['counts'].get(k, 0) for k in CAPS if k not in ('rss_bytes', 'additional_disk_bytes', 'workers')}
            active = Budget.active_seconds(state)
        ok = exit_code == 0 and reason is None and supervisor_error is None
        marker = markers / f'{args.name}.{"DONE" if ok else "FAILED"}.json'
        atomic(marker, {'job': args.name, 'job_index': index, 'status': 'success' if ok else 'failed_or_partial',
                        'exit_code': exit_code, 'abort_reason': reason, 'supervisor_error': supervisor_error,
                        'elapsed_seconds': time.monotonic() - began, 'peak_rss_bytes': peak_rss,
                        'cumulative_counts': summary, 'active_seconds_upper_bound': active,
                        'timebox_exceeded': active > TIMEBOX_ACTIVE_SECONDS, 'log': str(args.log),
                        'written_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())})
        caffeinate.terminate()
        lock.close()
    print(json.dumps({'job': args.name, 'exit_code': exit_code, 'abort_reason': reason,
                      'elapsed_seconds': round(time.monotonic() - began, 1), 'peak_rss_bytes': peak_rss}), flush=True)
    return 0 if ok else (exit_code if exit_code else 3)


def effort(kind: str, reason: str) -> None:
    """Record an idle pause or a wait for a steering answer so it is excluded
    from active hours (§17.8). Refused while a job runs: a pause never hides compute."""
    budget = Budget(ledger_path())
    with budget.transaction() as state:
        reconcile(state)
        if any(j.get('running') for j in state['jobs']):
            raise SystemExit('refused: a CP-24 job is running')
        e = state['effort']
        now = time.time()
        if kind == 'pause':
            if e.get('paused_since'):
                raise SystemExit('already paused')
            e['paused_since'] = now
            e.setdefault('pause_reasons', []).append({'start_epoch': now, 'reason': reason})
        else:
            if not e.get('paused_since'):
                raise SystemExit('not paused')
            e['pauses'].append([e.pop('paused_since'), now])
            e.setdefault('pause_reasons', []).append({'end_epoch': now, 'reason': reason})
        state['events'].append({'event': f'effort_{kind}', 'epoch': now, 'reason': reason})
    print(json.dumps({'effort': kind, 'reason': reason, 'epoch': now}))


def idle(start_iso: str, end_iso: str, reason: str) -> None:
    """Record a past idle gap (for example, a session stopped by a usage limit) as a pause, so it is excluded
    from active hours. Refused if any job ran in the interval, if it overlaps a recorded pause or lies in the
    future: a recorded idle gap never hides compute."""
    from datetime import datetime
    start, end = datetime.fromisoformat(start_iso).timestamp(), datetime.fromisoformat(end_iso).timestamp()
    budget = Budget(ledger_path())
    with budget.transaction() as state:
        reconcile(state)
        now = time.time()
        if not start < end <= now or start < state['effort']['session_start_epoch']:
            raise SystemExit('refused: the idle interval must lie inside the session and end in the past')
        for job in state['jobs']:
            a = job['start_epoch']
            b = job.get('end_epoch') or (now if job.get('running') else a + job.get('elapsed_seconds', 0))
            if a < end and b > start:
                raise SystemExit(f'refused: job {job["name"]} (index {job["index"]}) ran inside the interval')
        for a, b in state['effort']['pauses']:
            if a < end and b > start:
                raise SystemExit('refused: the interval overlaps a recorded pause')
        if state['effort'].get('paused_since') and state['effort']['paused_since'] < end:
            raise SystemExit('refused: the interval overlaps the open pause')
        state['effort']['pauses'].append([start, end])
        state['effort'].setdefault('pause_reasons', []).append({'start_epoch': start, 'end_epoch': end, 'reason': reason,
                                                                'recorded_epoch': now, 'kind': 'idle_gap'})
        state['events'].append({'event': 'effort_idle_gap', 'epoch': now, 'start_epoch': start, 'end_epoch': end,
                                'reason': reason})
    print(json.dumps({'idle_gap': [start_iso, end_iso], 'hours': round((end - start) / 3600, 3), 'reason': reason}))


def run_job(name: str, rest: list[str]) -> int:
    """Research jobs. Each is invoked as a child of `monitor`; none runs outside accounting."""
    if 'CP24_JOB_INDEX' not in os.environ:
        raise SystemExit('research jobs run only under the monitor (resource accounting, §23.11)')
    from cp24 import jobs
    return jobs.dispatch(ROOT, name, rest)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('init-ledger')
    sub.add_parser('status')
    for kind in ('pause', 'resume'):
        e = sub.add_parser(kind)
        e.add_argument('--reason', required=True)
    i = sub.add_parser('idle')
    i.add_argument('--start', required=True, help='ISO time with offset, e.g. 2026-10-05T07:45:00+03:00')
    i.add_argument('--end', required=True)
    i.add_argument('--reason', required=True)
    r = sub.add_parser('raise')
    r.add_argument('--counter', required=True)
    r.add_argument('--to', type=float, required=True)
    r.add_argument('--steering', required=True)
    m = sub.add_parser('monitor')
    m.add_argument('--name', required=True)
    m.add_argument('--workers', type=int, default=1)
    m.add_argument('--log', type=Path, required=True)
    m.add_argument('--expected-minutes', type=float, default=None,
                   help='Compatibility option; does not restrict when a job may run')
    m.add_argument('command', nargs=argparse.REMAINDER)
    j = sub.add_parser('job')
    j.add_argument('name')
    j.add_argument('rest', nargs=argparse.REMAINDER)
    args = ap.parse_args()
    if args.cmd == 'init-ledger':
        init_ledger()
        return 0
    if args.cmd in ('pause', 'resume'):
        effort(args.cmd, args.reason)
        return 0
    if args.cmd == 'idle':
        idle(args.start, args.end, args.reason)
        return 0
    if args.cmd == 'raise':
        value = int(args.to) if args.counter == 'ddnn2_fits' else float(args.to)
        print(json.dumps(Budget(ledger_path()).record_raise(ROOT, args.counter, value, args.steering)))
        return 0
    if args.cmd == 'status':
        state = Budget(ledger_path()).read()
        print(json.dumps({'counts': state['counts'], 'peaks': state['peaks'], 'caps': effective_caps(state),
                          'raises': state.get('raises', []),
                          'active_hours_upper_bound': round(Budget.active_seconds(state) / 3600, 3),
                          'machine_hours': round(state['counts'].get('machine_seconds', 0) / 3600, 3),
                          'running': [j['name'] for j in state['jobs'] if j.get('running')]}, indent=1, sort_keys=True))
        return 0
    if args.cmd == 'monitor':
        if not 1 <= args.workers <= CAPS['workers']:
            raise SystemExit('monitor requires 1..4 --workers')
        return monitor(args)
    return run_job(args.name, args.rest)


if __name__ == '__main__':
    raise SystemExit(main())
