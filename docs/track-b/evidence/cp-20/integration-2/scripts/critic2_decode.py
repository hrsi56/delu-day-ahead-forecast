"""CP-20 Integration Critic 2 -- own ecCodes decode of the eligible retained raw target messages (WX env).

Each listed message is sha256-checked against its recorded extraction identity, charged one message attempt
BEFORE decoding, decoded once, its metadata validated independently and its regional box selected from the
decoded geometry (coordinates, not stored indices). The box is compared bitwise with the stored run box.
Decoded boxes stay local (rights notice) under out/decoded/.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

import eccodes
import numpy as np

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp20.budget import Budget  # noqa: E402

ART = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20')
OUT = ART / 'critic-2/out'
LIST = ART / 'critic-2/eligible-decodes.txt'
FIELDS = ('u10', 'v10', 'u100', 'v100', 'dswrf')
LEADS = (21, 24, 27, 30, 33, 36, 39, 42, 45, 48)
KEYS = ('gridType', 'Ni', 'Nj', 'latitudeOfFirstGridPointInDegrees', 'longitudeOfFirstGridPointInDegrees',
        'latitudeOfLastGridPointInDegrees', 'longitudeOfLastGridPointInDegrees', 'iDirectionIncrementInDegrees',
        'jDirectionIncrementInDegrees', 'jScansPositively', 'iScansNegatively', 'dataDate', 'dataTime', 'startStep',
        'endStep', 'stepType', 'typeOfLevel', 'level', 'shortName', 'units', 'discipline', 'parameterCategory',
        'parameterNumber', 'productionStatusOfProcessedData', 'typeOfProcessedData', 'generatingProcessIdentifier',
        'centre', 'binaryScaleFactor', 'decimalScaleFactor', 'bitsPerValue', 'packingType', 'numberOfMissing', 'jPointsAreConsecutive')

raw_list = LIST.read_bytes()
assert hashlib.sha256(raw_list).hexdigest() == 'd35faaa4b4114edce9207823b2bf6f373f75e8bd64d6908bb6e3ca49a86e88f8'
paths = [Path(l) for l in raw_list.decode().splitlines() if l.strip()]
assert len(paths) == len(set(paths)) == 1035
b = Budget(os.environ['CP20_LEDGER'])
(OUT / 'decoded').mkdir(parents=True, exist_ok=True)
records, boxes, meta_out = {}, {}, {}
JOURNAL = OUT / 'decode-journal.jsonl'
journal = [json.loads(l) for l in JOURNAL.read_text().splitlines()] if JOURNAL.exists() else []
already = {j['path'] for j in journal}   # reserved or decoded earlier: never decoded a second time


def jot(**kw):
    with JOURNAL.open('a') as fh:
        fh.write(json.dumps(kw, default=str) + '\n')

summary = {'listed': len(paths), 'decoded': 0, 'sha256_mismatch': [], 'box_not_bitwise': [], 'meta_mismatch': [],
           'own_metadata_problems': [], 'quantum_mismatch': [], 'geometry': None, 'versions': {}}
for path in paths:
    if str(path) in already:
        continue
    run = path.parent.name
    lead = int(path.name[1:4])
    field, ep = path.name[5:-6].rsplit('_', 1)
    if run not in records:
        records[run] = json.loads((ART / 'weather/runs' / f'{run}.json').read_text())
        with np.load(ART / 'weather/runs' / f'{run}.npz') as z:
            boxes[run] = z['data'].copy()
            assert tuple(z['fields']) == FIELDS and tuple(z['leads']) == LEADS
    rec = records[run]
    msg = next(m for m in rec['messages'] if m['lead'] == lead and m['field'] == field)
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != msg['sha256'] or ep != msg['endpoint']:
        summary['sha256_mismatch'].append(str(path))
        continue
    b.reserve(message_attempts=1)            # charged before the decode
    jot(path=str(path), stage='reserved')
    h = eccodes.codes_new_from_message(raw)
    try:
        meta = {}
        for k in KEYS:
            try:
                meta[k] = eccodes.codes_get(h, k)
            except eccodes.KeyValueNotFoundError:
                meta[k] = None
        vals = eccodes.codes_get_values(h).astype(float)
        if eccodes.codes_get(h, 'bitmapPresent'):
            vals[vals == eccodes.codes_get_double(h, 'missingValue')] = np.nan
    finally:
        eccodes.codes_release(h)
    nj, ni = meta['Nj'], meta['Ni']
    grid = vals.reshape(nj, ni)
    lat0, lon0 = meta['latitudeOfFirstGridPointInDegrees'], meta['longitudeOfFirstGridPointInDegrees']
    dj, di = meta['jDirectionIncrementInDegrees'], meta['iDirectionIncrementInDegrees']
    lats = lat0 + (dj if meta['jScansPositively'] else -dj) * np.arange(nj)
    lons = lon0 + (-di if meta['iScansNegatively'] else di) * np.arange(ni)
    jj = np.flatnonzero((lats >= 47.0 - 1e-9) & (lats <= 55.25 + 1e-9))
    ii = np.flatnonzero((lons >= 5.5 - 1e-9) & (lons <= 15.5 + 1e-9))
    box = grid[np.ix_(jj, ii)]
    geom = (float(lats[jj[0]]), float(lats[jj[-1]]), len(jj), float(lons[ii[0]]), float(lons[ii[-1]]), len(ii))
    summary['geometry'] = summary['geometry'] or geom
    if geom != summary['geometry'] or geom != (55.25, 47.0, 34, 5.5, 15.5, 41):
        summary['own_metadata_problems'].append((str(path), 'geometry', geom))
    stored = boxes[run][FIELDS.index(field), LEADS.index(lead)]
    bitwise = bool(box.shape == stored.shape and np.array_equal(box, stored))
    if not bitwise:
        summary['box_not_bitwise'].append(str(path))
    # independent metadata expectations
    exp = {'dataDate': int(run.replace('-', '')), 'dataTime': 0, 'endStep': lead,
           'startStep': lead if field != 'dswrf' else (lead - 3 if lead % 6 == 3 else lead - 6),
           'stepType': 'instant' if field != 'dswrf' else 'avg',
           'typeOfLevel': 'heightAboveGround' if field != 'dswrf' else 'surface',
           'level': {'u10': 10, 'v10': 10, 'u100': 100, 'v100': 100, 'dswrf': 0}[field],
           'units': 'm s**-1' if field != 'dswrf' else 'W m**-2',
           'parameterNumber': {'u10': 2, 'v10': 3, 'u100': 2, 'v100': 3, 'dswrf': 192}[field],
           'parameterCategory': 2 if field != 'dswrf' else 4, 'discipline': 0,
           'productionStatusOfProcessedData': 0, 'typeOfProcessedData': 'fc', 'centre': 'kwbc',
           'gridType': 'regular_ll', 'Ni': 1440, 'Nj': 721, 'numberOfMissing': 0, 'jPointsAreConsecutive': 0,
           'jScansPositively': 0, 'iScansNegatively': 0, 'iDirectionIncrementInDegrees': 0.25, 'jDirectionIncrementInDegrees': 0.25}
    for k, v in exp.items():
        got = meta[k]
        if k == 'typeOfProcessedData' and got in (1, 'fc'):
            continue
        if got != v:
            summary['own_metadata_problems'].append((str(path), k, got, v))
    for k in ('dataDate', 'dataTime', 'startStep', 'endStep', 'stepType', 'typeOfLevel', 'level', 'shortName', 'units',
              'parameterNumber', 'binaryScaleFactor', 'decimalScaleFactor', 'bitsPerValue', 'packingType', 'Ni', 'Nj'):
        if msg['meta'].get(k) != meta[k]:
            summary['meta_mismatch'].append((str(path), k, msg['meta'].get(k), meta[k]))
    q = 2.0 ** meta['binaryScaleFactor'] / 10.0 ** meta['decimalScaleFactor']
    if not np.isclose(q, msg['packing_quantum'], rtol=1e-12, atol=0):
        summary['quantum_mismatch'].append((str(path), q, msg['packing_quantum']))
    summary['versions'][rec['version']] = summary['versions'].get(rec['version'], 0) + 1
    meta_out.setdefault(run, {})[f'{field}:{lead}'] = {'startStep': meta['startStep'], 'endStep': meta['endStep'], 'quantum': q,
                                                       'units': meta['units'], 'typeOfLevel': meta['typeOfLevel'], 'level': meta['level']}
    d = OUT / 'decoded' / f'{run}.npz'
    arr = np.load(d)['data'] if d.exists() else np.full((5, 10, 34, 41), np.nan)
    arr[FIELDS.index(field), LEADS.index(lead)] = box
    np.savez(d, data=arr)
    jot(path=str(path), stage='decoded', run=run, field=field, lead=lead, bitwise=bitwise, version=rec['version'],
        problems=[x for x in summary['own_metadata_problems'] if x[0] == str(path)],
        meta_mismatch=[x for x in summary['meta_mismatch'] if x[0] == str(path)],
        quantum_mismatch=[x for x in summary['quantum_mismatch'] if x[0] == str(path)],
        meta=meta_out[run][f'{field}:{lead}'])
journal = [json.loads(l) for l in JOURNAL.read_text().splitlines()]
done = [j for j in journal if j['stage'] == 'decoded']
reserved = {j['path'] for j in journal if j['stage'] == 'reserved'}
meta_all = {}
for j in done:
    meta_all.setdefault(j['run'], {})[f"{j['field']}:{j['lead']}"] = j['meta']
(OUT / 'decoded-meta.json').write_text(json.dumps(meta_all, indent=1))
summary['decoded'] = len(done)
summary['reserved'] = len(reserved)
summary['reserved_not_decoded'] = sorted(reserved - {j['path'] for j in done})
summary['box_bitwise_equal'] = sum(j['bitwise'] for j in done)
summary['problems_total'] = sum(len(j['problems']) + len(j['meta_mismatch']) + len(j['quantum_mismatch']) for j in done)
summary['versions'] = {v: sum(1 for j in done if j['version'] == v) for v in sorted({j['version'] for j in done})}
summary['runs'] = len(meta_all)
summary['decoded_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((OUT / 'decoded').glob('*.npz'))}
(OUT / 'decode-summary.json').write_text(json.dumps(summary, indent=1, default=str))
print(json.dumps({k: (v if not isinstance(v, list) else (len(v), v[:5])) for k, v in summary.items() if k != 'decoded_sha256'}, default=str))
