"""PyTorch correctness reference for DDNN (capstone v21-r10 §21.3, §18.3).

Explicitly invoked only, by the ``reference-checks`` job (``cp23.reference``). The file name does not
match ``test_*.py``, so the default suite never collects it. PyTorch is imported at module level with
no skip logic, so a missing PyTorch fails collection; it is never a skip. The tolerances are
``cp23.reference.REFERENCE_TOLERANCES``, frozen before the first comparison run. The inputs are fixed
synthetic arrays and seeds, and nothing here touches research data. CPU and float64 only, with one
thread.
"""
import json
import math
import os
from pathlib import Path

import numpy as np
import pytest
import torch
import torch.nn.functional as F

from cp23 import ddnn as D
from cp23.reference import REFERENCE_TOLERANCES as T, TRAINING_LOOP_EPOCHS, TRAJECTORY_STEPS

torch.set_default_dtype(torch.float64)
torch.set_num_threads(1)
ERRORS: dict = {}
CONFIG_IDS = [c['id'] for c in D.CONFIGS]
PINNED_TORCH = '2.14.1'


@pytest.fixture(scope='module', autouse=True)
def _write_errors():
    yield
    target = os.environ.get('CP23_REFERENCE_ERRORS')
    if target:
        Path(target).parent.mkdir(parents=True, exist_ok=True)
        Path(target).write_text(json.dumps(ERRORS, indent=1, sort_keys=True) + '\n')


def check(name, numpy_value, torch_value, kind):
    a = np.asarray(numpy_value, dtype=float)
    b = torch_value.detach().cpu().numpy() if isinstance(torch_value, torch.Tensor) else np.asarray(torch_value, dtype=float)
    assert a.shape == b.shape, (name, a.shape, b.shape)
    err = np.abs(a - b)
    bound = T[kind]['atol'] + T[kind]['rtol'] * np.abs(b)
    item = ERRORS.setdefault(name, {'kind': kind, 'max_abs_error': 0.0, 'max_error_to_bound': 0.0, 'comparisons': 0})
    item['max_abs_error'] = max(item['max_abs_error'], float(err.max()))
    item['max_error_to_bound'] = max(item['max_error_to_bound'], float((err / bound).max()))
    item['comparisons'] += int(err.size)
    assert np.all(err <= bound), (name, float(err.max()))


def data(n=256, d=9, seed=2026):
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, (n, d))
    y = rng.standard_t(3, n) * 1.5 + 0.3 * x[:, 0]
    return x, y


def config(cid):
    return next(c for c in D.CONFIGS if c['id'] == cid)


def leaf(params):
    return [torch.tensor(p, dtype=torch.float64, requires_grad=True) for p in params]


def torch_forward(tp, x):
    h = x
    for k in range(len(tp) // 2 - 1):
        h = F.elu(h @ tp[2 * k] + tp[2 * k + 1])
    out = h @ tp[-2] + tp[-1]
    return out, (out[:, 0], F.softplus(out[:, 1], threshold=50.0) + D.LAMBDA_FLOOR, out[:, 2],
                 F.softplus(out[:, 3], threshold=50.0) + D.DELTA_FLOOR)


def torch_logpdf(y, xi, lam, gamma, delta):
    """An independent Johnson SU density: Z = gamma + delta * asinh((Y - xi) / lambda) ~ N(0, 1), with
    the Jacobian dZ/dY taken from autograd rather than written out."""
    y = y.detach().clone().requires_grad_(True)
    z = gamma + delta * torch.asinh((y - xi) / lam)
    dz_dy, = torch.autograd.grad(z.sum(), y, create_graph=True)
    return torch.distributions.Normal(0.0, 1.0).log_prob(z) + torch.log(dz_dy)


def torch_loss(tp, x, y, l2):
    _, (xi, lam, gamma, delta) = torch_forward(tp, x)
    return -torch_logpdf(y, xi, lam, gamma, delta).mean() + l2 * sum((w * w).sum() for w in tp[0::2])


def network(cid, d=9, seed=5):
    params = D.init_params(d, config(cid)['hidden'], np.random.Generator(np.random.PCG64(seed)))
    rng = np.random.default_rng(seed + 100)
    for p in params:
        p += rng.normal(0, 0.05, p.shape)  # off the initial point, so every bias carries a gradient
    return params


@pytest.mark.parametrize('cid', CONFIG_IDS)
def test_forward_pass(cid):
    x, _ = data()
    params = network(cid)
    out, _ = D.forward(params, x)
    tout, tparams = torch_forward(leaf(params), torch.tensor(x))
    check(f'forward_outputs/{cid}', out, tout, 'forward_outputs')
    for name, a, b in zip(('xi', 'lambda', 'gamma', 'delta'), D.head(out), tparams):
        check(f'jsu_parameters/{name}/{cid}', a, b, 'jsu_parameters')


@pytest.mark.parametrize('cid', CONFIG_IDS)
def test_log_likelihood_and_its_partials(cid):
    x, y = data()
    out, _ = D.forward(network(cid), x)
    xi, lam, gamma, delta = D.head(out)
    nll, partials = D.jsu_nll_grad(y, xi, lam, gamma, delta)
    tv = [torch.tensor(v, requires_grad=True) for v in (xi, lam, gamma, delta)]
    tnll = -torch_logpdf(torch.tensor(y), *tv)
    check(f'log_likelihood/{cid}', nll, tnll, 'log_likelihood')
    grads = torch.autograd.grad(tnll.sum(), tv)
    for name, a, b in zip(('xi', 'lambda', 'gamma', 'delta'), partials, grads):
        check(f'log_likelihood_partials/{name}/{cid}', a, b, 'log_likelihood_partials')


@pytest.mark.parametrize('cid', CONFIG_IDS)
def test_network_gradients(cid):
    x, y = data()
    params = network(cid)
    l2 = D.TRAINING['l2']
    loss, grads = D.loss_and_grads(params, x, y, l2)
    tp = leaf(params)
    tloss = torch_loss(tp, torch.tensor(x), torch.tensor(y), l2)
    tloss.backward()
    check(f'loss/{cid}', loss, tloss, 'log_likelihood')
    for k, (g, t) in enumerate(zip(grads, tp)):
        check(f'network_gradients/param{k}/{cid}', g, t.grad, 'network_gradients')


@pytest.mark.parametrize('cid', CONFIG_IDS)
def test_quantiles_and_the_cdf_at_each_quantile(cid):
    x, _ = data()
    params = network(cid)
    q = D.jsu_quantiles(params, x)
    _, (xi, lam, gamma, delta) = torch_forward(leaf(params), torch.tensor(x))
    levels = torch.tensor(D.LEVELS)
    tq = xi[:, None] + lam[:, None] * torch.sinh((torch.special.ndtri(levels)[None, :] - gamma[:, None]) / delta[:, None])
    check(f'quantiles/{cid}', q, tq, 'quantiles')
    cdf = torch.distributions.Normal(0.0, 1.0).cdf(gamma[:, None] + delta[:, None] * torch.asinh((torch.tensor(q) - xi[:, None]) / lam[:, None]))
    check(f'cdf_at_quantiles/{cid}', np.broadcast_to(np.array(D.LEVELS), q.shape), cdf, 'cdf_at_quantiles')
    assert np.all(np.diff(q, axis=1) > 0)


@pytest.mark.parametrize('cid', CONFIG_IDS)
def test_adam_trajectory(cid):
    x, y = data()
    s = D.TRAINING
    params = D.init_params(x.shape[1], config(cid)['hidden'], np.random.Generator(np.random.PCG64(9)))
    tp = leaf(params)
    opt = D.Adam(params, s['lr'], s['beta1'], s['beta2'], s['eps'])
    topt = torch.optim.Adam(tp, lr=s['lr'], betas=(s['beta1'], s['beta2']), eps=s['eps'], foreach=False)
    rng = np.random.default_rng(17)
    xt, yt = torch.tensor(x), torch.tensor(y)
    for step in range(TRAJECTORY_STEPS):
        batch = rng.choice(len(y), 64, replace=False)
        _, grads = D.loss_and_grads(params, x[batch], y[batch], s['l2'])
        opt.step(params, grads)
        topt.zero_grad()
        torch_loss(tp, xt[batch], yt[batch], s['l2']).backward()
        topt.step()
        for k, (p, t) in enumerate(zip(params, tp)):
            check(f'adam_trajectory/param{k}/{cid}', p, t, 'adam_trajectory')


@pytest.mark.parametrize('cid', CONFIG_IDS)
def test_training_loop_trajectory(cid):
    """`train_member` for three epochs against a PyTorch replica of the same loop: the same seeded
    initialisation and permutations, torch.optim.Adam, the validation loss and the best-epoch weights."""
    x, y = data(n=320)
    xtr, ytr, xva, yva = x[:256], y[:256], x[256:], y[256:]
    settings = {**D.TRAINING, 'max_epochs': TRAINING_LOOP_EPOCHS, 'patience': 100, 'batch_size': 64}
    member = D.train_member(xtr, ytr, xva, yva, config(cid), 42, settings)
    rng = np.random.Generator(np.random.PCG64(42))
    tp = leaf(D.init_params(xtr.shape[1], config(cid)['hidden'], rng))
    topt = torch.optim.Adam(tp, lr=settings['lr'], betas=(settings['beta1'], settings['beta2']), eps=settings['eps'],
                            foreach=False)
    xt, yt, xv, yv = map(torch.tensor, (xtr, ytr, xva, yva))
    best, best_params, history = math.inf, None, []
    for _ in range(TRAINING_LOOP_EPOCHS):
        order = rng.permutation(len(ytr))
        for start in range(0, len(ytr), settings['batch_size']):
            idx = order[start:start + settings['batch_size']]
            topt.zero_grad()
            torch_loss(tp, xt[idx], yt[idx], settings['l2']).backward()
            topt.step()
        _, (xi, lam, gamma, delta) = torch_forward(tp, xv)
        val = float(-torch_logpdf(yv, xi, lam, gamma, delta).mean())
        history.append(val)
        if val < best:
            best, best_params = val, [t.detach().clone() for t in tp]
    assert member.epochs_run == TRAINING_LOOP_EPOCHS
    check(f'training_loop_trajectory/validation_history/{cid}', member.history, history, 'training_loop_trajectory')
    for k, (p, t) in enumerate(zip(member.params, best_params)):
        check(f'training_loop_trajectory/best_params{k}/{cid}', p, t, 'training_loop_trajectory')


def test_far_tail_likelihood_and_partials():
    rng = np.random.default_rng(3)
    u = np.concatenate([np.logspace(-6, 4, 30), -np.logspace(-6, 4, 30)])
    for delta_value in (D.DELTA_FLOOR, 0.3, 1.0, 3.0):
        xi = rng.normal(0, 1, len(u))
        lam = np.exp(rng.normal(0, 0.5, len(u))) + D.LAMBDA_FLOOR
        gamma = rng.normal(0, 1, len(u))
        delta = np.full(len(u), delta_value)
        y = xi + lam * u
        nll, partials = D.jsu_nll_grad(y, xi, lam, gamma, delta)
        tv = [torch.tensor(v, requires_grad=True) for v in (xi, lam, gamma, delta)]
        tnll = -torch_logpdf(torch.tensor(y), *tv)
        check(f'log_likelihood/far_tail/delta={delta_value}', nll, tnll, 'log_likelihood')
        for name, a, b in zip(('xi', 'lambda', 'gamma', 'delta'), partials, torch.autograd.grad(tnll.sum(), tv)):
            check(f'log_likelihood_partials/far_tail/{name}/delta={delta_value}', a, b, 'log_likelihood_partials')


def test_the_reference_is_the_pinned_cpu_float64_build():
    assert torch.__version__.split('+')[0] == PINNED_TORCH
    lock = (Path(__file__).parent / 'torch-reference' / 'uv.lock').read_text()
    assert f'name = "torch"\nversion = "{PINNED_TORCH}"' in lock
    assert torch.get_default_dtype() == torch.float64 and torch.get_num_threads() == 1
    assert torch.tensor([1.0]).device.type == 'cpu'
