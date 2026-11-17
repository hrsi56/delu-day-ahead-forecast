"""PRES-7: Business insights with CP-29's profit chart (decision 32), and PRES-6's follow-ups (O51 items 7 and 8).

The contracts, each with a negative control where a check could pass vacuously:

- the profit chart is drawn from CP-29's committed daily rows by packet §0's rules: each line's last value equals its
  record within a stated tolerance (floats, never bytes), every day is kept, and a changed row is refused;
- the chart and the text name the battery and costs, the policy and artifact, the population with its dates and units,
  and the evidence class; doing nothing is the zero line;
- CP-29's claims C1101-C1108 and PRES-7's C1201-C1204 are on the page, the limits in plain words, and what is still not
  evaluated replaces the gap; no error or coverage figure is called a profit (W54), and no return (W56), realized
  income (W57) or live or prospective profit (W58) appears;
- the README carries the same business claims through the claim layer;
- the comparison's phone axis holds v6's interval-score marker (O51 item 7);
- the wording pass defines its terms at first use and changes no number (O51 item 8).
"""
from __future__ import annotations

import collections
import html
import io
import math
import re
import subprocess
import sys
from pathlib import Path

import pytest

from delu_forecast import publication_lint as L
from delu_forecast import registry as G
from delu_forecast import research as R
from delu_forecast import research_claims as RC

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_pages as B  # noqa: E402

PAGE = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
BODY = PAGE.split("<script>")[0]
README = (ROOT / "README.md").read_text(encoding="utf-8")
#: The published page before PRES-7 (the issue commit), for the rendered-number diff.
BEFORE_COMMIT = "a5db292aa0aed68886ea0ab7237cf5fe9a672b65"
BEFORE_SHA256 = "5e294d40790f3415c14cf932e94f1351e2e99a0b84d6efd3d2321046d7eccdaa"
#: A drawn line's last value against its record: summation order may move the last bits (packet §0).
TOLERANCE = 1e-9


INLINE = re.compile(r"</?(?:span|data|strong|em|a|b|i|code|abbr|tspan)\b[^>]*>")


def _text(fragment: str) -> str:
    """The visible text: inline elements join their neighbours, block elements are separated by a space."""
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", INLINE.sub("", fragment)))).strip()


SECTION = re.compile(r'<section\b[^>]*\bid="([^"]+)"')


def _section(page: str, section_id: str) -> str:
    starts = [(m.group(1), m.start()) for m in SECTION.finditer(page)]
    i = next(i for i, (name, _) in enumerate(starts) if name == section_id)
    return page[starts[i][1]:starts[i + 1][1] if i + 1 < len(starts) else len(page)]


BUSINESS = _section(BODY, "business")


# --------------------------------------------------------------------------- the series (packet §0)


def test_each_line_ends_at_its_record_and_keeps_every_day():
    series = B.profit_series()
    assert set(series) == {"v6", "naive", "perfect_foresight"}
    for source, rule, _, _ in B.PROFIT_LINES:
        line = series[source]
        record = R.get(f"cp29.p_all.all.{source}.{rule}.w25.cumulative_profit_eur")
        assert len(line) == R.get(f"cp29.p_all.all.{source}.{rule}.w25.days").value == 2068
        assert line[0][0] == "2020-12-29" and line[-1][0] == "2026-09-06"
        assert [day for day, _ in line] == sorted(day for day, _ in line)
        assert math.isclose(line[-1][1], record.value, rel_tol=TOLERANCE, abs_tol=0.0), source
    # the ordering the text states: perfect foresight above v6 above the naive at the end
    ends = {source: line[-1][1] for source, line in series.items()}
    assert ends["perfect_foresight"] > ends["v6"] > ends["naive"] > 0


def test_negative_control_a_changed_daily_row_is_refused(monkeypatch):
    raw = R.source_bytes(B.CP29_DAILY).decode("utf-8")
    with pytest.raises(R.EvidenceError):  # the registered blob no longer matches
        monkeypatch.setattr(R, "source_bytes", lambda path: (raw.replace(",v6,median,25,", ",v6,median,25,", 1)
                                                            + "\n").encode())
        B.profit_series()
    monkeypatch.undo()
    # past the blob check, a line that no longer ends at its record stops the build
    rows = raw.splitlines()
    index = next(i for i, row in enumerate(rows) if ",v6,median,25," in row and ",True," in row)
    cells = rows[index].split(",")
    cells[13] = str(float(cells[13]) + 1.0)  # profit_eur
    rows[index] = ",".join(cells)
    monkeypatch.setattr(R, "check_source", lambda path: None)
    monkeypatch.setattr(R, "source_bytes", lambda path: ("\n".join(rows) + "\n").encode())
    with pytest.raises(B.ProfitSeriesError, match="v6"):
        B.profit_series()


def test_the_thinning_keeps_each_columns_first_lowest_highest_and_last_point():
    points = [(0.1, 5.0), (0.5, 9.0), (0.7, 1.0), (0.9, 4.0), (1.2, 3.0), (2.5, 7.0)]
    assert B._thin(points, 0.0) == [(0.1, 5.0), (0.5, 9.0), (0.7, 1.0), (0.9, 4.0), (1.2, 3.0), (2.5, 7.0)]
    dense = [(0.01 * i, float((i * 37) % 11)) for i in range(100)]  # one column
    kept = B._thin(dense, 0.0)
    assert kept[0] == dense[0] and kept[-1] == dense[-1] and len(kept) <= 4
    assert min(y for _, y in kept) == min(y for _, y in dense) and max(y for _, y in kept) == max(y for _, y in dense)


# --------------------------------------------------------------------------- the chart and its identity


def _chart(variant: str) -> str:
    return re.search(rf'<svg class="{variant}"[^>]*data-chart="business-profit".*?</svg>', BUSINESS, re.S).group(0)


def test_the_chart_draws_three_lines_and_doing_nothing_in_both_variants():
    for variant, labels in (("d", ("perfect foresight", "v6", "naive")), ("m", ("perfect", "foresight", "v6", "naive"))):
        svg = _chart(variant)
        assert svg.count("<polyline") == 3, variant
        texts = [_text(t) for t in re.findall(r"<text[^>]*>(.*?)</text>", svg)]
        for label in labels + ("doing nothing", "Cumulative net profit"):
            assert label in texts, (variant, label)
        assert "0" in texts and "300" in texts  # thousand EUR, from zero
        # the dashes distinguish the lines (no meaning by colour alone)
        assert len(set(re.findall(r'<polyline[^>]*?stroke-width="([^"]+)"(?: stroke-dasharray="([^"]+)")?', svg))) == 3


def test_the_graphic_names_battery_policy_population_dates_units_and_class():
    head = BUSINESS[BUSINESS.index('id="business-profit"'):BUSINESS.index('data-chart-id="business-profit-chart"')]
    identity = _text(head)
    for needed in ("1 MW", "2 MWh", "in EUR", "2,068 eligible development days", "2020-12-29 to 2026-09-06",
                   "€25 per MWh of wear", "v6's stored forecasts", "A1 in the frozen records", "the median rule",
                   "similar-day naive", "perfect foresight", "doing nothing earns zero",
                   "simulated, development, post-selection"):
        assert needed in identity, needed
    for variant in ("d", "m"):
        svg = _chart(variant)
        assert "Simulated, development, post-selection" in svg and "1 MW, 2 MWh" in svg
    key = _text(re.search(r'<p class="preview-key profit-key">.*?</p>', BUSINESS, re.S).group(0))
    for source, rule, _, _ in B.PROFIT_LINES:
        record_id = f"cp29.p_all.all.{source}.{rule}.w25.cumulative_profit_eur"
        assert f'data-record="{record_id}"' in BUSINESS
    assert key.startswith("v6, median rule: 257,212 EUR Similar-day naive, median rule: 220,136 EUR Perfect "
                          "foresight: 287,292 EUR Doing nothing: zero")


def test_the_section_keeps_a8s_place_and_routes_to_its_details():
    order = SECTION.findall(BODY)
    assert order[:5] == ["top", "product", "outcomes", "business", "research-results"]
    routes = re.findall(r'<a class="quiet" href="#(business-[a-z0-9]+)">', BUSINESS)
    assert routes == [anchor for anchor, _ in B.BUSINESS_ROUTES]
    for anchor, heading in B.BUSINESS_ROUTES:
        assert _text(re.search(rf'<h4 class="detail-head" id="{anchor}">(.*?)</h4>', BUSINESS, re.S).group(1)) == heading
    # each route is the only link to its heading, and no other route shares its first 40 characters (the release
    # check finds a route by its link and those characters; PRES-6's topic-6 route once matched a hidden twin)
    others = [_text(a)[:40] for nav in re.findall(r'<nav class="(?:explore|product-routes)".*?</nav>', BODY, re.S)
              for a in re.findall(r"<a [^>]*>(.*?)</a>", nav, re.S)]
    for anchor, heading in B.BUSINESS_ROUTES:
        assert BODY.count(f'href="#{anchor}"') == 1, anchor
        assert others.count(heading[:40]) == 1, heading
    assert "pres-7/publication-packet.md" in BUSINESS and G.EVIDENCE_TAGS["evidence/pres-7"][1] >= "2026-11-16"


# --------------------------------------------------------------------------- the text


def test_every_cp29_and_pres7_claim_is_on_the_page():
    for block in RC.CP29_BLOCKS + RC.PRES7_BLOCKS:
        assert f'data-block="{block.key}"' in BUSINESS, block.key
        assert RC.render(block.key) in BUSINESS, block.key
    assert {f"C{n}" for n in range(1201, 1205)} | {"W58"} <= RC.claim_map_ids()


def test_the_limits_are_on_the_page_in_plain_words():
    text = _text(BUSINESS)
    for needed in ("no money was traded", "Not realized income", "Only day-ahead arbitrage was simulated",
                   "not intraday trading, balancing energy or reserves", "price-taker", "Hourly, not quarter-hourly",
                   "chosen on these same days, so its result is optimistic for it", "not a trading recommendation",
                   "No return or payback is computed: there is no capital cost", "Not 4.7T's result",
                   "not a forecast of future profit", "Not a property of v6 alone",
                   "empty at the start and the end of each day", "no grid fees, levies or taxes are charged",
                   "never out of service", "the median rule"):
        assert needed in text, needed
    # each caveat once (editorial E5): the class caveat beside the finding, not repeated in the limits
    assert text.count("so its result is optimistic for it") == 1 and text.count("after selection") == 0


def test_what_is_still_not_evaluated_replaces_the_gap():
    text = _text(BUSINESS)
    gap = _text(RC.render("business.gap"))
    assert gap.startswith("Not evaluated.")
    for needed in ("intraday trading", "balancing energy or reserves", "a real battery's own costs",
                   "the live product's forecasts", "no live or prospective profit"):
        assert needed in gap, needed
    assert gap in text and "No decision policy, cost model or trading simulation" not in text


def test_the_untraded_days_and_the_risk_aware_variant_bind_their_records():
    untraded = RC.render("economics.untraded")
    for record_id in ("cp29.p_all.all.v6.median.w25.trading_days", "cp29.p_all.all.v6.median.w25.missing_days",
                      "cp29.p_all.all.naive.median.w25.missing_days"):
        assert f'data-record="{record_id}"' in untraded
    assert "traded on 1,770 of the 2,068 days" in _text(untraded) and "on 33, within a week after a clock change" in _text(untraded)
    assert "11 days that way" in _text(untraded)
    # C1203 says "lost money on fewer days ... but earned less": it holds on the records
    get = lambda rule, field: R.get(f"cp29.p_all.all.v6.{rule}.w25.{field}").value  # noqa: E731
    assert get("risk", "losing_days") < get("median", "losing_days")
    assert get("risk", "cumulative_profit_eur") < get("median", "cumulative_profit_eur")
    # C1202: the untraded days are kept in the curve at zero
    rows = [row for row in __import__("csv").DictReader(io.StringIO(R.source_bytes(B.CP29_DAILY).decode()))
            if row["source"] == "v6" and row["rule"] == "median" and row["wear_eur_per_mwh"] == "25"]
    missing = [row for row in rows if row["missing_hour"] == "True"]
    assert len(missing) == get("median", "missing_days") and all(float(row["profit_eur"]) == 0 for row in missing)


def test_no_status_word_in_the_new_or_reworded_text():
    """Standard v1 §§1, 5 (editorial E4): no wording that expires. The template lint scans only the claim layer's root
    block list, so PRES-7 scans its own blocks here."""
    keys = [block.key for block in RC.CP29_BLOCKS + RC.PRES7_BLOCKS] + [
        "business.use", "business.measured", "business.gap", "business.limits", "terms.class_final",
        "terms.selection_rule", "terms.final_candidate", "product.live", "comparison.caveat.a1", "everyday.finding.v6",
        "comparison.sub"]
    for key in keys:
        assert not L.STATUS_WORDS.search(re.sub(r"\{[^}]*\}", "", RC.BLOCKS_BY_KEY[key].template)), key
    assert L.STATUS_WORDS.search("What is still not evaluated.")  # the negative control: E4's first wording


def test_a_paired_money_difference_has_four_significant_figures():
    """Standard v1 §4 (editorial E6): a difference is shown to at most four significant figures."""
    record = R.get("cp29.paired.p_all.median.v6_minus_naive.w25.total_difference_eur")
    assert (R.display(record), R.display(record, "ci_low"), R.display(record, "ci_high")) == ("+37,080", "+32,320", "+42,310")
    assert abs(float(R.display(record).replace(",", "")) - record.value) / record.value < 5e-4
    v5 = R.get("cp29.paired.p_v5.median.v6_minus_v5.w25.total_difference_eur")
    assert (R.display(v5), R.display(v5, "ci_low"), R.display(v5, "ci_high")) == ("+165", "−727", "+1,032")
    rid = record.record_id
    assert L.precision_findings(L.reading_path(f'<p><span data-record="{rid}">+37,080</span></p>')) == []
    assert L.precision_findings(L.reading_path(f'<p><span data-record="{rid}">+37,077</span></p>'))
    assert "+37,080 EUR [+32,320, +42,310]" in _text(BUSINESS)


def test_the_forbidden_claims_are_absent_and_guarded():
    for surface in (_text(BODY), README):
        assert not [hit for hit in RC.withheld_findings(surface) if hit.split(":")[0] in ("W54", "W56", "W57", "W58")]
    for claim in ("its lower error is a profit", "the coverage equals a success rate", "a live profit of 12 EUR",
                  "prospective earnings were 300 EUR", "an annualized return of 9%", "a realized income of 1 EUR"):
        assert RC.withheld_findings(claim), claim
    for allowed in ("the report shows no live or prospective profit", "would have earned 257,212 EUR net",
                    "v6's profit minus the naive's, summed over the days, is +37,080 EUR"):
        assert not RC.withheld_findings(allowed), allowed
    assert "live." not in "".join(re.findall(r'data-record="([^"]+)"', BUSINESS))


def test_a_daily_money_figure_keeps_its_decimal():
    record_id = "cp29.p_all.pre_crisis.perfect_foresight.perfect.w25.mean_eur"
    shown = L.precision_findings(L.reading_path(f'<p><span data-record="{record_id}">22.2</span></p>'))
    assert shown == []
    assert L.precision_findings(L.reading_path(f'<p><span data-record="{record_id}">22</span></p>'))
    total = "cp29.p_all.all.v6.median.w25.cumulative_profit_eur"
    assert L.precision_findings(L.reading_path(f'<p><span data-record="{total}">257,212.5</span></p>'))


def test_the_readme_carries_the_same_business_claims():
    business = next(line for line in README.splitlines() if line.startswith("**Business insights:**"))
    for key in ("business.use", "business.measured", "economics.setup", "economics.finding", "economics.difference",
                "economics.v5", "economics.risk", "economics.sensitivity", "economics.regimes", "economics.limits",
                "economics.assumptions", "business.gap", "business.limits"):
        assert RC.render(key, "md", surface=RC.README) in business, key
    assert "cp29." not in README and "#business" in business


# --------------------------------------------------------------------------- O51 item 7: the phone axis


def _marks(svg: str) -> list[tuple[str, float, float]]:
    """(record, leftmost x, rightmost x) of every bound mark."""
    out = []
    for tag, attrs in re.findall(r"<(polygon|circle|rect)\b([^>]*data-record=\"[^\"]+\"[^>]*)/>", svg):
        record = re.search(r'data-record="([^"]+)"', attrs).group(1)
        if tag == "polygon":
            xs = [float(pair.split(",")[0]) for pair in re.search(r'points="([^"]+)"', attrs).group(1).split()]
        elif tag == "circle":
            cx, r = (float(re.search(rf'{k}="([^"]+)"', attrs).group(1)) for k in ("cx", "r"))
            xs = [cx - r, cx + r]
        else:
            x, w = (float(re.search(rf'{k}="([^"]+)"', attrs).group(1)) for k in ("x", "width"))
            xs = [x, x + w]
        out.append((record, min(xs), max(xs)))
    return out


def test_the_comparisons_phone_axis_holds_every_marker():
    svg = re.search(r'<svg class="m"[^>]*data-chart="overview".*?</svg>', BODY, re.S).group(0)
    marks = _marks(svg)
    assert len(marks) == 26  # thirteen rows, two panels
    assert all(0 <= low and high <= B.MOBILE_W for _, low, high in marks), [m for m in marks if m[1] < 0]
    assert [p.domain for p in B.overview_panels()] == [(0.4, 1.1), (0.4, 1.1)]
    lowest = min(R.get(row.record_id).value for panel in B.overview_panels() for row in panel.rows)
    assert lowest >= 0.4
    # every pinned comparison (published in MLflow) keeps its own axis
    assert [p.domain for p in B.overview_panels(G.V5_COMPARISON_ORDER, live=True)] == [(0.5, 1.1), (0.5, 1.1)]
    # the negative control: on the old axis, v6's interval-score hexagon (0.437) starts left of the drawing
    old = B.Scale("x", 0.5, 1.1, 22.0, B.MOBILE_W - 18.0, "ratio")
    assert old(R.get("pres5.metrics.A1.equal_fold.S_WIS").value) - 6.6 < 0


# --------------------------------------------------------------------------- O51 item 8: the wording pass


def test_the_terms_are_defined_at_first_use():
    body = _text(BODY[BODY.index("<body"):])
    first = lambda term: body.index(term)  # noqa: E731
    assert body[first("Owner") - 4:].startswith("The Owner, the project's lead,")
    assert body[first("re-baseline"):].startswith("re-baseline re-scored every policy on every day")
    assert body[first("A1 in the frozen records") - 6:].startswith("named A1 in the frozen records")
    # "descriptive", first used in the headline, is defined directly below it (editorial E2)
    terms = _text(BODY[BODY.index('class="headline-terms"'):BODY.index("</dd>", BODY.index('class="headline-terms"'))])
    assert first("descriptive") < first("descriptive intervals: not the rule's own test") and "descriptive intervals: not the rule's own test" in terms
    assert body[first("4.7T"):first("Open the live product")].count("its one test on new data") == 1
    assert "7 candidate policies tested" in body and "13 policies drawn" in body


def test_the_comparison_explains_its_populations_ends_and_intervals():
    text = _text(_section(BODY, "research-results"))
    assert ("The headline's −7% is another population, all 2,068 development days to 2026-09-06; this is the five "
            "test periods' 10,747 hours, the last on 2026-04-07.") in text
    assert ("confidence intervals from resampling 14-day blocks of days, called descriptive because the selection "
            "decided by its registered tests, not by them") in text


NUMBER = re.compile(r"[−+-]?\d[\d,]*(?:\.\d+)?%?")


def _without_business(page: str) -> str:
    i = page.index('<section class="section" id="business"')
    return page[:i] + page[page.index("</section>", i) + len("</section>"):]


def _bound_values(page: str) -> dict[tuple[str, str], set[str]]:
    out: dict[tuple[str, str], set[str]] = collections.defaultdict(set)
    for match in re.finditer(r'<(span|data|text|td|strong)\b([^>]*?data-record="([^"]+)"[^>]*?)(?<!/)>(.*?)</\1>',
                             page, re.S):
        field = re.search(r'data-field="([^"]+)"', match.group(2))
        out[(match.group(3), field.group(1) if field else "value")].add(_text(match.group(4)))
    return out


def number_changes(before: str, after: str) -> list[str]:
    """Outside Business insights: every bound value rendered as before, and no number in the reading text removed or
    added unless it was already on the page (O51 item 8: no number changes)."""
    before, after = _without_business(before), _without_business(after)
    old, new = _bound_values(before), _bound_values(after)
    problems = [f"{key}: {old[key]} -> {new.get(key)}" for key in old if old[key] != new.get(key)]
    problems += [f"{key}: new binding" for key in new.keys() - old.keys()]
    old_numbers = collections.Counter(NUMBER.findall(L.reading_text(before)))
    new_numbers = collections.Counter(NUMBER.findall(L.reading_text(after)))
    problems += [f"{number} removed" for number in old_numbers - new_numbers]
    problems += [f"{number} is new to the page" for number in new_numbers - old_numbers if number not in old_numbers]
    return problems


def test_the_wording_pass_changed_no_number():
    shown = subprocess.run(["git", "show", f"{BEFORE_COMMIT}:docs/index.html"], cwd=ROOT, capture_output=True)
    if shown.returncode != 0:
        pytest.skip("the pre-PRES-7 page is not in this checkout's history (packet §7 records the diff)")
    import hashlib

    assert hashlib.sha256(shown.stdout).hexdigest() == BEFORE_SHA256
    before = shown.stdout.decode("utf-8")
    assert number_changes(before, PAGE) == []
    # the negative control: one bound value changed outside Business insights is caught
    altered = PAGE.replace(">−6%<", ">−5%<", 1)
    assert altered != PAGE and number_changes(before, altered)
