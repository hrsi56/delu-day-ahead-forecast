# Capstone v21-r19 → v21-r20 — publishing and going live before 4.7T

**Owner authority, 2026-11-05.** The Owner's decision 28 is recorded in
`docs/track-b/owner-decisions-2026-11-05.md`, SHA-256 `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`.
- **What he decided.**
  - CP-18's activation and a publication come before 4.7T, not after it.
  - All the data is downloaded through the present, and the live product trains on it.
  - A1 stays frozen and untouched, and 4.7T tests it exactly as registered.
- **His words with it:** "זה שאנחנו רוצים לבדוק את המצב בעוד חודש לא אומר שאנחנו לא מפרסמים עד אז"
  ("Wanting to check the result in a month does not mean we don't publish until then").
- **The grant.** Decision 28 changes decision 25's order. Decision 25 covers "the Lockdown suspensions each named
  step needs", and decision 27 lets the Orchestrator run these steps alone.

**The scope of the suspension.** It covers four things:
- `capstone_v21.md`;
- this amendment record;
- the decision record and the directly necessary consistency edits to `progress.md`;
- the commit and push of these files to `main`.

It ends at this task's terminal return. It does not authorize:
- any other governance file, `AGENTS.md`, `docs/PUBLISH_RULES.md` and the exposure ledger included;
- a change to any code, test, frozen record, verdict or freeze;
- publication, or opening any checkpoint. CP-18c and PRES-5 each need their issued brief.

**The base:** r19 at `5954d8c3:capstone_v21.md`, SHA-256
`acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e`. When this revision was applied, `main` was
`5954d8c3`, CP-18b's closure, on top of its landing `ff382b2b`.

| Scope | r19 | r20 |
|---|---|---|
| The order | CP-18's preparation → 4.7T → CP-18's activation → one complete publication (decision 25) | CP-18c, the activation, and PRES-5, the publication, now → 4.7T at its date → the publication of its result (§24.14 item 1) |
| The boundary guard | retired for the live pipeline after 4.7T (§24.2); the runner runs on development data only (§24.13) | retired for the live pipeline at CP-18c. The live pipeline downloads all the data through the present and trains on it. Every research path keeps the guard (item 2) |
| The exposure ledger | `docs/track-b/exposure-ledger.md` | that file stays byte for byte, because CP-26's harness pins it. Later entries go in `docs/track-b/exposure-ledger-continued.md`, seeded by CP-18c with decision 28's entry (item 2) |
| The audit | §24.2's standard | unchanged for everything 4.7T tests. The live product's daily fits are the frozen policy's operation, recorded in the continuation (item 3) |
| The live start | carried from 4.7T's last window day to the first live day (§24.12) | seeded at the freeze origin, 2026-09-06, and carried to the first live day. The live product's window-day forecasts are its own, never 4.7T's (item 4) |
| What the product shows | — | the live record under A7 and A9, with A1 "final candidate · pending 4.7T" and prospective scores labelled "prospective evaluation in progress". Development displays stay through 2026-09-06 (item 5) |
| Publication | "No publication" (§24.10) | PRES-5: A1 in the comparison on v5's data, CP-26, CP-28, the freeze with 4.7T's registered terms, and the live product, under PUBLISH_RULES 1.5 (item 6) |
| The runner | `macos-26`, the local fallback on the Owner's Mac | the local fallback until the Owner enters the three repository secrets, then the `macos-26` schedule (item 7) |
| A1's freeze, and 4.7T's window, terms, machine and calendar | §24.12, §24.13 | unchanged |

**The review.** No independent plan critic ran for this revision. `AGENTS.md` does not require one, and the Owner asked for the
publication now. The text adds no term to 4.7T and changes none. 4.7T's audit, with its independent reviewer, reads §24.14
before 4.7T opens (§24.9).

**The CI.** The history-free CI (`CI=true`, Python 3.12, Git's global configuration hidden) on this revision's commit is
recorded in `progress.md`'s Session Log, beside the push.
