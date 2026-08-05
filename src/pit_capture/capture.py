"""One capture attempt -> one ledger row.

Nothing here crashes without recording the attempt: a failed, partial, absent
or rate-limited request still produces a ``not_qualifying`` entry carrying its
own reason (CP-0 item 2). The only two paths that write no entry at all are a
usage error (the argument was never a capture attempt) and a refusal to
overwrite a differing raw artifact (which would destroy prior evidence).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from . import (
    BIDDING_ZONE,
    BIDDING_ZONE_EIC,
    DOCUMENT_TYPE,
    INSTRUMENT_VERSION,
    PROCESS_TYPE,
    PULLED_AT_SEMANTICS,
    SOURCE,
    SOURCE_ENDPOINT,
)
from .fetch import FetchOutcome, fetch_live, fetch_replay
from .ledger import (
    LedgerError,
    append_entry,
    ledger_tail,
    sha256_bytes,
    write_raw_artifact,
)
from .parsing import PayloadParseError, assess_completeness, parse_a65_payload
from .timewindow import UTC, CaptureWindow, UsageError, derive_window, format_utc

DEFAULT_LEDGER = Path("data/pit-capture/ledger.jsonl")
DEFAULT_RAW_DIR = Path("data/pit-capture/raw")
DEFAULT_MAX_CLOCK_SKEW_SECONDS = 120

EXIT_OK = 0
EXIT_VERIFY_FAILED = 1
EXIT_USAGE = 2
EXIT_ARTIFACT_CONFLICT = 3


@dataclass
class CaptureResult:
    entry: dict[str, Any]
    exit_code: int
    artifact_action: str | None = None


def _raw_artifact_name(delivery_date, pulled_at_utc: datetime, payload_sha256: str) -> str:
    stamp = pulled_at_utc.astimezone(UTC).strftime("%Y%m%dT%H%M%SZ")
    return (
        f"{DOCUMENT_TYPE}-{PROCESS_TYPE}_{BIDDING_ZONE}_{delivery_date.isoformat()}"
        f"_pulled{stamp}_{payload_sha256[:12]}.xml"
    )


def run_capture(
    *,
    at_utc: datetime,
    ledger_path: Path = DEFAULT_LEDGER,
    raw_dir: Path = DEFAULT_RAW_DIR,
    replay_xml: Path | None = None,
    max_clock_skew_seconds: int = DEFAULT_MAX_CLOCK_SKEW_SECONDS,
    now_utc: datetime | None = None,
    api_token: str | None = None,
    fetch_outcome: FetchOutcome | None = None,
) -> CaptureResult:
    """Perform one capture attempt and append exactly one ledger row.

    ``now_utc`` and ``fetch_outcome`` exist for tests only; the CLI always uses
    the true wall clock and a real fetch.
    """
    window = derive_window(at_utc)
    wall_clock_utc = now_utc.astimezone(UTC) if now_utc else datetime.now(timezone.utc)
    clock_skew_seconds = round(
        (window.pulled_at_utc - wall_clock_utc).total_seconds(), 3
    )

    if fetch_outcome is not None:
        outcome = fetch_outcome
    elif replay_xml is not None:
        outcome = fetch_replay(Path(replay_xml))
    else:
        token = api_token if api_token is not None else os.environ.get("ENTSOE_API_TOKEN")
        if not token:
            raise UsageError(
                "ENTSOE_API_TOKEN is not set; export it or use --replay-xml for the offline path"
            )
        outcome = fetch_live(
            api_token=token,
            window_start_utc=window.window_start_utc,
            window_end_utc=window.window_end_utc,
        )

    payload = outcome.payload
    payload_sha256 = sha256_bytes(payload) if payload is not None else None
    artifact_path: Path | None = None
    artifact_action: str | None = None
    artifact_write_error: str | None = None
    if payload is not None and payload_sha256 is not None:
        candidate_path = Path(raw_dir) / _raw_artifact_name(
            window.delivery_date, window.pulled_at_utc, payload_sha256
        )
        try:
            artifact_action = write_raw_artifact(candidate_path, payload)
        except LedgerError as exc:
            # Refuse before appending: a rerun must never replace prior evidence.
            raise LedgerError(str(exc)) from exc
        except OSError as exc:
            # Disk-level failure (permission denied, full disk, missing mount,
            # ...) writing the raw artifact. This must still end in a ledger
            # row -- not an uncaught crash -- so record the attempt with no
            # raw_artifact_path and let the verdict logic below force
            # not_qualifying, since durable raw evidence was never written.
            artifact_action = None
            artifact_write_error = f"{type(exc).__name__}: {exc}"
        else:
            artifact_path = candidate_path

    entry = _build_entry(
        window=window,
        wall_clock_utc=wall_clock_utc,
        clock_skew_seconds=clock_skew_seconds,
        max_clock_skew_seconds=max_clock_skew_seconds,
        outcome=outcome,
        payload_sha256=payload_sha256,
        artifact_path=artifact_path,
        replay_xml=replay_xml,
        artifact_write_error=artifact_write_error,
    )

    index, prev_hash = ledger_tail(Path(ledger_path))
    entry["entry_index"] = index
    entry["prev_entry_sha256"] = prev_hash
    sealed = append_entry(Path(ledger_path), entry)
    return CaptureResult(entry=sealed, exit_code=EXIT_OK, artifact_action=artifact_action)


def _build_entry(
    *,
    window: CaptureWindow,
    wall_clock_utc: datetime,
    clock_skew_seconds: float,
    max_clock_skew_seconds: int,
    outcome: FetchOutcome,
    payload_sha256: str | None,
    artifact_path: Path | None,
    replay_xml: Path | None,
    artifact_write_error: str | None = None,
) -> dict[str, Any]:
    presence: str
    reasons: list[str] = []
    parsed = None
    completeness = None
    status_detail = outcome.status_detail

    if outcome.no_matching_data:
        presence = "absent"
        reasons.append("ENTSO-E returned a well-formed 'no matching data' answer")
    elif outcome.status_detail is not None:
        presence = "request_error"
        reasons.append(
            f"request failed ({status_detail}"
            + (f", HTTP {outcome.http_status_code}" if outcome.http_status_code else "")
            + f"): {outcome.error_message}"
        )
    elif outcome.payload is None:
        presence = "request_error"
        status_detail = "network_error"
        reasons.append("no response body was received")
    else:
        try:
            # outcome.encoding is whatever charset the server's Content-Type
            # header claimed; requests does not validate that name, so a
            # bogus/unknown charset must be treated as a payload defect
            # (LookupError), same as malformed XML, rather than crash the
            # attempt (UnicodeError guards the same call, belt-and-braces).
            text = outcome.payload.decode(outcome.encoding, errors="replace")
            parsed = parse_a65_payload(text)
        except PayloadParseError as exc:
            presence = "request_error"
            status_detail = "parse_error"
            reasons.append(f"payload could not be parsed: {exc}")
        except (LookupError, UnicodeError) as exc:
            presence = "request_error"
            status_detail = "parse_error"
            reasons.append(
                f"payload could not be decoded (encoding {outcome.encoding!r}): {exc}"
            )
        else:
            completeness = assess_completeness(parsed, window)
            complete = (
                completeness.expected_rows is not None
                and completeness.observed_rows == completeness.expected_rows
                and not completeness.missing_slots
                and not completeness.null_slots
            )
            if complete:
                presence = "present_complete"
                note = (
                    f" (note: {'; '.join(completeness.issues)})" if completeness.issues else ""
                )
                reasons.append(
                    f"complete D+1 vector: {completeness.observed_rows}/"
                    f"{completeness.expected_rows} {completeness.resolution} slots populated "
                    f"across a {window.day_length_hours}-hour delivery day" + note
                )
            else:
                presence = "present_partial"
                detail = "; ".join(completeness.issues) if completeness.issues else "short response"
                observed = completeness.observed_rows
                expected = completeness.expected_rows
                reasons.append(
                    f"incomplete D+1 vector ({observed}/"
                    f"{expected if expected is not None else 'unknown'} slots): {detail}"
                )

    pre_gate = window.pulled_at_utc < window.gate_at_utc
    skew_ok = abs(clock_skew_seconds) <= max_clock_skew_seconds
    if not pre_gate:
        reasons.append(
            f"pulled_at_utc {format_utc(window.pulled_at_utc)} is not before the 12:00 "
            f"Europe/Berlin gate {format_utc(window.gate_at_utc)}"
        )
    if not skew_ok:
        reasons.append(
            f"clock skew {clock_skew_seconds}s exceeds the "
            f"{max_clock_skew_seconds}s bound (pulled_at_utc vs wall clock)"
        )
    if artifact_write_error is not None:
        reasons.append(f"raw artifact could not be written to disk: {artifact_write_error}")

    qualifying = (
        presence == "present_complete"
        and pre_gate
        and skew_ok
        and artifact_write_error is None
    )
    verdict = "qualifying" if qualifying else "not_qualifying"
    reason = "; ".join(reasons) if reasons else "no reason recorded"

    entry: dict[str, Any] = {
        # provenance / identity
        "instrument_version": INSTRUMENT_VERSION,
        "capture_mode": outcome.capture_mode,
        "replay_source_path": str(replay_xml) if replay_xml is not None else None,
        "source": SOURCE,
        "source_endpoint": SOURCE_ENDPOINT,
        "document_type": DOCUMENT_TYPE,
        "process_type": PROCESS_TYPE,
        "bidding_zone": BIDDING_ZONE,
        "bidding_zone_eic": BIDDING_ZONE_EIC,
        # time
        "delivery_date": window.delivery_date.isoformat(),
        "gate_at_utc": format_utc(window.gate_at_utc),
        "pulled_at_utc": format_utc(window.pulled_at_utc),
        "pulled_at_semantics": PULLED_AT_SEMANTICS,
        "local_pull_time": window.local_pull_time.isoformat(),
        "local_pull_timezone": "Europe/Berlin",
        "utc_offset": window.utc_offset,
        "pull_local_date": window.pull_local_date.isoformat(),
        "wall_clock_utc": format_utc(wall_clock_utc),
        "clock_skew_seconds": clock_skew_seconds,
        "max_clock_skew_seconds": max_clock_skew_seconds,
        "pulled_at_is_pre_gate": pre_gate,
        "delivery_window_start_utc": format_utc(window.window_start_utc),
        "delivery_window_end_utc": format_utc(window.window_end_utc),
        "day_length_hours": window.day_length_hours,
        # request result
        "result_status": outcome.result_status,
        "http_status_code": outcome.http_status_code,
        "http_request_count": outcome.http_request_count,
        "status_detail": status_detail,
        "error_type": outcome.error_type,
        "error_message": outcome.error_message,
        "presence": presence,
        # payload facts
        "source_created_at_utc": format_utc(parsed.created_at_utc) if parsed else None,
        "resolution": completeness.resolution if completeness else None,
        "resolutions_detected": parsed.resolutions if parsed else [],
        "curve_types": parsed.curve_types if parsed else [],
        "timeseries_count": parsed.timeseries_count if parsed else 0,
        "expected_rows": completeness.expected_rows if completeness else None,
        "observed_rows": completeness.observed_rows if completeness else 0,
        "completeness_ratio": completeness.completeness_ratio if completeness else None,
        "missing_slots": completeness.missing_slots if completeness else None,
        "null_slots": completeness.null_slots if completeness else 0,
        "points_outside_window": completeness.points_outside_window if completeness else 0,
        "first_delivery_timestamp_utc": (
            format_utc(completeness.first_delivery_timestamp_utc) if completeness else None
        ),
        "last_delivery_timestamp_utc": (
            format_utc(completeness.last_delivery_timestamp_utc) if completeness else None
        ),
        "latest_fully_populated_timestamp_utc": (
            format_utc(completeness.latest_fully_populated_timestamp_utc)
            if completeness
            else None
        ),
        "payload_sha256": payload_sha256,
        "payload_bytes": len(outcome.payload) if outcome.payload is not None else 0,
        "raw_artifact_path": str(artifact_path) if artifact_path is not None else None,
        "raw_artifact_write_error": artifact_write_error,
        # verdict
        "verdict": verdict,
        "reason": reason,
        "counts_toward_section_3_qualifying_days": bool(
            qualifying and outcome.capture_mode == "live"
        ),
    }
    return entry
