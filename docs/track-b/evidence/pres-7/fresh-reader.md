# PRES-7 — fresh reader (PUBLISH_RULES 1.5 §10.2)

**Outcome: answers 1–5 agree with the registry, the evidence records and the derived records, and answers 7 and 8,
the brief's battery questions, agree with CP-29's records and the page's limits.** The reader quoted the battery's
257,212 EUR (0.8953 of perfect foresight's 287,292) against the naive's 220,136 (0.7662), the paired +37,080 EUR
[+32,320, +42,310], the losses, the wear sensitivity, the regimes, the cautious rule and v6 against v5 with its
interval spanning zero, each equal to its record at its displayed rounding. Its answer 8 lists the limits the page
states. Its confusions are dispositioned below: two in PRES-7's text were repaired after the reading; the others are
answered or concern sections PRES-7 does not change.

## How it was run

- **Page:** `docs/index.html` at `5575920c87f6754fcea52e8dfc65d413f6c2f819`, SHA-256
  `d2358f0feaba5cba5b55a7ea01cdc148ff1edbe058283d1f13134fb10475b0cd`, served over HTTP from `127.0.0.1` with every
  disclosure closed.
- **Screens:** written by `scripts/check_reader_paths.py release` (attempt 3, `cold_reader_screens`, 2026-11-17 from
  21:12 UTC), the page as a reader scrolls it, one viewport at a time, each step the viewport less the 56 px sticky
  header:
  - desktop, Google Chrome at 1440×900, 38 screens, supplied as D01–D38;
  - phone, Playwright WebKit at 390×844, 67 screens, supplied as P01–P67.
  They were copied under neutral names to `/Users/djourno/Downloads/PJM/.local/tmp/pres-7/fresh-reader/` (local only);
  their SHA-256 values are listed at the end. (Attempt 3's own verdict failed on one keyboard route timing out under
  the machine's load; attempt 4, on the same page, passed every check: packet §7. The screens are the page's.)
- **Reader:** one fresh agent. It wrote nothing in PRES-7 and was given no repository, project history, prior review,
  expected answers, chart locations or explanation: only the prompt below. A usage limit interrupted it before it had
  answered; it resumed from where it stopped with the same task, unchanged. It made 90 tool calls.
- **Date:** 2026-11-17 to 2026-11-18, after the editorial review's repairs.

### The prompt (verbatim)

The six questions of §10.2, unchanged, then the brief's two ("The fresh reader answers, among others: what the battery
earned with v6 against the naive, and what the result does not show").

```text
FIRST RULE: do not open, read or edit any file in /Users/djourno/.claude/projects/-Users-djourno-Downloads-PJM/memory/ (the Claude memory directory).

You are a reader seeing a web page for the first time. You have no other information about it, and you must not look for any: do not open, list or search any file or directory other than the 105 image files named below, do not run any command, and do not use the web.

The page is shown as screenshots taken while scrolling from the top to the bottom, with every collapsible section closed. There are two renderings of the same page: first a desktop browser (1440 × 900), screens D01 to D38; then a phone browser (390 × 844), screens P01 to P67. Read every one of them, in this order, with the Read tool. The files are in the folder /Users/djourno/Downloads/PJM/.local/tmp/pres-7/fresh-reader/ and are named D01.png, D02.png, … D38.png, then P01.png, P02.png, … P67.png (two digits, zero-padded), for example:

/Users/djourno/Downloads/PJM/.local/tmp/pres-7/fresh-reader/D01.png
/Users/djourno/Downloads/PJM/.local/tmp/pres-7/fresh-reader/D38.png
/Users/djourno/Downloads/PJM/.local/tmp/pres-7/fresh-reader/P01.png
/Users/djourno/Downloads/PJM/.local/tmp/pres-7/fresh-reader/P67.png

Read as an experienced data-science lead would, then answer these eight questions. For questions 1 to 5, 7 and 8, cite the screen or screens (for example D02 or P05) and quote the words you rely on. If something is unclear or missing, say so rather than guessing.

1. What is the headline result, with its numbers?
2. Against what?
3. How sure are we, and on what class of evidence?
4. What does the demo run, and why not the best model?
5. What was tried and dropped?
6. What would you ask the candidate?
7. What would a battery have earned with v6's forecasts, against the naive forecast, with its numbers?
8. What does that battery result not show?

After the eight answers, list anything that confused you, each with the screen where it happened.

Reply with your answers only, as plain text.
```

## The reader's answers (verbatim)

```text
1. What is the headline result, with its numbers?

The headline is v6 · DDNN-2 alone against v5, measured on every development day. D01/P01: "Selected by a rule set in advance: against v5 on all 2,068 development days, −7% [−9%, −5%] in point error and −11% [−13%, −9%] in interval error, as shares of v5's, with descriptive 95% intervals; 7 candidate policies tested."

The absolute figures (D02, P03–P04): "On all 2,068 eligible development days, v6's mean daily point error was 17.2 EUR/MWh [15.4, 19.1] against the similar-day naive's 34.6." Also: "Its 80% prediction intervals, 51.7 EUR/MWh wide on average, covered 0.7826 of the hours."

A second figure uses a different population, v5's five test periods (D12, D21, P21, P40): "−6% [−9%, −2%] on the point-error score and −11% [−15%, −8%] on the interval score." Its ratios to the naive are 0.493 and 0.437 (D12). D12 explains the difference: "The headline's −7% is another population."

The every-day table (D15) gives v6 a point error of 17.2 and an interval error of 9.7 EUR/MWh, with ratios to the naive of 0.4974 and 0.4580.

2. Against what?

- v5, its predecessor, which was the comparator set in advance. D16/P30: "Set in advance: v5 itself, the control of the selection rule, so the comparator is the predecessor."
- The similar-day naive, which normalises every score. D03: "The naive forecasts each hour with the same hour's price the day before, or a week before for Mondays and weekends." D13: "Each score divides a model's error by that of a simple similar-day forecast in the same period, which therefore scores 1.000."
- Against the naive on the five periods, v6 scores "−51% [−54%, −46%] on the point-error score and −56% [−59%, −52%] on the interval score" (D21).
- The benchmarks and targets are shown on the chart: daily LEAR (0.658/0.639) and daily LightGBM (0.784/0.740), with targets of "each error score at least 10% below the strongest benchmark's" (D12–D13). However, v6 "was tested by its own selection rule, on every development day, not against the targets" (D13).
- Six other arms in the selection also passed: "the six others, blends of v5's members, also passed every gate and were not selected" (D16). Their scores are not shown.

3. How sure are we, and on what class of evidence?

All of it is development evidence, scored after selection. D02: "Development · post-selection: development evidence, not a test on new data; descriptive intervals: not the rule's own test."

- The model was chosen on the same days it is scored on. D03: "v6 was chosen on these days." D22: "v6 was selected on every development day, four of these periods among them, after DDNN-2 alone had already scored best there."
- The intervals are bootstrap intervals and are only descriptive. D03: "95% confidence intervals of the mean, from 14-day block resamples." D14: "called descriptive because the selection decided by its registered tests, not by them."
- v6 and v5 did not work from the same information (D22). v6's forecasts were "issued one or two hours earlier, refitted every day". Under v5's protocol, the arm of the same name "scored 0.4785 and 0.4271".
- The same test periods were reused. v5 was "the second decision on a distributional neural network over the same five test periods" (D17/D25). The five-period gain of v5 over v4 does not hold across all days: "v5 against v4: −1% [−1%, +1%]" (D14).
- The intervals cover slightly less than their nominal level. D05: "each a little below its nominal level"; the crisis gives 0.7531 at 80%. In D07 the 80% coverage falls to 0.6868 in one forecast bin.
- The only test on new data has not happened yet. D11: "4.7T, which opens no earlier than 2026-12-04, is v6's one test on new data." D02: "90 days registered in advance." The live record is "prospective evaluation in progress" (D01), and the page shows no live numbers.
- The only confirmatory-style result on the page belongs to v1. D34: "confirmatory-style, not power-qualified."

My reading: v6 clearly beats the naive in-sample, by about half in every regime (ratios 0.4508–0.5047, all intervals below one; D04). The margin over v5 (−6 to −7%) is modest. It is measured after selection, under a different protocol, and has not been confirmed on new data.

4. What does the demo run, and why not the best model?

The Space (the live product) runs v6. D01/P02: "The Owner, the project's lead, has the Space run v6 · DDNN-2 alone daily before its one test: prospective evaluation in progress. A pass releases it; otherwise v1, the last released generation, is the product again." D35: "The frozen v6 issues each day's forecast before the auction; outcomes are scored after the fact."

The forecast chart on this page itself is "A stored development-day forecast, not a live one" (D01). v1's demo has moved: "the Space's root has since been given to the live product, and v1's demo is under its History" (D34).

On "why not the best model", the page does not support the premise. v6 is the model the page ranks best: it has "the lowest error of the re-baseline's policies on both scores" (D14). What v6 is not is released; v1 remains "the last released generation" (D01).

What is unclear is whether A1 was the best of the 7 selection arms. The six blends "also passed every gate and were not selected" (D16), but their scores and the reason the rule picked A1 are not on the visible page; there is only a "Read it" link (D01). The page mentions "v6's in-browser retraining" (D06) and a network "written in NumPy" (D35). These might favour a single network, but that is my inference and the page does not say so.

5. What was tried and dropped?

Between v1 and v2:
- The calibration experiment: "Recalibration alone was not enough: the model itself had to adapt." (D19, P37)
- The model comparison study: "No policy met the criteria; the study informed v2's blend of two LEAR forecasts." (D19)
- v1's LightGBM quantile model with fixed-window calibration was replaced "After v1 failed in the 2022 crisis" (D19). On the development folds v1 is "28.58% worse than the naive's", and over the August 2022 peak weeks its 95% interval covered 0.194 (D34).

Between v4 and v5:
- The pooled LightGBM member for v4: "Both candidates were decisively worse than v4 in one test period … the rule allowed none, so v4 was kept as it was." (D20). They scored 0.537/0.507 and 0.534/0.505 (D13).
- The DDNN member on v4, at one third of the blend's weight: "The improvement over v4 that the rule required was not shown, on either score." (D20). It scored 0.542/0.513 (D13).

Study arms that were never candidates:
- The normalized LEAR study scored 0.672/0.646 (D13).
- v4 had three study arms. Separate hour-block models were "not shown to help" (D18, D27).
- v5 had two: "DDNN-2 alone and v3 plus a DDNN-2 member, were built only to show where the change came from" (D17, D25). DDNN-2 alone later became v6.

In v6 itself:
- "v5's two LEAR forecasts, its LightGBM and the blend are dropped" (D16).
- The six other arms in the selection, all blends of v5's members, were not selected (D16).

In the battery evaluation, the cautious 75th/25th-percentile rule "earned less: 247,436 EUR" (D10–D11).

6. What would you ask the candidate?

- What exactly was the 2026-10-12 selection rule? Why did it pick A1 over six blends that also passed every gate? Please show their scores.
- How much of v6's −7% comes from selection? DDNN-2 alone "had already scored best" on four of the periods before it was selected. Under v5's protocol the same arm scored 0.4785/0.4271, better than v6's 0.493/0.437 (D22). What in the daily protocol costs that?
- What is 4.7T's registered pass criterion, its comparator and its power over 90 days? The v5 test periods include no October–December days (D17). How do you read a test that opens in December?
- Coverage is below nominal everywhere. Why is "The nominal level … a reference, not a target" (D05)? Is recalibration planned?
- Running the weather six hours late raises point error by 14% (D14). What does the live system do when the weather run is late?
- On 33 days the forecast had a missing hour after a clock change (D10). Was that a pipeline defect, and is it fixed in the live product?
- The battery result is "Hourly, not quarter-hourly" (D11). How does the product handle 15-minute day-ahead products?
- What does "released" mean operationally, compared with "adopted in research"?
- What is "in-browser retraining" (D06)?
- Which parts did you build yourself and which did the AI agents build (D37)?

7. What would a battery have earned with v6's forecasts, against the naive forecast, with its numbers?

The headline (D08, P15): "one 1 MW / 2 MWh battery scheduled each day from v6's forecasts would have earned 257,212 EUR net, 0.8953 of what a perfect forecast would have earned (287,292 EUR). Scheduled from the similar-day naive's forecasts, it would have earned 220,136 EUR, 0.7662 of it."

- The paired difference (D09, P17): "v6's profit minus the naive's, summed over the days, is +37,080 EUR [+32,320, +42,310]", a 95% interval from 14-day block resampling.
- The setup (D10): 85% round trip, one cycle a day, empty at the start and end of each day, wear of €25 per MWh, fees of €0.10 per MWh, and the median rule.
- Trading days (D10): v6's schedule traded on 1,770 of the 2,068 days. On 33 days the forecast was missing an hour and the day counts as zero profit; the naive's schedule lost 11 days that way.
- Losses (D10): v6's schedule lost money on 137 days, at most 97 EUR in a day, with a worst fall of 136 EUR below an earlier peak. The naive's lost on 355 days, at most 227 EUR in a day.
- Wear-cost sensitivity (D10): with no wear cost, 356,333 EUR (0.9210 of perfect); at €50 per MWh, 176,202 EUR (0.8495).
- By regime (D10): 0.6445 of perfect before the crisis, 0.8775 in it, and 0.9118 from 2023.
- The cautious rule (D10–D11): 247,436 EUR (0.8613), trading on 1,457 days and losing on 39.
- Against v5 on 358 days (D11): 55,708 against 55,544 EUR, "+165 EUR [−727, +1,032] … no advantage either way is shown."

8. What does that battery result not show?

D08: "Simulated, development, post-selection: no money was traded, and v6 was chosen on these same days, so its result is optimistic for it. Not realized income and not a trading recommendation."

D11 lists the rest:
- "Hourly, not quarter-hourly. Not a property of v6 alone … Not 4.7T's result and not a forecast of future profit. No return or payback is computed: there is no capital cost."
- Assumed, not modelled: the battery is a price-taker and never out of service; the wear and fee figures are assumptions; the grid-fee exemption "may change".
- Not evaluated: intraday trading, balancing or reserves; a real battery's own costs; and "not the live product's forecasts, so the report shows no live or prospective profit. Lower forecast error and interval coverage are not profit, and not a success rate of any decision."

It also does not show:
- That v6 earns more than v5 (D11).
- How the result would carry to other days: the interval is "of these days, not a forecast for other days" (D09).
- How large an allowance a decision should make for forecast misses: "how to size that allowance has not been evaluated" (D08).

Things that confused me:

- D01/P01: There are two boxes, "Live product v6" and "Final candidate · pending 4.7T", while v1 is "the last released generation". Whether v6 is live, released or pending is unclear at first.
- D01: "4.7T" is an opaque name. It is described only as "its one test on new data: 90 days registered in advance" (D02).
- D01: "The Owner, the project's lead" reads as if it were someone other than "Led by Yarden Viktor Dejorno".
- D01: The performance line ("0.55 MB … 1.86 s … served locally on development data") is out of place and not measured on the live site.
- D01/D12/D13: The headline numbers differ: −7% versus −6%, and "7 candidate policies tested" versus "25 policies were tested" versus "13 policies drawn".
- D02 vs D12: "Point and interval error" (EUR/MWh) and "error scores" (ratios to the naive) have similar names but are different measures. The interval width behind "interval score/error" is never stated.
- D02: "re-baseline" and "A1 in the frozen records" appear without definition. The selection rule itself is only a link.
- D02/P03: All topic cards are collapsed, so "Where it fails", "Limitations" and "Run and check this product" are not visible.
- D05: "The nominal level is a reference, not a target" does not fit an interval product that undercovers.
- D06/D08: "in-browser retraining" and "the retraining probe's native reference" are not explained.
- D07: "v5's test periods … (four periods …)": v5 has five. 358 days here versus 448 days (D12) is not reconciled on the spot.
- D09/P16: "policy identity 720fc581…" is a hash shown as jargon. The +37,080 figure is presumably 257,212 − 220,136 = 37,076, rounded.
- D10: The 33 clock-change days with a missing hour suggest a pipeline defect. It is unclear whether the accuracy averages include them.
- D13 vs D15 vs D34: v1 against the naive appears as 1.052, 1.0126 and "28.58% worse". There are three numbers for apparently related things.
- D16/D22: "frozen on 2026-10-28 and re-frozen on 2026-10-29 and 2026-10-30" gives no reason. "It was selected by its own rule, never adopted by v5's" is hard to parse.
- D17/D25 vs D03: The "end of the development period" is 2026-04-07 in one place and 2026-09-06 in the other.
- D22: "Its forecasts cover the first period, 2020, though that protocol's scores began after it" is unclear. So is why the same arm scored better (0.4785/0.4271) under v5's protocol.
- D36: "Dashed outlines mark planned parts", but no dashed outlines are visible in the cards in D35.
- D37: "the trained champion" is not defined. Which model is it?
- P09: The phone coverage table shows only the 50% columns; the other columns are cut off with no scroll hint.
- P13–P14: The phone bin table shows only Bin, Hours, from and to. The mean forecast, mean observed price and 80% share columns are hidden.
- P28: The phone policy table shows only point error. The ratio column is clipped ("Ratio to th"), and the interval columns are not visible.
```

## The answers against the records

| Answer | Quoted | Record | Agrees |
|---|---|---|---|
| 1 | −7% [−9%, −5%], −11% [−13%, −9%]; 2,068 days; 7 candidate policies | `derived.cp28.A1.{MAE,WIS}`, `cp28.paired_dates`, `derived.cp28.tested` | yes |
| 1 | 17.2 [15.4, 19.1] against 34.6; 51.7 wide, 0.7826 | `pres6.regime.all.MAE.{v6,naive}`; `pres6.coverage.all.80.*` | yes |
| 1, 2 | −6% [−9%, −2%], −11% [−15%, −8%]; 0.493, 0.437; −51%, −56% | `derived.change.v6.*`; `pres5.metrics.A1.equal_fold.*` | yes; the reader read "The headline's −7% is another population" as intended (O51 item 8) |
| 3 | development, post-selection; "descriptive intervals: not the rule's own test"; 4.7T no earlier than 2026-12-04 | the class; `terms.class_final` (editorial E2); 4.7T's registered calendar | yes: the reader read "descriptive" from the term directly below the headline |
| 4 | the Space runs v6 before its one test; v1 the last released generation | the registry's statuses (O13, O27) | yes |
| 5 | the experiments not adopted, with their scores | the registry; `cp24`, `cp22` records | yes |
| 7 | 257,212 (0.8953) against 220,136 (0.7662), 287,292; +37,080 [+32,320, +42,310]; losses 137, 97, 136 and 355, 227; €0 356,333 (0.9210), €50 176,202 (0.8495); regimes 0.6445, 0.8775, 0.9118; cautious 247,436 (0.8613), 1,457, 39; v5 55,708 against 55,544, +165 [−727, +1,032] | `cp29.*` (`summary.csv`, `paired.csv`) | yes, each at its displayed rounding |
| 8 | the class; hourly; not v6 alone; not 4.7T's; not a forecast of future profit; no return; the assumptions; not evaluated | C1108, C1204, `business.gap` | yes: every limit the brief names (§9.1) |

## Dispositions

**Repaired after the reading** (PRES-7's text; in the commit after `5575920c`):

| Observation | Disposition |
|---|---|
| D07 and Business insights' v6-against-v5 block: "v5's test periods" for 358 days, though v5 has five periods and 448 days | **Repaired in PRES-7's block** (C1104): "On the 358 days of v5's last four test periods (the eligible days inside them)". D07 itself (Product results' bins) is PRES-6's and unchanged; open item |
| D10: the 33 missing-hour days "suggest a pipeline defect" | **Repaired** (C1202): "the forecast was missing one hour by design (its input rules fail closed there)" |

**Answered, kept:**
- "The Owner, the project's lead" beside "Led by Yarden Viktor Dejorno": they are the same person, and the definition
  says so; a longer one would add a phone line above the product finding (A2, packet §10.2).
- "re-baseline" and "A1" (D02): both are defined at first use, in the terms directly below the headline ("before the
  re-baseline re-scored every policy on every day"; "v6 (named A1 in the frozen records)"); the reader's answers 1–3
  use both correctly.
- −7% against −6% and the counts (D01, D12, D13): reconciled where they meet ("The headline's −7% is another
  population"; "7 candidate policies tested", "13 policies drawn", "25 policies were tested against them"), as O51 item
  8 asked; the reader's answer 1 reports the reconciliation.
- The policy identity `720fc581…` (D09): kept, as packet §0 committed the graphic to name it (editorial A5); How the
  product works shows the same identity.
- +37,080 against 257,212 − 220,136 = 37,076: the paired total is the difference's own record, shown to four
  significant figures (editorial E6); the reader's reading is right.

**Outside PRES-7's sections** (unchanged by the brief), passed to the Orchestrator (packet §10.3): the live/final
candidate badges; "4.7T" as a name; the page-load line; "point error" against "error score"; the collapsed topic
cards; "the nominal level is a reference, not a target"; "in-browser retraining"; v1's three numbers; the re-freeze
dates; "Its forecasts cover the first period"; the planned-parts outlines; "the trained champion"; the phone tables'
hidden columns (P09, P13–P14, P28; they scroll sideways by design).

## Screen hashes (SHA-256)

```text
947950eeaef9188dde3e46945686f40ce197eedf6a802448975f44f7fe966a62  D01.png
597d3afa41966a98f9d1da7cc50c416fc7f799c3c820929cacd079e8994ffbe2  D02.png
c5bf93d0e1caf48c8e1a8e661fe17492511aea97490628f154322f07278a0010  D03.png
dd3a163ed9025fb9431b8961eafa7d449e73de44d3043d3e48afaa564634f978  D04.png
7dd82f07bdb04dc1787a42bf7eaa407aee686055f31600a9e9e610ee498b5053  D05.png
557d431d2c26a66af623745d151c95993c8f07ca51e40db5283e01d0eb237b7d  D06.png
6b343ed8f4df688bbe5f83e42894874739bb36626ad167de90f1098668f0e495  D07.png
0528affc3d5cf1a8b3de8ade2eb5d5747d94f3bf07e0aa5c55404bae148b63fa  D08.png
2e4c54cb04a6bf98c1189c65c444437dbfb520482ea63b39b12a63d37502e026  D09.png
496f04dfcc18a5a4287f3b2dabdd46a74680e479385aa3de78ad761fe13fae70  D10.png
691c202fa5912e7ce659edb12598b84e9dc4903aba088958e76ada22047e8e73  D11.png
f9c0e317c8234fa296233ebc61f93c9c7b3ec391f0fedce5f4462bb4af5173e8  D12.png
87941ff92da5a8feb99679019d59c0db12b7430e7bc5c1e9a4c5f6dfb3a8b941  D13.png
724350033cb54bf9315ad8a49a5979cb64de1f93f1d49f8f6516df54ac040193  D14.png
d8bb3e8c929188a247ea3b8d968b358a9c189b14473e3753234687d0ac98e4b1  D15.png
02827d30f54b1e93759f030cceb232b402d61d8163227d21d2386971b4773d00  D16.png
84baa9eead2d2838b7bf90325454d1688fef9c4404030e5bb55067fdd1ebaea6  D17.png
c6e6487cf59fc7fded314f6f09946b8e9d0904ff403f36a625f70b0d6b800ccd  D18.png
8a5ac6f1797cc7d7402a041b0361ca319d9b7d606e2ba1ca74b1231d7634f947  D19.png
c97878702401a2eee149c7b5405cfb2f7717aef6550c0d7177230d15d0f68982  D20.png
5f5683546cb4ef0ce9dc9ad09f493e8972c1f98e5e4d40e0b29e53cb69aa7bce  D21.png
2cc53516a9ddfc049758b087aa59511b7753237552e2f2255b40008f04ccdffc  D22.png
2d89f9a88d2fdf6af9f46d09effa192bcd786c07da781204dd889a7b54d90fd3  D23.png
d1c2ebf5caf80fbe4cbf6bc0c9b80cef31a7a0cf09a9597886b173432ddde913  D24.png
cc512b0e11d3c514701376b5786087819644e2314769c204476820c8d6d554bc  D25.png
b15aee41e2e5bbedb72b5e5efc9ee2f38268e2d6eb21f4fb47ff9553f991d6e9  D26.png
8fea3973d6efaf88d0d4d1b943b582eacdd80356101e3d3daf2ae563c63c9771  D27.png
10c3cdb821944da47b261ee148d9af7d8d5227cf908d4b6cddf050910e29195e  D28.png
f8406b686803a0ecaeb11c39e5cb3486dd9d8ea04693bb0498cb17729e43d2b2  D29.png
ccdd92ffe2486a002d37245f45e908f63e5741f4847297d04ef19d838e5c573c  D30.png
f6271f9573860fff7b37bcb22078e6e92bc597f537936b9ca2d0595fb0ed03f5  D31.png
d17b9f76790d664eeabccd9dd3cc53b62ec382acab3654a330975ab6b4e92d12  D32.png
a4905e359949dca744e372204eda289ab5fe73841032c654ce0cd74547812462  D33.png
bb4bb582a73d512cec443abf5d7ba3fbe17fa24cc27f4abc578f317e18acf659  D34.png
59bb77fba1518c51cc11e276f191868ed74202bc0306a5d2ebc462440494f666  D35.png
b1a838bf9922af4ab63b4c0967bd99ce96bb9dfdfe7ff55c9d01dda88fcdeed8  D36.png
6109d1ec7bd119fd14ad8fa835efc6fb7f5f064e6b9e180a825d97df793ed3e8  D37.png
5195c6adab5ad87fa2a8d60834ec3b28e14ff1609edb48ac9ba73120351f728b  D38.png
ddc103bf7dfd9dd47243c6f8a624b28400926f9213985b9f37c277ab915972e7  P01.png
20d8c0193aaa168ab02fd48c680aad6d673d42d454c7ead0c4b1ac1a77ce2837  P02.png
7e951a9a5df7aba7953d48ecebc4dd3f0f089aa5276da53c0fad4f54c8c6baf5  P03.png
4c9cef7c010b6a49f25495c6fb11e53bf7231c0a19b05d8ef12a92091b5f1a5b  P04.png
d3559451f8152430b0c2dabf16d8eca4ad7bbaa8856e7faf9e040881e3bccfe8  P05.png
cb2af6287f02dd68a2507345a38c24c5a75288d883ec3c51ae49fb8c395187b6  P06.png
3c753833e9d3bf76a74ceba4b496b2df48e94bfd22501fcea2ba949d1b5451a5  P07.png
3b76a9f77fd140026a15f3607130858a267f882b8837132e3605f43daadab02c  P08.png
2a1fea808556caceb8846e0c1a65daa4be25ac4e02402f197b78574d69092fee  P09.png
e4136f22e3cac252374dfb1fb944275311f139cde9ac4fb25c04b2c3b35a21e3  P10.png
6a9ca2b6958ab083e0e50860d901b8696d85654846621bd70e57414d98c7c886  P11.png
c913da6033747fddc4346713db47ac2729da1841e7812b4e0ed01d7171b058ad  P12.png
e772db6f8ad59574f8ac0769753e3a82a848d4e67b0f21b41003c549204569f7  P13.png
16b776bd1e32688433ce0bcb07e06f064a46b1cb5818934bbc52d36abe182f1b  P14.png
7269070169b5382dd72c128c643adda9c05950cbca9c002e0a2a4f99fe3682d6  P15.png
ceebac8763d83e9c40cdc320cb5bb68c5278787878bd708006a293583a17488b  P16.png
d765486b2520e00263d8e3f248eed2ab8b2412c9efc93e7f2faeb94625ad7d63  P17.png
473d7a687b30fcfa849d8944dd659bbd462ff460c59b71de1972fb5438495067  P18.png
696f385ed2a47884dcdd90e234f079cbfb94b41c3848df3681a82c6ba8037b01  P19.png
610feb3de07174d2d496cddb923d68a375963b7e67e5be91dc392ade00bda28e  P20.png
997a95f3d8dfb9e5ba82e48037bde3c58fd0db14c8f6f15f74f9cc0bf117cdd4  P21.png
f1736f487fdd6f0624b3be5be4974d268dc394f4c53dcfead35a738e06c1b816  P22.png
b1bc0fe0406de113272329b68de3da1dfab5581aaa3c2edf340c0cf9a2bade28  P23.png
e8c69810f507b624dd252770dca09c47edf5323c03742d9c696dccf8418793aa  P24.png
a77afb2f842934d83a7f69cb7d3332909c7c4f44f3f3605733835edccd73b4dd  P25.png
e21681209f7f45e62d7104a308e764030297c4346f64fd9c35568a78e76c883e  P26.png
03a875779177bdf6e36181739d1455d791134a2184cbc7bc4370b035a327a35d  P27.png
a517de4c122f7ed17dbfb46d6745afc069a2c882b30bf6d2ffbfeec7c5aa1ea5  P28.png
2c8048d154e8fccfea77d58a48c5ba63ab32a4bc00b83904433add73e024cb44  P29.png
a65013c9cd8d1e2fe22b36962c1004250ad6c2d4b0eb96823f04083b21a9fef5  P30.png
e82e0aad431c9c1f5057be71adec04f93eb1f755e8f9d4ef5d2191fadb722178  P31.png
9197933ff2541ac0f12bd19d860da3c80ae8a75f026f8da0fe324e88345ae44f  P32.png
8772c17e86191a036a7584733dfa40889d1325c2c8881584d687a943322a96e4  P33.png
8e167cb999cdf9a9ce1964578ab6d16d75301ca61329b7c358c99b2858eba761  P34.png
56634273fb379d183e0eeda5af220c57bfe52c5567a40f1fe3f8e48111193e70  P35.png
1268aee147297dd91578ab866911d992d1b2c7223430fcb5db65419bbe0c6052  P36.png
080f2a9dd1aaf10eeb07f28d32d220c38633a9c702b0ec98e07329294ae4a502  P37.png
aea65f886e3558ab7d4a0f3b3159760467d15bdb5e1373e058834c620f33c725  P38.png
9aff5d5dd68e6f32cb8a8c3850ff21b270462d0312c5b41bcf97e5b225cab588  P39.png
60502d45b297173bee65ca1a6042aab19570a352111c705fee067c5089c07eae  P40.png
bcc212c605d82bbc6b43b63a5db4ca120df14575bc9a84cead205a07693d0c7d  P41.png
ec290a2a2e2a5292160da96c13c9854f53deebf152b67766bf33836abe91a521  P42.png
3f25916789844137750d3f5dfac2355088a6bb021c9bab5623316d3d7a2f4bd4  P43.png
64a32f0bb7cc0f25b114cc64fbb62857cd4c7aebe85d1cefc1723a43087036c4  P44.png
6ef921aa8aacd3e3e2f0f10583761e9184ee061a682797b9fafdceaf97262be3  P45.png
7cf926a01e2e42fa01cc8b23caa7a054b933f36db7a5f6da524ebb3f018afd39  P46.png
3c94a0a511d8da355e0979c2765b3cc4b7d5eff4a74aeb92e250a0464484a941  P47.png
da9b9edcc9558fd3b841805f33bc84ca5ff091242553b6954f92a5fa1f62a2fe  P48.png
1d08424930203a42cab7d2db577279eb7315dc2713418c4c3673d79402113b09  P49.png
ee04b453e0941be0d4dcc39ea895eb2ae7dcd67f31e295d93680fec395655685  P50.png
be35109cada3d1ea46026f8fecae07209067c410a1d6892bcda97d8f20b6d731  P51.png
ec1004fbd561f749a3fff26c814f020a5e2dd10635ef9b77198051be1cf689a4  P52.png
7aeb70327e08f55b794260311a926d6212bb17ecbfc4c7f558b25c7409f662d6  P53.png
c8c72f3b3a7cb76812471046b7f479bc77273d8f8f1c9004784d23cb3a1189d7  P54.png
51c4777a3f99b554c1d6351e54ec2a832955e3799f23995efb1fee4f14cb2a12  P55.png
decf4d57bba61fcbf2de5bd36cd22d33fdb01e8255e769db69eb78f6741f9418  P56.png
58796310c26984686aedab0aa49315cd856617d7445c6536f4b652461457d3d2  P57.png
b58336ca0bb1d189885e17cb1dd133d5e908d8dbf0b27a048dc97ced76355e82  P58.png
3d2faf7a3a1038315a36edabbbf4bfdf633f3f9285c5fb6ba3e72c71788a76e2  P59.png
a482f16513f45cad8da6d24a5958a2a26057e00e856d787137dff5d86d4767ba  P60.png
de55d6c6312bed30f0c7ac56ee46eaab50fd8636887bd191dee537560690fc2c  P61.png
64a06a812dcb1047fa43af34db7f9886210d5e87799af388f9665fbd0c3ba887  P62.png
1a0c9cbc6435f05a3627a805068d052d7982f3ff6ec50aff4273b3dd53050326  P63.png
cc9700e920847f5f8f6fc4bf7b12849c3de5729b3368bd2344a7741cb14c6394  P64.png
c407bb41dd81f204240cfabd6316a0842654963ecc8022bb8d22378516e065a6  P65.png
000a390178ad0ba0ff5570fde045a5716096a17ae0f18b04085ad74650f82baf  P66.png
2a17496c180db5c8aeeb27bc5bd9ee43c8e934885cecf67fa3a7aaf5c5972f2f  P67.png
```
