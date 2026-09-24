# Presentation and tracking plan, revision 3: one scrolling history page and MLflow

**Revision 3, approved by the Owner on 2026-09-24, together with the decisions in §16.** It is
executed as task PRES-1 under the [Engineering Lead brief](pres-1-brief-2026-09-24.md).

- **R1–R6 stand as approved on 2026-09-24.** Revision 3 changes how R1, R2 and R5 are carried
  out. It does not reopen them.
- **Sources.** Two reviews are taken in, each after the checks recorded in §4:
  - the [external presentation review](presentation-review-and-corrections-2026-09-24.md)
    (F01–F11, U01–U06), taken in by revision 2;
  - the [external design review of revision 2](presentation-design-review-v2-2026-09-24.md)
    (D01–D10), taken in by this revision.

  Earlier revisions are at `955510b:` (revision 1) and `7d9959b:` (revision 2), both at
  `docs/track-b/presentation-and-tracking-plan-2026-09-24.md`.
- **Scope:**
  - programme stage 3, presentation around v2 (work items 4.3R, 4.3C and 4.10R);
  - the matching presentation of CP-20 (v3);
  - MLflow as the visible tool for tracking and comparing versions;
  - the design that later generations, the final model and the live model will extend.
- **Approval fixes the design only.** Every commit, push, upload or redeploy needs its own
  explicit instruction (§13).

---

## 0. Summary

**Design direction: a product-led research case study with precise analytical components.**
The page answers five questions, in this order:

| # | Question | Section |
|---|---|---|
| 1 | What did you build? | Product opening, with a real and labelled v1 preview |
| 2 | How did it evolve? | Lineage: adopted generations on the main line, experiments as branches |
| 3 | What improved, and was the comparison fair? | Overview comparison |
| 4 | How did you get there, and why should I trust it? | Chapters, newest first: v3, v2 (with the road to it), v1 (with its archived report) |
| 5 | How does it work, and how can I check it? | System view, reproduction, contribution, attribution |

Later generations, the final model and the live model will be added at the top.

**MLflow.** A new public experiment, `delu-generations`, is added.

- **Each evaluated policy appears exactly once,** as a nested run under the checkpoint that
  produced it. Metric names carry their units, and each run holds full metric histories.
- **One committed export is the only payload.** It is reviewed locally, uploaded only after the
  Owner authorizes it, and then checked run by run against the public server.
- **The repository stays the single source of truth.** The page is built from committed evidence
  only. MLflow mirrors that evidence, and a check proves the two agree.

**What revision 3 changes (design review):**

- **§7 becomes a design specification (D01, D03, D06–D09):**
  - page composition;
  - visual tokens, with contrast checked;
  - components and their states;
  - chart and table grammar;
  - the chapter as a decision story;
  - navigation, accessibility and demo states.
- **The opening (D02)** shows a real v1 preview with one primary action, and keeps the released
  product visibly separate from the latest research.
- **The lineage (D04)** has a main line of adopted generations and real branches. Planned work
  carries no score.
- **Each chapter (D05)** shows one or two primary outcomes, one main chart and its critical
  caveat. Diagnostics move into named disclosures.
- **The demo's loading, failure and retry states** are required in every case (D09).
- **D1 becomes a finished visual specimen (D10):** desktop and mobile, real content, reader tasks
  and screenshots. The Owner approves it before the template is rolled out.
- **Contract fixes:**
  - separate markup for evidence values in HTML and in SVG;
  - an explicit policy for structural numerals;
  - authority per action.

**Revision 2's changes stand:**

- publication happens in a fixed order;
- chart C2 keeps its units separate;
- v1 keeps its exact label;
- the release gates;
- the evidence and claim layer;
- the exact 23-run MLflow manifest.

| Phase | Where it runs | Deliverable | Indicative effort (agent) |
|---|---|---|---|
| 0 | Local, plus the Owner's devices | Demo diagnosis record (F01) | 1–2 h, plus the Owner's test |
| A | Local | CP-20 content and claim map; publication pass over the CP-15/16 draft | ~0.5 day |
| B | Local | Evidence and claim layer, README ownership, tests | 0.5–1 day |
| C | Local only | MLflow spec, read-only probe, local rehearsal, committed export, publisher and verifier | 1–1.5 days |
| D1 | Local only | Visual specimen: desktop and mobile, real content, token sheet, screenshots, reader tasks | 1–1.5 days |
| D2 | Local only | The full page and every surface, in the approved design | 1.5–2 days |
| E | Local | Independent claim and render check, CI-equivalent run, review packet | ~0.5 day, plus the Owner's review |
| F | Public; each step authorized | MLflow upload, index, verification, final build, push, Space redeploy, post-deploy check | ~0.5 day, plus the Owner's actions |

The total is about 6–8 agent days. This is indicative only: it will be re-estimated after Phase
0, the capability probe and D1.

---

## 1. Corrections to earlier revisions

| # | Revision | What it said | What is correct | Source |
|---|---|---|---|---|
| E1 | 1 | The HG−H0 forest plot (C2) had "one row per fold" beside the aggregate row. | The equal-fold rows are differences in normalized scores. The per-fold rows are paired mean daily loss differences in EUR/MWh. They cannot share an axis. | F06 |
| E2 | 1 | Phase C backfilled the public experiment before the Owner's review. | The public upload comes after the review packet and needs explicit Owner authorization. | F10 |
| E3 | 1 | "`check_links` passes" was listed as an invariant. | It always exits 0 (`check_links.py:107`), so it is not yet a gate. | F05 |
| E4 | 1 | README research lines 18–54 would be "regenerated from the same data layer". | No generator owns the research section (`cp3_readme.py:29–30`, `172–182`). | F04 |
| E5 | 1 | v1 carried the badge "Confirmatory". | v1's label is "confirmatory-style, not power-qualified". | F11 |
| E6 | 1 | DagsHub had refused registry tags. | `tags_refused` and `failures` are both empty in `reports/cp3/mlflow_registration.json`. | Registration record |
| E7 | 1 | The backfill would create "about 20 runs". | Exactly 23 runs (§10.3). | F09 |
| E8 | 1 | Only the client version was named (3.16.0). | The DagsHub server reports 3.5.1. The probe tests this client–server pair. | F09 |
| E9 | 1 | "Phase C runs after the Owner restarts the apps." | Phase C is local. Only Phase F's public upload needs the token. | F10 |
| E10 | 2 | §7.7 made the demo's loading and failure states conditional on Phase 0 reproducing the failure, while the Phase 0 row said they go ahead regardless. | They are required in every case (§7.11). | D09 |
| E11 | 2 | §9.3 wrapped every research figure in a `<data>` element, including inside SVG charts. | `<data>` is an HTML element and is not valid inside SVG. SVG elements carry `data-claim` and `data-record` attributes, and axis ticks come from typed scales (§9.3). | Design review §10 |
| E12 | 2 | §9.5 used the absence of bare numerals as the proof of provenance. | Provenance is proved by re-deriving records and binding claims. Structural numerals follow a declared policy. The bare-numeral check is only a backstop (§9.3, §9.5). | Design review §10 |
| E13 | 2 | §7.2 kept every diagnostic dimension visible and required three numbers in every chapter header. | One main chart and one or two primary outcomes stay visible. Diagnostics move into named disclosures (§7.6). | D05 |
| E14 | 2 | §7.1's lineage strip put CP-10 and CP-15 on one line with the generations. | A main line of adopted generations, with real branches (§7.7). | D04 |
| E15 | 2 | §7.1 put "How to read this page" and the system view before the chapters. | Definitions appear where they are used. The system view follows the chapters, with a short anchor near the opening (§7.2). | D03 |
| E16 | 2 | §7.5 kept "the current light, report-like look". | A defined visual system (§7.3, §7.4). | D01 |
| E17 | 2 | §13 cited the 2026-09-24 delegations in a way that could read as precedent. | Each commit, push, upload or redeploy needs its own explicit instruction. No delegation carries over (§13). | Design review §10 |

---

## 2. Goals and non-goals

**Goals:**

- A single scrolling page that is still readable when there are seven generations.
- A product-led design:
  - it shows the real product first;
  - it makes the measured result easy to understand;
  - then it lets the reader follow the decisions and inspect their evidence.
- A full, honest comparison of v1, v2 and v3, available now.
- Every number traceable to a committed file, a row and a claim ID.
- MLflow visibly used for tracking, lineage and comparison.
- A new reader can find all of the following without opening the technical appendix:
  - the product, and which version the demo runs;
  - the main observed improvement;
  - one feature change and one rejected idea;
  - the uncertainty that remains;
  - the route to the evidence.

  Design targets: orientation in about 30 seconds, and the full route in a few minutes. Actual
  times are recorded (§11.4), not claimed in advance.
- Every public route we advertise (the demo, MLflow views) works at the time it is advertised.
- No regression of any public-surface invariant (§6).

**Non-goals now:**

- No new model runs, extensions, fresh-data test (4.7T) or live operation.
- No metric for v2 or a later generation that uses data after 2026-04-07.
- No product, promotion, significance or economic claim.
- No Model Registry entry for HG, because HG is not frozen.
- No research budget spent. The presentation reads saved outputs only; the exhausted CP-20
  analysis and reference passes stay untouched.
- No change to `pyproject.toml` or `uv.lock`. Extra tools live in separate environments under
  `.local/tools/`.
- No theme switching, animated counters, scroll effects, framework or component-library
  migration (§7.13).

---

## 3. Decisions

**Taken by the Owner on 2026-09-24:**

1. **One scrolling page,** even with many generations. Chapters run newest to oldest, so
   scrolling down goes back in time.
2. **v2 and v3 are shown publicly now.** Each extension later becomes a chapter, and the live
   model goes at the top at the end.
3. **MLflow becomes the visible tool for comparing versions.** v2 and v3 are backfilled, and
   future work is tracked in it.

**Approved on 2026-09-24, with how revision 3 carries each one out:**

| ID | Approved recommendation | How revision 3 carries it out |
|---|---|---|
| R1 | Move v1's one-shot holdout out of the page header and into the v1 chapter. Do not delete it. | The badge text is exactly "confirmatory-style, not power-qualified" (F11). v1's full original report becomes an archive disclosure with a route back to the overview (§8.5). |
| R2 | Agents build the page and charts from data, and the Owner reviews visually before any push. | D1 is a finished visual specimen, desktop and mobile, that the Owner approves before the template is rolled out (D10). The tokens in §7.3 are a starting point; the Owner's visual judgment decides. |
| R3 | Version numbers go only to adopted models. | Naming rule (§16, decision 2): `vN · <adopted change>`; a number only on adoption; rejected experiments keep descriptive branch names; no number is reserved in advance; "Final candidate" and "Live" are statuses of a version, not names. |
| R4 | The repository is the source of truth, and the page never reads MLflow. | The page reads committed files only, including the committed MLflow index. |
| R5 | Track locally, and publish to DagsHub after landing. | Publishing is an explicit Phase F action. It needs its own instruction after the Owner reviews the committed export (§13). |
| R6 | The Model Registry holds only runnable, frozen policies. | Unchanged. |

---

## 4. How the reviews' findings are handled

### 4.1 Presentation review (F01–F11, U01–U06), taken in by revision 2

The checks were made on 2026-09-24:

- the code and data findings, by reading the cited lines and files;
- F02, measured in Claude's built-in browser at 390 × 844;
- F01, retried the same day;
- the MLflow server version, read from `/version`.

| ID | Finding | Our check | Decision | Where |
|---|---|---|---|---|
| F01 | The Hugging Face demo failed to start in the reviewer's browser. | Not reproduced. In Claude's built-in Chromium browser, the direct app computed a forecast after about 40 s, and the Hugging Face page showed it after about 70 s, with no error. The cold start shows only a bare spinner. | Accepted, adapted: Phase 0 diagnosis; a startup gate; demo states in every case | §7.11, §11, §12 |
| F02 | The page overflows horizontally on phones. | Reproduced: at 390 px, `scrollWidth` is 1,750. Both `.surfaces-table` tables sit outside `.scroll`. | Accepted | §7.10, §11.3 |
| F03 | Status text that is now stale remains beyond the top card. | Confirmed, with more instances: `delu-m4`, "the planned v2" and `#development-update`. | Accepted | §8.7 |
| F04 | No generator owns the README research section. | Confirmed | Accepted | §9.4 |
| F05 | The link checker always exits 0. | Confirmed (`check_links.py:107`); its explanation text is also stale. | Accepted | §11 |
| F06 | Chart C2 mixes normalized and EUR/MWh units. | Confirmed | Accepted; revision 1 was wrong | §8.3 |
| F07 | The comparison with v1 needs an explanation. | Confirmed (the table below) | Accepted | §8.2 |
| F08 | The contract between claims and data is undefined. | Confirmed gap in the plan | Accepted, kept proportionate | §9 |
| F09 | The MLflow contract is incomplete. | Confirmed gap in the plan; server 3.5.1 | Accepted | §10 |
| F10 | The public MLflow upload came before the Owner's review. | Confirmed | Accepted; revision 1 was wrong | §12, §13 |
| F11 | A plain "Confirmatory" badge strengthens v1's claim; 4.7T and the live panel are unresolved. | Confirmed | Accepted; future design decisions | §7.8, §15 |
| U01–U06 | Reader experience | Consistent with the Owner's goals | Accepted. The design review refines U01–U03 (D02–D04). | §7, §8 |

**Numbers behind F07.** All three figures cover the same 448 development days.

| Figure | Where it is from | What it measures | Reference forecast |
|---|---|---|---|
| "28.58% worse" | v1's own report (DM test, `dm_development.json`) | v1's daily mean absolute error relative to the naive forecast, pooled over all days. The mean daily loss difference is 9.278 EUR/MWh. | The raw similar-day naive, MAE 32.452 EUR/MWh |
| S_MAE 1.0518 | CP-20 scoreboard | v1's MAE divided by the naive's MAE in each fold, then averaged over the five folds | The naive's emitted median after the common residual layer, MAE 32.810 EUR/MWh |
| 41.743 EUR/MWh | Both records | v1's own pooled MAE | — |

### 4.2 Design review (D01–D10), taken in by this revision

The checks were made on 2026-09-24:

- **The review covers exactly revision 2.** The plan hash it cites (`d9d30a9b…`) matches
  revision 2 as committed in `7d9959b`.
- **The inconsistency between revision 2's §7.7 and its Phase 0 row** (D09) is real.
- **`<data>` is invalid inside SVG,** so the review's §10 point about markup is correct. Rows
  DR-10a to DR-10c below are that section's three clarifications.
- **The proposed colours were checked for contrast** (the results are in §7.3):
  - all text, link and generation colours pass 4.5:1;
  - the proposed border is decorative only;
  - the three generation colours have almost the same luminance.

| ID | Finding | Decision | Where |
|---|---|---|---|
| D01 | Replace "the current light, report-like look" with a defined visual system. | Accepted. The tokens are a starting point for D1, and the Owner decides there. | §7.3, §7.4 |
| D02 | A real v1 product preview and one primary action. The released product and the latest research are visibly separate. | Accepted. The preview is v1's saved historical replay, rendered as a static chart and labelled as a replay. | §7.2, §8.1 |
| D03 | A shorter prelude, no duplicated headline comparisons, one question per section. | Accepted. "How to read this page" dissolves into definitions placed where they are used. The system view follows the chapters. | §7.2 |
| D04 | A main line of adopted generations, rejected experiments as branches, planned work without scores. | Accepted | §7.7, §8.6 |
| D05 | Primary and secondary charts; one or two outcomes instead of three numbers. | Accepted | §7.6, §8.3 |
| D06 | Chart semantics: labels, units, direction of improvement, zero and reference lines, scales, intervals, mobile variants. | Accepted | §7.5, §8.2 |
| D07 | Generation identity, evidence class and adoption status are kept separate; type and contrast are accessible. | Accepted. The generation colours share almost the same luminance, so labels and marker shapes carry the meaning. | §7.3, §7.8, §7.12 |
| D08 | One navigation hierarchy, responsive composition, disclosure behaviour, and a route back from the v1 archive. | Accepted. Links into closed disclosures, and optional tracking of the current section, use a few lines of inline script. The zero-fetch rule allows this. | §7.10 |
| D09 | The demo's loading, failure and recovery states are mandatory. | Accepted; revision 2 was inconsistent here. | §7.11 |
| D10 | D1 is a finished desktop and mobile specimen, with reader tasks and screenshots. | Accepted | §11.4, §12 |
| DR-10a | Separate markup contracts for HTML and SVG. | Accepted; revision 2 was wrong. | §9.3 |
| DR-10b | A policy for structural numerals; a bare-numeral check does not prove provenance. | Accepted | §9.3, §9.5 |
| DR-10c | Design approval is not permission to commit or publish, and no delegation carries over. | Accepted | §13 |

**Where revision 3 goes beyond, or narrows, the review:**

- **Scope of the palette.** The review's palette is adopted as the D1 starting point, not as a
  final decision.
- **Colour.** Colour is never the only cue, because the generation colours cannot be told apart
  by lightness alone.
- **MLflow charts.** MLflow's own charts join fold steps with lines. The page never does, and
  each metric's description states that the step is the fold index.
- **v1's archived report** may adopt the new styles, but only deliberately: with scoped CSS, and
  reviewed in D1. Its text and behaviour stay protected by the tests.
- **The contribution statement.** The review asks for it to be required. The plan recommends
  that too. The Owner made it required and supplied the wording (§8.9; §16, decision 7).

---

## 5. Starting point

**The site:**

- `docs/index.html` is 1,014,592 bytes, byte-identical to the deployed page.
- `scripts/build_pages.py` generates it from `reports/cp2/*.csv` and seven PNG figures embedded
  as `data:` URIs. It is v1's report (sections 1–12), with an interactive SVG fan chart.
- Above that report sits a hand-written card, "Development update · 2026-09-16". It is out of
  date, and its numbers are typed directly into the generator.
- The title, meta description and opening paragraph frame the whole page around v1's holdout.
- There is one light report style, but no defined visual system: no type scale, colour roles or
  component states.
- On phones the page overflows horizontally (F02).

**The other surfaces:**

- `README.md` is only partly generated (F04).
- The static Space card `space-wasm/README.md`, the Space card `space/README.md` and
  `reports/cp3/mlflow_registration.json` render from `src/delu_forecast/claims.py` (104 claims)
  through `src/delu_forecast/surfaces.py`.
- The `delu-m4` promise appears on every surface, including the deployed Space.

**The guards:**

- Tests 17 and 19–24.
- `make verify`, which binds the v1 claim set.
- `scripts/check_links.py`, which records link results but never fails (F05).

**MLflow on DagsHub (server 3.5.1; our client is 3.16.0):**

- **One experiment, `delu-cp2`,** with 55 runs. That count includes reproductions that repeat the
  same run names.
- **The canonical v1 run** is `83e475627b6646c885c70f9010c8cf2e`, the registry's source run.
- **One registered model,** `delu-day-ahead-champion`, version 1, alias `champion`, with its
  version tags applied.
- **Nothing from CP-10 onward has been logged.**

**The demo.** It loaded in our check and failed in the reviewer's. This is unresolved (F01, §4.1).

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

**Consistency across checkpoints.**

- The references have identical pooled MAE and WIS in CP-15, CP-16 and CP-20, to 12 significant
  digits.
- CP-20's H0 is CP-16's V2-H. CP-20's Integration review found them bitwise identical.

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
from the standing decisions and from the two reviews.

1. **Zero runtime network calls.** Only plain `<a>` navigation and `data:` URIs: no CDN, fonts or
   analytics (`test_19`). New charts are inline SVG. Inline script is allowed.
2. **One claim source for v1.** `claims.py` feeds every surface.
   - `make verify` passes.
   - Rebuild `app/public/claims.json` (`make wasm-payload`) whenever claims change.
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
8. **Attribution and licensing appear on every surface,** including the GFS line.
9. **The v2 wording rules stand.**
   - W1–W21 apply (§8.8).
   - The upper end of the H−P MAE interval is printed in full as **+0.000003857628092332211**,
     never rounded and never hidden in a tooltip.
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
    aggregation, comparator and evidence class. One axis carries one unit.
16. **No placeholder ships.** The final build fails if a marker for an unpublished link remains.
17. **Research numbers come only from the evidence layer** (§9.3).
18. **A generator owns the README research section,** between explicit markers.
19. **Reader routes are advertised only after they pass their check.**
20. **Nothing becomes public before the Owner reviews** the local page and the export packet.
    Every public action needs its own instruction (§13).
21. **Presentation work spends no research budget.**
22. **No meaning depends on colour or hover alone.** Direct labels, marker shapes or line styles,
    and visible values, carry it.
23. **Charts have mobile variants rather than shrunk desktop versions.** Rendered chart text is at
    least 12 px at a width of 390 px.
24. **v1's archived report keeps its text and behaviour.** Its styling changes only deliberately:
    scoped CSS, reviewed in D1.
25. **The demo's loading, failure and retry states exist in every case,** whatever Phase 0 finds.
    No fake progress is shown.
26. **Planned work is never scored,** never given a version number and never shown as an
    available feature.

---

## 7. Design specification

### 7.1 Direction

The page is **a product-led research case study with precise analytical components.** Three
principles follow:

- **Success is visible without decoding checkpoint codes.** Plain names come first. Codes such as
  `HG`, `H0` and `S_MAE` appear only as secondary metadata.
- **Seriousness is shown without making the first screen an audit log.** Review mechanics sit one
  level deeper.
- **Visual variety follows meaning.** The page alternates:
  - a compact overview;
  - a spacious analytical figure;
  - brief narrative;
  - optional detail.

  Uniform cards everywhere would flatten the difference between a key finding, an
  implementation note and an artifact link.

**Inspiration:**

- Tremor's KPI cards and chart compositions, and shadcn's consistent cards, controls and tables,
  for the analytical components;
- Dub's product-led opening.

These sites are inspiration only; they are not reproduced. Everything is built with the existing
static renderer (`build_pages.py`): HTML, CSS custom properties and inline SVG. No framework,
component library or runtime dependency is added.

### 7.2 Page composition

Each section answers one question.

| Section | Question | Content |
|---|---|---|
| Header | Where am I? | Project name; main navigation: **Results · Journey · Evidence** |
| Product opening | What did you build? | Plain-language problem and purpose; the status pair (§8.1); one primary action and two quieter routes; a real, labelled v1 preview; a short "How it works" anchor |
| The progression | How did it evolve? | The lineage (§7.7); planned work in a separate, unscored block |
| What improved | What improved, and was it fair? | The overview comparison (§8.2), with a short fairness explanation; a table alternative; definitions in context |
| How it improved, newest first | How did you get there, and why trust it? | Chapters: v3; v2 with the road to it; v1 with its archived report |
| How the system works | How does it work? | The system view (§7.9) |
| Reproduce | Can I check it? | A command that rebuilds the page from saved evidence, with its runtime measured; links to full experiment reproduction |
| Contribution | Who did what? | The Owner's statement (§8.9) |
| Attribution | What are the terms? | Licensing and attribution (CC BY 4.0 and GFS); links |

**Order and placement:**

- **This is an information order,** not a demand to fit everything above the fold.
- **On phones,** the product preview follows the title and actions directly, never below a
  methodology section.
- **Metric definitions sit where they are used,** in small disclosures. There is no preliminary
  lesson.

### 7.3 Visual tokens

These are the starting specification for D1. D1 may refine them as a coherent set, and the Owner
approves the result. Contrast was computed on 2026-09-24 against white and against the canvas.

| Role | Token | Contrast (white / canvas) | Rule |
|---|---|---|---|
| Canvas | `#FAFAFA` | — | The page background. Narrative text sits directly on it. |
| Surface | `#FFFFFF` | — | Analytical panels only |
| Border | `#E4E4E7` | 1.27 / 1.22 | Decorative only. Any border that conveys state needs at least 3:1. |
| Text | `#18181B` | 17.72 / 16.97 | — |
| Secondary text | `#52525B` | 7.73 / 7.41 | Caveats use readable text, never faint microcopy |
| Link and focus accent | `#1D4ED8` | 6.70 / 6.42 | Underlined links and a 2 px focus outline; independent of generation colours |
| Primary action | Dark fill `#18181B`, white text | 17.72 | One per view; at least 44 px tall |
| v1 | Slate `#475569` | 7.58 / 7.26 | Identity, not status |
| v2 | Violet `#6D28D9` | 7.10 / 6.81 | Identity, not status |
| v3 | Teal `#0F766E` | 5.47 / 5.24 | Identity, not status |
| References | Neutral grey, labelled | — | Visually secondary, but fully readable |

**Generation colours.** Their luminance contrast with each other is only 1.07–1.38. They
therefore always come with direct version labels and distinct marker shapes or line styles.
Colour never means "passed".

**Typography:**

- **Font stack:** a system stack (`system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`), with
  no remote fonts.
- **Body text:** about 16 px on a 26 px line height, with prose 60–68 characters wide.
- **Numbers and code:** tabular numerals for data (`font-variant-numeric: tabular-nums`), and
  monospace for IDs and commands.
- **Heading scale:**
  - the opening: 48–56 px on desktop, 32–36 px on phones;
  - chapter headings: 28–32 px and 24–28 px.

  The headline must not push the product preview out of view.
- **Data text:**
  - headline values: 28–32 px;
  - labels: about 14 px;
  - tables: 13–14 px;
  - chart text: never below 12 px as rendered.

**Spacing, layout and containers:**

- **Spacing scale:** 4, 8, 12, 16, 24, 32, 48, 64 and 96 px. Large steps separate chapters; small
  steps group a claim with its caveat and source.
- **Width:** content up to about 1,200 px, with prose narrower. A desktop rail of about 140–160 px
  appears only when there is enough width for it.
- **Containers:**
  - about 10–12 px radius and a 1 px border;
  - a restrained shadow only where it helps, such as around the product preview;
  - no nested bordered cards around every paragraph.

**Implementation:**

- The tokens are CSS custom properties defined in the generator.
- v1's archived report gets its own scoped stylesheet, so global styles cannot change it by
  accident (invariant 24).

### 7.4 Components and states

D1 shows every component below, with at least six representative states between them.

| Component | Variants and states | Rule |
|---|---|---|
| Primary action | Default, hover, visible focus, pressed | One per view |
| Quiet link | Default, hover, visible focus, external-link marker | Underlined |
| Status pair | Released product · latest research | Text and badge; no success colour |
| Evidence badge | Short ("Development · post-selection"); long ("Confirmatory-style, not power-qualified", which wraps) | Placed next to the result it qualifies (§7.8) |
| Adoption label | Adopted · Not adopted · Planned, not evaluated | Text, separate from the badge; no green check mark |
| Analytical panel | With an interval; with a reference line; table alternative closed or open | §7.5 |
| Evidence row | Link available; link unavailable (in local prototypes only, for unpublished destinations) | §7.9 |
| Disclosure (`<details>`) | Closed, open, opened by an anchor link | §7.10 |
| Lineage node | Main line (adopted); branch (not adopted); planned (no score) | §7.7 |
| Data table | Standard; a long exact value that wraps (the H−P endpoint) | Numbers aligned; units in headers |
| Demo launcher (Space) | Ready, loading, failure, retry | §7.11 |

### 7.5 Chart and table grammar

**Every primary figure is an analytical panel,** with these parts in this order:

1. A title that states a plain-language question or finding.
2. A subtitle giving the metric, comparator, population and evidence class.
3. A legend next to the plot, or direct labels, with explicit units.
4. The chart itself, with its zero or reference line.
5. One finding and one qualification, followed by the evidence row (§7.9).

**Rules:**

- **Controls** appear only when they change a real view: no decorative tabs and no date pickers
  for a fixed evaluation window.
- **Nothing depends on hover.** No essential value, caveat or source is available only on hover.
- **Direction and reference.** Every chart states which direction is better. The reference line
  is labelled as a reference, not as a target.
- **Scales.** Directly comparable panels share the same scale. If v1's crisis errors would hide
  the differences between v2 and v3, a separate, labelled paired-difference view is added,
  rather than giving each model its own scale without saying so.
- **Folds and generations are discrete comparisons.** They are never drawn as a smooth time
  series or as a decorative "improvement" sparkline.
- **Coverage and interval width are shown together.** Higher coverage is not better on its own if
  the intervals widen.
- **Two kinds of interval.** A confidence interval of an estimated difference is not a forecast
  interval. Legends and text say which one is shown.
- **Units.** One unit per axis, enforced by typed series (invariant 15).
- **On phones,** paired panels stack. Labels are shortened responsibly, or legends move below the
  plot. A dedicated mobile variant is rendered, instead of scaling down the desktop SVG
  (invariant 23).
- **Table alternatives** carry the same values, definitions and precision as their chart.
- **Plain names come first,** for example "v3 · weather features", with `HG` as secondary
  metadata. Seven rows never get seven unrelated colours.

### 7.6 Chapter template: a decision story

**The sequence:** problem → hypothesis → change → measured result → limitation → decision →
evidence.

**Visible by default:**

- **A header:** version, date, adoption label, and the evidence badge next to the result.
- **One or two primary outcomes,** with context where needed. Counts of hours, runs or files are
  context, not success figures.
- **A small diagram of the change** in features or policy.
- **The main chart,** only one.
- **At least one compact finding** on where the change helps and where it hurts.
- **The critical caveats,** which are never hidden.
- **The reasoning behind the decision,** and the evidence row.

**Inside named disclosures,** for example "Consistency across folds", "Crisis window", "Hours of
the day", "Coverage and interval width" and "Protocol and review details":

- the full diagnostics, charts and tables;
- the review mechanics, including failed attempts and repair identifiers.

Opening a disclosure shows a properly sized chart, not a miniature.

**Rejected paths are made concrete:** what was tried, which result was not enough, and which
later decision it informed.

**Review wording:** "an independent Integration review within this project's process". Never
"peer review" or "external validation".

### 7.7 Lineage and planned work

```text
v1 ─────────────────── v2 ─────────────────── v3
 └─ calibration experiment (CP-10)            weather-feature bundle
    not adopted
         model-comparison study (CP-15) → informed v2
Planned, not evaluated (separate block, no scores)
```

- **The main line holds adopted generations only.**
- **Studies and experiments are branches,** marked with what they informed.
- **The planned block** lists each item with:
  - the question it will test;
  - the evidence that would decide it;
  - the note "subject to the active plan".

  It carries no score, no version number and no disabled button.
- **Future experiments that are evaluated and rejected** become branches, with their results.
- **Naming (§16, decision 2).**
  - Adopted generations are named `vN · <adopted change>`, for example `v3 · weather features`.
  - A number is assigned only on adoption. A rejected experiment keeps a descriptive branch name,
    and no number is reserved in advance.
  - "Final candidate" and "Live" are statuses shown on a version, never names that replace it.

### 7.8 Evidence badges and adoption status

**Three separate signals:**

- **Generation identity,** by colour and label.
- **Evidence class,** by badge.
- **Adoption,** by text.

**Badges:**

| Badge | Used for |
|---|---|
| **Confirmatory-style, not power-qualified** | v1's one-shot holdout, verbatim; allowed to wrap |
| **Development · post-selection** | CP-10, CP-15, CP-16, CP-20 and the extensions; placed next to each research result |
| **Prospective** | Reserved for the live model; its design is deferred (§15) |

No badge is promised yet for 4.7T (§15).

Numbers with different badges are never placed side by side as if they were comparable. "Adopted"
means adopted within this research programme. It never implies deployment or outside validation.

### 7.9 Evidence row, fairness note and system view

**The evidence row** sits beside each result: **Compare these runs in MLflow · Reviewed result ·
Source data**.

- Full hashes, internal claim IDs and repair identifiers stay in deeper metadata.
- In local prototypes, an unpublished destination is shown as "unavailable", never as a dead
  link that looks complete.

**The fairness note** sits next to the overview comparison.

- **Visible part:** the shared population of 10,747 hours over 448 days; equal-fold scoring; the
  development status.
- **One level deeper:** the paired bootstrap settings (seed 15042, 2,000 replicates, 7-day blocks)
  and the fold table.

**The system view** shows the real data flow: source data and vintages → availability checks →
features → model and interval policy → evaluation and artifacts → report, demo and tracking.

- It marks the information cutoff and where the leakage controls act.
- Implemented and planned components are distinguished by text and line style.
- It uses no logos.

**Current-looking figures.** Test totals, run counts and verification dates are never presented
as current unless a release record supports them.

### 7.10 Navigation and responsive behaviour

**Navigation:**

- **One compact main navigation** (Results · Journey · Evidence).
- **The generation rail** is secondary to it. On phones it becomes a compact jump control or a
  row of anchors.
- **No stacked sticky bars.**
- **The sticky header** never covers anchored headings or the keyboard focus
  (`scroll-margin-top`).
- **Links into closed disclosures:** a few lines of inline script open the target `<details>`,
  because Safari does not expand it automatically. The destination is labelled clearly.
- **The rail** is a stable jump list. Highlighting the current section is optional, and it is
  promised only if implemented (a small inline `IntersectionObserver`), since `:target` alone
  does not track scrolling.
- **v1's archive** has a clear route back to the overview.
- **Scale test.** A local stress case with seven generations checks the rail and the chapter
  summaries, using placeholders only. It is never published.

**Responsive fixes (F02):**

- Put every data table inside a labelled `.scroll` wrapper, including both `.surfaces-table`
  tables (`build_pages.py:584` and `:615`).
- Let prose, URLs and hashes wrap (`overflow-wrap: anywhere` on code and hash cells). Keep
  `nowrap` (`:146`) on numeric columns only.
- Stack the `.kv` grid (`:165`) below about 620 px.
- Keep primary summaries readable without scrolling sideways. Exceptionally long exact values
  wrap.

### 7.11 Demo presentation and states

**The demo action.**

- The primary action reads **Try the v1 demo**.
- Beside it, not inside its label, sits the startup information: the first visit downloads about
  57 MB; the measured start time, with its device, browser and date; and the date it was last
  verified.

**Replay versus live inference.**

- The page's own chart is v1's **historical replay**: precomputed, instant and offline.
- The Space runs **real inference in the browser.** Labels always make the difference clear.

**The Space's states are required in every case** (D09, invariant 25):

- **Ready, loading, failure and retry,** each with an obvious route back to the instant report.
- **The first loading or fallback message is in the static HTML.** It is visible before the
  runtime starts, and it stays visible if initialization fails.
- **Stages are shown only where the runtime reports them.** No invented percentage, and no timer
  shown as progress.
- **Where it is built:** `build_wasm_space.py`, whatever Phase 0 finds. The model and its
  bitwise-equivalence gate do not change.

**What stays out.**

- The static report does not auto-launch or embed the heavy runtime.
- It needs no loading skeletons.
- External demo and tracking links are identified as external.

### 7.12 Accessibility acceptance

**Contrast:**

- Normal text needs at least 4.5:1, and large text at least 3:1.
- Chart marks, controls, state-carrying borders and focus indicators are checked separately, at
  3:1 or more. A passing text palette does not settle them.

**Layout:**

- **Screenshots** at 1,440, 768, 390 and 360 px.
- **Zoom** at 200%.
- **Reflow** at 320 CSS px. Local scrolling is allowed only for genuinely two-dimensional tables.

**Interaction:**

- a logical keyboard order;
- disclosures that are announced;
- descriptive link text;
- a text or table route through every main figure;
- touch targets of about 44 px;
- removing colour removes no meaning.

The acceptance criteria follow the WCAG 2.2 contrast and reflow guidance. No WCAG conformance is
claimed from screenshots alone.

### 7.13 Out of scope for the design

- theme switching and dark mode;
- animated counters and scroll effects;
- framework or component-library migration;
- remote fonts;
- decorative tabs or date pickers;
- logo walls;
- disabled buttons for features that do not exist.

---

## 8. Content now

### 8.1 Opening and product preview

**Copy direction** (it still goes through claim review):

- the title, **"Forecasting tomorrow's electricity prices."**;
- a supporting sentence, **"Explore the released demo and follow how successive research models
  were compared and improved."**

**The status pair:**

- **Released demo:** v1.
- **Latest research:** v3, marked **Development · post-selection**.

Planned work belongs below the lineage, not in a third status card.

**Actions:**

- **One primary action:** **Try the v1 demo**.
- **Two quieter routes:** **Compare research results** and **View code and evidence**.
- The startup information sits beside the demo action (§7.11).

**The product preview.** A compact, static rendering of v1's saved historical replay: the fan
chart for the default day at ×1.00 and the 80% level, labelled "historical replay". It links to
the interactive version in v1's chapter, and to the in-browser demo. An optional screenshot of
the Space may be added, labelled "preview". Nothing implies that v3 runs in the demo.

**At most one summary value in the opening.** It must be a saved difference with its comparator
and development label, and it comes from the same evidence record the chapter uses. For example:
v3 against v2, normalized point error −0.078 [−0.101, −0.057]. The full scoreboard never appears
in the opening, and no new promotional percentage is introduced.

### 8.2 Overview comparison: "What improved"

**The layout.** Two aligned horizontal dot plots:

- **Point forecast error (lower is better),** using S_MAE;
- **Interval quality (lower is better),** using S_WIS.

**The subtitle:** "Equal-fold score relative to the similar-day naive · identical 10,747 hours ·
development, post-selection".

**The rows,** in one fixed order across both panels and the table:

| Order | Label (code as secondary metadata) | S_MAE | S_WIS | Weight |
|---|---|---|---|---|
| 1 | v3 · weather features (HG) | 0.5658 | 0.5322 | Generation |
| 2 | v2 · blended LEAR, hour-aware intervals (V2-H) | 0.6441 | 0.6160 | Generation |
| 3 | Daily LEAR (reference, B2) | 0.6578 | 0.6390 | Reference |
| 4 | Normalized LEAR (study challenger, A1) | 0.6723 | 0.6460 | Study |
| 5 | Daily LightGBM (reference, B3) | 0.7841 | 0.7399 | Reference |
| 6 | v1 · released LightGBM (development replay, B1) | 1.0518 | 0.9856 | Generation |
| 7 | Similar-day naive (normalizer, B0) | 1.0000 | 1.0000 | Reference |

**Reference lines:**

- "naive = 1.00", a reference and not a target;
- "the plan's diagnostic limits (criteria 1–2)", at 0.59203 and 0.57509. They are not presented
  as certification.

**Styling.** Generations are emphasized through labels and weight. References stay fully
readable. There is no pagination, search box, selection checkbox or toolbar.

**The fairness note** is described in §7.9.

**The F07 note,** in a "Definitions" disclosure beside the comparison (draft): "Why v1 scores 1.05
here but '28.58% worse' in its own report. Both numbers describe the same 448 development days.
v1's report compared its daily absolute error with the raw similar-day naive (MAE 32.45 EUR/MWh)
and pooled all days, so the 2022 crisis dominates. This comparison gives each of the five folds
equal weight, and its naive reference is the forecast's emitted median after the common residual
layer (MAE 32.81 EUR/MWh). v1's own error is 41.74 EUR/MWh in both. v1's original nine-quantile
pinball is a different score from the seven-quantile WIS used here."

### 8.3 v3 chapter (CP-20)

**Primary outcomes, against v2:**

| Outcome | Difference | 95% interval |
|---|---|---|
| Normalized point error | −0.0783 | [−0.1006, −0.0570] |
| Normalized interval score | −0.0838 | [−0.1044, −0.0655] |

Both carry the development badge.

**Visible by default:**

- a small diagram of the feature change: three weather features and their missing indicators,
  added to v2;
- **C2a** as the main chart;
- the bundle limitation: the gain belongs to the three features together, and no experiment
  isolates any single one;
- a visible note that in fold 3, the 2022 crisis, the interval of the MAE difference crosses zero;
- one compact finding on where the change helps and where it hurts: in the crisis window, MAE
  goes from 52.51 to 47.52 EUR/MWh and 95% interval hits from 377/408 to 383/408. This is
  descriptive, and shown only with a claim-map entry;
- the reasoning for adopting it, and the evidence row.

**Charts:**

| # | Chart | Unit | Where it sits | Source |
|---|---|---|---|---|
| C2a | Equal-fold HG−H0 for ΔS_MAE and ΔS_WIS. Negative favours v3. Zero and the full interval extent are shown. | Normalized score (ratio to B0) | Visible, main chart | `uncertainty.csv`, `equal_fold` |
| C1 | The GFS box (47–55.25°N, 5.5–15.5°E) and the feature recipe: per-cell wind speed at 10 m and 100 m, then an area average; DSWRF de-averaged; missing indicators | — | Disclosure: "How the weather features are built" | Static |
| C2b | HG−H0 per fold, MAE and WIS in separate panels. Fold 3's MAE is −3.18 [−6.09, +0.037]. Its crossing of zero is never cropped. | EUR/MWh, paired mean daily loss difference | Disclosure: "Consistency across folds" | `uncertainty.csv`, `fold_1`–`fold_5` |
| C3 | MAE and WIS per fold for v1, v2 and v3, on matching scales. A paired-difference view is added if v1 hides the others. | EUR/MWh | The same disclosure | `metrics.csv`, `per_fold` |
| C4 | Crisis window, 2022-08-15 → 08-31 (408 hours, 17 days) | EUR/MWh; hits out of 408 | Disclosure: "Crisis window" | `reports/cp15/peak.csv` for v1 and A1; `criteria.csv` criterion 4 for v2 and v3 |
| C5 | MAE by hour of day, v2 against v3. Descriptive; shown only with a claim-map entry | EUR/MWh | Disclosure: "Hours of the day" | `diagnostics.csv`, `hour` |
| C6 | Coverage and mean interval width at 50%, 80% and 95% for each generation | Fraction; EUR/MWh | Disclosure: "Coverage and interval width" | `metrics.csv` |

Chart C2 does not invent normalized confidence intervals per fold.

**C4 values:**

| Generation | MAE (EUR/MWh) | 95% interval hits |
|---|---|---|
| v1 | 275.26 | 79/408 |
| A1 | 49.88 | 378/408 |
| v2 | 52.51 | 377/408 |
| v3 | 47.52 | 383/408 |

**The decision story:**

- **Problem:** v2 used market data only.
- **Hypothesis:** forecast wind and solar drive both the level and the shape of prices.
- **Change:** three frozen weather features.
- **Result:** the joint improvement rule is met, and all five folds favour v3. As diagnostics, v3
  is the first evaluated policy to meet all six §8 criteria.
- **Limitation:** the bundle limitation above, fold 3, and development status.
- **Decision:** adopted as the current research model.

**Protocol and review details, in a disclosure:**

- Frozen causal controls ran as planned.
- Supplementary controls were added after we found that one frozen check could not fail.
- The first independent review failed on a byte-level reproducibility defect. The defect was
  repaired, and a fresh review passed. The repair identifiers stay inside this disclosure.
- **Cost:** 2,476 GFS runs and 123,800 messages; 136 GiB transferred; 40.1 machine-hours; $0.
- **Dependency:** a daily GFS retrieval. 2019-01-01 is structurally missing.
- The GFS attribution line.

### 8.4 v2 chapter, with the road to it

**The decision story:**

- **Problem:** v1 collapsed in the 2022 crisis. In the peak, its MAE was 275.26 EUR/MWh, and 79 of
  408 hours fell inside its 95% interval.
- **First attempt, a branch that was not adopted (CP-10).** Recalibrating v1 without refitting it
  raised peak coverage from 19.36% to 32.11%. That was not enough: the model itself had to
  adapt.
- **The study that informed v2, a branch (CP-15).**
  - Nine policies were compared.
  - Normalized LEAR (A1) cut peak MAE to 49.88 EUR/MWh, but no policy met the product criteria
    (`NOT_DEMONSTRATED`).
  - Daily LEAR (B2) had the better primary scores.
- **Change:** v2 blends B2 and A1 and adds hour-aware residual intervals (H), with a pooled
  control (P).
- **Result:**
  - H−B2 meets the joint improvement rule, as exploratory evidence.
  - H−P shows no demonstrated joint preference. The upper end of its MAE interval,
    **+0.000003857628092332211**, is visible in full and wraps.
  - H and P miss criteria 1–2.
- **Limitations:**
  - The improvement over B2 is not attributed to hour-aware intervals alone (W4, W5).
  - The split between the blend and the interval layer is not isolated.
- **Decision:** adopted as the research model that v3 builds on.

**Charts.** Chart specifications 1–2 from `cp15-cp16-update.md` (equal-fold, consistent units),
redrawn in the §7.5 grammar. The H−B2 outcome is the primary one.

### 8.5 v1 chapter and archive

**Visible:**

- **What v1 is,** and that the demo runs it.
- **The one-shot holdout,** under its exact badge: MAE 25.9078 against 27.7578; mean pinball
  6.7083 against 13.8789; DM p = 1.98e−18.
- **The two unflattering results.**
- **The lesson from its crisis failure:** the errors were about price level, not shape (bias
  −269.45; level MAE 269.45 against shape MAE 66.88).

**The archive disclosure,** "The original v1 report (published 2026-09-15), preserved":

- it holds the full report, including the interactive fan chart and its behaviour: ×1.02 hides
  the actual-price line and shows the scenario caveat, and choosing 95% shows 0.9398;
- it has scoped styles and a link back to the overview;
- its anchors stay stable (§7.10).

### 8.6 Planned, not evaluated

This block sits below the lineage. Every item is "subject to the active plan", and compared with
v3 on identical rows and information (standing decision).

| Work item | Question it will test | Evidence that would decide it |
|---|---|---|
| 4.6 DDNN / TabPFN | Does a distributional network, or a tabular foundation model, beat v3? | A licence and resource entry, then one predefined comparison |
| 4.4V VRE | Does an in-house wind and solar generation forecast add information beyond direct weather? | A held-forward generation model, then an ablation |
| 4.5 Three-block LightGBM | Does capacity per block help? | A per-block comparison |
| 4.8 Recombination | Does combining adopted models help? | A predefined combination test |
| 4.7T and live | How does the final model perform on data that was never used? | The final fresh-data test, then at least 90 live days |

No item has a score, a version number or a delivery date.

### 8.7 Stale text to reconcile (F03)

| Location | Now | Change |
|---|---|---|
| `build_pages.py:325–348` | The "Development update · 2026-09-16" card | Remove it. Keep `#development-update` as an alias, or repoint the link at `:620`. |
| `claims.py:67–76` (`MLFLOW_NEXT_EXPERIMENT = "delu-m4"` and its note) | "No v2 run exists yet …", on every surface and in the deployed Space | Describe `delu-generations` instead (§16, decision 6). This requires a Space redeploy in Phase F. |
| `claims.py:215` (a limitation) | "the defect the planned v2 targets" | "the defect later generations address (see the v2 and v3 chapters); it is not fixed in the released v1". The 0.194 figure and its mechanism are unchanged. |
| `README.md:18–54` | A hand-written "Current development" section that says CP-16 needs a brief | A block owned by the generator (§9.4) |
| Page title, meta description, opening paragraph | Framed around v1's holdout | The §8.1 opening; v1's holdout moves to its chapter |
| Page §12 tracking note | Written before the current plan | Updated |
| `space-wasm/README.md`, `space/README.md`, `app/public/claims.json` | Carry the claims above | Rebuilt; the Space is redeployed in Phase F if its content changed |

A phrase guard (§9.5) enforces this.

### 8.8 Claims discipline

- **Phase A output.** Phase A produces `cp20-update.md` and `cp20-claims.md`, in the format of
  `cp15-cp16-claims.md`.
- **What the site renders.** Only mapped claims. New display copy, such as the §8.1 title and
  sentence, goes through claim review too.

**New withheld claims:**

| ID | Withheld claim |
|---|---|
| W17 | Attributing the weather gain to any single feature |
| W18 | Calling the Integration review "peer review" or "external validation" |
| W19 | Stating or implying that v3 runs in the demo or live |
| W20 | Comparing v3 with v1 as a headline ratio without the comparison's definition and the development label |
| W21 | Calling v1's holdout "confirmatory" without "-style, not power-qualified" |

### 8.9 Contribution statement

Required (§16, decision 7). The Owner wrote it in Hebrew on 2026-09-24. This is its English
rendering, which the Owner confirms at D1:

> I led this project, from defining the problem and the success criteria to the decisions on the
> research direction and on how the product is presented. The work was carried out with the help
> of AI agents for writing code, analysis and documentation, in a process that included automated
> tests and reviews kept separate from the execution. Responsibility for adoption decisions, for
> approving the deliverables and for publication was mine.

It is displayed as written. It is not a research claim, and only the Owner changes it.

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
- **`claims.py`** keeps v1's bound claims, with only the reconciliation edits from §8.7.
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

### 9.3 Markup contract

| Where it appears | Markup | Validated as |
|---|---|---|
| A research value in HTML text | `<data value="…" data-claim="…" data-record="…">…</data>` | A claim bound to a record |
| A research value in SVG: a `<text>` label or a mark | The same `data-claim` and `data-record` attributes on the SVG element. `<data>` is not valid inside SVG. | A claim bound to a record |
| An axis tick | `data-scale="<scale id>"` | Derived from a typed scale; structural, not a claim |
| A structural numeral: version labels, dates, fold indices, section numbers, control values such as ×1.02 and 95% | Rendered through `structural(kind, value)`, which adds `data-structural="<kind>"` | Declared structural, so it cannot carry a research result |
| The README research block | Rendered from the same claim templates | Generated-block equality (§9.4) |

**Charts** take typed series objects. Each series carries its unit, and the renderer refuses to
put two units on one axis.

### 9.4 README ownership (F04)

- The research section sits between `<!-- research:start -->` and `<!-- research:end -->`.
- A generator owns it. It fails if either marker is missing or duplicated, and it is idempotent.
- The rest of the README is not touched. `cp3_readme.py` keeps its own span.

### 9.5 Tests (offline, run in CI)

| Test | What it checks | Negative controls |
|---|---|---|
| `test_29_research_evidence.py` | Every record re-derives from its source row and revision. References are identical across CP-15, CP-16 and CP-20, and H0 equals V2-H. This is the proof of provenance. | A wrong row, policy, aggregation, unit or revision fails. |
| `test_30_research_claims_rendered.py` | Every `data-claim` exists in the claim layer and the claim map, and every published claim is rendered. Withheld phrases and the stale-status phrases (§8.7) are absent. Date guard on typed fields: a v2+ record must have `window.last` ≤ 2026-04-07, and v1 holdout records carry the exact label. Unit guard. Placeholder guard on the final build. **Backstop:** every numeral in a research section is claim-bound, derived from a scale or declared structural. | A mixed-unit axis raises an error. A post-boundary window fails. A missing claim ID fails. An undeclared numeral fails. |
| `test_31_page_structure.py` | Every table sits inside `.scroll`. Internal anchors resolve. The size budget holds. Mobile SVG variants have text of at least 12 px. Every chart series has a direct label or a distinct marker. Badge texts are exact, and long exact values can wrap. The fan chart's caveat and its 0.9398 are present. | A table outside `.scroll` fails. A series without a label fails. |
| `test_32_readme_ownership.py` | The markers appear exactly once. Running the generator twice gives identical output. A fixture change updates the block. Bytes outside the block are unchanged. | A missing marker fails clearly. |
| `test_33_check_links_gate.py` | A required URL that fails gives a nonzero exit. Local documentation examples are classified as non-destinations. | A mocked 404 fails. |
| `test_34_mlflow_export.py` | The export is deterministic, and the manifest lists exactly 23 runs. Metric names carry units. Comparability IDs are consistent. The outbound scan runs. | A fake credential blocks the export, and its value is never printed. |
| `test_23` (extended) | The built Space's HTML contains the static loading, failure and retry markup, and the link back to the report. | Removing the markup fails. |

Existing tests 17–24 and 28 keep running on every change.

---

## 10. MLflow tracking (F09)

### 10.1 What a reviewer should see

- **Each policy exactly once,** in one experiment, as nested runs under its checkpoint.
- **A leaderboard** that sorts by `s_mae` and `s_wis`.
- **Charts per fold and per day,** inside MLflow itself. MLflow joins fold steps with lines; each
  metric's description states that the step is the fold index.
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
  - The references come from CP-15.
  - v2 is CP-16's V2-H, and CP-20's H0 is the same policy.
  - `test_29` ties CP-20's figures to these runs.
- **Run names:** "CP-20 · HG · v3", "CP-16 · V2-H · v2", "CP-15 · B1 · v1 development replay".

### 10.3 Exact run manifest (23 runs)

| Parent `run_key` | Child `run_key`s | Children |
|---|---|---|
| `cp10` "CP-10 · calibration only (branch)" | `cp10/v1_reference`, `cp10/c1_head_spread`, `cp10/c1_price_volatility` (selected), `cp10/c2_aci_gamma_0.000001`, `cp10/c2_aci_gamma_0.000005`, `cp10/c2_aci_gamma_0.00001`, `cp10/c2_aci_gamma_0.00002` (selected γ) | 7 |
| `cp15` "CP-15 · model-comparison study (informed v2)" | `cp15/B0`, `cp15/B1` (v1 development replay), `cp15/B2`, `cp15/B3`, `cp15/A1`, `cp15/A2`, `cp15/A3`, `cp15/A4`, `cp15/A5` | 9 |
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
  4. **A public upload runs only on an explicit instruction for that action,** recorded in the
     upload log (§13).
- **The index.** After the public upload, `reports/presentation/mlflow_index.json` maps each
  `run_key` to its public run ID, experiment ID and UI routes. It is committed, and the page build
  reads it. This mapping replaces the run IDs of the local rehearsal.

### 10.8 Scanning the outbound payload

The publisher checks every outbound string and every artifact byte against the credential values
from `scripts/secret_guard.py`. This covers parameters, tags, notes and metric keys, and it covers
every path, including partial failures. On a hit it aborts without printing the value. This
extends `redact()` in `tracking.py`, which masks only the DagsHub token, and only in parameter
strings.

### 10.9 Capability probe, with no public writes

1. **Read-only, against the public server:**
   - read `/version` (3.5.1);
   - check which fields `runs/search` on `delu-cp2` returns;
   - check anonymous access to experiment and run routes.
2. **Local rehearsal:** a 3.5.1 server in `.local/tools/mlflow-3.5.1/` (a separate `uv` venv; the
   project's `uv.lock` is not touched), used with the project's 3.16.0 client. It tests:
   - nesting;
   - metric timestamps and history lengths;
   - `log_input` and notes;
   - artifact sizes;
   - search by tag;
   - resuming an interrupted upload.
3. **No write probe on DagsHub** (§16, decision 5). A local success does not prove that DagsHub
   supports a feature. Every capability the page relies on is therefore verified against the
   service after the authorized upload (Phase F3).

Results are recorded in `reports/presentation/mlflow-capabilities.json`, including the fallback
for every unsupported feature. A tag can preserve a digest or a parent ID, but it cannot replace
a missing chart or comparison workflow. When one is missing, the page does not promise that
function.

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
    anonymously.

  A route is advertised only after both checks pass.

### 10.11 Workflow from CP-21 on

1. **During the checkpoint:** the Lead tracks runs in `.local/mlruns/<cp>`, using the same names
   and tags.
2. **In the checkpoint's evidence:** its committed export JSON, which is durable and which the
   Critic reviews.
3. **At landing:** publication follows the same sequence as Phase F, with its own instructions.
4. **In the templates:** adding this step to the landing templates needs a Lockdown suspension
   (§16, decision 4). Until then, each brief carries the step as an explicit section with its
   deliverables and acceptance criteria. After the route has completed and been verified once,
   the step is fixed in the templates: the Owner granted the Lockdown suspension for that
   specific edit on 2026-09-24, and it is applied in a separate task after PRES-1's return. The
   Lead proposes the exact text; it does not edit the templates.
5. **For the final model:** it is registered as a runnable `mlflow.pyfunc` policy
   (`delu-day-ahead-policy`). The `champion` alias moves only under the protocol settled in §15.
6. **For live operation:** live metrics go to `delu-live` only.

---

## 11. Verification gates

### 11.1 Offline, in CI on every push

- Existing tests 17–24 and 28, new tests 29–34, and the extended `test_23` (§9.5).
- `make verify`.
- The zero-fetch scan (`test_19`).

### 11.2 Release checks, which need the network and run outside CI

- **`check_links.py`, repaired (F05):**
  - it exits nonzero when a required public destination fails;
  - it classifies local development URLs and command examples explicitly;
  - it records the observed error and the check date.
- **Semantic MLflow route checks** (§10.10).
- **The mirror verifier.**

### 11.3 Browser and accessibility checklist, run by hand and recorded

The results go to `reports/presentation/release-checks/<date>.json`, with the browser, device,
app revision and outcome. Screenshots stay under `.local/artifacts/presentation/` unless the Owner
wants them committed.

| Surface | Checks | Devices and widths |
|---|---|---|
| Report | **Layout:** screenshots at 1,440, 768, 390 and 360 px; `scrollWidth ≤ clientWidth` on phones; 200% zoom; reflow at 320 CSS px. **Contrast:** text at 4.5:1 and 3:1; non-text elements at 3:1. **Keyboard:** order, visible focus, disclosures that are announced, anchor links into closed disclosures. **Touch:** targets of about 44 px. **Content:** charts readable; the meaning survives without colour; the fan chart keeps its ×1.02 and 95% behaviour. | Desktop Chrome and Safari; iPhone Safari |
| Demo | From a cold start to a visible forecast, timed. A level change and a scenario change work. The loading, failure and retry states work, and so does the route back to the report. | The same |
| MLflow | Every advertised route renders its intended run or comparison anonymously. | Desktop |

HTTP 200 responses, and old equivalence or load records, do not count as a substitute. No WCAG
conformance is claimed.

**Optional automation:** a `scripts/check_reader_paths.py` that runs only when Playwright is
installed in a separate tool environment under `.local/tools/`. It never runs in CI.

### 11.4 Reader tasks (U06, D10)

**The tasks.** Readers are not coached. Each is asked to:

1. find the product;
2. name the released version and the research version;
3. explain the main improvement;
4. find a rejected idea;
5. name a remaining uncertainty;
6. open the evidence supporting one claim.

**The readers:**

- the independent checker, an agent without context, which checks the facts and the routes;
- the Owner;
- ideally, one person who does not know the project.

**What is recorded:** the actual times and the points of confusion, against the targets of
orientation in about 30 seconds and the full route in a few minutes. Human judgment decides
visual quality.

---

## 12. Phases, order and acceptance

| Phase | Tasks | Outputs | Acceptance |
|---|---|---|---|
| **0: Demo diagnosis** | The Owner's device test was completed on 2026-09-24 (§16, decision 8). The executor records it, asking the Owner for the device, browser and outcome if they are not yet recorded. It then reproduces on desktop engines and, if a failure appears, captures the console and network. No code changes before a reproduction. | `release-checks/<date>-demo.json`; a fix plan | Diagnosis recorded. The demo states (§7.11) go ahead in any case. |
| **A: Content** | CP-20 update and claim map. A publication pass over the CP-15/16 draft (G9 resolved by the Owner's decision). The F07 text. The opening copy (§8.1). The planned-work items (§8.6). W17–W21. | `cp20-update.md`, `cp20-claims.md`; an updated withheld list | Every statement has a claim ID and a file/row source. No withheld phrasing. No v2+ content after 2026-04-07. |
| **B: Evidence layer** | `research.py`, `research_claims.py`, the markup contract (§9.3), the README markers and generator, tests 29–32 | Modules and tests | Tests green, negative controls included. No typed research number in any generator. |
| **C: MLflow preparation, local only** | Spec doc (`docs/track-b/mlflow-tracking-spec.md`). The read-only probe. The local rehearsal, including an interrupted upload that resumes and the deliberate faults. The export and manifest. A publisher dry run. Test 34. | Export files, `mlflow-capabilities.json`, the scripts | The rehearsal's verifier passes. An interrupted upload resumes without duplicates. The deliberate faults are caught. No public write. |
| **D1: Visual specimen** | A locally rendered page, built with real content, containing: (1) the opening with the v1 preview, the status pair and the action hierarchy; (2) the branching lineage and the full seven-policy comparison; (3) a complete v3 chapter with its caveats and one secondary diagnostic opened; (4) the longest badge, the long H−P endpoint, an evidence row, a table and disclosure states; (5) desktop and phone layouts of the same content, plus a local seven-generation navigation stress case; (6) a specimen of the demo states. Delivered with a token sheet and screenshots at the §11.3 widths. The reader tasks are run. | The local page, the token sheet, screenshots, the reader-task record | **Ready to extend when:** the Owner approves both the desktop and the phone composition; the hierarchy of result, limitation and evidence is clear; no scientific meaning depends on colour or hover; real content fits; and the reader tasks show no confusion between research progress and the released product. |
| **D2: Full page and surfaces** | The v2 chapter (with its road) and v1 with its archive. The system view. The reproduction and contribution sections. The fixes for F02, F03 and F05. The Space states (§7.11). The README block. The Space cards and `app/public/claims.json`. Test 33 and the extended `test_23`. | Generated page, README, cards and Space build | Tests 17–34 green. `make verify`. No fetches. The size budget holds. The §11.3 report checks pass locally. |
| **E: Review packet** | An independent claim and render check, with the reader tasks. A clean Python 3.12 CI-equivalent run. The release checks. A packet for the Owner: the local page, screenshots, the export, the manifest, the capability record and the checklist results. | The packet | The Owner approves the content. Any public action then needs its own instruction (§13). |
| **F: Publication** | Each step runs on its own instruction. F1: upload the committed export. F2: commit the index. F3: public mirror verification and route checks. F4: the final build with real links (placeholder guard). F5: the Owner's final visual approval. F6: commit and push. F7: redeploy the Space if its content changed. F8: post-deploy checks of the Pages bytes, demo startup and inference, and the MLflow routes. | Public experiment; published page; release-check record | Every step passes in order. If F3 fails, stop: the page is not published with broken routes. |

**Order:**

- Phase 0 and phases A, B and C can run in parallel.
- D1 needs A and B. D2 needs D1's approval and C's export.
- E needs C and D2. F comes last.

---

## 13. Authority and governance

**Approving this plan, a design or a phase authorizes local work only.** It never authorizes a
commit to `main`, a push, an MLflow upload or a Space redeploy.

- Each of those needs its own explicit instruction from the Owner, naming the action.
- No earlier delegation carries over, including those given on 2026-09-24.
- The Owner can also carry out any of these steps personally.

| Action | Performed by | Requires |
|---|---|---|
| Local work in phases 0–E | Executor | Approval of this revision and the Owner's instruction to execute |
| A commit to `main` | The Owner, or the executor | An explicit instruction naming that commit |
| Any public MLflow write: the probe or the upload | The Owner, or the executor | An explicit instruction naming the action, after the Owner reviews the export packet |
| A push to `origin`, which publishes the Pages site | The Owner, or the executor | The Owner's final visual approval, and an explicit instruction naming the push |
| A Hugging Face Space redeploy | The Owner, or the executor | An explicit instruction naming the redeploy. `HF_TOKEN` is used only as a stored variable. |
| Editing locked files, such as adding the MLflow step to the landing templates | Not in PRES-1. Applied later under the Owner's 2026-09-24 grant | §16, decision 4 |

**Notes:**

- **Files that stay untouched:** no locked files (`AGENTS.md`, the templates, the anchors), and
  `pyproject.toml` and `uv.lock` stay unchanged.
- **Credentials** are used only as stored variables (`AGENTS.md` § Credentials).
- **Cost:** $0. No paid service and no new project dependency.
- **Independent check (§16, decision 3).** It is mandatory, and done by a checker that did not
  write the changes: a fresh agent with no context from the build, working in a clean checkout of
  the exact candidate.
  - It verifies the data, the claims, the charts, the links and the reading experience.
  - It binds the final candidate SHA.
  - The Owner's visual approvals at D1 and at the end come in addition to it.
  - Neither external review is that check.
- **Interview capture.** Possible triggers:
  - presenting post-selection evidence honestly;
  - why MLflow mirrors the repository;
  - the unit-mixing error that the review caught;
  - designing the page for a reader instead of for the audit.

---

## 14. Risks and mitigations

| Risk | Mitigation |
|---|---|
| The page reads like a long generated document | The design specification (§7); the D1 specimen; reader tasks; the Owner's approval of both layouts |
| Meaning carried by colour alone | Labels, marker shapes and line styles; separate contrast checks for non-text elements |
| Illegible charts on phones | Mobile variants; a 12 px floor, tested |
| Design scope creep | §7.13; D1 sets the scope for D2 |
| New global styles change v1's protected content | Scoped archive styles; D1 review; the existing tests |
| The demo fails, or looks broken while it loads | The states from §7.11 in every case; Phase 0; the startup gate |
| Mixed units or misleading intervals | Typed series; a unit guard |
| Old "pending" wording survives | The reconciliation list; the phrase guard |
| The link check reports success falsely | Exit-code gate; a mocked-404 control; semantic route checks |
| Duplicate or partial MLflow packages, or drift | `run_key` idempotency; a completion flag per package; a verifier over the full history |
| Publication before review | Per-action instructions (§13); Phase F order |
| v1's claim is overstated | The verbatim label, tested; W21 |
| Server–client mismatch | Local 3.5.1 rehearsal; verification after upload |
| A token leaks through MLflow | Committed export scanned by the pre-commit guard; outbound scan |
| Overclaiming post-selection results | Evidence badges; claim maps; W1–W21 |
| The page grows too large by v7 | SVG charts; disclosures; the size budget; the stress case |
| The effort estimate is wrong | Re-estimate after Phase 0, the probe and D1 |
| Public CI turns red | A clean Python 3.12 CI-equivalent run before any push |
| v2+ data after 2026-04-07 slips into the content | A date guard on typed fields |

---

## 15. Forward look

- **Extension chapters.** Each one is filled from its checkpoint's committed report and its
  `delu-generations` runs, using the same template. It joins the main line if adopted, or appears
  as a branch if not.
- **The final model and 4.7T.** The final model keeps its generation number and name. "Final
  candidate" and "Live" are statuses shown on it (§16, decision 2). Before the page promises any
  badge for the result, the 4.7T protocol must settle three things:
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
  must resolve the Friday and Shabbat observance.

---

## 16. Owner decisions, 2026-09-24

| # | Question | Decision |
|---|---|---|
| 1 | Approve revision 3 | Approved. |
| 2 | Names for future generations | Simple numbering with the adopted change: `v4 · <adopted change>`, then v5 and so on. A number is given only after adoption. A rejected experiment stays a branch with a descriptive name. No number is reserved in advance for DDNN, VRE or any other candidate. "Final candidate" and "Live" are statuses of a specific version, never names that replace its identity. |
| 3 | Executor and independent check | A technical executor in the Engineering Lead role, in a separate execution session with a defined brief (PRES-1). The independent check is mandatory, by a checker that did not write the changes. It covers the data, the claims, the charts, the links and the reading experience. The Owner's visual approvals at D1 and at the end come in addition to it. |
| 4 | The MLflow step: templates or briefs | Briefs for now, as an explicit section with deliverables and acceptance criteria. After the route has completed and been verified once, the step is fixed in the landing templates. The Owner granted the Lockdown suspension for that specific edit. It is applied in a separate task after PRES-1's return (§10.11). |
| 5 | Capability probe | A local rehearsal, plus read-only checks against DagsHub. No public write probe. A local success does not prove that DagsHub supports a feature, so every capability is verified against the service after the authorized upload. |
| 6 | Experiment name | `delu-generations`. The references and texts on every surface are updated, and the existing history is preserved (`delu-cp2` stays untouched). |
| 7 | Contribution statement | Required, in the Owner's wording (§8.9). |
| 8 | Demo device test | Completed by the Owner on 2026-09-24. Phase 0 records it. |
| 9 | Visual tokens | Accepted as the D1 starting point (§7.3). The Owner makes the final choice in D1. |

---

## Appendix A: policy codes and public names

| Code | Public name | Definition |
|---|---|---|
| B0 | Similar-day naive | Reference and normalizer (emitted median after the common residual layer) |
| B1 | v1 · released LightGBM | The released LightGBM nine-quantile ensemble, calibrated with CQR and then isotonic regression. Shown as its development replay. |
| B2 | Daily LEAR | Daily rolling LEAR on the raw target, with capped expanding history |
| B3 | Daily LightGBM | Daily rolling LightGBM central forecast on the raw target |
| A1 | Normalized LEAR | CP-15's best challenger; part of v2's blend |
| A2–A5 | CP-15 challengers | Other adaptive policies from CP-15; not adopted |
| V2-H (H0) | v2 · blended LEAR, hour-aware intervals | The fixed B2/A1 blend with hour-aware residual intervals (CP-16 H). CP-20's H0 is the same policy. |
| V2-P | v2 control | The same blend with pooled residual intervals |
| HG | v3 · weather features | v2 plus three frozen GFS weather features and their missing indicators (CP-20) |
| `v1_reference`, `c1_*`, `c2_aci_gamma_*` | CP-10 candidates | Calibration-only variants of v1; a branch; nine-quantile scores |
