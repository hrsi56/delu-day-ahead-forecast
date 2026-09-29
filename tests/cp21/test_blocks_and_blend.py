"""CP-21 §17.3/§17.7: block membership and DST, the §15.3 weather imputer, the HGL blend and the
single-central H-layer identity. Synthetic fixtures only; no research data, no fit."""
from __future__ import annotations

from datetime import date

import numpy as np
import pandas as pd
import pytest

from cp15.data import day_hours
from cp15.models import prepared_linear
from cp16.residuals import SharedResidualState
from cp21 import lgbm
from cp21.execution import _twice
from cp21.scoring import BLOCK_OF


def test_blocks_are_exhaustive_disjoint_and_match_the_plan():
    hours = sorted(h for block in lgbm.BLOCKS.values() for h in block)
    assert hours == list(range(24)), 'every local hour belongs to exactly one block'
    assert lgbm.BLOCKS['night'] == (22, 23, 0, 1, 2, 3, 4, 5)
    assert lgbm.BLOCKS['solar'] == tuple(range(10, 17))
    assert lgbm.BLOCKS['shoulder'] == (6, 7, 8, 9, 17, 18, 19, 20, 21)
    assert [len(lgbm.BLOCKS[b]) for b in ('night', 'solar', 'shoulder')] == [8, 7, 9]
    # the scorer's block labels are the same map
    assert all(BLOCK_OF[h] == lgbm.block_of(h) for h in range(24))
    with pytest.raises(ValueError):
        lgbm.block_of(24)  # positive control: an hour outside every block is refused


def test_minimum_rows_are_365_times_block_hours():
    assert lgbm.MIN_TRAIN_ROWS == {'pooled': 8760, 'night': 2920, 'solar': 2555, 'shoulder': 3285}


@pytest.mark.parametrize('day, n, repeated', [(date(2021, 10, 31), 25, 2), (date(2022, 3, 27), 23, None),
                                              (date(2022, 6, 1), 24, None)])
def test_dst_days_keep_canonical_identity_and_block_membership(day, n, repeated):
    index = day_hours(day)
    local = index.tz_convert('Europe/Berlin').hour
    assert len(index) == n and not index.has_duplicates
    counts = pd.Series(local).value_counts()
    if repeated is not None:
        # both canonical local-hour-2 observations enter the night block
        assert counts[2] == repeated and lgbm.block_of(2) == 'night'
    if n == 23:
        assert 2 not in set(local)  # the missing spring hour stays absent
    blocks = pd.Series([lgbm.block_of(h) for h in local]).value_counts().to_dict()
    assert sum(blocks.values()) == n


def test_weather_imputer_is_the_section_15_3_rule_without_the_scaler():
    rng = np.random.default_rng(1)
    train = rng.normal(size=(50, 3))
    train[:5, 0] = np.nan
    train[:, 2] = np.nan  # all-null column -> 0
    other = rng.normal(size=(7, 3))
    other[0] = np.nan
    imputer = lgbm.WeatherImputer(train)
    ours = imputer.transform(other)
    # CP-15's prepared_linear applies the same imputation/indicators, then a StandardScaler.
    _, theirs, fill, scaler = prepared_linear(train, other)
    np.testing.assert_array_equal(imputer.fill, fill)
    np.testing.assert_allclose(scaler.inverse_transform(theirs), ours, rtol=0, atol=1e-12)
    assert imputer.fill[2] == 0.0 and ours[0, 3:].tolist() == [1.0, 1.0, 1.0]
    assert np.isfinite(ours).all(), 'LightGBM never sees a missing weather value'


def test_grid_is_ordered_capped_and_ends_at_the_inherited_setting():
    assert len(lgbm.GRID) <= 4
    capacity = [c['n_estimators'] * c['num_leaves'] for c in lgbm.GRID]
    assert capacity == sorted(capacity) and len(set(capacity)) == len(capacity)
    assert (lgbm.GRID[-1]['n_estimators'], lgbm.GRID[-1]['num_leaves']) == (600, 63)
    for c in lgbm.GRID[:-1]:
        assert c['n_estimators'] <= 600 and c['num_leaves'] <= 63 and (c['n_estimators'], c['num_leaves']) != (600, 63)


def test_hgl_blend_is_two_thirds_hg_plus_one_third_lightgbm_mean():
    rng = np.random.default_rng(7)
    a1, b2, ln, lr = (rng.normal(80, 40, 24) for _ in range(4))
    c = lgbm.hgl_central(a1, b2, ln, lr)
    hg = lgbm.hg_central(a1, b2)
    np.testing.assert_allclose(c - (2 / 3) * hg, (1 / 3) * (ln + lr) / 2, rtol=0, atol=1e-9)
    assert np.array_equal(c, a1 / 3 + b2 / 3 + ln / 6 + lr / 6), 'the frozen left-to-right float expression'
    # HGL differs from HG only by the added member: with L-N = L-R = c_HG, HGL equals HG
    np.testing.assert_allclose(lgbm.hgl_central(a1, b2, hg, hg), hg, rtol=0, atol=1e-9)
    with pytest.raises(ValueError):
        lgbm.hgl_central(a1, b2, ln[:23], lr)
    bad = ln.copy()
    bad[3] = np.nan
    with pytest.raises(ValueError):
        lgbm.hgl_central(a1, b2, bad, lr)


def test_single_central_h_layer_path_is_bitwise_the_two_component_path():
    """HG's A1/B2 pair and its central passed twice produce identical states and quantiles."""
    rng = np.random.default_rng(3)
    start = date(2022, 1, 1)
    days = list(pd.date_range(start, periods=40).date)
    pair, single = SharedResidualState(), SharedResidualState()
    truth_values = {}

    def truth(index):
        return np.array([truth_values[t] for t in index])

    for d in days:
        index = day_hours(d)
        a1, b2 = rng.normal(60, 20, len(index)), rng.normal(60, 20, len(index))
        scale = rng.uniform(1, 30, len(index))
        for t, v in zip(index, rng.normal(60, 25, len(index))):
            truth_values[t] = v
        pair.release(d, truth)
        single.release(d, truth)
        c = _twice(lgbm.hg_central(a1, b2))
        if d >= days[31]:
            qa, ma = pair.predict(d, index, a1, b2, scale)
            qb, mb = single.predict(d, index, c, c, scale)
            assert np.array_equal(qa['V2-H'], qb['V2-H']) and ma == mb
        pair.issue(d, index, a1, b2, scale)
        single.issue(d, index, c, c, scale)
    assert pair.dumps() == single.dumps()


def test_twice_refuses_a_vector_that_is_not_its_own_half_sum():
    assert np.array_equal(_twice(np.array([1.0, -3.5, 1e300])), np.array([1.0, -3.5, 1e300]))
    with pytest.raises(ValueError):
        _twice(np.array([5e-324]))  # the subnormal minimum halves to zero: identity fails, refused
