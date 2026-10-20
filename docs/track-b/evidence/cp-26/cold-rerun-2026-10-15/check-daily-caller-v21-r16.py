"""Affected pure caller checks; no data, fit, new seed or scientific replay."""
import importlib.util
import json
import os
from pathlib import Path

ROOT = Path.cwd()
directory = ROOT / 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15'
spec = importlib.util.spec_from_file_location('cold_daily', directory / 'daily-execution-v21-r16.py')
daily = importlib.util.module_from_spec(spec)
spec.loader.exec_module(daily)
calls = []


class Cache:
    route, identity, base = 'nominal', {'frozen': True}, ROOT
    def load(self, *args, **kwargs):
        calls.append('read')
        return {'status': 'ok'}
    def save(self, *args, **kwargs):
        raise AssertionError('readonly cache wrote')


guarded = daily.GuardedCache(Cache(), lambda stage: calls.append(stage), readonly=True)
guarded.load('2020-01-01', 'A1', None, None)
guarded.load('2020-01-01', 'B2', None, None)
guarded.load('2020-01-02', 'A1', None, None)
assert calls == ['prepare', 'read', 'read', 'prepare', 'read']
before = list(calls)
def stop(stage):
    raise RuntimeError('demonstrated guard stop')
guarded = daily.GuardedCache(Cache(), stop, readonly=True)
try:
    guarded.load('2020-01-01', 'A1', None, None)
except RuntimeError as error:
    assert str(error) == 'demonstrated guard stop'
else:
    raise AssertionError('guard failure did not stop the cache read')
assert calls == before
try:
    guarded.save()
except RuntimeError:
    pass
else:
    raise AssertionError('readonly cache wrote')
assert "self.gate('forecast')" not in Path(daily.__file__).read_text()
assert "E._gate(gate, 'forecast', fitting=True)" in Path(daily.__file__).read_text()
plan = json.loads((directory / 'daily-execution-plan-v21-r16.json').read_bytes())
from datetime import date, timedelta
days = []
for row in plan['groups']:
    start, end = date.fromisoformat(row['first']), date.fromisoformat(row['through'])
    days.extend(start + timedelta(days=i) for i in range((end-start).days+1))
assert len(days) == len(set(days)) == 2441
assert days == [date(2020, 1, 1) + timedelta(days=i) for i in range(2441)]
import sys
sys.path.insert(0, str(ROOT / 'src'))
from cp26.budget import atomic
atomic(directory / 'daily-caller-checks-v21-r16.json', {
    'status': 'PASS', 'checks': 6, 'scope': 'guard cadence, fail-before-read, readonly prohibition, '
    'full startup admission retained, exact nonoverlapping2441-origin partition',
    'job_id': os.environ['CP26_JOB_ID'], 'job_index': int(os.environ['CP26_JOB_INDEX']),
    'run_id': os.environ['CP26_RUN_ID']})
print('6 affected physical caller checks PASS', flush=True)
