"""Local CP-26 driver. Compute commands use an independent cumulative supervisor."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
for name in ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS',
             'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
os.environ['MLFLOW_DISABLE_TELEMETRY'] = 'true'
os.environ['DO_NOT_TRACK'] = '1'

from cp26.budget import Budget, CAPS, atomic, require_compute_ready, resource_summary  # noqa: E402
from cp26.harness import art, identities, landed_code, HARNESS_LOG  # noqa: E402
from cp26.supervisor import (apply_completion, completion_receipt, identity_status,  # noqa: E402
                             process_identity, reconcile_running, require_fresh_supervision,
                             startup_is_fresh, SUPERVISION_POLICY, LEDGER_TIMEOUT_SECONDS,
                             signal_identity, freshness_reason, monitor_failsafe,
                             STARTUP_GRACE_SECONDS, HEARTBEAT_TIMEOUT_SECONDS)
from cp25.guard import redact  # noqa: E402
from cp26.gates import PROJECTION_NAME
from cp26.limits import shutdown_exposure_seconds  # noqa: E402

JOB_NAMES = ('verify-inputs', 'parity', 'prepare', 'benchmark', 'pilot', 'project',
             'searches', 'forecasts', 'scores', 'inference', 'diagnostics', 'report', 'full-run')


def local_path(path: Path) -> Path:
    path = path.resolve()
    if not path.is_relative_to(art().resolve()):
        raise ValueError('job logs and receipts must stay inside primary .local/artifacts/cp-26')
    return path


def reconciled_tail(job: dict) -> float:
    """Keep the original bound-clock helper; v2 jobs require full supervisor evidence."""
    clock = local_path(Path(job.get('completion_clock', art() / 'jobs' / 'missing-clock.json')))
    if not clock.exists():
        raise RuntimeError('dead CP-26 monitor has no completion clock: worker runtime is uncertain; '
                           'new compute is stopped, and restart idle time is not charged')
    receipt = json.loads(clock.read_text())
    if job.get('job_id'):
        from cp26.supervisor import check_completion
        return check_completion(job, receipt)
    if receipt.get('job_index') != job.get('job_index') or receipt.get('started_epoch') != job['started_epoch']:
        raise RuntimeError('completion clock does not identify the interrupted CP-26 job')
    wall, charged = receipt.get('wall_seconds'), job.get('charged_wall_seconds')
    if (isinstance(wall, bool) or isinstance(charged, bool)
            or not isinstance(wall, (float, int)) or not isinstance(charged, (float, int))
            or not math.isfinite(wall) or not math.isfinite(charged) or not 0 <= charged <= wall):
        raise RuntimeError('completion clock does not bound the already measured worker duration')
    return (wall - charged) * job['workers']


def monitor(args) -> int:
    """Reserve workers atomically; a separate process accounts through outer-monitor death."""
    command = args.command[1:] if args.command and args.command[0] == '--' else args.command
    if not command or not 1 <= args.workers <= CAPS['workers']:
        raise ValueError('supply a command and 1..4 declared compute workers')
    budget = Budget()
    log_path = local_path(args.log or art() / 'logs' / f'{args.name}.log')
    log_path.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    monitor_identity = process_identity()
    job_id = uuid.uuid4().hex
    run_id = os.environ.get('CP26_RUN_ID')
    def reserve(state):
        reconcile_running(state)
        require_compute_ready(state)
        if run_id and run_id not in state.get('scientific_runs', {}):
            raise ValueError('CP26_RUN_ID must name a registered scientific run')
        running = [j for j in state['jobs'] if j['running']]
        workers = args.workers + sum(j['workers'] for j in running)
        if workers > CAPS['workers'] or any(j['name'] == args.name for j in running):
            raise RuntimeError('concurrent worker ceiling or duplicate job refuses start')
        if (resource_summary(state)['total_seconds'] + shutdown_exposure_seconds(workers)
                >= CAPS['machine_seconds']):
            raise RuntimeError('CP-26 shutdown headroom refuses admission before500hours')
        index = len(state['jobs'])
        prefix = art() / 'jobs' / f'{args.name}.{index}.{job_id}'
        request_path = prefix.with_name(prefix.name + '.request.json')
        clock = prefix.with_name(prefix.name + '.clock.json')
        progress = prefix.with_name(prefix.name + '.progress.json')
        request = {'schema': 'cp26-request-v2', 'job_id': job_id, 'job_index': index,
                   'run_id': run_id,
                   'name': args.name, 'workers': args.workers, 'started_epoch': now,
                   'monitor_identity': monitor_identity, 'ledger': str(budget.path.resolve()),
                   'command': command, 'cwd': str(ROOT), 'log': str(log_path),
                   'completion_clock': str(clock), 'progress_clock': str(progress),
                   'supervision_policy': SUPERVISION_POLICY}
        atomic(request_path, request)
        request_sha = hashlib.sha256(request_path.read_bytes()).hexdigest()
        state['jobs'].append({'name': args.name, 'workers': args.workers, 'running': True,
                              'run_id': run_id,
                              'job_id': job_id, 'job_index': index, 'phase': 'reserved',
                              'monitor_identity': monitor_identity, 'monitor_pid': os.getpid(),
                              'monitor_create_time': monitor_identity['create_time'],
                              'supervisor_identity': None, 'child_identity': None, 'child_pid': None,
                              'started_epoch': now, 'completion_clock': str(clock),
                              'reserved_monotonic': time.monotonic(),
                              'supervision_policy': SUPERVISION_POLICY,
                              'progress_clock': str(progress), 'request': str(request_path),
                              'request_sha256': request_sha, 'charged_wall_seconds': 0.0,
                              'last_charge_epoch': now, 'live_rss_bytes': 0, 'log': str(log_path)})
        state['peaks']['workers'] = max(workers, state['peaks'].get('workers', 0))
        return index, request_path
    budget.resource_read()
    index, request_path = budget.resource_update(reserve, timeout_seconds=LEDGER_TIMEOUT_SECONDS)
    env = os.environ.copy()
    env['CP26_WORKERS'] = str(args.workers)
    env['CP26_MONITORED_JOB'] = args.name
    env['CP26_JOB_ID'] = job_id
    env['CP26_JOB_INDEX'] = str(index)
    env['CP26_LEDGER'] = str(budget.path.resolve())
    env['PYTHONPATH'] = str(ROOT / 'src')
    interrupted = []
    previous_signals = {}
    for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
        previous_signals[sig] = signal.signal(sig, lambda signum, frame: interrupted.append(signum))
    supervisor = None
    supervisor_identity = None
    try:
        with log_path.open('a') as log:
            supervisor = subprocess.Popen([sys.executable, '-B', '-m', 'cp26.supervisor', str(request_path)],
                                          cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                                          stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            supervisor_identity = process_identity(supervisor.pid)
            def bind_supervisor(state):
                job = state['jobs'][index]
                if job['job_id'] != job_id:
                    raise RuntimeError('CP-26 job identity changed during launch')
                if not job['running']:
                    if supervisor_identity is not None and job.get('supervisor_identity') != supervisor_identity:
                        raise RuntimeError('CP-26 terminal supervisor identity changed during launch')
                    apply_completion(state, job, completion_receipt(job))
                    return
                if supervisor_identity is not None:
                    if job['supervisor_identity'] not in (None, supervisor_identity):
                        raise RuntimeError('CP-26 supervisor identity changed during launch')
                    job.update(supervisor_identity=supervisor_identity, supervisor_pid=supervisor.pid)
            budget.resource_read()
            budget.resource_update(bind_supervisor, timeout_seconds=LEDGER_TIMEOUT_SECONDS)
            while supervisor.poll() is None:
                job = budget.resource_read()['jobs'][index]
                if job.get('job_id') != job_id:
                    raise RuntimeError('CP-26 job identity changed during supervision')
                if job['running'] and not startup_is_fresh(job):
                    try:
                        require_fresh_supervision(job)
                    except RuntimeError:
                        healthy = [identity_status(job.get(f'{role}_identity')) == 'same'
                                   and freshness_reason(job, role) is None
                                   for role in ('supervisor', 'watchdog')]
                        if not any(healthy):
                            monitor_failsafe(request_path)
                if interrupted and identity_status(supervisor_identity) == 'same':
                    signal_identity(supervisor_identity, interrupted.pop(0))
                time.sleep(0.2)
            supervisor.wait()
            # Hard supervisor death can precede its watchdog's bound receipt. Wait
            # only while independently evidenced enforcement is completing it.
            deadline = time.monotonic() + STARTUP_GRACE_SECONDS + HEARTBEAT_TIMEOUT_SECONDS
            while True:
                job = budget.resource_read()['jobs'][index]
                if not job['running']:
                    break
                watchdog_fresh = (identity_status(job.get('watchdog_identity')) == 'same'
                                  and freshness_reason(job, 'watchdog') is None)
                if not watchdog_fresh:
                    monitor_failsafe(request_path)
                    break
                if time.monotonic() >= deadline:
                    raise RuntimeError('CP-26 independent ending receipt did not arrive; runtime is uncertain')
                time.sleep(0.05)
        # A terminal receipt survives death between clock write and ledger commit.
        def finish(state):
            job = state['jobs'][index]
            receipt = completion_receipt(job)
            apply_completion(state, job, receipt)
            return {'job': args.name, 'job_id': job_id, 'exit_code': job['exit_code'],
                      'abort_reason': job['abort_reason'], 'wall_seconds': job['wall_seconds'],
                      'peak_rss_bytes': job['peak_rss_bytes'], 'log': str(log_path),
                      'resources': resource_summary(state),
                      'machine_hours_cumulative': resource_summary(state)['machine_hours']}
        budget.resource_read()
        result = budget.resource_update(finish, timeout_seconds=LEDGER_TIMEOUT_SECONDS)
        atomic(art() / 'jobs' / f'{args.name}.json', result)
        print(json.dumps(result))
        return result['exit_code'] if not result['abort_reason'] else 70
    except BaseException:
        # A failed launcher/receipt leaves its registered job intact. Do not turn
        # uncertain worker duration into idle time or make a clean false ending.
        if supervisor is not None:
            if identity_status(supervisor_identity) == 'same' and supervisor.poll() is None:
                signal_identity(supervisor_identity, signal.SIGTERM)
                try:
                    supervisor.wait(timeout=12)
                except subprocess.TimeoutExpired:
                    pass
        raise
    finally:
        for sig, previous in previous_signals.items():
            signal.signal(sig, previous)


def dispatch(name: str) -> int:
    if not os.environ.get('CP26_MONITORED_JOB'):
        raise RuntimeError('compute jobs require the CP-26 resource monitor')
    from cp26.gates import OUTPUT
    if name == 'verify-inputs':
        inputs = identities(ROOT)
        modules = landed_code(ROOT)
        atomic(ROOT / OUTPUT / 'harness-log.json',
               {'schema': 'cp26-harness-log-v1', 'pins': inputs, 'landed_code': modules,
                'replacements': HARNESS_LOG})
        print(json.dumps({'pins_verified': len(inputs), 'landed_modules_verified': len(modules)}))
        return 0
    if name == 'parity':
        from cp26.parity import run
        result = run(ROOT, output=OUTPUT / 'parity.json')
        print(json.dumps({'status': result['status'], 'checks': len(result['checks'])}))
        return 0
    from cp26.gates import (ExecutionGate, OUTPUT, PROTOCOL, authorize_consuming_process,
                            code_identity, protocol_identity)
    from cp26 import execution as E
    authorize_consuming_process(ROOT)
    gate = ExecutionGate(ROOT)
    shared = protocol_identity(ROOT)
    if name == 'prepare':
        result = E.prepare(ROOT, shared, gate=gate)
        from cp26.scoring import load_population
        population = load_population(ROOT)
        population.verify_key_mapping(population.keys_by_day())
        print(json.dumps({'status': 'SUPPORT_AND_POPULATION_VERIFIED',
                          'searches': len(result['searches']), 'scoring_keys': len(population.keys)}))
        return 0
    if name == 'benchmark':
        from cp26.analysis import benchmark
        result = benchmark(ROOT)
        print(json.dumps(result))
        return 0
    if name == 'pilot':
        result = E.timing_pilot(ROOT, shared, gate=gate)
        print(json.dumps({'status': 'SEALED_PILOT_COMPLETE', 'summaries': len(result['summary']),
                          'probes': len(result['probes']), 'evaluation_scores_computed': False}))
        return 0
    if name == 'project':
        gate('pilot')
        from cp26.costing import price_pilot, persist_projection, require_projection
        paths = E.Paths.build(ROOT)
        manifest = E.manifest_for(paths, shared)
        pilot = E._read(paths.output / 'timing-pilot.json')
        projection_path = paths.output / PROJECTION_NAME
        if projection_path.exists():
            from cp26.costing import _verify, SCHEMA
            result = json.loads(projection_path.read_text())
            _verify(result, SCHEMA)
            if (result.get('protocol') != shared or result.get('code_sha256') != code_identity(ROOT)
                    or result.get('pilot_sha256') != E.digest(pilot)
                    or result.get('execution_manifest_sha256') != manifest['content_sha256']):
                raise RuntimeError('frozen projection cannot be reused with changed pilot/protocol/code/manifest')
            gate('search')
            from cp26.gates import outstanding_projection
            from cp26.budget import projected_cost, CapExceeded
            state = Budget().read()
            searches, remaining = outstanding_projection(result, paths.output, state)
            current = projected_cost(state, searches, remaining, run_id=shared.get('run_id'))
            if not current['within_pilot_stop']:
                raise CapExceeded(f"CP-26 projection {current['projected_total_hours']:.6f} hours exceeds "
                                  'the 440-hour cumulative admission line; Owner resource/protocol decision required')
            print(json.dumps({'status': 'COST_PROJECTION_REUSED', 'hours': current['projected_total_hours'],
                              'stop_hours': 440.0, 'searches_priced': 42,
                              'within_pilot_stop': current['within_pilot_stop'],
                              'original_projection_sha256': result['content_sha256']}), flush=True)
            return 0
        benchmark_result = E._read(paths.output / 'fixture-benchmark.json')
        if benchmark_result.get('code_sha256') != code_identity(ROOT):
            raise RuntimeError('fixture timing benchmark is stale for current code')
        plans = [E._read(paths.plan(route, k)) for route in E.ROUTES for k in range(14)]
        additional = copy.deepcopy(benchmark_result['additional_costs'])
        preliminary = price_pilot(Budget().read(), pilot, plans=plans, execution_manifest=manifest,
                                  protocol_bytes=(ROOT / PROTOCOL).read_bytes(), protocol=shared,
                                  code_sha256=code_identity(ROOT), additional_costs=additional)
        failed = additional['failed_jobs_and_resume']
        if failed.pop('extend_with_pilot_fit_and_search_prices', False):
            fit_and_search_seconds = preliminary['remaining_search_seconds'] + preliminary['remaining']['daily_fits']['machine_seconds']
            failed['machine_seconds'] += 0.10 * fit_and_search_seconds
            failed['basis'] += (f'; plus 10% of prospectively priced daily fits and all 42 searches '
                                f'({fit_and_search_seconds:.17g} seconds), separate from every cumulative prior charge/reserve')
        result = price_pilot(Budget().read(), pilot, plans=plans, execution_manifest=manifest,
                            protocol_bytes=(ROOT / PROTOCOL).read_bytes(), protocol=shared,
                            code_sha256=code_identity(ROOT), additional_costs=additional)
        persist_projection(ROOT, result, output=OUTPUT / PROJECTION_NAME)
        print(json.dumps({'status': 'COST_PROJECTION', 'hours': result['projected_total_hours'],
                          'stop_hours': 440.0, 'searches_priced': 42,
                          'within_pilot_stop': result['within_pilot_stop']}), flush=True)
        require_projection(result, Budget().read())
        return 0
    if name == 'searches':
        result = E.run_searches(ROOT, shared, gate=gate)
        print(json.dumps({'status': 'SEARCHES_COMPLETE', 'searches': sum(len(v) for v in result.values())}))
        return 0
    if name in ('forecasts', 'full-run'):
        if name == 'full-run':
            E.run_searches(ROOT, shared, gate=gate)
        from cp26.scoring import load_population
        population = load_population(ROOT)
        result = E.run_forecasts(ROOT, shared, population.keys_by_day(), gate=gate)
        print(json.dumps(result), flush=True)
        if name == 'forecasts':
            return 0
        for next_stage in ('scores', 'inference', 'diagnostics', 'report'):
            dispatch(next_stage)
        return 0
    if name in ('scores', 'inference', 'diagnostics'):
        from cp26 import analysis as A
        function = {'scores': A.run_scores, 'inference': A.run_inference,
                    'diagnostics': A.run_diagnostics}[name]
        result = function(ROOT, shared, gate=gate)
        print(json.dumps({'status': f'{name.upper()}_COMPLETE', 'manifest': result.get('manifest')}))
        return 0
    if name == 'report':
        gate('report')
        from cp26 import analysis as A
        from cp26.reporting import build_report
        scores = A.load_scores(ROOT, shared)
        output = ROOT / OUTPUT
        inference = E._read(output / 'inference-manifest.json')
        diagnostics = E._read(output / 'diagnostics-manifest.json')
        state = Budget().read()
        resources = {**resource_summary(state), 'repair_terminal_snapshot': state['repair_scope']['terminal_snapshot']}
        result = build_report(ROOT, output, scores, inference, diagnostics, resources, shared)
        print(json.dumps({'status': 'LOCAL_REPORT_DRAFT_COMPLETE', 'paths': result['paths']}))
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
    job.add_argument('name', choices=JOB_NAMES)
    args = parser.parse_args()
    if args.action == 'init-ledger':
        Budget().initialise()
        print('CP-26 cumulative ledger initialized (500 machine-hours; 4 workers; 12 GB).')
        return 0
    if args.action == 'status':
        state = Budget().read()
        print(json.dumps({**resource_summary(state), 'peaks': state['peaks'],
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
