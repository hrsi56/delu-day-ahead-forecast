#!/usr/bin/env python3
"""Pre-review check runner (automation plan item 7): the publication runbook §9 offline checks, in order, recorded once.

    uv run python scripts/prerelease.py [--stage pre-final|final]      (or: make prerelease)

It runs in the current checkout, with no worktree, and refuses to start unless the working tree is clean. In order:

1. `uv run pytest -q` on the project's Python 3.13 environment, after the CI steps that precede CI's own pytest run
   (the browser payload build), as CI orders them;
2. every `run:` step of `.github/workflows/tests.yml`, under Python 3.12, in its own environment under
   `.local/artifacts/prerelease/`, so the developer venv is never re-synced. A step CI runs only on `main` is left
   to step 7;
3. `make verify`;
4. `make lint-publication`;
5. rebuild determinism: `scripts/rebuild_presentation.py`, then an empty `git status --porcelain`;
6. `scripts/check_links.py`;
7. `scripts/publication_guard.py tree`. Before the `--final` build it is expected to fail, and is recorded that way;
   `--stage final` expects it to pass.

It continues past failures and exits 1 on any unexpected result. The committed record,
`reports/presentation/release-checks/<date>-prerelease.json`, keeps only each check's argv, expected and actual exit
codes, duration and pass/fail counts. Raw output goes only to `.local/artifacts/prerelease/<date>/`.

**Credentials (AGENTS.md § Credentials).** Before anything is written, every output line holding the value of a local
credential (`scripts/secret_guard.py::credentials`) is dropped. The run then fails closed and names the variable,
never the value. The standard's §10 browser checks stay out: they are `scripts/check_reader_paths.py`'s.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import secret_guard  # noqa: E402

RECORDS = ROOT / "reports" / "presentation" / "release-checks"
RAW = ROOT / ".local" / "artifacts" / "prerelease"
WORKFLOW = ROOT / ".github" / "workflows" / "tests.yml"
COUNTS = re.compile(r"(\d+) (passed|failed|skipped|errors?|xfailed|xpassed)\b")
#: Which interpreter and environment uv uses. A check sets them itself; it never inherits them from whatever ran
#: this script, or a 3.13 check could run in the 3.12 environment.
UV_SELECTION = ("UV_PYTHON", "UV_PROJECT_ENVIRONMENT")


def ci_steps(workflow: Path = WORKFLOW) -> tuple[list[tuple[str, list[str]]], list[str]]:
    """CI's `run:` steps as (name, argv), and the names of the conditional steps left out. `uses:` steps (checkout,
    setup-uv) have no local equivalent; the Python 3.12 pin they carry is applied to every step instead."""
    steps = yaml.safe_load(workflow.read_text())["jobs"]["properties"]["steps"]
    runs, conditional = [], []
    for step in steps:
        if "run" not in step:
            continue
        name = step.get("name") or step["run"]
        if "if" in step:
            conditional.append(name)
            continue
        runs.append((name, shlex.split(step["run"])))
    return runs, conditional


def plan(stage: str, py312_env: Path, workflow: Path = WORKFLOW) -> list[dict]:
    """The checks in the runbook's order: name, argv, the exit codes that count as expected, and environment."""
    py312 = {"UV_PROJECT_ENVIRONMENT": str(py312_env), "UV_PYTHON": "3.12"}
    py313 = {"UV_PYTHON": "3.13"}
    runs, _ = ci_steps(workflow)
    first_pytest = next(i for i, (_, argv) in enumerate(runs) if argv[:3] == ["uv", "run", "pytest"])
    prerequisites = [(name, argv) for name, argv in runs[:first_pytest] if argv[:2] != ["uv", "sync"]]
    checks = [{"name": f"Python 3.13, before pytest: {name}", "argv": argv, "expect": [0], "env": py313}
              for name, argv in prerequisites]
    checks += [{"name": "pytest, Python 3.13", "argv": ["uv", "run", "pytest", "-q"], "expect": [0], "env": py313}]
    checks += [{"name": f"CI, Python 3.12: {name}", "argv": argv, "expect": [0], "env": py312} for name, argv in runs]
    checks += [
        {"name": "make verify", "argv": ["make", "verify"], "expect": [0]},
        {"name": "make lint-publication", "argv": ["make", "lint-publication"], "expect": [0]},
        {"name": "rebuild the presentation", "argv": ["uv", "run", "python", "scripts/rebuild_presentation.py"],
         "expect": [0]},
        {"name": "the tree is unchanged after the rebuild", "argv": ["git", "status", "--porcelain"], "expect": [0],
         "empty_output": True},
        {"name": "links", "argv": ["uv", "run", "python", "scripts/check_links.py"], "expect": [0]},
        {"name": "publication guard (tree)", "argv": ["python3", "scripts/publication_guard.py", "tree"],
         "expect": [0] if stage == "final" else [1]},
    ]
    return checks


def redact(text: str, secrets: list[tuple[str, bytes]]) -> tuple[str, list[str]]:
    """Drop every line holding a credential value; return the rest and the names of the variables found."""
    kept, found = [], set()
    for line in text.splitlines():
        hits = {name for name, value in secrets if value.decode(errors="ignore") in line}
        if hits:
            found |= hits
            continue
        kept.append(line)
    return "\n".join(kept) + ("\n" if kept else ""), sorted(found)


def counts(output: str) -> dict[str, int]:
    """Pytest's summary counts, from its last summary line; empty for checks that are not pytest."""
    lines = [line for line in output.splitlines() if COUNTS.search(line) and (" in " in line or "=" in line)]
    if not lines:
        return {}
    return {kind.rstrip("s") if kind.startswith("error") else kind: int(n) for n, kind in COUNTS.findall(lines[-1])}


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")[:60]


def run_check(check: dict, number: int, raw_dir: Path, secrets, *, runner=subprocess.run) -> dict:
    env = {key: value for key, value in os.environ.items() if key not in UV_SELECTION} | check.get("env", {})
    started = time.monotonic()
    done = runner(check["argv"], cwd=ROOT, env=env, capture_output=True, text=True)
    seconds = round(time.monotonic() - started, 1)
    output, found = redact((done.stdout or "") + (done.stderr or ""), secrets)
    raw_dir.mkdir(parents=True, exist_ok=True)
    (raw_dir / f"{number:02d}-{_slug(check['name'])}.log").write_text(output)
    expected = done.returncode in check["expect"] and not (check.get("empty_output") and done.stdout.strip())
    result = {"name": check["name"], "argv": check["argv"], "expected_exit": check["expect"],
              "exit": done.returncode, "seconds": seconds, "counts": counts(output),
              "result": "as expected" if expected and not found else "UNEXPECTED"}
    if check.get("env"):
        result["python"] = check["env"].get("UV_PYTHON")
    if check.get("empty_output"):
        result["changed_paths"] = len(done.stdout.splitlines())
    if found:
        result["credential_values_found"] = [f"the value of {name}; its lines were dropped" for name in found]
    return result


def clean_tree() -> list[str]:
    return subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True,
                          check=True).stdout.splitlines()


def prerelease(stage: str, date: str, out_dir: Path, raw_root: Path, *, only: list[str] | None = None,
               runner=subprocess.run, secrets=None, workflow: Path = WORKFLOW) -> tuple[dict, int]:
    secrets = secret_guard.credentials() if secrets is None else secrets
    raw_dir = raw_root / date
    checks = plan(stage, raw_root / "py312-env", workflow)
    if only:
        checks = [c for c in checks if any(word.lower() in c["name"].lower() for word in only)]
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    results = [run_check(check, n, raw_dir, secrets, runner=runner) for n, check in enumerate(checks, 1)]
    unexpected = [r["name"] for r in results if r["result"] != "as expected"]
    body = {"schema": "prerelease-v1", "status": "PASS" if not unexpected else "FAIL", "stage": stage,
            "head": head, "started_utc": started,
            "completed_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "partial": bool(only), "conditional_ci_steps_left_to_the_guard_check": ci_steps(workflow)[1],
            "raw_output": f"{raw_dir.relative_to(ROOT).as_posix() if raw_dir.is_relative_to(ROOT) else raw_dir} "
                          "(local only, never committed)",
            "checks": results, "unexpected": unexpected}
    text = json.dumps(body, indent=2, sort_keys=True) + "\n"
    if any(value.decode(errors="ignore") in text for _, value in secrets):
        raise SystemExit("a credential value reached the record; nothing was written")
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{date}-prerelease.json").write_text(text)
    return body, 0 if not unexpected else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--stage", choices=("pre-final", "final"), default="pre-final",
                        help="before or after the --final build; it sets the publication guard's expected result")
    parser.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    parser.add_argument("--out-dir", type=Path, default=RECORDS)
    parser.add_argument("--only", nargs="+", help="run only the checks whose names contain one of these words "
                        "(the record is marked partial)")
    args = parser.parse_args(argv)
    dirty = clean_tree()
    if dirty:
        print("refused: the working tree is not clean:\n  " + "\n  ".join(dirty[:20]))
        return 2
    body, code = prerelease(args.stage, args.date, args.out_dir, RAW, only=args.only)
    for result in body["checks"]:
        print(f"{result['result']:>12}  exit {result['exit']} (expected {result['expected_exit']})  "
              f"{result['seconds']:>7}s  {result['name']}  {result['counts'] or ''}")
    print(f"\n{body['status']}: wrote {args.out_dir / (args.date + '-prerelease.json')}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
