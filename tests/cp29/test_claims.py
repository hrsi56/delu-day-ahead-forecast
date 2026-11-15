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


def test_the_blocks_are_written_for_pres7_and_appear_on_no_published_surface():
    keys = [block.key for block in RC.CP29_BLOCKS]
    assert keys and all(block.surfaces == frozenset({RC.PRES7}) for block in RC.CP29_BLOCKS)
    for key in keys:
        assert f'data-block="{key}"' not in PAGE
        with pytest.raises(RC.ClaimError):
            RC.render(key)                                   # not on the page in this round
    assert "cp29." not in PAGE and "cp29." not in README


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
