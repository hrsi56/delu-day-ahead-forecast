# Verdict — CP-17-probe — Integration — PASS

- Candidate SHA: b4f23422c60e40fa8f0d3f523c28605f5451d589
- Plan / version / bar: `capstone_v21.md`, v21-r17 (SHA-256 3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc
  at the candidate, on `main` and at `f7c9035`), §19.3 "Train it yourself" is required (items 1, 2, 4 and 5) and §19.2
  One code path, for the designated policy A1; issued brief `docs/track-b/evidence/cp-17-probe/issued-brief.md`,
  SHA-256 2afc610e2c3f61b4ba862a8b1d2b1cf878764900ad11f4b5832634df8c53b155 (recomputed; equal to the canonical
  `.local/artifacts/cp-17-probe/issued-brief.md`).
- Verbatim bar excerpt:
  > ### 19.3 "Train it yourself" is required
  >
  > The Owner requires an in-browser retraining action for the final product.
  >
  > 1. **What it does.** In the visitor's browser, it retrains the daily fit of one issued delivery
  >    day from that fit's shipped training window, with the same code, seed and selection rules.
  >    It then predicts that day's quantiles.
  > 2. **What it reports.**
  >    - whether every data-driven selection matched the issued artifact;
  >    - the largest absolute difference per emitted quantile, in EUR/MWh;
  >    - one status that states only what was measured: identical bit for bit, within the frozen
  >      tolerance τ_eq, or different.
  > 3. **What it never does.** It never replaces, rescores or relabels an issued forecast.
  > 4. **The probe.** Before the CP-17 freeze, a feasibility probe on development data measures, for
  >    the designated policy:
  >    - browser time and memory;
  >    - payload sizes;
  >    - the deviation from the native fit;
  >    - selection agreement.
  >
  >    CP-17 freezes τ_eq and the reference runtime from that measurement.
  > 5. **If the policy cannot meet this requirement** within the measured limits, CP-17 returns a
  >    blocker. Only an explicit Owner exception, with its public wording, lets the product ship
  >    without the action. The requirement is never dropped silently, and never met by retraining a
  >    different implementation.

  > ### 19.2 One code path
  >
  > The code that performs the daily fit, issuance and scoring is the code the Space runs in the
  > browser for §19.3 and §19.5. No second implementation stands in for the product. A component
  > that cannot run in the browser runtime is reported at CP-17 under §19.3's exception route; it is
  > never replaced silently.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: yes. `git status --porcelain` was empty and `HEAD` was
  b4f23422c60e40fa8f0d3f523c28605f5451d589 at the start and after the last command. The only byproducts are
  git-ignored `__pycache__/` folders under `src/`.

## Commands actually run

All from `/Users/djourno/Downloads/PJM/.local/worktrees/cp-17-probe/critic-3` unless stated, with
`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1`. There was no network contact: no download, fetch or `ls-remote`.

1. `git show main:scripts/gauntlet.py | python3 -I - critic-brief cp-17-probe` → exit 0. The brief was generated
   (250 lines). I read the script first: `critic-brief` only reads.
2. `git status --porcelain` → empty; `git rev-parse HEAD` → b4f23422c60e40fa8f0d3f523c28605f5451d589.
3. `python3 scripts/bar.py bar capstone_v21.md '19.2 One code path' --at b4f2342…` → exit 0. Identity: plan sha256
   3124451d…; the section is 6 lines, 335 bytes, sha256 53834210…. The text equals the §19.2 excerpt above.
   `git show main:scripts/bar.py | python3 -I - bar capstone_v21.md '### 19.3 "Train it yourself" is required' --at b4f2342… --quote`
   → exit 0, section 25 lines, sha256 5d1f869e…. The text equals the §19.3 excerpt above.
4. `shasum -a 256` of `capstone_v21.md` at the candidate, `main` and `f7c9035` → all 3124451d…. The issued brief
   → 2afc610e….
5. `git diff --name-status f7c9035 b4f2342` → 34 paths, all `A` (added), all under `src/cp17probe/`,
   `tests/cp17probe/`, `reports/cp17-probe/` and `docs/track-b/evidence/cp-17-probe/`. No path is modified or deleted.
   `git diff --stat 4f1c0d7 b4f2342` → only `reports/cp17-probe/report.md` and four evidence files
   (`integration-attempt-1.md`, `-2.md`, `lead-ci-attempt-1.md`, `-2.md`). `git diff --stat b242aa2 b4f2342` → only
   `report.md`, `integration-attempt-2.md` and `lead-ci-attempt-2.md`.
6. `git ls-tree -r -l b4f2342 | sort -k4 -n -r | head` → the largest committed file is
   `models/champion/python_model.pkl` at 30,830,306 bytes. Nothing is over 50 MB.
7. **The whole suite in CI mode.** I read the runner first: it `git archive`s the SHA into
   `.local/tmp/cp-17-probe/critic3-ci312/`, `git init`s that scratch copy and commits once, with the repository's
   `.githooks`. That is the brief's single-commit copy, not a write to this repository. Then it syncs offline
   (`UV_OFFLINE=1`, the project uv cache), runs the workflow's seven steps with `CI=true`, collects the `stress`
   tests, and removes the copy.
   Command: `python3 /Users/djourno/Downloads/PJM/.local/artifacts/cp-17-probe/critic3-runner.py b4f2342… ci312`
   → exit 0 (2026-10-27T17:19:21Z–17:28:18Z).
   `critic-validation-3/ci312/results.json`: tree 7c6631e1…, `complete: true`, `scratch_removed: true`. Steps:
   - `uv sync --locked --dev` → 0.
   - `python3 --version` and `uv run python --version` → both `Python 3.12.14`.
   - `build_wasm_payload.py` → 0 (76.1 s).
   - `uv run pytest -q` → 0: **2256 passed, 38 skipped** in 441.5 s.
   - `tests/test_10_cqr_order_statistic.py` → 0 (8 passed).
   - `verify_release.py` → 0.
   - `tests/test_22_wasm_equivalence.py` → 0 (15 passed).
   - `publication_guard.py tree` → 0 ("the tree carries no placeholder and a final build record").
   - `pytest --collect-only -m stress` → 0: 17 of 2293 tests collected, including
     `tests/cp17probe/test_probe_browser.py::test_one_browser_measurement_reproduces_the_committed_record`.

   The CP-17-probe skips in step 03 all state a reason:
   - `test_probe_browser.py`: "the pinned Pyodide 0.28.0, Playwright 1.63.0 browsers and probe payloads
     (.local/, never committed) are absent";
   - the four `test_probe_real_inputs.py` tests: "CP-26's local-only stored state (evidence/cp-26 extract and
     fit cache) is absent";
   - the CP-26 `stress` tests: the conftest's stated CI reason.
8. **`pytest -m stress`, CI unset:** the same runner with mode `stress` → exit 0 (17:28:39Z–17:33:16Z). Step
   `uv run pytest -m stress -q` → **17 passed, 1 skipped, 2276 deselected** in 246.6 s. The one skip is the
   collection-time `eccodes` import skip, which also appears in the CI collection. All 17 stress tests ran and
   passed, the CP-17-probe browser test among them. `results.json`: `complete: true`, `scratch_removed: true`.
   This ran alone, with no other job on the machine.
9. **The real inputs (embargo and A1 parity):**
   `OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 /Users/djourno/Downloads/PJM/.venv/bin/python -m pytest -p no:cacheprovider tests/cp17probe/test_probe_real_inputs.py -q -rs`
   → exit 0, **4 passed** in 34.6 s.
10. **The full native reference for all three fits, outside the worktree.** I ran `src/cp17probe/reproduce.sh`'s
    first command with `--out /Users/djourno/Downloads/PJM/.local/tmp/cp-17-probe/critic3-native`, BLAS at one
    thread, `PYTHONPATH=src` → exit 0. Output: `A1-2026-09-06 bitwise selections True 15.0s`,
    `A1-2026-03-29 bitwise selections True 16.2s`, `v2-2026-09-06 bitwise selections True 14.7s`, `PASS 68s`.
    I then compared that output with the committed `native-reference.json`, field by field and leaving out the
    timing fields and output paths: **0 differences**. All six payload files are byte-identical to the Lead's
    `.local/artifacts/cp-17-probe/final/payloads/`, which the browser test serves. The folder was then removed.
11. **One browser measurement, rerun:**
    `CP17_PROBE_BROWSERS=chromium,webkit /Users/djourno/Downloads/PJM/.venv/bin/python -m pytest -p no:cacheprovider -m stress tests/cp17probe/test_probe_browser.py -q -rs --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-17-probe/critic3-browser`
    → exit 0, **1 passed** in 143.9 s.
    I then read the rerun's `browser-results.json` myself:
    - Chromium 153.0.8010.12 and WebKit 26.6, A1 2026-09-06, Pyodide 0.28.0.
    - The quantiles are bit-identical to the committed record in both browsers (hash and values), and so are the
      attribution φ.
    - Every member record is equal apart from `seconds`.
    - Fit 65.7 s (Chromium) and 62.3 s (WebKit); committed 65.8 s and 62.0 s. WebAssembly memory 214.8 MiB in both.
    - `blocked_non_local_requests` [], `errors` [], `not_found` [].

    The folder was then removed.
12. **The committed records, recomputed:**
    `/Users/djourno/Downloads/PJM/.venv/bin/python -m pytest -p no:cacheprovider tests/cp17probe/test_probe_records.py tests/cp17probe/test_probe_units.py -q`
    → exit 0, **22 passed** in 3.4 s.
13. **The independent record checks (inline `python3 -c`, read-only):**
    - CP-26's stored nominal forecasts against the native records, IEEE-754 bits: A1-2026-09-06 168 of 168 values
      bitwise, A1-2026-03-29 161 of 161, v2-2026-09-06 168 of 168.
    - The input extract against the local tag `evidence/cp-26` (`ca203312…`): 20 of 20 files identical
      (`git show evidence/cp-26:<path> | shasum`).
    - The per-member browser−native deviation, epochs run and best epoch; the configurations from k12/k13.
    - Chromium against WebKit, field by field: only `fit_seconds`, `members[].seconds` and
      `attribution.seconds` differ.
    - Node.js against the browsers.
    - The served bytes by file.
    - The retrieval manifest against the files on disk (sha256 and size).
    - Overlaps in the compute ledger.
    - A scan of every new file for ISO dates after 2026-09-06.
14. `sysctl -n machdep.cpu.brand_string hw.memsize hw.ncpu; sw_vers -productVersion` → Apple M3, 17179869184,
    8, 26.5.2. `node --version` → v26.7.0, installed 2026-08-05 (Homebrew), before this checkpoint.
    `.local/tools/playwright/bin/python` → playwright 1.63.0.
15. Final: `git status --porcelain` → empty; `HEAD` → b4f23422c60e40fa8f0d3f523c28605f5451d589.

## Evidence actually inspected

- **`reports/cp17-probe/report.md`**, every line, against the committed records:
  - `measurements.json`: all 6 runs, `node_pyodide`, `native_runtime` and `browser_host`;
  - `browser-results.json`: the runs, served files, `source_sha256`, marks and member records;
  - `native-reference.json`: results, checks, attribution and member records;
  - the three `node-*.json`;
  - `bundle-manifest.json`, `retrieval-manifest.json` and `compute-ledger.jsonl`.
- **Code read:**
  - `src/cp17probe/`: `dailyfit.py` (`fit_a1`, `fit_v2`, `run`), `native.py`, `compare.py`, `attribution.py`,
    `browser/worker.js`, `browser/driver.py`, the routing in `measure.py`, and `reproduce.sh`;
  - `tests/cp17probe/`: all four files;
  - `tests/conftest.py`'s stress skip and `.github/workflows/tests.yml`'s seven steps;
  - the landed `cp24.execution.fit_origin`, the import chain behind proposal 4, κ's use in `cp24/ddnn2.py`, and
    `cp24.design.Preprocessor`.
- **CP-26 inputs:** `.local/artifacts/cp-17-probe/inputs/…/search-results/nominal/k12.json` and `k13.json` (search
  days, chosen configurations), `forecast-ledger/2026-09-06.json` and `2026-03-29.json` (`nominal/D2` and
  `nominal/v2`), and `parity.json` (the bit representation is IEEE-754 bits).
- **Pinned runtimes:**
  - `.local/tools/pyodide-0.28.0/`: 23 of 23 files match the manifest by sha256 and size; 17 of 17 package files
    match the release's `pyodide-lock.json`; 44,962,352 bytes in total;
  - `.local/tools/ms-playwright/chromium-1243`: 348 files and 375,624,473 bytes, as recorded; the Chrome binary's
    sha256 is 8319963f…, as recorded;
  - `webkit-2359` and `ffmpeg-1011` are present.
- **The earlier verdicts** `integration-attempt-1.md` and `-2.md`: their FAIL findings and acceptance tests, to
  confirm that this candidate corrects them.

**The report's figures, checked against the records.** All match:

- **The measurement table.**
  - Fit time: Chromium 65.8, 73.3 and 44.4 s; WebKit 62.0, 70.2 and 43.3 s.
  - Attribution: 0.34, 0.22, 0.32 and 0.20 s.
  - Native fit: 14.8, 15.6 and 24.5 s.
  - WebAssembly memory: 214.8, 187.1 and 257.8 MiB in Chromium; 214.8, 214.8 and 257.8 MiB in WebKit.
  - Browser processes: 1.60, 1.59 and 1.70 GiB in Chromium; 1.33, 1.33 and 1.42 GiB in WebKit.
  - Max abs: 9.4e-13, 6.3e-7 and 5.1e-13. Status: "different" throughout.
  - Node: 66.8, 72.7 and 44.6 s, 187.1–273.9 MiB.
- **Startup and payloads.**
  - Startup: 1.74–2.06 s.
  - First visit: 3,189 B (gzip 1,582 B).
  - Runtime: 12,259,068 B. Packages: 31,727,367 B for A1 and 32,687,456 B for v2.
  - Code: 51,600 B (`src.zip` 50,009 B plus the driver).
  - Data: 531,903 and 539,285 B for A1, 1,506,934 B for v2.
  - Training payload A1: 44,577,320 B (gzip 37,242,721 B).
  - NumPy, pandas, six, dateutil, pytz and tzdata: 9,498,766 B, the report's "9.5 MB".
- **Per member.** The configurations, epochs run, best epochs and browser−native maxima for all 16 members are
  exactly the report's table. For example, k13 `t005` ran 939 and 768 epochs at 2.3e-13 and 2.0e-13; k12 `t096`
  ran 338 (288) and 300 (250) at 1.8e-6 and 6.0e-7. Only those two members exceed 2e-11; the next largest is
  1.5e-11.
- **`t096`'s configuration:** softplus, hidden [140], `z-s4`, batch 32, lr 1.477e-4, κ = 0. κ = 0 means pinball loss
  only after `WARM_EPOCHS`, per `cp24/ddnn2.py`.
- **Attribution.**
  - Players: 10 on 2026-09-06 (all but `calendar`) and 9 on 2026-03-29 (all but `price_d2` and `calendar`).
  - Coalitions: 1,024 and 512.
  - Efficiency residual: at most 1.42e-13 (browser) and 1.14e-13 (native).
  - Issued gap: 0 in the browsers and at most 4.26e-14 natively.
  - Browser−native φ: at most 2.06e-7.
  - Native cost: 0.082 and 0.109 s.
- **Retrieval:**
  - Pyodide: 23 files, 44,962,352 B; 17 package files checked against the lock.
  - Chrome for Testing 153.0.8010.12: 190,970,181 B.
  - FFmpeg not fetched; `data_bytes_retrieved` 0.
- **Compute:** 0.3563 machine-hours to the final measurement.
- **Bundle:** 17 landed files, 3 probe modules and 2 stand-ins, as the union of the files A1 and v2 executed.
  Every executed file's hash equals the checkout's.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | **The measurement** under Pyodide in Chromium and WebKit: A1 retrained for 2026-09-06 and the DST day 2026-03-29, each from its training window, code, seed and selection rules, then the day's quantiles predicted. Recorded per browser and day: wall time and peak memory; first-visit and training payload sizes; max abs difference per emitted quantile against the native fit, in EUR/MWh, and whether bitwise; whether every selection matched. The same for v2 for one day. | PASS | `measurements.json` holds all six runs (2 browsers × A1 ×2 days + v2 2026-09-06): `time_seconds` (fit, attribution, startup marks, `total_in_worker`), `memory_bytes` (WebAssembly peak, browser RSS peak), `payload` (first visit, training payload raw and gzip), `deviation.max_abs_eur_by_level` for all seven levels, `bitwise_equal`, and `selections.all_match` = true everywhere. My browser rerun (command 11) reproduced the committed A1 2026-09-06 record bit for bit in both browsers. |
| 2 | **The native reference:** the same two A1 fits and one v2 fit natively, reproducing CP-26's stored forecasts to CP-26's parity standard (bitwise); the browser fits compared against them. | PASS | `native-reference.json` is `status` PASS with every check `bitwise_equal`. My own IEEE-754 bit comparison against the ledger's `nominal/D2` and `nominal/v2` matches all 168, 161 and 168 values. My rerun of the full native reference (command 10) reproduced the committed record exactly, and `test_probe_real_inputs.py` passed 4 of 4. CP-26's recorded member selections (best epoch, epochs run, stop reason, `params_sha256`, `n_inputs`, window and train-day hash, cap levels) all match. The browser deviations are computed against these fits (`compare.py`; recomputed in `test_probe_records.py`). |
| 3 | **Proposals,** each with its reasoning: τ_eq; the reference browser and runtime (versions, Pyodide, machine class, the limits a visitor is told); the attribution method for A1 (§19.7) with its in-browser cost; the one-code-path design (§19.2) and what CP-17 must freeze. | PASS | All four are present and reasoned (report §§ Proposals 1–4). The τ_eq reasoning now agrees with the records: 2 of 16 member fits, both of one of the eight configurations, exceed 2e-11. Its margins also hold: 0.01 is about 1.6e4 times 6.3e-7, and 0.001 about 1.6e3 times. The runtime versions match `retrieval-manifest.json` and the browser records. The machine class is true of this machine (`sysctl`), although "Apple M3" and "16 GB" are not in a committed record (see notes). The attribution cost and residuals match the records. Proposal 4's import-chain and Node-cost claims match the code and the records. |
| 4 | **The blocker route** (§19.3 item 5): BLOCKED with the numbers if infeasible within limits a visitor can meet or if selections do not match; the requirement never dropped or replaced. | PASS (correctly not triggered) | Every selection matched in every run. A1 takes about 62–73 s of fit (66.6–78.7 s in the worker in all) with at most 215 MiB of WebAssembly memory and a one-time 44.6 MB download. Those are limits a visitor can meet. The report says the route is not triggered, drops nothing, and states its limits, unmeasured browsers among them. |
| 5a | Development data only: no delivery day after 2026-09-06 read, recorded or mentioned. | PASS | A date scan of all 34 new files finds after 2026-09-06 only document and run dates (2026-09-30, 2026-10-15, 2026-10-25, 2026-10-27) and S_14 = 2027-01-06. S_14 is a search-protocol date quoted from the anchor's §24.9 ("protocol dates only, never permission to read future data"), and the report labels it so. No record holds a delivery day after the boundary, and `test_no_record_holds_a_day_after_the_boundary` passes. Every payload ends at D with D's outcome blanked (A1 test lines 46–68; v2 test 71–82, which also refuses a day after the boundary). |
| 5b | Software retrieval limited to the two pinned runtimes; no data retrieved. | PASS | `retrieval-manifest.json`: Pyodide 0.28.0 from `cdn.jsdelivr.net` (23 files, verified on disk) and Chrome for Testing through Playwright 1.63.0 (the installed tree's file count, bytes and binary hash all verified); `data_bytes_retrieved` 0. Node.js v26.7.0 was preinstalled (2026-08-05). Whether any other network contact happened cannot be checked from records beyond the manifest and the zero `blocked_non_local_requests`. |
| 5c | No committed file over 50 MB. | PASS | The largest is 30,830,306 B (command 6). |
| 5d | The workflow's seven steps green on a history-free single-commit copy with `CI=true` and Python 3.12. | PASS | Command 7: all seven steps exit 0 on Python 3.12.14; 2256 passed, 38 skipped. |
| 5e | Browser tests skip with a stated reason when the runtimes are absent. | PASS | In CI mode `test_probe_browser.py` skipped with the stated reason quoted in command 7, and the real-input tests with theirs. |
| 5f | Timing-sensitive tests carry the `stress` marker. | PASS | `test_probe_browser.py` carries `pytest.mark.stress` and is collected by `-m stress` (command 7, step 08). The probe's other tests are not timing-dependent: units, record recomputation and bitwise parity. |
| 5g | No pinned file and no landed code changed; new code only under the allowed paths. | PASS | `git diff --name-status f7c9035 b4f2342`: 34 additions, none modified or deleted, all under `src/cp17probe/`, `tests/cp17probe/` (new), `reports/cp17-probe/` and `docs/track-b/evidence/cp-17-probe/`. So `src/cp26/`, `src/cp15/`–`src/cp28/`, `src/delu_forecast/`, `data/`, earlier `reports/`, `pyproject.toml`, `uv.lock`, the anchors and the governance files are unchanged from `f7c9035`. |
| 5h | The Integration Critic reruns one browser measurement and the whole suite in that CI mode. | PASS | Commands 7, 8 and 11. |
| §19.3.1 | Retrains the daily fit of one issued delivery day from its shipped training window with the same code, seed and selection rules, then predicts the day's quantiles. | PASS | `dailyfit.fit_a1` calls the landed `cp24.member.fit_member`/`emit_rows`/`ddnn2.ensemble_median` with the payload's day table (D−735..D) and the eight frozen members' configurations and seeds. The browser executed the checkout's landed files byte for byte (`source_identical_to_checkout`, `test_the_browsers_executed_this_checkouts_files`, and my rerun). |
| §19.3.2 | Reports selection agreement, the max abs difference per emitted quantile in EUR/MWh, and a status stating only what was measured. | PASS | `compare.py` and `measurements.json`: `selections.all_match` with per-member differences; `max_abs_eur_by_level` for p025–p975; status "identical bit for bit" or "different", as no τ_eq exists yet. The report's status rule proposes the third state for CP-17. |
| §19.3.4 | A probe on development data measures, for A1, browser time and memory, payload sizes, the deviation from the native fit and selection agreement, before the CP-17 freeze. | PASS | Items 1–2 above. Days 2026-09-06 and 2026-03-29 are development days. |
| §19.3.5 | The blocker route if the policy cannot meet the requirement; never dropped silently; never met by a different implementation. | PASS | Item 4 above. The browser fit is the landed implementation; the stand-ins are import-only and disclosed. |
| §19.2 | The daily-fit code is the code the browser runs; no second implementation stands in; a component that cannot run in the browser is reported, never replaced silently. | PASS | The landed model code runs unchanged under Pyodide. The two import-only stand-ins (`holidays`, which raises on use; `resource`, which feeds a record field) are disclosed. The restated glue matches `cp24.execution.fit_origin` (lines 138–169) on reading: the same member loop, uncovered-window check, `emit_rows` and ensemble median. Bitwise CP-26 parity on all three fits confirms it. `cp24.execution` and `cp26` not loading in a browser is reported, and proposal 4 states what CP-17 must freeze. |
| — | Check also: the report's figures are those in `measurements.json` and the other committed records. | PASS, with notes | Every figure listed under *Evidence actually inspected* matches. The two earlier FAIL findings are corrected: the deviation is attributed to configuration, not training length; `t096`'s epochs are right; the 939- and 768-epoch members are cited; and the count is 16 DDNN-2 member fits. The notes below are minor and not decision-bearing. |
| — | Check also: blocker route not triggered; proposals reasoned; retrieval software-only; no record dated after 2026-09-06; protected paths unchanged. | PASS | Items 4, 3, 5b, 5a and 5g. |

**Notes (not decision-bearing; none changes a measurement, a proposal or the τ_eq premise):**

1. **The report's "One worker at a time" (Retrieval and compute) is off by a 13-second overlap.**
   - In the committed `compute-ledger.jsonl`, `attribution-native-check` starts 13.0 s before
     `browser-measurement-1` ends; that measurement run is the failed one, with exit 1.
   - The ceiling allows 4 workers, so this breaches nothing, and the 0.36 machine-hour total is unaffected.
2. **About 3 s of in-worker time sits between the startup mark (`payload_ms`) and the fit timer, and is not
   itemised.** It is spent importing the landed chain (scikit-learn, SciPy) and loading the payload.
   - The "Fit" column and "1.7–2.1 s" startup are accurate as labelled.
   - The full in-worker time (66.6–78.7 s for A1) is in `measurements.json` as `total_in_worker`.
   - The proposed visitor wording ("about 1–1.5 minutes") covers it.
3. **The reference machine's "Apple M3" and "16 GB" are true of this machine but are not in a committed record.**
   `browser_host` holds 8 cores, arm64 and macOS 26.5.2. CP-17 should record the full machine class if it freezes it.
4. **The report's list of diagnostics is not exhaustive.** `compare.py` also treats `cap_z`, LEAR's absolute alpha,
   solver passes and validation MAE as diagnostics. The report does not claim to be exhaustive, and the selections
   it lists match `compare.A1_SELECTIONS`/`H_SELECTION`.
5. **Not independently tested:** that Playwright's `context.route` intercepts requests from the dedicated Web Worker
   in WebKit. Every runtime and package file was served by, and counted at, the local server: the served lists
   account for every byte, and `not_found` is empty.
6. **Procedural.** The runner rewrites `.local/artifacts/cp-17-probe/history-free-message.txt` (its commit message
   file) and makes one commit in its own scratch copy, as the brief describes. I made no Git write to this
   repository or worktree. My scratch folders under `.local/tmp/cp-17-probe/` (`critic3-native`, `critic3-browser`)
   were removed.

## On FAIL only

Not applicable (PASS).
