# PRES-2 — content packet, coverage maps and applicability matrix

Written by the Track B Engineering Lead for PRES-2 (plan §6 P1 deliverables; packet template §§5a–5c;
PUBLISH_RULES 1.0 §11 and §13). Every number on a public surface comes from a committed row through
the evidence layer (`src/delu_forecast/research.py`, `derived.py`) and a claim block in
`src/delu_forecast/research_claims.py`, bound in `docs/track-b/research-content/publication-claims.md`
(rows P33–P50 are new in PRES-2, P20 amended). This packet names those bindings; it restates no
number that the page does not derive. The candidate SHA that carries this file is named in the
checkpoint return and in `integration.md`, not here.

## 1. Identity

| Item | Value |
|---|---|
| Checkpoint | PRES-2, brief `docs/track-b/pres-2-execution-brief-2026-09-29.md`, SHA-256 `fa118734a6d82d34bf94836a20452a79aa6d7d9a56f8a5529084be20933ad47e` |
| Publication anchor | `docs/PUBLISH_RULES.md` revision 1.0, SHA-256 `03f106060d9a646ce0c0c986d2f5fb6549929f2ed7270f0c8678fbfd2293b3a3` |
| Execution plan | `docs/track-b/publish-rules-migration-plan-2026-09-29.md` revision 1, SHA-256 `24913b2b947aeef585e5994d61c91fed3c9eb0da830d6366c7f749e689b724c8` |
| Incorporated baseline | Publication Standard v1 `01d721c2…69478cc`; presentation plan revision 3 `28119374…149812c` |
| Research anchor (read-only) | `capstone_v21.md` v21-r4, `150bd53f…c1926167`; no research checkpoint opened |
| Baseline commit | `3702340660bbc1a5e1483ecaa206cd6709eb63a3` (exact-copy baseline, `baseline.md`) |
| Released product (registry `released()`) | `v1 · released LightGBM`, status "released", 2026-09-15 |
| Research headline (registry `hero()`) | `v3 · weather features`, "adopted in research", 2026-09-24 |

The product and the research headline stay separate identities (PUBLISH_RULES §1.2, §4): the demo
serves v1 under the release rule; v3's research adoption does not change it.

## 2. The twelve product subjects (A4, §5.1; packet template §5b)

The section "How the product works" (`#product`) follows the product opening. It lists twelve
descriptive routes (`nav.product-routes`) and holds the topic bodies in one named disclosure, "All
topics in full" (`#product-manual`), inside the product section. The topics are built by
`PRODUCT_DOCS[released.id]` in `scripts/build_pages.py`; `product_topics()` refuses a build whose
topics miss, repeat or invent a subject, or carry a disposition other than supported / not evaluated
/ inapplicable (`tests/test_43_publish_rules_migration.py`, with negative controls).

| Subject (§5.1) | Route label → anchor | Disposition | Model, output and rows the evidence describes | Evidence (claim row; records or sources) |
|---|---|---|---|---|
| 1 Data | "Data and the information cutoff" → `#product-data` | supported | The released artifact's data contract: target, the committed snapshot 2019-01-01 to its cutoff, fit, calibration and holdout windows, quarter-hour handling; no live feed | P38; `claims.py` (`snapshot_cutoff`, `raw_model_fit_cutoff`, `final_calibration_window`, `holdout_window`, `attribution`, the availability assumption) |
| 2 Regimes | "Price regimes and negative prices" → `#product-regimes` | supported | Development hours of the released recipe, split by regime (population `v1-development/<stratum>`) | P39; `cp2.regime.{pre_crisis,crisis,post_crisis}.n_obs`, `cp2.regime.negative_price.{n_obs,n_days}` from `reports/cp2/regime_table.csv` (blob `417d2ccc…` at `evidence/cp-2`); archive route `#regimes` for the yearly figures |
| 3 Inputs | "The inputs it uses, and why" → `#product-inputs` | supported | The frozen artifact's 25-input `base` catalog, grouped from the model card; the rejected residual-load proxy and the excluded post-gate forecast, each with its pre-registered comparison | P40; `models/champion/champion_card.json` `feature_list`; `claims.py` (`champion_features`, `catalog_pct`, `benchmark_pct`) |
| 3b Seasonal rationale | same topic | supported | The spectral reasoning behind the calendar inputs, reused, not recomputed | P40; `reports/spectral_peak_bins.csv`; archive route `#spectral` |
| 4 Validation | "How it was tested before release" → `#product-validation` | supported | Five 90-day walk-forward development folds (10,747 hours on 448 days), three baselines on the same rows, the one-shot holdout, evidence classes, browser-path leakage controls | P41; `cp2.regime.all.{n_obs,n_days}`; `claims.py` (`holdout_days`, `holdout_window`, `holdout_dm_label`, `wasm_availability_statement`) |
| 5 Results | "Measured results: the one-shot test" → `#product-results` | supported | The frozen artifact on its 90-day holdout (population `v1-holdout-90d`, class "confirmatory-style, not power-qualified"), kept apart from v1's development replay in the shared comparison | P42 with P11 reused; `claims.py` holdout claims; `cp20.metrics.{B1,B0}.equal_fold.{S_MAE,S_WIS}` |
| 6 Attribution | "What drives its forecasts: SHAP chart" → `#product-attribution` | supported | **The frozen artifact's own SHAP values**, median head, on fold 5's test block 2026-01-08..2026-04-07: rows it was fitted on, labelled an in-sample diagnostic. Fold 5's development model (out of sample) appears only as a comparison: the rank agreement in the text, its ranking beside the values, and the archive route | P43; `cp2.diagnostics.frozen_shap.<rank>.*` (class `in_sample_diagnostic`), `cp2.diagnostics.fold5_shap.<rank>.*` (development), `cp2.diagnostics.frozen_vs_fold5.{rank_spearman,top10_overlap}`, from `reports/cp2/diagnostics.json` (blob `0b53a8be…`); chart `product-shap` |
| 7 Importance and sensitivity | "Input importance and its limits" → `#product-importance` | supported | Permutation importance of **fold 5's development model** on its own test block, out of sample, labelled as such; SHAP/permutation rank agreement; the load control described as a ceteris-paribus probe, not causal value | P44; `cp2.diagnostics.permutation.<rank>.*`, `cp2.diagnostics.shap_vs_permutation.rank_spearman`; `claims.py` `SENSITIVITY_PROBE_LABEL` |
| 8 Where it fails | "Where it fails: errors by regime" → `#product-failures` | supported | **The released recipe's development folds** (a model fitted and calibrated per fold, not the frozen artifact), with day-block bootstrap intervals and the thin-subset qualification | P45; `cp2.regime.<stratum>.{mae,mae_ci95_low,mae_ci95_high,coverage_95,n_obs,…}` (10 strata) |
| 9 Reliability | "Interval reliability: coverage chart" → `#product-reliability` | supported | The frozen artifact's holdout coverage by calibration stage, and the development folds' coverage by stage; development widths; crossings; CQR's conditional guarantee | P46; `cp2.holdout.coverage.{raw,post_cqr,final}.{50,80,95}` (`holdout_report.json`, blob `43676b8f…`), `cp2.reliability.<stage>.<level>` (`reliability_three_stage.csv`, blob `3994e819…`), `cp20.metrics.B1.pooled.mean_width*`; chart `product-coverage` |
| 10 Forecast | "Read a forecast: interactive replay" → `#product-forecast` | supported | The frozen artifact's precomputed replay of a holdout day (the same payload as the preview and the archive), with level and load-scenario controls; the demo recomputes it in the browser, bitwise equal on the fixture | P47; `claims.py` (`REPLAY_LABEL`, `wasm_fixture_days`, `wasm_cold_load_mb`); `window.__FAN__` from `build_chart_payload`; chart `p-chart` |
| 11 Limitations | "Limitations" → `#product-limitations` | supported | v1's complete limitation set and the floor change | P48; `claims.py` `LIMITATION_KEYS`, `FLOOR_CHANGE` |
| 12 Running it | "Run this product" → `#product-run` | supported | Current verified commands for the released model and the browser proof; identity fingerprints; MLflow `delu-cp2`; the archived container text marked historical | P49; `claims.py` (`champion_fingerprint`, `snapshot_sha256`, `mlflow_experiment_url`); `predict_next_day.py`; `Makefile` `wasm`; `tests/test_22_wasm_equivalence.py`; `docs/deploy.md` |

**Gaps disclosed on the page, not filled:** the holdout report records coverage but no interval
width (P46 says so); the regime strata describe fold models, not the frozen artifact (P45 says so);
the only attribution of the frozen artifact is in-sample (P43 says so). No holdout was reopened, no
SHAP, permutation or bootstrap was rerun, and no data window was extended.

### 2.1 Content classification (plan P1.2)

| Class | Where it lives | Examples |
|---|---|---|
| Active product | `#product` topics | subjects 1–12 above |
| Shared | The opening and definitions | the forecast target, the scores' definitions, the release rule |
| Development-only | Labelled as such inside the topic that uses it | fold strata (P45), fold-5 permutation (P44), v1's development replay (P42) |
| Historical | The v1 archive `<details id="v1-archive">`, byte-identical to `af0abb0` | the original report, its figures, its container instructions |
| Planned | "Planned work", unscored and unnumbered | unchanged from PRES-1 |
| Obsolete operational description | Replaced in `docs/deploy.md`; marked historical in P49 | "awaits upload / template only"; hosted container |

### 2.2 Replacement contract (plan P1.6, §5.1 lifecycle)

A future released successor changes the registry's `released()` entry. The build then stops with
`ProductDocsError` until `PRODUCT_DOCS` holds a builder for that id whose topics cover all twelve
subjects with a disposition each (tested with a negative control). The fields the successor must
replace: its data contract (P38), regimes if its eligible data differ (P39), its input catalog (P40),
its validation design and evidence class (P41), its own results (P42), attribution and importance of
its own artifact with their populations (P43–P44), its failure strata (P45), its interval pipeline
(P46), its replay payload and demo bundle (P47), its limitations (P48), its commands and identities
(P49), and the demo's startup measurement record (P34). Shared text is kept only after an
applicability check; v1's topics remain as history. Nothing in the product section names "v1" in a
heading: the model is named from the registry (`{g:released.name}`).

## 3. Transitions (A3; packet template §5a)

Predecessors are registry data (`Entry.predecessor`), validated by `registry.transition_problems()`
(one start, predecessors are registered generations, no double successor, date order, no cycle), each
with a negative control in `test_43`. Neither is derived from a version number.

| Field | From v2 to v3: adding weather forecasts (P35) | From v1 to v2: a blended linear model with hour-aware intervals (P36) |
|---|---|---|
| Predecessor and dates | v2, adopted in research 2026-09-23; v3 adopted in research 2026-09-24 | v1, released 2026-09-15; v2 adopted in research 2026-09-23 |
| The change | wind at 10 m and 100 m and solar radiation forecasts, each with a missing-data indicator, added to v2's blend and intervals | LightGBM quantile model and fixed-window calibration replaced by an equal blend of two daily-refitted LEAR forecasts and hour-aware residual intervals |
| Comparator set in advance | v2 itself on identical hours (`H0` = `V2-H`): comparator is the predecessor | daily LEAR (`B2`), not the predecessor; a pooled-interval control isolated the interval method |
| Result, uncertainty, class | `derived.change.v3.S_MAE` −12% [−16%, −9%], `derived.change.v3.S_WIS` −14% [−17%, −11%], as a share of v2's score; development | `derived.change.v2.S_MAE` −2% [−4%, −1%], `derived.change.v2.S_WIS` −4% [−5%, −2%], as a share of daily LEAR's score; development |
| Against the predecessor | the comparison above is direct | **no paired v2 − v1 interval exists** (the protocol did not test that pair); descriptive context without an interval on the same hours: point-error 1.052 (v1) and 0.644 (v2), interval 0.986 and 0.616; v1's holdout is a different window and class and is not compared |
| Not established | no single weather input isolated; within the 2022 crisis the point-error gain is not demonstrated on its own | no attribution to hour-aware intervals alone; blend and interval layer not separated; no demonstrated joint preference against the pooled control |
| Decision and route | adopted in research, September 2026; "The comparison chart and its evidence, in the v3 chapter" → `#v3-chart-title` | adopted in research, September 2026; "The comparison chart and its evidence, in the v2 chapter" → `#v2-chart-title` |

## 4. Rejected branches and counts (§3.3, §4; plan §5.2)

The branch group is headed **"Experiments not adopted between v1 and v2"**: the calibration
experiment (CP-10; four adaptive and two scaled conformal arms against v1, not adopted 2026-09-16)
and the model comparison study (CP-15; five study challengers against daily LEAR, not adopted
2026-09-16), each a card with question, comparator, deciding result, "Not adopted", reason, date and
evidence. v2's pooled-interval control remains inside the v2 chapter. **No group was created between
v2 and v3**: no rejected experiment is documented there. The census distinction (P33) sits beside
the target line: the overview's rows are not the target census; the eight policies tested at the v3
decision (the five challengers, v2, its pooled control and v3, each once) come from the derived
decision records, and the row count from the registry's comparison. Tests assert the definition,
not a fixed count.

## 5. Chart routes (A5; packet template §5c)

Every explanatory result chart is reached from a visible, descriptive label with every disclosure
closed. The routes are generated from the headings that introduce each chart
(`explore_routes()`, `transition_card()`, `product_section()`), not a hand-kept index.

| Chart | Its heading | The route's label | Where the route starts |
|---|---|---|---|
| `product-shap` | `#product-attribution` | "What drives its forecasts: SHAP chart" | product routes |
| `product-coverage` | `#product-reliability` | "Interval reliability: coverage chart" | product routes |
| `p-chart` (replay) | `#product-forecast` | "Read a forecast: interactive replay"; "Explore this forecast" | product routes; the preview |
| `overview` | `#comparison-finding` | visible on the default page | the comparison section |
| `v3-c2a` | `#v3-chart-title` | "The comparison chart and its evidence, in the v3 chapter" | the v2→v3 transition summary |
| `v3-c2b` | `#v3-per-period-differences` | "Did weather help in every test period?" | v3 "Explore these results" |
| `v3-c3` | `#v3-absolute-errors` | "Absolute errors per test period, for v1, v2 and v3" | v3 "Explore these results" |
| `v3-c5` | `#v3-hours` | "Errors by hour of the day, v2 against v3" | v3 "Explore these results" |
| `v3-c4` | `#v3-crisis` | "What happened in the 2022 crisis window" | v3 "Explore these results" |
| `v3-c6` | `#v3-coverage` | "Did the intervals get more reliable, or only wider?" | v3 "Explore these results" |
| `v2-chart2` | `#v2-chart-title` | "The comparison chart and its evidence, in the v2 chapter" | the v1→v2 transition summary |
| `v2-chart1` | `#v2-control` | "What the pooled-interval control established, and the scores against the targets" | v2 "Explore these results" |
| archive `#chart` (replay) | `#forecast` | "The replay in the archived report" | the preview |
| archive figures | `#regimes`, `#spectral`, `#shap` | "…, in the archived report" | the product topics for subjects 2, 3b and 6 |
| `preview` | the opening panel | visible on the default page | the opening |

Plan §5.3's reader questions map as follows: overall comparison → `overview`; weather per period →
`v3-c2b`; absolute errors → `v3-c3`; by hour → `v3-c5`; the crisis → `v3-c4`; reliable or wider →
`v3-c6`; v2's control → `v2-chart1`; how the product works and fails → the twelve product routes. Every
chapter anchor of the PRES-1 page still exists (`#v3-per-period-consistency`, `#v3-stress-period`,
`#v3-coverage-and-width`, `#v3-method`, `#v3-protocol-and-review`, `#v2-protocol-and-review`, the chart
titles); the new headings inside those disclosures are added beside them. Old archive anchors (`#data`,
`#results`, `#forecast`, `#repro`, …) are unchanged; new product anchors use the `product-` prefix and
collide with none. The discovery check followed all 26 routes by mouse,
keyboard and deep link in both engines at 1440×900 and 390×844 (`pres-2-local-release-attempt-*.json`,
`discovery`).

## 6. Applicability matrix — PUBLISH_RULES 1.0

Category per §1.3: **Inh** inherited (v1 or surviving plan clause), **Am** amendment, **Fut** future
trigger, **Hist** historical example. "Evidence" names where compliance is shown; the full local
acceptance matrix is `acceptance.md`.

| Clause | Category | Applies to PRES-2 | Treatment and evidence |
|---|---|---|---|
| §1.1 sources and precedence | Inh | yes | Pinned hashes in §1 above and `baseline.md`; no governing file edited (exact-copy baseline only) |
| §1.2 four identities | Inh | yes | Rule revision, generation, product status and artifact identities kept apart: registry, `baseline.md`, the return |
| §1.3 applicability categories | Inh | yes | This matrix |
| §2 reader contract and placements | Inh + A1/A2 | yes | Headline block visible without scrolling in both engines at 1440×900 and 390×844; definitions beneath; product identity beside the action; A2 below (`release` records, `placements`) |
| §3.1 evidence classes; W1–W21 | Inh | yes | Class badges on every result; product topics label development, one-shot and in-sample evidence; lint (`lint_publication.py`) and withheld-phrase tests |
| §3.2 scores, comparisons, fairness | Inh | yes | Scores named; changes as a share of the named comparator with 95% intervals; "10,747 historical hours over 448 days" visible (F04, P07); EUR/MWh context separate |
| §3.3 counting | Inh | yes | P33 census distinction; tests assert the definition (`test_43`) |
| §3.4 provenance and formatting | Inh | yes | Every product number bound to a record (`test_30` backstop, `verify_release.py`); precision rules in the claim layer |
| §4 registry, transitions (A3), branches | Inh + A3 | yes | §3–§4 above; `registry.transition_problems()` with negative controls |
| §5 page order (A4) | Am | yes | Order opening → product → comparison → journey → chapters → planned → evidence → contribution → attribution (`test_43` order test; `build_html`) |
| §5.1 twelve subjects and lifecycle | Am | yes | §2 above; `ProductDocsError` contract |
| §5.2 chapter grammar, 2.0 MB | Inh | yes | Chapters unchanged in grammar; page 1,684,252 bytes |
| §6 charts, discovery (A5) | Inh + A5 | yes | §5 above; chart text ≥ 12 px at 390 and 320 px measured by each text's screen transform; `charts` and `discovery` records |
| §7.1 product and demo contract | Inh | yes | Startup measurement beside the action, outside any disclosure (F03, P34); demo states; named controls (F01) |
| §7.2 future live, A7 | Fut / Am (conditional) | **no — deferred** | No live panel, schedule or promotion; trigger: an authorized live product meeting §7.2 and the research protocol |
| §8 surfaces and links | Inh | yes | README, both Space cards, demo claims and MLflow agree (`verify_release.py`); links gate (`pres-2-links-*.json`); `.mlflow` host only |
| §9 browser, accessibility, interaction | Inh | yes | Chrome and WebKit, five widths plus emulated iPhone; AX trees; keyboard; touch; contrast; zoom/reflow; demo widgets (`acceptance.md`) |
| §10.1 independence | Inh | yes | Integration Critic who authored nothing, detached checkout at the final candidate (`integration.md`) |
| §10.2 fresh reader | Inh | yes | `fresh-reader.md` |
| §10.3 public identity (A6) | Am | **local part only** | Public identity and pre-publication public observations recorded; the post-deployment checks are P8, after the Owner publishes |
| §10.4 verdict | Inh | yes | `integration.md` |
| §11 packet and sequence | Inh + A3–A5 fields | yes | This packet; `publication-packet.md`; no MLflow upload needed (export unchanged) |
| §12 baseline coverage map | Inh | yes | Invariants 1–26 carried; invariant 10 (date boundary) unchanged; 13 (`pyproject.toml`, `uv.lock` untouched); 14 (no retired-tooling narrative); 24 (archive byte-identical) |
| §13 acceptance record | Inh | yes | `acceptance.md` with this matrix |
| §14 maintenance and triggers | Fut | no trigger met | v4, v5 or size breach, final-candidate test, Live: none reached |
| §15 A1 | Am | yes | Headline: "…(v3: 14% below on the point-error score and 17% below on the interval score; …)" (P20 amended) |
| §15 A2 | Am | yes | `placement_findings()` uses N×H−(N−1)×h with the largest header seen; limits 1744 (desktop) and 2420 (phone) at h = 56 px; consecutive captures kept |
| §15 A3 | Am | yes | §3 above |
| §15 A4 | Am | yes | §2 above |
| §15 A5 | Am | yes | §5 above |
| §15 A6 | Am | local part now; public part at P8 | `publication-packet.md` §P8 lists the commands and records |
| §15 A7 | Am (conditional) | deferred | as §7.2 |
| §16 authority record | Hist | no action | Nothing in PRES-2 edits governance |
| §17 source identities | Inh | yes | Runbook and packet template changed under plan P4.8 (not locked); their new hashes are in the return |
