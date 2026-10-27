# CP-17-probe — "Train it yourself" for A1, measured in the browser before the freeze

*Capstone v21-r17 §19.3 item 4 (with items 1, 2 and 5) and §19.2, for the designated policy A1 (DDNN-2
alone); brief `2afc610e…`. Development data only: every day measured is on or before 2026-09-06.*

## Result

**A1's daily fit can be retrained in a visitor's browser.** The fit was retrained in Chromium and WebKit
for two development days, 2026-09-06 and the DST day 2026-03-29. Each fit used its shipped training
window and the landed code, seeds and selection rules:

- it took about 62–73 seconds, with 187–215 MB of WebAssembly memory;
- it downloaded 44.6 MB, or 37.2 MB compressed, once and on request;
- **every data-driven selection matched the native fit**;
- the emitted quantiles differ from the native fit by at most 6.3e-7 EUR/MWh;
- every WebAssembly host (Chromium, WebKit and Node.js) produced the same bits.

The blocker route of §19.3 item 5 is not triggered. v2, the fallback on GFS-late days, retrains in
about 44 seconds with the same agreement.

**The native reference is CP-26.** The three native fits reproduce CP-26's stored nominal forecasts
**bit for bit**, which is CP-26's recorded parity standard (`parity.json`: IEEE-754 bits). Every member
selection CP-26 recorded is reproduced. The fits ran from payloads in which the target day's own
outcome is blanked.

## What was measured

Status "different" means not bit-identical; no τ_eq exists yet. Selections: see
[§ Selections](#selections). Time is the fit in the worker, with the attribution beside it. Memory is the
WebAssembly linear memory's peak, and beside it the summed resident memory of the browser's processes.

| Browser | Day | Status | Max abs diff (EUR/MWh) | Selections | Fit | Attribution | Native fit | WebAssembly memory | Browser processes |
|---|---|---|---|---|---|---|---|---|---|
| Chromium 153.0.8010.12 | A1 2026-09-06 | different | 9.4e-13 | all match | 65.8 s | 0.34 s | 14.8 s | 215 MB | 1.64 GB |
| Chromium | A1 2026-03-29 (DST) | different | 6.3e-7 | all match | 73.3 s | 0.22 s | 15.6 s | 187 MB | 1.63 GB |
| Chromium | v2 2026-09-06 | different | 5.1e-13 | all match | 44.4 s | — | 24.5 s | 258 MB | 1.74 GB |
| WebKit 26.6 | A1 2026-09-06 | different | 9.4e-13 | all match | 62.0 s | 0.32 s | 14.8 s | 215 MB | 1.37 GB |
| WebKit | A1 2026-03-29 (DST) | different | 6.3e-7 | all match | 70.2 s | 0.20 s | 15.6 s | 215 MB | 1.36 GB |
| WebKit | v2 2026-09-06 | different | 5.1e-13 | all match | 43.3 s | — | 24.5 s | 258 MB | 1.45 GB |
| Node.js v26.7.0 (Pyodide) | each of the three | bitwise equal to both browsers | as above | all match | 66.8 / 72.7 / 44.6 s | — | — | 187–273 MB | — |

**Startup.** Before the fit, loading the runtime, the packages, the code and the day's data took 1.7–2.1
seconds from the probe's local server.

**Payloads**, measured as raw bytes served and as each file compressed with gzip -9:

| Part | Raw | gzip |
|---|---|---|
| First visit (the page; the runtime loads only when the visitor asks to retrain) | 3.2 KB | 1.6 KB |
| Runtime: Pyodide core | 12.26 MB | 5.45 MB |
| Packages, A1 (numpy, pandas, scikit-learn, scipy, openblas, requests and their dependencies, tzdata) | 31.73 MB | 31.21 MB |
| Packages, v2 (the same, plus LightGBM) | 32.69 MB | 32.16 MB |
| Code: the landed files and the probe's module (zip), and the driver | 52 KB | 49 KB |
| Data: A1's day table, D−735 to D | 0.53–0.54 MB | 0.53 MB |
| Data: v2's rows | 1.51 MB | 1.21 MB |
| **Training payload, A1** | **44.6 MB** | **37.2 MB** |

The deviation is **rounding**: the same float64 operations in a different order, through Accelerate's
BLAS natively and Pyodide's own kernels in WebAssembly. Training amplifies it. On 2026-09-06 it stays
near 1e-12. On 2026-03-29, one configuration (k12's `t096`, members 6 and 7, trained for 250–440
epochs) carried it to 1.8e-6 per member and 6.3e-7 in the ensemble median. Even there, its best epoch,
epochs run and stop reason were the same. **The deviation is not bounded by a constant:** it grows with
training length.

### Selections

**A1**, for each of the eight members:

- the seeded held-out weeks and the week pool;
- the training and held-out day sets, as counts and as int64 index hashes;
- the input count;
- the winsorisation activations on the training, held-out and forecast rows;
- early stopping's best epoch, epochs run and stop reason;
- the cap's activations;
- the guard events;
- and, across members, the crossing restorations of the median.

**v2:** LEAR's selected relative alpha in each of the 24 local hours of A1 and of B2, the training rows,
and the H layer's buffer (its 28 released days, their errors' hash and the issuing scale).

**Diagnostics, reported beside the selections and not counted as selections:** the weight hashes, the
best stopping metric, the preprocessor's statistics, and LEAR's iteration counts and model hashes. These
differ wherever the arithmetic does.

## How it was measured

- **Native reference** (`src/cp17probe/native.py`).
  - The development inputs are read through CP-26's pure loaders, under CP-25's partition specification,
    the 2026-09-06 boundary (`cp25.guard`) and CP-20's and CP-25's weather. CP-26's identity pins, authority
    checks and resource monitor are not called, and `src/cp26/` is unchanged.
  - The serving searches k12 and k13 and the forecast ledger come read-only from the local tag
    `evidence/cp-26`. v2's H buffer comes from CP-26's replay state.
- **Payloads** (`payload.py`).
  - A1 ships the DDNN-2 day table from D−735 (the 728-day window plus the D−7 lags) to D, the day's keys,
    and the eight frozen members of the serving search.
  - v2 ships CP-15's rows from LEAR's history start, the LEAR recipe, and the 28 released H days.
  - **D's price row, slot targets and mask (A1), and D's hourly targets (v2), are blanked.** The tests
    prove that a payload is unchanged when D's outcome changes, and changed when a window value changes.
- **One module, every host** (`dailyfit.py`).
  - Under native CPython and under Pyodide alike, it calls the landed `cp24.member.fit_member`,
    `cp24.member.emit_rows`, `cp24.ddnn2.ensemble_median`, `cp15.models.fit_day`, `cp21.lgbm.hg_central`
    and `cp16.residuals.SharedResidualState`.
  - It restates only the ~30 lines of glue that `cp24.execution.fit_origin` and `cp26.state` wrap around
    those calls, because their own import chains cannot load in a browser. The bitwise CP-26 parity proves
    the restatement.
- **Browsers** (`measure.py`, `browser/`).
  - The probe serves the pinned Pyodide, the page, the source bundle and the payload from one 127.0.0.1
    server that counts bytes. Any request elsewhere is blocked and recorded; there were none.
  - Each run uses a fresh browser context, so the cache is empty. Pyodide runs in a Web Worker.
  - The worker hashes the source files it executed. They equal the checkout's (`bundle-manifest.json`):
    21 landed files byte for byte, the probe's module, and two stand-ins:
    - **`holidays`**, which Pyodide 0.28.0 does not ship. `delu_forecast.features` imports it at module
      level and never uses it in a fit; any use raises.
    - **the POSIX `resource` module**, which Pyodide lacks. `cp24.member` and `cp21.lgbm` read
      `ru_maxrss` from it for a record field; the fallback reports 0.
- **Node.js** (`node_run.mjs`) runs the same driver under the same Pyodide, from local files.
- **Reproduction:** `src/cp17probe/reproduce.sh <project root> <out>`. The tests are in `tests/cp17probe/`:
  - the units, and the committed records recomputed, run everywhere;
  - the real-input embargo and parity tests skip without CP-26's local state;
  - the browser rerun is marked `stress` and skips without the local runtimes.

## Three things that went wrong, and what was done

1. **The first WebKit runs failed after 3 seconds. I caused it.** While the first full measurement was
   running, I edited the served `worker.js` to pass `attribution=`. WebKit, which ran after Chromium,
   loaded the new worker against the old bundle and raised `TypeError: run() got an unexpected keyword
   argument 'attribution'`.
   - A deliberate rerun reproduced the exact error.
   - The final measurement was run once, end to end, from the committed code, with nothing edited during
     it.
   - The failed runs are in the compute ledger and are not results.
2. **Index hashes differed between runtimes with equal values.** NumPy's default integer is 32-bit in
   WebAssembly, so a raw index array hashes differently from the native int64 array.
   - The probe's records hash canonical int64. Natively that equals CP-26's recorded hash.
3. **My v2 comparison first counted a value as a selection.** It compared the whole H-layer record,
   which includes the hash of the central forecast the layer is applied to. That reported a "mismatch"
   while all 48 alphas, the buffer and the rows matched.
   - The comparison now follows its documented definition: the buffer identity is the selection.
   - The tests hold both cases: a different central hash still matches, and a different buffer does not.
   - The raw results were not rerun or changed.

## Proposals for the Owner and for CP-17

### 1. τ_eq, the equality tolerance (§19.3 item 2), the Owner's to set

**Proposal: τ_eq = 0.01 EUR/MWh on every emitted quantile, and "within τ_eq" only when every
data-driven selection matched.** The status rule:

- **"identical bit for bit"** on exact IEEE-754 equality of every emitted quantile;
- **"within ±0.01 EUR/MWh"** when every selection matched and every quantile is within τ_eq;
- **"different"** otherwise, whatever the numbers, with the numbers.

The reasoning:

- **What was measured.** Rounding reached 6.3e-7 EUR/MWh in the ensemble and 1.8e-6 in one member, and
  it grows with training length (above). 1e-6, the first value I considered, would leave almost no margin.
- **Where 0.01 sits.** It is about four orders of magnitude above the largest observed deviation, and
  equal to the cent a display shows. A reader can understand "within one cent per MWh".
- **Why selections are required on top.** A different selection, such as another best epoch, another
  held-out week or another Lasso penalty, is a different model even when its quantiles happen to be
  close. The selection requirement, not τ_eq, is what separates "same model" from "different model".
- **The alternative.** 0.001 EUR/MWh would still keep three orders of magnitude of margin over what was
  observed on three fits. It is tighter, but leaves less room for days not measured.
- **If proposal 4's issuing host is adopted,** the issued artifact and the visitor's retrain run in the
  same runtime, and the measured status is "identical bit for bit": three hosts agreed on all three fits.
  τ_eq then only guards an engine that computes differently, such as Firefox or mobile Safari, neither of
  which was measured.

### 2. The reference browser and runtime

- **Runtime: Pyodide 0.28.0.**
  - Python 3.13.2, NumPy 2.2.5, pandas 2.3.0, SciPy 1.14.1, scikit-learn 1.7.0, LightGBM 4.6.0, built with
    Emscripten 4.0.9.
  - Every file is pinned in `retrieval-manifest.json`, and every wheel equals the release's own
    `pyodide-lock.json`.
- **Reference browsers:**
  - Chromium 153.0.8010.12: Chrome for Testing, through Playwright 1.63.0;
  - WebKit 26.6: Playwright's build webkit-2359.
- **Reference machine class:** Apple M3, 8 cores, 16 GB, macOS 26.5.2, running one fit at a time.
- **What a visitor is told**, measured on 2026-10-27 and rounded up:
  - *"Downloads about 45 MB (37 MB compressed) once, when you ask."*
  - *"About 1–1.5 minutes on the reference machine; allow up to 3 minutes on a recent laptop."*
  - *"Needs about 250 MB of memory for the computation; the browser itself needs more."*
  - *"Phones and other browsers have not been measured."*

### 3. The attribution method for A1 (§19.7)

**Proposal: exact baseline Shapley over DDNN-2's input groups, on the issued p50, with each member's
training-row mean as the baseline** (`src/cp17probe/attribution.py`).

- **Players:** the input groups the eight members use:
  - `price_d1`, `price_d2`, `price_d3`, `price_d7`;
  - `load_d0`, `load_d1`, `load_d7`;
  - `gfs`, with its missing indicators;
  - `stats`, `weekday`, `calendar`.

  These are groups, not 300 single columns, because a reader sees a 24-value curve as one input, and
  because exactness needs few players. On 2026-09-06 there were 10 groups; on 2026-03-29, 9.
- **Baseline:** "an average training day". That is each member's training-row mean, which is zero after
  the member's own preprocessor.
- **Value:** the issued p50 of each local-hour slot, computed by the landed forward pass, cap and
  ensemble median.
  - Every coalition is evaluated: 1,024 on 2026-09-06 and 512 on 2026-03-29, at most 2,048.
  - So the values are exact and deterministic: no seed, no sampling.
  - They add up: the sum over groups equals the issued p50 minus the baseline p50. The largest residual
    measured was 1.4e-13.
- **Cost:** 0.08–0.11 s natively and 0.20–0.34 s in the browser per day.
  - The browser values equal the native values within 2.1e-7 EUR/MWh.
  - Every WebAssembly host gives the same bits.
  - The full coalition reproduces the issued p50 exactly in the browsers, and within 4.3e-14 natively,
    where the batched forward pass sums in another order.
- **Alternatives set aside:**
  - integrated gradients: path-dependent, and it needs input gradients that the landed code does not
    compute;
  - sampled KernelSHAP: not exact, and seed-dependent;
  - permutation importance: needs outcomes, so it cannot explain a single issued forecast;
  - single-group occlusion: its contributions do not add up.
- **Wording:** "attribution within one fitted artifact, relative to an average training day", never
  causality or incremental value (§19.7).

### 4. The one-code-path design (§19.2), and what CP-17 must freeze

**What the probe established:**

- The landed fit code runs **unchanged** under Pyodide. It needs two import-only stand-ins: `holidays`
  and `resource`.
- **Import weight.** A1's fit itself needs only NumPy, plus pandas for dates. But the landed import chain
  pulls in more: `cp24.design` → `cp15.data` → `delu_forecast` → scikit-learn, SciPy and requests. That
  is 31.7 MB of packages where NumPy, pandas and their dependencies alone are 9.5 MB.
- **The orchestration does not load in a browser.** `cp24.execution` (the job ledger and protocol
  checks) and `cp26` (identity pins and the resource monitor) cannot load there. Their glue had to be
  restated, and the restatement was proven against CP-26's stored forecasts.
- **Records compared across runtimes must hash canonical int64 indices.**
- **Same runtime, same bits.** Chromium, WebKit and Node.js under Pyodide 0.28.0 produced bit-identical
  quantiles for all three fits. Native CPython differs from them by rounding.

**Proposed layout:** one browser-safe daily-fit package under `src/cp17/`. The issuing pipeline imports
it, and it is shipped to the Space byte for byte.

- **Imports:** only the standard library, NumPy and pandas, plus the landed model modules it needs.
  `cp24.ddnn2` is NumPy-only already. The design and member functions must be reached either without the
  `cp15.data` → `delu_forecast` chain, or with the two stand-ins frozen as part of the package.
- **Contents:** the daily-fit orchestration for A1, as `cp17probe.dailyfit` lays it out: window,
  held-out weeks, preprocessing, training, emission, ensemble median and attribution. Also v2's LEAR pair
  and H layer, for the GFS-late fallback.
- **Input:** the shipped payload is its only input, in the schema above. The embargo rule (D's outcome
  blanked) is part of the schema.

**Proposed issuing host: the official daily fit runs under the pinned Pyodide in Node.js.** A visitor's
retrain is then *identical bit for bit* (measured), not merely within τ_eq.

- **The cost** is time: about 67 s per A1 fit against 15 s natively, which is well inside a daily
  schedule.
- **It adds** a runtime dependency.
- **The development evidence stays native.** The issued values would differ from CP-26's native
  arithmetic by rounding (≤ 6.3e-7 EUR/MWh measured), and the freeze records that.
- If issuing stays native, the status a visitor sees is "within ±τ_eq" at best.

**What CP-17 must freeze for one code path:**

- the package's file hashes;
- the runtime's file hashes: Pyodide 0.28.0, and the CPython and NumPy build if issuing stays native;
- the issuing host;
- the payload schema and its embargo rule;
- τ_eq and the status rule;
- the attribution method;
- the stand-ins, if kept;
- the parity standard between the issuing host and CP-26's ledger.

## Limits of this measurement

- **Scale.** It covers one machine, two browsers, three fits: 24 DDNN-2 members and 48 LEAR hours.
  Firefox, mobile browsers and slower machines were not measured.
- **Deviation is not bounded by these days.** It grows with training length, and no day here trained
  near DDNN-2's 1,000-epoch maximum.
- **Selection agreement could fail on some other day.** A near-tie in early stopping, a winsorisation
  bound or a Lasso penalty could flip on another day. The status rule then says "different", which is
  the honest outcome.
- **Memory.** "Browser processes" counts every process of the browser, including its GPU and network
  helpers, so it overstates what the fit needs. The WebAssembly memory is the fit's own.
- **Hosting.** The times were taken with the files served from the same machine. A visitor's network
  adds the download.

## Retrieval and compute

- **Software retrieved:**
  - Pyodide 0.28.0: 23 files, 44,962,352 bytes, from `cdn.jsdelivr.net/pyodide/v0.28.0/full/`. The 17
    wheels were checked against the release lock.
  - Chrome for Testing 153.0.8010.12: 190,970,181 bytes, from `cdn.playwright.dev`, through Playwright
    1.63.0's installer. The installer deletes its archive, so the installed tree is fingerprinted instead.
    FFmpeg was already installed and was not fetched.
  - The Owner confirmed both retrievals in the Lead session. No data byte was retrieved, and there was no
    other network contact.
- **Compute:** 0.36 machine-hours to the final measurement (`compute-ledger.jsonl`), against the
  5-hour ceiling. One worker at a time; the browser jobs count as one worker each.
