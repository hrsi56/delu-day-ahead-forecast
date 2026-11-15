"""The contract's evaluation (§§3, 4, 6), on P-all and P-v5, written to `reports/cp29/`.

    uv run python -m cp29.evaluate              # the checks, then every daily row, the summaries and the report
    uv run python -m cp29.evaluate --check      # re-derive every summary from the committed daily rows; write nothing
    uv run python -m cp29.evaluate --summaries  # rewrite the summaries from the committed daily rows

**What is computed, and nothing else:** for each source and rule the contract names (v6 and v5 under the median rule
and the risk-aware variant; the similar-day naive under the median rule; perfect foresight), at each wear cost (€25,
the main value, then €0 and €50), one row per day: the schedule's energy, the realized profit and the forecast's own
expected profit. Then, from those rows alone: the contract's measures per population, source, rule and wear, by regime
with counts; and the paired differences with the moving-block bootstrap.
"""
from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

from cp29 import battery as B
from cp29 import inputs as I

OUT = Path("reports/cp29")
EVIDENCE = "simulated, development, post-selection"
#: The programme's form beyond the contract's numbers (the packet's §0).
SPEC = B.Spec(exclusive=True, wear_on_battery=True)
#: The rules by source: the prices each uses to buy and to sell (§3); perfect foresight uses the cleared prices.
RULES = {"v6": (("median", "q50", "q50"), ("risk", "q75", "q25")),
         "naive": (("median", "q50", "q50"),),
         "v5": (("median", "q50", "q50"), ("risk", "q75", "q25")),
         "perfect_foresight": (("perfect", "q50", "q50"),)}
#: The paired differences (§6), in the bootstrap's draw order: (population, rule, source, minus).
PAIRS = (("P-all", "median", "v6", "naive"), ("P-v5", "median", "v6", "naive"),
         ("P-v5", "median", "v6", "v5"), ("P-v5", "risk", "v6", "v5"))
BOOT_SEED = 20261115
#: The brute-force sample (§0): every 50th day of P-all in calendar order, from the first.
BRUTE_EVERY, BRUTE_STEP = 50, 0.05
DAILY_COLUMNS = ["day", "regime", "in_p_v5", "hours", "source", "rule", "wear_eur_per_mwh", "missing_hour", "traded",
                 "bought_mwh", "sold_mwh", "discharged_battery_mwh", "expected_profit_eur", "profit_eur",
                 "tie_break_fallbacks", "evidence_class"]


def _csv(frame: pd.DataFrame) -> str:
    return frame.to_csv(index=False, float_format="%.17g", lineterminator="\n")


# ------------------------------------------------------------------------------------------------------- daily rows

def daily_rows(days: dict[str, I.Day], p_v5: set[str]) -> pd.DataFrame:
    rows = []
    for day, data in days.items():
        regime = I.regime_of(day)
        for source, rules in RULES.items():
            if source not in data.sources:
                continue
            forecast = data.sources[source]
            for rule, buy_q, sell_q in rules:
                buy, sell = forecast[buy_q], forecast[sell_q]
                missing = bool(np.isnan(buy).any() or np.isnan(sell).any() or np.isnan(data.price).any())
                for wear in B.WEARS:
                    row = {"day": day, "regime": regime, "in_p_v5": day in p_v5, "hours": len(data.hours),
                           "source": source, "rule": rule, "wear_eur_per_mwh": wear, "missing_hour": missing,
                           "evidence_class": EVIDENCE}
                    if missing:      # §5: not traded, profit zero, kept and counted
                        row.update(traded=False, bought_mwh=0.0, sold_mwh=0.0, discharged_battery_mwh=0.0,
                                   expected_profit_eur=0.0, profit_eur=0.0, tie_break_fallbacks=0)
                    else:
                        s = B.plan(buy, sell, wear, SPEC)
                        bad = B.violations(s, SPEC)
                        if bad:
                            raise AssertionError(f"{day} {source} {rule} {wear}: the schedule breaks {bad}")
                        row.update(traded=s.traded, bought_mwh=float(s.charge.sum()),
                                   sold_mwh=float(s.discharge.sum()), discharged_battery_mwh=s.discharged_battery,
                                   expected_profit_eur=s.value, profit_eur=B.settle(s, data.price, wear, SPEC),
                                   tie_break_fallbacks=s.fallbacks)
                    rows.append(row)
    return pd.DataFrame(rows, columns=DAILY_COLUMNS)


# ------------------------------------------------------------------------------------------------------- measures

def max_drawdown(profits: np.ndarray) -> float:
    """The largest fall of the cumulative profit curve from a previous peak (the curve starts at zero)."""
    curve = np.concatenate([[0.0], np.cumsum(profits)])
    return float((np.maximum.accumulate(curve) - curve).max())


def measures(group: pd.DataFrame, pf_total: float) -> dict:
    p = group.sort_values("day").profit_eur.to_numpy(float)
    losing = p < 0
    total = float(p.sum())
    return {"days": len(p), "missing_days": int(group.missing_hour.sum()), "trading_days": int(group.traded.sum()),
            "cumulative_profit_eur": total,
            "share_of_perfect_foresight": (total / pf_total) if pf_total != 0 else None,
            "mean_eur": float(p.mean()), "median_eur": float(np.median(p)),
            "p05_eur": float(np.percentile(p, 5)), "p95_eur": float(np.percentile(p, 95)),
            "losing_days": int(losing.sum()), "losing_share": float(losing.mean()),
            "largest_daily_loss_eur": float(-p.min()) if losing.any() else 0.0,
            "max_drawdown_eur": max_drawdown(p),
            "bought_mwh": float(group.bought_mwh.sum()), "sold_mwh": float(group.sold_mwh.sum()),
            "discharged_battery_mwh": float(group.discharged_battery_mwh.sum()),
            "full_cycles": float(group.discharged_battery_mwh.sum() / B.CYCLE_MWH)}


def summaries(daily: pd.DataFrame) -> pd.DataFrame:
    """Every measure per population, scope (all or a regime), source, rule and wear, from the daily rows alone."""
    out = []
    for population in ("P-all", "P-v5"):
        rows = daily if population == "P-all" else daily.loc[daily.in_p_v5]
        for scope in ("all",) + tuple(name for name, _, _ in I.REGIMES):
            part = rows if scope == "all" else rows.loc[rows.regime == scope]
            for wear in B.WEARS:
                at = part.loc[part.wear_eur_per_mwh == wear]
                pf_total = float(at.loc[at.source == "perfect_foresight", "profit_eur"].sum())
                for source, rules in RULES.items():
                    if source == "v5" and population == "P-all":
                        continue                  # contract §4: v5 on P-v5 only, the days where its forecasts exist
                    for rule, _, _ in rules:
                        group = at.loc[(at.source == source) & (at.rule == rule)]
                        if group.empty:
                            continue
                        out.append({"population": population, "scope": scope, "source": source, "rule": rule,
                                    "wear_eur_per_mwh": wear, **measures(group, pf_total)})
    return pd.DataFrame(out)


def paired(daily: pd.DataFrame) -> pd.DataFrame:
    """v6 minus a benchmark, day by day, with the 95% interval of the mean daily difference and of the total from a
    paired non-circular moving-block bootstrap over days (14-day blocks, 2,000 replicates; one generator, seeded once,
    drawn in the order of `B.WEARS` then `PAIRS`)."""
    from delu_forecast.final_candidate import BOOT_BLOCK, BOOT_REPLICATES, _block_means

    assert (BOOT_BLOCK, BOOT_REPLICATES) == (14, 2000)
    rng = np.random.default_rng(BOOT_SEED)
    out = []
    for wear in B.WEARS:
        at = daily.loc[daily.wear_eur_per_mwh == wear]
        for population, rule, source, minus in PAIRS:
            rows = at if population == "P-all" else at.loc[at.in_p_v5]
            a = rows.loc[(rows.source == source) & (rows.rule == rule)].set_index("day").profit_eur
            b = rows.loc[(rows.source == minus) & (rows.rule == rule)].set_index("day").profit_eur
            if list(a.index) != list(b.index):
                raise ValueError(f"{population} {source} - {minus}: the days differ")
            diff = (a - b).sort_index().to_numpy(float)
            means = _block_means(diff[:, None], rng)[:, 0]
            n = len(diff)
            lo, hi = np.quantile(means, [0.025, 0.975])
            out.append({"population": population, "rule": rule, "source": source, "minus": minus,
                        "wear_eur_per_mwh": wear, "days": n, "mean_difference_eur": float(diff.mean()),
                        "mean_ci_lower": float(lo), "mean_ci_upper": float(hi),
                        "total_difference_eur": float(diff.sum()), "total_ci_lower": float(lo * n),
                        "total_ci_upper": float(hi * n), "block_days": BOOT_BLOCK, "replicates": BOOT_REPLICATES,
                        "seed": BOOT_SEED})
    return pd.DataFrame(out)


# ------------------------------------------------------------------------------------------------- checks (before)

def checks(days: dict[str, I.Day], root: Path = I.ROOT) -> dict:
    """The brief's outcome 2, before any result: the naive's parity, the populations, the brute force on a sample, and
    (filled from the daily rows) perfect foresight never negative and every schedule within the limits."""
    import struct

    record = json.loads((root / "reports/rebaseline/cold-rerun-2026-10-15/parity.json").read_text())
    naive = I.naive_central(root)
    parity = []
    for check in record["checks"]:
        if check.get("name") != "B0":
            continue
        committed = np.array([struct.unpack(">d", bytes.fromhex(b))[0] for b in check["actual_float64_bits"]])
        stamps = pd.DatetimeIndex(check["actual_timestamp_utc"]).tz_convert("UTC")
        ours = naive.reindex(stamps).to_numpy(float)
        parity.append({"day": check["day"], "path": check["path"], "hours": len(committed),
                       "bitwise_equal": bool(np.array_equal(ours, committed))})
    # A supplementary check, beside CP-26's: the frozen package's B0 (CP-17's, the same frozen rule), whose issued central
    # vector CP-18b's committed dry run records by its SHA-256 for five development days.
    from cp17.dailyfit import array_hash

    package = []
    for record_path in sorted((root / "reports/cp18b/dryrun/store/issued").glob("*/record.json")):
        shadow = json.loads(record_path.read_text())["shadows"]["B0"]
        day = record_path.parent.name
        package.append({"day": day, "equal": array_hash(days[day].sources["naive"]["q50"]) == shadow["central_sha256"]})
    pops = I.populations(root)
    brute = []
    for day in sorted(days)[::BRUTE_EVERY]:
        data = days[day]
        for source, rules in RULES.items():
            if source not in data.sources:
                continue
            for rule, buy_q, sell_q in rules:
                buy, sell = data.sources[source][buy_q], data.sources[source][sell_q]
                if np.isnan(buy).any() or np.isnan(sell).any():
                    continue
                s = B.plan(buy, sell, B.WEARS[0], SPEC)
                grid = B.brute_force(buy, sell, B.WEARS[0], SPEC, BRUTE_STEP)
                brute.append({"day": day, "source": source, "rule": rule, "solver_eur": s.value,
                              "brute_force_eur": grid, "brute_force_better": grid > s.value + B.TOL["value"]})
    return {"naive_parity_with_cp26_b0": {"record": "reports/rebaseline/cold-rerun-2026-10-15/parity.json",
                                          "days": parity, "all_bitwise_equal": all(p["bitwise_equal"] for p in parity)},
            "naive_against_the_frozen_package_b0": {"record": "reports/cp18b/dryrun/store/issued/*/record.json "
                                                               "(shadows.B0.central_sha256)",
                                                     "days": package, "all_equal": all(x["equal"] for x in package)},
            "populations": {name: len(v) for name, v in pops.items()},
            "brute_force": {"rule": f"every {BRUTE_EVERY}th day of P-all from the first; grid step {BRUTE_STEP} MWh; "
                                    f"wear {B.WEARS[0]}", "solves": len(brute),
                            "solver_never_beaten": not any(b["brute_force_better"] for b in brute),
                            "largest_solver_margin_eur": max(b["solver_eur"] - b["brute_force_eur"] for b in brute),
                            "rows": brute}}


def after_checks(daily: pd.DataFrame) -> dict:
    pf = daily.loc[daily.source == "perfect_foresight", "profit_eur"]
    return {"perfect_foresight_never_negative": bool((pf >= -B.TOL["value"]).all()),
            "perfect_foresight_min_eur": float(pf.min()),
            "every_schedule_within_the_limits": True,     # `daily_rows` raises on any violation
            "tie_break_fallbacks": int(daily.tie_break_fallbacks.sum()),
            "rows_with_a_fallback": int((daily.tie_break_fallbacks > 0).sum()),
            "rows": len(daily)}


# ------------------------------------------------------------------------------------------------------- outputs

def summary_files(daily: pd.DataFrame) -> dict[str, str]:
    return {"summary.csv": _csv(summaries(daily)), "paired.csv": _csv(paired(daily))}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true", help="re-derive the summaries from the committed daily rows")
    ap.add_argument("--summaries", action="store_true", help="rewrite the summaries from the committed daily rows")
    args = ap.parse_args(argv)
    root = I.ROOT
    out = root / OUT
    if args.summaries:
        daily = pd.read_csv(out / "daily.csv", dtype={"day": str})
        for name, text in summary_files(daily).items():
            (out / name).write_text(text)
        print(json.dumps({"wrote": sorted(summary_files(daily))}))
        return 0
    if args.check:
        daily = pd.read_csv(out / "daily.csv", dtype={"day": str})
        files = summary_files(daily)
        same = {name: (out / name).read_text() == text for name, text in files.items()}
        print(json.dumps({"identical_to_committed": same}, sort_keys=True))
        return 0 if all(same.values()) else 12
    days = I.load_days(root)
    p_v5 = set(I.populations(root)["P-v5"])
    pre = checks(days, root)
    if not (pre["naive_parity_with_cp26_b0"]["all_bitwise_equal"] and pre["naive_against_the_frozen_package_b0"]["all_equal"]
            and pre["brute_force"]["solver_never_beaten"]
            and pre["populations"] == {"P-all": I.P_ALL_DAYS, "P-v5": I.P_V5_DAYS}):
        print(json.dumps(pre, indent=1, default=str)[:4000])
        raise SystemExit("a check before the results failed: nothing is written")
    daily = daily_rows(days, p_v5)
    post = after_checks(daily)
    out.mkdir(parents=True, exist_ok=True)
    (out / "daily.csv").write_text(_csv(daily))
    daily = pd.read_csv(out / "daily.csv", dtype={"day": str})     # the summaries are derived from the file itself
    for name, text in summary_files(daily).items():
        (out / name).write_text(text)
    (out / "checks.json").write_text(json.dumps({**pre, "after": post, "spec": SPEC.__dict__, "tolerances": B.TOL,
                                                 "inputs_sha256": I.check_pins(root)}, indent=1, sort_keys=True,
                                                default=str) + "\n")
    print(json.dumps({"wrote": sorted(p.name for p in out.iterdir()), "rows": len(daily)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
