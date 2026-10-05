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
