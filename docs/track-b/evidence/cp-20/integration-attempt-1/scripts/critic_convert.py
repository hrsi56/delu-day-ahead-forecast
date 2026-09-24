"""CP-20 Integration Critic -- own section 15.2 conversion from the Critic's own decode of the 23
retained runs, compared with the committed weather-features.parquet (tolerance 1e-9), plus
negative recipe controls that the comparison must detect (wrong de-averaging, magnitude of mean
wind, unweighted mean, no clipping) and metadata/units/bounds checks from the own decode."""
import json
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path.cwd()
ART = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20')
DEC = ART / 'critic/out/decoded'
WA = ROOT / 'reports/weather-ablation'
F = ('u10', 'v10', 'u100', 'v100', 'dswrf')
L = (21, 24, 27, 30, 33, 36, 39, 42, 45, 48)
wf = pd.read_parquet(WA / 'weather-features.parquet')
wf['ts'] = wf.timestamp_utc.dt.tz_convert('UTC')
res = {'runs': [], 'max_abs': {'wind10': 0.0, 'wind100': 0.0, 'dswrf': 0.0}, 'clip_log_mismatch': [], 'meta_problems': [],
       'negative_controls_max_abs_min_over_runs': {}}
neg = {'dswrf_no_deaveraging': [], 'wind_magnitude_of_mean': [], 'unweighted_mean_wind100': [], 'dswrf_no_clipping_where_negative': []}
for npz in sorted(DEC.glob('*.npz')):
    run = date.fromisoformat(npz.stem)
    deliv = run + timedelta(days=1)
    meta = json.loads(npz.with_suffix('.json').read_text())
    with np.load(npz) as z:
        data, lats = z['data'], z['lats']
    for k, m in meta.items():
        field, lead = k.split('_f')
        lead = int(lead)
        exp_date = int(run.strftime('%Y%m%d'))
        valid = pd.Timestamp(run) + pd.Timedelta(hours=lead)
        p = []
        if m['dataDate'] != exp_date or m['dataTime'] != 0: p.append('init')
        if m['validityDate'] != int(valid.strftime('%Y%m%d')) or m['validityTime'] != valid.hour * 100: p.append('valid')
        if m['box_lat'] != [55.25, 47.0, 34] or m['box_lon'] != [5.5, 15.5, 41]: p.append('box')
        if m['gridType'] != 'regular_ll' or m['Ni'] != 1440 or m['Nj'] != 721: p.append('grid')
        if field == 'dswrf':
            lo = lead - 3 if lead % 6 == 3 else lead - 6
            if (m['startStep'], m['endStep'], m['stepType'], m['units'], m['typeOfFirstFixedSurface'], m['parameterCategory']) != (lo, lead, 'avg', 'W m**-2', 1, 4) or m['parameterNumber'] not in (192, 7):
                p.append('dswrf_meta')
        else:
            if (m['startStep'], m['endStep'], m['stepType'], m['units'], m['typeOfFirstFixedSurface'], m['level'], m['parameterCategory'], m['parameterNumber']) != \
                    (lead, lead, 'instant', 'm s**-1', 103, int(field[1:]), 2, 2 if field[0] == 'u' else 3):
                p.append('wind_meta')
        if m['productionStatusOfProcessedData'] != 0 or m['typeOfProcessedData'] != 1 or m['centre'] != 'kwbc' or m['generatingProcessIdentifier'] != 96:
            p.append('product')
        if p:
            res['meta_problems'].append((str(run), k, p))
    w = np.cos(np.deg2rad(lats))[:, None] * np.ones((1, 41))
    w = w / w.sum()
    rows = wf[wf.delivery_date == deliv].sort_values('ts')
    s = pd.Timestamp(deliv.isoformat(), tz='Europe/Berlin')
    e = pd.Timestamp((deliv + timedelta(days=1)).isoformat(), tz='Europe/Berlin')
    hours = pd.date_range(s, e, freq='h', inclusive='left').tz_convert('UTC')
    assert len(rows) == len(hours) and (rows.ts.to_numpy() == hours.to_numpy()).all()
    run0 = pd.Timestamp(run.isoformat(), tz='UTC')
    for (_, r), t in zip(rows.iterrows(), hours):
        h = int((t - run0) / pd.Timedelta(hours=1))
        lo3 = 3 * (h // 3)
        hi3 = lo3 if h % 3 == 0 else lo3 + 3
        a = (h - lo3) / 3.0 if hi3 != lo3 else 0.0
        mine = {}
        for lvl, (fu, fv) in (('wind10', ('u10', 'v10')), ('wind100', ('u100', 'v100'))):
            U = (1 - a) * data[F.index(fu), L.index(lo3)] + a * data[F.index(fu), L.index(hi3)]
            V = (1 - a) * data[F.index(fv), L.index(lo3)] + a * data[F.index(fv), L.index(hi3)]
            mine[lvl] = float((w * np.hypot(U, V)).sum())
            if lvl == 'wind100':
                neg['unweighted_mean_wind100'].append(abs(float(np.hypot(U, V).mean()) - r.wx_wind100_mean))
            neg['wind_magnitude_of_mean'].append(abs(float(np.hypot((w * U).sum(), (w * V).sum())) - r[f'wx_{lvl}_mean']))
        E = lo3 + 3 if h % 3 else h + 3
        E = 3 * (h // 3) + 3
        A = data[F.index('dswrf')]
        if E % 6 == 3:
            blk = A[L.index(E)].copy()
            qs = [meta[f'dswrf_f{E:03d}']['quantum']]
            naive = blk
        else:
            blk = 2 * A[L.index(E)] - A[L.index(E - 3)]
            qs = [meta[f'dswrf_f{E:03d}']['quantum'], meta[f'dswrf_f{E - 3:03d}']['quantum']]
            naive = A[L.index(E)]
        q = max(qs)
        negm = blk < 0
        below = blk < -3 * q
        if below.any():
            res['meta_problems'].append((str(run), f'h{h}', 'below_minus_3q'))
        clipped = np.where(negm, 0.0, blk)
        mine['dswrf'] = float((w * clipped).sum())
        if E % 6 == 0:
            neg['dswrf_no_deaveraging'].append(abs(float((w * np.where(naive < 0, 0, naive)).sum()) - r.wx_dswrf_mean))
        if negm.any():
            neg['dswrf_no_clipping_where_negative'].append(abs(float((w * blk).sum()) - r.wx_dswrf_mean))
        for lvl, col in (('wind10', 'wx_wind10_mean'), ('wind100', 'wx_wind100_mean'), ('dswrf', 'wx_dswrf_mean')):
            res['max_abs'][lvl] = max(res['max_abs'][lvl], abs(mine[lvl] - r[col]))
        log = (int(negm.sum()), float(blk.min()), float(q), float(-blk[negm].sum()))
        theirs = (int(r.dswrf_clipped_cells), float(r.dswrf_min_block), float(r.dswrf_quantum), float(r.dswrf_clipped_magnitude_sum))
        if log[0] != theirs[0] or abs(log[1] - theirs[1]) > 1e-9 or log[2] != theirs[2] or abs(log[3] - theirs[3]) > 1e-6:
            res['clip_log_mismatch'].append((str(deliv), h, log, theirs))
        if r.status != 'ok' or r.run_00z != str(run) or r.lead_hour != h:
            res['meta_problems'].append((str(deliv), h, 'row_identity'))
    res['runs'].append({'run': str(run), 'delivery': str(deliv), 'hours': len(hours), 'version': rows.version.iloc[0]})
res['hours_compared'] = int(sum(r['hours'] for r in res['runs']))
res['negative_controls_max_abs_min_over_runs'] = {k: {'n': len(v), 'max': float(max(v)) if v else None, 'median': float(np.median(v)) if v else None} for k, v in neg.items()}
res['all_within_1e-9'] = max(res['max_abs'].values()) <= 1e-9
(ART / 'critic/out/convert.json').write_text(json.dumps(res, indent=1, default=str))
print(json.dumps({k: v for k, v in res.items() if k != 'runs'}, default=str)[:4000])
print([ (r['run'], r['hours'], r['version']) for r in res['runs']])
