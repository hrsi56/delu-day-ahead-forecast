# CP-26 Ledger Fix and Immediate Continuation

You are the Track B Engineering Lead. Fix the specific ledger defect, finish the existing pilot, and proceed directly to full training if the complete cumulative forecast passes the budget gate. No restart and no broad repair program.

## Target

- Repository: `/Users/djourno/Downloads/PJM`; Lead: `.local/worktrees/cp-26/lead`.
- Authorized checkpoint: CP-26, continuing run `cp26-cold-rerun-2026-10-15-01` on `gauntlet/cp-26`.
- Ratified plan anchor: `capstone_v21.md`, v21-r14, complete §24.7 and its supporting sections; SHA-256 `3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5`, anchor commit `332baeb861cec5a58516c58a29a1a3afe1eec909`.

Read AGENTS, engineering-role and the existing issued cold-run brief. This Owner addendum preserves their scientific and hardware rules. Do not read program-state or Orchestrator/Track A/C materials.

## Orchestrator-reported expected state

Verify before editing: Lead tip `c1685ee735072a03861838d5e6960aff9a04e10e`; primary main unchanged at `647d6eb81b2cf6e0cfaf4152f659d689ff973578`. The existing pilot has **946/1,064 probes**, with **118 missing**. Recorded new-run spending is **1.160572 h**, cumulative spending **66.322696 h**; use live totals. All jobs stopped. Preserve both runs, the two untracked historical exports and all existing receipts.

## Observable outcome

The ledger handles valid concurrent refreshes correctly; the same pilot reaches 1,064 terminal probes; a complete supported forecast is recorded. If its conservative cumulative total is **at most 388 machine-hours**, immediately execute the existing full baseline workload without another Owner approval. Otherwise return BLOCKED with the cost table. Passing is not guaranteed.

## Complete authoritative checkpoint bar

All of v21-r14 §24.7 and its inherited requirements remain controlling. Its complete verbatim text is already preserved in `docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/complete-bar.md`. This addendum reduces preparation overhead, not the CP-26 acceptance bar.

## Work

1. **Fix the actual defect.** Inspect `src/cp26/budget.py`, `_resource_update`. It currently aborts on `conflicts > 2` or deadline expiry with the same error. The sole-worker receipt recorded three conflicts in **0.452786 s**, before the **0.5 s** deadline. Correct premature retry exhaustion or equivalent refresh handling while retaining the absolute deadline, locking, once-only updates and ownership checks. Distinguish conflict exhaustion from elapsed timeout. Do not merely lengthen timeouts or retry indefinitely.
2. **Check only what changed.** Demonstrate that more than three valid refresh conflicts can resolve within the deadline, actual deadline expiry fails closed, and task/counter updates remain exactly once. Reuse applicable tests; run affected supervision checks only if necessary. No new framework, exhaustive crash matrix or separate repair Critic.
3. **Resume the same pilot.** Preserve all 946 valid probes and complete only the missing 118, with the registered inputs/configurations/seeds and real supervision. Register the operational patch with truthful provenance; retain existing probe identities and reuse scientifically compatible results. Do not relabel old evidence, reset counters, create another run, rerun successful probes or substitute a new scientific protocol.
4. **Forecast, admit, train.** Price all remaining required searches, fits, replay, controls, analyses, reporting, final review, operational costs and contingencies. Add current cumulative spending once, retaining historical charges and reserves. Do not omit costs or reduce safety allowances merely to pass. Record a new forecast/admission result while preserving the rejected record. On a supported cumulative total **≤388 h**, continue immediately through training, forecasting, evaluation and final review under the existing grant. If it exceeds 388 or material costs remain unsupported, stop with the precise blocker.

## Applicable constraints

Keep the separate new-run counter and historical baseline; neither resets again. The **485-hour actual cumulative ceiling**, **388-hour cumulative admission gate**, four-worker maximum, BLAS=1, CPU-only execution, aggregate **12,000,000,000-byte RSS** cap, and existing **0.5 s ledger / 2 s heartbeat** limits remain unchanged. Use the existing MacBook scheduling and caffeinate support for continuous execution. Genuine guard failures still stop work.

Keep frozen inputs, calendar/masks, numerical recipes and causal state rules unchanged. No retrieval, remote writes, publication, main changes, governance edits or CP-28 execution. Preserve credential protections and hooks.

## Timebox

The existing approximate **24 active hours** applies; unattended computation is accounted separately. No separate repair-phase allocation or intermediate handover is required.

## Owner-only actions already authorized

**By delivering this brief, I authorize** the necessary non-destructive local ledger fix, related tests and minimal entry-point/admission/provenance changes, pilot completion, and—after admission PASS—continuous full CP-26 execution and final review. Ordinary CP-26 source/tests/drivers and cold-run output/evidence paths are authorized, including serial local commits on the existing branch. No per-command, per-file or per-stage permission is needed. No Lockdown suspension or budget increase is granted.

Preserve this delivered addendum in the cold evidence directory and record its actual authority before new compute; retain previous issued documents unchanged.

## Stop and return

Prioritize real baseline execution. Do not start another cold run or expand this into an infrastructure project. Complete CP-26 under its existing final Integration and PASS/BLOCKED/INCOMPLETE return contract. No full-checkpoint PASS without the fresh final Integration verdict. If blocked, give the exact remaining defect or complete cost shortfall and preserve progress; do not silently retry indefinitely or weaken the gate. Keep both resource views, prior science and main intact.
