"""DL controls on synthetic streams (capstone v21-r9 §20.7): each negative assertion is paired with
a positive control that can fail."""
from datetime import date, timedelta

import numpy as np
import pandas as pd
import pytest

from cp15.data import day_hours
from cp16.residuals import SharedResidualState
from cp22.dl import (ALPHAS, GAMMA, DynamicResidualState, aci_update, clip_bounds, day_weights, effective_count,
                     weighted_quantile)

START = date(2025, 1, 6)


def stream(days, *, noise=1.0, shift_from=None, shift=0.0, seed=0):
    rng = np.random.default_rng(seed)
    truth, centers = {}, {}
    for i in range(days):
        d = START + timedelta(days=i)
        ix = day_hours(d)
        c = 50 + 10 * np.sin(np.arange(len(ix)) / 3)
        y = c + noise * 5 * rng.standard_normal(len(ix))
        if shift_from is not None and i >= shift_from:
            y = y + shift
        truth.update(zip(ix, y))
        centers[d] = (ix, c)
    series = pd.Series(truth).sort_index()
    return centers, (lambda ix: series.reindex(ix).to_numpy())


def run(state, centers, truth, *, record=None):
    out = {}
    for d in sorted(centers):
        ix, c = centers[d]
        state.release(d, truth)
        ready = len(state._buffer) == 28
        if ready:
            q, meta = state.predict(d, ix, c, c, np.full(len(ix), 5.0))
            out[d] = (q['V2-H'] if 'V2-H' in q else q['DL'], meta)
        state.issue(d, ix, c, c, np.full(len(ix), 5.0))
    return out


def test_h_parity_without_weights_or_aci_is_bitwise():
    centers, truth = stream(80, seed=1)
    h = run(SharedResidualState(), centers, truth)
    d = run(DynamicResidualState('H-PARITY'), centers, truth)
    assert set(h) == set(d) and len(h) > 40
    assert all(np.array_equal(h[k][0], d[k][0]) for k in h)
    # positive control: the weighted variant does differ on the same stream
    w = run(DynamicResidualState('DL'), centers, truth)
    assert any(not np.array_equal(h[k][0], w[k][0]) for k in h)


def test_direction_fixtures_all_miss_lowers_alpha_and_widens_all_hit_raises():
    for a in ALPHAS:
        assert aci_update(a, a, 1.0) < a          # all-miss day lowers alpha_t ...
        assert aci_update(a, a, 0.0) > a          # ... an all-hit day raises it
        assert aci_update(a, a, a) == a           # exactly nominal leaves it
    centers, truth = stream(60, seed=2)
    s = DynamicResidualState('DL')
    run(s, dict(list(centers.items())[:45]), truth)
    widths_before = s.levels()
    # an all-miss day: force the emitted interval to miss every hour
    d = sorted(centers)[45]
    ix, c = centers[d]
    s.release(d, truth)
    q, _ = s.predict(d, ix, c, c, np.full(len(ix), 5.0))
    s.issue(d, ix, c, c, np.full(len(ix), 5.0))
    far = pd.Series(1e6, index=ix)
    truth2 = lambda x: far.reindex(x).fillna(pd.Series(truth(x), index=x)).to_numpy()  # noqa: E731
    alpha95 = s.alpha[0.05]
    s.release(d + timedelta(days=2), truth2)
    last = s.aci_trace[-1]
    assert last['day'] == str(d) and last['status'] == 'updated'
    for a in ALPHAS:  # the all-miss day: every hour outside, every alpha_t lowered (or held at its floor)
        assert last[str(a)]['miss_fraction'] == 1.0
        assert last[str(a)]['alpha_after'] < last[str(a)]['alpha_before'] or last[str(a)]['alpha_after'] == clip_bounds(a)[0]
    assert s.alpha[0.05] <= alpha95
    levels = s.levels()
    assert levels[0] <= widths_before[0] and levels[-1] >= widths_before[-1]  # wider residual levels


def test_clipping_bounds_hold():
    for a in ALPHAS:
        lo, hi = clip_bounds(a)
        x = a
        for _ in range(200):
            x = aci_update(x, a, 1.0)
        assert x == lo
        for _ in range(200):
            x = aci_update(x, a, 0.0)
        assert x == hi
    assert clip_bounds(0.50) == (0.10, 0.9) and clip_bounds(0.05) == (0.01, 0.10) and clip_bounds(0.20) == (0.04, 0.40)
    assert GAMMA == 0.10


def test_weights_sum_to_one_and_two_kernel_reduces_to_dl():
    ages = np.arange(28)[::-1].astype(float)
    for hl, fs in ((7.0, 0.0), (7.0, 1 / 3), (None, 0.0)):
        assert abs(day_weights(ages, hl, fs).sum() - 1) < 1e-12
    assert np.array_equal(day_weights(ages, 7.0, 0.0), day_weights(ages, 7.0))
    assert not np.allclose(day_weights(ages, 7.0, 1 / 3), day_weights(ages, 7.0))
    newest = day_weights(np.arange(28.), 7.0)[0]
    assert abs(newest - 0.1006) < 5e-4                       # about 10% (§20.3)
    assert abs(day_weights(np.arange(28.), 7.0, 1 / 3)[0] - 0.2337) < 5e-4   # about 23%
    assert 9 < effective_count(day_weights(np.arange(28.), 7.0, 1 / 3)) < 11  # about 10 effective days
    with pytest.raises(ValueError):
        day_weights(ages, None, 1 / 3)


def test_weighted_quantile_reduces_to_numpy_linear_with_equal_weights():
    rng = np.random.default_rng(3)
    levels = np.array([.01, .025, .1, .25, .5, .75, .9, .975, .99])
    for n in (2, 3, 24, 28 * 24, 673):
        x = rng.standard_normal(n) * 7
        x[: n // 5] = x[0]  # ties
        got = weighted_quantile(x, np.ones(n), levels)
        assert np.max(np.abs(got - np.quantile(x, levels, method='linear'))) <= 1e-12 * max(1, np.abs(x).max())
        w = rng.uniform(.1, 2, n)
        if n < 3:  # two points sit at 0 and 1 whatever their weights: weights act from n >= 3
            continue
        assert np.max(np.abs(weighted_quantile(x, w, levels) - np.quantile(x, levels, method='linear'))) > 1e-6
    x = rng.standard_normal(50)
    w = rng.uniform(.1, 2, 50)
    assert np.allclose(weighted_quantile(-x, w, 1 - levels), -weighted_quantile(x, w, levels))  # reflection
    assert (np.diff(weighted_quantile(x, w, np.linspace(0, 1, 101))) >= 0).all()             # monotone


def test_release_rule_refuses_d_minus_1_consumes_once_and_no_partial_day():
    centers, truth = stream(40, seed=4)
    s = DynamicResidualState('DL')
    run(s, centers, truth)
    last = max(centers)
    assert last - timedelta(days=1) not in s._consumed and last not in s._consumed   # D-1 refused
    assert last - timedelta(days=2) in s._consumed                                      # D-2 accepted
    n = len(s.trace)
    s.release(last, truth)                       # releasing again consumes nothing new
    assert len(s.trace) == n
    with pytest.raises(ValueError):
        s.issue(last, *centers[last][:1], centers[last][1], centers[last][1], np.full(len(centers[last][0]), 5.))
    # a partial issued day never enters the buffer
    p = DynamicResidualState('DL')
    d0 = START
    ix = day_hours(d0)[:-3]
    p.issue(d0, ix, np.zeros(len(ix)), np.zeros(len(ix)), np.ones(len(ix)) * 5)
    p.release(d0 + timedelta(days=2), truth)
    assert not p._buffer and p.trace[-1]['status'] == 'incomplete_issued_day'


def test_positive_control_level_shift_widens_within_implied_speed():
    shift_day = 50
    centers, truth = stream(80, shift_from=shift_day, shift=40.0, seed=5)
    h = run(SharedResidualState(), centers, truth)
    d = run(DynamicResidualState('DL'), centers, truth)
    days = sorted(centers)
    s0 = days[shift_day]
    # the first shifted error is released at origin s0+2; within one half-life (7 days) of that
    # release the weight on shifted days exceeds a half of the newest days' mass, and ACI has lowered
    # alpha_t by at most 7*gamma*(1-alpha). DL's upper 95% bound must have moved up by then, and
    # by more than the equal-weight H layer's.
    probe = s0 + timedelta(days=2 + 7)
    before = s0 - timedelta(days=1)
    up_dl = d[probe][0][:, 6].mean() - d[before][0][:, 6].mean()
    up_h = h[probe][0][:, 6].mean() - h[before][0][:, 6].mean()
    assert up_dl > 0 and up_dl > up_h
    # negative control: with no shift the same probe does not move materially
    centers0, truth0 = stream(80, seed=5)
    d0 = run(DynamicResidualState('DL'), centers0, truth0)
    assert abs(d0[probe][0][:, 6].mean() - d0[before][0][:, 6].mean()) < up_dl / 3


def test_state_round_trip_and_refusals():
    centers, truth = stream(45, seed=6)
    s = DynamicResidualState('DLF')
    run(s, dict(list(centers.items())[:40]), truth)
    t = DynamicResidualState.from_dict(s.to_dict())
    rest = dict(list(centers.items())[40:])
    a, b = run(s, rest, truth), run(t, rest, truth)
    assert all(np.array_equal(a[k][0], b[k][0]) for k in a) and s.alpha == t.alpha
    bad = s.to_dict()
    bad['params']['half_life'] = 3.0
    with pytest.raises(ValueError):
        DynamicResidualState.from_dict(bad)
    bad = s.to_dict()
    bad['alpha']['0.05'] = 0.5
    with pytest.raises(ValueError):
        DynamicResidualState.from_dict(bad)
