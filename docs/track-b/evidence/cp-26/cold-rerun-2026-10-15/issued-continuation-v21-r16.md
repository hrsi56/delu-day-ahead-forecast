# Track B Checkpoint Brief — CP-26: Resume the Existing Run

You are the Track B Engineering Lead. Apply the approved resource policy and continue the
existing baseline run. Do not restart, repeat the completed pilot or open another repair program.

## Target

- Repository: `/Users/djourno/Downloads/PJM`; Lead: `.local/worktrees/cp-26/lead`.
- Authorized checkpoint: CP-26; run `cp26-cold-rerun-2026-10-15-01`; branch `gauntlet/cp-26`.
- Ratified plan anchor: `capstone_v21.md`, v21-r16, complete §24.7 and cited supporting sections;
  commit `4766a61cb0c836573406f5a9729997d1b6ee9862`, SHA-256
  `27bdc6046117a543d4bfcaa439651e7bf2a8fa4d0c58af9631b606a358c10fd1`.

Read AGENTS, engineering-role, that anchor, its r15→r16 amendment and existing issued cold-run
briefs. r16 supersedes conflicting resource limits only. Retain role isolation.

## Orchestrator-reported expected state

Verify actual state. Previous evidence tip: `607e7985e58e07ce9398daedd9d6d7592a6f15e4`;
the policy commit above and an evidence-only brief commit follow it. Primary main remains clean
at `647d6eb81b2cf6e0cfaf4152f659d689ff973578`. CP-26 is INCOMPLETE; all jobs stopped.

Pilot: **1,064/1,064 probes**, all 42 pairs; 49 affected checks passed. Calibrated limits:
3 s ledger / 8 s heartbeat / 14 s startup / 0.2 s polling. Preserve these and all original probes.
Snapshot: **1.519930 h new-run**, **66.682055 h cumulative**, including historical baseline
65.16212464012295 h and retained reserves. Use live values. Prior return: `return-v21-r15.md`.

## Observable outcome

Complete this run's B0 and v1-R–v5 baseline over all frozen CP-25 keys: 2,068 eligible measurement
days and 2,441 total origins including warm-up. Prioritize nominal forecasts; retain all 42 searches,
registered controls, evaluation and final review.

## Complete authoritative checkpoint bar

Every item of v21-r16 `capstone_v21.md` §24.7 and its inherited requirements applies unchanged
scientifically. Preserve old bar extracts; use r16 for final review. Full Integration PASS is required.

## Continue

1. **Align enforcement before compute.** Update budget/gate assertions, displays, harness pins
   and operational authority to **440 h cumulative admission for this run** and **500 h actual
   cumulative ceiling**. No 450 h gate; the general line remains 436.5 h. With jobs stopped, back
   up the live ledger under primary `.local/` and make a locked, atomic, auditable cap transition
   from 485 to 500. Preserve all counters, charges, receipts and reserves; never reinitialize the
   ledger. Keep historical snapshots unchanged. Run only affected boundary checks.
2. **Carry forward the complete forecast.** Reuse the completed pilot and signed
   `reports/rebaseline/cold-rerun-2026-10-15/cost-projection.json`, retaining its bytes. Write
   versioned r16 projection/admission records using unchanged estimates, current authority/code,
   live charges and remaining transition/startup/closure costs, counted once. Last forecast:
   **439.801429 h**, not admission PASS. No repeated measurements/fits for policy-pin changes,
   omitted material costs or margin cuts merely to pass.
3. **Start and continue immediately on PASS.** At supported cumulative completion **≤440 h**,
   launch the full workload and continue through forecasts, analysis and final review without
   another approval. Preserve this run's identity, caches, plans, seeds and chronological state.
   No new namespace, counter reset, successful-probe rerun or old-run state import. Keep exports in
   `reports/rebaseline/continuation-v21-r14-accounting-3/` untouched.

## Applicable constraints

All prior charges remain within **500 h cumulative**. Keep both counters, the 2,826-second reserve
and closed repair scope. Preserve shutdown headroom and independent time/RSS/ownership guards.

Use the existing `.venv`, supervision and caffeinate continuously on the M3: ≤4 slots including
coordinators, BLAS=1, CPU only, aggregate RSS ≤12,000,000,000 bytes. Adapt to memory pressure.
Frozen inputs/recipes remain unchanged; `cp25.guard` and the 2026-09-06 boundary still apply.
Keep credential guards. No new scheduler, retrieval, remote write, publication, main/governance
edit, dependency/member-code change or CP-28 execution.

## Timebox

Continue the existing approximate **24 active hours**; unattended compute remains separately
accounted in machine-hours. No new repair phase or intermediate handover is required.

## Owner-only actions already authorized

The Owner's 2026-10-16 approval authorizes the **440 h exception**, **500 h ceiling**, necessary
non-destructive local enforcement/cap-transition/provenance/test updates and continuous CP-26
execution after admission. Ordinary CP-26 source/driver/test, cold-run outputs/evidence and ledger
writes are authorized, including serial local commits on `gauntlet/cp-26`; Lead is sole Git writer.
No per-command/file/stage approval is needed. Record the grant and live balances before compute.
The issuing task's Lockdown suspension expires at handoff and does not transfer; no governance edits.

## Stop and return

If the complete live forecast exceeds 440 h, material costs become unsupported or a genuine guard
fails, stop safely and return the exact blocker. Otherwise continue. Return PASS / BLOCKED /
INCOMPLETE under engineering-role/templates §3 with the full checklist, both resource views and
distinct candidate/evidence SHAs. No checkpoint PASS without fresh final Integration PASS.
