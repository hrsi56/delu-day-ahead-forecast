# CP-23 publication packet (draft)

**PUBLISH_RULES 1.3 §11; capstone v21-r10 §21.9; template `docs/track-b/publication-packet-template.md` (SHA-256 4efb0185…829cf).** Filled from inside CP-23. Numbers are never typed into a surface: each value names the committed row it comes from, and the evidence layer re-derives it. Identities that exist only at landing are marked **pending-at-landing**. Publication follows the Owner's landing, as the next publication under PUBLISH_RULES 1.3, and only if the Owner decides to publish the branch; nothing here is published.

Pinned rules: PUBLISH_RULES 1.3 `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4`. The issued brief omitted the hash §21.9 says it records; the Owner ruled on 2026-10-04 to pin 1.3's single identity. It incorporates Publication Standard v1 `01d721c2…478cc` and presentation plan revision 3 `28119374…c812c`; all verified at the pre-run freeze (protocol `issued_and_inherited_sha256`).

## 1. Identity

| Item | Value |
|---|---|
| Checkpoint | CP-23, brief `docs/track-b/evidence/cp-23/issued-brief.md` at `33f6b41202586b2fc4f1d87624c5978e1fd5bde1185ac05271429bf719502d0c` |
| Governing research plan and version | `capstone_v21.md` v21-r10 §21 (SHA-256 `6873c250…f6709`); rule `cp23-adoption` |
| Evidence tag and tip | `evidence/cp-23` at **pending-at-landing** (the evidence tip SHA is in the CP-23 return), frozen **pending-at-landing** |
| Final reviewed candidate (model code) | recorded in the CP-23 checkpoint return; a commit cannot contain its own SHA |
| Report, review verdict, landing record | `reports/distribution-challenger/report.md`; `docs/track-b/evidence/cp-23/integration.md`; landing record **pending-at-landing** |

## 2. The draft registry entries (standard §5)

Machine-readable: `reports/distribution-challenger/draft-registry.json`, derived mechanically from `decisions.json` (adopted **False**, first unmet condition **1**). Statuses are dated at landing; CP-23 registers nothing.

### `ddnn-member-on-v4` — branch

| Field | Value |
|---|---|
| `id` | ddnn-member-on-v4 |
| `name` | DDNN member on v4 |
| `subtitle` | v4 plus a DDNN member, under rule cp23-adoption |
| `short` | DDNN member on v4 |
| `kind` | branch |
| `codes` | CP-23: v5 (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-23 landing record, condition 1 of rule cp23-adoption, a joint improvement over v4, with the upper 95% endpoint of the interval-score difference below zero and that of the point-error difference at or below zero, was not met |
| `comparator` | `v4` (named by §21.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §21 (v21-r10); `cp23-adoption` |
| `sources` | `reports/distribution-challenger/metrics.csv`, `reports/distribution-challenger/uncertainty.csv`, `reports/distribution-challenger/criteria.csv`, `reports/distribution-challenger/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp23-claims.md` |
| `run_keys` | `cp23`, `cp23/v5` |
| `style`, `anchor` | branch; #branch-ddnn-member-on-v4 |
| `checkpoint`, `after` | CP-23; v4 |
| `question`, `informed` | Does a distributional neural network, added to v4 as a one-third member, improve on v4 jointly in point and interval accuracy?; none recorded |
| `predecessor` | n/a |

### `ddnn-alone` — study arm

| Field | Value |
|---|---|
| `id` | ddnn-alone |
| `name` | DDNN alone |
| `subtitle` | A distributional neural network with a Johnson SU head, with its own quantiles |
| `short` | DDNN alone |
| `kind` | study arm |
| `codes` | CP-23: D (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-23 landing record, a study arm for attribution; never eligible |
| `comparator` | `v4` (named by §21.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §21 (v21-r10); `cp23-adoption` |
| `sources` | `reports/distribution-challenger/metrics.csv`, `reports/distribution-challenger/uncertainty.csv`, `reports/distribution-challenger/criteria.csv`, `reports/distribution-challenger/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp23-claims.md` |
| `run_keys` | `cp23/D` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-23; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

### `v3-plus-ddnn` — study arm

| Field | Value |
|---|---|
| `id` | v3-plus-ddnn |
| `name` | v3 plus a DDNN member |
| `subtitle` | DDNN as v3's third member, in LightGBM's place |
| `short` | v3 + DDNN |
| `kind` | study arm |
| `codes` | CP-23: v3+D (common-10747h) |
| `statuses` | not adopted, pending-at-landing, pending-at-landing: the CP-23 landing record, a study arm for attribution; never eligible |
| `comparator` | `v3` (named by §21.2 before results) |
| `population` | `common-10747h` |
| `evidence_class` | Development (`development_post_selection`) |
| `plan`, `rules` | capstone_v21.md §21 (v21-r10); `cp23-adoption` |
| `sources` | `reports/distribution-challenger/metrics.csv`, `reports/distribution-challenger/uncertainty.csv`, `reports/distribution-challenger/criteria.csv`, `reports/distribution-challenger/decisions.json` |
| `claim_map` | `docs/track-b/research-content/cp23-claims.md` |
| `run_keys` | `cp23/v3+D` |
| `style`, `anchor` | study; none (a study arm has no anchor of its own) |
| `checkpoint`, `after` | CP-23; n/a |
| `question`, `informed` | n/a; none recorded |
| `predecessor` | n/a |

Proposed code additions to existing entries: `v4` gains CP-23 HGL; `v3` gains CP-23 HG; `naive` gains CP-23 B0; `v1` gains CP-23 B1; `daily-lear` gains CP-23 B2; `daily-lightgbm` gains CP-23 B3; `normalized-lear` gains CP-23 A1.

## 3. The claim map

`docs/track-b/research-content/cp23-claims.md` (SHA-256 `5c12f47b7de9b279df9f5bb31344156a1461c37d873a2425034c9d2ea040a172`): every claim with its committed rows, the entry gates, the adoption decision, every §21.5 contrast and diagnostic, and the withheld claims W35–W41 (W1–W34 stay in force).

## 4. The derived headline quantities (standard §3.3), computed inside the checkpoint

| Quantity | Value | From |
|---|---|---|
| (a) The pre-specified verdict | `cp23-adoption`: **v5 is not adopted: CP-23 becomes the branch "DDNN member on v4"** (first unmet condition 1; unmet [1, 4]) | `reports/distribution-challenger/decisions.json` |
| The rule, in words, with the date it was set | v5 is adopted in research only if both paired score differences against v4 improve (the interval score's upper 95% endpoint below zero, the point error's at or below zero), it meets all six original screening diagnostics, the evaluation is complete and valid, and no fold is decisively worse. Set **2026-10-04** | `capstone_v21.md` v21-r10 §21.6; `protocol.json` `rule_verbatim` (committed before any main-run fit) |
| Distance from v4 (the rule's comparator), in the rule's unit | ΔS_MAE 0.0064 (upper endpoint 0.0149, rule: at or below zero); ΔS_WIS 0.0071 (upper endpoint 0.0138, rule: below zero) | `uncertainty.csv` L72, L73 |
| N: policies tested against the same rule up to this decision | one eligible candidate, v5; DDNN alone and v3 plus a DDNN member are never eligible | `protocol.json` `policies`; §21.2 |
| "Point comparison" label needed? | no — every difference has a 95% interval | `uncertainty.csv` |
| (b) The change against v4, as a share of v4's score | S_MAE +1.2% (full 0.012033436406928999); S_WIS +1.4% (full 0.014023740930373174) | `uncertainty.csv` L72, L73 (`ratio`) |
| Its 95% interval | S_MAE [−0.3%, +2.7%]; S_WIS [−0.2%, +2.7%] — CP-23's own draws: seed 15042, 2,000 replicates, 7-calendar-day blocks | `uncertainty.csv` L72, L73; every draw in `replicates.parquet` |
| (b′) v5 against v3, for reference | S_MAE −4.2%, S_WIS −3.7% | `uncertainty.csv` L74, L75 |
| (c) Mean absolute error per period, EUR/MWh (v5) | ordinary periods (folds 1, 2, 4, 5): 5.0 (fold 1) to 15.2 (fold 5); stress period, fold 3: 48.9 | `metrics.csv` per-fold rows |

## 5. Draft slot texts (standard §6)

Only the outcome the rule yields is drafted: a branch card after v4, published only if the Owner so decides; no generation and no transition. Tokens: `{g:<id>.<field>}` registry fields; `{r:<record>}` evidence records. The §4 lint's code and status-word rules, applied to every draft: **0 findings**.

| Slot key | Draft |
|---|---|
| `branch.ddnn-member-on-v4.question` | {g:ddnn-member-on-v4.question} |
| `branch.ddnn-member-on-v4.comparator` | {g:v4.name} |
| `branch.ddnn-member-on-v4.result` | Against {g:v4.name}, adding the distributional neural network as a one-third member changed the point-error score by {r:cp23.ratio.v5-HGL.MAE} and the interval score by {r:cp23.ratio.v5-HGL.WIS}, each as a share of the comparator's score, with 95% intervals. |
| `branch.ddnn-member-on-v4.reason` | {g:ddnn-member-on-v4.status.reason} |
| `branch.ddnn-member-on-v4.decision` | The Owner decides whether this branch is published; {g:v4.name} is unchanged. |
| `branch.ddnn-member-on-v4.evidence` | the report, the review verdict, the claim map, the MLflow comparison |

### 5a. The adopted transition (A3)

Not applicable: v5 is not adopted, so no generation or transition exists.

### 5b. The released model's documentation (A4)

Not applicable: the released model does not change. v1 is the released product and the demo; CP-23 is research only (§21.6).

### 5c. The chart routes (A5)

None drafted: the branch card carries its deciding difference and interval in text; its reader route is the MLflow comparison `compare:ddnn-member-on-v4`, advertised only after the authorized upload and both route checks.

### 5d. Final-product transition / daily operation (A7/A8)

Not applicable: the trigger is unmet — no final-product designation, rollout or Live (§16 unchanged).

## 6. The MLflow export

- **Draft export:** `reports/distribution-challenger/mlflow-export-draft/cp23.json` (SHA-256 `6c20b7e16e69dec9535189290b30d2f3465e1acab90ebff94ec3991437649f5f`), built by `scripts/mlflow_export.py --draft cp23` from CP-23's committed rows and `draft-registry.json`: parent `cp23` and one child per new policy (`cp23/v5`, `cp23/D`, `cp23/v3+D`), experiment `delu-generations`. Pending fields: `checkpoint.evidence_sha`, `checkpoint.frozen_on`, `checkpoint.landing`, `evidence_ref`, `model_code_sha`, `original_completed_utc`, `statuses[].date`, `statuses[].source`.
- **Local tracking:** the same runs, names and tags in `.local/mlruns/cp23`, read back equal (`reports/distribution-challenger/mlflow-local.json`). No upload, no network call; MLflow telemetry disabled.
- **Record-level diff against the last published export:** the published set is unchanged — `scripts/mlflow_export.py --diff-against a4acd792954c577e60235c427380c82031c4372a` over 28 runs: only_identity True, identity changes on 0 runs, substantive changes none (`reports/distribution-challenger/published-export-diff.json`); `--check` passes.
- **Expected routes:** `experiment`; `compare:ddnn-member-on-v4` — verified by REST and in Chromium and WebKit before it is linked, at publication.

## 7. Checks the checkpoint ran

- Re-derivation tests with negative controls: `tests/cp23/test_saved_evidence.py` (new-policy metrics from committed predictions, every interval from its stored replicates, the rule re-applied, byte-exact storage) and `tests/cp23/test_draft_export.py` (every exported value from a committed row; a renamed run is caught; the earlier drafts and the published set unchanged).
- The export contract: the draft matches its draft entries (`draft_problems`); the published export still matches the registry (`--check`).
- The §4 lint (code and status-word rules) on every draft slot text: 0 findings.
- Transition contract tests (`tests/test_43_publish_rules_migration.py`): pass unchanged; not applicable (no transition).

## 8. Publication completion receipt — intended identities (publisher completes the rest)

| Surface | Intended identity | Action / unchanged rationale | Observed public identity and UTC time | Verification record and result | Outstanding action |
|---|---|---|---|---|---|
| GitHub source / README | after the Owner's decision on the branch | pending the Owner's decision | pending (publisher) | pending (publisher) | pending |
| GitHub Pages | after the Owner's decision; v4 unchanged meanwhile | pending the Owner's decision | pending (publisher) | pending (publisher) | pending |
| Public MLflow | regenerated `cp23.json` equal to this draft apart from pending fields | pending the Owner's decision | pending (publisher) | pending (publisher) | pending |
| Hugging Face Space card | unchanged | verified unchanged | pending (publisher) | pending (publisher) | pending |
| Hugging Face direct demo | v1 bundle unchanged | verified unchanged | pending (publisher) | pending (publisher) | pending |

- **Publication-to-MLflow mapping:** pending — filled by the publisher.
- **Final product and daily updates:** not applicable (no final-product designation).
- **Completion disposition:** incomplete by construction until the publication; CP-23 publishes nothing.
- **Authority:** none exercised; every external action needs the Owner's instruction for that action.

