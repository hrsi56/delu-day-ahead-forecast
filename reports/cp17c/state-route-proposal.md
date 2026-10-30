# The states' route: what CP-17c defined, and the form proposed for CP-18

r19 §24.13 asks CP-17c to define how each state reaches the runner and persists between runs. Persistence across
live runs is CP-18's to build, so this proposes its form. CP-17c exercised that form across the 14 shadow days.

## What CP-17c defined, and how each state reached the runner here

Every state lives at one project-relative path, the same on the runner and on the Owner's Mac
(`cp17.runtime`). The freeze manifest records each by hash, and `refreeze verify` checks each before the first fit:
it is H2's first check, and it prints `verified` only when every one is present and equal.

| State | Path | Bound by | Here, on the runner |
|---|---|---|---|
| A1's search state S_13 | `.local/artifacts/cp-17/inputs/…/nominal/k13.json` | file hash and content digest `6090f4ab…` | committed in the private scratch repository |
| the freeze-origin states of v4, v2 and B0 | `.local/artifacts/cp-17c/state/freeze-origin-state.json` | file hash; its buffers are CP-17's | committed there; a store was initialized from it and loaded back |
| the canary's payload | `.local/artifacts/cp-17c/state/canary/A1-2026-09-06.{json,npz}` | file hashes; payload identity `63ce7f45…` | committed there; the canary fit read it |
| Pyodide's 23 files | `.local/tools/pyodide-0.28.0/` | 23 file hashes | committed there |
| the binary | `.local/tools/node-v26.7.0-official/` | the tarball's and `bin/node`'s hashes | retrieved by the run, with `SHASUMS256.txt` |
| the shadows' buffers and the issued records | a state store (`cp17c.store`) | a SHA-256 chain over every state file and issued record | carried day to day, one process per day |

## The state store, exercised

A store is one folder:
- `head.json` names the last day, its state file and its artifact;
- `ledger.jsonl` holds one entry per issued delivery day, each chained to the one before by SHA-256;
- `states/<day>.json` holds the shadow states after that day's registrations;
- `issued/<day>/` holds the day's artifact and its record.

**Its rules:**
- **Loading checks everything** (every hash and the chain). A store that does not verify is refused, so nothing
  issues.
- **One issuance per delivery day.** A day already in the ledger is refused, and no issued record is replaced.
- **Days go forward.** A gap is allowed, for decision 23's catch-up.
- **The genesis entry names where the states started.**

**On the Owner's M3 and on the runner, all 14 shadow days,** each day ran in its own process, which:
1. loaded and checked the store;
2. released D−2;
3. checked the buffers against the ones the day's payloads carry;
4. issued A1 and the three shadows;
5. registered them;
6. appended to the store.

Every day's buffers equalled CP-17b's host shadow run. On both machines the early block's last state equalled the
late block's starting state, so the two blocks join without a seam (`reports/cp17c/measurement.json`).

**Between runs, the route is carried by the repository.**
- The runner's first shadow run reached its job limit after six days in each block, and uploaded each block's store.
- Those stores, checked file by file against the job's own hashes, are committed in the scratch repository at
  `states/store-<block>/` (`cp17c.inputs --stores`).
- A `resume` run loads each one, checks its chain, and continues from its last day.
  - On the runner, run 6 resumed both blocks and issued 2026-08-30 and 2026-09-06. Each carried store was equal to
    the first run's, and the days were bit-identical to CP-17b's.
  - On the M3, a rehearsal resumed the runner's early-block store, across machines, with the same result.

## The form proposed for CP-18

1. **One store for the live product,** whose genesis is the freeze-origin states, continuing from 4.7T's last window
   day. 4.7T's own run on the Owner's Mac writes the same store, one issuance per window day.
2. **Between runs, the store is the run's data-only record.**
   - At the end of each run, the store's new files are the day's generated records: the state file, the artifact,
     the record, and the ledger and head.
   - AGENTS.md's daily-update exception already lets the pipeline commit those to `main` in the paths CP-18's brief
     names.
   - The next run checks out `main`, loads and checks the store, and continues.
   - Nothing is ever rewritten. The chain makes a replaced or dropped record visible, and the store refuses it.
3. **The search state and the freeze-origin states** reach the runner at their pinned paths, by hash.
   - **The constraint for CP-18:** they are A1's state and CP-26's. Before decision 26 they could not sit in a public
     repository before decision 25's one complete publication.
   - **Decision 26 changed that for the scratch repository:** it is public, and these files are in it. Whether the
     product repository may hold them before that publication is the Owner's to rule for CP-18.
   - Unless he rules that it may, CP-18's brief must sequence their publication with that publication, or keep them
     in a private companion repository that the runner reads. Reading another repository needs a token, which is a secret and the Owner's
     (decision 25).
   - The same holds for the canary's payload.
4. **Pyodide's 23 files** can be committed in the product repository at a path CP-18 names, as the scratch
   repository holds them. The largest is 13.3 MB, under the 50 MB limit.
   - They are copied to `.local/tools/pyodide-0.28.0/` before the first fit, or that folder points at them.
   - The binary is retrieved each run.
5. **S_14 (2027-01-06)** writes its `k14.json` on the Owner's M3 (r19 §24.13, H4). It reaches the runner by the same
   route as `k13.json`, under a new freeze.
6. **The local fallback on the Owner's Mac** reads and writes the same store. The single source of what was issued
   is the store, so the runner and the fallback never issue the same day twice.
