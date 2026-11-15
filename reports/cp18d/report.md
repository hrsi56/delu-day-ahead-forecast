# CP-18d: no missing day, a daily operation that needs nobody, and the live product's follow-ups

*The Track B Lead's report for CP-18d (the brief `docs/track-b/evidence/cp-18d/issued-brief.md`, `d4fcc76a…`), with the
Orchestrator's rulings O54 and O56 (`docs/track-b/evidence/cp-18d/orchestrator-messages-as-relayed.md`). Every claim
here is to be checked against the code, the tests and the records it names.*

## 1. Decision 31: v6 with the load forecast fetched after the cutoff, labelled

- **The rule** (`src/cp18/live/history.py`, `fetched_after_cutoff`): when no copy of D's own load forecast is admitted
  against D's cutoff, the earliest complete live retrieval of it after the cutoff is used, and D's judgement stays "not
  admitted", naming the copy and its retrieval time. Only D's own load forecast: a history day's load forecast, the
  prices and the GFS flag keep decision 22's rule (`tests/cp18d/test_other_inputs_keep_d22.py`, through the real build
  on development days). No copy at all leaves the day open with its cause, as before.
- **The label** (`src/cp18/inputclass.py`): two classes, "all inputs before the cutoff" and "load forecast fetched
  after the cutoff" with that copy's retrieval time (UTC). Never "late", never "timely". A CP-18d day record must carry
  it and agree with its own availability evidence; a CP-18a–c record is derived from its evidence. The copy must precede
  the issuance that used it.
- **Where it is carried:** the build's availability (`live/build.py`), the inputs (`live_inputs.py`), the pipeline's
  day record and run record (`pipeline.py`), the store (`store.py`: refused at write and at verification without it),
  the Space's live record (`live_claims.live_record`, with the count per class), and every Space surface that shows an
  issued day (`space-product/app/main.js`).
- **Not in the bundle's files.** The scratch rehearsal (run 43670023047) found that the bundle's frozen schema
  (`cp17`'s verifier, through `cp18.r7`) refuses any key it does not know; the label first written into
  `issued-forecasts.json` and `evaluation.json` was refused. The fix (740ea312): the bundle keeps its frozen schema and
  only refuses an unlabelled day; the label and the evaluation per class live in the Space's own live record, computed
  at the build. A regression test builds a bundle from a store holding a day fetched after the cutoff and gates it
  (`tests/cp18d/test_evaluation_sets.py`).
- **The evaluation per class** (O32, O33): `cp18.evaluation.class_sets` scores the prospective record's days with every
  input before the cutoff on their own, and all issued days beside them, each with its count; the all-days set must equal
  the bundle's own prospective window. `cp18.running.running(..., classes=)` gives the running means and their
  intervals per set. The proposed display is in section 5.
- **CP-19's count:** a day issued with the copy after the cutoff is an issued day, counted with its label
  (`LiveStore.days()`, `live_record`'s `input_classes`).

## 2. The daily operation without the scheduler (item 2 and O54)

- **The measurement** (`reports/cp18d/schedule-probe.json`, by `src/cp18/schedule_probe.py`, read-only `gh` calls):
  FINAL NUMBERS PENDING THE THIRD PROBE DAY. On the probe's first night its runs were created 6 h 11 min to 7 h 36 min
  after their cron time, growing about half an hour an hour; the macOS queue was seconds. The Orchestrator measured
  `daily.yml`'s own 07:40 and 08:20 UTC crons start 7 h 16 min and 7 h 23 min late the same day.
- **First design, an hourly event through a Linux gate** (`src/cp18/window.py`): an event in a band of about 11 hours
  before D's cutoff starts D's acquisition in time, whatever the delay. It covers any delay up to 12 hours while events
  keep coming; it does not cover days on which the scheduler drops most events (`tests/cp18d/test_chain.py`, the
  simulation: with 85 % of events dropped, whole days go uncovered).
- **The design chosen, a self-dispatching chain** (`src/cp18/chain.py`, `.github/workflows/daily.yml`), because O54
  asks for robustness to both: each link is one run started by `workflow_dispatch` (GitHub starts it at once):
  `tick` (Linux; decides what is due from the store's run records on `main` and the last link's state; sleeps at most
  5.75 h), then `acquire` or `run` (macOS, CP-18c's jobs), then `alert`, then `next` (dispatches the next link with
  `actions: write` only). The scheduled events only seed a broken chain. One concurrency group keeps one link running
  and one pending, so a second chain dies at its next link and two acquisitions never write the same day. Every job is
  inside GitHub's 6-hour limit (tick 355 min, acquisition stop-by 340 min with timeout 355). A 60-day simulation in
  winter and summer acquires every day before its cutoff and runs it once after it.
- **The alert** (`src/cp18/alert.py`, `issues: write` and `contents: read` only): one GitHub issue per problem (a failed
  job, a recent day not issued, a recent day issued with the load forecast fetched after the cutoff), opened or
  commented on, closed by itself once a later day is issued with all inputs before the cutoff; tested with a mocked API.

## 3. The claim over a moved `main` (O47)

`src/cp18/claim.py`: a push refused because `main` moved is re-applied when no moved commit touched any of this
commit's own files and all of them are under `live/`: the same files and content, committed on the new `main` through
the hooks, pushed as a fast-forward; at most three times; never a force-push. A moved commit touching one of its files
still refuses, as before. Reproduced locally (`tests/cp18d/test_claim_o47.py`) and on the runner (runs 43670023047 and
43708842868: a commit pushed during the records step, the records kept).

## 4. The live product's follow-ups

- The two "A1" sentences now name v6, with "A1 in the frozen records"; the unused designation sentence is removed.
- "Runs daily" in the report and the root README is outside CP-18d's allowed paths: the Space states the schedule
  (`live_schedule`) beside its issued and not-issued days, and the report's sentence is a follow-up (open item).
- v1's history page carries its own preview tags naming v1 (`scripts/build_product_space.py`, recorded in
  `app/history-files.json`); whether the host's own tags still come first is visible only after a publication.
- The runner's Actions artifact keeps the whole Space build, hidden files included, recorded before the fitted arrays
  are deleted (`src/cp18/runner_artifact.py`: `record`, `verify`).

## 5. The proposed display (O16: the Orchestrator rules)

See the Space Builder's hand-over (`.local/artifacts/cp-18d/builder-space-handover.md`, section 3) and the screenshots
it lists: the label on every issued day, the counts once per view, hollow diamonds for the days fetched after the
cutoff in the per-day chart, the two sets in the cumulative section (one chart when they are the same days), the
per-set rows in Validation and Reliability.

## 6. The rehearsal (item 5)

`reports/cp18d/rehearsal/rehearsal-runs.json`: in `hrsi56/delu-pipeline-dryrun`, fake credentials, development days.
A normal day and a missed acquisition issued with the copy fetched after the cutoff, labelled, through the frozen chain
(Pyodide); a `main` moved during the records step, records kept; the acquisition's in-job wait (9 polls a real minute
apart) and the sleep before its start (600 s); the chain's self-dispatch.

## 7. Disclosures

Filled at the return.
