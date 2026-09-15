"""Reproduce CP-10 from preserved development predictions, without model fitting.

    uv run --frozen python scripts/cp10_calibration.py --output /tmp/cp10-repro
Only development windows are read as price inputs. Outputs must be outside v1.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from delu_forecast.calibration_comparison import (
    CANDIDATES, GAMMA_GRID, SELECTION_FOLDS, aci_predict, falsification,
    fit_scaled, fully_observed_days, head_spread, predict_scaled, price_volatility,
    select_candidate,
)
from delu_forecast.conformal import fit_cqr_thresholds
from delu_forecast.features import build_feature_catalog
from delu_forecast.folds import load_partition_spec, window_mask
from delu_forecast.metrics import crossing_violations, summarize
from delu_forecast.postprocess import QUANTILE_LABELS, cqr_then_isotonic

ROOT = Path(__file__).resolve().parents[1]
RAW = [f'raw_{label}' for label in QUANTILE_LABELS]
FINAL = [f'final_{label}' for label in QUANTILE_LABELS]
PROTOCOL = ROOT / 'reports/cp10/protocol.json'


def write_json(path, value):
    path.write_text(json.dumps(value,indent=2,sort_keys=True,allow_nan=False)+'\n')


def load_development():
    protocol = json.loads(PROTOCOL.read_text())
    for name, expected in protocol['input_sha256'].items():
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != expected:
            raise ValueError(f'pre-registered input hash mismatch: {name}')
    if tuple(protocol['candidate_order']) != CANDIDATES or tuple(protocol['aci_gamma_grid']) != GAMMA_GRID:
        raise ValueError('implementation differs from pre-run candidate/grid freeze')
    spec=load_partition_spec(ROOT/'data/partitions.json')
    # Parquet predicate excludes all reserved tail data before feature building.
    cutoff=spec.eda_cutoff
    snapshot=pd.read_parquet(ROOT/'data/snapshot.parquet',filters=[('delivery_date','<=',cutoff)])
    days=pd.Index(snapshot.delivery_date)
    if any(days > cutoff):
        raise AssertionError('reserved rows entered development')
    index=pd.DatetimeIndex(snapshot.timestamp_utc)
    features=build_feature_catalog(snapshot,'base')
    eligible=features.notna().all(axis=1).to_numpy() & np.isfinite(snapshot.price_eur_mwh.to_numpy())
    price=pd.Series(snapshot.price_eur_mwh.to_numpy(),index=index)
    cal=pd.read_parquet(ROOT/'reports/cp2/development_calibration_predictions.parquet')
    ev=pd.read_parquet(ROOT/'reports/cp2/development_predictions.parquet')
    cal=cal.loc[cal.arm.eq('base')].copy(); ev=ev.loc[ev.arm.eq('base')].copy()
    # These v1 records omit timestamp. Reconstruct from the original eligibility
    # rule and verify dates + every target, not a guessed hour-per-day ordinal.
    aligned=[]
    for fold in spec.development_folds:
        slices=[]
        for frame,window in ((cal,fold.calibration),(ev,fold.evaluation)):
            part=frame.loc[frame.fold.eq(fold.name)].reset_index(drop=True)
            mask=window_mask(days,window)&eligible
            if len(part)!=mask.sum() or not np.array_equal(part.delivery_date.to_numpy(),days[mask].to_numpy()) or not np.array_equal(part.y_true.to_numpy(),price.to_numpy()[mask]):
                raise AssertionError(f'preserved-row lineage mismatch: {fold.name}')
            part['timestamp_utc']=index[mask]
            slices.append(part)
        aligned.append((fold,*slices))
    return protocol,price,aligned


def run(output: Path):
    output=output.resolve()
    forbidden=[ROOT/'reports/cp2',ROOT/'models',ROOT/'data',ROOT/'docs/track-b/evidence']
    if any(output==p or p in output.parents for p in forbidden) or output==ROOT:
        raise ValueError('output would overlap protected evidence or repository root')
    protocol,price,folds=load_development()
    output.mkdir(parents=True,exist_ok=True)
    observed=fully_observed_days(price)
    metrics=[]; prediction_frames=[]; traces=[]; peak=[]; lineage=[]
    # Selection folds are evaluated first, then the diagnostic fold; the selection
    # function never consumes fold_3 even after its results exist.
    ordered=sorted(folds,key=lambda item:item[0].name=='fold_3')
    for fold,cal,ev in ordered:
        calraw=cal[RAW].to_numpy(); raw=ev[RAW].to_numpy()
        cy=cal.y_true.to_numpy(); y=ev.y_true.to_numpy(); days=pd.Index(ev.delivery_date)
        v1=cqr_then_isotonic(raw,fit_cqr_thresholds(calraw,cy))
        if not np.array_equal(v1,ev[FINAL].to_numpy()):
            raise AssertionError(f'v1 development replay differs: {fold.name}')
        results={'v1_reference':v1}
        for name,cs,es in [
            ('c1_head_spread',head_spread(calraw),head_spread(raw)),
            ('c1_price_volatility',price_volatility(price,pd.Index(cal.delivery_date)),price_volatility(price,days)),
        ]:
            results[name]=predict_scaled(raw,fit_scaled(calraw,cy,cs),es)
        for gamma in GAMMA_GRID:
            name=f'c2_aci_gamma_{gamma}'
            results[name],trace=aci_predict(calraw,cy,raw,days,y,gamma=gamma,observed_days=observed)
            trace.insert(0,'fold',fold.name); trace.insert(0,'candidate',name); traces.append(trace)
        for candidate,pred in results.items():
            if not np.isfinite(pred).all() or crossing_violations(pred)!=0:
                raise AssertionError(f'nonfinite/crossing output: {fold.name}/{candidate}')
            row={'candidate':candidate,'fold':fold.name,**summarize(y,pred),
                 'crossings':crossing_violations(pred),'n_days':len(days.unique()),
                 'window_start':str(fold.evaluation.start),'window_end':str(fold.evaluation.end),
                 'covered_95':int(((y>=pred[:,0])&(y<=pred[:,8])).sum())}
            metrics.append(row)
            frame=ev[['fold','timestamp_utc','delivery_date','y_true']].copy()
            frame.insert(0,'candidate',candidate); frame[FINAL]=pred
            prediction_frames.append(frame)
            if fold.name=='fold_3':
                mask=(pd.to_datetime(days)>=pd.Timestamp('2022-08-15')) & (pd.to_datetime(days)<=pd.Timestamp('2022-08-31'))
                peak.append({'candidate':candidate,'window_start':'2022-08-15','window_end':'2022-08-31',
                             **summarize(y[mask],pred[mask]),'n_days':len(days[mask].unique()),
                             'covered_95':int(((y[mask]>=pred[mask,0])&(y[mask]<=pred[mask,8])).sum())})
        lineage.append({'fold':fold.name,'calibration_rows':len(cal),'evaluation_rows':len(ev),
                        'eligible_evaluation_days':len(days.unique()),'calendar_evaluation_days':(fold.evaluation.end-fold.evaluation.start).days+1,
                        'v1_replay_max_abs_difference':float(np.max(abs(v1-ev[FINAL].to_numpy())))})
        print(f'{fold.name}: {len(cal)} calibration / {len(ev)} evaluation rows; 7 methods; zero crossings',flush=True)
    table=pd.DataFrame(metrics).sort_values(['candidate','fold']).reset_index(drop=True)
    winner,scores=select_candidate(table)
    rule_row=table.loc[table.candidate.eq(winner)&table.fold.eq('fold_3')].iloc[0]
    outcome=falsification(float(rule_row.coverage_95))
    outcome.update({'window_start':str(rule_row.window_start),'window_end':str(rule_row.window_end),
                    'n_obs':int(rule_row.n_obs),'n_days':int(rule_row.n_days),'covered_95':int(rule_row.covered_95),
                    'window_note':'Full eligible fold_3 block, as §4.2 rule 5 specifies. The literal 0.194 is from the shorter historical August peak subset; peak_windows.csv reports that same subset separately.'})
    selection={'selected_candidate':winner,'selected_aci_gamma':min(GAMMA_GRID,key=lambda g:scores[f'c2_aci_gamma_{g}']),
               'selection_folds':list(SELECTION_FOLDS),'selection_n_obs':int(table.loc[table.candidate.eq(winner)&table.fold.isin(SELECTION_FOLDS)].n_obs.sum()),
               'pooled_mean_pinball':scores,'tie_order':list(CANDIDATES),'falsification':outcome,
               'evidence_class':protocol['evidence_class'],'c3':protocol['c3_rejection']}
    table.to_csv(output/'metrics.csv',index=False)
    pd.DataFrame(peak).to_csv(output/'peak_windows.csv',index=False)
    pd.concat(prediction_frames,ignore_index=True).to_parquet(output/'predictions.parquet',index=False)
    pd.concat(traces,ignore_index=True).to_csv(output/'aci_trace.csv',index=False)
    write_json(output/'selection.json',selection)
    write_json(output/'lineage.json',{'folds':lineage,'input_sha256':protocol['input_sha256'],
               'protocol_sha256':hashlib.sha256(PROTOCOL.read_bytes()).hexdigest(),
               'source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['src/delu_forecast/calibration_comparison.py','scripts/cp10_calibration.py']},
               'price_rows_read':len(price),'latest_price_timestamp':str(price.index.max()),
               'attribution':'SMARD.de, Bundesnetzagentur, CC BY 4.0; data/source_manifest.json and data/README.md retain source-level attribution; no new data pull.',
               'new_model_fits':0,'holdout_evaluations':0,'external_writes':0})
    print(json.dumps(selection,indent=2,sort_keys=True),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,default=ROOT/'reports/cp10')
    run(parser.parse_args().output)
