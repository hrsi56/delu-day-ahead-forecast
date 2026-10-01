#!/usr/bin/env python3
"""Deploy the reviewed Static Space bundle to Hugging Face -- the Owner's action (AGENTS.md § Git and publication).

    uv run python scripts/deploy_space.py --bundle <dir> --expect <bundle sha256> [--delete PATH ... | --delete-none]
    uv run --with huggingface_hub python scripts/deploy_space.py --bundle <dir> --expect <bundle sha256> \\
        --upload (--delete PATH ... | --delete-none) \\
        --record reports/presentation/release-checks/<date>-space-deployment.json

**Check mode, the default, is safe to run by anyone.** It reads no credential for use and changes nothing: it
recomputes the bundle hash the independent review bound (`scripts/build_wasm_space.py::bundle_sha256`), runs the
credential-value guard over every outbound file (`scripts/secret_guard.py`), reads the Space's public identity -- its
SDK, its visibility and its revision -- and its file tree at that revision anonymously, and prints the plan: the
bundle files missing from the Space or different there, and the remote files the bundle does not carry, which an
upload would delete.

**Upload mode is the Owner's.** It refuses before any write unless the deletion set it computes is exactly the one
the Owner declared (`--delete PATH`, repeatable, or `--delete-none`). It then makes ONE Hub commit
(`HfApi.create_commit`) against the revision it has just read, so a concurrent change fails rather than being
overwritten: an add for every missing or changed file and a delete for every file the bundle does not carry -- only
deletes when the content already matches, and no commit at all when the Space already serves the bundle. It then
lists the tree at the resulting revision and requires the served file set to equal the bundle by path and per file --
the Git blob SHA-1, or the SHA-256 for a file stored through LFS -- and writes a record. A failure is recorded as the
exception type and HTTP status only. `HF_TOKEN` is read inside that commit, from the environment or the login
session, and is never printed, logged or written. `huggingface_hub` is not a project dependency; `uv run --with`
supplies it for this one run without touching `uv.lock`.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import secret_guard  # noqa: E402
from build_wasm_space import bundle_sha256  # noqa: E402

REPO = "Yarden-Viktor/delu-day-ahead-forecast"
HUB = "https://huggingface.co/"
API = f"{HUB}api/spaces/{REPO}"
MESSAGE = "Deploy the reviewed presentation bundle"

#: {path: {"sha1": Git blob SHA-1 or None, "sha256": content SHA-256 or None}} -- the form both the bundle and the
#: Space's tree are compared in.
Files = dict[str, dict[str, str | None]]


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _sorted(paths) -> list[str]:
    return sorted(paths, key=str.encode)


def bundle_files(bundle: Path) -> list[str]:
    return _sorted(p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file())


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


def local_files(bundle: Path) -> Files:
    """Both identities of every bundle file: the Hub reports the Git blob SHA-1 of a plain file and the SHA-256 of
    one stored through LFS, and which of the two a file gets is the Hub's decision, not ours."""
    out: Files = {}
    for path in bundle_files(bundle):
        data = (bundle / path).read_bytes()
        out[path] = {"sha1": hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest(),
                     "sha256": hashlib.sha256(data).hexdigest()}
    return out


def _hex(value: object) -> str | None:
    return value.lower().removeprefix("sha256:") if isinstance(value, str) and value else None


def parse_tree(entries: object) -> Files:
    """The Hub's recursive tree listing (`/api/spaces/<repo>/tree/<revision>?recursive=true`) as `Files`.

    A plain file's `oid` is its Git blob SHA-1. An LFS file's `oid` names the pointer, not the content, so only its
    `lfs.oid` (a bare hex SHA-256; a `sha256:` prefix is tolerated) is kept. Folders carry no content of their own.
    An entry that cannot be read fails the listing rather than being skipped, and an LFS entry without a content
    hash can never match, so either way a gap shows up as a difference, never as a pass.
    """
    if not isinstance(entries, list):
        raise ValueError("the Hub's tree listing is not a list")
    files: Files = {}
    for entry in entries:
        kind = entry.get("type") if isinstance(entry, dict) else None
        if kind == "directory":
            continue
        path = entry.get("path") if kind == "file" else None
        if not isinstance(path, str) or not path or path in files:
            raise ValueError(f"an unreadable or repeated {kind!r} entry in the Hub's tree listing")
        lfs = entry.get("lfs")
        if lfs is not None:
            files[path] = {"sha1": None, "sha256": _hex(lfs.get("oid") if isinstance(lfs, dict) else None)}
        else:
            files[path] = {"sha1": _hex(entry.get("oid")), "sha256": None}
    return files


def next_page(link: str | None) -> str | None:
    """The `rel="next"` target of a `Link` header -- how the Hub pages a long tree listing."""
    for part in (link or "").split(","):
        match = re.match(r'\s*<([^>]*)>(.*)', part)
        if match and re.search(r'\brel\s*=\s*"?next"?', match.group(2)):
            return match.group(1)
    return None


def same(local: dict, remote: dict) -> bool:
    """An LFS file is compared by SHA-256, a plain one by Git blob SHA-1; a missing hash never matches."""
    if remote.get("sha256"):
        return remote["sha256"] == local["sha256"]
    return bool(remote.get("sha1")) and remote["sha1"] == local["sha1"]


def plan(local: Files, remote: Files) -> dict:
    """What one commit must carry for the Space to serve exactly the bundle."""
    changes = [path for path in local if path in remote and not same(local[path], remote[path])]
    return {"planned_adds": _sorted(set(local) - set(remote)), "planned_changes": _sorted(changes),
            "planned_deletes": _sorted(set(remote) - set(local)),
            "served_equals_bundle": set(local) == set(remote) and not changes}


def verify(local: Files, remote: Files) -> dict:
    """The served file set equals the bundle: no path missing, none extra, and every file's hash the bundle's."""
    mismatched = [path for path in local if path in remote and not same(local[path], remote[path])]
    missing, extra = _sorted(set(local) - set(remote)), _sorted(set(remote) - set(local))
    return {"verified": not (missing or extra or mismatched), "missing": missing, "extra": extra,
            "mismatched": _sorted(mismatched)}


def _token() -> str:
    token = os.environ.get("HF_TOKEN", "")
    if not token:
        result = subprocess.run(["launchctl", "getenv", "HF_TOKEN"], capture_output=True, text=True)
        token = result.stdout.strip()
    if not token:
        raise SystemExit("HF_TOKEN is unset; no upload was attempted")
    return token


class Hub:
    """The real Hub. Every read is an anonymous HTTPS GET of the public API -- what a visitor sees -- and `commit`
    is the one write and the only place `HF_TOKEN` is read. Tests replace this object with a recording fake."""

    def __init__(self, api: str = API) -> None:
        self.api = api

    def _get(self, url: str) -> tuple[object, str | None]:
        if not url.startswith(HUB):
            raise ValueError("a Hub read outside huggingface.co was refused")
        with urllib.request.urlopen(url, timeout=60) as response:  # noqa: S310 - https on huggingface.co only
            return json.loads(response.read()), response.headers.get("Link")

    def identity(self) -> dict:
        """The Space as an anonymous visitor sees it: SDK, visibility and revision."""
        info, _ = self._get(self.api)
        return {"sdk": info.get("sdk"), "private": info.get("private"), "revision": info.get("sha"),
                "stage": (info.get("runtime") or {}).get("stage")}

    def tree(self, revision: str) -> Files:
        url: str | None = f"{self.api}/tree/{urllib.parse.quote(revision, safe='')}?recursive=true"
        entries: list = []
        seen: set[str] = set()
        while url:
            if url in seen:
                raise ValueError("the Hub's tree listing paged in a loop")
            seen.add(url)
            page, link = self._get(url)
            if not isinstance(page, list):
                raise ValueError("a page of the Hub's tree listing is not a list")
            entries += page
            target = next_page(link)
            url = urllib.parse.urljoin(url, target) if target else None
        return parse_tree(entries)

    def commit(self, bundle: Path, adds: list[str], deletes: list[str], parent: str, message: str) -> dict:
        from huggingface_hub import CommitOperationAdd, CommitOperationDelete, HfApi  # `uv run --with huggingface_hub`
        from huggingface_hub.utils import disable_progress_bars

        disable_progress_bars()
        operations = [CommitOperationAdd(path_in_repo=path, path_or_fileobj=str(bundle / path)) for path in adds]
        operations += [CommitOperationDelete(path_in_repo=path) for path in deletes]
        info = HfApi(token=_token()).create_commit(repo_id=REPO, repo_type="space", operations=operations,
                                                    commit_message=message, parent_commit=parent)
        return {"commit": info.oid, "commit_url": info.commit_url}


def _http_status(exc: Exception) -> int | None:
    status = getattr(getattr(exc, "response", None), "status_code", None)
    return status if status is not None else (exc.code if isinstance(getattr(exc, "code", None), int) else None)


def deploy(bundle: Path, expected: str, hub, *, upload: bool = False, declared: list[str] | None = None,
           message: str = MESSAGE) -> tuple[dict, int]:
    """Check, and with `upload` deploy, returning the record and the exit code. Every Hub call goes through `hub`;
    a refusal raises SystemExit before any write, and a failed Hub call is recorded, never raised."""
    if upload and declared is None:
        raise SystemExit("an upload needs the declared deletion set (--delete PATH ... or --delete-none); "
                         "nothing was written")
    record: dict = {"repo": REPO, "started_utc": _utc(), **check_bundle(bundle, expected),
                    "mode": "upload" if upload else "check only: nothing was written"}
    local = local_files(bundle)
    step = "read"
    try:
        identity = hub.identity()
        record.update(before=identity, before_revision=identity.get("revision"))
        if identity.get("sdk") != "static" or identity.get("private") is not False or not identity.get("revision"):
            raise SystemExit(f"the Space is not a public Static Space at a known revision: {identity}; no upload")
        record.update(plan(local, hub.tree(identity["revision"])))
        if declared is not None:
            record["declared_deletes"] = _sorted(set(declared))
            record["declared_matches"] = record["declared_deletes"] == record["planned_deletes"]
        if not upload:
            return record, 0 if record.get("declared_matches", True) else 1
        if not record["declared_matches"]:
            raise SystemExit(f"the deletion set is {record['planned_deletes']}, not the declared "
                             f"{record['declared_deletes']}; nothing was written")
        record.update(commit=None, commit_url=None)
        after = identity["revision"]
        adds = _sorted(record["planned_adds"] + record["planned_changes"])
        if adds or record["planned_deletes"]:
            step = "commit"
            committed = hub.commit(bundle, adds, record["planned_deletes"], identity["revision"], message)
            record.update(commit=committed["commit"], commit_url=committed["commit_url"])
            after = committed["commit"]
        step = "verify"
        record["after_revision"] = after
        record.update(verify(local, hub.tree(after)))
    except Exception as exc:  # the type and the HTTP status only: an exception text can carry a request URL
        record.update(status="failed", failed_step=step, verified=False, error_type=type(exc).__name__,
                      http_status=_http_status(exc), completed_utc=_utc())
        return record, 1
    if record["verified"]:
        record["status"] = "deployed" if record["commit"] else "already identical"
    else:
        record["status"] = "committed, not verified" if record["commit"] else "not verified"
    record["completed_utc"] = _utc()
    return record, 0 if record["verified"] else 1


def main(argv: list[str] | None = None, hub=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--bundle", type=Path, required=True, help="the reviewed bundle directory")
    parser.add_argument("--expect", required=True, help="the bundle SHA-256 the independent review bound")
    parser.add_argument("--upload", action="store_true", help="the Owner's upload; without it, nothing is written")
    declare = parser.add_mutually_exclusive_group()
    declare.add_argument("--delete", action="append", metavar="PATH",
                         help="a remote file the bundle does not carry, which the upload deletes; repeat per file")
    declare.add_argument("--delete-none", action="store_true", help="declare that the upload deletes nothing")
    parser.add_argument("--message", default=MESSAGE)
    parser.add_argument("--record", type=Path, default=None, help="where the upload writes its record")
    args = parser.parse_args(argv)
    declared = [] if args.delete_none else args.delete
    if args.upload and declared is None:
        parser.error("--upload needs the declared deletion set: --delete PATH (repeatable) or --delete-none")
    record, code = deploy(args.bundle, args.expect, hub if hub is not None else Hub(), upload=args.upload,
                          declared=declared, message=args.message)
    if args.upload and args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
    print(json.dumps(record, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
