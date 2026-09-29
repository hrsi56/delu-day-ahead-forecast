# PRES-2 — Engineering Lead launch brief

Issued 2026-09-29 at the Owner's request for a handoff to a new execution session.
The text below is the complete launch prompt. Delivery is by the Owner; this document does not
assert that a Lead session has started. The expected dirty primary checkout is handled explicitly.

```text
You are the Track B Engineering Lead.

Read the repository-root AGENTS.md and engineering-role.md. Execute only the
single Orchestrator-issued checkpoint brief pasted below. No read of
progress.md, the syllabus, Track A/C materials, or orchestrator-role.md may
inform any engineering decision; before the final Integration verdict exists,
do not read them at all. If you read any of them afterwards solely to author
the return accurately, say so in one line.

Validate the brief against the required-brief contract in engineering-role.md
before editing the repository. If it is invalid or contradicts the named
ratified plan, say so and get it corrected before doing repository work.

Build the checkpoint however it is best built — directly, or with bounded
Builders in isolated worktrees, your choice. Then review it once, from a fresh
clean detached checkout at the final candidate SHA, with one Integration
Critic. Stop at the terminal checkpoint return and do not inspect, plan, or
begin the next checkpoint.

ORCHESTRATOR BRIEF — BEGIN

# Track B Checkpoint Brief — PRES-2

## Target
- Repository: DE-LU day-ahead forecasting, /Users/djourno/Downloads/PJM.
- Authorized checkpoint: PRES-2, migration of the publication to PUBLISH_RULES 1.0.
  This is presentation work, not reopening PRES-1 or starting CP-21 or Live.
- Ratified publication anchor: docs/PUBLISH_RULES.md, revision 1.0,
  SHA-256 03f106060d9a646ce0c0c986d2f5fb6549929f2ed7270f0c8678fbfd2293b3a3.
- Research constraint anchor, read-only: capstone_v21.md, v21-r4,
  SHA-256 150bd53fa15067b1d138c95d0912f86a1e92ce74092059be09034758c1926167.
  Read its applicable research-preservation clauses, particularly §§2–3, 6–8,
  14 and 15. This brief does not activate any of its research checkpoints.
- Execution plan: docs/track-b/publish-rules-migration-plan-2026-09-29.md,
  revision 1, SHA-256
  24913b2b947aeef585e5994d61c91fed3c9eb0da830d6366c7f749e689b724c8.
- Incorporated baseline: docs/track-b/publication-standard-v1.md,
  SHA-256 01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc;
  docs/track-b/presentation-and-tracking-plan-2026-09-24.md, revision 3,
  SHA-256 281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c.
  Apply the precedence/amendments in PUBLISH_RULES; do not reinstate superseded rules.

## Orchestrator-reported expected state
- Primary checkout: main at 01e394d475202bb44a226f2ac5403aa084dc5b4c.
- Tracked local changes: AGENTS.md and progress.md.
- Untracked: docs/PUBLISH_RULES.md;
  docs/track-b/publication-postdeploy-independent-review-2026-09-29.md;
  docs/track-b/publish-rules-migration-plan-2026-09-29.md; this launch brief.
- No staged changes are expected. All incoming files must be preserved.
- Public Pages HTML last checked: 1,560,646 bytes, SHA-256
  d1227c0f64c6a478f6f076e713e2bed2755edf51d0b8f19522c9b978d42fab3d.
- Public Space revision: 59d941825755bf73eabb7ff20e31124fee305755.
  Demo: released v1. Research presentation: v1–v3. Reverify before relying on these.
- Verify branch, SHA, tree and topology yourself. Report a material mismatch;
  do not discard user work or treat additional unrelated work as permission to overwrite it.

### Baseline assembly: preserve main without requiring a commit on main
The expected dirty tree is not itself a blocker. The plan's P0 allows a separately
authorized baseline arrangement. For this checkpoint, assemble a local candidate
baseline from the verified main HEAD and exact copies of these supplied inputs:
  AGENTS.md;
  docs/PUBLISH_RULES.md;
  docs/track-b/publish-rules-migration-plan-2026-09-29.md;
  docs/track-b/publication-postdeploy-independent-review-2026-09-29.md;
  docs/track-b/pres-2-execution-brief-2026-09-29.md.

Use an isolated project-local checkout and gauntlet/pres-2 under the existing Lead
contract. Keep the primary checkout on main, including all its incoming edits.
The Lead may make local candidate commits only on gauntlet/pres-2. Do not reuse or
overwrite an existing checkout/ref with that name without resolving its ownership.

Copy those files byte for byte: no editing, normalization, rule change or new
ratification. This is packaging of supplied governing inputs into the candidate,
not authority to amend governance. Verify the anchor/plan hashes above and:
  AGENTS.md:
  ce2760612b19eb8321987c5ff1898946d306cf5f60e376922f87b0a160f1d7c4
  independent review:
  74d33d52b38aa96891d156c512c39d3cbcd7cc3484253d6fdae571b2796252cd
Record the launch brief's source/copy hashes and actual baseline commit in new
PRES-2 evidence before implementation. All governing inputs must be present at
the final candidate SHA, so the Critic can check the actual text it is judging.

Do not copy, open, diff or stage progress.md. Its filename/status is context for
preservation only. Avoid broad content diffs of the primary tree that would read it.
No main commit, stash, reset, cleanup or governance amendment is authorized.
If the Owner has already committed the supplied inputs, use that verified baseline
instead and record its real SHA; do not transplant stale versions over newer work.

## Observable outcome
Bring the report, README, Space cards, demo presentation and advertised tracking
routes into conformity with PUBLISH_RULES A1–A6, preserving the actual model,
research results and historical evidence. Build and independently review all
authorized local work through a concrete publication-ready handoff.

The public migration is complete only after authorized publication and P8's
fresh public verification. Do not call a local PASS a deployed migration.

## Complete authoritative checkpoint bar
- Read PUBLISH_RULES in full. Every applicable clause is controlling, including
  all incorporated surviving baseline requirements and the A1–A6 amendments.
- Read the migration plan in full. Its complete outcome and acceptance contract
  is §§1, 3–9, especially the twelve-subject product map (§4), transitions (§5),
  phase exits (§6), complete acceptance matrix (§8.3) and definition of done (§9).
  §7's current touchpoints and implementation suggestions are aids; you own how
  to achieve the outcome. They are not a required module decomposition.
- A7/Live is deferred under its actual trigger, not marked implemented.
- Use docs/track-b/gauntlet-templates.md §§2–3 for Critic/return contracts.
- The checklist is not capstone_v21.md §12 (CP-15). That historical research
  checklist is not PRES-2's presentation acceptance and does not authorize fits.
- Map every applicable item to evidence. No convenience summary below reduces it.

## Task-specific supporting extract
The Owner's priorities, already carried in the anchor and plan:
1. The detailed subjects 1–12 belong to the actual released/frozen product,
   immediately after its opening, not permanently to v1 at the page's bottom.
   Build this for today's released product; make it follow a future valid product
   replacement. Keep research-generation histories concise and the old archive intact.
2. Explain v1→v2 and v2→v3 as adopted transitions. Show rejected experiments
   separately with results and reasons. Preserve predecessor/comparator distinctions.
3. v2→v3 already has direct weather-ablation evidence. CP-16 has intervals against
   daily LEAR and the pooled control, not a paired v2−v1 interval. Do not invent one.
4. Name each headline metric; apply header-aware placement; make important charts
   reachable through descriptive visible routes with closed disclosures initially.
5. Repair the independent review's F01–F04: unnamed demo controls/menu target;
   public favicon 404; hidden startup measurement metadata; missing visible day count.
6. Validate graph/model/population identity. Fold-5 development SHAP and frozen
   artifact in-sample SHAP are different evidence, even if their rankings agree.

## Applicable constraints
- $0 external spend; no new research, fit, holdout opening, data acquisition,
  bootstrap experiment, promotion, daily retraining or live scheduler.
- Preserve the date boundary, saved model and research artifacts, adverse facts,
  v1 archive text/behaviour, prior reviews and pinned dependencies.
- Modify generators/claim sources; regenerate outputs. Preserve inference and
  the existing bitwise-equivalence gate. Check stale ignored payloads separately
  from the public bundle; local staleness is not proof of a public defect.
- Existing MLflow metric/history/artifact preservation remains binding. Even an
  altered historical SVG is substantive under the export diff. New page layout
  must not silently rewrite old experiment artifacts or weaken that test.
- Main, governing documents/configuration, progress.md and locked templates are
  not implementation edit targets. The exact-copy baseline allowance is only
  the packaging operation above. The prior Lockdown suspension is spent.
- Keep temporary worktrees/tools/cache/screenshots inside .local/. Required
  durable evidence goes in its normal project paths with preserved identities.
- Follow AGENTS.md credentials rules. No token values in prompts, logs or files.

## Reviews and evidence
- Perform the full required Chrome/WebKit width, accessibility, keyboard, contrast,
  chart, discovery, zoom/reflow, demo-state and link checks. Inspect actual rendered
  text and charts, not just automated test results. Distinguish local from public.
- Use a separate context-free fresh-reader agent: only closed-state screenshots
  and the six exact questions from PUBLISH_RULES §10.2; save its original answers.
- Use a fresh independent Integration Critic that authored none of the changes,
  in a clean detached candidate checkout. Supply only the prescribed Critic inputs.
- After final build/index changes, obtain the required exact-SHA focused recheck.
  Retain one binding final PASS and a verdict-only evidence-tip delta.
- Read-only verification of existing public MLflow/routes is authorized. If the
  export is unchanged, freshly verify it rather than reuploading unnecessarily.
- Never replace public evidence with a local tracker/browser result. Retain first
  failures and retries; disclose incomplete accessibility/tool coverage honestly.

## Timebox
Approximately 32 hours, orientation through terminal return. Report elapsed time
to the nearest half hour. At the estimate, follow the role's scope check; do not
weaken the bar or stop a short direct repair merely because the estimate elapsed.

## Owner-only actions already authorized
None: no mainline write, remote mutation, MLflow upload, Space upload, push, release,
destructive operation or new governance edit. The Owner's delivery of this brief
authorizes the local checkpoint and exact-copy baseline assembly described above.
Existing credentials may be consumed as stored variables only where an authorized
operation needs them; anonymous reads should remain anonymous.

If a public write is necessary, finish all independent local work and produce its
exact reviewed payload/diff and remaining operation. Do not reuse PRES-1 permission.
Do not ask the Owner to mediate ordinary implementation or internal review repairs.

## Stop and return
Use the complete §3 checkpoint-return form, adding the publication packet and
applicability matrix. Write new records under docs/track-b/evidence/pres-2/ and
reports/presentation/release-checks/pres-2-*; do not overwrite earlier attempts.

Return exactly PASS, BLOCKED or INCOMPLETE as the role defines. When all authorized
local work is ready but Owner publication is pending, return BLOCKED at that external
gate, explicitly stating local readiness and any binding Integration PASS. This is
not a product FAIL. PASS for the full migration requires the authorized public steps
and their postdeploy evidence; never report them performed when they were not.

Name final_candidate_sha and evidence_tip_sha, show their verdict-only diff, identify
the exact bundle and output hashes, list all changed files and checks/limits, account
for every branch/worktree/ref, and supply a concrete Owner landing/publication packet.
Do not land, merge, stage or commit on main, publish, push or begin another checkpoint.

ORCHESTRATOR BRIEF — END
```
