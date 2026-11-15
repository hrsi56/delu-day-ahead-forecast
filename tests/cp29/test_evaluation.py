"""CP-29's committed evaluation (`reports/cp29/`): the records re-derive from the daily rows, the checks before the
results hold, the contract's populations and sources are exactly the ones computed, and nothing else is."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from cp29 import battery as B
from cp29 import evaluate as E
from cp29 import inputs as I
from cp29 import report as RP

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / E.OUT


@pytest.fixture(scope="module")
def daily() -> pd.DataFrame:
    return pd.read_csv(OUT / "daily.csv", dtype={"day": str})


def test_the_summaries_and_the_report_rederive_from_the_daily_rows(daily):
    for name, text in E.summary_files(daily).items():
        assert (OUT / name).read_text() == text, name
    assert (OUT / "report.md").read_text() == RP.build(ROOT)


def test_the_checks_before_the_results_passed():
    c = json.loads((OUT / "checks.json").read_text())
    assert c["naive_parity_with_cp26_b0"]["all_bitwise_equal"] and len(c["naive_parity_with_cp26_b0"]["days"]) == 8
    assert c["naive_against_the_frozen_package_b0"]["all_equal"] and len(c["naive_against_the_frozen_package_b0"]["days"]) == 5
    assert c["populations"] == {"P-all": 2068, "P-v5": 358}
    assert c["brute_force"]["solver_never_beaten"] and c["brute_force"]["solves"] > 100
    assert c["after"]["perfect_foresight_never_negative"] and c["after"]["every_schedule_within_the_limits"]
    assert c["spec"] == {"exclusive": True, "wear_on_battery": True}     # O58
    assert c["inputs_sha256"] == I.PINNED


def test_exactly_the_contracts_rows(daily):
    keys = set(map(tuple, daily[["source", "rule"]].drop_duplicates().to_numpy()))
    assert keys == {("v6", "median"), ("v6", "risk"), ("naive", "median"), ("v5", "median"), ("v5", "risk"),
                    ("perfect_foresight", "perfect")}
    assert sorted(daily.wear_eur_per_mwh.unique()) == [0.0, 25.0, 50.0]
    per_day = daily.groupby("day").size()
    assert len(per_day) == 2068 and daily.day.max() <= "2026-09-06" and daily.day.min() == "2020-12-29"
    v5_days = set(daily.loc[daily.source == "v5", "day"])
    assert len(v5_days) == 358 and v5_days == set(daily.loc[daily.in_p_v5, "day"])
    assert len(daily) == (2068 * 4 + 358 * 2) * 3
    assert (daily.evidence_class == "simulated, development, post-selection").all()


def test_missing_hours_are_kept_counted_and_never_traded(daily):
    missing = daily.loc[daily.missing_hour]
    assert not missing.traded.any() and (missing.profit_eur == 0).all()
    counts = missing.loc[missing.wear_eur_per_mwh == 25].groupby("source").day.nunique().to_dict()
    assert counts == {"v6": 33, "naive": 11, "v5": 4}


def test_v5_is_reported_on_p_v5_only_and_shares_use_the_same_days():
    summary = pd.read_csv(OUT / "summary.csv")
    assert not ((summary.population == "P-all") & (summary.source == "v5")).any()
    for (population, scope, wear), group in summary.groupby(["population", "scope", "wear_eur_per_mwh"]):
        assert group.days.nunique() == 1, (population, scope, wear)
        pf = group.loc[group.source == "perfect_foresight"].iloc[0]
        assert pf.share_of_perfect_foresight == 1.0 and pf.losing_days == 0
        for _, row in group.iterrows():
            assert row.share_of_perfect_foresight == pytest.approx(row.cumulative_profit_eur / pf.cumulative_profit_eur)


def test_the_paired_differences_are_the_contracts(daily):
    paired = pd.read_csv(OUT / "paired.csv")
    assert list(map(tuple, paired[["population", "rule", "source", "minus"]].drop_duplicates().to_numpy())) == \
        list(E.PAIRS)
    assert set(paired.seed) == {20261115} and set(paired.block_days) == {14} and set(paired.replicates) == {2000}
    row = paired.iloc[0]
    at = daily.loc[daily.wear_eur_per_mwh == row.wear_eur_per_mwh]
    v6 = at.loc[(at.source == "v6") & (at.rule == "median")].set_index("day").profit_eur
    naive = at.loc[(at.source == "naive") & (at.rule == "median")].set_index("day").profit_eur
    assert row.total_difference_eur == pytest.approx((v6 - naive).sum())
    assert row.mean_ci_lower <= row.mean_difference_eur <= row.mean_ci_upper


def test_the_report_carries_the_contracts_disclosures_and_limits():
    text = (OUT / "report.md").read_text()
    for needed in ("Simulated, development, post-selection", "A price-taker", "Day-ahead only", "No outages",
                   "Hourly, not quarter-hourly", "Not a trading recommendation", "Not realized income",
                   "Not a property of v6 alone", "Not 4.7T's result", "No annualized return"):
        assert needed in text, needed
    for banned in ("success rate", "annualized return of", "IRR of", "payback of"):
        assert banned not in text.lower().replace("no annualized return", "")


def test_a_fresh_solve_of_sampled_days_reproduces_the_committed_rows(daily):
    """Every 250th P-all day (and every P-v5 day among them), re-solved from the pinned inputs, row for row."""
    days = I.load_days(ROOT)
    p_v5 = set(I.populations(ROOT)["P-v5"])
    sample = {day: days[day] for day in sorted(days)[::250]}
    fresh = E.daily_rows(sample, p_v5)
    committed = daily.loc[daily.day.isin(sample)].reset_index(drop=True)
    pd.testing.assert_frame_equal(fresh.reset_index(drop=True), committed, check_dtype=False, rtol=0, atol=1e-9)
