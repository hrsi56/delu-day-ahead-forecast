"""PyTorch correctness reference for DDNN-2 (capstone v21-r11 §23.7; §18.3, §21.3).

Explicitly invoked only, by the ``reference-checks`` job (``cp24.reference``). The file name does not
match ``test_*.py``, so the default suite never collects it. PyTorch is imported at module level with no
skip logic, so a missing PyTorch fails collection; it is never a skip. The tolerances are
``cp24.reference.REFERENCE_TOLERANCES``, frozen before the first comparison run. The inputs are fixed
synthetic arrays and seeds; nothing here touches research data. CPU and float64 only, one thread.
"""
import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pytest
import torch
import torch.nn.functional as F

from cp24 import ddnn2 as M
from cp24.reference import (LOCK_FILE, LOCK_SHA256, PINNED_TORCH, REFERENCE_TOLERANCES as T, TRAINING_LOOP_EPOCHS,
                            TRAJECTORY_STEPS)

torch.set_default_dtype(torch.float64)
torch.set_num_threads(1)
ERRORS: dict = {}
ROOT = Path(__file__).resolve().parents[2]
S = M.SLOTS


@pytest.fixture(scope='module', autouse=True)
def _write_errors():
    yield
    target = os.environ.get('CP24_REFERENCE_ERRORS')
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


def problem(seed=2026, n=40, p=9, hidden=(11, 7)):
    rng = np.random.default_rng(seed)
    x = rng.normal(0, 1, (n, p))
    t = rng.standard_t(3, (n, S)) * 0.9 + 0.3 * x[:, :1]
    mask = rng.random((n, S)) > 0.08
    mask[0, 2] = False
    weight = rng.uniform(0.3, 2.0, n)
    weight /= weight.mean()
    params = M.init_params(p, hidden, rng)
    for k in range(len(params)):
        params[k] = params[k] + rng.normal(scale=0.15, size=params[k].shape)
    dm = (rng.random(x.shape) >= 0.25) / 0.75
    return x, t, mask, weight, params, dm


def leaf(params):
    return [torch.tensor(p, dtype=torch.float64, requires_grad=True) for p in params]


def t_act(name, a):
    return {'elu': F.elu, 'relu': F.relu, 'tanh': torch.tanh,
            'softplus': lambda v: F.softplus(v, threshold=50.0)}[name](a)


def t_forward(tp, x, act, dm=None):
    h = x if dm is None else x * dm
    for k in range(len(tp) // 2 - 1):
        h = t_act(act, h @ tp[2 * k] + tp[2 * k + 1])
    out = h @ tp[-2] + tp[-1]
    return out, (out[:, 0:S], F.softplus(out[:, S:2 * S], threshold=50.0) + M.LAMBDA_FLOOR, out[:, 2 * S:3 * S],
                 F.softplus(out[:, 3 * S:4 * S], threshold=50.0) + M.DELTA_FLOOR)


def t_nll(t, xi, lam, gamma, delta):
    """An independent Johnson SU density: Z = gamma + delta*asinh((Y - xi)/lambda) ~ N(0,1), with dZ/dY
    from autograd rather than written out."""
    y = t.detach().clone().requires_grad_(True)
    z = gamma + delta * torch.asinh((y - xi) / lam)
    dz = torch.autograd.grad(z.sum(), y, create_graph=True)[0]
    return 0.5 * z * z + 0.5 * np.log(2 * np.pi) - torch.log(dz)


def t_pinball(t, xi, lam, gamma, delta):
    zl = torch.special.ndtri(torch.tensor(M.GRID))
    tau = torch.tensor(M.GRID)
    q = xi[..., None] + lam[..., None] * torch.sinh((zl - gamma[..., None]) / delta[..., None])
    u = t[..., None] - q
    return torch.maximum(tau * u, (tau - 1.0) * u)


def t_loss(tp, x, t, mask, weight, act, kappa, l1, l2, dm):
    _, (xi, lam, gamma, delta) = t_forward(tp, torch.tensor(x), act, None if dm is None else torch.tensor(dm))
    m = torch.tensor(mask.astype(float)) * torch.tensor(weight)[:, None]
    count = float(mask.sum())
    tt = torch.where(torch.tensor(mask), torch.tensor(t), xi.detach())
    loss = torch.zeros(())
    if kappa > 0:
        loss = loss + kappa * (m * t_nll(tt, xi, lam, gamma, delta)).sum() / count
    if kappa < 1:
        loss = loss + (1 - kappa) * (m[..., None] * t_pinball(tt, xi, lam, gamma, delta)).sum() / (count * len(M.GRID))
    for w in tp[0::2]:
        if l1:
            loss = loss + l1 * w.abs().sum()
        if l2:
            loss = loss + l2 * (w * w).sum()
    return loss


@pytest.mark.parametrize('act', M.ACTIVATIONS)
@pytest.mark.parametrize('hidden', [(13,), (11, 7)])
def test_forward_pass_and_jsu_parameters(act, hidden):
    x, t, mask, weight, params, dm = problem(hidden=hidden)
    out, _ = M.forward(params, x, act, dm)
    tout, tparams = t_forward(leaf(params), torch.tensor(x), act, torch.tensor(dm))
    check(f'forward_{act}_{len(hidden)}', out, tout, 'forward_outputs')
    for name, a, b in zip(('xi', 'lambda', 'gamma', 'delta'), M.head(out), tparams):
        check(f'jsu_{name}_{act}_{len(hidden)}', a, b, 'jsu_parameters')


def _compare_loss(name, x, t, mask, weight, params, act, kappa, l1, l2, dm, loss_kind):
    loss, grads = M.loss_and_grads(params, x, t, mask, weight, act, kappa, l1, l2, dm)
    tp = leaf(params)
    tl = t_loss(tp, x, t, mask, weight, act, kappa, l1, l2, dm)
    tl.backward()
    check(f'{name}_loss', loss, tl, loss_kind)
    for k, (g, p) in enumerate(zip(grads, tp)):
        check(f'{name}_grad_{k}', g, p.grad, 'loss_gradients')


@pytest.mark.parametrize('act', M.ACTIVATIONS)
def test_masked_weighted_jsu_nll_and_its_gradient(act):
    x, t, mask, weight, params, _ = problem(seed=11)
    _compare_loss(f'nll_{act}', x, t, mask, weight, params, act, 1.0, 0.0, 0.0, None, 'nll_loss')


@pytest.mark.parametrize('act', M.ACTIVATIONS)
def test_pinball_through_the_jsu_quantile_function_and_its_gradient(act):
    x, t, mask, weight, params, _ = problem(seed=12)
    _compare_loss(f'pinball_{act}', x, t, mask, weight, params, act, 0.0, 0.0, 0.0, None, 'pinball_loss')


@pytest.mark.parametrize('act', M.ACTIVATIONS)
@pytest.mark.parametrize('kappa', [1.0, 0.5, 0.0])
def test_full_loss_with_l1_l2_and_dropout_and_its_gradient(act, kappa):
    x, t, mask, weight, params, dm = problem(seed=13)
    _compare_loss(f'full_{act}_{kappa}', x, t, mask, weight, params, act, kappa, 3e-4, 2e-3, dm, 'full_loss')


def test_quantiles_inverse_transforms_and_the_cap():
    x, t, mask, weight, params, _ = problem(seed=14)
    for act in M.ACTIVATIONS:
        out, _ = M.forward(params, x, act)
        _, tpar = t_forward(leaf(params), torch.tensor(x), act)
        zl = torch.special.ndtri(torch.tensor(M.LEVELS))
        tq = tpar[0][..., None] + tpar[1][..., None] * torch.sinh((zl - tpar[2][..., None]) / tpar[3][..., None])
        check(f'quantiles_{act}', M.jsu_quantiles(*M.head(out)), tq, 'quantiles')
        for form in M.TRANSFORMS:
            cap = 3.0
            zq, active = M.member_quantiles_z(params, x, act, form, cap)
            tz = torch.sinh(tq) if form.startswith('asinh') else tq
            check(f'capped_{act}_{form}', zq, torch.clamp(tz, -cap, cap), 'quantiles')
            assert np.array_equal(active, (tz.abs() > cap).numpy())


def test_adam_trajectory_on_fixed_minibatches():
    x, t, mask, weight, params, dm = problem(seed=15, n=64)
    rng = np.random.default_rng(5)
    batches = [rng.choice(len(x), 16, replace=False) for _ in range(TRAJECTORY_STEPS)]
    lr = 3e-3
    p_np = [p.copy() for p in params]
    opt = M.Adam(p_np, lr, **M.ADAM)
    tp = leaf(params)
    topt = torch.optim.Adam(tp, lr=lr, betas=(M.ADAM['beta1'], M.ADAM['beta2']), eps=M.ADAM['eps'])
    for step, idx in enumerate(batches):
        _, grads = M.loss_and_grads(p_np, x[idx], t[idx], mask[idx], weight[idx], 'elu', 0.5, 1e-4, 1e-3, dm[idx])
        opt.step(p_np, grads)
        topt.zero_grad()
        t_loss(tp, x[idx], t[idx], mask[idx], weight[idx], 'elu', 0.5, 1e-4, 1e-3, dm[idx]).backward()
        topt.step()
        for k, (a, b) in enumerate(zip(p_np, tp)):
            check(f'adam_step{step}_param{k}', a, b, 'adam_trajectory')


def test_training_loop_trajectory_against_a_pytorch_replica():
    rng0 = np.random.default_rng(16)
    n, p = 70, 6
    x = rng0.normal(size=(n, p))
    t = rng0.standard_t(4, size=(n, S)) * 0.7
    mask = rng0.random((n, S)) > 0.1
    mask[:3] = False                      # rows without a present slot: a skipped batch is possible
    weight = rng0.uniform(0.5, 1.5, n)
    weight /= weight.mean()
    xh = rng0.normal(size=(15, p))
    yh = rng0.normal(size=(15, S)) * 20 + 60
    mh = rng0.random((15, S)) > 0.05
    ch, sh = np.full(15, 55.0), np.full(15, 18.0)
    cfg = {'id': 'R', 'hidden': (7, 5), 'activation': 'softplus', 'lr': 2e-3, 'batch_size': 32, 'kappa': 0.5,
           'l1': 1e-4, 'l2': 1e-3, 'input_dropout': 0.2, 'transform': 'asinh-mad'}
    seed, cap, warm = 77, 4.0, 2
    trace = []
    member = M.train(x, t, mask, weight, xh, yh, mh, ch, sh, cfg, seed, cap, max_epochs=TRAINING_LOOP_EPOCHS,
                     patience=100, warm_epochs=warm, trace=trace)
    # The replica: the same seeded stream for initialisation, permutations and dropout masks.
    rng = np.random.Generator(np.random.PCG64(seed))
    tp = leaf(M.init_params(p, cfg['hidden'], rng))
    topt = torch.optim.Adam(tp, lr=cfg['lr'], betas=(M.ADAM['beta1'], M.ADAM['beta2']), eps=M.ADAM['eps'])
    history = []
    for epoch in range(1, TRAINING_LOOP_EPOCHS + 1):
        order = rng.permutation(n)
        kappa = 1.0 if epoch <= warm else cfg['kappa']
        for start in range(0, n, cfg['batch_size']):
            idx = order[start:start + cfg['batch_size']]
            if not mask[idx].any():
                continue
            dm = (rng.random((len(idx), p)) >= cfg['input_dropout']) / (1 - cfg['input_dropout'])
            topt.zero_grad()
            t_loss(tp, x[idx], t[idx], mask[idx], weight[idx], cfg['activation'], kappa, cfg['l1'], cfg['l2'], dm).backward()
            topt.step()
        for k, (a, b) in enumerate(zip(trace[epoch - 1], tp)):
            check(f'loop_epoch{epoch}_param{k}', a, b, 'training_loop_trajectory')
        if epoch > warm:
            with torch.no_grad():
                _, (xi, lam, gamma, delta) = t_forward(tp, torch.tensor(xh), cfg['activation'])
                zl = torch.special.ndtri(torch.tensor(M.LEVELS))
                q = xi[..., None] + lam[..., None] * torch.sinh((zl - gamma[..., None]) / delta[..., None])
                z = torch.clamp(torch.sinh(q), -cap, cap)
                eur = torch.tensor(ch)[:, None, None] + torch.tensor(sh)[:, None, None] * z
                u = torch.tensor(yh)[..., None] - eur
                tau = torch.tensor(M.LEVELS)
                rho = torch.maximum(tau * u, (tau - 1) * u)
                history.append(float(rho[torch.tensor(mh)].mean()))
    check('loop_stopping_metric', member.history, history, 'stopping_metric')
    best = int(np.argmin(history)) + warm + 1
    assert member.best_epoch == best
    for k, (a, b) in enumerate(zip(member.params, trace[best - 1])):
        assert np.array_equal(a, b), k


def test_pinned_reference_versions():
    assert torch.__version__.split('+')[0] == PINNED_TORCH
    assert hashlib.sha256((ROOT / LOCK_FILE).read_bytes()).hexdigest() == LOCK_SHA256
    assert torch.get_default_dtype() == torch.float64
