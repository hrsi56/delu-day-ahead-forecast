# Verdict — M2/CP-2 — Integration — PASS

*Round 3 of three, and the binding verdict for this checkpoint. Rounds 1 and 2 are retained alongside
it at `integration-round-1.md` and `integration-round-2.md`; each bound an earlier candidate that the
Lead superseded by repair. The Lead's response to the findings below, including one it verified as a
misreading, is at `lead-note-on-integration-findings.md`.*

- **Candidate SHA:** `f3a1b7d7a1bddd50fb53c3b85e19327928fba4f0`
- **Plan / version / bar:** `capstone_V6_8.md`, v6.8 (owner-ratified 2026-09-09), §12 — "M2 — Model, calibration, and analysis", the complete **CP-2 (10 items)** checklist (found at line 468).
- **Verbatim bar excerpt** — confirmed present at this SHA. I extracted plan lines 469–478 and byte-diffed them against the brief's excerpt: `diff` returned no output, exit 0, all ten items identical.

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

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- **Worktree clean before and after:** yes. `git status --porcelain` empty immediately after `worktree add` (exit 0), empty again after `uv sync`, and empty at the end of the review with `git diff --stat HEAD` empty; HEAD read `f3a1b7d7a1bddd50fb53c3b85e19327928fba4f0` at both points. Only `.venv/`, `.pytest_cache/` and `__pycache__/` appeared, all gitignored. Worktree removed at the end (exit 0); `/Users/djourno/Downloads/PJM` left clean. No driver script and no `make` target was run.

## Commands actually run

Setup and environment (all from inside the detached worktree unless noted):

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git -C /Users/djourno/Downloads/PJM worktree add --detach …/critic-cp-2-r3 f3a1b7d7…` | 0 | `HEAD is now at f3a1b7d CP-2 final artifacts: regenerated end to end at 525fc2d` |
| 2 | `git status --porcelain` | 0 | empty |
| 3 | `git rev-parse HEAD` | 0 | `f3a1b7d7a1bddd50fb53c3b85e19327928fba4f0` |
| 4 | `diff plan_bar_items.txt brief_bar_items.txt` | 0 | no output — bar excerpt byte-identical, 10 lines each |
| 5 | `uv sync --locked --dev` | 0 | resolved and installed; `git status --porcelain` still empty |
| 6 | `shasum -a 256 data/snapshot.parquet` / `cat data/snapshot.sha256` | 0 | `7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00` — matches the pin |
| 7 | `uv run pytest -q` | 0 | `65 passed in 46.81s` |
| 8 | `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | `8 passed in 0.01s` |

Independent recomputation (my own scripts, all under `…/scratchpad/critic-scratch-r3/`, none inside the worktree):

| # | Command | Exit | Observed |
|---|---|---|---|
| 9 | `uv run python s1_cqr_fixture.py` | 0 | scores `−11…8`; ranks `[20,19,17,11]`, zero-based `[19,18,16,10]`, `Q=[8.0,7.0,5.0,−1.0]` — all `True` |
| 10 | `uv run python s1b_props.py` | 0 | candidate `fit_cqr_thresholds` returns the same four; p25/p75 width `40.0 → 38.0` (negative Q narrows); p50 unchanged on all rows; `n_cal=1/5/18` raise `UndersizedCalibrationSet`, `n_cal=19/20` return `k=19/20`; `cqr_threshold(n=10, α=.05)` raises rather than clipping |
| 11 | `uv run python s2_thresholds.py` | 0 | `STEP2_ALL_EXACT: True` (10 fold×arm threshold sets, exact equality, `n_cal` matches) and `STEP3_EXACT_EQUAL: True` (four final thresholds, `n_cal=1440`) |
| 12 | `uv run python s4_selection.py` | 0 | base `13.015841509664995` vs stored `…993` (rel 1.4e-16); augmented `13.064197422052182` vs `…183` (rel 1.4e-16); pct `0.37151583592409354` vs `0.3715158359241209` (rel 7.4e-14); identical `(fold,delivery_date)` multisets and identical `y_true`; `RULE_APPLIED_CORRECTLY: True` |
| 13 | `uv run python s5_gate.py` | 0 | development `final_` **0** crossings, holdout `final_` **0**; `raw_` **20721** / **1724** and `cqr_` **8311** / **700** — the gate discriminates |
| 14 | `uv run python s6_holdout.py` | 0 | every holdout figure `rel = 0.000e+00` except LRV at 2.3e-16; one deviation flagged (see #15) |
| 15 | `uv run python s6b_effect.py` | 0 | `standardized_effect_size` is `mean(d)/std(d, ddof=1)` (Cohen's d), matching exactly; my first guess used the HAC LRV. Confirmed against `metrics.py:154,166` — the DM statistic itself correctly uses Newey–West |
| 16 | `uv run python s7_a69.py` | 0 | strict `13.015841509664995`, augmented `10.478714632475889`, pct `−19.492607337797917` vs stored `−…907`; strict arm **bitwise equal** to development `base` (`raw_p50` `array_equal True`); identical rows; all ten per-fold values match |
| 17 | `uv run python s8_refit.py` | 0 | fold 1 `base` refit, seed 42: `max ABS diff: 0.0`, **`BITWISE IDENTICAL: True`** on 2160×9 |
| 18 | `uv run python s9_gateday.py` | 0 | champion refuses post-gate A69 frame; perturbing each of D=2026-07-15's 24 hours by +500 changes **0** of D's outputs; mutating one D−1 hour changes **216 of 216** |
| 19 | `uv run python s10_seq.py` | 0 | 8 holdout days rebuilt from truncated frames: `EXACT_EQUAL=True`, `max_abs_diff=0.0` on every one |
| 20 | `uv run python s11_identity.py` | 0 | `fingerprint()` = card = report = `57e3ad40a7f4…0fb`; catalog, thresholds and cutoffs agree across model/card/report |
| 21 | `env | grep -iE "mlflow\|dagshub"` | 1 | no credential in environment |
| 22 | `curl -s -X POST …/delu-day-ahead-forecast.mlflow/api/2.0/mlflow/runs/search -d '{"experiment_ids":["0"],"max_results":60}'` | 0 | `HTTP=200` anonymously, 55 runs |
| 23 | `uv run python s12_mlflow.py` / `s12b_champ.py` / `s12c.py` | 0 | all `baseline::*`, `catalog::*`, `benchmark::*`, `champion::final-fit-and-holdout` carry snapshot hash, code SHA, fold spec, feature list, seed, hyperparameters and metrics; 10 champion runs share **one** identical metric vector |
| 24 | `curl …/artifacts/list?run_id=…` per run | 0 | baselines → `dm_development.json`; benchmark → `a69_benchmark.json`; catalog → `catalog_selection.json`, `development_pooled_metrics.csv`; champion → `champion_card.json`, `holdout_report.json` |
| 25 | `uv run python s13_partitions.py` | 0 | zero intersection of the final-calibration slice and holdout with **every** fold component (train/cal/eval separately) and every diagnostic window; five tail partitions pairwise disjoint and ordered; embargoes exactly 1 day each; `min(fold_5) ≥ 2025-10-01`; fit cutoff strictly before Embargo A; `152` delivery days |
| 26 | `uv run python s13b_rows.py` | 0 | recomputed from the snapshot: 63695 rows before Embargo A, **62688** eligible, **1007** ineligible — matches the report exactly; 62688+1007=63695; 0 fit rows in calibration or holdout; max fit date 2026-04-07 |
| 27 | `uv run python s14_prose.py` | 0 | augmented lower on **2 of 5** folds; champion beats naive **5/5** pinball, **3/5** MAE; pooled MAE gap `+9.291182311`; fold_3 contributes `+10.874424`; **3** folds negative |
| 28 | `uv run python s14b_null456.py` | 0 | 456 null-proxy eval rows, all in fold_4 — independently recomputed |
| 29 | `uv run python s14c_devdm.py` | 0 | after fixing my own bad day-level merge, all development DM figures reproduce at `rel = 0.00e+00`; crossings 10158/4412/0 |
| 30 | `uv run python s14d_diag.py` | 0 | timings sum 695.4; SHAP overlap 5/5 and 10/10, Spearman 0.983846→0.984; SHAP-vs-permutation 0.6923→0.692; regime strata sum to 10747/448 three ways; all 5 thin rows carry CIs |
| 31 | `uv run python s14e_verbatim.py` | 0 | §7.1 limitation and §6.2 exchangeability paragraphs present **verbatim in the report**; one-shot DM label appears exactly once in plan, report, README and matches `holdout_report.json` |
| 32 | `git cat-file -t 525fc2d…` / `git merge-base --is-ancestor 525fc2d… f3a1b7d…` | 0 / 0 | real commit, reachable from the candidate |
| 33 | 9 × mutation runs (mutated copy of `src/` in scratch, loaded via `PYTHONPATH`; worktree never written) | — | every control fires — see below |
| 34 | `curl -o /dev/null -w "%{http_code} %{redirect_url}" https://dagshub.com/hrsi56/delu-day-ahead-forecast` | 0 | `HTTP=302 → https://dagshub.com/user/login` — the report's claim about the root is exactly right |
| 35 | `git status --porcelain`; `git diff --stat HEAD`; `git rev-parse HEAD` (final) | 0 | empty; empty; `f3a1b7d7…` unchanged |
| 36 | `git worktree remove --force …/critic-cp-2-r3` | 0 | removed; main repo clean |

**Mutation results (command 33)** — each mutation was applied to a copy of `src/delu_forecast` in scratch and the committed tests run against it:

| Mutation | Result |
|---|---|
| `isotonic_last` → identity | 4 failed (test_11 ×3, test_16 ×1) |
| `cqr_threshold` reads `scores[k]` | 2 failed (test_10) |
| undersized calibration set clips instead of raising | 1 failed (test_10) |
| `assert_no_reserved_rows` → no-op | 1 failed (test_12 smuggling control) |
| champion runtime firewall → no-op | 1 failed (test_13) |
| 720h rolling window reaches into delivery day D | 11 failed, incl. both `test_13` day-leak params |
| calendar-day lag → fixed 24-row UTC shift (the exact v6.7 defect) | **10 failed** across test_02/test_03/test_14 on the full suite |
| Newey–West LRV → plain sample variance | 2 failed (test_15) |
| `fingerprint()` → constant | 1 failed (test_16) |

No control was inert.

## Evidence actually inspected

`capstone_V6_8.md` §§4.1, 5.1, 6.2, 7.1, 7.2, 8.1–8.3, 12 and the v6.7→v6.8 delta block; `docs/track-b/gauntlet-templates.md` §2. Source: `conformal.py`, `postprocess.py`, `metrics.py` (`diebold_mariano`, `newey_west_lrv`), `experiment.py` (`load_inputs`, `run_fold_arm`), `model.py` (`ChampionModel`, `gate_feasible_frame`, `fingerprint`), `features.py` (`_calendar_day_lag`, `_daily_price_statistics`, `residual_proxy_details`), `ingest.py` series specs, `scripts/cp2_benchmark_a69.py`, `scripts/cp2_report.py`, `Makefile`. Artifacts: all six parquets, `development_metrics.csv`, `development_pooled_metrics.csv`, `development_fold_thresholds.json`, `catalog_selection.json`, `dm_development.json`, `a69_benchmark.json`, `holdout_report.json`, `champion_card.json`, `regime_table.csv`, `reliability_three_stage.csv`, both `shap_ranking*.csv`, `permutation_importance.csv`, `diagnostics.json`, `timings.json`, four `fig_*.png` (verified real PNGs), `models/champion/python_model.pkl` (loaded and exercised), `data/partitions.json`, `data/snapshot.parquet`. Narrative: all 414 lines of `docs/cp2-model-report.md` and all of README §CP-2. Tests `test_10`–`test_16` read and mutation-tested. The live DagsHub MLflow API, anonymously.

I did not read `progress.md`, `orchestrator-role.md`, the syllabus, or any other Track A/C material.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Similar-day naïve, seasonal-naïve-168h, Ridge and the nine-head LightGBM catalogs run on the five pinned folds within the M3 / 16 GB / CPU-only constraint | **PASS** | `development_metrics.csv` carries all five models × 5 folds (`nunique == 5` each); champion holds exactly 9 heads `p025…p975`; `timings.json` records `arm64 / Darwin 25.5.0, CPU only`, 695.4 s total, no GPU. Fold 1's `base` heads refit bitwise-identically (cmd 17) |
| 2 | MAE, mean pinball and both DM analyses reported with statistic, p-value, effect size, comparator and `evidence_class = development_post_selection` | **PASS** | All six DM tests in `dm_development.json` carry the five fields and the label. I recomputed both similar-day-naive analyses from the parquets with my own Newey–West: every figure `rel = 0.00e+00` (cmd 29). Report renders both with the label |
| 3 | Two-arm raw-head selection complete; matched folds/rows/seeds/hyperparameters/budget; augmented ships only if strictly lower; both losses, pct difference and selection reported | **PASS** | Pooled losses reproduced to 1.4e-16 relative, pct to 7.4e-14 (cmd 12); identical `(fold,delivery_date)` multisets and identical `y_true`; seed 42 and one frozen LGBM config shared by both arms; augmented is **higher**, so `base` ships — the declared rule as applied. "No improvement" reported as a result. One non-blocking prose defect in this section — see below |
| 4 | CQR and isotonic-last implemented; `n_cal=20` fixture reproduces ranks `{20,19,17,11}` and `Q={8,7,5,−1}`; raw/post-CQR/final coverage at 50/80/95; zero crossing violations | **PASS** | Fixture recomputed from the raw rows by me (cmd 9) and matched by the implementation (cmd 10), plus negative-Q narrowing, p50 invariance, and raise-not-clip. Three-stage coverage in `reliability_three_stage.csv` and the report. Hard gate: **0** final crossings in development and holdout, with `raw_` > 0 proving discrimination (cmd 13); mutation confirms the guard tests are live |
| 5 | Final fit, freeze, one-shot holdout; every named metric; exact DM label; frozen artifact ships, no retrain; four cutoffs distinct | **PASS** | Fit stops at 2026-04-07, strictly before Embargo A; 62688/1007/63695 row accounting recomputed from the snapshot (cmd 26); thresholds estimated once on the 60-day slice and exactly reproduced (cmd 11); every holdout metric, both pct differences, 50/80/95 coverage and the DM triple reproduce at `rel = 0` (cmd 14); label verbatim in report, README and `holdout_report.json`; `retrain/retune_after_holdout: false`; four cutoffs distinct and identical in card and report |
| 6 | Champion SHAP summary/top-10 and permutation importance committed and interpreted | **PASS** | `shap_ranking.csv`, `shap_ranking_frozen_champion_in_sample.csv`, `permutation_importance.csv`, `fig_shap_summary.png` + two dependence plots. Report renders both top-10s, states the out-of-sample scoping honestly, and reports the 0.692 SHAP-vs-permutation Spearman and the 0.984 cross-read agreement — both recomputed by me |
| 7 | Regime table with `n_obs` on every row, negative-price stratum, Dunkelflaute stratum, bootstrap CIs on thin subsets read qualitatively | **PASS** | 11 rows, `n_obs` on every one; strata sum to 10747/448 three independent ways; negative-price and Dunkelflaute strata present; all 5 `qualitative (thin subset)` rows carry `mae_ci95_low/high`; day-block bootstrap rationale stated |
| 8 | §7.2 A69 benchmark as one number, with limitation; no second calibration, no deployable artifact | **PASS** | `−19.4926%` recomputed to 5.5e-16 relative; strict arm bitwise-equal to development `base` (cmd 16); the predictions parquet has `raw_*` only — no `cqr_`/`final_` columns; `calibrated:false`, `coverage_reported:false`, `deployable_artifact:false`, `registry_version:false`; the only A69 files in the tree are the benchmark JSON, its parquet and its script; limitation verbatim in the JSON, report and README |
| 9 | MLflow records for decision-bearing baseline, champion and calibration runs carry the eight fields and are publicly viewable | **PASS** | HTTP 200 anonymously with **no credential** in my environment (cmd 21–22); every `baseline::*`, `catalog::*`, `benchmark::*` and `champion::final-fit-and-holdout` run carries snapshot hash, code SHA, fold spec, feature list, seed, hyperparameters, metrics and artifact links (cmd 23–24). README and report link the `.mlflow` URI only — the root 302s to sign-in, exactly as the report states |
| 10 | One fresh Integration Critic returns `PASS` from a clean detached checkout, with a verdict-only delta to the evidence tip | **PASS** | This verdict, produced from a clean detached worktree at `f3a1b7d7…` that was verified empty before and after and then removed. The verdict-only delta is the return's obligation: this file must be the sole change between `final_candidate_sha` and `evidence_tip_sha` |

## Defect found — recorded, not bar-failing

`docs/cp2-model-report.md` §1 attributes the null-proxy rows to the wrong ENTSO-E feed:

> 456 of the evaluation rows carry a null `residual_load_proxy` … chiefly **a missing A65 hour on 2025-07-09** …

The snapshot says otherwise. On 2025-07-09 the A65 series (`load_forecast_mw`) has **zero** nulls; `vre_actual_mw` — **A75**, per `ingest.py:47` and plan §4.1 — has exactly one. Across the entire snapshot there are ten days with A65 nulls and 2025-07-09 is not among them, while it is the *only* day with an A75 null. `features.py:176` fixes the completeness rule as `non_null_rows = frame["vre_actual_mw"].notna()`, so the 42-complete-day window that produced these nulls is an A75 rule end to end.

Everything else in the sentence is exactly right: the count (456, independently recomputed), the date, and the mechanism — the gap invalidates 2025-07-11 … 2025-07-29 within fold 4's eval block, 19 days × 24 h = 456 rows. The claim it supports ("those rows stay in both arms … no row is deleted") is true and I verified it.

I record this as a documentation defect rather than a bar miss: item 3 enumerates both losses, the percentage difference and the selected catalog, and all three are present and exactly reproducible; the misattribution sits in a voluntary explanatory aside and changes no number, no matched-rows conclusion and no decision. It is worth a one-word fix before CP-3, because A65/A69/A75 separation is the spine of the strict-gate argument and this report is where that rigor is on display.

One immaterial note alongside it: the report's "29.4 MB on disk" is `python_model.pkl` divided by 1048576 — that is 29.4 MiB (30.8 MB decimal). A unit-label convention, not a wrong measurement.

Two brief-vs-plan reconciliations worth stating, since neither is a gap: the §7.1 limitation and §6.2 exchangeability paragraphs appear verbatim in the report but not in the README — the plan scopes both to the report ("verbatim in the report", "Stated in the final report verbatim"), and README/Pages/Space agreement is CP-3's item 5, not CP-2's. And `standardized_effect_size` is Cohen's d, not the HAC-standardized statistic I first assumed; the DM statistic itself correctly uses the Newey–West LRV, so the two quantities are distinct by design.
