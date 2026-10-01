"""Publication Standard v1 §5 (brief W2): the registry is the one source of identity and status.

Every generation, branch, reference, study arm and control is registered with every §5 field; each
policy keeps one identity across experiment codes; and every surface derives its names, statuses
and order from the registry. The consistency checks fail when a registered generation lacks a
derived surface and when a surface names an unregistered entry -- each shown by a negative control.
"""

from __future__ import annotations

import json
import re
import sys

import pytest

from delu_forecast import publication_lint as L
from delu_forecast import registry as G
from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

PAGE = REPO_ROOT / "docs" / "index.html"
README = REPO_ROOT / "README.md"
EXPORT = REPO_ROOT / "reports" / "presentation" / "mlflow-export"


@pytest.fixture(scope="module")
def page() -> str:
    return PAGE.read_text()


@pytest.fixture(scope="module")
def readme() -> str:
    return README.read_text()


@pytest.fixture(scope="module")
def export() -> dict:
    return {name: json.loads((EXPORT / f"{name}.json").read_text()) for name in ("manifest", *G.parent_run_keys())}


# --------------------------------------------------------------------------- the entries (§5 fields)


def test_every_kind_the_standard_names_is_registered():
    kinds = {entry.kind for entry in G.entries()}
    assert kinds == set(G.KINDS)
    assert [entry.version for entry in G.generations()] == ["v1", "v2", "v3", "v4"]
    assert {entry.id for entry in G.branches()} == {"calibration", "model-comparison"}
    assert {entry.primary_code for entry in G.of_kind("reference")} == {"B0", "B2", "B3"}
    assert {entry.code_in("CP-15") for entry in G.of_kind("study arm") if entry.code_in("CP-15")} == {
        "A1", "A2", "A3", "A4", "A5"}
    assert [entry.primary_code for entry in G.of_kind("control")] == ["V2-P"]


@pytest.mark.parametrize("entry", G.entries(), ids=lambda entry: entry.id)
def test_every_entry_carries_every_section_5_field(entry):
    assert entry.id and entry.name and entry.kind in G.KINDS
    assert 1 <= len(entry.subtitle.split()) <= 8, f"{entry.id}: a subtitle is at most eight words"
    assert entry.codes, f"{entry.id}: no experiment code"
    for event in entry.statuses:
        assert event.status in G.STATUSES and re.fullmatch(r"\d{4}-\d{2}-\d{2}", event.date) and event.source
    if entry.kind != "reference":
        assert entry.statuses, f"{entry.id}: a {entry.kind} has a dated status"
    assert entry.comparator is None or G.get(entry.comparator)
    assert entry.population in G.POPULATIONS
    assert entry.evidence_class in G.BADGES
    assert entry.plan
    assert all(rule in G.RULES for rule in entry.rules)
    assert entry.sources and all((REPO_ROOT / path).is_file() for path in entry.sources)
    assert entry.claim_map is None or (REPO_ROOT / entry.claim_map).is_file()
    assert entry.run_keys


def test_generation_names_follow_the_naming_rule():
    """`vN · <adopted change>` for generations; a number only after adoption (plan §16 decision 2)."""
    for entry in G.entries():
        numbered = re.match(r"^v\d+ · ", entry.name) is not None
        assert numbered == (entry.kind == "generation"), entry.name
        if entry.kind == "generation":
            assert entry.status.status in (G.ADOPTED_IN_RESEARCH, G.RELEASED, G.FINAL_CANDIDATE, G.LIVE)


def test_one_identity_across_experiment_codes():
    assert G.by_code("H0") is G.by_code("V2-H") is G.get("v2")
    assert G.by_code("B1") is G.by_code("v1_reference") is G.get("v1")
    assert G.generation_of("H0") == G.generation_of("V2-H") == "v2"
    assert G.generation_of("B2") is None and G.generation_of("V2-P") is None


def test_status_is_derived_and_dated():
    assert G.current_generation().version == "v4"
    assert G.released().version == "v1"
    assert G.hero().version == "v1", "the released model outranks a research generation (standard §2)"
    assert G.status_sentence(G.get("v3")) == "In September 2026, v3 was adopted in research."
    assert G.status_sentence(G.get("v4")) == "In September 2026, v4 was adopted in research."
    assert G.status_sentence(G.get("calibration")) == "In September 2026, the calibration experiment was not adopted."


def test_negative_control_a_second_released_model_is_refused(monkeypatch):
    v3 = G.get("v3")
    twin = G.Entry(**{**v3.__dict__, "statuses": v3.statuses + (G.StatusEvent(G.RELEASED, "2026-10-01", "test"),)})
    monkeypatch.setattr(G, "_ENTRIES", tuple(twin if entry.id == "v3" else entry for entry in G._ENTRIES))
    G.entries.cache_clear(), G._by_id.cache_clear(), G._by_code.cache_clear()
    try:
        with pytest.raises(G.RegistryError):
            G.released()
    finally:
        monkeypatch.undo()
        G.entries.cache_clear(), G._by_id.cache_clear(), G._by_code.cache_clear()


def test_the_comparison_refuses_a_mix_of_populations(monkeypatch):
    monkeypatch.setattr(G, "COMPARISON_ORDER", G.COMPARISON_ORDER + ("cp10-head-spread",))
    with pytest.raises(G.RegistryError):
        G.comparison_rows()


def test_every_run_key_is_owned_once():
    owners = [key for entry in G.entries() for key in entry.run_keys]
    assert len(owners) == len(set(owners))
    assert sorted(owners) == sorted(G.expected_run_keys())
    for checkpoint in G.CHECKPOINTS.values():
        assert G.entry_for_run_key(checkpoint.run_key).id == checkpoint.owner


# --------------------------------------------------------------------------- surfaces derive from it


def test_the_page_derives_from_the_registry(page):
    assert L.page_consistency_problems(page) == []


def test_the_readme_derives_from_the_registry(readme):
    assert L.readme_consistency_problems(readme) == []


def test_the_export_derives_from_the_registry(export):
    assert L.export_consistency_problems(export) == []


def test_negative_control_a_generation_without_its_chapter_is_caught(page):
    broken = re.sub(r'<article class="chapter" id="v2".*?</article>', "", page, count=1, flags=re.DOTALL)
    assert any("v2 has no chapter" in problem for problem in L.page_consistency_problems(broken))


def test_negative_control_a_generation_missing_from_the_rail_is_caught(page):
    start = page.index('<nav class="rail"')
    end = page.index("</nav>", start)
    broken = page[:start] + page[start:end].replace('href="#v3"', 'href="#top"') + page[end:]
    assert any("v3 is missing from the rail" in problem for problem in L.page_consistency_problems(broken))


def test_negative_control_an_unregistered_generation_on_the_page_is_caught(page):
    start = page.index('<nav class="jump"')
    broken = page[:start] + page[start:].replace("</nav>", '<a href="#v5">v5</a></nav>', 1)
    assert any("names v5, which is not registered" in problem for problem in L.page_consistency_problems(broken))


def test_negative_control_a_missing_readme_heading_is_caught(readme):
    heading = next(line for line in readme.splitlines()
                   if line.startswith("#") and (" v3 · " in line or line.lstrip("# ").startswith("v3 · ")))
    broken = readme.replace(heading + "\n", "", 1)
    assert any("v3 has no heading" in problem for problem in L.readme_consistency_problems(broken))


def test_negative_control_an_unregistered_readme_heading_is_caught(readme):
    broken = readme + "\n### v5 · something unregistered\n"
    assert any("unregistered generation" in problem for problem in L.readme_consistency_problems(broken))


def test_negative_control_an_unregistered_run_is_caught(export):
    broken = json.loads(json.dumps(export))
    stray = json.loads(json.dumps(broken["cp20"]["runs"][-1]))
    stray["run_key"] = "cp20/H9"
    broken["cp20"]["runs"].append(stray)
    assert any("cp20/H9 is not registered" in problem for problem in L.export_consistency_problems(broken))
    broken["cp20"]["runs"] = broken["cp20"]["runs"][:1]
    assert any("cp20/HG is missing" in problem for problem in L.export_consistency_problems(broken))
