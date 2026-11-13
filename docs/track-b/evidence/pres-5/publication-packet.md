# PRES-5 publication packet

**PUBLISH_RULES 1.5 §11; the brief `docs/track-b/evidence/pres-5/issued-brief.md` (SHA-256
`9eb2a58433f41739fc22744854c4c55b099cc05ca729b677e9b3b5ccef87ebc3`); the packet template
`docs/track-b/publication-packet-template.md` (SHA-256 `4049c3e1f695034ec45fa185d465fce05ab1183cbded72188306579d7287d01a`).**
This packet completes CP-28's draft packet (`reports/cp28/publication-packet.md`, `a0a7f04c…b906`) into PRES-5's, with
CP-26's re-baseline and the freeze (CP-17, CP-17b, CP-17c). It publishes what decision 28 and research v21-r20 §24.14
item 6 cover: A1 in v5's comparison, on v5's own population; CP-26's re-baseline on every development day; CP-28's
selection; the freeze with 4.7T's registered terms; and the live product. Every value below names the committed row it
comes from; the evidence layer re-derives it and the page renders it from the record. Identities that exist only after
the review, the final build or the Orchestrator's steps are written `<…>` and filled in the return and by the receipt
(§8).

**The public name.** By ruling O30 the final candidate is the generation **"v6 · DDNN-2 alone"**, status "final
candidate · pending 4.7T". Its frozen records call it A1 (CP-28's arm, CP-17c's freeze); every surface that shows its
identity says "v6 (A1 in the frozen records)". Below, "v6" and "A1" name the same policy: identity
`720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`.

## 1. Identity

| Item | Value |
|---|---|
| Publication block | PRES-5, brief `docs/track-b/evidence/pres-5/issued-brief.md` at `9eb2a584…ebc3`, issued 2026-11-05 (`main` `3c8e158c`) |
| Publication anchor | `docs/PUBLISH_RULES.md` revision 1.5, `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e` |
| Research constraint anchor (read-only) | `capstone_v21.md` v21-r20, `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`; §24.14 (decision 28), §24.7 (CP-26), §24.8 (CP-28), §24.12–§24.13 (the freeze and 4.7T) |
| The Owner's decision | Decision 28, `docs/track-b/owner-decisions-2026-11-05.md`, `4daa5617…0215`: publish and go live now; A1 frozen and untouched; 4.7T exactly as registered |
| Checkpoints published | CP-26 (the re-baseline on every development day, landed `61658c7`, 2026-10-21); CP-28 (the selection, rule `cp28-selection`, evidence `1a86c54`, 2026-10-25); the freeze: CP-17 (`3876bcd`, 2026-10-28), CP-17b (`9b89774`, 2026-10-29), CP-17c (`2628804`, 2026-10-30), with 4.7T's rule `fresh-test-4-7t` (registered 2026-10-28) |
| Evidence tags and tips | `land/cp-26` `61658c7`; `evidence/cp-28` `1a86c54`; `evidence/cp-17` `3876bcd`; `evidence/cp-17b` `9b89774`; `evidence/cp-17c` `2628804`; `evidence/pres-5` `<evidence_tip_sha>` — `registry.py::EVIDENCE_TAGS` |
| Reports, verdicts, landing records | CP-26: `reports/rebaseline/cold-rerun-2026-10-15/presentation-v21-r16/report.md`, `docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/integration-final-r16-2-PASS.md`, `docs/track-b/cp-26-landing-2026-10-21.md`. CP-28: `reports/cp28/report.md` (`316d5505…8daa`), `docs/track-b/evidence/cp-28/integration.md` (`3df3797e…56fd1`), `docs/track-b/cp-28-landing-2026-10-25.md`. The freeze: `docs/track-b/evidence/cp-17c/integration.md` (`e9482e32…15be`), `docs/track-b/cp-17c-landing-2026-10-30.md`; the registered protocol `docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md` (`337a102d…7c58`) |
| This block's candidate and evidence tip | `<final_candidate_sha>` and `<evidence_tip_sha>` on `gauntlet/pres-5`, off `main` `3c8e158c` |

## 2. The registry entries, as entered (standard §5; runbook §2 and §3)

**v6, the final candidate (CP-28's A1; ruling O30).**

| Field | Value |
|---|---|
| `id`, `name`, `short` | `v6`, "v6 · DDNN-2 alone", "v6" |
| `subtitle` | "DDNN-2 alone, refitted daily, frozen for 4.7T" (eight words) |
| `kind`, `predecessor` | generation; `v5` (A3's transition "From v5 to v6") |
| `codes` | CP-28 `A1` (`cp28-paired-days`, selected); PRES-5 `A1` (`common-10747h`, v5's population); CP-26 `nominal/D2/{all_eligible, never_scored, old_fold_2_5, newly_opened}` (CP-26's four masks, descriptive) |
| `statuses` | final candidate, 2026-10-30, `docs/track-b/cp-17c-landing-2026-10-30.md`: "selected by CP-28's rule on 2026-10-25 and frozen for 4.7T; pending 4.7T". No adoption event: v5's rule never ran on it (W49) |
| `comparator` | `v5` (CP-28's control, nominal v5; the comparison on v5's population pairs it with v5 and with the naive) |
| `population`, `evidence_class` | `cp26-every-day`; development, post-selection |
| `plan`, `rules` | `capstone_v21.md` §24.8 and §24.12; `cp28-selection` (set 2026-10-12), `fresh-test-4-7t` (registered 2026-10-28) |
| `sources` | `reports/cp28/owner-summary.json`, `publication-packet.json`, `results/selection.json`; `reports/pres5/a1-in-v5/{metrics,uncertainty,ratio-intervals}.csv`, `summary.json` |
| `claim_map`, `run_keys` | `docs/track-b/research-content/pres5-claims.md`; `cp28`, `cp28/A1`, `cp26/nominal/D2/*` |
| `style`, `anchor` | `v6`: near-black `#18181B`, a filled hexagon (a visual choice for the Owner, O16); `#v6` |
| `checkpoint` | CP-28 |
| Frozen label | `registry.py::FROZEN_LABELS = {"v6": "A1"}`: the lint's code denylist admits `A1`, v6's frozen label, anywhere; that every `A1` on the reading path sits beside v6's identity is a review check, not the lint's (Integration review 1, F5) |

**CP-28's six other arms (O30): study arms, "not selected", named without their codes.** Each: kind study arm; code
CP-28 `A2`…`A7` (`cp28-paired-days`); status not adopted, 2026-10-25, `docs/track-b/cp-28-landing-2026-10-25.md`,
"passed every registered gate and was not selected: v6 had the lowest interval score"; comparator `v5`; run key
`cp28/A2`…`cp28/A7`. Names: "Equal-weight blend of v5's members" (A2), "Fitted blend weights, half shrunk" (A3),
"Per-block blend weights" (A4), "Small-network blend, half shrunk" (A5), "Fitted blend weights, unshrunk" (A6),
"Small-network blend, unshrunk" (A7). The page's arms table marks each "Not selected" and v6 "Selected".

**CP-26's entries.** `cp26-rebaseline` (reference, the checkpoint's owner); `v1-recipe-daily` — "v1's recipe, refitted
daily" (reference; CP-26 `nominal/v1-R/*`); six study arms, never eligible, not adopted 2026-10-21 ("a sensitivity
route of the re-baseline"): v3/v4/v5 with weather six hours late (`gfs6/*`) and v3/v4/v5 without the load forecast
(`noload/*`). CP-26's codes are added to the naive (`nominal/B0/*`) and to v2–v5 (`nominal/v2/*` … `nominal/v5/*`),
each under its own experiment (`registry.py::_with_cp26`); no published MLflow record changes (§6).

**The lists.** `CHECKPOINTS` gains CP-26 (run key `cp26`, 52 children: route × policy × mask) and CP-28 (`cp28`, owner
`v6`, children A1–A7); `EVIDENCE_TAGS` gains `land/cp-26`, `evidence/cp-28`, `evidence/cp-17`, `evidence/cp-17b`,
`evidence/cp-17c` and `evidence/pres-5` (dated by its tip); `RULES` gains `cp28-selection` and `fresh-test-4-7t`;
`POPULATIONS` gains `cp26-every-day`, `cp26-never-scored`, `cp26-old-folds`, `cp26-newly-opened` and `cp28-paired-days`;
`COMPARISON_ORDER` puts v6 first; `COMPARISON_EXPERIMENTS` gains PRES-5, so v6's comparison row comes from PRES-5's
rows and every other row stays CP-24's (`comparison_source`). `V5_COMPARISON_ORDER` keeps PRES-4's twelve rows for the
pinned `cp24/v5` overview chart, which therefore stays byte-identical in MLflow.

**Experiment codes stay scoped.** `A1` is CP-15's normalized LEAR and CP-28's arm; `by_code("A1")` without an
experiment is refused, and `by_code("A1", "CP-28")`, `by_code("A1", "PRES-5")` resolve to v6 (`tests/test_50`).

## 3. The claim maps

Registered in `research_claims.py::CLAIM_MAPS`: `pres5-claims.md` (`2004752f…fab5f`). Its claims: C901–C908 (v6 on v5's population), C601–C605 (CP-26 on every development day) and C607
(CP-26's disclosures, carried into v6's limitations), C701–C706 (CP-28's selection), C801–C804 (the freeze and 4.7T's
registered terms), and the publication's own wording P60–P66 (P60 the headline and its terms; P61 the final candidate's
term and the product line; P62 the comparison with v6 first; P63 CP-28's arms in the registry; P64 the planned list;
P65 the transition; P66 "How the product works" for v6, with C403 for its inputs). Withheld: W1–W48 in force; PRES-5 adds W49–W53, each guarded in
`research_claims.py::WITHHELD_PATTERNS` with negative controls in `tests/test_50`:

- W49 calling v6 (A1) "adopted" or "adopted in research" (v5's rule never ran on it);
- W50 presenting v6's comparison on v5's population as made under v5's protocol or information set;
- W51 pooling CP-26's every-day results with the five periods, or calling either a test on new data;
- W52 presenting a live forecast, score or price, or a number on a day after 2026-09-06, as research, or the live
  record as 4.7T's result;
- W53 giving v6 the status "live" or "released", or calling it the released product, before a passed 4.7T.

(Corrected after Integration review 2, N1, to the claim map's and `WITHHELD_PATTERNS`' definitions.) That no surface
says the Space, its root or its app runs v1 now is a separate check, `tests/test_50::test_no_surface_says_the_space_runs_v1_now`,
with its negative control (Integration review 2, G1).

## 4. The derived headline quantities (standard §3.3), re-derived from committed rows

| Quantity | Value | From |
|---|---|---|
| (a) The pre-specified verdict | `cp28-selection`: **met** — all seven arms passed every gate in all four analyses; among them A1, now v6, had the lowest interval score and was selected (`derived.cp28.tested` = 7) | `reports/cp28/results/selection.json`; `owner-summary.json` |
| The rule, in words, with its date | Seven recombinations of v5's members, each against v5 on every development day: both scores better by more than 0.5%; no complete year 2021–2025 or pooled season more than 2% worse; the largest one-sided p-value as the arm's test; Holm across the seven at 0.05; in the primary analysis and all three sensitivity variants; among those that pass, the lowest interval score wins. Set **2026-10-12** | `capstone_v21.md` §24.8; `docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md` (frozen before CP-26's first score); `registry.py::RULES["cp28-selection"]` |
| Distance from the comparator, the rule's unit | ratio to nominal v5 on 2,068 paired development days: MAE −7% [−9%, −5%] (−6.90%; −9.07%, −5.14%), WIS −11% [−13%, −9%] (−10.93%; −12.85%, −8.96%); Holm-adjusted p 0.0042 (main analysis) | `cp28.arm.A1.{MAE,WIS}.ratio_to_control` → `derived.cp28.A1.*`; `cp28.holm.primary14.A1.adjusted_p` |
| N | 7 arms tested against the rule (`derived.cp28.tested`) | `selection.json` |
| "Point comparison" label needed? | no: every difference has an interval | — |
| (b) On v5's population: the change against v5, as a share of v5's score | S_MAE −6% (−5.65%), S_WIS −11% (−11.40%) | `reports/pres5/a1-in-v5/uncertainty.csv` L22–L23 `ratio` → `derived.change.v6.*` |
| Its 95% interval | S_MAE [−9%, −2%] (−9.03%, −2.45%); S_WIS [−15%, −8%] (−14.54%, −7.89%) — CP-24's own index set: seed 15042, 2,000 replicates, 7-day blocks (`summary.json` `bootstrap.index_equals_cp20` true) | `uncertainty.csv` `ratio_ci_lower`/`ratio_ci_upper` = `ratio-intervals.csv` |
| Its 97.5% interval (the level v5's rule decided at) | S_MAE [−10%, −2%] (−9.64%, −2.12%); S_WIS [−15%, −8%] (−15.07%, −7.52%) | `ratio-intervals.csv` `ratio_ci97.5_*` → `derived.change_decision.v6.*` |
| Against the naive | S_MAE −51% [−54%, −46%]; S_WIS −56% [−59%, −52%] | `derived.change_naive.v6.*` |
| The scores themselves | v6 S_MAE 0.4928, S_WIS 0.4374; v5 0.5223, 0.4937 (CP-24's published rows, unchanged; parity maximum difference 0.0) | `metrics.csv` L8; `parity.json` |
| (c) MAE per period, EUR/MWh (v6) | ordinary periods 4.5–13.4; stress period (fold 3, 2022) 43.2 (v5 45.5) | `metrics.csv` per-fold rows → `derived.periods.v6.*` |
| Coverage of v5's population | 10,747 of 10,747 hours, 448 of 448 days, every day from v6's own forecasts (no fallback); the first period lies in CP-26's unscored warm-up (90 days) | `summary.json` `coverage`, `information_set` |

**CP-26 on every development day (descriptive, beside the five periods, never pooled).** 2,068 eligible days,
2020-12-29 to 2026-09-06, every policy refitted daily under one protocol: v5 against v4, MAE −1% [−1%, +1%] and WIS
−1% [−1%, +1%] (`derived.cp26.v5-v4.*`; CP-26's paired non-circular moving-block bootstrap, 14-day blocks, 10,000
replicates, seed 20261012); v6 against v5 on the same days, −7% and −11% (`derived.cp26.v6-v5.*`, equal to CP-28's
control ratios).

## 5. Slot texts, as published (standard §6)

Rendered from `research_claims.py`; every number is a record. The §4 lint (`make lint-publication`): 0 findings.

| Slot | Block | Claim |
|---|---|---|
| The question | `v6.question` | C901 |
| The change, with its diagram | `v6.change`; `build_pages.py::a1_change` | C901 |
| The main chart and its headline | `v6-c2a`: v6 − v5 on both scores, each at 95% and at the level v5's rule decided at (four rows); `v6.chart_headline` | C902 |
| The reading | `v6.reading` | C903 |
| Not established | `v6.caveat.information` (the comparison shares hours and prices, not the protocol), `v6.caveat.selection` (post-selection; 4.7T is its one test) | C904, C905 |
| The decision, dated | `v6.decision`: selected 2026-10-25 by the rule set 2026-10-12, frozen 2026-10-28, re-frozen unchanged 2026-10-30; "selected by its own rule, never adopted by v5's" | C906 |
| The evidence row | the raw CSV rows at `evidence/pres-5`; CP-28's verdict and report; the freeze's verdict; the registered protocol | — |
| Details | method (`v6.method.network`, `v6.method.scoring`, `v6.method.information`); per-period consistency (`v6.folds` and its value table, `v6.absolute`); the 2022 crisis (`v6.stress`); coverage and width (`v6.coverage`); protocol and review (`v6.rule`, `v6.selection` and the arms table, `v6.holm.note`, `v6.freeze`, `v6.fresh.window`, `v6.fresh.terms`, `v6.fresh.rules`, `v6.fresh.meaning`) | C901, C902, C904, C907, C908; C701–C705; C801, C803, C804 |

The headline (P60; decision 20): "Selected by a rule set before any result: against v5 on all 2,068 development days,
−7% [−9%, −5%] in point error and −11% [−13%, −9%] in interval error, as shares of v5's, with descriptive 95%
intervals; 7 policies tested." with the badge
"Development · post-selection", beside the status pair "Live product · v6 · DDNN-2 alone" and "Final candidate · pending
4.7T · v6 · DDNN-2 alone" (O27). The terms under it: daily errors, the selection rule, final candidate, policies tested,
the evidence class, DDNN-2.

**CP-26's every-day panel** (`#everyday`, C601–C605): its question, population and evidence class, v5 against v4
and v6 against v5 on every development day, "never pooled with the five periods above".

### 5a. The adopted transition (A3) — "From v5 to v6" (O30)

| Field | Value |
|---|---|
| Title | `transition.v5-v6.title`: "From v5 to v6: DDNN-2 alone" (P65) |
| Predecessor and dates | v5 · DDNN-2 added, adopted in research 2026-10-11; v6 selected 2026-10-25, frozen 2026-10-30, status final candidate |
| The change | `transition.v5-v6.change`: DDNN-2 alone, refitted every day; v5's two LEAR forecasts, its LightGBM and the blend dropped. "It is A1 in the frozen records." |
| The comparator set in advance | v5 (CP-28's control), which is the predecessor |
| The result, with its evidence class | `transition.v5-v6.result`: the every-day ratios with their intervals, and the same on v5's five periods; development, post-selection, not 4.7T |
| What it does not establish | `transition.v5-v6.limits` (page): selected by its own rule, never adopted by v5's; its forecasts come from a later, daily protocol; 4.7T is its one test on new data |
| The decision and the route | `v6.decision`; "The comparison chart and its evidence, in the v6 chapter" → `#v6-chart-title` |

### 5b. The product's documentation (A4) — v6, the product the Space runs (O26, O29)

Decision 28 makes the live product v6 now; the Orchestrator ruled (O29) that "How the product works" documents v6,
decision 28 prevailing over decision 21's timing (decision 21's fail branch survives). v1's manual is preserved in v1's
chapter, its archive and git history; no surface says or implies that the Space runs v1 now
(`tests/test_50::test_no_surface_says_the_space_runs_v1_now`).

| Subject (§5.1) | Disposition | Evidence | Route |
|---|---|---|---|
| 1 Data and the information cutoff | supported | `v6.product.sources`, `v6.product.cutoff`, `v6.product.windows` (P66); CP-17c's inputs | `#product-data` |
| 2 Regimes and negative prices | supported | `v6.product.regimes.periods` (v1's regime counts, named as v5's five test periods' hours: editorial V7), `v6.product.regimes` | `#product-regimes` |
| 3 Inputs; 3b seasonal rationale | supported | `v6.product.inputs` (C403), `product.inputs.seasonal` (shared) | `#product-inputs` |
| 4 Validation | supported | `v6.product.validation`: selection on development days, 4.7T registered | `#product-validation` |
| 5 Results | supported | `v6.product.results` → the v6 chapter's chart | `#product-results` |
| 6 Attribution | not evaluated in research | `v6.product.attribution`; routed to the Space's Explainability view | `#product-attribution` |
| 7 Importance and sensitivity | not evaluated in research | `v6.product.importance`; routed to the Space's Features view | `#product-importance` |
| 8 Where it fails | supported | `v6.product.failures` → per-period differences | `#product-failures` |
| 9 Reliability | supported | `v6.product.reliability` → coverage and width | `#product-reliability` |
| 10 Read a forecast | supported, on the live product | `v6.product.forecast`; the opening's labelled development preview (`PREVIEW_DAY` 2026-04-07, `reports/pres5/a1-in-v5/preview-day.csv`) | `#product-forecast` |
| 11 Limitations | supported | `v6.product.limits` (C607) | `#product-limitations` |
| 12 Running it | supported | `v6.product.run`; the freeze's verdict | `#product-run` |

Incoming product v6; outgoing v1, "the last released generation", whose demo is historical under the Space's
`/history/`.

### 5c. The chart routes (A5)

| Chart | Its heading | The route | Where it starts |
|---|---|---|---|
| `v6-c2a` (main) | `#v6-chart-title` | "The comparison chart and its evidence, in the v6 chapter"; from product topic 5, "v6's comparison chart, in its chapter" | the v5 → v6 transition card; product topic 5 |
| (text and tables) | `#v6-information`, `#v6-per-period-differences`, `#v6-absolute-errors`, `#v6-crisis`, `#v6-coverage`, `#v6-selection`, `#v6-freeze`, `#v6-fresh-test` | each heading's own words | v6's "Explore these results" |
| every-day panel | `#everyday` | its heading | the comparison section |
| `overview` | `#comparison-finding` | "Compare model results" | the opening |

### 5d. Final-product transition / daily operation (A7/A8/A9)

| Field | State |
|---|---|
| Owner designation and lifecycle | v6 (A1) selected 2026-10-25, frozen 2026-10-30; live by decision 28 through CP-18c; status "final candidate · pending 4.7T" (O13, O27); 4.7T's pass or fail decides the release (decision 21's branches, preserved) |
| One product identity | the report's opening, "How the product works", the README and the Space (CP-18c, the same public name, O30) name v6; MLflow tracks the research runs `cp28/A1` and `cp26/nominal/D2/*`. The report shows no live number |
| Frozen policy, daily training and issuance, coverage, today, scores, reliability | CP-17c's freeze and CP-18c's live pipeline: not this block's output. The report links the Space and says "prospective evaluation in progress" |
| Page order | A4's order, with "How the product works" documenting v6; A8's product-first order (Product results, Business insights before the comparison) is **not applied**: proposed ruling in §10, item 1 |
| Business evidence | not evaluated; nothing is claimed |
| Prospective state | in progress from CP-18c's first live day; nothing prospective is published here |

## 6. The MLflow export

| File | SHA-256 | Runs |
|---|---|---|
| `reports/presentation/mlflow-export/cp26.json` | `46483ce99154bf1890502de6cc96730cb9c2008ec4f80558782fbae4833d65c4` | `cp26` and its 52 children (route × policy × mask) |
| `cp28.json` | `226863998eaffd593d18dd400c86fe5cedc498e8e4429f43f608c3c667b836d7` | `cp28` and `cp28/A1` … `cp28/A7` |
| `manifest.json` | `57216cc680ee28719196c8c5e71faa8d24990e5cd502d94907601cd291a2e16f` | 105 runs: 10 parents, 95 children |
| `cp10` … `cp24` | unchanged bytes (`git diff 3c8e158c` empty on each) | the 44 published runs |

- **Built** from CP-26's and CP-28's committed drafts (`mlflow_export.py::pres5_runs`), with the registry's names,
  statuses, populations and comparability tags; `pres5_draft_problems()` is empty (each metric equals its draft's).
- **Against the published set** (`--diff-against 3c8e158c`; `pres-5-export-diff.json`): 44 → 105 runs, the 61 of cp26
  and cp28 added; no identity or substantive change to any published run; the one experiment-tag change is
  `mlflow.note.content` (naming CP-26 and CP-28).
- **The routes** the registry expects: `experiment`; `compare:overview` (twelve runs, `cp24/v5` to `cp15/B0`: v6's row
  has no CP-24 run, so the overview route lists the twelve runs MLflow holds, and the page says so in its audit);
  `compare:v6` (`cp28/A1` … `cp28/A7` and `cp26/nominal/v5/all_eligible`); the earlier routes unchanged. Each is linked only
  once the index covers it.
- **The upload, only after the independent check's PASS** (the brief's one authorized external action). The
  authenticated read-only gate first, then the bounded upload; the DagsHub variables are read inside the process only:

  ```bash
  MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true uv run python scripts/mlflow_publish.py --precheck
  ```

  ```bash
  MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true uv run python scripts/mlflow_publish.py --target public --owner-instruction "<the brief's authorization, verbatim, with the PASS's SHA and date>" --authorized-runs cp26,cp26/gfs6/v3/all_eligible,cp26/gfs6/v3/never_scored,cp26/gfs6/v3/old_fold_2_5,cp26/gfs6/v3/newly_opened,cp26/gfs6/v4/all_eligible,cp26/gfs6/v4/never_scored,cp26/gfs6/v4/old_fold_2_5,cp26/gfs6/v4/newly_opened,cp26/gfs6/v5/all_eligible,cp26/gfs6/v5/never_scored,cp26/gfs6/v5/old_fold_2_5,cp26/gfs6/v5/newly_opened,cp26/noload/v3/all_eligible,cp26/noload/v3/never_scored,cp26/noload/v3/old_fold_2_5,cp26/noload/v3/newly_opened,cp26/noload/v4/all_eligible,cp26/noload/v4/never_scored,cp26/noload/v4/old_fold_2_5,cp26/noload/v4/newly_opened,cp26/noload/v5/all_eligible,cp26/noload/v5/never_scored,cp26/noload/v5/old_fold_2_5,cp26/noload/v5/newly_opened,cp26/nominal/B0/all_eligible,cp26/nominal/B0/never_scored,cp26/nominal/B0/old_fold_2_5,cp26/nominal/B0/newly_opened,cp26/nominal/D2/all_eligible,cp26/nominal/D2/never_scored,cp26/nominal/D2/old_fold_2_5,cp26/nominal/D2/newly_opened,cp26/nominal/v1-R/all_eligible,cp26/nominal/v1-R/never_scored,cp26/nominal/v1-R/old_fold_2_5,cp26/nominal/v1-R/newly_opened,cp26/nominal/v2/all_eligible,cp26/nominal/v2/never_scored,cp26/nominal/v2/old_fold_2_5,cp26/nominal/v2/newly_opened,cp26/nominal/v3/all_eligible,cp26/nominal/v3/never_scored,cp26/nominal/v3/old_fold_2_5,cp26/nominal/v3/newly_opened,cp26/nominal/v4/all_eligible,cp26/nominal/v4/never_scored,cp26/nominal/v4/old_fold_2_5,cp26/nominal/v4/newly_opened,cp26/nominal/v5/all_eligible,cp26/nominal/v5/never_scored,cp26/nominal/v5/old_fold_2_5,cp26/nominal/v5/newly_opened,cp28,cp28/A1,cp28/A2,cp28/A3,cp28/A4,cp28/A5,cp28/A6,cp28/A7 --authorized-experiment-tags mlflow.note.content --log reports/presentation/release-checks/pres-5-mlflow-upload.json
  ```

  It refuses before the first write unless every write belongs to those 61 runs or to the one experiment tag. Then
  `verify_mlflow_mirror.py verify --target public` (`pres-5-public-mirror.json`), `check_reader_paths.py mlflow-routes`
  (`pres-5-public-mlflow-routes.json`), `verify_mlflow_mirror.py index`, and the `--final` build.

## 7. Checks run

Records under `reports/presentation/release-checks/` unless a path says otherwise. First failures and superseded runs
are kept beside their retries. The candidate's code is `14d13f6a`: Integration review 1's repairs (`d487b4bd`), review
2's (`e86528a1`, the README's generator and `tests/test_50`) and review 3's (`14d13f6a`: `delu.adopted` in the export,
and the rule's timing worded "set in advance"); the candidate adds this packet and the records.

| Check (runbook §9; the brief) | Record | Result |
|---|---|---|
| The offline checks, `scripts/prerelease.py --stage pre-final`, from a clean detached worktree at `14d13f6a`: the browser payload; pytest on Python 3.13; a clean Python 3.12 run of every CI step; `make verify`; `make lint-publication`; the rebuild and `git status`; links; the publication guard | `pres-5-pre-final-5-prerelease.json` (raw output local only, `.local/worktrees/pres-5/prerelease/.local/artifacts/prerelease/pres-5-pre-final-5/`) | 2026-11-13, 49 min: every check as expected except three, each explained in §10.3: pytest 3.13, 3,242 passed, 9 skipped, 2 failed (CP-18a's two push tests refuse the non-final build record until the `--final` build); CI 3.12 pytest, 3,240 passed, 12 skipped, 1 failed (CP-17c's manifest test off the pinned interpreter on this Mac, item 6); links, 2 failed (the `evidence/pres-5` tag is not pushed yet, item 5); the rebuild changed no path; the guard exits 1 as expected before the `--final` build |
| — its earlier runs | `pres-5-pre-final-4-prerelease.json` (at `e86528a1`, before review 3's repair), `pres-5-pre-final-3-prerelease.json` (at `d487b4bd`, before review 2's repair), `pres-5-pre-final-2-prerelease.json` (at `1d0f453e`, before Integration review 1's repairs) and `pres-5-pre-final-prerelease.json` (at `b20ee9d1`, before the editorial repairs): the same three explained results, nothing else | superseded by the run above |
| The full suite in the lead worktree | local runs at `ef77b8e4` (3,229 passed; 2 failed, CP-18a's, by design) | superseded by the prerelease |
| `make lint-publication` | inside the prerelease record; also run after every build | PASS: page, README and templates 0 findings |
| `make publication-guard` | inside the prerelease record | BLOCKED by design until the `--final` build: `reports/cp3/pages_build.json` is a non-final build record |
| Determinism: `rebuild_presentation.py`, then `git status` | inside the prerelease record; also in the lead worktree at `1d0f453e` | every generated surface equals its committed bytes |
| The page budget | `reports/cp3/pages_build.json` | 1,848,408 bytes ≤ 2,000,000 (151,592 to spare), with the archive's seven figures re-encoded without loss (O25; `compact_figures --check`: pixel-identical) |
| The §10 release checks and the placements, Chrome 157.0.8103.51 and WebKit 26.6, at 1440 × 900, 768 × 1024, 390 × 844, 360 × 780, 320 × 640 and the emulated iPhone 393 × 659 | `pres-5-local-release.json` (at `14d13f6a`'s page, `fd9887bd…4b3c`, 2026-11-13 10:22 UTC) | **passed**: the headline block ends at 774.6 / 775.3 px (desktop) and 628.6 / 628.7 px (phone); the finding at 1,667.6 / 1,668.3 px (A2 limit 1,744) and 2,394.5 / 2,394.3 px (limit 2,420); chart text at least 12.21 px (320 px), 14.58 px (390 px) and 12.38 px (1440 px); no chart overlap or clipping, no collapsed space, no horizontal overflow; no console error, failed request, HTTP error or resource after the document; accessibility trees, keyboard (160 stops), touch targets at 390 px (none under 24 px), contrast, 200% zoom and 320 px reflow, in both engines |
| — its earlier attempts | `.local/artifacts/pres-5/local-release-4.json` (passed at `d487b4bd`'s page, `409e1708…1cbe`, 2026-11-13 00:07 UTC, the finding at 1,672.6 / 2,394.5 px); `pres-5-local-release-at-1d0f453e.json` (passed at `1d0f453e`'s page, `2fcb53ac…d9ca`, 2026-11-12 14:18 UTC, the same placements; before review 1's repairs); `.local/artifacts/pres-5/local-release-1.json` (failed: the finding at 1,769.6 / 2,695.5 px; the product line not where the release check reads it; three routes reaching closed copies; v6's chart ticks overlapping); `local-release-2.json` (passed except three tap targets under 24 px; its screens are the fresh reader's) | superseded |
| A5 discovery, from the closed default page, by mouse, keyboard and deep link | inside the release record | 48 routes in each engine at both placement sizes |
| v6 on v5's population | `uv run python -m delu_forecast.final_candidate --check`; `reports/pres5/a1-in-v5/parity.json` | v6's rows re-derive byte for byte from the pinned inputs; v5's and the naive's recomputed scores equal CP-24's published rows (maximum difference 0.0) |
| The export | `pres-5-export-diff.json`; `mlflow_export.py --check`; `tests/test_50::test_no_export_calls_v6_adopted` | current at `14d13f6a`; runs 44 → 105, the 61 of cp26 and cp28 added, `only_identity` true, no identity or substantive change, the one experiment-tag change `mlflow.note.content`; `pres5_draft_problems()` empty; v6's five runs `delu.adopted = "false"`, `delu.status` "final candidate 2026-10-30" |
| The publisher, dry run (no `--target`) | the run's output, local | at `14d13f6a`: 105 runs, 17,003 metric points, 229 artifacts in the plan; the outbound credential-value scan clean; nothing written |
| The value-based secret scan | `scripts/secret_guard.py` | the pre-commit and commit-msg hooks on every commit; the pre-push scan over `gauntlet/pres-5` at the evidence tip, in the return |
| One editorial review | `docs/track-b/evidence/pres-5/editorial.md` (at `b20ee9d1`) | 12 violations (V1–V12), repaired in `1d0f453e`; 18 recommendations, dispositioned (§10.4) |
| The fresh reader | `docs/track-b/evidence/pres-5/fresh-reader.md` | answers 1–5 agree with the records; two reading-path gaps repaired; observations dispositioned; continued applicability recorded |
| Integration review 1, at `b866e996` | `docs/track-b/evidence/pres-5/integration-review-1.md` | **FAIL**: F1, the live product's startup line lacked §7.1's measured start, browser, date and last verification, and its size was typed (the editorial V4 deferred); F2, §8.2's command for a moved `main` used `--pathspec-from-file`, which `git diff` 2.50.1 rejects; F3, nothing checked the `evidence/pres-5` label's date; F4, "v5 and v4 are level" read a null result as equivalence; F5, the packet overstated what the lint checks for `A1`. All five repaired in `d487b4bd` (§10.4) |
| Integration review 2, at `9bb0cff8` | `docs/track-b/evidence/pres-5/integration-review-2.md` | **FAIL**: review 1's acceptance test met in every part; G1, the README's CP-3 section still said in the present tense that the Space runs v1's champion boosters at its root (the editorial V5's sentence, missed by the first repair), and no check guarded it; notes N1 (§3's W-list misdescribed), N2 (nothing set the evidence date), N3 (`reports/cp17c/inputs.json` records the five modules' old hashes). Repaired in `e86528a1` (§10.4) |
| Integration review 3, at `f865ff94` | `docs/track-b/evidence/pres-5/integration-review-3.md` | **FAIL**: reviews 1's and 2's acceptance tests met; F1, the export tagged v6's five runs `delu.adopted = "true"` (`registry.adopted_flag` counted "final candidate" as adopted), which W49 forbids and which the upload would have published. Repaired in `14d13f6a` (§10.4) |
| Integration review 4 at the repaired candidate, and the focused recheck at the final SHA | `docs/track-b/evidence/pres-5/integration.md` | after this packet |
| The authorized MLflow upload, the mirror verification, the browser routes and the index | `pres-5-mlflow-upload.json`, `pres-5-public-mirror.json`, `pres-5-public-mlflow-routes.json`, `reports/presentation/mlflow_index.json` | after the independent check's PASS, before the `--final` build |

No real Safari, real iPhone or screen reader was used; the phone widths are emulated viewports, and the iPhone is
Playwright's emulated device in WebKit.

## 8. Publication completion receipt and the Orchestrator's packet

### 8.0 What would be published

| Surface | Reviewed output | Identity | Now public |
|---|---|---|---|
| Report, GitHub Pages | `docs/index.html` at `<final_candidate_sha>`, the `--final` build | `<final_page_sha256>` (the return and `integration.md`); at the candidate, before the index, `1,848,408` bytes, `fd9887bd94b26a077815559343a7f4c8c54dc13ac678d622a69e07be6f1c4b3c` | 1,996,267 bytes, `54708134fdfeb2ce3f2ee2d04b1f93008b7506917690a74d93548951a18d37ce` (PRES-4, `main` `3c8e158c`) |
| README | `README.md` at `<final_candidate_sha>` | `<final_readme_sha256>` | at `main` `3c8e158c`: `c816972a7ddb4509f4e7617f4f480588b2500becb9217d8d36a4afebee8315fc` |
| Hugging Face Space and its card | **CP-18c's**, not this block's: PRES-5 uploads nothing to the Space | CP-18c's reviewed bundle and card identities, from CP-18c's return | revision `0331088725fedab2f5a1ec804ae03bf960cf126f` (PRES-4's v1 bundle) until CP-18c publishes |
| MLflow `delu-generations` | `reports/presentation/mlflow-export/` | 105 runs; `cp26.json` `46483ce9…65c4`, `cp28.json` `22686399…36d7`, `manifest.json` `57216cc6…e16f`; the 61 runs of cp26 and cp28 and the one experiment-description write, uploaded under the brief's authority before the final build (§6), their run IDs in `pres-5-public-mirror.json` | 44 runs, no cp26 or cp28 run (PRES-4) |

The report links the Space and names what it runs; its content is CP-18c's. If CP-18c has not published when these
steps run, the link and its wording stand (the brief's task-specific extract), and the public checks of the Space run
after both publications.

### 8.1 Receipt — intended identities (the Orchestrator and the public checker complete the rest)

| Surface | Intended identity | Action / unchanged rationale | Observed public identity and UTC time | Verification record and result | Outstanding action |
|---|---|---|---|---|---|
| GitHub source / README | `land/pres-5` (the squash of `<evidence_tip_sha>`, the same tree on PRES-5's paths); README `<final_readme_sha256>`, whose glance and generation list name v6 | push (§8.3) | to fill: pushed revision, time | `pres-5-publication-receipt.json` (GitHub main); the served README's hash (§8.5) | §8.2–8.3 |
| GitHub Pages | `<final_page_sha256>`: v6's headline with the live product, v6's chapter and transition, the comparison with v6 first, the every-day panel, the freeze and 4.7T's terms, "How the product works" for v6 | deploy by the push (§8.3) | to fill: served hash, time | `pres-5-publication-receipt.json` (Pages); `pres-5-public-report.json`; `pres-5-postdeploy-links.json` | §8.3, §8.5 |
| Public MLflow | `cp26` and `cp28` with their children in `delu-generations`, equal to the export; routes `experiment`, `compare:overview`, `compare:v6` and the earlier ones; the experiment description naming every parent; the 44 earlier runs unchanged | the authorized upload in this block, verified before the final build (§6) | run IDs and verification time: `pres-5-public-mirror.json` | `pres-5-public-mirror.json`, `pres-5-public-mlflow-routes.json`; after publication `pres-5-postdeploy-mlflow-mirror.json`, `pres-5-public-mlflow-routes-postdeploy.json` | post-deployment reverification (§8.5) |
| Hugging Face Space card | CP-18c's | **no PRES-5 action**: CP-18c's deployment | to fill from CP-18c's receipt | CP-18c's records; `pres-5-publication-receipt.json` (Space files) against CP-18c's reviewed bundle | after both publications |
| Hugging Face direct demo | CP-18c's live product at the root; v1's historical demo at `/history/` | **no PRES-5 action** | to fill | the same; the report's two Space links answer 200 (`pres-5-postdeploy-links.json`) | after both publications |

- **Publication-to-MLflow mapping:** `<final_candidate_sha>` → exports `cp26.json`, `cp28.json` (and `manifest.json`) →
  the run IDs in `pres-5-public-mirror.json` → the routes in `reports/presentation/mlflow_index.json`.
- **Final product and daily updates:** CP-18c's (§5d). The report carries no live record.
- **Completion disposition:** incomplete until these steps and their public checks; A12 (§8.6) decides whether an
  independent post-deployment check is required.
- **Authority:** the MLflow upload and the one experiment-description write, by the brief. The landing, the push and
  the Pages deployment are the Orchestrator's, after the return (the brief's "Owner-only actions already authorized";
  decisions 27 and 28). There is no Space step in PRES-5.

Every command below runs from the primary checkout, `/Users/djourno/Downloads/PJM`. None opens a pager or an editor.
Substitute `<evidence_tip_sha>`, `<land_sha>`, `<final_page_sha256>` and `<final_readme_sha256>` from the return, which
gives these commands with them filled in. Keep every record a step writes, first failures included.

### 8.2 Step 1 — the LAND

The primary checkout was on `main` at `3c8e158c9895f5b3fed13db794b0ddd5fb80c56f` = `origin/main`, clean, with no stash,
when read on 2026-11-06 at 13:02 UTC. CP-18c works beside PRES-5 on disjoint paths; if CP-18c lands first, `main` moves:
use the variant marked **(main moved)** below.

```bash
git --no-pager rev-parse --abbrev-ref HEAD
```

Expect `main`.

```bash
git --no-pager rev-parse HEAD gauntlet/pres-5
```

Expect `3c8e158c9895f5b3fed13db794b0ddd5fb80c56f` (or CP-18c's landing, if it landed first), then `<evidence_tip_sha>`.

```bash
git --no-pager status --porcelain=v1
```

Expect no output (or only ` M progress.md`, the Orchestrator's own edit). Any other line: stop and resolve it first.

**No untracked twin:**

```bash
git --no-pager diff --name-only 3c8e158c9895f5b3fed13db794b0ddd5fb80c56f <evidence_tip_sha> | while IFS= read -r f; do git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 && ! git --no-pager diff --quiet -- "$f" && echo "MODIFIED $f"; git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 || { [ -e "$f" ] && echo "TWIN $f"; }; done; echo twins-checked
```

Expect only `twins-checked`.

```bash
git --no-pager merge --squash gauntlet/pres-5
```

Expect `Squash commit -- not updating HEAD` and the diffstat; no `CONFLICT` line (with `main` at `3c8e158c`, also
`Updating 3c8e158c..<first 7 of evidence_tip_sha>` and `Fast-forward`).

**The staged tree equals the evidence tip's tree** (main unmoved):

```bash
git --no-pager diff --cached --name-only <evidence_tip_sha> && test "$(git write-tree)" = "$(git rev-parse '<evidence_tip_sha>^{tree}')" && echo STAGED-TREE-EQUALS-EVIDENCE-TIP
```

Expect only `STAGED-TREE-EQUALS-EVIDENCE-TIP`. If it does not print, stop: nothing is committed yet, and
`git reset --merge` restores the index.

**(main moved)** — PRES-5's paths equal the evidence tip's, and every other path equals `main`'s:

```bash
git --no-pager diff --name-only 3c8e158c9895f5b3fed13db794b0ddd5fb80c56f <evidence_tip_sha> > .local/artifacts/pres-5/pres5-paths.txt && xargs git --no-pager diff --cached --quiet <evidence_tip_sha> -- < .local/artifacts/pres-5/pres5-paths.txt && test -z "$(git --no-pager diff --cached --name-only HEAD | grep -vxFf .local/artifacts/pres-5/pres5-paths.txt)" && echo STAGED-PRES5-PATHS-EQUAL-EVIDENCE-TIP
```

Expect only `STAGED-PRES5-PATHS-EQUAL-EVIDENCE-TIP`. PRES-5's paths and CP-18c's are disjoint (the brief's task-specific
extract), so a line in between means a path both changed: stop. (Git 2.50.1's `git diff` has no `--pathspec-from-file`;
the command passes the paths through `xargs`, which fails if any comparison differs. Integration review 1, F2.)

**The evidence label's date equals the tip's** (Integration review 1, F3): the page labels v6's raw rows "frozen
<date>" from `registry.py::EVIDENCE_TAGS["evidence/pres-5"]`. The Lead sets that date by hand in the final-build
commit, to that commit's date, and the evidence tip follows on the same day (Integration review 2, N2); this check
confirms it before the tag is made.

```bash
git --no-pager log -1 --format=%cs <evidence_tip_sha> && git --no-pager show <evidence_tip_sha>:src/delu_forecast/registry.py | grep '"evidence/pres-5"'
```

Expect the same date on both lines. A different date: stop and report it; the label would misdate the evidence.

```bash
git commit -F .local/artifacts/pres-5/land-commit-message.txt
```

Expect `[main <land_sha>] Publish PRES-5: …`. The secret guard runs in the pre-commit and commit-msg hooks and prints
nothing when clean.

```bash
git tag land/pres-5 HEAD
```

```bash
git tag evidence/pres-5 <evidence_tip_sha>
```

Both print nothing.

```bash
git --no-pager diff --stat HEAD <evidence_tip_sha>
```

Expect no output when `main` had not moved (with **(main moved)**, only CP-18c's paths).

### 8.3 Step 2 — the push

**The value-based secret scan first**, over exactly what the push will send:

```bash
printf '%s %s %s %s\n' refs/heads/main "$(git rev-parse main)" refs/heads/main "$(git rev-parse origin/main)" refs/tags/land/pres-5 "$(git rev-parse land/pres-5)" refs/tags/land/pres-5 0000000000000000000000000000000000000000 refs/tags/evidence/pres-5 "$(git rev-parse evidence/pres-5)" refs/tags/evidence/pres-5 0000000000000000000000000000000000000000 | python3 scripts/secret_guard.py pre-push origin "$(git remote get-url origin)" && echo SECRET-SCAN-CLEAN
```

Expect `SECRET-SCAN-CLEAN`. A `secret-guard: BLOCKED` line means stop and tell no one the value.

```bash
python3 scripts/publication_guard.py tree
```

Expect a PASS line: the landed page is the final build.

```bash
git push origin main land/pres-5 evidence/pres-5
```

Expect `<old>..<first 7 of land_sha>  main -> main` and two `[new tag]` lines. GitHub Pages then serves `docs/`. Then
read GitHub's CI for the pushed commit (`gh run list --branch main --limit 3`) before the closure: GitHub's ubuntu runner
differs from the local one.

### 8.4 Step 3 — no Space upload

PRES-5 changes nothing on Hugging Face. The Space is CP-18c's to deploy; its root serves the live product and its
`/history/` route v1's historical demo. If the served Space is not what CP-18c's return names, that is CP-18c's to
resolve; do not redeploy under this packet.

### 8.5 Step 4 — the public checks, per surface

Each writes a new record; keep a first failure beside its retry. The Playwright commands need
`PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright`. Wait until Pages has deployed the
push (the first command returns `<final_page_sha256>`).

```bash
curl -s https://hrsi56.github.io/delu-day-ahead-forecast/ | shasum -a 256
```

Expect `<final_page_sha256>` once Pages has deployed (now `54708134…37ce`, PRES-4's).

```bash
curl -s https://raw.githubusercontent.com/hrsi56/delu-day-ahead-forecast/main/README.md | shasum -a 256
```

Expect `<final_readme_sha256>`.

**The receipt** (automation item 6): GitHub `main`, Pages, the Space's files and direct page against CP-18c's reviewed
bundle, the public MLflow mirror and the links, each checked independently and anonymously, every attempt kept. Run
it after both publications, with CP-18c's reviewed bundle directory and its SHA-256 from CP-18c's return:

```bash
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true uv run python scripts/publication_receipt.py --landing <land_sha> --bundle <CP-18c's reviewed Space bundle directory> --expect <its SHA-256, from CP-18c's return> --date pres-5
```

Expect the six §8 rows each `PASS` and `PASS: wrote reports/presentation/release-checks/pres-5-publication-receipt.json`,
with `pres-5-postdeploy-links.json` and `pres-5-postdeploy-mlflow-mirror.json` beside it; exit 0. If the Space rows
fail only because CP-18c's Space is not a static bundle that the receipt's file check can compare, record the failure,
keep it, and verify the Space with CP-18c's own public checks; the GitHub, Pages, MLflow and link rows still bind.

The browser records:

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py release https://hrsi56.github.io/delu-day-ahead-forecast/ --shots .local/artifacts/pres-5/public-report --out reports/presentation/release-checks/pres-5-public-report.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py mlflow-routes --mirror-record reports/presentation/release-checks/pres-5-postdeploy-mlflow-mirror.json --shots .local/artifacts/pres-5/public-mlflow-postdeploy --out reports/presentation/release-checks/pres-5-public-mlflow-routes-postdeploy.json
```

Each passes with `passed` true. GitHub may answer anonymous `blob` requests with 503 after a burst: keep the failed
receipt, wait, and rerun it with a new `--date` (for example `pres-5-retry-1`); a 503 is never a pass.

### 8.6 Step 5 — A12, then the receipt

**A12 (§10.5).** An independent post-deployment check is required if either:

1. a served surface differs from what the binding independent pre-deployment review covered: Pages' bytes (after the
   documented normalization of hosting injections) differ from `<final_page_sha256>`, the focused recheck's page; or
   the public MLflow differs from the committed export (`pres-5-postdeploy-mlflow-mirror.json` not equal); or
2. a required public check above fails without a passing targeted retry.

The Space's bytes are CP-18c's review's, not this one's. If neither condition arises, the receipt and the browser
records are the public-check record, and the closure states that neither arose. Where one arises, a checker that wrote
none of PRES-5 reads those records and the served surfaces fresh, forms its findings before reading earlier reviews,
and writes a dated review under `docs/track-b/` with the per-surface identities, the §9 matrix it could apply, first
failures and retries, and its PASS / FAIL / INCOMPLETE verdict. **Where it can add something** even without a trigger:
the one surface no PRES-5 review saw served is the report's links into CP-18c's Space (the live product and
`/history/`); a short independent look at those two routes after both publications is the useful check.

Then fill §8.1's last three columns from the records: the observed identity and UTC time per surface, the record and
its result, and any outstanding action. The disposition is complete only when every row is verified.

### 8.7 If publication fails

Stop the rollout and name each affected URL and revision. The identities to restore are `main`
`3c8e158c9895f5b3fed13db794b0ddd5fb80c56f` (Pages `54708134fdfeb2ce3f2ee2d04b1f93008b7506917690a74d93548951a18d37ce`).
PRES-5 does not touch the Space. The uploaded cp26 and cp28 runs stay: they are the committed evidence, and removing a
tracking run is not part of any recovery. No force-push, history rewrite or MLflow change is part of a recovery; a
rollback is its own Owner action.

## 9. Applicability matrix

### 9.1 PUBLISH_RULES 1.5, clause by clause

| Clause | Applies? | How PRES-5 meets it, or why not | Evidence |
|---|---|---|---|
| §1.1–§1.3 authority, four identities, categories | yes | Rules 1.5 and the research anchor v21-r20 pinned by hash in the brief and checked; the publication rule, the research generation (v6, final candidate), the product status (the live Space runs v6; v1 the last released generation) and the artifact identities (policy `720fc581…`, the exports, the page) kept apart | §1; the return's identities |
| §2 reader contract and placements; A1; A2 | yes | Each headline number names its metric (A1); the headline block on the first screen; the finding within A2's limits in Chrome and WebKit with the measured header; the product identity line beside the action, outside disclosures | `tests/test_43` A1; `pres-5-local-release.json` (`placements`) |
| §3.1 evidence classes; withheld claims | yes | Development, post-selection on every v6, CP-26 and CP-28 number; nothing live, prospective or 4.7T's; W1–W53 in force, W49–W53 guarded | `v6.caveat.*`; `WITHHELD_PATTERNS`; `tests/test_50` |
| §3.2 scores, comparisons, uncertainty | yes | CP-28's verdict with its rule, date and N; on v5's population the change as a share of v5's score with the ratio's interval from CP-24's own draws at 95% and at 97.5%; absolute MAE per period with the stress period apart; CP-26's every-day results as their own population, never pooled; v5's and the naive's rows are CP-24's, never recomputed (parity 0.0) | §4; `reports/pres5/a1-in-v5/parity.json`; `tests/test_50` |
| §3.3 counting | yes | CP-28's N (7) is its rule's; the comparison's 13 rows are distinguished from it; the targets' census unchanged; study arms, references and generations distinct kinds | `RC.census_sentence`; `tests/test_43` |
| §3.4 provenance and formatting | yes | Every number a record; whole percents, four significant figures, one decimal for EUR/MWh | `make lint-publication` PASS |
| §4 registry, transitions, branches; A3 | yes | One registry; v6 a generation (O30) with its dated final-candidate status and no adoption event; the transition "From v5 to v6" with its evidence class (A3); CP-28's six other arms study arms, "Not selected"; CP-26's sensitivity routes study arms, never eligible | §2; `tests/test_43` A3; `tests/test_50` |
| §4 A10 revision in place | no | No adopted generation is revised in place | — |
| §5 page architecture; A4 | yes | A4's order; "How the product works" documents v6, the product the Space runs (O26/O29), with the twelve-subject map (§5b) | `tests/test_45`; §5b |
| §5 A8 product-first order | not applied | See §10, item 1: a proposed ruling | — |
| §5.2 chapter grammar; page budget | yes | v6's chapter fills every slot (`slot_problems` empty); one page, `1,848,408` bytes ≤ 2.0 MB, by pixel-identical re-encoding of the archive's seven figures (O25) | `tests/test_50`; `reports/cp3/pages_build.json` |
| §6 charts, discovery; A5 | yes | v6's main chart with direct labels and its hexagon marker; the comparison with v6 first; A5 routes from the closed default page in both engines | `pres-5-local-release.json` (`discovery`) |
| §7.1 product contract | yes, changed | The opening names the product the Space runs (v6), its status and why it runs before its test (decision 28), beside "Open the live product"; the first visit's size beside the action (its measured start: §10.3 item 4); v1's historical demo linked at `/history/` | the opening; `tests/test_38`, `tests/test_43` F03 |
| §7.2 live presentation; A7 | the Space's (CP-18c) | The report shows no live panel and no live number (§24.14 item 5); it links the Space and says "prospective evaluation in progress" | `tests/test_24`, `tests/test_50` |
| §7.3 final-product Space; A9 | the Space's (CP-18c) | Not this block's surface | CP-18c's return |
| §8 surfaces | yes | Report, README and MLflow updated and in agreement; the Space is CP-18c's (§8.4) | §8 |
| §9 browser and accessibility matrix | yes | Chrome and WebKit, every width, accessibility trees, keyboard, touch, contrast, zoom and reflow, requests, placements | `pres-5-local-release.json` |
| §10.1 independence | yes | The editorial review, the fresh reader and the Integration Critic authored none of the changes | `editorial.md`, `fresh-reader.md`, `integration.md` |
| §10.2 fresh reader | yes | The six unchanged questions, closed-state screens only, answers kept | `fresh-reader.md` |
| §10.3 public identity; A6 | yes, after the Orchestrator's steps | The receipt and the browser records on the public URLs | §8.5 |
| §10.4 verdict | yes | The Integration verdict | `integration.md` |
| §10.5 A12 | yes, after deployment | Its two conditions and the useful check named in §8.6 | §8.6 |
| §11 packet and order | yes | This packet; build → editorial → fresh reader → independent check → upload and verification → final build → recheck → the Orchestrator's steps | §7 |
| §12 baseline coverage | yes | Incorporated clauses applied through the rows above; invariant 10's date 2026-09-06 holds for every research number | `tests/test_36`, `tests/test_50` |
| §13 acceptance record | yes | §9.2 below | — |
| §14 pending triggers | yes | "Before final-candidate test: its badge, wording, fresh headline window and hero-switch rule" — decided by decisions 20 and 21 and rulings O27/O30; "Before Live" — CP-18c's | the brief; §10 |
| A11 work availability | yes | `AGENTS.md` § Work availability; the pauses were usage limits (§10, disclosures) | — |

### 9.2 The §13 acceptance record

| Area | Record |
|---|---|
| Authority | Rules 1.5 `1bc0c523…f94e`; research anchor v21-r20 `80341681…30e6`; decision 28 `4daa5617…0215`; brief `9eb2a584…ebc3`; A7–A10 handled as §9.1 states |
| Identity | `gauntlet/pres-5` off `3c8e158c`; `<final_candidate_sha>`; `<evidence_tip_sha>`; the landing and served identities after the Orchestrator's steps |
| Claims | §4: source rows by blob and line, derivations, class, comparator and population, N, the limitations |
| Reader | Default path and placements (`pres-5-local-release.json`); definitions under the headline; the fresh reader's record |
| Journey | The v5 → v6 transition; CP-28's six other arms as study arms; CP-26's every-day panel; the planned list brought up to date (4.7T, the live trial, new input data, wind and solar) |
| Content | The twelve product subjects for v6 (§5b); v1's chapter and archive preserved; the archive's figures pixel-identical |
| Charts | v6's main chart; the comparison with v6 first; A5 routes |
| Product | The live product's identity and status beside its action; v1's historical demo linked; the Space is CP-18c's |
| Accessibility | The engine and width matrix (`pres-5-local-release.json`) |
| Tracking | The upload record, the mirror verification and the browser routes (§6) |
| Release | `--final` build, guard and test results; the exact-candidate Integration check; the authorized upload's record |
| Public check | After the Orchestrator's steps (§8.5–§8.6) |
| Follow-up | §10's open items with proposed rulings; the editorial review's and the fresh reader's findings, each dispositioned |
| Final product, daily panel, business, final-product Space | CP-18c's surfaces; the report's part is §5d |

### 9.3 The runbook

| Section | Touchpoint | Status |
|---|---|---|
| §2.1 `_ENTRIES` | v6 with every field and its dated final-candidate status (no adoption event); CP-28's six arms; CP-26's references and study arms; CP-26's codes on the naive and v2–v5 | done |
| §2.2 `CHECKPOINTS` | CP-26, CP-28 | done |
| §2.3 `EVIDENCE_TAGS` | `land/cp-26`, `evidence/cp-28`, `evidence/cp-17`, `-17b`, `-17c`, `evidence/pres-5` | done |
| §2.4 `RULES` | `cp28-selection`, `fresh-test-4-7t` | done |
| §2.5 `COMPARISON_ORDER` | v6 first; v6's row from PRES-5's rows (`COMPARISON_EXPERIMENTS`), every other row CP-24's | done |
| §2.6 `CRISIS_ORDER` | unchanged: v6's chapter states the 2022 period in text | not needed |
| §2.7 `research.py::SOURCES` | PRES-5's rows, CP-28's and CP-26's records, pinned by blob and tag | done |
| §2.8 `CRITERIA_FILES` | not needed: v6's verdict is CP-28's rule's, derived from `selection.json` (`derived.cp28.*`) | not needed |
| §2.9 `CHANGES` | `RATIO_CHANGES["v6"]`, `NAIVE_RATIO_CHANGES["v6"]`, `DECISION_LEVEL_CHANGES["v6"]`; CP-28's and CP-26's control changes | done |
| §2.10 `PERIOD_SUBJECTS` | `PERIOD_SOURCES["v6"]` = PRES-5 | done |
| §2.11 claim maps | `pres5-claims.md` | done |
| §2.12 / 12a `BLOCKS` | `v6.*`, `transition.v5-v6.*`, `everyday.*`, `terms.*`, `product.live*`, `v6.product.*` | done |
| §2.13 / 14 `a1_slots`, `chapter_sequence` | done |
| §2.15 `CHARTS_BY_RUN` | `cp24/v5`'s overview pinned to v5's twelve rows (`PINNED_CHARTS`), so no published artifact changes | done |
| §2.16 `TOKENS` and CSS | near-black `#18181B`, a filled hexagon, "v6" — a visual choice for the Owner (O16) | done; §10 |
| §2.17 `mlflow_export.py` | `EXPERIMENT_NOTE_CHECKPOINTS` and `PRES5_EXPORTS` (cp26, cp28) | done |
| §2.18 tests | `tests/test_50` and updates to tests 24, 29, 30, 34–39, 43, 45, 49; CP-26's two landed-code tests (O34) | done |
| §2 "Limits to watch" | placements with A2's header (both engines); chart text ≥ 12 px; the 2.0 MB budget | `pres-5-local-release.json`; the build record |
| §5 status transitions | `final candidate` used for the first time: the hero's research half, the badge and the headline window per decision 20 and O27 | done |
| §7a product documentation | v6's twelve subjects (§5b); v1's preserved | done |
| §1 order; §1a receipt; §8 routes; §9 checks | as §7 and §8 of this packet | done / the Orchestrator's |

### 9.4 The brief's observable outcome

| Outcome | Where it is met | Evidence |
|---|---|---|
| 1 v6 (A1) in v5's comparison, done properly | v5's population, all keys covered from v6's own stored forecasts, the information-set differences stated (`v6.caveat.information`, `v6.method.information`); v5's and the naive's rows CP-24's; paired comparisons v6 − v5 and v6 − naive with the rule's intervals; never "adopted" (W49) | `reports/pres5/a1-in-v5/`; `tests/test_50` |
| 2 CP-26 on every development day | `#everyday`, beside and never pooled with the five periods; its question, population, results and class | C601–C605; `tests/test_50` |
| 3 CP-28's selection | v6's chapter: the rule, the seven arms, the result, why v6 was selected | C701–C706; the arms table |
| 4 The freeze and 4.7T's terms | `#v6-freeze`, `#v6-fresh-test`: what CP-17, CP-17b, CP-17c froze, `720fc581`, the issuing host; the window, comparators, scores, pass conditions, margins and failure rules quoted from the protocol; what a pass and a fail mean | C801–C804; `tests/test_50` (`test_the_registered_terms_are_the_protocols`) |
| 5 The product | the opening's status pair, "Open the live product", the product line, v1's historical demo at `/history/`; no live number; nothing after 2026-09-06 | `tests/test_24`, `tests/test_50` |
| 6 The model identity | v6 · DDNN-2 alone (O30); the six arms study arms | §2 |
| 7 MLflow | §6; after the Integration PASS | `pres-5-mlflow-upload.json`, `pres-5-public-mirror.json` |
| 8 The page budget | `1,848,408` bytes ≤ 2,000,000, by lossless re-encoding (O25) | `reports/cp3/pages_build.json` |
| 9 Review | the Integration check at the candidate and the focused recheck at the final SHA | `integration.md` |
| 10 The packet | this packet's §8 | — |

## 10. Rulings, disclosures and open presentation items

### 10.1 The Orchestrator's rulings in this block (decision 27)

| Ruling | What it decided | Basis |
|---|---|---|
| O25 | The archive's seven PNG figures embedded as RGB copies, pixel-identical to the originals, with a pixel-equality test | §5.2's budget; no visual change (`src/delu_forecast/compact_figures.py`, `tests/test_50`) |
| O26, O29 | "How the product works" documents v6, the product the Space runs; decision 28 prevails over decision 21's timing; decision 21's fail branch survives; v1's manual preserved in its chapter, the archive and git history; the page never says or implies that the Space runs v1 now | A4 ("the documentation follows the new product"); decision 28; `test_no_surface_says_the_space_runs_v1_now` |
| O27 | The hero: v6 "final candidate · pending 4.7T", the headline CP-28's pre-specified verdict with the development post-selection badge; v1 stays "released", "the last released generation", its demo historical at `/history/`, the product again if 4.7T fails | §4's hero order; decision 20's fresh-headline window; decision 21 |
| O30 (replaces O28) | The public name "v6 · DDNN-2 alone", a generation, on the rail and timeline, the newest comparison row, the A3 transition "From v5 to v6" with its evidence class; "v6 (A1 in the frozen records)" where the identity is shown; CP-28's six other arms study arms "not selected", without codes; the Space uses the same name | §4; A3 |
| O34 | CP-26's two landed-code tests check five presentation modules against their bytes as landed at `61658c7`, recorded under `cp26-landed-presentation-code/` and bound by SHA-256 and git blob; every other landed file stays checked against the working tree; negative controls; the two new modules named outside CP-26's landed set | the brief's allowed paths include the registry and the report's build, which CP-26's harness log pins as landed code |

### 10.2 Disclosures

- **Pauses.** The work paused six times, each time resumed by the Orchestrator from the same worktree and branch,
  without starting over: three times for the five-hour usage limit before 2026-11-06 07:55 UTC; twice more on
  2026-11-06 (about 10:45–12:50 and 13:50–17:50 UTC); and once for the weekly limit, from 2026-11-06 about 17:55 UTC to
  2026-11-12 13:50 UTC. The editorial reviewer was stopped by the same limits twice and resumed on the same checkout.
- **O34's edit outside the allowed paths:** `tests/test_cp26_r15.py` and `tests/test_cp26_repair_contract.py`, one
  assertion each, and the helper `tests/pres5_landed_code.py`; no CP-26 record, manifest or harness file changed.
- **`reports/cp17c/inputs.json`** (CP-17c's input record) also lists the five presentation modules' bytes as they were
  at CP-17c's candidate. Nothing compares that record with the working tree, the freeze reads none of those modules,
  and the freeze is untouched (Integration review 2, N3).
- **The live-namespace wall** (`tests/test_24`) admits exactly three strings on the record surfaces — the product's
  name, its status and "prospective evaluation in progress" — by decision 28 and the brief's outcome 5; every live
  figure, score, date and other sentence stays behind it, with its positive control.
- **The frozen label.** The lint's code denylist admits `A1`, v6's frozen label, wherever it appears
  (`FROZEN_LABELS`); the lint does not check that it sits beside v6's identity. Integration review 1 found every `A1`
  on the reading path beside v6 (F5). CP-15's normalized LEAR keeps its own code `A1` in the comparison's values
  table, each scoped by its experiment.
- **The overview MLflow route** lists the twelve runs MLflow holds: v6's comparison row comes from PRES-5's rows, which
  have no MLflow run; the page's audit routes v6's row to its raw CSV rows at `evidence/pres-5`.
- **Startup metadata** (§7.1; Integration review 1, F1). Beside "Open the live product" the page reads from CP-18b's
  committed records the first visit's size, the measured cold start in Chromium and WebKit, the browsers, the
  machine, the date and the last verification (`build_pages.py::live_measurement`, which refuses a record whose cold
  start failed or lacks an engine; `tests/test_43` F03). They measure the Space CP-18b built, served locally on
  development data, and the line says so; no public timing of CP-18c's Space exists yet. v1's measured start of
  2026-09-29 timed the earlier Space's root, which decision 28 gives to the live product, so the opening links v1's
  historical demo without timing it.
- **CP-26's and CP-28's intervals** on the page carry CP-26's bootstrap (14-day blocks, 10,000 replicates, seed
  20261012); v6's intervals on v5's population carry CP-24's (7-day blocks, 2,000 replicates, seed 15042). Each is
  named where it is shown.
- **Visual choices for the Owner (O16):** v6's colour `#18181B` and filled hexagon; the "Result" column of the arms
  table.

### 10.3 Open presentation items, each with a proposed ruling

1. **A8's product-first order.** A8 orders, at the Owner-designated final-product transition, "How the product works"
   → "Product results" → "Business insights" → "How the models compare". PRES-5 keeps A4's order with "How the product
   works" documenting v6, because the Owner's designation of the final product is decision 21's outcome of 4.7T (O27
   keeps v1 "released" until then), and no business evaluation exists to fill "Business insights" honestly.
   **Proposed ruling:** A8's order applies at 4.7T's publication, with the release; until then A4's order stands.
2. **The Space's receipt rows** (§8.5). `scripts/publication_receipt.py` compares a static bundle file by file; if
   CP-18c's Space is served differently, its rows may fail for a reason that is not a defect. **Proposed ruling:** the
   Space's public identity is CP-18c's receipt's; PRES-5's receipt keeps its Space rows, failures included, as records.
3. **v6's colour and marker** (§2.16): **proposed ruling:** keep `#18181B` and the hexagon until the Owner chooses.
4. **The live product's public start** (editorial V4; Integration review 1, F1, repaired). The page now shows all of
   §7.1's fields, read from CP-18b's records of the Space served locally on development data. **Proposed ruling:**
   after both publications, time the public Space in §8.5 and bind the line to that record at the next
   publication.
5. **Two links to `evidence/pres-5`** (v6's raw rows, `metrics.csv#L8` and `uncertainty.csv#L22`) answer 404 until the
   Orchestrator pushes the tag in §8.3: the prerelease's link check records them as its one unexpected result.
   **Proposed ruling:** accept them as pending destinations; the receipt's link row after the push (§8.5) must show
   them 200, and a 404 there is a failed public check.
6. **CP-17c's `test_the_committed_manifest_verifies_here` under this Mac's Python 3.12** (prerelease, CI 3.12 step):
   it fails because the issuing host's local files are present and the interpreter is not the pinned 3.13.15.
   PRES-5 changed nothing it reads (`git diff 3c8e158c` empty on `src/cp17*`, `tests/cp17*`, `reports/cp17*`), and
   `main`'s GitHub CI on Python 3.12 passes. **Proposed ruling:** out of PRES-5's scope; a follow-up for CP-17c's
   owner, to skip that assertion off the pinned interpreter as the test beside it does.

### 10.4 The reviews' findings and their dispositions

**The editorial review** (`editorial.md`, at `b20ee9d1`): twelve violations, all repaired in `1d0f453e`:

| Finding | Repair |
|---|---|
| V1 "the released model" routes reached v6's manual | v1's chapter routes to "v1's original report, topic by topic" (`#v1-archive`); the reproduction line says "To check the live product's frozen policy, see Run and check this product; v1, the last released generation, runs from its original instructions … in its archive" |
| V2 no reason why the Space runs v6 | the product line beside the action: "… daily, frozen, before its one test, by the Owner's decision to go live: prospective evaluation in progress. A pass releases it; otherwise v1, the last released generation, is the product again." (P61; decision 28; C804) |
| V3 unlabelled brackets and shares | the headline: "…, as shares of v5's, with descriptive 95% intervals" |
| V4 incomplete startup metadata | deferred at first, then repaired after Integration review 1 (F1): every §7.1 field, read from CP-18b's records |
| V5 the README's CP-3 section in the present tense | `scripts/cp3_readme.py`: a dated line says the table describes the surfaces at v1's release and where v1's demo is now; "How the product works"; the replay sentence names v1's demo; and, after Integration review 2 (G1), v1's demo paragraph dated to its release and in the past tense |
| V6 the archive's Space links | a note outside the protected archive: "The archive below links the Space as it was at v1's release; the Space's root has since been given to the live product, and v1's demo is under its History." The archive's bytes are unchanged (`tests/test_45`) |
| V7 the regimes paragraph's population | v6's own block names v5's five test periods |
| V8 the README's research introduction | "…in the shared comparison; v6's section also reports every eligible development day, a separate population" |
| V9 a typed percentage | "its point error barely moved"; the value stays in the table |
| V10 C603 on C604's clause | a separate block, `everyday.finding.v6`, bound to C604 |
| V11 a repeated caveat | the transition's "Not established" lists performance on new data and equal information; the decision keeps "selected by its own rule" once |
| V12 expiring wording | "4.7T, from 2026-12-04, is its one test on new data" |

Recommendations: **taken** — R1 (v5's same-named study arm's scores in v6's information caveat), R2 ("before any
result"; "The selection was run…"), R3 ("does not pass" / "otherwise"), R4 (the lede without the frozen label), R5
("sensitivity runs"), R7 (both re-freeze dates, "its fit unchanged"; "all 58 fits"), R14 (one decimal; "covered 0.9447
of the hours"), R16 (C908's width), R17 ("every eligible development day"). **Not taken, with reasons** — R6 (the
values table's code column names each row's own experiment's code; v6's row shows its frozen label beside its name),
R8 (the comparison's MLflow route lists the runs MLflow holds; §10.2 discloses v6's row), R9 (the label's date is set
at the final build to the evidence tip's date), R10 (`refreeze verify`'s two outputs are the freeze's own wording),
R11–R13, R15 and R18 (wording beyond the rules, left for the next publication), R12's dashed outlines (the system
view's legend is shared with earlier generations).

**The fresh reader** (`fresh-reader.md`): answers 1–5 agree with the records; its observations 1–6 and 12 were
repaired in `1d0f453e`, the rest dispositioned in its record.

**Integration review 1** (`integration-review-1.md`, FAIL at `b866e996`): F1 repaired by `live_measurement` and the
startup line's five bound fields, with F03's test and its negative controls; F2 by the `xargs` form in §8.2, tested on
this git; F3 by the date step in §8.2 and `tests/test_50::test_the_evidence_tags_date_is_the_tips`; F4 by "v5's gain
over v4 is not shown there" and "the intervals do not establish that the two are equal"; F5 by the wording in §2 and
§10.2. Its observations on the A8 order stay with §10.3 item 1.

**Integration review 2** (`integration-review-2.md`, FAIL at `9bb0cff8`): G1 repaired by `scripts/cp3_readme.py`'s
`_v1_demo_paragraph` (v1's demo paragraph dated to its release, in the past tense, with its address under History;
the claims themselves unchanged, as the v1 Space card carries them) and by
`tests/test_50::test_no_surface_says_the_space_runs_v1_now` with its negative control; N1 by §3's list and W51's and
W52's negative controls in `tests/test_50`; N2 by the explicit date step (§8.2) taken in the final-build commit; N3
disclosed in §10.2.

**Integration review 3** (`integration-review-3.md`, FAIL at `f865ff94`): F1 repaired in `14d13f6a`:
`registry.adopted_flag` returns "false" for a final candidate with no adoption or release in its history, so v6's five
runs carry `delu.adopted = "false"`; `tests/test_50::test_no_export_calls_v6_adopted` checks every exported run against
its registry history, with a negative control (a final candidate tagged "true" is caught; the rule's two branches).
The export stays current and the 44 published runs unchanged; §6's and §8.0's hashes are the new export's, the
authorized-runs list unchanged. Its recommendations: the rule's timing taken ("set in advance"; the term: "before the
re-baseline's first score"); the browser record's page hash and W53's last clause noted for the next publication.

