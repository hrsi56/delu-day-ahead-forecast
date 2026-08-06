"""Append-only, hash-chained JSONL ledger and a content-addressed raw-artifact
store.

There is no update-by-key path anywhere in this module: the ledger only ever
grows by appending a new line, and the raw-artifact store only ever creates
a new immutable file or verifies an existing one byte-for-byte. Before an
append, the entire existing chain is re-verified from scratch; a corrupted
prior line makes `append_entry` raise instead of silently building on top of
bad data.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import tempfile
from dataclasses import is_dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any

GENESIS_HASH = "0" * 64


def _json_default(obj: Any):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def _canonical_json(obj: dict) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=_json_default)


def _sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _entry_to_dict(entry: Any) -> dict:
    if is_dataclass(entry) and not isinstance(entry, type):
        return dataclasses.asdict(entry)
    return dict(entry)


def _verify_chain(ledger_path: Path) -> tuple[list[str], str]:
    """Read every existing line, recompute and verify its entry_hash against
    prev_entry_hash + its own canonical body, and return (raw_lines,
    final_prev_hash_for_next_append). Raises ValueError on any mismatch."""
    if not ledger_path.exists():
        return [], GENESIS_HASH

    text = ledger_path.read_text(encoding="utf-8")
    lines = [line for line in text.split("\n") if line]
    prev_hash = GENESIS_HASH
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"ledger corrupted: line {i + 1} is not valid JSON") from exc

        stored_hash = obj.get("entry_hash")
        if not stored_hash:
            raise ValueError(f"ledger corrupted: line {i + 1} is missing entry_hash")
        if obj.get("prev_entry_hash") != prev_hash:
            raise ValueError(
                f"ledger corrupted: line {i + 1} prev_entry_hash does not match "
                "the hash of the preceding line; chain is broken"
            )

        body = {k: v for k, v in obj.items() if k != "entry_hash"}
        recomputed = _sha256_hex((prev_hash + _canonical_json(body)).encode("utf-8"))
        if recomputed != stored_hash:
            raise ValueError(
                f"ledger corrupted: line {i + 1} entry_hash does not match its "
                "own content; refusing to append onto a corrupted ledger"
            )
        prev_hash = stored_hash

    return lines, prev_hash


def append_entry(ledger_path: Path | str, entry: Any) -> dict:
    """Verify the existing chain, then append one new hash-chained line for
    `entry` (a LedgerEntry dataclass, or a plain dict of the same shape).

    Returns the exact dict that was written (including the chain fields).
    Raises ValueError if the existing ledger fails chain verification.
    """
    ledger_path = Path(ledger_path)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)

    existing_lines, prev_hash = _verify_chain(ledger_path)

    body = _entry_to_dict(entry)
    body["entry_seq"] = len(existing_lines)
    body["prev_entry_hash"] = prev_hash
    entry_hash = _sha256_hex((prev_hash + _canonical_json(body)).encode("utf-8"))
    body["entry_hash"] = entry_hash

    line = _canonical_json(body)
    with open(ledger_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

    return body


def _looks_like_xml(content: str) -> bool:
    stripped = content.lstrip()
    return stripped.startswith("<?xml") or stripped.startswith("<")


def write_raw_artifact(raw_dir: Path | str, content: str) -> Path:
    """Write `content` into the content-addressed raw store, keyed by its
    own sha256. Idempotent: writing the same content twice returns the same
    path without truncating the existing (read-only) file. If a file already
    exists at that hash with *different* bytes (a sha256 collision, for all
    practical purposes impossible), raise rather than overwrite.

    Written via temp file + atomic rename, then chmod 0o444; no code path in
    this function opens an existing artifact file for writing.
    """
    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)

    data = content.encode("utf-8")
    digest = _sha256_hex(data)
    ext = ".xml" if _looks_like_xml(content) else ".body"
    dest = raw_dir / f"{digest}{ext}"

    if dest.exists():
        existing = dest.read_bytes()
        if existing != data:
            raise ValueError(
                f"raw artifact integrity check failed: {dest} already exists "
                "with different content than the sha256-matching payload "
                "just captured"
            )
        return dest

    fd, tmp_path_str = tempfile.mkstemp(dir=raw_dir, prefix=f".tmp-{digest}-", suffix=ext)
    tmp_path = Path(tmp_path_str)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
        os.replace(tmp_path, dest)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    os.chmod(dest, 0o444)
    return dest
