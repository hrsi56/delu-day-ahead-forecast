# CP-21 publication packet (draft)

**Publication Standard v1 §12; PUBLISH_RULES 1.1 §11; capstone v21-r6 §17.9; template `docs/track-b/publication-packet-template.md` (SHA-256 4efb0185…829cf).** Filled from inside CP-21. Numbers are never typed into a surface: each value below names the committed row it comes from, and the evidence layer re-derives it. Identities that exist only at landing are marked **pending-at-landing**. Publication is a separate block after the Owner's landing; nothing here is published.

Pinned rules: PUBLISH_RULES 1.1 `91eea445…7584f3`, incorporating Publication Standard v1 `01d721c2…478cc` and presentation plan revision 3 `28119374…c812c` (all verified at the pre-run freeze, protocol `issued_and_inherited_sha256`).

## 1. Identity

| Item | Value |
|---|---|
| Checkpoint | CP-21, brief `docs/track-b/evidence/cp-21/issued-brief.md` at `813fb8a476a7b6d10ecf0a5519e97ec8efc4ff36e0f13868676ad34534fc020f` |
| Governing research plan and version | `capstone_v21.md` v21-r6 §17 (SHA-256 `ee402c47…67344`), rule `cp21-adoption` |
| Evidence tag and tip | `evidence/cp-21` at **pending-at-landing** (the evidence tip SHA is in the CP-21 return), frozen **pending-at-landing** |
| Final reviewed candidate (model code) | recorded in the CP-21 checkpoint return (`docs/track-b/evidence/cp-21/checkpoint-return.md`); a commit cannot contain its own SHA |
| Report, review verdict, landing record | `reports/block-challenger/report.md`; `docs/track-b/evidence/cp-21/integration.md`; landing record **pending-at-landing** |

## 2. The draft registry entries (standard §5)

Machine-readable: `reports/block-challenger/draft-registry.json` (outcome **adopted**, derived mechanically from `adoption.json`). Statuses are dated at landing; CP-21 registers nothing.

### `v4` — generation

| Field | Value |
|---|---|
| `id` | v4 |
| `name` | v4 · three-block LightGBM added |
| `subtitle` | v3 plus a three-block LightGBM member |
| `short` | v4 |
| `kind` | generation |
| `codes` | CP-21: HGL (common-10747h) |
| `statuses` | adopted in research, pending-at-landing, pending-at-landing: the CP-21 landing record |
| `comparator` | `v3` (v3, named by §17.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §17 (v21-r6); `cp21-adoption` |
| `sources` | `reports/block-challenger/metrics.csv`, `reports/block-challenger/uncertainty.csv`, `reports/block-challenger/criteria.csv`, `reports/block-challenger/adoption.json` |
| `claim_map` | `docs/track-b/research-content/cp21-claims.md` |
| `run_keys` | `cp21`, `cp21/HGL` |
| `style`, `anchor` | v4; #v4 — v4's encoding: amber `#B45309`, filled diamond, direct label "v4" (Owner decision D6) |
| `checkpoint`, `after` | CP-21; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | v3 |

### `pooled-lightgbm-weather` — study arm

| Field | Value |
|---|---|
| `id` | pooled-lightgbm-weather |
| `name` | Pooled LightGBM with weather |
| `subtitle` | One 24-hour LightGBM on v3 information |
| `short` | Pooled LightGBM |
| `kind` | study arm |
| `codes` | CP-21: L-P (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-21 landing record, a study arm for attribution; never eligible for adoption |
| `comparator` | `v3` (v3, named by §17.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §17 (v21-r6); `cp21-adoption` |
| `sources` | `reports/block-challenger/metrics.csv`, `reports/block-challenger/uncertainty.csv`, `reports/block-challenger/criteria.csv`, `reports/block-challenger/adoption.json` |
| `claim_map` | `docs/track-b/research-content/cp21-claims.md` |
| `run_keys` | `cp21/L-P` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-21; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

### `block-lightgbm` — study arm

| Field | Value |
|---|---|
| `id` | block-lightgbm |
| `name` | Three-block LightGBM |
| `subtitle` | Night, solar and peak models, raw price |
| `short` | Block LightGBM |
| `kind` | study arm |
| `codes` | CP-21: L-R (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-21 landing record, a study arm for attribution; never eligible for adoption |
| `comparator` | `v3` (v3, named by §17.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §17 (v21-r6); `cp21-adoption` |
| `sources` | `reports/block-challenger/metrics.csv`, `reports/block-challenger/uncertainty.csv`, `reports/block-challenger/criteria.csv`, `reports/block-challenger/adoption.json` |
| `claim_map` | `docs/track-b/research-content/cp21-claims.md` |
| `run_keys` | `cp21/L-R` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-21; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

### `normalized-block-lightgbm` — study arm

| Field | Value |
|---|---|
| `id` | normalized-block-lightgbm |
| `name` | Normalized three-block LightGBM |
| `subtitle` | The block models on a normalized price |
| `short` | Normalized block LightGBM |
| `kind` | study arm |
| `codes` | CP-21: L-N (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-21 landing record, a study arm for attribution; never eligible for adoption |
| `comparator` | `v3` (v3, named by §17.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §17 (v21-r6); `cp21-adoption` |
| `sources` | `reports/block-challenger/metrics.csv`, `reports/block-challenger/uncertainty.csv`, `reports/block-challenger/criteria.csv`, `reports/block-challenger/adoption.json` |
| `claim_map` | `docs/track-b/research-content/cp21-claims.md` |
| `run_keys` | `cp21/L-N` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-21; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

Proposed code additions to existing entries (the saved references appear in CP-21 too): `v3` gains CP-21 HG; `v2` gains CP-21 H0; `naive` gains CP-21 B0; `v1` gains CP-21 B1; `daily-lear` gains CP-21 B2; `daily-lightgbm` gains CP-21 B3; `normalized-lear` gains CP-21 A1.

## 3. The claim map

`docs/track-b/research-content/cp21-claims.md` (SHA-256 `8df2e9a5c0edd160c4c0d6536c40eb1b0fee248db890a65da58abe4c3ec37c43`): every claim with its committed rows, the block-split finding (C111), the ladder B3 → pooled → block → HGL with the bundling in the first step disclosed (C106), and the withheld claims W22–W27 (W1–W21 stay in force). Status words come only through registry tokens.

## 4. The derived headline quantities (standard §3.3), computed inside the checkpoint

| Quantity | Value | From |
|---|---|---|
| (a) The pre-specified verdict | **met**: v4 | `reports/block-challenger/adoption.json` (`verdict`, `conditions`) |
| The rule, in words, with the date it was set | HGL becomes v4 only if both paired differences against v3 improve (the interval score's upper 95% endpoint below zero, the point error's at or below zero), it meets all six original screening diagnostics, the evaluation is complete and valid, and no fold is decisively worse; set **2026-09-29** | `capstone_v21.md` v21-r6 §17.6; `protocol.json` `adoption_rule_verbatim` (committed before scoring) |
| Distance from the rule's comparator (v3), in the rule's unit | ΔS_WIS −0.0266 (upper endpoint −0.0204, rule < 0); ΔS_MAE −0.0301 (upper endpoint −0.0228, rule ≤ 0) | `uncertainty.csv` L73, L72 |
| N: policies tested against the same rule up to this decision | 1 — HGL (the pooled and block study arms are never eligible under the rule) | `protocol.json` `adoption_rule`; §17.2 |
| "Point comparison" label needed? | no — both differences have 95% intervals | `uncertainty.csv` |
| (b) The change against v3, as a share of v3's score | S_MAE −5% (full precision -0.053206217463102945); S_WIS −5% (full precision -0.05006184586553608) | `uncertainty.csv` L72, L73 (`ratio`) |
| Its 95% interval | S_MAE [−6%, −4%]; S_WIS [−6%, −4%] — from CP-21's own bootstrap draws: seed 15042, 2,000 replicates, 7-calendar-day blocks, percentiles of `S_HGL,b / S_v3,b − 1` | `uncertainty.csv` L72, L73 (`ratio_ci_lower`, `ratio_ci_upper`); every draw in `replicates.parquet` |
| (c) Mean absolute error per period, EUR/MWh (HGL) | ordinary periods (folds 1, 2, 4, 5): 4.9 (fold 1) to 15.0 (fold 5); stress period, fold 3 (2022-07-01..09-28): 47.0 | `metrics.csv` per-fold rows L45–L49 |

## 5. Draft slot texts (standard §6)

Only the outcome the rule yields is drafted: the v4 chapter and its A3 transition. Tokens: `{g:<id>.<field>}` registry fields; `{r:<record>}` evidence records (rendered with the §3.4 precision rules). The §4 lint's code and status-word rules, applied to every draft: **0 findings**.

| Slot key | Draft |
|---|---|
| `v4.question` | Does adding a nonlinear, block-structured forecaster to {g:v3.name} improve both of its error scores? |
| `v4.change` | {g:v4.name} adds a three-block LightGBM forecaster, with the same inputs as {g:v3.name}, to its blend of two linear forecasts, and re-estimates the hour-aware intervals on the new forecast's own errors. |
| `v4.main_chart.headline` | Against {g:v3.name}, the point-error score changed by {r:cp21.ratio.HGL-HG.MAE} and the interval score by {r:cp21.ratio.HGL-HG.WIS}, each as a share of the comparator's score, with 95% intervals. |
| `v4.reading` | Both paired differences lie below zero, no test period is decisively worse, and the six screening diagnostics hold, so the rule set in advance adopted the change in research. |
| `v4.not_established` | Development evidence after selection, not a test on new data. It does not show that separate hour-block models help: block against pooled models showed no demonstrated joint preference. No single weather feature is isolated. |
| `v4.decision` | Adopted in research on {g:v4.status.date}; the released model is unchanged. |
| `v4.evidence` | the report, the review verdict, the claim map, the MLflow comparison |
| `transition.v3-v4.title` | From v3 to v4: adding a three-block LightGBM |
| `transition.v3-v4.result` | Against {g:v3.name}, both of its predecessor and its comparator, the point-error score changed by {r:cp21.ratio.HGL-HG.MAE} and the interval score by {r:cp21.ratio.HGL-HG.WIS}, in development tests. |

### 5a. The adopted transition (A3)

| Field | Value |
|---|---|
| Title | "From v3 to v4: adding a three-block LightGBM" |
| Predecessor and dates | `v3` (adopted in research 2026-09-24); v4 adoption date **pending-at-landing** |
| The change | model: a three-block LightGBM member added to the blend; the interval layer re-estimated on the new errors |
| The comparator set in advance | `v3`; it is also the predecessor, so one comparison serves both |
| The result, with its uncertainty and evidence class | S_MAE −5% [−6%, −4%], S_WIS −5% [−6%, −4%]; development |
| Against the predecessor | the comparator is the predecessor |
| What it does not establish | performance on new data; that separate hour-block models help (block against pooled: no demonstrated joint preference); the contribution of any single weather feature |
| The decision, dated, and the route | adopted in research, **pending-at-landing**; `#v4` and `compare:v4` |

### 5b. The released model's documentation (A4)

Not applicable: the released model does not change. v1 remains the released product and the demo; CP-21 is research only (§17.1, §17.6).

### 5c. The chart routes (A5)

| Chart | Its heading | The route's label | Where the route starts |
|---|---|---|---|
| v4 paired differences (both scores, 95% intervals) | `#v4` | v4 against v3 | the v4 chapter's "Explore these results" and the transition summary |

### 5d. Final-product transition / daily operation (A7/A8)

Not applicable: the trigger is unmet — no final-product designation, rollout or Live. The final-product designation does not change (§16).

## 6. The MLflow export

- **Draft export:** `reports/block-challenger/mlflow-export-draft/cp21.json` (SHA-256 `0f23d52dec3c3d4a413cfe15d959f8dd134d706d240d24f4d5889e0847ef5603`), built by `scripts/mlflow_export.py --draft cp21` from CP-21's committed rows and `draft-registry.json`: parent `cp21` and children `cp21/HGL`, `cp21/L-P`, `cp21/L-R`, `cp21/L-N`, experiment `delu-generations`. Pending fields: `checkpoint.evidence_sha`, `checkpoint.frozen_on`, `checkpoint.landing`, `evidence_ref`, `model_code_sha`, `original_completed_utc`, `statuses[].date`, `statuses[].source`.
- **Local tracking:** the same runs, names and tags in `.local/mlruns/cp21` (read-back equal; `reports/block-challenger/mlflow-local.json`). No upload, no network call; MLflow telemetry disabled.
- **Record-level diff against the last published export:** the published set is unchanged — `scripts/mlflow_export.py --diff-against ffcf9f3d10ad21db5db65f42e0c40653dbc05904` over 23 runs: only_identity True, identity changes on 0 runs, substantive changes none (`reports/block-challenger/published-export-diff.json`); `--check` passes. The publication block registers the entries, regenerates the final export and must show it equals this draft apart from the pending fields, with no previously published record changed.
- **Expected routes:** `experiment`; `compare:v4` — verified by REST and in Chromium and WebKit before it is linked, at publication.

## 7. Checks the checkpoint ran

- Re-derivation tests with negative controls: `tests/cp21/test_saved_evidence.py` (new-arm metrics from committed predictions, every interval from its stored replicates, the §17.6 verdict re-applied, byte-exact storage) and `tests/cp21/test_draft_export.py` (every exported value from a committed row; a changed row changes the draft; a renamed run is caught).
- The export contract: the draft matches its draft entries (`draft_problems`); the published export still matches the registry (`contract_problems`, `--check`).
- The §4 lint (code and status-word rules) on every draft slot text: 0 findings.
- Transition contract tests (`tests/test_43_publish_rules_migration.py`): to be extended by the publication block with the v4 transition.

## 8. Publication completion receipt — intended identities (publisher completes the rest)

| Surface | Intended identity | Action / unchanged rationale | Observed public identity and UTC time | Verification record and result | Outstanding action |
|---|---|---|---|---|---|
| GitHub source / README | the Owner's landing SHA and the publication commit; README glance and generation list naming v4 | push by the Owner | pending (publisher) | pending (publisher) | pending |
| GitHub Pages | rebuilt report with the v4 chapter, A3 transition and v4 headline (amber #B45309, filled diamond, "v4") | deploy on the Owner's instruction | pending (publisher) | pending (publisher) | pending |
| Public MLflow | regenerated `cp21.json` equal to this draft apart from pending fields; parent `cp21`, four children | authorized upload, then verification | pending (publisher) | pending (publisher) | pending |
| Hugging Face Space card | registry-derived model line; released model unchanged (v1) | deploy only if the card changes | pending (publisher) | pending (publisher) | pending |
| Hugging Face direct demo | v1 bundle unchanged | verified unchanged or redeployed with the same v1 artifact | pending (publisher) | pending (publisher) | pending |

- **Publication-to-MLflow mapping:** pending — the publication SHA, export identity and run references are filled by the publisher.
- **Final product and daily updates:** not applicable (no final-product designation).
- **Completion disposition:** incomplete by construction until the publication block; CP-21 publishes nothing.
- **Authority:** none exercised; every external action needs the Owner's instruction for that action.

