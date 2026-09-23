"""Metered read-only HTTP for the two named GFS endpoints (extraction environment).

Every request is charged to the CP-20 ledger *before* it is sent (expected bytes plus
a fixed header/request allowance) and logged afterwards with its actual wire size.
A request that would cross the job's transfer stop line or the 160 GiB cap is refused
before any byte moves. Only the NCAR d084001 THREDDS file server and the NOAA AWS
``noaa-gfs-bdp-pds`` bucket are reachable through this module.
"""
from __future__ import annotations

import json
import threading
import time
import urllib.parse
from pathlib import Path

import requests

from .budget import Budget, CapExceeded

ALLOWED_HOSTS = {'noaa-gfs-bdp-pds.s3.amazonaws.com': 'aws', 'tds.gdex.ucar.edu': 'ncar'}
ALLOWANCE = 4096  # response headers + request line, charged per request up front
USER_AGENT = 'PJM-cp20-gfs-extraction/1.0 (read-only research)'


class TransferError(RuntimeError):
    """A request failed or returned an unexpected status/size (retryable at a higher level)."""


class NetworkError(TransferError):
    """Connection failure, timeout, 5xx/429 or a stalled trickle: retry the same endpoint."""


class ObjectError(TransferError):
    """4xx or a wrong-size response for this object: use the alternate endpoint."""


# A trickling connection never trips the no-byte read timeout; bound the whole request.
DEADLINE_BASE_S, DEADLINE_PER_BYTE_S = 30.0, 1e-5
CHUNK = 32768


class Fetcher:
    def __init__(self, budget: Budget, log_path: Path, stop_transfer_bytes: int,
                 timeout=(15.0, 60.0)):
        self.budget, self.log_path, self.stop, self.timeout = budget, Path(log_path), stop_transfer_bytes, timeout
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._local = threading.local()
        self.stats = {'requests': 0, 'bytes': 0}

    def _session(self):
        session = getattr(self._local, 'session', None)
        if session is None:
            session = requests.Session()
            session.headers['User-Agent'] = USER_AGENT
            self._local.session = session
        return session

    def get(self, url, purpose, *, byte_range=None, max_body=None):
        host = urllib.parse.urlsplit(url).netloc
        if host not in ALLOWED_HOSTS:
            raise ValueError(f'endpoint not authorised for CP-20: {host}')
        if byte_range is not None:
            start, end = byte_range
            if start < 0 or end < start:
                raise ValueError('invalid byte range')
            expected = end - start + 1
        elif max_body is not None:
            expected = max_body
        else:
            raise ValueError('every CP-20 request must bound its body size')
        reserved = expected + ALLOWANCE
        # Refused here, before sending, if it would cross the stop line or the hard cap.
        self.budget.reserve(limits={'transfer_bytes': self.stop}, transfer_bytes=reserved, requests=1)
        headers = {'Range': f'bytes={byte_range[0]}-{byte_range[1]}'} if byte_range else {}
        began, status, body, resp_headers, error, kind = time.time(), 0, b'', {}, None, None
        deadline = began + DEADLINE_BASE_S + DEADLINE_PER_BYTE_S * expected
        try:
            with self._session().get(url, headers=headers, timeout=self.timeout, stream=True) as resp:
                status = resp.status_code
                resp_headers = {k.title(): v for k, v in resp.headers.items()}
                chunks, got = [], 0
                for chunk in resp.raw.stream(CHUNK, decode_content=False):
                    chunks.append(chunk)
                    got += len(chunk)
                    if got > expected:
                        error, kind = f'body exceeded bound {expected}', 'object'
                        break
                    if time.time() > deadline:
                        error, kind = f'stalled: {got} of {expected} bytes after {time.time() - began:.0f} s', 'network'
                        break
                body = b''.join(chunks)
        except Exception as exc:  # noqa: BLE001 - recorded, classified by caller
            error, kind = f'{type(exc).__name__}: {exc}'[:300], 'network'
        wire = len(body) + sum(len(k) + len(str(v)) + 4 for k, v in resp_headers.items()) + 300 + len(url)
        if wire > reserved:  # never under-record bytes that already moved
            try:
                self.budget.reserve(transfer_bytes=wire - reserved)
            except CapExceeded:
                self.budget.event('transfer_overage_beyond_cap', url=url, bytes=wire - reserved)
                raise
        if error is None and status >= 400:
            error, kind = f'HTTP {status}', ('network' if status >= 500 or status == 429 else 'object')
        if error is None and byte_range is not None and (status != 206 or len(body) != expected):
            error, kind = f'range mismatch status={status} got={len(body)} want={expected}', 'object'
        if error is not None:  # never reuse a connection that failed or stalled
            session = getattr(self._local, 'session', None)
            if session is not None:
                session.close()
                self._local.session = None
        record = {'t_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(began)), 'error_kind': kind,
                  'elapsed_s': round(time.time() - began, 3), 'endpoint': ALLOWED_HOSTS[host],
                  'url': urllib.parse.urlunsplit(urllib.parse.urlsplit(url)._replace(query='', fragment='')),
                  'range': list(byte_range) if byte_range else None, 'status': status, 'body_bytes': len(body),
                  'wire_bytes_estimate': wire, 'charged_bytes': max(wire, reserved), 'purpose': purpose, 'error': error}
        with self._lock:
            self.stats['requests'] += 1
            self.stats['bytes'] += max(wire, reserved)
            with self.log_path.open('a') as fh:
                fh.write(json.dumps(record, sort_keys=True) + '\n')
        if error is not None:
            self.budget.reserve(failed_requests=1)
            raise (NetworkError if kind == 'network' else ObjectError)(f'{purpose}: {error}')
        return status, resp_headers, body
