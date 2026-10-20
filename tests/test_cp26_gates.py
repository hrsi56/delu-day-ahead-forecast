"""CLI refusal and durable signed progress are executable gates, not status flags."""
import importlib.util
import json
from pathlib import Path

import pytest

from cp26 import budget as B, costing as C, execution as E, gates as G


@pytest.fixture
def driver():
    path = Path(__file__).resolve().parents[1] / 'scripts/cp26_rebaseline.py'
    spec = importlib.util.spec_from_file_location('cp26_continuation_cli', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_prepare_admission_reconciles_through_resource_api_without_history_lock(tmp_path, monkeypatch):
    budget = B.Budget(tmp_path / 'admission-ledger.json')
    budget.initialise()
    authority = G.H.PINS[G.H.SCIENTIFIC_AUTHORITY_PATH]
    with budget.transaction() as state:
        state['continuation_scope'] = {'authority_sha256': authority}
        state['execution_tasks'] = [{'id': 'preserved/history', 'evidence': {'value': 1}}]
    original = budget.path.read_bytes()
    monkeypatch.setenv('CP26_MONITORED_JOB', 'synthetic-admission')
    monkeypatch.setenv('CP26_RUN_ID', G.RUN_ID)
    monkeypatch.setattr(G.H, 'runtime_lineage', lambda root: {'synthetic': True})
    monkeypatch.setattr(G.H, 'continuation_authority', lambda root: {})
    monkeypatch.setattr(G.H, 'check_blas', lambda: None)
    monkeypatch.setattr(G, 'protocol_identity', lambda root: {})

    def forbidden_history_transaction(**kwargs):
        raise AssertionError('admission may not lock and serialize task history')

    monkeypatch.setattr(budget, 'transaction', forbidden_history_transaction)
    G.ExecutionGate(tmp_path, budget=budget)('prepare')
    assert budget.path.read_bytes() == original
    assert budget.last_transaction['acquired'] and not budget.last_transaction['written']


def test_cli_parity_keeps_original_repair_output_unchanged(driver, monkeypatch):
    from cp26 import parity
    observed = []
    monkeypatch.setenv('CP26_MONITORED_JOB', 'fixture-no-physical-compute')
    monkeypatch.setattr(parity, 'run', lambda root, *, output: observed.append(output) or
                        {'status': 'PASS', 'checks': list(range(96))})
    assert driver.dispatch('parity') == 0
    assert observed == [G.OUTPUT / 'parity.json']


def test_cli_project_persists_refused_estimate_and_stops_execution(driver, monkeypatch, tmp_path, capsys):
    state = {'counts': {'machine_seconds': 130}, 'accounting': {
        'measured_seconds': 100, 'reported_seconds': 10, 'reserved_seconds': 20}, 'reserves': []}
    searches = [{'run': r, 'k': k, 'machine_seconds': 10, 'classification': 'conservative',
                 'basis': 'identity-bound fixture cost'} for r in ('nominal', 'noload', 'gfs6') for k in range(14)]
    searches[0]['machine_seconds'] = 440 * B.HOUR
    remaining = {n: {'machine_seconds': 1, 'classification': 'conservative', 'basis': 'fixture cost'}
                 for n in ('daily_fits', 'parity', 'tests', 'bootstrap', 'diagnostics', 'failed_jobs_and_resume')}
    projection = C._signed({'schema': C.SCHEMA, 'ledger_seconds_at_pricing': 130, 'protocol': {'run_id': G.RUN_ID},
                            'searches': searches, 'remaining': remaining,
                            **B.projected_cost(state, searches, remaining, run_id=G.RUN_ID)})
    shared, code = {'authority_sha256': 'a' * 64, 'run_id': G.RUN_ID}, {'fixture.py': 'b' * 64}
    monkeypatch.setenv('CP26_MONITORED_JOB', 'fixture-no-physical-compute')
    monkeypatch.setattr(driver, 'ROOT', tmp_path)
    monkeypatch.setattr(driver, 'Budget', lambda: type('FixtureBudget', (), {'read': lambda self: state})())
    monkeypatch.setattr(G, 'authorize_consuming_process', lambda root: shared)
    monkeypatch.setattr(G, 'ExecutionGate', lambda root: lambda stage: None)
    monkeypatch.setattr(G, 'protocol_identity', lambda root: shared)
    monkeypatch.setattr(G, 'code_identity', lambda root: code)
    monkeypatch.setattr(E, 'manifest_for', lambda *args: {'schema': 'fixture'})
    monkeypatch.setattr(E, '_read', lambda path: {'code_sha256': code, 'additional_costs': remaining}
                        if path.name == 'fixture-benchmark.json' else {'schema': 'fixture'})
    monkeypatch.setattr(C, 'price_pilot', lambda *args, **kwargs: projection)
    (tmp_path / G.PROTOCOL).parent.mkdir(parents=True)
    (tmp_path / G.PROTOCOL).write_bytes(b'fixture protocol, physical reads stubbed')
    with pytest.raises(B.CapExceeded, match='440-hour cumulative admission line'):
        driver.dispatch('project')
    saved = json.loads((tmp_path / G.OUTPUT / G.PROJECTION_NAME).read_text())
    assert saved == projection
    assert not saved['within_pilot_stop'] and saved['searches_priced'] == 42
    assert '"within_pilot_stop": false' in capsys.readouterr().out
    assert B.total_seconds(state) == 130


def test_completed_search_price_requires_cumulative_ledger_task():
    state = {'counts': {'machine_seconds': 0}, 'execution_tasks': []}
    rows = [{'run': r, 'k': k, 'machine_seconds': 10, 'classification': 'conservative', 'basis': 'fixture'}
            for r in ('nominal', 'noload', 'gfs6') for k in range(14)]
    rows[0]['completed_evidence'] = {'result_sha256': 'a' * 64, 'path': 'fixture/result.json', 'task_id': 'search/fixture'}
    costs = {n: {'machine_seconds': 1, 'classification': 'conservative', 'basis': 'fixture'}
             for n in ('daily_fits', 'parity', 'tests', 'bootstrap', 'diagnostics', 'failed_jobs_and_resume')}
    with pytest.raises(ValueError, match='matching cumulative-ledger task'):
        B.projected_cost(state, rows, costs)
    state['execution_tasks'].append({'id': 'search/fixture', 'evidence': {'result_sha256': 'a' * 64}})
    assert B.projected_cost(state, rows, costs)['remaining_search_seconds'] == 410
    assert B.total_seconds(state) == 0


def test_analysis_estimate_discount_requires_bound_terminal_task(tmp_path, monkeypatch):
    from cp26 import analysis as A
    code, protocol = {'fixture': 'a' * 64}, {'frozen': True}
    monkeypatch.setattr(G, 'code_identity', lambda _: code)
    output = tmp_path / G.OUTPUT
    output.mkdir(parents=True)
    scores = A._signed({'schema': A.SCORE_SCHEMA, 'protocol': protocol, 'code_sha256': code})
    value = A._signed({'schema': A.INFERENCE_SCHEMA, 'status': 'COMPLETE', 'protocol': protocol,
                       'code_sha256': code, 'scores_manifest_sha256': scores['content_sha256']})
    (output / 'scores-manifest.json').write_text(json.dumps(scores))
    (output / 'inference-manifest.json').write_text(json.dumps(value))
    remaining = {'bootstrap': {'machine_seconds': 123}, 'diagnostics': {'machine_seconds': 456}}
    state = {'execution_tasks': []}
    G._discount_completed_analysis(remaining, {'protocol': protocol}, tmp_path, output, state)
    assert remaining['bootstrap']['machine_seconds'] == 123
    task = {'id': f"analysis/{E.digest(protocol)}/inference", 'evidence': {
        'manifest_sha256': value['content_sha256'], 'status': 'COMPLETE', 'code_sha256': E.digest(code),
        'scores_manifest_sha256': scores['content_sha256']}}
    state['execution_tasks'].append(task)
    G._discount_completed_analysis(remaining, {'protocol': protocol}, tmp_path, output, state)
    assert remaining['bootstrap']['machine_seconds'] == 0
    assert remaining['diagnostics']['machine_seconds'] == 456
    task['evidence']['manifest_sha256'] = 'b' * 64
    with pytest.raises(RuntimeError, match='disagrees with its ledger task'):
        G._discount_completed_analysis(remaining, {'protocol': protocol}, tmp_path, output, state)


def test_project_retry_reuses_frozen_identity_and_reprices_live_ledger(driver, tmp_path, monkeypatch, capsys):
    shared, code = {'frozen': True, 'run_id': G.RUN_ID}, {'fixture': 'a' * 64}
    output = tmp_path / G.OUTPUT
    output.mkdir(parents=True)
    pilot, manifest = {'sealed': True}, {'content_sha256': 'b' * 64}
    projection = C._signed({'schema': C.SCHEMA, 'protocol': shared, 'code_sha256': code,
                           'pilot_sha256': E.digest(pilot), 'execution_manifest_sha256': manifest['content_sha256']})
    frozen = json.dumps(projection)
    (output / G.PROJECTION_NAME).write_text(frozen)
    state = {'counts': {'machine_seconds': 77}, 'accounting': {'measured_seconds': 77,
             'reported_seconds': 0, 'reserved_seconds': 0}, 'reserves': []}
    rows = [{'run': r, 'k': k, 'machine_seconds': 1, 'classification': 'conservative', 'basis': 'fixture'}
            for r in ('nominal', 'noload', 'gfs6') for k in range(14)]
    costs = {n: {'machine_seconds': 1, 'classification': 'conservative', 'basis': 'fixture'}
             for n in ('daily_fits', 'parity', 'tests', 'bootstrap', 'diagnostics', 'failed_jobs_and_resume')}
    seen = []
    monkeypatch.setenv('CP26_MONITORED_JOB', 'fixture-no-physical-compute')
    monkeypatch.setattr(driver, 'ROOT', tmp_path)
    monkeypatch.setattr(driver, 'Budget', lambda: type('FixtureBudget', (), {'read': lambda self: state})())
    monkeypatch.setattr(G, 'authorize_consuming_process', lambda _: shared)
    monkeypatch.setattr(G, 'protocol_identity', lambda _: shared)
    monkeypatch.setattr(G, 'code_identity', lambda _: code)
    monkeypatch.setattr(G, 'ExecutionGate', lambda _: lambda stage: seen.append(stage))
    monkeypatch.setattr(G, 'outstanding_projection', lambda *args: (rows, costs))
    monkeypatch.setattr(E, 'manifest_for', lambda *args: manifest)
    monkeypatch.setattr(E, '_read', lambda _: pilot)
    def unexpected(*args, **kwargs):
        raise AssertionError('retry regenerated immutable projection')
    monkeypatch.setattr(C, 'price_pilot', unexpected)
    assert driver.dispatch('project') == 0
    assert seen == ['pilot', 'search']
    assert (output / G.PROJECTION_NAME).read_text() == frozen
    result = json.loads(capsys.readouterr().out)
    assert result['status'] == 'COST_PROJECTION_REUSED'
    assert result['hours'] == 125 / B.HOUR
    state['counts']['machine_seconds'] = 440 * B.HOUR
    state['accounting']['measured_seconds'] = 440 * B.HOUR
    with pytest.raises(B.CapExceeded, match='440-hour cumulative admission line'):
        driver.dispatch('project')
    assert (output / G.PROJECTION_NAME).read_text() == frozen
