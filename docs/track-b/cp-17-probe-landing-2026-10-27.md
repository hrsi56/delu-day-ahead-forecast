# CP-17-probe landing — 2026-10-27

**CP-17-probe is closed.** It was §19.3 item 4's feasibility probe for A1, run before the CP-17
freeze on development data only.

**A1's daily fit can be retrained in a visitor's browser,** so the blocker route of §19.3 item 5 is
not triggered. The probe measured in Chromium 153 and WebKit 26.6, under Pyodide 0.28.0:

- **Time and memory:** A1 fits in 62–73 s, with 187–215 MiB of WebAssembly memory.
- **Agreement:** every data-driven selection matched the native fit.
- **Deviation:** the quantiles differ from the native fit by rounding only, at most 6.3e-7 EUR/MWh.
- **Hosts:** every WebAssembly host gave the same bits.

## Identities

| Item | Value |
|---|---|
| Brief | `docs/track-b/evidence/cp-17-probe/issued-brief.md`, SHA-256 `2afc610e2c3f61b4ba862a8b1d2b1cf878764900ad11f4b5832634df8c53b155`, issued 2026-10-27, recorded at `f7c9035`, packaged byte-identical from its canonical file |
| Anchor | `capstone_v21.md` v21-r17 §19.2 and §19.3, SHA-256 `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`, unchanged |
| Final candidate (the Integration PASS binds here) | `b4f23422c60e40fa8f0d3f523c28605f5451d589`; verdict `docs/track-b/evidence/cp-17-probe/integration.md`, SHA-256 `246f0812f7c85692314d63ebbd17dd879e11b08b845764bded7828d5cf9e5eb6` |
| Evidence tip / `evidence/cp-17-probe` (pushed) | `07da82a99e725663e25674aa2ce3aef8d8d881b7` |
| Squash landing / `land/cp-17-probe` | `42e27c7040ca1ba7147192c81ab4cd33bc33d362`, single parent `f7c9035`, tree `5ea3c755d83b73e25b033b15d3ecc6c27e2b395c`, equal to the evidence tip's |
| Outputs | `reports/cp17-probe/` (the report, the records, the retrieval manifest and the compute ledger) and `src/cp17probe/` |

## The return and its receipt

- **The Lead returned PASS** in about 5 of the 6 hours, using about 2.0 of the 5 machine-hours.
- **The Integration reviews:**
  - **Two returned FAIL,** on the report's accuracy alone. The first found a wrong account of the
    browser–native deviation. The second found a wrong count of the member fits.
  - **No measurement changed.** Both verdicts are preserved beside the PASS.
  - **The third Critic passed** `b4f2342` from a clean detached checkout. It:
    - reran the whole suite the way GitHub does, and the stress tests;
    - reran one browser measurement in both browsers, bit-identical to the committed record;
    - reran the native reference;
    - checked every figure in the report against the records.
- **The Orchestrator's receipt:**
  - `gauntlet.py return` reports 0 problems;
  - the delta is the verdict and the Lead's CI record only;
  - the packaged brief matches by hash;
  - all 36 files are new, under `src/cp17probe/`, `tests/cp17probe/`, `reports/cp17-probe/` and
    `docs/track-b/evidence/cp-17-probe/`, so no pinned or landed file changed;
  - the largest blob in the branch is 414 KB;
  - the value-based secret scan of the branch found nothing;
  - no committed file carries a delivery date after 2026-09-06;
  - on a history-free copy with `CI=true` and Python 3.12, the workflow's seven steps are green:
    2,260 passed and 34 skipped;
  - locally, `pytest -m stress` passes 17, with one collection skip (`eccodes` is not installed).
- **GitHub:** on the temporary branch `ci/cp-17-probe-land-check`, workflow run 40554314243 passed every
  step. Then `main`, `land/cp-17-probe` and `evidence/cp-17-probe` were pushed, and the branch was
  deleted.
- **The LAND** was executed by the Orchestrator under the Owner's delegation of 2026-10-27: "יש לך
  אישור מלא להתנהל בשמי עד שיש החלטות שדורשות אותי ספציפית".

## What the probe established

From `reports/cp17-probe/report.md` and its records:

| | Chromium 153 | WebKit 26.6 | Native |
|---|---:|---:|---:|
| A1, 2026-09-06: fit | 65.8 s | 62.0 s | 14.8 s |
| A1, 2026-03-29 (DST): fit | 73.3 s | 70.2 s | 15.6 s |
| v2, 2026-09-06: fit | 44.4 s | 43.3 s | 24.5 s |
| Largest deviation from native (EUR/MWh) | 9.4e-13 / 6.3e-7 / 5.1e-13 | the same bits | — |

- **The native reference is CP-26.** The three native fits reproduce CP-26's stored forecasts bit
  for bit, from payloads in which the day's own outcome is blanked.
- **Selections:** every one matched, in all 16 DDNN-2 member fits and all 48 LEAR hour models.
- **Deviation:** its size depends on the member's configuration, not on training length. One of the
  eight configurations, k12's `t096`, reached 1.8e-6 per member. The others stayed below 2e-11.
- **Payloads:**
  - the first visit is 3.2 KB;
  - the training payload, loaded on request, is 44.6 MB (37.2 MB gzipped);
  - the landed import chain brings in scikit-learn and SciPy, so most of it is packages.
- **One code path:**
  - the landed fit code runs unchanged under Pyodide, with two import-only stand-ins (`holidays` and
    `resource`);
  - about 30 lines of orchestration glue are restated, and the bitwise CP-26 parity proves them.
- **Software retrieved:**
  - Pyodide 0.28.0: 23 files, 44,962,352 bytes;
  - Chrome for Testing 153.0.8010.12 through Playwright 1.63.0's installer: 190,970,181 bytes.

  The Owner confirmed both in the Lead session. No data was retrieved, and there was no other network
  contact.

## Proposals carried to the Owner and to CP-17's reissue

1. **τ_eq,** the Owner's to set: 0.01 EUR/MWh on every emitted quantile, with "within τ_eq" only
   when every selection matched.
2. **The reference runtime:**
   - Pyodide 0.28.0, pinned by file hashes;
   - Chromium 153.0.8010.12 and WebKit 26.6;
   - the Apple M3 machine class.
3. **§19.7's attribution for A1:** exact baseline Shapley over DDNN-2's input groups, on the issued
   p50. It costs 0.2–0.34 s in the browser.
4. **One code path:** a browser-safe daily-fit package under `src/cp17/`. The official daily fit is
   issued under the pinned Pyodide in Node.js, so a visitor's retrain is identical bit for bit.

## Disclosures

1. **The first WebKit runs failed.** The Lead had edited the served worker while a measurement was
   running. The error was reproduced, and the final measurement was rerun end to end from committed
   code.
2. **Two Critic worktrees were not fully deleted** by `git worktree remove` ("Directory not empty").
   The Lead removed the remainder, re-added a clean worktree at the same SHA, and let `critic-close`
   remove it and hash the verdict.
3. **The Chromium archive's own SHA-256 was not observable,** because the installer deletes it. The
   installed tree is fingerprinted instead.
4. **Pyodide's lock file reports its version as `0.28.0.dev0`.** The files came from the `v0.28.0`
   release path, and the runtime is identified by its file hashes.
5. **Not measured:** Firefox, mobile browsers and slower machines.

## Reclamation

- **`gauntlet.py reclaim cp-17-probe --disposition land`:**
  - a verified bundle, `.local/artifacts/cp-17-probe-reclaim-20261027/gauntlet-cp-17-probe.bundle`
    (331,397 bytes);
  - a ref snapshot;
  - the worktree removed;
  - the branch deleted (it was `07da82a`).
- **Both tags are on GitHub.**
- **No live citation** needed repointing.
- **Retained locally,** for CP-17's reissue:
  - `.local/artifacts/cp-17-probe/`, with the records, the Critic runs and the extracted CP-26
    inputs (241 MB);
  - the pinned runtimes in `.local/tools/`: `pyodide-0.28.0/` and `ms-playwright/chromium-1243/`.
