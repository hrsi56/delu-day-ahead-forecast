# Verdict — CP-10 — Integration — PASS

- Candidate SHA: `ad3e1a5d5e42d70ea95bbffd01b4563eb2d6d803`
- Plan / version / bar: `capstone_v20.md`, version 20, ratified 2026-09-15; §9 complete CP-10 row, supported by §4 in full and §§3,13.
- Verbatim bar excerpt, confirmed in the committed plan at the candidate SHA:
  > All §4.3 candidates implemented with exact fixtures; selection on folds {1,2,4,5} only; the full table including fold_3 for **every** candidate **including the losers**; rule-5 falsification evaluated and reported whichever way it lands; zero crossings; a positive control on every negative assertion; C-2's two-day lag proved with the masking control rather than assumed
- The excerpt is the citation; line numbers are non-binding.
- Worktree: `/Users/djourno/Downloads/PJM-critic-cp-10`, fresh detached checkout supplied by the Lead. Worktree clean before and after: **yes**, `git status --porcelain=v1` emitted nothing both times. HEAD before and after: the full candidate SHA above. `git symbolic-ref -q HEAD` emitted nothing and returned 1, confirming detached HEAD.
- Isolation is cooperative, not a read-only mount. No repository source, tracked evidence, governance, input, model, or v1 report was written. Only ignored test setup byproducts and `/tmp` outputs were materialised. No refs were created, altered, or deleted; nothing was committed or published. The Lead owns removal of the supplied worktree.

## Commands actually run

All shell commands below ran in `/Users/djourno/Downloads/PJM-critic-cp-10`. Exit codes are actual outcomes; asynchronous polling only collected output from the same command and did not rerun it.

### Inspection and provenance commands

| Exact command | Exit | Observed output |
|---|---:|---|
| `git status --porcelain=v1 && git rev-parse HEAD` | 0 | Empty status; `ad3e1a5d5e42d70ea95bbffd01b4563eb2d6d803`. |
| `cat AGENTS.md` | 0 | Root router, bounded role, lockdown and Git constraints. |
| `rg -n '^#\|Integration\|Critic\|verdict' engineering-role.md docs/track-b/gauntlet-templates.md capstone_v20.md` | 0 | Located role protocol, canonical verdict form and plan sections. |
| `sed -n '54,73p' engineering-role.md && sed -n '68,123p' docs/track-b/gauntlet-templates.md` | 0 | Integration protocol and canonical §2 form. |
| `sed -n '148,246p' capstone_v20.md && sed -n '499,513p' capstone_v20.md && sed -n '579,640p' capstone_v20.md` | 0 | Complete §§3–4, CP-10 row, §13. No later checkpoint bar was inspected. |
| `wc -l src/delu_forecast/calibration_comparison.py scripts/cp10_calibration.py tests/test_25_cp10_calibration.py tests/test_26_cp10_evidence.py && cat reports/cp10/protocol.json reports/cp10/selection.json reports/cp10/lineage.json reports/cp10/report.md` | 0 | 180 / 263 / 240 / 111 lines; complete protocol, decisions, lineage and generated report. |
| `cat src/delu_forecast/calibration_comparison.py scripts/cp10_calibration.py` | 0 | Complete implementation and generator. |
| `cat tests/test_25_cp10_calibration.py tests/test_26_cp10_evidence.py` | 0 | Exact fixtures, temporal mutants and independent evidence checks. |
| `cat src/delu_forecast/conformal.py src/delu_forecast/postprocess.py src/delu_forecast/metrics.py && cat tests/test_10_conformal.py` | 1 | Three source modules read; guessed test filename did not exist. Correct file read below. |
| `rg --files tests \| rg 'test_02\|test_05\|test_13' && git log --format='%H %s' -4 && git show --stat --oneline 5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed && git diff --name-status 5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed..HEAD && cat data/partitions.json reports/cp2/catalog_selection.json` | 0 | Located inherited controls; protocol commit precedes implementation and evidence commits; only CP-10 additions; five development windows; preserved catalog is base. |
| `rg --files tests \| rg 'test_10' && cat tests/test_02_rolling_closed_left.py tests/test_05_schema_firewall.py tests/test_13_champion_no_delivery_day_leak.py` | 0 | Correct rank-test path and full inherited temporal/firewall controls. |
| `cat tests/test_10_cqr_order_statistic.py && git diff --name-status 5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed^..HEAD && git show 5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed:reports/cp10/protocol.json \| shasum -a 256 && shasum -a 256 reports/cp10/protocol.json && git merge-base --is-ancestor 5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed HEAD` | 1 | Rank fixture read; zsh rejected unquoted `^..HEAD` as a glob. Remaining commands did not execute; corrected below. |
| `git diff --name-status '5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed^..HEAD' && git show 5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed:reports/cp10/protocol.json \| shasum -a 256 && shasum -a 256 reports/cp10/protocol.json && git merge-base --is-ancestor 5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed HEAD` | 0 | Exactly 12 CP-10 added files, no modified/deleted files. Protocol hash identical at pre-run commit and HEAD: `ad1154ff33d3bcd946eae97b27a696391a09cf3505b12d3bb4695092c142e4e5`. Pre-run commit is an ancestor. |

### Reproduction and regression

Exact setup command, exit **0**:

```sh
uv run --frozen python - <<'PY'
from pathlib import Path
import runpy
ns = runpy.run_path('scripts/build_wasm_payload.py', run_name='cp10_test_setup')
ns['main'].__globals__['MANIFEST'] = Path('/tmp/cp10-critic-payload-manifest.json')
raise SystemExit(ns['main']())
PY
```

Observed: CPython 3.13.15; local `.venv` created with 117 pinned packages. Payload: 15,363,807 bytes across 14 files; series 7,248 rows; fixture 54 days / 1,296 rows, four fail-closed; temporary manifest written. This is the required existing frozen-model identity replay, including its existing holdout-named fixture regime, not a new holdout performance evaluation. The suite also fits small synthetic fixture models; CP-10 comparison performs no new production model fitting.

```sh
uv run --frozen pytest -q
```

Exit **0**; observed **217 passed in 51.34s**.

```sh
uv run --frozen python scripts/cp10_calibration.py --output /tmp/cp10-critic-repro
```

Exit **0**; observed:

```text
fold_1: 1440 calibration / 2160 evaluation rows; 7 methods; zero crossings
fold_2: 1437 calibration / 2159 evaluation rows; 7 methods; zero crossings
fold_4: 1436 calibration / 2160 evaluation rows; 7 methods; zero crossings
fold_5: 1440 calibration / 2156 evaluation rows; 7 methods; zero crossings
fold_3: 1440 calibration / 2112 evaluation rows; 7 methods; zero crossings
```

The emitted decision JSON selected `c1_price_volatility`, pooled mean pinball `4.385529023835001`, `selection_n_obs=8635`; all six candidate scores, full-fold falsification and matched peak diagnostic matched the committed decision.

```sh
uv run --frozen python - <<'PY'
from pathlib import Path
names=['metrics.csv','peak_windows.csv','predictions.parquet','aci_trace.csv','selection.json','lineage.json','report.md']
for name in names:
    assert (Path('reports/cp10')/name).read_bytes()==(Path('/tmp/cp10-critic-repro')/name).read_bytes(), name
print('7 generated artifacts match byte-for-byte')
PY
```

Exit **0**; observed `7 generated artifacts match byte-for-byte`.

### Critic's independent row and ACI-state audit

The following exact command uses NumPy/Pandas and rational arithmetic, without importing the calibration, selection or metric implementations:

```sh
uv run --frozen python - <<'PY'
import json, math
from datetime import timedelta
from fractions import Fraction
import numpy as np
import pandas as pd
from pathlib import Path
root=Path('reports/cp10')
p=pd.read_parquet(root/'predictions.parquet'); m=pd.read_csv(root/'metrics.csv'); peak=pd.read_csv(root/'peak_windows.csv'); trace=pd.read_csv(root/'aci_trace.csv'); s=json.loads((root/'selection.json').read_text())
labels=['p025','p05','p10','p25','p50','p75','p90','p95','p975']; cols=['final_'+v for v in labels]; taus=np.array([.025,.05,.1,.25,.5,.75,.9,.95,.975])
assert len(p)==75229 and len(m)==35 and not p.duplicated(['candidate','fold','timestamp_utc']).any()
maxerr=0.; scores={}
for (candidate,fold),g in p.groupby(['candidate','fold']):
    q=g[cols].to_numpy(); y=g.y_true.to_numpy(); residual=y[:,None]-q
    row=m.loc[m.candidate.eq(candidate)&m.fold.eq(fold)].iloc[0]
    pinball=np.where(residual>=0,taus*residual,(taus-1)*residual).mean()
    maxerr=max(maxerr,abs(pinball-row.mean_pinball)); assert abs(pinball-row.mean_pinball)<1e-12
    assert np.isfinite(q).all() and not (np.diff(q,axis=1)<0).any()
    assert row.n_obs==len(g) and row.n_days==g.delivery_date.nunique()
    assert abs(np.abs(y-q[:,4]).mean()-row.mae)<1e-12
    for label,lo,hi in [('50',3,5),('80',2,6),('95',0,8)]:
        hits=(y>=q[:,lo])&(y<=q[:,hi]); assert abs(hits.mean()-row['coverage_'+label])<1e-15
    assert hits.sum()==row.covered_95
for candidate in s['tie_order']:
    g=p.loc[p.candidate.eq(candidate)&p.fold.isin(['fold_1','fold_2','fold_4','fold_5'])]
    r=g.y_true.to_numpy()[:,None]-g[cols].to_numpy(); scores[candidate]=np.where(r>=0,taus*r,(taus-1)*r).mean()
    assert len(g)==8635 and abs(scores[candidate]-s['pooled_mean_pinball'][candidate])<1e-13
assert min(s['tie_order'],key=scores.get)==s['selected_candidate']
for row in peak.itertuples():
    g=p.loc[p.candidate.eq(row.candidate)&p.fold.eq('fold_3')]; g=g.loc[pd.to_datetime(g.delivery_date).between('2022-08-15','2022-08-31')]
    hits=(g.y_true>=g.final_p025)&(g.y_true<=g.final_p975)
    assert len(g)==408 and g.delivery_date.nunique()==17 and hits.sum()==row.covered_95 and abs(hits.mean()-row.coverage_95)<1e-15
print('35 groups / 75229 rows: independently recomputed MAE, pinball, coverages, counts; zero crossings; maximum pinball error',maxerr)
print('Independent selection:',s['selected_candidate'],repr(float(scores[s['selected_candidate']])), 'over 8635 observations')
for candidate in [s['selected_candidate'],'v1_reference']:
    g=p.loc[p.candidate.eq(candidate)&p.fold.eq('fold_3')]; hits=(g.y_true>=g.final_p025)&(g.y_true<=g.final_p975)
    sub=g.loc[pd.to_datetime(g.delivery_date).between('2022-08-15','2022-08-31')]; sh=(sub.y_true>=sub.final_p025)&(sub.y_true<=sub.final_p975)
    print(candidate,'full-fold',int(hits.sum()),'/',len(g),'=',hits.mean(),'; peak',int(sh.sum()),'/',len(sub),'=',sh.mean())
snapshot=pd.read_parquet('data/snapshot.parquet',filters=[('delivery_date','<=',pd.Timestamp('2026-04-07').date())],columns=['timestamp_utc','delivery_date','price_eur_mwh'])
observed=set()
for day,g in snapshot.groupby('delivery_date'):
    expected=pd.date_range(pd.Timestamp(day,tz='Europe/Berlin'),pd.Timestamp(day+timedelta(days=1),tz='Europe/Berlin'),freq='h',inclusive='left').tz_convert('UTC')
    if len(g)==len(expected) and set(pd.DatetimeIndex(g.timestamp_utc))==set(expected) and np.isfinite(g.price_eur_mwh).all(): observed.add(day)
cal=pd.read_parquet('reports/cp2/development_calibration_predictions.parquet'); cal=cal.loc[cal.arm.eq('base')]
trace_count=0
for (candidate,fold),t in trace.groupby(['candidate','fold']):
    g=p.loc[p.candidate.eq(candidate)&p.fold.eq(fold)]; step=Fraction(candidate.removeprefix('c2_aci_gamma_')); ncal=len(cal.loc[cal.fold.eq(fold)])
    for row in t.itertuples():
        day=pd.Timestamp(row.delivery_date).date(); cutoff=day-timedelta(days=2)
        assert pd.Timestamp(row.feedback_cutoff).date()==cutoff
        feedback=g.loc[(g.delivery_date<=cutoff)&g.delivery_date.isin(observed)]
        assert len(feedback)==row.n_feedback
        for label,lo,hi,nominal in [('95',0,8,Fraction(19,20)),('90',1,7,Fraction(9,10)),('80',2,6,Fraction(4,5)),('50',3,5,Fraction(1,2))]:
            hits=((feedback.y_true>=feedback[cols[lo]])&(feedback.y_true<=feedback[cols[hi]])).sum()
            state=nominal+step*(nominal*len(feedback)-int(hits)); rank=math.ceil((ncal+1)*state)
            assert abs(float(state)-getattr(row,'coverage_state_'+label))<2e-16
            assert rank==getattr(row,'rank_'+label) and 1<=rank<=ncal
        trace_count+=1
print('Independent D-2 trace audit:',trace_count,'origins; all cutoffs, complete-day feedback counts, four rational states and ranks match')
PY
```

Exit **0**; observed:

```text
35 groups / 75229 rows: independently recomputed MAE, pinball, coverages, counts; zero crossings; maximum pinball error 7.105427357601002e-15
Independent selection: c1_price_volatility 4.385529023834999 over 8635 observations
c1_price_volatility full-fold 1515 / 2112 = 0.7173295454545454 ; peak 131 / 408 = 0.32107843137254904
v1_reference full-fold 1173 / 2112 = 0.5553977272727273 ; peak 79 / 408 = 0.19362745098039216
Independent D-2 trace audit: 1792 origins; all cutoffs, complete-day feedback counts, four rational states and ranks match
```

### Final state and retained reproduction hashes

Exact final command, exit **0** (the detached `symbolic-ref` subcommand itself returned 1 as expected):

```sh
git status --porcelain=v1 && git rev-parse HEAD && git symbolic-ref -q HEAD; shasum -a 256 /tmp/cp10-critic-repro/metrics.csv /tmp/cp10-critic-repro/peak_windows.csv /tmp/cp10-critic-repro/predictions.parquet /tmp/cp10-critic-repro/aci_trace.csv /tmp/cp10-critic-repro/selection.json /tmp/cp10-critic-repro/lineage.json /tmp/cp10-critic-repro/report.md /tmp/cp10-critic-payload-manifest.json
```

Status empty, HEAD unchanged. Hash output:

```text
f54d43b27c1a0b17a533064042482ef23c5268efcc612b315d33407bfd9d15d8  /tmp/cp10-critic-repro/metrics.csv
5d0ca2f6cdbd3fc2b2716834c3f8e32d32164813957a340ebbc29b7750bd2496  /tmp/cp10-critic-repro/peak_windows.csv
e25e0e17fe8fceff44c70492e2f66e20823f515cbff7a04ecaa007084d1386a4  /tmp/cp10-critic-repro/predictions.parquet
9b00929944dbde061e2a5e58fb81b60f6111afe774eef6a242142baccf3dc227  /tmp/cp10-critic-repro/aci_trace.csv
592a5153a38689c8856fd6fa60b79009e2746e4588f361f823e31fa107d9b9ba  /tmp/cp10-critic-repro/selection.json
8fe6477c3f62c71f73de64c77b90d5a1cd44b06f3ae95990eb05b12256433764  /tmp/cp10-critic-repro/lineage.json
b7f1f298a0a0b6cba97df4eba571a15dbd0e316ce19dafe197b6d33deb47820e  /tmp/cp10-critic-repro/report.md
b561df6b01c18f6695c57c4c84ffb87dd6f7c8d3d1117de059e0d795d55765bb  /tmp/cp10-critic-payload-manifest.json
```

## Evidence actually inspected

- Controlling extracts: `AGENTS.md`; `engineering-role.md` Integration Critic protocol; `docs/track-b/gauntlet-templates.md` §2; `capstone_v20.md` §§3,4,9 CP-10 row,13.
- Complete new source and tests: `src/delu_forecast/calibration_comparison.py`, `scripts/cp10_calibration.py`, `tests/test_25_cp10_calibration.py`, `tests/test_26_cp10_evidence.py`.
- Complete inherited modules: `src/delu_forecast/conformal.py`, `src/delu_forecast/postprocess.py`, `src/delu_forecast/metrics.py`. Inherited exact/control tests: `test_02_rolling_closed_left.py`, `test_05_schema_firewall.py`, `test_10_cqr_order_statistic.py`, `test_13_champion_no_delivery_day_leak.py`.
- All eight committed CP-10 artifacts: `protocol.json`, `metrics.csv`, `peak_windows.csv`, `predictions.parquet`, `aci_trace.csv`, `selection.json`, `lineage.json`, `report.md`. All seven generated outputs were reproduced and byte-compared. All prediction groups and all trace origins were independently audited.
- Preserved inputs: `reports/cp2/development_predictions.parquet` and `development_calibration_predictions.parquet` through replay, tests, and direct calibration-row inspection; `reports/cp2/catalog_selection.json`; `data/partitions.json`; only the development slice of `data/snapshot.parquet` for the CP-10 data audit. Protocol/lineage hashes for these inputs, `data/source_manifest.json`, `uv.lock`, the plan and source files were checked by the generator and passing provenance test.
- Candidate history, protocol commit/tree identity, and the complete CP-10 path delta. The checkpoint adds only its eight artifacts, two implementation files and two test files. No v1/protected path is modified.

## Checklist verdict

Each semicolon-delimited CP-10 bar item has its own row.

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | All §4.3 candidates implemented with exact fixtures | PASS | C-1 raw head spread and 168-hour price volatility; all four frozen C-2 gamma settings. Scaled exact fixture yields `{8,7,5,-1}` or spread-normalised `{.2,.175,.125,-.025}` and the exact multiply-back vector `[84,86,90,102,120,138,150,154,156]`; separate exact volatility sample variance/window fixture. Every gamma has rational expected rank/output and opposite hit/miss controls. C-3 is explicitly rejected in protocol, decision and report, and is not implemented, as §4.3 requires. |
| 2 | Selection on folds {1,2,4,5} only | PASS | Selection filters before arithmetic, requires each frozen arm's four folds, pools by observation count and uses frozen order for exact ties. Huge antagonistic fold_3 losses do not move selection; selection-fold mutation does. Independent hourly audit selects `c1_price_volatility`, `4.385529023834999`, agreeing with stored `4.385529023835001` within rounding, over 8,635 observations. Best ACI gamma is `0.00002` by the same eligible-fold scalar. |
| 3 | Full table including fold_3 for every candidate including losers | PASS | `metrics.csv` and report contain all six candidates plus v1 reference across five folds: 35 groups. Predictions have 75,229 rows without duplicate candidate/fold/timestamp keys. All losing candidates' full-fold and 408-hour peak results are present and independently recomputed. |
| 4 | Rule-5 falsification evaluated and reported whichever way it lands | PASS | Exact-boundary fixture tests failure immediately below 0.394, success at 0.394, and failure recommendation v1. Selected full-fold 95% coverage is 1515/2112 = 0.7173295454545454 on July 1–September 28, 88 eligible days within 90 calendar days; literal rule clears. Report explicitly distinguishes the baseline's August 15–31 window: selected 131/408 vs v1 79/408, only 0.12745098039215688 absolute improvement. It discloses that v1 itself clears the literal full-fold threshold, states the original peak-week defect remains unresolved, and retains v1 as recommended frozen artifact. No favourable performance is required for this verdict. |
| 5 | Zero crossings | PASS | Independent adjacent-quantile comparison on every emitted row finds zero crossings and all finite outputs. All 35 metric groups report zero. Source applies CQR before final isotonic; adversarial shifts cross before projection and when operation order is reversed, proving the detector and ordering control can fail. |
| 6 | Positive control on every negative assertion | PASS | Reviewed matching controls for D-price masking/D−1 mutation; C-2 D and D−1 masking/D−2 hit mutation at every gamma; actual D−1 gate mutant rejected; incomplete-day feedback/complete-day change; 23/25-hour completeness/deleted hour; exact scales/wrong unscaled path; raw spread/sorted-head mutation; missing volatility hour/restored complete input; unclipped invalid rank/finite legal gamma; fold_3 exclusion/selection-fold mutation; complete grid/missing fold; crossing-free output/corrupted crossing; evidence metric and prediction corruption; preserved replay/altered vector; firewall refusals/accepted catalog. These controls are executed in the 217-test passing suite. |
| 7 | C-2 two-day lag proved with masking control rather than assumed | PASS | Every gamma's fixture masks D and D−1 feedback labels to NaN with exact `0.0` target-output difference, then mutates a D−2 label and observes nonzero difference. Monkeypatching the actual production boundary to D−1 makes the masked-label run raise `missing released feedback`. Independent audit reconstructs all 1,792 origins' D−2 cutoffs, complete-day feedback counts, all four rational coverage states and one-based ranks from emitted intervals and labels; all match. |

### Supporting invariants and complete artifact checks

| # | Supporting obligation | Verdict | Evidence |
|---|---|---|---|
| S1 | Frozen contract; no fold_3-specific calibration parameter | PASS | Protocol-only commit `5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed` precedes implementation `093692560b78c0ccb47a0ceb83428718c028090d` and the reviewed evidence commit. Protocol bytes unchanged. Constants match its candidate/grid freeze. Calibrator has no fold argument, crisis flag, regime taxonomy or date-selected switch. August dates occur only in reporting. |
| S2 | Unscaled carried rank fixture and isotonic last | PASS | Inherited `n_cal=20` fixture gives one-based ranks `{20,19,17,11}`, zero-based indices `{19,18,16,10}`, thresholds `{8,7,5,-1}`; off-by-one/interpolation controls discriminate. Both C-1 and C-2 apply isotonic last, and C-2 hits use previously emitted final intervals. |
| S3 | Delivery-day availability and schema firewall | PASS | C-1 full feature/model/calibration test masks D prices with exact `0.0` change and changes D−1 prices with nonzero change for both scales. Independent inherited ordinary/DST price controls, champion masking and accepted/refused schema cases all pass. Development loader reconstitutes original eligibility and target/date identities and filters before the reserved tail. |
| S4 | Independent metric recomputation and deterministic reproduction | PASS | Own audit covers all 35 groups, all quantile coverages/MAE/pinball/counts, all peak candidates and all ACI trace origins. Maximum pinball discrepancy `7.105427357601002e-15`. All seven reproduced artifact bytes are identical. Complete regression suite: 217 passed. |
| S5 | Preservation and scope | PASS | Full checkpoint diff comprises 12 added CP-10 paths only; no v1 evidence, model, snapshot, partition, source manifest, lockfile or governance edit. v1 saved final vectors replay exactly, with a corruption control. CP-10 generator reads saved raw development predictions and applies calibration; no fit, holdout performance call, registry/experiment write or network operation exists in its execution path. No refs or external state were changed by this Critic. |
| S6 | Documentation and limits | PASS | Generated report includes full table, selected scalar/denominator, matched and literal falsification windows, C-3 rejection, exact scales, coverage-state interpretation, conservative gamma rationale, no clipping, fixed reservoir, D−2 release semantics, input/source lineage and reproduction commands. It does not claim a new frozen model, holdout result, promotion or long-run delayed-ACI guarantee. The original peak-week failure is disclosed, not removed. |

This PASS binds only the named candidate and CP-10 correctness/evidence bar. It does not certify that the original peak-week calibration defect is fixed. The observed matched-window improvement is below 20 percentage points and v1 remains the recommended frozen artifact.

Interview-answer capture trigger: the literal full-fold falsification threshold and the original peak-window defect use different denominators; both were independently checked and disclosed. No entry was filed because capture is suspended.
