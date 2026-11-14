# PRES-6 publication packet

**PUBLISH_RULES 1.5 §11 and A8 (triggered, ruling O46); the brief `docs/track-b/evidence/pres-6/issued-brief.md` (SHA-256
`bdb78f02894896d2ee1f249355d23351f972cdb217d4d906d22561172f40e5f6`); the packet template
`docs/track-b/publication-packet-template.md` (`4049c3e1…d01a`).** This section, §0, was committed before any product
result was computed; the rest of the packet follows the template once the results exist.

## §0. Rules fixed before the computation (the brief's outcome 2)

Everything below is decided before any of the numbers it governs is computed or drawn. Nothing is fitted; no other
policy is recomputed. Every value the page shows is derived from committed rows and re-derived by a `--check`.

**The policy and its artifacts.** v6 (A1 in the frozen records; policy `720fc581…`), as CP-28 stored it:
- forecasts: `reports/cp28/forecast/hourly.parquet` (`f5cb02a1…f638`), arm `A1`;
- daily losses: `reports/cp28/results/daily-losses.parquet` (`7e9c972f…b85d`), stream `A1`, with the similar-day naive
  as the reference (stream `B0`);
- observed prices: CP-24's committed rows `reports/ddnn2/attempt-1/predictions.parquet` (`9d3f539f…5cf9`), column
  `y_true`, joined to v6's stored quantiles by delivery hour exactly as PRES-5's `final_candidate.py` joins them.

**The populations.**
- **P-all:** every eligible development day, 2020-12-29 to 2026-09-06, 2,068 days, 49,596 scored hours: the days CP-26
  scored and CP-28 selected on. Every daily figure comes from `daily-losses.parquet`; none is recomputed from hours.
- **P-v5:** the subset of P-all inside v5's five test periods: folds 2–5, 358 days (2021-04-01 to 2021-06-29,
  2022-07-01 to 2022-09-28, 2025-05-01 to 2025-07-29, 2026-01-08 to 2026-04-07), where committed hourly observed prices
  exist. Fold 1 (2020) lies before P-all and is left out.

**The regimes** (§5.1 subject 2, as the page already states them): pre-crisis, 2020-12-29 to 2021-08-31 (246 days of
P-all); the energy crisis, 2021-09-01 to 2022-12-31 (481); the market with frequent negative prices, 2023-01-01 to
2026-09-06 (1,341).

**Forecast against observed.**
- **Days, chosen by a rule:** for each regime, among the days of P-v5 in that regime, the day whose v6 daily MAE
  (from `daily-losses.parquet`) is the regime's median, taking the lower of the two middle days when the count is even.
  One day per regime, three in all. Each is drawn as v6's median with its 50%, 80% and 95% intervals against the
  cleared price, in EUR/MWh, by local hour.
- **The whole-population view:** every scored hour of P-v5, grouped into ten bins of equal count by v6's median
  forecast. For each bin: the mean median forecast, the mean observed price, the number of hours and the share of
  hours inside the 80% interval.

**Error over time.** The daily MAE and the daily interval score (WIS, the committed definition) of v6 and of the naive
on every day of P-all, drawn as their calendar-month means; every day counts once, no smoothing. The daily rows stay
in the committed output.

**Error by regime.** For each regime and for P-all: the number of days and scored hours; the mean daily MAE and WIS of
v6 and of the naive; and v6's ratio to the naive. 95% intervals from a non-circular moving-block bootstrap over the
regime's days, blocks of 14 consecutive days, 2,000 replicates, seed 20261114, resampling v6 and the naive on the same
days (the ratio's interval from the same draws). A regime with fewer than 60 days would be stated as thin; none is.

**Coverage with width.** For each nominal level, 50%, 80% and 95%, for P-all and for each regime, for v6 and for the
naive: coverage, the scored-hour-weighted share of hours inside the interval, and width, the scored-hour-weighted mean
interval width in EUR/MWh, both from `daily-losses.parquet`. The nominal level is drawn as a reference, never as a
target.
- *Correction, 2026-11-14, before any number was computed:* `daily-losses.parquet` carries coverage and width for the
  arms only; the naive's and the control's rows hold MAE and WIS alone. Coverage with width is therefore reported for
  v6 only, at each level, for P-all and for each regime. The naive's would need its hourly quantiles and the observed
  prices on P-all, which are not committed; it is not computed.

**Explanation or sensitivity.** No committed explanation of v6 exists. CP-28's stored `networks.npz` and
`features.parquet` belong to the small-network blend arms (A5, A7): their inputs are member error statistics and their
outputs are blend weights, so they cannot explain v6, which is DDNN-2 alone. The source and method are the subject of
an Orchestrator ruling requested on 2026-11-14 (proposed: the frozen §19.7 method, exact baseline Shapley over the 11
input groups on the issued median, by inference only, from CP-18b's committed A1 artifact for development day
2026-09-05). Until that ruling and its own pre-registration here, nothing is computed; if neither fits, the section
states the gap.
- *Correction, 2026-11-14, before any explanation was drawn or summarized:* **a committed explanation of v6 exists**,
  and the sentence "No committed explanation of v6 exists" above is wrong. CP-17-probe's native reference
  `reports/cp17-probe/native-reference.json` (`f1decb80…96ab`, committed in `42e27c70`, under `evidence/cp-17`) holds
  the §19.7 attribution of A1's fits for two development days. Its method is exact baseline Shapley over the input
  groups that day's members use, on the issued median, against each member's training-row mean:
  - 2026-03-29, the spring DST day: 23 delivered hours, 9 groups, 512 coalitions;
  - 2026-09-06: 24 hours, 10 groups, 1,024 coalitions.

  **Those fits are v6's stored forecasts:** their quantiles equal CP-28's `hourly.parquet` arm A1 rows for both days
  exactly (largest absolute difference 0). By the brief's first branch ("use an existing committed result for v6"),
  the section shows that result. **Nothing is computed by inference, and the ruling requested above is moot.**

  **The display rules, fixed now:**
  - **The source:** for each of the two days, the result's `attribution` (`players`, `phi_eur`, `baseline_p50`,
    `full_p50`).
  - **Delivered hours only:** a model slot counts when its `full_p50` equals the day's issued median (`central`)
    within 1e-9, matched in order. On 2026-03-29 that drops slot 2, local 02:00, which does not exist that day.
  - **Per day and input group, in EUR/MWh:** the mean over the delivered hours of the contribution, signed, and of its
    absolute value. Also the day's mean baseline median and mean issued median, which the signed means bridge
    exactly (the attribution's efficiency).
  - **The groups** in the frozen order (`cp17.attribution.GROUPS`). A group the day's members do not use is shown
    as such, never as zero.
  - **Drawn:** each day's mean absolute contribution by group, the same reading as the live product's Features view.
    The signed means and the bridge go in a values table.
  - **Wording:** attribution within one fitted artifact, relative to its stated baseline; never causality or
    incremental value (§19.7). Two days are not the population, and the section says so.

**Evidence class.** Development, post-selection on every figure: v6 was selected on P-all (CP-28). Nothing
prospective: the report shows no live forecast, score or price, and says that the Space shows the live record,
"prospective evaluation in progress".

---

The sections below follow the packet template. They were written after the results existed. Values marked
`<final_…>` are the final build's and the evidence tip's, and the return gives them filled in.

## 1. Identity

| Item | Value |
|---|---|
| Checkpoint | PRES-6, brief `docs/track-b/evidence/pres-6/issued-brief.md` at `bdb78f02894896d2ee1f249355d23351f972cdb217d4d906d22561172f40e5f6` (the first commit, `405e588c`, byte for byte) |
| Governing rules and plan | PUBLISH_RULES 1.5 (`1bc0c523…f94e`), A8 triggered by ruling O46; research v21-r20 §24.14 (what may be published now, on development data only) |
| Evidence tag and tip | `evidence/pres-6` at `<evidence_tip_sha>`, frozen `<final_date>` (`registry.EVIDENCE_TAGS["evidence/pres-6"]`, set in the final-build commit) |
| Final reviewed candidate | `<final_candidate_sha>`: the `--final` build of the page and README |
| Report, review verdict, landing record | this packet; `docs/track-b/evidence/pres-6/integration.md` (the Integration verdict at the candidate) and the focused recheck at the final SHA; the landing record is the Orchestrator's |

## 2. The registry entries (standard §5)

**None is added or changed.** PRES-6 evaluates no new identity. v6's entry (`v6`, A1 in the frozen records, policy
`720fc581…`) stands as PRES-5 entered it, status "final candidate · pending 4.7T" (O13). The similar-day naive is the
existing reference `B0`. The one registry change is the evidence tag `evidence/pres-6`, which dates the product
results' rows on the page.

## 3. The claim map

`docs/track-b/research-content/pres6-claims.md`: C1001–C1007 (the product results), P67–P71 (the order, the finding,
the graphics' identity, Business insights, R1–R7) and the withheld claims W54 (no error or coverage figure is a
profit or a success rate; no profit curve) and W55 (no product result is prospective). Both are in
`research_claims.WITHHELD_PATTERNS`, each with positive and negative tests
(`tests/test_51_pres6_product_results.py::test_the_withheld_claims_w54_and_w55_are_guarded`).

## 4. The derived headline quantities (standard §3.3)

**The report's headline is unchanged:** PRES-5's (P60), v6 against v5 on all 2,068 development days, −7% and −11%,
7 policies tested. PRES-6 adds no decision and no rule. The product finding (A2's bound under A8) reads these
records:

| Quantity | Value | Record (`reports/pres6/product-results/`) |
|---|---|---|
| (a) A pre-specified verdict | none: these are descriptions of the selected policy, not a test | — |
| Population | 2,068 eligible development days, 49,596 scored hours, 2020-12-29 to 2026-09-06 | `pres6.p_all.days`, `pres6.p_all.hours` (`summary.json`) |
| v6's mean daily point error | 17.19 EUR/MWh [15.45, 19.09] | `pres6.regime.all.MAE.v6` (`regimes.csv`) |
| The naive's | 34.55 [31.09, 38.26] | `pres6.regime.all.MAE.naive` |
| (b) v6 as a share of the naive's error | 0.4974 [0.4734, 0.5230] point; 0.4580 [0.4353, 0.4821] interval score | `pres6.regime.all.{MAE,WIS}.ratio` |
| Its 95% interval | the paired non-circular moving-block bootstrap of §0: 14-day blocks, 2,000 replicates, seed 20261114, order all, pre_crisis, crisis, negative_prices | `summary.json` `bootstrap` |
| (c) By regime, point error | before the crisis 6.25, in it 30.67, from 2023 14.36 EUR/MWh | `pres6.regime.{regime}.MAE.v6` |
| 80% coverage with width | 0.7826 of the hours, mean width 51.7 EUR/MWh | `pres6.coverage.all.80.{coverage,width_eur}` (`coverage.csv`) |

**The populations agree with CP-26's and CP-28's.** v6's and the naive's P-all means equal CP-26's every-day records
for DDNN-2 (`cp26.every.nominal.D2.all_eligible.*.raw_mean_daily_loss`) and the naive (`…B0…`) within 1e-9, on
both scores. The three regimes sum to the 2,068 days and the 49,596 hours
(`test_51::test_the_populations_agree_with_cp26_and_cp28`).

## 5. Slot texts, as rendered (standard §6)

There is no chapter grammar: Product results and Business insights are product sections (§5.1a). Each block is a
claim template in `research_claims.PRES6_BLOCKS`, rendered on the page and, where marked, in the README:

| Block | Claim | Text (README form) |
|---|---|---|
| `everyday.question` | P71 | Do the five-period results hold when every eligible day is scored under one daily protocol? |
| `outcomes.sub` | P69 | v6 · DDNN-2 alone (A1 in the frozen records), its forecasts as the selection stored them · every eligible development day, 2020-12-29 to 2026-09-06 · EUR/MWh · development, post-selection |
| `outcomes.finding` | P68 | On all 2,068 eligible development days, v6's mean daily point error was 17.2 EUR/MWh [15.4, 19.1] against the similar-day naive's 34.6; its 80% intervals covered 0.7826 of the hours. |
| `outcomes.caveat` | C1001 | Development evidence after selection: v6 was chosen on these days. The brackets are 95% confidence intervals of the mean, from 14-day block resamples. The live record is on the Space, prospective evaluation in progress. |
| `outcomes.days` | C1005 | Three development days, one per regime, each the day at its regime's median point error within v5's test periods, a rule fixed before any was drawn: 2021-06-16, 2022-07-26 and 2025-05-02. The line is v6's median forecast; the bands its 50%, 80% and 95% intervals; the dashes the price that cleared. |
| `outcomes.bins` | C1006 | Over every scored hour of those test periods inside the eligible days, 8,587 hours on 358 days, grouped into ten equal bins by v6's median forecast, the mean observed price follows the mean forecast in every bin; the share of hours inside the 80% interval runs from 0.6868 to 0.8685 across the bins. |
| `outcomes.time` | C1004 | Each day's point error and interval score, as calendar-month means from 2020-12 to 2026-09: v6 lies below the similar-day naive in every month on both scores, and both peak in the crisis months. |
| `outcomes.regimes` | C1002 | 246 days before the crisis, 481 in it and 1,341 from 2023; none is thin. In each, v6's mean daily point error is a fraction of the naive's, its ratio 0.4508, 0.4934 and 0.5047, each interval below one; the crisis carries the largest errors, 30.7 EUR/MWh in point error. |
| `outcomes.coverage` | C1003 | Over the eligible days, v6's 50%, 80% and 95% intervals covered 0.4779, 0.7826 and 0.9437 of the hours, at mean widths of 25.5, 51.7 and 88.8 EUR/MWh. In the crisis they covered least, 0.7531 at 80%, and were widest. The nominal level is a reference, not a target. |
| `outcomes.explanation` | C1007 | Which inputs moved v6's median on two development days: 2026-03-29, the spring clock-change day (23 hours), and 2026-09-06, the last development day. The attribution is the one committed, before the freeze, by the probe that measured its in-browser retraining: exact baseline Shapley over the input groups that day's networks use. Its fits are v6's stored forecasts for both days, quantile for quantile. On both days the load forecast for the delivery day and the weather forecast moved the median most: on average 14.0 and 14.4 EUR/MWh an hour on the first day, 43.7 and 30.8 on the second. |
| `outcomes.explanation.drawn` | C1007 | Drawn: the nine groups both days' networks use. Prices two days before, used on the last day only, moved the median by 2.7 EUR/MWh an hour; the holidays, day type and month group is used on neither day. |
| `outcomes.explanation.terms` | C1007 | Each value attributes that day's issued median within one fitted model, relative to its networks' training-mean baseline. It is not a cause, not the value an input adds, and not how the model behaves on other days; two days are not the development period. |
| `business.use` | P70 | **The intended use.** An hourly price forecast for the next delivery day, with intervals, issued before the 12:00 auction: an input to bidding, scheduling and hedging decisions in the German–Luxembourg market. |
| `business.measured` | P70 | **What the results imply for that use.** On an average development day the median misses the hourly price by 17.2 EUR/MWh, against the naive's 34.6, and by 30.7 in the crisis; an 80% interval about 51.7 EUR/MWh wide held 0.7826 of the hours. A decision that uses the forecast can size its margin to that spread. |
| `business.gap` | P70 | **What is not established.** No decision policy, cost model or trading simulation has been authorized or run for this product, so there is no profit, value or loss figure, and no curve of either. Lower forecast error and interval coverage are not profit, and not a success rate of any decision. |
| `business.limits` | P70 | **Limits.** These are development results after selection; 4.7T, from 2026-12-04, is v6's one test on new data, and the live record on the Space is prospective evaluation in progress. |

### 5a. The adopted transition (A3)

None: no generation is adopted. The "From v5 to v6" summary stands as PRES-5 published it.

### 5b. The product's documentation (A4, under A8)

The product is unchanged: v6, which the Space runs (O26, O29). "How the product works" keeps PRES-5's twelve subjects.
A8 makes the three product sections complement each other ("method explanations link to the canonical result
graphics"), so five topics gain a route to Product results. Each keeps its earlier route:

| Subject (§5.1) | Disposition | Evidence | Routes |
|---|---|---|---|
| 1 Data and the information cutoff | supported | unchanged (PRES-5) | `#product-data` |
| 2 Regimes and negative prices | supported | unchanged; **+** v6's error in each regime | `#product-regimes` → `#outcomes-regimes` |
| 3 Inputs; 3b seasonal rationale | supported | unchanged | `#product-inputs` |
| 4 Validation | supported | unchanged | `#product-validation` |
| 5 Results | supported | unchanged; **+** Product results, every development day | `#product-results` → `#outcomes`, `#v6-chart-title` |
| 6 Attribution | **supported, on two development days** (was "not evaluated in research") | `v6.product.attribution` rewritten: CP-17-probe's committed attribution of v6's stored fits, drawn in Product results (§0's correction; C1007) | `#product-attribution` → `#outcomes-explanation`, the Space's Explainability view |
| 7 Importance and sensitivity | not evaluated in research | unchanged | `#product-importance` → the Space's Features view |
| 8 Where it fails | supported | unchanged; **+** the month-by-month error | `#product-failures` → `#outcomes-time`, `#v6-per-period-differences` |
| 9 Reliability | supported | unchanged; **+** coverage with width at each level, every development day | `#product-reliability` → `#outcomes-coverage`, `#v6-coverage` |
| 10 Read a forecast | supported, on the live product | unchanged | `#product-forecast` |
| 11 Limitations | supported | unchanged | `#product-limitations` |
| 12 Running it | supported | unchanged | `#product-run` |

The incoming and outgoing product are both v6: no transition. v1's documentation stays where PRES-5 left it.

### 5c. The chart routes (A5)

| Chart | Its heading | The route | Where it starts |
|---|---|---|---|
| `outcomes-days-chart` | `#outcomes-days` | "Forecast against the observed price on three development days" | Product results' "Explore these results" |
| `outcomes-time-chart` | `#outcomes-time` | "Error over time, month by month" | the same; product topic 8 |
| `outcomes-regimes-chart` | `#outcomes-regimes` | "Error by regime, with intervals" | the same; product topic 2 |
| `outcomes-coverage-chart` | `#outcomes-coverage` | "Interval coverage with width" | the same; product topic 9 |
| `outcomes-explanation-chart` | `#outcomes-explanation` | "What drives its forecasts" | the same; product topic 6 |
| (table) | `#outcomes-bins-h` | "All hours of the test periods, by forecast bin" | the same |

Each chart has one heading and one canonical place, in Product results. Business insights draws no chart and cites the
results in words (A8: "without duplicating full charts").

### 5d. Final-product transition / daily operation (A7/A8/A9)

| Field | State |
|---|---|
| Owner designation and lifecycle | unchanged: v6 (A1) selected 2026-10-25, frozen 2026-10-30, live through CP-18c; "final candidate · pending 4.7T" (O13, O27) |
| One product identity | the opening, How the product works, Product results, Business insights, the README and the Space name v6; Product results names its artifact (CP-28's stored forecasts, arm A1) and policy |
| Frozen policy, daily training and issuance, coverage, today, scores, reliability | CP-17c's freeze and CP-18c's live pipeline, not this block's. The report shows no live number and says the Space shows the live record, "prospective evaluation in progress" |
| Page order | **A8's, now (O46):** compact navigation → the product and daily-forecast opening → How the product works → **Product results** → **Business insights** → How the models compare → the rest in their existing order (`test_51::test_the_order_is_a8s_product_first`) |
| A2 placement | the product finding `#product-finding` (§7, the browser matrix) |
| Product coverage and science | §5b; development results only, labelled post-selection; nothing unused-data or prospective |
| Business evidence | **not evaluated, and the gap stated:** the intended use and the measured forecasting implications only. No decision policy, cost model, capital or trading simulation exists, so there is no net-value series, profit curve or business rate |
| Acceptance | this packet's §7 and §9; the Integration check at the candidate and the recheck at the final SHA |
| Prospective state | in progress since CP-18c's first live day; nothing prospective is published here |

## 6. The MLflow export

**No run changes and nothing is uploaded.** The export's 105 runs and its experiment tags are byte-identical to the
published set. `manifest.json` changes only in its `sources` list, which gains the six PRES-6 files with the
`evidence/pres-6` tag: that list is a local record, and `scripts/verify_mlflow_mirror.py::verify` reads the runs and the
experiment tags, not the sources. No route changes, so `reports/presentation/mlflow_index.json` is unchanged.

## 7. Checks the checkpoint ran

| Check | Result | Record |
|---|---|---|
| The product results re-derive byte for byte from the four pinned inputs (`final_candidate --product --check`); a changed input is refused | pass | `tests/test_51` (`test_the_product_rows_rederive_byte_for_byte`, `test_a_changed_input_is_refused`) |
| The populations agree with CP-26's and CP-28's (2,068 days, 49,596 hours; v6's and the naive's means equal CP-26's D2 and B0 records within 1e-9) | pass | `test_51::test_the_populations_agree_with_cp26_and_cp28` |
| The three days are the rule's, re-chosen independently; the upper median would choose another day (the rule is not vacuous) | pass | `test_51::test_the_three_days_are_the_rules` |
| Every PRES-6 record re-derives (453 records); a perturbed value fails; no record describes a day after 2026-09-06 | pass | `test_51::test_every_pres6_record_rederives_and_a_perturbed_one_fails` |
| The explanation is the probe's committed result, its fits v6's stored forecasts (the probe's quantiles equal CP-28's A1 rows, both days); the bridge holds; each mark sits on its own group's row (negative control: the first draft's misaligned panels) | pass | `test_51` (four explanation tests) |
| A8's order; the navigation leads to Product results; the PRES-5 order is caught | pass | `test_51::test_the_order_is_a8s_product_first` |
| Product results and Business insights bind only PRES-6 records and show no unrounded value; the pre-fix page (v1's stratum table under a name clash) fails with 126 foreign values | pass | `test_51::test_product_results_binds_only_pres6_records_and_shows_no_live_number`, `…another_tables_values_are_caught` |
| W54 and W55, each with positive and negative cases, find nothing on the page or in the README | pass | `test_51::test_the_withheld_claims_w54_and_w55_are_guarded` |
| The link checker: the recorded `/history/` chain fails as a cross-host redirect; a same-host redirect passes and is recorded; a loop and a missing `Location` fail | pass | `tests/test_33` (fixture `tests/fixtures/pres6/recorded.json`) |
| The receipt: `normalize_space_page` is `cp18.publish.normalized`; the recorded served page passes after 495 bytes are removed; PRES-5's script-only rule, a changed page and an ambiguous second meta run fail | pass | `tests/test_48` |
| A2 under A8 (O48): the rule's arithmetic for the product finding, one pixel too low fails, an A4 page still checks the comparison's; in Chrome and WebKit the candidate passes, PRES-5's published page measures `#comparison-finding`, and a candidate with 900 px inserted above the product finding fails | pass | `tests/test_43` (A2 tests); `reports/presentation/release-checks/pres-6-placement-o48.json` |
| The presentation suites (tests 29–34, 38, 43, 50, 51) | 799 passed, 1 skipped at `9b60c88c` | local run |
| The prerelease in a clean worktree (runbook §9 offline checks) | `<prerelease result>` | `reports/presentation/release-checks/pres-6-pre-final-prerelease.json` |
| The browser release check over HTTP (Chrome and WebKit; 1440, 768, 390, 360, 320; iPhone 15 emulation; placements, accessibility, keyboard, contrast, charts, requests) | `<release result>` | `reports/presentation/release-checks/pres-6-local-release.json` |
| The page budget | `<final_page_bytes>` bytes ≤ 2,000,000 | `reports/cp3/pages_build.json` |

## 8. Publication completion receipt and the Orchestrator's packet

### 8.0 What would be published

| Surface | Reviewed output | Identity | Now public |
|---|---|---|---|
| Report, GitHub Pages | `docs/index.html` at `<final_candidate_sha>`, the `--final` build | `<final_page_sha256>`, `<final_page_bytes>` bytes | 1,848,955 bytes, `983a75c44b0f93dabd183ee810158aefbfa62adfb5545b4a433afe4b5bbb9475` (PRES-5 fix 1, `main` `50d51507`) |
| README | `README.md` at `<final_candidate_sha>` | `<final_readme_sha256>` | `bc98e9ccb74546a2d3fbdbbfabd8034bc63addfc165c0264598f1a1d3747c472` |
| Hugging Face Space and its card | **no PRES-6 action**: CP-18c's live product, published daily by the runner | the runner's latest publication (its `pipeline` artifact, §8.5) | revision `69c6ea3bebfc19bb2396679993f95b2b3fcbab40` at 2026-11-14 11:21 UTC; it moves with each daily run |
| MLflow `delu-generations` | **no PRES-6 action** (§6) | 105 runs, the committed export | 105 runs (PRES-5) |

### 8.1 Receipt — intended identities (the Orchestrator and the public checker complete the rest)

| Surface | Intended identity | Action / unchanged rationale | Observed public identity and UTC time | Verification record and result | Outstanding action |
|---|---|---|---|---|---|
| GitHub source / README | `land/pres-6` (the squash of `<evidence_tip_sha>` onto the moved `main`; PRES-6's paths equal the tip's); README `<final_readme_sha256>`, with the "Product results" and "Business insights" glance | push (§8.3) | to fill | `pres-6-publication-receipt.json` (GitHub main); the served README's hash (§8.5) | §8.2–8.3 |
| GitHub Pages | `<final_page_sha256>`: A8's order with Product results and Business insights before How the models compare | deploy by the push (§8.3) | to fill | `pres-6-publication-receipt.json` (Pages); `pres-6-public-report.json`; `pres-6-postdeploy-links.json` | §8.3, §8.5 |
| Public MLflow | unchanged: the committed export's 105 runs and experiment tags | verified unchanged (§6) | to fill | `pres-6-postdeploy-mlflow-mirror.json` | §8.5 |
| Hugging Face Space card | CP-18c's, as the runner last published it | **no PRES-6 action** | to fill | `pres-6-publication-receipt.json` (Space files) against the runner's `pipeline` build | §8.5 |
| Hugging Face direct demo | CP-18c's live product at the root; v1 at `history/index.html` | **no PRES-6 action** | to fill | `pres-6-publication-receipt.json` (direct page, by CP-18c's normalization); the report's Space links, each hop recorded, none ending on another host (`pres-6-postdeploy-links.json`) | §8.5 |

- **Publication-to-MLflow mapping:** unchanged: PRES-5's (`pres-5-public-mirror.json`, `mlflow_index.json`).
- **Final product and daily updates:** CP-18c's. The report carries no live record.
- **Completion disposition:** incomplete until these steps and their public checks pass; A12 is decided in §8.6.
- **Authority:** the landing, the push and the Pages deployment are the Orchestrator's, after the return (the
  brief's "Owner-only actions already authorized"; decisions 27 and 28). There is no Space or MLflow step.

Every command below runs from the primary checkout, `/Users/djourno/Downloads/PJM`. None opens a pager or an editor
(`git --no-pager`, `GH_PAGER=cat`). Substitute `<evidence_tip_sha>`, `<land_sha>`, `<final_page_sha256>`,
`<final_readme_sha256>` and `<final_date>` from the return, which gives these commands filled in. Keep every record a
step writes, first failures included.

### 8.2 Step 1 — the LAND, on a moved `main`

PRES-6 branched from `87811abc645b6d903dafaf7093452361e21aa193`. Since then `main` has moved by the Orchestrator's
`29b6431e` (`docs/track-b/cp-18c-landing-2026-11-13.md` only), and `origin/main` moves each day by the runner's
data-only commits (author `delu-daily`, `live/` only). PRES-6's paths (listed by the first command below) and those
are disjoint.

**No daily job may be running** (CP-18c's landing record, O47: a push during a run made the run discard its records).
Here and again before the push:

```bash
GH_PAGER=cat gh run list --workflow daily.yml --limit 6 --json databaseId,status,event,createdAt --jq '.[] | "\(.databaseId) \(.status) \(.event) \(.createdAt)"'
```

Expect every line `completed`. A `queued`, `in_progress` or `waiting` line: wait for it to finish. The scheduled jobs
start from 07:40 UTC; a run publishes until about 11:30 UTC.

```bash
git --no-pager rev-parse --abbrev-ref HEAD
```

Expect `main`.

```bash
git fetch origin && git --no-pager log --format='%h %an %s' main..origin/main && git --no-pager diff --name-only main origin/main | grep -v '^live/' ; echo only-live-checked
```

Expect only `delu-daily` commits and then only `only-live-checked`: nothing outside `live/` arrived. Any other path:
stop and read it first.

```bash
git merge --ff-only origin/main
```

Expect `Fast-forward` (or `Already up to date.`).

```bash
git --no-pager status --porcelain=v1
```

Expect no output (or only ` M progress.md`, the Orchestrator's own edit). Any other line: stop and resolve it first.

**PRES-6's paths, and no untracked twin:**

```bash
git --no-pager diff --name-only 87811abc645b6d903dafaf7093452361e21aa193 <evidence_tip_sha> > .local/artifacts/pres-6/pres6-paths.txt && wc -l < .local/artifacts/pres-6/pres6-paths.txt && grep -c '^live/' .local/artifacts/pres-6/pres6-paths.txt; while IFS= read -r f; do git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 && ! git --no-pager diff --quiet -- "$f" && echo "MODIFIED $f"; git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 || { [ -e "$f" ] && echo "TWIN $f"; }; done < .local/artifacts/pres-6/pres6-paths.txt; echo twins-checked
```

Expect the path count the return gives, then `0` (no `live/` path), then only `twins-checked`.

```bash
git --no-pager diff --name-only 87811abc645b6d903dafaf7093452361e21aa193 HEAD | grep -vxFf .local/artifacts/pres-6/pres6-paths.txt | grep -v '^live/' ; echo moved-main-checked
```

Expect only `docs/track-b/cp-18c-landing-2026-11-13.md` (and any later Orchestrator record), then
`moved-main-checked`. A path that is also in `pres6-paths.txt` would not be listed here, so this proves nothing about
overlap; the next check does.

```bash
git --no-pager diff --name-only 87811abc645b6d903dafaf7093452361e21aa193 HEAD | grep -xFf .local/artifacts/pres-6/pres6-paths.txt ; echo overlap-checked
```

Expect only `overlap-checked`: no path changed on both sides.

```bash
git --no-pager merge --squash gauntlet/pres-6
```

Expect `Squash commit -- not updating HEAD` and the diffstat, with no `CONFLICT` line.

**PRES-6's paths equal the evidence tip's, and every other path equals `main`'s:**

```bash
xargs git --no-pager diff --cached --quiet <evidence_tip_sha> -- < .local/artifacts/pres-6/pres6-paths.txt && test -z "$(git --no-pager diff --cached --name-only HEAD | grep -vxFf .local/artifacts/pres-6/pres6-paths.txt)" && echo STAGED-PRES6-PATHS-EQUAL-EVIDENCE-TIP
```

Expect only `STAGED-PRES6-PATHS-EQUAL-EVIDENCE-TIP`. If it does not print, stop: nothing is committed yet, and
`git reset --merge` restores the index.

**The evidence label's date equals the tip's:** the page labels the product results' rows "frozen <date>" from
`registry.py::EVIDENCE_TAGS["evidence/pres-6"]`.

```bash
git --no-pager log -1 --format=%cs <evidence_tip_sha> && git --no-pager show <evidence_tip_sha>:src/delu_forecast/registry.py | grep '"evidence/pres-6"'
```

Expect the same date on both lines (`<final_date>`). A different date: stop and report it.

```bash
git commit -F .local/artifacts/pres-6/land-commit-message.txt
```

Expect `[main <land_sha>] Publish PRES-6: …`. The hooks run and print nothing when clean.

```bash
git tag land/pres-6 HEAD
```

```bash
git tag evidence/pres-6 <evidence_tip_sha>
```

Both print nothing.

```bash
git --no-pager diff --stat HEAD <evidence_tip_sha> | tail -1
```

Expect only `main`'s own movement since `87811abc`: `docs/track-b/cp-18c-landing-2026-11-13.md` and the `live/` files.

### 8.3 Step 2 — the push

Re-run the first command of §8.2: no daily job may be running. Then **the value-based secret scan**, over exactly what
the push will send:

```bash
printf '%s %s %s %s\n' refs/heads/main "$(git rev-parse main)" refs/heads/main "$(git rev-parse origin/main)" refs/tags/land/pres-6 "$(git rev-parse land/pres-6)" refs/tags/land/pres-6 0000000000000000000000000000000000000000 refs/tags/evidence/pres-6 "$(git rev-parse evidence/pres-6)" refs/tags/evidence/pres-6 0000000000000000000000000000000000000000 | python3 scripts/secret_guard.py pre-push origin "$(git remote get-url origin)" && echo SECRET-SCAN-CLEAN
```

Expect `SECRET-SCAN-CLEAN`. A `secret-guard: BLOCKED` line means stop and tell no one the value.

```bash
python3 scripts/publication_guard.py tree
```

Expect a PASS line: the landed page is the final build.

```bash
git push origin main land/pres-6 evidence/pres-6
```

Expect `<old>..<first 7 of land_sha>  main -> main` and two `[new tag]` lines. **If the push is refused** because the
runner pushed in between (`fetch first`): never force, rebase or reset. Wait until no daily job runs, `git fetch
origin`, confirm with §8.2's command that the new commits touch only `live/`, merge them with `git merge --no-edit
origin/main` (data-only paths, so no conflict; the tags stay on the squash commit), and push again. GitHub Pages then
serves `docs/`. Read GitHub's CI for the pushed commit before the closure:

```bash
GH_PAGER=cat gh run list --branch main --limit 4
```

### 8.4 Step 3 — no Space upload and no MLflow write

PRES-6 changes nothing on Hugging Face or DagsHub. The Space is CP-18c's, published daily by the runner. If the served
Space is not what the runner's latest publication record names, that is CP-18c's to resolve; do not redeploy under
this packet.

### 8.5 Step 4 — the public checks, per surface

Each writes a new record; keep a first failure beside its retry. The Playwright commands need
`PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright`. Wait until Pages has deployed the
push:

```bash
curl -s https://hrsi56.github.io/delu-day-ahead-forecast/ | shasum -a 256
```

Expect `<final_page_sha256>` (now `983a75c4…9475`, PRES-5's).

```bash
curl -s https://raw.githubusercontent.com/hrsi56/delu-day-ahead-forecast/main/README.md | shasum -a 256
```

Expect `<final_readme_sha256>`.

**The Space's reviewed build is the runner's.** The receipt checks the Space's files and direct page against a local
build. The runner uploads its whole results folder, `space/` included, as the Actions artifact `pipeline` (30 days),
with its own hashes in `results-sha256.txt`. Fetch the latest successful run's (read-only), and check it against
those hashes:

```bash
RUN=$(GH_PAGER=cat gh run list --workflow daily.yml --status success --limit 1 --json databaseId --jq '.[0].databaseId') && echo "$RUN" && gh run download "$RUN" -n pipeline -D ".local/tmp/pres-6/runner-$RUN" && (cd ".local/tmp/pres-6/runner-$RUN" && shasum -a 256 -c results-sha256.txt --quiet) && echo RUNNER-BUILD-INTACT
```

Expect the run id and `RUNNER-BUILD-INTACT`.

**One served file is missing from the download by design:** before uploading, the runner deletes every
`*-arrays.npz` ("the fitted arrays deleted first"), and the Space serves `payloads/artifact-arrays.npz` (its
Explainability view needs it). Fetch that one file from the Space, anonymously, and check it, and every other file,
against the build's own record `app/space-build.json`:

```bash
B=".local/tmp/pres-6/runner-$RUN/space" && curl -sfL -o "$B/payloads/artifact-arrays.npz" https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/payloads/artifact-arrays.npz && python3 -c "import hashlib, json, os, sys; b = sys.argv[1]; files = json.load(open(os.path.join(b, 'app/space-build.json')))['files']; bad = [f['path'] for f in files if not os.path.isfile(os.path.join(b, f['path'])) or hashlib.sha256(open(os.path.join(b, f['path']), 'rb').read()).hexdigest() != f['sha256']]; print('BUILD-EQUALS-ITS-RECORD' if not bad else ('DIFFERS', bad[:5]))" "$B"
```

Expect `BUILD-EQUALS-ITS-RECORD`. Then its identity:

```bash
uv run python -c "import sys, pathlib; sys.path.insert(0, 'scripts'); from build_wasm_space import bundle_sha256; print(bundle_sha256(pathlib.Path('.local/tmp/pres-6/runner-$RUN/space')))"
```

**The receipt** (automation item 6): GitHub `main`, Pages, the Space's files and direct page against that build, the
public MLflow mirror and the links, each checked independently and anonymously, every attempt kept:

```bash
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 uv run python scripts/publication_receipt.py --landing land/pres-6 --bundle ".local/tmp/pres-6/runner-$RUN/space" --expect <the identity just printed> --date pres-6
```

Expect six rows `PASS` and `PASS: wrote reports/presentation/release-checks/pres-6-publication-receipt.json`, with
`pres-6-postdeploy-links.json` and `pres-6-postdeploy-mlflow-mirror.json` beside it; exit 0.
- **The direct page** passes by CP-18c's rule (`cp18.publish.normalized`): the record's `removed_bytes` is the host's
  script and meta run (495 bytes on 2026-11-14).
- **The links record** lists every hop of every redirect. Every link into the Space must end on the Space's own host:
  `cross_host_redirects` must be `[]`. The two same-host redirects known today are `….mlflow` → `….mlflow/` and the
  Space's root → `/index.html`.
- **This is the receipt's first run against a runner-published Space.** If the Space-files row fails because the Space
  moved after `$RUN` (a newer run published), rerun from the download with the newer run. If it fails for a reason the
  runner's own served-identity check does not share (for example the card `README.md`, which the runner verifies in
  the Hub tree only), keep the record, report it as a receipt-tool gap with the file names, and verify the Space with
  the runner's `publication.json`; the GitHub, Pages, MLflow and link rows still bind.

The browser records:

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py release https://hrsi56.github.io/delu-day-ahead-forecast/ --shots .local/artifacts/pres-6/public-report --out reports/presentation/release-checks/pres-6-public-report.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py mlflow-routes --mirror-record reports/presentation/release-checks/pres-6-postdeploy-mlflow-mirror.json --shots .local/artifacts/pres-6/public-mlflow-postdeploy --out reports/presentation/release-checks/pres-6-public-mlflow-routes-postdeploy.json
```

Each passes with `passed` true. GitHub may answer anonymous `blob` requests with 503 after a burst: keep the failed
record, wait, and rerun with a new `--date` (for example `pres-6-retry-1`); a 503 is never a pass. The links to
`blob/evidence/pres-6/…` answer 404 until the tag is pushed: run the checks after the push.

### 8.6 Step 5 — A12, then the receipt

**A12 (§10.5).** An independent post-deployment check is required if either:

1. a served surface differs from what the binding independent pre-deployment review covered: Pages' bytes differ from
   `<final_page_sha256>`, the focused recheck's page; or the public MLflow differs from the committed export; or
2. a required public check above fails without a passing targeted retry.

**Where it can add something** even without a trigger: the deployed page's order and the product finding's placement
in a real browser (A2 under A8), and the new link rule, live: one fresh anonymous visit to the deployed report in both
engines, reading `#outcomes` and `#business` and following the report's links into the Space hop by hop. A checker that
wrote none of PRES-6 forms its findings before reading earlier reviews and writes a dated review under `docs/track-b/`
with the per-surface identities, first failures and retries, and its PASS / FAIL / INCOMPLETE verdict.

Then fill §8.1's last three columns from the records. The disposition is complete only when every row is verified.

### 8.7 If publication fails

Stop the rollout and name each affected URL and revision. The identities to restore are Pages
`983a75c44b0f93dabd183ee810158aefbfa62adfb5545b4a433afe4b5bbb9475` and README `bc98e9cc…c472` (PRES-5 fix 1). PRES-6
touches neither the Space nor MLflow. No force-push or history rewrite is part of a recovery, and `main` keeps the
runner's commits: a revert is a new commit on top of them, and a rollback is its own Owner action.

## 9. Applicability matrix

### 9.1 PUBLISH_RULES 1.5, clause by clause

| Clause | Applies? | How PRES-6 meets it, or why not | Evidence |
|---|---|---|---|
| §1.1–§1.3 authority, identities, categories | yes | Rules 1.5 and research v21-r20 §24.14 by the brief's hashes; the product status (v6, "final candidate · pending 4.7T", live on the Space) unchanged; every new figure a development research result | §1; the brief |
| §2 reader contract; A1; A2 | yes | Each new number names its metric beside it (A1); **A2 under A8 applies to the product finding** (O48), measured with the persistent header in Chrome and WebKit | §7; `pres-6-placement-o48.json`; `pres-6-local-release.json` |
| §3.1 evidence classes; withheld claims | yes | Development, post-selection on every product result; nothing live, prospective or 4.7T's; W54 and W55 added and guarded, W1–W53 in force | `test_51` |
| §3.2 scores, comparisons, uncertainty | yes | The naive as the reference beside every error; regime means with the paired block-bootstrap intervals of §0; coverage with width at each level, the nominal level a reference; thin subsets stated (none) | §0; §4 |
| §3.3 counting | yes | No new rule, verdict or N; the 2,068 days and three regimes counted from the committed rows | §4 |
| §3.4 provenance and formatting | yes | Every number a record; whole percents, four significant figures for fractions and ratios, one decimal for EUR/MWh | the lint in the prerelease; `test_30` |
| §4 registry, transitions; A3; A10 | no change | No identity added or adopted; no generation revised in place | §2; §5a |
| §5 page architecture; **A8** | **yes, triggered (O46)** | A8's order; the three product sections complement each other: five product topics route to the canonical result graphics, Business insights cites the results in words with no chart; the comparison and later sections unchanged except R1, R2, R3, R5 and R7's wording | §5b–§5d; `test_51` |
| §5.1 twelve subjects; §5.1a Product results and Business insights | yes | §5b (subject 6 now supported on two development days); Product results' five items; Business insights' use, measured implications, gap and limits | §5, §5b |
| §5.2 page budget | yes | `<final_page_bytes>` bytes ≤ 2.0 MB; the regime chart draws point error only and the explanation's table its signed means only, to fit | `reports/cp3/pages_build.json` |
| §6 charts, discovery; A5 | yes | Five new charts, each with its heading, a route in "Explore these results", direct labels, and its policy, artifact, population, dates, units and class | §5c; `test_31`; `test_51` |
| §7.1–§7.3 product, live, final-product Space; A7, A9 | the Space's (CP-18c) | The report shows no live panel or live number, and says the Space shows the live record, "prospective evaluation in progress" | `test_24`, `test_51` |
| §8 surfaces | yes | Report and README updated and in agreement; MLflow and the Space unchanged (§6, §8.4) | §8 |
| §9 browser and accessibility matrix | yes | The release check over HTTP, both engines, every width, iPhone emulation | `pres-6-local-release.json` |
| §10.1–§10.4 independence, fresh reader, public identity, verdict; A6 | yes | Editorial review, fresh reader and Integration Critic, none an author of PRES-6; the public checks after the Orchestrator's steps | `editorial.md`, `fresh-reader.md`, `integration.md`; §8.5 |
| §10.5 A12 | yes, after deployment | Its conditions and the useful check | §8.6 |
| §11 packet and order | yes | §0 before the computation; build → editorial → fresh reader → Integration at the candidate → final build → focused recheck → the Orchestrator's steps | this packet |
| §12 baseline coverage | yes | Invariant 10's date: every research number on days through 2026-09-06 | `test_51`; `test_36` |
| §13 acceptance record | yes | §9.2 | — |
| §14 pending triggers | yes | A8's trigger was decided by O46; 4.7T's publication remains its own | the brief |
| A11 work availability | yes | One usage-limit pause, recorded (§10.2) | the ledger |

### 9.2 The §13 acceptance record

| Area | Record |
|---|---|
| Authority | Rules 1.5 `1bc0c523…f94e`; research v21-r20 §24.14; brief `bdb78f02…40e5f6`; rulings O46, O48, the explanation ruling (§10.1) |
| Identity | `gauntlet/pres-6` off `87811abc`; `<final_candidate_sha>`; `<evidence_tip_sha>`; the landing and served identities after the Orchestrator's steps |
| Claims | §0's rules committed before the numbers; §4's records with their source rows, populations and intervals; C1001–C1007 |
| Reader | A8's order; the product finding within A2 (O48); the fresh reader's record |
| Content | Product results' five items; Business insights with its gap; the twelve subjects (§5b) |
| Charts | Five charts, each identified, routed and directly labelled |
| Accessibility | The engine and width matrix over HTTP |
| Tracking | MLflow unchanged; the manifest's sources list only (§6) |
| Release | The prerelease in a clean worktree; the `--final` build; the exact-candidate Integration check; the focused recheck |
| Public check | After the Orchestrator's steps (§8.5–§8.6) |
| Follow-up | §10.3's open items with proposed rulings; the reviews' findings, each dispositioned (§10.4) |

### 9.3 The runbook

| Touchpoint | Status |
|---|---|
| `registry.EVIDENCE_TAGS["evidence/pres-6"]` | added; its date set in the final-build commit to that commit's date |
| `research.py::SOURCES`, `POPULATIONS` | PRES-6's seven files by blob and tag; the regime populations, `pres6-p-v5`, `pres6-explain-days` |
| Claim map and blocks | `pres6-claims.md`; `PRES6_BLOCKS`; `v6.product.attribution` and PRES-5's R1, R2, R7 blocks reworded |
| `CHARTS_BY_RUN`, `mlflow_export.py` | not needed: no run or route changes |
| Tests | `tests/test_51`; updates to tests 29, 33, 43, 48 |
| Limits to watch | A2 under A8 in both engines; chart text ≥ 12 px; the 2.0 MB budget (margin `<margin>` bytes) |

### 9.4 The brief's observable outcome

| Outcome | Where it is met | Evidence |
|---|---|---|
| 1 The order (A8) | navigation → opening → How the product works → Product results → Business insights → How the models compare → the rest unchanged | `test_51::test_the_order_is_a8s_product_first` |
| 2 Product results | forecast against observed on the rule's three days and the ten bins; error over time; error by regime with counts and intervals; the explanation (the committed attribution, two development days); coverage with width at 50/80/95%; each graphic identified; populations agree; A2 on the product finding | §0, §4, §7 |
| 3 Business insights | the intended use, the measured implications with their limits, the gap; no profit curve; W54 | `test_51` |
| 4 The README | "Product results" and "Business insights" in the glance, through the claim layer, the same numbers as the page | `test_51::test_the_readme_carries_the_same_claims` |
| 5 The link checker | hop by hop, the chain recorded, a cross-host end fails; the recorded `/history/` fixture | `test_33` |
| 6 The receipt's Space page | `cp18.publish.normalized`, imported; the recorded served page | `test_48` |
| 7 R1–R7 | §10.5 | — |
| 8 The page budget | `<final_page_bytes>` bytes | `reports/cp3/pages_build.json` |
| 9 Review | editorial, fresh reader, Integration at the candidate, focused recheck at the final SHA | `docs/track-b/evidence/pres-6/` |
| 10 The packet | §8 | — |

## 10. Rulings, disclosures and open presentation items

### 10.1 The Orchestrator's rulings in this block

| Ruling | What it decided |
|---|---|
| O46 | A8's product-first order now (reverses O38); the brief's basis |
| O48 | `scripts/check_reader_paths.py` and its test join the allowed paths: on an A8 page `PLACEMENT_JS` measures `#product-finding`, on an A4 page `#comparison-finding`, chosen from the page's own sections; a negative control each way; nothing else in the tool changes |
| The explanation (the Orchestrator's second message, superseding the first form of O49) | Use CP-17-probe's committed attribution under the brief's first branch and compute nothing; the label says it is an attribution of the named development days' issued median within one fitted model, never causality, incremental value or general behaviour; only days through 2026-09-06; cite the result by its committed path and evidence tag, with the check that its quantiles equal CP-28's arm A1 rows |

**A defect of the brief, resolved:** the brief pointed the explanation to "the stored networks and features", which
names CP-28's `networks.npz` and `features.parquet`. Those belong to the blend arms' meta-learner (their inputs are
member error statistics, their outputs blend weights) and cannot explain v6. The Orchestrator confirmed the error; the
existing committed result made any computation unnecessary.

### 10.2 Disclosures

- **§0 was corrected twice before use,** each in its own commit before the numbers it governs: coverage for v6 only
  (`beac7da6`: the naive's daily rows carry no coverage), and the explanation's source (`72e688e2`: the packet first
  said no committed explanation existed).
- **A defect found and fixed before review:** a second `regime_table()` in `build_pages.py` silently replaced PRES-6's,
  so Product results rendered v1's stratum table with unrounded values. The presentation suites passed it; `test_51`
  now refuses it (the pre-fix page fails with 126 foreign values).
- **The explanation chart's first draft mislabelled rows:** side-by-side panels share row labels, and the last day uses
  one more group. The chart now draws the nine groups both days use and states the tenth beside it (§0 had said "each
  day's … by group"; the values table keeps every group). A test refuses differing panels.
- **The fixtures were recorded live** on 2026-11-14 at 11:51 UTC by anonymous GETs that follow no redirect; the served
  page's injected script carries the Space creator's public user id, no credential.
- **The ledger's early rows are bounds,** not timings (the ledger says which). One usage-limit pause, about 12:15 to
  15:45 UTC; nothing ran during it.
- **The commit hook's fingerprint check (F1) is skipped in this worktree** (`.githooks/credential-fingerprints.json`
  is local to the primary checkout); F2 and F3 ran on every commit, and §8.3's value-based scan runs before the push.
- **A first full test run was stopped** at about 12% (25 minutes) in favour of the clean-worktree prerelease.

### 10.3 Open presentation items, each with a proposed ruling

1. **A2's margin on phones is 25.5 px** (2,394.5 against 2,420). Proposed: accept; anything added above the product
   finding must be re-measured.
2. **The page budget's margin is small** (`<margin>` bytes). Proposed: accept; the next publication that adds a chart
   plans its bytes first (for example by moving v1's archive figures out of the page, an Owner decision).
3. **The naive's coverage is not shown** (its daily rows hold MAE and WIS only). Proposed: accept; a later checkpoint
   may commit the naive's hourly quantiles on P-all.
4. **The explanation covers two development days,** not the population; the text says so. Proposed: accept; a
   population attribution would need a new, authorized inference run.
5. **The receipt's Space rows have never run against a runner-published Space** (§8.5). Proposed: run them against the
   runner's `pipeline` artifact; a failure the runner's own served-identity check does not share is a tool gap,
   recorded, not a PRES-6 failure.
6. **Business insights draws no chart** (A8: business conclusions cite the results "without duplicating full charts").
   Proposed: accept.

### 10.4 The reviews' findings and their dispositions

(Filled after the reviews.)

### 10.5 Integration review 4's R1–R7

| Item | Disposition |
|---|---|
| R1 | **Applied.** The every-day panel: "the lowest error of the re-baseline's policies" (`everyday.finding.v6`) |
| R2 | **Applied.** `v6.fresh.terms`: "The p-values come from a 7-day block bootstrap with 10,000 draws" |
| R3 | **Applied.** The values table shows a code text two rows share with its experiment ("A1, …"); `test_51::test_r3_a_shared_code_text_carries_its_experiment` |
| R4 | **Applied.** The release records are made over HTTP (`pres-6-local-release.json`; the final-SHA record likewise), with the served page's SHA-256 bound beside each (§7) |
| R5 | **Applied.** The every-day panel opens with its question as a sentence (`everyday.question`) |
| R6 | **Applied.** The machine-hours ledger (`.local/artifacts/pres-6/ledger.md`), named in the return |
| R7 | **Applied.** "While v6 runs on the Space, its live record stays …", which holds on both of 4.7T's branches (`v6.fresh.meaning`) |

None changes a published number.
