"""Affected static-window ownership checks; no model fits or market-data reads."""
import ast
from contextlib import ExitStack
from datetime import date, timedelta
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path.cwd()
DIRECTORY = ROOT / 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15'


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, DIRECTORY / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = load('original_cold_daily', 'daily-execution-v21-r16.py')
daily = load('native_window_daily', 'daily-execution-v21-r16-fit-only.py')
daily.require_custody(ROOT)

# The functions that select inputs, fit members, replay causal state and emit
# immutable evidence are bytecode-independent AST matches to the original.
def definitions(path):
    return {node.name: ast.dump(node, include_attributes=False)
            for node in ast.parse(Path(path).read_text()).body
            if isinstance(node, (ast.FunctionDef, ast.ClassDef))}


before, after = definitions(old.__file__), definitions(daily.__file__)
unchanged = ('GuardedCache', '_setup', '_phase', '_fit_route_owned', '_replay_owned')
assert all(before[name] == after[name] for name in unchanged)

expected = [date(2021, 5, 5) + timedelta(days=i) for i in range(1951)]
for route in daily.ROUTES:
    windows = daily.native_windows(ROOT, route)
    actual = [first + timedelta(days=i) for first, through in windows
              for i in range((through-first).days+1)]
    assert actual == expected and len(set(actual)) == 1951
    assert len(windows) == (8 if route == 'nominal' else 4)
    assert actual[-1] == date(2026, 9, 6)


def rejected(error_type, operation):
    try:
        operation()
    except error_type:
        return
    raise AssertionError('ownership or range guard did not reject the operation')


base = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/cold-rerun-2026-10-15/r16')
with tempfile.TemporaryDirectory(prefix='native-window-checks-', dir=base) as temporary:
    locks = Path(temporary) / 'locks'
    first, second = daily.native_windows(ROOT, 'nominal')[:2]

    def enter_window(window=first):
        with daily.native_window_lease(ROOT, locks, 'nominal', *window):
            pass

    def enter_original():
        with old.lease(locks, 'fit-nominal'):
            pass

    with daily.native_window_lease(ROOT, locks, 'nominal', *first):
        with daily.native_window_lease(ROOT, locks, 'nominal', *second):
            rejected(RuntimeError, enter_window)
            rejected(RuntimeError, enter_original)
    with old.lease(locks, 'fit-nominal'):
        rejected(RuntimeError, enter_window)
    enter_window()

    # Read-only replay must acquire the route locks before its data-consuming
    # routine. Test this with local lock fixtures, never live fit-worker locks.
    sys.path.insert(0, str(ROOT / 'src'))
    from cp26 import harness as H
    fake_artifacts = Path(temporary) / 'artifacts'
    route_locks = fake_artifacts / 'cold-rerun-2026-10-15/route-leases'
    with patch.object(H, 'art', return_value=fake_artifacts), \
            patch.object(daily, '_replay_owned', return_value='checked') as replay:
        with daily.native_window_lease(ROOT, route_locks, 'nominal', *first):
            rejected(RuntimeError, lambda: daily._replay(
                ROOT, first[1], readonly=True, budget=None))
            replay.assert_not_called()
        assert daily._replay(ROOT, first[1], readonly=True, budget=None) == 'checked'
        replay.assert_called_once()

    # No arbitrary or overlapping range can acquire shared native ownership.
    rejected(ValueError, lambda: enter_window((first[0], second[1])))
    rejected(ValueError, lambda: daily.native_windows(ROOT, 'unregistered'))
    fake_root = Path(temporary) / 'changed-plan'
    plan = fake_root / daily.NATIVE_PLAN
    plan.parent.mkdir(parents=True)
    plan.write_bytes((ROOT / daily.NATIVE_PLAN).read_bytes() + b'\n')
    rejected(RuntimeError, lambda: daily.native_windows(fake_root, 'nominal'))

job_id = os.environ.get('CP26_JOB_ID')
run_id = os.environ.get('CP26_RUN_ID')
if not job_id or run_id != 'cp26-cold-rerun-2026-10-15-01':
    raise RuntimeError('registered CP26_JOB_ID and CP26_RUN_ID are required')
from cp26.budget import atomic
atomic(DIRECTORY / 'native-window-checks-v21-r16.json', {
    'status': 'PASS', 'checks': 7, 'job_id': job_id,
    'job_index': int(os.environ.get('CP26_JOB_INDEX', '-1')), 'run_id': run_id,
    'unchanged_scientific_routines': list(unchanged),
    'caller_sha256': hashlib.sha256(Path(daily.__file__).read_bytes()).hexdigest(),
    'scope': 'Exact1951date coverage per route; finite disjoint windows; duplicate '
             'exclusion; shared-native/exclusive-original interlock in both directions; '
             'replay exclusion before data access and release; invalid ranges/routes; '
             'execution-plan pin; original fit/replay/cache routines unchanged.'})
print('7 affected native-window ownership checks PASS', flush=True)
