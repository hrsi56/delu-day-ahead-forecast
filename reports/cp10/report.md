# CP-10 — development calibration comparison

Selected: **c1_price_volatility**, pooled mean pinball **4.385529024** on **8,635 observations** from folds 1, 2, 4 and 5. v1 reference: 4.466576610. This is development evidence, not a new holdout result.

## Falsification: distinguish the two windows

The literal full-fold rule in v20 §4.2(5) is evaluated on 2022-07-01 through 2022-09-28: **1515 / 2112 = 0.717329545** 95% coverage, versus its fixed 0.394 threshold. Result: **fix cleared the pre-registered falsification threshold**. The denominator is 2,112 eligible hours on 88 represented days within the 90-day calendar block.

**This does not establish that the original peak-week collapse is fixed.** The plan's 0.194 baseline comes from August 15–31, not the full fold. On that same 408-hour / 17-day subset, the selected method covers **131/408 (0.321078431)**, versus v1 **79/408 (0.193627451)**: **12.745 percentage points** of improvement. This falls short of 20 points. Relative to the literal rounded 0.194, the improvement is 0.127078431, also below 0.20.

The matched full-fold change is 0.161931818, from v1's 0.555397727; v1 itself already clears the literal 0.394 full-fold threshold. Both comparisons are disclosed rather than treating different denominators as the same experiment. The same-window diagnostic does not alter selection or replace the pre-run full-fold rule. **The original peak-week defect remains unresolved; retain v1 as the currently recommended frozen artifact.** No v2 artifact was frozen, promoted or evaluated on a holdout, and no 90-day clock started.

## All candidates, including losers

C-1 head spread, C-1 trailing price volatility and all four frozen C-2 gamma settings are shown. v1 is a reference, outside the candidate set. Lower pooled pinball wins; exact ties follow the order below. The nine quantile losses are equally weighted within each observation; observations are pooled, not fold means averaged.

| Candidate | Selection pooled pinball | fold_3 pinball | fold_3 coverage95 | Peak coverage95 |
|---|---:|---:|---:|---:|
| v1_reference | 4.466576610 | 39.975234374 | 0.555397727 | 0.193627451 |
| c1_head_spread | 4.410400556 | 35.501294217 | 0.685606061 | 0.441176471 |
| c1_price_volatility | 4.385529024 | 35.856218027 | 0.717329545 | 0.321078431 |
| c2_aci_gamma_0.000001 | 4.466063444 | 39.939039786 | 0.558238636 | 0.193627451 |
| c2_aci_gamma_0.000005 | 4.464562255 | 39.905489937 | 0.559185606 | 0.193627451 |
| c2_aci_gamma_0.00001 | 4.462436310 | 39.825845757 | 0.565340909 | 0.198529412 |
| c2_aci_gamma_0.00002 | 4.460087920 | 39.631559811 | 0.573390152 | 0.205882353 |

### Full five-fold table

| Candidate | Fold | Hours | MAE | Pinball | Coverage50 | Coverage80 | Coverage95 | Crossings |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| c1_head_spread | fold_1 | 2160 | 6.602103 | 1.856061 | 0.361574 | 0.655093 | 0.864815 | 0 |
| c1_head_spread | fold_2 | 2159 | 20.037843 | 4.585139 | 0.304308 | 0.643353 | 0.945808 | 0 |
| c1_head_spread | fold_3 | 2112 | 141.008516 | 35.501294 | 0.281723 | 0.458807 | 0.685606 | 0 |
| c1_head_spread | fold_4 | 2160 | 20.053776 | 5.057081 | 0.439352 | 0.776852 | 0.952778 | 0 |
| c1_head_spread | fold_5 | 2156 | 23.165588 | 6.146617 | 0.493043 | 0.761596 | 0.921150 | 0 |
| c1_price_volatility | fold_1 | 2160 | 6.624001 | 1.808680 | 0.424074 | 0.697222 | 0.898611 | 0 |
| c1_price_volatility | fold_2 | 2159 | 20.038967 | 4.705379 | 0.326077 | 0.634553 | 0.912459 | 0 |
| c1_price_volatility | fold_3 | 2112 | 141.007963 | 35.856218 | 0.296875 | 0.470644 | 0.717330 | 0 |
| c1_price_volatility | fold_4 | 2160 | 20.068712 | 5.083709 | 0.466204 | 0.818056 | 0.970833 | 0 |
| c1_price_volatility | fold_5 | 2156 | 23.161209 | 5.947388 | 0.533395 | 0.811224 | 0.955937 | 0 |
| c2_aci_gamma_0.000001 | fold_1 | 2160 | 6.612876 | 1.826797 | 0.390278 | 0.676389 | 0.895833 | 0 |
| c2_aci_gamma_0.000001 | fold_2 | 2159 | 20.039141 | 4.868275 | 0.237610 | 0.506253 | 0.883279 | 0 |
| c2_aci_gamma_0.000001 | fold_3 | 2112 | 140.992859 | 39.939040 | 0.208807 | 0.352746 | 0.558239 | 0 |
| c2_aci_gamma_0.000001 | fold_4 | 2160 | 20.065272 | 5.092276 | 0.468056 | 0.812500 | 0.962500 | 0 |
| c2_aci_gamma_0.000001 | fold_5 | 2156 | 23.168349 | 6.080081 | 0.514842 | 0.786642 | 0.923933 | 0 |
| c2_aci_gamma_0.000005 | fold_1 | 2160 | 6.613025 | 1.826334 | 0.391204 | 0.678704 | 0.896296 | 0 |
| c2_aci_gamma_0.000005 | fold_2 | 2159 | 20.039140 | 4.863304 | 0.238073 | 0.509032 | 0.883279 | 0 |
| c2_aci_gamma_0.000005 | fold_3 | 2112 | 140.992933 | 39.905490 | 0.208807 | 0.354167 | 0.559186 | 0 |
| c2_aci_gamma_0.000005 | fold_4 | 2160 | 20.065326 | 5.092277 | 0.468519 | 0.812500 | 0.962500 | 0 |
| c2_aci_gamma_0.000005 | fold_5 | 2156 | 23.168349 | 6.079509 | 0.514842 | 0.786642 | 0.923933 | 0 |
| c2_aci_gamma_0.00001 | fold_1 | 2160 | 6.613101 | 1.825061 | 0.391204 | 0.681481 | 0.896759 | 0 |
| c2_aci_gamma_0.00001 | fold_2 | 2159 | 20.039131 | 4.855656 | 0.238073 | 0.510885 | 0.884206 | 0 |
| c2_aci_gamma_0.00001 | fold_3 | 2112 | 140.992999 | 39.825846 | 0.208807 | 0.355114 | 0.565341 | 0 |
| c2_aci_gamma_0.00001 | fold_4 | 2160 | 20.065332 | 5.092243 | 0.468981 | 0.812963 | 0.962500 | 0 |
| c2_aci_gamma_0.00001 | fold_5 | 2156 | 23.168352 | 6.079962 | 0.514842 | 0.786642 | 0.923933 | 0 |
| c2_aci_gamma_0.00002 | fold_1 | 2160 | 6.613452 | 1.823597 | 0.392130 | 0.684259 | 0.897222 | 0 |
| c2_aci_gamma_0.00002 | fold_2 | 2159 | 20.039123 | 4.846941 | 0.238073 | 0.514127 | 0.886522 | 0 |
| c2_aci_gamma_0.00002 | fold_3 | 2112 | 140.993556 | 39.631560 | 0.210701 | 0.359848 | 0.573390 | 0 |
| c2_aci_gamma_0.00002 | fold_4 | 2160 | 20.065445 | 5.092233 | 0.469444 | 0.812963 | 0.962037 | 0 |
| c2_aci_gamma_0.00002 | fold_5 | 2156 | 23.168387 | 6.080761 | 0.513451 | 0.785714 | 0.924397 | 0 |
| v1_reference | fold_1 | 2160 | 6.612889 | 1.828029 | 0.390278 | 0.676389 | 0.894444 | 0 |
| v1_reference | fold_2 | 2159 | 20.039141 | 4.868724 | 0.237147 | 0.506253 | 0.883279 | 0 |
| v1_reference | fold_3 | 2112 | 140.992852 | 39.975234 | 0.208807 | 0.352746 | 0.555398 | 0 |
| v1_reference | fold_4 | 2160 | 20.065272 | 5.092276 | 0.468056 | 0.812500 | 0.962500 | 0 |
| v1_reference | fold_5 | 2156 | 23.168349 | 6.080453 | 0.514842 | 0.786642 | 0.923933 | 0 |

## Frozen implementation choices and limitations

- `protocol.json` was committed at `5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed`, before calibration implementation or comparison execution. No parameter changed after viewing candidate results.
- C-1 normalises signed conformity scores before the exact one-based order statistic, then multiplies by the prediction-row scale. Raw spread is `raw_p95 - raw_p05`, without sorting heads first. Both scales have a fixed 1 EUR/MWh floor. Trailing volatility uses sample standard deviation of exactly 168 canonical hours ending before local delivery-day midnight. This is the inherited D-1 day-ahead price boundary, independently controlled with D masking and a D-1 mutation.
- C-2 uses one coverage state per symmetric pair: `c = 1 - paper_alpha`. With `target = nominal coverage`, `c += gamma * (target - hit)` is the exact equation in v20. It is algebraically the complement of the paper's miscoverage update. Each released hourly hit is applied once; all hours in one delivery day receive the same pre-origin state. The reference score reservoir is the initial unscaled calibration slice and stays fixed.
- C-2 only releases previously emitted predictions for delivery days through D-2, after validating complete 23/24/25-hour daily price availability. It does not use calibration outcomes as adaptive replay, embargo-day predictions, D-1 feedback or same-day feedback. The last two evaluation days have no feedback consumer within the fold. `aci_trace.csv` records each origin's cutoff, cumulative feedback count, coverage states and ranks.
- Gamma grid: 0.000001, 0.000005, 0.00001, 0.00002 per hourly feedback event. The upper bound is deliberately conservative: even 2,161 consecutive misses keep the 95% state below 0.991059, within finite ranks for these calibration samples. No state or rank clipping is used. This does not test rapidly adapting ACI or a rolling score reservoir; the null crisis result cannot rule out those variants. No delayed long-run coverage guarantee is claimed.
- Isotonic regression is last, including before deciding which previously emitted intervals covered their realised labels. Small median changes can arise from the final projection; no point-forecast improvement is the claim.
- C-3 is rejected and not implemented, exactly as §4.3 requires: a regime taxonomy based on hindsight dates violates the anti-overtuning rule. No crisis flag or hindsight date threshold is supplied to a calibrator. The two fixed August dates appear only in the reporting diagnostic inherited from v1.
- Prices, forecasts and eligibility are inherited from the frozen v1 development evidence. Inputs were not refit or reselected. Every saved target/date is matched to the original base-feature eligibility mask, and v1's saved final vectors replay with maximum absolute difference exactly 0.0. `lineage.json` contains input/source hashes, row counts and the latest price timestamp. The data loader filters before the reserved tail partitions.

## Verification and reproduction

Run from the repository root with the pinned `uv.lock`:

```sh
uv run --frozen pytest -q
uv run --frozen python scripts/cp10_calibration.py --output /tmp/cp10-repro
```

For a fresh checkout, first materialise the ignored v1 browser payload required by the existing regression suite. This performs frozen-model identity replay, not a new holdout performance evaluation; the tracked v1 manifest is redirected to a temporary file:

```sh
uv run --frozen python - <<'PY'
from pathlib import Path
import runpy
ns = runpy.run_path("scripts/build_wasm_payload.py", run_name="cp10_test_setup")
ns["main"].__globals__["MANIFEST"] = Path("/tmp/cp10-payload-manifest.json")
raise SystemExit(ns["main"]())
PY
```

The second command emits `metrics.csv`, `peak_windows.csv`, `predictions.parquet`, `aci_trace.csv`, `selection.json`, `lineage.json` and this `report.md`. Compare each file byte-for-byte with `reports/cp10/`. `protocol.json` is the pre-run input, not regenerated output. All computation is local CPU; no credentials, network requests, experiment writes or new dependencies are needed.

Exact and adversarial tests are in `tests/test_25_cp10_calibration.py`; independent recomputation from every emitted prediction is in `tests/test_26_cp10_evidence.py`. Existing unscaled rank fixtures (`test_10`), schema firewall controls (`test_05`), and feature/champion masking controls (`test_02`, `test_13`) remain in the complete suite. Every new negative behavioural assertion has a matching mutation, accepted input or corruption control. The pre-review baseline suite had 191 passing tests.

The first driver attempt was interrupted before any candidate metrics when mixed UTC timezone representations caused repeated pandas object-index hashing. Normalising the driver's timestamp index to UTC fixed the performance issue without changing instants, inputs, formulas or parameters. Completed reproduction runs are deterministic. This report is generated by `scripts/cp10_calibration.py`.

## Sources and evidence class

Data: Bundesnetzagentur / SMARD.de, CC BY 4.0. Attribution and the frozen ingestion record remain in `data/README.md` and `data/source_manifest.json`. No data were downloaded for CP-10.

ACI equation reference: [Gibbs and Candès (2021), §2, equation (2)](https://arxiv.org/html/2106.00170v3). The coverage-state complement is an algebraic implementation choice documented above; the conservative grid and delayed fixed-reservoir experiment are this checkpoint's choices, not claims attributed to the paper.

All results here are development calibration evidence. The preserved v1 report, point-MAE p=0.948, holdout evidence, champion, snapshot, partition manifest, closed experiment and release/evidence tags are untouched. Integration acceptance is recorded separately in the checkpoint verdict.
