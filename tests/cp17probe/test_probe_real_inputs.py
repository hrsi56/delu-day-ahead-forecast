"""CP-17-probe on the real development inputs: the payload embargo, and A1's native parity with CP-26.

These need CP-26's local-only stored state (the serving searches and the forecast ledger, extracted from
the local tag `evidence/cp-26` into `.local/artifacts/cp-17-probe/inputs/`), so they skip with that
reason where it is absent, as on CI. `CP17_PROBE_PROJECT_ROOT` names the checkout holding `.local/`.
"""
from __future__ import annotations

from dataclasses import replace
from datetime import date, timedelta
import json
import os
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from cp17probe import dailyfit, native, payload

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(os.environ.get('CP17_PROBE_PROJECT_ROOT', '/Users/djourno/Downloads/PJM'))
INPUTS = PROJECT / '.local/artifacts/cp-17-probe/inputs'
FITS = PROJECT / ('.local/artifacts/cp-26/cold-rerun-2026-10-15/fits/'
                  '195857d79c60b5573ae2238989be1f3042d71a67df9831fc36471a81e9736f3b/nominal')
DAY = date(2026, 9, 6)
K13 = INPUTS / native.RUN / 'search-results/nominal/k13.json'

pytestmark = pytest.mark.skipif(not (K13.exists() and (FITS / str(DAY) / 'D2.json').exists()),
                                reason="CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent")
BLAS = ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')


@pytest.fixture(scope='module')
def ctx():
    if any(os.environ.get(n) != '1' for n in BLAS):
        pytest.skip('BLAS threads must be set to 1 before NumPy loads, as in CP-26 (export the five *_NUM_THREADS=1)')
    return payload.context(ROOT)


@pytest.fixture(scope='module')
def ensemble():
    return json.loads(K13.read_text())


def test_the_a1_payload_carries_no_outcome_of_its_day(ctx, ensemble):
    arrays, meta = payload.a1_payload(ctx, DAY, ensemble)
    assert np.isnan(arrays['price'][-1]).all() and np.isnan(arrays['y'][-1]).all() and not arrays['mask'][-1].any()
    assert set(arrays) == set(dailyfit.A1_ARRAYS)
    assert arrays['days'][-1] == np.datetime64(DAY, 'D').astype('int64')
    assert date.fromisoformat(meta['first']) == DAY - timedelta(days=735)


def _with(ctx, **arrays):
    """A copy of the context whose day table has the given arrays replaced (the loaded arrays are read-only)."""
    return SimpleNamespace(dd=replace(ctx.dd, **arrays), keys=ctx.keys, data=ctx.data)


def test_the_payload_ignores_the_days_outcome_and_follows_its_window(ctx, ensemble):
    base = payload.a1_payload(ctx, DAY, ensemble)[1]['payload_sha256']
    i = ctx.dd.ix(DAY)
    price, y = ctx.dd.price.copy(), ctx.dd.y.copy()
    price[i] += 500.0
    y[i] -= 500.0
    assert payload.a1_payload(_with(ctx, price=price, y=y), DAY, ensemble)[1]['payload_sha256'] == base
    window = ctx.dd.price.copy()
    window[ctx.dd.ix(DAY - timedelta(days=30)), 5] += 1.0
    assert payload.a1_payload(_with(ctx, price=window), DAY, ensemble)[1]['payload_sha256'] != base


def test_the_v2_payload_refuses_an_unreleased_h_day(ctx):
    days = [DAY - timedelta(days=d) for d in range(29, 1, -1)]
    state = {'last_origin': str(DAY),
             'buffer': [{'day': str(d), 'errors': [0.0] * len(ctx.data.rows(d, eligible=False))} for d in days]}
    arrays, meta = payload.v2_payload(ctx, DAY, state, ctx.data.p)
    on_day = arrays['dates'] == np.datetime64(DAY, 'D').astype('int64')
    assert on_day.sum() == 24 and np.isnan(arrays['y'][on_day]).all() and np.isfinite(arrays['y'][~on_day][-48:]).all()
    late = dict(state, buffer=state['buffer'][1:] + [{'day': str(DAY - timedelta(days=1)), 'errors': [0.0] * 24}])
    with pytest.raises(ValueError, match='D-2'):
        payload.v2_payload(ctx, DAY, late, ctx.data.p)
    with pytest.raises(ValueError, match='after the development boundary'):
        payload.v2_payload(ctx, DAY + timedelta(days=1), state, ctx.data.p)


def test_a1_from_its_payload_reproduces_cp26_bitwise(ctx, ensemble, tmp_path):
    arrays, meta = payload.a1_payload(ctx, DAY, ensemble)
    files = payload.write(arrays, meta, tmp_path, 'A1')
    result = dailyfit.run('A1', files['npz'], files['meta'], attribution=True)
    check = native.check(result, native.stored(INPUTS, FITS, DAY, 'D2'), 'A1')
    assert check['bitwise_equal'] and check['selections']['all_match'], check
    shap = result['attribution']
    assert shap['efficiency_max_abs'] < 1e-9 and shap['issued_gap_max_abs'] < 1e-9
    assert {'price_d1', 'load_d0', 'weekday'} <= set(shap['players'])
