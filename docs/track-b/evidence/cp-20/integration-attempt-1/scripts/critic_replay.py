"""CP-20 Integration Critic -- independent causal H-layer replay for both arms, all folds.

Own implementation of plan section 14.2 (not cp16.residuals): standardized residuals
r=(y-c)/s with the issuance's A1 scale; the latest 28 complete released delivery days <= D-2;
consume once; incomplete issued days never enter; pooled and per-local-hour linear quantiles;
w_h=n_h/(n_h+56), w_h=0 below 14 distinct days; V2-H = c + s*(w Q_h + (1-w) Q_P). One
continuous replay per fold/arm from the frozen warm-up start through the evaluation end (no
serialisation), so a match also shows the committed admission->evaluation restart was lossless.
Central components: HG from the local content-hashed cache (digest re-verified here); H0 from the
identity-verified CP-15/CP-16 caches. Charges one policy-day per (date, arm) before replaying it.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp20.budget import Budget
from cp20.inputs import H0Components, load

ART = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20')
OUT = ART / 'critic/out'
WA = ROOT / 'reports/weather-ablation'
LEV = np.array([.025, .10, .25, .50, .75, .90, .975])
Q = ['p025', 'p10', 'p25', 'p50', 'p75', 'p90', 'p975']
b = Budget(os.environ['CP20_LEDGER'])


def canon(d):
    s = pd.Timestamp(d.isoformat(), tz='Europe/Berlin')
    e = pd.Timestamp((d + timedelta(days=1)).isoformat(), tz='Europe/Berlin')
    return pd.date_range(s, e, freq='h', inclusive='left').tz_convert('UTC')


def digest(item):
    return hashlib.sha256(json.dumps({k: v for k, v in item.items() if k != 'content_sha256'}, sort_keys=True,
                                     allow_nan=False, default=str).encode()).hexdigest()


def ahash(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


lin = json.loads((WA / 'lineage.json').read_text())
ident = lin['hg_identity']
im = json.loads((ROOT / 'reports/v2-causal/input-manifest.json').read_text())
data, _ = load(ROOT)
truth = pd.Series(data.y, index=data.index)
pred = pd.read_parquet(WA / 'predictions.parquet', filters=[('policy', 'in', ['H0', 'HG'])])
pred = pred.set_index(['policy', 'fold', 'timestamp_utc']).sort_index()
adm_lin = {(a['arm'], a['fold'], a['day']): a for a in lin['admission']}
eval_meta = {(o['arm'], o['fold'], o['day']): o for o in lin['origins'] if o['phase'] == 'evaluation' and o['predicted']}
res = {'folds': {}, 'policy_days_reserved': 0}
all_diff, all_bitwise, n_rows = 0.0, True, 0
support_mismatch, adm_hash_mismatch, meta_mismatch, final_buffer_mismatch = [], [], [], []
fallback = {}
for f in im['folds']:
    fold = f['fold']
    first = date.fromisoformat(f['evaluation_start'])
    last = date.fromisoformat(f['evaluation_end'])
    adm_days = {date.fromisoformat(x['day']) for x in f['admission']}
    dates = list(pd.date_range(f['warmup_start'], last).date)
    h0src = H0Components(ROOT, fold, data)
    for arm in ('H0', 'HG'):
        buffer, pending, consumed = [], {}, set()
        mine_rows = []
        for D in dates:
            b.reserve(policy_days=1)
            res['policy_days_reserved'] += 1
            cutoff = D - timedelta(days=2)
            for d in sorted(pending):
                if d > cutoff:
                    break
                ts, c, s = pending[d]
                if not ts.equals(canon(d)):
                    consumed.add(d)
                    continue
                yv = truth.reindex(ts).to_numpy(float)
                if not np.isfinite(yv).all():
                    continue
                r = (yv - c) / s
                buffer = sorted([*buffer, (d, r, ts.tz_convert('Europe/Berlin').hour.to_numpy())], key=lambda x: x[0])[-28:]
                consumed.add(d)
            for d in consumed:
                pending.pop(d, None)
            rows = data.rows(D)
            if not len(rows):
                continue
            ts = data.index[rows]
            if arm == 'HG':
                it = json.loads((ART / 'hg-components' / fold / f'{D}.json').read_text())
                if it['content_sha256'] != digest(it) or any(it[k] != v for k, v in ident.items()) or it['timestamp_utc'] != list(map(str, ts)):
                    raise ValueError(f'HG cache identity {fold} {D}')
                a1, b2 = np.asarray(it['central']['A1'], float), np.asarray(it['central']['B2'], float)
            else:
                _, cen, _ = h0src.get(D)
                a1, b2 = cen['A1'], cen['B2']
            c = a1 / 2 + b2 / 2
            s = data.scale[rows].astype(float)
            predict = (D >= first) or (D in adm_days)
            if predict:
                if len(buffer) != 28:
                    raise ValueError(f'buffer {len(buffer)} at {fold} {D}')
                err = np.concatenate([x[1] for x in buffer])
                hrs = np.concatenate([x[2] for x in buffer])
                dys = np.concatenate([[x[0]] * len(x[1]) for x in buffer])
                qp = np.quantile(err, LEV, method='linear')
                table, sup = {}, {}
                for h in range(24):
                    msk = hrs == h
                    n = int(msk.sum())
                    dist = len(set(dys[msk]))
                    w = n / (n + 56) if dist >= 14 else 0.0
                    table[h] = (w * np.quantile(err[msk], LEV, method='linear') + (1 - w) * qp) if w else qp.copy()
                    sup[str(h)] = {'n': n, 'distinct_days': dist, 'weight': w}
                    fallback.setdefault((arm, fold, 'evaluation' if D >= first else 'training_only'), [0, 0])
                    fallback[(arm, fold, 'evaluation' if D >= first else 'training_only')][0] += 1
                    if w == 0:
                        fallback[(arm, fold, 'evaluation' if D >= first else 'training_only')][1] += 1
                lh = ts.tz_convert('Europe/Berlin').hour
                hmat = np.asarray([table[h] for h in lh])
                out = c[:, None] + s[:, None] * hmat
                meta = {'buffer_start': str(buffer[0][0]), 'buffer_end': str(buffer[-1][0]), 'buffer_days': len(buffer)}
                if D < first:
                    ref = adm_lin[(arm, fold, str(D))]
                    if ahash(out) != ref['vector_sha256']:
                        adm_hash_mismatch.append((arm, fold, str(D)))
                    if ref['hour_support'] != sup:
                        support_mismatch.append((arm, fold, str(D)))
                    if any(ref[k] != v for k, v in meta.items()):
                        meta_mismatch.append((arm, fold, str(D)))
                else:
                    ref = eval_meta[(arm, fold, str(D))]
                    if ref['hour_support'] != sup:
                        support_mismatch.append((arm, fold, str(D)))
                    if any(ref[k] != v for k, v in meta.items()) or ref['vector_sha256'] != ahash(out):
                        meta_mismatch.append((arm, fold, str(D)))
                    theirs = pred.loc[(arm, fold)].loc[ts]
                    tq = theirs[Q].to_numpy(float)
                    diff = float(np.max(np.abs(tq - out)))
                    all_diff = max(all_diff, diff)
                    all_bitwise &= bool(np.array_equal(tq, out))
                    all_bitwise &= bool(np.array_equal(theirs.central.to_numpy(float), c))
                    n_rows += len(ts)
            pending[D] = (ts, c, s)
        # final buffer vs committed final state
        st = lin['states'][fold][arm]
        fb = [(x['day'], np.asarray(x['errors'])) for x in st['buffer']]
        if [str(x[0]) for x in buffer] != [x[0] for x in fb] or not all(np.array_equal(x[1], y[1]) for x, y in zip(buffer, fb)):
            final_buffer_mismatch.append((arm, fold))
    print(fold, 'replayed', flush=True)
fb_csv = pd.read_csv(WA / 'fallback.csv')
fb_ok = all(fallback[(r.arm, r.fold, r.phase)] == [r.hour_cells if False else fallback[(r.arm, r.fold, r.phase)][0], r.fallback_cells] for r in fb_csv.itertuples())
res.update({'evaluation_rows_compared': n_rows, 'max_abs_diff_quantiles': all_diff, 'bitwise_equal_quantiles_and_central': all_bitwise,
            'admission_vector_sha_mismatches': adm_hash_mismatch, 'hour_support_mismatches': support_mismatch[:10],
            'n_hour_support_mismatches': len(support_mismatch), 'buffer_meta_mismatches': meta_mismatch[:10],
            'final_buffer_state_mismatches': final_buffer_mismatch,
            'fallback_cells_mine': {'|'.join(k): v for k, v in fallback.items()}, 'fallback_csv_zero_and_mine_zero': bool(fb_csv.fallback_cells.eq(0).all() and all(v[1] == 0 for v in fallback.values()))})
json.dump(res, open(OUT / 'replay.json', 'w'), indent=1, default=str)
print(json.dumps({k: v for k, v in res.items() if k != 'fallback_cells_mine'}, default=str), flush=True)
