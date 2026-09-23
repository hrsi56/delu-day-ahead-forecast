"""Synthetic ecCodes round trip for the decode/validation path (extraction environment only).

Messages are built locally from ecCodes' GRIB2 sample, so no target message is decoded
and no attempt allowance is used. Skipped in the modelling environment (no ecCodes).
"""
import datetime as dt

import numpy as np
import pytest

eccodes = pytest.importorskip('eccodes')
from cp20 import gfs  # noqa: E402


def synthetic(run, lead, field, **override):
    g = eccodes.codes_grib_new_from_samples('GRIB2')
    try:
        keys = [('centre', 7), ('subCentre', 0), ('significanceOfReferenceTime', 1),
                ('dataDate', int(run.strftime('%Y%m%d'))), ('dataTime', 0),
                ('productionStatusOfProcessedData', 0), ('typeOfProcessedData', 1),
                ('Ni', 1440), ('Nj', 721), ('latitudeOfFirstGridPointInDegrees', 90.0),
                ('longitudeOfFirstGridPointInDegrees', 0.0), ('latitudeOfLastGridPointInDegrees', -90.0),
                ('longitudeOfLastGridPointInDegrees', 359.75), ('iDirectionIncrementInDegrees', 0.25),
                ('jDirectionIncrementInDegrees', 0.25), ('jScansPositively', 0), ('discipline', 0)]
        if field == 'dswrf':
            a, b = gfs.dswrf_bounds(lead)
            keys += [('productDefinitionTemplateNumber', 8), ('parameterCategory', 4), ('parameterNumber', 192),
                     ('typeOfFirstFixedSurface', 1), ('typeOfStatisticalProcessing', 0), ('stepUnits', 1),
                     ('stepType', 'avg'), ('stepRange', f'{a}-{b}')]
        else:
            keys += [('productDefinitionTemplateNumber', 0), ('parameterCategory', 2),
                     ('parameterNumber', 2 if field[0] == 'u' else 3), ('typeOfFirstFixedSurface', 103),
                     ('scaleFactorOfFirstFixedSurface', 0), ('scaledValueOfFirstFixedSurface', int(field[1:])),
                     ('stepUnits', 1), ('stepRange', str(lead))]
        keys += [('typeOfGeneratingProcess', 2), ('generatingProcessIdentifier', 96)]
        keys += list(override.items())
        for k, v in keys:
            eccodes.codes_set(g, k, v)
        eccodes.codes_set(g, 'packingType', 'grid_simple')
        eccodes.codes_set(g, 'decimalScaleFactor', 1)
        eccodes.codes_set(g, 'bitsPerValue', 16)
        values = (np.arange(1440 * 721) % 97) * 0.5
        eccodes.codes_set_values(g, values)
        return eccodes.codes_get_message(g), values.reshape(721, 1440)
    finally:
        eccodes.codes_release(g)


@pytest.mark.parametrize('field,lead', [('u10', 21), ('v100', 46 - 1), ('dswrf', 24), ('dswrf', 27)])
def test_decode_reads_code_keys_as_integers_and_validates(field, lead):
    run = dt.date(2019, 1, 1)
    msg, grid = synthetic(run, lead, field)
    gfs.check_frame(msg, len(msg))
    meta, box, q = gfs.decode(msg, run, lead, field)
    assert meta['typeOfFirstFixedSurface'] == (1 if field == 'dswrf' else 103)
    assert meta['typeOfFirstFixedSurface_native'] in ('sfc',) or field == 'dswrf'
    assert meta['typeOfProcessedData'] == 1 and meta['typeOfProcessedData_native'] == 'fc'
    assert q == 2.0 ** meta['binaryScaleFactor'] / 10.0 ** meta['decimalScaleFactor'] and 0 < q <= 0.5
    assert np.allclose(box, grid[gfs.ROW0:gfs.ROW1, gfs.COL0:gfs.COL1], atol=q)
    assert meta['box_nonfinite'] == 0 and box.shape == (34, 41)


@pytest.mark.parametrize('override', [dict(scaledValueOfFirstFixedSurface=80), dict(typeOfFirstFixedSurface=100),
                                      dict(centre=98), dict(productionStatusOfProcessedData=1),
                                      dict(dataDate=20190102), dict(generatingProcessIdentifier=81)])
def test_decoded_contradiction_stops(override):
    run = dt.date(2019, 1, 1)
    msg, _ = synthetic(run, 21, 'u10', **override)
    with pytest.raises(gfs.Contradiction):
        gfs.decode(msg, run, 21, 'u10')


def test_decoded_wrong_averaging_window_stops():
    run = dt.date(2019, 1, 1)
    msg, _ = synthetic(run, 24, 'dswrf', stepRange='21-24')
    with pytest.raises(gfs.Contradiction):
        gfs.decode(msg, run, 24, 'dswrf')
