"""CP-3 items 1, 2 and 4: the release surfaces say what the plan requires.

The replay label is a truthfulness requirement, not a caption (§9.2), and the
scenario control must be labelled a sensitivity probe. Both are asserted on the
artifacts themselves -- the app source, the static page and the Space card --
rather than on a promise that they are there.
"""

from __future__ import annotations

import json
import re

import pytest

from delu_forecast.claims import REPLAY_LABEL, SENSITIVITY_PROBE_LABEL, REPO_ROOT, build_claims
from delu_forecast.showcase import INTERVAL_LEVELS

APP = REPO_ROOT / "app" / "showcase.py"
PAGE = REPO_ROOT / "docs" / "index.html"
CARD = REPO_ROOT / "space" / "README.md"
DOCKERFILE = REPO_ROOT / "Dockerfile"
CLI = REPO_ROOT / "predict_next_day.py"


def test_the_replay_label_is_on_every_surface_that_shows_the_holdout():
    """§9.2: labelled 'in those words', never presented as a live forecast."""
    for path in (PAGE, CARD):
        assert REPLAY_LABEL in path.read_text(), path
    assert "historical out-of-sample replay" in PAGE.read_text().lower()
    # The app renders it from the claim set, so the reference is what to check.
    assert "replay_label" in APP.read_text()
    assert "historical out-of-sample replay" in APP.read_text().lower()


#: "live forecasting" is §7.1's description of how lag features behave and is not
#: a claim about this demo, so the noun phrase is matched and the gerund is not.
_LIVE_FORECAST = re.compile(r"\ba live forecast\b", re.IGNORECASE)


def test_no_surface_calls_the_replay_a_live_forecast():
    for path in (PAGE, CARD, APP, CLI):
        text = path.read_text()
        lowered = text.lower()
        for phrase in ("live forecast for", "today's forecast", "real-time forecast"):
            assert phrase not in lowered, f"{path}: {phrase}"
        for match in _LIVE_FORECAST.finditer(text):
            # The only permitted use is the denial, so look at the clause before it.
            window = lowered[max(0, match.start() - 90) : match.end()]
            assert "not" in window or "never" in window, f"{path}: ...{window}"


def test_the_scenario_control_is_labelled_a_sensitivity_probe():
    for path in (PAGE, CARD):
        assert SENSITIVITY_PROBE_LABEL in path.read_text(), path
    assert "sensitivity_probe_label" in APP.read_text()


def test_only_two_controls_exist_and_they_are_the_permitted_ones():
    """§9.2 fixes the quantile selector and allows at most one more control."""
    source = APP.read_text()
    widgets = re.findall(r"mo\.ui\.(\w+)\(", source)
    interactive = [name for name in widgets if name not in {"table"}]
    assert sorted(interactive) == ["radio", "slider"], interactive
    assert "Prediction-interval level" in source
    assert "Load-forecast scenario" in source
    for forbidden in ("shap.", "precomputed_grid", "ood_", "nearest_neighbour"):
        assert forbidden not in source, f"retired v6.3 machinery reappeared: {forbidden}"


def test_the_quantile_selector_annotates_empirical_coverage():
    claims = build_claims()
    source = APP.read_text()
    page = PAGE.read_text()
    assert "holdout_coverage_" in source
    for level in INTERVAL_LEVELS:
        assert claims[f"holdout_coverage_{level}"] in page, level


def test_the_app_runs_marimo_in_server_mode_not_wasm():
    dockerfile = DOCKERFILE.read_text()
    assert 'CMD ["marimo", "run"' in dockerfile, "§9.2 requires `marimo run`, not WASM"
    assert "export html-wasm" not in dockerfile
    assert "--headless" in dockerfile


def test_the_container_bundles_the_champion_and_the_snapshot():
    """§9.2: the champion loads from the image; no registry, no live pull."""
    dockerfile = DOCKERFILE.read_text()
    assert "models/champion/" in dockerfile
    assert "data/snapshot.parquet" in dockerfile
    # Comments explain what was deleted and must not be mistaken for the thing.
    instructions = "\n".join(
        line for line in dockerfile.splitlines() if line.strip() and not line.lstrip().startswith("#")
    )
    for secret in ("MLFLOW_TRACKING_URI", "DAGSHUB", "ENTSOE_API_TOKEN", "HF_TOKEN"):
        assert secret not in instructions.upper(), f"the runtime must not carry {secret}"
    assert "--mount=type=secret" not in instructions


def test_the_space_card_declares_the_docker_sdk_and_matching_port():
    text = CARD.read_text()
    assert text.startswith("---\n"), "the HF card needs YAML front-matter"
    front = text.split("---", 2)[1]
    assert re.search(r"^sdk:\s*docker\s*$", front, re.MULTILINE)
    port = re.search(r"^app_port:\s*(\d+)\s*$", front, re.MULTILINE)
    assert port, "app_port must be declared"
    assert f"--port\", \"{port.group(1)}\"" in DOCKERFILE.read_text()
    assert f"EXPOSE {port.group(1)}" in DOCKERFILE.read_text()


def test_the_space_link_discloses_what_a_visit_actually_costs_and_is_not_gated():
    """CP-3B: a Static Space cannot sleep, so the old ~30 s wake-up label became
    false. The cost a visitor pays is download weight, measured; the label says
    that, and the container card says plainly why it is not the hosted demo."""
    claims = build_claims()
    assert "wake" not in claims["space_link_label"] and "asleep" not in claims["space_link_label"]
    assert claims["wasm_cold_load_mb"] in claims["space_link_label"]
    assert claims["space_link_label"] in PAGE.read_text()
    assert "sleep" in CARD.read_text().lower(), "the container card must say why it is not hosted"
    # §9.2 retired every timing threshold; none may reappear as a gate.
    for path in (CARD, PAGE, APP):
        text = path.read_text()
        assert "<3 s" not in text and "under 3 seconds" not in text.lower()


def test_the_cli_defaults_to_the_bundled_offline_source():
    source = CLI.read_text()
    assert 'default="bundled"' in source
    assert "predict_next_day.py" in (REPO_ROOT / "Dockerfile").read_text()
    assert "--self-check" in source


def test_the_space_bundle_manifest_lists_what_the_image_needs():
    manifest = json.loads((REPO_ROOT / "reports" / "cp3" / "space_bundle.json").read_text())
    required = {"Dockerfile", "README.md", "src", "app", "models/champion", "data/snapshot.parquet"}
    assert required <= set(manifest["paths"]), required - set(manifest["paths"])
    assert manifest["sdk"] == "docker"
    assert manifest["app_port"] == 7860


@pytest.mark.parametrize("path", [PAGE, CARD])
def test_attribution_and_the_floor_change_are_disclosed(path):
    claims = build_claims()
    text = path.read_text()
    assert claims["attribution"] in text or "CC BY 4.0" in text
    assert "2026-05-28" in text or path is CARD


def test_the_pages_export_carries_the_whole_section_10_reading_order():
    """Twelve items, each identifiable on the page."""
    page = PAGE.read_text()
    for anchor in (
        'id="data"', 'id="regimes"', 'id="catalog"', 'id="spectral"', 'id="method"',
        'id="results"', 'id="shap"', 'id="regime-table"', 'id="reliability"',
        'id="forecast"', 'id="limitations"', 'id="repro"',
    ):
        assert anchor in page, anchor


def test_the_container_was_actually_exercised_with_the_network_disabled():
    """Item 1 says the container runs locally. `scripts/verify_container.py`
    records the run; this asserts the record describes a real offline success,
    not an intention. Re-run it with `make container-verify`."""
    record = json.loads((REPO_ROOT / "reports" / "cp3" / "container_check.json").read_text())
    assert record["passed"] is True
    probe = record["steps"]["offline_probe"]["detail"]
    assert probe["app_health_status"] == 200
    assert probe["app_index_bytes"] > 10_000
    for host in ("outbound_network", "cdn.jsdelivr.net", "huggingface.co", "dagshub.com"):
        assert probe[host].startswith("unreachable"), (
            f"{host} was reachable, so the offline run proves nothing"
        )
    cli = record["steps"]["cli_offline"]["detail"]
    assert cli["exit_code"] == 0
    assert cli["delivery_day_prices_change_nothing"] is True
    assert cli["positive_control_d_minus_1_changes_output"] is True
    assert record["steps"]["marimo_server_mode"]["ok"] is True
