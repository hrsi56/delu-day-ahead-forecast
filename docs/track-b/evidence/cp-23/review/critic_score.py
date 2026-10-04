"""Independent CP-23 recomputation by the Integration Critic.

Written from capstone_v21.md v21-r10 §14.3, §14.4, §17.5, §8, §21.2, §21.5 and §21.6 text only. It
imports no project scoring code. The single project import is the ledger, used to charge one
reference pass and one bootstrap pass (review allowance), as cp23.review does.

Usage (run from the critic worktree, under the CP-23 monitor):
    python critic_score.py <out.json>
"""
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path.cwd()
OUT = Path(sys.argv[1])
Q = ['p025', 'p10', 'p25', 'p50', 'p75', 'p90', 'p975']
ALPHAS = [(0.05, 'p025', 'p975'), (0.2, 'p10', 'p90'), (0.5, 'p25', 'p75')]
FOLDS = ['fold_1', 'fold_2', 'fold_3', 'fold_4', 'fold_5']
SEED, REPS = 15042, 2000
SAVED_CP20 = ['B0', 'B1', 'B2', 'B3', 'A1', 'HG']
NEW = ['v5', 'v3+D', 'D']
CONTRASTS = [('v5', 'HGL'), ('v5', 'HG'), ('D', 'HGL'), ('D', 'HG'), ('v3+D', 'HG'), ('HGL', 'HG'), ('v5', 'v3+D')]

if '--no-charge' not in sys.argv:
    sys.path.insert(0, str(ROOT / 'src'))
    from cp23.budget import ledger  # noqa: E402
    print('charged', ledger().reserve(reference_passes=1, analysis_passes=1), flush=True)

# ---- load -------------------------------------------------------------------------------------
cols = ['fold', 'policy', 'timestamp_utc', 'delivery_date', 'y_true', 'central', *Q]
a = pd.read_parquet(ROOT / 'reports/weather-ablation/predictions.parquet')
a = a.loc[a.policy.isin(SAVED_CP20), cols]
b = pd.read_parquet(ROOT / 'reports/block-challenger/predictions.parquet')
b = b.loc[b.policy.eq('HGL'), cols]
c = pd.read_parquet(ROOT / 'reports/distribution-challenger/predictions.parquet')[cols]
P = pd.concat([a, b, c], ignore_index=True)
P['timestamp_utc'] = pd.to_datetime(P.timestamp_utc, utc=True).dt.as_unit('ns')
P['delivery_date'] = pd.to_datetime(P.delivery_date).dt.normalize()
POL = SAVED_CP20 + ['HGL'] + NEW

exp = pd.read_parquet(ROOT / 'reports/cp15/predictions.parquet', columns=['fold', 'policy', 'timestamp_utc'])
exp = exp.loc[exp.policy.eq('B0'), ['fold', 'timestamp_utc']]
exp['timestamp_utc'] = pd.to_datetime(exp.timestamp_utc, utc=True).dt.as_unit('ns')
expkeys = set(map(tuple, exp[['fold', 'timestamp_utc']].astype(str).to_numpy()))
res = {'expected_keys': len(expkeys), 'policies': {}}

# ---- keys, finiteness, order, y_true agreement --------------------------------------------------
ref_y = None
for p in POL:
    d = P.loc[P.policy.eq(p)]
    keys = set(map(tuple, d[['fold', 'timestamp_utc']].astype(str).to_numpy()))
    q = d[Q].to_numpy(float)
    ys = d.sort_values(['fold', 'timestamp_utc']).y_true.to_numpy(float)
    if ref_y is None:
        ref_y = ys
    res['policies'][p] = {
        'rows': int(len(d)), 'duplicate_keys': int(d.duplicated(['fold', 'timestamp_utc']).sum()),
        'keys_equal_expected': keys == expkeys, 'finite_quantiles': bool(np.isfinite(q).all()),
        'finite_central': bool(np.isfinite(d.central.to_numpy(float)).all()),
        'strictly_ordered': bool((np.diff(q, axis=1) > 0).all()),
        'weakly_ordered': bool((np.diff(q, axis=1) >= 0).all()),
        'y_true_equal_B0': bool(np.array_equal(ys, ref_y)),
        'p50_equals_central_rows': int(np.sum(d.p50.to_numpy(float) == d.central.to_numpy(float))),
        'max_date': str(d.delivery_date.max().date()),
    }

# ---- composite parity (§21.2, §21.7) -----------------------------------------------------------
def by(p):
    return P.loc[P.policy.eq(p)].set_index(['fold', 'timestamp_utc']).sort_index()

v5, v4, hg, dd, v3d = by('v5'), by('HGL'), by('HG'), by('D'), by('v3+D')
res['parity'] = {
    'max_abs_v5_minus_2/3v4_minus_1/3D': float(np.max(np.abs(v5.central - (2 / 3) * v4.central - (1 / 3) * dd.central))),
    'max_abs_v3D_minus_2/3HG_minus_1/3D': float(np.max(np.abs(v3d.central - (2 / 3) * hg.central - (1 / 3) * dd.central))),
    'max_abs_c_v5_minus_2/3c_v4_vs_1/3D_identity': float(np.max(np.abs((v5.central - (2 / 3) * v4.central) - dd.central / 3))),
}

# ---- hourly losses (§14.3) ---------------------------------------------------------------------
y = P.y_true.to_numpy(float)
m = P.p50.to_numpy(float)
P['AE'] = np.abs(y - m)
wis = 0.5 * np.abs(y - m)
for alpha, lo, hi in ALPHAS:
    l, u = P[lo].to_numpy(float), P[hi].to_numpy(float)
    IS = (u - l) + (2 / alpha) * (l - y) * (y < l) + (2 / alpha) * (y - u) * (y > u)
    wis = wis + (alpha / 2) * IS
P['WIS'] = wis / 3.5
for lev, lo, hi in ((50, 'p25', 'p75'), (80, 'p10', 'p90'), (95, 'p025', 'p975')):
    P[f'cov{lev}'] = ((y >= P[lo]) & (y <= P[hi])).astype(float)
P['width95'] = P.p975 - P.p025

per_fold = P.groupby(['policy', 'fold'])[['AE', 'WIS', 'cov50', 'cov80', 'cov95', 'width95']].mean()
pooled = P.groupby('policy')[['AE', 'WIS', 'cov50', 'cov80', 'cov95', 'width95']].mean()
S = {}
for p in POL:
    S[p] = {mt: float(np.mean([per_fold.loc[(p, f), k] / per_fold.loc[('B0', f), k] for f in FOLDS]))
            for mt, k in (('S_MAE', 'AE'), ('S_WIS', 'WIS'))}
res['scores'] = S
res['pooled'] = {p: {k: float(v) for k, v in pooled.loc[p].items()} for p in POL}
res['per_fold'] = {p: {f: {k: float(per_fold.loc[(p, f), k]) for k in ('AE', 'WIS', 'cov95')} for f in FOLDS} for p in POL}

# ---- §8 for every new policy (and v3, v4) ------------------------------------------------------
peak = P.loc[(P.delivery_date >= '2022-08-15') & (P.delivery_date <= '2022-08-31')]
pk = peak.groupby('policy')[['AE', 'WIS', 'cov95']].mean()
res['peak_hours'] = int(len(peak.loc[peak.policy.eq('B0')]))
BASE = ['B0', 'B1', 'B2', 'B3']
sec8 = {}
for p in NEW + ['HG', 'HGL']:
    rows = []
    rows.append((1, S[p]['S_MAE'] <= 0.9 * min(S[x]['S_MAE'] for x in BASE)))
    rows.append((2, S[p]['S_WIS'] <= 0.9 * min(S[x]['S_WIS'] for x in BASE)))
    rows.append((3, all(0.90 <= per_fold.loc[(p, f), 'cov95'] <= 0.98 for f in FOLDS)))
    rows.append((4, pk.loc[p, 'cov95'] >= 0.90 and pk.loc[p, 'AE'] <= min(pk.loc[x, 'AE'] for x in BASE)
                 and pk.loc[p, 'WIS'] <= min(pk.loc[x, 'WIS'] for x in BASE)))
    rows.append((5, all(per_fold.loc[(p, f), k] <= 1.05 * min(per_fold.loc[(x, f), k] for x in ('B2', 'B3'))
                        for f in FOLDS for k in ('AE', 'WIS'))))
    st = res['policies'][p]
    rows.append((6, st['keys_equal_expected'] and st['finite_quantiles'] and st['strictly_ordered']))
    failed = [n for n, ok in rows if not ok]
    detail = {}
    if 5 in failed:
        detail['5'] = [(f, k, float(per_fold.loc[(p, f), k]), float(1.05 * min(per_fold.loc[(x, f), k] for x in ('B2', 'B3'))))
                       for f in FOLDS for k in ('AE', 'WIS')
                       if per_fold.loc[(p, f), k] > 1.05 * min(per_fold.loc[(x, f), k] for x in ('B2', 'B3'))]
    if 1 in failed:
        detail['1'] = (S[p]['S_MAE'], 0.9 * min(S[x]['S_MAE'] for x in BASE))
    sec8[p] = {'met': not failed, 'failed': failed, 'detail': detail}
res['section8'] = sec8

# ---- bootstrap (§14.4, §17.5) ------------------------------------------------------------------
rng = np.random.default_rng(SEED)
IDX = {f: (rng.integers(0, 84, size=(REPS, 13))[:, :, None] + np.arange(7)).reshape(REPS, -1)[:, :90] for f in FOLDS}
res['index_sha256'] = hashlib.sha256(b''.join(np.asarray(IDX[f], dtype='<i8').tobytes() for f in FOLDS)).hexdigest()

daily = P.groupby(['policy', 'fold', 'delivery_date']).agg(sAE=('AE', 'sum'), sWIS=('WIS', 'sum'), n=('AE', 'size'))
win = {}
samp_S = {p: {mt: [] for mt in ('AE', 'WIS')} for p in POL}       # per fold B0-normalised replicate means
fold_daily = {}
for f in FOLDS:
    dates = P.loc[P.fold.eq(f) & P.policy.eq('B0'), 'delivery_date']
    start = dates.min()
    grid = pd.date_range(start, periods=90, freq='D')
    win[f] = (str(grid[0].date()), str(grid[-1].date()), int(dates.nunique()), bool(dates.max() <= grid[-1]))
    n = daily.loc[('B0', f)].n.reindex(grid).fillna(0).to_numpy(float)
    sums = {}
    for p in POL:
        dp = daily.loc[(p, f)].reindex(grid)
        assert np.array_equal(dp.n.fillna(0).to_numpy(float), n), (p, f)
        sums[p] = {mt: dp[f's{mt}'].fillna(0).to_numpy(float) for mt in ('AE', 'WIS')}
    ix = IDX[f]
    valid = n > 0
    for p in POL:
        for mt in ('AE', 'WIS'):
            num = sums[p][mt][ix].sum(axis=1)
            den = n[ix].sum(axis=1)
            b0 = sums['B0'][mt][ix].sum(axis=1)
            samp_S[p][mt].append((num / den) / (b0 / den))
    # per-fold paired daily-loss: mean over valid days of each day's mean loss
    dmean = {p: {mt: np.where(valid, sums[p][mt] / np.where(valid, n, 1), 0.0) for mt in ('AE', 'WIS')} for p in POL}
    fold_daily[f] = (dmean, valid)
res['fold_windows'] = win

def pct(x):
    lo, hi = np.quantile(x, [0.025, 0.975], method='linear')
    return float(lo), float(hi)

unc = {}
for cand, base in CONTRASTS:
    row = {}
    for mt, key in (('MAE', 'AE'), ('WIS', 'WIS')):
        sc = np.mean(samp_S[cand][key], axis=0)
        sb = np.mean(samp_S[base][key], axis=0)
        point = S[cand][f'S_{mt}'] - S[base][f'S_{mt}']
        lo, hi = pct(sc - sb)
        rlo, rhi = pct(sc / sb - 1)
        row[mt] = {'diff': point, 'lo': lo, 'hi': hi, 'ratio': S[cand][f'S_{mt}'] / S[base][f'S_{mt}'] - 1,
                   'ratio_lo': rlo, 'ratio_hi': rhi}
        for f in FOLDS:
            dmean, valid = fold_daily[f]
            ix = IDX[f]
            dc = dmean[cand][key][ix].sum(axis=1) / valid[ix].sum(axis=1)
            db = dmean[base][key][ix].sum(axis=1) / valid[ix].sum(axis=1)
            pt = dmean[cand][key].sum() / valid.sum() - dmean[base][key].sum() / valid.sum()
            flo, fhi = pct(dc - db)
            row[f'{f}_{mt}'] = {'diff': float(pt), 'lo': flo, 'hi': fhi}
    W, M = row['WIS'], row['MAE']
    if W['hi'] < 0 and M['hi'] <= 0:
        reading = 'observed joint improvement'
    elif W['lo'] > 0 and M['lo'] >= 0:
        reading = 'observed joint worsening'
    else:
        reading = 'no demonstrated joint preference'
    row['reading'] = reading
    unc[f'{cand}-{base}'] = row
res['contrasts'] = unc

# ---- cp23-adoption (§21.6), mechanically --------------------------------------------------------
e = unc['v5-HGL']
c1 = e['WIS']['hi'] < 0 and e['MAE']['hi'] <= 0
c2 = sec8['v5']['met']
st = res['policies']['v5']
c3_keys = st['keys_equal_expected'] and st['finite_quantiles'] and st['strictly_ordered']
worse = [(f, mt) for f in FOLDS for mt in ('MAE', 'WIS') if e[f'{f}_{mt}']['lo'] > 0]
c4 = not worse
conds = {1: c1, 2: c2, 3: c3_keys, 4: c4}
unmet = [k for k, v in conds.items() if not v]
res['adoption'] = {'conditions_met': conds, 'unmet': unmet, 'first_unmet': unmet[0] if unmet else None,
                   'adopted': not unmet, 'folds_decisively_worse': worse,
                   'note': 'condition 3 here covers keys only; its Engineering PASS clause is this review itself'}
OUT.write_text(json.dumps(res, indent=1, default=str))
print(json.dumps({'adoption': res['adoption'], 'index_sha256': res['index_sha256'],
                  'v5-HGL': {k: unc['v5-HGL'][k] for k in ('MAE', 'WIS', 'reading')}}, default=str), flush=True)
