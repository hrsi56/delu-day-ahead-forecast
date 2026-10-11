# PRES-4 editorial review

- **Commit reviewed:** `87cdceaa38983ae9a74204d5738b621a7dcb7dde`, detached checkout `.local/worktrees/pres-4/editorial`. Before and after the review, `git status --porcelain` was empty and HEAD was that commit. Published base: `e398a30bb53ecd4c397aad0f34fd122d42e74553`.
- **Date:** 2026-10-11.
- **Reviewer:** a bounded editorial subagent. I authored none of the PRES-4 changes and worked read-only. I made no edits, stages, commits or pushes in any checkout, and I did not use the network. My method was text and markup analysis of the built files: the default page with every disclosure closed, plus the README's generated blocks. I did no browser rendering, so A2 placement and visual checks remain with the browser review.
- **Standard applied:**
  - `docs/PUBLISH_RULES.md` revision 1.4, SHA-256 `ccfe6199…a80`, which matches the brief. I applied §§1–6, §8, §10.1, A1–A5 and A11.
  - The incorporated `docs/track-b/publication-standard-v1.md`, SHA-256 `7bb90c4c…68c`, which matches the brief. I applied §§1, 3, 4, 6, 7, 9 and 15.
  - The brief's observable outcome, as additional acceptance under PUBLISH_RULES §1.1.
- **Claim maps applied:**
  - `cp24-claims.md`: C400–C449 and W42–W48.
  - `cp22-claims.md`: C200–C238 and W28–W34.
  - `cp23-claims.md`: C300–C328 and W35–W41.
  - `publication-claims.md`: P16–P26, P33 and P51–P58.
- **Files read:**
  - At both commits: `docs/index.html` and `README.md`.
  - `AGENTS.md`, the router, as `CLAUDE.md` requires.
  - The two standards and the four claim maps above.
  - In `src/delu_forecast/research_claims.py`: the `v5.*`, `transition.v4-v5.*` and `branch.*` blocks.
  - In `scripts/build_pages.py`: `legend`, `is_branch_point`, `comparison_role` and `comparison_label`.
  - In `src/delu_forecast/registry.py`: the CP-22/CP-23 branch and arm entries, `status_sentence` and `inline_name`.
  - The coverage record in `src/delu_forecast/derived.py` (around lines 491–541).
  - In `scripts/readme_research.py`: its uses of `status_sentence`.
  - The issued brief's "Observable outcome", plus a grep of the rest of the brief for pinned hashes.
  - `reports/ddnn2/attempt-1/protocol.json`, its `rule_verbatim` field.
  - `reports/cp3/pages_build.json`, and the keys of `reports/presentation/mlflow_index.json`.
  - A grep of `reports/presentation/mlflow-export/cp23.json` and `cp24.json`.
  - I did not read `progress.md`, `orchestrator-role.md`, the syllabus or any Track A/C material.

**Checks that passed.**

- **Unchanged material is byte-identical to the base.** This covers the v1, v2, v3 and v4 chapter articles, the product documentation section, the v1 archive, the three earlier transition cards, the v1–v2 branch group, and the contribution and attribution sections. The fairness disclosure differs only in `data-record` source attributes (cp21 → cp24); its rendered text is identical.
- **Headline:**
  - It meets A1: each value names its metric.
  - It leads with the pre-specified verdict, the rule's date is beneath it, and it states "1 policy tested against the rule". It carries the class badge.
  - It quotes only the 97.5% decision interval, so W47 holds.
  - It renders identically on the page and in the README's "At a glance" block, with identical terms.
  - The opening pairs research "v5 · DDNN-2 added" with released "v1 · released LightGBM", and the release rule is unchanged.
- **Orientation:**
  - The comparison's finding states the 95% ratio intervals and the caveat.
  - The absolute context is correct for v5: 4.8–14.4 and 45.5 EUR/MWh.
- **Target and census sentences are arithmetically right:**
  - The census of 25 = 5 + 2 + 1 + 4 + 10 + 3.
  - 17 policies met the targets: v3 plus 16 later ones.
  - The 12 rows = 8 tested against the targets + 4 references.
- **The A3 card agrees with the chapter.** It covers predecessor, change, comparator (which is also the predecessor), the result at 95% and at 97.5%, the dated decision, and a route to the chapter's chart.
- **The chapter grammar is complete:**
  - the question-and-change diagram;
  - a paired chart at both levels, with a "no difference" reference line;
  - a one-sentence reading;
  - three not-established items;
  - the dated decision;
  - an evidence row whose "frozen" dates match the tags (cp-22 and cp-23: 2026-10-04; cp-24: 2026-10-10);
  - the five-item detail menu and the Explore routes.
- **The protocol paragraph matches `rule_verbatim`.** That covers conditions 1–5, condition 1's < 0 for the interval score and ≤ 0 for the point-error score, condition 4 at 95%, and the 97.5% split.
- **The two new branch cards carry the contract's fields:** question, comparator, the deciding result with 95% intervals and its fold diagnostic, "Not adopted", the month, a one-line reason and the evidence. CP-23's candidate is never called "v5" on the reading path.
- **The planned-work list matches the brief:**
  - 4.6 is removed.
  - A re-evaluation and new input data are added, unnumbered.
  - The wind and solar item drops "in-house".
  - 4.8 and "4.7T and live" are unchanged.
  - The comparator is v5.
- **The new reading-path text is clean.** It contains no checkpoint codes, claim IDs, §-references, underscore identifiers, typed status words or withheld-claim wording (W28–W31, W34–W40, W42–W46).
- The system view adds v5 and its reproduction route. The demo action and its text still name v1.

## 1. Existing-rule violations

### V1 · Terms on the reading path are used before, or without, a definition (Medium)

- **Clause:** PUBLISH_RULES §2: "Write plainly. Define a term at first use; do not add a glossary as a substitute." Publication Standard v1 §4: "Each term is defined where it is first used. Terms first used in the headline block are defined directly below it."
- **Observed.** All of the following are on the reading path with every disclosure closed.
  1. **"DDNN-2" and "DDNN".**
     - The opening's status pair reads "Research · v5 · DDNN-2 added". The terms beneath the headline do not define it.
     - The comparison chart's row "DDNN member on v4 (not adopted)" uses "DDNN" before any explanation.
     - The first explanation is in the A3 card, two sections lower: "added DDNN-2, a distributional neural network that forecasts the whole next day at once".
     - The acronym is never expanded anywhere on the page. Nothing says what the "-2" means: that this is the second DDNN design, after the branch "DDNN member on v4".
  2. **"Pooled member, averaged (not adopted)" and "Pooled pair (not adopted)",** in the comparison chart.
     - Neither label is defined anywhere on the page.
     - The census disclosure names the same identities differently: "v3 plus a capacity-averaged pooled LightGBM; v3 plus pooled normalized and raw LightGBM".
     - The CP-22 card refers to "the averaged member" and "the pair" without introducing either.
  3. **"decisively worse".** The CP-22 card's visible reason reads "The rule allowed no test period to be decisively worse, so v4 was kept as it was." The term is defined only inside v5's closed "Protocol and review" disclosure. The reason also never says that a period *was* decisively worse.
  4. **"the six original screening criteria".** The v5 reading sentence reads "v5 passed the six original screening criteria". These criteria are spelled out only later, in the v4 chapter: "the six screening criteria set before the experiments (the two accuracy targets, …)".
- **Impact.** The research headline's own model name is opaque on the first screen. The three new chart rows cannot be interpreted. A fresh reader cannot tell what CP-22 tested, or why it failed.
- **Repair.**
  - **(a) A new headline term** (a `terms.*` block, page and README glance, bound to C403 and C449): "**DDNN-2:** a distributional neural network (DDNN) that forecasts the next day's 24 hourly prices together, each as a full probability distribution; the second DDNN to be decided on, after the branch "DDNN member on v4"."
  - **(b) A new comparison term,** after "Daily LEAR" (bound to P57, C204–C206 and C306): "**Not adopted:** candidates of the two experiments tested against v4 and not adopted. Pooled member, averaged: one LightGBM for all 24 hours on the normalized price, averaged over four sizes, in place of v4's three blocks. Pooled pair: v4's normalized and raw-price LightGBM pair, each pooled over all 24 hours. DDNN member on v4: a distributional neural network with one third of the blend's weight. Their cards are under Experiments not adopted between v4 and v5." Link the final phrase to `#branches-v4`.
  - **(c) The CP-22 reason** (bound to C209, C211 and C212): "Both candidates were decisively worse than v4 in one test period, with a 95% interval wholly above zero; the rule allowed none, so v4 was kept as it was."
  - **(d) In `v5.reading`,** replace "v5 passed the six original screening criteria" with "v5 passed the six screening criteria set before the experiments (the two accuracy targets, interval coverage in each test period, the August 2022 peak against the benchmarks, each test period against the daily benchmarks, and complete forecasts)".
- **Acceptance.**
  - With disclosures closed, each listed term is defined at or before its first reading-path use, on the page and in the README.
  - The README glance terms equal the page's.
  - A2 placement is re-measured, because the terms list grows.

### V2 · The comparison legend calls the not-adopted candidates "study arm" (Medium)

- **Clause:** PUBLISH_RULES §3.3: "Controls, references, study arms, rejected branches and adopted generations are distinct kinds." PUBLISH_RULES §6: "No meaning depends on colour or hover alone. Use direct labels, shape/line style and readable values."
- **Observed.**
  - The three branch candidates use the same open grey circle as the visible legend entry "study arm". Those candidates are "Pooled member, averaged (not adopted)", "Pooled pair (not adopted)" and "DDNN member on v4 (not adopted)".
  - The chart's accessible description says something different: "Candidates of experiments that were tested and not adopted are open circles, as study points."
  - Everywhere else, the page uses "study arm" to mean "never eligible for adoption", for example "it was a study arm, never eligible for adoption". The candidates were eligible, and were rejected by their rules. The legend therefore contradicts both the registry kinds (one is `kind="branch"`) and the rows' own "(not adopted)" labels.
  - The open-circle mark is the Owner's decision D2 and is not in question. Only the legend's wording is.
- **Impact.** The main overview chart misclassifies rejected candidates, and sighted readers and screen-reader users get different keys.
- **Repair.** When the comparison draws branch points, render the open-circle legend label as "study arm, or a candidate not adopted". This is `STYLE_LABELS["study"]` in that context, and it matches the description's "study points".
- **Acceptance.**
  - The visible legend and the accessible description name both kinds.
  - No visible text calls a branch candidate a study arm.
  - "Normalized LEAR (study)" is unchanged.

### V3 · DDNN-2 alone is quoted as a relative change without its interval, and in an ambiguous direction (Medium)

- **Clause:** PUBLISH_RULES §3.2: "Change in each primary score as a share of the named comparator's score, with its 95% interval." The brief's observable outcome: "**DDNN-2 alone,** descriptive and never eligible, exactly as the claim map reads it". C427 reads −10.7% [−14.0%, −7.3%] and −15.5% [−18.8%, −11.9%], status S-d.
- **Observed.** On the page's reading path and in the README: "DDNN-2 alone scored lower than v4 on both scores, −11% and −16% as shares of v4's score, but it was a study arm, never eligible for adoption; no rule tested it."
  - There is no interval.
  - The word "descriptive" appears only in the closed Method disclosure.
  - "scored lower" reads as "did worse" in ordinary English, although here lower is better.
- **Impact.** The largest numbers in the chapter, much larger than v5's −2%, appear bare. Their direction can be misread.
- **Repair.** In `v5.caveat.alone`, on the page and in the README: "**That DDNN-2 should replace v4 on its own.** DDNN-2 alone had lower, that is better, error scores than v4: −11% [−14%, −7%] on the point-error score and −16% [−19%, −12%] on the interval score, as shares of v4's score, with 95% confidence intervals. Descriptive only: it was a study arm, never eligible for adoption, and no rule tested it."
- **Acceptance.** The bullet shows both intervals, bound to `derived.change.ddnn2-alone.*` and C427, and the word "descriptive". The phrase "scored lower" no longer appears.

### V4 · The coverage limit "they hold 1 winter" is ambiguous and overstates winter coverage (Medium)

- **Clause:** the brief's observable outcome: "**the coverage limits, stated plainly:** … that no scored day falls in October to December; that the scored days hold one winter". PUBLISH_RULES §2: "Write plainly."
- **Observed.**
  - The chapter reads: "The comparison scores 448 of the 2,654 days in the data, from 2019-01-01 to 2026-04-07; 0 of them fall in October to December, and they hold 1 winter." The A3 card and README say the same.
  - The record behind "1" is defined as "distinct winters, December to February, holding at least one scored day" (`derived.py` L541).
  - The only winter days scored are 2026-01-08 to 2026-02-28, in fold 5. December is not scored at all, as the same sentence says.
  - "They hold 1 winter" reads as "a whole winter is covered", which is the opposite of the limitation it is meant to state.
  - The end date 2026-04-07 is the development boundary, but that is unnamed. "The days in the data" invites the reading that the data ends there.
- **Impact.** The caveat is meant to limit the claim, but it can be read as asserting winter coverage.
- **Repair.** In `v5.caveat.coverage` and `transition.v4-v5.limits`: "The comparison scores 448 of the 2,654 days of data up to the end of the development period, 2019-01-01 to 2026-04-07; 0 of them fall in October to December, and only 1 winter (December to February) contains any of them." Align P54's wording with this.
- **Acceptance.** The sentence matches the record's definition, and is identical in the chapter, the A3 card and the README.

### V5 · The new branch cards quote CP-22 and CP-23 numbers without their evidence class (Medium)

- **Clause:**
  - CP-22 claim map, W33: "Quoting any CP-22 number without its evidence class, or as a confirmatory or significance result".
  - CP-23 claim map, W41, the same for CP-23.
  - Both are kept in force through PUBLISH_RULES §3.1: "Preserve withheld claims … through their controlling claim maps".
  - Standard v1 §2: "Every result belongs to exactly one class. The class decides its badge and its wording."
- **Observed.**
  - The new cards quote "+0.0011 [−0.0031, +0.0054] … In fold 4, both were decisively worse: point error +0.3 [+0.1, +0.4] …" and "+0.0064 [−0.0016, +0.0149] … +1.9 [+0.3, +4.4] EUR/MWh". Neither card, nor the "Experiments not adopted between v4 and v5" heading, carries a badge or any class wording.
  - The A3 cards in the same section each carry "Development · post-selection".
  - In the README, the generations block's preamble ("The research results are development evidence after selection") covers this. The page has no equivalent statement in the journey section.
- **Repair.** End each `branch.*.result` block with "Development evidence after selection, not a test on new data." Alternatively, render the "Development · post-selection" badge in each new card's head, as the A3 cards do.
- **Acceptance.** Each new branch card states its evidence class beside its numbers, on the page and in the README.

### V6 · The README corrupts a canonical name: "the dDNN member on v4" (Medium)

- **Clause:** PUBLISH_RULES §4: "Names, ordering and state-dependent words derive from it on every public surface." PUBLISH_RULES §8: "The report, README, Space card, direct demo and MLflow must agree on identity, status, applicable limitations and claims."
- **Observed.**
  - The README reads: "*v4 plus a DDNN member, under rule cp23-adoption.* In October 2026, the dDNN member on v4 was not adopted."
  - The cause is that `registry.status_sentence` lowercases the first letter unconditionally: `f"the {entry.name[0].lower()}{entry.name[1:]}"`. It does not use `inline_name`, which keeps acronyms.
  - The same string is in `reports/presentation/mlflow-export/cp23.json` (6 occurrences) and `cp24.json` (2).
- **Repair.** In `status_sentence`, use `subject = entry.version or f"the {inline_name(entry)}"`, then regenerate the README and the export.
- **Acceptance.**
  - The README reads "the DDNN member on v4 was not adopted".
  - `grep -c dDNN` returns 0 for `README.md`, `docs/index.html` and `reports/presentation/mlflow-export/*.json`.
  - The cross-surface parity test passes.

### V7 · v5 chapter text is bound to the wrong claim, or to no claim (Medium)

- **Clause:** PUBLISH_RULES §3.4: "Research numbers originate in committed source rows pinned by hashes. The evidence layer derives them; claim maps bind the interpretation; generators render them."
- **Observed.**
  - **(a) The study-arms paragraph is bound to the wrong claim.** `v5.method.arms` is bound to C429, which is "(v3 + DDNN-2) − v4". It renders DDNN-2 alone against v4 (C427), and v5 − (v3 + DDNN-2) (C432). It also interprets C432's "**observed joint worsening**" as "with DDNN-2 present, adding the LightGBM member did not help", which understates the bound interpretation: both intervals lie wholly above zero.
  - **(b) Three statements have no claim.** No CP-24 claim contains:
    - the August 2022 peak values, "v5's point error is 46.9 EUR/MWh against v4's 50.1" (bound to C435, per-fold MAE);
    - the interval widths "25.3, 54.7 and 100.2 … against 26.3, 56.1 and 101.9";
    - the pooled coverages "0.4916, 0.7923 and 0.9395 … 0.4961, 0.7905 and 0.9392".

    The widths and coverages are bound to C433, which holds the equal-fold scores. Compare CP-22's C226 and CP-23's C320, which map their peak values explicitly.
  - **(c) The training window is misstated.** `v5.method.network` says "Each member trains on the two years before the forecast day". C403 says "[max(2019-01-01, D−728), D)". For fold 1, which starts 2020-07-01, the window is about 18 months.
- **Repair.**
  - (a) Split the block. Bind the DDNN-2-alone clause to C427 and the v5 − (v3 + DDNN-2) clause to C432, and replace "did not help" with "made both scores worse".
  - (b) Add CP-24 claims (for example C442–C444) for the peak MAE of v5 and v4 (D24 peak rows) and for the pooled widths and coverages at 50/80/95% (M24 pooled rows). Bind `v5.peak` and `v5.coverage` to them.
  - (c) Change the sentence to "Each member trains on up to two years before the forecast day, from 2019-01-01 at the earliest, minus …".
- **Acceptance.**
  - Every `data-claim` in the v5 chapter names a CP-24 claim whose text contains that value and its interpretation.
  - The claim-binding test gains a negative control for a value bound to a claim that does not contain it.

### V8 · Caveats use wording that expires, and "carries the protection" is unexplained (Low)

- **Clause:** Publication Standard v1 §1 (Tone): "Caveats never use wording that expires, such as "still to be evaluated"." It also requires that each caveat be "phrased as a property of its evidence class".
- **Observed.**
  - The chapter caveats, on the page and in the README:
    - "A re-evaluation on every eligible day is planned."
    - "The one-shot test on days never used, which is planned, carries the protection."
  - The A3 card drops "which is planned": "the one-shot test on days never used carries the protection". That can be read as saying such a test exists for v5. v1's product section does report a one-shot test.
  - "The protection" has no referent on the page. In the rule it means protection against reusing the same folds and adapting to them.
- **Repair.**
  - In `v5.caveat.coverage`, delete the last sentence. The planned-work list already carries the re-evaluation. Align P54.
  - Replace `v5.caveat.class` with: "**Performance on new data.** This is development evidence after selection, and the second decision on a distributional neural network over the same five test periods; only a one-shot test on days never used for development or selection protects against that reuse."
  - Replace the second sentence of `transition.v4-v5.limits` with: "It is the second decision on a distributional neural network over the same five test periods; only a one-shot test on days never used for development or selection protects against that reuse."
- **Acceptance.** No caveat in the v5 chapter, the A3 card or the README contains "planned", "yet" or "still". The A3 card and the chapter say the same thing.

### V9 · The leakage controls are not visible in the chapter or the A3 card (Low)

- **Clause:** the brief's observable outcome: "Visible in them, every value derived from committed rows and none typed: … **the full-coverage leakage controls,** as the claim map reads them".
- **Observed.**
  - Four of the five required items are on the reading path: the verdict, the coverage limits, DDNN-2 alone and the evidence class.
  - The leakage control (C441: "refitted at all 636 warm-up and evaluation origins reproduced the committed forecasts bit for bit") is only inside the closed "Protocol and review" disclosure. No visible label names it.
  - This finding assumes "visible" means visible with disclosures closed, the reading of PUBLISH_RULES §2. If the Lead and Owner read "visible" as "present", this item falls away.
- **Repair.** Add an item to the v5 "Explore these results" list, with a heading anchor `v5-leakage` on the leakage paragraph: "No delivery-day outcome is used: the leakage test at all 636 origins". This fits the chapter grammar better than a new prose slot.
- **Acceptance.** With disclosures closed, the v5 chapter shows the leakage fact and a working route to C441's paragraph.

### V10 · The exact ratio values are not in any value table (Low)

- **Clause:** Publication Standard v1 §4: "Exact values live in the value tables." PUBLISH_RULES §3.4: "Full precision in tables."
- **Observed.**
  - The A3 card, the chapter headline and the comparison finding show only whole percents, for example "−2% [−3%, −2%]".
  - No value table holds the exact ratios. The v5-c2a table holds score differences only.
  - P55 nevertheless asserts "exact values in the value tables: −2.49% [−2.96%, −1.79%] and [−3.04%, −1.68%]; −2.36% …".
  - The rounded display puts the point estimate on the interval's end, which the exact values would explain.
  - The v4 base has the same gap, so this is a precedent, not a PRES-4 regression. The P55 assertion is new.
- **Repair.** Add two rows to the v5-c2a value table, from `derived.change.v5.*` and `derived.change_decision.v5.*` at full precision: "Point-error score, as a share of v4's score: point, 95% interval, 97.5% interval" and the same for the interval score. Otherwise, correct P55's assertion.
- **Acceptance.** The exact ratio values, bound to the derived records, appear in a value table, or P55 no longer claims they do.

## 2. Product recommendations

1. **Surface the dominance on the reading path.** Both study arms scored better than the adopted v5: DDNN-2 alone, and v3 plus DDNN-2 (C432). Today only the first is visible. A Lead DS will ask why the dominated blend was adopted. The page's answer is that the rule fixed v5 as the only candidate, and that model combinations (4.8) are planned. Consider merging the third caveat into: "That v5's weights make the best use of DDNN-2: both study arms scored better than v5; neither was eligible."
2. **Name the first DDNN decision.** In the A3 card's "second decision on a distributional neural network", name it and link it: "after DDNN member on v4".
3. **README subtitles.** "v4 plus a DDNN member, under rule cp23-adoption" carries an internal rule identifier. "The block split removed, under non-inferiority" reads as an outcome, but the split was kept, and it uses undefined jargon. Suggested registry subtitles (≤ 8 words): "v4 plus a distributional neural network, one third" and "One pooled LightGBM in place of v4's blocks". The same strings feed the MLflow descriptions.
4. **A code collision in the comparison table.** The value table shows "DDNN member on v4 (not adopted) v5, CP-23", which carries the code "v5" next to the adopted v5. The CP-23 evidence links also land on a report that calls this candidate "v5". Add a note: "called v5 in its own experiment".
5. **Branch-group order.** On the page, "Experiments not adopted between v1 and v2" now precedes "between v4 and v5" inside a newest-first journey. In the README, the v4–v5 group sits after v1. Put the newest group first, or put it between v5 and v4.
6. **The CP-22 card's fold-4 result.** C209 and C211 record fold 4 as decisively worse in both MAE and WIS. The card shows only the point error. Add the interval-score values.
7. **Wording.** "built only to read the change", in both v5 decision blocks, would read better as "built only to show where the change came from".
8. **README repetition.** The v5 section ends the rule paragraph with "All five conditions held." and then repeats "All five conditions of the rule set in advance held: …". This is the inherited v4 pattern; one of the two could go.
9. **Planned work.** "would be compared with v5 on the same days" does not fit the re-evaluation item, which scores every generation. Its link "the plan" opens the presentation-and-tracking plan, not the research plan. The link is inherited.
10. **Attribution.** "The v3 research model's weather data is derived from NCEP GFS…" also applies to v4 and v5. This is inherited, from a byte-identical section, but now stale for the research headline.
11. **MLflow routes.** The candidate is a non-final build: `pages_build.json` has `final: false`, and `compare:overview`, `compare:v5` and both branch routes are omitted until verified. The comparison's evidence row has lost the base's "Compare the runs in MLflow". The focused recheck at the final SHA should confirm those labels and routes return.
12. **Page budget.** The page is 1,987,952 bytes against the 2.0 MB budget, and PUBLISH_RULES §5.2 and standard §6 say "at v5 … propose compaction" to the Owner. This is a process item for the Orchestrator and Owner, not a page edit.
13. **Optional plainness.** Give the actual winter span as a derived record: 2026-01-08 to 2026-02-28.

## 3. Proposed rule amendments

None.
