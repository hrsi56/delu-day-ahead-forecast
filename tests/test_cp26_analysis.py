"""Durable analysis orchestration fixtures; no real data or reduced production jobs."""
from datetime import date
import json

import numpy as np
import pandas as pd
import pytest

from cp26 import analysis as A
from cp26 import inference as I
from cp26 import diagnostics as D
from cp26 import scoring as S


def endpoint(values):
    return {'kind': 'paired_comparison', 'variant': 'primary14', 'left': 'nominal/v5', 'right': 'nominal/B0',
            'mask': 'all_eligible', 'metric': 'MAE', 'group': 'overall', 'value': 'overall',
            'difference': 1.0, 'difference_ci95': (np.nan, 2.0), 'replicate_differences': np.asarray(values, float),
            'draw_starts': np.arange(len(values), dtype=np.int32).reshape(-1, 1),
            'protocol_sha256': 'a' * 64, 'source_scores_sha256': 'b' * 64, 'analysis_code_sha256': 'c' * 64}


def test_parquet_roundtrip_preserves_mixed_groups_dates_and_undefined_lists(tmp_path):
    frame = pd.DataFrame({'stream': ['a', 'b', 'c'], 'value': [2021, True, 'DJF'],
                          'delivery_date': [date(2021, 1, 1)] * 3,
                          'periods': [[np.nan, 1.0], [2.0], []]})
    ref = A._table(tmp_path, 'fixture', frame, keys=('stream', 'value'))
    restored = A._load_table(tmp_path, ref)
    assert restored.value.tolist() == [2021, True, 'DJF']
    assert restored.delivery_date.tolist() == [date(2021, 1, 1)] * 3
    assert restored.periods.iloc[0] == [None, 1.0]
    assert A._table(tmp_path, 'fixture', frame, keys=('stream', 'value')) == ref
    changed = frame.copy()
    changed.at[0, 'value'] = 2022
    with pytest.raises(ValueError, match='preserve original'):
        A._table(tmp_path, 'fixture', changed, keys=('stream', 'value'))
    path = tmp_path / ref['path']
    with path.open('ab') as handle:
        handle.write(b'corruption')
    with pytest.raises(ValueError, match='hash changed'):
        A._load_table(tmp_path, ref)


def test_score_gate_runs_before_any_population_or_market_read(monkeypatch, tmp_path):
    reads = []
    monkeypatch.setattr(S, 'load_population', lambda root: reads.append(root))
    def denied(*args, **kwargs):
        raise RuntimeError('projection refused')
    monkeypatch.setattr(A, '_gate', denied)
    with pytest.raises(RuntimeError, match='projection refused'):
        A.run_scores(tmp_path, {'frozen': True}, gate=lambda _: None)
    assert reads == []


def test_numeric_replay_reuses_hashes_and_rejects_changed_replicates(tmp_path):
    relative = A.OUTPUT / 'inference' / 'fixture-endpoint'
    result = endpoint([.1, .2, .3])
    first = A._numeric(tmp_path, relative, result)
    second = A._numeric(tmp_path, relative, result)
    assert first == second
    assert first['difference_ci95'] == [None, 2.0]
    assert first['row_id'] == first['endpoint_id']
    assert 'replicate_differences' not in first
    with pytest.raises(ValueError, match='replicate array differs'):
        A._numeric(tmp_path, relative, endpoint([.1, .2, .4]))
    assert A._numeric(tmp_path, relative, result) == first


@pytest.mark.parametrize('interruption', ['between_renames', 'after_both_temp_files', 'array_temp_before_metadata'])
def test_numeric_atomic_pair_interruption_recovers_without_overwrite(tmp_path, interruption):
    relative = A.OUTPUT / 'inference' / 'fixture-recovery'
    result = endpoint([.1, .2, np.nan])
    original = A._numeric(tmp_path, relative, result)
    metadata, arrays = tmp_path / original['metadata_path'], tmp_path / original['arrays_path']
    if interruption == 'between_renames':
        metadata.unlink()
    elif interruption == 'array_temp_before_metadata':
        metadata.unlink()
        arrays.replace(arrays.with_name(arrays.name + '.tmp'))
    else:
        metadata.replace(metadata.with_name(metadata.name + '.tmp'))
        arrays.replace(arrays.with_name(arrays.name + '.tmp'))
    recovered = A._numeric(tmp_path, relative, result)
    assert recovered['arrays_sha256'] == original['arrays_sha256']
    assert json.loads(metadata.read_text())['result']['row_id'] == original['endpoint_id']
    assert A._numeric(tmp_path, relative, result) == recovered


def test_inference_restart_regenerates_rng_before_skipping_completed_writes(tmp_path, monkeypatch):
    monkeypatch.setattr(A, '_record_analysis_completion', lambda root, stage, value: value)
    protocol, code = {'frozen': True}, {'analysis': 'a' * 64}
    scores = {'daily': pd.DataFrame(), 'known_price_states': pd.DataFrame(),
              'manifest': {'content_sha256': 'b' * 64}}
    monkeypatch.setattr(A, '_gate', lambda *args: None)
    monkeypatch.setattr(A, '_code', lambda _: code)
    monkeypatch.setattr(A, 'load_scores', lambda *args: scores)
    monkeypatch.setattr(A, 'workload_counts', lambda: {'bootstrap_endpoints': 4, 'mcs_cells': 1,
                                                     'secondary_DM_GW_entries': 8, 'moment_cells': 936})
    monkeypatch.setattr(I, 'comparison_registry', lambda _: (('nominal/v5', 'nominal/B0'),))
    draws = []
    def iterator(daily, *, comparisons, production):
        assert production is True
        rng = np.random.default_rng(I.SEED)
        for index in range(4):
            values = rng.normal(size=5)
            draws.append((index, values.copy()))
            yield {**endpoint(values), 'value': index}
    monkeypatch.setattr(I, 'iter_inference', iterator)
    monkeypatch.setattr(I, 'iter_mcs', lambda *args, **kwargs: iter([
        {'mask': 'all_eligible', 'metric': 'MAE', 'status': 'fixture_unavailable', 'history': [], 'remaining': []}]))
    monkeypatch.setattr(S, 'paired_losses', lambda *args, **kwargs: (pd.DataFrame(), {'paired_dates': 0}))
    monkeypatch.setattr(I, 'diebold_mariano', lambda _: {'status': 'fixture_unavailable', 'p_value': 1.0})
    monkeypatch.setattr(I, 'giacomini_white', lambda *_: {'status': 'fixture_unavailable', 'p_value': 1.0})
    original, completed = A._numeric, []
    def interrupted(root, stem, result):
        if len(completed) == 2:
            raise RuntimeError('dedicated fixture interrupted')
        reference = original(root, stem, result)
        completed.append(reference)
        return reference
    monkeypatch.setattr(A, '_numeric', interrupted)
    with pytest.raises(RuntimeError, match='fixture interrupted'):
        A.run_inference(tmp_path, protocol, gate=lambda _: None)
    first_hashes = [(r['metadata_sha256'], r['arrays_sha256']) for r in completed]
    monkeypatch.setattr(A, '_numeric', original)
    manifest = A.run_inference(tmp_path, protocol, gate=lambda _: None)
    assert manifest['bootstrap_endpoint_count'] == 4
    assert [(r['metadata_sha256'], r['arrays_sha256']) for r in manifest['endpoints'][:2]] == first_hashes
    assert [index for index, _ in draws] == [0, 1, 2, 0, 1, 2, 3]
    assert all(np.array_equal(draws[index][1], draws[index + 3][1]) for index in range(3))


def test_diagnostics_holm_retains_all_936_cells_and_all_masks(tmp_path, monkeypatch):
    monkeypatch.setattr(A, '_record_analysis_completion', lambda root, stage, value: value)
    protocol, code = {'frozen': True}, {'analysis': 'a' * 64}
    manifest = {'content_sha256': 'b' * 64, 'tables': {'known_price_states': {'fixture': True},
                                                               'fallbacks_by_mask': {'fixture': True}}}
    scores = {'daily': pd.DataFrame(), 'hourly': pd.DataFrame(), 'manifest': manifest}
    monkeypatch.setattr(A, '_gate', lambda *args: None)
    monkeypatch.setattr(A, '_code', lambda _: code)
    monkeypatch.setattr(A, 'load_scores', lambda *args: scores)
    from test_cp26_analysis_inventory import complete_table
    monkeypatch.setattr(D, 'calibration_tables', lambda *_: {name: complete_table(name) for name in ('coverage', 'quantile_hits', 'histogram')})
    monkeypatch.setattr(D, 'christoffersen', lambda *_: pd.DataFrame())
    monkeypatch.setattr(D, 'realized_outcome_slices', lambda *_: {'slices': pd.DataFrame(), 'thresholds': pd.DataFrame()})
    def cells(*args, streams, production):
        assert streams == S.RESEARCH_STREAMS and production is True
        for stream in sorted(streams):
            for hour in range(24):
                for interval in (50, 80, 95):
                    yield {'identity': f'{stream}/hour{hour:02d}/interval{interval}', 'stream': stream,
                           'local_hour': hour, 'interval': interval, 'mask': 'all_eligible',
                           'p_value': 1.0, 'status': 'fixture_unavailable'}
    monkeypatch.setattr(D, 'iter_moment_family', cells)
    monkeypatch.setattr(A, '_numeric', lambda root, stem, result: {**result, 'endpoint_id': I.endpoint_identity(result)})
    original_read = A._read
    def read(path, schema=None):
        if path.name == 'inference-manifest.json':
            return {'status': 'COMPLETE', 'protocol': protocol, 'code_sha256': code,
                    'scores_manifest_sha256': manifest['content_sha256'], 'content_sha256': 'c' * 64,
                    'mcs': {'cells': []}}
        return original_read(path, schema)
    monkeypatch.setattr(A, '_read', read)
    result = A.run_diagnostics(tmp_path, protocol, gate=lambda _: None)
    assert len(result['moment_family']['cells']) == len(result['moment_family']['holm']) == 936
    assert all(row['family_size'] == 936 and row['adjusted_p_value'] == 1 for row in result['moment_family']['holm'])
    assert 'fallbacks_by_mask' in result['tables']


def test_workload_matches_registered_universe():
    assert A.workload_counts() == {'research_streams': 13, 'comparisons': 26, 'bootstrap_endpoints': 15808,
                                   'mcs_cells': 8, 'secondary_DM_GW_entries': 208, 'moment_cells': 936}


def test_future_test_price_includes_complete_preparation_worker_duration():
    jobs = [{'name': 'continuation-preparation-suite-r4', 'job_id': 'complete', 'running': False,
             'wall_seconds': 100.0, 'workers': 3},
            {'name': 'small-tests', 'job_id': 'small', 'running': False, 'wall_seconds': 5.0, 'workers': 1},
            {'name': 'current-parity', 'job_id': 'parity', 'running': False, 'wall_seconds': 500.0, 'workers': 1}]
    prices = A._prior_costs({'jobs': jobs})
    assert prices['tests']['machine_seconds'] == 600
    assert prices['tests']['maximum_job']['job_id'] == 'complete'
    assert prices['parity']['machine_seconds'] == 1000


def test_truncated_pending_npz_is_preserved_then_regenerated(tmp_path, monkeypatch):
    from cp26 import harness
    recovery_root = tmp_path / '.local/artifacts'
    monkeypatch.setattr(harness, 'art', lambda: recovery_root)
    relative = A.OUTPUT / 'inference' / 'truncated-fixture'
    result = endpoint([.1, .2, .3])
    original = A._numeric(tmp_path, relative, result)
    metadata, arrays = tmp_path / original['metadata_path'], tmp_path / original['arrays_path']
    metadata.unlink()
    pending = arrays.with_name(arrays.name + '.tmp')
    pending.write_bytes(arrays.read_bytes()[:12])
    arrays.unlink()
    partial = pending.read_bytes()
    restored = A._numeric(tmp_path, relative, result)
    assert restored['arrays_sha256'] == original['arrays_sha256']
    assert not pending.exists()
    assert any(path.read_bytes() == partial for path in recovery_root.rglob('*') if path.is_file())


def test_completed_inference_resume_verifies_hashes_without_new_draws(tmp_path, monkeypatch):
    protocol, code = {'frozen': True}, {'analysis': 'a' * 64}
    scores = {'daily': pd.DataFrame(), 'known_price_states': pd.DataFrame(),
              'manifest': {'content_sha256': 'b' * 64}}
    monkeypatch.setattr(A, '_gate', lambda *args: None)
    monkeypatch.setattr(A, '_code', lambda _: code)
    monkeypatch.setattr(A, 'load_scores', lambda *args: scores)
    monkeypatch.setattr(A, '_record_analysis_completion', lambda root, stage, value: value)
    counts = {'bootstrap_endpoints': 1, 'mcs_cells': 0, 'secondary_DM_GW_entries': 0, 'moment_cells': 936}
    monkeypatch.setattr(A, 'workload_counts', lambda: counts)
    monkeypatch.setattr(I, 'comparison_registry', lambda _: ())
    monkeypatch.setattr(I, 'iter_mcs', lambda *args, **kwargs: iter(()))
    monkeypatch.setattr(I, 'iter_inference', lambda *args, **kwargs: iter([endpoint([.1, .2, .3])]))
    result = A.run_inference(tmp_path, protocol, gate=lambda _: None)
    def unexpected(*args, **kwargs):
        raise AssertionError('completed inference consumed new RNG draws')
    monkeypatch.setattr(I, 'iter_inference', unexpected)
    assert A.run_inference(tmp_path, protocol, gate=lambda _: None) == result
    arrays = tmp_path / result['endpoints'][0]['arrays_path']
    arrays.write_bytes(arrays.read_bytes() + b'changed')
    with pytest.raises(ValueError, match='artifact content changed'):
        A.run_inference(tmp_path, protocol, gate=lambda _: None)


def test_terminal_analysis_counter_is_exactly_once_without_duration_charge(tmp_path, monkeypatch):
    from cp26.budget import Budget, total_seconds
    budget = Budget(tmp_path / 'budget.json')
    budget.initialise()
    monkeypatch.setattr(A, 'Budget', lambda: budget)
    value = {'protocol': {'frozen': True}, 'status': 'COMPLETE', 'content_sha256': 'a' * 64,
             'code_sha256': {'analysis.py': 'b' * 64}, 'scores_manifest_sha256': 'c' * 64}
    assert A._record_analysis_completion(tmp_path, 'inference', value) == value
    A._record_analysis_completion(tmp_path, 'inference', value)
    assert len(budget.read()['execution_tasks']) == 1
    assert total_seconds(budget.read()) == 0
    with pytest.raises(ValueError, match='reused with different evidence'):
        A._record_analysis_completion(tmp_path, 'inference', {**value, 'content_sha256': 'd' * 64})


def test_benchmark_requests_full_counts_and_returns_only_resource_evidence(tmp_path, monkeypatch):
    from cp26 import harness as H
    monkeypatch.setenv('CP26_MONITORED_JOB', 'dedicated-fixture')
    monkeypatch.setattr(H, 'continuation_authority', lambda _: {'fixture': True})
    monkeypatch.setattr(H, 'check_blas', lambda: None)
    code = {'src/cp26/analysis.py': 'a' * 64}
    monkeypatch.setattr(A, '_code', lambda _: code)
    monkeypatch.setattr(I, 'paired_bootstrap', lambda pair, production, **kwargs: {'replicate_differences': np.zeros(10000)})
    monkeypatch.setattr(I, 'secondary_ratio_bootstrap', lambda pair, group, production, **kwargs: {'replicate_ratios': np.zeros(10000)})
    monkeypatch.setattr(I, 'model_confidence_set', lambda losses, mask, metric, production: {
        'replicate_means': np.zeros((10000, 13)), 'status': 'computable', 'history': [{}] * 12, 'remaining': ['fixture']})
    monkeypatch.setattr(I, 'diebold_mariano', lambda _: {})
    monkeypatch.setattr(I, 'giacomini_white', lambda *_: {})
    monkeypatch.setattr(D, 'moment_test', lambda cell, interval, production: {'replicate_statistics': np.zeros(100000)})
    monkeypatch.setattr(A, '_calibration_fixture', lambda _: (pd.DataFrame(), pd.DataFrame()))
    monkeypatch.setattr(D, 'calibration_tables', lambda *_: {})
    monkeypatch.setattr(D, 'christoffersen', lambda *_: None)
    monkeypatch.setattr(D, 'realized_outcome_slices', lambda *_: {})
    names = []
    def measured(name, run):
        result = run()
        names.append(name)
        return result, {'name': name, 'started_epoch': 1.0, 'ended_epoch': 3.0, 'wall_seconds': 2.0, 'peak_rss_bytes': 1000}
    monkeypatch.setattr(A, '_measure', measured)
    class Ledger:
        def read(self):
            return {}
    monkeypatch.setattr(A, 'Budget', Ledger)
    monkeypatch.setattr(A, '_prior_costs', lambda _: {name: {'classification': 'conservative', 'machine_seconds': 10,
        'basis': 'identified fixture supervised receipt', 'evidence_sha256': 'b' * 64} for name in ('tests', 'parity')})
    result = A.benchmark(tmp_path)
    assert result['fixture_only'] and not result['market_data_read'] and not result['evaluation_scores_computed']
    assert result['code_sha256'] == code and len(names) == 10
    assert set(result['additional_costs']) == {'tests', 'parity', 'bootstrap', 'diagnostics', 'failed_jobs_and_resume'}
    assert result['additional_costs']['bootstrap']['machine_seconds'] == 1.5 * 2 * (15808 + 8 + 208)
    assert result['additional_costs']['diagnostics']['machine_seconds'] == 1.5 * 2 * (936 + 1)
    assert result['additional_costs']['failed_jobs_and_resume']['extend_with_pilot_fit_and_search_prices']
    assert all(row['machine_seconds'] > 0 and row['evidence_sha256'] for row in result['additional_costs'].values())
    assert not {'difference', 'ratio', 'p_value', 'statistic', 'coverage'}.intersection(result)
    assert A.benchmark(tmp_path) == result
