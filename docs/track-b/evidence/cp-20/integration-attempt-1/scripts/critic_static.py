"""CP-20 Integration Critic -- static/contract verification (no fits, no replay, no decode).

Reads the candidate worktree (cwd) and local CP-20 evidence read-only. Writes only to
.local/artifacts/cp-20/critic/out/. Charges nothing but monitor machine time.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path.cwd()
P = Path('/Users/djourno/Downloads/PJM')
ART = P / '.local/artifacts/cp-20'
OUT = ART / 'critic/out'
OUT.mkdir(parents=True, exist_ok=True)
WA = ROOT / 'reports/weather-ablation'
R = {}
FAIL = []


def check(name, ok, detail=None):
    R[name] = {'ok': bool(ok), 'detail': detail}
    if not ok:
        FAIL.append(name)
    print(('PASS ' if ok else 'FAIL ') + name + ('' if detail is None else f' :: {detail}'), flush=True)


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


# ------------------------------------------------------------------ issued identities
issued = {'capstone_v21.md': '150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167',
          'docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md': '3e0bdf6a343d5336f406f0eeb726b1b65c0f767ec8d9418a7d8118902e1ace55',
          'docs/track-b/cp-20-direct-weather-brief.md': '28a4e195fa7f66ff3270d5d54e477478e90aa42124bceb1ee529f95f5761883e'}
check('issued_document_sha256', all(sha_file(ROOT / k) == v for k, v in issued.items()))
check('intake_receipt_present', (ROOT / 'docs/track-b/weather-content-intake-2026-09-23.md').exists())
bad, n = [], 0
for mf in sorted((ROOT / 'reports/weather-admission/hashes').glob('*.sha256')):
    for line in mf.read_text().splitlines():
        if not line.strip():
            continue
        d, path = line.split(maxsplit=1)
        path = path.lstrip('*')
        cand = [ROOT / path, ROOT / 'reports/weather-admission' / path, P / path]
        hit = next((c for c in cand if c.exists()), None)
        if hit is None:
            continue
        n += 1
        if sha_file(hit) != d:
            bad.append(path)
check('admission_bundle_hash_lists_match_present_files', not bad, {'checked': n, 'bad': bad[:10]})

# ------------------------------------------------------------------ protocol freeze identities
proto = json.loads((WA / 'protocol.json').read_text())
mism = {}
for sec in ('implementation_sha256', 'frozen_inputs_sha256', 'issued_and_inherited_sha256'):
    for name, d in proto[sec].items():
        if ':' in name:
            continue
        h = sha_file(ROOT / name)
        if h != d:
            b = (ROOT / name).read_bytes()
            mism[name] = {'section': sec, 'frozen': d, 'candidate': h,
                          'candidate_with_CRLF': hashlib.sha256(b.replace(b'\n', b'\r\n')).hexdigest()}
check('protocol_frozen_hashes_match_candidate_bytes', not mism, mism)
am = json.loads((WA / 'artifact-manifest.json').read_text())
amm = {k: v for k, v in am['artifact_sha256'].items() if (ROOT / k).exists() and sha_file(ROOT / k) != v}
check('artifact_manifest_hashes_match_candidate_bytes', not amm, amm)

# ------------------------------------------------------------------ predictions
pred = pd.read_parquet(WA / 'predictions.parquet')
Q = ['p025', 'p10', 'p25', 'p50', 'p75', 'p90', 'p975']
check('predictions_rows_75229', len(pred) == 75229, len(pred))
cnt = pred.groupby('policy').size().to_dict()
check('seven_policies_10747_each', set(cnt) == {'B0', 'B1', 'B2', 'B3', 'A1', 'H0', 'HG'} and set(cnt.values()) == {10747}, cnt)
arms = pred[pred.policy.isin(['H0', 'HG'])]
check('contrast_rows_21494', len(arms) == 21494, len(arms))
fc = pred[pred.policy == 'HG'].groupby('fold').size().to_dict()
check('fold_counts', fc == {'fold_1': 2160, 'fold_2': 2159, 'fold_3': 2112, 'fold_4': 2160, 'fold_5': 2156}, fc)
keysets = {p: frozenset(map(tuple, g[['fold', 'timestamp_utc']].astype(str).to_numpy())) for p, g in pred.groupby('policy')}
check('identical_keys_all_policies', len(set(keysets.values())) == 1)
check('no_duplicate_policy_keys', not pred.duplicated(['policy', 'fold', 'timestamp_utc']).any())
num = pred[['y_true', 'central', 'level', 'scale', *Q]].to_numpy(float)
check('all_finite', bool(np.isfinite(num).all()))
check('ordered_quantiles_no_crossing', bool((np.diff(pred[Q].to_numpy(float), axis=1) >= 0).all()))
check('evidence_class_label', set(pred.evidence_class) == {'development_post_selection'}, sorted(set(pred.evidence_class)))
exp_origin = pd.to_datetime(pred.delivery_date) - pd.Timedelta(days=1) + pd.Timedelta(hours=11)
check('origin_is_D_minus_1_1100_utc', bool((pred.origin_utc.dt.tz_convert('UTC').dt.tz_localize(None).astype('datetime64[us]') == exp_origin.astype('datetime64[us]')).all()))
loc = pred.timestamp_utc.dt.tz_convert('Europe/Berlin')
check('delivery_date_is_berlin_local_date', bool((loc.dt.date == pred.delivery_date).all()))
for arm in ('H0', 'HG'):
    g = pred[pred.policy == arm]
    check(f'{arm}_p50_emitted_separately_from_central', float((g.p50 != g.central).mean()) > 0.99, float((g.p50 != g.central).mean()))
cp16 = pd.read_parquet(ROOT / 'reports/v2-causal/predictions.parquet')
v2h = cp16[cp16.policy == 'V2-H'].sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
h0 = pred[pred.policy == 'H0'].sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
cols = ['y_true', 'central', 'level', 'scale', *Q]
keys_eq = h0[['fold', 'timestamp_utc', 'delivery_date', 'origin_utc']].equals(v2h[['fold', 'timestamp_utc', 'delivery_date', 'origin_utc']])
bits_eq = all(np.array_equal(h0[c].to_numpy().view(np.uint64), v2h[c].to_numpy().view(np.uint64)) for c in cols)
check('H0_bitwise_equals_CP16_V2H_all_10747', len(h0) == 10747 and keys_eq and bits_eq,
      {'rows': len(h0), 'keys_equal': bool(keys_eq), 'bitwise': bool(bits_eq),
       'max_abs': float(np.max(np.abs(h0[cols].to_numpy(float) - v2h[cols].to_numpy(float))))})
cp15 = pd.read_parquet(ROOT / 'reports/cp15/predictions.parquet')
refok = {}
for p in ('B0', 'B1', 'B2', 'B3', 'A1'):
    a = pred[pred.policy == p].sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
    b = cp15[cp15.policy == p].sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
    refok[p] = bool(len(a) == len(b) == 10747 and a[['fold', 'timestamp_utc']].equals(b[['fold', 'timestamp_utc']])
                    and all(np.array_equal(a[c].to_numpy().view(np.uint64), b[c].to_numpy().view(np.uint64)) for c in cols))
check('saved_references_bitwise_equal_cp15', all(refok.values()), refok)
hg = pred[pred.policy == 'HG'].sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
check('H0_HG_same_truth_scale_level', all(np.array_equal(h0[c].to_numpy(), hg[c].to_numpy()) for c in ('y_true', 'scale', 'level')))
check('HG_central_differs_from_H0', float((hg.central != h0.central).mean()) > 0.99, float((hg.central != h0.central).mean()))
f3 = hg[hg.fold == 'fold_3']
dd = pd.to_datetime(f3.delivery_date)
peak = f3[(dd >= '2022-08-15') & (dd <= '2022-08-31')]
check('fold3_88_dates_peak_408h_17d', f3.delivery_date.nunique() == 88 and len(peak) == 408 and peak.delivery_date.nunique() == 17,
      {'f3_dates': int(f3.delivery_date.nunique()), 'peak_rows': len(peak), 'peak_days': int(peak.delivery_date.nunique())})

# ------------------------------------------------------------------ origin and run manifests
im = json.loads((ROOT / 'reports/v2-causal/input-manifest.json').read_text())
origins = [(f['fold'], date.fromisoformat(o['day'])) for f in im['folds'] for o in f['origins']]
adm = [(f['fold'], x['day']) for f in im['folds'] for x in f['admission']]
check('cp16_manifest_638_origins_35_admission', len(origins) == 638 and len(adm) == 35, {'origins': len(origins), 'admission': len(adm)})
ws = {f['fold']: f['warmup_start'] for f in im['folds']}
check('warmup_starts', ws == {'fold_1': '2020-05-25', 'fold_2': '2021-02-23', 'fold_3': '2022-05-25', 'fold_4': '2025-03-22', 'fold_5': '2025-12-02'}, ws)
need = set()
for _, d in origins:
    x = max(date(2019, 1, 1), d - timedelta(days=728))
    while x <= d:
        need.add(x)
        x += timedelta(days=1)
rm = json.loads((WA / 'run-manifest.json').read_text())
mdays = {date.fromisoformat(r['delivery_day']) for r in rm['runs']}
sdays = {date.fromisoformat(s['delivery_day']) for s in rm['structural_missing']}
check('run_manifest_2476_runs_plus_structural_2019_01_01', len(rm['runs']) == 2476 and sdays == {date(2019, 1, 1)}, {'runs': len(rm['runs']), 'structural': sorted(map(str, sdays))})
check('run_manifest_days_equal_required_union', (mdays | sdays) == need, {'need': len(need), 'manifest': len(mdays | sdays)})
check('run_is_delivery_minus_1', all(date.fromisoformat(r['run_00z']) == date.fromisoformat(r['delivery_day']) - timedelta(days=1) for r in rm['runs']))


def ver(run):
    return 'v14' if run < date(2019, 6, 13) else ('v15.1' if run < date(2021, 3, 23) else 'v16')


check('run_manifest_version_by_date', all(r['version'] == ver(date.fromisoformat(r['run_00z'])) for r in rm['runs']))
added = [r for r in rm['runs'] if not r['admission']['inventoried']]
check('eight_added_runs_2023_03_24_31', sorted(r['run_00z'] for r in added) == [f'2023-03-{d}' for d in range(24, 32)], sorted(r['run_00z'] for r in added))
check('no_run_before_2019', min(date.fromisoformat(r['run_00z']) for r in rm['runs']) >= date(2019, 1, 1))
check('availability_bracketed_all_runs', all(r['availability']['bracketed'] for r in rm['runs']), rm.get('availability_not_bracketed'))

# ------------------------------------------------------------------ messages (123,800)
msg = pd.read_parquet(WA / 'messages.parquet')
check('messages_123800_unique', len(msg) == 123800 and not msg.duplicated(['run_00z', 'lead', 'field']).any()
      and bool(msg.groupby('run_00z').size().eq(50).all()) and msg.run_00z.nunique() == 2476, len(msg))
check('messages_leads_fields', set(msg.lead) == {21, 24, 27, 30, 33, 36, 39, 42, 45, 48} and set(msg.field) == {'u10', 'v10', 'u100', 'v100', 'dswrf'})
run_dt = pd.to_datetime(msg.run_00z)
valid = run_dt + pd.to_timedelta(msg.lead, unit='h')
problems = Counter()
problems['dataDate'] = int((msg.dataDate != run_dt.dt.strftime('%Y%m%d').astype(int)).sum())
problems['dataTime'] = int((msg.dataTime != 0).sum())
problems['validityDate'] = int((msg.validityDate != valid.dt.strftime('%Y%m%d').astype(int)).sum())
problems['validityTime'] = int((msg.validityTime != valid.dt.hour * 100).sum())
wind = msg.field != 'dswrf'
sn = {'u10': '10u', 'v10': '10v', 'u100': '100u', 'v100': '100v', 'dswrf': 'dswrf'}
problems['shortName'] = int((msg.shortName != msg.field.map(sn)).sum())
w = msg[wind]
problems['wind_level'] = int((w.level != w.field.str[1:].astype(int)).sum())
problems['wind_typeOfLevel'] = int((w.typeOfLevel != 'heightAboveGround').sum())
problems['wind_units'] = int((w.units != 'm s**-1').sum())
problems['wind_step'] = int(((w.startStep != w.lead) | (w.endStep != w.lead) | (w.stepType != 'instant')).sum())
problems['wind_param'] = int((w.parameterNumber != w.field.str[0].map({'u': 2, 'v': 3})).sum())
problems['wind_surface'] = int((w.typeOfFirstFixedSurface != 103).sum())
d = msg[~wind]
lo = np.where(d.lead % 6 == 3, d.lead - 3, d.lead - 6)
problems['dswrf_bounds'] = int(((d.startStep != lo) | (d.endStep != d.lead) | (d.stepType != 'avg')).sum())
problems['dswrf_units_surface'] = int(((d.units != 'W m**-2') | (d.typeOfLevel != 'surface') | (d.typeOfFirstFixedSurface != 1)).sum())
problems['dswrf_param'] = int((~d.parameterNumber.isin([192, 7])).sum())
problems['production_status'] = int((msg.productionStatusOfProcessedData != 0).sum())
problems['processed_type'] = int((msg.typeOfProcessedData != 1).sum())
problems['generating_process'] = int((msg.generatingProcessIdentifier != 96).sum())
problems['centre'] = int((msg.centre != 'kwbc').sum())
q = 2.0 ** msg.binaryScaleFactor.astype(float) / 10.0 ** msg.decimalScaleFactor.astype(float)
problems['quantum'] = int((q != msg.packing_quantum).sum())
problems['box_nonfinite'] = int((msg.box_nonfinite != 0).sum())
problems['bytes'] = int((msg['bytes'] != msg.byte_end - msg.byte_start + 1).sum())
problems['version'] = int((msg.version != msg.run_00z.map(lambda s: ver(date.fromisoformat(s)))).sum())
coarse = d.packing_quantum >= 1.0
problems['dswrf_precision_vs_version'] = int((coarse != (d.version != 'v16')).sum())
ymd = run_dt.dt.strftime('%Y%m%d')
lead3 = msg.lead.map('{:03d}'.format)
aws_url = 'https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.' + ymd + '/00/' + pd.Series(np.where(msg.version == 'v16', 'atmos/', ''), index=msg.index) + 'gfs.t00z.pgrb2.0p25.f' + lead3
ncar_url = 'https://tds.gdex.ucar.edu/thredds/fileServer/files/g/d084001/' + run_dt.dt.year.astype(str) + '/' + ymd + '/gfs.0p25.' + ymd + '00.f' + lead3 + '.grib2'
problems['url'] = int((msg.url != pd.Series(np.where(msg.endpoint == 'aws', aws_url, ncar_url), index=msg.index)).sum())
check('messages_metadata_all_valid', sum(problems.values()) == 0, dict(problems))
ep = msg.groupby('endpoint').size().to_dict()
check('messages_by_endpoint', ep == {'aws': 87200, 'ncar': 36600}, ep)
R['messages_by_version'] = msg.groupby('version').size().to_dict()
primary = {r['run_00z']: (r['primary_endpoint'], r['alternate_endpoint']) for r in rm['runs']}
offm = [(r, e) for r, e in zip(msg.run_00z, msg.endpoint) if e not in primary[r]]
check('endpoint_is_primary_or_named_alternate', not offm, offm[:10])
alt = msg[[e != primary[r][0] for r, e in zip(msg.run_00z, msg.endpoint)]]
R['alternate_endpoint_messages'] = {'count': int(len(alt)), 'runs': sorted(alt.run_00z.unique().tolist())[:40]}
print('alternate endpoint messages', len(alt), alt.run_00z.nunique())

# ------------------------------------------------------------------ local per-run records and npz integrity
grid_bad, npz_bad, meta_bad, nrec = [], [], [], 0
want_grid = {'gridType': 'regular_ll', 'Ni': 1440, 'Nj': 721, 'latitudeOfFirstGridPointInDegrees': 90.0,
             'longitudeOfFirstGridPointInDegrees': 0.0, 'latitudeOfLastGridPointInDegrees': -90.0,
             'longitudeOfLastGridPointInDegrees': 359.75, 'iDirectionIncrementInDegrees': 0.25,
             'jDirectionIncrementInDegrees': 0.25, 'jScansPositively': 0, 'iScansNegatively': 0, 'editionNumber': 2,
             'numberOfDataPoints': 1440 * 721, 'significanceOfReferenceTime': 1, 'typeOfGeneratingProcess': 2}
msg_sha = {(r, l, f): s for r, l, f, s in zip(msg.run_00z, msg.lead, msg.field, msg.sha256)}
for r in rm['runs']:
    rec = json.loads((ART / 'weather/runs' / f"{r['run_00z']}.json").read_text())
    nrec += 1
    if rec.get('status') != 'complete' or sha_file(ART / 'weather/runs' / f"{r['run_00z']}.npz") != rec['npz_sha256']:
        npz_bad.append(r['run_00z'])
    for m in rec['messages']:
        mm = m['meta']
        if any(mm.get(k) != v for k, v in want_grid.items()):
            grid_bad.append((r['run_00z'], m['lead'], m['field']))
        if msg_sha.get((r['run_00z'], m['lead'], m['field'])) != m['sha256']:
            meta_bad.append((r['run_00z'], m['lead'], m['field']))
check('run_records_complete_and_npz_sha256', not npz_bad and nrec == 2476, {'records': nrec, 'bad': npz_bad[:10]})
check('grid_metadata_every_message', not grid_bad, grid_bad[:10])
check('run_record_sha_equals_messages_parquet', not meta_bad, meta_bad[:10])

# ------------------------------------------------------------------ retained raw byte identity
raw_bad, raw_n = [], 0
for dd_ in sorted((ART / 'weather/raw').iterdir()):
    for fpath in sorted(dd_.iterdir()):
        lead_s, field, endpoint = fpath.stem.split('_')
        raw_n += 1
        m = msg[(msg.run_00z == dd_.name) & (msg.lead == int(lead_s[1:])) & (msg.field == field)]
        if len(m) != 1 or m.iloc[0].endpoint != endpoint or sha_file(fpath) != m.iloc[0].sha256:
            raw_bad.append(str(fpath.relative_to(ART)))
retain = set(rm['retain_raw'])
check('cp20_retained_raw_sha256_equals_messages', not raw_bad and raw_n == 50 * len(retain)
      and {p.name for p in (ART / 'weather/raw').iterdir()} == retain, {'files': raw_n, 'runs': len(retain), 'bad': raw_bad[:10]})
ADM = {'u10': 'u10', 'v10': 'v10', 'u100': 'u_hub', 'v100': 'v_hub', 'dswrf': 'ssrd'}
inv = {v: k for k, v in ADM.items()}
listed = {}
for line in (ROOT / 'reports/weather-admission/hashes/raw_sample_objects.sha256').read_text().splitlines():
    dg, path = line.split(maxsplit=1)
    listed[Path(path).name] = dg
adm_dir = P / '.local/weather-admission/cache/gfs'
adm_bad, adm_n, adm_cmp, adm_runs = [], 0, 0, set()
for fpath in sorted(adm_dir.iterdir()):
    if not fpath.name.endswith('.grib2'):
        continue
    adm_n += 1
    h = sha_file(fpath)
    if listed.get(fpath.name) != h:
        adm_bad.append(('listed', fpath.name))
    parts = fpath.stem.split('_')
    run, lead_s, endpoint, fld = parts[0], parts[1], parts[-1], inv['_'.join(parts[2:-1])]
    adm_runs.add(run)
    m = msg[(msg.run_00z == run) & (msg.lead == int(lead_s[1:])) & (msg.field == fld) & (msg.endpoint == endpoint)]
    if len(m) == 1:
        adm_cmp += 1
        if m.iloc[0].sha256 != h:
            adm_bad.append(('cp20', fpath.name))
check('admission_600_retained_samples_byte_identical', adm_n == 600 and adm_cmp == 600 and not adm_bad,
      {'files': adm_n, 'compared_to_cp20': adm_cmp, 'runs': sorted(adm_runs), 'bad': adm_bad[:10]})
shc = pd.read_csv(WA / 'sample-hash-comparison.csv')
check('sample_hash_comparison_csv_600_identical', len(shc) == 600 and bool(shc.identical.all()))

# ------------------------------------------------------------------ weather features
sys.path.insert(0, str(ROOT / 'src'))
from cp15.data import day_hours
wf = pd.read_parquet(WA / 'weather-features.parquet')
days = sorted(need)
exp_ts = pd.DatetimeIndex(np.concatenate([day_hours(x).tz_convert('UTC').tz_localize(None).as_unit('ms').to_numpy() for x in days]))
got_ts = pd.DatetimeIndex(wf.timestamp_utc.dt.tz_convert('UTC').dt.tz_localize(None).sort_values().to_numpy()).as_unit('ms')
check('features_cover_every_canonical_hour_of_required_days', len(wf) == len(exp_ts) and got_ts.equals(exp_ts), {'rows': len(wf), 'expected': len(exp_ts)})
ok = wf.status == 'ok'
check('features_status_classes', wf.status.value_counts().to_dict() == {'ok': 59422, 'structural_missing_pre_2019_run': 24}, wf.status.value_counts().to_dict())
st = wf[~ok]
check('structural_rows_are_2019_01_01_all_nan', bool((st.delivery_date == date(2019, 1, 1)).all()) and bool(st[['wx_wind10_mean', 'wx_wind100_mean', 'wx_dswrf_mean']].isna().all().all()))
check('ok_rows_finite', bool(np.isfinite(wf.loc[ok, ['wx_wind10_mean', 'wx_wind100_mean', 'wx_dswrf_mean']].to_numpy()).all()))
runexp = (pd.to_datetime(wf.loc[ok, 'delivery_date']) - pd.Timedelta(days=1)).dt.strftime('%Y-%m-%d')
check('feature_run_is_D_minus_1_00z', bool((wf.loc[ok, 'run_00z'] == runexp).all()))
lead = (wf.timestamp_utc.dt.tz_convert('UTC').dt.tz_localize(None) - (pd.to_datetime(wf.delivery_date) - pd.Timedelta(days=1))) / pd.Timedelta(hours=1)
check('feature_lead_hours_22_to_46', bool((lead == wf.lead_hour).all()) and bool(wf.lead_hour.between(22, 46).all()), [int(wf.lead_hour.min()), int(wf.lead_hour.max())])
check('features_dswrf_nonnegative_wind_positive', bool((wf.loc[ok, 'wx_dswrf_mean'] >= 0).all()) and bool((wf.loc[ok, ['wx_wind10_mean', 'wx_wind100_mean']] > 0).all().all()))
wf['lh'] = wf.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour
g = wf.groupby(['delivery_date', 'lh'])
check('local_hour_cells_59440_repeated_6', len(g) == 59440 and int((g.size() == 2).sum()) == 6, {'cells': len(g), 'repeated': int((g.size() == 2).sum())})
from cp20.weather import WeatherDesign
check('weather_design_sha256_matches_protocol', WeatherDesign.from_features(pd.read_parquet(WA / 'weather-features.parquet')).sha256 == proto['weather_design_sha256'])
check('clipping_log_within_minus_3q', bool((wf.loc[ok, 'dswrf_min_block'] >= -3 * wf.loc[ok, 'dswrf_quantum'] - 1e-12).all()))

# ------------------------------------------------------------------ HG component cache: identity and fit accounting
lin = json.loads((WA / 'lineage.json').read_text())
ident = lin['hg_identity']


def digest(item):
    return hashlib.sha256(json.dumps({k: v for k, v in item.items() if k != 'content_sha256'}, sort_keys=True,
                                     allow_nan=False, default=str).encode()).hexdigest()


cache = ART / 'hg-components'
items, cbad, hist_bad = 0, [], []
solver_calls, hour_fits, sources = 0, 0, Counter()
wx_missing_train, wx_missing_fc = 0, 0
for fold, dday in origins:
    path = cache / fold / f'{dday}.json'
    if not path.exists():
        cbad.append(('missing', fold, str(dday)))
        continue
    it = json.loads(path.read_text())
    items += 1
    sources[it['source']] += 1
    if it['content_sha256'] != digest(it) or any(it.get(k) != v for k, v in ident.items()) or it['day'] != str(dday) or it['fold'] != fold:
        cbad.append(('identity', fold, str(dday)))
    for pol in ('A1', 'B2'):
        for log in it['fits'].get(pol, []):
            solver_calls += log['solver_calls']
            hour_fits += 1
            if log['selected_relative_alpha'] not in (0.001, 0.01, 0.1, 1.0) or log['fit_calls'] != 5 or len(log['validation_mae_by_alpha']) != 4:
                cbad.append(('fitlog', fold, str(dday), pol))
            if log['history_start'] != str(max(date(2019, 1, 1), dday - timedelta(days=728))) or log['history_end_exclusive'] != str(dday):
                hist_bad.append((fold, str(dday), pol))
        if pol in it.get('weather_rows', {}):
            wx_missing_train += it['weather_rows'][pol]['train_rows_weather_missing']
            wx_missing_fc += it['weather_rows'][pol]['forecast_rows_weather_missing']
check('hg_cache_638_items_identity_bound', items == 638 and not cbad, {'items': items, 'sources': dict(sources), 'bad': cbad[:10]})
check('hg_fit_history_windows', not hist_bad, hist_bad[:5])
R['hg_fit_accounting'] = {'hour_fits': hour_fits, 'solver_calls_main': solver_calls,
                          'train_rows_weather_missing_sum': wx_missing_train, 'forecast_rows_weather_missing_sum': wx_missing_fc}
print('hg fit accounting', R['hg_fit_accounting'])

# ------------------------------------------------------------------ ledger and caps
led = json.loads((ART / 'ledger/budget.json').read_text())
caps = {'component_attempts': 4000, 'main_component_attempts': 3000, 'primitive_fits': 480000, 'inner_fits': 384000,
        'final_fits': 96000, 'policy_days': 9000, 'reference_passes': 3, 'analysis_passes': 3,
        'machine_seconds': 120 * 3600, 'active_seconds': 80 * 3600, 'rss_bytes': 10 * 1024**3,
        'additional_disk_bytes': 40 * 1024**3, 'transfer_bytes': 160 * 1024**3, 'message_attempts': 3 * 123800, 'workers': 4}
check('ledger_caps_equal_section_15_5', led['caps'] == caps)
over = {k: (led['counts'].get(k, 0), c) for k, c in caps.items() if k in led['counts'] and led['counts'][k] > c}
check('ledger_counts_within_caps', not over, over)
check('ledger_peaks_within_caps', led['peaks']['rss_bytes'] <= caps['rss_bytes'] and led['peaks']['additional_disk_bytes'] <= caps['additional_disk_bytes'], led['peaks'])
check('no_running_jobs_in_ledger', not any(j.get('running') for j in led['jobs'] if not j['name'].startswith('critic-')))
check('all_jobs_blas_1', all(set(j['blas_environment'].values()) == {'1'} for j in led['jobs']))
check('workers_le_4', max(j['workers'] for j in led['jobs']) <= 4)
check('primitive_split', led['counts']['primitive_fits'] == led['counts']['inner_fits'] + led['counts']['final_fits'],
      {k: led['counts'][k] for k in ('primitive_fits', 'inner_fits', 'final_fits')})
R['ledger_counts'] = led['counts']
R['main_solver_calls_vs_ledger'] = {'main_solver_calls_from_cache_logs': solver_calls, 'ledger_primitive_fits_total': led['counts']['primitive_fits']}
ct = {c: int(subprocess.check_output(['git', 'show', '-s', '--format=%ct', c], cwd=ROOT)) for c in ('255ecfb', '30a958a', '2dac186')}
first_hg = min(j['start_epoch'] for j in led['jobs'] if j['name'] in ('hg-warmup', 'hg-evaluation', 'controls', 'controls-supplement', 'admission', 'comparison', 'score'))
check('protocol_commit_before_any_hg_fit', ct['255ecfb'] <= first_hg, {'protocol_commit': ct['255ecfb'], 'first_hg_job': first_hg})
comp = [j for j in led['jobs'] if j['name'] in ('comparison', 'score')]
check('admission_commit_before_outer_scoring', all(ct['30a958a'] <= j['start_epoch'] for j in comp), {'admission_commit': ct['30a958a'], 'comparison_start': [j['start_epoch'] for j in comp]})
proto_committed = subprocess.check_output(['git', 'show', '255ecfb:reports/weather-ablation/protocol.json'], cwd=ROOT) == (WA / 'protocol.json').read_bytes()
check('protocol_unchanged_since_freeze_commit', proto_committed)
lin_adm = json.loads(subprocess.check_output(['git', 'show', '30a958a:reports/weather-ablation/lineage.json'], cwd=ROOT))
check('admission_freeze_lineage_70_vectors_stage', len(lin_adm['admission']) == 70 and lin_adm['execution_stage'] == 'training_only_admission_complete_frozen_before_outer_scoring')
check('admission_vectors_preserved_in_final_lineage', lin_adm['admission'] == lin['admission'])
check('admission_dates_equal_cp16_manifest', sorted((a['fold'], a['day']) for a in lin['admission'] if a['arm'] == 'HG') == sorted(adm)
      and sorted((a['fold'], a['day']) for a in lin['admission'] if a['arm'] == 'H0') == sorted(adm))
pred_at_adm = subprocess.run(['git', 'cat-file', '-e', '30a958a:reports/weather-ablation/predictions.parquet'], cwd=ROOT, capture_output=True).returncode
check('no_predictions_committed_at_admission_freeze', pred_at_adm != 0)

json.dump({'results': R, 'failures': FAIL}, open(OUT / 'static.json', 'w'), indent=1, default=str)
print('FAILURES:', FAIL)
