# PRES-2 — fresh reader (PUBLISH_RULES 1.0 §10.2)

**Outcome: answers 1–5 agree with the registry and the derived records, from the placements the rules
require.** The reader found one rendering defect the automated checks had missed — words run together
in three route labels of the v3 chapter — which is repaired, with a new release-check finding and its
negative control. Its other observations and answer 6 are advisory.

## How it was run

- **Page:** `docs/index.html` SHA-256 `47c74c458b20568c4dec3a21fb7d12d3cead35e5c55a5651d9ef712113361f8d`
  (commit `a5bca2f`; unchanged by the index write and the final build at `cf1280a`), served over HTTP,
  every disclosure closed.
- **Screens:** written by `scripts/check_reader_paths.py release` (record
  `pres-2-local-release-attempt-6.json`, `cold_reader_screens`), the page as a reader scrolls it, one
  viewport at a time, each step the viewport less the sticky header:
  - desktop, Google Chrome 154.0.8037.58 at 1440×900, 15 screens, step 844 px, supplied as D01–D15;
  - phone, Playwright WebKit 26.6 at 390×844, 24 screens, step 788 px, supplied as P01–P24.
  Copied under neutral names to `.local/tmp/fresh-reader/`; their SHA-256 values are listed below.
- **Reader:** one fresh agent, which wrote nothing in PRES-2 and was given no repository, project
  history, prior review, expected answers, chart locations or explanation: only the prompt below. Its
  transcript shows exactly 39 tool calls, each a `Read` of one of the 39 images, in the order D01…D15,
  P01…P24, and nothing else.
- **Date:** 2026-09-29.

### The prompt (verbatim, except that the 39 image paths are abbreviated; they are the files listed in order below)

```text
You are a reader seeing a web page for the first time. You have no other information about it, and you must not look for any: do not open, list or search any file or directory other than the 39 image files named below, do not run any command, and do not use the web.

The page is shown as screenshots taken while scrolling from the top to the bottom, with every collapsible section closed. There are two renderings of the same page: first a desktop browser (1440 × 900), screens D01 to D15; then a phone browser (390 × 844), screens P01 to P24. Read every one of them, in this order, with the Read tool:

/Users/djourno/Downloads/PJM/.local/tmp/fresh-reader/D01.png
[… the 39 paths, D01.png to D15.png, then P01.png to P24.png, one per line …]
/Users/djourno/Downloads/PJM/.local/tmp/fresh-reader/P24.png

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
(n − 1) × 788 for 844 px. Placements are attempt 6's.

| Question | What the registry and the derived records hold | The reader | Within the placement rules |
|---|---|---|---|
| 1. The headline result, with its numbers | v3 met both targets: at least 10% below daily LEAR; v3 14% below on the point-error score and 17% below on the interval score; the first of N = 8 (`derived.criteria.v3.*`, P20); against v2 −12% [−16%, −9%] and −14% [−17%, −11%] (`derived.change.v3.*`); scale 5.3–15.6 and 48.0 EUR/MWh, naive 8.6–30.5 and 86.9 (`derived.periods.*`) | All of it, each number with its metric (D01/P01; D02/P03; D03/P06), plus the chart ratios 0.566 / 0.532 and the paired differences −0.0783 and −0.0838 | Yes. The headline block ends at 800.6 / 801.3 px (desktop) and 628.6 / 628.7 px (phone), inside the first screen; the finding at 1,702.6 / 1,703.3 px (A2 limit 1,744) and 2,381.5 px (limit 2,420). **A1:** the reader tied 14% to the point-error score and 17% to the interval score on the first screen |
| 2. Against what? | Comparator of the targets: daily LEAR; v3's pre-specified comparator: v2 (also its predecessor); v2's: daily LEAR, not v1; the naive as normalizer; 10,747 hours over 448 days, equal-fold | All of these, including the predecessor/comparator distinction for v2 (D05/P09) and the population (D03/P04) | Yes. Daily LEAR is in the headline and defined directly beneath it (D01–D02/P01) |
| 3. How sure, and on what evidence | Development · post-selection; "development evidence, not a test on new data"; "a development diagnostic, not a product qualification"; distances are point comparisons; v3–v2 intervals exclude zero; the crisis-period point gain not demonstrated; v1's holdout "confirmatory-style, not power-qualified" | All of these, with quotes (D01–D03, D07–D08, D11–D12; P01, P04, P12–P13, P19) | Yes. The badge is on the first screen; the caveat is in the comparison panel above its chart |
| 4. What the demo runs, and why not the best model | The released model, v1; the release rule; the replay is historical, not live | Both, with the rule quoted (D01/P01–P02), and the startup line | Yes. The rule is beside the demo action, outside any disclosure (`release_rule_in_disclosure` false) |
| 5. What was tried and dropped | The calibration experiment and the model comparison study, not adopted (2026-09-16); the pooled-interval control (2026-09-23); the study arm; no rejected experiment between v2 and v3 | Both branch cards with their reasons (D06/P10–P11), the pooled-interval control, the normalized-LEAR arm, and "No dropped experiments are shown between v2 and v3" | Yes. The branch group follows the transitions, headed apart as "Experiments not adopted between v1 and v2" (A3, A4) |

Answer 6 is advisory. It asks about: an interval for the distance to the target and selection among
eight policies; when and why the targets were set; why v1 is the released model and what v3 must
pass; the holdout's power and its naive comparator; equal-fold against pooled scoring; the missing
fuel-price inputs and the next level shift; the GFS cycle's availability before the auction; the
bootstrap design and the 10,747 hours; how much of the interval-score gain is narrower intervals; the
agents' part and the candidate's own; and who would use the forecasts. These are the return's
interview-capture triggers.

## What confused the reader, and what was done

| # | Observation (screen) | Disposition |
|---|---|---|
| 1 | Three "Explore these results" labels read "forv1,v2andv3", "day,v2againstv3" and "the2022crisis window" (D08/P14) | **A rendering defect, repaired.** The labels are links styled `inline-flex` for their 44 px target; each text run and version or date span became a flex item and the spaces at their edges were not drawn. The label is now one span (`scripts/build_pages.py::explore_routes`). The release check gains a finding for words that run together inside a flex or grid container without a gap (`COLLAPSED_SPACE_JS`); `pres-2-local-collapsed-space-control.json` shows it catches exactly these three labels on the page the reader saw, in both engines and both viewports, and none on the repaired page. A text comparison could not see it, because the text has the spaces |
| 2 | The two headline percentages use different baselines (daily LEAR, point comparison; v2, with intervals) and look alike (D01–D02/P01–P03) | Advisory. Each value names its metric (A1) and its comparator; the reader answered both correctly |
| 3 | "the distances are point comparisons" was understood only later (D01/P01) | Advisory; the wording is the standard's definition line |
| 4 | "8 policies" against "7 policies" on the chart; five tested policies are named only inside a disclosure (D01, D03/P04, P06) | Advisory, a recurrence of A-PRES1-10 that P33's census line now addresses on the reading path; the exact census stays in depth |
| 5 | v1's 1.052 on the chart against "28.58% worse" pooled (D03/P05, D12/P19) | Advisory, A-PRES1-11: protected v1 statements; the reconciliation is in the definitions disclosure |
| 6 | The point-error metric, the similar-day rule and the interval score's level are not defined on the open page (D01/P01, D03/P06) | Advisory, A-PRES1-18 recurrence |
| 7 | "Normalized LEAR" and "study arm" are unexplained (D03/P04, D09/P15) | Advisory |
| 8 | "crisis window", "2022 crisis period" and "August 2022 peak weeks" may be different periods (D12/P19–P20) | Advisory: they are different windows, each named for its own result |
| 9 | The same v3–v2 comparison appears as ratio points, shares and EUR/MWh (D02/P03, D07/P12, D08/P13) | Advisory; each is labelled with its unit |
| 10 | "joint improvement rule", "no demonstrated joint preference", "per-period criterion" and "+0.0000039: not equivalence" are undefined (D05/P09, D06/P10, D10/P17) | Advisory; chapter texts from PRES-1 |
| 11 | "Did the intervals get more reliable, or only wider?" does not fit, since v3's intervals got narrower (D08/P14) | Advisory: the plan's §5.3 reader question for this chart; the answer beside the chart says narrower, with coverage slightly lower |
| 12 | "only the final model … and live run": "final" is undefined and undated (D01/P02) | Advisory: the release rule's registry wording |
| 13 | "a held-out day" does not say held out from what (D01/P02) | Advisory |
| 14 | "Confirmatory-style, not power-qualified" is unexplained (D11/P19) | Advisory: v1's protected label (§3.1) |
| 15 | "the trained champion" (D14–D15/P23–P24) | Advisory, A-PRES1-15 recurrence |
| 16 | Whether the twelve topic cards stay on the page; the note under "Explore this forecast" missing on the phone (D02/P03, P02) | Advisory: internal routes carry no external-link arrow; the phone hides that note since PRES-1 (`265661d`) to keep the opening within its screens |
| 17 | On the phone, "targets:" and its "–" sit on the dashed target line (P04–P05) | Advisory: the overview chart's phone variant from PRES-1; its SVG is part of the published MLflow export, which PRES-2 keeps byte-identical |
| 18 | The desktop sidebar keeps v1 highlighted through the sections after the chapters (D11–D15) | Advisory: the generation navigation marks the last chapter passed |

Only observation 1 is a violation of an effective rule (A5's descriptive route; §2's plain reading
path). It changed three labels on the reading path, restoring their spaces; answers 1–5 do not depend
on them.

## Screens supplied (SHA-256)

```text
85297c7ce6ba315c0075315b7e56bc4a8276cf13c7e4e4c6e22e734f459c0cb7  D01.png
a97bf27bff9327bfee16baf311356a4d15ead78ebb7216fc91a7c8f859d9087e  D02.png
96b10bd2b9828f0db15c99c50d894005dd25e1290eeeb8717c1cd9fd117125ca  D03.png
83554c04749d9fad591503a99b38a614794438e21229a63182166502355951d6  D04.png
e5d75645f5ea32a7e5e01828b06214feb467db8154a49d06f54aa11b04c6a237  D05.png
bb855a83143643b7757c7d3297c816827b9bf1004f125cb1c17ed19a4df899a5  D06.png
6f8f62a8e997c39b4377b6856f122245d60347cc9c35bf3a3298a4f378680b69  D07.png
479a78ebbfd452dd097b3148c1c2e659a6eb7a5ca378bdebff631562fac92719  D08.png
7cc34e26a73140dc08283022cea7f613131083c8d59c0a7b2d391ad970db9075  D09.png
cdcc53607bb0072e8c429fdd90dadfde7650be0d6e4dd621fc175395c3e9fea8  D10.png
2907843f4d629e5a4fb6e0c3de91b12fe9faa49e36ab0af57146b72a66f80a27  D11.png
588867a6ac38f7a7cff27ee70e6b777a6ac3a1e1bfa9ea6a32a9a8c3774a1b06  D12.png
5df1075be273cd249c801dbec38a3b595e6ef04670ad1b6ec3a6dc01adfeacce  D13.png
dceab0b19c8d9dc68a606fe9eb8bd7c048d1890907fcd1825678f08539d443f5  D14.png
f5f9e70980e405d69ed2cfd612648df7d07da520e7f20e2d35e8bca8b610c656  D15.png
ac7c092cd1d507336765efafcb8c5be3d4970000679c5e81bb97d0ea1f5162fe  P01.png
32149a8da589c7864a26d7b3174cdee88f0271949829b0525db3c05768888a43  P02.png
8468a21e4a4fbfbcf68af03b1d11063ff1b79ed3aad37f0a3343f6b1c20461a9  P03.png
fef697bae5d390a443788656b1156008198197b821cc296e39282f19379456be  P04.png
9781c7534562dc84e71f84968f1efc172cae49b0554036a41acc550d386874b1  P05.png
d0275920da3436279339770832b62a3b4b32e9fb5fbbc1b9f205492c5fcc04fd  P06.png
6d73a9b84522eb3f9c00b9c9210d9c95613b232f1b2fc6c24e4e78825c5989de  P07.png
5f8d66a02f3536b0b92ae9db56af4f442db149a40b25fa4eb78912ea50c91295  P08.png
5d4bd5875574ec09bb8b8f4f16c190a1dd0338c43e5b2899e2691a08b23b5854  P09.png
05fc374a5ca81c90eade543d5eb843ba5ecaea8137cbf50ac6366d05107c0139  P10.png
51497ad599b74dd12e9a8c9de3123ae0172d0b87dd4fb3f488122378492edd88  P11.png
2c2ec7b0c32253c5bb2f21b9c2523ed7f46571c7d138bb594872a105e2caddb7  P12.png
63e9a0fc823bceca1f972948ce1708a1abcf6edb023d51e7c113e8e83eadbe47  P13.png
d3865534416b3690fdf4e4eb3cc598c898699009349d8187f8b267027aca7081  P14.png
0720e4a2f1f618b32034ea34a6e60824dd751f08c06b614b9f2b98969cb8372f  P15.png
12377bc0adecac054cc625736b6ea2ef8ab5b69f83d17edd5516d562961d31fc  P16.png
e8fd50c56ae5f779e0cc5fbb694b06565a33b186ef9b4bfc80265e2b18629451  P17.png
8b01ebf61275b694fc902517a584c89c2629b1be43d4fbe9d97cb3d783a94f52  P18.png
55be925a2b1b7f43bf4b4dc51cb0235899daa1cea0eb699b54fdf47da3810904  P19.png
fa67850f42b583dc37ccb65da65d0fe255ba265b5906ebf718cc393598c060e7  P20.png
3f6bd0985256e211eed05f2ea67e0ff0074f818aea9eee5f39913eab3419108b  P21.png
6f270aa54cf200eedc26201390c38e06175c6dfe21eda3a7a1a878d5cdb5784e  P22.png
144c6f6050303242a4607ce5701f08753fd5a98c6ea850e6481e63a2a1519462  P23.png
2a17496c180db5c8aeeb27bc5bd9ee43c8e934885cecf67fa3a7aaf5c5972f2f  P24.png
```

## The reader's answer, verbatim

Unedited, as the agent returned it (12,008 characters, SHA-256 of the UTF-8 text `6ea1a1bd142b88b181ac8e0b1e9e78ebcd89f1629af55fb35f9ccfce1fc654b6`).

```text
1. Headline result

The headline is a research result, not the product. The page title ("Day-ahead electricity forecasts, with uncertainty.") makes no claim. The "Research" card says v3 (v2 plus three weather-forecast inputs) "Met both accuracy targets set before the experiments: error scores at least 10% below the strongest benchmark, daily LEAR (v3: 14% below on the point-error score and 17% below on the interval score; the first of 8 policies tested to meet them)." (D01, P01)
- Chart scores, as a ratio to the naive (lower is better): v3 is 0.566 on point error and 0.532 on interval score. Daily LEAR is 0.658 and 0.639. (D03, P04–P05)
- Against its predecessor: "v3 against v2, as a share of v2's error scores: −12% [−16%, −9%] on the point-error score and −14% [−17%, −11%] on the interval score, with 95% confidence intervals." (D02, P03) The raw differences are −0.0783 [−0.1006, −0.0570] and −0.0838 [−0.1044, −0.0655], and "every test period favours v3". (D07, P12)
- For scale: "v3 5.3–15.6 EUR/MWh in the four ordinary periods and 48.0 EUR/MWh in the 2022 crisis period; the similar-day naive 8.6–30.5 and 86.9 EUR/MWh." (D03, P06)

2. Against what?

- Normaliser: "Each score divides a model's error by that of a simple similar-day forecast in the same period, which therefore scores 1.000." (D03, P06)
- Target benchmark: "Daily LEAR: the strongest benchmark, a linear model refitted daily." Targets were "set on 2026-09-15". (D01–D02, P01)
- v3's pre-set comparator: "Set in advance: v2 itself, on identical hours". (D05, P08)
- v2's pre-set comparator: "Set in advance: daily LEAR, the strongest benchmark, not the predecessor v1; a pooled-interval control isolated the interval method". (D05, P09)
- Other references on the chart: daily LightGBM 0.784/0.740, normalized LEAR (study) 0.672/0.646, and v1's development replay 1.052/0.986. (D03, P04–P05)
- Data: "the same 10,747 historical hours over 448 days · error scores averaged with equal weight over five test periods" (D03, P04). "The third covers the 2022 price crisis." (D04, P07)
- v1's holdout is compared only with the similar-day naive. (D11, P19)
- Missing from the open page:
  - the naive's exact rule;
  - the point-error metric (MAE is implied by "For scale, as mean absolute error", never stated);
  - the interval score's nominal level;
  - the fold dates (inside the closed "Bootstrap settings and the five historical test periods", D04, P07);
  - any external or market benchmark.

3. How sure, and on what class of evidence

- v2 and v3 have development evidence only: "Development · post-selection: development evidence, not a test on new data" (D02, P01). "Meeting the targets is a development diagnostic, not a product qualification." (D03, P04)
- v3 beating v2 is solid within that class. It uses a "paired 95% confidence interval · identical hours" (D07, P12), and "Both confidence intervals lie below zero and every test period favours v3". (D07, P12)
- v3 clearing the targets is weaker. "the distances are point comparisons" (D01, P01), so the 14% and 17% have no interval. They were also chosen after 8 policies were tried on the same folds, with no visible correction for that.
- Stated as not established (D05, D08, P08, P13):
  - which weather input matters;
  - the crisis-period gain, where the "confidence interval crosses zero: −3.2 [−6.1, +0.037] EUR/MWh";
  - "Performance on new data".
- Calibration: at the 95% level, coverage is "slightly lower, 0.9377 against 0.9389". Both are under the nominal 95%. (D07, P12–P13)
- Only v1 has a held-out test, marked "Confirmatory-style, not power-qualified". It was a "pre-specified 90-day holdout" with a Diebold–Mariano test giving p < 10⁻⁶ on pinball loss against the naive. The page adds: "it tests the probabilistic forecast, not the MAE difference". (D11, P19)
- Yet on the development folds v1 "is 28.58% worse than the naive's, pooled over all days (… p = 0.948: no evidence of an advantage)". Over the August 2022 peak weeks its 95% interval "covered 0.194 of outcomes". (D12, P19)
- There is no prospective evidence: "Live operation · planned". (D13, P21)
- I could not judge the bootstrap design, because it is inside a closed section. (D04, P07)
- My read: confident v3 beats v2 on these historical folds; moderately confident it clears daily LEAR by the target margin; no evidence yet on new data.

4. What the demo runs, and why not the best model

- It runs v1: "Try the v1 demo" and "Demo · v1 · released LightGBM". (D01, P01–P02) v1 is "A LightGBM ensemble forecasting nine quantiles for every hour, calibrated into 50 / 80 / 95% prediction intervals, and shipped exactly as it was evaluated". (D11, P18–P19)
- It is an in-browser historical replay. "Runs in your browser: about 57 MB on a first visit. A forecast appeared after 18.3 s", and "Forecast and observed price for a held-out day. This is a historical replay, not a live forecast." The day shown is 2026-09-06, with a median and an 80% interval. (D01, P02)
- The "Built with" list names marimo, Pyodide and Hugging Face Static Space (D13, P21). That suggests how it runs, but the page does not say so.
- Why not v3: "The demo runs the released model, v1. Research generations are not released one by one; only the final model, after its one-shot test and live run, replaces the released one." (D01, P02)
- v2 and v3 are only "Adopted in research". (D04, P07) The route to release is "an evaluation of the selected model under a frozen protocol and prospective monitoring". (D12, P20)
- So the reason is the release policy, not accuracy. No date is given. The model on show ranks below the naive in the page's own chart (1.052). (D03, P05)

5. Tried and dropped

- "Calibration experiment · Not adopted · Recalibration alone was not enough: the model itself had to adapt." (D06, P10) Also: "Recalibrating its intervals improved coverage, but the improvement was insufficient." (D09, P15)
- "Model comparison study · Not adopted · No policy met the criteria; the study informed v2's blend of two LEAR forecasts." (D06, P10–P11)
- v1's approach was dropped in research: v2 "replaced its LightGBM quantile model and fixed-window calibration with an equal blend of two LEAR forecasts refitted every day". (D05, P09)
- The pooled-interval control was not adopted. v2 beat it only on the interval score (D10, P17), and normalized LEAR alone shows "not met". (D03, P04)
- Of the "8 policies" tested against the targets, only 3 appear on the chart (D03, P06). The other 5 are not named anywhere on the open page.
- The detail for each dropped experiment is inside closed "Question, result and evidence" sections. (D06, P10–P11)
- No dropped experiments are shown between v2 and v3.

6. What I would ask the candidate

1) What is v3's confidence interval against daily LEAR, and does its bound clear the 10% target, not just zero? How do you account for picking the winner of 8 policies on the same folds? Was v3 the eighth, and did the search stop once something passed?
2) You set the targets on 2026-09-15 on folds that were already in use. Had you seen daily LEAR's scores on those folds? Why 10%? v2 missed the targets and gained only 2% on point error, yet it was adopted. What exactly is the "joint improvement rule"?
3) v1 loses to the naive on development (1.052 on the chart; 28.58% worse pooled) and covered 19.4% at 95% in August 2022. Why is it the public release rather than daily LEAR? v1 never had a live run, so why must its successor have one? What must v3 pass, and when?
4) In v1's holdout, the naive's pinball loss (13.9) is exactly half its MAE (27.8). That is what a plain point forecast scores, so p < 10⁻⁶ mostly shows that having a distribution beats having none. Why not test against LEAR, or on MAE? What effect size could a 90-day test detect?
5) Why average per-fold ratios with equal weight? It gives v1 1.052 against 28.58% worse pooled, and it plays down the crisis fold. Do the rankings change under pooling? Which view matches how the forecasts will be used?
6) v1 failed on price level (−269.4 EUR/MWh bias), and v3's crisis gain is unproven. Why are there no gas or carbon inputs? Why did GFS weather come before TSO wind and solar forecasts? What happens in the next level shift?
7) v2 and its control use "the same blend", yet their point errors differ (−0.0017). How does the interval method change the point forecast?
8) Which GFS cycle do you use, and is it available before the day-ahead auction? How do you handle the switch from the NCAR archive to AWS and the GFS version upgrades? How are the grid values aggregated to DE-LU, and how often do the missing-data flags fire?
9) Is the bootstrap a block bootstrap over days, and with what block length? Why are there 10,747 hours rather than 448 × 24 = 10,752?
10) v3's intervals are narrower and slightly under-cover, so how much of the interval-score gain is under-dispersion? What is coverage by hour and by regime? On the featured day, 2026-09-06, the observed price visibly sits above the 80% band for much of the morning and the evening peak. Why that day?
11) "AI agents assisted with implementation, analysis and documentation." What did you personally build and check? Tell me about a decision where you overruled the agents. How did v1's report (2026-09-15) reach v3's verdict (2026-09-24) in nine days?
12) Who would use these forecasts, and what decision changes with a 12% lower error?

Things that confused me

- D01/P01 and D02/P03: the two headline percentages use different baselines. 14%/17% is against daily LEAR with no interval; −12%/−14% is against v2 with intervals. They look alike and are easy to conflate.
- D01/P01: I only later understood that "the distances are point comparisons" means no interval on 14%/17%.
- D01/P01, D03/P04, D03/P06: "8 policies" are tested, but the chart subtitle says "7 policies", only 3 of which were tested. "Policies" also covers references that were never tested, and 5 of the tested ones are never named.
- D03/P05 against D12/P19: v1 is 1.052 on the chart but "28.58% worse" pooled. The reconciliation is in a closed section, "why v1 scores differently in its own report". (D04/P07)
- D01/P01, D03/P06: the point-error metric and the "similar-day" rule are never defined, and neither is the interval score's level.
- D03/P04, D09/P15: "Normalized LEAR" and "study arm" are not explained, and which study is meant is not said.
- D12/P19–P20: "crisis window", "2022 crisis period" and "August 2022 peak weeks" may not be the same period. A −269.4 EUR/MWh bias cannot cover a fold where the naive's MAE is 86.9 (D03/P06), so the window must be narrower, but the page does not say so.
- D02/P03, D07/P12, D08/P13: the same v3-versus-v2 comparison appears in three units (ratio points, share of v2, EUR/MWh).
- D05/P09, D06/P10, D10/P17: "joint improvement rule", "no demonstrated joint preference" and "per-period criterion" are undefined. The phrase "+0.0000039: not equivalence" is also unclear.
- D08/P14: in the v3 chapter, the link "Did the intervals get more reliable, or only wider?" does not fit, since v3's intervals got narrower (D07/P12). Several link labels are missing spaces: "forv1,v2andv3", "day,v2againstv3", "the2022crisis window".
- D01/P02: "only the final model … and live run" leaves "final" undefined and gives no date. v1 itself had no live run. (D13/P21)
- D01/P02: "a held-out day" does not say what it was held out from.
- D11/P19: "Confirmatory-style, not power-qualified" is unexplained, and so is how a point-forecast naive gets a pinball loss.
- D14–D15/P23–P24: "the trained champion" does not say which model.
- D02/P03: it is unclear whether the 12 topic cards jump within the page or leave it. The explanatory line under the "Explore this forecast" link (D01) is missing on phone (P02).
- P04–P05: on phone, "targets:" and its "–" sit on the dashed target line, and the "–" reads like a tick mark.
- D11–D15: the desktop sidebar keeps v1 highlighted through the system, contribution and terms sections.
```
