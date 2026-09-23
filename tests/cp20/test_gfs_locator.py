"""Synthetic GRIB2 framing, NCAR adaptive-locator and metadata-validation controls.

No network, no real target-message decoding (so no message-attempt allowance is used):
byte streams are synthetic and real admission metadata is read from committed JSON.
"""
import datetime as dt
import json
from pathlib import Path
import struct

import pytest

from cp20 import gfs

ROOT = Path(__file__).resolve().parents[2]
RUN = dt.date(2019, 6, 13)


def message(run, cat, num, surf, level, template, ftime, size):
    sec1 = struct.pack('>IBHHBBBHBBBBBBB', 21, 1, 7, 0, 2, 1, 1, run.year, run.month, run.day, 0, 0, 0, 0, 1)
    sec3 = struct.pack('>IB', 72, 3) + b'\0' * 67
    scale, value = (0, int(level)) if surf == 103 else (0, 0)
    sec4 = struct.pack('>IBHHBBBBBHBBIBbI', 34, 4, 0, template, cat, num, 2, 0, 96, 0, 0, 1, ftime, surf, scale, value)
    sec4 += b'\0' * (34 - len(sec4))
    body_len = size - 16 - len(sec1) - len(sec3) - len(sec4) - 4
    assert body_len > 0
    total = 16 + len(sec1) + len(sec3) + len(sec4) + body_len + 4
    sec0 = b'GRIB' + b'\0\0' + bytes([0, 2]) + struct.pack('>Q', total)
    # Filler must not accidentally contain a plausible header.
    return sec0 + sec1 + sec3 + sec4 + b'\x55' * body_len + b'7777'


def synthetic_file(run, lead, filler=200_000):
    parts, layout = [], {}
    def add(name, blob):
        layout[name] = (sum(map(len, parts)), len(blob))
        parts.append(blob)
    for i in range(30):
        add(f'pre{i}', message(run, 0, 0, 100, 0, 0, lead, filler + 997 * i))
    add('u10', message(run, 2, 2, 103, 10, 0, lead, 300_000))
    add('v10', message(run, 2, 3, 103, 10, 0, lead, 290_000))
    for i in range(12):
        add(f'mid{i}', message(run, 0, 1, 1, 0, 0, lead, filler + 13 * i))
    a, _ = gfs.dswrf_bounds(lead)
    add('dswrf', message(run, 4, 192, 1, 0, 8, a, 120_000))
    for i in range(12):
        add(f'late{i}', message(run, 0, 1, 1, 0, 0, lead, filler + 7 * i))
    add('u100', message(run, 2, 2, 103, 100, 0, lead, 310_000))
    add('v100', message(run, 2, 3, 103, 100, 0, lead, 305_000))
    for i in range(10):
        add(f'post{i}', message(run, 0, 3, 1, 0, 0, lead, filler))
    return b''.join(parts), layout


class FakeFetcher:
    def __init__(self, data):
        self.data, self.calls = data, []

    def get(self, url, purpose, *, byte_range=None, max_body=None):
        a, b = byte_range
        self.calls.append((purpose, a, b))
        return 206, {'Content-Range': f'bytes {a}-{b}/{len(self.data)}'}, self.data[a:b + 1]


def locate(data, lead, prior_frac_by_anchor, group):
    priors = {(gfs.version(RUN), lead, anchor): [(RUN - dt.timedelta(days=3), frac)]
              for anchor, frac in prior_frac_by_anchor.items()}
    loc = gfs.NcarLocator(FakeFetcher(data), gfs.OffsetModel(priors))
    trace = []
    found, window = loc.find_group('https://tds.gdex.ucar.edu/x', RUN, lead, len(data), group, trace)
    return loc, found, window, trace


@pytest.mark.parametrize('lead', [21, 24])
@pytest.mark.parametrize('shift', [-3_000_000, -600_000, 0, 250_000, 1_500_000])
def test_locator_finds_each_group_from_imperfect_predictions(lead, shift):
    data, layout = synthetic_file(RUN, lead)
    for group in gfs.GROUPS:
        true = layout[group[0]][0]
        loc, found, window, trace = locate(data, lead, {group[0]: (true + shift) / len(data)}, group)
        for name in group:
            assert (found[name].offset, found[name].length) == layout[name]
        first, blob, reused = loc.payload('https://tds.gdex.ucar.edu/x', RUN, lead, found, window, 'p')
        start, end = layout[group[0]][0], layout[group[-1]][0] + layout[group[-1]][1]
        assert first == start and blob == data[start:end]
        for name in group:
            o, n = layout[name]
            gfs.check_frame(blob[o - first:o - first + n], n)


def test_overshoot_is_detected_and_recovered_with_a_wider_window():
    data, layout = synthetic_file(RUN, 21)
    # Prediction far past u10/v10: the chain sees dswrf (later in file order) and backs off.
    _, found, _, trace = locate(data, 21, {'u10': (layout['u100'][0]) / len(data)}, ('u10', 'v10'))
    assert found['u10'].offset == layout['u10'][0]
    assert any(t['overshoot'] for t in trace)


def test_wrong_lead_or_wrong_average_is_not_identified_as_a_target():
    info = gfs.parse_header(message(RUN, 2, 2, 103, 10, 0, 24, 10_000)[:320])
    assert gfs.identify(info, 24) == 'u10' and gfs.identify(info, 21) is None
    dsw = gfs.parse_header(message(RUN, 4, 192, 1, 0, 8, 18, 10_000)[:320])
    assert gfs.identify(dsw, 24) == 'dswrf' and gfs.identify(dsw, 21) == 'dswrf'
    assert gfs.identify(dsw, 27) is None  # 24-27 average required at f027
    other_run = gfs.parse_header(message(RUN + dt.timedelta(days=1), 2, 2, 103, 10, 0, 24, 10_000)[:320])
    assert not gfs.plausible(other_run, RUN) and gfs.plausible(info, RUN)


def test_framing_refuses_truncated_or_unterminated_messages():
    msg = message(RUN, 2, 2, 103, 10, 0, 24, 10_000)
    gfs.check_frame(msg, len(msg))
    with pytest.raises(gfs.IntegrityError):
        gfs.check_frame(msg[:-1])
    with pytest.raises(gfs.IntegrityError):
        gfs.check_frame(msg[:-4] + b'7778')
    with pytest.raises(gfs.IntegrityError):
        gfs.check_frame(msg, len(msg) + 1)


def admission_meta(run, lead, name):
    d = json.loads((ROOT / f'reports/weather-admission/decoded/gfs_{run}.json').read_text())
    meta = dict(d['leads'][f'f{lead:03d}']['fields'][name]['meta'])
    # Keys this validator reads that the admission decoder did not record; values documented
    # in dossier section 4.1/5.2 (0.25 deg global grid, 90N 0E first point, GRIB edition 2).
    meta.update(iScansNegatively=0, numberOfDataPoints=1440 * 721, editionNumber=2,
                typeOfFirstFixedSurface=1 if name == 'ssrd' else 103)
    return meta


@pytest.mark.parametrize('run,lead,name,field', [('2019-01-01', 21, 'u10', 'u10'), ('2019-01-01', 24, 'ssrd', 'dswrf'),
                                                 ('2019-06-13', 21, 'v_hub', 'v100'), ('2022-08-25', 24, 'ssrd', 'dswrf'),
                                                 ('2022-08-25', 21, 'u_hub', 'u100')])
def test_real_admission_metadata_validates_positive_control(run, lead, name, field):
    gfs.validate(admission_meta(run, lead, name), dt.date.fromisoformat(run), lead, field)


@pytest.mark.parametrize('mutation', [dict(units='m/s'), dict(level=80), dict(typeOfLevel='isobaricInhPa'),
                                      dict(startStep=18), dict(dataDate=20190102), dict(centre='ecmf'),
                                      dict(productionStatusOfProcessedData=1), dict(typeOfGeneratingProcess=0),
                                      dict(Ni=720), dict(stepType='avg'), dict(generatingProcessIdentifier=81)])
def test_contradicting_metadata_stops_negative_control(mutation):
    meta = admission_meta('2019-01-01', 21, 'u10')
    meta.update(mutation)
    with pytest.raises(gfs.Contradiction):
        gfs.validate(meta, dt.date(2019, 1, 1), 21, 'u10')


@pytest.mark.parametrize('mutation', [dict(startStep=21), dict(endStep=21), dict(typeOfStatisticalProcessing=1),
                                      dict(units='J m**-2'), dict(lengthOfTimeRange=3)])
def test_radiation_averaging_bounds_are_validated_not_inferred_from_lead(mutation):
    meta = admission_meta('2019-01-01', 24, 'ssrd')
    gfs.validate(meta, dt.date(2019, 1, 1), 24, 'dswrf')
    meta.update(mutation)
    with pytest.raises(gfs.Contradiction):
        gfs.validate(meta, dt.date(2019, 1, 1), 24, 'dswrf')


def test_version_evidence_ties_precision_and_path_to_the_run_date():
    coarse = {'packing_quantum': 10.0}
    fine = {'packing_quantum': 0.015625}
    gfs.version_evidence(dt.date(2019, 1, 1), 'dswrf', coarse, 'ncar', gfs.ncar_url(dt.date(2019, 1, 1), 24))
    gfs.version_evidence(dt.date(2022, 8, 25), 'dswrf', fine, 'aws', gfs.aws_url(dt.date(2022, 8, 25), 24))
    with pytest.raises(gfs.Contradiction):
        gfs.version_evidence(dt.date(2019, 1, 1), 'dswrf', fine, 'ncar', gfs.ncar_url(dt.date(2019, 1, 1), 24))
    with pytest.raises(gfs.Contradiction):
        gfs.version_evidence(dt.date(2022, 8, 25), 'u10', fine, 'aws',
                             gfs.aws_url(dt.date(2022, 8, 25), 24).replace('atmos/', ''))


def test_idx_parsing_requires_exact_unique_records():
    lines = ['1:0:d=2022082500:TMP:2 m above ground:24 hour fcst:',
             '2:100:d=2022082500:UGRD:10 m above ground:24 hour fcst:',
             '3:250:d=2022082500:VGRD:10 m above ground:24 hour fcst:',
             '4:400:d=2022082500:DSWRF:surface:18-24 hour ave fcst:',
             '5:500:d=2022082500:UGRD:100 m above ground:24 hour fcst:',
             '6:650:d=2022082500:VGRD:100 m above ground:24 hour fcst:',
             '7:800:d=2022082500:TMP:surface:24 hour fcst:']
    found = gfs.parse_idx('\n'.join(lines), dt.date(2022, 8, 25), 24)
    assert found['dswrf'] == {'offset': 400, 'end': 499, 'idx_line': lines[3]}
    with pytest.raises(gfs.Contradiction):  # wrong averaging window at this lead
        gfs.parse_idx('\n'.join(lines).replace('18-24 hour ave', '0-24 hour ave'), dt.date(2022, 8, 25), 24)
    with pytest.raises(gfs.Contradiction):  # duplicate target record
        gfs.parse_idx('\n'.join(lines + ['8:900:d=2022082500:UGRD:10 m above ground:24 hour fcst:']),
                      dt.date(2022, 8, 25), 24)


def test_box_is_the_fixed_inclusive_proxy_grid():
    assert gfs.BOX_LATS[0] == 55.25 and gfs.BOX_LATS[-1] == 47.0 and len(gfs.BOX_LATS) == 34
    assert gfs.BOX_LONS[0] == 5.5 and gfs.BOX_LONS[-1] == 15.5 and len(gfs.BOX_LONS) == 41
