# CP-26 issued repair brief — v21-r14 candidate, 2026-10-13

**Issuer and authority:** the Owner's imperative repair request in chat on 2026-10-13. This
document records that request, not a new Orchestrator authorization. The Owner temporarily
suspended Governance Lockdown for `capstone_v21.md` and
`docs/track-b/capstone_v21-r13-to-v21-r14-amendments.md` solely for this repair, ending at final
return. r14 is a candidate, pending review and ratification before any experiment resumes.

**Repository/checkpoint:** `/Users/djourno/Downloads/PJM`; existing CP-26 only. Lead workspace
`.local/worktrees/cp-26/lead`, local branch `gauntlet/cp-26`, initial HEAD
`5cc3cc083c4340fd8d792eeaf6551a007987a877`. Verified initial primary checkout clean on main
`647d6eb81b2cf6e0cfaf4152f659d689ff973578`, unchanged landed-code comparison base.
Inherited changes: `scripts/cp26_rebaseline.py`, `reports/rebaseline/parity.json`,
`tests/test_cp26_monitor.py`, preserved with hashes before incorporation.

**Candidate anchor:** `capstone_v21.md` v21-r14, SHA-256
`3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5`, anchor-only commit
`332baeb861cec5a58516c58a29a1a3afe1eec909`. The original r13 brief
`issued-brief.md` is historical and unchanged, SHA-256
`5e16a134a9dd798733b0393f4f8e2570d03bf251471503d9292966e67e05214b`.
Its full CP-26 checklist remains open; this brief does not complete or narrow that checkpoint.

**Repair contract:** §§24.7–24.9 of this candidate and the Owner's six numbered contracts:
Jan15+182k support-only eligible blocks, exact landed mask/week rule and extrema ≥250/14;
sampler128/fixed space/halving/ranking/ties and separately frozen trial/member seeds; four
effective configs×two seeds, strict8, no stale/CP24 serving; native central/H/scored-source/full
error eligibility separated; own-error warm-up/recovery after D−2 while emitted fallback stays
scored; no intake on central/identity/solver/scale/numerical-H failure; B0 raw/no self fallback,
v1-R nine-head CQR; canonical complete days separate from frozen partial scoring keys and
three-member364/728 learning ledger; route/policy isolation and persistent once-only state;
versioned CP-28 protocol with seven arms/gates/Holm/shared fits/start weights unchanged.

**Allowlist:** `capstone_v21.md`, the new amendment sheet; `src/cp26/**`,
`scripts/cp26_*.py`, `tests/test_cp26_*.py`; this brief,
`cp28-frozen-protocol-v21-r14.md`, `docs/track-b/evidence/cp-26/repair-v21-r14/**`,
`reports/rebaseline/repair-v21-r14/**`. Active CP-26 outputs may change only after preserving
their prior identity. No change to original brief/protocol, programme state, governance files,
landed code, data, CP-25 outputs, hooks, dependencies or resource ceilings.

**Execution:** Lead is sole Git writer, local commits only on `gauntlet/cp-26`, hooks active,
`git commit -F <project-local-message-file>`. Disposable isolated Builder/review worktrees created
for this task stay inside `.local/worktrees/cp-26/`; imports are limited to owned allowed files.
Existing worktrees/refs are retained. No main writes, LAND, publication, push or history changes.

**Resources/accounting:** at most10 new machine-hours inside cumulative485; at most4 workers,
BLAS1, CPU only, aggregate RSS12GB, zero downloads/remote writes. Preserve547.5647564170067s
including6.125s already recorded. Add audit90.127s once as reported. The failed audit's15.01s
is only a lower bound; authorized2826s reserve requires enclosing-window evidence, remains a
reserve, and is never reduced without evidence. Include measured/reported/reserves in all caps
and projections. Death, PID reuse, resume and orphan handling must fail closed without terminal
worker evidence; no idle-gap charge as measured. Approximate active-work timebox12h.

**Acceptance:** monitored synthetic/support tests cover all14 dates×three routes, effective
distinctness/eight members, D−2 warmth/recovery, central failure refusal, B0/CQR differences,
partial scoring/full DST days, once-only release/historical scale/causality, restart equivalence,
search-boundary continuity, learning/H separation, route isolation, unchanged emitted fallback,
and death/hard kill/PID reuse/orphan/unreconciled reserve accounting. Old-settings parity fits
alone are permitted for current gate evidence, never serving CP-26.

**Stop/return:** stop before real searches, timing pilot, experimental-calendar replay or CP-26
scores; no CP-28 implementation/execution. Return REPAIR_READY only with repair evidence, or
precise blockers/gaps; CP-26 remains INCOMPLETE. Future pilot must price42 searches and total
expense including history/reserves against388h. Return candidate/final SHAs, document identities,
checklist/commands/results, full diff/status/file reasons, resources, worktree/ref accounting,
remaining experiment work and interview/exposure triggers. Do not claim Integration PASS or
edit `integration.md`. Leave branch/Lead worktree for Owner review; no automatic resumption.
