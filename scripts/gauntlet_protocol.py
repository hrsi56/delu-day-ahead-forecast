#!/usr/bin/env python3
"""Fail-closed local evidence helpers for the Track B Gauntlet.

This module intentionally uses only the Python standard library.  Its public
CLI can:

* initialize one ignored evidence directory for a Critic run;
* validate a component or Integration Critic verdict against the repository's
  documented v1 schema and all referenced local evidence;
* create or verify (never delete or publish) a local evidence-retention ref.
* execute the create-only CP-2 Blind prepare, recompute, freeze, reveal, and
  exact adjudication state transitions.

Two private CLI commands are used by ``gauntlet_critic_snapshot.sh`` to write
the before/after snapshot integrity manifest atomically.
"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import csv
import datetime as dt
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import io
import json
import os
from pathlib import Path
import re
import secrets
import stat
import subprocess
import sys
import tempfile
from typing import Any, Iterable, Mapping, NoReturn, Sequence


SCHEMA_VERSION = "1.0"
IDENTIFIER_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
GIT_SHA_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z$")
INTEGRITY_RECORD_TYPE = "gauntlet_snapshot_integrity_manifest"
COMPONENT_RECORD_TYPE = "component_critic_verdict"
INTEGRATION_RECORD_TYPE = "integration_critic_verdict"
SNAPSHOT_HELPER_RELATIVE_PATH = "scripts/gauntlet_critic_snapshot.sh"
PROTOCOL_HELPER_RELATIVE_PATH = "scripts/gauntlet_protocol.py"
VERDICT_SCHEMA_RELATIVE_PATH = "docs/track-b/schemas/critic-verdict.schema.json"
CP2_BLIND_SCHEMA_RELATIVE_PATH = (
    "docs/track-b/schemas/cp2-blind-four-catalog.schema.json"
)
CP2_SOURCE_MANIFEST_RELATIVE_PATH = "artifacts/cp2/blind/source-manifest.json"
CP2_SELECTION_DECLARATION_RELATIVE_PATH = (
    "artifacts/cp2/blind/selection-declaration.json"
)
CP2_BLIND_SCHEMA_ID = (
    "https://pjm.local/schemas/cp2-blind-four-catalog.schema.json"
)
CP2_BLIND_SCHEMA_VERSION = "1.0"
CP2_PERMUTATION_VERSION = "sha256-fisher-yates-v1"
CP2_COMMITMENT_DOMAIN = "PJM-CP2-BLIND-FOUR-CATALOG-COMMITMENT-v1"
CP2_PERMUTATION_DOMAIN = b"PJM-CP2-FY-v1\x00"
CP2_LABELS = ("A", "B", "C", "D")
CP2_FOLDS = (1, 2, 3, 4, 5)
CP2_SEMANTIC_ROLES = (
    "strict_base",
    "residual_arm",
    "scarcity_arm",
    "both_arms",
)
CP2_FEATURE_COUNTS = {
    "strict_base": 0,
    "residual_arm": 1,
    "scarcity_arm": 1,
    "both_arms": 2,
}
CP2_PREFERENCE = ("residual_arm", "scarcity_arm", "both_arms")
CP2_QUANTILES = (
    ("q025", Decimal("0.025")),
    ("q05", Decimal("0.05")),
    ("q10", Decimal("0.10")),
    ("q25", Decimal("0.25")),
    ("q50", Decimal("0.50")),
    ("q75", Decimal("0.75")),
    ("q90", Decimal("0.90")),
    ("q95", Decimal("0.95")),
    ("q975", Decimal("0.975")),
)
CP2_ANONYMOUS_HEADER = (
    "label",
    "fold_id",
    "row_id",
    "y",
    *(name for name, _ in CP2_QUANTILES),
)
CP2_SOURCE_HEADER = CP2_ANONYMOUS_HEADER[1:]
CP2_ROW_ID_RE = re.compile(r"^r[0-9]{6,}$")
CP2_DECIMAL_RE = re.compile(r"^-?(?:0|[1-9][0-9]*)(?:\.[0-9]+)?$")
CP2_PUBLIC_INPUT_FILENAME = "blind-public-input.csv"
CP2_PUBLIC_MANIFEST_FILENAME = "blind-public-manifest.json"
CP2_COMMITMENT_FILENAME = "blind-commitment.json"
CP2_METRICS_FILENAME = "blind-metrics.json"
CP2_FREEZE_FILENAME = "blind-freeze.json"
CP2_REVEAL_FILENAME = "blind-reveal.json"
CP2_ADJUDICATION_FILENAME = "blind-adjudication.json"
CP2_PREPARATION_RECEIPT_FILENAME = "blind-preparation-receipt.json"
CP2_RECOMPUTE_ATTEMPT_FILENAME = "blind-recompute-attempt.json"
CP2_FREEZE_ATTEMPT_FILENAME = "blind-freeze-attempt.json"
CP2_REVEAL_ATTEMPT_FILENAME = "blind-reveal-attempt.json"
CP2_ADJUDICATE_ATTEMPT_FILENAME = "blind-adjudicate-attempt.json"
CP2_CUSTODY_RECORD_FILENAME = "preparation-record.json"
CP2_PREPARATION_INVOCATION_FILENAME = "preparation-invocation.json"
CP2_MAPPING_PREIMAGE_FILENAME = "mapping-preimage.json"
CP2_CUSTODY_SOURCE_MANIFEST_FILENAME = "source-manifest.json"
CP2_CUSTODY_SELECTION_FILENAME = "selection-declaration.json"
CP2_REVEALED_MAPPING_FILENAME = "revealed-mapping.json"
CP2_REVEALED_PREPARATION_FILENAME = "revealed-preparation-record.json"
CP2_REVEALED_SOURCE_MANIFEST_FILENAME = "revealed-source-manifest.json"
CP2_REVEALED_SELECTION_FILENAME = "revealed-selection-declaration.json"
CP2_FROZEN_ANONYMOUS_FILENAME = "frozen-blind-public-input.csv"
CP2_FROZEN_PUBLIC_MANIFEST_FILENAME = "frozen-blind-public-manifest.json"
CP2_FROZEN_COMMITMENT_FILENAME = "frozen-blind-commitment.json"
CP2_FROZEN_RECEIPT_FILENAME = "frozen-blind-preparation-receipt.json"
CP2_FROZEN_METRICS_FILENAME = "frozen-blind-metrics.json"
CP2_RULE_VERSION = "cp2-four-catalog-exact-v1"
CP2_CANONICALIZATION_VERSION = "utf8-lf-decimal-interleaved-v1"
CP2_IDENTITY_TOKENS = (
    "strict_base",
    "strict base",
    "strict-base",
    "residual_arm",
    "residual arm",
    "residual-arm",
    "scarcity_arm",
    "scarcity arm",
    "scarcity-arm",
    "both_arms",
    "both arms",
    "both-arms",
    CP2_SOURCE_MANIFEST_RELATIVE_PATH,
    CP2_SELECTION_DECLARATION_RELATIVE_PATH,
)
CP2_BLIND_REVIEW_REQUIRED_FIELDS = (
    "blind_review_id",
    "public_manifest",
    "commitment",
    "preparation_receipt",
    "metrics",
    "protocol_schema",
    "recompute_command",
    "identity_decision",
)
CP2_BLIND_ADJUDICATION_REQUIRED_FIELDS = (
    "blind_review_id",
    "freeze",
    "reveal",
    "adjudication",
    "selected_role",
    "selection_declaration",
)
CP2_HASH_BINDING_REQUIRED_FIELDS = ("path", "sha256")
CP2_REPO_BLOB_BINDING_REQUIRED_FIELDS = ("repo_relative_path", "sha256")
CP2_SAFE_REPO_PATH_RE = re.compile(
    r"^(?!.*(?:^|/)\.{1,2}(?:/|$))(?!.*//)(?!/)[A-Za-z0-9_. -]+"
    r"(?:/[A-Za-z0-9_. -]+)*$"
)
VERDICT_BASE_REQUIRED_FIELDS = (
    "record_type",
    "schema_version",
    "run_id",
    "checkpoint",
    "piece",
    "critic_id",
    "verdict",
    "candidate",
    "verdict_schema",
    "artifact",
    "plan",
    "inputs",
    "commands",
    "expected_output",
    "tolerance",
    "integrity_manifest",
    "evidence",
    "reviewed_paths",
    "largest_meaningful_gap",
    "next_acceptance_test",
    "recorded_at_utc",
)
CANDIDATE_REQUIRED_FIELDS = ("commit_sha", "tree_sha", "evidence_ref")
COMMAND_REQUIRED_FIELDS = (
    "command",
    "exit_code",
    "stdout_path",
    "stdout_sha256",
    "stderr_path",
    "stderr_sha256",
)
EVIDENCE_REQUIRED_FIELDS = ("description", "path", "sha256")
PLAN_REQUIRED_FIELDS = (
    "filename",
    "version",
    "sha256",
    "bar_citation",
    "bar_excerpt",
)
COMPONENT_BINDING_REQUIRED_FIELDS = (
    "piece",
    "path",
    "sha256",
    "candidate_sha",
    "candidate_tree",
    "reviewed_paths",
)
REPO_RELATIVE_MARKDOWN_RE = re.compile(
    r"^(?!.*(?:^|/)\.{1,2}(?:/|$))(?!.*//)[A-Za-z0-9_. -]+"
    r"(?:/[A-Za-z0-9_. -]+)*\.md$"
)


class ProtocolError(RuntimeError):
    """An evidence or protocol invariant failed."""


def fail(message: str) -> NoReturn:
    raise ProtocolError(message)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def sha256_file(path: Path) -> str:
    descriptor: int | None = None
    try:
        descriptor = os.open(
            str(path),
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            fail(f"Refusing non-regular evidence file: {path}")
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = None
            digest = hashlib.sha256()
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
            return digest.hexdigest()
    except OSError as exc:
        fail(f"Cannot hash evidence file {path}: {exc}")
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _read_regular_file(path: Path, field: str) -> bytes:
    descriptor: int | None = None
    try:
        descriptor = os.open(
            str(path),
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            fail(f"Refusing non-regular {field}: {path}")
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = None
            return handle.read()
    except OSError as exc:
        fail(f"Cannot read {field} {path}: {exc}")
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _load_json(path: Path) -> tuple[Mapping[str, Any], bytes]:
    if not path.is_absolute():
        fail(f"JSON path must be absolute: {path}")
    raw = _read_regular_file(path, "JSON file")
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"Invalid JSON in {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root must be an object: {path}")
    return value, raw


def _atomic_json_write(
    path: Path,
    value: Mapping[str, Any],
    *,
    create: bool,
    expected_existing_sha256: str | None = None,
) -> str:
    if not path.is_absolute():
        fail(f"Manifest path must be absolute: {path}")
    if path.is_symlink():
        fail(f"Refusing symlinked manifest path: {path}")
    if create and path.exists():
        fail(f"Refusing to overwrite existing manifest: {path}")
    if not create and not path.is_file():
        fail(f"Manifest does not exist: {path}")
    if create and expected_existing_sha256 is not None:
        fail("Atomic create may not supply an existing-file hash")
    if not create and expected_existing_sha256 is None:
        fail("Atomic manifest replacement requires the expected existing SHA-256")
    if not path.parent.is_dir():
        fail(f"Manifest parent does not exist: {path.parent}")

    payload = _canonical_json_bytes(value)
    temporary_name: str | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
        )
        os.fchmod(descriptor, 0o600)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        if create:
            try:
                os.link(temporary_name, path)
            except FileExistsError:
                fail(f"Manifest appeared during atomic create: {path}")
            os.unlink(temporary_name)
            temporary_name = None
        else:
            actual_existing_hash = sha256_file(path)
            if actual_existing_hash != expected_existing_sha256:
                fail(
                    "Integrity manifest changed before atomic replacement: "
                    f"expected {expected_existing_sha256}, got {actual_existing_hash}"
                )
            os.replace(temporary_name, path)
            temporary_name = None
        directory_fd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except OSError as exc:
        fail(f"Cannot atomically write manifest {path}: {exc}")
    finally:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
    return _sha256_bytes(payload)


def _atomic_bytes_create(path: Path, payload: bytes, *, mode: int = 0o600) -> str:
    """Create one immutable-by-name regular file without an overwrite window."""

    if not path.is_absolute():
        fail(f"Output path must be absolute: {path}")
    if path.exists() or path.is_symlink():
        fail(f"Refusing to overwrite existing protocol artifact: {path}")
    if not path.parent.is_dir() or path.parent.is_symlink():
        fail(f"Protocol artifact parent is missing or symlinked: {path.parent}")
    temporary_name: str | None = None
    try:
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
        )
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary_name, path)
        except FileExistsError:
            fail(f"Protocol artifact appeared during atomic create: {path}")
        os.unlink(temporary_name)
        temporary_name = None
        os.chmod(path, mode)
        directory_fd = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except OSError as exc:
        fail(f"Cannot atomically create protocol artifact {path}: {exc}")
    finally:
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
    return _sha256_bytes(payload)


def _read_single_link_file(path: Path, field: str) -> bytes:
    descriptor: int | None = None
    try:
        descriptor = os.open(
            str(path),
            os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0),
        )
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            fail(f"Refusing non-regular {field}: {path}")
        if metadata.st_nlink != 1:
            fail(f"Refusing hard-linked {field} (st_nlink={metadata.st_nlink}): {path}")
        with os.fdopen(descriptor, "rb") as handle:
            descriptor = None
            return handle.read()
    except OSError as exc:
        fail(f"Cannot read {field} {path}: {exc}")
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _require_mode(path: Path, expected: int, field: str) -> None:
    try:
        metadata = os.lstat(path)
    except OSError as exc:
        fail(f"Cannot stat {field} {path}: {exc}")
    actual = stat.S_IMODE(metadata.st_mode)
    if actual != expected:
        fail(f"{field} mode must be {expected:04o}, got {actual:04o}: {path}")


def _timestamp_after(previous: str | None = None) -> str:
    now = dt.datetime.now(dt.timezone.utc)
    if previous is not None:
        previous_value = parse_utc(previous)
        if now <= previous_value:
            now = previous_value + dt.timedelta(microseconds=1)
    return now.isoformat(timespec="microseconds").replace("+00:00", "Z")


def _cp2_require_runtime_tool_hash(expected_sha256: str) -> str:
    expected = require_sha256(expected_sha256, "runtime protocol tool SHA-256")
    runtime_path = Path(__file__).resolve(strict=True)
    actual = sha256_file(runtime_path)
    if actual != expected:
        fail(
            "Executing gauntlet_protocol.py bytes do not match the protocol tool "
            f"bound by this CP-2 attempt: expected {expected}, got {actual}"
        )
    return actual


@contextmanager
def _exclusive_manifest_verify_lock(manifest_path: Path) -> Iterable[None]:
    lock_path = manifest_path.parent / ".integrity-manifest.verify.lock"
    descriptor: int | None = None
    try:
        try:
            descriptor = os.open(
                str(lock_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
            )
        except FileExistsError:
            fail(f"Integrity manifest verification is already locked: {lock_path}")
        payload = f"pid={os.getpid()} started_at_utc={utc_now()}\n".encode("utf-8")
        os.write(descriptor, payload)
        os.fsync(descriptor)
        yield
    finally:
        if descriptor is not None:
            os.close(descriptor)
            try:
                os.unlink(lock_path)
            except FileNotFoundError:
                pass


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace(
        "+00:00", "Z"
    )


def require_identifier(value: Any, field: str) -> str:
    if not isinstance(value, str) or not IDENTIFIER_RE.fullmatch(value):
        fail(
            f"{field} must match {IDENTIFIER_RE.pattern} and may not contain slashes"
        )
    return value


def require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        fail(f"{field} must be a non-empty string")
    return value


def require_git_sha(value: Any, field: str) -> str:
    if not isinstance(value, str) or not GIT_SHA_RE.fullmatch(value):
        fail(f"{field} must be a full lowercase 40- or 64-hex Git object ID")
    return value


def require_sha256(value: Any, field: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        fail(f"{field} must be a lowercase SHA-256 digest")
    return value


def require_json_integer(value: Any, field: str) -> int:
    """Require JSON's lexical integer representation, excluding bool and 1.0."""

    if type(value) is not int:
        fail(f"{field} must decode as a non-Boolean JSON integer")
    return value


def require_json_boolean(value: Any, field: str) -> bool:
    if type(value) is not bool:
        fail(f"{field} must decode as a JSON Boolean")
    return value


def _json_exact_equal(left: Any, right: Any) -> bool:
    """JSON comparison that never treats bool/int/float as interchangeable."""

    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(
            _json_exact_equal(left[key], right[key]) for key in left
        )
    if isinstance(left, list):
        return len(left) == len(right) and all(
            _json_exact_equal(left_item, right_item)
            for left_item, right_item in zip(left, right, strict=True)
        )
    return left == right


def require_absolute_path(value: Any, field: str) -> Path:
    if not isinstance(value, str) or not value:
        fail(f"{field} must be a non-empty absolute path")
    path = Path(value)
    if not path.is_absolute():
        fail(f"{field} must be absolute: {value}")
    return path


def require_utc(value: Any, field: str) -> str:
    if not isinstance(value, str) or not UTC_RE.fullmatch(value):
        fail(f"{field} must be an ISO-8601 UTC timestamp ending in Z")
    try:
        parsed = dt.datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as exc:
        fail(f"{field} is not a valid UTC timestamp: {exc}")
    if parsed.utcoffset() != dt.timedelta(0):
        fail(f"{field} must be UTC")
    return value


def parse_utc(value: str) -> dt.datetime:
    require_utc(value, "timestamp")
    return dt.datetime.fromisoformat(value[:-1] + "+00:00")


def require_exact_keys(
    value: Any,
    field: str,
    *,
    required: Iterable[str],
    optional: Iterable[str] = (),
) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        fail(f"{field} must be an object")
    required_set = set(required)
    allowed_set = required_set | set(optional)
    missing = sorted(required_set - set(value))
    unknown = sorted(set(value) - allowed_set)
    if missing:
        fail(f"{field} is missing required fields: {', '.join(missing)}")
    if unknown:
        fail(f"{field} has unknown fields: {', '.join(unknown)}")
    return value


def _is_within(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def _canonical_path(path: Path) -> Path:
    if not path.is_absolute():
        fail(f"Path must be absolute: {path}")
    try:
        return path.resolve(strict=True)
    except OSError as exc:
        fail(f"Cannot resolve path {path}: {exc}")


def _git(repo_root: Path, arguments: Sequence[str]) -> str:
    command = ["git", "-C", str(repo_root), *arguments]
    try:
        result = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except OSError as exc:
        fail(f"Cannot execute git: {exc}")
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        fail(f"{' '.join(command)} failed: {detail}")
    return result.stdout.strip()


def _git_bytes(repo_root: Path, arguments: Sequence[str]) -> bytes:
    command = ["git", "-C", str(repo_root), *arguments]
    try:
        result = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        fail(f"Cannot execute git: {exc}")
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        fail(f"{' '.join(command)} failed: {detail or 'unknown git error'}")
    return result.stdout


def canonical_repo_root(repo_root_input: str) -> Path:
    path = require_absolute_path(repo_root_input, "repo_root")
    root = _canonical_path(path)
    actual = Path(_git(root, ["rev-parse", "--show-toplevel"])).resolve(strict=True)
    if root != actual:
        fail(f"repo_root must be the exact Git top level: expected {actual}, got {root}")
    return root


def _reject_symlinked_evidence_ancestors(
    repo_root: Path,
    checkpoint: str,
    *,
    include_run: str | None = None,
    include_support_run: str | None = None,
) -> None:
    paths = [
        repo_root / ".gauntlet",
        repo_root / ".gauntlet" / "evidence",
        repo_root / ".gauntlet" / "evidence" / checkpoint,
    ]
    if include_run is not None:
        paths.append(paths[-1] / include_run)
    support_root = repo_root / ".gauntlet" / "evidence" / checkpoint / "_support"
    paths.append(support_root)
    if include_support_run is not None:
        paths.append(support_root / include_support_run)
    for path in paths:
        if path.is_symlink():
            fail(f"Evidence ancestor may not be a symlink: {path}")


def _evidence_context_from_run_path(
    run_path: Path, checkpoint: str, run_id: str
) -> tuple[Path, Path, Path]:
    checkpoint = require_identifier(checkpoint, "checkpoint")
    run_id = require_identifier(run_id, "run_id")
    if run_path.name != run_id:
        fail(f"Evidence run path does not match run_id {run_id}: {run_path}")
    checkpoint_path = run_path.parent
    if checkpoint_path.name != checkpoint:
        fail(
            f"Evidence run path does not match checkpoint {checkpoint}: {run_path}"
        )
    if checkpoint_path.parent.name != "evidence" or checkpoint_path.parent.parent.name != ".gauntlet":
        fail(
            "Evidence run must live at the exact Git repository path "
            ".gauntlet/evidence/<checkpoint>/<run-id>"
        )
    repo_root = checkpoint_path.parent.parent.parent
    repo_root = canonical_repo_root(str(repo_root))
    expected = repo_root / ".gauntlet" / "evidence" / checkpoint / run_id
    if run_path != expected:
        fail(f"Evidence run path is not canonical: expected {expected}, got {run_path}")
    _reject_symlinked_evidence_ancestors(
        repo_root,
        checkpoint,
        include_run=run_id,
        include_support_run=run_id,
    )
    support_root = checkpoint_path / "_support" / run_id
    if support_root.is_symlink() or not support_root.is_dir():
        fail(f"Critic support ownership directory is missing or symlinked: {support_root}")
    resolved_support = support_root.resolve(strict=True)
    if resolved_support != support_root:
        fail(
            f"Critic support ownership path traverses a symlink: "
            f"{support_root} -> {resolved_support}"
        )
    return repo_root, checkpoint_path, support_root


def _validate_full_commit(repo_root: Path, candidate_sha: str) -> tuple[str, str]:
    require_git_sha(candidate_sha, "candidate_sha")
    resolved = _git(repo_root, ["rev-parse", "--verify", f"{candidate_sha}^{{commit}}"])
    if resolved != candidate_sha:
        fail(f"candidate_sha is not the full resolved commit SHA: {resolved}")
    tree = _git(repo_root, ["rev-parse", "--verify", f"{candidate_sha}^{{tree}}"])
    require_git_sha(tree, "candidate_tree")
    return resolved, tree


def _ensure_real_directory(path: Path, *, mode: int = 0o700) -> None:
    if path.is_symlink():
        fail(f"Evidence ancestor may not be a symlink: {path}")
    try:
        path.mkdir(mode=mode, exist_ok=True)
    except OSError as exc:
        fail(f"Cannot create evidence directory {path}: {exc}")
    if path.is_symlink() or not path.is_dir():
        fail(f"Evidence ancestor must be a real directory: {path}")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        fail(f"Cannot resolve evidence directory {path}: {exc}")
    if resolved != path:
        fail(f"Evidence directory traverses a symlink: {path} -> {resolved}")


@contextmanager
def _exclusive_evidence_init_lock(
    checkpoint_root: Path, run_id: str
) -> Iterable[None]:
    lock_path = checkpoint_root / f".{run_id}.init.lock"
    descriptor: int | None = None
    try:
        try:
            descriptor = os.open(
                str(lock_path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
            )
        except FileExistsError:
            fail(f"Evidence initialization is already locked: {lock_path}")
        os.write(descriptor, f"pid={os.getpid()}\n".encode("utf-8"))
        os.fsync(descriptor)
        yield
    finally:
        if descriptor is not None:
            os.close(descriptor)
            try:
                os.unlink(lock_path)
            except FileNotFoundError:
                pass


def initialize_evidence_root(
    repo_root_input: str, checkpoint: str, run_id: str
) -> tuple[Path, Path]:
    repo_root = canonical_repo_root(repo_root_input)
    checkpoint = require_identifier(checkpoint, "checkpoint")
    run_id = require_identifier(run_id, "run_id")
    checkpoint_root = repo_root / ".gauntlet" / "evidence" / checkpoint
    evidence_root = checkpoint_root / run_id
    support_parent = checkpoint_root / "_support"
    support_root = support_parent / run_id
    _reject_symlinked_evidence_ancestors(repo_root, checkpoint)

    for path in (evidence_root, support_root):
        ignored = subprocess.run(
            [
                "git",
                "-C",
                str(repo_root),
                "check-ignore",
                "-q",
                "--no-index",
                str(path),
            ],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        if ignored.returncode != 0:
            detail = ignored.stderr.strip()
            suffix = f" ({detail})" if detail else ""
            fail(f"Evidence path is not ignored by Git: {path}{suffix}")

    for ancestor in (
        repo_root / ".gauntlet",
        repo_root / ".gauntlet" / "evidence",
        checkpoint_root,
        support_parent,
    ):
        _ensure_real_directory(ancestor)

    with _exclusive_evidence_init_lock(checkpoint_root, run_id):
        _reject_symlinked_evidence_ancestors(
            repo_root,
            checkpoint,
            include_run=run_id,
            include_support_run=run_id,
        )
        existing = [
            path for path in (evidence_root, support_root) if path.exists() or path.is_symlink()
        ]
        if existing:
            fail(
                "Refusing to reuse Critic evidence ownership path(s): "
                + ", ".join(str(path) for path in existing)
            )
        created_evidence = False
        created_support = False
        try:
            evidence_root.mkdir(mode=0o700)
            created_evidence = True
            support_root.mkdir(mode=0o700)
            created_support = True
            os.chmod(evidence_root, 0o700)
            os.chmod(support_root, 0o700)
        except OSError as exc:
            if created_support:
                try:
                    support_root.rmdir()
                except OSError:
                    pass
            if created_evidence:
                try:
                    evidence_root.rmdir()
                except OSError:
                    pass
            fail(f"Cannot initialize paired Critic evidence paths: {exc}")

    resolved_evidence = evidence_root.resolve(strict=True)
    resolved_support = support_root.resolve(strict=True)
    for path, resolved in (
        (evidence_root, resolved_evidence),
        (support_root, resolved_support),
    ):
        if not _is_within(resolved, repo_root) or resolved != path:
            fail(f"Evidence path escaped or traversed a symlink: {path} -> {resolved}")
    _reject_symlinked_evidence_ancestors(
        repo_root,
        checkpoint,
        include_run=run_id,
        include_support_run=run_id,
    )
    return resolved_evidence, resolved_support


def _manifest_path_checks(manifest_path: Path, snapshot_path: Path) -> tuple[Path, Path]:
    if manifest_path.name != "integrity-manifest.json":
        fail("Integrity manifest filename must be integrity-manifest.json")
    if not manifest_path.parent.is_dir():
        fail(f"Manifest parent does not exist: {manifest_path.parent}")
    manifest_parent = manifest_path.parent.resolve(strict=True)
    canonical_manifest = manifest_parent / manifest_path.name
    canonical_snapshot = _canonical_path(snapshot_path)
    if _is_within(canonical_manifest, canonical_snapshot):
        fail("Integrity manifest must be outside the Critic snapshot")
    return canonical_manifest, canonical_snapshot


def _validate_tool_binding(value: Any, field: str, expected_path: str) -> None:
    value = require_exact_keys(
        value, field, required=("repo_relative_path", "sha256")
    )
    if value["repo_relative_path"] != expected_path:
        fail(f"{field}.repo_relative_path must be {expected_path}")
    require_sha256(value["sha256"], f"{field}.sha256")


def _bind_integrity_tools(
    snapshot_path: Path,
    snapshot_helper_path_input: str,
    snapshot_helper_sha256: str,
    protocol_helper_path_input: str,
    protocol_helper_sha256: str,
) -> Mapping[str, Any]:
    """Bind invoking tools to identical committed copies in the candidate tree."""

    bindings: dict[str, Any] = {}
    for name, relative_path, invoking_input, supplied_hash in (
        (
            "snapshot_helper",
            SNAPSHOT_HELPER_RELATIVE_PATH,
            snapshot_helper_path_input,
            snapshot_helper_sha256,
        ),
        (
            "protocol_helper",
            PROTOCOL_HELPER_RELATIVE_PATH,
            protocol_helper_path_input,
            protocol_helper_sha256,
        ),
    ):
        invoking_path = require_absolute_path(invoking_input, f"{name}_path")
        supplied_hash = require_sha256(supplied_hash, f"{name}_sha256")
        if not invoking_path.is_file() or invoking_path.is_symlink():
            fail(f"Invoking {name} is missing or symlinked: {invoking_path}")
        invoking_hash = sha256_file(invoking_path)
        if invoking_hash != supplied_hash:
            fail(
                f"Invoking {name} SHA-256 mismatch: expected {supplied_hash}, "
                f"got {invoking_hash}"
            )
        committed_path = snapshot_path / relative_path
        if not committed_path.is_file() or committed_path.is_symlink():
            fail(f"Candidate snapshot lacks committed {relative_path}")
        committed_hash = sha256_file(committed_path)
        if committed_hash != invoking_hash:
            fail(
                f"Invoking {name} does not match committed candidate copy "
                f"{relative_path}: {invoking_hash} != {committed_hash}"
            )
        bindings[name] = {
            "repo_relative_path": relative_path,
            "sha256": invoking_hash,
        }
    return bindings


def _run_git_integrity_check(
    snapshot_path: Path, arguments: Sequence[str], field: str
) -> bytes:
    command = ["git", "-C", str(snapshot_path), *arguments]
    try:
        result = subprocess.run(
            command,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as exc:
        fail(f"Cannot execute {field}: {exc}")
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        fail(f"{field} failed: {detail or f'exit code {result.returncode}'}")
    return result.stdout


def _integrity_checks(
    snapshot_path: Path, candidate_sha: str, candidate_tree: str
) -> Mapping[str, Any]:
    """Observe the snapshot directly; never serialize caller-reported success."""

    snapshot_path = _canonical_path(snapshot_path)
    if not snapshot_path.is_dir():
        fail(f"Critic snapshot is not a directory: {snapshot_path}")
    top_level = Path(
        _run_git_integrity_check(
            snapshot_path, ["rev-parse", "--show-toplevel"], "snapshot top-level check"
        )
        .decode("utf-8", errors="strict")
        .strip()
    ).resolve(strict=True)
    if top_level != snapshot_path:
        fail(f"Critic snapshot must be the exact worktree top level: {top_level}")

    common_text = (
        _run_git_integrity_check(
            snapshot_path, ["rev-parse", "--git-common-dir"], "Git common-dir check"
        )
        .decode("utf-8", errors="strict")
        .strip()
    )
    common_path = Path(common_text)
    if not common_path.is_absolute():
        common_path = snapshot_path / common_path
    common_path = common_path.resolve(strict=True)
    if common_path.name != ".git":
        fail("Critic snapshot must be a linked worktree of a non-bare repository")
    source_repo_root = common_path.parent.resolve(strict=True)
    if _is_within(snapshot_path, source_repo_root):
        fail("Critic snapshot must be outside the Builder repository")

    head = (
        _run_git_integrity_check(
            snapshot_path, ["rev-parse", "--verify", "HEAD"], "snapshot HEAD check"
        )
        .decode("ascii", errors="strict")
        .strip()
    )
    tree = (
        _run_git_integrity_check(
            snapshot_path,
            ["rev-parse", "--verify", "HEAD^{tree}"],
            "snapshot tree check",
        )
        .decode("ascii", errors="strict")
        .strip()
    )
    if head != candidate_sha or tree != candidate_tree:
        fail(
            "Critic snapshot SHA/tree mismatch: "
            f"expected {candidate_sha}/{candidate_tree}, got {head}/{tree}"
        )

    branch = subprocess.run(
        ["git", "-C", str(snapshot_path), "symbolic-ref", "--quiet", "HEAD"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if branch.returncode == 0:
        branch_name = branch.stdout.decode("utf-8", errors="replace").strip()
        fail(f"Critic snapshot is not detached: {branch_name}")
    if branch.returncode != 1:
        detail = branch.stderr.decode("utf-8", errors="replace").strip()
        fail(f"Cannot verify detached Critic HEAD: {detail or branch.returncode}")

    workbench = snapshot_path / "workbench.md"
    if workbench.exists() or workbench.is_symlink():
        fail("workbench.md must not exist in the Critic snapshot")
    _run_git_integrity_check(
        snapshot_path,
        ["diff", "--quiet", "--exit-code"],
        "tracked snapshot diff check",
    )
    _run_git_integrity_check(
        snapshot_path,
        ["diff", "--cached", "--quiet", "--exit-code"],
        "snapshot index diff check",
    )
    status = _run_git_integrity_check(
        snapshot_path,
        [
            "status",
            "--porcelain=v1",
            "--untracked-files=all",
            "--ignored=matching",
        ],
        "snapshot tracked/index/untracked/ignored status check",
    )
    if status:
        rendered = status.decode("utf-8", errors="replace").rstrip("\n")
        fail(f"Critic snapshot is not clean:\n{rendered}")

    return {
        "head_sha": head,
        "tree_sha": tree,
        "detached_head": True,
        "workbench_absent": True,
        "tracked_diff": {
            "command": "git diff --quiet --exit-code",
            "exit_code": 0,
        },
        "index_diff": {
            "command": "git diff --cached --quiet --exit-code",
            "exit_code": 0,
        },
        "status": {
            "command": "git status --porcelain=v1 --untracked-files=all --ignored=matching",
            "raw_output": "",
            "raw_output_sha256": _sha256_bytes(status),
        },
    }


def create_integrity_manifest(
    manifest_input: str,
    run_id: str,
    candidate_sha: str,
    candidate_tree: str,
    snapshot_input: str,
    snapshot_helper_path_input: str,
    snapshot_helper_sha256: str,
    protocol_helper_path_input: str,
    protocol_helper_sha256: str,
) -> str:
    manifest_path = require_absolute_path(manifest_input, "manifest")
    snapshot_path = require_absolute_path(snapshot_input, "snapshot_path")
    manifest_path, snapshot_path = _manifest_path_checks(manifest_path, snapshot_path)
    run_id = require_identifier(run_id, "run_id")
    checkpoint = require_identifier(manifest_path.parent.parent.name, "checkpoint")
    _evidence_context_from_run_path(manifest_path.parent, checkpoint, run_id)
    candidate_sha = require_git_sha(candidate_sha, "candidate_sha")
    candidate_tree = require_git_sha(candidate_tree, "candidate_tree")
    if len(candidate_sha) != len(candidate_tree):
        fail("candidate_sha and candidate_tree must use the same Git object format")
    tool_bindings = _bind_integrity_tools(
        snapshot_path,
        snapshot_helper_path_input,
        snapshot_helper_sha256,
        protocol_helper_path_input,
        protocol_helper_sha256,
    )
    record: Mapping[str, Any] = {
        "record_type": INTEGRITY_RECORD_TYPE,
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "checkpoint": checkpoint,
        "candidate_sha": candidate_sha,
        "candidate_tree": candidate_tree,
        "snapshot_path": str(snapshot_path),
        "evidence_run_path": str(manifest_path.parent),
        "create": {
            "recorded_at_utc": utc_now(),
            "tools": tool_bindings,
            "checks": _integrity_checks(snapshot_path, candidate_sha, candidate_tree),
        },
        "verify": None,
    }
    return _atomic_json_write(manifest_path, record, create=True)


def _validate_integrity_record_shape(
    record: Mapping[str, Any], *, require_verify: bool
) -> Mapping[str, Any]:
    record = require_exact_keys(
        record,
        "integrity_manifest",
        required=(
            "record_type",
            "schema_version",
            "run_id",
            "checkpoint",
            "candidate_sha",
            "candidate_tree",
            "snapshot_path",
            "evidence_run_path",
            "create",
            "verify",
        ),
    )
    if record["record_type"] != INTEGRITY_RECORD_TYPE:
        fail("Integrity manifest has an unexpected record_type")
    if record["schema_version"] != SCHEMA_VERSION:
        fail("Integrity manifest has an unsupported schema_version")
    require_identifier(record["run_id"], "integrity_manifest.run_id")
    require_identifier(record["checkpoint"], "integrity_manifest.checkpoint")
    candidate_sha = require_git_sha(
        record["candidate_sha"], "integrity_manifest.candidate_sha"
    )
    candidate_tree = require_git_sha(
        record["candidate_tree"], "integrity_manifest.candidate_tree"
    )
    if len(candidate_sha) != len(candidate_tree):
        fail("Integrity manifest SHA and tree use different object formats")
    require_absolute_path(record["snapshot_path"], "integrity_manifest.snapshot_path")
    require_absolute_path(
        record["evidence_run_path"], "integrity_manifest.evidence_run_path"
    )
    create = require_exact_keys(
        record["create"],
        "integrity_manifest.create",
        required=(
            "recorded_at_utc",
            "tools",
            "checks",
        ),
    )
    require_utc(create["recorded_at_utc"], "integrity_manifest.create.recorded_at_utc")
    _validate_integrity_tools(create["tools"], "integrity_manifest.create.tools")
    _validate_integrity_checks(
        create["checks"],
        "integrity_manifest.create.checks",
        candidate_sha,
        candidate_tree,
    )

    verify = record["verify"]
    if verify is None:
        if require_verify:
            fail("Integrity manifest has no post-review verify record")
        return record
    verify = require_exact_keys(
        verify,
        "integrity_manifest.verify",
        required=(
            "recorded_at_utc",
            "pre_review_manifest_sha256",
            "tools",
            "checks",
        ),
    )
    require_utc(verify["recorded_at_utc"], "integrity_manifest.verify.recorded_at_utc")
    require_sha256(
        verify["pre_review_manifest_sha256"],
        "integrity_manifest.verify.pre_review_manifest_sha256",
    )
    _validate_integrity_tools(verify["tools"], "integrity_manifest.verify.tools")
    _validate_integrity_checks(
        verify["checks"],
        "integrity_manifest.verify.checks",
        candidate_sha,
        candidate_tree,
    )
    if verify["tools"] != create["tools"]:
        fail("Integrity helper path/hash bindings changed between create and verify")
    if parse_utc(create["recorded_at_utc"]) > parse_utc(verify["recorded_at_utc"]):
        fail("Integrity manifest create timestamp is later than verify timestamp")
    reconstructed_pre_record = dict(record)
    reconstructed_pre_record["verify"] = None
    reconstructed_pre_hash = _sha256_bytes(_canonical_json_bytes(reconstructed_pre_record))
    if reconstructed_pre_hash != verify["pre_review_manifest_sha256"]:
        fail(
            "Integrity manifest create record does not reconstruct to the bound "
            "pre-review SHA-256"
        )
    return record


def _validate_integrity_tools(value: Any, field: str) -> None:
    value = require_exact_keys(
        value, field, required=("snapshot_helper", "protocol_helper")
    )
    _validate_tool_binding(
        value["snapshot_helper"],
        f"{field}.snapshot_helper",
        SNAPSHOT_HELPER_RELATIVE_PATH,
    )
    _validate_tool_binding(
        value["protocol_helper"],
        f"{field}.protocol_helper",
        PROTOCOL_HELPER_RELATIVE_PATH,
    )


def _validate_integrity_checks(
    value: Any, field: str, candidate_sha: str, candidate_tree: str
) -> None:
    value = require_exact_keys(
        value,
        field,
        required=(
            "head_sha",
            "tree_sha",
            "detached_head",
            "workbench_absent",
            "tracked_diff",
            "index_diff",
            "status",
        ),
    )
    if value["head_sha"] != candidate_sha or value["tree_sha"] != candidate_tree:
        fail(f"{field} does not match the candidate SHA/tree")
    if value["detached_head"] is not True or value["workbench_absent"] is not True:
        fail(f"{field} detached_head and workbench_absent must be true")
    for key, expected_command in (
        ("tracked_diff", "git diff --quiet --exit-code"),
        ("index_diff", "git diff --cached --quiet --exit-code"),
    ):
        check = require_exact_keys(
            value[key], f"{field}.{key}", required=("command", "exit_code")
        )
        exit_code = require_json_integer(
            check["exit_code"], f"{field}.{key}.exit_code"
        )
        if check["command"] != expected_command or exit_code != 0:
            fail(f"{field}.{key} must bind the canonical command with exit_code 0")
    status = require_exact_keys(
        value["status"],
        f"{field}.status",
        required=("command", "raw_output", "raw_output_sha256"),
    )
    if status["command"] != "git status --porcelain=v1 --untracked-files=all --ignored=matching":
        fail(f"{field}.status.command is not canonical")
    if status["raw_output"] != "":
        fail(f"{field}.status.raw_output must be empty")
    if status["raw_output_sha256"] != _sha256_bytes(b""):
        fail(f"{field}.status.raw_output_sha256 must hash the empty byte string")


def _verify_integrity_manifest_unlocked(
    manifest_input: str,
    pre_review_sha256: str,
    candidate_sha: str,
    candidate_tree: str,
    snapshot_input: str,
    snapshot_helper_path_input: str,
    snapshot_helper_sha256: str,
    protocol_helper_path_input: str,
    protocol_helper_sha256: str,
) -> str:
    manifest_path = require_absolute_path(manifest_input, "manifest")
    snapshot_path = require_absolute_path(snapshot_input, "snapshot_path")
    manifest_path, snapshot_path = _manifest_path_checks(manifest_path, snapshot_path)
    expected_pre_hash = require_sha256(pre_review_sha256, "pre_review_manifest_sha256")
    candidate_sha = require_git_sha(candidate_sha, "candidate_sha")
    candidate_tree = require_git_sha(candidate_tree, "candidate_tree")

    record, raw = _load_json(manifest_path)
    actual_pre_hash = _sha256_bytes(raw)
    if actual_pre_hash != expected_pre_hash:
        fail(
            "Pre-review integrity manifest SHA-256 mismatch: "
            f"expected {expected_pre_hash}, got {actual_pre_hash}"
        )
    record = _validate_integrity_record_shape(record, require_verify=False)
    if record["verify"] is not None:
        fail("Integrity manifest already has a verify record")
    if record["candidate_sha"] != candidate_sha:
        fail("Integrity manifest candidate SHA does not match the verified snapshot")
    if record["candidate_tree"] != candidate_tree:
        fail("Integrity manifest candidate tree does not match the verified snapshot")
    if record["snapshot_path"] != str(snapshot_path):
        fail("Integrity manifest snapshot path does not match the verified snapshot")
    if record["evidence_run_path"] != str(manifest_path.parent):
        fail("Integrity manifest evidence_run_path does not match its actual run directory")
    if record["checkpoint"] != manifest_path.parent.parent.name:
        fail("Integrity manifest checkpoint does not match its actual run directory")
    _evidence_context_from_run_path(
        manifest_path.parent, record["checkpoint"], record["run_id"]
    )

    current_tools = _bind_integrity_tools(
        snapshot_path,
        snapshot_helper_path_input,
        snapshot_helper_sha256,
        protocol_helper_path_input,
        protocol_helper_sha256,
    )
    if current_tools != record["create"]["tools"]:
        fail("Integrity helper path/hash bindings changed since snapshot creation")

    updated = dict(record)
    updated["verify"] = {
        "recorded_at_utc": utc_now(),
        "pre_review_manifest_sha256": expected_pre_hash,
        "tools": current_tools,
        "checks": _integrity_checks(snapshot_path, candidate_sha, candidate_tree),
    }
    return _atomic_json_write(
        manifest_path,
        updated,
        create=False,
        expected_existing_sha256=expected_pre_hash,
    )


def verify_integrity_manifest(
    manifest_input: str,
    pre_review_sha256: str,
    candidate_sha: str,
    candidate_tree: str,
    snapshot_input: str,
    snapshot_helper_path_input: str,
    snapshot_helper_sha256: str,
    protocol_helper_path_input: str,
    protocol_helper_sha256: str,
) -> str:
    manifest_path = require_absolute_path(manifest_input, "manifest")
    if not manifest_path.parent.is_dir():
        fail(f"Manifest parent does not exist: {manifest_path.parent}")
    with _exclusive_manifest_verify_lock(manifest_path):
        return _verify_integrity_manifest_unlocked(
            manifest_input,
            pre_review_sha256,
            candidate_sha,
            candidate_tree,
            snapshot_input,
            snapshot_helper_path_input,
            snapshot_helper_sha256,
            protocol_helper_path_input,
            protocol_helper_sha256,
        )


def _validate_hash_or_na(
    value: Any, field: str, *, require_path: bool, support_root: Path
) -> None:
    base_required = ("status",)
    if not isinstance(value, dict) or "status" not in value:
        fail(f"{field} must be a HASHED or N/A object")
    if value["status"] == "N/A":
        value = require_exact_keys(
            value, field, required=(*base_required, "reason")
        )
        require_string(value["reason"], f"{field}.reason")
        return
    if value["status"] != "HASHED":
        fail(f"{field}.status must be HASHED or N/A")
    required = ["status", "name", "sha256"]
    if require_path:
        required.append("path")
    value = require_exact_keys(value, field, required=required)
    require_string(value["name"], f"{field}.name")
    require_sha256(value["sha256"], f"{field}.sha256")
    if require_path:
        path = require_absolute_path(value["path"], f"{field}.path")
        path = _require_run_support_path(path, support_root, f"{field}.path")
        if not path.is_file():
            fail(f"{field}.path does not exist: {path}")
        actual = sha256_file(path)
        if actual != value["sha256"]:
            fail(f"{field}.sha256 mismatch: expected {value['sha256']}, got {actual}")


def _validate_inputs(value: Any, support_root: Path) -> None:
    field = "inputs"
    if not isinstance(value, dict) or "status" not in value:
        fail("inputs must be a HASHED or N/A object")
    if value["status"] == "N/A":
        value = require_exact_keys(value, field, required=("status", "reason"))
        require_string(value["reason"], "inputs.reason")
        return
    if value["status"] != "HASHED":
        fail("inputs.status must be HASHED or N/A")
    value = require_exact_keys(value, field, required=("status", "items"))
    items = value["items"]
    if not isinstance(items, list) or not items:
        fail("inputs.items must be a non-empty array")
    names: set[str] = set()
    paths: set[str] = set()
    for index, item in enumerate(items):
        item_field = f"inputs.items[{index}]"
        item = require_exact_keys(
            item, item_field, required=("name", "path", "sha256")
        )
        name = require_string(item["name"], f"{item_field}.name")
        path = require_absolute_path(item["path"], f"{item_field}.path")
        path = _require_run_support_path(path, support_root, f"{item_field}.path")
        expected = require_sha256(item["sha256"], f"{item_field}.sha256")
        if name in names:
            fail(f"Duplicate input name: {name}")
        if str(path) in paths:
            fail(f"Duplicate input path: {path}")
        names.add(name)
        paths.add(str(path))
        if not path.is_file():
            fail(f"Input file does not exist: {path}")
        actual = sha256_file(path)
        if actual != expected:
            fail(f"{item_field}.sha256 mismatch: expected {expected}, got {actual}")


def _require_run_support_path(
    path: Path, support_root: Path, field: str
) -> Path:
    if path.is_symlink():
        fail(f"{field} may not be a symlink: {path}")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        fail(f"Cannot resolve {field} {path}: {exc}")
    if resolved != path:
        fail(f"{field} must be canonical and traverse no symlink: {path} -> {resolved}")
    if not _is_within(resolved, support_root) or resolved == support_root:
        fail(f"{field} must live under this Critic run's support root {support_root}")
    if not resolved.is_file():
        fail(f"{field} must be a regular file: {resolved}")
    return resolved


def _validate_commands(value: Any, support_root: Path) -> None:
    if not isinstance(value, list) or not value:
        fail("commands must be a non-empty array")
    for index, command in enumerate(value):
        field = f"commands[{index}]"
        command = require_exact_keys(
            command,
            field,
            required=COMMAND_REQUIRED_FIELDS,
        )
        require_string(command["command"], f"{field}.command")
        if isinstance(command["exit_code"], bool) or not isinstance(
            command["exit_code"], int
        ):
            fail(f"{field}.exit_code must be an integer")
        for stream in ("stdout", "stderr"):
            path = require_absolute_path(
                command[f"{stream}_path"], f"{field}.{stream}_path"
            )
            path = _require_run_support_path(
                path, support_root, f"{field}.{stream}_path"
            )
            expected = require_sha256(
                command[f"{stream}_sha256"], f"{field}.{stream}_sha256"
            )
            if not path.is_file():
                fail(f"{field}.{stream}_path does not exist: {path}")
            actual = sha256_file(path)
            if actual != expected:
                fail(
                    f"{field}.{stream}_sha256 mismatch: "
                    f"expected {expected}, got {actual}"
                )


def _validate_evidence(value: Any, support_root: Path) -> None:
    if not isinstance(value, list) or not value:
        fail("evidence must be a non-empty array")
    for index, item in enumerate(value):
        field = f"evidence[{index}]"
        if not isinstance(item, dict):
            fail(f"{field} must be an object")
        item = require_exact_keys(
            item, field, required=EVIDENCE_REQUIRED_FIELDS
        )
        require_string(item["description"], f"{field}.description")
        path = require_absolute_path(item["path"], f"{field}.path")
        path = _require_run_support_path(path, support_root, f"{field}.path")
        expected = require_sha256(item["sha256"], f"{field}.sha256")
        if not path.is_file():
            fail(f"Evidence file does not exist: {path}")
        actual = sha256_file(path)
        if actual != expected:
            fail(f"{field}.sha256 mismatch: expected {expected}, got {actual}")


def _validate_plan(
    value: Any, *, repo_root: Path, candidate_sha: str
) -> None:
    value = require_exact_keys(
        value, "plan", required=PLAN_REQUIRED_FIELDS
    )
    filename = require_string(value["filename"], "plan.filename")
    if not REPO_RELATIVE_MARKDOWN_RE.fullmatch(filename):
        fail("plan.filename must be a safe repo-relative Markdown path")
    require_string(value["version"], "plan.version")
    expected_hash = require_sha256(value["sha256"], "plan.sha256")
    require_string(value["bar_citation"], "plan.bar_citation")
    bar_excerpt = require_string(value["bar_excerpt"], "plan.bar_excerpt")
    committed_plan = _git_bytes(repo_root, ["show", f"{candidate_sha}:{filename}"])
    actual_hash = _sha256_bytes(committed_plan)
    if actual_hash != expected_hash:
        fail(f"Committed plan SHA-256 mismatch: expected {expected_hash}, got {actual_hash}")
    try:
        plan_text = committed_plan.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"Committed plan is not valid UTF-8: {filename}: {exc}")
    if bar_excerpt not in plan_text:
        fail("plan.bar_excerpt does not occur verbatim in the committed plan blob")


def _cp2_require_repo_path(value: Any, field: str) -> str:
    path = require_string(value, field)
    if not CP2_SAFE_REPO_PATH_RE.fullmatch(path):
        fail(f"{field} must be a safe repository-relative POSIX path")
    return path


def _cp2_decimal(value: Any, field: str, *, canonical: bool = True) -> Decimal:
    if not isinstance(value, str) or not CP2_DECIMAL_RE.fullmatch(value):
        fail(f"{field} must be a finite plain base-10 decimal string")
    try:
        parsed = Decimal(value)
    except InvalidOperation as exc:
        fail(f"{field} is not a valid Decimal: {exc}")
    if not parsed.is_finite():
        fail(f"{field} must be finite")
    normalized = _cp2_decimal_string(parsed)
    if canonical and value != normalized:
        fail(f"{field} is not canonical; expected {normalized!r}, got {value!r}")
    return parsed


def _cp2_decimal_string(value: Decimal) -> str:
    if not value.is_finite():
        fail("Cannot serialize a non-finite Decimal")
    if value == 0:
        return "0"
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    if rendered == "-0":
        return "0"
    return rendered


def _cp2_precision(values: Iterable[str], *, term_count: int = 1) -> int:
    """Conservative precision that makes all finite-decimal sums exact."""

    maximum_integer_digits = 1
    maximum_fractional_digits = 0
    for value in values:
        unsigned = value[1:] if value.startswith("-") else value
        integer, separator, fraction = unsigned.partition(".")
        maximum_integer_digits = max(maximum_integer_digits, len(integer))
        if separator:
            maximum_fractional_digits = max(
                maximum_fractional_digits, len(fraction)
            )
    carry_digits = len(str(max(1, term_count)))
    # Nine fixed taus have at most three fractional digits.  The margin covers
    # subtraction, multiplication by 1000, and a final carry without rounding.
    return (
        maximum_integer_digits
        + maximum_fractional_digits
        + carry_digits
        + 16
    )


def _cp2_csv_bytes(header: Sequence[str], rows: Sequence[Mapping[str, str]]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(header)
    for row in rows:
        writer.writerow([row[name] for name in header])
    return output.getvalue().encode("utf-8")


def _cp2_parse_csv(
    raw: bytes, *, anonymous: bool, field: str
) -> list[dict[str, str]]:
    if raw.startswith(b"\xef\xbb\xbf"):
        fail(f"{field} may not contain a UTF-8 BOM")
    if b"\r" in raw or not raw.endswith(b"\n"):
        fail(f"{field} must use canonical LF line endings and end in LF")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"{field} is not UTF-8: {exc}")
    try:
        parsed_rows = list(csv.reader(io.StringIO(text, newline=""), strict=True))
    except csv.Error as exc:
        fail(f"{field} is not valid canonical CSV: {exc}")
    expected_header = CP2_ANONYMOUS_HEADER if anonymous else CP2_SOURCE_HEADER
    if not parsed_rows or tuple(parsed_rows[0]) != expected_header:
        fail(f"{field} header must be exactly {','.join(expected_header)}")
    rows: list[dict[str, str]] = []
    for index, values in enumerate(parsed_rows[1:], start=2):
        row_field = f"{field}:row-{index}"
        if len(values) != len(expected_header):
            fail(f"{row_field} has {len(values)} fields; expected {len(expected_header)}")
        row = dict(zip(expected_header, values, strict=True))
        if anonymous and row["label"] not in CP2_LABELS:
            fail(f"{row_field}.label must be one of A/B/C/D")
        fold_text = row["fold_id"]
        if not fold_text.isdigit() or str(int(fold_text)) != fold_text:
            fail(f"{row_field}.fold_id must be a canonical integer")
        fold = int(fold_text)
        if fold not in CP2_FOLDS:
            fail(f"{row_field}.fold_id must be in 1..5")
        if not CP2_ROW_ID_RE.fullmatch(row["row_id"]):
            fail(
                f"{row_field}.row_id must be an opaque identifier matching "
                f"{CP2_ROW_ID_RE.pattern}"
            )
        for name in ("y", *(name for name, _ in CP2_QUANTILES)):
            _cp2_decimal(row[name], f"{row_field}.{name}")
        rows.append(row)
    if not rows:
        fail(f"{field} must contain data rows")
    label_index = {label: index for index, label in enumerate(CP2_LABELS)}
    if anonymous:
        sort_key = lambda row: (  # noqa: E731 - compact canonical-key definition.
            int(row["fold_id"]),
            row["row_id"].encode("utf-8"),
            label_index[row["label"]],
        )
    else:
        sort_key = lambda row: (  # noqa: E731
            int(row["fold_id"]),
            row["row_id"].encode("utf-8"),
        )
    if rows != sorted(rows, key=sort_key):
        fail(
            f"{field} rows are not in the canonical "
            "(fold_id numeric, row_id UTF-8 bytes, label A-D) order"
        )
    seen: set[tuple[str, ...]] = set()
    for row in rows:
        key = (
            *((row["label"],) if anonymous else ()),
            row["fold_id"],
            row["row_id"],
        )
        if key in seen:
            fail(f"{field} contains a duplicate row key: {key}")
        seen.add(key)
    canonical_bytes = _cp2_csv_bytes(expected_header, rows)
    if canonical_bytes != raw:
        fail(f"{field} is semantically valid but not byte-canonical")
    _cp2_validate_row_universe(rows, anonymous=anonymous, field=field)
    return rows


def _cp2_validate_row_universe(
    rows: Sequence[Mapping[str, str]], *, anonymous: bool, field: str
) -> None:
    if not anonymous:
        folds = {int(row["fold_id"]) for row in rows}
        if folds != set(CP2_FOLDS):
            fail(f"{field} must contain non-empty rows in all five folds")
        return
    by_key: dict[tuple[str, str], list[Mapping[str, str]]] = {}
    for row in rows:
        by_key.setdefault((row["fold_id"], row["row_id"]), []).append(row)
    for key, matched in by_key.items():
        labels = tuple(row["label"] for row in matched)
        if labels != CP2_LABELS:
            fail(f"{field} row key {key} does not contain exactly labels A/B/C/D")
        if len({row["y"] for row in matched}) != 1:
            fail(f"{field} row key {key} has differing target y across labels")
    for fold in CP2_FOLDS:
        for label in CP2_LABELS:
            if not any(
                int(row["fold_id"]) == fold and row["label"] == label for row in rows
            ):
                fail(f"{field} is missing fold {fold}, label {label}")


def _cp2_match_source_rows(
    rows_by_role: Mapping[str, Sequence[Mapping[str, str]]]
) -> None:
    reference_role = CP2_SEMANTIC_ROLES[0]
    reference = {
        (row["fold_id"], row["row_id"]): row["y"]
        for row in rows_by_role[reference_role]
    }
    for role in CP2_SEMANTIC_ROLES[1:]:
        current = {
            (row["fold_id"], row["row_id"]): row["y"]
            for row in rows_by_role[role]
        }
        if set(current) != set(reference):
            fail(f"Source catalog {role} does not have the matched row universe")
        for key in reference:
            if Decimal(current[key]) != Decimal(reference[key]):
                fail(f"Source catalog {role} has a different y for matched row {key}")


def _cp2_sha_stream(seed: bytes) -> Iterable[int]:
    counter = 0
    while True:
        block = hashlib.sha256(
            CP2_PERMUTATION_DOMAIN + seed + counter.to_bytes(8, "big")
        ).digest()
        counter += 1
        for offset in range(0, len(block), 8):
            yield int.from_bytes(block[offset : offset + 8], "big")


def cp2_permutation(seed: bytes) -> tuple[str, ...]:
    """Return semantic roles assigned to A/B/C/D using unbiased Fisher-Yates."""

    if len(seed) != 32:
        fail("CP-2 blind seed must be exactly 256 bits")
    values = list(CP2_SEMANTIC_ROLES)
    words = iter(_cp2_sha_stream(seed))
    two64 = 1 << 64
    for index in range(len(values) - 1, 0, -1):
        modulus = index + 1
        limit = two64 - (two64 % modulus)
        word = next(words)
        while word >= limit:
            word = next(words)
        swap_index = word % modulus
        values[index], values[swap_index] = values[swap_index], values[index]
    return tuple(values)


def _cp2_metrics(
    rows: Sequence[Mapping[str, str]], *, identity_field: str
) -> list[dict[str, Any]]:
    identities = CP2_LABELS if identity_field == "label" else CP2_SEMANTIC_ROLES
    output: list[dict[str, Any]] = []
    numeric_values = [
        row[name]
        for row in rows
        for name in ("y", *(name for name, _ in CP2_QUANTILES))
    ]
    with localcontext() as context:
        context.prec = _cp2_precision(
            numeric_values, term_count=max(1, len(rows) * len(CP2_QUANTILES))
        )
        context.Emax = max(context.Emax, context.prec * 2)
        context.Emin = min(context.Emin, -context.prec * 2)
        for identity in identities:
            selected = [row for row in rows if row[identity_field] == identity]
            if not selected:
                fail(f"Missing rows for {identity_field}={identity}")
            total_loss = Decimal(0)
            coverage_hits = 0
            folds: list[dict[str, Any]] = []
            for fold in CP2_FOLDS:
                fold_rows = [row for row in selected if int(row["fold_id"]) == fold]
                if not fold_rows:
                    fail(f"Missing fold {fold} for {identity_field}={identity}")
                fold_loss = Decimal(0)
                for row in fold_rows:
                    y = Decimal(row["y"])
                    for name, tau in CP2_QUANTILES:
                        delta = y - Decimal(row[name])
                        fold_loss += max(tau * delta, (tau - Decimal(1)) * delta)
                    if Decimal(row["q10"]) <= y <= Decimal(row["q90"]):
                        coverage_hits += 1
                total_loss += fold_loss
                folds.append(
                    {
                        "fold_id": fold,
                        "loss_sum": _cp2_decimal_string(fold_loss),
                        "loss_denominator": 9 * len(fold_rows),
                        "row_count": len(fold_rows),
                    }
                )
            metric: dict[str, Any] = {
                identity_field: identity,
                "loss_sum": _cp2_decimal_string(total_loss),
                "loss_denominator": 9 * len(selected),
                "coverage_hits": coverage_hits,
                "coverage_total": len(selected),
                "folds": folds,
            }
            output.append(metric)
    return output


def _cp2_validate_metric_entries(
    value: Any, *, identity_field: str, field: str
) -> list[Mapping[str, Any]]:
    identities = CP2_LABELS if identity_field == "label" else CP2_SEMANTIC_ROLES
    if not isinstance(value, list) or len(value) != 4:
        fail(f"{field} must contain exactly four metric entries")
    validated: list[Mapping[str, Any]] = []
    for index, item in enumerate(value):
        item_field = f"{field}[{index}]"
        item = require_exact_keys(
            item,
            item_field,
            required=(
                identity_field,
                "loss_sum",
                "loss_denominator",
                "coverage_hits",
                "coverage_total",
                "folds",
            ),
        )
        if item[identity_field] != identities[index]:
            fail(f"{item_field}.{identity_field} must be {identities[index]}")
        _cp2_decimal(item["loss_sum"], f"{item_field}.loss_sum")
        for name in ("loss_denominator", "coverage_hits", "coverage_total"):
            require_json_integer(item[name], f"{item_field}.{name}")
        if item["coverage_total"] <= 0:
            fail(f"{item_field}.coverage_total must be positive")
        if item["loss_denominator"] != 9 * item["coverage_total"]:
            fail(f"{item_field}.loss_denominator must equal 9*coverage_total")
        if not 0 <= item["coverage_hits"] <= item["coverage_total"]:
            fail(f"{item_field}.coverage_hits is outside 0..coverage_total")
        folds = item["folds"]
        if not isinstance(folds, list) or len(folds) != 5:
            fail(f"{item_field}.folds must contain exactly five entries")
        total_rows = 0
        fold_loss_values: list[str] = []
        for fold_index, fold in enumerate(folds):
            fold_field = f"{item_field}.folds[{fold_index}]"
            fold = require_exact_keys(
                fold,
                fold_field,
                required=("fold_id", "loss_sum", "loss_denominator", "row_count"),
            )
            fold_id = require_json_integer(fold["fold_id"], f"{fold_field}.fold_id")
            if fold_id != CP2_FOLDS[fold_index]:
                fail(f"{fold_field}.fold_id must be {CP2_FOLDS[fold_index]}")
            row_count = require_json_integer(
                fold["row_count"], f"{fold_field}.row_count"
            )
            if row_count <= 0:
                fail(f"{fold_field}.row_count must be a positive integer")
            loss_denominator = require_json_integer(
                fold["loss_denominator"], f"{fold_field}.loss_denominator"
            )
            if loss_denominator != 9 * row_count:
                fail(f"{fold_field}.loss_denominator must equal 9*row_count")
            total_rows += row_count
            _cp2_decimal(fold["loss_sum"], f"{fold_field}.loss_sum")
            fold_loss_values.append(fold["loss_sum"])
        if total_rows != item["coverage_total"]:
            fail(f"{item_field} fold row counts do not equal coverage_total")
        with localcontext() as context:
            context.prec = _cp2_precision(fold_loss_values, term_count=5)
            context.Emax = max(context.Emax, context.prec * 2)
            context.Emin = min(context.Emin, -context.prec * 2)
            total_fold_loss = sum((Decimal(value) for value in fold_loss_values), Decimal(0))
        if total_fold_loss != Decimal(item["loss_sum"]):
            fail(f"{item_field} fold loss sums do not equal pooled loss_sum")
        validated.append(item)
    denominators = {
        (item["loss_denominator"], item["coverage_total"]) for item in validated
    }
    if len(denominators) != 1:
        fail(f"{field} catalogs do not use the same matched-row denominator")
    for fold_index in range(5):
        fold_denominators = {
            item["folds"][fold_index]["loss_denominator"] for item in validated
        }
        if len(fold_denominators) != 1:
            fail(f"{field} fold {fold_index + 1} denominators differ by catalog")
    return validated


def _cp2_metric_entries_equal(left: Any, right: Any) -> bool:
    return _canonical_json_bytes({"metrics": left}) == _canonical_json_bytes(
        {"metrics": right}
    )


def _cp2_load_json_bytes(raw: bytes, field: str) -> Mapping[str, Any]:
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"Invalid JSON in {field}: {exc}")
    if not isinstance(value, dict):
        fail(f"{field} JSON root must be an object")
    if _canonical_json_bytes(value) != raw:
        fail(f"{field} JSON must use the canonical sorted/indented serialization")
    return value


def _cp2_validate_source_manifest(
    value: Any,
    *,
    source_manifest_sha256: str,
    selection_declaration_sha256: str,
) -> Mapping[str, Any]:
    value = require_exact_keys(
        value,
        "source_manifest",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "catalogs",
            "csv_contract",
            "data_snapshot",
            "rule",
            "selection_declaration",
        ),
    )
    if value["record_type"] != "cp2_blind_source_manifest":
        fail("source_manifest.record_type must be cp2_blind_source_manifest")
    if value["schema_version"] != CP2_BLIND_SCHEMA_VERSION:
        fail("source_manifest.schema_version is unsupported")
    if value["checkpoint"] != "CP-2":
        fail("source_manifest.checkpoint must be CP-2")
    catalogs = value["catalogs"]
    if not isinstance(catalogs, list) or len(catalogs) != 4:
        fail("source_manifest.catalogs must contain exactly four entries")
    for index, catalog in enumerate(catalogs):
        field = f"source_manifest.catalogs[{index}]"
        catalog = require_exact_keys(
            catalog,
            field,
            required=("role", "prediction_path", "sha256", "feature_count"),
        )
        role = CP2_SEMANTIC_ROLES[index]
        if catalog["role"] != role:
            fail(f"{field}.role must be {role}")
        _cp2_require_repo_path(catalog["prediction_path"], f"{field}.prediction_path")
        require_sha256(catalog["sha256"], f"{field}.sha256")
        require_json_integer(catalog["feature_count"], f"{field}.feature_count")
        if catalog["feature_count"] != CP2_FEATURE_COUNTS[role]:
            fail(
                f"{field}.feature_count must be the frozen value "
                f"{CP2_FEATURE_COUNTS[role]}"
            )
    if len({catalog["prediction_path"] for catalog in catalogs}) != 4:
        fail("source_manifest catalog prediction paths must be distinct")
    csv_contract = require_exact_keys(
        value["csv_contract"],
        "source_manifest.csv_contract",
        required=("header", "folds", "quantiles", "canonical_sort"),
    )
    if csv_contract["header"] != list(CP2_SOURCE_HEADER):
        fail("source_manifest.csv_contract.header is not canonical")
    if not _json_exact_equal(csv_contract["folds"], list(CP2_FOLDS)):
        fail("source_manifest.csv_contract.folds must be [1,2,3,4,5]")
    if csv_contract["quantiles"] != [name for name, _ in CP2_QUANTILES]:
        fail("source_manifest.csv_contract.quantiles is not canonical")
    if csv_contract["canonical_sort"] != ["fold_id_numeric", "row_id_utf8_bytes"]:
        fail("source_manifest.csv_contract.canonical_sort is not canonical")
    snapshot = require_exact_keys(
        value["data_snapshot"],
        "source_manifest.data_snapshot",
        required=("snapshot_id", "cutoff_utc", "sha256"),
    )
    require_string(snapshot["snapshot_id"], "source_manifest.data_snapshot.snapshot_id")
    require_utc(snapshot["cutoff_utc"], "source_manifest.data_snapshot.cutoff_utc")
    require_sha256(snapshot["sha256"], "source_manifest.data_snapshot.sha256")
    rule = require_exact_keys(
        value["rule"],
        "source_manifest.rule",
        required=(
            "version",
            "plan_filename",
            "plan_sha256",
            "bar_citation",
            "bar_excerpt",
            "canonicalization_version",
        ),
    )
    if rule["version"] != CP2_RULE_VERSION:
        fail(f"source_manifest.rule.version must be {CP2_RULE_VERSION}")
    plan_filename = _cp2_require_repo_path(
        rule["plan_filename"], "source_manifest.rule.plan_filename"
    )
    if not plan_filename.endswith(".md"):
        fail("source_manifest.rule.plan_filename must be Markdown")
    require_sha256(rule["plan_sha256"], "source_manifest.rule.plan_sha256")
    require_string(rule["bar_citation"], "source_manifest.rule.bar_citation")
    require_string(rule["bar_excerpt"], "source_manifest.rule.bar_excerpt")
    if rule["canonicalization_version"] != CP2_CANONICALIZATION_VERSION:
        fail(
            "source_manifest.rule.canonicalization_version must be "
            f"{CP2_CANONICALIZATION_VERSION}"
        )
    declaration_binding = require_exact_keys(
        value["selection_declaration"],
        "source_manifest.selection_declaration",
        required=CP2_REPO_BLOB_BINDING_REQUIRED_FIELDS,
    )
    if (
        declaration_binding["repo_relative_path"]
        != CP2_SELECTION_DECLARATION_RELATIVE_PATH
    ):
        fail(
            "source_manifest.selection_declaration.repo_relative_path must be "
            f"{CP2_SELECTION_DECLARATION_RELATIVE_PATH}"
        )
    bound_declaration_hash = require_sha256(
        declaration_binding["sha256"], "source_manifest.selection_declaration.sha256"
    )
    if bound_declaration_hash != selection_declaration_sha256:
        fail("source_manifest selection-declaration hash does not match the blob")
    require_sha256(source_manifest_sha256, "source_manifest_sha256")
    return value


def _cp2_validate_selection_declaration(value: Any) -> Mapping[str, Any]:
    value = require_exact_keys(
        value,
        "selection_declaration",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "source_manifest_repo_relative_path",
            "rule_version",
            "selected_role",
            "metrics_by_role",
            "recorded_at_utc",
        ),
    )
    if value["record_type"] != "cp2_blind_selection_declaration":
        fail(
            "selection_declaration.record_type must be "
            "cp2_blind_selection_declaration"
        )
    if value["schema_version"] != CP2_BLIND_SCHEMA_VERSION:
        fail("selection_declaration.schema_version is unsupported")
    if value["checkpoint"] != "CP-2":
        fail("selection_declaration.checkpoint must be CP-2")
    if (
        value["source_manifest_repo_relative_path"]
        != CP2_SOURCE_MANIFEST_RELATIVE_PATH
    ):
        fail(
            "selection_declaration.source_manifest_repo_relative_path must be "
            f"{CP2_SOURCE_MANIFEST_RELATIVE_PATH}"
        )
    if value["rule_version"] != CP2_RULE_VERSION:
        fail(f"selection_declaration.rule_version must be {CP2_RULE_VERSION}")
    if value["selected_role"] not in CP2_SEMANTIC_ROLES:
        fail("selection_declaration.selected_role is not a canonical catalog role")
    _cp2_validate_metric_entries(
        value["metrics_by_role"],
        identity_field="role",
        field="selection_declaration.metrics_by_role",
    )
    require_utc(value["recorded_at_utc"], "selection_declaration.recorded_at_utc")
    return value


def _cp2_committed_inputs(
    repo_root: Path, candidate_sha: str
) -> tuple[
    Mapping[str, Any],
    bytes,
    Mapping[str, Any],
    bytes,
    dict[str, bytes],
    dict[str, list[dict[str, str]]],
]:
    source_raw = _git_bytes(
        repo_root, ["show", f"{candidate_sha}:{CP2_SOURCE_MANIFEST_RELATIVE_PATH}"]
    )
    selection_raw = _git_bytes(
        repo_root,
        ["show", f"{candidate_sha}:{CP2_SELECTION_DECLARATION_RELATIVE_PATH}"],
    )
    source = _cp2_load_json_bytes(source_raw, "committed source manifest")
    selection = _cp2_load_json_bytes(selection_raw, "committed selection declaration")
    source_hash = _sha256_bytes(source_raw)
    selection_hash = _sha256_bytes(selection_raw)
    source = _cp2_validate_source_manifest(
        source,
        source_manifest_sha256=source_hash,
        selection_declaration_sha256=selection_hash,
    )
    selection = _cp2_validate_selection_declaration(selection)
    source_bytes: dict[str, bytes] = {}
    rows_by_role: dict[str, list[dict[str, str]]] = {}
    for catalog in source["catalogs"]:
        role = catalog["role"]
        raw = _git_bytes(repo_root, ["show", f"{candidate_sha}:{catalog['prediction_path']}"])
        actual_hash = _sha256_bytes(raw)
        if actual_hash != catalog["sha256"]:
            fail(
                f"Committed prediction hash mismatch for {role}: "
                f"expected {catalog['sha256']}, got {actual_hash}"
            )
        rows = _cp2_parse_csv(raw, anonymous=False, field=f"source catalog {role}")
        source_bytes[role] = raw
        rows_by_role[role] = rows
    _cp2_match_source_rows(rows_by_role)
    plan = source["rule"]
    plan_raw = _git_bytes(repo_root, ["show", f"{candidate_sha}:{plan['plan_filename']}"])
    if _sha256_bytes(plan_raw) != plan["plan_sha256"]:
        fail("source_manifest.rule.plan_sha256 does not match the committed plan")
    try:
        plan_text = plan_raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        fail(f"CP-2 plan is not UTF-8: {exc}")
    if plan["bar_excerpt"] not in plan_text:
        fail("source_manifest.rule.bar_excerpt is absent from the committed plan")
    schema_raw = _git_bytes(
        repo_root, ["show", f"{candidate_sha}:{CP2_BLIND_SCHEMA_RELATIVE_PATH}"]
    )
    try:
        schema_value = json.loads(schema_raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"Committed CP-2 blind schema is invalid JSON: {exc}")
    if not isinstance(schema_value, dict):
        fail("Committed CP-2 blind schema root must be an object")
    if schema_value.get("$id") != CP2_BLIND_SCHEMA_ID:
        fail("Committed CP-2 blind schema has an unexpected $id")
    if schema_value.get("x-validator") != "scripts/gauntlet_protocol.py@1.0":
        fail("Committed CP-2 blind schema and protocol validator versions disagree")
    return source, source_raw, selection, selection_raw, source_bytes, rows_by_role


def _cp2_run_paths(repo_root: Path, run_id: str) -> tuple[Path, Path]:
    run_id = require_identifier(run_id, "run_id")
    checkpoint_root = repo_root / ".gauntlet" / "evidence" / "CP-2"
    run_root = checkpoint_root / run_id
    support_root = checkpoint_root / "_support" / run_id
    _reject_symlinked_evidence_ancestors(
        repo_root, "CP-2", include_run=run_id, include_support_run=run_id
    )
    for path, field in ((run_root, "run root"), (support_root, "support root")):
        if path.is_symlink() or not path.is_dir():
            fail(f"CP-2 {field} is missing or symlinked: {path}")
        if path.resolve(strict=True) != path:
            fail(f"CP-2 {field} traverses a symlink: {path}")
        _require_mode(path, 0o700, f"CP-2 {field}")
    return run_root, support_root


def _cp2_run_ref(
    repo_root: Path, run_id: str, candidate_sha: str
) -> tuple[str, str]:
    prefix = f"refs/gauntlet-evidence/CP-2/{run_id}/"
    output = _git(
        repo_root,
        ["for-each-ref", "--format=%(refname) %(objectname)", prefix],
    )
    lines = [line for line in output.splitlines() if line]
    if len(lines) != 1:
        fail(f"CP-2 run {run_id} must have exactly one pre-created evidence ref")
    ref, resolved = lines[0].split(" ", 1)
    if not ref.startswith(prefix) or resolved != candidate_sha:
        fail(f"CP-2 run {run_id} evidence ref does not bind the exact candidate")
    piece = ref[len(prefix) :]
    require_identifier(piece, "CP-2 run piece")
    return ref, piece


def _cp2_custody_root(repo_root: Path, blind_review_id: str) -> Path:
    blind_review_id = require_identifier(blind_review_id, "blind_review_id")
    root = (
        repo_root
        / ".gauntlet"
        / "evidence"
        / "CP-2"
        / "_blind-custody"
        / blind_review_id
    )
    return root


def _cp2_binding(path: Path) -> Mapping[str, str]:
    return {"path": str(path), "sha256": sha256_file(path)}


def _cp2_validate_absolute_binding(
    value: Any, field: str, *, ownership_root: Path | None = None
) -> tuple[Path, str]:
    value = require_exact_keys(value, field, required=CP2_HASH_BINDING_REQUIRED_FIELDS)
    path = require_absolute_path(value["path"], f"{field}.path")
    if path.is_symlink() or not path.is_file():
        fail(f"{field}.path is missing or symlinked: {path}")
    if path.resolve(strict=True) != path:
        fail(f"{field}.path is not canonical: {path}")
    if ownership_root is not None and path.parent != ownership_root:
        fail(f"{field}.path must be directly owned by {ownership_root}")
    expected = require_sha256(value["sha256"], f"{field}.sha256")
    actual = sha256_file(path)
    if actual != expected:
        fail(f"{field}.sha256 mismatch: expected {expected}, got {actual}")
    return path, actual


def _cp2_create_attempt(
    path: Path,
    record_type: str,
    blind_review_id: str,
    *,
    previous: str | None = None,
) -> str:
    return _atomic_json_write(
        path,
        {
            "record_type": record_type,
            "schema_version": CP2_BLIND_SCHEMA_VERSION,
            "checkpoint": "CP-2",
            "blind_review_id": blind_review_id,
            "started_at_utc": _timestamp_after(previous),
        },
        create=True,
    )


def _cp2_validate_public_manifest(
    value: Any, *, support_root: Path, blind_review_id: str
) -> Mapping[str, Any]:
    value = require_exact_keys(
        value,
        "public_manifest",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "blind_schema",
            "protocol_tool",
            "anonymous_csv",
            "labels",
            "folds",
            "header",
            "quantiles",
            "canonical_sort",
            "row_count_per_label",
            "blindness_strength",
            "prepared_at_utc",
        ),
    )
    if value["record_type"] != "cp2_blind_public_manifest":
        fail("public_manifest.record_type must be cp2_blind_public_manifest")
    if value["schema_version"] != CP2_BLIND_SCHEMA_VERSION:
        fail("public_manifest.schema_version is unsupported")
    if value["checkpoint"] != "CP-2" or value["blind_review_id"] != blind_review_id:
        fail("public_manifest checkpoint/blind_review_id mismatch")
    candidate = require_exact_keys(
        value["candidate"], "public_manifest.candidate", required=("commit_sha", "tree_sha")
    )
    require_git_sha(candidate["commit_sha"], "public_manifest.candidate.commit_sha")
    require_git_sha(candidate["tree_sha"], "public_manifest.candidate.tree_sha")
    schema = require_exact_keys(
        value["blind_schema"],
        "public_manifest.blind_schema",
        required=CP2_REPO_BLOB_BINDING_REQUIRED_FIELDS,
    )
    if schema["repo_relative_path"] != CP2_BLIND_SCHEMA_RELATIVE_PATH:
        fail("public_manifest.blind_schema.repo_relative_path mismatch")
    require_sha256(schema["sha256"], "public_manifest.blind_schema.sha256")
    tool = require_exact_keys(
        value["protocol_tool"],
        "public_manifest.protocol_tool",
        required=CP2_REPO_BLOB_BINDING_REQUIRED_FIELDS,
    )
    if tool["repo_relative_path"] != PROTOCOL_HELPER_RELATIVE_PATH:
        fail("public_manifest.protocol_tool.repo_relative_path mismatch")
    require_sha256(tool["sha256"], "public_manifest.protocol_tool.sha256")
    csv_path, _ = _cp2_validate_absolute_binding(
        value["anonymous_csv"], "public_manifest.anonymous_csv", ownership_root=support_root
    )
    if csv_path.name != CP2_PUBLIC_INPUT_FILENAME:
        fail(f"public_manifest.anonymous_csv.path must end in {CP2_PUBLIC_INPUT_FILENAME}")
    if value["labels"] != list(CP2_LABELS):
        fail("public_manifest.labels must be [A,B,C,D]")
    if not _json_exact_equal(value["folds"], list(CP2_FOLDS)):
        fail("public_manifest.folds must be [1,2,3,4,5]")
    if value["header"] != list(CP2_ANONYMOUS_HEADER):
        fail("public_manifest.header is not canonical")
    if value["quantiles"] != [name for name, _ in CP2_QUANTILES]:
        fail("public_manifest.quantiles is not canonical")
    if value["canonical_sort"] != [
        "fold_id_numeric",
        "row_id_utf8_bytes",
        "label_A_to_D",
    ]:
        fail("public_manifest.canonical_sort is not canonical")
    row_count_per_label = require_json_integer(
        value["row_count_per_label"], "public_manifest.row_count_per_label"
    )
    if row_count_per_label <= 0:
        fail("public_manifest.row_count_per_label must be a positive integer")
    if value["blindness_strength"] != "COOPERATIVE_PROCEDURAL":
        fail(
            "The bundled protocol has no OS read sandbox and therefore requires "
            "blindness_strength=COOPERATIVE_PROCEDURAL"
        )
    require_utc(value["prepared_at_utc"], "public_manifest.prepared_at_utc")
    return value


def _cp2_validate_commitment(
    value: Any,
    *,
    support_root: Path,
    blind_review_id: str,
    public_manifest_path: Path,
    public_manifest_hash: str,
) -> Mapping[str, Any]:
    value = require_exact_keys(
        value,
        "commitment",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "domain",
            "commitment_sha256",
            "seed_bits",
            "permutation_version",
            "public_manifest",
            "anonymous_csv",
            "blind_schema",
            "recorded_at_utc",
        ),
    )
    if value["record_type"] != "cp2_blind_commitment":
        fail("commitment.record_type must be cp2_blind_commitment")
    if value["schema_version"] != CP2_BLIND_SCHEMA_VERSION:
        fail("commitment.schema_version is unsupported")
    if value["checkpoint"] != "CP-2" or value["blind_review_id"] != blind_review_id:
        fail("commitment checkpoint/blind_review_id mismatch")
    candidate = require_exact_keys(
        value["candidate"], "commitment.candidate", required=("commit_sha", "tree_sha")
    )
    require_git_sha(candidate["commit_sha"], "commitment.candidate.commit_sha")
    require_git_sha(candidate["tree_sha"], "commitment.candidate.tree_sha")
    if value["domain"] != CP2_COMMITMENT_DOMAIN:
        fail("commitment.domain mismatch")
    require_sha256(value["commitment_sha256"], "commitment.commitment_sha256")
    if require_json_integer(value["seed_bits"], "commitment.seed_bits") != 256:
        fail("commitment.seed_bits must be 256")
    if value["permutation_version"] != CP2_PERMUTATION_VERSION:
        fail("commitment.permutation_version mismatch")
    manifest_binding = require_exact_keys(
        value["public_manifest"],
        "commitment.public_manifest",
        required=CP2_HASH_BINDING_REQUIRED_FIELDS,
    )
    if (
        manifest_binding["path"] != str(public_manifest_path)
        or manifest_binding["sha256"] != public_manifest_hash
    ):
        fail("commitment.public_manifest does not bind the current public manifest")
    csv_path, _ = _cp2_validate_absolute_binding(
        value["anonymous_csv"], "commitment.anonymous_csv", ownership_root=support_root
    )
    if csv_path.name != CP2_PUBLIC_INPUT_FILENAME:
        fail("commitment.anonymous_csv has the wrong filename")
    schema = require_exact_keys(
        value["blind_schema"],
        "commitment.blind_schema",
        required=CP2_REPO_BLOB_BINDING_REQUIRED_FIELDS,
    )
    if schema["repo_relative_path"] != CP2_BLIND_SCHEMA_RELATIVE_PATH:
        fail("commitment.blind_schema.repo_relative_path mismatch")
    require_sha256(schema["sha256"], "commitment.blind_schema.sha256")
    require_utc(value["recorded_at_utc"], "commitment.recorded_at_utc")
    return value


def _cp2_public_bundle(
    support_root: Path, blind_review_id: str
) -> tuple[
    Mapping[str, Any],
    Path,
    str,
    Mapping[str, Any],
    Path,
    str,
    list[dict[str, str]],
]:
    manifest_path = support_root / CP2_PUBLIC_MANIFEST_FILENAME
    commitment_path = support_root / CP2_COMMITMENT_FILENAME
    receipt_path = support_root / CP2_PREPARATION_RECEIPT_FILENAME
    manifest, manifest_raw = _load_json(manifest_path)
    manifest_hash = _sha256_bytes(manifest_raw)
    manifest = _cp2_validate_public_manifest(
        manifest, support_root=support_root, blind_review_id=blind_review_id
    )
    commitment, commitment_raw = _load_json(commitment_path)
    commitment_hash = _sha256_bytes(commitment_raw)
    commitment = _cp2_validate_commitment(
        commitment,
        support_root=support_root,
        blind_review_id=blind_review_id,
        public_manifest_path=manifest_path,
        public_manifest_hash=manifest_hash,
    )
    if manifest["candidate"] != commitment["candidate"]:
        fail("Public manifest and commitment candidate identities differ")
    if manifest["blind_schema"] != commitment["blind_schema"]:
        fail("Public manifest and commitment schema bindings differ")
    if manifest["anonymous_csv"] != commitment["anonymous_csv"]:
        fail("Public manifest and commitment anonymous CSV bindings differ")
    receipt, _ = _load_json(receipt_path)
    receipt = require_exact_keys(
        receipt,
        "preparation_receipt",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "public_manifest",
            "commitment",
            "anonymous_csv",
            "custody_record_sha256",
            "recorded_at_utc",
        ),
    )
    if receipt["record_type"] != "cp2_blind_preparation_receipt":
        fail("preparation_receipt.record_type mismatch")
    if receipt["schema_version"] != CP2_BLIND_SCHEMA_VERSION:
        fail("preparation_receipt.schema_version mismatch")
    if receipt["checkpoint"] != "CP-2" or receipt["blind_review_id"] != blind_review_id:
        fail("preparation_receipt identity mismatch")
    if receipt["candidate"] != manifest["candidate"]:
        fail("preparation_receipt candidate mismatch")
    expected_bindings = (
        ("public_manifest", manifest_path, manifest_hash),
        ("commitment", commitment_path, commitment_hash),
        (
            "anonymous_csv",
            Path(manifest["anonymous_csv"]["path"]),
            manifest["anonymous_csv"]["sha256"],
        ),
    )
    for name, path, digest in expected_bindings:
        binding = require_exact_keys(
            receipt[name], f"preparation_receipt.{name}", required=CP2_HASH_BINDING_REQUIRED_FIELDS
        )
        if binding != {"path": str(path), "sha256": digest}:
            fail(f"preparation_receipt.{name} binding mismatch")
    require_sha256(
        receipt["custody_record_sha256"],
        "preparation_receipt.custody_record_sha256",
    )
    receipt_time = require_utc(receipt["recorded_at_utc"], "preparation_receipt.recorded_at_utc")
    if not (
        parse_utc(manifest["prepared_at_utc"])
        < parse_utc(commitment["recorded_at_utc"])
        < parse_utc(receipt_time)
    ):
        fail("Public prepare→commitment→receipt chronology is not strictly ordered")
    csv_path = Path(manifest["anonymous_csv"]["path"])
    csv_raw = _read_single_link_file(csv_path, "anonymous CP-2 CSV")
    rows = _cp2_parse_csv(csv_raw, anonymous=True, field="anonymous CP-2 CSV")
    if len(rows) != 4 * manifest["row_count_per_label"]:
        fail("public_manifest.row_count_per_label does not match the anonymous CSV")
    return (
        manifest,
        manifest_path,
        manifest_hash,
        commitment,
        commitment_path,
        commitment_hash,
        rows,
    )


def cp2_blind_prepare(
    repo_root_input: str,
    candidate_sha: str,
    blind_review_id: str,
    component_run_id: str,
) -> Mapping[str, Any]:
    repo_root = canonical_repo_root(repo_root_input)
    blind_review_id = require_identifier(blind_review_id, "blind_review_id")
    component_run_id = require_identifier(component_run_id, "component_run_id")
    candidate_sha, candidate_tree = _validate_full_commit(repo_root, candidate_sha)
    _, support_root = _cp2_run_paths(repo_root, component_run_id)
    component_ref, component_piece = _cp2_run_ref(
        repo_root, component_run_id, candidate_sha
    )
    preexisting_entries = sorted(path.name for path in support_root.iterdir())
    if preexisting_entries:
        fail(
            "Blind component support root must be completely empty before "
            f"blind-prepare: {preexisting_entries}"
        )
    target_names = (
        CP2_PUBLIC_INPUT_FILENAME,
        CP2_PUBLIC_MANIFEST_FILENAME,
        CP2_COMMITMENT_FILENAME,
        CP2_PREPARATION_RECEIPT_FILENAME,
        CP2_RECOMPUTE_ATTEMPT_FILENAME,
        CP2_METRICS_FILENAME,
    )
    existing_public = [name for name in target_names if (support_root / name).exists()]
    if existing_public:
        fail(f"Blind component support already contains protocol state: {existing_public}")
    custody_root = _cp2_custody_root(repo_root, blind_review_id)
    custody_parent = custody_root.parent
    _ensure_real_directory(custody_parent)
    _require_mode(custody_parent, 0o700, "CP-2 custody parent")
    try:
        custody_root.mkdir(mode=0o700)
    except FileExistsError:
        fail(f"Blind review ID is already spent: {blind_review_id}")
    except OSError as exc:
        fail(f"Cannot allocate blind custody root: {exc}")
    os.chmod(custody_root, 0o700)
    _require_mode(custody_root, 0o700, "CP-2 custody root")

    source, source_raw, selection, selection_raw, sources, rows_by_role = (
        _cp2_committed_inputs(repo_root, candidate_sha)
    )
    schema_raw = _git_bytes(
        repo_root, ["show", f"{candidate_sha}:{CP2_BLIND_SCHEMA_RELATIVE_PATH}"]
    )
    tool_raw = _git_bytes(
        repo_root, ["show", f"{candidate_sha}:{PROTOCOL_HELPER_RELATIVE_PATH}"]
    )
    runtime_tool_hash = _cp2_require_runtime_tool_hash(_sha256_bytes(tool_raw))
    invocation_path = custody_root / CP2_PREPARATION_INVOCATION_FILENAME
    invocation = {
        "record_type": "cp2_blind_preparation_invocation",
        "schema_version": CP2_BLIND_SCHEMA_VERSION,
        "checkpoint": "CP-2",
        "blind_review_id": blind_review_id,
        "candidate": {"commit_sha": candidate_sha, "tree_sha": candidate_tree},
        "argv": [
            "python3",
            PROTOCOL_HELPER_RELATIVE_PATH,
            "blind-prepare",
            "--repo-root",
            str(repo_root),
            "--candidate-sha",
            candidate_sha,
            "--blind-review-id",
            blind_review_id,
            "--component-run-id",
            component_run_id,
        ],
        "identity_inputs": [
            CP2_SOURCE_MANIFEST_RELATIVE_PATH,
            CP2_SELECTION_DECLARATION_RELATIVE_PATH,
        ],
        "runtime_tool_sha256": runtime_tool_hash,
        "recorded_at_utc": _timestamp_after(),
    }
    invocation_hash = _atomic_json_write(invocation_path, invocation, create=True)
    custody_source_manifest = custody_root / CP2_CUSTODY_SOURCE_MANIFEST_FILENAME
    custody_selection = custody_root / CP2_CUSTODY_SELECTION_FILENAME
    _atomic_bytes_create(custody_source_manifest, source_raw)
    _atomic_bytes_create(custody_selection, selection_raw)
    custody_sources: dict[str, Path] = {}
    for role in CP2_SEMANTIC_ROLES:
        path = custody_root / f"source-{role}.csv"
        _atomic_bytes_create(path, sources[role])
        custody_sources[role] = path

    seed = secrets.token_bytes(32)
    permuted_roles = cp2_permutation(seed)
    role_to_label = {
        role: CP2_LABELS[index] for index, role in enumerate(permuted_roles)
    }
    indexed_sources = {
        role: {(row["fold_id"], row["row_id"]): row for row in rows_by_role[role]}
        for role in CP2_SEMANTIC_ROLES
    }
    row_keys = sorted(
        indexed_sources[CP2_SEMANTIC_ROLES[0]],
        key=lambda key: (int(key[0]), key[1].encode("utf-8")),
    )
    anonymous_rows: list[dict[str, str]] = []
    for fold_id, row_id in row_keys:
        for label, role in zip(CP2_LABELS, permuted_roles, strict=True):
            source_row = indexed_sources[role][(fold_id, row_id)]
            anonymous_rows.append(
                {
                    "label": label,
                    **{name: source_row[name] for name in CP2_SOURCE_HEADER},
                }
            )
    anonymous_raw = _cp2_csv_bytes(CP2_ANONYMOUS_HEADER, anonymous_rows)
    _cp2_parse_csv(anonymous_raw, anonymous=True, field="prepared anonymous CP-2 CSV")
    anonymous_path = support_root / CP2_PUBLIC_INPUT_FILENAME
    anonymous_hash = _atomic_bytes_create(anonymous_path, anonymous_raw)
    prepared_at = _timestamp_after()
    schema_binding = {
        "repo_relative_path": CP2_BLIND_SCHEMA_RELATIVE_PATH,
        "sha256": _sha256_bytes(schema_raw),
    }
    public_manifest = {
        "record_type": "cp2_blind_public_manifest",
        "schema_version": CP2_BLIND_SCHEMA_VERSION,
        "checkpoint": "CP-2",
        "blind_review_id": blind_review_id,
        "candidate": {"commit_sha": candidate_sha, "tree_sha": candidate_tree},
        "blind_schema": schema_binding,
        "protocol_tool": {
            "repo_relative_path": PROTOCOL_HELPER_RELATIVE_PATH,
            "sha256": _sha256_bytes(tool_raw),
        },
        "anonymous_csv": {"path": str(anonymous_path), "sha256": anonymous_hash},
        "labels": list(CP2_LABELS),
        "folds": list(CP2_FOLDS),
        "header": list(CP2_ANONYMOUS_HEADER),
        "quantiles": [name for name, _ in CP2_QUANTILES],
        "canonical_sort": [
            "fold_id_numeric",
            "row_id_utf8_bytes",
            "label_A_to_D",
        ],
        "row_count_per_label": len(row_keys),
        "blindness_strength": "COOPERATIVE_PROCEDURAL",
        "prepared_at_utc": prepared_at,
    }
    public_manifest_path = support_root / CP2_PUBLIC_MANIFEST_FILENAME
    public_manifest_hash = _atomic_json_write(
        public_manifest_path, public_manifest, create=True
    )
    preimage = {
        "record_type": "cp2_blind_mapping_preimage",
        "schema_version": CP2_BLIND_SCHEMA_VERSION,
        "checkpoint": "CP-2",
        "blind_review_id": blind_review_id,
        "candidate": {"commit_sha": candidate_sha, "tree_sha": candidate_tree},
        "seed_hex": seed.hex(),
        "permutation_version": CP2_PERMUTATION_VERSION,
        "mapping": [
            {
                "label": label,
                "role": role,
                "feature_count": CP2_FEATURE_COUNTS[role],
                "source_sha256": source["catalogs"][
                    CP2_SEMANTIC_ROLES.index(role)
                ]["sha256"],
            }
            for label, role in zip(CP2_LABELS, permuted_roles, strict=True)
        ],
        "source_manifest_sha256": _sha256_bytes(source_raw),
        "selection_declaration_sha256": _sha256_bytes(selection_raw),
        "blind_schema_sha256": _sha256_bytes(schema_raw),
        "protocol_tool_sha256": _sha256_bytes(tool_raw),
        "preparation_invocation_sha256": invocation_hash,
        "public_manifest_sha256": public_manifest_hash,
        "anonymous_csv_sha256": anonymous_hash,
    }
    preimage_path = custody_root / CP2_MAPPING_PREIMAGE_FILENAME
    preimage_hash = _atomic_json_write(preimage_path, preimage, create=True)
    commitment_digest = _sha256_bytes(
        CP2_COMMITMENT_DOMAIN.encode("ascii")
        + b"\x00"
        + _canonical_json_bytes(preimage)
    )
    commitment_time = _timestamp_after(prepared_at)
    commitment = {
        "record_type": "cp2_blind_commitment",
        "schema_version": CP2_BLIND_SCHEMA_VERSION,
        "checkpoint": "CP-2",
        "blind_review_id": blind_review_id,
        "candidate": {"commit_sha": candidate_sha, "tree_sha": candidate_tree},
        "domain": CP2_COMMITMENT_DOMAIN,
        "commitment_sha256": commitment_digest,
        "seed_bits": 256,
        "permutation_version": CP2_PERMUTATION_VERSION,
        "public_manifest": {
            "path": str(public_manifest_path),
            "sha256": public_manifest_hash,
        },
        "anonymous_csv": {"path": str(anonymous_path), "sha256": anonymous_hash},
        "blind_schema": schema_binding,
        "recorded_at_utc": commitment_time,
    }
    commitment_path = support_root / CP2_COMMITMENT_FILENAME
    commitment_hash = _atomic_json_write(commitment_path, commitment, create=True)
    custody_time = _timestamp_after(commitment_time)
    custody_record = {
        "record_type": "cp2_blind_custody",
        "schema_version": CP2_BLIND_SCHEMA_VERSION,
        "checkpoint": "CP-2",
        "blind_review_id": blind_review_id,
        "candidate": {"commit_sha": candidate_sha, "tree_sha": candidate_tree},
        "component": {
            "run_id": component_run_id,
            "piece": component_piece,
            "evidence_ref": component_ref,
            "support_root": str(support_root),
        },
        "mapping_preimage": {"path": str(preimage_path), "sha256": preimage_hash},
        "preparation_invocation": {
            "path": str(invocation_path),
            "sha256": invocation_hash,
        },
        "source_manifest": {
            "repo_relative_path": CP2_SOURCE_MANIFEST_RELATIVE_PATH,
            "custody_path": str(custody_source_manifest),
            "sha256": _sha256_bytes(source_raw),
        },
        "selection_declaration": {
            "repo_relative_path": CP2_SELECTION_DECLARATION_RELATIVE_PATH,
            "custody_path": str(custody_selection),
            "sha256": _sha256_bytes(selection_raw),
        },
        "sources": [
            {
                "role": role,
                "repo_relative_path": source["catalogs"][index]["prediction_path"],
                "custody_path": str(custody_sources[role]),
                "sha256": source["catalogs"][index]["sha256"],
            }
            for index, role in enumerate(CP2_SEMANTIC_ROLES)
        ],
        "public_manifest": {
            "path": str(public_manifest_path),
            "sha256": public_manifest_hash,
        },
        "commitment": {"path": str(commitment_path), "sha256": commitment_hash},
        "recorded_at_utc": custody_time,
    }
    custody_record_path = custody_root / CP2_CUSTODY_RECORD_FILENAME
    custody_record_hash = _atomic_json_write(
        custody_record_path, custody_record, create=True
    )
    receipt_time = _timestamp_after(custody_time)
    receipt = {
        "record_type": "cp2_blind_preparation_receipt",
        "schema_version": CP2_BLIND_SCHEMA_VERSION,
        "checkpoint": "CP-2",
        "blind_review_id": blind_review_id,
        "candidate": {"commit_sha": candidate_sha, "tree_sha": candidate_tree},
        "public_manifest": {
            "path": str(public_manifest_path),
            "sha256": public_manifest_hash,
        },
        "commitment": {"path": str(commitment_path), "sha256": commitment_hash},
        "anonymous_csv": {"path": str(anonymous_path), "sha256": anonymous_hash},
        "custody_record_sha256": custody_record_hash,
        "recorded_at_utc": receipt_time,
    }
    receipt_path = support_root / CP2_PREPARATION_RECEIPT_FILENAME
    _atomic_json_write(receipt_path, receipt, create=True)
    for path in custody_root.iterdir():
        _require_mode(path, 0o600, "CP-2 custody file")
        sha256_file(path)
    return {
        "blind_review_id": blind_review_id,
        "component_run_id": component_run_id,
        "anonymous_csv": _cp2_binding(anonymous_path),
        "public_manifest": _cp2_binding(public_manifest_path),
        "commitment": _cp2_binding(commitment_path),
        "preparation_receipt": _cp2_binding(receipt_path),
    }


def _cp2_support_from_input(support_root_input: str, blind_review_id: str) -> Path:
    support_root = require_absolute_path(support_root_input, "support_root")
    if support_root.is_symlink() or not support_root.is_dir():
        fail(f"support_root is missing or symlinked: {support_root}")
    if support_root.resolve(strict=True) != support_root:
        fail("support_root must be canonical and traverse no symlink")
    if support_root.parent.name != "_support":
        fail("support_root must be a direct CP-2 _support/<run-id> directory")
    checkpoint_root = support_root.parent.parent
    if (
        checkpoint_root.name != "CP-2"
        or checkpoint_root.parent.name != "evidence"
        or checkpoint_root.parent.parent.name != ".gauntlet"
    ):
        fail("support_root must be under .gauntlet/evidence/CP-2/_support")
    require_identifier(support_root.name, "support run_id")
    require_identifier(blind_review_id, "blind_review_id")
    _require_mode(support_root, 0o700, "CP-2 support root")
    return support_root


def cp2_blind_recompute(
    support_root_input: str, blind_review_id: str
) -> Mapping[str, Any]:
    support_root = _cp2_support_from_input(support_root_input, blind_review_id)
    attempt_path = support_root / CP2_RECOMPUTE_ATTEMPT_FILENAME
    _cp2_create_attempt(
        attempt_path, "cp2_blind_recompute_attempt", blind_review_id
    )
    (
        manifest,
        manifest_path,
        manifest_hash,
        commitment,
        commitment_path,
        commitment_hash,
        rows,
    ) = _cp2_public_bundle(support_root, blind_review_id)
    _cp2_require_runtime_tool_hash(manifest["protocol_tool"]["sha256"])
    metrics = _cp2_metrics(rows, identity_field="label")
    command = (
        "python3 scripts/gauntlet_protocol.py blind-recompute "
        f"--support-root {support_root} --blind-review-id {blind_review_id}"
    )
    record = {
        "record_type": "cp2_blind_metrics",
        "schema_version": CP2_BLIND_SCHEMA_VERSION,
        "checkpoint": "CP-2",
        "blind_review_id": blind_review_id,
        "candidate": manifest["candidate"],
        "public_manifest": {"path": str(manifest_path), "sha256": manifest_hash},
        "commitment": {"path": str(commitment_path), "sha256": commitment_hash},
        "anonymous_csv": manifest["anonymous_csv"],
        "blind_schema": manifest["blind_schema"],
        "recompute_command": command,
        "metrics": metrics,
        "recorded_at_utc": _timestamp_after(commitment["recorded_at_utc"]),
    }
    metrics_path = support_root / CP2_METRICS_FILENAME
    metrics_hash = _atomic_json_write(metrics_path, record, create=True)
    return {
        "blind_review_id": blind_review_id,
        "metrics": {"path": str(metrics_path), "sha256": metrics_hash},
        "recompute_command": command,
    }


def _cp2_assert_public_sanitized(support_root: Path) -> None:
    forbidden = (*CP2_IDENTITY_TOKENS, "revealed-source-")
    for path in support_root.iterdir():
        name = path.name
        if path.is_symlink() or not path.is_file():
            fail(f"Blind support contains a non-regular pre-reveal entry: {path}")
        raw = _read_single_link_file(path, f"identity-free Blind support file {name}")
        lowered_name = name.lower()
        lowered_raw = raw.lower()
        for token in forbidden:
            lowered_token = token.lower()
            token_bytes = lowered_token.encode("utf-8")
            if lowered_token in lowered_name or token_bytes in lowered_raw:
                fail(f"Identity token leaked into Blind public artifact {name}")


def _cp2_assert_identity_free_value(value: Any, field: str) -> None:
    """Reject semantic catalog identities anywhere in a pre-reveal verdict."""

    if isinstance(value, str):
        lowered = value.lower()
        for token in CP2_IDENTITY_TOKENS:
            if token.lower() in lowered:
                fail(f"Identity token leaked into {field}")
        return
    if isinstance(value, Mapping):
        for key, item in value.items():
            _cp2_assert_identity_free_value(item, f"{field}.{key}")
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            _cp2_assert_identity_free_value(item, f"{field}[{index}]")


def _cp2_validate_metrics_record(
    support_root: Path, blind_review_id: str
) -> tuple[Mapping[str, Any], Path, str]:
    (
        manifest,
        manifest_path,
        manifest_hash,
        commitment,
        commitment_path,
        commitment_hash,
        rows,
    ) = _cp2_public_bundle(support_root, blind_review_id)
    attempt_path = support_root / CP2_RECOMPUTE_ATTEMPT_FILENAME
    attempt, _ = _load_json(attempt_path)
    attempt = require_exact_keys(
        attempt,
        "recompute_attempt",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "started_at_utc",
        ),
    )
    if attempt["record_type"] != "cp2_blind_recompute_attempt":
        fail("recompute_attempt.record_type mismatch")
    if (
        attempt["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or attempt["checkpoint"] != "CP-2"
        or attempt["blind_review_id"] != blind_review_id
    ):
        fail("recompute_attempt identity mismatch")
    attempt_time = require_utc(attempt["started_at_utc"], "recompute_attempt.started_at_utc")
    metrics_path = support_root / CP2_METRICS_FILENAME
    metrics, metrics_raw = _load_json(metrics_path)
    metrics_hash = _sha256_bytes(metrics_raw)
    metrics = require_exact_keys(
        metrics,
        "metrics_record",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "public_manifest",
            "commitment",
            "anonymous_csv",
            "blind_schema",
            "recompute_command",
            "metrics",
            "recorded_at_utc",
        ),
    )
    if metrics["record_type"] != "cp2_blind_metrics":
        fail("metrics_record.record_type must be cp2_blind_metrics")
    if (
        metrics["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or metrics["checkpoint"] != "CP-2"
        or metrics["blind_review_id"] != blind_review_id
    ):
        fail("metrics_record identity mismatch")
    if metrics["candidate"] != manifest["candidate"]:
        fail("metrics_record candidate mismatch")
    expected_bindings = {
        "public_manifest": {"path": str(manifest_path), "sha256": manifest_hash},
        "commitment": {"path": str(commitment_path), "sha256": commitment_hash},
        "anonymous_csv": manifest["anonymous_csv"],
    }
    for name, expected in expected_bindings.items():
        if metrics[name] != expected:
            fail(f"metrics_record.{name} binding mismatch")
    if metrics["blind_schema"] != manifest["blind_schema"]:
        fail("metrics_record.blind_schema mismatch")
    expected_command = (
        "python3 scripts/gauntlet_protocol.py blind-recompute "
        f"--support-root {support_root} --blind-review-id {blind_review_id}"
    )
    if metrics["recompute_command"] != expected_command:
        fail("metrics_record.recompute_command is not the exact safe command")
    validated_metrics = _cp2_validate_metric_entries(
        metrics["metrics"], identity_field="label", field="metrics_record.metrics"
    )
    recomputed = _cp2_metrics(rows, identity_field="label")
    if not _cp2_metric_entries_equal(validated_metrics, recomputed):
        fail("metrics_record does not equal independent exact Decimal recomputation")
    recorded_at = require_utc(metrics["recorded_at_utc"], "metrics_record.recorded_at_utc")
    if not (
        parse_utc(commitment["recorded_at_utc"])
        < parse_utc(attempt_time)
        < parse_utc(recorded_at)
    ):
        fail("commitment→recompute-attempt→metrics chronology is not strictly ordered")
    _cp2_assert_public_sanitized(support_root)
    return metrics, metrics_path, metrics_hash


def _cp2_validate_mapping_preimage(
    value: Any, *, blind_review_id: str
) -> Mapping[str, Any]:
    value = require_exact_keys(
        value,
        "mapping_preimage",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "seed_hex",
            "permutation_version",
            "mapping",
            "source_manifest_sha256",
            "selection_declaration_sha256",
            "blind_schema_sha256",
            "protocol_tool_sha256",
            "preparation_invocation_sha256",
            "public_manifest_sha256",
            "anonymous_csv_sha256",
        ),
    )
    if value["record_type"] != "cp2_blind_mapping_preimage":
        fail("mapping_preimage.record_type mismatch")
    if (
        value["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or value["checkpoint"] != "CP-2"
        or value["blind_review_id"] != blind_review_id
    ):
        fail("mapping_preimage identity mismatch")
    candidate = require_exact_keys(
        value["candidate"], "mapping_preimage.candidate", required=("commit_sha", "tree_sha")
    )
    require_git_sha(candidate["commit_sha"], "mapping_preimage.candidate.commit_sha")
    require_git_sha(candidate["tree_sha"], "mapping_preimage.candidate.tree_sha")
    seed_hex = value["seed_hex"]
    if not isinstance(seed_hex, str) or not re.fullmatch(r"[0-9a-f]{64}", seed_hex):
        fail("mapping_preimage.seed_hex must be exactly 256-bit lowercase hex")
    if value["permutation_version"] != CP2_PERMUTATION_VERSION:
        fail("mapping_preimage.permutation_version mismatch")
    mapping = value["mapping"]
    if not isinstance(mapping, list) or len(mapping) != 4:
        fail("mapping_preimage.mapping must have exactly four entries")
    derived = cp2_permutation(bytes.fromhex(seed_hex))
    for index, entry in enumerate(mapping):
        field = f"mapping_preimage.mapping[{index}]"
        entry = require_exact_keys(
            entry,
            field,
            required=("label", "role", "feature_count", "source_sha256"),
        )
        role = derived[index]
        if entry["label"] != CP2_LABELS[index] or entry["role"] != role:
            fail(f"{field} does not match the deterministic seeded permutation")
        require_json_integer(entry["feature_count"], f"{field}.feature_count")
        if entry["feature_count"] != CP2_FEATURE_COUNTS[role]:
            fail(f"{field}.feature_count mismatch")
        require_sha256(entry["source_sha256"], f"{field}.source_sha256")
    for name in (
        "source_manifest_sha256",
        "selection_declaration_sha256",
        "blind_schema_sha256",
        "protocol_tool_sha256",
        "preparation_invocation_sha256",
        "public_manifest_sha256",
        "anonymous_csv_sha256",
    ):
        require_sha256(value[name], f"mapping_preimage.{name}")
    return value


def _cp2_validate_preparation_invocation(
    value: Any,
    *,
    blind_review_id: str,
    candidate: Mapping[str, Any],
    repo_root: Path,
    component_run_id: str,
) -> Mapping[str, Any]:
    value = require_exact_keys(
        value,
        "preparation_invocation",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "argv",
            "identity_inputs",
            "runtime_tool_sha256",
            "recorded_at_utc",
        ),
    )
    if (
        value["record_type"] != "cp2_blind_preparation_invocation"
        or value["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or value["checkpoint"] != "CP-2"
        or value["blind_review_id"] != blind_review_id
        or value["candidate"] != candidate
    ):
        fail("preparation_invocation identity/candidate mismatch")
    expected_argv = [
        "python3",
        PROTOCOL_HELPER_RELATIVE_PATH,
        "blind-prepare",
        "--repo-root",
        str(repo_root),
        "--candidate-sha",
        candidate["commit_sha"],
        "--blind-review-id",
        blind_review_id,
        "--component-run-id",
        component_run_id,
    ]
    if value["argv"] != expected_argv:
        fail("preparation_invocation.argv is not the exact canonical invocation")
    if value["identity_inputs"] != [
        CP2_SOURCE_MANIFEST_RELATIVE_PATH,
        CP2_SELECTION_DECLARATION_RELATIVE_PATH,
    ]:
        fail("preparation_invocation.identity_inputs mismatch")
    require_sha256(
        value["runtime_tool_sha256"],
        "preparation_invocation.runtime_tool_sha256",
    )
    require_utc(value["recorded_at_utc"], "preparation_invocation.recorded_at_utc")
    return value


def _cp2_verify_commitment_preimage(
    preimage: Mapping[str, Any], commitment: Mapping[str, Any]
) -> None:
    actual = _sha256_bytes(
        CP2_COMMITMENT_DOMAIN.encode("ascii")
        + b"\x00"
        + _canonical_json_bytes(preimage)
    )
    if actual != commitment["commitment_sha256"]:
        fail(
            "Hidden mapping commitment does not open: "
            f"expected {commitment['commitment_sha256']}, got {actual}"
        )


def cp2_blind_freeze(
    repo_root_input: str,
    blind_review_id: str,
    component_verdict_input: str,
    integration_run_id: str,
    integration_piece: str,
) -> Mapping[str, Any]:
    repo_root = canonical_repo_root(repo_root_input)
    blind_review_id = require_identifier(blind_review_id, "blind_review_id")
    integration_run_id = require_identifier(integration_run_id, "integration_run_id")
    integration_piece = require_identifier(integration_piece, "integration_piece")
    component_verdict = require_absolute_path(
        component_verdict_input, "component_verdict"
    )
    component_record, component_hash = validate_verdict_file(component_verdict)
    if component_record["record_type"] != COMPONENT_RECORD_TYPE:
        fail("blind-freeze requires a component Critic verdict")
    if component_record["checkpoint"] != "CP-2":
        fail("blind-freeze requires a CP-2 component verdict")
    if component_record["verdict"] != "PASS":
        fail("blind-freeze refuses to freeze a non-PASS Blind verdict")
    blind_binding = component_record.get("blind_review")
    if not isinstance(blind_binding, dict):
        fail("blind-freeze requires the component verdict's blind_review binding")
    if blind_binding.get("blind_review_id") != blind_review_id:
        fail("Blind verdict blind_review_id mismatch")
    candidate = component_record["candidate"]
    candidate_sha = candidate["commit_sha"]
    candidate_tree = candidate["tree_sha"]
    # Allocation is intentionally inside this transition and after validation of
    # the Blind PASS.  A caller cannot pre-create an Integration root/ref and then
    # claim the required PASS < allocation chronology retroactively.
    _, integration_support = initialize_evidence_root(
        str(repo_root), "CP-2", integration_run_id
    )
    integration_ref, ref_candidate, ref_tree = create_evidence_ref(
        str(repo_root),
        "CP-2",
        integration_run_id,
        integration_piece,
        candidate_sha,
    )
    if ref_candidate != candidate_sha or ref_tree != candidate_tree:
        fail("New Integration evidence ref does not bind the Blind candidate SHA/tree")
    integration_allocated_at = _timestamp_after(component_record["recorded_at_utc"])
    _cp2_create_attempt(
        integration_support / CP2_FREEZE_ATTEMPT_FILENAME,
        "cp2_blind_freeze_attempt",
        blind_review_id,
        previous=integration_allocated_at,
    )
    freeze_attempt, _ = _load_json(
        integration_support / CP2_FREEZE_ATTEMPT_FILENAME
    )
    component_support = component_verdict.parent.parent / "_support" / component_record["run_id"]
    # The canonical sibling support path is already enforced by verdict validation.
    metrics, metrics_path, metrics_hash = _cp2_validate_metrics_record(
        component_support, blind_review_id
    )
    manifest_path = component_support / CP2_PUBLIC_MANIFEST_FILENAME
    commitment_path = component_support / CP2_COMMITMENT_FILENAME
    receipt_path = component_support / CP2_PREPARATION_RECEIPT_FILENAME
    anonymous_path = component_support / CP2_PUBLIC_INPUT_FILENAME
    public_manifest, _ = _load_json(manifest_path)
    blind_schema = public_manifest["blind_schema"]
    frozen_sources = (
        (anonymous_path, integration_support / CP2_FROZEN_ANONYMOUS_FILENAME),
        (manifest_path, integration_support / CP2_FROZEN_PUBLIC_MANIFEST_FILENAME),
        (commitment_path, integration_support / CP2_FROZEN_COMMITMENT_FILENAME),
        (receipt_path, integration_support / CP2_FROZEN_RECEIPT_FILENAME),
        (metrics_path, integration_support / CP2_FROZEN_METRICS_FILENAME),
    )
    for source_path, destination_path in frozen_sources:
        payload = _read_single_link_file(source_path, f"Blind frozen input {source_path.name}")
        copied_hash = _atomic_bytes_create(destination_path, payload)
        if copied_hash != sha256_file(source_path):
            fail(f"Frozen copy hash mismatch for {source_path.name}")
        if os.stat(source_path).st_ino == os.stat(destination_path).st_ino:
            fail(f"Frozen input {source_path.name} was hard-linked instead of copied")
    freeze_time = _timestamp_after(freeze_attempt["started_at_utc"])
    freeze = {
        "record_type": "cp2_blind_freeze",
        "schema_version": CP2_BLIND_SCHEMA_VERSION,
        "checkpoint": "CP-2",
        "blind_review_id": blind_review_id,
        "candidate": {"commit_sha": candidate_sha, "tree_sha": candidate_tree},
        "blind_component": {
            "run_id": component_record["run_id"],
            "piece": component_record["piece"],
            "evidence_ref": candidate["evidence_ref"],
            "verdict": {"path": str(component_verdict), "sha256": component_hash},
            "integrity_manifest": component_record["integrity_manifest"],
            "recorded_at_utc": component_record["recorded_at_utc"],
        },
        "integration": {
            "run_id": integration_run_id,
            "piece": integration_piece,
            "evidence_ref": integration_ref,
            "support_root": str(integration_support),
            "allocated_at_utc": integration_allocated_at,
        },
        "anonymous_csv": _cp2_binding(
            integration_support / CP2_FROZEN_ANONYMOUS_FILENAME
        ),
        "public_manifest": _cp2_binding(
            integration_support / CP2_FROZEN_PUBLIC_MANIFEST_FILENAME
        ),
        "commitment": _cp2_binding(
            integration_support / CP2_FROZEN_COMMITMENT_FILENAME
        ),
        "preparation_receipt": _cp2_binding(
            integration_support / CP2_FROZEN_RECEIPT_FILENAME
        ),
        "metrics": _cp2_binding(
            integration_support / CP2_FROZEN_METRICS_FILENAME
        ),
        "blind_schema": blind_schema,
        "recompute_command": metrics["recompute_command"],
        "recorded_at_utc": freeze_time,
    }
    freeze_path = integration_support / CP2_FREEZE_FILENAME
    freeze_hash = _atomic_json_write(freeze_path, freeze, create=True)
    return {
        "blind_review_id": blind_review_id,
        "integration_run_id": integration_run_id,
        "integration_piece": integration_piece,
        "integration_evidence_ref": integration_ref,
        "integration_support_root": str(integration_support),
        "freeze": {"path": str(freeze_path), "sha256": freeze_hash},
    }


def _cp2_validate_freeze(
    support_root: Path,
    blind_review_id: str,
    *,
    repo_root: Path | None = None,
) -> tuple[Mapping[str, Any], Path, str, Path]:
    attempt_path = support_root / CP2_FREEZE_ATTEMPT_FILENAME
    attempt, _ = _load_json(attempt_path)
    attempt = require_exact_keys(
        attempt,
        "freeze_attempt",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "started_at_utc",
        ),
    )
    if attempt["record_type"] != "cp2_blind_freeze_attempt":
        fail("freeze_attempt.record_type mismatch")
    if (
        attempt["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or attempt["checkpoint"] != "CP-2"
        or attempt["blind_review_id"] != blind_review_id
    ):
        fail("freeze_attempt identity mismatch")
    attempt_time = require_utc(attempt["started_at_utc"], "freeze_attempt.started_at_utc")
    freeze_path = support_root / CP2_FREEZE_FILENAME
    freeze, freeze_raw = _load_json(freeze_path)
    freeze_hash = _sha256_bytes(freeze_raw)
    freeze = require_exact_keys(
        freeze,
        "freeze",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "blind_component",
            "integration",
            "anonymous_csv",
            "public_manifest",
            "commitment",
            "preparation_receipt",
            "metrics",
            "blind_schema",
            "recompute_command",
            "recorded_at_utc",
        ),
    )
    if freeze["record_type"] != "cp2_blind_freeze":
        fail("freeze.record_type must be cp2_blind_freeze")
    if (
        freeze["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or freeze["checkpoint"] != "CP-2"
        or freeze["blind_review_id"] != blind_review_id
    ):
        fail("freeze identity mismatch")
    candidate = require_exact_keys(
        freeze["candidate"], "freeze.candidate", required=("commit_sha", "tree_sha")
    )
    candidate_sha = require_git_sha(candidate["commit_sha"], "freeze.candidate.commit_sha")
    candidate_tree = require_git_sha(candidate["tree_sha"], "freeze.candidate.tree_sha")
    component = require_exact_keys(
        freeze["blind_component"],
        "freeze.blind_component",
        required=(
            "run_id",
            "piece",
            "evidence_ref",
            "verdict",
            "integrity_manifest",
            "recorded_at_utc",
        ),
    )
    component_run = require_identifier(component["run_id"], "freeze.blind_component.run_id")
    component_piece = require_identifier(
        component["piece"], "freeze.blind_component.piece"
    )
    expected_component_ref = evidence_ref_name("CP-2", component_run, component_piece)
    if component["evidence_ref"] != expected_component_ref:
        fail("freeze.blind_component.evidence_ref mismatch")
    component_verdict_binding = require_exact_keys(
        component["verdict"],
        "freeze.blind_component.verdict",
        required=CP2_HASH_BINDING_REQUIRED_FIELDS,
    )
    component_verdict_path = require_absolute_path(
        component_verdict_binding["path"], "freeze.blind_component.verdict.path"
    )
    component_verdict_hash = require_sha256(
        component_verdict_binding["sha256"], "freeze.blind_component.verdict.sha256"
    )
    component_integrity_binding = require_exact_keys(
        component["integrity_manifest"],
        "freeze.blind_component.integrity_manifest",
        required=CP2_HASH_BINDING_REQUIRED_FIELDS,
    )
    require_absolute_path(
        component_integrity_binding["path"],
        "freeze.blind_component.integrity_manifest.path",
    )
    require_sha256(
        component_integrity_binding["sha256"],
        "freeze.blind_component.integrity_manifest.sha256",
    )
    component_time = require_utc(
        component["recorded_at_utc"], "freeze.blind_component.recorded_at_utc"
    )
    integration = require_exact_keys(
        freeze["integration"],
        "freeze.integration",
        required=(
            "run_id",
            "piece",
            "evidence_ref",
            "support_root",
            "allocated_at_utc",
        ),
    )
    integration_run = require_identifier(integration["run_id"], "freeze.integration.run_id")
    integration_piece = require_identifier(integration["piece"], "freeze.integration.piece")
    if integration["support_root"] != str(support_root):
        fail("freeze.integration.support_root mismatch")
    expected_integration_ref = evidence_ref_name("CP-2", integration_run, integration_piece)
    if integration["evidence_ref"] != expected_integration_ref:
        fail("freeze.integration.evidence_ref mismatch")
    allocation_time = require_utc(
        integration["allocated_at_utc"], "freeze.integration.allocated_at_utc"
    )
    frozen_names = {
        "anonymous_csv": CP2_FROZEN_ANONYMOUS_FILENAME,
        "public_manifest": CP2_FROZEN_PUBLIC_MANIFEST_FILENAME,
        "commitment": CP2_FROZEN_COMMITMENT_FILENAME,
        "preparation_receipt": CP2_FROZEN_RECEIPT_FILENAME,
        "metrics": CP2_FROZEN_METRICS_FILENAME,
    }
    frozen_paths: dict[str, Path] = {}
    for name, filename in frozen_names.items():
        path, _ = _cp2_validate_absolute_binding(
            freeze[name], f"freeze.{name}", ownership_root=support_root
        )
        if path.name != filename:
            fail(f"freeze.{name}.path must end in {filename}")
        frozen_paths[name] = path
    anonymous_raw = _read_single_link_file(
        frozen_paths["anonymous_csv"], "frozen anonymous CSV"
    )
    anonymous_rows = _cp2_parse_csv(
        anonymous_raw, anonymous=True, field="frozen anonymous CSV"
    )
    public_manifest, public_raw = _load_json(frozen_paths["public_manifest"])
    # Frozen records retain their original absolute provenance paths.  From this
    # point onward their contents are verified only against the Integration-owned
    # byte copies named by the freeze; no component-support path is dereferenced.
    public_manifest = require_exact_keys(
        public_manifest,
        "frozen public_manifest",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "blind_schema",
            "protocol_tool",
            "anonymous_csv",
            "labels",
            "folds",
            "header",
            "quantiles",
            "canonical_sort",
            "row_count_per_label",
            "blindness_strength",
            "prepared_at_utc",
        ),
    )
    if (
        public_manifest["record_type"] != "cp2_blind_public_manifest"
        or public_manifest["blind_review_id"] != blind_review_id
        or public_manifest["candidate"] != candidate
    ):
        fail("frozen public manifest identity/candidate mismatch")
    if not _json_exact_equal(public_manifest["folds"], list(CP2_FOLDS)):
        fail("frozen public manifest folds are not exact JSON integers 1..5")
    frozen_row_count = require_json_integer(
        public_manifest["row_count_per_label"],
        "frozen public manifest row_count_per_label",
    )
    if frozen_row_count <= 0:
        fail("frozen public manifest row_count_per_label must be positive")
    _cp2_require_runtime_tool_hash(public_manifest["protocol_tool"]["sha256"])
    if public_manifest["anonymous_csv"]["sha256"] != freeze["anonymous_csv"]["sha256"]:
        fail("frozen public manifest anonymous CSV hash mismatch")
    if len(anonymous_rows) != 4 * frozen_row_count:
        fail("frozen public manifest row count mismatch")
    commitment, _ = _load_json(frozen_paths["commitment"])
    commitment = require_exact_keys(
        commitment,
        "frozen commitment",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "domain",
            "commitment_sha256",
            "seed_bits",
            "permutation_version",
            "public_manifest",
            "anonymous_csv",
            "blind_schema",
            "recorded_at_utc",
        ),
    )
    if (
        commitment["record_type"] != "cp2_blind_commitment"
        or commitment["blind_review_id"] != blind_review_id
        or commitment["candidate"] != candidate
        or commitment["domain"] != CP2_COMMITMENT_DOMAIN
        or require_json_integer(
            commitment["seed_bits"], "frozen commitment.seed_bits"
        )
        != 256
        or commitment["permutation_version"] != CP2_PERMUTATION_VERSION
    ):
        fail("frozen commitment identity/protocol mismatch")
    require_sha256(commitment["commitment_sha256"], "frozen commitment digest")
    if commitment["public_manifest"]["sha256"] != _sha256_bytes(public_raw):
        fail("frozen commitment public-manifest hash mismatch")
    if commitment["anonymous_csv"]["sha256"] != freeze["anonymous_csv"]["sha256"]:
        fail("frozen commitment anonymous-CSV hash mismatch")
    receipt, _ = _load_json(frozen_paths["preparation_receipt"])
    if (
        receipt.get("record_type") != "cp2_blind_preparation_receipt"
        or receipt.get("blind_review_id") != blind_review_id
        or receipt.get("candidate") != candidate
        or receipt.get("public_manifest", {}).get("sha256")
        != freeze["public_manifest"]["sha256"]
        or receipt.get("commitment", {}).get("sha256")
        != freeze["commitment"]["sha256"]
        or receipt.get("anonymous_csv", {}).get("sha256")
        != freeze["anonymous_csv"]["sha256"]
    ):
        fail("frozen preparation receipt binding mismatch")
    require_sha256(
        receipt.get("custody_record_sha256"),
        "frozen preparation receipt custody_record_sha256",
    )
    metrics, _ = _load_json(frozen_paths["metrics"])
    metrics = require_exact_keys(
        metrics,
        "frozen metrics",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "public_manifest",
            "commitment",
            "anonymous_csv",
            "blind_schema",
            "recompute_command",
            "metrics",
            "recorded_at_utc",
        ),
    )
    if (
        metrics["record_type"] != "cp2_blind_metrics"
        or metrics["blind_review_id"] != blind_review_id
        or metrics["candidate"] != candidate
        or metrics["public_manifest"]["sha256"] != freeze["public_manifest"]["sha256"]
        or metrics["commitment"]["sha256"] != freeze["commitment"]["sha256"]
        or metrics["anonymous_csv"]["sha256"] != freeze["anonymous_csv"]["sha256"]
    ):
        fail("frozen metrics binding mismatch")
    metric_entries = _cp2_validate_metric_entries(
        metrics["metrics"], identity_field="label", field="frozen metrics.metrics"
    )
    if not _cp2_metric_entries_equal(
        metric_entries, _cp2_metrics(anonymous_rows, identity_field="label")
    ):
        fail("frozen metrics do not recompute from the frozen anonymous CSV")
    if freeze["blind_schema"] != public_manifest["blind_schema"]:
        fail("freeze.blind_schema binding mismatch")
    if freeze["recompute_command"] != metrics["recompute_command"]:
        fail("freeze.recompute_command mismatch")
    freeze_time = require_utc(freeze["recorded_at_utc"], "freeze.recorded_at_utc")
    if not (
        parse_utc(component_time)
        < parse_utc(allocation_time)
        < parse_utc(attempt_time)
        < parse_utc(freeze_time)
    ):
        fail(
            "Blind PASS→Integration allocation→freeze-attempt→freeze chronology "
            "is not strictly ordered"
        )
    if repo_root is not None:
        _cp2_validate_absolute_binding(
            component["verdict"], "freeze.blind_component.verdict"
        )
        _cp2_validate_absolute_binding(
            component["integrity_manifest"],
            "freeze.blind_component.integrity_manifest",
        )
        _, actual_tree = _validate_full_commit(repo_root, candidate_sha)
        if actual_tree != candidate_tree:
            fail("freeze candidate tree mismatch")
        if _git(repo_root, ["show-ref", "--verify", "--hash", expected_integration_ref]) != candidate_sha:
            fail("freeze Integration evidence ref does not bind the candidate")
        if _git(repo_root, ["show-ref", "--verify", "--hash", expected_component_ref]) != candidate_sha:
            fail("freeze Blind evidence ref does not bind the candidate")
        component_record, actual_component_hash = validate_verdict_file(
            component_verdict_path
        )
        if actual_component_hash != component_verdict_hash:
            fail("freeze Blind verdict hash changed")
        expected_component = {
            "run_id": component_record["run_id"],
            "piece": component_record["piece"],
            "evidence_ref": component_record["candidate"]["evidence_ref"],
            "verdict": {
                "path": str(component_verdict_path),
                "sha256": actual_component_hash,
            },
            "integrity_manifest": component_record["integrity_manifest"],
            "recorded_at_utc": component_record["recorded_at_utc"],
        }
        if component != expected_component:
            fail(
                "freeze.blind_component does not exactly reproduce the "
                "validated Blind verdict provenance"
            )
        if (
            component_record["verdict"] != "PASS"
            or component_record["checkpoint"] != "CP-2"
            or component_record["candidate"]
            != {
                "commit_sha": candidate_sha,
                "tree_sha": candidate_tree,
                "evidence_ref": expected_component_ref,
            }
            or component_record.get("blind_review", {}).get("blind_review_id")
            != blind_review_id
        ):
            fail("freeze no longer binds a current schema-valid Blind PASS")
    return freeze, freeze_path, freeze_hash, component_verdict_path


def _cp2_custody_snapshot(custody_root: Path) -> Mapping[str, tuple[str, int, int]]:
    if custody_root.is_symlink() or not custody_root.is_dir():
        fail(f"Custody root is missing or symlinked: {custody_root}")
    if custody_root.resolve(strict=True) != custody_root:
        fail("Custody root must be canonical and traverse no symlink")
    _require_mode(custody_root, 0o700, "CP-2 custody root")
    snapshot: dict[str, tuple[str, int, int]] = {}
    for path in sorted(custody_root.iterdir(), key=lambda item: item.name):
        if path.is_symlink() or not path.is_file():
            fail(f"Custody contains a non-regular entry: {path}")
        metadata = path.stat()
        if metadata.st_nlink != 1:
            fail(f"Custody file is hard-linked: {path}")
        mode = stat.S_IMODE(metadata.st_mode)
        if mode != 0o600:
            fail(f"Custody file mode must be 0600, got {mode:04o}: {path}")
        snapshot[path.name] = (sha256_file(path), mode, metadata.st_size)
    expected_names = {
        CP2_CUSTODY_RECORD_FILENAME,
        CP2_PREPARATION_INVOCATION_FILENAME,
        CP2_MAPPING_PREIMAGE_FILENAME,
        CP2_CUSTODY_SOURCE_MANIFEST_FILENAME,
        CP2_CUSTODY_SELECTION_FILENAME,
        *(f"source-{role}.csv" for role in CP2_SEMANTIC_ROLES),
    }
    if set(snapshot) != expected_names:
        fail("Custody root does not contain the exact canonical create-only file set")
    return snapshot


def cp2_blind_reveal(
    repo_root_input: str, blind_review_id: str, integration_run_id: str
) -> Mapping[str, Any]:
    repo_root = canonical_repo_root(repo_root_input)
    blind_review_id = require_identifier(blind_review_id, "blind_review_id")
    integration_run_id = require_identifier(integration_run_id, "integration_run_id")
    _, support_root = _cp2_run_paths(repo_root, integration_run_id)
    freeze, freeze_path, freeze_hash, _ = _cp2_validate_freeze(
        support_root, blind_review_id, repo_root=repo_root
    )
    if freeze["integration"]["run_id"] != integration_run_id:
        fail("blind-reveal integration_run_id does not match the freeze")
    attempt_path = support_root / CP2_REVEAL_ATTEMPT_FILENAME
    _cp2_create_attempt(attempt_path, "cp2_blind_reveal_attempt", blind_review_id)
    reveal_attempt, _ = _load_json(attempt_path)
    custody_root = _cp2_custody_root(repo_root, blind_review_id)
    before = _cp2_custody_snapshot(custody_root)
    custody_path = custody_root / CP2_CUSTODY_RECORD_FILENAME
    custody, custody_raw = _load_json(custody_path)
    custody = _cp2_load_json_bytes(custody_raw, "custody record")
    custody = require_exact_keys(
        custody,
        "custody",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "component",
            "mapping_preimage",
            "preparation_invocation",
            "source_manifest",
            "selection_declaration",
            "sources",
            "public_manifest",
            "commitment",
            "recorded_at_utc",
        ),
    )
    if custody["record_type"] != "cp2_blind_custody":
        fail("custody.record_type mismatch")
    if (
        custody["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or custody["checkpoint"] != "CP-2"
        or custody["blind_review_id"] != blind_review_id
        or custody["candidate"] != freeze["candidate"]
    ):
        fail("custody identity/candidate mismatch")
    custody_recorded_at = require_utc(
        custody["recorded_at_utc"], "custody.recorded_at_utc"
    )
    custody_component = require_exact_keys(
        custody["component"],
        "custody.component",
        required=("run_id", "piece", "evidence_ref", "support_root"),
    )
    component_run_id = require_identifier(
        custody_component["run_id"], "custody.component.run_id"
    )
    require_identifier(custody_component["piece"], "custody.component.piece")
    component_verdict_path = Path(freeze["blind_component"]["verdict"]["path"])
    component_support = (
        component_verdict_path.parent.parent / "_support" / component_run_id
    )
    expected_component = {
        "run_id": freeze["blind_component"]["run_id"],
        "piece": freeze["blind_component"]["piece"],
        "evidence_ref": freeze["blind_component"]["evidence_ref"],
        "support_root": str(component_support),
    }
    if custody_component != expected_component:
        fail("custody Blind component identity/support does not match freeze")
    custody_public_names = {
        "public_manifest": CP2_PUBLIC_MANIFEST_FILENAME,
        "commitment": CP2_COMMITMENT_FILENAME,
    }
    for name, filename in custody_public_names.items():
        binding = require_exact_keys(
            custody[name], f"custody.{name}", required=CP2_HASH_BINDING_REQUIRED_FIELDS
        )
        if (
            binding["path"] != str(component_support / filename)
            or binding["sha256"] != freeze[name]["sha256"]
        ):
            fail(f"custody.{name} does not bind the canonical frozen source")
    preimage_path, _ = _cp2_validate_absolute_binding(
        custody["mapping_preimage"], "custody.mapping_preimage", ownership_root=custody_root
    )
    if preimage_path != custody_root / CP2_MAPPING_PREIMAGE_FILENAME:
        fail("custody.mapping_preimage has the wrong canonical path")
    preimage, preimage_raw = _load_json(preimage_path)
    preimage = _cp2_validate_mapping_preimage(
        preimage, blind_review_id=blind_review_id
    )
    commitment, _ = _load_json(Path(freeze["commitment"]["path"]))
    _cp2_verify_commitment_preimage(preimage, commitment)
    if preimage["candidate"] != freeze["candidate"]:
        fail("mapping preimage candidate mismatch")
    if preimage["public_manifest_sha256"] != freeze["public_manifest"]["sha256"]:
        fail("mapping preimage public-manifest hash mismatch")
    public_manifest, _ = _load_json(Path(freeze["public_manifest"]["path"]))
    preparation_receipt, _ = _load_json(
        Path(freeze["preparation_receipt"]["path"])
    )
    if preparation_receipt.get("custody_record_sha256") != _sha256_bytes(
        custody_raw
    ):
        fail("Frozen preparation receipt custody-record hash mismatch")
    if preimage["anonymous_csv_sha256"] != public_manifest["anonymous_csv"]["sha256"]:
        fail("mapping preimage anonymous-CSV hash mismatch")

    copied_mapping = support_root / CP2_REVEALED_MAPPING_FILENAME
    copied_preparation = support_root / CP2_REVEALED_PREPARATION_FILENAME
    copied_manifest = support_root / CP2_REVEALED_SOURCE_MANIFEST_FILENAME
    copied_selection = support_root / CP2_REVEALED_SELECTION_FILENAME
    _atomic_bytes_create(copied_mapping, preimage_raw)
    invocation_path, _ = _cp2_validate_absolute_binding(
        custody["preparation_invocation"],
        "custody.preparation_invocation",
        ownership_root=custody_root,
    )
    if invocation_path != custody_root / CP2_PREPARATION_INVOCATION_FILENAME:
        fail("custody.preparation_invocation has the wrong canonical path")
    invocation_raw = _read_single_link_file(
        invocation_path, "custody preparation invocation"
    )
    if _sha256_bytes(invocation_raw) != preimage["preparation_invocation_sha256"]:
        fail("Custody preparation invocation is not bound by the hidden commitment")
    invocation = _cp2_validate_preparation_invocation(
        _cp2_load_json_bytes(invocation_raw, "custody preparation invocation"),
        blind_review_id=blind_review_id,
        candidate=freeze["candidate"],
        repo_root=repo_root,
        component_run_id=component_run_id,
    )
    if invocation["runtime_tool_sha256"] != preimage["protocol_tool_sha256"]:
        fail("Custody preparation invocation uses a different protocol tool")
    if not (
        parse_utc(invocation["recorded_at_utc"])
        < parse_utc(public_manifest["prepared_at_utc"])
        < parse_utc(commitment["recorded_at_utc"])
        < parse_utc(custody_recorded_at)
        < parse_utc(preparation_receipt["recorded_at_utc"])
    ):
        fail(
            "Preparation invocation→public manifest→commitment→custody→receipt "
            "chronology is not strictly ordered"
        )
    _atomic_bytes_create(copied_preparation, invocation_raw)
    custody_source_manifest = require_exact_keys(
        custody["source_manifest"],
        "custody.source_manifest",
        required=("repo_relative_path", "custody_path", "sha256"),
    )
    custody_selection = require_exact_keys(
        custody["selection_declaration"],
        "custody.selection_declaration",
        required=("repo_relative_path", "custody_path", "sha256"),
    )
    source_manifest_path = require_absolute_path(
        custody_source_manifest["custody_path"],
        "custody.source_manifest.custody_path",
    )
    selection_path = require_absolute_path(
        custody_selection["custody_path"],
        "custody.selection_declaration.custody_path",
    )
    if (
        custody_source_manifest["repo_relative_path"]
        != CP2_SOURCE_MANIFEST_RELATIVE_PATH
        or source_manifest_path != custody_root / CP2_CUSTODY_SOURCE_MANIFEST_FILENAME
    ):
        fail("custody.source_manifest path/identity is not canonical")
    if (
        custody_selection["repo_relative_path"]
        != CP2_SELECTION_DECLARATION_RELATIVE_PATH
        or selection_path != custody_root / CP2_CUSTODY_SELECTION_FILENAME
    ):
        fail("custody.selection_declaration path/identity is not canonical")
    source_manifest_raw = _read_single_link_file(source_manifest_path, "custody source manifest")
    selection_raw = _read_single_link_file(selection_path, "custody selection declaration")
    if (
        _sha256_bytes(source_manifest_raw) != custody_source_manifest["sha256"]
        or custody_source_manifest["sha256"] != preimage["source_manifest_sha256"]
    ):
        fail("custody source manifest hash mismatch")
    if (
        _sha256_bytes(selection_raw) != custody_selection["sha256"]
        or custody_selection["sha256"]
        != preimage["selection_declaration_sha256"]
    ):
        fail("custody selection declaration hash mismatch")
    source_manifest = _cp2_validate_source_manifest(
        _cp2_load_json_bytes(source_manifest_raw, "custody source manifest"),
        source_manifest_sha256=preimage["source_manifest_sha256"],
        selection_declaration_sha256=preimage[
            "selection_declaration_sha256"
        ],
    )
    preimage_sources = {
        entry["role"]: entry["source_sha256"] for entry in preimage["mapping"]
    }
    _atomic_bytes_create(copied_manifest, source_manifest_raw)
    _atomic_bytes_create(copied_selection, selection_raw)
    copied_sources: list[Mapping[str, str]] = []
    if not isinstance(custody["sources"], list) or len(custody["sources"]) != 4:
        fail("custody.sources must contain exactly four entries")
    for index, entry in enumerate(custody["sources"]):
        entry = require_exact_keys(
            entry,
            f"custody.sources[{index}]",
            required=("role", "repo_relative_path", "custody_path", "sha256"),
        )
        role = CP2_SEMANTIC_ROLES[index]
        if entry["role"] != role:
            fail(f"custody.sources[{index}].role must be {role}")
        source_identity = source_manifest["catalogs"][index]
        if (
            entry["repo_relative_path"] != source_identity["prediction_path"]
            or entry["sha256"] != source_identity["sha256"]
            or entry["sha256"] != preimage_sources[role]
        ):
            fail(
                f"Custody source identity/hash does not match the committed "
                f"source manifest and mapping preimage for {role}"
            )
        source_path = require_absolute_path(
            entry["custody_path"], f"custody.sources[{index}].custody_path"
        )
        if source_path != custody_root / f"source-{role}.csv":
            fail(f"Custody source path is not canonical for {role}")
        source_raw = _read_single_link_file(source_path, f"custody source {role}")
        if _sha256_bytes(source_raw) != entry["sha256"]:
            fail(f"Custody source hash mismatch for {role}")
        destination = support_root / f"revealed-source-{role}.csv"
        copied_hash = _atomic_bytes_create(destination, source_raw)
        if os.stat(destination).st_ino == os.stat(source_path).st_ino:
            fail(f"Revealed source {role} was hard-linked instead of copied")
        copied_sources.append(
            {"role": role, "path": str(destination), "sha256": copied_hash}
        )
    if _cp2_custody_snapshot(custody_root) != before:
        fail("Custody changed during reveal")
    reveal_time = _timestamp_after(reveal_attempt["started_at_utc"])
    if parse_utc(reveal_time) <= parse_utc(freeze["recorded_at_utc"]):
        reveal_time = _timestamp_after(freeze["recorded_at_utc"])
    reveal = {
        "record_type": "cp2_blind_reveal",
        "schema_version": CP2_BLIND_SCHEMA_VERSION,
        "checkpoint": "CP-2",
        "blind_review_id": blind_review_id,
        "candidate": freeze["candidate"],
        "freeze": {"path": str(freeze_path), "sha256": freeze_hash},
        "mapping": _cp2_binding(copied_mapping),
        "preparation_record": _cp2_binding(copied_preparation),
        "source_manifest": _cp2_binding(copied_manifest),
        "selection_declaration": _cp2_binding(copied_selection),
        "sources": copied_sources,
        "commitment": freeze["commitment"],
        "recorded_at_utc": reveal_time,
    }
    reveal_path = support_root / CP2_REVEAL_FILENAME
    reveal_hash = _atomic_json_write(reveal_path, reveal, create=True)
    return {
        "blind_review_id": blind_review_id,
        "reveal": {"path": str(reveal_path), "sha256": reveal_hash},
    }


def _cp2_validate_reveal(
    support_root: Path,
    blind_review_id: str,
    *,
    repo_root: Path | None = None,
) -> tuple[
    Mapping[str, Any],
    Path,
    str,
    Mapping[str, Any],
    Mapping[str, Any],
    dict[str, list[dict[str, str]]],
    list[Mapping[str, Any]],
]:
    freeze, freeze_path, freeze_hash, _ = _cp2_validate_freeze(
        support_root, blind_review_id, repo_root=repo_root
    )
    attempt_path = support_root / CP2_REVEAL_ATTEMPT_FILENAME
    attempt, _ = _load_json(attempt_path)
    attempt = require_exact_keys(
        attempt,
        "reveal_attempt",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "started_at_utc",
        ),
    )
    if (
        attempt["record_type"] != "cp2_blind_reveal_attempt"
        or attempt["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or attempt["checkpoint"] != "CP-2"
        or attempt["blind_review_id"] != blind_review_id
    ):
        fail("reveal_attempt identity mismatch")
    attempt_time = require_utc(attempt["started_at_utc"], "reveal_attempt.started_at_utc")
    reveal_path = support_root / CP2_REVEAL_FILENAME
    reveal, reveal_raw = _load_json(reveal_path)
    reveal_hash = _sha256_bytes(reveal_raw)
    reveal = require_exact_keys(
        reveal,
        "reveal",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "freeze",
            "mapping",
            "preparation_record",
            "source_manifest",
            "selection_declaration",
            "sources",
            "commitment",
            "recorded_at_utc",
        ),
    )
    if (
        reveal["record_type"] != "cp2_blind_reveal"
        or reveal["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or reveal["checkpoint"] != "CP-2"
        or reveal["blind_review_id"] != blind_review_id
        or reveal["candidate"] != freeze["candidate"]
    ):
        fail("reveal identity/candidate mismatch")
    if reveal["freeze"] != {"path": str(freeze_path), "sha256": freeze_hash}:
        fail("reveal.freeze binding mismatch")
    if reveal["commitment"] != freeze["commitment"]:
        fail("reveal.commitment binding mismatch")
    expected_file_names = {
        "mapping": CP2_REVEALED_MAPPING_FILENAME,
        "preparation_record": CP2_REVEALED_PREPARATION_FILENAME,
        "source_manifest": CP2_REVEALED_SOURCE_MANIFEST_FILENAME,
        "selection_declaration": CP2_REVEALED_SELECTION_FILENAME,
    }
    revealed_paths: dict[str, Path] = {}
    for name, filename in expected_file_names.items():
        path, _ = _cp2_validate_absolute_binding(
            reveal[name], f"reveal.{name}", ownership_root=support_root
        )
        if path.name != filename:
            fail(f"reveal.{name}.path must end in {filename}")
        revealed_paths[name] = path
    preimage, _ = _load_json(revealed_paths["mapping"])
    preimage = _cp2_validate_mapping_preimage(
        preimage, blind_review_id=blind_review_id
    )
    if preimage["candidate"] != freeze["candidate"]:
        fail("Revealed mapping candidate mismatch")
    commitment, _ = _load_json(Path(freeze["commitment"]["path"]))
    _cp2_verify_commitment_preimage(preimage, commitment)
    if preimage["public_manifest_sha256"] != freeze["public_manifest"]["sha256"]:
        fail("Revealed mapping public-manifest hash mismatch")
    if preimage["anonymous_csv_sha256"] != freeze["anonymous_csv"]["sha256"]:
        fail("Revealed mapping anonymous-CSV hash mismatch")
    preparation_raw = _read_single_link_file(
        revealed_paths["preparation_record"], "revealed preparation invocation"
    )
    if _sha256_bytes(preparation_raw) != preimage["preparation_invocation_sha256"]:
        fail("Revealed preparation invocation is not bound by the commitment")
    invocation_repo_root = repo_root if repo_root is not None else support_root.parents[4]
    preparation = _cp2_validate_preparation_invocation(
        _cp2_load_json_bytes(preparation_raw, "revealed preparation invocation"),
        blind_review_id=blind_review_id,
        candidate=freeze["candidate"],
        repo_root=invocation_repo_root,
        component_run_id=freeze["blind_component"]["run_id"],
    )
    if preparation["runtime_tool_sha256"] != preimage["protocol_tool_sha256"]:
        fail("Revealed preparation invocation uses a different protocol tool")
    source_manifest_raw = _read_single_link_file(
        revealed_paths["source_manifest"], "revealed source manifest"
    )
    selection_raw = _read_single_link_file(
        revealed_paths["selection_declaration"], "revealed selection declaration"
    )
    if _sha256_bytes(source_manifest_raw) != preimage["source_manifest_sha256"]:
        fail("Revealed source-manifest hash mismatch")
    if _sha256_bytes(selection_raw) != preimage["selection_declaration_sha256"]:
        fail("Revealed selection-declaration hash mismatch")
    source_manifest = _cp2_load_json_bytes(
        source_manifest_raw, "revealed source manifest"
    )
    selection = _cp2_load_json_bytes(
        selection_raw, "revealed selection declaration"
    )
    source_manifest = _cp2_validate_source_manifest(
        source_manifest,
        source_manifest_sha256=_sha256_bytes(source_manifest_raw),
        selection_declaration_sha256=_sha256_bytes(selection_raw),
    )
    selection = _cp2_validate_selection_declaration(selection)
    sources = reveal["sources"]
    if not isinstance(sources, list) or len(sources) != 4:
        fail("reveal.sources must contain exactly four entries")
    rows_by_role: dict[str, list[dict[str, str]]] = {}
    for index, entry in enumerate(sources):
        field = f"reveal.sources[{index}]"
        entry = require_exact_keys(
            entry, field, required=("role", "path", "sha256")
        )
        role = CP2_SEMANTIC_ROLES[index]
        if entry["role"] != role:
            fail(f"{field}.role must be {role}")
        path, digest = _cp2_validate_absolute_binding(
            {"path": entry["path"], "sha256": entry["sha256"]},
            field,
            ownership_root=support_root,
        )
        if path.name != f"revealed-source-{role}.csv":
            fail(f"{field}.path has the wrong canonical filename")
        catalog = source_manifest["catalogs"][index]
        if digest != catalog["sha256"] or digest != preimage["mapping"][
            next(i for i, item in enumerate(preimage["mapping"]) if item["role"] == role)
        ]["source_sha256"]:
            fail(f"{field} hash does not match source manifest/mapping")
        raw = _read_single_link_file(path, f"revealed source {role}")
        rows_by_role[role] = _cp2_parse_csv(
            raw, anonymous=False, field=f"revealed source {role}"
        )
        if repo_root is not None:
            committed_raw = _git_bytes(
                repo_root,
                ["show", f"{freeze['candidate']['commit_sha']}:{catalog['prediction_path']}"],
            )
            if raw != committed_raw:
                fail(f"Revealed source {role} is not the committed candidate blob")
    _cp2_match_source_rows(rows_by_role)
    if repo_root is not None:
        candidate_sha = freeze["candidate"]["commit_sha"]
        if source_manifest_raw != _git_bytes(
            repo_root, ["show", f"{candidate_sha}:{CP2_SOURCE_MANIFEST_RELATIVE_PATH}"]
        ):
            fail("Revealed source manifest is not the committed candidate blob")
        if selection_raw != _git_bytes(
            repo_root,
            ["show", f"{candidate_sha}:{CP2_SELECTION_DECLARATION_RELATIVE_PATH}"],
        ):
            fail("Revealed selection declaration is not the committed candidate blob")

    mapping_by_label = {entry["label"]: entry["role"] for entry in preimage["mapping"]}
    indexed = {
        role: {(row["fold_id"], row["row_id"]): row for row in rows}
        for role, rows in rows_by_role.items()
    }
    keys = sorted(
        indexed[CP2_SEMANTIC_ROLES[0]],
        key=lambda key: (int(key[0]), key[1].encode("utf-8")),
    )
    rebuilt_rows: list[dict[str, str]] = []
    for key in keys:
        for label in CP2_LABELS:
            row = indexed[mapping_by_label[label]][key]
            rebuilt_rows.append(
                {"label": label, **{name: row[name] for name in CP2_SOURCE_HEADER}}
            )
    rebuilt = _cp2_csv_bytes(CP2_ANONYMOUS_HEADER, rebuilt_rows)
    frozen_anonymous = _read_single_link_file(
        Path(freeze["anonymous_csv"]["path"]), "Integration frozen anonymous CSV"
    )
    if rebuilt != frozen_anonymous:
        fail("Revealed sources/mapping do not reconstruct the frozen anonymous CSV")
    metrics_record, _ = _load_json(Path(freeze["metrics"]["path"]))
    anonymous_metrics = _cp2_validate_metric_entries(
        metrics_record["metrics"],
        identity_field="label",
        field="frozen metrics.metrics",
    )
    reveal_time = require_utc(reveal["recorded_at_utc"], "reveal.recorded_at_utc")
    if not (
        parse_utc(freeze["recorded_at_utc"])
        < parse_utc(attempt_time)
        < parse_utc(reveal_time)
    ):
        fail("freeze→reveal-attempt→reveal chronology is not strictly ordered")
    return (
        reveal,
        reveal_path,
        reveal_hash,
        source_manifest,
        selection,
        rows_by_role,
        anonymous_metrics,
    )


def _cp2_adjudicate_exact_inner(
    metrics_by_role: Sequence[Mapping[str, Any]],
) -> tuple[str, Mapping[str, Any]]:
    metrics = {entry["role"]: entry for entry in metrics_by_role}
    base = metrics["strict_base"]
    base_loss = Decimal(base["loss_sum"])
    candidates: list[Mapping[str, Any]] = []
    eligible_roles: list[str] = []
    for role in CP2_SEMANTIC_ROLES[1:]:
        arm = metrics[role]
        arm_loss = Decimal(arm["loss_sum"])
        relative_lhs = Decimal(100) * (base_loss - arm_loss)
        relative_rhs = base_loss
        relative_pass = base_loss > 0 and relative_lhs >= relative_rhs
        coverage_lhs = 100 * (base["coverage_hits"] - arm["coverage_hits"])
        coverage_rhs = 2 * base["coverage_total"]
        coverage_pass = coverage_lhs <= coverage_rhs
        improving_folds = sum(
            Decimal(arm["folds"][index]["loss_sum"])
            < Decimal(base["folds"][index]["loss_sum"])
            for index in range(5)
        )
        fold_pass = improving_folds >= 4
        eligible = relative_pass and coverage_pass and fold_pass
        if eligible:
            eligible_roles.append(role)
        candidates.append(
            {
                "role": role,
                "relative_loss": {
                    "lhs": _cp2_decimal_string(relative_lhs),
                    "rhs": _cp2_decimal_string(relative_rhs),
                    "pass": relative_pass,
                },
                "coverage": {
                    "lhs": coverage_lhs,
                    "rhs": coverage_rhs,
                    "pass": coverage_pass,
                },
                "improving_folds": improving_folds,
                "fold_pass": fold_pass,
                "eligible": eligible,
            }
        )
    minimum_loss: Decimal | None = None
    tie_set: list[str] = []
    feature_survivors: list[str] = []
    calibration_survivors: list[str] = []
    if base_loss == 0:
        winner = "strict_base"
        decision_reason = "base_zero"
    elif not eligible_roles:
        winner = "strict_base"
        decision_reason = "no_eligible_arm"
    else:
        minimum_loss = min(Decimal(metrics[role]["loss_sum"]) for role in eligible_roles)
        if minimum_loss == 0:
            tie_set = [
                role for role in eligible_roles if Decimal(metrics[role]["loss_sum"]) == 0
            ]
        else:
            tie_set = [
                role
                for role in eligible_roles
                if Decimal(1000)
                * (Decimal(metrics[role]["loss_sum"]) - minimum_loss)
                <= minimum_loss
            ]
        minimum_features = min(CP2_FEATURE_COUNTS[role] for role in tie_set)
        feature_survivors = [
            role for role in tie_set if CP2_FEATURE_COUNTS[role] == minimum_features
        ]
        # All catalogs have a matched N.  Compare exact |coverage-4/5| by the
        # integer numerator |5*hits-4*N|; no rounded proportion is involved.
        deviations = {
            role: abs(
                5 * metrics[role]["coverage_hits"]
                - 4 * metrics[role]["coverage_total"]
            )
            for role in feature_survivors
        }
        minimum_deviation = min(deviations.values())
        calibration_survivors = [
            role for role in feature_survivors if deviations[role] == minimum_deviation
        ]
        winner = next(role for role in CP2_PREFERENCE if role in calibration_survivors)
        decision_reason = "eligible_arm_tie_break"
    decision = {
        "base_loss_zero": base_loss == 0,
        "candidates": candidates,
        "eligible_roles": eligible_roles,
        "minimum_eligible_loss": (
            _cp2_decimal_string(minimum_loss) if minimum_loss is not None else None
        ),
        "tie_set": tie_set,
        "tie_break": {
            "feature_survivors": feature_survivors,
            "calibration_survivors": calibration_survivors,
            "preference_order": list(CP2_PREFERENCE),
        },
        "winner": winner,
        "decision_reason": decision_reason,
    }
    return winner, decision


def _cp2_adjudicate_exact(
    metrics_by_role: Sequence[Mapping[str, Any]],
) -> tuple[str, Mapping[str, Any]]:
    loss_values = [
        str(entry["loss_sum"])
        for entry in metrics_by_role
    ] + [
        str(fold["loss_sum"])
        for entry in metrics_by_role
        for fold in entry["folds"]
    ]
    with localcontext() as context:
        context.prec = _cp2_precision(loss_values, term_count=1000)
        context.Emax = max(context.Emax, context.prec * 2)
        context.Emin = min(context.Emin, -context.prec * 2)
        return _cp2_adjudicate_exact_inner(metrics_by_role)


def cp2_blind_adjudicate(
    integration_support_root_input: str, blind_review_id: str
) -> tuple[Mapping[str, Any], bool]:
    support_root = _cp2_support_from_input(
        integration_support_root_input, blind_review_id
    )
    attempt_path = support_root / CP2_ADJUDICATE_ATTEMPT_FILENAME
    _cp2_create_attempt(
        attempt_path, "cp2_blind_adjudicate_attempt", blind_review_id
    )
    attempt, _ = _load_json(attempt_path)
    (
        reveal,
        reveal_path,
        reveal_hash,
        source_manifest,
        selection,
        rows_by_role,
        anonymous_metrics,
    ) = _cp2_validate_reveal(support_root, blind_review_id, repo_root=None)
    if parse_utc(attempt["started_at_utc"]) <= parse_utc(reveal["recorded_at_utc"]):
        fail(
            "Adjudication attempt must begin strictly after the immutable reveal; "
            "the blind ID is now spent"
        )
    freeze_path = support_root / CP2_FREEZE_FILENAME
    freeze, freeze_raw = _load_json(freeze_path)
    freeze_hash = _sha256_bytes(freeze_raw)
    mapping, _ = _load_json(support_root / CP2_REVEALED_MAPPING_FILENAME)
    mapping_by_label = {entry["label"]: entry["role"] for entry in mapping["mapping"]}
    anonymous_by_label = {entry["label"]: entry for entry in anonymous_metrics}
    mapped_metrics: list[Mapping[str, Any]] = []
    for role in CP2_SEMANTIC_ROLES:
        label = next(label for label, mapped_role in mapping_by_label.items() if mapped_role == role)
        anonymous = anonymous_by_label[label]
        mapped_metrics.append(
            {
                "role": role,
                **{key: value for key, value in anonymous.items() if key != "label"},
            }
        )
    mapped_metrics = list(
        _cp2_validate_metric_entries(
            mapped_metrics, identity_field="role", field="adjudication.metrics_by_role"
        )
    )
    semantic_rows: list[dict[str, str]] = []
    for role in CP2_SEMANTIC_ROLES:
        semantic_rows.extend(
            {"role": role, **row} for row in rows_by_role[role]
        )
    recomputed_by_role = _cp2_metrics(semantic_rows, identity_field="role")
    if not _cp2_metric_entries_equal(mapped_metrics, recomputed_by_role):
        fail("Mapped anonymous metrics do not equal Integration-owned source recomputation")
    winner, decision = _cp2_adjudicate_exact(recomputed_by_role)
    declaration_metrics_match = _cp2_metric_entries_equal(
        selection["metrics_by_role"], recomputed_by_role
    )
    winner_match = selection["selected_role"] == winner
    match = declaration_metrics_match and winner_match
    reasons: list[str] = []
    if not declaration_metrics_match:
        reasons.append("selection_metrics_mismatch")
    if not winner_match:
        reasons.append("winner_mismatch")
    reason = "match" if match else "+".join(reasons)
    recorded_at = _timestamp_after(attempt["started_at_utc"])
    record = {
        "record_type": "cp2_blind_adjudication",
        "schema_version": CP2_BLIND_SCHEMA_VERSION,
        "checkpoint": "CP-2",
        "blind_review_id": blind_review_id,
        "candidate": reveal["candidate"],
        "freeze": {"path": str(freeze_path), "sha256": freeze_hash},
        "reveal": {"path": str(reveal_path), "sha256": reveal_hash},
        "source_manifest": reveal["source_manifest"],
        "selection_declaration": reveal["selection_declaration"],
        "metrics_by_role": recomputed_by_role,
        "decision": decision,
        "computed_winner": winner,
        "declared_winner": selection["selected_role"],
        "declaration_metrics_match": declaration_metrics_match,
        "match": match,
        "reason": reason,
        "recorded_at_utc": recorded_at,
    }
    output_path = support_root / CP2_ADJUDICATION_FILENAME
    output_hash = _atomic_json_write(output_path, record, create=True)
    result = dict(record)
    result["artifact"] = {"path": str(output_path), "sha256": output_hash}
    return result, match


def _validate_canonical_verdict_location(
    verdict_path: Path, checkpoint: str, run_id: str
) -> tuple[Path, Path, Path]:
    if verdict_path.name != "critic-verdict.json":
        fail("Critic verdict filename must be critic-verdict.json")
    parent = verdict_path.parent
    if parent.name != run_id or parent.parent.name != checkpoint:
        fail(
            "Critic verdict must live under "
            ".gauntlet/evidence/<checkpoint>/<run-id>/critic-verdict.json"
        )
    repo_root, checkpoint_root, support_root = _evidence_context_from_run_path(
        parent, checkpoint, run_id
    )
    expected_names = {"integrity-manifest.json", "critic-verdict.json"}
    try:
        entries = list(parent.iterdir())
    except OSError as exc:
        fail(f"Cannot enumerate immutable Critic run directory {parent}: {exc}")
    actual_names = {entry.name for entry in entries}
    missing = sorted(expected_names - actual_names)
    if missing:
        fail(
            "Critic run directory must contain integrity-manifest.json and "
            f"critic-verdict.json (missing={missing})"
        )
    for entry in entries:
        if entry.is_symlink() or not entry.is_file():
            fail(f"Critic run artifact must be a regular non-symlink file: {entry}")
    return repo_root, checkpoint_root, support_root


def _validate_integrity_binding(
    value: Any,
    *,
    verdict_path: Path,
    run_id: str,
    checkpoint: str,
    candidate_sha: str,
    candidate_tree: str,
    repo_root: Path,
) -> Mapping[str, Any]:
    value = require_exact_keys(
        value, "integrity_manifest", required=("path", "sha256")
    )
    manifest_path = require_absolute_path(value["path"], "integrity_manifest.path")
    expected_hash = require_sha256(value["sha256"], "integrity_manifest.sha256")
    canonical_expected = verdict_path.parent / "integrity-manifest.json"
    if manifest_path != canonical_expected:
        fail(f"integrity_manifest.path must be {canonical_expected}")
    if not manifest_path.is_file():
        fail(f"Integrity manifest does not exist: {manifest_path}")
    manifest, manifest_raw = _load_json(manifest_path)
    actual_hash = _sha256_bytes(manifest_raw)
    if actual_hash != expected_hash:
        fail(
            "Final integrity manifest SHA-256 mismatch: "
            f"expected {expected_hash}, got {actual_hash}"
        )
    manifest = _validate_integrity_record_shape(manifest, require_verify=True)
    if manifest["run_id"] != run_id:
        fail("Integrity manifest run_id does not match the verdict")
    if manifest["checkpoint"] != checkpoint:
        fail("Integrity manifest checkpoint does not match the verdict")
    if manifest["evidence_run_path"] != str(verdict_path.parent):
        fail("Integrity manifest evidence_run_path does not match the verdict run")
    if manifest["candidate_sha"] != candidate_sha:
        fail("Integrity manifest candidate_sha does not match the verdict")
    if manifest["candidate_tree"] != candidate_tree:
        fail("Integrity manifest candidate_tree does not match the verdict")
    for tool_name, relative_path in (
        ("snapshot_helper", SNAPSHOT_HELPER_RELATIVE_PATH),
        ("protocol_helper", PROTOCOL_HELPER_RELATIVE_PATH),
    ):
        committed_bytes = _git_bytes(
            repo_root, ["show", f"{candidate_sha}:{relative_path}"]
        )
        committed_hash = _sha256_bytes(committed_bytes)
        manifest_hash = manifest["create"]["tools"][tool_name]["sha256"]
        if committed_hash != manifest_hash:
            fail(
                f"Committed {relative_path} does not match integrity manifest hash: "
                f"{committed_hash} != {manifest_hash}"
            )
    return manifest


def _validate_verdict_schema_binding(
    value: Any, repo_root: Path, candidate_sha: str
) -> str:
    value = require_exact_keys(
        value, "verdict_schema", required=("repo_relative_path", "sha256")
    )
    if value["repo_relative_path"] != VERDICT_SCHEMA_RELATIVE_PATH:
        fail(
            "verdict_schema.repo_relative_path must be "
            f"{VERDICT_SCHEMA_RELATIVE_PATH}"
        )
    expected = require_sha256(value["sha256"], "verdict_schema.sha256")
    raw = _git_bytes(
        repo_root, ["show", f"{candidate_sha}:{VERDICT_SCHEMA_RELATIVE_PATH}"]
    )
    actual = _sha256_bytes(raw)
    if actual != expected:
        fail(f"Committed verdict schema SHA-256 mismatch: expected {expected}, got {actual}")
    try:
        schema = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"Committed verdict schema is invalid JSON: {exc}")
    if not isinstance(schema, dict):
        fail("Committed verdict schema root must be an object")
    if schema.get("$id") != "https://pjm.local/schemas/critic-verdict.schema.json":
        fail("Committed verdict schema has an unexpected $id")
    if schema.get("x-validator") != "scripts/gauntlet_protocol.py@1.0":
        fail("Committed verdict schema and protocol validator versions disagree")
    return actual


def _validate_cp2_blind_review(
    value: Any,
    *,
    support_root: Path,
    repo_root: Path,
    candidate_sha: str,
    candidate_tree: str,
    checkpoint: str,
    recorded_at_utc: str,
) -> Mapping[str, Any]:
    if checkpoint != "CP-2":
        fail("blind_review is valid only on a CP-2 component verdict")
    value = require_exact_keys(
        value, "blind_review", required=CP2_BLIND_REVIEW_REQUIRED_FIELDS
    )
    blind_review_id = require_identifier(
        value["blind_review_id"], "blind_review.blind_review_id"
    )
    expected_names = {
        "public_manifest": CP2_PUBLIC_MANIFEST_FILENAME,
        "commitment": CP2_COMMITMENT_FILENAME,
        "preparation_receipt": CP2_PREPARATION_RECEIPT_FILENAME,
        "metrics": CP2_METRICS_FILENAME,
    }
    paths: dict[str, Path] = {}
    for name, filename in expected_names.items():
        path, _ = _cp2_validate_absolute_binding(
            value[name], f"blind_review.{name}", ownership_root=support_root
        )
        if path.name != filename:
            fail(f"blind_review.{name}.path must end in {filename}")
        paths[name] = path
    schema = require_exact_keys(
        value["protocol_schema"],
        "blind_review.protocol_schema",
        required=CP2_REPO_BLOB_BINDING_REQUIRED_FIELDS,
    )
    if schema["repo_relative_path"] != CP2_BLIND_SCHEMA_RELATIVE_PATH:
        fail("blind_review.protocol_schema.repo_relative_path mismatch")
    expected_schema_hash = require_sha256(
        schema["sha256"], "blind_review.protocol_schema.sha256"
    )
    schema_raw = _git_bytes(
        repo_root, ["show", f"{candidate_sha}:{CP2_BLIND_SCHEMA_RELATIVE_PATH}"]
    )
    if _sha256_bytes(schema_raw) != expected_schema_hash:
        fail("blind_review protocol schema does not match the committed candidate blob")
    metrics, metrics_path, metrics_hash = _cp2_validate_metrics_record(
        support_root, blind_review_id
    )
    if paths["metrics"] != metrics_path or value["metrics"]["sha256"] != metrics_hash:
        fail("blind_review.metrics does not bind the canonical recomputation record")
    if metrics["candidate"] != {
        "commit_sha": candidate_sha,
        "tree_sha": candidate_tree,
    }:
        fail("blind_review metrics candidate mismatch")
    if metrics["blind_schema"] != schema:
        fail("blind_review protocol schema and metrics schema differ")
    command = require_string(value["recompute_command"], "blind_review.recompute_command")
    if command != metrics["recompute_command"]:
        fail("blind_review.recompute_command must equal the safe metrics command")
    if value["identity_decision"] != "NOT_PERFORMED":
        fail("blind_review.identity_decision must be NOT_PERFORMED")
    if parse_utc(recorded_at_utc) <= parse_utc(metrics["recorded_at_utc"]):
        fail("Blind verdict must be recorded strictly after blind metrics")
    return value


def _cp2_validate_adjudication_record(
    support_root: Path, blind_review_id: str, *, repo_root: Path
) -> tuple[Mapping[str, Any], Path, str]:
    attempt_path = support_root / CP2_ADJUDICATE_ATTEMPT_FILENAME
    attempt, _ = _load_json(attempt_path)
    attempt = require_exact_keys(
        attempt,
        "adjudicate_attempt",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "started_at_utc",
        ),
    )
    if (
        attempt["record_type"] != "cp2_blind_adjudicate_attempt"
        or attempt["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or attempt["checkpoint"] != "CP-2"
        or attempt["blind_review_id"] != blind_review_id
    ):
        fail("adjudicate_attempt identity mismatch")
    attempt_time = require_utc(
        attempt["started_at_utc"], "adjudicate_attempt.started_at_utc"
    )
    (
        reveal,
        reveal_path,
        reveal_hash,
        _,
        selection,
        rows_by_role,
        anonymous_metrics,
    ) = _cp2_validate_reveal(
        support_root, blind_review_id, repo_root=repo_root
    )
    freeze_path = support_root / CP2_FREEZE_FILENAME
    freeze_raw = _read_single_link_file(freeze_path, "CP-2 freeze")
    freeze_hash = _sha256_bytes(freeze_raw)
    mapping, _ = _load_json(support_root / CP2_REVEALED_MAPPING_FILENAME)
    mapping_by_label = {entry["label"]: entry["role"] for entry in mapping["mapping"]}
    anonymous_by_label = {entry["label"]: entry for entry in anonymous_metrics}
    mapped_metrics: list[Mapping[str, Any]] = []
    for role in CP2_SEMANTIC_ROLES:
        label = next(label for label in CP2_LABELS if mapping_by_label[label] == role)
        entry = anonymous_by_label[label]
        mapped_metrics.append(
            {"role": role, **{name: item for name, item in entry.items() if name != "label"}}
        )
    semantic_rows: list[dict[str, str]] = []
    for role in CP2_SEMANTIC_ROLES:
        semantic_rows.extend({"role": role, **row} for row in rows_by_role[role])
    recomputed = _cp2_metrics(semantic_rows, identity_field="role")
    if not _cp2_metric_entries_equal(mapped_metrics, recomputed):
        fail("Adjudication mapping does not reproduce semantic source metrics")
    winner, decision = _cp2_adjudicate_exact(recomputed)
    declaration_metrics_match = _cp2_metric_entries_equal(
        selection["metrics_by_role"], recomputed
    )
    winner_match = selection["selected_role"] == winner
    expected_match = declaration_metrics_match and winner_match
    reasons: list[str] = []
    if not declaration_metrics_match:
        reasons.append("selection_metrics_mismatch")
    if not winner_match:
        reasons.append("winner_mismatch")
    expected_reason = "match" if expected_match else "+".join(reasons)
    path = support_root / CP2_ADJUDICATION_FILENAME
    record, raw = _load_json(path)
    digest = _sha256_bytes(raw)
    record = require_exact_keys(
        record,
        "adjudication",
        required=(
            "record_type",
            "schema_version",
            "checkpoint",
            "blind_review_id",
            "candidate",
            "freeze",
            "reveal",
            "source_manifest",
            "selection_declaration",
            "metrics_by_role",
            "decision",
            "computed_winner",
            "declared_winner",
            "declaration_metrics_match",
            "match",
            "reason",
            "recorded_at_utc",
        ),
    )
    if (
        record["record_type"] != "cp2_blind_adjudication"
        or record["schema_version"] != CP2_BLIND_SCHEMA_VERSION
        or record["checkpoint"] != "CP-2"
        or record["blind_review_id"] != blind_review_id
        or record["candidate"] != reveal["candidate"]
    ):
        fail("adjudication identity/candidate mismatch")
    if record["freeze"] != {"path": str(freeze_path), "sha256": freeze_hash}:
        fail("adjudication.freeze binding mismatch")
    if record["reveal"] != {"path": str(reveal_path), "sha256": reveal_hash}:
        fail("adjudication.reveal binding mismatch")
    if record["source_manifest"] != reveal["source_manifest"]:
        fail("adjudication.source_manifest binding mismatch")
    if record["selection_declaration"] != reveal["selection_declaration"]:
        fail("adjudication.selection_declaration binding mismatch")
    if not _cp2_metric_entries_equal(record["metrics_by_role"], recomputed):
        fail("adjudication.metrics_by_role mismatch")
    if not _json_exact_equal(record["decision"], decision):
        fail("adjudication decision trace mismatch")
    expected_scalars = {
        "computed_winner": winner,
        "declared_winner": selection["selected_role"],
        "declaration_metrics_match": declaration_metrics_match,
        "match": expected_match,
        "reason": expected_reason,
    }
    for name, expected in expected_scalars.items():
        if not _json_exact_equal(record[name], expected):
            fail(f"adjudication.{name} mismatch")
    recorded_at = require_utc(record["recorded_at_utc"], "adjudication.recorded_at_utc")
    if not (
        parse_utc(reveal["recorded_at_utc"])
        < parse_utc(attempt_time)
        < parse_utc(recorded_at)
    ):
        fail("reveal→adjudicate-attempt→adjudication chronology is not strictly ordered")
    return record, path, digest


def _validate_reviewed_paths(value: Any, *, repo_root: Path, candidate_sha: str) -> list[str]:
    """Candidate-tree paths this review actually covers.

    These are what make staleness computable: a later candidate only invalidates
    this verdict if it touched one of these paths.
    """
    if not isinstance(value, list) or not value:
        fail("reviewed_paths must be a non-empty array of repository-relative paths")
    seen: set[str] = set()
    for index, entry in enumerate(value):
        field = f"reviewed_paths[{index}]"
        path = require_string(entry, field)
        if not CP2_SAFE_REPO_PATH_RE.match(path):
            fail(f"{field} must be a safe repository-relative path: {path}")
        if path in seen:
            fail(f"Duplicate reviewed path: {path}")
        seen.add(path)
    listing = _git(
        repo_root,
        ["ls-tree", "-r", "--name-only", "--full-tree", candidate_sha],
    ).splitlines()
    tracked = set(listing)
    for path in seen:
        prefix = path.rstrip("/") + "/"
        if path not in tracked and not any(item.startswith(prefix) for item in tracked):
            fail(
                f"reviewed_paths entry {path} does not exist in the candidate tree "
                f"at {candidate_sha}"
            )
    return sorted(seen)


def _component_is_current(
    *,
    repo_root: Path,
    component_sha: str,
    final_sha: str,
    reviewed_paths: Sequence[str],
) -> tuple[bool, list[str]]:
    """A component verdict survives a later candidate iff nothing it reviewed changed."""
    if component_sha == final_sha:
        return True, []
    try:
        merge_base = _git(repo_root, ["merge-base", component_sha, final_sha])
    except ProtocolError:
        merge_base = ""
    if merge_base != component_sha:
        return False, ["<component candidate is not an ancestor of the final candidate>"]
    changed = _git(
        repo_root,
        ["diff", "--name-only", f"{component_sha}..{final_sha}", "--", *reviewed_paths],
    ).splitlines()
    return (not changed), changed


def _validate_component_bindings(
    value: Any,
    *,
    repo_root: Path,
    candidate_sha: str,
    candidate_tree: str,
    checkpoint: str,
    plan: Mapping[str, Any],
    integration_recorded_at: str,
    integration_path: Path,
    checkpoint_root: Path,
    seen: set[Path],
) -> list[tuple[Mapping[str, Any], Mapping[str, Any], str]]:
    if not isinstance(value, list) or not value:
        fail("component_verdicts must be a non-empty array for Integration records")
    pieces: set[str] = set()
    paths: set[Path] = set()
    validated: list[tuple[Mapping[str, Any], Mapping[str, Any], str]] = []
    for index, binding in enumerate(value):
        field = f"component_verdicts[{index}]"
        binding = require_exact_keys(
            binding,
            field,
            required=COMPONENT_BINDING_REQUIRED_FIELDS,
        )
        piece = require_identifier(binding["piece"], f"{field}.piece")
        component_path = require_absolute_path(binding["path"], f"{field}.path")
        try:
            component_path = component_path.resolve(strict=True)
        except OSError as exc:
            fail(f"Cannot resolve {field}.path {component_path}: {exc}")
        if not _is_within(component_path, checkpoint_root):
            fail(f"{field}.path must live under {checkpoint_root}")
        expected_hash = require_sha256(binding["sha256"], f"{field}.sha256")
        bound_sha = require_git_sha(binding["candidate_sha"], f"{field}.candidate_sha")
        bound_tree = require_git_sha(
            binding["candidate_tree"], f"{field}.candidate_tree"
        )
        if piece in pieces:
            fail(f"Duplicate component piece: {piece}")
        if component_path in paths:
            fail(f"Duplicate component verdict path: {component_path}")
        pieces.add(piece)
        paths.add(component_path)
        # Staleness is computed, not assumed.  A component verdict taken at an
        # earlier candidate still binds if the final candidate changed nothing it
        # reviewed; otherwise it is stale and that Critic must rerun.
        bound_reviewed = _validate_reviewed_paths(
            binding["reviewed_paths"],
            repo_root=repo_root,
            candidate_sha=bound_sha,
        )
        current, changed = _component_is_current(
            repo_root=repo_root,
            component_sha=bound_sha,
            final_sha=candidate_sha,
            reviewed_paths=bound_reviewed,
        )
        if not current:
            fail(
                f"{field} is stale: the final candidate changed reviewed paths "
                f"{changed}; rerun this component Critic"
            )
        if component_path == integration_path:
            fail(f"{field}.path may not reference the Integration verdict itself")
        if not component_path.is_file():
            fail(f"Component verdict does not exist: {component_path}")
        component_record, actual_hash = validate_verdict_file(component_path, _seen=seen)
        if actual_hash != expected_hash:
            fail(f"{field}.sha256 mismatch: expected {expected_hash}, got {actual_hash}")
        if component_record["record_type"] != COMPONENT_RECORD_TYPE:
            fail(f"{field}.path must reference a component Critic verdict")
        if component_record["verdict"] != "PASS":
            fail(f"{field}.path must reference a PASS component verdict")
        if component_record["piece"] != piece:
            fail(f"{field}.piece does not match the referenced verdict piece")
        if component_record["checkpoint"] != checkpoint:
            fail(f"{field}.path references a different checkpoint")
        component_plan = component_record["plan"]
        if (
            component_plan["filename"] != plan["filename"]
            or component_plan["version"] != plan["version"]
            or component_plan["sha256"] != plan["sha256"]
        ):
            fail(f"{field}.path references a different plan filename/version/hash")
        if parse_utc(component_record["recorded_at_utc"]) > parse_utc(
            integration_recorded_at
        ):
            fail(f"{field}.path was recorded after the Integration verdict")
        component_candidate = component_record["candidate"]
        if (
            component_candidate["commit_sha"] != bound_sha
            or component_candidate["tree_sha"] != bound_tree
        ):
            fail(f"{field} does not match the referenced verdict's candidate SHA/tree")
        if sorted(component_record["reviewed_paths"]) != bound_reviewed:
            fail(f"{field}.reviewed_paths does not match the referenced verdict")
        validated.append((binding, component_record, actual_hash))
    return validated


def _validate_cp2_integration_adjudication(
    value: Any,
    *,
    support_root: Path,
    repo_root: Path,
    candidate_sha: str,
    candidate_tree: str,
    integration_verdict: str,
    integration_recorded_at: str,
    component_records: Sequence[
        tuple[Mapping[str, Any], Mapping[str, Any], str]
    ],
) -> Mapping[str, Any]:
    value = require_exact_keys(
        value,
        "blind_adjudication",
        required=CP2_BLIND_ADJUDICATION_REQUIRED_FIELDS,
    )
    blind_review_id = require_identifier(
        value["blind_review_id"], "blind_adjudication.blind_review_id"
    )
    filename_by_name = {
        "freeze": CP2_FREEZE_FILENAME,
        "reveal": CP2_REVEAL_FILENAME,
        "adjudication": CP2_ADJUDICATION_FILENAME,
    }
    bound_paths: dict[str, Path] = {}
    for name, filename in filename_by_name.items():
        path, _ = _cp2_validate_absolute_binding(
            value[name], f"blind_adjudication.{name}", ownership_root=support_root
        )
        if path.name != filename:
            fail(f"blind_adjudication.{name}.path must end in {filename}")
        bound_paths[name] = path
    selected_role = value["selected_role"]
    if selected_role not in CP2_SEMANTIC_ROLES:
        fail("blind_adjudication.selected_role is not canonical")
    declaration = require_exact_keys(
        value["selection_declaration"],
        "blind_adjudication.selection_declaration",
        required=CP2_REPO_BLOB_BINDING_REQUIRED_FIELDS,
    )
    if declaration["repo_relative_path"] != CP2_SELECTION_DECLARATION_RELATIVE_PATH:
        fail("blind_adjudication.selection_declaration.repo_relative_path mismatch")
    declaration_hash = require_sha256(
        declaration["sha256"], "blind_adjudication.selection_declaration.sha256"
    )
    committed_declaration = _git_bytes(
        repo_root,
        ["show", f"{candidate_sha}:{CP2_SELECTION_DECLARATION_RELATIVE_PATH}"],
    )
    if _sha256_bytes(committed_declaration) != declaration_hash:
        fail("blind_adjudication selection declaration is not the committed blob")
    adjudication, adjudication_path, adjudication_hash = (
        _cp2_validate_adjudication_record(
            support_root, blind_review_id, repo_root=repo_root
        )
    )
    if (
        bound_paths["adjudication"] != adjudication_path
        or value["adjudication"]["sha256"] != adjudication_hash
    ):
        fail("blind_adjudication.adjudication binding mismatch")
    if adjudication["candidate"] != {
        "commit_sha": candidate_sha,
        "tree_sha": candidate_tree,
    }:
        fail("blind_adjudication candidate SHA/tree mismatch")
    if value["freeze"] != adjudication["freeze"]:
        fail("blind_adjudication.freeze binding mismatch")
    if value["reveal"] != adjudication["reveal"]:
        fail("blind_adjudication.reveal binding mismatch")
    if selected_role != adjudication["computed_winner"]:
        fail("blind_adjudication.selected_role must equal computed_winner")
    if integration_verdict == "PASS" and adjudication["match"] is not True:
        fail("CP-2 Integration PASS requires adjudication.match=true")
    if parse_utc(integration_recorded_at) <= parse_utc(
        adjudication["recorded_at_utc"]
    ):
        fail("Integration verdict must be recorded strictly after adjudication")
    blind_components = [
        (binding, record, digest)
        for binding, record, digest in component_records
        if "blind_review" in record
    ]
    if len(blind_components) != 1:
        fail("CP-2 Integration must rely on exactly one Blind component verdict")
    binding, blind_component, component_digest = blind_components[0]
    blind_review = blind_component["blind_review"]
    if blind_review["blind_review_id"] != blind_review_id:
        fail("Integration Blind component uses a different blind_review_id")
    freeze, _ = _load_json(bound_paths["freeze"])
    if (
        freeze["blind_component"]["verdict"]["path"] != binding["path"]
        or freeze["blind_component"]["verdict"]["sha256"] != component_digest
    ):
        fail("Freeze must cite the one canonical relied-on Blind component verdict")
    for name in (
        "public_manifest",
        "commitment",
        "preparation_receipt",
        "metrics",
    ):
        if blind_review[name]["sha256"] != freeze[name]["sha256"]:
            fail(f"Frozen {name} bytes differ from the canonical Blind component binding")
    return value


def validate_verdict_file(
    verdict_input: str | Path, *, _seen: set[Path] | None = None
) -> tuple[Mapping[str, Any], str]:
    verdict_path = require_absolute_path(str(verdict_input), "verdict")
    if verdict_path.is_symlink() or not verdict_path.is_file():
        fail(f"Critic verdict does not exist: {verdict_path}")
    try:
        resolved_verdict_path = verdict_path.resolve(strict=True)
    except OSError as exc:
        fail(f"Cannot resolve Critic verdict path {verdict_path}: {exc}")
    if verdict_path != resolved_verdict_path:
        fail(
            "Critic verdict path must be canonical and traverse no symlink: "
            f"{verdict_path} -> {resolved_verdict_path}"
        )
    verdict_path = resolved_verdict_path
    seen = set() if _seen is None else _seen
    if verdict_path in seen:
        fail(f"Cyclic Critic verdict reference: {verdict_path}")
    seen.add(verdict_path)
    try:
        record, raw = _load_json(verdict_path)
        verdict_sha256 = _sha256_bytes(raw)
        record_type = record.get("record_type")
        if record_type == INTEGRATION_RECORD_TYPE:
            record = require_exact_keys(
                record,
                "verdict",
                required=(*VERDICT_BASE_REQUIRED_FIELDS, "component_verdicts"),
                optional=("blind_adjudication",),
            )
        elif record_type == COMPONENT_RECORD_TYPE:
            record = require_exact_keys(
                record,
                "verdict",
                required=VERDICT_BASE_REQUIRED_FIELDS,
                optional=("blind_review",),
            )
        else:
            fail(
                "record_type must be component_critic_verdict or "
                "integration_critic_verdict"
            )
        if record["schema_version"] != SCHEMA_VERSION:
            fail("Verdict has an unsupported schema_version")
        run_id = require_identifier(record["run_id"], "run_id")
        checkpoint = require_identifier(record["checkpoint"], "checkpoint")
        piece = require_identifier(record["piece"], "piece")
        require_identifier(record["critic_id"], "critic_id")
        if record["verdict"] not in ("PASS", "FAIL"):
            fail("verdict must be PASS or FAIL")
        repo_root, checkpoint_root, support_root = _validate_canonical_verdict_location(
            verdict_path, checkpoint, run_id
        )

        candidate = require_exact_keys(
            record["candidate"],
            "candidate",
            required=CANDIDATE_REQUIRED_FIELDS,
        )
        candidate_sha = require_git_sha(candidate["commit_sha"], "candidate.commit_sha")
        candidate_tree = require_git_sha(candidate["tree_sha"], "candidate.tree_sha")
        if len(candidate_sha) != len(candidate_tree):
            fail("candidate.commit_sha and candidate.tree_sha use different object formats")
        _, actual_tree = _validate_full_commit(repo_root, candidate_sha)
        if actual_tree != candidate_tree:
            fail(
                "candidate.tree_sha does not match candidate.commit_sha^{tree}: "
                f"expected {actual_tree}, got {candidate_tree}"
            )
        expected_ref = evidence_ref_name(checkpoint, run_id, piece)
        if candidate["evidence_ref"] != expected_ref:
            fail(f"candidate.evidence_ref must be exactly {expected_ref}")
        actual_ref_sha = _git(
            repo_root, ["show-ref", "--verify", "--hash", expected_ref]
        )
        if actual_ref_sha != candidate_sha:
            fail(
                f"candidate.evidence_ref resolves to {actual_ref_sha}, "
                f"not {candidate_sha}"
            )
        _validate_verdict_schema_binding(
            record["verdict_schema"], repo_root, candidate_sha
        )

        _validate_hash_or_na(
            record["artifact"],
            "artifact",
            require_path=True,
            support_root=support_root,
        )
        _validate_plan(
            record["plan"], repo_root=repo_root, candidate_sha=candidate_sha
        )
        _validate_inputs(record["inputs"], support_root)
        _validate_commands(record["commands"], support_root)
        require_string(record["expected_output"], "expected_output")
        require_string(record["tolerance"], "tolerance")
        manifest = _validate_integrity_binding(
            record["integrity_manifest"],
            verdict_path=verdict_path,
            run_id=run_id,
            checkpoint=checkpoint,
            candidate_sha=candidate_sha,
            candidate_tree=candidate_tree,
            repo_root=repo_root,
        )
        _validate_evidence(record["evidence"], support_root)
        _validate_reviewed_paths(
            record["reviewed_paths"], repo_root=repo_root, candidate_sha=candidate_sha
        )
        require_string(record["largest_meaningful_gap"], "largest_meaningful_gap")
        require_string(record["next_acceptance_test"], "next_acceptance_test")
        recorded_at = require_utc(record["recorded_at_utc"], "recorded_at_utc")
        if parse_utc(recorded_at) < parse_utc(
            manifest["verify"]["recorded_at_utc"]
        ):
            fail("Verdict recorded_at_utc precedes the post-review integrity verify")
        if record_type == COMPONENT_RECORD_TYPE and "blind_review" in record:
            _validate_cp2_blind_review(
                record["blind_review"],
                support_root=support_root,
                repo_root=repo_root,
                candidate_sha=candidate_sha,
                candidate_tree=candidate_tree,
                checkpoint=checkpoint,
                recorded_at_utc=recorded_at,
            )
            _cp2_assert_identity_free_value(record, "Blind component verdict")
        if record_type == INTEGRATION_RECORD_TYPE:
            component_records = _validate_component_bindings(
                record["component_verdicts"],
                repo_root=repo_root,
                candidate_sha=candidate_sha,
                candidate_tree=candidate_tree,
                checkpoint=checkpoint,
                plan=record["plan"],
                integration_recorded_at=recorded_at,
                integration_path=verdict_path,
                checkpoint_root=checkpoint_root,
                seen=seen,
            )
            if checkpoint == "CP-2":
                if "blind_adjudication" not in record:
                    fail("CP-2 Integration verdict requires blind_adjudication")
                _validate_cp2_integration_adjudication(
                    record["blind_adjudication"],
                    support_root=support_root,
                    repo_root=repo_root,
                    candidate_sha=candidate_sha,
                    candidate_tree=candidate_tree,
                    integration_verdict=record["verdict"],
                    integration_recorded_at=recorded_at,
                    component_records=component_records,
                )
            elif "blind_adjudication" in record:
                fail("blind_adjudication is valid only on a CP-2 Integration verdict")
        final_ref_sha = _git(
            repo_root, ["show-ref", "--verify", "--hash", expected_ref]
        )
        if final_ref_sha != actual_ref_sha:
            fail(f"candidate.evidence_ref changed during verdict validation: {expected_ref}")
        return record, verdict_sha256
    finally:
        seen.remove(verdict_path)


def evidence_ref_name(checkpoint: str, run_id: str, piece: str) -> str:
    checkpoint = require_identifier(checkpoint, "checkpoint")
    run_id = require_identifier(run_id, "run_id")
    piece = require_identifier(piece, "piece")
    ref = f"refs/gauntlet-evidence/{checkpoint}/{run_id}/{piece}"
    result = subprocess.run(
        ["git", "check-ref-format", ref],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip()
        suffix = f": {detail}" if detail else ""
        fail(f"Generated evidence ref is not Git-safe: {ref}{suffix}")
    return ref


def create_evidence_ref(
    repo_root_input: str,
    checkpoint: str,
    run_id: str,
    piece: str,
    candidate_sha: str,
) -> tuple[str, str, str]:
    repo_root = canonical_repo_root(repo_root_input)
    checkpoint = require_identifier(checkpoint, "checkpoint")
    run_id = require_identifier(run_id, "run_id")
    piece = require_identifier(piece, "piece")
    candidate_sha, tree_sha = _validate_full_commit(repo_root, candidate_sha)
    ref = evidence_ref_name(checkpoint, run_id, piece)
    expected_branch = f"refs/heads/gauntlet/{checkpoint}"
    actual_branch = _git(repo_root, ["symbolic-ref", "--quiet", "HEAD"])
    if actual_branch != expected_branch:
        fail(
            "create-ref is Lead-only and requires current branch "
            f"{expected_branch}; got {actual_branch}"
        )
    current_head = _git(repo_root, ["rev-parse", "--verify", "HEAD"])
    if candidate_sha != current_head:
        fail(
            "create-ref requires candidate_sha to equal the current checkpoint HEAD: "
            f"expected {current_head}, got {candidate_sha}"
        )
    command = ["git", "-C", str(repo_root), "update-ref", ref, candidate_sha, ""]
    result = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown git error"
        fail(f"Refusing to create evidence ref {ref}: {detail}")
    return ref, candidate_sha, tree_sha


def verify_evidence_ref(
    repo_root_input: str,
    checkpoint: str,
    run_id: str,
    piece: str,
    candidate_sha: str,
) -> tuple[str, str, str]:
    repo_root = canonical_repo_root(repo_root_input)
    candidate_sha, tree_sha = _validate_full_commit(repo_root, candidate_sha)
    ref = evidence_ref_name(checkpoint, run_id, piece)
    actual = _git(repo_root, ["show-ref", "--verify", "--hash", ref])
    if actual != candidate_sha:
        fail(f"Evidence ref {ref} mismatch: expected {candidate_sha}, got {actual}")
    return ref, candidate_sha, tree_sha


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init-evidence", help="initialize one ignored Critic evidence run directory"
    )
    init_parser.add_argument("--repo-root", required=True)
    init_parser.add_argument("--checkpoint", required=True)
    init_parser.add_argument("--run-id", required=True)

    validate_parser = subparsers.add_parser(
        "validate-verdict", help="validate a Critic verdict and all bound evidence"
    )
    validate_parser.add_argument("--verdict", required=True)

    freeze_parser = subparsers.add_parser(
        "freeze-evidence",
        help="copy a closed checkpoint's verdict records out of ignored .gauntlet/ for committing",
    )
    freeze_parser.add_argument("--repo-root", required=True)
    freeze_parser.add_argument("--checkpoint", required=True)
    freeze_parser.add_argument(
        "--destination", required=True,
        help="repository-relative target, e.g. docs/track-b/evidence/CP-1",
    )

    scaffold_parser = subparsers.add_parser(
        "scaffold-verdict",
        help="emit a verdict skeleton with all tool-derivable fields prefilled",
    )
    for flag in (
        "--repo-root", "--checkpoint", "--run-id", "--piece", "--critic-id",
        "--candidate-sha", "--plan-filename", "--plan-version",
        "--plan-bar-citation", "--plan-bar-excerpt",
    ):
        scaffold_parser.add_argument(flag, required=True)
    scaffold_parser.add_argument(
        "--record-type", default=COMPONENT_RECORD_TYPE,
        choices=[COMPONENT_RECORD_TYPE, INTEGRATION_RECORD_TYPE],
    )
    scaffold_parser.add_argument(
        "--reviewed-path", action="append", required=True, dest="reviewed_paths",
        help="repository-relative path this review covers (repeatable)",
    )

    prepare_parser = subparsers.add_parser(
        "blind-prepare", help="prepare one create-only CP-2 label-blind review"
    )
    prepare_parser.add_argument("--repo-root", required=True)
    prepare_parser.add_argument("--candidate-sha", required=True)
    prepare_parser.add_argument("--blind-review-id", required=True)
    prepare_parser.add_argument("--component-run-id", required=True)

    recompute_parser = subparsers.add_parser(
        "blind-recompute", help="recompute identity-free CP-2 metrics"
    )
    recompute_parser.add_argument("--support-root", required=True)
    recompute_parser.add_argument("--blind-review-id", required=True)

    freeze_parser = subparsers.add_parser(
        "blind-freeze", help="freeze a schema-valid CP-2 Blind PASS"
    )
    freeze_parser.add_argument("--repo-root", required=True)
    freeze_parser.add_argument("--blind-review-id", required=True)
    freeze_parser.add_argument("--component-verdict", required=True)
    freeze_parser.add_argument("--integration-run-id", required=True)
    freeze_parser.add_argument("--integration-piece", required=True)

    reveal_parser = subparsers.add_parser(
        "blind-reveal", help="reveal one frozen CP-2 mapping into Integration"
    )
    reveal_parser.add_argument("--repo-root", required=True)
    reveal_parser.add_argument("--blind-review-id", required=True)
    reveal_parser.add_argument("--integration-run-id", required=True)

    adjudicate_parser = subparsers.add_parser(
        "blind-adjudicate", help="adjudicate CP-2 from Integration-owned copies"
    )
    adjudicate_parser.add_argument("--integration-support-root", required=True)
    adjudicate_parser.add_argument("--blind-review-id", required=True)

    for name, help_text in (
        ("create-ref", "create a new local evidence-retention ref"),
        ("verify-ref", "verify an existing local evidence-retention ref"),
    ):
        ref_parser = subparsers.add_parser(name, help=help_text)
        ref_parser.add_argument("--repo-root", required=True)
        ref_parser.add_argument("--checkpoint", required=True)
        ref_parser.add_argument("--run-id", required=True)
        ref_parser.add_argument("--piece", required=True)
        ref_parser.add_argument("--candidate-sha", required=True)

    manifest_create = subparsers.add_parser("_manifest-create", help=argparse.SUPPRESS)
    manifest_create.add_argument("--manifest", required=True)
    manifest_create.add_argument("--run-id", required=True)
    manifest_create.add_argument("--candidate-sha", required=True)
    manifest_create.add_argument("--candidate-tree", required=True)
    manifest_create.add_argument("--snapshot-path", required=True)
    manifest_create.add_argument("--snapshot-helper-path", required=True)
    manifest_create.add_argument("--snapshot-helper-sha256", required=True)
    manifest_create.add_argument("--protocol-helper-path", required=True)
    manifest_create.add_argument("--protocol-helper-sha256", required=True)

    manifest_verify = subparsers.add_parser("_manifest-verify", help=argparse.SUPPRESS)
    manifest_verify.add_argument("--manifest", required=True)
    manifest_verify.add_argument("--pre-review-sha256", required=True)
    manifest_verify.add_argument("--candidate-sha", required=True)
    manifest_verify.add_argument("--candidate-tree", required=True)
    manifest_verify.add_argument("--snapshot-path", required=True)
    manifest_verify.add_argument("--snapshot-helper-path", required=True)
    manifest_verify.add_argument("--snapshot-helper-sha256", required=True)
    manifest_verify.add_argument("--protocol-helper-path", required=True)
    manifest_verify.add_argument("--protocol-helper-sha256", required=True)
    return parser


def freeze_evidence(
    *, repo_root_input: str, checkpoint: str, destination_relative: str
) -> str:
    """Copy a closed checkpoint's verdict records out of ignored .gauntlet/ so they persist.

    Live evidence must stay outside the candidate tree: adding it mid-checkpoint would
    change the candidate SHA and recursively invalidate the reviews that cite it.  But
    once the checkpoint is terminal the candidate is fixed and pinned by its evidence
    refs, so committing a frozen copy invalidates nothing -- and it is the only thing
    that makes the Return Packet's citations checkable later.

    Run this only after the terminal Return Packet.  It copies each run's
    integrity-manifest.json and critic-verdict.json, re-verifies every hash while
    copying, and writes a manifest of what it froze.
    """
    repo_root = canonical_repo_root(repo_root_input)
    require_identifier(checkpoint, "checkpoint")
    if not CP2_SAFE_REPO_PATH_RE.match(destination_relative):
        fail(f"Destination must be a safe repository-relative path: {destination_relative}")

    evidence_root = repo_root / ".gauntlet" / "evidence" / checkpoint
    if not evidence_root.is_dir():
        fail(f"No evidence root for {checkpoint}: {evidence_root}")
    destination = repo_root / destination_relative
    if destination.exists():
        fail(f"Refusing to overwrite an existing frozen evidence root: {destination}")

    runs: list[dict[str, Any]] = []
    for run_root in sorted(evidence_root.iterdir(), key=lambda item: item.name):
        if not run_root.is_dir() or run_root.name.startswith("_"):
            continue
        verdict_path = run_root / "critic-verdict.json"
        manifest_path = run_root / "integrity-manifest.json"
        if not verdict_path.is_file() or not manifest_path.is_file():
            fail(f"Incomplete Critic run, refusing to freeze: {run_root}")
        record, verdict_hash = validate_verdict_file(verdict_path)
        target = destination / run_root.name
        try:
            target.mkdir(parents=True)
        except OSError as exc:
            fail(f"Cannot create frozen evidence directory {target}: {exc}")
        for name, source, expected in (
            ("critic-verdict.json", verdict_path, verdict_hash),
            ("integrity-manifest.json", manifest_path, sha256_file(manifest_path)),
        ):
            payload = _read_regular_file(source, name)
            if _sha256_bytes(payload) != expected:
                fail(f"{source} changed while freezing; aborting")
            _atomic_bytes_create(target / name, payload, mode=0o644)
        runs.append(
            {
                "run_id": str(record["run_id"]),
                "piece": str(record["piece"]),
                "record_type": str(record["record_type"]),
                "verdict": str(record["verdict"]),
                "candidate_sha": str(record["candidate"]["commit_sha"]),
                "evidence_ref": str(record["candidate"]["evidence_ref"]),
                "critic_verdict_sha256": verdict_hash,
                "integrity_manifest_sha256": sha256_file(manifest_path),
            }
        )
    if not runs:
        fail(f"No complete Critic runs to freeze under {evidence_root}")

    index = {
        "record_type": "frozen_checkpoint_evidence",
        "schema_version": SCHEMA_VERSION,
        "checkpoint": checkpoint,
        "frozen_at_utc": utc_now(),
        "source_root": str(evidence_root),
        "runs": runs,
    }
    _atomic_bytes_create(
        destination / "frozen-evidence.json",
        json.dumps(index, indent=2, sort_keys=True).encode("utf-8") + b"\n",
        mode=0o644,
    )
    print(
        f"Froze {len(runs)} Critic run(s) to {destination}.\n"
        "Commit this directory; it is the durable half of the Return Packet.",
        file=sys.stderr,
    )
    return str(destination)


def scaffold_verdict(
    *,
    repo_root_input: str,
    checkpoint: str,
    run_id: str,
    piece: str,
    critic_id: str,
    record_type: str,
    candidate_sha_input: str,
    plan_filename: str,
    plan_version: str,
    plan_bar_citation: str,
    plan_bar_excerpt: str,
    reviewed_paths: Sequence[str],
) -> str:
    """Emit a verdict skeleton with every tool-derivable field already filled.

    The Critic then supplies only judgement: verdict, expected_output, tolerance,
    largest_meaningful_gap, next_acceptance_test, and the inputs/commands/evidence
    it actually produced.  Hand-transcribing SHAs is the largest avoidable error
    source in the protocol, so the tool computes them.
    """
    repo_root = canonical_repo_root(repo_root_input)
    require_identifier(checkpoint, "checkpoint")
    require_identifier(run_id, "run_id")
    require_identifier(piece, "piece")
    require_identifier(critic_id, "critic_id")
    if record_type not in (COMPONENT_RECORD_TYPE, INTEGRATION_RECORD_TYPE):
        fail(f"Unsupported record_type: {record_type}")
    candidate_sha, candidate_tree = _validate_full_commit(repo_root, candidate_sha_input)

    run_root = repo_root / ".gauntlet" / "evidence" / checkpoint / run_id
    support_root = repo_root / ".gauntlet" / "evidence" / checkpoint / "_support" / run_id
    if not run_root.is_dir():
        fail(f"Run root does not exist; run init-evidence first: {run_root}")
    manifest_path = run_root / "integrity-manifest.json"
    if not manifest_path.is_file():
        fail(f"Integrity manifest does not exist yet: {manifest_path}")

    if not REPO_RELATIVE_MARKDOWN_RE.match(plan_filename):
        fail(f"plan.filename must be a safe repository-relative .md path: {plan_filename}")
    try:
        plan_blob = _git_bytes(repo_root, ["show", f"{candidate_sha}:{plan_filename}"])
    except ProtocolError:
        fail(f"plan.filename is not committed at {candidate_sha}: {plan_filename}")
    if plan_bar_excerpt.encode("utf-8") not in plan_blob:
        fail("plan.bar_excerpt does not occur verbatim in the committed plan blob")

    schema_relative = VERDICT_SCHEMA_RELATIVE_PATH
    schema_blob = _git_bytes(repo_root, ["show", f"{candidate_sha}:{schema_relative}"])

    skeleton: dict[str, Any] = {
        "record_type": record_type,
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "checkpoint": checkpoint,
        "piece": piece,
        "critic_id": critic_id,
        "verdict": "REPLACE_WITH_PASS_OR_FAIL",
        "candidate": {
            "commit_sha": candidate_sha,
            "tree_sha": candidate_tree,
            "evidence_ref": f"refs/gauntlet-evidence/{checkpoint}/{run_id}/{piece}",
        },
        "verdict_schema": {
            "repo_relative_path": schema_relative,
            "sha256": _sha256_bytes(schema_blob),
        },
        "artifact": {"path": "REPLACE_OR_NA", "sha256": "REPLACE_OR_NA"},
        "plan": {
            "filename": plan_filename,
            "version": plan_version,
            "sha256": _sha256_bytes(plan_blob),
            "bar_citation": plan_bar_citation,
            "bar_excerpt": plan_bar_excerpt,
        },
        "inputs": [],
        "commands": [],
        "expected_output": "REPLACE",
        "tolerance": "REPLACE",
        "integrity_manifest": {
            "path": str(manifest_path),
            "sha256": sha256_file(manifest_path),
        },
        "evidence": [],
        "reviewed_paths": _validate_reviewed_paths(
            list(reviewed_paths), repo_root=repo_root, candidate_sha=candidate_sha
        ),
        "largest_meaningful_gap": "REPLACE",
        "next_acceptance_test": "REPLACE",
        "recorded_at_utc": "REPLACE_AFTER_POST_REVIEW_VERIFY",
    }
    if record_type == INTEGRATION_RECORD_TYPE:
        skeleton["component_verdicts"] = []
    print(
        f"# Scaffold for {run_root / 'critic-verdict.json'}\n"
        f"# Support root: {support_root}\n"
        "# Replace every REPLACE* value; fill inputs/commands/evidence from real runs.",
        file=sys.stderr,
    )
    return json.dumps(skeleton, indent=2, sort_keys=False) + "\n"


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    arguments = parser.parse_args(argv)
    try:
        if arguments.command == "init-evidence":
            evidence_root, support_root = initialize_evidence_root(
                arguments.repo_root, arguments.checkpoint, arguments.run_id
            )
            print(f"evidence_root={evidence_root}")
            print(f"support_root={support_root}")
        elif arguments.command == "validate-verdict":
            verdict_path = require_absolute_path(arguments.verdict, "verdict")
            record, verdict_hash = validate_verdict_file(verdict_path)
            print(f"verdict_path={verdict_path.resolve(strict=True)}")
            print(f"verdict_sha256={verdict_hash}")
            print(f"schema_repo_relative_path={VERDICT_SCHEMA_RELATIVE_PATH}")
            print(f"schema_sha256={record['verdict_schema']['sha256']}")
        elif arguments.command == "freeze-evidence":
            print(
                freeze_evidence(
                    repo_root_input=arguments.repo_root,
                    checkpoint=arguments.checkpoint,
                    destination_relative=arguments.destination,
                )
            )
        elif arguments.command == "scaffold-verdict":
            sys.stdout.write(
                scaffold_verdict(
                    repo_root_input=arguments.repo_root,
                    checkpoint=arguments.checkpoint,
                    run_id=arguments.run_id,
                    piece=arguments.piece,
                    critic_id=arguments.critic_id,
                    record_type=arguments.record_type,
                    candidate_sha_input=arguments.candidate_sha,
                    plan_filename=arguments.plan_filename,
                    plan_version=arguments.plan_version,
                    plan_bar_citation=arguments.plan_bar_citation,
                    plan_bar_excerpt=arguments.plan_bar_excerpt,
                    reviewed_paths=arguments.reviewed_paths,
                )
            )
        elif arguments.command == "blind-prepare":
            result = cp2_blind_prepare(
                arguments.repo_root,
                arguments.candidate_sha,
                arguments.blind_review_id,
                arguments.component_run_id,
            )
            print(f"blind_review_id={result['blind_review_id']}")
            for name in (
                "anonymous_csv",
                "public_manifest",
                "commitment",
                "preparation_receipt",
            ):
                print(f"{name}_path={result[name]['path']}")
                print(f"{name}_sha256={result[name]['sha256']}")
        elif arguments.command == "blind-recompute":
            result = cp2_blind_recompute(
                arguments.support_root, arguments.blind_review_id
            )
            print(f"blind_review_id={result['blind_review_id']}")
            print(f"metrics_path={result['metrics']['path']}")
            print(f"metrics_sha256={result['metrics']['sha256']}")
            print(f"recompute_command={result['recompute_command']}")
        elif arguments.command == "blind-freeze":
            result = cp2_blind_freeze(
                arguments.repo_root,
                arguments.blind_review_id,
                arguments.component_verdict,
                arguments.integration_run_id,
                arguments.integration_piece,
            )
            print(f"blind_review_id={result['blind_review_id']}")
            print(f"integration_run_id={result['integration_run_id']}")
            print(f"integration_piece={result['integration_piece']}")
            print(f"integration_evidence_ref={result['integration_evidence_ref']}")
            print(f"integration_support_root={result['integration_support_root']}")
            print(f"freeze_path={result['freeze']['path']}")
            print(f"freeze_sha256={result['freeze']['sha256']}")
        elif arguments.command == "blind-reveal":
            result = cp2_blind_reveal(
                arguments.repo_root,
                arguments.blind_review_id,
                arguments.integration_run_id,
            )
            print(f"blind_review_id={result['blind_review_id']}")
            print(f"reveal_path={result['reveal']['path']}")
            print(f"reveal_sha256={result['reveal']['sha256']}")
        elif arguments.command == "blind-adjudicate":
            result, matched = cp2_blind_adjudicate(
                arguments.integration_support_root, arguments.blind_review_id
            )
            print(f"blind_review_id={result['blind_review_id']}")
            print(f"adjudication_path={result['artifact']['path']}")
            print(f"adjudication_sha256={result['artifact']['sha256']}")
            print(f"computed_winner={result['computed_winner']}")
            print(f"match={'true' if matched else 'false'}")
            if not matched:
                return 2
        elif arguments.command in ("create-ref", "verify-ref"):
            operation = (
                create_evidence_ref
                if arguments.command == "create-ref"
                else verify_evidence_ref
            )
            ref, commit_sha, tree_sha = operation(
                arguments.repo_root,
                arguments.checkpoint,
                arguments.run_id,
                arguments.piece,
                arguments.candidate_sha,
            )
            print(f"evidence_ref={ref}")
            print(f"candidate_sha={commit_sha}")
            print(f"tree_sha={tree_sha}")
        elif arguments.command == "_manifest-create":
            manifest_hash = create_integrity_manifest(
                arguments.manifest,
                arguments.run_id,
                arguments.candidate_sha,
                arguments.candidate_tree,
                arguments.snapshot_path,
                arguments.snapshot_helper_path,
                arguments.snapshot_helper_sha256,
                arguments.protocol_helper_path,
                arguments.protocol_helper_sha256,
            )
            print(manifest_hash)
        elif arguments.command == "_manifest-verify":
            manifest_hash = verify_integrity_manifest(
                arguments.manifest,
                arguments.pre_review_sha256,
                arguments.candidate_sha,
                arguments.candidate_tree,
                arguments.snapshot_path,
                arguments.snapshot_helper_path,
                arguments.snapshot_helper_sha256,
                arguments.protocol_helper_path,
                arguments.protocol_helper_sha256,
            )
            print(manifest_hash)
        else:  # pragma: no cover - argparse enforces the command set.
            parser.error("unknown command")
    except ProtocolError as exc:
        if arguments.command in ("blind-prepare", "blind-recompute"):
            print(
                "ERROR: pre-reveal blind phase failed; preserve the attempt and "
                "allocate a new blind-review ID",
                file=sys.stderr,
            )
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
