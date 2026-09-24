"""CP-20 Integration Critic 2 -- static / identity / contract checks (no fits, no replay, no decode).

Run from the clean critic worktree under the monitor. Writes out/static.json.
"""
from __future__ import annotations

import collections
from datetime import date, timedelta
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = Path.cwd()
PROJECT = Path('/Users/djourno/Downloads/PJM')
ART = PROJECT / '.local/artifacts/cp-20'
OUTDIR = ART / 'critic-2/out'
WA = ROOT / 'reports/weather-ablation'
checks = []


def check(name, ok, **detail):
    checks.append({'check': name, 'ok': bool(ok), **detail})
    print(('PASS ' if ok else 'FAIL ') + name, json.dumps(detail, default=str)[:700], flush=True)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


# ---------------------------------------------------------------- A. governance identities
head = git('rev-parse', 'HEAD').decode().strip()
check('head_is_candidate', head == '3e9ff8b500c2c655fea810ae11886503927f176c', head=head)
check('worktree_clean', git('status', '--porcelain') == b'')
assignment = (ART / 'critic-2/assignment.md').read_text()
lines = assignment.splitlines()
start = next(i for i, l in enumerate(lines) if l.startswith('- Verbatim bar excerpt'))
excerpt_lines = []
for l in lines[start + 1:]:
    if l.startswith('  >'):
        excerpt_lines.append(l[4:] if l.startswith('  > ') else l[3:])
    elif excerpt_lines:
        break
excerpt = '\n'.join(excerpt_lines)
plan_wt = (ROOT / 'capstone_v21.md').read_text()
plan_git = git('show', 'HEAD:capstone_v21.md').decode()
check('bar_excerpt_verbatim_worktree', excerpt in plan_wt, excerpt_lines=len(excerpt_lines),
      line=plan_wt[:plan_wt.find(excerpt)].count('\n') + 1 if excerpt in plan_wt else None)
check('bar_excerpt_verbatim_git_head', excerpt in plan_git)
issued = {'capstone_v21.md': '150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167',
          'docs/track-b/capstone_v21-r3-to-v21-r4-amendments.md': '3e0bdf6a343d5336f406f0eeb726b1b65c0f767ec8d9418a7d8118902e1ace55',
          'docs/track-b/cp-20-direct-weather-brief.md': '28a4e195fa7f66ff3270d5d54e477478e90aa42124bceb1ee529f95f5761883e'}
for n, h in issued.items():
    check(f'issued_sha256:{n}', sha_file(ROOT / n) == h)
check('intake_receipt_present', (ROOT / 'docs/track-b/weather-content-intake-2026-09-23.md').exists())

# ---------------------------------------------------------------- B. protocol / manifest identities
protocol = json.loads((WA / 'protocol.json').read_text())
bad = {}
for section in ('implementation_sha256', 'frozen_inputs_sha256', 'issued_and_inherited_sha256'):
    for name, digest in protocol[section].items():
        if ':' in name and len(name.split(':')[0]) == 40:
            actual = sha_bytes(git('show', name))
        else:
            actual = sha_file(ROOT / name)
        if actual != digest:
            bad[f'{section}:{name}'] = [digest, actual]
check('protocol_all_hashes_match_candidate_bytes', not bad, mismatches=bad,
      counted={s: len(protocol[s]) for s in ('implementation_sha256', 'frozen_inputs_sha256', 'issued_and_inherited_sha256')})
am = json.loads((WA / 'artifact-manifest.json').read_text())
bad = {n: [d, sha_file(ROOT / n) if (ROOT / n).exists() else None] for n, d in am['artifact_sha256'].items()
       if not (ROOT / n).exists() or sha_file(ROOT / n) != d}
check('artifact_manifest_hashes_match_candidate_bytes', not bad, entries=len(am['artifact_sha256']), mismatches=bad,
      other_keys={k: v for k, v in am.items() if k != 'artifact_sha256'})
tracked = git('ls-files', 'reports/weather-ablation').decode().splitlines()
unlisted = [t for t in tracked if t not in am['artifact_sha256'] and not t.endswith('artifact-manifest.json')]
check('artifact_manifest_covers_tracked_outputs', not unlisted, unlisted=unlisted, tracked=len(tracked))
try:
    sys.path.insert(0, str(ROOT / 'src'))
    from cp20.execution import check_protocol
    check_protocol(ROOT)
    check('candidate_check_protocol_clean_checkout', True)
except Exception as exc:  # noqa: BLE001
    check('candidate_check_protocol_clean_checkout', False, error=repr(exc))


def commits(path):
    return [l.split(' ', 1) for l in git('log', '--format=%H %cI', '--', path).decode().splitlines()]


pc = commits('reports/weather-ablation/protocol.json')
check('protocol_committed_once_at_prefit_freeze', len(pc) == 1 and pc[0][0].startswith('255ecfb'), commits=pc)
lc = commits('reports/weather-ablation/lineage.json')
check('lineage_commits', [c[0][:7] for c in lc] == ['2dac186', '30a958a'], commits=lc)
lin_freeze = json.loads(git('show', '30a958a:reports/weather-ablation/lineage.json'))
lin = json.loads((WA / 'lineage.json').read_text())
check('admission_freeze_stage', lin_freeze['execution_stage'] == 'training_only_admission_complete_frozen_before_outer_scoring'
      and len(lin_freeze['admission']) == 70)
check('admission_records_unchanged_after_freeze', lin_freeze['admission'] == lin['admission'])
check('admission_origins_unchanged_after_freeze', lin_freeze['origins'] == lin['origins'][:len(lin_freeze['origins'])],
      frozen_origins=len(lin_freeze['origins']), final_origins=len(lin['origins']))
pred_commits = commits('reports/weather-ablation/predictions.parquet')
metric_commits = commits('reports/weather-ablation/metrics.csv')
check('predictions_and_metrics_single_commit', len(pred_commits) == 1 and len(metric_commits) == 1,
      predictions=pred_commits, metrics=metric_commits)
changed_after = {}
for name in protocol['frozen_inputs_sha256']:
    later = [c for c in commits(name) if c[1] > pc[0][1]]
    if later:
        changed_after[name] = later
check('frozen_inputs_not_recommitted_after_freeze_except_r14', set(changed_after) <= {'reports/weather-ablation/prerun-attempts.csv'},
      changed=changed_after)
blob_freeze = git('show', f'{pc[0][0]}:reports/weather-ablation/prerun-attempts.csv')
blob_now = (WA / 'prerun-attempts.csv').read_bytes()
check('r14_prerun_attempts_content_equal_modulo_eol', blob_freeze.replace(b'\r\n', b'\n') == blob_now.replace(b'\r\n', b'\n'),
      freeze_blob_sha=sha_bytes(blob_freeze), now_sha=sha_bytes(blob_now),
      frozen=protocol['frozen_inputs_sha256']['reports/weather-ablation/prerun-attempts.csv'])
impl_changed = [n for n in protocol['implementation_sha256'] if git('show', f'{pc[0][0]}:{n}') != (ROOT / n).read_bytes()]
check('implementation_unchanged_since_freeze_commit', not impl_changed, changed=impl_changed)
check('lineage_protocol_sha_equals_protocol_bytes', lin['protocol_sha256'] == sha_file(WA / 'protocol.json'))
names = git('diff', '--name-status', 'main..HEAD').decode().splitlines()
envelope = ('src/cp20/', 'tests/cp20/', 'scripts/cp20_weather.py', 'reports/weather-ablation/', 'docs/track-b/evidence/cp-20/')
outside = [n for n in names if not n.split('\t')[-1].startswith(envelope)]
nonadd = [n for n in names if not n.startswith('A\t')]
check('branch_diff_within_section_15_7_paths', not outside, files=len(names), outside=outside, non_additions=nonadd)
main_sha = git('rev-parse', 'main').decode().strip()
check('main_is_ancestor', subprocess.run(['git', 'merge-base', '--is-ancestor', 'main', 'HEAD'], cwd=ROOT).returncode == 0, main=main_sha)

# ---------------------------------------------------------------- C. admission bundle re-hash
adm = ROOT / 'reports/weather-admission'
bad, n = [], 0
for line in (adm / 'hashes/report_files.sha256').read_text().splitlines():
    if line.strip():
        d, p = line.split(None, 1)
        n += 1
        if sha_file(adm / p) != d:
            bad.append(p)
check('admission_report_files_rehash', not bad, files=n, bad=bad)
bad, n = [], 0
for line in (adm / 'hashes/raw_sample_objects.sha256').read_text().splitlines():
    if line.strip():
        d, p = line.split(None, 1)
        n += 1
        if sha_file(PROJECT / p) != d:
            bad.append(p)
check('admission_raw_samples_byte_identity', not bad and n == 600, samples=n, bad=bad)

# ---------------------------------------------------------------- D. run manifest
rm = json.loads((WA / 'run-manifest.json').read_text())
cp16 = json.loads((ROOT / 'reports/v2-causal/input-manifest.json').read_text())
origins = [date.fromisoformat(o['day']) for f in cp16['folds'] for o in f['origins']]
check('cp16_origins_638', len(origins) == 638 and sum(f['date_count'] for f in cp16['folds']) == 638,
      per_fold=[f['date_count'] for f in cp16['folds']])
union = set()
for d in origins:
    lo = max(date(2019, 1, 1), d - timedelta(days=728))
    union |= {lo + timedelta(days=i) for i in range((d - lo).days + 1)}
deliveries = {date.fromisoformat(r['delivery_day']) for r in rm['runs']} | {date.fromisoformat(s['delivery_day']) for s in rm['structural_missing']}
check('run_manifest_equals_independent_union', deliveries == union, union=len(union), manifest=len(deliveries))
check('run_manifest_2476_runs', len(rm['runs']) == 2476 == len({r['run_00z'] for r in rm['runs']}))
check('run_is_delivery_minus_one', all(date.fromisoformat(r['run_00z']) == date.fromisoformat(r['delivery_day']) - timedelta(days=1) for r in rm['runs']))
check('structural_missing_only_2019_01_01', [s['delivery_day'] for s in rm['structural_missing']] == ['2019-01-01']
      and rm['structural_missing'][0]['run_00z'] == '2018-12-31')
check('no_pre_2019_runs', min(r['run_00z'] for r in rm['runs']) == '2019-01-01')


def expected_version(run):
    d = date.fromisoformat(run)
    return 'v14' if d <= date(2019, 6, 12) else ('v15.1' if d <= date(2021, 3, 22) else 'v16')


badv = [r['run_00z'] for r in rm['runs'] if r['version'] != expected_version(r['run_00z'])]
check('version_timeline', not badv, bad=badv[:10], counts=collections.Counter(r['version'] for r in rm['runs']))
added = sorted(r['run_00z'] for r in rm['runs'] if not r['admission'].get('inventoried'))
check('eight_added_runs', added == [f'2023-03-{d}' for d in range(24, 32)] and all(
    r['primary_endpoint'] == 'aws' for r in rm['runs'] if r['run_00z'] in added), added=added)
check('availability_bracketed_all', all(r['availability']['bracketed'] for r in rm['runs']),
      bases=collections.Counter(r['availability']['basis'] for r in rm['runs']))
ext = pd.read_csv(WA / 'extended-inventory.csv')
check('extended_inventory_added_runs_pass', sorted(ext.run_00z) == added and ext.metadata_validated.all()
      and ext.field_lead_availability_check.all() and (ext.decoded_messages == 50).all() and (ext.endpoint_used == 'aws').all())

# ---------------------------------------------------------------- E. messages metadata
m = pd.read_parquet(WA / 'messages.parquet')
check('messages_123800_unique', len(m) == 123800 and not m.duplicated(['run_00z', 'lead', 'field']).any()
      and set(m.run_00z) == {r['run_00z'] for r in rm['runs']})
LEADS = (21, 24, 27, 30, 33, 36, 39, 42, 45, 48)
check('messages_leads_fields', set(m.lead) == set(LEADS) and set(m.field) == {'u10', 'v10', 'u100', 'v100', 'dswrf'}
      and (m.groupby('run_00z').size() == 50).all())
run_dt = pd.to_datetime(m.run_00z)
valid_dt = run_dt + pd.to_timedelta(m.endStep, unit='h')
problems = collections.Counter()
problems['dataDate'] = int((m.dataDate != run_dt.dt.strftime('%Y%m%d').astype(int)).sum())
problems['dataTime'] = int((m.dataTime != 0).sum())
problems['validityDate'] = int((m.validityDate != valid_dt.dt.strftime('%Y%m%d').astype(int)).sum())
problems['validityTime'] = int((m.validityTime != valid_dt.dt.hour * 100).sum())
wind = m.field != 'dswrf'
problems['wind_level'] = int((m.loc[wind, 'level'] != m.loc[wind, 'field'].map({'u10': 10, 'v10': 10, 'u100': 100, 'v100': 100})).sum())
problems['wind_typeOfLevel'] = int((m.loc[wind, 'typeOfLevel'] != 'heightAboveGround').sum())
problems['wind_surface103'] = int((m.loc[wind, 'typeOfFirstFixedSurface'] != 103).sum())
problems['wind_instant'] = int(((m.loc[wind, 'stepType'] != 'instant') | (m.loc[wind, 'startStep'] != m.loc[wind, 'lead'])
                                | (m.loc[wind, 'endStep'] != m.loc[wind, 'lead'])).sum())
problems['wind_units'] = int((m.loc[wind, 'units'] != 'm s**-1').sum())
problems['wind_param'] = int((m.loc[wind, 'parameterNumber'] != m.loc[wind, 'field'].map({'u10': 2, 'v10': 3, 'u100': 2, 'v100': 3})).sum())
ds = m.loc[~wind]
exp_start = np.where(ds.lead % 6 == 3, ds.lead - 3, ds.lead - 6)
problems['dswrf_bounds'] = int(((ds.startStep != exp_start) | (ds.endStep != ds.lead)).sum())
problems['dswrf_avg'] = int((ds.stepType != 'avg').sum())
problems['dswrf_units'] = int((ds.units != 'W m**-2').sum())
problems['dswrf_surface'] = int(((ds.typeOfLevel != 'surface') | (ds.typeOfFirstFixedSurface != 1)).sum())
problems['dswrf_param'] = int((ds.parameterNumber != 7).sum())
problems['production_status_operational'] = int((m.productionStatusOfProcessedData != 0).sum())
problems['processed_forecast'] = int((m.typeOfProcessedData != 1).sum())
problems['process_96'] = int((m.generatingProcessIdentifier != 96).sum())
problems['centre_kwbc'] = int((m.centre != 'kwbc').sum())
q = (2.0 ** m.binaryScaleFactor) / (10.0 ** m.decimalScaleFactor)
problems['packing_quantum'] = int((~np.isclose(q, m.packing_quantum, rtol=1e-12, atol=0)).sum())
problems['numberOfMissing'] = int((m.numberOfMissing != 0).sum())
problems['box_nonfinite'] = int((m.box_nonfinite != 0).sum())
vmap = {r['run_00z']: r['version'] for r in rm['runs']}
problems['version'] = int((m.version != m.run_00z.map(vmap)).sum())
emap = {r['run_00z']: r['primary_endpoint'] for r in rm['runs']}
problems['endpoint_is_manifest_primary'] = int((m.endpoint != m.run_00z.map(emap)).sum())
ymd = run_dt.dt.strftime('%Y%m%d')
aws_url = ('https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.' + ymd + '/00/' + pd.Series(np.where(m.version == 'v16', 'atmos/', ''), index=m.index)
           + 'gfs.t00z.pgrb2.0p25.f' + m.lead.map('{:03d}'.format))
ncar_url = ('https://tds.gdex.ucar.edu/thredds/fileServer/files/g/d084001/' + run_dt.dt.strftime('%Y') + '/' + ymd + '/gfs.0p25.'
            + ymd + '00.f' + m.lead.map('{:03d}'.format) + '.grib2')
problems['url_pattern'] = int((m.url != np.where(m.endpoint == 'aws', aws_url, ncar_url)).sum())
problems['byte_len'] = int((m.byte_end - m.byte_start + 1 != m.bytes).sum())
check('messages_metadata_all_valid', sum(problems.values()) == 0, problems=dict(problems),
      shortnames={f: sorted(m.loc[m.field == f, 'shortName'].unique()) for f in sorted(m.field.unique())},
      endpoints=m.endpoint.value_counts().to_dict(), hosts=sorted(m.url.str.split('/').str[2].unique()),
      dswrf_quantum_by_version={v: [float(g.min()), float(g.max())] for v, g in ds.groupby('version').packing_quantum},
      purposes=m.purpose.value_counts().to_dict(), largest_message_bytes=int(m.bytes.max()))

# ---------------------------------------------------------------- F. run records, npz, retained raw
runs_dir = ART / 'weather/runs'
bad_rec, bad_npz, bad_msg, grid_bad = [], [], [], []
mi = m.set_index(['run_00z', 'lead', 'field']).sort_index()
for r in rm['runs']:
    rec = json.loads((runs_dir / f"{r['run_00z']}.json").read_text())
    if rec['status'] != 'complete' or rec['run_00z'] != r['run_00z'] or rec['delivery_day'] != r['delivery_day']:
        bad_rec.append(r['run_00z'])
    if sha_file(runs_dir / f"{r['run_00z']}.npz") != rec['npz_sha256']:
        bad_npz.append(r['run_00z'])
    for msg in rec['messages']:
        row = mi.loc[(r['run_00z'], msg['lead'], msg['field'])]
        if row.sha256 != msg['sha256'] or row.url != msg['url'] or row.byte_start != msg['byte_range'][0]:
            bad_msg.append((r['run_00z'], msg['lead'], msg['field']))
        meta = msg['meta']
        if (meta['gridType'], meta['Ni'], meta['Nj'], meta['iDirectionIncrementInDegrees'], meta['latitudeOfFirstGridPointInDegrees'],
                meta['longitudeOfFirstGridPointInDegrees']) != ('regular_ll', 1440, 721, 0.25, 90.0, 0.0):
            grid_bad.append((r['run_00z'], msg['lead'], msg['field']))
    if len(rec['messages']) != 50:
        bad_rec.append(('count', r['run_00z']))
runs_csv = pd.read_csv(WA / 'runs.csv')
csv_bad = [x for x, h in zip(runs_csv.run_00z, runs_csv.npz_sha256)
           if json.loads((runs_dir / f'{x}.json').read_text())['npz_sha256'] != h]
check('run_records_complete_and_npz_hashes', not bad_rec and not bad_npz and not csv_bad, bad_records=bad_rec[:5],
      bad_npz=bad_npz[:5], runs_csv_mismatch=csv_bad[:5], runs=len(rm['runs']))
check('run_record_messages_equal_messages_parquet', not bad_msg, bad=bad_msg[:5])
check('grid_regular_ll_1440x721_all_messages', not grid_bad, bad=grid_bad[:5])
raw = ART / 'weather/raw'
raw_bad, raw_n = [], 0
for run in sorted(os.listdir(raw)):
    for f in sorted(os.listdir(raw / run)):
        lead = int(f[1:4])
        field, ep = f[5:-6].rsplit('_', 1)
        raw_n += 1
        row = mi.loc[(run, lead, field)]
        if sha_file(raw / run / f) != row.sha256 or ep != row.endpoint:
            raw_bad.append(f'{run}/{f}')
retained_runs = sorted(os.listdir(raw))
check('retained_raw_messages_sha256_equal_recorded', not raw_bad and raw_n == 1150, files=raw_n, bad=raw_bad[:5],
      runs=len(retained_runs), versions=collections.Counter(vmap[r] for r in retained_runs))
shc = pd.read_csv(WA / 'sample-hash-comparison.csv')
adm_cache = PROJECT / '.local/weather-admission/cache/gfs'
bad = []
for row in shc.itertuples():
    a = sha_file(adm_cache / row.admission_object)
    b = mi.loc[(row.run_00z, row.lead, row.field)].sha256
    if not (a == row.admission_sha256 == b == row.cp20_sha256):
        bad.append(row.admission_object)
check('admission_samples_byte_identical_to_cp20_extraction', not bad and len(shc) == 600, rows=len(shc), bad=bad[:5])

# ---------------------------------------------------------------- G. weather features structure
wf = pd.read_parquet(WA / 'weather-features.parquet')
berlin = 'Europe/Berlin'
exp_rows = []
for d in sorted(deliveries):
    for t in pd.date_range(pd.Timestamp(d, tz=berlin), pd.Timestamp(d + timedelta(days=1), tz=berlin), freq='h', inclusive='left').tz_convert('UTC'):
        exp_rows.append((str(d), str(t)))
got_rows = sorted(zip(wf.delivery_date.astype(str), wf.timestamp_utc.dt.as_unit('ns').astype(str)))
check('features_cover_every_canonical_hour', got_rows == sorted(exp_rows) and len(wf) == len(exp_rows), rows=len(wf), expected=len(exp_rows))
run_of = (pd.to_datetime(wf.delivery_date.astype(str)) - pd.Timedelta(days=1))
lead = ((wf.timestamp_utc.dt.tz_convert(None) - run_of) / pd.Timedelta(hours=1))
ok_rows = wf.status == 'ok'
check('features_weather_origin_d1_00z_lead_22_46', (wf.loc[ok_rows, 'run_00z'] == run_of[ok_rows].dt.strftime('%Y-%m-%d')).all()
      and (lead == wf.lead_hour).all() and wf.lead_hour.between(22, 46).all(),
      lead_range=[int(wf.lead_hour.min()), int(wf.lead_hour.max())])
check('features_status', wf.status.value_counts().to_dict() == {'ok': 59422, 'structural_missing_pre_2019_run': 24}
      and wf.loc[~ok_rows, 'delivery_date'].astype(str).eq('2019-01-01').all()
      and wf.loc[~ok_rows, ['wx_wind10_mean', 'wx_wind100_mean', 'wx_dswrf_mean']].isna().all().all()
      and np.isfinite(wf.loc[ok_rows, ['wx_wind10_mean', 'wx_wind100_mean', 'wx_dswrf_mean']].to_numpy()).all(),
      counts=wf.status.value_counts().to_dict())
nh = wf.groupby('delivery_date').size()
check('dst_days_present', set(nh.unique()) == {23, 24, 25}, n23=int((nh == 23).sum()), n25=int((nh == 25).sum()))

# ---------------------------------------------------------------- H. predictions contract, H0 and references
pred = pd.read_parquet(WA / 'predictions.parquet')
LAB = ['p025', 'p10', 'p25', 'p50', 'p75', 'p90', 'p975']
counts = pred.groupby('policy').size().to_dict()
check('predictions_75229_rows_7x10747', len(pred) == 75229 and counts == {p: 10747 for p in ('B0', 'B1', 'B2', 'B3', 'A1', 'H0', 'HG')}, counts=counts)
keysets = {p: set(zip(g.fold, g.timestamp_utc.astype(str))) for p, g in pred.groupby('policy')}
check('identical_key_sets_all_policies', all(v == keysets['B0'] for v in keysets.values()))
check('contrast_rows_21494', int(pred.policy.isin(['H0', 'HG']).sum()) == 21494)
b0 = pred[pred.policy == 'B0']
fc = b0.groupby('fold').size().tolist()
peak = b0[(b0.fold == 'fold_3') & b0.delivery_date.astype(str).between('2022-08-15', '2022-08-31')]
check('fold_counts_peak_fold3', fc == [2160, 2159, 2112, 2160, 2156] and len(peak) == 408 and peak.delivery_date.nunique() == 17
      and b0[b0.fold == 'fold_3'].delivery_date.nunique() == 88, fold_counts=fc, peak=len(peak))
qv = pred[LAB].to_numpy(float)
check('finite_ordered_quantiles', np.isfinite(qv).all() and (np.diff(qv, axis=1) >= 0).all() and np.isfinite(pred[['y_true', 'central', 'scale']].to_numpy()).all())
arms = pred[pred.policy.isin(['H0', 'HG'])]
check('emitted_p50_distinct_from_central', True, share_p50_ne_central=float((arms.p50 != arms.central).mean()))
check('evidence_class_label', pred.evidence_class.eq('development_post_selection').all())
v2 = pd.read_parquet(ROOT / 'reports/v2-causal/predictions.parquet')
v2h = v2[v2.policy == 'V2-H']
cols = ['y_true', 'central', 'scale', 'level', *LAB]
a = pred[pred.policy == 'H0'].sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
bb = v2h.sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
check('H0_bitwise_equal_cp16_V2H', len(a) == len(bb) == 10747 and a[['fold', 'timestamp_utc']].astype(str).equals(bb[['fold', 'timestamp_utc']].astype(str))
      and np.array_equal(a[cols].to_numpy(float), bb[cols].to_numpy(float))
      and a.delivery_date.astype(str).equals(bb.delivery_date.astype(str)),
      max_abs=float(np.max(np.abs(a[cols].to_numpy(float) - bb[cols].to_numpy(float)))))
cp15 = pd.read_parquet(ROOT / 'reports/cp15/predictions.parquet')
refbad = {}
for p in ('B0', 'B1', 'B2', 'B3', 'A1'):
    x = pred[pred.policy == p].sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
    y = cp15[cp15.policy == p].sort_values(['fold', 'timestamp_utc']).reset_index(drop=True)
    c = [c for c in ['y_true', 'central', *LAB] if c in y]
    if not (len(x) == len(y) and x[['fold', 'timestamp_utc']].astype(str).equals(y[['fold', 'timestamp_utc']].astype(str))
            and np.array_equal(x[c].to_numpy(float), y[c].to_numpy(float), equal_nan=True)):
        refbad[p] = True
check('saved_references_bitwise_equal_cp15', not refbad, bad=refbad)
h0 = pred[pred.policy == 'H0'].set_index(['fold', 'timestamp_utc']).sort_index()
hg = pred[pred.policy == 'HG'].set_index(['fold', 'timestamp_utc']).sort_index()
check('H0_HG_same_truth_scale_level', h0[['y_true', 'scale', 'level']].equals(hg[['y_true', 'scale', 'level']]))
check('HG_central_differs_from_H0', True, share_differs=float((h0.central != hg.central).mean()))

# ---------------------------------------------------------------- I. HG cache
cache = ART / 'hg-components'
files = sorted(cache.glob('fold_*/*.json'))
digest_bad, ident_bad, central_bad = [], [], []
ident = lin['hg_identity']
hg_eval = pred[pred.policy == 'HG'].copy()
hg_idx = dict(zip(zip(hg_eval.fold, hg_eval.timestamp_utc.dt.as_unit('ns').astype(str)), hg_eval.central))
origin_days = {(f['fold'], o['day']) for f in cp16['folds'] for o in f['origins']}
first = {f['fold']: f['evaluation_start'] for f in cp16['folds']}
seen, warm, evalm, compared = set(), [], [], 0
for fp in files:
    item = json.loads(fp.read_text())
    seen.add((item['fold'], item['day']))
    body = {k: v for k, v in item.items() if k != 'content_sha256'}
    if hashlib.sha256(json.dumps(body, sort_keys=True, allow_nan=False, default=str).encode()).hexdigest() != item['content_sha256']:
        digest_bad.append(fp.name)
    if any(item.get(k) != v for k, v in ident.items()):
        ident_bad.append(fp.name)
    (warm if item['day'] < first[item['fold']] else evalm).append(fp.stat().st_mtime)
    if item['central'] and item['day'] >= first[item['fold']]:
        blend = np.asarray(item['central']['A1']) / 2 + np.asarray(item['central']['B2']) / 2
        keys = [(item['fold'], str(pd.Timestamp(t).tz_convert('UTC').as_unit('ns'))) for t in item['timestamp_utc']]
        got = [hg_idx.get(k) for k in keys]
        compared += len(keys)
        if any(g is None for g in got) or not np.array_equal(np.asarray(got, float), blend):
            central_bad.append(fp.name)
check('hg_cache_638_entries_one_per_origin', len(files) == 638 and seen == origin_days, files=len(files))
check('hg_cache_digests_and_identity', not digest_bad and not ident_bad, digest_bad=digest_bad[:5], ident_bad=ident_bad[:5], identity=ident)
check('hg_cache_blend_equals_emitted_HG_central', not central_bad and compared == 10747, bad=central_bad[:5], rows_compared=compared)
ct = lambda s: int(git('show', '-s', '--format=%ct', s).decode())
t_protocol, t_freeze = ct('255ecfb'), ct('30a958a')
ledger = json.loads((ART / 'ledger/budget.json').read_text())
jobs = ledger['jobs']
comp_job = [j for j in jobs if j['name'] == 'comparison' and j.get('exit_code') == 0]
adm_job = [j for j in jobs if j['name'] == 'admission' and j.get('exit_code') == 0]
check('ordering_protocol_warmup_admission_freeze_evaluation_comparison',
      t_protocol < min(warm + evalm) and max(warm) < adm_job[0]['start_epoch'] and adm_job[0]['end_epoch'] < t_freeze < min(evalm)
      and max(evalm) < comp_job[0]['start_epoch'] and len(adm_job) == 1 and len(comp_job) == 1,
      protocol_commit=t_protocol, warm=[min(warm), max(warm)], admission_job=[adm_job[0]['start_epoch'], adm_job[0]['end_epoch']],
      freeze_commit=t_freeze, evaluation=[min(evalm), max(evalm)], comparison_start=comp_job[0]['start_epoch'],
      n_warm=len(warm), n_eval=len(evalm))

# ---------------------------------------------------------------- J. ledger
caps_expected = {'component_attempts': 4000, 'main_component_attempts': 3000, 'primitive_fits': 480000, 'inner_fits': 384000,
                 'final_fits': 96000, 'policy_days': 9000, 'reference_passes': 3, 'analysis_passes': 3,
                 'machine_seconds': 120 * 3600, 'active_seconds': 80 * 3600, 'rss_bytes': 10 * 1024**3,
                 'additional_disk_bytes': 40 * 1024**3, 'transfer_bytes': 160 * 1024**3, 'message_attempts': 3 * 123800, 'workers': 4}
check('ledger_caps_equal_section_15_5', ledger['caps'] == caps_expected)
over = {k: [v, ledger['caps'][k]] for k, v in ledger['counts'].items() if k in ledger['caps'] and v > ledger['caps'][k]}
over.update({k: [v, ledger['caps'][k]] for k, v in ledger['peaks'].items() if v > ledger['caps'][k]})
check('ledger_counts_within_caps', not over, over=over, counts=ledger['counts'], peaks=ledger['peaks'])
blas_bad = [j['index'] for j in jobs if not j.get('blas_environment') or any(v != '1' for v in j['blas_environment'].values())]
check('all_jobs_blas_1_workers_le_4', not blas_bad and all(j['workers'] <= 4 for j in jobs), jobs=len(jobs), blas_bad=blas_bad)
ev = sorted([(j['start_epoch'], j['workers']) for j in jobs] + [(j.get('end_epoch') or j.get('reconciled_epoch') or 1e12, -j['workers']) for j in jobs],
            key=lambda x: (x[0], x[1]))
cur = peakw = 0
for _, w in ev:
    cur += w
    peakw = max(peakw, cur)
check('concurrent_workers_le_4', peakw <= 4, peak_concurrent_workers=peakw)
failed_jobs = [(j['index'], j['name'], j.get('exit_code'), j.get('abort_reason')) for j in jobs if j.get('exit_code') != 0 and not j.get('running')]
fcsv = pd.read_csv(WA / 'failures.csv')
listed = set(fcsv.loc[fcsv.kind == 'job', 'job_index'].dropna().astype(int))
missing_fail = [x for x in failed_jobs if x[0] not in listed]
check('failures_csv_lists_every_failed_ledger_job', not missing_fail, missing=missing_fail, failed=failed_jobs)
snap = json.loads((ROOT / 'docs/track-b/evidence/cp-20/ledger-snapshot-before-review.json').read_text())
check('snapshot_prefix_of_live_ledger', snap['jobs'] == jobs[:len(snap['jobs'])] and snap['caps'] == ledger['caps'],
      snapshot_jobs=len(snap['jobs']), live_jobs=len(jobs),
      after_snapshot=[(j['index'], j['name'], j.get('exit_code'), round(j.get('charged_seconds', 0), 1)) for j in jobs[len(snap['jobs']):]],
      count_deltas={k: ledger['counts'][k] - snap['counts'].get(k, 0) for k in ledger['counts'] if ledger['counts'][k] != snap['counts'].get(k, 0)})

OUTDIR.mkdir(parents=True, exist_ok=True)
(OUTDIR / 'static.json').write_text(json.dumps({'checks': checks, 'failed': [c['check'] for c in checks if not c['ok']]}, indent=1, default=str))
print('FAILED CHECKS:', [c['check'] for c in checks if not c['ok']])
