"""PRES-6: v6's product results and business insights, before the model comparison (PUBLISH_RULES A8; ruling O46).

The contracts, each with a negative control where a check could pass vacuously:

- the product results re-derive byte for byte from the three pinned inputs by the packet's §0 rules, and a changed
  input is refused (the brief's outcome 2);
- the populations agree with CP-26's and CP-28's: 2,068 eligible development days, 49,596 scored hours, the three
  regimes summing to them, and v6's and the naive's means equal to CP-26's every-day records for DDNN-2 and the naive;
- the three days are the rule's (the lower median of each regime's P-v5 days), not a choice;
- the page's order is A8's: the product opening, How the product works, Product results, Business insights, then How
  the models compare; the compact navigation leads to Product results;
- Product results binds only PRES-6's records, every graphic names its policy, population, dates, units and evidence
  class, and no live number appears;
- Business insights states the use, the measured implications and the gap, and no error or coverage figure is called a
  profit or a success rate (W54); no product result is called prospective (W55);
- the README carries the same claims (decision 30 later removed the 2.0 MB budget); R3's shared code texts carry their
  experiment.
"""
from __future__ import annotations

import csv
import html
import io
import json
import re
import sys
from pathlib import Path

import pandas as pd
import pytest

from delu_forecast import final_candidate as FC
from delu_forecast import research as R
from delu_forecast import research_claims as RC

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_pages  # noqa: E402

PAGE = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
BODY = PAGE.split("<script>")[0]
README = (ROOT / "README.md").read_text(encoding="utf-8")
OUT = ROOT / FC.PRODUCT_OUT


def _text(fragment: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", fragment))).strip()


def _rows(name: str) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO((OUT / name).read_text())))


SECTION = re.compile(r'<section\b[^>]*\bid="([^"]+)"')


def _order(page: str) -> list[str]:
    return SECTION.findall(page)


def _section(page: str, section_id: str) -> str:
    """From the section's opening tag to the next section's (each section is the page's top level)."""
    starts = [(m.group(1), m.start()) for m in SECTION.finditer(page)]
    i = next(i for i, (name, _) in enumerate(starts) if name == section_id)
    return page[starts[i][1]:starts[i + 1][1] if i + 1 < len(starts) else len(page)]


# --------------------------------------------------------------------------- the computation (outcome 2)


@pytest.fixture(scope="module")
def built() -> dict[str, str]:
    return FC.product_build(ROOT)


def test_the_product_rows_rederive_byte_for_byte(built):
    assert sorted(built) == ["bins.csv", "coverage.csv", "days.csv", "explanation.csv", "monthly.csv", "regimes.csv",
                            "summary.json"]
    for name, text in built.items():
        assert (OUT / name).read_text() == text, name


def test_a_changed_input_is_refused(monkeypatch):
    pinned = dict(FC.PRODUCT_INPUTS)
    first = next(iter(pinned))
    monkeypatch.setattr(FC, "PRODUCT_INPUTS", {**pinned, first: "0" * 64})
    with pytest.raises(ValueError, match="is not the pinned"):
        FC.product_build(ROOT)


def test_the_rules_are_the_packets():
    summary = json.loads((OUT / "summary.json").read_text())
    assert summary["bootstrap"] == {"block_days": 14, "interval": "percentile, 2.5% and 97.5%",
                                    "kind": "non-circular moving block, paired",
                                    "order": ["all", "pre_crisis", "crisis", "negative_prices"],
                                    "replicates": 2000, "seed": 20261114}
    assert summary["evidence_class"] == "development_post_selection"
    assert summary["inputs_sha256"] == FC.PRODUCT_INPUTS
    packet = (ROOT / "docs/track-b/evidence/pres-6/publication-packet.md").read_text()
    for rule in ("blocks of 14 consecutive days, 2,000 replicates, seed 20261114", "lower of the two middle days",
                 "ten bins of equal count", "calendar-month means"):
        assert rule in " ".join(packet.split()), rule


# --------------------------------------------------------------------------- the populations


def test_the_populations_agree_with_cp26_and_cp28():
    summary = json.loads((OUT / "summary.json").read_text())
    assert summary["p_all"] == {"days": 2068, "first_day": "2020-12-29", "hours": 49596, "last_day": "2026-09-06"}
    assert summary["p_v5"]["days"] == 358 and summary["p_v5"]["hours"] == 8587
    regimes = {(r["regime"], r["metric"], r["stream"]): r for r in _rows("regimes.csv")}
    days = {name: int(regimes[(name, "MAE", "v6")]["days"]) for name in ("pre_crisis", "crisis", "negative_prices")}
    hours = {name: int(regimes[(name, "MAE", "v6")]["hours"]) for name in days}
    assert days == {"pre_crisis": 246, "crisis": 481, "negative_prices": 1341} and sum(days.values()) == 2068
    assert sum(hours.values()) == int(regimes[("all", "MAE", "v6")]["hours"]) == 49596
    # CP-26's every-day records: DDNN-2 (D2) is v6's policy, B0 the naive; the means are the same numbers
    for metric in ("MAE", "WIS"):
        for stream, cp26 in (("v6", "D2"), ("naive", "B0")):
            ours = float(regimes[("all", metric, stream)]["value"])
            theirs = float(R.get(f"cp26.every.nominal.{cp26}.all_eligible.{metric}.raw_mean_daily_loss").raw)
            assert abs(ours - theirs) < 1e-9, (metric, stream, ours, theirs)
    assert "2,068" in R.POPULATIONS["cp26-every-day"]


def test_the_three_days_are_the_rules():
    """Re-chosen here from CP-28's committed daily losses, independently of `product_days`."""
    daily = pd.read_parquet(ROOT / "reports/cp28/results/daily-losses.parquet")
    mae = daily[daily.stream == "A1"].set_index("day").MAE
    p_v5 = sorted(set(FC._p_v5_hours(ROOT).day))
    summary = json.loads((OUT / "summary.json").read_text())
    upper_differs = False
    for (name, lo, hi), chosen in zip(FC.REGIMES, summary["chosen_days"]):
        ranked = sorted((d for d in p_v5 if lo <= d <= hi), key=lambda d: (float(mae.loc[d]), d))
        assert chosen["regime"] == name and chosen["days_in_regime"] == len(ranked)
        assert chosen["day"] == ranked[(len(ranked) - 1) // 2], name  # the lower median
        upper_differs |= ranked[len(ranked) // 2] != chosen["day"]
    assert upper_differs  # the rule is not vacuous: the upper median would have chosen another day
    assert [c["day"] for c in summary["chosen_days"]] == ["2021-06-16", "2022-07-26", "2025-05-02"]
    days = _rows("days.csv")
    assert len(days) == 72 and {r["day"] for r in days} == {"2021-06-16", "2022-07-26", "2025-05-02"}
    assert all(float(r["p025"]) <= float(r["p10"]) <= float(r["p25"]) <= float(r["p50"]) <= float(r["p75"])
               <= float(r["p90"]) <= float(r["p975"]) for r in days)


# --------------------------------------------------------------------------- the findings the page states


def test_v6_is_below_the_naive_in_every_month():
    rows = _rows("monthly.csv")
    months = sorted({r["month"] for r in rows})
    assert len(months) == 70 and months[0] == "2020-12" and months[-1] == "2026-09"
    by = {(r["month"], r["stream"]): r for r in rows}
    assert sum(int(by[(m, "v6")]["days"]) for m in months) == 2068
    for month in months:
        for metric in ("MAE", "WIS"):
            assert float(by[(month, "v6")][metric]) < float(by[(month, "naive")][metric]), (month, metric)


def test_every_regime_ratio_and_its_interval_lie_below_one():
    for row in _rows("regimes.csv"):
        value, low, high = float(row["value"]), float(row["ci_lower"]), float(row["ci_upper"])
        assert low <= value <= high, row
        assert int(row["days"]) >= 60  # none is thin
        if row["stream"] == "ratio":
            assert high < 1, row


def test_coverage_is_v6s_with_width_at_each_level():
    rows = _rows("coverage.csv")
    assert {r["stream"] for r in rows} == {"v6"}  # the naive's daily rows carry no coverage (§0's correction)
    assert {(r["regime"], r["level"]) for r in rows} == {(g, lv) for g in ("all", "pre_crisis", "crisis",
                                                                          "negative_prices") for lv in ("50", "80", "95")}
    for regime in ("all", "pre_crisis", "crisis", "negative_prices"):
        levels = sorted((int(r["level"]), float(r["coverage"]), float(r["width_eur"])) for r in rows
                        if r["regime"] == regime)
        assert [c for _, c, _ in levels] == sorted(c for _, c, _ in levels)
        assert [w for _, _, w in levels] == sorted(w for _, _, w in levels)


def test_the_bins_hold_every_p_v5_hour_in_ten_equal_bins():
    rows = _rows("bins.csv")
    counts = [int(r["hours"]) for r in rows]
    assert len(rows) == 10 and sum(counts) == 8587 and max(counts) - min(counts) <= 1
    inside = [float(r["inside80"]) for r in rows]
    assert f"{min(inside):.4f}" == "0.6868" and f"{max(inside):.4f}" == "0.8685"


def test_every_pres6_record_rederives_and_a_perturbed_one_fails():
    pres6 = [record for record_id, record in R.records().items() if record_id.startswith("pres6.")]
    assert len(pres6) > 400
    assert R.validate_all(pres6) == []
    record = R.get("pres6.regime.all.MAE.ratio")
    bad = R.EvidenceRecord(**{**record.__dict__, "raw": "0.51"})
    assert any("committed value" in problem for problem in R.validate_all([bad]))
    for record in pres6:
        assert record.window is None or record.window[1] <= R.RESEARCH_BOUNDARY, record.record_id


# --------------------------------------------------------------------------- the page (outcomes 1 and 3; A8)


def test_the_order_is_a8s_product_first():
    order = _order(BODY)
    assert order[:5] == ["top", "product", "outcomes", "business", "research-results"], order[:6]
    for heading, text in (("product-h", "How the product works"), ("outcomes-h", "Product results"),
                          ("business-h", "Business insights"), ("results-h", "How the models compare")):
        assert _text(re.search(rf'id="{heading}"[^>]*>(.*?)</h2>', BODY, re.S).group(1)) == text
    nav = re.search(r"<nav\b.*?</nav>", BODY, re.S).group(0)
    assert re.findall(r'href="(#[^"]+)"', nav)[0] == "#outcomes"
    # the negative control: the PRES-5 order (the comparison before the product's results) is caught
    old = BODY.replace('id="outcomes"', 'id="tmp-o"', 1).replace('id="research-results"', 'id="outcomes"', 1).replace(
        'id="tmp-o"', 'id="research-results"', 1)
    assert _order(old)[:5] != ["top", "product", "outcomes", "business", "research-results"]


def _foreign(section: str, prefixes: tuple[str, ...] = ("pres6.",)) -> list[str]:
    """What does not belong in a PRES-6 section: a record not PRES-6's (or, in Business insights since PRES-7, not
    CP-29's) or unknown, a live record, a raw value shown unrounded."""
    problems = [f"record {record_id}" for record_id in re.findall(r'data-record="([^"]+)"', section)
                if not record_id.startswith(prefixes) or record_id not in R.records()]
    visible = _text(re.sub(r"<svg.*?</svg>", "", re.sub(r"<data [^>]*>", "", section), flags=re.S))
    return problems + [f"unrounded {value}" for value in re.findall(r"\d+\.\d{6,}", visible)]


def test_product_results_binds_only_pres6_records_and_shows_no_live_number():
    assert _foreign(_section(BODY, "outcomes")) == []
    # PRES-7: Business insights renders CP-29's evaluation (decision 32) beside PRES-6's measured implications
    assert _foreign(_section(BODY, "business"), ("pres6.", "cp29.")) == []
    assert _foreign(_section(BODY, "outcomes") + '<span data-record="cp29.p_all.all.v6.median.w25.days">2,068</span>')
    bound = re.findall(r'data-record="([^"]+)"', _section(BODY, "outcomes"))
    assert len(bound) > 200 and not any(record_id.startswith("live") for record_id in bound)


def test_negative_control_another_tables_values_are_caught():
    # the defect the candidate first carried: v1's stratum table rendered inside Product results under a name clash
    v1_table = build_pages.regime_table()
    assert "released recipe" in v1_table and "released recipe" not in _section(BODY, "outcomes")
    assert _foreign(_section(BODY, "outcomes") + v1_table)
    assert build_pages.outcome_regime_table() in _section(BODY, "outcomes")


def test_each_graphic_names_policy_population_dates_units_and_class():
    section = _section(BODY, "outcomes")
    charts = re.findall(r'data-chart-id="(outcomes-[a-z]+-chart)"', section)
    assert charts == ["outcomes-days-chart", "outcomes-time-chart", "outcomes-regimes-chart", "outcomes-coverage-chart",
                      "outcomes-explanation-chart"]
    identity = _text(section[:section.index('data-chart-id="outcomes-days-chart"')])
    for needed in ("v6 · DDNN-2 alone", "A1", "every eligible development day", "2020-12-29 to 2026-09-06",
                   "EUR/MWh", "development, post-selection"):
        assert needed in identity, needed
    detail = _text(section)
    for needed in ("2021-06-16", "2022-07-26", "2025-05-02", "2020-12", "2026-09", "246 days", "481", "1,341"):
        assert needed in detail, needed


def test_the_product_finding_is_v6s_development_result():
    finding = re.search(r'<h3 [^>]*id="product-finding"[^>]*>.*?</h3>', BODY, re.S).group(0)
    records = re.findall(r'data-record="([^"]+)"', finding)
    for needed in ("pres6.p_all.days", "pres6.regime.all.MAE.v6", "pres6.regime.all.MAE.naive"):
        assert needed in records, needed
    text = _text(finding)
    assert "2,068" in text and "17.2 EUR/MWh" in text and "34.6" in text
    # coverage only with its width, on the line directly below the finding (editorial review E3; P68)
    after = BODY[BODY.index(finding) + len(finding):]
    coverage = re.match(r'\s*<p [^>]*data-block="outcomes.finding.coverage"[^>]*>.*?</p>', after, re.S)
    assert coverage and "51.7 EUR/MWh wide on average" in _text(coverage.group(0)) and "0.7826" in _text(coverage.group(0))
    caveat = _text(_section(BODY, "outcomes"))
    assert "Development evidence after selection" in caveat and "prospective evaluation in progress" in caveat


def test_business_insights_states_the_use_the_implications_and_the_gap():
    text = _text(_section(BODY, "business"))
    for needed in ("12:00 auction", "bidding, scheduling and hedging", "17.2", "34.6", "51.7", "0.7826",
                   "not profit, and not a success rate"):
        assert needed in text, needed
    # PRES-7 replaced the gap (CP-29's open item 4): an evaluation now exists, so the section says what is still not
    # evaluated; its profit chart and claims are tests/test_52_pres7_business_insights.py's
    assert "What is still not evaluated" in text
    for gone in ("No decision policy, cost model or trading simulation has been authorized or run",
                 "no profit, value or loss figure"):
        assert gone not in text and gone not in README, gone


def test_the_withheld_claims_w54_and_w55_are_guarded():
    for claim in ("The lower error is a profit", "its coverage equals a success rate",
                  "the product results are prospective", "These results were live"):
        assert RC.withheld_findings(claim), claim
    # PRES-7 (O60): W54 keeps only its "error or coverage called a profit" half; a labelled simulated profit is published
    for claim in ("a profit of 3", "a profit curve of 12"):
        assert not [h for h in RC.withheld_findings(claim) if h.split(":")[0] == "W54"], claim
    for allowed in ("Lower forecast error and interval coverage are not profit, and not a success rate.",
                    "These are development results after selection.", "there is no profit, value or loss figure"):
        assert not [h for h in RC.withheld_findings(allowed) if h.split(":")[0] in ("W54", "W55")], allowed
    for surface in (_text(BODY), README):
        assert not [hit for hit in RC.withheld_findings(surface) if hit.split(":")[0] in ("W54", "W55")]


def test_the_readme_carries_the_same_claims():
    product = next(line for line in README.splitlines() if line.startswith("**Product results:**"))
    business = next(line for line in README.splitlines() if line.startswith("**Business insights:**"))
    for key in ("outcomes.finding", "outcomes.finding.coverage", "outcomes.caveat"):
        assert RC.render(key, "md", surface=RC.README) in product, key
    page = _text(re.search(r'<h3 [^>]*id="product-finding"[^>]*>.*?</h3>', BODY, re.S).group(0))
    numbers = re.findall(r"\d[\d,]*\.?\d*", page)
    assert numbers == re.findall(r"\d[\d,]*\.?\d*", RC.render("outcomes.finding", "md", surface=RC.README))
    assert "#outcomes" in product and "prospective evaluation in progress" in product
    assert "What is still not evaluated" in business and "not a success rate" in business
    assert README.index("**Product results:**") < README.index("**Business insights:**")


def test_r3_a_shared_code_text_carries_its_experiment():
    table = build_pages.overview_table()
    codes = [_text(c) for c in re.findall(r'<span class="code">(.*?)</span>', table, re.S)]
    assert len(codes) == len(set(codes)), codes  # no two rows show the same code
    assert any(code.startswith("A1, ") for code in codes)


# --------------------------------------------------------------------------- the explanation (§0's correction; O49 superseded)


def test_the_explanation_is_the_probes_committed_attribution_of_v6s_stored_fits():
    """The cited result's fits are v6's stored forecasts: the probe's quantiles equal CP-28's arm A1 rows exactly."""
    probe = json.loads((ROOT / FC.EXPLAIN_SOURCE).read_text())["results"]
    hourly = pd.read_parquet(ROOT / "reports/cp28/forecast/hourly.parquet")
    for day in FC.EXPLAIN_DAYS:
        assert day <= "2026-09-06"  # r20 §24.14: development displays only
        stored = hourly[(hourly.arm == "A1") & (hourly.day.astype(str) == day)].sort_values("timestamp_utc")
        quantiles = stored[["q025", "q10", "q25", "q50", "q75", "q90", "q975"]].to_numpy(float).tolist()
        assert quantiles == probe[f"A1-{day}"]["quantiles"], day
    assert FC.PRODUCT_INPUTS[FC.EXPLAIN_SOURCE] == "f1decb8087de2abee65e32754e19b9c2a5d30cffdfa8aad1029be9bdc2df96ab"


def test_the_explanation_rows_bridge_the_baseline_and_count_delivered_hours():
    rows = _rows("explanation.csv")
    for day, hours in (("2026-03-29", 23), ("2026-09-06", 24)):
        mine = [r for r in rows if r["day"] == day]
        assert {int(r["hours"]) for r in mine} == {hours}
        groups = [r for r in mine if r["kind"] == "group"]
        assert [r["group"] for r in groups] == list(build_pages.EXPLAIN_GROUPS)
        used = [r for r in groups if r["used"] == "True"]
        assert all(r["mean_phi_eur"] == r["mean_abs_phi_eur"] == "" for r in groups if r["used"] == "False")
        base = float(next(r for r in mine if r["kind"] == "baseline")["mean_phi_eur"])
        issued = float(next(r for r in mine if r["kind"] == "issued")["mean_phi_eur"])
        assert abs(sum(float(r["mean_phi_eur"]) for r in used) - (issued - base)) < 1e-9
        assert all(float(r["mean_abs_phi_eur"]) >= abs(float(r["mean_phi_eur"])) for r in used)
    assert {r["group"] for r in rows if r["used"] == "False"} == {"price_d2", "calendar"}


def test_each_explanation_mark_sits_on_its_own_groups_row():
    labels = {label: group for group, label in build_pages.EXPLAIN_GROUPS.items()}
    panels = build_pages.explanation_panels()
    assert [p.title for p in panels] == [title for _, title in build_pages.EXPLAIN_DAYS]
    assert [r.label for r in panels[0].rows] == [r.label for r in panels[1].rows]  # side by side, one set of labels
    for panel, (day, _) in zip(panels, build_pages.EXPLAIN_DAYS):
        for row in panel.rows:
            assert row.record_id == f"pres6.explain.{day}.{labels[row.label]}.mean_abs"
    # the negative control: the first draft drew each day's own groups, so the last day's rows slid under the wrong
    # labels; panels that differ in their groups are refused here
    drafted = [tuple(g for g in build_pages.EXPLAIN_GROUPS if g in build_pages._explain_used(day))
               for day, _ in build_pages.EXPLAIN_DAYS]
    assert drafted[0] != drafted[1]
    assert "price_d2" not in {labels[r.label] for r in panels[1].rows}


def test_the_explanation_is_labelled_and_cited():
    section = _section(BODY, "outcomes")
    part = section[section.index('id="outcomes-explanation"'):section.index('id="outcomes-bins-h"')]
    text = _text(part)
    for needed in ("2026-03-29", "2026-09-06", "within one fitted model", "not a cause", "not the value an input adds",
                   "not how the model behaves on other days", "quantile for quantile", "used on the last day only"):
        assert needed in text, needed
    assert "reports/cp17-probe/native-reference.json" in section and "evidence/cp-17/" in section
    topic = BODY[BODY.index('id="product-attribution"'):]
    assert 'href="#outcomes-explanation"' in topic[:topic.index('id="product-importance"')]


def test_product_results_wears_none_of_the_v1_card_styles():
    """The release check caught it: wrappers named `outcome` took v1's result-card style (a border and 20 px padding),
    shrinking every new chart's text below 12 px at 320 px wide."""
    section = _section(BODY, "outcomes")
    assert not re.search(r'class="outcome"', section)
    assert section.count('class="outcome-block"') == 6
    css = build_pages.css()
    assert css.count(".outcome-block{") == 1 and ".outcome{" in css  # v1's card rule stays, unused here


def test_the_rank_and_extreme_words_hold_on_the_rows():
    """Editorial review E17: the words the templates fix -- the bins' rise and largest gap, the 2022 peaks, the
    crisis's least coverage and widest intervals, the two inputs that contributed most -- checked on the rows."""
    bins = _rows("bins.csv")
    observed = [float(r["mean_observed"]) for r in bins]
    assert all(a < b for a, b in zip(observed, observed[1:]))
    gaps = [abs(float(r["mean_observed"]) - float(r["mean_p50"])) for r in bins]
    assert gaps.index(max(gaps)) == 9  # the top bin
    inside = [float(r["inside80"]) for r in bins]
    assert inside.index(min(inside)) == 1 and inside.index(max(inside)) == 4  # bins 2 and 5, as the text binds them
    monthly = _rows("monthly.csv")
    for stream in ("v6", "naive"):
        for metric in ("MAE", "WIS"):
            peak = max((r for r in monthly if r["stream"] == stream), key=lambda r: float(r[metric]))
            assert peak["month"].startswith("2022"), (stream, metric)
    coverage = [r for r in _rows("coverage.csv") if r["regime"] != "all"]
    for level in ("50", "80", "95"):
        at = [r for r in coverage if r["level"] == level]
        assert min(at, key=lambda r: float(r["coverage"]))["regime"] == "crisis"
        assert max(at, key=lambda r: float(r["width_eur"]))["regime"] == "crisis"
    for row in (r for r in _rows("coverage.csv") if r["regime"] == "all"):
        assert float(row["coverage"]) < int(row["level"]) / 100  # "each a little below its nominal level"
    explain = [r for r in _rows("explanation.csv") if r["kind"] == "group" and r["used"] == "True"]
    for day in ("2026-03-29", "2026-09-06"):
        ranked = sorted((r for r in explain if r["day"] == day), key=lambda r: -float(r["mean_abs_phi_eur"]))
        assert {r["group"] for r in ranked[:2]} == {"load_d0", "gfs"}, day


#: Integration review 1's finding: hourly prices are committed for every development day (CP-26's pinned snapshot), so no
#: surface may say they are committed only for v5's test periods.
FALSE_PRICE_CLAUSES = re.compile(r"only hours whose prices are committed|prices are committed hour by hour|"
                                 r"with committed observed prices|where committed hourly observed prices exist")


def test_no_surface_says_hourly_prices_are_committed_only_for_v5s_periods():
    snapshot = pd.read_parquet(ROOT / "data/snapshot.parquet", columns=["delivery_date", "price_eur_mwh"])
    days = set(snapshot.loc[snapshot.price_eur_mwh.notna(), "delivery_date"].astype(str))
    assert {"2020-12-29", "2022-07-26", "2026-09-06"} <= days  # the premise is false: every period's prices are there
    templates = " ".join(block.template for block in RC.PRES6_BLOCKS)
    for name, text in (("page", _text(BODY)), ("README", README), ("templates", " ".join(templates.split())),
                       ("populations", " ".join(R.POPULATIONS.values()))):
        assert not FALSE_PRICE_CLAUSES.search(text), name
    assert FALSE_PRICE_CLAUSES.search("the only hours whose prices are committed hour by hour")  # the negative control


def test_the_evidence_tags_date_is_the_tips():
    """The page labels the product results' rows "frozen <date>" from the registry; that date is the evidence tip's.
    Checked where the tag is present. Without it (GitHub's CI checks out no tags) nothing in the history can date the
    tip, since `main` holds the squash, not the tip: packet §8.2 checks the date before the tag is made (Integration
    recheck, N1: a fallback to the landing commit's date would turn `main` red whenever the landing is a day late)."""
    import subprocess

    from delu_forecast import registry as G

    date = G.EVIDENCE_TAGS["evidence/pres-6"][1]
    assert re.fullmatch(r"2026-11-1[4-9]", date)
    tagged = subprocess.run(["git", "log", "-1", "--format=%cs", "evidence/pres-6"], cwd=ROOT, capture_output=True,
                            text=True)
    if tagged.returncode != 0 or not tagged.stdout.strip():
        pytest.skip("the evidence/pres-6 tag is not in this checkout (packet §8.2 checks the date before tagging)")
    assert date == tagged.stdout.strip()
