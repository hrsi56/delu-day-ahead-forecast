"""Append-only, hash-chained JSONL ledger.

Entries are never rewritten. Each row carries ``entry_index``,
``prev_entry_sha256`` and ``entry_sha256`` (SHA-256 over the row's canonical
JSON with ``entry_sha256`` excluded), which makes the file a tamper-evident
chain: editing any row breaks that row's own hash and every following link.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class LedgerError(RuntimeError):
    """Refusal to write, or a structurally unreadable ledger."""


def canonical_json(entry: dict[str, Any]) -> str:
    """Sorted keys, compact separators - the exact bytes that get hashed."""
    return json.dumps(entry, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def compute_entry_sha256(entry: dict[str, Any]) -> str:
    """SHA-256 of the canonical JSON with the ``entry_sha256`` key excluded."""
    payload = {key: value for key, value in entry.items() if key != "entry_sha256"}
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_entries(ledger_path: Path) -> list[dict[str, Any]]:
    """Read every ledger row. Missing file -> empty list."""
    if not ledger_path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for lineno, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise LedgerError(f"{ledger_path}:{lineno} is not valid JSON: {exc}") from exc
    return entries


def ledger_tail(ledger_path: Path) -> tuple[int, str | None]:
    """``(next entry_index, previous entry_sha256)`` for the next append."""
    entries = read_entries(ledger_path)
    if not entries:
        return 0, None
    return len(entries), entries[-1].get("entry_sha256")


def append_entry(ledger_path: Path, entry: dict[str, Any]) -> dict[str, Any]:
    """Seal ``entry`` with its hash and append it as one JSONL line.

    Strictly append-only: opened in mode ``"a"``, flushed and fsynced. Prior
    lines are never read back for modification and never rewritten.
    """
    sealed = dict(entry)
    sealed["entry_sha256"] = compute_entry_sha256(sealed)
    line = canonical_json(sealed)
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    return sealed


def write_raw_artifact(path: Path, payload: bytes) -> str:
    """Write the raw payload content-addressed, refusing to clobber.

    Identical bytes at the path -> reuse it. Different bytes -> raise, so a
    rerun can never silently replace a prior attempt's evidence.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = path.read_bytes()
        if existing == payload:
            return "reused"
        raise LedgerError(
            f"refusing to overwrite existing raw artifact with different bytes: {path} "
            f"(existing sha256={sha256_bytes(existing)}, new sha256={sha256_bytes(payload)})"
        )
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)
    return "written"


@dataclass
class EntryVerification:
    entry_index: int
    line_number: int
    ok: bool
    problems: list[str]


@dataclass
class VerificationReport:
    ok: bool
    entries: list[EntryVerification]
    problems: list[str]

    @property
    def entry_count(self) -> int:
        return len(self.entries)


def _resolve_artifact(recorded: str, raw_dir: Path, ledger_path: Path) -> Path | None:
    candidates = [Path(recorded)]
    if not Path(recorded).is_absolute():
        candidates.append(ledger_path.parent / recorded)
    candidates.append(raw_dir / Path(recorded).name)
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def verify_ledger(ledger_path: Path, raw_dir: Path) -> VerificationReport:
    """Re-walk the whole ledger: row hashes, chain order, artifact hashes."""
    problems: list[str] = []
    results: list[EntryVerification] = []

    if not ledger_path.exists():
        return VerificationReport(False, [], [f"ledger not found: {ledger_path}"])

    try:
        entries = read_entries(ledger_path)
    except LedgerError as exc:
        return VerificationReport(False, [], [str(exc)])

    if not entries:
        return VerificationReport(False, [], [f"ledger is empty: {ledger_path}"])

    previous_hash: str | None = None
    for position, entry in enumerate(entries):
        entry_problems: list[str] = []
        recorded_hash = entry.get("entry_sha256")
        recomputed = compute_entry_sha256(entry)
        if recorded_hash != recomputed:
            entry_problems.append(
                f"entry_sha256 mismatch: recorded {recorded_hash}, recomputed {recomputed} "
                "(the row was edited after it was written)"
            )

        recorded_index = entry.get("entry_index")
        if recorded_index != position:
            entry_problems.append(
                f"entry_index out of order: recorded {recorded_index}, expected {position}"
            )

        recorded_prev = entry.get("prev_entry_sha256")
        if recorded_prev != previous_hash:
            entry_problems.append(
                f"prev_entry_sha256 chain break: recorded {recorded_prev}, "
                f"expected {previous_hash}"
            )

        artifact = entry.get("raw_artifact_path")
        payload_hash = entry.get("payload_sha256")
        if artifact:
            resolved = _resolve_artifact(artifact, raw_dir, ledger_path)
            if resolved is None:
                entry_problems.append(f"raw artifact missing: {artifact}")
            else:
                actual = sha256_bytes(resolved.read_bytes())
                if actual != payload_hash:
                    entry_problems.append(
                        f"raw artifact hash mismatch for {resolved}: "
                        f"file sha256={actual}, ledger payload_sha256={payload_hash}"
                    )
        elif payload_hash:
            entry_problems.append("payload_sha256 recorded without a raw_artifact_path")

        results.append(
            EntryVerification(
                entry_index=recorded_index if isinstance(recorded_index, int) else position,
                line_number=position + 1,
                ok=not entry_problems,
                problems=entry_problems,
            )
        )
        previous_hash = recorded_hash

    ok = all(result.ok for result in results) and not problems
    return VerificationReport(ok=ok, entries=results, problems=problems)
