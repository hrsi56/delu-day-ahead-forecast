"""Finite-difference checks of DDNN-2's analytic gradients (capstone v21-r11 §23.7).

Synthetic inputs only, no research data. Central differences against `cp24.ddnn2.loss_and_grads` for:
the masked 24-hour Johnson SU loss; the pinball loss through the Johnson SU quantile function; their
mixture; L1 and L2; input dropout with fixed masks; every activation in the space; recency weights;
and every target transform with its inverse.
"""
import math

import numpy as np
import pytest

from cp24 import ddnn2 as M

ACTS = M.ACTIVATIONS


def problem(seed=7, n=12, p=6, hidden=(5, 4)):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(n, p))
    params = M.init_params(p, hidden, rng)
    for k in range(len(params)):           # move away from the initial symmetric point
        params[k] = params[k] + rng.normal(scale=0.1, size=params[k].shape)
    t = rng.standard_t(4, size=(n, M.SLOTS)) * 0.8
    mask = rng.random((n, M.SLOTS)) > 0.1
    mask[0, 2] = False                     # a 23-hour day's missing slot
    weight = rng.uniform(0.2, 2.0, n)
    weight /= weight.mean()
    return x, params, t, mask, weight


def numeric(f, params, k, idx, eps=1e-6):
    p0 = [p.copy() for p in params]
    p1 = [p.copy() for p in params]
    p0[k][idx] -= eps
    p1[k][idx] += eps
    return (f(p1) - f(p0)) / (2 * eps)


def check(x, params, t, mask, weight, act, kappa, l1=0.0, l2=0.0, dm=None, tol=1e-5, samples=6, seed=0):
    def f(ps):
        return M.loss_and_grads(ps, x, t, mask, weight, act, kappa, l1, l2, dm)[0]
    _, grads = M.loss_and_grads(params, x, t, mask, weight, act, kappa, l1, l2, dm)
    rng = np.random.default_rng(seed)
    worst = 0.0
    for k, p in enumerate(params):
        for _ in range(samples):
            idx = tuple(int(rng.integers(0, s)) for s in p.shape)
            num = numeric(f, params, k, idx)
            ana = grads[k][idx]
            err = abs(num - ana) / max(1.0, abs(num), abs(ana))
            worst = max(worst, err)
            assert err < tol, (act, kappa, k, idx, num, ana)
    return worst


@pytest.mark.parametrize('act', ACTS)
def test_masked_jsu_nll_gradient_every_activation(act):
    x, params, t, mask, weight = problem()
    check(x, params, t, mask, weight, act, kappa=1.0)


@pytest.mark.parametrize('act', ACTS)
def test_pinball_through_the_jsu_quantile_function(act):
    x, params, t, mask, weight = problem(seed=11)
    check(x, params, t, mask, weight, act, kappa=0.0, tol=1e-4)


@pytest.mark.parametrize('act', ACTS)
def test_mixture_with_l1_l2_and_fixed_dropout_masks(act):
    x, params, t, mask, weight = problem(seed=13, hidden=(6,))
    rng = np.random.default_rng(3)
    rate = 0.3
    dm = (rng.random(x.shape) >= rate) / (1 - rate)
    check(x, params, t, mask, weight, act, kappa=0.5, l1=1e-3, l2=1e-2, dm=dm, tol=1e-4)


def test_penalties_alone_have_the_closed_form_gradient():
    x, params, t, mask, weight = problem(seed=5)
    _, g0 = M.loss_and_grads(params, x, t, mask, weight, 'elu', 1.0, 0.0, 0.0)
    _, g1 = M.loss_and_grads(params, x, t, mask, weight, 'elu', 1.0, 0.01, 0.02)
    for k in range(0, len(params), 2):
        assert np.allclose(g1[k] - g0[k], 0.01 * np.sign(params[k]) + 0.04 * params[k], rtol=0, atol=1e-12)
    for k in range(1, len(params), 2):
        assert np.array_equal(g1[k], g0[k])  # biases unpenalised


def test_absent_slots_and_zero_weights_never_enter():
    x, params, t, mask, weight = problem(seed=17)
    loss, grads = M.loss_and_grads(params, x, t, mask, weight, 'tanh', 0.5, 0.0, 0.0)
    t2 = t.copy()
    t2[~mask] = 1e6                       # anything in an absent slot
    loss2, grads2 = M.loss_and_grads(params, x, t2, mask, weight, 'tanh', 0.5, 0.0, 0.0)
    assert loss == loss2 and all(np.array_equal(a, b) for a, b in zip(grads, grads2))
    w0 = weight.copy()
    w0[3] = 0.0
    t3 = t.copy()
    t3[3] += 50.0
    l_a, g_a = M.loss_and_grads(params, x, t, mask, w0, 'tanh', 0.5, 0.0, 0.0)
    l_b, g_b = M.loss_and_grads(params, x, t3, mask, w0, 'tanh', 0.5, 0.0, 0.0)
    assert l_a == l_b and all(np.array_equal(a, b) for a, b in zip(g_a, g_b))
    # positive control: a present slot's target moves the loss
    t4 = t.copy()
    r, s = np.argwhere(mask)[0]
    t4[r, s] += 1.0
    assert M.loss_and_grads(params, x, t4, mask, weight, 'tanh', 0.5, 0.0, 0.0)[0] != loss


def test_pinball_matches_its_definition_and_the_quantiles_are_increasing():
    rng = np.random.default_rng(1)
    xi, lam, gamma = rng.normal(size=(4, 24)), rng.uniform(0.2, 2, (4, 24)), rng.normal(size=(4, 24))
    delta = rng.uniform(0.3, 3, (4, 24))
    t = rng.normal(size=(4, 24))
    loss, _ = M.pinball_grad(t, xi, lam, gamma, delta)
    q = M.jsu_quantiles(xi, lam, gamma, delta, M.Z_GRID)
    for j, tau in enumerate(M.GRID):
        u = t - q[..., j]
        assert np.allclose(loss[..., j], np.where(u >= 0, tau * u, (tau - 1) * u), rtol=0, atol=1e-14)
    assert (np.diff(q, axis=-1) > 0).all()
    assert set(M.LEVELS) <= set(M.GRID) and len(M.GRID) == 19


@pytest.mark.parametrize('form', M.TRANSFORMS)
def test_every_target_transform_and_its_inverse(form):
    z = np.linspace(-40, 40, 2001)
    t = M.forward_transform(form, z)
    assert np.allclose(M.inverse_transform(form, t), z, rtol=1e-12, atol=1e-12)
    eps = 1e-6
    num = (M.forward_transform(form, z + eps) - M.forward_transform(form, z - eps)) / (2 * eps)
    ana = 1 / np.sqrt(1 + z * z) if form.startswith('asinh') else np.ones_like(z)
    assert np.allclose(num, ana, rtol=1e-6, atol=1e-9)
    # quantile equivariance: the inverse of a quantile in t is the quantile in z (monotone map)
    xi, lam, gamma, delta = (np.array([[0.1]]), np.array([[0.7]]), np.array([[0.2]]), np.array([[1.3]]))
    qt = M.jsu_quantiles(xi, lam, gamma, delta)
    qz = M.inverse_transform(form, qt)
    assert (np.diff(qz, axis=-1) > 0).all()


def test_cap_clips_and_counts_every_activation():
    rng = np.random.default_rng(2)
    params = M.init_params(3, (4,), rng)
    params[-1][3 * 24:] = -30.0             # delta at its floor: very wide tails
    x = rng.normal(size=(5, 3))
    zq, active = M.member_quantiles_z(params, x, 'elu', 'z-s4', cap=2.0)
    assert np.abs(zq).max() <= 2.0 and active.sum() > 0
    assert np.array_equal(active, np.abs(M.inverse_transform('z-s4', M.jsu_quantiles(*M.head(M.forward(params, x, 'elu')[0])))) > 2.0)


def test_ensemble_median_is_the_mean_of_the_two_middle_values_and_never_crosses():
    rng = np.random.default_rng(4)
    q = np.sort(rng.normal(size=(8, 3, 24, 7)), axis=-1)
    med, crossed = M.ensemble_median(q)
    s = np.sort(q, axis=0)
    assert np.allclose(med, (s[3] + s[4]) / 2, rtol=0, atol=0)
    assert crossed == 0 and (np.diff(med, axis=-1) >= 0).all()


def test_training_is_deterministic_and_keeps_the_best_epoch():
    rng = np.random.default_rng(9)
    n, p = 60, 5
    x = rng.normal(size=(n, p))
    t = rng.normal(size=(n, 24))
    mask = np.ones((n, 24), bool)
    xh = rng.normal(size=(10, p))
    yh = rng.normal(size=(10, 24)) * 5 + 50
    mh = np.ones((10, 24), bool)
    cfg = {'id': 'T', 'hidden': (8,), 'activation': 'softplus', 'lr': 1e-2, 'batch_size': 32, 'kappa': 0.5,
           'l1': 1e-5, 'l2': 1e-4, 'input_dropout': 0.2, 'transform': 'asinh-mad'}
    a = M.train(x, t, mask, np.ones(n), xh, yh, mh, np.full(10, 50.0), np.full(10, 5.0), cfg, 3, 10.0, max_epochs=40,
                patience=5, warm_epochs=3)
    b = M.train(x, t, mask, np.ones(n), xh, yh, mh, np.full(10, 50.0), np.full(10, 5.0), cfg, 3, 10.0, max_epochs=40,
                patience=5, warm_epochs=3)
    assert M.params_sha256(a.params) == M.params_sha256(b.params) and a.best_epoch == b.best_epoch
    assert a.best_epoch > 3 and math.isclose(a.best_metric, min(a.history))
    assert len(a.history) == a.epochs_run - 3
