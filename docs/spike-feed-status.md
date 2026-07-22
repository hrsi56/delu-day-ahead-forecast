# Month-0 ENTSO-E / SMARD Data-Layer Feed-Status Memo

**Date:** 2026-06-12. **Scope:** Month-0 de-risking spike per the B-Claude brief (capstone_V6_0.md S12, M1/CP-1 pre-confirmation input). Sample pulls only -- no bulk pull, no feature engineering, no model code.

**Environment:** Python 3.11, `uv`-managed (`pyproject.toml` / `uv.lock` committed). `entsoe-py==0.8.0` (satisfies the `>=0.7.5` pin -- the 15-min-MTU-aware version line). DE-LU area `10Y1001A1001A82H`. Token read from `ENTSOE_API_TOKEN`, never logged.

**Probe code:** `scripts/q1_*.py` .. `scripts/q8_*.py`, shared helpers in `src/spike/entsoe_helpers.py`. Each script is independently runnable via `uv run scripts/qN_*.py` and writes evidence JSON to `data/spike/` (gitignored scratch -- this memo is the durable record).

**Update (2026-06-14):** Q2's rerun snapshot/compare completed -- the R-2 verdict is in (VERIFIED, no overwrite detected). Q8 was re-probed from a second, independent sandbox instance -- still blocked on port 22, now with two data points.

---

## Q1 -- End-to-end access

**Status: VERIFIED**

`EntsoePandasClient.query_day_ahead_prices(DE_LU, ...)` authenticated with `ENTSOE_API_TOKEN` and returned 481 rows for 2026-06-08 -> 2026-06-13 (15-min resolution, current era). No 403/429s, no migration-related errors or warnings. Sample (EUR/MWh):

```
2026-06-08 00:00:00+02:00    152.12
2026-06-08 00:15:00+02:00    139.20
...
2026-06-12 23:45:00+02:00     93.60
2026-06-13 00:00:00+02:00    108.97
```

No R-3 symptoms observed in this session (no timeouts, no HTTP error codes, no parser exceptions).

---

## Q2 -- R-2 vintage probe (load forecast A65/A01 + VRE forecast A69/A01)

**Status: VERIFIED -- archive preserves as-published values; no overwrite detected**

This was the block's most important question. Three pieces of in-session evidence (below), then the rerun harness and its definitive result.

**1. `revisionNumber`/`createdDateTime` are not usable as vintage signals.** `explore` pulled A65/A01 and A69/A01 for six delivery dates spanning 2019-01-15 -> 2026-06-13 (D+1). Result, identical at every date including 2019:

| | A65/A01 load forecast | A69/A01 VRE forecast |
|---|---|---|
| `revisionNumber` | `1` (1 TimeSeries) | `3` (3 TimeSeries: B16 Solar, B18 Wind Offshore, B19 Wind Onshore) |
| `createdDateTime` | always == pull wall-clock time | always == pull wall-clock time |

`createdDateTime` is the API's response-wrapper generation time (always "now"), not the data's original publication time. `revisionNumber` is constant across 7+ years -- a 2019-01-15 delivery shows the same `revisionNumber=3` for its VRE forecast as a delivery from yesterday. If the platform continuously overwrote archived VRE forecasts with later intraday resubmissions over the years, we would expect revision counts to grow with elapsed time; they don't. Reading: `revisionNumber=3` looks like a static attribute of the TSOs' A69 submission template (one document, three PSR-type TimeSeries), not a live "this has been revised N times since gate-close" counter. **Neither field can adjudicate R-2 on its own** -- but see the final verdict below, where a *constant* `revisionNumber` across captures becomes corroborating evidence rather than a dead end.

**2. Direct evidence of publication-timing structure.** Pulled both forecasts for delivery date D+1 = 2026-06-13 at ~15:35 CEST on D-1 (2026-06-12):
- A65/A01 load forecast: **available**, 96 rows (full day, PT15M) -- consistent with its ~10:00 CET D-1 regulatory deadline (Art. 6(2)(b)), already passed.
- A69/A01 VRE forecast: **`NoMatchingDataError` (no data)** -- consistent with its 18:00 Brussels D-1 deadline (Art. 14(2)), not yet passed.

This is a clean confirmation that the platform genuinely has *nothing* for D+1's VRE forecast before the deadline (not an early/placeholder value that later gets overwritten) -- the publication-timing asymmetry described in capstone S3 is real and observable, and it is snapshot 1 in the final verdict below.

**3. Repeat-pull stability.** Two back-to-back pulls of a settled delivery day's (2026-06-05, D-7) VRE forecast within this session returned `Series.equals() == True` -- the platform is not returning jittery/regenerated values on repeated queries of the same period.

**Final verdict -- snapshot/compare rerun (`scripts/q2_vintage_probe.py`):**

Three snapshots of delivery date 2026-06-13 were captured across the publication and delivery lifecycle:

| # | Pulled at (UTC) | Context | load_fc (A65/A01) | vre_fc (A69/A01) |
|---|---|---|---|---|
| 1 | 2026-06-12 13:35:10 | D-1, pre-VRE-deadline | OK, 96 rows, rev=1 | `NO_DATA` |
| 2 | 2026-06-12 16:24:38 | D-1, ~2.5h post-VRE-deadline | OK, 96 rows, rev=1 | OK, 96 rows, rev=3 |
| 3 | 2026-06-14 12:03:47 | D+1, delivery day fully elapsed | OK, 96 rows, rev=1 | OK, 96 rows, rev=3 |

`compare --delivery-date 2026-06-13` pairwise results (`data/spike/q2_compare_2026-06-13.json`):
- **1 -> 2** (the publication-timing transition from point 2): `load_fc` rev 1->1, 96/96 common points, **0 differing**. `vre_fc` goes `NO_DATA` -> `OK` (a presence transition, not a value comparison).
- **2 -> 3** (the overwrite test -- ~44h later, after 2026-06-13 has fully elapsed): `load_fc` rev 1->1, 96/96 common, **0 differing**. `vre_fc` rev 3->3, 96/96 common, **0 differing**.

**Per-series verdict:**
- **A65/A01 (load forecast): NOT overwritten.** Identical across all three captures, from D-1 pre-publication through D+1 post-delivery -- 0 value differences, `revisionNumber` constant at 1.
- **A69/A01 (VRE forecast): NOT overwritten.** Snapshot 1 (`NO_DATA`) establishes only the publication-timing transition -- on its own it would prove presence, not overwrite-vs-not. But snapshot 2->3 *is* the direct overwrite test: the as-published values (captured ~2.5h after the 18:00 Brussels deadline) are bit-identical to the post-delivery archive (~44h later, after the delivery day fully elapsed) across all 96 quarter-hours, with `revisionNumber` constant at 3.

**Conclusion:** for this sample delivery day, the ENTSO-E Transparency Platform archives the as-published D-1 forecast and does not silently revise it after the fact. The M1 ingest pipeline can pull archived history directly with no special "first-seen-value" capture step, and the pre-authorized **S5.2 fallback is not invoked** for this sample. This is single-delivery-day evidence (n=1); if M1's full-history pull ever surfaces a delivery date where a re-pull differs from an earlier archived value, treat that as a contradiction of this finding and fall back to S5.2 for that date.

Snapshots: `data/spike/vintage/2026-06-13__20260612T133510Z.json`, `...20260612T162438Z.json`, `...20260614T120347Z.json`.

---

## Q3 -- Per-series native resolution, and since when

**Status: VERIFIED**

Sample pulls (3-day windows) at three points in time, for A44, A65/A01, A65/A16 (actual load), A69/A01:

| Window | A44 price | A65/A01 load forecast | A65/A16 actual load | A69/A01 VRE forecast |
|---|---|---|---|---|
| 2019-01-07 -> 01-10 | **PT60M** (24/day) | **PT15M** (96/day) | **PT15M** (96/day) | **PT15M** (96/day) |
| 2025-06-01 -> 06-04 (pre-MTU) | **PT60M** (24/day) | **PT15M** (96/day) | **PT15M** (96/day) | **PT15M** (96/day) |
| 2026-06-08 -> 06-11 (post-MTU) | **PT15M** (96/day) | **PT15M** (96/day) | **PT15M** (96/day) | **PT15M** (96/day) |

Confirms the expectation exactly: the load/actual-load/VRE feature feeds have been native PT15M for the entire archive (back to 2019), while A44 switches from PT60M to PT15M at the 2025-10-01 boundary (Q4). The quarter-hour -> hourly mean aggregation for the feature feeds is therefore needed across the *entire* 2019-pull-date window, not just post-transition -- a scope point for M1's ingest design (every feature feed needs the aggregation step from day one, not just from 2025-10-01).

---

## Q4 -- 15-min price boundary (2025-10-01)

**Status: VERIFIED**

Sample pull of A44 spanning 2025-09-28 -> 2025-10-04 (361 raw rows):

- Pre-transition (2025-09-28 -> 2025-09-30 23:00): 72 rows, **hourly** (`freq=h`).
- Post-transition (2025-10-01 00:00 -> 2025-10-04 00:00): 289 rows, **15-min** (`freq=15min`).
- Hourly-averaging the post-transition quarter-hours and concatenating with the pre-transition hourly series: **0 missing hours, 0 duplicated hours** across the full window.
- Spot-checked 8 post-transition hours: **every hourly value == mean of its 4 quarter-hours exactly** (e.g., 2025-10-01 07:00 hourly = 173.30 = mean(173.30, 173.30, 173.30, 173.30) -- to 1e-9).

This rehearses invariant test 4 (S9.4) successfully on a sample.

**Edge-case finding (affects M1 ingest design):** a pull whose `end` timestamp lands exactly on a quarter-hour (e.g., requesting `end="2025-10-04"` at local midnight) produces a **final hourly bin with only 1 of 4 quarter-hour points** when resampled -- a partial-bin artifact of the *query window*, not the underlying data (confirmed: `post.tail(2)` shows the 23:45 and 00:00 points are the last two of the pull; resampling `00:00` alone into its own hourly bin gives a "hourly" value equal to that single point). **M1 implication:** the bulk pull's per-chunk resampling must either (a) drop/recompute boundary bins after concatenating adjacent chunks, or (b) pad each chunk's pull window by one extra interval on each side before resampling. Same root cause hit Q6 below.

---

## Q5 -- Archive depth at/near 2019-01-01

**Status: VERIFIED**

Sample pull 2018-12-30 -> 2019-01-03 for A44, A65/A01, A69/A01 on DE-LU:

| Series | Status | n | Range |
|---|---|---|---|
| A44 price | OK | 97 | 2018-12-30 00:00 -> 2019-01-03 00:00 (+01:00) |
| A65/A01 load forecast | OK | 284 | 2018-12-31 01:00 -> 2019-01-02 23:45 (+01:00) |
| A69/A01 VRE forecast | OK | 384 | 2018-12-30 00:00 -> 2019-01-02 23:45 (+01:00) |

All three return non-empty DE-LU data spanning the 2019-01-01 window start (and a bit before, consistent with the DE-LU zone split on 2018-10-01). Minor note: A65/A01's earliest point in this window is 2018-12-31 01:00 rather than 2018-12-30 00:00 (a ~25h shorter edge than price/VRE) -- inconsequential for the 2019-01-01 window start, but worth a sanity check at the actual M1 pull if the window start were ever moved earlier.

---

## Q6 -- ENTSO-E <-> SMARD cross-pull

**Status: VERIFIED**

4-day sample (2026-06-08 -> 2026-06-12 local), DA price:
- ENTSO-E: 385 raw 15-min rows -> 96 complete hourly bins (1 partial boundary bin dropped, see Q4 finding -- same root cause).
- SMARD: filter `4169`, region `DE-LU`, `index_hour.json` + per-chunk `4169_DE-LU_hour_{timestamp}.json` -- both `DE-LU` and `DE` region codes work; 97 hourly rows returned, non-null back to 2018-09-30 22:00 UTC (402 weekly index chunks).
- **96/96 common hours within EUR 0.01/MWh (100.00%)**. Max abs diff = EUR 0.005/MWh, mean = EUR 0.0024/MWh -- pure 2-decimal rounding noise from SMARD's display rounding vs. ENTSO-E's higher-precision quarter-hour mean. Sample:

```
                           entsoe   smard  abs_diff
2026-06-08 00:00:00+00:00  132.71  132.71    0.0000
2026-06-08 02:00:00+00:00  130.18  130.18    0.0050
2026-06-11 21:00:00+00:00  116.06  116.06    0.0025
```

The cross-pull mechanism works end-to-end on both sources; sample agreement is well inside the CP-1 gate (>99.9% within EUR 0.01/MWh). The formal gate is a full-history M1 job.

---

## Q7 -- SMARD THE gas probe

**Status: VERIFIED (answer: No, with caveat)**

Checked the community-maintained OpenAPI spec for SMARD's `chart_data` API (`bundesAPI/smard-api`) -- the only gas-related filter is **`4071` "Stromerzeugung: Erdgas"** (electricity generation *from* natural gas, a generation-volume series), confirmed live (`GET /app/chart_data/4071/DE/index_hour.json` -> HTTP 200, data back to 2015). **No filter for a THE day-ahead gas *price* exists in this API.** SMARD's scope (per its own framing, "Strommarktdaten" / electricity market data) does not include gas commodity prices.

**Caveat:** SMARD recently added an "Energy data compact > Gas" front-end section (`smard.de/en/energy-data-compact/gas`) which the community spec may not yet cover, since it's JS-rendered and its data calls weren't visible to a static fetch. So this is a **preliminary No** -- if the orchestrator's S0-item-3 reopen decision hinges on this, a 10-minute browser-based check of that page's network tab (via Yarden) would close the gap. Per the brief, this is report-only; no gas wiring attempted.

---

## Q8 -- SFTP bulk path

**Status: PENDING-with-rerun-path (2/2 sandbox instances blocked)**

`socket.create_connection(("sftp-transparency.entsoe.eu", 22), timeout=10)` -> `TimeoutError`, reproduced on **two independent sandbox sessions** (2026-06-12 and 2026-06-14), both with otherwise-working HTTPS (ENTSO-E/SMARD/PyPI all fine in both sessions). `nc` is not installed in either environment, so the literal `nc -zv` one-liner couldn't be run -- `socket.create_connection` is the equivalent TCP-connect check and gives the same `TimeoutError`.

Two-for-two on port-22 timeouts across independently-provisioned sandboxes points to a **standing outbound-non-HTTP(S)-port policy on this class of cloud sandbox**, not a transient or session-specific issue -- but it still says nothing about reachability from Yarden's actual M3, which remains the only environment that can answer this.

**Re-run on Yarden's M3:** `nc -zv sftp-transparency.entsoe.eu 22` (or `sftp <account>@sftp-transparency.entsoe.eu`). Even if reachable, SFTP credentials are separate from `ENTSOE_API_TOKEN` and not present in any environment used so far -- account provisioning (if needed) is a separate B-Manual step. **One-line assessment:** for the M1 bulk pull's actual size (~66k hourly rows + ~26k native quarter-hourly rows, single-digit-MB compressed per S3), the chunked API (12 yearly Q1-style pulls per series) is almost certainly simpler and fast enough -- SFTP is worth revisiting only if the API proves unreliable in practice at M1, not as a default.

---

## CP-1 pre-confirmation

**Pre-confirmed:** the A44/A65-A01/A69 portion of CP-1 item 1 (non-empty recent data -- Q1/Q3; 2019-01-01 archive depth -- Q5) and SMARD reachability (Q6). **Not pre-confirmed:** A75 wind-onshore / wind-offshore / solar archive depth and completeness, added by v6.3 as the proper-training-only VRE-climatology fit target; that remains an M1 gate. Strong supporting evidence exists for item 3 (ENTSO-E<->SMARD sample: 100% of 96 hours within EUR 0.01/MWh -- Q6, full-history reconciliation remains an M1 job) and for the 15-min-boundary sub-clause of item 9 (continuity + exact hourly = mean-of-4-quarter-hours verified on the 2025-10-01 sample -- Q4).

**Remains open (by design -- this was a data-layer probe, not feature/pipeline code):** item 2 (the actual bulk pull, UTC/DST handling, Fold-5 date pinning), item 4's forecast-not-actual *code* guard, items 6-7 (regime flags, climatology -- M1 feature catalog), item 8 (CC BY attribution in a committed snapshot -- no snapshot exists yet), the DST and closed-left-rolling sub-clauses of item 9, and item 10 (leakage audit document).

**Item 5 (R-2 vintage probe) is VERIFIED** -- the snapshot/compare rerun (Q2 above) found zero value differences and a constant `revisionNumber` for both A65/A01 and A69/A01 across pre-publication, post-publication, and post-delivery captures of delivery date 2026-06-13. The archive preserves as-published values; the S5.2 fallback is not invoked for this sample.

**Findings that should shape the M1 plan:**
1. **Resampling boundary artifact (Q4/Q6):** any pull whose `end` lands exactly on a quarter-hour produces a partial final hourly bin. The M1 chunked yearly pulls must handle chunk-boundary bins explicitly (drop-and-let-the-next-chunk-complete, or pad-and-trim) -- otherwise this silently corrupts one hour per chunk boundary (12 hours/year if chunked yearly).
2. **PT15M is the native resolution for load/VRE feeds across the entire 2019-pull-date window** (Q3), not just post-2025-10-01 -- the hourly-aggregation step in the ingest pipeline applies uniformly from day one, simplifying the M1 ingest code (one aggregation path, not a date-conditional one for the feature feeds -- only A44 needs date-conditional handling).
3. **`revisionNumber`/`createdDateTime` alone are dead ends for R-2** (Q2), but the value-level snapshot/compare harness now gives a **definitive verdict: no overwrite detected** for the sampled delivery day -- M1 can pull archived history directly with no "first-seen-value" capture step.

---

## v6.3 interpretation note (appended 2026-07-22 — all measurements above unchanged)

The strict-gate methodology amendment (`capstone_V6_3.md`) reinterprets this probe's Q2 / Item-5 result **without changing any measurement above.** Archive stability (no overwrite) is confirmed and resolves the R-2 *overwrite* risk — **but it does not make delivery-day A69 available at the 12:00 gate.** The same probe established that A69/A01 for the delivery day is **not published until the 15:35–18:00 D-1 window, after the gate.** v6.3 therefore excludes delivery-day A69 and every feature computed from it from the champion's runtime schema; that vintage is confined to the §7.2 post-gate information benchmark. The champion proxies instead share one deterministic seasonal-diurnal expectation fit per fold on **proper-training-only aggregate A75 actual VRE**; A75 is a fit target, never a runtime feature, and its archive coverage is an unverified M1 gate. A lagged-A69/vintage substitute is not part of the frozen four-catalog experiment. The correct reading of Item-5 at v6.3 is therefore narrow: *the archive faithfully preserves the sampled post-gate A69 vintage for benchmark provenance*.
