"""CP-23 composites and the mechanical `cp23-adoption` rule (§21.2, §21.6, §21.7), on synthetic fixtures."""
import numpy as np
import pandas as pd
import pytest

from cp22.scoring import FOLDS
from cp23 import scoring as S
from cp23.execution import COMPOSITE_TOLERANCE, composite_gap, v3d_central, v5_central


def test_v5_and_v3d_composites_are_the_fixed_one_third_member():
    rng = np.random.default_rng(1)
    a1, b2, ln, lr, d = (rng.normal(80, 30, 500) for _ in range(5))
    c_v4 = a1 / 3 + b2 / 3 + ln / 6 + lr / 6
    c_hg = a1 / 2 + b2 / 2
    v5 = v5_central(c_v4, d)
    v3d = v3d_central(a1, b2, d)
    m = {'HGL': c_v4, 'HG': c_hg, 'D': d}
    assert composite_gap('v5', v5, m) <= COMPOSITE_TOLERANCE
    assert composite_gap('v3+D', v3d, m) <= COMPOSITE_TOLERANCE
    assert np.array_equal(v3d, a1 / 3 + b2 / 3 + d / 3)
    # positive control: a different member weight is caught
    assert composite_gap('v5', c_v4 * 0.6 + d * 0.4, m) > COMPOSITE_TOLERANCE
    with pytest.raises(ValueError):
        v5_central(c_v4, np.append(d[:-1], np.nan))


def _uncertainty(eq_mae, eq_wis, fold_rows):
    rows = []
    for metric, (point, lo, hi) in (('MAE', eq_mae), ('WIS', eq_wis)):
        rows.append(dict(scope='equal_fold', candidate='v5', baseline='HGL', metric=metric, difference=point, ci_lower=lo,
                         ci_upper=hi, status='resolved', ratio=point, ratio_ci_lower=lo, ratio_ci_upper=hi))
    for fold in FOLDS:
        for metric in ('MAE', 'WIS'):
            lo, hi = fold_rows.get((fold, metric), (-1.0, 1.0))
            rows.append(dict(scope=fold, candidate='v5', baseline='HGL', metric=metric, difference=(lo + hi) / 2,
                             ci_lower=lo, ci_upper=hi, status='resolved', ratio=np.nan, ratio_ci_lower=np.nan,
                             ratio_ci_upper=np.nan))
    return pd.DataFrame(rows)


def _criteria(met=True):
    return pd.DataFrame([dict(policy='v5', criterion=c, metric='m', scope='s', actual=0.0, lower_limit=None, upper_limit=None,
                              status='met' if (met or c != 3) else 'not_met', passed=bool(met or c != 3)) for c in range(1, 7)])


def test_adoption_requires_all_four_conditions_and_names_the_first_unmet():
    good = _uncertainty((-0.01, -0.02, -0.001), (-0.01, -0.02, -0.002), {})
    out = S.adoption(good, _criteria(), keys_complete=True)
    assert out['adopted'] and out['first_unmet_condition'] is None
    # condition 1: dS_MAE upper endpoint above zero is not a joint improvement
    mixed = _uncertainty((-0.01, -0.02, 0.001), (-0.01, -0.02, -0.002), {})
    out = S.adoption(mixed, _criteria(), keys_complete=True)
    assert not out['adopted'] and out['first_unmet_condition'] == 1
    # the MAE endpoint may equal zero; the WIS endpoint must be strictly below zero
    edge = _uncertainty((-0.01, -0.02, 0.0), (-0.01, -0.02, 0.0), {})
    assert S.adoption(edge, _criteria(), keys_complete=True)['first_unmet_condition'] == 1
    edge = _uncertainty((-0.01, -0.02, 0.0), (-0.01, -0.02, -1e-12), {})
    assert S.adoption(edge, _criteria(), keys_complete=True)['adopted']
    # condition 2: a section-8 failure
    assert S.adoption(good, _criteria(met=False), keys_complete=True)['first_unmet_condition'] == 2
    # condition 3: incomplete keys
    assert S.adoption(good, _criteria(), keys_complete=False)['first_unmet_condition'] == 3
    # condition 4: one fold decisively worse in WIS
    worse = _uncertainty((-0.01, -0.02, -0.001), (-0.01, -0.02, -0.002), {('fold_4', 'WIS'): (0.1, 0.5)})
    out = S.adoption(worse, _criteria(), keys_complete=True)
    assert out['first_unmet_condition'] == 4 and out['conditions'][4]['values']['folds_decisively_worse'][0]['scope'] == 'fold_4'
    # a lower endpoint exactly at zero is not "entirely above zero"
    touching = _uncertainty((-0.01, -0.02, -0.001), (-0.01, -0.02, -0.002), {('fold_1', 'MAE'): (0.0, 0.5)})
    assert S.adoption(touching, _criteria(), keys_complete=True)['adopted']


def test_only_v5_is_eligible_and_the_contrasts_are_section_21_5s():
    assert S.ELIGIBLE == ('v5',) and S.RULES['cp23-adoption']['candidate'] == 'v5'
    pairs = {(c, b) for c, b, _ in S.contrasts()}
    assert pairs == {('v5', 'HGL'), ('v5', 'HG'), ('D', 'HGL'), ('D', 'HG'), ('v3+D', 'HG'), ('HGL', 'HG'), ('v5', 'v3+D')}
    assert S.SAVED[0] == 'B0'  # the bootstrap normalises by the first policy
