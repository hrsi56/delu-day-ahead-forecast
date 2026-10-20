"""Complete descriptive-cell fixtures; no production outcomes or estimators."""
from datetime import date
from itertools import product

import pandas as pd
import pytest

from cp26 import analysis as A, reporting as R, scoring as S


def complete_table(name):
    """Declared synthetic constants on the independent public cell registry."""
    rows = []
    for mask, stream in product(S.MASKS, S.RESEARCH_STREAMS):
        if name == 'local_hour_summaries':
            cells = ({'local_hour': hour, 'metric': metric} for hour, metric in product(range(24), ('MAE', 'WIS')))
        elif name == 'summaries':
            cells = ({'group': group, 'value': value, 'metric': metric}
                     for (group, value), metric in product(S.registered_breakdown_cells(), ('MAE', 'WIS')))
        else:
            tail, values = {'coverage': ('interval', (50, 80, 95)),
                            'quantile_hits': ('quantile', S.QUANTILES), 'histogram': ('bin', range(8))}[name]
            cells = ({'group': group, 'value': value, tail: value_tail}
                     for (group, value), value_tail in product(S.registered_breakdown_cells(include_local_hours=True), values))
        for cell in cells:
            row = {'mask': mask, 'stream': stream, **cell, 'status': 'computable', 'reason': None,
                   'n_dates': 1, 'n_hours': 24, 'calendar_dates': 1}
            if name in ('summaries', 'local_hour_summaries'):
                row.update(raw_mean_daily_loss=10., B0_ratio=1., raw_available_dates=1, paired_dates=1,
                           paired_B0_loss=10., ratio_status='computable', ratio_undefined_reason=None)
            elif name == 'coverage':
                for level in (50, 80, 95):
                    row[f'coverage{level}'], row[f'width{level}'] = .8, 20.
            rows.append(row)
    return pd.DataFrame(rows)


@pytest.fixture(scope='module')
def complete():
    return {name: complete_table(name) for name in ('summaries', 'local_hour_summaries',
                                                   'coverage', 'quantile_hits', 'histogram')}


def test_fixed_universe_counts_independent_of_observed_support(complete):
    expected = {'summaries': 5096, 'local_hour_summaries': 2496, 'coverage': 11388,
                'quantile_hits': 26572, 'histogram': 30368}
    assert len(S.registered_breakdown_cells()) == 49
    assert len(S.registered_breakdown_cells(include_local_hours=True)) == 73
    for name, frame in complete.items():
        assert A.validate_registered_table(name, frame)['cells'] == expected[name]
        unavailable = frame.copy()
        unavailable['status'], unavailable['reason'] = 'unavailable', 'no_calendar_support'
        unavailable['n_hours'], unavailable['n_dates'], unavailable['calendar_dates'] = 0, 0, 0
        assert A.validate_registered_table(name, unavailable) == A.validate_registered_table(name, frame)


@pytest.mark.parametrize('name', ['summaries', 'local_hour_summaries', 'coverage', 'quantile_hits', 'histogram'])
@pytest.mark.parametrize('mutation', ['omitted', 'substituted', 'duplicated'])
def test_complete_contract_refuses_omitted_substituted_or_duplicate_identity(complete, name, mutation):
    frame = complete[name].copy()
    if mutation == 'omitted':
        frame = frame.iloc[1:]
    elif mutation == 'substituted':
        frame.at[0, 'stream'] = 'nominal/unregistered'
    else:
        frame = pd.concat([frame.iloc[1:], frame.iloc[[1]]], ignore_index=True)
    with pytest.raises(ValueError, match=f'registered {name} inventory differs'):
        A.validate_registered_table(name, frame)


def test_missing_whole_registered_table_is_refused(complete):
    with pytest.raises(ValueError, match='score inventory lacks required tables'):
        A.validate_score_tables({'summaries': complete['summaries']})
    with pytest.raises(ValueError, match='calibration inventory lacks required tables'):
        A.validate_calibration_tables({'coverage': complete['coverage']})


def test_rehashed_omitted_summary_fails_score_load(tmp_path, monkeypatch, complete):
    protocol, code = {'fixture': 'protocol'}, {'fixture': 'code'}
    days = [day.date() for day in pd.date_range('2020-12-29', '2026-09-06')]
    daily = pd.DataFrame((stream, day) for stream, day in product(S.RESEARCH_STREAMS, days))
    daily.columns = ['stream', 'delivery_date']
    tables = {'daily': A._table(tmp_path, 'daily', daily, keys=('stream', 'delivery_date'))}
    for name in ('summaries', 'local_hour_summaries'):
        frame = complete[name].iloc[1:] if name == 'summaries' else complete[name]
        tables[name] = A._table(tmp_path, name, frame, keys=A.registered_table_keys(name))
    manifest = A._signed({'schema': A.SCORE_SCHEMA, 'status': 'COMPLETE', 'protocol': protocol,
        'code_sha256': code, 'streams': list(S.RESEARCH_STREAMS), 'masks': list(S.MASKS),
        'forecast_days': 2441, 'tables': tables, 'registered_score_inventory': A.validate_score_tables(complete)})
    A._immutable(tmp_path / A.OUTPUT / 'scores-manifest.json', manifest)
    monkeypatch.setattr(A, '_code', lambda _: code)
    with pytest.raises(ValueError, match='registered summaries inventory differs'):
        A.load_scores(tmp_path, protocol)


def test_rehashed_omitted_calibration_fails_completed_resume(tmp_path, complete):
    protocol, code, score = {'fixture': 'protocol'}, {'fixture': 'code'}, {'content_sha256': 'a' * 64}
    tables = {}
    for name in ('coverage', 'quantile_hits', 'histogram'):
        frame = complete[name].iloc[1:] if name == 'coverage' else complete[name]
        tables[name] = A._table(tmp_path, name, frame, keys=A.registered_table_keys(name))
    value = {'status': 'COMPLETE', 'protocol': protocol, 'code_sha256': code,
        'scores_manifest_sha256': score['content_sha256'], 'tables': tables,
        'registered_calibration_inventory': A.validate_calibration_tables(complete),
        'moment_family': {'cells': [{'endpoint_id': f'fixture-{i}'} for i in range(936)], 'holm': [{}] * 936}}
    with pytest.raises(ValueError, match='registered coverage inventory differs'):
        A._validate_completed(tmp_path, 'diagnostics', value, protocol, score, code)


def test_report_refuses_omitted_cell_before_writing_artifacts(tmp_path, complete):
    scores = {'daily': pd.DataFrame(), 'hourly': pd.DataFrame(),
              'summaries': complete['summaries'], 'local_hour_summaries': complete['local_hour_summaries'],
              'secondary_summaries': pd.DataFrame(), 'fallbacks': pd.DataFrame(), 'population_evidence': {}}
    diagnostics = {'tables': {name: complete[name] for name in ('coverage', 'quantile_hits', 'histogram')}}
    diagnostics['tables']['histogram'] = complete['histogram'].iloc[1:]
    with pytest.raises(ValueError, match='registered histogram inventory differs'):
        R.build_report(tmp_path, None, scores, {'endpoints': []}, diagnostics, {}, {'fixture': 'protocol'})
    assert not (tmp_path / R.OUTPUT / 'report.json').exists()


def test_support_disclosure_separates_empty_raw_cells_from_unavailable_ratio(complete):
    scores = {name: R._catalog(name, complete[name]) for name in ('summaries', 'local_hour_summaries')}
    diagnostics = {name: R._catalog(name, complete[name]) for name in ('coverage', 'quantile_hits', 'histogram')}
    for rows in (*scores.values(), *diagnostics.values()):
        for row in rows:
            if row['mask'] == 'newly_opened' and row.get('group') == 'season' and row.get('value') == 'DJF':
                row.update(status='unavailable', reason='no_calendar_support', n_hours=0, n_dates=0,
                           raw_available_dates=0, calendar_dates=0, raw_mean_daily_loss=None, B0_ratio=None)
    counts = R._breakdown_support(scores, diagnostics)
    winter = next(row for row in counts if row['mask'] == 'newly_opened' and row['name'] == 'season')
    assert winter['zero_support_cells'] == 26 and winter['supported_cells'] == 78 and winter['absent_cells'] == 0
    empty = R._empty_breakdowns(scores, diagnostics)
    cell = next(row for row in empty if row['mask'] == 'newly_opened' and row['group'] == 'season' and row['value'] == 'DJF')
    assert cell['reasons'] == ['no_calendar_support'] and len(cell['source_rows']) == 260
    supported = dict(scores['local_hour_summaries'][0], B0_ratio=None, ratio_status='unavailable',
                     ratio_undefined_reason='zero_or_nonfinite_B0_denominator')
    unavailable = R._score_unavailable('local_hour_summaries', supported)
    assert unavailable['unavailable_parts'] == ['B0_ratio'] and supported['raw_mean_daily_loss'] == 10.
