# PRES-2 — editorial record

The author's editorial review of the rendered publication against PUBLISH_RULES 1.0 (§§2–8, A1–A5),
the first step of §11's order. It is not the fresh reader (`fresh-reader.md`) and not the
independent check (`integration.md`); the author wrote the changes it reviews.

## What was read

- **The default reading path, disclosures closed:** the page served over HTTP, as a reader scrolls
  it, Chrome 154 at 1440×900 (15 screens) and WebKit 26.6 at 390×844 (24 screens)
  (`.local/artifacts/pres-2/local-release-attempt-6/cold-reader/`), page SHA-256 `47c74c45…`; and
  the README's generated top block. After the route-label repair (finding 8), the rebuilt page
  `f36314e2…` was read again where it changed: the v3 and v2 chapters' route lists (attempt 7).
- **The product documentation opened:** every topic's text, the feature, regime, attribution and
  permutation tables, and the three product charts at 1440, 390 and 320 px
  (`.local/artifacts/pres-2/local-charts-attempt-2/`).
- **Transitions and branches**, the comparison panel, the chapters' "Explore these results" lists,
  and the archive's replay at 320 px.

## What the rendered page shows

| Rule | Observation |
|---|---|
| A1 | The headline reads "v3: 14% below on the point-error score and 17% below on the interval score"; the finding sentence names both scores beside −12% [−16%, −9%] and −14% [−17%, −11%] (desktop screens 1–2, phone 1 and 3) |
| §2 placements, A2 | The headline block is whole on the first screen in both engines; the terms sit directly beneath it; the release rule and the measured start sit beside the demo action, outside any disclosure (desktop 1, phone 2); the finding sentence is readable by desktop screen 2 and phone screen 3 with the sticky header on every screen |
| F03 | "Runs in your browser: about 57 MB on a first visit. A forecast appeared after 18.3 s in Chrome 153 on a Mac, public demo, 2026-09-29; last verified 2026-09-29." |
| F04 | "7 policies · the same 10,747 historical hours over 448 days · error scores averaged with equal weight over five test periods · lower is better" |
| A4 | "How the product works" follows the opening, names the released model from the registry, and offers twelve descriptive routes; the comparison follows it; then "How it evolved", the transitions, the non-adopted branches, the chapters, planned work, evidence and contribution |
| A3 | "From v2 to v3: adding weather forecasts" and "From v1 to v2: a blended linear model with hour-aware intervals", each with predecessor, change, comparator, result, limits and decision; the v1→v2 card states that no paired v2 − v1 interval exists; "Experiments not adopted between v1 and v2" is headed apart |
| A5 | Every result chart has a visible descriptive route; the preview's "Explore this forecast" opens the product replay; the archive keeps "The replay in the archived report" |
| §5.1 identities | The SHAP topic says it is the released artifact's in-sample SHAP on fold 5's test block and that fold 5's out-of-sample ranking is different evidence; permutation importance is labelled fold 5's development model; the regime strata say they come from fold models, not the frozen artifact; reliability separates the frozen artifact's holdout from the folds and says the holdout report records no width |
| §6 charts | Direct labels and values; distinct marks per stage (circle, diamond, triangle) and a black nominal-level reference named "a reference, not a target"; phone variants put labels above bars; chart text at least 12 px at 320 px |

## Findings during the build and what was done

Each was found by looking at the rendered page or by a check, and repaired in the generator; the
generated page was never edited.

| # | Finding | Repair |
|---|---|---|
| 1 | The first product-first layout put the finding sentence at 1,841 px (desktop) and 2,695 px (phone), beyond A2's 1,744 / 2,420 px | A shorter product lede that names the model, so the separate model line went; shorter route labels; one compact startup line; the demo-details disclosure removed from the opening; phone side padding 20 px. Finding at 1,702.6 / 2,381.5 px |
| 2 | The reliability chart hid one stage's marker behind another, its labels collided, and its "0.2" axis label was clipped | One line per stage, wider label estimates, more left padding |
| 3 | The reliability chart's headline was typed in the generator | Bound as claim block `product.reliability.headline` (P46) |
| 4 | Two standalone links in the product topics ("Why these scores differ from its own report" and the forecast topic's "Try the v1 demo") were under 24 px high | Full-height `.quiet` links |
| 5 | The preview note and the reproduction paragraph pointed readers into v1's archive | They route to the product documentation; the archive's container instructions are named as historical (P49) |
| 6 | The product replay's text rendered at 11.91 px at 320 px | The renderer draws at the width inside the chart's border (`a5bca2f`) |
| 7 | The inline icon's SVG namespace was read as an address by the link gate | The icon is base64 (`a5bca2f`) |
| 8 | Three "Explore these results" labels in the v3 chapter drew their words together ("forv1,v2andv3"). **This review missed it; the fresh reader found it** (`fresh-reader.md`, observation 1) | Each label is one span inside its `inline-flex` link; the release check now reports words that run together in a flex or grid container without a gap, with a negative control (`pres-2-local-collapsed-space-control.json`) |

## Advisories — not violations of an effective rule

| # | Observation | Why it stays |
|---|---|---|
| E1 | The Limitations topic shows v1's limitation statements verbatim, with the original report's codes (A65/A01, A69, A75) and "Section 8.4", which points into the archived report | These are the single v1 claim source (`claims.py`), shared with the byte-identical archive, the README and both Space cards (invariants 2, 4 and 24). They sit in the depth layer, inside a closed disclosure, where §8 allows codes. A future product's documentation should state its limits without them |
| E2 | The inputs topic shows v1's exact percentages "+0.371516%" and "-19.4926%" (hyphen-minus) | v1 claim values in their exact form (`catalog_pct`, `benchmark_pct`), inside a closed disclosure; the precedent is advisory A-PRES1-14 |
| E3 | The transition cards date decisions by month ("September 2026") | The chapters' existing convention; exact dates are in the registry and the evidence rows |
| E4 | The page's startup line describes the published PRES-1 bundle | Labelled "public demo, 2026-09-29"; the new bundle differs by the control-name and target-size repair, the scenario slider's plain label and one line in its card, not in its model or payload. P8 measures the new bundle's cold start |
| E5 | In the demo, the interval-level radios' arrow keys move from a different radio than the checked one | A behaviour of the framework's radio group, identical on the published bundle; the keys operate the control and focus is visible (`pres-2-local-demo-a11y-attempt-4.json`) |

No proposed rule amendment arises from this review.
