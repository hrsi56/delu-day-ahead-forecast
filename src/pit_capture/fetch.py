"""Exactly one HTTP request per capture attempt.

The session wrapper keeps the raw response body even when ``entsoe-py`` raises,
so a "no matching data" or an HTTP error still leaves hashable evidence on
disk. ``retry_count=1`` disables the library's internal connection retry, so an
attempt is one request and one request only, and ``http_request_count`` is
recorded in the ledger to prove it.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from entsoe import EntsoeRawClient
from entsoe.exceptions import (
    InvalidBusinessParameterError,
    InvalidParameterError,
    InvalidPSRTypeError,
    NoMatchingDataError,
    PaginationError,
)

from . import BIDDING_ZONE_EIC, PROCESS_TYPE

DEFAULT_TIMEOUT_SECONDS = 60


@dataclass
class FetchOutcome:
    """What one attempt produced. ``payload`` is the authoritative artifact."""

    capture_mode: str
    payload: bytes | None
    encoding: str
    http_status_code: int | None
    http_request_count: int
    result_status: str
    status_detail: str | None
    error_type: str | None
    error_message: str | None
    no_matching_data: bool = False

    @property
    def failed(self) -> bool:
        return self.status_detail is not None and not self.no_matching_data


class _CapturingSession(requests.Session):
    """Records every response so the body survives an exception."""

    def __init__(self) -> None:
        super().__init__()
        self.responses: list[requests.Response] = []

    def get(self, *args, **kwargs):  # type: ignore[override]
        response = super().get(*args, **kwargs)
        self.responses.append(response)
        return response


def fetch_live(
    *,
    api_token: str,
    window_start_utc: datetime,
    window_end_utc: datetime,
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS,
    session: requests.Session | None = None,
) -> FetchOutcome:
    """One A65/A01 request for the DE-LU D+1 window."""
    capturing = session if session is not None else _CapturingSession()
    client = EntsoeRawClient(
        api_key=api_token,
        session=capturing,
        retry_count=1,
        timeout=timeout_seconds,
    )
    start = pd.Timestamp(window_start_utc)
    end = pd.Timestamp(window_end_utc)

    error_type: str | None = None
    error_message: str | None = None
    status_detail: str | None = None
    result_status = "ok"
    no_matching_data = False

    try:
        client.query_load_forecast(
            BIDDING_ZONE_EIC, start=start, end=end, process_type=PROCESS_TYPE
        )
    except NoMatchingDataError as exc:
        no_matching_data = True
        result_status = "no_matching_data"
        error_type = type(exc).__name__
        error_message = str(exc) or "ENTSO-E returned 'No matching data found'"
    except requests.Timeout as exc:
        status_detail = "timeout"
        result_status = "timeout"
        error_type = type(exc).__name__
        error_message = str(exc)
    except requests.HTTPError as exc:
        code = getattr(getattr(exc, "response", None), "status_code", None)
        status_detail = "rate_limited" if code == 429 else "http_error"
        result_status = f"http_{code}" if code is not None else "http_error"
        error_type = type(exc).__name__
        error_message = str(exc)
    except (
        InvalidBusinessParameterError,
        InvalidParameterError,
        InvalidPSRTypeError,
        PaginationError,
    ) as exc:
        status_detail = "invalid_parameter"
        result_status = "invalid_parameter"
        error_type = type(exc).__name__
        error_message = str(exc) or type(exc).__name__
    except requests.RequestException as exc:
        status_detail = "network_error"
        result_status = "network_error"
        error_type = type(exc).__name__
        error_message = str(exc)
    except Exception as exc:  # noqa: BLE001 - an attempt must never crash without a ledger row
        status_detail = "network_error"
        result_status = "unexpected_error"
        error_type = type(exc).__name__
        error_message = str(exc) or type(exc).__name__

    responses = getattr(capturing, "responses", [])
    last = responses[-1] if responses else None
    payload = last.content if last is not None else None
    encoding = (last.encoding or "utf-8") if last is not None else "utf-8"
    http_status_code = last.status_code if last is not None else None
    if status_detail is None and not no_matching_data:
        result_status = f"http_{http_status_code}" if http_status_code else "ok"

    return FetchOutcome(
        capture_mode="live",
        payload=payload,
        encoding=encoding,
        http_status_code=http_status_code,
        http_request_count=len(responses),
        result_status=result_status,
        status_detail=status_detail,
        error_type=error_type,
        error_message=error_message,
        no_matching_data=no_matching_data,
    )


def fetch_replay(path: Path) -> FetchOutcome:
    """Read a local XML file instead of performing the HTTP request."""
    payload = path.read_bytes()
    return FetchOutcome(
        capture_mode="replay",
        payload=payload,
        encoding="utf-8",
        http_status_code=None,
        http_request_count=0,
        result_status="replay",
        status_detail=None,
        error_type=None,
        error_message=None,
    )
