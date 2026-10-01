#!/usr/bin/env python3
"""Publish the committed MLflow export to a tracking server (presentation plan §10.7–§10.8).

    uv run python scripts/mlflow_publish.py --dry-run
    uv run python scripts/mlflow_publish.py --target local          # the 3.5.1 rehearsal server
    uv run python scripts/mlflow_publish.py --target public \\
        --owner-instruction "<the Owner's words naming this upload>"   # Phase F1 only

Rules it enforces, in order:

1. **Only committed export files.** The working tree must equal `HEAD`, and the committed export
   must equal a fresh build from the evidence layer.
2. **Nothing credential-shaped leaves.** Every outbound string -- names, params, tags, notes,
   metric keys, dataset fields -- and every artifact byte is compared with the local credential
   values from `scripts/secret_guard.py` before the first request. A hit aborts without printing
   the value, and any exception text is redacted before it is shown.
3. **Idempotent by `delu.run_key`.** For each run it first searches by that tag: a complete run is
   skipped; an incomplete one is resumed, logging only the missing params, tags, history points,
   datasets and artifacts; otherwise the run is created. Two runs with one key abort the upload.
4. **Complete only after verification.** A run gets `delu.upload_state=complete` only after its
   history and artifacts read back equal to the export; a parent gets
   `delu.package_complete=true` only after all its children are complete and verified.
5. **A public upload needs the Owner's instruction for that action**, which is recorded in the
   upload log (§13). The credentials are read from the environment by the MLflow client; this
   script only reports whether they are set.

`--fail-after N` stops after N write operations, to rehearse an interrupted upload.

`--authorized-runs KEY,...` bounds an upload to the runs an instruction names (PRES-3: CP-21's five). Before the
first write it reads the service and refuses unless every write the upload would make belongs to those runs: the
experiment must exist with its tags already equal to the export's, and every other run must already be complete.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import mlflow_export as E  # noqa: E402
from delu_forecast import registry as G  # noqa: E402
import verify_mlflow_mirror as V  # noqa: E402

os.environ.setdefault("MLFLOW_DISABLE_AGENT_HINT", "1")

BATCH = 900  # MLflow accepts at most 1,000 metrics per log_batch call


class Interrupted(RuntimeError):
    """The rehearsal's deliberate interruption."""


class Refused(RuntimeError):
    """A precondition the publisher will not proceed without."""


class Writes:
    """Counts write operations so a rehearsal can stop part-way."""

    def __init__(self, fail_after: int | None) -> None:
        self.count, self.fail_after = 0, fail_after

    def tick(self, n: int = 1) -> None:
        self.count += n
        if self.fail_after is not None and self.count >= self.fail_after:
            raise Interrupted(f"deliberate interruption after {self.count} write operations")


def redact(text: str, secrets: list[tuple[str, bytes]]) -> str:
    for name, value in secrets:
        text = text.replace(value.decode("utf-8", "replace"), f"<{name} redacted>")
    return text


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=True).stdout


def preconditions(*, strict: bool) -> tuple[dict, dict[str, dict], str]:
    """The committed, current export, and the commit it is published from."""
    dirty = _git("status", "--porcelain=v1").strip()
    tracked = _git("ls-files", "--", "reports/presentation/mlflow-export").split()
    if strict and dirty:
        raise Refused("the working tree differs from HEAD; commit or discard first")
    files = E.build_export()
    fresh = E.render(files)
    untracked = sorted(set(f"reports/presentation/mlflow-export/{name}" for name in fresh) - set(tracked))
    if untracked:
        raise Refused(f"the export must be committed; git does not track {untracked}")
    stale = [name for name, text in fresh.items() if (E.EXPORT_DIR / name).read_text() != text]
    if stale:
        raise Refused(f"the committed export is stale: {stale}")
    # A contract, never a count (standard §11): the export holds exactly the runs the registry expects.
    problems = E.contract_problems(files)
    if problems:
        raise Refused("the export does not match the registry: " + "; ".join(problems))
    manifest, runs = V.load_export()
    return manifest, runs, _git("rev-parse", "HEAD").strip()


def scan(runs: dict[str, dict], secrets) -> None:
    files = {"export": {"runs": list(runs.values())}}
    items = list(E.outbound_strings(files))
    items += [(f"experiment tag {key}", f"{key}={value}") for key, value in E.EXPERIMENT_TAGS.items()]
    findings = E.outbound_findings(items, secrets)
    if findings:
        raise Refused("; ".join(dict.fromkeys(findings)))


# --------------------------------------------------------------------------- authenticated read-only gate


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None  # Never forward the Authorization header to another URL.


def public_precheck() -> dict:
    """Read the actual MLflow service with its configured Basic credentials (brief §9).

    DagsHub MLflow permits a token as username. The general /api/v1/user API does not
    accept that same Basic pair; using it here rejected valid MLflow credentials.
    A read success establishes service access, not untested write permissions.
    Neither account response data nor exception text is returned or logged.
    """
    names = ("MLFLOW_TRACKING_USERNAME", "MLFLOW_TRACKING_PASSWORD")
    state = {name: ("set" if os.environ.get(name) else "unset") for name in names}
    url = V.TARGETS["public"] + "/api/2.0/mlflow/experiments/get?experiment_id=0"
    record = {"checked_at_utc": V.utc_now(), "credential_state": state,
              "request": {"method": "GET", "url": url, "authentication": "Basic from existing MLflow variables",
                          "redirects_allowed": False}, "passed": False, "network_writes": 0}
    if "unset" in state.values():
        record["error"] = "required MLflow variable unset"
        return record
    pair = f"{os.environ.get(names[0])}:{os.environ.get(names[1])}".encode()
    authorization = "Basic " + base64.b64encode(pair).decode()
    request = urllib.request.Request(url, method="GET", headers={
        "Authorization": authorization, "User-Agent": "delu-mlflow-precheck/1.0 (read-only)"})
    del pair, authorization
    try:
        with urllib.request.build_opener(NoRedirect).open(request, timeout=30) as response:
            record["http_status"] = response.status
            body = json.loads(response.read())
        experiment = body.get("experiment", {})
        record["expected_experiment_matched"] = (experiment.get("experiment_id") == "0"
                                                 and experiment.get("name") == "delu-cp2")
        record["passed"] = record["http_status"] == 200 and record["expected_experiment_matched"]
    except urllib.error.HTTPError as exc:
        record["http_status"] = exc.code
    except Exception as exc:
        record["error"] = type(exc).__name__  # No exception message or response body can leak.
    return record


# --------------------------------------------------------------------------- the upload


def _client(uri: str):
    from mlflow.tracking import MlflowClient

    return MlflowClient(tracking_uri=uri)


def _find(client, experiment_id: str, run_key: str):
    runs = client.search_runs([experiment_id], filter_string=f"tags.`delu.run_key` = '{run_key}'",
                              max_results=10)
    if len(runs) > 1:
        raise Refused(f"{run_key}: {len(runs)} runs carry this key; resolve the duplicate by hand")
    return runs[0] if runs else None


def _artifact_paths(client, run_id: str, folder: str | None = None) -> set[str]:
    """Every artifact path already on a run, folders included (the chart artifacts sit in charts/)."""
    paths = set()
    for item in client.list_artifacts(run_id, folder):
        if item.is_dir:
            paths |= _artifact_paths(client, run_id, item.path)
        else:
            paths.add(item.path)
    return paths


def _log_run(client, reader: V.Reader, experiment_id: str, run: dict, parent_id: str | None,
             tool_sha: str, writes: Writes, log: list) -> str:
    from mlflow.entities import Dataset, DatasetInput, InputTag, Metric, Param, RunTag

    run_key = run["run_key"]
    existing = _find(client, experiment_id, run_key)
    if existing is not None and existing.data.tags.get("delu.upload_state") == "complete":
        log.append({"run_key": run_key, "action": "skipped (complete)", "run_id": existing.info.run_id})
        return existing.info.run_id
    tags = {**run["tags"], "delu.backfill_tool_sha": tool_sha}
    if parent_id:
        tags["mlflow.parentRunId"] = parent_id
    if existing is None:
        created = client.create_run(experiment_id, run_name=run["run_name"],
                                    tags={**tags, "delu.upload_state": "incomplete"})
        writes.tick()
        run_id, action = created.info.run_id, "created"
        present_params, present_tags = {}, {}
    else:
        run_id, action = existing.info.run_id, "resumed"
        present_params, present_tags = dict(existing.data.params), dict(existing.data.tags)
    for key, value in run["params"].items():
        if key in present_params and present_params[key] != value:
            raise Refused(f"{run_key}: param {key} already holds a different value")
    missing_params = [Param(k, v) for k, v in run["params"].items() if k not in present_params]
    missing_tags = [RunTag(k, v) for k, v in tags.items() if present_tags.get(k) != v]
    if missing_params or missing_tags:
        client.log_batch(run_id, params=missing_params, tags=missing_tags)
        writes.tick()
    logged_points = 0
    for key, points in run["metrics"].items():
        have = set(V._points(reader.history(run_id, key))) if action == "resumed" else set()
        wanted = [p for p in points if (int(p["step"]), int(p["timestamp"]), float(p["value"])) not in have]
        for start in range(0, len(wanted), BATCH):
            chunk = wanted[start:start + BATCH]
            client.log_batch(run_id, metrics=[Metric(key, float(p["value"]), int(p["timestamp"]), int(p["step"]))
                                              for p in chunk])
            writes.tick()
            logged_points += len(chunk)
    present_inputs = set()
    if action == "resumed":
        present_inputs = {item["dataset"]["name"] for item in
                          reader.get_run(run_id).get("inputs", {}).get("dataset_inputs", [])}
    dataset_status = "none"
    wanted_inputs = [d for d in run["inputs"] if d["name"] not in present_inputs]
    if wanted_inputs:
        try:
            client.log_inputs(run_id, datasets=[
                DatasetInput(
                    dataset=Dataset(name=d["name"], digest=d["digest"], source_type="local",
                                    source=json.dumps({"uri": d["source"], "sha256": d["sha256"]}),
                                    profile=json.dumps({"description": d["profile"]})),
                    tags=[InputTag("mlflow.data.context", d["context"])],
                ) for d in wanted_inputs])
            writes.tick()
            dataset_status = "logged"
        except Exception as exc:  # recorded as a capability gap; digests remain in the tags
            dataset_status = f"unsupported: {type(exc).__name__}"
    present_artifacts = _artifact_paths(client, run_id) if action == "resumed" else set()
    with tempfile.TemporaryDirectory() as scratch:
        for artifact in run["artifacts"]:
            if artifact["path"] in present_artifacts:
                continue
            local = Path(scratch) / artifact["path"]
            local.parent.mkdir(parents=True, exist_ok=True)
            local.write_text(artifact["content"])
            folder = str(Path(artifact["path"]).parent)
            client.log_artifact(run_id, str(local), artifact_path=None if folder == "." else folder)
            writes.tick()
    # Read back before marking complete.
    for key, points in run["metrics"].items():
        if V._points(reader.history(run_id, key)) != V._points(points):
            raise Refused(f"{run_key}: metric {key} did not read back equal; left incomplete")
    for artifact in run["artifacts"]:
        if hashlib.sha256(reader.artifact(run_id, artifact["path"])).hexdigest() != artifact["sha256"]:
            raise Refused(f"{run_key}: artifact {artifact['path']} did not read back equal; left incomplete")
    if run["parent"] is not None:
        client.set_tag(run_id, "delu.upload_state", "complete")
        writes.tick()
        client.set_terminated(run_id, "FINISHED")
    log.append({"run_key": run_key, "action": action, "run_id": run_id, "points_logged": logged_points,
                "datasets": dataset_status})
    return run_id


def write_plan(client, runs: dict[str, dict], authorized: tuple[str, ...]) -> dict:
    """Read-only: what an upload would write, and whether all of it lies inside the authorized runs. Nothing outside
    them may be written -- no experiment, no experiment tag, no other run -- so anything else refuses the upload."""
    unknown = sorted(set(authorized) - set(runs))
    if unknown:
        raise Refused(f"authorized runs not in the export: {unknown}")
    experiment = client.get_experiment_by_name(E.EXPERIMENT)
    plan: dict = {"authorized": sorted(authorized), "experiment_exists": experiment is not None,
                  "experiment_tags_to_write": [], "runs": {}}
    if experiment is None:
        raise Refused(f"the experiment {E.EXPERIMENT} does not exist; creating it is outside the authorized runs")
    present = dict(experiment.tags)
    plan["experiment_tags_to_write"] = sorted(key for key, value in E.EXPERIMENT_TAGS.items() if present.get(key) != value)
    outside = [f"experiment tag {key}" for key in plan["experiment_tags_to_write"]]
    for key in runs:
        found = _find(client, experiment.experiment_id, key)
        state = "absent" if found is None else found.data.tags.get("delu.upload_state", "incomplete")
        plan["runs"][key] = state
        if key not in authorized and state != "complete":
            outside.append(f"run {key} ({state})")
        elif key not in authorized and "/" not in key and found.data.tags.get("delu.package_complete") != "true":
            outside.append(f"run {key} (its package is not marked complete)")
    if outside:
        raise Refused("the upload would write outside the authorized runs: " + "; ".join(outside) + "; nothing was written")
    plan["to_write"] = sorted(key for key in authorized if plan["runs"][key] != "complete")
    return plan


def publish(uri: str, runs: dict[str, dict], tool_sha: str, writes: Writes,
            authorized: tuple[str, ...] | None = None) -> list[dict]:
    client = _client(uri)
    reader = V.Reader(uri)
    plan = write_plan(client, runs, authorized) if authorized is not None else None
    experiment = client.get_experiment_by_name(E.EXPERIMENT)
    experiment_id = experiment.experiment_id if experiment else client.create_experiment(E.EXPERIMENT)
    if experiment is None:
        writes.tick()
    present = dict(experiment.tags) if experiment else {}
    for key, value in E.EXPERIMENT_TAGS.items():
        if present.get(key) != value:
            client.set_experiment_tag(experiment_id, key, value)
            writes.tick()
    log: list[dict] = [{"write_plan": plan}] if plan is not None else []
    for checkpoint in G.parent_run_keys():
        parent = runs[checkpoint]
        parent_id = _log_run(client, reader, experiment_id, parent, None, tool_sha, writes, log)
        children = [run for run in runs.values() if run["parent"] == checkpoint]
        for child in children:
            _log_run(client, reader, experiment_id, child, parent_id, tool_sha, writes, log)
        # The package is complete only when every child is complete and reads back equal.
        tags = client.get_run(parent_id).data.tags
        if tags.get("delu.package_complete") != "true":
            for child in children:
                found = _find(client, experiment_id, child["run_key"])
                if found is None or found.data.tags.get("delu.upload_state") != "complete":
                    raise Refused(f"{checkpoint}: child {child['run_key']} is not complete")
            client.set_tag(parent_id, "delu.package_complete", "true")
            client.set_tag(parent_id, "delu.upload_state", "complete")
            writes.tick(2)
            client.set_terminated(parent_id, "FINISHED")
    return log


# --------------------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--precheck", action="store_true", help="authenticated read-only MLflow gate; no upload")
    mode.add_argument("--target", choices=("local", "public"))
    parser.add_argument("--tracking-uri", default=None)
    parser.add_argument("--fail-after", type=int, default=None)
    parser.add_argument("--owner-instruction", default=None,
                        help="public only: the Owner's instruction naming this upload, recorded verbatim")
    parser.add_argument("--log", type=Path, default=None)
    parser.add_argument("--authorized-runs", default=None,
                        help="comma-separated run keys: refuse before any write unless every write lies inside them")
    args = parser.parse_args()
    authorized = tuple(key.strip() for key in args.authorized_runs.split(",")) if args.authorized_runs else None
    secrets = E.local_secrets()
    try:
        if args.precheck:
            record = public_precheck()
            if args.log:
                args.log.parent.mkdir(parents=True, exist_ok=True)
                args.log.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
            print(json.dumps(record, sort_keys=True))
            return 0 if record["passed"] else 2
        manifest, runs, head = preconditions(strict=not args.dry_run)
        scan(runs, secrets)
        if args.dry_run:
            points = sum(len(p) for run in runs.values() for p in run["metrics"].values())
            print(f"dry run: {manifest['counts']['total']} runs, {points} metric points, "
                  f"{sum(len(run['artifacts']) for run in runs.values())} artifacts; outbound scan clean; "
                  f"export current at {head[:12]}")
            return 0
        uri = args.tracking_uri or V.TARGETS[args.target]
        if args.target == "public":
            if not args.owner_instruction:
                raise Refused("a public upload needs --owner-instruction with the Owner's words for this action")
            if uri != V.TARGETS["public"]:
                raise Refused("public target must be the configured DagsHub MLflow service")
            precheck = public_precheck()
            print(json.dumps(precheck, sort_keys=True))
            if not precheck["passed"]:
                raise Refused("authenticated read-only MLflow precheck failed; no upload attempted")
        elif not uri.startswith(("http://127.0.0.1", "http://localhost")):
            raise Refused("--target local must point at a loopback server")
        started = V.utc_now()
        writes = Writes(args.fail_after)
        log = publish(uri, runs, head, writes, authorized)
        record = {"target": args.target, "tracking_uri": uri, "experiment": E.EXPERIMENT,
                  "export_commit": head, "started_utc": started, "finished_utc": V.utc_now(),
                  "write_operations": writes.count, "runs": log,
                  "owner_instruction": args.owner_instruction}
        if args.log:
            args.log.parent.mkdir(parents=True, exist_ok=True)
            args.log.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        entries = [entry for entry in log if "action" in entry]
        created = sum(1 for entry in entries if entry["action"] == "created")
        resumed = sum(1 for entry in entries if entry["action"] == "resumed")
        print(f"published {len(entries)} runs to {uri}: {created} created, {resumed} resumed, "
              f"{len(entries) - created - resumed} already complete; {writes.count} write operations")
        return 0
    except Interrupted as exc:
        print(f"mlflow-publish: {exc}", file=sys.stderr)
        return 3
    except Refused as exc:
        print(f"mlflow-publish: REFUSED - {redact(str(exc), secrets)}", file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"mlflow-publish: FAILED - {type(exc).__name__}: {redact(str(exc), secrets)[:600]}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
