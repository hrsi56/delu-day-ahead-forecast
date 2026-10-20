"""Small cold-run preparation and sealed-pilot entry points; no restore queue."""
from pathlib import Path
import argparse
import contextlib
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
for name in ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS',
             'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[name] = '1'

from cp26.budget import Budget, atomic, resource_summary
from cp26.gates import OUTPUT, LOCAL_NAME, RUN_ID, RUN_EVIDENCE, code_identity, protocol_identity
from cp26 import execution as E, harness as H


def setup():
    if os.environ.get('CP26_RUN_ID') != RUN_ID or not os.environ.get('CP26_MONITORED_JOB'):
        raise RuntimeError('registered cold-run monitor required')
    paths = E.Paths.build(ROOT)
    forbidden = [paths.output / name for name in ('forecast-ledger', 'search-results', 'replay-state.json',
                                                  'learning-ledger.json', 'timing-pilot')]
    forbidden += [paths.local / name for name in ('fits', 'searches', 'state')]
    if any(p.exists() for p in forbidden):
        raise RuntimeError('cold scientific namespace is not empty at initial setup')
    old = ROOT / 'reports/rebaseline/continuation-v21-r14-accounting-3'
    preserve = [old / n for n in ('replay-state.json', 'learning-ledger.json', 'execution-manifest.json',
                                 'timing-pilot.json', 'cost-projection.json')]
    preserve += sorted((old / 'search-results').glob('*/*.json'))
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    from cp26.parity import require_pass
    parity = require_pass(ROOT, output=old.relative_to(ROOT) / 'parity.json')
    paths.output.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(old / 'parity.json', paths.output / 'parity.json')
    from cp26.scoring import load_population, MASKS
    population = load_population(ROOT)
    population.verify_key_mapping(population.keys_by_day())
    summary = {'eligible_measurement_days': int(population.keys.delivery_date.nunique()),
               'eligible_hours': len(population.keys), 'measurement_calendar_days': len(population.calendar),
               'warmup_origins': 363, 'total_origins': len(E.calendar()),
               'mask_days': {m: int(population.masks[m].sum()) for m in MASKS},
               'population_evidence': population.evidence}
    if summary['eligible_measurement_days'] != 2068 or summary['measurement_calendar_days'] != 2078:
        raise RuntimeError('CP25 population differs from issued expectation')
    atomic(ROOT / RUN_EVIDENCE / 'namespace-and-population.json', {
        'run_id': RUN_ID, 'output': str(OUTPUT), 'local': str(paths.local),
        'scientific_namespace_empty_before_setup': True, 'old_science_imported': False,
        'old_hashes': {str(p.relative_to(ROOT)): sha(p) for p in preserve},
        'old_terminal_searches': len(list((old / 'search-results').glob('*/*.json'))),
        'old_issued_origins': len(list((old / 'forecast-ledger').glob('*.json'))),
        'parity_reuse': {'path': str(old.relative_to(ROOT) / 'parity.json'),
                        'sha256': sha(old / 'parity.json'), 'checks': len(parity['checks'])},
        'population': summary, 'protocol': protocol_identity(ROOT)})
    print(json.dumps(summary), flush=True)


def tests():
    target = H.art() / LOCAL_NAME / 'preparation-tests.log'
    target.parent.mkdir(parents=True, exist_ok=True)
    arguments = ['-q', 'tests/test_cp26_run_accounting.py', 'tests/test_cp26_execution.py',
                 'tests/test_cp26_costing.py', '--basetemp', str(H.art() / LOCAL_NAME / 'pytest-tmp-affected')]
    import pytest
    # Nested fixture monitors own isolated synthetic ledgers, not this scientific run.
    run_id = os.environ.pop('CP26_RUN_ID', None)
    try:
        with target.open('w') as log, contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            exit_code = int(pytest.main(arguments))
    finally:
        if run_id is not None:
            os.environ['CP26_RUN_ID'] = run_id
    value = {'status': 'PASS' if exit_code == 0 else 'FAIL',
             'command': ['pytest.main', *arguments], 'exit_code': exit_code,
             'code_sha256': code_identity(ROOT), 'protocol': protocol_identity(ROOT),
             'job_id': os.environ['CP26_JOB_ID'], 'job_index': int(os.environ['CP26_JOB_INDEX']),
             'log': str(target), 'log_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
    atomic(ROOT / OUTPUT / 'preparation-tests.json', value)
    print(target.read_text(), flush=True)
    return exit_code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('setup', 'tests', 'pilot-shard', 'pilot-assemble'))
    parser.add_argument('--shard', type=int, choices=range(4))
    args = parser.parse_args()
    if args.action == 'setup':
        setup()
    elif args.action == 'tests':
        return tests()
    else:
        from cp26.gates import ExecutionGate, authorize_consuming_process
        authorize_consuming_process(ROOT)
        pairs = None
        if args.action == 'pilot-shard':
            if args.shard is None:
                parser.error('--shard required')
            pairs = [(r, k) for k in range(14) for i, r in enumerate(E.ROUTES)
                     if (k * 3 + i) % 4 == args.shard]
        result = E.timing_pilot(ROOT, protocol_identity(ROOT), gate=ExecutionGate(ROOT), pairs=pairs)
        print(json.dumps({'status': result.get('status', 'SEALED_PILOT_COMPLETE'),
                          'probes': result['probes'] if pairs else len(result['probes'])}), flush=True)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
