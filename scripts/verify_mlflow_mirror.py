#!/usr/bin/env python3
"""Check that an MLflow server mirrors the committed export, run by run (plan §10.9–§10.10).

Reads are **anonymous** and go over plain REST with the standard library: no MLflow client, no
credential, no cookie. That is how a reader sees the public server, and it keeps the verifier
from ever sending a token.

    uv run python scripts/verify_mlflow_mirror.py verify --target local
    uv run python scripts/verify_mlflow_mirror.py verify --target public --out reports/presentation/...
    uv run python scripts/verify_mlflow_mirror.py probe --out reports/presentation/mlflow-capabilities.json
    uv run python scripts/verify_mlflow_mirror.py rehearse     # loopback server only

`verify` checks that every `run_key` exists exactly once, the parent links, every parameter and
tag, every metric history point by (key, step, timestamp, value), every artifact's SHA-256 and the
upload-completion tags. `probe` is the read-only capability check against DagsHub (§10.9 item 1).
`rehearse` drives the local 3.5.1 rehearsal (§10.9 item 2): an interrupted upload that resumes
without duplicates, a clean verification, then two deliberate faults -- a deleted history point
and an altered artifact -- which the verifier must catch. It refuses any non-loopback server.

DagsHub quirk, measured 2026-09-24: `metrics/get-history` returns an empty first page unless
`max_results` is given. Every history read here passes it and follows page tokens.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from delu_forecast.claims import MLFLOW_URL  # noqa: E402

EXPORT_DIR = ROOT / "reports" / "presentation" / "mlflow-export"
EXPERIMENT = "delu-generations"
LOCAL_URI = "http://127.0.0.1:5051"
TARGETS = {"local": LOCAL_URI, "public": MLFLOW_URL}
HISTORY_PAGE = 25000
USER_AGENT = "delu-mirror-verifier/1.0 (anonymous, read-only)"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --------------------------------------------------------------------------- anonymous REST


class Reader:
    """Anonymous, read-only REST access to one tracking server."""

    def __init__(self, base: str) -> None:
        self.base = base.rstrip("/")

    def _request(self, method: str, path: str, payload: dict | None = None, raw: bool = False):
        url = f"{self.base}/{path}"
        data = json.dumps(payload).encode() if payload is not None else None
        request = urllib.request.Request(url, data=data, method=method, headers={
            "User-Agent": USER_AGENT, **({"Content-Type": "application/json"} if data else {})})
        with urllib.request.urlopen(request, timeout=60) as response:
            body = response.read()
        return body if raw else json.loads(body or b"{}")

    def get(self, path: str, **query):
        return self._request("GET", f"{path}?{urllib.parse.urlencode(query)}" if query else path)

    def post(self, path: str, payload: dict):
        # A search is a read: it is POST only because its filter is a JSON body.
        return self._request("POST", path, payload)

    def version(self) -> str:
        return self._request("GET", "version", raw=True).decode().strip()

    def experiment(self, name: str) -> dict | None:
        try:
            return self.get("api/2.0/mlflow/experiments/get-by-name", experiment_name=name)["experiment"]
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            raise

    def runs(self, experiment_id: str) -> list[dict]:
        runs, token = [], None
        while True:
            payload = {"experiment_ids": [experiment_id], "max_results": 1000, "run_view_type": "ACTIVE_ONLY"}
            if token:
                payload["page_token"] = token
            page = self.post("api/2.0/mlflow/runs/search", payload)
            runs += page.get("runs", [])
            token = page.get("next_page_token")
            if not token or not page.get("runs"):
                return runs

    def history(self, run_id: str, key: str) -> list[dict]:
        points, token = [], None
        while True:
            query = {"run_id": run_id, "metric_key": key, "max_results": HISTORY_PAGE}
            if token:
                query["page_token"] = token
            page = self.get("api/2.0/mlflow/metrics/get-history", **query)
            batch = page.get("metrics", [])
            points += batch
            token = page.get("next_page_token")
            if not token or not batch:
                return points

    def artifact(self, run_id: str, path: str) -> bytes:
        return self._request("GET", f"get-artifact?{urllib.parse.urlencode({'path': path, 'run_uuid': run_id})}",
                             raw=True)

    def get_run(self, run_id: str) -> dict:
        return self.get("api/2.0/mlflow/runs/get", run_id=run_id)["run"]


# --------------------------------------------------------------------------- the export


def load_export() -> tuple[dict, dict[str, dict]]:
    manifest = json.loads((EXPORT_DIR / "manifest.json").read_text())
    runs = {}
    for name in ("cp10", "cp15", "cp16", "cp20"):
        for run in json.loads((EXPORT_DIR / f"{name}.json").read_text())["runs"]:
            runs[run["run_key"]] = run
    return manifest, runs


def _tags(run: dict) -> dict[str, str]:
    return {tag["key"]: tag["value"] for tag in run["data"].get("tags", [])}


def _params(run: dict) -> dict[str, str]:
    return {param["key"]: param["value"] for param in run["data"].get("params", [])}


def _points(points) -> list[tuple[int, int, float]]:
    return sorted((int(p["step"]), int(p["timestamp"]), float(p["value"])) for p in points)


# --------------------------------------------------------------------------- verify


def verify(base: str, *, check_upload_tags: bool = True) -> dict:
    """Compare the server with the committed export. Returns a report; `passed` is the verdict."""
    reader = Reader(base)
    manifest, expected = load_export()
    report: dict = {"target": base, "checked_at_utc": utc_now(), "experiment": EXPERIMENT, "problems": [],
                    "runs": {}}
    problems = report["problems"]
    experiment = reader.experiment(EXPERIMENT)
    if experiment is None:
        problems.append(f"experiment {EXPERIMENT} does not exist")
        report["passed"] = False
        return report
    report["experiment_id"] = experiment["experiment_id"]
    experiment_tags = {tag["key"]: tag["value"] for tag in experiment.get("tags", [])}
    for key, value in manifest.get("experiment_tags", {}).items():
        if experiment_tags.get(key) != value:
            problems.append(f"experiment tag {key} differs")
    found: dict[str, list[dict]] = {}
    for run in reader.runs(experiment["experiment_id"]):
        key = _tags(run).get("delu.run_key")
        found.setdefault(key, []).append(run)
    unknown = sorted(str(key) for key in found if key not in expected)
    if unknown:
        problems.append(f"runs with unexpected run keys: {unknown}")
    run_ids: dict[str, str] = {}
    for run_key, run in expected.items():
        matches = found.get(run_key, [])
        if len(matches) != 1:
            problems.append(f"{run_key}: {len(matches)} runs carry this key (exactly one required)")
            continue
        run_ids[run_key] = matches[0]["info"]["run_id"]
    for run_key, run in expected.items():
        if run_key not in run_ids:
            continue
        run_id = run_ids[run_key]
        server = reader.get_run(run_id)
        tags, params = _tags(server), _params(server)
        entry = {"run_id": run_id, "metrics_checked": 0, "points_checked": 0, "artifacts_checked": 0}
        if server["info"].get("run_name") != run["run_name"]:
            problems.append(f"{run_key}: run name {server['info'].get('run_name')!r}")
        parent = run["parent"]
        if parent is not None and tags.get("mlflow.parentRunId") != run_ids.get(parent):
            problems.append(f"{run_key}: parent link is not {parent}")
        for key, value in run["params"].items():
            if params.get(key) != value:
                problems.append(f"{run_key}: param {key} differs")
        extra_params = set(params) - set(run["params"])
        if extra_params:
            problems.append(f"{run_key}: unexpected params {sorted(extra_params)}")
        for key, value in run["tags"].items():
            if tags.get(key) != value:
                problems.append(f"{run_key}: tag {key} differs")
        if check_upload_tags:
            if tags.get("delu.upload_state") != "complete":
                problems.append(f"{run_key}: delu.upload_state is {tags.get('delu.upload_state')!r}")
            if parent is None and tags.get("delu.package_complete") != "true":
                problems.append(f"{run_key}: delu.package_complete is not true")
            if not tags.get("delu.backfill_tool_sha"):
                problems.append(f"{run_key}: delu.backfill_tool_sha is missing")
        for key, points in run["metrics"].items():
            actual = _points(reader.history(run_id, key))
            wanted = _points(points)
            entry["metrics_checked"] += 1
            entry["points_checked"] += len(actual)
            if actual != wanted:
                missing = len(set(wanted) - set(actual))
                extra = len(set(actual) - set(wanted))
                problems.append(f"{run_key}: metric {key} history differs ({missing} missing, {extra} extra points)")
        server_keys = {metric["key"] for metric in server["data"].get("metrics", [])}
        if server_keys - set(run["metrics"]):
            problems.append(f"{run_key}: unexpected metrics {sorted(server_keys - set(run['metrics']))}")
        for artifact in run["artifacts"]:
            try:
                data = reader.artifact(run_id, artifact["path"])
            except urllib.error.HTTPError as exc:
                problems.append(f"{run_key}: artifact {artifact['path']} unreadable ({exc.code})")
                continue
            entry["artifacts_checked"] += 1
            if hashlib.sha256(data).hexdigest() != artifact["sha256"]:
                problems.append(f"{run_key}: artifact {artifact['path']} digest differs")
        inputs = server.get("inputs", {}).get("dataset_inputs", [])
        entry["datasets_on_server"] = sorted(item["dataset"]["name"] for item in inputs)
        report["runs"][run_key] = entry
    report["counts"] = {"expected": len(expected), "found": len(run_ids),
                        "metric_points": sum(e["points_checked"] for e in report["runs"].values())}
    report["passed"] = not problems
    return report


# --------------------------------------------------------------------------- probe (§10.9 item 1)


def probe(base: str) -> dict:
    """Read-only capability probe. It never writes, and it sends no credential."""
    reader = Reader(base)
    record: dict = {"target": base, "probed_at_utc": utc_now(), "client": USER_AGENT, "checks": {}}
    checks = record["checks"]

    def attempt(name, action):
        try:
            checks[name] = {"ok": True, "result": action()}
        except urllib.error.HTTPError as exc:
            checks[name] = {"ok": False, "status": exc.code}
        except Exception as exc:  # recorded, not raised: the probe reports what failed
            checks[name] = {"ok": False, "error": f"{type(exc).__name__}: {str(exc)[:200]}"}

    attempt("version", reader.version)
    attempt("experiment delu-cp2 (anonymous)", lambda: {k: reader.experiment("delu-cp2")[k]
                                                         for k in ("experiment_id", "name")})
    attempt("experiment delu-generations exists", lambda: reader.experiment(EXPERIMENT) is not None)

    def search_fields():
        page = reader.post("api/2.0/mlflow/runs/search", {"experiment_ids": ["0"], "max_results": 1})
        run = page["runs"][0]
        return {"run": sorted(run), "info": sorted(run["info"]), "data": sorted(run["data"]),
                "inputs_field_present": "inputs" in run}

    attempt("runs/search fields (delu-cp2)", search_fields)
    v1 = "83e475627b6646c885c70f9010c8cf2e"
    attempt("runs/get anonymous", lambda: reader.get_run(v1)["info"]["run_name"])

    def history_quirk():
        without = reader.get("api/2.0/mlflow/metrics/get-history", run_id=v1, metric_key="holdout_mae")
        with_max = reader.get("api/2.0/mlflow/metrics/get-history", run_id=v1, metric_key="holdout_mae",
                              max_results=100)
        return {"without_max_results_points": len(without.get("metrics", [])),
                "with_max_results_points": len(with_max.get("metrics", []))}

    attempt("metric history (get-history)", history_quirk)
    attempt("metric history bulk interval (UI charts)", lambda: len(reader.get(
        "ajax-api/2.0/mlflow/metrics/get-history-bulk-interval", run_ids=v1, metric_key="holdout_mae",
        max_results=100).get("metrics", [])))
    attempt("artifact download anonymous", lambda: len(reader.artifact(v1, "champion_card.json")))
    attempt("registered model anonymous", lambda: reader.get(
        "api/2.0/mlflow/registered-models/get", name="delu-day-ahead-champion")["registered_model"]["name"])

    def ui_route():
        request = urllib.request.Request(f"{reader.base}/", headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=60) as response:
            return {"status": response.status, "content_type": response.headers.get("Content-Type")}

    attempt("UI root anonymous", ui_route)
    return record


# --------------------------------------------------------------------------- rehearse (§10.9 item 2)


def _publish(*extra: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "mlflow_publish.py"), "--target", "local", *extra],
        cwd=ROOT, capture_output=True, text=True, env={**__import__("os").environ, "MLFLOW_DISABLE_AGENT_HINT": "1"},
    )


def rehearse(store: Path, artifacts: Path, out: Path) -> int:
    reader = Reader(LOCAL_URI)
    if not LOCAL_URI.startswith(("http://127.0.0.1", "http://localhost")):
        raise SystemExit("rehearse runs against a loopback server only")
    record: dict = {"server": LOCAL_URI, "server_version": reader.version(), "started_utc": utc_now(), "steps": []}
    if reader.experiment(EXPERIMENT) is not None:
        raise SystemExit(f"{EXPERIMENT} already exists on the rehearsal server; start from an empty store")

    def step(name, **fields):
        record["steps"].append({"step": name, **fields})
        print(f"[rehearse] {name}: {fields}")

    interrupted = _publish("--fail-after", "115")
    step("interrupted upload", exit_code=interrupted.returncode,
         tail=interrupted.stderr.strip().splitlines()[-1:] if interrupted.stderr else [])
    partial = verify(LOCAL_URI)
    step("verification after the interruption (expected to fail)", passed=partial["passed"],
         problems=len(partial["problems"]))
    resumed = _publish()
    step("resumed upload", exit_code=resumed.returncode, tail=resumed.stdout.strip().splitlines()[-3:])
    clean = verify(LOCAL_URI)
    step("verification after resume", passed=clean["passed"], problems=clean["problems"][:5],
         counts=clean.get("counts"))
    rerun = _publish()
    after_rerun = verify(LOCAL_URI)
    step("idempotent re-run", exit_code=rerun.returncode, passed=after_rerun["passed"],
         runs_found=after_rerun.get("counts", {}).get("found"))

    # Fault 1: delete one history point straight from the store.
    run_id = clean["runs"]["cp20/HG"]["run_id"]
    with sqlite3.connect(store) as db:
        deleted = db.execute(
            "DELETE FROM metrics WHERE run_uuid=? AND key='fold_mae_eur' AND step=3", (run_id,)).rowcount
    # Fault 2: alter one artifact's bytes on disk.
    target = next(path for path in artifacts.rglob("summary.json") if run_id in str(path))
    original = target.read_bytes()
    target.write_bytes(original.replace(b'"HG"', b'"HX"', 1))
    faulted = verify(LOCAL_URI)
    caught_history = any("cp20/HG: metric fold_mae_eur" in problem for problem in faulted["problems"])
    caught_digest = any("cp20/HG: artifact summary.json digest differs" in problem for problem in faulted["problems"])
    step("deliberate faults", deleted_points=deleted, altered_artifact=str(target.relative_to(artifacts)),
         verification_passed=faulted["passed"], caught_deleted_point=caught_history,
         caught_altered_digest=caught_digest, problems=faulted["problems"])
    target.write_bytes(original)
    record["passed"] = bool(
        interrupted.returncode != 0 and not partial["passed"] and resumed.returncode == 0 and clean["passed"]
        and after_rerun["passed"] and rerun.returncode == 0 and caught_history and caught_digest
    )
    record["finished_utc"] = utc_now()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(f"[rehearse] passed={record['passed']} -> {out}")
    return 0 if record["passed"] else 1


# --------------------------------------------------------------------------- main


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    v = sub.add_parser("verify")
    v.add_argument("--target", choices=sorted(TARGETS), required=True)
    v.add_argument("--tracking-uri", default=None)
    v.add_argument("--out", type=Path, default=None)
    p = sub.add_parser("probe")
    p.add_argument("--tracking-uri", default=MLFLOW_URL)
    p.add_argument("--out", type=Path, required=True)
    r = sub.add_parser("rehearse")
    r.add_argument("--store", type=Path, required=True, help="the rehearsal server's SQLite store")
    r.add_argument("--artifacts", type=Path, default=None)
    r.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "verify":
        report = verify(args.tracking_uri or TARGETS[args.target])
        text = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(text)
        for problem in report["problems"][:40]:
            print(f"MISMATCH {problem}")
        print(f"passed={report['passed']} counts={report.get('counts')}")
        return 0 if report["passed"] else 1
    if args.command == "probe":
        record = probe(args.tracking_uri)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        print(json.dumps(record["checks"], indent=1)[:3000])
        return 0
    artifacts = args.artifacts or args.store.parent / "artifacts"
    return rehearse(args.store, artifacts, args.out)


if __name__ == "__main__":
    raise SystemExit(main())
