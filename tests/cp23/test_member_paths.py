"""CP-23's fit, selection, cache and replay paths end to end on a synthetic calendar (no research data).

A synthetic `Inputs`-like object with real Europe/Berlin delivery hours exercises:

* the one-per-fold configuration choice and its training-only rows;
* one origin's ensemble fit and emission;
* the DDNN cache's identity, hash and refusal checks;
* the replay of v5, v3+D and D through CP-16's H layer, with D's own quantiles.

The training recipe is shortened through monkeypatching, so these fixture fits are fast. They use no
research data and are not DDNN member fits on the evaluation population.
"""
from datetime import date, timedelta
import types

import numpy as np
import pandas as pd
import pytest

from cp15.data import day_hours
from cp16.residuals import SharedResidualState
from cp23 import ddnn as D
from cp23 import execution as E
from cp23.budget import Budget
from cp23.member import fit_origin, fit_selection


class Data:
    """The attributes `model_rows`, the features and the replay read, on a synthetic hourly calendar."""

    def __init__(self, start: date, days: int, seed: int = 0):
        rng = np.random.default_rng(seed)
        index = pd.DatetimeIndex(np.concatenate([day_hours(start + timedelta(days=k)).as_unit('ns') for k in range(days)]))
        local = index.tz_convert('Europe/Berlin')
        self.index = index
        self.dates = np.array(local.date, dtype='datetime64[D]')
        self.hours = local.hour.to_numpy()
        n = len(index)
        self.level = 60 + 10 * np.sin(np.arange(n) / 500)
        self.scale = np.full(n, 15.0)
        self.y = self.level + self.scale * (0.3 * np.sin(self.hours / 24 * 2 * np.pi) + rng.standard_t(5, n) * 0.5)
        self.eligible = np.ones(n, bool)
        self.feature_valid = self.eligible

    def rows(self, d, eligible=True):
        return np.flatnonzero(self.dates == np.datetime64(d))


@pytest.fixture
def short_recipe(monkeypatch):
    monkeypatch.setitem(D.TRAINING, 'max_epochs', 3)
    monkeypatch.setitem(D.TRAINING, 'patience', 2)
    monkeypatch.setitem(D.TRAINING, 'batch_size', 512)


def _design(data):
    rng = np.random.default_rng(1)
    x = np.column_stack([np.eye(24)[data.hours], rng.normal(0, 1, (len(data.y), 3))])
    wx = rng.normal(0, 1, (len(data.y), 3))
    wx[::50, 0] = np.nan
    return x, wx, (data.y - data.level) / data.scale, np.ones(len(data.y), bool)


def test_selection_and_origin_fit_use_training_rows_only_and_emit_ordered_quantiles(short_recipe, tmp_path):
    data = Data(date(2019, 1, 1), 460)
    x, wx, z, present = _design(data)
    budget = Budget(tmp_path / 'b.json')
    budget.initialise({'git_bytes': 0})
    charged = []
    d0 = date(2020, 3, 1)
    sel = fit_selection(data, x, wx, z, present, d0, charge=lambda: charged.append('s'))
    assert len(charged) == len(D.CONFIGS) * len(D.SEEDS)
    assert sel['selected'] in {c['id'] for c in D.CONFIGS} and sel['rows']['holdout_last'] < str(d0)
    assert sel['rows']['stop_last'] < sel['rows']['holdout_first'] and sel['rows']['train_last'] < sel['rows']['stop_first']
    # outcomes on or after D0 cannot change the choice
    later = Data(date(2019, 1, 1), 460)
    later.y = data.y.copy()
    later.y[later.dates >= np.datetime64(d0)] += 500
    z2 = (later.y - later.level) / later.scale
    assert fit_selection(later, x, wx, z2, present, d0)['holdout_mae'] == sel['holdout_mae']
    fit = fit_origin(data, x, wx, z, present, d0, sel['selected'], charge=lambda: charged.append('f'))
    assert len(charged) == len(D.CONFIGS) * len(D.SEEDS) + len(D.SEEDS)
    q = fit['quantiles']
    assert q.shape == (24, 7) and np.isfinite(q).all() and np.all(np.diff(q, axis=1) > 0)
    assert np.array_equal(fit['central'], q[:, D.MEDIAN]) and fit['crossed_rows'] == 0
    assert fit['member_jsu_params'].shape == (len(D.SEEDS), 24, 4)
    assert fit['rows']['stop_last'] < str(d0) and fit['rows']['n_forecast'] == 24
    item = E.ddnn_entry(fit, 'fold_x', {'cp23_input_fingerprint': 'f', 'cp23_protocol_sha256': 'p', 'weather_design_sha256': 'w'})
    cache = E.DDNNCache('fold_x', data, {'cp23_input_fingerprint': 'f', 'cp23_protocol_sha256': 'p',
                                         'weather_design_sha256': 'w'}, tmp_path / 'fits')
    cache.save(item)
    got = cache.get(d0)
    assert np.array_equal(got['central'], fit['central']) and np.array_equal(got['quantiles'], q)
    wrong = E.DDNNCache('fold_x', data, {'cp23_input_fingerprint': 'other', 'cp23_protocol_sha256': 'p',
                                         'weather_design_sha256': 'w'}, tmp_path / 'fits')
    with pytest.raises(ValueError, match='stale or wrong'):
        wrong.get(d0)


class FakeSources:
    """Members for the replay: v3/v4 members and a D with its own ordered quantiles."""

    def __init__(self, data, policies):
        self.data, self.policies = data, tuple(policies)

    def get(self, d):
        rows = self.data.rows(d)
        base = self.data.level[rows]
        m = {'A1': base + 1, 'B2': base - 1, 'L-N': base + 2, 'L-R': base - 2}
        m['HG'] = m['A1'] / 2 + m['B2'] / 2
        m['HGL'] = m['A1'] / 3 + m['B2'] / 3 + m['L-N'] / 6 + m['L-R'] / 6
        m['D'] = base + 0.5
        m['D_quantiles'] = m['D'][:, None] + np.array([-20, -10, -5, 0, 5, 10, 20.0])[None, :]
        m['D_config'] = 'C1'
        centers = {'v5': E.v5_central(m['HGL'], m['D']), 'v3+D': E.v3d_central(m['A1'], m['B2'], m['D']), 'D': m['D']}
        return rows, {p: centers[p] for p in self.policies}, m, 'synthetic'


def test_replay_runs_the_h_layer_for_v5_and_v3d_and_emits_ds_own_quantiles(tmp_path):
    data = Data(date(2020, 1, 1), 70)
    budget = Budget(tmp_path / 'b.json')
    budget.initialise({'git_bytes': 0})
    states = {p: SharedResidualState() for p in E.H_POLICIES}
    lineage, frames = {'origins': []}, []
    dates = list(pd.date_range('2020-01-01', '2020-03-10').date)
    predict = set(dates[40:])
    truth = (lambda s: (lambda ix: s.reindex(ix).to_numpy()))(pd.Series(data.y, index=data.index))
    E.replay(data, 'fold_x', dates, FakeSources(data, E.NEW_POLICIES), states, truth, predict, lineage, 'synthetic',
             frames, budget, 'policy_days_admission')
    out = pd.concat(frames, ignore_index=True)
    assert set(out.policy) == set(E.NEW_POLICIES)
    assert out.groupby('policy').size().to_dict() == {p: sum(len(data.rows(d)) for d in predict) for p in E.NEW_POLICIES}
    q = out[['p025', 'p10', 'p25', 'p50', 'p75', 'p90', 'p975']].to_numpy()
    assert np.all(np.diff(q, axis=1) >= 0) and np.isfinite(q).all()
    d = out.loc[out.policy.eq('D')]
    assert np.array_equal(d.central.to_numpy(), d.p50.to_numpy())
    h = out.loc[out.policy.eq('v5')]
    assert not np.array_equal(h.central.to_numpy(), h.p50.to_numpy())  # the emitted p50 is kept separate from the central
    gaps = [r['composite_gap'] for r in lineage['origins'] if r['policy'] in E.H_POLICIES and r['predicted']]
    assert gaps and max(gaps) <= E.COMPOSITE_TOLERANCE
    assert budget.read()['counts']['policy_days'] == len(dates) * len(E.NEW_POLICIES)
