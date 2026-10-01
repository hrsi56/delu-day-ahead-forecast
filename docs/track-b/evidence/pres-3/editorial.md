# PRES-3 editorial review

- **Commit reviewed:** `7dd234bd4e07363ff7906f40824ba7a9b8057ab2` (clean detached checkout `.local/worktrees/pres-3/editorial`; working tree clean)
- **Date:** 2026-10-01
- **Reviewer:** bounded editorial subagent; authored none of the changes; read-only in the checkout.
- **Standard applied:** `docs/PUBLISH_RULES.md` revision 1.2 (§§2–6, §8, §10.1, A1, A3, A5); `docs/track-b/publication-standard-v1.md` §§1, 3, 4, 6, 7, 9, 15 (incorporated); claim maps `cp21-claims.md` (C100–C127, W22–W27) and `publication-claims.md` (P16–P26, P33, P51, P52 and PRES-3 notes).
- **Files read:** `docs/index.html` (text dump of all sections, raw HTML spot checks; diffed against the published base `17f354e`: v3/v2/v1 chapters, product documentation and archive are unchanged), `README.md` (glance and research blocks; diffed against `17f354e`), `docs/PUBLISH_RULES.md`, `docs/track-b/publication-standard-v1.md`, `docs/track-b/research-content/cp21-claims.md`, `docs/track-b/research-content/publication-claims.md`, `src/delu_forecast/research_claims.py` (terms, comparison, `v4.*`, `transition.v3-v4.*`, `headline_template`, `target_sentence`, `comparison_terms`), `scripts/build_pages.py` (`v4_*` charts, `LADDER`, `Scale.ticks`/`tick_text`, `v4_slots`, `block_change`, `PLANNED_WORK`, `planned_work`, `SYSTEM_VIEW`, `evidence_row`/`mlflow_route`), `reports/presentation/mlflow_index.json`, `reports/block-challenger/criteria.csv`, `capstone_v21.md` §8 and §18 (for the screening criteria and item 4.6), `docs/track-b/evidence/pres-3/issued-brief.md` (MLflow sequencing only).

**Owner direction of 2026-10-01 respected:** the comparison chart's short labels (v1–v4) and the met / not-met column's move into the value table ("Both targets") are not treated as defects.

**Checks that passed** (no finding): the headline (A1; standard §3.3 a, §3.4) leads with the met verdict, names each metric beside its value, gives N ("1 policy tested against the rule") and the class badge, and renders identically on the page and in the README; the block-split finding reads as C111 with no mechanism (W22); C120 is shown plainly in the transition card, the not-established list, the stress detail and its route label ("The August 2022 peak: where v4's point error is higher"); nothing says or implies that v4 runs in the demo, is the product or is live (W24); the Method paragraph discloses the daily-to-pooled bundle in full (C106, W23); the cost paragraph states the daily-cycle time is "a diagnostic, not … a qualification for daily operation" (W26); every v4 number sits under the "Development · post-selection" badge or states its class, with no significance or confirmatory wording (W27); the transition card meets A3 (predecessor, change, comparator = predecessor, result with interval, class, limits, dated decision, route) and agrees with the chapter; the target sentence and census sentence match P25/P33 (N = 12, the four names from the verdict records, 8 rows / 4 tested); the value table's "Both targets" column matches the verdict records; the planned list names only DDNN for 4.6, names v4 as the comparator without fixing a design, drops 4.5, keeps the other items, and neither surface contains "TabPFN" or "tabular foundation model"; the system flow and reproduction list add v4 correctly.

---

## 1. Existing-rule violations

### V1 — Comparison terms used on the reading path are defined only inside a closed disclosure, or after first use (page) · priority: medium

- **Clause.** PUBLISH_RULES §2: "Define a term at first use"; "The reading path excludes closed disclosure bodies … A fact buried in a disclosure does not satisfy a rule requiring that fact on the reading path." Publication Standard v1 §4, *Definitions*: "Each term is defined where it is first used" (the section applies on the reading path).
- **Observed** (`docs/index.html`, `section#research-results`):
  - The caveat directly under the finding: "Development evidence, not a test on new data. Meeting the targets is a development diagnostic, not a product qualification." This is the first use of "the targets" on the reading path. They are stated only after the chart: "The dashed lines mark the targets: each error score at least 10% below the strongest benchmark, daily LEAR (set 2026-09-15)."
  - "Daily LEAR (benchmark)" (chart rows) and "the strongest benchmark, daily LEAR" (target sentence): what LEAR is appears only inside the closed disclosure "Definitions, the policies tested, and why v1 scores differently in its own report", as "Daily LEAR: the strongest benchmark, a linear model refitted daily." "Policies: the models and variants tested." sits in the same closed body, while the visible subtitle reads "8 policies · …".
  - Cause: PRES-3 moved `terms.targets`, `terms.benchmark` and `terms.policies` from under the headline, where they were visible on the published page, into that disclosure (`research_claims.comparison_terms()`; P21 PRES-3 note).
- **Impact.** The comparison's main caveat qualifies a term the reader has not yet met. The benchmark that defines the targets is never explained on the reading path. This is a regression from the published page.
- **Repair.** Render `comparison_terms()` visibly, as a short term list like the headline's, directly below the comparison caveat and outside any disclosure. Keep the S_MAE/S_WIS definition, the census and the v1 note in the disclosure. Make the caveat qualify the headline's own verdict too (update P24):
  > Development evidence, not a test on new data. Meeting the adoption rule or the accuracy targets is a development diagnostic, not a product qualification.
  > - **Accuracy targets:** each error score at least 10% below the strongest benchmark's, set on 2026-09-15; the distances are point comparisons.
  > - **Daily LEAR:** the strongest benchmark, a linear model refitted daily.
  > - **Policies:** the models and variants tested.
- **Acceptance check.** Check `#research-results` with every disclosure closed, in Chrome and WebKit. Each occurrence of "targets", "LEAR" and "policies" comes at or after a visible definition. The A2 bound on the finding sentence still passes, because the list sits below it.

### V2 — README: the accuracy targets are named but never stated, and "the distances" point to nothing · priority: medium

- **Clause.** Publication Standard v1 §4, *Thresholds*: "A threshold is stated in words, with its date … A bare 'limit 0.59203' does not meet this rule." PUBLISH_RULES §2: define a term at first use.
- **Observed** (`README.md`, research block):
  - "Reading the comparison" gives: "**Accuracy targets:** set on 2026-09-15; the distances are point comparisons."
  - Since PRES-3, the README states no threshold anywhere and shows no distances. The published glance headline carried both ("at least 10% below the strongest benchmark, daily LEAR (v3: 14% below … 17% below …)").
  - The term is used before this definition, in the v3 section ("It met the joint improvement rule against v2 and both accuracy targets."), and again in the caveat "Meeting the targets is a development diagnostic, not a product qualification."
  - The README gives no N for the targets, and does not say who met them.
- **Impact.** A README reader cannot learn what the targets are, who met them or how many policies were tested against them. The definition refers to distances that do not exist on this surface.
- **Repair.** Add a README form of `target_sentence()` to "Reading the comparison", after the term list. The page form speaks of dashed lines, so the README needs its own wording:
  > The accuracy targets: each error score at least 10% below the strongest benchmark, daily LEAR (set 2026-09-15). 12 policies were tested against them; v3 was the first to meet both; v4, pooled LightGBM with weather, three-block LightGBM and normalized three-block LightGBM met them too.

  Give the term its threshold as well. `terms.targets` is shared with the page:
  > **Accuracy targets:** each error score at least 10% below the strongest benchmark's, set on 2026-09-15; the distances are point comparisons.
- **Acceptance check.** The README's generated blocks state the 10% threshold with its date, N = 12 and who met the targets, all bound to the derived records. "the distances" appears only on a surface that shows distances. The cross-surface parity test still passes.

### V3 — The adoption rule's conditions are undefined where the reading path relies on them, and the README's pointer leads to nothing · priority: medium

- **Clause.** PUBLISH_RULES §2: define a term at first use; closed disclosure bodies are off the reading path. Publication Standard v1 §4, *Definitions* and *Thresholds*.
- **Observed.**
  - **The v4 chapter's one-sentence reading.** It is visible below the main chart and repeated in the README's v4 section: "Both paired differences lie below zero, no test period is decisively worse, and the six screening diagnostics hold, so the rule set in advance adopted the change in research."
    - "the six screening diagnostics" and "decisively worse" are explained only inside the closed "Protocol and review" body ("it met the six original screening diagnostics", "decisively worse, that is, none had a paired interval wholly above zero").
    - The six are never named anywhere. The next paragraph calls them "six original screening criteria" and cites "criterion 4" and "criteria 4 and 5".
    - "the rule … adopted the change" is also inexact: the rule gives the verdict (C109), and adoption is the dated decision (C127).
  - **The README glance:** "**Adoption rule:** set on 2026-09-29; its four conditions are in the v4 chapter." The README's v4 section does not contain the four conditions, because the `v4.rule` block is page-only. The README does not link the report's chapter either. On the page, "the v4 chapter" is plain text, not a route to the Protocol and review detail.
- **Impact.** The chapter's verdict sentence rests on a set of tests that is never named. A README reader is sent to a section that does not state the rule.
- **Repair.**
  - Rewrite `v4.reading` (C109), for the page and the README:
    > Both paired differences' 95% confidence intervals lie below zero, no test period's interval lies wholly above zero, and v4 passed the six screening criteria set before the experiments (the two accuracy targets, coverage in each period, the August 2022 peak, each period against the daily benchmarks, and complete forecasts), so it met all four conditions of the rule set in advance and was adopted in research.
  - Add `v4.rule` to the README's v4 section (flag it README), or change the README's term to point to a working link to the report's chapter.
  - On the page, turn "the v4 chapter" in the adoption-rule term into a descriptive A5-style route that opens "Protocol and review" and lands on its first paragraph.
  - In `v4.criteria`, name criteria 4 and 5 in words ("the August 2022 peak check" and "the per-period check against the daily benchmarks").
- **Acceptance check.** With every disclosure closed, on both the page and the README, "screening criteria" and "decisively worse" (or their replacements) are defined in words where first used. The README carries the four conditions, or a working link to them. A grep for "rule set in advance adopted" returns nothing.

### V4 — "No study arm is better than v3" states an absence for contrasts whose intervals span zero · priority: high

- **Clause.** `cp21-claims.md` W25 withholds calling a mixed or non-significant contrast "equivalent", "no effect", "no benefit" or "no harm". It binds through PUBLISH_RULES §3.4 ("claim maps bind the interpretation"). PUBLISH_RULES §3.2: "A null result does not demonstrate equivalence."
- **Observed.** In the v4 chapter's Method disclosure, under "Each study arm against v3" (block `v4.method.arms`, mapped only to C115): "No study arm is better than v3 on its own: each arm's intervals against v3 span zero, except the three-block LightGBM's interval score, whose interval lies wholly above zero, worse: +0.0218 [+0.0004, +0.0450]."
- **Impact.** For pooled LightGBM (C114) and normalized three-block LightGBM (C116), both intervals span zero, and the claim map permits only "no demonstrated joint preference". "Is not better" asserts a finding of no benefit, which is the withheld wording in substance.
- **Repair.**
  > No study arm on its own shows a demonstrated joint preference over v3: each arm's intervals against v3 span zero, except the three-block LightGBM's interval score, whose interval lies wholly above zero, worse: +0.0218 [+0.0004, +0.0450].

  Map the block to C114–C116.
- **Acceptance check.** The rendered sentence contains "no demonstrated joint preference" and no "is better" or "is not better". The block's claim list covers C114, C115 and C116.

### V5 — Confidence intervals and forecast intervals share the label "95% interval(s)" in the v4 chapter · priority: medium

- **Clause.** PUBLISH_RULES §3.2: "Intervals of estimated differences and forecast intervals must have distinct labels."
- **Observed.**
  - Confidence intervals labelled only "95% interval(s)":
    - The v4 chapter headline, a visible h3 (block `v4.chart_headline`): "Against v3, the point-error score changed by −5% [−6%, −4%] and the interval score by −5% [−6%, −4%], each as a share of the comparator's score, with 95% intervals."
    - The arms chart's `<title>`: "Each study arm, and v4, against v3: equal-fold error-score differences with 95 percent intervals".
  - The same chapter uses that label for forecast intervals: "382 against 383 of its 408 hours fell inside the 95% interval", and the coverage rows are labelled "95% interval".
- **Impact.** In the chapter's own headline, the reader cannot tell whether [−6%, −4%] is a confidence interval of the change or a prediction interval.
- **Repair.**
  - The headline: "…each as a share of the comparator's score, with 95% confidence intervals."
  - The arms chart title: "…equal-fold error-score differences with 95 percent confidence intervals".
- **Acceptance check.** In the v4 chapter and the README's v4 section, every interval of an estimated difference or ratio is labelled "confidence interval". "95% interval" appears only for forecast intervals.

---

## 2. Recommendations (not violations)

1. **The ladder chart prints a signed zero.** The x-axis tick reads "-0.00", with an ASCII hyphen, four times: the desktop and mobile variants, both panels. The cause is that `Scale.ticks` accumulates floating-point steps from −0.25 by 0.05 and reaches `round(-1e-17, 10) == -0.0`, and `tick_text` leaves the hyphen when `value < 0` is false. Fix: normalise ticks with `abs(tick) < 1e-12` to `0.0` in `Scale.ticks`, or in `tick_text`. Add a lint that no tick text matches `^[-−]0(\.0+)?$`.
2. **Carry the full bundle into the ladder chart.** The row label and value-table row read "Pooled LightGBM − daily LightGBM: weather, bundled with size selection". The chart description, bound to C106, reads "Adding weather together with size selection lowered both scores". Both omit the missing-input rule that C106 includes. The Method paragraph above the chart does disclose it. However, the A5 route "The ladder: what each step added" lands on the heading below that paragraph. Proposed label: "Pooled − daily LightGBM: weather, bundled with size selection and the missing-input rule". Proposed description: "Adding weather, bundled with size selection and the missing-input rule, lowered both scores; …". Align C112's wording with C106, and say in one clause what "the missing-input rule" is.
3. **Say "attribution" less.** "Three study arms attribute the change one step at a time" (`v4.method.ladder`) implies the ladder explains v4's gain over v3. It does not: each arm alone is worse than v3, and the blend step has no ladder interval. Proposed: "Three study arms separate the change into steps, one at a time."
4. **Make the change of interval method visible** (PUBLISH_RULES §3.2, "Do not silently substitute methods"). v4's percentage intervals are percentile intervals of the ratio (P18). v2's and v3's are the difference's interval divided by a fixed denominator. The page shows both side by side as "95% confidence intervals"; v4's card adds only "from the experiment's own bootstrap draws". Proposed card text: "…as a share of v3's score, with 95% confidence intervals of that ratio from the experiment's own bootstrap draws". Proposed sentence in "Bootstrap settings…": "From v4 on, a percentage change's interval is the percentile interval of the ratio of the two scores over the same draws; for v2 and v3 it is the difference's interval divided by the comparator's score."
5. **Define "three-block" where it first appears.** It is used in the opening's name, the lineage and the transition card, and explained only in the v4 chapter's change diagram. Proposed transition-card text: "…added a three-block LightGBM forecaster (separate models for the night, the solar hours, and the shoulder and peak hours) with one third of the blend's weight…". Optionally add a headline term: "**Three-block LightGBM:** gradient-boosted trees with a separate model for each of three blocks of hours: night, solar hours, and shoulder and peak."
6. **State the rule's test in the headline's words.** "both error scores improved on v3's" is P51's sanctioned rule in words. It reads as a result rather than a test. Proposed: "Met the adoption rule set before the experiment: against v3, both error scores' 95% confidence intervals lie below zero (v4 − v3: …; 1 policy tested against the rule)." This needs a P51 edit.
7. **Tidy the transition card's "Not established".** "showed no demonstrated joint preference" is awkward, and the peak item is an adverse observation listed as if it were untested. Proposed: "Separate hour-block models are not shown to help: the three-block against the pooled LightGBM shows no demonstrated joint preference. No gain over the August 2022 peak: there, v4's point error is higher than v3's (descriptive, 17 days)."
8. **Use "information", not "inputs".** `v4.change` ("with the same inputs as v3") and the change diagram's note ("same inputs") say more than C105, which gives v3's *information*: CP-15's LightGBM features plus the GFS columns, not v3's LEAR inputs. Proposed: "with the same information as v3" and "same information". The transition card's "kept v3's inputs" is accurate for the LEAR pair.
9. **Report coverage at every level.** `v4.coverage` quotes only the 95% level, where v4 is higher. At 80%, v4 is lower (0.7905 against 0.7914). Proposed: "v4's pooled intervals are narrower than v3's at every level, with coverage within 0.003 of v3's at each (95%: 0.9392 against 0.9377)."
10. **Make the 4.6 evidence line match the anchor.** Research anchor §18.4 gives 4.6L as a provenance and *licence* record and 4.6R as resource measurements, gated by the correctness checks, before 4.6C. Proposed: "A provenance and licence record and resource measurements, then one predefined comparison on identical hours". The question ("Does a distributional neural network improve on v4, with the same information and on identical hours?") meets the brief as written.
11. **Extend the GFS attribution to v4.** The Terms line (`claims.GFS_ATTRIBUTION`, on the page and in the README) says "The v3 research model's weather data is derived from NCEP GFS…". v4 uses the same frozen GFS columns, and v3's protocol detail carries the attribution line while v4's does not. Proposed: "The research models' weather data, from v3 on, is derived from…". Add `GFS_ATTRIBUTION` to v4's protocol detail as v3's has it.
12. **Refresh the MLflow route before the final build.** At this candidate, the comparison's "Compare the runs in MLflow" uses the index entry verified on 2026-09-29. Its `run_keys` are the seven v3-era rows, without `cp21/HGL`, although the chart now draws eight. The "Tracking" sentence ("Every policy evaluated since v1 is in the MLflow experiment delu-generations") is also not yet true for the CP-21 policies. The brief sequences the upload, the verifier and the index before the `--final` build, and the verifier rebuilds every route from `expected_routes()`, so both should close then.
    - Acceptance at the final SHA: `compare:overview.run_keys` equals the registry's eight rows, including v4's run, and `compare:v4` is advertised.
    - Guard: `mlflow_route()` omits a route whose indexed `run_keys` differ from `expected_routes()`, instead of serving a stale verified URL.
13. **The met / not-met column on the reading path.** The page as a whole meets standard §15 literally: N (12) and the target in words are on the reading path, and the met / not-met column is in the value table, per the Owner direction. Optionally name the tested rows that did not meet the targets in the target sentence ("…met them too; v2 and normalized LEAR did not"). Update P25, whose text still says "The comparison's … chart's rows carry each policy's verdict".
14. **Reconcile the policy count.** The subtitle "8 policies" and the chart title "eight policies" count references the census calls "references that never were" tested, against the term "Policies: the models and variants tested". This predates PRES-3. Consider "8 rows" in the subtitle, or "Policies: the forecasting models and references compared" with "tested against the targets" kept for N.

---

## 3. Proposed rule amendments

**PA1 — Record where the target verdict column may live.**
- *Observed problem.* Standard §15, amending plan §8.2, requires the target line "with a met / not-met column and N". The rule does not say whether the column must be on the reading path, on the chart or in the value table. The Owner's direction of 2026-10-01 moved it into the comparison's value table ("Both targets"), and P25 still describes the chart's rows as carrying the verdict. A future checker could regrade this either way.
- *Exact change* (PUBLISH_RULES §15, as a note on the incorporated standard §15): "The met / not-met column may sit in the comparison's value table beside the canonical names, provided the chart's description points to it. The target in words, its date and N stay on the reading path (Owner direction, 2026-10-01)."
- *Applicability:* PRES-3 and later publications. *Test:* the value table has the column bound to the verdict records; the chart description names its location; the target sentence carries N. *Maintenance:* none beyond the existing P25 binding. Update P25's text.

Editorial verdict: 5 violations
