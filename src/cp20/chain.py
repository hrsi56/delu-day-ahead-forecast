"""Unattended CP-20 extraction chain (Owner standing instruction S1, 2026-09-23).

Phases run strictly one after another, each a monitored single-endpoint job:
  1. NCAR, all runs, 3 workers;
  2. AWS alone, all runs except the days that had already failed, 1 worker;
  3. final retry: every still-incomplete run (the earlier failed days included), AWS then NCAR.
A phase continues the chain only on exit 0 (complete) or 5 (some runs failed after their
bounded counted attempts). Any other end (stop request, contradiction, 60 minutes without
data, a cap or stop line) stops the chain and is written to ``chain-status.json``. Network
problems are handled inside the fetcher and never stop the chain.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
P = Path('/Users/djourno/Downloads/PJM')
A = P / '.local/artifacts/cp-20'
PY, WX = P / '.venv/bin/python', A / 'wx-venv/bin/python'
CONTINUE = {0, 5}


def status(**fields):
    path = A / 'chain-status.json'
    state = json.loads(path.read_text()) if path.exists() else {'phases': []}
    state.update(fields)
    tmp = path.with_suffix('.tmp')
    tmp.write_text(json.dumps(state, indent=1))
    os.replace(tmp, path)
    return state


def phase(name, endpoint, workers, select='all', exclude=''):
    cmd = [str(PY), 'scripts/cp20_weather.py', '--monitor', '--name', 'gfs-extract', '--workers', str(workers),
           '--stop-machine-hours', '85', '--log', str(A / 'logs/gfs-extract.log'), '--',
           str(WX), '-u', '-m', 'cp20.extract', '--manifest', 'reports/weather-ablation/run-manifest.json',
           '--out', str(A / 'weather'), '--admission', 'reports/weather-admission', '--select', select,
           '--endpoint', endpoint, '--workers', str(workers), '--stop-transfer-gib', '150', '--inventory-added']
    if exclude:
        cmd += ['--exclude', exclude]
    began = time.time()
    state = status(current=name)
    state['phases'].append({'phase': name, 'endpoint': endpoint, 'workers': workers, 'start_epoch': began})
    status(phases=state['phases'])
    code = subprocess.call(cmd, cwd=ROOT)
    marker = json.loads((A / 'markers' / ('gfs-extract.DONE.json' if code == 0 else 'gfs-extract.FAILED.json')).read_text())
    state = status()
    state['phases'][-1].update(end_epoch=time.time(), monitor_exit=code, marker=marker)
    status(phases=state['phases'])
    return code, marker


def failed_days():
    path = A / 'weather/failures.jsonl'
    if not path.exists():
        return []
    runs = {json.loads(l)['run'] for l in path.read_text().splitlines()}
    return sorted(r for r in runs if not (A / f'weather/runs/{r}.json').exists())


def main():
    caffeinate = subprocess.Popen(['/usr/bin/caffeinate', '-i', '-w', str(os.getpid())])
    deferred = ','.join(failed_days())
    status(started_epoch=time.time(), pid=os.getpid(), deferred_failed_days=deferred, result=None)
    plan = [('ncar-all', 'ncar', 3, 'all', ''), ('aws-all', 'aws', 1, 'all', deferred),
            ('retry-aws', 'aws', 1, 'all', ''), ('retry-ncar', 'ncar', 3, 'all', '')]
    for name, endpoint, workers, select, exclude in plan:
        code, marker = phase(name, endpoint, workers, select, exclude)
        child = (marker.get('abort_reason'), marker.get('exit_code'))
        if code not in CONTINUE and marker.get('exit_code') not in CONTINUE:
            status(result='stopped', stopped_in=name, reason=child, end_epoch=time.time())
            caffeinate.terminate()
            return 1
    remaining = [r for r in json.loads((ROOT / 'reports/weather-ablation/run-manifest.json').read_text())['runs']
                 if not (A / f'weather/runs/{r["run_00z"]}.json').exists()]
    status(result='complete' if not remaining else 'finished_with_incomplete_runs',
           incomplete_runs=[r['run_00z'] for r in remaining], end_epoch=time.time())
    caffeinate.terminate()
    return 0


if __name__ == '__main__':
    sys.exit(main())
