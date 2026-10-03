# Track B Checkpoint Return — CP-22

## Status

**PASS** — CP-22 is complete and valid at the final candidate, bound by one fresh Integration-Critic PASS on a clean detached checkout; its research result is **no replacement**.

**Research verdicts (the three §20.6 rules, set 2026-10-01, applied mechanically from the committed tables):**

- **`cp22-replacement`: no replacement.** R (PN averaged over capacities) and M (the pooled pair, the
  split removed) each meet conditions 1–3: non-inferior to v4 on both scores, all six §8 diagnostics,
  all 10,747 keys issued. Each fails **condition 4**, its first unmet condition: fold 4
  (2025-05-01..07-29) is decisively worse than v4 in both MAE and WIS; no other fold is. **CP-22 stops here
  for the Owner's decision; three-block v4 stays current** (§20.6).
- **`cp22-dynamic-layer`: not applicable** — no winner W; the layer arms on W were not run.
- **`cp22-fast-component`: not applicable** — no winner W.

**Statuses, kept distinct.** Engineering: PASS (the binding Integration verdict below). Research: a
development_post_selection result on the same five folds CP-15, CP-20 and CP-21 used. Product: unchanged — v1
remains the released product and the demo; no designation, freeze, Live or economic claim.

## Identity

- Repository / checkpoint / ratified anchor and version: DE-LU day-ahead forecasting
  (`/Users/djourno/Downloads/PJM`, origin `hrsi56/delu-day-ahead-forecast`) / CP-22 / `capstone_v21.md`
  v21-r9 §20 (SHA-256 `5fc9c6862aa9f623af29db295e79456ecd94c60e213f8f286cdca97153e09175`); amendment record
  `912eb98ffceb1b7b31e0e14da6cffc8725c3af7b227cbbcef4cea62841f5d52a`; PUBLISH_RULES 1.3
  `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4` — all three on `main` at `940eb98`,
  verified at the start.
- Issued brief: `docs/track-b/evidence/cp-22/issued-brief.md`, SHA-256
  `563f64f3602848808ff11a7d74da8218b16d51846f34e90ad754c36ec2461fb3`, byte-identical to the canonical copy; the
  pasted brief matched it in content (only markdown rendering differed).
- **final_candidate_sha: `29d8d383a8870fee10b04158c5e3e5fd89514fdc`** (every bar binds here).
- **evidence_tip_sha:** the commit on `gauntlet/cp-22` that adds this file, directly on the candidate; a commit
  cannot contain its own SHA, so the terminal message states it.
- `git diff --name-only 29d8d383a8870fee10b04158c5e3e5fd89514fdc..<evidence_tip_sha>`:

  ```text
  docs/track-b/evidence/cp-22/checkpoint-return.md
  docs/track-b/evidence/cp-22/integration.md
  docs/track-b/evidence/cp-22/resource-final.json
  docs/track-b/evidence/cp-22/review.json
  ```

## Repository state

- Branch: `gauntlet/cp-22` (local only). Working tree: clean at the evidence tip.
- **Created by this checkpoint:**
  - branch `gauntlet/cp-22`, from `940eb98` (`main` = `origin/main` at the start), holding the CP-22 candidate
    and evidence: 8 commits ahead of `main`, 4 behind (see below). Proposed disposition below.
  - worktree `.local/worktrees/cp-22/critic`: the clean detached checkout at the candidate for the Integration
    review; removed after the verdict was written.
  - worktree `.local/worktrees/cp-22/lead-verify`: a throwaway clean detached checkout at the candidate, used once
    by the Lead to run the full suite as CI does (below); removed at once.
  - Tags: none.
- **Not created by this checkpoint, reported:**
  - **`main` moved during the checkpoint, by ref only.** `main` and `origin/main` are now `32bdf9b`, four commits
    after `940eb98` (2026-10-01 14:38 UTC to 2026-10-03 17:34 UTC, author "Claude", another session), which add only
    `docs/automation-plan.md`. `origin/main` was fetched at 2026-10-03 20:10 and 20:40 IDT and `main` fast-forwarded
    at 20:46:49 IDT (reflog `pull: fast-forward`) by a client outside this session; `HEAD`'s reflog shows no checkout
    then, so the working tree stayed on `gauntlet/cp-22` throughout. The anchor, the amendment record, PUBLISH_RULES,
    the templates and `AGENTS.md` hash identically at `940eb98` and `32bdf9b`; `gauntlet/cp-22` shares no path with
    the four commits, so a squash landing touches disjoint files.
  - Branch `claude/automation-plan-corrections-t45wdc` (`1615866`), created 2026-10-01 22:08:43 IDT from
    `origin/claude/automation-plan-corrections-t45wdc` by GitHub Desktop (HEAD's reflog shows it checking that
    branch out, then `main`, then `gauntlet/cp-22`, within the same minute as the stash below). Its disposition is
    the Owner's.
  - `stash@{0}: On gauntlet/cp-22: !!GitHub_Desktop<gauntlet/cp-22>`, created by GitHub Desktop on 2026-10-01
    22:08 IDT while the Lead was paused. It held the two then-untracked post-freeze modules (`src/cp22/controls.py`,
    `src/cp22/daily.py`); the Lead restored them from it and left the stash in place. Its disposition is the Owner's.
- `main` not touched by the Lead (its move above is not this checkpoint's), nothing staged on `main`, nothing
  pushed, no remote ref, no public write (MLflow tracking local only; `remote_writes` 0).
- State verified at the start: `main` = `origin/main` = `940eb98`, a direct child of `ddb9379` adding exactly the
  six named documents; no `gauntlet/*` branch, no other worktree, no stash; clean tree; `land/cp-21` = `4e37cf7`,
  `evidence/cp-21` = `1d13f99`; CP-21's evidence and retained fit cache, CP-20's evidence, weather grids and HG
  component cache present and verified. No material mismatch.

## Complete checklist with direct evidence

| # | Checklist item (§20.10) | Status | Direct evidence (path, command, or metric) |
|---|---|---|---|
| 1 | Verify the starting state; package the brief; commit the frozen pre-run protocol before any outer scoring | Done | Anchor, amendment and PUBLISH_RULES hashes verified at the start and by `cp22.inputs.identities()` (raises on mismatch) before the protocol was written, and again by the Critic on `main` and at the candidate (the protocol record's `capstone_v21.md` key is mislabelled: see Disclosures); brief packaged byte for byte at `a3342f3`; protocol committed at `9afc1f9` (16:01:59 IDT, 2026-10-01) before the first main fit (`fits-warmup`, 16:02:05) and before any scoring, with arms/members, grid, inner split and tie rule (`capacity_grid`, `selection`), DL and fast-component parameters with fixtures (`interval_layers`, `fixtures`), seeds, manifest and cache identities, caps, and `rules_verbatim`; prior evidence untouched; the stash above preserved |
| 2 | Verify the inputs; reuse HG/CP-21 vectors only with verified identity; reproduce an HG and v4 slice; no retrieval, nothing after 2026-04-07 | Done | `reports/v4-revision/preflight/input-verification.json` (population, manifest, HG and CP-21 identities, `max_materialised_date` 2026-04-07), `preflight/weather-regeneration.json` (frozen weather), `reproduction.json` (independent representative HG and v4 slice, refitted: `all_bitwise` true); `download_bytes` 0 |
| 3 | Implement PN, its two forms, the composites and DL; training-only selection; the ladder's one-change-per-step property | Done | `src/cp22/pn.py`, `dl.py`, `execution.py` (hash-frozen in `protocol.json` `implementation_sha256`); `controls.json` (training-only selection, averaging and selection identity over all 636 PN fits, composite parity on every key, ladder rows); `tests/cp22/test_pn_and_composites.py`, `test_dynamic_layer.py` |
| 4 | Every §20.7 and §17.7 control, negative paired with positive | Done | `reports/v4-revision/controls.json`: 71 checks, `all_passed` true |
| 5 | All 10,747 keys for every new policy; finite, ordered quantiles; emitted p50 separate from the central | Done | `predictions.parquet`: R, M, A-PN-sel, A-LP, A-LN, v4+DL, v3+DL each 10,747 unique keys, every quantile finite and non-decreasing, `p50` stored apart from `central` |
| 6 | Score every policy; verify scores, diagnostics, coverage with width and all six §8 diagnostics | Done | `metrics.csv`, `diagnostics.csv`, `uncertainty.csv`, `criteria.csv`, `replicates.parquet`; v3/v4 rows reproduce CP-20's and CP-21's committed rows (`replacement.json` `consistency_with_committed`); re-derived by `tests/cp22/test_saved_evidence.py` and independently by the Critic |
| 7 | Apply the three rules mechanically, each with its first unmet condition; every §20.5 contrast with its reading; statuses distinct | Done | `decisions.json`: replacement none (R → 4, M → 4); dynamic layer and fast component not applicable (no W); 16 contrasts with readings (below); `report.md` Verdicts table |
| 8 | §20.5's diagnostics, including the Owner's investigation | Done | `investigation.json`, `investigation/*.csv` (ladder, member-weight curve, capacity stability, extrapolation, reaction, regimes, alpha paths, shock days, LEAR stability), `fit-cost.json`, `fit-cost-by-origin.csv`, `daily-cycle.json` |
| 9 | Enforce and report every §20.8 cap; respect the calendar | Done | Cumulative ledger, every counter reserved before use; `resources.json` (candidate) and `resource-final.json` (final, below); calendar: no job between Friday 00:00 and Saturday 20:33 IDT; 15 jobs from 20:35 to 21:31 IDT on Saturday under the Owner's written exception, each logged as `owner_calendar_exception_used` |
| 10 | Durable evidence, executable reproduction commands, byte-exact storage | Done | `artifact-manifest.json` (SHA-256 of 81 files), `lineage.json`, `reproduce.md`, `reports/v4-revision/.gitattributes` and `docs/track-b/evidence/cp-22/.gitattributes` (`* -text`) |
| 11 | §20.9's packet and draft export; public surfaces and the published export set unchanged; CI green; no public write | Done | `docs/track-b/evidence/cp-22/publication-packet.md`, `docs/track-b/research-content/cp22-claims.md` (lint 0), `draft-registry.json`, `mlflow-export-draft/cp22.json`, `mlflow-local.json` (read back equal), `published-export-diff.json` (28 runs, only identity, no substantive change); `mlflow_export.py --check`, `--draft cp21 --check`, `--draft cp22 --check`, `cp22.packet --check`, `cp22.claims --check` exit 0. CI runs on push, which is not authorized; its steps were run locally on a clean detached checkout of the candidate (payload build, full suite 1306 passed / 8 skipped, `verify_release.py` 0, `publication_guard.py tree` 0). `remote_writes` 0 |
| 12 | One fresh, independent Integration-Critic PASS on a clean detached checkout of the final candidate | PASS | `docs/track-b/evidence/cp-22/integration.md` |
| 13 | Return the canonical packet with the publication packet; both SHAs, a verdict-only delta, resource totals, branch and worktree accounting; stop at CP-22's local result | Done | This file; publication packet as above; stopped here |

### Every §20.5 contrast, with its reading (equal-fold ΔS, 95% intervals; `decisions.json`, `uncertainty.csv`)

| Contrast | Role | ΔS_MAE [95%] | ΔS_WIS [95%] | Reading |
|---|---|---|---|---|
| R − v4 | replacement | +0.0011 [−0.0031, +0.0054] | +0.0010 [−0.0028, +0.0049] | no demonstrated joint preference |
| M − v4 | replacement | −0.0013 [−0.0036, +0.0016] | −0.0008 [−0.0030, +0.0022] | no demonstrated joint preference |
| R − M | full vs minimal refinement | +0.0025 [−0.0016, +0.0058] | +0.0018 [−0.0018, +0.0049] | no demonstrated joint preference |
| A-PN-sel − M | dropping the raw half | +0.0015 [−0.0025, +0.0048] | +0.0005 [−0.0030, +0.0040] | no demonstrated joint preference |
| R − A-PN-sel | averaging vs daily selection | +0.0010 [−0.0009, +0.0025] | +0.0012 [−0.0006, +0.0026] | no demonstrated joint preference |
| A-PN-sel − A-LP | normalized vs raw, pooled | −0.0023 [−0.0102, +0.0041] | −0.0030 [−0.0099, +0.0035] | no demonstrated joint preference |
| A-LN − v4 | blocks under normalization (descriptive) | +0.0006 [−0.0035, +0.0043] | +0.0001 [−0.0035, +0.0038] | no demonstrated joint preference |
| v4+DL − v4 | DL on v4 (descriptive) | +0.0022 [−0.0041, +0.0077] | +0.0225 [+0.0161, +0.0308] | no demonstrated joint preference (WIS wholly worse) |
| v3+DL − v3 | DL on v3 (descriptive) | +0.0018 [−0.0041, +0.0072] | +0.0231 [+0.0165, +0.0316] | no demonstrated joint preference (WIS wholly worse) |
| R − v3 | reference | −0.0290 [−0.0366, −0.0210] | −0.0256 [−0.0322, −0.0185] | observed joint improvement |
| M − v3 | reference | −0.0314 [−0.0382, −0.0229] | −0.0274 [−0.0334, −0.0200] | observed joint improvement |
| A-PN-sel − v3 | reference | −0.0300 [−0.0376, −0.0219] | −0.0269 [−0.0336, −0.0192] | observed joint improvement |
| A-LP − v3 | reference | −0.0277 [−0.0351, −0.0179] | −0.0238 [−0.0310, −0.0156] | observed joint improvement |
| A-LN − v3 | reference | −0.0295 [−0.0365, −0.0227] | −0.0266 [−0.0328, −0.0205] | observed joint improvement |
| v4 − v3 | reference | −0.0301 [−0.0368, −0.0228] | −0.0266 [−0.0327, −0.0204] | observed joint improvement |
| v4+DL − v3 | reference | −0.0279 [−0.0372, −0.0189] | −0.0041 [−0.0112, +0.0050] | no demonstrated joint preference |

Not applicable without a winner W (§20.6), so not run: (W+DL) − W, (W+ACI) − W, (W+DL) − (W+ACI), (W+DLF) − (W+DL),
and the shock-day comparison of W, W+DL and W+DLF (the same windows are reported for v4, v4+DL, v3 and v3+DL).

**Condition 4, per fold (EUR/MWh, paired daily-loss differences against v4):** R fold 4 MAE +0.31 [+0.15, +0.42],
WIS +0.18 [+0.10, +0.23]; M fold 4 MAE +0.20 [+0.05, +0.33], WIS +0.11 [+0.02, +0.20]. No other fold has a lower
endpoint above zero for either policy.

## Integration verdict

- Path: `docs/track-b/evidence/cp-22/integration.md`   Result: **PASS**
- Candidate SHA it binds: `29d8d383a8870fee10b04158c5e3e5fd89514fdc`
- The Critic recomputed every metric, interval, §8 diagnostic, verdict, first unmet condition and reading (`cp22.review --score`: 105/192/189 rows, 0 unmatched, 0 NaN-pattern mismatches, max difference ≤ 5.7e-14) and, with its own code, re-derived all 192 intervals from the stored draws and regenerated the CP-20 index set; refitted PN at fold 3, 2022-08-16 (PN-avg and PN-sel bitwise; trees, losses, selection equal) and checked selection and averaging at all 636 origins; replayed M (H) and v4+DL (DL) bitwise from the admission-freeze states and rebuilt the DL quantiles (≤ 1.7e-12) and α_t path (438/438) independently; re-derived the packet, claims and draft export identically. Its `review.json` (SHA-256 `99cf10d5…23c2`) is committed beside the verdict. It marked item 13 "not yet due" (this return).

## Reproduction

`reports/v4-revision/reproduce.md` gives the full sequence. The checks below were run on the candidate, each under
the monitor (charged to the ledger):

| Command | Result |
|---|---|
| `scripts/cp22_revision.py job …` sequence (protocol → fits → admission → comparison → parity → score → controls → daily-cycle → finalise) | each exit 0, apart from the disclosed `investigation` ×2 and the stopped `controls` (`defects-and-repairs.md`) |
| `pytest tests/cp22` | 27 passed |
| `python -m cp22.packet --check`; `python -m cp22.claims --check` | exit 0; claim-map lint 0 findings |
| `mlflow_export.py --draft cp22 --check`; `--draft cp21 --check`; `--check` | exit 0 each |
| `mlflow_export.py --diff-against 940eb98…` | 28 → 28 runs, only identity, no substantive change |
| `verify_release.py`; `python3 publication_guard.py tree` | exit 0 each |
| Full suite on a clean detached checkout, before CI's payload step (#54) | 3 failed, 12 errors, all in `tests/test_22_wasm_equivalence.py`: `app/public/` absent (generated, Git-ignored; CI builds it first) |
| The same checkout after CI's payload step (`build_wasm_payload.py`, #55; suite #56) | 1306 passed, 8 skipped |
| Full suite in the Lead's own checkout | 3 failures from local state only (a stale gitignored `dist/space-wasm` build from 2026-10-01 13:41 IDT; `marimo` not on the monitor's PATH); disclosed in `defects-and-repairs.md` |
| Lead's dry run of `cp22.review` (`--pn fold_3:2022-08-16`, two replays; `--score` comparison against the committed tables, no pass spent) | PN-avg, PN-sel, trees, losses and selection equal; both replays bitwise |
| The Critic's `cp22.review --score --pn … --replay …` and its own checks | exit 0 throughout (ledger #58–#72); full suite 1307 passed, 7 skipped (none CP-22's); CI's named steps 23 passed; its first attempt at the review line failed in zsh before the monitor started (exit 127, uncharged) |

## Files changed

`git diff --stat 940eb98..<evidence_tip_sha>`: 86 files, all under the paths below (no file outside them):

- `docs/track-b/evidence/cp-22/` — the issued brief (byte for byte), `.gitattributes`, the publication packet, the
  Integration verdict and the Critic's `review.json`, `resource-final.json`, this return.
- `docs/track-b/research-content/cp22-claims.md` — the claim-to-evidence map for PRES-4.
- `reports/v4-revision/` (50 files) — the protocol, preflight, lineage, predictions and members, both scoring
  outputs, decisions, controls, parity, reproduction, diagnostics, investigation, packet artefacts, report,
  reproduction commands, disclosures, resources and the artefact manifest.
- `src/cp22/` (20 files) — the CP-22 implementation; the frozen modules hash as `protocol.json` records.
- `tests/cp22/` (5 files) — synthetic-fixture tests and re-derivations from committed rows.
- `scripts/cp22_revision.py` (the frozen driver), `scripts/cp22_owner_calendar_exception.py` (the Owner's scoped
  calendar exception), `scripts/mlflow_export.py` (the CP-22 draft path; CP-21's path and the published set
  unchanged).

## Resources against §20.8 (final ledger, `docs/track-b/evidence/cp-22/resource-final.json`)

| Dimension | Used | Cap |
|---|---|---|
| active effort (hard ceiling) (`active_seconds`) | 2.44 h | 32 h |
| peak added disk (`additional_disk_bytes`) | 0.30 GiB | 10 GiB |
| bootstrap passes (`analysis_passes`) | 2 | 3 |
| HG component-day attempts (`component_attempts`) | 124 | 1,600 |
| bytes downloaded (`download_bytes`) | 0 | 0 |
| LightGBM fits (total) (`lgbm_fits`) | 5,784 | 9,000 |
| machine time (wall × workers) (`machine_seconds`) | 3.78 h | 30 h |
| LightGBM fits (main) (`main_lgbm_fits`) | 5,088 | 6,000 |
| replay policy-days (`policy_days`) | 6,406 | 16,000 |
| Lasso primitive fits (`primitive_fits`) | 14,880 | 192,000 |
| reference passes (`reference_passes`) | 2 | 3 |
| remote writes (`remote_writes`) | 0 | 0 |
| peak aggregate RSS (`rss_bytes`) | 3.00 GiB | 10 GiB |
| concurrent workers (peak) (`workers`) | 4 | 4 |
| BLAS threads | 1 in all 73 jobs | 1 |
| external cost | $0 (no cloud, no GPU) | $0 |

By purpose (uncapped, inside the totals): LightGBM main 5088, benchmark 32, control 228, daily cycle 350, reproduction 70, review 16; policy-days admission 1316, evaluation 3150, parity 1276, control 484, daily cycle 50, review 130. 73 jobs in the ledger (`jobs_total`), every one charged, failed and stopped ones included. The reference and bootstrap passes: pass 1 (`score-replacement`) and the Critic's review; the Lead's `review-dryrun` (#57) replaced the scoring call with a reader of the committed tables and computed no pass, so none was charged.

## Elapsed

About **2.5 active hours** by the ledger (2.44 h when `resource-final.json` was written: from the Lead's first command, Thursday 2026-10-01 15:37:39 IDT, less the recorded idle pauses), against the brief's ~24-hour timebox and 32-hour ceiling. Active stretches: Thursday 15:37–16:10 and 21:01–21:04; Saturday 20:09–20:12 (status and clock checks only, no job, before the Owner's exception) and 20:33–21:35; Sunday from 01:10 to the evidence commit. The Critic notes that the pauses cannot be verified to the minute; its deliberately conservative bound (all wall time outside the Friday/Shabbat window) is about 14 h, also inside the timebox.

## Disclosures after the candidate (none changes a number, verdict or cap outcome)

- **A mislabelled hash in the frozen protocol's identity record** (the Critic's observation 1, confirmed by the Lead). In
  `protocol.json` `issued_and_inherited_sha256` and `preflight/input-verification.json`, the key `capstone_v21.md` carries
  CP-20's v21-r4 hash `150bd53f…` instead of v21-r9's `5fc9c686…`: CP-21's inherited `cp20_identities()` overwrites the key
  after `cp22.inputs.identities()` has already checked the tree against `5fc9c686…`, and that check raises on mismatch. The
  check ran and passed; only the record is mislabelled. The anchor's v21-r9 hash was verified at the start, by the Critic on
  `main` and at the candidate, and is recorded correctly in the brief and in this return. The protocol is hash-frozen and
  was not edited.
- **The Lead's `review-dryrun`** (ledger #57, after the candidate commit, before the Critic) exercised the never-run
  review module: its PN refit and two replays for real (charged: 8 review fits, 65 review policy-days) and its `--score`
  comparison code with the scoring call replaced by a reader of the committed tables (no pass computed, none charged;
  wrapper `.local/tmp/cp-22/review-dryrun.py`). The Critic did not open its output.
- **The Lead's first clean-checkout suite** (#54) ran before CI's payload-build step and failed only in
  `tests/test_22_wasm_equivalence.py`, which requires the generated, Git-ignored `app/public/`; after the payload step (#55)
  the suite passed (#56). The Critic's brief was then given CI's preparation step.
- **`resources.json`** in the candidate is the candidate-time snapshot; `resource-final.json` here is the final ledger.
- **Before the candidate:** the claim-map drafting correction and the Lead-checkout suite failures are disclosed in
  `reports/v4-revision/defects-and-repairs.md`. The second idle gap (Saturday 21:35 to Sunday 01:10 IDT, after the
  usage limit stopped the session) was recorded as a ledger pause on resumption, with its reason.

## Open risk or exact owner action

- **The Owner's decision under §20.6**: with no replacement, CP-22 stops here; three-block v4 stays current until
  the Owner decides.
- **The landing** (Owner, by hand): squash `gauntlet/cp-22` onto `main` (now `32bdf9b`; disjoint paths) and tag
  `land/cp-22` at the squash commit and `evidence/cp-22` at the evidence tip. Nothing is published before PRES-4.
- **Two items not from this checkpoint** for the Owner's disposition: branch `claude/automation-plan-corrections-t45wdc`
  and the move of `main` to `32bdf9b` (both described under Repository state).
- **The GitHub Desktop stash** `stash@{0}` (not the Lead's): it holds earlier versions of `src/cp22/controls.py` and
  `src/cp22/daily.py`, whose final versions are in the candidate; keep or drop it at the Owner's discretion.

## Landing report

- Proposed disposition: **LAND** — a complete, valid "no replacement" result with its Integration verdict is the
  durable record of the decision the Owner now takes; the product does not change.
- Evidence tip to preserve: the evidence tip SHA in the terminal message (tag `evidence/cp-22`).
- Live documents citing this branch (to repoint on reclamation): none outside the branch. `capstone_v21.md` names
  `gauntlet/cp-22` procedurally (where CP-22 works); the SHAs CP-22's own evidence cites (the candidate, the
  admission freeze `94439d0`, the protocol `9afc1f9`) stay reachable through `evidence/cp-22`.
- Proposed commit message: `CP-22: v4 revised, one pooled member and a dynamic interval layer — no replacement
  (cp22-replacement: R and M fail condition 4 on fold 4); the layer rules do not apply; development evidence,
  v1 unchanged`

## Interview-answer triggers (named here; the Orchestrator files)

- Why both pooled members passed non-inferiority overall yet failed the per-fold condition on fold 4 alone.
- Why the dynamic interval layer reacted faster at the 2022 crisis onset (4 days against 12) yet worsened the
  interval score overall.
- How an Owner's mid-checkpoint calendar exception was honoured without editing hash-frozen code or the anchor.

## Post-return reads

none
