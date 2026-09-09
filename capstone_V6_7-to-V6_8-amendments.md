# Capstone amendment record — v6.7 → v6.8

**Delivery-day availability correction. RATIFIED by the Owner 2026-09-09.** Drafted the same day by the Orchestrator under a task-scoped Governance Lockdown suspension, then twice independently reviewed. **`capstone_V6_8.md` v6.8 is the anchor** and `progress.md`'s Strategic Anchors name it. `capstone_V6_7.md` is superseded and retained as history.

---

## 1. What triggered this

An independent pre-landing audit of the M1/CP-1 candidate `368822de297e71f24fd08569815cae0289e65b96` returned **`FAIL`** and recommended **DO NOT LAND**. The Owner accepted the finding on 2026-09-09.

**The defect is in v6.7's text, not in the work built against it.** The Engineering Lead implemented the ratified specification correctly. The specification was wrong.

v6.7 defined price-feature availability **per row** — a strict `t−1` right edge, closed-left, plus a fixed UTC row-count lag (`24h = 24 rows, 168h = 168 rows, always`). That is the correct rule for a **rolling one-step-ahead** forecast. This project is not one. It emits the **whole D+1 curve once, at the 12:00 CET D-1 gate**, so a per-row boundary silently admits earlier hours of the delivery day into features for later hours of the same day — prices that do not exist at the forecast origin and that the model is being asked to predict.

**Measured on the candidate:**

- **64,537 of 67,343 rows — 95.83%** — carry rolling price features exposed to earlier same-delivery-day prices. Among complete base-catalog rows, 63,663 of 66,429.
- Mutating local hour 00 on 2026-03-01 changed hour 23's rolling mean, both standard deviations, the 5% quantile and the negative-price count.
- **Second manifestation, DST.** On the 25-hour fall-back day 2025-10-26, the target at local 23:00 (UTC 22:00) minus 24 UTC hours resolves to 2025-10-25 22:00 UTC — **local hour 00:00 of 2025-10-26, the same delivery day.** `price_lag_24h` consumed a price from the day being forecast.
- **Reproducibility consequence.** Fresh pre-gate inference could never reproduce the historical feature matrix: the delivery-day hours would be absent at 12:00 D-1, while backtesting populated them from outcomes.

The audit also found the §9.4 test suite passing while missing the defect — test 2 mutated only a row's *own* target — and found three further gaps recorded in §2 below.

---

## 2. Exact amendment map

Every edit below is applied in `capstone_V6_8.md`. Nothing else in the document changes.

| # | Site | Change |
|---|---|---|
| A-1 | **§5.2**, LAG bullet | Insert the **delivery-day availability invariant** verbatim as a governing rule stated once and binding everywhere. Rewrite the LAG bullet to bound features by delivery date rather than row offset, and **name the retired v6.7 formulation as retired**, with the reason. |
| A-2 | **§4.0**, UTC indexing paragraph | Replace `compute all lags in UTC so 24h = 24 rows, 168h = 168 rows, always` with **calendar-day lag matching**: 24h/48h/168h resolve to the same local hour of `D−1`/`D−2`/`D−7`. A fixed row offset is forbidden. A non-existent (spring-forward) or ambiguous (fall-back) match **fails closed as null**. |
| A-3 | **§4.0**, same paragraph | Add the **A65 daily completeness rule**: any per-delivery-day A65/A01 statistic requires the complete set of expected local hours — 23, 24 or 25 as the calendar requires. **A null-skipping partial-day mean is forbidden**; an incomplete day yields null. |
| A-4 | **§4.1**, rolling price statistics | Replace the strict `t−1` closed-left edge with a **D-1 frozen boundary for the whole forecast curve**: every target row of `D` receives the same rolling value, computed over delivery dates `≤ D−1`. State explicitly that per-row closed-left is **not sufficient and is forbidden here**. |
| A-5 | **§4.1**, Candidate 1 | Restate the `base` catalog as calendar-day-matched lags and D-1-frozen rolling statistics. |
| A-6 | **§5.2**, audited vector (i) | Widen from "the target is never in its own window" to **"no hour of the delivery day is inside any feature window"**. |
| A-7 | **§9.4**, header | **Eight mandatory tests become nine.** |
| A-8 | **§9.4 test 2** | Rewritten. Day-level mutation sweep across every hour of `D`, checking every price-derived column on every row of `D`, on an ordinary day and both DST days; plus 24h/48h/168h lag resolution to `D−1`/`D−2`/`D−7` across 23- and 25-hour days, never sourcing `D`, failing closed when unavailable or ambiguous. The v6.7 form is **named as insufficient**. |
| A-9 | **§9.4 test 8** | Assertions completed. Calibration and holdout disjoint from **every component of every development fold** (train, calibration, eval separately, fold by fold) and from **every diagnostic window**, asserted directly; **every embargo asserted to contain exactly one complete delivery day**. |
| A-10 | **§9.4 test 9** | **New.** A65 daily completeness fails closed, including an explicit construction of a 25-hour day with one hour absent. |
| A-11 | **§12 M0** | Ratification history extended; both amendment records named. |
| A-12 | **§12 CP-1 item 3** | Catalog restated; adds that every price-derived champion feature satisfies the §5.2 invariant. |
| A-13 | **§12 CP-1 item 4** | Exclusion and embargo rules restated to match A-9, and required to be asserted **explicitly rather than implied**. |
| A-14 | **§12 CP-1 item 6** | Nine tests, naming the new coverage — day-level leakage, DST lags, inclusive-right-endpoint normalization, half-open Berlin slicing, 92/96/100 quarter counts, completed partition assertions, A65 completeness. Adds: **"A test that passes without exercising its invariant does not satisfy this item."** |
| A-15 | **§12 CP-1 item 7** | Leakage audit must classify against the invariant and **name, for each price-derived feature, the latest delivery date it can consume**. Adds: no feature may be called gate-available on a row-wise `t−1` boundary. |
| A-16 | **Title, footer, §1 delta block** | Version markers to v6.8; a `v6.7 → v6.8` delta block added. |

**Consistency edits found during execution.** A full scan after the mapped edits found three further sites that the amendment had left contradicting itself. They are directly necessary and are covered by the same suspension.

| # | Site | Change |
|---|---|---|
| C-1 | **§9.4 test 3** | v6.7's test asserted *"a 24h/168h lag in UTC retrieves the correct row"* — the rule A-2 just retired. Rescoped to **DST delivery-day identity**: expected local-hour count, the fall-back hour retained as two distinct UTC rows, the spring-forward hour not synthesized, no hour dropped or duplicated. Lag resolution now belongs to item 2 and is explicitly handed there. |
| C-2 | **§13 interview script** | Listed the eight tests including *"closed-left rolling windows"*. Now lists **nine**, with day-level delivery-day leakage, calendar-day lag resolution, DST delivery-day identity and A65 daily completeness. |
| C-3 | **§13**, same block | *"eight tests and thin workflow required by §9"* → **nine**. |

**Review round R — corrections from the independent review of this amendment (2026-09-09).** An independent reviewer examined the draft for further wrong substance and found six items. Five are applied here under the same suspension; the sixth is out of its scope and is escalated in §6.

| # | Site | Change |
|---|---|---|
| R-1 | **§9.6** | **HIGH — the amendment had missed this.** §9.6 still mandated the retired algorithm by its SQL name: *"the lag-24h/168h and rolling-statistic constructions expressed as SQL window functions (`LAG`, `OVER (… ROWS …)`)"*. The rejected candidate implemented it literally (`ROWS BETWEEN 168 PRECEDING AND 1 PRECEDING`), and this artifact sits in the **public §10 reading order** — it would have published the wrong methodology. Rewritten to require calendar-day joins and D-1-frozen rolling queries, and to **name the fixed-offset and closed-left constructions as non-satisfying**. |
| R-2 | **§4.1** | Window length was implementable two ways — 168/720 observations, or 7/30 complete delivery days, which differ across DST. Pinned to **168 / 720 canonical hourly observations ending at the close of `D−1`**, computed once per delivery day and broadcast to every row. |
| R-3 | **§9.4 test 2** | A mutation sweep alone is satisfied by an all-null or over-frozen implementation. Added an independent numerical oracle, a non-null assertion, an identical-across-`D` assertion, a **positive-control mutation of an eligible `D−1` input**, and a case where the matched source day is itself a DST day. |
| R-3b | **§9.4 test 9** | Same vacuity. Added a positive control on complete 23/24/25-hour days before the missing-hour assertion. |
| R-4 | **§9.4** | Said *"All eight are CP-1 acceptance requirements"* immediately after defining nine. Corrected, and restated to say the candidate holds the v6.7 versions of items 1–8 while the v6.8 nine-test set does not yet exist. |
| R-5 | **§12 CP-1 item 3** | Binds the §9.6 SQL artifact to the same semantics, so a remediation cannot satisfy CP-1 while leaving the SQL wrong. |
| R-6 | **§3**, Ember / ICAP row | **Applied under an extended suspension granted 2026-09-09**, after this record had escalated it as out of scope. §3 still offered the EUA feature as *"wired only if trivially clean at M1"* while §4 recorded it **retired at v6.7** and §4.1 permits exactly two frozen catalogs — a contradiction **pre-existing in ratified v6.7**, not introduced here. The row is **kept rather than deleted** so the retirement stays legible, and restated to say plainly that it is not a champion input and may not be wired at M1. **No live feed, identifier or catalog changes** — the feature was already retired; only the contradiction is removed. |

**Second review round S — the same reviewer re-examined the applied result (2026-09-09).** Verdict: `RATIFY WITH CHANGES`, with one narrow correction, and **the reviewer reversed its own earlier wording** on the strength of an executable counterexample.

| # | Site | Change |
|---|---|---|
| S-1 | **§9.6** | **R-1's prohibition was overbroad and is corrected.** It banned `LAG(price, n)` by *syntax*. The reviewer demonstrated that `LAG(price, 1) OVER (PARTITION BY local_hour ORDER BY delivery_date)` over a complete **delivery-date × local-hour grid**, with unavailable and ambiguous sources represented as null, implements `D−1` matching exactly — executed against explicit calendar joins on 7,512 target rows spanning both DST transitions, **zero mismatches at offsets 1, 2 and 7**. The defect was never the operator; it was the operator applied to **UTC hourly rows**. §9.6 now permits joins and window functions alike and names what fails **by behaviour**: fixed offsets over the UTC hourly price rows, and rolling windows that advance with the target hour within `D`. |
| S-2 | **§12 CP-1 item 3** | Same correction. Compliance is determined by the semantics — source identity, the unavailable/ambiguous rule, exact window lengths — **regardless of whether the SQL uses joins or window functions**. |

**What the second review also established, and what it did not.** It confirmed R-1…R-6 correctly applied; re-derived the information boundary independently; and demonstrated that **R-1, R-2 and R-3 are jointly implementable** by constructing an implementation that satisfies all three — nine target-day cases including both transitions and the days one, two and seven after each, 216 individual same-day mutations, daily constancy of every rolling value, agreement between pre-`D`-only and full-history inputs, and rejection of both an all-null and a `D−2`-frozen implementation. It found **no defect introduced by the interaction of the six repairs**. It could not certify a future implementation, and it noted honestly that on the wording it had supplied it was re-examining its own work.

**One clarification it recorded against itself:** the first review overstated the case when it treated the operator names `LAG` and `ROWS` as proof of a mandated bad algorithm. The candidate's actual hourly-row queries were demonstrably wrong; the operators alone did not establish that.

### The invariant, verbatim as ratified

> For every forecast of delivery day D produced at the 12:00 CET D-1 forecast origin, every price-derived feature may consume only day-ahead prices whose delivery date is earlier than D. Row-wise `t−1` is not a sufficient availability boundary and must not be used when it permits any delivery-day-D price into a feature for D. Rolling price features must be frozen at a D-1 boundary for the whole forecast curve. Calendar-day lag matching and its 23/25-hour DST behavior must be explicit and deterministic; an unavailable or ambiguous pre-D match must fail closed rather than consume a same-day price.

---

## 3. What does not change

Asserted, not assumed. **No** feed identifier, EIC, document type or SMARD filter; **no** fold scheme, partition arithmetic (242 = 90+1+60+1+90) or the 152-day raw-model-fit cutoff; **no** metric, DM construction, CQR or isotonic rule; **no** model choice or hyperparameter; **no** scope boundary in §13; **no** §0 ratified decision; **no** governance rule, checkpoint contract, terminal status, timebox convention or publication authority; **no** change to the residual-load proxy, which was already correctly bounded at `D−2` and is **not implicated** by this defect; **no** change to §7.2's benchmark, §9.2's release shape, or the three-checkpoint arc.

**CP-1 remains ten items.** No item is added or removed; four are amended.

*Scope note, recorded honestly: §3 is touched by R-6. The edit removes a contradiction about an **already-retired** option and adds, removes and repoints no live feed, EIC, document type or SMARD filter. Every identifier the champion or benchmark actually consumes is byte-identical to v6.7.*

---

## 4. Acceptance test for the application

The application of this amendment is correct when all of the following hold against `capstone_V6_8.md`:

1. The title and footer read v6.8.
2. A `v6.7 → v6.8` delta block exists in §1 and names the audit as its trigger.
3. The invariant appears in §5.2, verbatim as ratified, exactly once.
4. `24h = 24 rows, 168h = 168 rows, always` appears nowhere.
5. `strict `t−1` right edge` appears nowhere except where the retired v6.7 rule is explicitly named as retired.
6. §9.4 says **nine** mandatory tests and contains items 1–9 with no gaps.
7. §12 CP-1 still contains exactly ten checkboxes.
8. Items 3, 4, 6 and 7 of CP-1 carry the amended text; items 1, 2, 5, 8, 9 and 10 are byte-identical to v6.7.
9. `git diff capstone_V6_7.md capstone_V6_8.md` touches only the sites listed in §2's amendment map, **and no unlisted hunk**.
10. No governance file or role document changed as part of this amendment. *(The `progress.md` anchor pointer moves on ratification, and did — see §5.)*
11. §9.6 and CP-1 item 3 constrain the SQL artifact by **semantics, not syntax**: no construction is excluded on the strength of the operator it uses.

---

## 5. Cascade on ratification

1. `progress.md` Strategic Anchors repoint from `capstone_V6_7.md` v6.7 to **`capstone_V6_8.md` v6.8** — Orchestrator, after ratification only.
2. One new self-contained **M1/CP-1 remediation brief** to a **separate** Engineering Lead, against the v6.8 anchor.
3. `program-stage-sequence.md` is a static non-anchor derived from the ratified plan; its CP-1 row cites section numbers that did not move. **No rebuild is required**, and none is authorized by this amendment.
4. The CP-1 candidate `368822de…` does not land. `gauntlet/cp-1` and its evidence tip `c0b6e180…` are preserved pending an Owner disposition. **The superseded Integration verdict is reachable from that branch; the independent pre-landing audit is not.** It is owner-supplied external evidence, committed nowhere — verified: `c0b6e180…` adds only `docs/track-b/evidence/cp-1/integration.md`. **No tag can preserve evidence that is not in the history**, so if the audit is to survive the branch it must first be committed into the CP-1 evidence directory. *(Corrected 2026-09-09 after an independent review found this record claiming otherwise.)*

---

*Drafted by the Orchestrator. The drafting agent does not certify its own work: this record and `capstone_V6_8.md` require Owner ratification, and the application should be independently verified against §4 before the remediation brief is issued.*

---

## 6. Escalation, closed

This record previously escalated the §3 Ember / ICAP contradiction as outside the granted suspension. **The Owner extended the suspension on 2026-09-09 and the fix is applied as R-6 above.** Nothing remains escalated.

---

*Drafted by the Orchestrator; revised after an independent review of this amendment found six further items, five applied under the original suspension and one under the extension. The drafting agent does not certify its own work: this record and `capstone_V6_8.md` require Owner ratification.*
