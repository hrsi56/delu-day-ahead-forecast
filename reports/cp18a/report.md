# CP-18a: the daily pipeline around the frozen A1, on development data

CP-18's preparation, part 1. The pipeline, its states, the runner workflow, the local fallback, the live-input payload
builder and the security items, all built and rehearsed on development days through 2026-09-06 only. Nothing under
`src/cp17/` or `src/cp17c/` changed: the frozen package is called, never edited, and `refreeze verify` on CP-17c's
manifest prints `verified` at the candidate.

<!-- RESULTS -->

## 1. One run of the pipeline (`src/cp18/`)

| Step | Where | Rule |
|---|---|---|
| The plan | `cp18.plan` | The current target day is the latest delivery day whose cutoff (D−1 11:00 Europe/Berlin, `cp25.guard.issue_time`) has passed. Decision 23's catch-up: the open days of the three-day lookback, oldest first, then the target day, at most four. A day older than the lookback is never issued. |
| The red line | `cp18.plan.admit` | Every planned day passes `cp25.guard.admit_delivery_day`; a plan holding any day after 2026-09-06 is refused whole before anything is synchronized, checked or retrieved, and the refusal names no such day. Retiring it is a one-line change to `cp25.guard`, which a later brief makes. |
| The claim | `cp18.claim` | The day's issued record on `main` is the claim: fetch and check out `main` before each day, commit and push the day's records after it (fast-forward only, through `.githooks`); the loser of a push race discards its own issuance and stops. A push refused by a guard is not a lost race: nothing is published. |
| The store | `cp18.store.LiveStore` | CP-17c's store, imported, its `verify()` called first (F1's head binding included), plus run, not-issued, search and carry entries, each carrying the state unchanged; delivery days strictly increase. |
| The H2 gate | `cp17.hostcheck` | Pins, binary, machine, canary, once per run before its first issuance. Any failure issues nothing; each planned day records the failed check. |
| Each issuance | `cp17.daily.issue_day` | Once per delivery day, with its shadows registered in the store's state after D−2's release. |
| The record | `live/store/` | Each day's artifact, its record (the run's own times: run start, issuance start and end; the cutoff; the inputs' availability; the gate's machine), the state after it; every run's record, whatever it did. |

**No deadline and no "late" label (decision 22).** The cutoff is unchanged. A run may happen at any time after it. The
run's times are in the day's record beside the artifact, its lineage; the artifact's `data_refresh_utc` is the day's
latest input retrieval. A live day's input availability is judged by each input's publication time against the day's
own cutoff, never by the run time, from the archive record of each input (source, publication time and its basis,
retrieval time, SHA-256).

**The five causes of a day not issued** (`cp18.causes`), each in the record: a failed issuance by the chain; a failed H2
check; a live day's inputs that cannot be shown to precede its cutoff; no run within the lookback; S_14's state not in
place. An attempted day stays open while it is inside the lookback, and is closed with its last attempt's cause (or "no
run within the lookback") once a later day is issued or it leaves the lookback. A chain failure closes it at once.

**R7** (`cp18.r7.verify`): wherever the pipeline verifies a bundle, a raised error is a refused record. No module of the
pipeline calls `verify_bundle` except through it (a test checks).

<!-- SECTIONS -->
