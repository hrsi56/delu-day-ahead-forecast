"""CP-18a item 2: client parsing on small synthetic responses built at test time (no local data, no network).

SMARD: hourly and quarter-hour buckets, the snapshot's aggregation rules, fail-closed partial bins, DST days.
ENTSO-E: A44 PT60M and PT15M (A01, A03), A65 with absent positions, an acknowledgement. GFS: the listing, the
index and the 50 byte-range messages with their checks, on synthetic GRIB2-framed bytes.
"""
from __future__ import annotations

from datetime import date, timedelta
import json
import struct

import numpy as np
import pandas as pd
import pytest

from cp15.data import day_hours
from cp18.live import entsoe, gfs, smard
from cp18.live.transport import ReplayFolder, ReplayTransport, Response
from cp20.gfs import FIELDS, LEADS, idx_record

PULL = '2026-09-08T13:34:33Z'


def _ms(ts) -> int:
    return int(pd.Timestamp(ts).value // 1_000_000)


def _week(day: date) -> pd.Timestamp:
    monday = day - timedelta(days=day.weekday())
    return pd.Timestamp(monday, tz='Europe/Berlin').tz_convert('UTC')


def _smard_folder(tmp_path, input_name, res, day, value_of, created=None):
    start = _week(day)
    end = pd.Timestamp((start.tz_convert('Europe/Berlin') + pd.DateOffset(days=7)))
    step = '1h' if res == 'hour' else '15min'
    instants = pd.date_range(start, end.tz_convert('UTC'), freq=step, inclusive='left')
    series = [[_ms(t), value_of(t)] for t in instants]
    folder = ReplayFolder(tmp_path / 'smard')
    folder.add(smard.index_request(input_name, res),
               Response(200, {}, json.dumps({'timestamps': [_ms(start)]}).encode(), PULL, 'rendered'))
    folder.add(smard.bucket_request(input_name, res, _ms(start)),
               Response(200, {}, json.dumps({'meta_data': {'version': 1, 'created': created}, 'series': series}).encode(),
                        PULL, 'rendered'))
    folder.save()
    return ReplayTransport(tmp_path / 'smard')


def test_smard_hourly_price_before_the_transition(tmp_path):
    day = date(2025, 3, 30)                                      # 23-hour day
    t = _smard_folder(tmp_path, 'price', 'hour', day, lambda ts: float(ts.hour) + 0.25)
    f = smard.fetch(t, 'price', [day])
    hours = day_hours(day)
    assert len(hours) == 23 and not f.problems
    assert np.array_equal(f.values[day], np.array([h.hour + 0.25 for h in hours]))
    assert [e.role for e in f.exchanges] == ['index', 'bucket'] and f.exchanges[1].covers == [day]


def test_smard_quarter_hour_price_is_the_mean_of_four(tmp_path):
    day = date(2025, 10, 26)                                     # 25-hour day, quarter-hour product
    t = _smard_folder(tmp_path, 'price', 'quarterhour', day, lambda ts: float(ts.minute))
    f = smard.fetch(t, 'price', [day])
    assert len(f.values[day]) == 25 and np.all(f.values[day] == 22.5) and not f.problems


def test_smard_load_is_the_sum_of_four_and_partial_bins_fail_closed(tmp_path):
    day = date(2026, 9, 1)
    bad = pd.Timestamp(day_hours(day)[5]) + pd.Timedelta(minutes=30)

    def value(ts):
        return None if ts == bad else 1000.25
    t = _smard_folder(tmp_path, 'load_forecast', 'quarterhour', day, value, created=1788000000000)
    f = smard.fetch(t, 'load_forecast', [day])
    v = f.values[day]
    assert np.isnan(v[5]) and np.all(np.delete(v, 5) == 4001.0)
    assert any('partial quarter-hour' in p for p in f.problems)
    assert f.exchanges[1].document_time_utc is not None


def test_smard_null_hour_stays_missing(tmp_path):
    day = date(2026, 9, 1)
    gap = day_hours(day)[3]
    t = _smard_folder(tmp_path, 'load_forecast', 'quarterhour', day,
                      lambda ts: None if ts.floor('h') == gap else 10.0)
    f = smard.fetch(t, 'load_forecast', [day])
    assert np.isnan(f.values[day][3]) and not any('partial' in p for p in f.problems)


def _a44(day, res, values, curve='A01', skip=()):
    hours = day_hours(day)
    start, end = hours[0], hours[-1] + pd.Timedelta(hours=1)
    pts = ''.join(f'<Point><position>{i + 1}</position><price.amount>{v}</price.amount></Point>'
                  for i, v in enumerate(values) if i + 1 not in skip)
    fmt = '%Y-%m-%dT%H:%MZ'
    return (f'<?xml version="1.0"?><Publication_MarketDocument xmlns="urn:x"><createdDateTime>2026-09-01T10:00:00Z'
            f'</createdDateTime><type>A44</type><TimeSeries><in_Domain.mRID codingScheme="A01">{entsoe.DELU}</in_Domain.mRID>'
            f'<curveType>{curve}</curveType><Period><timeInterval><start>{start.strftime(fmt)}</start>'
            f'<end>{end.strftime(fmt)}</end></timeInterval><resolution>{res}</resolution>{pts}</Period></TimeSeries>'
            '</Publication_MarketDocument>').encode()


def _entsoe_transport(tmp_path, input_name, day, body):
    folder = ReplayFolder(tmp_path / 'e')
    folder.add(entsoe.request(input_name, [day]), Response(200, {}, body, PULL, 'rendered'))
    folder.save()
    return ReplayTransport(tmp_path / 'e')


def test_entsoe_a44_hourly_and_document_time(tmp_path):
    day = date(2025, 3, 30)
    vals = [float(i) * 1.5 for i in range(23)]
    f = entsoe.fetch(_entsoe_transport(tmp_path, 'price', day, _a44(day, 'PT60M', vals)), 'price', [day])
    assert np.array_equal(f.values[day], np.array(vals)) and not f.problems
    assert f.exchanges[0].document_time_utc == '2026-09-01T10:00:00Z'


def test_entsoe_a44_quarter_hour_a03_carries_forward(tmp_path):
    day = date(2026, 9, 1)
    n = 96
    vals = [float(i // 8) for i in range(n)]                     # constant runs of 8 quarters
    skip = {i + 1 for i in range(n) if i % 8}                    # A03 omits the repeats
    body = _a44(day, 'PT15M', vals, curve='A03', skip=skip)
    f = entsoe.fetch(_entsoe_transport(tmp_path, 'price', day, body), 'price', [day])
    assert np.array_equal(f.values[day], np.repeat(np.arange(12.0), 2)) and not f.problems


def test_entsoe_a65_absent_positions_are_missing(tmp_path):
    day = date(2026, 9, 1)
    hours = day_hours(day)
    fmt = '%Y-%m-%dT%H:%MZ'
    pts = ''.join(f'<Point><position>{i}</position><quantity>{40000 + i}</quantity></Point>' for i in range(1, 97) if i != 9)
    body = (f'<GL_MarketDocument xmlns="urn:y"><createdDateTime>2026-09-01T07:00:00Z</createdDateTime><TimeSeries>'
            f'<outBiddingZone_Domain.mRID>{entsoe.DELU}</outBiddingZone_Domain.mRID><curveType>A01</curveType><Period>'
            f'<timeInterval><start>{hours[0].strftime(fmt)}</start><end>{(hours[-1] + pd.Timedelta(hours=1)).strftime(fmt)}'
            f'</end></timeInterval><resolution>PT15M</resolution>{pts}</Period></TimeSeries></GL_MarketDocument>').encode()
    f = entsoe.fetch(_entsoe_transport(tmp_path, 'load_forecast', day, body), 'load_forecast', [day])
    v = f.values[day]
    assert np.isnan(v[2]) and v[0] == 40002.5 and any('partial' in p for p in f.problems)


def test_entsoe_acknowledgement_is_no_data(tmp_path):
    day = date(2026, 9, 1)
    body = b'<Acknowledgement_MarketDocument xmlns="urn:z"><Reason><code>999</code><text>No matching data found</text></Reason></Acknowledgement_MarketDocument>'
    f = entsoe.fetch(_entsoe_transport(tmp_path, 'price', day, body), 'price', [day])
    assert np.isnan(f.values[day]).all() and any('No matching data' in p for p in f.problems)


# ------------------------------------------------------------------------------------------------ GFS
def _grib(n: int, tag: int) -> bytes:
    body = bytes([tag % 251]) * (n - 20)
    total = 16 + len(body) + 4
    return b'GRIB' + b'\x00\x00' + b'\x00' + b'\x02' + struct.pack('>Q', total) + body + b'7777'


def _gfs_folder(tmp_path, run, *, corrupt=None, index_lm='2024-06-01T03:45:00.000Z'):
    folder = ReplayFolder(tmp_path / 'g')
    order = ('u10', 'v10', 'dswrf', 'u100', 'v100')
    for lead in LEADS:
        msgs, lines, off = {}, [], 0
        for i, f in enumerate(order):
            m = _grib(64 + i, lead + i)
            msgs[f] = (off, m)
            lines.append(f'{i + 1}:{off}:d={run:%Y%m%d}00{idx_record(f, lead)}')
            off += len(m)
        lines.append(f'6:{off}:d={run:%Y%m%d}00:TMP:2 m above ground:{lead} hour fcst:')
        size = off + 50
        idx = ('\n'.join(lines) + '\n').encode()
        key = gfs.stem(run, lead)
        listing = ('<ListBucketResult><IsTruncated>false</IsTruncated>'
                   f'<Contents><Key>{key}</Key><LastModified>2024-06-01T03:50:00.000Z</LastModified><ETag>&quot;e{lead}&quot;</ETag><Size>{size}</Size></Contents>'
                   f'<Contents><Key>{key}.idx</Key><LastModified>{index_lm}</LastModified><ETag>&quot;i{lead}&quot;</ETag><Size>{len(idx)}</Size></Contents>'
                   '</ListBucketResult>').encode()
        folder.add(gfs.listing_request(run, lead), Response(200, {}, listing, '2024-06-01T08:00:00Z'))
        folder.add(gfs.idx_request(run, lead), Response(200, {}, idx, '2024-06-01T08:00:01Z'))
        for f, (o, m) in msgs.items():
            if corrupt == (lead, f):
                m = m[:-4] + b'XXXX'
            folder.add(gfs.message_request(run, lead, o, o + len(m) - 1, None),
                       Response(206, {'Content-Range': f'bytes {o}-{o + len(m) - 1}/{size}'}, m, '2024-06-01T08:00:02Z'))
    folder.save()
    return ReplayTransport(tmp_path / 'g')


def test_gfs_client_retrieves_and_checks_the_fifty_messages(tmp_path):
    run = date(2024, 6, 1)
    r = gfs.retrieve_run(_gfs_folder(tmp_path, run), run, tmp_path / 'raw')
    assert r.complete and len(r.messages) == len(LEADS) * len(FIELDS) and not r.problems
    m = r.messages[0]
    assert m['url'].endswith('atmos/gfs.t00z.pgrb2.0p25.f021') and m['bytes'] == 64
    assert (tmp_path / 'raw' / run.isoformat() / m['raw_file']).read_bytes()[:4] == b'GRIB'
    from cp18.live import availability as A
    pub = A.gfs_publication({k: {kk: vv for kk, vv in v.items() if kk in ('object', 'index')} for k, v in r.listing.items()}, None)
    assert pub['basis_id'] == 'aws_last_modified' and pub['utc'] == '2024-06-01T03:50:00Z'


def test_gfs_client_refuses_a_broken_frame(tmp_path):
    run = date(2024, 6, 1)
    r = gfs.retrieve_run(_gfs_folder(tmp_path, run, corrupt=(27, 'dswrf')), run, tmp_path / 'raw')
    assert not r.complete and any('f027 dswrf' in p and '7777' in p for p in r.problems)


def test_gfs_client_records_a_missing_lead(tmp_path):
    run = date(2024, 6, 1)
    t = _gfs_folder(tmp_path, run)
    del t.index[gfs.idx_request(run, 48).key()]
    r = gfs.retrieve_run(t, run, tmp_path / 'raw')
    assert not r.complete and any(p.startswith('f048: index not retrieved') for p in r.problems)
