"""CP-18a item 2: the input archive, the GFS flag from archived evidence, history assembly and `build_day`'s
early outcomes. No local data: the market responses are rendered at test time from the committed snapshot, and
the decoded GFS run is synthetic. Dates past the boundary are computed, never written or printed.
"""
from __future__ import annotations

from datetime import date, timedelta
import gzip
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cp15.data import day_hours
from cp18.live import archive as AR
from cp18.live import build, gfs, history as Hs, recorded, smard
from cp18.live.transport import ReplayTransport
from cp20.gfs import dswrf_bounds
from cp20.weather import BOX_LATS, BOX_LONS, COLUMNS, FIELDS, LEADS
from cp25 import guard

ROOT = Path(__file__).resolve().parents[2]
AFTER = guard.BOUNDARY + timedelta(days=1)


# ------------------------------------------------------------------------------------------------ storage
def test_archive_is_append_only_hashed_and_verifiable(tmp_path):
    a = AR.Archive(tmp_path)
    day = date(2026, 9, 1)
    rec = {'id': 'x-1', 'input': 'price', 'source': 'smard', 'provenance': 'rendered', 'covers': ['2026-08-31'],
           'publication': {}}
    stored = a.add(day, rec, body=b'{"series": []}')
    assert stored['sha256'] == hashlib.sha256(b'{"series": []}').hexdigest() and stored['bytes'] == 14
    assert a.add(day, rec, body=b'{"series": []}') == stored                  # idempotent
    with pytest.raises(AR.ArchiveError):
        a.add(day, rec, body=b'other')                                          # append-only
    assert a.verify(day) == [] and a.days() == [day] and a.size(day)['bytes'] > 0
    (a.day_dir(day) / stored['body']).write_bytes(gzip.compress(b'tampered', mtime=0))
    assert a.verify(day) and 'differs from its SHA-256' in a.verify(day)[0]


def test_archive_refuses_days_past_the_boundary(tmp_path):
    a = AR.Archive(tmp_path)
    with pytest.raises(guard.BoundaryRefused):
        a.day_dir(AFTER)
    with pytest.raises(guard.BoundaryRefused):
        a.add(date(2026, 9, 6), {'id': 'y', 'input': 'price', 'covers': [AFTER.isoformat()], 'publication': {}}, body=b'1')


# ------------------------------------------------------------------------------------------------ market records
@pytest.fixture(scope='module')
def snap():
    return recorded.snapshot(ROOT)


def _market_archive(tmp, snap, days, *, skip_load_of=None):
    """Development archive days with rendered SMARD responses (no GFS record)."""
    recorded.render_smard(tmp / 'replay', snap, recorded.market_days(days))
    t = ReplayTransport(tmp / 'replay')
    a = AR.Archive(tmp / 'archive')
    for x in days:
        AR.store_market(a, x, smard.fetch(t, 'price', [x - timedelta(days=k) for k in (3, 2, 1)]), development_snapshot=True)
        if x != skip_load_of:
            AR.store_market(a, x, smard.fetch(t, 'load_forecast', [x]), development_snapshot=True)
    return a


def test_market_records_carry_their_evidence(tmp_path, snap):
    day = date(2026, 9, 6)
    a = _market_archive(tmp_path, snap, [day])
    recs = a.records(day)
    price = [r for r in recs if r['input'] == 'price']
    load = [r for r in recs if r['input'] == 'load_forecast']
    assert sorted(c for r in price for c in r['covers']) == ['2026-09-03', '2026-09-04', '2026-09-05']
    assert all(r['provenance'] == 'rendered' and 'not a recorded raw response' in r['origin'] for r in recs)
    assert price[0]['publication'][price[0]['covers'][0]]['basis_id'] == 'documented_schedule'
    pub = load[0]['publication']['2026-09-06']
    assert pub['basis_id'] == 'ruling_1_exception' and 'development data only' in pub['basis']
    assert all(r['retrieved_utc'] == AR.SNAPSHOT_PULLED_UTC and r['document_time_utc'] is None for r in recs)
    assert a.verify(day) == []


# ------------------------------------------------------------------------------------------------ GFS
def _decoded_run(run: date, *, nan_cell=False) -> tuple[bytes, bytes]:
    rng = np.random.default_rng(7)
    data = np.empty((len(FIELDS), len(LEADS), len(BOX_LATS), len(BOX_LONS)))
    data[:4] = rng.normal(0.0, 5.0, (4, len(LEADS), len(BOX_LATS), len(BOX_LONS)))
    data[FIELDS.index('dswrf')] = 100.0
    if nan_cell:
        data[0, 3, 5, 5] = np.nan
    buf = io.BytesIO()
    np.savez_compressed(buf, data=data, lats=BOX_LATS, lons=BOX_LONS, fields=np.array(FIELDS), leads=np.array(LEADS))
    npz = buf.getvalue()
    messages, k = [], 0
    for lead in LEADS:
        for f in FIELDS:
            a, b = dswrf_bounds(lead) if f == 'dswrf' else (lead, lead)
            messages.append({'field': f, 'lead': lead, 'endpoint': 'aws', 'url': gfs.aws_url(run, lead),
                             'byte_range': [k * 100, k * 100 + 99], 'idx_line': f'{k}:{k * 100}:d={run:%Y%m%d}00:X:',
                             'idx_sha256': '0' * 64, 'bytes': 100, 'sha256': f'{k:064x}', 'retrieved_utc': '2024-06-01T08:00:00Z',
                             'packing_quantum': 0.01, 'meta': {'startStep': a, 'endStep': b}})
            k += 1
    record = {'status': 'complete', 'run_00z': run.isoformat(), 'delivery_day': (run + timedelta(days=1)).isoformat(),
              'version': 'v16', 'npz_sha256': hashlib.sha256(npz).hexdigest(), 'messages': messages}
    return json.dumps(record).encode(), npz


def _listing(last_modified):
    return {f'f{lead:03d}': {'object': {'last_modified': last_modified, 'size': 10, 'etag': 'e'},
                             'index': {'last_modified': last_modified, 'size': 5, 'etag': 'i'}, 'retrieved_utc': None}
            for lead in LEADS}


@pytest.mark.parametrize('case, lm, nan_cell, available, status', [
    ('on time', '2024-06-01T03:50:00.000Z', False, True, 'ok'),
    ('late (ruling 4)', '2024-06-01T15:10:00.000Z', False, False, 'documented_lateness'),
    ('at the cutoff', '2024-06-01T09:00:00.000Z', False, False, 'documented_lateness'),
    ('invalid vector', '2024-06-01T03:50:00.000Z', True, False, 'invalid_support'),
])
def test_gfs_flag_from_archived_evidence(tmp_path, case, lm, nan_cell, available, status):
    run = date(2024, 6, 1)
    day = run + timedelta(days=1)
    js, npz = _decoded_run(run, nan_cell=nan_cell)
    a = AR.Archive(tmp_path)
    AR.store_gfs(a, day, run=run, run_json=js, run_npz=npz, listing=_listing(lm), reconstructed=None,
                 provenance='recorded', origin='synthetic test run')
    assert a.verify(day) == []
    g = Hs.gfs_for_day(a, day)
    assert g['available'] is available and g['status'] == status, case
    feats = g['features']
    assert list(feats.timestamp_utc) == list(day_hours(day))
    finite = np.isfinite(feats[list(COLUMNS)].to_numpy())
    assert finite.all() if available else not finite.any()          # a False flag sets every hour missing


def test_gfs_without_any_record_is_unavailable(tmp_path):
    g = Hs.gfs_for_day(AR.Archive(tmp_path), date(2024, 6, 2))
    assert not g['available'] and 'no archived evidence' in g['reason']


def test_gfs_tampered_decoded_run_is_caught(tmp_path):
    run = date(2024, 6, 1)
    js, npz = _decoded_run(run)
    a = AR.Archive(tmp_path)
    rec = AR.store_gfs(a, run + timedelta(days=1), run=run, run_json=js, run_npz=npz,
                       listing=_listing('2024-06-01T03:50:00.000Z'), reconstructed=None, provenance='recorded', origin='t')
    (a.day_dir(run + timedelta(days=1)) / next(r for r in rec['files'] if r.endswith('.npz'))).write_bytes(b'x')
    assert a.verify(run + timedelta(days=1))
    assert not Hs.gfs_for_day(a, run + timedelta(days=1))['available']


# ------------------------------------------------------------------------------------------------ history
def test_history_ends_at_d_without_ds_price(tmp_path, snap):
    day, base_end = date(2026, 9, 6), date(2026, 9, 3)
    a = _market_archive(tmp_path, snap, [base_end + timedelta(days=i) for i in range(1, 4)])
    h = Hs.assemble(ROOT, a, day, base_end)
    f = h.frame
    assert max(f.delivery_date) == day and max(h.features.delivery_date) == day
    on_d = pd.Index(f.delivery_date) == day
    assert np.isnan(f.price_eur_mwh[on_d]).all()                     # the embargo
    inc = (pd.Index(f.delivery_date) > base_end) & ~on_d
    want = snap.loc[pd.DatetimeIndex(f.timestamp_utc[inc]).tz_convert('UTC').as_unit('ns'), 'price_eur_mwh'].to_numpy()
    assert np.array_equal(f.price_eur_mwh[inc].to_numpy().view(np.uint64), want.view(np.uint64))
    load_d = [j for j in h.judgements if j['input'] == 'load_forecast' and j['data_day'] == day.isoformat()][0]
    assert load_d['admitted'] and load_d['by_exception']
    assert h.gfs[day.isoformat()]['available'] is False                # no GFS archived here
    assert h.features.loc[h.features.delivery_date > base_end, list(COLUMNS)].isna().all().all()
    truth = h.truth()
    keys = day_hours(day - timedelta(days=2))
    assert np.array_equal(truth(keys), snap.loc[keys.as_unit('ns'), 'price_eur_mwh'].to_numpy())
    assert np.isnan(truth(day_hours(day))).all()                      # D's prices are never truth here


def test_history_never_reads_an_archive_day_after_d(tmp_path, snap):
    day, base_end = date(2026, 9, 5), date(2026, 9, 2)
    a = _market_archive(tmp_path, snap, [date(2026, 9, 3), date(2026, 9, 4), date(2026, 9, 6)])
    h = Hs.assemble(ROOT, a, day, base_end)
    # D = 09-05 has no archive day of its own; its load forecast exists only in no archive day <= D
    assert any('load forecast of 2026-09-05' in m for m in h.missing_required)


def test_build_day_early_outcomes(tmp_path, snap):
    day, base_end = date(2026, 9, 6), date(2026, 9, 3)
    a = _market_archive(tmp_path / 'a', snap, [base_end + timedelta(days=i) for i in range(1, 4)])
    empty = tmp_path / 'search'
    empty.mkdir()
    r = build.build_day(day, archive=a, base_end=base_end, buffers={}, search_dir=empty, out=tmp_path / 'o', root=ROOT)
    assert r['status'] == 'search_state_missing' and r['search']['k'] == 13 and not r['payloads']
    assert r['availability']['shown'] is True and r['gfs_available'] is False
    assert r['availability']['by_exception']
    b = _market_archive(tmp_path / 'b', snap, [base_end + timedelta(days=i) for i in range(1, 4)], skip_load_of=day)
    r = build.build_day(day, archive=b, base_end=base_end, buffers={}, search_dir=empty, out=tmp_path / 'o', root=ROOT)
    assert r['availability']['shown'] is False and any('load forecast of 2026-09-06' in x for x in r['availability']['reasons'])
    json.dumps(r)                                                     # the result is a JSON record
    with pytest.raises(guard.BoundaryRefused):
        build.build_day(AFTER, archive=a, base_end=base_end, buffers={}, search_dir=empty, out=tmp_path / 'o', root=ROOT)
