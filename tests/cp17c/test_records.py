"""CP-17c's committed records, checked from the repository alone (CI-safe): native parity, the browsers, R7's controls,
the freeze-origin reissue, the state route, the reference bundle, the runner's and the M3's measurement, the GitHub
minutes, the report's tables and the red line.
"""
from __future__ import annotations

import json
from pathlib import Path
import re

import pytest

from cp17 import hostcheck
from cp17.tools import refreeze17c

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / 'reports/cp17c'
EVIDENCE = ROOT / refreeze17c.EVIDENCE
CANARY = hostcheck.CANARY_QUANTILES_SHA256
#: Protocol and calendar dates the identity carries, which §24.2 permits: the CP-26 GFS ruling's date, and S_14.
CALENDAR = {'2026-10-19', '2027-01-06'}
#: A date, not one inside a path or name (CP-26's run folder `cold-rerun-2026-10-15` is not a data date).
DATE = re.compile(r'(?<![A-Za-z0-9/_.-])20\d\d-\d\d-\d\d')


def load(name: str):
    return json.loads((REPORTS / name).read_text())


def test_native_parity_equals_cp17bs_record_bitwise():
    record = load('native-parity.json')
    assert record['status'] == 'PASS' and len(record['origins']) == 9 and record['all_equal_to_cp17b']
    assert all(v == '1' for v in record['blas_threads'].values())
    assert all(set(o['checks']) == {'A1', 'v2', 'v4', 'v5', 'B0'} for o in record['origins'].values())


def test_the_browsers_reproduce_the_issuing_host_on_cp17cs_zip():
    record = load('browser.json')
    manifest = json.loads((EVIDENCE / 'freeze-manifest.json').read_text())
    assert record['package_zip_sha256'] == manifest['policy_identity']['code']['zip_sha256']
    assert {r['browser']: r['browser_version'] for r in record['runs']} == {'chromium': '153.0.8010.12', 'webkit': '26.6'}
    assert all(r['quantiles_sha256'] == CANARY and r['executed_files_match_package'] and not r['errors'] for r in record['runs'])
    assert all(record['equal_to_issuing_host'].values()) and all(record['equal_to_cp17b_browser_record'].values())
    assert record['playwright'] == '1.63.0'


def test_r7_is_listed_by_cp17c_and_raised_by_cp17b_on_the_same_bytes():
    record = load('r7-controls.json')
    cp17b = json.loads((ROOT / refreeze17c.CP17B_MANIFEST).read_text())['policy_identity']['code']['files_sha256']
    manifest = json.loads((EVIDENCE / 'freeze-manifest.json').read_text())['policy_identity']['code']['files_sha256']
    assert record['schema_py_sha256'] == {'cp17c': manifest['cp17/schema.py'], 'cp17b': cp17b['cp17/schema.py']}
    assert record['valid'] == {'cp17c': True, 'cp17b': True}
    assert record['negative_controls_equal'] and record['negative_controls_all_refused']
    assert record['all_listed_by_cp17c'] and record['all_raised_by_cp17b'] and len(record['malformed_day']) == 6
    assert all(v['cp17c']['listed'] for v in record['malformed_day'].values() if v['cp17c']['refused'] and
               not v['cp17c']['raised'] and v is not record['malformed_day']['days_not_a_list'])


def test_the_freeze_origin_reissue_differs_only_where_it_must():
    record = load('freeze-origin.json')
    assert record['fields_differing_from_cp17b'] == record['expected_differences']
    assert record['quantiles_sha256'] == CANARY and record['equal_to_canary'] and record['arrays_equal_to_cp17b']
    assert all(record['shadows_equal_to_cp17b_host_parity'].values())
    assert record['path'] == [['A1', 'ok']] and record['artifact_verifies'] and record['blocked_non_local_requests'] == []
    manifest = json.loads((EVIDENCE / 'freeze-manifest.json').read_text())
    assert manifest['freeze_origin']['artifact_sha256'] == record['artifact_sha256']


def test_the_state_route_is_cp17s_state_and_the_freeze_origin_payload():
    record = load('state-route.json')
    identity = json.loads((EVIDENCE / 'freeze-manifest.json').read_text())['policy_identity']
    state = record['freeze_origin_state']
    assert state['equal_to_cp17_recorded'] and state['equal_to_cp17b_native_shadow_run_final_state']
    assert state['file_sha256'] == identity['state_route']['freeze_origin_state']['file_sha256']
    assert state['buffers_sha256'] == identity['state_route']['freeze_origin_state']['buffers_sha256']
    assert all(state['pending'][p] == ['2026-09-05', '2026-09-06'] for p in ('v4', 'v2', 'B0'))
    assert record['canary_payload']['payload_sha256'] == identity['state_route']['canary_payload']['payload_sha256']
    assert record['k13']['file_sha256'] == identity['state_route']['k13']['file_sha256']


def test_the_reference_bundle_verifies_and_refuses_its_controls():
    record = load('reference-bundle.json')
    manifest = json.loads((EVIDENCE / 'freeze-manifest.json').read_text())
    assert record['valid'] and record['all_controls_refused'] and record['validation_errors'] == []
    assert record['manifest_sha256'] == manifest['reference_bundle_manifest_sha256']


def test_the_committed_identity_is_the_manifests():
    manifest = json.loads((EVIDENCE / 'freeze-manifest.json').read_text())
    assert load('policy-identity.json') == manifest['policy_identity']


def test_no_committed_record_holds_a_date_after_the_boundary():
    """The red line: no CP-17c record carries a delivery day, instant or value dated after 2026-09-06."""
    for path in sorted(REPORTS.glob('*')):
        # The compute ledger's and GitHub's dates are when jobs ran (October 2026), not delivery days or data.
        if path.suffix not in ('.json', '.csv', '.jsonl', '.md') or path.name in (
                'compute-ledger.jsonl', 'artifacts.json', 'scratch-repository.json', 'measurement.json', 'report.md'):
            continue
        late = sorted({m.group(0) for m in DATE.finditer(path.read_text()) if m.group(0) > '2026-09-06'} - CALENDAR)
        assert not late, f'{path.name}: {late[:5]}'


@pytest.mark.skipif(not (REPORTS / 'measurement.json').exists(), reason='the measurement is written after the runs')
def test_the_measurement_holds_on_both_machines():
    m = load('measurement.json')
    for machine in ('runner', 'local'):
        s = m[machine]['summary']
        assert s['parity_all_bit_identical'] and s['parity_origins'] == sorted(
            ['A1-2025-10-26', 'A1-2026-03-29'] + [f'A1-2026-0{d}' for d in
                                                  ('8-31', '9-01', '9-02', '9-03', '9-04', '9-05', '9-06')])
        assert s['fits'] == s['fits_bit_identical'] and s['all_payloads_equal'] and s['all_executed_files_match_package']
        assert s['all_within_ceilings'] and s['peak_bytes_max'] <= 4 * 1024 ** 3 and s['wall_seconds_max'] <= 900
        assert s['shadow_days'] == 14 and s['shadow_all_buffers_equal_reference'] and s['shadow_all_registered']
        assert s['shadow_all_issued_a1'] and s['shadow_all_artifacts_verify'] and s['shadow_all_fits_bit_identical']
        assert s['late_final_equals_reference_final'] and s['stitch_early_final_equals_late_start']
        assert all(s['gates_passed'].values()) and s['blocked_non_local_requests'] == []
        c = m[machine]['checks']
        assert c['gate_passed'] and c['pins_output'] == ['verified'] and c['all_forced_as_expected']
        assert {k: v['failed_at'] for k, v in c['forced'].items()} == {
            'pins': 'pins', 'binary': 'binary', 'machine': 'machine', 'canary': 'canary', 'canary_quantiles': 'canary'}
        assert not any(v['issuance_called'] for v in c['forced'].values())
        assert c['canary']['quantiles_sha256'] == CANARY
    runner = m['runner']['checks']['machine']
    assert runner['kind'] == 'GitHub-hosted runner' and runner['image_os'] == 'macos26' and runner['image_version']
    assert m['runner']['host']['checks']['cpython']['version'] == '3.13.15'
    assert m['minutes']['counted_total'] <= 1000
