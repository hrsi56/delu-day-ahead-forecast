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

- **The rehearsal found two defects, both fixed and both covered by tests:** the label written into the bundle's frozen
  files (run 43670023047; fixed at 740ea312, `test_evaluation_sets.py`'s gate test), and an undeclared dispatch input in
  the chain's rehearsal (run 43735265261, HTTP 422; fixed at 56d76de7, `test_chain.py`'s declared-inputs test).
- **The CI reproduction found six scanner failures** (pre1 at 3bf2e074: dates after the boundary in `src/cp18` and the
  workflow, and the frozen verifier's name outside `cp18.r7`); fixed at 633bcb75. pre2 at 0b84126a: every step exit 0.
- **The gate came first and was kept as a part:** the hourly event through a Linux gate (f375f99a) answered the probe's
  first measurements; O54 then raised the bar, and the chain (7631fa44) replaced the gate as the schedule. The gate's
  module (`window.py`) remains: the chain uses its cutoff, start and sleep limit, the acquisition rehearsal uses its
  plan, and the comparison test uses it as the alternative.
- **The test stand-ins** (`tests/cp18a/test_pipeline.py`, `tests/cp18c/support18c.py`) now return a built day's input
  class, which the pipeline requires; no assertion of theirs changed. Every changed CP-18a–c assertion has its `CP-18d`
  comment beside it (`tests/cp18c/test_acquire.py`, `test_space_live.py`, `test_workflow.py`).
- **A test fixture rewrites a copy of the live store** (`tests/cp18d/fixture_after_cutoff.py`) to render a day issued
  with the copy after the cutoff: no live day has one yet. It never touches a checkout's `live/`, says so in every file it
  writes, and re-chains the copy's ledger with CP-17c's own formula.
- **Not changed, by the brief's allowed paths:** the report's and the root README's "runs ... daily" sentence; the
  development bundle's bytes (CP-18b's evidence) stay reproducible (the label and the sets are added only where the
  live store or a CP-18d record carries them, and never into the bundle's files).
- **Usage-limit pauses:** three, recorded in the Lead's ledger with what was running.
