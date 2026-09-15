# Verdict — CP-15 — Integration — FAIL

- Candidate SHA: `f8d0ed2a5f0737f0d088c3474b5a9fe77a406f37`
- Candidate tree: `f5163f87cf9b0e04470a96b867e720fb1fe78f02`
- Plan / version / bar: `capstone_v21.md`, v21, complete §12, supported by §§1–8, 11 and 13.
- Plan SHA256: `62e84ceb4f35190c89faffaee4e8af01c5b3c81f9d78f9f3f68556e25f360065`; independently matched.
- Worktree: `/Users/djourno/Downloads/critic-cp-15`, detached at the candidate.
- Worktree clean before and after: yes; empty `git status --porcelain=v1`, unchanged HEAD/tree. Final checks occurred immediately before writing this verdict outside the checkout.
- Product feasibility: **NOT_DEMONSTRATED**. All six product criteria are **unassessed**, not measured failures. Best observed policy: **none (comparison not run)**. Qualified policy: **none**.
- Integration is **FAIL**, because substantive requirements are unmet. Review could be performed; therefore the Integration definition of BLOCKED does not apply. The candidate's reported engineering BLOCKED refers to its prehistory obstacle and is not an Integration verdict.

## Verbatim bar excerpt

> 1. Verify and report the starting state; preserve other sessions' work, v1/CP-10 evidence and
>    restricted partitions; commit the exact v21 anchor and pre-run protocol before comparison.
> 2. Implement every B0–B3/A1–A5 policy in §5 and the common uncertainty construction in §6;
>    prove genuine rolling fits, warm-up provenance and causal per-origin normalization with fixtures.
> 3. Prove §2 availability, D-2 feedback, single consumption, DST and schema refusal controls;
>    each negative assertion has a positive control, including inherited live-namespace guards.
> 4. Produce predictions on identical original eligible hours and all metrics/diagnostics in §7
>    for every arm; independently check counts, zero crossings, scores and exact window denominators.
> 5. Apply §7 ranking and every §8 criterion mechanically; report both Integration status and
>    product_feasibility, best observed policy, qualified policy or none, and all failed criteria.
> 6. Deliver the pinned Chronos-2 feasibility probe and structural-input feasibility sheet in §5;
>    document genuine access/resource limitations without inventing benchmark results or silently
>    promoting probes into the candidate set. Such probe limitations do not block the core comparison.
> 7. Provide pinned reproduction commands, dependency/input/protocol hashes, seeds, chronological
>    validation records, resource measurements and dependence-aware uncertainty; rerun relevant
>    controls and the existing regression suite, reporting any blockers without a false PASS.
> 8. One fresh independent Integration Critic reviews a clean detached checkout of the exact
>    final_candidate_sha, verifies every checklist item, independently recomputes saved-prediction
>    metrics and performs causal control/representative fit reproduction; commit its verdict only
>    after review. Record commands actually run, exit codes and limitations. No binding PASS means
>    no terminal PASS. Candidate-to-evidence-tip changes are confined to this checkpoint's evidence.

The supplied excerpt matches the committed plan.

## Commands actually run

All repository commands used the detached worktree above. No credentials, network requests, Git mutations, or publication were used. Generated environment/browser payload files are ignored; the payload manifest and reproduction outputs were redirected to /tmp as assigned.

| Command | Exit | Observed result |
|---|---:|---|
| `uv sync --frozen --offline` | 0 | Python 3.13.15; 117 packages installed, including the local project; ignored .venv created. |
| `uv run --frozen pytest -q tests/cp15` | 0 | 6 passed in 0.03s. |
| `uv run --frozen python scripts/cp15_forecasting.py --preflight --output /tmp/cp15-critic-reproduction` | 2 | Reported BLOCKED, NOT_DEMONSTRATED, model_fit_count 0. This is the deliberately encoded preflight refusal, not a failed model fit. |
| `cmp reports/cp15/preflight.json /tmp/cp15-critic-reproduction/preflight.json && cmp reports/cp15/history-windows.csv /tmp/cp15-critic-reproduction/history-windows.csv` (premature first attempt) | 2 | Preflight was still running; first output file did not yet exist. No artifact mismatch was established. |
| Same two `cmp` commands after preflight completion, followed by `git rev-parse 'HEAD^{tree}'` | 0 | Both files byte-identical; tree matched the supplied candidate tree. |
| Payload regeneration command below | 0 | 15,363,807 bytes across 14 files; 54 fixture days / 1,296 rows, 4 fail-closed; manifest written to /tmp. Historical frozen-artifact identity replay only. |
| `uv run --frozen pytest -q` | 0 | **223 passed in 46.53s**. Includes inherited causal, schema, DST, feedback, single-consumption and live-namespace positive/negative controls. |
| Independent arithmetic command in Appendix A | 0 | All 12 protocol hashes match; all 1,190 calendar/available-row calculations match; original saved base counts 2,160 / 2,159 / 2,112 / 2,160 / 2,156, total 10,747; peak 408 hours / 17 days. |
| Initial stronger independent eligibility-reconstruction command (Appendix B), and its vectorized retry (Appendix C) | 143 each | Both stopped after several minutes of active CPU computation to bound review time. No results claimed from either. `kill -TERM 39382` and `kill -TERM 40196` each returned 0. The completed Appendix A check does not independently rebuild feature eligibility. |
| `git symbolic-ref -q HEAD` | 1 | No output: detached HEAD, as required. |
| Final identity/cleanliness assertions immediately before writing | 0 | HEAD/tree unchanged, status empty, both unstaged and staged diffs empty. |

Payload command actually run:

```sh
uv run --frozen python - <<'PY'
from pathlib import Path
import runpy
ns=runpy.run_path('scripts/build_wasm_payload.py',run_name='cp15_critic_setup')
ns['main'].__globals__['MANIFEST']=Path('/tmp/cp15-critic-payload-manifest.json')
raise SystemExit(ns['main']())
PY
```

Read-only inspection commands and results:

- Initial `pwd && git rev-parse HEAD && git status --porcelain=v1 && shasum -a 256 capstone_v21.md && cat docs/track-b/gauntlet-templates.md`: exit 0; correct directory/SHA, empty status, matching plan hash, canonical verdict form inspected.
- `cat capstone_v21.md && cat docs/track-b/cp-15-brief.md`: exit 0; controlling text and immutable brief inspected.
- `rg --files src/cp15 tests/cp15 reports/cp15 && cat scripts/cp15_forecasting.py && cat reports/cp15/protocol.json`: exit 0; only preflight implementation/tests/reports, no model-comparison artifacts.
- `cat src/cp15/preflight.py && cat tests/cp15/test_preflight.py && cat reports/cp15/report.md && cat reports/cp15/starting-state.json && cat reports/cp15/validation.json && cat reports/cp15/preflight.json && cat reports/cp15/history-windows.csv`: exit 0; output exceeded display budget. Summary JSON and state were reread in full below; CSV values were checked programmatically.
- `cat reports/cp15/starting-state.json reports/cp15/validation.json reports/cp15/preflight.json data/partitions.json && cat src/delu_forecast/features.py && rg --files tests | sort && git log --oneline 4039ce24150b36ea233b043061e68eb2be78cbbe..HEAD && git diff --stat 4039ce24150b36ea233b043061e68eb2be78cbbe..HEAD`: exit 0; two CP-15 commits, 13 changed files, no preserved engineering/data paths changed.
- `cat tests/conftest.py tests/test_24_live_namespace_is_walled_off.py tests/test_13_champion_no_delivery_day_leak.py && git show --stat --oneline 884261d30284877092eadda9bfb6704f0ec1e890 && git rev-parse HEAD^{tree}`: exit 1 because zsh expanded the unquoted braces/glob in the last command; preceding reads and commit inspection succeeded. Quoted tree command subsequently passed.
- `cat tests/test_25_cp10_calibration.py`: exit 0; inherited D-2, completeness, single-consumption, causal scaling and mutant/positive controls inspected.
- `git diff --name-only 4039ce24150b36ea233b043061e68eb2be78cbbe..HEAD && git show 884261d30284877092eadda9bfb6704f0ec1e890:reports/cp15/protocol.json && git status --porcelain=v1`: exit 0; immutable packaging/preflight protocol precede implementation; empty status.
- `ps -axo pid,etime,time,command | rg 'uv run --frozen python|python -$'` and `ps -axo pid,ppid,etime,time,state,comm | awk '$1 == 39306 || $2 == 39306'`: both exit 0; initial independent process was running, with 3:06.65 CPU time after 3:08 elapsed at the second check. A further `ps -axo pid,ppid,etime,time,state,comm | awk '$6 ~ /python3$/ && $5 ~ /R/'` also returned 0, showing the retry active at 2:54 elapsed / 2:52.09 CPU. These inspected process state only.

## Evidence actually inspected

- The exact named plan, canonical §2 verdict form, and `docs/track-b/cp-15-brief.md`.
- All CP-15 source, driver, tests, and six report artifacts listed by the inventory.
- `data/partitions.json`; only four explicitly projected snapshot columns with the reader-level predicate `delivery_date <= 2026-04-07`.
- Original admissible `reports/cp2/development_predictions.parquet` date/target lineage. Other protocol inputs were hashed for immutable identity only.
- Inherited feature definitions, synthetic fixture generator, tests 13, 24 and 25 as source; complete regression suite executed.
- Candidate history and change list relative to the supplied CP-10 evidence base; exact protocol in the first CP-15 commit `884261d30284877092eadda9bfb6704f0ec1e890`.

## Independent arithmetic findings

All 12 preregistered input hashes matched. The admissible snapshot has 63,695 rows from 2019-01-01 through 2026-04-07. The completed independent script verified every one of 1,190 CSV rows for calendar boundaries, timezone-aware canonical hours, absent leading days/hours, support flag and available snapshot-row count. It used standard-library zoneinfo UTC arithmetic and NumPy day masks, with no CP-15 imports.

The original saved base vectors independently count to 2,160 / 2,159 / 2,112 / 2,160 / 2,156 rows across folds 1–5: **10,747** total. The matched peak has **408 hours across 17 days**. There are 90 evaluation and 29 optimistic warm-up origins without 728-day leading support, all in fold 1. The first evaluation shortage is **181 calendar days / 4,345 canonical hours**; the optimistic first warm-up shortage is **210 days / 5,041 hours**.

**Review limit:** the two attempts to reconstruct feature eligibility independently of the inherited feature builder were stopped for runtime, without completed results. Therefore CSV `inherited_eligible_training_rows` and feature-by-feature eligibility were not independently reconstructed. Their agreement is supported by byte-identical production-preflight reproduction, while the independent original eligible counts above come from the preserved saved base vectors. Neither aborted attempt contributes evidence.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Starting state, preservation, exact anchor and preregistration before comparison | PASS for delivered preflight prerequisites | Starting state is recorded; exact plan/rulebook/brief hashes match; immutable packaging and preflight protocol are in the first CP-15 commit; preserved engineering/data paths are unchanged against the supplied base. No comparison occurred. This does not certify a frozen comparison protocol: its choices are explicitly deferred. Other sessions' live checkouts were not independently inspected under isolation. |
| 2 | All nine policies, common uncertainty, rolling fits, warm-up and causal normalization fixtures | FAIL | Only preflight is implemented. No LEAR/LightGBM rolling policy, normalized policy, ensemble, rolling signed-error distribution, issued warm-up forecasts, or CP-15 fit/normalization fixtures exist. |
| 3 | Availability, D-2, single consumption, DST, schema and live guards with positive controls | FAIL | Six preflight tests and all inherited tests pass, including applicable positive controls. They do not prove these boundaries for the unimplemented CP-15 fitting/normalization/error-buffer pipeline. |
| 4 | Matched predictions, every score/diagnostic, independent counts/crossings/denominators | FAIL | Original saved eligible counts and calendar/available-row arithmetic are independently checked; feature-eligibility reconstruction remains limited as stated above. No nine-arm CP-15 predictions, zero-crossing result, §7 scores or diagnostics exist. Counts alone cannot satisfy this item. |
| 5 | Mechanical ranking and all six product criteria; separate outcomes | FAIL | Report honestly says no best observed policy, no qualified policy and NOT_DEMONSTRATED. There is no ranking or six-criterion calculation with actual values; all six criteria remain unassessed. |
| 6 | Pinned Chronos-2 probe and structural-input feasibility sheet | FAIL | Neither deliverable exists. Access/resource limits were not tested. The archive obstacle does not demonstrate that these independent feasibility tasks were impossible. No invented benchmark or unsupported access limitation is claimed. |
| 7 | Reproduction/hashes/seeds/validation/resources/uncertainty and regression | FAIL | Preflight reproduction, input/protocol/dependency hashes, preflight runtime/RSS record and 223 passing tests are present. Full comparison protocol, seeds, penalty grid, chronological validation records, model resources and 2,000-replicate paired 7-day block bootstrap are absent. |
| 8 | Fresh exact-candidate Integration, saved-metric recomputation and representative-fit reproduction | FAIL | Fresh detached review and causal regression were performed with exact identity/cleanliness checks. CP-15 saved-prediction metrics and representative fits could not be reproduced because they do not exist. This verdict cannot bind a PASS. Lead must commit it only after this review and verify the evidence-only candidate-to-tip delta. |

## Limitations and disposition of missing work

No CP-15 saved-prediction MAE, RMSE, WIS, coverage, widths, misses, quantile crossings, uncertainty, or ranking was independently recomputed: there are no CP-15 prediction vectors. The CP-2 read establishes original row/target lineage, not completion of CP-15's B1 reporting obligation. No representative CP-15 rolling fit or genuine warm-up was run: neither code nor results exist. Inherited synthetic fits and frozen identity tests are explicitly not substitutes.

The prehistory deficiency is real evidence worth preserving, and the candidate reports it honestly. It does not convert missing experiment and feasibility deliverables into completed acceptance items. No result about whether adaptive forecasting succeeds or fails follows from this candidate.

This Critic did not inspect other checkouts, program state, Orchestrator contracts, Track A/C, or later-checkpoint work; did not modify tracked files, manage Git state, or remove this worktree. Historical fixture replay was solely the expressly assigned frozen regression, with no restricted-partition fitting, tuning or selection. The Lead retains sole Git-writing/cleanup responsibility.

## On FAIL only

- **Single largest meaningful gap:** the required nine-policy rolling experiment has not been implemented or run. The candidate establishes a fold-1 archive deficiency, but delivers zero comparison predictions and no basis for the §7/§8 outcome.
- **Exact next acceptance test:** after an explicitly authorized resolution of fold-1 prehistory, the first-fold rolling pipeline must use the ratified 728-day history and genuine D-2-released warm-up (including the earliest supported issuance), then emit all **2,160 original fold-1 eligible targets for every B0–B3/A1–A5 policy** with finite ordered seven-quantile vectors and per-origin fit/normalization/error lineage. An independent replay must reproduce representative fits and saved-vector scores while delivery-day masking changes predictions by exactly zero and the available D-1 positive control moves them. This is the next necessary test, not a waiver of the remaining full-five-fold, feasibility-sheet/probe and complete §12 obligations.

## Appendix A — completed independent command

```sh
uv run --frozen python - <<'PY'
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import hashlib,json
import numpy as np
import pandas as pd
p=json.loads(Path('reports/cp15/protocol.json').read_text())
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in p['input_sha256'].items())
f=pd.read_parquet('data/snapshot.parquet',columns=['timestamp_utc','delivery_date','price_eur_mwh','load_forecast_mw'],filters=[('delivery_date','<=',date(2026,4,7))])
s=pd.read_parquet('reports/cp2/development_predictions.parquet',columns=['arm','fold','delivery_date','y_true'])
s=s[s.arm.eq('base')]
assert s.groupby('fold').size().tolist()==[2160,2159,2112,2160,2156]
assert len(s)==10747
peak=s[s.delivery_date.between(date(2022,8,15),date(2022,8,31))]
assert len(peak)==408 and peak.delivery_date.nunique()==17
assert len(f)==63695 and min(f.delivery_date)==date(2019,1,1) and max(f.delivery_date)==date(2026,4,7)
berlin=ZoneInfo('Europe/Berlin')
def utc(d): return datetime.combine(d,datetime.min.time(),berlin).astimezone(timezone.utc)
def hours(a,b): return int((utc(b)-utc(a)).total_seconds()/3600)
w=pd.read_csv('reports/cp15/history-windows.csv'); days=np.array(f.delivery_date,dtype='datetime64[D]')
for r in w.itertuples():
    d=date.fromisoformat(r.origin); a=d-timedelta(days=r.history_days); end=min(d,date(2019,1,1)); absent=max(0,(end-a).days)
    assert r.required_start==str(a) and r.required_end==str(d-timedelta(days=1))
    assert r.required_canonical_hours==hours(a,d) and r.absent_leading_calendar_days==absent
    assert r.absent_leading_canonical_hours==(hours(a,end) if absent else 0)
    assert bool(r.archive_reaches_required_start)==(absent==0)
    assert r.available_snapshot_rows==int(((days>=np.datetime64(a))&(days<np.datetime64(d))).sum())
assert len(w)==1190
bad=w[~w.archive_reaches_required_start]
assert len(bad)==119 and set(bad.fold)=={'fold_1'} and set(bad.history_days)=={728}
print('All',len(p['input_sha256']),'protocol hashes match; 63,695 admissible snapshot rows.')
print('Original saved base eligibility:',s.groupby('fold').size().to_dict(),'total',len(s),'peak',len(peak),'hours /',peak.delivery_date.nunique(),'days')
print('All 1,190 calendar-window and available-snapshot-row calculations match.')
print('Missing fold-1 728-day origins:',bad.groupby('phase').size().to_dict())
print('Evaluation shortage:',(date(2019,1,1)-date(2018,7,4)).days,hours(date(2018,7,4),date(2019,1,1)))
print('Optimistic warmup shortage:',(date(2019,1,1)-date(2018,6,5)).days,hours(date(2018,6,5),date(2019,1,1)))
PY
```

## Appendix B — first bounded, terminated attempt

```sh
uv run --frozen python - <<'PY'
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import hashlib, json
import numpy as np
import pandas as pd
root=Path('.')
spec=json.loads((root/'data/partitions.json').read_text())
protocol=json.loads((root/'reports/cp15/protocol.json').read_text())
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in protocol['input_sha256'].items())
f=pd.read_parquet('data/snapshot.parquet',columns=['timestamp_utc','delivery_date','price_eur_mwh','load_forecast_mw'],filters=[('delivery_date','<=',date(2026,4,7))])
assert len(f)==63695 and f.delivery_date.max()==date(2026,4,7)
berlin=ZoneInfo('Europe/Berlin')
def utc(d): return datetime.combine(d,datetime.min.time(),berlin).astimezone(timezone.utc)
def hours(a,b): return int((utc(b)-utc(a)).total_seconds()/3600)
idx=pd.DatetimeIndex(f.timestamp_utc)
p=pd.Series(f.price_eur_mwh.to_numpy(),index=idx)
load=pd.Series(f.load_forecast_mw.to_numpy(),index=idx)
days=f.delivery_date.to_numpy()
valid=np.isfinite(f.price_eur_mwh.to_numpy())
for d in sorted(set(days)):
    positions=np.flatnonzero(days==d)
    expected=pd.date_range(utc(d),utc(d+timedelta(days=1)),freq='h',inclusive='left')
    previous=pd.date_range(end=utc(d)-timedelta(hours=1),periods=720,freq='h')
    valid[positions] &= np.isfinite(load.reindex(expected).to_numpy()).all() and np.isfinite(p.reindex(previous).to_numpy()).all()
local=idx.tz_convert('Europe/Berlin').tz_localize(None)
for lag in [1,2,7]:
    lag_idx=(local-pd.Timedelta(days=lag)).tz_localize('Europe/Berlin',ambiguous='NaT',nonexistent='NaT').tz_convert('UTC')
    valid &= np.isfinite(p.reindex(lag_idx).to_numpy())
saved=pd.read_parquet('reports/cp2/development_predictions.parquet',columns=['arm','fold','delivery_date','y_true'])
saved=saved[saved.arm.eq('base')]
expected_summary=json.loads(Path('reports/cp15/preflight.json').read_text())
for fold,claimed in zip(spec['development_folds'],expected_summary['folds'],strict=True):
    a,b=map(date.fromisoformat,[fold['evaluation']['start'],fold['evaluation']['end']])
    inside=(days>=a)&(days<=b)
    mask=inside&valid
    ref=saved[saved.fold.eq(fold['name'])]
    assert np.array_equal(ref.delivery_date.to_numpy(),days[mask])
    assert np.array_equal(ref.y_true.to_numpy(),f.price_eur_mwh.to_numpy()[mask])
    counts=(int(mask.sum()),len(set(days[mask])),int(inside.sum()-mask.sum()))
    assert counts==(claimed['original_eligible_hours'],claimed['represented_delivery_days'],claimed['inherited_excluded_hours'])
    print(fold['name'],counts)
w=pd.read_csv('reports/cp15/history-windows.csv')
archive=min(days)
for row in w.itertuples():
    d=date.fromisoformat(row.origin); a=d-timedelta(days=row.history_days)
    end=min(d,archive); absent=max(0,(end-a).days)
    mask=(days>=a)&(days<d)
    assert row.required_start==a.isoformat() and row.required_end==(d-timedelta(days=1)).isoformat()
    assert row.required_canonical_hours==hours(a,d)
    assert row.absent_leading_calendar_days==absent
    assert row.absent_leading_canonical_hours==(hours(a,end) if absent else 0)
    assert bool(row.archive_reaches_required_start)==(absent==0)
    assert row.available_snapshot_rows==int(mask.sum())
    assert row.inherited_eligible_training_rows==int((mask&valid).sum())
assert len(w)==1190
bad=w[~w.archive_reaches_required_start]
assert len(bad)==119 and set(bad.fold)=={'fold_1'} and set(bad.history_days)=={728}
peak=valid&(days>=date(2022,8,15))&(days<=date(2022,8,31))
assert peak.sum()==408 and len(set(days[peak]))==17
print('All 13 protocol input hashes verified; all 1190 window rows independently matched.')
print('Original eligible total:',len(saved),'peak:',int(peak.sum()),'hours /',len(set(days[peak])),'days')
print('Missing fold-1 728-day origins:',bad.groupby('phase').size().to_dict())
print('First evaluation missing days/hours:',(archive-date(2018,7,4)).days,hours(date(2018,7,4),archive))
print('Optimistic first warmup missing days/hours:',(archive-date(2018,6,5)).days,hours(date(2018,6,5),archive))
PY
```

## Appendix C — vectorized retry, also terminated

```sh
uv run --frozen python - <<'PY'
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import hashlib, json
import numpy as np
import pandas as pd
root=Path('.')
spec=json.loads((root/'data/partitions.json').read_text())
protocol=json.loads((root/'reports/cp15/protocol.json').read_text())
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in protocol['input_sha256'].items())
f=pd.read_parquet('data/snapshot.parquet',columns=['timestamp_utc','delivery_date','price_eur_mwh','load_forecast_mw'],filters=[('delivery_date','<=',date(2026,4,7))])
assert len(f)==63695 and f.delivery_date.max()==date(2026,4,7)
berlin=ZoneInfo('Europe/Berlin')
def utc(d): return datetime.combine(d,datetime.min.time(),berlin).astimezone(timezone.utc)
def hours(a,b): return int((utc(b)-utc(a)).total_seconds()/3600)
idx=pd.DatetimeIndex(f.timestamp_utc)
p=pd.Series(f.price_eur_mwh.to_numpy(),index=idx)
load=pd.Series(f.load_forecast_mw.to_numpy(),index=idx)
days=f.delivery_date.to_numpy()
daynums=np.array(days,dtype='datetime64[D]')
valid=np.isfinite(f.price_eur_mwh.to_numpy())
for d in sorted(set(days)):
    positions=np.flatnonzero(daynums==np.datetime64(d))
    expected=pd.date_range(utc(d),utc(d+timedelta(days=1)),freq='h',inclusive='left')
    previous=pd.date_range(end=utc(d)-timedelta(hours=1),periods=720,freq='h')
    valid[positions] &= np.isfinite(load.reindex(expected).to_numpy()).all() and np.isfinite(p.reindex(previous).to_numpy()).all()
local=idx.tz_convert('Europe/Berlin').tz_localize(None)
for lag in [1,2,7]:
    lag_idx=(local-pd.Timedelta(days=lag)).tz_localize('Europe/Berlin',ambiguous='NaT',nonexistent='NaT').tz_convert('UTC')
    valid &= np.isfinite(p.reindex(lag_idx).to_numpy())
saved=pd.read_parquet('reports/cp2/development_predictions.parquet',columns=['arm','fold','delivery_date','y_true'])
saved=saved[saved.arm.eq('base')]
expected_summary=json.loads(Path('reports/cp15/preflight.json').read_text())
for fold,claimed in zip(spec['development_folds'],expected_summary['folds'],strict=True):
    a,b=map(date.fromisoformat,[fold['evaluation']['start'],fold['evaluation']['end']])
    inside=(daynums>=np.datetime64(a))&(daynums<=np.datetime64(b))
    mask=inside&valid
    ref=saved[saved.fold.eq(fold['name'])]
    assert np.array_equal(ref.delivery_date.to_numpy(),days[mask])
    assert np.array_equal(ref.y_true.to_numpy(),f.price_eur_mwh.to_numpy()[mask])
    counts=(int(mask.sum()),len(set(days[mask])),int(inside.sum()-mask.sum()))
    assert counts==(claimed['original_eligible_hours'],claimed['represented_delivery_days'],claimed['inherited_excluded_hours'])
    print(fold['name'],counts)
w=pd.read_csv('reports/cp15/history-windows.csv')
archive=min(days)
for row in w.itertuples():
    d=date.fromisoformat(row.origin); a=d-timedelta(days=row.history_days)
    end=min(d,archive); absent=max(0,(end-a).days)
    mask=(daynums>=np.datetime64(a))&(daynums<np.datetime64(d))
    assert row.required_start==a.isoformat() and row.required_end==(d-timedelta(days=1)).isoformat()
    assert row.required_canonical_hours==hours(a,d)
    assert row.absent_leading_calendar_days==absent
    assert row.absent_leading_canonical_hours==(hours(a,end) if absent else 0)
    assert bool(row.archive_reaches_required_start)==(absent==0)
    assert row.available_snapshot_rows==int(mask.sum())
    assert row.inherited_eligible_training_rows==int((mask&valid).sum())
assert len(w)==1190
bad=w[~w.archive_reaches_required_start]
assert len(bad)==119 and set(bad.fold)=={'fold_1'} and set(bad.history_days)=={728}
peak=valid&(daynums>=np.datetime64('2022-08-15'))&(daynums<=np.datetime64('2022-08-31'))
assert peak.sum()==408 and len(set(days[peak]))==17
print('All 13 protocol input hashes verified; all 1190 window rows independently matched.')
print('Original eligible total:',len(saved),'peak:',int(peak.sum()),'hours /',len(set(days[peak])),'days')
print('Missing fold-1 728-day origins:',bad.groupby('phase').size().to_dict())
print('First evaluation missing days/hours:',(archive-date(2018,7,4)).days,hours(date(2018,7,4),archive))
print('Optimistic first warmup missing days/hours:',(archive-date(2018,6,5)).days,hours(date(2018,6,5),archive))
PY
```
