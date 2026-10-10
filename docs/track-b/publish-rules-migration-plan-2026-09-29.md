# Migration to PUBLISH_RULES 1.0 — execution plan

> **Work-availability amendment, Owner-authorized 2026-10-10.** Scheduling restrictions
> have been removed under `AGENTS.md` § Work availability. Historical hashes and reviews
> bind the prior text at `522d7ea:docs/track-b/publish-rules-migration-plan-2026-09-29.md`; they do not bind this amended copy.

**Prepared:** 2026-09-29 · **Status:** complete planning deliverable; implementation not started.
**Proposed work item:** PRES-2, a presentation migration, separate from closed PRES-1 and unopened CP-21.
**Planning role:** Orchestrator. The Engineering Lead owns implementation choices when a valid brief
is issued. The touchpoints below identify inspected code, not a prescribed module decomposition.

## 1. Outcome, authority and scope

The migration is complete when the public report, README, Space card, runnable demo and advertised
MLflow routes meet [PUBLISH_RULES 1.0](../PUBLISH_RULES.md), including A1–A6, with independent
acceptance of the final candidate and fresh public verification after the Owner's publication.
Writing new rules or obtaining a local PASS does not complete this migration.

The visible result is a product opening followed immediately by useful documentation of the
actual released/frozen product; an early research comparison; clear transitions between adopted
generations and separate rejected experiments; and descriptive routes to the important charts.
The product documentation covers the original report's twelve subjects and moves with the product
when it is eventually replaced. It is not permanently tied to v1's chapter.

### 1.1 Governing identities

| Document | Version / identity / use |
|---|---|
| [PUBLISH_RULES](../PUBLISH_RULES.md) | 1.0; SHA-256 `03f106060d9a646ce0c0c986d2f5fb6549929f2ed7270f0c8678fbfd2293b3a3`; controlling publication anchor |
| [Publication Standard v1](publication-standard-v1.md) | Incorporated baseline; SHA-256 `01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`; apply its surviving clauses, not superseded wording |
| [Presentation/tracking plan R3](presentation-and-tracking-plan-2026-09-24.md) | SHA-256 `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`; surviving requirements under the precedence above |
| [AGENTS.md](../../AGENTS.md), [Engineering Lead contract](../../engineering-role.md) | Actual role, credentials, Git and publication authority |
| [Research anchor](../../capstone_v21.md) | v21-r4; SHA-256 `150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167`; read-only research constraints, particularly §§2–3, 6–8, 14 and 15; no new checkpoint execution |
| [Independent public review](publication-postdeploy-independent-review-2026-09-29.md) | Existing-rule findings F01–F04 and observed usability problems; unchanged historical evidence |
| [Runbook](publication-runbook.md), [packet template](publication-packet-template.md) | Execution references; their old structure does not override PUBLISH_RULES |
| [PRES-1 landing](pres-1-landing-2026-09-29.md) | Historical public identity and closure; its delegation is spent |

The previous task's Lockdown suspension ended at that task's return. This plan changes no anchor,
rulebook or role contract. It defines work under the existing publication anchor; it cannot relax it.
An implementation difficulty is not authority to move its bar.

### 1.2 What this plan includes

- Repair the four demonstrated v1 publication violations.
- Implement A1–A6 across the reading path, product documentation, generation transitions,
  chart discovery, accessibility checks and public verification.
- Reuse and accurately label existing evidence, adding presentation bindings and derived display
  records as necessary. Do not run new model evaluations to fill documentation gaps.
- Refresh generated surfaces and current deployment/reproduction instructions.
- Deliver a reviewed release packet, followed by Owner publication and independent public checks.
- Preserve all historical results, adverse facts, immutable review evidence and the v1 archive.

### 1.3 What remains deferred

A7's future-live contract is documented but not implemented as an operating service here.
No model is promoted, retrained, replaced or put live. No daily scheduler, new weather download,
new one-shot test, live scoring window, extension experiment or v4/v5 is introduced.
The demo remains the released v1 model until the research and release protocol permits replacement.

This distinction does not leave the twelve-subject product documentation waiting for a future model:
build it now for the actual released product, with identity derived from the registry. Design the
content contract so that a later authorized replacement changes the data and evidence it presents.

**Resources:** $0 external cost; no research-budget spend; dependencies remain pinned. Proposed
implementation timebox: **approximately 32 hours**, including review and directly necessary repair.
This is an estimate for the future brief, not a measured cost or a hard deadline that weakens acceptance.
Owner actions and service outages may extend elapsed calendar time. No recurring job is scheduled.

## 2. Verified starting point and preservation

### 2.1 Repository state at planning

- Branch: `main`.
- HEAD: `01e394d475202bb44a226f2ac5403aa084dc5b4c`.
- Incoming tracked modifications: `AGENTS.md`, `progress.md`.
- Incoming untracked files: `docs/PUBLISH_RULES.md` and the independent postdeploy review above.
- No staged change. No branch, worktree, commit, merge, push or deployment was created by this plan.

All incoming work belongs to the preceding tasks and must survive. Starting a candidate from HEAD
alone would omit the new anchor and review. Do not stash, reset, overwrite or silently absorb them.
The future execution start must identify a baseline that actually contains the agreed rules and plan.

### 2.2 Public identity rechecked for planning

Anonymous HTTP reads at **2026-09-28 23:35:00 UTC**, already **2026-09-29 in Asia/Jerusalem**, returned:

| Surface | Observation |
|---|---|
| [Pages](https://hrsi56.github.io/delu-day-ahead-forecast/) | 1,560,646 bytes; SHA-256 `d1227c0f64c6a478f6f076e713e2bed2755edf51d0b8f19522c9b978d42fab3d`; exact match to current local `docs/index.html` |
| [GitHub main](https://github.com/hrsi56/delu-day-ahead-forecast) | Same full SHA as local HEAD |
| [Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast) | Revision `59d941825755bf73eabb7ff20e31124fee305755`; Static; runtime reported RUNNING |
| [Direct app](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/) and [MLflow](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow/#/experiments/1) | Behaviour comes from the prior independent review; not freshly re-exercised during plan writing |

These are identity observations, not new browser, bundle-wide or service-acceptance verdicts.
The executable phases recheck identity and behaviour rather than treating this table as timeless.
Planning records are retained in `.local/artifacts/publish-rules-migration-plan-2026-09-29/`.

### 2.3 Known gaps

| ID | Current state | Required outcome | Phase |
|---|---|---|---|
| F01 | Demo slider and menu lack accessible names; menu target is small | Named, operable, appropriately sized controls in both engines; model identity preserved | P4 |
| F02 | Chrome requests a missing public favicon | Inline icon and actual public-origin request checks; no automatic 404 | P3, P8 |
| F03 | Measured startup/device/browser/date and last-verification metadata hidden | Compact verified metadata beside demo action, outside disclosure | P3–P4 |
| F04 | Overview's visible population omits 448 days | Bound hours and represented-day count visible together | P3 |
| A1 | Headline's 14% / 17% require later interpretation | Each value names point-error or interval score, with common headline source | P2–P3 |
| A2 | Placement check still uses raw 1800/2532 px limits | Header-aware formula and consecutive closed-state captures | P2, P5 |
| A3 | Rejected branches have an “Experiments between” heading; adopted transitions are less explicit | Distinct transition summaries for v1→v2 and v2→v3, with correct comparator and evidence | P2–P3 |
| A4 | Twelve-subject explanation sits in v1 archive near bottom | Current-product documentation immediately after opening, with all subjects accounted for | P1–P3 |
| A5 | Important graphs require undisclosed exploration | Descriptive visible routes, working deep links and keyboard access | P2–P3, P5 |
| A6 | Prior local/public checks have coverage gaps | Per-surface public identity and behaviour, retained failures/retries and honest tool limits | P5–P8 |
| Maintenance | README/product prose and deployment instructions carry historical or duplicated content | Accurate current instructions and concise paths; explicit historical archive | P4 |
| A7 | No eligible live product or issued daily forecast | Deferred; no placeholder masquerading as working live functionality | P9 |

The report's numeric results and core inference identity passed the prior review. Treat them as
protected regression targets, not as a reason to skip checks after moving or rebinding their display.

## 3. Target reading experience

### 3.1 Closed default page

1. **Opening:** forecast target and units; actual product identity/status and labelled preview;
   registry-derived research headline with metric names; demo action, startup metadata and release rule.
2. **How the product works:** short orientation followed by clearly named routes to the twelve
   product subjects. Detail bodies belong to this product section and expand here.
3. **How the models compare:** comparator, score-change intervals, principal caveat, absolute context,
   population/fairness and overview chart.
4. **How it evolved:** lineage and generation chapters, newest first. Each transition explains the
   change and decision. Rejected experiments are separately labelled and attached chronologically.
5. **Planned work:** unscored, no reserved version numbers or feature-availability claims.
6. **Additional engineering depth, contribution, terms and attribution:** no duplication of the
   product manual, and no essential product explanation available only at the bottom.

The twelve subjects are coverage requirements, not twelve long introductory essays. Group related
topics in a compact contents component. Use informative names such as “Data and information cutoff”,
“Validation and results”, “Where it fails”, “Intervals and reliability”, “Run this product”.
Every topic must still have a specific destination and traceable content; a generic collapsed
“Everything else” container does not satisfy discovery.

No new universal word count, click-count threshold or colour scheme is introduced. Existing
readability, placement, scale, precision, evidence and accessibility requirements decide acceptance.

### 3.2 Product and research stay legible as different things

- “Product” denotes the actually released model, currently v1. Use its model identifier visibly,
  without making the reusable documentation heading depend on the literal string “v1”.
- “Research” describes adopted experiments, currently through v3, without implying deployment.
- A research generation gets a concise question/change/result/limits/decision chapter. It does
  not receive a duplicate twelve-section product manual.
- The v1 archive stays available as a clearly historical record. Its old anchors remain valid.
  It is no longer the required route to understand the current product.

### 3.3 Placement and size feasibility are solved early

Measure the full headline without scrolling at 1440×900 and 390×844. The comparison finding must
fit at `N×H − (N−1)×h`, with N=2 desktop and N=3 phone, and h the measured persistent header height.
Use the largest header height on the route if it varies. Capture consecutive steps of usable
viewport height; do not hide the header or change the page to obtain a passing screenshot.

The starting document occupies about 1.56 MB of its 2.0 MB allowance. Adding a second copy of all
archived images is a known risk. Measure after the first product-topic prototype. Reuse existing
evidence and efficient offline assets; prefer data-rendered SVG where appropriate. If asset sharing
changes archive markup, prove the protected text and behaviour unchanged and review the rendered
diff fully. Do not claim byte identity after changing markup. Do not remove the archive, introduce
network dependencies or exceed the cap to make the layout pass. If no compliant solution fits,
return the exact compaction decision needed rather than silently changing the anchor.

## 4. Product-content migration inventory

P1 turns this table into a source-bound packet. Each subject records product ID/artifact or policy,
population, evidence class, source record/hash, proposed visible summary, detailed explanation,
graph/table route, limitation, and disposition: supported / not evaluated / inapplicable with reason.

The listed files exist at planning time. They are starting evidence locations, not permission to
assume that every result describes the exact frozen artifact. The Lead verifies that distinction.

| Subject | Starting source | Migration work and acceptance |
|---|---|---|
| 1 Data | `src/delu_forecast/claims.py`; existing archive's `#data`; committed snapshot metadata | Explain actual target, cadence, source, availability, cutoffs, preprocessing and rights. Bind quantitative facts. Distinguish product snapshot from research population and operational feed. |
| 2 Regimes | Existing archive `#regimes`; committed spectral/data summaries and their inputs | Retain the useful price-regime/negative-price explanation with dates and units. Reuse eligible historical data; no extension beyond the research boundary. Do not copy stale deployment statements. |
| 3 Features | `reports/cp2/catalog_selection.json`; product feature metadata; archive `#catalog` | Show features actually used by the released product, eligibility and exclusions. Separate selected features from historical candidate catalogs and post-gate diagnostics. |
| 3b Seasonal rationale | `reports/spectral_peak_bins.csv`, `reports/fig_per_regime_periodogram.png`; archive `#spectral` | Reuse supported seasonal reasoning, if applicable. This is not an instruction to recompute spectral analysis or impose it on every successor. |
| 4 Validation | `docs/cp2-model-report.md`; saved fold/holdout metadata; research protocols | Explain issue time, chronological splits, leakage controls, comparators and evidence classes. Preserve the one-shot label and unused-data protections. |
| 5 Results | `reports/cp2/holdout_report.json`, `development_metrics.csv`, `dm_development.json`; bound claims | Product results remain separated by evidence class. Keep adverse facts, units and uncertainty. Research-overview scores do not become a replacement holdout verdict. |
| 6 Attribution | `reports/cp2/diagnostics.json`, `shap_ranking.csv`, `shap_ranking_frozen_champion_in_sample.csv`, existing SHAP images | Inspect exact artifact/output/population. Distinguish fold-5 out-of-sample explanations from frozen-artifact in-sample explanations; never relabel one as the other. Use a correct label or a supported alternative. |
| 7 Importance/sensitivity | `reports/cp2/permutation_importance.csv`; diagnostic metadata; existing load-scenario logic | Label model, output and sample; distinguish importance, scenario sensitivity and causal/incremental value. No new permutation/SHAP run just to fill a topic. |
| 8 Conditional failures | `reports/cp2/regime_table.csv`; `diagnostics.json` | Present material regime failures with counts and uncertainty; qualify thin subsets and whether they describe development fits or the frozen artifact. |
| 9 Reliability | `reports/cp2/reliability_three_stage.csv`; holdout report; claims | Coverage and width together; actual pipeline stages and crossing facts. Keep observed final-output reliability distinct from a method's theoretical guarantee. |
| 10 Forecast | Existing replay payload/controls; `app/wasm_showcase.py`; frozen browser fixture | Provide a useful fan chart with actual replay date and level/scenario behaviour. Preserve outcome-versus-input and sensitivity caveats. No fabricated today's/tomorrow's prices. |
| 11 Limitations | `claims.py`; relevant research claim maps; active product metadata | Concise product-specific limits, failure modes and vintage assumptions, with fuller explanations in depth. Keep protected adverse facts; remove redundant prose only where the contract permits it. |
| 12 Reproduction | `scripts/rebuild_presentation.py`; `scripts/verify_wasm_equivalence.py`; README; `docs/deploy.md` | Separate reproduce report, run released model, inspect experiments and publish. Verify current instructions. Historical container hosting text cannot masquerade as the current Static Space route. |

**Important discovered distinction:** `diagnostics.json` contains
`frozen_champion_shap_top10_in_sample`, while the archived SHAP figure is described as fold-5
out-of-sample analysis. This is exactly why moving a figure under “The product” requires an identity
check. A shared method and similar feature rankings do not make the fitted artifacts identical.

If a required topic lacks product-specific evidence, report the gap honestly. Retain relevant
development evidence explicitly as such; do not rerun a holdout, invent a metric, or apply a cosmetic
“not applicable”. A missing research prerequisite follows the research authority, not this plan.

## 5. Generation transitions and experiment presentation

### 5.1 Required transition records

| Transition | Story to make visible | What the available comparison supports |
|---|---|---|
| v1→v2 | Move to the adopted blended LEAR policy with hour-aware intervals; how preceding experiments informed that choice | CP-16's pre-specified uncertainty rows compare V2-H with B2 and V2-P, and V2-P with B2. They do not provide a paired v2−v1 interval. The existing overview can supply correctly labelled descriptive common-population context. |
| v2→v3 | Add the admitted wind/radiation weather features and missingness indicators to v2 | CP-20 HG−H0 is a direct predecessor comparison; H0 is V2-H. Existing score-change records/intervals and per-period diagnostics already support the transition. |

For v1→v2, explicitly distinguish predecessor from research comparator. Do not fabricate a paired
confidence interval, treat unmatched holdout/development results as comparable, or introduce an
unapproved new headline ratio. State the limit of the predecessor comparison and link to the actual
protocol comparison. This satisfies A3 without commissioning a new experiment.

For v2→v3, use a descriptive heading such as **“From v2 to v3: adding weather forecasts”**.
Bind the existing point-score and interval-score change and uncertainty. State adoption in research,
the combined-feature nature of the test and the main limitations. The model served by the demo
remains separate and registry-derived.

Each record supplies predecessor, successor, actual change, comparator, population, evidence class,
decision date, outcome, limitations and evidence routes. Reuse chapter slots/registry records where
possible. If predecessor metadata is missing, add a validated relationship rather than deriving it
from a fragile label string or merely subtracting one from a version number.

### 5.2 Rejected paths

Preserve all existing rejected branches and their reasons. Label a group “Experiments not adopted
between …” or an equivalent unambiguous phrase. An adopted transition is not a rejected branch.
Do not manufacture “Experiments between v2 and v3” cards when no such additional rejected experiments
are documented. Include branches after the latest generation when evidence places them there.

Do not conflate:

- eight eligible policies tested against the target at the v3 decision;
- seven rows in the current overview;
- MLflow runs, controls, study arms or experiment-code aliases.

Display a short distinction where the counts coexist; retain the exact census in detail. The counts
remain derived and dated. Future tests assert their definition, not a permanently fixed eight/seven.

### 5.3 Chart discovery map

At minimum, expose descriptive routes to existing results that were hard to find:

| Reader's question | Existing target / evidence |
|---|---|
| How did the generations compare overall? | Overview comparison with fairness and absolute context |
| Did weather help across the periods? | `#v3-per-period-consistency`, including C2b |
| What are the absolute errors for each generation? | C3 within that disclosure |
| Does the difference vary by hour? | C5 within that disclosure; descriptive interpretation only |
| What happened during the crisis? | `#v3-stress-period`, C4 |
| Did intervals get more reliable or simply wider? | `#v3-coverage-and-width`, C6 |
| What did v2's control establish? | `#v2-protocol-and-review`, v2 chart 1 and the joint-preference limitation |
| How does the current product work/fail? | New product topic routes, independent of the v1 archive |

Preserve existing anchors or supply compatible aliases. New active-product IDs must not collide
with archive IDs such as `#data`, `#results`, `#forecast` and `#repro`. Direct links open ancestors;
keyboard focus and headings stay visible below the header. The preview may lead to the new product
forecast topic while old historical links continue to identify the archived replay honestly.

## 6. Phases, dependencies and deliverables

The critical path is **P0 → P1 → P2 → P3/P4 → P5 → P6 → P7 → P8**. P3 and P4 have independent
parts once content identity is fixed. The Lead chooses whether parallel work is useful and how
to isolate it under its contract. P9 is a future product lifecycle, not a task to execute now.

### P0 — Establish the actual execution baseline

**Entry:** Owner requests implementation and a valid single-work-item Lead brief is issued.

1. Resolve the existing uncommitted anchor/governance/review/plan work by Owner review and manual
   landing, or another explicitly authorized baseline arrangement that preserves every incoming file.
   No agent stages or commits main. No assumption that the current HEAD already contains the anchor.
2. Pin the resulting baseline, rule/plan hashes, source-data/model identities and current public
   revisions. Preserve the original comparison/replay/holdout evidence and archive behaviour.
3. Verify real branch/tree/topology before starting. The future Lead follows its authorized local
   checkpoint branch protocol. This planning task creates no branch/worktree and authorizes none now.
4. Collect the initial applicable-clause matrix, current output manifest and open-finding list.
5. Confirm tooling exists in project-local environments; do not change `pyproject.toml`/`uv.lock`
   or treat a missing tool as a reason to skip an acceptance requirement.

**Deliverable:** execution baseline record and populated acceptance matrix with A7 explicitly deferred.
**Exit:** the committed candidate basis really contains the controlling text; incoming work is safe;
one repository, work item, timebox and return contract are unambiguous.

### P1 — Establish content provenance and write the copy packet

1. Complete §4's twelve-subject inventory and §5's transitions from committed sources.
2. Classify existing paragraphs/figures as active-product, genuinely shared, development-only,
   historical, planned or obsolete operational description.
3. Draft short visible copy and deeper copy separately. Bind numbers, statuses and quantitative
   diagram labels to existing evidence sources. Add supported display bindings where absent.
4. Preserve v1's protected statements, one-shot qualification and adverse findings. Keep the
   original archive intact; new product prose is written outside it and verified independently.
5. Account for gaps without new scoring, new bootstrap draws or expansion of the data window.
6. Prepare the current-product replacement contract: the fields a future released successor must
   replace, with reuse of shared text only after an applicability check.

**Deliverables:** content/claim packet, product-topic coverage map, transition records, chart-route map.
**Exit:** every proposed factual sentence has a source or is clearly labelled explanation/planned work;
each graph has correct model/output/population identity; no product claim relies on a renamed v1 artifact.

### P2 — Prove the architecture with a narrow vertical slice

1. Render the opening with metric-labelled headline, visible startup metadata and release rule.
2. Add the compact product documentation entry and one representative topic with a real chart/table.
3. Move the comparison before lineage, and render one adopted transition plus one rejected branch.
4. Demonstrate descriptive topic/chart routes and automatic opening of nested disclosures.
5. Measure A2 with the actual header, body text and mobile variants; measure initial byte cost.
6. Adjust spacing, wording and grouping within approved tokens. Do not shrink labels below their
   floor, hide required caveats or push the comparison down to accommodate a large manual.

**Deliverables:** local desktop/phone specimen and initial placement/size record.
**Exit:** this structure can satisfy the inherited first-screen floor, A2 and the 2.0 MB budget
before all content is migrated. The specimen is not a publication PASS or permission to deploy.

### P3 — Complete the report and the research journey

1. Populate all product subjects from the accepted packet; implement product-bound content selection
   and model identity without duplicating the archive as the primary manual.
2. Complete v1→v2 and v2→v3 summaries and rejected-branch labels. Keep generic chapter slots and
   evidence links intact. Add no version number to a rejected or merely planned experiment.
3. Complete the discovery routes, exact-value alternatives, chart labels/mobile variants and old-anchor
   compatibility. Keep all required information on the appropriate reading layer.
4. Fix F02 in the page generator with an inline icon; preserve the report's offline/no-fetch property.
5. Fix F04 with a source-bound represented-day count beside the hours; do not hard-code 448.
6. Wire F03 to a verified measurement record outside a disclosure. Final public measurement is
   recorded in P8; an earlier local measurement is labelled by its actual environment/date.
7. Rebuild the page from its generator and verify archive text/behaviour, protected facts, numeric
   equivalence and size. Generated HTML is never edited directly.

**Deliverables:** complete generated report, source changes and focused regression checks.
**Exit:** no unpublished placeholders in the release candidate; no missing product topic; current
product/generation distinction is visible; route, evidence, presentation and scope contracts hold.

### P4 — Bring the demo and all companion surfaces into agreement

1. Repair F01 at the actual widget/export layer. A visible label in `mo.ui.slider` is already present;
   it did not establish the served control's accessible name. Inspect the compiled runtime/shadow
   DOM, name the slider and menu, and correct hit areas without changing model computation.
2. Test meaningful keyboard operation and both forecast-changing controls. Preserve the frozen
   model payload, inference path and bitwise-equivalence gate.
3. Regenerate `app/public/claims.json`, cards and the bundle before interpreting claim-parity tests.
   The earlier audit found stale ignored local payload fields while the public payload was correct;
   do not misreport this as a public-service defect or edit ignored output as the permanent repair.
4. Shorten the README's duplicated prose within its ownership boundaries. Keep the common headline,
   generation list, product identity, required limitations and useful run/reproduce routes.
5. Regenerate Space cards and align demo copy with the product explanation. Keep material limitations
   visible and use plain language for the scenario; move implementation terms into depth where allowed.
6. Correct current deployment/reproduction instructions, including `docs/deploy.md`'s old
   “awaits upload/template only” state. Distinguish the current public Space, local container and
   historical instructions. The prior landing used stored-token `HfApi.upload_folder`; verify the
   currently supported route at execution and document it without credential values or new login flows.
7. Compare MLflow export before/after. Keep research metrics, histories, provenance, historical
   experiment identities and existing artifact bytes unchanged, except the documented identity-only
   name/description/tag changes. `test_41_export_zero_diff.py` treats even a changed SVG as substantive.
   New report layouts/links must not silently rewrite old exported charts. Identity-only metadata
   changes receive a precise diff and the authorized mirror-update path in P7. Any irreducible
   substantive historical-export change is an explicit scope decision, not ordinary upload permission.
8. Update the non-governance runbook and packet template where new product/transition/route fields
   require it, preserving their contract checks. Locked landing templates remain untouched.

**Deliverables:** consistent README/cards, accessible demo bundle, updated operational documentation,
export diff and bundle manifest.
**Exit:** same actual model and research evidence; correct accessible controls; all surfaces agree;
instructions describe real supported operations, not the old deployment state.

### P5 — Complete local acceptance and upgrade checks that missed the defects

1. Run relevant claim/evidence, registry, page structure, parity, archive, offline and model-identity
   tests, including meaningful negative controls for new relationships/bindings.
2. Change the placement check from fixed 1800/2532 limits to A2's measured-header rule. Preserve
   consecutive screen evidence. Reject clipping/hidden content even when coordinates look valid.
3. Observe all report resource responses, console errors and automatic asset requests. A 404 may
   be an HTTP response without a Playwright `requestfailed` event. Inspect both.
4. Extend accessibility inspection to actual demo widgets, including supported frame/shadow boundaries.
   Report WebKit inspection gaps explicitly; an empty traversal is not a passing control inventory.
5. Record the full engine/width matrix, chart semantics, default and expanded layouts, discovery
   routes, keyboard/focus, contrast, touch and zoom/reflow.
6. Test demo cold starts and scenario/level response locally; exercise loading/failure/retry via
   browser interception that does not mutate a public service. Verify the instant-report return route.
7. Run one complete offline suite after the candidate stabilizes. Repeat only affected checks after
   subsequent fixes, with broader reruns when the change or failure warrants them.
8. Inspect JSON verdicts as well as process exit codes. Some existing reader-path subcommands write
   their findings and return zero; a zero exit alone is not an acceptance verdict.

**Deliverables:** complete local acceptance matrix, screenshots, machine-readable records and gaps.
**Exit:** no known local violation remains. Tests have not been weakened to match output. Claims of
public behaviour remain unverified until P8, even when identical local content passes.

### P6 — Editorial check, fresh reader and independent candidate review

1. Review the rendered reading path against the anchor, not only against the last review.
2. Supply a separate fresh agent with only closed-state screenshots and the six unchanged questions
   in PUBLISH_RULES §10.2. Preserve its actual answers, screen order and location of confusion.
   An informed author/checker cannot substitute for this agent. No repository/history/expected answers.
3. Check chart discovery separately by following the visible labels; do not coach the fresh reader.
4. Once the candidate stops changing, bind its full SHA and arrange the fresh, read-only independent
   checker under the Engineering Lead contract. The checker did not author the publication.
5. Review the full changed reading experience and all unchanged-content identity claims. Form
   findings independently before comparing earlier reviews and advisory dispositions.
6. Separate effective-rule violations, non-blocking product recommendations and proposed rule changes.
   Repair actual violations and recheck the resulting candidate; do not impose arbitrary review rounds.

**Deliverables:** editorial record, fresh-reader transcript/screens, independent verdict and review matrix.
**Exit:** independent PASS on the pre-publication candidate, or an honest INCOMPLETE/BLOCKED return
with the exact missing requirement. Publication is not implied by a PASS.

### P7 — Verify public tracking, freeze final artifacts and prepare Owner handoff

1. If export is unchanged, verify the existing public mirror and browser routes without a needless
   reupload. Reuse is justified by exact payload identity plus fresh verification, not prior PASS alone.
2. If the export has permitted identity-only changes, present its reviewed diff and obtain the
   required named public-action authority. Substantive changes to historical artifacts are outside
   this migration; do not upload them or weaken the export-preservation check. Upload only the
   accepted payload, scan outbound values with the real secret guard, and verify
   histories, parameters, tags, parent links, artifacts and intended routes. Preserve old experiment data.
3. The mirror verifier, never a person, writes the index from passing REST and Chrome/WebKit route
   records. Final build refuses missing expected routes. A local MLflow server is only rehearsal evidence.
4. Build final page/README/cards/bundle from the frozen sources and verified index; no later
   measurement or build step silently modifies reviewed content. Record source, output and bundle hashes.
5. Get a focused independent recheck on the exact final candidate SHA after final build/index changes.
   Re-run reader/editorial checks if the reading path changed. Preserve the verdict-only evidence-tip
   delta required by the Lead contract.
6. Hand the Owner the actual local artifacts, full diff, manifests, checks, open advisories and exact
   publication operations. Owner visual approval remains required unless explicitly delegated for this
   named publication. Prior PRES-1 delegation is not transferable.

**Deliverable:** publication-ready packet identifying final candidate, evidence tip, bundle, surfaces,
rules, authorized versus pending public actions and P8 commands.
**Exit:** locally complete, exact-candidate reviewed, no missing live link or placeholder. If publication
authority is absent, stop at this coherent handoff; do not claim the public migration complete.

### P8 — Owner publication and independent public acceptance

1. Owner performs mainline landing and publication under current AGENTS.md, with the prescribed
   review/evidence preservation and real hooks. This plan does not delegate mainline writes.
2. Publish the exact reviewed Space bundle and record its service revision. Coordinate Pages/README,
   card and demo updates to minimize mixed-version exposure; do not assume multiple hosts update atomically.
3. Fetch served HTML/card/assets independently. Compare with intended identities; retain raw bytes
   and explain any precisely identified hosting injection. Verify the complete bundle before asserting
   complete identity, not just its index. Record all surface revisions and timestamps.
4. Re-run required browser, placement, graph, link, accessibility and demo checks against public URLs.
   Explicitly close F01–F04 with their specified public acceptance evidence.
5. Verify anonymous MLflow mirror/routes and actual settled charts. A loaded app shell, login page,
   skeleton or HTTP 200 without the intended result is not a pass.
6. Preserve first failures, targeted retries, service conditions and tool limitations. Distinguish
   deployed defects, rate limiting and environment gaps. Do not edit a failure record into success.
7. Write a new postdeploy review with the applicable-clause matrix and PASS/FAIL/INCOMPLETE verdict.
   An earlier deployment PASS does not supersede a fresh demonstrated violation.
8. Close the migration only after public acceptance. Record outstanding advisories separately, update
   operational state and let the Owner decide branch disposition; preserve cited SHAs before cleanup.

**Deliverables:** deployment identities, public checks, before/after screenshots, new independent
postdeploy report and operational closure record.
**Exit:** all applicable effective requirements evidenced on the public surfaces. A7 is explicitly
N/A pending its trigger, not falsely marked as implemented or used to fail this publication.

### P9 — Future product replacement / Live handoff, not executed now

Carry forward a release checklist for the authorized future product:

- research qualification, one-shot/live prerequisites and policy freeze completed under their own plan;
- actual product registry/status transition, artifact/update lineage and valid release evidence;
- all twelve product subjects reviewed against the incoming product and updated together;
- historical product documents preserved while the main product explanation follows the successor;
- A7's issue time, delivery date/timezone, actual availability, score window/sample count, interval
  level, observed coverage/width, freshness and failure states populated from real records;
- daily inference versus retraining, frozen policy versus fixed weights and publication/scheduling
  authority explicitly resolved;
- no “percent correct” or “confidence tomorrow” label without its defined evidence and semantics.

This handoff is a documented interface for future work, not a placeholder live panel on today's site.

## 7. Inspected touchpoints and change boundaries

The Lead verifies these against the actual execution baseline. It may choose a smaller or cleaner
implementation without changing the acceptance bar. New modules are optional, not mandated here.

| Existing touchpoint | Why it is relevant |
|---|---|
| `scripts/build_pages.py::opening`, `demo_measurement`, `results`, `build_html` | Opening, startup metadata, fairness, section order, inline icon and size |
| `scripts/build_pages.py::render_chapter`, `v2_slots`, `v3_slots`, `lineage`, `branch_card` | Transition summaries, branch distinction, reusable chapter grammar |
| `scripts/build_pages.py::v1_archive_disclosure`, archived rendering, navigation JS | Protected archive, shared assets, stable links and separate product routes |
| `scripts/build_pages.py::CHARTS_BY_RUN` | Existing report/MLflow chart association; preserve historical exported chart bytes |
| `src/delu_forecast/registry.py::Entry`, `released`, `hero`, `_ENTRIES` | Actual product identity, dated statuses and predecessor relationships |
| `src/delu_forecast/research_claims.py`, `research.py`, `derived.py` | Metric-labelled headline, fairness population, transition claims, typed product display bindings |
| `src/delu_forecast/claims.py` | Released-product facts, limitations and shared claim provenance |
| `app/wasm_showcase.py`; `scripts/build_wasm_space.py` | Widget naming, menu target, plain demo copy, loading/retry and exported wrapper |
| `scripts/readme_research.py`, `scripts/cp3_readme.py`, `scripts/build_space.py` | Generated README/card parity and ownership boundaries |
| `scripts/rebuild_presentation.py`, `scripts/build_wasm_payload.py` | Coherent rebuild and fresh ignored payload; no model fit |
| `scripts/check_reader_paths.py::placement_findings`, `_screens`, AX helpers, `release`, `probe_demo`, `probe_states`, `mlflow_routes` | A2, public requests, demo AX coverage, discovery and real rendered routes |
| `scripts/verify_release.py`, `lint_publication.py`, `publication_guard.py` | Bound claims, offline property, lint, complete final output |
| `scripts/mlflow_export.py`, `verify_mlflow_mirror.py` | Export diff, immutable metrics, mirror/index and route identity |
| `tests/test_19_*` through relevant `test_42_*` | Existing offline, claims, archive, registry, architecture, parity, export and guard contracts |
| `docs/deploy.md`, `publication-runbook.md`, `publication-packet-template.md` | Current operational instructions and newly required packet fields |

**Generated outputs:** `docs/index.html`, generated README blocks, `space/README.md`,
`space-wasm/README.md`, presentation export/index/build records, and ignored browser payload/bundle.
Rebuild from source; never use a direct generated-output patch as the repair.

**Immutable or out of scope:** PUBLISH_RULES, AGENTS.md, role/configuration files, research anchors,
locked landing templates, preserved evidence/verdicts, raw model artifacts, saved research metrics,
one-shot results, `pyproject.toml`, `uv.lock` and all credentials. New evidence records use new names.
Do not overwrite a dated PRES-1 check when a current build helper defaults to that path.

If a helper necessarily writes a legacy build-manifest path, distinguish a current generated manifest
from immutable historical evidence, preserve the baseline and ensure the new publication record
points to the new candidate. The Lead reports the actual generated paths rather than hiding churn.

## 8. Verification recipe and tooling limits

Commands below document the existing interface; they are **not executed while writing this plan**.
Run them only inside the authorized execution checkout, with cache and temporary output inside
the project. The browser environment currently exists at `.local/tools/playwright/` and remains
separate from project dependencies. Confirm CLI/help at execution if the implementation changes it.

### 8.1 Rebuild and offline checks

```bash
uv run python scripts/rebuild_presentation.py
make wasm
make verify
make lint-publication
uv run pytest -q
```

`make wasm` builds the payload, proves existing fixture equivalence and assembles the export; it
does not authorize retraining. Do **not** run `make cp2`, `make train`, `make holdout`, `make diagnostics`,
`make register` or an umbrella target that publishes/registers or regenerates research.

After public tracking is verified and the index is current:

```bash
uv run python scripts/build_pages.py --final
make publication-guard
```

Expect the non-final-tree guard to fail before that point; do not disable it. Keep export and payload
consistency checks tied to the exact bundle being reviewed. Deterministic-content comparisons may
exclude only documented measurement timestamps, never claims or artifact identities.

### 8.2 Browser and public-service examples

For local development, substitute the local HTTP report/demo URLs and use new local-prefixed
record filenames. The commands shown here are **public checks after authorized publication**:

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py release \
  https://hrsi56.github.io/delu-day-ahead-forecast/ \
  --shots .local/artifacts/pres-2/public-report \
  --out reports/presentation/release-checks/pres-2-public-report.json

.local/tools/playwright/bin/python scripts/check_reader_paths.py demo \
  --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 \
  --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ \
  --out reports/presentation/release-checks/pres-2-public-demo.json

uv run python scripts/verify_mlflow_mirror.py verify --target public \
  --out reports/presentation/release-checks/pres-2-public-mirror.json

.local/tools/playwright/bin/python scripts/check_reader_paths.py mlflow-routes \
  --mirror-record reports/presentation/release-checks/pres-2-public-mirror.json \
  --shots .local/artifacts/pres-2/public-mlflow \
  --out reports/presentation/release-checks/pres-2-public-mlflow-routes.json
```

These existing commands are starting tools, not the complete new coverage. Extend them or add a
bounded companion check for demo accessibility, chart discovery, HTTP response failures, served
bundle identity and settled comparison plots as needed. Allocate new attempt filenames on reruns;
do not overwrite first observations. Promote required evidence to durable project paths according
to the return contract; `.local/` alone is not the release's public proof.

### 8.3 Required acceptance matrix

| Area | Acceptance |
|---|---|
| Rules/candidate | Exact hashes and full effective clause list; final candidate and reviewed output identities |
| Product | Released registry identity on all surfaces; twelve topics supported or honestly qualified; no transplanted model evidence |
| Opening/placement | First-screen headline in both engines; each score named; required terms/release rule/startup metadata; A2 with measured header |
| Transitions | v1→v2 comparator distinction and gap disclosed; v2→v3 direct evidence; rejected branches preserved; no invented experiment |
| Fair comparison | Bound hours/days, equal-fold method, proper metric/comparator/evidence class; no misleading aggregation or class mixing |
| Charts | Correct values, scales, units, interval kind and labels; phone variants; discoverable routes from closed default state |
| Browsers | Chrome and Playwright WebKit at 1440×900, 768, 390×844, 360, 320; emulated iPhone; heights/versions recorded |
| Accessibility | Named charts/controls, disclosure state, meaningful keyboard/focus, about-44px targets, required contrast; actual demo widgets inspected |
| Zoom/reflow | 200% and 320 CSS px; emulated equivalents explicitly labelled; no false claim of a real device/screen reader |
| Offline/size | No unintended report runtime request, favicon 404 or console failure; one self-contained page ≤2.0 MB |
| Demo | Fresh desktop/phone cold starts in both engines; level/scenario response; ready/loading/failure/retry; unchanged model equivalence |
| Archive | Protected text/adverse facts and behaviour retained; old anchors meaningful; current documentation is outside it |
| Parity | Same applicable headline, names, statuses, product limitations and valid links across report/README/cards/demo/tracking |
| Tracking | Exact mirror, histories/parents/artifacts and current advertised routes; intended settled plots; anonymous public access |
| Fresh reader | Separate agent, screenshots only, fixed six questions; answers 1–5 and placements checked; answer 6 advisory |
| Independent review | Checker did not author changes; final candidate bound; amendments not retroactively applied to historical reviews |
| Public acceptance | Served identities and actual behaviours, first failures/retries retained, F01–F04 closed by public evidence |

Tests do not replace manual inspection of text, chart meaning or default navigation. Real Safari,
a physical iPhone and a screen reader remain optional additions, not invented release gates.

## 9. Definition of done and failure handling

**Local-ready milestone:** complete P1–P6/P7 artifact set, no local violation, appropriate tests
and independent final-candidate PASS, reviewed export/bundle and a concrete Owner publication packet.

**Migration complete:** local-ready plus authorized P8 publication, matched public artifact identities,
all applicable public acceptance checks passed, and a new independent postdeploy PASS. A7 is deferred
with reasons. The old review remains intact and is linked to the new closure evidence.

If a required public check is unavailable, return **INCOMPLETE** unless a demonstrated violation
already warrants **FAIL**. Preserve service-rate-limit failures and retries. A green retry proves
that run, not uninterrupted availability. Do not call the entire migration complete while only
the local rendering is verified.

If publication fails or hosts serve mixed revisions, identify affected URLs/SHAs and stop further
unreviewed rollout. The Owner chooses a repair publication or restoration of the previously preserved
artifacts. Never auto-force-push, rewrite history, delete MLflow runs or change metric evidence.
No rollback is executed without its own authority; the packet supplies exact recoverable identities.

Advisory improvements may remain if they violate no effective rule. Missing current-rule evidence,
wrong model attribution or a broken required route cannot be relabelled as an advisory to finish.

## 10. Risks and planned responses

| Risk | Response / trigger |
|---|---|
| Current dirty main omits anchor from HEAD | Preserve incoming files; establish an Owner-reviewed baseline before candidate work |
| Product detail pushes comparison past its floor | P2 proves compact entry and real header-aware placement before full migration |
| Copying old figures misattributes a development fit to the frozen product | P1's artifact/population/class mapping; frozen SHAP versus fold-5 distinction explicitly checked |
| Duplicate archive/product figures exceed 2.0 MB | Early byte check; efficient reuse with archive behaviour proof; escalate actual irreducible compaction need |
| Generic “between versions” implies missing or invented experiments | Separate adopted transitions and non-adopted branches; show comparator/predecessor distinction |
| Framework widgets stay unnamed despite a Python-side label | Inspect exported controls, AX and shadow DOM; repair the source/export layer with unchanged inference |
| A 404 evades requestfailed monitoring | Inspect HTTP responses, resource timing and console alongside transport errors |
| Ignored local payload is stale | Rebuild claims/payload before parity and bundle checks; distinguish local mismatch from public state |
| Old tools return zero while records contain failures | Check structured findings and required coverage; no exit-code-only PASS |
| Fresh reader receives coaching/history | Separate context-free agent, fixed prompt, saved screenshot set and raw answer record |
| Tracking output changes during final build | Exact export diff; reject substantive historical-artifact changes, verify index and final-SHA rebuild/recheck |
| Public actions inherit spent PRES-1 permission | Named authority at the relevant step; Owner mainline/publication boundaries remain |
| Dependency or governance edit seems convenient | Preserve pinned dependencies/anchors; return exact necessity if no compliant local implementation exists |

## 11. Next execution handoff and outputs

The next action after Owner review is **one new presentation brief**, not reopening PRES-1 or
starting CP-21. The brief can use proposed identifier PRES-2, but the identifier is not opened by
this planning document. It must state:

- repository and actual Owner-reviewed baseline SHA containing this plan and anchor;
- PUBLISH_RULES version/hash and incorporated baseline identities above;
- complete acceptance scope: this plan §§1, 3–9 plus every applicable anchor clause; no convenience
  checklist narrows that scope;
- read-only research anchors/evidence, existing-rule findings and protected data/model artifacts;
- one approximately 32-hour timebox and the $0/no-research scope;
- exact currently authorized local/public actions and Owner handoff points;
- independent/fresh-reader requirements and required artifact/return paths;
- no presumed mainline/deployment delegation, no live activation and no locked-template amendment.

Suggested new output locations, finalized by the brief and never overwriting prior evidence:

| Output | Location |
|---|---|
| Content packet, applicability/transition map, candidate verdict and return | `docs/track-b/evidence/pres-2/` |
| Machine-readable local/public checks and deployment identity | New `reports/presentation/release-checks/pres-2-*` records, with attempt identities |
| New postdeploy independent report | A new dated file under `docs/track-b/`; no overwrite of the 2026-09-29 report |
| Local scratch, screenshots, browser caches and retained exact bundle | `.local/artifacts/pres-2/` and other project-local `.local/` paths |
| Required portable evidence | Committed records or referenced preserved artifacts as the return contract requires; not untracked machine-only proof |

The terminal return names work performed and unperformed, all checks/limits, final candidate and
evidence tip, output/bundle identities, public-action records, preserved baselines, changed files,
branch/worktree/ref accounting, open advisories and exact Owner next steps. It never describes
an uncommitted diff as an exact-SHA Integration PASS.

## 12. Planning validation and change record

This plan was prepared through read-only source inspection and anonymous public identity reads.
No training, evaluation, implementation build, browser acceptance suite or public mutation was run.
The source touchpoints and twelve-subject inventory were checked against actual repository files.
The current `placement_findings` still contains the old pixel constants; the existing screenshot
step already subtracts the header. The plan aligns their acceptance semantics rather than pretending
the new rule is implemented. The public identity check does not supersede the earlier review.

The only planned writing in this task is this document, a narrow `progress.md` routing/status entry,
and validation/handoff aids inside `.local/`. The active anchor, incoming AGENTS.md modifications,
independent review, historical rules/evidence and all source/build outputs are preserved.

**Revision 1, 2026-09-29:** full current-to-target migration plan; product documentation owns subjects
1–12; generation transitions distinguish predecessor from protocol comparator; four existing failures
and A1–A6 have executable phases and acceptance; A7 and product replacement have a bounded future handoff.
