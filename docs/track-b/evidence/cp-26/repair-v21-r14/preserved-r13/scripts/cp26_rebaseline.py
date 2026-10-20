"""Local CP-26 driver. Compute commands run under the cumulative resource monitor."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
# Set these before importing any modelling module, including NumPy.
for name in ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS',
             'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
os.environ['MLFLOW_DISABLE_TELEMETRY'] = 'true'
os.environ['DO_NOT_TRACK'] = '1'

from cp26.budget import Budget, CAPS, atomic, machine_hours  # noqa: E402
from cp26.harness import art, identities, landed_code, HARNESS_LOG  # noqa: E402
from cp25.guard import redact  # noqa: E402


def tree_rss(pid: int) -> int:
    import psutil
    try:
        parent = psutil.Process(pid)
        processes = [parent, *parent.children(recursive=True)]
    except psutil.NoSuchProcess:
        return 0
    total = 0
    for proc in processes:
        try:
            total += proc.memory_info().rss
        except psutil.NoSuchProcess:
            pass
    return total


def local_path(path: Path) -> Path:
    path = path.resolve()
    if not path.is_relative_to(art().resolve()):
        raise ValueError('job logs must stay inside primary .local/artifacts/cp-26')
    return path


def reconciled_tail(job: dict) -> float:
    """Only an evidenced monotonic completion duration can reconcile a dead monitor.

    Time since its last tick may include hours with no worker alive. Never charge that idle
    gap as measured computation. Without a completion clock, leave the measured ledger
    intact and refuse new compute until the uncertain job has been reconciled explicitly.
    """
    clock = local_path(Path(job.get('completion_clock', art() / 'jobs' / 'missing-clock.json')))
    if not clock.exists():
        raise RuntimeError('dead CP-26 monitor has no completion clock: worker runtime is uncertain; '
                           'new compute is stopped, and restart idle time is not charged')
    receipt = json.loads(clock.read_text())
    if receipt.get('job_index') != job.get('job_index') or receipt.get('started_epoch') != job['started_epoch']:
        raise RuntimeError('completion clock does not identify the interrupted CP-26 job')
    wall = receipt.get('wall_seconds')
    charged = job.get('charged_wall_seconds')
    if not isinstance(wall, (float, int)) or not isinstance(charged, (float, int)) or not 0 <= charged <= wall:
        raise RuntimeError('completion clock does not bound the already measured worker duration')
    return (wall - charged) * job['workers']


def monitor(args) -> int:
    """Charge all declared worker wall time, including failed jobs, before any later job starts."""
    import psutil
    command = args.command
    if command and command[0] == '--':
        command = command[1:]
    if not command or not 1 <= args.workers <= CAPS['workers']:
        raise ValueError('supply a command and 1..4 declared compute workers')
    budget = Budget()
    log_path = local_path(args.log or (art() / 'logs' / f'{args.name}.log'))
    log_path.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    with budget.transaction() as state:
        # A dead monitor cannot silently discard time or leave live unaccounted workers.
        for job in state['jobs']:
            if not job['running']:
                continue
            if psutil.pid_exists(job['monitor_pid']):
                expected = job.get('monitor_create_time')
                if expected is None or psutil.Process(job['monitor_pid']).create_time() == expected:
                    continue
            child = job.get('child_pid')
            if child and psutil.pid_exists(child):
                raise RuntimeError('orphaned CP-26 worker remains alive; reconcile its monitor before continuing')
            tail = reconciled_tail(job)
            state['counts']['machine_seconds'] = state['counts'].get('machine_seconds', 0) + tail
            job.update(running=False, live_rss_bytes=0, abort_reason='dead_monitor',
                       exit_code=None, reconciled_epoch=now)
        running = [j for j in state['jobs'] if j['running']]
        workers = args.workers + sum(j['workers'] for j in running)
        if workers > CAPS['workers'] or any(j['name'] == args.name for j in running):
            raise RuntimeError('concurrent worker ceiling or duplicate job refuses start')
        if state['counts'].get('machine_seconds', 0) >= CAPS['machine_seconds']:
            raise RuntimeError('CP-26 machine-hour ceiling exhausted')
        index = len(state['jobs'])
        clock = art() / 'jobs' / f'{args.name}.{index}.clock.json'
        state['jobs'].append({'name': args.name, 'workers': args.workers, 'running': True,
                              'monitor_pid': os.getpid(), 'child_pid': None, 'started_epoch': now,
                              'monitor_create_time': psutil.Process().create_time(),
                              'job_index': index, 'completion_clock': str(clock), 'charged_wall_seconds': 0.0,
                              'last_charge_epoch': now, 'live_rss_bytes': 0, 'log': str(log_path)})
        state['peaks']['workers'] = max(workers, state['peaks'].get('workers', 0))
    env = os.environ.copy()
    env['CP26_WORKERS'] = str(args.workers)
    env['CP26_MONITORED_JOB'] = args.name
    env['PYTHONPATH'] = str(ROOT / 'src')
    child = None
    reason = None
    interrupted = []
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        signal.signal(sig, lambda signum, frame: interrupted.append(signum))
    began = last = time.monotonic()
    peak = 0
    caffeinate = subprocess.Popen(['/usr/bin/caffeinate', '-i', '-w', str(os.getpid())],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        with log_path.open('a') as log:
            log.write(f'# CP-26 monitored job {args.name}; workers={args.workers}\n')
            log.flush()
            child = subprocess.Popen(command, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                                     stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            with budget.transaction() as state:
                state['jobs'][index]['child_pid'] = child.pid
            while child.poll() is None:
                time.sleep(0.5)
                tick = time.monotonic()
                rss = tree_rss(child.pid) + psutil.Process().memory_info().rss
                peak = max(peak, rss)
                with budget.transaction() as state:
                    counts = state['counts']
                    counts['machine_seconds'] = counts.get('machine_seconds', 0) + (tick - last) * args.workers
                    state['jobs'][index]['charged_wall_seconds'] += tick - last
                    state['jobs'][index].update(last_charge_epoch=time.time(), live_rss_bytes=rss)
                    aggregate = sum(j['live_rss_bytes'] for j in state['jobs'] if j['running'])
                    state['peaks']['rss_bytes'] = max(aggregate, state['peaks'].get('rss_bytes', 0))
                    if counts['machine_seconds'] >= CAPS['machine_seconds']:
                        reason = 'machine_hours_cap'
                    elif aggregate >= CAPS['rss_bytes']:
                        reason = 'aggregate_memory_cap'
                last = tick
                if interrupted:
                    reason = f'signal_{interrupted[0]}'
                if reason:
                    if child.poll() is None:
                        os.killpg(child.pid, signal.SIGTERM)
                        try:
                            child.wait(timeout=5)
                        except subprocess.TimeoutExpired:
                            os.killpg(child.pid, signal.SIGKILL)
                    break
            code = child.wait()
    except BaseException as exc:
        reason = redact(f'{type(exc).__name__}: {exc}')
        if child is not None and child.poll() is None:
            os.killpg(child.pid, signal.SIGTERM)
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(child.pid, signal.SIGKILL)
                child.wait()
        code = 70
    finally:
        ended = time.monotonic()
        atomic(clock, {'job_index': index, 'started_epoch': now, 'wall_seconds': ended-began,
                       'exit_code': locals().get('code', 70), 'abort_reason': reason})
        with budget.transaction() as state:
            state['counts']['machine_seconds'] = state['counts'].get('machine_seconds', 0) + (ended - last) * args.workers
            state['jobs'][index].update(running=False, live_rss_bytes=0, exit_code=locals().get('code', 70),
                                       abort_reason=reason, ended_epoch=time.time(),
                                       wall_seconds=ended-began, charged_wall_seconds=ended-began, peak_rss_bytes=peak)
            total = machine_hours(state)
        caffeinate.terminate()
        caffeinate.wait()
    result = {'job': args.name, 'exit_code': code, 'abort_reason': reason, 'wall_seconds': ended-began,
              'machine_hours_cumulative': total, 'peak_rss_bytes': peak, 'log': str(log_path)}
    atomic(art() / 'jobs' / f'{args.name}.json', result)
    print(json.dumps(result))
    return code if not reason else 70


def dispatch(name: str) -> int:
    if not os.environ.get('CP26_MONITORED_JOB'):
        raise RuntimeError('compute jobs require the CP-26 resource monitor')
    if name == 'verify-inputs':
        inputs = identities(ROOT)
        modules = landed_code(ROOT)
        atomic(ROOT / 'reports/rebaseline/harness-log.json',
               {'schema': 'cp26-harness-log-v1', 'pins': inputs, 'landed_code': modules,
                'replacements': HARNESS_LOG})
        print(json.dumps({'pins_verified': len(inputs), 'landed_modules_verified': len(modules)}))
        return 0
    if name == 'parity':
        from cp26.parity import run
        result = run(ROOT)
        print(json.dumps({'status': result['status'], 'checks': len(result['checks'])}))
        return 0
    raise ValueError(f'job not yet implemented: {name}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('init-ledger')
    sub.add_parser('status')
    mon = sub.add_parser('monitor')
    mon.add_argument('--name', required=True)
    mon.add_argument('--workers', type=int, default=1)
    mon.add_argument('--log', type=Path)
    mon.add_argument('command', nargs=argparse.REMAINDER)
    job = sub.add_parser('job')
    job.add_argument('name', choices=('verify-inputs', 'parity'))
    args = parser.parse_args()
    if args.action == 'init-ledger':
        Budget().initialise()
        print('CP-26 cumulative ledger initialized (485 machine-hours; 4 workers; 12 GB).')
        return 0
    if args.action == 'status':
        state = Budget().read()
        print(json.dumps({'machine_hours': machine_hours(state), 'peaks': state['peaks'],
                          'running': [j['name'] for j in state['jobs'] if j['running']]}))
        return 0
    if args.action == 'monitor':
        return monitor(args)
    return dispatch(args.name)


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(redact(f'{type(exc).__name__}: {exc}'), file=sys.stderr)
        raise SystemExit(70)
