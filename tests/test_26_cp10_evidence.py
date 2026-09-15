"""Independently recompute committed comparison evidence, with corruption controls."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

OUT=Path(__file__).resolve().parents[1]/'reports/cp10'
QUANTILES=np.array([.025,.05,.10,.25,.50,.75,.90,.95,.975])
LABELS=['p025','p05','p10','p25','p50','p75','p90','p95','p975']


def check_evidence(predictions,metrics):
    for (candidate,fold),rows in predictions.groupby(['candidate','fold']):
        reported=metrics.loc[metrics.candidate.eq(candidate)&metrics.fold.eq(fold)].iloc[0]
        q=rows[[f'final_{label}' for label in LABELS]].to_numpy()
        y=rows.y_true.to_numpy()
        err=y[:,None]-q
        assert np.isfinite(q).all()
        assert np.all(np.diff(q,axis=1)>=0)
        expected=np.maximum(QUANTILES*err,(QUANTILES-1)*err).mean()
        assert reported.mean_pinball==pytest.approx(expected,rel=1e-13,abs=1e-13)
        assert reported.mae==pytest.approx(np.abs(y-q[:,4]).mean(),rel=1e-13)
        for name,lo,hi in [('50',3,5),('80',2,6),('95',0,8)]:
            assert reported[f'coverage_{name}']==pytest.approx(((y>=q[:,lo])&(y<=q[:,hi])).mean(),abs=1e-15)
        assert reported.n_obs==len(q)
        assert reported.covered_95==((y>=q[:,0])&(y<=q[:,8])).sum()
        assert reported.crossings==0


def test_full_table_predictions_and_independent_metrics_with_corruption_control():
    predictions=pd.read_parquet(OUT/'predictions.parquet')
    metrics=pd.read_csv(OUT/'metrics.csv')
    protocol=json.loads((OUT/'protocol.json').read_text())
    expected=set(protocol['candidate_order'])|{'v1_reference'}
    assert set(predictions.candidate)==set(metrics.candidate)==expected
    assert len(metrics)==len(expected)*5
    assert all(set(g.fold)=={f'fold_{i}' for i in range(1,6)} for _,g in metrics.groupby('candidate'))
    check_evidence(predictions,metrics)
    corrupt=metrics.copy(); corrupt.loc[0,'mean_pinball']+=1
    with pytest.raises(AssertionError):
        check_evidence(predictions,corrupt)
    corrupt_predictions=predictions.copy(); corrupt_predictions.loc[0,'final_p025']=1e9
    with pytest.raises(AssertionError):
        check_evidence(corrupt_predictions,metrics)


def test_selection_recomputed_from_hourly_losses_and_peak_denominator():
    predictions=pd.read_parquet(OUT/'predictions.parquet')
    decision=json.loads((OUT/'selection.json').read_text())
    protocol=json.loads((OUT/'protocol.json').read_text())
    eligible=predictions.loc[predictions.fold.isin(['fold_1','fold_2','fold_4','fold_5'])]
    scores={}
    for candidate in protocol['candidate_order']:
        rows=eligible.loc[eligible.candidate.eq(candidate)]
        residual=rows.y_true.to_numpy()[:,None]-rows[[f'final_{l}' for l in LABELS]].to_numpy()
        scores[candidate]=float(np.maximum(QUANTILES*residual,(QUANTILES-1)*residual).mean())
        assert scores[candidate]==pytest.approx(decision['pooled_mean_pinball'][candidate],rel=1e-14)
        assert len(rows)==decision['selection_n_obs']==8635
    winner=min(protocol['candidate_order'],key=scores.__getitem__)
    assert winner==decision['selected_candidate']
    peak=pd.read_csv(OUT/'peak_windows.csv')
    assert set(peak.candidate)==set(predictions.candidate)
    assert peak.n_obs.tolist()==[408]*7
    assert peak.n_days.tolist()==[17]*7
    for _,record in peak.iterrows():
        rows=predictions.loc[predictions.candidate.eq(record.candidate)&predictions.fold.eq('fold_3')]
        dates=pd.to_datetime(rows.delivery_date)
        rows=rows.loc[dates.between('2022-08-15','2022-08-31')]
        coverage=((rows.y_true>=rows.final_p025)&(rows.y_true<=rows.final_p975))
        assert record.covered_95==coverage.sum()
        assert record.coverage_95==pytest.approx(coverage.mean(),abs=1e-15)
    assert peak.loc[peak.candidate.eq('v1_reference'),'covered_95'].iloc[0]==79
    # Mutating diagnostic losses must not enter the independent selection input.
    changed=predictions.copy(); changed.loc[changed.fold.eq('fold_3'),'y_true']=1e9
    pd.testing.assert_frame_equal(changed.loc[changed.fold.isin(['fold_1','fold_2','fold_4','fold_5'])],eligible)
    changed.loc[changed.fold.eq('fold_1'),'y_true']=1e9
    assert not changed.loc[changed.fold.eq('fold_1'),'y_true'].equals(eligible.loc[eligible.fold.eq('fold_1'),'y_true'])


def test_falsification_is_bound_to_reported_full_fold_and_both_branches_tested_elsewhere():
    decision=json.loads((OUT/'selection.json').read_text()); outcome=decision['falsification']
    metrics=pd.read_csv(OUT/'metrics.csv')
    row=metrics.loc[metrics.candidate.eq(decision['selected_candidate'])&metrics.fold.eq('fold_3')].iloc[0]
    assert outcome['n_obs']==row.n_obs==2112
    assert outcome['window_start']=='2022-07-01' and outcome['window_end']=='2022-09-28'
    assert outcome['covered_95']==row.covered_95
    assert outcome['fix_worked']==bool(row.coverage_95>=.394)
    if not outcome['fix_worked']:
        assert outcome['recommended_frozen_artifact']=='v1'


def test_provenance_inputs_sources_and_v1_replay():
    root=OUT.parents[1]
    lineage=json.loads((OUT/'lineage.json').read_text())
    for path,expected in {**lineage['input_sha256'],**lineage['source_sha256']}.items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest()==expected
    assert hashlib.sha256((OUT/'protocol.json').read_bytes()).hexdigest()==lineage['protocol_sha256']
    assert all(f['v1_replay_max_abs_difference']==0.0 for f in lineage['folds'])
    original=pd.read_parquet(root/'reports/cp2/development_predictions.parquet')
    reference=pd.read_parquet(OUT/'predictions.parquet')
    keys=['fold','delivery_date','y_true']+[f'final_{l}' for l in LABELS]
    left=original.loc[original.arm.eq('base'),keys].sort_values(keys[:3]).reset_index(drop=True)
    right=reference.loc[reference.candidate.eq('v1_reference'),keys].sort_values(keys[:3]).reset_index(drop=True)
    pd.testing.assert_frame_equal(left,right)
    altered=right.copy(); altered.loc[0,'final_p025']+=1
    with pytest.raises(AssertionError):
        pd.testing.assert_frame_equal(left,altered)
    assert pd.Timestamp(lineage['latest_price_timestamp'])<pd.Timestamp('2026-04-08',tz='Europe/Berlin')
