"""End-to-end capture attempts: presence, verdict, immutability, evidence."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest
import requests
from a65_xml import build_day
from conftest import FIXTURE_DIR

from pit_capture.capture import run_capture
from pit_capture.fetch import FetchOutcome, _CapturingSession, fetch_live
from pit_capture.ledger import LedgerError, read_entries, sha256_bytes

PULL = datetime(2026, 8, 5, 8, 30, tzinfo=timezone.utc)  # 10:30 Berlin, pre-gate
COMPLETE = FIXTURE_DIR / "a65_a01_de-lu_2026-08-06_complete_96.xml"
TRUNCATED = FIXTURE_DIR / "a65_a01_de-lu_2026-08-06_truncated_80.xml"


def _capture(ledger_paths, **kwargs):
    ledger, raw_dir = ledger_paths
    params = {
        "at_utc": PULL,
        "ledger_path": ledger,
        "raw_dir": raw_dir,
        "now_utc": PULL,
        "replay_xml": COMPLETE,
    }
    params.update(kwargs)
    return run_capture(**params)


def _live_outcome(payload: bytes) -> FetchOutcome:
    """A 'live' outcome around a fixture payload (positive control, live path)."""
    return FetchOutcome(
        capture_mode="live",
        payload=payload,
        encoding="utf-8",
        http_status_code=200,
        http_request_count=1,
        result_status="http_200",
        status_detail=None,
        error_type=None,
        error_message=None,
    )


# --------------------------------------------------------------------------
# positive control
# --------------------------------------------------------------------------


def test_complete_response_is_present_complete_and_qualifying(ledger_paths):
    entry = _capture(ledger_paths).entry
    assert entry["presence"] == "present_complete"
    assert entry["verdict"] == "qualifying"
    assert entry["expected_rows"] == 96
    assert entry["observed_rows"] == 96
    assert entry["completeness_ratio"] == 1.0
    assert entry["day_length_hours"] == 24
    assert entry["resolution"] == "PT15M"
    assert entry["pulled_at_is_pre_gate"] is True
    assert entry["clock_skew_seconds"] == 0.0
    assert entry["delivery_date"] == "2026-08-06"
    assert entry["gate_at_utc"] == "2026-08-05T10:00:00+00:00"
    assert entry["local_pull_time"] == "2026-08-05T10:30:00+02:00"
    assert entry["utc_offset"] == "+02:00"
    assert entry["latest_fully_populated_timestamp_utc"] == "2026-08-06T21:45:00+00:00"


def test_replayed_qualifying_capture_never_counts_toward_section_3(ledger_paths):
    entry = _capture(ledger_paths).entry
    assert entry["verdict"] == "qualifying"
    assert entry["capture_mode"] == "replay"
    assert entry["counts_toward_section_3_qualifying_days"] is False


def test_live_complete_capture_counts_toward_section_3(ledger_paths):
    entry = _capture(
        ledger_paths, replay_xml=None, fetch_outcome=_live_outcome(COMPLETE.read_bytes())
    ).entry
    assert entry["capture_mode"] == "live"
    assert entry["presence"] == "present_complete"
    assert entry["verdict"] == "qualifying"
    assert entry["counts_toward_section_3_qualifying_days"] is True


# --------------------------------------------------------------------------
# failure taxonomy
# --------------------------------------------------------------------------


def test_truncated_response_is_partial_and_not_qualifying(ledger_paths):
    entry = _capture(ledger_paths, replay_xml=TRUNCATED).entry
    assert entry["presence"] == "present_partial"
    assert entry["verdict"] == "not_qualifying"
    assert entry["observed_rows"] == 80
    assert entry["expected_rows"] == 96
    assert entry["missing_slots"] == 16
    assert "incomplete D+1 vector (80/96 slots)" in entry["reason"]
    assert entry["counts_toward_section_3_qualifying_days"] is False
    assert entry["payload_sha256"] == sha256_bytes(TRUNCATED.read_bytes())


def test_rate_limited_request_records_request_error(ledger_paths):
    body = b"Too many requests. Maximum 400 requests per minute."
    outcome = fetch_live(
        api_token="unused",
        window_start_utc=datetime(2026, 8, 5, 22, 0, tzinfo=timezone.utc),
        window_end_utc=datetime(2026, 8, 6, 22, 0, tzinfo=timezone.utc),
        session=_canned_session(429, body),
    )
    entry = _capture(ledger_paths, replay_xml=None, fetch_outcome=outcome).entry
    assert entry["presence"] == "request_error"
    assert entry["status_detail"] == "rate_limited"
    assert entry["http_status_code"] == 429
    assert entry["http_request_count"] == 1
    assert entry["verdict"] == "not_qualifying"
    assert entry["counts_toward_section_3_qualifying_days"] is False
    # the failing body is still retained as evidence
    assert entry["payload_sha256"] == sha256_bytes(body)
    assert Path(entry["raw_artifact_path"]).read_bytes() == body


def test_server_error_records_http_error(ledger_paths):
    outcome = fetch_live(
        api_token="unused",
        window_start_utc=datetime(2026, 8, 5, 22, 0, tzinfo=timezone.utc),
        window_end_utc=datetime(2026, 8, 6, 22, 0, tzinfo=timezone.utc),
        session=_canned_session(503, b"service unavailable"),
    )
    entry = _capture(ledger_paths, replay_xml=None, fetch_outcome=outcome).entry
    assert entry["presence"] == "request_error"
    assert entry["status_detail"] == "http_error"
    assert entry["http_status_code"] == 503
    assert entry["verdict"] == "not_qualifying"


def test_no_matching_data_records_absent(ledger_paths):
    body = (
        b'<?xml version="1.0" encoding="UTF-8"?><Acknowledgement_MarketDocument>'
        b"<Reason><code>999</code><text>No matching data found for Data item Load "
        b"[6.1.B].</text></Reason></Acknowledgement_MarketDocument>"
    )
    outcome = fetch_live(
        api_token="unused",
        window_start_utc=datetime(2026, 8, 5, 22, 0, tzinfo=timezone.utc),
        window_end_utc=datetime(2026, 8, 6, 22, 0, tzinfo=timezone.utc),
        session=_canned_session(200, body, content_type="application/xml"),
    )
    entry = _capture(ledger_paths, replay_xml=None, fetch_outcome=outcome).entry
    assert entry["presence"] == "absent"
    assert entry["result_status"] == "no_matching_data"
    assert entry["verdict"] == "not_qualifying"
    assert entry["payload_sha256"] == sha256_bytes(body)


def test_timeout_records_request_error(ledger_paths):
    outcome = fetch_live(
        api_token="unused",
        window_start_utc=datetime(2026, 8, 5, 22, 0, tzinfo=timezone.utc),
        window_end_utc=datetime(2026, 8, 6, 22, 0, tzinfo=timezone.utc),
        session=_raising_session(requests.Timeout("read timed out")),
    )
    entry = _capture(ledger_paths, replay_xml=None, fetch_outcome=outcome).entry
    assert entry["presence"] == "request_error"
    assert entry["status_detail"] == "timeout"
    assert entry["payload_sha256"] is None
    assert entry["raw_artifact_path"] is None
    assert entry["verdict"] == "not_qualifying"


def test_unparseable_payload_records_parse_error(ledger_paths, tmp_path):
    broken = tmp_path / "broken.xml"
    broken.write_text("<GL_MarketDocument><unclosed>")
    entry = _capture(ledger_paths, replay_xml=broken).entry
    assert entry["presence"] == "request_error"
    assert entry["status_detail"] == "parse_error"
    assert entry["verdict"] == "not_qualifying"
    assert entry["payload_sha256"] is not None  # evidence still retained


def test_bogus_declared_encoding_records_parse_error_not_a_crash(ledger_paths):
    """A server (or gateway) that claims an unknown charset in Content-Type
    must not crash the attempt: requests does not validate that name, and
    bytes.decode() raises LookupError for it, which must be caught the same
    way a malformed-XML PayloadParseError is."""
    outcome = _live_outcome(COMPLETE.read_bytes())
    outcome.encoding = "bogus-nonexistent-codec"
    entry = _capture(ledger_paths, replay_xml=None, fetch_outcome=outcome).entry
    assert entry["presence"] == "request_error"
    assert entry["status_detail"] == "parse_error"
    assert entry["verdict"] == "not_qualifying"
    assert "could not be decoded" in entry["reason"]
    assert entry["payload_sha256"] is not None  # evidence still retained


def test_raw_artifact_disk_write_failure_still_records_a_not_qualifying_entry(
    ledger_paths,
):
    """A disk-level failure writing the raw artifact (permission denied, full
    disk, ...) must still end in a ledger row, not an uncaught crash. Trigger
    it portably by making raw_dir a plain file, so os.makedirs/mkdir raises
    OSError rather than needing chmod (which root would bypass)."""
    ledger, raw_dir = ledger_paths
    raw_dir.parent.mkdir(parents=True, exist_ok=True)
    raw_dir.write_bytes(b"not a directory")  # raw_dir path is a file, not a dir

    entry = _capture((ledger, raw_dir)).entry
    assert entry["presence"] == "present_complete"  # payload itself was fine
    assert entry["verdict"] == "not_qualifying"
    assert entry["raw_artifact_path"] is None
    assert entry["raw_artifact_write_error"] is not None
    assert "raw artifact could not be written to disk" in entry["reason"]
    assert entry["counts_toward_section_3_qualifying_days"] is False
    # the attempt still produced exactly one ledger row
    assert len(read_entries(ledger)) == 1


def test_post_gate_pull_is_not_qualifying(ledger_paths):
    post_gate = datetime(2026, 8, 5, 13, 35, tzinfo=timezone.utc)  # 15:35 Berlin
    entry = _capture(ledger_paths, at_utc=post_gate, now_utc=post_gate).entry
    assert entry["presence"] == "present_complete"
    assert entry["pulled_at_is_pre_gate"] is False
    assert entry["verdict"] == "not_qualifying"
    assert "not before the 12:00 Europe/Berlin gate" in entry["reason"]


def test_excessive_clock_skew_is_not_qualifying(ledger_paths):
    entry = _capture(ledger_paths, now_utc=PULL - timedelta(minutes=30)).entry
    assert entry["presence"] == "present_complete"
    assert entry["clock_skew_seconds"] == 1800.0
    assert entry["verdict"] == "not_qualifying"
    assert "clock skew" in entry["reason"]


# --------------------------------------------------------------------------
# pulled_at semantics
# --------------------------------------------------------------------------


def test_pulled_at_never_tracks_created_date_time(ledger_paths, tmp_path):
    """CP-0 item 3: createdDateTime lands in its own field and nowhere else."""
    created = datetime(2026, 8, 4, 22, 15, 3, tzinfo=timezone.utc)
    payload = build_day(
        start_utc=datetime(2026, 8, 5, 22, 0, tzinfo=timezone.utc),
        slots=96,
        created_at_utc=created,
    )
    fixture = tmp_path / "created_far_from_pull.xml"
    fixture.write_text(payload)

    entry = _capture(ledger_paths, replay_xml=fixture).entry
    assert entry["pulled_at_utc"] == "2026-08-05T08:30:00+00:00"
    assert entry["source_created_at_utc"] == "2026-08-04T22:15:03+00:00"
    assert entry["pulled_at_utc"] != entry["source_created_at_utc"]
    assert "observed-available-by" in entry["pulled_at_semantics"]


def test_fall_back_day_dual_offset_captures_are_two_distinct_entries(ledger_paths, tmp_path):
    """CP-0 item 4, end to end: both Berlin 02:30 pulls survive as distinct rows."""
    payload = build_day(start_utc=datetime(2026, 10, 25, 23, 0, tzinfo=timezone.utc), slots=96)
    fixture = tmp_path / "delivery_2026-10-26.xml"
    fixture.write_text(payload)

    first_at = datetime(2026, 10, 25, 0, 30, tzinfo=timezone.utc)  # 02:30 +02:00
    second_at = datetime(2026, 10, 25, 1, 30, tzinfo=timezone.utc)  # 02:30 +01:00
    first = _capture(
        ledger_paths, at_utc=first_at, now_utc=first_at, replay_xml=fixture
    ).entry
    second = _capture(
        ledger_paths, at_utc=second_at, now_utc=second_at, replay_xml=fixture
    ).entry

    assert first["pulled_at_utc"] != second["pulled_at_utc"]
    assert first["utc_offset"] == "+02:00"
    assert second["utc_offset"] == "+01:00"
    assert first["local_pull_time"].startswith("2026-10-25T02:30:00")
    assert second["local_pull_time"].startswith("2026-10-25T02:30:00")
    assert first["delivery_date"] == second["delivery_date"] == "2026-10-26"
    assert first["presence"] == second["presence"] == "present_complete"
    assert first["raw_artifact_path"] != second["raw_artifact_path"]  # distinct pull stamps
    assert first["payload_sha256"] == second["payload_sha256"]  # same bytes


# --------------------------------------------------------------------------
# immutability
# --------------------------------------------------------------------------


def test_rerun_appends_and_never_rewrites_the_prior_entry(ledger_paths):
    ledger, _ = ledger_paths
    first = _capture(ledger_paths).entry
    first_line = ledger.read_text().splitlines()[0]

    second = _capture(ledger_paths).entry
    lines = ledger.read_text().splitlines()

    assert len(lines) == 2
    assert lines[0] == first_line  # byte-identical: nothing was rewritten
    assert first["entry_index"] == 0
    assert second["entry_index"] == 1
    assert first["prev_entry_sha256"] is None
    assert second["prev_entry_sha256"] == first["entry_sha256"]
    assert second["raw_artifact_path"] == first["raw_artifact_path"]  # same bytes reused


def test_refuses_to_overwrite_a_differing_raw_artifact(ledger_paths):
    ledger, _ = ledger_paths
    first = _capture(ledger_paths).entry
    artifact = Path(first["raw_artifact_path"])
    artifact.write_bytes(b"tampered payload")

    with pytest.raises(LedgerError, match="refusing to overwrite"):
        _capture(ledger_paths)

    assert len(read_entries(ledger)) == 1  # aborted before appending
    assert artifact.read_bytes() == b"tampered payload"  # and without clobbering


def test_every_section_3_field_is_present(ledger_paths):
    entry = _capture(ledger_paths).entry
    required = [
        "source",
        "document_type",
        "process_type",
        "bidding_zone",
        "bidding_zone_eic",
        "delivery_date",
        "gate_at_utc",
        "pulled_at_utc",
        "local_pull_time",
        "utc_offset",
        "result_status",
        "http_status_code",
        "expected_rows",
        "observed_rows",
        "completeness_ratio",
        "first_delivery_timestamp_utc",
        "last_delivery_timestamp_utc",
        "latest_fully_populated_timestamp_utc",
        "payload_sha256",
        "raw_artifact_path",
        "raw_artifact_write_error",
        "presence",
        "day_length_hours",
        "resolution",
        "verdict",
        "reason",
        "source_created_at_utc",
        "wall_clock_utc",
        "clock_skew_seconds",
        "capture_mode",
        "counts_toward_section_3_qualifying_days",
        "instrument_version",
        "entry_index",
        "prev_entry_sha256",
        "entry_sha256",
    ]
    missing = [key for key in required if key not in entry]
    assert missing == []
    assert json.loads(json.dumps(entry)) == entry  # JSON-serialisable as written


# --------------------------------------------------------------------------
# canned-session helpers (no network)
# --------------------------------------------------------------------------


def _make_response(status_code: int, body: bytes, content_type: str) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = body
    response.encoding = "utf-8"
    response.url = "https://web-api.tp.entsoe.eu/api"
    response.headers["content-type"] = content_type
    return response


def _canned_session(status_code: int, body: bytes, content_type: str = "text/plain"):
    class CannedSession(_CapturingSession):
        def request(self, *args, **kwargs):  # type: ignore[override]
            return _make_response(status_code, body, content_type)

    return CannedSession()


def _raising_session(error: Exception):
    class RaisingSession(_CapturingSession):
        def request(self, *args, **kwargs):  # type: ignore[override]
            raise error

    return RaisingSession()
