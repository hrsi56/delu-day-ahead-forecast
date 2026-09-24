# Flagship portfolio presentation — verified review and correction handoff

**Date:** 2026-09-24. **Reviewed checkout:** `955510b5111af20348e09387fa4bf4db1948b769`, branch `main`, initially clean.

**Purpose:** give the Owner and the next executor a concrete correction package for [the presentation and tracking plan](presentation-and-tracking-plan-2026-09-24.md). This is a presentation/code review, not an Integration verdict, a scientific re-evaluation, or authorization to implement or publish. R1–R6 remain accepted; the recommendations below clarify their execution. No existing plan, anchor, source, generated page, registry or program-state file was changed by this review.

**Owner clarification during this review:** the site has not been updated to implement the plan; the plan describes a future update of the existing site. Accordingly, missing v2/v3 chapters and the old CP-15 card are baseline observations, **not defects in an allegedly completed implementation**. Read the findings as changes/clarifications to the future execution package. There is no request here to patch the old presentation separately before building the new one.

| Already in the approved plan — retain | Add or make explicit in the execution plan |
|---|---|
| Replace stale update; publish v2/v3 chapters; preserve v1 evidence | Cover old wording/anchors throughout the page; actually extend the README generator's ownership |
| Shared research data layer and claim maps | Typed units, comparator/population identity, public-claim interfaces and negative controls |
| Responsive single page, inline SVG and expandable details | Fix measured document overflow; test chart readability and real browser startup |
| MLflow backfill, capability probe, mirror check and saved link index | Retry/resume, durable exports, complete metric histories, actual reader-route verification and publication ordering |
| Hypothesis/results/proof/cost per generation | A visible product-to-progress journey, explicit feature deltas and nearby tool links |

## 1. The intended reader experience

The Owner wants a flagship portfolio project that visibly presents the product and its achievements, the development journey, the features added over time, the comparisons that justified decisions, and the professional tools through which a reader can inspect the evidence.

Build the page around this sequence:

**Working product and current status → comparable progress → what changed → how it was tested → what happened → why it was adopted or rejected → inspect/reproduce the evidence.**

Keep one scrolling page and the approved newest-first chapters. Do not hide the development journey in an appendix. Keep each chapter's conclusion, feature change, main comparison and limitation visible; put exhaustive tables, protocol details and review mechanics in expandable sections.

The current system has substantial material worth showing: the functioning static forecast interaction, a browser-model equivalence gate, published historical holdout evidence, research comparisons and paired uncertainty, saved causal controls, independent Integration reviews, versioned artifacts, and a real public MLflow service. The principal gap is connecting these into a coherent reader journey while fixing the defects below.

## 2. What was actually verified

### Live surfaces

- Opened the [public report](https://hrsi56.github.io/delu-day-ahead-forecast/) in the Codex in-app browser; inspected the rendered content and desktop screenshots; tested the interval selector and scenario slider; inspected the page at a 390 × 844 viewport.
- Retrieved the public HTML without authentication and compared its bytes with `docs/index.html`: **identical**, 1,014,592 bytes, SHA256 `3b37d7c29a965746d7fd200bd87f07fa8869b98c18a47faec11ba0c008e2d5b2`.
- Opened [MLflow](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow/#/experiments): the visible experiment list contained `delu-cp2` only, with previous/next pagination disabled. Opened the registered source run `83e475627b6646c885c70f9010c8cf2e`; its page exposed the historical holdout metrics, including MAE `25.907780440955044`. No login was requested. The UI displayed server version **3.5.1**; this is distinct from the plan's local client version.
- Opened the [direct browser app](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/) and the [Hugging Face wrapper](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast). The direct app remained blank during observation. The wrapper eventually displayed a CSS preload error, also after one “Try again” action. Details and limits appear in F01.
- Ran unauthenticated HTTP probes against the 12 distinct URL strings extracted by the existing link-checker's rules from its four local surfaces. **11 public URLs returned 200**. The remaining URL was the documented local development server, `http://127.0.0.1:8820`, which was not running. This is not a broken public destination. HTTP success does not verify fragment routes, app startup or inference.

### Repository and checks

Reviewed the page generator and its CSS/JavaScript, README regeneration boundaries, the claim/surface modules, static dependency scanner, link checker, tracking helper, WASM app source, relevant CI/Make targets, tests 17/19–24, research content and claim maps, saved CP-15/16/20 summaries, and applicable plan/state passages.

- Ran tests **17, 19, 20, 21, 22, 23 and 24: 117 passed in 6.21 s** under the existing Python **3.13.15** environment. The first invocation had 116 passes and one launcher failure because `marimo` was missing from `PATH`; adding the existing virtualenv's `bin` directory resolved it. This was an audit invocation error, not a product defect. Credentials were removed from the test subprocess environment.
- Ran `scripts/verify_release.py`: **PASS**, no bound-claim disagreements, no external fetching references found by the static scanner, no forbidden DagsHub links.
- Matched all seven proposed scoreboard rows against `reports/weather-ablation/metrics.csv` at the proposed four-decimal precision. Checked the saved HG−H0 equal-fold intervals and the fold-3 MAE interval; inspected the four proposed crisis rows against their saved sources.
- Compared the CP-20 H0 and CP-16 V2-H summary records for available `S_MAE`, `S_WIS`, `MAE`, `WIS`, `coverage95` and `n_hours`: pooled, five per-fold and equal-fold rows agreed to absolute tolerance `1e-12`. This checks summary continuity, not independent replay identity.
- Confirmed that the plan's 40.1 machine-hours is supported by the terminal Integration record; the earlier `resources.json` has 39.946 hours. Use the final record for final totals.
- Reproduced the link-checker's false-success behavior with a mocked 404 and a local fixture: an unresolved link was recorded, but `main()` returned **0**. No remote mutation was involved.

### Explicit limits

This was not a clean Python 3.12/Linux CI-equivalent run, a complete repository line-by-line audit, or a new independent validation of the forecasting science. No model fitting, CP-16/20 scoring pass, fresh-data evaluation, weather retrieval, container rebuild, remote write or publication was performed. Do not consume exhausted research pass budgets to implement presentation changes. Browser checks used one engine; the external demo failure still needs cross-browser diagnosis. No MLflow backfill/capability mutation probe was authorized or attempted. Data licensing text was inspected as project evidence, not re-adjudicated.

Local audit commands, logs and machine-readable results are retained in `.local/artifacts/presentation-review-2026-09-24/`. The findings and essential measurements are recorded here so that the handoff does not depend on those ignored files.

## 3. Corrections required before the new public presentation

Priority definitions: **P1** affects the usable product, correctness of a public claim, or a claimed release gate; **P2** affects clarity, maintainability or the agreed reader experience. “Verified defect” describes current behavior. “Plan gap” describes a missing or ambiguous requirement, not a feature that was supposed to have been implemented already.

### F01 — P1 — External demo failed to start in the review browser

**Status:** observed runtime failure; root cause unresolved.

The report's static chart works. The separate Hugging Face app did not reach a usable forecast in this review. The wrapper displayed:

`Unable to preload CSS for https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/assets/layout-D-WxHzKd.css`

The same error remained after retry. A separate unauthenticated request for that exact CSS returned 200, `text/css`, 2,816 bytes. The observed entry JavaScript also returned 200. This rules out treating the observation as an established missing-file/404 problem; browser loading, delivery, policy and transient causes remain possible. A platform “Running” badge did not establish app readiness.

**Change:** make real browser startup and successful inference an explicit acceptance gate. Diagnose the deployed asset chain and reproduce on an ordinary browser before changing code. Provide a visible loading state, intelligible failure/retry state and a link back to the self-contained report. Do not advertise the external demo as freshly verified until it has completed startup and a control-driven forecast.

**Acceptance:** cold startup, visible forecast, interval change and scenario change succeed on a desktop browser and a mobile viewport; record browser, date, app revision and result. If it fails, preserve the actual failure and fallback. Do not substitute HTTP 200 or old equivalence/load records for this check.

**Relevant source:** [WASM app](../../app/wasm_showcase.py), [Static Space assembly](../../scripts/build_wasm_space.py), [static-space tests](../../tests/test_23_static_space.py).

### F02 — P1 — Mobile page has document-level horizontal overflow

**Status:** verified rendering defect.

At a 390 px viewport, `document.documentElement.clientWidth` was **390** and `scrollWidth` was **1,750**. The reproduction surfaces table measured approximately **1,720 px** wide. Some other wide tables are correctly contained in `.scroll`; the two `.surfaces-table` tables are not wrapped that way. Global table cells use `white-space: nowrap`; long hashes and the two-column `.kv` grid also need narrow-screen handling. The fan chart itself shrinks to fit, leaving very small axis text on mobile.

**Change:** contain intentional table scrolling, allow prose/URLs and hashes to wrap appropriately, stack the key/value layout on narrow screens, and keep mobile chart labels readable. Repair the generator, never the generated HTML by hand.

**Acceptance:** at 390 px and a smaller agreed phone width, document width does not exceed viewport width; wide data tables scroll within their own labeled container; controls, evidence links and chart interpretation remain usable. Check keyboard focus and zoom, not only screenshots.

**Source:** [page generator](../../scripts/build_pages.py), CSS lines 146, 160–167 and tables near 584/615.

### F03 — P2 — Planned migration: “preserve v1 unchanged” needs a precise boundary

**Status:** known baseline gap already addressed by the future plan; migration coverage needs clarification.

The live site and README say CP-16 still needs a brief. The site presents CP-15 as the current development update; v2/v3 research is absent. This is consistent with presentation phases not having started, not a failure to execute an already-completed phase. However, replacing only the top card leaves other old future-facing text: the limitations call v2 “planned,” and the archived tracking note still describes a future `delu-m4` experiment. A link near the end points to `#development-update`, which the plan proposes removing.

**Change:** preserve v1's evidence, required honesty statements, values and historical context; distinguish those from obsolete navigation and current-status prose. Label retained historical forecasts/notes as historical and provide the current interpretation nearby. Update or preserve compatibility for affected anchors. Make v1 released, v2/v3 research-adopted, and future work separate states. Integration PASS is not product qualification or deployment.

**Acceptance:** no unqualified statement describes landed work as pending; all internal anchors resolve; the released model is explicit beside every demo link; historic statements remain accurate in their dated context.

**Source:** [page generator](../../scripts/build_pages.py), lines 325–347 and 620; [README](../../README.md); [claims](../../src/delu_forecast/claims.py); plan §§4, 5.1, 6.5–6.6.

### F04 — P1 — The README regeneration boundary does not cover the stale research section

**Status:** verified implementation fact that the plan describes imprecisely.

`cp3_readme.py` regenerates only the span from `## CP-3 showcase and release` to `## Setup`. It preserves the earlier “Current development” section. Running the existing script will therefore not refresh README research lines 18–54, even after adding a data loader elsewhere.

**Change:** explicitly assign generator ownership to the research section, using stable boundaries with checks for missing/duplicate markers. Keep unrelated hand-authored README material intact. Do not describe the entire current README as generated by this script.

**Acceptance:** changing one research fixture updates the research section through the generator; running it twice is stable; unrelated sections remain unchanged; missing markers fail clearly rather than silently leaving stale content.

**Source:** [README generator](../../scripts/cp3_readme.py), lines 29–30 and 172–182; plan §§3, 6.6, 7 and phase D.

### F05 — P1 — The current link checker is not a reliable pass/fail gate

**Status:** verified defect, reproduced with a negative control.

`check_links.py` records unresolved links but always returns 0. It also emits an obsolete fixed explanation that Pages and the Space have not been deployed, regardless of why a request failed. Its regex includes a localhost command example. For MLflow fragment URLs, a 200 response checks the HTML shell, not the experiment/run selected by the fragment.

**Change:** return nonzero for unresolved required public destinations; distinguish navigational links from command examples; classify local development URLs explicitly; record observed errors without guessing deployment state. Add semantic browser checks for the flagship destinations and the intended MLflow run/comparison, plus offline checks for local paths and anchors.

**Acceptance:** an injected required 404 causes failure; a localhost documentation example does not masquerade as a broken public link; an invalid run/fragment cannot pass only because the hosting shell returns 200. Store link observations with a check date.

**Source:** [link checker](../../scripts/check_links.py), lines 55–107. Local control: `link-control-exit.json` records exit 0 with an unresolved injected URL.

### F06 — P1 — Explicitly separate normalized and absolute uncertainty in chart C2

**Status:** verified source-unit difference; ambiguous chart specification.

The equal-fold rows in `uncertainty.csv` are differences in normalized scores. The per-fold rows are paired mean daily loss differences in **EUR/MWh**. For example, equal-fold MAE difference is `-0.07831150099532369`; fold-3 MAE difference is `-3.178237230571846`, with upper endpoint `+0.036877001609893`. Placing these rows on one common numerical axis would be misleading. The plan says “plus one row per fold” without defining separate units/axes.

**Change:** use a normalized aggregate panel and separate per-fold panels in EUR/MWh, with distinct MAE/WIS labeling. Do not invent normalized per-fold confidence intervals by dividing stored endpoints; a new estimand may require an authorized analysis. Show fold-3's crossing of zero visibly.

**Acceptance:** every series declares metric, unit, aggregation, comparator, interval method and evidence class. Rendering tests reject incompatible units on one axis.

**Source:** [uncertainty CSV](../../reports/weather-ablation/uncertainty.csv); plan §6.3 C2.

### F07 — P1 — Explain the v1 comparison change accurately, including the reference forecast

**Status:** verified presentation risk; correction to the earlier conversational review.

The difference between historical “28.58% worse” and `S_MAE=1.0518` is not just equal-fold versus pooled weighting. The saved CP-2 naive point MAE is `32.452299246301294`; the CP-20 B0 emitted-p50 pooled MAE is `32.81010165627617`. CP-20 preserves that first value as B0's `raw_central_MAE`. The common signed-residual distribution moves the emitted median. B1's pooled MAE remains `41.743481556831235` in both records.

**Change:** explain both differences beside the canonical comparison: equal-fold ratios versus pooled values, and raw-central naive versus the later residual-centered emitted-p50 reference. Also distinguish the original nine-quantile mean pinball score from seven-quantile WIS. Use a short explanation with an expandable metric definition, not unexplained conflicting headlines.

**Acceptance:** the reader can identify the population, weighting, forecast output and baseline for each percentage. No equation implies that all historical v1 numbers are directly comparable to the new scoreboard.

**Source:** [CP-2 pooled metrics](../../reports/cp2/development_pooled_metrics.csv), [CP-20 metrics](../../reports/weather-ablation/metrics.csv), [ratified definitions](../../capstone_v21.md) §§6–7, [existing content map](research-content/cp15-cp16-claims.md) C11/C14. No new score was estimated by this review.

### F08 — P1 — Define the claim/data contract and the scope of the tests

**Status:** plan gap; current checks cover a bounded v1 claim set.

The plan says `claims.py` feeds every surface, then introduces direct `research.py` consumers. This can be implemented coherently, but the interfaces and responsibility for public wording are unspecified. The existing CP-15 development card already contains literal numbers in the HTML generator. Passing `make verify` verifies its bound claim keys; it does not prove every research sentence and figure is mapped.

**Change:** define a shared evidence record with policy/generation identity, source file and immutable revision/hash, row selector, metric, units, aggregation, evaluation population, baseline, evidence class and display precision. Define how public claim IDs bind to these records and how renderers use the same approved wording. `research.py` can supply typed numeric records; `claims.py` or a clearly named research-claim layer owns the mapped public assertions. Do not force historical v1 strings to serve as unqualified descriptions of all generations.

**Acceptance:** a wrong row, wrong policy, wrong aggregation, missing claim ID or contradictory label fails, even when the same number appears elsewhere in the source. Every newly published qualitative assertion is reviewed against the claim map. Date guards inspect evaluation/input dates, not arbitrary publication/protocol dates in text. They must permit Sep-2026 checkpoint dates and historical v1 holdout disclosures without allowing new v2+ outcome use.

**Source:** [claims](../../src/delu_forecast/claims.py), [surface checks](../../src/delu_forecast/surfaces.py), [research draft](research-content/cp15-cp16-update.md); plan §§4.2, 6.7, 7 and phase A acceptance.

### F09 — P1 — Complete the MLflow contract before backfill

**Status:** plan gap, not a claim that planned code already exists.

The public service and v1 record are real. The new experiment and mirror tools are not yet implemented. The existing [tracking helper](../../src/delu_forecast/tracking.py) starts ordinary runs, logs scalar metrics, redacts only the configured DagsHub token in parameter strings, and uploads artifacts without the proposed upload scan. Those observations do not establish a current leak; they identify requirements for the new path.

**Change:** specify the following before adding the public backfill:

- Stable record identity and retry/resume behavior: rerunning an interrupted upload must not create unexplained duplicate runs or publish a partial package as complete.
- A durable committed export/manifest for reviewed tracking evidence. `.local/mlruns/<cp>` alone is disposable and cannot be the only preserved record. Remap parent/child run identities on publication and retain that mapping.
- Full verification of metric histories by key, step and timestamp, not only a run's latest scalar. Include both MAE and WIS paired deltas/intervals; the current metric list names only the MAE delta family.
- A comparability identifier that binds evaluation keys, target, units, score/quantile definitions, aggregation and reference policy. Identical metric names or `canonical_comparison=true` alone do not establish future cross-version comparability.
- Distinguish model-producing code SHA, evidence revision, and backfill-tool SHA. Do not stamp the backfill checkout as the historical model code. Preserve known original completion times; label missing metadata rather than fabricate it.
- Scan the actual outbound payload—artifacts, descriptions, tags and parameters—against the required credential sources without emitting values. Cover partial-failure paths. Do not infer that scanning only artifacts protects every logged string.
- Enumerate the exact expected runs, parents and references instead of “about 20.” Define what replaces unsupported features: a tag can preserve a digest or parent ID, but cannot replace a missing chart or anonymous comparison workflow.

**Acceptance:** an interrupted local rehearsal resumes without duplicates; a deliberately missing metric-history point or altered input digest fails mirror validation; an invalid public comparison route fails the reader-path check. Check the actual server/client combination. Do not upgrade hashed dependency files merely to obtain a UI feature.

### F10 — P1 — Separate preparation from public upload and owner publication

**Status:** ordering/authority ambiguity in the plan.

Phase C uploads to a public experiment before phase E's visual review. Thus the current sequence can publish charts, text and artifacts before the stated publication checkpoint. “At landing a publish script uploads” also needs an explicit executor and authorized action. Landing is not automatic authorization for an agent to publish externally.

**Change:** prepare and validate an export locally; render the proposed content with explicit unpublished-link placeholders; review the page and MLflow export packet; have the Owner perform or expressly authorize the permitted public MLflow action; capture real run IDs and validate the completed public destination; then rebuild the final page/index and hand it over for the Owner's visual approval and manual repository publication. Never ship placeholders. The capability probe needs a declared nonpublic/local mode or explicit authority if it creates public records.

**Acceptance:** the execution brief names which outputs remain local, the exact public actions, their owner and the ordering. Agents do not commit to `main` or push. Any required governance change is escalated under the existing Lockdown; this review authorizes none.

### F11 — P2 — Future evaluation and live display remain unresolved design work

**Status:** future plan gap; not a reason to block today's v1–v3 presentation.

The retrospective 4.7T window in the presentation plan overlaps periods previously evaluated for v1. The active anchor separately describes at least 90 consecutive days after policy freeze for future confirmation. The final protocol must reconcile those facts and prior knowledge before the page promises a “confirmatory” badge. For v1 preserve **“confirmatory-style, not power-qualified”**; a shortened badge must not silently strengthen that claim.

The future live panel also needs a clear boundary within the shared page, a separate data/claim builder and agreed publication mechanics. A `live_` prefix alone does not prove that the old guard protects the new design: `test_24` looks for live keys in `build_claims()`; its surface test checks only those detected keys. Live values rendered through another source can evade that mechanism. Conversely, adding live keys to the existing frozen claim set would violate its first assertion.

**Change:** keep retrospective final testing and prospective operation distinct until their protocols are settled; define semantic boundaries and meaningful negative controls for any future shared live/history page. Mark automated daily commits/publication as a future authorization/design decision, not an already-approved implementation detail.

**Source:** [active anchor](../../capstone_v21.md) §9, [live guard](../../tests/test_24_live_namespace_is_walled_off.py), plan §§5.4 and 12. The earlier conversational review overstated any implication that simply adding a live panel would automatically be caught by the current test.

## 4. Reader-experience additions to the plan

These are recommendations grounded in the inspected page and the Owner's stated goal. They are not measured usability-test outcomes and do not reopen approved R1–R6.

### U01 — Make the product and progress visible in the first screen

The current first screen is the title, methodology-heavy introduction, offline implementation explanation and table of contents. The forecast is section 10; tool destinations are concentrated in section 12.

Add a short problem/outcome introduction and three direct actions: **Try v1 demo**, **Compare research models**, **Inspect code and evidence**. Place a compact status strip beside them: released demo / latest adopted research model / next evaluation. Prefer an immediate link to the working inline historical replay as well as the heavier external app, clearly distinguishing lookup from actual browser inference. Keep measured first-load disclosures for the external app. Do not imply v3 runs in today's demo.

Show one principal comparison prominently, with its evidence qualification beside the numbers. Describe success as observed research improvement where that is what the evidence supports. Do not suggest measured trading returns, production readiness or universal superiority.

### U02 — Make feature development and decision history the spine of every chapter

Keep the approved newest-first order. Add a compact v1 → v2 → v3 lineage strip near the top, then anchor it to the chapters. Each adopted generation has a visible feature/policy delta, hypothesis, predecessor comparison, result, remaining weakness and adoption rationale. Rejected experiments are visible side branches. Planned features are a distinct “planned, not evaluated” list, never scored rows or invented version numbers.

Use the strongest existing stories: v1's crisis failure and insufficient calibration repair; moving toward LEAR/blending/residual intervals; adding the weather feature group with causal checks. Do not attribute H versus B2 improvement uniquely to hour-aware intervals: H versus P is the isolated comparison and does not establish joint preference. Do not attribute the aggregate weather gain separately to each of the three weather features without an isolating ablation.

### U03 — Add the system view and a short comparison-design explanation

Include one architecture diagram: source data and vintages → availability checks → feature construction → model/interval policy → evaluation and artifacts → report/demo/tracking. Mark implemented and planned components distinctly. Identify the information cutoff and where leakage controls act.

Add “How we made the comparison fair” beside the scoreboard: identical eligible rows, fixed score definitions and references, paired comparisons, uncertainty, and evidence limitations. Keep the detailed fold table and criteria accessible. Show the seven-policy table without making every reference policy compete equally for headline attention with v1/v2/v3.

### U04 — Let professional tools substantiate nearby claims

Put **Compare these runs in MLflow** beside the corresponding comparison; **Inspect the reviewed result** beside the decision; **View the source rows** beside a table; and a reproducibility link beside the architecture/results. Use canonical run identities rather than asking visitors to find one of several identically named reproductions. Explain the role of each tool in a sentence; avoid a logo wall and unsupported “best-in-class” claims.

Specify review provenance honestly: an independent Integration check within the project's review process is distinct from external scientific peer review. Record the exact candidate/verdict, preserve failed attempts in the deeper evidence trail, and avoid crowding the main narrative with internal repair identifiers.

### U05 — Add a small reproducibility path and an accurate ownership statement

Define a lightweight command that rebuilds a selected table/chart from committed summaries without fetching data, fitting models or consuming analysis-pass budgets. State expected output and requirements; measure its runtime before publishing it. Label it “rebuild the presentation from saved evidence,” distinct from full experiment reproduction.

Have the Owner validate a brief contribution statement: problem formulation, experimental decisions, implementation responsibilities, review and tool assistance, limited to what actually happened. Do not invent personal authorship or turn the project page into an agent-governance report.

### U06 — Add reader and interaction acceptance alongside numeric tests

An unfamiliar reader should be able to identify the product, the demo's version, the main observed improvement, one feature change, one rejected idea, the remaining uncertainty and the route to evidence. Verify that with an actual walkthrough; do not claim it has already been tested.

Require readable mobile charts, keyboard-operable controls/expansions, visible focus, useful text/table alternatives and durable anchors. Test final layouts with representative future chapter data so the v7 promise is about usable navigation and readable summaries, not just file size. Preserve the current scenario behavior: changing load from ×1.00 to ×1.02 hides the actual-price line and shows the scenario caveat; changing level to 95% shows empirical coverage `0.9398`.

## 5. Plan edits and proposed execution order

| Plan area | Required revision |
|---|---|
| §3 baseline | State that README regeneration is partial; bound claims do not cover all existing research prose. Separate observed client/server versions and dated observations. |
| §4 invariants | Preserve v1 evidence with explicit scope; define current-status wording updates; date guards operate on typed data fields. |
| §5 page design | Add U01–U06; retain newest-first chapters and visible process; define mobile/keyboard acceptance. |
| §6 content | Resolve C2 units; explain changed baseline/aggregation; preserve exact H−P endpoint and limitations; use final resource evidence. |
| §7 data layer | Add claim identity, evidence schema, provenance, comparability and renderer contracts; explicitly own the README research block. |
| §8 tracking | Add full-history verification, exact run manifest, retry/resume, durable export, provenance separation and outbound scanning. |
| §9 phases | Separate local preparation from public backfill and final owner publication; add runtime-demo and responsive gates. |
| §10 execution | Name the appropriate executor in the issued brief; require an independent claim-map/rendered-output check before publication. This review is not that independent final check. |
| §12 future | Mark confirmatory classification, live boundary and automated publication as future protocol/design decisions. |

Suggested implementation sequence once the Owner authorizes an execution task:

1. Diagnose F01 and incorporate F02/F05 into the update's acceptance requirements. Repair the relevant generators/checker as part of the authorized update; no separate cosmetic refresh of the old site is required.
2. Complete CP-20 claim mapping and the CP-15/16 publication pass. Specify metric units, comparator semantics and schema before parallel implementation.
3. Build the shared data/claim layer and explicit README section ownership. Validate presentation-only extraction without research reruns.
4. Produce one complete v3 chapter and the top product/comparison section locally; review their content density and evidence links. Then apply the template to v2/v1 and rejected branches.
5. Prepare the MLflow spec/export/retry/mirror implementation and a local rehearsal. Resolve real capability gaps without silently dropping promised reader functions.
6. Conduct the independent claim/rendering review, relevant automated checks and desktop/mobile walkthrough. Present the complete local page and export packet to the Owner.
7. Follow F10's authorized public-upload/index/final-build sequence. Run the required clean Python 3.12 CI-equivalent checks in the implementation task; preserve lockfile/manifest bytes. Owner performs repository publication. Verify the deployed reader paths afterward.

No fixed “agent days” estimate is validated by this review. Re-estimate after resolving the demo failure and the capability probe; those are concrete sources of uncertainty.

## 6. Handoff checklist

- [ ] Actual browser demo startup and inference verified; fallback is understandable.
- [ ] No document-level overflow at tested phone widths; chart labels and controls remain readable.
- [ ] Stale current-status text and removed anchors reconciled across page/README/cards.
- [ ] README research content is actually owned by a generator.
- [ ] Seven-policy comparison, exact H−P endpoint and HG−H0 findings trace to mapped sources.
- [ ] Raw-central versus emitted-p50, normalized versus absolute scores, and pinball versus WIS are explicit.
- [ ] No marginal interval, feature-bundle result or Integration PASS is presented as evidence it does not supply.
- [ ] New claims and charts bind typed evidence records; guard tests include wrong-label/wrong-source negative controls.
- [ ] Required public-link failures produce nonzero status; important app/MLflow routes are checked semantically.
- [ ] MLflow export is durable, complete, repeatable, scanned, and verified over metric history; no public mutation precedes its authority.
- [ ] Reader can see the product, progress, feature changes, rejected alternatives and inspection tools without reading the entire technical appendix.
- [ ] Clean required CI-equivalent run and independent content check completed on the final implementation; Owner reviews and publishes.

## 7. Return and repository accounting

This task creates this handoff document only as durable project content. It does not implement the corrections. No branch, tag or worktree was created; no file was staged or committed; no external state was changed. The initially clean `main` checkout is left with this new untracked Markdown document.

Retained local material: `.local/artifacts/presentation-review-2026-09-24/` contains the audit script, test/verification logs, HTTP and CSV observations, mocked link-control evidence, and small test scratch directories. It is recovery/diagnostic material; this document preserves the essential review evidence. A full new-file diff is provided there for owner review.

Proposed commit message (Owner only): `docs: record verified presentation review and correction handoff`.
