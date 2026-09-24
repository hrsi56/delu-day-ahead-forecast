"""Presentation plan §9.5 and §10: the committed MLflow export is deterministic and exact.

It lists exactly 23 runs (4 parents, 19 children), every metric name carries its unit, the
comparability IDs group the runs the plan says are comparable, every value is a committed record,
and the outbound scan blocks a credential value without printing it.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import subprocess
import sys

import pytest

from delu_forecast import research as R
from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import mlflow_export as E  # noqa: E402

EXPORT = REPO_ROOT / "reports" / "presentation" / "mlflow-export"

EXPECTED_RUN_KEYS = {
    "cp10", "cp10/v1_reference", "cp10/c1_head_spread", "cp10/c1_price_volatility",
    "cp10/c2_aci_gamma_0.000001", "cp10/c2_aci_gamma_0.000005", "cp10/c2_aci_gamma_0.00001",
    "cp10/c2_aci_gamma_0.00002",
    "cp15", "cp15/B0", "cp15/B1", "cp15/B2", "cp15/B3", "cp15/A1", "cp15/A2", "cp15/A3", "cp15/A4", "cp15/A5",
    "cp16", "cp16/V2-P", "cp16/V2-H",
    "cp20", "cp20/HG",
}


@pytest.fixture(scope="module")
def built():
    return E.build_export()


@pytest.fixture(scope="module")
def runs(built):
    return {run["run_key"]: run for name in ("cp10", "cp15", "cp16", "cp20") for run in built[name]["runs"]}


def test_the_export_is_deterministic_and_committed(built):
    again = E.render(E.build_export())
    assert again == E.render(built), "two builds differ"
    for name, text in again.items():
        assert (EXPORT / name).read_text() == text, f"{name} is stale; run scripts/mlflow_export.py"


def test_the_manifest_lists_exactly_23_runs(built):
    manifest = built["manifest"]
    assert manifest["counts"] == {"parents": 4, "children": 19, "total": 23}
    assert {run["run_key"] for run in manifest["runs"]} == EXPECTED_RUN_KEYS
    for run in manifest["runs"]:
        if "/" in run["run_key"]:
            assert run["parent"] == run["run_key"].split("/")[0]
        else:
            assert run["parent"] is None


def test_each_policy_appears_once(runs):
    codes = [run["tags"]["delu.policy_code"] for run in runs.values() if run["parent"]]
    assert len(codes) == len(set(codes)) == 19
    assert runs["cp15/B1"]["tags"]["delu.v1_record_run"] == "83e475627b6646c885c70f9010c8cf2e"
    assert runs["cp20/HG"]["run_name"] == "CP-20 · HG · v3"
    assert runs["cp16/V2-H"]["run_name"] == "CP-16 · V2-H · v2"
    assert runs["cp15/B1"]["run_name"] == "CP-15 · B1 · v1 development replay"


UNIT_SUFFIX = re.compile(r"(_eur(_vs_\w+)?|coverage(50|80|95)|hits95|^s_(mae|wis)|^delta_s_(mae|wis)_vs_\w+)")


def test_every_metric_name_carries_its_unit(runs):
    for run in runs.values():
        for key in run["metrics"]:
            unit = E.metric_unit(key)
            assert run["metric_units"][key] == unit
            assert UNIT_SUFFIX.search(key), f"{run['run_key']}: {key} does not say its unit"
            if unit.startswith("EUR/MWh"):
                assert "_eur" in key, key


def test_fold_histories_step_over_the_five_folds(runs):
    for run in runs.values():
        for key, points in run["metrics"].items():
            if key.startswith(("fold_", "delta_fold_")):
                assert [p["step"] for p in points] == [1, 2, 3, 4, 5], (run["run_key"], key)
                assert [p["timestamp"] for p in points] == sorted(p["timestamp"] for p in points)


def test_every_metric_value_is_a_committed_record(runs):
    for run in runs.values():
        for key, sources in run["metric_provenance"].items():
            if key == "daily_mae_eur":
                continue
            for point, source in zip(run["metrics"][key], sources):
                record_id, which = source.split("#")
                record = R.get(record_id)
                raw = {"value": record.raw, "ci_low": record.ci_low_raw, "ci_high": record.ci_high_raw}[which]
                assert point["value"] == float(raw), (run["run_key"], key, source)


def test_comparability_ids_group_the_right_runs(runs):
    common = {run["tags"]["delu.comparability_id"] for key, run in runs.items() if not key.startswith("cp10")}
    cp10 = {run["tags"]["delu.comparability_id"] for key, run in runs.items() if key.startswith("cp10")}
    assert len(common) == 1 and len(cp10) == 1 and common != cp10
    assert all(not key.startswith("s_") for key in runs["cp10/c1_price_volatility"]["metrics"]), (
        "CP-10 is not normalized to B0 and must carry no s_ score"
    )


def test_provenance_tags_are_separate(runs):
    hg = runs["cp20/HG"]["tags"]
    assert hg["delu.model_code_sha"] == "3e9ff8b500c2c655fea810ae11886503927f176c"
    assert hg["delu.evidence_ref"] == "evidence/cp-20@a7a9b2e"
    assert "delu.backfill_tool_sha" not in hg, "the tool SHA is written at upload time, never as model code"
    assert hg["delu.backfilled"] == "true" and hg["delu.original_completed_utc"] == "unknown"
    blobs = json.loads(hg["delu.source_blobs"])
    assert blobs and all(R.SOURCES[path].blob == blob for path, blob in blobs.items())
    assert "gfs-weather-features" in json.loads(hg["delu.datasets"])


def test_artifact_digests_match_their_content(runs):
    import hashlib

    for run in runs.values():
        for artifact in run["artifacts"]:
            assert hashlib.sha256(artifact["content"].encode()).hexdigest() == artifact["sha256"]


# -- the outbound scan ----------------------------------------------------------------


def test_the_outbound_scan_covers_names_params_tags_metrics_and_artifacts(built):
    places = {where.split(" ", 1)[1].split(" ")[0] for where, _ in E.outbound_strings(built)}
    assert {"run", "param", "tag", "metric", "dataset", "artifact"} <= places


def test_negative_control_a_fake_credential_is_caught_and_never_printed(built):
    token = secrets.token_hex(20)
    doctored = json.loads(json.dumps({k: v for k, v in built.items() if k != "manifest"}))
    doctored["cp20"]["runs"][1]["tags"]["delu.evidence_ref"] += f" {token}"
    findings = E.outbound_findings(E.outbound_strings(doctored), [("FAKE_TOKEN", token.encode())])
    assert findings and all(token not in finding for finding in findings)
    assert any("cp20/HG tag delu.evidence_ref" in finding for finding in findings)


def test_negative_control_the_export_command_refuses_and_hides_the_value(built):
    """End to end: a credential whose value occurs in the export blocks the command."""
    value = built["cp20"]["runs"][1]["tags"]["delu.comparability_id"]
    env = {k: v for k, v in os.environ.items()
           if not re.search(r"TOKEN|SECRET|PASSWORD|PASSWD|API_?KEY|ACCESS_KEY|PRIVATE_KEY|MLFLOW", k, re.I)}
    env.update(SECRET_GUARD_ENV_ONLY="1", PRES1_FIXTURE_TOKEN=value, MLFLOW_DISABLE_AGENT_HINT="1")
    result = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "mlflow_export.py"), "--check"],
                            cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=300)
    output = result.stdout + result.stderr
    assert result.returncode == 1
    assert "PRES1_FIXTURE_TOKEN" in output
    assert value not in output
