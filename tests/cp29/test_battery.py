"""CP-29's battery programme (`cp29.battery`) on synthetic days: the contract's limits, its rule, the tie-break, the
settlement and the brute-force bound, each with a negative control where a check could pass vacuously."""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from cp29 import battery as B
from cp29 import evaluate as E
from cp29 import inputs as I

SPEC = E.SPEC
ETA = B.ETA


def _day(cheap: float = 0.0, dear: float = 100.0, n: int = 24) -> np.ndarray:
    half = n // 2
    return np.array([cheap] * half + [dear] * (n - half), float)


def test_a_hand_computed_day():
    """Free energy for the first half, 100 EUR/MWh after: fill the battery (2 MWh at the terminals, 2/η at the grid)
    in the earliest hours, then sell it all (2η at the grid) in the earliest dear hours."""
    p = _day()
    s = B.plan(p, p, 25.0, SPEC)
    assert s.charge.sum() == pytest.approx(2 / ETA, abs=1e-7) and s.discharge.sum() == pytest.approx(2 * ETA, abs=1e-7)
    assert list(np.flatnonzero(s.charge)) == [0, 1, 2] and list(np.flatnonzero(s.discharge)) == [12, 13]
    assert s.charge[:2].tolist() == pytest.approx([1.0, 1.0]) and s.discharge[12] == pytest.approx(1.0)
    wear = 25.0 * 2 if SPEC.wear_on_battery else 25.0 * 2 * ETA
    expected = 100 * 2 * ETA - wear - B.FEE * (2 / ETA + 2 * ETA)
    slack = B.TOL["value"] + 1e-9                     # equal optima are values within ε_v of the best
    assert expected - slack <= s.value <= expected + 1e-9
    assert B.settle(s, p, 25.0, SPEC) == pytest.approx(s.value, abs=1e-9)
    assert B.violations(s, SPEC) == []


def test_nothing_when_the_spread_does_not_cover_the_costs():
    flat = np.full(24, 80.0)
    assert not B.plan(flat, flat, 25.0, SPEC).traded
    narrow = _day(0.0, 27.0)          # 27 x 2η = 49.8 < the wear on 2 MWh (50) and the fees (0.4): not above zero
    assert not B.plan(narrow, narrow, 25.0, SPEC).traded
    wide = _day(0.0, 40.0)            # 40 x 2η = 73.8 > 50.4: trades
    assert B.plan(wide, wide, 25.0, SPEC).traded


def test_the_same_inputs_give_the_same_schedule():
    rng = np.random.default_rng(7)
    for _ in range(5):
        p = rng.normal(80, 60, 24)
        a, b = B.plan(p, p, 25.0, SPEC), B.plan(p.copy(), p.copy(), 25.0, SPEC)
        assert np.array_equal(a.charge, b.charge) and np.array_equal(a.discharge, b.discharge)


def test_ties_go_to_the_earliest_hours():
    p = np.array([10.0] * 6 + [200.0] * 6 + [10.0] * 6 + [200.0] * 6)
    s = B.plan(p, p, 25.0, SPEC)
    assert s.charge[:6].sum() > 0 and s.charge[12:18].sum() == 0      # the earlier cheap block
    assert s.discharge[6:12].sum() > 0 and s.discharge[18:].sum() == 0  # the earlier dear block


def test_every_limit_holds_on_random_and_negative_price_days():
    rng = np.random.default_rng(11)
    for _ in range(20):
        p = rng.normal(70, 80, 24)
        p[rng.integers(0, 24, 4)] = -rng.uniform(50, 500, 4)
        for wear in B.WEARS:
            s = B.plan(p, p, wear, SPEC)
            assert B.violations(s, SPEC) == []
            assert s.value >= 0
            if SPEC.exclusive:
                assert not ((s.charge > 0) & (s.discharge > 0)).any()


@pytest.mark.parametrize("broken, word", [
    ((np.r_[1.2, np.zeros(23)], np.zeros(24)), "power"),
    ((np.r_[np.ones(3), np.zeros(21)], np.zeros(24)), "energy"),
    ((np.r_[1.0, np.zeros(23)], np.zeros(24)), "not empty"),
])
def test_negative_control_the_limit_check_catches_a_broken_schedule(broken, word):
    c, d = broken
    problems = B.violations(B.Schedule(c, d, 0.0), SPEC)
    assert any(word in p for p in problems), problems


def test_negative_control_simultaneous_and_over_cycle_schedules_are_caught():
    c = np.r_[np.ones(3), np.zeros(21)] * 0.9
    d = np.r_[0.5, np.zeros(23)]
    if SPEC.exclusive:
        assert any("same hour" in p for p in B.violations(B.Schedule(c, d, 0.0), SPEC))
    over = B.Schedule(np.r_[np.ones(3), np.zeros(5), np.ones(3), np.zeros(13)],
                      np.r_[np.zeros(4), np.ones(3), np.zeros(5), np.ones(3), np.zeros(9)], 0.0)
    assert any("cycle" in p for p in B.violations(over, SPEC))


def test_the_brute_force_never_beats_the_solver_and_finds_a_planted_better_schedule():
    rng = np.random.default_rng(3)
    for _ in range(4):
        p = rng.normal(80, 70, 24)
        s = B.plan(p, p, 25.0, SPEC)
        assert B.brute_force(p, p, 25.0, SPEC) <= s.value + B.TOL["value"]
    # the negative control: a schedule worse than the optimum is beaten by the brute force
    p = _day()
    half = B.Schedule(np.r_[1.0, np.zeros(23)], np.r_[np.zeros(12), ETA * ETA, np.zeros(11)], 0.0)
    worse = B.settle(half, p, 25.0, SPEC)
    assert B.brute_force(p, p, 25.0, SPEC) > worse + 1.0


def test_the_risk_rule_trades_at_most_as_much_as_the_median_rule():
    rng = np.random.default_rng(5)
    for _ in range(5):
        q50 = rng.normal(80, 60, 24)
        spread = rng.uniform(1, 30, 24)
        median = B.plan(q50, q50, 25.0, SPEC)
        risk = B.plan(q50 + spread, q50 - spread, 25.0, SPEC)
        assert risk.value <= median.value + B.TOL["value"]


@pytest.mark.parametrize("hours", [23, 24, 25])
def test_daylight_saving_days_solve_over_their_own_hours(hours):
    p = _day(n=hours)
    s = B.plan(p, p, 25.0, SPEC)
    assert len(s.charge) == len(s.discharge) == hours and B.violations(s, SPEC) == []


def test_a_missing_hour_is_never_planned_and_is_recorded_as_not_traded():
    p = _day()
    gap = p.copy(); gap[5] = np.nan
    with pytest.raises(ValueError, match="missing hour"):
        B.plan(gap, gap, 25.0, SPEC)
    hours = pd.date_range("2024-06-03 22:00", periods=24, freq="h", tz="UTC")
    day = I.Day("2024-06-04", hours, p, {"v6": {"q25": gap, "q50": gap, "q75": gap}, "naive": {"q50": p},
                                         "perfect_foresight": {"q50": p}})
    rows = E.daily_rows({"2024-06-04": day}, set())
    v6 = rows.loc[rows.source == "v6"]
    assert len(v6) == 2 * len(B.WEARS) and v6.missing_hour.all() and not v6.traded.any() and (v6.profit_eur == 0).all()
    assert rows.loc[rows.source == "naive", "traded"].all()
    assert (rows.evidence_class == "simulated, development, post-selection").all()


def test_the_measures():
    assert E.max_drawdown(np.array([10.0, -4.0, -3.0, 5.0, -9.0])) == pytest.approx(11.0)
    assert E.max_drawdown(np.array([1.0, 2.0])) == 0.0
    group = pd.DataFrame({"day": ["a", "b", "c", "d"], "profit_eur": [5.0, -2.0, 0.0, 7.0],
                          "missing_hour": [False, False, True, False], "traded": [True, True, False, True],
                          "bought_mwh": [1.0] * 4, "sold_mwh": [1.0] * 4, "discharged_battery_mwh": [1.0] * 4})
    m = E.measures(group, 20.0)
    assert m["cumulative_profit_eur"] == 10.0 and m["share_of_perfect_foresight"] == 0.5
    assert m["losing_days"] == 1 and m["largest_daily_loss_eur"] == 2.0 and m["missing_days"] == 1
    assert E.measures(group, 0.0)["share_of_perfect_foresight"] is None    # "undefined" for a zero denominator
