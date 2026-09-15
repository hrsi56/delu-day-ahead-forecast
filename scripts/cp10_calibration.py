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
    index=pd.DatetimeIndex(snapshot.timestamp_utc).tz_convert('UTC')
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


def write_report(output, table, peak, selection, lineage):
    winner=selection['selected_candidate']
    scores=selection['pooled_mean_pinball']
    reference=table.loc[table.candidate.eq('v1_reference') & table.fold.isin(SELECTION_FOLDS)]
    v1_score=float(np.dot(reference.n_obs,reference.mean_pinball)/reference.n_obs.sum())
    crisis=table.loc[table.candidate.eq(winner)&table.fold.eq('fold_3')].iloc[0]
    old=table.loc[table.candidate.eq('v1_reference')&table.fold.eq('fold_3')].iloc[0]
    peak_table=pd.DataFrame(peak)
    peak_new=peak_table.loc[peak_table.candidate.eq(winner)].iloc[0]
    peak_old=peak_table.loc[peak_table.candidate.eq('v1_reference')].iloc[0]
    lines=[
        '# CP-10 — development calibration comparison', '',
        f"Selected: **{winner}**, pooled mean pinball **{scores[winner]:.9f}** on "
        f"**{selection['selection_n_obs']:,} observations** from folds 1, 2, 4 and 5. "
        f"v1 reference: {v1_score:.9f}. This is development evidence, not a new holdout result.", '',
        '## Falsification: distinguish the two windows', '',
        f"The literal full-fold rule in v20 §4.2(5) is evaluated on 2022-07-01 through "
        f"2022-09-28: **{int(crisis.covered_95)} / {int(crisis.n_obs)} = {crisis.coverage_95:.9f}** "
        f"95% coverage, versus its fixed 0.394 threshold. Result: **{selection['falsification']['result']}**. "
        'The denominator is 2,112 eligible hours on 88 represented days within the 90-day calendar block.', '',
        "**This does not establish that the original peak-week collapse is fixed.** The plan\'s "
        '0.194 baseline comes from August 15–31, not the full fold. '
        f"On that same 408-hour / 17-day subset, the selected method covers **{int(peak_new.covered_95)}/408 "
        f"({peak_new.coverage_95:.9f})**, versus v1 **{int(peak_old.covered_95)}/408 "
        f"({peak_old.coverage_95:.9f})**: **{100*(peak_new.coverage_95-peak_old.coverage_95):.3f} percentage points** "
        'of improvement. This falls short of 20 points. Relative to the literal rounded 0.194, '
        f"the improvement is {peak_new.coverage_95-.194:.9f}, also below 0.20.", '',
        f"The matched full-fold change is {crisis.coverage_95-old.coverage_95:.9f}, "
        f"from v1\'s {old.coverage_95:.9f}; v1 itself already clears the literal 0.394 full-fold threshold. "
        'Both comparisons are disclosed rather than treating different denominators as the same experiment. '
        'The same-window diagnostic does not alter selection or replace the pre-run full-fold rule. '
        '**The original peak-week defect remains unresolved; retain v1 as the currently recommended frozen artifact.** '
        'No v2 artifact was frozen, promoted or evaluated on a holdout, and no 90-day clock started.', '',
        '## All candidates, including losers', '',
        'C-1 head spread, C-1 trailing price volatility and all four frozen C-2 gamma settings are shown. '
        'v1 is a reference, outside the candidate set. Lower pooled pinball wins; exact ties follow the order below. '
        'The nine quantile losses are equally weighted within each observation; observations are pooled, not fold means averaged.', '',
        '| Candidate | Selection pooled pinball | fold_3 pinball | fold_3 coverage95 | Peak coverage95 |',
        '|---|---:|---:|---:|---:|',
    ]
    for name in ('v1_reference',*CANDIDATES):
        row=table.loc[table.candidate.eq(name)&table.fold.eq('fold_3')].iloc[0]
        pk=peak_table.loc[peak_table.candidate.eq(name)].iloc[0]
        lines.append(f"| {name} | {scores.get(name,v1_score):.9f} | {row.mean_pinball:.9f} | {row.coverage_95:.9f} | {pk.coverage_95:.9f} |")
    lines += ['', '### Full five-fold table', '',
              '| Candidate | Fold | Hours | MAE | Pinball | Coverage50 | Coverage80 | Coverage95 | Crossings |',
              '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for row in table.itertuples():
        lines.append(f"| {row.candidate} | {row.fold} | {int(row.n_obs)} | {row.mae:.6f} | {row.mean_pinball:.6f} | {row.coverage_50:.6f} | {row.coverage_80:.6f} | {row.coverage_95:.6f} | {row.crossings} |")
    lines += ['', '## Frozen implementation choices and limitations', '',
        '- `protocol.json` was committed at `5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed`, before calibration implementation or comparison execution. No parameter changed after viewing candidate results.',
        '- C-1 normalises signed conformity scores before the exact one-based order statistic, then multiplies by the prediction-row scale. Raw spread is `raw_p95 - raw_p05`, without sorting heads first. Both scales have a fixed 1 EUR/MWh floor. Trailing volatility uses sample standard deviation of exactly 168 canonical hours ending before local delivery-day midnight. This is the inherited D-1 day-ahead price boundary, independently controlled with D masking and a D-1 mutation.',
        '- C-2 uses one coverage state per symmetric pair: `c = 1 - paper_alpha`. With `target = nominal coverage`, `c += gamma * (target - hit)` is the exact equation in v20. It is algebraically the complement of the paper\'s miscoverage update. Each released hourly hit is applied once; all hours in one delivery day receive the same pre-origin state. The reference score reservoir is the initial unscaled calibration slice and stays fixed.',
        '- C-2 only releases previously emitted predictions for delivery days through D-2, after validating complete 23/24/25-hour daily price availability. It does not use calibration outcomes as adaptive replay, embargo-day predictions, D-1 feedback or same-day feedback. The last two evaluation days have no feedback consumer within the fold. `aci_trace.csv` records each origin\'s cutoff, cumulative feedback count, coverage states and ranks.',
        '- Gamma grid: 0.000001, 0.000005, 0.00001, 0.00002 per hourly feedback event. The upper bound is deliberately conservative: even 2,161 consecutive misses keep the 95% state below 0.991059, within finite ranks for these calibration samples. No state or rank clipping is used. This does not test rapidly adapting ACI or a rolling score reservoir; the null crisis result cannot rule out those variants. No delayed long-run coverage guarantee is claimed.',
        '- Isotonic regression is last, including before deciding which previously emitted intervals covered their realised labels. Small median changes can arise from the final projection; no point-forecast improvement is the claim.',
        '- C-3 is rejected and not implemented, exactly as §4.3 requires: a regime taxonomy based on hindsight dates violates the anti-overtuning rule. No crisis flag or hindsight date threshold is supplied to a calibrator. The two fixed August dates appear only in the reporting diagnostic inherited from v1.',
        '- Prices, forecasts and eligibility are inherited from the frozen v1 development evidence. Inputs were not refit or reselected. Every saved target/date is matched to the original base-feature eligibility mask, and v1\'s saved final vectors replay with maximum absolute difference exactly 0.0. `lineage.json` contains input/source hashes, row counts and the latest price timestamp. The data loader filters before the reserved tail partitions.', '',
        '## Verification and reproduction', '',
        'Run from the repository root with the pinned `uv.lock`:', '',
        '```sh',
        'uv run --frozen pytest -q',
        'uv run --frozen python scripts/cp10_calibration.py --output /tmp/cp10-repro',
        '```', '',
        'For a fresh checkout, first materialise the ignored v1 browser payload required by the existing regression suite. '
        'This performs frozen-model identity replay, not a new holdout performance evaluation; the tracked v1 manifest is redirected to a temporary file:', '',
        '```sh',
        "uv run --frozen python - <<'PY'",
        'from pathlib import Path',
        'import runpy',
        'ns = runpy.run_path("scripts/build_wasm_payload.py", run_name="cp10_test_setup")',
        'ns["main"].__globals__["MANIFEST"] = Path("/tmp/cp10-payload-manifest.json")',
        'raise SystemExit(ns["main"]())',
        'PY',
        '```', '',
        'The second command emits `metrics.csv`, `peak_windows.csv`, `predictions.parquet`, `aci_trace.csv`, '
        '`selection.json`, `lineage.json` and this `report.md`. Compare each file byte-for-byte with '
        '`reports/cp10/`. `protocol.json` is the pre-run input, not regenerated output. All computation is local CPU; '
        'no credentials, network requests, experiment writes or new dependencies are needed.', '',
        'Exact and adversarial tests are in `tests/test_25_cp10_calibration.py`; independent recomputation from '
        'every emitted prediction is in `tests/test_26_cp10_evidence.py`. Existing unscaled rank fixtures '
        '(`test_10`), schema firewall controls (`test_05`), and feature/champion masking controls '
        '(`test_02`, `test_13`) remain in the complete suite. Every new negative behavioural assertion '
        'has a matching mutation, accepted input or corruption control. The pre-review baseline suite had 191 passing tests.', '',
        'The first driver attempt was interrupted before any candidate metrics when mixed UTC timezone representations '
        'caused repeated pandas object-index hashing. Normalising the driver\'s timestamp index to UTC fixed the '
        'performance issue without changing instants, inputs, formulas or parameters. Completed reproduction runs '
        'are deterministic. This report is generated by `scripts/cp10_calibration.py`.', '',
        '## Sources and evidence class', '',
        'Data: Bundesnetzagentur / SMARD.de, CC BY 4.0. Attribution and the frozen ingestion record remain '
        'in `data/README.md` and `data/source_manifest.json`. No data were downloaded for CP-10.', '',
        'ACI equation reference: [Gibbs and Candès (2021), §2, equation (2)]'
        '(https://arxiv.org/html/2106.00170v3). The coverage-state complement is an algebraic implementation '
        'choice documented above; the conservative grid and delayed fixed-reservoir experiment are this '
        'checkpoint\'s choices, not claims attributed to the paper.', '',
        'All results here are development calibration evidence. The preserved v1 report, point-MAE p=0.948, '
        'holdout evidence, champion, snapshot, partition manifest, closed experiment and release/evidence tags '
        'are untouched. Integration acceptance is recorded separately in the checkpoint verdict.', '']
    (output/'report.md').write_text('\n'.join(lines))


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
    peak_df=pd.DataFrame(peak)
    selected_peak=peak_df.loc[peak_df.candidate.eq(winner)].iloc[0]
    reference_peak=peak_df.loc[peak_df.candidate.eq('v1_reference')].iloc[0]
    selection['same_window_diagnostic']={
        'window_start':'2022-08-15','window_end':'2022-08-31','n_obs':408,
        'selected_coverage_95':float(selected_peak.coverage_95),
        'v1_coverage_95':float(reference_peak.coverage_95),
        'absolute_improvement':float(selected_peak.coverage_95-reference_peak.coverage_95),
        'clears_20_percentage_point_improvement':bool(selected_peak.coverage_95-reference_peak.coverage_95>=.20),
        'interpretation':'The original peak-week defect remains unresolved; literal full-fold rule-5 clearance must not be read as fixing that defect.',
        'recommended_frozen_artifact':'v1',
        'selection_influence':'none; reported diagnostic only'}
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
    write_report(output,table,peak,selection,lineage)
    print(json.dumps(selection,indent=2,sort_keys=True),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,default=ROOT/'reports/cp10')
    run(parser.parse_args().output)
