# PRES-4 publication packet

**PUBLISH_RULES 1.4 §11; the brief `docs/track-b/evidence/pres-4/issued-brief.md` (SHA-256
`54169c7c998958e850d451bf5c766dddbd559721f1920370020035e3bae57bdd`); the packet template
`docs/track-b/publication-packet-template.md` (SHA-256 `4049c3e1f695034ec45fa185d465fce05ab1183cbded72188306579d7287d01a`).**
This packet completes CP-24's draft packet (`docs/track-b/evidence/cp-24/publication-packet.md`, `62729107…6be`) into
PRES-4's, with the branch entries of CP-22's (`evidence/cp-22/publication-packet.md`, `f05dfb86…219`) and CP-23's
(`evidence/cp-23/publication-packet.md`, `e0eba441…ce49`). Every value below names the committed row it comes from; the
evidence layer re-derives it and the page renders it from the record. Identities that exist only after the review, the
final build or the Owner's steps are named `<…>` and filled in the return and by the Owner's receipt (§8).

## 1. Identity

| Item | Value |
|---|---|
| Publication block | PRES-4, brief `docs/track-b/evidence/pres-4/issued-brief.md` at `54169c7c…57bdd`, issued 2026-10-11 |
| Publication anchor | `docs/PUBLISH_RULES.md` revision 1.4, `ccfe6199535dc104250ee1ed1d8ff57bf0b12fbfb4945a3521e2e29fad479a80`; incorporating Publication Standard v1 `7bb90c4c…b68c` and the presentation plan `b04a0bb1…e19c` |
| Research constraint anchor (read-only) | `capstone_v21.md` v21-r12, `caf03d705a785369972b6e9ef3d043815a4a7ba77830cabb51e939c486477ce4`; CP-24 ran under v21-r11 (`evidence/cp-24:capstone_v21.md`, `11068e3f…ed2d2`); §23.12, §20.13, §21.9 |
| Checkpoints published | CP-24 (v5) — rule `cp24-adoption`; CP-22 (branch "Pooled LightGBM member for v4") — `cp22-replacement`; CP-23 (branch "DDNN member on v4") — `cp23-adoption` |
| Evidence tags and tips | `evidence/cp-24` at `05b7e618de8de2f3f59c3e62aaf1664807bf397e` (2026-10-10); `evidence/cp-23` at `928bc1389627499fba14222e552feb62492f6e2d` (2026-10-04); `evidence/cp-22` at `8daf7d0775404611e9f7ef4844fc602f1aa67b26` (2026-10-04) — `registry.py::EVIDENCE_TAGS` |
| Final reviewed candidates (model code) | CP-24 `7949a98f80c81c5a789dd69c213da16c811d345c`; CP-23 `f9a737eb2bb8ccdb93c0de5cf1449630ee246e90`; CP-22 `29d8d383a8870fee10b04158c5e3e5fd89514fdc` (each checkpoint's return; `mlflow_export.py::CHECKPOINTS`) |
| Reports, verdicts, landing records | `reports/ddnn2/report.md`, `docs/track-b/evidence/cp-24/integration.md` (`b112a2ca…304a`), `docs/track-b/cp-24-landing-2026-10-11.md` (`4b37b337…c6ca4`, the source of v5's adoption); `reports/distribution-challenger/report.md`, `evidence/cp-23/integration.md`, `cp-23-landing-2026-10-04.md` (`a860780a…7d`); `reports/v4-revision/report.md`, `evidence/cp-22/integration.md`, `cp-22-landing-2026-10-04.md` (`a999acb7…600`) |
| This block's candidate and evidence tip | `<final_candidate_sha>` and `<evidence_tip_sha>` on `gauntlet/pres-4`, off `main` `e398a30bb53ecd4c397aad0f34fd122d42e74553` |

## 2. The registry entries, as entered (standard §5; runbook §2 steps 1–6 and §3 steps 1–3)

**v5 and its study arms (CP-24).** Entered as `reports/ddnn2/draft-registry.json` (`7d25bdca…70ee`) drafts them, with two
changes the brief names: v5's name is the Owner's, **"v5 · DDNN-2 added"** (the draft's "v5 · DDNN-2 member added" is
nowhere on a surface), and every status is dated **2026-10-11** with the CP-24 landing record as its source.

| Entry | Kind | Codes | Status | Comparator | Other fields |
|---|---|---|---|---|---|
| `v5` — v5 · DDNN-2 added | generation | CP-24 `v5` (scored attempt 1) | adopted in research, 2026-10-11, CP-24 landing record | `v4` | predecessor `v4`; style `v5`; anchor `#v5`; rule `cp24-adoption`; sources the four attempt-1 files; claim map `cp24-claims.md`; run keys `cp24`, `cp24/v5` |
| `ddnn2-alone` — DDNN-2 alone | study arm | CP-24 `D2` | not adopted, 2026-10-11 — "a study arm for attribution; never eligible" | `v4` | style `study`; run key `cp24/D2` |
| `v3-plus-ddnn2` — v3 plus a DDNN-2 member | study arm | CP-24 `v3+D2` | not adopted, 2026-10-11 — the same | `v3` | run key `cp24/v3+D2` |

**CP-22 and CP-23 as branches (runbook §3).** Entered from `reports/v4-revision/draft-registry.json` and
`reports/distribution-challenger/draft-registry.json` as drafted, with their statuses dated 2026-10-04 and sourced from
their landing records. Two recorded departures: CP-22's branch reason drops its pending clause ("the Owner decides
first (§20.6)"), which the landing record resolved ("v4 נשאר כפי שהוא": "the Owner kept v4 unchanged"); and CP-23's
"DDNN alone" subtitle is shortened from thirteen words to the registry's eight-word field ("A distributional neural
network with its own quantiles"; A-PRES4-4). Every other field is the draft's (`tests/test_49` checks each field).

| Entry | Kind | Codes | Status (2026-10-04, landing record) | Comparator |
|---|---|---|---|---|
| `pooled-lightgbm-member-for-v4` — Pooled LightGBM member for v4 | branch, after v4 | CP-22 `CP-22` | not adopted — cp22-replacement yielded no replacement: for R and for M, condition 4, no resolved per-fold degradation, was not met; the Owner kept v4 unchanged | `v4` |
| R — v3 plus a capacity-averaged pooled LightGBM; M — v3 plus pooled normalized and raw LightGBM | study arms | CP-22 `R`, `M` | not adopted — condition 4 not met | `v4` |
| A-PN-sel, A-LP, A-LN, v4+DL, v3+DL (five more) | study arms | CP-22 | not adopted — a study arm for attribution; never eligible | `v4` |
| `ddnn-member-on-v4` — DDNN member on v4 | branch, after v4 | CP-23 `v5` | not adopted — condition 1, a joint improvement over v4, was not met | `v4` |
| `ddnn-alone` — DDNN alone; `v3-plus-ddnn` — v3 plus a DDNN member | study arms | CP-23 `D`, `v3+D` | not adopted — never eligible | `v4`; `v3` |

**The code additions to existing entries.** Every addition of the three drafts is entered (v4 `HGL`, v3 `HG`, v1 `B1`,
the naive `B0`, daily LEAR `B2`, daily LightGBM `B3`, normalized LEAR `A1` in CP-22/23/24; v2 `H0` in CP-22; CP-23's
DDNN alone `D` in CP-24). None changes a previously published MLflow record: a run's name reads only its own
experiment's code, and the record-level diff against the published set finds no change (§6). None was left out.

**Experiment codes are scoped.** CP-23's candidate and CP-24's v5 share the code text `v5`. The registry now resolves a
code inside its experiment (`registry.py::by_code(code, experiment)`), refuses an unscoped lookup of a shared text, and
the lint treats `v5` as the public version label (A-PRES4-3).

**The lists.** `CHECKPOINTS` gains CP-22, CP-23 and CP-24 (run key, owner, evidence tag and SHA, freeze date, report,
verdict, landing record, children); `EVIDENCE_TAGS` gains the three tags with each tip's commit date; `RULES` gains
`cp22-replacement`, `cp22-dynamic-layer` and `cp22-fast-component` (set 2026-10-01), `cp23-adoption` (2026-10-04) and
`cp24-adoption` (2026-10-05); `COMPARISON_ORDER` puts v5 first. `CRISIS_ORDER` is unchanged: v4's chapter keeps its
peak chart, and v5's states its peak in text.

## 3. The claim maps

Registered in `research_claims.py::CLAIM_MAPS`: `cp22-claims.md` (`a9deb409…c0a62`), `cp23-claims.md` (`5c12f47b…a172`),
`cp24-claims.md` (`918a71f2…f774`). The publication's own wording is P53–P59 in `publication-claims.md`: the v5 headline
(P53), the coverage limits (P54), the v4 → v5 transition (P55), the branch cards (P56), the comparison after v5 (P57),
the planned list (P58), and v5's peak and intervals, descriptive (P59). Withheld claims stay withheld: W1–W48 in force; the lint's guards gain CP-24's W42–W47
(`research_claims.py::WITHHELD_PATTERNS`, each with a negative control in `tests/test_49`).

## 4. The derived headline quantities (standard §3.3), re-derived from committed rows

| Quantity | Value | From |
|---|---|---|
| (a) The pre-specified verdict | `cp24-adoption`: **met** — all five conditions; the committed candidate `v5` adopted (`derived.adoption.v5.verdict`) | `reports/ddnn2/attempt-1/decisions.json` `adoption` (conditions 1–5 met; `adopted` true; `candidate` `v5`) |
| The rule, in words, with its date | Against v4: both paired differences improve at the attempts-adjusted 97.5% level (interval score's upper endpoint below zero, point error's at or below zero); the six original screening diagnostics; a complete, valid evaluation; no fold decisively worse; both point estimates improve v4 by at least 0.5%. Set **2026-10-05** (`derived.adoption.v5.set_on`) | `capstone_v21.md` §23.9 "Pre-registered rule `cp24-adoption`, set 2026-10-05", quoted verbatim by `protocol.json` `rule_verbatim` |
| Distance from v4, in the rule's unit, at the decision level | ΔS_MAE −0.0133 [−0.0166, −0.0091]; ΔS_WIS −0.0119 [−0.0147, −0.0084] (97.5%) | `uncertainty.csv` L112, L113 (`ci97.5_lower`, `ci97.5_upper`), equal to `decisions.json` condition 1 |
| The same at 95% | [−0.0161, −0.0096]; [−0.0143, −0.0087] | `uncertainty.csv` L112, L113 (`ci_lower`, `ci_upper`) |
| N | 1 eligible policy, `v5`; DDNN-2 alone and v3 + DDNN-2 never eligible (`derived.adoption.v5.tested`) | `decisions.json` `adoption.candidate` |
| "Point comparison" label needed? | no — every difference has an interval | — |
| (b) The change against v4, as a share of v4's score | S_MAE −2% (exact −2.4899%); S_WIS −2% (−2.3561%) | `uncertainty.csv` L112, L113 `ratio` = `ratio-intervals.csv` L2, L3 |
| Its 95% interval | S_MAE [−3%, −2%] (−2.9585%, −1.7939%); S_WIS [−3%, −2%] (−2.7787%, −1.7145%) — CP-24's own draws: seed 15042, 2,000 replicates, 7-day blocks (`decisions.json` `bootstrap`) | `uncertainty.csv` `ratio_ci_lower`/`ratio_ci_upper`, equal to `ratio-intervals.csv` `ratio_ci95_*` |
| Its 97.5% interval, the decision level | S_MAE [−3%, −2%] (−3.0368%, −1.6823%); S_WIS [−3%, −2%] (−2.8593%, −1.6208%) — the same stored draws (`derived.change_decision.v5.*`) | `ratio-intervals.csv` L2, L3 `ratio_ci97.5_*` |
| (c) MAE per period, EUR/MWh (v5) | ordinary periods 4.8–14.4; stress period, fold 3, 45.5 (v4 47.0) (`derived.periods.v5.*`) | `metrics.csv` per-fold rows; the stress period from `reports/cp10/protocol.json` and the anchor |
| The coverage limits | 448 scored days of the 2,654 days in the data from 2019-01-01 to 2026-04-07; 0 in October to December; 1 winter (`derived.coverage.*`) | `metrics.csv` B0 pooled `represented_dates`; `data/source_manifest.json` (first price hour, no missing hour); `data/partitions.json` `eda_cutoff` |
| The targets' census (criteria 1–2) | 25 identities tested, by decision date; v3 the first to meet both; 16 later policies met them, among them v4 and v5 (`derived.criteria.*`) | the criteria rows of CP-15 to CP-24 |

**The branches' deciding results, in each rule's unit (95%).**

| Branch | Deciding result | From |
|---|---|---|
| Pooled LightGBM member for v4 | over the five folds no 95% interval wholly above zero — R ΔS_MAE +0.0011 [−0.0031, +0.0054], ΔS_WIS +0.0010 [−0.0028, +0.0049]; M −0.0013 [−0.0036, +0.0016], −0.0008 [−0.0030, +0.0022] — but fold 4 decisively worse for both: R +0.31 [+0.15, +0.42], M +0.20 [+0.05, +0.33] EUR/MWh in MAE | `reports/v4-revision/uncertainty.csv` L162–L165, L98, L100 |
| DDNN member on v4 | ΔS_MAE +0.0064 [−0.0016, +0.0149], ΔS_WIS +0.0071 [−0.0009, +0.0138]: the required improvement not shown; fold 3 decisively worse, +1.92 [+0.30, +4.39] EUR/MWh in MAE | `reports/distribution-challenger/uncertainty.csv` L72, L73, L30 |

## 5. Slot texts, as published (standard §6)

Rendered from `research_claims.py`; every number is a record. The §4 lint (`make lint-publication`): 0 findings.

| Slot | Block | Claim |
|---|---|---|
| The question | `v5.question` | C403 |
| The change, with its diagram | `v5.change`; `build_pages.py::ddnn_change` | C403 |
| The main chart and its headline | `v5-c2a`: v5 − v4 on both scores, each at 95% and at the 97.5% decision level (four rows); `v5.chart_headline` | C420 |
| The reading | `v5.reading` | C421 |
| Not established (three) | `v5.caveat.coverage` (P54), `v5.caveat.class` (C449), `v5.caveat.alone` (C427) | — |
| The decision, dated | `v5.decision` | C422 |
| The evidence row | `compare:v5` (once verified), the review verdict, the engineering report and the raw rows at `evidence/cp-24` | — |
| Details | method (`v5.method.blend`, `v5.method.network`, `v5.method.arms`); per-period consistency (`v5.folds` and its value table, `v5.absolute`); stress period (`v5.peak`); coverage and width (`v5.coverage`); protocol and review (`v5.rule`, `v5.criteria`, `v5.controls`, `v5.leakage`) | C403, C429, C421, C435, C433, C401, C434, C439, C441 |

**The branch cards** (runbook §3; `build_pages.py::branch_card`, attached by `lineage` under "Experiments not adopted
between v4 and v5"): `branch.<id>.question` (P56, naming v4 as the comparator), `.result` (C208 / C308), `.reason`
(C212 / C310), the dated "Not adopted · October 2026", and the evidence row (the report and the verdict at each
evidence tag, and `compare:<id>` once verified).

### 5a. The adopted transition (A3)

| Field | Value |
|---|---|
| Title | `transition.v4-v5.title`: "From v4 to v5: adding a distributional neural network" |
| Predecessor and dates | v4 · three-block LightGBM added, adopted in research in September 2026; v5 adopted 2026-10-11 |
| The change | `transition.v4-v5.change` |
| The comparator set in advance | v4 itself, which is the predecessor (`comparator_is_predecessor`); no separate predecessor row |
| The result | `transition.v4-v5.result`: the ratio at 95% and at 97.5%; development evidence after selection |
| What it does not establish | `transition.v4-v5.limits`: the coverage limits and the evidence class |
| The decision and the route | `v5.decision`; "The comparison chart and its evidence, in the v5 chapter" → `#v5-chart-title` |

### 5b. The released model's documentation (A4)

Not applicable: the released model does not change. v1 is the released product and the demo; the product section is
byte-identical to the published page.

### 5c. The chart routes (A5)

| Chart | Its heading | The route | Where it starts |
|---|---|---|---|
| `v5-c2a` (main) | `#v5-chart-title` | "The comparison chart and its evidence, in the v5 chapter" | the v4 → v5 transition card |
| (text and tables) | `#v5-arms`, `#v5-per-period-differences`, `#v5-absolute-errors`, `#v5-peak`, `#v5-coverage` | each heading's own words | v5's "Explore these results" |
| `overview` | `#comparison-finding` | "Compare model results" | the opening |

The v5 chapter draws one chart; its other results are text and value tables, to fit the 2.0 MB budget (A-PRES4-5).

### 5d. Final-product transition / daily operation (A7/A8/A9)

Not applicable: no final-product designation, rollout or live panel.

## 6. The MLflow export

| File | SHA-256 | Runs |
|---|---|---|
| `reports/presentation/mlflow-export/cp24.json` | `d55cf3de8834fb1677ced747019881f8620316ba77074d09d7a3b83f0bce2911` | `cp24` and `cp24/v5`, `cp24/D2`, `cp24/v3+D2` |
| `cp23.json` | `413ebf56f826a33a88f445cdfe1bd52433286d8d0a65c3b46970c52ff697eac0` | `cp23` and `cp23/v5`, `cp23/D`, `cp23/v3+D` |
| `cp22.json` | `4be85b847a3451a691221d5cc5d8b28d8976aa9af4799be23c47668633959359` | `cp22` and its seven children |
| `manifest.json` | `af680390f6244e318f1cf5e218ca380a7992eb3809e5f32ed69d5d838e19ae1d` | 44 runs: 8 parents, 36 children |
| `cp10`, `cp15`, `cp16`, `cp20`, `cp21` | unchanged bytes (`git diff e398a30` empty on each) | the 28 published runs |

- **Built** by the drafts' own code paths with the registry's entries (`mlflow_export.py::tracked_runs`,
  `_later_tracked_runs`; CP-24's by `cp24.export`'s functions, imported unchanged).
- **Against the drafts** (`mlflow_export.py::later_final_vs_draft`; `pres-4-export-final-vs-draft.json`): each equals its
  draft apart from the pending fields (`delu.status`, `delu.evidence_ref`, `delu.model_code_sha`,
  `delu.original_completed_utc`, `mlflow.note.content`, and the README's pending lines). `cp24.json` also carries the
  Owner's name on `cp24` and `cp24/v5` (run name, `delu.public_name`, description, `summary.json`, `README.md`, and
  nothing else), and v5's two charts on `cp24/v5` (`charts/overview.svg`, `charts/v5-c2a.svg`).
- **Against the published set** (`--diff-against e398a30`; `pres-4-export-diff.json`): 28 → 44 runs; the 16 new runs
  added; no identity or substantive change to any published run (`cp21/HGL`'s overview chart is pinned to v4's
  comparison, `build_pages.py::PINNED_CHARTS`); the one experiment-tag change is `mlflow.note.content` (A-PRES3-1).
- **The routes** the registry expects: `experiment`; `compare:overview` (twelve runs, from `cp24/v5` to `cp15/B0`);
  `compare:v5` (`cp24/v5`, `cp24/D2`, `cp24/v3+D2`, `cp21/HGL`); `compare:pooled-lightgbm-member-for-v4` (CP-22's seven);
  `compare:ddnn-member-on-v4` (CP-23's three). Each is linked only once the index covers it.
- **The upload, only after the independent check's PASS** (runbook §1 step 5; the brief's one authorized external
  action). First the authenticated read-only gate, then the bounded upload; the DagsHub variables are read inside the
  process only, and the publisher's outbound credential-value scan runs before the first request:

  ```bash
  MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true uv run python scripts/mlflow_publish.py --precheck
  ```

  ```bash
  MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true uv run python scripts/mlflow_publish.py --target public --owner-instruction "<the brief's authorization, verbatim, with the PASS's SHA and date>" --authorized-runs cp22,cp22/A-LN,cp22/A-LP,cp22/A-PN-sel,cp22/M,cp22/R,cp22/v3+DL,cp22/v4+DL,cp23,cp23/D,cp23/v3+D,cp23/v5,cp24,cp24/D2,cp24/v3+D2,cp24/v5 --authorized-experiment-tags mlflow.note.content --log reports/presentation/release-checks/pres-4-mlflow-upload.json
  ```

  It refuses before the first write unless every write belongs to those sixteen runs or to the one experiment tag.
  Then `verify_mlflow_mirror.py verify --target public` (`pres-4-public-mirror.json`), `check_reader_paths.py
  mlflow-routes` (`pres-4-public-mlflow-routes.json`), `verify_mlflow_mirror.py index`, and the `--final` build.
- **Frozen files.** `scripts/mlflow_export.py` is bound by CP-21's, CP-22's and CP-23's artifact manifests. Its change is
  recorded as PRES-3 recorded CP-21's: `tests/cp23/test_saved_evidence.py::AMENDED_BY_PUBLICATION` (with the draft-export
  and saved-evidence tests), the same record in `tests/cp22/test_saved_evidence.py`, each with a test that the amended
  files keep their reviewed bytes at the evidence tag, and each draft-export test's post-publication invariant. CP-24's
  draft-export test skips by design. No artifact manifest is edited.

## 7. Checks run

Records under `reports/presentation/release-checks/` unless a path says otherwise. First failures and superseded runs
are kept beside their retries. A check run on `2064fb6e7c01e662332a5401a2e86344e24d1b1c` covered a tree that differs
from the candidate only in this packet and the records that the next commit adds. The candidate follows Integration
review 1's FAIL at `a852c0a` and its repair, `1cae93f` (below).

| Check (runbook §9; brief "Reviews and evidence") | Record | Result |
|---|---|---|
| The offline checks, `scripts/prerelease.py --stage pre-final` from a clean tree: the browser payload; pytest on Python 3.13; a clean Python 3.12 run of every CI step (`uv sync --locked --dev`, the payload, pytest, the CQR fixture, cross-surface agreement, the WASM equivalence); `make verify`; `make lint-publication`; the rebuild and `git status`; links; the publication guard | `pres-4-pre-final-prerelease.json` (at `2064fb6`; raw output local only, `.local/artifacts/prerelease/pres-4-pre-final/`) | **PASS**, 2026-10-11 11:34–11:45 UTC, every check as expected: the payload on 3.13; pytest on 3.13.15, 1,658 passed, 8 skipped by design; on 3.12.14, `uv sync --locked --dev`, the payload, pytest (1,658 passed, 8 skipped), the CQR fixture (8 passed), cross-surface agreement, the WASM equivalence (15 passed); `make verify`; `make lint-publication`; the rebuild with 0 changed paths; links (46, none failed); the publication guard exiting 1 as expected before the `--final` build |
| — its earlier attempts | attempt 1 (stopped after four steps because the tree changed under it; logs only, kept locally at `.local/artifacts/pres-4/prerelease-attempt-1-aborted/`); `pres-4-pre-final-prerelease-attempt-2.json` (at `db65a46`: every check as expected except links, which met 26 GitHub `blob` 503s); `pres-4-pre-final-prerelease-attempt-3.json` (at `b0ed155`: PASS, 1,652 passed and 8 skipped on each Python; the candidate Integration review 1 failed) | superseded by attempt 4 |
| Links (`check_links.py`), unauthenticated | `pres-4-links-attempt-1.json` (the first failure: GitHub 503s); `pres-4-links-attempt-2.json` = `pres-4-links.json` (after a 30-minute pause); `reports/cp3/link_check.json`, the prerelease's own run at `2064fb6` | 46 links, no failed destination; the four gated DagsHub UI paths redirect to login, as controls. Against the published page, the link set changes only where v5 replaces v4 at the top of the page and the branch cards add their reports and verdicts; the v4 chapter keeps its links |
| `make verify`; `make lint-publication` | inside the prerelease record | PASS; page, README and templates 0 findings |
| `make publication-guard` | inside the prerelease record | BLOCKED, by design, until the `--final` build: `reports/cp3/pages_build.json` is a non-final build record |
| Determinism: `rebuild_presentation.py`, then `git status` | inside the prerelease record | every generated surface equals its committed bytes |
| The page budget | `reports/cp3/pages_build.json` | 1,994,385 bytes ≤ 2,000,000 (5,615 to spare), without compaction; v2 and v3 sections byte-identical (`tests/test_45`, `tests/test_49`) |
| The §10 release checks and the placements, Chrome 154.0.8037.98 and WebKit 26.6, at 1440 × 900, 768 × 1024, 390 × 844, 360 × 780, 320 × 640 and the emulated iPhone 393 × 659 | `pres-4-local-release.json` (attempt 4, at `1cae93f`, the page `1512deee…`, the candidate's) | passed: the headline block ends at 800.6 / 801.3 px (desktop) and 628.6 / 628.7 px (phone); the finding at 1,727.6 / 1,728.3 px (A2 limit 1,744) and 2,402.5 px (limit 2,420); chart text at least 12.21 px (320 px), 14.58 px (390 px) and 12.38 px (1440 px), with every disclosure open as well; no chart overlap or clipping, no collapsed space, no horizontal overflow; no console error, failed request, HTTP error or resource after the document; accessibility trees, keyboard, touch targets at 390 px, contrast, 200% zoom and 320 px reflow, in both engines |
| — its earlier attempts | `pres-4-local-release-attempt-1.json` (failed: the phone finding at 2,443.5 px, beyond A2's 2,420; the per-period route reached a table inside a closed disclosure); `-attempt-2.json` (passed, but the editorial repairs changed the page during the run); `-attempt-3.json` (passed, at `db65a46`, the page `e22525a9…`, the fresh reader's screens; the same placements as attempt 4) | superseded by attempt 4 |
| A5 discovery, from the closed default page, by mouse, keyboard and deep link | inside the release record | 40 routes in each engine at both placement sizes |
| The demo: cold start and controls; accessibility and keyboard; startup states (the bundle served locally on 127.0.0.1) | `pres-4-local-demo.json`, `pres-4-local-demo-a11y.json`, `pres-4-local-states.json` | ready in 10.1–11.7 s, 0 console errors, 0 failed requests; every control named, no target under 44 px, keyboard operation of the slider, the level and the menu; loading, failure and retry |
| The Space unchanged | `pres-4-space-unchanged.json` (at `db65a46`); `pres-4-space-check.json`; `make wasm` again at `2064fb6` (the bundle `9028a118…`, its 805 files equal to the reviewed copy; no tracked file changed) | `make wasm` rebuilds bundle `9028a118…` (805 files, 44,164,910 bytes), equal file by file to the reviewed copy; both cards byte-identical to `e398a30` (`745bbb93…`, `c92a2666…`); the bitwise-equivalence gate at deviation 0.0 with its three positive controls breaking it; `make wasm` changes no tracked file. Read-only check mode: the served Space, revision `0331088725fedab2f5a1ec804ae03bf960cf126f`, equals the bundle; nothing to add, change or delete; nothing written |
| The export | `pres-4-export-diff.json`, `pres-4-export-final-vs-draft.json` | `--check` current; runs 28 → 44, the 16 of cp22, cp23 and cp24 added, `only_identity` true, no identity or substantive change, the one experiment-tag change `mlflow.note.content`; each later export equals its draft apart from its pending fields (cp24 also the Owner's name and v5's two charts); `--draft cp22 --check` and `--draft cp23 --check` current |
| The publisher, dry run (no `--target`) | the run's output, local | 44 runs, 16,753 metric points, 107 artifacts in the plan; the outbound credential-value scan clean; nothing written |
| The value-based secret scan | `scripts/secret_guard.py` | the pre-commit and commit-msg hooks on every commit; an explicit pre-commit scan before each evidence commit; the pre-push scan over `gauntlet/pres-4` at the evidence tip, in the return |
| One editorial review | `docs/track-b/evidence/pres-4/editorial.md` | 10 violations (V1–V10), repaired in `db65a46`; 13 recommendations, each dispositioned in the advisory log |
| The fresh reader | `docs/track-b/evidence/pres-4/fresh-reader.md` | answers 1–5 agree with the registry and the records; no violation; one new advisory (A-PRES4-7). A section appended after Integration review 1 corrects its observation 3 and records the reading's continued applicability to the repaired page: no answer quotes the changed text, and the placements are unchanged |
| Integration review 1, at `a852c0a` | `docs/track-b/evidence/pres-4/integration-review-1.md` | **FAIL**: V1, the v5 exact-ratio table's interval columns showed the rounded point value (`research_claims._render_derived` ignored `ciexact`); V2, the error scores' term had drifted from the standard's definition (P21) and the paired-difference term from P53's quotation. Both repaired in `1cae93f`, each bound by `tests/test_49` with negative controls; dispositions of its five observations in the advisory log (A-PRES4-8) |
| Integration review 2, at the candidate, and the focused recheck at the final SHA | `docs/track-b/evidence/pres-4/integration.md` | after this packet |
| The authorized MLflow upload, the mirror verification, the browser routes and the index | `pres-4-mlflow-upload.json`, `pres-4-public-mirror.json`, `pres-4-public-mlflow-routes.json`, `reports/presentation/mlflow_index.json` | after the independent check's PASS, before the `--final` build |

No real Safari, real iPhone or screen reader was used; the phone widths are emulated viewports, and the iPhone is
Playwright's emulated device in WebKit.

## 8. Publication completion receipt and the Owner's packet

### 8.0 What would be published

| Surface | Reviewed output | Identity | Now public |
|---|---|---|---|
| Report, GitHub Pages | `docs/index.html` at `<final_candidate_sha>`, the `--final` build | `<final_page_sha256>` (the return and `integration.md`); at the candidate, before the index, 1,994,385 bytes, `1512deee08086daf4a38362fcb98ff945785bb99222cc98756c6d743509090ac` | 1,907,718 bytes, `8a1fedd8bc6bf89d1db170b3fb83df34255e4c350c22113d1df52088c25c8c39` (PRES-3, `main` `e398a30`), read by the Orchestrator 2026-10-10T23:17Z |
| README | `README.md` at `<final_candidate_sha>` | `<final_readme_sha256>`; at the candidate `c816972a7ddb4509f4e7617f4f480588b2500becb9217d8d36a4afebee8315fc` | at `main` `e398a30`: `4ee0602e8809810d19c97e53f7cf50bf24536d2eb7a2a95652db44957385e4fa` |
| Static Space bundle | none: unchanged by the Owner's decision of 2026-10-11 | `9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585`, 805 files, 44,164,910 bytes; the reviewed copy at `.local/artifacts/pres-3/space-wasm-9028a118/`; `make wasm` at the candidate rebuilds it file for file (`pres-4-space-unchanged.json`) | revision `0331088725fedab2f5a1ec804ae03bf960cf126f`, serving exactly that bundle (`pres-4-space-check.json`, read 2026-10-11T10:49Z) |
| Space change | **none**: no upload, no deletion | — | — |
| Static Space card | `space-wasm/README.md` (the bundle's `README.md`) | `c92a2666d76255b24d8e0fb159f97bedcbee0a7a948fb6afeac4b02089bb9a67`, unchanged | the same |
| Space card (container, not hosted) | `space/README.md` | `745bbb932d78afbecdca3964af4885d223fd9301cd628bde1744f08e9f71d553`, unchanged | repository file only |
| MLflow `delu-generations` | `reports/presentation/mlflow-export/` | 44 runs; `cp22.json` `4be85b84…59359`, `cp23.json` `413ebf56…7eac0`, `cp24.json` `d55cf3de…2911`, `manifest.json` `af680390…ae1d`; the 16 runs of cp22, cp23 and cp24 and the one experiment-description write, uploaded under the brief's authority before the final build (§6), their run IDs in `pres-4-public-mirror.json` | 28 runs, no cp22, cp23 or cp24 run (PRES-3) |

The demo still runs v1: the model, its payload, the v1 claims and both cards are unchanged; the cards name v1.

### 8.1 Receipt — intended identities (the Owner and the public checker complete the rest)

| Surface | Intended identity | Action / unchanged rationale | Observed public identity and UTC time | Verification record and result | Outstanding action |
|---|---|---|---|---|---|
| GitHub source / README | `land/pres-4` (the squash of `<evidence_tip_sha>`, the same tree); README `<final_readme_sha256>`, whose glance and generation list name v5 and the two branches | push by the Owner (§8.3) | the Owner fills: pushed revision, time | `pres-4-publication-receipt.json` (GitHub main); the served README's hash (§8.5) | §8.2–8.3 |
| GitHub Pages | `<final_page_sha256>`: v5 headline, chapter, transition, comparison rows, branch cards, corrected planned list | deploy by the push (§8.3) | the Owner fills: served hash, time | `pres-4-publication-receipt.json` (GitHub Pages); `pres-4-public-report.json`; `pres-4-postdeploy-links.json` | §8.3, §8.5 |
| Public MLflow | `cp22`, `cp23` and `cp24` with their children in `delu-generations`, equal to the export; routes `experiment`, `compare:overview`, `compare:v5`, `compare:pooled-lightgbm-member-for-v4`, `compare:ddnn-member-on-v4`; the experiment description naming all eight parents; the 28 earlier runs unchanged | the authorized upload in this block, verified before the final build (§6) | run IDs and verification time: `pres-4-public-mirror.json` | `pres-4-public-mirror.json`, `pres-4-public-mlflow-routes.json`; after publication `pres-4-postdeploy-mlflow-mirror.json`, `pres-4-public-mlflow-routes-postdeploy.json` | post-deployment reverification (§8.5) |
| Hugging Face Space card | `c92a2666…`, unchanged | **no action**: the Space is unchanged by the Owner's decision; the card rides in the served bundle | the Owner fills: Hub revision (expected `0331088…`), public visibility, card hash | `pres-4-publication-receipt.json` (Space files); the card's raw bytes (§8.5) | §8.5 |
| Hugging Face direct demo | bundle `9028a118…`, serving the same v1 artifact | **no action**: unchanged | the Owner fills: the revision the receipt reads | `pres-4-publication-receipt.json` (Space files, direct demo page); `pres-4-public-demo.json`, `pres-4-public-demo-a11y.json`, `pres-4-public-states.json` | §8.5 |

- **Publication-to-MLflow mapping:** `<final_candidate_sha>` → exports `cp22.json`, `cp23.json`, `cp24.json` (and
  `manifest.json`) → the run IDs in `pres-4-public-mirror.json` → the routes in `reports/presentation/mlflow_index.json`.
- **Final product and daily updates:** not applicable (no final-product designation).
- **Completion disposition:** incomplete until the Owner's steps and their public checks; the independent public review
  gives the PASS / FAIL / INCOMPLETE verdict.
- **Authority:** the MLflow upload and the one experiment-description write, by the brief (the Owner's decision of
  2026-10-11). The landing, the push and the Pages deployment each need the Owner's own instruction; this packet grants
  none. There is no Space step.

Every command below is the Owner's, run from the primary checkout, `/Users/djourno/Downloads/PJM`. None opens a pager or
an editor. Substitute `<evidence_tip_sha>`, `<land_sha>`, `<final_page_sha256>` and `<final_readme_sha256>` from the
return, which also gives these commands with them filled in. Keep every record a step writes, first failures included.

### 8.2 Step 1 — the LAND

The primary checkout was on `main` at `e398a30` = `origin/main`, clean, with no stash, when read on 2026-10-11 at
10:52 UTC; the branch does not touch `progress.md`. If `main` has moved, stop: the tree check below assumes the
branch's base.

```bash
git --no-pager rev-parse --abbrev-ref HEAD
```

Expect `main`.

```bash
git --no-pager rev-parse HEAD gauntlet/pres-4
```

Expect `e398a30bb53ecd4c397aad0f34fd122d42e74553`, then `<evidence_tip_sha>`.

```bash
git --no-pager status --porcelain=v1
```

Expect no output (or only ` M progress.md`, the Orchestrator's own edit). Any other line: stop and resolve it first.

**No untracked twin** (a file in the working tree at a path the branch adds or changes would block or be overwritten by
the squash):

```bash
git --no-pager diff --name-only e398a30bb53ecd4c397aad0f34fd122d42e74553 <evidence_tip_sha> | while IFS= read -r f; do git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 && ! git --no-pager diff --quiet -- "$f" && echo "MODIFIED $f"; git ls-files --error-unmatch -- "$f" >/dev/null 2>&1 || { [ -e "$f" ] && echo "TWIN $f"; }; done; echo twins-checked
```

Expect only `twins-checked` (it printed only that against `2064fb6` on 2026-10-11 at 11:47 UTC).

```bash
git --no-pager merge --squash gauntlet/pres-4
```

Expect `Updating e398a30..<first 7 of evidence_tip_sha>`, `Fast-forward`, `Squash commit -- not updating HEAD`, then the
diffstat; no `CONFLICT` line.

**The staged tree equals the evidence tip's tree**, on the branch's paths and every other:

```bash
git --no-pager diff --cached --name-only <evidence_tip_sha> && test "$(git write-tree)" = "$(git rev-parse '<evidence_tip_sha>^{tree}')" && echo STAGED-TREE-EQUALS-EVIDENCE-TIP
```

Expect only `STAGED-TREE-EQUALS-EVIDENCE-TIP` (no path listed before it). If it does not print, stop: nothing is
committed yet, and `git reset --merge` restores the index.

```bash
git commit -F .local/artifacts/pres-4/land-commit-message.txt
```

Expect `[main <land_sha>] Publish PRES-4: v5 on every research surface, and two experiments not adopted`, then the
summary. The secret guard runs in the pre-commit and commit-msg hooks and prints nothing when clean.

```bash
git tag land/pres-4 HEAD
```

```bash
git tag evidence/pres-4 <evidence_tip_sha>
```

Both print nothing.

```bash
git --no-pager diff --stat HEAD <evidence_tip_sha>
```

Expect no output: the landed tree is the reviewed evidence tip's.

```bash
git --no-pager status --porcelain=v1
```

Expect the same as before the squash.

### 8.3 Step 2 — the push

**The value-based secret scan first**, over exactly what the push will send: the same guard the pre-push hook runs,
reading the credential values inside the process and printing only a variable's name and a path if one is found.

```bash
printf '%s %s %s %s\n' refs/heads/main "$(git rev-parse main)" refs/heads/main "$(git rev-parse origin/main)" refs/tags/land/pres-4 "$(git rev-parse land/pres-4)" refs/tags/land/pres-4 0000000000000000000000000000000000000000 refs/tags/evidence/pres-4 "$(git rev-parse evidence/pres-4)" refs/tags/evidence/pres-4 0000000000000000000000000000000000000000 | python3 scripts/secret_guard.py pre-push origin "$(git remote get-url origin)" && echo SECRET-SCAN-CLEAN
```

Expect `SECRET-SCAN-CLEAN`. A `secret-guard: BLOCKED` line means stop and tell no one the value (AGENTS.md
§ Credentials).

```bash
python3 scripts/publication_guard.py tree
```

Expect a PASS line: the landed page is the final build.

```bash
git push origin main land/pres-4 evidence/pres-4
```

Expect `e398a30..<first 7 of land_sha>  main -> main` and two `[new tag]` lines. The pre-push hook repeats both guards.
GitHub Pages then serves `docs/`.

### 8.4 Step 3 — no Space upload

The Space is unchanged by the Owner's decision of 2026-10-11: it keeps serving the released v1 from bundle `9028a118…`,
and the generated cards are byte-identical. There is no `deploy_space.py --upload` in PRES-4. If any later step finds the
served Space different from that bundle, stop and report it; do not redeploy under this packet.

### 8.5 Step 4 — the A6 public checks, per surface

Each writes a new record; keep a first failure beside its retry. The Playwright commands need
`PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright` (A-PRES3-4). Wait until Pages has
deployed the push (the first command returns `<final_page_sha256>`).

```bash
curl -s https://hrsi56.github.io/delu-day-ahead-forecast/ | shasum -a 256
```

Expect `<final_page_sha256>` once Pages has deployed (now `8a1fedd8…`, PRES-3's).

```bash
curl -s https://raw.githubusercontent.com/hrsi56/delu-day-ahead-forecast/main/README.md | shasum -a 256
```

Expect `<final_readme_sha256>`.

**The receipt** (automation item 6): GitHub `main`, Pages, the Space's files and direct demo page against the unchanged
bundle, the public MLflow mirror and the links, each checked independently and anonymously, every attempt kept.

```bash
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true uv run python scripts/publication_receipt.py --landing <land_sha> --bundle .local/artifacts/pres-3/space-wasm-9028a118 --expect 9028a11869a378ea5c3401a00ad46368e1c9e2f2f9f8732330d32b71af081585 --date pres-4
```

Expect the six §8 rows each `PASS` and `PASS: wrote reports/presentation/release-checks/pres-4-publication-receipt.json`,
with `pres-4-postdeploy-links.json` and `pres-4-postdeploy-mlflow-mirror.json` beside it; exit 0. The Space rows must
show the Space still serving `9028a118…`. (The two environment variables keep MLflow's usage telemetry off: the mirror
check imports MLflow.)

```bash
curl -s https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast/raw/main/README.md | shasum -a 256
```

Expect `c92a2666d76255b24d8e0fb159f97bedcbee0a7a948fb6afeac4b02089bb9a67` (the card is unchanged).

The browser records:

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py release https://hrsi56.github.io/delu-day-ahead-forecast/ --shots .local/artifacts/pres-4/public-report --out reports/presentation/release-checks/pres-4-public-report.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py demo --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/pres-4-public-demo.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py demo-a11y --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/pres-4-public-demo-a11y.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py states --engine chrome --engine webkit --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/pres-4-public-states.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py mlflow-routes --mirror-record reports/presentation/release-checks/pres-4-postdeploy-mlflow-mirror.json --shots .local/artifacts/pres-4/public-mlflow-postdeploy --out reports/presentation/release-checks/pres-4-public-mlflow-routes-postdeploy.json
```

Each passes with `passed` true (the routes: every expected route verified in both engines). The states check forces
failures inside the test browser only; it changes nothing on Hugging Face. GitHub may answer anonymous `blob` requests
with 503 after a burst: keep the failed receipt, wait, and rerun it with a new `--date` (for example
`pres-4-retry-1`); a 503 is never a pass.

**The independent public review.** A checker that wrote none of PRES-4's changes reads these records and the served
surfaces fresh, forms its findings before reading earlier reviews, and writes a new, dated review under `docs/track-b/`
with the per-surface identities (§10.3), the §9 matrix it could apply, first failures and retries, and its PASS / FAIL /
INCOMPLETE verdict (§10.4).

### 8.6 Step 5 — the receipt

Fill §8.1's last three columns from those records: the observed identity and UTC time per surface, the record and its
result, and any outstanding action. The closure record's inputs: the landing SHA and tags; the pushed revision; Pages'
served hash; the Space's revision, unchanged, and its served-set verification; the MLflow run IDs and the
post-deployment mirror and route records (§6); the receipt; the independent public review and its verdict; and every
first failure with its retry. The disposition is complete only when every row is verified.

### 8.7 If publication fails

Stop the rollout and name each affected URL and revision. The identities to restore are `main`
`e398a30bb53ecd4c397aad0f34fd122d42e74553` (Pages `8a1fedd8bc6bf89d1db170b3fb83df34255e4c350c22113d1df52088c25c8c39`);
the Space is not touched and stays at revision `0331088725fedab2f5a1ec804ae03bf960cf126f`. The uploaded cp22, cp23 and
cp24 runs stay: they are the committed evidence, and removing a tracking run is not part of any recovery. No force-push,
history rewrite or MLflow change is part of a recovery; a rollback is its own Owner action.

## 9. Applicability matrix

### 9.1 PUBLISH_RULES 1.4, clause by clause

| Clause | Applies? | How PRES-4 meets it, or why not | Evidence |
|---|---|---|---|
| §1.1–§1.3 authority, four identities, categories | yes | Rules 1.4 and the incorporated baseline pinned by hash in the brief and checked; publication rule, research generation (v5), product status (released v1 unchanged) and artifact identities kept apart | §1 of this packet; the return's identities |
| §2 reader contract and placements; A1; A2 | yes | Headline names each metric (A1) and leads with the verdict; placements measured in Chrome and WebKit with the measured header (A2) | `tests/test_43` A1; `pres-4-local-release.json` (`placements`) |
| §3.1 evidence classes; withheld claims | yes | Development, post-selection, on every v5 and branch number; W1–W48 in force, W42–W47 guarded | `v5.caveat.class`; `research_claims.py::WITHHELD_PATTERNS`; `tests/test_49` |
| §3.2 scores, comparisons, uncertainty | yes | The verdict with its date and N; the change as a share of v4's score with the ratio's interval from CP-24's own draws, at 95% and at the 97.5% decision level; absolute MAE per period with the stress period apart; one population, its dates and counts stated | §4; `derived.py`; `tests/test_49` |
| §3.3 counting | yes | The targets' census counts identities once by decision date (25); the chart's 12 rows are distinguished from it; study arms, branches and generations are distinct kinds | `RC.census_sentence`; P57 |
| §3.4 provenance and formatting | yes | Every number a record; whole percents, four significant figures, one decimal for EUR/MWh; the share of days as a count (A-PRES4-2) | `make lint-publication` PASS |
| §4 registry, transitions, branches; A3 | yes | One registry; v5's transition card (A3); the two branch cards after v4 with question, comparator, deciding result, "Not adopted", reason, date and evidence | `tests/test_43` A3; `tests/test_49` |
| §4 A10 revision in place | no | v5 is a new generation; no adopted generation is revised in place | — |
| §5 page architecture; A4 | yes, unchanged | The A4 order is unchanged; the product section documents the released v1 and is byte-identical | `tests/test_45` published sections |
| §5.2 chapter grammar; page budget | yes | v5's chapter fills every slot (`slot_problems` empty); one page, 1,994,385 bytes ≤ 2.0 MB without compaction (the Owner's D1) | `tests/test_49`; `reports/cp3/pages_build.json` |
| §6 charts, discovery; A5 | yes | v5's main chart with direct labels, the pentagon and readable values; the comparison's study points; A5 routes from the closed default page in both engines | `pres-4-local-release.json` (`discovery`); `tests/test_43` A5 |
| §7.1 product contract | yes, unchanged | The opening names v1 as the demo's model and v5 as research; release rule and startup line unchanged | the opening |
| §7.2 live presentation; A7 | no | No live panel is authorized | — |
| §7.3 final-product Space; A9 | no | No final-product designation | — |
| §8 surfaces | yes | Report, README, MLflow updated; Space card and demo verified unchanged (`pres-4-space-unchanged.json`, `pres-4-space-check.json`) | §8 of this packet |
| §9 browser and accessibility matrix | yes | Chrome and WebKit, every width, AX trees, keyboard, touch, contrast, zoom and reflow, requests, placements; the demo's controls | `pres-4-local-release.json`; `pres-4-local-demo*.json`, `pres-4-local-states.json` |
| §10.1 independence | yes | The editorial review, the fresh reader and both Integration Critics authored none of the changes | `editorial.md`, `fresh-reader.md`, `integration.md` |
| §10.2 fresh reader | yes | The six unchanged questions, closed-state screens only, answers kept | `fresh-reader.md` |
| §10.3 public identity; A6 | yes, after the Owner's steps | The receipt and the browser records on the public URLs | §8.5 |
| §10.4 verdict | yes | The Integration verdict | `integration.md` |
| §11 packet and order | yes | This packet; build → editorial → fresh reader → independent check → upload and verification → final build → recheck → the Owner's steps | §7 |
| §12 baseline coverage | yes | Incorporated clauses applied through the rows above | — |
| §13 acceptance record | yes | §9.2 below | — |
| §14 pending triggers | yes | "v5 or size-budget breach: the Owner decides compaction" — decided 2026-10-11, no compaction (D1); v5's encoding decided 2026-10-11 | the brief |
| A8 final product | no | No final-product designation or rollout | — |
| A11 work availability | yes | `AGENTS.md` § Work availability: no calendar check or pause was used | — |

### 9.2 The §13 acceptance record

| Area | Record |
|---|---|
| Authority | Rules 1.4 `ccfe6199…a80`; standard `7bb90c4c…68c`; plan `b04a0bb1…19c`; research anchor v21-r12 `caf03d70…7e4`; brief `54169c7c…bdd`; A7–A10 not applicable, with reasons (§9.1) |
| Identity | `gauntlet/pres-4` off `e398a30`; `<final_candidate_sha>`; `<evidence_tip_sha>`; the landing and the served identities after the Owner's steps |
| Claims | §4: source rows by blob and line, derivations, class, comparator and population, the census, the limitations |
| Reader | Default path and placements (`pres-4-local-release.json`); definitions under the headline, bound to their claims (`tests/test_49`); the fresh reader's record and its appended continued applicability |
| Journey | The v4 → v5 transition; two branch cards between v4 and v5; the planned list after the programme plan; no unperformed experiment implied |
| Content | The twelve product subjects unchanged for the released v1; v5's concise history; the v1 archive unchanged |
| Charts | v5's main chart; the comparison with its study points; A5 routes |
| Product | The demo's identity (v1), startup metadata, controls unchanged; the bundle `9028a118…` rebuilt identically |
| Accessibility | The engine and width matrix, keyboard, AX, focus, targets, contrast, zoom and reflow (`pres-4-local-release.json`); the demo's controls (`pres-4-local-demo-a11y.json`) |
| Tracking | The upload record, the mirror verification and the browser routes (§6–§7) |
| Release | `--final` build, guard and test results; the exact-candidate Integration check; the authorized upload's record |
| Public check | After the Owner's steps (§8.5) |
| Follow-up | Advisories A-PRES4-1 to A-PRES4-8; Integration review 1's two violations, repaired, and five observations; dispositions of A-PRES3-1, -5, -7; the editorial review's 13 recommendations and the fresh reader's 18 observations (§10) |
| Final product, daily panel, business, final-product Space | Not applicable |

### 9.3 The runbook

| Section | Touchpoint | Status |
|---|---|---|
| §2.1 `_ENTRIES` | v5 entry with every field, dated status from the landing record, predecessor v4 | done |
| §2.2 `CHECKPOINTS` | CP-24 (and CP-22, CP-23 under §3) | done |
| §2.3 `EVIDENCE_TAGS` | the three tags and dates | done |
| §2.4 `RULES` | `cp24-adoption` (and CP-22's three, `cp23-adoption`) | done |
| §2.5 `COMPARISON_ORDER` | v5 first; the comparison draws each row from its newest experiment (`COMPARISON_EXPERIMENTS`, `comparison_source`), guarded by `comparison_parity_problems` | done |
| §2.6 `CRISIS_ORDER` | unchanged: v5's chapter states its peak in text | not needed |
| §2.7 `research.py::SOURCES` | CP-22's, CP-23's and CP-24's rows pinned by blob; records including the 97.5% decision level | done |
| §2.8 `CRITERIA_FILES` | CP-22, CP-23, CP-24 | done |
| §2.9 `CHANGES` | `RATIO_CHANGES["v5"]`, `DECISION_LEVEL_CHANGES["v5"]`, `RATIO_CHANGES["ddnn2-alone"]` | done |
| §2.10 `PERIOD_SUBJECTS` | `PERIOD_SOURCES`: v5 from CP-24, the others unchanged | done |
| §2.11 claim maps | cp22, cp23, cp24 registered | done |
| §2.12 / 12a `BLOCKS` | `v5.*`, `transition.v4-v5.*` | done |
| §2.13 / 14 `v5_slots`, `chapter_sequence` | done |
| §2.15 `CHARTS_BY_RUN` | `cp24/v5`: the comparison and v5's main chart; `cp21/HGL`'s comparison pinned | done |
| §2.16 `TOKENS` and CSS | rose `#BE123C`, filled pentagon, "v5" (the Owner, 2026-10-11) | done |
| §2.17 `mlflow_export.py::CHECKPOINTS` | cp24 (and cp22, cp23) | done |
| §2.18 tests | `tests/test_49`, `tests/test_43` | done |
| §2 "What follows without an edit" | opening, rail, jump row, lineage, comparison rows, chapter order, README glance, run set and routes followed; the README's `generation_section` needed v5's section (it refuses an unknown generation); both Space cards' model line unchanged (the released model is v1) | checked |
| §2 "Limits to watch" | placements with A2's header (both engines); chart text ≥ 12 px; the 2.0 MB budget | `pres-4-local-release.json`; the build record |
| §3.1–3.5, CP-22 and CP-23 | entries of kind `branch` with study arms; checkpoints; tags; `branch.<id>.*` blocks; export specifications | done |
| §1 order; §1a receipt; §8 routes; §9 checks | as §7 and §8 of this packet | done / the Owner's |

### 9.4 The programme plan, stage 2 (scope)

| Item | Disposition |
|---|---|
| D1 no compaction | v2 and v3 untouched (byte-identical); the page fits |
| D2 CP-22 and CP-23 as "tested, not adopted", briefly and point by point, into the comparison chart where possible | Two branch cards; three study points (R, M, and CP-23's candidate), all on one population with v5 and v4 |
| D3 automation items 6 and 7 | Used: `scripts/prerelease.py` before the review; `scripts/publication_receipt.py` in the Owner's §8.5 |
| D4 advisories | A-PRES3-1 taken up; A-PRES3-7 deferred to the final product's Space deployment; A-PRES3-5 deferred (needs a suspension) |
| The Space stays on v1 | Unchanged: bundle `9028a118…`, both cards byte-identical, the equivalence gate passing |
| Risk: the page budget | Measured; within 2.0 MB without touching v2 or v3 |
| Risk: `scripts/mlflow_export.py` bound by CP-23's tests | `AMENDED_BY_PUBLICATION` in CP-23's (and CP-22's) tests, as PRES-3 did for CP-21 |
| "Say plainly": 17% of days, no October–December, one winter; DDNN-2 alone descriptive; post-selection development evidence and v1 the product; a full re-evaluation follows | Stated in the chapter, the transition and the planned list (the share as "448 of the 2,654 days", A-PRES4-2) |

### 9.5 The planned list (the brief's task-specific extract; P58)

| The brief | On the page and in the README |
|---|---|
| 4.6 removed | Gone: it is v5's chapter and the branch "DDNN member on v4" |
| A re-evaluation on every eligible day added | "A re-evaluation on every eligible day", with its question and deciding evidence |
| New input data added: fuel and carbon prices, neighbouring markets, earlier forecasts covering the delivery day | "New input data": "Do fuel and carbon prices, neighbouring markets, or earlier forecasts that already cover the delivery day add information to v5?" |
| 4.4V source-neutral (no "in-house") | "Wind and solar generation forecasts": "A generation forecast available before the auction, then an ablation" |
| 4.8 and "4.7T and live" kept | "Combining models" (4.8 · Recombination) and "Frozen-protocol evaluation, then prospective monitoring" (4.7T and live · Final evaluation), their content unchanged |
| Unscored, unnumbered, committing to no unfixed design; the comparator follows the registry | No item carries a score; "compared with v5 on the same days", from the registry's current generation |


## 10. Advisories carried with this packet

All in `docs/track-b/publication-advisory-log.md`, PRES-4's section:

- **PRES-3's open advisories named by the brief:** A-PRES3-1 taken up (the experiment description names all eight
  parents, one authorized write); A-PRES3-7 deferred to the final product's Space deployment (the Space is unchanged);
  A-PRES3-5 deferred (it needs a Lockdown suspension).
- **New:** A-PRES4-1 (whole-percent intervals that coincide at two levels), A-PRES4-2 (the share of days as a count),
  A-PRES4-3 (the experiment code `v5` in CP-23's run name), A-PRES4-4 (a draft subtitle over the field's length), A-PRES4-5
  (5,615 bytes left in the page budget at the candidate: the Owner decides compaction before the next generation), A-PRES4-6 (runbook §2
  still names CP-21 as the model), A-PRES4-7 (the branch cards do not name their own rules; the fresh reader), A-PRES4-8 (the draft-equality check
  cannot see a non-pending description change; Integration review 1).
- **The editorial review's** ten violations, repaired, and thirteen recommendations, each dispositioned; **the fresh
  reader's** eighteen observations, dispositioned in its record; **Integration review 1's** two violations, repaired in
  `1cae93f`, and five observations, each dispositioned.
