# Verdict — CP-18a — Integration — PASS

- Candidate SHA: fcdec05b249929cd70befe96d7f01af565ff056c (branch `gauntlet/cp-18a`; base `main` = 0d7d63103a633f89b81f7d3bc7a27f4dd6b992f6; tree 0e1bdc70439acc6c0174e0d336c4bfa90f6bcf69)
- Plan / version / bar: `capstone_v21.md`, v21-r19 (file SHA-256 acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e, recomputed), §24.13 "For CP-18"; the checklist is the issued brief `docs/track-b/evidence/cp-18a/issued-brief.md` (SHA-256 0c805a7167e33d21596fc2fef384d44428831fa23595876b96257c0f14192255, recomputed): Observable outcome 1–8, Further items 1–5, Applicable constraints, plus the Orchestrator's amendment of 2026-10-31.
- Verbatim bar excerpt:

> #### For CP-18
>
> These add to §24.12's list "For CP-18", as amended above:
> - **the unattended pipeline on the `macos-26` runner.** It calls `cp17.daily` once per issuance, with the
>   checks above and decision 23's catch-up. It has a schedule and a failure rule, and no deadline;
> - **the public runner class's timing,** measured in the product's repository on development days before
>   the first live issuance, against criterion 5's ceilings;
> - **the cause of each day that is not issued,** in the record. The causes are:
>   - a failed issuance by the chain;
>   - a failed H2 check;
>   - a live day's inputs that cannot be shown to precede its cutoff;
>   - no run within the lookback;
>   - S_14's state not in place;
> - **one issuance per delivery day across the runner and the local fallback.** The issued record is the
>   single source, and no issued forecast is replaced;
> - **how the states are carried** from 4.7T's last window day to the first live day;
> - **a live day's input availability,** made verifiable as the publication time above requires;
> - **the credentials as GitHub secrets.** The Owner enters them himself (decision 25), and agents never
>   handle their values;
> - **`AGENTS.md`'s conditions on the runner:**
>   - the secret guard and the pre-push guards run on the runner's own commits and pushes;
>   - credentials are used only as stored variables inside the consuming process;
> - **public run logs.** The repository is public, so its run logs are public. Credentials, and any value
>   derived from them, are never printed;
> - **GitHub's rule that disables a scheduled workflow** after a period without repository activity. CP-18
>   shows how the pipeline stays enabled;
> - **a local fallback on the Owner's Mac,** with the same binary and the same checks;
> - **the red line on the runner.** Until CP-18's brief retires the boundary guard after 4.7T (§24.2), the
>   runner's pipeline runs only on development data through 2026-09-06 (decision 7). No scheduled run
>   retrieves later data.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.) The rest of the bar the brief quotes (§24.13's publication time, catch-up and S_14 sections; §24.12's "Open…" with R7; §19.4; §22's binding reminder; the Space plan §7) was checked by `bar.py check` against its files at the candidate: all 8 excerpts found.
- Worktree clean before and after: yes. `git status --porcelain` empty at the start and at the end (only ignored `__pycache__/`), `HEAD` = fcdec05b249929cd70befe96d7f01af565ff056c throughout. No Git write was made in the candidate repository. Isolation was cooperative (procedural), not a read-only mount.

## Commands actually run

Every shell exported the brief's environment (`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1`, the five `*_NUM_THREADS=1`, `PYTHONPATH=src`, `CP17_PROJECT_ROOT=/Users/djourno/Downloads/PJM`). Python: `/Users/djourno/Downloads/PJM/.venv/bin/python` (3.13.15) unless stated. Scratch: `/Users/djourno/Downloads/PJM/.local/tmp/cp-18a/critic/`.

| # | Command | Exit | Observed |
|---|---|---|---|
| 0 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief cp-18a` | 0 | The brief printed (candidate, bar, assignment, protocol, form). |
| 1 | `git status --porcelain`; `git rev-parse HEAD`; `git rev-parse main` | 0 | Empty; fcdec05b…; main = 0d7d6310 (the base). 22 commits on the branch. |
| 2 | `shasum -a 256 docs/track-b/evidence/cp-18a/issued-brief.md capstone_v21.md docs/track-b/final-product-space-plan-2026-09-30.md` | 0 | 0c805a71…, acdeeab1…, ad3568c8… — each equal to the pinned value. |
| 3 | `git show main:scripts/bar.py \| python3 -I - check docs/track-b/evidence/cp-18a/issued-brief.md --source capstone_v21.md@fcdec05b… --source docs/track-b/final-product-space-plan-2026-09-30.md@fcdec05b…` | 0 | `ok` for all 8 excerpts (7 in capstone_v21.md, 1 in the Space plan). |
| 4 | `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json` | 0 | Exactly `verified`. |
| 5 | `git diff --stat 0d7d6310 fcdec05b… -- src/cp17 src/cp17c src/delu_forecast src/cp15 src/cp16 src/cp20 … src/cp28 src/cp17probe src/cp17cprobe data reports/development-inputs pyproject.toml uv.lock` | 0 | Empty. |
| 6 | `git diff --name-only 0d7d6310 HEAD` filtered by the allowed paths | 0 | 134 files changed; the only two outside the brief's allowed paths are `tests/test_40_publication_guard.py` and `tests/test_48_publication_tools.py` (the amendment). |
| 7 | `git diff 0d7d6310 fcdec05b… -- tests/test_40_publication_guard.py tests/test_48_publication_tools.py` | 0 | test_40: one line, the fixture also copies `leak_scan.py`. test_48: the order shifts by one for the leak scan; two assertions become three. Nothing else. |
| 8 | `git ls-tree -r -l HEAD \| sort -k4 -n -r \| head` | 0 | Largest committed file 30.8 MB (pre-existing); largest added 20.2 MB (the pinned `k13.json`). None over 50 MB. |
| 9 | `git diff --stat 99f01705 fcdec05b… -- src/cp18 .github .githooks scripts` and the full diff | 0 | Only `src/cp18/__main__.py` (seed-store's optional `:<origin>`, and its genesis `source` label "development state X" → "state X") and `src/cp18/forced.py` (its record's `origin_log` cut to 5 lines). |
| 10 | `git -C .local/tmp/cp-18a/scratch1 ls-tree -r 0b2fd1bf…` compared blob by blob with `git ls-tree -r 99f01705` and with the candidate | 0 | The scratch commit run 41701507248 ran (0b2fd1bf, per the GitHub ledger): 418 files, every blob equal to 99f01705's except the scratch README and `scratch-files.json`. Against the candidate it differs only in the README, `src/cp18/__main__.py` and `src/cp18/forced.py`. The workflow is identical. |
| 11 | `python3 .local/artifacts/cp-18a/ci-runner.py critic fcdec05b… ci312 stress` (script read first) | 0 | **ci312** (history-free single commit, same tree 0e1bdc70, `CI=true`, Python 3.12.14): leak scan 0 (`clean (F1 skipped, F2, F3; allowlist 4 entries)`); `uv sync --locked --dev` 0; build_wasm_payload 0; `pytest -q` 0 (`2840 passed, 51 skipped in 632.31s`); CQR fixture 0 (8 passed); verify_release 0 (PASS); WASM equivalence 0 (15 passed); publication_guard tree 0; stress collection 0 (21/2890). **stress** (3.12): `19 passed, 3 skipped`, exit 0. Scratch removed. Logs: `.local/artifacts/cp-18a/critic-validation/{ci312,stress}/`. |
| 12 | `python -m pytest -m stress -rA -p no:cacheprovider` (worktree, project venv) | 0 | `21 passed, 1 skipped (eccodes absent), 2869 deselected in 885.61s`. PASSED includes `test_dry_run.py::test_a_real_dry_run_then_the_fallback_finds_the_day_claimed`, `test_forced.py::test_each_cause_is_forced_and_recorded` and all 15 CP-26 supervision, monitor and ledger-liveness tests. |
| 13 | `python -m cp18.forced --project /Users/djourno/Downloads/PJM --work <empty> --out <file>` (≈176 s) | 0 | 2026-08-31 h2, 09-01 no_run, 09-02 s14, 09-03 inputs, 09-04 chain, 09-05 chain, "every cause forced: True \| as expected: True". `found` equals `reports/cp18a/forced-causes.json`'s `found`. `gate_a`, `gate_b` (canary 4e6abb02…), `origin_log` and the 2026-09-04 chain path are also equal. `store_head` differs (run records carry wall-clock times), as expected. |
| 14 | By hand: bare origin, a `--no-local` clone of the candidate, `python -m cp18 seed-store --genesis reports/cp18a/dryrun/states/start-2026-08-31.json:2026-08-31`, a commit and push through `.githooks`, then `python -m cp18 run --host runner --now 2026-08-30T12:00:00+02:00 --inputs live:reports/cp18a/dryrun/recorded` under `env -i` with `SECRET_GUARD_ENV_ONLY=1` (`critic/byhand.sh`) | 0 | Seed commit 0 and push 0, through the hooks. Gate passed (pins, binary, machine, canary 4e6abb02…). Planned [2026-08-31], `done`. A1 issued, quantiles 75d86a3b3cb9f670b091a0da…. v4, v2 and B0 equal CP-17c's (`reports/cp17c/measurement.json`), and the live payloads and every fit equal runner run 41701507248's. |
| 15 | `python -m pytest tests/cp18a/test_pipeline.py -q` | 0 | 19 passed. |
| 16 | `python -m pytest tests/cp18a/test_red_line.py -q` | 0 | 134 passed. |
| 17 | `python -m pytest tests/cp18a/test_leak_scan.py tests/cp18a/test_environ_access.py tests/cp18a/test_environ_redact.py -q` | 0 | 72 passed; "environ-access lint: 32 allowlist entries covering 37 bare reads". |
| 18 | `env -i PATH=/usr/bin:/bin:/opt/homebrew/bin HOME=<temp> python3 scripts/leak_scan.py tree` | 0 | F1 skipped (no fingerprint file); 11 findings suppressed by 4 allowlist entries; `clean`. |
| 19 | `python -m pytest tests/cp18a/test_live_runner_env.py tests/cp18a/test_live_equality.py -q` | 0 | 3 passed (2026-09-06 with LightGBM refused and no `.local/`; parity origin 2026-03-29 byte-identical; GFS client on 2026-09-05). |
| 20 | `python -m cp18.live.recorded render --days 2025-10-16..2025-10-26`, `… archive --days 2025-10-19..2025-10-26`, `python -m cp18.live.equality --sets parity --days 2025-10-26 --workers 1` | 0, 0, 0 | Extra parity origin 2025-10-26 (the autumn DST day): `all_equal: true`, 4/4 stems. The live hashes also equal the record's for that day. |
| 21 | Rehash of the 92 development-builder reference files (`.local/artifacts/cp-17b/runs/{native-parity,shadow-host}/payloads/`) against `reports/cp18a/live-equality.json` | 0 | 92/92 json, npz and `payload_sha256` equal the record's reference values; 23 days (9 parity, 14 shadow); the record shows 92/92 equal. |
| 22 | `python -m cp18.compare timing --downloads … --record fetch-41185674168.json fetch-41204328732.json fetch-41701507248.json --out <file>` | 0 | Every file hashed as listed. `runs` (fetch aside) and `summary` equal `reports/cp18a/runner-timing.json`; the fetch blocks are equal too. One issuance 344.3–413.4 s; four with the canary 1,634 / 1,838 s pipeline, 1,693 / 1,903 s job; slowest fit 173.6 s; largest peak ≈930 MiB; all fits within 900 s / 4 GiB; all 36 fits equal CP-17c's. |
| 23 | `python -m cp18.compare carry --carried …/carried/window --resumed runner=…/41204328732/live/store --resumed m3=…/carry-m3/clone/live/store --out <file>` | 0 | `same_on_both`, `fits` and `resumed` equal `reports/cp18a/carry-rehearsal.json`. Ledger prefix True and carried files unchanged on both; 2026-09-04 `outside`; 2026-09-05 A1 8d5cb5ea… on both. Run 41185674168's ledger is also a byte prefix of the carried one. |
| 24 | `python -m cp18.guarddemo scan --run-id <run> .local/artifacts/cp-18a/logs/run-<run>.log …/downloads/<run>` for 41185674168, 41204328732, 41701507248 | 0, 0, 0 | 77, 45 and 77 files; `clean: true`, `found: {}`. The log SHA-256s equal `credential-scan.json`'s. |
| 25 | Read each run's `guard-demo.json` | — | `all_as_expected: true` on all three. Fake values blocked by value: staged ENTSOE_API_TOKEN, message HF_TOKEN, pushed DAGSHUB_USER_TOKEN. The environment dump is blocked by the leak scan in 41204328732 and 41701507248 (not applicable in 41185674168, before the scan existed). The data-only commit and push pass. No value in any output. |
| 26 | My own red-line scan, `critic/redline_scan.py`, over all 134 added or changed files. It gunzips `.gz` bodies, opens every NumPy array and matches ISO and compact YYYYMMDD dates, timestamps and epoch-ms numbers. | 0 | No market data after 2026-09-06. See finding N1. Dates after the boundary are calendar, protocol, document or wall-clock dates (snapshot pull 09-08, CP-25 retrieval 10-12, run times 10-31 and 11-03, image versions, S_13/S_14 dates, 4.7T 09-07 and 12-04). The ENTSO-E rendered bodies' last instant is 2026-09-06T22:00Z, the `end` of D=09-06's interval. The SMARD bodies end at 2026-09-06T21:45Z. |
| 27 | `ls ~/Library/LaunchAgents \| grep -i delu`; `HOMEBREW_NO_AUTO_UPDATE=1 brew list --pinned`; `ls /opt/homebrew/Cellar/node/` | 0 | No delu agent installed; `node` pinned; 26.7.0 installed. |
| 28 | `git grep -l 'pytest\.ini' HEAD`; read `src/cp26/harness.py` PINS and `src/cp24/basetree.py` | 0 | No freeze manifest and no PINS entry binds `pytest.ini`. `reports/ddnn2/base-tree.json` records its old hash as CP-24's candidate-scoped base record, explicitly not enforced after LAND. |

## Evidence actually inspected

- **The brief and report:** `docs/track-b/evidence/cp-18a/issued-brief.md` (whole) and `reports/cp18a/report.md` (whole, §8 = item 8's table).
- **Code, read in full:** `src/cp18/{__init__,plan,causes,r7,pipeline,claim,store,inputs,live_inputs,host,local,guarddemo,forced,compare,__main__}.py`; `src/cp18/live/{__init__,build,availability}.py`; the heads of `archive.py` and `scratch.py`; the guard calls and imports of every `src/cp18/live/*.py`; `transport.py`'s guard and credential path; `src/cp17c/store.py` (F1 binding); the relevant parts of `src/cp17/shadow.py` (release semantics), `src/cp17/runtime.py` (`retrieve`) and `src/cp25/guard.py` (BOUNDARY, GFS_RUN_CUTOFF, admit_gfs).
- **Workflow and security:** `.github/workflows/daily.yml`, `.github/workflows/tests.yml`, the `.githooks/` diff, `pytest.ini`, `tests/environ_redact.py`, `scripts/leak_scan.py` (header, modes, ALLOWLIST with reasons), `scripts/credential_fingerprints.py` (prints and refusals), `tests/cp18a/test_environ_access.py` (ALLOWLIST with reasons), `reports/cp18a/rulesets/*.json` and `README.md`, `reports/cp18a/launchd/com.delu.daily-fallback.plist`.
- **Tests:** `tests/cp18a/test_pipeline.py` (fixtures, the race test, the claim, store, carry and keep-enabled tests), `test_red_line.py`, `test_dry_run.py`, `test_forced.py`, `test_live_runner_env.py`, `test_live_equality.py`, and parts of `test_live_transport.py`.
- **Records:** `reports/cp18a/{github-ledger,compute-ledger,forced-causes,runner-timing,carry-rehearsal,credential-scan,live-equality}.json`.
- **Runner downloads** (`.local/artifacts/cp-18a/downloads/<run>/`): `run/run.json`, `prepare.json` (4 pinned states copied by hash; Pyodide 23 retrieved from `https://cdn.jsdelivr.net/pyodide/v0.28.0/full`; Node v26.7.0 tarball and SHASUMS256 from nodejs.org; package equal to the manifest), `guard-demo.json`, `cpython.json` (3.13.15), the stores' `issued/<day>/{artifact,record}.json` and `results-sha256.txt`. The public logs `run-<run>.log` were scanned only, never printed.
- **The Lead's validation:** `final3-validation/{ci312,stress,stress313}/results.json`, `stress313/02-stress.log` (the five CP-26 failures), `stress-local-fcdec05b.log`, `.local/tmp/cp-18a/stress-cp26-main.log`.
- **My own run's material:** the forced run's input archive `live/inputs/days/<day>/manifest.json` (records with source, publication per data day with basis, `retrieved_utc`, SHA-256, provenance).

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| O1.a | Pipeline package `src/cp18/`, tests `tests/cp18a/` | PASS | Present; the suite runs in CI and locally (rows 11, 12, 15–19). |
| O1.b | One run: H2 gate once before the first issuance; any failure issues nothing | PASS | `pipeline.run`: `hostcheck.gate` once, only if days are planned, before the loop; on failure every planned day stays open with cause `h2`. Forced run A (row 13) and `test_a_failed_h2_check…`. |
| O1.c | Decision 23's catch-up: 3-day lookback, ≤4 per run, oldest first | PASS | `plan.lookback`/`plan.plan` (`MAX_ISSUANCES = 4`); days older than the lookback closed by `to_close`. `test_catch_up…`, runner runs plan 08-31..09-03 at a 09-02 wall clock. |
| O1.d | Each issuance through `cp17.daily`, once per delivery day | PASS | `default_issue` → `cp17.daily.issue_day`. The store refuses a decided day (`check_day`). Rows 12 and 14. |
| O1.e | No deadline, no "late" label; cutoff D−1 11:00 Berlin; run time kept | PASS | `plan.cutoff = guard.issue_time`; no late status (`causes.text('late')` raises). The actual run, issuance-start and issuance-end times are in `issued/<day>/record.json`, hash-bound in the ledger beside the artifact. The frozen artifact's own `times` hold nominal instants and cannot change without a re-freeze (finding N3). |
| O1.f | Availability judged by publication time vs the cutoff, never by run time; verifiable from the record (publication, retrieval time, hash) | PASS | `cp18.live.availability.judge` uses the per-input basis against `cutoff(for_day)`, or the served day's cutoff for GFS. The day record holds each judgement (publication_utc, basis, sha256, record id). The committed archive manifest holds `retrieved_utc` and the body hash. The forced 09-03 case shows a retrieval after the cutoff refused. |
| O1.g | Issued record single source; one issuance per day across runner and fallback; never replaced; claim designed; race tested | PASS | `cp18.claim`: fetch, detached checkout, commit through `.githooks`, fast-forward push. A non-fast-forward loser checks out the winner's main and stops. `test_the_push_race_loser_discards_its_own_issuance` races two clones of one bare origin (the winner runs inside the loser's issuance window). The loser ends on the winner's main with one issuance and one run record. The stress dry run shows the fallback finds the day claimed. |
| O1.h | Cause of each day not issued: r19's five, in the record | PASS | `cp18.causes` (exactly 5); `not_issued` ledger entries validated by `LiveStore.verify`. All five forced through the real pipeline at the candidate (row 13). |
| O1.i | R7: a raised `verify_bundle` error is a refused record | PASS | `cp18.r7.verify` wraps it; `test_rules` checks that no module calls `verify_bundle` except through it. The pipeline verifies no bundle this round; the bundle is CP-18b's. |
| O1.j | Red line in code; refuse any day after 2026-09-06 via `cp25.guard`; retirement a reviewed change, not a flag | PASS | `plan.admit(lookback + target)` is the first act of `pipeline.run`, before sync, gate or retrieval (exit 3, no day named). The live builder's only boundary is `cp25.guard` (`cp17.tools.payloads` is not called). No flag. The retirement touches `BOUNDARY` and `GFS_RUN_CUTOFF` in `cp25.guard` (finding N2). |
| O1.k | Red-line test over every file this round adds, none skipped whole | PASS (with finding N1) | `test_red_line.py` enumerates every added path and the changed hooks, workflow and ini, 134 checks, and excludes none. Its byte scan cannot see inside `.gz` bodies, epoch-ms numbers or integer dates. My own scan (row 26) covered those and found nothing after the boundary beyond what N1 describes. |
| O2.a | Live-input payload builder into the frozen payload kinds; GFS flag under the tier register and rulings | PASS | `src/cp18/live/` (contract in `__init__.py`); `build_day` writes A1, v4, v2 and B0; GFS flag per ruling 4 (`availability`, `history`). |
| O2.b | Byte-identical to `cp17.tools.payloads` at the 9 parity origins and the 14 shadow days, from CP-25's recorded data | PASS | The record shows 92/92. I rehashed all 92 reference files (row 21) and recomputed 2026-03-29 (test), 2026-09-06 with LightGBM refused and no `.local/` (test), and 2025-10-26 (CLI, row 20). All byte-identical. |
| O2.c | Retrieval clients exercised only against recorded responses | PASS | GFS truly recorded (test, 50 messages). SMARD and ENTSO-E are rendered from the recorded snapshot in each documented shape, labelled `rendered` everywhere and disclosed. `HttpTransport` is never instantiated outside its refusal and no-network tests (finding N7). |
| O2.d | No network data retrieval this round | PASS | Every run used replay transports and simulated wall clocks. My reruns made no network contact (replay only). |
| O3.a | Store keeps CP-17c's F1 fix (head bound to the ledger's last entry) | PASS | `LiveStore(Store)` calls `super().verify()` first. `test_the_store_keeps_cp17cs_head_binding…` repoints `last_day`, `last_artifact_sha256` and `state_file`, and each fails. |
| O3.b | Where the states live; exact daily data-only paths named | PASS | `live/store/` (head, ledger, `states/`, `issued/<day>/`, `runs/`, `search/`) and `live/inputs/days/<day>/`. Pinned states once at `live/pinned/local/…`, outside `docs/`, which is all Pages serves (`docs/deploy.md`). A minor wording inconsistency is noted in N4. |
| O3.c | Carry from 4.7T's last window day to the first live day: designed and rehearsed bit for bit across a gap | PASS | `carry` entry (`record_carry`; gap days `outside`); rehearsal recomputed (row 23): runner and M3 identical, equal to CP-17c's. |
| O3.d | S_14 (H4): where its state enters; what is recorded while absent | PASS | `python -m cp18 search --k 14` → `search/k14.json`, validated (`validate_ensemble`) and hash-bound. While absent the day stays open with `s14` (forced 09-02). |
| O4.a | `daily.yml` new, `workflow_dispatch` only, no `schedule:` | PASS | Read in full. |
| O4.b | Binary by hash, H2 gate, then the pipeline in dry-run mode on development days | PASS | `cp18 prepare --retrieve-node` → `cp17.runtime.retrieve` (SHASUMS, tarball, binary by hash), then `cp18 run --mode dry-run` (only mode accepted); gate passed on all three runs. |
| O4.c | Binary and Pyodide's 23 files by hash from their official URLs | PASS | `host.pyodide` places a file only after its manifest hash holds; `prepare.json` shows 23 retrieved from jsDelivr's Pyodide v0.28.0 path and Node from nodejs.org. |
| O4.d | Secret guard and pre-push guards on the runner's own commits and pushes, shown with a fake credential blocked by value | PASS | `Claim.publish` refuses unless `core.hooksPath` is the checkout's `.githooks`. The guard demo on each runner blocked the fake values by value (row 25). The seed commit and push on the runner ran the hooks (public log). |
| O4.e | Credentials only as stored variables in the consuming process; no log line or artifact holds a fake value | PASS | Fakes derived from the run id, set only in the pipeline step, never printed. Scans of the logs and artifacts are clean (row 24). The live transport reads the token with `os.environ.get` inside `send`. See N8. |
| O4.f | Secret names fixed; no other credential named | PASS | `ENTSOE_API_TOKEN`, `HF_TOKEN`, `DAGSHUB_USER_TOKEN`. The report states no other credential is needed (the day's push uses the workflow token). No secret in `daily.yml`. |
| O4.g | GitHub's disable rule: how the pipeline stays enabled | PASS | Every run pushes its run record to `main`, whatever it did (`test_every_run_whatever_it_does_pushes_a_commit_to_main`); the fallback pushes too. The stated exception is a refused store. |
| O4.h | Permissions: `contents: write` only where needed; else read | PASS | Top `permissions: {}`; `contents: write` on the one job (the activation's data-only commit); `persist-credentials: false`. Actions pinned by SHA; inputs passed through `env`. See N6. |
| O5 | Local fallback: same binary, checks and claim; one command; launchd written, not installed | PASS | `python -m cp18.local run`: Node checked in place at `.local/tools/node-v26.7.0-official/`, package zip rebuilt and compared, same `cp18 run` (gate, claim). The stress dry run shows the fallback finds the day claimed. The plist is written and absent from `~/Library/LaunchAgents`. |
| O6 | Public runner class timing: one issuance and four with the canary vs criterion 5's ceilings; CP-17c's data point | PASS | Recomputed from the hashed downloads (row 22): one issuance 344–413 s; four with the canary 28.2 and 31.7 job-minutes; every fit ≤173.6 s and ≈930 MiB, within 900 s and 4 GiB. The product-repository dispatch is the Orchestrator's, after landing. |
| O7.a | P0-2 leak scan: F1 fingerprints (Owner-generated), F2, F3; wired after `secret_guard.py` and as CI's first step; acceptance on fake fixtures | PASS | `scripts/leak_scan.py`, `scripts/credential_fingerprints.py` (prints names only, refuses under 128 bits); hooks call it after the guard and fail closed; `tests.yml`'s first run step; fixture tests pass (row 17); CI step green (row 11). |
| O7.b | P0-3: AST lint with reasoned allowlist, `src/cp17` allowlisted as frozen; redaction plugin by `-p` if `pytest.ini` is unbound | PASS | 32 entries, each with a reason; `src/cp17` entries say "frozen package"; no `src/cp18` entry. `pytest.ini` is unbound by PINS and every freeze manifest (row 28); `-p environ_redact` registered; child-pytest acceptance passes. |
| O7.c | P0-7 rulesets as JSON, with acceptance steps; not applied | PASS | Three rulesets and push protection in `reports/cp18a/rulesets/`, apply commands written not run, Owner acceptance steps, non-interactive (`GH_PAGER=cat`). Non-application cannot be checked from here (I ran nothing on GitHub). |
| O8 | One table of what the activation and 4.7T briefs cite | PASS | `report.md` §8: paths, commands, secret names, claim rule, daily and pinned state paths, genesis, carry, S_14, timing; plus "what the activation needs beyond this round". |
| F1 | Blind: nothing after 2026-09-06 downloaded, read or inferred; no 4.7T or live forecast | PASS | Rows 22–26. Every run issued development days 08-31..09-05 at simulated clocks. N1 explains the only boundary-adjacent value. |
| F2 | No committed file over 50 MB | PASS | Row 8. |
| F3 | CI-ready: workflow steps (leak scan first) green on a history-free single commit, `CI=true`, 3.12; `pytest -m stress` passes locally; skips state reasons | PASS | Row 11, every step exit 0. Row 12: stress 21 passed in the project venv. The two real-gate stress tests skip under 3.12 (`ss`), by the `skipif` reason "the H2 gate's pins check requires the issuing host's CPython 3.13.15". In CI they skip with "the local runtime, states or payloads are absent". **The disclosed `stress313` failures** (5 CP-26 supervision tests in a fresh 3.13.15 venv: process identity `reused` instead of `same`, and SIGSTOP signalling) do not reproduce at the candidate in the project venv (row 12, all 15 CP-26 stress tests pass). `src/cp26` and `tests/test_cp26_*` are unchanged, and the new `-p environ_redact` plugin only rewrites reports. I judge it an artifact of that venv mode, not a candidate defect; `stress313` is not a mode the brief requires. |
| F4 | What never changes; no earlier evidence's bytes broken; `refreeze verify` prints `verified` | PASS | Rows 4–7. No anchor, amendment, decisions record, AGENTS.md, role file, exposure ledger or backup register in the diff; no other checkpoint's reports or evidence. `pytest.ini` checked (row 28). |
| F5 | The Critic's local reruns | PASS | Suite and stress (rows 11, 12); one dry run through the H2 gate (rows 12 and 14); race test (row 15); forced causes (row 13); byte equality (rows 19–21); leak scan and lint (rows 17, 18); every runner comparison from the hashed downloads (rows 22–25). Nothing was run on GitHub. |
| AMD | Amendment of 2026-10-31 (test_40 and test_48) | PASS | Row 7: each diff is exactly the amended change. |
| RUN | Runner evidence valid for the candidate | PASS | Row 10: run 41701507248's tree equals 99f01705's. Since then only `seed-store`'s optional origin and genesis label and `forced.py`'s log trim changed, and neither touches the gate, plan, claim, store, inputs, issuance or workflow. Row 14 reissues 2026-08-31 at the candidate through the live builder with every fit and payload equal to that run's. The only effect is a different genesis `source` label (so a different genesis entry hash) for a store seeded at the candidate. Artifacts are unaffected. |
| C1 | Red line (§24.2) | PASS | As F1. |
| C2 | Homebrew `node` pinned and installed | PASS | Row 27. |
| C3 | Credentials per AGENTS.md; no real credential; MLflow telemetry off | PASS | Only fake, run-derived values; no secret created; workflow and plist export `MLFLOW_DISABLE_TELEMETRY`/`DO_NOT_TRACK`. Whether GitHub holds no secret or variable cannot be checked from here. |
| C4 | Allowed paths | PASS | Row 6, plus the amendment. |
| C5 | Long computation within ceilings, with a ledger | PASS | `compute-ledger.json` (2.04 of 10 machine-hours) and `github-ledger.json` (1.249 of 15 job-hours; my sum of job seconds agrees). Each job sets `timeout-minutes`. |
| C6 | Tools (gauntlet start, worktree, one Critic via critic-open/brief/close; first assignment line forbids memory) | PASS | This review came through `critic-brief`. The assignment's first line forbids the memory directory. Start and close are the Lead's steps, outside this review. |
| C7 | Memory directory not opened | PASS (cooperative) | I did not open it. The Lead's compliance can only be taken procedurally. |
| C8 | Owner-facing Git commands non-interactive | PASS | Rulesets README exports `GH_PAGER=cat GIT_PAGER=cat`. Claim and guard demo set `GIT_PAGER=cat`, `GIT_EDITOR=true`, `GIT_TERMINAL_PROMPT=0`. |

### Findings (non-blocking; none changes an item's verdict)

- **N1: red-line test blind spots.** The test byte-scans 34 gzip replay bodies without decompressing them, so it cannot see their contents. It matches only ISO dates, so SMARD epoch-ms timestamps and integer dates such as GFS `validityDate` pass unseen. It also leaves out the two amended files, though the report says it covers every file the round "adds or changes".
  - My own scan covered all of these. The rendered bodies end at D=2026-09-06.
  - The one value after the boundary is the recorded GFS run of 2026-09-05 00Z (`reports/cp18a/dryrun/recorded/gfs/runs/2026-09-05.json`): its f048 messages carry `validityDate` 20260907, valid at 2026-09-07T00Z. That run serves D=2026-09-06, was published 2026-09-05, and is admitted by the landed `cp25.guard` GFS rule (run initialized before 2026-09-06 00Z, leads f021–f048).
  - Worth hardening before the live data grows: gunzip `.gz`, and match epoch and compact dates.
- **N2: retirement is two constants, not one line.** Retiring the red line touches both `BOUNDARY` and `GFS_RUN_CUTOFF` in `src/cp25/guard.py`. The report's §8 names both.
- **N3: run time sits beside the artifact.** The actual run time is in the day's hash-bound `record.json` next to the artifact, not inside it. The frozen artifact's `times.issuance_utc` is the nominal instant, and putting the run time inside would be a re-freeze.
- **N4: path wording.** `store.py`'s docstring and a `daily.yml` comment say `live/inputs/<day>/`. The code and report §8 say `live/inputs/days/<day>/`.
- **N5: exceptions escape the run.** An exception during a day's acquisition or build (a missing recorded day now; a network error at activation) propagates out of `pipeline.run` instead of becoming a recorded cause. Closure writes made earlier in that run then stay uncommitted.
  - On the runner's fresh checkout this is harmless.
  - In the fallback's persistent clone, the next run refuses on the dirty tree. That fails closed but needs a manual clean.
  - For the activation brief.
- **N6: unused write permission.** The dry run's job holds `contents: write` it does not use. Credentials are not persisted, so the token cannot push.
- **N7: rendered responses untested against live APIs.** SMARD and ENTSO-E responses are rendered, not recorded raw, and this is disclosed. Whether the live APIs return exactly those shapes is untested until activation.
- **N8: one place the credential scan cannot see.** The by-value scan cannot see inside `origin.bundle`, a compressed pack. The store is extracted and scanned in plaintext; the input archive is only in the bundle, and replayed inputs carry no credential.
- **N9: rounding.** The report's "929 MiB" largest peak recomputes to 929.x, shown as ≈930.

## On FAIL only
- Single largest meaningful gap: n/a (PASS)
- Exact next acceptance test: n/a (PASS)
