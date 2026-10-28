"""4.7T's frozen analysis on synthetic losses only (CI-safe): no day after 2026-09-06 exists or is read."""
from __future__ import annotations

from datetime import date

import numpy as np
import pytest

from cp17.issue import canonical_hours
from cp17.tools import fresh_test as T

#: 90 development dates standing in for the window; the losses are synthetic, not development outcomes.
STAND_IN = (date(2026, 6, 9), date(2026, 9, 6))


def synthetic(product_error: float, v5_error: float, b0_error: float, drop=()):
    rng = np.random.default_rng(7)
    issued, outcomes = {'A1': {}, 'v5': {}, 'B0': {}}, {}
    for day in T.window_days(STAND_IN):
        keys = canonical_hours(day)
        truth = 60 + 20 * rng.standard_normal(len(keys))
        outcomes.update(zip(keys, truth))
        for policy, scale in (('A1', product_error), ('v5', v5_error), ('B0', b0_error)):
            if policy == 'A1' and str(day) in drop:
                continue
            centre = truth + scale * rng.standard_normal(len(keys))
            q = centre[:, None] + np.array([-2, -1.3, -0.7, 0, 0.7, 1.3, 2]) * scale
            issued[policy][str(day)] = (keys, q.tolist())
    return issued, outcomes


def test_window_is_the_registered_one():
    days = T.window_days()
    assert len(days) == 90 and str(days[0]) == '2026-09-07' and str(days[-1]) == '2026-12-05'


def test_a_clearly_better_product_passes_and_a_worse_one_fails():
    better = T.analyse(*synthetic(5.0, 9.0, 20.0), window=STAND_IN)
    assert better['decision'] == 'pass' and better['compound_p'] <= 0.05 and better['paired_days'] == {'v5': 90, 'B0': 90}
    worse = T.analyse(*synthetic(12.0, 9.0, 20.0), window=STAND_IN)
    assert worse['decision'] == 'fail' and worse['compound_p'] > 0.05
    assert [(e['comparator'], e['metric']) for e in better['endpoints']] == [('v5', 'MAE'), ('v5', 'WIS'), ('B0', 'MAE'), ('B0', 'WIS')]


def test_the_analysis_is_deterministic():
    a = T.analyse(*synthetic(8.0, 9.0, 20.0), window=STAND_IN)
    b = T.analyse(*synthetic(8.0, 9.0, 20.0), window=STAND_IN)
    assert a == b and a['seed'] == 20261204 and a['block_days'] == 7 and a['replicates'] == 10_000


def test_minimum_support():
    days = [str(d) for d in T.window_days(STAND_IN)]
    short = T.analyse(*synthetic(5.0, 9.0, 20.0, drop=set(days[:31])), window=STAND_IN)
    assert short['decision'] == 'inconclusive (support)' and short['paired_days']['v5'] == 59
    enough = T.analyse(*synthetic(5.0, 9.0, 20.0, drop=set(days[:30])), window=STAND_IN)
    assert enough['support_sufficient'] and enough['paired_days']['B0'] == 60


def test_the_real_window_is_refused_until_the_gate():
    from cp25.guard import BoundaryRefused
    issued, outcomes = synthetic(5.0, 9.0, 20.0)
    shifted = {p: {str(date.fromisoformat(d) + (T.WINDOW[0] - STAND_IN[0])): v for d, v in days.items()}
               for p, days in issued.items()}
    with pytest.raises(BoundaryRefused):
        T.analyse(shifted, outcomes)
