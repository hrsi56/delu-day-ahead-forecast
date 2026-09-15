"""CP-3 item 5: the four public surfaces agree, and the check can fail.

Item 5 is the one that catches drift, so the risk is a check that passes because
it cannot fail. Every assertion here is paired with a positive control: a
deliberately corrupted copy of a surface that the same code must reject.
"""

from __future__ import annotations

import json

import pytest

from delu_forecast.claims import REQUIRED_ON_EVERY_SURFACE, build_claims, forbidden_dagshub_links
from delu_forecast.surfaces import (
    CUTOFF_KEYS,
    MLFLOW_TAG_FOR_CLAIM,
    Surface,
    agreement_matrix,
    disagreements,
    html_to_text,
    link_discipline_failures,
    load_surfaces,
    normalise,
)


@pytest.fixture(scope="module")
def surfaces() -> list[Surface]:
    return load_surfaces()


def test_every_bound_surface_exists(surfaces):
    names = {surface.name for surface in surfaces}
    assert names == {"README", "Space card", "Static Space card", "Pages export", "MLflow record"}
    for surface in surfaces:
        assert surface.path.exists(), surface.path
        assert surface.text, f"{surface.name} is empty"


def test_every_bound_claim_appears_on_every_surface(surfaces):
    problems = disagreements(surfaces)
    assert not problems, "cross-surface disagreement:\n  " + "\n  ".join(problems)


def test_all_four_cutoffs_appear_separately_and_identically(surfaces):
    """Item 5 names the cutoffs separately, so they are checked separately."""
    claims = build_claims()
    values = {claims[key] for key in CUTOFF_KEYS}
    assert len(values) == len(CUTOFF_KEYS), "the four cutoffs must be four distinct strings"
    for key in CUTOFF_KEYS:
        for surface in surfaces:
            assert surface.carries(key, claims[key]), f"{surface.name} lacks {key}={claims[key]}"


def test_no_surface_links_a_gated_dagshub_path(surfaces):
    """A link to the repo UI lands an anonymous reader on a sign-in page."""
    assert not link_discipline_failures(surfaces)
    for surface in surfaces:
        assert "dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow" in surface.path.read_text(), (
            f"{surface.name} does not link the anonymously-readable tracking URI"
        )


# -- positive controls: the checks above must be able to fail -----------------


def test_positive_control_a_reworded_number_is_caught(surfaces):
    """Round one published metric differently and the matrix must go red."""
    claims = build_claims()
    readme = next(surface for surface in surfaces if surface.name == "README")
    corrupted = Surface(
        readme.name,
        readme.path,
        readme.text.replace(claims["holdout_mae_champion"], "25.91"),
    )
    assert corrupted.text != readme.text, "the control did not modify anything"
    others = [surface for surface in surfaces if surface.name != "README"]
    problems = disagreements([corrupted, *others])
    assert any("holdout_mae_champion" in problem for problem in problems), problems


def test_positive_control_a_swapped_cutoff_is_caught(surfaces):
    """Swap two of the four cutoffs and the separate-cutoff check must fail."""
    claims = build_claims()
    card = next(surface for surface in surfaces if surface.name == "Space card")
    swapped = Surface(
        card.name,
        card.path,
        card.text.replace(claims["raw_model_fit_cutoff"], "2026-09-06"),
    )
    assert not swapped.carries("raw_model_fit_cutoff", claims["raw_model_fit_cutoff"])


def test_positive_control_a_missing_verbatim_paragraph_is_caught(surfaces):
    """Drop the power-qualification label from one surface; it must be reported."""
    claims = build_claims()
    pages = next(surface for surface in surfaces if surface.name == "Pages export")
    stripped = Surface(
        pages.name, pages.path, pages.text.replace(normalise(claims["holdout_dm_label"]), "")
    )
    others = [surface for surface in surfaces if surface.name != "Pages export"]
    problems = disagreements([stripped, *others])
    assert any("holdout_dm_label" in problem for problem in problems), problems


def test_positive_control_a_gated_dagshub_link_is_caught():
    for bad in (
        "see https://dagshub.com/hrsi56/delu-day-ahead-forecast/experiments for runs",
        "code at https://dagshub.com/hrsi56/delu-day-ahead-forecast/src/main",
        "tracking at https://dagshub.com/hrsi56/delu-day-ahead-forecast ",
    ):
        assert forbidden_dagshub_links(bad), f"not caught: {bad}"
    good = "runs at https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow — anonymous"
    assert not forbidden_dagshub_links(good)


def test_positive_control_mlflow_tag_match_is_exact():
    """A tag that merely contains the claim is a miss, not a hit."""
    claims = build_claims()
    key = "selected_catalog"
    tag = MLFLOW_TAG_FOR_CLAIM.get(key, key)
    exact = Surface("MLflow record", __file__, "", tags={tag: claims[key]})
    loose = Surface("MLflow record", __file__, "", tags={tag: claims[key] + "_plus"})
    assert exact.carries(key, claims[key])
    assert not loose.carries(key, claims[key])


def test_html_to_text_does_not_invent_adjacency():
    """Stripping tags must not fuse two cells into a claim nobody published."""
    assert "ab" not in html_to_text("<td>a</td><td>b</td>")
    assert "a b" in html_to_text("<td>a</td><td>b</td>")


# -- the MLflow surface is a real record of a real registration ---------------


def test_mlflow_record_describes_the_shipped_artifact():
    from delu_forecast.surfaces import MLFLOW_RECORD_PATH

    claims = build_claims()
    record = json.loads(MLFLOW_RECORD_PATH.read_text())
    assert record["registered_model"] == "delu-day-ahead-champion"
    assert record["alias"] == "champion"
    assert record["local_artifact_fingerprint_sha256"] == claims["champion_fingerprint"]
    assert record["fingerprint_matches_champion_card"] is True
    assert record["version_tags"]["release_status"] == "portfolio_release"
    for key in ("source_run_id", "code_commit", "snapshot_sha256", *CUTOFF_KEYS):
        assert record["version_tags"].get(key), f"lineage tag {key} missing from the record"
    # §9.1 makes registration non-gating, so a disclosed failure is allowed --
    # what is not allowed is an undisclosed one.
    assert "failures" in record, "a registration record must state its failures, even when empty"


def test_every_required_claim_key_resolves():
    claims = build_claims()
    for key in REQUIRED_ON_EVERY_SURFACE:
        assert claims[key], f"claim {key} is empty"


def test_the_published_artifact_size_ignores_transient_bytecode(tmp_path, monkeypatch):
    """A published number must not depend on whether the model was loaded first.

    MLflow adds `models/champion/code` to `sys.path` when it loads the pyfunc, and
    under some import orders Python writes `__pycache__` there. Before this was
    excluded, `champion_dir_bytes` — printed on all four surfaces — moved by tens
    of kilobytes depending on execution order.
    """
    import json
    import shutil

    from delu_forecast import claims as claims_module

    root = tmp_path / "repo"
    (root / "models" / "champion" / "code" / "delu_forecast").mkdir(parents=True)
    real = claims_module.REPO_ROOT
    for relative in (
        "models/champion/champion_card.json",
        "models/champion/python_model.pkl",
        "reports/cp2/holdout_report.json",
        "reports/cp2/catalog_selection.json",
        "reports/cp2/a69_benchmark.json",
        "reports/cp2/dm_development.json",
        "reports/cp2/development_pooled_metrics.csv",
        "reports/cp3b/network.json",
        "reports/cp3b/equivalence.json",
    ):
        (root / relative).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(real / relative, root / relative)

    def size(with_cache: bool) -> str:
        cache = root / "models" / "champion" / "code" / "delu_forecast" / "__pycache__"
        if with_cache:
            cache.mkdir(exist_ok=True)
            (cache / "claims.cpython-313.pyc").write_bytes(b"x" * 73_554)
        elif cache.exists():
            shutil.rmtree(cache)
        monkeypatch.setattr(claims_module, "REPO_ROOT", root)
        claims_module.build_claims.cache_clear()
        return claims_module.build_claims()["champion_dir_bytes"]

    try:
        clean, polluted = size(False), size(True)
        assert clean == polluted, (
            f"the published directory size moved when bytecode appeared: {clean} -> {polluted}"
        )
        # Positive control: the sum is real, not a hardcoded constant.
        (root / "models" / "champion" / "extra.bin").write_bytes(b"y" * 1000)
        claims_module.build_claims.cache_clear()
        assert claims_module.build_claims()["champion_dir_bytes"] != clean
    finally:
        monkeypatch.undo()
        claims_module.build_claims.cache_clear()
        assert json.loads((real / "models/champion/champion_card.json").read_text())
