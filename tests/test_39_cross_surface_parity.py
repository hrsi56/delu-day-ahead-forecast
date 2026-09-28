"""Publication Standard v1 §8 (brief W9): the headline block, names and statuses agree on every surface.

`scripts/verify_release.py` extends the CP-3 agreement check with this parity check; here it runs
on the committed surfaces -- the page, the README, both Space cards and the MLflow export -- and on
deliberately broken copies: a changed headline, a name that is not the registry's, an unregistered
generation and a status the registry does not hold.
"""

from __future__ import annotations

import sys

import pytest

from delu_forecast import publication_lint as L
from delu_forecast import registry as G
from delu_forecast import research_claims as RC
from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import verify_release  # noqa: E402


@pytest.fixture(scope="module")
def surfaces() -> dict[str, str]:
    return L.surface_texts(REPO_ROOT)


def test_the_committed_surfaces_agree():
    assert verify_release.parity_problems() == []


def test_verify_release_runs_the_parity_check(capsys):
    assert verify_release.main() == 0
    assert "Cross-surface parity" in capsys.readouterr().out


def test_the_space_card_takes_its_model_line_from_the_registry(surfaces):
    card = surfaces["Static Space card"]
    released = G.released()
    assert f"**Model: {released.name}.** {G.status_sentence(released)} {G.release_sentence()}" in card


def test_negative_control_a_changed_headline_is_caught(surfaces):
    problems = L.parity_problems(surfaces, page_headline=RC.headline(),
                                 readme_headline=RC.headline("md").replace("14%", "15%"))
    assert any(problem.startswith("headline:") for problem in problems)


def test_negative_control_a_non_canonical_name_is_caught(surfaces):
    doctored = {**surfaces, "README": surfaces["README"] + "\n### v2 · hour-aware intervals\n"}
    problems = L.parity_problems(doctored, page_headline=RC.headline(), readme_headline=RC.headline("md"))
    assert any("not the canonical name" in problem for problem in problems)


def test_negative_control_an_unregistered_generation_is_caught(surfaces):
    doctored = {**surfaces, "Static Space card": surfaces["Static Space card"] + "\nv4 · something new\n"}
    problems = L.parity_problems(doctored, page_headline=RC.headline(), readme_headline=RC.headline("md"))
    assert any("v4 is not a registered generation" in problem for problem in problems)


def test_negative_control_a_status_the_registry_does_not_hold_is_caught(surfaces):
    doctored = {**surfaces, "page": surfaces["page"] + "<p>In October 2026, v3 was released.</p>"}
    problems = L.parity_problems(doctored, page_headline=RC.headline(), readme_headline=RC.headline("md"))
    assert any("is not the registry's" in problem for problem in problems)
