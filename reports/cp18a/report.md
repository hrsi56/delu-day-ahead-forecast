# CP-18a: the daily pipeline around the frozen A1, on development data

CP-18's preparation, part 1. The pipeline, its states, the runner workflow, the local fallback, the live-input payload
builder and the security items, all built and rehearsed on development days through 2026-09-06 only. Nothing under
`src/cp17/` or `src/cp17c/` changed: the frozen package is called, never edited, and `refreeze verify` on CP-17c's
manifest prints `verified` at the candidate.

## Results

| Item | Result |
|---|---|
| The pipeline (item 1) | `src/cp18/`; `tests/cp18a/` holds 293 tests, two of them `stress`. A real dry run through the H2 gate issued 2026-08-31 by A1, bit-identical to CP-17c; the local fallback then found the day claimed |
| The five causes | Each forced through the real pipeline (`python -m cp18.forced`, `reports/cp18a/forced-causes.json`): 2026-08-31 a failed H2 check; 2026-09-01 no run within the lookback; 2026-09-02 S_14's state not in place; 2026-09-03 inputs not shown to precede the cutoff; 2026-09-04 and 2026-09-05 a failed issuance by the chain |
| The claim | The push race tested with two clones of one bare origin: the loser discards its own issuance, the winner's record stands, nothing is replaced |
| The live-input builder (item 2) | 92 of 92 payload files byte-identical to the development builder's (9 parity origins, 14 shadow days); also with the native LightGBM refused and no `.local/` (`tests/cp18a/test_live_runner_env.py`, in CI); on the runner, four issuances built by it equal CP-17c's on all 16 fits |
| The store (item 3) | CP-17c's F1 head binding kept; carried across a gap and resumed bit for bit on the runner and the M3 (`reports/cp18a/carry-rehearsal.json`) |
| The workflow (item 4) | Dispatch only; binary and Pyodide by hash on every run; the guards block fake credentials by value on the runner's own commits and pushes; no fake value in any log or artifact (`reports/cp18a/credential-scan.json`) |
| The local fallback (item 5) | One command; the launchd file written, not installed |
| Timing (item 6) | One issuance 344–413 s; four with the canary 1,634 s and 1,838 s of pipeline time (28.2 and 31.7 job-minutes); every fit inside 900 s and 4 GiB (`reports/cp18a/runner-timing.json`) |
| Security (item 7) | Leak scan in the hooks and as CI's first step; environment lint and redaction plugin; three rulesets and push protection written, not applied |
| GitHub | `hrsi56/delu-pipeline-dryrun`, public, no Pages, no secret, no variable: 6 runs, 1.25 job-hours of 15, uncounted minutes (`reports/cp18a/github-ledger.json`) |
| Local | About 2 machine-hours of 10, at most 2 workers, BLAS 1 (`reports/cp18a/compute-ledger.json`) |


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

## 2. The live-input payload builder (`src/cp18/live/`)

The code that turns retrieved source data into the frozen payload kinds `cp17.daily` takes (A1, v4, v2, B0), with
each day's GFS flag set under the tier register and the Owner's rulings. 4.7T's brief and CP-18's activation brief
cite it.

- **One red line.** `cp25.guard` is the only boundary on its path. It never calls `cp17.tools.payloads`, whose own
  `BOUNDARY` constant would be a second, hidden one, nor the CP-26 loaders that bind 2026-09-06 (`H.NEW`, `spec_for`,
  `load_frame`, `guarded_weather`). It assembles the context from the landed blocks with a cutoff derived from the day
  being built, and the frame never holds a row after D. Every landed binding found on the path is listed, with how it
  is avoided, in `.local/artifacts/cp-18a/builders/builder-live-report.md` and below in §8.
- **Shown equal to the development builder: 92 of 92 files byte-identical** (`reports/cp18a/live-equality.json`):
  A1, v4, v2 and B0 at the nine parity origins and on the 14 shadow days. Each `.json` and `.npz` is identical byte for
  byte, as is `payload_sha256`. Each day was built from the committed history cut 8 days before D, plus archive days up
  to D, using CP-25's and CP-1's recorded data (never a fresh download). The ENTSO-E route gives the same bytes on two
  origins (`reports/cp18a/live/equality-entsoe-route.json`).
- **The retrieval clients, exercised only against recorded responses.**
  - **GFS** is truly recorded. On CP-25's 2026-09-05 run, all 50 messages match the record. CP-20's decoder in its
    ecCodes environment gives arrays bit-identical to the recorded run, and the converted features equal the committed
    weather bit for bit. Published 04:03:41Z, before the 09:00Z cutoff, so the flag is True
    (`reports/cp18a/live/gfs-client-2026-09-05.json`).
  - **SMARD and ENTSO-E** were never recorded raw, so their responses are rendered from the snapshot's values (pulled
    2026-09-08) in each source's documented response shape. They are labelled `rendered` in every replay entry and
    archive record, and never called recorded raw responses. The clients read them back bit-exactly on all 2,806
    development days and 67,343 hours (`reports/cp18a/live/recorded-parse.json`).
- **The availability judgement** (`cp18.live.availability`) is by publication time against D's own cutoff, never by
  the run time, and each archive record holds the input's source, publication time and its basis, retrieval time and
  SHA-256:
  - **prices** (tier 2, ruling 2): the documented schedule (P's prices by P−1 13:00 Berlin);
  - **the load forecast** (tier 3): retrieved before the cutoff, or a document time before it. Ruling 1's recorded
    exception admits the stored development history only, and is refused for any later day independently of the guard;
  - **GFS** (tier 2, ruling 4): all 20 AWS objects and indexes with `LastModified` strictly before the cutoff, and a
    valid vector. Otherwise the flag is False and D's three weather columns are missing (§15.3).
- **Through the pipeline.** A local dry run with the live builder replaying recorded responses issued 2026-08-31 with
  A1's quantiles and all three shadows bit-identical to CP-17c's (and on the runner, run 41701507248: four issuances, all 16 fits equal to CP-17c's).

## 3. The state store

- **CP-17c's fix for its first Critic's F1 is kept.** `cp18.store.LiveStore` subclasses `cp17c.store.Store` and calls
  its `verify()` first, so a repointed head still fails (`tests/cp18a/test_pipeline.py`, three repointed fields).
- **Where the states live** (decisions 26 and 27, CP-17c's landing record).
  - **The daily data-only paths** (AGENTS.md's standing exception requires the brief to name them): `live/store/`
    (`head.json`, `ledger.jsonl`, `states/<day>.json`, `issued/<day>/{artifact,record}.json`, `runs/<run_id>.json`,
    `search/k<NN>.json`) and `live/inputs/days/<day>/` (the input archive).
  - **Placed once by CP-18's activation, not daily:** A1's `k13.json`, the freeze-origin states and the canary payload,
    at `live/pinned/local/<path>`, mirroring their `.local/` runtime paths. `cp18.host.materialize` copies each into
    place by the freeze manifest's hash before the gate. Pyodide's 23 files and the binary are never committed: each run
    retrieves them from their official URLs, checked by hash. This round's dry runs use the same files at
    `reports/cp18a/dryrun/pinned/`.
- **The carry from 4.7T's last window day to the first live day.** A `carry` entry names both days, and the days
  between them are recorded as outside both, never issued (`python -m cp18 carry`).
  - **Rehearsed on development days, across two machines.** Runner run 3's store (2026-08-31 to 2026-09-03) was carried
    out of the runner, given a carry to 2026-09-05 (a gap at 2026-09-04), and committed in the scratch repository.
    Runner run 4 resumed from it, and so did the M3.
  - **Result:** on both, the carried ledger is a byte prefix of the resumed one, and every carried file is unchanged.
    2026-09-04 is outside. The resumed day's four fits and the state after it are identical on the two machines, and
    equal to CP-17c's (`reports/cp18a/carry-rehearsal.json`).
- **S_14 (H4).**
  - **Where it enters.** `k14.json`, written natively on the Owner's M3, enters through a `search` entry
    (`python -m cp18 search --k 14 --file <k14.json>`, `LiveStore.record_search`). The entry copies it to `live/store/search/k14.json`, validates it
    as search 14 (`cp26.search.validate_ensemble`) and binds its file hash and content digest in the ledger.
  - **While it is absent**, every day it serves stays open with "S_14's state not in place", and decision 23's catch-up
    then applies.

## 4. The runner workflow (`.github/workflows/daily.yml`)

- **`workflow_dispatch` only.** No `schedule:`: CP-18's activation adds it.
- **Permissions:** `{}` at the top, and `contents: write` on the one job, for the day's data-only commit at activation.
  A dry run pushes nothing to GitHub: its claim's origin is a bare repository on the runner.
- **Pinned retrievals:** actions pinned by commit SHA; uv 0.12.6 and uv's CPython 3.13.15 with the environment
  `uv.lock` pins; Node.js v26.7.0 and `SHASUMS256.txt` and Pyodide's 23 files from their official URLs, each checked by
  hash (`prepare: pinned states 4 | pyodide 23 | node a9bd0630891c2dcd | package equal` in every runner log).
- **The guards on the runner's own commits and pushes.** `core.hooksPath` is `.githooks` (the claim refuses to commit
  otherwise), so every commit runs the secret guard and the leak scan, and every push runs them with the publication
  guard. `cp18.guarddemo` shows it on the runner with fake credentials derived from the run id, never printed:
  - a staged fake `ENTSOE_API_TOKEN`, a message holding a fake `HF_TOKEN`, and a pushed commit holding a fake
    `DAGSHUB_USER_TOKEN` are blocked by value;
  - a staged environment dump is blocked by the leak scan, by its shape;
  - a data-only commit and its push pass;
  - no output line holds a value.
- **Credentials** are read only as stored variables inside the consuming process, as `os.environ.get`. The pipeline
  step gets the three fake values; afterwards, the results and the log were scanned for them by value (§6).
  - **The secret names** are fixed by the Orchestrator: `ENTSOE_API_TOKEN`, `HF_TOKEN`, `DAGSHUB_USER_TOKEN`. The
    Owner enters them himself. This round creates and uses none.
  - **No other credential** is needed by the pipeline. The day's push uses the workflow's own token, and the MLflow URI
    is public configuration.
- **GitHub's rule that disables a scheduled workflow** after 60 days without repository activity: every run, whatever
  it did, pushes its run record to `main`. That covers an issuance, a failed H2 gate, inputs not shown and nothing to
  issue (`tests/cp18a/test_pipeline.py::test_every_run_whatever_it_does_pushes_a_commit_to_main`). So a schedule that
  fires keeps the repository active, and the local fallback pushes its own runs too. The one exception is a run
  refused before any issuance (a store that does not verify), which is an incident for the Owner.

## 5. The local fallback (`python -m cp18.local run`)

- **One command**, in the pipeline's own clone of the product repository, with the same binary
  (`.local/tools/node-v26.7.0-official/`, checked in place, retrieved by hash only if absent). It rebuilds and checks
  the package zip, then runs the same H2 gate and the same claim rule.
- **Tested for real** (`tests/cp18a/test_dry_run.py`, stress). A runner-kind run issues 2026-08-31 bit-identically to
  CP-17c. The fallback, in its own clone at the same wall clock, then finds the day claimed and issues nothing.
- **The launchd agent** `reports/cp18a/launchd/com.delu.daily-fallback.plist` is written, not installed (`plutil
  -lint` OK). It runs daily at 13:30 Berlin, holds no credential, and inherits the launchd session's environment.

## 6. The public runner class's timing (§24.13)

Measured on standard GitHub-hosted `macos-26` runners of the public scratch repository, the same class as the
product repository's, on development days. Each number is recomputed by `python -m cp18.compare timing` from the run's
downloaded artifact, every file checked against the run's own `results-sha256.txt`
(`reports/cp18a/runner-timing.json`).

| Run | Image | What | Canary fit | Issuances (A1 and three shadows, one after another) | Pipeline | Job |
|---|---|---|---|---|---|---|
| 41185674168 | 20261026.0455.2 | four with the canary, prebuilt payloads | 164.5 s | 413.4, 344.3, 347.7, 351.7 s | 1,634 s | 1,693 s (28.2 min) |
| 41204328732 | 20261013.0424.1 | one, from the store carried across a gap | 142.7 s | 393.6 s | 545 s | 606 s (10.1 min) |
| 41701507248 | 20261026.0455.2 | four with the canary, the live-input builder | 158.0 s | 408.7, 374.6, 376.0, 357.9 s | 1,838 s | 1,903 s (31.7 min) |

- **The machine:** Apple M1 (Virtual), 3 cores, 7 GiB, on both image versions.
- **Criterion 5's ceilings hold on every fit.** The slowest fit took 173.6 s (A1, 2026-08-31, on the run's first
  issuance), against 900 s. The largest peak was 929 MiB, against 4 GiB.
- **Every fit equals CP-17c's.** All 36 fits of the nine issuances (A1, v4, v2, B0) match CP-17c's record of the same
  day, on two image versions.
- **Decision 23's bound.** A four-issuance run with its canary took about 32 minutes of job time, against GitHub's
  6-hour limit and r19's ceiling-bound estimate of about 4¼ hours. The live builder adds about 20–60 s per issuance (run
  41701507248 against 41185674168).
- **Against CP-17c's one data point** (382.7 s per issuance alone, on the public class), the nine issuances here took
  344–413 s each.
- **The lookback is not shortened.** At about 32 minutes for a full catch-up run, the measured runtime gives no reason
  to shorten it.
- **Still to come:** the Orchestrator repeats one dispatch in the product repository after the landing.


## 7. Security hardening (§22; the archived proposal's P0-2, P0-3, P0-7)

- **P0-2, the value-free leak scan** `scripts/leak_scan.py` (standard library only):
  - **F1:** salted fingerprints from `.githooks/credential-fingerprints.json`, full value and first half. The Owner
    generates the file on his Mac with `scripts/credential_fingerprints.py write`, which refuses values under 128 bits
    and prints names only. Until then F1 is skipped with a notice;
  - **F2:** environment-dump shapes;
  - **F3:** known token prefixes.

  It runs from `.githooks/` after the secret guard, failing closed, and as the first CI step in `tests.yml`. The
  proposal's acceptance is on fake fixtures only (`tests/cp18a/test_leak_scan.py`). Four allowlist entries, each with
  its reason, cover 11 findings on the current tree: the recorded CP-20 exposure itself, frozen evidence and two
  landed test fixtures.
- **P0-3, environment-dump prevention:**
  - the AST lint for bare `os.environ[...]` reads (`tests/cp18a/test_environ_access.py`): 32 allowlist entries over 37
    landed reads, each with a reason. The frozen `src/cp17/` reads are allowlisted as frozen. `src/cp18/` has no entry,
    and a new read there fails;
  - the redaction plugin `tests/environ_redact.py`, registered with `-p environ_redact` in `pytest.ini`.
    `pytest.ini` is bound by no earlier evidence (checked against `PINS` and every freeze manifest). The registration
    loads under `python -m pytest`, the `pytest` entry point and `uv run pytest`;
  - the acceptance: a child pytest whose sanitized environment holds a fake token, and a test reading a missing
    variable bare. The output lacks the fake with the plugin, and contains it without.
- **P0-7, the server-side rulesets** `reports/cp18a/rulesets/` hold their exact configuration as JSON (main,
  preserved tags, never pushed, and secret scanning with push protection), with the apply commands written but not run,
  and the acceptance as Owner steps. Applying them is outside this round.

## 8. What CP-18's activation brief and 4.7T's brief cite

| Item | Value |
|---|---|
| The pipeline | `src/cp18/` (`cp18.pipeline.run`); one run: `PYTHONPATH=src python -m cp18 run --root <checkout> --project <folder holding .local> --out <dir> --host runner\|local --now <ISO> --inputs live:<recorded>` (this round: `--mode dry-run` only, `--now` required). Exit 0 done, 1 a day not issued, 2 refused or unpublished, 3 the red line |
| Before the gate | `python -m cp18 prepare --root . --project . --pinned live/pinned --retrieve-pyodide --retrieve-node --out <file>`: the pinned states by the freeze manifest's hashes, Pyodide 0.28.0's 23 files from `https://cdn.jsdelivr.net/pyodide/v0.28.0/full/` and Node.js v26.7.0 from `https://nodejs.org/dist/v26.7.0/`, each by hash; the package zip rebuilt and compared |
| The H2 gate | `cp17.hostcheck` (pins via `refreeze verify` printing exactly `verified`, binary, machine, canary `4e6abb02…`), once per run before its first issuance |
| The live-input builder | `src/cp18/live/`; `cp18.live.build.build_day(day, *, archive, base_end, buffers, search_dir, out, root)`, contract in `src/cp18/live/__init__.py`; live `base_end` = 2026-09-06; shown equal to `cp17.tools.payloads` on 92 of 92 files (`reports/cp18a/live-equality.json`); the clients `cp18.live.{smard,entsoe,gfs}` with `cp18.live.transport.HttpTransport`, instantiated by nothing in this round |
| The red line | `src/cp25/guard.py` `BOUNDARY` (and `GFS_RUN_CUTOFF`): the only boundary on the pipeline's and the builder's paths; retiring it is a one-line, reviewed change. Ruling 1's scope `cp18.live.availability.RULING_1_LAST_DAY` = 2026-09-06 stays after the retirement, by design |
| The workflow | `.github/workflows/daily.yml`: `workflow_dispatch` only; the activation adds `schedule:` and the live mode, and points the claim's remote at `origin` |
| The local fallback | `python -m cp18.local run --clone <path> --url https://github.com/hrsi56/delu-day-ahead-forecast.git --project /Users/djourno/Downloads/PJM --out <dir> --now <ISO> --inputs <spec>`; the agent file `reports/cp18a/launchd/com.delu.daily-fallback.plist`, written, not installed |
| Secret names | `ENTSOE_API_TOKEN`, `HF_TOKEN`, `DAGSHUB_USER_TOKEN`: repository secrets of `hrsi56/delu-day-ahead-forecast`, entered by the Owner, read only inside the consuming process. No other credential is needed: the day's push uses the workflow token (`contents: write`), the MLflow URI is public configuration |
| The claim rule | The day's issued record on `origin/main` is the claim: fetch and check out `main` before each day; commit the day's records through `.githooks` and fast-forward `main` after it; the loser of a push race discards its own issuance and stops; a guard refusal publishes nothing (`cp18.claim`) |
| The daily data-only paths | `live/store/` (`head.json`, `ledger.jsonl`, `states/`, `issued/<day>/`, `runs/`, `search/`) and `live/inputs/days/<day>/` |
| The states, placed once | `live/pinned/local/artifacts/cp-17/inputs/reports/rebaseline/cold-rerun-2026-10-15/search-results/nominal/k13.json`, `live/pinned/local/artifacts/cp-17c/state/freeze-origin-state.json`, `live/pinned/local/artifacts/cp-17c/state/canary/A1-2026-09-06.{json,npz}` (the same blobs as `reports/cp18a/dryrun/pinned/`) |
| The store's genesis | `python -m cp18 seed-store --genesis live/pinned/local/artifacts/cp-17c/state/freeze-origin-state.json:2026-09-07:2026-09-06`: the freeze-origin states at 2026-09-06, first day 2026-09-07; its state file reproduces the manifest's `1388d74d…` |
| The carry | `python -m cp18 carry --last-window-day <4.7T's last window day> --first-live-day <the first live day> --reason <text>`; rehearsed across a gap on two machines (`reports/cp18a/carry-rehearsal.json`) |
| S_14 (H4) | `python -m cp18 search --k 14 --file <k14.json from the M3> --provenance <text>` → `live/store/search/k14.json`; until then each day S_14 serves stays open with "S_14's state not in place" |
| The timing | Public `macos-26` class: one issuance 344–413 s; four with the canary 1,634–1,838 s of pipeline time, 28–32 job-minutes; slowest fit 173.6 s, largest peak 929 MiB (`reports/cp18a/runner-timing.json`) |

**What the activation needs beyond this round** (named, not done):
- **Live GFS decoding on the runner** needs an ecCodes environment (`eccodes` 2.48 / `eccodeslib` 2.49, as CP-20's
  `reports/weather-admission/requirements.freeze.txt` pins them), or the decode moves to the Owner's Mac. This round
  replays decoded runs.
- **The load forecast's availability.** It is tier 3, so on a live day the retrieval must run and archive it before the
  cutoff (published by D−1 10:00 Berlin, cutoff 11:00), or take a document time from a vintage-preserving source. A run
  after the cutoff can show neither, and the day is not issued with its cause.
- **Live GFS needs the AWS listing.** CP-25's documented-schedule reconstruction has no dated captures after
  2026-09-23, so it cannot cover a live day.
- **A calendar edge for a later brief.** On a live day that is a Monday 31 December (2029, 2035), the landed holiday
  code gives `is_bridge_day = 0` for D, because the frame stops at D (`src/delu_forecast/features.py:112–113,124`).
  Fixing it needs a frozen-code change or a frame past D.
- **The product repository's dispatch.** The Orchestrator's dispatch after landing uses this round's committed
  material: `reports/cp18a/dryrun/` (states, recorded responses) and the workflow's defaults.



## 9. The red line, the CI, and what stayed frozen

- **The red line in code.** The pipeline refuses a plan holding any day after 2026-09-06, before anything is
  synchronized, checked or retrieved, and names no such day (`cp18.plan.admit`, `cp25.guard`). The live builder's only
  boundary is `cp25.guard`. In this round no market data after 2026-09-06 was downloaded, read or printed, on this
  machine or on a runner. Every runner run used a simulated wall clock on a development day.
- **The red-line test** (`tests/cp18a/test_red_line.py`) covers every file this round adds or changes, with no file
  skipped whole:
  - JSON is parsed;
  - NumPy archives are opened, and their instants and days checked;
  - wheels and archives are opened;
  - everything else is scanned as bytes.

  Each date after the boundary must be a calendar or protocol date from its reasoned list, or a wall-clock timestamp.
- **Frozen.** Nothing under `src/cp17/`, `src/cp17c/`, `src/delu_forecast/`, `src/cp15/` to `src/cp28/`,
  `src/cp17probe/`, `src/cp17cprobe/`, `data/`, `reports/development-inputs/`, `pyproject.toml` or `uv.lock` changed;
  no anchor or governance file did either. `refreeze verify` on CP-17c's manifest prints `verified` at the candidate.
- **Allowed paths.** Every changed path is inside the brief's list, plus two that the Orchestrator's amendment of
  2026-10-31 adds for item 7:
  - `tests/test_40_publication_guard.py`: its throwaway repository also copies `scripts/leak_scan.py`, which the
    fail-closed pre-push hook now runs;
  - `tests/test_48_publication_tools.py`: the expected prerelease order shifts by one for the leak scan, which is
    `tests.yml`'s first run step.
- **CI-ready.** The workflow's steps, the leak scan first, are green on a history-free single-commit copy with
  `CI=true` and Python 3.12, and `pytest -m stress` passes locally (the return gives the logs).

## 10. Disclosures

- **Two usage-limit pauses** interrupted the round. The work is unchanged by them, and both Builders resumed from
  their own state.
- **The runner runs, in order** (`reports/cp18a/github-ledger.json`):
  - runs 41185415753 and 41185552151 stopped early: the leak-scan case of the guard demonstration ran before the scan
    was in the tree, and a shallow checkout cannot seed an empty bare repository. Both were fixed in the workflow;
  - run 41206393403 issued nothing. The runner cannot load the native LightGBM (no `libomp`), which the live builder
    had imported through CP-26's `install_issue_label` and `cp15.models`. Every day was recorded as not issued, with
    its cause and the build's own error. The builder now imports neither, and a test builds with LightGBM refused.
- **A pipeline defect, found by the forced causes and fixed.** A run that left two days open and then issued two later
  days tried to close the open days twice. The store refused the second close, so nothing wrong was written. A unit
  test now covers it.
- **Rendered responses.** SMARD and ENTSO-E responses were never recorded raw. The clients are exercised on the
  snapshot's recorded values rendered in each source's response shape, and say so everywhere; GFS is truly recorded.
- **One construction difference in the live builder:** `eligible` on D's rows is their feature validity, because the
  live frame never holds D's price. It equals the development value on every development day, and no frozen fit reads
  it.
