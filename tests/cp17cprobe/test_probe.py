"""CP-17c-probe: the runner harness, the shipped inputs, the scratch workflow, and the committed measurement.

CI-safe tests check the repository alone. Tests that need the reference runs (CP-17b's `.local/artifacts`) or the
downloaded runner results skip with that reason where those are absent, as on CI.
"""
from __future__ import annotations

from datetime import date
import hashlib
import json
import math
import os
from pathlib import Path
import re

import pytest
import yaml

from cp17cprobe import compare, run

ROOT = Path(__file__).resolve().parents[2]
REPORTS = ROOT / 'reports/cp17c-probe'
WORKFLOW = ROOT / 'src/cp17cprobe/probe.yml'
FAKE_NODE = Path(__file__).resolve().parent / 'fake_node.py'
BOUNDARY = date(2026, 9, 6)


def load(path: Path):
    return json.loads(Path(path).read_text())


def sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def project() -> Path:
    from cp17.tools import ledger
    return ledger.project_root(ROOT)


def need_reference():
    if not (project() / '.local/artifacts/cp-17b/runs/shadow-host/payloads').exists():
        pytest.skip("the reference runs are local material (CP-17b's .local/artifacts), absent on CI")


@pytest.fixture(scope='module')
def inputs():
    return load(REPORTS / 'inputs.json')


# --- the scratch workflow -----------------------------------------------------------------------------------------

def test_workflow_uses_only_githubs_own_actions_pinned_by_commit():
    text = WORKFLOW.read_text()
    uses = re.findall(r'uses:\s*(\S+)', text)
    assert uses
    for item in uses:
        assert re.fullmatch(r'actions/[a-z-]+@[0-9a-f]{40}', item), item


def test_workflow_token_reads_and_no_secret_is_used():
    value = yaml.safe_load(WORKFLOW.read_text())
    assert value['permissions'] == {'contents': 'read'}
    assert 'permissions' not in value['jobs']['probe']
    assert 'secrets.' not in WORKFLOW.read_text()
    checkout = next(s for s in value['jobs']['probe']['steps'] if s.get('uses', '').startswith('actions/checkout@'))
    assert checkout['with']['persist-credentials'] is False


def test_default_jobs_are_standard_runners_bounded_under_the_minute_ceiling():
    value = yaml.safe_load(WORKFLOW.read_text())
    default = json.loads(value[True]['workflow_dispatch']['inputs']['jobs']['default'])['include']
    assert {(j['runner'], j['kind']) for j in default} == {(r, k) for r in ('ubuntu-24.04', 'macos-26')
                                                           for k in ('parity', 'shadow-late', 'shadow-early')}
    assert all(j['step_minutes'] < j['job_minutes'] for j in default)
    worst = sum(j['job_minutes'] * (10 if j['runner'].startswith('macos') else 1) for j in default)
    assert worst <= 1500, worst


def test_workflow_runs_the_chain_on_the_shipped_inputs_after_checking_them():
    steps = [s.get('name', '') for s in yaml.safe_load(WORKFLOW.read_text())['jobs']['probe']['steps']]
    order = [i for i, name in enumerate(steps) if name.startswith(('Verify the shipped inputs', 'Node.js', 'The host',
                                                                    'The frozen chain'))]
    assert len(order) == 4 and order == sorted(order)


# --- the shipped inputs -------------------------------------------------------------------------------------------

def test_committed_states_are_the_shipped_ones(inputs):
    for name in ('start-2026-08-24.json', 'start-2026-08-30.json', 'truth.json'):
        assert inputs['files'][f'states/{name}']['sha256'] == sha(REPORTS / 'states' / name)
    assert inputs['start']['2026-08-24']['state_file_sha256'] == sha(REPORTS / 'states/start-2026-08-24.json')
    assert inputs['start']['2026-08-30']['state_file_sha256'] == sha(REPORTS / 'states/start-2026-08-30.json')
    assert len(inputs['dry_replay_buffers_equal_reference']) == 14
    assert all(inputs['dry_replay_buffers_equal_reference'].values())


def test_inputs_bind_the_references_to_the_committed_cp17b_reports(inputs):
    from cp17cprobe.inputs import REPORTS as CITED
    for kind, rel in CITED.items():
        assert inputs['references']['reports_sha256'][kind] == sha(ROOT / rel), rel
    runs = inputs['references']['runs']
    assert len(runs['parity']) == 15 and len(runs['f1']) == 4 and len(runs['shadow']) == 56


def test_inputs_ship_the_frozen_files_by_their_frozen_hashes(inputs):
    freeze = load(ROOT / 'docs/track-b/evidence/cp-17b/freeze-manifest.json')['policy_identity']
    code = freeze['code']
    for rel, expected in code['files_sha256'].items():
        assert inputs['files'][f'src/{rel}']['sha256'] == expected
    assert inputs['files']['src/cp17/daily.py']['sha256'] == code['pipeline_files_sha256']['cp17/daily.py']
    assert inputs['files']['src/cp17/host/node_run.mjs']['sha256'] == code['runner_files_sha256']['cp17/host/node_run.mjs']
    assert inputs['files']['bundle/src.zip']['sha256'] == code['zip_sha256']
    for name, expected in freeze['issuing_host']['pyodide']['files_sha256'].items():
        assert inputs['files'][f'pyodide/{name}']['sha256'] == expected
    assert sum(1 for k in inputs['files'] if k.startswith('pyodide/')) == 23


def test_the_committed_harness_and_workflow_are_the_ones_that_ran(inputs):
    """The scratch repository received these files; a later edit here would leave its runs unexplained."""
    for rel in ('src/cp17cprobe/__init__.py', 'src/cp17cprobe/run.py'):
        assert inputs['files'][rel]['sha256'] == sha(ROOT / rel), rel
    assert inputs['files']['.github/workflows/probe.yml']['sha256'] == sha(WORKFLOW)
    assert inputs['files']['pyproject.toml']['sha256'] == sha(ROOT / 'pyproject.toml')
    assert inputs['files']['uv.lock']['sha256'] == sha(ROOT / 'uv.lock')


def test_no_shipped_input_reaches_past_the_development_boundary(inputs):
    for rel in inputs['files']:
        for found in re.findall(r'(\d{4}-\d{2}-\d{2})\.(?:json|npz)$', rel):
            assert date.fromisoformat(found) <= BOUNDARY, rel
    truth = load(REPORTS / 'states/truth.json')
    assert truth['last_day'] == '2026-09-04' and len(truth['keys']) == len(truth['y'])
    for name in ('start-2026-08-24.json', 'start-2026-08-30.json'):
        days = re.findall(r'"(\d{4}-\d{2}-\d{2})"', (REPORTS / 'states' / name).read_text())
        assert days and max(date.fromisoformat(d) for d in days) <= BOUNDARY


def test_inputs_fit_a_github_repository(inputs):
    assert inputs['largest_file_bytes'] < 50 * 1024 ** 2
    for path in REPORTS.rglob('*'):
        if path.is_file():
            assert path.stat().st_size < 50 * 1024 ** 2, path


# --- the harness, unit by unit ------------------------------------------------------------------------------------

def test_truth_is_nan_unless_every_key_is_present(tmp_path):
    path = tmp_path / 'truth.json'
    path.write_text(json.dumps({'keys': ['2026-08-30T00:00:00+00:00', '2026-08-30T01:00:00+00:00'], 'y': [10.5, -3.25]}))
    at = run.truth_from(path)
    assert at(['2026-08-30T01:00:00+00:00']).tolist() == [-3.25]
    got = at(['2026-08-30T00:00:00+00:00', '2026-08-30T02:00:00+00:00'])
    assert len(got) == 2 and all(math.isnan(v) for v in got)


def test_verify_finds_an_altered_or_missing_input(tmp_path):
    (tmp_path / 'a').write_bytes(b'one')
    (tmp_path / 'b').write_bytes(b'two')
    files = {'a': hashlib.sha256(b'one').hexdigest(), 'b': hashlib.sha256(b'two').hexdigest()}
    assert run.verify_inputs(tmp_path, files)['verified']
    (tmp_path / 'b').write_bytes(b'tw0')
    files['c'] = files['a']
    assert run.verify_inputs(tmp_path, files)['problems'] == ['b', 'c']


def test_buffer_hash_is_cp17bs():
    from cp17.tools import states
    buffer = [{'day': '2026-08-01', 'errors': [0.1, -2.5, 1e-14]}]
    assert run.buffer_sha256(buffer) == states.buffer_sha256(buffer)


def test_counted_minutes_round_each_job_up_and_count_macos_tenfold():
    artifacts = {'runs': {'1': {'jobs': [], 'billable': {
        'UBUNTU': {'job_runs': [{'job_id': 1, 'duration_ms': 60_001}, {'job_id': 2, 'duration_ms': 120_000}]},
        'MACOS': {'job_runs': [{'job_id': 3, 'duration_ms': 30_000}]}}}}}
    value = compare.counted_minutes(artifacts)
    assert value['runs']['1']['counted_from_billable'] == 2 + 2 + 10
    assert value['counted_total'] == 14


# --- the harness, end to end on the reference's own records (local) ------------------------------------------------

def _stand_in(tmp_path, inputs, kind) -> Path:
    path = tmp_path / f'{kind}-records.json'
    path.write_text(json.dumps({s: str(project() / r['record']) for s, r in inputs['references']['runs'][kind].items()}))
    return path


def _blas(monkeypatch):
    for name in run.BLAS:
        monkeypatch.setenv(name, '1')


def test_shadow_harness_carries_the_reference_states_with_a_stand_in_node(tmp_path, monkeypatch, inputs):
    """With the reference's own fits handed back, the runner's states must be the reference's at every origin,
    equal to the buffers the shipped payloads carry, and every shadow registered."""
    need_reference()
    _blas(monkeypatch)
    monkeypatch.setenv('CP17C_FAKE_RECORDS', str(_stand_in(tmp_path, inputs, 'shadow')))
    payloads = project() / '.local/artifacts/cp-17b/runs/shadow-host/payloads'
    out = tmp_path / 'late'
    code = run.main(['shadow', '--node', str(FAKE_NODE), '--pyodide', str(tmp_path), '--zip', str(REPORTS / 'inputs.json'),
                     '--payloads', str(payloads), '--first', '2026-08-30', '--last', '2026-09-02',
                     '--state', str(REPORTS / 'states/start-2026-08-30.json'), '--truth', str(REPORTS / 'states/truth.json'),
                     '--out', str(out)])
    assert code == 0
    record = load(out / 'shadow.json')
    for day, d in record['days'].items():
        assert d['buffers_sha256'] == inputs['references']['shadow_buffers_sha256'][day]
        assert all(d['buffers_equal_payload'].values())
        assert set(d['intake'].values()) == {'registered'} and d['issued_policy'] == 'A1'
        for policy, row in d['runs'].items():
            assert row['quantiles_sha256'] == inputs['references']['runs']['shadow'][f'{policy}-{day}']['quantiles_sha256']


def test_parity_harness_judges_each_attempt_as_the_chain_does(tmp_path, monkeypatch, inputs):
    need_reference()
    _blas(monkeypatch)
    monkeypatch.setenv('CP17C_FAKE_RECORDS', str(_stand_in(tmp_path, inputs, 'parity')))
    payloads = project() / '.local/artifacts/cp-17b/runs/native-parity/payloads'
    code = run.main(['parity', '--node', str(FAKE_NODE), '--pyodide', str(tmp_path), '--zip', str(REPORTS / 'inputs.json'),
                     '--payloads', str(payloads), '--stems', 'A1-2025-10-26,B0-2026-09-06', '--out', str(tmp_path / 'p')])
    assert code == 0
    rows = load(tmp_path / 'p/parity.json')['stems']
    assert [r['attempt']['status'] for r in rows] == ['ok', 'ok']
    assert all(r['attempt']['resources']['limits'] == {'wall_seconds': 900, 'peak_bytes': 4 * 1024 ** 3} for r in rows)
    assert [r['quantiles_sha256'] for r in rows] == [inputs['references']['runs']['parity'][s]['quantiles_sha256']
                                                     for s in ('A1-2025-10-26', 'B0-2026-09-06')]


def test_compare_finds_a_one_ulp_difference(inputs):
    """The comparison is bitwise: a record equal to the reference but for one quantile's last bit is not identical,
    and its deviation is that bit."""
    need_reference()
    import numpy as np
    row, ref = compare._reference(inputs, 'parity', 'B0-2026-09-06')
    mine = json.loads(json.dumps(ref))
    q = np.asarray(mine['python']['result']['quantiles'], float)
    q[0, 3] = np.nextafter(q[0, 3], np.inf)
    mine['python']['result']['quantiles'] = q.tolist()
    same = compare._fit_row('B0', row, ref, {**row, 'result_payload_sha256': row['payload_sha256']}, ref, lambda _: True)
    other = compare._fit_row('B0', row, ref, {**row, 'quantiles_sha256': 'x', 'result_payload_sha256': row['payload_sha256']},
                             mine, lambda _: True)
    assert same['bit_identical'] and same['bitwise_equal'] and same['max_abs_eur'] == 0
    assert not other['bit_identical'] and not other['bitwise_equal'] and 0 < other['max_abs_eur'] < 1e-12
    assert other['selections_match']


# --- the committed measurement ------------------------------------------------------------------------------------

def test_measurement_recomputes_from_the_downloaded_results():
    """Item 5: the committed measurement is what the downloaded results give, verified by their hashes."""
    downloads = project() / '.local/artifacts/cp-17c-probe/downloads'
    local = project() / '.local/artifacts/cp-17c-probe/runs/local-control'
    if not (REPORTS / 'measurement.json').exists():
        pytest.skip('no measurement committed yet')
    if not downloads.exists() or not local.exists():
        pytest.skip('the downloaded runner results and the local control are local material, absent on CI')
    need_reference()
    value = compare.compare(REPORTS / 'inputs.json', REPORTS / 'artifacts.json', downloads, local)
    assert value == load(REPORTS / 'measurement.json')


def test_report_is_the_render_of_the_committed_measurement():
    """Every table in the report is the measurement's: rendering it again gives the committed report."""
    from cp17cprobe import report
    if not (REPORTS / 'measurement.json').exists():
        pytest.skip('no measurement committed yet')
    rendered = report.render(load(REPORTS / 'measurement.json'), (REPORTS / 'proposals.md').read_text())
    assert rendered == (REPORTS / 'report.md').read_text()


def test_measurement_answers_every_recorded_item():
    """Per runner, day and policy: the identity, the frozen comparison, the measurement and the payload identity."""
    if not (REPORTS / 'measurement.json').exists():
        pytest.skip('no measurement committed yet')
    m = load(REPORTS / 'measurement.json')
    assert {'ubuntu-24.04', 'macos-26'} <= set(m['runners'])
    for label, r in {**m['runners'], 'local control': m['local_control']}.items():
        fits = list(r['parity'].values()) + list(r['f1'].values()) + [
            f for s in r['shadow'].values() for d in s['days'].values() for f in d['fits'].values()]
        assert fits, label
        for f in fits:
            assert f['bit_identical'] == (f['quantiles_sha256'] == f['reference_quantiles_sha256'])
            assert 'status' in f and 'max_abs_eur_by_level' in f and 'selections_match' in f
            assert f['wall_seconds'] is not None and f['peak_bytes'] is not None
            assert f['payload_identity_equal'] is not None
        assert r['host']['node']['version'] == '26.7.0'
    assert m['local_control']['host']['node']['sha256'] != m['reference']['node']['sha256']
    assert m['minutes']['counted_total'] <= 1500
