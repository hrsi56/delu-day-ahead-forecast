"""Does the rich-admin liveness test time out only when no bytecode exists? Cold, then warm."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).parent))
import ci_check as C  # noqa: E402

CAND = sys.argv[1]
OUT = Path(sys.argv[2]).resolve()
RUNS = int(sys.argv[3]) if len(sys.argv) > 3 else 2
TEST = ('tests/test_cp26_ledger_liveness.py::'
        'test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history')
OUT.mkdir(parents=True)
main = C.git('rev-parse', 'main').strip()
paths, _ = C.curated(main, CAND)
tree = OUT / 'tree'
tree.mkdir()
C.extract(main, [], tree)
C.extract(CAND, paths, tree)
env = C.environment(OUT)
record = {'candidate': CAND, 'steps': []}


def step(name, command, **extra):
    began = time.time()
    run = subprocess.run(command, cwd=tree, env={**env, **extra}, capture_output=True, text=True)
    (OUT / f'{name}.log').write_text(run.stdout + run.stderr)
    lines = [line for line in (run.stdout + run.stderr).splitlines() if line.strip()]
    record['steps'].append({'step': name, 'exit_code': run.returncode, 'seconds': round(time.time() - began, 2),
                            'summary': lines[-1] if lines else ''})
    print(json.dumps(record['steps'][-1])[:400], flush=True)
    return run


def pyc_count():
    return sum(1 for _ in (OUT / 'env').rglob('*.pyc')) + sum(1 for _ in (tree / 'src').rglob('*.pyc'))


step('sync', ['uv', 'sync', '--locked', '--dev'])
record['pyc_after_sync'] = pyc_count()
step('import-cold-B', ['uv', 'run', 'python', '-B', '-c', 'import cp26.supervisor, cp26.budget'],
     PYTHONPATH=str(tree / 'src'))
record['pyc_after_cold_import'] = pyc_count()
for index in range(RUNS):
    step(f'test-cold-{index}', ['uv', 'run', 'pytest', '-q', '-p', 'no:cacheprovider', '-rfE',
                                f'--basetemp={OUT}/bt-cold-{index}', TEST])
record['pyc_after_cold_tests'] = pyc_count()
step('warm-bytecode', ['uv', 'run', 'python', '-c', 'import cp26.supervisor, cp26.budget, cp26.harness'],
     PYTHONPATH=str(tree / 'src'))
record['pyc_after_warm'] = pyc_count()
step('import-warm-B', ['uv', 'run', 'python', '-B', '-c', 'import cp26.supervisor, cp26.budget'],
     PYTHONPATH=str(tree / 'src'))
for index in range(RUNS):
    step(f'test-warm-{index}', ['uv', 'run', 'pytest', '-q', '-p', 'no:cacheprovider', '-rfE',
                                f'--basetemp={OUT}/bt-warm-{index}', TEST])
(OUT / 'experiment.json').write_text(json.dumps(record, indent=1) + '\n')
shutil.rmtree(OUT / 'env', ignore_errors=True)
print(json.dumps({k: v for k, v in record.items() if k != 'steps'}))
