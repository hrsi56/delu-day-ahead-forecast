# CP-17b: the re-freeze before r18

**What it is.** A short re-freeze of CP-17's policy A1 (DDNN-2 alone), before the anchor amendment r18 and before
4.7T. It implements the Owner's decisions 13 (partial days) and 14 (shadow issuances), fixes CP-17's review notes
N1–N7, and moves the freeze's pins of governance documents to frozen copies, so that r18 does not break the
freeze's verifier. The fit is unchanged.

**Its freeze** is [`docs/track-b/evidence/cp-17b/freeze-record.md`](../../docs/track-b/evidence/cp-17b/freeze-record.md),
with the machine-readable [`freeze-manifest.json`](../../docs/track-b/evidence/cp-17b/freeze-manifest.json). It
supersedes CP-17's freeze, whose records stay as committed. 4.7T's protocol, revised only where decisions 13 and 14
touch it, is [`4-7t-frozen-protocol.md`](../../docs/track-b/evidence/cp-17b/4-7t-frozen-protocol.md).

**Its records** are in this folder: every figure in the tables below is rendered from them (`cp17.tools.report17b`),
and `tests/cp17b/test_records.py` requires it. The full outputs, with every fitted result, are local
(`.local/artifacts/cp-17b/runs/`), and each record names its source's SHA-256.

**Nothing was retrieved,** and no delivery day after 2026-09-06 was read: every input is the `evidence/cp-26`
extract, the snapshot and the pinned runtimes. Every host and browser run blocked and recorded non-local requests;
there were none.

## What was done

- **Partial days (decision 13).** A fit that emits seven finite, ordered quantiles on every hour the frozen design
  can forecast succeeds on those hours, and is issued and displayed as partial with the missing hours named. A day
  with no forecastable hour fails every policy at its inputs: a failed issuance, written and verified. Exercised on
  2026-03-30, the day after the spring clock change, and on 2023-08-31, under the issuing host and natively. On
  2026-03-30 the 02:00 row's same-hour price lag would come from the change day, which has no 02:00, so the landed
  rule (a row is forecastable when all its base features are present, `cp15.data.prepare`) leaves that one hour
  unforecastable. On 2023-08-31 the load forecast is absent on all 24 hours (CP-25's eligibility calendar), so no
  hour is forecastable.
- **Shadow issuances (decision 14).** Every day, v4, v2 and B0 are fitted under the issuing host as shadows, never
  published, and kept in their own states under CP-26's intake rule. B0 is shadow-issued too: its buffer rebuilt from
  published prices alone is not CP-26's. Exercised on 14 consecutive development days, from CP-26's state at
  2026-08-24 through delivery 2026-09-06.
- **N1–N7.** The issuance driver `cp17.daily` is frozen beside the package (N1); an issued artifact carries its fit's
  measurement, which the schema and the verifier require (N2); criterion 4 is judged inside the chain (N3);
  `cp17.tools.refreeze verify` recomputes every hash it records, or says how each is checked (N4); this report lists
  every open item (N5); the manifest carries the browser part of the reference runtime (N6); the ceiling's message
  reports wall time exactly (N7).
- **Governance pins that survive amendment (decision 19).** The anchor at v21-r17, CP-17's two briefs and this
  brief, both decisions records, and the CP-25 and CP-26 GFS rulings are bound by frozen copies in
  `docs/track-b/evidence/cp-17b/pinned/`. Computational inputs, code and runtimes stay verified live.
- **The fit is unchanged, shown.** `schema.py` changed, so CP-17's full native parity (five policies, nine
  origins) and its issuing-host parity were rerun; both equal CP-17's committed records.

<!-- generated tables: begin -->

### Item 6: native parity, against CP-17's record

| Origin (delivery) | A1 | v5 | v4 | v2 | B0 | equal to CP-17's record |
|---|---|---|---|---|---|---|
| 2025-10-26 | bitwise | bitwise | bitwise | bitwise | bitwise | yes |
| 2026-03-29 | bitwise | bitwise | bitwise | bitwise | bitwise | yes |
| 2026-08-31 | bitwise | bitwise | bitwise | bitwise | bitwise | yes |
| 2026-09-01 | bitwise | bitwise | bitwise | bitwise | bitwise | yes |
| 2026-09-02 | bitwise | bitwise | bitwise | bitwise | bitwise | yes |
| 2026-09-03 | bitwise | bitwise | bitwise | bitwise | bitwise | yes |
| 2026-09-04 | bitwise | bitwise | bitwise | bitwise | bitwise | yes |
| 2026-09-05 | bitwise | bitwise | bitwise | bitwise | bitwise | yes |
| 2026-09-06 | bitwise | bitwise | bitwise | bitwise | bitwise | yes |

### Item 6: issuing-host parity and browser identity, against CP-17's record

| Run | Status vs native | Largest deviation (EUR/MWh) | Selections | Equal to CP-17's record |
|---|---|---:|---|---|
| A1-2025-10-26 | different | 2.8e-02 | all matched | yes |
| A1-2026-03-29 | within ±0.01 EUR/MWh | 6.3e-07 | all matched | yes |
| A1-2026-08-31 | within ±0.01 EUR/MWh | 9.4e-09 | all matched | yes |
| A1-2026-09-01 | within ±0.01 EUR/MWh | 8.2e-10 | all matched | yes |
| A1-2026-09-02 | within ±0.01 EUR/MWh | 1.3e-11 | all matched | yes |
| A1-2026-09-03 | within ±0.01 EUR/MWh | 1.6e-09 | all matched | yes |
| A1-2026-09-04 | within ±0.01 EUR/MWh | 3.0e-11 | all matched | yes |
| A1-2026-09-05 | within ±0.01 EUR/MWh | 7.5e-10 | all matched | yes |
| A1-2026-09-06 | within ±0.01 EUR/MWh | 9.4e-13 | all matched | yes |
| B0-2026-03-29 | identical bit for bit | 0 | all matched | yes |
| B0-2026-09-06 | identical bit for bit | 0 | all matched | yes |
| v2-2026-03-29 | within ±0.01 EUR/MWh | 5.4e-13 | all matched | yes |
| v2-2026-09-06 | within ±0.01 EUR/MWh | 5.1e-13 | all matched | yes |
| v4-2026-03-29 | within ±0.01 EUR/MWh | 3.3e-13 | all matched | yes |
| v4-2026-09-06 | within ±0.01 EUR/MWh | 4.3e-13 | all matched | yes |
| chromium A1-2026-09-06 | identical bit for bit (vs the issuing host) | 0 | all matched | yes |
| webkit A1-2026-09-06 | identical bit for bit (vs the issuing host) | 0 | all matched | yes |

### Item 1: partial days, under the issuing host and natively

| Day | Hours | Forecastable | Missing | Issuing host | Native | Same path | Shadows' intake |
|---|---:|---:|---|---|---|---|---|
| 2023-08-31 | 24 | 0 | all | failed issuance (no hour of the day is forecastable by the frozen design) | failed issuance (no hour of the day is forecastable by the frozen design) | yes | no intake: the fit failed |
| 2026-03-30 | 24 | 23 | 02:00 Europe/Berlin | successful daily fit (partial: 23 of 24 hours; missing 02:00 Europe/Berlin) | successful daily fit (partial: 23 of 24 hours; missing 02:00 Europe/Berlin) | yes | no intake: not a complete canonical issuance |

### Item 2: the shadow run, day by day

| Delivery day | Issued | A1 (s) | v4 (s) | v2 (s) | B0 (s) | Total (s) | Buffers vs CP-26, host (largest) | Natively |
|---|---|---:|---:|---:|---:|---:|---|---|
| 2026-08-24 | A1 | 106 | 99 | 71 | 5 | 282 | bitwise | bitwise |
| 2026-08-25 | A1 | 116 | 96 | 71 | 6 | 288 | bitwise | bitwise |
| 2026-08-26 | A1 | 94 | 100 | 71 | 7 | 272 | within 2.2e-14 | bitwise |
| 2026-08-27 | A1 | 86 | 106 | 71 | 7 | 271 | within 2.2e-14 | bitwise |
| 2026-08-28 | A1 | 120 | 88 | 71 | 5 | 284 | within 2.2e-14 | bitwise |
| 2026-08-29 | A1 | 106 | 95 | 71 | 8 | 280 | within 2.2e-14 | bitwise |
| 2026-08-30 | A1 | 92 | 81 | 65 | 6 | 244 | within 2.2e-14 | bitwise |
| 2026-08-31 | A1 | 97 | 81 | 71 | 5 | 255 | within 2.2e-14 | bitwise |
| 2026-09-01 | A1 | 88 | 76 | 68 | 5 | 237 | within 2.2e-14 | bitwise |
| 2026-09-02 | A1 | 80 | 81 | 77 | 5 | 243 | within 2.2e-14 | bitwise |
| 2026-09-03 | A1 | 79 | 82 | 77 | 6 | 244 | within 2.2e-14 | bitwise |
| 2026-09-04 | A1 | 76 | 78 | 71 | 6 | 231 | within 2.2e-14 | bitwise |
| 2026-09-05 | A1 | 100 | 82 | 65 | 5 | 252 | within 2.2e-14 | bitwise |
| 2026-09-06 | A1 | 85 | 83 | 64 | 5 | 236 | within 2.2e-14 | bitwise |

### Item 2: the shadow run, at the freeze origin

| Mode | Days | Final buffers equal to CP-17's recorded state | Largest standardized difference | Every day's buffers | Every shadow registered | Other |
|---|---:|---|---:|---|---|---|
| native | 14 | B0 bitwise, v2 bitwise, v4 bitwise | 0 | bitwise | yes | CP-26's stored forecasts reproduced bitwise: yes |
| host | 14 | B0 bitwise, v2 not bitwise, v4 not bitwise | 2.2e-14 | within rounding | yes | total per day max 288 s, median 255 s; within the 900 s ceiling: yes; peak 902 MiB |

### Item 2: B0's buffer rebuilt from published prices

| Question | Answer |
|---|---|
| Days CP-26 consumed into B0's buffer | 2,390 |
| Of them, rebuilt from prices bit for bit | 2,390 of 2,390 |
| Days the price rebuild takes and CP-26 did not | 36 (CP-26 issued 23 of 24 keys: 26; CP-26 issued no B0 key: 10) |
| Days CP-26 took and the price rebuild cannot | 0 |
| Origins whose 28-day buffer differs | 524 of 2,381 |
| Conclusion | not equal: B0 is shadow-issued too, as the brief prescribes (cp17.shadow, cp17.daily) |

### N1 and item 5: the killed-process control and the freeze-origin issuance

| Case | Path | Display | Artifact verifies | A1's cause |
|---|---|---|---|---|
| N1 control: A1's process killed after 15 s, a stale A1 record planted | A1 failed → v4 ok | failed fit; fallback v4 issued | yes | training: FitFailure: the issuing-host process exceeded the 15.0 s timeout and was killed |
| The freeze-origin issuance, 2026-09-06 | A1 ok | successful daily fit | yes | — |

<!-- generated tables: end -->

## Open items

Every open item, for the Owner and r18 (N5). None was resolved by looking at a 4.7T outcome; none exists.

**For r18 to ratify, with CP-17b's freeze identity:**
- **C2, partial days (decision 13):** the success definition's criterion 3 on the forecastable hours, the partial
  display, and a day with no forecastable hour as a failed issuance.
- **G1, shadow issuances (decision 14):** the shadow rule as frozen, including **B0's shadow**, which decision 14 did
  not foresee: B0's buffer rebuilt from published prices alone differs from CP-26's (36 days, 524 origins), so B0 is
  shadow-issued too, as the brief prescribes. It costs about 5 s a day.
- **The chains (decision 15)** stay as decisions 11 and 12 set them.
- **C1's wording (decision 16):** released errors from complete delivery days ≤ D−2; training targets the days
  before D published strictly before the issue time.
- **G2 (decision 17):** GFS missing in A1's training window fails A1 and v4, so v2 issues.
- **F1 (decision 18), disclosed, and observed again larger:** at the DST origin 2025-10-26, A1 under the issuing host
  differs from native by up to 0.028 EUR/MWh (p50), every selection identical; this round's rerun reproduces it
  exactly. On item 1's spring day 2026-03-30 the same mechanism gives up to 0.082 EUR/MWh (p2.5; 0.028 at the p50),
  from one member that stopped by patience at 351 epochs, not at the epoch cap (`f1-2026-03-30.json`). So 0.028 is
  not a bound, and r18's disclosure should state the larger figure. τ_eq stays 0.01 as the visitor's tolerance against
  the issued artifact, which is bit for bit; nothing is changed.
- **The GFS-late disclosure** (CP-17's item 1): v2 is +2.27% MAE and +6.68% WIS against A1's GFS +6 h route on
  1,354 paired affected development dates.
- **4.7T's protocol revision** for partial days and shadows (item 7).

**Disclosed by this round:**
- **A partial day's shadow enters no buffer** (CP-26's intake rule takes only a complete canonical issuance), so
  after a clock change a buffer keeps its older complete days a little longer. CP-26 ran so; the buffers stay 28
  complete days.
- **The host's buffers differ from native by rounding.** After 14 shadow days under the issuing host, v4's and v2's
  standardized errors differ from CP-26's by at most the figure in the table above, and B0's are bitwise; natively
  all three are bitwise.
- **The timings here were measured with jobs running concurrently:** two shadow-run days at a time, among up to four
  workers, so the per-day totals are conservative.
- **On CI, `freeze verify` reports the local runtimes unchecked** (the 23 Pyodide files, Node.js, the search state),
  never passed; the issuing machine checks them all.
- **§19.2, one code path.** The fit, the chain's judgement, the shadow states and the scoring are package files,
  run by the issuing host and the browser alike. The driver `cp17.daily` runs natively, because it starts the
  issuing host's processes. It is frozen by hash beside the package and never ships; it holds no fit, judgement or
  scoring of its own.

**For 4.7T (not begun):**
- the window opens no earlier than 2026-12-04, after the price for 2026-12-05 is published;
- the §24.2 audit and the Owner's declaration come first; the retrieval plan is prepared, not run; the guard moves
  only at the gate;
- the proposed ceiling stays 20 machine-hours; the product run with its shadows is re-estimated in the protocol's §11.

**For CP-18:**
- the unattended daily pipeline, which calls `cp17.daily` once per delivery day after building the day's payloads,
  with its schedule, deadline and late-forecast rule;
- publication authority, the MLflow registration of the local names and versions, and the Space's activation;
- the visitor wording for §19.3's "Train it yourself", proposed in CP-17's report for the Owner.
