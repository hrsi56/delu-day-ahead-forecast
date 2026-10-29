"""CP-17b's committed records, checked from the repository alone (CI-safe): the re-frozen identity and manifest,
the package and what changed in it, item 6's parity against CP-17's records, item 1's partial days, item 2's shadow
run and B0 check, N1's control, the freeze-origin issuance, the reference bundle, the pinned copies, the schemas,
the report's tables, the red line, and the window's analysis tool still refused.
"""
from __future__ import annotations

from datetime import date, timedelta
import hashlib
import json
from pathlib import Path
import re

import pytest

from cp17 import issue, schema
from cp17.tools import freeze, refreeze

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / 'reports/cp17b'
EVIDENCE = ROOT / refreeze.EVIDENCE
CP17_REPORTS = ROOT / 'reports/cp17'
SHADOW_DAYS = [str(date(2026, 8, 24) + timedelta(days=i)) for i in range(14)]
#: Item 6: the package files CP-17b changed or added, against CP-17's frozen package.
CHANGED = {'cp17/issue.py': 'decision 13, N2, N3, N7', 'cp17/schema.py': 'N2 (the artifact v2 forms) and decision 13 '
           '(issued forecasts v2)', 'cp17/shadow.py': 'decision 14 (new: the shadow states)'}


def load(path: Path):
    return json.loads(path.read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope='module')
def manifest():
    return load(EVIDENCE / 'freeze-manifest.json')


def test_the_identity_holds_the_re_frozen_terms(manifest):
    identity = manifest['policy_identity']
    assert manifest['policy_identity_sha256'] == freeze.digest(identity) and identity['schema'] == 'cp17b-policy-identity-v1'
    assert identity['designated_policy'] == 'A1' and identity['registry']['version'] == 1
    assert identity['failure_policy']['gfs_unavailable'] == ['v2', 'B0']
    assert identity['failure_policy']['a1_failed'] == ['v4', 'v2', 'B0']
    assert len(identity['success_definition']['criteria']) == 5
    assert 'decision 13' in identity['success_definition']['criteria'][2] and 'N3' in identity['success_definition']['criteria'][3]
    assert identity['shadow']['policies'] == ['v4', 'v2', 'B0'] and identity['shadow']['decision'] == 14
    assert identity['retrain']['tau_eq_eur'] == 0.01 and 'F1' in identity['disclosures']
    assert identity['refit_schedule']['next'] == 'S_14 = 2027-01-06'
    runtime = identity['reference_runtime']                                           # N6
    assert (runtime['chromium'], runtime['webkit'], runtime['playwright']) == ('153.0.8010.12', '26.6', '1.63.0')
    assert runtime['machine_class'] and runtime['measured']['browsers'] == {'chromium': '153.0.8010.12', 'webkit': '26.6'}
    assert identity['supersedes']['policy_identity_sha256'] == 'b304d6479a8628a26014422c6682f1e6543bd0d9ff656ad34b2d87b163bc254e'
    assert identity['code']['pipeline_files_sha256'] == {'cp17/daily.py': sha(ROOT / 'src/cp17/daily.py')}    # N1
    assert len(identity['issuing_host']['pyodide']['files_sha256']) == 23
    assert identity['issuing_host']['node']['sha256'] == '1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040'


def test_the_package_is_the_checkouts_and_its_changes_are_declared(manifest):
    bundle = load(REPORTS / 'bundle-manifest.json')
    code = manifest['policy_identity']['code']
    assert code['files_sha256'] == bundle['files_sha256'] and code['package_sha256'] == bundle['package_sha256']
    assert all(sha(ROOT / 'src' / rel) == h for rel, h in bundle['files_sha256'].items())
    cp17 = load(CP17_REPORTS / 'bundle-manifest.json')
    changed = {k for k in set(bundle['files_sha256']) | set(cp17['files_sha256'])
               if bundle['files_sha256'].get(k) != cp17['files_sha256'].get(k)}
    assert changed == set(CHANGED)
    assert bundle['runner_files_sha256'] == cp17['runner_files_sha256']         # the runners are CP-17's
    assert 'cp17.shadow' in bundle['entry_modules'] and not any(k.startswith('cp17/tools/') for k in bundle['files_sha256'])


def test_native_parity_reruns_cp17s_record_bitwise():
    record = load(REPORTS / 'native-parity.json')
    assert record['status'] == 'PASS' and len(record['origins']) == 9 and record['all_equal_to_cp17']
    assert all(v == '1' for v in record['blas_threads'].values())


def test_issuing_host_parity_and_browser_identity_equal_cp17s_records():
    record = load(REPORTS / 'host-parity.json')
    assert record['all_equal_to_cp17'] and len(record['issuing_host_parity']) == 15
    assert record['package_sha256'] == load(REPORTS / 'bundle-manifest.json')['package_sha256']
    for row in record['issuing_host_parity']:
        assert row['blocked_non_local_requests'] == [] and row['executed_files_match_package'], row['stem']
    browsers = record['browser_runs']
    assert {b['browser'] for b in browsers} == {'chromium', 'webkit'} and all(record['browser_equal_to_cp17'].values())
    for b in browsers:
        assert not b['errors'] and b['blocked_non_local_requests'] == [] and b['executed_files_match_package']
        assert b['bitwise_equal_to_issuing_host'] and b['status_vs_issuing_host'] == 'identical bit for bit'


def test_item_1_partial_days():
    record = load(REPORTS / 'partial-days.json')
    spring = record['2026-03-30']
    assert spring['canonical_hours'] == 24 and set(spring['forecastable_hours'].values()) == {23}
    assert spring['cp26_keys'] == {'v4': 23, 'v2': 23, 'B0': 23} and not any(spring['cp26_error_eligible'].values())
    assert len(spring['missing_hours']['missing_hours']) == 1
    assert spring['host']['path'] == [['A1', 'ok']] and spring['same_path'] and spring['same_display']
    assert spring['host']['display'].startswith('successful daily fit (partial: 23 of 24 hours; missing ')
    assert spring['host']['artifact_verifies'] and spring['host']['artifact']['partial'] == spring['missing_hours']
    assert spring['native_vs_cp26']['A1']['pass'] and spring['native_vs_cp26']['A1']['quantiles_bitwise']
    assert spring['issued_vs_native']['selections_match']
    for p, s in spring['host']['shadows'].items():
        assert s['status'] == 'ok' and s['keys'] == 23 and s['intake'] == 'no intake: not a complete canonical issuance', p
    gap = record['2023-08-31']
    assert gap['canonical_hours'] == 24 and set(gap['forecastable_hours'].values()) == {0}
    assert gap['cp26_keys'] == {'v4': 0, 'v2': 0, 'B0': 0}
    assert gap['host']['display'] == gap['native']['display'] == f'failed issuance ({issue.NO_FORECASTABLE_HOUR})'
    assert gap['host']['artifact']['issued_policy'] is None and gap['host']['artifact_verifies'] and gap['same_path']
    assert gap['host']['process_seconds'] == {}                       # no fit was started
    assert all(s['intake'] == 'no intake: the fit failed' for s in gap['host']['shadows'].values())


def test_item_2_the_shadow_run():
    record = load(REPORTS / 'shadow-run.json')
    freeze_state = load(ROOT / 'docs/track-b/evidence/cp-17/freeze-manifest.json')['initial_state']['buffers_sha256']
    for mode in ('native', 'host'):
        run = record[mode]
        assert sorted(run['days']) == SHADOW_DAYS and run['start']['origin'] == '2026-08-24'
        assert run['start']['pending'] == {p: ['2026-08-23'] for p in ('v4', 'v2', 'B0')}
        assert run['summary']['all_registered'] and run['final']['origin'] == '2026-09-06'
        assert run['final']['cp17_recorded_sha256'] == {p: freeze_state[p] for p in ('v4', 'v2', 'B0')}
    native, host = record['native'], record['host']
    assert native['summary']['all_buffers_bitwise'] and native['summary']['all_parity_cp26']
    assert all(native['final']['equal_to_cp17_bitwise'].values())                 # bitwise natively
    assert host['summary']['max_abs_standardized'] < 1e-9                          # within rounding under the host
    assert host['final']['equal_to_cp17_bitwise']['B0']
    s = host['summary']
    assert s['all_within_ceiling'] and s['total_seconds_max'] <= 900 and s['all_artifacts_verify']
    assert s['all_executed_files_match_package'] and s['blocked_non_local_requests'] == []
    for day in host['days'].values():
        assert day['path'] == [['A1', 'ok']] and day['issued_policy'] == 'A1'
        assert {p: v['fitted_by'] for p, v in day['shadows'].items()} == dict.fromkeys(('v4', 'v2', 'B0'), 'shadow')


def test_item_2_b0s_buffer_from_prices_is_not_cp26s():
    record = load(REPORTS / 'b0-rebuild.json')
    assert record['common_days_bitwise_equal'] == record['common_days'] > 2000
    assert not record['equal'] and record['days_only_in_price_rebuild'] and record['origins_whose_28_day_buffer_differs'] > 0
    assert record['conclusion'].startswith('not equal: B0 is shadow-issued too')


def test_n1_the_killed_process_control():
    record = load(REPORTS / 'control.json')
    assert record['pass'] and record['path'][:2] == [['A1', 'failed'], ['v4', 'ok']] and record['issued_policy'] == 'v4'
    assert 'killed' in record['causes']['A1'] and record['artifact_verifies']
    assert record['stale_record']['planted'] and record['a1_folder'] not in record['stale_record']['planted']


def test_item_5_the_freeze_origin_issuance(manifest):
    record = load(REPORTS / 'issuance.json')
    art = load(EVIDENCE / 'artifact-2026-09-06.json')
    assert sha(EVIDENCE / 'artifact-2026-09-06.json') == record['artifact_file_sha256'] == manifest['freeze_origin']['artifact_file_sha256']
    assert art == record['artifact'] and issue.verify_artifact(art) == []
    assert schema.validate(art, schema.SCHEMAS['fitted_artifact']) == []
    assert art['lineage']['policy_identity_sha256'] == manifest['policy_identity_sha256']
    assert art['lineage']['code_sha256'] == manifest['policy_identity']['code']['package_sha256']
    assert art['issued_policy'] == 'A1' and art['display'] == 'successful daily fit' and art['partial'] is None
    assert art['issue_utc'] == '2026-09-05T09:00:00+00:00' and art['resources']['wall_seconds'] <= 900
    assert record['path'] == [['A1', 'ok']] and all(record['executed_files_match_package'].values())
    assert {p: s['status'] for p, s in record['shadows'].items()} == dict.fromkeys(('v4', 'v2', 'B0'), 'ok')
    assert record['total_seconds'] <= 900 and record['blocked_non_local_requests'] == []


def test_the_reference_bundle_holds_the_v2_kinds(manifest):
    record = load(REPORTS / 'reference-bundle.json')
    assert record['valid'] and record['validation_errors'] == [] and record['all_controls_refused']
    assert record['negative_controls']['partial_record_wrong']['refused']
    assert record['manifest']['artifact']['artifact_sha256'] == manifest['freeze_origin']['artifact_sha256']
    assert manifest['reference_bundle_manifest_sha256'] == record['manifest_sha256']


def test_the_schema_files_are_the_packages_and_the_pinned_copies_hold():
    for kind, value in schema.SCHEMAS.items():
        assert load(EVIDENCE / 'schemas' / f'{kind}.schema.json') == json.loads(json.dumps(value)), kind
    for name, (_, copy_name, expected) in refreeze.GOVERNANCE.items():
        assert sha(EVIDENCE / 'pinned' / copy_name) == expected, name
    assert (EVIDENCE / 'issued-brief.md').read_bytes() == (EVIDENCE / 'pinned' / 'cp-17b-brief-b9aeeee4.md').read_bytes()


DATE = re.compile(r'(?<![A-Za-z0-9/_.-])(20\d\d)-(\d\d)-(\d\d)')


def test_no_committed_record_holds_a_date_after_the_boundary():
    """The red line: no CP-17b record carries a delivery day, instant or value dated after 2026-09-06."""
    for path in sorted(REPORTS.glob('*')):
        # The compute ledger's dates are when its jobs ran (October 2026), not delivery days or data.
        if path.suffix not in ('.json', '.csv', '.jsonl') or path.name == 'compute-ledger.jsonl':
            continue
        late = sorted({m.group(0) for m in DATE.finditer(path.read_text()) if m.group(0) > '2026-09-06'})
        assert not late, f'{path.name}: {late[:5]}'


def test_report_tables_are_the_records():
    from cp17.tools import report17b
    text = (REPORTS / 'report.md').read_text()
    a, b = text.index(report17b.BEGIN), text.index(report17b.END) + len(report17b.END)
    assert text[a:b] == report17b.render(ROOT)


def test_the_report_lists_every_open_item():                                            # N5
    text = (REPORTS / 'report.md').read_text()
    section = text[text.index('## Open items'):]
    for item in ('F1', 'C1', 'C2', 'G1', 'G2', 'B0', 'r18', '4.7T', 'CP-18', 'τ_eq', '§19.2', 'unchecked', 'concurrently'):
        assert item in section, item


def test_nothing_was_retrieved():
    record = load(REPORTS / 'retrieval-manifest.json')
    assert record['data_bytes_retrieved'] == 0 and record['software_bytes_retrieved'] == 0 and record['remote_writes'] == 0


def test_the_windows_analysis_tool_stays_refused_by_the_guard():
    from cp17.tools import fresh_test as T
    from cp25.guard import BoundaryRefused
    # synthetic losses on development keys, labelled with the window's calendar dates, as CP-17's test does
    issued, outcomes = {'A1': {}, 'v5': {}, 'B0': {}}, {}
    for real, stand_in in zip(T.window_days(), T.window_days((date(2026, 6, 9), date(2026, 9, 6)))):
        keys = issue.canonical_hours(stand_in)
        outcomes.update(dict.fromkeys(keys, 60.0))
        for policy, error in (('A1', 1.0), ('v5', 2.0), ('B0', 3.0)):
            issued[policy][str(real)] = (keys, [[60 + error + d for d in (-3, -2, -1, 0, 1, 2, 3)] for _ in keys])
    with pytest.raises(BoundaryRefused):
        T.analyse(issued, outcomes)
