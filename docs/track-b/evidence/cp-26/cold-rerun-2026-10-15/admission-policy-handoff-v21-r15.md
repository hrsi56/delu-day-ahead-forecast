# CP-26 r15 policy and continuation handoff — 2026-10-16

This scoped policy/handoff task is complete. **CP-26 remains INCOMPLETE**, without Integration
PASS or a new admission PASS. No pilot, training or checkpoint test job was launched here;
runtime calibration, remaining probes and gate enforcement updates belong to the next executor.

- Starting tip: `1e7eb029f1cbbec6483aea4a7dda0754fd7adf0b` on existing `gauntlet/cp-26`.
- Owner approval: **“מאשר”**, 2026-10-16, responding to the stated narrow Lockdown suspension,
  436.5-hour gate amendment and operational calibration/continuation proposal.
- Policy commit: `c9d5ab98d590ac9b1958e0ec9efe61a78ffcde7c`.
- Anchor SHA-256: `490aea3bef90887af1fc3e0776c21eff53b2a155142c4dcf54c0977a27842521`.
- Amendment SHA-256: `9e7e87361a7030c14158bb880370acaef52940cd2c76f699a59f47d19c03dc41`.
- English brief: `issued-admission-calibration-v21-r15.md`, SHA-256
  `743721cd6746fefbfe4e2315d3b9c37f5e30e967faa7913b62d609b523b8e444`.

The Owner-approved cumulative admission gate is now **436.5 h**. The actual cumulative hard
ceiling remains **485 h**. Completed probes and historical charges do not reset. The snapshot
of 1,013/1,064 probes, 1.319834 new-run hours and 66.481959 cumulative hours is historical;
the executor must use live values. The prior 396.461874 h subtotal remains incomplete.

## Validation actually performed

- Exact byte comparison against the starting anchor: after removing the new preface/restoring
  its historical heading, the only body changes are the three authorized §24.7 substitutions
  (80→90, 388→436.5 twice). Scientific text and 485-hour enforcement policy are unchanged.
- SHA-256 checks on the committed new anchor and amendment; original cold-run issued brief
  remains byte-identical. Prior candidate `80f12d09690aa34813c9b715b5cf5edc3a351037` remains
  reachable on the existing checkpoint branch.
- Main's `scripts/bar.py brief` checked the English brief's required fields and §24.7 citation:
  exit 0. This checks form, not checkpoint completion. `git diff --check`: exit 0.
- Two bounded read-only advisory checks found no material authority/accounting inconsistency.
  These are not Integration verdicts. No additional repair review is required by this handoff.
- Runtime code still uses the old pins/limits. The brief explicitly authorizes the next executor
  to update ordinary enforcement/provenance code before compute; no runtime repair is claimed.

## Files and retained state

| Changed path | Reason |
|---|---|
| `capstone_v21.md` | Record approved 90%/436.5 cumulative admission policy and historical precedence. |
| `docs/track-b/capstone_v21-r14-to-v21-r15-amendments.md` | Record precise Owner authority, scope, budget semantics and preservation requirements. |
| `issued-admission-calibration-v21-r15.md` in this directory | Give the independent executor the authorized finite calibration and same-run continuation task. |
| This handoff record | Preserve actual validation, limitations and authority expiry. |

No branch, worktree or tag was created. The Lead and branch are retained for continued CP-26
execution and Owner review. Both untracked historical exports remain untouched; no clean-up,
history operation, main change or remote write occurred. Main stays at
`647d6eb81b2cf6e0cfaf4152f659d689ff973578`. The two local commits are proposed for retention;
only the Owner may decide LAND or DISCARD.

Small local validation files and the complete four-path task diff are retained under primary
`.local/artifacts/cp-26/admission-v21-r15/` for review. They contain no model output and are
recovery material; required authority and handoff decisions are committed here.

Interview trigger for Orchestrator capture: operational deadline calibration and a forecast
admission margin are separate from the unchanged scientific protocol and actual resource cap.
No interview document or program-state document was read or edited.

**The task-scoped Lockdown suspension ends at this handoff's terminal return.** It does not
transfer to the executor, whose ordinary source/evidence/compute authority remains as issued.
