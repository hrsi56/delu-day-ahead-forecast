# Presentation and tracking plan: one scrolling history page and MLflow

**Approved by the Owner, 2026-09-24.** R1–R6 are accepted as written. The §13 questions 2–4 stay
open. This plan covers three things:

- programme stage 3 (presentation around v2, work items 4.3R/4.3C/4.10R);
- the matching presentation of CP-20 (v3);
- MLflow as the visible tool for tracking and comparing versions.

It also fixes the design that later generations, the final model and the live model will extend.
Approval fixes the design only. Each phase runs as an Owner-authorized task, and publication
still waits for the Owner's visual review.

---

## 0. Summary

One public page tells the model history newest first. As the reader scrolls down they meet v3,
then v2 and its road, then v1. Later generations, the final model and the live model will be
added at the top. A scoreboard at the top compares every generation on the same evaluation rows.
Each generation is one chapter with the same template, a clear verdict and an evidence badge.

MLflow gets a new public experiment, `delu-generations`. It holds every generation as nested runs
with identical metric names, so MLflow's own comparison views show v1, v2 and v3 side by side.
From CP-21 on, experiments are tracked in MLflow while they run and published after landing.
The repository stays the single source of truth: the page is built from committed evidence, and
MLflow mirrors the same numbers, with a check that the two agree.

| Phase | Deliverable | Effort (agent) |
|---|---|---|
| A | CP-20 content draft and claim map; publication pass over the CP-15/16 draft | ~0.5 day |
| B | One data layer that reads committed evidence, with number, wording and date-guard tests | ~0.5 day |
| C | MLflow tracking spec, capability probe, backfill, mirror verification and link index | 1–1.5 days |
| D | The page (hero, scoreboard, reading guide, timeline rail, v3/v2/v1 chapters), README and Space cards | 1–1.5 days |
| E | Full CI-equivalent run, Owner visual review, publication, progress update | ~0.5 day + Owner review |

Total: roughly 3.5–4.5 agent days. A/B and C1–C2 can run in parallel.

---

## 1. Goals and non-goals

**Goals:**

- A single scrolling page that stays readable at v7.
- A full, honest v1 → v2 → v3 comparison now.
- Every number traceable to a committed file and a claim ID.
- MLflow visibly used for tracking, lineage and comparison.
- No regression of any public-surface invariant (§4).

**Non-goals now:**

- New model runs, extensions, the fresh-data test (4.7T) or live operation.
- Any metric for v2 or later that uses data after 2026-04-07.
- Any product, promotion, significance or economic claim.
- Registering HG in the Model Registry, because HG is not frozen.

---

## 2. Decisions

**Taken by the Owner (2026-09-24):**

1. One scrolling page, even with many generations. Chapters run newest to oldest, so scrolling
   down means going back in time.
2. v2 and v3 are presented publicly now. Each extension becomes a chapter later, and the live
   model goes at the top at the end.
3. MLflow becomes the visible cross-version comparison tool: backfill v2/v3 and track future
   work in it.

**Approved by the Owner (2026-09-24):**

| ID | Recommendation | Reason |
|---|---|---|
| R1 | Move v1's one-shot holdout out of the page header into the v1 chapter, labelled confirmatory for v1 only. Do not delete it. | It is v1's only confirmatory evidence and it is already public. Removing it would read as cherry-picking. It does not bind v2+, which never used that period. |
| R2 | Agents generate the page and charts from data; the Owner reviews visually before any push. | Keeps the build reproducible and testable. Presentation decisions remain the Owner's. |
| R3 | Version numbers go only to adopted models. The final model takes the next number, v4 if no extension is adopted. Experiments that are not adopted are named by content. | The timeline has a main line and side branches (§5.2). |
| R4 | The repository is the source of truth. MLflow mirrors it, and the page never reads MLflow, whether at build or at view time. | Zero runtime network calls; reproducible builds; no silent drift. |
| R5 | Track locally during a checkpoint and publish to DagsHub after landing. | Network outages cannot stall runs, the public server holds only reviewed runs, and this matches "LAND, then publish". |
| R6 | The Model Registry holds only runnable, frozen policies: v1 `champion` now and the final policy later. | A registry entry without a runnable artifact is hollow, and HG is not frozen. |

---

## 3. Baseline: what exists today

**Site:**

- `docs/index.html` is 1,014,592 bytes. `scripts/build_pages.py` generates it from
  `reports/cp2/*.csv` and seven PNG figures embedded as `data:` URIs.
- The page is the v1 report: sections 1–12 plus an interactive SVG fan chart.
- Above them sits a hand-written "Development update · 2026-09-16" card. It is stale (it says
  CP-16 still needs a brief), and its numbers are typed into the generator.
- The title, meta description and lede frame the page around v1's one-shot holdout.

**Other surfaces:**

- `README.md`, generated by `scripts/cp3_readme.py`. Lines 18–54 are stale.
- `space-wasm/README.md` (Static Space), `space/README.md` and `reports/cp3/mlflow_registration.json`.
- All of them render from `src/delu_forecast/claims.py` (104 claims) through
  `src/delu_forecast/surfaces.py`.

**Guards:**

- Tests: `test_17_cross_surface_agreement`, `test_19_static_page_is_offline`,
  `test_20_release_surfaces`, `test_21_limitations_are_complete`, `test_22_wasm_equivalence`,
  `test_23_static_space` and `test_24_live_namespace_is_walled_off`.
- Scripts: `scripts/verify_release.py` (`make verify`) and `scripts/check_links.py`.

**MLflow on DagsHub:**

- One experiment, `delu-cp2`, with 55 runs including reproductions. The page names the nine
  decision-bearing runs.
- One registered model, `delu-day-ahead-champion`, version 1, alias `champion`.
- The client is `mlflow` 3.16.0. `src/delu_forecast/tracking.py` provides `redact`, basic-auth
  bridging, `code_sha`, `snapshot_hash`, `run` and `log_decision_record`.
- The CP-3 registration record lists `tags_refused`, so some DagsHub registry features are
  limited.
- Nothing from CP-10, CP-15, CP-16 or CP-20 is logged.

**Evidence available for the comparison (all committed):**

| Source | Content |
|---|---|
| `reports/weather-ablation/metrics.csv` | B0, B1 (v1 development replay), B2, B3, A1, H0 (v2) and HG (v3) on the **same 10,747 hours**, per fold, pooled and equal-fold |
| `reports/weather-ablation/uncertainty.csv` | HG−H0 paired intervals, equal-fold and per fold |
| `reports/weather-ablation/criteria.csv` | §8 criteria 1–6 for H0 and HG, including the matched crisis window |
| `reports/weather-ablation/diagnostics.csv` | Daily (90 per fold) and hour-of-day (24 per fold) rows per policy |
| `reports/v2-causal/{metrics,uncertainty,criteria}.csv` | H versus P and the CP-16 references |
| `reports/cp15/{relative_scores,peak,criteria}.csv` | Nine policies; matched crisis window for B1, A1 and B2 |
| `reports/cp10/report.md` | Calibration-only experiment |
| `reports/cp2/*` | v1 |
| `docs/track-b/research-content/cp15-cp16-update.md` and `cp15-cp16-claims.md` | v2 narrative, chart specs 1–2, withheld claims W1–W16 |

**Development folds (identical for every policy):**

| Fold | Delivery days | Days | Hours |
|---|---|---|---|
| 1 | 2020-07-01 → 2020-09-28 | 90 | 2,160 |
| 2 | 2021-04-01 → 2021-06-29 | 90 | 2,159 |
| 3 (crisis) | 2022-07-01 → 2022-09-28 | 88 | 2,112 |
| 4 | 2025-05-01 → 2025-07-29 | 90 | 2,160 |
| 5 | 2026-01-08 → 2026-04-07 | 90 | 2,156 |

**Data boundary:**

- Development ends 2026-04-07.
- v1 used 2026-04-09 → 06-07 for calibration and 2026-06-09 → 09-06 as its published holdout.
- Nothing after 2026-09-06 has ever been published.

---

## 4. Invariants that must not break

Each was paid for; the sources are the commits that introduced them (155b0f8, 8341fba, 7f16f4e,
99c9250, 5b94b8f) and the standing decisions.

1. **Zero runtime network calls.** Only plain `<a>` navigation and `data:` URIs; no CDN, fonts or
   analytics (CP-3 item 3; `test_19`). New charts are inline SVG.
2. **One claim source.** `claims.py` feeds every surface.
   - `make verify` must pass.
   - Rebuild `app/public/claims.json` (`make wasm-payload`) whenever claims change, because
     `test_22` fails on drift.
3. **Fix the generator, not the output.** Never hand-edit `docs/index.html` or `README.md`.
4. **v1's honesty statements stay exact:**
   - development point-MAE DM p = 0.948 with statistic +1.6228, stated as a deficit (the median is
     28.58% worse than the naive);
   - 0.194 coverage over the August-2022 peak weeks, with its mechanism;
   - fold 3 explained as shrinkage toward the training level, not as "trained on pre-crisis data";
   - crossings 10,158 → 4,412 → 0;
   - "the shipped model is the evaluated model";
   - the four cutoffs and the 152-day staleness.
5. **Every limitation appears on every human surface** (`test_21`).
6. **Every tracking link uses the `.mlflow` host.** `check_links` passes unauthenticated, and the
   gated repository-UI URLs remain its control.
7. **The `live_` namespace wall** (`test_24`): no daily-service figure on model-of-record surfaces.
8. **Attribution and licensing appear on every surface.** Add the GFS line from `DATA-LICENSE.md`
   to the `licensing` claim.
9. **v2 wording rules stand.**
   - W1–W16 from `cp15-cp16-claims.md` apply.
   - The H−P MAE upper endpoint is printed in full as **+0.000003857628092332211** and never
     rounded.
   - No significance wording.
   - W14 is relaxed for weather only, within CP-20 evidence. VRE, TabPFN, DDNN and Chronos-2
     claims stay withheld.
10. **No v2+ metric uses data after 2026-04-07, and no v2+ model is scored on v1's holdout
    window.**
11. **Labels stay:** `development_post_selection`, CP-15 `NOT_DEMONSTRATED`, "no demonstrated
    joint preference ≠ equivalence", descriptive economics only.
12. **English only.** Presentation belongs to the Owner, who reviews before publication.
13. **`pyproject.toml` and `uv.lock` stay byte-identical,** because frozen protocols hash them.
14. **No public text about retired governance tooling.**

---

## 5. Page design

### 5.1 Structure, top to bottom

1. **Hero.**
   - One line: "From a LightGBM baseline to a weather-aware LEAR forecast."
   - Status strip: what is released (v1, which the browser demo runs), the best research model
     (v3, development evidence) and what comes next.
   - Three key numbers with their evidence badge.
2. **Scoreboard.** One chart and one table over every policy on the identical 10,747 hours (§6.2),
   with a row added automatically per generation.
3. **How to read this page.** Evaluation design, evidence badges, the data boundary and how
   experiments are tracked in MLflow (§6.1).
4. **Timeline.** Chapters newest first. Future chapters (live, final, extensions) are inserted
   here.
   - v3 (CP-20).
   - v2 (CP-16), including "the road to v2" (CP-10, CP-15).
   - v1 (CP-1…CP-3B): a condensed card followed by the full existing report, unchanged.
5. **Footer.** Licensing and attribution (CC BY 4.0 and GFS), reproducibility, and links.

### 5.2 Chapter template (identical for every generation)

- **Header strip:** version, date, verdict (adopted / not adopted), evidence badge, and three
  numbers against the predecessor.
- **What changed:** one paragraph plus a small pipeline-delta diagram.
- **Hypothesis:** what we expected, as stated before the run.
- **Result against the predecessor.** Paired intervals where they are saved; a descriptive score
  change otherwise, labelled as such.
- **Where it helps and where it hurts:** per fold, the crisis window and hours of the day. Only
  claims that are sourced in the claim map.
- **Proof:** causal controls and the independent review, including failed attempts.
- **Cost and dependencies:** compute, data sources and operational risk.
- **Pros and cons.**
- **Links:** report, independent verdict, reproduction command and "Open in MLflow".

The main line holds adopted models. Evaluated but rejected experiments appear as side-branch
chapters with "not adopted, and why", which makes "improves or not" visible.

### 5.3 Navigation and scale

- **Timeline rail:** a sticky side rail (CSS only, anchor links) listing every generation with its
  key number and the current position. On mobile it becomes a top bar.
- **Deep content folds away.** Full tables and long methodology sit in `<details>` (native HTML,
  no script). Summaries and main charts stay visible so the scroll tells the story.
- **Size budget:** at most 30 KB per new SVG chart and 2.5 MB for the whole page at v7, enforced
  by a test. v1's existing PNGs are kept.
- **Script:** none is required beyond the existing fan chart. An optional MAE/WIS toggle on the
  scoreboard may use a few lines of inline script.

### 5.4 Evidence badges

- **Confirmatory:** v1's one-shot holdout; later, 4.7T.
- **Development · post-selection:** CP-10/15/16/20 and the extensions.
- **Prospective:** live.

Numbers with different badges are never placed side by side as comparable. The scoreboard uses
only development rows. v1's holdout lives in v1's chapter.

### 5.5 Visual language (suggestions; the Owner decides)

- One colour per generation, used identically in the scoreboard, charts and rail. References
  (B0, B2, B3) are neutral greys.
- Charts are generated at build time as inline SVG, with text labels, `aria` descriptions and a
  table fallback.
- The current light, report-like style is kept.

---

## 6. Content now

### 6.1 How to read this page

- **Five development folds** (the table in §3), including the 2022 crisis fold.
- **Equal-fold scores** normalized to the similar-day naive (B0 = 1.00; lower is better).
- **WIS:** seven quantiles, central intervals at 50, 80 and 95%.
- **Paired moving-block bootstrap:** seed 15042, 2,000 replicates, 7-calendar-day blocks.
- **The joint improvement rule.**
- **Independent Integration review** for every generation.
- **The three evidence badges.**
- **The data boundary:** nothing after 2026-04-07 is used before the final test.
- **MLflow:** a short paragraph with a link to the `delu-generations` leaderboard.

### 6.2 Scoreboard

Equal-fold scores, development and post-selection. Source: `reports/weather-ablation/metrics.csv`.

| Row | Public name | S_MAE | S_WIS |
|---|---|---|---|
| B0 | Similar-day naive (reference) | 1.0000 | 1.0000 |
| B1 | v1, development replay | 1.0518 | 0.9856 |
| B3 | Daily LightGBM (reference) | 0.7841 | 0.7399 |
| A1 | Normalized LEAR (CP-15 best challenger) | 0.6723 | 0.6460 |
| B2 | Daily LEAR (reference) | 0.6578 | 0.6390 |
| H0 | v2 | 0.6441 | 0.6160 |
| HG | v3 | 0.5658 | 0.5322 |

Reference lines mark the §8 criteria 1–2 limits (0.59203 S_MAE, 0.57509 S_WIS; 0.90 × the best of
B0–B3) and B0 = 1.00.

### 6.3 v3 chapter (CP-20)

**Charts:**

| # | Chart | Source |
|---|---|---|
| C1 | Diagram of the GFS box (47–55.25°N, 5.5–15.5°E) and the feature recipe: per-cell wind speed at 10 m and 100 m, then an area average; DSWRF de-averaged; missing indicators | Static |
| C2 | Forest plot of HG−H0: equal-fold ΔS_WIS −0.0838 [−0.1044, −0.0655] and ΔS_MAE −0.0783 [−0.1006, −0.0570], plus one row per fold. Fold 3's MAE interval crosses zero and is shown | `uncertainty.csv` |
| C3 | Small multiples of MAE and WIS per fold for v1, v2 and v3 | `metrics.csv` (per_fold) |
| C4 | Crisis window, 2022-08-15 → 08-31 (408 hours, 17 days) | `reports/cp15/peak.csv` for v1/A1; `criteria.csv` criterion 4 for v2/v3 |
| C5 | Hour-of-day MAE profile, v2 against v3. Descriptive; enters only with a claim-map entry | `diagnostics.csv` (hour) |
| C6 | Coverage and mean width at 50/80/95% per generation | `metrics.csv` |

C4 values:

| Generation | MAE | 95% coverage |
|---|---|---|
| v1 | 275.26 | 79/408 |
| A1 | 49.88 | 378/408 |
| v2 | 52.51 | 0.924 |
| v3 | 47.52 | 0.939 |

**Text:**

- **What changed:** three weather features were added to v2.
- **Hypothesis:** forecast wind and solar drive price levels and shape.
- **Result:** HG meets all six §8 criteria as diagnostics, the first evaluated policy to do so.
- **Proof:**
  - frozen and supplementary causal controls, including the r13 lesson;
  - Integration attempt 1 FAIL (line endings), repair r14, then a fresh PASS.
- **Cost:** 2,476 GFS runs, 123,800 messages, 136 GiB transferred, 40.1 machine-hours, $0.
- **Dependency:** a daily GFS retrieval; 2019-01-01 is structurally missing.
- **Pros and cons.**
- **The GFS attribution line.**

### 6.4 v2 chapter (CP-16) with "the road to v2"

- **CP-10 (side branch):** calibration only. Full-fold 95% coverage 55.54% → 71.73%; crisis peak
  19.36% → 32.11%. Not enough.
- **CP-15 (road):**
  - Nine policies; A1 is the best challenger, B2 has better primary scores, and none qualifies
    (`NOT_DEMONSTRATED`).
  - Crisis fold MAE: v1 140.99 against A1 51.21. Matched peak MAE 275.26 → 49.88.
  - This explains why v2 left LightGBM for LEAR.
- **CP-16 (v2 = H):**
  - Chart specs 1–2 from `cp15-cp16-update.md`: the scoreboard with the §8 limits, and the forest
    plot of H−P, H−B2 and P−B2.
  - The H−P MAE upper endpoint is printed in full.
  - H−B2 is an exploratory joint improvement.
  - H and P miss criteria 1–2.
- **Pros and cons.**

### 6.5 v1 chapter

- **Condensed card:**
  - what v1 is;
  - the one-shot holdout, badged confirmatory (MAE 25.9078 vs 27.7578; mean pinball 6.7083 vs
    13.8789; DM p = 1.98e−18);
  - the two unflattering results;
  - the level-versus-shape anatomy of its crisis failure (bias −269.45; level MAE 269.45 against
    shape MAE 66.88, from `peak.csv`).
- **The full current report** follows unchanged, including the fan chart. Long sections may sit in
  `<details>`.

### 6.6 Removed or replaced

- The "Development update · 2026-09-16" card.
- Title, meta description and lede, reframed around the programme. v1's holdout claim stays
  accurate inside its chapter.
- README research lines 18–54, regenerated from the same data layer.
- Space cards gain one line: "The browser demo runs v1; later generations are documented on the
  report."

### 6.7 Claims discipline

Phase A produces `cp20-claims.md` in the format of `cp15-cp16-claims.md`: claim IDs, file/row
sources, gaps and withheld claims. The site renders only mapped claims.

---

## 7. Data layer (single source)

- **`src/delu_forecast/research.py`** loads the committed evidence (CP-10/15/16/20) into typed
  records per generation and policy. `build_pages.py`, `cp3_readme.py` and the MLflow backfill all
  read from it. No research number is typed into a generator.
- **Derived values:** any value not already saved is computed by a committed script whose output
  CSV is committed under `reports/presentation/`. None is expected for Phase D, because C4's
  crisis values are saved.
- **Tests:**
  - every research number on each surface equals its source;
  - no withheld phrasing appears;
  - no v2+ date after 2026-04-07;
  - page size is within budget;
  - chart data equals source rows.

---

## 8. MLflow tracking

### 8.1 What a reviewer should see

- A clear experiment list.
- Nested runs.
- A leaderboard sortable by `s_mae` and `s_wis`.
- Per-fold and daily charts inside MLflow.
- Parameters that fully define each model.
- Lineage tags (code, data, environment, protocol, evidence tag).
- Datasets with digests.
- Artifacts: the same charts as the site, metric tables and a verdict link.
- Short run descriptions.
- A registry with a clear promotion story at the end.

### 8.2 Tracking specification

`docs/track-b/mlflow-tracking-spec.md`, implemented by extending `src/delu_forecast/tracking.py`.

**Experiments:**

- `delu-cp2` stays untouched.
- `delu-generations` holds every research generation.
- `delu-live` comes later, keeping the `live_` wall.

**Hierarchy and names:**

- One parent run per checkpoint ("CP-20 · v3 weather") and one child per policy
  ("CP-20 · HG · v3").
- CP-20's children carry `canonical_comparison=true`. They are the identical-row set behind the
  site scoreboard.

**Metrics (identical names in every run):**

- Equal-fold: `s_mae`, `s_wis`.
- Pooled: `pooled_mae`, `pooled_wis`.
- Per fold as `step = 1..5`: `mae`, `wis`, `rmse`, `bias`, `coverage50/80/95`, `mean_width95`.
- Crisis window: `peak_mae`, `peak_wis`, `peak_coverage95`.
- Daily series: `daily_mae`, with the metric timestamp set to the delivery date so MLflow charts
  show real dates.
- On the candidate run: `delta_s_mae_vs_<baseline>`, with `_ci_low` and `_ci_high`.

**Parameters:** model family, features, weather flag, history window, interval method, blend,
seed, anchor version and protocol SHA256.

**Tags:**

- `generation`, `checkpoint`, `policy_code`;
- `evidence_class`, `adopted`;
- `evidence_tag`, `candidate_sha`, `code_sha`;
- `snapshot_sha256`, `uv_lock_sha256`;
- `backfilled_from=<file>@<sha>` and `original_completed_utc`;
- the run description (`mlflow.note.content`).

**Datasets:** `log_input` for the market snapshot, the GFS features and the evaluation
predictions, each with its digest. If the server lacks support (§8.3), the digests go into tags.

**Artifacts:** metric, criteria and uncertainty slices, chart SVGs, and a README per run linking
the verdict. Every artifact passes the value-based secret scan (`scripts/secret_guard.py`
credentials) before upload. Parameters pass through the existing `redact`.

### 8.3 Capability probe (DagsHub)

Check each of these before the backfill:

- nested runs;
- custom metric timestamps;
- `log_input` datasets;
- run descriptions;
- artifact size limits;
- model-version tags and aliases (for later);
- anonymous access to compare and leaderboard URLs.

Unsupported features degrade to tags and the fallback is recorded.

### 8.4 Backfill scope

About 20 runs, all labelled as backfilled from committed evidence:

- **CP-10:** calibration, as a side branch.
- **CP-15:** nine policies.
- **CP-16:** H, P and the references.
- **CP-20:** H0, HG and the references, as the canonical set.

B1 is v1's development replay. It links to its original record with the tag
`v1_record=delu-cp2/champion::final-fit-and-holdout`.

### 8.5 Verification and site links

- `scripts/verify_mlflow_mirror.py` reads the runs anonymously and requires every mirrored metric
  to equal the data-layer value. It runs at each landing; it is not in CI, because it needs the
  network.
- The backfill writes `reports/presentation/mlflow_index.json`: run IDs and compare URLs. The page
  build reads that committed file, so it stays offline and deterministic. `check_links` covers
  the new URLs.

### 8.6 Workflow from CP-21 on

1. During a checkpoint, the Lead tracks runs in a local file store (`.local/mlruns/<cp>`) and uses
   MLflow to compare candidates. The Critic inspects the same runs.
2. At landing, a publish script uploads the reviewed runs to `delu-generations`, including
   rejected ones, labelled. It then runs the mirror check.
3. Adding this step to the landing templates needs a Lockdown suspension. Until then, each brief
   requires it.
4. The final model is packaged as a runnable `mlflow.pyfunc` policy and registered as
   `delu-day-ahead-policy`. The `champion` alias moves only after 4.7T.
5. Live metrics go to `delu-live` only.

### 8.7 Security

- Credentials are read only from the environment (`AGENTS.md` § Credentials).
- Logging runs only from a process that holds the rotated token, so the Owner's pending restart
  comes first.
- No environment variable is ever logged.
- Every artifact is secret-scanned before upload.
- The git hooks guard commits and pushes.

---

## 9. Phases, outputs and acceptance

| Phase | Tasks | Outputs | Acceptance |
|---|---|---|---|
| **A: content** | CP-20 narrative and claim map; publication pass over the CP-15/16 draft (G9 resolved by Owner decision) | `docs/track-b/research-content/cp20-update.md`, `cp20-claims.md`; updated withheld list | Every statement has a claim ID and file/row source; no withheld phrasing; no post-2026-04-07 content |
| **B: data layer** | `research.py`; tests | module; `tests/test_29_*` (numbers, wording, dates, size) | Tests green; no hand-typed research number in generators |
| **C: MLflow** | C1 spec and module; C2 probe; C3 backfill; C4 mirror check and index | spec doc, `scripts/mlflow_backfill.py`, `scripts/verify_mlflow_mirror.py`, `reports/presentation/mlflow_index.json` | All runs present; mirror check passes; artifacts scanned; links return 200 unauthenticated; `delu-cp2` untouched |
| **D: surfaces** | `build_pages.py` restructure; SVG chart module; README; Space cards; `licensing` claim with GFS; stale card removed | regenerated `docs/index.html`, `README.md`, cards, `app/public/claims.json` | Clean Python 3.12 run of every CI step; `make verify`; `check_links`; zero fetching references; size budget; §4 invariants |
| **E: review and publish** | Owner reviews `docs/index.html` locally, then commit and push. Pages deploys on push. CI green; progress update; Q&A capture | published page | Owner approval; CI green; mirror check still passes |

**Order:** A and B run alongside C1–C2. C3 needs B. D needs A, B and C4. E comes last.

---

## 10. Execution and governance

- **Authority.** One bounded, Owner-authorized presentation task. No locked file changes
  (`AGENTS.md`, templates and anchors untouched); `pyproject.toml` and `uv.lock` untouched.
  Publication happens only after the Owner's visual review.
- **Executor.** This assistant or a fresh executor, working from a brief derived from this plan.
- **Independent check (recommended).** Before the push, a second agent checks the claim maps
  against the rendered page.
- **Cost.** $0: no new paid service and no new dependency (charts are plain Python-generated SVG).
- **Interview capture.** Candidate triggers: presenting post-selection evidence honestly, and why
  MLflow mirrors the repository instead of feeding the page.

---

## 11. Risks and mitigations

| Risk | Mitigation |
|---|---|
| Numbers drift between the page, README and MLflow | One data layer, number-equality tests and the mirror check |
| Overclaiming post-selection results | Evidence badges, the withheld-phrasing test, claim maps |
| Mixing v1's holdout with development numbers | Badge rule; the scoreboard uses development rows only |
| Page bloat by v7 | SVG charts, `<details>`, size-budget test |
| Breaking v1's bound claims | The v1 report generator stays intact; tests 17–24 run on every change |
| Token leak through MLflow artifacts | Value-based scan before every upload |
| DagsHub feature gaps | Capability probe and recorded fallbacks |
| A red public CI | Every CI step reproduced in a clean Python 3.12 checkout before the push |
| Stale derived files | `make wasm-payload` and a page rebuild in the release checklist |
| Post-2026-04-07 data entering v2+ content | Date-guard test |

---

## 12. Forward look

- **Extension chapters.** Each is filled from its checkpoint's committed report and its
  `delu-generations` runs, with the same template, and marked adopted or not adopted.
- **Final model chapter.**
  - Its 4.7T result is the first confirmatory evidence of the new lineage.
  - The window is 2026-04-08 through the test date. The never-published sub-period from
    2026-09-07 is reported separately.
  - Its registry version takes the `champion` alias.
- **Live panel (top).**
  - Today's forecast and "day N of 90", badged prospective, in the `live_` namespace (`test_24`)
    and the `delu-live` experiment.
  - Because the page makes no network calls, a scheduled job commits each day's forecast and
    Pages rebuilds.
  - The daily schedule must resolve the Friday/Shabbat observance explicitly, since the market
    runs every day.
  - Operation requires CP-18 authority.

---

## 13. Questions for the Owner

1. ~~Approve R1–R6 (§2), or amend them.~~ Approved 2026-09-24.
2. Public names for future generations (R3).
3. Executor choice, and whether to require the independent claim check before the push.
4. Whether to add the MLflow landing step to the templates now (needs a suspension) or carry it
   in briefs until later.

---

## Appendix A: policy codes and public names

| Code | Public name | Definition |
|---|---|---|
| B0 | Similar-day naive | Reference and normalizer |
| B1 | v1 | Released LightGBM nine-quantile ensemble with CQR then isotonic; development replay |
| B2 | Daily LEAR | Daily rolling LEAR on the raw target, capped expanding history |
| B3 | Daily LightGBM | Daily rolling LightGBM central forecast, raw target |
| A1 | Normalized LEAR | CP-15 best challenger |
| H0 (V2-H) | v2 | Fixed B2/A1 blend with hour-aware residual intervals (CP-16 H) |
| P | v2 control | The same blend with pooled residual intervals |
| HG | v3 | v2 plus three frozen GFS weather features with missing indicators (CP-20) |
