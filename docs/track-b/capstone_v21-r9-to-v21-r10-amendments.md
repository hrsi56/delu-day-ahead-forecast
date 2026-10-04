# Capstone v21-r9 → v21-r10 — CP-23: the DDNN route, CP-22's outcome and the programme order (ratified)

**Ratified by the Owner on 2026-10-04.** The text was drafted under the Owner's task-scoped
suspension. That grant also covers its commit and push. CP-23's execution is **not** granted by
this revision; it needs the Owner's explicit grant with the issued brief (§21.11).

## Decision and authority

After CP-22's receipt, on 2026-10-04, the Owner wrote, in order (verbatim):

> v4 נשאר כפי שהוא

> החלטות לגבי ddn שאתה כבר יכול לעגן
> * v5 = v4 ועוד רכיב DDNN
> * יתחרה כמובן מול V4.
> * צריך סעיף עוגן חדש, v21-r10, תחת השעיית Lockdown. הסעיף יתעד גם את תוצאת CP-22 מול §20.1. מאושר באופן מלא, כולל השעיה וכולל קומיט פוש מה שאתה צריך.

In English:

- v4 stays as it is.
- Decisions on DDNN to anchor now: v5 = v4 plus a DDNN component, competing against v4.
- A new anchor section, v21-r10, under a Lockdown suspension, which also records CP-22's outcome
  against §20.1. Fully approved, including the suspension and the commit and push.

The Owner then set the programme order and wrote "בצע" (execute):

> הסדר המאושר: יישם את פריטים 2, 1, 5, 3, 4 ו-8, בסדר הבנייה של התוכנית. DDNN, דחה את 6 ו-7
> לפרסום הבא אבל תייק תזכורת שתחייב אותנו לדון בהם בזמן הנכון. אחר כך קבלת נתונים ו-4.4V, אחר כך
> 4.8 עם ה-meta-learner, ובסוף 4.7T.

In the same message, on the data research: "תייק אחרי DDNN ותגדיר מחקר מקיף על הוספת דאטה. מחירי
אנרגיה, ריביות, מדד פחד בבורסה המקומית כל מה שאפשר וחוקי לשלוף וללמוד ממנו". The research is to
include later vintages or other horizons for inputs published after the origin, and other
available, reliable forecast APIs. On 4.8, the Owner wrote: "כבר מתוייק ומוגדר ב4.8 לבחון רשת
ב-NumPy לצורך meta-learner ? אם לא תייק".

**How the grant is read.**

- **Owner decisions.** "v4 stays as it is", D1–D3 and the programme order are the Owner's.
- **Delegated decisions.** "מאושר באופן מלא … מה שאתה צריך" delegates the remaining design
  choices. They are D4–D10 in §21.12, each marked "Orchestrator, under the Owner's grant", so that
  the Owner can see and reverse any of them before CP-23's brief is issued.

## Identities

| Item | Identity |
|---|---|
| Incoming `main` = `origin/main` | `42e4ceb` (the automation tools, on CP-22's closure `6483324`) |
| Previous research anchor | v21-r9 at `940eb98:capstone_v21.md`, SHA-256 `5fc9c6862aa9f623af29db295e79456ecd94c60e213f8f286cdca97153e09175` |
| CP-22's governing bytes | v21-r9 §20 at `evidence/cp-22`; v21-r10 neither reopens nor rescores CP-22 |
| Ratified identity | `capstone_v21.md` v21-r10, by SHA-256 in `progress.md`. CP-23's issued brief will also record it |
| Publication anchor | PUBLISH_RULES 1.3, unchanged |

**What v21-r10 adds:**

- a header;
- one CP-23 row in §10's table;
- §20.13, CP-22's outcome;
- §21, CP-23;
- §22, the programme order.

No existing line is deleted or altered, and `git diff` against v21-r9 shows only additions.

## Decisions

| # | Decision | Set by | Outcome |
|---|---|---|---|
| D1 | The candidate | Owner | v5 = v4 plus a DDNN member |
| D2 | The opponent | Owner | The three-block v4 on identical rows, with v3, A1 and B2 as references |
| D3 | This anchor | Owner | v21-r10, recording CP-22's outcome against §20.1 (§20.13) |
| D4 | The member weight | Orchestrator, under the grant | One third, as CP-21 added LightGBM: `(2/3)·c_v4 + (1/3)·D`. Fixed, never tuned |
| D5 | Shape | Orchestrator, under the grant | One checkpoint, 4.6L → 4.6R → 4.6C with gates |
| D6 | Intervals | Orchestrator, under the grant | v5 and v3+D use the H layer on their own errors; DDNN alone uses its own JSU quantiles |
| D7 | The rule | Orchestrator, under the grant | `cp23-adoption`, CP-21's four conditions, against v4 |
| D8 | Ceilings | Orchestrator, under the grant | §21.8: 4,000 main and 6,000 total DDNN fits, 60 machine-hours, about 30 active hours (hard 40) |
| D9 | The reference tests | Orchestrator, under the grant | PyTorch CPU, pinned, test-only, recorded, never skipped silently |
| D10 | Publication | Orchestrator, under the grant | The next publication after LAND if v5 is adopted; the Owner sets the encoding first |
| D11 | The programme order | Owner | §22 |

**Why these choices.**

- **D4: a one-third weight.** It repeats CP-21's recipe, so v5 adds one member exactly as v4 did,
  and it leaves weight learning to 4.8. With it, LEAR carries 4/9 of v5's central forecast,
  LightGBM 2/9 and DDNN 1/3.
- **D5: one checkpoint.** The 4.6L and 4.6R gates are short and stop the route cheaply. A single
  Integration review then covers the whole route.
- **D6: the intervals.** DDNN alone tests the distributional head. v5 keeps the interval layer
  that v3 and v4 use, so v5 − v4 isolates the member.
- **D8: the ceilings.** They were sized for one configuration per fold and daily refits of at
  most four seeds at about 640 origins. 4.6R measures the cost and refuses a run its projection
  does not fit.

## Disclosures

- **Known results.** The Owner and the agents know CP-15's, CP-20's, CP-21's and CP-22's results
  on these folds. The Orchestrator also computed a hindsight bound for per-block LightGBM weights
  on 2026-10-04; it is disclosed in §22.
- **Selection.** CP-23 is one more decision on the same five folds. Its results stay
  `development_post_selection`, and 4.7T's manifest carries v3, v4 and v5 if adopted.
- **What CP-23 cannot establish:**
  - performance on new data;
  - economic value;
  - daily operation;
  - in-browser retraining, which §16 and §19 decide.

## Files touched by this task

| File | Change | Authority |
|---|---|---|
| `capstone_v21.md` | v21-r10: header, a §10 row, §20.13, §21 and §22; additions only | Suspension; commit and push instructed |
| `docs/track-b/capstone_v21-r9-to-v21-r10-amendments.md` | This record, new | Suspension; commit and push instructed |
| `docs/track-b/v3-plan-handoff-2026-09-22.md` | A dated v21-r10 note; no historical sentence removed | Suspension (consistency); commit and push instructed |
| `progress.md` | The ratified state, the order and the filed notes | Orchestrator regeneration contract; commit and push instructed |

## Documentation validation

This task checked:

- that the anchor's diff against v21-r9 contains only additions;
- that §21.10, the CP-23 bar, extracts cleanly with `scripts/bar.py` at the ratification commit;
- that every relative link added here resolves.

This is a documentation ratification, not an implementation PASS or a research result.
