"""CP-29's entries in the claim layer (ruling O57): the records re-derive, the claims PRES-7 will render bind them and
hold on them, and no page or README changes in this round."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from delu_forecast import registry as G
from delu_forecast import research as R
from delu_forecast import research_claims as RC

ROOT = Path(__file__).resolve().parents[2]
PAGE = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")


def _cp29() -> list[R.EvidenceRecord]:
    return [record for key, record in R.records().items() if key.startswith("cp29.")]


def test_every_cp29_record_rederives_and_a_perturbed_one_fails():
    records = _cp29()
    assert len(records) > 2000 and R.validate_all(records) == []
    record = R.get("cp29.p_all.all.v6.median.w25.cumulative_profit_eur")
    bad = R.EvidenceRecord(**{**record.__dict__, "raw": "300000"})
    assert any("committed value" in problem for problem in R.validate_all([bad]))
    for record in records:
        assert record.evidence_class == R.EVIDENCE_CLASS_SIMULATED and record.window[1] <= R.RESEARCH_BOUNDARY


def _publication_problems(block: RC.Block, page: str, readme: str) -> list[str]:
    """Where a CP-29 block is not on the page and in the README exactly as the claim layer renders it, bound to its
    `cp29.*` records on the page."""
    problems = []
    rendered = RC.render(block.key)
    if f'data-block="{block.key}"' not in page or rendered not in page:
        problems.append(f"{block.key}: not on the page as the claim layer renders it")
    for record_id in block.records():
        if f'data-record="{record_id}"' not in rendered or f'data-record="{record_id}"' not in page:
            problems.append(f"{block.key}: {record_id} is not bound on the page")
    if RC.render(block.key, "md", surface=RC.README) not in readme:
        problems.append(f"{block.key}: not in the README as the claim layer renders it")
    return problems


def test_the_blocks_render_on_the_page_and_the_readme_through_the_claim_layer():
    """PRES-7's successor (ruling O63) to CP-29's round-scoped `..._appear_on_no_published_surface`: PRES-7 publishes
    the eight blocks, so each renders on the page and in the README from the claim layer and binds its records; an
    altered number or record fails (the negative control)."""
    assert len(RC.CP29_BLOCKS) == 8
    for block in RC.CP29_BLOCKS:
        assert block.surfaces == frozenset({RC.PRES7, RC.PAGE, RC.README}), block.key
        assert all(record_id.startswith("cp29.") for record_id in block.records()), block.key
        assert _publication_problems(block, PAGE, README) == [], block.key
    # C1101 (the setup) and C1108 (the limits) are definitions; the other six bind CP-29's records
    assert [block.key for block in RC.CP29_BLOCKS if not block.records()] == ["economics.setup", "economics.limits"]
    assert "cp29." not in README                              # the README carries the text, not the bindings
    # The negative control: the finding with one number altered, on the page and in the README, fails.
    finding = RC.BLOCKS_BY_KEY["economics.finding"]
    number = re.sub(r"<[^>]+>", "", RC.render(finding.key)).split("earned ")[1].split(" ")[0]
    altered = number[:-1] + str((int(number[-1]) + 1) % 10)
    assert number in PAGE and number in README and altered != number
    assert _publication_problems(finding, PAGE.replace(number, altered), README)
    assert _publication_problems(finding, PAGE, README.replace(number, altered))
    # ... and a block bound to a record it does not render fails too.
    record_id = finding.records()[0]
    assert _publication_problems(finding, PAGE.replace(f'data-record="{record_id}"', 'data-record="cp29.altered"'), README)


def test_each_block_binds_its_records_and_the_claims_hold_on_them():
    for block in RC.CP29_BLOCKS:
        rendered = RC.render(block.key, surface=RC.PRES7)
        for record_id in block.records():
            assert f'data-record="{record_id}"' in rendered
    pair = R.get("cp29.paired.p_v5.median.v6_minus_v5.w25.total_difference_eur")
    assert pair.ci_low < 0 < pair.ci_high                    # C1104: "whose interval spans zero"
    naive = R.get("cp29.paired.p_all.median.v6_minus_naive.w25.total_difference_eur")
    assert naive.ci_low > 0                                  # C1103 says "more", with its interval
    assert R.get("cp29.p_all.all.perfect_foresight.perfect.w25.losing_days").value == 0     # C1105
    v6, v5 = (R.get(f"cp29.p_v5.all.{s}.median.w25.cumulative_profit_eur").value for s in ("v6", "v5"))
    assert abs(v6 - v5) / v5 < 0.01                          # C1104: "about the same"
    pre = R.get("cp29.p_all.pre_crisis.perfect_foresight.perfect.w25.mean_eur").value
    later = [R.get(f"cp29.p_all.{s}.perfect_foresight.perfect.w25.mean_eur").value for s in ("crisis", "negative_prices")]
    assert pre < min(later) / 3                              # C1107: "earned only ... a day" before the crisis


def test_the_withheld_claims_w56_and_w57_are_guarded():
    for claim in ("an annualized return of 12%", "a payback period of 7 years", "the IRR is 9%",
                  "a realized income of 257,212 EUR", "actual profit was 100 EUR"):
        assert [h for h in RC.withheld_findings(claim) if h.split(":")[0] in ("W56", "W57")], claim
    for allowed in ("No return or payback is computed: there is no capital cost.", "not realized income",
                    "would have earned 257,212 EUR net"):
        assert not [h for h in RC.withheld_findings(allowed) if h.split(":")[0] in ("W56", "W57")], allowed
    for surface in (re.sub(r"<[^>]+>", " ", PAGE.split("<script>")[0]), README):
        assert not [h for h in RC.withheld_findings(surface) if h.split(":")[0] in ("W56", "W57")]


def test_the_evidence_tag_and_the_claim_map():
    assert G.EVIDENCE_TAGS["evidence/cp-29"][1] >= "2026-11-15"
    ids = RC.claim_map_ids()
    assert {f"C{n}" for n in range(1101, 1109)} <= ids and {"W56", "W57"} <= ids
    for path in ("reports/cp29/summary.csv", "reports/cp29/paired.csv", "reports/cp29/daily.csv"):
        assert R.SOURCES[path].tag == "evidence/cp-29"
