# PRES-6 editorial review

| Item | Value |
|---|---|
| Commit reviewed | `2da56fa9c15c38072a98370c1a7c790bfb7bf6cb` (`gauntlet/pres-6`), detached checkout `.local/worktrees/pres-6/editorial`, tree clean |
| Page verified | `docs/index.html` SHA-256 `06796448d1cd47e615c888be5e06b9642c48b6e6acee89a4fa1afed0b4d05663`, 1,997,595 bytes |
| README verified | `README.md` SHA-256 `9fc80a8462b71208bd765769072d1a3be924f50996122c577a66017c34304ae2`, 61,604 bytes |
| Published base | `main` = `29b6431e`: `docs/index.html` `983a75c44b0f93dabd183ee810158aefbfa62adfb5545b4a433afe4b5bbb9475` and `README.md` `bc98e9ccb74546a2d3fbdbbfabd8034bc63addfc165c0264598f1a1d3747c472`, both equal to the brief's |
| Rules | `docs/PUBLISH_RULES.md` `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e` (rev 1.5, the brief's); standard v1 §§1–7 |
| Date | 2026-11-14 |

**Independence and method.** I authored none of PRES-6's changes. I worked read-only: no edit, stage, commit or push in
any checkout, no network use, and no credential read. My only writes are this file and throwaway scripts and text dumps
under `.local/tmp/pres-6/editorial-scratch/`. I read `AGENTS.md` (as `CLAUDE.md` directs), the brief, the packet, the
claim map, PUBLISH_RULES §§2, 3, 5, 5.1, 5.1a, 6, A1, A2, A8 and the standard §§1–7. I did not open the memory
directory, `progress.md`, any syllabus, Track A or C material, or `orchestrator-role.md`. Python ran with
`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1`.

I read the new text on the reading path first (every disclosure closed, tables and SVG-only text excluded), then the
disclosure bodies, tables and chart text. **Not checked here:** browser rendering, A2 placement, the test suites, and the
bootstrap intervals (not re-run). The `--final` build is also not checked.

**The page budget bounds every fix below.** At this commit the page is 2,405 bytes under the 2,000,000-byte budget.
Every wording fix proposed here is short, but together they must still fit. E2's lines cost the most, about 1.5 KB.

---

## Checks that passed

1. **A8's order.** The section order is `top` → `product` → `outcomes` ("Product results") → `business` ("Business
   insights") → `research-results` ("How the models compare") → `journey` → `chapters` → `planned` → `evidence` →
   `contribution` → `attribution`. On `main` it was `top` → `product` → `research-results` → the same tail.
   - The header's "Results" link now targets `#outcomes`; it was `#research-results`. "Compare model results" in the
     opening still targets `#research-results`.
   - The twelve product topic routes (`docs/index.html:475`) stay outside any disclosure.
   - The opening keeps "Final candidate · pending 4.7T", the Space link and "v1's historical demo"; its text is unchanged
     from `main`.
2. **Every bound number matches its committed row.** I parsed every `data-record` element in `docs/index.html:446–535`
   (the opening, How the product works, Product results and Business insights).
   - 311 text bindings equal the committed value from `reports/pres6/product-results/*.csv` or `summary.json`, rounded
     at the record's precision, and each `value` attribute equals the raw row. There were no mismatches.
   - 78 chart marks are also bound.
   - The script reads the rows directly and does not use `research.py` (`editorial-scratch/verify_records.py`).
3. **The rows re-derive from their sources.** I recomputed these myself:
   - **`regimes.csv` and `coverage.csv`** from `reports/cp28/results/daily-losses.parquet` (streams A1 and B0). All four
     populations match: 2,068, 246, 481 and 1,341 days; 49,596, 5,900, 11,536 and 32,160 hours. The mean daily MAE and
     WIS match, as do the hour-weighted coverage and width at 50, 80 and 95%.
   - **The three chosen days,** by §0's lower-median rule over the P-v5 days: 2021-06-16 (90 days, MAE 5.3034),
     2022-07-26 (88, 35.0559) and 2025-05-02 (180, 12.0779).
   - **`explanation.csv`** from `reports/cp17-probe/native-reference.json`, counting delivered hours only (23 and 24).
     The largest difference is 5e-15, and the baseline and issued means match.
4. **The chart geometry matches the rows (spot checks).**
   - The three-day chart's median and observed lines match `days.csv` within 0.53 px on all 72 hours.
   - The monthly chart's points match `monthly.csv`: the naive's 2022-09 point at 130.6 and v6's 2022-12 at 55.7.
   - The regime chart's marks and whiskers match `regimes.csv`, for example pre-crisis v6 6.25 [5.54, 7.01].
5. **A1.** Each headline number names its metric beside it, except the explanation's figures (E6):
   - the finding: "mean daily point error … EUR/MWh", "80% intervals covered … of the hours";
   - the regime ratios: "ratio" of the "mean daily point error";
   - coverage with "mean widths";
   - Business: "misses the hourly price by", "interval … wide", "held … of the hours".
6. **Evidence class.**
   - No record in `#outcomes` or `#business` describes a day after 2026-09-06, and none is a live record.
   - The class is stated as "Development evidence after selection" (`outcomes.caveat`) and "development, post-selection"
     (`outcomes.sub`).
   - The page says the Space holds the live record, "prospective evaluation in progress". 4.7T appears only as the
     future test.
7. **W54 and W55.**
   - "profit", "success rate", "value" and "loss" occur only in negations (`business.gap`).
   - `#business` has no chart.
   - No product result is called prospective, live, unused-data or 4.7T evidence.
   - `test_51` asserts that neither the page nor the README has a W54 or W55 hit; I did not run it. My own search of
     both surfaces found none.
8. **The explanation's source and label.**
   - `outcomes.explanation.terms` says each value attributes "that day's issued median within one fitted model" and that
     it is "not a cause, not the value an input adds, and not how the model behaves on other days".
   - Both days fall on or before 2026-09-06.
   - The evidence row cites `blob/evidence/cp-17/reports/cp17-probe/native-reference.json`, labelled "frozen 2026-10-28":
     - the tag `evidence/cp-17` = `3876bcdc` is dated 2026-10-28;
     - the file at the tag hashes `f1decb80…96ab`, as the packet pins;
     - its commit `42e27c70` (2026-10-27) is reachable from the tag.
   - The headings are a separate problem (E1).
9. **The qualitative claims hold on the rows.**
   - "below the similar-day naive in every month on both scores": the smallest margin is 2020-12, 0.0095 EUR/MWh in MAE
     over 3 days.
   - "both peak in the crisis months": v6 peaks in 2022-12, the naive in 2022-09.
   - "In the crisis they covered least … and were widest": true at all three levels.
   - "each interval below one": the ratio intervals' upper bounds are 0.4912, 0.5425 and 0.5376.
   - "none is thin": the smallest regime has 246 days.
   - On both days the load forecast for the day and the weather moved the median most: 14.35 and 14.01 on 2026-03-29;
     43.67 and 30.77 on 2026-09-06, with prices of the day before third.
   - "2.7" is `price_d2`'s mean absolute contribution.
   - The bins' 80% coverage runs from 0.6868 (bin 2) to 0.8685 (bin 5).
10. **The README** gains "**Product results:**" and "**Business insights:**" (`README.md:23`, `:25`), in that order, after
    "How the product works".
    - Their text is the page blocks' (`outcomes.finding` + `outcomes.caveat`; `business.*`).
    - The numbers are identical: 2,068; 17.2 [15.4, 19.1]; 34.6; 0.7826; 30.7; 51.7.
11. **The comparison and later sections** (`main` line 479 on, against this page's line 536 on) differ in exactly five
    places:
    - R3: the overview values table's code cells read "A1, PRES-5", "v5, CP-24" and "A1, CP-24" (a disclosure table);
    - R5: `everyday.question` was added;
    - R1: `everyday.finding.v6` now reads "the lowest error of the re-baseline's policies";
    - R2: `v6.fresh.terms` now reads "The p-values come from";
    - R7: `v6.fresh.meaning` now reads "While v6 runs on the Space, its live record stays …".

    No bound value changed. In the page head, the only changes are two CSS rules for the new rows and the header's
    "Results" target.
12. **The five product topics gained routes,** each keeping its earlier route. Each route has a label that describes it
    and a target that exists:
    - topic 2 → `#outcomes-regimes`;
    - topic 5 → `#outcomes`;
    - topic 6 → `#outcomes-explanation`;
    - topic 8 → `#outcomes-time`;
    - topic 9 → `#outcomes-coverage`.
13. **Business insights covers its four required parts:**
    - the intended use;
    - the measured implications;
    - the gap ("No decision policy, cost model or trading simulation has been authorized or run");
    - the limits.

---

## Findings

### E1 — violation: the explanation is headed as a general, causal account

- **Where:**
  - `docs/index.html:513`, `h4#outcomes-explanation`, "What drives its forecasts";
  - `:488`, the "Explore these results" item "What drives its forecasts";
  - `:475`, product topic list item "What drives its forecasts". On `main` it read "What drives its forecasts: live
    product".
  - Source: `scripts/build_pages.py:2133`, `:2416`, `:2866`.
- **Why it matters:**
  - The explanation ruling (packet §10.1) requires the label to say this is an attribution of the named development
    days' issued median within one fitted model, never causality, incremental value or general behaviour.
  - "Drives" frames a cause. "Its forecasts" claims general behaviour.
  - Both contradict the section's own terms line, "not how the model behaves on other days", and §5.1 subject 7
    ("Distinguish attribution from … causality").
  - The topic list item, on the reading path, lost its ": live product" scope. It now promises a general explanation.
- **Fix:**
  - h4 and Explore item: "Which inputs moved its median on two development days". This is the text topic 6's route
    already uses.
  - Topic list item and topic 6's h3: "What moved its forecasts: two development days and the live product".

### E2 — violation: no graphic visibly names its own artifact, and most omit their evidence class and dates

- **Where:**
  - `#outcomes`, the five charts (`docs/index.html:493`, `:498`, `:503`, `:509`, `:515`) and the bins table (`:523`);
  - `scripts/build_pages.py:2392–2425`.
- **What is visible today:**
  - **The identity line.** The one visible identity line is `outcomes.sub` (`:486`), inside the finding's panel, which
    holds no chart. It names "every eligible development day, 2020-12-29 to 2026-09-06". That is the wrong population
    for the three-day chart, the explanation and the bins (358 days of v5's test periods).
  - **Per chart:**

    | Graphic | Artifact | Class | Population or dates |
    |---|---|---|---|
    | Three-day chart | not named | not named | given |
    | Time chart | not named | not named | months given; the population ("every eligible development day") not named |
    | Regime chart | not named | not named | regime dates missing |
    | Coverage chart | not named | not named | dates missing |
    | Explanation chart | given | "post-selection" missing | given |

  - **The SVG text.** Each chart's `<title>` and `<desc>` carry "Development evidence after selection", but those are
    hover or screen-reader text only.
- **Why it matters:**
  - The brief's outcome 2 and §5.1a: "Each graphic names the policy/artifact, population, dates, units and evidence
    class".
  - §6: "No meaning depends on colour or hover alone".
  - Packet §9.1 states each chart carries all six, which the visible page does not bear out. `test_51` checks only the
    section-level line.
- **Fix:** add one visible line under each heading, generated from the claim layer like `outcomes.sub`:
  - **days:** "v6's stored forecasts · 2021-06-16, 2022-07-26 and 2025-05-02, by local hour · EUR/MWh · development,
    post-selection";
  - **time:** "v6's and the naive's stored daily errors · every eligible development day, 2020-12-29 to 2026-09-06 ·
    EUR/MWh, calendar-month means · development, post-selection";
  - **regimes:** "v6's and the naive's stored daily errors · 2020-12-29 to 2021-08-31, 2021-09-01 to 2022-12-31,
    2023-01-01 to 2026-09-06 · EUR/MWh · development, post-selection";
  - **coverage:** "v6's stored forecasts · every eligible development day, 2020-12-29 to 2026-09-06 · share of hours;
    width in EUR/MWh · development, post-selection";
  - **explanation:** "v6's fits for 2026-03-29 and 2026-09-06, the committed attribution · EUR/MWh an hour ·
    development";
  - **bins:** "v6's stored forecasts · 8,587 hours on 358 days of v5's test periods · EUR/MWh · development,
    post-selection".

  If the budget cannot hold six lines, reword `outcomes.sub` to apply to every graphic. Its population would then read
  "every eligible development day, 2020-12-29 to 2026-09-06, unless a graphic names fewer". The time, regime and
  coverage paragraphs would then need their dates added.

### E3 — violation: the product finding gives coverage without width, and differs from its claim P68

- **Where:**
  - `h3#product-finding`, block `outcomes.finding` (`docs/index.html:484`; `research_claims.py:1082`);
  - `README.md:23`;
  - claim map `pres6-claims.md`, P68.
- **Quoted:** "…against the similar-day naive's 34.6; its 80% intervals covered 0.7826 of the hours."
- **Why it matters:**
  - §3.2: "Coverage is presented together with width." The README line never gives the width.
  - P68 promises "point error and interval score … with their intervals, and its 80% coverage with width". The rendered
    finding has neither the interval score nor the width.
- **Fix:**
  - Change the finding to "…against the similar-day naive's 34.6; its 80% intervals, 51.7 EUR/MWh wide on average,
    covered 0.7826 of the hours." (`{r:pres6.coverage.all.80.width_eur}`).
  - Amend P68 to "v6's mean daily point error on every eligible development day against the naive, with its interval,
    and its 80% coverage with width".
  - Re-measure A2. The phone margin is only 25.5 px (packet §10.3 item 1). If the added clause breaks A2, drop the
    coverage clause from the finding and amend P68 to match instead.

### E4 — violation: the regime values table has no unit

- **Where:** `details#outcomes-regimes-table` (`docs/index.html:504`; `scripts/build_pages.py:2308`).
- **Quoted:**
  - Caption: "Mean daily error by regime, with 95% intervals of the mean".
  - Columns: Regime, Days, Hours, Score, v6, Naive, Ratio. No EUR/MWh appears anywhere in the table.
- **Why it matters:**
  - §6: "Exact-value tables retain definitions and units".
  - §3.4: "State metric, unit".
  - The overview table further down uses "Interval score (S_WIS)" for a ratio to the naive (about 0.44). Here
    "Interval score 9.7" is EUR/MWh. Without the unit, the two are easily confused.
- **Fix:** caption "Mean daily error by regime, EUR/MWh, with 95% confidence intervals of the mean; the ratio is v6's
  mean divided by the naive's". Ideally also give the regime dates in the row headers ("Before the crisis, 2020-12-29 to
  2021-08-31", etc.).

### E5 — advisory: the bins claim is unquantified, and "equal bins" is ambiguous

- **Where:**
  - block `outcomes.bins` (`docs/index.html:522`; `research_claims.py:1094`);
  - the bins caption (`build_pages.py:2323`);
  - the Explore item and h4 "All hours of the test periods, by forecast bin" (`build_pages.py:2134`, `:2425`).
- **Quoted:** "Over every scored hour of those test periods inside the eligible days, … grouped into ten equal bins by
  v6's median forecast, the mean observed price follows the mean forecast in every bin".
- **Is it fair, given `bins.csv`?** Broadly yes: the mean observed price rises with the mean forecast in every bin.
  - The absolute gaps are all within 6.0 EUR/MWh: the forecast is 6.0 high in bin 10, 4.8 in bin 9 and 4.6 in bin 2
    (48.0 against 43.4, about 10%).
  - In bin 1 the observed price is 3.1 against 1.3 forecast.
  - "Follows" sets no criterion. A careful reader may take it as "calibrated in every bin".
  - The comparison also has limits: no uncertainty is given, and the mean of a median forecast against the mean price
    does not test the median's calibration.
- **Further problems:**
  - "ten equal bins" can be read as equal-width bins. The table shows ranges from about 12 EUR/MWh (bin 6) to 446
    (bin 10).
  - "those test periods" refers back three headings, and has no antecedent when a reader arrives through the route.
- **Fix:**
  - "Over every scored hour of v5's test periods that falls on an eligible development day, 8,587 hours on 358 days,
    sorted by v6's median forecast into ten bins of equal size, the mean observed price rises with the mean forecast
    from bin to bin and stays close to it, the largest gap in the top bin: 516.9 EUR/MWh forecast against 510.9
    observed. The share of hours inside the 80% interval runs from 0.6868 to 0.8685 across the bins." This uses
    `pres6.bin.10.mean_p50` and `pres6.bin.10.mean_observed`.
  - Caption: "ten bins of equal size".
  - Route and h4: "All hours of v5's test periods, by forecast bin".

### E6 — advisory: the explanation's figures do not name their metric, and the method is jargon

- **Where:** blocks `outcomes.explanation` and `outcomes.explanation.drawn` (`docs/index.html:514`, `:516`;
  `research_claims.py:1115`, `:1125`).
- **Quoted:**
  - "moved the median most: on average 14.0 and 14.4 EUR/MWh an hour on the first day, 43.7 and 30.8 on the second";
  - "Prices two days before … moved the median by 2.7 EUR/MWh an hour";
  - "the probe that measured its in-browser retraining: exact baseline Shapley …";
  - "Its fits are v6's stored forecasts".
- **Why it matters:**
  - The figures are mean absolute contributions, but the prose never says "absolute".
  - The signed table directly below shows −13.7 for the same group, and +2.0 where the prose says "moved … by 2.7". A
    reader will take 2.7 as a net shift.
  - That is A1's concern: the metric is not beside the value.
  - "Exact baseline Shapley" is undefined at first use (§2). "The probe that measured its in-browser retraining" is
    process history. "Its fits" has no clear antecedent.
- **Fix:**
  - `outcomes.explanation`: "Which inputs moved v6's median on two development days: 2026-03-29, the spring clock-change
    day (23 hours), and 2026-09-06, the last development day. The attribution was computed and committed before the
    freeze, in a study of v6's in-browser retraining, as exact baseline Shapley values: each input group's share of the
    step from the networks' training-mean forecast to the issued median. The models it explains reproduce v6's stored
    forecasts for both days, quantile for quantile. On both days the load forecast for the delivery day and the weather
    forecast contributed most, with mean absolute contributions of 14.0 and 14.4 EUR/MWh an hour on the first day, and
    43.7 and 30.8 on the second."
  - `.drawn`: "… Prices two days before, used on the last day only, had a mean absolute contribution of 2.7 EUR/MWh an
    hour; …"

### E7 — advisory: Business insights' "average day", tense and unevaluated advice

- **Where:**
  - block `business.measured` (`docs/index.html:531`; `research_claims.py:1134`; `README.md:25`);
  - block `business.gap` (`:1139`).
- **Quoted:**
  - "On an average development day the median misses the hourly price by 17.2 EUR/MWh … an 80% interval about 51.7
    EUR/MWh wide held 0.7826 of the hours. A decision that uses the forecast can size its margin to that spread."
  - "…and no curve of either."
- **Why it matters:**
  - **"Average day".** 17.2 is the mean of the daily errors, not the error of a typical day. The median day's MAE in
    `daily-losses.parquet` (A1) is 12.6.
  - **Tense.** The present tense "misses" generalizes beyond the development period. The neighbouring verbs are past
    tense ("held", "was").
  - **"About".** "About 51.7" hedges a one-decimal mean.
  - **The advice.** "can size its margin to that spread" is prescriptive and unevaluated. The 80% intervals held 0.7826
    overall, and 0.7531 at a mean width of 87.8 in the crisis. Sizing to the average spread is the kind of decision the
    next paragraph says was never evaluated. That edges toward §5.1a's "do not … imply gains".
  - **"Either".** It is used for three nouns.
- **Fix:**
  - `business.measured`: "**What the results imply for that use.** Averaged over the development days, the median
    forecast missed the hourly price by 17.2 EUR/MWh, against the naive's 34.6, and by 30.7 in the 2021–2022 crisis; its
    80% intervals, 51.7 EUR/MWh wide on average, held 0.7826 of the hours, a little less than their nominal level. A
    decision built on the forecast must allow for misses of that size, larger in a crisis; how to size that allowance
    has not been evaluated."
  - `business.gap`: "…no profit, value or loss figure, and no curve of any of them."
  - Optionally, a route to `#outcomes`, since A8 asks that business conclusions "cite those results".

### E8 — advisory: confidence intervals and prediction intervals share one word

- **Where:**
  - the Explore item and h4 "Error by regime, with intervals" (`build_pages.py:2131`, `:2402`);
  - `outcomes.regimes`, "each interval below one";
  - `outcomes.finding`, "its 80% intervals", beside "[15.4, 19.1]";
  - `outcomes.coverage` and `outcomes.days`, "intervals".
- **Why it matters:** §3.2: "Intervals of estimated differences and forecast intervals must have distinct labels."
  - The caveat does call the brackets "95% confidence intervals of the mean".
  - Elsewhere, bare "interval(s)" means each kind in turn, sometimes in adjacent lines.
  - The opening's legend already says "80% prediction interval".
- **Fix:**
  - Route and h4: "Error by regime, with 95% confidence intervals".
  - `outcomes.regimes`: "each 95% confidence interval below one".
  - Use "prediction intervals" in `outcomes.coverage`, `outcomes.days` and, if A2 allows, `outcomes.finding`.

### E9 — advisory: the regimes paragraph — undated "crisis", "a fraction", "thin"

- **Where:** block `outcomes.regimes` (`docs/index.html:502`; `research_claims.py:1102`); also `business.measured`'s
  "in the crisis".
- **Quoted:** "246 days before the crisis, 481 in it and 1,341 from 2023; none is thin. In each, v6's mean daily point
  error is a fraction of the naive's, its ratio 0.4508, 0.4934 and 0.5047, each interval below one; the crisis carries
  the largest errors, 30.7 EUR/MWh in point error."
- **Why it matters:**
  - **The crisis is never dated in Product results.** That matters because topics 5 and 8 and the comparison call v5's
    third test period "the 2022 crisis period", at 43.2 EUR/MWh. Topic 8's new route sends the reader straight from that
    43.2 to this 30.7, with "crisis" naming both.
  - **"A fraction of" usually means a small part.** The ratios are about one half.
  - **"Thin" is never defined.**
- **Fix:** "246 days before the crisis (2020-12-29 to 2021-08-31), 481 in it (2021-09-01 to 2022-12-31) and 1,341 from
  2023-01-01; each has at least 60 days, so none is too thin to report. In each, v6's mean daily point error is about
  half the naive's: ratios of 0.4508, 0.4934 and 0.5047, each 95% confidence interval below one. The crisis carries the
  largest errors, 30.7 EUR/MWh in point error over the whole regime."

### E10 — advisory: the coverage paragraph leaves out an adverse fact and the missing comparator

- **Where:** block `outcomes.coverage` (`docs/index.html:508`; `research_claims.py:1108`).
- **Quoted:** "…covered 0.4779, 0.7826 and 0.9437 of the hours, at mean widths of 25.5, 51.7 and 88.8 EUR/MWh. … The
  nominal level is a reference, not a target."
- **Why it matters:**
  - Every level covers a little less than its nominal level. The page leaves the reader to notice; §5.1 subject 11 says
    retain adverse facts.
  - The naive's coverage is absent, but the page never says why (packet §10.3 item 3).
- **Fix:** "…covered 0.4779, 0.7826 and 0.9437 of the hours, each a little below its nominal level, at mean widths of …
  The naive's coverage is not in the committed rows, so none is shown."

### E11 — advisory: an evidence link's label promises more than its target

- **Where:** the `#outcomes` evidence row (`docs/index.html:525`; `build_pages.py:2368`).
- **Quoted:** "Daily, regime and coverage results, frozen 2026-11-14", which links to `regimes.csv` only.
- **Why it matters:**
  - The coverage rows are in `coverage.csv` and the daily-to-monthly rows in `monthly.csv`.
  - `bins.csv` and `summary.json` (the populations, the chosen days and the bootstrap settings) have no link at all.
  - §6 and A5: "The link says what the reader will see."
- **Fix (byte-neutral):** relabel the link "All product-result rows, frozen 2026-11-14" and point it at
  `tree/evidence/pres-6/reports/pres6/product-results`. Alternatively, relabel it "Regime means with their intervals"
  and add links for `coverage.csv`, `monthly.csv` and `bins.csv` if the budget allows.

### E12 — advisory: two terms are first used without a definition

- **Where:** `outcomes.finding` (`docs/index.html:484`) and `README.md:23`. A8 moved Product results ahead of the
  comparison.
- **Terms:**
  - **"the similar-day naive".** The reading path never says what it is; the comparison's terms say only "a simple naive
    forecast".
  - **"eligible" development days.** Never defined. The opening says "all 2,068 development days" for the same days.
- **Why it matters:** §2: "Define a term at first use".
- **Fix:** define both once, at the finding or in `outcomes.caveat`:
  - "the similar-day naive (the same hour's price from the day before, or from a week before for Mondays and weekends)".
    Confirm this against B0's definition, `src/delu_forecast/baselines.py::SIMILAR_DAY_LAG_BY_WEEKDAY`.
  - Define "eligible" by CP-26's definition. The 728-day fitting window before each day explains the 2020-12-29 start.
    Otherwise use the opening's "all 2,068 development days" throughout.

### E13 — advisory: the three-day panels use different price scales without saying so

- **Where:** `#outcomes-days-chart` (`docs/index.html:493`) and block `outcomes.days`.
- **Why it matters:**
  - The y-axes run 60–120, 0–400 and 0–200 EUR/MWh, and the first starts at 60.
  - The bands look similar in width, while the crisis day's are many times wider in EUR/MWh.
  - §6: "Comparable panels share scales". If separate scales are kept deliberately, they must at least be stated.
- **Fix:** add to `outcomes.days`: "Each panel has its own price scale."

### E14 — advisory: topic 6's rewritten body repeats itself and drops the scope words

- **Where:** block `v6.product.attribution` (`docs/index.html:477`, inside `#product-manual`; `research_claims.py:1007`).
- **Quoted:** "On two development days, in Product results. An attribution of v6's issued median by input group,
  committed before the freeze, is drawn for two development days."
- **Why it matters:**
  - "Two development days" appears twice.
  - The new sentence omits "within one fitted model" and "not how it behaves on other days", which the ruling wants on
    the label. Only the live-product sentence keeps "never what caused".
- **Fix:** "**Drawn in Product results for two development days.** An attribution of v6's issued median by input group,
  within each day's fitted model, committed before the freeze: not a cause, and not how it behaves on other days. The
  live product's Explainability view …" Keep the rest unchanged.

### E15 — advisory: the README's route to Product results leaves out the explanation

- **Where:** `README.md:23`.
- **Quoted:** "[Read them in the report](…#outcomes): forecast against the observed price, error over time and by regime,
  and interval coverage with width."
- **Fix:** "…error over time and by regime, interval coverage with width, and which inputs moved its median on two
  development days."

### E16 — advisory: Business "Limits" — "from 2026-12-04" and an awkward predicate

- **Where:** block `business.limits` (`docs/index.html:533`; `research_claims.py:1143`; `README.md:25`).
- **Quoted:** "4.7T, from 2026-12-04, is v6's one test on new data, and the live record on the Space is prospective
  evaluation in progress."
- **Why it matters:**
  - The anchor's term is "opens no earlier than 2026-12-04". The README's own 4.7T paragraph says "opening no earlier
    than 2026-12-04".
  - "From 2026-12-04" can be read as the test's data starting then. The window is 2026-09-07 to 2026-12-05.
  - This wording copies PRES-5's `v6.product.limits`.
  - "The live record … is prospective evaluation in progress" is a category error.
- **Fix:** "**Limits.** These are development results after selection. 4.7T, which opens no earlier than 2026-12-04, is
  v6's one test on new data; the Space shows the live record, prospective evaluation in progress."

### E17 — advisory: some extreme and rank claims are fixed in the templates, not derived

- **Where:** `research_claims.py`:
  - `outcomes.bins`: "from `{r:pres6.bin.2.inside80}` to `{r:pres6.bin.5.inside80}`", fixed bin indices;
  - `outcomes.explanation`: load and weather "moved the median most";
  - `outcomes.coverage`: "covered least … and were widest";
  - `outcomes.time`: "both peak in the crisis months".
- **Why it matters:**
  - All four are true at this commit (check 9).
  - `test_51` guards the bins' minimum and maximum and the every-month claim. Nothing guards the peak, least-and-widest
    or top-two claims.
  - A regenerated row would leave these sentences silently wrong (§3.4: derived, never typed).
- **Fix:** derive the minimum and maximum bin, and the top two groups, as records. Alternatively, add `test_51`
  assertions for each claim. No page change.

---

**Summary:**
- **Four violations:**
  - E1: the explanation's "What drives its forecasts" headings;
  - E2: no graphic visibly names its own artifact, and most omit their evidence class and dates;
  - E3: coverage without width in the product finding and README, which differs from P68;
  - E4: the regime values table has no unit.
- **Thirteen advisories,** E5–E17, all wording, labelling or provenance robustness. The bins claim is broadly fair on
  `bins.csv` but should be quantified (E5).
- **No number differs from its committed row,** and no evidence-class breach or W54/W55 breach was found.
- **Budget:** the fixes must fit the 2,405-byte margin and be re-checked under A2 on phones.
