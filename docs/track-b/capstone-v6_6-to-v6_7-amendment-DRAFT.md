# DRAFT v3 — capstone v6.6 → v6.7 scope and governance reduction

**STATUS: DRAFT PROPOSAL. NOT RATIFIED. NOTHING APPLIED.**

## Executive judgment

Draft v2 was careful, but it did not go far enough. It removed several visible chores while
preserving the systems that created most of them: the 38-coefficient A75 climatology, four matched
feature catalogs, exact Decimal adjudication, catalog-identity artifacts, repeated component
Critics, five future checkpoints, raw-second clock accounting, and a syllabus-derived calendar.
Replacing the Blind Critic with the Integration Critic would have saved one review while retaining
almost the whole dependency tree.

This draft takes the stronger position:

1. **Track A becomes an optional library, not a track on the critical path.** No syllabus block,
   month gate, NotebookLM verdict, SQL exercise, algorithm quota, or learning deliverable may block
   Track B, Track C, an application, or a release.
2. **The champion catalog is fixed and simple.** Remove A75, the synthetic VRE climatology, both
   proxy arms, the four-catalog experiment, and all selection/blinding machinery. Preserve the
   owner-requested A69 benchmark as one raw-head comparison and one number.
3. **Measurements describe the artifact; they do not decide whether it may exist.** DM significance,
   coverage, runtime, and feature importance are reported honestly. An unfavorable result changes
   the conclusion and limitations, not the checkpoint status.
4. **Five future checkpoints become three.** Data → model and analysis → release. The former M2/M3
   split and M4/M5 split no longer protect a live dependency after the selection and forward-audit
   machinery is removed.
5. **One independent review per checkpoint.** The Lead may build directly or delegate at its
   discretion. One fresh Integration Critic reviews the final candidate from a clean detached
   checkout. Component-verdict choreography, surface declarations, staleness bookkeeping,
   workbench ceremony, provenance declarations, and raw-second accounting are retired.

The governing test for every retained obligation is:

> Retain it only if it (a) prevents a plausible silent correctness or leakage failure, (b) is
> necessary to reproduce the released artifact, or (c) is directly visible and valuable to a Data
> Science hiring manager. Otherwise delete it, or make it optional and non-gating.

This is a portfolio project, not a regulated production service or a clinical confirmatory study.
The plan should protect scientific honesty and artifact quality; it should not simulate an
enterprise change-control system around a solo build.

---

## Owner decisions this amendment records

These decisions are inputs to the amendment, not questions for the executor to reopen:

- **A65/A01 pre-gate availability is assumed** from Regulation 543/2013 Art. 6(2)(b), corroborated
  but not empirically demonstrated by the 2026-06-12 observation. The assumption is disclosed.
- **The syllabus is optional.** `syllabus_v3_2.md` remains a useful curriculum and NotebookLM input,
  but no part of it gates the capstone, applications, or any other work.
- **The A69 information benchmark stays, but is trimmed** to one raw-head comparison and one
  headline number.
- **The project optimizes for a finished, honest, recruiter-visible artifact.** It does not optimize
  for procedural proof that every agent handoff was pristine.

---

## Application scope

Applying this sheet requires one owner-authorized, task-scoped suspension of the Governance
Lockdown naming the following **six existing locked files**, authorizing promotion of this draft to
the final amendment record, and stating the objective “apply the ratified v6.7 scope and governance
reduction atomically”:

| # | Locked file | Why it changes |
|---|---|---|
| 1 | `capstone_V6_6.md` | product scope, methodology, milestones, and checkpoint bars |
| 2 | `engineering-role.md` | collapse the Gauntlet to one final independent review |
| 3 | `docs/track-b/gauntlet-templates.md` | replace the ten-form protocol with a short brief, verdict, return, and receipt |
| 4 | `orchestrator-role.md` | make Track A optional and adopt the three-checkpoint flow |
| 5 | `program-stage-sequence.md` | rebuild v7 as a capstone-first v8 map with an optional learning sidecar |
| 6 | `docs/track-b/rule-inventory.md` | retire eliminated rules and record the new live inventory |

The suspension does **not** need to name `AGENTS.md`, `CLAUDE.md`, `notebooklm-role.md`,
`syllabus_v3_2.md`, or `docs/track-b/cp-0-defects.md`; this amendment deliberately leaves them
unchanged. The root publication, `main`, local-branch, evidence-retention, tag-before-delete, and
Builder ≠ Critic protections remain compatible with the leaner loop.

Directly necessary non-locked consistency edits in the later application task:

- `README.md`
- `progress.md` (Orchestrator operational state)
- `aws-extension-spec_v1_1.md`
- `pyproject.toml`
- removal of the inactive `src/pit_capture/` and `tests/pit_capture/` trees after the existing
  `evidence/cp-0` tag is verified

On ratification, this draft should be promoted to the repository's normal amendment-record name,
`capstone_V6_6-to-V6_7-amendments.md`, as part of the same coherent application task. Until then,
only this draft exists and nothing below is operative.

---

## AMD-0 — Make the syllabus genuinely optional, not merely labelled optional

`progress.md` already records the owner's decision, but the live Orchestrator contract and the stage
map still require the syllabus at session start, route every session toward the next syllabus topic,
enforce G0–G5 learning gates, make SQL-B a prerequisite for applications, and define the program
goal by completion of a ~729-hour curriculum. That is a semantic contradiction, not harmless stale
wording.

### `orchestrator-role.md`

1. **Startup read.** Remove the syllabus from the mandatory first-session read order. Read it only
   when Yarden explicitly requests a learning block or when a concrete capstone task needs a theory
   refresher.
2. **Track definition.** Define Track A as an optional, on-demand resource. It has no current
   position, next-due topic, schedule, monthly gate, or completion obligation unless Yarden chooses
   to run a specific block.
3. **No interleave contract.** Delete the mandatory “How Tracks A and B interleave” schedule and all
   statements that locate M1–M5 inside syllabus months. Track B advances only by CP-1 → CP-2 → CP-3.
4. **Type L survives as a utility.** A requested learning brief may still cite the syllabus, use a
   depth label, and ask NotebookLM for a deliverable. Remove mandatory checkpoint flags,
   consolidation verdicts, and “the syllabus is taught in full” behavior.
5. **Session lifecycle.** Delete the Track-A carry-forward status line and learning-checkpoint
   exception. Optional learning is recorded only when it materially affects current plans.
6. **Track C independence.** Delete the SQL-B/G3 and Month-5 application gates. M2 remains a useful
   suggested portfolio trigger for stronger outreach, not permission to apply. Active applications
   may begin whenever Yarden chooses.
7. **Progress skeleton.** Track A appears only while an optional block is active; the mandatory
   durable positions are Track B and Track C. No “next pending Track A checkpoint” exists.
8. **Routing.** Replace “does this move him toward the next syllabus topic?” with “does this advance
   the current capstone/release goal, the job search, or an optional gap Yarden chose to close?”
9. **Goal.** Delete the ~729/~753-hour program target and February/April curriculum projections.
   The goal becomes shipping the flagship through CP-3 and using optional learning/companion/cloud
   work only when its value is separately chosen.

Current edit sites include `orchestrator-role.md` lines 16–26, 46–119, 121–140, 148–161,
263–297, 342–350, 378–421, and 430–442. Edit by semantic anchor, not by stale line number.

### `program-stage-sequence.md`

Rebuild the document as **v8**, rather than patching twelve rows in a syllabus-first v7 map:

- Main table: M1/CP-1 → M2/CP-2 → M3/CP-3, plus only the manual prerequisites and Track C actions
  that actually serve those stages.
- Optional learning sidecar: syllabus topics indexed by the capstone task they can help with. They
  are suggestions, can be taken in any useful order, and never sit between two Track B rows.
- Retire G0–G4 learning gates, the SQL-B application gate, algorithm quotas, monthly consolidation
  verdicts, curriculum calendar projections, and the total-program hour envelope.
- Retire the automatic DEC-AWS ballot and automatic companion launch. Both become separate future
  projects requiring a new explicit owner instruction after the flagship ships.
- Preserve already completed history only as a short note. The map is for routing forward work, not
  proving that every old syllabus row still has a home.

### Files deliberately unchanged

`syllabus_v3_2.md` remains a coherent optional curriculum. `notebooklm-role.md` remains the contract
for a voluntary teaching session; its checkpoint behavior simply never fires unless a future prompt
explicitly requests it. Editing either file would spend governance effort without changing the
critical path.

---

## AMD-1 — Cancel point-in-time capture and remove its inactive implementation

### Claim that survives

Use this wording consistently in §3, §5.2, R-2, the README limitations, and the final report:

> A65/A01 pre-gate availability is an explicit assumption based on Regulation 543/2013
> Art. 6(2)(b), corroborated but not empirically demonstrated by the 2026-06-12 observation. The
> archived vector was unchanged from 15:35 CEST D-1 through post-delivery on the one sampled day
> (n=1, `revisionNumber=1`), which supports archive stability only and says nothing about pre-gate
> availability.

Never describe the assumption as spike-confirmed, measured, proven, or empirically established.

### Capstone edits

- Delete §3's capture contract, ledger schema, and “observed available by” protocol.
- Delete B-Man-PIT and every live prerequisite, gate, reading-order item, risk statement, and
  checkpoint item that depends on the ledger.
- Keep M0.5/CP-0 as one short **historical** paragraph: executed, landed, tagged, and later retired
  when its underlying requirement was cancelled. Do not preserve its seven-item live checklist in
  the current plan.
- Re-tense the v6.4/v6.5 delta paragraphs as superseded historical decisions.
- Remove the separate CP-1 “feed exists/recent 30 days” probe. A successful required bulk pull is
  already the stronger test; do not test existence and then immediately test it again by ingesting
  the same feed.

### Repository cleanup during application

After verifying `evidence/cp-0` resolves and preserves the reviewed candidate chain:

- delete `src/pit_capture/` and `tests/pit_capture/` from the active tree;
- remove `src/pit_capture` from the Hatch package list in `pyproject.toml`;
- retain the CP-0 verdicts, disposition tags, `docs/spike-feed-status.md`, and
  `docs/pit-metadata-investigation.md` as historical evidence.

Dead implementation is not evidence preservation. The tag and verdicts preserve the evidence; the
unused package only makes the repository look as if capture is still supported.

---

## AMD-2 — Remove the synthetic VRE proxy and four-catalog selection system

This is the largest substantive cut and the main correction to draft v2.

### Why it goes

The current design fetches A75 actual generation, fits a 38-coefficient seasonal-diurnal OLS model
inside every fold, persists fit lineage, creates two proxy features, trains a full 2×2 catalog
experiment, specifies exact Decimal/CSV/JSON canonicalization, commits identity manifests, and then
adds special criticism and adjudication. All of that exists to decide whether a synthetic expectation
of renewable output adds value to a champion that cannot use the real delivery-day VRE forecast.

The likely hiring signal is smaller than the system built to defend it. The cleaner scientific
choice is to omit the weak proxy from the champion and show, once, what the unavailable real
information would have changed.

### Replacement design

The champion feature catalog is frozen in the plan before fitting:

- calendar and static regime features;
- A65/A01 day-ahead load forecast;
- lagged day-ahead prices and closed-left rolling price statistics.

Delivery-day A69 and all derivatives remain forbidden in the champion. A69 is used only in the
trimmed §7.2 benchmark and, where useful, as a post-hoc evaluation stratum. Actual-load and
actual-generation feeds are not required pipeline inputs.

### Required deletions and rewrites

- §0 item 3: remove the optional gas browser re-check and all claims that a proxy may carry the
  merit-order signal. Gas stays omitted; the A69 benchmark is the only quantified counterfactual.
- §0 item 5: keep “external weather omitted because the load forecast embeds weather”; delete the
  A75 climatology and conditional proxy language.
- §3/§4: remove A75/A65-A16/A74 requirements, the optional EUA row/feature, both proxy features, and
  every runtime/fitting obligation attached to actual generation.
- §4.1: delete the OLS basis, proxy definitions, four catalogs, retention thresholds, Decimal
  comparisons, canonical CSV/JSON contracts, selection declaration, and independence split.
  Replace the whole section with a short “fixed strict-gate catalog” section.
- §5.1/§5.2/§6.1/§8.1/§9.1/§11/§13: remove proxy refits, A75 fit lineage, conditional champion
  packaging, proxy-selection narratives, and candidate-stage interview answers.
- §9.4: replace the current combined schema-and-fit-lineage invariant with a simple schema firewall:
  champion inference rejects A69-derived and actual-value columns; the benchmark admits only the
  named A69 additions.
- CP-1: delete A75 depth, fit-lineage, standardization, proxy, and independent poisoning-oracle
  requirements.
- CP-2: delete the catalog-selection gate, selection artifacts, blind review, and deterministic
  adjudication. The model is compared only with the three stated baselines.
- All role/template/rule-inventory references to a CP-2 blind/four-catalog surface disappear; there
  is no replacement surface because there is no longer a selection decision to police.

**Scientific cost, stated plainly:** the champion no longer tests whether a calendar-derived VRE
expectation improves pre-gate prediction. That possible feature is abandoned. In return, the shipped
model has a much smaller leakage surface and the report retains the more interpretable question:
how much does the real, but post-gate, A69 information improve raw quantile loss?

---

## AMD-3 — Keep §7.2 as one run and one number

**Owner decision, 2026-09-06:** preserve the benchmark as an interview answer; do not carry a second
calibrated model through the project.

- Strict arm: frozen fixed champion catalog.
- Augmented arm: identical folds, rows, seeds, hyperparameters, and training budget, plus
  delivery-day A69 and its named derivatives.
- Run on raw quantile heads before CQR/isotonic.
- Report exactly one headline: pooled mean pinball loss across nine quantiles and five folds,
  expressed as the percentage difference between arms.
- Median MAE may be included only if it comes free from the same stored predictions.
- Do not report coverage, interval width, or calibration error for an uncalibrated comparison.
- The benchmark is never calibrated, registered, deployed, or eligible to replace the champion.

Required limitation:

> This uncalibrated raw-head comparison isolates the information content of post-gate A69. It makes
> no claim about calibrated interval quality and does not make A69 available at the forecast gate.

Update §7.2, §10, the model/benchmark schema invariant, the combined model checkpoint, the release
page, README, and §13 to the same one-number claim.

---

## AMD-4 — Make empirical outcomes reporting obligations, not completion gates

The current plan can permanently block a correct and honest portfolio artifact because the data did
not produce a preferred result. That confuses research outcome with engineering validity.

- CP-2's Fold-5/pooled DM significance rule becomes a reporting protocol. Report statistic,
  p-value, effect size, comparator, and `development_post_selection`; do not require `p<0.05` to
  proceed.
- The ≥15% pinball improvement remains a narrative target only.
- CP-3's “80% coverage within ±5 pp on 4 of 5 folds” becomes a prominently reported diagnostic, not
  a pass/fail threshold.
- Remove the automatic EnbPI remediation reopen at >10 pp divergence. A miss is shown and discussed;
  it does not silently create a second calibration project.
- SHAP ranking/overlap and regime differences are observations. Require the plots/tables and honest
  interpretation, never a preferred rank, overlap, or direction.
- Training/render/load durations are measured and reported where useful, but exact laptop/network
  timings do not block release unless the artifact is functionally unusable.

**Scientific cost:** v6.7 may ship a negative result — a model that does not significantly beat the
naïve comparator or whose intervals miss nominal coverage on some folds. That is not a defect if the
pipeline is correct and the conclusion is honest. Fabricating a favorable gate or endlessly tuning
until it passes would be the scientific defect.

---

## AMD-5 — Remove the forward confirmatory audit in full

Delete §7.1's future-window audit, power calculation, quarantine, `selection_cutoff`, audit manifest,
`PENDING_UNDERPOWERED` / `CONFIRMED` / `NOT_CONFIRMED`, pre-registration, and all dependent fields,
checklist items, reading-order entries, README claims, and interview language.

Keep one clear evidence label:

> All reported model-comparison results are development-stage, post-selection descriptive evidence
> on the five pinned walk-forward folds. No separate confirmatory out-of-sample test was performed.

**Scientific cost:** the project makes no confirmatory-superiority claim. Reconstructing one later
would require a new model version and genuinely untouched future data. That is acceptable because
the artifact's claim is methodological competence and honest evaluation, not a publishable causal or
confirmatory result.

---

## AMD-6 — Delete the offline data/output-health report

Delete §9.5 and all M4/M5, reading-order, limitation, risk, syllabus-map, README, and AWS-proposal
dependencies. It cannot measure accuracy drift without labels and it exists only to imitate an
operations surface the project explicitly says it is not building.

The released artifact keeps ordinary input validation and schema tests. It does not produce PSI,
freshness dashboards, interval-width alerts, or monitoring colors.

Expected direct saving: the plan's own ≤8 h implementation allowance, plus future rendering and
maintenance.

---

## AMD-7 — Trim spectral EDA to three figures and one paragraph

Keep the part that is visible and differentiated by Yarden's signal-processing background:

- Welch periodogram with 24 h / 168 h / 12 h labels;
- per-regime spectral overlay;
- ACF cross-check;
- one 3–4 sentence interpretation paragraph using “confirms/justifies,” never “proves.”

Delete the standalone-module requirement, `<60s` gate, FFT-bin unit-test gate, optional MSTL,
dependency policing, and overrun-escalation protocol. Budget becomes a non-binding estimate of
~3 h. Collapse the three current CP-1 spectral checkboxes into one.

---

## AMD-8 — Keep DuckDB as a visible SQL artifact, not a second production path

Keep 3–4 hand-authored DuckDB queries against the committed Parquet: lag-24/168, rolling windows,
and null/duplicate/full-bin checks. They must be committed and runnable.

Delete the requirement that DuckDB be the canonical feature source consumed by the model and delete
the duplicate invariant suite on SQL-built columns. The Python feature pipeline remains canonical.
SQL-B is optional learning/interview practice and has no deadline, capstone gate, application gate,
or program-hours allocation.

---

## AMD-9 — Simplify the released artifact and remove recurring maintenance

Preserve the recruiter-visible shape: a static GitHub Pages report as the primary URL, a small
interactive marimo Space as the optional deep dive, a public MLflow experiment trace, and a
reproducible repository.

Remove the machinery around it:

1. **No precomputed multidimensional slider/SHAP grid and no per-cell nearest-neighbor OOD flags.**
   Keep the quantile-level selector and at most one simple load-forecast scenario control. Use direct
   local LightGBM inference or a one-dimensional lookup. SHAP remains a static diagnostic. State once
   that scenario perturbations are sensitivity probes and may be out of distribution.
2. **Bundle the champion in the image.** DagsHub MLflow remains public experiment evidence, but the
   deployed Space does not attempt registry-first loading and does not need a DagsHub secret/fallback
   dual path.
3. **Frozen release, not weekly service.** Delete the Monday snapshot/re-export/commit procedure,
   ≤48 h freshness smoke gate, and all recurring-refresh language. The page states the training and
   snapshot cutoff. A future manual refresh is permitted but never scheduled or required.
4. **No external-reviewer dependency.** The stranger test becomes optional user feedback, not a
   checkpoint gate. Delete the technical/non-technical reviewer recruitment block.
5. **No brittle timing gate.** Verify that Pages is static and has no runtime calls and that both
   Pages and Space render without broken assets. Record observed load time if useful; do not fail a
   release on `<3s`, `<5s`, `<10s`, or `≤30s` platform/network thresholds.
6. **Marketing is outside the engineering bar.** CV and LinkedIn updates are optional Track C
   actions after release, never CP criteria.

This keeps the parts a recruiter can see while removing the dual-load path, combinatorial lookup,
ongoing update obligation, external-human dependency, and network-speed lottery.

---

## AMD-10 — Replace five future milestones/checkpoints with three

The new §12 should be authored from these complete checklists first; all other milestone text and
cross-references should then be made to agree with them.

### M1 / CP-1 — Data and fixed features (**9 items**)

1. Required snapshot contains A44, A65/A01, and benchmark-only A69 from 2019-01-01 through the pull
   date, with the known A65 head gap handled and snapshot hash recorded.
2. UTC indexing, Berlin 23/25-hour identity, PT15M→hour aggregation, chunk stitching, missing-quarter
   fail-closed behavior, and the 2025-10-01 price transition are correct.
3. Fixed champion catalog is implemented: calendar/regime, A65 load forecast, lagged prices, and
   closed-left rolling price statistics; A69/actual columns are rejected by champion inference.
4. ENTSO-E↔SMARD prices are reconciled on a fixed stratified sample covering pre-crisis, crisis,
   post-crisis, and the PT15M transition; do not re-compare the whole archive merely because it is
   available.
5. The targeted repository tests cover chunk stitching, a missing quarter, fall-back DST identity,
   closed-left rolling windows, transition aggregation, and the schema firewall.
6. Leakage audit records every champion feature as KFT/LAG, states the A65 assumption honestly, and
   confines A69 to the benchmark/evaluation stratum.
7. Snapshot/data folder and README carry CC BY 4.0 attribution and the data cutoff.
8. Three spectral figures and one short interpretation paragraph are committed.
9. One fresh Integration Critic returns `PASS` on the final candidate from a clean detached checkout.

### M2 / CP-2 — Model, calibration, and analysis (**8 items**)

1. Similar-day naïve, seasonal-naïve-168 h, Ridge, and the fixed-catalog nine-head LightGBM run on
   the five pinned folds within the Apple M3 / 16 GB / CPU-only constraint.
2. MAE, mean pinball loss, and both DM analyses are reported with effect sizes and
   `development_post_selection`; no favorable result is required.
3. CQR and isotonic-last are implemented; the 20-row `Q={8,7,5,−1}` fixture passes; raw,
   post-CQR, and final empirical coverage are reported; final quantiles are monotone.
4. Champion SHAP and permutation-importance outputs are committed and interpreted without a
   required feature ranking or overlap.
5. Regime-stratified error table includes observation counts, the negative-price stratum, and honest
   thin-slice uncertainty.
6. The one-shot raw-head A69 benchmark reports pooled mean-pinball percentage difference and its
   limitation; no second calibration or deployable artifact exists.
7. Reproducibility/MLflow records for the decision-bearing baseline, champion, and calibration runs
   contain snapshot hash, code SHA, folds, feature list, seed, hyperparameters, metrics, and artifact
   links. No hypothesis/parent/delta/decision bureaucracy is required for every exploratory run.
8. One fresh Integration Critic returns `PASS` on the final candidate from a clean detached checkout.

### M3 / CP-3 — Showcase and release (**6 items**)

1. Bundled champion, CLI, container, and marimo app run locally from a clean setup.
2. Quantile selector and at most one simple scenario control work without the retired multidimensional
   grid, dynamic SHAP, or per-cell OOD system.
3. Static Pages export carries the lean reading order and performs no runtime calls; all assets and
   links render.
4. HF Space deploys the bundled champion and renders the same release snapshot; free-tier sleep is
   disclosed, not performance-gated.
5. README, Pages, Space metadata, and MLflow links agree on snapshot/cutoff, fixed catalog, metrics,
   development evidence class, benchmark limitation, and champion identity. Limitations and
   reproduction instructions are complete.
6. One fresh Integration Critic returns `PASS` on the final candidate from a clean detached checkout.

Old CP-4 and CP-5 are retired. The companion artifact and AWS extension become optional future
projects opened only by a new owner instruction after CP-3; neither starts automatically and neither
is part of the v6.7 completion definition.

**Net checklist change:** 56 future checkboxes across CP-1…CP-5 become 23 across CP-1…CP-3, while
every retained checkpoint still has an independent final review.

---

## AMD-11 — Collapse the Gauntlet to a lean checkpoint review loop

### What survives

- One exact repository, checkpoint, and ratified anchor per brief.
- The complete named checkpoint checklist; a brief cannot silently reduce it.
- Local `gauntlet/<checkpoint>` candidate branch; never `main`, never pushed.
- Builder ≠ Critic and no self-certification.
- A fresh Integration Critic in a clean detached checkout at the final candidate SHA.
- Exact reproduction commands and observed results.
- One committed markdown verdict under `docs/track-b/evidence/<checkpoint>/`.
- `final_candidate_sha` plus `evidence_tip_sha`, with a verdict-only delta.
- Owner-only LAND decision, evidence tag, and tag-before-delete lifecycle from `AGENTS.md`.

### What retires

- mandatory Builder decomposition and mandatory Builder worktrees for every piece;
- component Critics and per-surface verdicts;
- five-surface scope declarations and all independent fixture materialization/hash ceremony;
- `reviewed_paths` staleness calculations, because there are no earlier component verdicts to reuse;
- mandatory `workbench.md` and its lifecycle;
- raw-second active-elapsed arithmetic, pause ledgers, and `started_at_utc` as first output;
- executor-tier and “brand-new session” gates;
- exhaustive read-scope/provenance declarations and `ASSERTED_ROLE_BOUNDARY`;
- reproducing every brief field inside the Return Packet;
- Builder seed and start/end topology tables;
- formal `BRIEF_INVALID`, `PLATEAU`, and `BUDGET_EXHAUSTED` states;
- mandatory “largest gap,” “exact next acceptance test,” and 3–5 defense-question fields on every
  review/return;
- duplicate Orchestrator re-validation of every record-level claim.

The Engineering Lead may implement directly or use bounded Builders. If it uses parallel writable
contexts, it still isolates disjoint paths and remains the sole Git writer. These are engineering
choices, not mandatory ceremony.

### New terminal vocabulary

- `PASS` — every checklist item is evidenced and the fresh final Integration verdict is `PASS`.
- `BLOCKED` — an owner credential/action, publication, destructive action, new authority, or plan
  decision is required.
- `INCOMPLETE` — work is coherent and reviewable but one or more checklist items remain open,
  including when the planning timebox is no longer worth extending.

An invalid or contradictory brief is corrected before repository work; it does not need a formal
checkpoint status, timestamps, or a special report template.

### Minimal artifacts

The template file should contain only four short forms:

1. checkpoint brief;
2. final Integration-Critic assignment and verdict;
3. checkpoint return;
4. Orchestrator receipt plus the existing AGENTS-owned disposition commands.

The checkpoint return contains: status; repo/checkpoint/anchor; both SHAs and verdict-only delta;
working-tree/branch state required by `AGENTS.md`; complete checklist with direct evidence; final
Critic verdict; reproduction commands/results; files changed/diffstat; open risk or owner action;
and proposed disposition/commit message.

`docs/track-b/rule-inventory.md` must preserve its historical tables but add a new v6.7 current-state
section, mark eliminated rules retired, re-baseline the live count from the authored documents, and
stop advertising 168 as the current rule count. Do not guess the new count in advance; compute it
from the final text and record the arithmetic.

---

## AMD-12 — Version, public claims, and parked proposals

1. Change the declared capstone version to **v6.7** while retaining the filename
   `capstone_V6_6.md`, matching the repository's existing in-place anchor convention. Add a
   v6.6→v6.7 delta block and update M0's ratification history.
2. Change the stage map from **v7 to v8** and make it the new capstone-first routing aid.
3. Update `progress.md`: v6.7 active, optional syllabus, M1/CP-1 next, no pending amendment, no
   capture blocker, no five-checkpoint/24-hour reserve, no curriculum envelope.
4. Rewrite the README's current-status and results language. Remove forward-audit claims, measured
   pre-gate claims, proxy-selection claims, recurring refresh, health report, and hard speed claims.
   State the fixed catalog, development evidence, one-number A69 benchmark, frozen snapshot, and
   three-stage project shape.
5. Mark `aws-extension-spec_v1_1.md` **STALE / NOT SCHEDULED** at the top. Its weekly refresh,
   health-report, lookup-grid, outcome-gate, version cascade, and Month-6 sequencing premises are
   retired. Do not line-edit the parked architecture into apparent currency. If cloud work is later
   desired, write a new proposal against the artifact that actually shipped.
6. Keep historical amendment sheets, CP-0 evidence, and defect records unchanged. History may name
   retired machinery as history; it must not be mistaken for a live requirement.

---

## What v6.7 still protects

- Correct UTC/DST handling and the PT15M→hourly transition.
- Complete-bin ingestion and fail-closed missing-quarter behavior.
- Closed-left lag/rolling features and a strict champion runtime schema.
- An explicit, limited A65 assumption and an explicit A69 post-gate boundary.
- Five pinned walk-forward folds across the three regimes.
- Transparent baselines, LightGBM quantile heads, CQR, isotonic-last, and precise coverage claims.
- SHAP, permutation importance, regime/negative-price analysis, and the one-number A69 benchmark.
- A committed redistributable snapshot with attribution, fixed seeds/dependencies, and reproducible
  decision-bearing runs.
- Static recruiter-first presentation plus a small deployed interactive deep dive.
- One genuinely independent, fresh final review per checkpoint.
- Local-only agent work, owner publication authority, and preserved evidence refs.

Those are the parts whose failure would materially damage the project. Everything else should have
to earn its way back through a new owner decision.

---

## Application order

1. **Ratify this sheet and grant one task-scoped suspension naming the six locked files and the
   amendment-record promotion.**
2. **Author the three new §12 checklists first.** They define the destination and prevent old
   checklist fragments from surviving by accident.
3. Apply AMD-1 through AMD-9 across the capstone, working outward from the new checklists.
4. Rewrite `engineering-role.md` and `gauntlet-templates.md` to the AMD-11 loop; then update the
   Orchestrator's Track B briefing/receipt sections.
5. Apply AMD-0 to `orchestrator-role.md` and rebuild `program-stage-sequence.md` v8 from the new
   Track B critical path.
6. Apply README, progress, AWS-proposal, package, and dead-capture-code consistency edits.
7. Update the rule inventory last, from the text that actually exists.
8. Run the acceptance test below and return one full diff for owner review. Do not publish or land.

---

## Acceptance test for the application task

1. **Scope:** no file outside the six locked targets, the final amendment record, and the listed
   non-locked consistency targets was changed.
2. **Critical path:** the only live flagship sequence is M1/CP-1 → M2/CP-2 → M3/CP-3. No Track A,
   SQL-B, G0–G5, AWS, companion, reviewer-recruitment, or calendar prerequisite can block it.
3. **Checklist counts:** CP-1 = 9, CP-2 = 8, CP-3 = 6; CP-4/CP-5 have no live checklist.
4. **No outcome gate:** no live checkpoint requires favorable p-values, effect size, coverage,
   importance ranking, direction, or network/runtime threshold.
5. **Data scope:** no live requirement fetches or fits A75/actual generation; no proxy or
   four-catalog selection language survives outside explicitly historical text.
6. **Benchmark scope:** exactly one live A69 benchmark contract exists: raw heads, pooled mean
   pinball percentage difference, optional free MAE, no calibration/deployment.
7. **Assumption:** every live claim about A65's **pre-gate** availability says assumption; none calls
   that pre-gate status demonstrated, confirmed, proven, or measured.
8. **Review loop:** exactly one mandatory fresh Integration verdict is required per checkpoint; no
   live component-Critic, surface-declaration, oracle-hash, staleness, workbench, provenance,
   raw-second, or five-status requirement survives.
9. **Release scope:** no live multidimensional lookup/OOD grid, registry-first runtime load, weekly
   refresh, health report, stranger-test gate, hard load-time gate, or CV/LinkedIn checkpoint item
   survives.
10. **Dead code:** `src/pit_capture/` and `tests/pit_capture/` are absent from the active tree,
    `pyproject.toml` no longer packages them, and `evidence/cp-0` still resolves.
11. **Cross-reference sweep:** repository-wide searches for the retired vocabulary are either empty
    in live sections or appear only in clearly labelled historical amendment/evidence text. Every
    live reference resolves to an existing section/artifact.
12. **Public consistency:** README, capstone, stage map, and progress agree on v6.7, the fixed
    champion catalog, development evidence, three checkpoints, and optional syllabus.
13. **Governance accounting:** the rule inventory's current count is mechanically derived from the
    final documents; prior counts remain labelled historical.
14. **Repository handoff:** run the relevant tests, `git status --porcelain=v1`, `git diff --stat`,
    and the full diff; list every touched file with one-line rationale and propose one commit message.

---

## Bottom line

Draft v2 would have made the existing program somewhat cheaper. Draft v3 makes it a different,
finishable program: no compulsory syllabus, no synthetic VRE selection bureaucracy, no
result-dependent stop signs, no recurring pseudo-production chores, three checkpoints, and one
independent review at each. The remaining rigor is concentrated where a silent failure would make
the portfolio claim false.
