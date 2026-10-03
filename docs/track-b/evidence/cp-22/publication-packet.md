# CP-22 publication packet (draft)

**PUBLISH_RULES 1.3 §11; capstone v21-r9 §20.9; template `docs/track-b/publication-packet-template.md` (SHA-256 4efb0185…829cf).** Filled from inside CP-22. Numbers are never typed into a surface: each value names the committed row it comes from, and the evidence layer re-derives it. Identities that exist only at landing are marked **pending-at-landing**. Publication is PRES-4, after the Owner's landing, and only after the Owner's decision; nothing here is published.

Pinned rules: PUBLISH_RULES 1.3 `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4` (the hash the issued brief records), incorporating Publication Standard v1 `01d721c2…478cc` and presentation plan revision 3 `28119374…c812c`; all verified at the pre-run freeze (protocol `issued_and_inherited_sha256`).

## 1. Identity

| Item | Value |
|---|---|
| Checkpoint | CP-22, brief `docs/track-b/evidence/cp-22/issued-brief.md` at `563f64f3602848808ff11a7d74da8218b16d51846f34e90ad754c36ec2461fb3` |
| Governing research plan and version | `capstone_v21.md` v21-r9 §20 (SHA-256 `5fc9c686…09175`); rules `cp22-replacement`, `cp22-dynamic-layer`, `cp22-fast-component` |
| Evidence tag and tip | `evidence/cp-22` at **pending-at-landing** (the evidence tip SHA is in the CP-22 return), frozen **pending-at-landing** |
| Final reviewed candidate (model code) | recorded in the CP-22 checkpoint return; a commit cannot contain its own SHA |
| Report, review verdict, landing record | `reports/v4-revision/report.md`; `docs/track-b/evidence/cp-22/integration.md`; landing record **pending-at-landing** |

## 2. The draft registry entries (standard §5)

Machine-readable: `reports/v4-revision/draft-registry.json`, derived mechanically from `decisions.json` (replacement **none**). Statuses are dated at landing; CP-22 registers nothing.

### `pooled-lightgbm-member-for-v4` — branch

| Field | Value |
|---|---|
| `id` | pooled-lightgbm-member-for-v4 |
| `name` | Pooled LightGBM member for v4 |
| `subtitle` | The block split removed, under non-inferiority |
| `short` | Pooled member for v4 |
| `kind` | branch |
| `codes` | CP-22: CP-22 (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-22 landing record, cp22-replacement yielded no replacement: for R, condition 4 of rule cp22-replacement, no resolved per-fold degradation, was not met; for M, condition 4 of rule cp22-replacement, no resolved per-fold degradation, was not met; the Owner decides first (§20.6) |
| `comparator` | `v4` (named by §20.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §20 (v21-r9); `cp22-replacement` |
| `sources` | `reports/v4-revision/metrics.csv`, `reports/v4-revision/uncertainty.csv`, `reports/v4-revision/criteria.csv`, `reports/v4-revision/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp22-claims.md` |
| `run_keys` | `cp22` |
| `style`, `anchor` | branch; #branch-pooled-lightgbm-member-for-v4 |
| `checkpoint`, `after` | CP-22; v4 |
| `question`, `informed` | Can one pooled LightGBM member replace v4's three-block member without losing accuracy?; none recorded |
| `predecessor` | n/a |

### `v3-plus-pooled-normalized-lightgbm-averaged` — study arm

| Field | Value |
|---|---|
| `id` | v3-plus-pooled-normalized-lightgbm-averaged |
| `name` | v3 plus a capacity-averaged pooled LightGBM |
| `subtitle` | v3 with a normalized pooled LightGBM, capacities averaged |
| `short` | Pooled member, averaged |
| `kind` | study arm |
| `codes` | CP-22: R (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-22 landing record, condition 4 of rule cp22-replacement, no resolved per-fold degradation, was not met |
| `comparator` | `v4` (named by §20.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §20 (v21-r9); `cp22-replacement` |
| `sources` | `reports/v4-revision/metrics.csv`, `reports/v4-revision/uncertainty.csv`, `reports/v4-revision/criteria.csv`, `reports/v4-revision/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp22-claims.md` |
| `run_keys` | `cp22/R` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-22; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

### `v3-plus-pooled-lightgbm-pair` — study arm

| Field | Value |
|---|---|
| `id` | v3-plus-pooled-lightgbm-pair |
| `name` | v3 plus pooled normalized and raw LightGBM |
| `subtitle` | v4 with the block split removed |
| `short` | Pooled pair |
| `kind` | study arm |
| `codes` | CP-22: M (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-22 landing record, condition 4 of rule cp22-replacement, no resolved per-fold degradation, was not met |
| `comparator` | `v4` (named by §20.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §20 (v21-r9); `cp22-replacement` |
| `sources` | `reports/v4-revision/metrics.csv`, `reports/v4-revision/uncertainty.csv`, `reports/v4-revision/criteria.csv`, `reports/v4-revision/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp22-claims.md` |
| `run_keys` | `cp22/M` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-22; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

### `v3-plus-pooled-normalized-lightgbm-selected` — study arm

| Field | Value |
|---|---|
| `id` | v3-plus-pooled-normalized-lightgbm-selected |
| `name` | v3 plus a pooled normalized LightGBM |
| `subtitle` | The raw half dropped; daily capacity selection |
| `short` | Pooled normalized member |
| `kind` | study arm |
| `codes` | CP-22: A-PN-sel (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-22 landing record, a study arm for attribution; never eligible |
| `comparator` | `v4` (named by §20.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §20 (v21-r9); `cp22-replacement` |
| `sources` | `reports/v4-revision/metrics.csv`, `reports/v4-revision/uncertainty.csv`, `reports/v4-revision/criteria.csv`, `reports/v4-revision/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp22-claims.md` |
| `run_keys` | `cp22/A-PN-sel` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-22; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

### `v3-plus-pooled-raw-lightgbm` — study arm

| Field | Value |
|---|---|
| `id` | v3-plus-pooled-raw-lightgbm |
| `name` | v3 plus a pooled raw LightGBM |
| `subtitle` | v3 with the pooled raw LightGBM member |
| `short` | Pooled raw member |
| `kind` | study arm |
| `codes` | CP-22: A-LP (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-22 landing record, a study arm for attribution; never eligible |
| `comparator` | `v4` (named by §20.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §20 (v21-r9); `cp22-replacement` |
| `sources` | `reports/v4-revision/metrics.csv`, `reports/v4-revision/uncertainty.csv`, `reports/v4-revision/criteria.csv`, `reports/v4-revision/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp22-claims.md` |
| `run_keys` | `cp22/A-LP` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-22; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

### `v3-plus-normalized-block-lightgbm` — study arm

| Field | Value |
|---|---|
| `id` | v3-plus-normalized-block-lightgbm |
| `name` | v3 plus normalized block LightGBM |
| `subtitle` | v3 with the normalized three-block member |
| `short` | Normalized block member |
| `kind` | study arm |
| `codes` | CP-22: A-LN (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-22 landing record, a study arm for attribution; never eligible |
| `comparator` | `v4` (named by §20.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §20 (v21-r9); `cp22-replacement` |
| `sources` | `reports/v4-revision/metrics.csv`, `reports/v4-revision/uncertainty.csv`, `reports/v4-revision/criteria.csv`, `reports/v4-revision/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp22-claims.md` |
| `run_keys` | `cp22/A-LN` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-22; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

### `v4-with-dynamic-intervals` — study arm

| Field | Value |
|---|---|
| `id` | v4-with-dynamic-intervals |
| `name` | v4 with dynamic intervals |
| `subtitle` | Three-block v4 with the dynamic interval layer |
| `short` | v4 + dynamic layer |
| `kind` | study arm |
| `codes` | CP-22: v4+DL (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-22 landing record, a study arm for attribution; never eligible |
| `comparator` | `v4` (named by §20.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §20 (v21-r9); `cp22-replacement` |
| `sources` | `reports/v4-revision/metrics.csv`, `reports/v4-revision/uncertainty.csv`, `reports/v4-revision/criteria.csv`, `reports/v4-revision/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp22-claims.md` |
| `run_keys` | `cp22/v4+DL` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-22; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

### `v3-with-dynamic-intervals` — study arm

| Field | Value |
|---|---|
| `id` | v3-with-dynamic-intervals |
| `name` | v3 with dynamic intervals |
| `subtitle` | v3 with the dynamic interval layer |
| `short` | v3 + dynamic layer |
| `kind` | study arm |
| `codes` | CP-22: v3+DL (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-22 landing record, a study arm for attribution; never eligible |
| `comparator` | `v4` (named by §20.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §20 (v21-r9); `cp22-replacement` |
| `sources` | `reports/v4-revision/metrics.csv`, `reports/v4-revision/uncertainty.csv`, `reports/v4-revision/criteria.csv`, `reports/v4-revision/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp22-claims.md` |
| `run_keys` | `cp22/v3+DL` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-22; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

Proposed code additions to existing entries: `v4` gains CP-22 HGL; `v3` gains CP-22 HG; `v2` gains CP-22 H0; `naive` gains CP-22 B0; `v1` gains CP-22 B1; `daily-lear` gains CP-22 B2; `daily-lightgbm` gains CP-22 B3; `normalized-lear` gains CP-22 A1.

## 3. The claim map

`docs/track-b/research-content/cp22-claims.md` (SHA-256 `a9deb40982550d19535cad0d11e91b77eabe96d8a8f48d3c81fa11347e3c0a62`): every claim with its committed rows, the ladder, the replacement and layer findings, the Owner's investigation, and the withheld claims W28–W34 (W1–W27 stay in force).

## 4. The derived headline quantities (standard §3.3), computed inside the checkpoint

| Quantity | Value | From |
|---|---|---|
| (a) The pre-specified verdicts | `cp22-replacement`: **no replacement: CP-22 stops at its return and the Owner decides; three-block v4 stays current** (first unmet: R 4, M 4); `cp22-dynamic-layer`: **not applicable: no winner W**; `cp22-fast-component`: **not applicable: no winner W** | `reports/v4-revision/decisions.json` |
| The rules, in words, with the date they were set | R, then M, replaces v4's three-block construction only if neither paired score difference against v4 has a 95% interval entirely above zero, all six screening diagnostics hold, the evaluation is complete and valid, and no fold is decisively worse; the dynamic layer then replaces the winner's interval layer only if its interval-score gain's upper endpoint is below zero, its point error has no interval above zero, it meets the screen, its pooled 95% coverage is closer to 0.95 and no fold is decisively worse; the fast component is decided only as an add-on to an adopted dynamic layer. Set **2026-10-01** | `capstone_v21.md` v21-r9 §20.6; `protocol.json` `rules_verbatim` (committed before any fit) |
| Distance from v4 (the rule's comparator), in the rule's unit | R − v4: ΔS_MAE 0.0011 (lower endpoint −0.0031, rule: not above zero); ΔS_WIS 0.0010 (lower endpoint −0.0028) | `uncertainty.csv` L162, L163 |
| N: policies tested against the same rule up to this decision | two eligible policies in a fixed sequence (R, then M), plus two layer decisions in sequence (the dynamic layer, then its fast component); attribution arms are never eligible | `protocol.json` `rules`; §20.2 |
| "Point comparison" label needed? | no — every difference has a 95% interval | `uncertainty.csv` |
| (b) The change against v4, as a share of v4's score (R) | S_MAE +0.2% (full 0.0021328616777005482); S_WIS +0.2% (full 0.00198426700200538) | `uncertainty.csv` L162, L163 (`ratio`) |
| Its 95% interval | S_MAE [−0.6%, +1.0%]; S_WIS [−0.5%, +1.0%] — CP-22's own draws: seed 15042, 2,000 replicates, 7-calendar-day blocks | `uncertainty.csv` L162, L163; every draw in `replicates.parquet` |
| (b′) v4 (three-block), unchanged, against v3, for reference | S_MAE −5.3%, S_WIS −5.0% | `uncertainty.csv` L192, L193 |
| (c) Mean absolute error per period, EUR/MWh (R) | ordinary periods (folds 1, 2, 4, 5): 5.0 (fold 1) to 14.9 (fold 5); stress period, fold 3: 46.7 | `metrics.csv` per-fold rows |

## 5. Draft slot texts (standard §6)

Only the outcome the rules yield is drafted: a branch card after v4, for the Owner's decision; no revision and no transition. Tokens: `{g:<id>.<field>}` registry fields; `{r:<record>}` evidence records. The §4 lint's code and status-word rules, applied to every draft: **0 findings**.

| Slot key | Draft |
|---|---|
| `branch.pooled-lightgbm-member-for-v4.question` | {g:pooled-lightgbm-member-for-v4.question} |
| `branch.pooled-lightgbm-member-for-v4.comparator` | {g:v4.name} |
| `branch.pooled-lightgbm-member-for-v4.result` | Against {g:v4.name}, the averaged pooled forecaster changed the point-error score by {r:cp22.ratio.R-HGL.MAE} and the interval score by {r:cp22.ratio.R-HGL.WIS}, each as a share of the comparator's score, with 95% intervals. |
| `branch.pooled-lightgbm-member-for-v4.reason` | {g:pooled-lightgbm-member-for-v4.status.reason} |
| `branch.pooled-lightgbm-member-for-v4.decision` | Pending the Owner's decision; {g:v4.name} is unchanged until then. |
| `branch.pooled-lightgbm-member-for-v4.evidence` | the report, the review verdict, the claim map, the MLflow comparison |

### 5a. The adopted transition (A3)

Not applicable: no replacement, so v4 is unchanged and no revision or transition exists.

### 5b. The released model's documentation (A4)

Not applicable: the released model does not change. v1 remains the released product and the demo; CP-22 is research only (§20.6).

### 5c. The chart routes (A5)

None drafted: the branch card carries its deciding difference and interval in text; its reader route is the MLflow comparison `compare:pooled-lightgbm-member-for-v4`, advertised only after the authorized upload and both route checks.

### 5d. Final-product transition / daily operation (A7/A8)

Not applicable: the trigger is unmet — no final-product designation, rollout or Live (§16 unchanged).

## 6. The MLflow export

- **Draft export:** `reports/v4-revision/mlflow-export-draft/cp22.json` (SHA-256 `7810af06132e3807a5438d08529af77f73d01cc1ba5cc2d2078089d2f2b0d83a`), built by `scripts/mlflow_export.py --draft cp22` from CP-22's committed rows and `draft-registry.json`: parent `cp22` and one child per new policy (`cp22/R`, `cp22/M`, `cp22/A-PN-sel`, `cp22/A-LP`, `cp22/A-LN`, `cp22/v4+DL`, `cp22/v3+DL`), experiment `delu-generations`. Pending fields: `checkpoint.evidence_sha`, `checkpoint.frozen_on`, `checkpoint.landing`, `evidence_ref`, `model_code_sha`, `original_completed_utc`, `revisions[].adopted / superseded`, `statuses[].date`, `statuses[].source`.
- **Local tracking:** the same runs, names and tags in `.local/mlruns/cp22`, read back equal (`reports/v4-revision/mlflow-local.json`). No upload, no network call; MLflow telemetry disabled.
- **Record-level diff against the last published export:** the published set is unchanged — `scripts/mlflow_export.py --diff-against 940eb9846f3f1e891a0c585eb8e13089570b5ae9` over 28 runs: only_identity True, identity changes on 0 runs, substantive changes none (`reports/v4-revision/published-export-diff.json`); `--check` passes. 
- **Expected routes:** `experiment`; `compare:pooled-lightgbm-member-for-v4` — verified by REST and in Chromium and WebKit before it is linked, at publication.

## 7. Checks the checkpoint ran

- Re-derivation tests with negative controls: `tests/cp22/test_saved_evidence.py` (new-policy metrics from committed predictions, every interval from its stored replicates, the three verdicts re-applied, byte-exact storage) and `tests/cp22/test_draft_export.py` (every exported value from a committed row; a renamed run is caught; CP-21's draft and the published set unchanged).
- The export contract: the draft matches its draft entries (`draft_problems`); the published export still matches the registry (`--check`).
- The §4 lint (code and status-word rules) on every draft slot text: 0 findings.
- **Unavailable comparisons, with the reason:** (W+DL) − W, (W+ACI) − W, (W+DL) − (W+ACI) and (W+DLF) − (W+DL), and the shock-day comparison of W, W+DL and W+DLF, do not exist: `cp22-replacement` yielded no winner W, so the layer arms on W were not run (§20.6). The dynamic layer is reported on v4 and v3, descriptively.
- Transition contract tests (`tests/test_43_publish_rules_migration.py`): pass unchanged; not applicable (no transition).

## 8. Publication completion receipt — intended identities (publisher completes the rest)

| Surface | Intended identity | Action / unchanged rationale | Observed public identity and UTC time | Verification record and result | Outstanding action |
|---|---|---|---|---|---|
| GitHub source / README | after the Owner's decision | pending the Owner's decision | pending (publisher) | pending (publisher) | pending |
| GitHub Pages | after the Owner's decision; v4 unchanged meanwhile | pending the Owner's decision | pending (publisher) | pending (publisher) | pending |
| Public MLflow | regenerated `cp22.json` equal to this draft apart from pending fields | pending the Owner's decision | pending (publisher) | pending (publisher) | pending |
| Hugging Face Space card | unchanged | verified unchanged | pending (publisher) | pending (publisher) | pending |
| Hugging Face direct demo | v1 bundle unchanged | verified unchanged | pending (publisher) | pending (publisher) | pending |

- **Publication-to-MLflow mapping:** pending — filled by the publisher.
- **Final product and daily updates:** not applicable (no final-product designation).
- **Completion disposition:** incomplete by construction until PRES-4; CP-22 publishes nothing.
- **Authority:** none exercised; every external action needs the Owner's instruction for that action.

