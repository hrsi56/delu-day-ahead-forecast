"""CP-25's committed outputs (capstone v21-r13 §24.6 items 3-8), checked against their sources.

Fast checks read the committed files and the preserved snapshot; nothing is fetched. Rebuilding the
outputs is `scripts/cp25_data_gaps.py build all` (see reports/development-inputs/reproduce.md).
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cp25 import calendar as C
from cp25 import guard, runs, tiers as T

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'reports/development-inputs'


def _days(a, b):
    return [a + timedelta(days=i) for i in range((b - a).days + 1)]


# ---- missing-input rules: every citation points at its text ------------------------------------

@pytest.mark.parametrize('key', sorted(T.CITES))
def test_missing_input_citation_points_at_its_text(key):
    path, line, text = T.CITES[key]
    lines = (ROOT / path).read_text().split('\n')
    assert text in lines[line - 1], f'{path}:{line} no longer holds {text!r}'


def test_every_rule_cites_landed_code():
    for rule in T.MISSING_INPUT_RULES:
        for c in rule['cites']:
            path, line = c.rsplit(':', 1)
            assert (ROOT / path).exists() and int(line) > 0


# ---- the register -----------------------------------------------------------------------------

def test_register_categories_and_tiers():
    reg = json.loads((OUT / 'tier-register.json').read_text())
    tiers = {p['input'].split(' (')[0]: p['tier'] for p in reg['published_inputs']}
    assert tiers['target price'] == 2 and tiers['GFS 0.25° D-1 00 UTC weather'] == 2
    assert tiers['day-ahead load forecast'] == 3
    assert reg['tier3_inputs_of_b0_v1_v5'] and all('load forecast' in x for x in reg['tier3_inputs_of_b0_v1_v5'])
    labels = {h['label'].split(' ')[0] for h in reg['hindsight_labels']}
    assert labels == {'crisis_period', 'post_crisis'}
    assert any('A69' in r['input'] and 'refused' in r['status'] for r in reg['refused_or_unused'])
    for p in reg['published_inputs']:
        for e in p['evidence']:
            assert e in reg['documents']


def test_hindsight_label_lines():
    lines = (ROOT / 'src/delu_forecast/features.py').read_text().split('\n')
    assert 'crisis_period' in lines[155] and 'post_crisis' in lines[158]


# ---- the margin table -------------------------------------------------------------------------

def test_margin_rule_is_strictly_before():
    # Load forecast: deadline D-1 10:00 local, issue D-1 11:00 local: margin exactly 1 h, so +1 h is not strictly before.
    avail = T.availability(ROOT)
    row = avail[avail.delivery_date == date(2025, 1, 15)].iloc[0]
    assert (row.issue_utc - row.load_d0_available_utc) == timedelta(hours=1)
    assert (row.issue_utc - row.price_d1_available_utc) == timedelta(hours=22)
    summer = avail[avail.delivery_date == date(2025, 7, 15)].iloc[0]
    assert summer.issue_utc == datetime(2025, 7, 14, 9, 0, tzinfo=timezone.utc)


def test_margin_table_classes():
    table = pd.read_csv(OUT / 'margin-table.csv')
    cls = {(r.subgroup.split(':')[0].split(' (')[0], r.shift_hours): r['class'] for _, r in table.iterrows()}
    assert cls[('D-1 prices', 1)] == 'none' and cls[('D-1 prices', 6)] == 'none' and cls[('D-1 prices', 24)] == 'structural'
    assert cls[('D-2 and older prices', 24)] == 'none'
    gfs = table[table.group == 'gfs'].set_index('shift_hours')['class'].to_dict()
    assert gfs == {1: 'none', 6: 'partial', 24: 'structural'}
    load = table[table.subgroup.str.startswith('load forecast of D ')].set_index('shift_hours')['class'].to_dict()
    assert load == {1: 'structural', 6: 'structural', 24: 'structural'}


def test_margin_days_agree_with_table():
    table = pd.read_csv(OUT / 'margin-table.csv')
    days = pd.read_csv(OUT / 'margin-days.csv')
    for _, r in table.iterrows():
        sel = days[days.subgroup == r.subgroup]
        assert len(sel) == r.days_considered
        assert int(sel[f'affected_plus_{r.shift_hours}h'].sum()) == r.affected_days
        assert ((sel.margin_hours <= r.shift_hours) == sel[f'affected_plus_{r.shift_hours}h']).all()


# ---- the calendar -----------------------------------------------------------------------------

def test_calendar_covers_development_exactly():
    cal = pd.read_csv(OUT / 'eligibility-calendar.csv', parse_dates=['delivery_date'])
    assert list(cal.delivery_date.dt.date) == _days(date(2019, 1, 1), date(2026, 9, 6))
    assert cal.delivery_date.max().date() == guard.BOUNDARY


def test_calendar_exclusions_and_reasons():
    cal = pd.read_csv(OUT / 'eligibility-calendar.csv', parse_dates=['delivery_date'])
    out = cal[~cal.eligible]
    assert len(out) == 40
    early = out[out.delivery_date < '2019-02-01']
    assert list(early.delivery_date.dt.date) == _days(date(2019, 1, 1), date(2019, 1, 30))
    assert early.exclusion_reason.str.contains('720h_history').all()
    load = out[out.delivery_date >= '2019-02-01']
    assert load.exclusion_reason.str.startswith('load_forecast_absent').all()
    snap = pd.read_parquet(ROOT / 'data/snapshot.parquet', columns=['delivery_date', 'load_forecast_mw'])
    null_days = sorted(set(snap.delivery_date[snap.load_forecast_mw.isna()]))
    assert list(load.delivery_date.dt.date) == null_days
    assert (cal.eligible == (cal.landed_eligible_hours > 0)).all()
    assert cal.target_complete.all()
    # No weather column or model output enters the calendar.
    assert not any('wx' in c or 'weather' in c or 'score' in c for c in cal.columns)


def test_ineligible_hours_are_dst_adjacent_lags():
    rows = pd.read_csv(OUT / 'ineligible-hours.csv')
    assert (rows.local_hour == 2).all()
    assert rows.null_base_features.str.match(r'^price_lag_(24|48|168)h$').all()


# ---- the masks --------------------------------------------------------------------------------

def test_masks_subtract_the_four_sources():
    mask = pd.read_csv(OUT / 'record-masks.csv', parse_dates=['delivery_date'])
    parts = json.loads((ROOT / 'data/partitions.json').read_text())
    scored = set()
    for f in parts['development_folds']:
        scored |= set(_days(date.fromisoformat(f['evaluation']['start']), date.fromisoformat(f['evaluation']['end'])))
    scored |= set(_days(date(2026, 6, 9), date(2026, 9, 6)))
    m = json.loads((ROOT / 'reports/v2-causal/input-manifest.json').read_text())
    scored |= {date.fromisoformat(a['day']) for f in m['folds'] for a in f['admission']}
    for a, b in C.CP24_GATES.values():
        scored |= set(_days(date.fromisoformat(a), date.fromisoformat(b)))
    s = json.loads((ROOT / 'reports/ddnn2/rounds/round-1/search-ledger.json').read_text())
    for x in s['folds'].values():
        for a, b in x['batches']:
            scored |= set(_days(date.fromisoformat(a), date.fromisoformat(b)))
    got = set(mask.delivery_date.dt.date[mask.scored])
    assert got == scored
    assert set(mask.delivery_date.dt.date[mask.never_scored]) == set(_days(date(2019, 1, 1), date(2026, 9, 6))) - scored


def test_cp24_gate_windows_match_the_gate_record():
    gate = json.loads((ROOT / 'reports/ddnn2/rounds/round-1/gate.json').read_text())
    days = set(gate['excluded_training_days']['ddnn2_by_day'])
    expected = {d.isoformat() for a, b in C.CP24_GATES.values() for d in _days(date.fromisoformat(a), date.fromisoformat(b))}
    assert days == expected and len(expected) == 280


def test_old_fold_mask_and_fold_1_in_warm_up():
    mask = pd.read_csv(OUT / 'record-masks.csv', parse_dates=['delivery_date'])
    old = mask[mask.old_fold_2_5]
    assert len(old) == 360
    f1 = mask[mask.fold_1_evaluation].delivery_date
    assert f1.min() == pd.Timestamp('2020-07-01') and f1.max() == pd.Timestamp('2020-09-28')
    assert f1.min() >= pd.Timestamp('2020-01-01') and f1.max() <= pd.Timestamp('2020-12-28')


def test_fit_or_calibrate_days_are_listed_not_subtracted():
    mask = pd.read_csv(OUT / 'record-masks.csv', parse_dates=['delivery_date'])
    cal = mask[mask.fit_or_calibrate_sources.fillna('').str.contains('v1_final_calibration')]
    assert len(cal) == 60 and cal.delivery_date.min() == pd.Timestamp('2026-04-09')
    assert not mask.loc[mask.fit_or_calibrate_only, 'scored'].any()


# ---- the weather features -----------------------------------------------------------------------

def test_gap_features_schema_and_coverage():
    cp20 = pd.read_parquet(ROOT / 'reports/weather-ablation/weather-features.parquet')
    gaps = pd.read_parquet(OUT / 'weather-features-gaps.parquet')
    assert list(gaps.columns) == list(cp20.columns)
    assert dict(gaps.dtypes) == dict(cp20.dtypes)
    want = set(_days(date(2022, 9, 29), date(2023, 3, 24))) | set(_days(date(2026, 4, 8), date(2026, 9, 6)))
    assert set(gaps.delivery_date) == want and len(want) == 329
    assert not set(gaps.delivery_date) & set(cp20.delivery_date)
    union = pd.concat([cp20, gaps])
    assert set(union.delivery_date) == set(_days(date(2019, 1, 1), date(2026, 9, 6)))
    assert union.timestamp_utc.is_unique
    for d, g in gaps.groupby('delivery_date'):
        assert len(g) == len(C.expected_hours(d))
    assert (gaps.status == 'ok').all() and gaps.lead_hour.between(22, 46).all()
    assert (gaps.run_00z == (pd.to_datetime(gaps.delivery_date) - pd.Timedelta(days=1)).dt.strftime('%Y-%m-%d')).all()
    assert gaps.timestamp_utc.max() <= pd.Timestamp('2026-09-06 21:00', tz='UTC')


def test_targeted_checks_and_messages():
    checks = pd.read_csv(OUT / 'gfs-targeted-checks.csv')
    assert len(checks) == 329 and checks.field_lead_availability_check.all() and checks.metadata_validated.all()
    assert (checks.aws_leads_listed == 10).all() and (checks.aws_idx_listed == 10).all()
    assert (~checks.inventoried_by_admission).all()
    msgs = pd.read_parquet(OUT / 'gfs-messages.parquet')
    assert len(msgs) == 329 * 50 and msgs.sha256.str.fullmatch('[0-9a-f]{64}').all()
    assert (msgs.dataTime == 0).all() and set(msgs.lead) == set(runs.LEADS)
    assert (msgs.productionStatusOfProcessedData == 0).all() and (msgs.typeOfProcessedData == 1).all()
    assert pd.to_datetime(msgs.run_00z).max() == pd.Timestamp('2026-09-05')


def test_retrieval_log_stays_inside_the_guard():
    log = pd.read_csv(OUT / 'retrieval-log.csv')
    assert set(log.endpoint) <= {'aws', 'ncar'}
    objects = log[log.url != 'https://noaa-gfs-bdp-pds.s3.amazonaws.com/']
    for url in objects.url.unique():
        guard.admit_url(url)
    assert not log.url.str.contains(r'\?').any()


def test_conversion_identity_record():
    rec = json.loads((OUT / 'conversion-identity.json').read_text())
    assert rec['values_bitwise_identical'] and rec['keys_identical'] and rec['status_identical'] and rec['runs'] == 2476
    assert rec['committed_sha256'] == hashlib.sha256((ROOT / 'reports/weather-ablation/weather-features.parquet').read_bytes()).hexdigest()


def test_partition_spec_is_a_new_file_and_the_old_is_unchanged():
    spec = json.loads((OUT / 'partitions-development.json').read_text())
    assert spec['development'] == {**spec['development'], 'first_delivery_day': '2019-01-01', 'last_delivery_day': '2026-09-06', 'days': 2806}
    assert hashlib.sha256((ROOT / 'data/partitions.json').read_bytes()).hexdigest() == \
        '6bee065368b721ae8092ba287e04bb6dda0d4bde80909e72380503ba61e0b090' == spec['historical_partitions']['sha256']
    assert hashlib.sha256((ROOT / 'data/snapshot.parquet').read_bytes()).hexdigest() == \
        '7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00' == spec['snapshot']['sha256']
    assert spec['eligibility_calendar']['sha256'] == hashlib.sha256((OUT / 'eligibility-calendar.csv').read_bytes()).hexdigest()
    assert spec['record_masks']['sha256'] == hashlib.sha256((OUT / 'record-masks.csv').read_bytes()).hexdigest()


def test_manifest_hashes_every_output():
    m = json.loads((OUT / 'manifest.json').read_text())
    files = sorted(p for p in OUT.iterdir() if p.is_file() and p.name != 'manifest.json')
    assert set(m['outputs_sha256']) == {f'reports/development-inputs/{p.name}' for p in files}
    for name, digest in m['outputs_sha256'].items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    for name, digest in {**m['implementation_sha256'], **m['reused_landed_code_sha256']}.items():
        assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == digest, name


def test_no_raw_grib_or_grid_is_committed():
    for p in ROOT.joinpath('reports/development-inputs').rglob('*'):
        assert p.suffix not in ('.grib2', '.npz', '.grb', '.grib'), p
        if p.is_file():
            assert p.read_bytes()[:4] != b'GRIB', p


def test_listing_evidence_and_attempts():
    lines = [json.loads(l) for l in (OUT / 'gfs-aws-listing.jsonl').read_text().splitlines()]
    assert len(lines) == 329 and all(e['aws_complete'] for e in lines)
    checks = pd.read_csv(OUT / 'gfs-targeted-checks.csv').set_index('run_00z')
    for e in lines:
        stamps = [v[k]['last_modified'] for v in e['leads'].values() for k in ('object', 'index')]
        assert pd.Timestamp(max(stamps)) == pd.Timestamp(checks.at[e['run'], 'aws_last_modified_max_utc'])
    late = checks[~checks.per_run_strictly_before_issue.astype(bool)].index.tolist()
    assert late == ['2022-11-30', '2023-01-20']
    att = json.loads((OUT / 'gfs-attempt-outcomes.json').read_text())
    assert att['outcome_counts'] == {'integrity_failure': 20, 'success': 16450}
    assert {(r['run'], r['lead']) for r in att['not_success']} == {('2022-11-30', l) for l in (27, 33, 36, 45)}
