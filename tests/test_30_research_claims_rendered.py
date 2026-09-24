"""Presentation plan §9.5: research claims render only through the claim layer, and only as approved.

The provenance proof is test_29 (every record re-derives from its row). This file checks the
layer above it: every rendered claim exists in the claim layer and a claim map, every numeral in a
research block is bound to a record or declared structural, withheld and stale phrasing is absent,
no v2+ record crosses the development boundary, and the exact H−P endpoint is never rounded.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from delu_forecast import research as R
from delu_forecast import research_claims as RC
from delu_forecast.claims import REPO_ROOT

README = REPO_ROOT / "README.md"
BARE_NUMERAL = re.compile(r"\S*\d\S*")
BOUND = re.compile(r"<data\b[^>]*>.*?</data>|<span data-structural=\"[^\"]+\">.*?</span>", re.DOTALL)
TAG = re.compile(r"<[^>]+>")


def unbound_numerals(fragment: str) -> list[str]:
    """Numerals left once every claim-bound value and declared structural numeral is removed."""
    return BARE_NUMERAL.findall(TAG.sub(" ", BOUND.sub(" ", fragment)))


# -- the claim layer and the maps ----------------------------------------------


def test_every_claim_the_layer_renders_is_in_a_claim_map():
    missing = sorted(RC.all_claim_ids() - RC.claim_map_ids())
    assert not missing, f"claims rendered but absent from both claim maps: {missing}"


def test_the_maps_define_the_withheld_list_w1_to_w21():
    ids = RC.claim_map_ids()
    assert {f"W{n}" for n in range(1, 22)} <= ids


@pytest.mark.parametrize("block", RC.BLOCKS, ids=lambda b: b.key)
def test_every_block_renders_and_binds_every_numeral(block):
    rendered = RC.render(block.key)
    assert unbound_numerals(rendered) == [], f"{block.key}: unbound numerals {unbound_numerals(rendered)}"
    for record_id in block.records():
        assert f'data-record="{record_id}"' in rendered
    assert f'data-claim="{block.claim_id}"' in rendered or not block.records()


@pytest.mark.parametrize("block", RC.BLOCKS, ids=lambda b: b.key)
def test_no_block_carries_withheld_or_stale_phrasing(block):
    for target in ("html", "md"):
        text = TAG.sub(" ", RC.render(block.key, target))
        assert not RC.withheld_findings(text), (block.key, RC.withheld_findings(text))
        assert not RC.stale_findings(text), (block.key, RC.stale_findings(text))


def test_every_block_record_is_a_real_record():
    for block in RC.BLOCKS:
        for record_id in block.records():
            R.get(record_id)


# -- guards on the typed fields -------------------------------------------------


def test_date_guard_v2_and_later_records_stay_inside_development():
    for block in RC.BLOCKS:
        for record_id in block.records():
            record = R.get(record_id)
            if record.checkpoint in ("CP-15", "CP-16", "CP-20") and record.window:
                assert record.window[1] <= R.EVIDENCE_BOUNDARY, (block.key, record_id, record.window)


def test_date_guard_negative_control():
    import dataclasses

    record = R.get("cp20.metrics.HG.fold_5.MAE")
    late = dataclasses.replace(record, window=("2026-06-09", "2026-09-06"))
    assert late.window[1] > R.EVIDENCE_BOUNDARY


def test_the_exact_endpoint_is_forced_wherever_it_is_rendered():
    html = RC.render("v2.result.hp")
    assert "+0.000003857628092332211" in html
    assert "0.0000]" not in html and "0.0000<" not in html
    # Even a template that asks for the rounded endpoint gets the full value.
    forced = RC.render_template("C34", "{r:cp16.uncertainty.V2-H-V2-P.equal_fold.MAE|hi}")
    assert "+0.000003857628092332211" in forced


def test_the_readme_block_carries_no_withheld_or_stale_phrasing():
    text = README.read_text()
    block = text[text.index("<!-- research:start -->"):text.index("<!-- research:end -->")]
    assert not RC.withheld_findings(block), RC.withheld_findings(block)
    assert not RC.stale_findings(block), RC.stale_findings(block)


# -- negative controls -----------------------------------------------------------


def test_negative_control_an_undeclared_numeral_is_caught():
    rendered = RC.render_template("C69", "The gain is 7.8% on {r:cp20.metrics.HG.equal_fold.S_MAE}.")
    assert unbound_numerals(rendered) == ["7.8%"]


def test_negative_control_a_structural_numeral_is_not_a_finding():
    rendered = RC.render_template("C69", "In fold {s:fold:3} the value is {r:cp20.metrics.HG.fold_3.MAE}.")
    assert unbound_numerals(rendered) == []


def test_negative_control_a_missing_claim_id_is_caught():
    assert "C999" not in RC.claim_map_ids()
    with pytest.raises(RC.ClaimError):
        RC.svg_binding("C999", "cp20.metrics.HG.equal_fold.S_MAE")


def test_negative_control_an_unknown_record_is_caught():
    with pytest.raises(R.EvidenceError):
        RC.render_template("C69", "{r:cp20.metrics.HG.equal_fold.S_MAX}")


@pytest.mark.parametrize(
    "sentence, withheld",
    [
        ("Hour-aware intervals are better than pooled ones.", "W1"),
        ("The interval ends at +0.0000] so it improves.", "W3"),
        ("This result is statistically significant.", "W7"),
        ("Wind at 100 m drives the gain.", "W17"),
        ("The model passed peer review.", "W18"),
        ("Try the v3 demo in your browser.", "W19"),
        ("v3 is 46% better than v1.", "W20"),
        ("The holdout gave a confirmatory result.", "W21"),
        ("It has a coverage guarantee.", "W15"),
    ],
)
def test_negative_control_withheld_phrasing_is_caught(sentence, withheld):
    assert any(finding.startswith(withheld) for finding in RC.withheld_findings(sentence)), sentence


@pytest.mark.parametrize(
    "sentence",
    [
        "The holdout label is confirmatory-style, not power-qualified.",
        "The development results are never confirmatory.",
        "Residual intervals carry no conformal coverage guarantee.",
        "An independent Integration review within this project's process.",
    ],
)
def test_negative_control_honest_denials_are_not_findings(sentence):
    assert not RC.withheld_findings(sentence), sentence


def test_negative_control_stale_phrasing_is_caught():
    assert RC.stale_findings("Its runs land in a separate `delu-m4` experiment.")
    assert RC.stale_findings("it is the defect the planned v2 targets")
