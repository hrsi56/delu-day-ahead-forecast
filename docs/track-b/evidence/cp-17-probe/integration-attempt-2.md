# Verdict — CP-17-probe — Integration — FAIL

- Candidate SHA: b242aa2923a4a3055ddc8c2654689ee9b783607d
- Plan / version / bar: `capstone_v21.md`, v21-r17 (SHA-256 3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc
  at the candidate), §19.3 "Train it yourself" is required (items 1, 2, 4 and 5) and §19.2 One code path; the issued
  brief `docs/track-b/evidence/cp-17-probe/issued-brief.md` (SHA-256 2afc610e2c3f61b4ba862a8b1d2b1cf878764900ad11f4b5832634df8c53b155),
  its Observable outcome 1–4 and Further items 1–5. This is the second Integration review; the first (candidate
  `4f1c0d7c08d2f51010279b75de566eb9e57e502e`) returned FAIL.
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
  stayed b242aa2923a4a3055ddc8c2654689ee9b783607d. The only byproducts in the worktree are gitignored `__pycache__/`
  folders under `src/`.

## Commands actually run

All commands ran with `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1`, with `CI` unset unless the runner set it. There
was no network contact, no `git fetch` and no download. No Git write was made in the repository or the worktree; the
runner's `git init` and commit happen inside its own throwaway history-free copy, as the brief prescribes, and the
runner removed both copies. Every output I wrote is under `.local/artifacts/cp-17-probe/critic-2/` or the session
scratchpad. Line numbers below refer to `reports/cp17-probe/report.md` at the candidate.

| # | Command (from the worktree unless stated) | Exit | Observed output |
|---|---|---|---|
| 1 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief cp-17-probe` | 0 | This assignment. `scripts/gauntlet.py` and `scripts/bar.py` in the worktree are identical to `main` (`f7c9035c8c…`). |
| 2 | `git status --porcelain`; `git rev-parse HEAD` | 0 | Empty; `b242aa2923a4a3055ddc8c2654689ee9b783607d`. |
| 3 | `python3 scripts/bar.py bar capstone_v21.md '19.3 "Train it yourself" is required' --at b242aa2…` | 0 | Plan sha256 `3124451d…`; section 25 lines, 1354 bytes, sha256 `5d1f869e…`. Text identical to the brief's excerpt. |
| 4 | `python3 scripts/bar.py bar capstone_v21.md '19.2 One code path' --at b242aa2…` | 0 | Section 6 lines, 335 bytes, sha256 `53834210…`. Text identical to the brief's. |
| 5 | `shasum -a 256 capstone_v21.md docs/track-b/evidence/cp-17-probe/issued-brief.md`; `cmp` of the brief against `.local/artifacts/cp-17-probe/issued-brief.md` | 0 | `3124451d…`, `2afc610e…c53b155`; the packaged brief is byte-identical to the canonical one. |
| 6 | `git diff --stat 4f1c0d7… b242aa2…` | 0 | 3 files: `reports/cp17-probe/report.md` (+43/−19) and two new files, `docs/track-b/evidence/cp-17-probe/integration-attempt-1.md` and `lead-ci-attempt-1.md`. Every other committed record is byte-identical to the first candidate. |
| 7 | `git diff --name-status f7c9035 b242aa2…`, filtered for paths outside `src/cp17probe/`, `tests/cp17probe/`, `reports/cp17-probe/`, `docs/track-b/evidence/cp-17-probe/` | 0 | 32 paths, all `A`; none outside the allowlist; no pre-existing test file modified. |
| 8 | `git diff --quiet f7c9035 b242aa2… -- src/cp15 … src/cp28 src/delu_forecast data pyproject.toml uv.lock AGENTS.md CLAUDE.md engineering-role.md orchestrator-role.md notebooklm-role.md docs/track-b/{gauntlet-templates,rule-inventory,cp-0-defects,backup-register,exposure-ledger,publication-standard-v1}.md docs/PUBLISH_RULES.md .claude .githooks .github scripts tests/conftest.py progress.md 'capstone_*.md' 'syllabus_v*.md' program-stage-sequence.md`; the same for `reports ':!reports/cp17-probe'` | 0, 0 | No difference on any protected path; earlier `reports/` unchanged. |
| 9 | `git ls-tree -r -l b242aa2…` filtered for blobs over 50,000,000 bytes | 0 | None. Largest blob is the pre-existing `models/champion/python_model.pkl` (30,830,306 bytes); largest new file `reports/cp17-probe/browser-results.json` (413,805). |
| 10 | Date scan: every `20YY-MM-DD` later than 2026-09-06 in every file the candidate adds; timestamps of 2026-09-06 22:00/23:00 UTC; ISO timestamps in the two result records | 0 | Data records: none after the boundary; the last hourly timestamp is `2026-09-06T21:00:00+00:00` (23:00 Berlin on 2026-09-06). Text: `2026-10-27` (measurement/authorisation date), `2026-10-15` (CP-26's run folder), governance dates in the brief and in `integration-attempt-1.md`, and **`2027-01-06` in report line 82** ("the next at S_14 = 2027-01-06"), new in this candidate. |
| 11 | `python3 .local/artifacts/cp-17-probe/critic2-runner.py b242aa2… ci312` (read first: it strips credentials from the subprocess environment, runs `UV_OFFLINE=1`, `UV_PYTHON_DOWNLOADS=never`, and hides the local probe inputs in CI mode) | 0 | Copy tree `962274935c45…` = the candidate's tree, one commit; Python 3.12.14. `uv sync --locked --dev` 0; `build_wasm_payload.py` 0 (77.9 s); `pytest -q` 0, **2256 passed, 38 skipped** in 445.54 s; `test_10_cqr_order_statistic.py` 0 (8 passed); `verify_release.py` 0 (PASS); `test_22_wasm_equivalence.py` 0 (15 passed); `publication_guard.py tree` 0; `pytest --collect-only -m stress` 0 (17/2293 collected, `tests/cp17probe/test_probe_browser.py::test_one_browser_measurement_reproduces_the_committed_record` among them). `complete: true`, `scratch_removed: true`. Logs and `results.json` in `.local/artifacts/cp-17-probe/critic-validation-2/ci312/`. |
| 11a | (from 11's `03-pytest.log`) | — | `SKIPPED tests/cp17probe/test_probe_browser.py: the pinned Pyodide 0.28.0, Playwright 1.63.0 browsers and probe payloads (.local/, never committed) are absent`; `SKIPPED tests/cp17probe/test_probe_real_inputs.py:46/59/71/85: CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent`. |
| 12 | `python3 .local/artifacts/cp-17-probe/critic2-runner.py b242aa2… stress` (CI unset) | 0 | Same tree, Python 3.12.14; `uv run pytest -m stress -q`: **17 passed, 1 skipped**, 2276 deselected in 245.47 s. The 17 stress tests are those collected in 11, the probe browser test among them; the one skip is the collection-time `tests/cp20/test_gfs_eccodes.py` (no `eccodes`). So the probe browser test ran and passed. Copy removed. |
| 13 | `CP17_PROBE_BROWSERS=chromium,webkit .venv/bin/python -m pytest -p no:cacheprovider -m stress tests/cp17probe/test_probe_browser.py -q -rA --basetemp=.local/artifacts/cp-17-probe/critic-2/browser-rerun` (CI unset) | 0 | **1 passed in 144.46 s.** In the kept output: Chromium 153.0.8010.12 and WebKit 26.6, Pyodide 0.28.0, A1 2026-09-06 quantiles **equal to the committed record bit for bit** (hash and values), all eight member records equal (timings aside), attribution φ equal; max \|browser − native\| 9.3792e-13; fit 65.4 s and 62.1 s; WebAssembly peak 214.8 MiB; no error, no blocked non-local request, no 404. The rebuilt bundle's zip sha256 `d132571a…` and its file hashes equal `bundle-manifest.json`. |
| 14 | `OPENBLAS/VECLIB/OMP/MKL/NUMEXPR_NUM_THREADS=1 .venv/bin/python -m pytest -p no:cacheprovider tests/cp17probe/test_probe_real_inputs.py -q -rA` | 0 | **4 passed in 35.67 s**: the A1 payload carries no outcome of its day; the payload ignores the day's outcome and follows its window; the v2 payload refuses an unreleased H day; A1 from its payload reproduces CP-26 bitwise. |
| 15 | Same BLAS settings, `PYTHONPATH=src .venv/bin/python -m cp17probe.native --root . --inputs …/cp-17-probe/inputs --fits …/fits/195857d7…/nominal --state …/state/e17f95f7…/replay-state.json --out .local/artifacts/cp-17-probe/critic-2/native` | 0 | `A1-2026-09-06 bitwise selections True 15.3s`; `A1-2026-03-29 bitwise selections True 16.4s`; `v2-2026-09-06 bitwise selections True 15.2s`; `PASS 71s`. My output equals the committed `native-reference.json` in quantiles, payload hashes, member records (timings aside) and attribution φ; payload sizes 534,762/4,523, 527,478/4,425 and 1,476,468/30,466 bytes, as committed. |
| 16 | `.venv/bin/python -m pytest -p no:cacheprovider tests/cp17probe/test_probe_records.py tests/cp17probe/test_probe_units.py -q` | 0 | **22 passed in 3.12 s.** |
| 17 | `python3 -I <scratchpad>/recompute.py <worktree>`: my own recomputation from `native-reference.json`, `browser-results.json`, `measurements.json` and the three `node-*.json` | 0 | See *Evidence actually inspected*. Every figure in the report's measurement, payload and per-member tables reproduces. **The A1 fits hold 16 DDNN-2 members (8 per day × 2 days); v2 holds none** (`fit_v2` is LEAR A1 and B2, `hg_central` and the H layer). |
| 18 | `python3 -I <scratchpad>/runtimes.py <worktree>`; `.local/tools/playwright/bin/python -c "…version('playwright')"` | 0 | Pyodide: 23 files, 44,962,352 bytes, 0 hash or size mismatches, no extra file; the 17 wheels equal `pyodide-lock.json` and are exactly the lock closure of `numpy, pandas, scikit-learn, requests, tzdata, lightgbm`. `chromium-1243`: 348 files, 375,624,473 bytes, tree fingerprint `955ce3e0…` and binary `8319963f…` equal the manifest. `webkit-2359` and `ffmpeg-1011` present. Playwright 1.63.0. |
| 19 | For each of the 20 files under `.local/artifacts/cp-17-probe/inputs/`: `git -C <primary> archive evidence/cp-26 <path> \| tar -xO \| cmp - <file>` | 0 | `evidence/cp-26` = `ca203312…`; 20 checked, 0 differ. `parity.json`: "each float64 as its uint64 IEEE-754 bits", status PASS. |
| 20 | `cmp` of `reports/cp17-probe/*` against `.local/artifacts/cp-17-probe/final/*` | 0 | `browser-results`, `measurements`, `native-reference`, the three `node-*` files, and `bundle-manifest` (= `final/bundle/src.json`) identical. |
| 21 | `python3 -I` over CP-26's `search-results/nominal/k12.json` and `k13.json` (members' configs); `grep kappa src/cp24/ddnn2.py` | 0 | `cp26-k12-t096`: softplus, hidden [140], `z-s4`, batch 32, lr 1.4772e-4, κ 0.0; `WARM_EPOCHS = 20` with k = 1, then k = κ (κ = 0: pinball only). Matches report lines 77–78. |
| 22 | `sysctl -n machdep.cpu.brand_string hw.ncpu hw.memsize`; `sw_vers -productVersion`; `node --version` | 0 | Apple M3, 8, 17179869184, 26.5.2, v26.7.0: the report's machine class. |
| 23 | `git show main:scripts/bar.py \| python3 -I - check <this verdict> --source capstone_v21.md@b242aa2923a4a3055ddc8c2654689ee9b783607d` | 0 | `ok: lines 12–36 (1353 bytes) appear in capstone_v21.md@b242aa2923a4`; `ok: lines 40–45 (334 bytes) appear in capstone_v21.md@b242aa2923a4`. |
| 24 | `git status --porcelain`; `git rev-parse HEAD`, after the review | 0 | Empty; `b242aa2923a4a3055ddc8c2654689ee9b783607d`. |

## Evidence actually inspected

- **The change since the first candidate,** in full: `git diff 4f1c0d7 b242aa2 -- reports/cp17-probe/report.md`, and
  the two new evidence files. The report's lines 59–63, 156 and 274–275 that the first verdict named are rewritten;
  line 111's file count (now line 130) and the memory units are corrected.
- **The whole report** (`report.md`, 319 lines) against the records, figure by figure; the brief in full; the anchor's
  §24.2 and §24.9; `src/cp17probe/{dailyfit,payload,compare,measure,attribution (header and grouping),native (header)}.py`,
  `reproduce.sh`, `tests/cp17probe/test_probe_browser.py` and the header of `test_probe_real_inputs.py`;
  `src/cp26/search.py:70` (`search_day`).
- **Recomputed from the records** (row 17):
  - The per-member table (lines 65–74): every configuration, epochs run, best epoch and browser−native deviation
    matches. Per member: k13 `t040` 145 (95) 8.53e-13, 259 (209) 4.55e-13; `t094` 147 (97) 1.54e-11, 86 (36) 2.84e-13;
    `t030` 92 (42) 4.55e-13, 119 (69) 4.55e-13; `t005` 939 (889) 2.27e-13, 768 (718) 1.99e-13; k12 `t041` 94 (44)
    2.42e-13, 92 (42) 2.27e-13; `t083` 73 (23) 5.97e-13, 86 (36) 2.10e-12; `t108` 441 (391) 2.56e-13, 334 (284)
    5.40e-13; `t096` 338 (288) **1.78e-6**, 300 (250) **6.02e-7**. Every stop reason is `patience`, identical natively
    and in the browser. Chromium, WebKit and Node.js are bitwise equal per member.
  - The claims built on it hold: only `t096` exceeds 2e-11; the longest-trained members stay near 2e-13; the ensemble
    median is 6.277e-7 on 2026-03-29 and 9.379e-13 on 2026-09-06.
  - **The member count does not hold:** 16 DDNN-2 members were measured, not 24 (see *On FAIL only*).
  - The measurement table (lines 35–41): fit 65.8/73.3/44.4/62.0/70.2/43.3 s; attribution 0.34/0.22/0.32/0.20 s;
    native 14.8/15.6/24.5 s; WebAssembly 214.8/187.1/257.8/214.8/214.8/257.8 MiB; processes 1.60/1.59/1.70/1.33/1.33/1.42
    GiB; Node.js 66.8/72.7/44.6 s and 187.1–273.9 MiB; per-level deviations equal `measurements.json`; startup
    1.74–2.06 s. All match.
  - Payloads (lines 50–57): 3,189/1,582; 12,259,068/5,446,388; 31,727,367/31,213,266; 32,687,456/32,156,585;
    51,600/49,491; 531,903–539,285/525,328–533,576; 1,506,934/1,212,815; A1 total 44,577,320/37,242,721. All match.
    Line 251's 9.5 MB is NumPy, pandas, python-dateutil, pytz, six and tzdata (9,498,766 bytes).
  - Attribution: 10 and 9 players, 1,024 and 512 coalitions, browser efficiency residual 1.42e-13, browser−native φ
    2.06e-7, issued gap 0 in the browsers and ≤ 4.26e-14 natively, cost 0.08–0.11 s native and 0.20–0.34 s browser.
  - Bundle: 22 files = 17 landed + 3 probe + 2 stand-ins; each run executed 17 of them, all equal to the checkout.
  - Compute ledger: 11 jobs, 1,282.6 s = 0.356 machine-hours.
  - `measurements.json`: `tau_eq: null`, status "different" in all six runs, every selection matching.
- **Inputs:** the CP-26 extract against `evidence/cp-26`, the pinned runtimes, and the Lead's `final/` outputs. I did
  not read the Lead's logs, drafts, launch envelope or `critic2-assignment.md`, nor the first Critic's working folder.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | **The measurement** under Pyodide in Chromium and WebKit: A1 retrained for 2026-09-06 and 2026-03-29 from its window, code, seed and selection rules; per browser and day, wall time and peak memory, first-visit and training payload sizes, the largest absolute difference per emitted quantile and bitwise status, and selection agreement; the same for v2 for one day. | PASS | `measurements.json`: 6 runs, every field present and recomputed (row 17). I reran A1 2026-09-06 in both browsers (row 13): bitwise equal to the committed record. |
| 2 | **The native reference:** two A1 fits and one v2 fit natively, reproducing CP-26's stored forecasts to CP-26's parity standard, with the browser fits compared against them. | PASS | Rows 14 and 15: all three fits bitwise equal to CP-26's stored nominal forecasts (`parity.json`: IEEE-754 bits), every recorded selection reproduced; inputs equal `evidence/cp-26` (row 19). `compare.build` compares each browser fit against these. |
| 3 | **Proposals,** each with its reasoning: τ_eq; the reference browser and runtime; the attribution method for A1 (§19.7) with its in-browser cost; the one-code-path design (§19.2) and what CP-17 must freeze. | **FAIL** | All four proposals are present and reasoned. The first verdict's defect is fixed: the deviation's account now matches the records member by member (lines 59–82, 175–178, 296–299). But the rewritten τ_eq reasoning (lines 175–177) says "only two of 24 members (one configuration of eight) went beyond 2e-11", and the records hold 16 DDNN-2 members. |
| 4 | **The blocker route** (§19.3 item 5): BLOCKED with the numbers if A1 is infeasible within limits a visitor can meet, or if selections do not match. | PASS | Every selection matches in every browser run; A1 fits in 62–73 s on the reference machine with about 45 MB downloaded on request. Not triggering the blocker is correct, and the report states its limits. |
| 5a | Development data only: no delivery day after 2026-09-06 read, recorded or mentioned. | PASS, with a note | `payload._admit` applies `cp25.guard` and refuses days after the boundary (row 14). No record holds a delivery day or hour after 2026-09-06 (row 10). **Note:** report line 82 names `S_14 = 2027-01-06`. That is the search-schedule protocol date that the ratified anchor itself states (§24.9: "These are protocol dates only, never permission to read future data"), and CP-17 must freeze it. It carries no data or outcome, so I do not count it as a red-line breach. I record it because the brief's wording includes "mentioned". |
| 5b | Software retrieval limited to the two pinned runtimes; no data retrieved. | PASS | Row 18: `retrieval-manifest.json` lists only Pyodide 0.28.0 (every file verified) and Chrome for Testing 153.0.8010.12 (installed tree and binary verified; the archive hash is `null` with its stated reason), with `data_bytes_retrieved: 0`. |
| 5c | No committed file over 50 MB. | PASS | Row 9. |
| 5d | The workflow's seven steps green on a history-free single-commit copy, `CI=true`, Python 3.12. | PASS | Row 11. |
| 5e | Browser tests skip with a stated reason when the runtimes are absent. | PASS | Row 11a. |
| 5f | Timing-sensitive tests carry the `stress` marker. | PASS | The browser rerun carries `pytest.mark.stress`; the other probe tests assert no timing. Rows 11 and 12. |
| 5g | No pinned file and no landed code changes; new code only under `src/cp17probe/`, `tests/` (new files), `reports/cp17-probe/` and `docs/track-b/evidence/cp-17-probe/`. | PASS | Rows 7 and 8. |
| 5h | The Integration Critic reruns one browser measurement and the whole suite in that CI mode. | PASS | Rows 11, 12 and 13. |
| §19.3.1 | In the browser, retrain one issued day's daily fit from its shipped training window with the same code, seed and selection rules, then predict the day's quantiles. | PASS | The A1 payload ships D−735..D with D's price row, targets and mask blanked (row 14 proves outcome-independence). The browser executes the landed `cp24`/`cp15`/`cp16`/`cp21`/`delu_forecast` files byte for byte (row 13). Seeds and configs come from CP-26's serving searches. |
| §19.3.2 | Reports selection agreement, the largest absolute difference per emitted quantile in EUR/MWh, and a status stating only what was measured. | PASS | `compare.build`: `selections.all_match`, `deviation.max_abs_eur_by_level`, and `status` ∈ {"identical bit for bit", "different"} while no τ_eq exists. Recomputed (rows 16, 17). |
| §19.3.4 | On development data, for the designated policy A1: browser time and memory, payload sizes, deviation from the native fit, selection agreement. | PASS | Item 1. The measurement is sound and reproduced; the defect is in the report's account of its scale (item 3). |
| §19.3.5 | A blocker if the policy cannot meet the requirement; never dropped, never met by a different implementation. | PASS | Item 4. The browser runs the landed implementation, not a substitute. |
| §19.2 | The daily-fit code is the code the browser runs; no second implementation; a component that cannot run in the browser is reported, never replaced silently. | PASS | The landed model code runs unchanged under Pyodide (row 13: executed hashes equal the checkout). The report discloses the two import-only stand-ins and the ~30 restated lines of `cp24.execution`/`cp26` glue, which bitwise CP-26 parity on all three fits confirms (row 15). Proposal 4 states what CP-17 must freeze. |
| — | Check also: the report's figures are those in `measurements.json`. | **FAIL** | Every measurement, payload, per-member, attribution and compute figure matches (row 17). The memory units and the bundle file count are now correct. The exception is the DDNN-2 member count: lines 176 and 294 say 24 where the records hold 16. Minor, not decision-bearing: line 213–217's player list includes `calendar`, which no member used on either day. That list is the candidate group set in `attribution.GROUPS`; the 10 and 9 counts on line 220 are right. |
| — | Check also: the blocker route is correctly not triggered; the proposals carry their reasoning; the retrieval manifest shows software only; no committed record holds a date after 2026-09-06; the protected paths are unchanged from `f7c9035`. | PASS | Items 4, 3 (apart from the count), 5b, 5a and 5g. |

## On FAIL only

- **Single largest meaningful gap.** The report overstates how many DDNN-2 members the measurement covers, in the two
  places the Owner reads to set τ_eq. The rewritten τ_eq reasoning says "only two of 24 members (one configuration of
  eight) went beyond 2e-11" (lines 175–177), and "Limits of this measurement" says "three fits: 24 DDNN-2 members and
  48 LEAR hours" (line 294). The records hold 16 DDNN-2 members: 8 for each of the two A1 days. v2 has none; it is
  LEAR's A1 and B2 with HG's central and the H layer. So the amplifying configuration is 2 of 16 members (1 in 8), not
  1 in 12. The previous verdict's acceptance test required every per-member claim in this reasoning to equal the
  records, and this one does not.
- **Exact next acceptance test.** Submit a new candidate that changes only `reports/cp17-probe/report.md`:
  - lines 176 and 294 state 16 DDNN-2 members (two A1 fits × 8), with v2's scale stated as its 48 LEAR hours;
  - no other per-member or count claim disagrees with `native-reference.json` and `browser-results.json`;
  - optionally, the attribution player list (lines 213–217) is limited to the groups actually used, or labelled as
    the candidate set.

  A fresh Integration Critic then confirms those lines against the records. `tests/cp17probe/test_probe_records.py`
  and the `ci312` runner must stay green, and every other committed file must be byte-identical to `b242aa2`.
