"""CP-20 Integration Critic -- representative HG component reproduction and causal/weather controls.

Reproduction: 8 origins across all folds (warm-up and evaluation, spring-DST days, crisis peak),
fresh HG A1/B2 refits with the frozen recipe on the full (not truncated) permitted data, compared
with the cached HG components (atol 1e-8, rtol 1e-10), fit logs and identity fingerprints
recomputed here from the candidate's inputs. Controls on two origins chosen by the Critic
(different from the Lead's): delivery-day/future mask and future-weather mutation must change the
components by exactly 0.0; target-day weather change and available D-1 price change must move
them by >1e-6 EUR/MWh; all-weather-missing must reproduce the cached H0 components (<=1e-8).
Every fit runs inside counted_fits(budget, main=False); one policy-day is charged per real-data
forecast variant.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp15.data import prepare, sha
from cp20.budget import Budget
from cp20.components import augment, counted_fits, fingerprint, fit_hg
from cp20.inputs import H0Components, identities, load
from cp20.weather import COLUMNS, WeatherDesign

ART = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20')
OUT = ART / 'critic/out'
WA = ROOT / 'reports/weather-ablation'
b = Budget(os.environ['CP20_LEDGER'])
REPRO = [('fold_1', date(2020, 5, 25)), ('fold_2', date(2021, 3, 28)), ('fold_2', date(2021, 6, 29)),
         ('fold_3', date(2022, 8, 20)), ('fold_4', date(2025, 3, 30)), ('fold_4', date(2025, 7, 15)),
         ('fold_5', date(2025, 12, 2)), ('fold_5', date(2026, 3, 29))]
CONTROL = {('fold_3', date(2022, 8, 20)), ('fold_5', date(2026, 3, 29))}
proto = json.loads((WA / 'protocol.json').read_text())
features = pd.read_parquet(WA / 'weather-features.parquet')
design = WeatherDesign.from_features(features)
assert design.sha256 == proto['weather_design_sha256']
_, ids = identities(ROOT)
psha = sha(WA / 'protocol.json')
identity = {'input_fingerprint': fingerprint(ids, design.sha256, psha), 'weather_design_sha256': design.sha256, 'protocol_sha256': psha}
lin = json.loads((WA / 'lineage.json').read_text())
res = {'identity_recomputed_equals_lineage': identity == lin['hg_identity'], 'identity': identity, 'repro': [], 'controls': []}
print('identity equal', res['identity_recomputed_equals_lineage'], flush=True)
data, _ = load(ROOT)
aug, present = augment(data, design)
rng = np.random.default_rng(20260924)


def fit_pair(dat, day, rows):
    out = {}
    with counted_fits(b, main=False) as fit:
        for pol in ('A1', 'B2'):
            out[pol], _ = fit(dat, day, pol, rows=rows)
    return out


def dmax(a, c):
    return {p: float(np.max(np.abs(a[p] - c[p]))) for p in ('A1', 'B2')}


STRIP = ('fit_seconds',)
for fold, day in REPRO:
    b.reserve(policy_days=1)
    cached = json.loads((ART / 'hg-components' / fold / f'{day}.json').read_text())
    item = fit_hg(aug, present, day, fold, b, main=False, identity=identity)
    rec = {'fold': fold, 'day': str(day), 'n_hours': len(item['timestamp_utc'])}
    fresh = {p: np.asarray(item['central'][p]) for p in ('A1', 'B2')}
    cach = {p: np.asarray(cached['central'][p]) for p in ('A1', 'B2')}
    rec['max_abs'] = dmax(fresh, cach)
    rec['allclose_atol1e-8_rtol1e-10'] = all(np.allclose(fresh[p], cach[p], rtol=1e-10, atol=1e-8) for p in fresh)
    rec['bitwise'] = all(np.array_equal(fresh[p], cach[p]) for p in fresh)
    rec['identity_fields_equal'] = all(item[k] == cached[k] for k in ('input_fingerprint', 'weather_design_sha256', 'protocol_sha256', 'origin_utc', 'timestamp_utc', 'scale_sha256'))
    logs_eq = True
    for p in ('A1', 'B2'):
        for x, y in zip(item['fits'][p], cached['fits'][p]):
            if {k: v for k, v in x.items() if k not in STRIP} != {k: v for k, v in y.items() if k not in STRIP}:
                logs_eq = False
        logs_eq &= len(item['fits'][p]) == len(cached['fits'][p])
    rec['fit_logs_equal_excluding_timing'] = logs_eq
    rec['weather_rows_equal'] = item['weather_rows'] == cached['weather_rows']
    rec['selected_alphas'] = {p: sorted({l['selected_relative_alpha'] for l in item['fits'][p]}) for p in ('A1', 'B2')}
    res['repro'].append(rec)
    print(json.dumps(rec), flush=True)
    if (fold, day) not in CONTROL:
        continue
    rows = data.rows(day)
    base = fresh
    ctl = {'fold': fold, 'day': str(day), 'n_hours': int(len(rows))}
    # (a) delivery-day / future mask: prices from D on removed, later loads and later weather scrambled
    b.reserve(policy_days=1)
    fr = data.frame.copy()
    fr.loc[fr.delivery_date >= day, 'price_eur_mwh'] = np.nan
    later = fr.delivery_date > day
    fr.loc[later, 'load_forecast_mw'] = rng.uniform(1e4, 1e5, int(later.sum()))
    mdata = prepare(fr, data.p, data.spec)
    tab = design.table.copy()
    fut = np.asarray(tab.index.get_level_values(0) > day)
    tab.loc[fut, list(COLUMNS)] = rng.uniform(-50, 5000, (int(fut.sum()), 3))
    fdesign = replace(design, table=tab)
    ctl['delivery_day_and_future_mask'] = dmax(fit_pair(augment(mdata, fdesign)[0], day, rows), base)
    # (b) future weather only (delivery days after D; includes the D 00 UTC run and later)
    b.reserve(policy_days=1)
    ctl['future_weather_mutation'] = dmax(fit_pair(augment(data, fdesign)[0], day, rows), base)
    # (c) positive: target-day (D-1 run) weather changed non-affinely
    b.reserve(policy_days=1)
    tab = design.table.copy()
    tgt = np.asarray(tab.index.get_level_values(0) == day)
    tab.loc[tgt, 'wx_wind10_mean'] = tab.loc[tgt, 'wx_wind10_mean'] * 1.5
    tab.loc[tgt, 'wx_wind100_mean'] = tab.loc[tgt, 'wx_wind100_mean'] + 3.0
    tab.loc[tgt, 'wx_dswrf_mean'] = tab.loc[tgt, 'wx_dswrf_mean'] * 0.5
    ctl['target_day_weather_change'] = dmax(fit_pair(augment(data, replace(design, table=tab))[0], day, rows), base)
    ctl['target_rows_changed'] = int(tgt.sum())
    # (d) positive: available D-1 price change
    b.reserve(policy_days=1)
    fr = data.frame.copy()
    fr.loc[fr.delivery_date.eq(day - timedelta(days=1)), 'price_eur_mwh'] += 100.0
    ctl['available_d1_price_change'] = dmax(fit_pair(augment(prepare(fr, data.p, data.spec), design)[0], day, rows), base)
    # (e) missingness / arm difference: every weather value missing -> H0's cached no-weather components
    b.reserve(policy_days=1)
    tab = design.table.copy()
    tab[list(COLUMNS)] = np.nan
    neutral = fit_pair(augment(data, replace(design, table=tab))[0], day, rows)
    h0 = H0Components(ROOT, fold, data).get(day)[1]
    ctl['all_weather_missing_vs_H0'] = dmax(neutral, h0)
    ctl['hg_vs_h0'] = dmax(base, h0)
    ctl['pass'] = {'mask_exact_zero': all(v == 0.0 for v in ctl['delivery_day_and_future_mask'].values()),
                   'future_weather_exact_zero': all(v == 0.0 for v in ctl['future_weather_mutation'].values()),
                   'target_weather_positive': all(v > 1e-6 for v in ctl['target_day_weather_change'].values()),
                   'd1_price_positive': all(v > 1e-6 for v in ctl['available_d1_price_change'].values()),
                   'all_missing_equals_H0': max(ctl['all_weather_missing_vs_H0'].values()) <= 1e-8}
    res['controls'].append(ctl)
    print(json.dumps(ctl), flush=True)
json.dump(res, open(OUT / 'components.json', 'w'), indent=1, default=str)
print('DONE', json.dumps({'repro_all_allclose': all(r['allclose_atol1e-8_rtol1e-10'] for r in res['repro']),
                          'repro_all_bitwise': all(r['bitwise'] for r in res['repro']),
                          'logs_equal': all(r['fit_logs_equal_excluding_timing'] for r in res['repro']),
                          'identity_equal': all(r['identity_fields_equal'] for r in res['repro']),
                          'controls_pass': [c['pass'] for c in res['controls']]}), flush=True)
