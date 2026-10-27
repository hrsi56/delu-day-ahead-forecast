# Verdict — CP-17-probe — Integration — FAIL

- Candidate SHA: 4f1c0d7c08d2f51010279b75de566eb9e57e502e
- Plan / version / bar: `capstone_v21.md`, v21-r17 (SHA-256 3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc
  at the candidate), §19.3 "Train it yourself" is required (items 1, 2, 4 and 5) and §19.2 One code path; the issued
  brief `docs/track-b/evidence/cp-17-probe/issued-brief.md` (SHA-256 2afc610e2c3f61b4ba862a8b1d2b1cf878764900ad11f4b5832634df8c53b155),
  its Observable outcome 1–4 and Further items 1–5.
- Verbatim bar excerpt (extracted with `scripts/bar.py bar` at the candidate: section 25 lines, 1354 bytes, sha256
  5d1f869e153bac43b8f049ee8395b317f48a28e65282109eb107821ef28e582e, as the brief records):

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

  and (section 6 lines, 335 bytes, sha256 538342106768fedad8201f44bd4aadc3de02415cebf321cd0c1584eca75f6f7c):

> ### 19.2 One code path
>
> The code that performs the daily fit, issuance and scoring is the code the Space runs in the
> browser for §19.3 and §19.5. No second implementation stands in for the product. A component
> that cannot run in the browser runtime is reported at CP-17 under §19.3's exception route; it is
> never replaced silently.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: yes. `git status --porcelain` was empty before the review and after it, and `HEAD`
  stayed 4f1c0d7c08d2f51010279b75de566eb9e57e502e. The only byproducts in the worktree are gitignored `__pycache__/`
  folders, written by `cp17probe.bundle.closure`'s subprocess, which strips the environment.

## Commands actually run

All commands ran with `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1`, with `CI` unset unless the runner set it. There
was no network contact, no `git fetch` and no download. No Git write was made in the repository or the worktree. The
runner's `git init` and commit happen inside its own throwaway history-free copy, as the brief prescribes, and the
runner then removes that copy.

| # | Command (from the worktree unless stated) | Exit | Observed output |
|---|---|---|---|
| 1 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief cp-17-probe` | 0 | This assignment. `scripts/gauntlet.py` and `scripts/bar.py` in the worktree are identical to `main` (`f7c9035c8c…`). |
| 2 | `git status --porcelain`; `git rev-parse HEAD` | 0 | Empty; `4f1c0d7c08d2f51010279b75de566eb9e57e502e`. |
| 3 | `python3 scripts/bar.py bar capstone_v21.md '19.3 "Train it yourself" is required' --at 4f1c0d7…` | 0 | Plan sha256 `3124451d…`; section 25 lines, 1354 bytes, sha256 `5d1f869e…`. The text is identical to the brief's excerpt. |
| 4 | `python3 scripts/bar.py bar capstone_v21.md '19.2 One code path' --at 4f1c0d7…` | 0 | Section 6 lines, 335 bytes, sha256 `53834210…`. The text is identical to the brief's. |
| 5 | `shasum -a 256 docs/track-b/evidence/cp-17-probe/issued-brief.md`; `cmp` against `.local/artifacts/cp-17-probe/issued-brief.md` | 0 | `2afc610e…c53b155`; byte-identical to the canonical brief. |
| 6 | `git diff --name-status f7c9035 4f1c0d7…` | 0 | 30 paths, all `A`, all under `src/cp17probe/`, `tests/cp17probe/`, `reports/cp17-probe/` or `docs/track-b/evidence/cp-17-probe/`. No path is outside those prefixes. |
| 7 | `git diff --quiet f7c9035 4f1c0d7… -- src/cp15 … src/cp28 src/delu_forecast data pyproject.toml uv.lock AGENTS.md CLAUDE.md engineering-role.md orchestrator-role.md notebooklm-role.md docs/track-b/{gauntlet-templates,rule-inventory,cp-0-defects,backup-register,exposure-ledger}.md docs/PUBLISH_RULES.md .claude .githooks .github scripts tests/conftest.py progress.md`, and the same for `capstone_*.md`, `syllabus_v*.md` and `program-stage-sequence.md` | 0 | No difference on any of these paths. |
| 8 | `git ls-tree -r -l 4f1c0d7…` filtered for files over 50,000,000 bytes | 0 | None. The largest blob is the pre-existing `models/champion/python_model.pkl` (30,830,306 bytes). The largest new file is `browser-results.json` (413,805 bytes). |
| 9 | `python3 .local/artifacts/cp-17-probe/critic-runner.py 4f1c0d7… ci312` (read first; it strips credentials from the environment, runs `UV_OFFLINE=1` and hides the local inputs) | 0 | Copy tree `beb5c04b…` equals the candidate's tree, as one commit. Python 3.12.14. Steps: `uv sync --locked --dev` 0; `build_wasm_payload.py` 0; `pytest -q` 0, **2256 passed, 38 skipped** in 443.68 s; `test_10_cqr_order_statistic.py` 0 (8 passed); `verify_release.py` 0 (PASS); `test_22_wasm_equivalence.py` 0 (15 passed); `publication_guard.py tree` 0; `pytest --collect-only -m stress` 0 (17 collected). The copy was removed. |
| 9a | (from 9's `03-pytest.log`) | — | The probe skips state their reasons: `test_probe_browser.py: the pinned Pyodide 0.28.0, Playwright 1.63.0 browsers and probe payloads (.local/, never committed) are absent`, and `test_probe_real_inputs.py:46/59/71/85: CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent`. |
| 10 | `python3 .local/artifacts/cp-17-probe/critic-runner.py 4f1c0d7… stress` (CI unset) | 0 | Python 3.12.14; `uv run pytest -m stress -q`: **17 passed, 1 skipped**, 2276 deselected in 247.74 s. The copy was removed. |
| 10a | `pytest -p no:cacheprovider -m stress --co -q -rs` (CI unset) | 0 | 17 stress tests collected, `tests/cp17probe/test_probe_browser.py::test_one_browser_measurement_reproduces_the_committed_record` among them. The one skip is the collection-time `tests/cp20/test_gfs_eccodes.py` (no `eccodes`). So in step 10 the probe browser test **ran and passed**. |
| 11 | `CP17_PROBE_BROWSERS=chromium,webkit .venv/bin/python -m pytest -p no:cacheprovider -m stress tests/cp17probe/test_probe_browser.py -q -rs --basetemp=.local/artifacts/cp-17-probe/critic-1/browser-rerun` | 0 | **1 passed in 147.59 s.** In the kept rerun output, both Chromium 153.0.8010.12 and WebKit 26.6 have A1 2026-09-06 quantiles **bitwise equal to the committed record**. Both are 9.379e-13 from native, with identical member records and attribution φ, no error, no blocked non-local request, no 404 and Pyodide 0.28.0. The rebuilt bundle's zip sha256 `d132571a…` and file hashes equal `bundle-manifest.json`. |
| 12 | `OPENBLAS/VECLIB/OMP/MKL/NUMEXPR_NUM_THREADS=1 .venv/bin/python -m pytest -p no:cacheprovider tests/cp17probe/test_probe_real_inputs.py -q -rs` | 0 | **4 passed in 35.06 s.** These cover the A1 embargo, outcome-independence and window-sensitivity, the v2 D-2 and boundary refusals, and A1 2026-09-06 bitwise equal to CP-26 with all selections matching. |
| 13 | Same BLAS settings, `PYTHONPATH=src .venv/bin/python -m cp17probe.native --root . --inputs …/cp-17-probe/inputs --fits …/fits/195857d7…/nominal --state …/state/e17f95f7…/replay-state.json --out .local/artifacts/cp-17-probe/critic-1/native` | 0 | `A1-2026-09-06 bitwise selections True 15.0s`; `A1-2026-03-29 bitwise selections True 16.0s`; `v2-2026-09-06 bitwise selections True 23.6s`; `PASS 77s`. The quantile, payload and attribution hashes equal the committed `native-reference.json`. |
| 14 | `.venv/bin/python -m pytest -p no:cacheprovider tests/cp17probe/test_probe_records.py tests/cp17probe/test_probe_units.py -q` | 0 | **22 passed in 3.50 s.** |
| 15 | Hash check of `.local/tools/pyodide-0.28.0/*` against `retrieval-manifest.json` and the release's `pyodide-lock.json` | 0 | 23 files, 44,962,352 bytes, 0 mismatches, no extra file. All 17 wheels/zips equal the lock. The lock closure of the six requested packages is exactly those 17. |
| 16 | Fingerprint of `.local/tools/ms-playwright/chromium-1243` (sha256 over sorted `relpath\0sha256\n`), plus the binary's sha256 and `playwright` version | 0 | 348 files, 375,624,473 bytes. Tree `955ce3e0…` and binary `8319963f…` equal the manifest. Playwright 1.63.0. `webkit-2359` and `ffmpeg-1011` are present. |
| 17 | `git -C <primary> archive evidence/cp-26 <path> \| tar -xO \| shasum` against `.local/artifacts/cp-17-probe/inputs/<path>` | 0 | `evidence/cp-26` = `ca203312…`. The forecast ledgers 2026-09-06 and 2026-03-29, search results k12 and k13, and `parity.json` match the tag. `parity.json`'s standard is "each float64 as its uint64 IEEE-754 bits", status PASS. |
| 18 | `cmp` of `reports/cp17-probe/*` against `.local/artifacts/cp-17-probe/final/*` | 0 | `browser-results`, `measurements`, `native-reference`, the three `node-*` files and `bundle-manifest` (= `final/bundle/src.json`) are identical. The final payloads' `payload_sha256` and byte sizes equal `native-reference.json`. |
| 19 | Date scan (`20YY-MM-DD` later than 2026-09-06) over every committed probe file | 0 | The data records hold none. Found: `2026-10-27` in `report.md` and `retrieval-manifest.json` (measurement and authorisation date); `2026-10-15` in `native.py`, `reproduce.sh` and `test_probe_real_inputs.py` (CP-26's run folder `cold-rerun-2026-10-15`); governance dates in the issued brief. None is a delivery day. |
| 20 | `sysctl machdep.cpu.brand_string hw.ncpu hw.memsize`; `sw_vers`; `node --version` | 0 | Apple M3, 8, 17179869184, 26.5.2, v26.7.0. This is the report's machine class. |
| 21 | `git show main:scripts/bar.py \| python3 -I - check <this verdict> --source capstone_v21.md@4f1c0d7c08d2f51010279b75de566eb9e57e502e` | 0 | `ok: lines 11–35 (1353 bytes) appear in capstone_v21.md@4f1c0d7c08d2`; `ok: lines 39–44 (334 bytes) appear …`. |
| 22 | `git status --porcelain`; `git rev-parse HEAD`, after the review | 0 | Empty; `4f1c0d7c08d2f51010279b75de566eb9e57e502e`. |

## Evidence actually inspected

- **Code, read in full:** `src/cp17probe/{__init__,dailyfit,payload,native,bundle,measure,compare,attribution}.py`,
  `node_run.mjs`, `reproduce.sh`, `browser/{index.html,worker.js,driver.py}`, both stubs, and the four test files.
  I compared the restated glue with the landed `cp24.execution.fit_origin` (lines 138–169) and found it equivalent.
  `tests/conftest.py` (stress handling) is unchanged.
- **Records:** `report.md` in full. Computed from `measurements.json`, `native-reference.json`, `browser-results.json`,
  `bundle-manifest.json`, `retrieval-manifest.json`, `compute-ledger.jsonl` and the three `node-*.json`:
  - every table figure;
  - per-member epochs run, best epoch and browser−native deviation;
  - memory in bytes, MiB and GB;
  - payload bytes by category.
- **Inputs:** the CP-26 extract and `parity.json`, the pinned runtimes, and the Lead's `final/` outputs. I did not
  read the Lead's logs, drafts or launch envelope.

**What the measurement shows, all of which I reproduced:**

- The three native fits are bitwise CP-26, with every recorded selection reproduced.
- Six browser runs (Chromium 153.0.8010.12 and WebKit 26.6 × A1 2026-09-06, A1 2026-03-29 (DST), v2 2026-09-06):
  - **all selections match;**
  - max |browser − native| is 9.38e-13, 6.28e-7 and 5.12e-13 EUR/MWh;
  - the status is "different" in every run;
  - the A1 fit took 62.0–73.3 s; v2 took 43.3–44.4 s.
- Chromium, WebKit and Node.js under Pyodide 0.28.0 are bitwise equal to one another on all three fits.
- WebAssembly memory peaks at 196.2–270.3 MB (187.1–257.8 MiB). The browsers' summed process RSS is 1.43–1.82 GB.
- The training payload is 44,577,320 bytes for A1 (37,242,721 gzip) and 46,505,058 for v2. The first visit is 3,189
  bytes.
- No non-local request was made. The browsers executed exactly the checkout's 17 landed and probe files, plus the two
  stand-ins.
- Compute was 0.356 machine-hours.

**Per-member records,** epochs run and max |browser − native| in EUR/MWh:

- **A1 2026-09-06:**
  - t040: 145 epochs (8.5e-13), 259 (4.6e-13)
  - t094: 147 (1.5e-11), 86 (2.8e-13)
  - t030: 92 (4.6e-13), 119 (4.6e-13)
  - t005: **939, best epoch 889** (2.3e-13), 768 (2.0e-13)
- **A1 2026-03-29:**
  - t041: 94 (2.4e-13), 92 (2.3e-13)
  - t083: 73 (6.0e-13), 86 (2.1e-12)
  - t108: 441 (2.6e-13), 334 (5.4e-13)
  - t096: **338, best epoch 288** (1.8e-6), **300, best epoch 250** (6.0e-7)
- DDNN-2's `MAX_EPOCHS` is 1000 (`src/cp24/ddnn2.py:72`).

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | **The measurement** under Pyodide in Chromium and WebKit: A1 retrained for 2026-09-06 and 2026-03-29 from its window, code, seed and selection rules; per browser and day, wall time and peak memory, first-visit and training payload sizes, the largest absolute difference per emitted quantile and bitwise status, and selection agreement; the same for v2 for one day. | PASS | `measurements.json`: 6 runs, all fields present (`time_seconds`, `memory_bytes`, `payload`, `deviation.max_abs_eur_by_level`, `bitwise_equal`, `selections.all_match`). I reran A1 2026-09-06 in both browsers (row 11): bitwise equal to the committed record. |
| 2 | **The native reference:** two A1 fits and one v2 fit natively, reproducing CP-26's stored forecasts to CP-26's parity standard, with the browser fits compared against them. | PASS | Rows 12 and 13: all three fits are bitwise equal to CP-26's stored nominal D2 and v2 forecasts (`parity.json`: IEEE-754 bits), with every recorded selection reproduced. The inputs equal `evidence/cp-26` (row 17). `compare.build` compares the browser fits against these. |
| 3 | **Proposals,** each with its reasoning: τ_eq; the reference browser and runtime; the attribution method for A1 (§19.7) with its in-browser cost; the one-code-path design (§19.2) and what CP-17 must freeze. | **FAIL** | All four proposals are present and reasoned. But the τ_eq reasoning and the report's account of the deviation that it rests on are contradicted by the committed records (see below). |
| 4 | **The blocker route** (§19.3 item 5): BLOCKED with the numbers if A1 is infeasible within limits a visitor can meet, or if selections do not match. | PASS | Every selection matches in every browser run. A1 fits in 62–73 s on the reference machine, with about 45 MB downloaded on request. Not triggering the blocker is correct. The report states its limits (unmeasured phones and Firefox; process RSS overstates the fit's need). |
| 5a | Development data only: no delivery day after 2026-09-06 read, recorded or mentioned. | PASS | `payload._admit` uses `cp25.guard` and the boundary refusal is tested (row 12). Row 19: no delivery day after 2026-09-06 in any record. The later dates found are the measurement date and CP-26's run label, not delivery days. |
| 5b | Software retrieval limited to the two pinned runtimes; no data retrieved. | PASS | Rows 15 and 16: `retrieval-manifest.json` lists only Pyodide 0.28.0 (23 files, all hashes and the lock verified) and Chrome for Testing 153.0.8010.12 (the installed tree verified), with `data_bytes_retrieved: 0`. The Chromium archive's SHA-256 is `null`; the manifest states why, and the installed tree and binary are fingerprinted instead. |
| 5c | No committed file over 50 MB. | PASS | Row 8. |
| 5d | The workflow's seven steps green on a history-free single-commit copy, `CI=true`, Python 3.12. | PASS | Row 9: all seven steps exit 0 under Python 3.12.14 on a one-commit copy of tree `beb5c04b…`. |
| 5e | Browser tests skip with a stated reason when the runtimes are absent. | PASS | Row 9a. |
| 5f | Timing-sensitive tests carry the `stress` marker. | PASS | The browser rerun is `pytestmark = [pytest.mark.stress, …]`. The other probe tests assert no timing. Row 10a. |
| 5g | No pinned file and no landed code changes; new code only under `src/cp17probe/`, `tests/` (new files), `reports/cp17-probe/` and `docs/track-b/evidence/cp-17-probe/`. | PASS | Rows 6 and 7: 30 additions, all inside the allowlist. Every protected path is unchanged from `f7c9035`. |
| 5h | The Integration Critic reruns one browser measurement and the whole suite in that CI mode. | PASS | Rows 9, 10 and 11. |
| §19.3.1 | In the browser, retrain one issued day's daily fit from its shipped training window with the same code, seed and selection rules, then predict the day's quantiles. | PASS | The payload ships D−735..D with D's outcome blanked (row 12 proves outcome-independence). The browser executes the landed `cp24`/`cp15`/`cp16`/`cp21`/`delu_forecast` files byte for byte (hashes equal the checkout; row 11). Seeds and configs come from CP-26's serving search. |
| §19.3.2 | Reports selection agreement, the largest absolute difference per emitted quantile in EUR/MWh, and a status stating only what was measured. | PASS | `compare.build`: `selections.all_match`, `deviation.max_abs_eur_by_level`, and `status` ∈ {"identical bit for bit", "different"}, since no τ_eq exists yet. Recomputed by `test_probe_records.py` (row 14) and by me. |
| §19.3.4 | On development data, for the designated policy A1: browser time and memory, payload sizes, deviation from the native fit, selection agreement. | PASS | Item 1 above. The measurement itself is sound and reproduced. Its written interpretation is the item-3 defect. |
| §19.3.5 | A blocker if the policy cannot meet the requirement; never dropped, never met by a different implementation. | PASS | Item 4. The browser runs the landed implementation, not a substitute. |
| §19.2 | The daily-fit code is the code the browser runs; no second implementation; a component that cannot run in the browser is reported, never replaced silently. | PASS | The model code runs unchanged in Pyodide. The report discloses the two import-only stand-ins (`holidays`, which raises on any use, and `resource`, a record field only) and the ~30 restated lines of `cp24.execution`/`cp26` glue. The glue is equivalent to `fit_origin` on reading, and bitwise CP-26 parity confirms it on all three fits. Proposal 4 states what CP-17 must freeze. |
| — | Check also: the report's figures are those in `measurements.json`. | PASS, with notes | Every table figure (times, deviations, payload bytes, startup 1.7–2.1 s, attribution cost and residuals) matches. Units are inconsistent but not decision-changing: WebAssembly "MB" are MiB (214.8 MiB = 225.2 MB); "Browser processes … GB" are MiB/1000 (1,716,011,008 bytes is shown as "1.64 GB"); payload MB are decimal. Line 111's "21 landed files" is wrong: the bundle holds 17 landed files, 3 probe files and 2 stand-ins. |

## On FAIL only

- **Single largest meaningful gap.** The report misstates how large the deviation was and what drove it. These
  statements are a premise of the τ_eq proposal (line 156) and of "Limits of this measurement" (lines 274–275):
  - it says the deviation "grows with training length";
  - it says "no day here trained near DDNN-2's 1,000-epoch maximum";
  - it says t096's members "trained for 250–440 epochs" (lines 60–63).

  The committed records contradict all three. On 2026-09-06, member 6 ran 939 epochs (best epoch 889) with a
  browser−native deviation of 2.3e-13, and member 7 ran 768 epochs with 2.0e-13. t096's members ran 338 and 300
  epochs, and a 441-epoch t108 member shows 2.6e-13. The deviation tracks the configuration, not the training length.
  The Owner sets τ_eq from this account.
- **Exact next acceptance test.** Submit a new candidate that changes only `reports/cp17-probe/report.md`:
  - lines 59–63, 156 and 274–275, corrected so that every per-member claim (configuration, epochs run, best epoch,
    deviation) equals what `native-reference.json` and `browser-results.json` record;
  - preferably also line 111's file count and the memory units.

  A fresh Integration Critic then confirms those claims against the records. `tests/cp17probe/test_probe_records.py`
  and the `ci312` runner must stay green, and every other committed record must be byte-identical to this candidate.
