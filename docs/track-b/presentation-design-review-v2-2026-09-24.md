# Design corrections for presentation plan revision 2

**2026-09-24 · Review and handoff proposal; not an implementation or release verdict.**

Reviewed: [presentation plan, revision 2](presentation-and-tracking-plan-2026-09-24.md), working-tree SHA-256 `d9d30a9b35ffec1f926325d0f8ea19c669a4cc89015ffabf782ae311181b8c9e`.

This supplements the [earlier technical and reader-experience review](presentation-review-and-corrections-2026-09-24.md). The existing site is the starting point: it has not implemented this future plan. Its missing v2/v3 presentation is therefore not an implementation failure.

## Recommendation

Revision 2 is substantially stronger: it specifies fair comparisons, distinguishes released software from research, preserves uncertainty, and connects claims to evidence. Keep that foundation. **Before implementing the full page, turn §7 into an actual design specification and strengthen D1 into a desktop-and-mobile design checkpoint.**

The remaining risk is a technically rigorous report that still feels like a long generated document. A list of cards, charts and badges does not determine visual quality. The plan needs decisions about emphasis, typography, spacing, chart grammar, states and how much the reader sees at once.

The proposed direction is **a product-led research case study with precise analytical components**: show a real product immediately, make the measured result easy to understand, then let the reader follow the decisions and inspect their evidence. Success should be visible without making the reader decipher internal checkpoint codes; serious work should be demonstrable without making the first screen an audit log.

## 1. What was inspected, and what this review can establish

For this revision, the plan and relevant renderer/verification specifications were read, and the requested reference websites were inspected in a desktop browser. Tremor's repository and package manifest were also inspected. The earlier review records the existing report, code, demo and test checks; those observations are attributed to that review, rather than represented as a new full execution of the tests.

| Reference | Observed design pattern | Application to this project |
|---|---|---|
| [Tremor KPI cards](https://blocks.tremor.so/blocks/kpi-cards) | Quiet borders, clear label–value hierarchy, concise context alongside a value. | A small number of evidence-backed result summaries, with the comparator and evidence class visible. |
| [Tremor chart compositions](https://blocks.tremor.so/blocks/chart-compositions) | Chart panels connect title, headline, legend and plot; surrounding whitespace helps distinguish their roles. | A consistent analytical panel whose title states the question and whose caption states the finding and limitation. |
| [shadcn dashboard](https://ui.shadcn.com/examples/dashboard) | Consistent cards, typography, controls, segmented selectors and table alignment. | Reuse that consistency for real controls and compact data tables. A research case study does not need the example's full application navigation. |
| [Dub](https://dub.co/) | A strong opening, restrained actions and an early product preview; later sections vary their visual rhythm. | Introduce the forecasting product and show its actual output before asking the reader to absorb the research history. |

These are observations and inspiration, not a proposal to reproduce the reference sites. The [Tremor source](https://github.com/tremorlabs/tremor-blocks) uses a React/Next.js application stack; the desired visual qualities can be implemented in the project's existing static HTML, CSS and inline SVG. No framework migration or new runtime dependency is needed for this proposal.

**Limits:** reference-site mobile layouts were not successfully verified at a changed viewport in this session. Mobile layouts below are proposed acceptance requirements, not claims about tested reference behavior. No revised local page exists yet, so visual quality, accessibility and performance of the future implementation remain unverified. No new scientific analysis was performed.

## 2. Prioritized changes to the plan

“P1” means resolve in the specification and D1 before rolling the design out to every generation. “P2” means specify now and verify during D2/E. These priorities concern the proposed design, not production incidents.

| ID | Priority / plan section | Correction | Acceptance evidence |
|---|---|---|---|
| D01 | P1 · §7.5 | Replace “the current light, report-like look is kept” with a deliberate visual system. Keep light surfaces, but define type, spacing, color roles, component hierarchy and chart styles. | D1 contains actual tokens and six representative component states, not just a wireframe. |
| D02 | P1 · §§7.1, 8.1 | Specify an actual v1 product preview and one primary action. Separate the released product from the latest research visually as well as in wording. | An unfamiliar reader correctly names the demo version and the research version from the opening. |
| D03 | P1 · §§7.1–7.3 | Reduce the explanatory prelude and remove duplicated headline comparisons. Give each section a distinct question to answer. | The first research chapter follows the overview comparison; full methods and architecture do not interrupt that route. |
| D04 | P1 · §§7.1, 7.2, 8.4 | Draw adopted generations as the main line and rejected experiments as actual branches. Do not turn every checkpoint into an equal milestone with a compulsory score. | CP-10 cannot be mistaken for an adopted successor; future work has no evaluated score. |
| D05 | P1 · §§7.2, 8.3 | Assign primary and secondary roles to charts. Replace the compulsory “three numbers” per chapter with the number the evidence justifies. | One main result is visually dominant; a critical counterexample or uncertainty remains visible without opening details. |
| D06 | P1 · §§7.5, 8.2–8.4 | Specify chart semantics: labels, units, direction of improvement, zero/reference lines, scales, intervals and readable mobile variants. | A reader can explain each main plot without learning policy codes or relying on hover. |
| D07 | P2 · §§7.4–7.6 | Separate generation identity, evidence class and adoption status; define accessible type and contrast. | Color removal does not remove meaning; long badges and exact scientific values remain readable. |
| D08 | P2 · §§7.3, 7.6, 11.3 | Specify one navigation hierarchy, responsive composition, disclosure behavior and a route back from the full v1 archive. | Desktop and phone reader routes work with keyboard and touch, including at seven generations. |
| D09 | P1 · §7.7, Phase 0/D2 | Make loading, failure and recovery states mandatory for the demo, independent of whether the earlier failure is reproduced. | A cold start never looks like an unexplained blank page; no fake progress percentage is shown. |
| D10 | P1 · D1, §11.4 | Review a finished visual specimen before extending the template. Add explicit reader tasks and screenshots. | Owner approves an actual desktop/mobile composition; later checks record both comprehension and visual defects. |

## 3. Proposed page composition

The opening should answer “what did you build?” The comparison answers “what improved?” The chapters answer “how did you get there, and why should I trust it?”

```text
Compact header: project name                         Results · Journey · Evidence

PRODUCT OPENING
Plain-language problem and purpose
Released demo: v1                 Latest research: v3 · Development · post-selection
One primary action + two quieter routes
Real, clearly labeled product preview

THE PROGRESSION
v1 ─────────────── v2 ─────────────── v3
 └─ calibration experiment            Weather-feature bundle
    not adopted
          model comparison study → informed v2
Planned work — separate, unscored

WHAT IMPROVED
One overview comparison + short fairness explanation
Readable values/table alternative + route to definitions

HOW IT IMPROVED — newest first
v3: feature change → result → limitation → decision → evidence
v2: design change + the useful and rejected paths that led to it
v1: original product + failure lessons + preserved full report

HOW THE SYSTEM WORKS / REPRODUCE / CONTRIBUTION / ATTRIBUTION
```

This is information order, not a requirement to fit everything above the fold. On a phone the product image can follow the title and actions; it should not be pushed below a full methodology section. The system diagram can have a short “How it works” anchor near the opening and a larger treatment later. Metric definitions should be available where used, without requiring a separate preliminary lesson.

### Opening and product preview

- Use a real v1 interface or historical forecast output. Label a screenshot as a preview; label the existing precomputed fan chart as a historical replay. Do not depict v3 as the running demo.
- Preserve the three useful routes in the plan, but choose one primary filled button, recommended **Try the v1 demo**. Use quieter links for **Compare research results** and **View code and evidence**. Place the download/startup information beside the demo action, not in its main label.
- The static page should show a useful preview immediately. Do not auto-launch or embed the heavy inference environment just to make the opening look interactive.
- Give status a compact two-part treatment: released product and latest research. Planned work belongs below the lineage rather than as a third equally prominent success card.
- Do not repeat the full scoreboard in the hero. If a summary value is used there, it must carry its comparator and development label and come from the same evidence record. Saved score differences are preferable to introducing a new promotional percentage.
- Suggested title direction: **“Forecasting tomorrow's electricity prices.”** A possible supporting sentence is: **“Explore the released demo and follow how successive research models were compared and improved.”** These are copy proposals; precise product wording still goes through the claim review.

### The portfolio needs a clear contribution statement

Change §7.1's optional “About this project” into a required, Owner-approved section for the portfolio release. State the Owner's actual role, the major decisions owned, and how tooling and independent checks supported the work. Do not invent sole authorship or hide assistance. One compact paragraph is enough. A hiring reader must be able to distinguish the project's accomplishments from the contributor's responsibilities.

## 4. Visual system to add to §7.5

The following values are a proposed starting specification, not values extracted from Tremor or an accessibility certification. D1 may refine them as a coherent set.

| Role | Proposed rule |
|---|---|
| Canvas and surfaces | Canvas `#FAFAFA`, analytical surfaces white, borders `#E4E4E7`. Let narrative paragraphs sit directly on the page. |
| Text | Main `#18181B`; secondary `#52525B`. Important caveats use readable text, not faint gray microcopy. |
| Actions | Dark primary button; underlined links with a distinct focus treatment. A link accent such as `#1D4ED8` is independent of version colors. |
| Generation identity | v1 slate `#475569`, v2 violet `#6D28D9`, v3 teal `#0F766E`. Repeat version labels and use markers or line styles as needed. Color does not mean “passed.” |
| Typography | System sans-serif stack, no remote font dependency. Body approximately 16 px / 26 px. Prose width 60–68 characters. Tabular numerals for data; monospace for IDs and commands. |
| Heading scale | Opening 48–56 px desktop, 32–36 px phone; chapter headings 28–32 / 24–28 px. Avoid an oversized marketing headline that displaces the product. |
| Data type | Headline values 28–32 px, explanatory labels around 14 px, ordinary tables 13–14 px. Chart text never below the plan's rendered 12 px minimum. |
| Spacing | Use a small scale: 4, 8, 12, 16, 24, 32, 48, 64, 96 px. Larger spaces separate chapters; smaller spaces group claim, caveat and source. |
| Layout | Content approximately 1,200 px maximum; readable prose stays narrower. Desktop rail approximately 140–160 px only when enough width remains for the content. |
| Containers | Approximately 10–12 px radius, 1 px border, restrained shadow only where useful. Avoid nested bordered cards around every paragraph and every fact. |

The page should alternate compact overview, spacious analytical figure, brief narrative and optional detail. Uniform cards everywhere would flatten the distinction between a key finding, an implementation note and an artifact link.

**Replacement direction for §7.5's style bullet:**

> Use a light, product-led case-study design with a defined type and spacing scale, restrained surfaces, and analytical components inspired by Tremor and shadcn. The opening introduces the real product; chapter layouts establish a clear hierarchy between result, explanation, limitation and evidence. Reuse the existing static renderer. Review the visual system on desktop and mobile in D1 before applying it to all generations.

Do not add theme switching, animated counters, scroll effects or a component-library migration to this scope. They would consume effort without addressing the current reader tasks.

## 5. Chart and table grammar

### One consistent analytical panel

Each primary figure should contain, in order:

1. A plain-language question or finding as its title.
2. Metric, comparator, population and evidence class in a short subtitle/caption.
3. A legend close to the plot, direct labels where practical, and explicit units.
4. The actual chart, with the relevant zero/reference line.
5. One finding and one qualification, followed by links to source rows and the corresponding tracking view.

Controls are present only when they change a real view. Do not borrow a dashboard date picker when the evaluation window is fixed, or draw tabs that are only decoration. No essential value, caveat or source should require hover.

### Overview comparison

Use two aligned horizontal dot plots or an equivalently clear two-panel design: **point forecast error** and **interval quality**. State “lower is better” and explain normalization to the similar-day reference. Keep the metric symbols available, but do not make `S_MAE`, `S_WIS`, `HG` and `H0` the reader's first vocabulary.

Use one consistent row order across the two panels and table. Highlight v1/v2/v3 through labels and weight; references remain fully readable. B0 = 1.00 is a reference, not a target to optimize visually. Diagnostic limits must say what they are and must not look like production certification.

The seven-row table needs no pagination, search field, selection checkboxes or management toolbar. Align numbers, put units in headers, and preserve the full comparison. Use **v3 · weather features** with `HG` as secondary metadata rather than an unexplained `HG` heading. Do not use seven unrelated colors for seven rows.

### v3 chapter hierarchy

The chart inventory in §8.3 is useful, but should not create seven competing headline figures:

| Visible by default | Secondary depth |
|---|---|
| Short feature-delta diagram; C2a as the main result; the development label; the bundle-attribution limitation; a visible note that fold 3's MAE interval crosses zero; adoption reasoning. | Detailed recipe/geography (C1), per-fold intervals (C2b), absolute fold scores (C3), crisis diagnostics (C4), hourly diagnostics (C5), coverage/width (C6). |

At least one compact helps/hurts finding remains visible. Put the complete diagnostic plots in clearly named native disclosures such as “Consistency across folds” and “Coverage and interval width.” This deliberately revises §7.2's requirement to keep every diagnostic dimension expanded. Opening a disclosure reveals a properly sized chart, not a miniature chart shrunk to fit its card.

### Scientific meaning must survive visual polish

- Keep C2a's normalized scores separate from C2b's EUR/MWh differences. Negative differences favor v3; label this directly. Show zero and the full interval extent. Never crop away fold 3's crossing.
- For absolute fold comparisons, use matching scales across directly comparable panels. If v1's crisis errors obscure v2/v3, add a clearly labeled paired-difference view rather than silently assigning each model its own scale.
- Folds and model generations are discrete comparisons. Do not turn their scores into a smooth time series or a decorative improvement sparkline.
- Coverage and width belong together. Increased coverage alone is not automatically better when intervals widen. Keep fraction/percentage conventions explicit and consistent with the evidence layer.
- In v2, preserve the full required near-zero upper endpoint in visible text. Do not turn it into `0.00`, an ellipsis, or a tooltip-only value. Let it wrap without breaking the page.
- A confidence interval for an estimated improvement is not the same object as a forecast interval. Legends and explanatory text must distinguish them.
- The alternative data table must carry the same values, definitions and precision rules as the chart, rather than only a simplified summary.

## 6. A repeatable chapter that tells a decision story

Use this content sequence for each generation: **problem → hypothesis → change → measured result → limitation → decision → evidence**. The initial summary can be short; the deeper layer provides the complete detail.

Replace the fixed three-number header with **one or two primary outcomes, plus context where necessary**. A mandatory third metric invites padding or misleading comparisons between unlike evidence. Counts of hours, runs or files are context, not success KPIs.

Show adopted/not-adopted as text separate from the evidence badge. Keep the exact v1 badge, “Confirmatory-style, not power-qualified,” and allow it to wrap. The development badge should remain adjacent to the research result, not buried in a global legend. Do not use a green checkmark to imply that “adopted for research” means deployed or independently validated outside this project.

Make at least one failed or rejected path concrete: what was tried, what result was insufficient, and which later decision it informed. The CP-10 branch and the road to v2 provide material already in the plan. Process credibility comes from this causal explanation, not from showing a wall of review filenames.

Future work uses an unscored “Planned / not evaluated” block. Each item can state the question it will test and what evidence would inform a decision, subject to the active plan. It must not imply a measured gain or a delivery commitment that has not been authorized.

For v1, retain its evidence, controls, caveats and stable anchors. Place the full original report in a clearly identified archive disclosure with a route back to the overview. The current wording “follows unchanged” should distinguish preserved content/behavior from any permitted surrounding CSS: do not silently restyle protected content, but also do not accidentally inherit conflicting global styles.

## 7. Evidence and tools as part of the reading experience

Use a small evidence row beside the result: **Compare these runs in MLflow · Reviewed result · Source data**. Keep full hashes, internal claim IDs and repair identifiers in deeper metadata. In a local prototype, mark unpublished destinations as unavailable rather than rendering a dead link that appears complete.

The architecture diagram should show the actual data flow and the leakage/availability boundary. Distinguish implemented and planned components with text and line treatment. A collection of cloud logos is not a substitute for a system explanation.

Keep the fairness note close to the scoreboard, but split it into a short visible explanation and expandable protocol details. The visible portion must retain the common population, equal-fold comparison and development status; the seed and block-bootstrap settings can sit one level deeper.

This provides the professional-tool impression the Owner wants through useful, verifiable interaction. Do not add a tool to the stack merely to display its logo. Do not show test totals, run counts or verification dates as current unless the release record supports them.

## 8. Responsive behavior, navigation and states

### Layout and navigation

- Use one compact main navigation. The desktop generation rail is subordinate to it; on phones it becomes a compact generation jump control or simple anchor row. Avoid multiple stacked sticky bars.
- Stack paired chart panels on phones. Shorten labels responsibly or move legends below; do not shrink the entire desktop SVG until its text is illegible.
- Keep primary summaries readable without sideways scrolling. Wide source tables may scroll within their own labeled wrapper. Numerical cells still need special handling for exceptionally long exact values.
- A sticky header must not cover anchored headings or keyboard focus. If a link targets content inside a closed disclosure, ensure the destination becomes reachable and understandable in the supported browsers.
- A CSS-only rail may be a stable jump list. Do not promise automatic “current section” tracking unless that behavior is actually implemented; `:target` alone tracks an anchor target, not ordinary scrolling.
- At seven generations, the rail and chapter summaries must remain usable. The scale specimen uses local placeholders only and must never present imagined future results publicly.

### Accessibility acceptance

Check normal text at a minimum contrast of 4.5:1 and large text at 3:1, following [WCAG contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Check chart marks, controls, borders that convey state and focus indicators separately; a passing body-text palette does not establish their accessibility.

Record report screenshots at desktop width (for example 1,440 px), 768 px, 390 px and 360 px; also check 200% zoom and reflow at 320 CSS px, allowing local scrolling for genuinely two-dimensional tables. The latter requirement follows the distinction in [WCAG reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html). Test keyboard order, disclosure announcements, descriptive links and a text/table route through each main figure. Use approximately 44 px touch targets as the project's usability target. Do not declare WCAG conformance from screenshots alone.

### Demo and failure states

Reconcile §7.7 with Phase 0: the phase table already says loading/fallback improvements proceed even when failures cannot be reproduced, but §7.7 makes them conditional. **Make them unconditional.** A slow successful cold start also needs an explanation.

Specify ready, loading, failure and retry states, plus an obvious return to the instant report. The initial loading/fallback message must be visible before the heavy runtime has initialized, including when initialization fails. Use instrumented stages where available; do not invent a percentage or show a timer as a progress estimate. Publish measured startup information with its device/browser/date context rather than promising a universal duration.

The static report itself does not need artificial loading skeletons. It should remain useful offline, with external demo and tracking links clearly identified. Planned experiments should be plain text, not disabled buttons suggesting an available feature.

## 9. Replace D1 with a reviewable visual specimen

Before extending the template to all generations, D1 should deliver a locally rendered page with:

1. The opening, real v1 product preview, status distinction and actual CTA hierarchy.
2. The branching lineage and complete seven-policy overview comparison.
3. A full v3 chapter, including the critical caveats and an expanded secondary diagnostic.
4. The longest evidence badge, long metric endpoint, source-link row, table and disclosure states.
5. Desktop and phone layouts using the same real content; a local seven-generation navigation stress case.
6. A demo-state specimen covering loading/failure/retry, even if the runtime fix is delivered in D2.

Deliver the token choices and screenshots alongside the page. Review layout, hierarchy and scientific meaning together; a beautiful fake-data mockup cannot establish whether real labels, intervals and qualifications fit.

Extend §11.4 with recorded tasks. Ask readers, without coaching, to locate the product, name the released and research versions, explain the main improvement, find a rejected idea, name a remaining uncertainty, and open the evidence supporting one claim. A useful design target is orientation within roughly 30 seconds and the full route within a few minutes; record actual results rather than claiming this has already been achieved. An agent can check facts and routes; human judgment is still needed for visual quality and natural reading.

**D1 is ready to extend when:** the Owner approves both desktop and mobile composition; the result/limitation/evidence hierarchy is clear; no important scientific meaning depends on color or hover; real content fits; and the reader tasks reveal no confusion between research progress and the released product.

## 10. Small specification clarifications before handoff

- **§9.3:** define separate valid markup contracts for HTML values and SVG labels. Use `<data>` for HTML text and suitable `data-claim`/`data-record` attributes on SVG elements; do not require an HTML `<data>` node around every SVG number. Axis ticks derived from a typed scale should be validated as such.
- **§9.5:** distinguish scientific claims from structural numerals. Version labels, dates, axes and controls need an explicit rendering policy; a broad “no bare numerals” check should not be the sole proof of evidence provenance.
- **§13:** design approval must not be treated as permission for publication or commits to `main`. The standing repository rules reserve those actions to the Owner. Historical task-specific delegation is not standing authorization for this task. State the performer and authority separately for any eventual public step; this review changes neither.

These clarifications do not authorize changes to locked documents or to the scientific plan. All new copy and derived displays still go through the existing claim-map and release gates.

## Handoff outcome

Accept revision 2's evidence architecture as the basis for the presentation work, subject to its own technical verification. Incorporate D01–D10 into the next plan revision, then produce the D1 specimen before broad implementation. Preserve the existing invariants, source evidence, exact uncertainty wording and zero-fetch/static-output constraints.

This review created only this new corrections document. It did not edit the plan, site, application, governance or program state; it did not commit, publish, upload tracking data or run new model experiments.
