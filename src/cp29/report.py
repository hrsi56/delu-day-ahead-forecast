"""`reports/cp29/report.md`, written from the committed records alone: every number is read from `summary.csv`,
`paired.csv` and `checks.json`, never typed.

    uv run python -m cp29.report            # write the report
    uv run python -m cp29.report --check    # compare with the committed report; write nothing
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import pandas as pd

from cp29 import battery as B
from cp29 import inputs as I

OUT = Path("reports/cp29")
NAMES = {("v6", "median"): "v6, median rule", ("v6", "risk"): "v6, risk-aware variant",
         ("naive", "median"): "Similar-day naive, median rule", ("v5", "median"): "v5, median rule",
         ("v5", "risk"): "v5, risk-aware variant", ("perfect_foresight", "perfect"): "Perfect foresight (the ceiling)"}
REGIME_NAMES = {"all": "All days", "pre_crisis": "Before the crisis (to 2021-08-31)",
                "crisis": "The crisis (2021-09-01 to 2022-12-31)", "negative_prices": "From 2023-01-01"}


def eur(x: float, places: int = 0) -> str:
    s = f"{abs(x):,.{places}f}"
    return ("−" if x < 0 and float(s.replace(",", "")) != 0 else "") + s


def signed(x: float, places: int = 0) -> str:
    return ("+" if x > 0 else "") + eur(x, places)


def share(x) -> str:
    return "undefined" if x is None or (isinstance(x, float) and pd.isna(x)) else f"{100 * float(x):.1f}%"


def _rows(summary: pd.DataFrame, population: str, scope: str, wear: float) -> pd.DataFrame:
    return summary.loc[(summary.population == population) & (summary.scope == scope)
                       & (summary.wear_eur_per_mwh == wear)]


def main_table(summary: pd.DataFrame, population: str) -> list[str]:
    out = ["| Source and rule | Cumulative net profit, EUR | Share of perfect foresight | Trading days | Losing days "
           "| Largest daily loss, EUR | Maximum drawdown, EUR | Mean / median daily profit, EUR | 5th–95th percentile, "
           "EUR | Discharged from the battery, MWh (full cycles) |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in _rows(summary, population, "all", B.WEARS[0]).iterrows():
        out.append(f"| {NAMES[(r.source, r.rule)]} | {eur(r.cumulative_profit_eur)} | {share(r.share_of_perfect_foresight)} "
                   f"| {int(r.trading_days):,} of {int(r.days):,} | {int(r.losing_days):,} ({share(r.losing_share)}) "
                   f"| {eur(r.largest_daily_loss_eur)} | {eur(r.max_drawdown_eur)} | {eur(r.mean_eur, 1)} / "
                   f"{eur(r.median_eur, 1)} | {eur(r.p05_eur, 1)} to {eur(r.p95_eur, 1)} "
                   f"| {eur(r.discharged_battery_mwh)} ({eur(r.full_cycles)}) |")
    return out


def wear_table(summary: pd.DataFrame, population: str) -> list[str]:
    out = ["| Source and rule | " + " | ".join(f"€{w:g} per MWh: profit, EUR (share)" for w in sorted(B.WEARS)) + " |",
           "|---|" + "---|" * len(B.WEARS)]
    main = _rows(summary, population, "all", B.WEARS[0])
    for _, r in main.iterrows():
        cells = []
        for w in sorted(B.WEARS):
            x = _rows(summary, population, "all", w)
            x = x.loc[(x.source == r.source) & (x.rule == r.rule)].iloc[0]
            cells.append(f"{eur(x.cumulative_profit_eur)} ({share(x.share_of_perfect_foresight)})")
        out.append(f"| {NAMES[(r.source, r.rule)]} | " + " | ".join(cells) + " |")
    return out


def regime_table(summary: pd.DataFrame, population: str) -> list[str]:
    scopes = ["all"] + [name for name, _, _ in I.REGIMES]
    main = _rows(summary, population, "all", B.WEARS[0])
    out = ["| Source and rule | " + " | ".join(REGIME_NAMES[s] for s in scopes) + " |", "|---|" + "---|" * len(scopes)]
    days = [int(_rows(summary, population, s, B.WEARS[0]).days.iloc[0]) for s in scopes]
    out.append("| Days | " + " | ".join(f"{d:,}" for d in days) + " |")
    for _, r in main.iterrows():
        cells = []
        for s in scopes:
            x = _rows(summary, population, s, B.WEARS[0])
            x = x.loc[(x.source == r.source) & (x.rule == r.rule)].iloc[0]
            cells.append(f"{eur(x.cumulative_profit_eur)} ({share(x.share_of_perfect_foresight)})")
        out.append(f"| {NAMES[(r.source, r.rule)]} | " + " | ".join(cells) + " |")
    return out


def paired_table(paired: pd.DataFrame) -> list[str]:
    out = ["| Population | Rule | Difference | Wear, €/MWh | Days | Mean daily difference, EUR [95% interval] | Total "
           "difference, EUR [95% interval] |", "|---|---|---|---|---|---|---|"]
    for _, r in paired.iterrows():
        out.append(f"| {r.population} | {'median' if r.rule == 'median' else 'risk-aware'} | {r.source} − {r.minus} "
                   f"| {r.wear_eur_per_mwh:g} | {int(r.days):,} | {signed(r.mean_difference_eur, 1)} "
                   f"[{signed(r.mean_ci_lower, 1)}, {signed(r.mean_ci_upper, 1)}] | {signed(r.total_difference_eur)} "
                   f"[{signed(r.total_ci_lower)}, {signed(r.total_ci_upper)}] |")
    return out


def build(root: Path = I.ROOT) -> str:
    out = root / OUT
    summary = pd.read_csv(out / "summary.csv")
    paired = pd.read_csv(out / "paired.csv")
    checks = json.loads((out / "checks.json").read_text())
    daily = pd.read_csv(out / "daily.csv", dtype={"day": str}, usecols=["source", "rule", "wear_eur_per_mwh",
                                                                         "missing_hour", "day"])
    missing = daily.loc[daily.missing_hour & (daily.wear_eur_per_mwh == B.WEARS[0])].groupby("source").day.nunique()
    after = checks["after"]
    lines = [
        "# CP-29: battery arbitrage on the development forecasts",
        "",
        "**Simulated, development, post-selection.** A simulation of a price-taking battery on the development days, "
        "under the Owner's approved economic-policy contract (`docs/track-b/economic-policy-contract-2026-11-15.md`, "
        "decision 32). No money was traded. v6 was selected on these same days (CP-28), so its result is optimistic for "
        "v6. The rules this round fixed before any number are in `docs/track-b/evidence/cp-29/publication-packet.md` §0.",
        "",
        "## What was evaluated",
        "",
        "- **The battery:** 1 MW at the grid, 2 MWh usable, 85% round trip (√0.85 on charge and on discharge), empty at "
        "the start and the end of each delivery day, at most 2 MWh leaving its terminals a day, and charging or "
        "discharging in an hour, never both.",
        "- **The costs:** wear of €25 per MWh leaving the battery's terminals (with €0 and €50 as sensitivity), and an "
        "exchange fee of €0.10 per MWh bought and per MWh sold. No grid fees, under the German storage exemption.",
        "- **The rule:** on the day before, the schedule that maximizes the forecast's net value (median rule: the "
        "forecast median as the price; risk-aware variant: buy at the 75th percentile, sell at the 25th). If that value "
        "is not above zero, the battery does nothing. The schedule is then settled at the cleared day-ahead prices, "
        "with the same costs.",
        "- **The sources:** v6 (CP-28's stored forecasts, arm A1), the similar-day naive (its frozen rule, from the "
        "committed snapshot), v5 (CP-24's committed predictions, only on P-v5) and perfect foresight (the cleared "
        "prices themselves: the ceiling).",
        f"- **The populations:** P-all, every eligible development day from 2020-12-29 to 2026-09-06 "
        f"({checks['populations']['P-all']:,} days), and P-v5, the {checks['populations']['P-v5']:,} days of v5's "
        "test periods 2–5 inside it.",
        "",
        "## Checks run before the results",
        "",
        f"- **The naive's parity:** its central vector equals CP-26's B0 central vector bit for bit wherever a "
        f"committed record holds it ({sum(d['bitwise_equal'] for d in checks['naive_parity_with_cp26_b0']['days'])} "
        f"of {len(checks['naive_parity_with_cp26_b0']['days'])} records), and the frozen package's issued B0 central "
        f"vector on {sum(d['equal'] for d in checks['naive_against_the_frozen_package_b0']['days'])} further days.",
        f"- **The solver against a brute force:** on {checks['brute_force']['solves']} sampled day-source-rule "
        "programmes, an exhaustive search over a grid of schedules never beat the solver "
        f"({'none did' if checks['brute_force']['solver_never_beaten'] else 'ONE DID'}).",
        f"- **The limits:** every one of the {after['rows']:,} daily schedules meets every limit; perfect foresight is "
        f"never negative on a day (its lowest day: {eur(after['perfect_foresight_min_eur'], 2)} EUR).",
        f"- **The tie-break:** {after['tie_break_fallbacks']} tie-break solves fell back to the previous stage "
        f"({after['rows_with_a_fallback']} rows), as §0 provides.",
        "- **Days not traded because an hour is missing** (contract §5: kept, counted, profit zero): "
        + ", ".join(f"{src} {int(n)}" for src, n in missing.items()) + ".",
        "",
        "## Results on P-all, at the main wear cost (€25 per MWh)",
        "",
        *main_table(summary, "P-all"),
        "",
        "## Results on P-v5, at the main wear cost",
        "",
        *main_table(summary, "P-v5"),
        "",
        "## The wear cost's sensitivity",
        "",
        "P-all:",
        "",
        *wear_table(summary, "P-all"),
        "",
        "P-v5:",
        "",
        *wear_table(summary, "P-v5"),
        "",
        "## By regime (P-all, €25): cumulative profit, EUR (share of perfect foresight)",
        "",
        *regime_table(summary, "P-all"),
        "",
        "## Paired differences, with their uncertainty",
        "",
        "Day by day on the same days; the 95% interval from a paired non-circular moving-block bootstrap over days "
        "(14-day blocks, 2,000 replicates, seed 20261115). The interval describes how the difference varies across "
        "resampled blocks of these development days; it is not a forecast for other days.",
        "",
        *paired_table(paired),
        "",
        "## Disclosures (contract §8)",
        "",
        "- **A price-taker:** every schedule is filled at the cleared price, with no effect on it.",
        "- **Day-ahead only:** no intraday re-trading, balancing energy or ancillary services. These are a large share "
        "of German batteries' revenue in practice, so this measures only the day-ahead arbitrage value of the forecast, "
        "not a battery's total income.",
        "- **No outages,** no imbalance and no forecast failure: the schedule is executed exactly.",
        "- **Costs:** only those above. The wear cost and the exchange fee are stated assumptions; the grid-fee "
        "exemption is a legal assumption that may change.",
        "- **Hourly, not quarter-hourly:** since 1 October 2025 the market clears in quarter-hours; the hourly price is "
        "their average, and a schedule flat within each hour settles exactly at it.",
        "- **Post-selection:** v6 was selected on these days, so its result is optimistic for v6.",
        "- **Simulated, not realized:** no money was traded.",
        "",
        "## What it does not claim (contract §9)",
        "",
        "- Not a trading recommendation, an investment case or a forecast of future profit.",
        "- Not realized income.",
        "- Not a property of v6 alone: the result depends on the battery, the costs and the rule stated here.",
        "- Not 4.7T's result, and not a test of v6.",
        "",
        "No annualized return, internal rate of return, payback or business case is reported: there is no capital cost "
        "model. Forecast error and interval coverage are not profit.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    text = build()
    path = I.ROOT / OUT / "report.md"
    if args.check:
        same = path.read_text() == text
        print(json.dumps({"identical_to_committed": same}))
        return 0 if same else 12
    path.write_text(text)
    print(json.dumps({"wrote": str(path.relative_to(I.ROOT))}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
