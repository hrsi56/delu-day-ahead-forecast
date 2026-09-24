"""CP-20 Integration Critic -- independent scoring, section 8 criteria and paired bootstrap.

Own implementation from the plan text (sections 7, 8, 14.3, 14.4, 15.4); only the frozen
bootstrap draw convention (seed 15042; per fold in fold order: 13 noncircular 7-day block
starts uniform on 0..83, concatenated and truncated to 90 dates) is taken from the protocol.
Charges one analysis pass and one reference pass before scoring.
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
from cp20.budget import Budget

ROOT = Path.cwd()
OUT = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic/out')
WA = ROOT / 'reports/weather-ablation'
b = Budget(os.environ['CP20_LEDGER'])
print('reserved', b.reserve(analysis_passes=1, reference_passes=1), flush=True)

FOLDS = ['fold_1', 'fold_2', 'fold_3', 'fold_4', 'fold_5']
WIN = {'fold_1': ('2020-07-01', '2020-09-28'), 'fold_2': ('2021-04-01', '2021-06-29'), 'fold_3': ('2022-07-01', '2022-09-28'),
       'fold_4': ('2025-05-01', '2025-07-29'), 'fold_5': ('2026-01-08', '2026-04-07')}
POL = ['B0', 'B1', 'B2', 'B3', 'A1', 'H0', 'HG']
Q = ['p025', 'p10', 'p25', 'p50', 'p75', 'p90', 'p975']
TAU = np.array([.025, .10, .25, .50, .75, .90, .975])
INT = [(50, .5, 'p25', 'p75'), (80, .2, 'p10', 'p90'), (95, .05, 'p025', 'p975')]

pr = pd.read_parquet(WA / 'predictions.parquet')
pr['date'] = pd.to_datetime(pr.delivery_date)
y = pr.y_true.to_numpy(float)
m = pr.p50.to_numpy(float)
pr['ae'] = np.abs(m - y)
pr['se'] = (m - y) ** 2
pr['err'] = m - y
pr['cae'] = np.abs(pr.central.to_numpy(float) - y)
tot = np.abs(m - y) * 0.5
for cov, a, l, u in INT:
    L, U = pr[l].to_numpy(float), pr[u].to_numpy(float)
    pr[f'w{cov}'] = U - L
    pr[f'hit{cov}'] = (y >= L) & (y <= U)
    pr[f'lo{cov}'] = y < L
    pr[f'up{cov}'] = y > U
    # interval score times alpha/2 = alpha/2*(U-L) + (L-y)+ + (y-U)+
    tot = tot + a / 2 * (U - L) + np.clip(L - y, 0, None) + np.clip(y - U, 0, None)
pr['wis'] = tot / 3.5
r = y[:, None] - pr[Q].to_numpy(float)
pr['pin'] = np.where(r >= 0, TAU * r, (TAU - 1) * r).mean(axis=1)
grp = pr.groupby(['policy', 'fold', 'date'])
pr['dm_p'] = grp.p50.transform('mean')
pr['dm_y'] = grp.y_true.transform('mean')
pr['lvl'] = np.abs(pr.dm_p - pr.dm_y)
pr['shp'] = np.abs((pr.p50 - pr.dm_p) - (pr.y_true - pr.dm_y))
pr['lh'] = pr.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour
pr['block'] = np.where((pr.lh >= 22) | (pr.lh <= 5), 'night', np.where(pr.lh.between(10, 16), 'solar', 'shoulder'))


def summ(g):
    out = {'n_hours': len(g), 'n_days': g.date.nunique(), 'MAE': g.ae.mean(), 'RMSE': np.sqrt(g.se.mean()), 'WIS': g.wis.mean(),
           'mean_pinball_7': g.pin.mean(), 'raw_central_MAE': g.cae.mean(), 'centering_effect': (g.ae - g.cae).mean(),
           'bias': g.err.mean(), 'daily_mean_level_MAE': g.lvl.mean(), 'within_day_shape_MAE': g.shp.mean()}
    for cov, *_ in INT:
        w = g[f'w{cov}'].to_numpy()
        out |= {f'coverage{cov}': g[f'hit{cov}'].mean(), f'hit_count{cov}': g[f'hit{cov}'].sum(),
                f'lower_miss_count{cov}': g[f'lo{cov}'].sum(), f'upper_miss_count{cov}': g[f'up{cov}'].sum(),
                f'mean_width{cov}': w.mean(), f'median_width{cov}': np.median(w), f'p95_width{cov}': np.quantile(w, .95)}
    return out


def compare(mine: pd.DataFrame, theirs: pd.DataFrame, keys, label):
    a = mine.set_index(keys).sort_index()
    t = theirs.set_index(keys).sort_index()
    if not a.index.equals(t.index):
        return {'label': label, 'index_equal': False, 'mine': len(a), 'theirs': len(t)}
    worst, col_w = 0.0, None
    for c in a.columns:
        if c not in t.columns:
            continue
        x = pd.to_numeric(a[c], errors='coerce').to_numpy(float)
        z = pd.to_numeric(t[c], errors='coerce').to_numpy(float)
        both_nan = np.isnan(x) & np.isnan(z)
        if (np.isnan(x) != np.isnan(z)).any():
            return {'label': label, 'index_equal': True, 'nan_pattern_differs': c}
        d = np.abs(x - z)[~both_nan]
        if d.size and d.max() > worst:
            worst, col_w = float(d.max()), c
    return {'label': label, 'index_equal': True, 'rows': len(a), 'columns_compared': [c for c in a.columns if c in t.columns],
            'max_abs_diff': worst, 'worst_column': col_w}


res = {}
met = pd.read_csv(WA / 'metrics.csv')
# per-fold and pooled
mine = []
for p in POL:
    g = pr[pr.policy == p]
    mine.append({'policy': p, 'scope': 'pooled', 'fold': 'all', **summ(g)})
    for f in FOLDS:
        mine.append({'policy': p, 'scope': 'per_fold', 'fold': f, **summ(g[g.fold == f])})
mine = pd.DataFrame(mine)
S = {}
for p in POL:
    S[p] = {}
    for k in ('MAE', 'WIS'):
        num = mine[(mine.policy == p) & (mine.scope == 'per_fold')].set_index('fold')[k].reindex(FOLDS).to_numpy()
        den = mine[(mine.policy == 'B0') & (mine.scope == 'per_fold')].set_index('fold')[k].reindex(FOLDS).to_numpy()
        S[p][f'S_{k}'] = float(np.mean(num / den))
pooled_b0 = mine[(mine.policy == 'B0') & (mine.scope == 'pooled')].iloc[0]
mine.loc[mine.scope == 'pooled', 'pooled_ratio_MAE'] = mine.loc[mine.scope == 'pooled', 'MAE'] / pooled_b0.MAE
mine.loc[mine.scope == 'pooled', 'pooled_ratio_WIS'] = mine.loc[mine.scope == 'pooled', 'WIS'] / pooled_b0.WIS
their = met[met.scope.isin(['pooled', 'per_fold'])].copy()
res['metrics_per_fold_and_pooled'] = compare(mine, their[[c for c in their.columns if c in mine.columns]], ['policy', 'scope', 'fold'], 'metrics')
eq = met[met.scope == 'equal_fold'].set_index('policy')
res['equal_fold_scores'] = {p: {k: [S[p][k], float(eq.loc[p, k]), abs(S[p][k] - float(eq.loc[p, k]))] for k in ('S_MAE', 'S_WIS')} for p in POL}
res['equal_fold_max_abs_diff'] = max(v[k][2] for v in res['equal_fold_scores'].values() for k in v)

# diagnostics: hour/block/peak/recovery and daily
dg = pd.read_csv(WA / 'diagnostics.csv', low_memory=False)
rows = []
for p in POL:
    g = pr[pr.policy == p]
    for f in FOLDS:
        gf = g[g.fold == f]
        for h in range(24):
            x = gf[gf.lh == h]
            rows.append({'policy': p, 'fold': f, 'scope': 'hour', 'group': str(h), 'support_status': 'eligible' if x.date.nunique() >= 56 else 'support_limited', **summ(x)})
        for bl in ('night', 'solar', 'shoulder'):
            x = gf[gf.block == bl]
            rows.append({'policy': p, 'fold': f, 'scope': 'block', 'group': bl, 'support_status': 'eligible' if x.date.nunique() >= 56 else 'support_limited', **summ(x)})
    x = g[(g.fold == 'fold_3') & g.date.between('2022-08-15', '2022-08-31')]
    rows.append({'policy': p, 'fold': 'fold_3', 'scope': 'peak', 'group': 'August15-31', **summ(x)})
    for st in (1, 8, 15, 22):
        x = g[(g.fold == 'fold_3') & g.date.between(f'2022-09-{st:02}', f'2022-09-{st + 6:02}')]
        rows.append({'policy': p, 'fold': 'fold_3', 'scope': 'recovery', 'group': f'2022-09-{st:02}', **summ(x)})
mdg = pd.DataFrame(rows)
tdg = dg[dg.scope.isin(['hour', 'block', 'peak', 'recovery'])].copy()
tdg['group'] = tdg.group.astype(str)
res['diagnostics_hour_block_peak_recovery'] = compare(mdg.drop(columns=['support_status']), tdg[[c for c in tdg.columns if c in mdg.columns and c != 'support_status']], ['policy', 'fold', 'scope', 'group'], 'diagnostics')
sup = mdg.set_index(['policy', 'fold', 'scope', 'group']).support_status.dropna()
tsup = tdg.set_index(['policy', 'fold', 'scope', 'group']).support_status.reindex(sup.index)
res['support_labels_equal'] = bool((sup == tsup).all())
res['support_limited_cells'] = int((sup == 'support_limited').sum())
# daily
drows = []
for (p, f), g in pr.groupby(['policy', 'fold']):
    dd = g.groupby('date').agg(n_hours=('wis', 'size'), MAE=('ae', 'mean'), WIS=('wis', 'mean'), coverage95=('hit95', 'mean'),
                               hit_count95=('hit95', 'sum'), lower_miss_count95=('lo95', 'sum'), upper_miss_count95=('up95', 'sum'),
                               mean_width95=('w95', 'mean'))
    dd = dd.reindex(pd.date_range(*WIN[f]))
    dd['n_hours'] = dd.n_hours.fillna(0)
    dd.index.name = 'delivery_date'
    dd = dd.reset_index()
    dd['policy'], dd['fold'] = p, f
    drows.append(dd)
mday = pd.concat(drows, ignore_index=True)
tday = dg[dg.scope == 'daily'].copy()
tday['delivery_date'] = pd.to_datetime(tday.delivery_date)
res['daily_rows'] = compare(mday, tday[[c for c in tday.columns if c in mday.columns]], ['policy', 'fold', 'delivery_date'], 'daily')

# section 8 criteria (plan text)
pf = mine[mine.scope == 'per_fold'].set_index(['policy', 'fold'])
pk = mdg[mdg.scope == 'peak'].set_index('policy')
crit = []
for c in ('H0', 'HG'):
    for n_, k in ((1, 'S_MAE'), (2, 'S_WIS')):
        lim = 0.9 * min(S[bb][k] for bb in ('B0', 'B1', 'B2', 'B3'))
        crit.append((c, n_, k, 'equal_fold', S[c][k], None, lim))
    for f in FOLDS:
        crit.append((c, 3, 'coverage95', f, pf.loc[(c, f), 'coverage95'], .90, .98))
    crit.append((c, 4, 'coverage95', 'peak', pk.loc[c, 'coverage95'], .90, None))
    for k in ('MAE', 'WIS'):
        crit.append((c, 4, k, 'peak', pk.loc[c, k], None, min(pk.loc[bb, k] for bb in ('B0', 'B1', 'B2', 'B3'))))
        for f in FOLDS:
            crit.append((c, 5, k, f, pf.loc[(c, f), k], None, 1.05 * min(pf.loc[(bb, f), k] for bb in ('B2', 'B3'))))
    g = pr[pr.policy == c]
    six = float(len(g) == 10747 and np.isfinite(g[Q].to_numpy()).all() and (np.diff(g[Q].to_numpy(), axis=1) >= 0).all())
    crit.append((c, 6, 'complete_finite_ordered', 'all_eligible', six, 1.0, 1.0))
mc = pd.DataFrame(crit, columns=['policy', 'criterion', 'metric', 'scope', 'actual', 'lower_limit', 'upper_limit'])
mc['passed'] = [(lo is None or pd.isna(lo) or a >= lo) and (up is None or pd.isna(up) or a <= up) for a, lo, up in zip(mc.actual, mc.lower_limit, mc.upper_limit)]
tc = pd.read_csv(WA / 'criteria.csv')
mc['criterion'] = mc.criterion.astype(int)
res['criteria'] = compare(mc.drop(columns=['passed']), tc[['policy', 'criterion', 'metric', 'scope', 'actual', 'lower_limit', 'upper_limit']], ['policy', 'criterion', 'metric', 'scope'], 'criteria')
tcp = tc.set_index(['policy', 'criterion', 'metric', 'scope']).passed.sort_index()
mcp = mc.set_index(['policy', 'criterion', 'metric', 'scope']).passed.sort_index()
res['criteria_pass_flags_equal'] = bool((tcp.astype(bool) == mcp.astype(bool)).all())
res['section8_status'] = {c: 'met' if mc[mc.policy == c].passed.all() else 'not_met' for c in ('H0', 'HG')}
res['section8_failed'] = {c: sorted(mc[(mc.policy == c) & ~mc.passed].criterion.unique().tolist()) for c in ('H0', 'HG')}

# paired bootstrap (own implementation)
rng = np.random.default_rng(15042)
IDX = {}
for f in FOLDS:
    starts = rng.integers(0, 84, size=(2000, 13))
    IDX[f] = (starts[:, :, None] + np.arange(7)[None, None, :]).reshape(2000, 91)[:, :90]
fp = hashlib.sha256(b''.join(np.asarray(IDX[f], dtype='<i8').tobytes() for f in FOLDS)).hexdigest()
lin = json.loads((WA / 'lineage.json').read_text())
res['bootstrap_index_sha256'] = {'mine': fp, 'lineage': lin['research_summary']['bootstrap']['index_sha256'], 'equal': fp == lin['research_summary']['bootstrap']['index_sha256']}
ratio_rep = {k: [] for k in ('MAE', 'WIS')}
ratio_pt = {k: [] for k in ('MAE', 'WIS')}
perfold = []
for f in FOLDS:
    dates = pd.date_range(*WIN[f])
    g = pr[pr.fold == f]
    sums = {k: g.pivot_table(index='date', columns='policy', values={'MAE': 'ae', 'WIS': 'wis'}[k], aggfunc='sum').reindex(index=dates, columns=POL).fillna(0.0).to_numpy() for k in ('MAE', 'WIS')}
    cnt = g.pivot_table(index='date', columns='policy', values='ae', aggfunc='size').reindex(index=dates, columns=POL).fillna(0).to_numpy(float)
    ix = IDX[f]
    for k in ('MAE', 'WIS'):
        s_rep = sums[k][ix].sum(axis=1)          # (2000, 7)
        c_rep = cnt[ix].sum(axis=1)
        mean_rep = s_rep / c_rep
        ratio_rep[k].append(mean_rep / mean_rep[:, [0]])
        mean_pt = sums[k].sum(axis=0) / cnt.sum(axis=0)
        ratio_pt[k].append(mean_pt / mean_pt[0])
        # descriptive per-fold daily-loss difference: equal weight per valid sampled date
        daily = np.where(cnt > 0, sums[k] / np.where(cnt > 0, cnt, 1), 0.0)
        valid = cnt[:, 0] > 0
        dsamp = daily[ix].sum(axis=1) / valid[ix].sum(axis=1)[:, None]
        dpt = daily[valid].mean(axis=0)
        a, bb = POL.index('HG'), POL.index('H0')
        dif = dsamp[:, a] - dsamp[:, bb]
        lo_, hi_ = np.quantile(dif, [.025, .975], method='linear')
        perfold.append({'scope': f, 'metric': k, 'difference': dpt[a] - dpt[bb], 'ci_lower': lo_, 'ci_upper': hi_})
eqrows = []
for k in ('MAE', 'WIS'):
    rep = np.mean(ratio_rep[k], axis=0)
    pt = np.mean(ratio_pt[k], axis=0)
    a, bb = POL.index('HG'), POL.index('H0')
    dif = rep[:, a] - rep[:, bb]
    lo_, hi_ = np.quantile(dif, [.025, .975], method='linear')
    eqrows.append({'scope': 'equal_fold', 'metric': k, 'difference': pt[a] - pt[bb], 'ci_lower': lo_, 'ci_upper': hi_,
                   'undefined': int((~np.isfinite(dif)).sum())})
    res[f'equal_fold_point_vs_S_{k}'] = abs((pt[a] - pt[bb]) - (S['HG'][f'S_{k}'] - S['H0'][f'S_{k}']))
mu = pd.DataFrame(perfold + eqrows)
tu = pd.read_csv(WA / 'uncertainty.csv')
res['uncertainty'] = compare(mu[['scope', 'metric', 'difference', 'ci_lower', 'ci_upper']], tu[['scope', 'metric', 'difference', 'ci_lower', 'ci_upper']], ['scope', 'metric'], 'uncertainty')
e = {r['metric']: r for r in eqrows}
joint = bool(e['WIS']['ci_upper'] < 0 and e['MAE']['ci_upper'] <= 0)
res['equal_fold_HG_minus_H0'] = eqrows
res['joint_rule_mine'] = 'observed joint improvement' if joint else 'no demonstrated joint preference'
res['joint_rule_theirs'] = lin['research_summary']['joint_conclusions']
res['ranking_mine'] = sorted(['H0', 'HG'], key=lambda p: (S[p]['S_WIS'], S[p]['S_MAE'], p != 'H0'))
res['per_fold_hg_minus_h0'] = perfold
json.dump(res, open(OUT / 'scoring.json', 'w'), indent=1, default=str)
for k, v in res.items():
    print(k, json.dumps(v, default=str)[:900], flush=True)
