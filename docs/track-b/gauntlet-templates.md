# Track B — Canonical Templates (v6.7)

Boundary-contract forms, not a second capstone plan. The ratified plan named in `progress.md` is normative; `engineering-role.md` owns the execution process; `AGENTS.md` owns branch, tag and publication authority. Replace every bracketed field; never infer an anchor from the highest version on disk.

Isolation is a plain `git worktree` at the candidate SHA. The verdict is a markdown file committed under `docs/track-b/evidence/<checkpoint>/`. There is no protocol tool, schema, or evidence-ref namespace.

**Section-number compatibility (read this before following a citation).** `AGENTS.md`, `orchestrator-role.md`, `engineering-role.md`, `program-stage-sequence.md` and `capstone_V6_7.md` were repointed to the new numbering on 2026-09-07. **Historical documents were not** — the amendment sheets, `cp-0-defects.md`, `docs/track-b/rule-inventory.md` and the Hebrew Gauntlet guide still cite this file's old ten-form numbering, correctly, as the numbering that was current when they were written. **All ten old sections** resolve as follows:

| Cited as | Now |
|---|---|
| `gauntlet-templates.md` §1 — Orchestrator checkpoint brief | **§1** (same role; the CP-2 blind block, executor preconditions and raw-second ceiling are gone) |
| `gauntlet-templates.md` §2 — active `workbench.md` | **retired**; the Lead keeps whatever working notes it likes and none are program state |
| `gauntlet-templates.md` §3 — Builder assignment | **retired**; delegation is an unmandated engineering choice (`engineering-role.md` § *Checkpoint execution* step 3) |
| `gauntlet-templates.md` §4 — independent (component) Critic assignment | **retired**; one fresh Integration Critic per checkpoint, assigned from **§2** |
| `gauntlet-templates.md` §5 — Critic verdict | **§2**, *Integration Critic assignment and verdict* |
| `gauntlet-templates.md` §6 — fresh Integration Critic | **§2**, *Integration Critic assignment and verdict* |
| `gauntlet-templates.md` §7 — Consolidated Return Packet | **§3**, *Checkpoint return* — the whole form, including its *Landing report* block |
| `gauntlet-templates.md` §8 — Orchestrator receipt and gate | **§4**, *Orchestrator receipt and disposition* |
| `gauntlet-templates.md` §9 — inspection, disposition, reclamation | **§4**, *Orchestrator receipt and disposition* |
| `gauntlet-templates.md` §10 — `BRIEF_INVALID` return | **retired**; a malformed brief is corrected in conversation |

**v6.7 reduced this file from ten forms to four.** Retired: the active `workbench.md` form, the Builder assignment form, the component-Critic assignment form, the separate component-verdict form, the mandatory-surface scope table, the Builder-seed and start/end topology tables, the provenance/read-scope block, and the `BRIEF_INVALID` return. A malformed brief is now corrected in conversation before repository work begins.

---

## 1. Orchestrator checkpoint brief

```text
# Track B Checkpoint Brief — [M#/CP-#]

## Target
- Repository: [name and local path]
- Authorized checkpoint: [exactly one]
- Ratified plan anchor: [exact filename and version]

## Orchestrator-reported expected state
- Branch / commit: [...]
- Working tree: [...]
- What already exists: [...]
- Verify this yourself before relying on it, and report any material mismatch.

## Observable outcome
[What must be demonstrably true when this checkpoint closes.]

## Complete authoritative checkpoint bar
[Citation to the complete named checklist in the plan's §12 — every item, not an extract.]

## Task-specific supporting extract
[Optional. A convenience quote. It cannot narrow, weaken or replace the complete checklist above.]

## Applicable constraints
[Budget, hardware, data sources, scope boundaries, reproducibility — from the named plan.]

## Timebox
[One approximate figure in hours, covering orientation through terminal return. Report elapsed
hours to the nearest half hour. Crossing it is a scope check, not an automatic stop.]

## Owner-only actions already authorized
[Credentials supplied, destructive operations pre-approved, or "none".]

## Stop and return
Return exactly one of PASS / BLOCKED / INCOMPLETE using §3. Do not begin, scaffold, or plan the
next checkpoint. Do not commit to main, publish, or push.
```

---

## 2. Integration Critic assignment and verdict

**Assignment** — the Lead gives the Critic exactly this and nothing else. No Builder checkout, no uncommitted diff, no reasoning, no summary, no conversation history.

```text
# Integration Critic — [checkpoint]

## Candidate
- Full SHA: [40 hex]
- Clean detached worktree: git worktree add --detach <path-outside-repo>/critic-[cp] <sha>
- Confirm `git status --porcelain` is empty before and after your review.

## Controlling plan
- File: [repository-relative .md path]   Version: [...]
- Bar citation: [section]
- Verbatim bar excerpt:
  > [paste the exact text; confirm it appears in that file at this SHA]

## What to verify
The complete named checklist, item by item: contract consistency, hard invariants, reported
metrics, reproduction, documentation. Recompute independently. Do not redesign.

## Reproduction
- Commands: [exact]
- Expected output or tolerance: [...]
```

**Verdict** — one markdown file, committed to `docs/track-b/evidence/<checkpoint>/integration.md` *after* the review is complete.

```text
# Verdict — [checkpoint] — Integration — [PASS | FAIL | BLOCKED]

- Candidate SHA: [40 hex]
- Plan / version / bar: [file, version, section]
- Verbatim bar excerpt: > [...]
  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: [yes]

## Commands actually run
[Each command, its exit code, and the observed output. Not a description of what you would run.]

## Evidence actually inspected
[Files, artifacts, figures, metrics — what you opened, not what exists.]

## Checklist verdict
| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
[Every item in the complete named checklist. No item may be omitted or merged.]

## On FAIL only
- Single largest meaningful gap: [one or two sentences]
- Exact next acceptance test: [what would have to pass]
```

`BLOCKED` means the check could not be performed at all (missing credential, unavailable source). It is never a substitute for `FAIL`, and a required review left `BLOCKED` cannot support a terminal `PASS`.

---

## 3. Checkpoint return

```text
# Track B Checkpoint Return — [M#/CP-#]

## Status
[PASS | BLOCKED | INCOMPLETE]  — one only.

## Identity
- Repository / checkpoint / ratified anchor and version: [...]
- final_candidate_sha: [40 hex]   (every bar binds here)
- evidence_tip_sha:    [40 hex]
- git diff --name-only <final_candidate_sha>..<evidence_tip_sha>:
  [paste output — must be empty outside docs/track-b/evidence/<checkpoint>/]

## Repository state
- Branch: gauntlet/[cp]   Working tree: [clean | listed exceptions]
- Branches, worktrees or tags this checkpoint created: [each one named, with purpose and state,
  or "none". An undeclared branch is a defect in this return.]
- main untouched, nothing staged on main, nothing pushed: [confirm]

## Complete checklist with direct evidence
| # | Checklist item | Status | Direct evidence (path, command, or metric) |
|---|---|---|---|
[The complete named checklist from the plan's §12 — never the brief's extract.]

## Integration verdict
- Path: docs/track-b/evidence/[cp]/integration.md   Result: [PASS]
- Candidate SHA it binds: [40 hex]

## Reproduction
[Commands a reader can run, and the results observed when they were run.]

## Files changed
[git diff --stat, plus one line of rationale per file.]

## Elapsed
[Approximate hours to the nearest half hour, against the brief's timebox.]

## Open risk or exact owner action
[The smallest exact decision, authority, credential or resource needed — or "none".]

## Landing report
- Proposed disposition: [LAND | DISCARD] with one line of reasoning
- Evidence tip to preserve: [40 hex]
- Live documents citing this branch (to repoint on reclamation): [list, or "none"]
- Proposed commit message: [one message, for the owner to use or discard]

## Post-return reads
[If you read progress.md or orchestrator material after the Integration verdict solely to author
this return accurately, say so in one line. Otherwise "none".]
```

---

## 4. Orchestrator receipt and disposition

**Receipt — the Orchestrator verifies rather than accepts.** Run, do not read about:

```text
git -C <repo> log --oneline -3 <evidence_tip_sha>
git -C <repo> diff --name-only <final_candidate_sha>..<evidence_tip_sha>
git -C <repo> status --porcelain=v1
git -C <repo> branch -vv
test -f docs/track-b/evidence/<cp>/integration.md && head -5 docs/track-b/evidence/<cp>/integration.md
```

Confirm: status is one of the three; the verdict file exists and reads `PASS` at `final_candidate_sha`; the two-SHA delta touches evidence paths only; every checklist item carries direct evidence; `main` is untouched and nothing was pushed. **Do not re-derive every record-level claim the return already evidences** — verify the SHAs, the verdict, the delta and the checklist coverage, and take the rest as reported.

**Disposition — the procedure is `AGENTS.md` § *Branch and ref lifecycle*; this is the command form.**

*Step 1 — INSPECT (agent, read-only).*

```text
git worktree list
git branch -vv
git tag --list 'land/*' 'evidence/*' 'archive/*'
git log --oneline --graph main..<evidence_tip_sha>
git diff --stat main...<evidence_tip_sha>
git diff --name-only <final_candidate_sha>..<evidence_tip_sha>   # evidence paths only
```

*Step 2 — DISPOSE (exactly one).*

**LAND — owner, by hand. Never delegated, never agent-executed.**

```text
git checkout main && git merge --squash gauntlet/<cp>
git status && git diff --cached      # review the staged tree; nothing is committed yet
git commit                           # authored by hand, after the owner's own review
git tag land/<cp> <the squash commit on main>
git tag evidence/<cp> <evidence_tip_sha>
```

**Both tags, always.** `land/<cp>` records where the work landed; `evidence/<cp>` preserves the reviewed candidate chain. A squash commit does not contain the candidate SHAs the verdict cites, so tagging only the landing point leaves that chain reachable from nothing once the branch is reclaimed. This is the rule `AGENTS.md` states and the defect `D-CP0-19` was filed for; **v6.7 corrected this block, which had named only one tag.**

**DISCARD — agent-executed.**

```text
git tag archive/<cp>-attempt-<k> <evidence_tip_sha>
```

*Step 3 — REPOINT (agent).* Update every live document that cites the branch about to be deleted, in the same operation. The citation follows the ref.

*Step 4 — RECLAIM (agent).* Only after the disposition is recorded and the tag verified to resolve:

```text
git tag --list 'evidence/<cp>' 'archive/<cp>-*'    # must resolve before deleting anything
git branch -D gauntlet/<cp>
git worktree remove <each worktree this checkpoint created>
git worktree prune
```

An agent may never delete a ref whose SHAs are not already reachable from a verified tag, and never a branch the owner has not dispositioned. Unknown branches are escalated to the owner with findings and a recommendation — never auto-deleted, and never grounds for refusing to run a checkpoint.
