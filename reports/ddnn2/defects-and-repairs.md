# CP-24 — defects and repairs

Every defect found during CP-24 and its repair, in order. No repair changed a frozen element after any outcome it
could depend on; none is outcome-driven.

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
