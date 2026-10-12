"""§24.2's boundary guard, §24.4's issue time and the credential rule (capstone v21-r13 §24.6 item 9)."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pytest

from cp25 import guard
from cp25.guard import BoundaryRefused, CredentialRefused

UTC = timezone.utc


# ---- rows: the instants 2026-09-06 21:00 and 22:00 UTC (§24.2's named tests) -----------------

def test_row_2026_09_06_2100_utc_is_admitted():
    # 23:00 CEST on 2026-09-06: the last development hour.
    assert guard.admit_row(datetime(2026, 9, 6, 21, 0, tzinfo=UTC)) == date(2026, 9, 6)


def test_row_2026_09_06_2200_utc_is_refused():
    # 00:00 CEST on 2026-09-07: the first closed delivery day.
    with pytest.raises(BoundaryRefused):
        guard.admit_row(datetime(2026, 9, 6, 22, 0, tzinfo=UTC))


def test_batch_with_one_row_after_the_boundary_is_refused_whole():
    rows = [datetime(2026, 9, 6, 20, 0, tzinfo=UTC), datetime(2026, 9, 6, 21, 0, tzinfo=UTC),
            datetime(2026, 9, 6, 22, 0, tzinfo=UTC)]
    with pytest.raises(BoundaryRefused):
        guard.admit_rows(rows)
    assert guard.admit_rows(rows[:2]) == 2


def test_naive_row_is_refused():
    with pytest.raises(BoundaryRefused):
        guard.admit_row(datetime(2026, 9, 6, 12, 0))


def test_winter_boundary_uses_cet():
    # A CET day ends at 23:00 UTC: 2026-01-31 22:00 UTC is still 2026-01-31 local.
    assert guard.delivery_day(datetime(2026, 1, 31, 22, 0, tzinfo=UTC)) == date(2026, 1, 31)
    assert guard.delivery_day(datetime(2026, 1, 31, 23, 0, tzinfo=UTC)) == date(2026, 2, 1)


def test_delivery_day_after_boundary_is_refused():
    assert guard.admit_delivery_day(date(2026, 9, 6)) == date(2026, 9, 6)
    with pytest.raises(BoundaryRefused):
        guard.admit_delivery_day(date(2026, 9, 7))


# ---- GFS: the run's initialization, not its valid time --------------------------------------

def test_run_2026_09_06_00_utc_is_refused():
    with pytest.raises(BoundaryRefused):
        guard.admit_gfs(guard.run_init(date(2026, 9, 6)), 21)
    with pytest.raises(BoundaryRefused):
        guard.admit_url('https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20260906/00/atmos/gfs.t00z.pgrb2.0p25.f024')


def test_run_2026_09_05_00_utc_f048_is_admitted():
    # Valid 2026-09-07 00 UTC, after the boundary, but it serves delivery day 2026-09-06.
    init = guard.run_init(date(2026, 9, 5))
    guard.admit_gfs(init, 48)
    assert init + timedelta(hours=48) > datetime(2026, 9, 6, 22, 0, tzinfo=UTC)
    assert guard.served_delivery_day(date(2026, 9, 5)) == date(2026, 9, 6)
    parsed = guard.admit_url('https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20260905/00/atmos/gfs.t00z.pgrb2.0p25.f048')
    assert parsed == {'endpoint': 'aws', 'kind': 'aws_object', 'run': date(2026, 9, 5), 'lead': 48}


def test_any_later_run_and_intraday_cycle_is_refused():
    for d in (date(2026, 9, 7), date(2026, 12, 5)):
        with pytest.raises(BoundaryRefused):
            guard.admit_gfs(guard.run_init(d), 24)
    with pytest.raises(BoundaryRefused):  # 2026-09-05 12 UTC: not the 00 UTC cycle
        guard.admit_url('https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20260905/12/atmos/gfs.t12z.pgrb2.0p25.f024')
    with pytest.raises(BoundaryRefused):  # an instant after the cutoff, on the boundary run date
        guard.admit_gfs(datetime(2026, 9, 6, 6, 0, tzinfo=UTC), 21)


@pytest.mark.parametrize('lead', [0, 3, 18, 20, 49, 51, 120, 384])
def test_leads_outside_f021_f048_are_refused(lead):
    with pytest.raises(BoundaryRefused):
        guard.admit_gfs(guard.run_init(date(2026, 9, 5)), lead)


@pytest.mark.parametrize('lead', [21, 24, 27, 30, 33, 36, 39, 42, 45, 48])
def test_section_15_2_leads_are_admitted(lead):
    guard.admit_gfs(guard.run_init(date(2022, 9, 28)), lead)


def test_pre_2019_run_is_refused():
    with pytest.raises(BoundaryRefused):
        guard.admit_gfs(guard.run_init(date(2018, 12, 31)), 24)


def test_url_forms_of_both_archives():
    assert guard.admit_url('https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20221028/00/atmos/gfs.t00z.pgrb2.0p25.f021.idx')['kind'] == 'aws_index'
    listing = guard.admit_url('https://noaa-gfs-bdp-pds.s3.amazonaws.com/?list-type=2&prefix='
                              'gfs.20260905/00/atmos/gfs.t00z.pgrb2.0p25.f048')
    assert listing['kind'] == 'aws_listing' and listing['lead'] == 48
    ncar = guard.admit_url('https://tds.gdex.ucar.edu/thredds/fileServer/files/g/d084001/2026/20260905/gfs.0p25.2026090500.f048.grib2')
    assert ncar == {'endpoint': 'ncar', 'kind': 'ncar_object', 'run': date(2026, 9, 5), 'lead': 48}
    assert guard.admit_url('https://tds.gdex.ucar.edu/thredds/catalog/files/g/d084001/2026/20260905/catalog.xml')['kind'] == 'ncar_catalog'


@pytest.mark.parametrize('url', [
    'https://tds.gdex.ucar.edu/thredds/fileServer/files/g/d084001/2026/20260906/gfs.0p25.2026090600.f021.grib2',
    'https://tds.gdex.ucar.edu/thredds/catalog/files/g/d084001/2026/20260906/catalog.xml',
    'https://noaa-gfs-bdp-pds.s3.amazonaws.com/?list-type=2&prefix=gfs.20260906/00/atmos/gfs.t00z.pgrb2.0p25.f021',
    'https://noaa-gfs-bdp-pds.s3.amazonaws.com/?list-type=2&prefix=gfs.20260905/00/atmos/gfs.t00z.pgrb2.0p25.f0',
    'https://noaa-gfs-bdp-pds.s3.amazonaws.com/?list-type=2&prefix=gfs.20260905/',
    'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20260905/00/atmos/gfs.t00z.pgrb2.0p25.f051',
    'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20260905/00/atmos/gfs.t00z.pgrb2.1p00.f024',
    'https://example.org/gfs.20220928/00/atmos/gfs.t00z.pgrb2.0p25.f024',
    'http://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20220928/00/atmos/gfs.t00z.pgrb2.0p25.f024',
    'https://smard.de/app/chart_data/4169/DE/4169_DE_hour_1757282400000.json',
])
def test_refused_urls(url):
    with pytest.raises((BoundaryRefused, CredentialRefused)):
        guard.admit_url(url)


# ---- the issue time (§24.4) -------------------------------------------------------------------

def test_issue_time_cet_and_cest():
    assert guard.issue_time(date(2026, 1, 15)) == datetime(2026, 1, 14, 10, 0, tzinfo=UTC)
    assert guard.issue_time(date(2026, 7, 15)) == datetime(2026, 7, 14, 9, 0, tzinfo=UTC)


def test_issue_time_follows_d_minus_1_offset_on_transition_days():
    # D-1 = 2026-03-29 (spring forward at 01:00 UTC): 11:00 local is CEST, 09:00 UTC.
    assert guard.issue_time(date(2026, 3, 30)) == datetime(2026, 3, 29, 9, 0, tzinfo=UTC)
    # D-1 = 2025-10-26 (fall back at 01:00 UTC): 11:00 local is CET, 10:00 UTC.
    assert guard.issue_time(date(2025, 10, 27)) == datetime(2025, 10, 26, 10, 0, tzinfo=UTC)
    # D = the transition day itself takes the previous day's offset.
    assert guard.issue_time(date(2026, 3, 29)) == datetime(2026, 3, 28, 10, 0, tzinfo=UTC)
    assert guard.issue_time(date(2025, 10, 26)) == datetime(2025, 10, 25, 9, 0, tzinfo=UTC)


def test_strictly_before_the_issue_time():
    d = date(2026, 7, 15)
    at = guard.issue_time(d)
    assert guard.strictly_before(at - timedelta(seconds=1), d)
    assert not guard.strictly_before(at, d)
    assert not guard.strictly_before(at + timedelta(seconds=1), d)


# ---- credentials: no value in a URL, an error message or a log ---------------------------------

@pytest.mark.parametrize('url', [
    'https://user:pw@noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20220928/00/atmos/gfs.t00z.pgrb2.0p25.f024',
    'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.20220928/00/atmos/gfs.t00z.pgrb2.0p25.f024?securityToken=x',
    'https://noaa-gfs-bdp-pds.s3.amazonaws.com/?list-type=2&prefix=gfs.20220928/00/atmos/gfs.t00z.pgrb2.0p25.f024&X-Amz-Signature=x',
    'https://tds.gdex.ucar.edu/thredds/fileServer/files/g/d084001/2022/20220928/gfs.0p25.2022092800.f024.grib2?token=x',
])
def test_credential_bearing_urls_are_refused(url):
    with pytest.raises(CredentialRefused):
        guard.admit_url(url)


FAKE = {'DAGSHUB_USER_TOKEN': 'fake-dagshub-0123456789', 'MLFLOW_TRACKING_USERNAME': 'fake-mlflow-user-42',
        'MLFLOW_TRACKING_PASSWORD': 'fake-mlflow-pass-0123456789', 'ENTSOE_API_TOKEN': 'fake-entsoe-0123456789abcdef',
        'HF_TOKEN': 'hf_fake0123456789abcdef'}


@pytest.fixture
def fake_credentials(monkeypatch):
    for name, value in FAKE.items():
        monkeypatch.setenv(name, value)
    return FAKE


def test_redact_removes_every_stored_value(fake_credentials):
    text = ' | '.join(f'{k}={v}' for k, v in fake_credentials.items())
    text += ' https://web-api.tp.entsoe.eu/api?securityToken=' + fake_credentials['ENTSOE_API_TOKEN'] + '&documentType=A65'
    out = guard.redact(text)
    for value in fake_credentials.values():
        assert value not in out
    assert '[REDACTED:ENTSOE_API_TOKEN]' in out and 'documentType=A65' in out


def test_redact_strips_token_query_values_without_env():
    out = guard.redact('GET https://x.example/api?token=abc123def&prefix=gfs.2022 failed')
    assert 'abc123def' not in out and 'prefix=gfs.2022' in out


def test_scan_reports_names_never_values(fake_credentials, tmp_path):
    (tmp_path / 'clean.log').write_text('nothing here')
    (tmp_path / 'leak.log').write_text('oops ' + fake_credentials['HF_TOKEN'])
    found = guard.scan([tmp_path])
    assert found == {'HF_TOKEN': [str(tmp_path / 'leak.log')]}
    assert all(v not in repr(found) for v in fake_credentials.values())


def test_variables_set_reports_booleans_only(fake_credentials):
    flags = guard.variables_set()
    assert set(flags) == set(guard.CREDENTIAL_VARIABLES) and all(v is True for v in flags.values())
