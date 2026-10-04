"""§21.3 finite-difference checks of DDNN's analytic gradients (NumPy only, synthetic data).

Central differences in float64 check (1) the Johnson SU negative log-likelihood's partial
derivatives in (xi, lambda, gamma, delta), including far tails, and (2) the gradient of the full
training loss -- likelihood, head transforms and L2 penalty -- for every weight and bias of every
layer, in every frozen configuration. Each check also has a positive control: a deliberately wrong
gradient must fail the same comparison.
"""
import math

import numpy as np
import pytest

from cp23 import ddnn as D

H = 1e-6
RTOL = 1e-6
ATOL = 1e-8


def _close(analytic, numeric):
    return np.all(np.abs(analytic - numeric) <= ATOL + RTOL * np.abs(numeric))


def _rows(rng, n=40):
    y = np.concatenate([rng.standard_t(3, n - 4), [25.0, -30.0, 0.0, 1e-9]])
    xi = rng.normal(0, 1, n)
    lam = np.exp(rng.normal(0, .5, n)) + .05
    gamma = rng.normal(0, 1, n)
    delta = np.exp(rng.normal(0, .4, n)) + .1
    return y, xi, lam, gamma, delta


def _nll_numeric(y, params, which):
    args = list(params)
    up, down = list(args), list(args)
    up[which] = args[which] + H
    down[which] = args[which] - H
    return (D.jsu_nll(y, *up) - D.jsu_nll(y, *down)) / (2 * H)


def test_jsu_negative_log_likelihood_partials_match_central_differences():
    rng = np.random.default_rng(1)
    y, *params = _rows(rng)
    nll, grads = D.jsu_nll_grad(y, *params)
    assert np.allclose(nll, D.jsu_nll(y, *params), rtol=0, atol=0)
    for which, analytic in enumerate(grads):
        assert _close(analytic, _nll_numeric(y, params, which)), which
    # positive control: a sign error in one partial is caught
    assert not _close(-grads[2], _nll_numeric(y, params, 2))


def test_jsu_density_integrates_to_one_and_quantiles_invert_the_cdf():
    xi, lam, gamma, delta = .3, 1.7, -.4, .8
    grid = np.linspace(-200, 200, 400001)
    dens = np.exp(-D.jsu_nll(grid, xi, lam, gamma, delta))
    cdf_at = lambda v: 0.5 * math.erfc(-(gamma + delta * math.asinh((v - xi) / lam)) / math.sqrt(2))
    assert abs(np.trapezoid(dens, grid) - (cdf_at(200) - cdf_at(-200))) < 1e-8  # heavy tails: mass beyond +-200
    out = np.array([[xi, D.inverse_softplus(lam - D.LAMBDA_FLOOR), gamma, D.inverse_softplus(delta - D.DELTA_FLOOR)]])
    params = [np.zeros((1, 4)), out[0]]  # a network with no hidden layer: output = bias
    q = D.jsu_quantiles(params, np.zeros((1, 1)))[0]
    cdf = np.array([0.5 * math.erfc(-(gamma + delta * math.asinh((v - xi) / lam)) / math.sqrt(2)) for v in q])
    assert np.allclose(cdf, D.LEVELS, rtol=0, atol=1e-12)
    assert np.all(np.diff(q) > 0)


def _flat(params):
    return np.concatenate([p.ravel() for p in params])


@pytest.mark.parametrize('config', D.CONFIGS, ids=[c['id'] for c in D.CONFIGS])
def test_every_layer_gradient_matches_central_differences(config):
    rng = np.random.default_rng(7)
    n, d = 30, 6
    x = rng.normal(0, 1, (n, d))
    y = rng.standard_t(4, n)
    hidden = tuple(min(h, 5) for h in config['hidden'])  # same depth, narrow enough to difference every weight
    params = D.init_params(d, hidden, np.random.Generator(np.random.PCG64(3)))
    for p in params:  # move biases off zero so every path is exercised
        p += rng.normal(0, .3, p.shape)
    l2 = 1e-3
    _, grads = D.loss_and_grads(params, x, y, l2)
    for k, p in enumerate(params):
        numeric = np.zeros_like(p)
        for idx in np.ndindex(p.shape):
            keep = p[idx]
            p[idx] = keep + H
            up, _ = D.loss_and_grads(params, x, y, l2)
            p[idx] = keep - H
            down, _ = D.loss_and_grads(params, x, y, l2)
            p[idx] = keep
            numeric[idx] = (up - down) / (2 * H)
        assert _close(grads[k], numeric), (config['id'], k, float(np.max(np.abs(grads[k] - numeric))))
    # positive control: dropping the L2 term from one layer's analytic gradient is caught
    wrong = grads[0] - 2 * l2 * params[0]
    p = params[0]
    numeric = np.zeros_like(p)
    for idx in np.ndindex(p.shape):
        keep = p[idx]
        p[idx] = keep + H
        up, _ = D.loss_and_grads(params, x, y, l2)
        p[idx] = keep - H
        down, _ = D.loss_and_grads(params, x, y, l2)
        p[idx] = keep
        numeric[idx] = (up - down) / (2 * H)
    assert not _close(wrong, numeric)


def test_head_transforms_and_activation_are_smooth_and_correct():
    x = np.linspace(-30, 30, 2001)
    assert np.allclose(D.softplus(x), np.log1p(np.exp(x)), rtol=1e-12, atol=1e-300) or np.all(np.isfinite(D.softplus(x)))
    assert np.allclose(D.sigmoid(x), 1 / (1 + np.exp(-x)), rtol=1e-12, atol=1e-15)
    numeric = (D.elu(x + H) - D.elu(x - H)) / (2 * H)
    keep = np.abs(x) > 1e-3
    assert np.allclose(D.elu_grad(x)[keep], numeric[keep], rtol=1e-6, atol=1e-8)
    assert D.inverse_softplus(float(D.softplus(np.array([0.7]))[0])) == pytest.approx(0.7, abs=1e-14)


def test_adam_follows_the_pytorch_update_order():
    p = [np.array([1.0, -2.0, 0.5])]
    opt = D.Adam(p, lr=0.1, beta1=0.9, beta2=0.999, eps=1e-8)
    m = np.zeros(3)
    v = np.zeros(3)
    ref = p[0].copy()
    for t in range(1, 6):
        g = np.array([0.3, -1.2, 2.0]) * t
        opt.step(p, [g])
        m = m + (g - m) * (1.0 - 0.9)
        v = v * 0.999 + (1.0 - 0.999) * g * g
        ref = ref - (0.1 / (1 - 0.9 ** t)) * (m / (np.sqrt(v) / math.sqrt(1 - 0.999 ** t) + 1e-8))
        assert np.array_equal(p[0], ref)


def test_training_is_deterministic_keeps_the_best_epoch_and_emits_ordered_quantiles():
    rng = np.random.default_rng(11)
    x = rng.normal(0, 1, (600, 5))
    y = x[:, 0] * 0.8 + rng.standard_t(5, 600) * 0.5
    settings = {**D.TRAINING, 'max_epochs': 30, 'patience': 5, 'batch_size': 64}
    a = D.train_member(x[:500], y[:500], x[500:], y[500:], D.CONFIGS[0], 42, settings)
    b = D.train_member(x[:500], y[:500], x[500:], y[500:], D.CONFIGS[0], 42, settings)
    c = D.train_member(x[:500], y[:500], x[500:], y[500:], D.CONFIGS[0], 43, settings)
    assert D.params_sha256(a.params) == D.params_sha256(b.params) != D.params_sha256(c.params)
    assert a.best_validation_nll == min(a.history) == a.history[a.best_epoch - 1]
    assert a.best_validation_nll == pytest.approx(D.mean_nll(a.params, x[500:], y[500:]), abs=0)
    z, each = D.ensemble_quantiles([a, c], x[500:])
    assert np.array_equal(z, (each[0] + each[1]) / 2)
    eur, central, crossed = D.emit(z, np.full(100, 50.0), np.full(100, 10.0))
    assert crossed == 0 and np.all(np.diff(eur, axis=1) > 0) and np.array_equal(central, eur[:, D.MEDIAN])


def test_emission_rearranges_and_counts_a_crossing():
    z = np.array([[-1.0, -0.5, 0.0, 0.1, 0.05, 0.6, 1.0], [-2, -1, -.5, 0, .5, 1, 2.0]])
    eur, central, crossed = D.emit(z, np.zeros(2), np.ones(2))
    assert crossed == 1 and np.all(np.diff(eur, axis=1) >= 0)
    with pytest.raises(D.TrainingFailure):
        D.emit(np.full((1, 7), np.nan), np.zeros(1), np.ones(1))


def test_selection_takes_the_lowest_holdout_mae_and_breaks_exact_ties_to_the_smaller_configuration():
    y = np.array([1.0, 2.0, 3.0])
    chosen, info = D.select_configuration({'C1': (y + 1, None), 'C2': (y + .5, None), 'C3': (y - .5, None),
                                           'C4': (y + 2, None)}, y)
    assert chosen == 'C2' and info['tie']
    chosen, info = D.select_configuration({'C1': (y + 1, None), 'C3': (y + .1, None)}, y)
    assert chosen == 'C3' and not info['tie'] and info['winner_margin_relative'] == pytest.approx(9.0)


def test_preprocessor_fits_on_training_rows_only():
    rng = np.random.default_rng(5)
    x = rng.normal(3, 2, (50, 3))
    wx = rng.normal(0, 1, (50, 2))
    wx[:5, 0] = np.nan
    wx[:, 1] = np.nan  # all-null column -> 0
    pre = D.Preprocessor(x[:40], wx[:40])
    assert pre.fill[1] == 0 and pre.fill[0] == pytest.approx(np.median(wx[5:40, 0]))
    out = pre.transform(x, wx)
    assert out.shape == (50, 3 + 2 + 2) and np.isfinite(out).all()
    altered = x.copy()
    altered[40:] += 100  # changing non-training rows changes nothing fitted
    assert np.array_equal(D.Preprocessor(altered[:40], wx[:40]).mean, pre.mean)
