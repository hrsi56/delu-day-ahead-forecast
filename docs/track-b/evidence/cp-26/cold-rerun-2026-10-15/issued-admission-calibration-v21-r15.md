# Track B Checkpoint Brief — CP-26: Calibrate and Continue

You are the Track B Engineering Lead. Resume the existing cold run, fix its specific operational
timeout, finish the pilot, and start full baseline training immediately after supported budget
admission. Preserve completed work. No restart or broad repair program.

## Target

- Repository: `/Users/djourno/Downloads/PJM`; Lead: `.local/worktrees/cp-26/lead`.
- Authorized checkpoint: CP-26; run `cp26-cold-rerun-2026-10-15-01`; branch `gauntlet/cp-26`.
- Ratified plan anchor: `capstone_v21.md`, v21-r15, complete §24.7; Owner-approved admission
  amendment committed at `c9d5ab98d590ac9b1958e0ec9efe61a78ffcde7c`, SHA-256
  `490aea3bef90887af1fc3e0776c21eff53b2a155142c4dcf54c0977a27842521`.

Read AGENTS, engineering-role, that exact anchor and its cited supporting sections. Read the
existing cold-run `issued-brief.md` and `issued-ledger-fix-addendum.md` in this directory. This
Owner-approved addendum supersedes their 388-hour admission gate and fixed 0.5 s ledger /
2 s heartbeat restrictions only; their remaining scientific and execution requirements continue.
The original instruction to create a fresh namespace is already fulfilled: continue this run.
Do not read program state, Orchestrator/Track A/C materials or select a different plan.

## Orchestrator-reported expected state

Verify actual state before editing. The policy commit above follows evidence tip
`1e7eb029f1cbbec6483aea4a7dda0754fd7adf0b`; a later evidence-only handoff commit may contain
this brief. Primary `main` is clean at `647d6eb81b2cf6e0cfaf4152f659d689ff973578`.
CP-26 is INCOMPLETE, without Integration PASS. All prior owned jobs stopped.

The same sealed pilot has **1,013/1,064 probes**, 40/42 complete route/search pairs and **51
missing probes**. No cold-run full search or forecast replay has started. The removed retry-count
cutoff already passed 21 targeted checks; do not redo that repair. The next genuine ledger
transaction took **0.531298 s**, exceeding 0.5 s with two conflicts while refreshing 8.62 MB.

Snapshot: **1.319834 h new-run**, **66.481959 h cumulative**, including historical baseline
**65.16212464012295 h**. Read live totals from primary `.local/artifacts/cp-26/ledger/budget.json`;
preserve the two accounting views, 2,826-second historical reserve and closed old repair scope.
Keep the older 42 searches/575 forecasts unused and both untracked historical files under
`reports/rebaseline/continuation-v21-r14-accounting-3/` (`learning-ledger.json`, `replay-state.json`).

## Observable outcome

Complete this run's B0 and v1-R–v5 baseline over the full frozen CP-25 population: currently
2,068 eligible measurement days, 2,078 calendar days, 363 warm-up dates and 2,441 total origins.
The Owner's approximate 1,926 days is not a smaller sample instruction. Complete nominal
forecasts first while retaining all registered no-load/GFS+6 controls and final obligations.

Immediate milestone: calibrated reliable supervision, all 1,064 existing pilot probes, and a
complete conservative forecast. On cumulative forecast **≤436.5 machine-hours**, record
admission PASS and continue training, searches, chronological replay, analysis and final review
continuously without another Owner approval. The actual cumulative ceiling stays **485 h**.

## Complete authoritative checkpoint bar

Every item of v21-r15 `capstone_v21.md` §24.7, its cited supporting requirements and unchanged
CP-25 scientific rulings governs completion. Only their former admission rule is superseded by
`docs/track-b/capstone_v21-r14-to-v21-r15-amendments.md`, SHA-256
`9e7e87361a7030c14158bb880370acaef52940cd2c76f699a59f47d19c03dc41`.
The earlier `complete-bar.md` remains historical r14 evidence. Extract a new versioned r15 bar
with `scripts/bar.py` when needed; do not overwrite the old bar. No checklist reduction or new
repair-phase Integration review is required. One fresh final Integration review remains mandatory.

## Work

1. **Align authority and enforcement before compute.** Record this actual Owner grant and
   update the operational admission fraction/threshold to 0.90/436.5, including assertions,
   cost-spec checks, gate messages and harness authority/anchor pins. Relevant existing code
   includes `src/cp26/budget.py`, `costing.py`, `gates.py` and `harness.py`. Keep 485 enforcement.
   Preserve old authority, rejected forecasts and the 1,013 original probe receipts unchanged;
   record truthful operational lineage and reuse scientifically compatible probes. No broad
   identity migration, relabelling of evidence or new accounting framework.
2. **Calibrate the actual deadline problem narrowly.** Measure representative ledger refresh
   and observer latency on this Mac under the intended bounded concurrency. Choose finite,
   documented ledger/heartbeat limits from observed tails, permitting at most **5 s ledger**
   and **15 s heartbeat**, not automatic defaults; retain 0.2 s polling. Startup and watchdog
   ordering must be coherent. Ledger waits must not block independent ownership, worker-time,
   RSS or hard-budget enforcement. Keep locking and exactly-once writes. Demonstrate, using
   small affected checks, that real refreshes complete, duplicates do not double-charge, and a
   stopped observer/deadline violation still stops owned workers within the documented bound.
   Reuse applicable passed checks. No exhaustive failure matrix, broad suite or separate Critic.
3. **Resume only the missing 51 probes.** Use the same configurations, inputs and seeds; no
   new run, counter reset, successful-probe rerun or replacement model seeds. Retain valid
   existing timing evidence and namespace/state. Charge calibration, tests, failed attempts and
   shutdown tails to this run and cumulative accounting once. A genuine unresolved guard
   failure still stops compute; do not repeat failures indefinitely.
4. **Forecast completely, then train immediately.** Price all 42 fresh searches, all required
   origins/routes and controls, fits, replay/persistence, analyses/diagnostics, reporting, draft
   packet, final review/closure and justified failure allowance. Include bounded operational
   overhead and longer detection/shutdown exposure. Add remaining work to updated cumulative
   charges once. Preserve existing cost margins unless real evidence supports a change; never
   cut factors merely to pass. The prior **396.461874 h subtotal is incomplete**, not admission.
   Record the complete component table, cumulative/new-run completion estimates and wall-time
   forecast at chosen concurrency. Admit only with all required pilot coverage and supported
   material costs at **≤436.5 h**; otherwise stop with the exact shortfall or unsupported item.

## Applicable constraints

436.5 h is a **cumulative completion projection gate**, not a new-run allocation. At the quoted
snapshot it leaves 370.018041 h of future projected work. The 48.5 h gap to 485 is headroom,
not extra permission. Stop admitting work early enough to cover allocated workers multiplied
by worst-case detection, ledger/poll jitter, termination grace and closing-accounting time before
485. Reserve/charge that exposure without duplicating historical reserves. Unknown worker
duration or uncertain termination blocks further compute.

Use the locked primary `.venv` and existing supervised drivers/caffeinate. On the M3 16 GiB
MacBook, use up to four registered workers, BLAS=1, CPU only, aggregate RSS ≤12,000,000,000
bytes; a computing or reserved coordinator consumes its slot. Choose useful sustained throughput
within memory pressure, starting with fewer workers when needed; four is a maximum, not an
assumption. Keep healthy work running continuously at any hour. Retain chronological causal
state and all numerical recipes; no new scheduler or OS power/priority changes.

Preserve frozen inputs, masks, issue time, seeds and development boundary. All data access uses
`cp25.guard`; no post-2026-09-06 data. No retrieval, remote writes, external spend, publication,
main edits, CP-28 execution, governance edits, dependency changes or landed member-code changes.
Preserve credentials and hooks. Keep new temporary work and any isolated worktrees inside primary
`.local/`. Reuse existing evidence; do not generate another gigabyte handoff diff.

## Timebox

Approximately **24 active hours**, continuing the existing task; unattended compute is accounted
separately in machine-hours. No new repair-phase timebox or intermediate handover is required.

## Owner-only actions already authorized

The Owner's **“מאשר” on 2026-10-16** authorizes this narrow operational calibration, necessary
ordinary CP-26 source/test/driver/gate/provenance updates, completion of the existing pilot and,
after supported admission, uninterrupted full CP-26 execution and final review. Ordinary cold-run
output/evidence paths, operational ledger writes and serial local commits on `gauntlet/cp-26`
are authorized; the Lead remains sole Git writer. No per-command, per-file or per-stage approval
is needed. This brief is the handoff of that approval, not a claim of new consent or admission.

The specific Lockdown suspension was used solely to record r15 and its amendment and ends at
the issuing task's return. **It does not transfer to you.** Read the recorded policy; do not edit
anchors, amendments, governance/agent files or program state. Preserve this issued brief and
prior records in place; record your starting tip and live balances before new compute.

## Stop and return

Prioritize the baseline. If admission passes, continue automatically under this grant. Return
PASS / BLOCKED / INCOMPLETE under engineering-role and templates §3 with the complete checklist,
both resource views and preserved history. No checkpoint PASS without the final fresh binding
Integration PASS and distinct candidate/evidence SHAs. On a real blocker, stop owned jobs,
preserve progress and state the smallest exact issue. Leave main and remote state untouched.
