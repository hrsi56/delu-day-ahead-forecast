# CP-17: the freeze of A1 as a complete daily policy on one code path

- **Evidence class.** Everything here is `development_post_selection` and descriptive, on development data to
  2026-09-06 only.
- **No 4.7T forecast.** None exists, and none was produced.
- **The frozen identities** are in [`freeze-manifest.json`](../../docs/track-b/evidence/cp-17/freeze-manifest.json)
  and the [freeze record](../../docs/track-b/evidence/cp-17/freeze-record.md).
- **The tables below are generated** from this folder's records by `cp17.tools.report`.

## What CP-17 established

1. **The GFS check (item 1)** met its stop rule. The Owner then ruled:
   - **decision 11:** GFS late or missing → v2 → B0, with the excess disclosed;
   - **decision 12:** A1's own fit failed while the weather is available → v4 → v2 → B0.

   The check: on the 1,354 paired GFS +6 h affected dates, v2 is +2.27% (MAE) and +6.68% (WIS) against A1's
   GFS +6 h route. See [`gfs-check.md`](gfs-check.md).
2. **One code path (item 2).** `src/cp17/` is one package of 33 files that runs unchanged natively, under the
   issuing host, and in Chromium and WebKit. It fits A1, v4, v2 and B0 from their shipped payloads (and v5,
   the 4.7T control, natively).
   - Its imports are the standard library, NumPy, pandas, scikit-learn and LightGBM through the landed model
     modules, plus two import-only stand-ins that fail if reached.
   - No component needs §19.3's exception route.
3. **Native parity (item 3)** is bitwise for every policy at every origin, against CP-26's stored nominal
   forecasts:
   - five policies at nine origins: the last seven development origins and the two DST days;
   - every member's central and every recorded selection;
   - the interval layers' buffers, rebuilt from the ledger and checked against CP-26's own consumption hashes.
4. **Issuing-host parity (item 3).** Every issuing-host fit is within τ_eq of the native fit, with every
   selection matched. A1 runs at nine origins, v4 and v2 at two. The deviations come from rounding only, in
   the LEAR solver and in DDNN-2's arithmetic. LightGBM's members are bit-identical across runtimes.
5. **Browser identity (item 3).** A1 retrained in Chromium and in WebKit is bit-identical to the issuing
   host's artifact. v4 runs in both browsers.
6. **The failure policy** runs on the issuing host, on real payloads, exactly as natively:
   - the freeze origin's own A1 issuance;
   - a GFS-late issuance (v2);
   - a real A1 training failure from development, 2022-12-04, where v4 issues.
7. **§19.5's records** (item 5) recompute under the issuing host bit for bit. §19.3's status rule and its
   negative controls (item 6) behave as frozen. The reference bundle (item 7) validates, and every tampering
   control is refused.

<!-- generated tables: begin -->
<!-- generated tables: end -->

## Reading the tables

- **"within ±0.01 EUR/MWh"** is the Owner's status for a retrain that matched every data-driven selection and
  stayed within τ_eq of the issued artifact (decision 9). "identical bit for bit" is stricter: it requires
  every emitted quantile to be IEEE-754 identical.
- **Issuing host against native.** These deviations are between the issuing host and the native fit. They are
  not the visitor's check: a visitor's retrain is compared with the issued artifact, which the issuing host
  produced, and the browser identity rows show that comparison is bit for bit.
- **Timing.** Times are on one Apple M3 (8 cores, 16 GB, macOS 26.5.2), one worker per run, with at most two
  runs at once; the browser runs ran alone.
  - Each time includes attribution where it was computed (A1, v4 and v2 at 2026-09-06 and 2026-03-29).
  - The native fits ran with BLAS at one thread.
- **Memory.**
  - "Wasm heap" is the WebAssembly linear memory, which only grows, so its final size is the peak.
  - "Peak RSS" is the Node.js process's maximum resident set.
  - "Browser RSS peak" is the summed resident memory of the browser's processes, sampled every 0.25 s.
- **The training payload** is what a visitor's browser loads on "Train it yourself": the runtime, the
  packages, the package code and the day's training window. The first visit is the page alone.

## §19.7's attributions, frozen

| Component class | Method | Checked |
|---|---|---|
| A1 (neural) | exact baseline Shapley over DDNN-2's input groups on the issued p50, each member's training-row mean as the baseline, every coalition (at most 2,048) | the values add up to the issued p50 minus the baseline in every hour; equal across runtimes within rounding |
| LEAR members (v2, v4) | coefficient × centered, standardized input, from the refitted final Lasso | the refit reproduces the recorded coefficient hash; contributions plus intercept equal the member's forecast |
| LightGBM members (v4) | TreeSHAP per prediction, and split gain, from the refitted booster | the refit reproduces the recorded tree hash; contributions plus expected value equal the member's forecast |
| Blends (v2, v4) | each component's weight × its forecast | the decomposition equals the central forecast within rounding |
| Interval layers (H, B0) | explained in words; no per-input attribution | — |

All of it is attribution within one fitted artifact, relative to its stated baseline, never causality or
incremental value (§19.7).

## The reference runtime, and the visitor wording proposed for the Owner

**The reference runtime:**
- Pyodide 0.28.0;
- Chromium 153.0.8010.12 and WebKit 26.6, through Playwright 1.63.0;
- Node.js v26.7.0;
- the Apple M3 machine class, 8 cores, 16 GB, macOS 26.5.2.

**Proposed wording** (for the Owner's later publication decision; not frozen here): "Retraining this day's
model downloads about the training payload shown above, once, and took about the measured fit time on an
Apple M3 laptop in Chromium and WebKit (measured 2026-10-28). Your result is compared with the
issued forecast: identical bit for bit, within ±0.01 EUR/MWh, or different, with the numbers. It never
replaces the issued forecast."

## The Owner's summary for the anchor amendment (r18)

- **The GFS check and the rulings:**
  - item 1's table;
  - decision 11 (GFS late → v2 → B0, with the excess disclosed);
  - decision 12 (A1 failed → v4 → v2 → B0).
- **The freeze identities:**
  - the policy identity and the freeze manifest (their SHA-256 values are in the return);
  - the package `f0a11c0f…`;
  - the issuing host: Pyodide 0.28.0 by its 23 file hashes, and Node.js v26.7.0 `1ef99ea2…`.
- **Parity:** the tables above.
- **The failure policy and the success definition:** freeze record §10.
- **The protocol's key choices:**
  - the endpoints and the compound test at α = 0.05;
  - 7-day blocks, 10,000 replicates, seed 20261204;
  - the minimum support of 60 paired days;
  - the retrieval plan, about 4.2 GB, prepared not run;
  - the proposed ceiling of 20 machine-hours;
  - PUBLISH_RULES §14's four items.
- **The open items** (freeze record §11):
  - **G1:** daily shadow issuances for the fallbacks' interval states;
  - **C1:** "labels ≤ D−2" read as released errors, with training targets published before the issue time;
  - **C2:** partial issuance on days the design cannot forecast in full;
  - **G2:** GFS missing in a training window.
- **§19.3 exceptions:** none needed.

## Compute, retrieval and the red line

- **Compute** is in [`compute-ledger.jsonl`](compute-ledger.jsonl), summed over workers' wall time, within the
  15-machine-hour ceiling.
- **Retrieval:** none. No data, software or remote byte was retrieved
  ([`retrieval-manifest.json`](retrieval-manifest.json)).
- **Network:** every Node.js and browser run refused and recorded non-local requests, and none was made.
- **The red line:**
  - no delivery day after 2026-09-06 exists on this machine, or was read;
  - the boundary guard stays at 2026-09-06;
  - no committed record carries a later date (`tests/cp17/test_records.py`). The 4.7T protocol names its
    future window as protocol dates only.

## Reproduction

- **Every record:** `src/cp17/tools/reproduce.sh <project root> <out>` from a checkout. It needs no network.
  It takes about 40 minutes on the reference machine, and uses the pinned runtimes and the `evidence/cp-26`
  extract in `.local/`.
- **Committed:** `python -m cp17.tools.records --run <out>` collects the records, and
  `python -m cp17.tools.report` renders these tables.
- **Tests:** `tests/cp17/`. The records tests and units are CI-safe. The real-input tests skip without the
  extract, and the host and browser tests are marked `stress` and skip without the runtimes.
