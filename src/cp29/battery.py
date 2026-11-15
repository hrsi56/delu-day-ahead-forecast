"""The battery's daily programme, exactly the contract's §2 and §3 (the packet's §0, "The programme").

**Variables,** for each hour t of the delivery day (T = 23, 24 or 25): `c[t]`, the energy bought at the grid (MWh,
charging); `d[t]`, the energy sold at the grid (MWh, discharging); `s[t]`, the stored energy at the end of hour t
(MWh, at the battery's terminals); and, when charging and discharging are exclusive, a binary `z[t]` (1: may charge).

**Limits (§2):**
- power, 1 MW at the grid each way: 0 ≤ c[t] ≤ 1, 0 ≤ d[t] ≤ 1 (MWh in one hour);
- efficiency, √0.85 on charge and on discharge: s[t] = s[t−1] + η·c[t] − d[t]/η, η = √0.85;
- usable energy, 0 ≤ s[t] ≤ 2 MWh; empty at the start and at the end of the day: s[−1] = 0, s[T−1] = 0;
- one cycle a day: the energy discharged from the battery, Σ d[t]/η, is at most 2 MWh;
- exclusive (when ruled so): c[t] ≤ z[t], d[t] ≤ 1 − z[t].

**The objective (§3),** a forecast's net value of the schedule, maximized:
Σ sell[t]·d[t] − Σ buy[t]·c[t] − wear·W − fee·Σ (c[t] + d[t]), where W is the wear base (the energy discharged from
the battery, Σ d[t]/η, or at the grid, Σ d[t], as §0 fixes it), `buy = sell = q50` under the median rule and
`buy = q75`, `sell = q25` under the risk-aware variant. If the best value is not above zero, the battery does nothing.

**The tie-break (§3: "among equal optima, the schedule that trades earliest and least"):** three solves. (1) the best
value V*; (2) among schedules worth at least V* − ε_v, the least energy traded, E* = min Σ (c + d); (3) among those
also trading at most E* + ε_e, the earliest: min Σ (t + 1)·(c[t] + d[t]). Every solve is HiGHS with the tolerances
below; the result is a function of the inputs alone. Equal optima are values within ε_v of the best, so the chosen
schedule's value is within ε_v of V*.

**Settlement (§3 step 4):** the chosen schedule at the cleared prices, with the same wear and fees.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, linprog, milp

ETA = math.sqrt(0.85)
POWER_MWH = 1.0          # 1 MW for one hour, at the grid
ENERGY_MWH = 2.0         # usable, at the terminals
CYCLE_MWH = 2.0          # discharged from the battery per day
FEE = 0.10               # EUR per MWh bought and per MWh sold
WEARS = (25.0, 0.0, 50.0)  # EUR per MWh discharged: the main value, then the sensitivity
#: Tolerances (the packet's §0): HiGHS's primal and dual feasibility; the value slack ε_v (EUR) and the energy slack
#: ε_e (MWh) of the tie-break; the do-nothing threshold (EUR); the zero below which an energy is set to 0 (MWh); and the
#: feasibility tolerance of the schedule check (MWh).
TOL = {"feasibility": 1e-9, "value": 1e-6, "energy": 1e-7, "nothing": 1e-6, "zero": 1e-9, "check": 1e-7}
HIGHS = {"primal_feasibility_tolerance": TOL["feasibility"], "dual_feasibility_tolerance": TOL["feasibility"],
         "presolve": True}


@dataclass(frozen=True)
class Spec:
    """What §0 fixes about the programme beyond the contract's numbers."""
    exclusive: bool          # charging and discharging never in the same hour (a binary per hour)
    wear_on_battery: bool    # the wear base: energy discharged from the battery (else at the grid)


@dataclass(frozen=True)
class Schedule:
    charge: np.ndarray       # c[t], MWh bought at the grid
    discharge: np.ndarray    # d[t], MWh sold at the grid
    value: float             # the forecast's own net value of this schedule, EUR

    @property
    def traded(self) -> bool:
        return bool(self.charge.sum() + self.discharge.sum() > 0)

    @property
    def discharged_battery(self) -> float:
        return float(self.discharge.sum() / ETA)

    def soc(self) -> np.ndarray:
        return np.cumsum(ETA * self.charge - self.discharge / ETA)


NOTHING = None


def _matrices(n: int, spec: Spec):
    """The constraint rows over x = [c (n), d (n), s (n), z (n if exclusive)]."""
    nz = n if spec.exclusive else 0
    m = 3 * n + nz
    rows, lo, hi = [], [], []
    for t in range(n):                       # s[t] - s[t-1] - eta c[t] + d[t]/eta = 0
        r = np.zeros(m)
        r[2 * n + t] = 1.0
        if t:
            r[2 * n + t - 1] = -1.0
        r[t] = -ETA
        r[n + t] = 1.0 / ETA
        rows.append(r); lo.append(0.0); hi.append(0.0)
    r = np.zeros(m); r[n:2 * n] = 1.0 / ETA  # one cycle: sum d/eta <= 2
    rows.append(r); lo.append(-np.inf); hi.append(CYCLE_MWH)
    if spec.exclusive:
        for t in range(n):                   # c[t] - z[t] <= 0 ; d[t] + z[t] <= 1
            r = np.zeros(m); r[t] = 1.0; r[3 * n + t] = -1.0
            rows.append(r); lo.append(-np.inf); hi.append(0.0)
            r = np.zeros(m); r[n + t] = 1.0; r[3 * n + t] = 1.0
            rows.append(r); lo.append(-np.inf); hi.append(1.0)
    lb = np.zeros(m)
    ub = np.concatenate([np.full(n, POWER_MWH), np.full(n, POWER_MWH), np.full(n, ENERGY_MWH), np.ones(nz)])
    ub[3 * n - 1] = 0.0                      # empty at the end of the day
    return np.array(rows), np.array(lo), np.array(hi), lb, ub, m


def _value_row(buy: np.ndarray, sell: np.ndarray, wear: float, spec: Spec, m: int) -> np.ndarray:
    """The objective as a row: the forecast's net value of x."""
    n = len(buy)
    w = wear / ETA if spec.wear_on_battery else wear
    r = np.zeros(m)
    r[:n] = -buy - FEE
    r[n:2 * n] = sell - w - FEE
    return r


def _solve(objective: np.ndarray, rows, lo, hi, lb, ub, spec: Spec, n: int) -> np.ndarray:
    """Minimize objective · x under the rows and bounds; HiGHS (MIP when exclusive)."""
    if spec.exclusive:
        integrality = np.zeros(len(objective)); integrality[3 * n:] = 1
        res = milp(objective, constraints=LinearConstraint(rows, lo, hi), bounds=Bounds(lb, ub),
                   integrality=integrality, options={"presolve": True, "mip_rel_gap": 0.0})
    else:
        eq = lo == hi
        upper = ~eq & np.isfinite(hi)
        lower = ~eq & np.isfinite(lo)
        a_ub = np.vstack([rows[upper], -rows[lower]])
        b_ub = np.concatenate([hi[upper], -lo[lower]])
        res = linprog(objective, A_ub=a_ub, b_ub=b_ub, A_eq=rows[eq], b_eq=lo[eq], bounds=list(zip(lb, ub)),
                      method="highs", options=HIGHS)
    if res.status != 0:
        raise RuntimeError(f"HiGHS: {res.message}")
    return res.x


def _stages(buy: np.ndarray, sell: np.ndarray, wear: float, spec: Spec, cmax: np.ndarray, dmax: np.ndarray):
    """The three solves (value, then least energy, then earliest) with per-hour power bounds; None when the best value
    is not above zero."""
    n = len(buy)
    rows, lo, hi, lb, ub, m = _matrices(n, spec)
    ub[:n] = np.minimum(ub[:n], cmax)
    ub[n:2 * n] = np.minimum(ub[n:2 * n], dmax)
    value = _value_row(buy, sell, wear, spec, m)
    x = _solve(-value, rows, lo, hi, lb, ub, spec, n)
    best = float(value @ x)
    if best <= TOL["nothing"]:
        return None
    energy = np.zeros(m); energy[:2 * n] = 1.0
    rows2 = np.vstack([rows, value]); lo2 = np.append(lo, best - TOL["value"]); hi2 = np.append(hi, np.inf)
    x = _solve(energy, rows2, lo2, hi2, lb, ub, spec, n)
    least = float(energy @ x)
    early = np.zeros(m); early[:n] = early[n:2 * n] = np.arange(1, n + 1)
    rows3 = np.vstack([rows2, energy]); lo3 = np.append(lo2, -np.inf); hi3 = np.append(hi2, least + TOL["energy"])
    return _solve(early, rows3, lo3, hi3, lb, ub, spec, n), value


def plan(buy: np.ndarray, sell: np.ndarray, wear: float, spec: Spec) -> Schedule:
    """§3's rule for one day: the best schedule under the forecast, tie-broken, or nothing when not above zero.

    When charging and discharging are exclusive, the three solves run first as mixed-integer programmes, which choose
    each hour's direction; then, with those directions fixed, they run again as linear programmes, at the linear
    solver's tolerances (scipy's `milp` cannot tighten HiGHS's MIP feasibility tolerance, about 1e-6)."""
    buy, sell = np.asarray(buy, float), np.asarray(sell, float)
    n = len(buy)
    if n == 0 or np.isnan(buy).any() or np.isnan(sell).any():
        raise ValueError("a day with a missing hour is not planned (the caller records it as not traded)")
    full = np.full(n, POWER_MWH)
    linear = Spec(exclusive=False, wear_on_battery=spec.wear_on_battery)
    if spec.exclusive:
        found = _stages(buy, sell, wear, spec, full, full)
        if found is None:
            return Schedule(np.zeros(n), np.zeros(n), 0.0)
        z = np.round(found[0][3 * n:])               # 1: the hour may charge; 0: it may discharge
        found = _stages(buy, sell, wear, linear, full * z, full * (1 - z))
    else:
        found = _stages(buy, sell, wear, linear, full, full)
    if found is None:
        return Schedule(np.zeros(n), np.zeros(n), 0.0)
    x, value = found
    c, d = x[:n].copy(), x[n:2 * n].copy()
    c[np.abs(c) < TOL["zero"]] = 0.0
    d[np.abs(d) < TOL["zero"]] = 0.0
    c, d = np.clip(c, 0.0, POWER_MWH), np.clip(d, 0.0, POWER_MWH)
    return Schedule(c, d, float(value[:2 * n] @ np.concatenate([c, d])))


def settle(schedule: Schedule, price: np.ndarray, wear: float, spec: Spec) -> float:
    """The realized net profit of a schedule at the cleared prices, EUR (§3 step 4)."""
    w = wear / ETA if spec.wear_on_battery else wear
    c, d = schedule.charge, schedule.discharge
    return float(np.dot(price, d) - np.dot(price, c) - w * d.sum() - FEE * (c.sum() + d.sum()))


def violations(schedule: Schedule, spec: Spec) -> list[str]:
    """Every §2 limit the schedule breaks, beyond the check tolerance; empty when it meets them all."""
    tol, c, d = TOL["check"], schedule.charge, schedule.discharge
    s = schedule.soc()
    out = []
    if (c < -tol).any() or (d < -tol).any() or (c > POWER_MWH + tol).any() or (d > POWER_MWH + tol).any():
        out.append("power")
    if (s < -tol).any() or (s > ENERGY_MWH + tol).any():
        out.append("energy")
    if abs(s[-1]) > tol:
        out.append("not empty at the end of the day")
    if d.sum() / ETA > CYCLE_MWH + tol:
        out.append("more than one cycle")
    if spec.exclusive and ((c > tol) & (d > tol)).any():
        out.append("charging and discharging in the same hour")
    return out


def brute_force(buy: np.ndarray, sell: np.ndarray, wear: float, spec: Spec, step: float = 0.05) -> float:
    """The best forecast value over every schedule on a grid of stored energy (step MWh), by dynamic programming over
    (stored energy, energy discharged so far): an exhaustive search of the grid, never better than the solver's
    optimum when the solver is right. One battery flow per hour (charging or discharging), so it also bounds the
    exclusive programme."""
    k = int(round(ENERGY_MWH / step))
    w = wear / ETA if spec.wear_on_battery else wear
    levels = np.arange(k + 1) * step
    neg = -np.inf
    best = np.full((k + 1, k + 1), neg)        # [stored, discharged-so-far (battery side)]
    best[0, 0] = 0.0
    for t in range(len(buy)):
        nxt = np.full_like(best, neg)
        for i in range(k + 1):
            for j in range(k + 1):
                v = best[i, j]
                if v == neg:
                    continue
                for i2 in range(k + 1):
                    delta = levels[i2] - levels[i]
                    if delta > 0:                  # charge: c = delta / eta at the grid
                        c = delta / ETA
                        if c > POWER_MWH + 1e-12:
                            continue
                        gain, j2 = -buy[t] * c - FEE * c, j
                    elif delta < 0:                # discharge: the battery gives -delta, the grid gets -delta * eta
                        d = -delta * ETA
                        if d > POWER_MWH + 1e-12:
                            continue
                        j2 = j + (i - i2)
                        if j2 > k:
                            continue
                        gain = sell[t] * d - w * d - FEE * d
                    else:
                        gain, j2 = 0.0, j
                    if v + gain > nxt[i2, j2]:
                        nxt[i2, j2] = v + gain
        best = nxt
    return float(max(best[0].max(), 0.0))
