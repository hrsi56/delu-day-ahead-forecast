# PRES-4 — fresh reader (PUBLISH_RULES 1.4 §10.2)

**Outcome: answers 1–5 agree with the registry, the evidence records and the derived records, from the placements the
rules require.** Every score the reader quoted equals its record. The reader found no violation of an effective rule:
two observations that looked like candidates were checked and are not (observations 9 and 10 below). The rest, and answer
6, are advisory; one new advisory, A-PRES4-7, is filed in `docs/track-b/publication-advisory-log.md`.
No text on the page changed after the reading.

## How it was run

- **Page:** `docs/index.html` at `db65a46`, SHA-256
  `e22525a960ad4cd1147c6d8179ace980123a3b6c2051565b134c0c68bddaa366`, served over HTTP on 127.0.0.1, every disclosure
  closed.
- **Screens:** written by `scripts/check_reader_paths.py release` (record `pres-4-local-release-attempt-3.json`,
  `cold_reader_screens`), the page as a reader scrolls it, one viewport at a time, each step the viewport less the
  56 px sticky header:
  - desktop, Google Chrome 154.0.8037.98 at 1440×900, 23 screens, step 844 px, supplied as D01–D23;
  - phone, Playwright WebKit 26.6 at 390×844, 39 screens, step 788 px, supplied as P01–P39.
  They were copied under neutral names to `.local/tmp/pres-4/fresh-reader/`. Their SHA-256 values are listed below.
- **Reader:** one fresh agent. It wrote nothing in PRES-4, and it was given no repository, project history, prior
  review, expected answers, chart locations or explanation: only the prompt below. Its record shows 62 tool calls, all
  reads, one per image, of exactly the 62 files named. Its transcript was not otherwise inspected.
- **Date:** 2026-10-11.

### The prompt (verbatim, except that the 62 image paths are abbreviated; they are the files listed in order below)

```text
You are a reader seeing a web page for the first time. You have no other information about it, and you must not look for any: do not open, list or search any file or directory other than the 62 image files named below, do not run any command, and do not use the web.

The page is shown as screenshots taken while scrolling from the top to the bottom, with every collapsible section closed. There are two renderings of the same page: first a desktop browser (1440 × 900), screens D01 to D23; then a phone browser (390 × 844), screens P01 to P39. Read every one of them, in this order, with the Read tool:

/Users/djourno/Downloads/PJM/.local/tmp/pres-4/fresh-reader/D01.png
[… the 62 paths, D01.png to D23.png, then P01.png to P39.png, one per line …]
/Users/djourno/Downloads/PJM/.local/tmp/pres-4/fresh-reader/P39.png

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

## Grading: answers 1–5 against the registry and the records

A desktop screen n covers document pixels from (n − 1) × 844 for 900 px; a phone screen n from (n − 1) × 788 for
844 px. Placements are attempt 3's: the headline block ends at 800.6 / 801.3 px (desktop, Chrome / WebKit) and
628.6 / 628.7 px (phone); the finding ends at 1,727.6 / 1,728.3 px (A2 limit 1,744) and 2,402.5 px (limit 2,420).

| Question | What the registry and the records hold | The reader | Within the placement rules |
|---|---|---|---|
| 1. The headline result, with its numbers | v5 met rule `cp24-adoption` (`derived.adoption.v5.verdict`); the distances v5 − v4 at the rule's 97.5% level: −0.0133 [−0.0166, −0.0091] on the point-error score and −0.0119 [−0.0147, −0.0084] on the interval score; N = 1 (`derived.adoption.v5.*`, `cp24.uncertainty97_5.*`); the change as a share of v4's score, −2% [−3%, −2%] on each (`derived.change.v5.*`); for scale, v5's MAE 4.8–14.4 EUR/MWh in the ordinary periods and 45.5 in the 2022 crisis period, the naive's 8.6–30.5 and 86.9 (`derived.periods.*`) | All of it, each number with its metric (D01/P01; D02/P03, D09/P17; D04/P07), plus the chart's ratios 0.522 / 0.494 and v4's 0.536 / 0.506 (`cp24.metrics.v5.equal_fold.*` 0.5223 / 0.4937; `HGL` 0.5357 / 0.5056) | Yes. **A1:** the reader tied each difference to its metric and its level on the first screen. As in PRES-3, it noted that the research headline sits beside the released v1 demo |
| 2. Against what? | v5's comparator, set in advance: v4 itself, on identical hours; the naive as the normalizer; the targets' benchmark, daily LEAR (0.6578 / 0.6390); 10,747 hours over 448 days | All of these: the comparator set in advance (D05/P09), the normalizer (D04/P07), the targets with their date (D03/P04). Its own arithmetic, v5 about 21% and 23% below daily LEAR, equals `derived.criteria.v5.distance.*` (−21%, −23%), which the page does not print | Yes |
| 3. How sure, and on what evidence | Development · post-selection; "development evidence, not a test on new data"; meeting the targets is "a development diagnostic, not a product qualification"; the decision at 97.5%, every interval below zero; the practical size, half a percent; the coverage limit, 448 of the 2,654 days, none in October to December, 1 winter (`derived.coverage.*`, P54); the reuse of the five test periods; 25 policies tested against the targets (`derived.criteria.v5.tested`); v1's holdout "confirmatory-style, not power-qualified"; no live evidence | All of these, with quotes (D02/P01, D03/P04, D09–D10/P17–P19, D04/P07, D19/P33, D21/P36) | Yes. The badge is on the first screen; the coverage and reuse caveats are directly under the finding. The bootstrap design and the five periods sit in a closed disclosure, which the rules allow |
| 4. What the demo runs, and why not the best model | The released model, v1; the release rule; the replay is historical, not live; v1's development scores (1.052; the August 2022 peak coverage 0.194) | All of it, with the rule quoted beside the demo action (D01/P02) and the startup line | Yes. The rule is beside the demo action, outside any disclosure |
| 5. What was tried and dropped | The calibration experiment and the model comparison study, not adopted; CP-22's two candidates (R 0.5368 / 0.5066, M 0.5343 / 0.5048) and CP-23's candidate (0.5421 / 0.5127), not adopted, with their reasons; v5's study arms DDNN-2 alone (−11%, −16% against v4, `derived.change.ddnn2-alone.*`) and v3 plus a DDNN-2 member, never candidates, descriptive; v4's three study arms; normalized LEAR (0.6723 / 0.6460); v2's pooled-interval control | All of these, with each branch card's reason and each score as recorded (D08/P15, D03, D06, D10–D11/P19–P20, D17–D18) | Yes |

Answer 6 is advisory. It asks about: why the fixed one-sixth weight was the only eligible candidate when DDNN-2 alone
and v3 plus DDNN-2 scored better, and how the next model will be chosen without another selection on the same five
periods; whether the rule (set 2026-10-05) was written after CP-22's and CP-23's failures; the bootstrap's blocks and
draws, the 97.5% split and the multiplicity of 25 policies; the absent October–December days; v1's 1.052 against
"28.58% worse", the naive's pinball loss, and v1's 0.194 crisis coverage; the one-shot test's size and detectable
effect; whether the per-period veto favours the incumbent; the interval score's levels and v3's under-coverage; the
GFS run's availability before the auction; the business meaning of 2%; and the candidate's own part against the AI
agents'. These are the return's interview-capture triggers.

## What confused the reader, and what was done

| # | Observation (screen) | Disposition |
|---|---|---|
| 1 | The opening leads with research v5 in score units, without v4's base value, beside the v1 demo; on the phone the demo action follows the research card (D01, P01–P02) | Advisory: the opening pairs research and release by design (Observable outcome); each half is labelled. v4's score is in the comparison (D03/P04), the share of it directly below the headline (D02/P03) |
| 2 | "1 policy tested against the rule" beside three candidates "tested against v4 and not adopted"; were they tested under the same rule? (D01/P01, D03) | Advisory, **A-PRES4-7**: N counts CP-24's rule only, as A1's form requires; each branch was tested against its own experiment's rule, named in the registry (`cp22-replacement`, `cp23-adoption`) but not on the cards |
| 3 | "−2% [−3%, −2%]": the point estimate on the interval's edge (D02/P03, D09/P17) | Advisory, A-PRES4-1 recurrence: whole-percent rounding of −2.48% [−3.11%, −1.70%] (standard §4); the exact ratios are in the value table |
| 4 | "12 policies" in the chart, "8 of them were tested", "25 policies", "16 later policies" (D03–D04, P04, P07) | Advisory, A-PRES1-10 recurrence: the census sentence says the chart's rows are not the census |
| 5 | The targets were set on 2026-09-15, v1's report date (D03, D19) | Advisory: the registry's date for rule `criteria-1-2`, with its provenance (the pre-registration commit `bb5e678` precedes CP-15's results), unchanged since PRES-1 |
| 6 | v1's 1.052 against "28.58% worse"; "its development replay" (D04, D19/P34) | Advisory: unchanged product text; the explanation is in the disclosure "why v1 scores differently in its own report" |
| 7 | The five test periods and the 448 days are not listed in visible text (D05, D10) | Advisory: they are in the closed disclosure "Bootstrap settings and the five historical test periods" (§3.3 allows it); the caveat's counts are on the path |
| 8 | v4's name "three-block LightGBM added" against "not shown to contribute" (D06, D13/P24) | Advisory: v4's published chapter, byte-identical |
| 9 | The pooled pair (0.534 / 0.505) plots left of v4 (0.536 / 0.506), yet its card says "decisively worse" (D03, D08) | **Checked, not a violation:** the card's reason reads "decisively worse than v4 in one test period, with a 95% interval wholly above zero" — rule `cp22-replacement`'s per-fold condition ("no fold is decisively worse"), true as recorded: fold 4's point-error intervals are [+0.148, +0.423] (averaged member) and [+0.051, +0.326] (pair) EUR/MWh (`cp22.uncertainty.R-HGL.fold_4.MAE`, `M-HGL`). The card's result already states the averaged differences, their intervals crossing zero, beside fold 4's (C208) |
| 10 | "six screening criteria" followed by five items (D10/P18, D13/P23) | **Checked, not a violation:** the parenthesis counts the two accuracy targets as two of the six, in the wording of v4's published chapter, which v5's reading repeats. Rules differ by generation because each checkpoint set its own (named in each chapter) |
| 11 | The study arms that scored best are not in the comparison chart (D03) | Advisory: the chart's rows are the Owner's comparison (generations, the branch points and the benchmarks); the arms, their intervals and "Descriptive only" are on the v5 path (D10–D11/P19–P20; editorial recommendation 1) |
| 12 | v1 is "one LightGBM quantile model" (D17) and "A LightGBM ensemble" (D19) | Advisory: unchanged historical and product text |
| 13 | The demo's 80% interval, coverage at 95%, the interval score's levels unstated (D01, D15, D19) | Advisory, A-PRES1-18 recurrence |
| 14 | v5 has no "Compare the runs in MLflow" link, although D22 says every policy is in MLflow (D11/P20, D22) | Expected: the route returns with the MLflow upload, the index and the `--final` build (editorial recommendation 11), checked at the final SHA |
| 15 | The reproductions list omits the calibration experiment, the two October branches and v1 (D21/P37) | Advisory: the list names the generations' and the study's reproductions; the runbook's branch touchpoints (§3) do not include it. Each branch card links its report and verdict |
| 16 | The GFS attribution names only v3's weather data (D22/P38) | Advisory, A-PRES3-7 (deferred to the Space's redeployment by the Owner's decision of 2026-10-11) |
| 17 | v2's "added" box has v3's border colour (D17/P30) | Advisory: v2's published section, which the Owner's decision D1 leaves unedited |
| 18 | The phone timeline drops the one-line descriptions (P08–P09) | Advisory: PRES-2's responsive design, unchanged |

No observation is a violation of an effective rule. No page text changed after the reading, so the screens are the
candidate's page.

## The reader's answers, as given

The reader's reply, preserved without edits. The one character sequence the notification escaped, `&lt;`, is restored
to `<`.

```text
1. What is the headline result, with its numbers?

The page leads with a research model, not the released one. v5 ("DDNN-2 added") met its pre-set adoption rule against v4. The hero says: "both error scores improved on v4's (v5 – v4 at 97.5%: −0.0133 [−0.0166, −0.0091] on the point-error score, −0.0119 [−0.0147, −0.0084] on the interval score; 1 policy tested against the rule)" (D01, P01).

As a relative change: "−2% [−3%, −2%] on the point-error score and −2% [−3%, −2%] on the interval score, with 95% confidence intervals" (D02, P03; repeated at D09, P17).

The absolute scores, as ratios to the naive forecast, are v5 0.522 point and 0.494 interval, against v4's 0.536 and 0.506 (D03, P04–P06).

For scale: "v5 4.8–14.4 EUR/MWh in the four ordinary periods and 45.5 EUR/MWh in the 2022 crisis period; the similar-day naive 8.6–30.5 and 86.9 EUR/MWh" (D04, P07).

The released product has a separate headline. v1's one-shot holdout gave "MAE 25.9 against 27.8 EUR/MWh, and mean pinball loss 6.7 against 13.9 EUR/MWh", with "one-sided Diebold–Mariano … p < 10⁻⁶" on pinball loss only (D19, P33).

2. Against what?

- **The direct comparison:** v5 against its predecessor v4. "Comparator: Set in advance: v4 itself, on identical hours, so the protocol's comparator is also the predecessor and the comparison is direct" (D05, P09).
- **What every score is measured against:** a naive baseline. "Each score divides a model's error by that of a simple similar-day forecast in the same period, which therefore scores 1.000" (D04, P07).
- **The accuracy targets:** "each error score at least 10% below the strongest benchmark's, set on 2026-09-15", and "Daily LEAR: the strongest benchmark, a linear model refitted daily" (D03, P04). Daily LEAR scores 0.658 / 0.639 and daily LightGBM 0.784 / 0.740 (D03). By my own arithmetic, not stated on the page, v5 is about 21% (point) and 23% (interval) below daily LEAR.
- **v1's holdout:** compared against "the similar-day naive" (D19).
- **Never compared:** "No paired interval for v2 against v1 exists: the protocol did not test that pair" (D07, P14).

3. How sure are we, and on what class of evidence?

Everything for v2 to v5 is a development backtest after model selection, not a test on new data.

- Each research result carries the badge "Development · post-selection", explained as "development evidence, not a test on new data" (D02, P01).
- The page also says "Meeting the targets is a development diagnostic, not a product qualification" (D03, P04).

The statistics are paired confidence intervals on identical hours, using "the experiment's own bootstrap draws" (D05). The decision was made at a 97.5% level, and all intervals lie well below zero (D09–D10, P17–P18). The rule had five conditions, including a practical-size threshold: "both scores improved on v4's by more than the practical size set in advance, half a percent" (D10, P18).

The page lists its own limits:

- **Season coverage:** "The comparison scores 448 of the 2,654 days … 0 of them fall in October to December, and only 1 winter (December to February) contains any of them" (D10, P19).
- **Reuse of the same test periods:** "the second decision on a distributional neural network over the same five test periods … only a one-shot test on days never used for development or selection protects against that reuse" (D10, P19).
- **Many candidates on the same data:** "25 policies were tested against them" (D04, P07).

The effect is small. By my arithmetic it is about 2.5% of v4's score.

The only out-of-sample evidence is v1's single 90-day holdout, labelled "Confirmatory-style, not power-qualified" (D19, P33). There is no live evidence yet: "Live operation · planned" (D21, P36).

What is missing: the bootstrap design (block length, what is resampled) and the definitions of the five test periods are inside collapsed sections ("Bootstrap settings and the five historical test periods", D04). I could not check them.

4. What does the demo run, and why not the best model?

The demo runs v1, "v1 · released LightGBM" (D01, P01), described as "A LightGBM ensemble forecasting nine quantiles for every hour, calibrated into 50 / 80 / 95% prediction intervals" (D19, P33).

It runs in the browser: "about 57 MB on a first visit. A forecast appeared after 18.3 s" (D01, P02). The sample chart is "a historical replay, not a live forecast" for 2026-09-06 with an 80% interval (D01, P02).

Why not v5: "Research generations are not released one by one; only the final model, after its one-shot test and live run, replaces the released one" (D01, P02). None of v2 to v5 has had a one-shot test or a live run. The next step is "an evaluation of the selected model under a frozen protocol and prospective monitoring" (D20, P35).

The page is candid that the demo model is the weakest on development data:

- It scores 1.052 against the naive's 1.000 (D03, P05).
- "On the development folds its point error is 28.58% worse than the naive's, pooled over all days … p = 0.948" (D19, P34).
- "Over the August 2022 peak weeks its 95% interval covered 0.194 of outcomes" (D19, P34).

5. What was tried and dropped?

Between v1 and v2 (D08, P15):

- **Calibration experiment, Sept 2026:** "Recalibration alone was not enough: the model itself had to adapt."
- **Model comparison study, Sept 2026:** "No policy met the criteria; the study informed v2's blend of two LEAR forecasts."

Between v4 and v5 (D08, P15; scores on D03):

- **Pooled LightGBM member for v4, Oct 2026:** "Both candidates were decisively worse than v4 in one test period, with a 95% interval wholly above zero; the rule allowed none, so v4 was kept as it was." The two candidates were "Pooled member, averaged" (0.537 / 0.507) and "Pooled pair" (0.534 / 0.505).
- **DDNN member on v4, Oct 2026:** "The improvement over v4 that the rule required was not shown, on either score." It scored 0.542 / 0.513.

Study arms that were never candidates:

- **For v5:** "DDNN-2 alone and v3 plus a DDNN-2 member" (D06, D11, P20). DDNN-2 alone beat v4 by "−11% [−14%, −7%] … and −16% [−19%, −12%]", and "v3 plus a DDNN-2 member also scored better than v5. Descriptive only" (D10–D11, P19–P20).
- **For v4:** three study arms (D06).
- **Others:** "Normalized LEAR (study)" at 0.672 / 0.646 (D03), and v2's pooled-interval control (D17–D18).

v1 itself was replaced in research after it "failed in the 2022 crisis" (D07, P13).

6. What would you ask the candidate?

1. DDNN-2 alone beat v4 by 11–16%, and v3 plus DDNN-2 also beat v5. Why was a fixed one-sixth weight the only eligible candidate, and why are these arms left off the comparison chart? Does the adopted v5 lose to a model you built and set aside? How will you choose the next model without one more round of selection on the same five test periods?
2. The adoption rule is dated 2026-10-05, after the two October experiments failed against v4. Was the rule written after seeing those failures? The hero's "1 policy tested against the rule" makes this matter.
3. How was the bootstrap set up: blocks by day or week, resampling within each test period, number of draws? Why 97.5%: a Bonferroni split across the two scores? How do you account for 25 policies tested against the same targets?
4. Why are there no October to December days and only one winter in 448 test days, for a market whose prices depend heavily on season?
5. v1 scores 1.052 (5% worse than naive), yet "28.58% worse" when pooled over all days. Explain the difference. Also explain how the similar-day naive gets a pinball loss, and why shipping a model with 0.194 coverage of a 95% interval in a crisis is acceptable.
6. What is the plan, sample size and minimum detectable effect for the one-shot test? Can 90 days detect a 2.5% improvement, given that v1's holdout was "not power-qualified"?
7. The pooled pair beat v4 on both averaged scores but was vetoed on one test period. Meanwhile v4's three-block split was kept although "not shown to contribute" and its point estimate against pooled was worse (+0.0050). Is the per-period rule biased toward the incumbent?
8. Which interval levels make up the interval score, and does v3's under-coverage (0.9377 at 95%) carry forward to v5?
9. Weather inputs use "the GFS run of the day before" (D20). Which cycle, and was it actually available before the auction closed? Availability is "Assumed and documented", not checked in code (D21).
10. What does a 2% lower error score mean in EUR or in trading decisions, and who is the user?
11. What did you implement yourself, given "AI agents assisted with implementation, analysis and documentation" (D22)? For example, could you walk me through the NumPy DDNN-2?

Things that confused me:

- **D01, P01:** The hero leads with a research model (v5) and raw differences in score units, without giving v4's base value (0.536 only appears on D03). Meanwhile the demo button runs a different model, v1. On the phone, the demo button doesn't appear until P02, below the research card.
- **D01, P01, D03:** "1 policy tested against the rule" sits beside three other candidates that were "tested against v4 and not adopted". It is unclear whether those were tested under the same rule.
- **D02, P03, D09, P17:** "−2% [−3%, −2%]" puts the point estimate on the interval's edge. It looks like a rounding artefact; by my arithmetic the values are about −2.5% [−3.1%, −1.7%]. One more decimal place would help.
- **D03, D04, P04, P07:** The counts are hard to follow: "12 policies" in the chart (which includes benchmarks and the naive, which aren't policies), "8 of them were tested", "25 policies were tested", "16 later policies".
- **D03, D19:** The accuracy targets were set on 2026-09-15, the same date as the original v1 report. Were they set after seeing v1's results?
- **D04, D19, P34:** v1's 1.052 and "28.58% worse" disagree without explanation. The reason is in a collapsed section. The phrase "v1 appears here as its development replay" is also not explained.
- **D05, D10:** The five test periods and the 448 days are never listed in visible text, so the season-coverage caveat cannot be judged.
- **D06, D13, P24:** The v4 generation is named "three-block LightGBM added", yet the text says "The LightGBM's split into hour blocks is not shown to contribute".
- **D03, D08:** The pooled pair (0.534 / 0.505) appears to the left of v4 (0.536 / 0.506), so it looks better, yet it was rejected as "decisively worse".
- **D03:** The study arms that scored best (DDNN-2 alone, v3 plus DDNN-2) are missing from the main comparison chart.
- **D10, P18, D13, P23:** "six screening criteria" is followed by a list of five items, unless the two accuracy targets count as two. Also, v5's rule has five conditions and v4's four, while v3 used a "joint improvement rule … and both accuracy targets" (D16). The rules differ between generations and the page doesn't explain why.
- **D17, D19, P33:** v1 is "one LightGBM quantile model" on D17 but "A LightGBM ensemble" on D19.
- **D01, D15, D19:** The demo shows an 80% interval, while coverage is reported at 95%. The interval levels used in the interval score are never stated.
- **D11, P20, D22:** v5's evidence links have no "Compare the runs in MLflow" link, unlike v2 to v4 (D13, D16, D18). Yet D22 says "Every policy evaluated since v1 is in the MLflow experiment".
- **D21, P37:** "Each experiment below has its own full reproduction" lists v2 to v5 and the comparison study. It leaves out the calibration experiment, the two dropped October experiments and v1.
- **D22, P38:** The terms name only "The v3 research model's weather data", though v4 and v5 use the same weather inputs.
- **D17, P30:** The v2 "added" box has the teal border used for v3, not v2's purple.
- **P08–P09:** On the phone, the timeline drops the one-line descriptions that the desktop shows (D05).
```

## Screens supplied (SHA-256)

```text
e756739bef789ff20692d1c6d18075f59eb5795487a3d32bc8c6087d4355861a  D01.png
fc0f01772122207bd5618bdc01d5770eee2f469df09ad24df0f108b45d21b8df  D02.png
4f3a770abf0f983f76fd690f652b3d0f8ad92b9e7c2ffc940de1914b88789972  D03.png
6a47a60764235465c4b08656b09e856bfd21983ad81173a5a4705a0f4b112da5  D04.png
0ede3b64effaa22f5796a4ad54c5967be0bf7949dc5316421e0f946d973769c7  D05.png
0228a73edf4c9f80f1c37449d6b21a2b56c72f594f9317e3728f5cb2a81888ed  D06.png
0e20039be33fc60d9a64bba33c3d4238e824128bcac44bc84c15194148fc5a72  D07.png
ace1dc2ca833bf458ba5bac977fa52b505233ef3e195146036ddd970f8670e1c  D08.png
ee38f320203f401afc353f26c0248a52a2d499c1d47cab61a1e11165a44324dd  D09.png
d48e63addec70b68f4f33070e27533abfb4a119e3292f933b830f1be360a6ea4  D10.png
753f8d849ec4cca8717f1205dc9c3b764a07ec4edff543bb8a682145785a5b2c  D11.png
35dcbe1904777b91b0330e387f41bf1d3cc6a00c10b27b279b7e360bfaf3a49a  D12.png
2ee1c3cf429b60f17291aa6190942f2f1ce465eadf53ee91cdcd681bb09f7a7a  D13.png
5dc37c97e47e2c0735a970c25ae23b7dab66ed72a0c7bfc7d2afafad7aa2f43f  D14.png
2f0dd0ed826f35bf1754b69248319b37b1804ec80afb586120a1d4a27674f7d5  D15.png
4213f4b6c1ff45cced67a8a1982a53471dd6accfdb9c92aa9192126fb5c517c8  D16.png
33330f163bbd2cab06906cd59dd472aed9b89b9089fb7fb0294568d3e51030e6  D17.png
48410e2b34f037aceecbbf34d53aeaf2f7eff9bfcfc930ef1c2acf7090185447  D18.png
fc26b59c1afe42286e4e4c973e9af90230c1704bb616d024fd48e6fb71a8e187  D19.png
15761f983dc8eeaa9d0c94919d23e944762f45d2e70aeae169ba2f5c2809ba67  D20.png
254efca3a52a7565d8e43268e456cc030e61854d1187ede02e421af99a976378  D21.png
86515034a1ae92fa6097a4c542581ed16e063ecac3610eb1f07cd04d258c4145  D22.png
e0c80dd90563754a5ac130eda17fc54336cb64dc619b96334cb93a10530db1d7  D23.png
12d05c776e8ff4f00bed78b9c12caa2381321e7e35ec565d5b2eaeb74ed97eb7  P01.png
4a009c2b14b9b74360c70a4e858aef0067b0267ad69405b40f40e2b6ba2c817b  P02.png
cc64161135b2cf48ef684e4affff5e8e2c4cde2d75360aa115667801f68e2a68  P03.png
97320ccf3ccdc2eae44a717b0c78bfd11c3ca453bf2a5bb9c95f89450ae806ae  P04.png
99500c1e3ecdd6388c02ef8ae2e8054cf95e3d45458b2eeac87017594de23580  P05.png
e869e0edffa60719ac9599f19957e5ba2e668a2ce1d81e809958238e0ccd988d  P06.png
7122d2af96f91b0945f9bb57f1b7cf9c320e7f8cd10ea788ba1e3ce36b9871dc  P07.png
ae3ef6aaeed4740dd850da35254ba249f01529e58b86c93b28fe267bde51831d  P08.png
904f3d223bef950a68dceecf2d6ef3fba620eda0e69affeee1eaf439340bd81e  P09.png
dfbc3faaf486c11e2170d19f9c5ac32fbbc4fc04f2c203e6042eec31874a2a85  P10.png
68a6d4c3a25f26ca0fd4effa3de7552277c2014afd7400cad18e99ba5c80fc8c  P11.png
ecf1a8ed4f85c5e6c62f31ba4ec8c55acd4e1ae1ff2ed88b7e254d3c8baccada  P12.png
6ef3aed5a0e1f5fe9c7bc1ae0292e9fafc7a8c9739635d97c5aff24cf5592f6a  P13.png
a8358b6451e01df39528cdf1d4ef1db395b18f26bc2f65318d5814ca6b23ad57  P14.png
62e88eb5e6e10b273efcb8ad42d60ec6828f9c983bd4c5a900e4a3a134e25dc0  P15.png
562f3c6dfd18a1bb8aeda99c95d43ae0dc74535ef48b610d992c92a5d6574368  P16.png
56e0c3983847bef33c0811b207d8905c04b896125a0cce3eddb0047af291a176  P17.png
e49cacd7adf7ada21cdecca8bbfda2001c1e26d0eb71dd129a1ae03416ef379c  P18.png
2cbe9ac33f94e87b9804ef96fad5b763b7c1b2fbc20d21a5744872b1ef161148  P19.png
125661849c2704adcca20bb8d788124d7088f52d104de3f52d3af8ab418d41c2  P20.png
319ed861acf44c7b29903a4d8573c7f5e8ecd1363f9ddaab38bc17179ca4df53  P21.png
8c3c70489dce719039de56cf52c19ebef34d954d781952a18d7ce11ab0fc7d08  P22.png
712bc5289980259925ea588c5cf1107b17e6df72d6130e6af5da53af1511a87e  P23.png
751112405373f60f2ba94b0e0d3d5ade179ea88d555f3b3e9c25e27c795b57cf  P24.png
301a4138d0a19e27c797da1394e928e9ddc1ab53edc414eff46cc7cbdd761831  P25.png
ff512819b37b7006e09d3a750399574a4e94105137d4b21f4c5144e20ac677c1  P26.png
3c74ef8c03d597f0660ba36f9390cfbc4e9e87811a5d45f68077eef023f61037  P27.png
fbb450dd2e067cd8fbd3176b50b00b908d30c7865c708e2bd91674df2718a288  P28.png
64fdb1ba308204981b9856bbeed5701dee82763c3ab0337cb49ffdcaa6ab0350  P29.png
174c783fdd71de20a57f087f85a09ab142717c112594c5c10441491341155ce1  P30.png
9fc150f64ea267bc3bd893bc9c889f36ec447a30aff2ca4d90c517bf7cef3361  P31.png
64198a5b2dd10bbdba35c159884683a4a3ad8ea7e8dc96c41e0d97f7800424e4  P32.png
ac09df99f88e94e2a9ad1707466bd664506f649f769f2ffd309a3f849594947c  P33.png
bf242266245b34140d89de0edd639ad999fe16dc07267925f7bba666f339ca74  P34.png
2c63892a27cd8c86a8924c3b17ecd153569bebf9ed12624d28fad1a4212f0bae  P35.png
793f8713b76c85d78cf5949f65c7f6c9c0bb2c7bf59ae62f14e080438857d72d  P36.png
a37bb10008a480caee83d9f29b72d9f80e2f4132fba609d8c17594cec7ae0d8d  P37.png
53faa8c04c3da70e643c4c53336f05fe9b9412c320389467fcb46662e3ec65e5  P38.png
2a17496c180db5c8aeeb27bc5bd9ee43c8e934885cecf67fa3a7aaf5c5972f2f  P39.png
```
