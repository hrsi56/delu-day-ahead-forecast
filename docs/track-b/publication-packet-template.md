# Publication packet: template

**Publication Standard v1 §12; written by the PRES-1 conformance task (brief W15), 2026-09-28;
PUBLISH_RULES 1.0 §11's A3–A5 fields added by PRES-2, 2026-09-29.**
Prospective final-product fields in §5d follow PUBLISH_RULES 1.1 A7/A8 and research v21-r5
§16 (Owner-approved 2026-09-29). They do not alter historical PRES-2 packets or activate Live.
Each research checkpoint's return includes one packet, filled in from inside the checkpoint, before
its results are published. The publication is built from it (`docs/track-b/publication-runbook.md`
gives every place each item lands). Until the landing templates carry the packet (standard §12,
§17 D6), the checkpoint's brief carries this template as its own section.

Replace every `<…>` with the checkpoint's value. Where an item does not apply, write "none" and the
reason. Numbers are never typed into a surface: each one below names the committed row it comes
from, and the evidence layer re-derives it.

---

## 1. Identity

| Item | Value |
|---|---|
| Checkpoint | `<CP-nn>`, brief `<path>` at `<SHA-256>` |
| Governing research plan and version | `<anchor and version>` |
| Evidence tag and tip | `evidence/<cp-nn>` at `<SHA>`, frozen `<YYYY-MM-DD>` |
| Final reviewed candidate (model code) | `<SHA>` |
| Report, review verdict, landing record | `<paths at the evidence tag>` |

## 2. The draft registry entry (standard §5)

One entry per identity the checkpoint evaluated: the candidate, and any new branch, reference, study
arm or control. Every field is required.

| Field | Value |
|---|---|
| `id` | `<id>` |
| `name` | For a generation adopted at this checkpoint: `v<N> · <adopted change>` (a number only on adoption, plan §16 decision 2). Otherwise a descriptive name. |
| `subtitle` | `<at most eight words>` |
| `short` | `<a short form for tight chart labels>` |
| `kind` | `generation`, `branch`, `reference`, `study arm` or `control` |
| `codes` | `<experiment>: <code> (<population>)`, one per experiment in which it appears. One identity across codes. |
| `statuses` | `<status>, <YYYY-MM-DD>, <source record>, <one-line reason if not adopted>` |
| `comparator` | `<registry id>`, as the governing plan names it (standard §3.2), recorded before results exist |
| `population` | `<comparability ID>`; if new, its plain description (runbook §4) |
| `evidence_class` | Development, one-shot test or live (standard §2) |
| `plan`, `rules` | `<plan §>`; `<pre-specified rule id, if any>` |
| `sources` | `<committed rows the numbers come from>` |
| `claim_map` | `<path>` |
| `run_keys` | `<cp-nn>/<code>, …` |
| `style`, `anchor` | `<marker and colour role>`; `<page anchor>`. **A new generation's colour is the Owner's decision** (standard §16, "At v4"). |
| `checkpoint`, `after` | `<CP-nn>`; for a branch, the generation it follows |
| `question`, `informed` | For a branch: its question, and what it informed |
| `predecessor` | For a generation after the first: the adopted generation it replaced (A3); never inferred from the version number |

## 3. The claim map

`docs/track-b/research-content/<cp-nn>-claims.md`: every sentence the publication will render, with
the committed rows it binds and the withheld phrases (W1–W21) it avoids. Status words come only
through registry tokens (`{g:<id>.<field>}`).

## 4. The derived headline quantities (standard §3.3), computed inside the checkpoint

| Quantity | Value | From |
|---|---|---|
| (a) The pre-specified verdict | met / not met | `<criteria row>` |
| The rule, in words, with the date it was set | `<rule>`, set `<YYYY-MM-DD>` | `<the record that establishes the date>` |
| Distance from the rule's comparator, in the rule's unit | `<point / interval>` | `<score rows>` |
| N: policies tested against the same rule up to this decision | `<N>`, listed | `<rows>` |
| "Point comparison" label needed? | yes / no | whether a confidence interval exists |
| (b) The change against the comparator, as a share of the comparator's score | `<point>%` and `<interval>%` | `<score rows>` |
| Its 95% interval | `[<low>%, <high>%]` | **The ratio's interval from the checkpoint's own bootstrap draws** (from CP-21 on), with the seed, replicates and block length |
| (c) Mean absolute error per period, EUR/MWh | ordinary periods `<low>–<high>`; stress period `<value>` | `<per-period rows>`; the stress period as the protocol names it |

## 5. Draft slot texts (standard §6)

One per slot of the chapter grammar, each as a claim block keyed `<id>.<slot>`:

| Slot | Draft |
|---|---|
| The question | `<…>` |
| The change | `<…>` |
| The main chart and its headline | the paired differences against the comparator on both primary scores, with 95% intervals; headline `<…>` |
| The reading, in one sentence | `<…>` |
| What the result does not establish (one to three) | `<…>` |
| The decision, dated | `<…>` |
| The evidence row | the report, the review verdict, the claim map, the MLflow comparison |
| Details, from the fixed menu | method; per-period consistency; stress period; coverage and width; protocol and review |

For a branch-only checkpoint: the branch card's question, comparator, difference with its interval
(or the diagnostic that decided it), "Not adopted" with a one-line reason, and the evidence.

## 5a. The adopted transition (PUBLISH_RULES 1.0 A3)

For a generation adopted at this checkpoint, one summary, reusing the chapter's records:

| Field | Value |
|---|---|
| Title | "From v<N−1> to v<N>: <the adopted change>" |
| Predecessor and dates | `<registry id>`, its dated status; this generation's adoption date |
| The change | `<data, features, model or interval policy>` |
| The comparator set in advance | `<registry id>`; whether it is also the predecessor |
| The result, with its uncertainty and evidence class | `<share of the comparator's score, 95% interval>`; `<class>` |
| Against the predecessor | when the comparator is not the predecessor: the commensurate comparison and where it is, or why none exists (no invented interval) |
| What it does not establish | `<limitations>` |
| The decision, dated, and the route to the comparison | `<decision>`; `<chart heading anchor>` |

Rejected branches of the checkpoint stay branch cards, headed apart from this summary.

## 5b. The released model's documentation (PUBLISH_RULES 1.0 A4) — only when the released model changes

| Subject (§5.1) | Disposition | Evidence (model, output, rows) | Route |
|---|---|---|---|
| 1 Data · 2 Regimes · 3 Inputs · 3b Seasonal rationale · 4 Validation · 5 Results · 6 Attribution · 7 Importance and sensitivity · 8 Where it fails · 9 Reliability · 10 Forecast · 11 Limitations · 12 Running it | supported / not evaluated / inapplicable, with the reason | `<record ids>`: the model, output and rows each describes | `#<topic anchor>` |

Also: the incoming and outgoing product, what shared text was kept after checking it applies, and
where the outgoing model's documentation is preserved.

## 5c. The chart routes (PUBLISH_RULES 1.0 A5)

| Chart | Its heading | The route's label | Where the route starts |
|---|---|---|---|
| `<chart id>` | `<heading anchor>` | `<descriptive label>` | the chapter's "Explore these results", a transition summary or a product topic |

## 5d. Final-product transition / daily operation (1.1 A7/A8, conditional)

Complete this section when the Owner-designated final product is selected or rolled out;
otherwise state the unmet trigger. A completed form is not operational evidence or permission.

| Field | Required value / evidence |
|---|---|
| Owner designation and lifecycle | Exact selected final version, dated decision; selected/frozen/deployed/live/evaluated states and outstanding prerequisites |
| One product identity | Incoming/outgoing product; registry/policy identity across opening, primary demo, README, Space and tracking; dated daily artifacts and historical replay labels |
| Frozen policy | Code/dependency, feature/input, hyperparameter, history/label-delay, initialization, seed, uncertainty/scoring and failure contracts; exact registry versions/fingerprints |
| Daily training and issuance | Numeric schedule, cutoffs, windows, resources, successful-fit records, artifact/input lineage; separate fit/refresh/issue times; explicit Owner-approved exception if retraining is impossible |
| Operational coverage | Every delivery day including DST; authorized unattended Friday/Shabbat coverage without manual Owner work; operator, monitoring, retry/fallback/staleness and failed-issuance records |
| Today | Saved pre-outcome hourly forecasts versus available published prices; source/revision timestamps, eligible hours, partial-day completeness and original issuing artifact |
| Percentage performance and MAE | Frozen formula, denominator, success tolerance if any, window/sample count, zero/negative/missing-price handling; distinguish benchmark improvement from correctness |
| Tomorrow and reliability | Issued hourly point/interval forecasts or pending/unavailable state; nominal interval level; measured past coverage and width with named window; no unqualified confidence percentage |
| Page order | Product/forecast opening → How the product works → Product results → Business insights → How the models compare; remaining sections unchanged; A8/A2 product finding placements |
| Product coverage and science | §5b's twelve-subject map, one canonical route per graphic, actual model/output/population; development, unused-data and prospective results separated |
| Business evidence | Intended decision policy, constraints/costs/capital, benchmark, complete cumulative net-value series and risk/loss context; simulation/realization labels and business-rate denominator; explicit gap if not evaluated |
| Acceptance | Daily record/replay and negative-control evidence; independent exact-candidate review; public service identities and existing browser/accessibility checks; unperformed checks labelled |
| Prospective state | Run start and days actually covered; failures/outages preserved; evaluation in progress until authorized CP-19 after at least 90 consecutive delivery days |

Do not invent metrics, tolerances, profit results or numeric operational budgets to fill the form.
Use the future ratified execution protocol and record unresolved prerequisites before launch.

## 6. The MLflow export

- The committed export (`scripts/mlflow_export.py`), built from the checkpoint's committed rows, with
  run names, parents, descriptions and tags from the registry entry above.
- The record-level diff against the last published export (`scripts/mlflow_export.py
  --diff-against <ref>`): nothing published before changes except names, descriptions and tags.
- The routes the registry will expect (`registry.expected_routes()`), each verified by REST and in
  Chromium and WebKit before it is linked.

## 7. Checks the checkpoint ran

- The re-derivation tests for every new record, with negative controls.
- The export contract test (the export matches the registry).
- The §4 lint on the draft slot texts.
- The transition's and, when it changed, the product documentation's contract tests
  (`tests/test_43_publish_rules_migration.py`).

## 8. Publication completion receipt — no surface omitted

Required for every publication under PUBLISH_RULES §§8, 10.3 and 11. The executor populates
intended identities before publication; the authorized publisher completes actual identities
and public verification afterwards. Do not retrofit these fields into a historical packet;
use its existing requirements and a new continuation/receipt where necessary.

| Surface | Intended identity | Action / unchanged rationale | Observed public identity and UTC time | Verification record and result | Outstanding action |
|---|---|---|---|---|---|
| GitHub source / README | `<landing SHA / content hash>` | `<push or verified unchanged>` | `<actual revision>` | `<public evidence>` | `<none or exact gap>` |
| GitHub Pages | `<report hash / release identity>` | `<deploy or verified unchanged>` | `<served identity>` | `<applicable public browser checks>` | `<none or exact gap>` |
| Public MLflow | `<export identity; experiment, run IDs and applicable registry versions>` | `<changed: authorized upload; unchanged: identity/diff and existing run references>` | `<actual verified record identities>` | `<fresh anonymous record/history/route verification>` | `<none or exact gap>` |
| Hugging Face Space card | `<Space revision / card identity>` | `<deploy or verified unchanged>` | `<Hub revision / public visibility>` | `<served card verification>` | `<none or exact gap>` |
| Hugging Face direct demo | `<bundle; model/policy and dated artifact/forecast identities>` | `<deploy or verified unchanged>` | `<served identities and freshness>` | `<artifact and applicable public demo checks>` | `<none or exact gap>` |

- **Publication-to-MLflow mapping:** `<publication SHA → export identity → public evidence/run/model references>`.
  An unchanged research export needs current verification, not duplicate research runs. Changed
  model/evaluation evidence must appear in its authorized public tracking destination.
- **Final product and daily updates, when applicable:** `<Owner-designated product → registered
  policy/initialization → dated daily fit/issuance records → actual served Hugging Face artifact
  and forecast>`. Include separate last successful training/publication times, failures, stale
  state and the frozen recovery disposition. Local success cannot substitute for hosted identity.
- **Completion disposition:** `<complete / incomplete>` with `<unresolved surfaces/actions>` and
  the standard's independent PASS/FAIL/INCOMPLETE verdict. A mismatch or missing required check
  prevents completion even when main was pushed. Preserve first failures and retries.
- **Authority:** `<Owner instruction for each external action or authorized operational scope>`.
  The form grants no upload, recurring publication or credential authority.
