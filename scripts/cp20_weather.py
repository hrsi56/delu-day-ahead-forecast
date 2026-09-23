"""CP-20 driver. Every compute job runs under ``--monitor``; long jobs add ``--detach``.

The monitor owns the job's resource accounting: it charges machine time as
wall-clock x declared workers, samples process-tree RSS and the aggregate of all
running CP-20 jobs, measures added disk, refuses a duplicate instance, keeps the
machine awake with ``caffeinate -i -w <monitor pid>``, terminates the job at any hard
cap or stop line and writes a completion marker whose ``exit_code`` distinguishes
success from partial work. A job interrupted by a crash is reconciled on the next
start with a conservative tail charge; accounting is never reset.
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
PROJECT = Path(os.environ.get('CP20_PROJECT_ROOT', '/Users/djourno/Downloads/PJM'))
LOCAL = PROJECT / '.local'
ART = LOCAL / 'artifacts' / 'cp-20'
LEDGER = ART / 'ledger' / 'budget.json'
MAIN_PY = PROJECT / '.venv' / 'bin' / 'python'
WX_PY = ART / 'wx-venv' / 'bin' / 'python'
sys.path.insert(0, str(ROOT / 'src'))
BLAS = ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
        'NUMEXPR_NUM_THREADS')
for name in BLAS:
    os.environ[name] = '1'
from cp20.budget import Budget, CAPS, GIB, TIMEBOX_ACTIVE_SECONDS, atomic, dir_bytes, pid_alive  # noqa: E402

TICK = 1.0
DISK_EVERY = 30.0
RECONCILE_TAIL_SECONDS = 60.0


def disk_paths():
    return {'git': PROJECT / '.git', 'worktree': ROOT,
            'cp20_local': [LOCAL / 'artifacts' / 'cp-20', LOCAL / 'tmp' / 'cp-20', LOCAL / 'worktrees' / 'cp-20']}


def measure_disk(baseline):
    paths = disk_paths()
    git = dir_bytes([paths['git']])
    # The worktree's own .git is a pointer file; its checkout grows with new outputs.
    tree = dir_bytes([ROOT]) if ROOT != PROJECT else 0
    local = dir_bytes(paths['cp20_local'])
    added = max(0, git - baseline['git_bytes']) + max(0, tree - baseline['worktree_bytes']) + local
    return added, {'git_bytes': git, 'worktree_bytes': tree, 'cp20_local_bytes': local}


def init_ledger():
    paths = disk_paths()
    baseline = {'git_bytes': dir_bytes([paths['git']]), 'worktree_bytes': dir_bytes([ROOT]),
                'cp20_local_bytes_at_init': dir_bytes(paths['cp20_local']),
                'weather_admission_retained_bytes': dir_bytes([LOCAL / 'weather-admission']),
                'measured_epoch': time.time(),
                'rule': 'added = growth(.git) + growth(worktree) + all .local/{artifacts,tmp,worktrees}/cp-20 bytes'}
    Budget(LEDGER).initialise(baseline)
    print(json.dumps(baseline, indent=1))


def tree_rss(pid):
    import psutil
    try:
        parent = psutil.Process(pid)
        procs = [parent, *parent.children(recursive=True)]
    except psutil.NoSuchProcess:
        return 0
    total = 0
    for p in procs:
        try:
            total += p.memory_info().rss
        except psutil.NoSuchProcess:
            pass
    return total


def reconcile(state):
    """Close jobs whose monitor died without recording an exit, with a conservative charge."""
    for job in state['jobs']:
        if job.get('running') and not pid_alive(job.get('monitor_pid', -1)):
            tail = RECONCILE_TAIL_SECONDS * job.get('workers', 1)
            state['counts']['machine_seconds'] = state['counts'].get('machine_seconds', 0) + tail
            job.update(running=False, exit_code=None, abort_reason='reconciled_dead_monitor',
                       reconciled_tail_seconds=tail, reconciled_epoch=time.time())
            state['events'].append({'event': 'reconciled_dead_job', 'epoch': time.time(),
                                    'job': job['name'], 'job_index': job['index'], 'tail_seconds': tail})


def monitor(args):
    budget = Budget(LEDGER)
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
        running = [j for j in state['jobs'] if j.get('running')]
        if any(j['name'] == args.name for j in running):
            raise SystemExit(f'duplicate {args.name} job refused by ledger')
        if sum(j['workers'] for j in running) + args.workers > CAPS['workers']:
            raise SystemExit('refused: concurrent CPU workers would exceed 4')
        if state['counts'].get('machine_seconds', 0) >= CAPS['machine_seconds']:
            raise SystemExit('machine-hour cap exhausted')
        if Budget.active_seconds(state) >= CAPS['active_seconds']:
            raise SystemExit('active-hour hard stop reached')
        index = len(state['jobs'])
        state['jobs'].append({'index': index, 'name': args.name, 'command': command, 'workers': args.workers,
                              'monitor_pid': os.getpid(), 'start_epoch': time.time(), 'running': True,
                              'live_rss_bytes': 0, 'log': str(args.log),
                              'stop_machine_seconds': args.stop_machine_hours * 3600 if args.stop_machine_hours else None,
                              'blas_environment': {k: os.environ[k] for k in BLAS}})
        baseline = state['disk_baseline']
    for stale in (markers / f'{args.name}.DONE.json', markers / f'{args.name}.FAILED.json'):
        if stale.exists():
            stale.rename(stale.with_name(f'{stale.stem}.superseded-{index}.json'))
    caffeinate = subprocess.Popen(['/usr/bin/caffeinate', '-i', '-w', str(os.getpid())],
                                  stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    args.log.parent.mkdir(parents=True, exist_ok=True)
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src'), 'PYTHONDONTWRITEBYTECODE': '1',
           'CP20_LEDGER': str(LEDGER), 'CP20_JOB_INDEX': str(index), 'CP20_JOB_NAME': args.name,
           'CP20_PROJECT_ROOT': str(PROJECT), 'CP20_WORKERS': str(args.workers)}
    reason, supervisor_error, proc = None, None, None
    peak_rss = peak_agg = peak_disk = 0
    began = last = time.monotonic()
    last_disk = -DISK_EVERY
    stop = {'signal': None}

    def on_signal(signum, _frame):
        stop['signal'] = signum
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig, on_signal)
    try:
        with args.log.open('a') as log:
            log.write(f'# CP-20 job {args.name} index {index} start {time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}\n')
            log.flush()
            proc = subprocess.Popen(command, cwd=ROOT, env=env, stdin=subprocess.DEVNULL, stdout=log,
                                    stderr=subprocess.STDOUT, start_new_session=True)
            with budget.transaction() as state:
                state['jobs'][index]['child_pid'] = proc.pid
            while True:
                time.sleep(TICK)
                now = time.monotonic()
                delta, last = now - last, now
                rss = tree_rss(proc.pid)
                peak_rss = max(peak_rss, rss)
                measure = now - last_disk >= DISK_EVERY
                if measure:
                    disk, parts = measure_disk(baseline)
                    peak_disk = max(peak_disk, disk)
                    last_disk = now
                with budget.transaction() as state:
                    counts = state['counts']
                    counts['machine_seconds'] = counts.get('machine_seconds', 0) + delta * args.workers
                    job = state['jobs'][index]
                    job['charged_seconds'] = job.get('charged_seconds', 0) + delta * args.workers
                    job['elapsed_seconds'] = now - began
                    job['live_rss_bytes'] = rss
                    agg = sum(j.get('live_rss_bytes', 0) for j in state['jobs'] if j.get('running'))
                    peak_agg = max(peak_agg, agg)
                    state['peaks']['rss_bytes'] = max(state['peaks'].get('rss_bytes', 0), agg)
                    if measure:
                        state['peaks']['additional_disk_bytes'] = max(state['peaks'].get('additional_disk_bytes', 0), disk)
                        state['last_disk'] = {'epoch': time.time(), 'added_bytes': disk, **parts}
                    active = Budget.active_seconds(state)
                    state['active_seconds_upper_bound'] = active
                    if counts['machine_seconds'] >= CAPS['machine_seconds']:
                        reason = 'machine_seconds_cap'
                    elif job['stop_machine_seconds'] and counts['machine_seconds'] >= job['stop_machine_seconds']:
                        reason = 'machine_seconds_stop_line'
                    elif active >= CAPS['active_seconds']:
                        reason = 'active_seconds_hard_stop'
                    elif agg >= CAPS['rss_bytes']:
                        reason = 'aggregate_rss_cap'
                    elif measure and disk >= CAPS['additional_disk_bytes']:
                        reason = 'additional_disk_cap'
                    elif stop['signal'] is not None:
                        reason = f'monitor_signal_{stop["signal"]}'
                if reason or proc.poll() is not None:
                    break
            if reason and proc.poll() is None:
                os.killpg(proc.pid, signal.SIGTERM)
                try:
                    proc.wait(timeout=30)
                except subprocess.TimeoutExpired:
                    os.killpg(proc.pid, signal.SIGKILL)
                    proc.wait()
    except BaseException as exc:  # never leave an unguarded child running
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
                       supervisor_error=supervisor_error, end_epoch=time.time(),
                       elapsed_seconds=time.monotonic() - began,
                       charged_seconds=job.get('charged_seconds', 0) + tail * args.workers,
                       peak_process_tree_rss_bytes=peak_rss, peak_aggregate_rss_bytes=peak_agg,
                       peak_added_disk_bytes=peak_disk)
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


def detach(argv):
    """Relaunch this monitor in its own session so it survives the agent turn/session."""
    child = [a for a in argv if a != '--detach']
    out = ART / 'logs' / 'monitors.log'
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('a') as fh:
        proc = subprocess.Popen([str(MAIN_PY), str(Path(__file__).resolve()), *child], cwd=ROOT,
                                stdin=subprocess.DEVNULL, stdout=fh, stderr=subprocess.STDOUT, start_new_session=True)
    print(json.dumps({'detached_monitor_pid': proc.pid}), flush=True)
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--init-ledger', action='store_true')
    ap.add_argument('--monitor', action='store_true')
    ap.add_argument('--detach', action='store_true')
    ap.add_argument('--name')
    ap.add_argument('--workers', type=int, default=1)
    ap.add_argument('--log', type=Path)
    ap.add_argument('--stop-machine-hours', type=float)
    ap.add_argument('--status', action='store_true')
    ap.add_argument('command', nargs=argparse.REMAINDER)
    args = ap.parse_args()
    if args.init_ledger:
        init_ledger()
        return 0
    if args.status:
        state = Budget(LEDGER).read()
        print(json.dumps({'counts': state['counts'], 'peaks': state['peaks'],
                          'active_seconds_upper_bound': Budget.active_seconds(state),
                          'running': [j['name'] for j in state['jobs'] if j.get('running')]}, indent=1))
        return 0
    if args.monitor:
        if not args.name or not args.log or not 1 <= args.workers <= CAPS['workers']:
            raise SystemExit('monitor requires --name, --log and 1..4 --workers')
        if args.detach:
            return detach(sys.argv[1:])
        return monitor(args)
    raise SystemExit('nothing to do; research jobs are commands run under --monitor')


if __name__ == '__main__':
    raise SystemExit(main())
