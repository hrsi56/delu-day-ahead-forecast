# PUBLISH_RULES — publication anchor

**Revision:** 1.1 · **Updated:** 2026-09-29 · **Owner:** Yarden Viktor Dejorno

**Revision 1.1 authority:** the Owner explicitly approved the task-scoped Governance Lockdown
suspension after specifying one final product/demo/daily model and its page order (§16.1).
Revision 1.0 remains preserved at `evidence/pres-2:docs/PUBLISH_RULES.md` and governs PRES-2.
This revision adds A8 and strengthens conditional A7 for the future final-product transition;
it does not regrade PRES-1/PRES-2, designate a model now, or start training/deployment.

**Status: active publication anchor, established under the Owner's explicit task-wide
authorization on 2026-09-29.** The Owner requested this anchor, then expressly authorized all
actions necessary for this task after the need for a task-scoped Governance Lockdown suspension
was explained. That authority covers authoring and integrating this anchor and its amendments;
it is not a claim that the Owner personally reviewed every final sentence or rendered artifact.

**Effective scope:** A1–A6 govern the next publication after this authorization and all later
publications. A7 applies only when a live panel is separately authorized and its research/operational
prerequisites are met. PRES-1 and its historical reviews retain Publication Standard v1 as their
original acceptance contract. The currently deployed site has not been migrated by this task.
No implementation, publication, promotion, new research or scheduled operation is executed here.

This document consolidates the existing publication contract and adds the bounded revision
recorded in §15, based on the independent post-deployment review and the Owner's subsequent
questions. It is written for future authors, Engineering Leads, independent checkers and the
Orchestrator. Public-facing copy remains English. This internal anchor is not landing-page copy.

**Navigation:** authority and applicability (§1); reader and claims (§§2–3); generations (§4);
active-product documentation and graphs (§§5–6); demo/live (§7); surfaces (§8); verification (§§9–10); publication (§11);
coverage and acceptance (§§12–13); maintenance, amendments and authority record (§§14–17).

## 1. Authority, applicability and version identity

### 1.1 Read this contract without inventing authority

The following sources have distinct responsibilities:

| Source | Responsibility |
|---|---|
| [AGENTS.md](../AGENTS.md) and the applicable role contract | Governance Lockdown, role boundaries, credentials, Git and publication authority |
| The exact ratified research anchor named in the task and the Owner's standing decisions | Research question, comparator, information set, data eligibility, evaluation, adoption, freeze and live eligibility |
| [Publication Standard v1](track-b/publication-standard-v1.md), including §§14–17 | Incorporated baseline and historical PRES-1 contract, with amendments and trigger rules |
| [Presentation and tracking plan, revision 3](track-b/presentation-and-tracking-plan-2026-09-24.md) | Requirements that v1 carries forward and has not superseded |
| This document | Active publication entry point; approved amendments and applicability in §§15–16 |
| Publication brief | Exact task, candidate, authorized actions and additional acceptance; cannot relax the governing standard |
| [Runbook](track-b/publication-runbook.md) and [packet template](track-b/publication-packet-template.md) | Implementation touchpoints and packet structure; cannot change acceptance or grant authority |
| Reviews, landing records and [advisory log](track-b/publication-advisory-log.md) | Evidence and recommendations; a PASS or recommendation does not make a rule or grant publication authority |

This document is the publication entry point for its effective scope. The exact baseline requirements
in Publication Standard v1 and the surviving plan clauses are **incorporated by reference**, with
only the express amendments in §15 replacing their named clauses. The concise restatements
below do not silently repeal an omitted requirement. A conflict not resolved by §15 is reported
to the Owner before dependent work proceeds. Research authority and AGENTS.md always retain
their own scope; presentation rules do not alter either.

The preserved [PRES-1 conformance brief](track-b/evidence/pres-1/pres-1-conformance-brief-2026-09-28.md)
and [landing record](track-b/pres-1-landing-2026-09-29.md) explain that release. Their ceilings,
candidate identities and delegated publication authority do not authorize another release.
Do not reopen or rewrite those records to adopt this document.

### 1.2 Four identities that must not be conflated

1. **Publication-rule revision:** for example `PUBLISH_RULES 1.0`, with ratification date and SHA-256.
2. **Research generation:** `vN · <adopted change>`, assigned only upon adoption.
3. **Product status:** adopted in research, released, final candidate, live or retired, with dated evidence.
4. **Artifact identity:** reviewed candidate SHA, evidence SHA/tag, landing SHA, service revision and served hashes.

A new publication-rule revision is not a new model. A model adopted in research is not automatically
the model served by the demo. A landing SHA is not necessarily the reviewed candidate SHA.

Every future publication brief pins the effective rules and incorporated baseline hashes. A review
records those hashes before testing. Ratification records live in the programme's anchor/state
record; this document must not assert a self-referential hash. Preserve prior ratified revisions
by reachable Git references. No historical review is regraded under a newly proposed rule.

### 1.3 Applicability categories

- **Inherited:** already required by v1 or surviving plan clauses. Applies now under those sources.
- **Amendment A1–A7:** precisely listed in §15 and authorized in §16. A1–A6 apply from the next
  publication; A7 is conditional on Live. They cannot fail PRES-1 retrospectively.
- **Revision 1.1 / A8:** final-product identity, page order and daily-operation obligations apply
  when the Owner designates the final model and its transition is executed. A7's operational
  display applies as live operation starts; unavailable states apply before then. Existing
  research releases keep their effective contract. Research authority is `capstone_v21.md` §16.
- **Future trigger:** one-shot test, final candidate, daily updates or live operation. Applies when
  its prerequisite and governing protocol exist. Not a reason to invent data, retrain or start a service.
- **Historical example:** illustrates an observed case; never a permanent test constant or live status feed.

## 2. Purpose and reader contract

The primary readers are a Lead Data Scientist and an engineering manager evaluating the project
and its owner's judgement. They should understand what was built, what is usable, what improved,
against what, how the work was performed, what failed and what remains planned.

The reading path excludes closed disclosure bodies and exact-value tables. It includes the
report's default view and the README's generated top block. A fact buried in a disclosure does
not satisfy a rule requiring that fact on the reading path.

The inherited placements are measured with all disclosures closed, in Chrome and Playwright WebKit:

| Layer | Required answer | Existing placement |
|---|---|---|
| Headline | Forecast target; headline numbers; evidence class; demo model | Entire block visible without scrolling at 1440 × 900 and 390 × 844 |
| Orientation | Comparator, change and uncertainty, principal caveat | Finding sentence above comparison chart; fully visible within 1800 px desktop and 2532 px phone |
| Definitions | Terms first used in the headline | Directly beneath its block |
| Product identity | Why this demo runs this model | Beside demo action, outside disclosures |
| Contribution | Who did what | Byline route to the approved statement |
| Journey | Change, evidence, failed paths, decision, system and reproduction | Ordered chapters and supporting sections |
| Depth | Values, runs, source records, code and review | Labelled routes from the relevant result |

**A1 requires** naming each metric beside its headline number. **A2 requires** measuring the
comparison's screen allowance after subtracting persistent header space (§15). The raw pixel
limits above are retained as the historical v1 baseline; A2 governs future publication acceptance.

For the final-product page only, A8 changes which content occupies these early slots: the
product/forecast summary is the headline and its performance/uncertainty finding is the
orientation. A2's measured-header formula and two/three-screen limits still apply to that
product finding. The later **How the models compare** section is no longer required within
those screens; its comparison/fairness finding remains immediately above its chart. This is
an explicit conditional placement amendment, not a relaxation for current research releases.

Write plainly. Define a term at first use; do not add a glossary as a substitute. Put a caveat
where it qualifies a claim, once. Avoid internal codes, repair history and repeated assurances
that reviews happened. A decision and its evidence matter more than the volume of process text.

## 3. Evidence, numbers and claims

### 3.1 Evidence classes and status

| Class | Required distinction |
|---|---|
| Development | Historical, post-selection evidence. Can justify research adoption; cannot establish performance on unseen data, product qualification or live eligibility. |
| One-shot test | A pre-specified evaluation on an unused window. Use its protocol's badge, metric and exact dates. Preserve v1's label, “confirmatory-style, not power-qualified”. |
| Prospective live | Forecasts issued before the relevant outcome was available, scored afterwards. State the observed number of live days and the covered period. |

Do not combine classes as if they were interchangeable. Preserve withheld claims W1–W21 through
their controlling claim maps and plan references. In particular: no unqualified significance,
validation, economic-value or causal-feature claim follows from development comparisons.
An independent project review is not external scientific peer review.

### 3.2 Primary scores, comparisons and uncertainty

The research protocol chooses the scores and comparator before results. Currently the research
scores are point-error score (S_MAE) and interval score (S_WIS): error relative to the similar-day
naive within each period, averaged with equal period weight; lower is better. The naive normalizer,
the decision-rule benchmark and the comparator for a generation change may be different identities.
Name each role rather than treating every baseline as the same model.

Publish the following from typed, derived evidence records:

- The pre-specified verdict, its dated rule, distance from its comparator, and the eligible
  policy count at that decision. Label a point comparison when it has no confidence interval.
- Change in each primary score as a share of the named comparator's score, with its 95% interval.
  Preserve the historical interval convention for v2/v3; from CP-21, derive the interval of the
  ratio from that checkpoint's own bootstrap draws. Do not silently substitute methods.
- Absolute MAE in EUR/MWh across ordinary periods, with the protocol's stress period separate.
  This context does not replace the pre-specified ranking metric.

One comparison uses one eligible population and comparability ID. Show its dates, hours/days,
aggregation and evidence class. A changed population gets a separate comparison; do not join
incompatible results into an apparent improvement curve. On the existing overview, the visible
fairness note includes **10,747 hours over 448 days**, equal-fold scoring and development status.
Those counts are evidence values for this population, not constants for future populations.

Intervals of estimated differences and forecast intervals must have distinct labels. Coverage
is presented together with width. A null result does not demonstrate equivalence. A gain from
a bundle of features does not establish which feature caused it.

### 3.3 Counting models and experiments

Count identities under a declared rule and date, not table rows, run totals or aliases. State what
the count excludes. Controls, references, study arms, rejected branches and adopted generations
are distinct kinds. A policy with two experiment codes remains one policy.

Historical example: v2's `V2-H` and CP-20's `H0` are the same identity. The v3 target census is
A1–A5, V2-H, V2-P and HG: eight policies. The seven rows of the overview serve a different purpose.
Never infer a target census from the number of rows displayed or hard-code eight into a contract test.

### 3.4 Provenance and formatting

Research numbers originate in committed source rows pinned by hashes. The evidence layer derives
them; claim maps bind the interpretation; generators render them. No hand-typed research number
in a generator or generated output substitutes for this chain.

- Scores/differences: at most four significant figures on the reading path.
- Relative percentages: whole numbers; only the categories permitted by v1 §3/§4.
- EUR/MWh: one decimal place; one precision within a chart.
- Preserve sign and at least two significant figures for a near-zero value. Full precision in tables.
- Floor displayed p-values at 10⁻⁶, retaining exact values in the table.
- State metric, unit, aggregation, comparator and evidence class. One unit per axis.
- Structural numerals and the protected v1 statements retain their prescribed exceptions.

Evidence re-derivation, claim binding, precision, code/status lint and registry checks need meaningful
negative controls. Tests verify contracts, not “exactly N runs” or yesterday's content count.

## 4. Model identity, transitions and rejected experiments

One registry supplies canonical names, aliases, kinds, status history, comparator, population,
evidence class, rule, claim map and MLflow run keys. Names, ordering and state-dependent words
derive from it on every public surface. Do not hand-write “current”, “latest” or “the demo runs”.

The hero's inherited status priority is live, final candidate, released, then research. The research
headline and released-product identity remain explicitly separate. The demo serves the released
model according to the approved release rule; research adoption alone never changes it.

**A3 requires a transition summary for every newly adopted generation after the first:**

- predecessor and adoption date;
- question and actual change in data, features, model or interval policy;
- pre-specified comparator and whether it is also the predecessor;
- comparable measured result, uncertainty, evidence class and limitations;
- dated decision and a direct route to its comparison and evidence;
- a clear explanation when a predecessor comparison is unavailable or invalid.

The transition summary reuses the chapter's existing evidence. It is not a second leaderboard or
a requirement to repeat research. When the predecessor differs from the protocol comparator,
report both only if commensurate evidence exists. Otherwise disclose the gap and retain the
protocol comparator. Do not authorize a new research run through a presentation task.

Rejected experiments remain descriptive branch cards: question, comparator, deciding diagnostic
or difference with interval, “Not adopted”, reason, date and evidence. They attach to the correct
place in time, including after the latest generation. Failed or rejected work must not be omitted
merely because it weakens the story; planned work must not be invented to fill a branch group.

**Historical application, not new results:** the current “Experiments between v1 and v2” group
contains non-adopted branches. The v2→v3 weather experiment was adopted as v3 and already has a
paired comparison. Its appropriate transition summary is **“From v2 to v3: adding weather forecasts”**.
No additional rejected branch between these generations was established in the independent review.

Illustrative copy, to be generated from existing bound records when implemented:

> v3 added weather forecasts to v2. In development tests, the point-error score changed by −12%
> [95% interval −16%, −9%] and the interval score by −14% [−17%, −11%], each as a share of v2's
> score. The combined weather feature set was adopted in research. This comparison does not
> isolate the contribution of each weather feature or establish performance on new data.

This is a copy specification, not permission to paste constants into public output. The demo's
model line remains registry-derived and separate from this historical decision.

## 5. Page architecture and active-product documentation

**A4 replaces v1 §6's section order for future publications with:**

1. Compact navigation.
2. Product opening: what it does, actual available model/status, research headline, actions,
   release rule and labelled preview or eligible live panel.
3. **The product explained, immediately after the product opening:** the maintained documentation
   of the actual released/frozen product, covering the twelve subjects in §5.1. Show a concise
   orientation and descriptive routes here; expand details in this product section, not inside an
   old generation chapter. Shared explanations belong here alongside product-specific evidence.
4. Overview comparison and fairness note.
5. Lineage and generation chapters, newest first, with transition summaries and rejected branches.
6. Planned work, unscored and unnumbered.
7. Optional engineering/audit depth not already covered by the product documentation. Do not
   relocate essential data, method, forecast, limitations or reproduction explanations here.
8. Reproduction, contribution, terms and attribution.

**A8 overrides this order at the final-product transition:** compact navigation → one product
and daily-forecast opening → **How the product works** → **Product results** (scientific
results and graphics) → **Business insights** → **How the models compare** → the remaining
lineage, chapters, planned work, depth, reproduction, contribution, terms and attribution in
their existing relative order. No change is made to the comparison content or later sections.
The three product sections complement each other: method explanations link to the canonical
result graphics; business conclusions cite those results and their own evaluated use case,
without duplicating full charts or manuals. Descriptive routes remain visible by default.

At that transition, the latest Owner-designated final version, selected product, primary demo
and daily training/forecasting policy must share one version and policy identity. The opening
must not pair a newer research model with an older primary demo. Later experiments remain
research history until a separately authorized product replacement. Designation is recorded
immediately as selected; if rollout is incomplete, show that state and the currently runnable
identity honestly. Never relabel an old demo as the incoming model or claim the transition done.

The product documentation must fit the headline/orientation placement contract. Its concise
orientation and descriptive topic routes are visible immediately after the product panel; long
bodies may use named disclosures within that section. Moving the entire old report into the
opening is not the intended implementation. Moving the comparison before lineage is an explicit
amendment that preserves room for product context while keeping the result early.

The public heading identifies the product, for example **“How the product works”**, with the actual
model/version visible as provenance. It is not permanently named “About v1”. While v1 is the only
released product, its verified applicable evidence supplies that documentation. When a successor
is validly released/frozen, the documentation follows the new product. A research leader must never
be documented as the shipped product merely because its scores are better.

### 5.1 The twelve product subjects and their lifecycle

**One comprehensive current-product explanation; concise generation histories.** The Owner's
clarification is that the depth of the original report's subjects 1–12 belongs to the product,
not to v1 as a historical generation. It is not sufficient to move only model-independent prose:
features, validation, explanations, reliability and reproducibility must describe the actual
product too. Research chapters retain their required decision/evidence slots but do not each
acquire a duplicate full product manual.

The original report combines 6–7 under one explainability heading and includes a 3b spectral
subsection. The following is a coverage map, not a requirement to preserve its numbering or wording:

| Original subject | Required current-product explanation | Identity / caveat to preserve |
|---|---|---|
| 1 · The data | Target, sources, date range, cadence, units, preprocessing, availability and cutoffs | Actual product data contract and source rights; distinguish training, evaluation and operational inputs |
| 2 · Three regimes | Material price regimes, negative prices and why these affect evaluation or use | Periods and plots from eligible data; do not silently refresh research plots beyond the permitted boundary |
| 3 · Feature catalog | Inputs/features actually used, why they are eligible and what was excluded | Current frozen policy's feature set; historical selection experiments remain dated evidence |
| 3b · Spectral view | Explain seasonal-feature reasoning where relevant and supported | Not a mandate to rerun or reproduce a spectral analysis for every model; omit the technique if inapplicable and explain the design directly |
| 4 · Validation design | Forecast origin, temporal splits, leakage protection, baselines and evaluation windows | Actual governing protocol, with development, one-shot and live evidence separated |
| 5 · Results | Product's measured point/interval performance, uncertainty and meaningful comparison | Results for this product/artifact; historical research improvement is not substituted for a product test |
| 6 · Explainability: attribution | What the chosen explanation method says about the product's predictions | Model/output/population to which it applies; SHAP is an example, not a universal mandated method |
| 7 · Explainability: sensitivity/importance | What an appropriate robustness, importance or sensitivity analysis establishes | Distinguish attribution from incremental value or causality; no transplantation of v1 rankings |
| 8 · Regime-stratified error | Where the product succeeds or fails, with relevant groups, counts and uncertainty | Evidence-supported strata and thin-subset limitations; no invented evaluation |
| 9 · Reliability | Observed interval coverage and width, applicable calibration stages and limitations | Actual interval pipeline; v1's three stages are not imposed on a different method |
| 10 · Next-day forecast | Product output and how to read it; useful chart and actual controls | Explicit replay/inference/live identity; only eligible Live can show current issued forecasts as live |
| 11 · Honest limitations | Data assumptions, failure modes, generalization and operational limits | Limitations of the active product; retain adverse facts and evidence-class qualifications |
| 12 · Reproducibility | How to run/reproduce the product, artifact/policy identity and useful evidence routes | Current verified commands and service routes; do not reuse historical container instructions as current |

Every subject is accounted for as supported, not yet evaluated, or inapplicable with a specific
reason. This presentation obligation does not authorize missing research. A missing result is
shown honestly and routed to the research plan; any required product-qualification gate still
has to be met under that plan. Do not display an old model's graph under the new product heading
or assert “not applicable” solely because the evidence is inconvenient.

For a product replacement, its publication packet identifies the incoming and outgoing product,
rechecks these subjects against incoming evidence, updates model-specific graphs and instructions,
retains genuinely shared material after an applicability check, and preserves the outgoing evidence
as history. Publish the updated product identity and documentation together. A data-only update
under an authorized frozen policy updates its issuance/freshness/evaluation metadata; it does not
pretend to be a new model release or trigger a new full historical narrative every day.

The original “DE-LU day-ahead price forecasting” report is currently at the bottom because it is
the preserved v1 archive. Retain its protected text/behaviour and an explicitly historical route,
but do not make it the only route to understanding the current product. The active-product section
is maintained outside that archive. Its facts and graphs are selected and rewritten for the actual
product; merely renaming the archived report does not meet this requirement.

### 5.1a Final-product results and business interpretation (A8)

**Product results**, directly after How the product works, presents the selected product's
forecast-versus-observed charts, error over time and by material regimes, explanation/sensitivity
results, and interval coverage together with width. Each graphic names the policy/artifact,
population, dates, units and evidence class. Historical development, unused-data evaluation and
prospective issued forecasts are visibly separate. Use the §5.1 coverage map across these
adjacent sections; do not transplant another model's evidence or duplicate every topic.

**Business insights**, directly after Product results, explains the intended use, measured
benefit, losses and limits. Where a decision-policy evaluation exists, show cumulative net
profit/value over the full named period, against the declared benchmark, with units, costs,
constraints, initial conditions and risk/loss context. Label simulated/backtested results versus
realized operation; preserve failed and missing days and disclose capital/denominators for
returns. Forecast error reduction and interval coverage are not profit or trade-success rates.
Business success percentages name the decision, formula, denominator and evaluation window.
If this evaluation is not yet authorized or available, retain the section with the specific
gap and measured forecasting implications; do not manufacture a profit curve or imply gains.
Economic modelling stays governed by the research/use-case protocol (programme §4.E).

### 5.2 Chapter grammar

Preserve the inherited slots: question/change diagram; main paired-difference chart for both
primary scores with 95% intervals; one-sentence reading; at most three things not established;
dated decision; evidence row; named detail sections.

The detail menu remains method; per-period consistency including absolute errors; stress period;
coverage and width; protocol and review. The transition summary in §4 uses these slots, with links
to deeper results. v1's archive is not forced into the modern chapter grammar.

One scrolling history page remains the rule. The self-contained page budget remains 2.0 MB.
At v5, or before adding a chapter that would exceed it, propose compaction to the Owner. Moving
full chapters off the page requires amendment of the one-page decision.

## 6. Charts, discovery and navigation

Every primary chart carries a plain question/finding, metric, comparator, population, evidence
class, units, readable marks, reference line, finding, qualification and evidence route. Comparable
panels share scales; an additional labelled difference view may expose smaller effects. Do not
use smooth time-series imagery for discrete generation or fold comparisons.

No meaning depends on colour or hover alone. Use direct labels, shape/line style and readable
values. Distinguish a reference line from a target. Exact-value tables retain definitions and units.
Mobile variants reorganize the chart; they are not desktop SVGs shrunk beyond legibility.
Research chart text is at least 12 px at 390 px. Visual tokens remain the Owner's decision.

**A5 establishes a discovery contract:** every explanatory result chart offered on the report has a
descriptive route from its generation's visible summary, or from the active-product documentation where
appropriate. The link says what the reader will see. A route opens ancestor disclosures and lands
on a heading visible below the sticky header. A chart's existence, a hidden source link or a generic
“Details” control does not by itself demonstrate discoverability.

This does not require all charts open by default. A compact “Explore these results” list can link
to absolute errors, period consistency, stress-period behaviour, hourly errors and coverage/width.
Archive charts may use the clearly labelled archive route and its internal contents navigation.
Technical audit-only plots are labelled as such and need not all be promoted onto the main path.

The existing navigation remains compact: Results, Journey, Evidence, with generation navigation
secondary. No stacked sticky bars. Preserve deep links, descriptive link text and a return route
from the archive. External demo/tracking destinations are identified as external.

Check discovery by starting at the actual default page with disclosures closed. Record the labels
and actions taken to reach each advertised chart. A screenshot produced after opening every
disclosure proves rendering, not this route. Test the deep link directly and by keyboard as well.
This is separate from the six fixed cold-reader questions; do not coach that reader with locations.

## 7. Product, demo and future live operation

### 7.1 The existing product contract

The opening identifies exactly which model is runnable and why the research model differs.
The static report's historical replay is precomputed and offline; the Space's browser inference
is a different operation. Neither is described as a live forecast without prospective evidence.

Beside the demo action, outside a disclosure, show download size, measured cold-start time,
device/browser/date and last verification date. Measurements are tied to a release, not timeless
performance promises. The report must not embed or auto-launch the heavy runtime.

The demo has ready, loading, failure and retry states, with a route back to the instant report.
The first loading/fallback message exists before runtime initialization and remains useful when
initialization fails. Only real runtime stages appear; no invented progress percentage.
Every control, including framework widgets, has an accessible name and operable focus behaviour.

### 7.2 Future live presentation — conditional, not activation

The Owner's requested direction is a leading panel for today's forecast versus available actuals
and tomorrow's forecast with uncertainty, followed by the product documentation. It requires the
research/live protocol and the triggers in v1 §16 before implementation as a live product.

Revision 1.1 makes this a required outcome for the Owner-designated final product, not an
optional dashboard. The lifecycle and daily-training contract are in research anchor §16.
Freeze the policy and reproducible initialization, not all future weights. Daily retraining,
eligible input refresh and forecast issuance are mandatory for that selected product, subject
to its declared failure policy. Input/context refresh alone is not training; a model that
cannot meet daily training needs a documented Owner-approved exception before live admission.
No such exception is granted here to TabPFN, immutable v1 or any other model.

Distinguish:

- **Frozen fitted artifact:** weights and calibration are unchanged.
- **Frozen policy:** the algorithm, inputs, update rules and evaluation contract are fixed; fitting
  can update only if that frozen protocol permits it.
- **Daily inference/data refresh:** new forecasts from new eligible inputs; does not imply retraining.
- **Daily retraining:** an explicit update operation requiring its own eligibility, reproducibility
  and failure rules under the research protocol.

**A7 requires the following display contract when a live panel is authorized:**

| Field | Meaning and required qualification |
|---|---|
| Model and policy | Version, actual status and fitted-artifact/update identity |
| Time | Forecast issue time, information cutoff, delivery date and explicit timezone |
| Today's prices | Hourly values or an explicitly defined aggregate; distinguish forecast, published actual and not-yet-available outcome |
| Observed error | A defined metric, units, scoring window, sample count and which issued forecasts it scores |
| Tomorrow | Issued hourly forecast and prediction interval at the stated nominal level, or a clearly marked unavailable state |
| Reliability | Observed interval coverage together with width over the named past window; no promise that a nominal level is verified future confidence |
| Freshness | Last successful update and stale/missing/failed state; never silently present old forecasts as newly issued |

The panel also shows the last successful **training** time separately from data refresh and
forecast issuance, and identifies the daily artifact that produced each forecast. Today's
score uses the predictions actually issued for today's delivery hours, not predictions
recomputed by today's newer fit. Tomorrow's forecast is issued before its outcomes are known;
before the issuance cutoff or on failure, show a dated pending/unavailable state.

Show a **defined percentage performance measure alongside MAE in EUR/MWh**. Its formula,
denominator, eligible hours, scoring window, partial-day completeness and handling of zero and
negative prices must be fixed before evaluation. A possible contract is the percentage of
scored hours within a predeclared absolute-error tolerance; the numeric tolerance must be
justified and frozen by the protocol, not chosen after seeing results. A relative improvement
against a benchmark must be labelled as improvement, not percentage correct. No clipping or
silent exclusion may make a negative/undefined score look like high accuracy. If there are no
eligible outcomes, show not yet scored, not 0% or 100%.

Do not label performance merely “X% correct”. Hourly prices can be zero or negative, making common
percentage errors misleading. Use the protocol's MAE in EUR/MWh and, if authorized and properly
defined, its benchmark comparison. Do not equate a 95% forecast interval with a 95% probability that
the point price is correct. A confidence interval for a historical score is a different object.

The panel cannot determine when an outcome becomes scoreable: the protocol defines source,
publication time, revisions and eligibility. Pending outcomes remain unscored. Keep the `live_`
namespace boundary, final test protections and prospective publication timestamps.

Before Live, resolve update/publication authority, Friday and Shabbat scheduling, `delu-live`,
the runnable frozen-policy registry model, extended namespace tests, live claim builder and the
demo approach for daily weather inputs. No unattended publishing authority is granted by this anchor.

Daily means every delivery day, including 23/25-hour days. The future operating brief must
reconcile this with the Owner's no-manual-work Friday/Shabbat constraint through an explicitly
authorized unattended schedule and failure coverage; skipping those days silently is not daily
operation. This document creates no scheduler or standing unattended-publication permission.
The static report may be regenerated by that future authorized process; its no-runtime-network
rule remains in force. Demo and panel use the same policy and identify any different dated
artifacts; an older historical replay is labelled as such and is not the primary live demo.

## 8. Public surfaces and evidence links

The report, README, Space card, direct demo and MLflow must agree on identity, status, applicable
limitations and claims. A check of one surface does not certify the others.

- **README:** generated At a glance block, same research headline, product/report/evidence/MLflow
  routes, then generated generation list. Stable setup/licence text may be hand-written. v1's
  historical read belongs under its v1 heading. No hand-written current-state claims.
- **Space card and demo:** actual released model, matching limitations, correct actions and
  attribution. Check the served bundle, not only the local build directory.
- **MLflow:** repository is source of truth; registry-driven names, descriptions, tags and parents.
  Metrics, histories, parameters, provenance and artifacts mirror committed evidence. The verifier
  writes the public index. Preserve the historical `delu-cp2` experiment.
- **Report:** self-contained, no runtime network dependencies; no CDN, analytics or fetched fonts.
  New charts use inline SVG. Plain navigation links are allowed. Check browser-generated asset
  requests too: a source-level absence of `fetch()` is not evidence of zero public requests.
- **All relevant surfaces:** attribution/licensing, including GFS attribution; model-specific
  limitations. The approved contribution wording and public name change only by Owner decision.

Reader-grade links lead to page value tables or working MLflow run/comparison views. Audit-grade
links belong in the evidence row, labelled by type and freeze date. Frozen evidence with an older
status remains unchanged and is explicitly labelled as historical. Audit hashes, internal claim
IDs and checkpoint codes remain in depth, not the main reading path.

All advertised MLflow routes use the `.mlflow` host and pass anonymous read checks. Test both the
REST evidence and the rendered destination; a 200 response or a loaded application shell does
not establish that the intended runs or charts appear. Gated repository-UI URLs are controls,
not substitutes for public tracking routes. A local tracker is not proof about DagsHub.

## 9. Browser, accessibility and interaction acceptance

The following combines v1 §10/§11 with surviving plan §§7.5, 7.10–7.12 and §11:

| Check | Required evidence |
|---|---|
| Engines | Chrome and Playwright WebKit; record actual versions |
| Widths | 1440 × 900, 768, 390 × 844, 360 and 320 CSS px; record heights where not specified; emulated iPhone |
| Layout | Default page and relevant expanded content; charts at each width; no prose/primary-summary horizontal scrolling |
| Zoom/reflow | 200% zoom and 320 CSS px reflow; any emulation/substitute labelled accurately |
| Accessibility tree | Named charts and controls; disclosure expanded/collapsed state in both engines |
| Keyboard | Logical order, visible focus, operation of controls/disclosures and unobscured anchored targets |
| Touch | Targets about 44 px; inspect actual widgets, including framework controls |
| Contrast | Text 4.5:1, large text 3:1; relevant chart marks, controls, focus and state-carrying borders at least 3:1 |
| Chart meaning | Units, direction, reference/target, interval kind, labels, scales, table/text alternatives; no colour/hover-only meaning |
| Demo | Fresh anonymous cold start; meaningful control response; loading/failure/retry and return route |
| Requests and links | No failed requests; report's no-runtime-network rule; valid destinations and anchors |
| MLflow | Complete mirror verification and settled intended comparison charts/routes anonymously in both engines |

Record screenshots with URL, time, viewport, engine and disclosure state. Screenshots alone do
not establish accessibility conformance. Traverse embedded frames/shadow-root controls where
necessary; a tool that cannot inspect them leaves a gap, not a PASS.

Real Safari, a real iPhone and a screen reader are not mandatory under v1. Say whether they were
used. Playwright WebKit is not Safari and emulation is not a physical-device test.

## 10. Independent, fresh-reader and post-deployment review

### 10.1 Independence and reading order

The independent checker must not have authored the publication changes. Pin the candidate and
effective rules first. Review source evidence, rendered claims and reader experience rather than
accepting automated tests or earlier approvals as the verdict.

Check unchanged material by byte identity or identical output records; otherwise review it fully.
An exact-candidate PASS loses its coverage for subsequently changed content until a focused recheck.

Keep three outputs separate:

1. **Existing-rule violations:** exact effective clause, observation, reproducible evidence,
   impact, priority, concrete repair and acceptance check.
2. **Product recommendations:** useful improvements that are not current violations.
3. **Proposed rule amendments:** observed problem, inadequacy of existing rules, exact change,
   applicability, test and maintenance cost.

Only the first category can fail compliance. Do not invent a rule to justify a finding.

### 10.2 Fresh reader

A separate fresh agent receives only the rendered screens with disclosures closed and these
unchanged questions. It receives no repository, project history, prior review, expected answers,
chart locations or explanation from the author:

1. What is the headline result, with its numbers?
2. Against what?
3. How sure are we, and on what class of evidence?
4. What does the demo run, and why not the best model?
5. What was tried and dropped?
6. What would you ask the candidate?

Preserve its answers, supplied screenshots and screen order. The checker compares answers 1–5
against the registry/derived evidence and placement rules. Answer 6 is advisory. Do not have an
informed source reviewer answer as a fresh reader. A human cold read remains optional.

### 10.3 Public artifact identity and actual behaviour

**A6 makes the post-deployment check's evidence contract explicit.** For each surface,
record URL, UTC observation time, reported revision, fetched content identity, intended identity,
observed behaviour and limitations. Distinguish model code, candidate, landing and deployment SHAs.

Fetch public bytes separately from local files. Explain hosting injections before comparing hashes;
retain raw identity and any precisely defined normalized comparison. A byte match for HTML does
not certify all its assets. Report bundle-wide verification only when the full bundle was checked.

Use public browser sessions for actual-service claims. Record anonymous/authenticated context,
caches and cold/warm state. Read-only inspection is the default; no test run may upload, publish,
alter a tracking run or expose a secret without separate authority.

Distinguish product failure, service availability observation and test-environment limitation.
Retain first failures and targeted retries with times. A successful retry proves a later success;
it neither erases the failure nor proves uninterrupted availability. Local rendering can diagnose
a failure but cannot establish that the public service works.

Form the independent findings before comparing prior reviews and advisory dispositions. Then
identify repeated issues and claims of closure that the new evidence does not support. Append a
new review; never rewrite historical reviews to align them with the latest verdict.

### 10.4 Verdict

- **PASS:** all applicable required checks have sufficient evidence and no violation remains.
- **FAIL:** at least one applicable rule is violated; enumerate the violations and remaining gaps.
- **INCOMPLETE:** required evidence is missing and no established violation independently decides FAIL.

If a product FAIL and environmental gaps coexist, retain FAIL and list the incomplete checks.
Do not describe an untested requirement as PASS or a test-environment limitation as a demonstrated
product defect. Keep publication-readiness separate from research adoption and earlier checkpoint closure.

## 11. Publication packet and execution sequence

Each research checkpoint supplies its packet from inside the checkpoint, including:

- governing plan/brief/rules identities and applicable clauses;
- draft registry entries and dated status/adoption evidence;
- claim map, permitted and withheld claims;
- pre-specified verdict, rule/date, eligible N, ratio interval and per-period absolute context;
- draft chapter/branch slots and, under A3, predecessor-transition fields;
- deterministic MLflow export with provenance and expected routes;
- meaningful tests/negative controls and any unavailable comparison, with reason.

Under A4/A5, include the twelve-subject active-product coverage/applicability map, any
product-replacement documentation migration, and chart-route mapping in the same packet. Do not create a second hand-maintained catalogue if registry/slot data can generate it.

When A8 applies, include the Owner's exact final-version designation, outgoing/incoming demo
mapping, policy freeze and daily-artifact lineage, training/issuance schedule and exceptions,
percentage-score protocol, uncertainty records, business evidence/gaps and final-product page
order. The packet must distinguish selected, frozen, deployed, live and prospectively evaluated
states. Do not wait for the 90-day evaluation to display honestly labelled live observations;
do not award prospective qualification before that evaluation.

Follow v1 §12's order: build from packet → editorial review → fresh reader → independent check →
authorized MLflow upload and verification → final build → final-SHA focused recheck → authorized
landing/push/Space redeploy → public post-deployment checks. Roles and actual authority come from
AGENTS.md and the task, not from this sequence. The spent PRES-1 delegation is never reused.

No placeholder or non-final build reaches main. Only verified reader routes are advertised.
Pre-push guards fail closed; CI is a backstop. Never disable the secret guard or publish first
on the expectation of fixing the site afterwards.

The runbook owns exact commands and code symbols. Generated page, README blocks, Space cards,
exports and bundles are regenerated from their sources; never repaired by editing generated output.
Do not freeze implementation paths or host capabilities into new acceptance rules unnecessarily.

## 12. Full baseline coverage map

These tables are an index into binding text, not a replacement that drops unlisted subclauses.

| Publication Standard v1 | Covered here / disposition |
|---|---|
| §0 rationale | §§2, 10, 15; retained as historical rationale |
| §1 audience/placements | §2; A1/A2 amendments |
| §2 evidence classes | §§3.1, 4, 7; unchanged |
| §3 headline/comparator/quantities | §§2–4; A1 metric-label amendment; research comparator retained |
| §4 numbers/words/lint | §§2, 3.4; unchanged |
| §5 registry/release rule | §4; unchanged; transition summary is A3 |
| §6 architecture/chapter/branches/scale | §§4–6; A4 order and A5 discovery additions |
| §7 links/frozen evidence | §8; unchanged |
| §8 README/limitations/Space/MLflow | §8; unchanged |
| §9 completeness | §11; unchanged |
| §10 devices/accessibility | §9; unchanged requirements, explicit evidence limitations |
| §11 CI/release/reader/independent/blocking | §§9–10; A6 postdeploy specification; six reader questions unchanged |
| §12 packet/workflow | §11; A3–A5 packet additions for future publications |
| §13 governance | §§1, 14–16; no new power to edit or publish |
| §14 carryover | This section; all surviving requirements retained |
| §15 plan amendments | Incorporated exactly; A4 additionally changes section order |
| §16 triggers | §§7.2, 14; no early activation |
| §17 decisions | §§1, 14; preserve history and task-scoped limits |

| Plan invariant | Effective treatment |
|---|---|
| 1 zero runtime network | §8; includes browser-observed asset requests |
| 2 one v1 claim source | §§3.4, 8, 11; claims changes require payload rebuild |
| 3 generator, not output | §11 |
| 4 protected v1 honesty statements | Retained exactly through plan §6 invariant 4 and v1 §4; no archive rewrite |
| 5 limitations | v1 §8's per-model scope, not the superseded every-limitation-everywhere wording |
| 6 tracking host | §8, `.mlflow` |
| 7 live namespace | §7.2; research/live separation |
| 8 attribution/licensing | §8 |
| 9 v2 wording/near-zero endpoint | v1 §4 sign/precision amendment; exact endpoint remains in value table |
| 10 date boundary | Before final test, no v2+ research number/chart/choice uses data after 2026-04-07; v1 published replay exception preserved |
| 11 labels/no equivalence | §3.1/§3.2; plain labels on reading path, internal identifiers in depth |
| 12 language/Owner presentation | §§1, 8, 11 |
| 13 dependency files | `pyproject.toml` and `uv.lock` remain unchanged by presentation work unless separately authorized under governing rules |
| 14 retired tooling | §2; no public retired-governance narrative |
| 15 units/aggregation | §3.4/§6 |
| 16 no placeholder | §11 |
| 17 evidence-only numbers | §3.4 |
| 18 generated README research | §8 |
| 19 verified reader routes | §§8, 11 |
| 20 Owner review/public actions | §§1, 11; no inherited PRES-1 delegation |
| 21 no research budget | §4; no new experiment required to populate a presentation section |
| 22 no colour/hover-only meaning | §6 |
| 23 phone chart variants/text | §§6, 9 |
| 24 v1 archive | §5.1; preserve text/behaviour, styling only under approved scoped change |
| 25 demo states | §7.1 |
| 26 planned work | §§4–5; unscored, unnumbered, unavailable |

Surviving plan details also include analytical-panel grammar (§7.5), visible fairness population
(§7.9), anchors that open disclosures (§7.10), startup metadata beside the action (§7.11),
contrast/zoom/reflow (§7.12), claim/evidence-layer requirements (§9), MLflow verification (§10),
and Owner decisions (§16). Their exact text continues except where the existing v1 §15 amendments
or the §15 amendments below explicitly replace it.

The PRES-1 W1–W16 implementation acceptance is historical task acceptance, not an instruction to
repeat PRES-1 for each release. Reusable obligations are traced to the standard/plan, and future
briefs state their own task-specific acceptance.

## 13. Acceptance record for a future publication

One review record can carry this matrix; duplicate certificates are unnecessary:

| Area | Required record |
|---|---|
| Authority | Effective rules/hash; research anchor; brief; applicable clauses and justified N/A triggers |
| Identity | Local branch/SHA/tree state; final candidate; landing/service revisions; served hashes |
| Claims | Source rows/hashes, derivations, classes, comparator/population, count census, limitations |
| Reader | Default path/screens, placements, definitions, unchanged six-question fresh-agent record |
| Journey | Adopted transitions, rejected branches, plans; no implied unperformed experiment |
| Content | Twelve active-product subjects, applicability, product-replacement migration, concise research histories, protected archive and approved contribution |
| Charts | Rendering, semantics, mobile variants, values and discoverable routes under A5 |
| Product | Actual demo identity, startup metadata, cold start, controls, failure/retry, applicable limitations |
| Accessibility | Engine/width matrix, keyboard, AX controls, focus, targets, contrast, zoom/reflow, tool gaps |
| Tracking | Mirror, histories/artifacts, anonymous routes and settled charts; no substituted local proof |
| Release | Final build, guard/test results, exact-candidate independent check, authorized action record |
| Public check | Per-surface identity/behaviour, first failures/retries, limitations and verdict |
| Follow-up | Violations versus recommendations versus rule proposals; comparison with earlier findings |
| Final product (A8, conditional) | Owner designation; one product/demo/daily-policy identity; frozen update contract; daily fit/issuance lineage; ordered method/results/business/comparison sections; actual rollout status |
| Daily panel (A7/A8, conditional) | Today issued-versus-published prices; percentage and MAE derivations including zero/negative/missing outcomes; tomorrow intervals; coverage/width; separate training/issuance timestamps and stale/failure states |
| Business (A8, conditional) | Reproducible cumulative net value and benchmark when evaluated; explicit unevaluated state otherwise; costs, denominators, risk and simulation/realization labels |

Preserve screenshots and necessary machine-readable evidence with the review's declared scope.
Release evidence uses the normal committed evidence locations; task scratch stays in `.local/`.
For an expressly local-only review, identify retained local evidence honestly and do not claim
its machine-specific paths are publicly available. Do not overwrite a prior report to claim closure.

## 14. Maintenance and pending triggers

The Owner ratifies publication rules and decides their effective scope. The existing locked core
remains protected. Flexible copy/chart/tool/test maintenance remains limited by v1 §13 and the
broader Governance Lockdown; it cannot alter a locked document without the required suspension.
Only the Owner changes the public name, contribution statement and approved visual choices.

An amendment needs an observed problem, affected clause, proposed text, acceptance method and
maintenance cost. Consolidation is not a reason to add thresholds, new review cycles or more
research. Do not turn a subjective preference into an automatic release blocker.

After publication, review advisories and recurrence. Keep the governing revision if its rules
already cover the failure; fix implementation or test coverage. Amend only for a demonstrated gap.
No rule proposal retroactively changes a published artifact's verdict under its original contract.

Pending triggers inherited from v1:

- **v4:** Owner decides encoding for the new generation before publication.
- **v5 or size-budget breach:** Owner decides compaction; one-page rule remains until amended.
- **Before final-candidate test:** its badge, wording, fresh headline window and hero-switch rule.
- **Before Live:** the protocol and operational items in §7.2, including publication authority.
- **Landing templates:** the packet/MLflow incorporation is a separate governance task under its
  applicable suspension; this document does not execute the historical D6 proposal.

## 15. Amendments and their justification

**A1–A7 are incorporated under the authority in §16.** A1–A6 apply from the next publication.
A7 is a conditional Live requirement. The justification and maintenance cost remain here so that
future reviews can distinguish an intentional amendment from an accidental paraphrase.

Revision 1.1 strengthens A7 as specified in §7.2 and adds A8 below; the original A1–A7
authority and PRES-2's revision-1.0 acceptance remain historical and unchanged.

### A1 — Name each headline metric

**Observed need:** independent postdeploy review V2-01 and recurring advisory A-PRES1-9 found that
fresh readers could not associate 14% and 17% with their metrics on the first screen.

**Exact addition to v1 §3.4:** “Every headline result names its metric beside its value. A pair of
values must not require a later sentence, chart or disclosure to establish which metric is which.”

**Check:** default headline screenshot and fresh-reader answers map each number correctly.
**Maintenance:** two metric-labelled fields in the existing headline template; no second claim source.

### A2 — Measure usable screen depth

**Observed need:** review V2-02 measured PASS against raw page coordinates while the complete
orientation statement arrived on screenshot 3/4, beyond the intended two/three-screen experience.

**Replacement for v1 §1 orientation placement calculation:** “For a limit of N screens with
viewport height H and a persistent header of measured height h, the finding sentence's bottom
must be at or before N×H−(N−1)×h in document CSS pixels. If header height changes, use the largest
height observed on that route. Verify the statement is readable through N consecutive screen
captures advanced by the usable viewport height; anchored headings remain unobscured.”

N remains 2 at 1440×900 and 3 at 390×844; headline visibility remains unchanged.
**Check:** both engines, disclosure-closed default layout, measured header plus consecutive captures.
**Maintenance:** add header measurement to the placement check; no fixed historical header constant.

### A3 — Explain every adopted generation transition

**Observed need:** the Owner interpreted “Experiments between v1 and v2” as a potentially missing
v2→v3 comparison, although the adopted comparison already existed elsewhere.

**Addition to v1 §6:** “Every adopted generation after the first states its predecessor, question,
change, measured result, uncertainty, limitations and dated decision in a visible transition
summary. It names the protocol comparator separately where necessary. Link to a valid predecessor
comparison when available; otherwise state why it is not available or comparable. Do not invent
experiments, renumber rejected work or commission research through the publication requirement.”

**Check:** registry predecessor/date, source comparison, summary and route agree; absent comparisons
are explained. Adopted transitions and non-adopted branch groups are unambiguous.
**Maintenance:** reuse chapter fields and comparison records; add predecessor metadata only as needed.

### A4 — Current-product documentation directly below the product panel

**Observed need:** the Owner found useful data/explanation/graphs only in the old v1 report at
the bottom, then clarified that the depth of subjects 1–12 belongs to the frozen product rather
than to v1 specifically. An early generic introduction alone would not address this: method,
features, reliability, explanations and reproduction are partly product-specific.

**Replacement of v1 §6 section order:** use §5's eight-item order. “The maintained documentation
of the active released/frozen product sits immediately after its product opening, with a concise
visible orientation and descriptive routes to all applicable subjects in §5.1. Its detail lives
in that product section, independently of generation archives. When the released product changes,
update its documentation and evidence together. Research generations keep concise decision/evidence
chapters; a full product manual is required only for the actual product. Preserve historical v1
records without making them the primary product explanation. Keep existing headline/orientation
floors; put the overview before lineage and chapters.”

**Check:** default order/placements, descriptive routes and all twelve subject dispositions;
product identity matches each model-specific result, graphic and instruction; a replacement packet
accounts for retained/updated/archived content. Preserve the original v1 archive text/behaviour.
**Maintenance:** one active-product documentation section, with shared content reused where valid;
no duplicate full manual for each research model, no new experimental-method requirement.

### A5 — Make explanatory charts discoverable

**Observed need:** the Owner could not find graphs shown during review. The review opened disclosures
to inspect rendering; successful rendering did not prove an ordinary reader could find those graphs.

**Addition to v1 §6/§11:** “Each explanatory result chart has a descriptive route from its generation's
visible summary or active-product documentation. The route opens the needed disclosures and exposes an
unobscured heading. Verify routes from the closed default view, not only from direct URLs or an
all-expanded screenshot. Clearly labelled archive navigation may serve archived charts.”

**Check:** follow the visible route by mouse/touch and keyboard in both engines, including phone;
record the label, destination and resulting chart. Preserve the original cold-reader questions.
**Maintenance:** generate route labels/targets from chapter chart metadata; avoid a separate manual index.

### A6 — Specify public post-deployment evidence

**Observed need:** postdeploy F01/F02 exposed unnamed demo controls and a public favicon request that
report-only accessibility or local source checks had not settled. Earlier PASS records did not
prove current public behaviour. The existing postdeploy step lacked this explicit evidence contract.

**Addition to v1 §12 step 9:** “Verify the served identity and public behaviour of each advertised
surface, using fresh observations against the applicable browser/interaction requirements. Record
service revisions, raw/normalized hashes as applicable, first failures and retries, test limitations,
and the difference between product defects and missing evidence. Local output and prior approvals
cannot substitute for public checks. Compare previous findings only after forming independent findings.”

**Check:** §10.3 identity records plus applicable §9 matrix and §10.4 verdict.
**Maintenance:** reuse release checks against public URLs; retain existing probes and truthful scope.
This clarifies evidence coverage, not a demand for real Safari/iPhone or a new research evaluation.

### A7 — Define the future live panel honestly

**Observed need:** the Owner's requested “daily updated frozen model”, “percent correct” and “confidence
tomorrow” combine concepts that the existing deferred-live clause leaves undefined.

**Conditional addition to v1 §16's live-panel trigger:** “Before displaying a live forecast, define
policy/artifact update identity, issue and delivery times, information cutoff, freshness/failure state,
available actuals, scoring window, sample count and forecast-interval level. Distinguish daily inference
from retraining, frozen policy from fixed weights, and nominal interval level from observed coverage.
Use a defined metric in appropriate units; no unqualified percentage-correct or confidence claim.”

**Check:** an authorized future live specification fills §7.2's fields and traces scoring/update rules
to the research protocol; public acceptance waits for actual live implementation.
**Maintenance:** populate fields from existing issuance/scoring metadata when that system exists.
No new live service, automation, retraining schedule or model promotion is approved by this amendment.

**Revision 1.1 clarification:** the default daily-training requirement is now ratified in
research anchor §16; operational numeric schedules and execution authority remain future work.
The paragraph above records original A7's implementation boundary, not an option to omit the
new final-product requirement.

### A8 — One final product, daily operation and product-first results

**Observed need:** the current split between research v3 and demo v1 does not express the
Owner's intended final product. A4 did not place dedicated scientific results and business
interpretation before model comparisons; original A7 did not require daily retraining.

**Amendment:** at the Owner-designated final-product transition, §§5, 5.1a and 7.2 govern one
product/demo/daily-policy identity, the specified product-first page order, daily training,
defined percentage scores, and honest uncertainty/business claims. For this triggered layout,
§2 applies A2's early-placement bound to the product finding, not the later model comparison.
Only this explicit order/placement change supersedes A4 and v1's early research-comparison
position; comparison content, later sections and all other applicable acceptance remain.

**Check:** trace designation → registry/policy → daily artifacts → issued predictions → demo,
panel and documentation. Reproduce scores and any business series from source records;
check timing/no outcome leakage, missing/zero/negative prices, failed fit/issuance, stale data,
partial days and DST. Verify the default section order, product-first placement, descriptive
routes and served identity in the existing browser matrix. A future independent verdict binds
the implementation; writing this rule is not a PASS. Unperformed economics are disclosed, not
fabricated; unsupported daily training remains a blocker unless the Owner grants an exception.

**Maintenance:** one product identity and issuance/scoring record feed all surfaces; reuse
the existing subject and chart maps. Daily records and monitored operation have real storage,
runtime and operator costs, to be bounded in the future operational brief. This amendment adds
no model search, paid service, new economic experiment or current implementation.

## 16. Owner authority and integration record

### 16.0 Historical establishment of revision 1.0

The Owner first instructed: “תבנה עוגן ״PUBLISH_RULES״ בdocs ותעגן אותו יחד עם שאר העוגנים.
תבנה מסמך מקיף ומדויק שישמש אותנו לעתיד”. After the agent explained that registering a binding
anchor required a task-scoped Governance Lockdown suspension, the Owner replied:
“יש לך אישור מפורש לצורך כל המשימה לכל מה שאתה צריך”. Both instructions were given on 2026-09-29. During the same authorized task, the Owner clarified
that the original report's subjects 1–12 should document the frozen product, not v1 specifically,
and should not be relegated to the bottom. A4 and §5 incorporate that clarification.

This is recorded as explicit authority to establish and integrate this publication anchor,
including the directly necessary AGENTS.md and programme-state consistency edits. It is not
recorded as a separate line-by-line review, a publication instruction or a new research protocol.

| Item | Effective disposition |
|---|---|
| Publication anchor | `docs/PUBLISH_RULES.md`, revision 1.0 |
| Owner authorization | 2026-09-29, task-wide instruction quoted above, following the explicit Lockdown explanation |
| Amendments | A1–A6 for the next and subsequent publications; A7 at its Live trigger |
| Historical PRES-1 acceptance | Publication Standard v1, unchanged and preserved |
| Incorporated baseline | v1 and surviving plan requirements, at §17's pinned hashes |
| Anchor registration | AGENTS.md protected set and publication read route; `progress.md` Strategic Anchors and standing decisions |
| Integrity identity | SHA-256 recorded in `progress.md`; future briefs pin that hash and the incorporated baseline |
| Implementation/deployment | Neither performed nor opened by this document |
| Lockdown suspension | Task-scoped, spent at this task's terminal return; future edits require their own applicable authority |

AGENTS.md protects this anchor and the historical publication standard explicitly. No research
anchor, frozen evidence, prior review or deployed artifact is modified. No template or agent-role
rewrite is necessary merely to register this publication entry point. The runbook and packet
remain implementation references; when they lag a new requirement, the next brief carries that
requirement explicitly rather than treating the old template as a waiver.

All edits remain uncommitted for Owner review on main. This governance update does not close
any public-product findings and does not confer a compliance verdict on the unchanged website.

### 16.1 Revision 1.1 — final-product decision, 2026-09-29

The Owner specified that the final version, product, demo and daily-updated model must be the
same model; the page must show the product, How the product works, scientific product results,
business insights, then How the models compare and the remaining planned sections unchanged.
After the agent named the affected anchors and directly necessary consistency documents and
requested the task-scoped Lockdown suspension, the Owner replied: **“מאשר באופן מלא”**.

This authorizes this documentation amendment and its necessary consistency edits to
`capstone_v21.md`, the programme handoff, publication runbook/packet and `progress.md`, including
the research amendment record. It authorizes no model selection now, training run, external
action, commit, push, deployment or permanent governance exception. The suspension is spent at
this task's terminal return. AGENTS.md and historical baseline/brief/review/evidence bytes stay
unchanged. Research v21-r5 §16 supplies the operational policy obligation; this revision supplies
presentation and acceptance. Programme state records the new hashes without rewriting old briefs.

## 17. Source identities and change record

Prepared on `main` at `01e394d475202bb44a226f2ac5403aa084dc5b4c`. The existing untracked independent
review was preserved. These hashes identify the baseline read for this anchor, not future deployments:

| Source | SHA-256 |
|---|---|
| Publication Standard v1 | `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc` |
| Presentation/tracking plan revision 3 | `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c` |
| Preserved PRES-1 conformance brief | `51dd9b8685ea9feb774bd27a7d1241d7e678182dd93b1820cead686686d1f502` |
| Publication runbook | `462983758193e459642d0043870e256dda2429523b774601d5b32aa9f8630166` |
| Publication packet template | `2976a5f6d563bc7b9e4930da8f673a0a271d93e989d685898aabdb20cbd7a334` |
| Publication advisory log | `d1cb5309e43e3801bf1409016ddbd216279d92c2ed9ec9d48904439a9f59702f` |
| PRES-1 landing record | `410475d242b827ee7ae138617132575b12f97776472d1b57c9374ac28d725973` |
| Independent postdeploy review | `74d33d52b38aa96891d156c512c39d3cbcd7cc3484253d6fdae571b2796252cd` |

The [independent review](track-b/publication-postdeploy-independent-review-2026-09-29.md) contains
the observed violations, prior-review comparison, screenshots and limits. Its FAIL is against
v1, not this successor anchor. Its four implementation findings can be repaired under existing rules;
the rule changes here are not a prerequisite for repairing them.

**1.0, 2026-09-29:** consolidate authority and carried requirements; establish seven explicit
amendments; separate generation comparisons from rejected experiments; define the twelve-subject active-product documentation and
chart discovery; specify future-live semantics without activating live operation. The root governance
router and programme-state pointers register this anchor under the quoted authorization. The
baseline standard, historical evidence, implementation and public services remain unchanged.

**1.1, 2026-09-29:** Owner-approved final-product identity, daily-training default and display
contract, product results and business sections, and explicit conditional placement amendment.
Revision 1.0 is preserved at `evidence/pres-2:docs/PUBLISH_RULES.md`, SHA-256
`03f106060d9a646ce0c0c986d2f5fb6549929f2ed7270f0c8678fbfd2293b3a3`.
Only future final-product execution triggers A8; PRES-2 and its migration plan stay pinned to 1.0.
