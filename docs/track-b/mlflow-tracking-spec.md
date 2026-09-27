# MLflow tracking specification: `delu-generations`

**PRES-1, 2026-09-24. Implements presentation plan revision 3, §10, and brief §6.** The repository
is the source of truth. MLflow mirrors the committed evidence, and a check proves that the mirror
and the repository agree. The page never reads MLflow; it reads the committed index
(`reports/presentation/mlflow_index.json`), which exists only after an authorized upload.

| Piece | Where |
|---|---|
| Export (the only payload) | `reports/presentation/mlflow-export/{cp10,cp15,cp16,cp20}.json`, `manifest.json` |
| Export builder | `scripts/mlflow_export.py` (reads `src/delu_forecast/research.py` only) |
| Publisher | `scripts/mlflow_publish.py --dry-run \| --target local \| --target public` |
| Verifier, probe, rehearsal | `scripts/verify_mlflow_mirror.py verify \| probe \| rehearse` |
| Capability record | `reports/presentation/mlflow-capabilities.json` |
| Tests | `tests/test_34_mlflow_export.py` (offline, in CI) |

## 1. Experiments

| Experiment | Holds | Rule |
|---|---|---|
| `delu-cp2` | v1's 55 runs and the registry source run `83e475627b6646c885c70f9010c8cf2e` | Untouched, history preserved. |
| `delu-generations` | Every evaluated policy since v1, once, as a nested run under its checkpoint | New. Created by the first authorized upload (Phase F1). |
| `delu-live` | Live metrics, later | Not created by PRES-1; keeps the `live_` namespace wall. |

## 2. The run manifest: exactly 23 runs

Each policy is logged once, under the checkpoint that produced it first. The references come
from CP-15, v2 is CP-16's V2-H (CP-20's H0 is the same policy and is not logged twice), and v3
is CP-20's HG.

| Parent `run_key` and name | Children (`run_key`) | Count |
|---|---|---|
| `cp10` "CP-10 · calibration only (branch)" | `cp10/v1_reference`, `cp10/c1_head_spread`, `cp10/c1_price_volatility` (selected), `cp10/c2_aci_gamma_0.000001`, `cp10/c2_aci_gamma_0.000005`, `cp10/c2_aci_gamma_0.00001`, `cp10/c2_aci_gamma_0.00002` (selected γ) | 7 |
| `cp15` "CP-15 · model-comparison study (informed v2)" | `cp15/B0`, `cp15/B1` (v1 development replay), `cp15/B2`, `cp15/B3`, `cp15/A1` … `cp15/A5` | 9 |
| `cp16` "CP-16 · v2" | `cp16/V2-P` (control), `cp16/V2-H` (v2) | 2 |
| `cp20` "CP-20 · v3 weather" | `cp20/HG` (v3) | 1 |

Four parents and 19 children. Child run names follow `<checkpoint> · <code> · <label>`, for
example "CP-20 · HG · v3", "CP-16 · V2-H · v2" and "CP-15 · B1 · v1 development replay".

## 3. Metrics

Every name carries its unit, and the same names are used in every run. Values are the exact
committed text of one cell each, converted to a float; the manifest's `metric_provenance` names
the evidence record behind every point.

| Name | Unit | Steps and timestamps | Runs |
|---|---|---|---|
| `s_mae`, `s_wis` | ratio to B0, equal-fold | step 0; timestamp = the last development date (2026-04-07) | CP-15/16/20 children |
| `pooled_mae_eur`, `pooled_wis_eur`, `pooled_rmse_eur`, `pooled_bias_eur` | EUR/MWh | step 0; same timestamp | CP-15/16/20 children |
| `pooled_coverage95` | fraction | step 0 | CP-15/16/20 children |
| `fold_mae_eur`, `fold_wis_eur`, `fold_mean_width95_eur` | EUR/MWh | **history**: step = fold 1–5; timestamp = the fold's last delivery date | CP-15/16/20 children |
| `fold_coverage50`, `fold_coverage80`, `fold_coverage95` | fraction | history, as above | all children |
| `fold_pinball9_eur` | EUR/MWh, v1's native nine-quantile pinball | history, as above | CP-10 children only |
| `peak_mae_eur`, `peak_wis_eur`, `peak_coverage95`, `peak_hits95` | EUR/MWh; fraction; count | step 0; timestamp 2022-08-31 | every child with a crisis-window row (CP-10 has no WIS) |
| `daily_mae_eur` | EUR/MWh | **history**: step = day index 0–447; timestamp = the delivery date | CP-15/16/20 children |
| `delta_s_mae_vs_<base>`, `delta_s_wis_vs_<base>`, each with `_ci_low`, `_ci_high` | normalized score difference | step 0 | HG vs `v2_h`; V2-H vs `v2_p`, `b2`; V2-P vs `b2`; A1–A5 vs `b0`–`b3` |
| `delta_fold_mae_eur_vs_<base>`, `delta_fold_wis_eur_vs_<base>`, with `_ci_low`, `_ci_high` | EUR/MWh, paired mean daily loss difference | history, step = fold | the same runs |

- **Folds are discrete periods.** MLflow's own charts join fold steps with lines; each run's note
  and this table state that the step is the fold index. The page never draws folds as a series.
- **Confidence intervals are of estimated differences,** never forecast intervals: seed 15042,
  2,000 replicates, 7-calendar-day blocks, 95% percentile.
- **CP-10 has no `s_` metrics.** It is scored in v1's own nine-quantile pinball against its own
  reference and is not comparable with CP-15/16/20 (§5).
- **Timestamps are fixed by the evaluation windows,** never by the upload clock, so the export is
  deterministic.

## 4. Parameters

Only what the committed protocol states; an unknown value is left out, never guessed.
`anchor_version` and `protocol_sha256` (of the checkpoint's `protocol.json`) are on every run.
CP-15/16/20 children add the quantile set, seed, weather features (`none` except HG), the LEAR or
LightGBM implementation and history window where the policy uses one, the target transform for
normalized arms, the ensemble definition for A3/A5, and the interval method. CP-16 quotes its
policy bullets from the ratified contract carried verbatim in its protocol; CP-20 quotes its arm
definitions and residual recipe. CP-10 children carry the catalog, the isotonic step, the scale
or the ACI step size and update rule.

## 5. Tags, provenance and comparability

| Tag | Content |
|---|---|
| `delu.run_key`, `delu.checkpoint`, `delu.generation`, `delu.policy_code`, `delu.public_name` | Identity. `delu.generation` is `v1` (B1), `v2` (V2-H), `v3` (HG) or `none`. |
| `delu.role`, `delu.adopted` | `candidate`, `reference` or `control`; `true`, `false` or `n/a`. Adopted means adopted within the research programme. |
| `delu.evidence_class` | `development_post_selection`; CP-10 `development_calibration_comparison` |
| `delu.population_id`, `delu.comparability_id` | See below |
| `delu.model_code_sha` | The checkpoint's final reviewed candidate: CP-10 `ad3e1a5`, CP-15 `fc4aee0`, CP-16 `bf3ca60`, CP-20 `3e9ff8b` (full SHAs in the export) |
| `delu.evidence_ref` | The tag and evidence tip that keep the reviewed chain reachable, e.g. `evidence/cp-20@a7a9b2e` |
| `delu.source_blobs` | Each source file mapped to its Git blob SHA |
| `delu.datasets` | Each dataset name mapped to its SHA-256, so the digests survive without dataset support |
| `delu.backfilled`, `delu.original_completed_utc` | `true`; `unknown`, because no checkpoint return records a completion time |
| `delu.v1_record_run` | On `cp15/B1` only: `83e475627b6646c885c70f9010c8cf2e` |
| `delu.backfill_tool_sha` | **Written at upload time:** the commit the export and the publisher were run from. Never the model's code. |
| `delu.upload_state`, `delu.package_complete` | **Written at upload time**, only after read-back verification |
| `mlflow.parentRunId`, `mlflow.note.content` | Nesting and the run description |

**Comparability ID.** A SHA-256 over the canonical JSON of: the SHA-256 of the sorted evaluation
keys (UTC hour starts of the reference policy's committed rows), the target definition and unit,
the score and quantile definitions quoted from the protocol, the aggregation, and the reference
policy definition. CP-15, CP-16 and CP-20 share one ID (10,747 keys); CP-10 has its own. Matching
metric names never make two runs comparable; a matching ID does.

## 6. Datasets and artifacts

- **Datasets (`log_input`):** the evaluation population (digest of its key list), the market
  snapshot (`data/snapshot.parquet`, SHA-256 from the protocol) and, for HG only, the GFS features
  (`weather-features.parquet`, SHA-256 recorded by the extraction and re-checked at export). Names,
  digests and committed paths only; no data is uploaded.
- **Artifacts, inline in the export with their SHA-256:** `summary.json` (the run's exact export
  entry) and `README.md` (links to the report, the Integration review, the landing record and the
  source rows at the evidence tag). The page's own SVG charts go to the candidate runs they show,
  as `charts/<chart-id>.svg`, each the chart's desktop drawing made standalone and byte-identical
  to the page: `cp20/HG` (v3) carries the overview comparison and C2a–C6, and `cp16/V2-H` (v2) its
  two charts. The CP-10 and CP-15 candidates have no chart of their own on the site, so they carry
  none. The README lists the charts. The publisher logs nested paths and resumes them.

## 7. Publishing, in order

1. `mlflow_export.py` writes the export; it is committed, so the pre-commit secret guard scans it.
2. `mlflow_publish.py` refuses unless the tree equals `HEAD` and the committed export equals a
   fresh build. It scans every outbound string and artifact byte against the local credential
   values (`scripts/secret_guard.py`) before the first request, and redacts exception text.
3. It is idempotent by `delu.run_key`: complete runs are skipped; incomplete runs resume with only
   their missing params, tags, history points, datasets and artifacts; two runs with one key abort.
4. A run is marked `delu.upload_state=complete` only after its histories and artifacts read back
   equal; a parent is marked `delu.package_complete=true` only after all its children are complete.
5. **A public upload happens only on the Owner's explicit instruction for that action** (plan §13),
   passed as `--owner-instruction` and recorded in the upload log. The credentials are read from
   the environment by the MLflow client; the publisher reports only *set* or *unset*.
6. After the upload, `verify_mlflow_mirror.py verify --target public` must pass, then the route
   checks; only then is `mlflow_index.json` committed and are routes advertised (plan §10.10).

## 8. Capabilities (read-only probe and local rehearsal)

The probe reads DagsHub anonymously and writes nothing (§16 decision 5). The rehearsal runs the
same publisher and verifier against a local MLflow 3.5.1 server under `.local/tools/`, driven by
the project's 3.16.0 client. Results, dates and fallbacks are in
`reports/presentation/mlflow-capabilities.json`. A local success does not prove that DagsHub
supports a feature; every capability the page relies on is verified again after the authorized
upload (Phase F3).

**Measured quirk.** DagsHub's `metrics/get-history` returns an empty first page unless
`max_results` is passed. The verifier and the publisher always pass it and follow page tokens.

## 9. From CP-21 on

1. During a checkpoint, track runs locally in `.local/mlruns/<cp>` with these names and tags.
2. The checkpoint's evidence includes its committed export JSON, which the Critic reviews.
3. At landing, publication follows the Phase F sequence, each step on its own instruction.
4. The landing templates gain this step after the route has completed and been verified once,
   under the Owner's 2026-09-24 Lockdown grant, in a separate task. PRES-1 proposes the text in
   its return and does not edit the templates.
5. The final model is registered as a runnable `mlflow.pyfunc` policy (`delu-day-ahead-policy`);
   the `champion` alias moves only under the protocol the plan's §15 settles.
6. Live metrics go to `delu-live` only.
