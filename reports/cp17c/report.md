# CP-17c: A1 re-frozen under the `macos-26` issuing host

*Rendered from the records in this folder by `cp17c.report`; every figure is in a record.*

## The result

- **The policy identity** is `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`, in `docs/track-b/evidence/cp-17c/freeze-manifest.json`, with its freeze record beside it.
- **Every fit that ran is bit-identical to CP-17b's records:** 58 of 58 on the runner and 58 of 58 on the M3. That covers A1 at the nine parity origins on both, and all four policies on 14 shadow days on the runner and 14 on the M3.
- **The shadows' buffers** equal CP-17b's host shadow run at every origin that ran: 14 on the runner and 14 on the M3. On the runner, the final state equals CP-17b's (yes) and the early block ends in the state the late block started from (yes). On the M3, the final state equals CP-17b's (yes) and the early block ends in the state the late block started from (yes).
- **The checks before each run's first issuance (H2)** passed in every run, and one forced failure of each stopped at its own check with nothing issued.
- **The ceilings held:** the slowest fit took 231.9 s on the runner and 157.1 s on the M3, against 900 s; the largest peak was 934 MiB, against 4 GiB.
- **Native parity with CP-26:** PASS, five policies at nine origins, equal to CP-17b's record: yes.
- **Chromium and WebKit** reproduce the issuing host on the new zip: yes.
- **R7** is fixed: CP-17c lists all six malformed-day controls (yes), and CP-17b's `schema.py` raises on all six (yes).
- **GitHub minutes:** 660 as a private repository counts them, of the 1,000 allowed; 18 more job-minutes on the public repository (decision 26), which GitHub does not count.

## The machines

| | Kind | Image | CPU | Cores | Memory | OS |
|---|---|---|---|---|---|---|
| GitHub-hosted `macos-26` | GitHub-hosted runner | macos26 20261013.0424.1 | Apple M1 (Virtual) | 3 | 7.0 GiB | macOS 26.6.2 |
| the Owner's M3 | local Mac | -  | Apple M3 | 8 | 16.0 GiB | macOS 26.5.2 |

**The runner, run by run.** Each run records its machine in its checks; image version, CPU and memory are recorded, never pinned.

| Job | Run | Repository | Image | CPU | Cores | Memory |
|---|---|---|---|---|---|---|
| checks | 41031373014 | private | macos26 20261013.0424.1 | Apple M1 (Virtual) | 3 | 7.0 GiB |
| shadows | 41033064719 | private | macos26 20261021.0445.8 | Apple M1 (Virtual) | 3 | 7.0 GiB |
| resume | 41071696187 | public (decision 26) | macos26 20261013.0424.1 | Apple M1 (Virtual) | 3 | 7.0 GiB |

The scratch repository was made public at 2026-10-30 14:21 UTC by the Owner's decision 26 (`docs/track-b/evidence/cp-17c/owner-decision-26-as-relayed.md`), so its later runs ran on the public repository's runner class, against r19 §24.13's reason for a private one.

The runner's CPython was 3.13.15 (`7710b0490e6af648…`, zlib 1.2.12); its binary was retrieved from `https://nodejs.org/dist/v26.7.0/node-v26.7.0-darwin-arm64.tar.gz` (57,622,243 bytes, `7ee659a7768e641b…`), `bin/node` `a9bd0630891c2dcd…`.

## The checks before each run's first issuance (H2)

| | `refreeze verify` | The gate | Its seconds | Canary | forced: binary | forced: canary | forced: canary_quantiles | forced: machine | forced: pins |
|---|---|---|---|---|---|---|---|---|---|
| GitHub-hosted `macos-26` | verified | passed | 122 | `4e6abb02fbb0…` in 118.3 s | stopped at binary, nothing issued | stopped at canary, nothing issued | stopped at canary, nothing issued | stopped at machine, nothing issued | stopped at pins, nothing issued |
| the Owner's M3 | verified | passed | 85 | `4e6abb02fbb0…` in 80.4 s | stopped at binary, nothing issued | stopped at canary, nothing issued | stopped at canary, nothing issued | stopped at machine, nothing issued | stopped at pins, nothing issued |

Each shadow block ran its own gate too: GitHub-hosted `macos-26` checks: passed, early: passed, late: passed; the Owner's M3 checks: passed, early: passed, late: passed.

## A1's parity at the nine origins

| Origin | Bit-identical (runner) | Wall (runner) | Bit-identical (M3) | Wall (M3) | CP-17b's quantiles |
|---|---|---|---|---|---|
| A1-2025-10-26 | yes | 231.9 s | yes | 157.1 s | `93f75363ec6e…` |
| A1-2026-03-29 | yes | 118.7 s | yes | 82.4 s | `b5ca894f8f99…` |
| A1-2026-08-31 | yes | 196.7 s | yes | 81.0 s | `75d86a3b3cb9…` |
| A1-2026-09-01 | yes | 149.4 s | yes | 79.8 s | `a3a092caa60b…` |
| A1-2026-09-02 | yes | 135.7 s | yes | 72.9 s | `4fe630ec8d40…` |
| A1-2026-09-03 | yes | 143.2 s | yes | 77.2 s | `d04d0ba5a68a…` |
| A1-2026-09-04 | yes | 134.7 s | yes | 71.7 s | `8b8d025217f8…` |
| A1-2026-09-05 | yes | 168.7 s | yes | 98.7 s | `8d5cb5ea35cc…` |
| A1-2026-09-06 | yes | 127.2 s | yes | 82.0 s | `4e6abb02fbb0…` |
- GitHub-hosted `macos-26`: 2 in the checks run as parity fits, 7 from the late shadow block's A1 issuances.
- the Owner's M3: 2 in the checks run as parity fits, 7 from the late shadow block's A1 issuances.

Every payload is the parity payload of its origin, checked by its identity.

## The 14 shadow days, carried by the state store

| Day | Buffers = CP-17b (runner) | Fits bit-identical (runner) | Day (runner) | Buffers = CP-17b (M3) | Fits bit-identical (M3) | Day (M3) |
|---|---|---|---|---|---|---|
| 2026-08-24 | yes | yes | 467.3 s | yes | yes | 227.7 s |
| 2026-08-25 | yes | yes | 439.0 s | yes | yes | 246.0 s |
| 2026-08-26 | yes | yes | 417.7 s | yes | yes | 242.7 s |
| 2026-08-27 | yes | yes | 404.5 s | yes | yes | 227.2 s |
| 2026-08-28 | yes | yes | 441.8 s | yes | yes | 237.0 s |
| 2026-08-29 | yes | yes | 410.8 s | yes | yes | 265.9 s |
| 2026-08-30 | yes | yes | 395.6 s | yes | yes | 246.5 s |
| 2026-08-31 | yes | yes | 489.3 s | yes | yes | 236.1 s |
| 2026-09-01 | yes | yes | 405.2 s | yes | yes | 232.6 s |
| 2026-09-02 | yes | yes | 425.2 s | yes | yes | 248.2 s |
| 2026-09-03 | yes | yes | 430.0 s | yes | yes | 242.4 s |
| 2026-09-04 | yes | yes | 433.7 s | yes | yes | 235.8 s |
| 2026-09-05 | yes | yes | 436.1 s | yes | yes | 286.2 s |
| 2026-09-06 | yes | yes | 369.8 s | yes | yes | 234.9 s |

Each day ran in its own process: load and check the store, release D-2, check the buffers against the day's payloads, issue A1 and the three shadows one after another, register them, append to the store. On both machines the two blocks ran at once, each its days one after another, so the day figures are conservative.

## The cost (item 7)

| | Machine | n | Min | Median | Max |
|---|---|---|---|---|---|
| One issuance (A1 and three shadows, one after another), beside the other block | GitHub-hosted `macos-26` | 12 | 404.5 s | 431.8 s | 489.3 s |
| One issuance, alone (the resumed days, on the public repository's class: a first measurement there, not CP-18's) | GitHub-hosted `macos-26` | 2 | 369.8 s | 382.7 s | 395.6 s |
| Decision 23's four issuances with the canary (the gate and four consecutive days), beside the other block | GitHub-hosted `macos-26` | 6 | 1849.0 s | 1887.8 s | 1923.2 s |
| One issuance (A1 and three shadows, one after another), beside the other block | the Owner's M3 | 14 | 227.2 s | 239.7 s | 286.2 s |
| One issuance, alone | the Owner's M3 | not measured | - | - | - |
| Decision 23's four issuances with the canary (the gate and four consecutive days), beside the other block | the Owner's M3 | 8 | 1023.5 s | 1046.0 s | 1092.6 s |

A job's setup before its run (checkout, uv, CPython, the environment, the inputs, the binary and the package) took 27 s, 42 s, 49 s. The public runner class is CP-18's to time (§24.13).

## The re-freeze shown

- **The freeze-origin artifact** `4aedd5e052f0ee8d3d6aeed47c395c5cb246853e27ed129cdf514dcd9e3bf9b5` differs from CP-17b's only in `artifact_sha256`, `attempts`, `lineage.code_sha256`, `lineage.policy_identity_sha256`, `resources.peak_bytes`, `resources.wall_seconds`. Its quantiles are the canary's, `4e6abb02fbb02aa8…`, and its arrays are CP-17b's: yes.
- **Native parity** at nine origins: PASS; equal to CP-17b's record in every check, payload, quantile and ledger hash: yes.
- **Browsers** (1.63.0): chromium 153.0.8010.12 `4e6abb02fbb0…`, webkit 26.6 `4e6abb02fbb0…`.
- **R7's controls** on CP-17c's reference bundle: the valid bundle verifies under both; CP-17b's negative controls are refused alike (yes); day_not_an_object: CP-17c listed, CP-17b raised; days_not_a_list: CP-17c listed, CP-17b raised; delivery_day_absent: CP-17c listed, CP-17b raised; impossible_date: CP-17c listed, CP-17b raised; keys_absent: CP-17c listed, CP-17b raised; keys_not_a_list: CP-17c listed, CP-17b raised.
- **The freeze-origin states** on the route equal CP-17's recorded buffers: yes; and CP-17b's native shadow run's final state: yes.

## GitHub minutes

| Run | Job | Seconds | Counted |
|---|---|---|---|
| 41030551242 | macos-26 checks | 40 | 10 |
| 41030551242 | macos-26 shadow-early | 0 | 0 |
| 41030551242 | macos-26 shadow-late | 44 | 10 |
| 41031373014 | macos-26 checks | 647 | 110 |
| 41031373014 | macos-26 shadow-early | 0 | 0 |
| 41031373014 | macos-26 shadow-late | 110 | 20 |
| 41033064719 | macos-26 shadows | 3016 | 510 |
| 41040116539 | macos-26 resume | 0 | 0 |
| 41071149787 | macos-26 resume | 33 | 0 (public) |
| 41071696187 | macos-26 resume | 970 | 0 (public) |

Total: **660** counted minutes (per job that ran, rounded up to the minute; macOS x10 (the larger of the two counts per run); a job cancelled while queued never had a runner and counts nothing; a run on the public repository (decision 26, from 2026-10-30T14:21:00Z) counts nothing, its job minutes recorded); 18 job-minutes on the public repository, not counted.

