"""CP-20 Integration Critic 2 -- representative HG component reproduction, causal/weather controls, refusals.

Fits run through the inherited recipe inside cp20.components.counted_fits(b, main=False): every component-day
attempt and every Lasso solver call is reserved on the shared ledger first. One policy-day is reserved per
real-data A1+B2 forecast pair. Origins differ from the Lead's and from Integration attempt 1.
Budget for this job: 36 component-day attempts (4 reproduction origins x 2 + 2 control origins x 7 variants x 2).
"""
from __future__ import annotations

from dataclasses import replace
from datetime import date, timedelta
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp15.data import prepare, history_start  # noqa: E402
from cp20.budget import Budget  # noqa: E402
from cp20.components import HGComponents, augment, counted_fits  # noqa: E402
from cp20.execution import cache_dir, check_protocol, hg_identity, weather_design  # noqa: E402
from cp20.inputs import H0Components, load  # noqa: E402
from cp20 import weather as W  # noqa: E402

OUT = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic-2/out')
TMP = Path('/Users/djourno/Downloads/PJM/.local/tmp/cp-20/critic-2')
WA = ROOT / 'reports/weather-ablation'
COLS = list(W.COLUMNS)
REPRO = [('fold_1', date(2020, 6, 10)), ('fold_2', date(2021, 4, 4)), ('fold_3', date(2022, 8, 26)), ('fold_5', date(2026, 4, 7))]
CONTROL = [('fold_2', date(2021, 5, 20)), ('fold_4', date(2025, 4, 25))]
TIMING = {'fit_seconds', 'hour_fit_seconds', 'seconds', 'elapsed_seconds'}

b = Budget(os.environ['CP20_LEDGER'])
res = {'reproduction': [], 'controls': [], 'refusals': {}, 'augmentation': []}
start_counts = dict(b.read()['counts'])

p = check_protocol(ROOT)
design = weather_design(ROOT, p)
identity = hg_identity(ROOT, p)
lin = json.loads((WA / 'lineage.json').read_text())
res['identity_recomputed'] = identity
res['identity_equals_lineage'] = identity == lin['hg_identity']
data, _ = load(ROOT)
aug, present = augment(data, design)

# ---------------- own local-hour weather table from weather-features.parquet (independent of WeatherDesign)
wf = pd.read_parquet(WA / 'weather-features.parquet')
wf['lh'] = wf.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour
own = {}
for (d, h), g in wf.groupby(['delivery_date', 'lh']):
    v = g[COLS].to_numpy(float)
    own[(d, h)] = v.mean(axis=0) if np.isfinite(v).all() else np.full(3, np.nan)


def own_matrix(rows):
    out = np.full((len(rows), 3), np.nan)
    for i, r in enumerate(rows):
        key = (pd.Timestamp(data.dates[r]).date(), int(data.hours[r]))
        if key in own:
            out[i] = own[key]
    return out


def fit_pair(dset, day, rows):
    b.reserve(policy_days=1)
    out, logs = {}, {}
    with counted_fits(b, main=False) as fit:
        for pol in ('A1', 'B2'):
            out[pol], logs[pol] = fit(dset, day, pol, rows=rows)
    return out, logs


def maxabs(a, c):
    return {k: float(np.max(np.abs(np.asarray(a[k]) - np.asarray(c[k])))) for k in ('A1', 'B2')}


def strip(logs):
    return [{k: v for k, v in r.items() if k not in TIMING and 'seconds' not in k} for r in logs]


def check_aug(fold, day, rows):
    rec = {'fold': fold, 'day': str(day)}
    idx = np.unique(np.concatenate([rows] + [np.flatnonzero((data.dates >= np.datetime64(history_start(day, pol))) & (data.dates < np.datetime64(day)) & data.eligible) for pol in ('A1', 'B2')]))
    mine = own_matrix(idx)
    theirs = aug.lear_raw[idx, -3:]
    rec['rows_checked'] = int(len(idx))
    rec['weather_cols_equal_own_lookup'] = bool(np.array_equal(mine, theirs, equal_nan=True) and np.array_equal(aug.lear_normalized[idx, -3:], theirs, equal_nan=True))
    rec['other_cols_unchanged'] = bool(np.array_equal(aug.lear_raw[:, :-3], data.lear_raw, equal_nan=True) and np.array_equal(aug.lear_normalized[:, :-3], data.lear_normalized, equal_nan=True))
    rec['only_3_columns_added'] = aug.lear_raw.shape[1] == data.lear_raw.shape[1] + 3
    rec['training_rows_weather_missing'] = int((~np.isfinite(theirs)).any(axis=1).sum())
    res['augmentation'].append(rec)


def reproduce(fold, day):
    rows = data.rows(day)
    check_aug(fold, day, rows)
    cache = HGComponents(cache_dir(), fold, data, identity)
    item = cache.load(day)
    cached = cache.get(day)[1]
    fresh, logs = fit_pair(aug, day, rows)
    d = maxabs(fresh, cached)
    close = all(np.allclose(fresh[k], cached[k], atol=1e-8, rtol=1e-10) for k in ('A1', 'B2'))
    logs_equal = all(strip(logs[k]) == strip(item['fits'][k]) for k in ('A1', 'B2'))
    rec = {'fold': fold, 'day': str(day), 'n_hours': int(len(rows)), 'max_abs': d, 'bitwise': all(v == 0.0 for v in d.values()),
           'allclose_atol1e-8_rtol1e-10': close, 'fit_logs_equal_excluding_timing': logs_equal,
           'cache_identity_fields': {k: item[k] for k in identity}, 'source': item['source']}
    if not logs_equal:
        rec['log_diff_example'] = [(a, c) for a, c in zip(strip(logs['A1']), strip(item['fits']['A1'])) if a != c][:1]
    return rec, fresh, rows


# ---------------- refusals and cache identity (synthetic or copies; no fits)
R = res['refusals']
try:
    bad = data.frame.iloc[:48].copy()
    bad['delivery_date'] = bad['delivery_date'].map(lambda d: d - timedelta(days=1))
    prepare(bad, data.p, data.spec)
    R['prepare_pre_2019'] = 'NOT refused'
except ValueError as exc:
    R['prepare_pre_2019'] = str(exc)
for pol in ('A1', 'B2', 'A4'):
    try:
        R[f'history_start_{pol}_2019-02-01'] = str(history_start(date(2019, 2, 1), pol))
    except ValueError as exc:
        R[f'history_start_{pol}_2019-02-01'] = 'refused: ' + str(exc)
try:
    W.missing_day(date(2021, 1, 1), 'extraction_not_finished', 'x')
    R['non_imputable_missing_class'] = 'NOT refused'
except W.ConversionRefused as exc:
    R['non_imputable_missing_class'] = str(exc)
try:
    W.build_features({'structural_missing': [], 'runs': [{'delivery_day': '2021-01-02', 'run_00z': '2021-01-01', 'version': 'v15.1'}]}, TMP / 'empty-weather')
    R['unfinished_extraction'] = 'NOT refused'
except W.ConversionRefused as exc:
    R['unfinished_extraction'] = str(exc)
try:
    W.hour_leads(date(2021, 1, 1))
    R['hour_leads_2021-01-01'] = list(map(int, W.hour_leads(date(2021, 1, 1))))
except W.ConversionRefused as exc:
    R['hour_leads_2021-01-01'] = str(exc)
try:
    W.interpolate_wind(np.zeros((10, 2, 2)), np.zeros((10, 2, 2)), 49)
    R['no_extrapolation_h49'] = 'NOT refused'
except W.ConversionRefused as exc:
    R['no_extrapolation_h49'] = str(exc)
q = [0.01] * 10
bounds_bad = [(18, 21), (18, 24)] + [(0, 0)] * 8
try:
    W.radiation_block(np.zeros((10, 2, 2)), [(18, 21), (21, 24)] + [(0, 0)] * 8, q, 24)
    R['radiation_wrong_bounds'] = 'NOT refused'
except W.ConversionRefused as exc:
    R['radiation_wrong_bounds'] = str(exc)
arr = np.zeros((10, 2, 2))
arr[1] = -0.02          # 2*(-0.02) - 0 = -0.04 >= -3q (q=0.02): clipped
blk, log = W.radiation_block(arr, bounds_bad, [0.02] * 10, 24)
R['radiation_clip_within_3q'] = {'clipped_cells': log.get('clipped_cells'), 'min_block': log.get('min_block'), 'result_min': float(blk.min())}
arr[1] = -0.05          # -0.10 < -0.06: conversion failure
blk, log = W.radiation_block(arr, bounds_bad, [0.02] * 10, 24)
R['radiation_below_minus_3q'] = {'block': None if blk is None else 'returned', 'failure': log.get('failure')}
blk, log = W.radiation_block(np.zeros((10, 2, 2)), bounds_bad, [None] * 10, 24)
R['radiation_unknown_quantum'] = log.get('failure')
# stale / wrong cache refusal on a private copy of one real entry
TMP.mkdir(parents=True, exist_ok=True)
tdir = Path(tempfile.mkdtemp(dir=TMP))
fold, day = CONTROL[0]
(tdir / fold).mkdir()
src = cache_dir() / fold / f'{day}.json'
shutil.copy(src, tdir / fold / src.name)
ok_load = HGComponents(tdir, fold, data, identity).load(day) is not None
try:
    HGComponents(tdir, fold, data, {**identity, 'protocol_sha256': '0' * 64}).load(day)
    R['cache_wrong_identity'] = 'NOT refused'
except ValueError as exc:
    R['cache_wrong_identity'] = str(exc)
item = json.loads((tdir / fold / src.name).read_text())
item['central']['A1'][0] += 1.0
(tdir / fold / src.name).write_text(json.dumps(item))
try:
    HGComponents(tdir, fold, data, identity).load(day)
    R['cache_tampered_content'] = 'NOT refused'
except ValueError as exc:
    R['cache_tampered_content'] = str(exc)
try:
    HGComponents(tdir, fold, data, identity).get(day + timedelta(days=1))
    R['cache_miss'] = 'NOT refused'
except ValueError as exc:
    R['cache_miss'] = str(exc)
R['cache_copy_loads_unmodified'] = ok_load
shutil.rmtree(tdir)
print('refusals', json.dumps(R, default=str), flush=True)



def save():
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / 'components.partial.json').write_text(json.dumps(res, indent=1, default=str))


for fold, day in REPRO:
    rec, _, _ = reproduce(fold, day)
    res['reproduction'].append(rec)
    save()
    print('repro', json.dumps(rec)[:600], flush=True)

rng = np.random.default_rng(20260924)
for fold, day in CONTROL:
    rec, base, rows = reproduce(fold, day)
    res['reproduction'].append(rec)
    c = {'fold': fold, 'day': str(day), 'n_hours': int(len(rows))}
    dates = design.table.index.get_level_values(0)
    # 1. delivery-day and future mask (prices from D, loads after D, weather after D)
    fr = data.frame.copy()
    fr.loc[fr.delivery_date >= day, 'price_eur_mwh'] = np.nan
    fr.loc[fr.delivery_date > day, 'load_forecast_mw'] = 7.7e7
    mt = design.table.copy()
    mt.loc[dates > day, COLS] = rng.normal(1e5, 1e4, size=(int((dates > day).sum()), 3))
    mdata = prepare(fr, data.p, data.spec)
    c['mask_rows_identical'] = bool(np.array_equal(mdata.rows(day), rows))
    out, _ = fit_pair(augment(mdata, replace(design, table=mt))[0], day, rows)
    c['delivery_day_and_future_mask_change'] = maxabs(out, base)
    # 2. future weather only
    out, _ = fit_pair(augment(data, replace(design, table=mt))[0], day, rows)
    c['future_weather_only_change'] = maxabs(out, base)
    # 3. available D-1 price mutation (positive)
    fr = data.frame.copy()
    fr.loc[fr.delivery_date == day - timedelta(days=1), 'price_eur_mwh'] += 250.0
    out, _ = fit_pair(augment(prepare(fr, data.p, data.spec), design)[0], day, rows)
    c['available_d1_price_change'] = maxabs(out, base)
    # 4. target-day (D-1 00 UTC run) weather, non-affine per-hour change (positive)
    tt = design.table.copy()
    tgt = dates == day
    k = int(tgt.sum())
    tt.loc[tgt, COLS] = tt.loc[tgt, COLS].to_numpy() * rng.uniform(0.2, 2.5, size=(k, 3)) + rng.uniform(1, 4, size=(k, 3)) * np.array([1, 1, 50])
    out, _ = fit_pair(augment(data, replace(design, table=tt))[0], day, rows)
    c['target_day_weather_change'] = maxabs(out, base)
    c['target_rows_changed'] = k
    # 5. training-history weather permutation (positive)
    pt = design.table.copy()
    pool = np.flatnonzero((dates < day) & np.isfinite(pt[COLS].to_numpy(float)).all(axis=1))
    vals = pt[COLS].to_numpy(float, copy=True)
    vals[pool] = vals[rng.permutation(pool)]
    pt[COLS] = vals
    out, _ = fit_pair(augment(data, replace(design, table=pt))[0], day, rows)
    c['training_weather_permutation_change'] = maxabs(out, base)
    # 6. all weather missing -> must reproduce the no-weather H0 components (arm difference = weather only)
    nt = design.table.copy()
    nt[COLS] = np.nan
    out, _ = fit_pair(augment(data, replace(design, table=nt))[0], day, rows)
    h0 = H0Components(ROOT, fold, data).get(day)[1]
    c['all_weather_missing_vs_H0_max_abs'] = maxabs(out, h0)
    c['hg_vs_h0_max_abs'] = maxabs(base, h0)
    c['negative_controls_exact_zero'] = all(v == 0.0 for v in (*c['delivery_day_and_future_mask_change'].values(), *c['future_weather_only_change'].values()))
    c['positive_controls_above_1e-6'] = all(max(c[x].values()) > 1e-6 for x in ('available_d1_price_change', 'target_day_weather_change', 'training_weather_permutation_change'))
    c['all_missing_equals_H0_within_1e-8'] = max(c['all_weather_missing_vs_H0_max_abs'].values()) <= 1e-8
    res['controls'].append(c)
    save()
    print('control', json.dumps(c), flush=True)

end_counts = b.read()['counts']
res['charged_by_this_job'] = {k: end_counts[k] - start_counts.get(k, 0) for k in ('component_attempts', 'main_component_attempts', 'primitive_fits', 'inner_fits', 'final_fits', 'policy_days') if end_counts.get(k, 0) != start_counts.get(k, 0)}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'components.json').write_text(json.dumps(res, indent=1, default=str))
print(json.dumps({k: v for k, v in res.items() if k != 'reproduction'}, indent=1, default=str)[:5000])
