# Presentation and tracking plan, revision 2: one scrolling history page and MLflow

**Revision 2, 2026-09-24. It awaits the Owner's approval, together with the answers in §16.**

- **R1–R6 stand as approved on 2026-09-24.** Revision 2 changes how two of them are carried
  out: R1's badge wording and R5's publication step. It does not reopen them.
- **Source.** This revision takes in the
  [external presentation review](presentation-review-and-corrections-2026-09-24.md), after the
  checks recorded in §4. Revision 1 is at
  `955510b:docs/track-b/presentation-and-tracking-plan-2026-09-24.md`.
- **Scope:**
  - programme stage 3, presentation around v2 (work items 4.3R, 4.3C and 4.10R);
  - the matching presentation of CP-20 (v3);
  - MLflow as the visible tool for tracking and comparing versions;
  - the design that later generations, the final model and the live model will extend.
- **Approval fixes the design only.** Every public action in this plan is a step that needs its
  own authorization (§13).

---

## 0. Summary

One public page tells the model history, newest first. It opens with three things:

- the working product and its current status;
- a lineage strip, v1 → v2 → v3;
- a fair comparison of every generation on identical evaluation rows.

The chapters follow, newest first:

1. v3;
2. v2, together with the road that led to it;
3. v1, with its original report kept in full.

Later generations, the final model and the live model will be added at the top.

MLflow gets a new public experiment, `delu-generations`.

- **Each evaluated policy appears exactly once,** as a nested run under the checkpoint that
  produced it. Metric names carry their units, and each run holds full metric histories.
- **One committed export is the only payload.** It is reviewed locally, uploaded only after the
  Owner authorizes it, and then checked run by run against the public server.
- **The repository stays the single source of truth.** The page is built from committed evidence
  only. MLflow mirrors that evidence, and a check proves the two agree.

**What revision 2 changes:**

- **Publication order is fixed (F10).** Nothing becomes public before the Owner reviews the
  local page and the MLflow export packet.
- **Chart C2 is split (F06):** one normalized panel, plus per-fold panels in EUR/MWh.
- **v1's badge keeps its exact label (F11):** "confirmatory-style, not power-qualified".
- **New release gates (F01, F02, F04, F05):**
  - the demo starts and runs inference;
  - the page does not overflow on phones;
  - the link checker fails when a link breaks;
  - a generator owns the README research section.
- **A typed evidence and claim layer (F08),** with tests that include negative controls.
- **An exact 23-run MLflow manifest (F09),** with repeatable uploads, a committed export and
  full-history mirror checks.
- **A reader-first design (U01–U06):**
  - the product is visible from the first screen;
  - a lineage strip and a system diagram;
  - a note on how the comparison was kept fair;
  - tool links placed next to the claims they support;
  - a command that rebuilds the page from saved evidence.

| Phase | Where it runs | Deliverable | Indicative effort (agent) |
|---|---|---|---|
| 0 | Local, plus the Owner's devices | Demo diagnosis record (F01) | 1–2 h, plus the Owner's test |
| A | Local | CP-20 content and claim map; publication pass over the CP-15/16 draft | ~0.5 day |
| B | Local | Evidence and claim layer, README ownership, tests | 0.5–1 day |
| C | Local only | MLflow spec, read-only probe, local rehearsal, committed export, publisher and verifier | 1–1.5 days |
| D | Local only | Prototype review (D1), then the full page and surfaces (D2) | 1.5–2 days |
| E | Local | Independent claim and render check, CI-equivalent run, review packet | ~0.5 day, plus the Owner's review |
| F | Public; each step authorized | MLflow upload, index, verification, final build, push, Space redeploy, post-deploy check | ~0.5 day, plus the Owner's actions |

The total is roughly 4.5–6 agent days. This figure is indicative only: it will be re-estimated
after Phase 0 and the capability probe, which are the two largest unknowns.

---

## 1. Corrections to revision 1

| # | What revision 1 said | What is correct | Source |
|---|---|---|---|
| E1 | The HG−H0 forest plot (C2) had "one row per fold" beside the aggregate row. | The equal-fold rows are differences in normalized scores. The per-fold rows are paired mean daily loss differences in EUR/MWh. They cannot share an axis. | F06; estimands in `uncertainty.csv` |
| E2 | Phase C backfilled the public experiment before the Owner's review in Phase E. | The public upload comes after the review packet and needs explicit Owner authorization. | F10 |
| E3 | "`check_links` passes" was listed as an invariant. | It records failures but always exits 0 (`check_links.py:107`), so it is not yet a gate. | F05 |
| E4 | README research lines 18–54 would be "regenerated from the same data layer". | `cp3_readme.py` owns only the span from `## CP-3 showcase and release` to `## Setup` (lines 29–30 and 172–182). No generator owns the research section. | F04 |
| E5 | v1 carried the badge "Confirmatory". | v1's label is "confirmatory-style, not power-qualified" (`HOLDOUT_DM_LABEL` in `claims.py`). | F11 |
| E6 | "The CP-3 registration record lists `tags_refused`, so some DagsHub registry features are limited." | `tags_refused` and `failures` are both empty. The registration succeeded, with its version tags applied. | `reports/cp3/mlflow_registration.json` |
| E7 | The backfill would create "about 20 runs". | Exactly 23 runs (§10.3). | F09 |
| E8 | Only the client version was named (3.16.0). | The DagsHub server reports 3.5.1 (`/version`, 2026-09-24). The probe tests this client–server pair. | F09 |
| E9 | "Phase C runs after the Owner restarts the apps." | Phase C is local and needs no token. Only Phase F's public upload needs one. | F10 |

---

## 2. Goals and non-goals

**Goals:**

- A single scrolling page that is still readable when there are seven generations.
- A full, honest comparison of v1, v2 and v3, available now.
- Every number traceable to a committed file, a row and a claim ID.
- MLflow visibly used for tracking, lineage and comparison.
- A new reader can find all of the following without opening the technical appendix:
  - the product, and which version the demo runs;
  - the main observed improvement;
  - one feature change and one rejected idea;
  - the uncertainty that remains;
  - the route to the evidence.
- Every public route we advertise (the demo, MLflow views) works at the time it is advertised.
- No regression of any public-surface invariant (§6).

**Non-goals now:**

- No new model runs, extensions, fresh-data test (4.7T) or live operation.
- No metric for v2 or a later generation that uses data after 2026-04-07.
- No product, promotion, significance or economic claim.
- No Model Registry entry for HG, because HG is not frozen.
- No research budget spent. The presentation reads saved outputs only; the exhausted CP-20
  analysis and reference passes stay untouched.
- No change to `pyproject.toml` or `uv.lock`. Extra tools, such as a local MLflow 3.5.1 server or
  optional browser automation, live in separate environments under `.local/tools/`.

---

## 3. Decisions

**Taken by the Owner on 2026-09-24:**

1. **One scrolling page,** even with many generations. Chapters run newest to oldest, so
   scrolling down goes back in time.
2. **v2 and v3 are shown publicly now.** Each extension later becomes a chapter, and the live
   model goes at the top at the end.
3. **MLflow becomes the visible tool for comparing versions.** v2 and v3 are backfilled, and
   future work is tracked in it.

**Approved on 2026-09-24, with how revision 2 carries each one out:**

| ID | Approved recommendation | How revision 2 carries it out |
|---|---|---|
| R1 | Move v1's one-shot holdout out of the page header and into the v1 chapter. Do not delete it. | The badge text is exactly "confirmatory-style, not power-qualified" (F11). |
| R2 | Agents build the page and charts from data, and the Owner reviews visually before any push. | Adds a prototype review midway (D1) and an independent claim and render check before the Owner's final review. |
| R3 | Version numbers go only to adopted models. | Unchanged. Names for future generations remain an open question (§16). |
| R4 | The repository is the source of truth, and the page never reads MLflow. | The page reads committed files only, including the committed MLflow index. |
| R5 | Track locally, and publish to DagsHub after landing. | Publishing is an explicit Phase F action that the Owner authorizes after reviewing the committed export (F10). |
| R6 | The Model Registry holds only runnable, frozen policies. | Unchanged. |

---

## 4. How the review's findings are handled

**What was checked, 2026-09-24:**

- The code and data findings were checked by reading the cited lines and files.
- F02 was measured in Claude's built-in browser at 390 × 844.
- F01 was retried the same day.
- The MLflow server version was read from its `/version` endpoint.
- These checks share the review's own limits: one browser engine, and no clean Python 3.12
  run.

| ID | Finding | Our check | Decision | Where |
|---|---|---|---|---|
| F01 | The Hugging Face demo failed to start in the reviewer's browser. | Not reproduced. In Claude's built-in Chromium browser, the direct app computed a forecast after about 40 s ("Recomputed in your browser just now"). The Hugging Face wrapper showed it after about 70 s. There was no error, but the cold start shows only a bare spinner. | Accepted, adapted. Phase 0 diagnoses the demo on the Owner's devices. Startup and inference become a release gate, and loading, failure and fallback states are added. | §7.7, §11, §12 |
| F02 | The page overflows horizontally on phones. | Reproduced. At 390 px, `clientWidth` is 390 and `scrollWidth` is 1,750. Both `.surfaces-table` tables (1,720 px and 746 px) sit outside `.scroll`. | Accepted. | §7.6, §11.3 |
| F03 | Status text that is now stale remains beyond the top card. | Confirmed, with more instances: the published `delu-m4` promise (`claims.py:67–76`, `README.md:254`, the deployed Space), the limitation "the planned v2" (`claims.py:215`) and the `#development-update` link (`build_pages.py:620`). | Accepted. | §8.6 |
| F04 | No generator owns the README research section. | Confirmed (`cp3_readme.py:29–30` and `172–182`). | Accepted. | §9.4 |
| F05 | The link checker always exits 0. | Confirmed (`check_links.py:107`). Its fixed "not deployed" explanation (lines 95–99) is also stale. | Accepted. MLflow links get semantic checks through its REST API; browser checks run outside CI. | §11 |
| F06 | Chart C2 mixes normalized and EUR/MWh units. | Confirmed from the estimand column of `uncertainty.csv`. | Accepted; revision 1 was wrong. | §8.3 |
| F07 | The comparison with v1 needs an explanation. | Confirmed (see the table below). | Accepted. | §8.2 |
| F08 | The contract between claims and data is undefined. | Confirmed gap in the plan. | Accepted, kept proportionate. | §9 |
| F09 | The MLflow contract is incomplete. | Confirmed gap in the plan. The server version, 3.5.1, confirmed. | Accepted. | §10 |
| F10 | The public MLflow upload came before the Owner's review. | Confirmed; revision 1 was wrong. | Accepted, with a new order. | §12, §13 |
| F11 | A plain "Confirmatory" badge strengthens v1's claim; 4.7T and the live panel are unresolved. | Confirmed from the verbatim v1 label in `claims.py`. | Accepted. 4.7T and the live panel become future design decisions. | §7.4, §15 |
| U01–U06 | Reader experience. | Consistent with the Owner's goals. | Accepted. The contribution statement (U05) is the Owner's choice. | §7, §8 |

**Numbers behind F07.** All three figures cover the same 448 development days.

| Figure | Where it is from | What it measures | Reference forecast |
|---|---|---|---|
| "28.58% worse" | v1's own report (DM test, `dm_development.json`) | v1's daily mean absolute error relative to the naive forecast, pooled over all days. The mean daily loss difference is 9.278 EUR/MWh. | The raw similar-day naive, MAE 32.452 EUR/MWh |
| S_MAE 1.0518 | CP-20 scoreboard | v1's MAE divided by the naive's MAE in each fold, then averaged over the five folds | The naive's emitted median after the common residual layer, MAE 32.810 EUR/MWh |
| 41.743 EUR/MWh | Both records | v1's own pooled MAE | — |

---

## 5. Starting point

**The site:**

- `docs/index.html` is 1,014,592 bytes; the review found it byte-identical to the deployed page.
- `scripts/build_pages.py` generates it from `reports/cp2/*.csv` and seven PNG figures embedded
  as `data:` URIs. It is v1's report (sections 1–12), with an interactive SVG fan chart.
- Above that report sits a hand-written card, "Development update · 2026-09-16". It is out of
  date, and its numbers are typed directly into the generator.
- The title, meta description and opening paragraph frame the whole page around v1's holdout.
- On phones the page overflows horizontally (F02).

**The other surfaces:**

- `README.md` is only partly generated (F04).
- The static Space card `space-wasm/README.md`, the Space card `space/README.md` and
  `reports/cp3/mlflow_registration.json` render from `src/delu_forecast/claims.py` (104 claims)
  through `src/delu_forecast/surfaces.py`.
- The `delu-m4` promise appears on every surface, including the deployed Space.

**The guards:**

- Tests 17 and 19–24.
- `make verify` (`scripts/verify_release.py`), which binds the v1 claim set.
- `scripts/check_links.py`, which records link results but never fails (F05).

**MLflow on DagsHub (server 3.5.1; our client is 3.16.0):**

- **One experiment, `delu-cp2`,** with 55 runs. That count includes reproductions that repeat the
  same run names.
- **The canonical v1 run** is `83e475627b6646c885c70f9010c8cf2e`, the registry's source run.
- **One registered model,** `delu-day-ahead-champion`, version 1, alias `champion`, with its
  version tags applied.
- **Nothing from CP-10 onward has been logged.**

**The demo:**

- **In our check,** in Claude's built-in browser: the direct app computed a forecast after about
  40 s, and the Hugging Face wrapper showed it after about 70 s.
- **In the reviewer's browser,** the wrapper showed a CSS preload error and the direct app stayed
  blank.
- **Status:** unresolved (F01).

**The evidence available for the comparison (all committed):**

| Source | Content |
|---|---|
| `reports/weather-ablation/metrics.csv` | B0, B1 (v1's development replay), B2, B3, A1, H0 (v2) and HG (v3), all on the **same 10,747 hours**: per fold, pooled and equal-fold |
| `reports/weather-ablation/uncertainty.csv` | HG−H0 paired intervals for MAE and WIS, equal-fold (normalized) and per fold (EUR/MWh) |
| `reports/weather-ablation/criteria.csv` | §8 criteria 1–6 for H0 and HG, including the matched crisis window |
| `reports/weather-ablation/diagnostics.csv` | Daily rows (90 per fold) and hour-of-day rows (24 per fold) for each policy |
| `reports/v2-causal/{metrics,uncertainty,criteria}.csv` | Seven policies; 36 paired contrasts: H−P, H−B2 and P−B2, equal-fold and per fold |
| `reports/cp15/{per_fold,pooled,relative_scores,peak,daily,bootstrap,criteria}.csv` | Nine policies; 240 paired contrasts; the matched crisis window |
| `reports/cp10/{metrics,selection,peak_windows}.*` | Seven calibration candidates. They use a different score set: nine-quantile pinball, not seven-quantile WIS |
| `reports/cp2/*` | v1 |
| `docs/track-b/research-content/cp15-cp16-{update,claims}.md` | The v2 narrative, chart specifications 1–2 and withheld claims W1–W16 |

**Consistency across checkpoints, checked on 2026-09-24:**

- The references B0, B1 and B2 have identical pooled MAE and WIS in CP-15, CP-16 and CP-20, to
  12 significant digits.
- CP-20's H0 is CP-16's V2-H. CP-20's Integration review found them bitwise identical, and the
  review found their summaries agree to within 1e-12.

**Development folds (identical for every policy):**

| Fold | Delivery days | Days | Hours |
|---|---|---|---|
| 1 | 2020-07-01 → 2020-09-28 | 90 | 2,160 |
| 2 | 2021-04-01 → 2021-06-29 | 90 | 2,159 |
| 3 (crisis) | 2022-07-01 → 2022-09-28 | 88 | 2,112 |
| 4 | 2025-05-01 → 2025-07-29 | 90 | 2,160 |
| 5 | 2026-01-08 → 2026-04-07 | 90 | 2,156 |

**The data boundary:**

- Development ends on 2026-04-07.
- v1 used 2026-04-09 → 06-07 for calibration and 2026-06-09 → 09-06 as its published holdout.
- Nothing after 2026-09-06 has ever been published.

---

## 6. Invariants

These come from the commits that shaped the site (155b0f8, 8341fba, 7f16f4e, 99c9250, 5b94b8f),
from the standing decisions and from this review.

1. **Zero runtime network calls.** Only plain `<a>` navigation and `data:` URIs: no CDN, fonts or
   analytics (CP-3 item 3; `test_19`). New charts are inline SVG.
2. **One claim source for v1.** `claims.py` feeds every surface.
   - `make verify` passes.
   - Rebuild `app/public/claims.json` (`make wasm-payload`) whenever claims change; otherwise
     `test_22` fails.
   - Research claims use the layer in §9.
3. **Fix the generator, not the output.** Never hand-edit `docs/index.html` or a generated README
   block.
4. **v1's honesty statements stay exact:**
   - the development point-MAE DM test: p = 0.948, statistic +1.6228, presented as a deficit;
     the median is 28.58% worse than the naive;
   - 0.194 coverage over the peak weeks of August 2022, together with its mechanism;
   - fold 3 explained as shrinkage toward the training level;
   - crossings 10,158 → 4,412 → 0;
   - "the shipped model is the evaluated model";
   - the four cutoffs and the 152-day staleness;
   - the holdout label, verbatim: "confirmatory-style, not power-qualified".
5. **Every limitation appears on every human surface** (`test_21`).
6. **Every tracking link uses the `.mlflow` host.** The gated repository-UI URLs remain the
   control.
7. **The `live_` namespace wall holds** (`test_24`). Its limits are discussed in §15.
8. **Attribution and licensing appear on every surface.** The GFS line from `DATA-LICENSE.md` is
   added to the `licensing` claim.
9. **The v2 wording rules stand.**
   - W1–W16 apply, extended with W17–W21 (§8.7).
   - The upper end of the H−P MAE interval is printed in full as **+0.000003857628092332211**
     and never rounded.
   - No significance wording.
10. **No v2+ metric uses data after 2026-04-07,** and no v2+ model is scored on v1's holdout
    window.
11. **The labels stay:**
    - `development_post_selection`;
    - CP-15 `NOT_DEMONSTRATED`;
    - "no demonstrated joint preference" is not equivalence;
    - economics are descriptive only.
12. **English only.** Presentation belongs to the Owner, who reviews before anything is
    published.
13. **`pyproject.toml` and `uv.lock` stay byte-identical.**
14. **No public text about retired governance tooling.**
15. **Units are declared.** Every number and every chart series states its metric, unit,
    aggregation, comparator and evidence class. One axis carries one unit (F06).
16. **No placeholder ships.** The final build fails if a marker for an unpublished link remains
    (F10).
17. **Research numbers come only from the evidence layer.** Research sections contain no bare
    numerals (F08).
18. **A generator owns the README research section,** between explicit markers (F04).
19. **Reader routes are advertised only after they pass their check:** demo startup and inference,
    and each MLflow route (F01, F05).
20. **Nothing becomes public before the Owner reviews** the local page and the export packet.
    Every public action is explicitly authorized (§13).
21. **Presentation work spends no research budget:** no fits, scoring passes or data retrieval.

---

## 7. Page design

### 7.1 Structure, top to bottom

1. **Opening (U01).**
   - Two sentences on the problem and the outcome.
   - Three actions: **Try the v1 demo**, **Compare the research models**, **Inspect code and
     evidence**.
   - A status strip:
     - *Released:* v1, which the demo runs.
     - *Latest adopted research model:* v3, development evidence.
     - *Next:* the extension experiments, then the final fresh-data test.
   - The main comparison figure, with its evidence badge beside it.
2. **Lineage strip (U02).** v1 → CP-10 (side branch) → CP-15 (the road) → v2 → v3. Each step has
   a one-line change and one number, and links to its chapter. Below it, a separate "planned,
   not evaluated" list names the extensions, without scores or version numbers.
3. **Scoreboard (§8.2),** with "How we made the comparison fair" beside it (U03).
4. **System view (U03).** One diagram:
   - the flow: source data and vintages → availability checks → feature construction → model and
     interval policy → evaluation and artifacts → report, demo and tracking;
   - where the information cutoff sits and where the leakage controls act;
   - which components are implemented and which are planned.
5. **How to read this page:** the evidence badges, the data boundary and the MLflow paragraph.
6. **Timeline chapters,** newest first: v3, v2 (with the road to it), v1.
7. **Rebuild and reproduce (U05).**
   - A command rebuilds the page and its charts from saved evidence, with no data fetch, fitting
     or research budget. Its runtime is measured before publication.
   - Full experiment reproduction is linked separately.
8. **About this project (U05, optional).** A short contribution statement that the Owner writes
   or approves (§16).
9. **Footer:** licensing and attribution (CC BY 4.0 and GFS) and links.

A sticky timeline rail, built with CSS only, lists every generation with its key number. On
phones it turns into a top bar.

### 7.2 Chapter template (the same for every generation)

**Always visible:**

- **Header strip:** version, date, verdict (adopted / not adopted), evidence badge, and three
  numbers compared with the predecessor.
- **What changed:** the feature or policy change, with a small diagram of the change in the
  pipeline.
- **Hypothesis:** what we expected, as stated before the run.
- **Main comparison:** paired intervals where they are saved, a descriptive change where they are
  not. Units are always explicit.
- **Where it helps and where it hurts:** per fold, the crisis window, hours of the day. Only claims
  with an entry in the claim map.
- **Remaining weakness,** and **why it was adopted or rejected.**
- **Tool links beside the claims they support (U04):** "Open these runs in MLflow", "Read the
  reviewed result", "View the source rows".

**Inside `<details>`:** full tables, protocol detail, review mechanics (failed attempts and
repair identifiers included) and cost detail.

**Rules for every chapter:**

- **Review wording:** "an independent Integration review within this project's process". Never
  "peer review" or "external validation".
- **Main line and side branches:** adopted models form the main line. Experiments that were
  evaluated and rejected appear as side-branch chapters, marked "not adopted, and why".

### 7.3 Navigation and scale

- **Depth sits in `<details>`** (native HTML, no script). Summaries and the main charts stay
  visible, so scrolling alone tells the story.
- **Size budget:** at most 30 KB per new SVG chart, and at most 2.5 MB for the whole page at seven
  generations. A test enforces both.
- **Tested at scale:** the layout is checked locally with representative placeholder chapters for
  v4–v7, which are never published. The aim is usable navigation and readable summaries, not
  just file size.

### 7.4 Evidence badges

| Badge | Used for |
|---|---|
| **Confirmatory-style, not power-qualified** | v1's one-shot holdout, verbatim |
| **Development · post-selection** | CP-10, CP-15, CP-16, CP-20 and the extensions |
| **Prospective** | Reserved for the live model; its design is deferred (§15) |

No badge is promised yet for 4.7T (§15).

Numbers with different badges are never placed side by side as if they were comparable. The
scoreboard shows development rows only, and v1's holdout stays in v1's chapter.

### 7.5 Visual language and accessibility

- **Colour:** one colour per generation, used the same way in the scoreboard, the charts and the
  rail. References (B0, B2, B3) are neutral greys and visually secondary.
- **Charts** are inline SVG generated at build time. Each has text labels, an `aria`
  description and a table alternative. Text is at least 12 px when rendered at a width of 390 px.
- **Interaction:** a visible keyboard focus, keyboard-operable `<details>` and controls, and
  anchors that stay stable.
- **Style:** the current light, report-like look is kept. Final visual choices are the Owner's.

### 7.6 Responsive fixes (F02)

- Put every data table inside `.scroll`, including both `.surfaces-table` tables
  (`build_pages.py:584` and `:615`).
- Let prose cells, URLs and hashes wrap (`overflow-wrap: anywhere` on code and hash cells). Keep
  `nowrap` (`:146`) on numeric columns only.
- Stack the `.kv` grid (`:165`) into one column below about 620 px.
- Keep the fan chart's axis labels readable at 360–390 px, with larger text or fewer ticks at
  small widths.

### 7.7 How the demo is presented (F01)

- **The demo link states what it does:** it runs v1 in your browser; the first visit downloads
  about 57 MB; the measured start time; the date it was last verified.
- **The page's own fan chart is a historical replay:** precomputed, instant and offline. The
  Space, by contrast, runs real inference in the browser. The page labels each accordingly.
- **If Phase 0 confirms failures,** `build_wasm_space.py` adds a visible loading message and a
  failure-and-retry state that links back to the report. The model and its bitwise-equivalence
  gate are not changed.

---

## 8. Content now

### 8.1 Opening and lineage

The opening and the lineage strip follow §7.1. Their figures come from the evidence layer, and
the claim map controls their wording.

Two rules apply:

- The demo is always described as v1.
- Nothing implies that v3 runs in the demo or live.

### 8.2 Scoreboard

Equal-fold scores, development, post-selection. Source: `reports/weather-ablation/metrics.csv`.

| Row | Public name | S_MAE | S_WIS | Emphasis |
|---|---|---|---|---|
| HG | v3 | 0.5658 | 0.5322 | Generation |
| H0 | v2 | 0.6441 | 0.6160 | Generation |
| B2 | Daily LEAR (reference) | 0.6578 | 0.6390 | Reference |
| A1 | Normalized LEAR (CP-15's best challenger; part of v2's blend) | 0.6723 | 0.6460 | Road |
| B3 | Daily LightGBM (reference) | 0.7841 | 0.7399 | Reference |
| B1 | v1, development replay | 1.0518 | 0.9856 | Generation |
| B0 | Similar-day naive (normalizer) | 1.0000 | 1.0000 | Reference |

- **Reference lines:** the §8 limits for criteria 1–2, at 0.59203 (S_MAE) and 0.57509 (S_WIS),
  which is 0.90 × the best of B0–B3; and B0 at 1.00.
- **"How we made the comparison fair":**
  - identical 10,747 hours over 448 days;
  - five folds, one of them the 2022 crisis;
  - fixed score definitions, normalized to the naive forecast;
  - paired moving-block bootstrap: seed 15042, 2,000 replicates, 7-day blocks;
  - an independent Integration review for every generation;
  - the limits that apply.
- **The F07 note (draft):** "Why v1 scores 1.05 here but '28.58% worse' in its own report. Both
  numbers describe the same 448 development days. v1's report compared its daily absolute error
  with the raw similar-day naive (MAE 32.45 EUR/MWh) and pooled all days, so the 2022 crisis
  dominates. This scoreboard gives each of the five folds equal weight, and its naive reference
  is the forecast's emitted median after the common residual layer (MAE 32.81 EUR/MWh). v1's own
  error is 41.74 EUR/MWh in both. v1's original nine-quantile pinball is a different score from
  the seven-quantile WIS used here." A definition of each metric is available in an expandable
  section.

### 8.3 v3 chapter (CP-20)

**Charts:**

| # | Chart | Unit | Source |
|---|---|---|---|
| C1 | Diagram of the GFS box (47–55.25°N, 5.5–15.5°E) and the feature recipe: per-cell wind speed at 10 m and 100 m, then an area average; DSWRF de-averaged; missing indicators | — | Static |
| C2a | Equal-fold HG−H0: ΔS_MAE −0.0783 [−0.1006, −0.0570]; ΔS_WIS −0.0838 [−0.1044, −0.0655] | Normalized score (ratio to B0) | `uncertainty.csv`, `equal_fold` |
| C2b | HG−H0 per fold, MAE and WIS in separate panels. Fold 3's MAE is −3.18 [−6.09, +0.037]; its crossing of zero is drawn visibly | EUR/MWh, paired mean daily loss difference | `uncertainty.csv`, `fold_1`–`fold_5` |
| C3 | MAE and WIS per fold, as small multiples for v1, v2 and v3 | EUR/MWh | `metrics.csv`, `per_fold` |
| C4 | Crisis window, 2022-08-15 → 08-31 (408 hours, 17 days) | EUR/MWh; hits out of 408 | `reports/cp15/peak.csv` for v1 and A1; `criteria.csv` criterion 4 for v2 and v3 |
| C5 | MAE by hour of day, v2 against v3. Descriptive, and shown only with a claim-map entry | EUR/MWh | `diagnostics.csv`, `hour` |
| C6 | Coverage and mean interval width at 50%, 80% and 95% for each generation | Fraction; EUR/MWh | `metrics.csv` |

Chart C2 does not invent normalized confidence intervals per fold, because that would be a new
estimand needing an authorized analysis.

**C4 values:**

| Generation | MAE (EUR/MWh) | 95% interval hits |
|---|---|---|
| v1 | 275.26 | 79/408 |
| A1 | 49.88 | 378/408 |
| v2 | 52.51 | 377/408 |
| v3 | 47.52 | 383/408 |

**Text:**

- **What changed:** three weather features were added to v2.
- **Hypothesis:** forecast wind and solar drive both the level and the shape of prices.
- **Result:**
  - the joint improvement rule is met;
  - all five folds favour v3, and fold 3's MAE interval crosses zero;
  - v3 meets all six §8 criteria as diagnostics, the first evaluated policy to do so.
- **Caveats (U02):**
  - The gain belongs to the three-feature bundle. No experiment isolates the effect of any one
    feature.
  - All results are development evidence, post-selection.
- **Proof, in plain words:**
  - Frozen causal controls ran as planned.
  - Supplementary controls were added after we found that one frozen check could not fail.
  - The first independent review failed on a byte-level reproducibility defect. The defect was
    repaired, and a fresh review passed.
  - The repair identifiers stay inside `<details>`.
- **Cost:**
  - 2,476 GFS runs and 123,800 messages;
  - 136 GiB transferred;
  - 40.1 machine-hours, from the final Integration record;
  - $0.
- **Dependency:** a daily GFS retrieval. 2019-01-01 is structurally missing.
- **Pros and cons.**
- **The GFS attribution line.**

### 8.4 v2 chapter, with the road to v2

**CP-10, a side branch: calibration only.**

- Full-fold 95% coverage rose from 55.54% to 71.73%, and crisis-peak coverage from 19.36% to
  32.11%.
- That was not enough.

**CP-15, the road.**

- Nine policies were compared. A1 was the best challenger, B2 had better primary scores, and none
  qualified (`NOT_DEMONSTRATED`).
- Crisis fold MAE: v1 140.99, A1 51.21. Matched peak MAE: 275.26 → 49.88.
- This explains why v2 moved from LightGBM to LEAR.

**CP-16, where v2 is V2-H.**

- **Charts:** chart specifications 1–2 from `cp15-cp16-update.md`. Both use equal-fold rows, so
  their units are consistent.
- **H−P:** no demonstrated joint preference. The upper end of the MAE interval is printed in
  full.
- **H−B2:** an exploratory joint improvement. It is not attributed to hour-aware intervals
  alone (U02, W4, W5).
- **Criteria:** H and P both miss criteria 1–2.
- **Pros and cons.**

### 8.5 v1 chapter

**A condensed card:**

- what v1 is;
- the one-shot holdout, under its exact badge: MAE 25.9078 against 27.7578, mean pinball 6.7083
  against 13.8789, DM p = 1.98e−18;
- the two unflattering results;
- the anatomy of its crisis failure, which was about price level rather than shape (bias
  −269.45; level MAE 269.45 against shape MAE 66.88, from `peak.csv`).

**The full current report** follows unchanged, including the fan chart. Its long sections can sit
inside `<details>`.

The fan chart's behaviour must be preserved:

- moving the load scenario from ×1.00 to ×1.02 hides the actual-price line and shows the scenario
  caveat;
- choosing the 95% level shows an empirical coverage of 0.9398.

### 8.6 Stale text to reconcile (F03)

| Location | Now | Change |
|---|---|---|
| `build_pages.py:325–348` | The "Development update · 2026-09-16" card | Remove it. Keep `#development-update` as an alias for the new status section, or repoint the link at `:620`. |
| `claims.py:67–76` (`MLFLOW_NEXT_EXPERIMENT = "delu-m4"` and its note) | "No v2 run exists yet …", on every surface and in the deployed Space | Describe `delu-generations` instead (Q6). This requires a Space redeploy in Phase F. |
| `claims.py:215` (a limitation) | "the defect the planned v2 targets" | "the defect later generations address (see the v2 and v3 chapters); it is not fixed in the released v1". The 0.194 figure and its mechanism are unchanged. |
| `README.md:18–54` | A hand-written "Current development" section that says CP-16 needs a brief | A block owned by the generator (§9.4) |
| Page title, meta description, opening paragraph | Framed around v1's holdout | Framed around the programme; v1's holdout moves to its chapter |
| Page §12 tracking note | Written before the current plan | Updated |
| `space-wasm/README.md`, `space/README.md`, `app/public/claims.json` | Carry the claims above | Rebuilt; the deployed Space is redeployed in Phase F if its content changed |

A test enforces this. A list of pending-status phrases ("needs a brief", "planned v2", "No v2 run
exists", "not yet") must not appear describing work that has already landed.

### 8.7 Claims discipline

Phase A produces `docs/track-b/research-content/cp20-update.md` and `cp20-claims.md`, in the
format of `cp15-cp16-claims.md`: claim IDs, file and row sources, gaps and withheld claims. The
site renders mapped claims only.

**New withheld claims:**

| ID | Withheld claim |
|---|---|
| W17 | Attributing the weather gain to any single feature (10 m wind, 100 m wind or DSWRF) |
| W18 | Calling the Integration review "peer review" or "external validation" |
| W19 | Stating or implying that v3 runs in the demo or live |
| W20 | Comparing v3 with v1 as a headline ratio without the scoreboard's definition (equal-fold weighting, emitted-median naive reference) and the development label |
| W21 | Calling v1's holdout "confirmatory" without "-style, not power-qualified" |

---

## 9. Evidence and claim layer (F08)

### 9.1 Modules

- **`src/delu_forecast/research.py`** loads typed evidence records from the committed files of
  CP-10, CP-15, CP-16 and CP-20. It never scores anything.
- **`src/delu_forecast/research_claims.py`** holds the research claims:
  - a claim ID;
  - the approved wording template;
  - the record IDs the claim binds;
  - the surfaces it may appear on;
  - its status, published or withheld.
- **`claims.py`** keeps v1's bound claims, with only the reconciliation edits from §8.6. v1's
  strings are never reused as descriptions of later generations.
- **Consumers:** `build_pages.py`, the README generator and the MLflow export all read these two
  modules. No generator contains a typed research number.

### 9.2 Evidence record

| Field | Example |
|---|---|
| `record_id` | `cp20.metrics.HG.equal_fold.S_MAE` |
| `checkpoint`, `generation`, `policy_code` | `CP-20`, `v3`, `HG` |
| `source_path`, `source_revision` | `reports/weather-ablation/metrics.csv`; tag `evidence/cp-20` plus the file's Git blob SHA |
| `row_selector` | `{policy: HG, scope: equal_fold}` |
| `metric`, `unit` | `S_MAE`, a ratio to B0 · `MAE`, EUR/MWh · `coverage95`, a fraction · `hits95`, a count |
| `aggregation` | `equal_fold`, `pooled`, `per_fold`, `peak_window`, `daily`, `hour` |
| `population_id` | `common-10747h` |
| `comparator` | The normalizer (B0) or the paired baseline |
| `interval` | Method, level, seed and replicates, when an interval exists |
| `evidence_class` | `development_post_selection`, `confirmatory_style_not_power_qualified`, `development_calibration_comparison` |
| `window` | The first and last delivery dates of the evaluated rows |
| `display_precision` | For example, 4 decimals |

### 9.3 Renderer contract

- **On the page,** every research figure renders as
  `<data value="…" data-claim="…" data-record="…">…</data>`. The `<data>` element is standard
  HTML and costs nothing to render.
- **In the README,** the owned block is rendered from the same claim templates.
- **Charts** take typed series objects. Each series carries its unit, and the renderer refuses to
  put two units on one axis.

### 9.4 README ownership (F04)

- The research section sits between `<!-- research:start -->` and `<!-- research:end -->`.
- A generator owns it. It fails if either marker is missing or duplicated, and it is idempotent.
- The rest of the README is not touched. `cp3_readme.py` keeps its own span.

### 9.5 Tests (offline, run in CI)

| Test | What it checks | Negative controls |
|---|---|---|
| `test_29_research_evidence.py` | Every record re-derives from its source row and revision. References are identical across CP-15, CP-16 and CP-20, and H0 equals V2-H. | A wrong row, policy, aggregation, unit or revision fails. |
| `test_30_research_claims_rendered.py` | Every `data-claim` exists in the claim layer and the claim map, and every published claim is rendered. Withheld phrases are absent. Research sections contain no bare numerals, apart from an allowlist of years and fold indices. Date guard: a v2+ record must have `window.last` ≤ 2026-04-07. v1 holdout records must carry the exact label. The guard reads typed fields, not prose. Unit guard. The placeholder guard applies to the final build. | A mixed-unit axis raises an error. A post-boundary window fails. A missing claim ID fails. |
| `test_31_page_structure.py` | Every table sits inside `.scroll`. Internal anchors resolve. The size budget holds. The fan chart's scenario caveat and its 0.9398 coverage are present. | A table outside `.scroll` fails. |
| `test_32_readme_ownership.py` | The markers appear exactly once. Running the generator twice gives identical output. A fixture change updates the block. Bytes outside the block are unchanged. | A missing marker fails clearly. |
| `test_33_check_links_gate.py` | A required URL that fails gives a nonzero exit. Local documentation examples are classified as non-destinations. | A mocked 404 fails. |
| `test_34_mlflow_export.py` | The export is deterministic, and the manifest lists exactly 23 runs. Metric names carry units. Comparability IDs are consistent. The outbound scan runs. | A fake credential in the payload blocks the export, and its value is never printed. |

Existing tests 17–24 and 28 keep running on every change.

---

## 10. MLflow tracking (F09)

### 10.1 What a reviewer should see

- **Each policy exactly once,** in one experiment, as nested runs under its checkpoint.
- **A leaderboard** that sorts by `s_mae` and `s_wis`.
- **Charts per fold and per day,** inside MLflow itself.
- **Parameters** that define each model, and **tags** that show lineage and provenance.
- **Datasets with digests,** where the server supports them.
- **Artifacts:** the site's charts, the run's summary and links to its verdict.
- **Short run descriptions.**
- **A registry** that tells a clear promotion story at the end (R6).

### 10.2 Structure and naming

- **Experiments:**
  - `delu-cp2` stays untouched, including its 55 runs.
  - `delu-generations` is new.
  - `delu-live` comes later, to keep the `live_` wall.
- **Runs:** one parent per checkpoint, with one child per policy that the checkpoint produced
  first. Each policy is logged once.
  - The references come from CP-15, where they were produced.
  - v2 is CP-16's V2-H, and CP-20's H0 is the same policy.
  - `test_29` ties CP-20's figures to these runs.
- **Run names:** "CP-20 · HG · v3", "CP-16 · V2-H · v2", "CP-15 · B1 · v1 development replay".

### 10.3 Exact run manifest (23 runs)

| Parent `run_key` | Child `run_key`s | Children |
|---|---|---|
| `cp10` "CP-10 · calibration only (side branch)" | `cp10/v1_reference`, `cp10/c1_head_spread`, `cp10/c1_price_volatility` (selected), `cp10/c2_aci_gamma_0.000001`, `cp10/c2_aci_gamma_0.000005`, `cp10/c2_aci_gamma_0.00001`, `cp10/c2_aci_gamma_0.00002` (selected γ) | 7 |
| `cp15` "CP-15 · adaptive feasibility (road to v2)" | `cp15/B0`, `cp15/B1` (v1 development replay), `cp15/B2`, `cp15/B3`, `cp15/A1`, `cp15/A2`, `cp15/A3`, `cp15/A4`, `cp15/A5` | 9 |
| `cp16` "CP-16 · v2" | `cp16/V2-P` (control), `cp16/V2-H` (v2) | 2 |
| `cp20` "CP-20 · v3 weather" | `cp20/HG` (v3) | 1 |

That makes 4 parents and 19 children.

- **Comparability:** CP-10 carries its own comparability ID. CP-15, CP-16 and CP-20 share one
  (§10.5).
- **Link to v1's record:** `cp15/B1` carries `delu.v1_record_run=83e475627b6646c885c70f9010c8cf2e`.

### 10.4 Metrics

Every metric name carries its unit. The same names are used in every run.

| Name | Unit | Where it appears |
|---|---|---|
| `s_mae`, `s_wis` | Ratio to B0, equal-fold | Comparability group of CP-15/16/20 |
| `pooled_mae_eur`, `pooled_wis_eur`, `pooled_rmse_eur`, `pooled_bias_eur`, `pooled_coverage95` | EUR/MWh; fraction | All runs |
| `fold_mae_eur`, `fold_wis_eur`, `fold_coverage50`, `fold_coverage80`, `fold_coverage95`, `fold_mean_width95_eur` | EUR/MWh; fraction. History with step = fold 1–5, timestamp = the fold's last delivery date | All runs |
| `peak_mae_eur`, `peak_wis_eur`, `peak_coverage95`, `peak_hits95` | EUR/MWh; fraction; count | Wherever a crisis-window row exists |
| `daily_mae_eur` | EUR/MWh. History with step = day index, timestamp = the delivery date | Where daily rows are committed (CP-15; CP-20 diagnostics) |
| `delta_s_mae_vs_<base>`, `delta_s_wis_vs_<base>`, each with `_ci_low` and `_ci_high` | Difference in normalized score | Candidate runs: HG vs V2-H; V2-H vs V2-P and B2; V2-P vs B2; CP-15's bootstrap contrasts |
| `delta_fold_mae_eur_vs_<base>`, `delta_fold_wis_eur_vs_<base>`, with CI histories | EUR/MWh, paired mean daily loss difference, step = fold | The same candidate runs |
| `fold_pinball9_eur` | EUR/MWh, nine-quantile pinball | CP-10 only; it has no `s_` metrics |

### 10.5 Parameters, tags, provenance and comparability

**Parameters.** Only what the committed protocol states:

- model family, target transform, history window and blend;
- interval method;
- weather features, `none` or the list of three plus their indicators;
- quantile set, seed, anchor version and protocol SHA256.

A value that is unknown is left out, never guessed.

**Tags:**

- **Identity:** `delu.run_key`, `delu.checkpoint`, `delu.generation`, `delu.policy_code`.
- **Role and status:** `delu.role` (candidate, reference or control), `delu.adopted`,
  `delu.evidence_class`.
- **Comparability:** `delu.population_id` and `delu.comparability_id`.
  - The comparability ID is a SHA256 over: the sorted evaluation keys; the target definition and
    unit; the score and quantile definitions; the aggregation; and the reference policy
    definition.
  - Matching metric names alone do not establish that two runs are comparable.
- **Provenance, kept separate:**
  - `delu.model_code_sha`: the checkpoint's final candidate SHA;
  - `delu.evidence_ref`: for example, `evidence/cp-20@a7a9b2e`;
  - `delu.source_blobs`: each source path mapped to its blob SHA;
  - `delu.backfill_tool_sha`: the commit of the export and publish scripts. It is never stamped
    as the model's code.
- **Backfill markers:** `delu.backfilled=true`, and `delu.original_completed_utc`. That value
  comes from the checkpoint return; if the return does not give it, the value is `unknown`.
- **Upload state:** `delu.upload_state` and, on each parent, `delu.package_complete`.
- **MLflow built-ins:** `mlflow.parentRunId` for nesting, and `mlflow.note.content` for the
  description.

### 10.6 Datasets and artifacts

- **Datasets,** through `log_input` if the probe shows support:
  - the evaluation population (a digest of its key list);
  - the market snapshot (its SHA256);
  - the GFS features (the SHA256 of `weather-features.parquet`, for HG only).

  Without support, the digests stay in tags, and the page does not advertise dataset views.
- **Artifacts:**
  - `summary.json`, the run's exact entry in the export;
  - the site's SVG charts, for candidate runs;
  - a `README.md` with links to the report, the verdict, the landing record and the source rows
    at the evidence tag.

### 10.7 Committed export and repeatable publishing

- **The export.** `scripts/mlflow_export.py` writes a deterministic
  `reports/presentation/mlflow-export/{cp10,cp15,cp16,cp20}.json`, plus a `manifest.json` that
  lists the 23 `run_key`s, their parents and each run's expected metric keys and history lengths.
  The export is committed, so the pre-commit secret guard scans it.
- **The publisher.** `scripts/mlflow_publish.py --dry-run | --target local | --target public`:
  1. **It uploads only committed export files,** and refuses when the working tree differs from
     `HEAD`.
  2. **It is idempotent.** For each `run_key` it first searches by the `delu.run_key` tag:
     - a complete run is skipped;
     - an incomplete run is resumed, and only the missing metrics, history points and artifacts
       are logged;
     - otherwise the run is created.
  3. **It marks packages complete only after verification.** A parent is set to
     `delu.package_complete=true` only after all its children are complete and verified.
  4. **Public uploads need explicit Owner authorization,** recorded in the upload log (§13).
- **The index.** After the public upload, `reports/presentation/mlflow_index.json` maps each
  `run_key` to its public run ID, experiment ID and UI routes. It is committed, and the page build
  reads it. This mapping replaces the run IDs of the local rehearsal.

### 10.8 Scanning the outbound payload

The publisher checks every outbound string and every artifact byte against the credential values
from `scripts/secret_guard.py`. This covers parameters, tags, notes and metric keys, and it covers
every path, including partial failures. On a hit it aborts without printing the value.

This extends `redact()` in `tracking.py`, which masks only the DagsHub token, and only in
parameter strings.

### 10.9 Capability probe, with no public writes

1. **Read-only, against the public server:**
   - read `/version` (3.5.1);
   - check which fields `runs/search` on `delu-cp2` returns, including inputs and notes;
   - check anonymous access to experiment and run routes.
2. **Local rehearsal:** a 3.5.1 server in `.local/tools/mlflow-3.5.1/` (a separate `uv` venv; the
   project's `uv.lock` is not touched), used with the project's 3.16.0 client. It tests:
   - nesting;
   - metric timestamps and history lengths;
   - `log_input` and notes;
   - artifact sizes;
   - search by tag;
   - resuming an interrupted upload.
3. **A write probe on DagsHub** would create public records. It runs only if the Owner authorizes
   it (Q5), in a throwaway experiment that is deleted afterwards.

Results are recorded in `reports/presentation/mlflow-capabilities.json`. When a feature is not
supported, the fallback is recorded as well:

- A tag can preserve a digest or a parent ID.
- A tag cannot replace a missing chart or a comparison workflow. When one is missing, the page
  does not promise that function.

### 10.10 Mirror verification and reader routes

- **Mirror check.** `scripts/verify_mlflow_mirror.py --target local | public` reads the runs
  anonymously. It checks that:
  - every `run_key` exists exactly once;
  - the parent links are right;
  - the parameters and tags match;
  - every metric history matches by key, step, timestamp and value;
  - every artifact's SHA256 matches.

  In the rehearsal it must catch two deliberate faults: a deleted history point and an altered
  digest.
- **Reader routes:** run pages, comparison views for each checkpoint, and a leaderboard or search
  route.
  - **The REST check.** The run and experiment IDs are parsed from each route's fragment, and
    `runs/get` must return the right `run_key`.
  - **The browser check.** A real browser confirms that the comparison view renders
    anonymously. It is recorded in the release checks.

  A route is advertised only after both checks pass.

### 10.11 Workflow from CP-21 on

1. **During the checkpoint:** the Lead tracks runs in `.local/mlruns/<cp>`, using the same names
   and tags.
2. **In the checkpoint's evidence:** its committed export JSON, which is durable and which the
   Critic reviews.
3. **At landing:** publication follows the same authorized sequence as Phase F.
4. **In the templates:** adding this step to the landing templates needs a Lockdown suspension
   (Q4). Until then, each brief requires it.
5. **For the final model:** it is registered as a runnable `mlflow.pyfunc` policy
   (`delu-day-ahead-policy`). The `champion` alias moves only under the protocol settled in §15.
6. **For live operation:** live metrics go to `delu-live` only.

---

## 11. Verification gates

### 11.1 Offline, in CI on every push

- Existing tests 17–24 and 28, and new tests 29–34 (§9.5).
- `make verify`.
- The zero-fetch scan (`test_19`).

### 11.2 Release checks, which need the network and run outside CI

- **`check_links.py`, repaired (F05):**
  - it exits nonzero when a required public destination fails;
  - it classifies local development URLs and command examples explicitly;
  - it records the observed error and the check date, instead of a fixed explanation.
- **Semantic MLflow route checks** (§10.10).
- **The mirror verifier.**

### 11.3 Browser checklist, run by hand and recorded

The results go to `reports/presentation/release-checks/<date>.json`, with the browser, device,
app revision and outcome.

| Surface | Checks | Devices |
|---|---|---|
| Report | At 390 px and 360 px, `scrollWidth ≤ clientWidth`. The rail or top bar works. `<details>` and the controls work from the keyboard, with a visible focus. Charts are readable. The fan chart keeps its ×1.02 and 95% behaviour (§8.5). | Desktop Chrome and Safari; iPhone Safari |
| Demo | From a cold start to a visible forecast, timed. A level change works, and a scenario change works. The failure-and-retry state and the link back to the report work. | The same |
| MLflow | Every advertised route renders its intended run or comparison anonymously. | Desktop |

HTTP 200 responses, and old equivalence or load records, do not count as a substitute for these
checks.

Optional automation: a `scripts/check_reader_paths.py` that runs only when Playwright is
installed in a separate tool environment under `.local/tools/`. It never runs in CI and never
touches `uv.lock`.

### 11.4 Reader walkthrough (U06)

Two readers each go through the page: the independent checker (an agent without context) and
the Owner. Each confirms they can identify:

- the product, and which version the demo runs;
- the main observed improvement;
- one feature change and one rejected idea;
- the uncertainty that remains;
- the route to the evidence.

---

## 12. Phases, order and acceptance

| Phase | Tasks | Outputs | Acceptance |
|---|---|---|---|
| **0: Demo diagnosis** | The Owner opens both demo URLs on iPhone Safari and on desktop. The executor reproduces on desktop engines and, if it fails, captures the console and network. No code changes before a reproduction. | `release-checks/<date>-demo.json`; a fix plan | Diagnosis recorded. If the failure is not reproducible, the loading and fallback improvements still go ahead in D2. |
| **A: Content** | CP-20 update and claim map. A publication pass over the CP-15/16 draft (G9 resolved by the Owner's decision). The F07 text. The U02 caveats. W17–W21. Review wording. | `cp20-update.md`, `cp20-claims.md`; an updated withheld list | Every statement has a claim ID and a file/row source. No withheld phrasing. No v2+ content after 2026-04-07. |
| **B: Evidence layer** | `research.py`, `research_claims.py`, the README markers and generator, tests 29–32 | Modules and tests | Tests green, negative controls included. No typed research number in any generator. |
| **C: MLflow preparation, local only** | Spec doc (`docs/track-b/mlflow-tracking-spec.md`). The read-only probe. The local rehearsal, including an interrupted upload that resumes and the deliberate faults. The export and manifest. A publisher dry run. Test 34. | Export files, `mlflow-capabilities.json`, the scripts | The rehearsal's verifier passes. An interrupted upload resumes without duplicates. The deliberate faults are caught. No public write. |
| **D1: Prototype checkpoint** | The opening, lineage strip, scoreboard and v3 chapter, rendered locally with placeholders for unpublished links | A local page | The Owner reviews density, style and evidence links before the template is rolled out further. |
| **D2: Full page and surfaces** | The v2 chapter (with its road) and the v1 chapter. The rail and the system view. The rebuild command. The fixes for F02, F03 and F05, and the demo presentation (F01). The README block. The Space cards and `app/public/claims.json`. Test 33. | Generated page, README and cards | Tests 17–34 green. `make verify`. No fetches. The size budget holds. The §11.3 report checks pass locally at 390 px and 360 px. |
| **E: Review packet** | An independent claim and render check, with the reader walkthrough. A clean Python 3.12 CI-equivalent run. The release checks. A packet for the Owner: the local page, the export, the manifest, the capability record and the checklist results. | The packet | The Owner approves the content, and explicitly authorizes (or declines) the public MLflow upload. |
| **F: Publication** | F1: upload the committed export (authorized). F2: commit the index. F3: public mirror verification and route checks. F4: the final build with real links (placeholder guard). F5: the Owner's final visual approval. F6: commit and push. F7: redeploy the Space if its content changed (authorized). F8: post-deploy checks of the Pages bytes, demo startup and inference, and the MLflow routes. | Public experiment; published page; release-check record | Every step passes in order. If F3 fails, stop: the page is not published with broken routes. |

**Order:**

- Phase 0 and phases A, B and C can run in parallel.
- D1 needs A and B. D2 needs D1 and C's export.
- E needs C and D2. F comes last.

---

## 13. Authority and governance

| Action | Performed by | Requires |
|---|---|---|
| Local work in phases 0–E | Executor | Approval of this revision and the Owner's instruction to execute |
| Committing local work | The Owner, or the executor on explicit instruction | Per task |
| Any public MLflow write: the probe or the upload | The executor or the Owner | Explicit Owner authorization, after reviewing the export packet |
| Pushing to `origin`, which publishes the Pages site | The Owner, or the executor on explicit instruction | The Owner's final visual approval |
| Redeploying the Hugging Face Space | The Owner, or the executor on explicit instruction | The same. `HF_TOKEN` is used only as a stored variable. |
| Editing locked files, such as adding the MLflow step to the landing templates | Owner suspension | Q4 |

**Notes:**

- **Delegation.** By default, `AGENTS.md` reserves commits and pushes to `main` for the Owner.
  The Owner has delegated both for specific tasks, as on 2026-09-24. The ordering rule from F10
  applies whoever performs the action.
- **Files that stay untouched:** no locked file changes (`AGENTS.md`, the templates, the
  anchors), and `pyproject.toml` and `uv.lock` stay unchanged.
- **Credentials** are used only as stored variables (`AGENTS.md` § Credentials).
- **Cost:** $0. No paid service and no new project dependency; charts are plain SVG generated in
  Python.
- **Independent check.** A fresh agent, with no context from the build, checks the claim maps
  against the rendered page before the Owner's final review. This review is not that check.
- **Interview capture.** Possible triggers:
  - presenting post-selection evidence honestly;
  - why MLflow mirrors the repository instead of feeding the page;
  - the unit-mixing error that the review caught.

---

## 14. Risks and mitigations

| Risk | Mitigation |
|---|---|
| The demo fails for some visitors (F01) | Phase 0; loading and fallback states; a startup gate; the verified date shown next to the link |
| Mixed units or misleading intervals (F06) | Typed series; a unit guard with a negative control |
| Old "pending" wording survives (F03) | The reconciliation list; the phrase guard |
| The link check reports success falsely (F05) | Exit-code gate; a mocked-404 control; semantic route checks |
| Duplicate or partial MLflow packages, or drift (F09) | `run_key` idempotency; a completion flag per package; a verifier over the full history |
| Publication before review (F10) | Phase F order; explicit authorization for each public action |
| v1's claim is overstated (F11) | The verbatim label, tested; W21 |
| Server–client mismatch (3.5.1 vs 3.16.0) | Local 3.5.1 rehearsal; verification after upload |
| A token leaks through MLflow | Committed export scanned by the pre-commit guard; outbound scan of every field |
| Numbers drift between page, README and MLflow | One evidence layer; the renderer contract; the mirror check |
| Overclaiming post-selection results | Evidence badges; claim maps; W1–W21 |
| The page grows too large by v7 | SVG charts; `<details>`; the size budget; placeholder chapters at scale |
| The effort estimate is wrong | Re-estimate after Phase 0 and the probe; the D1 checkpoint |
| Public CI turns red | A clean Python 3.12 CI-equivalent run before any push |
| `uv.lock` drifts | Tools live in separate environments under `.local/tools/` |
| v2+ data after 2026-04-07 slips into the content | A date guard on typed fields |

---

## 15. Forward look

- **Extension chapters.** Each one is filled from its checkpoint's committed report and its
  `delu-generations` runs, using the same template, and is marked adopted or not adopted.
- **The final model and 4.7T.** Before the page promises any badge for the result, the 4.7T
  protocol must settle three things:
  1. the overlap between candidate windows and periods already evaluated and published for v1:
     calibration 2026-04-09 → 06-07, and the holdout 2026-06-09 → 09-06;
  2. the anchor's requirement of at least 90 consecutive days after a policy freeze for
     prospective evaluation;
  3. what the result can honestly be called.

  The page reserves a slot for the result. The period from 2026-09-07, which has never been
  published, is reported separately.
- **The live panel.** It needs:
  - a data and claim builder of its own;
  - a clear boundary on the shared page;
  - negative controls of its own.

  `test_24` checks only the keys of `build_claims()`, so live values rendered from another source
  would get past it. It must be extended.

  Daily automated commits and publication need a future authorization (CP-18). The daily schedule
  must also resolve the Friday and Shabbat observance.

---

## 16. Questions for the Owner

1. **Approve revision 2.**
2. **Public names for future generations** (R3). Carried over from revision 1.
3. **Executor, and whether the independent claim and render check is required.** Recommended:
   required.
4. **The MLflow landing step:** add it to the templates now (needs a suspension), or carry it in
   briefs?
5. **The capability probe:** local rehearsal only (recommended), or also an authorized write
   probe on DagsHub in a throwaway experiment?
6. **Rename the published `delu-m4` slot to `delu-generations` on every surface?**
   Recommended. It needs a Space redeploy in Phase F so the deployed Space matches.
7. **The contribution statement (U05):** include it or not? If yes, the Owner writes or approves
   the wording. Recommended: short and factual, including that development was assisted by AI
   agents.
8. **The demo test for Phase 0:** open both demo URLs on your iPhone (Safari) and on desktop, and
   report what you see.

---

## Appendix A: policy codes and public names

| Code | Public name | Definition |
|---|---|---|
| B0 | Similar-day naive | Reference and normalizer (emitted median after the common residual layer) |
| B1 | v1 | The released LightGBM nine-quantile ensemble, calibrated with CQR and then isotonic regression. Shown as its development replay. |
| B2 | Daily LEAR | Daily rolling LEAR on the raw target, with capped expanding history |
| B3 | Daily LightGBM | Daily rolling LightGBM central forecast on the raw target |
| A1 | Normalized LEAR | CP-15's best challenger; part of v2's blend |
| A2–A5 | CP-15 challengers | Other adaptive policies from CP-15; not adopted |
| V2-H (H0) | v2 | The fixed B2/A1 blend with hour-aware residual intervals (CP-16 H). CP-20's H0 is the same policy. |
| V2-P | v2 control | The same blend with pooled residual intervals |
| HG | v3 | v2 plus three frozen GFS weather features and their missing indicators (CP-20) |
| `v1_reference`, `c1_*`, `c2_aci_gamma_*` | CP-10 candidates | Calibration-only variants of v1; side branch; nine-quantile scores |
