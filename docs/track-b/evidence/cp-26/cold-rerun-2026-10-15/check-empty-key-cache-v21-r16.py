"""One guarded key check and affected empty-cache checks; no model fitting."""
import ast
from datetime import date
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
DIRECTORY = ROOT / 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15'
path = DIRECTORY / 'daily-execution-v21-r16-empty-keys.py'
spec = importlib.util.spec_from_file_location('empty_key_daily', path)
daily = importlib.util.module_from_spec(spec)
spec.loader.exec_module(daily)
daily.require_custody(ROOT)

from cp26 import fits, gates as G, harness as H, state
from cp26.scoring import load_population
import numpy as np
import pandas as pd

G.authorize_consuming_process(ROOT)
day = date(2022, 2, 22)
H.install_issue_label(H.NEW)
data = H.load(ROOT, H.NEW)
native_index = data.index[data.rows(day)]
population = load_population(ROOT)
score_index = population.keys_by_day()[day]
assert len(native_index) == len(score_index) == 0

def rejected(error, operation):
    try:
        operation()
    except error:
        return
    raise AssertionError('required validation did not fail')

original = state.quantiles
assert fits.quantiles is original
empty = np.empty((0, 7))
rejected(ValueError, lambda: original(json.loads(json.dumps(empty.tolist())), 0))

base = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/cold-rerun-2026-10-15/r16')
with tempfile.TemporaryDirectory(prefix='empty-key-cache-checks-', dir=base) as directory:
    cache = fits.FitCache(directory, 'nominal', {'fixture': 'empty-key-cache'})
    result = {'status': 'ok', 'central': np.empty(0), 'quantiles': empty}
    ensemble = {'fixture': 'empty-key-cache'}
    issue = H.issue_instant(day, H.NEW)
    with patch('cp26.search.validate_ensemble'):
        rejected(ValueError, lambda: cache.save(day, 'D2', native_index, issue, result, ensemble=ensemble))
        assert not cache.path(day, 'D2').exists()
        with daily.empty_quantile_axis():
            assert state.quantiles is original
            saved = cache.save(day, 'D2', native_index, issue, result, ensemble=ensemble)
            raw = cache.path(day, 'D2').read_bytes()
            loaded = cache.load(day, 'D2', native_index, issue, ensemble=ensemble)
            assert loaded['quantiles'].shape == (0, 7)
            assert loaded['central'].shape == (0,)
            assert loaded['cache_content_sha256'] == saved
            rejected(FileExistsError, lambda: cache.save(day, 'D2', native_index, issue, result, ensemble=ensemble))
            assert cache.path(day, 'D2').read_bytes() == raw
            good = np.arange(14, dtype=float).reshape(2, 7)
            assert np.array_equal(fits.quantiles(good.tolist(), 2), original(good, 2))
            for invalid, n in (([], 1), (np.empty((0, 8)), 0), ([[1.] * 7], 0),
                               (good[:, ::-1], 2), (np.full((2, 7), np.nan), 2),
                               (np.ones((2, 6)), 2)):
                rejected(ValueError, lambda v=invalid, count=n: fits.quantiles(v, count))
        assert fits.quantiles is state.quantiles is original

# A zero-key calendar date remains missing and never seeds own errors. Its
# original state validator is untouched by the cache serialization adapter.
policy = state.PolicyState('D2', 'nominal', {'fixture': 'empty-key-cache'}, 'direct')
policy.release(day, lambda index: np.empty(0))
row = policy.issue(day, native_index, np.empty(0), issue_utc=H.issue_instant(day, H.NEW),
                   native_quantiles=empty, scoring_index=score_index, scored=True)
assert not row['native_central_valid'] and not row['error_eligible']
assert row['output_source'] == 'missing' and row['reason'] == 'no_native_forecast_keys'
assert state.PolicyState.from_dict(json.loads(json.dumps(policy.to_dict()))).to_dict() == policy.to_dict()

def definitions(p):
    return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(p.read_text()).body
            if isinstance(n, (ast.FunctionDef, ast.ClassDef))}

old = definitions(DIRECTORY / 'daily-execution-v21-r16-fit-only.py')
new = definitions(path)
assert all(old[name] == new[name] for name in old)
job = os.environ.get('CP26_JOB_ID')
assert job and os.environ.get('CP26_RUN_ID') == G.RUN_ID
from cp26.budget import atomic
atomic(DIRECTORY / 'empty-key-cache-checks-v21-r16.json', {
    'status': 'PASS', 'checks': 8, 'job_id': job,
    'job_index': int(os.environ['CP26_JOB_INDEX']), 'run_id': G.RUN_ID,
    'guarded_native_keys_on_2022_02_22': len(native_index),
    'frozen_scoring_keys_on_2022_02_22': len(score_index),
    'caller_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
    'all_original_caller_functions_ast_unchanged': True,
    'state_quantile_validator_unchanged': True,
    'scope': 'Guarded zero-key diagnosis; original cache failure reproduced; empty-axis '
             'save/load with identical hashes; no overwrite; nonempty parity; strict invalid '
             'shape/nonfinite/order rejection; no own-error intake and calendar preservation; '
             'validator restoration and original scientific/ownership caller routines unchanged.',
    'model_fits': 0})
print('8 affected empty-key cache checks PASS; zero native/scoring keys verified; no model fits', flush=True)
