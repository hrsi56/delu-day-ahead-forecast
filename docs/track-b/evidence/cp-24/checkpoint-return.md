# Track B Checkpoint Return — CP-24

## Status

**PASS.** CP-24 closes on the result its branch records: **v5 is adopted in research, in scored attempt 1.** One
fresh Integration-Critic PASS, on a clean detached checkout, binds the final candidate. That candidate also meets the
continuation brief's three conditions.

**The research verdict:** `cp24-adoption` (§23.9), applied mechanically.

- All five conditions are met, so the first unmet condition is none.
- v5 − v4:
  - ΔS_MAE −0.0133, 97.5% [−0.0166, −0.0091]; as a share of v4's score, −2.49%, 97.5% [−3.04%, −1.68%];
  - ΔS_WIS −0.0119, 97.5% [−0.0147, −0.0084]; as a share, −2.36%, 97.5% [−2.86%, −1.62%].
- D2 alone against v4: −10.67% S_MAE and −15.53% S_WIS. It is never eligible. Leakage is ruled out at full
  coverage (below).

**Statuses, kept distinct:**

- **Engineering:** PASS, under the verdict below.
- **Research:** a `development_post_selection` adoption, the second DDNN decision on these five folds. 4.7T carries
  the protection.
- **Product:** unchanged. v1 is the released product and the demo; there is no designation, freeze or Live (§16).

**What this continuation did, against its brief:**

1. **The landing-safety repair.**
   - **The defect.** `tests/cp24/test_base_tree.py` hashed all 1,322 files tracked at `522d7ea`, `progress.md`,
     `capstone_v21.md`, `AGENTS.md`, `README.md` and `docs/index.html` among them. A simulated LAND of the
     pre-continuation tip `9667fb4` onto today's `main` already failed it: 1 failed, 1,474 passed.
   - **The repair.** "Unchanged" is now proved for one candidate commit, by
     `python -m cp24.basetree --check-rev <candidate>`. That Git-object check needs every recorded file
     byte-identical, and every other file in the commit under CP-24's write paths. The default-suite test checks
     only CP-24's own record and the checker itself, on fixtures.
   - **The other CP-24 tests, audited.** `test_draft_export.py` no longer hashes CP-23's lock. The one remaining
     binding of a non-CP-24 file is `test_reference_record.py`'s check of CP-23's test-only lock. That test is part
     of attempt 1's frozen implementation, so it stays, and CP-23's own tests bind the same file
     (`defects-and-repairs.md` item 12).
   - **The evidence that CI stays green after the LAND** is `cp24.landsim`, run at the final candidate
     (`land-simulation.md`). It builds the exact squash tree in a fresh one-commit, tagless repository and runs CI's
     steps there:
     - squashed onto `main` `7ff6a50`: green, 1,479 passed, 13 skipped, with all six CI steps exiting 0;
     - the candidate's own tree: green, 1,439 passed;
     - squashed, with simulated later edits to 8 living files: 3 failures. All three bind CP-23's test-only lock or
       `scripts/mlflow_export.py`; two are CP-23's own tests, and the third is the frozen CP-24 test named above. No
       repaired CP-24 test fails.
   - **A correction (verdict observation O1).** `defects-and-repairs.md` item 11 says the edited run is green too.
     It is not, as stated here and in `land-simulation.md`.
2. **The item-9 control decision.**
   - **Decision: extended.** The committed controls (80 of 80) did not by themselves support item 9 for a member this
     strong. Their masks were proven at two origins, with member 0 and one weather member, and their search and gate
     negatives for one fold each. A leak confined to another input group of the 20 frozen configurations, to another
     fold or to another origin would have passed them.
   - **The extension.** `cp24.leakage` (job `leakage-a1`) is verification only: no frozen element changed, nothing
     was rescored, and it cost 5,294 control fits within §23.11.
   - **The results** (`attempt-1/leakage-controls.json`, 12 of 12 checks):
     - at all 636 warm-up and evaluation origins, the frozen eight-member ensemble, refitted with every outcome on or
       after the delivery day destroyed, reproduces the committed D2 vectors bit for bit (636 of 636), with every
       member at its recorded weights;
     - all 10,747 scored keys equal `predictions.parquet`;
     - a D−1 evening price mutation moves the ensemble at 22 of 22 stratified origins;
     - a planted one-day leak is detected in 5 of 5 folds;
     - the search and gate negatives and positives hold fold by fold in all 5 folds;
     - 5,088 member windows, 3,464 search batches and the gate days are structurally clean.
   - **Independent confirmation.** Critics 3 and 4 each confirmed this with their own destroy-the-future refits at
     origins of their choice.
3. **Every interruption, accounted for.**
   - **Critic records 1 and 2** (at `5fd4e3a` and `d637590`) had no verdict. Both are closed in `critic-open.json`
     with `verdict_sha256: null` and a written disposition.
   - **The `critic-2` worktree** was removed under the brief's authorization. Its partial output stays unread in
     `.local/artifacts/cp-24/critic-2/`, and no later Critic received anything from Critics 1 or 2.
   - **The idle gap,** 2026-10-05 14:28Z to 2026-10-10 16:54Z (122.43 h), is recorded in the ledger as an idle pause.
4. **The review route.**
   - Critic 3 failed candidate `7ea9bdd` on one gap: §23.8's ratio intervals were reported at 95% only, not also at
     97.5%. Its verdict is preserved in `review/critic-3-integration-FAIL.md`.
   - The repair, `cp24.ratios`, derives the 97.5% intervals from the committed stored draws, with no pass and no
     frozen file changed.
   - Critic 4 passed the repaired candidate `7949a98`.

## Identity

- **Repository, checkpoint and anchor:**
  - DE-LU day-ahead forecasting (`/Users/djourno/Downloads/PJM`, origin `hrsi56/delu-day-ahead-forecast`), CP-24.
  - `capstone_v21.md` v21-r11 §23, SHA-256 `11068e3f57bd9277be50db62d109f3e7d8ea7b8fdfa042886ccc4ae5ab1ed2d2`,
    verified at the candidate. Its calendar clauses are superseded by `AGENTS.md` § Work availability, introduced at
    `main` `7ff6a50cb54ad34a7f0e52981e18f990fa0323bb` by the Owner's decision of 2026-10-10.
- **Briefs:**
  - the issued brief `docs/track-b/evidence/cp-24/issued-brief.md`, SHA-256 `a3f11470…34bd0`, packaged in `1cead62`;
  - the continuation brief `docs/track-b/evidence/cp-24/continuation-brief.md`, SHA-256 `5960b908…86e4ec`. The
    Owner's maintenance commit `9667fb4698076fe942aae2246e44366e91efd388` had already packaged it byte for byte, and
    `cmp` against the canonical copy shows them equal. The pasted text matched the canonical file apart from markdown
    rendering.
- **final_candidate_sha: `7949a98f80c81c5a789dd69c213da16c811d345c`** (every bar binds here).
- **evidence_tip_sha:** the commit on `gauntlet/cp-24` that adds this file, directly on the candidate. A commit cannot
  contain its own SHA, so it is printed by `scripts/gauntlet.py return` and resolved by
  `git rev-parse gauntlet/cp-24`.
- **The delta.** `git diff --name-only 7949a98f80c81c5a789dd69c213da16c811d345c..<evidence_tip_sha>` lists only
  these files, all under `docs/track-b/evidence/cp-24/`:

  ```text
  docs/track-b/evidence/cp-24/checkpoint-return.md
  docs/track-b/evidence/cp-24/integration.md
  docs/track-b/evidence/cp-24/land-simulation.md
  docs/track-b/evidence/cp-24/resource-final.json
  ```

## Repository state

- **Branch:** `gauntlet/cp-24` at the evidence tip, local only, with its worktree `.local/worktrees/cp-24/lead`
  clean. It was created on 2026-10-05 by CP-24's first Lead.
- **Created and removed by this continuation:**
  - the Critic worktrees `.local/worktrees/cp-24/critic-3` and `critic-4`, created by `critic-open` and removed by
    `critic-close`;
  - the worktree `critic-2` (created on 2026-10-05), removed under the brief's authorization.
- **Created by this continuation:** no branch, no tag, no stash.
- **Not created by CP-24, and escalated to the Owner:** the branch `codex/final-product-price-lock-plan` at
  `7ff6a50`, with its worktree `.local/worktrees/final-product-price-lock-plan`. It appeared at about 18:55Z on
  2026-10-10 with 6 uncommitted paths, from another session. CP-24 did not touch it.
- **`main`:** `main` = `origin/main` = `7ff6a50`, unchanged during the continuation. Nothing staged on `main`,
  nothing committed there, nothing pushed, no tag, no remote write. The Owner moved `main` from `522d7ea` to
  `7ff6a50` before the continuation.
- **Retained recovery material:**
  - `.local/artifacts/cp-24/`: the ledger, the caches, the logs, the leakage records, the LAND-simulation records
    and the Critic records;
  - `.local/artifacts/cp-24-orchestrator/pause-2026-10-05/`, which is the Orchestrator's.
  - **Keep before any cleanup (verdict observation O2).** The 188 warm-up and 280 gate-day DDNN-2 vectors exist only
    in `.local/artifacts/cp-24/attempt-1/fits/` and `rounds/round-1/gate/`. The committed vectors cover the 10,747
    evaluation keys, and 4.8 may need the rest.
  - The disposable simulation trees were deleted.

## Complete checklist with direct evidence

The checklist is §23.13 v21-r11, all eighteen items.

| # | Checklist item | Status | Direct evidence |
|---|---|---|---|
| 1 | Verify the starting state; baseline with `gauntlet.py start`; work in `lead` on `gauntlet/cp-24`; package the issued brief | Met | `.local/artifacts/cp-24/start.json`; brief packaged in `1cead62`, byte-identical; the continuation re-verified the state and reported the mismatches: `main` moved by the Owner, maintenance commit `9667fb4` |
| 2 | Verify the inputs | Met | `d5aee2d`; `reports/ddnn2/preflight/input-verification.json`, `weather-regeneration.json`; CP-23's D reproduced at `evidence/cp-23`; nothing after 2026-04-07 |
| 3 | Complete 4.6L′ | Met: PASS | `reports/ddnn2/licence-admission.md` (`d5aee2d`) |
| 4 | Prove the code's correctness | Met | `36764cb`; `reference-checks.json` 32 of 32, 0 skipped (rerun by Critic 4); import audit; finite-difference tests `tests/cp24/test_ddnn2_gradients.py` |
| 5 | Complete 4.6R′ | Met: PASS | `1e2cf6b`; `resource-admission.md` (128 trials per fold per round) |
| 6 | Run every pre-fold round | Met: one round | `0a423fb` (search ledger and ensembles), `645dc92`: gate PASS with G1 12.538 ≤ 12.849, G2 0.8525 ≤ 1.10, G3 0.088% < 0.1% |
| 7 | Commit every S1 exchange and each attempt's frozen protocol before its fits | Met | S1 `031f826`, `118089a`; protocol `62b8e51`, an ancestor of `dea6664` (lineage) and `cb52fe2` (predictions), and before `attempt_1_first_fit` in the ledger |
| 8 | Implement exactly DDNN-2, v5 and the arms; composite parity | Met | `controls.json` population: parity on every key ≤ tolerance; `tests/cp24/test_composites_and_rule.py` |
| 9 | Prove every control, each negative paired with a positive | Met | `controls.json` 80 of 80; `leakage-controls.json` 12 of 12 at full coverage (see Status, part 2) |
| 10 | 10,747 keys per new policy, finite and ordered; p50 kept separate from the central forecast | Met | `predictions.parquet`; `test_saved_evidence.py` |
| 11 | Score every policy and verify the scores, diagnostics, coverage with width, and §8 | Met | `f7eb23e`; `metrics.csv`, `uncertainty.csv`, `diagnostics.csv`; Critic 4 recomputed them with its own code to within 1e-13, and regenerated 200 stored replicates exactly |
| 12 | Apply `cp24-adoption` mechanically; every contrast with its reading; statuses distinct | Met | `decisions.json`, `adoption.json`; `report.md` contrast table, with 95% and 97.5% difference and ratio intervals (`ratio-intervals.csv`) |
| 13 | Respect the attempt bounds | Met | one scored attempt, adopted, so there was no S2 and no attempt 2 (§23.6); nothing was rescored after scoring |
| 14 | Deliver §23.8's diagnostics | Met | `d22f053`; `attempt-1/diagnostics/` (13 CSVs), `diagnostics.json`, `fit-cost.json`, `daily-cycle.json` |
| 15 | Store the DDNN-2 vectors; enforce and report every §23.11 cap; respect the calendar | Met | `predictions.parquet`, `members.parquet`, `fits.parquet`, with warm-up and gate vectors in `.local` (retain, see O2); `resource-final.json` within every cap, no raise; the calendar is superseded by `AGENTS.md` § Work availability (Owner, 2026-10-10) and was not reinstated |
| 16 | Durable evidence: reproduction commands, byte-exact storage, the packet and draft export, the unchanged files, CI green, no public write | Met | `reproduce.md`; manifest of 116 files and `* -text`; `publication-packet.md`, `mlflow-export-draft/cp24.json`; `basetree --check-rev 7949a98`: 1,322 files unchanged, 118 added under CP-24's paths; CI green on the candidate and after the LAND (`land-simulation.md`); 0 remote writes |
| 17 | One fresh Integration-Critic PASS on a clean detached checkout of the final candidate | Met | `docs/track-b/evidence/cp-24/integration.md`: PASS at `7949a98f80c81c5a789dd69c213da16c811d345c` |
| 18 | Return the canonical packet, checked with `gauntlet.py return` | Met | this file; `scripts/gauntlet.py return cp-24 7949a98f80c81c5a789dd69c213da16c811d345c` |

## Integration verdict

- Path: `docs/track-b/evidence/cp-24/integration.md`. Result: **PASS**. SHA-256
  `b112a2ca8bf00ee0316f7036110e29e534f812ed435cd8fde7b02be8e541304a`.
- Candidate SHA it binds: `7949a98f80c81c5a789dd69c213da16c811d345c`.
- The superseded review (FAIL at `7ea9bdd`) is at `docs/track-b/evidence/cp-24/review/critic-3-integration-FAIL.md`.

## Reproduction

Run these from the worktree, with `PY=.venv/bin/python` and `PYTHONPATH=src`. The results observed at the candidate
are given after each command.

```bash
$PY -m cp24.basetree --check-rev 7949a98f80c81c5a789dd69c213da16c811d345c
$PY -m cp24.ratios --attempt 1 --check
$PY -m cp24.packet --check
$PY -m cp24.claims --check
$PY -m cp24.report --check
$PY -m pytest -q tests/cp24
$PY -m cp24.landsim --main 7ff6a50cb54ad34a7f0e52981e18f990fa0323bb --candidate 7949a98f80c81c5a789dd69c213da16c811d345c --out <dir outside the checkout>
```

- `basetree --check-rev`: unchanged, 118 added.
- `cp24.ratios --check`, `packet`, `claims`, `report`: identical.
- `pytest tests/cp24`: 80 passed.
- `cp24.landsim`: green.

Run each compute command under the monitor, as `reproduce.md` lists, including `cp24.leakage --attempt 1`. The
attempt-1 entry points refuse at this candidate by design, after the maintenance; they run at `d637590`
(`reproduce.md`, "At the final candidate").

## Files changed

`git diff --stat 522d7ea..7949a98`: 118 files changed, 300,975 insertions, additions only, all under §23.14's write
paths. Files 1–91 are the first Lead's run, through `d637590`: the brief, code, tests, records and evidence of items
1–16. This continuation and the Owner's maintenance changed 27 paths:

- **The Owner's maintenance (`9667fb4`):**
  - `scripts/cp24_ddnn2.py` and `src/cp24/budget.py`: the calendar gates removed;
  - `src/cp24/report.py` and `src/cp24/finalise.py`: the report text and the manifest paths;
  - `tests/cp24/test_work_availability.py`;
  - `docs/track-b/evidence/cp-24/continuation-brief.md` and `work-availability-2026-10-10.md`.
- **The landing safety:**
  - `src/cp24/basetree.py`: adds `check_rev`;
  - `tests/cp24/test_base_tree.py`: the record and checkers on fixtures;
  - `tests/cp24/test_draft_export.py`: no live hash of a non-CP-24 file;
  - `src/cp24/landsim.py`: the read-only LAND simulation.
- **Item 9:**
  - `src/cp24/leakage.py`;
  - `reports/ddnn2/attempt-1/leakage-controls.json` and `leakage-by-origin.csv`;
  - `tests/cp24/test_leakage_controls.py`.
- **Critic 3's gap:**
  - `src/cp24/ratios.py`;
  - `reports/ddnn2/attempt-1/ratio-intervals.csv`;
  - `tests/cp24/test_ratio_intervals.py`;
  - `docs/track-b/evidence/cp-24/review/critic-3-integration-FAIL.md`.
- **The documents:**
  - `src/cp24/report.py` and `src/cp24/claims.py`: the controls section, C441, and the 97.5% ratios;
  - `reports/ddnn2/report.md`, `docs/track-b/research-content/cp24-claims.md` and
    `docs/track-b/evidence/cp-24/publication-packet.md`, regenerated;
  - `reports/ddnn2/defects-and-repairs.md`: items 9–15;
  - `reports/ddnn2/reproduce.md`: the continuation's commands and the route's status at the candidate;
  - `reports/ddnn2/resources.json` and `artifact-manifest.json`: `finalise`.
- **The evidence delta:**
  - `integration.md`: the binding verdict;
  - `land-simulation.md`: condition 1's evidence and the O1 correction;
  - `resource-final.json`: the final totals;
  - this return.

## Elapsed

- **This continuation:** about **3.5 active hours**, from 16:54Z to the return, against its 8-hour timebox.
- **Cumulative:** about **8 active hours**, against §23.11's effort line of about 35 and a hard ceiling of 50. The
  ledger's upper bound reads 7.85 h when `resource-final.json` is written, with four recorded pauses.

**Final resource totals** (`resource-final.json`). No raise was recorded.

| Ceiling | Used | Maximum |
|---|---|---|
| DDNN-2 fits | 16,436 | 40,000 |
| Machine-hours | 18.94 | 150 |
| Policy-days | 4,558 | 12,000 |
| Reference passes | 3 | 3 |
| Bootstrap passes | 3 | 6 |
| Rounds before attempt 1 | 1 | 3 |
| Scored attempts | 1 | 2 |
| Peak aggregate RSS | 4.55 GiB | 10 GiB |
| Peak added disk | 5.36 GiB | 10 GiB |
| Workers | 4 | 4 |
| Data downloads, remote writes, cost | 0, 0, $0 | 0, 0, $0 |

- **The fits by purpose:** search 3,465, gate 2,240, warm-up 1,504, evaluation 3,584, control 5,325 (5,294 of them
  this continuation's leakage controls), daily cycle 200, review 98, resource admission 18, correctness 2.
- **The policy-days** include 840 that Critic 3's `cp24.review --gate` and 840 that Critic 4's `--gate` charged to
  `policy_days_gate` (2,520 in all), not to a review counter.
- **Reference passes reached their cap of 3:** the Lead's scoring, Critic 2's aborted review and Critic 3's review.
  Critic 4 spent none.
- **Bootstrap passes, 3 of 6:** the Lead, Critic 2 and Critic 3.
- **The §14.6 E4 sessions:**
  - the Lead sessions: CP-24's first Lead (2026-10-05, stopped three times by the usage limit) and this continuation
    Lead (Claude Code, 2026-10-10);
  - the reviewers: Critics 1 and 2 (no verdict), Critic 3 (FAIL) and Critic 4 (PASS). Each was a fresh general-purpose
    subagent launched with `critic-open`'s printed prompt.

## Open risk or exact owner action

- **The LAND** is the Owner's, by hand (`scripts/gauntlet.py land-commands cp-24`), followed by the closure records.
- **Decide on `codex/final-product-price-lock-plan`** and its worktree. They were not created by CP-24.
- **Retain the `.local` warm-up and gate-day DDNN-2 vectors (O2)** before any reclamation.
- **A later change to CP-23's test-only lock** needs the Owner's `AMENDED_BY_…` treatment in CP-23's tests and in
  CP-24's frozen `test_reference_record.py`. A later change to `scripts/mlflow_export.py` needs it in CP-23's tests.
- **Publication** stays the Owner's decisions under §23.12: v5's encoding and the A3 transition.

## Landing report

- **Proposed disposition:** LAND. Engineering PASS on a mechanically adopted research result, and the squash is
  verified green on today's `main`.
- **Evidence tip to preserve:** the tip of `gauntlet/cp-24` after this commit (`git rev-parse gauntlet/cp-24`), to be
  tagged `evidence/cp-24`.
- **Live documents citing this branch** (`gauntlet.py citations cp-24`):
  - `progress.md:105`, live, to repoint at reclamation;
  - `capstone_v21.md` lines 3701 and 3798, locked and historical, never repointed.
- **Proposed commit message:** `CP-24: DDNN-2 — v5 adopted in research in scored attempt 1 (v5 = v4 + 1/6 DDNN-2); leakage ruled out at all 636 origins; landing-safe evidence`

## Post-return reads

`gauntlet.py citations cp-24` printed one line of `progress.md` while this return was being written. There were no
other reads of program material.

**Interview-answer triggers:**

- ruling out leakage for a surprisingly strong member by an exhaustive future-blind refit, rather than more spot
  controls;
- a test that bound living files and would have turned `main` red after the LAND;
- an Integration FAIL on a presentation-only 97.5% ratio interval.
