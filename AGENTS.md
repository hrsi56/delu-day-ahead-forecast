# Project role router

This repository is shared by program orchestration and Track B engineering, but those execution contexts are isolated. Establish the role before mutating anything.

- **ORCHESTRATOR session:** when the session is explicitly the Orchestrator or the task concerns cross-track planning/state, read `orchestrator-role.md` and the anchors it directs you to. Do not act as the Engineering Lead.
- **ENGINEERING-LEAD session:** when the session receives an Orchestrator-issued Track B brief, read `engineering-role.md` and only the exact ratified capstone plan named in that brief. Do not read program Track A/C materials, the syllabus, `progress.md`, or `orchestrator-role.md` during execution.
- **BOUNDED SUBAGENT:** when spawned by the Engineering Lead, follow only the bounded task, named plan sections, constraints, owned paths, and artifact paths. Do not assume Lead or Orchestrator authority; do not update `progress.md`, open/close a checkpoint, or inspect later work.
- **ROLE-MAINTENANCE exception:** a task explicitly authorized to compare or edit these contracts may read both role documents and the root router.
- **AMBIGUOUS role:** read-only inspection is allowed, but ask for the missing role/brief before changing project files. A bare request to “execute the capstone” does not authorize the full arc.

`progress.md` is controlled only by the Orchestrator. An active `workbench.md` is controlled only by the Engineering Lead, exists only inside one authorized checkpoint, and is never program state.

`AGENTS.md` is the single canonical root-role router. `CLAUDE.md` must contain only a pointer to this file; do not duplicate policy there.

## Git and publication authority

All agent work is local. Publication and mainline history belong to Yarden alone, in every role and every session. No brief, checkpoint authorization, PASS verdict, or convenience argument grants either.

- **Never publish.** No `git push` under any refspec or flag, no pushed tags, no remote branch creation or deletion, no PR, release, or issue, no `gh` command or other call that mutates `origin` or GitHub state. `origin` is a public portfolio repository linked from the CV and LinkedIn; treat every push as an irreversible public act that only its owner may take.
- **Never commit to `main`.** `main` is written by Yarden, by hand, after his own review. Agents leave their work in the working tree and do not stage, commit, amend, rebase, reset, revert, cherry-pick, drop a stash, or check out over uncommitted work on that branch.
- **Finish, then hand over.** An agent that reaches a point where a commit would normally follow does not stop mid-task to ask. It completes every task inside its authorization, brings the tree to one coherent reviewable state, and only then presents: `git status --porcelain=v1`, `git diff --stat`, the full diff, the list of files touched with a one-line reason each, and a proposed commit message. It then stops and waits. A commit that Yarden defers or refuses is never a reason to redo, revert, or abandon completed work.
- **Sole commit exception — Track B candidates.** Inside one authorized checkpoint, the **Engineering Lead is the sole Git writer**. It may create/switch to the local disposable branch `gauntlet/<checkpoint>` and may serially stage and commit candidate work there because the mandatory isolated Critic protocol in `engineering-role.md` requires a full candidate SHA. Builders never stage, commit, merge, switch branches, or update refs; parallel Builders work only in Lead-created isolated writable worktrees/snapshots, on disjoint allowlisted paths, and the Lead imports and commits those paths serially. Candidate commits stay local, never touch `main`, and are never pushed. Whether any candidate reaches `main` is Yarden's decision alone.
- **Local evidence preservation is part of that exception.** Critic verdicts are markdown files committed under `docs/track-b/evidence/<checkpoint>/` on that same local branch, after their review is complete. The candidate SHA cited by a verdict must stay reachable on the `gauntlet/<checkpoint>` branch until Yarden decides what reaches `main`. Nothing is pushed.
- **Bounded worktree lifecycle.** During the active checkpoint, the Lead may create and remove only the isolated Builder worktrees/snapshots it created for that checkpoint and the clean detached Critic snapshots required by `engineering-role.md`, after importing allowed Builder paths or completing the Critic integrity record as applicable. Builders may not manage worktrees. Removing any other worktree remains owner-only.
- **Destructive local operations are owner-only too.** History rewriting, `git clean`, hard resets, branch deletion outside a spent `gauntlet/*`, and worktree removal outside the bounded lifecycle above require an explicit instruction naming the operation.
