# CP-24 publication packet (draft)

**PUBLISH_RULES 1.3 §11; capstone v21-r11 §23.12; template `docs/track-b/publication-packet-template.md` (SHA-256 4efb0185…829cf).** Filled from inside CP-24, in every outcome; a stop is recorded as such. Numbers are never typed into a surface: each value names the committed row it comes from. Identities that exist only at landing are marked **pending-at-landing**. Nothing here is published.

Pinned rules (the issued brief also records them): PUBLISH_RULES 1.3 `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4`; packet template `4efb01855ae2d9a6f54b5624607a93046b1fffa881e34af0c6798c513c7829cf`. Both verified by `cp24.inputs.identities`.

## 1. Identity

| Item | Value |
|---|---|
| Checkpoint | CP-24, brief `docs/track-b/evidence/cp-24/issued-brief.md` at `a3f11470dde0a36e9bdf84fbf02de0597ae3d0eca4c4c75f18e79ab173c34bd0` |
| Governing research plan and version | `capstone_v21.md` v21-r11 §23 (SHA-256 `11068e3f…ed2d2`); rule `cp24-adoption` |
| Evidence tag and tip | `evidence/cp-24` at **pending-at-landing** (the evidence tip SHA is in the CP-24 return), frozen **pending-at-landing** |
| Final reviewed candidate (model code) | recorded in the CP-24 checkpoint return; a commit cannot contain its own SHA |
| Report, review verdict, landing record | `reports/ddnn2/report.md`; `docs/track-b/evidence/cp-24/integration.md`; landing record **pending-at-landing** |

**Outcome:** adopted; pre-fold rounds 1 (gates passed: round 1 yes); scored attempts 1.

## 2. The draft registry entries (standard §5)

### `v5` — generation

| Field | Value |
|---|---|
| `id` | v5 |
| `name` | v5 · DDNN-2 member added |
| `subtitle` | v4 plus a DDNN-2 member |
| `short` | v5 |
| `kind` | generation |
| `codes` | CP-24: v5 (common-10747h, scored attempt 1) |
| `statuses` | adopted in research, pending-at-landing, pending-at-landing: the CP-24 landing record |
| `comparator` | `v4` (named by §23.5 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §23 (v21-r11); `cp24-adoption` |
| `sources` | `reports/ddnn2/attempt-1/metrics.csv`, `reports/ddnn2/attempt-1/uncertainty.csv`, `reports/ddnn2/attempt-1/criteria.csv`, `reports/ddnn2/attempt-1/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp24-claims.md` |
| `run_keys` | `cp24`, `cp24/v5` |
| `style`, `anchor` | v5; #v5 — v5's colour is the Owner's decision before the publication brief (PUBLISH_RULES §14) |
| `checkpoint`, `after` | CP-24; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | v4 |

### `ddnn2-alone` — study arm

| Field | Value |
|---|---|
| `id` | ddnn2-alone |
| `name` | DDNN-2 alone |
| `subtitle` | A day-level distributional network with its own quantiles |
| `short` | DDNN-2 alone |
| `kind` | study arm |
| `codes` | CP-24: D2 (common-10747h, scored attempt 1) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-24 landing record, a study arm for attribution; never eligible |
| `comparator` | `v4` (named by §23.5 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §23 (v21-r11); `cp24-adoption` |
| `sources` | `reports/ddnn2/attempt-1/metrics.csv`, `reports/ddnn2/attempt-1/uncertainty.csv`, `reports/ddnn2/attempt-1/criteria.csv`, `reports/ddnn2/attempt-1/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp24-claims.md` |
| `run_keys` | `cp24/D2` |
| `style`, `anchor` | study; none |
| `checkpoint`, `after` | CP-24; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

### `v3-plus-ddnn2` — study arm

| Field | Value |
|---|---|
| `id` | v3-plus-ddnn2 |
| `name` | v3 plus a DDNN-2 member |
| `subtitle` | DDNN-2 as v3's third member, in LightGBM's place |
| `short` | v3 + DDNN-2 |
| `kind` | study arm |
| `codes` | CP-24: v3+D2 (common-10747h, scored attempt 1) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-24 landing record, a study arm for attribution; never eligible |
| `comparator` | `v3` (named by §23.5 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §23 (v21-r11); `cp24-adoption` |
| `sources` | `reports/ddnn2/attempt-1/metrics.csv`, `reports/ddnn2/attempt-1/uncertainty.csv`, `reports/ddnn2/attempt-1/criteria.csv`, `reports/ddnn2/attempt-1/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp24-claims.md` |
| `run_keys` | `cp24/v3+D2` |
| `style`, `anchor` | study; none |
| `checkpoint`, `after` | CP-24; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

## 3. The claim map

`docs/track-b/research-content/cp24-claims.md` (SHA-256 `918a71f269b4d2e24a7bdb107825aa1476cf32e2adaa04e80e5d506dd5f3f774`): every claim with its committed rows, the entry gates, every round's gate, the steering record, the adoption decision, every §23.8 contrast and diagnostic, and the withheld claims W42–W48 (W1–W41 stay in force).

## 4. The derived headline quantities (standard §3.3), computed inside the checkpoint

| Quantity | Value | From |
|---|---|---|
| The gate results | round 1: passed | `reports/ddnn2/rounds/round-<r>/gate.json` |
| The number of rounds and scored attempts | 1 pre-fold round(s); 1 scored attempt(s) | `reports/ddnn2/rounds/`, `reports/ddnn2/attempt-<k>/`, `steering/` |
| The adjusted level | condition 1 of `cp24-adoption` at two-sided 97.5% (the 1.25% and 98.75% percentiles of the shared replicates), splitting 5% across the cap of two attempts; per-fold condition 4 at 95% | CAP §23.9 |
| (a) The pre-specified verdict (deciding attempt 1) | `cp24-adoption`: **v5 is adopted in research as v5 ("v5 · DDNN-2 member added", predecessor v4)** (first unmet condition None; unmet []) | `reports/ddnn2/attempt-1/decisions.json` |
| The rule, in words, with the date it was set | v5 is adopted in research only if, against v4, both paired score differences improve at 97.5% (interval score upper endpoint below zero, point error at or below zero), it meets all six original screening diagnostics, the evaluation is complete and valid with every guard activation reported, no fold is decisively worse, and both point estimates improve v4 by at least 0.5%. Set **2026-10-05** | CAP §23.9; `protocol.json` `rule_verbatim` |
| Distance from v4, in the rule's unit | ΔS_MAE −0.0133 (97.5% upper −0.0091); ΔS_WIS −0.0119 (97.5% upper −0.0084) | `uncertainty.csv` L112, L113 |
| N: policies tested against the same rule up to this decision | 1 v5 candidate(s), one per scored attempt; DDNN-2 alone and v3 + DDNN-2 are never eligible | `protocol.json` `arms` |
| "Point comparison" label needed? | no — every difference has an interval | `uncertainty.csv` |
| (b) The change against v4, as a share of v4's score | S_MAE −2.5%; S_WIS −2.4% | `uncertainty.csv` L112, L113 (`ratio`) |
| Its 95% interval | S_MAE [−3.0%, −1.8%]; S_WIS [−2.8%, −1.7%] — CP-24's own draws: seed 15042, 2,000 replicates, 7-calendar-day blocks | `uncertainty.csv`; `replicates.parquet` |
| Its 97.5% interval, the decision level (§23.8) | S_MAE [−3.0%, −1.7%]; S_WIS [−2.9%, −1.6%] — the 1.25% and 98.75% percentiles of the same stored draws | `ratio-intervals.csv` L2, L3 |
| (c) Mean absolute error per period, EUR/MWh (v5) | ordinary periods 4.8–14.4; stress period, fold 3: 45.5 | `metrics.csv` per-fold rows |

## 5. Draft slot texts (standard §6)

Only the outcome the rule yields is drafted. The §4 lint's code and status-word rules on every draft: **0 findings**.

| Slot key | Draft |
|---|---|
| `v5.question` | Does a day-level distributional neural network, added to {g:v4.name} at a fixed one-sixth weight, improve on it jointly in point and interval accuracy? |
| `v5.change` | {g:v5.name} adds a distributional neural network, written in NumPy and tuned on training data only, inside the nonlinear third of {g:v4.name}. |
| `v5.main_chart.headline` | Against {g:v4.name}, the point-error score changed by {r:cp24.ratio.v5-HGL.MAE} and the interval score by {r:cp24.ratio.v5-HGL.WIS}, each as a share of the comparator's score. |
| `v5.reading` | Both scores improved against the comparator at the adjusted level, by more than the practical size, and no test period was decisively worse. |
| `v5.not_established` | Development evidence after selection, not a test on new data. |
| `v5.decision` | Adopted in research on {g:v5.status.date}; the released model is unchanged. |
| `v5.evidence` | the report, the review verdict, the claim map, the MLflow comparison |
| `transition.v4-v5.title` | From v4 to v5: adding a distributional neural network |

### 5a. The adopted transition (A3)

See the slot `transition.v4-v5.title`; the comparator is the predecessor, v4.

### 5b. The released model's documentation (A4)

Not applicable: the released model does not change (v1; §23.9).

### 5c. The chart routes (A5)

The v5 chapter's paired differences against v4 (`#v5`).

### 5d. Final-product transition / daily operation (A7/A8)

Not applicable: no final-product designation, rollout or Live.

## 6. The MLflow export

- **Draft export:** `reports/ddnn2/mlflow-export-draft/cp24.json` (SHA-256 `ead221fbdccfdd1ce589c0844493e46d981fc96249d347fdf823afa6fd62ce21`), built by `python -m cp24.export` importing `scripts/mlflow_export.py`'s functions unchanged, from CP-24's committed rows and `draft-registry.json`; experiment `delu-generations`; pending fields as listed in the draft registry.
- **Local tracking:** the same runs in `.local/mlruns/cp24`, read back equal (`reports/ddnn2/mlflow-local.json`). No upload, no network call; MLflow telemetry disabled.
- **The published export set** (`reports/presentation/mlflow-export/`) and `scripts/mlflow_export.py` are unchanged; `scripts/mlflow_export.py --check` passes.

## 7. Checks the checkpoint ran

- `tests/cp24/` (re-derivation, the rule on synthetic fixtures, DST fixtures, the search procedure, the import audit, the finite-difference checks, the reference record) and the full default suite, in a clean detached worktree.
- The §4 lint on every draft slot text: 0 findings.

## 8. Publication completion receipt — intended identities (publisher completes the rest)

| Surface | Intended identity | Action / unchanged rationale | Observed | Verification | Outstanding |
|---|---|---|---|---|---|
| GitHub source / README | after the Owner's landing and decisions (§23.12) | pending the Owner | pending | pending | pending |
| GitHub Pages | after the Owner's landing and decisions (§23.12) | pending the Owner | pending | pending | pending |
| Public MLflow | after the Owner's landing and decisions (§23.12) | pending the Owner | pending | pending | pending |
| Hugging Face Space card | after the Owner's landing and decisions (§23.12) | pending the Owner | pending | pending | pending |
| Hugging Face direct demo | after the Owner's landing and decisions (§23.12) | pending the Owner | pending | pending | pending |

- **Authority:** none exercised; every external action needs the Owner's instruction for that action.

