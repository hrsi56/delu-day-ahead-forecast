# Amendment record — capstone v6.6 → v6.7 — scope and governance reduction

**STATUS: RATIFIED 2026-09-07 BY THE PROJECT OWNER. APPLIED; OWNER-AUTHORIZED CONSISTENCY REPAIR AWAITS FRESH INDEPENDENT RE-VERIFICATION.**

**The three owner decisions were all accepted as YES:**

| # | Decision | Owner ruling |
|---|---|---|
| **D-1** | Keep one gate-feasible residual-load feature, rebuilt as a 42-day D-2-bounded trailing-window lag feature, selected by a two-arm development comparison | **YES** — *"the feature adds domain judgement, and the base is selected if it does not improve, so it forces no performance cost"* |
| **D-2** | Freeze the final 90 complete delivery days as an untouched holdout, evaluated once after the champion freezes | **YES** — *"for a portfolio project, clean evidence on a frozen model matters more than a model trained to a later date with no clean test; the historical replay prevents any misrepresentation as a live service"* |
| **D-3** | Register the champion to the DagsHub MLflow Registry as a non-gating step | **YES** — *"clear evidentiary value, small cost, no runtime dependency, and it does not block release"* |

Applied under one owner-authorized, task-scoped suspension of the Governance Lockdown covering nine
locked files, the `capstone_V6_6.md` → `capstone_V6_7.md` rename, and this promotion. The suspension
is spent at the terminal return of that task. No file outside its scope was changed by that task,
`CLAUDE.md` is untouched, and nothing was published, landed, committed to `main`, or pushed.
**`AGENTS.md` was edited afterwards, under a second and separate owner authorization granted on
2026-09-07 after this record was written** — seven citation-repair sites, no policy moved, listed in
`progress.md`. The statement below that *this* suspension "does not need to name `AGENTS.md`"
remains true of this suspension.

**A later independent re-verification returned `FAIL` on remaining semantic inconsistencies.** On
2026-09-07 the Owner authorized repair of every finding as one task-scoped continuation covering the
affected locked files and directly necessary consistency edits. That repair reconciles the capstone,
Orchestrator, rule inventory, progress/stage state, this record's impossible substring test, and the
third and fourth bounded `cp-0-defects.md` regions. The repairing agent may run mechanical checks but
does not independently certify its own work; closure requires a fresh read-only review.

Resulting checklist counts: **CP-1 = 10, CP-2 = 10, CP-3 = 6 (26 total)**, replacing 56 across
CP-1…CP-5.

## Provenance

This sheet was drafted in six iterations between 2026-09-06 and 2026-09-07 and reviewed against the
repository at each one. **v3** proposed the structural cut — optional syllabus, no four-catalog
selection, no outcome gates, three checkpoints, one review each — and its arithmetic verified exactly
(56 future checkboxes across CP-1…CP-5: 17/9/10/7/13). **v4** corrected four defects: the anchor-rename
convention had been stated backwards (git history shows every version bump renamed the file), the
suspension needed more locked files than six, two consistency targets were missing, and the retired
ceiling had been left with nothing in its place. v4 also pulled back three cuts that removed a
*deliverable* rather than ceremony — the domain feature, the out-of-sample number, and the registry
entry — which became decisions D-1, D-2 and D-3. **v5** caught that v4's holdout collided with v6.6
§5.1's Fold 5, which was defined as the final 90 days of the snapshot; it re-pinned the tail
partitions, wrote the final fit and calibration protocol v6.6 never had, and replaced the deprecated
MLflow `Production` stage with the current alias and tag contract. **v6** corrected two arithmetic
errors carried in the review — the raw-model fit cutoff is 152 delivery days before the snapshot
cutoff, not 241, because the final fit includes Fold 5's evaluation block — replaced the derived
minimum pull date with a direct assertion, and established that the 90-day holdout DM is
confirmatory-style but **not** power-qualified, since the retired §7.1 contract had made 90 a floor
rather than a demonstration of power. Two micro-fixes closed at ratification: the optional `N_80`
note was deleted, and the `cp-0-defects.md` contradiction was resolved by adding that file to the
suspension for two initial edits. A later owner-authorized repair pass found one adjacent
present-tense AMD-G5 paragraph that still declared three v6.7-retired mechanisms “fully in force”;
the owner expanded the same task scope to that bounded consistency region. The final repair then
caught that the ledger header still counted the now-MOOT D-CP0-18 as “remedied but not re-tested” and
corrected that one status line under the same direct-consistency authority. The current acceptance
bar therefore expects exactly four changed regions in that file, not two.

---

## Owner decisions ratified before application

The owner ratified **YES / YES / YES** on D-1, D-2 and D-3. The table preserves the alternatives that
were presented before ratification; they are decision provenance, not open questions for the
executor.

| # | Decision | Recommended | If you decline |
|---|---|---|---|
| **D-1** | Keep one gate-feasible residual-load feature, rebuilt as a trailing-window lag feature, selected by a two-arm development ablation? | **Yes** — ~6–10 h, and it is the project's only explicit power-system/merit-order feature | Champion ships on calendar/load/lag/rolling only; §0 item 3's merit-order rationale becomes "unrepresented"; remove one CP-2 item, while CP-1's count is unchanged |
| **D-2** | Freeze the final 90 complete delivery days of the snapshot as an untouched holdout, evaluated once after the champion freezes? | **Yes** — ~2–3 h, converts "no confirmatory evidence" into one clean out-of-sample number | All model evidence is development-stage post-selection, disclosed as such; remove one item from CP-1 and one from CP-2 |
| **D-3** | Register the champion to the DagsHub MLflow Registry as a non-gating step? | **Yes** — a small bounded operation, the cheapest visible MLOps signal | Public experiment runs remain the only MLflow surface; CP-3's count is unchanged because registration is a clause inside item 1 |

**All three recommended: CP-1 = 10, CP-2 = 10, CP-3 = 6 (26 total).** Counts by substantive choice:

| D-1 | D-2 | CP-1 | CP-2 | CP-3 |
|---|---|---:|---:|---:|
| Yes | Yes | 10 | 10 | 6 |
| No | Yes | 10 | 9 | 6 |
| Yes | No | 9 | 9 | 6 |
| No | No | 9 | 8 | 6 |

D-3 changes the registration clause inside CP-3 item 1, not the checkpoint's item count. The counts in
AMD-10 and the acceptance test assume D-1 and D-2 are accepted; if either is declined, remove its
starred clauses/items and use this table. D-3 is edited as a clause only.

None of the three re-introduces process. Each is a deliverable — a feature, a table, a number, a
registry entry — and each replaces machinery that costs several times more.

---

## Executive judgment

The systems being removed created most of the visible chores: the 38-coefficient A75 climatology,
four matched feature catalogs, exact Decimal adjudication, catalog-identity artifacts, repeated
component Critics, five future checkpoints, raw-second clock accounting, and a syllabus-derived
calendar. Removing chores while keeping the systems that generate them would save one review and
retain the whole dependency tree.

The position of this sheet:

1. **Track A becomes an optional library, not a track on the critical path.** No syllabus block, month
   gate, NotebookLM verdict, SQL exercise, algorithm quota, or learning deliverable may block Track B,
   Track C, an application, or a release.
2. **The candidate set is fixed and simple, and frozen in the plan before fitting.** Remove A75's
   per-fold climatology, the four-catalog experiment, and all selection/blinding machinery. Keep at
   most one explicit power-system feature, built as a lag feature that needs none of that machinery
   (D-1). Select between the two predeclared catalogs by one raw-head development metric, freeze the
   result at CP-2, and preserve the owner-requested A69 benchmark as one raw-head comparison and one
   number.
3. **Measurements describe the artifact; they do not decide whether it may exist.** DM significance,
   coverage, runtime, and feature importance are reported honestly. An unfavorable result changes the
   conclusion and limitations, not the checkpoint status.
4. **Five future checkpoints become three.** Data → model and analysis → release. The former M2/M3
   split and M4/M5 split no longer protect a live dependency after the selection and forward-audit
   machinery is removed.
5. **One independent review per checkpoint.** The Lead may build directly or delegate at its
   discretion. One fresh Integration Critic reviews the final candidate from a clean detached
   checkout. Component-verdict choreography, surface declarations, staleness bookkeeping, workbench
   ceremony, provenance declarations, and raw-second accounting are retired.

The governing test for every retained obligation is:

> Retain it only if it (a) prevents a plausible silent correctness or leakage failure, (b) is
> necessary to reproduce the released artifact, or (c) is directly visible and valuable to a Data
> Science hiring manager. Otherwise delete it, or make it optional and non-gating.

This is a portfolio project, not a regulated production service or a clinical confirmatory study. The
plan should protect scientific honesty and artifact quality; it should not simulate an enterprise
change-control system around a solo build.

**The symmetric failure is worth naming once.** Over-cutting is as expensive as over-processing,
because a portfolio artifact that a hiring manager finds generic costs the whole project's purpose,
and nothing in a leaner process recovers it. The three pull-backs above are where v3 crossed that
line: each removes a *deliverable* the interview rests on in order to save machinery that this sheet
was already deleting anyway.

---

## Owner decisions this amendment records

These are inputs to the amendment, not questions for the executor to reopen. All four are recorded in
`progress.md` § *Standing Scope Decisions* as of 2026-09-06:

- **A65/A01 pre-gate availability is assumed** from Regulation 543/2013 Art. 6(2)(b), corroborated but
  not empirically demonstrated by the 2026-06-12 observation. The assumption is disclosed.
- **The syllabus is optional.** `syllabus_v3_2.md` remains a useful curriculum and NotebookLM input,
  but no part of it gates the capstone, applications, or any other work.
- **The A69 information benchmark stays, but is trimmed** to one raw-head comparison and one headline
  number.
- **The project optimizes for a finished, honest, recruiter-visible artifact.** It does not optimize
  for procedural proof that every agent handoff was pristine.

---

## Application scope

Applying this sheet requires one owner-authorized, task-scoped suspension of the Governance Lockdown
naming the following **nine existing locked files**, authorizing promotion of this draft to the final
amendment record, and stating the objective "apply the ratified v6.7 scope and governance reduction
atomically":

| # | Locked file | Why it changes | Depth |
|---|---|---|---|
| 1 | `capstone_V6_6.md` → **renamed** `capstone_V6_7.md` | product scope, methodology, milestones, and checkpoint bars | rewrite |
| 2 | `engineering-role.md` | collapse the Gauntlet to one final independent review | rewrite |
| 3 | `docs/track-b/gauntlet-templates.md` | replace the ten-form protocol with a short brief, verdict, return, and receipt | rewrite |
| 4 | `orchestrator-role.md` | make Track A optional and adopt the three-checkpoint flow | rewrite |
| 5 | `program-stage-sequence.md` | rebuild v7 as a capstone-first v8 map with an optional learning sidecar | rebuild |
| 6 | `docs/track-b/rule-inventory.md` | retire eliminated rules and record the new live inventory | rewrite |
| 7 | `notebooklm-role.md` | 4 anchor citations to repoint; one banner stating its checkpoint behaviour never fires unless a prompt requests it | banner + citations |
| 8 | `syllabus_v3_2.md` | 5 anchor citations to repoint; one banner stating it is optional as of 2026-09-06 and gates nothing | banner + citations |
| 9 | `docs/track-b/cp-0-defects.md` | status-summary arithmetic; `D-CP0-18`'s disposition; striking it from the ledger's closure sentence; later-authorized re-tensing of the adjacent AMD-G5 paragraph that otherwise declared retired mechanisms live | four bounded regions |

Files 7 and 8 are in scope for **citation and banner edits only**. Their content is not rewritten and
their curriculum is not retired — but leaving them untouched would leave two live locked documents
asserting that a demoted syllabus gates Track B, and would break 9 citations the rename repoints.
`AGENTS.md`'s own rule is explicit: *the citation follows the ref.*

File 9's initial application scope was **two edits only** — a disposition field and one clause of the
closure sentence. Later owner-authorized repairs add exactly two bounded regions: re-tensing the
adjacent AMD-G5 paragraph and marking its `BRIEF_INVALID`/clock-exclusion/§10 statements superseded,
and correcting the top status summary so it counts D-CP0-18 as MOOT rather than remedied. Every
defect definition, acceptance criterion and historical evidence link remains untouched; see AMD-1
for why the closure-sentence edit cannot ride on the operational-record exception.

The suspension does **not** need to name `AGENTS.md` or `CLAUDE.md`. The root publication, `main`,
local-branch, evidence-retention, tag-before-delete, and Builder ≠ Critic protections all remain
compatible with the leaner loop and are deliberately unchanged.

Directly necessary non-locked consistency edits in the later application task:

- `README.md`
- `progress.md` (Orchestrator operational state)
- `aws-extension-spec_v1_1.md` — STALE banner only
- `docs/track-b/gauntlet-amendment-plan.md` — historical banner and 3 anchor citations *(the three
  citation repoints were reverted on 2026-09-07 — see the post-ratification repair addendum, R-1;
  the banner stands)*
- `PJM_Track_B_Gauntlet_Loop_Guide_HE.md` — historical-banner tense correction only
- `pyproject.toml`
- removal of the inactive `src/pit_capture/` and `tests/pit_capture/` trees after the existing
  `evidence/cp-0` tag is verified

**Deliberately not touched, verified rather than assumed** — do not spend effort here:

- `Mid_M_0_Gate.md` is a Track A linear-algebra consolidation gate. Under AMD-0 it simply stops being
  a gate. No edit; it survives as an optional artifact.
- The CP-0 evidence files, `docs/spike-feed-status.md`, and `docs/pit-metadata-investigation.md` stay
  as historical evidence. So does the remainder of `docs/track-b/cp-0-defects.md`; only the four
  bounded regions named in the scope table above change.

At ratification, the draft was promoted to the repository's final amendment-record name,
`docs/track-b/capstone_V6_6-to-V6_7-amendments.md`, as part of the same coherent application task.

---

## AMD-0 — Make the syllabus genuinely optional, not merely labelled optional

`progress.md` already records the owner's decision, but the live Orchestrator contract and the stage
map still require the syllabus at session start, route every session toward the next syllabus topic,
enforce G0–G5 learning gates, make SQL-B a prerequisite for applications, and define the program goal
by completion of a ~729-hour curriculum. That is a semantic contradiction, not harmless stale wording.

Verified live as of `d5b0b12`: `orchestrator-role.md` line 5 and line 20 (~729 h / ≈753 h envelope),
line 119 (the mandatory monthly interleave), lines 137 and 338 ("all active applications open after
SQL-B completes at G3"), line 382 ("does this session move Yarden closer to the next syllabus topic
he's due for?"), and line 432 (the goal defined as completing the ~729-hour program).

### `orchestrator-role.md`

1. **Startup read.** Remove the syllabus from the mandatory first-session read order. Read it only
   when Yarden explicitly requests a learning block or when a concrete capstone task needs a theory
   refresher.
2. **Track definition.** Define Track A as an optional, on-demand resource. It has no current
   position, next-due topic, schedule, monthly gate, or completion obligation unless Yarden chooses to
   run a specific block.
3. **No interleave contract.** Delete the mandatory "How Tracks A and B interleave" schedule and all
   statements that locate M1–M5 inside syllabus months. Track B advances only by CP-1 → CP-2 → CP-3.
4. **Type L survives as a utility.** A requested learning brief may still cite the syllabus, use a
   depth label, and ask NotebookLM for a deliverable. Remove mandatory checkpoint flags, consolidation
   verdicts, and "the syllabus is taught in full" behavior.
5. **Session lifecycle.** Delete the Track-A carry-forward status line and learning-checkpoint
   exception. Optional learning is recorded only when it materially affects current plans.
6. **Track C independence.** Delete the SQL-B/G3 and Month-5 application gates. M2 remains a useful
   suggested portfolio trigger for stronger outreach, not permission to apply. Active applications may
   begin whenever Yarden chooses.
7. **Progress skeleton.** Track A appears only while an optional block is active; the mandatory
   durable positions are Track B and Track C. No "next pending Track A checkpoint" exists.
8. **Routing.** Replace "does this move him toward the next syllabus topic?" with "does this advance
   the current capstone/release goal, the job search, or an optional gap Yarden chose to close?"
9. **Goal.** Delete the ~729/~753-hour program target and the February/April curriculum projections.
   The goal becomes shipping the flagship through CP-3 and using optional learning/companion/cloud
   work only when its value is separately chosen.

Current edit sites include `orchestrator-role.md` lines 16–26, 46–119, 121–140, 148–161, 263–297,
342–350, 378–421, and 430–442. Edit by semantic anchor, not by stale line number.

### `program-stage-sequence.md`

Rebuild the document as **v8**, rather than patching twelve rows in a syllabus-first v7 map:

- Main table: M1/CP-1 → M2/CP-2 → M3/CP-3, plus only the manual prerequisites and Track C actions that
  actually serve those stages.
- Optional learning sidecar: syllabus topics indexed by the capstone task they can help with. They are
  suggestions, can be taken in any useful order, and never sit between two Track B rows.
- Retire G0–G4 learning gates, the SQL-B application gate, algorithm quotas, monthly consolidation
  verdicts, curriculum calendar projections, and the total-program hour envelope.
- Retire the automatic DEC-AWS ballot and automatic companion launch. Both become separate future
  projects requiring a new explicit owner instruction after the flagship ships.
- Preserve already completed history only as a short note. The map is for routing forward work, not
  proving that every old syllabus row still has a home.

### `syllabus_v3_2.md` and `notebooklm-role.md`

Banner and citations only, as scoped above. `syllabus_v3_2.md` remains a coherent optional
curriculum; it is not rewritten and not retired. `notebooklm-role.md` remains the contract for a
voluntary teaching session; its checkpoint behavior simply never fires unless a future prompt
explicitly requests it. Each banner must say explicitly that later body language using “must,”
“gate,” fixed months, or mandatory interleaving is superseded and non-operative unless a future owner
prompt opts into that learning block. Rewriting either would spend governance effort without changing
the critical path — but neither may present Track A as a live gate, and neither may keep citing a
filename that no longer exists.

---

## AMD-1 — Cancel point-in-time capture and remove its inactive implementation

### Claim that survives

Use this wording consistently in §3, §5.2, R-2, the README limitations, and the final report:

> A65/A01 pre-gate availability is an explicit assumption based on Regulation 543/2013 Art. 6(2)(b),
> corroborated but not empirically demonstrated by the 2026-06-12 observation. The archived vector was
> unchanged from 15:35 CEST D-1 through post-delivery on the one sampled day (n=1,
> `revisionNumber=1`), which supports archive stability only and says nothing about pre-gate
> availability.

Never describe the assumption as spike-confirmed, measured, proven, or empirically established.

### Capstone edits

- Delete §3's capture contract, ledger schema, and "observed available by" protocol.
- Delete B-Man-PIT and every live prerequisite, gate, reading-order item, risk statement, and
  checkpoint item that depends on the ledger.
- Keep M0.5/CP-0 as one short **historical** paragraph: executed, landed, tagged, and later retired
  when its underlying requirement was cancelled. Do not preserve its seven-item live checklist in the
  current plan.
- Re-tense the v6.4/v6.5 delta paragraphs as superseded historical decisions.
- Remove the separate CP-1 "feed exists / recent 30 days" probe. **A successful required bulk pull is
  already the stronger archive-reachability and snapshot-completeness test; do not test existence and
  then immediately test it again by ingesting the same feed.** It is not evidence of pre-gate
  availability. The same reasoning retires archive-depth confirmation as a separate item: a pull that
  returns 2019-01-01 → pull-date has demonstrated its own archive depth.

### Defect-ledger consequence — record it, do not rediscover it

`docs/track-b/cp-0-defects.md` carries two remedied-but-not-re-tested defects that `progress.md`
schedules inside CP-1:

- **`D-CP0-18`** (`started_at_utc` is required but the executor has no clock unless told to call one)
  remediated `engineering-role.md` step 1. **AMD-11 deletes that requirement entirely**, so the re-test
  becomes moot: there is nothing left to re-test. Record it as such.
- **`D-CP0-19`** (`LAND` has two things worth tagging and the contract named one) remediated
  `AGENTS.md` R2, which this amendment does **not** touch. Its re-test still rides inside CP-1's
  landing, exactly as planned.

**The scope splits in two, and only the first half is free.**

- **`D-CP0-18`'s status/disposition line** becomes `MOOT — underlying requirement retired by v6.7`.
  That is a status and disposition field, squarely inside the `AGENTS.md` *Operational-record
  exception*, and needs no suspension. The defect definition, its history and its evidence links are
  untouched.
- **The ledger's closure sentence is not free, and the file itself records why.** It reads *"This
  ledger stays OPEN. It closes when D-CP0-18's and D-CP0-19's remedies are re-tested,"* and the very
  next sentence states that the AMD-G5 clause was struck from that same condition **"under an
  owner-authorized, task-scoped suspension of the Governance Lockdown."** Striking `D-CP0-18` from it
  is the identical operation on the identical sentence, and `AGENTS.md` excludes *acceptance criteria*
  from the operational-record exception. **Follow the recorded precedent: name
  `docs/track-b/cp-0-defects.md` in the suspension, initially scoped to those two edits.** That makes
  the suspension **nine** files. The later repair authorization adds only the adjacent AMD-G5
  re-tensing and the status-summary correction described in *Application scope*; it does not reopen
  any defect definition, acceptance criterion, or historical evidence.

Leaving the sentence alone is not a safe shortcut: the ledger would then read `D-CP0-18 — MOOT` in one
place and "closes when D-CP0-18's remedy is re-tested" in another, which is exactly the live
contradiction this amendment exists to remove. After the edit, closure depends on `D-CP0-19` alone.

### Repository cleanup during application

After verifying `evidence/cp-0` resolves and preserves the reviewed candidate chain:

- delete `src/pit_capture/` and `tests/pit_capture/` from the active tree;
- remove `src/pit_capture` from the Hatch package list in `pyproject.toml`;
- retain the CP-0 verdicts, disposition tags, `docs/spike-feed-status.md`, and
  `docs/pit-metadata-investigation.md` as historical evidence.

Dead implementation is not evidence preservation. The tag and verdicts preserve the evidence; the
unused package only makes the repository look as if capture is still supported.

---

## AMD-2 — Remove the four-catalog selection system; rebuild the domain feature as a lag feature

This is the largest substantive cut, and the one place where the machinery and the science have to be
separated carefully.

### What goes, and why

The current design fetches A75 actual generation, fits a 38-coefficient seasonal-diurnal OLS model
inside every fold, persists fit lineage, creates two proxy features, trains a full 2×2 catalog
experiment, specifies exact Decimal/CSV/JSON canonicalization, commits identity manifests, and then
adds a label-blind review and a deterministic adjudication with eligibility thresholds and a
three-level tie-break. All of that exists to decide whether a synthetic expectation of renewable
output adds value to a champion that cannot use the real delivery-day VRE forecast.

**The apparatus is disproportionate to the decision it protects.** A two-arm ablation answers the same
question. Everything above the ablation — blinding, Decimal comparisons, canonical byte contracts,
identity manifests, eligibility boundaries, tie-break ordering, the selection declaration, and the
independent poisoning oracle — is machinery for adjudicating a decision that a table and a paragraph
of honest prose can carry.

### What should not go with it

Deleting the *feature* along with the apparatus is a step too far. §1 names "domain understanding,
defensible feature engineering" as a required demonstration, and §0 item 3 justifies omitting the gas
marker on the grounds that the merit-order signal is carried by a residual-load proxy. Remove the
feature and the champion keeps useful domain-informed calendar, regime and negative-price-memory
features, but loses its only explicit power-system/merit-order construction; §0 item 3's rationale is
then left dangling.

### Replacement design (decision **D-1**, recommended)

Two candidate strict-gate catalogs and their selection metric are frozen in the plan before fitting:

- `base`: calendar and static regime features; A65/A01 day-ahead load forecast; lagged day-ahead
  prices; and closed-left rolling price statistics;
- `base + residual_load_proxy`: the base plus **one gate-feasible residual-load feature**, defined as a
  plain lag feature:

  > `vre_norm(d,h)` = mean of aggregate A75 actual wind-onshore + wind-offshore + solar generation at
  > local clock hour `h` over the trailing **42 complete delivery days** ending at the close of
  > **D-2**.
  >
  > `residual_load_proxy(d,h) = load_fc(d,h) − vre_norm(d,h)`

`h` is the Europe/Berlin local clock hour while every row retains its canonical UTC identity.

**DST contract, target day and window alike** — the unit test needs something to assert on both
sides. *Target day:* on the fall-back day both repeated local-hour rows receive the same historical
mean; no row is synthesized for the absent spring-forward hour. *Inside the window:* every
observation bearing that local clock hour participates in the mean, so a 42-day window contributes
43 observations at hour 02 across a fall-back boundary and 41 across a spring-forward boundary. Row
identity remains UTC throughout; only the grouping key is local.

Forty-two days (six weeks) is pinned as a simple bias/variance
compromise: enough observations to smooth daily weather noise while remaining responsive to recent
season and capacity levels. It is a design choice, not selected or tuned later.

**Why this is cheaper *and* better than v6.6's climatology — three reasons, all checkable:**

1. **It is a LAG feature by construction, so the entire apparatus this amendment is deleting does not
   apply to it.** It consumes only actuals published through D-2 — Regulation 543/2013 Art. 16(2)(b) requires
   [aggregated generation by production type no later than one hour after the operational period](https://eur-lex.europa.eu/eli/reg/2013/543/2020-01-01/eng),
   so a D-2 window is available well before the 12:00 D-1 gate. There is no proper-training partition
   rule, no per-fold refit, no
   fit-lineage invariant to check, and no independent poisoning oracle to run, because there is no fit.
   It is audited exactly like `price_lag_168`.
2. **It can track the build-out; the old climatology has no explicit mechanism to do so.** German
   installed solar capacity rose from
   [48.9 GW at end-2019](https://www.bundesnetzagentur.de/SharedDocs/Downloads/EN/Areas/ElectricityGas/Monitoring/KernaussagenEng_MB2020.pdf)
   to [117 GW at end-2025](https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/EN/2026/20260108_EEG.html).
   Although v6.6 re-estimates its
   fixed-form seasonal-diurnal basis per fold, that basis is fit across the whole proper-training
   partition and has no capacity or trend term. It therefore risks bias toward older capacity levels
   in recent folds. A trailing window adapts to that growth without adding a fitted model. Whether it
   improves price forecasts remains an empirical question for the ablation; do not state
   under-prediction as an observed result before measuring it.
3. **It is ~20 lines against a 38-coefficient basis, its exclusion accounting, its coefficient
   persistence, and its fit-poisoning positive control.**

`expected_scarcity_proxy` is not retained. Its interview defense (why `relu`, why a product) is
preserved in §13 as a design idea that was scoped out, which is an honest and adequate answer.

**Honest caveat, disclosed in the same sentence as the A65 assumption:** A75 actuals are subject to
later revision, so the trailing window uses the archive's current values rather than the values
visible in real time. This is the same class of assumption as the A65 KFT assumption and is disclosed
the same way — one sentence in §5.2 and one in the public limitations.

**A real, small runtime cost, named rather than discovered.** v6.6's champion consumed no feed at
inference — its climatology was frozen coefficients. Under D-1 the champion needs 42 trailing days of
A75 actuals, so the fresh-data CLI pulls three feeds instead of two: lagged A44 prices, the A65/A01
load forecast, and A75. The bundled Space is snapshot-served and unaffected. This is an ordinary lag
dependency of the same class as the price lags, and it is inside the ~6–10 h D-1 estimate — but it is
a real change to the runtime surface and §0 item 5 must stop claiming otherwise.

### Development selection, reduced to one comparison

Run the two frozen catalogs on the same five development folds, rows, seeds, hyperparameters and
budget. The decision metric is pooled observation-weighted **raw-head** mean pinball loss across all
nine quantiles. Ship the augmented catalog only if its unrounded stored pooled loss is lower; equality
defaults to `base`. Report both losses, their percentage difference, and the selected catalog. This is an ordinary
development-stage model-selection decision, not a confirmatory result.

No blinding, Decimal contract, canonical CSV/JSON, identity manifest, eligibility thresholds,
multi-level tie-break, selection-declaration artifact, or independent adjudication verdict is needed.
The final Integration review verifies the rows are matched and the declared one-line rule was applied.
"The domain feature did not earn its place, and here is the number" is a strong, publishable finding,
not a failure — and it is the answer a hiring manager is most likely to respect.

Delivery-day A69 and all derivatives remain forbidden in the champion. A69 is used only in the trimmed
§7.2 benchmark and, where useful, as a post-hoc evaluation stratum.

### Required deletions and rewrites

- §0 item 3: remove the optional gas browser re-check; keep the merit-order rationale, now carried by
  the single lag proxy under D-1 (or state it as unrepresented if D-1 is declined). Gas stays omitted;
  the A69 benchmark is the only quantified counterfactual for the VRE half of that signal.
- §0 item 5: keep "external weather omitted because the load forecast embeds weather"; replace the A75
  climatology language with the trailing-window definition. **The clause "No actual value is a runtime
  model input" becomes false under D-1 and is replaced verbatim by:** *"No delivery-day or same-day
  actual enters champion inference. Historical A75 actuals through D-2 are permitted LAG inputs."*
  §0 is a ratified-decisions section, so this wording is prescribed rather than left to the executor.
- §3/§4: keep A75 as an ordinary pulled feed; remove A65-A16/A74 requirements, the optional EUA row,
  `expected_scarcity_proxy`, and every runtime/fitting obligation attached to fitted climatology.
- §4.1: delete the OLS basis, the second proxy, four catalogs, retention thresholds, Decimal
  comparisons, canonical CSV/JSON contracts, selection declaration, and the independence split.
  Replace the whole section with a short "frozen strict-gate candidates" section carrying the
  lag-proxy definition and the two-arm development selection above.
- §5.1/§5.2/§6.1/§8.1/§9.1/§11/§13: remove proxy refits, A75 fit lineage, conditional champion
  packaging, four-catalog narratives, and candidate-stage interview answers.
- §9.4: replace the combined schema-and-fit-lineage invariant with a simple schema firewall — champion
  inference rejects A69-derived and same-day actual columns; the benchmark admits only the named A69
  additions.
- CP-1: delete A75 depth-as-separate-gate, fit lineage, per-fold standardization, and the independent
  poisoning-oracle requirement. Add an ordinary unit test proving that the 42-day calculation ends at
  D-2, is unchanged when D-1/D rows are poisoned, and preserves UTC row identity on the fall-back day.
- CP-2: delete the catalog-selection gate, selection artifacts, blind review, and deterministic
  adjudication. The model is compared with the three stated baselines and the one ablation arm.
- All role/template/rule-inventory references to a CP-2 blind/four-catalog surface disappear. The
  ordinary two-arm selection is covered by the single final Integration review; it is not a dedicated
  critic surface or protocol.

**Scientific cost, stated plainly:** the champion tests one calendar/lag-derived VRE expectation
instead of two proxies across four matched catalogs, and the retention decision uses one simple
development metric rather than a mechanically adjudicated multi-condition rule. In return the leakage
surface is smaller than v6.6's fitted-climatology surface, and the report keeps both interpretable
questions: does the domain feature earn its place, and how much does real but post-gate A69
information improve raw quantile loss.

---

## AMD-3 — Keep §7.2 as one run and one number

**Owner decision, 2026-09-06:** preserve the benchmark as an interview answer; do not carry a second
calibrated model through the project.

- Strict arm: the selected strict-gate champion catalog frozen at CP-2.
- Augmented arm: identical folds, rows, seeds, hyperparameters, and training budget, plus delivery-day
  A69 and its named derivatives.
- Run on raw quantile heads before CQR/isotonic.
- Report exactly one headline: pooled mean pinball loss across nine quantiles and five folds,
  expressed as the percentage difference between arms.
- Median MAE may be included only if it comes free from the same stored predictions.
- Do not report coverage, interval width, or calibration error for an uncalibrated comparison.
- The benchmark is never calibrated, registered, deployed, or eligible to replace the champion.

Required limitation:

> This uncalibrated raw-head comparison isolates the information content of post-gate A69. It makes no
> claim about calibrated interval quality and does not make A69 available at the forecast gate.

Update §7.2, §10, the model/benchmark schema invariant, the combined model checkpoint, the release
page, README, and §13 to the same one-number claim.

---

## AMD-4 — Make empirical outcomes reporting obligations, not completion gates

The current plan can permanently block a correct and honest portfolio artifact because the data did
not produce a preferred result. That confuses research outcome with engineering validity.

- CP-2's Fold-5/pooled DM significance rule becomes a reporting protocol. Report statistic, p-value,
  effect size, comparator, and `development_post_selection`; do not require `p<0.05` to proceed.
- The ≥15% pinball improvement remains a narrative target only.
- CP-3's "80% coverage within ±5 pp on 4 of 5 folds" becomes a prominently reported diagnostic, not a
  pass/fail threshold.
- Remove the automatic EnbPI remediation reopen at >10 pp divergence. A miss is shown and discussed; it
  does not silently create a second calibration project.
- SHAP ranking/overlap and regime differences are observations. Require the plots/tables and honest
  interpretation, never a preferred rank, overlap, or direction.
- Training/render/load durations are measured and reported where useful, but exact laptop/network
  timings do not block release unless the artifact is functionally unusable.
- An unfavorable result constrains the public claim. If the selected champion does not beat the
  similar-day naïve on the frozen holdout, the README and interview narrative present a reproducible
  probabilistic-forecasting study and negative result; they do not call the model superior or
  production-performing. Completion is not a license to overclaim.

**One retained hard gate, because it is a correctness property rather than an outcome:** zero
quantile-crossing violations after the full CQR-then-isotonic pipeline. Crossing quantiles are not an
unfavorable result, they are a broken output.

**Scientific cost:** v6.7 may ship a negative result — a model that does not significantly beat the
naïve comparator or whose intervals miss nominal coverage on some folds. That is not a defect if the
pipeline is correct and the conclusion is honest. Fabricating a favorable gate or endlessly tuning
until it passes would be the scientific defect.

---

## AMD-5 — Remove the forward confirmatory audit; keep a frozen holdout instead

Delete §7.1's future-window audit, power calculation, quarantine, `selection_cutoff`, audit manifest,
`PENDING_UNDERPOWERED` / `CONFIRMED` / `NOT_CONFIRMED`, pre-registration, and all dependent fields,
checklist items, reading-order entries, README claims, and interview language. Waiting on future
delivery days is a schedule trap with no defined end, and `PENDING_UNDERPOWERED` is a status no
recruiter will ever read favorably.

### Replacement (decision **D-2**, recommended)

Deleting the audit and putting nothing in its place leaves every number in the project
development-stage and post-selection. There is a version that costs about two hours and needs no
future data at all.

At CP-1, after completeness filtering and before EDA or model development, pin five non-overlapping
tail partitions by complete **delivery day**:

1. **Fold 5:** the latest 90-day development-evaluation block that ends before the first embargo. It
   is the **latest development fold** and joins Folds 1–4 for development selection, diagnostics and
   DM reporting. V6.6's old "final 90 days ending at pull-date" definition is retired, and with it
   Fold 5's role as the current-tail headline evaluation — **that role transfers to the holdout**,
   which is now the most recent partition and the one evaluated on the series the deployed product
   actually serves.
2. **Embargo A:** one complete delivery day. It enters no fit, calibration or evaluation.
3. **Final calibration:** the next 60 complete delivery days. It is excluded from all five development
   folds, hyperparameter/catalog selection, EDA and diagnostic narratives. After selection, it is used
   once to estimate the final CQR thresholds.
4. **Embargo B:** one complete delivery day. It enters no fit, calibration or evaluation.
5. **Holdout:** the final 90 complete delivery days ending at the snapshot cutoff. It is excluded from
   every fold, fit, calibration slice, EDA and development diagnostic.

**The embargo is a principle, not a single boundary.** §5.1's stated job for the embargo is to break
the autocorrelation adjacency between the last fitted target and the first measured feature. That
adjacency exists at *every* fit/measure boundary, so one day separates each of them: final training →
calibration, and calibration → holdout. **The same rule applies inside each development fold**, where
§6.2 currently places the calibration slice flush against proper-training: a one-day embargo goes
there too, so the contract does not hold two different rules for the same hazard. Total cost across
the whole plan: seven delivery days.

**Do not pin a derived date.** The tail spans 242 delivery days from Fold 5's first day to the
snapshot cutoff, which implies some earliest workable pull date — but that constant goes stale the
moment any window changes. CP-1 asserts the property directly instead: `min(fold_5.delivery_date) >=
2025-10-01`, so Fold 5 is verified fully post-transition rather than argued to be.

### The final fit, and which model ships

After the catalog, hyperparameters and all implementation choices are frozen at CP-2, fit the nine raw
heads once on every eligible row strictly before Embargo A, generate fixed-model predictions for the
60-day calibration slice, estimate the four CQR thresholds, attach the deterministic isotonic-last
operation, and freeze that complete artifact. Then evaluate it **exactly once** on the holdout.
Forecasts are generated sequentially, so earlier holdout prices and A75 actuals may enter later
holdout rows only through the already-declared LAG rules; no holdout outcome may enter a fit,
threshold or human development decision.

**The artifact evaluated on the holdout is the artifact that ships.** There is no retrain on the full
snapshot after the holdout is opened. A refit model would be a different set of weights from the one
the reported number describes, and the release page would then be quoting evidence for a model nobody
can see. One model, one number, one story is worth more here than five months of extra training rows.

The consequence is a raw-model fit cutoff **152 delivery days before the snapshot cutoff** (1 + 60 + 1
+ 90). That is a real staleness cost and it is disclosed, not hidden. Since the fit covers every row
before Embargo A, it *includes* Fold 5's evaluation block — the 242-day span above is measured from
Fold 5's first day and is a different quantity from the fit cutoff.

**Four cutoffs, published separately**, on the release page and in the MLflow lineage tags, because
they are four different dates and collapsing them would make the page contradict itself:

| Field | Meaning |
|---|---|
| `snapshot_cutoff` | last delivery day in the committed snapshot |
| `raw_model_fit_cutoff` | last delivery day entering the raw quantile heads |
| `final_calibration_window` | start/end of the 60-day CQR calibration slice |
| `holdout_window` | start/end of the 90-day one-shot evaluation period |

### The one-shot report

It contains champion and similar-day-naïve MAE, champion and naïve mean pinball loss, their percentage
differences, final empirical coverage at 50/80/95, and the **probabilistic daily-vector
Diebold–Mariano** statistic, effect size and p-value against the similar-day naïve. The DM machinery
already exists for the development folds, so this is one call on a different array.

**Label it exactly, and never more strongly than it earns:**

> Pre-specified one-shot holdout DM test on a fixed 90-day window — confirmatory-style, not
> power-qualified.

The retired §7.1 contract required `N_required = max(90 complete delivery days, N_80)`, so 90 was a
**floor**, never a demonstration of adequate power; the window here is fixed by partition design, not
derived from a power calculation, and that is disclosed wherever the number appears. It is not a gate.
A result that does not support superiority forbids the superiority claim and nothing else. `N_80`
itself is **not** recomputed or reported: the power machinery that defined it is deleted, so naming a
quantity the active contract no longer defines would only leave a door open for the machinery to
return.

The result is reported whatever it says. There is no re-tuning, revised model/analysis choice, or
second holdout run after outcomes are opened; honest interpretation of the frozen metrics is required.

No power formula gate, no quarantine manifest, no sealed status, no pre-registration document, no
eligibility computation, no waiting.

**What it buys.** "The walk-forward results are post-selection descriptive evidence; the frozen model
was then evaluated once on a 90-day period it had never seen" is a materially stronger answer than
"no out-of-sample test was performed," and the clean-test question is among the most likely things an
interviewer will press on. It is also the honest version of what §7.1 was reaching for.

**Stated limitation, required verbatim in the report:**

> The holdout is a single contiguous recent period, so it tests generalization to the most recent
> regime rather than repeated out-of-sample skill. Its partitions were pinned before development and
> it was evaluated once, after the complete model and calibration pipeline were frozen, with no
> subsequent tuning. The 90-day length was fixed by partition design, not by a power calculation, so
> the Diebold–Mariano result is confirmatory-style but not power-qualified. The model shown is exactly
> the model evaluated — no refit followed the holdout — so its raw-model fit cutoff precedes the
> snapshot cutoff by 152 delivery days. Sequential lag features may use earlier holdout observations
> exactly as they would in live forecasting; no holdout outcome entered fitting or a development
> decision. Enforcement is procedural: this is a solo build and the discipline is disclosed, not
> cryptographically guaranteed.

If D-2 is declined, keep one clear evidence label instead:

> All reported model-comparison results are development-stage, post-selection descriptive evidence on
> the five pinned walk-forward folds. No separate confirmatory out-of-sample test was performed.

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
- one 3–4 sentence interpretation paragraph using "confirms/justifies," never "proves."

Delete the standalone-module requirement, the `<60s` runtime gate, the optional MSTL, the dependency
policing, and the R-5 overrun-escalation protocol. Budget becomes a non-binding estimate of ~3 h.
Collapse the three current CP-1 spectral checkboxes into one.

**Keep the FFT-bin check as an ordinary unit test, not a gate.** Asserting that `annotate_peaks`
returns a peak within one FFT bin of 1/24 and 1/168 h⁻¹ is about five lines and it is the only thing
standing between the project and a confidently mislabeled figure on the recruiter-facing page. It
belongs with the other targeted tests in CP-1 item 5, not in a separate acceptance protocol.

---

## AMD-8 — Keep DuckDB as a visible SQL artifact, not a second production path

Keep 3–4 hand-authored DuckDB queries against the committed Parquet: lag-24/168, rolling windows, and
null/duplicate/full-bin checks. They must be committed and runnable.

Delete the requirement that DuckDB be the canonical feature source consumed by the model and delete
the duplicate invariant suite on SQL-built columns. **Two feature paths that must agree is double
implementation plus a reconciliation obligation, in exchange for a SQL sample that a single committed
query file already provides.** The Python feature pipeline remains canonical. SQL-B is optional
learning/interview practice and has no deadline, capstone gate, application gate, or program-hours
allocation.

---

## AMD-9 — Simplify the released artifact and remove recurring maintenance

Preserve the recruiter-visible shape: a static GitHub Pages report as the primary URL, a small
interactive marimo Space as the optional deep dive, a public MLflow experiment trace, and a
reproducible repository.

Remove the machinery around it:

1. **No precomputed multidimensional slider/SHAP grid and no per-cell nearest-neighbor OOD flags.**
   Keep the quantile-level selector and at most one simple load-forecast scenario control. Use direct
   local LightGBM inference — one model, one row, milliseconds — or a one-dimensional lookup. SHAP
   remains a static diagnostic. State once that scenario perturbations are sensitivity probes and may
   be out of distribution.
2. **Bundle the champion in the image.** The deployed Space loads the bundled model. Delete the
   registry-first runtime load, the DagsHub secret, and the dual-path fallback — a runtime dependency
   on a third-party registry, guarded by a secret, to load a file already in the image.
3. **Keep the registration itself (decision D-3, recommended).** Register the champion `pyfunc` as a
   DagsHub MLflow model version, assign the current `champion` alias, and attach version tags for
   `release_status=portfolio_release`, `source_run_id`, code commit, and snapshot hash. Current MLflow
   aliases and tags replace the
   [deprecated fixed `Production` model stage](https://mlflow.org/docs/latest/ml/model-registry/workflow/).
   This is a small bounded operation and the cheapest visible MLOps-hygiene signal available. It is
   **non-gating**: if the registry or an
   alias/tag operation is unavailable at release time, the release proceeds and the failed step is
   disclosed. This is the opposite of item 2 — the registry is portfolio evidence, never a runtime
   dependency.
4. **Frozen release, not weekly service.** Delete the Monday snapshot/re-export/commit procedure, the
   ≤48 h freshness smoke gate, and all recurring-refresh language. The page states all four AMD-5
   cutoffs — snapshot, raw-model fit, final calibration, holdout — separately, and MLflow carries the
   same four as lineage tags. A future manual refresh is permitted but never scheduled or required.
   ★(D-2) **What the Space displays over the holdout period is a historical out-of-sample replay**,
   labelled in those words on the page itself. It is not a live forecast and must never be presented
   as one — the honesty of the replay is the point, and an ambiguous label would spend it.
5. **No external-reviewer dependency.** The stranger test becomes optional user feedback, not a
   checkpoint gate. Delete the technical/non-technical reviewer recruitment block. A release cannot be
   blocked on recruiting a volunteer.
6. **No brittle timing gate.** Verify that Pages is static and performs no runtime calls and that both
   Pages and Space render without broken assets. Record observed load time if useful; do not fail a
   release on `<3s`, `<5s`, `<10s`, or `≤30s` platform/network thresholds.
7. **Marketing is outside the engineering bar.** CV and LinkedIn updates are optional Track C actions
   after release, never CP criteria.

---

## AMD-10 — Replace five future milestones/checkpoints with three

The new §12 should be authored from these complete checklists first; all other milestone text and
cross-references should then be made to agree with them.

*Counts assume D-1 and D-2 are accepted. D-3 changes a clause but no item count. Content marked ★
exists only under the decision named.*

### M1 / CP-1 — Data and fixed features (**10 items**)

1. Required snapshot contains A44, A65/A01, benchmark-only A69, and ★(D-1) A75 aggregate VRE from
   2019-01-01 through the pull date, with the known A65 head gap handled and the snapshot hash recorded.
   **The successful pull is archive-reachability and snapshot-completeness evidence, not pre-gate
   availability evidence** — there is no separate existence or archive-depth probe.
2. UTC indexing, Berlin 23/25-hour identity, PT15M→hour aggregation, chunk stitching, missing-quarter
   fail-closed behavior, and the 2025-10-01 price transition are correct.
3. The frozen `base` catalog is implemented with calendar/regime, A65 load forecast, lagged prices and
   closed-left rolling price statistics; ★(D-1) a frozen augmented candidate adds only the 42-day,
   D-2-bounded `residual_load_proxy`. A69 and same-day actual columns are rejected by champion
   inference.
4. ★(D-2) The five tail partitions — Fold 5, Embargo A, the 60-day final-calibration slice, Embargo
   B, and the final 90-day holdout — are pinned without overlap, and `min(fold_5.delivery_date) >=
   2025-10-01` is asserted directly rather than derived from a pull date. Calibration and holdout rows
   are excluded from all development folds and diagnostics; holdout outcomes are excluded from every
   fit and threshold. Each fold's §6.2 calibration slice carries the same one-day embargo. The
   partition and exclusion rules are asserted by a committed test.
5. ENTSO-E↔SMARD prices are reconciled on a fixed stratified sample covering pre-crisis, crisis,
   post-crisis, and the PT15M transition; do not re-compare the whole archive merely because it is
   available.
6. Targeted repository tests cover chunk stitching, a missing quarter, fall-back DST identity,
   closed-left rolling windows, transition aggregation, the schema firewall, the spectral FFT-bin
   assertion, and ★(D-1) the residual proxy's 42-day/D-2 boundary plus its DST behaviour on both
   sides — the target day's repeated/absent local hour and the window's own 43/41-observation counts
   across a fall-back and spring-forward boundary.
7. Leakage audit records every champion feature as KFT/LAG, states the A65 assumption and ★(D-1) the
   A75-revision caveat honestly, and confines A69 to the benchmark/evaluation stratum.
8. Snapshot/data folder and README carry CC BY 4.0 attribution and the data cutoff.
9. Three spectral figures and one short interpretation paragraph are committed.
10. One fresh Integration Critic returns `PASS` on the final candidate from a clean detached checkout.

### M2 / CP-2 — Model, calibration, and analysis (**10 items**)

1. Similar-day naïve, seasonal-naïve-168 h, Ridge, and the nine-head LightGBM candidate catalog(s) run
   on the five pinned development folds within the Apple M3 / 16 GB / CPU-only constraint.
2. MAE, mean pinball loss, and both DM analyses are reported with effect sizes and
   `development_post_selection`; no favorable result is required.
3. ★(D-1) The two-arm raw-head ablation (base vs. base + `residual_load_proxy`) runs on matched folds,
   rows, seeds and budget; the augmented arm ships only if its unrounded pooled mean pinball loss is
   lower, with equality defaulting to base. Both losses, their percentage difference and the selected
   catalog are reported. "No improvement" is a valid, reportable outcome.
4. CQR and isotonic-last are implemented; the 20-row `Q={8,7,5,−1}` fixture passes; raw, post-CQR, and
   final empirical coverage are reported; **final quantiles are monotone with zero crossing
   violations** (the one retained hard gate, per AMD-4).
5. ★(D-2) After catalog/hyperparameter selection, the raw heads are fit on every row before Embargo A,
   final CQR thresholds are estimated once on the distinct 60-day slice, and the complete artifact is
   frozen. The final 90-day holdout is then evaluated exactly once; champion/naïve MAE and mean pinball
   loss, percentage differences, final 50/80/95 coverage, and the probabilistic daily-vector DM
   statistic, effect size and p-value are reported. The DM result carries its exact label —
   *pre-specified one-shot holdout DM test on a fixed 90-day window, confirmatory-style, not
   power-qualified* — and no superiority claim the result does not support. **The frozen artifact is
   the artifact that ships; there is no retrain after the holdout is opened**, and the four cutoffs
   (snapshot, raw-model fit, final calibration, holdout) are recorded distinctly.
6. Champion SHAP and permutation-importance outputs are committed and interpreted without a required
   feature ranking or overlap.
7. Regime-stratified error table includes observation counts, the negative-price stratum, and honest
   thin-slice uncertainty.
8. The one-shot raw-head A69 benchmark reports pooled mean-pinball percentage difference and its
   limitation; no second calibration or deployable artifact exists.
9. Reproducibility/MLflow records for the decision-bearing baseline, champion, and calibration runs
   contain snapshot hash, code SHA, folds, feature list, seed, hyperparameters, metrics, and artifact
   links. No hypothesis/parent/delta/decision bureaucracy is required for every exploratory run.
10. One fresh Integration Critic returns `PASS` on the final candidate from a clean detached checkout.

### M3 / CP-3 — Showcase and release (**6 items**)

1. Bundled champion, CLI, container, and marimo app run locally from a clean setup. ★(D-3) The
   champion is registered as a DagsHub MLflow model version with the `champion` alias and
   release/lineage tags — non-gating; a registry or metadata-operation outage does not block release.
2. Quantile selector and at most one simple scenario control work without the retired
   multidimensional grid, dynamic SHAP, or per-cell OOD system.
3. Static Pages export carries the lean reading order and performs no runtime calls; all assets and
   links render.
4. HF Space deploys the **bundled** champion — the same artifact the holdout evaluated — and renders
   the same release snapshot; free-tier sleep is disclosed, not performance-gated. ★(D-2) Anything
   the Space shows over the holdout period is labelled **historical out-of-sample replay** on the page
   itself, never presented as a live forecast.
5. README, Pages, Space metadata, and MLflow links agree on the selected catalog, metrics, development
   evidence class, benchmark limitation, champion identity, and ★(D-2) the holdout result with its
   power-qualification label and the statement that the shipped model is the evaluated model. All four
   cutoffs — snapshot, raw-model fit, final calibration, holdout — appear separately and identically
   on every surface. Limitations and reproduction instructions are complete.
6. One fresh Integration Critic returns `PASS` on the final candidate from a clean detached checkout.

Old CP-4 and CP-5 are retired. The companion artifact and AWS extension become optional future
projects opened only by a new owner instruction after CP-3; neither starts automatically and neither
is part of the v6.7 completion definition.

**Net checklist change:** 56 future checkboxes across CP-1…CP-5 (17/9/10/7/13, verified at `d5b0b12`)
become **26** across CP-1…CP-3, while every retained checkpoint still has an independent final review.

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
- `final_candidate_sha` plus `evidence_tip_sha`, with a verdict-only delta. **Retained deliberately:**
  it is one `git diff --name-only` line, and it exists because a bar demanding Integration `PASS` "at
  the branch tip" was literally unsatisfiable by any ordering. It is the cheapest surviving piece of
  the machinery and it caught a real defect.
- The single largest gap and the exact next acceptance test — **on `FAIL` verdicts only**. On a FAIL
  it is one or two sentences and it is what makes the verdict actionable. On a PASS it is filler.
- Owner-only LAND decision, evidence tag, and tag-before-delete lifecycle from `AGENTS.md`.

### What retires

- mandatory Builder decomposition and mandatory Builder worktrees for every piece;
- component Critics and per-surface verdicts;
- five-surface scope declarations and all independent fixture materialization/hash ceremony;
- `reviewed_paths` staleness calculations, because there are no earlier component verdicts to reuse;
- mandatory `workbench.md` and its lifecycle;
- raw-second active-elapsed arithmetic, pause ledgers, and `started_at_utc` as first output;
- executor-tier and "brand-new session" gates;
- exhaustive read-scope/provenance declarations and `ASSERTED_ROLE_BOUNDARY`;
- reproducing every brief field inside the Return Packet;
- Builder seed and start/end topology tables;
- formal `BRIEF_INVALID`, `PLATEAU`, and `BUDGET_EXHAUSTED` states;
- duplicate Orchestrator re-validation of every record-level claim.

The Engineering Lead may implement directly or use bounded Builders. If it uses parallel writable
contexts, it still isolates disjoint paths and remains the sole Git writer. These are engineering
choices, not mandatory ceremony. **The Lead may also run an internal review mid-checkpoint at its own
discretion and needs no authorization to do so** — CP-2 in particular is now a large surface, and one
terminal review of a large surface is a shallower review. Stating this explicitly is what prevents
someone later "fixing" the problem by re-mandating component Critics.

### Budget: a timebox, not a ledger

Retiring the raw-second ceiling without replacing it would leave a checkpoint that can run
indefinitely — the failure mode this whole amendment exists to end. Replace it with the smallest thing
that works:

- The brief states **one approximate hour timebox**.
- The Lead reports **approximate elapsed hours**, to the nearest half hour, from ordinary wall clock.
- No `started_at_utc`-as-first-output requirement, no pause ledger, no eligible-pause definition, no
  raw seconds, no arithmetic anyone can get wrong.
- At the timebox the Lead makes one scope check. Crossing it does not invalidate work or force an
  immediate return: the Lead may finish a short, direct path to the existing checklist. Otherwise it
  stops at the next coherent boundary and returns `INCOMPLETE` with what is done and what remains.
  There is no automatic re-brief merely because an estimate was crossed. **A timebox is never
  permission to weaken a bar** — that still requires an owner-ratified amendment.

### New terminal vocabulary

- `PASS` — every checklist item is evidenced and the fresh final Integration verdict is `PASS`.
- `BLOCKED` — an owner credential/action, publication, destructive action, new authority, or plan
  decision is required.
- `INCOMPLETE` — work is coherent and reviewable but one or more checklist items remain open,
  including when the timebox is no longer worth extending.

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
Critic verdict; reproduction commands/results; files changed/diffstat; approximate elapsed hours
against the timebox; open risk or owner action; and proposed disposition/commit message.

`docs/track-b/rule-inventory.md` must preserve its historical tables but add a new v6.7 current-state
section, mark eliminated rules retired, re-baseline the live count from the authored documents, and
stop advertising 168 as the current rule count. Do not guess the new count in advance; compute it from
the final text and record the arithmetic.

---

## AMD-12 — Version, public claims, and parked proposals

1. **Rename the anchor to `capstone_V6_7.md` and declare it v6.7.** This follows the repository's
   actual convention, verified in git history rather than assumed: `6285bf6` renamed
   `capstone_V6_5.md` → `capstone_V6_6.md` (R100), and `ab9eb15`, `888f7de`, `55963e3`, `a3feb06` and
   `34f1cad` did the same at every prior bump. Add a v6.6→v6.7 delta block and update M0's
   ratification history. Repoint every live citation in the same operation — `progress.md` (9),
   `rule-inventory.md` (14), `syllabus_v3_2.md` (5), `notebooklm-role.md` (4),
   `program-stage-sequence.md` (3), `gauntlet-amendment-plan.md` (3), `gauntlet-templates.md` (2),
   `README.md` (1). Leave the historical citations in `cp-0-defects.md`, `evidence/cp-0/*`,
   `spike-feed-status.md` and `pit-metadata-investigation.md` pointing at the name that was current
   when they were written; that is what history is for.
2. Change the stage map from **v7 to v8** and make it the new capstone-first routing aid.
3. Update `progress.md`: v6.7 active, optional syllabus, M1/CP-1 next, no pending amendment, no capture
   blocker, no five-checkpoint/24-hour reserve, no curriculum envelope. Record `D-CP0-18`'s re-test as
   moot and `D-CP0-19`'s as still riding inside CP-1's landing.
4. Rewrite the README's current-status and results language. Remove forward-audit claims, measured
   pre-gate claims, four-catalog selection claims, recurring refresh, health report, and hard speed
   claims. State the two frozen candidate catalogs, the selected champion catalog, development
   evidence, ★(D-2) the holdout result, the one-number A69 benchmark, the frozen snapshot, and the
   three-stage project shape. `README.md` is not locked and its CP-0-pending drift is already an open
   item — fix it here.
5. Mark `aws-extension-spec_v1_1.md` **STALE / NOT SCHEDULED** at the top. Its weekly refresh,
   health-report, lookup-grid, outcome-gate, version cascade, and Month-6 sequencing premises are
   retired. Do not line-edit the parked architecture into apparent currency. If cloud work is later
   desired, write a new proposal against the artifact that actually shipped.
6. Mark `docs/track-b/gauntlet-amendment-plan.md` historical at the top — it plans the ten-form loop
   AMD-11 retires — and repoint its 3 anchor citations.
7. In `PJM_Track_B_Gauntlet_Loop_Guide_HE.md` change only the historical banner's present-tense claim
   that the August mechanisms are “today” part of the ratified plan. State that they were adopted in
   August 2026 and that the active v6.7 contract supersedes or retires them where applicable. Do not
   rewrite the historical body.
8. Keep historical amendment sheets, CP-0 evidence, and defect records unchanged **apart from the
   four bounded regions in `docs/track-b/cp-0-defects.md` named in AMD-1 and the later repair note** —
   the status-summary arithmetic, `D-CP0-18`'s disposition, its clause in the closure sentence, and
   the adjacent AMD-G5 re-tensing. Nothing else in that file moves. History may name
   retired machinery as history; it must not be mistaken for a live requirement.

---

## What v6.7 still protects

- Correct UTC/DST handling and the PT15M→hourly transition.
- Complete-bin ingestion and fail-closed missing-quarter behavior.
- Closed-left lag/rolling features and a strict champion runtime schema.
- An explicit, limited A65 assumption and an explicit A69 post-gate boundary.
- Five pinned development folds across the three regimes, ★(D-2) plus a distinct final-calibration
  slice and one frozen holdout evaluated once — with the shipped model being exactly the evaluated
  model, and a one-day embargo at every fit/measure boundary.
- Transparent baselines, LightGBM quantile heads, CQR, isotonic-last, zero quantile crossing, and
  precise coverage claims.
- ★(D-1) One explicit power-system/merit-order feature, honestly ablated and honestly reported either
  way.
- SHAP, permutation importance, regime/negative-price analysis, and the one-number A69 benchmark.
- A committed redistributable snapshot with attribution, fixed seeds/dependencies, and reproducible
  decision-bearing runs.
- Static recruiter-first presentation plus a small deployed interactive deep dive.
- One genuinely independent, fresh final review per checkpoint.
- Local-only agent work, owner publication authority, and preserved evidence refs.

Those are the parts whose failure would materially damage the project. Everything else should have to
earn its way back through a new owner decision.

---

## Application order

1. **Ratify this sheet, answer D-1/D-2/D-3, and grant one task-scoped suspension naming the nine
   locked files, the `capstone_V6_6.md` → `capstone_V6_7.md` rename, and the amendment-record
   promotion.**
2. **Author the three new §12 checklists first.** They define the destination and prevent old checklist
   fragments from surviving by accident. Adjust counts for any declined decision before proceeding.
3. Apply AMD-1 through AMD-9 across the capstone, working outward from the new checklists.
4. Rewrite `engineering-role.md` and `gauntlet-templates.md` to the AMD-11 loop; then update the
   Orchestrator's Track B briefing/receipt sections.
5. Apply AMD-0 to `orchestrator-role.md` and rebuild `program-stage-sequence.md` v8 from the new Track
   B critical path; add the two banners to `syllabus_v3_2.md` and `notebooklm-role.md`.
6. Execute the rename and repoint all live citations in one operation.
7. Apply README, progress, AWS-proposal, both historical-banner corrections,
   gauntlet-amendment-plan, package, and dead-capture-code consistency edits.
8. Update the rule inventory last, from the text that actually exists.
9. ~~On promotion, collapse the draft-history sections into one provenance paragraph.~~ **Done** —
   see *Provenance* above. The v3→v6 argument belonged to the drafting process; carrying a
   document's disagreement with its own earlier selves into the ratified record would have let
   future readers mistake retired options for live ones.
10. Run the acceptance test below and return one full diff for owner review. Do not publish or land.

---

## Acceptance test for the application task

> **Read the *Post-ratification repair addendum — 2026-09-07* below before running this test.**
> Items **1**, **12** and **15** were superseded on 2026-09-07 by owner-authorized post-ratification
> repairs (addendum R-2, R-3, R-4), and the *Application scope* bullet for
> `docs/track-b/gauntlet-amendment-plan.md` was superseded by R-1. The text of those items is left as
> ratified; the addendum states what replaces it. Every other item stands unchanged.

1. **Scope:** *(superseded in part — addendum R-2)* no file outside the nine locked targets, the final amendment record, the later separately
   authorized `AGENTS.md` repair, and the listed non-locked consistency targets was changed. In
   `docs/track-b/cp-0-defects.md` exactly four bounded regions differ: the status-summary arithmetic,
   `D-CP0-18`'s disposition, its clause in the closure sentence, and the adjacent AMD-G5 paragraph
   re-tensed and marked superseded.
2. **Critical path:** the only live flagship sequence is M1/CP-1 → M2/CP-2 → M3/CP-3. No Track A,
   SQL-B, G0–G5, AWS, companion, reviewer-recruitment, or calendar prerequisite can block it.
3. **Checklist counts:** the counts named in §12 are the counts named everywhere else. With D-1/D-2
   accepted that is CP-1 = 10, CP-2 = 10, CP-3 = 6. D-1 changes CP-2 by one item; D-2 changes CP-1 and
   CP-2 by one each; D-3 changes a clause and no count. Every document follows the decision table.
   CP-4/CP-5 have no live checklist.
4. **No outcome gate:** no live checkpoint requires favorable p-values, effect size, coverage,
   importance ranking, direction, or network/runtime threshold. Quantile monotonicity is the one
   retained hard gate and is a correctness property, not an outcome.
5. **Data scope:** no live requirement fits a per-fold climatology or persists fit lineage; no
   four-catalog, blind-review, Decimal-contract or selection-declaration language survives outside
   explicitly historical text. ★(D-1) `residual_load_proxy` is classified LAG in the leakage audit,
   consumes nothing later than D-2, and passes its 42-day/DST boundary test on both the target day and
   the window. The champion runtime schema rejects delivery-day and same-day actuals while permitting
   lagged actuals through D-2, and no live text still claims that no actual value is a runtime input.
   The two-arm selection is labelled development-stage and applies the declared raw-head rule.
6. **Benchmark scope:** exactly one live A69 benchmark contract exists: raw heads, pooled mean pinball
   percentage difference, optional free MAE, no calibration/deployment.
7. **Assumption:** every live claim about A65's **pre-gate** availability says assumption; none calls
   that pre-gate status demonstrated, confirmed, proven, or measured. ★(D-1) The A75-revision caveat
   appears wherever the A65 assumption does.
8. ★(D-2) **Holdout integrity:** a committed test asserts that Fold 5, both embargoes, final
   calibration and holdout are disjoint, that `min(fold_5.delivery_date) >= 2025-10-01`, and that each
   fold's calibration slice carries its own embargo; calibration/holdout are absent from all
   development folds and diagnostics; holdout outcomes enter no fit or threshold. Sequential lag use is
   limited to observations already available under the declared forecast gate. The report states that
   the holdout was evaluated once after the complete artifact froze, that the shipped model is that
   same artifact with no subsequent retrain, and that the DM result is confirmatory-style and not
   power-qualified. No derived minimum pull date is pinned anywhere.
9. **Review loop:** exactly one mandatory fresh Integration verdict is required per checkpoint; no live
   component-Critic, surface-declaration, oracle-hash, staleness, workbench, provenance, raw-second, or
   five-status requirement survives. A timebox in hours exists and no second-level ledger does.
10. **Release scope:** no live multidimensional lookup/OOD grid, registry-first runtime load, weekly
    refresh, health report, stranger-test gate, hard load-time gate, or CV/LinkedIn checkpoint item
    survives. ★(D-3) Registration uses a current alias/tags contract and is marked non-gating.
    ★(D-2) Any Space rendering over the holdout period is labelled a historical out-of-sample replay.
11. **Dead code:** `src/pit_capture/` and `tests/pit_capture/` are absent from the active tree,
    `pyproject.toml` no longer packages them, and `evidence/cp-0` still resolves.
12. **Rename integrity:** *(permitted-hit list superseded — addendum R-3)* `capstone_V6_7.md` exists and `capstone_V6_6.md` does not. Run the exact-name
    search `grep -rnE '(^|[^[:alnum:]_])capstone_V6_6\.md([^[:alnum:]_]|$)' --include='*.md' . --exclude-dir=.git --exclude-dir=worktrees` — do not use the old substring search, which necessarily matched the live amendment filename. Hits are
    permitted only in `cp-0-defects.md`, `docs/track-b/evidence/`, `docs/spike-feed-status.md`,
    `docs/pit-metadata-investigation.md`, and amendment sheets that explicitly discuss the historical
    anchor. No live document cites a filename that no longer exists.
13. **Cross-reference sweep:** repository-wide searches for the retired vocabulary are either empty in
    live sections or appear only in clearly labelled historical amendment/evidence text. Every live
    reference resolves to an existing section/artifact.
14. **Public consistency:** README, capstone, stage map, and progress agree on v6.7, the frozen
    candidates and selected champion catalog, development evidence, three checkpoints, and optional
    syllabus. ★(D-2) The four cutoffs appear separately and identically on README, Pages, Space
    metadata and MLflow. Both historical-guide banners distinguish past adoption from the active
    contract.
15. **Governance accounting:** *(closure clause superseded — addendum R-4)* the rule inventory's current count is mechanically derived from the
    final documents; prior counts remain labelled historical. `D-CP0-18` reads `MOOT — underlying
    requirement retired by v6.7`, the ledger's closure sentence names `D-CP0-19` alone, and no live
    text still says the ledger waits on a re-test that can no longer be performed. No `N_80`,
    power-formula or forward-audit vocabulary survives in any live section of the capstone or the role
    documents; the amendment sheet's own citation of the retired `max(90, N_80)` contract exists only
    to explain why the 90-day window is not power-qualified.
16. **Repository handoff:** run the relevant tests, `git status --porcelain=v1`, `git diff --stat`, and
    the full diff; list every touched file with one-line rationale and propose one commit message.

---

## Post-ratification repair addendum — 2026-09-07

**Status: POST-RATIFICATION. The substantive ratified requirements above remain quoted unchanged;
post-ratification edits above this heading are limited to a warning block and four inline
supersession pointers** — the *Application scope* bullet's R-1 parenthetical, and one marker each on
acceptance items 1, 12 and 15. This addendum records repairs authorized *after* that ratification
and, where it conflicts with the text above, **this addendum governs**. It exists so
that the acceptance test can be re-run truthfully rather than quietly rewritten — a ratified test
that no longer matches the repository is a defect either way, and the honest fix is a dated
supersession, not a silent edit.

**Trigger.** An independent read-only audit of the applied working tree returned
`PASS WITH NON-BLOCKING NOTES` and raised two P2 findings and seven P3 notes. The Owner authorized
repair of all of them except the finding proposing a standard-error / minimum-effect rule on the
§4.1 two-arm comparison, which was **declined** on the grounds that it would reintroduce the
selection machinery AMD-2 exists to remove. A second authorization then covered `notebooklm-role.md`,
this record, and `docs/track-b/cp-0-defects.md`. Nothing was committed, landed, or published.

**R-1 — supersedes the *Application scope* bullet for `docs/track-b/gauntlet-amendment-plan.md`.**
That bullet reads "historical banner and 3 anchor citations". The three anchor repoints were
**reverted** on 2026-09-07: the file is a historical execution plan for the **v6.6** contract, and
repointing its citations made it assert that the 2026-08-06 clean-room CP-0 re-run was anchored at a
file that did not exist on that date. Two of the three reverts restored the file to its `HEAD` text;
the third corrected a pre-existing corruption from commit `1b1ca21` and now reads
`capstone_V6_5.md` → `capstone_V6_6.md`, which is what that amendment actually produced. **The
historical banner stands; the citation repoints do not.** History records what was, not what is.

**R-2 — supersedes acceptance item 1's `cp-0-defects.md` clause.** The bounded regions are **five**,
not four: the four v6.7-application regions, plus one factual repair made on 2026-09-07 under the
same owner authorization. **In diff order** they are: the status-summary arithmetic (original line
3); `D-CP0-18`'s disposition (line 14); the adjacent AMD-G5 paragraph re-tensed and marked
superseded (line 22); the closure sentence (line 29 — D-CP0-18 struck, D-CP0-20 added, with its
justification in the same paragraph); and the archive-tag description (line 38 —
`archive/cp-0-attempt-1` was recorded as an *annotated ref*, but `git cat-file -t` reports its object
type as `commit`, so it is a **lightweight tag**; every cited SHA remains reachable from it and no
retagging was required). `git diff -U0 -- docs/track-b/cp-0-defects.md` returns **exactly five
hunks**, all confined to the file header (original lines 1–38 of 1134). No defect definition,
acceptance criterion, or item of historical evidence moved.

**R-3 — supersedes acceptance item 12's permitted-hit list.** Add
`docs/track-b/gauntlet-amendment-plan.md` to the files in which an exact-name `capstone_V6_6.md` hit
is permitted, for the reason in R-1: it is a banner-marked historical execution plan whose subject
*is* the v6.6 contract. The governing principle in that item is unchanged and still holds — **no
*live* document cites a filename that no longer exists.**

**R-4 — supersedes acceptance item 15's closure clause.** Read: "**the ledger's closure sentence
names `D-CP0-19` and `D-CP0-20`**". D-CP0-20 was added to the closure condition on 2026-09-07 because
the ledger reported it *remedied but not re-tested* while permitting closure without it. Its remedy
was authored 2026-08-10, four days after the only acceptance test this contract has ever run, so no
exercise of it exists and no other test proved it. The rest of item 15 is unchanged.

**Also repaired under the same authorizations, needing no acceptance-test change:** the §13 hosting
sentence in `capstone_V6_7.md` and the equivalent sentence in `notebooklm-role.md` no longer describe
the Space as *backed by* a DagsHub registry (it loads the bundled artifact and never queries the
registry — §9.2); `notebooklm-role.md`'s milestone range is corrected from `M0–M5` to
`M0–M3 as of v6.7`; the Reg. 543/2013 citations are split into their data and deadline sub-points
(`6(1)(b)`/`6(2)(b)`, `14(1)(d)`/`14(2)(d)`, `16(1)(b)`/`16(2)(b)`), verified against the EUR-Lex
consolidated text `02013R0543-20200101`; Art. 6(2)(b)'s "**updated when significant changes occur**"
revision channel is now disclosed as the second half of the existing A65 assumption rather than as a
third assumption, so every "two disclosed assumptions" statement stays true; and the
`syllabus_v3_2.md` banner now names the **v6.2-era** stranger-test gate and `<3 s` load threshold as
retired, which its v6.4-era enumeration did not reach.

**Third authorized repair round, 2026-09-07.** A later independent read-only audit returned `FAIL`
on seven consistency findings. Under a new task-scoped Lockdown suspension, the capstone's live
test/CI prose and its §13 interview answer were made explicit CP-1 requirements rather than claims
about the current M0 tree; the final weekly-snapshot sentence was replaced by the frozen-release
contract; the Month-0 archive statement was narrowed to its one sampled delivery day; R-2 above was
reconciled to the five-hunk diff created when the CP-0 archive ref was accurately recorded as a
lightweight tag; the stage map was repointed to the existing *Track C activation rules* heading; and
the ratified `Binary Classification Mini-Capstone.md` was restored at repository root byte-for-byte
from the Owner's source (`SHA-256 1a26f069b0b98a541644559a25f5c838e002761773f1c80563fa98426172d817`).
The same authorization covered directly necessary wording in `engineering-role.md` and
`orchestrator-role.md`, which now identify the former M1 oracles as CP-1 test requirements, not
already-committed tests. Nothing was staged, committed, landed, tagged or published, and this repair
does not certify itself; a fresh independent re-verification remains required.

---

## Bottom line

v6.7 is a different, finishable program: no compulsory syllabus, no four-catalog selection
bureaucracy, no result-dependent stop signs, no recurring pseudo-production chores, three checkpoints,
one independent review at each, and a timebox instead of a stopwatch.

What it deliberately does **not** cut is the work a hiring manager actually looks at. One domain
feature, honestly ablated. One clean out-of-sample number. One registry entry. Those three cost
roughly 9–14 hours between them and replace machinery costing several times that — and they are the
difference between a project that is defensible in an interview and one that is merely finished.

The remaining rigor is concentrated in exactly two places: where a silent failure would make the
portfolio claim false, and where a hiring manager will press.
