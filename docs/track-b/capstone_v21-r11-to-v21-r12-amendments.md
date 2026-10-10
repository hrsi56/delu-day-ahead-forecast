# v21-r11 → v21-r12 and PUBLISH_RULES 1.3 → 1.4 — work availability

Owner-authorized on 2026-10-10, in a dedicated editing session.

## Authority and scope

The Owner requested permanent removal of all work-calendar prohibitions from rules and
contracts so agents work at any time without checking a restricted day, time or approaching
window. The Owner explicitly authorized every necessary document edit, commit and push,
including work on main, for this objective only. This is the task-scoped Lockdown suspension
and Git/publication exception for this maintenance change; it grants no later task new authority.

## Result

- `AGENTS.md` § Work availability states the effective rule for all agents and all future work.
  Earlier calendar restrictions, including those in pinned briefs, no longer govern execution.
- Research §§16, 17.8, 17.10, 20.8, 21.8 and 23.11 lose their calendar restrictions and associated
  pause/resumption conditions. Research methods, acceptance bars and resource caps are unchanged.
- Publication §7.2, incorporated plans, runbook, packet template and historical policy copies
  no longer impose special-day coverage or manual-work restrictions. Daily coverage remains.
- CP-21/22/23 monitors no longer consult a work calendar at admission or during execution.
  Resource accounting, timeboxes, concurrency, signals, atomic writes and hard caps remain.
  The old CP-22 wrapper is a compatibility entry point with no expiry or exception logging.
- `--expected-minutes` remains accepted for old reproduction commands; it imposes no scheduling
  condition. Elapsed-time accounting and timestamps still serve resource/evidence requirements.

## Evidence and existing work

Prior repository state is preserved at `522d7ea722b5d215d827d7aed9c56b7a9dec066e`.
Historical release evidence, issued briefs, landing records, report payloads and quoted
verdicts are not rewritten. Their calendar observations describe the rules then in effect,
not current work restrictions. Old hashes continue to bind those prior Git bytes; new anchor
hashes are recorded in `progress.md`. Historical policy copies changed here carry this distinction.

No existing CP-24 worktree, candidate SHA, resource ledger or checkpoint state is changed.
Existing sessions must apply the Owner decision and current Work availability rule when they
continue; this amendment authorizes no research execution or evidence regrading.
The existing CP-24 Lead and detached Critic checkouts remain at `d637590` and contain their
original calendar-gated CP-24 driver. They are frozen candidate snapshots, not updated copies
of main. Before that driver is reused or landed, its calendar gates must be removed and reviewed
under the current rule. The shared runtime regression suite automatically includes CP-24 when
`scripts/cp24_ddnn2.py` is present, so landing its old gate cannot pass the new work-availability
checks. No old worktree is silently modified or represented as updated by this maintenance task.

## Validation

`tests/test_work_availability.py` exercises all three real monitors with synthetic ledgers:
admission during previously restricted times, continuation across the former boundary and
20:00, ordinary-day controls, admission refusal and live termination at resource caps, and the legacy command’s non-expiring entry
point. Temporary ledgers and logs stay under `.local/tmp/calendar-removal/`.

Run the tests with:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/test_work_availability.py tests/cp21/test_guards.py tests/cp21/test_saved_evidence.py tests/cp22/test_saved_evidence.py tests/cp23/test_saved_evidence.py --basetemp=.local/tmp/calendar-removal/pytest
```

**Local result:** 62 tests passed. `git diff --check`, Python syntax checks, current anchor
hash checks and `scripts/publication_guard.py tree` passed. Both historical evidence tags
were available and their checks passed (no skipped historical-source checks).

## Files changed

- `AGENTS.md` — update work-availability policy, references or verification.
- `capstone_v21.md` — update work-availability policy, references or verification.
- `docs/PUBLISH_RULES.md` — update work-availability policy, references or verification.
- `docs/track-b/capstone_v21-r4-to-v21-r5-amendments.md` — update work-availability policy, references or verification.
- `docs/track-b/capstone_v21-r5-to-v21-r6-amendments.md` — update work-availability policy, references or verification.
- `docs/track-b/cp-24-research-directions-2026-10-05.md` — update work-availability policy, references or verification.
- `docs/track-b/final-product-space-plan-2026-09-30.md` — update work-availability policy, references or verification.
- `docs/track-b/presentation-and-tracking-plan-2026-09-24.md` — update work-availability policy, references or verification.
- `docs/track-b/progress-context-recovery-2026-09-15.md` — update work-availability policy, references or verification.
- `docs/track-b/publication-packet-template.md` — update work-availability policy, references or verification.
- `docs/track-b/publication-runbook.md` — update work-availability policy, references or verification.
- `docs/track-b/publication-standard-v1.md` — update work-availability policy, references or verification.
- `docs/track-b/publish-rules-migration-plan-2026-09-29.md` — update work-availability policy, references or verification.
- `docs/track-b/v2-decision-brief-packet.md` — update work-availability policy, references or verification.
- `docs/track-b/v3-plan-handoff-2026-09-22.md` — update work-availability policy, references or verification.
- `progress.md` — update work-availability policy, references or verification.
- `scripts/cp21_blocks.py` — remove runtime calendar enforcement or its obsolete protocol text.
- `scripts/cp22_owner_calendar_exception.py` — remove runtime calendar enforcement or its obsolete protocol text.
- `scripts/cp22_revision.py` — remove runtime calendar enforcement or its obsolete protocol text.
- `scripts/cp23_ddnn.py` — remove runtime calendar enforcement or its obsolete protocol text.
- `src/cp21/budget.py` — remove runtime calendar enforcement or its obsolete protocol text.
- `src/cp21/protocol.py` — remove runtime calendar enforcement or its obsolete protocol text.
- `src/cp22/budget.py` — remove runtime calendar enforcement or its obsolete protocol text.
- `src/cp22/protocol.py` — remove runtime calendar enforcement or its obsolete protocol text.
- `src/cp23/budget.py` — remove runtime calendar enforcement or its obsolete protocol text.
- `src/cp23/protocol.py` — remove runtime calendar enforcement or its obsolete protocol text.
- `tests/cp21/test_guards.py` — update work-availability policy, references or verification.
- `tests/test_work_availability.py` — exercise unrestricted scheduling and retained resource limits.
- This amendment record — preserve authority, scope and historical identity.
- `tests/cp21/test_saved_evidence.py` — verify amended historical sources against `evidence/cp-21` while retaining current-file checks for all other artifacts.
- `tests/cp23/test_saved_evidence.py` — verify amended historical sources against `evidence/cp-23` while retaining current-file checks for all other artifacts.

Historical source checks skip only when their evidence tag is unavailable in a shallow checkout,
as the existing CP-21 publication-amendment test already does. This session verifies both tags
locally; the original manifests are unchanged. Current runtime checks run without those tags.
