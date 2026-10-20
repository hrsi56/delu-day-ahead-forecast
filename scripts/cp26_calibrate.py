"""Short real-ledger contention/observer calibration; no model or market-data reads."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
for name in ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS',
             'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'
from cp26.budget import Budget, atomic
from cp26.gates import RUN_ID, RUN_EVIDENCE
from cp26.harness import art, continuation_authority
from cp26.supervisor import register_worker, SUPERVISION_POLICY

LOCAL = art() / 'cold-rerun-2026-10-15/calibration-r15'


def worker(path, output):
    register_worker()
    budget = Budget(path)
    rows = []
    for i in range(8):
        start = time.perf_counter()
        budget.resource_read()
        refresh = time.perf_counter() - start
        budget.resource_update(lambda state: state['counts'].update(
            calibration=state['counts'].get('calibration', 0) + 1))
        sample = budget.last_transaction.copy()
        budget.event('r15_calibration_only', worker=os.getpid(), sequence=i)
        rows.append({'refresh_seconds': refresh, 'resource_transaction': sample,
                     'append_transaction': budget.last_transaction.copy(),
                     'total_seconds': time.perf_counter() - start})
    atomic(output, {'pid': os.getpid(), 'rows': rows})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--worker', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if args.worker:
        worker(args.worker, args.output)
        return
    if os.environ.get('CP26_RUN_ID') != RUN_ID or int(os.environ.get('CP26_WORKERS', '0')) != 4:
        raise RuntimeError('registered four-slot calibration monitor required')
    continuation_authority(ROOT)
    LOCAL.mkdir(parents=True, exist_ok=True)
    original = Budget().path
    phases = []
    for children in (2, 3):
        copy = LOCAL / f'ledger-{children+1}.json'
        shutil.copyfile(original, copy)
        # This copy is a resource fixture, never a second production account.
        start = time.perf_counter()
        processes, outputs = [], []
        for i in range(children):
            out = LOCAL / f'phase-{children+1}-worker-{i}.json'
            process = subprocess.Popen([sys.executable, '-B', __file__, '--worker', str(copy),
                                        '--output', str(out)], cwd=ROOT)
            processes.append(process)
            outputs.append(out)
        for process in processes:
            if process.wait(timeout=60) != 0:
                raise RuntimeError('bounded calibration worker failed; no automatic retry')
        rows = [json.loads(path.read_text()) for path in outputs]
        phases.append({'actual_process_allocation': children+1, 'outer_reserved_slots': 4,
            'seconds': time.perf_counter()-start, 'completed_operations': children*16,
            'workers': rows, 'resource_fixture_bytes': copy.stat().st_size})
    samples = [row for phase in phases for worker_row in phase['workers'] for row in worker_row['rows']]
    production = Budget().resource_read()['jobs'][int(os.environ['CP26_JOB_INDEX'])]
    result = {'schema': 'cp26-r15-calibration-v1', 'run_id': RUN_ID, 'phases': phases,
        'source_ledger_bytes': original.stat().st_size,
        'maximum_refresh_seconds': max(r['refresh_seconds'] for r in samples),
        'maximum_resource_transaction_seconds': max(r['resource_transaction']['total_seconds'] for r in samples),
        'maximum_append_transaction_seconds': max(r['append_transaction']['total_seconds'] for r in samples),
        'observer_telemetry': {role: production.get(role+'_ledger_lock_telemetry')
                               for role in ('supervisor', 'watchdog')},
        'policy_tested': SUPERVISION_POLICY, 'prior_measured_tail_seconds': .6453919999767095,
        'models_fit': 0, 'market_data_read': False, 'resource_copy_only': True,
        'job_id': os.environ['CP26_JOB_ID'], 'job_index': int(os.environ['CP26_JOB_INDEX'])}
    atomic(ROOT / RUN_EVIDENCE / 'calibration-v21-r15.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'phases'}), flush=True)


if __name__ == '__main__':
    main()
