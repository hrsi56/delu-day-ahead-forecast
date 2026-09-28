# D1 review: design, reader experience and replacement copy

**2026-09-25 · Stop 1 advisory review. Recommendation: retain the visual direction; revise D1 before final approval.**

The colors, typography, restrained panels and real product preview are a sound foundation. The main remaining editorial problem is that the page often explains its own research process before explaining what the reader should learn from it. The solution is a focused editing and layout pass, not a new design system.

This review proposes changes for the Owner and executor. It does not grant D1 approval, start D2, change the approved plan, or replace the mandatory independent implementation review.

## 1. What was reviewed

- Candidate: local `gauntlet/pres-1`, `92604e7dccbbbee50013491bb9f7a247891fe77c`, in `.local/worktrees/pres-1/lead/`. Main was at `e8025cc` and both trees were clean at inspection.
- Actual D1 specimen: `.local/artifacts/presentation/d1/index.html`, SHA-256 `66c222f8d7002efe9e0d11e826be77228b68aa4e4057e59edd7f1d421847ad02`.
- Browser inspection of that local specimen at desktop width, 390 × 844 and 320 × 844; navigation into the archived replay and its results link; the component sheet. Supplied desktop/mobile screenshots, demo-state specimen and measurement records were also inspected.
- Candidate sources: `scripts/build_pages.py`, `src/delu_forecast/research_claims.py`, relevant markup tests, measurement code and demo-state copy. All code locations below refer to the candidate, not the older generator on main.
- The builder's reader report was read. Its initial text pack precedes the final copy fixes; findings here use the final specimen itself.

The builder reports 711 passing and 7 skipped tests. This review did not rerun that suite or re-audit every scientific result. It directly verified the reader-facing defects below. Browser viewport testing is not a physical iPhone/Safari test. The MLflow placeholders and the unconnected demo-state specimen are expected at this stage, not failed public integrations.

## 2. Stop 1 decision

| Item | Recommendation |
|---|---|
| Palette, system font, basic type scale, panel style | Retain. Refine density and composition using these tokens. |
| Desktop composition | Retain the product/chart pairing; shorten the opening and remove duplicate navigation. |
| Phone composition | Revise: bring the product preview forward and stop the expanded roadmap from preceding the results. |
| Public copy | Revise before approval. Concrete replacements are provided below. |
| Scientific qualifications | Preserve their meaning and exact protected labels; express the surrounding explanation more naturally. |
| D1 completion | Return for a targeted correction pass, then review the corrected specimen. |

Several requirements were implemented faithfully but do not yet work well with real content. Collapsing the roadmap, consolidating result cards and shortening chapter prose are proposed plan adjustments for the Owner to approve, not accusations that the executor ignored the brief.

## 3. Verified findings and required corrections

### R01 — The opening describes the page rather than the product

**Where:** `build_pages.py:1166`, `research_claims.py:117`; opening screenshot.

“Explore the released demo and follow how successive research models were compared and improved” says what the visitor can browse. It does not explain hourly forecasts, uncertainty, or what the demo lets someone explore. The long startup paragraph then mixes interaction instructions, deployment architecture, download size, browser version, cache state and measurement date. The research summary adds a normalized subtraction and confidence interval before explaining the practical finding.

**Change:** use the opening copy in §4A. Keep the measured startup record, but move its detailed conditions into a disclosure. Keep a short download warning beside the demo action. Use a qualitative, evidence-bound research takeaway in the opening; the exact differences and intervals already have a better home in the research chart.

**Acceptance:** before any methodology explanation, a reader can say what the forecast contains, what the demo runs and what improved in research. The research result remains clearly separated from the released v1 demo.

### R02 — The phone route delays both the product and the achievement

**Where:** `opening()`, `journey()`, `planned_work()` in `build_pages.py:1166`, `1379`, `861`.

Fresh browser measurements at 390 × 844, in the specimen's default state:

| Landmark | Approximate page Y coordinate |
|---|---:|
| First product plot | 1,057 px |
| Journey section | 1,782 px |
| Expanded planned-work block | 2,507 px; about 1,078 px tall |
| Overview results section | 3,601 px |

The reader passes technical startup prose and more than a screen of unevaluated plans before reaching the main comparison. This is a hierarchy problem even though the page has no horizontal overflow.

**Change:** on phones, order the opening as title → concrete description → compact version/status pair → actions with one short startup line → product preview. Under the compact lineage, replace the expanded roadmap with one sentence and “See planned experiments.” Put the full roadmap after the completed research story, or keep it in a closed disclosure.

**Acceptance:** the preview begins within approximately the first screen to screen-and-a-half at 390 × 844, without shrinking text. The comparison follows the compact lineage; the visitor need not read the future-work inventory to reach a measured result. Treat the coordinate target as a usability target, not a reason to remove necessary qualification.

### R03 — The same result is presented repeatedly, while the decision is hard to extract

**Where:** `v3_chapter()` at `build_pages.py:1271`; `v2_chapter()` at `1319`.

v3 repeats the normalized differences in the opening, two outcome tiles and the main chart; the chart title and following paragraph repeat the confidence-interval conclusion. The evidence badge also recurs in close proximity. Meanwhile the chapter's introduction uses three parallel blocks whose cumulative prose makes a long phone prelude. v2 asks a newcomer to decode LEAR, pooled control, joint preference and several score pairs at once.

**Change:** let one main figure carry the exact results. Either integrate the outcome values into its header or remove the separate duplicate tiles. Keep one concise explanation of the change, one interpretation, the critical limitation and the adoption decision. The surrounding copy in §4C–D supplies that sequence. Keep all protected exact values and caveats visible where required.

**Acceptance:** each chapter has one unmistakable takeaway. A reader can explain the change and its limitation without reading source codes or all experimental contrasts. A result is not repeated merely to fill another card.

### R04 — The mobile v2 plot still has a text collision

**Where:** `build_pages.py:438–440` and the mobile row layout at `526–558`; chart `v2-chart2`.

At 390 px the long H−P interval label overlaps the next row label, “control − daily LEAR.” This was reproduced in the browser and is also visible in the final supplied screenshot. The helper drops long text by 19 SVG units, but the next row is still placed using the unchanged 58-unit row spacing.

**Change:** reserve actual extra row height for long values, or put that interval in its own text row outside the plotted region. The exact upper endpoint `+0.000003857628092332211` must remain visible and must not become `0.00` or a tooltip-only value. It is already printed separately below the plot, so avoid an unnecessary second long overprinted instance.

**Acceptance:** inspect this exact row at 390, 360 and 320 px, and on desktop. No label overlaps another row, a mark or an interval. A font-size/overflow check alone does not detect this defect.

[Evidence crop from the supplied final 390 px screenshot](../../.local/artifacts/presentation-d1-review-2026-09-25/v2-mobile-crop.png).

### R05 — The readable-phone-chart claim does not cover the complete reader route

**Where:** opening preview, archived interactive `#chart`, and `tests/test_31_page_structure.py:91`.

- At 320 px the preview's mobile SVG renders 262 px wide from a 320-unit viewBox with 13-unit text: approximately **10.64 px**. This matches the builder's recorded reflow result and is below the plan's general 12 px floor.
- More seriously, following the prominent replay link at 390 px opens the archived interactive chart with a 960-unit viewBox rendered at 358 px. Its 11-unit axis labels render at approximately **4.10 px**. The new-variant measurement/test does not establish readability of this legacy chart.

**Change:** provide a legible responsive treatment for the interactive replay as well as the new preview. Use a mobile geometry, fewer ticks and sufficient label space while preserving controls, plotted data and scientific meaning. Do not solve this by making readers zoom into a miniature desktop chart.

**Acceptance:** verify rendered text on the actual preview-to-replay route at the supported phone widths. Keep the 95% coverage and scenario-caveat behaviors intact. Report the legacy chart and 320 px exception honestly until fixed.

### R06 — The archive's “Results” link goes to the wrong results

**Where:** `build_pages.py:1209` and archived heading/navigation at `2012`; `test_31_page_structure.py:70`.

The final HTML contains two elements with `id="results"`: the new research overview and the original v1 “5 · Results” heading. Clicking the archive's “5 · Results” link jumped to the new overview in the browser. The current anchor test converts IDs to a set, so it verifies existence but misses duplication and destination meaning.

**Change:** use unique IDs and explicitly preserve the intended legacy destinations. A clean option is to give the new comparison its own anchor, such as `#research-results`, while keeping `#results` for the original v1 section. Update the new navigation and “Back to overview” links consistently; ensure navigation into the archive opens it.

**Acceptance:** no duplicate IDs, and both the top-level Results route and the v1 Results route land on the intended content. Verify old bookmarks as well as current links.

### R07 — Main research charts lack the promised table alternative

**Where:** `single_rows()` return at `build_pages.py:566`; v3 and v2 analytical panels.

The overview has a table disclosure, but the v3 main difference panel and v2 main contrast panel have none. Their SVG descriptions and adjacent prose explain the conclusion, but are not a complete table of the chart's records and intervals. This falls short of the plan's table-alternative contract.

**Change:** provide a labeled “View values” table for each research chart, built from the same typed series, with contrast, metric, estimate, interval and unit. Put it in a disclosure so it adds access without adding initial visual density.

**Acceptance:** a reader can retrieve every plotted value without interpreting an SVG or following a raw CSV link. The full exact v2 endpoint remains available in the accessible text/table route.

### R08 — Some wording is vague, defensive or stronger than the evidence needs

**Where:** claim templates and `build_wasm_space.py:184–189`.

| Current wording | Problem | Proposed wording/direction |
|---|---|---|
| “the crisis fold is not diluted by the calmer ones” | Does not explain equal weighting clearly; it can imply crisis upweighting. | “We score each historical period separately, compare it with the same baseline, and give all five periods equal weight.” |
| “Before you read more into it” | Addresses the reader defensively. | “What this result does not establish.” |
| “No prospective clock has started” | Internal process vocabulary. | “Performance on future data has not yet been evaluated.” |
| “in exchange” for lower coverage | Suggests an isolated causal tradeoff. The page presents observed width/coverage together. | “The intervals are narrower, while pooled 95% coverage is slightly lower.” Keep the recorded values. |
| “v1 collapsed” | Dramatic and less precise than the measured mechanism. | “v1 substantially underestimated prices during the 2022 crisis.” |
| “Nothing is sent to a server” | An unqualified network/privacy assertion is unnecessary beside a runtime download. | “Forecast calculations run locally in your browser.” |
| “The report has the same results and needs no download” | Opening a report still transfers its page; it also cannot perform every demo interaction. | “You can view the saved forecast and research results without loading the model.” |

The system view also needs to distinguish **enforced input cutoffs** from **documented source-availability assumptions**. Its current universal “each is tested with a control” language should be reconciled with the archive's explicit load-forecast availability assumption. Suggested summary: “Inputs are restricted to the forecast's information cutoff; source-availability assumptions are documented.” Link the assumptions rather than implying that every publication timestamp was measured.

## 4. Replacement copy for the main reading route

These are proposed public-facing English strings, not an instruction to bypass the claim layer. Rebind existing claim IDs and source records to the revised templates. Numbers below retain the candidate's display values; no new percentages, model runs or analyses are proposed. Preserve the exact v1 evidence label and other protected wording where required.

### A. Opening

**Eyebrow:** German–Luxembourg electricity market

**Title:** Day-ahead electricity forecasts, with uncertainty.

**Description:** Explore hourly price forecasts and prediction intervals on historical days. See how successive research models improved, what failed, and how each result was checked.

**Status pair:**

- Demo: v1 · Released model
- Research: v3 · Weather features — Development · post-selection

**Actions:** Try the v1 demo · Compare model results · Code and evidence

**Short startup note:** Runs in your browser. First visit downloads about 57 MB; startup time varies.

**Disclosure: “What the demo does and startup details”**

> The demo runs the released model on historical delivery days. Change the interval level or load scenario to explore its forecasts. Calculations run locally in your browser. In the recorded cold-start test, a forecast appeared after 20.4 seconds in Chrome 153 on a Mac, measured on 2026-09-24. Other devices and connections may take longer.

Render the measurement from its release record; do not hard-code this example in the generator.

**Preview label:** Historical forecast · v1

**Preview caption:** Forecast and observed price for a held-out day. This is a historical replay, not a live forecast.

**Legend:** Median forecast · 80% prediction interval · Observed price

**Preview action:** Explore this forecast

Add a short secondary destination note, “Opens the replay in the original v1 report,” rather than putting that whole explanation inside a prominent link label.

**Research takeaway:** Adding weather inputs improved both point-error and interval scores compared with v2 in development tests. Performance on future data is still to be evaluated.

This qualitative sentence is the recommended replacement for the opening's unexplained delta. It requires no new relative-percentage claim.

### B. Overview and progression

**Lineage introduction:** v1 is the released demo. v2 changed the forecasting approach; v3 added weather inputs. The branches show experiments that informed those decisions.

Keep the canonical version names in metadata and chapter headings. In the compact diagram, describe the change in accessible language instead of making a long model name do all the explanatory work.

**Roadmap teaser:** Next, we will test alternative models, renewable-generation forecasts and model combinations, followed by evaluation on fresh data. These steps are planned, not evaluated.

The detailed roadmap should use descriptive names first. Put `4.6`, `4.4V`, checkpoint codes and license/resource prerequisites in the detail layer. For example: “Alternative model families,” “Wind and solar generation forecasts,” “Models for different parts of the day,” “Combining models,” and “Fresh-data evaluation.” Keep the active plan's actual sequence and conditions.

**Overview heading:** How the models compare

**Finding:** v3 has the lowest point-error and interval scores among the seven evaluated policies on this shared development comparison.

**How to read it:** Lower is better. Each score compares a model with a simple similar-day forecast, which scores 1.00. The interval score accounts for both interval width and missed outcomes.

**Fair-comparison note:** Every policy was evaluated on the same 10,747 hours across five historical periods. Scores are normalized within each period, then averaged with equal weight. These are development results, not evidence from a new future-data test.

Keep the diagnostic threshold explanation next to the chart. Keep the full bootstrap settings and the explanation of v1's different historical score in disclosures. Add a short visible pointer beside v1: “Development replay; its separate holdout results are in the v1 chapter.”

### C. v3 chapter

**Editorial subtitle:** Adding weather information improved both forecast scores.

**Change:** v2 used price history, the load forecast and calendar inputs. v3 added forecast wind speed and solar radiation available before the auction, while retaining the same underlying modeling setup for the comparison.

Keep the existing diagram to name the three features precisely, including both wind heights. Detailed missing-indicator and GFS-recipe text belongs in the feature disclosure.

**Main chart title:** Weather inputs improved both development scores against v2.

**Interpretation:** Both estimated score differences favor v3, and their aggregate 95% confidence intervals remain below zero. The exact values and intervals are shown in the chart.

**Visible qualification:** The point-error result is less certain in the 2022 crisis fold: its confidence interval crosses zero. The gain belongs to the three-feature bundle; this comparison does not isolate an individual feature's contribution.

Keep the recorded fold-3 interval beside this explanation, and retain the development label. The critical limitation must remain visible even when diagnostics are closed.

**Decision:** We retained v3 as the current research model. The demo continues to run v1; v3 has not yet been evaluated on future data.

Keep the existing compact helps/hurts comparison, using the neutral coverage wording from R08. Put the six-criteria inventory and review mechanics in their appropriate deeper sections, with a concise visible statement if needed by the claim contract.

### D. v2 chapter

**Editorial subtitle:** Recalibration alone was not enough; the forecasting model had to change.

**Problem:** v1 substantially underestimated prices during the 2022 crisis. Recalibrating its intervals improved coverage, but the improvement was insufficient.

**What informed the change:** A comparison of nine forecasting policies informed the move to a blend of two LEAR forecasts. The simpler daily LEAR reference remained a strong benchmark.

**What changed:** v2 combines the two forecasts and uses intervals that account for the hour of the day. A control version uses the same blend with a pooled interval method, allowing the interval approaches to be compared.

**Main chart title:** v2 improved on daily LEAR; the interval-method comparison was inconclusive on joint improvement.

**Visible interpretation:** Against daily LEAR, v2 improved both development scores. Against the same blend with pooled intervals, the comparison did not establish improvement on both scores. The point-error confidence interval extends slightly above zero; the exact endpoint is shown below.

Preserve the full endpoint, the interval-score result and “This is not equivalence.” The gains over the reference must not be attributed to hour-aware intervals alone. Keep the original contrasts available in the chart/table, without repeating every tuple again in surrounding prose.

### E. v1 and evidence

**v1 introductory direction:** introduce it as the released historical demo, summarize its separate holdout result under the exact badge, then explain the crisis weakness that motivated further work. Keep all protected evidence; avoid making a DM statistic the introductory sentence a new reader must understand.

**Evidence links:** Compare experiment runs · Read the review · View source values

**Tracking explanation, for the final verified public state:** Experiment runs, metrics and artifacts can be inspected in MLflow. The published page is built from saved repository evidence and works independently of the tracking service.

**Prototype state:** retain honest unavailable-link text until the public routes are verified. Do not make the proposed final-state copy claim an upload has already occurred.

**Reproduction heading:** Rebuild the report from saved evidence

Separate dependency setup (`uv sync`, which may download packages) from the subsequent report rebuild. “No download” should describe the evidence rebuild after setup, not both commands indiscriminately.

## 5. Answers to the builder's outstanding Stop 1 questions

1. **Composition and tokens:** retain the tokens and visual direction; amend the composition and defects listed above before final D1 approval. Remove the desktop rail's duplicate Results/Journey/Evidence list; the header already provides those routes. Retain the generation rail. Give the phone header a compact project identity or home link.
2. **Contribution statement:** the current statement is honest but reads like a literal translation. Recommend the tighter wording below, subject to the Owner's explicit approval. Use the Owner's approved public name, preferably once as a compact byline near the opening linked to the full statement. Do not add unsupported claims of sole implementation.
3. **Device test:** remains an Owner-supplied observation. This review's emulated widths do not fill in a missing physical-device record.
4. **Move Contribution up:** move a short identity/role line up; keep the full paragraph near the end. The measured product and results should retain priority.
5. **Replace the delta with a percentage:** use the plain-language takeaway above instead. A future relative percentage needs a clearly defined denominator and a typed, tested derivation; `−0.0783` must never silently become “7.83% better.”
6. **Define more terms:** yes, at first relevant use. “Five historical test periods” can introduce folds; explain normalized scores beside the overview; explain the baseline and the control in the v2 story. Full formulas and internal checkpoint codes can stay deeper. Avoid expanding the hero into a glossary.

**Proposed contribution wording — Owner approval required before replacement:**

> I led the project's problem definition, evaluation criteria and research direction, and made the decisions on model adoption and product presentation. AI agents assisted with implementation, analysis and documentation. Automated tests and reviews separate from implementation supported verification. I retained responsibility for approving deliverables and publication.

This is a wording proposal only. The approved plan reserves changes to that statement to the Owner; the current statement was not edited.

## 6. What to return for the next D1 review

- A corrected opening and compact route from product to measured results, at desktop and 390/360 px.
- The v2 main chart at desktop, 390, 360 and 320 px, with the exact endpoint and no overlap.
- The preview-to-interactive-replay route at phone widths, with readable axes and the existing control behaviors preserved.
- A unique-anchor check and a browser check showing that original v1 Results and new research Results are distinct working routes.
- Accessible value tables for the main research charts, with the remaining chart alternatives accounted for before publication.
- Updated reader tasks against the corrected specimen, using the copy changes above. Record whether the reader can explain what improved, rather than merely locate a number or repeat an internal term.

The specimen deliberately opens one diagnostic for D1; that is not itself a defect. Review the final default reading state separately, with optional diagnostics closed. Do not call D1 approved solely because numeric binding, page width and unit tests pass: the overlap and wrong Results destination demonstrate why direct reading and interaction remain necessary.

**Scope of this review:** one new review document and ignored local review evidence only. No candidate source, approved plan, contribution statement, governance file or program state was changed. No commit, publication, MLflow write or D2 execution was performed.
