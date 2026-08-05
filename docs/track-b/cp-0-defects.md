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
| 2026-08-05 | CP-0 Return Packet (`PASS`, final candidate `8f371e5` on `gauntlet/cp-0`) and Orchestrator receipt-gate verification of it | D-CP0-6 … D-CP0-11 |

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

---

# Findings from the CP-0 run — 2026-08-05

CP-0 returned **`PASS`**, final candidate `8f371e5` on `gauntlet/cp-0`, 2727 s of a 7200 s ceiling.
The receipt gate accepted it; the verification behind that acceptance is recorded at the end of this
section. Six further defects follow. **None of them invalidates the CP-0 `PASS`**, and none touches a
capstone bar.

## D-CP0-6 — Integration cannot review the commit that records its own verdict

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

**Ownership.** `capstone_V6_5.md` §12 (item 7 wording) and `engineering-role.md` §§ *Gauntlet
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

**Statement.** `engineering-role.md:9` forbids the Lead from reading `progress.md` or
`orchestrator-role.md` "during Track B execution." The Return Packet is written during execution —
terminal return is its end, not a phase after it. A Lead that discovers something needing honest
disclosure in the packet must read program state to describe it accurately, and thereby breaches the
rule. **The contract makes candour a violation.**

**Evidence.** The Lead read only the brief, `AGENTS.md`, `engineering-role.md`, `capstone_V6_5.md`
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

**Statement.** The contract requires a **verbatim excerpt** verified present in the cited plan at the
candidate SHA. It says nothing about line numbers. Both critics volunteered line ranges anyway, and
one was wrong.

**Evidence.** `**CP-0**` sits at line 459 of `capstone_V6_5.md` (verified independently). The
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
  directions: CP-1 carries 16 checklist items and three mandatory surfaces, so it is not a linear
  scale-up of one piece.

## Receipt-gate verification behind the accepted `PASS`

Checked against the repository, not against the packet's claims: `main` clean at `d7bdd5f`;
`gauntlet/cp-0` linear at `d7bdd5f → 7526310 → 63ebfab → 8f371e5`; both cited SHAs reachable on that
branch; `7526310` an ancestor of `8f371e5`; both verdict files present in the candidate tree; the
candidate diff confined to `pyproject.toml`, `scripts/pit_capture.py`, `src/pit_capture/**`,
`tests/**`, and `docs/track-b/evidence/cp-0/**` with no later-checkpoint scope; all seven checklist
items mapped to reproducible evidence with no open item hidden behind `PASS`.

**The `PASS` stands.** D-CP0-6's circularity does not undermine it here because the delta between the
reviewed SHA and the branch tip is provably a single evidence file — but that is a property of this
run, not a guarantee of the contract, which is the defect.

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
  removal. The Lead correctly declined to remove a worktree it did not create.
