"""CP-18a item 2: the transport interface, the boundary refusal before any socket, and the credential rules.

Fast; no local data; no network (every networking entry point is patched to raise). Dates past the boundary
are computed from `cp25.guard.BOUNDARY` at run time and never printed.
"""
from __future__ import annotations

from datetime import date, timedelta
import gzip
import http.client
import json
from pathlib import Path
import re
import socket
import urllib.request

import pytest

from cp18.live import entsoe, gfs, smard
from cp18.live.transport import (CredentialMissing, HttpTransport, ReplayFolder, ReplayMiss, ReplayTransport, Request,
                                 Response, TransportError)
from cp25 import guard

SRC = Path(__file__).resolve().parents[2] / 'src' / 'cp18'
AFTER = guard.BOUNDARY + timedelta(days=1)          # computed, never written


class NetworkTouched(AssertionError):
    pass


@pytest.fixture
def no_network(monkeypatch):
    def refuse(*_a, **_k):
        raise NetworkTouched('a network call was attempted')
    monkeypatch.setattr(socket, 'socket', refuse)
    monkeypatch.setattr(socket, 'create_connection', refuse)
    monkeypatch.setattr(socket, 'getaddrinfo', refuse)
    monkeypatch.setattr(http.client.HTTPConnection, 'connect', refuse)
    monkeypatch.setattr(http.client.HTTPSConnection, 'connect', refuse)
    monkeypatch.setattr(urllib.request, 'urlopen', refuse)


def _refused(callable_):
    try:
        callable_()
    except guard.BoundaryRefused:
        return True
    return False


def test_http_transport_refuses_past_the_boundary_before_any_socket(no_network):
    t = HttpTransport()
    assert _refused(lambda: t.send(entsoe.request('price', [AFTER])))
    assert _refused(lambda: t.send(entsoe.request('load_forecast', [guard.BOUNDARY, AFTER])))
    import pandas as pd
    week_after = int(pd.Timestamp(AFTER, tz='Europe/Berlin').tz_convert('UTC').value // 1_000_000)
    assert smard.bucket_days(week_after)[0] == AFTER       # a bucket's scope is the days it can hold
    assert _refused(lambda: t.send(smard.bucket_request('price', 'quarterhour', week_after)))
    run_after = guard.BOUNDARY                         # a run initialized at the boundary's 00 UTC
    for req in (gfs.listing_request(run_after, 21), gfs.idx_request(run_after, 21),
                gfs.message_request(run_after, 21, 0, 10, None)):
        assert _refused(lambda: t.send(req))
    assert _refused(lambda: t.send(gfs.idx_request(guard.BOUNDARY - timedelta(days=1), 51)))   # lead outside f021-f048


def test_an_admitted_request_is_the_only_one_that_reaches_the_network(no_network):
    with pytest.raises(TransportError) as exc:
        HttpTransport().send(gfs.idx_request(date(2026, 9, 5), 21))
    assert 'NetworkTouched' in str(exc.value)


def test_replay_transport_admits_through_the_guard_too(tmp_path):
    folder = ReplayFolder(tmp_path / 'r')
    with pytest.raises(guard.BoundaryRefused):
        folder.add(entsoe.request('price', [AFTER]), Response(200, {}, b'x', '2026-09-08T13:34:33Z'))


def test_credentials_are_refused_in_urls_and_headers():
    with pytest.raises(guard.CredentialRefused):
        Request('GET', entsoe.API, params=(('securityToken', 'x' * 12),), scope=('market', '2026-09-01')).admit()
    with pytest.raises(guard.CredentialRefused):
        Request('GET', entsoe.API, params=(('documentType', 'A44'),), headers=(('Authorization', 'y'),),
                scope=('market', '2026-09-01')).admit()
    with pytest.raises(guard.BoundaryRefused):
        Request('GET', entsoe.API, scope=('market',)).admit()


def test_the_entsoe_request_names_the_variable_not_the_value():
    req = entsoe.request('price', [date(2026, 9, 1)])
    assert req.credential == 'ENTSOE_API_TOKEN'
    red = json.dumps(req.redacted())
    assert 'securityToken' not in req.full_url() and 'securityToken' not in red
    assert dict(req.params)['periodStart'] == '202608312200' and dict(req.params)['periodEnd'] == '202609012200'


def test_the_live_transport_adds_the_token_inside_and_redacts_errors(monkeypatch):
    fake = 'fake-test-value-not-a-credential-0123456789'
    monkeypatch.setenv('CP18A_TEST_ONLY_VARIABLE', fake)
    seen = {}

    def opener(req, timeout=None):
        seen['has_token'] = fake in req.full_url
        raise OSError(f'failed for {req.full_url}')
    monkeypatch.setattr(urllib.request, 'urlopen', opener)
    req = Request('GET', entsoe.API, params=(('documentType', 'A44'),), credential='CP18A_TEST_ONLY_VARIABLE',
                  scope=('market', '2026-09-01'))
    with pytest.raises(TransportError) as exc:
        HttpTransport().send(req)
    assert seen['has_token'] is True
    assert fake not in str(exc.value) and '[REDACTED]' in str(exc.value)
    assert fake not in json.dumps(req.redacted())


def test_a_missing_credential_is_named_not_shown(monkeypatch, no_network):
    monkeypatch.delenv('CP18A_TEST_ONLY_VARIABLE', raising=False)
    req = Request('GET', entsoe.API, params=(('documentType', 'A44'),), credential='CP18A_TEST_ONLY_VARIABLE',
                  scope=('market', '2026-09-01'))
    with pytest.raises(CredentialMissing, match='CP18A_TEST_ONLY_VARIABLE is unset'):
        HttpTransport().send(req)


def test_replay_round_trip_miss_and_tamper(tmp_path):
    folder = ReplayFolder(tmp_path / 'r')
    req = gfs.idx_request(date(2026, 9, 5), 21)
    folder.add(req, Response(200, {'X': '1'}, b'hello idx', '2026-10-12T10:59:54Z', 'recorded', 'note'))
    folder.save()
    t = ReplayTransport(tmp_path / 'r')
    got = t.send(req)
    assert (got.status, got.body, got.retrieved_utc, got.provenance) == (200, b'hello idx', '2026-10-12T10:59:54Z', 'recorded')
    with pytest.raises(ReplayMiss):
        t.send(gfs.idx_request(date(2026, 9, 5), 24))
    entry = next(iter(json.loads((tmp_path / 'r' / 'index.json').read_text())['entries'].values()))
    (tmp_path / 'r' / entry['body']).write_bytes(gzip.compress(b'tampered', mtime=0))
    with pytest.raises(TransportError):
        ReplayTransport(tmp_path / 'r').send(req)


def test_request_keys_ignore_headers_and_credential_names():
    a = gfs.message_request(date(2026, 9, 5), 21, 0, 99, '"etag"')
    b = gfs.message_request(date(2026, 9, 5), 21, 0, 99, None)
    assert a.key() == b.key()
    assert a.key() != gfs.message_request(date(2026, 9, 5), 21, 0, 98, None).key()


#: Dates after the boundary that the package names, none of them a delivery day: the snapshot's pull, the
#: Owner's rulings and CP-25's retrieval, CP-26's cold rerun (a path), NCEP's last dated capture.
NOT_DELIVERY_DAYS = {'2026-09-08', '2026-10-12', '2026-10-15', '2026-09-23'}


def test_no_bare_environment_subscript_and_no_delivery_day_past_the_boundary():
    texts = {p: p.read_text() for p in SRC.rglob('*.py')}
    texts.update({p: p.read_text() for p in Path(__file__).parent.glob('test_live_*.py')})
    pattern = 'os.environ' + '['
    assert not [str(p) for p, t in texts.items() if pattern in t]
    found = set()
    for t in texts.values():
        for m in re.finditer(r'\b(20\d\d)-(\d\d)-(\d\d)\b', t):
            try:
                d = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                continue
            if d > guard.BOUNDARY:
                found.add(m.group(0))
    unexpected = sorted(found - NOT_DELIVERY_DAYS)
    assert not unexpected
