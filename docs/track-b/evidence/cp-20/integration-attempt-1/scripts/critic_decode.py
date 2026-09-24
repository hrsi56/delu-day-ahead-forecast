"""CP-20 Integration Critic -- own ecCodes decode of every retained raw target message (WX env).

Each retained message is decoded exactly once after b.reserve(message_attempts=1). The regional
box is located from the decoded grid geometry (not from fixed indices), compared bit-for-bit with
the extraction's stored box, and written with its metadata for the independent conversion step.
No network. Admission copies are byte-identical (sha256, verified separately) and are not
decoded a second time.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import eccodes
import numpy as np

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp20.budget import Budget  # stdlib-only ledger

ART = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20')
OUT = ART / 'critic/out/decoded'
OUT.mkdir(parents=True, exist_ok=True)
b = Budget(os.environ['CP20_LEDGER'])
FIELDS = ('u10', 'v10', 'u100', 'v100', 'dswrf')
LEADS = (21, 24, 27, 30, 33, 36, 39, 42, 45, 48)
INTK = ('discipline', 'parameterCategory', 'parameterNumber', 'typeOfFirstFixedSurface', 'productionStatusOfProcessedData',
        'typeOfProcessedData', 'generatingProcessIdentifier', 'productDefinitionTemplateNumber', 'stepUnits',
        'jScansPositively', 'iScansNegatively', 'bitmapPresent', 'numberOfMissing', 'binaryScaleFactor', 'decimalScaleFactor',
        'bitsPerValue', 'Ni', 'Nj', 'dataDate', 'dataTime', 'startStep', 'endStep', 'level', 'validityDate', 'validityTime',
        'editionNumber')
STRK = ('shortName', 'units', 'typeOfLevel', 'stepType', 'gridType', 'packingType', 'centre')
FLTK = ('latitudeOfFirstGridPointInDegrees', 'longitudeOfFirstGridPointInDegrees', 'latitudeOfLastGridPointInDegrees',
        'longitudeOfLastGridPointInDegrees', 'iDirectionIncrementInDegrees', 'jDirectionIncrementInDegrees', 'referenceValue')
summary = {'decoded': 0, 'box_bitwise_equal_stored': 0, 'box_mismatch': [], 'runs': []}
for rd in sorted((ART / 'weather/raw').iterdir()):
    run = rd.name
    rec = json.loads((ART / 'weather/runs' / f'{run}.json').read_text())
    shas = {(m['lead'], m['field']): m['sha256'] for m in rec['messages']}
    with np.load(ART / 'weather/runs' / f'{run}.npz') as z:
        stored = z['data'].copy()
        sf, sl = tuple(z['fields']), tuple(int(x) for x in z['leads'])
    boxes = np.full((5, 10, 34, 41), np.nan)
    metas = {}
    for fi, field in enumerate(FIELDS):
        for li, lead in enumerate(LEADS):
            path = next(rd.glob(f'f{lead:03d}_{field}_*.grib2'))
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != shas[(lead, field)]:
                raise ValueError(f'retained raw sha mismatch {run} {lead} {field}')
            b.reserve(message_attempts=1)
            gid = eccodes.codes_new_from_message(raw)
            try:
                meta = {}
                for k in INTK:
                    meta[k] = eccodes.codes_get(gid, k, ktype=int)
                for k in STRK:
                    meta[k] = eccodes.codes_get(gid, k)
                for k in FLTK:
                    meta[k] = eccodes.codes_get(gid, k, ktype=float)
                vals = eccodes.codes_get_values(gid).astype(np.float64)
            finally:
                eccodes.codes_release(gid)
            summary['decoded'] += 1
            nj, ni = meta['Nj'], meta['Ni']
            lat = meta['latitudeOfFirstGridPointInDegrees'] - meta['jDirectionIncrementInDegrees'] * np.arange(nj)
            lon = meta['longitudeOfFirstGridPointInDegrees'] + meta['iDirectionIncrementInDegrees'] * np.arange(ni)
            if meta['jScansPositively'] != 0 or meta['iScansNegatively'] != 0 or meta['bitmapPresent'] != 0:
                raise ValueError('unexpected scan/bitmap')
            grid = vals.reshape(nj, ni)
            rows = np.flatnonzero((lat >= 47.0 - 1e-9) & (lat <= 55.25 + 1e-9))
            cols = np.flatnonzero((lon >= 5.5 - 1e-9) & (lon <= 15.5 + 1e-9))
            box = grid[np.ix_(rows, cols)]
            meta['box_lat'] = [float(lat[rows[0]]), float(lat[rows[-1]]), len(rows)]
            meta['box_lon'] = [float(lon[cols[0]]), float(lon[cols[-1]]), len(cols)]
            meta['quantum'] = 2.0 ** meta['binaryScaleFactor'] / 10.0 ** meta['decimalScaleFactor']
            meta['sha256'] = shas[(lead, field)]
            boxes[fi, li] = box
            metas[f'{field}_f{lead:03d}'] = meta
            if np.array_equal(box, stored[sf.index(field), sl.index(lead)]):
                summary['box_bitwise_equal_stored'] += 1
            else:
                summary['box_mismatch'].append((run, field, lead, float(np.nanmax(np.abs(box - stored[sf.index(field), sl.index(lead)])))))
    np.savez(OUT / f'{run}.npz', data=boxes, lats=90.0 - 0.25 * np.arange(139, 173), lons=0.25 * np.arange(22, 63))
    (OUT / f'{run}.json').write_text(json.dumps(metas, indent=0, default=str))
    summary['runs'].append(run)
    print(run, 'decoded 50', flush=True)
(ART / 'critic/out/decode-summary.json').write_text(json.dumps(summary, indent=1, default=str))
print(json.dumps({k: (v if k != 'runs' else len(v)) for k, v in summary.items()}), flush=True)
