# Capstone — Completion and Corrections

**Anchor document. Status: DRAFT, awaiting owner ratification.** Authored by the Orchestrator
2026-09-15 on the owner's instruction of the same date.

**This document closes `capstone_V6_8.md` as an active plan.** v6.8 is complete: M1/CP-1, M2/CP-2,
M3/CP-3 and M3.5/CP-3B all landed, REL-1 is complete, and all three public surfaces are live. v6.8
remains the **ratified historical record of v1** and is not edited. Everything forward lives here.

**`capstone_M4_v2-plan.md` is superseded by §4–§6 of this document** and should carry a pointer
rather than a second copy of the stage. It is not deleted; it is the record of how M4 was reasoned
out and ratified on 2026-09-15.

---

## 0. What this is, and the one sentence that describes it

v1 is a **frozen artifact with measured limits**. This document turns it into a **running system**:
a model that retrains every day on real data, publishes a forecast, and scores yesterday's forecast
in public — with MLflow as the system of record rather than a screenshot, and with the one rigorous
confirmatory test preserved rather than dissolved into the daily churn.

### Two models, two jobs, and the division is absolute

**This is the load-bearing distinction in the whole document. Everything else follows from it.**

| | **v2 — frozen** | **the daily model** |
|---|---|---|
| **What it is for** | **the model of record.** Every result, every metric, every comparison, every claim on every surface, and the line on the CV | **the demo.** One job: show that the system runs end to end in production |
| **Lifecycle** | trained once, frozen, fingerprinted, set aside untouched, tested **exactly once** after 90 days | retrained from scratch every morning; no version survives the day |
| **Evidence class** | **one-shot confirmatory** | **prospective observation of a running service** |
| **What it proves** | whether the model is good | whether the *system* works — ingest, unattended training, calibration, publication, honest public scoring |
| **What it may never do** | — | **supply a performance claim.** Its numbers describe a running service; they are not this project's statement of model quality |

> **v2 frozen carries all the results. The daily model carries none of them.** It is product proof:
> evidence that the pipeline exists and runs, not evidence about how well the model forecasts. A
> rolling error figure from the live service has no clean test set behind it and never will, and it
> is never quoted as if it did.

**Four things are built, in order, and each depends on the one before it:**

| | Stage | What it produces |
|---|---|---|
| **§2** | MLflow as system of record | the tracking server on the critical path |
| **§4** | **M4** — regime-robust calibration | `v2-calibration-only`, `v2-full`, **the models of record** |
| **§6** | **M5** — the daily retraining service | v2's recipe, retrained daily, for the demo only |
| **§7** | The live scorecard | yesterday scored, today forecast, in public |

---

## 1. Topology — where each thing actually runs, and why

Checked 2026-09-15, because a plan that names a platform must verify what that platform does.

| Layer | Runs on | Why there |
|---|---|---|
| **Compute** (training, inference, rendering) | **GitHub Actions** | Free and **unmetered for public repositories**. The champion trains end-to-end in minutes on CPU, well inside a standard runner. |
| **System of record** (runs, metrics, models, the forecast log) | **MLflow on DagsHub** | Free remote tracking server and model registry per repository. **DagsHub provides tracking, registry and storage — it does not provide compute.** Training cannot run there. |
| **Publication** | **GitHub Pages**, from `main` `/docs` | Already live. Serves a committed file; makes zero runtime calls. |
| **Interactive demo** | **Hugging Face Static Space** | Free, and verified not to sleep. Docker/Gradio moved behind PRO on 2026-07-08. |
| **Data** | **SMARD.de** | Keyless, CC BY 4.0, and §3 of v6.8 already ratifies it as `fallback-primary`. **No ENTSO-E token in an unattended job.** |

> **The answer to "will it run on DagsHub?" is no, and the answer to "do the numbers reach the
> GitHub page?" is yes.** Actions computes, DagsHub records, git publishes, Pages serves.

**Why SMARD and not ENTSO-E for the daily pull.** ENTSO-E needs a token, and `entsoe-py` 0.8.0
passes it as a **query parameter** — so it appears in request URLs and in raised exception text,
which in an unattended job means in CI logs. SMARD needs no key at all. It is also the source that
kept CP-1 alive through a multi-week ENTSO-E outage. The daily path uses SMARD; ENTSO-E stays
available for manual reconciliation.

---

## 2. (א) MLflow gets physical use — and the test for that is falsifiable

**The bar: something must break if the tracking server is unreachable.** Logging more artifacts is
not physical use; it is a larger screenshot. Today MLflow is **write-only and read-never** — every
`mlflow` reference in `claims.py` is a URL string, the champion is bundled, and every published
number comes from a committed JSON file. That changes here.

### 2.1 What the daily job reads from MLflow

1. **The model.** The job resolves the deployed model from the **registry** —
   `models:/delu-day-ahead-champion@champion` — not from a path in the repository. The alias is
   what says which model is live. Promotion is an alias move, not a commit.
2. **Yesterday's forecast.** The scorecard is built by **querying the tracking server** for the run
   that produced yesterday's forecast and reading its logged prediction vector. *"What I predicted
   yesterday"* lives in the tracking record, not in a file this repository could rewrite.
3. **The run history.** The rolling error series, the run counts, and the model-version lineage on
   the published page are all **query results**, not maintained files.

### 2.2 What it writes

Every daily run logs: the SMARD pull's coverage and hashes, the training rows and cutoffs, the
fitted model (registered as a new version), the forecast vector for D+1, the realised prices for
the scored day, the error metrics, and the input-validation verdict. One run per day, named
`daily::<delivery-date>`.

### 2.3 The cost of a real dependency, and how it degrades

**A DagsHub outage breaks the daily build. That is the price of the dependency being real, and it is
designed rather than discovered.**

- The job **fails loudly and publishes nothing.** It does not fall back to a local copy and pretend.
- The published page therefore keeps **yesterday's committed content**, which already carries its own
  data date and a staleness line. A reader sees an older date, never a wrong number presented as
  fresh.
- Two consecutive failures raise a visible banner on the page: *"the daily run has not completed
  since &lt;date&gt;"*. The banner is generated from the committed content's own date, so it works
  even when the tracking server is the thing that is down.

### 2.4 Closing the run-count gap that exists today

An anonymous visitor who clicks through to the tracking server **today** counts **10 runs named
`champion::final-fit-and-holdout`** against a headline claim of *"evaluated exactly once"*. The
reconciliation is real and was written in advance — *"'Evaluated exactly once' is a statement about
the evaluation decision, not about how many times a deterministic script may be run"* — but it lives
in `reports/cp2/holdout_report.json`, not on the surface the reader is standing on.

**Fix, in two parts:**

- **Now:** the reconciliation becomes a claim in `claims.py` and renders on every surface.
- **With §7:** the page carries a **"what the tracking server says"** panel, built from a real query
  at render time and baked into the static HTML. A reader who does not click sees what the record
  contains; a reader who does click and counts finds the answer where they are standing. The page
  still makes **zero runtime calls** — the query happens at build time, not in the visitor's browser.

---

## 3. Re-ratified from v1 — the invariants nothing here may weaken

- **§5.2 delivery-day availability.** No component, including anything generated daily, may consume
  a value unavailable at the 12:00 CET D−1 origin. The control stands: masking delivery-day prices
  changes the output by exactly `0.0`, and a D−1 mutation moves it.
- **Positive controls on every negative assertion.** A test that something does not happen is
  satisfiable by an inert implementation unless a control proves it can fail.
- **Zero quantile crossings** after the full pipeline. The one hard gate.
- **Results are reported, never gated.** No stage here requires a favourable number.
- **v1 is preserved, not superseded in place.** `land/cp-3`, `evidence/cp-3`, `land/cp-3b`,
  `evidence/cp-3b`, `models/champion/`, `docs/cp2-model-report.md` and the v1 report stay exactly as
  they are, including the 0.194 coverage collapse.
- **The schema firewall.** Post-gate A69 and same-day actual columns are refused at the model
  boundary. It already refused an input it had never seen; it stays.

---

## 4. (ב) M4 — regime-robust calibration

Re-derived here rather than copied, and fitted to the system this document builds.

### 4.1 The defect, stated so it can be falsified

| | |
|---|---|
| Nominal | 95 % |
| Observed, August-2022 peak weeks (408 h / 17 days) | **0.194** |
| Observed, one-shot holdout (2,160 h / 90 days) | 0.9398 |
| fold_3 calibration window | 2022-05-01 … 2022-06-29, mean level ≈ **€198** |
| fold_3 evaluation block | 2022-07-01 … 2022-09-28, mean level **€375.96** |
| Level ratio, calibration → evaluation | **1.90×** |

**Mechanism.** The CQR conformity score is `max(q̂_lo − y, y − q̂_hi)` and its correction is an
**additive** shift in EUR/MWh estimated on the calibration slice. Residual magnitude in this market
scales with price level. A threshold sized in a €198 world is too narrow in a €376 world. This is
split conformal behaving exactly as documented when exchangeability fails — the guarantee is
finite-sample but *conditional*, and a structural break voids the condition.

**What M4 does not claim.** The point forecast degrades by a **different** mechanism — shrinkage
toward the training level, with 61.3 % of fold_3's evaluation block above the 99th percentile of its
training data while only 2.45 % exceeds the maximum. M4 does not fix that, and anything it improves
there is a reported side effect.

### 4.2 Anti-overtuning discipline — the binding constraint

**fold_3's answer is already known.** Every choice made while looking at it is fitted to a result we
have seen. Pre-registered here, before any code runs:

1. **fold_3 is a diagnostic control, never a selection metric.** Selection runs on folds
   {1, 2, 4, 5} only, pooled, by the observation-weighted rule v1 used.
2. **The method set is frozen before any v2 code runs** — §4.3 names it exhaustively. Adding a
   candidate afterwards requires a written owner amendment and is recorded.
3. **One scalar per candidate, fixed in advance:** pooled mean pinball loss over {1, 2, 4, 5}. Ties
   resolve to the simpler method, in the order listed.
4. **fold_3 is published for every candidate, including the losers.** Publishing only the winner's
   crisis number would let a lucky draw pass as a fix.
5. **A pre-registered falsification.** If the selected method's fold_3 95 % coverage does not exceed
   **0.194 by at least 0.20 absolute**, the stage reports that **the fix did not work** and v1
   remains the recommended frozen artifact. Written now.
6. **No fold_3-specific parameter may exist.** No crisis flag consumed by the calibrator, no regime
   switch, no threshold table keyed on a date chosen by looking at prices.

> Rule 5 is what makes this honest. Without a pre-registered failure condition, any calibration
> change can be narrated afterwards as an improvement.

### 4.3 The candidates, frozen

**C-1 — Scaled (normalised) conformal.** Divide the conformity score by a locally estimated scale
`σ̂(x)` before the order statistic, multiply back at prediction time; the threshold becomes
multiplicative. Scale estimators, also frozen: (a) the raw head spread `q̂_0.95 − q̂_0.05`;
(b) a trailing rolling price volatility computed under the §5.2 boundary.

**C-2 — Adaptive Conformal Inference** (Gibbs & Candès, 2021). `α_{t+1} = α_t + γ(target − 1{y_t ∈ C_t})`,
with `γ` selected on folds {1, 2, 4, 5} from a frozen grid. **The owner granted the §13
sequential-conformal amendment on 2026-09-15**, scoped to C-2 and to nothing else.

> **C-2's feedback lag is two delivery days and it is structural.** At the 12:00 CET D−1 origin,
> delivery day D−1 is still in progress, so the most recent fully observed day is **D−2**. No amount
> of accumulated history changes this: it is forecast geometry, not data availability. It is also
> harmless — the update reads the most recent *available* realisation and adapts slightly more
> slowly. **It must be proved with the masking control, not assumed.**

**C-3 — Mondrian / regime-conditional conformal. REJECTED before any run, and not implemented.** It
requires a regime taxonomy, and ours is defined by dates chosen *after* seeing the price history —
exactly what rule 6 forbids. Implementing a method already committed to rejection is waste; the
recorded rejection is the deliverable.

**Why both C-1 and C-2 run rather than the simpler one alone.** They fail differently. C-1 assumes
residual magnitude scales with price level — a modelling assumption that can be wrong. C-2 assumes
nothing about the mechanism; it watches realised coverage and corrects. Run C-1 alone and a null
result is uninterpretable: you cannot separate *"the calibration is unfixable"* from *"we guessed
the wrong mechanism."*

**Carried bars.** The `n_cal=20` one-based-rank fixture must still reproduce `{20,19,17,11}` →
`Q={8,7,5,−1}` on the unscaled path, and the scaled path gets its own exact fixture before use.
Isotonic stays last. Zero crossings stays the hard gate.

---

## 5. (ג) M4's holdout — one model, set aside, untouched, for 90 days

**This is the rigorous claim of the whole programme, and §6's daily service must never touch it.**

### 5.1 The protocol, pre-registered

1. Build and select **entirely on folds {1, 2, 4, 5}**, fold_3 reported as a diagnostic only.
2. **Freeze two artifacts** and fingerprint them (see 5.2). Register both in MLflow under a
   dedicated `delu-m4` experiment, tagged `frozen-awaiting-holdout`, so the freeze date is on a
   third-party record rather than only in a commit message.
3. **Wait 90 delivery days from the freeze**, accumulating data the frozen models have never seen.
4. Pull a fresh snapshot, apply a one-delivery-day embargo, and **evaluate exactly once.**

**No retrain, no retune, no re-threshold, no peeking.** The artifacts sit in the registry with an
alias that says what they are. The daily service of §6 trains its own models and **never writes to
these versions, never reads them as a starting point, and never shares a registry alias with them.**

### 5.2 Two artifacts, not one — how Track 2 enters without confounding

Both the calibration change and the data feed would otherwise land in the same one-shot window,
where a joint improvement could not be attributed to either. So:

| Artifact | Contains | Endpoint |
|---|---|---|
| **`v2-calibration-only`** | Track 1 alone | **Primary** — interval coverage and pinball vs v1. The question the stage exists to answer. |
| **`v2-full`** | Track 1 + Track 2 (§6.1 features) | **Secondary** — point accuracy and pinball vs `v2-calibration-only`. The data track, isolated. |

Both are evaluated on the **same** window. That is one extra evaluation of an already-frozen
artifact, not a second holdout. `v2-full` ships if it does not degrade the primary endpoint.

### 5.3 Window length — computed, not guessed

From v1's own holdout: day-level coverage standard deviation **0.1149**, day-level effective sample
size **76.7 of 90** (dependence inflation 1.17×).

| Purpose | Days |
|---|---|
| Coverage CI half-width ±5.0 pp | 24 |
| ±4.0 pp | 38 |
| ±3.0 pp | 67 |
| ±2.0 pp | 149 |
| DM power 0.80, one-sided α=0.05, \|d\|=0.50 | 25 |
| \|d\|=0.30 | 69 |
| \|d\|=0.2165 *(v1's development effect vs naive)* | 132 |

**Decision: 90 delivery days.** It matches v1's holdout exactly, so the two are compared on equal
footing; it gives **±3.8 pp** on coverage and reaches 80 % power at **\|d\| ≥ 0.26**.

**Pre-registered limitation:** a pinball effect smaller than \|d\| ≈ 0.26 **will not be detectable**
at this window, and the report will say so rather than reading a null as a tie.

**The clock starts at the freeze, not today.** There is no usable buffer to shorten it with: v1's
snapshot is fully consumed through 2026-09-06, and the days accruing since are already what the
90-day count consumes.

---

## 6. (ד) M5 — the daily retraining service

**Based on M4 and running only after it freezes.** A fresh model every day, trained on real data
pulled that morning, never stale in its inputs.

**Its role is the demo and nothing else.** It is **v2's recipe retrained** — the CP-1 feature
catalog, the CP-2 hyperparameters, and M4's calibration method, all frozen; only the data is new. So
it demonstrates the validated method running in production rather than being a second, unvalidated
model. **It supplies no result to any surface except the live scorecard**, and the scorecard's own
numbers describe the service, not the model's skill. Every metric this project quotes about model
quality comes from frozen v2 and its one-shot holdout.

### 6.1 What it does, once per day

Scheduled after ~13:00 CET, when the day-ahead auction has published (clearing 12:45–12:57 CET):

1. **Pull from SMARD.de** the delivery days missing since the last successful run — prices, load
   forecast, and the generation series the frozen feature catalog needs. Keyless, CC BY 4.0.
2. **Validate before training** (§6.3). A failed validation means the run stops and publishes
   nothing.
3. **Retrain** the nine quantile heads on everything available, with the CP-1 feature catalog, the
   CP-2 hyperparameters, and **M4's calibration method** — all frozen. Only the data is new.
4. **Calibrate** on the most recent slice under the §5.2 boundary, isotonic last, zero crossings
   enforced.
5. **Forecast** delivery day D+1 and log the full nine-quantile vector to MLflow.
6. **Score** the forecast made for the most recent fully settled day, read back from MLflow (§2.1).
7. **Register** the new model version; move the `daily` alias to it. **`champion` is untouched** —
   that alias belongs to the frozen v1 artifact.
8. **Render and commit** the page (§7).

**Track 2's data feeds enter here as well as in `v2-full`:** Open-Meteo fixed-lead-time weather
(CC BY 4.0, **available from 2024 only** — see §6.4) and ENTSO-E **planned** outages. Forced outages
are excluded: the archive is the current view, not the as-of-gate view, and for forced outages that
distinction is fatal.

### 6.2 What daily retraining fixes — and what it does not

**This section exists because the obvious reading is wrong, and a public surface that implies
otherwise would be an overclaim.**

**It fixes:** input staleness. v1's raw-model fit cutoff is 2026-04-07 and recedes further every day.
A daily model's training data ends yesterday.

**It does not fix:**
- **Hyperparameters**, chosen once at CP-2 and frozen.
- **The feature catalog**, frozen at CP-1.
- **The calibration method** — that is M4's job, not this one.
- **And critically, a regime break.** In August 2022 a daily-retrained model would still have had
  the overwhelming majority of its training mass in the moderate-price regime. **Retraining daily is
  not adaptation to a level shift.** M5 without M4's calibration fix would reproduce v1's failure
  exactly. That is why M5 depends on M4 and not the reverse, and the ordering is a design
  constraint, not a schedule.

### 6.3 Unattended training that publishes — the failure mode, designed in

**A model that trains and publishes without supervision will one day train on corrupt data and
publish a wrong number.** SMARD has had gaps; the 2025-10-01 quarter-hourly transition already bit
this project once. The service is built to refuse rather than to guess.

**Gates, all of which stop the run rather than degrade it:**

| Gate | Refusal condition |
|---|---|
| **Completeness** | any delivery day in the new window missing hours, or a DST day without 23/25 as required |
| **Schema firewall** | the existing runtime check — post-gate A69 or same-day actual columns present |
| **Reconciliation** | the newly pulled overlap disagrees with the committed history beyond €0.01/MWh |
| **Boundary control** | masking delivery-day prices does not produce `0.0`, or a D−1 mutation does not move the output |
| **Crossing gate** | any quantile crossing survives the pipeline |
| **Sanity bounds** | a forecast outside the harmonised clearing bounds (+4,000 / −600 EUR/MWh from 2026-05-28) |

**On refusal:** the job fails loudly, publishes nothing, and the page keeps its previous committed
content with its own visible data date. **A stale page with an honest date beats a fresh page with a
wrong number**, and the choice is made here rather than at 3 a.m. by whoever is reading the logs.

### 6.4 The honest limitation of the data track, stated unprompted

**Gate-legal weather forecasts begin in 2024.** Open-Meteo's Historical Forecast API reaches 2017 but
**stitches short-lead-time runs**, which is look-ahead; only the fixed-lead-time endpoints are §5.2
legal, and those start in January 2024 (ECMWF single runs from 2024-03-14). **Folds 1, 2 and 3 are
unreachable.** The data track improves the product that is actually deployed. **It cannot touch the
crisis regime, and no surface may imply that it can.**

**Gas remains omitted,** re-closed on evidence 2026-09-15: every TTF/THE source found is commercial
with redistribution-prohibiting terms; ACER publishes a daily **LNG** assessment, not a hub price;
Trading Hub Europe publishes consumption, not prices. `capstone_V6_8.md` §0 item 3 stands.

---

## 7. (ה) The live scorecard

**The page is re-rendered by the daily job with the numbers baked in.** It is not a dashboard that
fetches — the static export's zero-runtime-calls property survives, because the numbers are in the
HTML by the time a visitor loads it.

### 7.1 What it shows

1. **Yesterday, scored.** The forecast that was published for the most recent fully settled delivery
   day, the prices that actually cleared, and the error — MAE, pinball, and whether each hour fell
   inside the 50/80/95 % interval. Read back from MLflow, not from a local file.
2. **Today's forecast** for delivery day D+1, as a quantile fan, with the interval the model is
   actually offering rather than a point number dressed as certainty.
3. **The running record.** A rolling error series and rolling empirical coverage over every day the
   service has run. **Every day it has run.** No date picker, no "best week", no ability to choose
   the window. The chart starts on day one and never drops a day.
4. **What the tracking server says** — run counts and model lineage from a real query at build time,
   which is also what closes §2.4's gap.
5. **The staleness line**, always: the data date, the model's training cutoff, and how many days ago
   the last successful run was.

### 7.2 Why no date picker, and what it costs

**A scorecard you can filter is a marketing asset. A scorecard you cannot filter is evidence.**
Anyone can publish a good week. The claim only means something if the bad days are in it and cannot
be removed.

**And they will be there.** The error will be worse on volatile days, worse under a regime shift,
and the running coverage will wander around nominal rather than sitting on it. That is the point.
A public, unfilterable, daily-updating error record is the single most falsifiable artifact in this
project, which is precisely why it is worth more than another chart.

### 7.3 Which model is quoted where — the line that must never blur

**Frozen v2 is the model of record and supplies every result. The daily model supplies one page and
no results.** This table is the routing rule, and it is enforced by `claims.py`: a number sourced
from the daily service cannot be rendered into a slot that belongs to the model of record, because
the two are different claim namespaces.

| Surface / number | Model | Evidence class | May claim |
|---|---|---|---|
| The report, all metrics, SHAP, regimes, reliability | **frozen v2** | **one-shot confirmatory** | whether the model is good, on the evaluated window and nothing wider |
| The M4 holdout result (§5) | **frozen v2** | **one-shot confirmatory** | whether the calibration fix works |
| The CV line, any figure quoted in an interview | **frozen v2** | **one-shot confirmatory** | — |
| v1's preserved report | frozen v1 champion | **one-shot confirmatory** | what v1 achieved, including its 0.194 collapse |
| **The live scorecard only** | **daily model** | **prospective observation of a running service** | that the system runs, ingests, trains unattended, calibrates, publishes and scores itself in public |

**The daily model has no clean test set and never will** — every version of it has seen everything up
to yesterday, by construction. It is not a second opinion on model quality; it is proof that the
product exists and functions.

> **Three prohibitions, and they are absolute.**
>
> 1. **A rolling figure from the live service may never be quoted as, compared with, or substituted
>    for a confirmatory holdout result** — not on the page, not in the README, not on the CV, not in
>    a room.
> 2. **The daily model's numbers never appear in a headline claim about forecast quality.** They
>    appear on the scorecard, labelled, and nowhere else.
> 3. **The scorecard never implies the frozen model produced it, and the report never implies the
>    daily model produced it.** Each number carries its source model beside it.

**Why the demo is still worth building under those restrictions.** Because the thing it proves is
not available any other way. A frozen model with a good holdout proves *the method works*. A service
that pulls real data every morning, refuses bad input, retrains, publishes, and scores itself in
public with no ability to pick its days proves *the engineering works* — and that is the half of the
claim a hiring manager cannot check from a notebook.

---

## 8. (ו) Everything through MLflow — the integration contract

| Object | Where it lives | Consequence |
|---|---|---|
| Deployed daily model | registry, alias `daily` | promotion is an alias move, not a commit |
| Frozen v1 champion | registry, alias `champion` | **never moved by the daily job** |
| Frozen M4 artifacts | registry, `delu-m4`, tagged `frozen-awaiting-holdout` | the freeze date is third-party evidence |
| Every forecast vector | run artifact, `daily::<date>` | the scorecard is built by querying it |
| Every realised outcome and error | run metrics | the running record is a query, not a file |
| Data-validation verdicts | run tags | a refusal is on the record, not only in a log |
| v1's experiment | `delu-cp2` | untouched forever |

**Three experiments, never mixed:** `delu-cp2` (v1, closed), `delu-m4` (the frozen calibration
artifacts), `delu-daily` (the service). Separation is what keeps v1's record exactly as the one-shot
holdout left it.

**Secrets.** `MLFLOW_TRACKING_USERNAME` / `MLFLOW_TRACKING_PASSWORD` as GitHub Actions secrets —
HTTP basic auth, not Bearer. **No ENTSO-E token in the daily job at all.** No token value is ever
printed, logged or committed; CI output is checked for leakage as a gate.

---

## 9. Checkpoints

| | Stage | Bar |
|---|---|---|
| **CP-9** | MLflow integration (§2) | The registry is the source of the model; the scorecard reads from the tracking server; a simulated outage is shown to fail the build loudly and publish nothing; §2.4's reconciliation claim renders on every surface |
| **CP-10** | M4 calibration (§4) | All candidates implemented with exact fixtures; selection on {1,2,4,5}; the full table including fold_3 for **every** candidate including losers; rule-5 falsification evaluated and reported; zero crossings; positive controls on every negative assertion |
| **CP-11** | Freeze (§5) | Both artifacts frozen, fingerprinted, registered, tagged; the 90-day clock starts and its start date is on the tracking record; interim status published per §7.3; **nothing evaluated** |
| **CP-12** | The daily service (§6) | SMARD ingest; every §6.3 gate implemented **with a positive control that makes it fire**; a deliberately corrupted input must stop the run and publish nothing |
| **CP-13** | The live scorecard (§7) | Page re-rendered and committed by the job; zero runtime calls preserved; no date filter; evidence classes labelled beside every number; staleness banner proved by a simulated missed run |
| **CP-14** | M4 one-shot evaluation (§5) | ≥ 90 delivery days after the CP-11 freeze; fresh snapshot; one embargo day; **opened exactly once**; primary and secondary endpoints; the power limitation stated |

Each follows the existing contract: one brief in, one packet out, one fresh Integration Critic,
`PASS`/`BLOCKED`/`INCOMPLETE`, owner-authored landing.

**No landing without a verdict binding the final candidate.** CP-3B landed with item 6 unmet —
recorded at `docs/track-b/evidence/cp-3b/item-6-NOT-COMPLETED.md` — because its review was cut off
twice. **That is not a precedent, and every brief in this document says so.**

---

## 10. What this is NOT

- **Not a trading layer.** No position, no P&L, no execution, no financial advice. A published
  forecast and its error record, nothing else.
- **Not a claim that daily retraining fixes regime shift.** §6.2 says the opposite, in advance.
- **Not a second source of performance claims.** The daily model supplies the live scorecard and
  nothing else. Every figure this project states about forecast quality comes from frozen v2 and its
  one-shot holdout (§7.3).
- **Not a licence to touch the M4 holdout.** The daily service never reads, writes, or aliases the
  frozen artifacts.
- **Not a filtered scorecard.** No date picker, ever.
- **Not a fuel-price layer.** Re-closed on evidence 2026-09-15.
- **Not a rewrite of the model.** One monolithic LightGBM quantile ensemble, nine heads.
- **Not a service with an uptime promise.** It is a portfolio artifact that runs daily and says
  plainly when it did not.

---

## 11. What this supersedes in `capstone_V6_8.md`

Stated explicitly, with the original reasoning answered rather than ignored.

| v6.8 boundary | Status | Why the ground moved |
|---|---|---|
| §9.2 *"no live API pull during user sessions"* | **Still holds.** | The page never fetches. The pull happens in CI, and the numbers are baked in. |
| §9.2 *"Frozen release, not a weekly service"*; the Monday refresh deleted | **Superseded** | v6.7 removed it as an *obligation that protected no live dependency* — a judgement about burden, not value. There was no live artifact and no audience then; there are both now. |
| v6.2 rider: *"no keep-alive of any kind… the GH-Actions cron option is deleted"* | **Superseded for rendering; upheld for keep-alive** | No keep-alive runs on any platform — the Static Space cannot sleep, so there is nothing to keep alive. The cron rebuilds content; it does not ping a service. |
| §13 *"No enterprise production pipeline"* | **Narrowed** | No enterprise pipeline, no SLA, no orchestration platform. One scheduled job that trains, publishes and scores itself. The original boundary guarded against scope creep with no hiring payoff; a public, unfilterable daily error record is arguably the highest-payoff artifact in the programme. |
| §13 *"no sequential conformal (EnbPI / SPCI)"* | **Amended for C-2 only** | Granted 2026-09-15. §13 itself named the reopen route; fold_3's 0.194 is the evidence that made it the obvious next step rather than a distraction. |

---

## 12. Open decisions for the owner

1. **Ratify this document as the forward anchor**, closing `capstone_V6_8.md` as an active plan and
   pointing `capstone_M4_v2-plan.md` here.
2. **The daily model's alias name** — `daily` is proposed, deliberately distinct from `champion` so
   that no tooling, link or reader can confuse the retrained model with the frozen evaluated one.
2b. **How hard to enforce §7.3's routing.** The recommendation is a **separate claim namespace** in
   `claims.py` — daily figures live under a `live_*` prefix that the report and README generators
   cannot read at all, so a mix-up is a build error rather than a review catch. That is stricter
   than a convention and costs one afternoon.
3. **How long the scorecard runs before it goes on the CV.** A record with four days in it invites a
   different reading from one with sixty. The recommendation is that the link goes up immediately
   and the scorecard simply shows however many days exist, labelled — but a deliberate wait is a
   legitimate alternative and should be a decision rather than a drift.
4. **The document's name.** *"Completion and Corrections"* describes §2's repairs accurately but
   undersells §6 and §7, which are a larger build than v1 was. Renaming is cosmetic and entirely
   the owner's call.
