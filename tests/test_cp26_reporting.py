"""Stored synthetic evidence presentation; no score, fit or inference execution."""
import copy
import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

from cp26 import reporting as R
from test_cp26_analysis_inventory import complete_table


def test_report_reads_identity_bound_json_columns_as_values(tmp_path):
    from datetime import date
    from cp26 import analysis as A
    frame = pd.DataFrame({'stream': ['nominal/v5'], 'delivery_date': [date(2021, 1, 1)],
                          'value': [2021], 'periods': [[None, 2.0]]})
    reference = A._table(tmp_path, 'report-fixture', frame, keys=('stream', 'delivery_date'))
    restored = R._load_table(tmp_path, reference)
    assert restored.stream.iloc[0] == 'nominal/v5'
    assert restored.delivery_date.iloc[0] == date(2021, 1, 1)
    assert restored.value.iloc[0] == 2021
    assert restored.periods.iloc[0] == [None, 2.0]

PROTOCOL = {'documents': {'execution': 'synthetic'}, 'evidence_class': 'development_post_selection'}


def evidence():
    streams = ('nominal/B0', 'nominal/v1-R', 'nominal/v2', 'nominal/v3', 'nominal/v4', 'nominal/v5',
               'nominal/D2', 'noload/v3', 'noload/v4', 'noload/v5', 'gfs6/v3', 'gfs6/v4', 'gfs6/v5')
    summaries = complete_table('summaries')
    summaries.loc[summaries.metric.eq('WIS'), 'raw_mean_daily_loss'] = 20.
    summaries['raw_available_dates'], summaries['paired_dates'] = 1000, 1000
    for year, loss in ((2023, 11.), (2024, 10.), (2025, 12.)):
        selected = summaries.stream.eq('nominal/v5') & summaries['mask'].eq('all_eligible') & summaries.metric.eq('MAE') \
                   & summaries.group.eq('year') & summaries.value.eq(year)
        summaries.loc[selected, ['raw_mean_daily_loss', 'raw_available_dates', 'paired_dates']] = [loss, 365, 365]
    selected = summaries.stream.eq('nominal/v5') & summaries['mask'].eq('all_eligible') & summaries.metric.eq('MAE') \
               & summaries.group.eq('stress_2021_2022') & summaries.value.eq(True)
    summaries.loc[selected, 'raw_mean_daily_loss'] = 30.
    fallback = [{'stream': stream, 'calendar_dates': 2078, 'eligible_dates': 1000,
                 'fallback_dates': 20 if stream == 'nominal/v5' else 10 if stream == 'noload/v5' else 0,
                 'failed_dates': 0, 'fallback_fraction': .02 if stream == 'nominal/v5' else .01 if stream == 'noload/v5' else 0.,
                 'exceeds_one_percent': stream == 'nominal/v5', 'reason_counts': {}} for stream in streams]
    scores = {'daily': pd.DataFrame(), 'hourly': pd.DataFrame(), 'summaries': pd.DataFrame(summaries),
              'secondary_summaries': pd.DataFrame(), 'local_hour_summaries': complete_table('local_hour_summaries'),
              'fallbacks': pd.DataFrame(fallback), 'population_evidence': {'fixture_only': True},
              'released_reference': {'daily': [{'delivery_date': '2026-06-09', 'MAE': 8., 'WIS': 12., 'available': True}],
                                     'metadata': {'source': 'historical synthetic reference', 'original_issue_contract': True},
                                     'key_differences': []}}
    endpoints = []
    contrasts = [('nominal/v3', 'nominal/v2'), ('nominal/v4', 'nominal/v3'), ('nominal/v5', 'nominal/v4'),
                 ('noload/v5', 'nominal/v5'), ('gfs6/v5', 'nominal/v5')]
    for left, right in contrasts:
        for mask in R.MASKS:
            for metric in ('MAE', 'WIS'):
                ratio = 1.02001 if left == 'gfs6/v5' and metric == 'MAE' else .99
                endpoints.append({'endpoint_id': f'{left}/{right}/{mask}/{metric}', 'kind': 'paired_comparison',
                    'variant': 'primary14', 'left': left, 'right': right, 'mask': mask, 'metric': metric,
                    'group': 'overall', 'value': 'overall', 'ratio': ratio, 'difference': -.1,
                    'ratio_status': 'computable', 'difference_status': 'computable',
                    'ratio_ci95': [.98, 1.04], 'difference_ci95': [-.2, .1],
                    'calendar_dates': 1000, 'paired_dates': 990, 'either_missing_dates': 10})
    calibration = {name: complete_table(name) for name in ('coverage', 'quantile_hits', 'histogram')}
    coverage = calibration['coverage']
    selected = coverage['mask'].eq('all_eligible') & coverage.stream.eq('nominal/v5') \
               & coverage.group.eq('overall') & coverage.interval.eq(80)
    coverage.loc[selected, ['coverage80', 'width80', 'n_dates']] = [.75, 22.5, 990]
    diagnostics = {'schema': 'cp26-diagnostics-manifest-v1', 'tables': calibration,
        'moment_family': {'cells': [{'endpoint_id': 'moment-fixture', 'status': 'insufficient_support', 'p_value': 1.}],
                          'holm': {'moment-fixture': {'adjusted_p_value': 1., 'rejected': False}}}, 'mcs': {'cells': []}}
    resources = {'measured_seconds': 100., 'reported_seconds': 5., 'reserved_seconds': 10., 'total_seconds': 115.,
                 'repair_seconds_used': 50., 'repair_scope_active': False, 'continuation_seconds_used': 40.,
                 'repair_terminal_snapshot': {'resources_sha256': 'synthetic-snapshot', 'total_seconds': 75.}}
    return scores, {'schema': 'cp26-inference-manifest-v1', 'endpoints': endpoints}, diagnostics, resources


def build(tmp_path, inputs=None):
    scores, inference, diagnostics, resources = inputs or evidence()
    return R.build_report(tmp_path, 'reports/rebaseline/continuation-v21-r14', scores, inference,
                          diagnostics, resources, PROTOCOL)


def test_deterministic_report_binds_masks_transitions_references_and_local_routes(tmp_path):
    result = build(tmp_path)
    report, packet, export = (result['report'], result['publication_packet'], result['mlflow_export'])
    assert len(report['transitions']) == 3
    assert all({r['mask'] for r in t['comparisons']} == set(R.MASKS) for t in report['transitions'])
    assert report['gfs6']['fragile'] is True
    assert len(report['main_fallback_flags']) == 1
    assert report['released_reference']['daily_rows'][0]['delivery_date'] == '2026-06-09'
    assert not report['missing_references']
    ordinary = next(r for r in report['absolute_context'] if r['stream'] == 'nominal/v5')
    assert ordinary['ordinary_complete_year_range'] == [10., 12.]
    assert report['adoption_decision'] is None and report['integration_verdict'] is None
    assert packet['status'] == 'DRAFT_LOCAL'
    assert packet['publication_completion_receipt']['status'] == 'INCOMPLETE'
    assert all(r['status'] == 'not performed' for r in packet['publication_completion_receipt']['surfaces'].values())
    assert export['destination'] == 'local-only' and export['remote_writes'] == 0
    run = next(r for r in export['runs'] if r['key'] == 'cp-26/nominal/v5/all_eligible')
    assert run['metrics']['MAE/raw_mean_daily_loss'] == 10.
    assert run['metric_source_rows']
    first = {name: Path(path).read_bytes() for name, path in result['paths'].items()}
    assert build(tmp_path)['report'] == report
    assert first == {name: Path(path).read_bytes() for name, path in result['paths'].items()}
    assert all('<…>' not in value.decode() for value in first.values())


def test_degeneracy_and_unavailable_reference_stay_explicit(tmp_path):
    inputs = evidence()
    row = next(r for r in inputs[1]['endpoints'] if r['left'] == 'nominal/v5' and r['right'] == 'nominal/v4'
               and r['mask'] == 'all_eligible' and r['metric'] == 'MAE')
    row.update(ratio_status='nonpositive_or_nonfinite_observed_variance', ratio_ci95=[.8, 1.2])
    inputs[0].pop('released_reference')
    result = build(tmp_path, inputs)
    comparison = next(r for r in result['report']['transitions'][2]['comparisons']
                      if r['mask'] == 'all_eligible' and r['metric'] == 'MAE')
    assert comparison['point_comparison'] and comparison['ratio_ci95'] is None
    assert row['endpoint_id'] in {r['row_id'] for r in result['report']['unavailable_inference']}
    assert result['report']['missing_references'] == ['released-v1 original holdout']
    text = Path(result['paths']['report.md']).read_text()
    assert 'point comparison, interval unavailable' in text and 'reference is unavailable' in text


def test_strict_fragility_threshold_and_fallback_negative_control(tmp_path):
    inputs = evidence()
    for row in inputs[1]['endpoints']:
        if row['left'] == 'gfs6/v5':
            row['ratio'] = 1.02
    assert build(tmp_path, inputs)['report']['gfs6']['fragile'] is False
    inputs[0]['fallbacks'].loc[inputs[0]['fallbacks'].stream.eq('nominal/v5'), 'exceeds_one_percent'] = False
    with pytest.raises(ValueError, match='threshold flag'):
        build(tmp_path, inputs)


def test_resource_changes_fingerprint_without_changing_population_or_closed_snapshot(tmp_path):
    first = build(tmp_path)['report']
    inputs = evidence()
    inputs[3]['measured_seconds'] += 1.
    second = build(tmp_path, inputs)['report']
    assert first['candidate_fingerprint'] != second['candidate_fingerprint']
    assert first['population_id'] == second['population_id']
    assert second['resources']['repair_terminal_snapshot'] == first['resources']['repair_terminal_snapshot']
    assert second['resources']['repair_seconds_used'] == first['resources']['repair_seconds_used']


def test_artifact_hash_and_scalar_binding_refuse_manipulated_endpoint(tmp_path):
    inputs = evidence()
    row = inputs[1]['endpoints'][0]
    directory = tmp_path / 'reports/rebaseline/continuation-v21-r14/inference'
    directory.mkdir(parents=True)
    arrays = directory / 'fixture.npz'
    arrays.write_bytes(b'synthetic stored numeric artifact')
    array_hash = hashlib.sha256(arrays.read_bytes()).hexdigest()
    metadata = directory / 'fixture.json'
    metadata.write_text(json.dumps({'schema': 'cp26-numeric-artifact-v1', 'endpoint_id': row['endpoint_id'],
                                   'arrays_file': arrays.name, 'arrays_sha256': array_hash, 'result': copy.deepcopy(row)}))
    row.update(metadata_path=str(metadata.relative_to(tmp_path)), metadata_sha256=hashlib.sha256(metadata.read_bytes()).hexdigest(),
               arrays_path=str(arrays.relative_to(tmp_path)), arrays_sha256=array_hash)
    row['ratio'] = .01
    with pytest.raises(ValueError, match='committed metadata row'):
        build(tmp_path, inputs)
    row['ratio'] = .99
    arrays.write_bytes(b'changed content')
    with pytest.raises(ValueError, match='array hash'):
        build(tmp_path, inputs)


def test_report_rejects_closed_delivery_day_and_output_escape(tmp_path):
    inputs = evidence()
    inputs[0]['released_reference']['daily'][0]['delivery_date'] = '2026-09-07'
    with pytest.raises(ValueError):
        build(tmp_path, inputs)
    with pytest.raises(ValueError, match='reports/rebaseline'):
        R.build_report(tmp_path, '../escape', *evidence(), PROTOCOL)


def test_empty_registered_cells_and_ratio_only_failure_remain_visible(tmp_path):
    inputs = evidence()
    summaries = inputs[0]['summaries']
    selected = summaries['mask'].eq('newly_opened') & (
        (summaries.group.eq('season') & summaries.value.eq('DJF')) |
        (summaries.group.eq('canonical_hours') & summaries.value.isin((23, 25))))
    summaries.loc[selected, ['status', 'reason', 'ratio_status', 'ratio_undefined_reason']] = [
        'unavailable', 'no_calendar_support', 'unavailable', 'zero_or_nonfinite_B0_denominator']
    summaries.loc[selected, ['n_hours', 'n_dates', 'raw_available_dates', 'calendar_dates', 'paired_dates']] = 0
    summaries.loc[selected, ['raw_mean_daily_loss', 'B0_ratio', 'paired_B0_loss']] = float('nan')
    for table in inputs[2]['tables'].values():
        selected = table['mask'].eq('newly_opened') & (
            (table.group.eq('season') & table.value.eq('DJF')) |
            (table.group.eq('canonical_hours') & table.value.isin((23, 25))))
        table.loc[selected, ['status', 'reason']] = ['unavailable', 'no_calendar_support']
        table.loc[selected, ['n_hours', 'n_dates', 'calendar_dates']] = 0
        quantities = [name for name in table if name.startswith(('coverage', 'width'))]
        table.loc[selected, quantities] = float('nan')
    hours = inputs[0]['local_hour_summaries']
    selected = hours['mask'].eq('all_eligible') & hours.stream.eq('nominal/v5') & hours.local_hour.eq(0) & hours.metric.eq('MAE')
    hours.loc[selected, ['B0_ratio', 'ratio_status', 'ratio_undefined_reason']] = [
        float('nan'), 'unavailable', 'zero_or_nonfinite_B0_denominator']
    result = build(tmp_path, inputs)
    report, packet = result['report'], result['publication_packet']
    winter = next(row for row in report['breakdown_coverage'] if row['mask'] == 'newly_opened' and row['name'] == 'season')
    assert winter['zero_support_cells'] == 26 and winter['absent_cells'] == 0
    ratio_only = next(row for row in report['unavailable_score_cells'] if row['table'] == 'local_hour_summaries')
    assert ratio_only['raw_mean_daily_loss'] == 10. and ratio_only['unavailable_parts'] == ['B0_ratio']
    assert any(row['row_id'] == ratio_only['row_id'] for row in packet['descriptive_support']['unavailable_score_cells'])
    empty = next(row for row in report['empty_breakdown_cells'] if row['mask'] == 'newly_opened' and row['group'] == 'season' and row['value'] == 'DJF')
    text = Path(result['paths']['report.md']).read_text()
    assert '| newly_opened | season | DJF |' in text
    assert '| newly_opened | canonical_hours | 23 |' in text and '| newly_opened | canonical_hours | 25 |' in text
    assert empty['source_rows'][0]['row_id'] in text and 'full refs in report.json' in text
    assert any(row.get('coverage50') is None and row['status'] == 'unavailable'
               for row in report['diagnostic_tables']['coverage'])
