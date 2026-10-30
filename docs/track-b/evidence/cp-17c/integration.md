# Verdict — CP-17c — Integration — PASS

- Candidate SHA: `a248455542329059b8b8cc062e707d838348e9f9` (branch `gauntlet/cp-17c`, base `main` = `adcaf051560bbeebec9065e848bcc1cbab3939fe`)
- Plan / version / bar: `capstone_v21.md`, v21-r19, SHA-256 `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e` (unchanged between the base and the candidate). §24.13, "What CP-17c re-freezes, and what 4.7T then tests" (the controlling section: 80 lines, 4,886 bytes, SHA-256 `adee5cff2146948b0aac8c2d2b1cf69615db59db57bc87682ae6f5af4a980263`), read with "The issuing host (decision 24; H1)" (73 lines, 5,646 bytes, `6eacad578ebbded76cc978cb1ef839e024089b28e532e17eb0cd88da50f24d1e`). The checklist is the brief `docs/track-b/evidence/cp-17c/issued-brief.md` (`5f34f3ab298cfa619ddefaa9b1dcfd5df207c73a0ae06cbf8ed30454ac559c7d`).
- Verbatim bar excerpt (both sections, extracted at the candidate by `main`'s `scripts/bar.py bar … --at a2484555… --quote`, and checked against the anchor at the candidate by `bar.py check`):
  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)

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

- Worktree clean before and after: yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/cp-17c/critic-2 status --porcelain` was empty and `HEAD` was `a248455542329059b8b8cc062e707d838348e9f9` at the start, midway, and after the last command. I ran Python there with `PYTHONDONTWRITEBYTECODE=1` and pytest with `-p no:cacheprovider`, and wrote every output under `/Users/djourno/Downloads/PJM/.local/artifacts/cp-17c/critic2-validation/`.

**Why PASS.** The one gap that held the first review at BLOCKED is closed, by that review's own acceptance test, and I recomputed each part of it from GitHub's hash-checked artifacts. The runner now shows all 14 shadow days, with `shadow_missing_days` empty. Its final state equals CP-17b's. The early block ends in the state the late block starts from. Each block's store, as the repository carried it, is byte-identical to what the first run left. The resume run passed its own H2 gate, and all 58 fits are bit-identical, within 900 s and 4 GiB. My reruns of everything the brief names for the Critic pass, and `measurement.json` and `report.md` recompute byte for byte.

The repair changes no file of the frozen package, its manifest or its identity. It touches only the harness (`src/cp17c/compare.py`, `report.py`, `store.py`), tests, records and evidence. I reviewed the whole candidate again, not only the repair, and found no defect that fails the bar.

**The Owner's decision 26.** The brief said the scratch repository "is never made public", and r19 §24.13 gives a reason for a private repository. The candidate states the deviation and its effect honestly:
- what changed, and when (14:21 UTC);
- which runs ran on which class: runs 1 to 4 private, 5 and 6 public;
- that this departs from §24.13's reason for a private class;
- what became public with the repository, A1's search state among it;
- that the public runs' minutes are recorded and counted as zero;
- that the resume's two issuances alone are a first public-class measurement, not CP-18's.

I checked each factual claim it makes against the records, and found three wording slips, none of which changes a figure. They are listed under the non-gating findings. Whether the Owner may make that ruling is outside this review.

## Commands actually run

**How they ran.**
- **Python and the environment.** Every project Python command (2–6, 11, 13, 14) ran with `/Users/djourno/Downloads/PJM/.venv/bin/python` (CPython 3.13.15, zlib 1.2.12) and `PYTHONPATH=src`, from the worktree. It had `MLFLOW_DISABLE_TELEMETRY=true`, `DO_NOT_TRACK=1`, the five `*_NUM_THREADS=1` and `PYTHONDONTWRITEBYTECODE=1`.
- **The exceptions.** `main`'s `gauntlet.py` and `bar.py`, my standard-library checks (7–10, 12, 15–19) and `ci-runner.py` ran under the system `python3 -I` or `python3`. `ci-runner.py` drives `uv` offline with Python 3.12.14 in its own scratch copies, and removes each copy afterwards.
- **Where the outputs are.** Under `/Users/djourno/Downloads/PJM/.local/artifacts/cp-17c/critic2-validation/`.
- **Ceilings.** At most two workers ran at once: the CI sequence plus one other command. Machine time was about 0.6 h (the CI sequence 15:10:46Z–15:38:41Z, plus about 8 minutes of other reruns), within the 2 machine-hour ceiling.
- **No network.** Nothing ran on GitHub, and I made no network contact.

| # | Command | Exit | Observed output |
|---|---|---|---|
| 0 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief cp-17c` | 0 | the assignment this review follows. `critic-open.json` holds record `n` 2 at this SHA, assignment `2ac1ba0e…`, the hash of `.local/artifacts/cp-17c/critic-assignment-2.md` |
| 0a | `git -C <wt> status --porcelain`; `git rev-parse HEAD`; `shasum -a 256` of the brief and `capstone_v21.md`, at the candidate and at `adcaf051` | 0 | empty; `a2484555…`; `5f34f3ab…`; `acdeeab1…` at both commits |
| 0b | `git show main:scripts/bar.py \| python3 -I - bar capstone_v21.md "<each heading>" --at a2484555… [--quote]` | 0, 0 | the two excerpts above, with the identities stated in the header. The controlling section is byte-identical to the generated assignment's excerpt (`adee5cff…`) |
| 1 | `python3 /Users/djourno/Downloads/PJM/.local/artifacts/cp-17c/ci-runner.py critic2 a248455542329059b8b8cc062e707d838348e9f9 ci312 amended stress` | 0 (every step 0) | Each mode starts from a `git archive` of the candidate as a one-commit copy, tree `e0f1f7cd…` (the candidate's tree). It runs offline `uv sync --locked --dev` under Python 3.12.14, with `CI=true` and the local inputs hidden. **ci312:** `build_wasm_payload.py` 0; `pytest -q` **2550 passed, 48 skipped** (535.0 s); `test_10` 8 passed; `verify_release.py` PASS; `test_22` 15 passed; `publication_guard.py tree` 0; stress collection 19/2597. **amended** (a section appended to `capstone_v21.md` and a new decisions record added, before the steps): the same seven steps, all 0, **2550 passed, 48 skipped** (515.1 s). **stress** (CI unset, local inputs present): `pytest -m stress -q` **19 passed, 1 skipped** (403.9 s; the skip is the `eccodes` import skip that the stress collection step also shows). Every skip states its reason. The reasons are CI-only absences: local material, history, tags, the pinned CPython, the browsers or `eccodes`; the CP-26 supervision tests run locally; and CP-16's anchor binding. The scratch copies were removed |
| 1b | `python -m pytest tests/cp17c tests/cp17b/test_refreeze.py tests/cp17b/test_records.py -q -rs -p no:cacheprovider --basetemp=critic2-validation/pytest-pinned/tmp` (pinned CPython 3.13.15, local inputs present, CI unset) | 0 | **153 passed** in 27.7 s, 0 skipped. This includes the new `repointed_head` store control, the minutes-by-repository test, `test_the_runner_carried_its_stores_between_runs`, and `test_the_measurement_recomputes_from_the_downloaded_results` |
| 2a | `python -c 'import platform, zlib, sys; …'` | 0 | `3.13.15 1.2.12 /Users/djourno/Downloads/PJM/.venv/bin/python` |
| 2b | `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json` | 0 | exactly `verified` (manifest file `ceab4309…2532`) |
| 2c | Build `critic2-validation/amended-tree` with `git archive HEAD \| tar -x`. Append `## r20 (a simulated amendment for the second Critic)` to `capstone_v21.md` (now `4adedff0…`) and a line to `docs/track-b/owner-decisions-2026-10-30.md` (now `b1704076…`), and add `docs/track-b/owner-decisions-2099-01-01.md`. Then run `CP17_PROJECT_ROOT=/Users/djourno/Downloads/PJM python -m cp17.tools.refreeze verify <amended>/…/freeze-manifest.json --root <amended>` | 0 | exactly `verified` |
| 2d | the same on the amended tree with `CP17_PROJECT_ROOT=critic2-validation/no-local-files` (empty) | 0 | `verified, except 28 local runtime or state files absent on this machine (unchecked, not passed)`: the 23 Pyodide files, `bin/node`, `k13.json`, the freeze-origin state and the two canary files. No problem |
| 2e | negative control on a further copy, `negative-tree`: one byte appended to `src/cp17/hostcheck.py` and to `pinned/owner-decisions-2026-10-30.md`, then the same verify | 1 | `…/pinned/owner-decisions-2026-10-30.md: the frozen governance copy is missing or altered`; `src/cp17/hostcheck.py: missing or altered` |
| 2f | `refreeze17c.cp17b_superseded(Path('.'))`; and `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17b/freeze-manifest.json` | 0; 1 | The function returns the five declared lines (`schema.py`, `daily.py`, and the rebuilt files, identity and zip). They equal `refreeze17c.CP17B_EXPECTED`: `True`. The CLI prints the same five lines |
| 3 | `python -m cp17c.run checks --out critic2-validation/checks` | 0 | `H2 passed` in 88 s. Pins 2.3 s, `['verified']`. Binary 0.1 s. Machine: `local Mac`, Apple M3. Canary 75.3 s, quantiles `4e6abb02…a5`, attempt `ok`, wall 75.0 s, peak 883,884,032 B, under the official binary. Each forced failure stopped at its own check, ran none after it, and issued nothing: pins (`refreeze verify (exit 1)…`), binary (`bin/node` 145,238,561 bytes), machine (`ImageOS 'macos15'`) and canary (`BadZipFile: Bad CRC-32`). The freeze-origin store was initialized and loaded back with CP-17's buffers B0 `cb08e92c…`, v2 `3eb4770d…` and v4 `511f4334…` |
| 4 | `python -m cp17c.run parity --payloads /Users/djourno/Downloads/PJM/.local/artifacts/cp-17b/runs/native-parity/payloads --stems A1-2026-03-29 --out critic2-validation/parity` | 0 | `H2 passed`; `A1-2026-03-29 ok 85.8s 835 MiB b5ca894f8f99128f`. The quantiles `b5ca894f8f99128fc69ed1b6c6afdaea3fa5d7e05052ae90e70eedd01022cc05` equal `reports/cp17b/host-parity.json`'s `issued_quantiles_sha256` for that stem. `node_execpath` is the official binary, Pyodide is 0.28.0, and no non-local request was made |
| 5 | `python -m cp17.tools.parity --origins 2025-10-26 --out critic2-validation/native-parity` | 0 | `2025-10-26 PASS {'A1': True, 'v2': True, 'v4': True, 'v5': True, 'B0': True}`, `PASS 91s`. Its checks, payload identities, quantile hashes and ledger hash each equal `reports/cp17b/native-parity.json` at that origin |
| 6a | `python -m cp17c.compare compare --inputs reports/cp17c/inputs.json --artifacts reports/cp17c/artifacts.json --downloads …/cp-17c/downloads --local …/cp-17c/local --tree …/tmp/cp-17c/scratch2 --out critic2-validation/measurement.json`; `cmp` | 0 | runner: 58/58 bit-identical, 14 shadow days, gates `checks`/`late`/`early` passed. Local: the same. **Byte-equal**: both `ec2fe9e78f6bc46e8509e300658df429123d26e64a62e5734192d76d138a5d3b` |
| 6b | `python -m cp17c.report --out critic2-validation/report.md`; `cmp` | 0 | **byte-equal** to `reports/cp17c/report.md` |
| 7 | My own check (`scratchpad/zipcheck.py`): each `downloads/<run>/<name>.zip` against `artifacts.json`'s GitHub `digest` and size, every zip member against the extracted file, and every line of each job's `results-sha256.txt` | 0 | All six zips match their digest. Members equal to extracted files: 9, 9, 10, 23, 110 and 72 (the resume), with 0 mismatches. Every listed result hash holds, except two lines in `41031373014/checks`. Those two are the forced binary check's scaffolding under `checks/forced/project/.local/…` (a tarball copy and the altered `bin/node`). `upload-artifact` leaves hidden paths out, and `compare.HIDDEN_EXCLUDED` names exactly those |
| 8 | My own check: `measurement.json`'s nine parity rows on each machine against `reports/cp17b/host-parity.json` directly | 0 | 9/9 equal on the runner and 9/9 on the M3. The runner's 2026-09-06 now comes from the resume's late-block issuance (`4e6abb02…`, 127.2 s, 865,976,320 B), not from the canary |
| 9 | My own check (`scratchpad/shadowcheck.py`): every runner day's record (run 3's store for the 12 days it reached, the resume's store for 2026-08-30 and 2026-09-06), and every M3 day. Each against `reports/cp17b/shadow-run.json` (v4, v2 and B0 quantile and central hashes, intakes, issued policy, display) and against CP-17b's cited source `…/cp-17b/runs/shadow-host/shadow-run.json` (`ccbb681e…`, buffers per day). I also asserted every fit's ceiling | 0 | 14 days on each machine: **532 comparisons, 0 differences**. The resume stores' copies of the 12 carried days' records equal run 3's |
| 10 | `diff -rq` of the scratch tree's `states/store-<block>` against run 3's uploaded `shadow-<block>/store`, for both blocks; the stores' genesis and last ledger entries | 0 | Both are identical: the store GitHub carried is the store run 3 left. **Stitch:** the late store's genesis state file `73c6aede…` is the early block's 2026-08-30 state file `73c6aede…`, digests B0 `79725edc…`, v2 `80979162…` and v4 `2899c177…`. **Final:** the late store's 2026-09-06 state is B0 `cb08e92c…`, v2 `d2def77c…` and v4 `0f79714e…`, equal to `shadow-run.json`'s `final.buffers_sha256`. Each store's artifact-parent chain is intact over its seven issuances |
| 11 | Reading the resume's own records: `41071696187/resume/checks.json`, `cpython.json`, `node-retrieval.json`, `package.json`, `inputs-verified.json`, `project-sha256.txt` | 0 | gate `passed`, order pins, binary, machine, canary. Pins `['verified']`. Binary `a9bd0630…`, tarball `7ee659a7…`, retrieved with `SHASUMS256.txt` `4533f0a4…`. Machine: GitHub-hosted runner, `macos26` `20261013.0424.1`, Apple M1 (Virtual), 3 cores, 7 GiB. Canary `4e6abb02…` in 136.0 s, 769,146,880 B. CPython 3.13.15 `7710b049…`, zlib 1.2.12. Package zip `460a94e1…`, equal to the manifest. Inputs: 505 files verified. `uv.lock` `5d2aecc3…` and `pyproject.toml` `aa35326a…` |
| 12 | `git -C …/tmp/cp-17c/scratch2 rev-parse HEAD; status; log`; `diff -rq` of `src/cp17`, `src/cp17c` and the workflow against the candidate; every file against `inputs-files.json`; file names scanned for dates | 0 | HEAD `32fce099…`, clean. `src/cp17` is identical, and so are `src/cp17c/run.py`, `inputs.py` and the workflow. `compare.py`, `records.py`, `report.py` and `store.py` differ (local-only tools, and the store before the F1 fix). 505/505 files match `inputs-files.json` (`49d6fcb7…`, as `inputs.json` records). The largest is `k13.json`, 20,230,545 bytes. File-name dates after 2026-09-06 are document dates only |
| 13 | `scratchpad/store_probe.py`: the resume's two real stores, loaded with the candidate's `cp17c.store`. Then `head.json` fully repointed (state file, state digest, day and artifact) to the previous issuance | 0 | Both real stores verify, and `state()`'s digest equals the head. Each repointed head is **refused**: `head.json names another state, day or artifact than the ledger's last entry` |
| 14 | `records.r7(…/cp-17c, Path('.'), …/tmp/cp-17c/old/src)` | 0 | The old `schema.py` is `a53006e0…`, CP-17b's frozen file. The recomputed `r7-controls.json` equals the committed one: `True`. CP-17c lists all six, CP-17b raises on all six, the valid bundle verifies under both, and the negative controls are equal |
| 15 | `shasum -a 256` of Homebrew's `node`, the official `bin/node`, tarball and `SHASUMS256.txt`; `brew list --pinned` | 0 | `1ef99ea2…d040`; `a9bd0630…`; `7ee659a7…`; `4533f0a4…`; `node` pinned |
| 16 | `git diff --name-only adcaf051 HEAD`, filtered by the brief's allowed paths; `git diff --stat adcaf051 HEAD -- <the never-change paths, governance, .github>`; base hashes of every edited file grepped across the base tree | 0 | No path is outside the allowed set, and nothing is under `.github/`. The protected-path diff is empty. The old bytes of `daily.py` and `schema.py` are pinned only by CP-17b's manifest and bundle record, the anchor's text, and `reports/cp17c-probe/inputs.json`, which records the probe's inputs and is not re-read against the live tree. The other edited files are pinned nowhere |
| 17 | `git diff adcaf051 HEAD` added lines scanned for dates after 2026-09-06, by file; `measurement.json` and `report.md` scanned in full | 0 | Only document, ruling, run and calendar dates, plus the R7 control `2026-13-45`. In `measurement.json` and `report.md`, the only such dates are decision 26's switch time (`2026-10-30T14:21:00Z`, and `2026-10-30` in prose) |
| 18 | `shasum -a 256` of `pinned/*`, `issued-brief.md`, the live anchor and decisions records, `artifact-2026-09-06.json`, `freeze-manifest.json`; `cmp` of the brief with `.local/artifacts/cp-17c/issued-brief.md`; the first commit's stat; the committed `integration.md` against Critic 1's file | 0 | The pinned copies equal the anchor at r19, the brief and the live decisions records (`5bf49634…`, `12865483…`). The brief is byte-equal to the canonical one. The first commit `c5bf749a` adds only the brief. `c860d986` adds only the first verdict, byte-equal to `critic-1/integration.md` (`3108f972…`) |
| 19 | `reports/cp17c/compute-ledger.jsonl` summed, and its intervals overlapped | 0 | 19 entries, 3.5 machine-hours (wall × workers). At most 4 measured entries overlap (09:18:53Z). See finding N5 |
| 20 | `git show main:scripts/bar.py \| python3 -I - check /Users/djourno/Downloads/PJM/.local/artifacts/cp-17c/critic-2/integration.md --source capstone_v21.md@a248455542329059b8b8cc062e707d838348e9f9` | 0 | `ok: lines 8–80 (5645 bytes) appear in capstone_v21.md@a24845554232`; `ok: lines 84–163 (4885 bytes) appear in capstone_v21.md@a24845554232`. Both quoted blocks appear byte for byte in the anchor at the candidate |

## Evidence actually inspected

- **The assignment and the brief** (`issued-brief.md`, all 407 lines), `AGENTS.md`, and the candidate's full diff stat (49 files, 22 commits from `adcaf051`). I also read the repair diff `548bd069..a2484555` in full for code, tests and prose: 14 files.
- **The previous verdict** (`integration.md` at the candidate): its BLOCKED gap, its acceptance test, and its findings F1–F3.
- **The freeze record and manifest.**
  - `freeze-record.md`, all of it, including the changed §8;
  - `freeze-manifest.json`'s identity `720fc581…`, recomputed from the canonical identity, and its state route;
  - `policy-identity.json`, equal to the manifest's identity;
  - `artifact-2026-09-06.json` `066064c3…`;
  - the four `pinned/` copies, hashed;
  - `owner-decision-26-as-relayed.md`, all of it.
- **Code read line by line:**
  - the diffs of `src/cp17/schema.py`, `daily.py`, `tools/bundle.py`, `tools/hosts.py` and `tools/refreeze.py`;
  - the whole of `src/cp17/runtime.py` and `hostcheck.py`, and `tools/refreeze17c.py`'s `verify`, `issuing_machine` and `cp17b_superseded`;
  - `src/cp17c/store.py` (whole), `compare.py` (fetch, minutes, `_hashes`, `checks_part`, `machine_part`, `cost`, `compare`, `_chosen`), `run.py` (`_gate`, `forced`, `parity_fits`, `day`, `resume`), `records.py`'s `r7` and `native_parity`, `report.py`'s render changes, `refreeze.yml` (whole), and the headers of `inputs.py` and `state.py`;
  - the superseded tests' diffs in `tests/cp17/test_hosts.py`, `tests/cp17b/test_records.py` and `tests/cp17b/test_refreeze.py`;
  - `tests/cp17c/test_records.py` (whole), and in `test_units.py` the R7, store and minutes tests and the test list. I also read `test_refreeze17c.py`'s test list.
- **Records:**
  - `report.md` (whole);
  - `measurement.json`: both summaries, every shadow block's parts, gates and machines, the cost and the minutes;
  - `artifacts.json`: all six runs, their jobs, steps, annotations, `head_sha`, billable and artifacts;
  - `scratch-repository.json`, `state-route-proposal.md`, `compute-ledger.jsonl`, `r7-controls.json`, `browser.json`, `native-parity.json`, `freeze-origin.json`, `resume-rehearsal.json`, `retrieval-local.json`, and `inputs.json` (boundary, candidate, references, file-list hash).
- **Each record's cited local source, re-hashed, all equal:**
  - `runs/browser-results.json` `b4193ad6…`;
  - `runs/native-parity/native-parity.json` `afcf3d68…`;
  - `freeze/issuance/issuance-2026-09-06.json` `93bc6165…`;
  - `local-resume-rehearsal/shadow-early/shadow.json` `1432707e…`;
  - CP-17b's `runs/shadow-host/shadow-run.json` `ccbb681e…`.

  `inputs.json`'s four CP-17b report hashes (`f1`, `host_parity`, `partial_days`, `shadow_run`) equal the committed reports, and its 14 per-day buffer references equal CP-17b's cited source.
- **The runner's downloads:**
  - all six artifacts (command 7);
  - the resume's `checks.json`, `shadow-<block>/shadow.json`, the stores' `head.json` and `ledger.jsonl`, and the issued records of 2026-08-30 and 2026-09-06 with their four `run.json` files.
- **The scratch tree** at `32fce099` (commands 10 and 12). **The M3's stores** under `.local/artifacts/cp-17c/local/shadow-<block>/store/` (command 9).
- **Not opened, by rule:** the Lead's return and drafts, logs and notes under `.local/artifacts/cp-17c/`. That covers `return*.md`, `lead*`, `early-*`, `launch-envelope.md`, `critic-assignment*.md` beyond hashing the second, and `run5-*`. I did not read `progress.md`, and I did not open the Claude memory directory.
- **Not rerun:** Chromium and WebKit, which are not in the rerun list. I judged `browser.json` from its record and its re-hashed source.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| G | **The first review's gap, by its own acceptance test.** The runner's summary shows `shadow_days` 14, `shadow_missing_days` [], `late_final_equals_reference_final` true, `stitch_early_final_equals_late_start` true, and `carried_store_equal_to_the_first_runs` true for both blocks. The resume's own H2 gate passed. Every fit is bit-identical within 900 s and 4 GiB. `measurement.json` and `report.md` are re-rendered, and `RUNNER_MISSING` and freeze record §8 are updated | PASS | **The summary (6a)** reads exactly so, and I recomputed it byte for byte. **Independently:** the final state and the stitch (10); the carried stores against run 3's (10, by `diff -rq`, and in `compare` by hash and ledger prefix); and the resume gate (11: pins `verified`, `macos26`, canary `4e6abb02…`). All 58 fits are bit-identical: the worst wall is 231.9 s and the worst peak 968,884,224 B on the runner. The resumed days were A1 145.3 s and 127.2 s, at most 865,976,320 B, with every shadow ≤ 134.3 s and ≤ 950,059,008 B. **Records:** the zip is checked against GitHub's digest (7). The test drops `RUNNER_MISSING` and now asserts 14 days on both machines, and §8 is rewritten. The resume was dispatched twice: run 5 failed at checkout (403 annotations, no step past checkout), and run 6 succeeded. Each run's `head_sha` is `32fce099` |
| PF1 | The store's head bound to its ledger (`src/cp17c/store.py`), with a test | PASS | `verify` now requires `state_file`, `state_sha256`, `last_day` and `last_artifact_sha256` to equal the ledger's last entry and last issuance. `state()` checks the loaded digest. `test_a_tampered_store_is_refused[repointed_head]` passes (1b). My probe (13) on the runner's real stores: they verify, and a fully repointed head is refused. The runner itself ran the store module from before this fix (12), and the fixed `verify` accepts every store it wrote (6a, 13) |
| PF2 | GitHub's check-run annotations recorded in `reports/cp17c/artifacts.json` | PASS | Each non-success job carries `annotations`. That includes run `41040116539`'s billing refusal, verbatim, run `41033064719`'s 50-minute limit, and run `41071149787`'s three 403s. `report.py`'s literal quote now renders only when days are missing, which they are not |
| PF3 | The runner ran earlier harness revisions (stated in the return) | Holds; the return is outside this review | All three runs read for the comparison ran scratch commits whose `src/cp17` is byte-identical to the candidate's. The resume's commit `32fce099` also has the candidate's `run.py`, `inputs.py` and workflow (12). Its `store.py` predates PF1's fix, which is harmless (PF1). I did not read the return |
| D26 | **The Owner's decision 26:** the candidate states the deviation (scratch repository made public, against the brief's "is never made public" and §24.13's reason for a private class) and its effect honestly | PASS, with wording notes N1–N3 | **Stated in** `owner-decision-26-as-relayed.md`, freeze record §8, `report.md` (runner table by run and repository), `state-route-proposal.md` (its CP-18 consequence is left to the Owner), `scratch-repository.json` (`visibility` `public`), and `compare.PUBLIC_FROM`. **Checked against records:** runs 5 and 6 were created at 14:21:57Z and 14:27:53Z, after the 14:21Z switch, and runs 1–4 before it. Run 6's machine equals run 2's: image `20261013.0424.1`, M1 (Virtual), 3 cores, 7 GiB. Run 5 shows 33 s of job time, checkout `failure`, and three 403 annotations. The public jobs' 18 minutes are recorded, and counted as 0. The two resumed issuances alone (369.8 s, 395.6 s) are labelled a first public-class measurement, not CP-18's. **Not checked by me:** the Orchestrator's secret scan before the switch, which is relayed, not recorded. The frozen identity and manifest contain no "private" claim, so the switch touches no frozen term |
| O1 | **The re-freeze record** and `freeze-manifest.json`: complete on its own; records the new identity, the reissued freeze-origin artifact, the canary hash, and the six §24.12 rows; CP-17b superseded, not edited; governance pinned (anchor r19, brief, decisions 20–21 and 22–25); a later anchor revision leaves `verify` green | PASS | **Content.** §1 lists every change and §7 carries CP-17b's terms by hash. §9 holds the six rows plus the issuing host. The identity is `720fc581…` (recomputed), the artifact `4aedd5e0…`, and the canary `4e6abb02…`. **Integrity.** CP-17b's evidence is unchanged (16), and `verify` checks it by hash. The four pinned copies hash as cited (18), and `verify` checks twelve pins. **Amendment.** A simulated anchor and decisions change stays `verified` (2c), with no problem without local files (2d). An altered pinned copy is refused (2e). The CI `amended` mode is green (1) |
| O2 | **The issuing host, frozen**: binary by tarball and `bin/node` hashes, retrieved per run with `SHASUMS256.txt`; the path replacing the Homebrew defaults; the Pyodide folder and how its 23 files reach the runner; `verify` with no problem and no unchecked item on both machines, the zip under the recorded zlib; CPython patch pinned without changing `uv.lock`/`pyproject.toml`; where image and CPU are recorded | PASS | **Retrieval.** `cp17.runtime` pins §24.13's bytes and hashes exactly. `retrieve` checks `SHASUMS256.txt`, its listing, the tarball and `bin/node` before moving anything into place. The runner's retrieval in run 6 shows the same hashes (11). **Path.** `daily.NODE` and `hosts.NODE` name the official binary, and my reruns executed it (3, 4). **Pyodide.** The 23 files are committed in the scratch tree and verified there (11: 505 files). **`verify`.** It printed `verified` on the runner (run 2 and run 6) and on the M3 (2b), with zlib `1.2.12` on both. **CPython.** 3.13.15, executable `7710b049…` on the runner; `uv.lock` and `pyproject.toml` are unchanged (11, 16). **Image and CPU** are recorded in each run's check record (6a; report table) |
| O3 | **H2 frozen as code with tests**: pins, binary, machine (`ImageOS` `macos26`), canary, in order; any failure issues nothing; for 4.7T a blocker; each check tested failing alone | PASS | **Code.** `cp17.hostcheck` is a pipeline file in the identity (`1c721b58…`). `gate` stops at the first failure, and `run` calls the issuance only after a pass. **Tests.** Each check failing alone, a raising check, and issuance only after a pass: these pass in CI and in 1b. **Reruns.** In my rerun (3), four forced failures each stopped at their own check. The runner and the M3 recorded five, including the canary-hash case (6a). The resume's gate passed (11). **4.7T.** The blocker rule is in the module, the identity and §3 |
| O4 | **The states' route** defined and exercised on the runner (`k13.json`, freeze-origin states, shadow buffers, issued records, canary payload); how each reaches the runner and persists; CP-18's form proposed and exercised over the 14 days | PASS | **Defined** by path and hash in the identity's `state_route` and checked by `verify` (2b, 2d). **Exercised on the runner:** `k13.json`, the freeze-origin state and the canary payload were committed and verified. The freeze-origin store was initialized and loaded back. The shadow buffers and issued records were carried day to day, then between runs: run 3's stores, committed in the scratch repository and byte-identical (10), resumed by run 6 for 2026-08-30 and 2026-09-06. **Proposed:** `state-route-proposal.md` |
| O5 | **R7 fixed on its error path only**: a malformed day listed, not raised; tested; every fit, quantile and artifact field bit-identical | PASS | **The diff** touches only `verify_bundle`'s per-day loop and the cross-check's day list. A record that verifies yields the same days and messages; the change of message affects only records that schema validation already refuses. The schemas are unchanged. **Recomputed (14):** CP-17c lists all six controls and CP-17b raises on all six. **Bit-identical:** host parity (4), native parity (5), and 58/58 fits on each machine (6a) |
| O6 | **The parity, shown.** On the runner and the M3: `verify` clean; host parity at nine origins bit for bit; shadow buffers over the 14 days against `shadow-run.json`; H2 passing with one forced failure each; timing and peak per fit against 15 min and 4 GB. On the M3 only: native parity five policies × nine origins; Chromium and WebKit at the freeze origin | PASS (runner days 2026-08-30 and 2026-09-06 on the public class, by decision 26) | **`verify` and H2:** clean on both machines (6a; 2b, 3; 11). **Host parity:** 9/9 on each machine, checked directly (8). **Shadows:** 14/14 days on each, 532/532 comparisons (9); the final state and the stitch on both (6a, 10). **Ceilings:** worst 231.9 s and 157.1 s, and peaks 968,884,224 B and 979,763,200 B. **Native parity:** recorded PASS 5×9, equal to CP-17b's record; my rerun at 2025-10-26 equals it (5). **Browsers:** Chromium 153.0.8010.12 and WebKit 26.6 give `4e6abb02…` on zip `460a94e1…` (record, re-hashed source). **Runner class:** checks and 12 shadow days ran on the private class, as §24.13 asks; the last two days ran on the public one, stated (D26) |
| O7 | **The cost** on the scratch repository's `macos-26`, from the shadow run's sequential issuances: one issuance, and decision 23's four with the canary | PASS (with a note) | **Runner** (private class, beside the other block): one issuance median 431.8 s (404.5–489.3, n = 12); four with the canary median 1,887.8 s (1,849.0–1,923.2, n = 6). **Alone, public class:** 369.8 and 395.6 s, labelled as such. **M3:** 239.7 s and 1,046.0 s. The figures beside the other block are conservative, as stated. See N2 for one sentence of the report |
| O8 | **The values 4.7T's brief cites**, in one table | PASS for the candidate | Freeze record §9, every value checked above. The return is outside this review |
| F1 | **Blind**: boundary 2026-09-06; no later byte downloaded, read or inferred; no 4.7T forecast | PASS | `inputs.json` records the boundary guard over the shipped rows (67,343 and 59,446) and prices (336). The scratch tree's files match its hash list (12), and no shipped name carries a later data date. The added lines carry only document, ruling, run and calendar dates (17). No 4.7T issuance exists. See N4 on the test's exclusion |
| F2 | **GitHub-landable**: no committed file over 50 MB | PASS | The largest added file is `pinned/anchor-capstone-v21-r19.md`, 342,690 bytes. The largest file in the tree is 30,830,306 bytes and predates this round. The scratch tree's largest is 20,230,545 bytes |
| F3 | **CI-ready**: the seven steps green on a history-free single-commit copy, `CI=true`, Python 3.12; `pytest -m stress` locally; no test depends on history, tags or local-only inputs; such tests skip with a stated reason | PASS | Command 1: green as built and after a simulated amendment, 2550 passed and 48 skipped each, and the stress run passed: 19 passed, 1 skipped. Every skip states its reason. With the local inputs present (1b), the CP-17c and superseded CP-17b tests give 153 passed and 0 skipped |
| F4 | **What may change**: `src/cp17/` with every change listed; superseded tests in `tests/cp17/` and `tests/cp17b/`, listed; new files under `tests/cp17c/`, `reports/cp17c/` and `docs/track-b/evidence/cp-17c/`; harness under `src/cp17c/`; nothing under `.github/` | PASS | Every changed path is allowed and none is under `.github/` (16). Every `src/cp17/` change, with its reason, is in §1. The seven superseded tests and the `stress` fixture are in §11, and their diffs match that list. The repair added nothing under `src/cp17/`. The workflow is kept at `src/cp17c/refreeze.yml` |
| F5 | **What never changes**; no earlier evidence binds an edited file's bytes | PASS | The protected-path diff is empty (16). The old bytes of the edited files are pinned only where CP-17c supersedes them. CP-17b's verifier reports exactly the declared set (2f). `src/cp26/harness.py`'s `PINS` names none of them |
| F6 | **The Critic's reruns** (suite and stress; `verify` on the new manifest and after a simulated anchor change; H2 with one forced failure; host parity at one origin; native parity at one DST origin; every runner comparison recomputed from the hash-verified downloads; nothing on GitHub) | PASS | Commands 1–7, each with its exit code and output above |
| C1 | **The red line (§24.2)** | PASS | As F1 |
| C2 | **Homebrew's `node` stays pinned and installed** | PASS | Command 15 |
| C3 | **Credentials**; no secret created; MLflow telemetry off | PASS | **Scratch repository:** 0 secrets, 0 variables, default workflow permissions `read`. **Workflow:** `permissions: contents: read`, `persist-credentials: false`, no `secrets.` reference, and `MLFLOW_DISABLE_TELEMETRY` and `DO_NOT_TRACK` set. **Code:** the changed code reads no credential and prints no environment |
| C4 | **Long computation within the ceilings, under a ledger; WIP commits**; GitHub within 1,000 counted minutes, standard `macos-26` only, no paid usage | PASS (with note N5) | **Local:** 3.5 machine-hours of 8. **Commits:** 22 commits. **GitHub:** 660 minutes counted on the private class, or 820 if queued time counted, against 1,000; standard `macos-26` only; GitHub's billable time is empty or 0 on every run, so the count is the job-time count. The public runs count 0 by GitHub's terms for public repositories, with their 18 job-minutes recorded |
| C5 | **Tools**: `gauntlet.py start` first; the Lead worktree; one Critic through `critic-open`/`critic-brief`/`critic-close`, its first line forbidding the memory directory; `gauntlet.py return` | PASS for what exists now | **Start.** `start.json` records `main` = `adcaf051…` at 03:25Z. **Critics.** `critic-open.json` holds two records, one per candidate. The first is closed with a stated note. The second is this one, and its assignment's first line is the memory rule. A second Critic is what the first's BLOCKED required ("a new candidate SHA … needs a fresh Integration review"), and one fresh PASS binds the final candidate. `critic-close` and `return` come after this verdict |
| C6 | **Memory** not opened or edited | Not checkable from the artifact | No trace of it in the candidate. I did not open it |
| C7 | **Owner-facing Git commands non-interactive** | Not exercised by the candidate | The candidate gives the Owner no Git command |

## On FAIL only

- Single largest meaningful gap: not applicable (PASS).
- Exact next acceptance test: not applicable (PASS).

## Findings that do not gate this verdict

- **N1, "private" left in three places.** Freeze record §1's Pyodide row and §6's "How it reached the runner here" column both say the files were "committed in the private scratch repository". `state-route-proposal.md`'s table says the same, and so does `cp17c/inputs.py`'s docstring. That was true when they were committed, and §8 and the proposal state the switch. Read alone, though, §1 and §6 now misdescribe the repository. A one-word fix ("the scratch repository, private until decision 26") would keep §1 and §6 complete on their own.
- **N2, one report sentence.** `report.md` says "On both machines the two blocks ran at once, each its days one after another, so the day figures are conservative." On the runner, 2026-08-30 and 2026-09-06 ran in the resume, one block after the other. The cost table separates them correctly ("alone"), so no figure is wrong.
- **N3, the "is disabled" text is not in a record.** `owner-decision-26-as-relayed.md` and freeze record §8 quote run 5's 403 as "Repository … is disabled". `artifacts.json` holds the run's annotations, which record three `403` checkout failures and git's exit 128, but not that text. It sits only in a local job log, which I did not open. The annotations support a transient 403 at checkout, which is all the conclusion needs.
- **N4, the red-line test's exclusion is wider than needed.** `test_no_committed_record_holds_a_date_after_the_boundary` now skips `measurement.json` and `report.md` entirely, for one switch time. My scan (17) finds nothing else after the boundary in either file. Excluding only that string would keep both files under the test.
- **N5, the ledger's estimate spans.** The ledger's measured entries overlap at most 4 at a time, the brief's ceiling. Three entries are aggregates: two "ESTIMATE" entries spread over 75- and 80-minute spans, and Critic 1's time taken from its verdict. So they can be neither placed against nor excluded from that peak. The ledger is otherwise well within 8 machine-hours.
- **N6, `compare.PUBLIC_FROM` is a minute-precision constant.** It is not read from GitHub's audit of the visibility change. No run falls near it: run 4 was at 10:21Z and run 5 at 14:21:57Z. For CP-18's records, the visibility at each run would be better read than assumed.
