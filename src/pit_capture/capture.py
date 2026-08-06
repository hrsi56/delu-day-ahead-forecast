"""One capture attempt for ENTSO-E day-ahead load forecast A65/A01 on DE-LU.

Deliberate deviation from using entsoe-py's own request methods: this module
makes the HTTP GET itself (via `requests`) instead of calling
`EntsoeRawClient.query_load_forecast`, because entsoe-py's `_base_request`
raises bare exceptions on error/empty responses without attaching the
response body, which would silently break the "every attempt retains the
raw response" contract (including failed attempts) required by the plan.
"""

from __future__ import annotations

import dataclasses
import hashlib
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import pandas as pd
import requests
from entsoe.entsoe import URL
from entsoe.parsers import parse_loads

from . import ledger
from .berlin_window import (
    BERLIN,
    expected_quarter_hour_count,
    expected_quarter_hour_grid_utc,
    gate_at_utc,
    resolve_local,
)

SOURCE = "entsoe"
DOCUMENT_TYPE = "A65"
PROCESS_TYPE = "A01"
DOMAIN_EIC = "10Y1001A1001A82H"  # DE-LU

_REQUEST_TIMEOUT_SECONDS = 30


@dataclass(frozen=True)
class LedgerEntry:
    """The §3 point-in-time capture contract fields, plus the qualifying
    verdict and its reason."""

    source: str
    document_type: str
    process_type: str
    domain_eic: str
    delivery_date: date
    gate_at_utc: datetime
    pulled_at_utc: datetime
    local_pull_time: str
    utc_offset: str
    http_status: Optional[int]
    status: str  # present_complete | present_partial | absent | request_error
    expected_row_count: int
    observed_row_count: int
    completeness_ratio: float
    first_delivery_timestamp: Optional[datetime]
    last_delivery_timestamp: Optional[datetime]
    latest_fully_populated_timestamp: Optional[datetime]
    payload_sha256: Optional[str]
    raw_artifact_path: Optional[str]
    qualifying: bool
    qualifying_reason: str


def _format_period(dt: datetime) -> str:
    """Replicate entsoe-py's `_datetime_to_str`: convert to UTC, round to
    the nearest hour, format as %Y%m%d%H00. Berlin local midnight always
    falls on a whole UTC hour (the Berlin/UTC offset is always a whole
    number of hours), so this rounding is a no-op in practice but is
    implemented faithfully regardless."""
    dt = dt.astimezone(timezone.utc)
    minute_fraction = dt.minute + dt.second / 60 + dt.microsecond / 6.0e7
    if minute_fraction >= 30:
        dt = dt.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        dt = dt.replace(minute=0, second=0, microsecond=0)
    return dt.strftime("%Y%m%d%H00")


def fetch_raw(delivery_date: date, token: str, session=None) -> tuple[int, str]:
    """Perform the real GET for the full Berlin delivery-day window of
    `delivery_date`. Returns (status_code, response_text).

    Network-level exceptions (`requests.exceptions.RequestException`) are
    allowed to propagate to the caller uncaught.
    """
    from .berlin_window import delivery_day_window_utc

    start_utc, end_utc = delivery_day_window_utc(delivery_date)
    params = {
        "documentType": DOCUMENT_TYPE,
        "processType": PROCESS_TYPE,
        "outBiddingZone_Domain": DOMAIN_EIC,
        "securityToken": token,
        "periodStart": _format_period(start_utc),
        "periodEnd": _format_period(end_utc),
    }
    getter = session.get if session is not None else requests.get
    response = getter(URL, params=params, timeout=_REQUEST_TIMEOUT_SECONDS)
    return response.status_code, response.text


def classify(
    raw_status: Optional[int],
    raw_text: Optional[str],
    fetch_exception: Optional[Exception],
    pulled_at_utc: datetime,
    delivery_date: date,
) -> LedgerEntry:
    """Pure, no network: classify one capture attempt's outcome and build
    its LedgerEntry. Safe for a Critic to call directly against fixtures.

    `raw_artifact_path` is always None here (writing the raw artifact is an
    I/O side effect owned by capture_attempt, which fills it in after this
    function returns).
    """
    if pulled_at_utc.tzinfo is None:
        raise ValueError("pulled_at_utc must be timezone-aware (an unambiguous UTC instant)")
    pulled_at_utc = pulled_at_utc.astimezone(timezone.utc)

    gate = gate_at_utc(delivery_date)
    local = resolve_local(pulled_at_utc)
    expected_row_count = expected_quarter_hour_count(delivery_date)

    payload_sha256 = (
        hashlib.sha256(raw_text.encode("utf-8")).hexdigest() if raw_text is not None else None
    )

    observed_row_count = 0
    completeness_ratio = 0.0
    first_ts: Optional[datetime] = None
    last_ts: Optional[datetime] = None
    latest_full_ts: Optional[datetime] = None

    if fetch_exception is not None:
        status = "request_error"
        reason = "request_error"
    elif raw_status == 429:
        status = "request_error"
        reason = "rate_limited"
    elif raw_status is None or not (200 <= raw_status < 300):
        status = "request_error"
        reason = "request_error"
    elif raw_text is not None and "No matching data found" in raw_text:
        status = "absent"
        reason = "absent"
    else:
        try:
            df = parse_loads(raw_text, process_type=PROCESS_TYPE)
        except Exception:
            df = None

        if df is None or df.empty or "Forecasted Load" not in df.columns:
            status = "absent"
            reason = "absent"
        else:
            grid = expected_quarter_hour_grid_utc(delivery_date)
            grid_keys = {int(ts.timestamp()) for ts in grid}

            col = df["Forecasted Load"]
            present: list[tuple[datetime, float]] = []
            for ts, val in col.items():
                if pd.notna(val):
                    present.append((pd.Timestamp(ts).to_pydatetime(), val))

            observed_keys = {int(ts.timestamp()) for ts, _ in present if int(ts.timestamp()) in grid_keys}
            observed_row_count = len(observed_keys)
            completeness_ratio = (
                observed_row_count / expected_row_count if expected_row_count else 0.0
            )

            if present:
                ordered = sorted(present, key=lambda pair: pair[0])
                first_ts = ordered[0][0]
                last_ts = ordered[-1][0]

            for grid_ts in grid:
                if int(grid_ts.timestamp()) in observed_keys:
                    latest_full_ts = grid_ts
                else:
                    break

            if expected_row_count > 0 and observed_row_count == expected_row_count:
                status = "present_complete"
                reason = None  # decided below, based on the gate
            else:
                status = "present_partial"
                reason = "present_partial"

    if status == "present_complete":
        if pulled_at_utc < gate:
            qualifying = True
            reason = "qualifying"
        else:
            qualifying = False
            reason = "post_gate"
    else:
        qualifying = False

    return LedgerEntry(
        source=SOURCE,
        document_type=DOCUMENT_TYPE,
        process_type=PROCESS_TYPE,
        domain_eic=DOMAIN_EIC,
        delivery_date=delivery_date,
        gate_at_utc=gate,
        pulled_at_utc=pulled_at_utc,
        local_pull_time=local["local_iso"],
        utc_offset=local["utc_offset"],
        http_status=raw_status,
        status=status,
        expected_row_count=expected_row_count,
        observed_row_count=observed_row_count,
        completeness_ratio=completeness_ratio,
        first_delivery_timestamp=first_ts,
        last_delivery_timestamp=last_ts,
        latest_fully_populated_timestamp=latest_full_ts,
        payload_sha256=payload_sha256,
        raw_artifact_path=None,
        qualifying=qualifying,
        qualifying_reason=reason,
    )


def capture_attempt(
    pulled_at_utc: datetime,
    delivery_date: Optional[date],
    token: str,
    ledger_path: Path,
    raw_dir: Path,
) -> LedgerEntry:
    """Orchestrate one capture attempt: fetch_raw -> classify -> raw-artifact
    write -> ledger append. Returns the appended LedgerEntry."""
    if pulled_at_utc.tzinfo is None:
        raise ValueError("pulled_at_utc must be timezone-aware (an unambiguous UTC instant)")
    pulled_at_utc = pulled_at_utc.astimezone(timezone.utc)

    if delivery_date is None:
        local_calendar_date = pulled_at_utc.astimezone(BERLIN).date()
        delivery_date = local_calendar_date + timedelta(days=1)

    raw_status: Optional[int] = None
    raw_text: Optional[str] = None
    fetch_exception: Optional[Exception] = None
    try:
        raw_status, raw_text = fetch_raw(delivery_date, token)
    except requests.exceptions.RequestException as exc:
        fetch_exception = exc

    entry = classify(raw_status, raw_text, fetch_exception, pulled_at_utc, delivery_date)

    raw_artifact_path: Optional[Path] = None
    if raw_text is not None:
        raw_artifact_path = ledger.write_raw_artifact(raw_dir, raw_text)
        entry = dataclasses.replace(entry, raw_artifact_path=str(raw_artifact_path))

    ledger.append_entry(ledger_path, entry)
    return entry
