"""Presentation plan §9.5 and §10, standard §5 and §11: the committed MLflow export is deterministic and exact.

The export matches the registry -- a contract, never a run count (standard §11, brief W14): exactly
the run keys the registry expects, each policy once per population, each name, parent and public
name the registry's. Every metric name carries its unit, the comparability IDs group the runs the
plan says are comparable, every value is a committed record, and the outbound scan blocks a
credential value without printing it.
"""

from __future__ import annotations

import json
import os
import re
import secrets
import subprocess
import sys

import pytest

from delu_forecast import registry as G
from delu_forecast import research as R
from delu_forecast.claims import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))

import mlflow_export as E  # noqa: E402

EXPORT = REPO_ROOT / "reports" / "presentation" / "mlflow-export"

@pytest.fixture(scope="module")
def built():
    return E.build_export()


@pytest.fixture(scope="module")
def runs(built):
    return {run["run_key"]: run for name in G.parent_run_keys() for run in built[name]["runs"]}


def test_the_export_is_deterministic_and_committed(built):
    again = E.render(E.build_export())
    assert again == E.render(built), "two builds differ"
    for name, text in again.items():
        assert (EXPORT / name).read_text() == text, f"{name} is stale; run scripts/mlflow_export.py"


def test_the_export_matches_the_registry(built):
    """The contract that replaced "exactly 23 runs" (standard §11, brief W14)."""
    assert E.contract_problems(built) == []
    manifest = built["manifest"]
    assert sorted(run["run_key"] for run in manifest["runs"]) == sorted(G.expected_run_keys())
    for run in manifest["runs"]:
        if "/" in run["run_key"]:
            assert run["parent"] == run["run_key"].split("/")[0]
        else:
            assert run["parent"] is None
        assert run["run_name"] == G.mlflow_run_name(run["run_key"])


def test_negative_control_an_unregistered_or_missing_run_breaks_the_contract(built):
    extra = json.loads(json.dumps(built))
    stray = json.loads(json.dumps(extra["cp20"]["runs"][-1]))
    stray["run_key"] = "cp20/HX"
    extra["cp20"]["runs"].append(stray)
    assert any("unregistered ['cp20/HX']" in problem for problem in E.contract_problems(extra))
    missing = json.loads(json.dumps(built))
    missing["cp16"]["runs"] = missing["cp16"]["runs"][:-1]
    assert any("missing ['cp16/V2-H']" in problem for problem in E.contract_problems(missing))
    renamed = json.loads(json.dumps(built))
    renamed["cp20"]["runs"][-1]["run_name"] = "CP-20 · HG · v3"
    assert any("run name is not the registry's" in problem for problem in E.contract_problems(renamed))


def test_each_policy_appears_once_per_population(runs):
    """One identity, one run per comparability group: v2 is logged once although CP-20 calls it H0."""
    seen: dict[tuple[str, str], str] = {}
    for key, run in runs.items():
        if run["parent"] is None:
            continue
        identity = (run["tags"]["delu.registry_id"], run["tags"]["delu.population_id"])
        assert identity not in seen, f"{key} repeats {seen.get(identity)}"
        seen[identity] = key
        assert run["tags"]["delu.public_name"] == G.entry_for_run_key(key).name
    assert runs["cp15/B1"]["tags"]["delu.v1_record_run"] == "83e475627b6646c885c70f9010c8cf2e"
    assert G.by_code("H0") is G.by_code("V2-H")


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


def test_candidate_runs_carry_the_pages_own_charts(runs):
    """Plan §10.6: the site's SVG charts on the candidate runs they show, identical to the page."""
    import build_pages as B

    with_charts = {key for key, run in runs.items() if any(a["path"].startswith("charts/") for a in run["artifacts"])}
    assert with_charts == {"cp20/HG", "cp16/V2-H"}
    page = (REPO_ROOT / "docs" / "index.html").read_text()
    for run_key, charts in B.CHARTS_BY_RUN.items():
        artifacts = {a["path"]: a["content"] for a in runs[run_key]["artifacts"]}
        for chart_id, _ in charts:
            svg = artifacts[f"charts/{chart_id}.svg"]
            assert svg.startswith('<?xml version="1.0"') and 'xmlns="http://www.w3.org/2000/svg"' in svg
            drawing = re.sub(r'^<svg width="[\d.]+" height="[\d.]+" ', "<svg ", svg.split("\n", 1)[1].rstrip("\n"))
            assert drawing in page, f"{chart_id}: the artifact is not the page's drawing"
            assert f"charts/{chart_id}.svg" in artifacts["README.md"]


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
    # the chart files are scanned byte for byte too
    doctored["cp20"]["runs"][1]["artifacts"][-1]["content"] += f"<!-- {token} -->"
    findings = E.outbound_findings(E.outbound_strings(doctored), [("FAKE_TOKEN", token.encode())])
    assert any("artifact charts/" in finding for finding in findings)


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


# Auth gate must exercise MLflow's endpoint, not the unrelated account API.
def test_public_precheck_uses_existing_basic_pair_without_exposing_it(monkeypatch):
    import base64
    import io
    import mlflow_publish as P

    username, password = "test-mlflow-user", "test-mlflow-password"
    monkeypatch.setenv("MLFLOW_TRACKING_USERNAME", username)
    monkeypatch.setenv("MLFLOW_TRACKING_PASSWORD", password)

    class Response(io.BytesIO):
        status = 200

    class Opener:
        def open(self, request, timeout):
            assert request.full_url == P.V.TARGETS["public"] + "/api/2.0/mlflow/experiments/get?experiment_id=0"
            assert request.get_method() == "GET"
            assert request.get_header("Authorization") == "Basic " + base64.b64encode(f"{username}:{password}".encode()).decode()
            return Response(b'{"experiment":{"experiment_id":"0","name":"delu-cp2"},"private":"not logged"}')

    monkeypatch.setattr(P.urllib.request, "build_opener", lambda handler: Opener())
    result = P.public_precheck()
    assert result["passed"] and result["http_status"] == 200 and result["network_writes"] == 0
    assert all(value not in json.dumps(result) for value in (username, password, "not logged"))
    assert P.NoRedirect().redirect_request(None, None, None, None, None, None) is None


@pytest.mark.parametrize("mode", ["unset", "http403", "exception", "wrong-experiment"])
def test_precheck_failures_are_closed_and_never_emit_exception_or_body(monkeypatch, mode):
    import io
    import urllib.error
    import mlflow_publish as P

    monkeypatch.setenv("MLFLOW_TRACKING_USERNAME", "synthetic-user")
    monkeypatch.setenv("MLFLOW_TRACKING_PASSWORD", "synthetic-secret")
    if mode == "unset":
        monkeypatch.delenv("MLFLOW_TRACKING_PASSWORD")

    class Response(io.BytesIO):
        status = 200

    class Opener:
        def open(self, request, timeout):
            assert mode != "unset", "unset credentials must never cause a request"
            if mode == "http403":
                raise urllib.error.HTTPError(request.full_url, 403, "synthetic-secret", {}, None)
            if mode == "exception":
                raise RuntimeError("synthetic-secret")
            return Response(b'{"experiment":{"experiment_id":"0","name":"unexpected"}}')

    monkeypatch.setattr(P.urllib.request, "build_opener", lambda handler: Opener())
    result = P.public_precheck()
    assert not result["passed"]
    assert "synthetic-secret" not in json.dumps(result)
