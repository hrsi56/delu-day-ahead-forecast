# CP-0 operational defects — the Gauntlet contract's own findings

**Status: OPEN — 20 defects. 17 ACCEPTED · 3 REMEDIED but not re-tested · 1 amendment WAIVED BY
OWNER.**

The v6.6 amendment was ratified 2026-08-05, hardened across seven independent review rounds, and put
to its acceptance test on 2026-08-06 by the clean-room CP-0 re-run. **That run returned `PASS` on all
seven CP-0 checklist items**, the receipt gate verified it against the repository rather than the
packet's claims, and the candidate landed on `main` as `a911191`. The Phase-5 matrix in
`docs/track-b/gauntlet-amendment-plan.md` then judged the amendment itself: **11 of 13 accepted on
observed behaviour.**

- **D-CP0-1 … D-CP0-17 — ACCEPTED.** Each was remedied and its remedy exercised by the run.
- **D-CP0-18 — REMEDIED 2026-09-03, not re-tested.** AMD-G7 failed its acceptance test,
  self-reported by the executor; the owner-authorized remedy is recorded at `6ea6a20`.
- **D-CP0-19 — REMEDIED 2026-08-06, not re-tested.** Found by the reclamation guard at landing.
- **D-CP0-20 — REMEDIED 2026-08-10, not re-tested.** Found by an agent reading the corpus to document
  it. Fixed under **the first authorized suspension of the Governance Lockdown**.
- **AMD-G5 — WAIVED BY OWNER, 2026-09-04.** The `BRIEF_INVALID` negative control was skipped at the
  CP-0 re-run and, after being re-proposed twice, was **declined as an informed owner decision** — a
  deliberate risk acceptance, not an oversight, and **not an open item**. **What is waived is the
  test, not the mechanism:** `BRIEF_INVALID`, its clock-exclusion rule and the §10 form remain fully
  in force under the ratified contract, and an Engineering Lead meeting a malformed brief must still
  return on that form. They simply ship unexercised. The compensating control is the Orchestrator's
  mandatory pre-dispatch brief validation (`orchestrator-role.md`), which was always the primary
  gate; the waiver removes the backup test, not the primary control. **Do not re-raise this as a
  pending test, a ledger condition, or a risk-reduction suggestion.**

**This ledger stays OPEN.** It closes when D-CP0-18's and D-CP0-19's remedies are re-tested. The
AMD-G5 clause was struck from this condition on 2026-09-04 under an owner-authorized, task-scoped
suspension of the Governance Lockdown, because the owner waived that test; every other closure
condition is unchanged and no bar moved. **An amendment authored is not an amendment proven** — and
two of these were found only because the contract was executed rather than read.

**CP-0 attempt 1 is closed `PASS`, never landed, and now archived.** Owner decision of record,
2026-08-05: nothing from it merges to `main`, and CP-1 is not briefed until the contract itself is
fixed. Its branch `gauntlet/cp-0` was retired on 2026-08-05 under the tag-before-delete rule; **every
SHA this document cites is preserved at the annotated ref `archive/cp-0-attempt-1` (= `8f371e5`)**
and is reachable from it. Attempt 1 is superseded by a clean-room re-run, not merged
(`docs/track-b/gauntlet-amendment-plan.md`, DEC-3).

> **Reading SHAs in this document.** Every `gauntlet/cp-0` reference below is historical — it records
> what was true during attempt 1. To inspect any cited SHA today, use the archive tag:
> `git show archive/cp-0-attempt-1`, `git log --oneline main..archive/cp-0-attempt-1`,
> `git show <sha>`.

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
| 2026-08-05 | CP-0 Return Packet (`PASS`; `final_candidate_sha` `63ebfab`, `evidence_tip_sha` `8f371e5`, on `gauntlet/cp-0`) and Orchestrator receipt-gate verification of it | D-CP0-6 … D-CP0-11 |
| 2026-08-05 | Owner's standing requirement that no unnecessary branch ever stay open, and the ref cleanup that followed CP-0 | D-CP0-13 |
| 2026-08-05 | The v6.6 amendment rule inventory (`rule-inventory.md`, Phase 2.1) | D-CP0-14, D-CP0-15 |
| 2026-08-05 | Authoring AMD-G11 in Phase 2.2 | D-CP0-16 |
| 2026-08-05 | The third independent review of the v6.6 amendment (Phase 2.3) | D-CP0-17 |
| 2026-08-06 | The CP-0 clean-room re-run — self-reported by the Engineering Lead against its own run, and confirmed by the Phase-5 acceptance matrix | D-CP0-18 |
| 2026-08-06 | Executing the `LAND` disposition and reclamation for CP-0 | D-CP0-19 |
| 2026-08-10 | An independent agent reading the corpus to write the public method article | D-CP0-20 |

D-CP0-1 … D-CP0-5 were found **before a single line of CP-0 product code was written** — the
contract's own front gate producing findings on its first real contact with an execution attempt.
D-CP0-6 … D-CP0-19 came from checkpoints that **passed cleanly**, from authoring the amendment, from
seven independent reviews of it, and from executing the landing — which is the more useful result:
the loop worked and the contract around it did not quite. Two defects surfaced only under execution,
after seven text reviews had found nothing further.

## Defect index

| ID | One line | Owner document | Severity |
|---|---|---|---|
| D-CP0-1 | Role is asserted, never verified | `AGENTS.md`, launch envelope | Standing |
| D-CP0-2 | No terminal status for an invalid brief | `capstone_V6_6.md` §12, templates | High |
| D-CP0-3 | No defined clock start on a rejected brief | `engineering-role.md` ceiling § | Medium |
| D-CP0-4 | Brief validity judged by its beneficiary | templates §8, `engineering-role.md` | High |
| D-CP0-5 | No execution-capability floor; a stall returns no status | `orchestrator-role.md`, §12 | High |
| **D-CP0-6** | **Integration cannot review the commit recording its own verdict** | **§12 item 7, `engineering-role.md` 8–9** | **Blocking — structurally unsatisfiable** |
| D-CP0-7 | Candidate provenance unspecified; disclosure voluntary | `engineering-role.md` step 4, templates | Medium |
| **D-CP0-8** | **Honest disclosure required violating the role boundary** | **`engineering-role.md:9`** | **High — inverts the incentive** |
| D-CP0-9 | Cache-routing rule unenforceable by its own test | `engineering-role.md:56` | Low |
| D-CP0-10 | Concurrent sessions on one repository are unmodelled | `AGENTS.md`, `engineering-role.md` step 1 | Medium |
| D-CP0-11 | Volunteered line citations create false discrepancy signals | templates §5 | Low |
| **D-CP0-12** | **No defined landing path from candidate branch to `main`** | **`AGENTS.md`, templates §8** | **High — blocks acceptance** |
| **D-CP0-13** | **No branch or ref reclamation rule** | **`AGENTS.md`, `orchestrator-role.md`, templates §9** | **High — blocks acceptance** |
| D-CP0-14 | `orchestrator-role.md` was never rule-inventoried | `rule-inventory.md`, `orchestrator-role.md` | Medium |
| D-CP0-15 | The rule ledger's own statements went stale after Option C | `rule-inventory.md` | Medium |
| **D-CP0-16** | **The verdict form omits `reviewed_paths`, which computed staleness depends on** | **templates §5** | **High — the staleness rule's input was never collected** |
| D-CP0-17 | `AGENTS.md` was never rule-inventoried either | `rule-inventory.md`, `AGENTS.md` | Medium |
| **D-CP0-18** | **`started_at_utc` is required but the executor has no clock unless told to call one** | **`engineering-role.md` step 1** | **High — failed its own acceptance test** |
| **D-CP0-19** | **`LAND` tags the landing point or the reviewed chain, and the contract named only one** | **`AGENTS.md` R2** | **High — caught at the reclamation guard** |
| **D-CP0-20** | **The Orchestrator's limit was written as a capability ("no shell"), not a scope** | **`orchestrator-role.md`** | **Medium — REMEDIED 2026-08-10** |

D-CP0-1 … D-CP0-17 are remedied by the **v6.6 amendment (AMD-G1 … G14)**, ratified 2026-08-05 and
recorded in `capstone_V6_5-to-V6_6-amendments.md`, **and accepted 2026-08-06** by the clean-room CP-0
re-run. D-CP0-18 and D-CP0-19 came out of that run and its landing. The drafts for the three original
blocking items are kept below as the record of how they were reasoned through.

---

## D-CP0-1 — Role is asserted, never verified

**Status: REMEDIED BY AMD-G2 + G4 — pending acceptance in the CP-0 re-run.**

**Statement.** `AGENTS.md` routes every session to a role and forbids an Engineering-Lead session
from reading `orchestrator-role.md`, `progress.md`, the syllabus, or Track A/C material during
execution. Nothing detects or prevents a session that has *already* read them from then declaring
itself the Lead. The role boundary is a declaration, not a verified property.

**Evidence.** On 2026-08-05 a session that had read `orchestrator-role.md`, `progress.md`,
`docs/track-b/rule-inventory.md`, the Hebrew guide, and `capstone_V6_6.md` §11–§12 in full — for
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

**Status: REMEDIED BY AMD-G5 — remedy stands; its acceptance test is WAIVED BY OWNER, 2026-09-04
and will not run.**

**Statement.** `capstone_V6_6.md` §12 defines exactly four terminal statuses: `PASS`, `BLOCKED`,
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

**Ownership.** `capstone_V6_6.md` §12 owns the status vocabulary (the bar); `engineering-role.md`
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

**Status: REMEDIED BY AMD-G5 — remedy stands; its acceptance test is WAIVED BY OWNER, 2026-09-04
and will not run.**

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

**Status: REMEDIED BY AMD-G6 — pending acceptance in the CP-0 re-run.**

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

**Status: REMEDIED BY AMD-G4 + G7 — pending acceptance in the CP-0 re-run.**

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
`capstone_V6_6.md` §12 (the status vocabulary).

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

---

# Findings from the CP-0 run — 2026-08-05

CP-0 returned **`PASS`** on `gauntlet/cp-0`, 2727 s of a 7200 s ceiling. Under v6.6 its `final_candidate_sha` is **`63ebfab`** — the SHA the Integration Critic reviewed — and its `evidence_tip_sha` is **`8f371e5`**.
The receipt gate accepted it; the verification behind that acceptance is recorded at the end of this
section. Six further defects follow. **None of them invalidates the CP-0 `PASS`**, and none touches a
capstone bar.

## D-CP0-6 — Integration cannot review the commit that records its own verdict

**Status: REMEDIED BY AMD-G1 — pending acceptance in the CP-0 re-run.**

**Statement.** Two rules that are individually correct cannot both be satisfied. CP-0 item 7 requires
a "fresh Integration-Critic `PASS` **at the exact final candidate SHA/tree**." `engineering-role.md`
§ *Evidence retention* requires each verdict to be committed **after** its review completes, "so the
reviewed candidate SHA is never altered by the act of recording the review." For the Integration
verdict — the last one, with nothing above it — recording it necessarily creates a commit that no
Integration Critic has reviewed. **There is no ordering that satisfies both.**

**Evidence.** Verified directly, not taken from the packet:

```text
git show 8f371e5:docs/track-b/evidence/cp-0/integration-round1.md | grep "Candidate SHA"
  → Candidate SHA: 63ebfaba701fbe54e5533170ac89c08204184446
git diff --stat 63ebfab..8f371e5
  → docs/track-b/evidence/cp-0/integration-round1.md | 73 ++++++ (1 file changed)
```

The Return Packet declares `8f371e5` the final candidate. The Integration Critic reviewed `63ebfab`.
So either the packet's final-candidate field is wrong, or item 7 is unsatisfied — and no third
option exists. This is structural, not an execution error: it recurs identically at every checkpoint.

**Impact.** The branch tip is always outside the reviewed set. Today that is harmless because the
delta is provably one file under `docs/track-b/evidence/` — but *nothing in the contract says it has
to be*. The same sequence would accept a tip commit that also touched source, and no verdict would
cover it. The rule that closes the loop is missing, not merely unstated.

**Ownership.** `capstone_V6_6.md` §12 (item 7 wording) and `engineering-role.md` §§ *Gauntlet
execution* step 8 / *Evidence retention*.

**Candidate remedies.**
1. **Define the final candidate as the SHA the Integration Critic reviewed**, and require the branch
   tip above it to be verdict-only — enforced by a stated check the Orchestrator can run:
   `git diff --name-only <final-sha>..<tip>` must contain nothing outside
   `docs/track-b/evidence/<checkpoint>/`. Rewrite item 7 to bind that SHA, and have the Return Packet
   carry both `final_candidate_sha` and `evidence_tip_sha` as distinct fields.
2. Commit the Integration verdict to a separate evidence branch, leaving the candidate tip exactly at
   the reviewed SHA. Cleaner conceptually, but it splits provenance across two refs and forfeits "the
   candidate SHA plus the branch is the whole provenance chain."

**Recommendation:** 1. It is two fields, one check, and it makes explicit the property the current
run happens to satisfy by luck.

---

## D-CP0-7 — Candidate provenance is unspecified, and disclosure is voluntary

**Status: REMEDIED BY AMD-G8 — pending acceptance in the CP-0 re-run.**

**Statement.** `engineering-role.md` step 4 assumes a Builder authors its piece from the brief.
Nothing states where a Builder's starting tree may come from, whether pre-existing unreviewed work
may seed it, or that its origin must be disclosed.

**Evidence.** The Lead found a substantial uncommitted draft of exactly this instrument — 38 passing
tests — in a *different, earlier session's* scratch worktree under `/private/tmp`, and seeded a fresh
Lead-created Builder worktree from it rather than rebuilding. That worktree is still registered:
`.../23cc0d4e-.../scratchpad/gauntlet/builder-instrument`, detached at `d7bdd5f`, uncommitted.

**Impact.** The engineering call was sound, and the artifact then passed genuinely independent review
— which is precisely the design's claim: provenance should not matter if the artifact is judged
independently against the bar. Two things qualify that.

First, **the bar is a checklist, not a completeness statement.** A Critic confirms seven properties
hold. It does not confirm that nothing else is present. Independent review of an artifact of unknown
origin is weaker than independent review of an artifact built to the brief, and the contract does not
distinguish them.

Second, and worse: **only the Lead's own candour surfaced this.** No rule required the disclosure,
nothing would have detected its absence, and the receipt gate does not ask. A packet that omitted the
paragraph would have passed identically.

**Ownership.** `engineering-role.md` step 4; `gauntlet-templates.md` §7 (packet) and §8 (receipt).

**Candidate remedies.**
1. Require the Return Packet to state each Builder worktree's seed — brief-authored, or copied from a
   named path at a named SHA/state — as a mandatory field, and add it to the §8 receipt gate.
2. State explicitly that seeding from prior unreviewed work is **permitted**, since forbidding it
   would waste sound work, but that a seeded piece requires the Critic to review the whole artifact
   rather than a diff. (That is what happened here; it should not depend on the Lead choosing it.)

**Recommendation:** both. 1 makes it visible, 2 makes the review strength explicit.

---

## D-CP0-8 — Honest disclosure required violating the role boundary

**Status: REMEDIED BY AMD-G2 — pending acceptance in the CP-0 re-run.**

**Statement.** `engineering-role.md:9` forbids the Lead from reading `progress.md` or
`orchestrator-role.md` "during Track B execution." The Return Packet is written during execution —
terminal return is its end, not a phase after it. A Lead that discovers something needing honest
disclosure in the packet must read program state to describe it accurately, and thereby breaches the
rule. **The contract makes candour a violation.**

**Evidence.** The Lead read only the brief, `AGENTS.md`, `engineering-role.md`, `capstone_V6_6.md`
§§3/4.0/12, and the templates for the entire Builder → Critic → Integration sequence — then, after
the candidate was built, committed, and twice independently `PASS`'d, read a `progress.md` diff and
this ledger in order to write its addendum truthfully. It disclosed the read, its timing, and its
scope unprompted.

**Impact.** Conduct that the architecture should reward is technically non-compliant. Worse for the
health of the contract: the *safe* move under the current text is to disclose nothing, since silence
is compliant and disclosure is not. That is exactly backwards, and it directly undercuts the remedy
proposed for **D-CP0-1**, which asks the Lead to affirm its read-scope in the packet — an affirmation
the current rule would make it unable to write honestly.

**Ownership.** `engineering-role.md:9`.

**Candidate remedies.**
1. Scope the prohibition to the decision-bearing phase: no program-state read may inform
   decomposition, a Builder brief, a Critic brief, a verdict, or a repair. Reads performed **after
   the final Integration verdict, solely to author the packet**, are permitted and must be declared
   with their timing.
2. Require the packet's provenance block to state read-scope and the timing of any late read, making
   the declaration the control rather than the silence.

**Recommendation:** both, as one edit. This is the cheapest high-value fix in the ledger.

---

## D-CP0-9 — The cache-routing rule is unenforceable by its own cleanliness test

**Status: REMEDIED BY AMD-G9 — pending acceptance in the CP-0 re-run.**

**Statement.** `engineering-role.md:56` requires generated caches and outputs to be routed outside
the Critic worktree "so an ignored byproduct does not muddy that check." The check itself is
`git status --porcelain` returning empty — which **cannot observe a gitignored byproduct**. A Critic
that ignores the routing rule passes the test that the rule exists to protect.

**Evidence.** The component Critic ran `uv run` inside its worktree, creating `.venv/` and
`src/pit_capture/__pycache__/`. Both are gitignored, `git status --porcelain` printed nothing, and
the cleanliness determination passed. The Critic disclosed this in its verdict.

**Impact.** Low severity, real defect. The rule is advisory in practice while written as mandatory,
and the gap is invisible to every party downstream. Note the honest disclosure here came, again, from
the reviewer volunteering it.

**Ownership.** `engineering-role.md:56`; `gauntlet-templates.md` §4.

**Candidate remedies.**
1. Make the check `git status --porcelain --untracked-files=all --ignored=matching` and state the
   expected non-empty exceptions, so routing violations are visible.
2. Or drop the routing rule to a recommendation and rely on `--porcelain` alone, accepting that
   ignored byproducts are harmless. Cheaper and arguably correct — but then say so, rather than
   stating a mandatory rule nothing checks.

**Recommendation:** 2, unless a case is found where an ignored byproduct actually changes a verdict.
An unenforced mandatory rule is worse than an honest recommendation.

---

## D-CP0-10 — Concurrent sessions on one repository are unmodelled

**Status: REMEDIED BY AMD-G10 — pending acceptance in the CP-0 re-run.**

**Statement.** The contract makes the Lead the sole Git writer *within* a checkpoint but says nothing
about other sessions operating on the same repository at the same time, on sibling branches or in
other worktrees.

**Evidence.** During CP-0, this Orchestrator-side session committed `b8b70e6` to
`claude/gauntlet-loop-article-19d7ae` roughly one minute after the candidate's instrument commit.
Six worktrees were registered against the repository concurrently, including an orphan from a third
session. The Integration Critic discovered the sibling branch through a git-topology sweep and
reconciled it correctly — but **no rule required that sweep**, and nothing would have flagged a
sibling commit that did touch the reviewed paths.

**Impact.** Benign here, and partly by deliberate care: the sibling commit avoided `main` precisely
so the Lead's expected-state verification would hold. That care was ad hoc. A concurrent session
editing `progress.md` or a reviewed path mid-checkpoint would corrupt state verification or verdict
staleness with no defined detection.

**Ownership.** `AGENTS.md` (the router) and `engineering-role.md` step 1.

**Candidate remedies.**
1. Require the Lead to record the repository's worktree and branch topology at `started_at_utc` and
   again at terminal return, and to report any change — making the Integration Critic's ad-hoc sweep
   a stated obligation.
2. State in `AGENTS.md` that while a checkpoint is open, no other session may write to the target
   repository's `main` or to any path inside the checkpoint's owned set.

**Recommendation:** both. 2 is the rule; 1 is the detection.

---

## D-CP0-11 — Volunteered line citations create false discrepancy signals

**Status: REMEDIED BY AMD-G11 — pending acceptance in the CP-0 re-run.**

**Statement.** The contract requires a **verbatim excerpt** verified present in the cited plan at the
candidate SHA. It says nothing about line numbers. Both critics volunteered line ranges anyway, and
one was wrong.

**Evidence.** `**CP-0**` sits at line 459 of `capstone_V6_6.md` (verified independently). The
component verdict cited "lines 456-461"; the correct range for its five-item excerpt is 459-464. The
Integration Critic caught the discrepancy and correctly classified it as cosmetic — the quoted text
was verbatim-correct throughout. It was the only defect either critic found in the other's work.

**Impact.** The contract's actual mechanism worked perfectly: verbatim text matched at the candidate
SHA, twice. The single "defect" surfaced in review was in decoration the contract never asked for and
does not check. Left unaddressed, unspecified metadata will keep generating findings that look like
process failures and are not — which is a slow way to erode trust in the verdicts that matter.

**Ownership.** `gauntlet-templates.md` §5.

**Candidate remedies.**
1. State that a line citation is optional and non-binding, and that only the verbatim excerpt and its
   presence at the candidate SHA are load-bearing. One sentence in the form.
2. Or require line ranges and make them a checked field. More precise, more brittle — line numbers
   move with every plan edit while the text does not, which is exactly why the excerpt mechanism was
   chosen over a citation in the first place.

**Recommendation:** 1.

---

## D-CP0-12 — No defined landing path from the candidate branch to `main`

**Status: REMEDIED BY AMD-G3 — pending acceptance in the CP-0 re-run.**

**Statement.** The contract describes in detail how a checkpoint is built, reviewed, and closed in
*program state* — and says **nothing about how the reviewed code reaches `main`**. The Return Packet
ends with "Track B has stopped." `AGENTS.md` states that `main` is written by Yarden by hand after
his own review. Between those two sentences there is no defined operation, no inspection procedure,
and no artifact telling the owner what he is being asked to accept.

**Evidence.** CP-0 returned `PASS` on 2026-08-05 with its artifact on the local disposable branch
`gauntlet/cp-0`. The checkpoint is closed in `progress.md`. The code is on a branch explicitly
described as disposable, `main` is untouched at `d7bdd5f`, and the contract provides no next step.
The packet did not enumerate what the run left behind; the orphaned worktree at
`.../23cc0d4e-.../scratchpad/gauntlet/builder-instrument` surfaced only because the Integration
Critic ran an unrequired topology sweep (see D-CP0-10).

**Impact.** Three distinct gaps, all owner-facing:

1. **No inspection surface.** The Orchestrator gates a *packet*. It has no defined way to see the
   branches, worktrees, and SHAs the Engineering Lead actually created, or how the candidate differs
   from `main`. It is asked to close a checkpoint without a view of the tree that checkpoint
   produced.
2. **No acceptance operation.** "Written by hand after his own review" is a policy, not a procedure.
   Without a named operation the owner either invents one per checkpoint or defers indefinitely —
   and deferral is what actually happened: CP-0 is closed and unlanded.
3. **No cleanup obligation.** The Lead may only remove worktrees it created this checkpoint, which is
   correct, but nobody is charged with *enumerating* what exists at terminal return so the owner can
   act on the rest.

**This is also the clean resolution of D-CP0-6.** A squash merge collapses the candidate commit, the
component verdict commit, and the evidence-tip commit into **one owner-authored commit on `main`**
whose tree is the reviewed tree plus its verdicts. The circularity is a property of the *candidate
branch's* commit ordering; it does not propagate to `main`, because `main` never replays that
ordering. Landing by squash is therefore not merely convenient — it is the step at which the
D-CP0-6 anomaly is discharged rather than inherited.

**The required capability, precisely.** The Orchestrator must be able to (a) inspect the trees and
branches the Engineering Lead opened, (b) decide on a **local squash merge**, and (c) execute it
**without producing an automatic commit** — leaving the result staged in the working tree for the
owner to inspect and commit by hand. `git merge --squash` has exactly these semantics: it applies the
merged tree to the index and working tree and deliberately stops short of creating a commit. It is
the operation `AGENTS.md`'s hand-written-`main` rule has always implied without ever naming.

**Ownership.** `AGENTS.md` (git and publication authority); `gauntlet-templates.md` §7 (packet) and
§8 (receipt gate); a new §9 landing form.

**Candidate remedies.** Drafted as **AMD-G3** below.

---

## D-CP0-13 — No branch or ref reclamation rule

**Status: REMEDIED BY AMD-G13 — pending acceptance in the CP-0 re-run.**

**Statement.** Nothing in the contract says what happens to `gauntlet/<checkpoint>`, or to any
worktree, after a checkpoint closes. Refs accumulate silently across sessions, and there is no rule
preventing the deletion of a branch that live documents still depend on.

**Evidence.** The 2026-08-05 cleanup found **six worktrees and eight local branches** against one
repository, including an orphan from a third session, none of which any rule required anyone to
reclaim. Simultaneously, this document cited `7526310`, `63ebfab`, and `8f371e5` — all reachable
**only** from `gauntlet/cp-0`. Deleting that branch as "cleanup" would have left the ledger citing
SHAs that garbage collection is free to destroy.

**Impact.** Two failure modes pulling in opposite directions: refs accumulate until nobody knows
which are live, and the obvious remedy — delete them — silently breaks the evidence chain the whole
architecture rests on. The contract has no position on either.

There is a third, subtler face. Preserving the SHA is not the same as preserving the citation: a tag
that keeps `8f371e5` reachable while the prose still says "reachable on that branch" satisfies the
mechanism and defeats its purpose. Ref hygiene and document hygiene are one operation, and nothing
said so.

**Ownership.** `AGENTS.md`, `orchestrator-role.md`, `gauntlet-templates.md` §9.

**Remedy.** AMD-G13 — branch accountability (every branch an agent opens is declared in its terminal
return) with owner escalation for anything unaccounted, LAND/DISCARD dispositions, tag-before-delete,
and the citation-follows-ref rule, with an execution split that delegates reclamation to agents and
keeps authorship of `main` with the owner. The single-branch invariant first drafted here was retired
on 2026-08-05: it optimised a multi-agent repository for one agent at a time. Full draft in `docs/track-b/gauntlet-amendment-plan.md`.

**Status.** The procedure was executed manually on 2026-08-05, before the rule existed:
`archive/cp-0-attempt-1` tagged and verified, seven citations in this document repointed, then
`gauntlet/cp-0` and the last article branch deleted. AMD-G13 codifies what was done so it stops
depending on anyone remembering it.

---

## D-CP0-14 — `orchestrator-role.md` was never rule-inventoried

**Status: REMEDIED BY AMD-G14 (domain Q) — pending acceptance in the CP-0 re-run.**

**Statement.** The Phase 1 rule inventory enumerated four documents — `capstone_V6_6.md` §12,
`engineering-role.md`, `gauntlet-templates.md`, and the then-separate CP-2 protocol file. It did not
enumerate `orchestrator-role.md`. **The entire Orchestrator side of the contract has never been
enumerated, single-owned, or verified against loss.**

**Evidence.** `rule-inventory.md` header, *Sources inventoried (complete read)*. Domain N covers the
receipt gate, but it lives in the templates; the launch envelope, the B-Claude block contract, the
checkpoint-verification rules, and the progress-regeneration contract are all in
`orchestrator-role.md` and appear in no domain.

**Impact.** Half the contract has no drift protection. The Phase 1 method exists because duplicated
prose diverges — that is how D-1 survived two sessions — and it has only ever been applied to the
executor side. Three of this amendment's own remedies (AMD-G4, G7, G13) land in `orchestrator-role.md`
and would be authored into an unenumerated document, which is precisely the condition the method
was built to prevent.

**Ownership.** `rule-inventory.md`.

**Remedy.** Enumerate `orchestrator-role.md`'s Track-B-facing rules as a new **domain Q** in the
Phase 2.1 inventory, before authoring. Done — see `rule-inventory.md` § *v6.6 amendment inventory*.

---

## D-CP0-15 — The rule ledger's own statements went stale after Option C

**Status: REMEDIED BY AMD-G14 — pending acceptance in the CP-0 re-run.**

**Statement.** Option C retired 33 rules and reduced 8 more, and recorded that as a delta section
appended to `rule-inventory.md`. The per-domain tables above it were never rewritten. **The ledger's
rule statements therefore still describe machinery that no longer exists**, and a reader who consults
a domain table gets the pre-Option-C text with no marking.

**Evidence.** `E6` still reads "same two-record contract"; `C1` still requires a "pre-created
evidence ref"; `G1` still names `.gauntlet/evidence/`; `D1`'s fields are the retired JSON schema's.
All four describe retired mechanics. Separately, `engineering-role.md:56`'s cache-routing sentence
survives in the live document as a remnant of retired `C7` — **a rule in force that the ledger says
does not exist**, which is how D-CP0-9 stayed invisible.

**Impact.** The inventory is the instrument the project uses to prove nothing was lost. An instrument
whose readings are one amendment out of date will certify a state that is not the state. This is the
same class as D-1 — a rule surviving where the record says it does not — inverted.

**Ownership.** `rule-inventory.md`.

**Remedy.** AMD-G14 extends to a restatement pass: every surviving rule whose mechanics Option C
changed is restated from the current document text, and every retired rule is struck through in place
rather than only listed in a delta section. The 8 reduced rules (`C1`, `C8`, `C13`, `D1`, `G1`, `G7`,
`G8`, `O1`) are the minimum set; `engineering-role.md:56` is re-ledgered or dropped by AMD-G9.

---

## D-CP0-16 — The verdict form omits `reviewed_paths`, the input computed staleness runs on

**Status: REMEDIED BY AMD-G11 — pending acceptance in the CP-0 re-run.**

**Statement.** `E1` requires every component verdict to declare a non-empty `reviewed_paths` set, and
`E2`–`E4` — the entire computed-staleness rule — take that set as their input. **The verdict form in
`gauntlet-templates.md` §5 has no such field.** The rule the project considers its most important
efficiency mechanism was never given a place to record its own operand.

**Evidence.** Found while authoring AMD-G11 in Phase 2.2. The §5 form's header ran
`Status · Checkpoint · Candidate SHA · Controlling plan · Bar excerpt · Artifact · Worktree clean`
— no reviewed paths. Both CP-0 verdicts complied with the form and therefore declared none. The Lead
improvised: the component verdict's `Artifact:` line (`scripts/pit_capture.py, src/pit_capture/**`)
was treated as the reviewed set, and the Integration Critic computed
`git diff --name-only 7526310..63ebfab -- scripts/pit_capture.py src/pit_capture tests pyproject.toml`
against paths that were never formally declared anywhere.

**Impact.** CP-0's staleness computation was sound because one competent Lead chose a sensible set
and one competent Critic chose a compatible one — not because the contract collected it. The rule's
stated soundness condition is *"declare `reviewed_paths` honestly and broadly"*, and a field that
does not exist cannot be declared honestly, broadly, or at all. At CP-1's seventeen checklist items and
three mandatory surfaces, two agents silently choosing different implicit sets is a live path to a
`PASS` resting on a verdict that a repair had already invalidated.

This is the same class as D-CP0-15 and D-1: a rule in force with no corresponding mechanism. It is
the sharpest instance, because the missing mechanism belongs to the rule the CP-0 run singled out as
having *worked*.

**Ownership.** `gauntlet-templates.md` §5.

**Remedy.** AMD-G11 extends to adding `Reviewed paths:` to the §5 header and to the packet's verdict
table, with the soundness condition stated on the form itself where the Critic will read it.
Authored 2026-08-05.

---

## D-CP0-17 — `AGENTS.md` was never rule-inventoried either

**Status: REMEDIED BY AMD-G14 (domain S) — pending acceptance in the CP-0 re-run.**

**Statement.** Phase 2.1 closed D-CP0-14 by enumerating `orchestrator-role.md` as domain Q, and in
the same pass made `AGENTS.md` the owner of five new rules (R1–R5) while recording its baseline as
**0**. That baseline was false. `AGENTS.md` already carried thirteen normative rules — the role
router, the publication prohibition, never-commit-to-`main`, finish-then-hand-over, the commit
exception, evidence retention, the worktree lifecycle, and the destructive-operations rule — none of
which appeared in any domain.

**Evidence.** Found by the third independent review of the v6.6 amendment. `rule-inventory.md` listed
`AGENTS.md` as a complete-read source and assigned it a baseline of 0 in the same table.

**Impact.** The instrument that certifies nothing was lost did not cover a document the amendment had
just promoted to owner. Worse than D-CP0-14 in one respect: there, an unenumerated document was left
alone; here, an unenumerated document was actively edited — the destructive-operations rule lost its
branch-deletion clause in the first authoring pass and was restored only because a reviewer noticed,
not because the ledger flagged a missing ID.

It is the same defect class as D-CP0-14 and D-CP0-15, and the third instance in three passes. The
pattern is now clear enough to state as a rule rather than rediscover: **a document that any contract
rule points at must be enumerated before it can be amended.**

**Ownership.** `rule-inventory.md`, `AGENTS.md`.

**Remedy.** Domain S, thirteen rules, enumerated in `rule-inventory.md` § *v6.6 amendment inventory*.
Baseline 128 → 141; post-amendment 153 → **168** (R7 added later by G10); `AGENTS.md` ownership
5 → **20**. AMD-G14's verification protocol now runs over 168 IDs.

---

## D-CP0-18 — `started_at_utc` is required but unobtainable without an instruction to fetch it

**Status: REMEDIED 2026-09-03 under owner authorization; not re-tested.**

**Statement.** AMD-G7 requires the Lead to emit `started_at_utc` together with its verified
repository state as the **first observable output**. `engineering-role.md` step 1 says *what* must be
emitted and never says *how* the value is obtained. A language model has no clock: unless the
contract tells it to call one, it cannot produce a wall-clock timestamp, and it will discover this
only after the moment it was supposed to record has passed.

**Evidence.** The CP-0 clean-room re-run (2026-08-06) self-reported the failure in its Return Packet:
the Lead emitted verified repository state early, as required, but captured no timestamp there. The
earliest real timestamp it held — `12:51:49Z` — came several tool calls later, during unrelated
library research. Its own words: *"The true start was somewhat earlier; I have no exact value for
it."* Consumed elapsed was therefore reported as a conservative ≈4187 s against a 7200 s ceiling.

**Impact.** Bounded here — even the conservative window sat well under the ceiling, so no terminal
determination changed. It is not bounded in general. `consumed = terminal − start − pauses` is the
enforcement mechanism for `BUDGET_EXHAUSTED`, and a start time reconstructed after the fact is not
evidence. At CP-1's larger allocation, a Lead that under-reports its start by twenty minutes reports
a consumption figure nobody can check, and the ceiling stops being a control.

The deeper defect is the shape, not the size: **G7 specified an obligation without specifying the
mechanism that makes it satisfiable.** That is the same class as D-CP0-16, where the staleness rule
required an input the form never collected — a rule in force with no way to comply.

**Ownership.** `engineering-role.md` step 1.

**Remedy (authored 2026-09-03; `6ea6a20`).** `engineering-role.md` step 1 now states the mechanism:
*"Obtain `started_at_utc` by calling `date -u +%Y-%m-%dT%H:%M:%SZ` in the same tool batch as the
first `git worktree list` / `git branch -vv` topology check, and emit both together."* One clause,
and it makes the obligation executable rather than aspirational. It remains unproven until the next
checkpoint re-tests it.

**Credit where it is due.** This defect exists in the record because the executor audited its own
compliance and reported a failure nobody would have detected from the artifacts. That is the
behaviour the provenance block and the honest-negative-result culture were built to produce, and it
is the strongest single piece of evidence that the amendment's disclosure machinery works.

---

## D-CP0-19 — `LAND` has two things worth tagging and the contract named one

**Status: REMEDIED 2026-08-06 — `AGENTS.md` R2 now requires both tags. Not yet re-tested.**

**Statement.** AMD-G13's `LAND` disposition said: squash, commit by hand, then
`git tag land/<cp> <evidence_tip_sha>`. Two different commits deserve a marker at a landing, and the
rule named only one — under a name whose plain meaning points at the other. `land/cp-0` reads as
*where the work landed*, which is the squash commit on `main`; the rule intended *the reviewed chain
that justified it*, which is `evidence_tip_sha` on the checkpoint branch. A squash commit contains
the landed **content** and none of the candidate **SHAs**.

**Evidence.** At CP-0's landing on 2026-08-06 the owner tagged `land/cp-0` at the squash commit
`a911191` — the natural reading. The reclamation guard then refused to delete `gauntlet/cp-0`:
`1a1defc`, `12abbbd` and `31022b5` were reachable from the branch and from nothing else. Deleting it
would have left every citation in both verdict files, the Return Packet and this ledger pointing at
unreachable objects.

**Impact.** Bounded only because the guard held. This is the first live case where **tag-before-delete
did the exact job it was written for**, and it fired against a tag that had been created in good faith
under the rule's own wording. An ambiguous instruction and a correct guard produced the right outcome;
the ambiguity alone would have produced evidence destruction.

**Ownership.** `AGENTS.md` § *Branch and ref lifecycle*, R2.

**Remedy (authored 2026-08-06).** `LAND` now produces **two** tags: `land/<cp>` at the squash commit
on `main`, recording where the work landed, and `evidence/<cp>` at `evidence_tip_sha`, preserving the
reviewed chain — **the second is the one tag-before-delete requires.** Applied to CP-0 in the same
operation: `evidence/cp-0` was created at `31022b5` and all three candidate SHAs re-verified reachable
before `gauntlet/cp-0` was deleted.

---

## D-CP0-20 — the Orchestrator's limit was written as a capability, not a scope

**Status: REMEDIED 2026-08-10 under the first authorized Governance Lockdown suspension. Not re-tested.**

**Statement.** `orchestrator-role.md` read: *"You do not audit evidence files yourself, **and you have
no shell**."* Those are two different claims welded into one sentence. The first is a load-bearing
authority rule — the Orchestrator must not re-derive the engineering, because if it does it becomes a
second Engineering Lead with worse information and the authority split collapses. The second was an
**environment assumption**, true when the Orchestrator was a chat session and false the moment the
role ran anywhere with a terminal. The justification had quietly become the rule.

**Evidence.** Found on 2026-08-10 by an independent agent reading the corpus in order to write the
public method article — not by any review round, and not by a checkpoint run. It observed that the
v6.6 receipt gate now requires two checks the Orchestrator must perform itself (*"run
`git diff --name-only <final>..<tip>` yourself and confirm it… Do not take the packet's word for it"*
and *"Run the §9 inspection"*) while the role document still denied it a shell. Both statements were
live and they contradicted each other. Separately, every gate command at CP-0 was in fact run from an
Orchestrator context that had a shell — so the claim was already false in practice.

**Impact.** "No shell" was a **weak fence**: it constrained the Orchestrator by accident of
environment rather than by rule, and therefore stopped constraining anything the moment the role was
instantiated somewhere with a terminal. Meanwhile the contradiction left two live documents
disagreeing about what the gate actually is, which is the condition `orchestrator-role.md`'s own
version-precedence rule says must be surfaced and never silently reconciled.

**Ownership.** `orchestrator-role.md` § *Verification and checkpoints*.

**Remedy (applied 2026-08-10).** State the limit as a limit on **scope**, not on capability. The
Orchestrator does not audit or re-derive the engineering — that was already judged by parties with
better information and no stake. It **does** run the checks that verify the packet against the
repository, because a claim accepted on the packet's word is not evidence; those checks are read-only
and **enumerated exhaustively** (seven commands), and anything beyond that list — reading source,
running tests, re-deriving a metric, inspecting a Builder workspace — is re-doing the engineering and
is forbidden. If a context has no shell the obligation does not lapse: it delegates to a read-only
agent or to the owner. **The check is mandatory in every environment; only who types it varies.**

An enumerated command list is a real fence. It survives the role moving to a context that can run
anything, which "no shell" did not.

**The pattern, third instance.** `D-CP0-16`: verdicts had to declare `reviewed_paths` and the form had
no field. `D-CP0-18`: the Lead had to emit a start time and had no way to obtain a clock. Here: an
authority limit expressed as a capability rather than a scope. Each time the rule was right and the
thing that made it *executable* was absent or wrong — and all three survived document review.

**How it was fixed matters as much as the fix.** No agent repaired this. The finding was raised, the
exact clause and its replacement were put to the owner, and the owner named the file, quoted the text,
and lifted the Lockdown for that one edit — recorded in commit `3670949` as the first authorized
suspension. The ledger entry you are reading required a second, separate authorization, because a
suspension covers one file and one change and is spent on use.

---

## What the run confirmed — recorded so the amendment does not overcorrect

Not every finding is a defect. Six properties were operationally validated for the first time, and
the amendment must not weaken them:

- **Independent review found real bugs.** The Builder's own critical read against the bar fixed three
  crash-without-ledger-entry paths — an escaping `ValueError` on malformed timestamps, an uncaught
  `LookupError` on a bogus response charset, an uncaught `OSError` on raw-artifact write failure.
  Each is exactly the failure class CP-0 item 2 exists to prevent, and each was found by requiring a
  line-by-line read against the bar rather than "make the tests pass."
- **Builder≠Critic was not theatre.** The component Critic hand-authored its fixtures outside the
  candidate checkout, computed every expectation before running anything, and never opened `tests/`.
  The Integration Critic then re-derived the Berlin DST facts a third time from bare `zoneinfo`
  without importing the candidate's own time module. Three passes, no shared evidence, converging.
- **Computed staleness worked on its first real use.** `git diff --name-only 7526310..63ebfab` over
  the reviewed paths was empty, so the component `PASS` carried to the final candidate without a
  rerun. Verified independently at the gate: `7526310` is an ancestor of `8f371e5`.
- **Worktree isolation held.** Detached HEAD confirmed by `git symbolic-ref -q HEAD` exiting 1; SHA
  and clean status matched before and after each review; `main` never moved from `d7bdd5f`.
- **The expected-state mismatch rule fired correctly.** A pre-existing `gauntlet/cp-0` branch (no
  commits ahead) contradicted the brief; the Lead reported it before relying on the brief, per B1.
- **The ceiling was generous, and now has a measurement.** 2727 s consumed against 7200 s — 38%.
  The 2 h reserve was ≈2.6× the actual for a one-piece checkpoint with two reviews. CP-1's 6 h
  reserve should be re-derived from this rather than from the original estimate, in **both**
  directions: CP-1 carries 17 checklist items and three mandatory surfaces, so it is not a linear
  scale-up of one piece.

## Receipt-gate verification behind the accepted `PASS`

Checked against the repository, not against the packet's claims: `main` clean at `d7bdd5f`;
`gauntlet/cp-0` linear at `d7bdd5f → 7526310 → 63ebfab → 8f371e5`; both cited SHAs reachable on that
branch at the time of the gate, and reachable today from `archive/cp-0-attempt-1`, which succeeded
it; `7526310` an ancestor of `8f371e5`; both verdict files present in the candidate tree; the
candidate diff confined to `pyproject.toml`, `scripts/pit_capture.py`, `src/pit_capture/**`,
`tests/**`, and `docs/track-b/evidence/cp-0/**` with no later-checkpoint scope; all seven checklist
items mapped to reproducible evidence with no open item hidden behind `PASS`.

**The `PASS` stands.** D-CP0-6's circularity does not undermine it here because the delta between the
reviewed SHA and the branch tip is provably a single evidence file — but that is a property of this
run, not a guarantee of the contract, which is the defect.

---

# Proposed amendments — DRAFT, NOT RATIFIED

Concrete replacement text for the three items that block CP-1: **D-CP0-6** (structurally
unsatisfiable), **D-CP0-8** (inverts the honesty incentive and contradicts D-CP0-1's own remedy), and
**D-CP0-12** (no acceptance path). Each states its owner document, the change, and how it is checked.

**These are drafts for owner adjudication.** Nothing here is in force. Most touch
`capstone_V6_6.md` §12, so ratification produces **capstone v6.6 with a new exact anchor**, and no
brief may cite it until that anchor exists. No draft below weakens a bar, checklist item, invariant,
or acceptance criterion; AMD-G1 and AMD-G3 make an existing requirement satisfiable, and AMD-G2
narrows a prohibition that currently forbids honest reporting.

## AMD-G1 — Separate the final candidate from the evidence tip *(closes D-CP0-6)*

**Problem restated.** Item 7 binds Integration `PASS` to "the exact final candidate SHA/tree" while
evidence retention requires each verdict to be committed after its review. The Integration verdict
has nothing above it, so committing it always produces a tip no Integration Critic reviewed. No
ordering satisfies both.

**Resolution.** Name the two SHAs, bind the bar to the reviewed one, and constrain the delta.

**(a) `engineering-role.md`, step 8 — add after the existing final-candidate designation:**

> The checkpoint has **two** terminal SHAs and they are never the same commit.
> **`final_candidate_sha`** is the SHA the fresh Integration Critic reviewed: the candidate after it
> stopped changing, carrying every component verdict. It is what every bar binds to.
> **`evidence_tip_sha`** is the branch tip after the Integration verdict itself is committed.
> The delta between them is **verdict-only**: `git diff --name-only <final_candidate_sha>..<evidence_tip_sha>`
> must return nothing outside `docs/track-b/evidence/<checkpoint>/`. A tip that touches any other path
> invalidates the terminal `PASS` and requires a new final candidate and a new Integration review.

**(b) `capstone_V6_6.md` §12 — replace the last CP-N checklist item wherever it appears:**

> - [ ] Fresh Integration-Critic `PASS` at the exact **`final_candidate_sha`**/tree, with the
>   evidence tip above it containing verdict files only.

**(c) `gauntlet-templates.md` §7 — replace the single "Final candidate commit / branch" field:**

```markdown
Final candidate SHA (Integration-reviewed; every bar binds here):
Evidence tip SHA (branch tip after the Integration verdict was committed):
Verdict-only delta confirmed: `git diff --name-only <final>..<tip>` → [paths, all under docs/track-b/evidence/<checkpoint>/]
```

**(d) `gauntlet-templates.md` §8 — add to the receipt gate:**

> 7. carries both terminal SHAs, and the diff between them contains only paths under
>    `docs/track-b/evidence/<checkpoint>/`. Run it; do not take the packet's word.

**Check.** One command the Orchestrator runs at the gate. **Retrofit:** CP-0 satisfies this as
drafted — `final_candidate_sha = 63ebfab`, `evidence_tip_sha = 8f371e5`, delta is
`docs/track-b/evidence/cp-0/integration-round1.md` alone. The amendment records what CP-0 achieved by
accident as a property the contract now requires.

## AMD-G2 — Scope the role boundary to the decision-bearing phase *(closes D-CP0-8)*

**Problem restated.** `engineering-role.md:9` forbids reading program state "during Track B
execution." The Return Packet is written during execution. A Lead needing to describe something
accurately must read program state and thereby breach the rule, so the compliant move is silence —
the opposite of what the architecture wants, and it makes D-CP0-1's proposed remedy unwritable.

**Resolution.** Forbid the *influence*, not the *reading*, and make the declaration the control.

**(a) `engineering-role.md:9` — replace the prohibition sentence:**

> During Track B execution, no read of `orchestrator-role.md`, `progress.md`, the syllabus, or Track
> A/C material may inform any engineering decision: decomposition, a Builder or Critic brief, a
> verdict, a repair, or the terminal status. Before the final Integration verdict exists, do not read
> them at all. **After** that verdict is written and no engineering decision remains, a read
> performed **solely to author the Return Packet accurately** is permitted, and must be declared in
> the packet's provenance block with its scope and timing. Silence about such a read is a defect in
> the packet, not compliance.

**(b) `gauntlet-templates.md` §7 — add a mandatory block:**

```markdown
## Provenance and read scope
Documents read during the decision-bearing phase: [exhaustive list]
Reads performed after the final Integration verdict, solely to author this packet:
  [document] — [UTC time] — [why it was necessary] — [what it did NOT influence]
Role-boundary guarantee: ASSERTED_ROLE_BOUNDARY — this is the Lead's own declaration.
  The harness does not enforce read isolation and this packet does not claim it does.
```

**(c) `gauntlet-templates.md` §8 — add to the receipt gate:** a packet with no provenance block is
returned unread. An absent block is not an assertion that no late read occurred.

**Note.** `ASSERTED_ROLE_BOUNDARY` is the same honesty pattern as `COOPERATIVE_PROCEDURAL`: name the
guarantee at its real strength rather than implying enforcement the harness does not provide. This
amendment also unblocks D-CP0-1's remedy, which cannot be adopted before it.

## AMD-G3 — Terminal handover and the owner squash merge *(closes D-CP0-12)*

**Problem restated.** The contract has no operation between "Track B has stopped" and "`main` is
written by Yarden by hand." The Orchestrator cannot see what the Lead built, and the owner has no
named acceptance step. CP-0 is closed and unlanded as a direct result.

**Resolution.** A Landing Report in the packet, an inspection procedure at the gate, and one named
owner operation that stages without committing.

**(a) `engineering-role.md` — new section, *Terminal handover*:**

> At terminal return, enumerate what the checkpoint leaves behind so the owner can act on it without
> reconstructing it. Report the checkpoint branch and both terminal SHAs; every worktree registered
> against the repository, marked as created-by-this-checkpoint (removed) or pre-existing (left, with
> its path and state); every `gauntlet/*` branch; and the exact diffstat of the candidate against
> `main`. Removing a worktree this checkpoint did not create remains owner-only. Never merge, squash,
> rebase, or fast-forward anything into `main`, and never propose doing so as an action you will take.

**(b) `gauntlet-templates.md` §7 — new section in the packet:**

```markdown
## Landing report
Checkpoint branch: gauntlet/<checkpoint>
final_candidate_sha / evidence_tip_sha:
Diff against main:  `git diff --stat main...<evidence_tip_sha>`  → [summary]
Commits on the branch: `git log --oneline main..<evidence_tip_sha>` → [list]
Worktrees created by this checkpoint: [paths] — all removed / [exceptions with reason]
Worktrees NOT created by this checkpoint: [paths, SHA, clean/dirty] — left untouched, owner-only
Other gauntlet/* branches present: [list, or none]
Proposed landing: squash `gauntlet/<checkpoint>` into main as ONE owner-authored commit.
Proposed commit message: [subject + body, for the owner to use, edit, or discard]
```

**(c) `gauntlet-templates.md` — new §9, *Landing inspection and owner squash merge*:**

> **Inspection — the Orchestrator, read-only.** The receipt gate closes a checkpoint in program
> state; landing is a separate decision and needs its own look at the tree:
>
> ```text
> git worktree list
> git branch -vv --list 'gauntlet/*'
> git log --oneline --graph main..<evidence_tip_sha>
> git diff --stat main...<evidence_tip_sha>
> git diff --name-only <final_candidate_sha>..<evidence_tip_sha>   # AMD-G1: evidence paths only
> ```
>
> Reconcile this against the Landing Report. A discrepancy between what the packet claims the
> checkpoint left behind and what the repository actually holds is a receipt-gate failure, not a
> footnote.
>
> **The owner operation.** Landing is a squash merge run locally by Yarden, and by no agent:
>
> ```text
> git checkout main
> git merge --squash gauntlet/<checkpoint>
> git status            # review the staged tree — nothing has been committed
> git diff --cached     # this is exactly what would enter main
> git commit            # authored by hand, after his own review
> ```
>
> `git merge --squash` applies the merged tree to the index and working tree and **deliberately does
> not create a commit**. That is the point: it produces a reviewable staged state and stops, so the
> commit that lands on `main` is written by the owner rather than generated by the merge. It also
> collapses the candidate, the component verdicts, and the evidence tip into **one** commit, which
> discharges the D-CP0-6 ordering anomaly instead of replaying it onto `main`.
>
> Nothing here authorizes an agent to run any of it. A `PASS` packet is evidence for the decision; it
> is not the decision, and a checkpoint may stay closed-and-unlanded indefinitely.

**(d) `AGENTS.md` — add under *Git and publication authority*:**

> **Landing is owner-only and squash-only.** A reviewed checkpoint reaches `main` as one
> owner-authored commit produced by a local `git merge --squash` that Yarden runs and commits by
> hand. Agents never merge, squash, rebase, fast-forward, or cherry-pick into `main`, and never
> offer to. An agent may prepare the Landing Report and a proposed commit message; it may not
> execute the landing.

**Check.** The gate reconciles the Landing Report against the live repository. The landing itself is
outside agent authority by construction, so it needs no agent-side check.

## Sequencing

1. **AMD-G2 first.** It is the cheapest, and D-CP0-1's remedy cannot be adopted before it — the
   current text makes the required declaration impossible to write honestly.
2. **AMD-G1 next.** It is the only structurally unsatisfiable defect, and it must be settled before
   CP-1 produces a candidate under the old wording.
3. **AMD-G3 last of the three**, because its landing rule depends on AMD-G1's two-SHA vocabulary.
4. Then D-CP0-2 through D-CP0-5, D-CP0-7, and D-CP0-9 through D-CP0-11, which are underspecified
   rather than contradictory and can be drafted together once the shape above is settled.
5. Ratify as **capstone v6.6 + a new exact anchor**, then close this ledger, then brief CP-1.

## Still open

- Whether the packet's 3–5 defense questions are answerable by the owner — untested until Yarden
  reads them.
- Whether the five mandatory critic surfaces were correctly judged out of scope at CP-0. The packet
  never declares an in-scope/out-of-scope determination for them, and §8 receipt item 3 asks the
  Orchestrator to confirm their presence with nothing to check against. Item 4's Berlin DST work is
  arguably surface 1 (temporal normalization) in scope; it was covered substantively by both critics
  but never labelled as a mandatory surface. **Adjudicate this before CP-1, where all three of
  surfaces 1–3 are unambiguously in scope.**
- The orphaned worktree at `.../23cc0d4e-.../scratchpad/gauntlet/builder-instrument` awaits owner
  removal. The Lead correctly declined to remove a worktree it did not create. Under AMD-G3 this
  would have appeared in a Landing Report rather than surfacing through an unrequired topology sweep.
- ~~**CP-0's landing decision itself.**~~ **RESOLVED 2026-08-05 — DISCARD.** Attempt 1 was reviewed,
  closed, and never landed. It was archived at `archive/cp-0-attempt-1` and its branch retired, per
  DEC-3: attempt 1 was built under the defective contract, so it is superseded by a clean-room re-run
  rather than merged. It remains the worked example of the gap D-CP0-12 names — a `PASS` artifact
  that sat with no contractual route to `main` — and the first application of AMD-G13's
  tag-before-delete rule, performed manually before that rule existed.
- ~~**Whether the amendment should be one capstone v6.6 or two releases.**~~ **RESOLVED 2026-08-05 —
  DEC-2: one bundled v6.6 package**, ratified in full before the re-run. The original reasoning is
  kept below for the record. AMD-G2 is independent and
  could ship immediately; AMD-G1 and AMD-G3 are coupled through the two-SHA vocabulary. Shipping G2
  alone would unblock honest packets sooner at the cost of a second ratification cycle. Owner call.
