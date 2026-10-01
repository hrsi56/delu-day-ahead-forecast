# PRES-3 — fresh reader (PUBLISH_RULES 1.2 §10.2)

**Outcome: answers 1–5 agree with the registry and the derived records, from the placements the rules
require.** The reader found one violation the editorial review had missed: the headline uses
"policy" ("1 policy tested against the rule") and the word was defined only further down. It is
repaired, with a test and a negative control. Two of its other observations led to clarifications on
the reading path. The rest, and answer 6, are advisory.

## How it was run

- **Page:** `docs/index.html` at `d9c4438`, SHA-256
  `b2b5b2b64ac929c046e730df8f2379a584295bf862b1780ea1cf1f69d81a84dc`, served over HTTP, every
  disclosure closed.
- **Screens:** written by `scripts/check_reader_paths.py release` (record
  `pres-3-local-release-attempt-3.json`, `cold_reader_screens`), the page as a reader scrolls it, one
  viewport at a time, each step the viewport less the 56 px sticky header:
  - desktop, Google Chrome 154.0.8037.58 at 1440×900, 18 screens, step 844 px, supplied as D01–D18;
  - phone, Playwright WebKit 26.6 at 390×844, 30 screens, step 788 px, supplied as P01–P30.
  They were copied under neutral names to `.local/tmp/pres-3/fresh-reader/`. Their SHA-256 values are
  listed below.
- **Reader:** one fresh agent. It wrote nothing in PRES-3, and it was given no repository, project
  history, prior review, expected answers, chart locations or explanation: only the prompt below. Its
  usage record shows 48 tool calls, one per image. Its transcript was not otherwise inspected.
- **Date:** 2026-10-01.

### The prompt (verbatim, except that the 48 image paths are abbreviated; they are the files listed in order below)

```text
You are a reader seeing a web page for the first time. You have no other information about it, and you must not look for any: do not open, list or search any file or directory other than the 48 image files named below, do not run any command, and do not use the web.

The page is shown as screenshots taken while scrolling from the top to the bottom, with every collapsible section closed. There are two renderings of the same page: first a desktop browser (1440 × 900), screens D01 to D18; then a phone browser (390 × 844), screens P01 to P30. Read every one of them, in this order, with the Read tool:

/Users/djourno/Downloads/PJM/.local/tmp/pres-3/fresh-reader/D01.png
[… the 48 paths, D01.png to D18.png, then P01.png to P30.png, one per line …]
/Users/djourno/Downloads/PJM/.local/tmp/pres-3/fresh-reader/P30.png

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

## Grading: answers 1–5 against the registry and the derived records

A desktop screen n covers document pixels from (n − 1) × 844 for 900 px; a phone screen n from
(n − 1) × 788 for 844 px. Placements are attempt 3's: the headline block ends at 800.6 / 801.3 px
(desktop) and 628.6 / 628.7 px (phone); the finding ends at 1,677.6 / 1,678.3 px (A2 limit 1,744)
and 2,379.5 px (limit 2,420).

| Question | What the registry and the derived records hold | The reader | Within the placement rules |
|---|---|---|---|
| 1. The headline result, with its numbers | v4 met rule `cp21-adoption` (`derived.adoption.v4.verdict`); the distances v4 − v3: −0.0301 [−0.0368, −0.0228] on the point-error score and −0.0266 [−0.0327, −0.0204] on the interval score; N = 1 (`derived.adoption.v4.*`); the change as a share of v3's score, −5% [−6%, −4%] on each (`derived.change.v4.*`); for scale, v4's MAE 4.9–15.0 EUR/MWh in the ordinary periods and 47.0 in the 2022 crisis period, the naive's 8.6–30.5 and 86.9 (`derived.periods.*`) | All of it, each number with its metric (D01/P01; D02/P03; D04/P06), plus the chart ratios 0.536 / 0.506 and v3's 0.566 / 0.532 | Yes. **A1:** the reader tied each difference to its metric on the first screen. It hesitated over which result is "the headline", because v1's holdout result is the only test on new data |
| 2. Against what? | v4's comparator, set in advance: v3, which is also its predecessor, on identical hours; the naive as the normalizer; the targets' benchmark, daily LEAR; 10,747 hours over 448 days | All of these, including the comparator set in advance (D05/P08), the normalizer (D03/P06) and the targets' threshold with its date, quoted from the new comparison terms (D03/P04). It noted that the distance to the targets is a point comparison | Yes |
| 3. How sure, and on what evidence | Development · post-selection; "development evidence, not a test on new data"; meeting the targets is "a development diagnostic, not a product qualification"; v4's intervals below zero, with no test period's interval wholly above zero; not established: the block split (C111), a gain over the August 2022 peak (C120); 12 policies tested against the targets; v1's holdout "confirmatory-style, not power-qualified" | All of these, with quotes (D02/P01, P04, D08/P14–P15, D03, D14/P24–P25), including the peak's MAE 50.1 against 47.5 | Yes. The badge is on the first screen; the caveat is directly under the finding. The bootstrap design sits in a closed disclosure, which the rules allow |
| 4. What the demo runs, and why not the best model | The released model, v1; the release rule; the replay is historical, not live | Both, with the rule quoted (D01/P02) and the startup line | Yes. The rule is beside the demo action, outside any disclosure |
| 5. What was tried and dropped | The calibration experiment and the model comparison study, not adopted; v2's pooled-interval control; the study arms: normalized LEAR (CP-15) and CP-21's pooled, three-block and normalized three-block LightGBM, not adopted as study arms | The branch cards with their reasons (D07/P12), the pooled-interval control (D12–D13), normalized LEAR and CP-21's arms (D03, D08). It could not tell why v4 went forward and the arms did not | Yes, with a gap: the page did not say that the arms were never candidates. Repaired below (observation 3) |

Answer 6 is advisory. It asks about: the optimism of model selection in the −5%, and the data left
for v4's one-shot test; the bootstrap's blocks, and how the intervals reflect the periods; why the
three-block design over the pooled one; whether the rule was set before any v4 result was seen, and
why the rule's form changed from v3's; v1's three different-looking figures and the untested MAE
difference; coverage by regime and in the crisis weeks; the August 2022 peak and price-level
shifts; the GFS run's availability before the auction; the candidate's own part against the AI
agents', and who wrote the review verdict; and exact definitions of the scores and the naive. These
are the return's interview-capture triggers.

## What confused the reader, and what was done

| # | Observation (screen) | Disposition |
|---|---|---|
| 1 | "1 policy tested against the rule" uses "policy", which is defined only later (D01, D03) | **A violation of PUBLISH_RULES §2, repaired.** Terms first used in the headline are defined directly beneath it. PRES-2's headline form defined "policies" there; v4's adoption form had dropped it. `research_claims.headline_terms` now includes it, and `test_45::test_every_term_the_headline_uses_is_defined_beneath_it` and its negative control check every word the headline uses against the terms beneath it. Answers 1–5 do not depend on it. The finding moves to 1,702.6 px (desktop) and 2,400.5 px (phone), within A2 (attempt 4) |
| 2 | "passed the six screening criteria … so it met all four conditions": the relation of the six criteria to the four conditions is unclear (D08/P14) | **Clarified.** The reading now lists the four conditions as such, the six criteria being one of them: "All four conditions of the rule set in advance held: both paired differences' 95% confidence intervals lie below zero; v4 passed the six screening criteria …; the evaluation was complete and valid; and no test period's paired interval lies wholly above zero." (C109) |
| 3 | Why v4 went forward and the study arms that also met the targets did not (D03, D08) | **Clarified.** The v4 chapter's decision, on the page and in the README, adds: "The three study arms were built only to separate the change into steps, and were never candidates for adoption." (the registry's status reason; P51) |
| 4 | Which result is "the headline": v4's research result beside the v1 demo (D01/P01–P02) | Advisory: the opening pairs research v4 with released v1 by design (Observable outcome); each half is labelled |
| 5 | "1 policy", "12 policies" and "8 policies" (D01, D03) | Advisory, a recurrence of A-PRES1-10: the census sentence says the chart's rows are not the census |
| 6 | "the final model" is undefined and undated (D01) | Advisory: the release rule's registry wording, unchanged since PRES-1 |
| 7 | The observed price leaves the 80% band on the showcase day (D01) | Advisory: v1's historical replay, part of the unchanged product documentation |
| 8 | −0.0301 in the headline and −5% below it; the ratio interval cannot be checked by hand from the page (D01–D02) | Advisory: the two are the rule's unit and the share of v3's score; the bootstrap settings now state that v4's percentage interval is the ratio's (P08, P18) |
| 9 | The point-error score, the interval score's level and the similar-day naive are not defined precisely (D01–D03) | Advisory, A-PRES1-18 recurrence |
| 10 | The targets' values (0.592 / 0.575) are not printed (D03) | Advisory: the dashed line and the threshold in words; the value table carries the distances |
| 11 | The timeline runs oldest first, the cards and chapters newest first; the v2→v3→v4 story appears three times (D04–D07) | Advisory: PRES-2's architecture (A3, A4), unchanged |
| 12 | "the protocol's comparator" and "the protocol did not test that pair" (D05–D06) | Advisory |
| 13 | "August 2022 peak", "2022 crisis period" and "crisis window" overlap (D08, D11, D15) | Advisory: different windows, each named for its own result; v4's stress-period detail states that the peak is 17 days inside the crisis period |
| 14 | A unit switch in v3's per-period chart; "+0.0000039: not equivalence"; "confirmatory-style, not power-qualified"; "delu-cp2"; "the trained champion" (D11, D13–D18) | Advisory: unchanged historical chapters and product text, byte-identical to the published page |
| 15 | The GFS attribution names v3 only, though v4 uses the same weather (D18/P29) | Advisory, A-PRES3-7 (the Owner's wording; it also feeds the Space cards and the v1 demo's claims) |

Only observation 1 is a violation of an effective rule (PUBLISH_RULES §2). Observations 2 and 3
changed two sentences in the v4 chapter.

## The reader's answers, as given

The reader's reply, preserved without edits. The one character sequence the notification escaped,
`&lt;`, is restored to `<`.

```text
1. What is the headline result, with its numbers?

The top card reports a research result, not the product. v4 (v3's blend plus a three-block LightGBM) beat v3 on both error scores.
- D01/P01: "Met the adoption rule set before the experiment: both error scores improved on v3's (v4 – v3: −0.0301 [−0.0368, −0.0228] on the point-error score, −0.0266 [−0.0327, −0.0204] on the interval score; 1 policy tested against the rule)."
- As a relative change, D02/P03: "−5% [−6%, −4%] on the point-error score and −5% [−6%, −4%] on the interval score, with 95% confidence intervals."
- As levels, D03/P04–P05: v4 scores "0.536" on the point-error score and "0.506" on the interval score, as a ratio to the naive forecast. v3 scores 0.566 and 0.532.
- In money terms, D04/P06: "v4 4.9–15.0 EUR/MWh in the four ordinary periods and 47.0 EUR/MWh in the 2022 crisis period; the similar-day naive 8.6–30.5 and 86.9 EUR/MWh."

The only held-out result on the page belongs to the released model, v1. D14/P24: "v1 beat the similar-day naive: MAE 25.9 against 27.8 EUR/MWh, and mean pinball loss 6.7 against 13.9 EUR/MWh."

I had to decide for myself which of these is "the headline". The page leads with v4's step over v3, which is the weaker class of evidence.

2. Against what?

- The comparison is paired against v3. D05/P08: "Comparator: Set in advance: v3 itself, on identical hours."
- Every score is divided by a naive forecast's score. D03/P06: "Each score divides a model's error by that of a simple similar-day forecast in the same period, which therefore scores 1.000."
- The absolute bar is set by the strongest benchmark. D03/P04: "each error score at least 10% below the strongest benchmark's, set on 2026-09-15" and "Daily LEAR: the strongest benchmark, a linear model refitted daily."
  - By my arithmetic, v4 is about 19% below daily LEAR on the point-error score (0.536 vs 0.658) and about 21% below on the interval score (0.506 vs 0.639).
  - D02 notes that "a policy's distance from them is a point comparison". No confidence interval is shown for v4 against daily LEAR.
- The generations form a chain of comparisons: v2 against daily LEAR (D06), v3 against v2 (D05), v4 against v3. There is no direct test against v1. D06/P11: "No paired interval for v2 against v1 exists: the protocol did not test that pair."
- v1's holdout is compared only with the similar-day naive (D14).
- Daily LightGBM is also shown as a benchmark: 0.784 and 0.740 (D03).

3. How sure are we, and on what class of evidence?

For v2, v3 and v4 the evidence is historical backtesting only, after model selection:
- It uses paired 95% bootstrap confidence intervals over "the same 10,747 historical hours over 448 days", with scores averaged over five test periods (D03/P04).
- Each result is labelled "Development · post-selection: development evidence, not a test on new data" (D02/P01). D02/P04 adds: "Meeting the targets is a development diagnostic, not a product qualification."

For v4 against v3, the intervals are well clear of zero. D08/P14: "Both paired differences' 95% confidence intervals lie below zero, no test period's paired interval lies wholly above zero."

The page states its own limits on v4:
- There is no evidence that the block structure matters. D08/P15: three-block vs pooled LightGBM gives "point-error score +0.0050 [−0.0084, +0.0142]".
- v4 does worse at the 2022 peak. D08: "MAE 50.1 against 47.5 EUR/MWh."
- The v3 step shows no demonstrated gain on the crisis period taken alone. D11: "−3.2 [−6.1, +0.037] EUR/MWh."

The result was selected from a search on the same data. D03: "12 policies were tested against them." The page does not say how the bootstrap was built (block bootstrap or not, block length). That detail is in a closed section, "Bootstrap settings and the five historical test periods" (D04).

For v1:
- The evidence is a one-shot, pre-specified 90-day holdout, labelled "Confirmatory-style, not power-qualified" (D14/P24).
- The Diebold–Mariano test gives "p < 10⁻⁶" on pinball loss, but "it tests the probabilistic forecast, not the MAE difference" (D14/P25). So the MAE gain (25.9 vs 27.8) is not tested.

There is no live or forward-looking evidence yet:
- D16: "Live operation · planned".
- D15: "Planned, not evaluated … then an evaluation of the selected model under a frozen protocol and prospective monitoring."

Net: the ranking on the historical periods looks solid. Only v1 has been tested on new data, and v1 is the weakest model on the historical periods.

4. What does the demo run, and why not the best model?

The demo runs v1, "Demo v1 · released LightGBM" (D01/P01). D01/P02: "The demo runs the released model, v1. Research generations are not released one by one; only the final model, after its one-shot test and live run, replaces the released one."
- It runs in the browser: "about 57 MB on a first visit. A forecast appeared after 18.3 s in Chrome 153 on a Mac."
- The embedded chart is "a historical replay, not a live forecast" for 2026-09-06 (D01/P02).

Why not v4: v4 has only historical, post-selection evidence, with no one-shot test and no live run. D09/P15: "the released model, v1, did not change."

The policy is defensible, but it leaves a tension. The model being demonstrated scores worst on the historical periods:
- "1.052" on the point-error score (D03)
- "28.58% worse than the naive's, pooled over all days" (D15)
- "Over the August 2022 peak weeks its 95% interval covered 0.194 of outcomes" (D15)

The page does not say what "the final model" will be, whether v4 is the candidate, or when that decision comes.

5. What was tried and dropped?

- Recalibrating v1's intervals: "Calibration experiment · Not adopted · Recalibration alone was not enough: the model itself had to adapt" (D07/P12). D12/P20 adds: "Recalibrating its intervals improved coverage, but the improvement was insufficient."
- The model comparison study: "Model comparison study · Not adopted · No policy met the criteria; the study informed v2's blend of two LEAR forecasts" (D07/P12).
- v1's design, replaced in research: "v2 replaced its LightGBM quantile model and fixed-window calibration" (D06/P11).
- v2's pooled-interval control, which served as a control and was not chosen (D12–D13).
- Other study arms: pooled LightGBM with weather and normalized three-block LightGBM "met them too" (D03), yet only v4 went forward. Normalized LEAR (0.672 / 0.646) appears as a "study arm" (D03). The page does not say why the three-block version was preferred over the pooled one, and its own numbers show no difference between them (D08). "Each study arm against v3" is only a link (D09).
- Only the v1-to-v2 stage has a "not adopted" list. Nothing else is listed as dropped at later stages.
- Planned rather than dropped: "a distributional neural network, renewable-generation forecasts and model combinations" (D15).

6. What would you ask the candidate?

- Twelve policies were tested against the targets on the same 448 days, and the v2 blend came out of a study run on that data. How much optimism from model selection do you expect in the −5%? Do you have any untouched data left for v4's one-shot test, and how long will the test window be?
- How were the bootstrap samples drawn: blocks by day or week, and what block length? With only five test periods and one crisis period, how much do the intervals reflect differences between periods?
- The three-block and pooled LightGBM are indistinguishable (+0.0050 [−0.0084, +0.0142]). Why ship the more complex version?
- The adoption rule was set on 2026-09-29 and the v4 evidence was frozen on 2026-09-30. Had you seen any v4-arm results before setting the rule? Why did the rule change from v3's "joint improvement rule … and both accuracy targets" to v4's "four conditions", with six screening criteria besides?
- v1 scores 1.052 in one place, "28.58% worse" pooled in another, and beats the naive on the holdout. Explain the gap: which window was the holdout, how much does the crisis period dominate, and why is the MAE difference not tested?
- Interval coverage: v3's pooled 95% coverage is 0.9377, below nominal. What is v4's coverage by regime, and especially in the crisis weeks where v1 covered 0.194?
- The August 2022 peak got worse with v4. What is your plan for a shift in price level? Would the normalized arms behave better?
- Leakage and timing: which GFS run ("the GFS run of the day before") is used, and is it really available before the day-ahead auction closes?
- You say "AI agents assisted with implementation, analysis and documentation" (D17). Which parts did you do yourself, how did you check what the agents produced, and who performed the "Review verdict"?
- Define precisely the point-error score (MAE ratio?), the interval score (at what nominal level?) and the "similar-day" naive.

Things that confused me:

- D01/P01: The page opens with v4's research result right next to "Demo v1 · released LightGBM", so it is unclear which one is the headline. On the phone (P01–P02), the demo button and the "demo runs the released model" note sit below the v4 card.
- D01: "1 policy tested against the rule" uses "policy", which is only defined later (D03: "Policies: the models and variants tested").
- D01, D03: The counts of policies conflict: "1 policy tested against the rule" (D01), "12 policies were tested" and "8 policies" in the chart (D03). D03 explains only partly: "The chart's 8 rows are not that census."
- D01: "only the final model, after its one-shot test and live run, replaces the released one." "Final model" is never defined, and no date is given.
- D01 chart: by eye, the observed price falls outside the 80% band for many hours (early morning and roughly hours 17–23) on the showcase day, and the page says nothing about it. Also unclear: which holdout "a held-out day" (2026-09-06) belongs to.
- D01 vs D02: The same result appears in absolute score units (−0.0301) in one place and as a percentage (−5%) in the other. Dividing the D01 point-error bounds by v3's 0.566 gives about [−6.5%, −4.0%], shown as [−6%, −4%]. That may come from computing the ratio in each bootstrap draw, but I could not check it from the page.
- D01–D03: "Point-error score", "interval score" and "similar-day naive" are never defined precisely. D03 says only that the interval score "accounts for both interval width and missed outcomes", with no nominal level.
- D03 vs D15: v1 is "1.052" on the chart but "28.58% worse than the naive's, pooled over all days" in its chapter. The explanation is behind the closed section "why v1 scores differently in its own report" (D04).
- D03: The target line is drawn but its value (about 0.592 / 0.575) is never printed.
- D04/P07–P08 vs D05/D07: The "How it evolved" timeline runs oldest first, while the cards and chapters below run newest first. The same v2→v3→v4 story is told three times: hero and compare section, adopted-changes cards, and chapters.
- D05, D06: "the protocol's comparator" and "the protocol did not test that pair". The protocol itself is never described on the surface.
- D08/P14: "passed the six screening criteria … so it met all four conditions of the rule". The relation between six criteria and four conditions is unclear.
- D08, D11, D15: "August 2022 peak" (17 days), "2022 crisis period" (the third period) and "crisis window" / "peak weeks" overlap, and I could not tell which is which.
- D11: The unit switches from score to EUR/MWh ("−3.2 [−6.1, +0.037] EUR/MWh") without warning.
- D13/P23: "+0.0000039: not equivalence". The seven-decimal precision and the phrasing are distracting.
- D14/P24: "Confirmatory-style, not power-qualified" is jargon, and the 90-day holdout's dates are not shown on the surface.
- D17/P28: "Experiment delu-cp2 holds v1's own runs". "cp2" is unexplained. "Each experiment below has its own full reproduction", yet the list has no entry for the calibration experiment.
- D18/P29: "the trained champion is a derived work of it". "Champion" appears nowhere else. Also, "The v3 research model's weather data" is attributed, although v4 uses the same weather inputs.
```

## Screens supplied (SHA-256)

```text
92ffb459251da5f27f6d7f4d2236ca036111d93ebc0dfd0b18e94435aa1af30b  D01.png
239c8edd46217cf93cb30c48ef46a3f5693dc576617d6193391a95cab4d0e64f  D02.png
ba127744dce076affbb1b785e1d0a1fb49fa1ecadd4014058f8bc1fb129a0b91  D03.png
a66a533551c7a81c302ab16d019e5b4a09ff1e01203fd5c9a8c536369b192d98  D04.png
a994296da3e2acd08a29900b280a4059e247ccb70ef6a311ec12c28085dcc11d  D05.png
6851edce0a7131157e8204068e35f6dea73b6e94c9d4f25b2aebece9c90e0ac7  D06.png
28a8e531eaf9b038e13fad9f252a54f4966bc3a91949b60ae7ac65741b6e912f  D07.png
fd01eb6f73fe47c1a96058d2ac0c710340f8b62328357cdb5f7e2831d4882c0b  D08.png
57a16afd98084ed398ce3cfb5b975577fe2f5022e52a5e7ae20c2a148572708d  D09.png
4735ef4124052d960114088ea0dcbc848d80415c12e19ff68f52301604f2f65f  D10.png
da4bbd9e7c113c6f6b42158bdb628184b422bbe197adb49308bb8f67fb33fcd8  D11.png
26508cdf6c4fd510e88c2533b136abba8357fbe0b8da82f7ba02a5a8b3bf5421  D12.png
08de64a6774e8f98821f5f7ae17d383f00c68f40e82a694e37344641a3c4d93e  D13.png
109cca8cb15c786503e343e513ccd47df211da03139b219bb756e2dd09ce948d  D14.png
7523162b458c37c041057641e44b53422c5b24fe01f53d6dd629ce194b6bca01  D15.png
bd5251710977a11c84d36128a35fb7a190f09e10e35c343a1308b4f23ce3f60f  D16.png
306073a74fd9c5bf44e16e04e8b85499230d644328567f6099104cd945c77b58  D17.png
e809eb7608688c779ee3b9e9f2f376e7ecc35c5d25596ac93fc2f53fc1620500  D18.png
43daba328da370c07f2c27c9653b0152713150d51a22dd44a23f52a106c88abd  P01.png
6de58d2680b90f55bde1b5dac11137e47e51c564fa1e91a5051206ee9b478f0c  P02.png
6372f858a495225ebe5c4b52a864d690c60d531756388fe0208c507c29e39dd9  P03.png
9ac841f4b6aee3625def43f7d58f1fd75084f13772f4d7366daf0d09eeb8e437  P04.png
607d15325866fde09e435c40743a3956b85fa6ffd5c2933de06578cf2cce4eea  P05.png
2a7f3d5338de9eec399d37b0cb7a6bcc8546bf27d76aab935587f6b36c36e415  P06.png
79dd85cfd20b696f9875b2461043b62f161137b43853cfc6e78b799b6cc846cf  P07.png
63d5d1bb990f1ef11bc677853c0e6f62c3ef02a84c2bc80fd85df786ab6a8857  P08.png
0806e4e97ee8d2ff2dded442d76ac55f12e718447a6762eba7fe3b4228c62cdb  P09.png
42ddc2db78b0a762189d86f7cc7d345a2302f55a89eefdc56c2d668422ac2dd2  P10.png
247e40f2d532e3a635a585e28e8df6d02b61a60029d19c2bf54bf69b2454afa5  P11.png
da9b5b09bf9c4e603c3b96c095003692dab3d36a0c79b61d4b274145c2059e5f  P12.png
13ca7f1af3b6fa6f249f1799fe0dba37292478026f4cb6ceaa587a21633f67af  P13.png
14eb7a65ac2c1859b477cb4ea8b69d75b2d1d02cfa5516c324fa7463c31f9439  P14.png
602dd910419384ae1ddbf3e97ea6e51682fd1574b08ccc3239a003b242cdaef9  P15.png
6a629098355159374bb8cbec3b43755ff52c454f840abd61812bca8906443d08  P16.png
2b54253794488ea5feefac90648b881dc85a604987ebe0719619376e2f0b4ac8  P17.png
169668a3f8f0eb431c75551baebf499a066ea19683d5c83249d22c3971ab1289  P18.png
f45950b67045d7df82bd57f2bdd35ea718199f497fea9c180ee8ad80b59a8669  P19.png
57938122a33b883122f7852293d14f0c5149bad73a8b1282bdeb3ac3d0693be7  P20.png
95de2e8b44beb3727f201ec502175780761c38e69ec6486c3a5ff106cf132a3b  P21.png
2ce6006dc666de0626f7116bf0e67d00a3ec4438f699d21a9af6dc5c25d6505f  P22.png
9040b5cbb828c0d02f9b0821a2fa71bc8f02f96fa252584ae32b02eb7e82b083  P23.png
ed41104e9e68609835b6e02f06daec5f6b90c75e38c2dbccc60608ef9490eba9  P24.png
910f4e3416f060e799ee6d10f49eebfeab20805254461237514759b0558270a3  P25.png
6f7b3868cbb96043f57fb70aa646f313ca01823078d53d773facf7d8fa9aa489  P26.png
c312ee442625049e021cc69153f1bbd532de8b795a1076d9cd2c6f0dfc595d31  P27.png
3a7b4def5aa5c81c24ee530dec02351a241deea94cea33b0c8d3488f4a3d4acb  P28.png
45dfee9d8933c25d530540d984064e2a74c5ff57c3f76df753d01c2ee7dc0622  P29.png
3371cb922ae79a8ec2b16c2e97830d8943bf86b10223daf9fb202e6cdc69cd6c  P30.png
```
