"""CP-3 item 5: "Limitations and reproduction instructions are complete."

§10 item (11) enumerates the set. Completeness was previously a matter of three
documents having been written carefully, and it failed the way that always fails:
the 15-minute-MTU averaging limitation sat on the Pages export and on neither
other surface. Each limitation is now one string rendered onto every human
surface from `delu_forecast.claims`, and this asserts it.

The reproduction half is checked too: a reader must be able to get from any
surface to a command that runs.

**Per model** (Publication Standard v1 §8, re-scoping plan invariant 5, approved at ratification as
D2): a model's limitations appear on every surface that presents that model -- the demo, the Space
card, its chapter and its README section. v1's set is checked on v1's surfaces; each research
generation's limitations on its chapter and its README section.
"""

from __future__ import annotations

import pytest

from delu_forecast import registry as G
from delu_forecast import research_claims as RC
from delu_forecast.claims import (
    LIMITATION_KEYS,
    LIMITATION_LABELS,
    LIMITATION_TOPICS,
    REPRODUCIBILITY_KEYS,
    REPRODUCIBILITY_LABELS,
    REPRODUCIBILITY_TOPICS,
    build_claims,
    limitation_bullets,
    reproducibility_bullets,
)
from delu_forecast.surfaces import (
    PAGES_PATH,
    README_PATH,
    SPACE_CARD_PATH,
    STATIC_SPACE_CARD_PATH,
    Surface,
    html_to_text,
    normalise,
)

#: The MLflow record carries tags, not prose, so the limitations set is asserted on the human
#: surfaces that present v1: its README section, both Space cards and its chapter on the page.
HUMAN_SURFACES = ("README", "Space card", "Static Space card", "Pages export")


def readme_section(text: str, entry: G.Entry) -> str:
    """A generation's README section: from its registry heading to the next heading of that level."""
    start = text.index(f"\n### {entry.name}\n")
    end = text.find("\n### ", start + 1)
    return text[start:end if end >= 0 else len(text)]


def page_chapter(document: str, entry: G.Entry) -> str:
    start = document.index(f'<article class="chapter" id="{entry.id}"')
    return document[start:document.index("</article>", start)]


@pytest.fixture(scope="module")
def human_surfaces() -> list[Surface]:
    v1 = G.released()
    return [
        Surface("README", README_PATH, normalise(readme_section(README_PATH.read_text(), v1))),
        Surface("Space card", SPACE_CARD_PATH, normalise(SPACE_CARD_PATH.read_text())),
        Surface("Static Space card", STATIC_SPACE_CARD_PATH, normalise(STATIC_SPACE_CARD_PATH.read_text())),
        Surface("Pages export", PAGES_PATH, html_to_text(page_chapter(PAGES_PATH.read_text(), v1))),
    ]


@pytest.fixture(scope="module")
def whole_surfaces() -> list[Surface]:
    """Every human surface in full: reproduction and attribution are not per model."""
    return [
        Surface("README", README_PATH, normalise(README_PATH.read_text())),
        Surface("Space card", SPACE_CARD_PATH, normalise(SPACE_CARD_PATH.read_text())),
        Surface("Static Space card", STATIC_SPACE_CARD_PATH, normalise(STATIC_SPACE_CARD_PATH.read_text())),
        Surface("Pages export", PAGES_PATH, html_to_text(PAGES_PATH.read_text())),
    ]


def test_the_demo_renders_every_one_of_v1s_limitations():
    """The demo presents v1, so it carries v1's whole set: it renders every `limitation_` claim."""
    from delu_forecast.claims import REPO_ROOT

    notebook = (REPO_ROOT / "app" / "wasm_showcase.py").read_text()
    assert 'k.startswith("limitation_")' in notebook and "CLAIMS['holdout_limitation']" in notebook
    assert all(key.startswith("limitation_") for key in LIMITATION_KEYS)


RESEARCH_LIMITATIONS = {
    "v3": ("v3.caveat.bundle", "v3.caveat.fold3", "v3.caveat.class"),
    "v2": ("v2.caveat.attribution", "v2.caveat.split", "v2.caveat.class"),
}


@pytest.mark.parametrize("version", sorted(RESEARCH_LIMITATIONS))
def test_each_research_generations_limitations_are_on_its_chapter_and_its_readme_section(version):
    entry = G.get(version)
    chapter = page_chapter(PAGES_PATH.read_text(), entry)
    section = readme_section(README_PATH.read_text(), entry)
    for key in RESEARCH_LIMITATIONS[version]:
        assert RC.render(key) in chapter, (version, key, "chapter")
        assert RC.render(key, "md", surface=RC.README) in section, (version, key, "README section")


def test_negative_control_a_research_limitation_dropped_from_its_readme_section_is_caught():
    entry = G.get("v3")
    section = readme_section(README_PATH.read_text(), entry)
    dropped = section.replace(RC.render("v3.caveat.bundle", "md", surface=RC.README), "")
    assert RC.render("v3.caveat.bundle", "md", surface=RC.README) not in dropped


def test_the_set_covers_every_topic_section_10_item_11_names():
    """The plan's own list, transcribed once and checked against the claim keys."""
    assert set(LIMITATION_TOPICS) == {
        "exchangeability",
        "evidence_distinction",
        "assumption_a65",
        "assumption_a75",
        "strict_gate_cost",
        "bounded_tail",
        "coverage_divergence",
        "staleness",
        "mtu_averaging",
        "not_an_operations_system",
    }
    assert set(LIMITATION_LABELS) == set(LIMITATION_KEYS)
    assert len(limitation_bullets(build_claims())) == len(LIMITATION_KEYS)


@pytest.mark.parametrize("key", LIMITATION_KEYS)
def test_every_limitation_appears_on_every_human_surface(human_surfaces, key):
    claims = build_claims()
    missing = [surface.name for surface in human_surfaces if not surface.carries(key, claims[key])]
    assert not missing, f"{key} missing from: {', '.join(missing)}"


def test_the_staleness_limitation_names_all_four_cutoffs():
    claims = build_claims()
    text = claims["limitation_staleness"]
    for key in ("snapshot_cutoff", "raw_model_fit_cutoff", "final_calibration_window", "holdout_window"):
        assert claims[key] in text, f"{key} absent from the staleness limitation"


def test_positive_control_a_limitation_dropped_from_one_surface_is_caught(human_surfaces):
    """The exact defect the round-1 Critic found: present on one surface only."""
    claims = build_claims()
    key = "limitation_mtu_averaging"
    readme = next(surface for surface in human_surfaces if surface.name == "README")
    stripped = Surface(readme.name, readme.path, readme.text.replace(normalise(claims[key]), ""))
    assert stripped.text != readme.text, "the control did not modify anything"
    assert not stripped.carries(key, claims[key])
    others = [surface for surface in human_surfaces if surface.name != "README"]
    assert all(surface.carries(key, claims[key]) for surface in others), (
        "the control is meaningless unless the other surfaces still carry it"
    )


def test_reproduction_instructions_are_runnable_on_every_human_surface(whole_surfaces):
    """A reader must reach a command, not a description of one."""
    for surface in whole_surfaces:
        text = surface.text
        assert "uv sync" in text, f"{surface.name} does not say how to install"
        assert "predict_next_day.py" in text, f"{surface.name} does not say how to run the model"
        assert "docker" in text.lower(), f"{surface.name} does not say how to run the container"
        if surface.name != "README":
            # The README is served from the repository, so it need not link it;
            # a reader who lands on the Space or the page must be able to get there.
            assert "github.com/hrsi56/delu-day-ahead-forecast" in text, surface.name


def test_the_floor_change_one_liner_is_present_where_the_plan_requires_it(human_surfaces):
    """§9.3: a second one-liner notes the floor change to −600 EUR/MWh from 2026-05-28."""
    claims = build_claims()
    for surface in human_surfaces:
        assert surface.carries("floor_change", claims["floor_change"]), surface.name
    assert "2026-05-28" in claims["floor_change"]
    assert "600" in claims["floor_change"]


# -- §10 item (12): the reproducibility statement -----------------------------


def test_the_set_covers_every_element_section_10_item_12_names():
    """The plan's own list, transcribed once and checked against the claim keys."""
    assert set(REPRODUCIBILITY_TOPICS) == {
        "tagged_commit",
        "mlflow_permalink",
        "registered_champion",
        "pages_canonical",
        "duckdb_sql",
        "four_cutoffs",
        "attribution",
    }
    assert set(REPRODUCIBILITY_LABELS) == set(REPRODUCIBILITY_KEYS)
    assert len(reproducibility_bullets(build_claims())) == len(REPRODUCIBILITY_KEYS)


@pytest.mark.parametrize("key", REPRODUCIBILITY_KEYS)
def test_every_reproducibility_element_appears_on_every_human_surface(whole_surfaces, key):
    claims = build_claims()
    missing = [surface.name for surface in whole_surfaces if not surface.carries(key, claims[key])]
    assert not missing, f"{key} missing from: {', '.join(missing)}"


def test_the_registered_champion_element_names_the_model_and_the_alias():
    """The round-2 defect: §10 item (12) requires the registered `champion` alias
    in the reproducibility statement, and it was on none of the three surfaces."""
    import json

    from delu_forecast.claims import REPO_ROOT

    text = build_claims()["repro_registered_champion"]
    record = json.loads((REPO_ROOT / "reports" / "cp3" / "mlflow_registration.json").read_text())
    assert record["registered_model"] in text
    assert f"`{record['alias']}` alias" in text
    assert "release" in text and "lineage" in text
    # ...and says plainly that it is evidence, not a runtime dependency (§9.1).
    assert "never queries the registry" in text


def test_positive_control_a_reproducibility_element_dropped_is_caught(whole_surfaces):
    claims = build_claims()
    key = "repro_registered_champion"
    card = next(surface for surface in whole_surfaces if surface.name == "Space card")
    stripped = Surface(card.name, card.path, card.text.replace(normalise(claims[key]), ""))
    assert stripped.text != card.text, "the control did not modify anything"
    assert not stripped.carries(key, claims[key])
    others = [surface for surface in whole_surfaces if surface.name != "Space card"]
    assert all(surface.carries(key, claims[key]) for surface in others)


def test_the_four_cutoffs_element_names_all_four():
    claims = build_claims()
    text = claims["repro_four_cutoffs"]
    for key in ("snapshot_cutoff", "raw_model_fit_cutoff", "final_calibration_window", "holdout_window"):
        assert claims[key] in text, f"{key} absent from the four-cutoffs element"
