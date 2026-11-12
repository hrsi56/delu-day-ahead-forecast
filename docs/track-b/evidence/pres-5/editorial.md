# PRES-5 editorial review

- **Commit reviewed:** `b20ee9d1dbfa052e687bd9338270435ad155db5d` (branch `gauntlet/pres-5`'s state). Published base for comparison: `main` at `3c8e158c`.
- **Checkout:** `/Users/djourno/Downloads/PJM/.local/worktrees/pres-5/editorial`, detached. HEAD was `b20ee9d1…` with an empty `git status --porcelain` at the start, on each resume and at the end.
- **Date:** 2026-11-12. The review began on 2026-11-06 and was resumed twice after usage-limit pauses. The coordinator's resume message moved the review date.
- **Reviewer statement:** a bounded editorial subagent. I authored none of PRES-5's changes. I worked read-only: no edit, stage, commit or push, and no network use. Scratch extractions were written only to the session scratchpad, outside the checkout. I did not open the Claude memory directory, `progress.md`, any syllabus, Track A or C material, or `docs/track-b/orchestrator-role.md`. No credential was read or printed.
- **Standard applied, with hashes I verified:**
  - PUBLISH_RULES rev 1.5, `1bc0c523…f94e`: §§1–6, §8, §10.1 and A1–A12, including §15's A1–A5 and A11.
  - The Publication Standard v1 it incorporates: §§1–7.
  - The brief `9eb2a584…ebc3`: Observable outcome and the complete checkpoint bar.
  - The binding rulings O25, O26/O29, O27, O30 and O34. A8's order is recorded as an open item and not graded.
  - Input hashes I verified against the brief: 4.7T protocol `337a102d…7c58`; CP-17 landing `7f90cb87…267b`; CP-17b landing `2b64f542…a72f`; CP-17c landing `89b65c84…4759`; CP-18b landing `fe191d89…efe2`.
- **Claim maps applied:**
  - `docs/track-b/research-content/pres5-claims.md` (`43323946…`): C601–C607, C701–C706, C801–C804, C901–C908, P60–P66, W49–W53.
  - `publication-claims.md` (`3ce4d0d5…`): P07, P11, P21–P26, P35–P36, P39, P52, P54–P55.
  - `cp24-claims.md`: C403, C420 and C427.
- **Surfaces reviewed:**
  - `docs/index.html`: `a27564ea…2f37`, 1,846,009 bytes. I read it as text and markup, with every disclosure closed as the reading path, then read all disclosure bodies.
  - `README.md`: `90895abd…729c`. I read the glance block and the research block, plus the hand-written v1-era sections where they conflict with them.
- **Files read:**
  - Rules and brief: `AGENTS.md`; `docs/PUBLISH_RULES.md`; `docs/track-b/publication-standard-v1.md`; `docs/track-b/evidence/pres-5/issued-brief.md`.
  - Claim maps: the three listed above.
  - Code: `src/delu_forecast/research_claims.py` (the PRES-5 blocks); `src/delu_forecast/registry.py` (`RELEASE_RULE`, `release_sentence`, `expected_routes`); `scripts/build_pages.py` (the opening, route coverage); `scripts/readme_research.py` (lines 169 and 342); `src/cp17/tools/refreeze.py`; `pyproject.toml`.
  - Records: `reports/pres5/a1-in-v5/{ratio-intervals.csv, metrics.csv, summary.json, parity.json}`; `reports/ddnn2/attempt-1/metrics.csv`; `reports/cp28/owner-summary.json`; `reports/rebaseline/cold-rerun-2026-10-15/presentation-v21-r16/publication-packet.json`.
  - Freeze and landing records: `docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md`; the CP-17b protocol revision (diffed against CP-17's); `docs/track-b/cp-17-landing-2026-10-28.md`, `cp-17b-landing-2026-10-29.md`, `cp-17c-landing-2026-10-30.md`, `cp-18b-landing-2026-11-05.md`.
  - The published base: `3c8e158c:docs/index.html` and `3c8e158c:README.md`.

## Checks that passed

1. **Outcome 1: v6 in v5's comparison**
   - **Population.** v6 is scored on v5's own population: "the same 10,747 historical hours over 448 days · error scores averaged with equal weight over five test periods". Stored-forecast coverage is 10,747 of 10,747 hours (`summary.json` `coverage`).
   - **v5's and the naive's rows** in `#overview-table` are byte-identical to the published base's. `parity.json` records `max_abs_difference` 0.0.
   - **Ratios recomputed from `ratio-intervals.csv`:**
     - against v5: −6% [−9%, −2%] and −11% [−15%, −8%] at 95%; [−10%, −2%] and [−15%, −8%] at 97.5%;
     - against the naive: −51% [−54%, −46%] and −56% [−59%, −52%].
   - **Chart differences** (−0.0295 [−0.0494, −0.0128]; −0.0563 [−0.0747, −0.0390]) agree with the ratios times v5's scores, 0.5223 and 0.4937.
   - **The information-set difference** (C904) is on the reading path, in `[v6.caveat.information]`: "The comparison shares the hours and prices, not the protocol."
   - **No adoption by v5's rule:** `[v6.reading]` says "v5's adoption rule was not re-run, and it adopts nothing here." W49 and W50 are respected.
   - **Absolute errors and coverage:**
     - v6's per-period MAE 4.5–13.4 and 43.2 EUR/MWh;
     - v5's 4.8–14.4 and 45.5;
     - pooled 95% coverage 0.9447 at 82.4 EUR/MWh, against v5's 0.9395 at 100.2.

     These match `metrics.csv`; v5's width in the record is 100.248.
2. **Outcome 2: CP-26's every-day results**
   - `#everyday` sits beside the five periods and is labelled "A separate population … never pooled with the five periods above · development, post-selection". W51 is respected.
   - Values match PK26 and X26:
     - v5 against v4: −1% [−1%, +1%] on both scores;
     - DDNN-2 alone against v5: −7% and −11%, a point comparison;
     - the GFS +6 h route: +14% [+10%, +16%] and +15% [+12%, +18%] (OS28 `gfs_note_headline`);
     - the table's EUR/MWh values and ratios to the naive.
3. **Outcome 3: CP-28's selection**
   - The rule (C701) is in `#v6-rule`: "All seven passed every analysis". Interval error 9.68 against 10.13 EUR/MWh.
   - p = 0.0042 is both A1's compound p and its Holm-adjusted p in OS28 `holm.primary14`. The six blends' 0.0007 is Holm-adjusted.
   - The arms table names the six other arms in words, "Not selected", without codes (O30).
   - The Holm conditionality is disclosed (C705).
   - The 18 fallback days were filled from v5 (OS28 `fallbacks`: `by_source` `v5`: 18), and none falls in the five periods (`summary.json`).
4. **Outcome 4: the freeze and 4.7T**
   - Freeze dates 2026-10-28, 10-29 and 10-30; the issuing host; the identity "begins 720fc581". The hash sits in the detail layer, as §8 requires.
   - `[v6.fresh.window]`, `[v6.fresh.terms]` and `[v6.fresh.rules]` agree with the protocol's §§1, 2, 4, 5, 6, 7 and 8:
     - the window, the one look, the control and the reference;
     - the descriptive comparators, the scores and the 0.995 margin;
     - the compound p ≤ 0.05;
     - the 7-day blocks with 10,000 replicates;
     - at least 60 of 90 days, otherwise inconclusive;
     - no runner-up, the window spent, a null result valid.
   - CP-17b's revision leaves those sections unchanged.
   - `[v6.fresh.meaning]` matches C804 and O29.
   - Descriptive routes "The freeze" and "4.7T, registered before the test" are visible on the reading path (A5).
5. **Outcome 5: the product**
   - The hero shows v6 "Final candidate · pending 4.7T" with the "Development · post-selection" badge (O27).
   - "Open the live product" links the Space and says "prospective evaluation in progress".
   - v1 is "the last released generation", with its demo at `/history/`, from the opening and from v1's chapter.
   - No live forecast, score or price appears. No number falls on a day after 2026-09-06; the later dates are 4.7T's window, decision dates and evidence labels. W52 and W53 are respected.
   - "Live product" is used only as the Space's role, as W53 allows.
6. **Outcome 6: the identity**
   - "v6 · DDNN-2 alone" appears on the rail, in the journey list, as the comparison's first row and in the chapter.
   - The A3 transition "From v5 to v6: DDNN-2 alone" carries its class: "Development, after selection; not 4.7T".
   - "A1 in the frozen records" appears where the identity is shown.
7. **A1 and terms**
   - Each headline number names its metric.
   - The terms directly beneath the headline define the errors, the selection rule, the final candidate and 4.7T, policies, the class and DDNN-2.
   - The comparison's terms define the error scores, the targets and daily LEAR.
8. **Precision and codes on the reading path**
   - Whole percents, one decimal for EUR/MWh, and at most four significant figures for ratios.
   - No `CP-n`, claim ID, `§` or underscore identifier on the reading path. Only "A1" (allowed beside v6's identity) and "4.7T" (the status term, defined) appear.
9. **Page and README**
   - The README glance headline and terms are identical to the page's (`README.md` lines 10–17), and so is the product line (line 19).
   - v6's README section carries the comparison, the rule, 4.7T's terms and their meaning.
10. **Other rulings and the base**
    - O34: no page effect found.
    - v5–v1 chapters are unchanged from the base, except the v1 demo link, now `/history/`, and the planned and system items.

Not checked here: O25's pixel identity of the archive's seven PNGs. That is a byte matter, not a text matter.

## Violations

**V1 (high): "the released model" routes land on v6's documentation.**
- **Locations:**
  - `#v1`, `p.chapter-links`: `<a href="#product">How the released model works, topic by topic</a>`;
  - `#reproduce`: "Each experiment below has its own full reproduction. To run the released model, see `<a href="#product-run">`Run this product`</a>`".
- **What is wrong.** `#product` now documents v6 ("The product the Space runs, v6 · DDNN-2 alone"). `#product-run` gives v6's `refreeze verify`. Both labels present v6's manual as the released model's.
- **Rules:**
  - O26 and O29: "How the product works" documents v6, and v1's manual stays in v1's chapter, its archive and the history.
  - O27: v1 is "the last released generation".
  - W53: v6 is never called the released product.
  - PUBLISH_RULES §5 / A4: a research leader is never documented as the shipped product.
- **Fix:**
  - In v1's chapter, relabel and retarget the link, for example "v1's original report, topic by topic" → `#v1-archive`.
  - In `#reproduce`, write: "To check the live product's frozen policy, see Run and check this product; v1, the last released generation, runs from its archive's instructions (#repro)."

**V2 (medium-high): the opening no longer says why the Space runs v6, and no release rule is stated anywhere.**
- **Location:** `div.release-rule[data-block=release-rule]`, which now holds only `[product.live]`; README line 19. The quoted text: "The Space runs v6 · DDNN-2 alone daily, frozen: prospective evaluation in progress. v1, the last released generation, is its historical demo, and the product again if 4.7T fails."
- **What is wrong.** The PRES-5 branch of the opening (`build_pages.py`, `if final is None` … `else`) and `readme_research.py:169` drop P22 entirely. Nothing tells the reader why an unreleased candidate is the product while v1 stays released: decision 28, going live before the test.
- **Rules:** PUBLISH_RULES §2's reader table, "Product identity: Why this demo runs this model, beside demo action, outside disclosures"; Standard v1 §1 (iii) and §5, "The release rule is stated once, from the registry"; §7.1.
- **Fix:** one registry-derived sentence on both surfaces, for example: "It runs v6 before its test by the Owner's decision of 2026-11-05, so that its forecasts are issued and scored prospectively; a generation is released only after it passes its one-shot test, so v1 remains the last released generation." The fix needs:
  - P61's extension by an Orchestrator ruling under decision 27;
  - `RELEASE_RULE` and `release_sentence()` updated so that "The demo runs the released model" is no longer said.

**V3 (medium): the headline's bracketed intervals carry no label, and its percentages no comparator-share label.**
- **Location:** `dd#headline[data-block=headline]`; README line 10. The quoted text: "against v5 on all 2,068 development days, −7% [−9%, −5%] in point error and −11% [−13%, −9%] in interval error; 7 policies tested against the rule."
- **What is wrong.** Neither the bracket's level nor its kind is stated, and no term beneath defines it. The bracket stands next to "interval error", so it reads as a forecast interval. Everywhere else on the page these brackets are labelled: "descriptive 95% intervals" in the transition and in the arms table.
- **Rules:** PUBLISH_RULES §3.2, "with its 95% interval" and "Intervals of estimated differences and forecast intervals must have distinct labels"; Standard v1 §3.3(b), "Its label reads 'as a share of <comparator>'s score'"; P60, "with its descriptive interval".
- **Fix:** "…−11% [−13%, −9%] in interval error, as shares of v5's, with descriptive 95% intervals; …", or a headline term: "Brackets: descriptive 95% intervals of the change, not forecast intervals."

**V4 (medium): the live product's startup metadata is incomplete.**
- **Location:** `p.startup[data-block=product.live.startup]`. The quoted text: "It opens with about 0.55 MB of the day's records, measured on development data; the training window loads on request."
- **What is wrong.**
  - No measured start time, device or browser, measurement date, or last-verified date is shown.
  - "0.55" is typed (`{s:size:0.55}`), not bound to CP-18b's record of 551,515 bytes. v1's former line bound both its size and its time to records.
- **Rules:** PUBLISH_RULES §7.1, "show download size, measured cold-start time, device/browser/date and last verification date" beside the action; §7.3 (A9), startup metadata beside the primary action.
- **Fix:**
  - Measure the public live Space's first visit after CP-18c deploys, in the A6 post-deployment step.
  - Bind its size and time to a release-check record, and show the browser and device, the date and the last-verified date.
  - Until that record exists, carry the gap in the packet as an open item.

**V5 (medium): the README's hand-written v1-era section makes current-state claims that are now false.**
- **Location:** README lines 448–449, 452 and 538, outside the generated blocks. I record them because the README is a PRES-5 surface and §8 requires its surfaces to agree.
- **What is wrong:**
  - Line 448 describes the report as "How the released model works, topic by topic — … a forecast replay, limitations and how to run it". The report now documents v6.
  - Line 449 links the Space root as "The champion's own boosters, running in your browser under Pyodide | about 57 MB first visit". The root now runs v6, with a first visit of about 0.55 MB.
  - Line 538 says "Anything the Space or the static page renders over the holdout window 2026-06-09..2026-09-06 is that replay". The live Space renders v6's development records on those dates.
- **Rules:** PUBLISH_RULES §8, "No hand-written current-state claims" and surfaces agree on identity; O27, which says nothing may imply the Space runs v1 now.
- **Fix:**
  - Date the CP-3 table and put it in the past tense ("At v1's release, 2026-09-15: …"), and point its Space links to `/history/`; or replace it with a generated surfaces block.
  - Reword line 538 to name v1's replay at `/history/`.

**V6 (medium-low): the v1 archive's Space links now land on v6.**
- **Location:** `details#v1-archive`, closed. The affected links:
  - "The interactive demo — runs in your browser; the first visit downloads about 57 MB — runs the champion's own boosters", pointing to `https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast`;
  - "⚡ Interactive Space: the Space · the app directly", pointing to the Space root and to `https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/`.
- **What is wrong.** After CP-18c these addresses serve v6, so the archive's text names v1's champion while its links reach the live product.
- **Rules:** O27; §8 (valid link destinations). Invariant 24 preserves the archive's text and behaviour; that behaviour was to reach v1's demo, which now lives at `/history/`.
- **Fix:**
  - Retarget the three hrefs to `/history/` with the text unchanged, under an Orchestrator ruling that this preserves invariant 24's behaviour.
  - If the hrefs are judged protected, add one label line outside the archive text: "v1's demo, linked below as the Space, is now at the Space's History."

**V7 (medium): the regimes paragraph in v6's manual mislabels its population.**
- **Location:** `[data-block=product.regimes.periods]` in `#product-manual`. The quoted text: "Three regimes shape the development period: … The development hours split into 4,319, 2,112 and 4,316 hours across them; 465 hours, on 85 days, had a negative price."
- **What is wrong.** P39 and RT2 count the five test periods' 10,747 hours (4,319 + 2,112 + 4,316), not the development period of about 67,343 hours from 2019-01-01 to 2026-09-06.
  - In v1's manual, "development hours" was defined by subject 4.
  - v6's validation topic no longer defines it, so the sentence reads as a whole-period count and greatly understates negative-price hours.
- **Rules:** PUBLISH_RULES §3.2, "Show its dates, hours/days"; §5.1, subject 2 and shared material kept "after an applicability check"; P66.
- **Fix:** "Across v5's five test periods, 10,747 hours, the three regimes hold 4,319, 2,112 and 4,316 hours; 465 of those hours, on 85 days, had a negative price."

**V8 (low-medium): the README's research-block introduction is now false.**
- **Location:** README line 36, generated at `scripts/readme_research.py:342`. The quoted text: "The research results are development evidence after selection, on the same historical hours for every policy".
- **What is wrong.** v6's section (lines 44–78) reports CP-26's and CP-28's results on 2,068 every-day dates, a separate population.
- **Rules:** PUBLISH_RULES §3.2 (a changed population gets a separate comparison); W51; §8.
- **Fix:** "…on the same historical hours for every policy in the shared comparison; v6's section also reports every eligible development day, a separate population."

**V9 (low): a typed research percentage passes as a structural level.**
- **Location:** `[data-block=everyday.routes]`; README line 78. The quoted text: "without the load forecast, its point error rose by less than 1%".
- **What is wrong.** The template writes `{s:level:1%}`. It types a measured relative change, +0.075% in X26 `noload/v5`, as a structural level, outside the evidence chain.
- **Rules:** PUBLISH_RULES §3.4, "No hand-typed research number in a generator or generated output". Standard v1 §3.3 and §4 admit a % only as a derived record, a structural level or a v1 statement.
- **Fix:** bind the value to `derived.cp26.noload-v5.MAE` and render it under §3.4's near-zero rule (sign and two significant figures), or drop the number from the prose and leave it in the table.

**V10 (low): claim binding mismatch.**
- **Location:** `[everyday.title]` and `[everyday.finding]` are bound to C603 (`research_claims.py` lines 845 and 850). The `<data data-claim="C603">` elements wrap "−7%" and "−11%" in "v6's forecasts, DDNN-2 alone, have the lowest error on both scores, a point comparison: −7% and −11% against v5".
- **What is wrong.** That interpretation is C604's.
- **Rule:** PUBLISH_RULES §3.4, where claim maps bind the interpretation; Standard v1 §3.3, "mapped in the claim map".
- **Fix:** bind those elements, and the title's clause, to C604.

**V11 (low): a repeated caveat inside one transition summary.**
- **Location:** `#transition-v5-v6`.
  - `[transition.v5-v6.limits]` says "Selected by its own rule, never adopted by v5's; its forecasts come from a later, daily protocol; and 4.7T, from 2026-12-04, is its one test on new data."
  - `[v6.decision]` in the same summary repeats "It was selected by its own rule, never adopted by v5's."
- **Rule:** PUBLISH_RULES §2, "Put a caveat where it qualifies a claim, once… Avoid … repeated assurances".
- **Fix:** keep the sentence once, in the Decision. Make "Not established" list only what is not established: "Performance on new data: 4.7T, from 2026-12-04, is its one test. Equal information with v5: its forecasts come from a later, daily protocol."

**V12 (low): wording that expires.**
- **Location:** `[v6.product.limits]`, closed. The quoted text: "The results are development evidence after selection, and 4.7T is still to come."
- **Rule:** Standard v1 §1, Tone, incorporated by PUBLISH_RULES §1.1: "Caveats never use wording that expires, such as 'still to be evaluated'."
- **Fix:** "…development evidence after selection; 4.7T, from 2026-12-04, is its one test on new data."

## Recommendations

- **R1. Reconcile the two "DDNN-2 alone" identities (important).**
  - v5's reading path (`[v5.caveat.alone]`) says CP-24's study arm "DDNN-2 alone" scored −11% and −16% against v4 on these same hours. Its scores, from C427, are about 0.479 and 0.427.
  - v6, named "DDNN-2 alone", scores 0.4928 and 0.4374 on the same hours.
  - A careful reader will find the same name with different results. Name CP-24's arm distinctly ("DDNN-2 alone, v5's study arm") and add one bound sentence in v6's information caveat saying that, under v5's protocol, that arm scored differently.
- **R2. Disambiguate "the test".** The headline's "Selected by a rule set before the test" and `[v6.holm.note]`'s "The test was run only after the Owner saw…" both use "the test", which the page otherwise reserves for 4.7T. Write "before any result" and "The selection was run…".
- **R3. Cover the inconclusive branch.** The opening and README line 19 say "the product again if 4.7T fails", while the chapter says "does not pass". Use "does not pass" everywhere, because an inconclusive result also brings v1 back (C804).
- **R4. Cut the repetitions of "A1 in the frozen records".** It appears six times on the reading path, plus "arm A1, now v6" twice. Keep it in the hero term and the chapter header.
- **R5. Define or replace jargon on the reading path:**
  - "declared routes" in `[everyday.routes]`;
  - "arms" against "policies": the headline says "7 policies", the decision "7 arms";
  - "interval score" inside `[terms.daily_errors]`, which defines "interval error" in terms of it.
- **R6. Qualify duplicate codes.** `#overview-table` gives the code "A1" to both v6 and Normalized LEAR. Qualify them by experiment.
- **R7. Tighten the freeze wording.**
  - `[v6.decision]` "re-frozen, unchanged, on 2026-10-30" omits 2026-10-29. The policy identity changed at each re-freeze; only the forecasts did not.
  - `[v6.freeze]` "every fit identical bit for bit" should say "58 of 58 fits" (C801).
- **R8. Label the MLflow comparison link.** "Compare the runs in MLflow" sits under a 13-row chart, but MLflow holds 12 of those rows (P62). Say so in the label.
- **R9. Check the evidence labels at landing.**
  - The label "The final candidate's raw CSV rows, frozen 2026-11-06" must match the date of the `evidence/pres-5` tag when it is created (Standard v1 §7).
  - Consider linking CP-17b's protocol revision beside CP-17's.
- **R10. Make the run command reproducible.** `python -m cp17.tools.refreeze verify …` needs `src` on the path, because `src/cp17` is not among the packages in `pyproject.toml`. On a machine without the issuing host's runtimes it prints "verified, except N … (unchecked, not passed)", not "verified". State both.
- **R11. Widen the GFS attribution.** It is scoped to "The v3 research model's weather data". v4–v6 and the live product use GFS too. Widen it, and put GFS next to the product's data-source topic.
- **R12. Update the system section.**
  - "Evaluation and artifacts: Five historical periods, identical hours" omits the every-day evaluation.
  - "Dashed outlines mark planned parts" no longer refers to anything.
- **R13. Fix the planned-list sentence.** "Each item … would be compared with v6 on the same days" does not fit the 4.7T item, which compares v6 with v5 and the naive.
- **R14. Keep one precision per value.** Disclosures give 43.19 (`[v6.stress]`, `[v6.product.failures]`) where nearby text gives 43.2. Also correct the phrase "covered a share 0.9447".
- **R15. Add the selection result to the README.** README v6 lacks `[v6.selection]` (all seven passed; 9.68 against 10.13 EUR/MWh), which is why v6 was selected.
- **R16. Fix claim map C908.** It says v5's width is "100.3"; the record is 100.248. The page's 100.2 is correct.
- **R17. Say "eligible".** Write "every eligible development day (2,068 from 2020-12-29)" rather than "every development day", because the data starts in 2019.
- **R18. Describe the first visit accurately.** "0.55 MB of the day's records": O17 records that 85% of it is static development records. Say so.

**Note (A8, not graded).** The page keeps A4's order. v6's measured results sit as a topic inside the closed product manual, and there is no "Product results" or "Business insights" section. This bears on the open A8 ruling.