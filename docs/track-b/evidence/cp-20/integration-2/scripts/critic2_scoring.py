"""CP-20 Integration Critic 2 -- independent scoring, section 8 criteria and paired HG-H0 bootstrap.

Own implementation from the plan text (sections 7, 8, 14.3, 14.4, 15.4); imports nothing from cp15/cp16/cp20
scoring. Reserves 1 analysis pass and 1 reference pass on the shared ledger before scoring.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

import sys
sys.path.insert(0, str(Path.cwd() / 'src'))
from cp20.budget import Budget  # noqa: E402  (ledger only)

ROOT = Path.cwd()
OUT = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic-2/out')
WA = ROOT / 'reports/weather-ablation'
POL = ['B0', 'B1', 'B2', 'B3', 'A1', 'H0', 'HG']
FOLDS = [f'fold_{i}' for i in range(1, 6)]
WIN = {'fold_1': ('2020-07-01', '2020-09-28'), 'fold_2': ('2021-04-01', '2021-06-29'), 'fold_3': ('2022-07-01', '2022-09-28'),
       'fold_4': ('2025-05-01', '2025-07-29'), 'fold_5': ('2026-01-08', '2026-04-07')}
Q = ['p025', 'p10', 'p25', 'p50', 'p75', 'p90', 'p975']
LV = np.array([.025, .1, .25, .5, .75, .9, .975])
INT = {50: ('p25', 'p75', .5), 80: ('p10', 'p90', .2), 95: ('p025', 'p975', .05)}

b = Budget(os.environ['CP20_LEDGER'])
MARK = OUT / 'scoring-pass-reserved.json'
if MARK.exists():  # continuation of this review's single charged pass after a script fault
    print('pass already reserved for this review:', MARK.read_text(), flush=True)
else:
    counts = b.reserve(analysis_passes=1, reference_passes=1)
    OUT.mkdir(parents=True, exist_ok=True)
    MARK.write_text(json.dumps({'analysis_passes': counts['analysis_passes'], 'reference_passes': counts['reference_passes'],
                                'job': os.environ.get('CP20_JOB_INDEX')}))
    print('reserved', counts, flush=True)

pred = pd.read_parquet(WA / 'predictions.parquet')
pred['date'] = pd.to_datetime(pred.delivery_date.astype(str))
y = pred.y_true.to_numpy(float)
m = pred.p50.to_numpy(float)
L = pd.DataFrame({'policy': pred.policy, 'fold': pred.fold, 'date': pred.date,
                  'lh': pred.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour})
L['ae'] = np.abs(m - y)
L['se'] = (m - y) ** 2
L['err'] = m - y
L['cae'] = np.abs(pred.central.to_numpy(float) - y)
L['ce'] = L.ae - L.cae
wis = 0.5 * np.abs(y - m)
for k, (lo, hi, a) in INT.items():
    l, u = pred[lo].to_numpy(float), pred[hi].to_numpy(float)
    L[f'w{k}'] = u - l
    L[f'hit{k}'] = (y >= l) & (y <= u)
    L[f'lm{k}'] = y < l
    L[f'um{k}'] = y > u
    wis = wis + a / 2 * (u - l) + np.clip(l - y, 0, None) + np.clip(y - u, 0, None)
L['WIS'] = wis / 3.5
r = y[:, None] - pred[Q].to_numpy(float)
L['pin7'] = np.maximum(LV * r, (LV - 1) * r).mean(axis=1)
g = L.groupby(['policy', 'fold', 'date'])
dm_pred = pd.Series(m, index=L.index).groupby([L.policy, L.fold, L.date]).transform('mean')
dm_true = pd.Series(y, index=L.index).groupby([L.policy, L.fold, L.date]).transform('mean')
L['lvl'] = np.abs(dm_pred - dm_true)
L['shape'] = np.abs((m - dm_pred) - (y - dm_true))
L['block'] = np.where((L.lh >= 22) | (L.lh <= 5), 'night', np.where((L.lh >= 10) & (L.lh <= 16), 'solar', 'shoulder'))


def summ(s):
    n = len(s)
    out = {'n_hours': n, 'n_days': s.date.nunique(), 'MAE': s.ae.mean(), 'RMSE': np.sqrt(s.se.mean()), 'WIS': s.WIS.mean(),
           'mean_pinball_7': s.pin7.mean(), 'raw_central_MAE': s.cae.mean(), 'centering_effect': s.ce.mean(), 'bias': s.err.mean(),
           'daily_mean_level_MAE': s.groupby(['fold', 'date']).lvl.first().mean(), 'within_day_shape_MAE': s['shape'].mean()}
    for k in INT:
        out.update({f'coverage{k}': s[f'hit{k}'].sum() / n, f'hit_count{k}': int(s[f'hit{k}'].sum()),
                    f'lower_miss_count{k}': int(s[f'lm{k}'].sum()), f'upper_miss_count{k}': int(s[f'um{k}'].sum()),
                    f'mean_width{k}': s[f'w{k}'].mean(), f'median_width{k}': s[f'w{k}'].median(),
                    f'p95_width{k}': s[f'w{k}'].quantile(.95)})
    return out


mine = {}
for p in POL:
    sp = L[L.policy == p]
    mine[(p, 'pooled', 'all', '')] = summ(sp)
    for f in FOLDS:
        sf = sp[sp.fold == f]
        mine[(p, 'per_fold', f, '')] = summ(sf)
        for h in range(24):
            mine[(p, 'hour', f, str(h))] = summ(sf[sf.lh == h]) | {'support': sf[sf.lh == h].date.nunique() >= 56}
        for bl in ('night', 'solar', 'shoulder'):
            mine[(p, 'block', f, bl)] = summ(sf[sf.block == bl]) | {'support': sf[sf.block == bl].date.nunique() >= 56}
    pk = sp[(sp.fold == 'fold_3') & sp.date.between('2022-08-15', '2022-08-31')]
    mine[(p, 'peak', 'fold_3', 'August15-31')] = summ(pk)
    for d0 in (1, 8, 15, 22):
        s = f'2022-09-{d0:02}'
        e = f'2022-09-{d0 + 6:02}'
        mine[(p, 'recovery', 'fold_3', s)] = summ(sp[(sp.fold == 'fold_3') & sp.date.between(s, e)])

metrics = pd.read_csv(WA / 'metrics.csv')
diag = pd.read_csv(WA / 'diagnostics.csv', low_memory=False)
cmp_cols = [c for c in next(iter(mine.values())) if c != 'support']
maxdiff, count_mismatch, missing, compared = {}, [], [], 0
for key, val in mine.items():
    p, scope, f, grp = key
    if scope in ('pooled', 'per_fold'):
        row = metrics[(metrics.policy == p) & (metrics.scope == scope) & (metrics.fold == f)]
    else:
        row = diag[(diag.policy == p) & (diag.scope == scope) & (diag.fold == f) & (diag.group.astype(str) == grp)]
    if len(row) != 1:
        missing.append(key)
        continue
    row = row.iloc[0]
    compared += 1
    for c in cmp_cols:
        a, bv = float(val[c]), float(row[c])
        if c.startswith(('n_', 'hit_count', 'lower_miss', 'upper_miss')):
            if a != bv:
                count_mismatch.append((key, c, a, bv))
        else:
            maxdiff[c] = max(maxdiff.get(c, 0.0), abs(a - bv))
    if 'support' in val and (row['support_status'] == 'eligible') != val['support']:
        count_mismatch.append((key, 'support_status', val['support'], row['support_status']))
n_metric_rows = len(metrics[metrics.scope.isin(['pooled', 'per_fold'])]) + len(diag[diag.scope.isin(['hour', 'block', 'peak', 'recovery'])])

# daily table
daily = g.agg(n_hours=('WIS', 'size'), MAE=('ae', 'mean'), WIS=('WIS', 'mean'), coverage95=('hit95', 'mean'),
              hit_count95=('hit95', 'sum'), lower_miss_count95=('lm95', 'sum'), upper_miss_count95=('um95', 'sum'),
              mean_width95=('w95', 'mean')).reset_index()
dd = diag[diag.scope == 'daily'].copy()
dd['date'] = pd.to_datetime(dd.delivery_date)
full = []
for f, (s, e) in WIN.items():
    for p in POL:
        for d in pd.date_range(s, e):
            full.append((p, f, d))
grid = pd.DataFrame(full, columns=['policy', 'fold', 'date']).merge(daily, how='left', on=['policy', 'fold', 'date'])
grid['n_hours'] = grid.n_hours.fillna(0).astype(int)
jj = grid.merge(dd, on=['policy', 'fold', 'date'], suffixes=('', '_c'), how='outer', indicator=True)
daily_rows_ok = (jj._merge == 'both').all() and len(jj) == 3150
daily_diff = {c: float(np.nanmax(np.abs(jj[c].astype(float) - jj[c + '_c'].astype(float)))) for c in
              ['MAE', 'WIS', 'coverage95', 'hit_count95', 'lower_miss_count95', 'upper_miss_count95', 'mean_width95']}
daily_nan_pattern_ok = all((jj[c].isna() == jj[c + '_c'].isna()).all() for c in ['MAE', 'WIS'])
daily_nhours_ok = (jj.n_hours == jj.n_hours_c).all()

# equal-fold scores
S = {p: {mt: float(np.mean([mine[(p, 'per_fold', f, '')][mt] / mine[('B0', 'per_fold', f, '')][mt] for f in FOLDS]))
         for mt in ('MAE', 'WIS')} for p in POL}
ef = metrics[metrics.scope == 'equal_fold'].set_index('policy')
s_diff = max(max(abs(S[p]['MAE'] - ef.loc[p, 'S_MAE']), abs(S[p]['WIS'] - ef.loc[p, 'S_WIS'])) for p in POL)
pooled_ratio_diff = max(max(abs(mine[(p, 'pooled', 'all', '')][mt] / mine[('B0', 'pooled', 'all', '')][mt]
                            - metrics[(metrics.policy == p) & (metrics.scope == 'pooled')][f'pooled_ratio_{mt}'].iloc[0]) for mt in ('MAE', 'WIS')) for p in POL)

# section 8 criteria, own reading of the plan
crit = []
BASE = ['B0', 'B1', 'B2', 'B3']
for p in ('H0', 'HG'):
    crit.append((p, 1, 'S_MAE', 'equal_fold', S[p]['MAE'], None, 0.9 * min(S[x]['MAE'] for x in BASE)))
    crit.append((p, 2, 'S_WIS', 'equal_fold', S[p]['WIS'], None, 0.9 * min(S[x]['WIS'] for x in BASE)))
    for f in FOLDS:
        crit.append((p, 3, 'coverage95', f, mine[(p, 'per_fold', f, '')]['coverage95'], .90, .98))
    pk = lambda q, mt: mine[(q, 'peak', 'fold_3', 'August15-31')][mt]
    crit.append((p, 4, 'coverage95', 'peak', pk(p, 'coverage95'), .90, None))
    for mt in ('MAE', 'WIS'):
        crit.append((p, 4, mt, 'peak', pk(p, mt), None, min(pk(x, mt) for x in BASE)))
        for f in FOLDS:
            crit.append((p, 5, mt, f, mine[(p, 'per_fold', f, '')][mt], None,
                         1.05 * min(mine[(x, 'per_fold', f, '')][mt] for x in ('B2', 'B3'))))
    ok6 = int(len(L[L.policy == p]) == 10747 and np.isfinite(pred.loc[pred.policy == p, Q].to_numpy()).all()
              and (np.diff(pred.loc[pred.policy == p, Q].to_numpy(), axis=1) >= 0).all())
    crit.append((p, 6, 'complete_finite_ordered', 'all_eligible', ok6, 1, 1))
cc = pd.read_csv(WA / 'criteria.csv')
crit_mismatch, crit_maxdiff = [], 0.0
status = {}
for p, n, mt, sc, act, lo, hi in crit:
    passed = (lo is None or act >= lo) and (hi is None or act <= hi)
    status.setdefault(p, []).append(passed)
    row = cc[(cc.policy == p) & (cc.criterion == n) & (cc.metric == mt) & (cc.scope == sc)]
    if len(row) != 1:
        crit_mismatch.append(('missing', p, n, mt, sc))
        continue
    row = row.iloc[0]
    crit_maxdiff = max(crit_maxdiff, abs(act - row.actual), abs((hi if hi is not None else 0) - (0 if pd.isna(row.upper_limit) else row.upper_limit)),
                       abs((lo if lo is not None else 0) - (0 if pd.isna(row.lower_limit) else row.lower_limit)))
    if bool(row.passed) != bool(passed):
        crit_mismatch.append((p, n, mt, sc, passed, row.passed))
section8 = {p: ('met' if all(v) else 'not_met') for p, v in status.items()}
failed = {p: sorted({c[1] for c, ok in zip([c for c in crit if c[0] == p], status[p]) if not ok}) for p in status}

# paired block bootstrap, one shared index set
rng = np.random.default_rng(15042)
IX = {}
for f in FOLDS:
    starts = rng.integers(0, 84, size=(2000, 13))
    IX[f] = (starts[:, :, None] + np.arange(7)[None, None, :]).reshape(2000, 91)[:, :90]
ix_sha = hashlib.sha256(b''.join(np.asarray(IX[f], dtype='<i8').tobytes() for f in FOLDS)).hexdigest()
lin = json.loads((WA / 'lineage.json').read_text())
ratios, points, perfold = [], [], {}
for f in FOLDS:
    dates = pd.date_range(*WIN[f])
    sums = np.zeros((90, len(POL), 2))
    cnt = np.zeros((90, len(POL)))
    dmean = np.full((90, len(POL), 2), np.nan)
    for j, p in enumerate(POL):
        sub = L[(L.policy == p) & (L.fold == f)]
        gg = sub.groupby('date').agg(n=('ae', 'size'), sae=('ae', 'sum'), swis=('WIS', 'sum')).reindex(dates)
        cnt[:, j] = gg.n.fillna(0).to_numpy()
        sums[:, j, 0] = gg.sae.fillna(0).to_numpy()
        sums[:, j, 1] = gg.swis.fillna(0).to_numpy()
        valid = cnt[:, j] > 0
        dmean[valid, j, 0] = sums[valid, j, 0] / cnt[valid, j]
        dmean[valid, j, 1] = sums[valid, j, 1] / cnt[valid, j]
    assert (cnt == cnt[:, :1]).all()
    ix = IX[f]
    samp = sums[ix].sum(axis=1) / cnt[ix].sum(axis=1)[:, :, None]          # (R, P, 2) resampled means
    ratios.append(samp / samp[:, :1, :])
    pt = sums.sum(axis=0) / cnt.sum(axis=0)[:, None]
    points.append(pt / pt[:1, :])
    valid = cnt[:, 0] > 0
    dz = np.where(valid[:, None, None], dmean, 0.0)
    ds = dz[ix].sum(axis=1) / valid[ix].sum(axis=1)[:, None, None]
    dp = dz.sum(axis=0) / valid.sum()
    a, bb = POL.index('HG'), POL.index('H0')
    for k, mt in enumerate(('MAE', 'WIS')):
        draws = ds[:, a, k] - ds[:, bb, k]
        perfold[(f, mt)] = (float(dp[a, k] - dp[bb, k]), *np.quantile(draws, [.025, .975], method='linear'))
agg = np.mean(ratios, axis=0)
ptt = np.mean(points, axis=0)
a, bb = POL.index('HG'), POL.index('H0')
eq = {}
for k, mt in enumerate(('MAE', 'WIS')):
    draws = agg[:, a, k] - agg[:, bb, k]
    eq[mt] = (float(ptt[a, k] - ptt[bb, k]), *[float(x) for x in np.quantile(draws, [.025, .975], method='linear')],
              int((~np.isfinite(draws)).sum()))
unc = pd.read_csv(WA / 'uncertainty.csv')
unc_diff = 0.0
for _, row in unc.iterrows():
    mine_row = eq[row.metric][:3] if row.scope == 'equal_fold' else perfold[(row.scope, row.metric)]
    unc_diff = max(unc_diff, *(abs(x - y) for x, y in zip(mine_row, (row.difference, row.ci_lower, row.ci_upper))))
joint = eq['WIS'][2] < 0 and eq['MAE'][2] <= 0
result = {
    'rows_scored': len(L), 'summary_cells_compared': compared, 'summary_cells_in_candidate': n_metric_rows, 'summary_missing': missing,
    'max_abs_diff_by_column': maxdiff, 'count_or_support_mismatches': count_mismatch[:20],
    'daily_rows_matched': bool(daily_rows_ok), 'daily_max_abs_diff': daily_diff, 'daily_nan_pattern_ok': bool(daily_nan_pattern_ok),
    'daily_n_hours_equal': bool(daily_nhours_ok),
    'S_scores': S, 'S_max_abs_diff': s_diff, 'pooled_ratio_max_abs_diff': pooled_ratio_diff,
    'criteria_rows': len(crit), 'criteria_candidate_rows': len(cc), 'criteria_mismatches': crit_mismatch, 'criteria_max_abs_diff': crit_maxdiff,
    'section8_status': section8, 'section8_failed_criteria': failed,
    'bootstrap_index_sha256': ix_sha, 'lineage_index_sha256': lin['research_summary']['bootstrap']['index_sha256'],
    'equal_fold_HG_minus_H0': {k: dict(zip(('point', 'ci_lower', 'ci_upper', 'undefined'), v)) for k, v in eq.items()},
    'per_fold_daily_HG_minus_H0': {f'{f}:{mt}': v for (f, mt), v in perfold.items()},
    'uncertainty_max_abs_diff': unc_diff,
    'joint_rule_observed_joint_improvement': bool(joint),
    'candidate_joint_conclusion': lin['research_summary']['joint_conclusions'],
    'descriptive_order': sorted(['H0', 'HG'], key=lambda p: (S[p]['WIS'], S[p]['MAE'], p != 'H0')),
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'scoring.json').write_text(json.dumps(result, indent=1, default=float))
print(json.dumps(result, indent=1, default=float)[:6000])
