# Final-product Space plan — from a frozen demo to a daily product tool

> **Work-availability amendment, Owner-authorized 2026-10-10.** Scheduling restrictions
> have been removed under `AGENTS.md` § Work availability. Historical hashes and reviews
> bind the prior text at `522d7ea:docs/track-b/final-product-space-plan-2026-09-30.md`; they do not bind this amended copy.

**Orchestrator planning document, 2026-09-30, written at the Owner's request. Not an execution
brief.** It plans how the Hugging Face Space becomes the final product's useful, informative
tool: trained and updated daily, with the Owner's panels and analyses. It executes as part of
the final product's rollout (CP-17 freeze, CP-18 daily operation), not now.

The binding parts are anchored by authority (§5):

- **What the Space computes and claims** is anchored in research
  [`capstone_v21.md` v21-r8 §19](../../capstone_v21.md).
- **How it is presented and accepted** is anchored in publication
  [PUBLISH_RULES 1.2 §7.3 and A9](../PUBLISH_RULES.md).
- **Owner-only decisions and authority** stay with the Owner (§5.1). This plan grants none of
  them.

**Inputs.** This plan was built only from the contracts, rules and anchors. On the Owner's
instruction, the current Space, the site and the demo code were not inspected: they predate
PRES-3 and are out of date. Every requirement below traces to a governing text or to the Owner's
request.

| Source read | Identity at reading |
|---|---|
| `capstone_v21.md` v21-r7 (§§2, 8–10, 16, 18) | `e6a4e301…` |
| PUBLISH_RULES 1.1 (all) | `91eea445…` |
| Presentation and tracking plan, revision 3 (§§6–7, 8.1, 15) | `28119374…` |
| Publication Standard v1 (§§2, 16–17) | `01d721c2…` |
| Publication runbook (§§1, 1a, 7a, 7b, 9) | `b5d00008…` |
| Publication packet template (§§5b, 5d, 8) | `4efb0185…` |
| Programme handoff (4.9O, 4.9, §5) | `cf498c44…` |
| `AGENTS.md` (Git and publication authority, credentials) | at `6f4575b` |

---

## 1. The Owner's request

On 2026-09-30 the Owner wrote (quoted in full in the
[v21-r7 → v21-r8 amendment record](capstone_v21-r7-to-v21-r8-amendments.md)):

> הספייס נראה כרגע מעפן ולא אינפורמטיבי. חייבים לשפר אותו משמעותית כשיש מוצר חי. תסקור אותו
> ואת הכללים כרגע ותנסה לבנות תוכנית כיצד אנחנו עושים ממנו באמת כלי שימושי ואינפורמטיבי
> שתעוגן Split by authority ותמומש ברגע שיהיה לנו מודל סופי.

In English: the Space currently looks poor and uninformative. It must improve substantially once
there is a live product. Review it and the current rules, and build a plan to make it a genuinely
useful and informative tool, anchored split by authority, to be implemented as soon as there is a
final model.

**What the Owner asked the Space to show:**

| # | Owner's item | Where this plan specifies it |
|---|---|---|
| 1 | A reproduction and demo trained and updated daily: today's price and how accurate it was in percent; tomorrow's price and how sure the model is | §4.3 product panel |
| 2 | A "Train it yourself" button | §4.4 |
| 3 | Panels "Today: issued forecast against published price" and "Tomorrow: forecast with intervals"; rolling coverage and width; a percentage measure defined in advance beside MAE; training, refresh and issuance times shown separately, as §16.3 and A7 require | §4.3 |
| 4 | Data analyses: price distribution, negative hours, hourly profile and regimes, computed from the shipped series | §4.10 |
| 5 | Feature analyses: the selected day's feature values against history, and importance by gain read from the model files, worded as attribution, not causality | §4.9 |
| 6 | Validation: every evaluation day recomputed in the browser (MAE, pinball, coverage and width against the similar-day naive), ending in a "matches the stored value ✓" row; development folds shown statically from evidence | §4.6 |
| 7 | Explainability | §4.8 |
| 8 | Reliability and confidence measures: a reliability diagram for every emitted quantile, rolling coverage and width, PIT; always the nominal level against the measured coverage, never "X% confidence" | §4.7 |
| 9 | Forecast | §4.5 |
| 10 | Limitations | §4.11 |
| 11 | Follow the current publication rules on design and focus, and adapt the Hugging Face update to the site's UI/UX line | §§3, 4.1–4.2 |
| 12 | Assess the Headline Arena message received on the Space | §9 |

Two items need care to fit the evidence rules:

- **Item 6's "90 holdout days"** belongs to v1. v1's holdout is spent and stays v1 history. For
  the final product, the same recomputation runs over its own evaluation windows: the one-shot
  fresh-data test (4.7T) and the prospective record, which reaches at least 90 consecutive
  delivery days at CP-19 (§4.6).
- **Item 8's "nine quantiles"** is v1's count. v2 and later policies emit seven levels (.025,
  .10, .25, .50, .75, .90, .975). The diagram covers every level the final product actually emits.

---

## 2. What the contracts already require

The final product already carries a demanding contract. The Space has to satisfy all of it:

| Requirement | Source | What it means for the Space |
|---|---|---|
| One identity for final version, product, primary demo and daily policy | research §16.1; PUBLISH_RULES A8, §5 | The Space serves the designated final product only. An old replay may stay as labelled history, never as a second primary product. |
| Daily retraining, input refresh and issuance, with dated, lineage-bearing artifacts | research §16.2; handoff 4.9O | Every served forecast names the daily artifact that issued it. Context or input refresh alone is not training. |
| Today's issued forecasts against published prices; a percentage measure beside MAE; tomorrow's forecasts and intervals; coverage with width; separate training, refresh and issuance times; stale, failed and pending states | research §16.3; PUBLISH_RULES §7.2 (A7); packet §5d | The product panel's fields. Scoring uses the forecast actually issued, never a newer fit. |
| No "X% correct" and no confidence percentage; nominal level distinguished from measured coverage | research §16.3; PUBLISH_RULES §7.2 | Wording rules for every panel (§6). |
| The twelve product subjects, documented for the actual product | PUBLISH_RULES §5.1 | The Space's analyses must agree with the report's product documentation (§8 parity). |
| Demo states (ready, loading, failure, retry), startup metadata beside the action, accessible controls | PUBLISH_RULES §7.1; plan §7.11 | Every Space view and every long computation, the retrain included. |
| The browser and accessibility matrix, including framework widgets | PUBLISH_RULES §9 | Applies to every Space view and control. |
| Hugging Face is a required destination; served identity verified per release and daily | runbook §1a; packet §8 | The daily pipeline must deliver each admitted artifact to the Space and verify what it serves. |
| "Do not assume a browser-only WASM demo can retrain or refresh itself automatically" | runbook §7b | The Space never fetches or trains on its own schedule; a delivery pipeline publishes each day. |
| Before Live: publication authority, daily coverage, `delu-live`, the registry model, an extended `test_24`, a live claim builder and a demo concept for daily weather inputs | PUBLISH_RULES §7.2; Standard v1 §16 | Prerequisites of CP-18, carried into §7 of this plan. |
| Daily data-only updates need an `AGENTS.md` amendment by the Owner or an Owner-run push | Standard v1 §16 | Unattended daily publication is an Owner authority decision (§5.1). |
| Evidence classes are never pooled; development, one-shot and prospective stay separate | PUBLISH_RULES §3.1 | Validation and reliability views keep the classes apart (§4.6). |
| No data after 2026-04-07 in research numbers or charts before the final test | Standing decision, 2026-09-24 | Governs which dates the data and feature views may show before 4.7T (§4.10). |
| DDNN, if chosen, is one NumPy implementation behind every number | research §18.2 | Keeps the in-browser retrain possible for DDNN too. |

---

## 3. Gaps: what is missing or needs fixing

| # | Gap | Why it matters | Resolution |
|---|---|---|---|
| G1 | No contract for the Space's content beyond demo states and startup metadata | The Owner's analyses, validation and reliability views have no specification, so a future build could ship any subset | PUBLISH_RULES 1.2 §7.3 (A9) defines the required views |
| G2 | In-browser retraining is not required anywhere; v21-r7 §18.2 deferred it | The "Train it yourself" button needs a semantics, an equality claim and an exception route | Research v21-r8 §19.3 makes it a delivery requirement, as the Owner decided |
| G3 | No definition of in-browser recomputation of the final product's evaluation, or of a "matches stored value" check | v1 proved inference identity in the browser; the final product needs the equivalent for its scores | §19.5–19.6 |
| G4 | The percentage measure is required but has no formula, tolerance or denominator | Without a frozen definition, the number could be chosen after the results | §19.5 requires CP-17 to freeze it before 4.7T; §4.3 proposes a candidate; the Owner decides the tolerance |
| G5 | No definition of the reliability diagram, the rolling window or PIT for quantile forecasts | "Confidence" displays drift easily into misleading claims | §19.5 defines them; CP-17 freezes the window lengths |
| G6 | No method for feature importance or attribution per model component | The final model may blend linear, tree and neural components, whose honest methods differ | §19.7 fixes the method by component class; CP-17 freezes the neural method if one is used |
| G7 | No authority for unattended daily publication to the Space; no delivery design | Without it, "updated daily" is not lawful or not true | Owner decision at CP-18 (§5.1); delivery design in §4.12 and CP-18's brief |
| G8 | The data and feature views could silently cross the date boundary before the final test | Standing decision of 2026-09-24 | §19.8 ties their date range to the boundary and to live operation |
| G9 | No size budget for a Space that also carries training inputs and a larger runtime | The first visit would grow, silently | A9 requires lazy loading of the retrain payload, with its size disclosed before loading |
| G10 | The live namespace test (`test_24`) and the claim builder do not cover live or Space values | Live values from another source would bypass the guards | CP-18 acceptance (§7) |
| G11 | v1's replay, its bitwise identity check and its four cutoffs would become history | An outside reader singled out exactly that discipline (§9); losing it would lose the page's strength | A9 keeps a labelled history route and carries the discipline forward: served identity, equality checks and separate dates |
| G12 | The final model is not yet chosen (v4 now; DDNN in 4.6; possibly recombination in 4.8) | The plan must hold for a LEAR/LightGBM blend and for a NumPy network, with seven or nine quantiles | Every specification here is by component class and emitted levels, not by one model |

---

## 4. Target design: the Space as the product's daily tool

### 4.1 Principles, taken from the site's UI/UX line

The Space follows the same line as the report: **a product-led research case study with precise
analytical components** (plan §7.1). Concretely:

- **Plain names first.** "v4 · three-block LightGBM added" style names from the registry; codes
  such as `HGL` only as secondary metadata. The product's status comes from the registry.
- **Analytical panels** (plan §7.5): a title that states the question or finding; a subtitle
  with metric, comparator, population and evidence class; direct labels with units; the chart
  with its reference line; one finding, one qualification and the evidence route.
- **Controls only when they change a real view.** Tabs switch real views; a day picker offers
  only days with an issued forecast. No date picker over a fixed evaluation window, no
  decorative tabs, and no disabled buttons for features that do not exist (plan §7.13).
- **Nothing depends on colour or hover.** Values, caveats and sources are visible. Generation
  colours always come with direct labels and marker shapes; v4 is amber `#B45309` with a filled
  diamond (standing decision, 2026-09-29).
- **Visual tokens** as the report: canvas `#FAFAFA`, surface `#FFFFFF` for analytical panels,
  text `#18181B`, secondary `#52525B`, accent `#1D4ED8`, a dark primary action, one primary
  action per view; the system font stack, tabular numerals, the spacing scale and the
  typography sizes of plan §7.3. No remote fonts, dark mode, animated counters or scroll
  effects.
- **Mobile variants, not shrunk desktop charts.** Chart text at least 12 px at 390 px; touch
  targets about 44 px; reflow at 320 px.
- **Honest states everywhere:** ready, loading, pending, partial, stale, failed, unavailable,
  retry, each with a route back to the report. Progress only as the runtime reports it.

### 4.2 Information architecture

The Space opens on the product panel, then offers the analyses as real views:

| Order | View | The question it answers |
|---|---|---|
| 1 | **Product panel** (always first, not a tab) | What is today's price, how close was the forecast, and what is tomorrow's forecast with its uncertainty? |
| 2 | **Train it yourself** | Can I reproduce today's daily model on my own machine? |
| 3 | **Forecast** | What did the product issue for a given day, and what happened? |
| 4 | **Validation** | How well does the product score, recomputed here from its own records? |
| 5 | **Reliability** | How often do the intervals hold, and how wide are they? |
| 6 | **Explainability** | What drove this forecast, by model component and by input? |
| 7 | **Features** | How unusual are today's inputs, and which inputs does the fitted model use most? |
| 8 | **Data** | What does the price series look like: distribution, negative hours, hourly profile, regimes? |
| 9 | **Limitations** | What the product cannot do, from the same claim layer as the report |
| — | **History** (a labelled route) | v1's frozen demo, its replay and identity check, as history |

The views are an accessible tab list with keyboard arrows, `aria-selected` and deep links
(`#validation`), so a report route can open a view directly (A5).

### 4.3 The product panel: today, tomorrow and how sure

Every field below is required by research §16.3 and PUBLISH_RULES §7.2 (A7). The Space shows
them first.

**Identity and time strip:**

- **Product:** version and status from the registry, for example "v4 · … · Final product ·
  Prospective · N days". It says "prospective evaluation in progress" until CP-19.
- **Daily artifact:** the identity of the fit that issued the forecasts shown.
- **Three separate times:** last successful training; last data refresh; forecast issuance.
  Also the information cutoff, the delivery dates and the timezone (Europe/Berlin).
- **Freshness state:** current, stale since a date, or failed. A failed or skipped fit is shown
  as such even when a valid fallback issued the forecast (research §16.2).

**Today: issued forecast against published price.**

- The chart shows the hourly forecast issued before the auction for today's delivery hours. It
  sits against the published hourly prices available so far. Hours still pending are marked
  and unscored.
- **Score, with its population named:**
  - the frozen percentage measure, over today's scored hours;
  - MAE in EUR/MWh over the same hours;
  - the number of scored hours out of the day's canonical 23, 24 or 25, as partial-day
    completeness.

  With no scored hour yet, it shows "not yet scored", never 0% or 100%.
- **Proposed percentage measure,** to be frozen at CP-17 before 4.7T: *the share of scored
  hours whose absolute error is within ±τ EUR/MWh.*
  - An absolute tolerance behaves correctly for zero and negative prices, which break
    percentage errors.
  - τ is a use-case tolerance fixed by the Owner before any evaluation, not fitted to results.
  - It is labelled "within ±τ EUR/MWh", never "correct".
  - Benchmark-relative figures are labelled as improvement.

**Tomorrow: forecast with intervals.**

- The chart shows the issued hourly p50 with the nominal bands the product emits. With seven
  levels these are 50% (.25–.75), 80% (.10–.90) and 95% (.025–.975). Before issuance, or on
  failure, it shows a dated pending or unavailable state.
- **"How sure", honestly.** Next to the bands:
  - **Nominal level:** "80% interval (nominal)".
  - **Measured coverage and width:** over a named past window, for example "over the last 28
    scored delivery days, 81% of hours fell inside the 80% intervals; mean width 41 EUR/MWh".
    These numbers are illustrative; the window length is frozen at CP-17.
  - No sentence claims a probability that the point price is right.

**Reliability strip:** measured coverage together with width for each nominal band, over the
named rolling window. It links to the Reliability view.

### 4.4 Train it yourself

The Owner's button. Research v21-r8 §19.3 fixes its meaning; A9 fixes its presentation.

**What it does:**

1. It retrains, in the visitor's browser, the daily fit of one issued delivery day (default:
   today's). It uses that fit's shipped training window, the same code, the same seed and the
   same selection rules.
2. It predicts that day's hourly quantiles with the retrained model.
3. It compares the retrained model with the issued artifact on three points:
   - whether every data-driven selection matched (for example the Lasso penalty and the
     LightGBM capacity);
   - the largest absolute difference in each emitted quantile, in EUR/MWh;
   - a status stating only what was measured: **identical bit for bit**, **within the frozen
     tolerance of ±τ_eq**, or **different**, with the numbers.
4. It never replaces or rescores an issued forecast. The retrained result is labelled "your
   retrained model", never "the forecast".

**How it is presented:**

- Before the action: the extra download size of the training payload, the measured time on a
  named reference device and browser, and the date of that measurement (PUBLISH_RULES §7.1).
  The training payload loads only on request.
- During the run: only the stages the runtime actually reports, for example "fitting component
  2 of 4". No invented percentage. A cancel control.
- After the run: the three results above, plus the runtime on the visitor's machine. There is
  a route to the artifact's lineage record and to "how this is checked".
- On failure: the failure state, the reason when known, retry, and the route back.

**Why it is feasible.** Pyodide provides NumPy, scikit-learn and LightGBM, which the current
product family uses. DDNN is NumPy-only by research §18.2. CP-21 measured v4's cold daily cycle
at a median of 24.7 s and a maximum of 69.4 s on the M3 with four processes. The browser runs a
single process, so its time is unmeasured and must be measured (§7, CP-17 step 2). Equality
between the browser and the native run is not assumed; §19.3 makes the claim a measured one.

### 4.5 Forecast

- **Day picker:** only days with an issued forecast in the served record, defaulting to the
  latest.
- **Chart:** the issued p50 and nominal bands; the published outcome where available; pending
  hours marked. The panel grammar of plan §7.5 applies.
- **Labels:** "issued at <time> by artifact <id>" for real forecasts. Any interactive what-if
  control is labelled "counterfactual scenario — not an issued forecast" (research §16.3).
- **History:** v1's replay stays behind the History route, labelled historical replay.

### 4.6 Validation — recomputed in the browser

Three evidence classes are kept apart, never pooled into one number or chart (PUBLISH_RULES §3.1):

| Window | Source | Computation | Badge |
|---|---|---|---|
| Development folds | Committed evidence of the product's research evaluation | Static, from the evidence records | Development · post-selection |
| One-shot fresh-data test (4.7T) | The frozen test's issued forecasts and outcomes, shipped with the Space | Recomputed in the browser | As 4.7T's protocol fixes it |
| Prospective record | Every issued daily forecast since the run start, with reconciled outcomes | Recomputed in the browser, growing daily | Prospective · N days; "evaluation in progress" until CP-19 |

**For each recomputed window**, the browser computes:

- MAE in EUR/MWh;
- pinball loss and the interval score as the protocol defines them;
- per nominal band, coverage together with mean width;
- the same metrics for the similar-day naive, as context. The naive is labelled as a reference,
  not a target.

Counts are shown: days, hours, and failed or late issuances, which stay in the record.

**Last row: "Matches the stored value".** Each recomputed metric is compared with the committed
evaluation record of the same window. Integer counts must match exactly. Real-valued metrics
match within a tolerance frozen at CP-17; a proposed value is a relative error of 1e-9, since
the code and records are the same. The row shows ✓ with the compared values, or ✗ with both
values. A mismatch is shown, never hidden, and blocks the day's publication as a product
failure (§19.5).

v1's 90-day holdout is not in this view. It stays in v1's history route with its original
label, "confirmatory-style, not power-qualified".

### 4.7 Reliability — nominal against measured, always

- **Reliability diagram:** for each emitted quantile level q, the observed share of outcomes at
  or below that quantile forecast, against q, with the count of scored hours. The window is
  named and the evidence classes are separate. It uses points with counts, not a smooth curve.
- **Rolling coverage and width:** for each nominal band, coverage over a rolling window of scored
  delivery days, plotted together with the band's mean width over the same window. The window
  length is frozen at CP-17; 28 days is proposed, matching v3's 28-day residual window. The
  nominal level is drawn as a labelled reference line, not a target.
- **PIT, defined for quantile forecasts:** the share of outcomes in each band between adjacent
  emitted quantiles, against that band's nominal share. With seven levels there are eight
  bands. It is labelled as a quantile-band PIT histogram, with counts; no continuous PIT is
  claimed.
- **Wording:** "nominal 80% interval; measured coverage 81% over <window>; mean width <w>
  EUR/MWh". Never "80% confidence" or "the model is 80% sure".

### 4.8 Explainability — attribution, not causes

The methods follow research §19.7, by component class:

| Component | Method | Exactness |
|---|---|---|
| The blend | Each component's weight times its forecast | Exact decomposition of the central forecast |
| Linear components (LEAR, Lasso) | Coefficient times the input's deviation from its training mean, in the model's standardized space | Exact for the linear model |
| Tree components (LightGBM) | Per-prediction contributions (TreeSHAP) from the fitted model | Exact for the fitted trees |
| A neural component (for example DDNN), if chosen | A method fixed at CP-17 and computed from the frozen artifact | As stated by that method |

- **View:** for the selected day and hour, the forecast decomposed into its components, then
  each component into its largest contributions, with units in EUR/MWh and a baseline stated.
- **Wording:** "contributed +x EUR/MWh to this forecast, relative to the model's baseline". It
  never says "caused" or "drives the price", nor claims incremental value, since a contribution
  within a fitted model is not the value of adding that input (PUBLISH_RULES §5.1, subjects 6–7).
- The interval layer is explained in words: how intervals come from recent errors by hour of the
  day, where that is the product's method. There is no fake per-feature attribution of
  interval width.

### 4.9 Features

- **Today against history:** for the selected day, each input's value, its percentile within the
  daily fit's training window, and a compact distribution with that day marked. Weather inputs
  carry their GFS attribution and missing-indicator state.
- **Importance, read from the fitted artifact:**
  - for tree components, gain importance read from the model files;
  - for linear components, standardized coefficient magnitudes;
  - for a neural component, the CP-17 method.

  Each is labelled with the component, the fitted artifact and its date.
- **Wording:** "how much this fitted model relies on each input". This is not causality and not
  incremental value. A rank is a property of one fitted artifact, not a permanent truth, and it
  changes with daily refits.

### 4.10 Data

- **Views:** price distribution, with negative hours and the floor marked; negative-hour counts
  by period; the hourly profile by season or regime; the regimes with their periods.
- **Computation:** in the browser, from the shipped hourly price series (the series payload,
  `series.json` in the current bundle design; the name follows the implementation).
- **Definitions shown where used:** hourly prices are the mean of four quarter-hour prices from
  2025-10-01, so hour-level counts differ from quarter-hour counts. The price floor moved to
  −600 EUR/MWh from 2026-05-28.
- **Date range:** before the final test, no research chart uses data after 2026-04-07 (standing
  decision). After the final test and from CP-18, the view runs through the latest published
  day, labelled with its last date.

### 4.11 Limitations

Generated from the same claim layer as the report and the README (invariant 5,
PUBLISH_RULES §8): the data assumptions, failure modes, regime and environment shifts,
operational limits, and the product's own adverse results. There is no hand-written copy.

### 4.12 What the daily pipeline delivers to the Space

The Space computes nothing on a schedule and fetches nothing from data sources. Each day, the
authorized pipeline (§5) publishes a dated bundle:

| Payload | Content | Loaded |
|---|---|---|
| Manifest | Every served file with its SHA-256; product and policy identity; daily artifact identity; the three times; freshness state | At start; the page verifies the hashes and shows the served identity |
| Issued forecasts | Every issued day's hourly quantiles with issue time and issuing artifact | At start |
| Outcomes | Reconciled published prices with source, publication and revision times | At start |
| Evaluation records | The committed metric records that the recomputation must match | At start |
| Fitted artifact | The day's model files (for example LightGBM text, NumPy arrays and coefficients) | For Explainability, Features and Train it yourself |
| Training window | Inputs and targets of the day's fit window, with the GFS aggregates | Only on "Train it yourself", with its size disclosed first |
| Series | Hourly prices for the Data view | For Data |

- **Runtime rule:** the Space loads its pinned runtime and its own served files only. There are
  no runtime calls to ENTSO-E, SMARD, GFS, the registry or MLflow. The report's
  no-runtime-network rule is unchanged.
- **Licensing:** CC BY 4.0 data and GFS-derived aggregates may be redistributed with attribution
  (`DATA-LICENSE.md`). No raw GRIB and no credentials are shipped.

---

## 5. Split by authority

### 5.1 The Owner

| Decision | When | Status |
|---|---|---|
| Require "Train it yourself" for the final product, with an exception route | 2026-09-30 | **Decided** by the Owner's request; anchored in research §19.3 |
| Anchor this plan (research §19, publication A9, this document) | 2026-09-30 | **Authorized** for this task ("יש לך אישור לבצע כל מה שאתה צריך") |
| Designate the final version | After 4.7T and the final 4.7 | Open |
| The percentage tolerance τ, from §4.3's proposal | At CP-17, before 4.7T | Open |
| The equality tolerance τ_eq, after the feasibility probe measures the browser | At CP-17 | Open |
| An exception, if the designated model cannot be retrained in the browser within the measured limits, with its public wording | At CP-17, only if needed | Conditional |
| **Unattended daily publication authority:** an `AGENTS.md` amendment naming the automation, the surfaces (Space, and the report if regenerated), the credential use, and the daily coverage | At CP-18, before launch | Open; Owner-only (Standard v1 §16; `AGENTS.md`) |
| Where the daily pipeline runs (§8) | At CP-18 | Open |
| Visual approval of the new Space | Before its first publication | Open; presentation is the Owner's |
| The reply to Headline Arena (§9) | Any time | Open; recommendation in §9 |

### 5.2 Research anchor — what the Space computes and claims (v21-r8 §19)

- One code path from the daily pipeline to the browser, with an exception route (§19.2).
- "Train it yourself": its meaning, its measured equality claim and its infeasibility route
  (§19.3).
- The daily delivery rule: the Space serves the issued forecasts and the artifact that issued
  them; there is no rescoring by a newer fit (§19.4).
- Metric definitions to freeze at CP-17: the percentage measure, the rolling windows, the
  reliability diagram, the quantile-band PIT and the recomputation tolerance (§19.5).
- Validation windows, kept by evidence class (§19.6).
- Attribution and importance methods by component class (§19.7).
- The date range of the data and feature views (§19.8).

### 5.3 Publication anchor — how the Space presents and is accepted (PUBLISH_RULES 1.2 A9)

- The required views and their order (§4.2 above), each a real view.
- The panel grammar, tokens, typography, states, startup metadata, mobile variants and
  accessibility, as on the report.
- Wording: nominal against measured; the percentage measure named by its tolerance; attribution,
  not causality; issued, retrained and counterfactual labels; evidence badges.
- The runtime rule and the payload loading rule.
- Acceptance: the §9 matrix on every view; recomputation rows pass on the served bundle; served
  identity equals the intended daily artifact; negative controls; A6 public checks.

### 5.4 Orchestrator — sequencing and briefs

- **The CP-17 brief** carries §19's freeze fields and the feasibility probe (§7).
- **The CP-18 brief** carries A9 and this plan's §7 checklist as controlling acceptance, and
  requests the Owner's `AGENTS.md` decision before launch.
- **Publication briefs** pin PUBLISH_RULES 1.2 from now on. A9 is conditional on A8's trigger,
  so it does not apply to PRES-3, which publishes v4 as research.
- Progress records and the programme handoff point here.

### 5.5 Engineering Lead — implementation, inside each authorized checkpoint

- **CP-17:** measure browser feasibility for the designated model and freeze the fields, then
  register the policy.
- **CP-18:** build the daily pipeline, the payloads, the Space views, the contract tests and the
  negative controls, then pass independent review.
- **The runbook** gains its Space touchpoints in CP-18, when the code exists. `test_42` resolves
  every `file::symbol`, so they cannot be written earlier.

### 5.6 Independent checker

- The exact-candidate review of the Space build under A9.
- Public post-deployment checks (A6) of the served Space: identity, views, states and controls.
- The daily-operation checks of research §16.4 and packet §5d.

---

## 6. Wording rules, with examples

The numbers below are illustrative, not results.

| Say | Never say |
|---|---|
| "Of today's 17 scored hours, 13 were within ±τ EUR/MWh of the published price; MAE 8.4 EUR/MWh." | "Today the model was 76% correct." |
| "80% interval (nominal): 62–118 EUR/MWh. Over the last 28 scored days, 81% of hours fell inside the 80% intervals; mean width 41 EUR/MWh." | "We are 80% confident the price will be 90 EUR/MWh." |
| "Prospective · 34 days · evaluation in progress" | "Validated in live use" |
| "Your retrained model is within ±τ_eq of the issued artifact (largest difference 0.0003 EUR/MWh)." | "Identical" when the check was not bitwise |
| "Wind speed contributed −12 EUR/MWh to this forecast, relative to the model's baseline." | "Wind caused the price to fall." |
| "Gain importance in today's fitted model" | "The most important driver of electricity prices" |

---

## 7. Automatic execution at the final-product rollout

Nothing here needs a new decision later, beyond §5.1's open items. The anchors make the Space a
required part of the final product's rollout: research §16 and §19 bind CP-17 and CP-18, and
publication A8 and A9 bind the release. Every future brief pins both.

**The checklist the CP-17 and CP-18 briefs carry:**

1. **Designation (Owner).** Record the final version. Its evidence class and product identity
   drive every Space label.
2. **Feasibility probe (CP-17, before the freeze).** Train one delivery day of the designated
   policy under Pyodide in Chromium and WebKit, on development data only. Measure:
   - time and peak memory;
   - the first-visit and training-payload sizes;
   - the deviation from the native fit, bitwise or not;
   - whether the selections match.

   If this is infeasible, return a blocker for the Owner's §19.3 decision. This can also run
   earlier, as a bounded probe with its own brief, to de-risk the button.
3. **Freeze (CP-17):**
   - τ (Owner), the percentage formula, denominator and partial-day rule, and zero or negative
     handling;
   - the rolling window lengths, the PIT and diagram definitions, and the recomputation
     tolerance;
   - τ_eq (Owner) and the reference browser and runtime;
   - the attribution method for any neural component;
   - the payload schema and manifest.
4. **Daily pipeline (CP-18):**
   - acquire, validate, fit and issue before the gate;
   - build the dated bundle and verify it (hashes, schema, recomputation rows);
   - publish it to the Space and verify the served identity;
   - reconcile outcomes later and update the records.

   Failures and staleness stay visible, and every delivery day is covered, including DST days. This needs the Owner's `AGENTS.md` authority first.
5. **Space build (CP-18):** §4's views under A9, from the payload only, with the History route
   for v1.
6. **Tests (CP-18):**
   - an extended `test_24` (the live namespace);
   - a live claim builder;
   - payload contract tests;
   - negative controls: a tampered file is detected; a pending outcome stays unscored; a stale
     artifact is shown as stale; a mismatched recomputation shows ✗ and blocks publication; a
     retrain with a changed seed is reported as different; a counterfactual is never labelled
     issued.
7. **Review and release:** the independent exact-candidate review; the packet with §5d and A9
   rows; the Owner-authorized launch; public A6 checks of every view.
8. **Operation:** "prospective evaluation in progress" until CP-19 closes after at least 90
   consecutive delivery days.

---

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Browser training is too slow or too heavy | Probe first (§7 step 2); lazy-load the training payload; disclose size and time; Owner exception route |
| Browser and native fits differ | The claim is measured, with τ_eq. Option: run the official daily fit in the same WebAssembly runtime, to be measured at CP-17 |
| Daily publication fails (outage, 429, credentials) | The stale or failed state shows; retries are logged; the served identity is checked every day; no silent reuse of an old success |
| The first visit grows | Only the manifest and the day's records load at start; the rest loads on demand; sizes are disclosed |
| Unattended publishing leaks a secret | The secret guard, the deploy script's bundle-hash refusal and value scanning apply to every daily upload; the policy code is reviewed once, and daily data passes automated validation |
| Confidence wording drifts | A9 wording rules, backed by the existing lint (§4) and a new lint for the Space |
| Where the daily job runs | Options for CP-18: the Owner's machine unattended, or GitHub Actions. A free Actions schedule is not relied on for a hard deadline (lesson of 2026-09-24); it can serve as a monitored backup. The Owner decides |

---

## 9. The Headline Arena message

**What it says.** An operator of Headline Arena praised the Space's discipline and invited the
project to submit daily forecasts. Headline Arena is a public arena where agents submit daily
forecasts that are settled against outcomes and scored (CRPS for numeric prints), with public
calibration records. The operator offers integration through a plugin or REST, free, with
credits for LLM inference for good scores.

**Assessment:**

- **Target fit is not established.** The listed targets are gold, crude oil, natural gas,
  treasuries, equity indices, soybeans, the dollar index and macro prints. DE-LU day-ahead power
  is not among them. Our model forecasts DE-LU hourly prices and has no skill claim for those
  targets. "No modelling work" holds only if a DE-LU day-ahead target exists.
- **It is external, automated publication.** Posting forecasts to a third-party service is a
  public write that needs the Owner's authority under `AGENTS.md`. As a daily job, it needs
  unattended authority too, and a credential for another service.
- **It does not replace our own record.** The prospective evaluation is defined in-house (CP-18
  and CP-19), with frozen scoring, served identity and lineage. A second, differently scored
  public record would need its own claims discipline, and could not be cited as CP-19.
- **The timing is wrong.** There is no live product yet, and v1 is frozen and not updated daily.
- **Licensing is not a blocker:** issued forecasts derived from CC BY 4.0 data may be shared
  with attribution.

**Recommendation.** Decline for now, politely. Revisit only after CP-19, and only if the arena
offers a DE-LU day-ahead target. It would then be an additional read-only mirror of forecasts
the frozen policy already issued, under a separate Owner authorization. The reply is the Owner's
external action. A suggested text:

> Thank you — that is generous, and the replay-versus-live distinction is exactly what we care
> about. We don't have a live product yet: the current Space is a frozen historical model by
> design, and our next step is our own prospective record for a daily-trained final model. Our
> target is the DE-LU hourly day-ahead price, which isn't among your current questions, so
> we'll pass for now. If you add European day-ahead power, we'd be glad to look again once our
> live evaluation has run. Closing this discussion — thanks again.

---

## 10. Not authorized by this plan

This plan authorizes none of the following:

- a model designation, freeze, training run, scheduler or daily job;
- a Space or site change, an upload or an MLflow write;
- an `AGENTS.md` change or unattended publication;
- a reply to Headline Arena;
- a research budget.

Each follows its own authority in §5.
