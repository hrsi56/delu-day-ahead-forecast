"""CP-17's committed records, checked from the repository alone (CI-safe): the freeze manifest and its
refusals, the parity and host tables, the issuances, the controls, the scoring check, the reference bundle,
the schema files, and the red line.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import re

import pytest

from cp17 import retrain, schema
from cp17.tools import freeze

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / 'reports/cp17'
EVIDENCE = ROOT / 'docs/track-b/evidence/cp-17'
ORIGINS = ('2025-10-26', '2026-03-29', '2026-08-31', '2026-09-01', '2026-09-02', '2026-09-03', '2026-09-04',
           '2026-09-05', '2026-09-06')


def load(path: Path):
    return json.loads(path.read_text())


@pytest.fixture(scope='module')
def manifest():
    return load(EVIDENCE / 'freeze-manifest.json')


#: Superseded at CP-17b, whose re-freeze changes these package files of CP-17's (and adds `cp17/shadow.py`, which
#: CP-17's manifest does not list). CP-17's freeze is superseded, not edited: its manifest must still verify against
#: this tree in everything else (`docs/track-b/evidence/cp-17b/freeze-record.md`).
CP17B_REFROZEN = ('src/cp17/issue.py', 'src/cp17/schema.py')


def test_freeze_manifest_verifies(manifest):
    assert sorted(freeze.verify(manifest, ROOT)) == [f'{p}: missing or altered' for p in CP17B_REFROZEN]
    identity = manifest['policy_identity']
    assert manifest['policy_identity_sha256'] == freeze.digest(identity)
    assert identity['designated_policy'] == 'A1' and identity['registry']['version'] == 1
    assert identity['failure_policy']['gfs_unavailable'] == ['v2', 'B0']
    assert identity['failure_policy']['a1_failed'] == ['v4', 'v2', 'B0']
    assert identity['retrain']['tau_eq_eur'] == 0.01 and identity['definitions']['tau_eur'] == 10.0
    assert identity['refit_schedule']['next'] == 'S_14 = 2027-01-06'
    assert identity['issuing_host']['node']['sha256'] == '1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040'
    assert len(identity['issuing_host']['pyodide']['files_sha256']) == 23


def test_freeze_manifest_refuses_alterations(manifest, tmp_path):
    """§9's positive controls: an altered artifact, a wrong version and a broken digest are refused."""
    wrong = copy.deepcopy(manifest)
    wrong['policy_identity']['registry']['version'] = 2
    assert freeze.verify(wrong, ROOT)
    altered = copy.deepcopy(manifest)
    name = next(iter(altered['policy_identity']['code']['files_sha256']))
    altered['policy_identity']['code']['files_sha256'][name] = '0' * 64
    assert any('altered' in p or 'digest' in p for p in freeze.verify(altered, ROOT))
    moved = copy.deepcopy(manifest)
    moved['freeze_origin']['artifact_sha256'] = 'f' * 64
    assert any('content digest' in p for p in freeze.verify(moved, ROOT))
    swapped = copy.deepcopy(manifest)
    swapped['freeze_origin']['artifact_file_sha256'] = '0' * 64
    assert any('freeze-origin artifact is missing or altered' in p for p in freeze.verify(swapped, ROOT))
    runner = copy.deepcopy(manifest)
    runner['policy_identity']['code']['runner_files_sha256']['cp17/host/node_run.mjs'] = '0' * 64
    assert 'src/cp17/host/node_run.mjs: missing or altered' in freeze.verify(runner, ROOT)
    # a file on disk that differs from its recorded hash
    fake = tmp_path / 'root'
    (fake / 'src').mkdir(parents=True)
    rel = 'cp17/retrain.py'
    (fake / 'src' / 'cp17').mkdir()
    (fake / 'src' / rel).write_text((ROOT / 'src' / rel).read_text() + '\n# changed\n')
    assert f'src/{rel}: missing or altered' in freeze.verify(manifest, fake)


def test_freeze_cites_the_package_and_the_artifact(manifest):
    bundle = load(REPORTS / 'bundle-manifest.json')
    assert manifest['policy_identity']['code']['files_sha256'] == bundle['files_sha256']
    artifact = load(EVIDENCE / 'artifact-2026-09-06.json')
    assert manifest['freeze_origin']['artifact_sha256'] == artifact['artifact_sha256']
    assert artifact['issued_policy'] == 'A1' and artifact['display'] == 'successful daily fit'
    assert artifact['lineage']['policy_identity_sha256'] == manifest['policy_identity_sha256']
    assert artifact['lineage']['code_sha256'] == bundle['package_sha256']
    assert artifact['issue_utc'] == '2026-09-05T09:00:00+00:00'
    from cp17.issue import verify_artifact
    assert verify_artifact(artifact) == []


def test_native_parity_is_bitwise_everywhere():
    record = load(REPORTS / 'native-parity.json')
    assert record['status'] == 'PASS' and sorted(record['origins']) == sorted(ORIGINS)
    for day, o in record['origins'].items():
        assert o['pass'], day
        assert set(o['checks']) == {'A1', 'v2', 'v4', 'v5', 'B0'}
        assert all(c['pass'] for c in o['checks'].values()), day
        assert o['checks']['A1']['quantiles_bitwise'] and o['checks']['v5']['policy']['quantiles_bitwise']
    assert all(v == '1' for v in record['blas_threads'].values())


def test_issuing_host_parity_and_browser_identity():
    record = load(REPORTS / 'host-parity.json')
    rows = {r['stem']: r for r in record['issuing_host_parity']}
    assert {f'A1-{d}' for d in ORIGINS} <= set(rows)
    for stem in ('v4-2026-09-06', 'v4-2026-03-29', 'v2-2026-09-06', 'v2-2026-03-29'):
        assert stem in rows
    for stem, r in rows.items():
        assert r['status'] in retrain.STATUS
        assert r['blocked_non_local_requests'] == [] and r['executed_files_match_package'], stem
        if r['selections_match'] and r['max_abs_eur'] <= retrain.TAU_EQ:
            assert r['status'] in retrain.STATUS[:2]
    browsers = record['browser_runs']
    a1 = [b for b in browsers if b['stem'] == 'A1-2026-09-06']
    assert {b['browser'] for b in a1} == {'chromium', 'webkit'}
    for b in browsers:
        assert not b['errors'] and b['blocked_non_local_requests'] == [] and b['executed_files_match_package']
    for b in a1:
        assert b['bitwise_equal_to_issuing_host'] and b['status_vs_issuing_host'] == 'identical bit for bit'


def test_issuances_walk_the_frozen_chains():
    record = load(REPORTS / 'issuance.json')
    assert record['2026-09-06-gfs1']['comparison']['host_path'] == [['A1', 'ok']]
    assert record['2026-09-06-gfs0']['comparison']['host_path'] == [['A1', 'skipped'], ['v2', 'ok']]
    assert record['2022-12-04-gfs1']['comparison']['host_path'] == [['A1', 'failed'], ['v4', 'ok']]
    for key, item in record.items():
        assert item['artifact_verifies'] and item['comparison']['same_path'], key
        assert item['host']['blocked_non_local_requests'] == [] and item['host_errors'] in ({}, {'A1': item['host_errors'].get('A1')})
        assert item['resources']['wall_seconds'] <= 900 and item['resources']['peak_bytes'] <= 4 * 1024 ** 3
        for attempt in item['attempts']:
            if attempt['status'] == 'ok':
                assert isinstance(attempt['resources'], dict) and attempt['resources']['wall_seconds'] <= 900
    assert record['2022-12-04-gfs1']['display'] == 'failed fit; fallback v4 issued'


def test_retrain_controls_and_scoring_check():
    controls = load(REPORTS / 'controls.json')
    assert controls['all_pass'] and controls['seed']['status'] == 'different'
    assert controls['training_window']['status'] == 'different' and controls['target_day_outcome']['unchanged']
    scoring = load(REPORTS / 'scoring-check.json')
    assert scoring['all_match'] and all(scoring['bitwise_equal'].values())


def test_reference_bundle_and_schemas():
    record = load(REPORTS / 'reference-bundle.json')
    assert record['valid'] and record['validation_errors'] == [] and record['all_controls_refused']
    assert schema.validate(record['manifest'], schema.SCHEMAS['manifest']) == []
    assert {f['kind'] for f in record['manifest']['files']} == set(schema.KINDS[1:])
    for kind, value in schema.SCHEMAS.items():
        # Superseded at CP-17b for the two kinds it re-froze (issued forecasts v2, the fitted artifact v2), whose
        # schema files are CP-17b's (tests/cp17b/test_records.py); the other five are unchanged.
        if kind in ('issued_forecasts', 'fitted_artifact'):
            continue
        assert load(EVIDENCE / 'schemas' / f'{kind}.schema.json') == json.loads(json.dumps(value)), kind


#: A date that stands as a value (a JSON string, an ISO instant, a CSV cell), not one inside a file or folder
#: name such as CP-26's `cold-rerun-2026-10-15`.
DATE = re.compile(r'(?<![A-Za-z0-9/_.-])(20\d\d)-(\d\d)-(\d\d)')


def test_no_committed_record_holds_a_date_after_the_boundary():
    """The red line: no CP-17 record carries a delivery day, instant or value dated after 2026-09-06."""
    for path in sorted(REPORTS.glob('*')):
        # The compute ledger's dates are when its jobs ran (October 2026), not delivery days or data.
        if path.suffix not in ('.json', '.csv', '.jsonl') or path.name == 'compute-ledger.jsonl':
            continue
        late = sorted({m.group(0) for m in DATE.finditer(path.read_text()) if m.group(0) > '2026-09-06'})
        assert not late, f'{path.name}: {late[:5]}'


def test_report_tables_are_the_records():
    from cp17.tools import report
    text = (REPORTS / 'report.md').read_text()
    a, b = text.index(report.BEGIN), text.index(report.END) + len(report.END)
    assert text[a:b] == report.render(ROOT)


def test_nothing_was_retrieved():
    record = load(REPORTS / 'retrieval-manifest.json')
    assert record['data_bytes_retrieved'] == 0 and record['software_bytes_retrieved'] == 0
    assert record['remote_writes'] == 0
