# PRES-7 editorial review

| Item | Value |
|---|---|
| Candidate | `306c6096a31fc2e68a00f948c350ee7d5879b22f` (`gauntlet/pres-7`), clean detached checkout `.local/worktrees/pres-7/editorial` |
| Page `docs/index.html` | SHA-256 `a6a67a6acbe70825a39bd68d2ebc766c89dccf0e7da284869c5c139e9c55688a`, 2,081,626 bytes (+83,753 against the base) |
| README `README.md` | SHA-256 `e2fa8ce4b50cd91794065a3ce8bf93f5e351f69deff673a73dae7690bba73821`, 65,352 bytes (+3,246) |
| Published base | `a5db292aa0aed68886ea0ab7237cf5fe9a672b65`: page `5e294d40790f3415c14cf932e94f1351e2e99a0b84d6efd3d2321046d7eccdaa`, 1,997,873 bytes; README `da9ae187766c895d102676b16a5870540029d471b26687fe78cc3319edc77e1a`, 62,106 bytes (both hashes match the brief) |
| Rules | `docs/PUBLISH_RULES.md` 1.5 `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e` (decision 30 supersedes §5.2's page budget); `docs/track-b/publication-standard-v1.md` `7bb90c4cbd15bde42121d615bd850854610a1aa0b3a776190a58ef481abeb68c` (incorporated baseline) |
| Round inputs | brief `b6a45b6002969c238547938661841e74f7b44f343fc60e3a56ced02879451175`; packet `7fe2d84d1e53f81bace1495eb8b77b25b6a5f68b5a1caf57c250bd7a0c0af23d` (§0 only); contract `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; `cp29-claims.md` `ef01e60a…82c6`; `pres7-claims.md` `8a19abf2…37ab`; `reports/cp29/daily.csv` `bf39cc7b…7ae3`, `summary.csv` `3392db1b…196f`, `paired.csv` `f07d4c17…4b18` (all three equal the brief's hashes, and their blobs equal `evidence/cp-29`'s) |
| Date | Started 2026-11-16; paused by a weekly usage limit after the standard v1 §§1–7 reading; resumed and finished 2026-11-17 at the same candidate (HEAD re-verified, tree clean) |

## Independence and method

- **Independence.** I wrote none of PRES-7 and took no part in building it. I worked read-only in the editorial worktree: I made no edits, staging, commits or pushes, used no network (`uv run --offline`), and read no credential. I exported `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1` in every shell that ran Python. The single import of the project's own lint ran with `PYTHONDONTWRITEBYTECODE=1`. `uv` created the worktree's ignored `.venv`, and `git status --porcelain` stayed empty.
- **Pause.** A weekly usage limit paused the review after I had read standard v1 §§1–7. It resumed on 2026-11-17 at the same point, not from the start. HEAD was still `306c6096`, and none of the evidence below depends on the time of the pause.
- **Read, in this order:**
  - `AGENTS.md`;
  - the brief;
  - the packet's §0;
  - `pres7-claims.md` and `cp29-claims.md`;
  - the contract's §§1–9 (I also read §§10–11);
  - PUBLISH_RULES §§2, 3, 5, 5.1a, 6, A1, A2, A5, A8, 10.1 and the §12 coverage map;
  - standard v1 §§0–7.
- **Read to check specific claims:**
  - PRES-6's `fresh-reader.md` and its packet's §10.3 items 7–8, for what the wording pass was meant to fix;
  - `reports/cp28/report.md` line 23 and CP-28's integration lines on the 14-day resampling, for the new "descriptive" sentence;
  - the diffs of `scripts/build_pages.py`, `scripts/readme_research.py`, `src/delu_forecast/research_claims.py`, `publication_lint.py` and `registry.py`, for how the text and the chart are produced.
- **Not opened:** `progress.md`, any syllabus, Track A or Track C material, `orchestrator-role.md`, and the Claude memory directory.
- **Tools.** I wrote my own scripts and did not reuse the build's code. They live in `/Users/djourno/Downloads/PJM/.local/tmp/pres-7/editorial/scratch/`:
  - `pagetext.py`, `flat.py` and `extract.py` extract text by block;
  - `numdiff.py` compares the rendered numbers outside Business insights;
  - `verify_numbers.py` checks the bindings and re-derives the series;
  - `verify_chart.py` re-derives the polylines;
  - `verify_readme.py` checks the README;
  - `sigfig.py` lists numbers above four significant figures;
  - `axis.py` reads the comparison axis.
  - Their outputs are `*.out` beside them. To rerun any of them: `cd .local/worktrees/pres-7/editorial && MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 uv run --offline python <script> .` (`numdiff.py` takes `base_index.html docs/index.html`).
- **Outside my scope, not reviewed:** browser rendering, A2 placement, the test suites and the final build. One observation is for the Integration check, not a finding of this review. `tests/cp29/test_claims.py` is edited (+37/−8) although the brief lists `tests/cp29/` as read-only. The edit cites a ruling, O63, that appears in neither the brief nor the packet's §0.

## Checks that passed

**P1. Every number in Business insights is bound to its committed row** (`verify_numbers.out`).
- All 44 `<data>` elements in `section#business` that bind a `cp29.*` record (39 distinct records) pass two tests:
  - the `value` attribute equals the `summary.csv` or `paired.csv` field exactly;
  - the displayed text equals that value at the displayed rounding.
- Covered: C1102–C1107, C1201–C1203 and the paired intervals (`total_ci_lower`, `total_ci_upper`). None fails.
- No numeral in the section's text sits outside a `<data>` binding or a `data-structural` span (the script's unbound list is empty).
- The pre-existing P70 values (17.2, 34.6, 30.7, 51.7, 0.7826) are unchanged from the base.

**P2. The README's Business insights paragraph carries the same values through the claim layer** (`verify_readme.out`).
- `scripts/readme_research.py` renders the paragraph from these blocks via `render(key)`: `business.use`, `business.measured`, `economics.setup`, `.finding`, `.difference`, `.v5`, `.risk`, `.sensitivity`, `.regimes`, `.limits`, `.assumptions`, then `business.gap` and `business.limits`.
- All 31 economic numerals in it (2,068; 257,212; 0.8953; 287,292; 220,136; 0.7662; +37,077 [+32,323, +42,311]; 358; 55,708; 55,544; +165 [−727, +1,032]; 137; 97; 136; 355; 227; 356,333; 0.9210; 176,202; 0.8495; 0.6445; 246; 22.2; 0.8775; 481; 0.9118; 1,341) are values P1 verified on the page.
- The README omits C1202 and C1203 and links to them instead (Advisory A6).

**P3. The chart's end values and its shape follow from `daily.csv`** (`verify_numbers.out`, `verify_chart.out`).
- At wear 25 on P-all there is one row per day for each line: 2,068 days for v6 median, the naive median and perfect foresight, from 2020-12-29 to 2026-09-06, with no duplicate days.
- Untraded days stay in the series as their committed zero:

| Line | Re-derived end (EUR) | Record (EUR) | Relative difference |
|---|---|---|---|
| v6 | 257,212.49414167128 | 257,212.49414167088 | 1.6e-15 |
| naive | 220,135.66873625107 | 220,135.668736251 | 2.6e-16 |
| perfect foresight | 287,291.70019389637 | 287,291.7001938969 | 1.8e-15 |

- All three are within 1e-9; `math.fsum` agrees to the same order.
- The re-derived measures match their records:
  - maximum drawdown: 136.379 for v6 and 0 for perfect foresight;
  - losing days: 137, 355 and 0;
  - trading days: 1,770, 1,872 and 1,857;
  - missing days: 33, 11 and 0.
- **The shape.** I mapped each day to x linearly from the first to the last date, and y from the lower of 0 and the lowest point (the naive's −219.59 EUR on 2021-03-21) up to 300 thousand EUR. I thinned the points by packet §0's rule (each pixel column's first, lowest, highest and last point). The result is byte-identical to the drawn `points` strings for all six polylines (desktop 1,204/1,274/1,345 points; phone 379/405/450).
- Every drawn point lies on the full-resolution series. Each line's last point converts back to its record within 0.1 px.
- The axes follow §0:
  - y ticks at 0, 100, 200 and 300 thousand EUR;
  - x ticks at each 1 January, 2021–2026 on desktop and odd years on the phone;
  - "doing nothing" drawn and labelled at 0.

**P4. §5.1a's requirements are met, except one** (Violation E1).
- **Intended use:** `business.use`.
- **Measured benefit:**
  - against the naive, +37,077 EUR paired over the same days with its 95% interval;
  - against the ceiling, 0.8953 against 0.7662.
- **Losses and risk:**
  - losing days, the largest daily loss and the drawdown;
  - the risk-aware variant;
  - wear-cost sensitivity at €0 and €50, reported "never chosen afterwards";
  - the regimes.
- **Limits:** P6.
- **Cumulative net profit over the full named period:** 2020-12-29 to 2026-09-06, all 2,068 eligible days. Eligibility is defined directly above, in Product results.
- **Against the declared benchmark:** the similar-day naive.
- **Units:** EUR, with the axis in thousand EUR, for one 1 MW / 2 MWh battery.
- **Costs:** €25 per MWh discharged and €0.10 per MWh traded.
- **Constraints:** 1 MW at the grid, 2 MWh usable, 85% round trip, at most one cycle a day, one direction an hour.
- **Labelled simulated, not realized:** "no money was traded"; "not realized income".
- **Failed and missing days kept:** 33 and 11 missing-hour days, "Every such day stays in the curve, at zero".
- **No return without capital:** "No return or payback is computed: there is no capital cost".
- **No business success percentage:** the shares are fractions with their denominator named (287,292 EUR).

**P5. The graphic names its identity** (one part falls short; see E1).
- Title: "Cumulative net profit of one battery from v6's, the naive's and perfect forecasts, development days".
- The line directly above the chart carries:
  - the battery (1 MW / 2 MWh) and the wear cost (€25);
  - the policy and artifact: v6's stored forecasts, v6 · DDNN-2 alone, A1 in the frozen records, the median rule; the naive; the cleared prices as perfect foresight;
  - the population, its dates and its unit: 2,068 eligible days, 2020-12-29 to 2026-09-06, EUR;
  - the class: "simulated, development, post-selection".
- The `<desc>` repeats the unit, battery, period, wear and class, and names each line's dash style.
- A key below gives the three totals, bound to C1201.

**P6. The limits are on the page and in the README in plain words.**

| Required limit | Where |
|---|---|
| A simulation, not realized income | caveat line; `economics.limits` ("No money was traded… not realized income") |
| Day-ahead only: no intraday, balancing or reserves | `economics.limits`; `business.gap` |
| A price-taker | `economics.assumptions` |
| Hourly | "hourly, not quarter-hourly" |
| Post-selection, optimistic for v6 | caveat line; `economics.limits` |
| Not a trading recommendation | caveat line; `economics.limits` |
| No return or payback | `economics.limits` |

- **Contract §8, all present:**
  - price-taker;
  - day-ahead only, a large share of revenue excluded;
  - no outages or imbalance: "never out of service and never deviates from its schedule";
  - costs as stated assumptions, with the grid-fee exemption a legal assumption;
  - hourly;
  - post-selection;
  - simulated.
- **Contract §9:**
  - present: not a trading recommendation; not realized income; not a property of v6 alone; not 4.7T's result. "Not a test of v6" follows from "4.7T … is v6's one test on new data".
  - not stated in words: "an investment case" and "a forecast of future profit". No sentence claims either (Advisory A10).

**P7. Nothing forbidden appears.**
- **No error or coverage figure called a profit or success rate.** The forecast-error paragraph (P70) is separate, and `business.gap` says so in words.
- **No annualized return** (W56).
- **No live or prospective profit:**
  - "the report shows no live or prospective profit";
  - outside `#business`, no rendered block contains profit, earn, income, revenue or payback;
  - W58's pattern finds nothing.
- **No class mixing in one sentence:** development forecast errors and simulated money sit in separate paragraphs.

**P8. The wording pass changed no number outside Business insights** (`numdiff.out`).
- Bound `<data>` outside `#business`: base 1,342, candidate 1,345, none removed or changed. Added: 2,068, −7% and 10,747 in the new reconciliation sentence, each bound (`cp28.paired_dates`, `derived.cp28.A1.MAE`, `cp24.metrics.B0.pooled.n_hours`).
- Text numerals: none removed. Added: those three, the two dates 2026-09-06 and 2026-04-07, the structural "14" (14-day blocks) and four "0.4" axis ticks.
- Each wording item, at its place:
  - **"Owner"**, first use (page block 27; README line 19): "The Owner, the project's lead, has the Space run…".
  - **"re-baseline"**, first use (definitions list): "before the re-baseline re-scored every policy on every day".
  - **"4.7T"**, directly below the headline: "frozen for 4.7T, its one test on new data: 90 days registered in advance".
  - **"A1 in the frozen records"**, first use: "v6 (named A1 in the frozen records)".
  - **Counts:** "7 candidates tested" and "13 policies drawn". The 25 and 16 already said what they count.
  - **−7% beside −6%:** reconciled at the comparison, beside the −6%. The sentence names the two development ends, 2026-09-06 and 2026-04-07.
  - **"Descriptive" against "confidence":** the reconciling sentence is accurate. CP-28's report line 23: intervals "studentized… descriptive, never a substitute for the registered 0.995/1.02 tests"; the primary analysis uses 14-day blocks. Its placement fails the define-at-first-use rule (E2).

**P9. The comparison axis fix (item 4) is geometrically effective** (`axis.py`). Only the page's comparison widens to 0.4, on both variants.
- **Phone:** before, the lowest polygon point was x = −11.3, off the canvas. Now the axis starts at x = 22.0 and the lowest point is 29.1.
- **Desktop:** before, the lowest point was 260.8, left of the 0.5 axis at 270. Now the axis starts at 270 and the lowest point is 291.6.
- The pinned MLflow overviews keep (0.5, 1.1) through `page_comparison`.

**P10. Standard v1 §§4 and 7 hold for codes, routes and the evidence row.**
- **Codes:** the new text has no checkpoint codes, claim IDs, §-references or underscore identifiers. "A1" appears only as the frozen-record alias defined at first use, as in PRES-6's identity line.
- **Routes:** the five "Explore the evaluation" links name what each lands on.
- **Evidence row:** audit-grade links only, labelled "<type>, frozen <date>".
  - `evidence/cp-29` exists locally at `d253482f`, dated 2026-11-15, and contains all six linked files. The blobs of the three CSVs equal the candidate's.
  - The seventh link, to `evidence/pres-7`, is discussed in A15.
- **The chart against §6:**
  - question and finding;
  - metric;
  - comparator, the naive, with perfect foresight as the ceiling;
  - population;
  - class;
  - units;
  - a labelled reference line, the zero line, kept distinct from the ceiling;
  - direct end labels and distinct dash styles, so no meaning rests on colour;
  - a reorganized phone variant;
  - the evidence row.

## Violations

**E1 (medium). The profit evaluation omits its initial conditions, and the graphic omits part of the battery and its costs.**
- **Clauses:**
  - PUBLISH_RULES 1.5 §5.1a: "show cumulative net profit/value … with units, costs, constraints, **initial conditions** and risk/loss context";
  - the brief's Observable outcome 1: "The graphic names: the battery and its costs (C1101)";
  - packet §0 commits the same in "the chart's title and description and in the line directly above it".
- **Observation:**
  - The contract's §2 initial and terminal condition, "empty at the start and at the end of each delivery day … no state carries between days", appears nowhere on the page or in the README. A grep for "empty", "state of charge" and "start of each" finds nothing in either.
  - The line above the chart and its `<desc>` name only "1 MW / 2 MWh" and "€25 per MWh of wear". The €0.10 per MWh exchange fee, the 85% round trip and the one-cycle and one-direction limits of C1101 appear only two headings further down (`#business-setup`).
- **Evidence:** `grep -c -i -E 'empty|state of charge|start of each' README.md docs/index.html` gives 0 matches. `cand_business_flat.txt` shows the `economics.chart` line and `economics.setup` text.
- **Impact:** the reader cannot tell that each day starts and ends empty, which matters for an arbitrage result (no stored energy is carried or valued between days). The graphic's identity is incomplete against the round's own bar.
- **Repair:**
  - Add the condition to `economics.setup`, which renders on both surfaces through the claim layer: "…at most one cycle a day, empty at the start and end of each day, and charging or discharging in an hour, never both."
  - Add the fee and the constraints to `economics.chart` and the `<desc>`: "…at €25 per MWh of wear and €0.10 per MWh traded, 85% round trip, one cycle a day, empty at each day's start and end…"
- **Acceptance:** both surfaces state the empty start and end. The line above the chart names both costs and the constraints. No number changes, and `verify_numbers.py` stays clean.

**E2 (medium). "Descriptive 95% intervals" is first used in the headline but defined only at the comparison.**
- **Clauses:**
  - standard v1 §4, Definitions: "Each term is defined where it is first used. Terms first used in the headline block are defined directly below it";
  - PUBLISH_RULES §2: "Define a term at first use; do not add a glossary as a substitute".
  - The headline line changed in this round ("policies" became "candidates"), so it is reviewed in full (§10.1).
- **Observation:**
  - **Page:** the headline (block 19 of 4,851) reads "with descriptive 95% intervals". The definitions list directly below has no entry for it. Product results (block 118) then calls its brackets "95% confidence intervals of the mean, from 14-day block resamples". The reconciling sentence ("confidence intervals from resampling 14-day blocks of days, called descriptive because…") appears only at block 1,071, in How the models compare, after Business insights.
  - **README:** the term appears at line 10 and is defined at line 82.
  - This is the exact confusion PRES-6's fresh reader recorded: D01 against D03.
- **Evidence:** `grep -n -i descriptive scratch/cand_text.tsv` gives blocks 19, 1071 and 1174. `grep -n descriptive README.md` gives lines 10, 50, 82…
- **Impact:** the reader meets two names for intervals from one family before the explanation. The O51 item 8 fix lands where the reader no longer needs it.
- **Repair:** move the definition directly below the headline (page and README). For example, extend the existing bullet: "Selection rule: set on 2026-10-12, before the re-baseline re-scored every policy on every day; it decided by registered tests, so the 95% intervals above are descriptive: confidence intervals from 14-day block resamples." The comparison sentence may stay or shorten. The opening grows by about one phone line, so A2's phone margin (50.5 px at PRES-6) must be re-measured by the browser check.
- **Acceptance:** the first sentence after the headline that mentions intervals defines "descriptive". A2 is re-measured and passes. No number changes.

**E3 (medium). Business insights uses three terms before defining them: "the schedule", "the median rule" and "the contract".**
- **Clauses:** PUBLISH_RULES §2, "Define a term at first use"; standard v1 §4, Definitions.
- **Observation:**
  - **"The schedule".** The section's finding (`economics.finding`, an h3) says "the schedule from v6's forecasts would have earned 257,212 EUR net". On the page this is the first mention of any trading. The battery is introduced only below, in the chart line and in `#business-setup`; the README orders setup first.
  - **"The median rule".** It is used in the chart line and the key ("v6, median rule", "Similar-day naive, median rule"), but nowhere says what it is. The heading "The battery, its costs and the trading rule" promises the rule. Its paragraph says only that the schedule "is fixed from the forecast", not that the battery takes the schedule the forecast's median prices value highest net of costs, and does nothing if none pays (contract §3).
  - **"The contract".** In `economics.untraded`, "the contract counts such a day as not traded" is undefined. In a trading context a reader may take it for a market contract.
- **Evidence:** `cand_business_flat.txt`, blocks `[h3]`, the `Drawn:` line, the key line, and the `[h4] The battery, its costs and the trading rule` paragraph.
- **Impact:** the headline money figure has no subject, and the decision rule that turns a forecast into money, the core of the evaluation, is never stated.
- **Repair:**
  - **Finding:** "On all 2,068 eligible development days, one 1 MW / 2 MWh battery scheduled each day from v6's forecasts would have earned…". Business insights is below the product finding, so A2 is unaffected.
  - **`economics.setup`:** add one sentence: "The rule: each day it takes the schedule that the forecast's median prices value highest, net of these costs, and does nothing if none pays (the median rule)."
  - **`economics.untraded`:** "…and the evaluation's rules, fixed in advance, count such a day as not traded…".
- **Acceptance:** each of the three terms is defined at or before its first use on the page and in the README. No number changes.

**E4 (low). Caveat heading worded so it will expire.**
- **Clauses:**
  - standard v1 §1, Tone: "Caveats never use wording that expires, such as 'still to be evaluated'";
  - standard v1 §5: status words ("still"…) "come only through registry tokens".
  - Both are carried unchanged by PUBLISH_RULES §12's coverage map (§1 to §2; §5 unchanged).
  - Standard v1's precedence: a brief "may never relax a clause". The brief's own phrase "what is still not evaluated" does not authorize the wording.
- **Observation:** the new `business.gap` opens "**What is still not evaluated.**" on the page (`#business-limits`) and in README line 25.
- **Evidence:**
  - the scan of changed text for the project's `STATUS_WORDS` pattern finds only this "still";
  - the project's template lint (`publication_lint.template_strings`) does not scan `PRES6_BLOCKS`, where `business.gap` sits, so it is not caught (Advisory A16).
- **Impact:** the heading becomes wrong as soon as any of the items is evaluated, for example the live record (contract §7).
- **Repair:** "**What this simulation did not evaluate.**", or "**Not evaluated.**", keeping the dated, past-tense content.
- **Acceptance:** neither surface's new text contains a status word outside a registry token.

**E5 (low). The same caveat appears twice within Business insights, and again in the README.**
- **Clauses:**
  - PUBLISH_RULES §2: "Put a caveat where it qualifies a claim, once";
  - standard v1 §1, Tone: "Each caveat appears once, where it applies".
- **Observation:** on the page:
  - **First:** the caveat line under the finding reads "Simulated, development, post-selection: no money was traded, and v6 was chosen on these same days, so its result is optimistic for it. Not realized income and not a trading recommendation."
  - **Second:** `economics.limits` repeats it almost word for word: "Simulated, development, post-selection. No money was traded, and v6 was selected on these same days, so its result is optimistic for it. … Not a trading recommendation, not realized income…".
  - **Third:** `business.limits` then says a third time "These are development results after selection."
  - The README carries the second and third.
- **Evidence:** `cand_business_flat.txt`, the `[p] Simulated, development, post-selection:` line and the two `[p]` lines under `What the simulation does not show`.
- **Impact:** repetition dilutes the caveats that are stated only once (day-ahead only, hourly, not a property of v6 alone) and lengthens a section that is already long.
- **Repair:**
  - Keep the caveat line under the finding.
  - Cut `economics.limits` to the limits not stated there: day-ahead arbitrage only, hourly, not a property of v6 alone, not 4.7T's result, no return or payback.
  - Merge `business.limits`'s post-selection half into the caveat line, or drop it.
  - The README, which has no caveat line, keeps one full statement beside its first profit number (see A6).
- **Acceptance:** each caveat appears once per surface, beside the claim it qualifies. Every P6 item is still present.

**E6 (low). The paired money difference is shown at five significant figures.**
- **Clauses:**
  - standard v1 §4, Precision: "Scores and differences: at most four significant figures" (exempt only: versions, dates, levels, counts, axis ticks and the invariant-4 statements);
  - PUBLISH_RULES §3.4: "Scores/differences: at most four significant figures on the reading path".
- **Observation:**
  - **Values:** `economics.difference` shows "+37,077 EUR [+32,323, +42,311]" (record `cp29.paired.p_all.median.v6_minus_naive.w25.total_difference_eur`, unit "EUR, paired difference of daily profits"). It is on the reading path of both surfaces; Business insights has no disclosure.
  - **The lint:** PRES-7's change to `publication_lint._unit_rule` classes EUR totals, this difference included, as "count", which the clause does not exempt.
  - **Reading:** I read "differences" as including this money difference, an estimate with an interval. If the Orchestrator rules that the clause means score differences only, that ruling closes this item.
- **Evidence:** `sigfig.py docs/index.html` lists three signed `total_difference_eur` values above four significant figures, all in `#business`. The base has none.
- **Impact:** false precision. The interval is about 10,000 EUR wide, yet the point is given to the euro. The displayed totals also disagree in the last digit: 257,212 − 220,136 = 37,076, against +37,077.
- **Repair:** render paired EUR differences at four significant figures, "+37,080 EUR [+32,320, +42,310]" (the v5 difference, +165 [−727, +1,032], already complies), or in thousand EUR, "+37.08 thousand EUR [+32.32, +42.31]". Classify `UNIT_EUR_MONEY_DIFF` as `sig4` in the lint.
- **Acceptance:** the lint's precision family fails a five-figure EUR difference (negative control) and passes the rendered values. The displayed values still round from their records.

## Advisories

- **A1. Misleading phrase: "Day by day on the same days, v6's schedule earned more than the naive's".**
  - It reads as "on every day". From `daily.csv` at wear 25, v6's schedule earned more on 1,377 days, less on 566 and the same on 125.
  - Suggest: "Paired over the same days, v6's schedule earned more in total than the naive's, though not on every day: …". Do not add the day counts unless they become committed records.
- **A2. The v5 block.** "Earned about the same" is defensible for these totals, but per §3.2's "a null result does not demonstrate equivalence" add "no advantage either way is shown". Also label the bracket "95% interval" in that block: readers who arrive by its route skip the label in `economics.difference`. Optionally name v5's four test periods.
- **A3. Untraded days.**
  - "The forecast had no value for one hour" can be read as "was worthless". Say "was missing one hour".
  - "Shortly after a clock change" is accurate for v6's 33 days (1, 2 or 7 days after a change) and the naive's 11 (7 days after). "Within a week after a clock change" is more precise.
- **A4. Tense and W57.** The text mixes "would have earned" (finding, sensitivity) with plain "earned" (difference, regimes, v5, risk-aware) and "its cumulative earnings fell". The class labels keep it within W57, but one conditional or "simulated profit" throughout would read more safely.
- **A5. Packet §0 against the page.** §0 calls perfect foresight's line "thin and dashed" and lists policy `720fc581…` and "the naive's frozen rule" in the graphic's identity. The page draws the line dotted (`2 3`, and its `<desc>` and key say "dotted") and carries neither the hash nor the rule in the chart line; the naive's rule is in Product results above. Align the packet's later sections with the page.
- **A6. The README.**
  - It omits C1202 (untraded days) and C1203 (risk-aware variant), linking to them. The brief's outcome 4 ("the same business claims") can be read either way. C1202's one sentence is the §5.1a "failed and missing days" disclosure and is worth carrying.
  - The README has no caveat line: its first profit number comes about ten numbers before "post-selection". Put the class beside the first figure.
- **A7. README length.** The README's Business insights is one paragraph of about 650 words. Splitting it at its bold labels would help a skimming reader.
- **A8. README wording.** README line 291's "The opening's −7%": a README has no "opening". "The −7% at the top" reads better there.
- **A9. Counting words.** The headline now says "7 candidates tested", but the definitions list below still defines "Policies", and the page also says "seven arms" (block 87) and "among 7 arms" (blocks 1178 and 1382). One word for the selection's candidates, defined once, would finish O51's counts item.
- **A10. Contract §9.** Its "not … an investment case or a forecast of future profit" is not stated in words. A reader can easily divide 257,212 EUR by 5.7 years. Add "not a forecast of future profit" to the limits sentence.
- **A11. Grid fees.** The page says "the exemption from grid fees is a legal assumption" but never states that no grid fees, levies or taxes were charged (contract §2). Add it to the costs.
- **A12. The population span.** The chart spans 2,078 calendar days and draws 2,068. The 10 days missing from P-all (2022-02-22, 2022-03-24, 2022-07-20/21, 2022-12-21/22, 2023-03-13, 2023-08-31, 2023-10-29, 2024-10-27) are outside the population, and the line joins across them. Eligibility is defined in Product results. A short clause near the chart ("10 days in that span lack complete prices or load forecasts and are not in the population") would answer the obvious question.
- **A13. Totals.** Totals such as 257,212 EUR show six significant figures. No clause caps a total, but thousand EUR at four figures (257.2) would match the chart's axis and E6.
- **A14. A tension in `business.measured`.** It still ends "how to size that allowance has not been evaluated". The risk-aware variant now evaluates one way of allowing for misses. Consider "…not evaluated beyond the cautious rule below".
- **A15. The `evidence/pres-7` link.**
  - "The chart's rules … frozen 2026-11-16" points at `evidence/pres-7`, which does not exist yet.
  - Standard v1 §7 requires the label date to equal the tag's date. The registry fixes 2026-11-16, and the evidence tip may be committed later. Re-check the date at the final build.
  - The link returns 404 until the tag is pushed, so packet §8 should push it with or before the Pages deploy.
- **A16. A gap in the status-word lint.** `publication_lint.TEMPLATE_SOURCES` scans only the `BLOCKS` root of `research_claims.py`, not `PRES5_BLOCKS`, `PRES6_BLOCKS`, `CP29_BLOCKS` or `PRES7_BLOCKS` (`template_strings` does not contain `business.gap`). That is why E4's "still", and the pre-existing "may still be revised" in How the product works, pass. This is for the Integration check: tests are not mine.
- **A17. "Owner".** The new definition says who the Owner is, but not why he had v6 run early. PRES-6's fresh reader asked both. This is optional and was not required by O51.
