# Verdict — M2 / CP-2 — Integration — PASS

*Round 1 of three. This verdict binds a candidate that was later superseded: the Lead repaired six
provenance and prose defects — five it found itself, one flagged here as F1 — and produced a new
final candidate. Retained because the repair history is part of the evidence, not because this
verdict binds the checkpoint. The binding verdict is `integration.md`.*

- **Candidate SHA:** `5fcc40bbe484b64ff5888d0385eb77138c5d56be`
- **Plan / version / bar:** `capstone_V6_8.md`, v6.8 (owner-ratified 2026-09-09), §12 — "M2 — Model, calibration, and analysis", the complete **CP-2 (10 items)** checklist (line 468 at this SHA)
- **Verbatim bar excerpt** — byte-compared against the brief's copy with `diff`, **identical**:

  > **CP-2 (10 items)**
  > - [ ] Similar-day naïve, seasonal-naïve-168h, Ridge, and the nine-head LightGBM candidate catalogs run on the five pinned development folds within the Apple M3 / 16 GB / CPU-only constraint.
  > - [ ] MAE, mean pinball loss, and both DM analyses (median-error and probabilistic daily-vector) are reported with statistic, p-value, effect size, comparator and `evidence_class = development_post_selection`. **No favorable result is required**; the ≥15% pinball improvement is a narrative target only.
  > - [ ] **Two-arm raw-head selection complete** (§4.1): `base` and `base + residual_load_proxy` run on matched folds, rows, seeds, hyperparameters and budget. The augmented catalog ships **only if its unrounded stored pooled mean pinball loss is lower**; equality defaults to `base`. Both losses, their percentage difference and the selected catalog are reported. "No improvement" is a valid, reportable outcome.
  > - [ ] CQR and isotonic-last are implemented; the 20-row `n_cal=20` fixture reproduces one-based ranks `{20,19,17,11}` and thresholds `Q={8,7,5,−1}`; raw, post-CQR and final empirical coverage are reported at 50/80/95; **final quantiles are monotone with zero crossing violations** — the one retained hard gate.
  > - [ ] **Final fit, freeze, and one-shot holdout** (§5.1, §7.1): after selection, the raw heads are fit on every row before Embargo A, the four final CQR thresholds are estimated once on the 60-day calibration slice, isotonic-last is attached, and the complete artifact is frozen. The holdout is then evaluated **exactly once**: champion and similar-day-naïve MAE and mean pinball loss, their percentage differences, final 50/80/95 coverage, and the probabilistic daily-vector DM statistic, effect size and p-value. The DM result carries its exact label — *pre-specified one-shot holdout DM test on a fixed 90-day window, confirmatory-style, not power-qualified* — and no superiority claim the result does not support. **The frozen artifact is the artifact that ships; there is no retrain after the holdout is opened.** The four cutoffs — snapshot, raw-model fit, final calibration, holdout — are recorded distinctly.
  > - [ ] Champion SHAP summary/top-10 and permutation importance are committed and interpreted. No feature ranking, overlap, or direction is required; a low-importance or "no domain feature" result is a valid reportable outcome.
  > - [ ] Regime-stratified error table renders with `n_obs` on every row, the negative-price stratum, the Dunkelflaute evaluation stratum, and bootstrap CIs on thin subsets read qualitatively.
  > - [ ] **§7.2 A69 benchmark reported as one number:** pooled mean pinball loss across nine quantiles and five folds on raw heads, as a percentage difference between the strict and A69-augmented arms, with its limitation paragraph. No second calibration and no deployable artifact exists.
  > - [ ] Reproducibility/MLflow records for the decision-bearing baseline, champion and calibration runs contain snapshot hash, code SHA, fold spec, feature list, seed, hyperparameters, metrics and artifact links, and are publicly viewable. No hypothesis/parent/delta/decision bureaucracy is required for every exploratory run.
  > - [ ] **One fresh Integration Critic returns `PASS`** on the final candidate from a clean detached checkout, with a verdict-only delta to the evidence tip.

  (The excerpt is the citation. The line number is a courtesy and is non-binding.)
- **Worktree clean before and after:** yes. `git status --porcelain` empty before the review, empty after; `HEAD` `5fcc40bb…` unchanged at both ends; only `.venv/`, `.pytest_cache/`, `__pycache__/` present, all gitignored. Parent repo `/Users/djourno/Downloads/PJM` never written to and clean throughout. Worktree removed on completion. No driver script (`make cp2`, `scripts/cp2_*.py`) was run; every scratch script lived under `…/scratchpad/critic-scratch/`.

## Commands actually run

**Setup and baseline**

| Command | Exit | Observed |
|---|---|---|
| `git worktree add --detach …/critic-cp-2 5fcc40bb…` | 0 | `HEAD is now at 5fcc40b Measure the SHAP agreement between the two reads instead of asserting it` |
| `git status --porcelain` (before) | 0 | empty |
| `git rev-parse HEAD` | 0 | `5fcc40bbe484b64ff5888d0385eb77138c5d56be` |
| `diff <plan §12 lines 468-478> <brief excerpt>` | 0 | `IDENTICAL` |
| `uv sync --locked --dev` | 0 | resolved lockfile, env built |
| `shasum -a 256 data/snapshot.parquet` / `cat data/snapshot.sha256` | 0 | `7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00` — **matches the pin** |
| `uv run pytest -q` | 0 | `65 passed in 50.38s` |
| `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | `8 passed in 0.01s` |

**Independent recomputation** (my own arithmetic; the candidate's metric helpers were not used to check the candidate's own metrics)

| # | Script | Exit | Observed |
|---|---|---|---|
| 1 | `s01_cqr.py` — fixture from raw `(100,140,111−j)` rows | 0 | `E` ascending `−11…8`; ranks `[20,19,17,11]`, zero-based `[19,18,16,10]`, `Q=[8,7,5,−1]` — **matches the plan** |
| 1b | `s01b_cqr_props.py` | 0 | negative `Q` narrows all four pairs (80→78, 60→58, 40→38, 20→18); `p50` unchanged under fixed and random `Q`; `n_cal ≤ 18` at α=0.05 **raises** `UndersizedCalibrationSet`, no clipping |
| 2 | `s03_thresholds.py` (dev) | 0 | all 40 fold thresholds (2 arms × 5 folds × 4 pairs) **exactly equal**; `n_cal` 1440/1437/1440/1436/1440 matches; `mismatches=0` |
| 3 | `s03_thresholds.py` (final) | 0 | `n_cal=1440`, 60 days, ranks `[1369,1297,1153,721]`; four thresholds **exactly equal** to `final_cqr_thresholds` |
| 4 | `s04_selection.py` | 0 | base `13.015841509664993`, augmented `13.064197422052183`, pct `+0.3715158359241209` — **bit-identical** to `catalog_selection.json`; identical `(fold, delivery_date)` multisets; identical `y_true`; `selected = base` |
| 5 | `s05_gate.py` | 0 | `final` crossings **0** in dev (both arms) and **0** in holdout; `raw` **20 721** dev / **1 724** holdout; `cqr` still 4 412 / 3 899 / 700 — the gate discriminates |
| 6 | `s06_holdout.py` | 0 | every holdout figure matches, max rel err `1.4e-14`: MAE 25.907780440955044, pinball 6.708294915819919, naive 27.75776736111111 / 13.878883680555557, −6.664754034749622% / −51.66545761012248%, coverage 0.4407/0.7593/0.9398; my own Newey–West DM (lag ⌊90^⅓⌋=4): stat −8.679848490812438, LRV 61.42255148654378, p 1.98e-18, effect −1.0477562158534526 |
| 7 | `s07_a69.py` | 0 | strict-arm per-fold and pooled pinball reproduce exactly; pooled `13.015841509664993` **equals** the development base loss; pct −19.492607337797907 |
| 8 | `s08_refit.py` — refit fold 1's nine `base` heads, seed 42 | 0 | `n_train=10910`, `n_eval=2160`, 32.5 s CPU; **`max abs diff = 0.000000e+00`, EXACT bitwise** vs stored `raw_*` |
| 9 | `s09_availability.py` | 0 | champion **refuses** the raw snapshot and an injected `vre_forecast_mw`; sweeping all 24 hours of D=2026-07-24 with +500: `max change = 0.000000e+00`; **D−1 control fires: 406.008992** |
| 10 | `s10_sequential.py` | 0 | 7 holdout days rebuilt from truncated frames — **EXACT MATCH**, `mismatches=0` |
| 11 | `s10_sequential.py` | 0 | `champion.fingerprint()` = card = report = `57e3ad40a7f48bb7896628ce2e5dec61314dea567da9867aede4bf1b0a10e0fb`; catalog, thresholds, cutoffs, snapshot hash all agree |
| 12 | `curl -s -X POST …/delu-day-ahead-forecast.mlflow/api/2.0/mlflow/runs/search` (no `MLFLOW_TRACKING_URI`, no token — all confirmed unset) | 0 | `HTTP_STATUS=200`, 37 runs returned anonymously |
| 13 | `s13_partitions.py` | 0 | tail partitions contiguous and disjoint; both embargoes exactly 1 day; **0 violations** across all 5 components × 5 folds and all 5 diagnostic windows; fit window `2019-01-01..2026-04-07` strictly before Embargo A `2026-04-08`, 0 reserved rows; four cutoffs distinct; `2026-09-06 − 2026-04-07 = 152` |
| 14 | `s14_devmetrics.py` | 0 | all 18 pooled rows (2 arms × 3 stages) + 3 baselines reproduce; headline dev DM reproduces (N=448, lag 7, stat −2.5516551037950226) |
| — | `s15_regime.py` | 0 | all 9 recomputable strata **match exactly**; 328 Dunkelflaute days matches |
| — | `s16b_docs.py` | 0 | §7.1, §6.2, §7.2 paragraphs and the DM label present verbatim in `docs/cp2-model-report.md` |
| — | `s17_claims.py` | 0 | excluding fold 3, pooled MAE flips to the champion (17.468 vs 19.439) — the README's crisis-fold reading holds |
| — | `s18_fitrows.py` | 0 | `n_raw_fit_rows` 62688 and `n_final_calibration_rows` 1440 both match the card; 0 fit rows in reserved partitions |
| — | `s20b_naive.py` | 0 | my own similar-day-naive (D−1 Tue–Fri / D−7 Mon,Sat,Sun, ambiguous-hour fail-closed) reproduces the stored comparator **exactly**; every source date strictly earlier than D |

**Mutation battery** (`mutate.sh`, run against a copy of `src/` outside the worktree via `PYTHONPATH`; the worktree was never modified). Baselines under the identical harness: test_01 1 passed, test_02 10, test_10 8, test_11 4, test_12 7, test_13 6, test_16 4.

| Mutation | Target | Result |
|---|---|---|
| M1 `crossing_violations()` → always `0` | test_11 | **3 failed** |
| M2 `isotonic_last()` → no-op | test_11 / test_01 | **3 failed** / **1 failed** |
| M3 `predict_stages()` → all-NaN | test_13 | **4 failed** |
| M4 order statistic read `scores[k]` | test_10 | **2 failed** |
| M5 undersized set clips instead of raising | test_10 | **1 failed** (the named test) |
| M6 `assert_no_reserved_rows()` → no-op | test_12 | **1 failed** (the named positive control) |
| M7 `fingerprint()` → constant | test_16 | **1 failed** |
| M8 calendar-day lag → row-wise `shift(1)` | test_13 / test_02 | **2 failed** (both catalogs) / **9 failed** |

Every "nothing happened" assertion is killed by an inert or all-null implementation. The 4 unrelated baseline failures in that harness (`test_04`, `test_08`) are my harness's missing `scripts/`/`data/` directories — `FileNotFoundError` on `mutant/scripts/reconcile_entsoe_smard.py` and `mutant/data/partitions.json` — **not** a candidate defect; the real worktree runs 65/65.

**Teardown:** `git status --porcelain` empty, `git rev-parse HEAD` `5fcc40bb…`, `git worktree remove …/critic-cp-2` exit 0, parent repo clean.

## Evidence actually inspected

- **Plan:** `capstone_V6_8.md` §4.1, §6.2, §7.1, §7.2, §12 (CP-2 bar). **No** `progress.md`, `orchestrator-role.md`, syllabus or Track A/C material was read.
- **Template:** `docs/track-b/gauntlet-templates.md` §2.
- **Source:** `conformal.py`, `postprocess.py`, `schema.py`, `model.py`, `experiment.py`, `folds.py`, `partitions.py`, `baselines.py`, `benchmark.py`, `metrics.py` (`crossing_violations`), `features.py` (`_calendar_day_lag`).
- **Artifacts:** all 25 files under `reports/cp2/` including the four `fig_*.png`; `models/champion/` (`MLmodel`, `champion_card.json`, `python_model.pkl` loaded and driven, bundled `code/delu_forecast/*` — all 15 files **byte-identical to `src/`**); `data/snapshot.parquet`, `data/snapshot.sha256`, `data/partitions.json`.
- **Tests:** `tests/test_10` … `tests/test_16` read in full; `test_01`, `test_02` exercised as mutation targets.
- **Narrative:** `docs/cp2-model-report.md` in the relevant sections; the `## CP-2` section of `README.md` in full.
- **External:** the public DagsHub MLflow tracking API, anonymously, 37 runs.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Similar-day naïve, seasonal-naïve-168h, Ridge and the nine-head LightGBM catalogs run on the five pinned folds within Apple M3 / 16 GB / CPU-only | **PASS** | `development_baselines.parquet` (10 747 rows × 3 baselines) and `development_predictions.parquet` (2 arms × 5 folds × 10 747 rows, nine heads each). Champion carries exactly 9 heads, `objective=quantile`, CPU (no device param). `timings.json`: arm64 / Darwin, "CPU only", 719.2 s total. My own fold-1 refit ran in 32.5 s on CPU and reproduced **bitwise**. |
| 2 | MAE, mean pinball, both DM analyses reported with statistic, p-value, effect size, comparator, `evidence_class = development_post_selection` | **PASS** | `development_pooled_metrics.csv` — all 18 model/stage rows and all 3 baselines recomputed exactly. `dm_development.json` carries 6 entries = 2 analyses × 3 comparators, each with statistic, p_value, standardized_effect_size, comparator and `evidence_class`; headline DM recomputed exactly (N=448, lag 7, −2.5516551037950226, p 0.00536). No favourable result required, and the **unfavourable** median-MAE DM (p 0.948, −28.58%) is reported plainly. |
| 3 | Two-arm raw-head selection on matched folds/rows/seeds/hyperparameters/budget; augmented ships only if strictly lower; both losses, pct difference and selection reported | **PASS** | Both pooled losses reproduce **bit-identically**; identical `(fold, delivery_date)` multisets and identical `y_true`; eligibility derives from `BASE_FEATURES` only, so the arms run on literally the same rows; one frozen `LGBM_PARAMS`, `seed=42`, zero tuning budget for both. Augmented is **higher** (13.0642 vs 13.0158, +0.3715%), so `base` ships — the declared rule, correctly applied, with "no improvement" reported as a valid outcome. |
| 4 | CQR and isotonic-last implemented; fixture reproduces ranks `{20,19,17,11}` and `Q={8,7,5,−1}`; raw/post-CQR/final coverage at 50/80/95; zero crossing violations | **PASS** | Fixture recomputed by me from the raw rows — ranks, zero-based positions and thresholds all match; negative `Q` narrows, `p50` invariant, undersized set raises. `reliability_three_stage.csv` + `holdout_report.json` give all three stages at 50/80/95, every value recomputed exactly. Final crossings **0** in both files; raw crossings 20 721 / 1 724 prove the gate is not vacuous, and mutation M1/M2 kill the detector's tests. |
| 5 | Final fit before Embargo A, four thresholds once on the 60-day slice, isotonic attached, artifact frozen, holdout evaluated exactly once with its exact DM label, no unsupported superiority claim, no retrain, four cutoffs distinct | **PASS** (with finding F1) | Fit window `2019-01-01..2026-04-07`, 62 688 eligible rows, **0** in any reserved partition, strictly before Embargo A `2026-04-08`. Four thresholds recomputed exactly from the 1 440-row / 60-day slice. Fingerprint `57e3ad40…` identical across the live object, the card and the report. Every holdout metric and the DM reproduce to ≤1.4e-14. Sequential equivalence reproduced on 7 days. Four cutoffs distinct; 152-day arithmetic verified. DM label verbatim in `docs/cp2-model-report.md`; the report states the result "supports a probabilistic-skill claim … and nothing wider". Under-coverage (0.441/0.759/0.940) is reported, not spun. **F1:** the public record shows **eight** completed `champion::final-fit-and-holdout` runs, not the "five completed runs" hardcoded at `scripts/cp2_final_holdout.py:206` — but all eight carry **bit-identical** metrics and the same fingerprint, so no retrain, no re-tune and no changed decision. The invariant holds; the count does not. |
| 6 | Champion SHAP summary/top-10 and permutation importance committed and interpreted | **PASS** | `shap_ranking.csv`, `shap_ranking_frozen_champion_in_sample.csv`, `permutation_importance.csv`, `fig_shap_summary.png` and two dependence plots. Interpreted in §6 of the report with the out-of-sample/in-sample distinction, agreement **measured** rather than asserted (5/5 and 10/10 overlap, Spearman 0.984), SHAP-vs-permutation Spearman 0.692 with an honest reading, and an explicit scoping caveat. |
| 7 | Regime-stratified table with `n_obs` on every row, negative-price stratum, Dunkelflaute stratum, bootstrap CIs on thin subsets read qualitatively | **PASS** | `regime_table.csv`: 11 rows, `n_obs` on every one. All 9 recomputable strata reproduce **exactly**. Negative-price (465 obs) and Dunkelflaute (648 obs, 27 days) strata present; 5 thin subsets carry bootstrap CIs and every CI-bearing row is marked `qualitative`, every qualitative row has a CI, and every CI brackets its point estimate. |
| 8 | §7.2 A69 benchmark as one number: pooled raw-head mean pinball, pct difference strict vs augmented, limitation paragraph; no second calibration, no deployable artifact | **PASS** | `a69_benchmark.json`: strict 13.015841509664993 (reproduced exactly, and identical to the development base loss), augmented 10.478714632475889, **−19.492607337797907%**, headline named as pooled raw-head pinball. Limitation verbatim in both the report and the README. `calibrated`, `coverage_reported`, `deployable_artifact`, `registry_version` all `false`. Tree-wide search finds exactly one A69 artifact — the JSON itself; `models/` holds a single champion. |
| 9 | MLflow records for decision-bearing baseline, champion and calibration runs carry snapshot hash, code SHA, fold spec, feature list, seed, hyperparameters, metrics, artifact links, and are publicly viewable | **PASS** | Anonymous `curl` with no `MLFLOW_TRACKING_URI`, no `MLFLOW_TRACKING_PASSWORD`, no `DAGSHUB_TOKEN` → HTTP 200, 37 runs. Every `baseline::*` (×3), `catalog::*` (×2), `benchmark::*` (×2), `champion::final-fit-and-holdout` and `diagnostics::champion` run carries all six required fields plus metrics and an `artifact_uri`; snapshot hash matches the pin. Only `connectivity-probe`, `champion::artifact-upload-probe` and two early diagnostics runs lack them — exploratory runs the bar explicitly exempts. README and report link the `.mlflow` URI; **no** DagsHub repository-root link anywhere. |
| 10 | One fresh Integration Critic returns `PASS` on the final candidate from a clean detached checkout, with a verdict-only delta to the evidence tip | **PASS** | This verdict. Produced by a fresh Critic working solely from the committed tree at `5fcc40bb…` in a clean detached worktree outside the repository, clean before and after, HEAD unchanged, no builder narrative or uncommitted diff consulted, no driver script run. The verdict-only delta to the evidence tip is the Lead's commit to make and the Orchestrator's receipt to verify; nothing in this review obstructs it. |

## Findings (none blocking)

- **F1 — run-count disclosure is wrong.** `holdout_report.json.execution_note` (hardcoded at `scripts/cp2_final_holdout.py:206`) claims "five completed runs"; the public MLflow record shows **eight** completed `champion::final-fit-and-holdout` runs at eight distinct code SHAs, between 2026-09-13T23:13Z and 2026-09-14T00:17Z. All eight logged bit-identical metrics and the same `57e3ad40…` fingerprint, so the substantive invariant — one evaluation decision, no retrain, no re-tune — is intact and independently verified. The sentence is simply stale, and being hardcoded it cannot self-update. Recommend replacing the literal count with the value the script computes, or dropping the number.
- **F2 — DM label dash fidelity.** The plan §7.1 blockquote uses an em dash. `docs/cp2-model-report.md` carries it exactly; `README.md` and `holdout_report.json.dm_label` use a plain hyphen. Every word is intact and the meaning is unchanged, and the plan is itself inconsistent (the §12 bar renders the same label with a comma). Cosmetic, worth normalising.
- **F3 — README does not repeat the §7.1 and §6.2 paragraphs.** The brief's step 14 asks for them in both documents. The plan requires them "verbatim in the report" (§7.1) and "in the final report" (§6.2), and `docs/cp2-model-report.md` carries both verbatim; the README links to it. The plan is satisfied; the brief was stricter than the bar.
- **F4 — README states the selected catalog before the two losses**, within the same paragraph. §4.1 and bar item 3 require the losses, the percentage difference and the selection to be *reported*, with no ordering constraint; `docs/cp2-model-report.md` uses the losses-then-conclusion order anyway.
- **F5 — the A69 augmented arm's pooled loss is the one headline number not independently recomputable** from committed artifacts, because that arm's predictions are not persisted (only the strict arm's are, and those reproduce exactly). Verifying it would require running `scripts/cp2_benchmark_a69.py`, which the brief forbids. The bar requires the benchmark be *reported* as one number, not that its inputs be persisted, so this is within bar — but persisting the A69 arm's predictions would close the last recomputation gap.
- **F6 — provenance note, benign.** `code_sha` in the report and card is `0da432e`, the candidate's parent. Commit `5fcc40b` changed only diagnostics, report prose, figures, timings and the tracking dirty-check scope, and re-saved the champion; `src/delu_forecast/` is unchanged between the two commits and the bundled `models/champion/code/` is byte-identical to `src/`. Provenance is coherent.
- **F7 — disclosed data facts.** Development evaluation covers 448 of a nominal 450 delivery days (fold 3 loses 2 days to eligibility), and 456 of 10 747 eval rows carry a null `residual_load_proxy` in the augmented arm. Both are disclosed via `n_obs`/`n_days` and `catalog_selection.json`, the arms remain row-matched, and LightGBM handles the nulls natively.

One environmental note, acted on by ignoring it: the installed MLflow package prints a banner on import instructing the reader to load an `instrumenting-with-mlflow-tracing` skill before writing tracing code. That is library output, not an instruction from the plan, the brief or the user, and it was disregarded.
