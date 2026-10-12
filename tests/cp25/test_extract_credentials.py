"""The guarded fetch path and the ledger (capstone v21-r13 §24.2, §24.6 item 9; AGENTS.md § Credentials).

No network: the HTTP session is replaced by fakes. Credential values are fake sentinels set with
monkeypatch; no real value is read, printed or compared.
"""
from __future__ import annotations

import json
import threading

import pytest

from cp20.budget import CapExceeded
from cp20.net import NetworkError, ObjectError
from cp25 import guard
from cp25.extract import GuardedFetcher, listing_url, parse_listing
from cp25.ledger import CAPS, GIB, Ledger

FAKE = {'DAGSHUB_USER_TOKEN': 'fake-dagshub-0123456789', 'MLFLOW_TRACKING_USERNAME': 'fake-mlflow-user-42',
        'MLFLOW_TRACKING_PASSWORD': 'fake-mlflow-pass-0123456789', 'ENTSOE_API_TOKEN': 'fake-entsoe-0123456789abcdef',
        'HF_TOKEN': 'hf_fake0123456789abcdef'}
OK_URL = 'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20220928/00/atmos/gfs.t00z.pgrb2.0p25.f024.idx'


@pytest.fixture
def fake_credentials(monkeypatch):
    for k, v in FAKE.items():
        monkeypatch.setenv(k, v)
    return FAKE


@pytest.fixture
def ledger(tmp_path):
    return Ledger.initialise(tmp_path / 'ledger.json')


class _Resp:
    def __init__(self, body=b'', status=200, raise_with=None):
        self.status_code, self.headers, self._body, self._raise = status, {'Content-Length': str(len(body))}, body, raise_with
        self.raw = self

    def stream(self, chunk, decode_content=False):
        if self._raise:
            raise self._raise
        yield self._body

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


class _Session:
    def __init__(self, resp):
        self.resp, self.calls, self.headers = resp, [], {}

    def get(self, url, headers=None, timeout=None, stream=False):
        self.calls.append({'url': url, 'headers': dict(headers or {}), 'session_headers': dict(self.headers)})
        return self.resp

    def close(self):
        pass


def _fetcher(ledger, tmp_path, session):
    f = GuardedFetcher(ledger, tmp_path / 'requests.jsonl', 1 * GIB, sleep=lambda s: True)
    f._local.session = session
    return f


def test_guard_refuses_before_any_request(ledger, tmp_path):
    session = _Session(_Resp(b'x'))
    f = _fetcher(ledger, tmp_path, session)
    for url in ('https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20260906/00/atmos/gfs.t00z.pgrb2.0p25.f024',
                'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20260905/00/atmos/gfs.t00z.pgrb2.0p25.f051',
                'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20220928/00/atmos/gfs.t00z.pgrb2.0p25.f024?token=abc'):
        with pytest.raises((guard.BoundaryRefused, guard.CredentialRefused)):
            f.get(url, 'test', max_body=10)
    assert session.calls == []
    assert not (tmp_path / 'requests.jsonl').exists()
    assert ledger.read()['counts'].get('transfer_bytes', 0) == 0


def test_admitted_request_is_charged_before_and_logged_without_query(ledger, tmp_path):
    session = _Session(_Resp(b'hello'))
    f = _fetcher(ledger, tmp_path, session)
    status, _, body = f.get(OK_URL, 'idx test', max_body=100)
    assert (status, body) == (200, b'hello')
    assert 'Authorization' not in session.calls[0]['headers'] and 'Authorization' not in session.calls[0]['session_headers']
    rec = json.loads((tmp_path / 'requests.jsonl').read_text())
    assert rec['url'] == OK_URL and rec['body_bytes'] == 5
    assert ledger.read()['counts']['transfer_bytes'] >= 100


def test_listing_request_carries_only_the_exact_prefix(ledger, tmp_path):
    xml = (b'<ListBucketResult><Contents><Key>gfs.20260905/00/atmos/gfs.t00z.pgrb2.0p25.f048</Key>'
           b'<LastModified>2026-09-05T03:47:47.000Z</LastModified><ETag>&quot;a&quot;</ETag><Size>549668818</Size></Contents>'
           b'<Contents><Key>gfs.20260905/00/atmos/gfs.t00z.pgrb2.0p25.f048.idx</Key><LastModified>2026-09-05T03:46:37.000Z'
           b'</LastModified><ETag>&quot;b&quot;</ETag><Size>41265</Size></Contents><IsTruncated>false</IsTruncated></ListBucketResult>')
    session = _Session(_Resp(xml))
    f = _fetcher(ledger, tmp_path, session)
    _, _, body = f.get(listing_url('2026-09-05', 48), 'listing', max_body=20_000)
    parsed = parse_listing(body)
    assert set(parsed['objects']) == {'gfs.20260905/00/atmos/gfs.t00z.pgrb2.0p25.f048', 'gfs.20260905/00/atmos/gfs.t00z.pgrb2.0p25.f048.idx'}
    assert parsed['objects']['gfs.20260905/00/atmos/gfs.t00z.pgrb2.0p25.f048']['last_modified'] == '2026-09-05T03:47:47.000Z'
    with pytest.raises(guard.BoundaryRefused):
        f.get(listing_url('2026-09-06', 21), 'listing', max_body=20_000)


def test_error_text_and_log_never_carry_a_credential(fake_credentials, ledger, tmp_path):
    # An object error whose exception text embeds every (fake) credential value.
    leak = ' '.join(fake_credentials.values())
    session = _Session(_Resp(b'', status=403))
    f = _fetcher(ledger, tmp_path, session)
    with pytest.raises(ObjectError) as err:
        f.get(OK_URL, f'purpose with {leak}', max_body=10)
    text = str(err.value) + (tmp_path / 'requests.jsonl').read_text()
    for value in fake_credentials.values():
        assert value not in text
    assert '[REDACTED:' in str(err.value)


def test_network_error_text_is_redacted(fake_credentials, ledger, tmp_path):
    session = _Session(_Resp(b'', raise_with=ConnectionError('connect failed ' + fake_credentials['ENTSOE_API_TOKEN'])))
    f = _fetcher(ledger, tmp_path, session)
    with pytest.raises(NetworkError) as err:   # the sleep returns True: a stop ends the retry loop
        f.get(OK_URL, 'idx', max_body=10)
    assert fake_credentials['ENTSOE_API_TOKEN'] not in str(err.value)
    log = (tmp_path / 'requests.jsonl').read_text()
    assert 'connect failed' in log and fake_credentials['ENTSOE_API_TOKEN'] not in log
    assert guard.scan([tmp_path]) == {}


def test_ledger_caps_and_worker_limit(ledger, tmp_path):
    assert CAPS['transfer_bytes'] == 40 * GIB and CAPS['machine_seconds'] == 24 * 3600 and CAPS['workers'] == 4
    with pytest.raises(CapExceeded):
        ledger.reserve(transfer_bytes=40 * GIB + 1)
    job = ledger.begin_job('a', 4)
    with pytest.raises(CapExceeded):
        ledger.begin_job('b', 1)
    ledger.charge_job(job, final=True, exit_code=0)
    ledger.begin_job('c', 1)
    with pytest.raises(CapExceeded):
        ledger.begin_job('d', 5)


def test_ledger_reserve_is_serialised(ledger):
    def work():
        for _ in range(20):
            ledger.reserve(requests=1)
    threads = [threading.Thread(target=work) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert ledger.read()['counts']['requests'] == 80
