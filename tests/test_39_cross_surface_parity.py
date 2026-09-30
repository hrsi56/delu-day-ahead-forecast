"""Publication Standard v1 §8 (brief W9): the headline block, names and statuses agree on every surface.

`scripts/verify_release.py` extends the CP-3 agreement check with this parity check; here it runs
on the committed surfaces -- the page, the README, both Space cards and the MLflow export -- and on
deliberately broken copies: a changed headline, a name that is not the registry's, an unregistered
generation and a status the registry does not hold. Both Space cards carry the registry's model
line and links (`build_space.model_lines`); a card without a required line fails.
"""

from __future__ import annotations

import json
import sys

import pytest

from delu_forecast import publication_lint as L
from delu_forecast import registry as G
from delu_forecast import research_claims as RC
from delu_forecast.claims import REPO_ROOT, build_claims

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import build_space  # noqa: E402
import verify_release  # noqa: E402

CARDS = {"Space card": REPO_ROOT / "space" / "README.md", "Static Space card": REPO_ROOT / "space-wasm" / "README.md"}


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


def test_both_space_cards_carry_every_required_line():
    pages_url = build_claims()["pages_url"]
    lines = build_space.model_lines(pages_url)
    assert lines[0].startswith(f"**Model: {G.released().name}.**") and pages_url in lines[1]
    for name, card in CARDS.items():
        assert build_space.missing_card_lines(card.read_text(), pages_url) == [], name


@pytest.mark.parametrize("name", sorted(CARDS))
def test_negative_control_a_card_without_a_required_line_fails(name):
    pages_url = build_claims()["pages_url"]
    card = CARDS[name].read_text()
    for line in build_space.model_lines(pages_url):
        assert build_space.missing_card_lines(card.replace(line + "\n", "", 1), pages_url) == [line]


def test_negative_control_verify_release_reports_a_card_that_lacks_a_line(monkeypatch):
    monkeypatch.setattr(verify_release, "missing_card_lines", lambda card, url: ["**Model: v1 · released LightGBM.**"])
    problems = verify_release.parity_problems()
    assert any(problem.startswith("Space card: lacks") for problem in problems)
    assert any(problem.startswith("Static Space card: lacks") for problem in problems)


def test_the_mlflow_link_is_required_once_the_verifier_indexed_it(tmp_path):
    """No placeholder: before the index, a card has no MLflow link; after it, a card without one fails."""
    pages_url = build_claims()["pages_url"]
    index = tmp_path / "mlflow_index.json"
    assert "MLflow" not in " ".join(build_space.model_lines(pages_url, index))
    url = "https://dagshub.com/owner/repo.mlflow/#/experiments/1"
    index.write_text(json.dumps({"routes": {"experiment": {"url": url}}}))
    lines = build_space.model_lines(pages_url, index)
    assert f"[the `delu-generations` MLflow experiment]({url})" in lines[1]
    unlinked = build_space.model_lines(pages_url, tmp_path / "absent.json")
    assert build_space.missing_card_lines("\n".join(unlinked), pages_url, index) == [lines[1]]


def test_negative_control_a_changed_headline_is_caught(surfaces):
    problems = L.parity_problems(surfaces, page_headline=RC.headline(),
                                 readme_headline=RC.headline("md").replace("−0.0301", "−0.0302"))
    assert any(problem.startswith("headline:") for problem in problems)


def test_negative_control_a_non_canonical_name_is_caught(surfaces):
    doctored = {**surfaces, "README": surfaces["README"] + "\n### v2 · hour-aware intervals\n"}
    problems = L.parity_problems(doctored, page_headline=RC.headline(), readme_headline=RC.headline("md"))
    assert any("not the canonical name" in problem for problem in problems)


def test_negative_control_an_unregistered_generation_is_caught(surfaces):
    doctored = {**surfaces, "Static Space card": surfaces["Static Space card"] + "\nv5 · something new\n"}
    problems = L.parity_problems(doctored, page_headline=RC.headline(), readme_headline=RC.headline("md"))
    assert any("v5 is not a registered generation" in problem for problem in problems)


def test_negative_control_a_status_the_registry_does_not_hold_is_caught(surfaces):
    doctored = {**surfaces, "page": surfaces["page"] + "<p>In October 2026, v3 was released.</p>"}
    problems = L.parity_problems(doctored, page_headline=RC.headline(), readme_headline=RC.headline("md"))
    assert any("is not the registry's" in problem for problem in problems)
