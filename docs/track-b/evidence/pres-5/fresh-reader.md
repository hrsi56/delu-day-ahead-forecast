# PRES-5 — fresh reader (PUBLISH_RULES 1.5 §10.2)

**Outcome: answers 1–5 agree with the registry, the evidence records and the derived records.** Every number the
reader quoted equals its record. Two gaps on the reading path were found and repaired after the reading (observations
1 and 2 below); the rest of the observations, and answer 6, are advisory and dispositioned below.

## How it was run

- **Page:** `docs/index.html` at `b20ee9d1dbfa052e687bd9338270435ad155db5d`, SHA-256
  `a27564eaa52f79a7674457dcb07a58fdf54bae9a19885275a39b96dada2f4d37`, opened from the file with every disclosure closed.
- **Screens:** written by `scripts/check_reader_paths.py release` (the local record
  `.local/artifacts/pres-5/local-release-2.json`, `cold_reader_screens`, 2026-11-06 13:09 UTC), the page as a reader
  scrolls it, one viewport at a time, each step the viewport less the 56 px sticky header:
  - desktop, Google Chrome 156.0.8078.80 at 1440×900, 28 screens, step 844 px, supplied as D01–D28;
  - phone, Playwright WebKit 26.6 at 390×844, 48 screens, step 788 px, supplied as P01–P48.
  They were copied under neutral names to `/Users/djourno/Downloads/PJM/.local/tmp/pres-5/fresh-reader/` (local only);
  their SHA-256 values are listed at the end.
- **Reader:** one fresh agent. It wrote nothing in PRES-5 and was given no repository, project history, prior review,
  expected answers, chart locations or explanation: only the prompt below. Its record shows 76 tool calls, one read of
  each named image. Its transcript was not otherwise inspected.
- **Date:** 2026-11-12. The reading ran after the editorial review had started and before its repairs.

### The prompt (verbatim, except that the 76 image paths are abbreviated)

The prompt's first line is the Orchestrator's standing rule for every launched agent (no access to the Claude memory
directory); the rest is §10.2's unchanged form.

```text
FIRST RULE: do not open, read or edit any file in /Users/djourno/.claude/projects/-Users-djourno-Downloads-PJM/memory/ (the Claude memory directory).

You are a reader seeing a web page for the first time. You have no other information about it, and you must not look for any: do not open, list or search any file or directory other than the 76 image files named below, do not run any command, and do not use the web.

The page is shown as screenshots taken while scrolling from the top to the bottom, with every collapsible section closed. There are two renderings of the same page: first a desktop browser (1440 × 900), screens D01 to D28; then a phone browser (390 × 844), screens P01 to P48. Read every one of them, in this order, with the Read tool:

/Users/djourno/Downloads/PJM/.local/tmp/pres-5/fresh-reader/D01.png
[… the 76 paths, D01.png to D28.png, then P01.png to P48.png, one per line …]
/Users/djourno/Downloads/PJM/.local/tmp/pres-5/fresh-reader/P48.png

Read as an experienced data-science lead would, then answer these six questions. For questions 1 to 5, cite the screen or screens (for example D02 or P05) and quote the words you rely on. If something is unclear or missing, say so rather than guessing.

1. What is the headline result, with its numbers?
2. Against what?
3. How sure are we, and on what class of evidence?
4. What does the demo run, and why not the best model?
5. What was tried and dropped?
6. What would you ask the candidate?

After the six answers, list anything that confused you, each with the screen where it happened.

Reply with your answers only, as plain text.
```

## The reader's answers (verbatim)

```text
1. What is the headline result, with its numbers?

The headline is that v6, "DDNN-2 alone" (a distributional neural network, refitted daily), beats the previous research generation v5 on both point and interval error.
- Hero (D01, P01): "against v5 on all 2,068 development days, –7% [–9%, –5%] in point error and –11% [–13%, –9%] in interval error; 7 policies tested against the rule."
- Second version, on five historical test periods (D02, P03): "–6% [–9%, –2%] on the point-error score and –11% [–15%, –8%] on the interval score, with 95% confidence intervals." D11 adds the 97.5% level: "[–10%, –2%] and [–15%, –8%]".
- Ratio to the similar-day naive forecast (D03, P05, P06): v6 scores "0.493" on points and "0.437" on intervals. v5 scores 0.522 / 0.494 and daily LEAR 0.658 / 0.639.
- Against the naive directly (D12): "–51% [–54%, –46%] on the point-error score and –56% [–59%, –52%] on the interval score".
- Absolute errors (D04, P08): "v6 4.5–13.4 EUR/MWh in the four ordinary periods and 43.2 EUR/MWh in the 2022 crisis period; the similar-day naive 8.6–30.5 and 86.9 EUR/MWh."
- Every-day table (D05): v6 point error "17.2" EUR/MWh (ratio 0.4974) and interval error "9.7" (ratio 0.4580). v5 is 18.5 / 10.9.

2. Against what?

- The main comparator is v5, set in advance: "Set in advance: v5 itself, the control of the selection rule, so the comparator is the predecessor" (D07, P12). v5 is "two LEAR forecasts and a LightGBM, five sixths of the weight; DDNN-2, one sixth" (D11).
- All scores are ratios to a naive forecast: "Each score divides a model's error by that of a simple similar-day forecast in the same period, which therefore scores 1.000" (D04).
- The strongest benchmark is "Daily LEAR: the strongest benchmark, a linear model refitted daily" (D03). The accuracy targets are "each error score at least 10% below the strongest benchmark's, set on 2026-09-15" (D03).
- v6 itself was not judged against those targets: "v6 · DDNN-2 alone was tested by its own selection rule, on every development day, not against the targets" (D04, P07).
- The released v1 is shown too, at "1.052" / "0.986" (D04). On development replay it is no better than the naive on point error.
- I saw no comparison with external or published DE-LU forecasting results beyond LEAR and LightGBM benchmarks the project built itself.

3. How sure are we, and on what class of evidence?

The evidence class is development data, judged after selection. Nothing has been tested on new data yet.
- The page says so itself: "Development · post-selection: development evidence, not a test on new data" (D01, P01), repeated on every chapter.
- The uncertainty is paired bootstrap confidence intervals. On the five periods: "both paired differences lie below zero, at 95% and at 97.5%" (D12). "A description, not a decision: v5's adoption rule was not re-run" (D12).
- The 2,068-day figures are called "descriptive 95% intervals" (D07). Elsewhere the same figures are called "a point comparison: –7% and –11%" (D05).
- Selection was not clean of the data:
  - "v6 was selected on every development day, four of these periods among them, after DDNN-2 alone had already scored best there" (D12, P23).
  - The rule picked "arm A1, now v6, among 7 arms" (D07).
  - The same five periods were reused: "the second decision on a distributional neural network over the same five test periods" (D15).
- The protocols differ. v6's forecasts were "issued one or two hours earlier, refitted every day, with its own network searches and data identity" (D12).
- Seasonal coverage is thin: "448 of the 2,654 days … 0 of them fall in October to December, and only 1 winter" (D15). That is stated for v5, but the same five periods apply to v6.
- One warning sign is already on the page. v5's five-period gain over v4 did not hold on every day: "v5 against v4: –1% [–1%, +1%] … the five periods' gain does not carry over to every day" (D05).
- The only test on new data is still in the future: "4.7T, on 90 days whose data was opened only after its registration, is its one test" (D12), "opening no earlier than 2026-12-04" (D25). Live results: "prospective evaluation in progress" (D01), with no numbers shown.
- The only near-confirmatory evidence on the page is for v1, not v6: "Confirmatory-style, not power-qualified" (D24). v1 had "MAE 25.9 against 27.8 EUR/MWh" and a Diebold–Mariano test gave "p < 10⁻⁶".

4. What does the demo run, and why not the best model?

- The live Space runs v6: "The Space runs v6 · DDNN-2 alone daily, frozen: prospective evaluation in progress" (D01, P02). The header says "Live product v6 · DDNN-2 alone" (D01).
- v6 is also the best-scoring model on every chart shown, so for the live Space the "why not the best model" question does not really arise.
- The chart on the landing page is not live: "A stored forecast for a development day, with the observed price; not a live forecast" (D01). It is dated 2026-04-07.
- The historical demo and the formal release are v1, the weakest model: "v1, the last released generation, is its historical demo, and the product again if 4.7T fails" (D01). v1 is "Released · September 2026" (D06).
- The page implies v6 is not released because 4.7T has not happened. v2–v5 were only "Adopted in research", with "the released model, v1, did not change" (D08).
- The page does not explain why none of v2–v5 was ever released.
- It also does not explain why the fallback if 4.7T fails is v1 (1.052 against the naive) rather than v5 (0.522).

5. What was tried and dropped?

- Calibration experiment, September 2026: "Recalibration alone was not enough: the model itself had to adapt" (D10, P19).
- Model comparison study, September 2026: "No policy met the criteria; the study informed v2's blend of two LEAR forecasts" (D10).
- Pooled LightGBM member for v4 (the averaged pooled member and the pooled pair), October 2026: "Both candidates were decisively worse than v4 in one test period, with a 95% interval wholly above zero; the rule allowed none" (D10). Overall they scored 0.537/0.507 and 0.534/0.505, against v4's 0.536/0.506 (D03).
- DDNN member on v4, October 2026: "The improvement over v4 that the rule required was not shown, on either score" (D10). It scored 0.542/0.513 (D03).
- Study arms that were never candidates:
  - "Normalized LEAR (study)" 0.672/0.646 (D03).
  - v4's "three study arms" (D08).
  - v5's arms "DDNN-2 alone and v3 plus a DDNN-2 member … never candidates for adoption" (D08). DDNN-2 alone later came back as v6.
  - v2's pooled-interval control (D22).
- Components dropped going from v5 to v6: "v5's two LEAR forecasts, its LightGBM and the blend are dropped" (D06).
- The v1 approach was replaced: "v2 replaced its LightGBM quantile model and fixed-window calibration" (D09).
- The other six of the "7 arms" in v6's selection (D07) are not named or described anywhere I could see.

6. What would you ask the candidate?

- If 4.7T fails, why fall back to v1, which is worse than the naive on development replay, rather than v5 or v4? And why were v2–v5 never released?
- The selection rule was set on 2026-10-12, after DDNN-2 alone had already won as a v5 study arm. How independent was the rule? What were the other six arms? Was there any correction for multiple comparisons?
- v5's gain over v4 disappeared on the every-day re-baseline. Why should I trust five-period gains at all, and what does that imply for v6?
- How much of v6's gain comes from the daily refit, the 728-day window, the earlier issue time and its own network searches, rather than from the model? Is the 2,068-day comparison fully like-for-like?
- DDNN-2 itself:
  - What distribution and architecture does it use?
  - How was the hyperparameter search done?
  - How much do results vary across seeds?
  - Was the search nested inside the evaluation?
- How well calibrated are v6's 80% and 95% intervals in each period, especially in the 2022 crisis and around negative prices?
- v5 degraded by 14–15% with the weather run six hours late. Is v6 equally exposed, and what happens operationally when GFS is late?
- 4.7T:
  - What exactly is the pass criterion, and what effect can 90 days detect?
  - The window falls in winter, which development data barely covers. How does that affect the result?
- Is there any decision-value metric (trading or procurement cost), or only statistical scores?
- The page says "AI agents assisted with implementation, analysis and documentation" (D27). What did you personally build and verify, and how did you check the agents' work?

Things that confused me:

- Is the –7% / –11% result a point comparison or does it have intervals? D01 gives intervals, D05 says "a point comparison: –7% and –11% against v5", and D07 says "descriptive 95% intervals".
- There are two different v6-vs-v5 headlines on two populations (–7%/–11% in D01, –6%/–11% in D02), and the reader has to work out which is primary. "Point error" (daily mean absolute error of the median, D01) and "point-error score" (ratio to the naive, D03) are easy to mix up.
- "Live product: v6" sits beside "v1, the last released generation" and "Final candidate · pending 4.7T", while "Open the live product" leads to a chart marked "not a live forecast" (D01). I could not tell what is actually in production.
- "4.7T" is never spelled out (D01, D07, D25). "A1 in the frozen records", "arms", "policies", "declared routes" (D05) and "folds" (D06, which says "called folds below" but nothing visible below uses the word) are jargon left undefined.
- The counts don't line up: "7 policies tested against the rule" (D01), "13 policies" in the chart (D03), and "25 policies were tested against them … 16 later policies met them too" (D04).
- The development period has two different ends: "up to the end of the development period, 2019-01-01 to 2026-04-07" (D07, D15) against "2,068 eligible days from 2020-12-29 to 2026-09-06" (D05).
- v1's development error has two different numbers: "28.58% worse than the naive's, pooled over all days" (D24) against 1.052 (about 5% worse) in the chart (D04). They are not reconciled.
- D12 says "the first period, 2020, lies in that protocol's unscored warm-up", yet v6 is scored on all five periods (D11). I could not see where v6's 2020 forecasts come from.
- "Selection rule: set on 2026-10-12, before any result" (D01) reads oddly next to "after DDNN-2 alone had already scored best there" (D12).
- v6 is reported at v5's 97.5% rule level (D11), but the page also says "v5's adoption rule was not re-run" (D12). Why use that level?
- "frozen on 2026-10-28 and re-frozen, unchanged, on 2026-10-30" (D07): why re-frozen?
- The interval score's nominal level is never stated in visible text. The chart shows an 80% interval (D01), v1 has "50 / 80 / 95%" (D24), and v3 reports pooled 95% coverage (D20). v6's coverage is not visible with sections closed (D13).
- "Pooled member, averaged: one LightGBM for all 24 hours, averaged over four sizes" (D03): I could not tell what the four sizes are.
- "It opens with about 0.55 MB of the day's records … the training window loads on request" (D01) means little to a first-time reader.
- "v1's stays in its chapter" is a fragment (D02, P03).
- "Normalized LEAR" is never defined (D03, D22).
- On the phone, the every-day table is cut off at the right edge with no scroll cue: "Ratio to th" is visible, the interval columns are not (P09, P10).
- On the phone, v6's marker in the interval-score chart is clipped at the left edge next to "0.437" (P06).
- With sections closed, all method detail is hidden: bootstrap settings, the five periods' dates, and the stress-period and coverage results (D06, D13, D16).
```

## Grading: answers 1–5 against the registry and the records

A desktop screen n covers document pixels from (n − 1) × 844 for 900 px; a phone screen n from (n − 1) × 788 for
844 px. At the page read, the headline block ended at 774.6 px (desktop) and 604.6 px (phone); the finding at
1,672.6 px (A2 limit 1,744) and 2,400.5 px (limit 2,420), in Chrome and WebKit alike.

| Question | What the registry and the records hold | The reader | Within the placement rules |
|---|---|---|---|
| 1. The headline result, with its numbers | v6 met `cp28-selection` (`derived.cp28.tested` = 7); against v5 on 2,068 development days −7% [−9%, −5%] (MAE) and −11% [−13%, −9%] (WIS) (`derived.cp28.A1.*`); on v5's five periods −6% [−9%, −2%] and −11% [−15%, −8%] at 95%, [−10%, −2%] and [−15%, −8%] at 97.5% (`derived.change.v6.*`, `derived.change_decision.v6.*`); against the naive −51% and −56% (`derived.change_naive.v6.*`); scores 0.4928 / 0.4374 (`pres5.metrics.A1.equal_fold.*`); per-period MAE 4.5–13.4 and 43.2 EUR/MWh (`derived.periods.v6.*`) | All of it, each number with its metric and population (D01/P01, D02/P03, D03, D04/P08, D11, D12), plus the every-day table's EUR/MWh values | Yes. **A1:** each value named by its metric on the first screen |
| 2. Against what? | v5, set in advance as the selection rule's control, which is the predecessor; the naive as normalizer; daily LEAR as the targets' benchmark; v6 not tested against the targets | All of these (D07/P12, D04, D03, D04/P07) | Yes |
| 3. How sure, and on what evidence | Development · post-selection; descriptive intervals; selection after DDNN-2 alone scored best (C905); a different, later daily protocol (C904); the five periods' reuse and coverage limits; 4.7T the one test, from 2026-12-04; nothing live shown | All of these, with quotes (D01/P01, D07, D12/P23, D15, D25) | Yes. It noted that the every-day panel called the same −7% / −11% "a point comparison" while the headline gives intervals: observation 1, repaired |
| 4. What the demo runs, and why not the best model | The live Space runs v6, the final candidate, "prospective evaluation in progress"; v1 the last released generation, its demo historical, the product again if 4.7T does not pass; the opening's chart a stored development forecast, not live | All of it (D01/P02, D06, D08) | Yes. It asked why the release falls back to v1 rather than v5: answered by decision 21 in v6's chapter (`v6.fresh.meaning`), and the opening now says why the Space runs v6 before its test (editorial V2) |
| 5. What was tried and dropped | The calibration experiment and the model comparison study; CP-22's two candidates and CP-23's candidate, not adopted; v5's and v4's study arms; normalized LEAR; v2's control; v5's components dropped by v6; CP-28's six other arms, which passed every gate and were not selected | All of these except CP-28's six other arms, which it said were "not named or described anywhere I could see" (D07) | **No, for the six arms:** they were only in a closed disclosure (the arms table). Observation 2, repaired: `v6.decision` now names them on the reading path |

Answer 6 is advisory. It asks about the fallback to v1; the rule's independence from DDNN-2 alone's earlier result
and the multiplicity correction (stated in `v6.holm.note`); why five-period gains should be trusted after the
every-day re-baseline; how much of v6's gain comes from the daily protocol; DDNN-2's architecture, search and seeds;
calibration by period; exposure to a late weather run; 4.7T's power in a winter window; decision value; and the
candidate's own part against the AI agents'.

## Observations and dispositions

1. **"Point comparison" against "descriptive 95% intervals" for the same −7% / −11% (D01, D05, D07).** A real
   inconsistency: the every-day panel cited CP-26's point ratios while the headline cites CP-28's control ratios with
   their descriptive intervals — the same numbers. **Repaired** (`1d0f453e`): the panel's v6 clause
   (`everyday.finding.v6`, C604) now carries CP-28's descriptive 95% intervals.
2. **CP-28's six other arms not visible with sections closed (D07).** **Repaired:** `v6.decision` names them on the
   reading path ("the six others, blends of v5's members, also passed every gate and were not selected").
3. **"4.7T" never spelled out (D01, D07, D25).** **Repaired:** the final candidate's term now reads "frozen for 4.7T,
   its one test, on 90 days registered in advance".
4. **"v1's stays in its chapter" a fragment (D02, P03).** **Repaired:** the product lede no longer carries it.
5. **"It opens with about 0.55 MB of the day's records" means little (D01).** **Repaired** in part: the sentence now
   reads "It opens with about 0.55 MB, measured on development data; the training window loads on request." The
   missing measured start time is an open item (packet §10.3, item 4).
6. **The 2020 warm-up (D12).** **Repaired:** v6's information caveat now says its forecasts cover 2020 though the
   daily protocol's scores began after it.
7. **"Selection rule … before any result" next to "after DDNN-2 alone had already scored best" (D01, D12).** Both are
   true: the rule was registered before CP-26's first score, and the Owner chose to run it after seeing the
   re-baseline's report, which `v6.holm.note` discloses. No change.
8. **The 97.5% level when v5's rule was not re-run (D11, D12).** The brief requires "the rule's intervals"; the chart
   names the level as the one v5's rule decided at. No change.
9. **Live product beside "not a live forecast" (D01).** The preview is labelled as a stored development forecast; the
   primary action opens the live Space. The opening now also says why the Space runs v6 (editorial V2). No further
   change.
10. **Counts 7 / 13 / 25 (D01, D03, D04)** and **two development-period ends (D05, D07, D15).** Each is a different,
    labelled population or count (the rule's N, the comparison's rows, the targets' census; v5's data window and
    CP-26's eligible days). No change.
11. **v1's 1.052 against "28.58% worse" (D04, D24).** The archive's pooled figure and the comparison's equal-fold
    score are different aggregations; the archive is preserved as published. No change.
12. **v6's marker clipped at the left edge of the phone comparison (P06).** **Repaired:** the page's comparison axis
    starts at 0.4; the overview charts pinned in MLflow keep their axes.
13. **The every-day table cut off at the right on the phone (P09, P10).** The table sits in the page's standard
    horizontal-scroll region (keyboard-focusable, labelled), like every other wide table; no overflow of the page
    itself. No change.
14. **Undefined words: arms, policies, declared routes, folds, normalized LEAR, the interval score's level (D03–D07,
    D22).** "Declared routes" replaced by "sensitivity runs"; the rest are defined in the comparison's terms or the
    chapters' details. Advisory.
15. **Method detail hidden with sections closed (D06, D13, D16).** By design (§2: the reading path excludes closed
    disclosures; the details' routes are visible). No change.

## Continued applicability after the repairs

The repairs after the reading (`1d0f453e`) changed the opening's wording (the headline's label, the product line, the
final candidate's term, the lede, the startup line, the preview caption, the comparison's caveat), v6's decision and
the every-day panel. No answer quotes a sentence in a way the repairs contradict; the numbers and placements the
answers rely on are unchanged (the finding now ends at 1,672.6 px and 2,394.5 px). The reading stands for the
candidate, with observations 1–6 and 12 addressed.

## The screens' SHA-256

| Screen | SHA-256 |
|---|---|
| D01.png | `407116dcf74244c79d0c28e54e987bcea3192b6567a7d0a773d0757c857fe916` |
| D02.png | `52ed91ad8cd56c360b4226cc275199883db5a20f3f275f5b3407d5f7ad913d3e` |
| D03.png | `f8ec45fd036be1f537e60969c71e67319af0e88777a73e3f5abcc4974427fa17` |
| D04.png | `63683d60269644628bcf6cb73815f3f04545ce6743bb87bffd8ea3a96cf1650c` |
| D05.png | `4cd8e00ccd0e7f7a08e827ff49a42a044bb644510d85e854a2934a142b55eba8` |
| D06.png | `1d863930f491361cc33844ce749cf0bfdc4b3939454eb290a647ce4c4b5fba0c` |
| D07.png | `ddec58ffc87379b02789e0892ddd7d2c798d2711daf37cb435f48c543c887044` |
| D08.png | `d7ba138a7965d17fed1631f12a03936133984e9a025daf0b306b9ae462a13bf7` |
| D09.png | `e140d516226b4745a2014a8371dfc9ffa979dc95c86579c4c3627e4318ea1347` |
| D10.png | `fe157692f55b599fdf58d02b3ed0cd58dc917c60b2a1b97a26f31077c52fc121` |
| D11.png | `afe0b1d0cc6ef9ecc78c3e14d4d997ad47f8dc40653afbb6c0860fa55fa0c15d` |
| D12.png | `5efc747b816e93537eea45817a7976b4767d08fa3faa3f2844daa00beac318da` |
| D13.png | `e7264e6fb7f1ce49fa09e99a86f1ae313e5ef94a279315a6269aceafd256be2c` |
| D14.png | `63fb0710e9e08b772704dcd85395196bbbb878c87e01fd626bc7d25f1a94bd4e` |
| D15.png | `031d19434c1f541a4b3b63fab61a1ff88282b18bb477339cdd1bfe5b3c882fb2` |
| D16.png | `e6fff3aae2e18c67733fa9eb406a02d3a5a84a4b644c58d997cac38ed705662e` |
| D17.png | `fbc088100993c7219fe7f7e1b9236bd2c63a3c4384a2d26583d5629fdf2e915b` |
| D18.png | `f56c42335951679dbdbc7c616583c7d3b686fbdd805cf1cb5268e953ea1e3854` |
| D19.png | `44bfc3195a5318ad82e8d2b36fbea8f3affd2d48dd741ad79445c384ee2c16dd` |
| D20.png | `6490f0dade78fa17d4a404a15f3f1fe6097603037bfc997127b21a73aec23f0d` |
| D21.png | `8e934953c27801ef549f62b0accc3e0b0730e86555fe30a8bbbbd67b71e33b56` |
| D22.png | `ecf5ba85ae0d949b332d386e4746e093455f93e90b322cc0a1c58b7699d7daf2` |
| D23.png | `49012f1529e3c3ffda96507870c18f122587bb793d3a6b93e988eae87039fc50` |
| D24.png | `64959573dc37f0951e995619c3d46d6991dc50d8a1799b5a467945c663c5acfa` |
| D25.png | `ee0bcc9257d5ed6273147c8ca44cdf6709674bc8cd01af25da03ef46a6ba30ea` |
| D26.png | `d032ae0975da892f0e37cb28dc2cafa6dd23eb6ea55465a2883ae706f4e9e8ec` |
| D27.png | `253a4316f5dbe20e9b36577041a98263f6e4d7c86b6b73efe536f014a978eb64` |
| D28.png | `0c75f6931b3ca32f819ad53fd01ebcc38a8f431ac6d72b4109cd37404c79803c` |
| P01.png | `7c4f4ad97ec20a5370c2e6253d23d7003000c1a6532a575cea150416c21ce6ff` |
| P02.png | `7d3bbeea377f2c3b434ec6afa9d4dc0c1d7182b30b48f7e151ac3fcdc0dcfdc3` |
| P03.png | `d3b68656f4ef3f50f959a20a153450043b5f34de117aab5467da538f6a255695` |
| P04.png | `975ced58c91a1f4a1f2f2b448172a89aa2abf70cf02d36422a268232cdd07a4a` |
| P05.png | `17eebb0e07707183cfba78bb6aa9aa029749217c3693caf54584e2c05f8d9b38` |
| P06.png | `ff18f633d18e8c3a704d595e487ebeb00fa0a8169c14477a13e20c51cc2fbdca` |
| P07.png | `2982adf5a4d0dab632a025105f9525940d52adcd3c2f5c95acd497691a2f94fb` |
| P08.png | `289e7f31fe7f7bc0298f884ad61dd6e02cf759e884bd139dbc168ecd93e15c22` |
| P09.png | `70b742a3d7c46ba647d7c43e9de624dd56742e5fb87f459508e10a2589f6be4b` |
| P10.png | `19d44cde4022d400078885ea10aaf978eae93a81de1ffa5c2139392eafc00a36` |
| P11.png | `8eb329e3ad09181d67e59d2d14d1ec7beccc6d0d8502ea6cdfc300797a5edae8` |
| P12.png | `1f8f0fc6318eadeb6f59c19efe9e5ce72e3ec1016041a36fd074532939dd0926` |
| P13.png | `1c0671a0aedca02c01ae4bb9c3a8022d31f153e42b27fcac6c8e5f9e3470f1db` |
| P14.png | `b1f6865814b570ebf28824a8bd31a7e805bfcb554041605fcd6d461d9565110a` |
| P15.png | `8022aa2f7131e102d7465f393f04b53116430125b487c2d1f796800827da735c` |
| P16.png | `5daf812c949bee67be0453850238dbdac410d68e52f348c6d31e2a6ac74b9959` |
| P17.png | `2953eb2e1b829502333d025cca5c3fc29ab9f7153bd933ae22e7abd1d2132c0a` |
| P18.png | `cb592fb2a947c612c08ec310a49bd84308106d15afcdd17495252b0890cf59d7` |
| P19.png | `192dcbcc810dd3079c7796ec153d60dbce7fce76199e4722e85c524a913edbca` |
| P20.png | `1885f2d8dd7d84423519efb7139a71080d22dd7368c57042136a70afeb5983cb` |
| P21.png | `66a1ae6c50740515ebf86521ad453648745275256442c24e3ac3e06e43736af4` |
| P22.png | `efc0660a81b4605db2eaf5ef02dbe30c02fd507cf94bfde9ca99cce12898e1b3` |
| P23.png | `f8ef0dedcc93c4d551d8bfca1a825d141af8bc53a6676875d2d5a3fa3c8f7bcc` |
| P24.png | `de3d91aa889582962fa1449d61b2f523caddd7dfe6eadb757192d6be7f829267` |
| P25.png | `0e44b65e141d8b484d1b014c4c968f40237f349662f16f02e84e9b538438ae11` |
| P26.png | `b0813868dbf8772dba8b8eeb13dc02b76136332b2c201c744665073c2d0ab5fc` |
| P27.png | `3c341de212066d7dacbf5119a34b3c0b561d6a9def40010eb694041739b8bd4f` |
| P28.png | `3eed67f60470a656172f46bc028a4fc51a6c305f5ece14a47abfabc26a1d426d` |
| P29.png | `75388a48983f15cada980dcab019106dcea09de45838e20aa2ea7afb76de423f` |
| P30.png | `3701a4e32ec2ce04213fe38aacf6d66f9f8b6f62525a899ba6d0ab588a5b104e` |
| P31.png | `0da6897d1a75b6d3526bfd7225f9c3bbd4bb68c10df902c6f5ac3344c972786f` |
| P32.png | `e37c256f91b54fa9a571292e3aff932f0deda2f01e557f946f76ab42dd2577f0` |
| P33.png | `533c01dc8276465ae19053f4334e24ccbb19e867fdf167555eaf2001ecec60cd` |
| P34.png | `988a74df0991ccc2f090ee71ccd8e1d2e27fae3d27ccf913f7fbd83e9282ae26` |
| P35.png | `40b750563e439d5b7fa4230a54e93278c648538219b4c3e66ed2a405e0854c49` |
| P36.png | `b3163641ad82848819044817197ba63ca2839545df3990f19df7352250ebc90c` |
| P37.png | `a07f24b5e3413f0774c78dd04c6aeb3083ec0c9a954280886fd2fc1ef160fa12` |
| P38.png | `04e58d31c63f11090e449b3c674e97b58b79410e79f8ed9b3c59ac142a66bb50` |
| P39.png | `41a755dcb9b6186b15418472747af55c6dad9d8003884bfe81849623f2ad531d` |
| P40.png | `8716fcbbd044ca9f334f74dce80ddb39622e6b34d31237f567d5d805dc55e4ae` |
| P41.png | `938edbbbc0fe4b39c9412b06b0a60ac363744256fe6f6935901fab8cb3ed49e2` |
| P42.png | `029f016355ced3e5c5dd13df502b3c1b4c2ce2fd27a9b82c5662542df5e2e315` |
| P43.png | `b5b837f03b1db9e33fbf012ab35df64604d217ec03e23c655ed6accf48746926` |
| P44.png | `218c21e1abd81cfee3a183b43620d8ad092754dbc1a877ead02c7ba8ca070eab` |
| P45.png | `a8116eff566fe1b2ca02b3914d3bfabaf9ae0dec0a7046bfa3818af2a49515c6` |
| P46.png | `fc4fc7d053d368052526e2151f5c9c79e8571214fcf34fb8bca2a1bbc771de52` |
| P47.png | `9535f33a4decacea1964aebca0ab0bc1f7fdc45541314c77d379c7b3843c0ff6` |
| P48.png | `2a17496c180db5c8aeeb27bc5bd9ee43c8e934885cecf67fa3a7aaf5c5972f2f` |
