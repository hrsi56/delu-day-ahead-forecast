# Capstone v21-r7 → v21-r8 and PUBLISH_RULES 1.1 → 1.2 — the final-product Space (Owner-authorized)

**Authorized by the Owner on 2026-09-30. A documentation amendment only: it opens no checkpoint,
designates no model, runs nothing and publishes nothing.**

## Decision and authority

On 2026-09-30 the Owner wrote (the request, verbatim):

> עכשיו אני נותן לך את המשימה בכללותה.
>
> הספייס נראה כרגע מעפן ולא אינפורמטיבי. חייבים לשפר אותו משמעותית כשיש מוצר חי. תסקור אותו
> ואת הכללים כרגע ותנסה לבנות תוכנית כיצד אנחנו עושים ממנו באמת כלי שימושי ואינפורמטיבי
> שתעוגן Split by authority ותמומש ברגע שיהיה לנו מודל סופי.
>
> שחזור ודמו יתאמן ויעודכן יומית ויציג מה המחיר היום ובכמה אחוזים הוא צדק ומה המחיר מחר ובכמה
> המודל בטוח בו. כפתור "אמן בעצמך"

The request continued with the panels, the analyses and the rules the Space must follow; the plan
lists them item by item. On authority and scope, the Owner wrote:

> לצורך המשימה הזו במלואה יש לך אישור לבצע כל מה שאתה צריך קומיט מרג׳ פוש הוספת קבצים ועריכה.
>
> שים לב, המשימה היא לא משימת ביצוע של פרסום אלא משימה לבניית תוכנית ביצוע לפתרון הנושא […]
> נכון לעכשיו אנחנו עוד לפני press-03 אז אל תסתכל בכלל מה קיים כרגע בhf או באתר וכו. רק בחוזים
> ובכללים והעוגנים. הקיים כרגע לא מעודכן.

In English:

- **The request.** The Space looks poor and uninformative, and must improve substantially once
  there is a live product. Build a plan, anchored split by authority, to make it a genuinely
  useful and informative tool, implemented once there is a final model. It should train and
  update daily; show today's price and how accurate it was in percent, and tomorrow's price and
  how sure the model is; and offer a "Train it yourself" button.
- **The authority.** For this task in full: commits, merges, pushes, new files and edits.
- **The scope.** A plan to be executed as part of the final product's publication, not a
  publication. The current Space and site were not to be inspected, since they predate PRES-3.

**How the authority is read.**

- **The Lockdown.** The grant acts as a task-scoped Lockdown suspension covering:
  - `capstone_v21.md` revision v21-r8 (a header and §19);
  - `docs/PUBLISH_RULES.md` revision 1.2;
  - this record and the plan;
  - directly necessary consistency edits to the programme handoff and `progress.md`.
- **Git.** It covers the commit, push, pull request and squash merge of these documents.
- **What it does not cover:** `AGENTS.md`, deployment, schedules, unattended publication and
  external replies.
- **When it ends:** it is spent at this task's terminal return.

## Identities

| Item | Identity |
|---|---|
| Incoming `main` = `origin/main` | `6f4575baa88b5c99e75626ea11e1ee1b7a2542be` (the CP-21 landing record) |
| Previous research authority | v21-r7 at `c9dc364:capstone_v21.md`, SHA-256 `e6a4e301d5db080c6427f925f51e2cf69367c42225b292c78050117003aa7b0c` |
| Revised research anchor | `capstone_v21.md` v21-r8, SHA-256 `81d6127197cabf344f56c2cf25ef5fc8f9fdb2860e249c294177471d3130c182` |
| Previous publication anchor | PUBLISH_RULES 1.1 at `6f4575b:docs/PUBLISH_RULES.md`, SHA-256 `91eea445434718a163f03bcfd82e1db275a9d98311e76eb6cd1365f3707584f3` |
| Revised publication anchor | PUBLISH_RULES 1.2, SHA-256 `a43ac02021b7de468e02db30b61ec73f86cdafa69df845cf084ab196528bb15b` |
| Plan | `docs/track-b/final-product-space-plan-2026-09-30.md`, SHA-256 `e2160b827fcb569f564ec8eb5ecdfa1e5aa2aefdc14c6534708f9adf88b69418` |
| This record | Its SHA-256 is recorded in `progress.md` |

**What changed:**

- **v21-r8** adds a header and §19; `git diff` against v21-r7 shows 139 added lines and none
  removed.
- **PUBLISH_RULES 1.2** changes one existing line, the revision header, and adds:
  - the 1.2 authority note;
  - a §1.3 applicability entry;
  - §7.3 (A9);
  - a §13 acceptance row;
  - one sentence in §15's preamble;
  - A9's justification;
  - §16.2;
  - the §17 change record.

## The split by authority

| Authority | What it holds | Where |
|---|---|---|
| Owner | The in-browser retraining requirement (decided in the request); final designation; the percentage tolerance τ; the equality tolerance τ_eq; any retraining exception; unattended daily publication (`AGENTS.md`); where the daily job runs; visual approval; the Headline Arena reply | Plan §5.1 |
| Research anchor | What the Space computes and claims: one code path; "Train it yourself"; daily delivery; the frozen definitions; the evaluation windows; attribution methods; data date ranges | v21-r8 §19 |
| Publication anchor | How the Space presents and is accepted: the required views; the presentation line; loading and network; acceptance | PUBLISH_RULES 1.2 §7.3 (A9) |
| Orchestrator | The CP-17 and CP-18 briefs carry §19 and A9; publication briefs pin 1.2; programme state | Plan §5.4 |
| Engineering Lead | The feasibility probe and freeze (CP-17); the pipeline, the Space, tests and negative controls (CP-18); runbook touchpoints once the code exists | Plan §5.5 |
| Independent checker | Candidate review under A9; A6 public checks; daily-operation checks | Plan §5.6 |

## Left unchanged on purpose

- **`AGENTS.md`.** Unattended daily publication needs the Owner's own amendment at CP-18. Writing
  it now would grant authority before a final product exists.
- **The publication runbook.** `tests/test_42_publication_runbook.py` resolves every
  `file::symbol` it names, so the Space touchpoints are added in CP-18, when the code exists.
- **The packet template.** Its §5d already carries the daily-operation fields; A9's acceptance row
  is in PUBLISH_RULES §13, which briefs pin.
- **The current Space, site and demo code.** They were not inspected or changed, on the Owner's
  instruction.
- **The CP-21 publication plan.** It pinned 1.1 for PRES-3. 1.2 adds only the conditional A9, so
  PRES-3 under 1.2 has the same obligations.

## Headline Arena

The Owner forwarded a message received on the Space inviting daily forecast submissions to
Headline Arena. The plan (§9) recommends declining for now: the arena's targets do not include
DE-LU day-ahead power; submitting is an external, automated publication; and it cannot stand in
for CP-19's own prospective record. The reply is the Owner's action; a suggested text is in the
plan.
