"""Protocol §§4, 5, 8 and 9 on synthetic fixtures: grid ties, weighting, the network, scores and inference."""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pytest

from cp28 import grid, inference, meta, scoring

# ------------------------------------------------------------------------------------------ grid

def test_grid_enumeration_order_and_size():
    assert grid.POINTS == 5151
    assert (grid.I[0], grid.J[0], grid.K[0]) == (0, 0, 100) and (grid.I[-1], grid.J[-1]) == (100, 0)
    keys = list(zip(grid.W_HG, grid.W_L))
    assert keys == sorted(keys)                                   # lexicographic (w_HG, w_L), ascending
    assert np.all(grid.WEIGHTS.sum(axis=1) <= 1 + 1e-15) and np.all(grid.WEIGHTS >= 0)


def test_grid_tie_breaks_by_integer_distance_then_lowest_index():
    flat = np.zeros(grid.POINTS)                                  # every point exactly tied
    chosen = grid.choose(flat)
    # Nearest grid points to (2/3, 1/6, 1/6): (66,17,17), (67,16,17) and (67,17,16), integer distance 24 each;
    # the lowest index, (66,17,17), wins.
    assert (chosen['i'], chosen['j'], chosen['k']) == (66, 17, 17)
    assert chosen['objective_ties'] == 5151 and chosen['distance_ties'] == 3
    assert sorted(int(grid.DISTANCE[k]) for k in np.flatnonzero(grid.DISTANCE == 24)) == [24, 24, 24]
    two = np.ones(grid.POINTS)
    a = int(np.flatnonzero((grid.I == 0) & (grid.J == 0))[0])        # (0,0,100), far from W0
    b = int(np.flatnonzero((grid.I == 50) & (grid.J == 25))[0])      # (50,25,25), nearer
    two[[a, b]] = 0.5
    assert grid.choose(two)['index'] == b
    with pytest.raises(FloatingPointError):
        grid.choose(np.full(grid.POINTS, np.nan))


def test_each_date_weighs_equally_including_dst_lengths():
    rng = np.random.default_rng(1)
    def date_loss(hours):
        c = rng.normal(50, 5, (hours, 3))
        y = rng.normal(50, 5, hours)
        blocks = (['night'] * 8 + ['solar'] * 7 + ['shoulder_peak'] * 9 + ['night'] * 3)[:hours]
        overall, _ = grid.date_losses(c[:, 0], c[:, 1], c[:, 2], y, blocks)
        k = 1234
        manual = np.mean(np.abs((grid.W_HG[k] * c[:, 0] + grid.W_L[k] * c[:, 1]) + grid.W_D2[k] * c[:, 2] - y))
        assert overall[k] == pytest.approx(manual, rel=1e-14)
        return overall
    short, long = date_loss(23), date_loss(25)
    objective = grid.window_objective([short, long], [0, 1])
    assert np.allclose(objective, (short + long) / 2, rtol=1e-15, atol=0)


def test_weighted_central_uses_the_grid_arithmetic():
    rng = np.random.default_rng(2)
    c, l, d = rng.normal(size=(3, 24))
    k = 777
    deployed = grid.weighted_central(grid.WEIGHTS[k], c, l, d)
    per_hour = grid.weighted_central(np.tile(grid.WEIGHTS[k], (24, 1)), c, l, d)
    loop = np.array([(grid.W_HG[k] * c[h] + grid.W_L[k] * l[h]) + grid.W_D2[k] * d[h] for h in range(24)])
    assert np.array_equal(deployed, loop) and np.array_equal(per_hour, loop)

# --------------------------------------------------------------------------------------- network

def tiny_problem(seed=0, n=6):
    rng = np.random.default_rng(seed)
    rows = 3 * n
    x = rng.normal(size=(rows, 16))
    c = rng.normal(50, 10, (rows, 9, 3))
    y = rng.normal(50, 10, (rows, 9))
    mask = np.ones((rows, 9))
    mask[1::3, 7:] = 0
    hours = np.full(rows, 24.0)
    return x, c, y, mask, hours, n


def test_seed_and_initialization_are_the_registered_draws():
    day = date(2023, 5, 17)
    params = meta.initial_parameters(day)
    rng = np.random.default_rng(np.random.SeedSequence([28, day.toordinal(), 0x4D4C]))
    assert np.array_equal(params['W1'], rng.normal(0, 0.1, (16, 8)))
    assert np.array_equal(params['W2'], rng.normal(0, 0.1, (8, 3)))
    assert not params['b1'].any() and not params['b2'].any()
    assert not np.array_equal(meta.initial_parameters(day + timedelta(days=1))['W1'], params['W1'])


def test_gradient_matches_finite_differences_including_the_l2_term():
    x, c, y, mask, hours, n = tiny_problem()
    q = 1.0 / (n * hours)
    params = meta.initial_parameters(date(2022, 1, 1))
    xs = (x - x.mean(0)) / x.std(0)

    def objective(p):
        loss, _ = meta.gradients(p, xs, c, y, mask, q)
        return loss + meta.L2 * (np.sum(p['W1'] ** 2) + np.sum(p['W2'] ** 2))
    _, grads = meta.gradients(params, xs, c, y, mask, q)
    eps = 1e-6
    for name, index in (('W1', (3, 2)), ('W1', (15, 7)), ('W2', (4, 1)), ('b1', (5,)), ('b2', (2,))):
        up = {k: v.copy() for k, v in params.items()}
        down = {k: v.copy() for k, v in params.items()}
        up[name][index] += eps
        down[name][index] -= eps
        numeric = (objective(up) - objective(down)) / (2 * eps)
        assert grads[name][index] == pytest.approx(numeric, rel=1e-5, abs=1e-9), name


def test_adam_update_rule_and_deterministic_fit(monkeypatch):
    x, c, y, mask, hours, n = tiny_problem(seed=3)
    day = date(2021, 7, 1)
    fit = meta.fit(day, x, c, y, mask, hours, n)
    assert fit.seed == (28, day.toordinal(), 0x4D4C)
    assert fit.initial_sha256 == meta.parameter_hash(meta.initial_parameters(day))
    assert meta.fit(day, x, c, y, mask, hours, n).final_sha256 == fit.final_sha256     # no retry seed, no jitter
    # Two updates by hand, with bias correction and epsilon outside the square root.
    weight = mask.sum(1) / (n * hours)
    mean, _, scale = meta.standardize_fit(x, weight)
    xs, q = (x - mean) / scale, 1.0 / (n * hours)
    params = meta.initial_parameters(day)
    m = {k: np.zeros_like(v) for k, v in params.items()}
    v = {k: np.zeros_like(v) for k, v in params.items()}
    for t in (1, 2):
        _, g = meta.gradients(params, xs, c, y, mask, q)
        for k in params:
            m[k] = 0.9 * m[k] + (1 - 0.9) * g[k]
            v[k] = 0.999 * v[k] + (1 - 0.999) * g[k] * g[k]
            params[k] = params[k] - 0.01 * (m[k] / (1 - 0.9 ** t)) / (np.sqrt(v[k] / (1 - 0.999 ** t)) + 1e-8)
    monkeypatch.setattr(meta, 'EPOCHS', 2)
    two = meta.fit(day, x, c, y, mask, hours, n)
    assert two.final_sha256 == meta.parameter_hash(params)
    assert meta.EPOCHS == 2 and fit.final_sha256 != two.final_sha256


def test_scaler_uses_row_weights_and_zero_sd_scale_one():
    x = np.array([[1.0, 5.0], [3.0, 5.0], [7.0, 5.0]])
    w = np.array([0.5, 0.25, 0.25])
    mean, sd, scale = meta.standardize_fit(x, w)
    assert mean[0] == pytest.approx(3.0) and sd[1] == 0 and scale[1] == 1.0
    assert sd[0] == pytest.approx(np.sqrt(0.5 * 4 + 0.25 * 0 + 0.25 * 16))


def test_meta_loss_is_mean_daily_mae():
    x, c, y, mask, hours, n = tiny_problem(seed=4)
    params = meta.initial_parameters(date(2024, 2, 2))
    xs = x.copy()
    loss, _ = meta.gradients(params, xs, c, y, mask, 1.0 / (n * hours))
    _, p = meta.forward(params, xs)
    central = meta.combine(p, c)
    per_date = [(np.abs(central[3 * s:3 * s + 3] - y[3 * s:3 * s + 3]) * mask[3 * s:3 * s + 3]).sum() / 24 for s in range(n)]
    assert loss == pytest.approx(np.mean(per_date), rel=1e-12)

# ---------------------------------------------------------------------------------------- scores

def test_wis_matches_the_registered_formula():
    q = np.array([[10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0]])
    for y, expected_mae in ((40.0, 0.0), (5.0, 35.0), (100.0, 60.0)):
        mae, wis = scoring.hourly(q, np.array([y]))
        manual = 0.5 * abs(y - 40)
        for alpha, lo, hi in ((0.5, 30, 50), (0.2, 20, 60), (0.05, 10, 70)):
            manual += alpha / 2 * ((hi - lo) + 2 / alpha * max(lo - y, 0) + 2 / alpha * max(y - hi, 0))
        assert mae[0] == expected_mae and wis[0] == pytest.approx(manual / 3.5)

# ------------------------------------------------------------------------------------- inference

def dates(first, count, skip=()):
    out = [first + timedelta(days=i) for i in range(count)]
    return [d for d in out if d not in set(skip)]


def test_runs_split_at_gaps_and_years_and_join_2020_to_2021():
    days = dates(date(2020, 12, 29), 10) + dates(date(2021, 12, 30), 5)
    runs = inference.calendar_runs(days)
    assert [(b, e) for b, e, _ in runs] == [(0, 10), (10, 12), (12, 15)]   # gap, then the 2022 stratum
    unstratified = inference.calendar_runs(days, stratified=False)
    assert [(b, e) for b, e, _ in unstratified] == [(0, 10), (10, 15)]


def test_draw_plan_and_hac_match_cp26_reference():
    cp26 = pytest.importorskip('cp26.inference', reason='CP-26 reference implementation unavailable')
    days = dates(date(2021, 1, 1), 400, skip=[date(2021, 3, 3), date(2021, 7, 9)])
    rng_a, rng_b = np.random.default_rng(5), np.random.default_rng(5)
    for block, stratified in ((14, True), (7, True), (28, True), (14, False)):
        ours = inference.draw_plan(inference.calendar_runs(days, stratified=stratified), block_days=block, rng=rng_a, replicates=50)
        ref = cp26.draw_plan(days, block_days=block, stratified=stratified, rng=rng_b, replicates=50)
        assert np.array_equal(ours.starts, ref.starts) and np.array_equal(ours.indices(), ref.indices())
    x = np.random.default_rng(6).normal(size=(3, len(days)))
    runs = inference.calendar_runs(days)
    assert np.allclose(inference.hac_variance(x, runs), cp26.hac_variance_mean(x, runs), rtol=1e-12, atol=0)


def test_one_sided_boundary_and_degenerate_endpoints():
    days = dates(date(2021, 1, 1), 200)
    rng = np.random.default_rng(inference.SEED)
    d = np.sin(np.arange(200))
    d = d - d.mean()                                                   # mean exactly at the null boundary
    result = inference.test_endpoint(d, days, block_days=14, stratified=True, rng=rng, required_cell=False, replicates=999)
    assert result['status'] == 'computable' and result['p'] > 0.05
    state = rng.bit_generator.state
    flat = inference.test_endpoint(np.zeros(200), days, block_days=14, stratified=True, rng=rng, required_cell=False)
    assert flat['p'] == 1.0 and flat['status'] == 'nonpositive_or_nonfinite_variance'
    short = inference.test_endpoint(np.ones(89), days[:89], block_days=14, stratified=True, rng=rng, required_cell=True)
    assert short['p'] == 1.0 and short['status'].startswith('deficient')
    assert rng.bit_generator.state == state                            # uncomputable endpoints consume no draw
    strong = inference.test_endpoint(-1 + 0.1 * np.sin(np.arange(200)), days, block_days=14, stratified=True,
                                     rng=np.random.default_rng(1), required_cell=False, replicates=999)
    assert strong['p'] == 1 / 1000                                     # positive control: a clear improvement rejects


def test_twenty_endpoints_and_the_compound_maximum():
    names = [e['name'] for e in inference.endpoints()]
    assert len(names) == 20 and names[:2] == ['overall:overall:MAE', 'overall:overall:WIS']
    assert names[2:4] == ['year:2021:MAE', 'year:2021:WIS'] and names[-2:] == ['season:SON:MAE', 'season:SON:WIS']
    days = dates(date(2020, 12, 29), 5 * 365 + 200)
    rng = np.random.default_rng(9)
    v5 = {d: (20 + rng.normal(), 12 + rng.normal()) for d in days}
    good = {d: (0.9 * a, 0.9 * b) for d, (a, b) in v5.items()}
    hole = {d: v for d, v in good.items() if not (d.year == 2023 and d.month < 11)}   # 2023 keeps 61 dates
    losses = {'v5': v5, **{arm: good for arm in inference.ARMS}, 'A3': hole}
    out = inference.run_variant(losses, inference.VARIANTS[0], replicates=199)
    assert out['A1']['compound_p'] == max(r['p'] for r in out['A1']['endpoints']) < 0.05
    assert out['A3']['compound_p'] == 1.0 and out['A3']['first_unmet'] == 'year:2023:MAE'


def test_holm_step_down_and_adjusted_p():
    p = {'A1': 0.004, 'A2': 0.02, 'A3': 0.008, 'A4': 0.5, 'A5': 0.008, 'A6': 1.0, 'A7': 0.03}
    rows = inference.holm(p)
    assert [r['arm'] for r in rows] == ['A1', 'A3', 'A5', 'A2', 'A7', 'A4', 'A6']     # equal p: lower arm number first
    assert [r['rejected'] for r in rows] == [True, True, True, False, False, False, False]  # 0.02 > 0.05/4 stops
    assert rows[0]['threshold'] == pytest.approx(0.05 / 7) and rows[3]['threshold'] == pytest.approx(0.05 / 4)
    assert [round(r['adjusted_p'], 6) for r in rows] == [0.028, 0.048, 0.048, 0.08, 0.09, 1.0, 1.0]
    late = inference.holm({**p, 'A1': 0.0072})                                        # just above 0.05/7: nothing rejects
    assert not any(r['rejected'] for r in late)


def test_sensitivity_variants_and_pass_rule():
    names = [v[0] for v in inference.VARIANTS]
    assert names == ['primary14', 'sensitivity7', 'sensitivity28', 'unstratified14']
    assert [v[1] for v in inference.VARIANTS] == [14, 7, 28, 14] and [v[2] for v in inference.VARIANTS] == [True, True, True, False]
    days = dates(date(2021, 12, 20), 30)
    plan = inference.draw_plan(inference.calendar_runs(days, stratified=False), block_days=14,
                               rng=np.random.default_rng(0), replicates=200)
    crosses = (plan.indices()[:, 11] == 11) & (plan.indices()[:, 12] == 12)   # Dec 31 → Jan 1 kept adjacent
    assert crosses.any()


def test_selection_ties_and_simplicity_order():
    wis = {'A1': 10.0, 'A2': 10.04, 'A3': 10.06, 'A4': 9.999, 'A5': 10.2, 'A6': 10.0499, 'A7': 9.98}
    out = inference.select(['A2', 'A3', 'A4', 'A6', 'A7'], wis)
    # best 9.98 (A7); bound 10.0299: A4, A7 tied → A4 is simpler than A7.
    assert out['best_arm'] == 'A7' and out['tie_set'] == ['A4', 'A7'] and out['selected'] == 'A4'
    exactly = inference.select(['A1', 'A2'], {'A1': 10.05, 'A2': 10.0})
    assert exactly['tie_set'] == ['A2'] and exactly['selected'] == 'A2'                 # +0.5% exactly is not tied
    assert inference.select([], wis)['selected'] == 'control'
