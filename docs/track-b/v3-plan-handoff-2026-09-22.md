# v2 / v3 programme plan — owner handoff

**2026-09-22 · Proposed plan, not a ratified anchor or execution brief.**
CP-15 has Engineering PASS and `product_feasibility = NOT_DEMONSTRATED`.
No successor model is promoted or frozen. `capstone_v21.md` remains controlling;
§8 and its historical failed bar remain unchanged. This document proposes the work
needed for a decision packet, an additive CP-16 amendment and subsequent authorized checkpoints.
The current task rewrites this document only; none of that work is opened here.

**Zero external cost.** Free registration and free click-through terms are acceptable
where applicable in future authorized work; this rewrite accepts no terms, downloads no
weights, retrieves no data, creates no automation, contacts no provider and runs no admission checks or experiments. Paid services,
data, commercial-licence purchases and negotiated exceptions are outside scope, not future
workarounds. All agent work stays local. Owner alone lands and publishes. Presentation work
is content only: no rendering, layout review or visual QA.

**Reading order:** [three deliveries (§1)](#section-1), [next packet (§2)](#section-2), [Owner decisions (§3)](#section-3), [work (§4)](#section-4), [evidence (§5)](#section-5), [local handoff (§6)](#section-6).
[Work-item navigation index](#work-item-index) · [budget prerequisites (4.B)](#section-4-b) · [economic policy contract (4.E)](#section-4-e).
The [independent review](v3-plan-independent-review-2026-09-22.md) supplies the verification
methods and IR-01–IR-08 findings. The [earlier review](plan-review-2026-09-22.md) is historical
evidence, not authority. All reused development results remain `development_post_selection`.
Numerical verification labels below are attributed to those reviews; this rewrite ran no experiments.

<a id="work-item-index"></a>

**Navigation key.** Work-item IDs (`4.0`–`4.10` and their suffixes) are programme identifiers,
not a consecutive document-section sequence. The numbered document sections are §§1–6;
4.B and 4.E label the shared budget and economic contracts. Existing headings that carry
work-item IDs keep their labels for reference compatibility. A work item may be defined in
a register row or inline paragraph rather than its own heading. Links below use explicit,
stable anchors; the primary location and supporting requirements together identify its definition.
Parent/group IDs collect the listed existing items; they do not introduce additional work.
Grouped shorthand is expanded into separate links. The [4.5](#work-4-5)–[4.8](#work-4-8) heading covers shared candidate
constraints; [4.7](#work-4-7) and [4.7T](#work-4-7t) are distinct work items, not duplicate sections.

| Work-item ID | Primary definition | Supporting locations |
|---|---|---|
| [4.0](#work-4-0) | Preparation/amendment group | [4.0a](#work-4-0a); [4.0b](#work-4-0b); [budget prerequisites](#section-4-b) |
| [4.0a](#work-4-0a) | First-packet mandate in §2 | [register](#record-4-0); [assembled packet](v2-decision-brief-packet.md) |
| [4.0b](#work-4-0b) | Amendment/brief completion in register | [register](#record-4-0); [authority](#section-3-3); [budget prerequisites](#section-4-b); [economic contract](#section-4-e) |
| [4.1](#work-4-1) | Historical archive admission | [register](#record-4-1); [fallback decision](#section-3-2); [budget prerequisites](#section-4-b) |
| [4.2](#work-4-2) | Causal v2 specification | [register](#record-4-2); [budget prerequisites](#section-4-b); [economic contract](#section-4-e) |
| [4.3](#work-4-3) | Content group in register | [4.3R](#work-4-3r); [4.3C](#work-4-3c); [budget prerequisites](#section-4-b) |
| [4.3R](#work-4-3r) | Existing-evidence content in register | [existing-evidence route](#section-2); [budget prerequisites](#section-4-b) |
| [4.3C](#work-4-3c) | Candidate content in register | [4.7](#work-4-7); [budget prerequisites](#section-4-b) |
| [4.4](#work-4-4) | Weather/VRE boundary group | [4.4D](#work-4-4d); [4.4V](#work-4-4v); [register](#record-4-4); [budget prerequisites](#section-4-b) |
| [4.4D](#work-4-4d) | Direct-weather inline definition | [4.4](#work-4-4); [register](#record-4-4); [budget prerequisites](#section-4-b) |
| [4.4V](#work-4-4v) | Optional VRE inline definition | [4.4](#work-4-4); [register](#record-4-4); [budget prerequisites](#section-4-b) |
| [4.5](#work-4-5) | Per-block LightGBM constraints | [register](#record-4-5); [candidate constraints](#candidate-constraints); [budget prerequisites](#section-4-b) |
| [4.6](#work-4-6) | Distribution-challenger group in register | [4.6L](#work-4-6l); [4.6R](#work-4-6r); [4.6C](#work-4-6c); [budget prerequisites](#section-4-b) |
| [4.6L](#work-4-6l) | Licence admission | [register](#record-4-6l); [candidate constraints](#candidate-constraints); [budget prerequisites](#section-4-b) |
| [4.6R](#work-4-6r) | Training-only resource admission | [register](#record-4-6r); [budget prerequisites](#section-4-b) |
| [4.6C](#work-4-6c) | Predefined development comparison | [register](#record-4-6c); [budget prerequisites](#section-4-b); [economic contract](#section-4-e) |
| [4.7](#work-4-7) | Quality and delivery disposition | [register](#record-4-7); [budget prerequisites](#section-4-b); [economic contract](#section-4-e) |
| [4.7T](#work-4-7t) | Fresh-data comparison | [register](#record-4-7t); [4.9O](#work-4-9o); [budget prerequisites](#section-4-b); [economic contract](#section-4-e) |
| [4.8](#work-4-8) | Recombination definition in register | [candidate constraints](#candidate-constraints); [4.6C](#work-4-6c); [budget prerequisites](#section-4-b) |
| [4.9](#work-4-9) | Final freeze and prospective chain | [register](#record-4-9); [4.9O](#work-4-9o); [budget prerequisites](#section-4-b); [economic contract](#section-4-e) |
| [4.9O](#work-4-9o) | Daily operating/update contract | [4.9](#work-4-9); [register](#record-4-9); [budget prerequisites](#section-4-b) |
| [4.10](#work-4-10) | Local-handoff group in register | [4.10R](#work-4-10r); [4.10Q](#work-4-10q); [handoff requirements](#section-6); [budget prerequisites](#section-4-b) |
| [4.10R](#work-4-10r) | Research handoff branch in register | [register](#record-4-10); [handoff requirements](#section-6); [budget prerequisites](#section-4-b) |
| [4.10Q](#work-4-10q) | Qualified-product handoff branch in register | [register](#record-4-10); [handoff requirements](#section-6); [budget prerequisites](#section-4-b); [economic contract](#section-4-e) |

<a id="section-1"></a>

## 1. Three deliveries

| Delivery | Output | Entry conditions | Finish condition | Dependencies and existing work mapping |
|---|---|---|---|---|
| **v2 — improvement using existing information** | Combined forecasts with a causal uncertainty layer, pooled-residual control, saved predictions and evaluated results. | Authorized existing-input brief and applicable protocol/budgets under [4.0](#work-4-0). | Validated evaluation and disposition, including negative results; a blocked attempt returns its evidence and unmet conditions, not a completed evaluation. | [4.0](#work-4-0) → [4.2](#work-4-2) → [4.7](#work-4-7) delivery disposition / [4.3C](#work-4-3c) → applicable [4.10](#work-4-10) handoff. **Can finish without v3 or v3 live.** |
| **v3 — admissible weather information, historical evaluation** | Direct-weather paired ablation and contribution report; VRE modelling remains an optional extension under [4.4](#work-4-4). | Historical archive admission in [4.1](#work-4-1) and authorized weather brief/budgets under [4.0](#work-4-0). | Validated historical comparison and disposition, whether the gain is positive or negative; admission/execution failure returns a scoped blocker. | [4.1](#work-4-1) + [4.0](#work-4-0) → [4.4D](#work-4-4d) ([4.4V](#work-4-4v) only if admitted) → [4.8](#work-4-8) if admitted → [4.7](#work-4-7)/[4.3C](#work-4-3c) → applicable [4.10](#work-4-10). Uses the comparison policy fixed in [4.4](#work-4-4); depends on v2 outputs only if that comparison uses them. No live-source admission or prospective run is needed to finish historical research. |
| **v3 live — daily operation and prospective evaluation of the selected policy** | Daily acquisition and quality/freshness checks, prescribed model/state/context updates, scheduled saved forecasts, later outcome reconciliation; registered policy and final prospective evaluation. | Candidate/protocol freeze and fresh-data comparison [4.7T](#work-4-7t) → documented final [4.7](#work-4-7) decision and ratified feasibility. Before run start: CP-17 final policy freeze/registration, live suitability and CP-18 operational/publication authorization. | **Run start:** authorized daily issuance under [4.9O](#work-4-9o). **Validation finish:** ≥90 consecutive delivery days after the final freeze, using actual pre-outcome forecasts and the registry-bound CP-19 evaluation; include failures/delays. No guaranteed positive verdict. | Development → [4.7T](#work-4-7t) → final [4.7](#work-4-7) → [4.9](#work-4-9) final freeze/daily operation/prospective validation → [4.3C](#work-4-3c)/[4.10](#work-4-10). Only admitted candidates enter; this is an operational stage, not another model version. |

**Sequence for the live route:** freeze V3 candidates and the test protocol → compare on
new data unused for development/selection → document the decision → final freeze of the
selected policy → daily operation → prospective validation. The candidate freeze is **not
a final product freeze**. [4.7T](#work-4-7t) precedes final selection and full live-system setup; its
bounded chronological evaluation does not require that setup. It is not a prerequisite for
independent v2 delivery, historical V3 research or closing research with a negative/blocker report.

**Completion, quality and publication are separate.** Completing an authorized experiment
or reporting a blocker closes its work packet; only a completed evaluation against the
applicable ratified bar can demonstrate quality. Starting the live run does not complete
validation. Local handoff is separate from Owner publication authority, and none of these
delivery names guarantees a gain or a qualified product.

A1 scores **S_MAE 0.67229 / S_WIS 0.64602**, against the unchanged §8 limits
**0.59203 / 0.57509**. B2 has the best single-arm S_MAE, **0.65781**.
Restricted oracle combinations still miss the point bar; they do **not** establish
an information ceiling or rule out a better architecture on the same inputs (§5.2).

Weather is a promising new-input hypothesis. The post-gate A69 bundle reduced v1 pooled
raw-head pinball by **19.4926%**; that is neither measured CP-15 S_MAE improvement nor
an expected gain from an in-house VRE forecast. Historical GFS and ICON-EU archives
predate 2021, so crisis-fold feasibility remains open. Resolve actual vintage, variable
coverage and extraction cost before committing to a weather build ([4.1](#work-4-1)).

<a id="section-2"></a>

## 2. Existing evidence and the next bounded packet

v1 remains the shipped, frozen, public LightGBM nine-quantile ensemble, CQR then isotonic
projection. Preserve its reported failures: **p=.948** and August-2022 peak coverage
**79/408 ≈ .194**. These are historical reported evidence, not newly verified here.

Existing CP-15 evidence can separately finish an authorized research-content package through
**[4.3R](#work-4-3r) → [4.10R](#work-4-10r)**, with no new model, v2/v3 result or prospective qualification required.
It carries limitations and no qualified-successor claim; public release still needs its
Owner-approved route and any necessary additive amendment.

CP-15 A1 already reduced **full-crisis-fold** MAE from v1's **140.99 to 51.21 EUR/MWh
(~64%)**. This belongs to CP-15, not to an unbuilt v2. Emitted A1+B2 scores **.64466**,
central A1+B2 before new residuals **.64070**, and emitted A1/A3/A5/B2 **.64280 S_MAE**.
These are different policies; none measures the proposed causal v2.

**Recommendation, not an Owner decision:** authorize **[4.0a](#work-4-0a)**, one decision-ready packet
for a single existing-input v2 test. If research content is wanted now, authorize **[4.3R](#work-4-3r)**
independently. Weather admission and architectural challengers need not precede either.
The unresolved choice of next delivery remains [D1](#decision-d1) below.

<a id="work-4-0a"></a>

**First packet [4.0a](#work-4-0a) — ready to authorize as document work.** Accountable executor: a future
Orchestrator, not this rewriter. Inputs: this plan, the two reviews, CP-15 protocol/status,
and Owner choices already supplied. Deliver one proposed decision sheet and one draft v2
brief at [docs/track-b/v2-decision-brief-packet.md](v2-decision-brief-packet.md), a proposed destination requiring the
packet's allowlist. Include the fixed central blend, one otherwise identical pooled-residual
control, causal checks, proposed engineering specification, exact missing Owner fields and
amendment scope. No fitting, new archive admission or locked-file editing belongs to [4.0a](#work-4-0a).

Estimated effort **4–8 active hours** covers [4.0a](#work-4-0a) plus the [4.0b](#work-4-0b) documentation completion
below, not a hard resource allowance. The finite packet ends after one assembled draft and
its consistency check: return it with unresolved fields marked, rather than loop on decisions
or solicit permission per detail. Dependencies are only packet authorization and existing
evidence. It can finish decision-ready/blocked-for-execution without waiting for Owner latency.
Any added rounds or experiments are outside this packet. Its handoff lets the Owner resolve
only material choices, then lets [4.0b](#work-4-0b) finalize the authorized amendment/brief.

<a id="section-3"></a>

## 3. Owner decisions — unresolved

<a id="section-3-1"></a>

### 3.1 Product, comparator and economic bar

Choose the intended user/decision and whether the next delivery is a research artifact,
a point-forecast product, an interval product, or both. Decide a new CP-16 bar before
new comparisons; preparing [4.0a](#work-4-0a) does not require that decision to be settled. A demanding
diagnostic best-reference comparator is legitimate;
its non-deployability is not by itself a defect. Keep the original §8 assessment visible.

> **Contamination disclosure — read before adopting any threshold below.**
> An earlier draft of this plan proposed an economic threshold of "one third of the gap between
> naive and perfect foresight", i.e. ≈ 90.9 %. **That fraction was chosen after seeing that the
> candidates sit at 90.7–91.4 % (§5.6).** It is a bar fitted to its candidates, which is precisely
> what §8 forbids. It is disclosed rather than laundered, and **it must not be adopted as written.**
> It has a second defect independent of its origin: at 90.9 % it discriminates between A2 and the
> blend on 0.6 percentage points of a backtest carrying no confidence interval — a threshold inside
> the noise of the thing it judges.
>
> **The economic threshold must be derived from outside the results** — from what a forecast is
> worth to a flexibility operator, a margin over the cost of running it, or any external rationale
> the owner can state in one sentence — and fixed before looking at §5.6 again. If a threshold
> derived that way lands below what v2 already achieves, that is a legitimate answer. The reverse
> is not.


The historical block above is preserved verbatim. Its “v2 already achieves” wording does
not report an outcome for the unbuilt causal v2. The later exploratory interval in §5.6 does
not rehabilitate the contaminated threshold. A new externally justified specification can
govern future evaluation; it cannot make already-seen results unseen.

**Actionable decision record:** specify user, asset/exposure, comparator, execution
assumptions, independently justified operating cost and required surplus. Define an
incremental *net-value* gate and uncertainty rule from those inputs. If no external
rationale exists, choose economics as descriptive only; do not manufacture a percentage
threshold. Already-seen results cannot become unseen through a new specification.

Proposed tiers remain decisions, not accepted criteria:

- **Tier 0:** B0 as deployable comparator; report B2 alongside it. Owner decides whether
  this is sufficient, including whether a stronger deployable reference should gate promotion.
- **Tier 1:** beat B0 on both MAE and WIS in every fold; A1 passes this descriptive test.
- **Tier 2:** set coverage tolerances, width/WIS guardrails, minimum support and uncertainty
  treatment for fixed hour blocks. Suggested exhaustive blocks are night 22–05, solar
  10–16, shoulder/peak 06–09 and 17–21. Point and interval gates are separate.
- **Tier 3:** predefine economic decision, fees/degradation, SOC/cycle constraints, missing
  days, temporal aggregation and paired uncertainty. EUR/MW/year requires a representative
  horizon and declared annualization; selected seasonal folds do not provide one.
- **Tier 4:** retain the original 10%-over-best-reference screen as a reported stretch
  comparison if the Owner chooses a different new product gate; never relabel CP-15 as passed.

<a id="section-3-2"></a>

### 3.2 Evaluation scope if archive admission fails

Do not assume failure from an archive summary. NCAR GFS has documented depth for all
five folds; OCF ICON-EU has plausible crisis training depth. [4.1](#work-4-1) determines admission.
If it fails, the Owner chooses: (1) modern folds only with matched baselines and a scoped
claim; (2) amended fold dates, retaining the 2019 input boundary unless separately decided;
(3) a strictly causal proxy with its own label, never reanalysis presented as a forecast;
or (4) a modern-regime prospective evaluation after policy freeze. No option is selected here.

`2026-04-08..2026-09-06` is **152 calendar days**, but contains v1 embargo, final calibration
and spent holdout partitions. It is not unused confirmation data. April 8..September 22
is 168 dates only including today; the snapshot ends September 6. Data from September 7
onward is outside that snapshot, not automatically collected or an authorized holdout.
Retrospective comparisons stay exploratory. The standing prospective gate is **at least
90 consecutive delivery days after policy freeze**, not a retrospectively chosen window.

<a id="section-3-3"></a>

### 3.3 Decision register and authority

Only the following material choices belong to the Owner. Engineering specifies reproducible
methods within that authorized scope; it need not request approval for each parameter,
file or routine verification. A future brief can settle its engineering fields in one pass.

| Decision | Unresolved Owner choice | Work actually blocked |
|---|---|---|
| <a id="decision-d1"></a>[D1](#decision-d1) | Intended user, decision/exposure and next delivery: research, point, interval or both. | Choice of delivery; [4.3R](#work-4-3r)/[4.10R](#work-4-10r) need their content/release scope. Does not prevent preparation of [4.0a](#work-4-0a). |
| <a id="decision-d2"></a>[D2](#decision-d2) | Comparator; point/interval/coverage/support/uncertainty gates; external economic rationale and required net surplus, or descriptive economics. | [4.0b](#work-4-0b) ratification and new scored experiments [4.2](#work-4-2)/[4.4](#work-4-4)–[4.6](#work-4-6)/[4.8](#work-4-8) under their applicable bars; product qualification. Existing evidence needs no new bar. |
| <a id="decision-d3"></a>[D3](#decision-d3) | Market/settlement resolution, live operation expectations and quality-versus-delivery tradeoff. | Product economics, delivery admission and [4.9](#work-4-9)/[4.10Q](#work-4-10q); not scoped hourly descriptive reporting. |
| <a id="decision-d4"></a>[D4](#decision-d4) | Exact material resource/candidate allowances; admission of the TabPFN–DDNN route in [4.6](#work-4-6), other optional challengers, VRE extension or recombination. | Each affected experiment and prospective operating budget only. [4.6](#work-4-6) does not block v2; no default replacement version/family or optional extension. |
| <a id="decision-d5"></a>[D5](#decision-d5) | Archive-failure fallback in §3.2. | Weather work on an unadmitted scope; never existing-input v2 or existing-evidence content. |
| <a id="decision-d6"></a>[D6](#decision-d6) | Task-scoped Lockdown suspension, additive amendment, ratification, checkpoint/operational authorizations and research/product release route. | [4.0b](#work-4-0b) locked edits and subsequent stages requiring that authority. No amendment or operational authority is granted here. |
| <a id="decision-d7"></a>[D7](#decision-d7) | Landing, commit and publication. | Owner's external/mainline actions only; completed local handoff need not wait. |

The daily operating objective in §1/[4.9O](#work-4-9o) is now specified; it does not settle [D1](#decision-d1)'s user or
product scope. [D2](#decision-d2)–[D4](#decision-d4) still govern material test/selection gates, service/failure tolerance,
candidate allowances and test/daily-operation budgets for [4.7T](#work-4-7t)/[4.9](#work-4-9). Engineering fixes exact
unused dates, per-model cadences, windows and reproducible methods within those allowances
before candidate freeze. [D6](#decision-d6) covers the necessary future test/stage authority; none is granted here.

For **existing-input v2**, [4.0b](#work-4-0b) can follow [4.0a](#work-4-0a) and the applicable decisions without [4.1](#work-4-1).
Only a **weather-scoped amendment/brief** needs its admission decision. Before any locked
edit, the Owner must manually and temporarily suspend the Lockdown for the named objective
and files. The future additive change concerns `capstone_v21.md` §10's CP-16 candidates/bar
and any necessary research route through §§9–10, plus a specifically named amendment record.
Exact proposed additions belong in [4.0a](#work-4-0a) for review; no sentence of the existing §8 is removed
or relaxed, and this document grants no research-route exception. CP-17 still requires
feasibility under the ratified route. No locked change is needed to finish this rewrite.

<a id="section-4"></a>

## 4. Work register — bounded first packet, conditional engineering

IDs [4.0](#work-4-0)–[4.10](#work-4-10) are retained. [4.0a](#work-4-0a)/[4.0b](#work-4-0b) split preparation from authorized amendment completion;
[4.3R](#work-4-3r)/[4.3C](#work-4-3c) split existing-evidence from candidate content; [4.4D](#work-4-4d)/[4.4V](#work-4-4v) split direct weather
from optional VRE; [4.6L](#work-4-6l)/[4.6R](#work-4-6r)/[4.6C](#work-4-6c) separate licence, resource and comparison stages,
with reporting/selection in [4.7](#work-4-7); [4.7T](#work-4-7t) adds the fresh-data test before final live-policy
selection, and [4.9O](#work-4-9o) specifies daily operation. [4.10R](#work-4-10r)/[4.10Q](#work-4-10q) distinguish research from qualified-product handoff.
These suffixes separate deliverables, not additional approval gates; one appropriately scoped
Owner authorization may cover consecutive steps. No item is opened by this plan.
A future brief assigns a named executor/reviewer and paths.
The destinations below are **proposed**, not newly authorized outputs.

Effort ranges are active engineering/documentation estimates, including verification and
review preparation, **not measured runtimes or hard caps**. Missing numeric budgets in [§4.B](#section-4-b)
block the affected execution, not preparation of its brief. All items stop at their authorized
scope/budget and return completed evidence or an explicit negative/blocked disposition;
none silently expands its search. External cost is zero throughout.

| ID / accountable future role | Deliverable → proposed local destination | Dependency / finish and handoff | Estimated effort |
|---|---|---|---|
| <a id="record-4-0"></a><a id="work-4-0"></a><a id="work-4-0b"></a>[4.0a](#work-4-0a) / [4.0b](#work-4-0b) / Orchestrator | Decision packet → [docs/track-b/v2-decision-brief-packet.md](v2-decision-brief-packet.md); exact amendment/brief paths named there · [budget prerequisites](#section-4-b) · [economic contract](#section-4-e) | [4.0a](#work-4-0a) as §2. [4.0b](#work-4-0b) needs [D1](#decision-d1)–[D4](#decision-d4) as applicable and [D6](#decision-d6); weather-only scope also [4.1](#work-4-1). Finish with ratified bounded brief or exact unresolved blocker. No locked edit without suspension. → relevant experiment | 4–8 h total + Owner latency for [4.0b](#work-4-0b) |
| <a id="record-4-1"></a>[4.1](#work-4-1) / Lead under feasibility brief | Historical provider/fold admission and gap dossier → `reports/weather-admission/` | Separate read-only feasibility authorization, source/sample budget. Apply [4.1](#work-4-1); ADMIT or NOT_ADMITTED for historical use, independently of live suitability in [4.9](#work-4-9). Stop at **16 active hours** even if gaps remain. → [4.0b](#work-4-0b) weather scope/[4.4](#work-4-4) or [D5](#decision-d5) | 8–16 h + transfer/registration/queues |
| <a id="record-4-2"></a>[4.2](#work-4-2) / Lead | Causal v2 and pooled control, common-grid predictions, review → `reports/v2-causal/` | [4.0b](#work-4-0b) v2 brief, [§4.B](#section-4-b) budgets, [4.2](#work-4-2) protocol. Validated positive/negative result or evidenced blocked replay; no missing rows disguised as success. → [4.7](#work-4-7) and [4.3C](#work-4-3c) | 24–40 h |
| <a id="record-4-3r"></a><a id="work-4-3"></a><a id="work-4-3r"></a>[4.3R](#work-4-3r) / content executor named by brief | CP-15 narrative, tables/chart specifications, claim links → `docs/track-b/research-content/` · [budget prerequisites](#section-4-b) | [D1](#decision-d1) and bounded content authorization; existing evidence only. Finish evidence-linked local content with failures/limits and withheld claims explicit. No [4.2](#work-4-2)/[4.9](#work-4-9) dependency. → [4.10R](#work-4-10r) | 6–10 h |
| <a id="record-4-3c"></a><a id="work-4-3c"></a>[4.3C](#work-4-3c) / [same role](#work-4-3r) | Candidate-specific content → `docs/track-b/candidate-content/` · [budget prerequisites](#section-4-b) | Validated results of admitted experiments, including negative/blocked. No invented v2 results. → corresponding [4.10](#work-4-10) route | 6–10 h; shared work not double-counted |
| <a id="record-4-4"></a>[4.4D](#work-4-4d) / [4.4V](#work-4-4v) / Lead | Weather lineage and direct paired ablation; optional VRE comparison → `reports/weather-ablation/` | [4.1](#work-4-1) historical admission + [4.0b](#work-4-0b) weather brief/budgets; no live-source prerequisite. D first; V only if explicitly admitted under [4.4](#work-4-4). Negative gain completes a comparison. → [4.8](#work-4-8) if admitted, else [4.7](#work-4-7); failed admission → [D5](#decision-d5) | 64–120 h for original combined scope; direct-only estimate must be supplied by brief |
| <a id="record-4-5"></a>[4.5](#work-4-5) / Lead | Three-block LightGBM raw/normalized comparison and fit-cost report → `reports/block-challenger/` | Explicit candidate brief/[D4](#decision-d4); fixed blocks, training-only selection and budgets. Report all applicable gates, even when failed. → [4.8](#work-4-8) if admitted, else [4.7](#work-4-7) | 12–24 h |
| <a id="record-4-6l"></a><a id="work-4-6"></a>[4.6L](#work-4-6l) / Lead under bounded admission brief | Version-specific use-permission table and sources → `reports/distribution-challenger/licence-admission.md` | [D4](#decision-d4) route/resource allowance, exact intended user/uses and admission authority. Apply [4.6L](#work-4-6l); finish with a disposition for every use. Stop at the earlier of the brief cap or **4 active hours**, retaining unresolved entries; research not permitted/unresolved → no run, report to [4.7](#work-4-7). Research permitted → [4.6R](#work-4-6r), even if product use is not. | 2–4 h |
| <a id="record-4-6r"></a>[4.6R](#work-4-6r) / Lead | Training-only resource/output feasibility record → `reports/distribution-challenger/resource-admission.md` | Research permission for each tested candidate, authorized hardware and numeric thresholds/sample scope fixed in the brief. Apply [4.6R](#work-4-6r); finish PASS/NOT_ADMITTED per candidate. Stop at first exhausted cap or failed threshold/output requirement; no evaluation-driven tuning. → [4.6C](#work-4-6c) if eligible, otherwise [4.7](#work-4-7) | 4–8 h |
| <a id="record-4-6c"></a>[4.6C](#work-4-6c) / Lead | One preregistered TabPFN–DDNN/reference comparison, emitted predictions and uncertainty/cost report → `reports/distribution-challenger/comparison/` | Both candidates pass licence/resource entry checks; authorized [4.0b](#work-4-0b) brief, [§4.B](#section-4-b) budgets and [4.6C](#work-4-6c) protocol fixed before execution. Finish the specified comparison or an explicit partial/blocked report at its first stop condition. A candidate failing entry permits only the reference comparisons already authorized by the protocol; no claim of a completed direct comparison. → [4.8](#work-4-8) only if separately admitted, otherwise [4.7](#work-4-7) | 18–36 h for the combined comparison, not per family |
| <a id="record-4-8"></a><a id="work-4-8"></a>[4.8](#work-4-8) / Lead, optional | Frozen-family recombination/disagreement test → `reports/recombination/` · [budget prerequisites](#section-4-b) | New admitted arm from [4.4](#work-4-4)/[4.5](#work-4-5)/[4.6](#work-4-6), explicit opt-in protocol and budget. Score fixed/estimated combinations on identical rows; oracle separate; accept negative result. → [4.7](#work-4-7) | 8–16 h |
| <a id="record-4-7t"></a>[4.7T](#work-4-7t) / Lead + named independent reviewer | Candidate/protocol manifest, unused-period audit, chronological comparison and failure/cost evidence → `reports/fresh-policy-comparison/` | Authorized brief/[D2](#decision-d2)–[D4](#decision-d4)/[D6](#decision-d6); admitted candidates after bounded development, including [4.8](#work-4-8) only if admitted; [4.7T](#work-4-7t) data and protocol gate. Finish one valid comparison or exact negative/blocked report. Stop at any exhausted cap, compromised independence or invalid replay; no tuning loop. → final [4.7](#work-4-7), or research closure | 16–32 h estimated preparation/replay/review; data accrual and compute separately budgeted |
| <a id="record-4-7"></a>[4.7](#work-4-7) / Orchestrator | Separate measured-quality finding and delivery selection; final retained/reference/rejected/deferred record and evidence identity → `docs/track-b/candidate-disposition.md` | Enter with completed results or evidenced blockers; apply [4.7](#work-4-7). Record each delivery without waiting for later deliveries. Final live-policy selection requires [4.7T](#work-4-7t) after admitted development comparisons, **including [4.8](#work-4-8) if admitted**, otherwise its deferral. Finish with quality, permissions and disposition, even if inconclusive/no feasible policy. Stop at the documentation/review cap with gaps; no new experiments. → local research handoff independently, or [4.9](#work-4-9) if selected/feasible | 2–4 h, including [4.6](#work-4-6)/[4.7T](#work-4-7t) decision reporting |
| <a id="record-4-9"></a>[4.9](#work-4-9) / Lead + named operator; Owner/Orchestrator stage authority | Registry/freeze, issued lineage, scorecard, final evaluation → `reports/prospective-policy/` | Ratified feasibility, final [4.7](#work-4-7), live suitability of selected inputs, [D3](#decision-d3)/[D6](#decision-d6) and [4.9](#work-4-9) chain. Recorded run start is distinct from the final positive/negative/blocked evaluation; elapsed time alone never qualifies. → [4.3C](#work-4-3c)/[4.10](#work-4-10) | 16–24 h setup/evaluation estimate; operation extra, undetermined |
| <a id="record-4-10"></a><a id="work-4-10"></a>[4.10R](#work-4-10r) / [4.10Q](#work-4-10q) / Lead for local bundle; Owner for release | Reproduction/runnable artifacts, notices, evidence-labelled content, review and handoff → `docs/track-b/release-handoff/` (artifact paths in brief) · [budget prerequisites](#section-4-b) · [economic contract](#section-4-e) | <a id="work-4-10r"></a>[4.10R](#work-4-10r): [4.3R](#work-4-3r) and approved research scope, no [4.2](#work-4-2)/[4.9](#work-4-9). <a id="work-4-10q"></a>[4.10Q](#work-4-10q): [4.3C](#work-4-3c) + qualified [4.9](#work-4-9). Negative candidates can finish a research handoff under its route. Local review/manifest complete → Owner; publication may wait | 8–16 h local + separate Owner time |

<a id="section-4-b"></a>

### 4.B Budget and brief prerequisites

**Engineering fields:** within Owner allowances, the assigned Lead fixes recipes, numerical
methods, controls, inner-validation splits, tie rules, manifests, tests and failure dispositions.
Freeze inner-selection rules and outer-scoring policy before execution. Unknown allowances
are [D4](#decision-d4) decisions; unspecified technical fields are brief-completion work, not extra approval gates.

Every experiment brief must supply numeric caps for **candidate policies, configurations,
seeds, ensemble members, feature recipes, selection trials, refits/warm-up/replays, aggregate
fits, compute hours, active effort, memory/storage**, plus exact durable artifact paths and
reviewer. Explicitly set unused dimensions to zero/not applicable; do not leave “bounded”
as a value. Count references that need new fits, pooled controls, raw/normalized variants,
failed admissions and failed fits, warm-up and any [4.8](#work-4-8) work. Stop on the first exhausted cap,
retain partial evidence and report BLOCKED/INCOMPLETE; that is not product failure evidence
unless the authorized protocol says so. No automatic retries or extra families beyond budget.

Item-specific unresolved fields before execution:

- **[4.0b](#work-4-0b):** exact bars, amendment/brief paths and authority; its draft may return those gaps.
- **[4.1](#work-4-1):** number of providers/runs/decoded samples, fields/endpoints, bytes/storage/transfer
  limit and historical-coverage/publication-evidence deadline; 16-active-hour stop remains.
  Live continuity belongs to [4.9](#work-4-9), not historical admission. No fitting budget needed.
- **[4.2](#work-4-2):** hour-pooling/shrinkage configuration count, fixed pooled control, warm-up/refit
  counts and compute/replay budget; one proposed v2 policy does not imply one model fit.
- **[4.3R](#work-4-3r) / [4.3C](#work-4-3c):** precise content allowlist and finite correction-round/active-effort allowance;
  no model work. Close with a documented gap if evidence cannot support a requested claim.
- **[4.4D](#work-4-4d) / [4.4V](#work-4-4v):** separate direct-weather and VRE feature/configuration/label/admission/fit budgets,
  continuation criterion, cost estimate and generated-feature validation paths. VRE is optional.
- **[4.5](#work-4-5):** raw/normalized arms and capacity-grid/seed/refit caps.
- **[4.6L](#work-4-6l) / [4.6R](#work-4-6r) / [4.6C](#work-4-6c):** exact candidate versions/revisions and intended uses; bounded licence-source
  review; hardware, training-only sample manifest and representative size; peak-memory and
  load/preparation-or-fit/prediction-time thresholds; finite configurations/seeds/ensembles,
  inner-selection/refit and total-compute caps, including both candidates, references and
  failed checks. Fix the shared information/history/row contract, output/calibration recipes,
  v2 inclusion rule, paired uncertainty method, quality preference/tradeoff rule and permitted
  comparisons if a candidate fails entry. These are required pre-run fields, not approved
  values supplied by this rewrite. [D4](#decision-d4) sets material allowances; Engineering fills the brief
  within them without per-detail approval.
- **[4.8](#work-4-8):** combiner family/grid, feature/disagreement recipes, chronological training, fit/seed
  caps and declared gain/uncertainty rule. Otherwise explicitly deferred in [4.7](#work-4-7).
- **[4.7](#work-4-7)/[4.10](#work-4-10):** finite documentation/review-round effort and exact candidate/artifact identity;
  **[4.7T](#work-4-7t):** final candidate list and frozen artifacts/update policies, independently unused
  period and access audit, time blocks/targets/horizons, metric/selection/uncertainty rules,
  input-matched contrasts, initial states, chronology, failure policy and total replay budget.
  **[4.9](#work-4-9):** [4.9O](#work-4-9o)'s per-model numeric cadence/window/label-delay manifest; hardware and daily
  acquisition/check/update/prediction deadlines, compute/memory/storage and bounded retry caps;
  setup plus operator/incident time, monitoring and evaluation budget. No unstated 90-day
  maintenance commitment. These fields must be complete before [4.7T](#work-4-7t), not invented after selection.

**Path accounting:** the existing-input path through v2, then v3 live if that policy is selected,
to local qualified handoff is approximately
**76–134 active hours** ([4.0](#work-4-0)+[4.2](#work-4-2)+[4.3C](#work-4-3c)+[4.7T](#work-4-7t)+[4.7](#work-4-7)+[4.9](#work-4-9)+[4.10Q](#work-4-10q)), adding the proposed 16–32 h
fresh-data test to the earlier 60–102 h estimate. Exclude data-accrual time, operation,
Owner latency and ≥90 consecutive days after final freeze; this is not an approved budget.
[4.7T](#work-4-7t) adds no work to standalone v2 completion. Weather admission is not required for an
existing-input policy. Existing-evidence
content plus local handoff is **14–26 h** ([4.3R](#work-4-3r)+[4.10R](#work-4-10r)); [4.0](#work-4-0) is another **4–8 h** if a decision/
amendment packet is commissioned alongside it. Add only the optional items actually admitted.
Archive transfer/queues, Owner response time and prospective operating effort are separate
unknowns; the direct-weather-only path has no validated total yet. No six-week release promise.

<a id="work-4-1"></a>

### 4.1 Historical archive admission; live suitability belongs to [4.9](#work-4-9)

Navigation: [index](#work-item-index) · [budget prerequisites](#section-4-b).

Prioritize NCAR GFS for a common historical grid and OCF ICON-EU for higher-resolution
crisis/modern sensitivity. §5.9 records documented dates; those are not admission verdicts.
Require a small decoded sample from the earliest required period, crisis, modern period
and both DST transitions, plus an inventory of all required runs/variables before full scoring.
Samples must cover required wind/radiation fields and **h22–h46 hour starts**, including
23/24/25-hour days and accumulation/interpolation endpoints (potentially **h48** on a
three-hour grid), not just h24. Each contributing step must have been released by the origin.
Audit historical model/grid/schema changes, conversions and coverage. Historical admission
requires an accessible archive and evidence that each input was available at its historical
forecast origin; a discontinued update service can still supply an admissible historical archive.
Missing historical evidence at the brief's deadline/16-hour stop yields NOT_ADMITTED for
that historical scope, with a gap list and [D5](#decision-d5) fallback decision. A supported live feed,
continued updates and historical-to-live equivalence are assessed for the selected policy
in [4.9](#work-4-9). Their absence blocks its live use, not an otherwise admissible historical experiment;
historical admission alone never certifies live suitability.

Record provider/model/version, init_time, documented dissemination and available_at,
valid_time, lead, retrieval time, content hash, source URL/retrieval date/source-text fingerprint,
units, grid/zone aggregation, wind height, radiation accumulation/averaging, interpolation and missingness. Use D−1 00 UTC only
when the required output was available before the inherited **11:00 UTC** origin
(12:00 fixed CET; delivery calendar Europe/Berlin). Initialization time is not publication.
Archive retrieval now is not proof of historical
operational publication; label reconstructed availability separately from contemporaneous evidence.
Reject later updates, retrospective hindcasts and stitched analyses as historical vintages.

Apply `max(2019-01-01,D−728 days)` and genuine pre-fold warm-up. First-evaluation training
starts are **2019-01-01 / 2019-04-04 / 2020-07-03 / 2023-05-04 / 2024-01-11**;
warm-up can move these earlier, except the 2019 floor. Resolve the D−1 weather-run offset
at the boundary without importing pre-2019 inputs. State storage/download volume,
local processing time, service limits and free-use/redistribution terms. Stop at 16 active
hours with an explicit gap list if admission cannot be established; Owner chooses §3.2.

<a id="work-4-2"></a>

### 4.2 v2 specification to freeze before fitting

Navigation: [index](#work-item-index) · [budget prerequisites](#section-4-b) · [economic contract](#section-4-e).

Proposed central forecast is `(A1.central+B2.central)/2`, with a **new**, consistently
scaled signed-error distribution; it is not an average of already calibrated p50s.
Use only issued errors from complete delivery days ≤D−2, consumed once. Predeclare
hour-aware pooling/shrinkage, residual units, 28-day window, small-sample fallback and
genuine pre-fold warm-up; 28 observations/hour do not establish accurate 2.5% tails.
Select those choices on training/inner-validation data, not against §5.5's oracle range.
Include **one otherwise identical pooled-residual control**: same central blend, units/scale,
28-day released-error history, warm-up, eligibility and quantile convention; vary only the
hour-aware pooling layer. Freeze both constructions before outer scoring and count both in
the brief's budget. This identifies the layer's contribution without an open-ended sweep.
Filter authorized partitions before materializing inputs: no spent holdout or reserved-tail
outcomes for fitting, tuning or selection. Preserve original eligible targets; missing forecasts
are reported failures, never grounds to shrink the scored population. Freeze warm-up failure
and missing-input fallback rules, quantile interpolation/ties and units/scale before replay.

Re-score B0/B1/B2/A1 and the final v2 emitted vectors under CP-15's seven-quantile WIS,
equal-fold normalization, common eligibility and fixed timezone contract. Preserve native
v1 nine-quantile pinball separately. B1 versus B0 fold-3 WIS **87.94 versus 51.73** uses
different comparator constructions: B1 preserves v1's calibrated/projected quantiles; B0
uses its rolling signed-error distribution. This is not native v1 pinball. Run availability
mutation/positive controls, state replay, DST/completeness and quantile-order checks.
Report original §8 criteria alongside any newly ratified bar. Its unchanged constraints include
per-fold 95% coverage [.90,.98], peak coverage ≥.90 with MAE/WIS no worse than matched best
B0–B3, every-fold MAE/WIS ≤1.05×best rolling B2/B3, and complete finite ordered issuance.
The diagnostic best-reference comparator is legitimate; no retrospective PASS is created.
No oracle score, hard-coded winning range or historically spent window can serve as completion evidence.

<a id="work-4-4"></a>

### 4.4 Weather/VRE experiment boundary

Navigation: [index](#work-item-index) · [budget prerequisites](#section-4-b).

<a id="work-4-4d"></a>

**[4.4D](#work-4-4d) first:** use admitted zonal wind/irradiance in a fixed same-policy ±direct-weather
paired ablation on identical inherited eligible rows. Freeze the feature recipe and count both
arms. Finish with measured point/interval effects, uncertainty, missing-input behavior and cost.
At that boundary stop unless the authorized protocol's predeclared result/cost rule justifies
an already admitted extension, or a new bounded VRE authorization supplies the rationale and
budget. No favorable gain is promised; a negative direct-weather result does not prove every
intermediate VRE representation useless.

<a id="work-4-4v"></a>

**[4.4V](#work-4-4v) only if admitted:** optionally predict onshore/offshore/solar generation from available
A75 actuals and form `residual_load_forecast = load_forecast − vre_forecast`. Audit label
coverage, release/revision semantics and capacity changes. Price-model training features must
be chronologically held-forward generation predictions; fitting generation on training-plus-test
history leaks. Only this admitted extension requires the direct-weather-versus-VRE comparison;
[4.4D](#work-4-4d) alone has no mandatory generation-model deliverable.

Freeze a missing-input fallback and all training-only transformations. The in-house forecast
has no measured recovery fraction of the **19.49%** A69 gain; do not invent one as a target.
Residual-load shape and fuel/EUA level are separate hypotheses. No redistributable TTF/THE
series is admitted by this plan; fuel work remains outside scope. Existing causal proxies
and historical load/cross-border feasibility findings remain controls/research leads.

<a id="candidate-constraints"></a>

### 4.5–4.8 Candidate and delivery constraints

<a id="work-4-5"></a>

Navigation: [index](#work-item-index) · [register](#record-4-5) · [budget prerequisites](#section-4-b).

Per-block LightGBM uses the exhaustive blocks in §3.1, with training-only capacity selection.
At full 728-day history, nominal counts are **5,824 night / 5,096 solar / 6,552 shoulder**
rows before eligibility/DST, versus **728** per hour; early folds have less. Current
**600 trees / 63 leaves** are not justified for smaller fits.
The old **~1,300 fits / 20–45 minutes**, versus **~10,700 fits / overnight** for 24 hours,
exclude tuning, warm-up and multiple policies: estimates, not measured budgets. Likewise
night MAE **21.88→~17.7** and S_MAE **0.784→0.73–0.75** assume half the gap closes;
no result is promised.

| Candidate / arm | Proposed disposition, subject to the authorized experiment |
|---|---|
| B0 / B1 | Permanent naive / immutable v1 replay references. |
| B2 / A1 | Retain: best single-arm S_MAE / strongest of this pair in crisis; proposed v2 inputs. |
| B3 / A2 | Retain as pooled controls and economic challengers; economic lead is decision-specific. |
| A4 | No new short-window build proposed; **0.76466** S_MAE is uncompetitive in the recorded experiment. |
| A3 / A5 | Preserve historical ensemble results; distinguish them from the proposed v2 policy. |
| DDNN, Johnson SU head | Named direct comparator to TabPFN in [4.6C](#work-4-6c), subject to its own research-permission, resource and output checks in [4.6L](#work-4-6l) / [4.6R](#work-4-6r) and [D4](#decision-d4) allowance. Freeze version, refit/ensemble schedule and quantile construction. No superiority or delivery compatibility is assumed; failed entry is reported, not replaced by another family. |
| TabPFN (2.5 is the currently named candidate; exact version/revision to be fixed) | Defined route [4.6L](#work-4-6l) → [4.6R](#work-4-6r) → [4.6C](#work-4-6c) → [4.7](#work-4-7). Research admission and delivery eligibility are separate. Identify the licence applying to the exact candidate, then test resources on training data only; if eligible, make one predefined comparison including DDNN and B2/A1. No family-wide licence inference, preferred winner or automatic version search. |
| Chronos-2 | Existing pinned probe (`29ec3766…`, full revision/hashes in CP-15 feasibility records) is not a benchmark. Pretraining overlap/cutoff is unverified; no assertion that 2022 is definitely included or later folds are clean. |
| NBEATSx | Defer for search-budget reasons; existing load is usable exogenous information, so weather is not a mathematical prerequisite. |
| QRA / controller / JEV | No build scheduled. Existing QRA/controller tests do not prove impossibility; reopen only through a bounded protocol. JEV's proposed categorical controller role adds no established value. |

The current LightGBM browser demonstration has a reported **~57 MB** first-visit budget
and bitwise artifact parity. DDNN/TabPFN do not inherit that implementation. Prove local
inference and choose an allowable delivery form before promotion; the Owner decides any
quality/browser tradeoff using a declared margin. A lookup does not waive model-output terms.

<a id="work-4-6l"></a>

### 4.6L Licence entry — exact candidate and exact uses

Navigation: [index](#work-item-index) · [budget prerequisites](#section-4-b).

This is a **future verification task**, not a licence determination. Identify the exact
TabPFN package/model version, weight revision and applicable licence text(s), with source
URL, licence version, retained text/fingerprint and check date. Do not transfer a conclusion
from one TabPFN version to the family. Identify the actual user/entity and research setup;
check DDNN's applicable implementation/weight terms separately for its entry disposition.

The use table records **permitted under stated conditions / not permitted / unresolved**,
with conditions and the source, licence version and check date for each row:

| Use to assess separately | Required scope |
|---|---|
| Research and local comparison | User eligibility and our precise local research/comparison use. |
| Retaining results | Predictions, metrics and research artifacts retained locally. |
| Publishing research findings | The proposed findings/output disclosure; no inference from permission to retain results. |
| Local prospective operation | Using predictions in the intended ongoing local operation. |
| Public demonstration | The actual demonstration and exposed outputs. |
| Hosted service | The proposed service and its users. |
| Product | The intended product use/distribution. |

If the research/comparison use or retention required for reproducible evidence is not
permitted or remains unresolved, stop before running that candidate. If research is
permitted but a delivery use is not permitted/unresolved, proceed only within the proven
research permissions. This is no authorization for operation or publication, including
publication of findings; carry each restriction forward to [4.7](#work-4-7)/[4.10](#work-4-10). At the bounded review
deadline, unresolved remains unresolved: no paid licence, commercial purchase, provider
negotiation or replacement-version search is presumed to resolve it.

<a id="work-4-6r"></a>

### 4.6R Resource entry — training data only

Navigation: [index](#work-item-index) · [budget prerequisites](#section-4-b).

For each research-admitted candidate, use only permitted training partitions, filtered before
materialization. Exclude evaluation-fold scores and holdout/reserved-tail outcomes entirely;
this is not model selection. Before running, the engineering brief fixes the representative
row/feature/history sizes and bounded checks, hardware/software configuration, allowed
compute/memory/storage, numeric pass thresholds and stop rules within [D4](#decision-d4) allowances.
No resource threshold or test size is approved by this rewrite.

Record peak memory (host and accelerator where used), load time, preparation/adaptation/fit
time and prediction time on that documented hardware at the intended representative scale.
Verify that the fixed output procedure can emit finite, ordered CP-15 quantiles and its
required point forecast p50; record the recipe and feasibility, not evaluation accuracy.
Finish with measured values versus thresholds and PASS/NOT_ADMITTED plus the cause for each
candidate. Exceeding a cap, failing a requirement or leaving feasibility unproved ends that
entry attempt. No evaluation-guided tuning, automatic larger machine or new variant follows.

<a id="work-4-6c"></a>

### 4.6C One predefined TabPFN–DDNN comparison with existing references

Navigation: [index](#work-item-index) · [budget prerequisites](#section-4-b) · [economic contract](#section-4-e).

After both candidates pass [4.6L](#work-4-6l) / [4.6R](#work-4-6r), execute **one bounded comparison** under the authorized
brief. It uses existing admissible information: new weather is not an entry requirement,
and neither this route nor a challenger result is required to complete v2. Before any
comparison run, freeze:

- Exact versions/revisions, configurations, seeds, ensembles, refit/output procedures and
  final selection/computation budgets for both candidates and references under [§4.B](#section-4-b).
- The same information available at each forecast origin, history windows and evaluation
  rows, retaining the 2019 floor and inherited causal/release rules. Selection, transformations
  and calibration use training/inner-validation data only. Document necessary representation
  and training differences; identical hyperparameters across architectures do not establish
  fairness. Do not shrink histories/rows for one candidate to conceal resource failure.
- B2 and A1 as existing references; include v2 only under a predeclared availability/identity
  rule. Its absence does not trigger a v2 build or block this comparison. Saved references
  must satisfy the same information/history/row contract, or require budgeted matched replay.
- Scoring of **actually emitted p50 and all seven CP-15 quantiles**
  **.025/.10/.25/.50/.75/.90/.975**: S_MAE and S_WIS with B0 fold normalization and
  **equal fold weights**, plus coverage, width and failures. Preserve eligible rows and
  predeclare missing/failed issuance handling; never substitute an internal loss/head for
  the emitted forecasts. Report original §8 and any applicable new bar without rewriting either.
- Total compute cost, peak memory and reproducibility artifacts; a paired uncertainty method
  for score differences preserving the temporal/fold structure. Fix the preference rule and
  uncertainty/tie treatment before running, including better S_MAE but worse S_WIS and the
  reverse. [D2](#decision-d2)/[D3](#decision-d3) own material quality/delivery tradeoffs; Engineering specifies the method
  within them. A tie, inconclusive result or no preferred candidate is a valid outcome.

“One comparison” may include all prescribed folds and the finite inner selection authorized
in advance. It permits **no further improvement rounds after evaluation scores**. Evidence
remains `development_post_selection`; all-fold completion does not make it confirmatory.
Stop at the first exhausted budget or protocol failure and retain partial evidence. If DDNN
fails entry, explicitly state that the direct TabPFN–DDNN comparison was **not completed**;
list only the reference comparisons actually performed under the predeclared fallback scope.
The same accounting applies if TabPFN fails entry. Neither an entry failure nor a negative
score opens a search over other versions or model families. Any optional [4.8](#work-4-8) work has its
own preauthorized protocol/budget and cannot reopen or relabel this comparison.
The separately bounded fresh-data test in [4.7T](#work-4-7t) reuses admitted fixed candidates for final
selection; it is not another development/tuning round or a relabelling of [4.6C](#work-4-6c) evidence.

<a id="work-4-7t"></a>

### 4.7T Candidate freeze and comparison on genuinely unused data

Navigation: [index](#work-item-index) · [budget prerequisites](#section-4-b) · [economic contract](#section-4-e).

Before final policy selection or full daily-system setup, freeze a finite manifest of
relevant existing models (B0/B1, B2/A1, available v2 and other justified retained controls)
and admitted V3 candidates. Include a direct TabPFN–DDNN contrast only when both pass
[4.6L](#work-4-6l) / [4.6R](#work-4-6r) for this exact use, scale and update policy; otherwise report the missing comparison
and the permitted comparisons actually made. Research permission does not grant live use.
Include matched information ablations needed to distinguish information from model effects
in this same finite manifest/budget; do not add arms after results. No automatic replacement.

Before test-outcome access, register exact versions/configurations, seeds/ensembles, initial
states, update schedules ([4.9O](#work-4-9o)), test start/end and fixed time blocks, targets/horizons,
metrics, selection/tie/uncertainty rules, budget and failure/stop rules. Reuse [4.6C](#work-4-6c)'s emitted
p50/seven-quantile S_MAE/S_WIS, coverage/width and preference contract, with equal weighting
of the new predeclared time blocks and matched B0 normalization. Do not reuse the old fold
dates as if new. Record any necessary scope-specific protocol completion before exposure;
leave historical §8 findings intact. No winner follows merely from a slightly lower mean.

Audit dataset/period identity, partition lineage, access and prior run/analysis records to
establish that the proposed outcomes have not been used for development, calibration,
selection **or inspection of results** by the project. Record the cutoff, attestations,
sources and gaps; recent download dates or being outside an old snapshot prove nothing.
The spent/embargoed/reserved partitions in §3.2 are not automatically available. If an
untouched accessible period cannot be demonstrated, return BLOCKED or, under a predefined
authorized collection protocol, await genuinely future observations; never silently use an
exposed period. This rewrite performs no data audit, retrieval or collection.

Run the frozen policies chronologically on identical forecast origins, targets, horizons
and eligible rows, using only input vintages and labels available at each origin. For direct
model contrasts, match the available information and history; disclose necessary representation
differences. When inputs differ, report that contrast as the combined information/model
effect and use the predeclared same-model ±information and same-information model contrasts
to separate contributions; absent those controls, do not attribute the gain to architecture.
Replay the intended daily context/state refresh and scheduled refits exactly, with released
labels consumed only after availability and once per permitted update. Test-period labels
may enter **later** updates only under this frozen chronological rule; they may never tune
the rule itself. This is sequential evaluation, not fitting on future test outcomes.

Report forecast quality, stability over the fixed subperiods, paired uncertainty, runtime,
peak memory, failures/delays and fallback use, retaining failed rows/days in the accounting.
Apply the existing predeclared preference rule, including mixed metric outcomes and no clear
winner. Stop on budget exhaustion, invalid chronology or independence breach and label any
partial/exposed evidence accurately. Retuning after test results spends that period: a changed
method requires a new frozen protocol and genuinely unused test period, with new authority
and budget, never an automatic continuation. Record [4.7T](#work-4-7t) separately from historical
`development_post_selection` evidence. Because it informs selection, it is not independent
confirmation of the selected policy and supplies **zero days** toward the post-final-freeze
live validation. Negative/blocked results can close research without launching a live system.

<a id="work-4-7"></a>

### 4.7 Report measured quality separately from delivery selection

Navigation: [index](#work-item-index) · [budget prerequisites](#section-4-b) · [economic contract](#section-4-e).

Use the admitted evidence and use table to report separately **(1) the best measured model
under the predefined rule, or an inconclusive/no-preference finding**, and **(2) the model
selected for delivery under licensing, resource and operational requirements, or none**.
Do not call an eligible substitute the quality winner when the comparison says otherwise,
and do not call a model a failure because one delivery use is unavailable. Missing direct
comparison evidence cannot support a TabPFN-versus-DDNN ranking. Label development findings
and fresh-test findings separately. For the live route, document the [4.7T](#work-4-7t) result, decision
rule, selected exact policy/update contract, rejected/deferred candidates and licence/resource
reasons **before** CP-17 final freeze; an inconclusive test need not yield a quality winner.
This decision is not live certification. Standalone v2 and negative research dispositions
can finish without [4.7T](#work-4-7t) or a final live-policy choice.

Only if both the measured results and the version-specific licence finding support it,
candidate content may say: “Under the predefined comparison, TabPFN showed [measured
advantage] over DDNN. We selected [model] for delivery because the tested TabPFN version's
licence does not permit [specific use] within this project. The selection reflects delivery
requirements; TabPFN's measured advantage remains in the comparison report.” If differences
are inconclusive, say so. If licence suitability is unresolved, say **“suitability has not
been established”**, not that the use is certainly prohibited. Carry these two findings and
their exact evidence/permission limits into [4.3C](#work-4-3c) and [4.10](#work-4-10); public release still requires both
the applicable permissions and Owner authorization. Complete the report even with a blocked
candidate or unresolved delivery choice; return the precise missing Owner decision without
new research or approval requests for routine details.

<a id="section-4-e"></a>

### 4.E Economic policy contract

[D1](#decision-d1)–[D3](#decision-d3) retain ownership of exposure, market resolution, external economic rationale and required
net surplus; descriptive economics remains a valid choice. The future brief must specify the
forecast functional/objective (conditional mean, median proxy or explicit risk objective),
cashflow direction, settlement cadence, bids/fills/imbalance assumptions, physical constraints,
efficiency, initial/terminal SOC, cycles, fees/degradation and other costs. Engineering must
freeze deterministic optimization tie-breaking, solver/version/tolerances, missing-input and
failed-issuance execution, aggregation/denominators (including zero/nonpositive perfect-foresight
value), paired uncertainty and fallback. No values are chosen here.

Hourly complete-day diagnostics in §5.6 do not establish quarter-hour, outage-inclusive
product value. Marginal quantiles are not a joint scenario distribution for intertemporal
risk optimization. Match the PF benchmark to each identical decision specification. No new
trading implementation is commissioned by this contract.

<a id="work-4-9o"></a>

### 4.9O Daily operating objective and per-model update contract

Navigation: [index](#work-item-index) · [budget prerequisites](#section-4-b).

Every day, acquire the inputs actually available by the frozen forecast-origin cutoff;
check schema, completeness, quality, vintage and freshness; perform only scheduled updates;
then generate, timestamp and durably save the scheduled forecast **before outcome revelation**.
Preserve input/feature hashes, model and state/context identity, issued p50/quantiles, runtime
and failure status. Later reconcile published targets and revisions with their available_at
timestamps for scoring and permitted future updates; never overwrite the issued forecast.
The inherited research origin is 11:00 UTC and delivery calendar Europe/Berlin; any different
operational schedule/horizon needs explicit resolution before [4.7T](#work-4-7t) and final freeze.

Daily issuance does not imply daily weight training. The brief must complete the following
per-model manifest before candidate freeze; these are proposed operating recipes, not new
facts about existing artifacts or already approved compute allowances:

| Model/policy, if admitted | Refit versus daily state/context action | Training/history and labels to freeze |
|---|---|---|
| B0/B1 and immutable v1 references | Daily forecast/input refresh; retain the pinned reference's refit and residual-state rules. Do not retrain immutable v1 weights. | Record the exact pinned numeric history/calibration windows and label-release delays; distinguish stored weight provenance from currently available inputs. Missing specifications block that reference's replay. |
| B2/A1; admitted block LightGBM or supervised V3 price model | Proposed daily scheduled refit on eligible history; daily input refresh and only prescribed residual-state updates. A different fixed cadence must be specified and tested before freeze if daily refits exceed allowance. | Proposed inherited rolling `max(2019-01-01,D−728 days)` history, filtered by availability; record target-release cutoff, warm-up and each calibration window. Direct model contrasts use the common history contract. |
| v2 combination and uncertainty layer | Components follow their fixed schedules; recompute blend daily, without relearning weights. Update residual state once per eligible released complete day. | [4.2](#work-4-2)'s 28-day residual window and errors from complete delivery days ≤D−2, also subject to actual availability; component histories as above. No fit to the current day's unrevealed error. |
| DDNN | Fix a numeric refit cadence and cold-start/warm-start recipe in the brief; daily inputs and prescribed residual-state refresh between fits. No unspecified online gradient steps. | Common admitted training history, label-release cutoff, warm-up and calibration windows; exact ensembles/seeds and fit cost included. Cadence is unresolved until the training-only resource check supports it. |
| TabPFN | Refresh the permitted labelled context and query inputs daily; context replacement is not weight retraining. Record whether the exact admitted implementation performs any adaptation/fit and, if so, its fixed cadence and cost. | Common admitted history and deterministic context construction/cap, available labels only; resource checks must support the intended scope. A context reduction must be disclosed in the comparison, never passed off as matched information. |
| Optional VRE model or recombination | Declare each upstream refit cadence separately from daily feature inference; frozen combiner weights stay fixed unless an update rule was explicitly admitted before the test. | Record generation/price label release and revision rules, upstream windows and causal generated-feature lineage; no assumed same-day labels. |

For **every** admitted model, replace unresolved manifest fields with numeric cadence
(or explicit no-refit), window/context size, label-availability rule and initialization before
[4.7T](#work-4-7t). Specify hardware, daily total runtime/memory/storage and per-stage limits for acquisition,
validation, preparation/refit, prediction and persistence; include finite retries and the
issuance deadline. No numbers are invented here as approved budgets. If these cannot be fixed
within [D4](#decision-d4), return a blocker before the test rather than discover a new policy during live use.

For missing/stale inputs, unavailable labels, time/memory exhaustion or failed fits, freeze
the exact action: skip an ineligible update, retain a last valid state only within its declared
staleness limit, issue the named admissible fallback by deadline, or record a failed issuance
if no valid fallback exists. Specify which condition chooses each action, retry cap and operator
escalation. Log late outputs as late; never backfill them as timely forecasts or exclude the
day. Replay these same rules in [4.7T](#work-4-7t). No daily refit, state update or context refresh promises
daily improvement; performance and stability are measured outcomes.

<a id="work-4-9"></a>

### 4.9 Final freeze, daily operation and prospective evaluation chain

Navigation: [index](#work-item-index) · [budget prerequisites](#section-4-b) · [economic contract](#section-4-e).

Finish admitted development, **including [4.8](#work-4-8) if admitted**, then candidate/protocol freeze
and **[4.7T](#work-4-7t) → final [4.7](#work-4-7) → CP-17 final freeze → CP-18 daily operation → CP-19 validation**.
Deferred development is recorded; no subsequent recombination inherits the chosen identity.
A qualified route follows the unchanged [anchor §§9–10](../../capstone_v21.md):

1. Ratified feasibility and final disposition identify one exact policy/evidence set. If none
   qualifies, close with the negative record and the authorized research/local handoff route.
2. CP-17 authority freezes code, input/feature contract, hyperparameters, update/fit schedule,
   delayed-error handling, initial state and failure policy. Register exact names, **numeric
   versions, run IDs, initialization and complete-artifact fingerprints**; verify cold-start replay.
   Freeze the policy/algorithm and [4.9O](#work-4-9o) update rules, not an eternally unchanged fitted state:
   prescribed refits, state transitions and input-context refreshes continue with saved lineage.
3. **Run start:** CP-18 requires **separate operational and publication authorization** to
   issue and record the frozen policy's forecasts and live scorecard. Before issuance, establish
   supported live access, timely availability, continuity and historical-to-live equivalence
   for its selected inputs, with the frozen fallback. Missing live suitability blocks this
   run, not [4.4](#work-4-4) historical research. Timestamp before target revelation; retain vintages,
   state hashes and lineage. Name the operator, monitoring metrics, allowed observations/
   updates, incident budget and staleness rules in advance. Starting is not validation.
4. Accumulate **≥90 consecutive delivery days after the final freeze**, from forecasts actually
   issued before outcomes were revealed, reporting failures, delays, outages and staleness.
   Neither [4.7T](#work-4-7t) replay nor its elapsed days substitutes for this record. Never drop difficult days. Prescribed
   state updates continue; discretionary retuning, policy changes or dashboard-driven champion
   selection cannot occur within confirmation. A policy/selection change requires a new final
   freeze and a new evaluation period. If [4.7T](#work-4-7t) is ever performed after an existing final freeze,
   changing the selected policy because of it cannot retain that earlier freeze or its clock.
5. **Validation finish:** before outcome access, the authorized evaluator resolves the exact
   registry versions and verifies fingerprints; wrong/missing versions or changed artifacts cause refusal, with
   positive controls. No moving alias/local fallback replaces that check. Under a complete
   ratified CP-19 bar and analysis protocol, produce the final positive/negative/blocked verdict.

Elapsed time is insufficient evidence. No prospective clock, freeze or stage authorization
starts in this rewrite. Publication and local artifacts remain separate at every stage.

<a id="section-5"></a>

## 5. Evidence ledger — verification and limitations

The [independent verification gate](v3-plan-independent-review-2026-09-22.md#verification-gate--pass)
used **10,747 original targets per policy**, folds **2,160/2,159/2,112/2,160/2,156**, without
extra filtering. Point loss uses emitted p50; seven-quantile WIS uses
**.025/.10/.25/.50/.75/.90/.975**, interval alpha .5/.2/.05, median weight .5, divisor 3.5.
Within each fold average losses, divide by that fold's B0 mean, then equally average five
ratios. Pooled-hour ratios and native v1 nine-quantile pinball are different estimands.
Gate **REPRODUCED**: **B0 1/1; B2 .65781/.63899; A1 .67229/.64602; A2 .77371/.73167**.
Original §8 aggregate limits remain **.59203/.57509**; A1 fails criteria 1, 2 and 5.

Labels attach to exact claims: **REPRODUCED** means a specified calculation/source matches;
**REPRODUCED WITH DEVIATION** means a named related variant differs; **NOT TESTED** means
missing recipe/evidence or no attempt; **NOT REPRODUCED** means an adequately specified
tested claim fails, or a source assertion is unsupported as explained. None certifies a
causal v2 outcome. Below, “original” means the historical author's claim, “revised” the
specified review experiment. All historical results here remain `development_post_selection`.
Full methods are in the independent review, particularly
[combinations/day switching](v3-plan-independent-review-2026-09-22.md#combinations-and-day-switching),
[battery/solver ties/bootstrap](v3-plan-independent-review-2026-09-22.md#battery-robust-caution-not-a-general-winning-model)
and [fixed-p50 and other recalculations](v3-plan-independent-review-2026-09-22.md#other-recalculations-and-inference-limits).
The earlier review's code appendix omits an explicit p50 reset and bootstrap implementation;
its prose numbers are supported by the independent durable methods, not by pretending that
appendix covers every calculation. No re-execution was done in this rewrite.

### 5.1 VRE publication — named routes verified; universal assertion unsupported

[SMARD](https://www.smard.de/page/en/wiki-article/5884/206318/forecast-data) states 18:00
submission/publication; [TenneT wind](https://netztransparenz.tennet.eu/electricity-market/transparency-pages/transparency-germany/network-figures/actual-and-forecast-wind-energy-feed-in)
states 08:00 estimation and 18:00 publication. These documented late routes support rejection
at the gate (**REPRODUCED**). The June n=1 absence at **15:35 CEST** is a historical report,
consistent but **NOT TESTED** by the independent review. “Any published feed” and “an 18:00
deadline proves no earlier publication” are **NOT REPRODUCED**. Withhold admission
without affirmative pre-gate evidence; do not generalize one control-area wind schedule
to every TSO/solar product. No polling is needed to reject the two documented routes.

### 5.2 Combination — specified optima reproduced; no information ceiling

Six-arm population throughout: **B1, B2, B3, A1, A2, A4**, using emitted p50 on the
original targets. Revised full-grid figures below are **REPRODUCED** by the independent
review. Original static/hour recipes are **NOT TESTED** as exact experiments; the declared
equal-fold optimum is a related variant **WITH DEVIATION** from their quoted numbers.

| S_MAE claim | Original | Revised specified calculation |
|---|---:|---:|
| A1 / six-arm mean | .67229 / .67136 | .67229 / .67136 |
| Static / per-fold / per-hour convex oracle | .63744 / .62472 / .63015 | **.63544 / .62472 / .62634** |
| Per-row discrete oracle | .33445 | .33445 |
| Fold×hour / per-row convex oracle | — | .60407 / **.27245** |
| A1+B2 emitted-vector 50/50 | .64466 in §5.3 | **.64466 S_MAE / .62002 S_WIS** |
| A1+B2 central mean, before new residuals | distinct policy | **.64070 S_MAE**, REPRODUCED, not causal v2 |
| Reduced-grid fixed / rolling QRA | .63487/.61383; .64590/.63423 | **NOT TESTED**; different grid, not full-grid v2 |
| Honest / leaky stacker | .85456 versus A1 .68350 / .52938 | **NOT TESTED**; exact recipe absent |
| Learned day/night weights | .66175 versus fixed .66020 | **NOT TESTED** |

Exact LP optimizes the equal-fold objective; pooled-MAE optimization gives .63742 static
and .63011 per-hour. This is a plausible provenance explanation, not proof of the unavailable
original code's objective. Restricted fixed partitions miss
**.59203**; arbitrary weighting is not bounded by them. A 28-day pooled QRA test does
not rule out per-hour half-year calibration; generating longer pre-fold forecasts costs work
but is not prohibited by a 90-day evaluation window. Never fit a meta-model on its scoring rows.

### 5.3 Day switching — revised statistics reproduced; original controller untested

A1/B2 MAE by fold: **6.820/6.219; 9.953/9.676; 51.213/54.008; 16.740/16.541;
19.482/19.203**. Oracle switches reproduce **.65138 per fold / .59919 per day /
.53055 per row**. A1 wins **227/448 = 50.67%**, crisis **53/88 = 60.23%**. Within-fold adjacent
**represented** days give lag **.07889** (443 pairs); restricting to consecutive calendar
dates gives **.08134** (442 pairs), mean run **2.14354**. These revised statistics are
**REPRODUCED**; versus original **50.7% / .078 / 2.16**, the specified variant is
**REPRODUCED WITH DEVIATION**.
The original logistic **42.8% versus 51.1%**, S_MAE **.69118 versus .66020**, is
**NOT TESTED** without its exact features. The earlier review's separate illustration reports
**51.67% versus 51.11%**; it was **NOT TESTED** by the independent review.
Low unconditional persistence does not prove conditional unpredictability; classifier accuracy also ignores loss magnitude. Defer on evidence/budget.

### 5.4 Disagreement — original recipe NOT TESTED; specified variant REPRODUCED

Author: MAE quintiles **5.90→50.05**, crisis correlation **.075**, elsewhere **.24–.31**;
width-driver S_WIS **.63425 versus .60691**, blending **~0.3%** improvement.
Revised explicit six-arm population SD versus A1 absolute error: **6.394→48.639** and correlations
**.41647/.07601/.00048/.25662/.20023**. Original population/error/driver fitting is
unspecified; the original quintile/correlation recipe and driver WIS/blend variants are
**NOT TESTED** as exact experiments. The revised SD variant is **REPRODUCED**, and is a
related calculation **WITH DEVIATION** from the historical figures. Do not install a
disagreement-based uncertainty rule from these numbers; reassess only with a changed arm set and frozen recipe.

### 5.5 Hour-aware intervals — mismatch and specified oracles reproduced

A1 width is constant within a day to <1.8e−13. Author pooled width **134.325 EUR/MWh**
becomes **134.32455–134.42098** across hour-specific means because denominators differ.
Night 00–05 coverage **.993–.998**, MAE **9.2–13.7**, versus hours 12–15 coverage
**.866–.888**, MAE **26.9–28.2**, reproduce: the structured mismatch is real.

Author A1 oracle WIS **.64602→.61009**; review fixed-p50 raw-residual-tail oracle
**.61048**. Within fold/hour, take linear quantiles of raw signed `y-emitted_p50`,
add to emitted p50, and explicitly keep the .5 column fixed. The revised result is
**REPRODUCED**; the original .61009 recipe is **NOT TESTED** as an exact experiment,
with the related fixed-p50 variant **WITH DEVIATION**. Original expanding cold-start causal
**.63793** is **NOT TESTED**.
Four-component emitted mean A1/A3/A5/B2: point **.64280** reproduces; author oracle
WIS **.58927** (**NOT TESTED** original recipe), revised fixed-p50 **.58936**
(**REPRODUCED** specified variant, **WITH DEVIATION** from original).
Author criterion-5 pass on all five folds is
**NOT TESTED** for the original construction. These use evaluation residuals.

The predicted causal landing interval **.589–.638** and claimed **~2.4%** interval-only
opportunity are unverified expectations, not bounds or pass criteria. No particular causal
score proves leakage; inspect lineage and controls. Re-estimating the residual median also
changes S_MAE, so this is not automatically an interval-only intervention.

### 5.6 Battery — original exact experiment NOT TESTED; specified sensitivities reproduced

1 MW / 2 MWh, 90% round-trip efficiency. Review uses symmetric efficiency, empty daily
start/end and **444 complete days**; original SOC/cycle/missing-day details are unspecified.
This is a conditional complete-day economic sample, separate from statistical scores on all
10,747 original rows. Revised sensitivities are **REPRODUCED**, except B0 **WITH DEVIATION**;
they are related experiments **WITH DEVIATION** from the underspecified original table.

| Policy | Author EUR/day / PF capture % | Review closure-only EUR/day / equal-fold capture % |
|---|---|---|
| Perfect foresight | 253.91 / 100 | 251.85 / 100 |
| B0 | 223.12 / 86.4 | 221.86 / 86.56 |
| A1 | 226.49 / 88.1 | 224.85 / 88.11 |
| B2 | 228.66 / 89.7 | 226.59 / 89.59 |
| B3 | 229.89 / 90.7 | 228.15 / 90.64 |
| A1+B2 | 232.28 / 90.8 | 230.29 / 90.71 |
| A2 | 233.83 / 91.4 | 232.10 / 91.45 |

B0 closure **221.86398** in the cumulative-state LP versus **221.90379** in the independent
explicit-state LP reflects equal forecast-objective dispatch ties, not a revenue-formula failure.
Fourteen days differ; objectives agree within 1.2e−13. Non-closure B0 differences were not
individually tie-audited. A deterministic tie policy is therefore a future brief requirement.

Author **13.6 percentage points** naive-to-PF spread depends on its aggregation; displayed
EUR/day ratios differ from displayed percentages. Closure-only permits ~2 cycles/day and
simultaneous charging/discharging at negative prices. A one-equivalent-cycle cap gives
**A2 179.97 / blend 178.38 / B2 175.37 / PF 200.01 EUR/day**. Adding illustrative
€10/grid-MWh throughput cost and exclusive modes gives equal-fold capture **A2 75.46% /
blend 77.71% / B2 77.17%**, although A2 retains the largest pooled EUR/day of the three.
The fixed-strike illustration **buys at the hourly price and resells/offsets exposure at €50**:
`(50-y)*I(p50<50)`, averaged over all original target hours, gives **A1 6.85 / B2 6.82 /
A2 6.31 / blend 6.87 EUR/target-hour** (**REPRODUCED**). It is a median-threshold proxy,
not generally an expected-profit optimum. These are sensitivities, not chosen
product economics. Perfect execution, price-taking, daily reset and hourly aggregation
remain limitations; no generalized economic winner, representative annual value or
preregistered confidence claim is established. An exploratory 95% paired 7-day block
interval for closure-only A2−blend is **[−.486,4.292] EUR/day**, point **+1.806**, including
zero (**REPRODUCED**). Recipe: seed 15042, 2,000 replicates; sample noncircular 7-date blocks
within each fold's full 90-date calendar, concatenate/truncate to 90, preserve missing dates
as NaN, then pool represented paired days. It is exploratory post-selection uncertainty,
not a confirmatory superiority test. €30 sensitivity and €10 bootstrap were not independently
retested. See §3.1's intact contamination disclosure; this CI does not cure threshold selection.

### 5.7 Architecture / block deficit — REPRODUCED

Source confirms 24 hourly LEAR regressions versus one pooled LightGBM with **23** features.
B3/B2 block MAE ratios: author **1.627 / 1.173 / 1.133**; review
**1.626536 / 1.172716 / 1.133081**, over **3,579 / 4,032 / 3,136** hours.
Approximate A1/B2 error shares **22% night / 40% shoulder / 38% solar** motivate diagnosis,
not a promise of recoverable error. More or fewer models are hypotheses to test.

### 5.8 Level / shape and A69 — REPRODUCED WITH DEVIATION

A1 daily level MAE reproduces **5.634 / 7.402 / 41.621 / 9.258 / 14.404**.
Author shape **4.833 / 6.967 / 35.484 / 15.531 / 14.952** reproduces with equal-day
weighting; protocol hourly weighting gives **4.833 / 6.965 / 35.484 / 15.531 / 14.936**.
Level/shape MAEs are not additive, and shape error alone does not identify VRE as its cause.

A69 benchmark **REPRODUCED**: pooled nine-quantile raw pinball
**13.01584151→10.47871463 (19.49260734%)**; raw p50 MAE
**41.75983236→29.93830428**. This is a v1 post-gate feature-bundle comparison: base versus
base+A69 wind-onshore,
wind-offshore, solar, total VRE, residual-load forecast and Dunkelflaute flag. Both arms have
10,747 ordered fold/date/truth rows, but the A69 artifact alone lacks hourly timestamps for
independent hourly-key lineage certification. Average over all rows and nine raw quantiles
**.025/.05/.10/.25/.50/.75/.90/.95/.975**, not CP-15's equal-fold seven-quantile WIS.
Fold 2 pinball worsens **5.92946717→6.08276822**; pooled gain is not every-fold gain.
Transfer to normalized CP-15 S_MAE or in-house VRE improvement is **NOT TESTED**.

### 5.9 Archives — documentary dates REPRODUCED; full admission NOT TESTED

| Specific archive | Documented depth / limitation |
|---|---|
| [NCAR GFS 0.25°](https://gdex.ucar.edu/datasets/d084001/) | Operational runs from **2015-01-15**, plausible all-fold depth. Source warns NCAR updating stops early 2026 and points to AWS. Its conflicting future upper timestamp is not continuation proof; field/lead/publication admission still needs [4.1](#work-4-1). |
| [OCF ICON-EU](https://huggingface.co/datasets/openclimatefix/dwd-icon-eu) | **2020-01-01**, early subset of wind/radiation fields; schema changes March 2023; gated free access, archive no longer updated. Crisis-depth candidate. |
| [OCF ICON-Global](https://huggingface.co/datasets/openclimatefix/dwd-icon-global) | **March 2023**; too late for crisis training. |
| [Dynamical GFS](https://dynamical.org/catalog/noaa-gfs-forecast/) / [ICON-EU](https://dynamical.org/catalog/dwd-icon-eu-forecast-5-day/) | **2021-05-01 / 2026-02-10**; historical OCF continuity cannot be inferred from a replacement-service link. |
| [Open-Meteo Historical Forecast](https://open-meteo.com/en/docs/historical-forecast-api) | Stitched short-lead series, not the required D−1 run; GFS 2021-03-23 and ICON-family 2022-11-24 dates do not prove admission. |
| [Open-Meteo Single Runs](https://open-meteo.com/en/docs/single-runs-api) / [Previous Runs](https://open-meteo.com/en/docs/previous-runs-api) | Single IFS HRES **2024-03-14** (early coverage described as hindcasts), others **2026-04-02**. Fixed-offset runs mostly Jan 2024, with GFS temperature March 2021 and JMA 2018 exceptions; audit variables and origin semantics. |

Documentary dates above were checked by the independent review on **2026-09-22**. The NCAR
warning and [Dynamical migration notice](https://dynamical.org/migration-2026/) were rechecked
for this rewrite on that date. Dynamical asks users to plan for **September 30, 2026**, with
legacy URLs turned off dataset by dataset over following months; supported access resolves
STAC/Icechunk repositories. This is phased access migration, **not universal data deletion**,
and it does not recover OCF history by implication. Future admission records source-text
fingerprints for historical admission ([4.1](#work-4-1)); selected-source live continuity and equivalence
must be verified for [4.9](#work-4-9), not inferred from these summaries or imposed on historical research.

The old universal “archives start around 2021” source assertion is **NOT REPRODUCED** because
NCAR/OCF documentation explicitly predates it. Corrected dates are **REPRODUCED as documentation**.
**Historical depth is plausible, not closed negatively; no fold is yet declared admitted.**
Reanalysis and retrospective hindcasts are not as-issued forecasts. Keep primary-source
citations, inventory and sample decoding in the future admission dossier.

<a id="section-6"></a>

## 6. Local handoff and historical disclosures

The selected route ends with local content/artifacts, reproduction instructions, claim-to-evidence
links, data/model notices and a review/disposition record. A research bundle may point to
existing runnable CP-15 artifacts; it need not manufacture a new model. The record names
positive, negative or blocked results, withheld product claims and every deferred item
([4.1](#work-4-1)/[4.4](#work-4-4) weather, [4.5](#work-4-5)/[4.6](#work-4-6) challengers, [4.7T](#work-4-7t) fresh-data test, [4.8](#work-4-8) recombination or [4.9](#work-4-9) qualification as applicable),
with its reason and reopening dependency. No losing model forces another search. No feasible
candidate means no qualified product, but the authorized research handoff can still finish.
For [4.6](#work-4-6), carry [4.7](#work-4-7)'s measured-quality finding separately from delivery selection, the exact
version/use-permission table and any uncompleted direct comparison into that handoff. Retain
or release only artifacts/findings permitted by the applicable use rows; research admission
alone grants neither prospective-operation nor public-release permission.

Owner landing, commit, public release and confirmation of publication are separate actions.
Local completion does not claim they happened or wait indefinitely for them. Preserve v1
as historical fallback; a proposed candidate does not silently replace its surfaces.

Use [CP-15 landing](cp-15-landing.md) in this checkout, not a removed sibling path. Its
historical publication authorization grants none here. Keep B2/A1 references, demonstrated
historical availability, criteria before new experiments, the 2019 floor and post-selection
labels. The reviews explain why archive/switching/combination evidence cannot support
universal closure.

Q&A is outside this task. Owner-reported **30 entries, next 31** remains attributed and
unverified; numbering/Word-resave work and content are untouched. For factual accuracy in
this plan only: **τ=.5 mean pinball is MAE/2**, with the same minimizer as MAE. The historical
shrinkage diagnosis (**61.3%** above training p99, **2.45%** above training maximum) remains
reported evidence, not a newly verified result. The historical **67,343-row** feature repair
versus **2,160-row (3.2%)** truncated-history check remains a material scope distinction.
The prior **95.83%** leaking-row lesson motivates causal-semantic checks, not new validation
of this plan. These disclosures do not open a maintenance work queue. Only the Orchestrator
can later decide whether to capture the named interview-answer trigger; this task files none.
