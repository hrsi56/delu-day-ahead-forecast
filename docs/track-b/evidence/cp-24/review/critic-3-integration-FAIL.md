# Verdict — CP-24 — Integration — FAIL

- **Candidate SHA:** `7ea9bdd73fb7df50991083e674c4dad24335aaf0` (local branch `gauntlet/cp-24`; base `522d7ea722b5d215d827d7aed9c56b7a9dec066e`; `main` = `origin/main` = `7ff6a50cb54ad34a7f0e52981e18f990fa0323bb`, moved by the Owner, not by CP-24).
- **Plan / version / bar:** `capstone_v21.md`, revision **v21-r11**, SHA-256 `11068e3f57bd9277be50db62d109f3e7d8ea7b8fdfa042886ccc4ae5ab1ed2d2` at the candidate (`main` now carries v21-r12; the candidate is bound to v21-r11). Bar: **§23.13 "Complete CP-24 acceptance checklist", all eighteen items**, governed by §23.1–§23.12 and §23.14 with their inheritances, plus the continuation brief's three conditions (`docs/track-b/evidence/cp-24/continuation-brief.md`, SHA-256 `5960b90855910c8deb433b83ffedd93add7c494fcc10833a5f25f2b16686e4ec`). Section identity from the generated brief: 77 lines, 4,591 bytes, SHA-256 `5ffb90a3bd275ad59cc8fd8d60103a683ba590b946bda1a54e50211e1b164abe`.
- **Reviewer:** one fresh Integration Critic session, launched with the prompt `git show main:scripts/gauntlet.py | python3 -I - critic-brief cp-24` (record `critic-3`, opened 2026-10-10T19:08:13Z, assignment `.local/artifacts/cp-24/critic-assignment-3.md`, SHA-256 `c111bdd0…5da536`, unchanged — `critic-brief` re-checks it). It received only the generated brief. It did not open `.local/artifacts/cp-24/critic-1/` or `critic-2/`, the Lead's worktree, the Lead's notes, `progress.md` or `orchestrator-role.md`. **Disclosure:** the session's harness context carried the Owner's auto-memory index, and at orientation this session read two memory notes (the retired-tooling note and the CP-24 continuation note, which names the continuation brief's original hash `11063a11…`). That hash differs from the packaged `5960b908…`; the difference is explained by the brief's own "Maintenance update — 2026-10-10" section and by `docs/track-b/evidence/cp-24/work-availability-2026-10-10.md`, and nothing else in the review relied on the note. Isolation is cooperative: a clean detached `git worktree`, no read-only mount.
- **Worktree clean before and after:** yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/cp-24/critic-3 status --porcelain` was empty and `HEAD` was `7ea9bdd73fb7df50991083e674c4dad24335aaf0` at the start, after every job and immediately before this verdict was written. The payload build wrote only ignored files (`app/public/`, `reports/cp3b/payload.json`).
- **Verbatim bar excerpt** (from the generated brief; checked against the file at the candidate with `bar.py check`, see command 19). The excerpt is the citation. Any line number is a courtesy and is non-binding.

> ### 23.13 Complete CP-24 acceptance checklist
>
> All eighteen items are mandatory. Engineering PASS requires neither admission nor adoption: a
> complete, valid NOT_ADMITTED, gate-stopped or not-adopted result can pass.
>
> **After a stop:**
>
> - a NOT_ADMITTED stop under item 3 makes items 4–14 not applicable;
> - a NOT_ADMITTED stop under item 5 makes items 6–14 not applicable;
> - a stop under item 7 before attempt 1 makes items 8–14 not applicable.
>
> Each not-applicable item is recorded with the stop's evidence, and items 15–18 apply in full.
>
> 1. **Verify the starting state** and preserve prior evidence and other sessions' work.
>    - Verify the ratified anchor's SHA-256 against the brief.
>    - Record the baseline with `scripts/gauntlet.py start cp-24`.
>    - Work only in the worktree `.local/worktrees/cp-24/lead`, on `gauntlet/cp-24`.
>    - Package the issued brief byte for byte as `docs/track-b/evidence/cp-24/issued-brief.md`.
> 2. **Verify the inputs:**
>    - population, manifest and frozen weather, including the coverage gap of §23.6;
>    - saved-vector identities, including CP-23's D, reproduced from the objects preserved at the
>      evidence tags where a live identity check no longer applies;
>    - an independent representative HG and v4 slice;
>    - no retrieval, and nothing after 2026-04-07.
> 3. **Complete 4.6L′.**
> 4. **Prove the code's correctness** under §23.7: the import audit, the finite-difference checks,
>    and the PyTorch reference checks, installed so that they cannot be skipped silently.
> 5. **Complete 4.6R′** on pre-fold data, with PASS or NOT_ADMITTED and its cause. On
>    NOT_ADMITTED, stop, with no gate and no comparison.
> 6. **Run every pre-fold round** (§23.4, §23.6), with no DDNN-2 or new-policy fit at a warm-up
>    or evaluation origin:
>    - each fold's search, recorded in a ledger;
>    - the gate, with v4's members proven on the same code path and the weather-coverage rule
>      applied;
>    - the pre-fold report.
> 7. **Commit every S1 exchange** and, for each attempt that runs, its frozen protocol, before any
>    of its warm-up or evaluation fits. Stop when §23.6 says the route ends.
> 8. **Implement exactly DDNN-2, v5 and the arms,** and prove composite parity.
> 9. **Prove every control** of §23.10 and the inherited ones, each negative paired with a
>    positive.
> 10. **Produce all 10,747 keys for every new policy** in every scored attempt, with finite,
>     ordered quantiles. Keep the emitted p50 separate from the central forecast.
> 11. **Score every policy of every attempt,** and independently verify:
>     - the scores and the diagnostics;
>     - coverage with width;
>     - all six §8 diagnostics for each new policy.
> 12. **Apply `cp24-adoption` mechanically** to every scored attempt. State each decision with its
>     first unmet condition, and every §23.8 contrast with its reading. Keep the Engineering,
>     research and product statuses distinct.
> 13. **Respect the attempt bounds.** Commit the S2 exchange and any attempt 2 under §23.6's
>     bounds. Run at most two scored attempts, and none after an adoption.
> 14. **Deliver §23.8's diagnostics** to `reports/ddnn2/`.
> 15. **Store whatever DDNN-2 vectors exist** for 4.8. **Enforce and report every §23.11 cap,**
>     with any committed raise, and respect the calendar.
> 16. **Supply the durable evidence,** with executable reproduction commands and byte-exact
>     storage.
>     - Deliver §23.12's packet, which records any stop, and the draft export.
>     - These stay unchanged: the public surfaces, the published export set,
>       `scripts/mlflow_export.py`, and the root `pyproject.toml` and `uv.lock`.
>     - CI is green, and there is no public write.
> 17. **Obtain one fresh, independent Integration-Critic PASS** on a clean detached checkout of
>     the final candidate. Launch it with `scripts/gauntlet.py critic-open`, `critic-brief` and
>     `critic-close`. The review independently:
>     - recomputes every scored attempt's metrics, intervals and verdict;
>     - checks the gate's results and the steering record against §23.6;
>     - checks pre-registration by Git ancestry and the ledgers;
>     - reruns the reference checks;
>     - reproduces a representative search trial, a representative DDNN-2 ensemble fit and its
>       emission;
>     - re-derives the packet.
> 18. **Return the canonical packet** (templates §3), checked with `scripts/gauntlet.py return`.
>     It carries:
>     - both terminal SHAs and the verdict-only delta;
>     - resource totals, the number of rounds and scored attempts;
>     - branch, worktree and stash accounting.
>
>     Stop at CP-24's local result.

## Summary

Every scientific and engineering result of CP-24 reproduced. Scored attempt 1's scores, intervals and `cp24-adoption`
verdict recompute exactly, twice: with the frozen scoring code (`cp24.review --score`) and with this review's own
code, which rescored no saved reference. The leakage extension is sound. This review's own future-truncated refits
reproduce the committed D2 vectors bit for bit. The landing-safety repair holds: CI is green on the simulated squash
onto `main`. All three interruptions are accounted for. Every §23.11 cap holds.

**One explicit requirement of the bar is unmet.** §23.8 says: "Ratio intervals are reported at 97.5%, the decision
level, and at 95% for comparison with CP-21 to CP-23." The candidate reports ratio intervals (§17.5's
`R_b = S_policy,b / S_comparator,b − 1`) at 95% only. That holds in `uncertainty.csv` (`ratio_ci_*`), in
`decisions.json` (`ratio_ci`), in `report.md` (ratio points only), in the claim map and in the packet's headline
quantity (b) ("Its 95% interval"). The 97.5% intervals it reports are for the paired *differences* (`ci97.5_*`), not
for the ratios. Nothing in the decision changes: condition 1 is defined on the differences, and the omitted intervals
are derivable from the committed stored draws (command 18). It is still a mandated report of every scored attempt
under §23.8, which governs items 11, 12 and 16. It is also the publication-facing form of the adopted result. Hence
FAIL. The repair is verification-only and small (see "On FAIL only").

## Commands actually run

All from `/Users/djourno/Downloads/PJM/.local/worktrees/cp-24/critic-3` (`WT`), with
`PY=/Users/djourno/Downloads/PJM/.venv/bin/python`, `CP24_PROJECT_ROOT=/Users/djourno/Downloads/PJM`,
`MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1`. "Under the monitor" means
`$PY scripts/cp24_ddnn2.py monitor --workers 1 --name <name> --log .local/artifacts/cp-24/critic-3/<name>.log -- …`,
which charges the shared ledger. Every log and output named below is under
`/Users/djourno/Downloads/PJM/.local/artifacts/cp-24/critic-3/`. This review's helper scripts (`gapcheck.py`,
`indep_score.py`, `blind_check.py`, `search_check.py`) live in the session scratchpad, outside the repository.

1. `git show main:scripts/gauntlet.py | python3 -I - critic-brief cp-24`. Exit 0. A 372-line brief: candidate,
   bar excerpt, assignment, fixed rules, the Integration Critic protocol and the templates §2 form.
2. `git -C $WT status --porcelain` and `git -C $WT rev-parse HEAD`. Empty, `7ea9bdd7…`. Repeated after every job
   and before writing, with the same result.
3. `shasum -a 256` of the candidate's copies, then `cmp` of both briefs against their canonical copies:
   - `capstone_v21.md` = `11068e3f…ed2d2`;
   - the issued brief = `a3f11470…34bd0`, `cmp`-identical to `.local/artifacts/cp-24/issued-brief.md`;
   - the continuation brief = `5960b908…86e4ec`, `cmp`-identical to `.local/artifacts/cp-24/continuation-brief.md`;
   - `docs/PUBLISH_RULES.md` = `5a660864…73b4` (1.3);
   - the packet template = `4efb0185…29cf`;
   - the amendment record = `474017e1…d782`;
   - `tests/cp23/torch-reference/uv.lock` = `b3164a37…fed`.

   All match. On `main`, the anchor (`caf03d70…`) and PUBLISH_RULES (`ccfe6199…`) differ, as the assignment says.
4. The full suite under the monitor, as the brief gives it (`/usr/bin/env -u CP16_LEDGER … -u CP24_WORKERS $PY -m
   pytest -q -p no:cacheprovider -rfEs`; job `critic3-pytest-full`). Exit 1: 3 failed, 12 errors, 1426 passed and
   9 skipped. Every failure and error was in `tests/test_22_wasm_equivalence.py`, because `app/public/` was absent
   ("generated from the committed models/champion/ by make wasm-payload … deliberately not committed"). CI builds
   that payload first.
5. `scripts/build_wasm_payload.py` under the monitor (`critic3-wasm-payload`). Exit 0: 15,363,807 bytes, ignored
   outputs only.
6. Command 4 again (`critic3-pytest-full-ci`). **Exit 0: 1442 passed, 8 skipped.** The skips are `eccodes`
   missing; CP-16's identity bound to v21-r3; CP-16's production verification ×5; `marimo` missing. No CP-24 test
   was skipped.
7. The generators, the export and the base tree, each `PYTHONPATH=src $PY -m …`. **All exit 0**:
   - `cp24.packet --check` → `draft_registry_identical_to_committed: true`;
   - `cp24.claims --check` → both files identical, `lint_findings: []`;
   - `cp24.report --check` → identical;
   - `cp24.basetree --check` → `unchanged: true`;
   - `cp24.basetree --check-rev 7ea9bdd7…` → 1,322 recorded files unchanged, 114 added under CP-24's paths,
     `problems: []`;
   - `cp24.export --attempt 1 --check` → "the committed draft export is current";
   - `$PY scripts/mlflow_export.py --check` → "the committed export is current".

   **Positive control:** `cp24.basetree --check-rev 7ff6a50` exits 1 and lists `AGENTS.md`, `capstone_v21.md`,
   `docs/PUBLISH_RULES.md`, `progress.md`, `scripts/cp23_ddnn.py` and the other files `main` changed. As a separate
   check, `cp24.basetree.build()` at `522d7ea` equals `reports/ddnn2/base-tree.json` byte for byte.
8. `git diff --name-status 522d7ea..7ea9bdd`: 114 entries, all `A`, all under §23.14's write paths. None
   modified or deleted.
9. Pre-registration:
   - `git merge-base --is-ancestor 62b8e51 dea6664` exits 0, and `git merge-base --is-ancestor 62b8e51 cb52fe2`
     exits 0;
   - the first commits holding `protocol.json`, `lineage.json` and `predictions.parquet` are `62b8e51`, `dea6664`
     and `cb52fe2`;
   - `protocol.json` has exactly one commit.

   In the ledger (`budget.json`, read only), the protocol commit is 08:39:57Z. Event 13, `attempt_1_first_fit`
   (08:40:05Z), records `protocol_commit 62b8e51…` and SHA-256 `2fd3c464…`. Event 14, the first `fits_start`, is at
   08:40:59Z. The S1 answer `118089a` (08:32:30Z) precedes the protocol.
10. The frozen identities at the candidate, `d637590` and `9667fb4`: every file in `implementation_sha256` (50)
    and `frozen_inputs_sha256` (25) hashed at each.
    - At `d637590` all match.
    - At the candidate exactly two differ: `scripts/cp24_ddnn2.py` and `src/cp24/budget.py`.
    - `git diff 62b8e51 HEAD` of those two files removes only the calendar gate (`calendar_stop`,
      `CALENDAR_MARGIN_SECONDS`, the refusal and the in-loop stop) and rewords a docstring and help text. No
      forecast path is touched.
11. `gapcheck.py` under the monitor (`critic3-gapcheck`). Exit 0. Fold 4's first gate day, 2025-01-25, has the
    window [2023-01-28, 2025-01-25), which overlaps the gap by 56 days. 55 are excluded. The 56th, 2023-03-13, has no
    eligible target, so it is not a training row anyway. The uncovered days with targets are exactly
    2022-09-29..2023-03-24, 174 of them.
12. The review reproduction under the monitor (`critic3-review`). Exit 0, 109 s. The command was
    `$PY -m cp24.review --out review.json --score 1 --gate 1 --trial 1:fold_4:58:4 --ensemble 1:fold_3:2022-08-26
    --replay 1:v5:fold_3:2022-07-01:2022-07-14`. Results:
    - `score`: `all_equal: true`, every one of these differences ≤ 1e-9:

      | Table | Rows | Unmatched | NaN mismatches | Max absolute difference |
      |---|---|---|---|---|
      | `metrics` | 91 | 0 | 0 | 5.7e-14 |
      | `uncertainty` | 132 | 0 | 0 | 3.6e-15 |
      | `criteria` | 105 | 0 | 0 | 7.1e-15 |

      The verdict and the first unmet condition (`None`) equal the committed ones. All 11 readings are equal, and
      the guard report equals `guards.json`.
    - `gate`: `conditions_and_folds_equal: true`, passed.
    - `trial`: pinball 4.275926699402708, MAE 15.977520186913953 and 643 epochs, each equal to the ledger. This is
      fold 4, a non-ensemble trial, with 174 uncovered days excluded.
    - `ensemble`: D2's central and quantiles are bitwise equal, and all eight members' weight hashes equal
      `fits.parquet` (24 hours, the 2022 peak).
    - `replay`: v5 through the H layer from the admission freeze, 336 rows, `bitwise_equal: true`.
13. `indep_score.py` under the monitor (`critic3-independent-decision`). Exit 0; output in
    `independent-decision.json`. It is this review's own code for:
    - the new policies' losses from `predictions.parquet` and the snapshot's prices;
    - the equal-fold scores;
    - CP-20's index generator, whose fingerprint equals `e1df9a68…`;
    - the decision bootstrap, the per-fold daily intervals, the six §8 diagnostics and the five conditions.

    It rescores **no** saved reference: B0–B3 and HGL enter only through CP-21's committed `metrics.csv`,
    `diagnostics.csv` daily and peak rows, and `replicate-scores.parquet`. Results:
    - the snapshot's truth equals the committed `y_true` exactly;
    - the per-fold scores and S equal the committed ones (largest difference 0.0);
    - the decision intervals match within 1.7e-16 and the per-fold v5 − v4 intervals within 1.5e-14;
    - HGL's replicate scores rebuilt from CP-21's daily rows equal CP-21's committed replicate scores (0.0);
    - conditions 1–5 are all met, with no first unmet condition, equal to the committed decision;
    - §8 is all six met for v5, v3+D2 and D2;
    - v5 − v4 per fold has every 95% interval below zero in both MAE and WIS.
14. `blind_check.py` under the monitor (`critic3-blind-refit`, 48 review fits). Exit 0. It truncates the inputs
    after D, replaces D's own prices by `500 − price`, overwrites the weather after D, and refits the frozen eight
    members:

    | Origin | Members | D2 vector | Positive: D−1 prices +150 moves the forecast by |
    |---|---|---|---|
    | fold_3 2022-08-30, evaluation | equal `fits.parquet` | bitwise equal to `predictions.parquet` and `lineage.json` | 230.6 EUR/MWh |
    | fold_5 2026-03-29, evaluation, a 23-hour DST day | equal `fits.parquet` | bitwise equal to `predictions.parquet` and `lineage.json` | 79.2 EUR/MWh |
    | fold_4 2025-04-20, warm-up | equal `fits.parquet` | central SHA-256 equal to `lineage.json` | 105.2 EUR/MWh |
15. `$PY -m pytest -q -p no:cacheprovider -rA tests/cp24/torch_reference_checks.py` under the monitor
    (`critic3-torch-reference`). **Exit 0: 32 passed, 0 skipped.** The module imports `torch` at top level, with
    no skip logic.
16. `$PY -m cp24.landsim --main 7ff6a50… --candidate 7ea9bdd… --out critic-3/landsim` under the monitor. **Exit 0,
    `green: true`.**
    - Preconditions all true: 114 candidate additions, all under CP-24's paths; `main` changed 31 files, none
      under them.
    - The steps: payload 0; suite 0 (1478 passed, 13 skipped, no CP-24 skip); CQR 0; `verify_release` 0
      ("PASS"); WASM 0 (15 passed); publication guard 0.
    - Scratch tree `7f9e05c7…`.
17. The same with `--later-edits` (`critic-3/landsim-edits`). Exit 1: 3 failed, 1474 passed, 14 skipped. The
    failures were `tests/cp23/test_reference_record.py::…nothing_skipped`,
    `tests/cp23/test_saved_evidence.py::test_byte_exact_storage_of_every_manifested_file` and
    `tests/cp24/test_reference_record.py::…nothing_skipped`. Every other step was 0. The judgement is under
    condition 1 below.
18. A read of the committed `replicates.parquet`: the percentiles of the stored equal-fold `ratio` draws, with no
    bootstrap pass. The 95% percentiles equal every committed `ratio_ci_*` exactly. The 97.5% (1.25%/98.75%)
    ratio intervals, which the candidate does not report, are:

    | Contrast | MAE ratio, 97.5% interval | WIS ratio, 97.5% interval |
    |---|---|---|
    | v5 − v4 | [−3.04%, −1.68%] | [−2.86%, −1.62%] |
    | D2 − v4 | [−14.63%, −6.78%] | [−19.31%, −11.62%] |
    | v5 − v3 | [−8.59%, −6.30%] | [−8.08%, −5.92%] |
    | (v3+D2) − v4 | [−4.82%, −2.24%] | [−4.66%, −2.15%] |

    The full table is in `ratio-97.5-from-stored-draws.txt`.
19. `git show main:scripts/bar.py | python3 -I - check <this verdict> --source capstone_v21.md@7ea9bdd73fb7df50991083e674c4dad24335aaf0`,
    run after writing. Its result is recorded at the end of this file.
20. Read-only inspection of the ledger with `$PY scripts/cp24_ddnn2.py status` and Python reads of
    `budget.json`: the jobs, events, pauses and peaks, before and after the review. The figures are in the item 15
    and item 18 rows.
21. `search_check.py` and an inline re-derivation from the per-task records in
    `.local/artifacts/cp-24/rounds/round-1/search/`, with no fits. For every fold they reproduce:
    - the 28-day batch tiling backward from D0 − 57 (B = 3, 7, 11, 11, 11);
    - the stage-A pooled pinball and the survivors (ceil(128/3) = 43; all 128 in fold 1);
    - the all-batch ranking and the four distinct ensemble configurations.

    The ensembles equal `ensembles.json` and `protocol.json`, with eight distinct seeds each. Every batch ends
    before D0 − 56, and there are 3,464 records.

## Evidence actually inspected

- **Plan and briefs.** `capstone_v21.md` §23.1–§23.15 at the candidate, plus §8, §14.6, §17.5, §18.2–18.3, §21.3,
  §21.5 and §20.5. The issued brief, the continuation brief and `work-availability-2026-10-10.md`. The steering
  pair `steering/s1-round-1-report.md` and `s1-round-1-answer.md`.
- **Records.** `reports/ddnn2/`: `report.md`, `reproduce.md`, `defects-and-repairs.md`, `licence-admission.md`,
  `resource-admission.md`, `v4-parity.json`, `preflight/input-verification.json`, `preflight/weather-regeneration.json`,
  `base-tree.json`, `resources.json`, `mlflow-local.json`, `rounds/round-1/{gate,search-ledger,ensembles}.json`.
- **Attempt 1.** `attempt-1/`: `protocol.json`, `predictions.parquet`, `members.parquet`, `fits.parquet`,
  `lineage.json`, `metrics.csv`, `uncertainty.csv`, `criteria.csv`, `decisions.json`, `summary.json`,
  `replicates.parquet`, `replicate-scores.parquet`, `controls.json` (80 checks, all true),
  `leakage-controls.json`, `leakage-by-origin.csv`, `daily-cycle.json` (25 origins), and `diagnostics/*.csv` (all
  13).
- **Packet and claims.** `publication-packet.md` and `cp24-claims.md`.
- **Code.** `src/cp24/{leakage,landsim,basetree,execution,review,inputs,design,member,ddnn2 (header and constants),
  audit,scoring,gate (evaluation),protocol (check_protocol),controls (admission states)}.py`, `scripts/cp24_ddnn2.py`,
  every CP-24 test that binds files (`test_base_tree`, `test_saved_evidence`, `test_draft_export`,
  `test_reference_record`, `test_leakage_controls`, `test_work_availability`, `test_numpy_only`) and
  `torch_reference_checks.py`'s header.
- **Comparison tables.** CP-21's committed `metrics.csv`, `diagnostics.csv` and `replicate-scores.parquet`.
- **Ignored state, read only.** The ledger, `critic-open.json`, `start.json` and the round-1 per-task search records.
- **Topology.** `git worktree list`, `git branch -a -vv` and the primary checkout's reflog.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Starting state: anchor SHA-256 against the brief; `gauntlet.py start`; the Lead worktree on `gauntlet/cp-24`; issued brief byte for byte | **Met** | The anchor `11068e3f…` equals the brief (command 3). `start.json` (2026-10-05T03:16:55Z) records `main` = `origin/main` = `522d7ea`, clean, one worktree, no stash. The first branch commit `1cead62` (parent `522d7ea`) adds only `issued-brief.md`, `cmp`-identical to the canonical copy. The primary checkout is still on `main`, clean; its reflog shows no checkout since 2026-10-04. The Lead worktree is `.local/worktrees/cp-24/lead` on `gauntlet/cp-24`. Prior evidence is untouched (command 7: `--check-rev`). |
| 2 | Inputs: population, manifest and frozen weather with the §23.6 gap; saved-vector identities incl. CP-23's D from evidence tags; an independent HG and v4 slice; no retrieval, nothing after 2026-04-07 | **Met** | `input-verification.json`: 112 identities, CP-23's from `evidence/cp-23` blobs. That record shows 638 origins and 10,747 keys, saved-vector consistency all true, `retrieval: none` and maximum date 2026-04-07. The gap is 2022-09-29..2023-03-24 (177 days). `weather-regeneration.json` has the rebuilt design equal to the frozen one and the values bitwise equal. `v4-parity.json` holds 11 origins, bitwise for A1, B2, L-N, L-R, HG and v4, and the wrapper changed nothing. `identities()` was re-executed at the candidate inside command 12's replay. Every key is ≤ 2026-04-07 (command 13). |
| 3 | 4.6L′ | **Met** | `licence-admission.md`: PASS. The code is original (MIT), no third-party code or weights, method sources cited, the reuse of the test-only reference stated, under half an hour of the 2-hour cap. |
| 4 | Correctness under §23.7: import audit, finite-difference checks, PyTorch reference checks that cannot skip silently | **Met** | `test_numpy_only.py` audits `ddnn2.py` and `sampler.py`, with framework fixtures that fail. `member.py` imports pandas only for a type annotation; the design pipeline sits outside the rule under §18.2 item 3. `test_ddnn2_gradients.py` passed in command 6. The reference rerun gave 32 of 32 with 0 skipped (command 15). `torch` is a top-level import with no skip, and the non-collected script uses CP-23's pinned lock `b3164a37…`. The root `pyproject.toml` and `uv.lock` are unchanged (command 7). `test_reference_record.py` binds the record to the current `ddnn2.py`. |
| 5 | 4.6R′ on pre-fold data, PASS or NOT_ADMITTED | **Met** | `resource-admission.md`: PASS. Timing fits forecast only validation-batch days. It fixes 128 trials per fold per round (≥ 32), the maximal route and the review reserve, and projects both routes against §23.11, the worst case included. `protocol.json` `resource_admission` repeats it. |
| 6 | Every pre-fold round: search in a ledger; gate with v4's members on the same code path and the coverage rule; the pre-fold report; no DDNN-2 or new-policy fit at a warm-up or evaluation origin | **Met** | One round. The search re-derivation in command 21 matches. The gate recomputes equal to the committed one (command 12). Its values: G0 true; G1 12.538 ≤ 12.849; G2 0.852 ≤ 1.10; G3 0.088% < 0.1%. The windows equal §23.6's five, 280 days. The coverage rule holds (command 11; `controls.json` `weather_coverage.*`). `rounds/round-1/report.md` exists. No attempt-fit counter moved before `62b8e51`, and the leakage structure check finds no gate or batch day among the scored days. |
| 7 | Every S1 exchange and each attempt's frozen protocol committed before its warm-up or evaluation fits; stop when the route ends | **Met** | The S1 report is `031f826` and the verbatim answer `118089a` ("freeze round 1's design"), committed with time, round and attempt (none). The round's gate passed, so a freeze was allowed. The answer carries pre-fold evidence only and prescribes no implementation. The protocol `62b8e51` precedes every attempt-1 fit by ancestry and in the ledger (command 9). |
| 8 | Exactly DDNN-2, v5 and the arms; composite parity | **Met** | `ddnn2.py`'s constants and parameterisation match §23.3: the ξ, λ, γ, δ heads; 20 NLL epochs, then κ·NLL + (1−κ)·pinball over 19 levels; patience 50; maximum 1,000; cap 1.25×; median of eight members. The search space matches §23.4's table. v5 is `A1/3 + B2/3 + L-N/12 + L-R/12 + D2/6`, and v3+D2 is CP-22's form. Composite parity holds on every key (≤ 1e-9; `test_composites_and_rule.py`, `controls.json` `population.composite_parity_passed`). v5 and v3+D2 run on HG's H path (`population.v5_and_v3d2_on_h_path`; the replay in command 12). |
| 9 | Every §23.10 control and the inherited ones, each negative paired with a positive | **Met** | `controls.json`: 80 of 80. `leakage-controls.json`: 12 of 12 (636 of 636 origins bitwise with the future destroyed; 10,747 keys equal `predictions.parquet`; D−1 positive at 22 of 22; planted leak in 5 of 5 folds; search and gate fold by fold; exhaustive structure). This review's own differently-constructed blind refits reproduce at 3 origins, with paired positives (command 14). DST is covered by `test_design_dst.py`'s 17 cases (command 6). See condition 2 below. |
| 10 | All 10,747 keys for every new policy, finite and ordered; emitted p50 separate from the central | **Met** | From command 13: v5, v3+D2 and D2 each have 10,747 rows on exactly CP-15's B0 key set, finite and ordered. D2's p50 equals its central. v5's and v3+D2's p50s differ from their centrals. |
| 11 | Score every policy of every attempt; independently verify the scores, the diagnostics, coverage with width, all six §8 diagnostics per new policy | **Not met (reporting)** | Scores, coverage with width, §8 and the diagnostics all verify. The `cp24.review` recomputation equals the committed tables (command 12). This review's own code reproduces S, per-fold metrics and coverage exactly, with §8 all met for v5, v3+D2 and D2 (command 13). The spot checks agree: D2's calibration (coverage 0.484, 0.794 and 0.954) and pooled error correlations (D2~HG 0.826, D2~L 0.803). **But §23.8's metrics and uncertainty for every scored attempt require ratio intervals at 97.5% as well as 95%, and only the 95% ratio intervals are produced** (command 18). |
| 12 | `cp24-adoption` applied mechanically; each decision with its first unmet condition; every §23.8 contrast with its reading; Engineering, research and product statuses distinct | **Met for the decision, with item 11's gap in the contrast reporting** | The decision recomputes independently: all five conditions met, first unmet `None`, adopted (commands 12–13). Condition 1's 97.5% *difference* upper endpoints are −0.0091 (MAE) and −0.0084 (WIS). Condition 5 is −2.49% and −2.36% against −0.5%. Condition 4 has no fold interval above zero; every interval lies below zero. All 11 contrasts are stated with readings equal to the recomputation, and the statuses are kept distinct in `report.md`. The contrasts' ratio intervals are given at 95% only (item 11). |
| 13 | Attempt bounds | **Met** | One scored attempt, adopted, so no S2 and no attempt 2 (§23.6). `scored_attempts` = 1, `rounds_before_attempt_2` = 0. |
| 14 | §23.8's diagnostics in `reports/ddnn2/` | **Met** | All of them are under `attempt-1/diagnostics/`, in `fit-cost.json` and in `daily-cycle.json`. The cold daily cycle is 25 origins; the error correlations are pooled and by fold for D2, D, HG, A1, B2 and L; MAE by hour sits beside L, HG and HGL; the extrapolation beside CP-23's record; the peak and folds 3–4; guards by fold and by member; the search beside validation, gate and fold; member stability; the shape blend; and the PIT. |
| 15 | Store DDNN-2 vectors for 4.8; enforce and report every §23.11 cap with any raise; respect the calendar | **Met** (calendar clause superseded) | D2's vectors are in `predictions.parquet`, `members.parquet` and `fits.parquet` (5,088 member records). There are no raises. Caps after this review: DDNN-2 fits 16,395 / 40,000; v4 gate origins 280 / 280; policy-days 3,697 / 12,000; reference passes **3 / 3**; bootstrap passes 3 / 6; scored attempts 1 / 2; rounds 1 / 3 and 0 / 1; machine-hours 18.30 / 150; aggregate RSS 3.97 GiB / 10; added disk 3.23 GiB / 10; workers ≤ 4; data 0, remote writes 0, cost $0; active hours ≈ 7.2 / 50 (upper bound). The calendar sentence is superseded by `AGENTS.md` § Work availability (`main` `7ff6a50`, the Owner, 2026-10-10), as the assignment directs, and is not reinstated. |
| 16 | Durable evidence: executable reproduction, byte-exact storage, §23.12's packet and draft export, unchanged public surfaces, export set, `mlflow_export.py`, root lock; CI green; no public write | **Met, except the packet inherits item 11's gap** | Byte-exact storage: the manifest test and `git check-attr text` are unset on every report and evidence file (command 6). The generators and the export are current (command 7). The unchanged files are proved candidate-scoped (command 7) and the export set is current. CI is green in the candidate's suite and on the simulated LAND (commands 6 and 16). MLflow is `delu-generations`, local `.local/mlruns/cp24`, `network: none`, read-back equal. The only remote ref is `origin/main`. The packet's derived quantities agree with the tables (−0.0133 and −0.0119; the 97.5% upper endpoints; ratios −2.5% and −2.4%; per-fold MAE 4.8–14.4 and 45.5). Its headline (b) gives only the 95% ratio interval. The reproduction is executable at the candidate through `cp24.review` and `cp24.leakage` (see the `check_protocol` question below). |
| 17 | One fresh, independent Integration-Critic PASS on a clean detached checkout; launched with `critic-open`, `critic-brief`, `critic-close`; recompute metrics, intervals and verdict; check the gate and steering; pre-registration; reference rerun; reproduce a search trial, an ensemble fit and its emission; re-derive the packet | **Performed; the verdict is FAIL** | Every listed check was performed and passed (commands 7, 9, 12–15, 18 and 21). The FAIL rests solely on items 11, 12 and 16's ratio-interval reporting. `critic-close` is the Lead's next step. |
| 18 | Canonical packet (templates §3) with `gauntlet.py return` | **Not yet due** (the Lead's post-verdict obligation) | It cannot exist at the candidate. See "For the Lead's return" below. |

### The continuation brief's three conditions

| Condition | Verdict | Evidence |
|---|---|---|
| 1. CI stays green on `main` after the LAND; item 16's "unchanged" proof holds for the candidate; no CP-24 test binds files later authorized work may change | **Met** | `--check-rev` proves the candidate changed no base file (command 7). The default-suite base-tree test now checks only the committed record and both checkers, on fixtures with paired negatives. The simulated squash onto `7ff6a50` (v21-r12, PUBLISH_RULES 1.4) is green in every CI step (command 16). See the first note below for the edited run. |
| 2. Item 9's control evidence matches the strength of the result; any extension verification only, nothing rescored, within §23.11 | **Met** | The Lead's decision to extend was right: two origins with member 0 could not rule out leakage for a −10.67% / −15.53% member. The full-coverage negative destroys every outcome on or after D at all 636 origins with eligible hours, and is bitwise. Its paired positives move the forecast. The construction is sound: `prepare` recomputes every feature from the frame, and `p` is CP-15's static protocol. This review's own variant (command 14) truncates the frame after D and perturbs D's prices to finite values, and still reproduces bit for bit. That rules out a NaN-skipping blind spot. Verification only: `git diff --name-status d637590..7ea9bdd` adds only `leakage-controls.json` and `leakage-by-origin.csv` under `attempt-1/`. No protocol, prediction, member, fit, lineage, metric, interval, criterion or decision file changed. The cost was 5,294 control fits and 7.27 machine-hours, within the caps. |
| 3. Every interruption accounted for: Critics 1 and 2 closed or disclosed; their worktree removed; the idle gap in the effort ledger; the new Critic receives nothing from them | **Met** | `critic-open.json` n = 1 and n = 2 are closed at 2026-10-10T17:13:27Z with `verdict_sha256: null` and no-verdict dispositions. `git worktree list` shows no `critic-2`. The ledger pause 2026-10-05T14:28Z → 2026-10-10T16:54Z (122.43 h) is recorded as an `idle_gap`. `idle` refuses an interval in which any job ran. The last earlier job, `critic2-independent-score`, ended 14:19:14Z, and the next, `landsim-tip`, started 17:01:35Z on 10-10. This review received nothing from Critics 1 and 2. |

**On the edited LAND run (condition 1).** The `--later-edits` run fails three tests (command 17). All three fail on the
same edit, the one to CP-23's test-only lock `tests/cp23/torch-reference/uv.lock`. Two of them are CP-23's own
tests, already on `main`. The third is `tests/cp24/test_reference_record.py`, which binds the same lock. None of
the edits to `progress.md`, `docs/track-b/cp-0-defects.md`, `AGENTS.md`, `capstone_v21.md`, `README.md`,
`docs/index.html` or `scripts/mlflow_export.py` fails any CP-24 test. `test_draft_export` skips with its reason, as
designed. I accept the Lead's disposition, for three reasons:

- the lock is a file §23.14 and the issued brief say never changes, and CP-23's artifact manifest binds it;
- §23.7 requires the collected record test to be tied to that lock;
- the test is in attempt 1's frozen `implementation_sha256`.

So a later change to the lock already turns `main` red through CP-23 and requires an Owner amendment. That
amendment must add `tests/cp24/test_reference_record.py` to its exemption set. `defects-and-repairs.md` item 12
says so. CP-24 adds no new exposure.

**On `check_protocol(root, 1)` refusing at the candidate (the assignment's question).** The refusal is sound and
designed. The Owner-authorized maintenance commit `9667fb4`, which the continuation brief requires the final
candidate to retain, changed two files in `implementation_sha256`. The guard detects exactly that (command 10). The
change touches no forecast path, as the diff in command 10 shows. Every attempt-1 fit, the scoring and the controls
ran before it, and attempt 1 is adopted, so no attempt-1 entry point needs to run again. `cp24.leakage.frozen_guard`
is a faithful narrowing. It applies `check_protocol`'s conditions and admits only those two files, and only if their
live bytes equal `9667fb4`'s blobs and their blobs at the protocol commit equal the frozen hashes. The 636-origin
bitwise reproduction is the direct proof that the forecast path is the frozen one. All original entry points remain
runnable at `d637590`, where every frozen file matches (command 10). The reproduction path at the candidate,
`cp24.review`, works (command 12). One gap: `reproduce.md` does not say that the route's attempt-1 commands refuse
at the final candidate by design, nor where they run. See the observations.

## Observations (not blocking on their own)

1. **The leakage job ran from an uncommitted module.**
   - `leakage-a1` started at 17:12:32Z. `src/cp24/leakage.py` was committed in `1dd919a` at 17:12:47Z, and
     `leakage-controls.json` records `frozen_guard.head = 3580bf9`.
   - The module has not changed since, and the record's structure matches the committed code and test.
   - Command 14 independently confirms the central claim. The return should disclose the 15-second ordering.
2. **The review's `--gate` recomputation charges `policy_days_gate`.** It charged 840 more (now 1,680) rather than a
   review counter, so the gate sub-counter no longer equals one gate pass. The return should explain it.
3. **`resources.json` and `report.md` predate the Lead's post-candidate jobs.** Their resource table ("at the
   candidate, before the review") does not include the three concurrent `landsim-*` jobs run after `7ea9bdd`. Those
   jobs raised the peak aggregate RSS to 3.97 GiB and the added disk to 2.08 GiB, and this review raised the added
   disk to 3.23 GiB. The return must give the final totals.
4. **`reproduce.md` should state the attempt-1 refusal.** Its attempt-1 route commands refuse at the final candidate
   (`check_protocol`, after `9667fb4`). It should say so, point to `d637590` for the original entry points, and name
   `cp24.review` and `cp24.leakage` as the reproduction path at the candidate. Today only
   `defects-and-repairs.md` item 10 explains it.
5. **No single §14.6 E1–E4 record.** §23.11 asks the Lead to complete E1–E4 with the Lead and Critic sessions named.
   E1–E2 are in `preflight/` and the protocol, and E3 in the monitor and ledger and in 4.6R′. E4's session
   identities should be stated in the return.
6. **Claim C441's heading overstates.** "Leakage ruled out at every origin" should stay scoped to what was tested:
   no use of any outcome dated on or after the delivery day. The input vintages (A65 load forecasts, CP-20's GFS
   availability rule) are inherited from CP-15 and CP-20 and were not re-reviewed here beyond CP-24's identity
   checks.
7. **The Owner's maintenance validation ran outside the ledger.** It ran 20 tests outside the CP-24 monitor; it is
   disclosed in the maintenance record and is negligible. The continuation Lead's two unmonitored checks are
   disclosed in `defects-and-repairs.md` item 14.
8. **Reference passes are now at their cap (3 of 3).** One was the Lead's, one Critic 2's aborted review and one
   this review's. The cap is not raisable (§23.6). **A further Integration review cannot run `cp24.review --score`.**
   That would reserve a fourth pass. It must recompute without rescoring the saved references, for example from
   CP-21's committed reference tables as command 13 does, and percentiles of stored draws are not a pass.

## For the Lead's return (item 18)

The return must carry:

- **Both terminal SHAs and the verdict-only delta.**
- **This review's charges:** 57 review fits; 14 review policy-days, plus 840 charged to `policy_days_gate`; 1
  reference pass; 1 bootstrap pass; 0.38 charged machine-hours over the jobs `critic3-*`.
- **Branch, worktree and stash accounting:**
  - `gauntlet/cp-24` and its `lead` worktree;
  - the `critic-3` worktree, which `critic-close` removes;
  - no stash;
  - another session's branch `codex/final-product-price-lock-plan` at `7ff6a50`, with its worktree
    `.local/worktrees/final-product-price-lock-plan`. It is not CP-24's and should be declared as such or escalated.
- **Disposable scratch:** this review's scratch trees under `.local/artifacts/cp-24/critic-3/landsim{,-edits}/tree`.

## On FAIL only

- **Single largest meaningful gap:** §23.8 requires ratio intervals for every scored attempt "at 97.5%, the decision
  level, and at 95% for comparison with CP-21 to CP-23". These are §17.5's `R_b = S_policy,b / S_comparator,b − 1`,
  the publication form of each contrast. The candidate reports them only at 95%, in `uncertainty.csv`,
  `decisions.json`, `report.md`, `cp24-claims.md` and the packet's headline (b). So the adopted result's share of
  v4's score is presented only at a level below the one the decision was taken at. Every other item verifies, and
  the decision itself is unaffected.
- **Exact next acceptance test:** a new final candidate that differs from `7ea9bdd73fb7df50991083e674c4dad24335aaf0`
  only under CP-24's write paths, in which:
  1. **The intervals are reported.** For each of attempt 1's §23.8 contrasts and metrics, the 97.5% ratio interval
     (the 1.25% and 98.75% percentiles of the committed equal-fold `ratio` draws in
     `reports/ddnn2/attempt-1/replicates.parquet`) is reported beside the 95% one. It appears in the report's
     contrast table and, for v5 − v4, in the packet's headline quantity (b) and the claim map. Undefined rows, such
     as D2 − L in WIS, stay marked undefined. The expected values are those of command 18; for v5 − v4: MAE
     [−3.04%, −1.68%], WIS [−2.86%, −1.62%].
  2. **They are derived only from the committed stored draws:** no rescoring, no bootstrap or reference pass, and no
     change to any file in attempt 1's `implementation_sha256` or `frozen_inputs_sha256`. Nothing changes in
     `protocol.json`, `predictions.parquet`, `members.parquet`, `fits.parquet`, `lineage.json`, `metrics.csv`,
     `uncertainty.csv`, `criteria.csv`, `decisions.json` or `replicates.parquet`.
  3. **Every check still passes:**
     - `python -m cp24.packet --check`, `cp24.claims --check` and `cp24.report --check`;
     - `cp24.basetree --check-rev <new candidate>`;
     - the default suite;
     - `cp24.landsim` against `main`.
  4. **`reproduce.md` states the route's status at the candidate:** the attempt-1 commands refuse there by design
     after `9667fb4`, they run at `d637590`, and `cp24.review` and `cp24.leakage` are the reproduction path at the
     candidate.

  A fresh Integration Critic confirms this by recomputing those percentiles from the committed draws. Under
  observation 8, its recomputation of the scores must not spend a reference pass.

## Command 19 result

`git show main:scripts/bar.py | python3 -I - check integration.md --source capstone_v21.md@7ea9bdd73fb7df50991083e674c4dad24335aaf0` → exit 0: `ok: lines 9–85 (4590 bytes) appear in capstone_v21.md@7ea9bdd73fb7`. Final `git -C /Users/djourno/Downloads/PJM/.local/worktrees/cp-24/critic-3 status --porcelain` before closing this file: empty; `HEAD` `7ea9bdd73fb7df50991083e674c4dad24335aaf0`.
