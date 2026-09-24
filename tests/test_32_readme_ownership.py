"""Presentation plan §9.4 (finding F04): a generator owns the README's research section.

The markers appear exactly once, the generator is idempotent, a change in the claim layer reaches
the block, and bytes outside the block never change.
"""

from __future__ import annotations

import sys

import pytest

from delu_forecast import research_claims as RC
from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import readme_research as G  # noqa: E402

README = REPO_ROOT / "README.md"


@pytest.fixture(scope="module")
def text() -> str:
    return README.read_text()


def test_the_markers_appear_exactly_once(text):
    assert text.count(G.START) == 1
    assert text.count(G.END) == 1
    assert text.index(G.START) < text.index(G.END)


def test_the_committed_block_is_current(text):
    assert G.apply(text) == text, "README research block is stale; run scripts/readme_research.py"


def test_running_twice_gives_identical_output(text):
    once = G.apply(text)
    assert G.apply(once) == once


def test_bytes_outside_the_block_are_unchanged(text):
    begin, finish = text.index(G.START), text.index(G.END) + len(G.END)
    doctored = text[:begin] + G.START + "\nstale\n" + G.END + text[finish:]
    rebuilt = G.apply(doctored)
    assert rebuilt[:begin] == text[:begin]
    assert rebuilt[-(len(text) - finish):] == text[finish:]
    assert rebuilt == text


def test_a_claim_change_reaches_the_block(text, monkeypatch):
    """Fixture change: alter one block's template and the generated README must follow it."""
    key = "v3.caveat.bundle"
    original = RC.BLOCKS_BY_KEY[key]
    changed = RC.Block(original.key, original.claim_id, original.template + " FIXTURE-SENTINEL.",
                       original.surfaces, original.status)
    monkeypatch.setitem(RC.BLOCKS_BY_KEY, key, changed)
    assert "FIXTURE-SENTINEL" in G.apply(text)
    assert "FIXTURE-SENTINEL" not in text


def test_the_block_renders_only_readme_blocks_from_the_claim_layer(text):
    begin, finish = text.index(G.START), text.index(G.END)
    block = text[begin:finish]
    for key in RC.README_BLOCKS:
        assert RC.render(key, "md", surface=RC.README) in block, key
    assert "+0.000003857628092332211" in block, "the H−P endpoint must be printed in full"


# -- negative controls ---------------------------------------------------------


def test_a_missing_marker_fails_clearly(text):
    with pytest.raises(G.MarkerError, match="exactly once"):
        G.apply(text.replace(G.END, ""))
    with pytest.raises(G.MarkerError, match="exactly once"):
        G.apply(text.replace(G.START, ""))


def test_a_duplicated_marker_fails_clearly(text):
    with pytest.raises(G.MarkerError, match="exactly once"):
        G.apply(text + "\n" + G.START + "\n" + G.END + "\n")


def test_reversed_markers_fail(text):
    swapped = text.replace(G.START, "@@S@@").replace(G.END, G.START).replace("@@S@@", G.END)
    with pytest.raises(G.MarkerError):
        G.apply(swapped)
