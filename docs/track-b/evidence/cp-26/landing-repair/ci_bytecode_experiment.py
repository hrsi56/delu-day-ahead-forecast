"""The rich-admin liveness test alone, in a fresh tree and venv, with Python writing bytecode as on CI.

CI does not set PYTHONDONTWRITEBYTECODE; this machine's shell does. Runs the test alone N times
and reports, from each run's inner ledger, how long the admin job took against the 15 s window.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).parent))
import ci_check as C  # noqa: E402

CAND, OUT, RUNS = sys.argv[1], Path(sys.argv[2]).resolve(), int(sys.argv[3])
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
env.pop('PYTHONDONTWRITEBYTECODE', None)
record = {'candidate': CAND, 'PYTHONDONTWRITEBYTECODE': 'unset, as on CI', 'runs': []}
subprocess.run(['uv', 'sync', '--locked', '--dev'], cwd=tree, env=env, check=True, capture_output=True)
record['pyc_after_sync'] = sum(1 for _ in (OUT / 'env').rglob('*.pyc'))
for index in range(RUNS):
    base = OUT / f'bt-{index}'
    began = time.time()
    run = subprocess.run(['uv', 'run', 'pytest', '-q', '-p', 'no:cacheprovider', '-rfE', f'--basetemp={base}', TEST],
                         cwd=tree, env=env, capture_output=True, text=True)
    (OUT / f'test-{index}.log').write_text(run.stdout + run.stderr)
    ledger = next(base.glob('*/.local/artifacts/cp-26/ledger/budget.json'))
    jobs = {j['name']: j for j in json.loads(ledger.read_text())['jobs'][160:]}
    admin = jobs.get('ledger-rich-admin', {})
    lines = [line for line in (run.stdout + run.stderr).splitlines() if line.strip()]
    record['runs'].append({'index': index, 'exit_code': run.returncode, 'summary': lines[-1] if lines else '',
                           'seconds': round(time.time() - began, 2),
                           'admin_wall_seconds': admin.get('wall_seconds'),
                           'admin_running': admin.get('running'), 'admin_exit_code': admin.get('exit_code'),
                           'pyc_in_env': sum(1 for _ in (OUT / 'env').rglob('*.pyc'))})
    print(json.dumps(record['runs'][-1]), flush=True)
(OUT / 'experiment.json').write_text(json.dumps(record, indent=1) + '\n')
shutil.rmtree(OUT / 'env', ignore_errors=True)
print(json.dumps({k: v for k, v in record.items() if k != 'runs'}))
