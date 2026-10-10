#!/usr/bin/env python3
"""Post-deploy publication receipt (automation plan item 6): what every public surface actually serves.

    uv run python scripts/publication_receipt.py --landing <sha> --bundle <dir> --expect <bundle sha256>

Read-only, anonymous and credential-free. It writes nothing outside its records. For each surface it
compares the intended identity with the observed one:

- **GitHub:** `origin`'s `main` (`git ls-remote`) is the landing commit.
- **Pages:** the bytes Pages serves hash to `docs/index.html` at the landing commit.
- **Space files:** the Space is a public Static Space, and its file tree at its current revision is the reviewed
  bundle, file by file. It reuses `scripts/deploy_space.py`'s anonymous Hub reads and per-file check, after the
  bundle itself is checked against `--expect`. An unchanged Space is verified the same way: it must still serve
  the bundle it was last deployed with.
- **Space page:** the served direct-app page is the bundle's `index.html` once Hugging Face's injected
  `window.huggingface` creator-metadata script, and only that, is removed. Both hashes are recorded.
- **MLflow:** the public mirror holds the committed export (`scripts/verify_mlflow_mirror.py::verify`).
- **Links:** every destination on the public surfaces answers 200 (`scripts/check_links.py::main`).

**Each surface is checked independently.** A failed attempt is retried after `--wait` seconds, up to `--retries`
times. Every attempt, the first failure included, stays in the record (publication runbook §1). The records go to
`reports/presentation/release-checks/`:

- `<date>-publication-receipt.json`;
- the link checker's and mirror verifier's own records, `<date>-postdeploy-links.json` and
  `<date>-postdeploy-mlflow-mirror.json`.

It prints the packet template's §8 rows, and exits 1 unless every surface passes. The browser checks stay in
`scripts/check_reader_paths.py`; the packet cites their records.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "src"))

import deploy_space  # noqa: E402
from delu_forecast.claims import build_claims  # noqa: E402

RECORDS = ROOT / "reports" / "presentation" / "release-checks"
#: Hugging Face injects exactly this into every served Static Space page (observed 2026-09-29 and 2026-10-11).
HF_INJECTION = re.compile(rb"<script>window\.huggingface=\{[^<]*?\};</script>")
AGENT = "delu-publication-receipt (anonymous, read-only)"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str) -> bytes:
    """An anonymous GET that follows redirects, as a visitor's browser would. No cookie and no token."""
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 - fixed public https URLs
        return response.read()


def remote_main() -> str:
    out = subprocess.run(["git", "ls-remote", "origin", "refs/heads/main"], cwd=ROOT, capture_output=True,
                         text=True, check=True).stdout.split()
    return out[0] if out else ""


def landing_page(landing: str) -> bytes:
    return subprocess.run(["git", "show", f"{landing}:docs/index.html"], cwd=ROOT, capture_output=True,
                          check=True).stdout


def resolve(commit: str) -> str:
    return subprocess.run(["git", "rev-parse", "--verify", f"{commit}^{{commit}}"], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()


def normalize_space_page(body: bytes) -> tuple[bytes, int]:
    """The served page without Hugging Face's creator-metadata script, and how many such scripts there were."""
    found = len(HF_INJECTION.findall(body))
    return HF_INJECTION.sub(b"", body), found


def check_github(landing: str, *, remote=remote_main) -> dict:
    observed = remote()
    return {"intended": landing, "observed": observed, "passed": observed == landing}


def check_pages(landing: str, url: str, *, page=landing_page, get=fetch) -> dict:
    expected, served = _sha256(page(landing)), get(url)
    return {"intended": expected, "observed": _sha256(served), "url": url, "bytes": len(served),
            "passed": _sha256(served) == expected}


def check_space_files(bundle: Path, expected: str, *, hub) -> dict:
    """The Space serves the reviewed bundle: same file set, every file's Hub hash equal to the bundle's."""
    bound = deploy_space.check_bundle(bundle, expected)  # raises SystemExit when the bundle is not the reviewed one
    identity = hub.identity()
    public_static = identity.get("sdk") == "static" and identity.get("private") is False
    served = deploy_space.verify(deploy_space.local_files(bundle), hub.tree(identity["revision"]))
    return {"intended": bound["bundle_sha256"], "observed": identity.get("revision"), "identity": identity,
            "files": bound["files"], **served, "passed": public_static and served["verified"]}


def check_space_page(bundle: Path, url: str, *, get=fetch) -> dict:
    expected = _sha256((bundle / "index.html").read_bytes())
    served = get(url)
    normalized, injected = normalize_space_page(served)
    return {"intended": expected, "observed": _sha256(normalized), "url": url, "sha256": _sha256(served),
            "normalized_sha256": _sha256(normalized), "exact_bytes_match": _sha256(served) == expected,
            "hosting_injection": "Hugging Face window.huggingface public creator metadata script",
            "injected_script_count": injected,
            "passed": injected <= 1 and _sha256(normalized) == expected}


def check_mlflow(record: Path, *, verify=None) -> dict:
    if verify is None:
        from verify_mlflow_mirror import TARGETS, verify as mirror_verify

        verify = lambda: mirror_verify(TARGETS["public"])  # noqa: E731
    report = verify()
    record.parent.mkdir(parents=True, exist_ok=True)
    record.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    counts = report.get("counts") or {}
    return {"intended": f"{counts.get('expected')} runs of the committed export",
            "observed": f"{counts.get('found')} runs found", "record": _rel(record),
            "problems": report.get("problems", [])[:20], "passed": bool(report.get("passed"))}


def check_links(record: Path, *, links=None) -> dict:
    if links is None:
        from check_links import main as links

    code = links([], record=record)
    failed = json.loads(record.read_text()).get("failed_destinations", {}) if record.is_file() else {}
    return {"intended": "every destination answers 200", "observed": f"{len(failed)} failed destinations",
            "record": _rel(record), "failed": failed, "passed": code == 0}


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def attempt(check, *, retries: int, wait: float, sleep=time.sleep) -> dict:
    """Run one surface's check until it passes or the retries run out. Every attempt is kept, failures included;
    an exception is recorded by its type and message, which for these anonymous reads carry no credential."""
    attempts: list[dict] = []
    for number in range(retries + 1):
        if number:
            sleep(wait)
        started = _utc()
        try:
            result = check()
        except (Exception, SystemExit) as exc:  # noqa: BLE001 - a surface's failure must not stop the others
            result = {"passed": False, "error": f"{type(exc).__name__}: {exc}"}
        attempts.append({"attempt": number + 1, "checked_at_utc": started, **result})
        if result["passed"]:
            break
    final = attempts[-1]
    first_failure = next((a for a in attempts if not a["passed"]), None)
    return {"passed": final["passed"], "intended": final.get("intended"), "observed": final.get("observed"),
            "checked_at_utc": final["checked_at_utc"], "first_failure": first_failure, "attempts": attempts}


def rows(surfaces: dict[str, dict], record: str) -> list[str]:
    """The packet template's §8 rows: intended identity, observed identity with its UTC time, record and result,
    and the outstanding action."""
    out = ["| Surface | Intended identity | Observed identity, UTC | Record and result | Outstanding action |",
           "|---|---|---|---|---|"]
    for name, result in surfaces.items():
        verdict = "PASS" if result["passed"] else "FAIL"
        retries = len(result["attempts"]) - 1
        if retries:
            verdict += f" after {retries} retr{'y' if retries == 1 else 'ies'}"
        last = result["attempts"][-1]
        action = "none" if result["passed"] else f"recheck {name}: {last.get('error') or last.get('observed')}"
        out.append(f"| {name} | `{result['intended']}` | `{result['observed']}`, {result['checked_at_utc']} | "
                   f"`{record}`: {verdict} | {action} |")
    return out


def receipt(landing: str, bundle: Path, expected: str, out_dir: Path, date: str, *, retries: int = 2,
            wait: float = 30.0, checks: dict | None = None, sleep=time.sleep) -> tuple[dict, int]:
    """Check every surface independently, write the record, and return it with the exit code."""
    claims = build_claims()
    out_dir.mkdir(parents=True, exist_ok=True)
    record_path = out_dir / f"{date}-publication-receipt.json"
    checks = checks or {
        "GitHub main": lambda: check_github(landing),
        "GitHub Pages": lambda: check_pages(landing, claims["pages_url"]),
        "Hugging Face Space files": lambda: check_space_files(bundle, expected, hub=deploy_space.Hub()),
        "Hugging Face direct demo page": lambda: check_space_page(bundle, claims["space_app_url"]),
        "Public MLflow mirror": lambda: check_mlflow(out_dir / f"{date}-postdeploy-mlflow-mirror.json"),
        "Public links": lambda: check_links(out_dir / f"{date}-postdeploy-links.json"),
    }
    started = _utc()
    surfaces = {name: attempt(check, retries=retries, wait=wait, sleep=sleep) for name, check in checks.items()}
    passed = all(result["passed"] for result in surfaces.values())
    body = {"schema": "publication-receipt-v1", "status": "PASS" if passed else "FAIL", "landing": landing,
            "bundle": str(bundle), "bundle_sha256": expected, "started_utc": started, "completed_utc": _utc(),
            "client": "anonymous urllib and git ls-remote: no cookie, no token, no credential",
            "browser_checks": "not run here: scripts/check_reader_paths.py records are cited by the packet",
            "surfaces": surfaces}
    record_path.write_text(json.dumps(body, indent=2, sort_keys=True) + "\n")
    body["table"] = rows(surfaces, _rel(record_path))
    return body, 0 if passed else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--landing", required=True, help="the landing commit on main")
    parser.add_argument("--bundle", type=Path, required=True, help="the Space bundle the Space should serve")
    parser.add_argument("--expect", required=True, help="that bundle's reviewed SHA-256")
    parser.add_argument("--date", default=datetime.now(timezone.utc).date().isoformat())
    parser.add_argument("--out-dir", type=Path, default=RECORDS)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--wait", type=float, default=30.0, help="seconds between attempts")
    args = parser.parse_args(argv)
    body, code = receipt(resolve(args.landing), args.bundle, args.expect, args.out_dir, args.date,
                         retries=args.retries, wait=args.wait)
    print("\n".join(body["table"]))
    print(f"\n{body['status']}: wrote {_rel(args.out_dir / f'{args.date}-publication-receipt.json')}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
