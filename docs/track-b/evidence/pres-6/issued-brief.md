# Track B Checkpoint Brief — PRES-6 (the final product first: v6's product results and business insights, under A8)

*Issued by the Orchestrator on 2026-11-14, Asia/Jerusalem, under the Owner's decisions 27 and 28 and his question
of 2026-11-14 (ruling O46).*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`, public; Pages serves `main:/docs`).
- Authorized checkpoint: PRES-6, exactly one.
- **What it does.** It gives the report A8's product-first order now.
  - **The Owner's question,** on 2026-11-14: "למה אין בראש העמוד גרפים שנוגעים לביצועים של v6 כמו שהגדרנו בחוזה
    הפרסום למוצר סופי?" ("Why are there no charts of v6's performance at the top of the page, as we defined in the
    publication contract for a final product?").
  - **O46** reverses O38. A8 applies now: decision 28 and O29 made v6 the product, and A8 §5.1a asks for
    development results labelled by evidence class, not live scores.
  - **The new order:** compact navigation → the product and daily-forecast opening → **How the product works** →
    **Product results** → **Business insights** → **How the models compare** → the rest, in its existing relative
    order.
  - **Beside it, three follow-ups from PRES-5** (its landing record, O45):
    - the link checker fails any redirect that ends on another host;
    - the receipt normalizes the Space's served page by CP-18c's rule;
    - Integration review 4's wording recommendations R1–R7, where they still apply.
- **Its research numbers use development data only,** delivery days through 2026-09-06 (r20 §24.14, P1). The report
  shows no live forecast, score or price. 4.7T stays the one test of v6.
- Ratified plan anchor: the publication anchor `docs/PUBLISH_RULES.md`, revision 1.5, SHA-256
  `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`.
  - Apply its precedence and amendments A1–A12. Record any that is not applicable, with the reason.
- **Research constraint anchor, read-only:** `capstone_v21.md` v21-r20, SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`, §24.14.
- **Execution inputs.** Verify each hash before relying on it:

  | Input | Path | SHA-256 |
  |---|---|---|
  | PRES-5's publication packet (the page's current state, its §9 matrix) | `docs/track-b/evidence/pres-5/publication-packet.md` | `2b67c80c60a9882e6e75abb90ba93b9ae0648aae9108deb7663dfdf2eaaa56a7` |
  | PRES-5's landing record (O43–O45, the follow-ups) | `docs/track-b/pres-5-landing-2026-11-14.md` | `6a9a5499074c6866bc18e6012c6007f83a081d8182c9a95d084203c0768c5f36` |
  | PRES-5's A12 post-deployment review (its recommendations) | `docs/track-b/pres-5-a12-postdeploy-review-2026-11-14.md` | `7632db7c249ff6501be1690701898f90188fd382255d1d13cdb72d65f558aba0` |
  | PRES-5's Integration review 4 (recommendations R1–R7) | `docs/track-b/evidence/pres-5/integration-review-4.md` | `fce6c28c246b0420b593b6666002d2c23605662260f2617bb7ad7d4364a6a197` |
  | CP-28's report | `reports/cp28/report.md` | `316d55056d0904ee63cd57fc3b2212cb3562b3b5357a280a5c431dd06ea68daa` |
  | CP-28's publication packet | `reports/cp28/publication-packet.md` | `a0a7f04c78c8955c8932f829e0ad1e0d772b53d04cab41d9ed54e90213b5b906` |
  | CP-28's stored forecasts' manifest | `reports/cp28/forecast/manifest.json` | `f092140ed028d18a973bfad11ad9aa0397ad3e492223c4da683bc8e775cf3ce8` |
  | CP-28's stored hourly forecasts (v6 = arm A1) | `reports/cp28/forecast/hourly.parquet` | `f5cb02a19236edd20c182c2874a5d59628652e6838fe5745aa6ffacf3f53f638` |
  | CP-28's stored features | `reports/cp28/forecast/features.parquet` | `02a84820870ae4ee3465e73a483c710dbd40f4d61779614d4a77161b93bae6e1` |
  | CP-28's stored networks | `reports/cp28/forecast/networks.npz` | `bfb1d1c37b8c2232a9171f5e2d8ec45059f2796f2e5f1ea38916fc2732cd94a2` |
  | CP-26's report (every development day) | `reports/rebaseline/cold-rerun-2026-10-15/CURRENT-REPORT.md` | `411c0f841ae373cf9894b19a4c0c869b447be9c69d7fd8c2ffa758269841de8e` |
  | CP-17c's landing record (the policy identity 720fc581…) | `docs/track-b/cp-17c-landing-2026-10-30.md` | `89b65c841950cbb389a7e0f849f149f487669819491a71bb434e9d91f96b4759` |
  | CP-18c's landing record (the live product) | `docs/track-b/cp-18c-landing-2026-11-13.md` | `bda09c0a66ec27d6bcc14d730e5dc44b6c85e31a09a369b3b67ca15e24ed71cb` |
  | 4.7T's registered protocol | `docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md` | `337a102d6bbbf6d9335fe6ed701a4c80ea1b9172344ffc0f63909b155b567c58` |
  | The publication runbook | `docs/track-b/publication-runbook.md` | `0f92b92b69572b142a2f5091a7d8737ed6c1f90a7f8beed35a292d297f0af3e9` |
  | The packet template | `docs/track-b/publication-packet-template.md` | `4049c3e1f695034ec45fa185d465fce05ab1183cbded72188306579d7287d01a` |
  | The publication advisory log | `docs/track-b/publication-advisory-log.md` | `6901fdaca2dba21d36e2e94cadefbffe24d48ebd0d4ef2680fb2569eeea4bfbf` |

- **The Owner's decisions:** 1–19 bound by the frozen copies; 20–28 (`progress.md`;
  `docs/track-b/owner-decisions-2026-11-05.md`, `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`).
- **The Orchestrator's rulings that bind the wording:** O13, O14 (F1 at 0.082 EUR/MWh), O16, O26–O30, O44, O45
  and O46.
- **Decision 27** has the Orchestrator decide every open presentation matter that costs the Owner nothing, and log
  it.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records this brief's issue, a descendant of
  `fed4915d` (PRES-5's closure) through the runner's data-only commits. The issue commit changes only `progress.md`.
  - **`main` moves during this round.** The live product's daily runner pushes data-only commits to `main`, by the
    author `delu-daily`, touching only `live/`. Never write under `live/`. The packet's LAND commands assume a moved
    `main`.
  - **Tags:** every landed checkpoint's `land/` and `evidence/` tags are pushed, except `evidence/cp-26` = `ca20331`,
    which is **local-only and never pushed**. The rulesets refuse moving or deleting a `land/`, `evidence/` or
    `archive/` tag, and refuse pushing a `gauntlet/*` branch.
  - **Branches and worktrees:** `main` only. No other checkpoint runs beside this one.
- **Working tree:** the primary checkout is on `main` and clean apart from ignored material.
  - **The Orchestrator uses it.** Never switch its branch, and never write a tracked file in it. Your only writes
    there are under `.local/artifacts/pres-6/`, `.local/tmp/pres-6/` and the worktrees under `.local/worktrees/pres-6/`.
  - **The canonical brief** is `.local/artifacts/pres-6/issued-brief.md`. Package that file byte for byte.
  - **A Finder `.DS_Store`** may sit in ignored folders such as `space-product/`. It is local-only and fails
    `tests/cp18c/test_space_live.py::test_the_page_sources_type_neither_the_old_name_nor_a_bare_issued_at` in the
    primary checkout only. A clean worktree does not have it.
- **The published surfaces:**
  - the report `docs/index.html`, SHA-256 `983a75c44b0f93dabd183ee810158aefbfa62adfb5545b4a433afe4b5bbb9475`,
    1,848,955 bytes. Its order is A4's: the opening, then How the product works, then How the models compare. The
    opening has one v6 chart (a stored development day, 2026-04-07);
  - the README, SHA-256 `bc98e9ccb74546a2d3fbdbbfabd8034bc63addfc165c0264598f1a1d3747c472`;
  - MLflow on DagsHub, the experiment `delu-generations`, with 105 runs. This round writes nothing there;
  - the Space `Yarden-Viktor/delu-day-ahead-forecast`, CP-18c's live product, updated daily by the runner. This
    round changes nothing there.
- **What already exists for this round:** the inputs table above; the report's build `scripts/build_pages.py` and its
  claim layer (`src/delu_forecast/claims.py`, `surfaces.py`, `research_claims.py`, `registry.py`); PRES-5's
  `src/delu_forecast/final_candidate.py` (v6 on v5's population); the publication tools (`scripts/check_links.py`,
  `scripts/publication_receipt.py`, `scripts/publication_guard.py`, `scripts/check_reader_paths.py`).
- **Credentials:** none are needed. This round makes no external write.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
When this checkpoint closes, after the Orchestrator's post-return steps, the report leads with the final product. It
shows v6's development results and their business meaning before any model comparison.

1. **The order (A8, §5).**
   - Compact navigation, then the product and daily-forecast opening, which keeps v6 "final candidate · pending
     4.7T" with the live Space link and v1 as the historical demo.
   - Then **How the product works**, then **Product results**, then **Business insights**, then **How the models
     compare**.
   - Everything after the comparison keeps its existing relative order. The comparison's content and the later
     sections do not change, except for item 7's wording.
   - Descriptive routes stay visible by default.
2. **Product results (§5.1a),** for v6 (A1 in the frozen records; policy `720fc581…`), on development delivery days
   only, from CP-28's stored forecasts (`reports/cp28/forecast/`, arm A1) under A1's frozen rules. No fit, and no
   recomputation of another policy.
   - **Forecast against observed:** the median and the intervals against the cleared price, on days chosen by a rule
     written in the packet before any is drawn (for example one per material regime), plus a whole-population view.
   - **Error over time:** the daily point error and interval score across the development days, with the
     similar-day naive as the reference.
   - **Error by material regime** (§5.1 subject 2's regimes), with counts and uncertainty. Thin subsets are stated
     as such.
   - **Explanation or sensitivity.** Use an existing committed result for v6 if there is one.
     - If there is none, compute one by inference only from the stored networks and features on development days:
       no fit, by a method and feature grouping written in the packet before the computation.
     - If neither fits within the ceilings, the section states the gap.
   - **Interval coverage together with width,** at each nominal level.

   Each graphic names:
   - the policy and artifact;
   - the population, its dates and its units;
   - its evidence class: development, and post-selection where it applies.

   Development and prospective evidence stay visibly separate. The report holds no prospective number, and it says
   that the Space shows the live record, "prospective evaluation in progress". Every value is derived from committed
   rows, and none is typed.
   - **The populations must agree** with CP-26's and CP-28's records (2,068 development days, or the stated
     subset).
   - **A2's early-placement bound** now applies to the product finding (A8), measured in the browser matrix.
3. **Business insights (§5.1a).**
   - **The section stays.** It explains the intended use and the measured forecasting implications, with their
     limits.
   - **It states the gap:** no decision-policy or economic evaluation has been authorized or run. It shows no profit
     curve and implies no gain.
   - **No error or coverage figure is called a profit** or a success rate.
4. **The README.** Its product-first summary agrees with the page. It carries the same claims, through the claim
   layer.
5. **The link checker.**
   - `scripts/check_links.py` (and the receipt's link row) fails a redirect whose final host differs from the
     linked URL's host. It records the redirect chain.
   - A test covers the Space's bare `/history/` → `huggingface.co/history` case with a recorded fixture, not the
     network.
6. **The receipt's Space page.** `scripts/publication_receipt.py` normalizes the served page by the same rule as
   `src/cp18/publish.py`'s `normalized`: the host's one injected script, plus its injected meta tags. Reuse the rule;
   do not copy a different one. A test covers it with a recorded fixture.
7. **R1–R7.**
   - Apply each of Integration review 4's recommendations that still applies to the page or the README.
   - Record each one as applied or not applicable, with the reason.
   - None may change a published number.
8. **The page budget.** The page is 1,848,955 bytes, 151,045 under PUBLISH_RULES' 2.0 MB budget.
   - Keep it within the budget, by the means the rules allow.
   - If it cannot fit, return BLOCKED with the measured need and a proposed remedy. Do not exceed the budget.
9. **Review.**
   - The editorial review and a fresh reader, as the runbook provides.
   - The independent Integration check passes at the candidate, and a focused recheck passes at the final SHA.
10. **The packet.** Its §8 names the exact payloads and the ready-to-run commands for the Orchestrator's steps:
    - the landing on a moved `main` (the runner's data-only commits) and the push, which deploys Pages;
    - the public post-deployment checks, including `scripts/publication_receipt.py`, with every link into the Space
      checked without following redirects;
    - A12's independent post-deployment check where it can add something.

The publication is complete only after those steps and their public evidence. A local PASS is not a deployed
publication.

## Complete authoritative checkpoint bar
- **PUBLISH_RULES 1.5 in full.** Every applicable clause, including the incorporated baseline, A1–A12 and §13's
  acceptance record. A8 is triggered (O46).
- **The runbook** `docs/track-b/publication-runbook.md`: every touchpoint that applies.
- **The packet template, every section.**
- **r20 §24.14,** for what may be published now and on which data.
- **Critic and return:** `docs/track-b/gauntlet-templates.md` §§2–3. This authorizes no fit.

Verbatim, extracted by `scripts/bar.py bar … --at fed4915d --quote` from `main` at PRES-5's closure.
(The excerpt is the citation. Any line number is a courtesy and is non-binding.)

**`docs/PUBLISH_RULES.md` revision 1.5 §5** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 126 lines, 10801 bytes, SHA-256 `209185ae916b98a305aa171b9fd4cc90fc9d047cc3fba54711338fea9c92861d`):

> ## 5. Page architecture and active-product documentation
>
> **A4 replaces v1 §6's section order for future publications with:**
>
> 1. Compact navigation.
> 2. Product opening: what it does, actual available model/status, research headline, actions,
>    release rule and labelled preview or eligible live panel.
> 3. **The product explained, immediately after the product opening:** the maintained documentation
>    of the actual released/frozen product, covering the twelve subjects in §5.1. Show a concise
>    orientation and descriptive routes here; expand details in this product section, not inside an
>    old generation chapter. Shared explanations belong here alongside product-specific evidence.
> 4. Overview comparison and fairness note.
> 5. Lineage and generation chapters, newest first, with transition summaries and rejected branches.
> 6. Planned work, unscored and unnumbered.
> 7. Optional engineering/audit depth not already covered by the product documentation. Do not
>    relocate essential data, method, forecast, limitations or reproduction explanations here.
> 8. Reproduction, contribution, terms and attribution.
>
> **A8 overrides this order at the final-product transition:** compact navigation → one product
> and daily-forecast opening → **How the product works** → **Product results** (scientific
> results and graphics) → **Business insights** → **How the models compare** → the remaining
> lineage, chapters, planned work, depth, reproduction, contribution, terms and attribution in
> their existing relative order. No change is made to the comparison content or later sections.
> The three product sections complement each other: method explanations link to the canonical
> result graphics; business conclusions cite those results and their own evaluated use case,
> without duplicating full charts or manuals. Descriptive routes remain visible by default.
>
> At that transition, the latest Owner-designated final version, selected product, primary demo
> and daily training/forecasting policy must share one version and policy identity. The opening
> must not pair a newer research model with an older primary demo. Later experiments remain
> research history until a separately authorized product replacement. Designation is recorded
> immediately as selected; if rollout is incomplete, show that state and the currently runnable
> identity honestly. Never relabel an old demo as the incoming model or claim the transition done.
>
> The product documentation must fit the headline/orientation placement contract. Its concise
> orientation and descriptive topic routes are visible immediately after the product panel; long
> bodies may use named disclosures within that section. Moving the entire old report into the
> opening is not the intended implementation. Moving the comparison before lineage is an explicit
> amendment that preserves room for product context while keeping the result early.
>
> The public heading identifies the product, for example **“How the product works”**, with the actual
> model/version visible as provenance. It is not permanently named “About v1”. While v1 is the only
> released product, its verified applicable evidence supplies that documentation. When a successor
> is validly released/frozen, the documentation follows the new product. A research leader must never
> be documented as the shipped product merely because its scores are better.
>
> ### 5.1 The twelve product subjects and their lifecycle
>
> **One comprehensive current-product explanation; concise generation histories.** The Owner's
> clarification is that the depth of the original report's subjects 1–12 belongs to the product,
> not to v1 as a historical generation. It is not sufficient to move only model-independent prose:
> features, validation, explanations, reliability and reproducibility must describe the actual
> product too. Research chapters retain their required decision/evidence slots but do not each
> acquire a duplicate full product manual.
>
> The original report combines 6–7 under one explainability heading and includes a 3b spectral
> subsection. The following is a coverage map, not a requirement to preserve its numbering or wording:
>
> | Original subject | Required current-product explanation | Identity / caveat to preserve |
> |---|---|---|
> | 1 · The data | Target, sources, date range, cadence, units, preprocessing, availability and cutoffs | Actual product data contract and source rights; distinguish training, evaluation and operational inputs |
> | 2 · Three regimes | Material price regimes, negative prices and why these affect evaluation or use | Periods and plots from eligible data; do not silently refresh research plots beyond the permitted boundary |
> | 3 · Feature catalog | Inputs/features actually used, why they are eligible and what was excluded | Current frozen policy's feature set; historical selection experiments remain dated evidence |
> | 3b · Spectral view | Explain seasonal-feature reasoning where relevant and supported | Not a mandate to rerun or reproduce a spectral analysis for every model; omit the technique if inapplicable and explain the design directly |
> | 4 · Validation design | Forecast origin, temporal splits, leakage protection, baselines and evaluation windows | Actual governing protocol, with development, one-shot and live evidence separated |
> | 5 · Results | Product's measured point/interval performance, uncertainty and meaningful comparison | Results for this product/artifact; historical research improvement is not substituted for a product test |
> | 6 · Explainability: attribution | What the chosen explanation method says about the product's predictions | Model/output/population to which it applies; SHAP is an example, not a universal mandated method |
> | 7 · Explainability: sensitivity/importance | What an appropriate robustness, importance or sensitivity analysis establishes | Distinguish attribution from incremental value or causality; no transplantation of v1 rankings |
> | 8 · Regime-stratified error | Where the product succeeds or fails, with relevant groups, counts and uncertainty | Evidence-supported strata and thin-subset limitations; no invented evaluation |
> | 9 · Reliability | Observed interval coverage and width, applicable calibration stages and limitations | Actual interval pipeline; v1's three stages are not imposed on a different method |
> | 10 · Next-day forecast | Product output and how to read it; useful chart and actual controls | Explicit replay/inference/live identity; only eligible Live can show current issued forecasts as live |
> | 11 · Honest limitations | Data assumptions, failure modes, generalization and operational limits | Limitations of the active product; retain adverse facts and evidence-class qualifications |
> | 12 · Reproducibility | How to run/reproduce the product, artifact/policy identity and useful evidence routes | Current verified commands and service routes; do not reuse historical container instructions as current |
>
> Every subject is accounted for as supported, not yet evaluated, or inapplicable with a specific
> reason. This presentation obligation does not authorize missing research. A missing result is
> shown honestly and routed to the research plan; any required product-qualification gate still
> has to be met under that plan. Do not display an old model's graph under the new product heading
> or assert “not applicable” solely because the evidence is inconvenient.
>
> For a product replacement, its publication packet identifies the incoming and outgoing product,
> rechecks these subjects against incoming evidence, updates model-specific graphs and instructions,
> retains genuinely shared material after an applicability check, and preserves the outgoing evidence
> as history. Publish the updated product identity and documentation together. A data-only update
> under an authorized frozen policy updates its issuance/freshness/evaluation metadata; it does not
> pretend to be a new model release or trigger a new full historical narrative every day.
>
> The original “DE-LU day-ahead price forecasting” report is currently at the bottom because it is
> the preserved v1 archive. Retain its protected text/behaviour and an explicitly historical route,
> but do not make it the only route to understanding the current product. The active-product section
> is maintained outside that archive. Its facts and graphs are selected and rewritten for the actual
> product; merely renaming the archived report does not meet this requirement.
>
> ### 5.1a Final-product results and business interpretation (A8)
>
> **Product results**, directly after How the product works, presents the selected product's
> forecast-versus-observed charts, error over time and by material regimes, explanation/sensitivity
> results, and interval coverage together with width. Each graphic names the policy/artifact,
> population, dates, units and evidence class. Historical development, unused-data evaluation and
> prospective issued forecasts are visibly separate. Use the §5.1 coverage map across these
> adjacent sections; do not transplant another model's evidence or duplicate every topic.
>
> **Business insights**, directly after Product results, explains the intended use, measured
> benefit, losses and limits. Where a decision-policy evaluation exists, show cumulative net
> profit/value over the full named period, against the declared benchmark, with units, costs,
> constraints, initial conditions and risk/loss context. Label simulated/backtested results versus
> realized operation; preserve failed and missing days and disclose capital/denominators for
> returns. Forecast error reduction and interval coverage are not profit or trade-success rates.
> Business success percentages name the decision, formula, denominator and evaluation window.
> If this evaluation is not yet authorized or available, retain the section with the specific
> gap and measured forecasting implications; do not manufacture a profit curve or imply gains.
> Economic modelling stays governed by the research/use-case protocol (programme §4.E).
>
> ### 5.2 Chapter grammar
>
> Preserve the inherited slots: question/change diagram; main paired-difference chart for both
> primary scores with 95% intervals; one-sentence reading; at most three things not established;
> dated decision; evidence row; named detail sections.
>
> The detail menu remains method; per-period consistency including absolute errors; stress period;
> coverage and width; protocol and review. The transition summary in §4 uses these slots, with links
> to deeper results. v1's archive is not forced into the modern chapter grammar.
>
> One scrolling history page remains the rule. The self-contained page budget remains 2.0 MB.
> At v5, or before adding a chapter that would exceed it, propose compaction to the Owner. Moving
> full chapters off the page requires amendment of the one-page decision.

**`docs/PUBLISH_RULES.md` revision 1.5 §5.1** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 46 lines, 5089 bytes, SHA-256 `4535c0d2ee830a525f5152a9669910a52695f5df057e89198c3aecf36a33770c`):

> ### 5.1 The twelve product subjects and their lifecycle
>
> **One comprehensive current-product explanation; concise generation histories.** The Owner's
> clarification is that the depth of the original report's subjects 1–12 belongs to the product,
> not to v1 as a historical generation. It is not sufficient to move only model-independent prose:
> features, validation, explanations, reliability and reproducibility must describe the actual
> product too. Research chapters retain their required decision/evidence slots but do not each
> acquire a duplicate full product manual.
>
> The original report combines 6–7 under one explainability heading and includes a 3b spectral
> subsection. The following is a coverage map, not a requirement to preserve its numbering or wording:
>
> | Original subject | Required current-product explanation | Identity / caveat to preserve |
> |---|---|---|
> | 1 · The data | Target, sources, date range, cadence, units, preprocessing, availability and cutoffs | Actual product data contract and source rights; distinguish training, evaluation and operational inputs |
> | 2 · Three regimes | Material price regimes, negative prices and why these affect evaluation or use | Periods and plots from eligible data; do not silently refresh research plots beyond the permitted boundary |
> | 3 · Feature catalog | Inputs/features actually used, why they are eligible and what was excluded | Current frozen policy's feature set; historical selection experiments remain dated evidence |
> | 3b · Spectral view | Explain seasonal-feature reasoning where relevant and supported | Not a mandate to rerun or reproduce a spectral analysis for every model; omit the technique if inapplicable and explain the design directly |
> | 4 · Validation design | Forecast origin, temporal splits, leakage protection, baselines and evaluation windows | Actual governing protocol, with development, one-shot and live evidence separated |
> | 5 · Results | Product's measured point/interval performance, uncertainty and meaningful comparison | Results for this product/artifact; historical research improvement is not substituted for a product test |
> | 6 · Explainability: attribution | What the chosen explanation method says about the product's predictions | Model/output/population to which it applies; SHAP is an example, not a universal mandated method |
> | 7 · Explainability: sensitivity/importance | What an appropriate robustness, importance or sensitivity analysis establishes | Distinguish attribution from incremental value or causality; no transplantation of v1 rankings |
> | 8 · Regime-stratified error | Where the product succeeds or fails, with relevant groups, counts and uncertainty | Evidence-supported strata and thin-subset limitations; no invented evaluation |
> | 9 · Reliability | Observed interval coverage and width, applicable calibration stages and limitations | Actual interval pipeline; v1's three stages are not imposed on a different method |
> | 10 · Next-day forecast | Product output and how to read it; useful chart and actual controls | Explicit replay/inference/live identity; only eligible Live can show current issued forecasts as live |
> | 11 · Honest limitations | Data assumptions, failure modes, generalization and operational limits | Limitations of the active product; retain adverse facts and evidence-class qualifications |
> | 12 · Reproducibility | How to run/reproduce the product, artifact/policy identity and useful evidence routes | Current verified commands and service routes; do not reuse historical container instructions as current |
>
> Every subject is accounted for as supported, not yet evaluated, or inapplicable with a specific
> reason. This presentation obligation does not authorize missing research. A missing result is
> shown honestly and routed to the research plan; any required product-qualification gate still
> has to be met under that plan. Do not display an old model's graph under the new product heading
> or assert “not applicable” solely because the evidence is inconvenient.
>
> For a product replacement, its publication packet identifies the incoming and outgoing product,
> rechecks these subjects against incoming evidence, updates model-specific graphs and instructions,
> retains genuinely shared material after an applicability check, and preserves the outgoing evidence
> as history. Publish the updated product identity and documentation together. A data-only update
> under an authorized frozen policy updates its issuance/freshness/evaluation metadata; it does not
> pretend to be a new model release or trigger a new full historical narrative every day.
>
> The original “DE-LU day-ahead price forecasting” report is currently at the bottom because it is
> the preserved v1 archive. Retain its protected text/behaviour and an explicitly historical route,
> but do not make it the only route to understanding the current product. The active-product section
> is maintained outside that archive. Its facts and graphs are selected and rewritten for the actual
> product; merely renaming the archived report does not meet this requirement.

**`docs/PUBLISH_RULES.md` revision 1.5 §5.1a** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 19 lines, 1543 bytes, SHA-256 `51b54d5baf606a796386a99bd5d089df7ec976f92e89fdedc16d66163eab5eea`):

> ### 5.1a Final-product results and business interpretation (A8)
>
> **Product results**, directly after How the product works, presents the selected product's
> forecast-versus-observed charts, error over time and by material regimes, explanation/sensitivity
> results, and interval coverage together with width. Each graphic names the policy/artifact,
> population, dates, units and evidence class. Historical development, unused-data evaluation and
> prospective issued forecasts are visibly separate. Use the §5.1 coverage map across these
> adjacent sections; do not transplant another model's evidence or duplicate every topic.
>
> **Business insights**, directly after Product results, explains the intended use, measured
> benefit, losses and limits. Where a decision-policy evaluation exists, show cumulative net
> profit/value over the full named period, against the declared benchmark, with units, costs,
> constraints, initial conditions and risk/loss context. Label simulated/backtested results versus
> realized operation; preserve failed and missing days and disclose capital/denominators for
> returns. Forecast error reduction and interval coverage are not profit or trade-success rates.
> Business success percentages name the decision, formula, denominator and evaluation window.
> If this evaluation is not yet authorized or available, retain the section with the specific
> gap and measured forecasting implications; do not manufacture a profit curve or imply gains.
> Economic modelling stays governed by the research/use-case protocol (programme §4.E).

**`docs/PUBLISH_RULES.md` revision 1.5 §6** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 31 lines, 2318 bytes, SHA-256 `4fb26baeacf12ff7dfac14ed5f1efbb32161c91f21e44476c8e47da132f15fe7`):

> ## 6. Charts, discovery and navigation
>
> Every primary chart carries a plain question/finding, metric, comparator, population, evidence
> class, units, readable marks, reference line, finding, qualification and evidence route. Comparable
> panels share scales; an additional labelled difference view may expose smaller effects. Do not
> use smooth time-series imagery for discrete generation or fold comparisons.
>
> No meaning depends on colour or hover alone. Use direct labels, shape/line style and readable
> values. Distinguish a reference line from a target. Exact-value tables retain definitions and units.
> Mobile variants reorganize the chart; they are not desktop SVGs shrunk beyond legibility.
> Research chart text is at least 12 px at 390 px. Visual tokens remain the Owner's decision.
>
> **A5 establishes a discovery contract:** every explanatory result chart offered on the report has a
> descriptive route from its generation's visible summary, or from the active-product documentation where
> appropriate. The link says what the reader will see. A route opens ancestor disclosures and lands
> on a heading visible below the sticky header. A chart's existence, a hidden source link or a generic
> “Details” control does not by itself demonstrate discoverability.
>
> This does not require all charts open by default. A compact “Explore these results” list can link
> to absolute errors, period consistency, stress-period behaviour, hourly errors and coverage/width.
> Archive charts may use the clearly labelled archive route and its internal contents navigation.
> Technical audit-only plots are labelled as such and need not all be promoted onto the main path.
>
> The existing navigation remains compact: Results, Journey, Evidence, with generation navigation
> secondary. No stacked sticky bars. Preserve deep links, descriptive link text and a return route
> from the archive. External demo/tracking destinations are identified as external.
>
> Check discovery by starting at the actual default page with disclosures closed. Record the labels
> and actions taken to reach each advertised chart. A screenshot produced after opening every
> disclosure proves rendering, not this route. Test the deep link directly and by keyboard as well.
> This is separate from the six fixed cold-reader questions; do not coach that reader with locations.

**`docs/PUBLISH_RULES.md` revision 1.5 A2** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 14 lines, 996 bytes, SHA-256 `9e62954aac8c9874c50a3769d37f70e6a68368fd36ad8a58c9104a3520846ca6`):

> ### A2 — Measure usable screen depth
>
> **Observed need:** review V2-02 measured PASS against raw page coordinates while the complete
> orientation statement arrived on screenshot 3/4, beyond the intended two/three-screen experience.
>
> **Replacement for v1 §1 orientation placement calculation:** “For a limit of N screens with
> viewport height H and a persistent header of measured height h, the finding sentence's bottom
> must be at or before N×H−(N−1)×h in document CSS pixels. If header height changes, use the largest
> height observed on that route. Verify the statement is readable through N consecutive screen
> captures advanced by the usable viewport height; anchored headings remain unobscured.”
>
> N remains 2 at 1440×900 and 3 at 390×844; headline visibility remains unchanged.
> **Check:** both engines, disclosure-closed default layout, measured header plus consecutive captures.
> **Maintenance:** add header measurement to the placement check; no fixed historical header constant.

**`docs/PUBLISH_RULES.md` revision 1.5 A5** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 13 lines, 953 bytes, SHA-256 `4518287504cd82fddf14dfd1f609742d343ccaf4fbab9478e6abfc5bc41a13f9`):

> ### A5 — Make explanatory charts discoverable
>
> **Observed need:** the Owner could not find graphs shown during review. The review opened disclosures
> to inspect rendering; successful rendering did not prove an ordinary reader could find those graphs.
>
> **Addition to v1 §6/§11:** “Each explanatory result chart has a descriptive route from its generation's
> visible summary or active-product documentation. The route opens the needed disclosures and exposes an
> unobscured heading. Verify routes from the closed default view, not only from direct URLs or an
> all-expanded screenshot. Clearly labelled archive navigation may serve archived charts.”
>
> **Check:** follow the visible route by mouse/touch and keyboard in both engines, including phone;
> record the label, destination and resulting chart. Preserve the original cold-reader questions.
> **Maintenance:** generate route labels/targets from chapter chart metadata; avoid a separate manual index.

**`docs/PUBLISH_RULES.md` revision 1.5 A8** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 25 lines, 1924 bytes, SHA-256 `72aac9b9fb2c1e8cb04271c1bad3ca8f1b871817f154fba3c35697f36c9e34b3`):

> ### A8 — One final product, daily operation and product-first results
>
> **Observed need:** the current split between research v3 and demo v1 does not express the
> Owner's intended final product. A4 did not place dedicated scientific results and business
> interpretation before model comparisons; original A7 did not require daily retraining.
>
> **Amendment:** at the Owner-designated final-product transition, §§5, 5.1a and 7.2 govern one
> product/demo/daily-policy identity, the specified product-first page order, daily training,
> defined percentage scores, and honest uncertainty/business claims. For this triggered layout,
> §2 applies A2's early-placement bound to the product finding, not the later model comparison.
> Only this explicit order/placement change supersedes A4 and v1's early research-comparison
> position; comparison content, later sections and all other applicable acceptance remain.
>
> **Check:** trace designation → registry/policy → daily artifacts → issued predictions → demo,
> panel and documentation. Reproduce scores and any business series from source records;
> check timing/no outcome leakage, missing/zero/negative prices, failed fit/issuance, stale data,
> partial days and DST. Verify the default section order, product-first placement, descriptive
> routes and served identity in the existing browser matrix. A future independent verdict binds
> the implementation; writing this rule is not a PASS. Unperformed economics are disclosed, not
> fabricated; unsupported daily training remains a blocker unless the Owner grants an exception.
>
> **Maintenance:** one product identity and issuance/scoring record feed all surfaces; reuse
> the existing subject and chart maps. Daily records and monitored operation have real storage,
> runtime and operator costs, to be bounded in the future operational brief. This amendment adds
> no model search, paid service, new economic experiment or current implementation.

**`capstone_v21.md` v21-r20 §24.14** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 115 lines, 7426 bytes, SHA-256 `5d38de24b3c68ec01e2f5c4e6eaf368c253485107549fc2d85c3c71ccf2f5349`):

> ### 24.14 Publishing and going live before 4.7T (v21-r20)
>
> **What this section does.** It applies the Owner's decision 28 of 2026-11-05
> (`docs/track-b/owner-decisions-2026-11-05.md`, SHA-256 `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`).
> - It governs where it differs from §24.2, §24.9, §24.10, §24.12's list "For CP-18", §24.13's list "For CP-18" and
>   decision 25's order.
> - Every term below was set without any 4.7T outcome, since none exists.
>
> #### What stays exactly as registered
>
> - **A1's freeze.** CP-17c's policy identity `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`,
>   its manifest and the frozen package stay unchanged. `refreeze verify` guards them, and the live pipeline
>   calls the package without editing it.
> - **4.7T, in every registered term** (§24.12, §24.13):
>   - the window, delivery days 2026-09-07 to 2026-12-05;
>   - the candidate, the comparators, the scores, the pass conditions, the margins and the failure rules;
>   - the vintage terms (the protocol's §3);
>   - the machine (the Owner's Mac, no cloud) and the H2 checks before its first issuance;
>   - the calendar: it opens no earlier than 2026-12-04, after the price for 2026-12-05 is published;
>   - the audit, the Owner's declaration and his retrieval approval.
> - **4.7T issues its window itself.** Its issuance starts from the freeze-origin state, runs on the Owner's Mac
>   under its terms, and keeps its own store. Nothing the live product issues is 4.7T's issuance or score.
> - **No registered term changes from here until 4.7T is scored.** A proposal to change one returns 4.7T to the
>   Owner as BLOCKED.
>
> #### What changes
>
> **1. The order (decision 25).** CP-18's activation and a publication now come before 4.7T:
> - **CP-18c**, the activation: the live product starts and runs daily;
> - **PRES-5**, the publication: the research since v5, A1 in the comparison, and the live product;
> - **then 4.7T** at its date, and the publication of its result.
>
> Decision 25's "one complete publication" becomes these two publications.
>
> **2. The red line, for the live pipeline only.** §24.2's guard retires for the live pipeline at CP-18c, not
> after 4.7T.
> - **The live pipeline downloads all the data through the present** and trains on it, as §24.2's last
>   paragraph allows ("The live product, once running, trains on all the data available to it").
> - **Every research path keeps the guard.** The development downloaders and builders still refuse any row after
>   2026-09-06, and CP-17c's development builder stays as frozen.
> - **Reading.** The live data is handled by code.
>   - An agent that operates the live pipeline may read its logs and records, only to operate it.
>   - No agent uses data after 2026-09-06 for any research number, chart, choice or registration before 4.7T is
>     scored.
>   - §24.2's rule on reports, news and analyses about market events after 2026-09-06 is unchanged.
> - **The exposure ledger.** Its pinned file `docs/track-b/exposure-ledger.md` stays byte for byte. Later entries
>   go in its continuation, `docs/track-b/exposure-ledger-continued.md`, which the audit reads with it.
>   - CP-18c seeds the continuation with decision 28's entry, dated by the live pipeline's first
>     retrieval.
>   - **Its impact assessment:** nothing 4.7T tests can change after it. Everything 4.7T tests was frozen,
>     registered and pushed to the public repository before decision 28: `land/cp-17c`, 2026-10-30, and the
>     protocol at its freeze. `refreeze verify` checks the freeze on every run.
>
> **3. The audit (§24.2's standard) reads with this.**
> - **The live product's daily fits** are the frozen policy's own operation, not research fits. They sit
>   outside the standard's "fit" and are recorded in the continuation.
> - **The standard's test applies unchanged** to everything 4.7T tests.
> - **The Owner's declaration** covers his decisions before 4.7T opens. Decision 28 used no information after
>   2026-09-06.
>
> **4. The live product's start.**
> - **The live store** is seeded at the freeze origin, 2026-09-06, with CP-18a's genesis command. It is carried
>   to the first live day with CP-18a's `carry`.
> - **The days between** are outside the live record and are never issued by the live product.
> - **The live product's forecasts for window days,** from its first live day to 2026-12-05, are its own. Each
>   carries its actual run time, and none is 4.7T's.
> - **After 4.7T** the live store continues. §24.12's carry "from 4.7T's last window day to the first live day"
>   becomes this carry from the freeze origin.
>
> **5. What the live product shows.**
> - **It shows the live record** under PUBLISH_RULES A7 and A9: the issued forecasts, the outcomes as published,
>   and the issued forecasts' prospective scores.
> - **A1's status** reads "final candidate · pending 4.7T" (O13).
> - **The prospective scores** are labelled "prospective evaluation in progress" (§24.9).
> - **No display presents a live score** as 4.7T's, or as a test result.
> - **The development-period displays** stay on days through 2026-09-06.
>
> **6. The publication (PRES-5).** Decision 28 is the separate decision that §24.10 requires for publishing
> CP-26's and CP-28's results.
> - **It covers:**
>   - A1 in the published comparison, on the same data as v5's comparison;
>   - CP-26's re-baseline on every development day;
>   - CP-28's selection;
>   - the freeze, with 4.7T's registered terms;
>   - the live product.
> - **Its research numbers use development data only.**
> - **It runs under PUBLISH_RULES 1.5.**
>
> **7. The runner and the secrets.**
> - **Until the Owner enters the three repository secrets** (decision 25), the daily runs use the local fallback
>   on the Owner's Mac (§24.13), with the credentials used only inside the consuming process.
> - **The `macos-26` schedule is enabled** once the secrets exist.
> - **The issuing host and the H2 checks are unchanged** on either machine.
>
> **8. What this supersedes:**
> - **§24.2:** "After 4.7T, CP-18's brief retires the guard for the live pipeline only" (item 2);
> - **§24.9:** the order of "Then: CP-18 … and site activation" (item 1);
> - **§24.10:** "No publication" (item 6);
> - **§24.12's list "For CP-18":** the carry from 4.7T's last window day (item 4);
> - **§24.13's list "For CP-18":** the item on the red line on the runner (item 2).
>
> S_14 (§24.13, H4) is unchanged.
>
> #### Decisions recorded (v21-r20)
>
> | # | Decision | Who |
> |---|---|---|
> | 28 | Publish and go live now; A1 frozen and untouched; 4.7T exactly as registered | Owner, 2026-11-05 (`docs/track-b/owner-decisions-2026-11-05.md`, SHA-256 `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`) |
> | P1 | "All the data" for the published research means every development day. Research numbers on window days wait for 4.7T, so that it stays the one test | Orchestrator, under decision 27 |
> | P2 | The live start: genesis at the freeze origin, carried to the first live day. The live product's window-day forecasts are its own, never 4.7T's | Orchestrator, under decision 27 |
> | P3 | The guard retires for the live pipeline only. The exposure ledger continues in a new file, because its own file is pinned | Orchestrator, applying decision 28 |
> | P4 | The local fallback runs until the repository secrets exist | Orchestrator, under decision 27 |
>
> **The Owner's declaration (§24.2)** covers decision 28. P1–P4 are registrations under §24.2's test, which the
> audit checks, as R1–R7 and H1–H4 are.

Map every applicable item to evidence. The extract below does not narrow this bar.

## Task-specific supporting extract
- **The paths this round never touches,** because the live product owns them:
  - `src/cp18/`, `space-product/`, `scripts/build_product_space.py`, `.github/workflows/daily.yml` and `live/`;
  - `tests/cp18c/`, `reports/cp18c/` and `docs/track-b/evidence/cp-18c/`;
  - `docs/track-b/exposure-ledger-continued.md`.

  `src/cp18/publish.py`'s `normalized` may be imported or read, never edited.
- **The red line for research.** No research number, chart or choice uses data after 2026-09-06. The report reads no
  live record.
- **The ceilings:** 10 local machine-hours, summed over workers' wall time, at most 4 concurrent workers, CPU only.
  Keep a ledger, and stop before a ceiling.
- **Presentation.** Visual choices are the Owner's (O16). Build to the existing page's tokens and chart components.
  Do not hold the round for visual taste.

## Applicable constraints
- **Homebrew's `node` stays pinned and installed.**
- **Credentials:** none are needed. Never print, log or echo a credential value. Export `MLFLOW_DISABLE_TELEMETRY=true`
  and `DO_NOT_TRACK=1`.
- **Allowed paths:**
  - `docs/index.html`, `README.md`, `reports/cp3/pages_build.json`, and the report's build, claim layer and their
    tests (`scripts/build_pages.py`, `scripts/readme_research.py`, `scripts/cp3_readme.py`, `src/delu_forecast/`,
    `tests/`, apart from `tests/cp18c/`);
  - `scripts/check_links.py` and `scripts/publication_receipt.py`, with their tests;
  - `docs/track-b/research-content/`, the registry and its draft files;
  - `reports/pres6/`, `reports/presentation/` (the release checks `pres-6-*` and the MLflow index if a route
    changes);
  - `docs/track-b/evidence/pres-6/`.

  No anchor, governance file, `docs/PUBLISH_RULES.md`, frozen record or live-product path.
- **Before editing a tracked file,** check that no earlier evidence binds its bytes. That includes:
  - `src/cp26/harness.py`'s `PINS`;
  - `tests/pres5_landed_code.py` (O34's record of CP-26's presentation modules);
  - every freeze manifest's governance pins.
- **Tools:**
  1. run `scripts/gauntlet.py start pres-6` first, from the primary checkout;
  2. create the worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/pres-6 .local/worktrees/pres-6/lead main`;
  3. run the independent check through `critic-open`, `critic-brief` and `critic-close`. **The first line of the
     Critic's launch assignment** forbids opening the Claude memory directory;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`).
- **Owner-facing Git commands** must be non-interactive.

## Timebox
About 16 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **PRES-6's execution** under decisions 27 and 28 and this brief, on `gauntlet/pres-6`. The Orchestrator delivers this
  brief under the Owner's grant, and that delivery is the grant.
- **No external action.** No MLflow write, Space upload, push, landing, merge or tag on `origin`, Pages deployment or
  governance edit. Those that apply are the Orchestrator's, after the return.

## Stop and return
- **First commit.** The first commit copies the canonical brief byte for byte to
  `docs/track-b/evidence/pres-6/issued-brief.md`.
- **Questions.** If the brief is unclear or wrong, ask the Orchestrator, or stop at the conflict. PUBLISH_RULES, the
  anchor and the Owner's decisions prevail over this brief.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3, with both terminal SHAs and
  the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - Its "Open risk or exact owner action" section gives packet §8's steps and every presentation item still open, with
    a proposed ruling for each.
  - Name the machine-hours used.
- Leave your worktree and branch for the LAND.
