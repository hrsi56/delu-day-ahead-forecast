# CP-0 operational defects — the Gauntlet contract's own findings

**Status: OPEN.** Opened 2026-08-05, before CP-0 produced a candidate. Append findings as they
surface; do not close until CP-0 returns a terminal packet and the amendment in
`progress.md`'s Blockers section is ratified.

**Purpose.** `progress.md:27` designates CP-0 as the operational validation of
`engineering-role.md`, and the Notes for Future Sessions direct that its Return Packet be read for
*protocol defects as well as for its checkpoint verdict*. This file is that reading, kept as a
working artifact rather than folded into the session log, because the defects are structural and
will outlive the run that found them.

**Scope.** These are defects in the **contract and architecture**, not in any capstone bar. Nothing
here weakens or questions a scientific criterion, a checklist item, an invariant, or an acceptance
test. Every defect below is owned by `engineering-role.md`, `AGENTS.md`, the templates, or
`orchestrator-role.md`.

**How to append.** New findings get the next `D-CP0-n` ID, the same five-field shape (statement,
evidence, impact, ownership, candidate remedies), and a dated provenance line. Never renumber an
existing ID; a superseded defect is marked superseded and kept.

---

## Provenance of the current entries

| Date | Source | IDs |
|---|---|---|
| 2026-08-05 | Brief-validation failure on the first CP-0 handoff attempt — the brief was returned invalid before any repository edit | D-CP0-1 … D-CP0-4 |
| 2026-08-05 | Executor stall on a low-reasoning-effort run, before any candidate existed | D-CP0-5 |

All five were found **before a single line of CP-0 product code was written.** That is itself the
first result: the contract's own front gate produced findings on its first real contact with an
execution attempt.

---

## D-CP0-1 — Role is asserted, never verified

**Statement.** `AGENTS.md` routes every session to a role and forbids an Engineering-Lead session
from reading `orchestrator-role.md`, `progress.md`, the syllabus, or Track A/C material during
execution. Nothing detects or prevents a session that has *already* read them from then declaring
itself the Lead. The role boundary is a declaration, not a verified property.

**Evidence.** On 2026-08-05 a session that had read `orchestrator-role.md`, `progress.md`,
`docs/track-b/rule-inventory.md`, the Hebrew guide, and `capstone_V6_5.md` §11–§12 in full — for
unrelated article work — was handed a CP-0 execution instruction. It could have proceeded. The only
thing that stopped it was the session choosing to disclose its own contamination.

**Impact.** The contamination the router exists to prevent is exactly the contamination that lets an
executor choose its own scope: a Lead that has read `progress.md` knows what the next milestone is,
which checkpoint follows, and what the program considers behind schedule. `engineering-role.md:9`
and `:97` both assume that knowledge is absent. A contaminated Lead can satisfy every written rule
while making decisions the architecture assumes it cannot make.

**Ownership.** `AGENTS.md` (the router) and `orchestrator-role.md` (the launch envelope).

**Candidate remedies.**
1. **Declare and record.** The launch envelope states the session must be new; the Lead affirms in
   the Return Packet's provenance block that it read only the brief, `engineering-role.md`, and the
   named plan. Cheap, checkable at the receipt gate, and honest about being cooperative.
2. **Label the guarantee.** Adopt an explicit `ASSERTED_ROLE_BOUNDARY` label, in the same spirit as
   `COOPERATIVE_PROCEDURAL`, so no packet implies an enforcement the harness does not provide.
3. Harness-level read allowlisting, if and when the tooling supports it. Not available today, and
   not worth building — see the standing preference for procedural controls that are honestly
   labelled over machinery that overstates itself.

**Recommendation:** 1 + 2. They cost two lines each and close the disclosure gap, which is the part
that actually failed here.

---

## D-CP0-2 — The terminal-status taxonomy has no slot for an invalid brief

**Statement.** `capstone_V6_5.md` §12 defines exactly four terminal statuses: `PASS`, `BLOCKED`,
`PLATEAU`, `BUDGET_EXHAUSTED`. `engineering-role.md:7` separately requires the Lead to "stop and
return the discrepancy" when a brief is invalid. That return is a **fifth terminal outcome with no
name, no form, and no place in the Return Packet**, whose template requires one of the four
statuses.

**Evidence.** The 2026-08-05 discrepancy return — eight of ten required brief fields missing — had
no defined shape in any contract document. It was authored ad hoc.

**Impact.** Three consequences, in increasing severity:
- The Orchestrator receipt (`gauntlet-templates.md` §8) gates a *packet*. A discrepancy return is
  not a packet, so it passes through **no gate at all**.
- `progress.md` has no vocabulary to record it. A checkpoint that was attempted, correctly refused,
  and never opened is indistinguishable in program state from one never attempted.
- Because it is unnamed, there is no rule about what happens next: whether the reissued brief is a
  new checkpoint attempt, whether the refusal is evidence, whether it is reportable at all.

**Ownership.** `capstone_V6_5.md` §12 owns the status vocabulary (the bar); `engineering-role.md`
owns the mechanism; `gauntlet-templates.md` owns the form.

**Candidate remedies.**
1. **Add `BRIEF_INVALID` as a pre-work terminal status** with a minimal form: the missing or
   contradictory required fields, whatever repository state the Lead did verify, and an explicit
   "no clock consumed, no repository edit made" line. Requires a §12 amendment and a ninth template.
2. Fold it into `BLOCKED` with a required subtype. Cheaper — no new status — but muddies `BLOCKED`,
   which today means *work started and hit an owner-only dependency*, a materially different thing
   from *work never started because the authorization was malformed*.

**Recommendation:** 1. The distinction is real and the receipt gate needs it.

---

## D-CP0-3 — The clock has no defined start on a rejected brief

**Statement.** The ceiling "covers the whole checkpoint run from orientation through the terminal
Return Packet" (`engineering-role.md` § *Active-elapsed wall-clock ceiling*), and orientation
includes brief validation. But a rejected brief produces no packet, and the packet is the only place
`started_at_utc` and `consumed_active_elapsed_seconds` are recorded. Whether validation time is on
the clock is therefore **undefined**.

**Evidence.** Direct consequence of D-CP0-2, surfaced in the same return. Both readings are
defensible from the current text.

**Impact.** Two failure modes, in opposite directions:
- If validation is on the clock, a sequence of malformed briefs can silently consume a checkpoint's
  entire ceiling without any work being done, and the eventual valid brief starts already depleted.
- If it is not, there is no recorded cost to issuing bad briefs, and no signal in program state that
  the checkpoint was attempted more than once.

Neither is catastrophic at CP-0's 2 h reserve. Both become material at CP-1's larger allocation, and
the ambiguity compounds with D-CP0-5, where a stalled run consumes real time that no packet records.

**Ownership.** `engineering-role.md` § *Active-elapsed wall-clock ceiling*.

**Candidate remedies.**
1. State explicitly that **brief validation precedes the clock and consumes no ceiling**; the clock
   starts at the first repository-state verification performed under a valid brief. One sentence.
2. Require any `BRIEF_INVALID` return (per D-CP0-2) to carry `validation_started_at_utc` and
   `returned_at_utc` as a record, explicitly excluded from the ceiling — so the cost is visible
   without being charged.

**Recommendation:** 1 + 2 together. 1 resolves the ambiguity; 2 preserves the signal that 1 would
otherwise discard.

---

## D-CP0-4 — The only validity gate is judged by the party that benefits from passing it

**Statement.** The Lead validates its own brief, and nothing independently confirms that validation
happened or was correct. This is structurally the same defect the architecture closes at the piece
level — a Builder may not grade its own work — displaced one level upward, where it is not closed:
**Lead ≠ brief-validator is not enforced.**

**Evidence.** `engineering-role.md:7` and § *Required brief fields* assign validation to the Lead.
`gauntlet-templates.md` §8 gates the packet against the checklist, the verdicts, and the Integration
`PASS` — it never asks whether the brief that authorized the run was itself valid.

**Impact.** A permissive Lead proceeds on an underspecified brief, and the resulting `PASS` rests on
a bar that no one confirmed was complete. The failure is silent by construction: a brief missing its
complete-checklist citation produces a packet whose criteria table maps whatever subset the Lead
inferred, and the receipt gate checks that table against the brief it was given — not against the
plan. The self-certification ban is enforced against the Builder and the Lead's *work*, but not
against the Lead's *authorization*.

**Ownership.** `gauntlet-templates.md` §8 (the receipt gate) and `engineering-role.md`
§ *Terminal conditions and checkpoint return*.

**Candidate remedies.**
1. **Require the Return Packet to reproduce the brief's ten required fields verbatim.** The
   Orchestrator then checks validity retroactively at the receipt gate, against the plan it holds.
   No new agent, no new context, one table.
2. Have the Integration Critic confirm the packet's criteria table covers the complete named
   checklist at the cited plan and version. It already reads the plan and already verifies checklist
   coverage; extending it to the brief's completeness is nearly free.

**Recommendation:** 1, with 2 if it proves cheap in practice at CP-0. 1 alone closes the hole,
because the Orchestrator is the party that wrote the brief and can see immediately what it omitted.

---

## D-CP0-5 — No stated execution-capability floor, and a stalled executor returns no status

**Statement.** The contract names no minimum executor capability, while assuming one: an agent able
to hold roughly 8,500 words of contract and plan while creating worktrees, routing Builders and
Critics, and maintaining the clock. Below that threshold the run does not fail — it **stalls**, and
a stalled run produces no terminal status at all.

**Evidence.** 2026-08-05: a CP-0 execution attempt on a low-reasoning-effort configuration stalled
without returning any status. No packet, no `BLOCKED`, no partial evidence. The attempt was
abandoned and reissued to a different executor configuration.

**Impact.** This is the deepest of the five, because it breaks an assumption the whole upward
contract rests on: **that the executor always terminates.** All four statuses describe *outcomes of
a run that finished*. Silence is not among them, and `orchestrator-role.md` explicitly withdraws the
silence-means-success convention for Track B — correctly — while providing no replacement. The
Orchestrator therefore cannot distinguish *still working* from *dead*, and has no defined waiting
period after which it may act. Together with D-CP0-2, the taxonomy has two holes on the same edge:
one for runs that never legitimately start, one for runs that never legitimately end.

There is a second-order effect worth recording: the Phase 1 prune reduced agent-facing prose to
~8,500 words on the argument that context cost was the binding constraint. That measurement said
nothing about the *reasoning* capacity needed to act on those words, which is what actually failed
here. Smaller context did not make the contract executable by a weaker executor.

**Ownership.** `orchestrator-role.md` (the launch envelope and the checkpoint-waiting convention);
`capstone_V6_5.md` §12 (the status vocabulary).

**Candidate remedies.**
1. **Name a minimum executor tier and reasoning effort in the launch envelope**, as a stated
   precondition of the contract, the same way hardware and budget are stated constraints.
2. **Define an owner-side abandonment convention:** a run whose real elapsed time materially exceeds
   its active-elapsed ceiling with no packet is treated as abandoned. It is not
   `BUDGET_EXHAUSTED` — that status asserts the ceiling was consumed by work, which an abandoned run
   cannot evidence. It needs its own name, and it needs to be recordable in `progress.md` so a
   reissued brief is visibly a second attempt.
3. Require the Lead to emit `started_at_utc` and its verified repository state as a first
   observable output, so an abandoned run leaves at least the evidence that it began.

**Recommendation:** all three. 1 is prevention, 2 is the missing status, 3 is the minimum forensic
trace — and 3 is what would have made this stall diagnosable instead of merely observable.

---

## Cross-cutting observation

Four of the five defects (D-CP0-2 through D-CP0-5) are **edge conditions of the run, not of the
work**: what happens before a valid run starts, and what happens when a run does not end. The
contract is detailed and well-owned about the middle — decomposition, isolation, verdicts,
staleness, integration, closure — and thin at both boundaries.

That is the predictable shape of a contract written by reasoning forward from a successful run.
D-CP0-1 is the exception and the more uncomfortable one: it is not an edge case but a standing
property, and it is only visible from outside the session that violates it.

---

## Open — awaiting CP-0's Return Packet

Sonnet's Lead session was issued a completed CP-0 brief on 2026-08-05 and is running. Append here:

- defects surfaced during Builder → Critic → repair cycles;
- defects in the verdict form (`gauntlet-templates.md` §5) once one is actually written;
- whether the computed-staleness rule (`engineering-role.md:39`) is usable by hand at CP-0's scale,
  or whether it only pays off at CP-1's;
- whether `git worktree --detach` isolation held in practice, and what it cost in wall-clock;
- whether the 2 h reserve bore any relation to the real ceiling consumed;
- whether the Return Packet's defense questions were answerable by the owner.
