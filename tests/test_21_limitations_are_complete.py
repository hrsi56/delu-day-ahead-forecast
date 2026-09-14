"""CP-3 item 5: "Limitations and reproduction instructions are complete."

§10 item (11) enumerates the set. Completeness was previously a matter of three
documents having been written carefully, and it failed the way that always fails:
the 15-minute-MTU averaging limitation sat on the Pages export and on neither
other surface. Each limitation is now one string rendered onto every human
surface from `delu_forecast.claims`, and this asserts it.

The reproduction half is checked too: a reader must be able to get from any
surface to a command that runs.
"""

from __future__ import annotations

import pytest

from delu_forecast.claims import (
    LIMITATION_KEYS,
    LIMITATION_LABELS,
    LIMITATION_TOPICS,
    build_claims,
    limitation_bullets,
)
from delu_forecast.surfaces import (
    PAGES_PATH,
    README_PATH,
    SPACE_CARD_PATH,
    Surface,
    html_to_text,
    normalise,
)

#: The MLflow record carries tags, not prose, so the limitations set is asserted
#: on the three human surfaces. §10 item (11) is a reading-order requirement.
HUMAN_SURFACES = ("README", "Space card", "Pages export")


@pytest.fixture(scope="module")
def human_surfaces() -> list[Surface]:
    return [
        Surface("README", README_PATH, normalise(README_PATH.read_text())),
        Surface("Space card", SPACE_CARD_PATH, normalise(SPACE_CARD_PATH.read_text())),
        Surface("Pages export", PAGES_PATH, html_to_text(PAGES_PATH.read_text())),
    ]


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


def test_reproduction_instructions_are_runnable_on_every_human_surface(human_surfaces):
    """A reader must reach a command, not a description of one."""
    for surface in human_surfaces:
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
