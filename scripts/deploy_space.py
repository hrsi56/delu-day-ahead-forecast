#!/usr/bin/env python3
"""Upload the reviewed Static Space bundle to Hugging Face -- the Owner's action (AGENTS.md § Git and publication).

    uv run python scripts/deploy_space.py --bundle <dir> --expect <bundle sha256>
    uv run --with huggingface_hub python scripts/deploy_space.py --bundle <dir> --expect <bundle sha256> \\
        --upload --record reports/presentation/release-checks/<date>-space-deployment.json

**Check mode, the default, is safe to run by anyone.** It reads no credential for use and changes nothing: it
recomputes the bundle hash the independent review bound (`scripts/build_wasm_space.py::bundle_sha256`), runs the
credential-value guard over every outbound file (`scripts/secret_guard.py`), and reads the Space's public identity --
its SDK, its visibility and its revision -- anonymously.

**Upload mode is the Owner's.** After the same checks it uploads exactly those files with
`huggingface_hub.HfApi.upload_folder`, against the revision it has just read (so a concurrent change fails rather
than being overwritten), then compares every remote file with the bundle -- the Git blob SHA-1, or the SHA-256 for a
file stored through LFS -- and writes a record. `HF_TOKEN` is read inside the process, from the environment or the
login session, and is never printed, logged or written. `huggingface_hub` is not a project dependency;
`uv run --with` supplies it for this one run without touching `uv.lock`.

Neither mode deletes a remote file: a file the bundle does not carry (the Space template's unused `style.css`) is left
in place and listed in the record.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import secret_guard  # noqa: E402
from build_wasm_space import bundle_sha256  # noqa: E402

REPO = "Yarden-Viktor/delu-day-ahead-forecast"
API = f"https://huggingface.co/api/spaces/{REPO}"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bundle_files(bundle: Path) -> list[str]:
    return sorted((p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file()), key=str.encode)


def check_bundle(bundle: Path, expected: str) -> dict:
    """The bundle is the one the review bound, and no local credential value is in any file of it."""
    if not (bundle / "index.html").is_file():
        raise SystemExit(f"{bundle} holds no index.html; nothing was checked")
    files = bundle_files(bundle)
    actual = bundle_sha256(bundle)
    if actual != expected:
        raise SystemExit(f"bundle hash {actual} is not the reviewed {expected}; no upload")
    findings = secret_guard._scan([(path, (bundle / path).read_bytes()) for path in files], secret_guard.credentials())
    if findings:
        # the guard names the variable and the file, never the value
        raise SystemExit("the credential-value guard blocked the bundle: " + "; ".join(findings))
    return {"bundle": str(bundle), "bundle_sha256": actual, "files": len(files),
            "bytes": sum((bundle / path).stat().st_size for path in files), "credential_guard": "passed"}


def public_identity() -> dict:
    """The Space as an anonymous visitor sees it: SDK, visibility and revision."""
    with urllib.request.urlopen(API, timeout=60) as response:  # noqa: S310 - a fixed https URL
        info = json.loads(response.read())
    return {"sdk": info.get("sdk"), "private": info.get("private"), "revision": info.get("sha"),
            "stage": (info.get("runtime") or {}).get("stage")}


def _token() -> str:
    token = os.environ.get("HF_TOKEN", "")
    if not token:
        result = subprocess.run(["launchctl", "getenv", "HF_TOKEN"], capture_output=True, text=True)
        token = result.stdout.strip()
    if not token:
        raise SystemExit("HF_TOKEN is unset; no upload was attempted")
    return token


def upload(bundle: Path, before: str, message: str) -> dict:
    from huggingface_hub import HfApi  # the Owner's run supplies it with `uv run --with huggingface_hub`
    from huggingface_hub.utils import disable_progress_bars

    disable_progress_bars()
    api = HfApi(token=_token())
    result = api.upload_folder(repo_id=REPO, repo_type="space", folder_path=str(bundle), path_in_repo=".",
                               commit_message=message, parent_commit=before)
    remote = {item.path: item for item in api.list_repo_tree(REPO, repo_type="space", revision=result.oid,
                                                             recursive=True) if hasattr(item, "blob_id")}
    mismatched = []
    for path in bundle_files(bundle):
        item, data = remote.get(path), (bundle / path).read_bytes()
        if item is None:
            mismatched.append(path)
            continue
        lfs = getattr(item, "lfs", None)
        if lfs:
            digest = lfs.sha256 if hasattr(lfs, "sha256") else lfs.get("sha256")
            if digest != hashlib.sha256(data).hexdigest():
                mismatched.append(path)
        elif item.blob_id != hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest():
            mismatched.append(path)
    return {"commit": result.oid, "commit_url": result.commit_url, "remote_files_verified": not mismatched,
            "mismatched": mismatched, "remote_files_not_in_bundle": sorted(set(remote) - set(bundle_files(bundle)))}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--bundle", type=Path, required=True, help="the reviewed bundle directory")
    parser.add_argument("--expect", required=True, help="the bundle SHA-256 the independent review bound")
    parser.add_argument("--upload", action="store_true", help="the Owner's upload; without it, nothing is written")
    parser.add_argument("--message", default="Deploy the reviewed presentation bundle")
    parser.add_argument("--record", type=Path, default=None, help="where the upload writes its record")
    args = parser.parse_args()
    record = {"repo": REPO, "started_utc": _utc(), **check_bundle(args.bundle, args.expect)}
    identity = public_identity()
    record["before"] = identity
    if identity["sdk"] != "static" or identity["private"]:
        raise SystemExit(f"the Space is not a public Static Space: {identity}; no upload")
    if not args.upload:
        record["mode"] = "check only: nothing was uploaded"
        print(json.dumps(record, indent=2, sort_keys=True))
        return 0
    try:
        record.update(upload(args.bundle, identity["revision"], args.message), mode="upload", status="uploaded")
    except SystemExit:
        raise
    except Exception as exc:  # the type and the HTTP status only: an exception text can carry a request URL
        status = getattr(getattr(exc, "response", None), "status_code", None)
        record.update(mode="upload", status="failed", error_type=type(exc).__name__, http_status=status)
    record["completed_utc"] = _utc()
    if args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if record.get("status") == "uploaded" and record.get("remote_files_verified") else 1


if __name__ == "__main__":
    raise SystemExit(main())
