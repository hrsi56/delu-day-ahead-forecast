> Consolidated 2026-09-16: only `/Users/djourno/Downloads/PJM` on `main` remains.
> All temporary branches and checkout paths below are historical; use `progress.md` for current state.

> CP-10 cleanup: the primary pending-work branch is now `codex/orchestration-pending`;
> `gauntlet/cp-10` below is historical. The experiment is preserved by `evidence/cp-15`.

> Historical handover, superseded by the CP-15 LAND on 2026-09-16. Current state is in
> `progress.md`; retrieve the reviewed chain via `evidence/cp-15` at
> `1bdc75b8ab943092bb8de6ba893defb9e12250d8` and current files in
> `/Users/djourno/Downloads/PJM-main-landing`. The CP-15 branch/worktree has been reclaimed.
> The original handover below is retained unchanged as history.

# Orchestrator handover — 2026-09-15

You are the Orchestrator for `/Users/djourno/Downloads/PJM`.

## Read first, in this order

1. `AGENTS.md` — canonical router and Governance Lockdown.
2. `progress.md` — current state and preserved open decisions.
3. `capstone_v21.md` — the only active plan; §12 is the complete CP-15 bar, §13 the Lead handoff.
4. `orchestrator-role.md` — read its scope-narrowed header before the historical body.

Then inspect actual Git state before relying on this handover. Reply in English. One engineering
track; Track A/C are cancelled. Owner carries one brief to the Engineer and returns one packet.
Do not launch, message or impersonate another executor.

## The decision already made

The owner rejected progressing toward freeze merely because CP-10 had passed its engineering
bar. The product still forecasts poorly under the known crisis regime. The authorized direction
is now improving point forecasts and useful uncertainty together, with a fixed comparison in v21.
Only CP-15 is execution-ready. CP-16–CP-19 require complete future bars and separate briefs.
No new model has been trained under v21; no product-feasibility result exists; no policy or artifact
has been frozen; the prospective 90-day clock has not started.

The owner will give the new Engineer **`docs/track-b/cp-15-brief.md`**. It contains the entire
checkpoint checklist, constraints, return contract, and safe credential-access instructions.
Do not substitute an earlier copy: this final brief includes restored reasoning capture and
byte-exact transport of the corrected AGENTS.md from the older CP-10 base.

Current SHA256 identities:

- AGENTS.md: `4a590cea7fd29f2b230a203f492f179318d50d825aed3d68918b3f7ba932bbee`
- capstone_v21.md: `62e84ceb4f35190c89faffaee4e8af01c5b3c81f9d78f9f3f68556e25f360065`
- CP-15 brief: `0853a3578c886bb11d26fae4ca55b1aef031f3f3558da8ea7ce12ac5b3e72efc`

The Engineer creates a separate local `gauntlet/cp-15` worktree from the verified CP-10 evidence
tip. Only exact supplied AGENTS/v21/brief bytes may be packaged in its pre-run protocol commit;
this is not permission to edit governance or absorb other orchestration changes. Keep the primary
checkout and other sessions' work intact. The launch brief already specifies these boundaries.

## Evidence that stays intact

- v1 is complete, live on Pages, the Static Space and MLflow, and closed.
- Development point-MAE p = **0.948**, statistic **+1.6228**, and median **28.58% worse** than
  similar-day naive remain disclosed. Peak nominal-95% coverage **79/408 = 0.193627** remains
  the v1 result. Neither is a formatting defect or permission to change evidence.
- CP-10's binding fresh Integration PASS applies to its original v20 experiment. Candidate
  `ad3e1a5d5e42d70ea95bbffd01b4563eb2d6d803`; evidence tip
  `4039ce24150b36ea233b043061e68eb2be78cbbe`; verdict
  `docs/track-b/evidence/cp-10/integration.md`.
- Selected calibration: matched August 15–31 peak **131/408 = 32.11%** versus **19.36%**.
  Entire crisis fold **1,515/2,112 = 71.73%** versus **55.54%**. Never interchange the windows.
  Raw forecasts were not refitted; central-forecast MAE remained approximately EUR 141/MWh.
- The previous LAND recommendation was withdrawn. **CP-10 is neither landed nor discarded;
  disposition is an unresolved owner decision.** Preserve its branch and evidence chain.
- CP-3B landed with item 6 unmet: no Integration verdict binds its final candidate. See
  `docs/track-b/evidence/cp-3b/item-6-NOT-COMPLETED.md`. **This is not a precedent. Every brief
  must say so.** No CP-15 terminal PASS without its own fresh binding Integration PASS.

## How to judge the next packet

Check all eight v21 §12 items and the exact-candidate Integration verdict, using the prescribed
Orchestrator packet/Git checks. Separately assess every §8 product criterion. The nine required
policies, causal per-origin normalization, real rolling fits, common residual comparison,
D-2 feedback, matched hours, Chronos-2 feasibility probe and structural-input sheet are fixed.
`PASS` may coexist with `product_feasibility = NOT_DEMONSTRATED`. A best observed candidate
is not necessarily qualified. No automatic promotion or next checkpoint follows either result.

Known development folds remain post-selection evidence. Do not reopen the spent holdout or
reserved outcomes for fitting/selection. Future work would freeze an update policy, not merely
weights, verify initial numeric registry versions/fingerprints, retain state lineage and evaluate
its actually issued future forecasts. This architecture is planned, not implemented.

Read the research memo only as historical motivation if needed:
`docs/track-b/forecasting-research-2026-09-15.md`. It cannot broaden the Engineer's fixed methods.

## What the final governance/documentation task changed

The owner explicitly authorized the amendments after reviewing the proposed scope. AGENTS now
locks current and historical ratified anchors independent of filename case, explicitly naming
v21/v20/M4; retired NotebookLM/syllabus documents remain locked. The original Q&A capture rule
is restored intact and reconciled with v20, v21, the brief and progress. Publication restrictions
are unchanged; only the rationale now says “public repository”.

Reasoning capture is active and separate from cancelled Track C. Only the Orchestrator appends
with `scripts/qa_append.py`. The Hebrew document has **31 entries**; original entries 1–25 are
unchanged, 26–31 cover the new decisions. The Lead only names triggers in its return.

README and local `docs/index.html` explain v1, CP-10's inadequate result and the unexecuted v21
plan. Generator sources and the page-size record are updated. These changes are **local and
unpublished**. Existing public figures, replay payload, frozen metrics and MLflow claims remain
unchanged. New Pages links assume the owner eventually publishes their referenced files too.

One necessary test correction followed an observed failure: changing v20's capture paragraph
invalidated CP-10's exact plan-input hash. We archived the original reviewed plan byte-for-byte at
`docs/track-b/anchors/cp-10-capstone_v20.md` and changed only that input's lookup in
`tests/test_26_cp10_evidence.py`. The recorded lineage hash is unchanged:
`0902a70151cf2a36ef609c35effe49cce725a63eb8ba78478c43421c0507bda4`.
The archive's retired capture wording is historical evidence, never current authority.
No CP-10 source, input, protocol, prediction, result or verdict was revised.

Validation in an isolated plain copy: **217 tests passed**, including the existing live-namespace
synthetic-key control; **make verify passed**; document generators passed. The original run's one
plan-hash failure is recorded honestly. Deliberately corrupting the archived plan failed its
provenance check; restoring it passed. DOCX XML/ZIP preservation and consecutive numbering were
checked without rendering. These checks are not an independent engineering audit of v21.

## Repository state at return — verify again

- Primary: `/Users/djourno/Downloads/PJM`, `gauntlet/cp-10`, HEAD
  `4039ce24150b36ea233b043061e68eb2be78cbbe`, **4 ahead / 0 behind main**, dirty with declared
  local orchestration/documentation work and the provenance-test consistency edit above.
- `main = origin/main = live remote main`:
  `3618658ec16d57795a69c68ccb4cbdab926d73a5` at the final task's check.
- Existing Orchestrator worktree: `/Users/djourno/Downloads/PJM-orchestrator-v20-review`, branch
  `codex/v20-plan-corrections`, same main SHA, **0 ahead / 0 behind**, dirty. Retain it for owner
  review. Its v20-r1 draft has older additional corrections and is superseded as a future plan;
  do not overwrite the primary v20 with it. It lacks CP-10 engineering and therefore does not
  receive the CP-10 test file. Shared handoff/documentation files are synchronized.
- No stage, commit, tag, branch/worktree creation, cleanup, landing or publication occurred in
  the final task. Validation used a plain temporary file copy, with no Git refs.
- Complete local review: `/tmp/PJM-governance-docs-review.md`; primary and isolated patches:
  `/tmp/PJM-governance-docs-primary.patch`, `/tmp/PJM-governance-docs-isolated.patch`.
  Keep the owner-authored landing/publication boundary; do not commit, merge or push on the
  strength of this handover.

The preceding task-scoped governance suspension is **spent at its terminal return**. It grants
no new amendment authority to you or the Engineer. The explicit CP-15 checkpoint authority and
narrow immutable packaging permission remain as written. Do not infer publication authority
from a broad approval for local work.

Your next action: verify the read order and repository state, acknowledge the active CP-15
handoff, and wait for its one terminal packet. Do not re-derive the accepted CP-10 science or
start a competing experiment. If the owner changes the objective, record that decision before
issuing a replacement brief.
