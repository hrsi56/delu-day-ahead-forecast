# CP-21 defects, repairs and invalidated outputs (§17.10 item 10)

Every defect found during CP-21, what it affected, and how it was repaired. Failed and repeated
jobs stay charged in the cumulative ledger (`resources.json`, `jobs_by_name`). **No committed
research output was invalidated**, no frozen forecast-path file changed after the pre-run freeze
(the protocol's implementation hashes still hold), and no outcome informed any repair.

| # | Found | Defect | Effect | Repair | Charged |
|---|---|---|---|---|---|
| D1 | Pre-run, job `verify-weather` (first run) | The regenerated-weather comparison used `Series.equals`, which also compares the timestamp storage unit (a Parquet round trip stores microseconds). Values, statuses and the design hash were already equal. | A false mismatch; the job exited 1 | Compare instants (`as_unit('ns')`); the rerun passed: keys, values and statuses bit for bit, design SHA-256 `f5a9c6ed…` | Both runs |
| D2 | Pre-run, job `benchmark` (first run) | The timing record's per-configuration table had tuple keys, which JSON cannot hold | 37 accuracy-blind timing fits ran; the record was not written | String keys; the rerun wrote `preflight/benchmark.json` | Both runs (74 fits) |
| D3 | Pre-run, jobs `benchmark` and `determinism` (first run) | Full model strings were compared across thread counts; LightGBM records `[num_threads: N]` in the string, so identical trees looked different. `preflight/benchmark.json`'s `thread_determinism` field (`identical: false`) is that superseded full-string comparison; its forecasts were already equal. | The first comparison was inconclusive | A tree hash (the model string through its end-of-trees marker); `preflight/thread-determinism.json` reruns 24 real-data cases: identical trees and bitwise-identical forecasts at 1 and 4 threads, and repeatable at 4 | Both runs |
| D4 | Before the first scoring pass, by the Lead's code review | The frozen `cp21.scoring.adoption` returns criteria records that can hold undefined limits (NaN); the strict JSON writer refuses NaN, so the scoring job would have failed after charging its reference and bootstrap passes | None: found before any scoring | The unfrozen writer `cp21/evaluate.py` maps undefined values to null (`clean`); a synthetic end-to-end test covers the path | None |
| D5 | Before the first controls run, by review | The key-alignment control compared int64 timestamps across storage units (CP-20's Parquet stores milliseconds) | None: found before the run | Compare instants | None |
| D6 | Before the first daily-cycle run, by review | The parent's data load overlapped the four-process pool, briefly five computing processes against the four-worker limit | None: found before the run | The parent loads first, then the pool starts | None |

**Operational note.** The Lead session was stopped by a usage limit from 2026-09-29 19:26 to
22:11 IDT with no job running; the gap is recorded as an effort pause in the ledger and excluded
from active hours.
