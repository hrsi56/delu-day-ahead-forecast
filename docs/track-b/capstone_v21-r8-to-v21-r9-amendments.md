# Capstone v21-r8 → v21-r9 and PUBLISH_RULES 1.2 → 1.3 — CP-22: v4 revised (ratified)

**Ratified by the Owner on 2026-10-01. CP-22's execution was authorized the same day.** The text
was drafted under the Owner's task-scoped suspension and the Owner's approval of decisions
D1–D8. The Owner then wrote:

> נותן לך את: 1. אישור הטקסט. 2. אישור ביצוע CP-22. 3. הוראה ואישור לעשות commit ו-push לכל המסמכים בעצמך. נעשה הכל מקומית

That is:

1. the text is ratified;
2. CP-22's execution is authorized;
3. the agent is instructed to commit and push all the documents itself.

Everything runs locally.

## Decision and authority

On 2026-10-01 the Owner wrote (the request, verbatim):

> לפני שאנחנו מתחילים לבחון את הddn אני רוצה שנבחן שוב את V4 וננסה לשפר את האלגוריתם שלה.
> השיפור שבה לעומת V3 לא גדול ואני חושב שאולי מסתתר שם משהו בעייתי. ההצעה שלי היא כזו: תפרק
> את ההבדלים בין V4 ו V3 לגורמים. תבחן כל אחד מהם בנפרד, תנסה לשחק עם הפרמטרים שלו ולמצוא שיפור.
> תרכיב מחדש בצורה מיטבית.

In English: before DDNN, re-examine v4 and try to improve its algorithm. Decompose v4 − v3 into
its factors, examine each one, tune its parameters, and reassemble the best combination.

The Orchestrator advised against tuning on the evaluation folds. All five folds are both the
selection ground and the test, so that gain would shrink on new data. It recommended instead
pre-registered policies whose parameters are fixed in advance or chosen inside each origin's
training window, judged by a rule fixed in advance. The Owner then decided:

> לא. בוא נגדיר שהגרסא החדשה שתצא תדרוס את V4. הפיצול יימחק בכל מקרה. אין בו הגיון.

That is: the new version replaces v4, and the block split is removed in every outcome, because
there is no logic in it. The Owner also asked whether v3's calibration should be examined in the
same version, and proposed handing the work directly to an Engineering Lead with the return
coming back to the Orchestrator. On the decisions and the authority, the Owner wrote:

> ההחלטות D1–D8: מאשר כפי שהמלצת
>
> אם גם R וגם M גרועות בבירור: עוצרים וחוזרים אליך
>
> ההשעיה תכסה כל מה שצריך.
>
> בנוסף. לדעתי 28 יום זה הרבה וזה רדג׳ידי. משברים מתחילים מהר. צריך איזשהי למידה דינאמית יותר

In English: D1–D8 approved as recommended. If both R and M are decisively worse, stop and return
to the Owner. The suspension covers everything needed. And 28 days is long and rigid; crises
start fast, so more dynamic learning is needed.

The Owner then asked why a single day should not carry its own weight: a one-day spike or a large
error is critical information. The Orchestrator explained that a single day already acts in
three ways: through the price lags and normalization, through the 168-hour scale, and through
ACI's next-day widening. It also explained why a buffer is still needed: 24 hours cannot
estimate the tails, and one-off errors would cause over-correction. It then offered an
attribution arm with a 3-day half-life to measure the trade-off. The Owner replied "תוסיף" (add
it), then refined the request:

> אני לא רוצה שהזרוע תבחר ותחליף את ה7 ימים. אני רוצה לבדוק האם נכון להוסיף משקל מהיר יותר
> בנוסף, לזיהוי שינויים חדים

That is: not a 3-day replacement of the 7-day memory, but a test of whether a faster weight
should be added on top of it, to identify sharp changes. The 3-day arm was therefore replaced by
W+DLF:

- the 7-day kernel, plus a fast one-day-half-life kernel carrying one third of the weight;
- a fixed-sequence add-on decision, `cp22-fast-component`, that runs only after W+DL is adopted;
- shock-day diagnostics.

**How the authority is read.** The Owner's words act as a task-scoped Lockdown suspension. It
covers:

- `capstone_v21.md` revision v21-r9: a header, one §10 row and new §20;
- `docs/PUBLISH_RULES.md` revision 1.3: A10;
- this record;
- directly necessary consistency edits to the programme handoff and `progress.md`.

Beyond the suspension, the Owner granted two things on 2026-10-01:

- CP-22's execution, under §20.11;
- a task-scoped instruction to commit and push these documents. That is not a standing
  exception.

The grant does not cover publication or an `AGENTS.md` change.

The suspension ends at this task's terminal return.

## Identities

| Item | Identity |
|---|---|
| Incoming `main` = `origin/main` | `ddb9379` (PRES-3 closed) |
| Previous research anchor | v21-r8 at `c352436:capstone_v21.md`, SHA-256 `81d6127197cabf344f56c2cf25ef5fc8f9fdb2860e249c294177471d3130c182` |
| Previous publication anchor | PUBLISH_RULES 1.2 at `c352436:docs/PUBLISH_RULES.md`, SHA-256 `a43ac02021b7de468e02db30b61ec73f86cdafa69df845cf084ab196528bb15b` |
| CP-21's governing bytes | v21-r6 §17 at `evidence/cp-21`; CP-22 neither reopens nor rescores CP-21 |
| Ratified identities | `capstone_v21.md` v21-r9 and PUBLISH_RULES 1.3, by SHA-256 in `progress.md` and the issued brief, which cite this record's hash |

**What v21-r9 adds:** a header, one CP-22 row in §10's table and new §20. No existing line is
deleted or altered; `git diff` against v21-r8 shows only additions. **What 1.3 adds:** the
revision line, a 1.3 authority paragraph, §4's A10 paragraph, the A10 entry, §16.3 and a §17
line. The only line replaced is the revision line.

## Decisions (Owner, 2026-10-01: approved as recommended)

| # | Question | Outcome |
|---|---|---|
| D1 | Shape | One checkpoint, CP-22. Two eligible policies in a fixed sequence: R (one pooled normalized member averaged over G1–G4), then M (the split removed only). Attribution arms are never eligible. |
| D2 | Replacement rule | `cp22-replacement`: non-inferiority against v4 on both scores and per fold, all six §8 diagnostics, and a complete valid evaluation. If both fail, stop and return to the Owner. |
| D3 | Representation | v4 keeps its number, with a dated revision; the three-block construction becomes a superseded revision (PUBLISH_RULES 1.3, A10). |
| D4 | Ceilings | §20.8: 6,000 main and 9,000 total LightGBM fits, 16,000 policy-days (recomputed for W+DLF), 30 machine-hours, about 24 active hours (hard 32) |
| D5 | Publication | PRES-4 after LAND. If there is no replacement, the Owner decides first. |
| D6 | Learned weight | Excluded; it stays in programme 4.8 |
| D7 | Interval calibration | In CP-22, as a separate decision on the winner (`cp22-dynamic-layer`). Its form follows the Owner's dynamics decision: recency weights with a 7-day half-life inside the 28-day buffer, plus adaptive coverage (ACI) with γ = 0.10 per day. The Owner added a fast component as an add-on, never a replacement for the 7-day memory: W+DLF, under `cp22-fast-component`, with shock-day diagnostics. |
| D8 | LEAR's internals | Diagnostics only now; any change goes to a later, separate checkpoint |

**Parameters fixed by mechanism.** They are not tuned on outcomes, and the Owner may change them
at ratification:

- **DL's half-life of 7 days** matches the 168-hour scale `s_t`.
- **ACI's γ = 0.10 per day** gives an effective memory of about ten days, with `α_t` clipped to
  `[α/5, min(2α, 0.9)]`.

## The evidence that motivated the design

All of it is committed CP-21 evidence (`evidence/cp-21`) and `development_post_selection`:

- **The member, not the split, carries v4's gain.** Alone, the tree arms score 0.5769–0.5835
  S_MAE, against v3's 0.5658; blended, v4 scores 0.5357. L-R − L-P shows no demonstrated joint
  preference.
- **The raw-target half of v4's member drives the peak degradation.** Peak MAE is 66.3 (L-P) and
  70.1 (L-R), against 52.2 (L-N), 50.1 (v4) and 47.5 (v3).
- **A normalized pooled member was never tested,** because §17.2 excluded it.
- **The daily capacity selection is mostly noise.** The smallest configuration was chosen on
  24–44% of origins, the largest on 20–33%, and the median winner margin is 1.5%.
- **v3 and v4 under-cover** in four of five folds: 0.932–0.940, against the nominal 0.95.

## Disclosures

- **Known results.** The Owner and the agents know CP-15's, CP-20's and CP-21's results on these
  folds. R, M and DL were chosen from mechanisms visible in that evidence, before any CP-22
  scoring.
- **Selection.** CP-22 is one more decision on the same five folds. Its results stay
  `development_post_selection`, and 4.7T's manifest carries every revision.
- **What CP-22 cannot establish:**
  - performance on new data;
  - which individual weather feature helps;
  - economic value;
  - daily operation.

## Files touched by this task

| File | Change | Authority |
|---|---|---|
| `capstone_v21.md` | v21-r9: header, a §10 row and new §20; additions only | Suspension; commit and push instructed |
| `docs/PUBLISH_RULES.md` | 1.3: A10 (revising a generation in place) | Suspension; commit and push instructed |
| `docs/track-b/capstone_v21-r8-to-v21-r9-amendments.md` | This record, new | Suspension; commit and push instructed |
| `docs/track-b/cp-22-publication-plan-2026-10-01.md` | The publication plan, new; not locked | Orchestrator planning; commit and push instructed |
| `docs/track-b/v3-plan-handoff-2026-09-22.md` | A dated CP-22 note; no historical sentence removed | Suspension (consistency); commit and push instructed |
| `progress.md` | CP-22's ratified state and the Owner's decisions | Orchestrator regeneration contract; commit and push instructed |

## Documentation validation

This task checked:

- that the anchor's diff against v21-r8 contains only additions;
- that PUBLISH_RULES' diff replaces only its revision line;
- that every relative link added here resolves.

This is a documentation ratification, not an implementation PASS or a research result.
