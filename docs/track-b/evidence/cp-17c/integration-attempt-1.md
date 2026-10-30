# Verdict — CP-17c — Integration — BLOCKED

- Candidate SHA: 548bd0694b7b739df25997074f476bf761041046 (`gauntlet/cp-17c`; base `main` = adcaf051560bbeebec9065e848bcc1cbab3939fe)
- Plan / version / bar: `capstone_v21.md`, v21-r19, SHA-256 `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e` at the candidate; §24.13 "The issuing host (decision 24; H1)" (73 lines, 5,646 bytes, section SHA-256 `6eacad578ebbded76cc978cb1ef839e024089b28e532e17eb0cd88da50f24d1e`) and "What CP-17c re-freezes, and what 4.7T then tests" (80 lines, 4,886 bytes, section SHA-256 `adee5cff2146948b0aac8c2d2b1cf69615db59db57bc87682ae6f5af4a980263`). The controlling brief is `docs/track-b/evidence/cp-17c/issued-brief.md`, SHA-256 `5f34f3ab298cfa619ddefaa9b1dcfd5df207c73a0ae06cbf8ed30454ac559c7d`, equal to the canonical `.local/artifacts/cp-17c/issued-brief.md` and to its frozen copy under `pinned/`.
- Verbatim bar excerpt (both sections, extracted at the candidate with `scripts/bar.py bar ... --at 548bd069... --quote`; the excerpt is the citation, and any line number is a courtesy and non-binding):

> #### The issuing host (decision 24; H1)
>
> **From CP-17c's landing on,** the issuing host is the following.
>
> | Item | Value |
> |---|---|
> | The runtime | Pyodide 0.28.0, by its 23 pinned file hashes, in the official Node.js v26.7.0 darwin-arm64 binary, one worker. The tarball is `node-v26.7.0-darwin-arm64.tar.gz` from `https://nodejs.org/dist/v26.7.0/`, 57,622,243 bytes, SHA-256 `7ee659a7768e641bbfd5360940660b8e8fd0052f77488f365562bac522fc15d4`. Its `bin/node` is 145,238,560 bytes, SHA-256 `a9bd0630891c2dcdee70de88270fee2cc0c4a9e76495039dd3b4f91c5e6b71df`. The chain's judgement and the shadow states run in CPython inside `cp17.daily`, in the environment `uv.lock` pins, under one CPython patch version that CP-17c pins |
> | The machines | **The daily product:** a GitHub-hosted standard runner, label `macos-26` (Apple silicon), in the product's repository, `hrsi56/delu-day-ahead-forecast`, which is public. **4.7T and any local run:** the Owner's Apple-silicon Mac. The runner's image version and CPU model are recorded, and are not pinned |
> | The reference runtime (§19.3) | the issuing host above, plus Chromium 153.0.8010.12 and WebKit 26.6 through Playwright 1.63.0, on the Apple M3 machine class, as §24.12 records |
> | Resources | unchanged: criterion 5's one worker, 15 minutes of wall time and 4 GB of peak memory |
>
> **What this supersedes in §24.12, from CP-17c's landing:**
> - **its "The issuing host" row,** and the issuing-host part of its "reference runtime" row;
> - **in its list "For CP-18":**
>   - the first item's "deadline and late-forecast rule (§24.4)". The publication time below governs;
>   - the item "where the pipeline runs". The issuing host is the binary and runtime pinned above.
>     - **A machine that passes the checks below (H2) is not a runtime change.** That covers any
>       `macos-26` runner VM, image version or CPU model, and the Owner's Apple-silicon Mac.
>     - **Any other binary, runtime file, operating system or architecture is a runtime change** (§16.2).
>
> **Until CP-17c lands,** §24.12's issuing host stays the frozen host. That is the Homebrew binary
> `1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040`, and Homebrew's `node` stays pinned
> on the Owner's Mac.
>
> **Why macOS and not Linux (H1).** Both runners passed cleanly, and decision 24 leaves the choice to the
> Orchestrator. CP-17c-probe proposed Linux.
> - **One binary for the whole product.**
>   - 4.7T runs on the Owner's Mac with no cloud (§24.12).
>   - With the macOS runner, the daily product, 4.7T and any local run all use the same binary,
>     `a9bd0630…`, on the same architecture. So 4.7T tests the binary and runtime the product issues
>     with. The probe found the arithmetic identical on every machine it measured, and the canary checks
>     it on every run.
>   - Linux's binary, `ad19784f…`, cannot run on the Owner's Mac. 4.7T would then have tested another
>     binary, or moved to the cloud against its registered terms.
> - **The machine moved no bit.** The same binary reproduced every fit on the runners' M2 Pro, across two
>   runner images, and the parity and F1 fits on the M3.
> - **The cost is the same.** The product's repository is public, where standard runners cost nothing on
>   either OS, by GitHub's published terms. The probe's ten-times macOS rate is a private repository's.
> - **What Linux would have given:**
>   - reproduction on two runner CPU generations, one of them from the cancelled run's records. macOS
>     showed two Apple generations, the M2 Pro and the M3;
>   - more plentiful runners. Decisions 22 and 23 already absorb a delayed or dropped run.
>
> **The runner class.** The probe measured a private repository's `macos-26` class, and the public
> repository's class may differ.
> - **The arithmetic** did not change across machines. The canary checks it on every run.
> - **The timing** did change. Each fit's ceiling is enforced in its own process, so a slower class fails
>   closed, never silently.
> - **So CP-17c measures on a private repository's `macos-26`.** CP-18 measures the public class's timing
>   in the product's repository, on development days, before the first live issuance.
> - **Why not a public scratch repository.** Its runs would need A1's search state and CP-17c's material.
>   That would publish them before decision 25's one complete publication.
>
> **The checks before each run's first issuance (H2).**
> - They run once per run, on either machine, in the order below. They run again whenever the machine or
>   the runtime changes within a run.
> - **Any failure means nothing in that run is issued,** and each of its days is not issued.
> - **For 4.7T,** they run once before the window's first issuance, as part of §24.12's runtime
>   precondition. A failure there is not a day's outcome: no window issuance runs, nothing is counted, and
>   4.7T's brief returns it as a blocker.
>
> The checks:
> 1. **The pins.** `refreeze verify` against CP-17c's manifest must report no problem and no unchecked
>    item. It exits 0 in both cases, so the run reads its output, as §24.12 requires for 4.7T.
> 2. **The binary.** The tarball and `bin/node` must match the hashes above.
> 3. **The machine.** It must be macOS on ARM64. On the runner, `ImageOS` must be `macos26`, and the image
>    version is recorded.
> 4. **A canary fit.** A1 at the freeze origin, 2026-09-06, is reissued under the host. Its quantiles must
>    reproduce the frozen SHA-256 that CP-17c records for the freeze origin.
>    - The probe found CP-17b's value,
>      `4e6abb02fbb02aa8ef202207f21b76bc33b34c37d025a0a93a491135ea43cea5` (`reports/cp17b/host-parity.json`),
>      and CP-17c shows it unchanged.
>    - It took 98.8 s on `macos-26`.

and

> #### What CP-17c re-freezes, and what 4.7T then tests
>
> **A new runtime is a change under §16.2,** so CP-17c re-freezes A1 before 4.7T opens. 4.7T is the new
> evaluation. CP-17c records a new policy identity, and 4.7T tests that identity under the host above.
> CP-17c's brief is the Orchestrator's, under decision 25.
>
> **What CP-17c changes:**
> - **the issuing host** above, by its hashes;
> - **how a run gets the binary.** The tarball (57,622,243 bytes) is over the project's 50 MB limit for a
>   committed file, and `bin/node` (145,238,560 bytes) is over GitHub's 100 MB limit, by GitHub's published
>   terms. So each run retrieves
>   the tarball and checks both by hash. A failed retrieval or a failed hash means the run issues nothing;
> - **the binary's path.** The frozen defaults `cp17.daily.NODE` and `cp17.tools.hosts.NODE` name
>   Homebrew's path;
> - **the Pyodide folder** (`cp17.tools.freeze.RUNTIME_DIR`, now `.local/tools/pyodide-0.28.0`), and how
>   the 23 files reach the runner. The probe proposed committing them;
> - **`refreeze verify`'s zip check.** It must report no unchecked item on the runner and on the Owner's
>   Mac. The zip is compared only where the zlib runtime equals the one the manifest records. CP-17b's is
>   `1.2.12`, and CP-17c records its own, so the check must pass on both machines;
> - **where `refreeze verify` runs:** on the runner and on the Owner's Mac, before the first fit;
> - **how the states reach the runner and persist between runs:**
>   - A1's search state `k13.json`, now only in the local `evidence/cp-26` extract;
>   - the freeze-origin states of v4, v2 and B0;
>   - the shadows' buffers;
>   - the issued records;
>   - the canary's payload;
> - **the CPython patch version,** pinned without changing the root `uv.lock` or `pyproject.toml`, which
>   CP-26's tests pin;
> - **where the image version and CPU model are recorded:** in the artifact's lineage, or in CP-18's
>   records;
> - **the checks above** (H2);
> - **R7's `schema.py` defect, fixed (H3).** §24.12's R7 fixes it "at the next freeze". CP-17c is that
>   freeze, and it comes before 4.7T, so 4.7T's result covers the fixed identity.
>   - **The fix changes only that error path.** Every fit, quantile and artifact field stays
>     bit-identical, and CP-17c's parity shows it.
>   - **R7's acceptance and its instruction end at CP-17c's landing.**
>   - **If the fix cannot be that narrow,** R7 stands unchanged, and the Owner is told.
>
> **What CP-17c shows.**
> - **On a GitHub-hosted `macos-26` runner in a private repository, and on the Owner's M3:**
>   - `refreeze verify` with no problem and no unchecked item;
>   - the issuing host's parity at the nine origins, bit for bit;
>   - the shadows' buffers over the 14 days, as CP-17b did;
>   - the timing.
> - **On the Owner's M3 only:**
>   - native parity with CP-26, which is the check of code identity (§24.12);
>   - Chromium's and WebKit's parity at the freeze origin, if the package's zip changed. The reference
>     runtime's machine class is the M3's.
>
> **What it keeps.** Every other term of CP-17b's freeze, as §24.12 ratifies it:
> - the candidate;
> - the success definition and the two chains;
> - partial days and the shadows;
> - τ and τ_eq, and F1's disclosure;
> - the seeds and the refit schedule.
>
> **4.7T's registered terms do not change in their text.**
> - **Its protocol** (`337a102d…` as revised by `04aac76a…`) names CP-17b's freeze manifest and freeze
>   identity, in the revision's preamble and §3, and the issuing host.
>   - From CP-17c's landing, these read as CP-17c's freeze manifest, its policy identity and the issuing
>     host above.
>   - So do §24.12's rows "The freeze", "Where it landed", "The code", "The freeze origin" and "The check
>     that survives amendment".
>   - **CP-17c's landing record states each value,** and 4.7T's brief cites them from it. No further
>     anchor revision is needed for them.
> - **4.7T still runs on the Owner's Mac,** with no cloud, within 20 machine-hours. The official binary ran
>   the probe's local control at 0.90 times the Homebrew binary's time.
> - **Decision 20's badge and wording stay true under CP-17c.** The protocol's text is unchanged, and the
>   re-freeze also comes before any of the window's data is opened. Any change to them stays the Owner's.
> - **Two frozen sentences on daily operation** are superseded for CP-18 by the publication time below.
>   Neither is one of 4.7T's terms:
>   - the protocol's "It is issued at 11:00 local, before the 12:00 gate. CP-18 fixes the deadline and the
>     late-forecast rule (§24.4).";
>   - CP-17b's freeze record §11, "issued at 11:00 local".
>
> **If CP-17c cannot land before 4.7T opens,** including when its parity fails on the product's runner
> class or on the Owner's Mac:
> - the frozen host and CP-17b's identity stay;
> - 4.7T does not open under either until the Owner decides. Decision 24 reads: "Any other outcome is a
>   new decision, brought to the Owner."

- Worktree clean before and after: yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/cp-17c/critic-1 status --porcelain` was empty and `HEAD` was `548bd0694b7b739df25997074f476bf761041046` before the review and after the last command. The only byproducts inside it are git-ignored `src/*/__pycache__/` folders.

**Why BLOCKED and not PASS or FAIL.** Everything I could check holds, bit for bit, and I found no defect that fails the bar. One required observation does not exist. The brief's item 6 asks for the shadows' buffers over the 14 days, 2026-08-24 to 2026-09-06, on the GitHub-hosted `macos-26` runner. The runner covered 12 of them: 2026-08-30 and 2026-09-06 never ran. The run that would have resumed them (`41040116539`) was refused by GitHub before any step: no runner, no steps, conclusion `failure`, 3 s. Because of that, the runner's final state against CP-17b's, and the stitch between the two blocks, are not shown on the runner either. The brief's "Task-specific supporting extract" covers this case: "If the quota stops the runs before all three are done, return BLOCKED with what was measured. The Orchestrator resumes when the quota resets." The candidate records the gap honestly (`shadow_missing_days`, the freeze record §8, the report) and does not claim the missing days. So this is a check that could not be performed because its source, GitHub's runner, was unavailable. It is not a failure of the candidate. Under the protocol, this BLOCKED cannot support a terminal PASS.

## Commands actually run

Every project Python command (commands 1b–6, 11 and 12) ran with `/Users/djourno/Downloads/PJM/.venv/bin/python` (CPython 3.13.15, zlib 1.2.12), `PYTHONPATH=src`, `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1`, the five `*_NUM_THREADS=1`, and `PYTHONDONTWRITEBYTECODE=1`, from the worktree. Exceptions: `main`'s `gauntlet.py` and `bar.py`, `ci-runner.py` (which drives `uv` offline with Python 3.12.14 in its own scratch copies), and my standard-library hash checks (7–10) ran under the system `python3 -I` or `python3`. Outputs are under `/Users/djourno/Downloads/PJM/.local/artifacts/cp-17c/critic-validation/` (`reruns.out`, `ci-runner.out` and the per-step folders). At most two workers ran at once. Machine time was about 0.6 h, within the 2 machine-hour ceiling. Nothing ran on GitHub, and I made no network contact.

| # | Command | Exit | Observed output |
|---|---|---|---|
| 0 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief cp-17c` | 0 | the 277-line brief this review follows; the assignment hash matched `critic-open` |
| 0a | `git -C <wt> status --porcelain`; `git rev-parse HEAD`; `shasum -a 256 docs/track-b/evidence/cp-17c/issued-brief.md capstone_v21.md` | 0 | empty; `548bd069…`; `5f34f3ab…`, `acdeeab1…` |
| 0b | `git show main:scripts/bar.py \| python3 -I - bar capstone_v21.md "<each heading>" --at 548bd069… --quote` | 0, 0 | the two excerpts above; the identities as stated. The re-freeze section is byte-identical to the generated brief's excerpt |
| 1 | `python3 /Users/djourno/Downloads/PJM/.local/artifacts/cp-17c/ci-runner.py critic 548bd0694b7b739df25997074f476bf761041046 ci312 amended stress` | 0 (each mode 0) | `git archive` of the candidate into a one-commit copy (tree `74e593a9…` = the candidate's tree), offline `uv sync --locked --dev`, Python 3.12.14, `CI=true`, local inputs hidden. **ci312:** `build_wasm_payload.py` 0; `pytest -q` **2547 passed, 48 skipped** (514.5 s); `test_10` 8 passed; `verify_release.py` PASS; `test_22` 15 passed; `publication_guard.py tree` 0; stress collection 19/2594. **amended** (a section appended to `capstone_v21.md` and a new decisions record before the steps): the same seven steps, all 0, **2547 passed, 48 skipped**. **stress** (CI unset, local inputs present): `pytest -m stress -q` **19 passed, 1 skipped**. Each scratch copy was removed. Every skip states its reason (CI-only absences of local material, history, tags, the pinned CPython or `eccodes`; CP-26 supervision tests deferred to local runs) |
| 1b | `python -m pytest tests/cp17c tests/cp17b/test_refreeze.py tests/cp17b/test_records.py -q -rs -p no:cacheprovider --basetemp=critic-validation/pytest-pinned/tmp` (pinned CPython 3.13.15, local inputs present, CI unset) | 0 | `150 passed in 26.50s`, no skip |
| 2a | `python -c 'import platform, zlib, sys; ...'` | 0 | `3.13.15 1.2.12 /Users/djourno/Downloads/PJM/.venv/bin/python` |
| 2b | `cp17.tools.bundle.build(Path('src'), critic-validation/bundle/src.zip)` against the manifest's `code` | 0 | zip `460a94e1…` (91,835 bytes): equal. Package `9a2d961a…`: equal. Files: 34, equal. Pipeline and runner files: equal. `stubbed []`. The Lead's `.local/artifacts/cp-17c/bundle/src.zip`, which the host loads, hashes to the manifest's `zip_sha256` |
| 2c | `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json` | 0 | exactly `verified` |
| 2d | `git archive HEAD` into `critic-validation/amended-tree`. Then I appended `## r20 (a simulated amendment for the Critic)` to `capstone_v21.md` (now `0bf995f5…`), appended a line to `docs/track-b/owner-decisions-2026-10-30.md` (now `a99bc704…`), and added `docs/track-b/owner-decisions-2099-01-01.md`. Then `CP17_PROJECT_ROOT=/Users/djourno/Downloads/PJM python -m cp17.tools.refreeze verify … --root critic-validation/amended-tree` | 0 | exactly `verified` |
| 2e | the same on the amended tree with `CP17_PROJECT_ROOT=critic-validation/no-local-files` (empty) | 0 | `verified, except 28 local runtime or state files absent on this machine (unchecked, not passed)`: the 23 Pyodide files, `bin/node`, `k13.json`, the freeze-origin state and the two canary files. No problem |
| 2f | `refreeze17c.cp17b_superseded(Path('.'))` | 0 | `['src/cp17/schema.py: missing or altered', 'src/cp17/daily.py: missing or altered', "the rebuilt package's files differ …", "… identity differs …", "… zip differs …"]`, equal to `refreeze17c.CP17B_EXPECTED`: True |
| 3 | `python -m cp17c.run checks --out critic-validation/checks` | 0 | `H2 passed` (pins 2.1 s printing `verified`; binary 0.1 s; machine: local Mac, Apple M3; canary 72.3 s, quantiles `4e6abb02…`, attempt `ok`, 873,725,952 B peak). Each forced failure stopped at its own check, ran none after it, and issued nothing. Pins: the one-byte manifest's verify exited 1, listing the content digest, the identity digest and the zip. Binary: `bin/node` was 145,238,561 bytes. Machine: `ImageOS` `macos15`. Canary: `BadZipFile: Bad CRC-32`. The freeze-origin store was initialized and loaded back with buffers B0 `cb08e92c…`, v2 `3eb4770d…`, v4 `511f4334…` (CP-17's) |
| 4 | `python -m cp17c.run parity --payloads /Users/djourno/Downloads/PJM/.local/artifacts/cp-17b/runs/native-parity/payloads --stems A1-2026-03-29 --out critic-validation/parity` | 0 | `H2 passed`; `A1-2026-03-29 ok 83.8s 801 MiB b5ca894f8f99128f`. Quantiles `b5ca894f8f99128fc69ed1b6c6afdaea3fa5d7e05052ae90e70eedd01022cc05`, equal to `reports/cp17b/host-parity.json`'s `issued_quantiles_sha256` for that stem. `node_execpath` was the official binary under `.local/tools/node-v26.7.0-official/`; Pyodide 0.28.0; no non-local request |
| 5 | `python -m cp17.tools.parity --origins 2025-10-26 --out critic-validation/native-parity` | 0 | `2025-10-26 PASS {'A1': True, 'v2': True, 'v4': True, 'v5': True, 'B0': True}`, `PASS 86s`. Checks, payload identities, quantile hashes and ledger hash all equal `reports/cp17b/native-parity.json` at that origin |
| 6a | `python -m cp17c.compare compare --inputs reports/cp17c/inputs.json --artifacts reports/cp17c/artifacts.json --downloads …/cp-17c/downloads --local …/cp-17c/local --tree …/tmp/cp-17c/scratch2 --out critic-validation/measurement.json`; `cmp` | 0 | runner: 50/50 fits bit-identical, 12 shadow days, parity all bit-identical, gates passed. Local: 58/58, 14 days. `measurement byte-equal`, both `9bba1096…` |
| 6b | `python -m cp17c.report --out critic-validation/report.md`; `cmp` | 0 | `report byte-equal` |
| 7 | My own check (Python): each `downloads/<run>/<name>.zip` against `artifacts.json`'s GitHub `digest`, and every zip member against the extracted file | 0 | all six zips matched their digest (`41030551242` checks and shadow-late; `41031373014` checks and shadow-late; `41033064719` shadows). Members equal to extracted files: 9, 9, 23, 10 and 110, with 0 mismatches |
| 8 | My own check: `measurement.json`'s nine parity rows, both machines, against `reports/cp17b/host-parity.json` directly | 0 | 9/9 equal on the runner (2 parity fits, 6 late-block A1 issuances, 1 canary) and 9/9 on the M3 |
| 9 | My own check: every v4, v2 and B0 shadow quantile hash, intake and issued policy in `measurement.json` against `reports/cp17b/shadow-run.json` (host) directly | 0 | 78 comparisons, 0 differences. The M3's late final digest equals `shadow-run.json`'s final `buffers_sha256` |
| 10 | My own check: `src/cp17/**` in the scratch repository's working copy (`32fce099`) against the candidate, file by file; `git -C scratch2 diff --stat <ad3153bb\|aad2e550> 32fce099` | 0 | every `src/cp17` file is identical. Between the commits the runner ran and `32fce099`, `src/cp17` did not change. Only the harness (`src/cp17c/`) and the workflow differ |
| 11 | `records.r7(local, root, /Users/djourno/Downloads/PJM/.local/tmp/cp-17c/old/src)`, with the old `schema.py` hashed against CP-17b's frozen value | 0 | old `schema.py` is CP-17b's frozen file: True. The recomputed `r7-controls.json` equals the committed one: True |
| 12 | `scratchpad/store_head_probe.py` (stand-in states, as `tests/cp17c/test_units.py` builds them) | 0 | `repointed head ACCEPTED by verify(): states/2026-08-24.json 2026-08-24` (finding F1 below) |
| 13 | `shasum -a 256 /opt/homebrew/Cellar/node/26.7.0/bin/node`; `brew list --pinned`; `shasum` of the official binary, tarball and `SHASUMS256.txt` under `.local/tools/node-v26.7.0-official/` | 0 | `1ef99ea2…d040`; `node`; `a9bd0630…`, `7ee659a7…`, `4533f0a4…` |
| 14 | `git diff --name-only adcaf051 HEAD` filtered by the brief's allowed paths; `git diff --stat adcaf051 HEAD -- <the never-change paths>` | 0 | no path outside `src/cp17/`, `src/cp17c/`, `tests/cp17/`, `tests/cp17b/`, `tests/cp17c/`, `reports/cp17c/`, `docs/track-b/evidence/cp-17c/`; nothing under `.github/`; empty for the protected paths |
| 15 | `git diff adcaf051 HEAD` added lines scanned for dates after 2026-09-06 | 0 | only document, ruling, run and calendar dates (`2026-10-xx`, `2027-01-06` S_14, `2026-09-07` as 4.7T's first window day) |
| 16 | `git show main:scripts/bar.py \| python3 -I - check <this verdict> --source capstone_v21.md@548bd069…` | 0 | `ok: lines 7–79 (5645 bytes) appear in capstone_v21.md@548bd0694b7b`; `ok: lines 83–162 (4885 bytes) appear in capstone_v21.md@548bd0694b7b`: both quoted blocks appear byte for byte in the anchor at the candidate |

## Evidence actually inspected

- **The brief** (`issued-brief.md`, all 407 lines) and the candidate's full diff stat: 47 files, 20 commits from `c5bf749a`. That first commit adds only the brief, byte for byte.
- **The freeze:** `freeze-record.md` (all of it); `freeze-manifest.json`, file `ceab4309…2532`, whose identity, content digests and pins are verified by command 2c; `artifact-2026-09-06.json`, file `066064c3…`, artifact `4aedd5e0…`; the four `pinned/` copies. Their hashes equal the brief, the anchor at r19 and the live decisions records `5bf49634…` and `12865483…`.
- **Code read line by line:**
  - the diffs of `src/cp17/schema.py`, `daily.py`, `tools/bundle.py`, `tools/hosts.py` and `tools/refreeze.py`;
  - the new `src/cp17/runtime.py`, `hostcheck.py` and `tools/refreeze17c.py`;
  - `src/cp17c/run.py`, `compare.py`, `store.py`, `state.py`, `inputs.py`, `records.py` and `refreeze.yml`, and `report.py`'s entry;
  - the superseded tests in `tests/cp17/test_hosts.py`, `tests/cp17b/test_records.py` and `tests/cp17b/test_refreeze.py`;
  - the test lists of `tests/cp17c/*`, and the store, measurement, boundary and closure tests in full.
- **Records:**
  - `reports/cp17c/report.md`, `measurement.json` (both summaries, the cost and the minutes), `artifacts.json` (all four runs, their jobs and `head_sha`) and `inputs.json` (boundary, candidate `241722dc`, carried stores);
  - `freeze-origin.json`, `browser.json`, `native-parity.json`, `r7-controls.json`, `state-route.json`, `state-route-proposal.md`, `resume-rehearsal.json`, `retrieval-local.json`, `scratch-repository.json`, `policy-identity.json` (equal to the manifest's identity) and `compute-ledger.jsonl`;
  - each record's cited local source, re-hashed. Equal: `runs/browser-results.json`, `runs/native-parity/native-parity.json`, `freeze/issuance/issuance-2026-09-06.json` and `local-resume-rehearsal/shadow-early/shadow.json`.
- **Local inputs:**
  - the state route's files: `k13.json` `17ade451…`, `freeze-origin-state.json` `1388d74d…`, and the canary `A1-2026-09-06.json` and `.npz`. Each equals the manifest;
  - the runner's downloads (command 7);
  - the scratch working copy's history (command 10);
  - CP-17b's committed `host-parity.json`, `shadow-run.json` and `native-parity.json`. Also CP-17b's cited shadow source `.local/artifacts/cp-17b/runs/shadow-host/shadow-run.json`, whose hash equals the citation `ccbb681e…`.
- **Not opened, by rule:** the Lead's return drafts, logs and notes under `.local/artifacts/cp-17c/` (`return*.md`, `lead-*`, `early-*`, `launch-envelope.md`, `critic-assignment.draft.md`). I did not open the Claude memory directory.
- **Not rerun:** Chromium and WebKit were not in the rerun list. I judged `browser.json` from its record and its re-hashed source.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| O1 | **The re-freeze record** and `freeze-manifest.json`: complete on its own; records the new policy identity, the freeze-origin artifact reissued under the new host, the canary's frozen quantile hash, and every value of §24.12's rows "The freeze", "Where it landed", "The code", "The freeze origin", "The initial state" and "The check that survives amendment"; CP-17b superseded, not edited; governance pinned by frozen copies (anchor r19, brief, decisions 20–21 and 22–25); a later anchor revision leaves `refreeze verify` green | PASS | The record states every change (§1) and carries CP-17b's terms by hash (§7). Its §9 table holds all six rows (plus the issuing host). Identity `720fc581…`; artifact `4aedd5e0…`, quantiles `4e6abb02…`, arrays equal to CP-17b's; canary hash in the identity and the manifest. CP-17b's records are unchanged (empty diff) and re-hashed by the verifier (2c). The four pinned copies' hashes are as cited, and `verify` checks twelve pins. The simulated anchor and decisions change stays `verified` (2d) and has no problem without local files (2e) |
| O2 | **The issuing host, frozen**: the binary by tarball and `bin/node` hashes, retrieved each run with `SHASUMS256.txt` and checked by hash; the binary's path in place of the Homebrew defaults; the Pyodide folder and how the 23 files reach the runner; `refreeze verify` with no problem and no unchecked item on the runner and the Owner's Mac, including the zip under the recorded zlib; the CPython patch pinned without changing `uv.lock` or `pyproject.toml`; where the image version and CPU model are recorded | PASS | **Pins.** `cp17.runtime` pins §24.13's exact bytes and hashes. `retrieve` checks `SHASUMS256.txt`, its listing, the tarball and the extracted `bin/node`, and moves the files into place only after every hash holds; four failure tests. Retrieval records: runner (`measurement.json` host) and M3 (`retrieval-local.json`). **Paths.** `daily.NODE` and `hosts.NODE` name the official binary; my parity run executed it (4). The Pyodide folder is unchanged, and its 23 files reach the runner committed in the private repository (`inputs-verified` 461/463 files). **`refreeze verify`.** The runner printed `verified` (`pins_output`), and so did the M3 (2c). The zip was compared under zlib `1.2.12` on both machines (runner `cpython.json`; 2a, 2b). **CPython.** 3.13.15 is pinned in `cp17.runtime` and required by `verify` on the issuing machine; the runner used the same interpreter `7710b049…`. `uv.lock` and `pyproject.toml` are unchanged. **Machine record.** Image and CPU go in each run's check record: runner `macos26 20261013.0424.1`, Apple M1 (Virtual), 3 cores |
| O3 | **H2 checks frozen as code with tests**: pins, binary, machine (`ImageOS` `macos26`), canary, in that order; any failure issues nothing; for 4.7T a blocker; each check tested failing on its own | PASS | **Code.** `cp17.hostcheck` is in the identity's pipeline files. `gate` stops at the first failure, and `run` calls the issuance only when every check passed. **Tests.** `tests/cp17c/test_units.py` covers each check failing alone, a raising check, issuance only after a pass, the pins check reading the output, and the machine and canary cases. **Runs.** My rerun (3): the gate passed, and four forced failures stopped at their own checks with nothing issued. The runner's and the M3's records (`measurement.json`) show five forced failures, the canary's quantile hash among them. **4.7T.** The blocker rule is stated in the module, the identity and the freeze record |
| O4 | **The states' route** defined and exercised on the runner (`k13.json`, freeze-origin states of v4/v2/B0, shadows' buffers, issued records, canary payload); how each reaches the runner and persists; CP-18's form proposed and exercised across the 14 shadow days | PASS on the definition, the proposal and the M3. BLOCKED on the runner's last 2 of 14 days | **Definition.** Each state is defined by path and hash in the identity (`state_route`) and checked by `verify` (2c, 2e lists them). **On the runner:** `k13.json`, the freeze-origin state and the canary payload were committed and verified; the freeze-origin store was initialized and loaded back; the store carried buffers and issued records for 6 + 6 days, one process per day. **On the M3:** all 14 days, plus the cross-machine resume of the runner's early store (`resume-rehearsal.json`). **The runner's own resume** between runs was refused by GitHub (see O6). **Proposal:** `state-route-proposal.md`. Non-gating finding F1 below |
| O5 | **R7 fixed on its error path only**: a structurally malformed day in a re-hashed issued-forecasts record listed as a fault, not raised; tested; every fit, quantile and artifact field bit-identical | PASS | **The diff.** It changes only `verify_bundle`'s per-day loop and the artifact cross-check's day list; `DAY_ITEM` is the existing schema's item; the schemas are unchanged (test). A well-formed record gives the same list of days and the same messages. **Recomputed (11):** CP-17c lists all six malformed controls, five with the R7 message and `days_not_a_list` through schema validation, as freeze record §4 states. CP-17b's frozen `schema.py` raises on all six. The valid bundle verifies under both, and the negative controls are identical. **Fits unchanged:** native parity (5) and host parity (4) are bit-identical |
| O6 | **The parity, shown.** On the runner and the M3: `refreeze verify` clean; host parity at the nine origins bit for bit; the shadows' buffers over the 14 days against `reports/cp17b/shadow-run.json`; the H2 checks passing with one forced failure each; timing and peak memory per fit against 15 min and 4 GB. On the M3 only: native parity five policies × nine origins; Chromium and WebKit at the freeze origin | **BLOCKED** (the runner's 14-day shadows); every other part PASS | **`verify` and H2:** clean on both machines (runner `pins_output` `['verified']`, all forced failures as expected; M3 2c and 3). **Host parity:** recomputed (6a) and checked directly against `host-parity.json`, 9/9 on each machine (8). On the runner the ninth origin is the canary on the parity payload, payload identity checked. **Shadows:** the M3 shows all 14 days, the final state equal to CP-17b's and the stitch. **The runner shows 12:** 2026-08-30 and 2026-09-06 are missing because run `41040116539` was refused before any step, so the runner's final state and stitch are not shown. 78/78 shadow quantile hashes match `shadow-run.json` directly (9). **Ceilings:** worst fit 231.9 s on the runner and 157.1 s on the M3; peak 968,884,224 B and 979,763,200 B. **Native parity:** recorded PASS 5×9, equal to CP-17b's; my rerun at 2025-10-26 is PASS and equal (5). **Browsers:** Chromium 153.0.8010.12 and WebKit 26.6 give `4e6abb02…` on zip `460a94e1…` (record and source hash) |
| O7 | **The cost** on the scratch repository's `macos-26`, from the shadow run's sequential issuances: one issuance, and decision 23's four with the canary | PASS (with a note) | **Runner:** one issuance median 431.8 s (404.5–489.3, n = 12); four issuances with the canary median 1,887.8 s (1,849.0–1,923.2, n = 6). **M3:** 239.7 s and 1,046.0 s. The issuances in each block ran one after another, but the two blocks ran at once on 3 vCPUs, so the figures are conservative. "One issuance, alone" is recorded as not measured |
| O8 | **The values 4.7T's brief cites**, in one table | PASS for the candidate | Freeze record §9 holds the table, with every value checked above. The return itself is outside this review (`scripts/gauntlet.py return`) |
| F1 | **Blind**: boundary 2026-09-06; no later byte downloaded, read or inferred, here or on a runner; no 4.7T forecast | PASS | `cp17c.inputs.boundary` runs `cp25.guard` (fail closed) over the shipped snapshot rows (67,343), weather rows (59,446) and prices (336), and every payload day; recorded in `inputs.json`. Only payloads and states through 2026-09-06 were shipped. The added lines carry no post-boundary data date (15). No 4.7T issuance exists in the candidate |
| F2 | **GitHub-landable**: no committed file over 50 MB | PASS | The largest added file is `pinned/anchor-capstone-v21-r19.md`, 342,690 bytes; the largest file in the tree is 30,830,306 bytes and predates this round. The scratch tree's largest file was 20,230,545 bytes |
| F3 | **CI-ready**: the seven steps green on a history-free single-commit copy with `CI=true`, Python 3.12, and `pytest -m stress` locally; no test depends on history, tags or local-only inputs; tests over local inputs skip with a stated reason | PASS | **History-free CI** (command 1): the seven steps were green, with 2547 passed and 48 skipped, both as built and after a simulated anchor amendment. The stress run passed: 19 passed, 1 skipped. **Skips.** Every skip has a stated reason tied to absent local material, history or tags; the CP-17c tests that need local inputs skip with "local only" or "not the pinned CPython". **With those inputs present** under the pinned CPython 3.13.15 (command 1b), `tests/cp17c`, `tests/cp17b/test_refreeze.py` and `tests/cp17b/test_records.py` gave 150 passed and 0 skipped, including the real-local-files verify and the measurement recomputed from the downloads |
| F4 | **What may change**: `src/cp17/` with every change listed; `tests/cp17/` and `tests/cp17b/` only where superseded, listed; new files under `tests/cp17c/`, `reports/cp17c/`, `docs/track-b/evidence/cp-17c/`; harness under `src/cp17c/`; nothing under `.github/` | PASS | **Paths.** Every changed path is in the allowed set, and none is under `.github/` (14). **Package changes.** Every `src/cp17/` change, with its reason, is in freeze record §1. **Supersessions.** Seven tests in `tests/cp17b/` and the `stress` fixture in `tests/cp17/test_hosts.py` are listed in §11, and their diffs match that list. **The workflow** is kept at `src/cp17c/refreeze.yml` |
| F5 | **What never changes** (earlier reports and evidence, landed code, `data/`, development inputs, root `pyproject.toml` and `uv.lock`, anchors, decisions, `AGENTS.md`, role files, exposure ledger, backup register); no earlier evidence binds an edited file's bytes | PASS | **Protected paths.** The diff over all of them is empty (14). **Earlier bindings.** The edited files appear in earlier evidence only as cited paths, not byte pins. `tests/cp17cprobe/test_probe.py:111` compares two committed records, not the live `daily.py`. `src/cp26/harness.py`'s `PINS` names none of them. CP-17b's verifier reports exactly the declared set (2f) |
| F6 | **The Critic's reruns** (suite and stress; `verify` on the new manifest and after a simulated anchor change; H2 with one forced failure; host parity at one origin; native parity at one DST origin; every runner comparison recomputed from the hash-verified downloads; nothing on GitHub) | PASS | Commands 1–7 above, each with its exit code and output |
| C1 | **The red line (§24.2)** | PASS | As F1. `tests/cp17c/test_records.py::test_no_committed_record_holds_a_date_after_the_boundary` ran in the suite |
| C2 | **Homebrew's `node` stays pinned and installed** | PASS | Command 13: installed at `26.7.0`, hash `1ef99ea2…`, listed by `brew list --pinned` |
| C3 | **Credentials** (`AGENTS.md`); no secret created; MLflow telemetry off | PASS | **Scratch repository** (`scratch-repository.json`): private, 0 secrets, 0 variables, default workflow permissions `read`. **Workflow:** `permissions: contents: read`, `persist-credentials: false`, no `secrets.` reference, `MLFLOW_DISABLE_TELEMETRY` and `DO_NOT_TRACK` set. **Code:** the changed code reads no credential and prints no environment |
| C4 | **Long computation within the ceilings, under a ledger; WIP commits at every stage boundary**; GitHub within 1,000 counted minutes, standard `macos-26` only, no paid usage | PASS (with a note) | **Local:** `compute-ledger.jsonl` holds 14 entries, about 2.2 machine-hours summed, at most 4 workers at once. **Commits:** 20 WIP commits. **GitHub:** 660 minutes counted from job times, 820 if queued time counted, both under 1,000; standard `macos-26` only; the runs stopped at GitHub's billing refusal. Note: the timing API's `billable` was empty for every run (`counted_from_billable` 0), so the count is the job-time count, not GitHub's own usage report |
| C5 | **Tools**: `gauntlet.py start` first; the Lead worktree; one Critic through `critic-open`/`critic-brief`/`critic-close`, its first line forbidding the memory directory; `gauntlet.py return` | PASS for what exists now | `.local/artifacts/cp-17c/start.json` records `main` = `adcaf051…`. `.local/worktrees/cp-17c/lead` exists. `critic-open.json` holds one record, `n` 1, at this SHA. The assignment's first line is the memory rule. `critic-close` and `return` come after this verdict |
| C6 | **Memory**: the Claude memory directory not opened or edited | Not checkable from the artifact | No trace of it in the candidate. I did not open it |
| C7 | **Owner-facing Git commands non-interactive** | Not exercised by the candidate | The candidate gives the Owner no Git command. LAND commands come from `scripts/gauntlet.py land-commands` |

## What blocks, and the test that clears it

- **The single gap:** the runner's shadow coverage is 12 of 14 days. Missing: 2026-08-30 (early block) and 2026-09-06 (late block), with the runner's final state against CP-17b's and the stitch between the blocks. GitHub refused run `41040116539`, which would have resumed both from the stores run `41033064719` left (committed in the scratch repository at `states/store-<block>/`, scratch commit `32fce099`).
- **The exact next acceptance test**, once the Orchestrator reports the quota reset:
  1. Dispatch the scratch repository's `resume` job once (input `{"include": [{"kind": "resume", "minutes": …}]}`), within the remaining minutes.
  2. Fetch its artifact with `cp17c.compare fetch` and check its zip against GitHub's digest.
  3. Recompute `cp17c.compare compare`, with `_chosen` now reading `resume`.
  4. **It passes when** the runner's summary shows `shadow_days` 14, `shadow_missing_days` [], `late_final_equals_reference_final` true, `stitch_early_final_equals_late_start` true, `carried_store_equal_to_the_first_runs` true for both blocks, the resume's own H2 gate passed, and every fit bit-identical within 900 s and 4 GiB.
  5. Re-render `measurement.json` and `report.md`, and update `tests/cp17c/test_records.py`'s `RUNNER_MISSING` expectation and the freeze record's §8 bullet.
- That is a new candidate SHA, so it needs a fresh Integration review.

## Findings that do not gate this verdict

- **F1, the state store's head is not bound to its ledger** (`src/cp17c/store.py`, outside the identity; the form proposed for CP-18).
  - **The gap.** `Store.verify()` checks every entry's hash, the chain, every state, artifact and record file, and that `head.json` names the last entry's `entry_sha256` and the entry count. It does not check that `head.json`'s `state_file`, `state_sha256`, `last_day` and `last_artifact_sha256` are the last entry's.
  - **Shown (command 12):** a 3-day store whose `head.json` was repointed at the intact `states/2026-08-24.json` and that day's artifact is accepted. `state()` would then load 2026-08-24's states, and `last_artifact_sha256()` would return 2026-08-24's artifact as the next day's parent, while the ledger's last day is 2026-08-26.
  - **Why it does not gate here.** Every store in this round was written by the code and never edited, and every day's buffers were checked against CP-17b's references. Freeze record §6 and the store's docstring nonetheless say loading "checks everything".
  - **Suggested fix**, before CP-18 builds persistence on it: in `verify`, require those four head fields to equal the last entry's (`last_day` and `last_artifact_sha256` from the last issuance entry), and in `state()`, check the loaded state's `digest()` against `state_sha256`.
- **F2, the billing refusal's wording is not in a record.** The quoted refusal ("recent account payments have failed…") is a literal in `src/cp17c/report.py`. `artifacts.json` records only the job's `failure`, 3 s, no runner and no steps, which is consistent with a refusal before any step. Consider fetching the check-run annotation into a record, since the report says "every figure is in a record".
- **F3, the runner ran earlier harness revisions.** It ran the scratch repository's commits `ad3153bb` (checks) and `aad2e550` (shadows). Their `src/cp17c/run.py`, `inputs.py` and workflow differ from the candidate's: the `resume` job came later. The frozen package, its pipeline files and its tools on the runner are byte-identical to the candidate's (command 10), and the runner's own `refreeze verify` confirmed the identity. The harness is outside the identity, so this does not affect the bar.
