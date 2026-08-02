# Project role router

This repository is shared by program orchestration and Track B engineering, but those execution contexts are isolated. Establish the role before mutating anything.

- **ORCHESTRATOR session:** when the session is explicitly the Orchestrator or the task concerns cross-track planning/state, read `orchestrator-role.md` and the anchors it directs you to. Do not act as the Engineering Lead.
- **ENGINEERING-LEAD session:** when the session receives an Orchestrator-issued Track B brief, read `engineering-role.md` and only the exact ratified capstone plan named in that brief. Do not read program Track A/C materials, the syllabus, `progress.md`, or `orchestrator-role.md` during execution.
- **BOUNDED SUBAGENT:** when spawned by the Engineering Lead, follow only the bounded task, named plan sections, constraints, owned paths, and artifact paths. Do not assume Lead or Orchestrator authority; do not update `progress.md`, open/close a checkpoint, or inspect later work.
- **ROLE-MAINTENANCE exception:** a task explicitly authorized to compare or edit these contracts may read both role documents and the root router.
- **AMBIGUOUS role:** read-only inspection is allowed, but ask for the missing role/brief before changing project files. A bare request to “execute the capstone” does not authorize the full arc.

`progress.md` is controlled only by the Orchestrator. An active `workbench.md` is controlled only by the Engineering Lead, exists only inside one authorized checkpoint, and is never program state.

`AGENTS.md` is the single canonical root-role router. `CLAUDE.md` must contain only a pointer to this file; do not duplicate policy there.
