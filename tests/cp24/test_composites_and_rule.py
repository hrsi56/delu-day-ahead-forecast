"""CP-24 composites and the mechanical `cp24-adoption` rule (§23.5, §23.9, §23.10), on synthetic fixtures."""
import numpy as np
import pandas as pd
import pytest

from cp22.scoring import FOLDS
from cp24 import scoring as S
from cp24.execution import COMPOSITE_TOLERANCE, composite_gap, v3d2_central, v5_central


def test_v5_and_v3d2_composites_are_the_fixed_weights():
    rng = np.random.default_rng(1)
    a1, b2, ln, lr, d2 = (rng.normal(80, 30, 500) for _ in range(5))
    c_v4 = a1 / 3 + b2 / 3 + ln / 6 + lr / 6
    c_hg = a1 / 2 + b2 / 2
    v5 = v5_central(a1, b2, ln, lr, d2)
    v3d2 = v3d2_central(a1, b2, d2)
    m = {'HGL': c_v4, 'HG': c_hg, 'D2': d2, 'L-N': ln, 'L-R': lr}
    assert composite_gap('v5', v5, m) <= COMPOSITE_TOLERANCE           # c_v5 - c_v4 = (1/6)(D2 - L)
    assert composite_gap('v3+D2', v3d2, m) <= COMPOSITE_TOLERANCE
    assert np.max(np.abs(v5 - ((2 / 3) * c_hg + (ln / 2 + lr / 2) / 6 + d2 / 6))) <= 1e-9   # LEAR keeps its two thirds
    assert np.array_equal(v3d2, a1 / 3 + b2 / 3 + d2 / 3)
    # positive controls: CP-23's one-third weight, or another split, is caught
    assert composite_gap('v5', 2 * c_v4 / 3 + d2 / 3, m) > COMPOSITE_TOLERANCE
    assert composite_gap('v5', a1 / 3 + b2 / 3 + ln / 6 + d2 / 6, m) > COMPOSITE_TOLERANCE
    with pytest.raises(ValueError):
        v5_central(a1, b2, ln, lr, np.append(d2[:-1], np.nan))


def _uncertainty(eq_mae, eq_wis, fold_rows, ci975=None):
    rows = []
    for metric, (point, lo, hi) in (('MAE', eq_mae), ('WIS', eq_wis)):
        lo975, hi975 = (ci975 or {}).get(metric, (lo - 0.001, hi + 0.001))
        rows.append(dict(scope='equal_fold', candidate='v5', baseline='HGL', metric=metric, difference=point, ci_lower=lo,
                         ci_upper=hi, status='resolved', ratio=point, ratio_ci_lower=lo, ratio_ci_upper=hi,
                         **{'ci97.5_lower': lo975, 'ci97.5_upper': hi975}))
    for fold in FOLDS:
        for metric in ('MAE', 'WIS'):
            lo, hi = fold_rows.get((fold, metric), (-1.0, 1.0))
            rows.append(dict(scope=fold, candidate='v5', baseline='HGL', metric=metric, difference=(lo + hi) / 2,
                             ci_lower=lo, ci_upper=hi, status='resolved', ratio=np.nan, ratio_ci_lower=np.nan,
                             ratio_ci_upper=np.nan, **{'ci97.5_lower': lo, 'ci97.5_upper': hi}))
    return pd.DataFrame(rows)


def _criteria(met=True):
    return pd.DataFrame([dict(policy='v5', criterion=c, metric='m', scope='s', actual=0.0, lower_limit=None, upper_limit=None,
                              status='met' if (met or c != 3) else 'not_met', passed=bool(met or c != 3)) for c in range(1, 7)])


SCORES = {'HGL': {'S_MAE': 0.53, 'S_WIS': 0.50}}
BIG = (-0.01, -0.02, -0.004)      # a 1.9% / 2% improvement: clears the 0.5% practical size


def test_adoption_requires_all_five_conditions_at_the_975_level_and_names_the_first_unmet():
    good = _uncertainty(BIG, (-0.01, -0.02, -0.004), {})
    out = S.adoption(good, _criteria(), SCORES, keys_complete=True, guards_reported=True)
    assert out['adopted'] and out['first_unmet_condition'] is None
    # condition 1 reads the 97.5% interval, not the 95% one
    wide = _uncertainty(BIG, (-0.01, -0.02, -0.004), {}, ci975={'MAE': (-0.03, 0.001), 'WIS': (-0.03, -0.001)})
    out = S.adoption(wide, _criteria(), SCORES, keys_complete=True, guards_reported=True)
    assert not out['adopted'] and out['first_unmet_condition'] == 1
    edge = _uncertainty(BIG, (-0.01, -0.02, -0.004), {}, ci975={'MAE': (-0.03, 0.0), 'WIS': (-0.03, 0.0)})
    assert S.adoption(edge, _criteria(), SCORES, keys_complete=True, guards_reported=True)['first_unmet_condition'] == 1
    edge = _uncertainty(BIG, (-0.01, -0.02, -0.004), {}, ci975={'MAE': (-0.03, 0.0), 'WIS': (-0.03, -1e-12)})
    assert S.adoption(edge, _criteria(), SCORES, keys_complete=True, guards_reported=True)['adopted']
    # condition 2: a section-8 failure
    out = S.adoption(good, _criteria(met=False), SCORES, keys_complete=True, guards_reported=True)
    assert out['first_unmet_condition'] == 2
    # condition 3: incomplete keys or unreported guards
    assert S.adoption(good, _criteria(), SCORES, keys_complete=False, guards_reported=True)['first_unmet_condition'] == 3
    assert S.adoption(good, _criteria(), SCORES, keys_complete=True, guards_reported=False)['first_unmet_condition'] == 3
    # condition 4: one fold decisively worse in WIS
    worse = _uncertainty(BIG, (-0.01, -0.02, -0.004), {('fold_3', 'WIS'): (0.1, 2.0)})
    assert S.adoption(worse, _criteria(), SCORES, keys_complete=True, guards_reported=True)['first_unmet_condition'] == 4
    # condition 5: a resolved but too small improvement (0.1% of S_MAE(v4))
    small = _uncertainty((-0.0005, -0.0009, -0.0001), (-0.01, -0.02, -0.004), {},
                         ci975={'MAE': (-0.001, -0.00005), 'WIS': (-0.03, -0.001)})
    out = S.adoption(small, _criteria(), SCORES, keys_complete=True, guards_reported=True)
    assert out['first_unmet_condition'] == 5 and not out['adopted']
    # S2's trigger: condition 3's Integration clause alone never counts as not adopted; the others do
    assert not S.adoption(good, _criteria(), SCORES, keys_complete=True, guards_reported=True)['counts_as_not_adopted_for_s2']
    assert S.adoption(small, _criteria(), SCORES, keys_complete=True, guards_reported=True)['counts_as_not_adopted_for_s2']


def test_the_975_interval_uses_the_125_and_9875_percentiles_of_the_same_draws():
    rng = np.random.default_rng(5)
    d = rng.normal(0, 1, 2000)
    unc = pd.DataFrame([dict(scope='equal_fold', candidate='v5', baseline='HGL', metric='MAE', difference=0.0,
                             ci_lower=np.quantile(d, .025), ci_upper=np.quantile(d, .975), status='resolved')])
    draws = pd.DataFrame({'scope': 'equal_fold', 'candidate': 'v5', 'baseline': 'HGL', 'metric': 'MAE',
                          'replicate': np.arange(2000), 'difference': d, 'ratio': np.nan})
    out = S.with_level(unc, draws)
    lo, hi = np.quantile(d, [0.0125, 0.9875], method='linear')
    assert out.loc[0, 'ci97.5_lower'] == lo and out.loc[0, 'ci97.5_upper'] == hi
    assert out.loc[0, 'ci97.5_lower'] < out.loc[0, 'ci_lower'] and out.loc[0, 'ci97.5_upper'] > out.loc[0, 'ci_upper']


def test_the_contrast_table_is_23_8s():
    pairs = {(c, b) for c, b, _ in S.contrasts()}
    assert {('v5', 'HGL'), ('v5', 'HG'), ('D2', 'L'), ('D2', 'HG'), ('D2', 'HGL'), ('D2', 'D'), ('v3+D2', 'HGL'),
            ('v3+D', 'HGL'), ('v3+D2', 'HG'), ('v5', 'v3+D2')} <= pairs
    assert S.ELIGIBLE == ('v5',) and 'D2' not in S.ELIGIBLE and 'v3+D2' not in S.ELIGIBLE
