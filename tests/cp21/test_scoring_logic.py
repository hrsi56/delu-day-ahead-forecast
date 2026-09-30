"""CP-21 §17.5-§17.6 logic on synthetic losses: the shared index set, ratio intervals from the
same draws, stored replicates, the §14.4 endpoint reading and the mechanical adoption rule."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from cp15.scoring import FOLDS, FOLD_WINDOWS
from cp21 import scoring as S


def _daily(effects=None, seed=0, missing_day=True):
    """A matched 11-policy daily table: B0 is the normalizer, each policy a multiple of it."""
    rng = np.random.default_rng(seed)
    effects = effects or {}
    frames = []
    for fold, (start, end) in FOLD_WINDOWS.items():
        dates = pd.date_range(start, end)
        base_mae = rng.uniform(10, 30, len(dates))
        base_wis = base_mae * 0.6
        hours = np.full(len(dates), 24)
        if missing_day and fold == 'fold_3':
            hours[19] = 0  # an excluded date keeps zero observations, not zero loss
        for policy in S.POLICIES:
            f = effects.get(policy, 1.0)
            noise = rng.normal(1, 0.02, len(dates))
            mae = np.where(hours > 0, base_mae * f * noise, np.nan)
            wis = np.where(hours > 0, base_wis * f * noise, np.nan)
            frames.append(pd.DataFrame({'policy': policy, 'fold': fold, 'delivery_date': dates, 'n_hours': hours,
                                        'MAE': mae, 'WIS': wis}))
    return pd.concat(frames, ignore_index=True)


def test_index_set_is_cp20s_and_ratio_intervals_come_from_the_same_draws():
    daily = _daily({'HGL': 0.9, 'HG': 1.0})
    rows, draws, scores, meta = S.bootstrap(daily, replicates=2000)
    assert meta['index_sha256'] == S.CP20_INDEX_SHA256 and meta['index_equals_cp20']
    eq = rows.loc[rows.scope.eq('equal_fold') & rows.candidate.eq('HGL') & rows.baseline.eq('HG')].set_index('metric')
    for metric in ('MAE', 'WIS'):
        d = draws.loc[draws.scope.eq('equal_fold') & draws.candidate.eq('HGL') & draws.metric.eq(metric)]
        assert len(d) == 2000 and d.replicate.tolist() == list(range(2000))
        s_hgl = scores.loc[scores.policy.eq('HGL') & scores.metric.eq(metric), 'S'].to_numpy()
        s_hg = scores.loc[scores.policy.eq('HG') & scores.metric.eq(metric), 'S'].to_numpy()
        np.testing.assert_array_equal(d.ratio.to_numpy(), s_hgl / s_hg - 1)
        np.testing.assert_array_equal(d.difference.to_numpy(), s_hgl - s_hg)
        lo, hi = np.quantile(d.ratio, [.025, .975], method='linear')
        assert eq.loc[metric, 'ratio_ci_lower'] == lo and eq.loc[metric, 'ratio_ci_upper'] == hi
        assert eq.loc[metric, 'ratio'] < 0 and eq.loc[metric, 'ci_upper'] < 0
    # every contrast is stored at every scope
    expected = len(S.CONTRASTS) * 2 * 2000 * (1 + len(FOLDS))
    assert len(draws) == expected


def test_readings_improvement_worsening_and_mixed():
    rows, *_ = S.bootstrap(_daily({'L-R': 0.85, 'L-P': 1.0}), replicates=500)
    assert S.joint_reading(rows, 'L-R', 'L-P')['reading'] == 'observed joint improvement'
    rows, *_ = S.bootstrap(_daily({'L-R': 1.15, 'L-P': 1.0}), replicates=500)
    assert S.joint_reading(rows, 'L-R', 'L-P')['reading'] == 'observed joint worsening'
    rows, *_ = S.bootstrap(_daily({'L-R': 1.0, 'L-P': 1.0}, seed=4), replicates=500)
    reading = S.joint_reading(rows, 'L-R', 'L-P')
    assert reading['reading'] == 'no demonstrated joint preference' and set(reading['directions']) == {'MAE', 'WIS'}


def _criteria(met=True):
    status = 'met' if met else 'not_met'
    return pd.DataFrame([dict(policy='HGL', criterion=c, metric='x', scope='s', actual=1.0, lower_limit=None,
                              upper_limit=None, comparator=None, status=status if c == 3 else 'met',
                              passed=(status == 'met') if c == 3 else True) for c in range(1, 7)])


def test_adoption_first_unmet_condition_is_reported_mechanically():
    improving, *_ = S.bootstrap(_daily({'HGL': 0.9, 'HG': 1.0}), replicates=500)
    verdict = S.adoption(improving, _criteria(True), keys_complete=True)
    assert verdict['verdict'] == 'v4' and verdict['first_unmet_condition'] is None
    assert S.adoption(improving, _criteria(False), keys_complete=True)['first_unmet_condition'] == 2
    assert S.adoption(improving, _criteria(True), keys_complete=False)['first_unmet_condition'] == 3
    worse, *_ = S.bootstrap(_daily({'HGL': 1.1, 'HG': 1.0}), replicates=500)
    v = S.adoption(worse, _criteria(True), keys_complete=True)
    assert v['verdict'] == 'Not adopted' and v['first_unmet_condition'] == 1 and 4 in v['unmet_conditions']
    assert v['conditions'][4]['values']['folds_decisively_worse'], 'resolved per-fold degradations are listed'


def test_one_fold_degradation_vetoes_an_otherwise_improving_candidate():
    daily = _daily({'HGL': 0.8, 'HG': 1.0})
    part = daily.policy.eq('HGL') & daily.fold.eq('fold_2')
    daily.loc[part, ['MAE', 'WIS']] *= 1.5  # fold 2 decisively worse, the aggregate still better
    rows, *_ = S.bootstrap(daily, replicates=500)
    v = S.adoption(rows, _criteria(True), keys_complete=True)
    assert v['conditions'][1]['met'] and not v['conditions'][4]['met'] and v['first_unmet_condition'] == 4


def test_undefined_draws_leave_the_interval_unresolved():
    daily = _daily()
    daily.loc[daily.policy.eq('B0') & daily.fold.eq('fold_1'), ['MAE', 'WIS']] = 0.0  # zero normalizer
    rows, *_ = S.bootstrap(daily, replicates=200)
    assert rows.loc[rows.scope.eq('equal_fold'), 'status'].eq('unresolved_uncertainty').all()


def test_refuses_an_unmatched_grid():
    daily = _daily()
    with pytest.raises(ValueError):
        S.bootstrap(daily.iloc[1:], replicates=10)
