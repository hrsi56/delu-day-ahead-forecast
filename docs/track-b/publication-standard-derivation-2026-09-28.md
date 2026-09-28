# How Publication Standard v1 was derived — record, 2026-09-28

## The question

The Orchestrator's PRES-1 release review of 2026-09-28 listed fixes R1–R8 and blockers B1–B4. The
Owner asked whether those fixes were structural, reaching the root of the problems, or point
patches. He called this the one chance to set the publication standard before the next model
generations are published on it, and suggested discussing it with an independent agent.

## Method

The Orchestrator consulted an **independent advisor**: a read-only subagent that had written nothing
in PRES-1. The discussion ran in three rounds.

1. **Round 1, cold.**
   - **Material:** only the rendered candidate page (`af0abb0`, 29 screens with disclosures closed,
     at 1,440 × 900 and 390 × 844), the README and the production code.
   - **Withheld:** the plan, the review history and the Orchestrator's view.
   - **Independence:** the Orchestrator wrote down its own position before reading the report.
2. **Round 2, challenge.** The advisor took on the plan (revision 3), the brief, the review history
   (both reader-task rounds, the D1 editorial review, both independent checks, the final editorial
   audit), the release review and the Orchestrator's position.
3. **Round 3, red team** of the draft standard.

The Orchestrator verified each factual claim against the repository before relying on it.

## What both sides found

**The release review was mostly patches.**

- R1–R4 and R6–R8 fixed this page's symptoms.
- R5 was structural but narrow.
- The review also claimed to leave the approved plan untouched, while R1 and R2 in fact amended
  §8.1 and §8.2 without saying so.

**Three root causes, all descending from a one-page plan hardened by patches from each review:**

1. **No floors.** The plan said at length what must not be said, and never what must be said, or
   where.
2. **No single source for the story's state.** Names, statuses and "current" were typed in many
   places.
3. **A review ratchet.** Each round reviewed against the previous bar and could only add
   constraints. The plan's reader-hostile clauses stayed frozen, and nothing let a reviewer change
   them.

**The decisive evidence.**

- A number was on the first screen of the first D1 specimen.
- After the D1 editorial review, the headline was a sentence without numbers on screen 2, and the
  numbers were on screen 5.
- The reader gate, whose tasks asked only whether a reader could locate an answer, passed every
  round.
- Both independent checks failed on real-device requirements that no agent can meet.

## Plan clauses behind the symptoms

| Plan revision 3 | Symptom |
|---|---|
| §8.1: at most one summary value, no new percentage | No result in the opening |
| §7.2: an information order, not a first-screen demand | No placement requirement |
| §8.2: "the plan's diagnostic limits" | The strongest result read as a bare "limit 0.59203" |
| Invariant 9: the endpoint printed in full | A 21-digit number, four times; readers took it for a bug |
| Invariant 5, with the README's CP-3 sections | A README led by v1 |
| §8.3: "adopted as the current research model" | Status written into prose, false the day v4 lands |
| §11.3: real Safari and iPhone | The FAIL item common to both independent checks |
| §11.4: reader tasks that only test locating | A reader gate that could not fail on prominence |
| §10.3: the 23-run manifest | A test hard-coded to 23 runs |
| §15: "the same template" | No defined path for v4 or for a rejected branch |

## Facts the Orchestrator verified

- **The CP-20 report** that the page links as "Full report" still reads "pending fresh
  exact-candidate Integration review".
- **The page** is 1,519,837 bytes against its 2,000,000-byte budget.
- **No script writes `mlflow_index.json`.**
- **N = 8 policies** were tested against capstone v21 §8 criteria 1–2: A1–A5, V2-H and its control
  V2-P, and HG. Only HG met them.
- **The targets preceded the results.**
  - Pre-registration commit `bb5e678`, 2026-09-16 00:17, is reachable from `evidence/cp-15`.
  - CP-15's results were committed at 03:15.
  - The §8 text is identical to the anchor preserved from attempt 1.
- **The placements are feasible.** Measured in Chrome and WebKit:
  - the research status card ends at y = 721 on desktop and y = 604 on a phone;
  - moving the headline there and dropping the separate summary puts the result on the first
    screen of both;
  - moving planned work after the chapters brings the comparison's finding sentence within 2
    desktop screens and 3 phone screens.

## Positions and how they were resolved

| Topic | Resolution |
|---|---|
| The first cause | Floors first for this audience (the Orchestrator's position; the advisor agreed) |
| The absolute anchor | Per-period ranges. A single EUR/MWh mean is dominated by the 2022 crisis and reverses a ranking. The Orchestrator conceded. |
| The headline | One sentence plus a badge. Seven elements was too long; the Orchestrator conceded. |
| The endpoint | +0.0000039 on the reading path, with the full value in the table. This keeps W3's purpose; the Orchestrator conceded. |
| Sequencing | Complete PRES-1 against the standard's core now, and build the chapter grammar before CP-21 publishes. The Orchestrator conceded that a full refactor now would change little that a reader sees. |
| The primary action | "Try the v1 demo" stays, as the Owner approved. The advisor withdrew its objection. |
| "8 candidates" | "8 policies". V2-P is a control. |

## Round 3 blocking items, all applied to the draft

1. Landing, pushing and redeploying stay with the Owner or his explicit instruction (`AGENTS.md`).
2. Comparators come from the research anchors and standing decisions. The standard governs only
   presentation.
3. The plan's invariants are carried over explicitly.
4. The percentage and precision rules exempt v1's protected statements and nominal levels.
5. The date of the targets comes with a provenance record.
6. The headline is one sentence, with its terms defined directly below it.
7. The orientation answers have measurable placements.
8. "Begins" is defined as the finding sentence being fully visible; the phone headline budget
   tightened to the first screen.
9. Clauses in force are listed per publication.
10. No-placeholder is enforced at pre-push. The lock is described honestly as detection until it
    is added to `AGENTS.md`.
11. The Owner keeps visual tokens and the contribution statement. Only the Owner may loosen a
    budget.

## Ratification, 2026-09-28

**Approved:**

- D1: the standard, with its core protected by detection;
- D2: the plan amendments;
- D3: the date-boundary reading;
- D5: execution and authority;
- D6: the template suspension, extended to the publication packet.

**Not taken up:**

- D7, the human cold read, stays an option.
- D4 was withdrawn: the repository root is the Owner's personal decision.

**The Owner widened the scope.** The current state is to be brought to the standard "including
everything", by a new Lead session. So the chapter grammar and the lint are no longer deferred to a
later task. The brief is `docs/track-b/pres-1-conformance-brief-2026-09-28.md`.

## Local working records

These are not committed:

- `.local/tmp/pub-standard/orchestrator-position-round0.md`;
- `advisor-round1.md` and `advisor-round2.md`;
- the reader pack and the measurement script.
