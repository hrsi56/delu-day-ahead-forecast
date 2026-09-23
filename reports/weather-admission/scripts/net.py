"""Metered, read-only HTTP access for programme 4.1 weather-archive admission.

Every network request made by the admission scripts goes through ``fetch``.
Each call appends one JSON line to ``.local/weather-admission/logs/usage.jsonl``
with the URL (query strings dropped), purpose, byte range, status, header and
body bytes.  The cumulative transfer ceiling is enforced *before* a request is
sent: a request whose requested or declared size would cross the stop line is
refused.  The Hugging Face token is read from the environment only for requests
that need it, is never logged, and requests drops it on cross-host redirects.
"""

from __future__ import annotations

import hashlib
import json
import os
import threading
import time
import urllib.parse
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[3]
LOCAL = ROOT / ".local" / "weather-admission"
LOG = LOCAL / "logs" / "usage.jsonl"
SOURCES = LOCAL / "sources"
SOURCE_MANIFEST = SOURCES / "manifest.jsonl"
GIB = 1024**3
TRANSFER_CAP = 4 * GIB
# Stop line leaves headroom below the 4 GiB maximum for request overhead.
STOP_LINE = int(3.85 * GIB)
USER_AGENT = "PJM-weather-admission/1.0 (read-only research)"

_lock = threading.Lock()
_local = threading.local()
_used: int | None = None


class CapReached(RuntimeError):
    pass


def _redact(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def _record_bytes(rec: dict) -> int:
    return rec.get("header_bytes", 0) + rec.get("body_bytes", 0) + rec.get("request_bytes", 0)


_offset = 0


def used_bytes() -> int:
    """Cumulative logged bytes across all processes (incremental tail read of the shared log)."""
    global _used, _offset
    with _lock:
        if _used is None:
            _used = 0
        if LOG.exists():
            with LOG.open("rb") as fh:
                fh.seek(_offset)
                chunk = fh.read()
            complete = chunk[: chunk.rfind(b"\n") + 1]
            for line in complete.splitlines():
                if line.strip():
                    _used += _record_bytes(json.loads(line))
            _offset += len(complete)
        return _used


def _log(rec: dict) -> None:
    with _lock:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        with LOG.open("a") as fh:
            fh.write(json.dumps(rec, sort_keys=True) + "\n")


def _session() -> requests.Session:
    s = getattr(_local, "session", None)
    if s is None:
        s = requests.Session()
        s.headers["User-Agent"] = USER_AGENT
        _local.session = s
    return s


def fetch(
    url: str,
    purpose: str,
    *,
    byte_range: tuple[int, int] | None = None,
    suffix: int | None = None,
    method: str = "GET",
    auth_hf: bool = False,
    max_body: int | None = None,
    timeout: float = 120.0,
    retries: int = 2,
) -> tuple[int, dict, bytes]:
    """Return (status, headers, body).  Raises CapReached before crossing the stop line."""
    expected = 0
    if suffix is not None:
        expected = suffix
    elif byte_range is not None:
        expected = byte_range[1] - byte_range[0] + 1
    elif max_body is not None:
        expected = max_body
    if used_bytes() + expected + 4096 > STOP_LINE:
        raise CapReached(f"transfer stop line: used={used_bytes()} expected={expected}")

    headers = {}
    if byte_range is not None:
        headers["Range"] = f"bytes={byte_range[0]}-{byte_range[1]}"
    elif suffix is not None:
        headers["Range"] = f"bytes=-{suffix}"
    if auth_hf:
        token = os.environ.get("HF_TOKEN")
        if not token:
            raise RuntimeError("HF_TOKEN not present in environment")
        headers["Authorization"] = f"Bearer {token}"

    attempt = 0
    while True:
        attempt += 1
        started = time.time()
        status, resp_headers, body, error, final_url = 0, {}, b"", None, url
        try:
            with _session().request(method, url, headers=headers, timeout=timeout, stream=True) as resp:
                status = resp.status_code
                resp_headers = {k.title(): v for k, v in resp.headers.items()}
                final_url = resp.url
                declared = int(resp_headers.get("Content-Length", "0") or 0)
                if method != "HEAD":
                    limit = max_body if max_body is not None else declared
                    if byte_range is None and suffix is None and max_body is None and used_bytes() + declared + 4096 > STOP_LINE:
                        error = "refused: declared length would cross stop line"
                    else:
                        chunks, got = [], 0
                        for chunk in resp.raw.stream(65536, decode_content=False):
                            chunks.append(chunk)
                            got += len(chunk)
                            if max_body is not None and got >= limit:
                                break
                        body = b"".join(chunks)
                        if resp_headers.get("Content-Encoding") == "gzip":
                            import gzip

                            wire = len(body)
                            body = gzip.decompress(body)
                            resp_headers["X-Wire-Bytes"] = str(wire)
                if status >= 400:
                    error = f"HTTP {status}"
        except Exception as exc:  # noqa: BLE001 - logged, retried if transient
            error = f"{type(exc).__name__}: {exc}"[:300]
        wire_body = int(resp_headers.get("X-Wire-Bytes", len(body)))
        header_bytes = sum(len(k) + len(str(v)) + 4 for k, v in resp_headers.items()) + 20
        _log(
            {
                "t_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(started)),
                "elapsed_s": round(time.time() - started, 3),
                "url": _redact(url),
                "method": method,
                "range": list(byte_range) if byte_range else ([-suffix] if suffix else None),
                "status": status,
                "header_bytes": header_bytes,
                "body_bytes": wire_body,
                "request_bytes": 300 + len(url),
                "purpose": purpose,
                "attempt": attempt,
                "error": error,
            }
        )
        if error and error.startswith("refused"):
            raise CapReached(error)
        transient = error is not None and status in (0, 429, 500, 502, 503, 504)
        if transient and attempt <= retries:
            time.sleep(2.0 * attempt)
            continue
        resp_headers["X-Final-Url"] = final_url
        return status, resp_headers, body


def save_source(
    url: str, purpose: str, *, name: str, auth_hf: bool = False, max_body: int = 5_000_000
) -> tuple[int, bytes, str]:
    """Fetch a documentation/source page, store raw bytes and a dated sha256 fingerprint."""
    status, headers, body = fetch(url, purpose, auth_hf=auth_hf, max_body=max_body)
    digest = hashlib.sha256(body).hexdigest()
    SOURCES.mkdir(parents=True, exist_ok=True)
    (SOURCES / name).write_bytes(body)
    with _lock, SOURCE_MANIFEST.open("a") as fh:
        fh.write(
            json.dumps(
                {
                    "name": name,
                    "url": _redact(url),
                    "retrieved_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "status": status,
                    "sha256": digest,
                    "bytes": len(body),
                    "last_modified": headers.get("Last-Modified"),
                    "purpose": purpose,
                },
                sort_keys=True,
            )
            + "\n"
        )
    return status, body, digest


def summary() -> dict:
    n = 0
    if LOG.exists():
        with LOG.open() as fh:
            n = sum(1 for _ in fh)
    total = used_bytes()
    return {"requests": n, "bytes": total, "gib": round(total / GIB, 4), "stop_line_gib": round(STOP_LINE / GIB, 3)}


if __name__ == "__main__":
    print(json.dumps(summary()))
