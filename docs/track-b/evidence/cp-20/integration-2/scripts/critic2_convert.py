"""CP-20 Integration Critic 2 -- own section 15.2 conversion from the critic's own decoded boxes.

Written from the plan text only (no cp20.weather import). Reconstructs every canonical delivery hour whose
required messages were decoded by critic2_decode.py and compares with reports/weather-ablation/weather-features.parquet.
Also runs wrong-recipe sensitivity controls (magnitude of mean u/v, unweighted mean, no de-averaging, lead shift)
to show the comparison would detect those errors. No ledger charge beyond machine time (no decode here).
"""
from __future__ import annotations

from datetime import date, timedelta
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path.cwd()
OUT = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic-2/out')
WA = ROOT / 'reports/weather-ablation'
FIELDS = ('u10', 'v10', 'u100', 'v100', 'dswrf')
LEADS = (21, 24, 27, 30, 33, 36, 39, 42, 45, 48)
LAT = np.array([55.25 - 0.25 * j for j in range(34)])
W = np.repeat(np.cos(np.radians(LAT))[:, None], 41, axis=1)
W = W / W.sum()
meta = json.loads((OUT / 'decoded-meta.json').read_text())
wf = pd.read_parquet(WA / 'weather-features.parquet')
wf['ts'] = wf.timestamp_utc.dt.as_unit('ns').astype(str)
feat = wf.set_index('ts')


def cell(arr, field, lead):
    return arr[FIELDS.index(field), LEADS.index(lead)]


def have(arr, field, lead):
    return np.isfinite(cell(arr, field, lead)).all()


def speed(arr, u, v, h, magnitude_of_mean=False, weights=W):
    lo = 3 * (h // 3)
    hi = lo if h % 3 == 0 else lo + 3
    if not all(have(arr, f, L) for f in (u, v) for L in (lo, hi)):
        return None
    w = (h - lo) / 3
    uu = (1 - w) * cell(arr, u, lo) + w * cell(arr, u, hi)
    vv = (1 - w) * cell(arr, v, lo) + w * cell(arr, v, hi)
    if magnitude_of_mean:
        return float(np.hypot((weights * uu).sum(), (weights * vv).sum()))
    return float((weights * np.sqrt(uu ** 2 + vv ** 2)).sum())


def dswrf(arr, m, h, dealias=True, weights=W):
    end = 3 * (h // 3) + 3
    k = f'dswrf:{end}'
    if not have(arr, 'dswrf', end) or k not in m:
        return None, None
    if end % 6 == 3:
        if (m[k]['startStep'], m[k]['endStep']) != (end - 3, end):
            raise ValueError('bounds')
        blk, qs = cell(arr, 'dswrf', end).copy(), [m[k]['quantum']]
    else:
        k0 = f'dswrf:{end - 3}'
        if not have(arr, 'dswrf', end - 3) or k0 not in m:
            return None, None
        if (m[k]['startStep'], m[k]['endStep']) != (end - 6, end) or (m[k0]['startStep'], m[k0]['endStep']) != (end - 6, end - 3):
            raise ValueError('bounds')
        blk = 2 * cell(arr, 'dswrf', end) - cell(arr, 'dswrf', end - 3) if dealias else cell(arr, 'dswrf', end).copy()
        qs = [m[k]['quantum'], m[k0]['quantum']]
    q = max(qs)
    neg = blk < 0
    if (blk < -3 * q).any():
        return 'invalid', None
    clipped = int(neg.sum())
    blk[neg] = 0.0
    return float((weights * blk).sum()), clipped


res = {'runs': 0, 'hours_reconstructed': 0, 'hours_skipped_missing_decode': 0, 'max_abs': {'wind10': 0.0, 'wind100': 0.0, 'dswrf': 0.0},
       'clip_count_mismatch': 0, 'status_mismatch': 0, 'missing_feature_rows': 0, 'units_levels': {},
       'sensitivity_max_abs': {'magnitude_of_mean_u_v_wind100': 0.0, 'unweighted_mean_wind10': 0.0, 'no_deaveraging_dswrf': 0.0,
                               'lead_shift_plus3_wind100': 0.0}, 'dst_days': [], 'per_run': {}}
UNI = np.full((34, 41), 1 / (34 * 41))
for p in sorted((OUT / 'decoded').glob('*.npz')):
    run = p.stem
    arr = np.load(p)['data']
    m = meta[run]
    for k, v in m.items():
        res['units_levels'].setdefault(k.split(':')[0], set()).add((v['units'], v['typeOfLevel'], v['level']))
    delivery = date.fromisoformat(run) + timedelta(days=1)
    hrs = pd.date_range(pd.Timestamp(delivery, tz='Europe/Berlin'), pd.Timestamp(delivery + timedelta(days=1), tz='Europe/Berlin'),
                        freq='h', inclusive='left').tz_convert('UTC')
    if len(hrs) != 24:
        res['dst_days'].append((str(delivery), len(hrs)))
    run0 = pd.Timestamp(run, tz='UTC')
    n_ok = 0
    for t in hrs:
        h = int((t - run0) / pd.Timedelta(hours=1))
        s10 = speed(arr, 'u10', 'v10', h)
        s100 = speed(arr, 'u100', 'v100', h)
        rad, clipped = dswrf(arr, m, h)
        if s10 is None or s100 is None or rad is None:
            res['hours_skipped_missing_decode'] += 1
            continue
        key = str(t.as_unit('ns'))
        if key not in feat.index:
            res['missing_feature_rows'] += 1
            continue
        row = feat.loc[key]
        if row.status != 'ok' or row.run_00z != run or int(row.lead_hour) != h:
            res['status_mismatch'] += 1
            continue
        res['max_abs']['wind10'] = max(res['max_abs']['wind10'], abs(s10 - row.wx_wind10_mean))
        res['max_abs']['wind100'] = max(res['max_abs']['wind100'], abs(s100 - row.wx_wind100_mean))
        res['max_abs']['dswrf'] = max(res['max_abs']['dswrf'], abs(rad - row.wx_dswrf_mean))
        if clipped != row.dswrf_clipped_cells:
            res['clip_count_mismatch'] += 1
        sm = res['sensitivity_max_abs']
        sm['magnitude_of_mean_u_v_wind100'] = max(sm['magnitude_of_mean_u_v_wind100'], abs(speed(arr, 'u100', 'v100', h, True) - row.wx_wind100_mean))
        sm['unweighted_mean_wind10'] = max(sm['unweighted_mean_wind10'], abs(speed(arr, 'u10', 'v10', h, weights=UNI) - row.wx_wind10_mean))
        nd, _ = dswrf(arr, m, h, dealias=False)
        if isinstance(nd, float):
            sm['no_deaveraging_dswrf'] = max(sm['no_deaveraging_dswrf'], abs(nd - row.wx_dswrf_mean))
        if h + 3 <= 46:
            shifted = speed(arr, 'u100', 'v100', h + 3)
            if shifted is not None:
                sm['lead_shift_plus3_wind100'] = max(sm['lead_shift_plus3_wind100'], abs(shifted - row.wx_wind100_mean))
        n_ok += 1
    res['per_run'][run] = {'delivery': str(delivery), 'hours': len(hrs), 'reconstructed': n_ok}
    res['hours_reconstructed'] += n_ok
    res['runs'] += 1
res['units_levels'] = {k: sorted(map(list, v)) for k, v in res['units_levels'].items()}
res['within_1e-9'] = all(v <= 1e-9 for v in res['max_abs'].values())
(OUT / 'convert.json').write_text(json.dumps(res, indent=1, default=str))
print(json.dumps({k: v for k, v in res.items() if k != 'per_run'}, indent=1, default=str))
