"""The search procedure's fixed parts (capstone v21-r11 §23.4, §23.6): batch tiling (B = 3, 7, 11, 11, 11),
the gate windows, the seeded sampler, the space's bounds, successive halving and the ranking rule."""
from datetime import date

import math
import numpy as np

from cp24 import sampler as SP

FOLDS = [(date(2020, 5, 25), date(2020, 9, 28)), (date(2021, 2, 23), date(2021, 6, 29)), (date(2022, 5, 25), date(2022, 9, 28)),
         (date(2025, 3, 22), date(2025, 7, 29)), (date(2025, 12, 2), date(2026, 4, 7))]
GATES = [('2020-03-30', '2020-05-24'), ('2020-12-29', '2021-02-22'), ('2022-03-30', '2022-05-24'), ('2025-01-25', '2025-03-21'),
         ('2025-10-07', '2025-12-01')]


def test_gate_windows_are_the_anchors_and_hold_280_days():
    total = 0
    for (d0, _), (a, b) in zip(FOLDS, GATES):
        g0, g1 = SP.gate_window(d0)
        assert (str(g0), str(g1)) == (a, b)
        total += (g1 - g0).days + 1
    assert total == 280


def test_batches_tile_backward_skip_every_folds_days_and_give_b_3_7_11_11_11():
    counts = []
    for d0, _ in FOLDS:
        bs = SP.batches(d0, FOLDS)
        counts.append(len(bs))
        assert bs[0][1] == date.fromordinal(d0.toordinal() - 57)
        for a, b in bs:
            assert (b - a).days == 27 and a >= date(2020, 1, 1)
            assert all(b < s or a > e for s, e in FOLDS)
            for g0, g1 in (SP.gate_window(x) for x, _ in FOLDS):
                if g0 >= d0:
                    assert b < g0                           # never fold f's own gate or later
        assert all(bs[i][0] > bs[i + 1][1] for i in range(len(bs) - 1))
    assert counts == [3, 7, 11, 11, 11]


def test_the_sampler_is_seeded_and_stays_inside_the_space():
    a = SP.trials(1, 2, 64, SP.SPACE_ROUND_1)
    b = SP.trials(1, 2, 64, SP.SPACE_ROUND_1)
    assert a == b and SP.trials(1, 3, 64, SP.SPACE_ROUND_1) != a
    for c in a:
        assert len(c['hidden']) in (1, 2) and all(16 <= w <= 512 for w in c['hidden'])
        assert c['activation'] in ('elu', 'relu', 'softplus', 'tanh')
        assert c['input_dropout'] is None or 0.05 <= c['input_dropout'] <= 0.5
        assert c['l1'] is None or 1e-7 <= c['l1'] <= 1e-3
        assert c['l2'] is None or 1e-6 <= c['l2'] <= 1e-2
        assert 1e-4 <= c['lr'] <= 1e-2 and c['batch_size'] in (32, 64, 128) and c['kappa'] in (1.0, 0.5, 0.0)
        assert c['half_life'] in (None, 365, 180) and set(c['groups']) <= set(SP.OPTIONAL_GROUPS)
        assert c['transform'] in ('z-s4', 'asinh-s4', 'z-mad', 'asinh-mad')


def test_halving_ranking_and_seeds():
    assert SP.halving_survivors(128) == 43 and SP.halving_survivors(32) == 11
    res = {'a': 1.0, 'b': 1.0, 'c': 0.5, 'd': math.inf}
    size = {'a': 100, 'b': 50, 'c': 999, 'd': 1}
    assert SP.rank(res, size, ['a', 'b', 'c', 'd']) == ['c', 'b', 'a', 'd']
    seeds = SP.member_seeds(1, 3)
    assert len(set(seeds)) == 8
    assert SP.pooled({0: 2.0, 1: 4.0}, {0: 1, 1: 3}, [0, 1]) == 1.5 and SP.pooled({0: 2.0}, {0: 1}, [0, 1]) == math.inf
