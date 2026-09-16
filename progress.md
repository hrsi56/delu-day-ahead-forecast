# Programme state — DE-LU day-ahead forecasting

*Orchestrator-owned. **Updated 2026-09-16 for the owner-authorized CP-15 landing under v21-r1.**
Single-track programme; current authority is below, historical checkpoint evidence remains intact.*

**The one active plan: [`capstone_v21.md`](capstone_v21.md) — *Adaptive forecasting with measured
product quality*, revision **v21-r1**, history correction owner-authorized 2026-09-16.** The owner approved execution of the research
direction and necessary plan replacement; the Orchestrator drafted the detailed specification
under that authority. This does not claim sentence-by-sentence owner review. Only CP-15 has a
complete execution-ready bar. No new engineering session has been launched by the Orchestrator.

**Prior isolated correction, now superseded as a future proposal:** `capstone_v20.md` **v20-r1** was owner-authorized
and available for review in `/Users/djourno/Downloads/PJM-orchestrator-v20-review`, branch
`codex/v20-plan-corrections`. It was never adopted on `main` or in the CP-10 checkout; retain its uncommitted work for review.
v21 carries forward the useful registry/lineage and convention corrections under the new design.
CP-10 returned against its original v20 anchor; no brief or anchor was changed mid-run.
The prepared review is at
`/Users/djourno/Downloads/PJM-orchestrator-v20-review/docs/track-b/v20-plan-review-2026-09-15.md`.

**Verified starting state, 2026-09-15:** `main` = `origin/main` = live remote `main` =
**`24da4bd13188a4d0e4e7589c61206d8cd62e5ae8`**; tree clean before CP-10 briefing.
191 passing tests and the completed repository audit are accepted from the handover, not rerun.
At brief delivery, local unstaged changes are this file and `docs/track-b/cp-10-brief.md`;
no commit, stage, branch, worktree, tag or publication was made by the Orchestrator.

---

## 1. Current Position

**v1 is complete, live, and closed. CP-10's engineering PASS is accepted against original v20,
but the owner rejected proceeding toward landing/freezing as the next objective. The owner has now
authorized the adaptive forecasting direction. CP-15 completed its nine-policy comparison
under v21-r1 with a fresh binding Integration PASS. Engineering PASS is accepted; product
feasibility remains NOT_DEMONSTRATED. A1 is best among A1–A5; no candidate qualifies.
The known peak improved substantially in development, but the released v1 evidence is unchanged
and no qualified replacement has been promoted. The owner authorized LAND of the completed
experiment and its inherited CP-10 work, including commit, merge and push for this task.
The reviewed experiment is at `land/cp-15`; the original chain is at `evidence/cp-15`.
No v2 policy is frozen; the 90-day clock has not started.**

| | | |
|---|---|---|
| **M1 / CP-1** | Data layer, fixed features | `land/cp-1` · `evidence/cp-1` |
| **M2 / CP-2** | Model, calibration, analysis | `land/cp-2` · `evidence/cp-2` |
| **M3 / CP-3** | Showcase and release | `land/cp-3` · `evidence/cp-3` |
| **M3.5 / CP-3B** | WASM showcase on a Static Space | `land/cp-3b` · `evidence/cp-3b` |
| **REL-1** | Publish | **complete** — all four conditions met |
| **CP-10** | M4 calibration, original `capstone_v20.md` §9 | **Engineering PASS accepted; inherited work landed with CP-15; primary dirty branch retained for pending orchestration edits** |
| **CP-11 → CP-14 (old v20)** | Retired future sequence | **never started; superseded by v21** |
| **CP-15** | Adaptive forecasting feasibility, v21-r1 §12 | **LAND complete; Engineering PASS; product NOT_DEMONSTRATED; A1 best challenger, none qualified; branch reclaimed** |
| **CP-16 → CP-19** | v21 §10 direction | **not authorized; complete future bars required** |

### The three live surfaces

| | |
|---|---|
| **[Static report](https://hrsi56.github.io/delu-day-ahead-forecast/)** | The primary link. The full §10 reading order in one self-contained file that makes **zero network calls** — it cannot sleep and cannot break when a CDN does. |
| **[Interactive Space](https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast)** · [app direct](https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/) | The champion's own boosters running in the browser under Pyodide, proved **bitwise equal** to the frozen artifact. A Static Space executes nothing, so it never sleeps. ~57 MB first visit, ~1 MB after. |
| **[MLflow on DagsHub](https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow)** | Every decision-bearing run, anonymously readable. |

### What v1 actually claims

The champion beats the similar-day naive on the one-shot holdout on **both** metrics — MAE
25.9078 vs 27.7578 (−6.66 %), mean pinball 6.7083 vs 13.8789 (−51.67 %), DM p 1.98e−18 — and that is
the only confirmatory evidence in the project. Everything else is `development_post_selection`.

**Two results are deliberately unflattering and must stay that way.** The point-MAE DM in
development is `p = 0.948` with statistic **+1.6228** — the median is 28.58 % *worse* than the
naive, dominated by fold_3, the August-2022 crisis peak. And the 95 % interval covered **0.194** of
outcomes over the August-2022 peak weeks. **That collapse motivated v20; v21 now addresses both price forecasting and uncertainty**, and it is documented on every public surface. It is not a bug to quietly repair.

**Recovered v1 interpretation, from `2517e55:progress.md` and the preserved CP-2 report:**
fold 3 was not trained exclusively on pre-crisis data. Training ran through 2022-04-29 and
included 5,784 crisis hours. The recorded diagnosis was shrinkage toward the training level;
61.3% of evaluation observations exceeded the training 99th percentile, while only 2.45%
exceeded its maximum. These are historical reported measurements, not a new recomputation.
The selected `base` catalog excluded the losing residual-load proxy (13.0158 vs 13.0642
mean pinball, +0.3715% for the augmented arm). The measured 19.49% strict-gate information
cost did not authorize using post-gate A69. Preserve the four distinct cutoffs (snapshot,
raw fit, final calibration, holdout), the no-retrain identity, and the semantic fingerprint
used because pickle bytes were not stable. These v1 findings do not preselect CP-15’s winner.

---

## 2. What happens next

**Current disposition — CP-15 LAND, owner-authorized 2026-09-16.** The owner explicitly
permitted commit, merge and push for this landing. This task-specific instruction authorizes
these operations; it does not amend the standing rulebook or permit model promotion.

- Experiment landing: `0be8e56726262336ead20adc70c69668ba59e1f6` (`land/cp-15`).
  Its Git tree is exactly the reviewed evidence-tip tree, `53a093a8ae22d9bc8dc93ac127008c6cd124e244`.
- Permanent evidence reference: `evidence/cp-15` at `1bdc75b8ab943092bb8de6ba893defb9e12250d8`.
  This preserves both CP-15 attempts and all four inherited CP-10 commits and their candidate SHAs.
- CP-15's completed branch/worktree are reclaimed. Current evidence paths resolve in
  `/Users/djourno/Downloads/PJM-main-landing`, the new clean main checkout. Historic briefs,
  verdicts and receipts retain their original execution paths; use this mapping for retrieval.
- The dirty primary CP-10 checkout and `codex/v20-plan-corrections` checkout remain preserved.
  Their pending documentation, Q&A and test edits are not included in the experiment landing.
  CP-10 code is included, but its old checkout remains open for that pending work.
- Local backups, full experiment diff, resource-retention mapping and verification records:
  `/Users/djourno/Downloads/PJM-cp15-landing-record-2026-09-16/`.
- Landing accounting: [CP-15 landing record](docs/track-b/cp-15-landing.md).
  No policy freeze, promotion, holdout opening or prospective clock follows this landing.
- Next step: define the bounded CP-16 experiment and its complete bar from the CP-15 result.
  Keep B2 and A1 as references; prioritize demonstrably available historical input vintages
  and stronger challengers, then adaptive uncertainty. This is planning direction only:
  the exact candidate set, acceptance bar and new brief need owner authorization and a
  scoped amendment to the locked plan. `NOT_DEMONSTRATED` remains the product conclusion.


**Historical receipt before disposition — completed CP-15, 2026-09-16: Engineering PASS accepted;
product_feasibility = NOT_DEMONSTRATED.** A1 (normalized LEAR) ranks first among A1–A5;
qualified policy: none. This accepts experiment completion, not checkpoint closure, model
promotion, a relaxed product screen, publication, or authorization for the next checkpoint.

- Full owner-supplied packet: `/Users/djourno/Downloads/PJM-cp15-r1-handoff/checkpoint-return.md`.
  Candidate: `fc4aee038cf898998a292506df62ddb0dcfaf22a`; evidence tip:
  `1bdc75b8ab943092bb8de6ba893defb9e12250d8`; pre-run protocol:
  `bb5e67882fcfdf65b963d25ce785a3999816dfc2`. Binding verdict and final scientific report:
  `docs/track-b/evidence/cp-15/integration.md` and `report.md` at that evidence tip.
- All eight v21-r1 §12 items map to PASS evidence in the exact-candidate verdict. The Critic
  reports 339 tests/no skips, independent saved-metric agreement within 5.7e-14, all 240 paired
  bootstrap contrasts reconstructed, two production origins reproduced exactly, production
  causal controls, and all four Chronos-2 probe digests matched. It did not refit every origin.
  Original A65 vintage availability remains an assumption; the peak is only 17 days and all
  development inference remains exploratory after selection.
- Every policy covers the same 10,747 eligible hours, 96,723 predictions across nine policies.
  Full fold 3 is 2,112 hours / 88 represented days in the original 90-calendar-day window;
  peak is 408 hours / 17 days. No missing/nonfinite/crossed emitted quantiles were reported.
  The fixed 2019 boundary and capped expanding-history policy were retained.
- A1’s six product criteria: (1) FAIL, S_MAE 0.6722908121 >0.5920298211;
  (2) FAIL, S_WIS 0.6460150916 >0.5750919367; (3) PASS, full-fold coverage
  93.1450%–95.6401%; (4) PASS, peak 378/408, MAE 49.876699 ≤57.617759 and
  WIS 29.403713 ≤33.729705; (5) FAIL, fold-1 MAE 6.819900 >6.530233;
  (6) PASS, complete finite ordered forecasts. A1/A3/A4/A5 fail 1/2/5; A2 fails 1/2/4/5.
- Interpretation from the reported tables: A1 is the best challenger, not the best policy on
  the primary equal-fold scores. B2 (raw rolling LEAR) has S_MAE 0.6578109124 and
  S_WIS 0.6389910407, both lower than A1. A1 has slightly better pooled scores and better
  peak behavior. On the matched peak, v1→A1 MAE is 275.25954→49.87670 EUR/MWh, coverage
  79/408→378/408, and mean interval width 418.23701→275.86208 EUR/MWh. This is substantial
  observed development improvement in both point error and intervals, not coverage bought
  solely by widening. It does not prove normalization is the overall best choice, isolate
  every causal contribution of the new pipeline, or provide future confirmation.
- Prescribed packet/Git checks reconciled: 28 commits above main, including four inherited
  CP-10 and three first-attempt CP-15 commits; main-to-tip scope 150 files / +147,745 / −12.
  All 16 candidate-to-tip paths are inside CP-15 evidence. All cited local commit objects
  exist. Branch is clean, 28 ahead / 0 behind main. Only the retained CP-15, primary CP-10
  and Orchestrator worktrees remain; temporary Builder/Critic worktrees are absent; no new
  tags. Main/origin/main and the checked live remote remain at
  `3618658ec16d57795a69c68ccb4cbdab926d73a5`. Original FAIL is preserved at
  `docs/track-b/evidence/cp-15/attempt-1-integration.md`, with its original chain reachable.
- The Orchestrator inspected the packet, verdict and scientific report and ran repository
  checks; it did not read engineering source, rerun tests or independently recompute scores.
  Lead reports approximately 2.5 hours for resumption plus the prior 0.5-hour attempt, $0
  external spending. Post-return reads were a filename-only citation scan, disclosed.
- Orchestrator recommendation: LAND the completed experiment/evidence subject to the owner’s
  decision about CP-15 and its inherited CP-10 work. The earlier CP-10 standalone LAND
  recommendation remains withdrawn; no CP-10 disposition is silently inferred. Nothing has
  been landed, tagged, published, promoted, discarded or reclaimed by this receipt.
- Interview-capture trigger from the Lead: improved crisis and pooled performance did not
  meet the predeclared equal-fold product screen; original hours and thresholds were retained.
  Q&A remains owner-managed; no document entry was appended in this receipt.

**Historical handoff — CP-15 resumption, owner-authorized 2026-09-16, now returned.**
Complete replacement: [CP-15 resumption brief](docs/track-b/cp-15-resumption-brief.md).
The owner approved the exact capped expanding-history proposal and the task-scoped Lockdown
suspension for the plan and directly necessary briefing/routing edits.

- Active plan: `capstone_v21.md`, **v21-r1**, SHA256
  `44ea4e545d2caa276a36a7a70db6ea044b3975196ead06f3ce59f976c83354b3`.
- Replacement brief SHA256: `b6a24e40f13f28ad0b459395f6969d29fa6ebc86b5d688fa8ed246475556b280`.
- B2/B3/A1/A2 use calendar dates `[max(2019-01-01, D - 728 days), D)` for delivery
  day D, subject to the inherited forecast-origin timestamp and availability filters, for evaluation and genuine warm-up. A4 remains exactly 84 days.
  No additional market history, changed target rows, weaker product criteria or reduced
  checklist was authorized. Remaining input/normalization/warm-up sufficiency must be proved.
- The existing clean `/Users/djourno/Downloads/PJM-cp-15` worktree is the authorized execution
  context, on `gauntlet/cp-15` at `193d9cf48c586b9c4b1f43d7a5677b2d5f400832`, verified
  7 ahead / 0 behind main. Main/origin/main/live remote main all remain
  `3618658ec16d57795a69c68ccb4cbdab926d73a5`. No branch, tag or worktree was created.
- The Engineer receives narrow permission to copy the exact revised plan and replacement
  brief into that branch before any comparison, preserve prior evidence, and complete the
  same checkpoint. Original v21 and the first brief remain at the original evidence tip.
  A later canonical verdict must preserve the old FAIL byte-for-byte at a distinct evidence
  path and report the mapping. The original candidate is never retrospectively rescored.
- Approximately 12 hours for the resumed run, with the earlier approximately 0.5-hour blocked
  attempt reported separately. All eight checklist items, all nine policies, all six product
  criteria, both feasibility deliverables and a fresh binding Integration review remain required.
- Only plan, replacement brief and affected progress sections were prepared in the two
  Orchestrator checkouts. The Engineer’s checkout and evidence were untouched. Q&A stays
  owner-managed at 30 questions in the primary document; no append or synchronization occurred.
  The amendment suspension is spent at this task’s terminal return; no further governance edit,
  publication, mainline operation, disposition or cleanup is authorized by it.

**Owner correction and history recovery, 2026-09-15:** the archive’s start is a deliberate
standing decision. Commit `4ec9fab` added it to progress; `2517e55:progress.md:106` still stated
“The data window starts 2019-01-01 and not earlier.” Commit `8d56942` removed that line during
regeneration. Q&A entry 2 has retained the original explanation since `7aaa02b`, with its text
unchanged. The Orchestrator missed this surviving context before recommending earlier history;
that recommendation is withdrawn. July 2018 prices belong to the pre-split DE-AT-LU product,
so they cannot silently extend the same DE-LU target series. Even the post-split tail of 2018
does not supply the full July-start window. Full recovery inventory and source references:
[`progress-context-recovery-2026-09-15.md`](docs/track-b/progress-context-recovery-2026-09-15.md).

**Historical receipt — CP-15 attempt 1, 2026-09-15: BLOCKED; Integration FAIL;
product_feasibility = NOT_DEMONSTRATED (all six criteria unassessed).** No comparison ran,
no best observed or qualified policy exists, and CP-15 remains open.

- Candidate: `f8d0ed2a5f0737f0d088c3474b5a9fe77a406f37`; evidence tip:
  `193d9cf48c586b9c4b1f43d7a5677b2d5f400832`; preflight protocol commit:
  `884261d30284877092eadda9bfb6704f0ec1e890`. Original verdict at the first evidence tip:
  `docs/track-b/evidence/cp-15/integration.md`; its preserved current path is
  `docs/track-b/evidence/cp-15/attempt-1-integration.md` on `gauntlet/cp-15`.
  Owner-supplied complete return: `/tmp/cp15-handoff/checkpoint-return.md`.
- The packet and binding verdict establish that the snapshot starts 2019-01-01. Fold 1's
  first required 728-day window starts 2018-07-04: 181 days / 4,345 canonical hours absent.
  The optimistic first warm-up origin requires 210 days / 5,041 hours before the archive.
  All 90 fold-1 evaluation origins lack leading support. These are received findings,
  not an Orchestrator recomputation.
- All eight checklist items are mapped in the packet/verdict. Item 1 is partial: preflight
  prerequisites passed, but the comparison protocol remains unfinished. Items 2–8 are unmet.
  Existing controls do not prove an unimplemented CP-15 pipeline. The Chronos-2 probe and
  structural-input sheet were not performed; the history blocker does not establish that
  those independent tasks were impossible. All six §8 criteria are unassessed, not failures
  measured against thresholds. No inference about adaptive-model quality is supported.
- Critic-reported validation: 223 tests passed; preflight reproduced byte-for-byte with
  deliberate exit 2 and zero fits; 1,190 window calculations and saved original row counts
  checked (10,747 total, peak 408 hours / 17 days). Separate feature-eligibility reconstruction
  was terminated for runtime and contributes no evidence. Reported preflight resources:
  19.14 seconds / 188,973,056 bytes RSS. Elapsed checkpoint time: approximately 0.5 hours
  against 12 hours; blocked on a data/plan decision, not time.
- Prescribed Orchestrator Git checks passed: seven commits above main (four inherited CP-10,
  three CP-15); main-to-tip scope 27 files / +5,660 / −11, reconciling the packet's CP-15-only
  14 files / +2,528 / −11 with inherited CP-10 work. Candidate-to-tip delta is only the CP-15
  Integration verdict. All cited commit objects exist. Branch/worktree/tag inventory matches
  the return; gauntlet/cp-15 is clean at the evidence tip, seven ahead / zero behind main.
  `/Users/djourno/Downloads/PJM-cp-15` is retained; `critic-cp-15` is absent. No CP-15 tag exists.
  Primary CP-10 and the declared Orchestrator worktree remain in place.
- The Orchestrator read the return and verdict and checked repository records; it did not
  read engineering source, rerun tests, reproduce fits or recalculate results. Receipt accepts
  BLOCKED as the reported execution status, not checkpoint completion. No landing, discard,
  cleanup, replacement brief, amendment, publication or later checkpoint is authorized here.

**Original handoff, now returned BLOCKED: [CP-15 Engineering Lead brief](docs/track-b/cp-15-brief.md).**
One complete prompt, one checkpoint, approximately **12 hours** from orientation to return.
The owner carries it to the Lead; the Orchestrator does not launch or impersonate an executor.

**v21 changes the experiment:** real rolling fits, causal price normalization, short/long history
and simple ensembles; common rolling residual uncertainty; a named foundation-model feasibility
probe and a structural-input feasibility sheet. All nine core policies are required. Candidate
ranking and product criteria are specified in advance. A fresh Integration verdict remains
mandatory, and `product_feasibility` must appear beside engineering status. Neither 32%/40%
coverage nor engineering PASS permits freezing or promotion.

**Forecasting policy rather than frozen weights:** the eventual prospective evaluation will
measure the same policy that runs daily, including its prescribed updates. Exact initial registry
versions/fingerprints and subsequent state lineage remain required. No prospective clock starts
in CP-15. No reserved outcome partition is opened.

| Checkpoint | Next purpose | Current authority |
|---|---|---|
| CP-15 | Completed adaptive forecasting experiment | LAND complete; Engineering PASS; product NOT_DEMONSTRATED |
| CP-16 | Stronger neural/structural challengers and adaptive uncertainty | Requires results, exact method set, bar and new brief |
| CP-17 | Freeze/register a qualified update policy | Requires demonstrated feasibility and future complete bar |
| CP-18 | Operate that policy and its scorecard | Requires future bar and explicit publication authority |
| CP-19 | Prospective evaluation | Requires policy freeze, elapsed horizon and future complete bar |

**Historical preparation state, before CP-15 execution:** local main, origin/main and live remote main all resolve to
`3618658ec16d57795a69c68ccb4cbdab926d73a5`. Primary checkout remains on `gauntlet/cp-10` at
`4039ce24150b36ea233b043061e68eb2be78cbbe`; it has orchestration-only pending files.
The Lead must use a new isolated `gauntlet/cp-15` worktree based on that CP-10 evidence tip,
without switching or cleaning the primary checkout. The existing Orchestrator worktree stays on
`codex/v20-plan-corrections`, 0 ahead/behind main, dirty with declared planning work. No new
branch, worktree or tag was created by this preparation task.

**Governance/documentation validation, 2026-09-15:** completed in a plain isolated file copy
of the CP-10-based checkout, using the existing pinned environment with package imports confirmed
inside the copy. No Git branch/worktree was created for testing. `make readme-cp3 pages` passed;
`uv run pytest -q` finished with **217 passed**; `make verify` passed with no cross-surface claim
disagreements, no fetching references and no gated tracking links. The first suite run had
216 passes and one historical-anchor hash failure caused by the authorized v20 scope edit.
The byte-exact archived anchor and narrowly corrected provenance lookup resolved it without
changing CP-10's recorded hash, inputs, source, protocol, predictions or verdict. A deliberately
corrupted archive made that check fail; restoring it made the check pass. The original Q&A
content, section properties and all other DOCX parts are unchanged; numbering is consecutive
through 31. The Pages figures and interactive replay/coverage data are byte-identical to before.
These are regression/documentation checks, not a fresh CP-10 or CP-15 Integration verdict.

**Prepared local documentation:** README, Hebrew Q&A, `docs/index.html`, generator sources and
its build-size record. They have not been published. Final handoff:
[`docs/track-b/orchestrator-handover-2026-09-15.md`](docs/track-b/orchestrator-handover-2026-09-15.md).
The owner can carry the final CP-15 brief to a new Engineer and this handoff to a new Orchestrator;
no agent session is launched here. CP-15 packages only exact AGENTS/v21/brief bytes, not this
broader documentation work. Full local review files are `/tmp/PJM-governance-docs-review.md`,
`/tmp/PJM-governance-docs-primary.patch` and `/tmp/PJM-governance-docs-isolated.patch`.

**CP-10 receipt retained below as historical evidence, not current routing authority.**

**Current receipt — CP-10 only:** the owner returned one `PASS` packet from the
[Engineering Lead brief](docs/track-b/cp-10-brief.md), reporting approximately **0.5 hours** against
the **4-hour** timebox. The Orchestrator accepted it against the original v20 checkpoint bar after
the prescribed packet checks. No new brief or executor was launched. CP-3B's missing item 6 is
not a precedent: CP-10 has a committed fresh Integration PASS binding its exact candidate.

**Binding evidence and repository checks:**

- `final_candidate_sha`: `ad3e1a5d5e42d70ea95bbffd01b4563eb2d6d803`.
- `evidence_tip_sha`: `4039ce24150b36ea233b043061e68eb2be78cbbe` on `gauntlet/cp-10`.
- Verdict: `docs/track-b/evidence/cp-10/integration.md` at the evidence tip; all seven checklist
  items and supporting invariants mapped to evidence, with exact commands, exit codes and a
  declared fresh clean detached review checkout. The verdict binds the final candidate above.
- `git log --oneline main..<evidence_tip_sha>` shows the four claimed commits: protocol,
  implementation, comparison evidence, Integration verdict. `git diff --stat main...<evidence_tip_sha>`
  matches **13 files / 3,132 insertions**. The candidate-to-evidence-tip name-only delta contains
  only `docs/track-b/evidence/cp-10/integration.md`.
- `git branch -vv`, `git worktree list` and `git tag --list` reconcile with the return: the
  checkpoint branch is **4 ahead / 0 behind main**; its Critic worktree is removed; no CP-10 tag
  exists yet. The separate Orchestrator branch/worktree remains declared and untouched by CP-10.
  `main` and `origin/main` remain `3618658ec16d57795a69c68ccb4cbdab926d73a5`.
- `git cat-file -e` succeeded for both terminal SHAs, the main baseline, protocol commit
  `5e16ad1600b30ef8a2d66eb32c1cc6c90973b7ed` and implementation commit
  `093692560b78c0ccb47a0ceb83428718c028090d`. The original working-tree exception was this
  unstaged Orchestrator-owned progress file; no engineering work was left uncommitted.

**Accepted results, as independently evidenced in the verdict:** C-1 trailing price volatility
was selected on folds {1,2,4,5}, pooled pinball **4.385529023835001** over **8,635 observations**.
The Critic reports **217 passing tests**, seven reproduced artifacts matching byte-for-byte,
zero crossings over **75,229 rows**, and independent reconstruction of **1,792 ACI origins**.
The Orchestrator read the committed verdict and checked the packet against Git; it did not rerun
tests, read engineering source or independently recompute the metrics.

**Scientific disposition:** full-fold coverage is **1,515/2,112 = 71.73%** versus v1
**1,173/2,112 = 55.54%**. On the matched August 15–31 peak window, coverage is
**131/408 = 32.11%** versus v1 **79/408 = 19.36%**, an improvement of **12.745 percentage points**.
The literal full-fold threshold of 0.394 clears even for v1; the matched peak improvement is below
20 points. The return and Critic disclose this and retain v1 as recommended. ACI's documented
coverage-state update and quantile-rank mapping are consistent, with hit/miss fixtures; the
earlier notation concern does not establish an implementation defect or require a rerun.

**Disposition undecided; previous LAND recommendation withdrawn following owner feedback.**
The owner requested research toward a better forecasting product, not progression based on this
result. That is not a DISCARD instruction. Preserve `gauntlet/cp-10` and evidence tip
`4039ce24150b36ea233b043061e68eb2be78cbbe`; no landing, tag or reclamation has occurred.
The existing disposition/preservation procedure applies when the owner decides. Live citations
include `docs/track-b/cp-10-brief.md`, `progress.md`, and the isolated research memo below.
**CP-10 remains open.** No CP-11 brief, freeze, promotion or holdout opening is authorized.

**Session record, 2026-09-15:** owner authorized the proposed CP-10 scope and requested that the
four `launchctl` variable names be recorded in both brief and progress. Corrected the stale
`8d56942` starting-state reference to the verified commit above. Preserved the handover's existing
decisions, open items and historical evidence; no governance or ratified anchor was changed.

**Author-note receipt, 2026-09-15:** owner relayed four previously session-only notes from the
plan's author; their findings and verification limits are preserved below. The Orchestrator's
read-only state check found the shared checkout on `gauntlet/cp-10` with a modified
`tests/test_25_cp10_calibration.py`; that engineering change belongs to the active execution,
was not inspected or altered, and is not an unexplained branch requiring disposition now.
This receipt updates only program state, does not amend the dispatched brief or ratified plan,
and is not a checkpoint verdict.

**Correction session, 2026-09-15:** the owner granted the requested task-scoped Lockdown
suspension and required that the Engineer's work not be overwritten or interrupted. Created the
separate branch/worktree above from `main` at `3618658ec16d57795a69c68ccb4cbdab926d73a5`.
Copied the existing Orchestrator receipt into this worktree and made all subsequent changes here;
the original checkout's files and branch were left untouched. Prepared ACI notation and frozen
registry-loading corrections, reconciled the daily alias and dependency prose, and corrected
availability citations. No code, test, result, active brief, candidate or verdict was inspected or
changed. No stage, commit, tag, publication, merge or ref deletion was performed.

**Next orchestration action:** prepare the CP-16 scope decision from the landed experiment.
B2 and A1 are the reference pair suggested by the results; neither is promoted. The full
future bar and exact candidates require a scoped plan amendment and a new brief. Preserve
the 2019 boundary, original eligible hours, released v1 evidence and attempt-1 FAIL.

**Receipt session, 2026-09-15:** terminal packet and committed verdict read; prescribed Git
checks passed; engineering PASS accepted without converting it into a successful calibration-fix
claim. Synchronized this operational receipt across the primary and isolated worktree copies of
`progress.md`, preserving all prior open items and correction history. No plan, engineering file,
verdict, ref, tag, branch, worktree, index or commit was changed in this receipt session.


**Earlier research session, before the present approval:** primary literature reviewed against CP-10's reported limitations.
The comparison left fold-3 median MAE essentially unchanged at approximately EUR 141/MWh and
used fixed raw forecasts; its very conservative ACI grid and fixed score reservoir do not test
rapid adaptation. These observations are taken from the engineering report, not a source audit
or new experiment. The research memo records German crisis-era target-normalization evidence,
trend decomposition, adaptive conformal methods, 2026 foundation-model evidence, and a structural
merit-order alternative with unestablished fuel-data access. It proposes evaluating a frozen
**update policy** prospectively, including its prescribed state changes, rather than using a
separate frozen artifact as evidence for an adaptive product. This is unratified.

**Research deliverable:**
`/Users/djourno/Downloads/PJM-orchestrator-v20-review/docs/track-b/forecasting-research-2026-09-15.md`.
All suggested thresholds and comparisons are proposals; no new brief, training run, engineering
audit, publication, secret access or governance edit occurred. The prior task-scoped Lockdown
suspension ended at the correction task's terminal return and is not reused for this research.
The Orchestrator updated only this operational state in both checkouts and added the research
memo in its existing isolated worktree.

---

## 3. Blockers / Open Questions

- **Q&A owner edit completed.** The owner deleted entries 31 and 32 and reports 30 questions;
  read-only XML inspection confirms questions 1–30 in the primary document. No agent append
  or correction is pending. The isolated Orchestrator worktree still contains the older
  32-question copy; it is stale and must not overwrite the owner’s primary document.
  No DOCX synchronization was performed; the owner manages its content.
- **Product feasibility remains NOT_DEMONSTRATED after completed CP-15.** A1/A3/A4/A5 fail
  criteria 1, 2 and 5; A2 also fails criterion 4. No candidate qualifies. The experiment’s
  engineering requirements, including both feasibility deliverables, passed the binding review.
  Chronos-2 was an unscored feasibility probe; source/vintage/reuse gaps and pretraining overlap
  remain limitations, not evidence of a deployable neural or structural model.
- **CP-15 disposition resolved: LAND.** The owner explicitly authorized this experiment landing,
  including commit/merge/push. `land/cp-15` marks the exact reviewed tree; `evidence/cp-15`
  retains the reviewed chain. The completed checkpoint branch/worktree are reclaimed.
- **CP-10 inherited code landed; pending checkout retained.** Its four commits are included in
  the CP-15 landing and preserved by `evidence/cp-15`. The primary dirty checkout remains
  available for separately pending orchestration/docs/Q&A changes; no model promotion follows.
- **Registry-loading correction — adopted in v21 §9 as a future requirement.** Exact initialization
  versions/fingerprints and refusal before outcome access are required, including state lineage
  for prescribed updates. No registry implementation or prospective freeze is claimed.
- **CP-10 ACI convention — implementation concern resolved; historical clarification retained.** Original
  v20 §4.3 uses a coverage indicator without defining the parameter's convention.
  [Gibbs–Candès (2021), §2, equation (2)](https://arxiv.org/html/2106.00170v3#S2.E2)
  defines alpha as miscoverage and uses the noncoverage event. With that convention the plan's
  indicator gives the wrong feedback direction; the written formula can instead describe a
  coverage-level parameter if explicitly defined and used that way. v20-r1 defines the paper's
  convention, requires hit/miss direction fixtures, permits a documented and tested equivalent
  coverage parameterization, and preserves D-2 feedback. **The CP-10 packet and binding Critic
  verdict now resolve the implementation concern:** the Lead used a consistent coverage-state
  parameterization and demonstrated hit/miss directions. No engineering remediation is requested
  for that concern. v21 uses an empirical residual benchmark initially; a later adaptive method
  must define its parameter convention explicitly. No clarification changes CP-10 retrospectively.
- **Independent plan review limits remain explicit.** The author reports that ratification was
  followed only by self-review, not an independent audit. The handover's nine corrected repository
  defects do not establish that the forward plan has been independently audited. This receipt
  checks the registry gap and ACI convention; the isolated correction also reconciles direct
  registry, dependency and citation inconsistencies. Further questions are recorded in
  the isolated `docs/track-b/v20-plan-review-2026-09-15.md`: frozen ACI state versus “no re-threshold”, the
  peak-only 0.194 baseline versus whole-fold wording, CP-11 feature/preregistration requirements,
  and daily data timing/source consistency. v20 was superseded without claiming that audit complete.
  v21 receives Orchestrator consistency checks here, not an independent engineering verdict.
  CP-15 requires fresh independent Integration, and prospective stages need complete reviewed bars. The CP-10
  packet now demonstrates the denominator problem and reports both windows honestly; changing
  future plan wording still requires a properly authorized amendment rather than retroactive scoring.
- **Live-namespace guard — control re-run during authorized validation, 2026-09-15.** The
  docstring confirms that the two guards precede live claims. The existing synthetic-key positive
  control ran and passed in the 217-test suite. This verifies the present prefix guard, not a
  future daily system; no live publication or prospective model was exercised. The initial
  author-note receipt itself involved no test execution.
- **⚠ CP-3B item 6 was never completed.** No Integration Critic verdict binds its final candidate
  `55a70e7`: round 1 FAIL, round 2 FAIL then repaired, round 3 cut off twice by usage limits. The
  Lead returned `INCOMPLETE`; the owner directed release. Recorded at
  [`docs/track-b/evidence/cp-3b/item-6-NOT-COMPLETED.md`](docs/track-b/evidence/cp-3b/item-6-NOT-COMPLETED.md)
  with the Orchestrator's substitute verification described for exactly what it is and is not.
  **This is not a precedent** — active `capstone_v21.md` §12 requires a binding verdict, and
  every brief must say so.
- **A cold first visit to the Space can meet a `429`.** Immediately after an upload, Hugging Face's
  own edge rate-limited a burst of ~176 parallel asset requests and the page rendered blank; a
  reload cleared it. Transient, but a first-time visitor can hit it.
- **`reports/cp3/pages_build.json` stamps `built_on` with the build date**, so regenerating on a
  later day dirties that record. No published surface moves. Fold it into the next regeneration.

**Closed and not to be re-opened:** the CP-0 defect ledger (20 defects, closed 2026-09-14); the
ENTSO-E outage (resolved, and the v2 daily path uses SMARD anyway); PRE-2 / DagsHub MLflow; the
`hrsi56` vs `Yarden-Viktor` Hugging Face account; the missing LICENSE.

---

## 4. Lessons that cost something

Each of these was paid for once. None should be re-learned.

- **Compression must preserve decision reasons.** `8d56942` removed the 2019 market boundary
  and other standing context while claiming every load-bearing fact survived. That omission
  became operationally relevant in CP-15. Read the surviving decision record before proposing
  a remedy; recover a decision with its provenance instead of treating silence as a reset.
- **Check the forecasting task before the implementation.** The old row-wise availability
  rule was correct for a different forecast shape. Its historical lesson survives: reason
  from one whole-day issuance and admissible information first. Constrain semantics, not
  specific SQL syntax. This is planning context, not permission to redo the Lead’s audit.
- **Plan for source and scheduler failure.** The historical ENTSO-E outage justified the
  prearranged fallback; the earlier scheduler lesson was not to rely on a free GitHub Actions
  schedule for a hard deadline. Future operating design needs explicit timing/failure handling;
  the old observation is not a newly verified statement about a provider’s present service.
- **A clarification can expose an unverified assumption.** The plan author's receipt note names
  three such cases: a later checkpoint's actual coverage, a platform's free tier, and whether two
  stages are distinct. Check the relevant artifact or current primary source before answering;
  neither a confident prior answer nor ratification is verification.
- **A green test run is not evidence.** CP-1's first attempt returned `PASS` from its own Integration
  Critic while **95.83 % of its rows leaked**, because every test inherited the same wrong premise.
  An independent pre-landing audit caught it and paid for itself on first use.
- **Where a test asserts something does *not* happen, it needs a positive control that proves it can
  fail.** An assertion satisfiable by an inert implementation is not an assertion.
- **Fix the generator, not the output.** A value corrected in a file while the script that writes
  that file still emits the old one is silently reverted by the next build. This happened here: a
  MiB/MB label was fixed in a report while `scripts/cp2_report.py` still divided by 1,048,576 and
  wrote `MB`.
- **A brief that asserts a platform fact must re-verify it.** The CP-3 brief told a Lead that
  Hugging Face's free tier served Docker Spaces. It had stopped two months earlier. The Lead built
  the whole container path against a constraint that no longer existed.
- **Tell a Lead to verify the state it is told it is starting from.** Two separate Leads caught
  factual errors in Orchestrator-issued briefs — wrong SMARD filter IDs, and crossing counts that
  were the two arms stacked rather than the champion's. Both were right.
- **Read a return for protocol defects as well as for its verdict**, and verify the hard gate
  independently rather than re-running the Lead's own suite.
- **Grep for conflict markers when opening a session** — `^<<<<<<<`, `^=======$`, `^>>>>>>>`,
  `Updated upstream`, `Stashed changes`. Commit `30b1b9f` published six of them to a public repo.
- **The holdout is opened once.** v1's is spent permanently. v2 gets its own, and the model that
  ships is the model that was evaluated.

---

## 5. Setup State — environment, access and pending handoff

- **Role routing.** `AGENTS.md` is the canonical router and carries the Governance Lockdown;
  `CLAUDE.md` points at it only; `orchestrator-role.md` governs programme management;
  `engineering-role.md` governs execution. `docs/track-b/gauntlet-templates.md` has the four forms.
  > Both `orchestrator-role.md` and `program-stage-sequence.md` carry a **scope-narrowed header**:
  > everything in them about Track A or Track C is historical. Their Track B governance is unchanged.
- **Credentials — never printed, logged or committed.**
  - **Owner-confirmed 2026-09-15: available through `launchctl`:** `DAGSHUB_USER_TOKEN`,
    `MLFLOW_TRACKING_URI`, `HF_TOKEN`, `ENTSOE_API_TOKEN`. This is supplied access information,
    not an Orchestrator credential test; no values were read. Check inherited process variables
    first; an already-running session may not have inherited later `launchctl` settings. If
    necessary, capture `launchctl getenv <name>` privately inside the consuming process and
    report presence/absence only, never raw output. Access does not authorize publication or cost.
  - `MLFLOW_TRACKING_URI`, `MLFLOW_TRACKING_USERNAME`, `MLFLOW_TRACKING_PASSWORD` in `~/.zshrc`.
    **Auth is HTTP basic, not Bearer** — Bearer returns `401`. `DAGSHUB_USER_TOKEN` being present
    does not by itself establish that the MLflow client is configured.
  - `HF_TOKEN` via `launchctl setenv`, reaching a session by **process inheritance**. It authenticates
    as `Yarden-Viktor`.
  - `ENTSOE_API_TOKEN` present. **`entsoe-py` 0.8.0 passes it as a query parameter**, so it appears
    in request URLs *and in raised exception text* — redact before logging, and prefer SMARD in any
    unattended job.
  - **Verify anything set in `~/.zshrc` with `zsh -ic`, not `zsh -lc`.** A login but non-interactive
    shell does not source it; an earlier probe reported variables absent and was wrong.
- **Link discipline.** The DagsHub *repository* UI answers `302 → /user/login` anonymously despite
  `private=False`. **Every public link uses the `.mlflow` host**; `scripts/check_links.py` carries the
  four gated URLs as a control.
- **Hugging Face.** Account `Yarden-Viktor`. Docker and Gradio Spaces moved behind paid PRO on
  2026-07-08; **only Static Spaces are free**, and a Static Space never sleeps.
  `hf upload` returns `402` because the CLI calls repo-create even when the repo exists — use
  `HfApi.upload_folder` against the existing Space.
- **Compute.** DagsHub gives tracking, registry and storage and **no compute**. GitHub Actions is
  **free and unmetered for public repositories**. Local: Apple M3, 16 GB; CPU core comparison and bounded local MPS probe under v21,
  **$0 expected external run rate**. The inherited $65/month ceiling is not spending authorization.
- **Which check covers what.** `make verify` binds the item-5 *claim* set across surfaces — cutoffs,
  catalog, metrics, evidence class, benchmark. It does **not** check URLs; the test suite and
  `scripts/check_links.py` do. Naming the wrong one in a bar was a real defect found at handover.

---

## 6. Standing Scope Decisions

### Recovered standing context — sources preserved, 2026-09-15

These are recovered decisions and evidence limits, not a new anchor or an amendment to v21.
The detailed source/disposition inventory is in the context-recovery report above.

- **Data begins 2019-01-01 by design.** DE-LU split from DE-AT-LU on 2018-10-01; earlier
  prices represent a different market product. The 2019 start was chosen to cover the
  pre-crisis, crisis and normalization regimes without adding a different target series.
  It is not a source outage, accidental truncation or an invitation to fetch all available history.
  Source: `4ec9fab`, retained at `2517e55:progress.md:106`, and Q&A entry 2.
- **Two inherited data-vintage assumptions remain disclosed.** A65/A01 load-forecast
  pre-gate availability was assumed, not empirically established by pre-gate captures.
  A post-gate observation or stable archive does not prove earlier availability. A75 actual
  generation in the historical 42-day, D-2-bounded proxy uses the archive’s current values,
  not a proven record of values visible at each past origin. Its revision status is the
  second assumption. Keep both limitations with any historical leakage/availability claim;
  inherited tests do not turn them into measured guarantees. These do not relax v21’s
  causal-input requirements. Sources: `2517e55:progress.md:98–99`, historical v6.8 §§3/5.2/R-2.
- **SMARD was the planned fallback-primary source.** CP-1 used it when ENTSO-E was unavailable,
  under the existing fallback clause; that choice did not itself require an amendment.
  Cross-source reconciliation still required ENTSO-E to return and subsequently closed.
  The 2019 cutoff is independent of this outage/fallback history. Source: `2517e55` standing
  decisions and CP-1 receipt; Q&A entries 1–3. This records the existing-source decision,
  not blanket authority for new sources or changed targets.
- **Hourly means and canonical delivery hours remain the target.** The historical contract
  keeps an hourly target across the 2025-10-01 quarter-hour market transition; native
  quarter-hour features require hourly aggregation across the archive, with complete-bin
  and chunk-boundary handling. Preserve 23/24/25-hour delivery-day identity. The recorded
  2025 snapshot count of 576 negative hourly means and the regulator’s 573 are different
  reported quantities, not interchangeable corrections. Sources: progress before `888f7de`,
  `2517e55`’s negative-hours note, historical v6.8 §§4.0/9.4, Q&A entry 15.
- **Owner observance constraint:** no scheduled work on Friday or Shabbat. Restored from
  `2517e55:progress.md` and originally recorded at `38001da`; cancellation of Track A/C did
  not record a withdrawal of this preference. Any future operational schedule must resolve
  its scope explicitly rather than assume the owner’s availability. Nothing is scheduled now.
- **Retired controls stay retired.** AMD-G5’s negative control was knowingly waived; the old
  point-in-time capture ledger, publication-metadata substitution and four-catalog selection
  machinery were retired by recorded owner decisions. Restoring their history does not reopen
  them or waive CP-15’s own current tests. The old forward-audit design is history; v21’s
  future prospective requirements govern. Sources: `2517e55` standing decisions/notes and
  historical v6.8’s supersession record.

**Carried forward; explicit v21 changes are named here:**

- **Track C — cancelled 2026-09-15.** Outreach, CV surfaces, LinkedIn, target research and interview
  rehearsal left this repository. `TRIG-C` and `C-1` are struck.
- **Reasoning capture — reinstated by the owner, 2026-09-15.** `AGENTS.md` § *Interview-answer
  capture* applies to ongoing engineering decisions, independently of Track C distribution.
  Only the Orchestrator files entries through `scripts/qa_append.py`; the Lead names a trigger in
  its return. The owner-edited primary `שאלות תשובות.docx` now has **30 questions**, verified
  by read-only XML inspection. The owner removed entries 31 and 32; earlier session records
  describing their creation are historical, not the present count. No agent append is pending
  for this correction. The isolated worktree’s older 32-question copy is stale; preserve the
  primary owner-edited document. CP-15’s comparison is now complete; this receipt makes no
  Q&A edit. The Lead’s new interview-capture trigger is retained in the current receipt.
- **Track A — out**, as it already was in practice. `syllabus_v3_2.md` gated nothing.
- **No implemented fuel-price layer.** v21 permits a read-only structural-input feasibility sheet;
  it does not grant purchase or redistribution rights. Earlier source finding, 2026-09-15: every TTF/THE source found is
  commercial with redistribution-prohibiting terms; ACER publishes a daily *LNG* assessment, not a
  hub price. A reproducible open repository that cannot legally ship its own inputs is not
  reproducible — see [`DATA-LICENSE.md`](DATA-LICENSE.md).
- **Gate-legal weather forecasts begin in 2024.** Open-Meteo's archive reaches 2017 but stitches
  short-lead-time runs, which is look-ahead. **Folds 1–3 are unreachable**, so the data track cannot
  touch the crisis regime and no surface may imply it can.
- **The inherited delivery-day availability invariant remains mandatory (v21 §2).** Masking delivery-day prices must change
  the output by exactly `0.0`; a D−1 mutation must move it. Currently `220.9433` EUR/MWh.
- **Amendments granted and spent:** WASM for CP-3B only (§9.2's "server mode, not WASM"), and
  sequential conformal for C-2 only (§13's EnbPI/SPCI exclusion). v21 is a separately authorized
  plan replacement: it opens the stated modelling comparison and future policy direction only,
  not an unlimited method set or reusable governance suspension.
- **Optional, unscheduled, neither starts on its own:** `Binary Classification Mini-Capstone.md` and
  `aws-extension-spec_v1_1.md` (stale).

---

## 7. Where the history lives

**Pending local documentation context (not part of the reviewed experiment landing):** the
following archive/test consistency edits and the earlier research/handover notes remain in
the two preserved Orchestrator checkouts unless individually stated otherwise. Main retains
the original reviewed v20 anchor and test.

**CP-10's exact reviewed anchor** is additionally preserved at
`docs/track-b/anchors/cp-10-capstone_v20.md`, copied byte-for-byte from final candidate
`ad3e1a5d5e42d70ea95bbffd01b4563eb2d6d803`, SHA256
`0902a70151cf2a36ef609c35effe49cce725a63eb8ba78478c43421c0507bda4`.
Its old capture wording is historical evidence, not current instructions. The necessary
`tests/test_26_cp10_evidence.py` consistency edit in the primary checkout now checks that
archive against CP-10's unchanged lineage hash; data/source/protocol checks remain in place.
The isolated main-based Orchestrator worktree lacks CP-10 engineering and does not receive that test.

This file no longer narrates it. It is preserved and addressable:

- **The reviewed chains** — `evidence/cp-0`, `evidence/cp-1`, `evidence/cp-2`, `evidence/cp-3`,
  `evidence/cp-3b`, `evidence/cp-15` (including the CP-10 chain). Each landing was a squash with one parent, so the candidate SHAs are **not** on
  `main` and the tag is the only thing preserving them. Verdicts are at
  `docs/track-b/evidence/<cp>/`.
- **v1's ratified plan** — `capstone_V6_8.md`, with its amendment sheets. History, not instruction.
- **M4's reasoning** — `capstone_M4_v2-plan.md`, including the one Orchestrator recommendation the
  owner overruled and why. Superseded by `capstone_v20.md` §4–§5.
- **The defect ledger** — `docs/track-b/cp-0-defects.md`, closed 2026-09-14 after 40 days.
- **v1's results** — `docs/cp2-model-report.md` and `reports/cp2/`. Evidence; not to be changed.
- **Everything else** — `git log`. Commit messages in this repository carry the reasoning, not just
  the change.


## 8. Strategic Anchors

- **Only active plan:** `capstone_v21.md`, revision **v21-r1**, original design authorized
  2026-09-15 and capped expanding-history correction approved 2026-09-16. Active checkpoint
  none: CP-15 is landed/closed; §12 remains its immutable bar. CP-16 is direction only,
  awaiting a complete authorized bar and brief.
- **Historical authorities:** original `capstone_v20.md` for CP-10; `capstone_V6_8.md` for v1.
  Original v20 methods and bar remain unchanged; only its reasoning-capture scope paragraph was
  reconciled with the restored rule. Isolated v20-r1 retains its separate, superseded corrections.
- **Target:** DE-LU hourly day-ahead price forecasting with the inherited forecast-origin and
  eligibility contract; improve point predictions and honest, useful uncertainty.
- **Budget/hardware:** local M3 / 16 GB, CPU core and bounded local MPS probe; no external spending.
- **Language:** English. **Track A/C:** outside programme scope, as recorded above.
- **Governance:** AGENTS.md canonical; engineering-role.md and templates unchanged. All current
  and historical ratified anchors stay locked regardless of filename case, explicitly including
  v21, v20 and the M4 companion. Retired NotebookLM/syllabus material remains locked for completeness.
  Routing pointers and active capture instructions are reconciled; publication and mainline history
  remain owner-only. CP-15 may package exact supplied AGENTS/v21/brief bytes only, under v21 §13.

## 9. Session Log — newest first

- **CP-15 LAND, 2026-09-16:** owner explicitly authorized landing and publication of the
  completed experiment, including inherited CP-10 work. Squashed the exact reviewed tree
  into `0be8e56`, tagged `land/cp-15` and `evidence/cp-15`, repointed current routing and
  reclaimed only the completed CP-15 branch/worktree. Preserved all pending work in the two
  other checkouts and archived checkpoint-local caches/logs. Product NOT_DEMONSTRATED,
  no freeze/promotion, no prospective clock, no next-checkpoint execution. Operational
  landing documentation is a separate commit; the reviewed experimental tree is unchanged.

- **CP-15 completed receipt, 2026-09-16:** accepted Engineering PASS after reading the
  complete packet, exact-candidate verdict and final report and performing the prescribed
  Git checks. Product NOT_DEMONSTRATED remains controlling. Recorded A1’s candidate rank,
  B2’s stronger primary scores, the large matched-peak improvement and all six criterion
  outcomes. Both feasibility deliverables completed within their stated limits. Recommended
  owner LAND of the experiment with explicit CP-10 ancestry; no disposition or next brief
  issued. Only operational progress copies updated; Q&A and engineering untouched.

- **v21-r1 resumption preparation, 2026-09-16:** owner explicitly approved the proposed
  history rule and task-scoped Lockdown suspension. Amended §5’s four long-history table cells
  and rule, identified the revision, and reconciled §13 for the retained worktree and evidence
  preservation. The complete §12 checklist and §8 product criteria are byte-identical. Supplied
  one replacement brief for the same Lead; no session was launched or messaged. Original
  brief, attempt-1 branch contents, candidate and FAIL remain unchanged. No resumed model
  comparison, training sufficiency or product feasibility has been claimed.

- **Engineer acknowledgment and owner Q&A edit:** owner relayed the Lead’s confirmation:
  2019-01-01 stays fixed, earlier-history ingestion is withdrawn, evidence tip remains
  `193d9cf48c586b9c4b1f43d7a5677b2d5f400832`, Integration FAIL and all unassessed/unperformed
  items stand; no edits or execution resumed. This is an acknowledgment, not a new checkpoint
  packet or disposition. Owner reports deleting Q&A entries 31/32; primary numbering 1–30
  verified, isolated stale copy recorded. Only operational progress was updated here.

- **Owner follow-up, 2026-09-15:** owner will correct the Q&A himself and requested a
  response to the same Engineering Lead. Prepared a receipt clarification preserving the
  2019 boundary, BLOCKED/Integration FAIL evidence, and pending plan/disposition decisions.
  No amendment or resumed engineering execution is authorized by this response.

- **Context recovery after owner correction, 2026-09-15:** traced the 2019 data boundary to
  `4ec9fab`, its deletion to `8d56942`, and its unchanged surviving explanation to Q&A entry 2.
  Audited all 25 standing-decision bullets immediately before the rewrite, plus relevant
  setup, notes, historical receipts and earlier hourly-target history. Restored applicable
  context with provenance; kept intentionally superseded model/track rules historical.
  Withdrew this session’s earlier-history recommendation and recorded the CP-15 planning
  conflict. No ratified plan, governance file, brief, engineering evidence or ref was changed.

- **CP-15 blocked receipt, 2026-09-15:** complete packet and committed exact-candidate
  Integration FAIL inspected; prescribed Git checks reconcile. Recorded the missing-history
  prerequisite, all eight unmet/partial checklist statuses and all six unassessed product
  criteria. Owner history decision and separate CP-15/CP-10 dispositions remain open.
  Captured the reasoning in Q&A entry 32 using the required appender. Synchronized only
  operational progress and Q&A copies in the two Orchestrator checkouts; engineering, anchors,
  briefs, evidence and refs untouched. No new executor or experiment was started.

- **Governance and documentation reconciliation, 2026-09-15:** owner granted the explicitly
  proposed task-scoped amendment after review. Verified the case-sensitive lock mismatch;
  named current and historical anchors, reinstated reasoning capture, preserved retired locked
  material, and changed only the publication rationale to “public repository”. Reconciled v20,
  v21, the CP-15 brief and the role's filename pointer. The corrected AGENTS travels byte-for-byte
  with the CP-15 plan because its CP-10 base contains the old rulebook. Restored capture produced
  entries 26–31 via the required appender. README and local Pages content now distinguish released
  v1, completed CP-10 evidence and planned CP-15; their generators preserve that distinction.
  No Engineer session was launched or interrupted. No stage, commit, branch/ref mutation or
  publication is authorized or performed by this task; this amendment authority ends at return.

- **v21 preparation, 2026-09-15:** owner granted full approval to execute the researched direction.
  Treated that approval as task-scoped authority for this specific plan replacement and directly
  necessary routing/state consistency edits. Wrote v21 and one CP-15 brief; synchronized copies
  into the primary checkout without changing its branch or engineering files. Narrow immutable
  plan/brief packaging is expressly authorized for the Lead's pre-run candidate commit. No other
  governance editing is delegated. This preparation authority is spent at this task's terminal return.
- **Research:** completed primary-source review; withdrew LAND recommendation; no model trained.
- **CP-10 receipt:** accepted binding engineering PASS; product defect unresolved; no disposition.
- **v20-r1 correction:** isolated owner-authorized draft completed; no publication; now superseded
  as future direction by v21, with its necessary registry and causal-policy issues carried forward.
- **v1:** complete and closed; exact historical evidence and public surfaces preserved above.

## 10. Notes for Future Sessions

- CP-15 now distinguishes experiment validity from product feasibility. Use its B2/A1 tradeoff
  when the owner chooses
  whether to refine adaptation, add information or prioritize the named stronger challengers.
- No CP-16–CP-19 executor starts without its own complete bar and brief. No prospective clock
  starts until an eligible policy and its update/evaluation rules are frozen.
- Carry forward known weather-vintage, fuel-rights, delayed-feedback and registry-loading limits;
  none is solved merely by having a token, a newer library or a successful local test.
- No Track A/C follow-up, application task or optional project is scheduled. Engineering reasoning
  capture remains active when its rule triggers.
