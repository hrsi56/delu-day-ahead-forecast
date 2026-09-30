# Track B Checkpoint Return — CP-21

## Status

**PASS** — every item of the complete §17.10 checklist is evidenced, and the fresh Integration
verdict binding `final_candidate_sha` is PASS.

**Research verdict (rule `cp21-adoption`, §17.6, set 2026-09-29): v4.** All four conditions hold,
condition 3's Engineering PASS being the Integration verdict below. HGL, "v4 · three-block LightGBM
added" (the draft name; the version is assigned and dated at landing), is adopted in research
only. **Product status is unchanged:** v1 remains the released product and demo. No promotion,
freeze, final-product designation, Live or economic claim follows.

**Block-split finding (L-R − L-P, §17.5 reading): no demonstrated joint preference.**

## Identity

- Repository / checkpoint / ratified anchor and version: DE-LU day-ahead forecasting
  (`/Users/djourno/Downloads/PJM`, origin `hrsi56/delu-day-ahead-forecast`) / CP-21 /
  `capstone_v21.md` v21-r6 §17 (SHA-256 `ee402c4703d176f8181ed82966c978ad84c3c73a0cdb1d3567871f58bc867344`;
  amendment record `a9086fa1d70ea9cfd9c7fde3733f631bff7b8e372a8990e6cc7a52be3650bedd`; both on
  `main` at the ratification commit `270a0a0`).
- Issued brief: `docs/track-b/evidence/cp-21/issued-brief.md`, SHA-256
  `813fb8a476a7b6d10ecf0a5519e97ec8efc4ff36e0f13868676ad34534fc020f`, byte-identical to the canonical copy
  and to the brief as pasted to the Lead (no difference).
- **final_candidate_sha: `260dcf9fb3f5706cb896991ba7b6edf4cd9494b6`** (every bar binds here).
- **evidence_tip_sha:** the commit on `gauntlet/cp-21` that adds this file. A commit cannot contain
  its own SHA; the terminal return message states it.
- `git diff --name-only 260dcf9fb3f5706cb896991ba7b6edf4cd9494b6..<evidence_tip_sha>`:

  ```text
  docs/track-b/evidence/cp-21/checkpoint-return.md
  docs/track-b/evidence/cp-21/integration.md
  docs/track-b/evidence/cp-21/resource-final.json
  ```

  Verdict-only: nothing outside `docs/track-b/evidence/cp-21/`.

## Repository state

- Branch: `gauntlet/cp-21` (local only), working tree clean at the evidence tip.
- **Created by this checkpoint:**
  - branch `gauntlet/cp-21`, from `ffcf9f3` (`main` = `origin/main` at the start), holding the
    CP-21 candidate and evidence: 6 commits ahead of `main`, 0 behind, clean. Proposed disposition:
    LAND.
  - worktree `.local/worktrees/cp-21/lead`: the Lead's checkout of `gauntlet/cp-21`, clean, retained
    for the landing; remove at reclamation.
  - worktree `.local/worktrees/cp-21/critic`: a detached checkout at the candidate for the first
    review session, which an API session limit stopped before any verdict. Removed clean.
  - worktree `.local/worktrees/cp-21/critic-2`: a fresh detached checkout at the candidate for the
    binding review. Removed clean after the verdict.
  - Tags: none. Stash: none.
- `main` untouched (`ffcf9f3` = `origin/main`), nothing staged on `main`, nothing pushed, no remote
  ref, no public write (MLflow tracking local only; `remote_writes` 0).
- State verified at the start: `main` = `origin/main` = `ffcf9f3`, one Q&A commit above the
  ratification commit `270a0a0` (the Owner's note); `270a0a0` is a direct child of `05587ac` and adds
  exactly the five named documents; no `gauntlet/*` branch, no other worktree, no stash; clean tree.
  `land/cp-20` = `f450bc1`, `evidence/cp-20` = `a7a9b2e`. No material mismatch. Word's lock file
  `~$לות תשובות.docx` was present in the primary checkout (ignored; not touched).

## Complete checklist with direct evidence

| # | Checklist item (§17.10) | Status | Direct evidence |
|---|---|---|---|
| 1 | Repository/input state; prior work preserved; anchor and amendment verified; brief packaged byte for byte; frozen pre-run protocol before any outer scoring | Met | Hashes verified at the start; brief committed `b9d6310` (`-text`); `reports/block-challenger/protocol.json` committed `49bcdfc` before the first main fit and every score (arms, blend, blocks, 29-column features and §15.3 rule, grid G1–G4, 28-day inner split, tie rule, fixtures, seeds 42/15042, 638-origin table and key hash, cache identities, caps/E1–E4, §17.6 and §17.3 verbatim); only accuracy-blind training-only timing and determinism fits preceded it (`preflight/`) |
| 2 | CP-20 population/manifest and weather from the retained grids; HG components only with verified identity; independent HG reproduction; no retrieval; nothing after 2026-04-07 | Met | `preflight/input-verification.json` (all 638 HG cache entries against CP-20 fingerprints; 448 evaluation-day centrals bitwise = accepted HG); `preflight/weather-regeneration.json` (2,476 grids, bitwise); `hg-parity.json` (10,747 keys bitwise); refits bitwise in `daily-cycle.json` (25 origins), `controls.json` and the Critic's own; `download_bytes` 0; loader and guard filter at 2026-04-07 |
| 3 | Exactly L-P, L-R, L-N, HGL; training-only capacity selection for every LightGBM model; the three parity proofs | Met | `src/cp21/lgbm.py` (one implementation); `fits.parquet` (22,260 main fits; every final configuration is the inner-validation argmin, ties to the smaller); HGL blend parity ≤ 1.99e-13 on every key and components bit for bit (`controls.json`); one H-layer path, v3 reproduced bitwise (`hg-parity.json`); L-R/L-N differ only in target and features (`test_selection.py`); L-P/L-R identical rows (`controls.json` `pooled_block_rows_equal`) |
| 4 | Every §17.7 control with transform-surviving positive controls; inherited regression and namespace guards | Met | `controls.json`: 49 checks, all passed (delivery-day mask 0.0 against a non-uniform D−1 mutation that moves every arm; future weather 0.0 against cross-date permutation and within-day rearrangement; training-only selection both ways; pooled–block parity; DST; state/cache refusals; boundary guard; n_jobs 4 = main run); full suite 1,131 passed including `test_24_live_namespace_is_walled_off.py`, `test_05_schema_firewall.py`, CP-15/16/20 suites |
| 5 | All 10,747 keys per new arm, finite ordered quantiles, p50 separate from central; failures, exclusions and fallback accounted | Met | `predictions.parquet` 42,988 rows; `failures.csv` 0 rows; `fallback.csv` 0 of 11,592 cells per arm; denominators identical for all eleven policies |
| 6 | Score all eleven policies; verify scores, diagnostics with denominators and support labels, coverage with width, §8 per new arm | Met | `metrics.csv`, `diagnostics.csv`, `criteria.csv`; reproduced by the Critic's own reference pass to ≤ 3.4e-16 relative; saved references equal CP-20's rows exactly |
| 7 | §17.6 mechanically; contrasts with paired, per-fold and ratio intervals from stored draws; block split; verdict; mixed and negative findings; statuses distinct | Met | `uncertainty.csv`, `replicates.parquet` (168,000 draws), `replicate-scores.parquet`, `adoption.json`; the Critic's own bootstrap reproduces all 84 rows; `report.md` states the research verdict, Engineering status and product status separately, and the mixed/negative findings below |
| 8 | Fit-cost and daily-retrain diagnostic in `reports/block-challenger/` | Met | `fit-cost.md`, `fit-cost.{csv,json}`, `fit-cost-by-origin.csv`, `fits.parquet`, `daily-cycle.json` (25 cold origins, median 24.7 s, maximum 69.4 s; diagnostic only, D3) |
| 9 | Every §17.8 cap from the first job, including controls, failures and review; calendar | Met | Ledger initialised before the first job; `resources.json` (candidate) and `resource-final.json` (final, with both review sessions); no cap exceeded; reference and bootstrap passes 3/3 (reached, not exceeded); every job on Tue 29 / Wed 30 Sep, none in the Friday/Shabbat window |
| 10 | Durable evidence and reproduction commands; byte-exact hash-bound files; defects, repairs and invalidated outputs | Met | `reproduce.md`; `artifact-manifest.json` (66 files, `* -text`); `defects-and-repairs.md` (D1–D7; no committed output invalidated) |
| 11 | Publication packet and draft MLflow export; public surfaces and published export set unchanged; CI green; no public write | Met | `docs/track-b/evidence/cp-21/publication-packet.md`; `docs/track-b/research-content/cp21-claims.md`; `mlflow-export-draft/cp21.json`; `mlflow-local.json`; `published-export-diff.json` (23 runs, only identity, 0 changes); `--check` current; no public-surface diff; locally 1,131 passed / 8 environment skips, `verify_release.py` PASS, publication guard clean. GitHub CI itself was not run: no push is authorized |
| 12 | One fresh, independent Integration-Critic PASS on a clean detached checkout of the exact final candidate | Met | `docs/track-b/evidence/cp-21/integration.md`: **PASS** at `260dcf9fb3f5706cb896991ba7b6edf4cd9494b6`, with its own reference and bootstrap passes, independent LightGBM, HG, H-layer and state reproductions and packet/export re-derivation |
| 13 | Canonical return with the publication packet; both SHAs; verdict-only delta; reachable evidence; resources and elapsed hours; branch and worktree accounting | Met | This return, the attached packet, `resource-final.json`; every cited SHA reachable on `gauntlet/cp-21` |

## Research results (development_post_selection)

| Quantity | Value | Row |
|---|---|---|
| S_MAE / S_WIS | HGL 0.5357 / 0.5056; v3 (HG) 0.5658 / 0.5322; L-P 0.5785 / 0.5477; L-R 0.5835 / 0.5540; L-N 0.5769 / 0.5402; B3 0.7841 / 0.7399 | `metrics.csv` equal-fold rows |
| HGL − HG, ΔS_MAE | −0.0301 [−0.0368, −0.0228]; as a share of v3's score −5.3% [−6.4%, −4.0%] | `uncertainty.csv` L72 |
| HGL − HG, ΔS_WIS | −0.0266 [−0.0327, −0.0204]; −5.0% [−6.0%, −3.8%] | `uncertainty.csv` L73 |
| Per fold (condition 4) | every point estimate favours HGL; fold 3 (stress) MAE −1.01 [−2.56, +0.59] and WIS −0.78 [−1.70, +0.09] span zero; no fold decisively worse | `uncertainty.csv` |
| §8 screen | HGL met all six; HG met; L-N met; L-P not met (criterion 4); L-R not met (criteria 4, 5) | `criteria.csv` |
| Block split, L-R − L-P | ΔS_MAE +0.0050 [−0.0084, +0.0142], ΔS_WIS +0.0063 [−0.0050, +0.0135]: no demonstrated joint preference; both point estimates slightly worse for the blocks | `uncertainty.csv` L74–L75 |
| Mixed and negative | L-R − HG: S_WIS interval wholly above zero (worse), S_MAE spans zero; HGL's MAE on the 17-day peak is 50.1 against v3's 47.5 EUR/MWh (descriptive); L-P − B3 (−26% both scores) bundles weather with capacity selection | `uncertainty.csv`; `diagnostics.csv` peak rows |
| Stress period | HGL fold-3 MAE 47.0 EUR/MWh (v3 48.0); ordinary folds 4.9–15.0 | `metrics.csv` per-fold rows |

## Integration verdict

- Path: `docs/track-b/evidence/cp-21/integration.md`. Result: **PASS**.
- Candidate SHA it binds: `260dcf9fb3f5706cb896991ba7b6edf4cd9494b6`.
- Reviewer: one fresh, independent Integration Critic (a separate session), on a clean detached checkout
  created for it. An earlier Critic session for the same candidate was stopped by an API session limit
  before writing any verdict. The binding reviewer did not open its scratch; both sessions' compute is
  charged. Isolation is cooperative (a clean detached worktree, not a read-only mount).
- Non-blocking observations (the verdict's own list):
  - A daily-cycle docstring overstates how little data the cycle loads. The forecast is unaffected:
    the mask control is exact, and the cycle equals the main run bit for bit.
  - The passes are now at 3/3.
  - The 8 skips are environment-gated.
  - The review worktree was left for the Lead, and has since been removed.

## Reproduction

`reports/block-challenger/reproduce.md` gives every command, each run under the monitor against the
shared ledger. The pre-run stage had no forecast failure (D1 and D2 in `defects-and-repairs.md`
were reporting defects), and the stages ran in this order:

1. Pre-run: `verify-inputs`, `verify-weather`, `benchmark`, `determinism`, `e1`, `protocol`.
2. Fits: warm-up 564 tasks with 0 failures, then evaluation 1,344 tasks with 0 failures.
3. `admission`, then `comparison`: 42,988 rows.
4. `hg-parity`: bitwise.
5. `score`: v4.
6. `controls`: 49 of 49.
7. `fit-cost`.
8. `daily-cycle`: 25 origins, all bitwise.
9. `packet`, then `draft-export`, then `mlflow-local`: read-back equal.
10. `claims`: 0 lint findings, then `report`, then `finalise`.
11. The checks:
    - `pytest tests/cp21`: 44 passed.
    - Full suite: 1,131 passed, 8 skipped.
    - `verify_release.py`: PASS.
    - `publication_guard.py tree`: clean.
    - `mlflow_export.py --check`, `--draft cp21 --check` and the generators' `--check`: all identical.

## Files changed

`git diff --stat ffcf9f3..<evidence_tip_sha>`: 70 files, all inside the §17.11 write paths. Every
file is new except `scripts/mlflow_export.py`, the only modified file.

| Path | Rationale |
|---|---|
| `docs/track-b/evidence/cp-21/issued-brief.md`, `.gitattributes` | The issued brief, byte for byte (`-text`) |
| `docs/track-b/evidence/cp-21/publication-packet.md` | §17.9 publication packet (template sections 1–8) |
| `docs/track-b/evidence/cp-21/integration.md` | The binding Integration verdict (verdict-only delta) |
| `docs/track-b/evidence/cp-21/resource-final.json` | Final §17.8 totals, including review (verdict-only delta) |
| `docs/track-b/evidence/cp-21/checkpoint-return.md` | This return (verdict-only delta) |
| `docs/track-b/research-content/cp21-claims.md` | The claim map (C100–C127, W22–W27) |
| `reports/block-challenger/protocol.json`, `preflight/*.json` (5) | Frozen pre-run protocol and pre-run evidence (E1–E4) |
| `reports/block-challenger/lineage.json`, `predictions.parquet` | Admission freeze, comparison vectors (four new arms) and replay lineage |
| `reports/block-challenger/metrics.csv`, `diagnostics.csv`, `uncertainty.csv`, `criteria.csv`, `fallback.csv`, `failures.csv`, `adoption.json` | Scores, diagnostics, paired/per-fold/ratio intervals, §8 screen, fallback, failures, §17.6 verdict |
| `reports/block-challenger/replicates.parquet`, `replicate-scores.parquet` | Every stored bootstrap draw (§17.5; PUBLISH_RULES 1.1 §3.2) |
| `reports/block-challenger/controls.json`, `hg-parity.json` | §17.7 controls; v3 reproduced through the CP-21 interval-layer path |
| `reports/block-challenger/fit-cost.md`, `fit-cost.{csv,json}`, `fit-cost-by-origin.csv`, `fits.parquet`, `daily-cycle.json` | §17.5 fit-cost and daily-retrain diagnostic |
| `reports/block-challenger/draft-registry.json`, `mlflow-export-draft/cp21.json`, `mlflow-local.json`, `published-export-diff.json` | Draft registry entries, draft export, local tracking record, published-set diff |
| `reports/block-challenger/report.md`, `reproduce.md`, `defects-and-repairs.md`, `resources.json`, `artifact-manifest.json`, `.gitattributes` | Report, reproduction, disclosure, candidate-time resources, hash binding, byte-exact storage |
| `src/cp21/*.py` (19 modules) | Identities, LightGBM blocks and selection, replay, scoring, controls, diagnostics, packet, tracking, review |
| `tests/cp21/*.py` (7 files) | Synthetic controls, the scoring path, saved-evidence re-derivation, draft-export contract |
| `scripts/cp21_blocks.py` | The driver: ledger, monitor, calendar and cap enforcement |
| `scripts/mlflow_export.py` (modified) | The `--draft cp21` path, the ratio-metric vocabulary and a `weather=` option on `datasets()`; the published export set is unchanged (`--check`, record-level diff) |

## Resource totals (§17.8, first job through the review)

| Item | Used | Cap |
|---|---|---|
| Policies | 4 new (L-P, L-R, L-N, HGL) + 7 saved = 11 scored | 4 new |
| LightGBM fits | 24,157 total, of which 22,260 main; 152 benchmark/determinism, 630 controls, 750 daily cycle, 365 review | 24,000 main; 35,000 total |
| HG components | 72 component-days (0 in the main run: verified CP-20 cache; 12 controls, 50 daily cycle, 10 review); 8,630 Lasso attempts | 1,600; 192,000 |
| Replay | 4,190 policy-days (admission 752, evaluation 1,800, HG parity 638, controls 84, daily cycle 25, review 891) | 10,500 |
| Passes | 3 reference passes and 3 bootstrap passes (scoring 1, interrupted review 1, binding review 1): at the cap, not over it | 3; 3 |
| Compute | 6.13 aggregate machine-hours (wall × declared workers; 3.94 CPU-hours observed); at most 4 concurrent workers; BLAS 1; 0 GPU, 0 cloud | 60 |
| Memory and disk | Peak aggregate RSS 3.68 GiB; peak added disk 0.49 GiB | 10 GiB; 20 GiB |
| Data and network | 0 bytes downloaded; 0 remote writes; $0 | 0; 0 |

Synthetic fixture fits (tests only, no research data), tracked and not capped: 435.

## Elapsed

- **Active:** about **3.5 hours**, against the 32-hour timebox and the 40-hour hard ceiling. That is
  2026-09-29 18:51 to 2026-09-30 about 04:00 IDT, less two recorded usage-limit pauses of 2.8 h each,
  with no job running during either.
- **Compute effort:** 6.1 machine-hours, including the review.

## Open risk or exact Owner action

- **LAND or DISCARD `gauntlet/cp-21`** (proposed: LAND), with the tags `land/cp-21` and
  `evidence/cp-21`. The PRES-3 publication block follows as its own brief.
- At landing, §17.6 applies. The standing decision "same information, same opponent" names HG, and the
  Owner updates it so that later extensions face v4 on v4's information. 4.7T's frozen manifest must
  carry both v3 and v4.
- The reference and bootstrap pass caps are exhausted (3/3). Any rescoring of CP-21 would need a new
  Owner-approved allowance.
- GitHub CI was not run, because no push is authorized. Its local equivalent is green.

## Landing report

- **Proposed disposition:** LAND. Engineering PASS with a binding Integration PASS. The research
  verdict (v4) is published in either outcome under decision D5, and the page derives every number
  from committed rows on `main`.
- **Evidence tip to preserve:** the evidence tip above, stated in the terminal message. Tag it
  `evidence/cp-21`: the squash commit does not contain the candidate SHAs the verdict cites.
- **Live documents citing this branch:**
  - `docs/track-b/evidence/cp-21/issued-brief.md` and this return name `gauntlet/cp-21`. They are
    hash-bound historical records, not repointed.
  - No other live document cites the branch.
- **Retained local material** (ignored; recovery material, not the sole copy of any evidence):
  - `.local/artifacts/cp-21/` (62 MB): the fit cache (37 MB), HGL state snapshots (21 MB), the ledger,
    logs, markers, preflight copies, and both review sessions' scratch;
  - `.local/mlruns/cp21/` (1.9 MB): the local MLflow store;
  - `.local/tmp/cp-21/`: empty.
- **Proposed commit message:**

  ```text
  CP-21: three-block LightGBM on v3 — HGL adopted in research as v4

  Capstone v21-r6 §17 (programme 4.5). HGL adds a three-block LightGBM member
  (1/3 weight, the mean of raw and normalized block models) to v3's two LEAR
  components, with v3's hour-aware interval layer re-estimated on HGL's own
  errors. On CP-20's 10,747 development hours it met all four conditions of the
  pre-registered rule cp21-adoption: S_MAE -5.3% [-6.4%, -4.0%] and S_WIS -5.0%
  [-6.0%, -3.8%] against v3, all six section-8 diagnostics, a complete valid
  evaluation, and no fold decisively worse. The block split itself (three-block
  versus pooled LightGBM) showed no demonstrated joint preference.
  Development evidence after selection; v1 remains the released product.

  Evaluation, controls, diagnostics, packet and draft export under
  reports/block-challenger/; Integration PASS at 260dcf9 in
  docs/track-b/evidence/cp-21/integration.md.
  ```

## Interview-answer triggers (one line each; the Lead files nothing)

1. LightGBM's model hash differed between 1 and 4 threads. We traced it to a recorded
   `[num_threads]` parameter, not the trees, proved identical trees on 24 real cases, and ran four
   single-thread processes.
2. The gain came from blending a nonlinear member into v3, not from splitting the day into blocks:
   block against pooled LightGBM showed no demonstrated joint preference.
3. Every arm, v3 included, runs through the one frozen interval-layer class. Each passes its single
   forecast twice, since `c/2 + c/2 == c` exactly, and v3 reproduced bit for bit.
4. An API limit stopped the first review before its verdict. The capped scoring and bootstrap passes
   (3 each) were exactly enough, because the tests were designed never to spend them.

## Post-return reads

None. No read of `progress.md`, `orchestrator-role.md`, the syllabus or Track A/C material was made.
