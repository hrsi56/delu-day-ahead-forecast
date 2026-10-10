# CP-24 — defects and repairs

Every defect found during CP-24 and its repair, in order. No repair changed a frozen element after any outcome it
could depend on; none is outcome-driven. The Owner's work-availability maintenance (item 10) changed two files in
attempt 1's frozen implementation list. It touched only their calendar gate, never a forecast path.

1. **Round 1's search ledger write (2026-10-05, 07:42 IDT).** `job_search` completed all 3,464 trial-batch fits
   (3,462 succeeded; 2 failed with a nonfinite training loss at epoch 21 and rank last, as the procedure says), then
   failed while writing `rounds/round-1/search-ledger.json`: a trial outside the halving survivors, or with a failed
   fit, has an infinite pooled metric, and the ledger writer refuses non-JSON floats. `src/cp24/search.py` is part of
   the search identity that binds every task record, so it was left byte-identical. `src/cp24/searchledger.py`
   (job `search-ledger`) loads every expected record with that identity, recomputes the halving survivors with the
   same rule, checks that the stage-B records are exactly the survivors on the remaining batches, and applies
   `job_search`'s post-processing unchanged, writing an undefined (infinite) metric as null. No fit was repeated.
   The ensembles were written before any gate fit and are committed before the gate runs.
2. **The one search fit lost at the worker change (07:24 IDT).** The search was started on one worker while v4's
   gate pass held three, then stopped by its monitor (SIGTERM) when that pass finished and restarted on four. The fit
   in flight at the stop had been charged and was refitted on restart: `ddnn2_fits_search` = 3,465 for 3,464 records.
3. **A session stopped by an account usage limit (07:45–11:02 IDT).** No job ran in the gap (the search's last job
   ended at 07:42:51 IDT). The gap is recorded in the ledger as an idle pause (`scripts/cp24_ddnn2.py idle`, which
   refuses an interval in which any job ran), so it is excluded from active hours.
4. **The real-data DST test's comparison of a missing hour (2026-10-05, 11:38 IDT, before attempt 1's freeze).**
   `tests/cp24/test_design_dst.py`, run on the frozen snapshot for the first time, failed on 2023-10-29 and
   2024-10-27: the snapshot lacks the 00:00 load forecast on both days (neither day has a feature-valid or eligible
   hour), the day table correctly keeps that hour missing, and the test compared NaN with NaN by `np.isclose`
   without `equal_nan`. The test now passes `equal_nan=True`; the design code did not change. All 17 cases pass.
5. **A second session stopped by the usage limit (12:35–16:02 IDT).** Attempt 1's evaluation fits had finished at
   12:32 IDT (448 origins, none failed, monitor exit 0). On resuming, every one of the 636 warm-up and evaluation cache
   entries was verified read-only (identity, content hash, keys, finite ordered quantiles, eight members; no fit), and
   the ledger's 10,813 charged fits match the records (5,725 before the attempt, 1,504 warm-up, 3,584 evaluation), so no
   work was lost. The gap is recorded as an idle pause, like item 3.
6. **The 97.5% interval test's levels (after scoring, 2026-10-05 16:42 IDT).** `tests/cp24/test_saved_evidence.py`
   compared the committed 97.5% endpoints with `np.quantile` at the literal levels 0.0125 and 0.9875. The frozen
   scoring code computes them as (1 − 0.975)/2 and its complement, which is 0.012500000000000011 in floating point,
   so 52 of the 132 endpoints differed in the last bits (largest 3.6e-15). The test now rederives the endpoints at
   the scoring code's levels exactly (132 of 132) and checks the literal levels within 1e-12. No frozen element,
   score or decision changed; condition 1's upper endpoints are −0.0091 and −0.0084.
7. **The draft registry's `--check` (after scoring, 16:42 IDT).** `python -m cp24.packet --check` compared the
   stored JSON with the in-memory registry, whose round and attempt keys are integers that JSON stores as strings,
   so it reported a difference for an identical file. It now compares after a JSON round trip; the registry did
   not change. Items 6 and 7 change files that attempt 1's protocol lists under `recorded_not_enforced_sha256`;
   their hashes at the freeze are recorded there.
8. **Byte-exact storage attributes (found by the Lead after the first candidate, 2026-10-05 17:00 IDT).**
   - **The gap.** CP-21 to CP-23 store their report and evidence directories with `* -text`, so no checkout
     normalises line endings. CP-24 relied only on the manifest's SHA-256 check, which passed on this machine
     and in the CI-equivalent run.
   - **The repair.** `reports/ddnn2/.gitattributes` and `docs/track-b/evidence/cp-24/.gitattributes` now carry
     `* -text`. Both are bound in the manifest. `tests/cp24/test_saved_evidence.py` checks them, checks that
     `git check-attr text` is unset for every manifested report and evidence file, and checks the issued brief
     against the hash in the protocol. `src/cp24/finalise.py` adds the evidence attribute file to its manifest
     paths. No committed blob changed, because every file was already stored with LF and no conversion.
   - **The review.** The first Integration review (`critic-1`) had been opened on the superseded candidate
     `5fd4e3ae360855e45f504944dd21d570e2026490`. It was stopped before it ran any monitored job or wrote a
     verdict. The corrected candidate receives its own fresh review.
9. **The third usage-limit stop and the two unfinished reviews (2026-10-05, about 14:22–14:28Z).**
   - **What stopped.** Critic 2, opened at 14:06Z on `d637590`, was stopped by the account's usage limit at about
     14:22Z and wrote no verdict. The Lead stopped at about 14:28Z while it waited. No job ran after 14:19:15Z.
   - **The idle gap,** 2026-10-05 14:28Z to 2026-10-10 16:54Z, 122.43 hours, is recorded in the ledger as an idle
     pause (`scripts/cp24_ddnn2.py idle`), like items 3 and 5. The continuation Lead started at 16:54Z.
   - **The two open Critic records** in `.local/artifacts/cp-24/critic-open.json` are closed with
     `verdict_sha256: null` and a no-verdict disposition. They are n = 1 at `5fd4e3a` (item 8) and n = 2 at
     `d637590`.
   - **Critic 2's leftovers.** Its clean detached worktree was removed under the continuation brief's
     authorization. Its partial output (8 files, no verdict) stays unread under `.local/artifacts/cp-24/critic-2/`.
     The new review received nothing from either Critic.
10. **The Owner's work-availability maintenance (2026-10-10, `9667fb4`).**
    - **What changed.** The commit removed the calendar gate from `scripts/cp24_ddnn2.py` and
      `src/cp24/budget.py`. It also changed the report text, the manifest paths and the tests, and packaged the
      continuation brief byte for byte. The continuation's first commit therefore had nothing to copy;
      `cmp` against `.local/artifacts/cp-24/continuation-brief.md` shows them equal, SHA-256 `5960b908…`.
    - **The consequence.** Both scripts are in attempt 1's `implementation_sha256`, so `check_protocol(root, 1)`
      now refuses at every later commit, as designed: "implementation changed since attempt 1's freeze:
      scripts/cp24_ddnn2.py".
    - **Why it changes no frozen element.** Every attempt-1 fit, the scoring and the controls ran before the
      maintenance. Its diff touches only the calendar check, never a forecast path. The continuation runs no
      entry point that calls `check_protocol`.
    - **How the continuation guards the frozen code.** Its leakage controls use `cp24.leakage.frozen_guard`,
      which applies `check_protocol`'s conditions with this one recorded exception. Each of the two files must
      equal its blob at `9667fb4`, and its blob at the protocol commit must equal the frozen hash. Their
      bit-for-bit reproduction of every committed D2 vector (item 13) shows the forecast path is the frozen one.
11. **The base-tree test bound living files (found by the Orchestrator; repaired by the continuation).**
    - **The defect.** `tests/cp24/test_base_tree.py` hashed all 1,322 files tracked at `522d7ea` in the default
      suite, among them `progress.md`, `capstone_v21.md`, `AGENTS.md`, `README.md` and `docs/index.html`.
      Authorized work on `main` changes those files, and the closure records after the LAND would too.
    - **The evidence.** A simulated LAND of `9667fb4` onto today's `main` (`7ff6a50`) already failed it:
      1 failed, 1474 passed, 13 skipped. That squash tree was built in a fresh one-commit repository and run with
      CI's steps.
    - **The repair.** "Unchanged" is a property of the candidate commit, so it is now proved
      candidate-scoped by `python -m cp24.basetree --check-rev <candidate>`. That Git-object check requires every
      recorded file to be byte-identical and every other entry to be a file under CP-24's write paths. The Lead runs
      it before the review, and the Critic reruns it. `--check` keeps the in-checkout form. `build()` is refactored
      and rebuilds `base-tree.json` byte for byte.
    - **The test now.** The default-suite test checks only the committed record and both checkers, on fixtures,
      with paired positives and negatives.
    - **The candidate's LAND.** `cp24.landsim` builds the squash tree read-only and runs CI's steps. It is green
      on `main` as it stands, and again after simulated later edits to the living files (see the return).
12. **The other CP-24 tests, audited for the same property.**
    - **`test_draft_export.py`.** Its live hash of CP-23's test-only lock is removed; the candidate-scoped proof
      covers that lock. The fresh-build comparison of the draft export runs while `scripts/mlflow_export.py` holds
      its base bytes, and otherwise skips with the reason. The manifest still binds the draft byte for byte.
    - **`test_reference_record.py`.** It is part of attempt 1's frozen implementation, and it still asserts
      `torch_lock_sha256 == sha(tests/cp23/torch-reference/uv.lock)`.
      - Why unchanged: editing it would change a frozen element (§23.6).
      - Why it adds no exposure: CP-23's manifest test on `main` binds the same file. A later change to that lock
        must already amend CP-23's test, and the same `AMENDED_BY_…` pattern the Owner used for CP-21 and CP-23 on
        2026-10-10 then applies here.
    - **Tests that bind only CP-24's own files or fixtures:** `test_saved_evidence.py`, `test_leakage_controls.py`,
      `test_work_availability.py`, `test_guards_by_fold.py`, `test_composites_and_rule.py`,
      `test_search_procedure.py`, `test_numpy_only.py` and `test_ddnn2_gradients.py`.
    - **`test_design_dst.py`.** It reads the frozen snapshot through CP-21's loader, a behavioural dependency every
      earlier checkpoint's tests share. It pins no hash.
13. **Item 9's control evidence, extended (the continuation's decision).**
    - **The decision.** The committed controls (`controls.json`, 80 of 80) do not on their own support item 9 for a
      result this strong. D2 alone is −10.67% S_MAE and −15.53% S_WIS against v4. The controls prove the masks at
      two origins, with member 0 and one weather member, and the search and gate negatives for one fold each. A
      leak confined to another input group of the 20 frozen configurations, another fold or another origin would
      pass them.
    - **The extension** is `cp24.leakage`, job `leakage-a1`. It is verification only: no frozen element changed,
      no forecast was produced or replaced, and nothing was rescored. Its refits are charged as control fits.
    - **Results:**
      - at all 636 warm-up and evaluation origins, the frozen eight-member ensemble, refitted with every outcome on
        or after the delivery day destroyed, reproduces the committed D2 vectors bit for bit:
        636 of 636, every member at its recorded weights;
      - 10,747 evaluation keys equal `predictions.parquet`;
      - a D−1 evening price mutation moves the ensemble at 22 of 22 stratified origins, with the smallest
        move 31.28 EUR/MWh;
      - a planted one-day leak is detected in 5 of 5 folds;
      - the search and gate negatives and positives hold fold by fold in all 5 folds;
      - the structure is clean: 5,088 member windows, 3,464 search batches and the 280 gate days.
    - **Cost:** 5,294 control fits, the 4-origin smoke included, and 7.27 charged machine-hours (the smoke 0.08,
      the full job 7.19).
14. **Unmonitored checks.**
    - **A dry check before the leakage smoke.** It ran `cp24.leakage.tasks`, `structure` and `frozen_guard` once,
      outside the monitor, for about one minute in one process. It made no fit and charged nothing.
    - **A function check of `cp24.landsim`.** It ran `preconditions` and `materialise` once, outside the monitor:
      `git archive`, an untar and a scratch-repository commit, in about 8 seconds, with no test run. The tree it
      built (`3e19dd1`) equals the monitored simulation's squash tree. The scratch tree was deleted.
15. **The third Integration review returned FAIL: the 97.5% ratio intervals were missing (2026-10-10).**
    - **The review.** Critic 3 (record n = 3) reviewed candidate `7ea9bdd73fb7df50991083e674c4dad24335aaf0`, opened at
      19:08:13Z and closed at 19:45:05Z. Its verdict is preserved byte for byte as
      `docs/track-b/evidence/cp-24/review/critic-3-integration-FAIL.md`, SHA-256 `eaf3ada6…de01e8`.
    - **What reproduced.** Every other item: the scores, the decision, the gate, a search trial, an ensemble fit,
      a replay, pre-registration, the reference checks, the leakage extension, the landing safety and the accounting.
    - **The gap.** §23.8 asks for ratio intervals "at 97.5%, the decision level, and at 95%". Attempt 1's frozen
      scoring stored the 95% ratio interval and the 2,000 equal-fold ratio draws, but computed 97.5% intervals only
      for the score differences.
    - **The repair** is `cp24.ratios`. It writes `attempt-1/ratio-intervals.csv` from the committed draws in
      `replicates.parquet`, with no rescoring and no bootstrap or reference pass.
      - Its 95% interval equals `uncertainty.csv`'s exactly. Its 97.5% interval uses the scoring code's decision
        levels.
      - For v5 − v4: S_MAE −2.49% [95% −2.96%, −1.79%; 97.5% −3.04%, −1.68%]; S_WIS −2.36% [95% −2.78%, −1.71%;
        97.5% −2.86%, −1.62%]. D2 − L in WIS stays undefined.
      - The report's contrast table, the claim map (C420 and every contrast claim, source RI24) and the packet's
        headline (b) now carry both levels. `tests/cp24/test_ratio_intervals.py` re-derives the table.
      - No file of attempt 1's protocol, predictions, members, fits, lineage, metrics, uncertainty, criteria,
        decisions or replicates changed.
    - **The verdict's other observations, each addressed:**
      - The leakage job `leakage-a1` started at 17:12:32Z, 15 seconds before `src/cp24/leakage.py` was committed in
        `1dd919a` at 17:12:47Z. That is why its `frozen_guard.head` reads `3580bf9`. The module has not changed since.
      - The review's `cp24.review --gate` recomputation charged its 840 policy-days to `policy_days_gate`, which now
        reads 1,680, and not to a review counter. The total `policy_days` (3,697 of 12,000) is right.
      - Reference passes are at their cap, 3 of 3: the Lead's scoring, Critic 2's aborted review and Critic 3's
        review. Bootstrap passes stand at 3 of 6. A further review must not run `cp24.review --score`.
      - `reproduce.md` now states that the attempt-1 entry points refuse at the candidate, that they run at
        `d637590`, and what reproduces at the candidate.
      - Claim C441 is scoped to what was tested: no use of any outcome dated on or after the delivery day. The
        inherited input vintages are named as not re-tested.
      - `resources.json` is the ledger at the candidate, before the review. The final totals are in
        `docs/track-b/evidence/cp-24/resource-final.json` and the return. The §14.6 E4 session identities are in the
        return.
