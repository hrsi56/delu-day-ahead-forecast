#!/usr/bin/env python3
"""Build and exercise the release container, and record what actually happened.

CP-3 item 1 requires the bundled champion, the CLI, the container and the marimo
app to run locally from a clean setup. This runs that check rather than
describing it, and writes `reports/cp3/container_check.json` so a reviewer can
compare their own run against ours instead of taking a paragraph on trust.

The decisive step is `docker run --network none`: §9.2 says the champion loads
from the image with no live call during a user session, and a container with no
network at all either serves the app and the CLI or it does not.

Requires a Docker daemon. Without one it writes an honest "not attempted" record
and exits 0, because the artifact is the Dockerfile and the missing thing is the
reviewer's runtime, not the release.

    uv run python scripts/verify_container.py [--image delu-showcase:verify]
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "reports" / "cp3" / "container_check.json"
PORT = 7860

PROBE = """
import json, socket, urllib.request
out = {}
try:
    socket.create_connection(("1.1.1.1", 443), timeout=4)
    out["outbound_network"] = "reachable"
except OSError as exc:
    out["outbound_network"] = f"unreachable ({type(exc).__name__})"
for name, url in (
    ("cdn.jsdelivr.net", "https://cdn.jsdelivr.net/"),
    ("huggingface.co", "https://huggingface.co/"),
    ("dagshub.com", "https://dagshub.com/"),
):
    try:
        urllib.request.urlopen(url, timeout=4)
        out[name] = "reachable"
    except Exception as exc:
        out[name] = f"unreachable ({type(exc).__name__})"
response = urllib.request.urlopen("http://127.0.0.1:%d/health", timeout=8)
out["app_health_status"] = response.status
out["app_health_body"] = response.read().decode()[:64]
out["app_index_bytes"] = len(urllib.request.urlopen("http://127.0.0.1:%d/", timeout=15).read())
print(json.dumps(out))
""" % (PORT, PORT)


def run(command: list[str], **kwargs) -> subprocess.CompletedProcess:
    return subprocess.run(command, capture_output=True, text=True, **kwargs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default="delu-showcase:verify")
    parser.add_argument("--context", default=str(ROOT))
    parser.add_argument("--keep", action="store_true", help="leave the container running")
    parser.add_argument(
        "--out",
        type=Path,
        default=RECORD,
        help="where to write the record. A reviewer re-running this in a clean worktree should "
        "point it somewhere outside the tree, so the check does not dirty what it is checking.",
    )
    args = parser.parse_args()

    record: dict[str, object] = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "image": args.image,
        "build_context": Path(args.context).name,
        "steps": {},
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)

    def finish(ok: bool) -> int:
        record["passed"] = ok
        args.out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        print(f"\nwrote {args.out}")
        return 0 if ok else 1

    if shutil.which("docker") is None:
        record["steps"]["docker_available"] = {"ok": False, "detail": "no docker on PATH"}
        record["note"] = (
            "No container runtime here, so the container was not exercised. The Dockerfile is the "
            "artifact; run `make container` on a machine with a daemon to reproduce."
        )
        return finish(False)

    version = run(["docker", "version", "--format", "{{.Server.Version}}"])
    if version.returncode != 0:
        record["steps"]["docker_daemon"] = {"ok": False, "detail": version.stderr.strip()[:300]}
        record["note"] = "Docker CLI present but no daemon responded."
        return finish(False)
    record["docker_server_version"] = version.stdout.strip()
    info = run(["docker", "info", "--format", "{{.OperatingSystem}} / {{.Architecture}} / {{.NCPU}} CPU"])
    record["docker_host"] = info.stdout.strip()

    print(f"building {args.image} from {args.context} ...")
    build = run(["docker", "build", "-t", args.image, args.context])
    record["steps"]["build"] = {"ok": build.returncode == 0, "detail": build.stderr.strip()[-400:] or "built"}
    if build.returncode != 0:
        return finish(False)

    size = run(["docker", "images", args.image, "--format", "{{.Size}}"])
    record["image_size"] = size.stdout.strip()

    container = "delu-showcase-verify"
    run(["docker", "rm", "-f", container])
    print("starting the container with --network none ...")
    start = run(["docker", "run", "-d", "--name", container, "--network", "none", args.image])
    record["steps"]["run_offline"] = {
        "ok": start.returncode == 0,
        "detail": start.stdout.strip()[:12] or start.stderr.strip()[:300],
    }
    if start.returncode != 0:
        return finish(False)

    try:
        probe: dict | None = None
        for _ in range(24):
            time.sleep(5)
            attempt = run(["docker", "exec", "-i", container, "python", "-"], input=PROBE)
            if attempt.returncode == 0 and attempt.stdout.strip():
                probe = json.loads(attempt.stdout.strip().splitlines()[-1])
                break
        record["steps"]["offline_probe"] = {
            "ok": bool(probe) and probe.get("app_health_status") == 200,
            "detail": probe or "the app never answered /health inside an isolated container",
        }

        print("running the CLI inside the isolated container ...")
        cli = run(
            ["docker", "exec", container, "python", "predict_next_day.py", "--level", "80", "--self-check"]
        )
        passed = "passed: True" in cli.stdout
        record["steps"]["cli_offline"] = {
            "ok": cli.returncode == 0 and passed,
            "detail": {
                "exit_code": cli.returncode,
                "delivery_day_prices_change_nothing": "delivery_day_prices_change_nothing: True" in cli.stdout,
                "positive_control_d_minus_1_changes_output": (
                    "positive_control_d_minus_1_changes_output: True" in cli.stdout
                ),
                "tail": cli.stdout.strip().splitlines()[-1] if cli.stdout.strip() else cli.stderr[-200:],
            },
        }

        logs = run(["docker", "logs", container])
        record["steps"]["marimo_server_mode"] = {
            "ok": "Running showcase.py" in logs.stdout + logs.stderr,
            "detail": (logs.stdout + logs.stderr).strip().splitlines()[-1][:160] if (logs.stdout + logs.stderr).strip() else "",
        }
    finally:
        if not args.keep:
            run(["docker", "rm", "-f", container])

    ok = all(step["ok"] for step in record["steps"].values())
    for name, step in record["steps"].items():
        print(f"  [{'ok' if step['ok'] else 'FAIL'}] {name}")
    return finish(ok)


if __name__ == "__main__":
    raise SystemExit(main())
