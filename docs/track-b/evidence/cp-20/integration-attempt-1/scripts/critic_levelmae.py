"""Follow-up to critic_scoring (same analysis pass, no bootstrap, no new pass charged):
recompute only daily_mean_level_MAE with the day-weighted definition (mean over represented
delivery days of |daily mean p50 - daily mean truth|, day means over the full day) and compare."""
import json
from pathlib import Path
import numpy as np, pandas as pd
WA = Path.cwd() / 'reports/weather-ablation'
pr = pd.read_parquet(WA / 'predictions.parquet', columns=['policy', 'fold', 'timestamp_utc', 'delivery_date', 'y_true', 'p50'])
pr['date'] = pd.to_datetime(pr.delivery_date)
g = pr.groupby(['policy', 'fold', 'date'])
pr['lvl'] = np.abs(g.p50.transform('mean') - g.y_true.transform('mean'))
pr['lh'] = pr.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour
pr['block'] = np.where((pr.lh >= 22) | (pr.lh <= 5), 'night', np.where(pr.lh.between(10, 16), 'solar', 'shoulder'))
lv = lambda x: x.groupby(['fold', 'date']).lvl.first().mean()
met = pd.read_csv(WA / 'metrics.csv'); dg = pd.read_csv(WA / 'diagnostics.csv', low_memory=False)
worst = 0.0; n = 0
for _, r in met[met.scope.isin(['pooled', 'per_fold'])].iterrows():
    x = pr[pr.policy == r.policy] if r.scope == 'pooled' else pr[(pr.policy == r.policy) & (pr.fold == r.fold)]
    worst = max(worst, abs(lv(x) - r.daily_mean_level_MAE)); n += 1
for _, r in dg[dg.scope.isin(['hour', 'block', 'peak', 'recovery'])].iterrows():
    x = pr[(pr.policy == r.policy) & (pr.fold == r.fold)]
    if r.scope == 'hour': x = x[x.lh == int(r.group)]
    elif r.scope == 'block': x = x[x.block == r.group]
    elif r.scope == 'peak': x = x[x.date.between('2022-08-15', '2022-08-31')]
    else: x = x[x.date.between(r.window_start, r.window_end)]
    worst = max(worst, abs(lv(x) - r.daily_mean_level_MAE)); n += 1
print(json.dumps({'rows_compared': n, 'max_abs_diff_daily_mean_level_MAE': worst}))
json.dump({'rows_compared': n, 'max_abs_diff_daily_mean_level_MAE': worst}, open('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic/out/levelmae.json', 'w'))
