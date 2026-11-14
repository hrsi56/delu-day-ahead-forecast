# PRES-6 — fresh reader (PUBLISH_RULES 1.5 §10.2)

**Outcome: answers 1–5 agree with the registry, the evidence records and the derived records.** The numbers the reader
quoted from Product results (17.2 against 34.6 EUR/MWh with [15.4, 19.1]; 80% prediction intervals 51.7 EUR/MWh wide
covering 0.7826; coverage 0.4779 / 0.7826 / 0.9437; the bins' 0.6868–0.8685) equal their records, and it read the A8
order as built: the product opening, How the product works, Product results, Business insights, then the comparison.
Its confusions are dispositioned below: four touched PRES-6's sections and were repaired after the reading; the rest
concern sections PRES-6 does not change and are passed to the Orchestrator as open items (packet §10.3).

## How it was run

- **Page:** `docs/index.html` at `ef9681871d4d606075511a277c51fb6378917dcd`, SHA-256
  `9fc144b9287572a213505e8879843e0f5c8d8a918d9c2ef969900dcb317dd6b2`, served over HTTP from `127.0.0.1` with every
  disclosure closed.
- **Screens:** written by `scripts/check_reader_paths.py release` (the record
  `reports/presentation/release-checks/pres-6-local-release.json`, `cold_reader_screens`, 2026-11-14 16:27–16:36 UTC),
  the page as a reader scrolls it, one viewport at a time, each step the viewport less the 56 px sticky header:
  - desktop, Google Chrome at 1440×900, 34 screens, supplied as D01–D34;
  - phone, Playwright WebKit at 390×844, 61 screens, supplied as P01–P61.
  They were copied under neutral names to `/Users/djourno/Downloads/PJM/.local/tmp/pres-6/fresh-reader/` (local only);
  their SHA-256 values are listed at the end.
- **Reader:** one fresh agent. It wrote nothing in PRES-6 and was given no repository, project history, prior review,
  expected answers, chart locations or explanation: only the prompt below. It made 95 tool calls, one read of each
  image. Its transcript was not otherwise inspected.
- **Date:** 2026-11-14, after the editorial review's repairs.

### The prompt (verbatim)

```text
FIRST RULE: do not open, read or edit any file in /Users/djourno/.claude/projects/-Users-djourno-Downloads-PJM/memory/ (the Claude memory directory).

You are a reader seeing a web page for the first time. You have no other information about it, and you must not look for any: do not open, list or search any file or directory other than the 95 image files named below, do not run any command, and do not use the web.

The page is shown as screenshots taken while scrolling from the top to the bottom, with every collapsible section closed. There are two renderings of the same page: first a desktop browser (1440 × 900), screens D01 to D34; then a phone browser (390 × 844), screens P01 to P61. Read every one of them, in this order, with the Read tool. The files are in the folder /Users/djourno/Downloads/PJM/.local/tmp/pres-6/fresh-reader/ and are named D01.png, D02.png, … D34.png, then P01.png, P02.png, … P61.png (two digits, zero-padded), for example:

/Users/djourno/Downloads/PJM/.local/tmp/pres-6/fresh-reader/D01.png
/Users/djourno/Downloads/PJM/.local/tmp/pres-6/fresh-reader/D34.png
/Users/djourno/Downloads/PJM/.local/tmp/pres-6/fresh-reader/P01.png
/Users/djourno/Downloads/PJM/.local/tmp/pres-6/fresh-reader/P61.png

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

There are two headline figures, and the page leads with the relative one.

- The hero card (D01, P01) gives the result against v5: "against v5 on all 2,068 development days, −7% [−9%, −5%] in point error and −11% [−13%, −9%] in interval error, as shares of v5's, with descriptive 95% intervals; 7 policies tested."
- The first Product results card (D02, P03) gives the absolute result: "v6's mean daily point error was 17.2 EUR/MWh [15.4, 19.1] against the similar-day naive's 34.6." It adds: "Its 80% prediction intervals, 51.7 EUR/MWh wide on average, covered 0.7826 of the hours."
- The every-day table (D11) gives the full row for v6: point error 17.2 EUR/MWh, ratio to the naive 0.4974; interval error 9.7 EUR/MWh, ratio 0.4580.
- The model is "v6 · DDNN-2 alone", which D17 describes as "refitted every day on the 728 days before the forecast, issued at 11:00 Berlin time the day before delivery, and has been frozen since 2026-10-30."
- A second, smaller version of the result comes from v5's five test periods (D17–D18): "on the same 10,747 hours … −6% [−9%, −2%] … and … −11% [−15%, −8%]". Against the naive on those periods it is "−51% [−54%, −46%] … and −56% [−59%, −52%]".

2. Against what?

- v5, the previous generation. D13 says it was "Set in advance: v5 itself, the control of the selection rule, so the comparator is the predecessor."
- The similar-day naive, used as the yardstick for every score. D03 and P04 define it: it "forecasts each hour with the same hour's price the day before, or a week before for Mondays and weekends". D10 adds that scores divide by it, "which therefore scores 1.000."
- Benchmarks on the five-period chart (D09–D10): Daily LEAR, "the strongest benchmark", at 0.658 and 0.639; Daily LightGBM at 0.784 and 0.740; and v1's development replay at 1.052 and 0.986.
- The accuracy targets, which are "each error score at least 10% below the strongest benchmark's" (D09). D10 says v6 "was tested by its own selection rule, on every development day, not against the targets," although its points sit left of the target lines.
- The six other arms in the selection. They "also passed every gate and were not selected" (D13). Their scores are not shown.
- Nothing on the page compares v6 with an outside or commercial forecast or with published results.

3. How sure are we, and on what class of evidence?

All of v6's evidence is development evidence after selection. None of it comes from new data.

- Every v6 result carries the "Development · post-selection" badge (D01). D02 explains: "development evidence, not a test on new data."
- D03 says "v6 was chosen on these days" and describes the brackets as "95% confidence intervals of the mean, from 14-day block resamples." The hero calls its intervals "descriptive" (D01).
- D19 is explicit about reuse: "v6 was selected on every development day, four of these periods among them, after DDNN-2 alone had already scored best there."
- The five-period paired differences lie below zero at both 95% and 97.5% (D18), but the page calls this "A description, not a decision: v5's adoption rule was not re-run."
- D18 also says the comparison is not like for like: "v6's forecasts were made under the later daily protocol … The comparison shares the hours and prices, not the protocol."
- The one real test is still to come. D08 says "4.7T, which opens no earlier than 2026-12-04, is v6's one test on new data." D19 describes it as running "on 90 days whose data was opened only after its registration." The live record is "prospective evaluation in progress" (D01, D08), and no live numbers are shown.
- The prediction intervals cover slightly less than they claim (D05): 0.4779, 0.7826 and 0.9437 against nominal 50%, 80% and 95%. In the crisis the 80% interval covered 0.7531. Across forecast bins (D07) the 80% coverage ranges "from 0.6868 to 0.8685."
- The earlier five-period protocol had weak seasonal coverage. D14 and D21 say it scores "448 of the 2,654 days … 0 of them fall in October to December, and only 1 winter (December to February)." D14 adds that the same five periods were reused for a second neural-network decision.
- The only confirmatory-style result on the whole page belongs to v1 (D30): a 90-day holdout labelled "Confirmatory-style, not power-qualified."

4. What does the demo run, and why not the best model?

- The demo runs v6. D01 and P02: "By the Owner's decision, the Space runs v6 · DDNN-2 alone daily before its one test … A pass releases it; otherwise v1, the last released generation, is the product again."
- v6 is also the best-scoring model on every comparison the page shows, so the demo does run the best model the page reports.
- The released model is v1, which scores worst. Its recipe refitted daily scores 35.0 EUR/MWh against the naive's 34.6 (D11). So v6 is live but unreleased, and it runs early only because of the "Owner's decision". The page never explains who the Owner is or why the decision was made.
- One number on the page beats v6. In v5's experiment, the study arm also called DDNN-2 alone "scored 0.4785 and 0.4271 on these hours" (D18), against v6's 0.493 and 0.437 (D09). The page puts the difference down to protocol: v6 is "issued one or two hours earlier, refitted every day, with its own network searches." It does not say how much the earlier issue time costs.
- The page does not state the selection rule that chose arm A1 over six arms that "also passed every gate" (D13). It only links to it: "Selection rule: set on 2026-10-12 … Read it" (D02).
- The forecast chart in the hero is "A stored development-day forecast, not a live one" (D01). v1's own demo lives separately under the Space's "History" (D31).

5. What was tried and dropped?

- From v5 to v6, the ensemble went. D13: "v5's two LEAR forecasts, its LightGBM and the blend are dropped." The six other selection arms, all "blends of v5's members", passed every gate and were not selected (D13, D19).
- The calibration experiment, between v1 and v2, was not adopted: "Recalibration alone was not enough: the model itself had to adapt" (D16).
- The model comparison study was not adopted: "No policy met the criteria; the study informed v2's blend of two LEAR forecasts" (D16). The Normalized LEAR study arm scored 0.672 and 0.646 (D10).
- The pooled LightGBM member for v4 was not adopted. D16: "Both candidates were decisively worse than v4 in one test period, with a 95% interval wholly above zero." Their scores were 0.537/0.507 and 0.534/0.505 (D09).
- The DDNN member on v4, at one third of the blend's weight, was not adopted: "The improvement over v4 that the rule required was not shown, on either score" (D16). It scored 0.542 and 0.513 (D09). v5 later added DDNN-2 at one sixth of the weight.
- v1's LightGBM quantile model with fixed-window conformal calibration was replaced after the 2022 crisis.
  - D16: "After v1 failed in the 2022 crisis".
  - D31: on the development folds it was "28.58% worse than the naive's"; its 95% interval "covered 0.194 of outcomes" over the August 2022 peak; its bias was −269.4 EUR/MWh.
- Several study arms were never candidates for adoption: v2's pooled-interval control, v4's three study arms, and v5's arms "DDNN-2 alone and v3 plus a DDNN-2 member" (D14, D22). DDNN-2 alone later came back as v6.
- v4's split of the LightGBM into hour blocks was kept even though D14 says it "is not shown to contribute". v6 then dropped LightGBM altogether.
- Planned but not yet tried: "new input data and renewable-generation forecasts" (D31).

6. What would you ask the candidate?

- How much of the −7% and −11% is selection bias? You picked 1 of 7 arms on the same 2,068 days, after DDNN-2 alone had already scored best on four of the five periods. Did you correct for that, and what exactly is the rule that broke the tie when all seven passed every gate?
- v5's study arm called DDNN-2 alone scored 0.4785 and 0.4271, better than v6's 0.493 and 0.437. Is the earlier issue time costing about 3%? Why ship the protocol that scores worse?
- In the every-day re-baseline, v5 against v4 is −1% [−1%, +1%], so v5's five-period adoption does not hold up. What does that say about the five-period protocol, and about the v3 and v4 adoptions decided on it?
- What exactly is 4.7T? What are the pass criteria and the comparator? Does a 90-day window starting in December have the power to detect a 7% gain, given that v1's holdout was "not power-qualified"? What happens if only one score passes?
- Coverage is below nominal everywhere, 0.7531 in the crisis and 0.6868 in bin 2. Why not recalibrate, and who carries that miss in a bidding decision?
- A weather run six hours late adds 14% to point error. What does the product do when the GFS run is late?
- Why does the Space run an untested v6 "by the Owner's decision" while v1 is the released model? What does a visitor see that tells them v6 is unvalidated?
- Is 9.7 EUR/MWh of "interval error" consistent with intervals 51.7 EUR/MWh wide? Which interval levels and which scaling does the interval score use?
- No cost model has been run. How would you turn 17.2 EUR/MWh MAE into value, and do peak hours or negative prices matter more?
- How does this compare with published DE-LU results for LEAR and DNN models?
- The Contribution section says AI agents implemented much of this. Which parts did you build or check yourself?

Things that confused me:

- D01 and P01: v6 is labelled both "Live product" and "Final candidate · pending 4.7T", while v1 is "the last released generation". It is unclear what "released" means.
- "Owner" is never introduced (D01), and neither is the name "4.7T" (D01, D08, D31).
- D02: "re-baseline" is used before it is explained. "A1 in the frozen records" is internal jargon that appears throughout.
- D01 and D09: point error against v5 appears as both −7% [−9%, −5%] and −6% [−9%, −2%]. The reason, two populations (2,068 days against 10,747 hours), is only reconciled in D13.
- The page uses "point error" (EUR/MWh) and "point-error score" (ratio to the naive), and likewise "interval error" and "interval score", without making the difference obvious.
- D11: v6's interval error is 9.7 EUR/MWh against intervals 51.7 wide. The interval score's definition and level are not visible with the sections closed.
- The policy count keeps changing: "7 policies tested" (D01), "13 policies" (D09), "25 policies were tested" and "16 later policies" (D10), "among 7 arms" (D13).
- "Eligible" development day is never defined (D02).
- The end of the development period appears as 2026-04-07 (D14) and as 2026-09-06 (D03, D06).
- D01 calls its intervals "descriptive 95% intervals" and D03 calls them "95% confidence intervals … from 14-day block resamples". Whether these are the same method is unclear.
- v1 gets three different numbers: 1.052 for its development replay (D10), 35.0 for its recipe refitted daily (D11), and its holdout MAE of 25.9 against 27.8 (D30).
- D11's heading says "v5's gain over v4 is not shown there". This reads as "not displayed" when it means "not demonstrated".
- D05: "The naive's coverage is not in the committed rows". It is unclear whether the naive has intervals at all.
- D06: the page says "networks" in the plural, refers to "in-browser retraining", and has a grammar slip ("the holidays, day type and month group is used"). It is unclear whether DDNN-2 is an ensemble and whether the live product retrains in the browser.
- D07: the bin table uses only v5's test periods (8,587 hours on 358 days) rather than all 2,068 days, with no reason given.
- D13 and P25: "selected by its own rule, never adopted by v5's" is hard to parse, and the second "re-frozen" date is not explained.
- D14 and D20: "−2% [−3%, −2%]" puts the point estimate on the interval bound because of rounding.
- D02: the selection rule is only behind a "Read it" link.
- D18: the better-scoring v5 study arm is mentioned but not discussed.
- D34: "the trained champion" is never defined.
- D01: page-load timings ("1.86 s in Chromium 153") sit in the hero and are noise for this reader.
- Phone layout:
  - P09, P13 and P22: tables are cut off on the right, with a truncated caption ("every eligible developn") and missing ratio and coverage columns.
  - P18: v6's interval-score marker is clipped at the chart's left edge.
```

## Dispositions

**Repaired after the reading** (PRES-6's sections; commit after `14d67ea5`):

| Observation | Disposition |
|---|---|
| "Eligible" development day is never defined (D02) | **Repaired.** The caveat under the finding: "Eligible days are the development days from 2020-12-29 with complete prices and load forecasts" (CP-26's eligibility calendar, v21 §24.7 item 7) |
| The bin table uses only v5's test periods, with no reason (D07) | **Repaired, then corrected.** The first repair gave a false reason ("…the only hours whose prices are committed hour by hour…"; Integration review 1 found the snapshot holds every hour's price). The text now names the periods' dates and the true reason: "the population fixed before any bin was drawn" |
| "The naive's coverage is not in the committed rows" leaves open whether it has intervals (D05) | **Repaired.** "The naive's daily rows record its interval score but not its coverage, so none is shown." |
| A grammar slip, "the holidays, day type and month group is used" (D06) | **Repaired.** "the group of holidays, day type and month is used on neither day" |
| Phone: table captions cut off on the right (P09, P13) | **Repaired** for PRES-6's tables: the four new captions are short enough for a phone (the tables still scroll sideways, by design). P22 is PRES-5's every-day table, scrolled by design, its caption whole |

**Kept, with the reason:** "networks" in the plural (D06) is accurate (v6's daily fit is eight networks); "in-browser
retraining" names the study the attribution comes from.

**Outside PRES-6's sections** (the brief: the comparison and the later sections do not change, apart from R1–R7), passed
to the Orchestrator with a proposed ruling each (packet §10.3): the undefined "Owner", "4.7T", "re-baseline" and "A1 in
the frozen records"; the shifting policy counts (7, 13, 25, 16); −7% beside −6% on two populations; "point error"
beside "point-error score"; the interval score's definition when closed; the two development-period ends (2026-04-07 and
2026-09-06); "descriptive" beside "confidence" intervals; v1's three numbers; "is not shown there"; the "re-frozen"
date; "−2% [−3%, −2%]"; "the trained champion"; the page-load timings in the hero; **P18: v6's interval-score marker in
the comparison chart sits at the axis's left edge, partly clipped** (0.437 below the axis start).

## Screen hashes (SHA-256)

```text
b03cddd5015d6f72fd6e01654d5c2ac40bbdebe63beee71ff93a0f5cf990985d  D01.png
08fb9fd0bdca26294615f740ddf6f334832bffe633dbc352b87cf3016b909f35  D02.png
8f28c4f89255ae22e36637b9a9bd2f565a2cfc964c4393c77c69bd898053a016  D03.png
986d866af0e9eaafeba3fded59176ea94bf7e3ceabc39176fafa6a7378fdccd1  D04.png
6daac551d9d92f955d38afd52c2d5fb174a195f6aa7503d92f9c30b183f9b495  D05.png
cbb94ece2d81e96e722a6f720b3f96b4db7c2ed75111fba73febef75350a4741  D06.png
eca5b1d9d7460aa5e67c0534f040401e63ae3241977ea56cc1bb305a8fa6abed  D07.png
8b268ff7f3301a208021b884f3fbfaa881fb32234df90bd5c18a1d7577997d43  D08.png
24151f432ec4ca4ae5a344f298bf4dffa2b50e6cbf1be81ddfc7cf5f5d0cee7e  D09.png
9e1385abef1b56f936ea0d99337237c0c8c757d2db4f1483614535fee194904f  D10.png
9fa42a567a37165370db2e6e3f05ddb81f333b1622ada50f70350eecb62bd5ce  D11.png
067a78afe142016afd65f46b3b3dd8d5331b583a7be34bae61e27f7019644101  D12.png
c9bc97b64ac959422cef133153442c5614a1202aae2cac81d80e625c9337aefa  D13.png
6132a1d8f72cec4d17e832912c2b1d8eecad73cae3c66489e1a7282933f107af  D14.png
38bbd766c2eb3fd372ecaa0811dd33fdd58a114cba04ad527f42e4f420b3d915  D15.png
f02de2d0a76382f800a94ba999540824e858d6729d36b975b0e677c6bcf77901  D16.png
4bf1114f84497e0e0e116e43e925fd50332df9dd083124ec7e6b54b894fcfd77  D17.png
d9c5071fe64ceab203e79f2852251c2c41af2ce2032bdc1fc58d748b4b968f20  D18.png
de602448521287569515a97d326c838fedb09b151408e1d28bcec5a84c433372  D19.png
e1350a4a8a2730a1db74aa293f733ff1b01a349cced4ec01e7df5f0a25260c53  D20.png
add8a66e4e903a9ce68d549269c504bb16885fc321c52d579909966382bf7557  D21.png
706dc137545639190bc9f5e342c3fb2ccfd307fb8b9753df417af6ffacaa63d0  D22.png
9e110fcb209004185b250f64f2ff01a5d507b5e3d472504842a9e550128fd754  D23.png
d2030eef9972c5bfe4e1ea9658be8e2ba61e1145d43f6fc5eee6a6bacf7d59f7  D24.png
d005df2529c87fd12b135d8a934412c42cdfaa138e73eceab202da4c45e90fc9  D25.png
c37bfe7ae4bb17253d614bfd0818788d730291c28832cdf33d97452aadadc5ce  D26.png
01e369b18a0f67fb07d0ca6321409ae373d10f2d7166206ec270b4c16cc5ea39  D27.png
8d24dae78544e5bb46734f016ce78b5d52434b17b2f1aa7eb417f997349c4af7  D28.png
69d9fb9536f260ef19f9f57d349f91bd83d5dd8ea888224013362da96461100e  D29.png
fa4a1ec8d7b6f4be0842871c958c015f5ec44471ad01ac205d00f035c4724a35  D30.png
62d16f02d159324e6a82e00197e6154ed12373f0e280faee5f2994912c0b958e  D31.png
8a9e01cdcf243598e28eb3a7178a351274d12a7bfcf29a47905d50d135aed10a  D32.png
2b29899d140d247f707f78334f12c571da6091c09d3c9e9e9b8d8858669323d5  D33.png
5195c6adab5ad87fa2a8d60834ec3b28e14ff1609edb48ac9ba73120351f728b  D34.png
d59f82c73d9def1c65cb753340269e0e574fadd13176ad0b73f136236919d952  P01.png
20a17fdfe257618dbbd742d4965e295d111be90a5e6e58fb97530da1fc124a13  P02.png
1589f9976586bd280c6f20a75c04ad47b3d7f48fef1bfb63877b3c30f05742e3  P03.png
ef341ef0716cddb0084111e48b7fdba7e8a706f491a2286cb2d28285cdabe2ef  P04.png
fc1d7769fbc62edd11507ab6e455e6e920384efba7f3be383b3400b6285659a6  P05.png
9fb1c0fe390a37a103872478fbd40db52eb2aba026fe8cb202a15f5741b3d045  P06.png
8ed7336be9c9c69dda07aedbdbac265c1c82233f948b818733a3ecd4242947be  P07.png
e00f60ac06bd4d8e15f3b1a2549f4b402c88e0b01ab15977426653eb0329a652  P08.png
965f69037ea8b0835710ca5d693ebabbc58ed6823bf8c968ba17367ef6e9d43d  P09.png
d8de989086afd2c977f65c4428e4a6890914f46b6c42e1e2258d9e10e76032c1  P10.png
8c86cb149807d2666ddf0c10169a622469c5d53f7a4425a2faf8890579f2314b  P11.png
83955f7a79bb840064b7f7de489b2b576a307b70806e41c65b9b599371fbf165  P12.png
1c7d043b20b91275e8c84d80937b6d4a5c60724f03f6a1e7631b595483f3185b  P13.png
3903fd7cc8ed89840c18646df314d51a01f8f6a7364908bb60d01e8da7433780  P14.png
e84ca5fc1ed852e42dbda6062db4c75b72f77d47da98fd03a034a8c76a5835b4  P15.png
0362c0ba28d6deba277eacdcec0a1130b5139f018fcee930dbc01cadfa54a85e  P16.png
530b8b50cff2456aa044805115ba2a09411ff7350b951950b820c6aa1224e355  P17.png
8d5327b22fa4a47a7a911f421418245e211bccc72c9d3e67384ed533b2d90221  P18.png
287aee991e4235d0a7c80a1dece2e86e74e6b329e300d32953ca23333644addc  P19.png
58cfc2cce346059f1954a95c5331a86e8fe3aadf1f0c6e53b7ee5cabbda223fe  P20.png
0b3d533cc6ca50597c288611b1fb6c4b1626d48945641a1ad585a282e3085b56  P21.png
84bace82f89e08f34fb331bde9fd1c0f6b3b15928d5c50b0ddb795978007085b  P22.png
53effe912ab65ba212aa768059d23c980333a8992c204ec2f095c656195cc8e5  P23.png
37b650cb1eb7a0f951189f55ef21edc3fa75deb9634f21b5bc3bca6745b67adb  P24.png
ce36082ac7ce5db8fb2b0c6042c5169634b72b988e22c244399e562c097d09b4  P25.png
d514daae878df7b47f6f3938a168f0f6da0d9d0f65788205076e9d9efc7bdec3  P26.png
d3227de9e4c7677770ebbc698797eef830d38742dc289925851e5237c3e21c50  P27.png
93dfa96852b3dd86b1d7c09381a86f3c99c9ac01a54b1af7558862724659543c  P28.png
0f5d4b6df92b227e7cdd40e7f014b022e3facc361c5b050fce47b23df989db88  P29.png
c39a648003205e104cf966153119207498f24efb0e2b01a207f0e45eb535f441  P30.png
1ad1391aa4fd4808103b798f846239f4f4bf762ecf78be39bfa2be31f2694025  P31.png
7e8914837a412c44f235ba0d6f67f35b414c432eb298e7e93196cc59d2aca25c  P32.png
1aa4e755bdf9e7d8fdaff4a0394e4e4384f02d5592325cd82de42878db9eb473  P33.png
bf5cadebd23e3db2dfa0718d5b824cde288e83e9ce62d20f8d56f8dba12ecf0b  P34.png
773ac043761e4c9729f59835a12e5df668ea9a4f8193ff6c76619e958065e94e  P35.png
ad335c2d84847b1d14ae4d3b3e6bb318ffd152eb9a0d3598231139cd00fa7676  P36.png
038fbe1fb2829688c3f3e9a1f54c055066d12aa6353b52832989b08df3e86c53  P37.png
c8f5c376f2e6c3367b6db8db851007df5689a86e5976da7a282e4eb2aae21999  P38.png
aa295625947ca23b434600ef8b378adb3d969b94a84e86b65c52a7b92efcba40  P39.png
5f4874d7e672375d4d0abb58cd82f1fe3fe9e13f5a6eff03700f3b709a10cb80  P40.png
5d3a17e4b3cf04b2188bb97b2e847d812e58b2d57028edbcda927995f939a390  P41.png
1f2bc345654fb53dcd788c4afffa0a3c4df77d38f983200e96ce605f4ec30621  P42.png
8ff3c2b856ccc47b9f330d0905c6043c8411ffbb8fe4f35c340fe86f9aa40786  P43.png
960d807442282daab6e3646df4d89fe7c02c0ee550c176a8d98365fc60cd7845  P44.png
d7089506dc38360111947ae0b7d1ce3529a430c55e3b6651a8af7533c32c48b9  P45.png
5d5ee184f7e9872bb0f8fdfbe2614ecff290309b0caeba9d287a47967a8efb56  P46.png
d0c587c19879e2a251347798052a56b8646f8bc6a85d0a8d9eeede41f3cafe4d  P47.png
4c1805ee4905a04d3de34c8d339cbceaa2773f11c80680cf4be8d8bb7e2a4dc4  P48.png
bac51f25d9ddd78b5b67115075608c9cd2a8a7a9b9dda809ee1b2c7be8436361  P49.png
a95c9a344c632a35abbdb5b67d002c903bfd598f84d609644063a85d27a67100  P50.png
7f598fd1902a4d00c66fcef067ea807530c14ba97765124404353239b597059f  P51.png
b5bb7b23491510cc5202b5d7938d0427b33a2a5d60d1d950e9c24a81f6824242  P52.png
1d57118b20cbc9704ccfa9bcc2c235a27c09ef9f3fcf514088a0b18aea87d07d  P53.png
34de1a3f78738adefb75879c3f0df306b54357df902356e2217dfb8c2dce2578  P54.png
543894b0f3362bbd99da8da6986c3e8d8f74f40a4692ec2a05df829e6ae7034d  P55.png
fe2161d70e35c87ff3c998d978dbc65fa336e92cd7033353732de95c16bb41c2  P56.png
21ac5026cf1e10bcd0cfe92da0de0ff16461264f91b162b66e2df1b18881cd25  P57.png
1985db9b57202c83f31e98e76cbe863c56dd1d6a4483dc0248d5102f8a94328f  P58.png
8707db61da66e43aa9e974c0378380c0e51e554828e13bc75efea18840ea9a48  P59.png
4cdee539216fbdfb2f065e07ba2f683b57a80b919404d7c2f4a40d7030bc2295  P60.png
2a17496c180db5c8aeeb27bc5bd9ee43c8e934885cecf67fa3a7aaf5c5972f2f  P61.png
```
