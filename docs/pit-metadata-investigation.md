# Can source metadata replace the point-in-time capture? — live investigation

**Date:** 2026-09-04. **Authorization:** owner instruction to re-open and attack the question in
full, after he rejected the Month-0 spike's one-line finding as implausible. **Scope:** read-only
GETs against the ENTSO-E Transparency Platform Web API and the SMARD JSON API, with the owner's own
`ENTSOE_API_TOKEN`. No repository code was added; probe scripts ran from a scratch directory. $0.

**The question.** `capstone_V6_6.md` §3 requires an observed point-in-time capture ledger — the
B-Man-PIT block, run at ~10:30 and ~11:45 Europe/Berlin on D-1 across three non-consecutive delivery
days — to establish that A65/A01 is *empirically* known before the 12:00 CET gate. If the platform
published an honest per-datapoint publication timestamp, the ledger could be replaced by a query and
the timed capture dropped.

**The answer: no — but for a much more specific reason than "the API doesn't have it."**
The platform *does* have update-tracking machinery, it *does* work, and it is simply not attached to
day-ahead load forecasts. Evidence below.

---

## 1. The parameter vocabulary is strictly validated

An invented parameter is rejected, so acceptance is informative rather than permissive:

| Request | Result |
|---|---|
| `+asOf=202608041000` | **HTTP 400** · `Acknowledgement_MarketDocument` · code 999 · *"Input parameter does not exist: asOf"* |
| `+version=1` | **HTTP 400** · *"Input parameter does not exist: version"* |
| `+zzzUnknown=1` (control) | **HTTP 400** · *"Input parameter does not exist: zzzUnknown"* |

Whereas these were **accepted** (HTTP 200) on an A65 query: `periodStartUpdate`, `periodEndUpdate`,
`timeIntervalUpdate`, `docStatus`. So the update/version vocabulary exists in the API.

## 2. That machinery genuinely works — proven on A80

`A80` (production/generation unavailability) is a document type the platform *does* revise.
Same parameters, same bidding zone, delivery window 2026-08-01 → 2026-08-08:

| Request | Result |
|---|---|
| A80, no update window | HTTP 400 — *"The number of instances (352) exceeds the allowed maximum (200)"* |
| A80 `+ periodStartUpdate=2019-01-01, periodEndUpdate=2019-01-02` | HTTP 200 — **"No matching data found"** |
| A80 `+ periodStartUpdate=2026-08-01, periodEndUpdate=2026-09-04` | HTTP 200 — **201,208 bytes** |

The 2019 window correctly returns nothing; the Aug-2026 window returns the data. **The update-time
filter is real and functioning.**

## 3. It is accepted and silently ignored for A65

Same A65/A01 query, DE-LU, delivery day 2026-08-05. Payload hashed with the two volatile header
fields (`mRID`, `createdDateTime`) normalized out:

| Request | Points | SHA-256 (16) | Bytes |
|---|---|---|---|
| baseline, no update window | 96 | `5ceebf5aeaff0cc1` | 13607 |
| `+ update window 2019-01-01…01-02` | 96 | `5ceebf5aeaff0cc1` | 13607 |
| `+ update window 2026-08-01…08-02` | 96 | `5ceebf5aeaff0cc1` | 13607 |
| `+ update window 2027-01-01…01-02` (future) | 96 | `5ceebf5aeaff0cc1` | 13607 |
| `+ docStatus=A05` (active) | 96 | `5ceebf5aeaff0cc1` | 13607 |
| `+ docStatus=A09` (cancelled) | 96 | `5ceebf5aeaff0cc1` | 13607 |
| `+ docStatus=A13` (withdrawn) | 96 | `5ceebf5aeaff0cc1` | 13607 |

Byte-identical in every case, including a window entirely in the future. **A65 carries no update
dimension** — not because the platform is primitive, but because a day-ahead load forecast is
modeled as a *single non-revisable publication*, unlike a revisable outage notice.

## 4. `createdDateTime` is response-generation time — reconfirmed directly

The complete `GL_MarketDocument` header contains exactly one timestamp. Two sequential A65 queries
for different delivery dates returned `createdDateTime` of `2026-09-03T23:46:43Z` and
`2026-09-03T23:46:49Z` — **six seconds apart, matching the interval between the two requests.**
`revisionNumber` is `1`. The full tag inventory of the document is: `mRID`, `revisionNumber`, `type`,
`process.processType`, sender/receiver participant + role, `createdDateTime`,
`time_Period.timeInterval`, then per-TimeSeries `businessType`, `objectAggregation`,
`outBiddingZone_Domain.mRID`, `quantity_Measure_Unit.name`, `curveType`, `Period`, `resolution`, and
96 `Point`/`position`/`quantity` triples. **There is no publication-time field of any kind.**

## 5. SMARD has a `created` field — genuine, stable, and still unusable

SMARD data files carry `{"meta_data":{"version":1,"created":<epoch ms>}}`. It is real: re-fetching
the same file three seconds later returned an identical `created`. But it is **file-build time**:

| Weekly file starts | `meta_data.created` | Gap |
|---|---|---|
| 2018-10-28 | **2026-05-29** | ~7.6 years after the data |
| 2024-12-15 | 2025-03-18 | ~3 months after |
| 2026-07-26 | 2026-08-03 | 8 days after |
| 2026-08-30 (current) | 2026-09-03 23:48 | ~1 minute before the probe |

`created` is always *after* the delivery day and moves whenever the archive is regenerated, so it can
never evidence availability *before* a gate on a past day. `version` is `1` on every file.

## 6. The SFTP bulk route

`sftp-transparency.entsoe.eu:22` — **not reachable** (third independent observation, after the
Month-0 spike's Q8 probed it twice). Its monthly files are regenerated on update in any case, so they
inherit the same defect as SMARD's weekly files.

---

## Conclusion

**The archive preserves values, not times.** The Month-0 finding stands, now on far stronger
evidence: it is not that the platform lacks versioning, it is that A65 is deliberately not a
versioned document. No source-declared field on either ratified source can substitute for an
observed capture, so `capstone_V6_6.md` §3 is unchanged and no amendment was warranted or made.

**What the investigation did change.** The objection behind the question — being tied to specific
hours — is real and is solved without touching the contract: the CP-0-reviewed instrument at
`src/pit_capture/` takes its token from the environment and needs no judgement at run time, so a
scheduled job can execute the two instants with nobody present. The evidence requirement is about
*when the observation happened*, never about who was awake for it.

**Reopening condition.** A re-probe that returns a real per-datapoint publication timestamp for
A65/A01. Nothing short of that.
