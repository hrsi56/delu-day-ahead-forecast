# CP-18e — decision 33: the live product keeps S_13's search

*Track B, the Engineering Lead's report for the Integration Critic and the Orchestrator. Brief:
`docs/track-b/evidence/cp-18e/issued-brief.md` (`49b66354…`). Anchor `capstone_v21.md` v21-r20 (`80341681…`).*

## What changed

**One rule, in `src/cp18/` only** (`src/cp18/serving.py`). CP-26's 182-day schedule (`cp26.search.serving_search`)
names S_k for the days from S_k's day to the day before S_(k+1)'s. The live rule is that search capped at S_13:
`min(k, 13)`. It equals the schedule on every day through 2027-01-05 and is S_13 from 2027-01-06 on (the Owner's
decision 33). `cp26.search` and the frozen package (`src/cp17*`) are not edited.

| Where the live code asks which search serves a day | Before (5133b02c) | Now |
|---|---|---|
| the pipeline (`cp18.pipeline.run`, its `serving=` default) | `cp26.search.serving_search` | `cp18.serving.LIVE` |
| the payload (`cp18.live.payloads.load_ensemble`, `a1_payload`) | `cp26.search.serving_search` | `cp18.serving.serving_search` (= `LIVE`) |
| the build (`cp18.live.build.build_day`, through `load_ensemble`) | as the payload | as the payload |
| the bundle's rebuild (`cp18.bundle`, a day's payloads again) | `cp26.search.serving_search` | `cp18.serving.serving_search` |
| the store (`cp18.store.LiveStore.record_search`, `verify`) | any validated search k | k > 13 refused, naming decision 33 |
| the command line (`cp18 search --k 14`, H4's route) | entered S_14's state | refused, exit 2, naming decision 33 |

**The state is the pinned one.** For every live day the payload's state is `cp17.runtime.K13`'s `k13.json`, validated
as before by `cp26.search.validate_ensemble(..., 13, 'nominal')`: its search day 2026-07-08, its own eight member
seeds (`member_seeds(13)`) and its content digest. Nothing re-labels it: the A1 payload's `search` stays 13 and
`a1_payload` refuses any other state for a live day (a state of search 14 or 12, or S_13's with a changed seed).

**The frozen package does not tie a day to the schedule.** `cp17.daily`, `cp17.dailyfit` and `cp17.issue` read the
payload's members and pass `meta['search']` through. Only CP-17c's development builder `cp17.tools.payloads` calls
`serving_search`, and it never runs on the live path (its own `BOUNDARY` refuses any day after 2026-09-06). So no day
from 2027-01-06 needs an edit of `src/cp17*` or `src/cp26/`: not BLOCKED.

## "S_14's state not in place"

- **The live rule never names a search after S_13**, and the store refuses one. So no live day can reach the cause.
- **The cause stays in `cp18.causes`** for two reasons:
  - CP-18a's recorded evidence and its forced days. `cp18.forced` gives 2026-09-02 to S_14 by injecting a plain
    function as the rule, and r19's five causes are all forced and recorded there.
  - The negative control below.

  A plain callable passed as `serving=` is a rule before decision 33. Only a `cp18.serving.Rule` applies the cap.
- **The pinned S_13 state absent** no longer reads "S_14's state not in place". A live day whose pinned `k13.json` is
  not in place is left open with the inputs cause and a note naming the pinned state. Before, it took the S_14 cause.
  - The runner never reaches this case: `cp18 prepare` places `k13.json` by hash or refuses the run.
  - The local fallback runs from the Owner's project, where the file is CP-17's.

  This is the one change in what a day before 2027-01-06 can record. It is in a failure path that no issued day
  took. (The other changes of behaviour, the refusals of a later search's state, concern no day.)

## The record and the Space

- **The issued record** names the serving search for every day as before (`inputs.search`: `k`, `file_sha256`,
  `content_sha256`, `search_day`). A day the schedule gives to a later search also carries, at the top level and in
  the run's item for the day, the field the Lead proposes (the Orchestrator rules):

  ```json
  "serving_rule": {"search": 13, "search_day": "2026-07-08", "scheduled_search": 14,
                   "scheduled_search_day": "2027-01-06", "decision": 33,
                   "text": "S_13's state serves this day: DDNN-2's searches in operation end at S_13, and S_14 and every later search are not run (the Owner's decision 33)"}
  ```

  (as the rehearsal's `decision33` leg recorded it). A day the schedule gives to S_13 or earlier gets no such field:
  its record has the keys and values the code at 5133b02c writes, the run's own fields apart.
- **The Space.** No Space surface described how v6's networks are chosen. The two sentences go where the Space
  describes the daily refit: one row after "Last training" in the product panel, through the claim layer
  (`live_network_choice`, both modes). 182 and 2026-07-08 are read from `cp26.search`, not typed. No number changes.
  The row uses the panel's existing key–value list, with no new style (O16).

## The controls (tests/cp18e/test_serving_rule.py)

| Rule | Control | Test |
|---|---|---|
| The live rule is the schedule through 2027-01-05 | every day from 2019-01-01 to 2027-01-05: `LIVE(d) == cp26.search.serving_search(d)`, no `serving_rule` | `test_the_live_rule_is_the_schedule_on_every_day_through_2027_01_05` |
| S_13 from 2027-01-06 | every day to 2040-12-31: 13, and the field names the schedule's search and decision 33 | `test_from_2027_01_06_every_day_is_s13s_and_its_record_names_decision_33` |
| A later search's state never enters the store | `record_search(14, …)` refused naming decision 33, the ledger byte-identical, no `search/`; `cp18 search --k 14` exits 2 naming decision 33; a `k = 14` entry written around `record_search` fails `verify` naming decision 33 | `test_a_later_search_state_entered_into_the_store_is_refused_naming_decision_33` |
| A day served by another state than S_13's is refused by the live path | for a day of 2027, `a1_payload` refuses a well-formed state of search 14, S_13's relabelled as 12, and S_13's with one seed changed; S_13's own state passes validation | `test_a_day_served_by_another_state_than_s13s_is_refused_by_the_live_path` |
| The payload takes the pinned S_13 for a later day | `load_ensemble` gives `k13.json` (the committed pinned copy) for 2026-08-31, 2026-11-20, 2027-01-06, 2027-07-06, 2031-03-01; S_12's day unchanged; under CP-26's schedule S_13's state does not validate for 2027-01-06 (why the change is needed) | `test_the_payload_takes_s13s_pinned_state_…` |
| The rule before decision 33 leaves a day from 2027-01-06 open | a live run (inside the live boundary) on 2027-01-06 with CP-26's schedule injected as the rule: open, "S_14's state not in place", search 14, nothing built, nothing recorded; with the default rule the same day is issued, S_13 asked, the record names decision 33 | `test_control_the_rule_before_decision_33_…`, `test_a_live_day_from_2027_01_06_is_issued_from_s13_…` |
| The injection point on a development day | 2026-08-31 given to S_14 by an injected schedule: issued, record names decision 33; the same schedule as a plain rule: open with the S_14 cause | `test_on_a_development_day_the_injected_schedule_…` |
| Nothing before 2027-01-06 changes in the record | 2026-08-31 under the live rule and under CP-26's schedule: the same search asked, the same record and run item apart from the run's own fields | `test_nothing_before_2027_01_06_changes_in_the_record` |
| No live day carries the S_14 cause | the pinned state absent: open with the inputs cause, search 13, a note naming the pinned state | `test_no_live_day_carries_s14_when_the_pinned_state_is_absent` |
| The Space | two sentences, both modes, 182 and 2026-07-08 from code, after "Last training" | `test_the_space_states_decision_33_where_it_describes_the_daily_refit` |

No CP-18a–d test is changed: their injected rules are plain callables, so CP-18a's forced day and
`test_s14_not_in_place_leaves_the_day_open` keep the S_14 cause, and CP-18a's `record_search(13, …)` test still enters
S_13.

## The rehearsal: a day from 2027-01-06, on a development day (`reports/cp18e/rehearsal.json`)

`python -m cp18.serving_rehearsal`, at `cc64813b` (the final candidate's `src/`). Delivery day 2026-08-31,
wall clock 2026-08-30 12:00 Berlin. Every leg is a fresh pipeline checkout as CP-18a's forced days make one (a bare
origin, the store at CP-17b's state before 2026-08-31, the hooks), with the live-input builder replaying the recorded
responses, the real H2 gate (`refreeze verify`, the binary, the machine, the canary fit) and `cp17.daily.issue_day`
under the frozen host (Pyodide in Node.js). Nothing is retrieved; nothing is pushed beyond the leg's bare origin.

| Leg | Code | Rule injected at `serving=` | 2026-08-31 | Its record | Leg time |
|---|---|---|---|---|---|
| `old` | `src/` at 5133b02c (tree `74d9b30af38f…`) | none: its own (CP-26's schedule) | issued, A1 | `search.k` 13; no `serving_rule` | 409 s |
| `new` | the candidate | none: its own (`cp18.serving.LIVE`) | issued, A1 | `search.k` 13; no `serving_rule` | 410 s |
| `decision33` | the candidate | `Rule(scheduled)`: the schedule gives 2026-08-31 to S_14 | issued, A1, from S_13's state | `search.k` 13, `file_sha256` the pinned `17ade451…`; `serving_rule`: search 13, scheduled search 14, decision 33 | 371 s |
| `control` | the candidate | `scheduled` itself, a plain callable: the rule before decision 33 | open: "S_14's state not in place", search 14 | no record (an open day is recorded in the run only); the run exits 1 | 130 s |

- **Checks** (all `True`, `as expected: True`): `control_open_with_s14`, `decision33_built_from_s13`, `decision33_issued`, `decision33_names_decision_33`, `decision33_record_differs_only_by_serving_rule`, `decision33_same_payloads_and_forecast_as_old`, `new_equals_old`, `new_issued`, `new_record_has_no_serving_rule`, `old_issued`.
- **`new` against `old`:** the eight payload files byte for byte (A1's `A1-2026-08-31.json` `98b6b24f1804…`); the
  forecast's `quantiles_sha256` `75d86a3b3cb9f670…` in all three issued legs; the artifact equal
  outside its own measured fields (`artifact_sha256`, `attempts[0].resources.peak_bytes`, `attempts[0].resources.wall_seconds`, `attempts[0].seconds`, `resources.peak_bytes`, `resources.wall_seconds`); the record and the run's
  item equal outside the run's own fields (its id, times, durations, the shadow fits' measured resources).
- **`decision33` against `old`:** the same payloads and forecast; the record and the run's item differ only by
  `serving_rule` (outside the run's own fields).
- **The `old` leg is the code at 5133b02c:** its `src/` extracted by `git archive` and checked against that commit's
  `src` tree (`74d9b30af38f6417b9496e1c44718f89bf61f62f`); the candidate differs from it under `src/` in `src/cp18/` only
  (13 files).
- Time: 781 s wall, two legs at a time; the legs' sum 1320 s.

## Nothing before 2027-01-06 changes

- **The rule.** `min(k, 13) == k` for every k the schedule gives through 2027-01-05; the test walks every day from
  2019-01-01 and finds the live rule equal to CP-26's schedule, with no `serving_rule`.
- **A development day, end to end** (the rehearsal's `new` against `old`, above): the four payloads (eight files)
  byte for byte;
  the artifact equal outside its own measured resources (`artifact_sha256` covers them), the forecast's
  `quantiles_sha256` equal; the record and the run's item equal outside the run's own fields.
- **The live record's ten issued days** (`reports/cp18e/live-days.json`, `python -m cp18.serving_rehearsal
  --live-days --refit 2026-11-20`, at `cc64813b`). Each day is recomputed locally from what the store holds, by the
  code at 5133b02c and by the candidate, each in its own interpreter, from a scratch copy of `live/`. The steps: the
  state before the day (its ledger entry), D−2's release from the committed archive, the serving search under each
  code's own rule, and the day's four payloads from the committed archive. Every request to the network is refused,
  and nothing under `live/` is written.

| Day | Schedule / 5133b02c's rule / the candidate's / the record's `search.k` | Payload files, 5133b02c against the candidate | Payload hashes against the record | Differences from the record's `inputs` (both codes alike) |
|---|---|---|---|---|
| 2026-11-06 | 13 / 13 / 13 / 13 | byte-identical | equal | decision 31's label, absent from this CP-18c record; `data_refresh_utc`: the same instant, `…Z` in the record, `…+00:00` now |
| 2026-11-07 | 13 / 13 / 13 / 13 | byte-identical | equal | decision 31's label, absent from this CP-18c record |
| 2026-11-08 | 13 / 13 / 13 / 13 | byte-identical | equal | decision 31's label, absent from this CP-18c record |
| 2026-11-14 | 13 / 13 / 13 / 13 | byte-identical | equal | decision 31's label, absent from this CP-18c record |
| 2026-11-15 | 13 / 13 / 13 / 13 | byte-identical | equal | decision 31's label, absent from this CP-18c record |
| 2026-11-16 | 13 / 13 / 13 / 13 | byte-identical | equal | none |
| 2026-11-17 | 13 / 13 / 13 / 13 | byte-identical | equal | none |
| 2026-11-18 | 13 / 13 / 13 / 13 | byte-identical | equal | none |
| 2026-11-19 | 13 / 13 / 13 / 13 | byte-identical | equal | none |
| 2026-11-20 | 13 / 13 / 13 / 13 | byte-identical | equal | none |

- Every day's `search` in the record names S_13's pinned file (`file_sha256` `17ade4513a39dffdf6b3fc90e5d45228bbafa71b86af04af22ae4b2418f9d5dc`, the freeze
  manifest's `state_route.k13`), and no record carries `serving_rule`. The two codes' recomputations are byte-identical
  (the payload files and the build's whole record of the inputs, its timings and scratch paths apart).
- The differences from the issued records are the records' own age: days 2026-11-06 to -15 were written by CP-18c's
  code, before CP-18d added decision 31's four label fields; both codes now add them, the same way. 2026-11-06's data
  refresh time is written in CP-18c's earlier notation.
- **The forecast.** A1's fit of 2026-11-20 again, under the frozen host from the candidate's rebuilt payload:
  `quantiles_sha256` `7fb7c9889c7e9274d50d909cbb3ec3dbf4a47f0789992639ce6d4f68f259e0c8`, equal to the issued artifact's, every member's weights' hash equal.
- The store verified with the same head (`227cb8fc3cb7d916…`) in both codes. Time: 356 s, two
  workers (281 s and 281 s), then the refit.

## The freeze, CP-26 and the other bindings

- **A1's freeze:** `PYTHONPATH=src python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json
  --root .` prints `verified` at `cc64813b` (the final candidate's `src/`). `git diff --stat 08e6dcd2 HEAD` over
  `src/cp17`, `src/cp17b`, `src/cp17c`, `src/cp17probe`, `src/cp17cprobe`, `src/cp26`, `live/`, `.github/`,
  `docs/index.html`, `README.md`, the anchor, PUBLISH_RULES, `progress.md` and the exposure ledger is empty.
- **The frozen package zip** is the import closure of `cp17`'s entry modules (`cp17.tools.bundle`); `cp18` is not in
  it, so the package identity is unchanged (`refreeze verify` rebuilds and compares it).
- **No earlier evidence binds a changed file's bytes.** No changed path is named in `src/cp26/harness.py`'s `PINS` or
  `tests/pres5_landed_code.py`, or in any freeze manifest. The files' hashes at the base appear only in briefs, as
  inputs: CP-18e's, and CP-18d's for `causes.py`. They appear in no verdict, in no file under `reports/`, and in
  none of CP-18c's or CP-18d's evidence. `space-product/app/main.js`'s bytes at the base are cited nowhere.
- **The red line:** the rehearsal uses development days only. The live-day recomputation is the live pipeline's
  own (r20 §24.14's exemption), reads the committed archive, retrieves nothing and makes no research number, chart or
  choice. CP-18a's and CP-18b's red-line scans and CP-18a's live-transport lint pass over `src/cp18/`.
- **4.7T:** nothing here is 4.7T's; its window (2026-09-07 to 2026-12-05) is S_13's under either rule.

## Disclosures

- **A pre-existing failure, not this round's.** `tests/cp18a/test_forced.py` (a local stress test, skipped in CI) fails
  at the base, before any CP-18e change (`4dfa981e`, the brief's commit on `08e6dcd2`), and identically at the
  candidate. 2026-09-03 is forced as "inputs not shown" (its load forecast archived as a live retrieval two hours after
  the cutoff), and since CP-18d's decision 31 such a day is issued with the copy fetched after the cutoff. Then the
  run's broken host fails it as a chain failure: found `chain`, expected `inputs`. Every other forced day is as
  expected, 2026-09-02's "S_14's state not in place" included. CP-18d's stress runs used Python 3.12, where the test is
  skipped (its pins check needs the issuing host's CPython 3.13.15), so it was not seen. It is outside decision 33 and
  this round's scope; the proposed ruling is in the return.
- **The first rehearsal (at `8ef98fe8`) reported "as expected: False"** on two checks. Its substance held: the same
  payloads byte for byte, the same forecast, S_13 named, the control open. The records also differed in the shadow
  fits' own wall time and peak memory, a run field the driver had not classified. `156bba12` classifies it, like the
  artifact's own `resources`. The first run's record is not kept.
- **A rehearsal run I voided.** The second run (at `156bba12`) failed in its `decision33` leg because I committed
  `ff008241` while it ran: each leg clones the candidate's `HEAD` when it starts. No record was written. `cc64813b`
  makes the driver refuse a candidate whose `src/` differs from `HEAD` and void a run if `HEAD` moves. The records in
  `reports/cp18e/` are both from `cc64813b`, with nothing committed during either run. Two earlier live-day runs (at
  `156bba12` and `ff008241`, both as expected) are superseded: the first did not keep the values of the differences
  from the issued records, which `ff008241` added.
- **A lint found two post-boundary date literals** (S_14's day) in the new docstrings; CP-18a's live-transport lint
  lists no such date for `src/cp18/`. They now read "S_14's day". The record field likewise names decision 33 by
  number and text, without its record's file name, which carries a date after the boundary.
- **Four tests failed in my first suite run** for want of the five BLAS variables in that shell (CP-26's harness
  refuses to build otherwise). With them set, they pass.
