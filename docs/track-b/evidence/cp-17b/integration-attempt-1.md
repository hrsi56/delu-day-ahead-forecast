# Verdict — CP-17b — Integration — FAIL

- Candidate SHA: 2529c62f0640ae4fedb4b81b9d64dfc8e2c0eeed
- Plan / version / bar: `capstone_v21.md`, v21-r17 (SHA-256 `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`),
  `### 16.2 What freezes and what updates every day` (section 32 lines, 2408 bytes, SHA-256
  `c54723eff2f113a18efaef5884c3c2a93876c755edacf3b2fb70dc3af44ac5ec`), with §24.9's failure rules, §19.2 and the Owner's
  decisions 13–19 (`docs/track-b/cp-17-owner-decisions-2026-10-28.md`, `4d049770…`), as the brief `b9aeeee4…` binds them.
- Verbatim bar excerpt (confirmed in the file at the candidate with `scripts/bar.py bar … --at 2529c62f…`, exit 0):

  > ### 16.2 What freezes and what updates every day
  >
  > Freeze code and dependencies, algorithm/architecture, feature and source-availability
  > contracts, hyperparameters, training-window and label-delay rules, initial artifact/state,
  > randomness, refit schedule, uncertainty/calibration updates, scoring/decision rules and failure
  > policy. Store numeric registry versions and initialization fingerprints as §9 requires.
  >
  > For the selected final product, **daily retraining, eligible input refresh and forecast
  > issuance are required on every delivery day**. Each successful fit produces a versioned
  > artifact with its training window, available labels, seed, timestamps and parent/input/state
  > hashes. Use only information available at the fixed origin. Daily fitting changes weights/state
  > within the frozen policy, not the adopted generation; discretionary tuning or changing that
  > policy requires a new freeze and evaluation. Never overwrite an issued forecast after outcomes.
  >
  > The future brief fixes numeric origin/deadlines, windows, resource ceilings and the exact
  > meaning of a successful daily fit before the fresh-data replay/final freeze. Input refresh,
  > residual-state maintenance or TabPFN context replacement alone is not weight training. A
  > candidate unable to meet daily retraining within admitted licensing/resources needs an explicit
  > Owner-approved exception specifying its real update mechanism and public wording before live
  > admission; no alternative cadence or exemption is silently inferred from model family.
  > Immutable historical v1/reference artifacts remain untouched; this requirement does not
  > retroactively retrain them or force every research comparator to train daily.
  >
  > Daily operation covers all delivery days, including DST. The operational brief supplies an
  > explicitly authorized unattended schedule and incident/fallback policy. Publication authority,
  > operator ownership, monitoring, permissions and resources must be settled before launch. This
  > amendment creates no automation or standing authority to publish externally.
  >
  > For missing inputs/labels, failed training, resource exhaustion or source outage, apply the
  > frozen fallback/staleness limits or record failed issuance. Display a failed/skipped fit as
  > such, even if a valid fallback produces a forecast. Do not count retained weights as a new
  > successful training run or backfill a late forecast as timely. Failures remain in the record.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: yes. `git -C …/critic-1 status --porcelain` was empty at the start and at the end;
  `HEAD` stayed `2529c62f0640ae4fedb4b81b9d64dfc8e2c0eeed`. I made no Git write in the repository. The only commits were
  the CI runner's own, inside its throwaway `git init` copies under `.local/tmp/cp-17b/critic-{ci312,stress}`, which it
  removed (`scratch_removed: true`). My scratch copies (a `git archive` extract and a copied Pyodide folder) were under
  `.local/artifacts/cp-17b/critic-1/` and are deleted.
- Compute: about **2.0 machine-hours** (summed worker wall time), at most 4 concurrent workers, BLAS 1 for every native
  fit, no network, no retrieval. Itemised at the end.

## Commands actually run

All from `/Users/djourno/Downloads/PJM/.local/worktrees/cp-17b/critic-1` (or the scratch copy named), with
`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src`, the five `*_NUM_THREADS=1` for
every fit, `CP17_PROJECT_ROOT=/Users/djourno/Downloads/PJM`, and `/Users/djourno/Downloads/PJM/.venv/bin/python` (3.13.15).
Outputs are under `.local/artifacts/cp-17b/critic-1/` (abbreviated `$O`).

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git status --porcelain`; `git rev-parse HEAD` | 0 | empty; `2529c62f…eed` |
| 2 | `git show main:scripts/bar.py \| python3 -I - bar capstone_v21.md '### 16.2 What freezes and what updates every day' --at 2529c62f…` | 0 | the excerpt above; plan sha256 `3124451d…`, section `c54723ef…` |
| 3 | `shasum -a 256` of the anchor, the brief, both decisions records, the 8 pinned copies, CP-17's four evidence files and its landing record | 0 | every hash equals the brief's and the freeze record's citations; `issued-brief.md` equals `.local/artifacts/cp-17b/issued-brief.md` byte for byte (`b9aeeee4…`) |
| 4 | `git diff --name-status 6abbce5f 2529c62f…` filtered against the allowlist | 0 | no path outside `src/cp17/`, `tests/cp17/`, `tests/cp17b/`, `reports/cp17b/`, `docs/track-b/evidence/cp-17b/`; in `tests/cp17/` only `test_records.py` (two tests) and `test_hosts.py` (the `package` fixture) |
| 5 | `git ls-tree -r -l 2529c62f…` for files > 50 MB | 0 | none; largest 30.8 MB (`models/champion/python_model.pkl`) |
| 6 | red-line scan of every added line for dates after 2026-09-06 (and UTC keys `2026-09-06T22/23`) | 0 | only file names, ledger timestamps and protocol/calendar dates (2026-09-07/09 window origins, 2026-10-25 clock change, 2026-12-04/05, S_14 = 2027-01-06); no UTC key after the boundary |
| 7 | `python -m cp17.tools.bundle --out $O/bundle/src.zip` | 0 | `34 files 91480 bytes 41256a486bae6477`; `src.json` equals `reports/cp17b/bundle-manifest.json` in every key |
| 8 | `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17b/freeze-manifest.json` | 0 | `verified` |
| 9 | `python -m cp17.tools.freeze verify docs/track-b/evidence/cp-17/freeze-manifest.json` | 1 | exactly `src/cp17/issue.py: missing or altered`, `src/cp17/schema.py: missing or altered` (as the freeze record says) |
| 10 | `python3 …/ci-runner.py critic 2529c62f… ci312` | 0 | tree `0b8686ac…`; Python 3.12.14; steps 01 sync, 02 `build_wasm_payload.py` (82 s), 03 `pytest -q` **2420 passed, 42 skipped** (634 s), 04 CQR fixture 8 passed, 05 `verify_release.py` PASS, 06 WASM equivalence 15 passed, 07 `publication_guard.py tree` clean, 08 stress collection 19/2461; every step exit 0; scratch removed |
| 11 | `python3 …/ci-runner.py critic 2529c62f… stress` | 0 | `pytest -m stress -q`: **19 passed, 1 skipped** (475 s); scratch removed |
| 12 | `pytest -m stress -rA tests/cp17/test_hosts.py tests/cp17probe/test_probe_browser.py` (in the worktree, local inputs present) | 0 | `test_issuing_host_reproduces_its_record` PASSED, `test_browser_reproduces_the_issuing_host` PASSED, probe browser PASSED (3 passed, 241 s) — confirms the stress run's host tests ran rather than skipped |
| 13 | `python -m cp17.tools.exercise partial --day 2026-03-30 --bundle $O/bundle/src.zip --out $O/partial/2026-03-30` | 0 | `[('A1','ok')] successful daily fit (partial: 23 of 24 hours; missing 02:00 Europe/Berlin) True` (365 s) |
| 14 | `python -m cp17.tools.exercise partial --day 2023-08-31 …` | 0 | every policy failed at its inputs, "failed issuance (no hour of the day is forecastable by the frozen design)", no process started (30 s) |
| 15 | `python -m cp17.tools.exercise shadow-run --mode native --first 2026-08-24 --out $O/shadow-native` | 0 | 14 days, each `{'v4','v2','B0'}: registered`, buffers bitwise; `final {'v4': True, 'v2': True, 'B0': True}` (634 s) |
| 16 | `python -m cp17.tools.exercise shadow-run --mode host --first 2026-08-24 --bundle $O/bundle/src.zip --out $O/shadow-host` (full 14 days, two workers) | 0 | A1 ok every day; buffers within 2.18e-14, B0 bitwise; `final {'v4': False, 'v2': False, 'B0': True}` against CP-17's bitwise digest, i.e. within rounding (1,846 s) |
| 17 | `python -m cp17.tools.exercise control --day 2026-09-06 --payloads $O/shadow-native/payloads --bundle $O/bundle/src.zip --stale .local/artifacts/cp-17/final/nodes/node-A1-2026-09-06.json --out $O/control` | 0 | `[('A1','failed'),('v4','ok')] failed fit; fallback v4 issued PASS` (178 s) |
| 18 | `python -m cp17.tools.parity --out $O/parity --origins 2026-03-29` | 0 | `2026-03-29 PASS {A1,v2,v4,v5,B0: True}`; `PASS 102s` |
| 19 | `python -m cp17.tools.b0check --out $O/b0/b0-rebuild.json` | 0 | 2,390 of 2,390 common days bitwise, 36 extra days (26 + 10), 524 origins differ: "not equal: B0 is shadow-issued too"; the JSON equals `reports/cp17b/b0-rebuild.json` key for key (84 s) |
| 20 | scratch `git archive 2529c62f… \| tar -x` → `refreeze verify … --root <scratch>` | 0 | `verified` |
| 21 | same scratch with `capstone_v21.md` appended, decisions 13–19 and 1–12 and the CP-25 rulings appended, a new decisions record added, CP-17's brief appended → `refreeze verify` | 0 | `verified` (local runtimes checked from the primary checkout) |
| 22 | same scratch → `python -m cp17.tools.freeze verify docs/track-b/evidence/cp-17/freeze-manifest.json --root <scratch>` | 1 | `capstone_v21.md: altered`, CP-17 brief altered, rulings altered, CP-25 rulings altered, plus the two package files |
| 23 | scratch: tier register +1 byte → `refreeze verify` | 1 | `reports/development-inputs/tier-register.json: missing or altered` |
| 24 | scratch: `uv.lock` +1 byte → `refreeze verify` | 1 | `uv.lock: missing or altered` |
| 25 | scratch: `src/cp17/dailyfit.py` appended → `refreeze verify` | 1 | the file altered; rebuilt package files, identity and zip differ |
| 26 | scratch: `src/cp17/daily.py` (the driver) appended → `refreeze verify` | 1 | `src/cp17/daily.py: missing or altered` |
| 27 | scratch restored → `refreeze verify` | 0 | `verified` |
| 28 | `CP17_PROJECT_ROOT=<copy of the project's Pyodide 0.28.0 + extract link>`: unaltered → `refreeze verify`; then `pyodide.mjs` appended → `refreeze verify` | 0, then 1 | `verified`; then `…/pyodide-0.28.0/pyodide.mjs: altered` |
| 29 | scratch with all of row 21's changes: `pytest -q tests/cp17/test_records.py::test_freeze_manifest_verifies tests/cp17b/test_refreeze.py` | 1 | **1 failed, 24 passed**: `test_freeze_manifest_verifies` fails (`capstone_v21.md: altered` and four more); every `tests/cp17b/test_refreeze.py` test passes |
| 30 | scratch reset to the candidate except **only** `capstone_v21.md` appended and a new decisions record added: `pytest tests/cp17/test_records.py::test_freeze_manifest_verifies`; `refreeze verify` | 1; 0 | `AssertionError: assert ['capstone_v2...g or altered'] == ['src/cp17/is...g or altered']`; `verified` |
| 31 | same scratch, `CI=true`, local inputs hidden: `pytest -q -m 'not stress' tests/cp15 tests/cp16 tests/cp17 tests/cp17b tests/cp17probe tests/cp20 tests/cp25 tests/cp28 tests/test_cp26_*.py tests/test_36_derived_records.py tests/test_43_publish_rules_migration.py tests/test_45_pres3_v4_publication.py` (excluding `test_cp26_search.py`) | 1 | **1 failed, 1164 passed, 14 skipped**; the one failure is `tests/cp17/test_records.py::test_freeze_manifest_verifies`. The anchor-reading tests of CP-16, CP-24's derived records and CP-26 (`test_cp26_r15.py`, `test_cp26_repair_contract.py`, `test_36_derived_records.py`) pass under the same change |
| 32 | final `git status --porcelain`; `git rev-parse HEAD` | 0 | empty; `2529c62f…eed` |

## Evidence actually inspected

- **The brief** `docs/track-b/evidence/cp-17b/issued-brief.md` (all of it) and the Owner's decisions 13–19.
- **The diff** `6abbce5f..2529c62f`: `src/cp17/issue.py`, `schema.py`, `daily.py`, `shadow.py`, `tools/bundle.py`,
  `tools/refbundle.py`, `tools/refreeze.py`, `tools/exercise.py` and `tools/b0check.py` read in full or in their changed
  parts; `tests/cp17/test_records.py` and `test_hosts.py` supersessions; `tests/cp17b/test_daily.py`,
  `test_refreeze.py`, `test_units.py` (partial-day boundary cases) and `test_records.py` (test list).
- **CP-17's verifier** `src/cp17/tools/freeze.py` (`ROOT_FILES`, `CONTRACT_FILES`, `verify`) and CP-17's freeze manifest
  `pinned_files` (anchor, CP-17 brief, decisions 1–12, …) and `contracts_sha256` (CP-25 rulings, CP-26 GFS ruling, …);
  CP-17's verdict notes N1–N7.
- **The evidence:** `freeze-record.md` (all), `freeze-manifest.json` (identity `439115fb…`, content `261c6283…`,
  `reference_runtime`, `pipeline_files_sha256`, `verification`), `artifact-2026-09-06.json` (verifies, schema-valid,
  cites `439115fb…` and package `682c5833…`; quantiles bit for bit CP-17's artifact `4e6abb02…`, same payload),
  `4-7t-frozen-protocol.md` (diffed against CP-17's), the eight `pinned/` copies.
- **The records:** `reports/cp17b/report.md` (all, including Open items), `partial-days.json`, `shadow-run.json`,
  `control.json`, `native-parity.json`, `b0-rebuild.json`, `compute-ledger.jsonl` (16 rows, 2.33 machine-hours).
- **The runner** `.local/artifacts/cp-17b/ci-runner.py` (read before use), and the earlier runner's step timings only,
  for budgeting.
- **My run outputs**, compared field by field with the committed records:
  - **partial days:** every recorded field equal (forecastable hours, missing hour, payloads, paths, displays,
    shadows' quantile hashes and intakes, A1 issued-vs-native 0.0823 EUR/MWh with selections matched, A1 native vs
    CP-26 D2 bitwise, the host's issued quantile hash `718f0c0d…`); A1's own measurement 112.3 s / 656 MiB; no
    non-local request; the native comparison labelled "not judged: the native comparison path, which can never issue";
  - **native shadow run:** start state and every day's payloads equal to the record; every day's buffers bitwise equal
    to CP-26's rebuilt state; every shadow's quantiles bitwise equal to CP-26's stored forecast; final buffers equal
    to CP-17's recorded freeze-origin digests for v4, v2 and B0;
  - **host shadow run (all 14 days):** A1 issued every day ("successful daily fit"), every artifact verifies, every
    shadow registered; largest standardized buffer difference against CP-26's 2.18e-14, B0 bitwise; per-day total of A1
    plus the three shadows median 249 s, largest 277 s, within 900 s on every day; peak process RSS 916 MiB; no
    non-local request; final digests, payloads and all 42 shadow quantile hashes equal to the Lead's host record;
  - **control:** A1's process killed at 15.0 s, its fresh folder left empty; the planted stale record (quantiles
    `4e6abb02…`, a valid successful A1 record of the same target) never read; v4 issued from its own fit (81.9 s,
    792 MiB), the artifact verifies; v4/v2/B0 shadow hashes equal to the record;
  - **parity spot 2026-03-29:** checks, payload hashes, quantile hashes and ledger file hash all equal to CP-17's
    committed record.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| O1 | Partial days (decision 13): criterion 3 on the forecastable hours by the design's rule; partial display naming the missing hours; no-forecastable-hour day a failed issuance for every policy; exercised under the host and natively on a post-DST day and an input-gap day; tested with boundary cases | PASS | `issue.forecastable_keys` / `check_inputs` / `check_emission` / `partial` / `verify_artifact`; `schema` v2 kinds and `verify_bundle`'s partial check. Rows 13–14 reproduce `partial-days.json` exactly (2026-03-30: 23 of 24, missing 02:00, same path and display; 2023-08-31: failed issuance, no process). Unit tests cover 23/24/25-hour complete days, one missing hour, 24 of 25, a single hour, zero hours, extra/missing/reordered/duplicated keys, a key outside the day, and a fallback on a partial day |
| O2 | Shadow issuances (decision 14): v4 and v2 every day under the host, stored before the outcome, own errors into own buffer once after D−2, never published; B0 rebuilt from prices shown equal to CP-26's or else shadow-issued; consecutive-day exercise from an earlier CP-26 origin through 2026-09-06 ending at CP-17's recorded state (bitwise natively, within rounding under the host); measured per-day total within 15 min | PASS | `cp17.daily.issue_day` shadows, `cp17.shadow.ShadowStates` on CP-26's classes. Row 19: the price rebuild is not CP-26's (36 days, 524 origins), so B0 is shadow-issued, as the brief prescribes. Rows 15–16: natively bitwise every day and at the end; under the host within 2.18e-14 (B0 bitwise); per day ≤ 277 s |
| O3 | N1–N7 fixed | PASS | **N1:** one fresh process per attempt, `mkdtemp` output path, 900 s timeout, killed/timed-out/non-zero/recordless/unreadable/foreign/unmeasured record → failed fit (`tests/cp17b/test_daily.py`, real processes); row 17 on the issuing host; the driver hashed in `pipeline_files_sha256` and refused when altered (row 26). **N2:** `fitted_artifact` v2's two forms, `MEASUREMENT` ≤ 900 s / 4 GiB, `issue.artifact` raises and `verify_artifact` refuses without a measurement; native path labelled and never issues. **N3:** `decide`'s `accept` builds and verifies the artifact inside the chain. **N4:** `refreeze verify` recomputes the package (rebuilt), Pyodide's 23 files, Node.js, `k13.json`, the schemas and the governance copies (rows 8, 20–28). **N5:** the report's Open items include F1 (but see O4/O8). **N6:** `policy_identity.reference_runtime` carries Chromium 153.0.8010.12, WebKit 26.6, Playwright 1.63.0, the machine class, checked against a measured run. **N7:** `resources_ok` prints `{wall_seconds!r}` |
| O4 | Governance pins that survive amendment (decision 19): governance documents bound by frozen copies with SHA-256; computational inputs, code and runtimes verified live; tests prove a changed live anchor or a new decisions record leaves `freeze verify` green and a changed computational input, code file or runtime file fails it | **FAIL** | The frozen copies are right (row 3), and `refreeze verify` behaves exactly as required (rows 20–28). But the candidate's suite still binds the live anchor: `tests/cp17/test_records.py::test_freeze_manifest_verifies`, which this round superseded, asserts that CP-17's `freeze.verify` reports **exactly** the two re-frozen package files, and CP-17's manifest pins `capstone_v21.md` (and CP-17's brief, decisions 1–12 and the CP-25/CP-26 rulings) live. With only the anchor changed and a new decisions record added — the r18 case the candidate's own `test_refreeze.py` simulates — that test fails (rows 29–30), and it is the only failure in a 1,165-test governance-sensitive subset (row 31). So r18 turns the workflow's `pytest -q` red, against decision 19's stated purpose ("so that r18 and later records do not break `freeze.verify`"). The report's Open items do not name it |
| O5 | The re-freeze record and manifest: complete on its own; decisions 13–18, the success definition with the partial-day rule, the shadow rule, C1, G2, F1 stated; the new policy identity and the reissued freeze-origin artifact; CP-17's freeze superseded, not edited | PASS | `freeze-record.md` §§1–13 (read in full); identity `439115fb…`; artifact `91e00fea…` issued under the host with the new code (80.4 s, A1, "successful daily fit"), verifies and is schema-valid, quantiles bit for bit CP-17's; CP-17's four evidence files unchanged at the cited hashes and checked by `refreeze verify` |
| O6 | The fit is unchanged, shown: every changed `src/cp17/` file listed with why; `schema.py` changed, so CP-17's full native parity and issuing-host parity rerun, equal to CP-17's records | PASS | Changed: `issue.py`, `schema.py` (and new `shadow.py`, driver `daily.py`, native-only tools) — the record's table matches the diff; `dailyfit.py`, `scoring.py`, `retrain.py`, `attribution.py`, the runners and `host/driver.py` unchanged. `native-parity.json` and `host-parity.json` report every origin/run equal to CP-17's (all true). Row 18 reproduces 2026-03-29 equal to CP-17's record; row 12: issuing host and Chromium reproduce CP-17's committed A1 quantiles on CP-17b's package |
| O7 | 4.7T's protocol revised only where decisions 13 and 14 touch it, outcome-blind; everything else by CP-17's hash; the analysis tool still refused by the guard | PASS | `4-7t-frozen-protocol.md` replaces §3 and §11 and adds to §4 and §7 only, cites CP-17's protocol `337a102d…`; no outcome; `fresh_test.py` unchanged; `tests/cp17b/test_records.py::test_the_windows_analysis_tool_stays_refused_by_the_guard` and CP-17's guard test pass in row 10 |
| O8 | The Owner's summary for r18 in the return | Not verifiable at the candidate | The return is not part of the candidate. The report's Open items (the r18 terms, F1 at 0.082 EUR/MWh, the GFS-late disclosure, the protocol revision, CI's unchecked runtimes, §19.2) are present and accurate as far as my reruns reach; they omit the r18 CI break found under O4 |
| F1 | Blind: boundary 2026-09-06; no later byte read or inferred; no 4.7T forecast | PASS | Row 6; every exercise reads development data through 2026-09-06 (`payloads.admit`); my runs touched no later day; `test_no_committed_record_holds_a_date_after_the_boundary` passes |
| F2 | GitHub-landable: no committed file over 50 MB | PASS | Row 5 |
| F3 | CI-ready: seven steps green history-free with `CI=true` Python 3.12; `pytest -m stress` passes; no test depends on history, tags or local-only inputs; local-input tests skip with a reason | PASS (at this tree) | Rows 10–12. Under `CI=true` with local inputs hidden, the cp17/cp17b local-input tests skip with stated reasons (row 31's skip list). O4 records why this stops holding at r18 |
| F4 | What may change, all listed | PASS | Row 4; the record lists every `src/cp17/` change and the three `tests/cp17/` supersessions |
| F5 | What never changes | PASS | Row 4: nothing under `reports/cp17/`, `docs/track-b/evidence/cp-17/`, `src/cp17probe/`, `src/delu_forecast/`, `src/cp15/`–`src/cp28/`, `data/`, `reports/development-inputs/`, root `pyproject.toml`/`uv.lock`, anchors, decisions records, `AGENTS.md`, role files, exposure ledger or backup register changed; `src/cp17/tools/freeze.py` unchanged |
| F6 | The Critic's reruns: CI 3.12 history-free and stress; one partial-day issuance; the shadow run; the killed-process control; `freeze verify` after a simulated anchor change | PASS (all performed; results as expected) | Rows 10–17, 20–28. The shadow run was run in full under the issuing host (14 days), not shortened |

### Observations (not blocking on their own)

- **N1. Ledger figure in the commit subject.** `2529c62f`'s subject says "2.8 machine-hours"; the committed
  `reports/cp17b/compute-ledger.jsonl` sums to 2.33 (workers × wall seconds). The records themselves state no total.
- **N2. What `refreeze verify` does not recompute.** The freeze-origin arrays hash, the reference bundle manifest hash and
  the initial state are named in `verification` as local reproduction material, not recomputed. N4's list (package,
  Pyodide, Node.js, search state, schemas, governance copies) is fully recomputed.
- **N3. The host's buffers diverge from native by rounding** (2.18e-14 after 14 days; v4 and v2 not bitwise at the
  freeze origin, B0 bitwise), as the brief allows and the record discloses. 4.7T's product shadows will carry host
  rounding from 2026-09-07 while the descriptive v4 comparator stays native; the protocol says so.
- **N4. The assignment names the worktree `critic-open`;** the worktree made for this review is `critic-1`. No effect.

## On FAIL only

- **Single largest meaningful gap:** the candidate still binds the live anchor in CI. This round's supersession of
  `tests/cp17/test_records.py::test_freeze_manifest_verifies` requires CP-17's `freeze.verify` to report exactly the two
  re-frozen package files, and CP-17's manifest pins `capstone_v21.md` (and CP-17's brief, decisions 1–12 and the
  CP-25/CP-26 rulings) live. So r18's anchor edit fails the workflow's `pytest -q`, against decision 19's purpose, and
  the open items do not say so.
- **Exact next acceptance test:** on a history-free single-commit copy of the next candidate with `capstone_v21.md`
  changed and a new decisions record added, the workflow's seven steps pass under `CI=true` Python 3.12, including
  `tests/cp17/test_records.py::test_freeze_manifest_verifies`, and `refreeze verify` still prints `verified`. In the same
  copy, a changed computational input, or a CP-17 code file other than `issue.py`/`schema.py`, must still fail both. A
  CI-safe test in `tests/cp17b/` should exercise that anchor-change case against the superseded CP-17 check.

## Compute

| Job | Workers | Wall (s) |
|---|---:|---:|
| CI 3.12 history-free (row 10) | 1 | 742 |
| stress (row 11) | 1 | 511 |
| host and browser stress tests (row 12) | 1 | 242 |
| partial days (rows 13–14) | 1 | 395 |
| shadow run, native (row 15) | 1 | 636 |
| shadow run, issuing host, 14 days (row 16) | 2 | 1,848 |
| control (row 17) | 1 | 178 |
| parity spot (row 18) | 1 | 103 |
| B0 rebuild (row 19) | 1 | 84 |
| r18 simulation subset and targeted tests (rows 29–31) | 1 | about 560 |
| bundle builds and `verify` runs (rows 7–9, 20–28) | 1 | about 60 |
| **Total** | ≤ 4 at once | **about 7,200 worker-seconds, 2.0 machine-hours** |
