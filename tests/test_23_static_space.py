"""M3.5/CP-3B items 1, 4 and 5: the Static Space says what is true about itself.

The model-identity gate lives in test_22. This file pins everything around it:
the card declares a Static Space, the notebook keeps §9.2's two-control scope,
the replay and probe labels are present, the measured network record is
internally consistent, and the build refuses to ship an internal file.
"""

from __future__ import annotations

import ast
import json
import re

from delu_forecast.claims import REPLAY_LABEL, SENSITIVITY_PROBE_LABEL, REPO_ROOT, build_claims

NOTEBOOK = REPO_ROOT / "app" / "wasm_showcase.py"
CARD = REPO_ROOT / "space-wasm" / "README.md"
NETWORK = REPO_ROOT / "reports" / "cp3b" / "network.json"
EQUIVALENCE = REPO_ROOT / "reports" / "cp3b" / "equivalence.json"
BUNDLE_MANIFEST = REPO_ROOT / "reports" / "cp3b" / "space_wasm_bundle.json"


def _front_matter() -> dict[str, str]:
    text = CARD.read_text()
    assert text.startswith("---\n"), "the HF card needs YAML front-matter"
    block = text.split("---", 2)[1]
    return {
        line.split(":", 1)[0].strip(): line.split(":", 1)[1].strip()
        for line in block.splitlines()
        if ":" in line and not line.startswith(" ")
    }


# -- the card ----------------------------------------------------------------


def test_the_card_declares_a_public_static_space():
    front = _front_matter()
    assert front["sdk"] == "static", "Docker and Gradio SDKs are paid; only Static is free"
    assert front["app_file"] == "index.html"
    assert len(front["short_description"]) <= 60, "the Hub truncates short_description at 60"


def test_the_card_carries_the_labels_and_the_measured_cost():
    claims = build_claims()
    text = " ".join(CARD.read_text().split())
    assert REPLAY_LABEL in text
    assert SENSITIVITY_PROBE_LABEL in text
    assert " ".join(claims["wasm_cold_load"].split()) in text
    assert claims["wasm_cold_load_bytes"] in text, "publish the number, not an adjective"
    assert " ".join(claims["wasm_identity"].split()) in text
    # Phrases that *assert* a wake-up. "there is no server to wake" is the denial
    # and is correct, so the bare word is not a finding.
    for phrase in ("asleep", "~30 s", "may take", "cold start"):
        assert phrase not in text, f"a Static Space cannot sleep; the card must not say '{phrase}'"


def test_the_card_links_the_static_report_as_the_primary_entry_point():
    claims = build_claims()
    text = CARD.read_text()
    assert claims["pages_url"] in text
    assert "primary entry point" in text


# -- the notebook ------------------------------------------------------------


def test_the_notebook_keeps_section_9_2_scope():
    source = NOTEBOOK.read_text()
    widgets = re.findall(r"mo\.ui\.(\w+)\(", source)
    assert sorted(widgets) == ["radio", "slider"], widgets
    tree = ast.parse(source)
    imported = {
        (node.module or "").split(".")[0] if isinstance(node, ast.ImportFrom) else alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in (node.names if isinstance(node, ast.Import) else [None])
    }
    imported.discard("")
    for forbidden in ("shap", "mlflow", "matplotlib", "sklearn", "requests"):
        assert forbidden not in imported, f"the WASM notebook must not import {forbidden}"
    for retired in ("precomputed_grid", "nearest_neighbour", "ood_"):
        assert retired not in source


def test_the_notebook_executes_the_verified_module_and_renders_the_labels():
    source = NOTEBOOK.read_text()
    assert 'read_text("browser_champion.py")' in source, "the page must run the verified bytes"
    assert "replay_label" in source and "sensitivity_probe_label" in source
    assert "holdout_coverage_" in source, "the level selector must annotate empirical coverage"
    # The identity check and the network table both run in front of the reader.
    assert "bitwise identical" in source
    assert "getEntriesByType" in source


def test_the_notebook_retypes_no_published_number():
    """Every figure a visitor reads comes from claims.json; the only literals left
    are layout constants and the scenario slider's range."""
    source = NOTEBOOK.read_text()
    for figure in ("25.9078", "0.4407", "0.7593", "0.9398", "-19.4926", "2026-04-07", "57e3ad40"):
        assert figure not in source, f"{figure} is retyped in the notebook instead of read from claims"


# -- item 4: the measurement is internally consistent ------------------------


def test_the_network_record_adds_up():
    record = json.loads(NETWORK.read_text())
    hosts = record["hosts"]
    assert sum(h["requests"] for h in hosts.values()) == record["totals"]["requests"]
    assert sum(h["bytes"] for h in hosts.values()) == record["totals"]["bytes"]
    assert record["totals"]["bytes"] > 1_000_000, "a WASM page with a Python runtime is not tiny"
    # Browser-opaque sizes must be labelled as out-of-band, never passed off as measured 0.
    for name, host in hosts.items():
        if host.get("browser_reported_size") == 0:
            assert "out-of-band" in host["source"], name
            assert host["bytes"] > 0, name


def test_the_published_cold_load_figure_is_the_recorded_one():
    claims = build_claims()
    record = json.loads(NETWORK.read_text())
    assert claims["wasm_cold_load_bytes"] == f"{record['totals']['bytes'] / 1_000_000:.2f} million bytes"
    # The exact record is self-referential to one byte; the published precision must absorb it.
    low, high = record["totals"]["bytes"] - 1, record["totals"]["bytes"] + 1
    assert f"{low / 1_000_000:.2f}" == f"{high / 1_000_000:.2f}", "published precision no longer absorbs ±1 byte"
    assert "self_reference" in record
    assert claims["wasm_cold_load_mb"] == str(round(record["totals"]["bytes"] / 1_000_000))
    assert claims["wasm_cold_load_requests"] == str(record["totals"]["requests"])


def test_the_equivalence_record_matches_the_gate_test():
    record = json.loads(EQUIVALENCE.read_text())
    assert record["gate"]["bitwise_identical"] is True
    assert record["gate"]["max_abs_deviation"] == 0.0
    assert record["gate"]["tolerance"] == 0.0
    assert record["fixture"]["delivery_days"] >= 30
    assert all(c["broke_the_gate"] for c in record["positive_controls"].values())
    availability = record["delivery_day_availability"]
    assert availability["masked_max_abs_difference"] == 0.0
    assert availability["masked_output_bitwise_identical"] is True
    assert availability["d_minus_1_control_max_abs_difference"] > 1.0


# -- the build refuses to publish what it should not -------------------------


def test_the_bundle_manifest_is_clean_and_complete():
    manifest = json.loads(BUNDLE_MANIFEST.read_text())
    assert manifest["sdk"] == "static"
    assert manifest["problems"] == []
    assert len(manifest["boosters"]) == 9
    assert manifest["asset_files"] > 100, "html-wasm ships marimo's frontend locally"
    import hashlib

    assert manifest["browser_champion_sha256"] == hashlib.sha256(
        (REPO_ROOT / "app" / "browser_champion.py").read_bytes()
    ).hexdigest()


def test_the_payload_and_bundle_carry_no_compiled_bytecode():
    """A .pyc is neither source nor reproducible; it must never reach the Space."""
    payload = json.loads((REPO_ROOT / "reports" / "cp3b" / "payload.json").read_text())
    assert not any(name.endswith(".pyc") for name in payload["file_bytes"])
    manifest = json.loads(BUNDLE_MANIFEST.read_text())
    assert "compiled bytecode present in the bundle" not in manifest["problems"]


def test_the_export_allowlist_cannot_admit_a_governance_file():
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from build_wasm_space import ALLOWED_ROOT

    for internal in ("CLAUDE.md", "AGENTS.md", "engineering-role.md", "progress.md", ".env"):
        assert internal not in ALLOWED_ROOT
    assert {"index.html", "assets", "public", "README.md"} <= ALLOWED_ROOT


def test_the_browser_run_record_carries_the_in_browser_evidence():
    """Items 1-3 require properties to hold *in the browser*; this pins what was observed there."""
    record = json.loads((REPO_ROOT / "reports" / "cp3b" / "browser_run.json").read_text())
    raw = record["item_2_raw_heads_cross_build"]
    assert raw["heads_bitwise_identical"] == 9 and raw["max_abs_deviation"] == 0.0
    page = record["item_2_full_pipeline_in_page"]
    assert page["max_abs_deviation"] == 0.0 and page["delivery_days"] >= 30
    avail = record["item_3_delivery_day_availability_in_pyodide"]
    assert avail["masked_max_abs_difference"] == 0.0 and avail["masked_output_bitwise_identical"]
    assert avail["d_minus_1_control_max_abs_difference"] > 1.0
    host = json.loads(EQUIVALENCE.read_text())["delivery_day_availability"]
    assert avail["d_minus_1_control_max_abs_difference"] == host["d_minus_1_control_max_abs_difference"], (
        "the browser and host controls disagree — the paths are not the same computation"
    )
    assert record["static_page_non_regression"]["network_requests"] == 1
    assert record["static_page_non_regression"]["resource_timing_entries"] == 0
