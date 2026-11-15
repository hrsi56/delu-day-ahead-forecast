# Track B Checkpoint Brief — PRES-7 (Business insights with the profit chart, and PRES-6's follow-ups)

*Issued by the Orchestrator on 2026-11-16, Asia/Jerusalem, under the Owner's decisions 27, 28, 30 and 32.*

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`, public; Pages serves `main:/docs`).
- Authorized checkpoint: PRES-7, exactly one.
- **Beside it** runs CP-18d, the live product's round, in another Lead's own worktree. The two share no path.
- **What it does.** It publishes CP-29's economic evaluation in the report's Business insights, as the Owner asked
  ("ואז PRES-7 שמציג את גרף הרווח", decision 32).
  - **Business insights** shows the cumulative net profit of a price-taking 1 MW / 2 MWh battery, scheduled from each
    forecast and settled at the cleared day-ahead price, on the development days (P-all, 2,068 days): v6, the
    similar-day naive and perfect foresight, with "doing nothing" as the zero line. Beside it: the share of perfect
    foresight captured, the losing days, the wear-cost sensitivity, the regimes, the paired difference v6 − naive with
    its interval, and v6 against v5 on P-v5, whose interval spans zero.
  - **The section's gap sentence is replaced:** a decision-policy evaluation now exists, as a simulation on
    development days, labelled **simulated, development, post-selection**.
  - **Beside it, four follow-ups:**
    - **Decision 30:** the report has no page-size limit. `tests/test_31`'s size-budget assertion is removed; the
      page's size is still measured, recorded in `reports/cp3/pages_build.json` and stated in the packet.
      `docs/PUBLISH_RULES.md` is not edited: CP-26's harness pins its bytes, and decision 30 supersedes §5.2's budget
      sentence and §14's trigger until the rules' next revision;
    - **PRES-6's O51 item 7:** the comparison chart no longer clips v6's interval-score marker on phones (the phone
      axis's lower bound);
    - **PRES-6's O51 item 8:** one glossary-and-wording pass over the opening and the comparison: "Owner", "4.7T",
      "re-baseline" and "A1 in the frozen records" defined at first use; the policy counts made consistent; −7% beside
      −6% explained by their populations; the two development-period ends named; "descriptive" and "confidence"
      intervals distinguished. No number changes;
    - **CP-29's open items 3–5:** the untraded days' counts are stated; the claim layer's `business.gap` is rewritten
      and W54 narrowed to its "error or coverage called a profit" half; W56 and W57 stay; doing nothing is the
      chart's zero line.
- **Its numbers are development data only,** delivery days through 2026-09-06 (r20 §24.14). The report shows no live
  forecast, score, price or profit. 4.7T stays the one test of v6.
- Ratified plan anchor: the publication anchor `docs/PUBLISH_RULES.md`, revision 1.5, SHA-256
  `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`, with decision 30 superseding its page budget.
  - Apply its precedence and amendments A1–A12. Record any that is not applicable, with the reason.
- **Research constraint anchor, read-only:** `capstone_v21.md` v21-r20, SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`, §16.3 and §24.14.
- **The economic contract, read-only:** `docs/track-b/economic-policy-contract-2026-11-15.md` (decision 32), SHA-256
  `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`, with O58's clarifications. Its §§8–9 (disclosures and what it does not claim) bind every sentence.
- **Execution inputs.** Verify each hash before relying on it:

  | Input | Path | SHA-256 |
  |---|---|---|
  | The approved economic-policy contract (decision 32) | `docs/track-b/economic-policy-contract-2026-11-15.md` | `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889` |
  | CP-29's landing record | `docs/track-b/cp-29-landing-2026-11-16.md` | `010c16f169ccc65e64e8b63496f7a690742094c1d6454930ebb858f8b7002a0a` |
  | CP-29's report | `reports/cp29/report.md` | `4787056aef44a906897138a835ffa8250b62899a6046275ae842861a393458fb` |
  | CP-29's summaries | `reports/cp29/summary.csv` | `3392db1b0371f28755d496d5fa9c683c3b76f395ec1fb905a7fc28900bc5196f` |
  | CP-29's paired differences | `reports/cp29/paired.csv` | `f07d4c17a91d60a0789666ff6b04d648f2f46a4cdc9f79abb6a841db14564b18` |
  | CP-29's daily rows (the cumulative series) | `reports/cp29/daily.csv` | `bf39cc7b875437ba003f7a3a17c3e178d49c5e6cb5be52d9e61629f66b237ae3` |
  | CP-29's claim map (C1101-C1108, W56, W57) | `docs/track-b/research-content/cp29-claims.md` | `ef01e60a2a48d83e83582d6c743377482726ea0c36cb5a0995f56317287b82c6` |
  | CP-29's publication packet (§0, its open items) | `docs/track-b/evidence/cp-29/publication-packet.md` | `de2e52cc854a14555e1ee04a1bd3d925de170859700d77c802618123596aed4b` |
  | PRES-6's landing record (O50, O51) | `docs/track-b/pres-6-landing-2026-11-15.md` | `415e2e7c89a47018546b91ac4bd46f40622440fdbc049b5b39b782196bbc198b` |
  | PRES-6's publication packet (§10.3's items 7 and 8) | `docs/track-b/evidence/pres-6/publication-packet.md` | `83468823cc363f24a2d3b3031308524e62b6f857a038518d3cb5033549716cb6` |
  | PRES-6's fresh-reader record (the confusions) | `docs/track-b/evidence/pres-6/fresh-reader.md` | `742c4b1dff00cf2c8fdacdb9d62e80fcca4ddd2f11e1535ffac12598cbdd7533` |
  | The Owner's decisions 29-31 (decision 30: no page limit) | `docs/track-b/owner-decisions-2026-11-15.md` | `ad1beb9f9e7ee235195db96d63d8c3684a5d664f29d51622c866538620c7a323` |
  | The page-structure test (the size budget) | `tests/test_31_page_structure.py` | `af9b7b9448bfaa4ab749263ef13a2f1fe82c13e2259bd56adb92ee6ad6a8c2cc` |

- **The Owner's decisions:** 1–19 bound by the frozen copies; 20–28 (`progress.md` and the dated records); 29–31
  (`docs/track-b/owner-decisions-2026-11-15.md`); 32 (the contract's header).
- **The Orchestrator's rulings that bind the wording:** O13, O14 (F1 at 0.082 EUR/MWh), O16, O26–O30, O44–O46, O50,
  O51, O57–O59.
- **Decision 27** has the Orchestrator decide every open presentation matter that costs the Owner nothing, and log it.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the commit that records this brief's issue, a descendant of CP-29's
  closure through the runner's data-only commits. The issue commit changes only `progress.md`.
  - **`main` moves during this round.** The live product's daily runner pushes data-only commits to `main`, by the
    author `delu-daily`, touching only `live/`. Never write under `live/`. The packet's LAND commands assume a moved
    `main`. GitHub's scheduler runs about 7–8 hours late, so the runner's commits can arrive at any hour.
  - **CP-18d runs beside this round** (O56) on the live product's paths, in `.local/worktrees/cp-18d/`. Never touch its
    worktrees or branch. If it lands first, `main` gains its changes to `src/cp18/`, `space-product/` and
    `.github/workflows/`.
  - **Tags:** every landed checkpoint's `land/` and `evidence/` tags are pushed, except `evidence/cp-26` = `ca20331`,
    which is **local-only and never pushed**. The rulesets refuse moving or deleting a `land/`, `evidence/` or
    `archive/` tag, and refuse pushing a `gauntlet/*` branch.
- **Working tree:** the primary checkout is on `main` and clean apart from ignored material.
  - **The Orchestrator uses it.** Never switch its branch, and never write a tracked file in it. Your only writes
    there are under `.local/artifacts/pres-7/`, `.local/tmp/pres-7/` and the worktrees under `.local/worktrees/pres-7/`.
  - **The canonical brief** is `.local/artifacts/pres-7/issued-brief.md`. Package that file byte for byte.
  - **A Finder `.DS_Store`** may sit in ignored folders such as `space-product/`. It is local-only and fails one
    CP-18c test in the primary checkout only. A clean worktree does not have it.
- **The published surfaces:**
  - the report `docs/index.html`, SHA-256 `5e294d40790f3415c14cf932e94f1351e2e99a0b84d6efd3d2321046d7eccdaa`,
    1,997,873 bytes, in A8's order (PRES-6). Its Business insights states that no economic evaluation exists;
  - the README, SHA-256 `da9ae187766c895d102676b16a5870540029d471b26687fe78cc3319edc77e1a`;
  - MLflow on DagsHub, the experiment `delu-generations`, with 105 runs. This round writes nothing there;
  - the Space `Yarden-Viktor/delu-day-ahead-forecast`, the live product, published daily by the runner. This round
    changes nothing there.
- **What already exists for this round:** CP-29's landed records (`reports/cp29/`, `src/cp29/`) and its claims
  C1101–C1108 on the claim layer's `PRES7` surface (`src/delu_forecast/research_claims.py`,
  `docs/track-b/research-content/cp29-claims.md`); PRES-6's build, claim layer and Product results; the publication
  tools.
- **Credentials:** none are needed. This round makes no external write.
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
When this checkpoint closes, after the Orchestrator's post-return steps, the report's Business insights shows what v6's
forecasts were worth to a battery on the development days, against the naive and the ceiling, with every limit stated.

1. **The profit chart (§5.1a).**
   - **Cumulative net profit in EUR over P-all**, one line each for v6 (median rule), the naive (median rule) and
     perfect foresight, with doing nothing at zero. From CP-28's and CP-29's committed rows only
     (`reports/cp29/daily.csv`); every value derived, none typed.
   - **The graphic names:** the battery and its costs (C1101); the policy and artifact; the population, its dates
     and units (EUR, for 1 MW / 2 MWh); its evidence class, simulated, development, post-selection.
   - **Beside it,** from CP-29's claims C1101–C1108: the share of perfect foresight; the losing days and the largest
     daily loss; the drawdown; the wear sensitivity (€0, €25, €50); the regimes; v6 − naive with its 95% interval;
     v6 against v5 on P-v5 (an interval spanning zero: no advantage shown); the risk-aware variant; the untraded days.
   - **The limits, in plain words, on the page:** a simulation, not realized income; day-ahead arbitrage only, which
     is not a battery's whole income (no intraday, balancing or reserves); a price-taker; hourly; post-selection
     (v6 was chosen on these days, so its result is optimistic for v6); not a trading recommendation; no return or
     payback (no capital cost).
   - **Forbidden** (§5.1a): a forecast error or coverage figure called a profit or a success rate; an annualized return;
     any live or prospective profit.
2. **Business insights' text.** The intended use, the measured implications, the evaluation's result, and its limits.
   The old gap sentence goes; the section says what is still not evaluated (intraday, reserves, a real battery's
   costs, the live record).
3. **The order (A8)** is unchanged: the opening, How the product works, Product results, Business insights, How the
   models compare, the rest. A2's early-placement bound on the product finding still holds, measured in the browser
   matrix; anything added above it is re-measured.
4. **The README** carries the same business claims, through the claim layer.
5. **Decision 30, O51 items 7 and 8, CP-29's items 3–5:** as in the Target. Each glossary or wording change is listed
   in the packet, with "no number changed" checked by a diff of the rendered numbers.
6. **The page's size** is measured and stated. There is no limit (decision 30), but the page stays one self-contained
   file, and the packet states its bytes and any growth.
7. **Review.**
   - The editorial review and a fresh reader, as the runbook provides. The fresh reader answers, among others: what
     the battery earned with v6 against the naive, and what the result does not show.
   - The independent Integration check passes at the candidate, and a focused recheck passes at the final SHA.
8. **The packet.** Its §8 names the exact payloads and the ready-to-run commands for the Orchestrator's steps:
   - the landing on a moved `main` (the runner's data-only commits) and the push, which deploys Pages;
   - the public post-deployment checks, including `scripts/publication_receipt.py`, with every link into the Space
     checked without following redirects. The Space's build for the receipt is assembled from the runner's latest
     publication as PRES-6's landing record describes, unless CP-18d has landed its full artifact;
   - A12's independent post-deployment check where it can add something.

The publication is complete only after those steps and their public evidence. A local PASS is not a deployed
publication.

## Complete authoritative checkpoint bar
- **PUBLISH_RULES 1.5 in full,** with decision 30 superseding the page budget. Every applicable clause, including the
  incorporated baseline, A1–A12 and §13's acceptance record. A8 is in force (O46).
- **The runbook** `docs/track-b/publication-runbook.md`: every touchpoint that applies.
- **The packet template, every section.**
- **r20 §24.14** and **§16.3**, for what may be published now and on which data.
- **The contract's §§6, 8 and 9.**
- **Critic and return:** `docs/track-b/gauntlet-templates.md` §§2–3. This authorizes no fit and no new computation
  beyond rendering CP-29's committed rows.

Verbatim, extracted by `scripts/bar.py bar … --at 382c2010 --quote` from `main` at the issue.
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

**`docs/PUBLISH_RULES.md` revision 1.5 A6** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 15 lines, 1143 bytes, SHA-256 `df28e45b323f87ee4824c47e8d16b7c904793c3e7712da8e73edc50e1bd3cef7`):

> ### A6 — Specify public post-deployment evidence
>
> **Observed need:** postdeploy F01/F02 exposed unnamed demo controls and a public favicon request that
> report-only accessibility or local source checks had not settled. Earlier PASS records did not
> prove current public behaviour. The existing postdeploy step lacked this explicit evidence contract.
>
> **Addition to v1 §12 step 9:** “Verify the served identity and public behaviour of each advertised
> surface, using fresh observations against the applicable browser/interaction requirements. Record
> service revisions, raw/normalized hashes as applicable, first failures and retries, test limitations,
> and the difference between product defects and missing evidence. Local output and prior approvals
> cannot substitute for public checks. Compare previous findings only after forming independent findings.”
>
> **Check:** §10.3 identity records plus applicable §9 matrix and §10.4 verdict.
> **Maintenance:** reuse release checks against public URLs; retain existing probes and truthful scope.
> This clarifies evidence coverage, not a demand for real Safari/iPhone or a new research evaluation.

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

**`docs/PUBLISH_RULES.md` revision 1.5 A12** (the file `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`; the section 14 lines, 641 bytes, SHA-256 `76a6a3e5be37964991298fe116a24c61e1ed7b9f74066e47138af257161c4ce2`):

> ### A12 — The independent post-deployment check when it can add something
>
> **Observed need.** PRES-2, PRES-3 and PRES-4 each waived the check on the same basis: the served
> surfaces equalled what the independent review had covered, and every public check passed or
> passed on retry. A rule that is always waived is not a rule.
>
> **Addition:** §10.5.
>
> **Effective scope:** from the next publication. PRES-2–4's waivers stand as recorded.
>
> **Check:** the closure record names which condition arose, if any, and links the receipt.
>
> **Maintenance:** `scripts/publication_receipt.py` already records byte identity, mirror equality
> and retries.

**`capstone_v21.md` v21-r20 §16.3** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 30 lines, 2368 bytes, SHA-256 `3bec66a22d7fc86f6dcde441c82328229f94e0d49efe28abf63965ada4568c0e`):

> ### 16.3 What the product and demo expose
>
> The product panel comes first, followed by How the product works, scientific Product results,
> Business insights, How the models compare and all remaining sections in their existing order.
> [PUBLISH_RULES 1.1](docs/PUBLISH_RULES.md) §§5, 5.1a, 7.2 and A8 define presentation acceptance.
> The twelve-subject product coverage follows the actual final policy and its dated artifacts;
> the outgoing product's evidence stays historical. The primary demo uses the same product policy,
> and identifies the artifact/issue date and whether an interaction is a counterfactual scenario.
> An old replay may remain as labelled history, not as a different primary product.
>
> Show today's issued hourly forecasts versus available published outcomes, a defined percentage
> performance measure alongside MAE in EUR/MWh, and tomorrow's issued hourly forecasts and prediction
> intervals. Freeze the percentage formula, denominator, eligible population, scoring window,
> zero/negative-price treatment and any success tolerance before evaluation. A benchmark-relative
> percentage is labelled improvement, not correctness. Missing/pending outcomes are unscored;
> partial-day scores show completeness. Scoring uses the artifact that issued the prediction,
> not a newer fit. Record the price source, publication/revision times and outcome eligibility.
>
> Distinguish nominal prediction-interval level from measured coverage and width on an explicitly
> named past window. Neither means a point price has that percentage probability of being correct.
> Display separate last-training, data-refresh and issuance times, delivery date/timezone,
> freshness and failure state. No data or no evidence means a labelled unavailable state.
>
> Scientific graphics separate development, unused-data and prospective results. Business
> interpretation must separate forecast performance from an evaluated economic decision policy.
> Cumulative net profit/value, returns or business success rates require a frozen use case,
> constraints, costs, benchmark, denominator, complete time series and loss/risk disclosure;
> label simulated versus realized results. Without authorized evaluation, show the specific gap
> and measured forecasting implications. This is no authorization for trading, a new economic
> experiment or a fabricated profitable result; programme §4.E governs such evaluation.

**`capstone_v21.md` v21-r20 §24.14, "What stays exactly as registered"** (the file `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; the section 16 lines, 1161 bytes, SHA-256 `0e1f357969f5bad69b4e5dbc4682631196a77b4580381b6ef887cb96b7607c84`):

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

**The contract, §6** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 18 lines, 1393 bytes, SHA-256 `3eba0aa669aff0700fd50aee9db1642d3a756d8a27a5c09ad039949e918e131c`):

> ## 6. The measures
>
> For each benchmark, population and rule:
> - **cumulative net profit** in EUR over the named period, as a complete daily time series, with the per-day units and
>   the battery's size beside it;
> - **the share of perfect foresight captured:** the sum of the benchmark's daily profits divided by the sum of perfect
>   foresight's, over the same days. Perfect foresight's daily profit is never negative (it can do nothing), so the
>   ratio is defined on sums only; a population with zero perfect-foresight profit reports "undefined";
> - **the daily profit distribution:** mean, median, 5th and 95th percentiles;
> - **losing days:** their number and share, and the largest single-day loss;
> - **the maximum drawdown** of the cumulative profit curve;
> - **trading days:** how many days the rule traded, and the energy cycled;
> - **paired uncertainty:** the daily profit difference v6 minus the naive (and v6 minus v5 on P-v5), with a 95%
>   interval from a non-circular moving-block bootstrap over days, blocks of 14 days, 2,000 replicates, the seed fixed
>   in the research round's packet before computing. These are the same settings as PRES-6's regime intervals.
>
> **Not reported:** no annualized return, internal rate of return, payback or business case, since there is no capital
> cost model; no "success rate". Forecast error and interval coverage are not profit (PUBLISH_RULES §5.1a).

**The contract, §8** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 12 lines, 785 bytes, SHA-256 `ebbe45e7e0928d1311a3cb339ac7d9cf46f11cb5358babde1db7346e80768772`):

> ## 8. Disclosures
>
> - **A price-taker:** every schedule is filled at the cleared price, with no effect on it.
> - **Day-ahead only:** no intraday re-trading, no balancing energy, and no ancillary services (frequency containment or
>   restoration reserves). In practice these are a large share of German batteries' revenue, so this measures only the
>   day-ahead arbitrage value of the forecast, not a battery's total income.
> - **No outages,** no imbalance and no forecast failure: the schedule is executed exactly.
> - **Costs:** only those in §2. The wear cost and the exchange fee are stated assumptions; the grid-fee exemption is a
>   legal assumption that may change.
> - **Hourly, not quarter-hourly** (§5).
> - **Post-selection** (§5).
> - **Simulated, not realized:** no money was traded.

**The contract, §9** (the file `21a9208573668becd2af3d9e476855e3f8c0e66c85fc9097194bd6deae580889`; the section 6 lines, 280 bytes, SHA-256 `3952659973529e51957f60db8236c4066db319961116ef024f8e74d134ad8620`):

> ## 9. What it does not claim
>
> - not a trading recommendation, an investment case or a forecast of future profit;
> - not realized income;
> - not a property of v6 alone: the result depends on the battery, the costs and the rule stated here;
> - not 4.7T's result, and not a test of v6.

Map every applicable item to evidence. The extract below does not narrow this bar.

## Task-specific supporting extract
- **The paths this round never touches,** because the live product or CP-18d owns them:
  - `src/cp18/`, `space-product/`, `scripts/build_product_space.py`, `.github/`, `live/`;
  - `tests/cp18a/`–`tests/cp18d/`, `reports/cp18c/`, `reports/cp18d/` and their evidence;
  - `docs/track-b/exposure-ledger-continued.md`.
- **CP-29's records are read-only:** `src/cp29/`, `reports/cp29/`, `tests/cp29/`. A defect found in them is reported to
  the Orchestrator, not fixed here.
- **The red line.** No number, chart or choice uses data after 2026-09-06. The report reads no live record.
- **The ceilings:** 10 local machine-hours, summed over workers' wall time, at most 4 concurrent workers, CPU only.
  Keep a ledger, and stop before a ceiling.
- **Presentation.** Visual choices are the Owner's (O16). Build to the existing page's tokens and chart components; the
  profit chart follows Product results' chart grammar. Do not hold the round for visual taste.

## Applicable constraints
- **Homebrew's `node` stays pinned and installed.**
- **Credentials:** none are needed. Never print, log or echo a credential value. Export `MLFLOW_DISABLE_TELEMETRY=true`
  and `DO_NOT_TRACK=1`.
- **Allowed paths:**
  - `docs/index.html`, `README.md`, `reports/cp3/pages_build.json`, and the report's build, claim layer and their
    tests (`scripts/build_pages.py`, `scripts/readme_research.py`, `scripts/cp3_readme.py`, `src/delu_forecast/`,
    `tests/`, apart from the never-touch tests above), `tests/test_31_page_structure.py` included for decision 30;
  - `scripts/check_links.py`, `scripts/publication_receipt.py`, `scripts/check_reader_paths.py`, with their tests;
  - `docs/track-b/research-content/`, the registry and its draft files;
  - `reports/pres7/`, `reports/presentation/` (the release checks `pres-7-*` and the MLflow index if a route
    changes);
  - `docs/track-b/evidence/pres-7/`.

  No anchor, governance file, `docs/PUBLISH_RULES.md`, the contract, frozen record or live-product path.
- **Before editing a tracked file,** check that no earlier evidence binds its bytes: `src/cp26/harness.py`'s `PINS`,
  `tests/pres5_landed_code.py`, every freeze manifest's governance pins.
- **Tools:**
  1. run `scripts/gauntlet.py start pres-7` first, from the primary checkout;
  2. create the worktree with
     `git -C /Users/djourno/Downloads/PJM worktree add -b gauntlet/pres-7 .local/worktrees/pres-7/lead main`;
  3. run the independent check through `critic-open`, `critic-brief` and `critic-close`. **The first line of the
     Critic's launch assignment** forbids opening the Claude memory directory;
  4. check the return with `scripts/gauntlet.py return`.
- **Memory:** do not open or edit the files in the Claude memory directory
  (`~/.claude/projects/-Users-djourno-Downloads-PJM/memory/`).
- **Owner-facing Git commands** must be non-interactive.

## Timebox
About 14 active hours from orientation to the terminal return.

## Owner-only actions already authorized
- **PRES-7's execution** under decisions 27, 28, 30 and 32 and this brief, on `gauntlet/pres-7`. The Orchestrator
  delivers this brief under the Owner's grant, and that delivery is the grant.
- **No external action.** No MLflow write, Space upload, push, landing, merge or tag on `origin`, Pages deployment or
  governance edit. Those that apply are the Orchestrator's, after the return.

## Stop and return
- **First commit.** The first commit copies the canonical brief byte for byte to
  `docs/track-b/evidence/pres-7/issued-brief.md`.
- **Questions.** If the brief is unclear or wrong, ask the Orchestrator, or stop at the conflict. PUBLISH_RULES (with
  decision 30), the anchor, the contract and the Owner's decisions prevail over this brief.
- **The return.** Return exactly one of PASS / BLOCKED / INCOMPLETE, using templates §3, with both terminal SHAs and
  the verdict-only delta, checked with `scripts/gauntlet.py return`.
  - Its "Open risk or exact owner action" section gives packet §8's steps and every presentation item still open, with
    a proposed ruling for each.
  - Name the machine-hours used.
- Leave your worktree and branch for the LAND.
