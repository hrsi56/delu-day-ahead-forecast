# Track B Checkpoint Return — CP-23

## Status

**PASS**. CP-23 is complete and valid at the final candidate, and one fresh Integration-Critic PASS on a
clean detached checkout binds it. Its research result is **v5 not adopted**: CP-23 becomes the branch
"DDNN member on v4".

**The route.** DDNN entered the comparison through every gate:

- **4.6L:** research use and retention permitted. Hosted service and product are unresolved and carried to
  4.7 and 4.10.
- **§21.3:** the NumPy-only audit, finite-difference gradients and the PyTorch reference (26 of 26 checks
  at frozen tolerances) all passed.
- **4.6R:** PASS on training data only.
- **Then** the frozen protocol, and 4.6C.

**Research verdict:** `cp23-adoption`, set 2026-10-04 and applied mechanically.

- **v5 is not adopted. First unmet condition: 1**, a joint improvement over v4. v5 − v4 shows no
  demonstrated joint preference:
  - ΔS_MAE +0.0064 [−0.0016, +0.0149], +1.2% [−0.3%, +2.7%] of v4's score;
  - ΔS_WIS +0.0071 [−0.0009, +0.0138], +1.4% [−0.2%, +2.7%].

  Condition 4 is also unmet: fold 3, the stress period, is decisively worse in MAE (+1.92 EUR/MWh
  [0.30, 4.39]). Conditions 2 (all six §8 diagnostics) and 3 (every key issued, Engineering PASS) are
  met.
- **The other §21.5 readings:**
  - v5 − v3: observed joint improvement (−4.2% / −3.7%).
  - DDNN alone against v4 and against v3: observed joint worsening.
  - DDNN as v3's third member, (v3+D) − v3: observed joint improvement (−2.5% / −2.1%). Beside it, v4 − v3
    gives −5.3% / −5.0%.
  - v5 − (v3+D): observed joint improvement, so LightGBM still adds once DDNN is present.

**Statuses, kept distinct.**

- **Engineering:** PASS, the binding Integration verdict below.
- **Research:** a development_post_selection result on the same five folds CP-15, CP-20, CP-21 and CP-22
  used.
- **Product:** unchanged. v1 is the released product and the demo; there is no designation, freeze, Live or
  economic claim.

## Identity

- **Repository, checkpoint and anchor:**
  - DE-LU day-ahead forecasting (`/Users/djourno/Downloads/PJM`, origin `hrsi56/delu-day-ahead-forecast`),
    CP-23.
  - `capstone_v21.md` v21-r10 §21, SHA-256 `6873c2501067c63692ec7cb79dfd4073164a8a014edbd6ebc23169e7e8ff6709`,
    verified at the start. The amendment record is
    `453a66a107e6b597cecc80c02e04995b4de4a0935960638df220c5722afa5199`.
  - PUBLISH_RULES 1.3 at `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4`, by the Owner's
    ruling, because the brief omitted the hash.
- **Issued brief:** `docs/track-b/evidence/cp-23/issued-brief.md`, SHA-256
  `33f6b41202586b2fc4f1d87624c5978e1fd5bde1185ac05271429bf719502d0c`. It is byte-identical to the canonical
  copy, and packaged as the first commit on the branch (`cb9ba29`).
- **final_candidate_sha: `f9a737eb2bb8ccdb93c0de5cf1449630ee246e90`** (every bar binds here).
- **evidence_tip_sha:** the commit on `gauntlet/cp-23` that adds this file, directly on the candidate. A
  commit cannot contain its own SHA; `scripts/gauntlet.py return` prints it, and the Owner's
  `git rev-parse gauntlet/cp-23` resolves it.
- `git diff --name-only f9a737eb2bb8ccdb93c0de5cf1449630ee246e90..<evidence_tip_sha>`:
  ```
  docs/track-b/evidence/cp-23/checkpoint-return.md
  docs/track-b/evidence/cp-23/ci-equivalent.md
  docs/track-b/evidence/cp-23/integration.md
  docs/track-b/evidence/cp-23/resource-final.json
  docs/track-b/evidence/cp-23/review/critic_score.py
  docs/track-b/evidence/cp-23/review/ddnn.json
  docs/track-b/evidence/cp-23/review/independent-score.json
  docs/track-b/evidence/cp-23/review/replay.json
  docs/track-b/evidence/cp-23/review/score.json
  docs/track-b/evidence/cp-23/review/torch-max-errors.json
  ```
  Every path is under `docs/track-b/evidence/cp-23/`, so the delta is verdict-only.

## Repository state

- **Branch:** `gauntlet/cp-23`, created by this checkpoint from `main` = `a4acd79` to hold the candidate
  and evidence commits. At return its tip is the evidence tip and the tree is clean. It is 14 commits
  ahead of `main` and 0 behind, and is proposed for LAND (below).
- **Worktrees this checkpoint created, all removed:**
  - `.local/worktrees/cp-23/probe-lock`, at `cb9ba29`: the `uv.lock` probe, removed the same hour.
  - `.local/worktrees/cp-23/ci`, at the final candidate: the CI-equivalent run, removed after it.
  - `.local/worktrees/cp-23/critic-1`: removed by `critic-close`.

  `git worktree list` shows only the primary checkout.
- **Tags created:** none. **Stashes:** none, at the start or at return (`git stash list` is empty).
- **`main` is untouched:** `main` = `origin/main` = `a4acd792954c577e60235c427380c82031c4372a`,
  unchanged since the start. Nothing is staged on `main` and nothing was pushed. No remote write was made
  and there was no publication.
- **No other branch appeared** during the checkpoint. The local branches are `main` and `gauntlet/cp-23`.

## Complete checklist with direct evidence

`capstone_v21.md` v21-r10 §21.10, all sixteen items.

| # | Checklist item | Status | Direct evidence (path, command, or metric) |
|---|---|---|---|
| 1 | Verify the starting state and preserve prior evidence; the anchor SHA-256; baseline with `gauntlet.py start cp-23`; package the issued brief byte for byte | Met | Anchor `6873c250…f6709` equals the brief's. `gauntlet.py start cp-23` recorded `.local/artifacts/cp-23/start.json` at 2026-10-04T14:22:50Z (HEAD = `main` = `origin/main` `a4acd79`, one worktree, no stash, clean). The first commit, `cb9ba29`, packages the brief byte for byte (`cmp`). No earlier evidence was modified: every changed path is a CP-23 write path |
| 2 | 4.6L complete, every use dispositioned; stop at its cap or if research is not permitted | Met | `reports/distribution-challenger/licence-admission.md`: provenance (original MIT code, method sources, no third-party code or weights); seven test-only packages with source, version and licence, checked 2026-10-04; the seven uses dispositioned (research and retention permitted; publishing, local operation and demonstration permitted on licence only and not authorized; hosted service and product unresolved). Under one active hour of the 4-hour cap |
| 3 | §21.3: the NumPy-only import audit; finite-difference gradient checks; the PyTorch reference passing at frozen tolerances and installed so it cannot be skipped silently | Met | `src/cp23/audit.py` with `tests/cp23/test_numpy_only.py`, whose framework fixtures fail it. `tests/cp23/test_ddnn_gradients.py` checks the JSU partials and every layer in all four configurations, each with a positive control. `reports/distribution-challenger/reference-checks.json`: 26 passed, 0 skipped, torch 2.14.1, tolerances committed in `cd56434` before the first run, largest error 3.3e-4 of its bound. The check file is collected only when named and imports torch at module level, so a missing torch fails. `require_passing_record()` gates every DDNN fit. The Critic reran it: 26 of 26 |
| 4 | 4.6R on training data only, with measured values, the projection against §21.8, and PASS or NOT_ADMITTED | Met | `resource-admission.md` and `.json`: **PASS**. Two training-only warm-up origins, every configuration × 4 seeds, accuracy-blind. The projection: 2,624 main fits of 4,000; 4,560 total of 6,000; 15.2 of 60 machine-hours; 3.9 of 10 GiB RSS |
| 5 | Commit the frozen pre-run protocol before any evaluation fit | Met | `reports/distribution-challenger/protocol.json` was committed at `a008c47` (15:10:03Z), before the first main-run fit job, `select` (15:10:12Z). `check_protocol()` is enforced by every fit, replay and scoring job. It binds the representation, architecture, C1–C4, the selection rule, early stopping, seeds 42–45, quantile averaging, the reference tolerances, the arms, budget accounting, `cp23-adoption` verbatim and the §21.5 diagnostics |
| 6 | Verify the inputs: population, manifest and frozen weather; saved-vector identities; an independent HG and v4 slice; no retrieval and nothing after 2026-04-07 | Met | `preflight/input-verification.json`: 79 identities; all 638 HG cache entries and 1,908 CP-21 member entries verified; v4's composite equals CP-21's lineage hash at all 636 origins; evaluation vectors bitwise equal. `preflight/weather-regeneration.json`: regenerated from CP-20's grids bitwise, no retrieval. `reproduction.json`: HG, v4, L-N and L-R refitted at two origins bitwise. `parity.json`: v3 and v4 replayed bitwise on all 10,747 keys. The boundary guard is in `controls.json` |
| 7 | Exactly DDNN, v5 and the arms, with training-only selection and early stopping; composite parity | Met | `src/cp23/ddnn.py`, `features.py`, `member.py`, `execution.py`. `selection.json` holds one choice per fold before its first origin (C2, C4, C2, C3, C4). Early stopping uses `[D−28, D)`. Composite parity holds within 1.4e-13 EUR/MWh on every key (`controls.json`), and v5 and v3+D run on HG's H layer |
| 8 | Every §21.7 and inherited control, each negative paired with a positive | Met | `controls.json`: 61 checks, all passed. Masking: 0.0. Non-uniform D−1 mutation: moves. Future weather: 0.0. Weather permutation and rearrangement: move. Early stopping responds to inner-validation outcomes. The configuration choice is identical under evaluation-outcome mutation, and its losses change under holdout mutation. Determinism: bitwise in a fresh process. Restart replay, release, consume-once and cache refusals all hold; 23/24/25-hour days keep their identity; the extra-column refusal and the boundary guard hold |
| 9 | All 10,747 keys for every new policy, with finite, ordered quantiles and the emitted p50 separate from the central forecast | Met | `predictions.parquet`: v5, v3+D and D each have 10,747 keys with finite, ordered quantiles, and 0 rows needed rearranging. For v5 and v3+D the p50 is distinct from the central forecast; for D it is the ensemble median by definition (`tests/cp23/test_saved_evidence.py`, `controls.json`) |
| 10 | Score every policy, and independently verify the scores, the diagnostics, coverage with width, and all six §8 diagnostics per new policy | Met | `metrics.csv`, `uncertainty.csv`, `criteria.csv`, `diagnostics.csv` and `replicates.parquet`, from one reference pass and one bootstrap pass with the shared CP-20 index set. The re-derivation tests pass. The Critic recomputed everything (≤ 6e-14) and also wrote an independent scorer from the plan text (≤ 4.3e-14) (`review/score.json`, `review/independent-score.json`) |
| 11 | Apply `cp23-adoption` mechanically; the decision with its first unmet condition, every §21.5 contrast with its reading; statuses kept distinct | Met | `decisions.json` and `adoption.json`: not adopted, first unmet condition 1, unmet {1, 4}. All seven contrasts are read under §17.5 (`report.md`, `cp23-claims.md` C308–C316). The engineering, research and product statuses are kept distinct (`decisions.json` `statuses`) |
| 12 | Deliver §21.5's diagnostics to `reports/distribution-challenger/` | Met | `diagnostics.json` and `diagnostics/`: calibration by level and the PIT histogram; extrapolation beside CP-22's tree record; the peak and fold 4; seed stability and epochs. The configuration per fold is in `selection.json`, the fit cost in `fit-cost.json` and `fits.parquet`, and the cold daily cycle at 25 origins (all bitwise) in `daily-cycle.json` |
| 13 | Enforce and report every §21.8 cap, and respect the calendar | Met | Every cap is reserved before use in `.local/artifacts/cp-23/ledger/budget.json`. Final totals (`resource-final.json`): DDNN fits 2,856 of 6,000 (main 2,624 of 4,000); policy-days 3,293 of 8,000; reference passes 3 of 3 and bootstrap passes 3 of 3 (two by the review); 2.25 machine-hours monitored, and an upper bound of 3.25 including unmonitored test runs, of 60; peak RSS 3.19 GiB of 10; added disk 0.30 GiB of 10; 4 workers; BLAS 1; CPU only; 0 data bytes; 0 remote writes; $0. The one permitted download is recorded (137,444,189-byte upper bound). Every job ran on Sunday, outside the Friday/Shabbat window |
| 14 | Durable evidence, executable reproduction commands and byte-exact storage; §21.9's packet and draft export; public surfaces and the published export unchanged; CI green; no public write | Met | `reproduce.md`; `artifact-manifest.json` with 86 SHA-256s, all matching; `* -text` attributes. `docs/track-b/evidence/cp-23/publication-packet.md` and `docs/track-b/research-content/cp23-claims.md` (0 lint findings, `--check` identical). `mlflow-export-draft/cp23.json` and `mlflow-local.json` (read back equal). `published-export-diff.json`: 28 runs, no change; `--check` current. CI-equivalent at the candidate: 1,363 passed, 8 skipped; `verify_release.py` PASS; the WASM gate passes (`ci-equivalent.md`). No public surface was touched |
| 15 | One fresh, independent Integration-Critic PASS on a clean detached checkout, launched with `critic-open`, `critic-brief` and `critic-close`; independent recomputation, reference rerun, DDNN reproduction and packet re-derivation | Met | `docs/track-b/evidence/cp-23/integration.md`: **PASS** at `f9a737e…`, by one `general-purpose` subagent through the three commands (record `critic-1`; verdict SHA-256 `59ac4ea7…c241f1f3`). Its outputs are under `review/`: scores, an independent scorer, the reference rerun, DDNN fits reproduced bit for bit at three origins, and the v5 replay |
| 16 | Return the canonical packet (templates §3), checked with `gauntlet.py return`, with both terminal SHAs and the verdict-only delta, resource totals, and branch, worktree and stash accounting | Met | This file, checked with `python3 scripts/gauntlet.py return cp-23 f9a737eb2bb8ccdb93c0de5cf1449630ee246e90 gauntlet/cp-23`. Both SHAs and the delta are under Identity, the resources under item 13, the accounting under Repository state |

## Integration verdict

- Path: `docs/track-b/evidence/cp-23/integration.md`. Result: **PASS**.
- Candidate SHA it binds: `f9a737eb2bb8ccdb93c0de5cf1449630ee246e90`.

## Reproduction

`reports/distribution-challenger/reproduce.md` gives the complete ordered route under the monitor and the
verification commands. Observed at the candidate:

- `python -m pytest -q tests/cp23`: 41 passed.
- `python -m cp23.packet --check`, `python -m cp23.claims --check`,
  `python scripts/mlflow_export.py --draft cp23 --check` and `python scripts/mlflow_export.py --check`:
  identical, identical, current and current.
- The full suite: 1,363 passed, 8 skipped.
- The Critic's independent runs are in `docs/track-b/evidence/cp-23/review/`.

## Files changed

`git diff --stat a4acd79..f9a737e`: 87 files, all under §21.11's write paths.

- **`src/cp23/`:** DDNN (`ddnn.py`) and its inputs, ledger, monitor jobs, protocol, replay, scoring,
  controls, diagnostics, report, packet and claims, tracking, finalise and review.
- **`tests/cp23/`:** the audit, the gradient checks, the reference record, composites and the rule, paths,
  saved evidence, the draft export, the explicitly invoked PyTorch checks, and the test-only lock in
  `torch-reference/`.
- **`scripts/cp23_ddnn.py`:** the monitor and driver.
- **`scripts/mlflow_export.py`:** the CP-23 draft-export section only. The published path is unchanged.
- **`reports/distribution-challenger/`:** every record, table and diagnostic.
- **`docs/track-b/evidence/cp-23/`:** the brief, the packet and the attributes.
- **`docs/track-b/research-content/cp23-claims.md`:** the claim map.
- **Not changed:** the root `pyproject.toml` and `uv.lock`, by the Owner's ruling on §21.3.

## Elapsed

About **4.5 active hours** of the 30-hour timebox (hard ceiling 40), from 16:30 to about 21:00 IDT on
2026-10-04. A usage-limit wait of about an hour is included as active, conservatively.

## Open risk or exact owner action

- **LAND or DISCARD `gauntlet/cp-23`** (Owner). The proposal is LAND, below.
- **Whether the branch "DDNN member on v4" is published** (Owner, §21.9). Nothing is published until then.
- **Environment note.** The PyTorch reference is installed in `.venv` from the separate test-only lock. A
  plain `uv sync --locked` removes it; reinstall it with `reproduce.md`'s two commands. The reference step
  would fail loudly, never skip.
- **The scoring-pass allowance is spent** (3 of 3 each). Any re-scoring of a changed candidate needs a new
  allowance.

## Landing report

- **Proposed disposition: LAND.** The result is a complete, valid not-adopted research result with durable
  DDNN code, evidence and a publication-ready draft. It changes no public surface, and the squash adds only
  CP-23 paths.
- **Evidence tip to preserve:** the tip of `gauntlet/cp-23`, the commit that adds this file. Tag it
  `evidence/cp-23` at LAND.
- **Live documents citing this branch** (to repoint on reclamation): none. `gauntlet.py citations cp-23`
  lists only historical text (the issued brief and the 4.6L record) and the locked anchor.
- **Proposed commit message** (for `git commit -F`):

  ```
  CP-23: the DDNN route — v5 not adopted; the branch "DDNN member on v4"

  A NumPy-only distributional neural network (Johnson SU head) passed 4.6L, the PyTorch reference
  checks and 4.6R, then was tested as v4's fixed one-third member under cp23-adoption. v5 is not
  adopted: the first unmet condition is 1 (v5 - v4 shows no demonstrated joint preference); fold 3 is
  also decisively worse in MAE. Integration PASS at f9a737e; evidence tag evidence/cp-23.
  ```

## Post-return reads

None. Neither `progress.md`, the syllabus, Track A/C material nor `orchestrator-role.md` was read.

## Interview-answer triggers (for the Orchestrator to file)

- Why the PyTorch pin moved out of the root `uv.lock`: CP-10's and CP-15's evidence binds its hash.
- DDNN as v3's third member helps (−2.5%) but less than LightGBM (−5.3%), and added to v4 it is
  directionally worse.
- How the review checked independently when the provided review command reused the Lead's scoring code:
  the Critic wrote a second scorer from the plan text.
