"""Immutability / hash-chain tests (pure/filesystem, no network). Covers
CP-0 items 1 and 5: append-only, hash-bound, a rerun cannot silently
replace a prior attempt.
"""

import json
import stat
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

from pit_capture import ledger
from pit_capture.capture import LedgerEntry

DELIVERY_DATE = date(2026, 8, 5)


def _make_entry(pulled_at: datetime, status: str = "present_complete") -> LedgerEntry:
    return LedgerEntry(
        source="entsoe",
        document_type="A65",
        process_type="A01",
        domain_eic="10Y1001A1001A82H",
        delivery_date=DELIVERY_DATE,
        gate_at_utc=datetime(2026, 8, 4, 10, 0, tzinfo=timezone.utc),
        pulled_at_utc=pulled_at,
        local_pull_time=pulled_at.isoformat(),
        utc_offset="+02:00",
        http_status=200,
        status=status,
        expected_row_count=96,
        observed_row_count=96,
        completeness_ratio=1.0,
        first_delivery_timestamp=None,
        last_delivery_timestamp=None,
        latest_fully_populated_timestamp=None,
        payload_sha256="a" * 64,
        raw_artifact_path=None,
        qualifying=True,
        qualifying_reason="qualifying",
    )


def test_two_sequential_appends_produce_two_distinct_untouched_lines(tmp_path):
    ledger_path = tmp_path / "ledger.jsonl"

    entry1 = _make_entry(datetime(2026, 8, 3, 8, 0, tzinfo=timezone.utc))
    ledger.append_entry(ledger_path, entry1)
    first_line_after_first_append = ledger_path.read_text(encoding="utf-8")

    entry2 = _make_entry(datetime(2026, 8, 3, 9, 0, tzinfo=timezone.utc))
    ledger.append_entry(ledger_path, entry2)

    lines = [ln for ln in ledger_path.read_text(encoding="utf-8").split("\n") if ln]
    assert len(lines) == 2
    assert lines[0] + "\n" == first_line_after_first_append  # byte-for-byte unchanged
    assert lines[0] != lines[1]

    obj0 = json.loads(lines[0])
    obj1 = json.loads(lines[1])
    assert obj0["entry_seq"] == 0
    assert obj1["entry_seq"] == 1
    assert obj0["prev_entry_hash"] == "0" * 64
    assert obj1["prev_entry_hash"] == obj0["entry_hash"]
    assert obj0["entry_hash"] != obj1["entry_hash"]


def test_corrupted_existing_line_refuses_further_appends(tmp_path):
    ledger_path = tmp_path / "ledger.jsonl"
    ledger.append_entry(ledger_path, _make_entry(datetime(2026, 8, 3, 8, 0, tzinfo=timezone.utc)))

    # Corrupt one byte of the existing line on disk.
    text = ledger_path.read_text(encoding="utf-8")
    corrupted = text[:-3] + ("9" if text[-3] != "9" else "8") + text[-2:]
    ledger_path.write_text(corrupted, encoding="utf-8")

    with pytest.raises(ValueError):
        ledger.append_entry(ledger_path, _make_entry(datetime(2026, 8, 3, 9, 0, tzinfo=timezone.utc)))

    # The corrupted file must not have gained a second (silently appended) line.
    lines = [ln for ln in ledger_path.read_text(encoding="utf-8").split("\n") if ln]
    assert len(lines) == 1


def test_raw_artifact_write_is_idempotent_and_read_only(tmp_path):
    raw_dir = tmp_path / "raw"
    content = "<?xml version='1.0'?><root>hello</root>"

    path1 = ledger.write_raw_artifact(raw_dir, content)
    mode1 = stat.S_IMODE(path1.stat().st_mode)
    assert mode1 == 0o444

    path2 = ledger.write_raw_artifact(raw_dir, content)
    assert path1 == path2

    files = list(raw_dir.iterdir())
    assert len(files) == 1  # one file, not two
    assert stat.S_IMODE(path2.stat().st_mode) == 0o444


def test_raw_artifact_hash_mismatch_raises(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    content = "<?xml version='1.0'?><root>hello</root>"
    path = ledger.write_raw_artifact(raw_dir, content)

    # Simulate a (practically impossible) sha256 collision: force the
    # digest function to return the same digest for different content, and
    # confirm the integrity check refuses to silently overwrite.
    real_sha256_hex = ledger._sha256_hex
    forced_digest = path.stem  # the digest already used above

    def _fake_sha256_hex(data: bytes) -> str:
        return forced_digest

    monkeypatch.setattr(ledger, "_sha256_hex", _fake_sha256_hex)
    try:
        # Must still look like XML so it maps to the same `<digest>.xml`
        # destination path as the original write -- that's what exercises
        # the collision-detection branch instead of just writing a
        # differently-named `<digest>.body` file alongside it.
        with pytest.raises(ValueError):
            ledger.write_raw_artifact(raw_dir, "<?xml version='1.0'?><root>different</root>")
    finally:
        monkeypatch.setattr(ledger, "_sha256_hex", real_sha256_hex)
