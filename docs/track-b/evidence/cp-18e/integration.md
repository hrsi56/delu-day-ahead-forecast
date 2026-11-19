# Verdict — CP-18e — Integration — PASS

- Candidate SHA: `61d3fd1f97ce23920d10f1439bd85766f0570457` (`gauntlet/cp-18e`; base `main` = `08e6dcd2478872b6851b9b0d011eed702a94bc5b`)
- Plan / version / bar: `capstone_v21.md`, v21-r20 (file SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`), §24.13 "#### Where S_14 runs (H4)" (section 14 lines, 885 bytes, SHA-256 `ad374e1dbe1a68ee197a1bfbd2a6f904cc70f45b991d5f8f90898aca4f71fb68`); with the brief's four further quoted bars (§24.9, §24.13 "For CP-18", §24.14 "What stays exactly as registered", `docs/PUBLISH_RULES.md` 1.5 A9), read under the Owner's decision 33 (`docs/track-b/owner-decisions-2026-11-19.md`, `73d64e47…`), which supersedes H4 and the cause "S_14's state not in place" for the live product only.
- Verbatim bar excerpt:

  > #### Where S_14 runs (H4)
  >
  > - **S_14 = 2027-01-06 runs natively on the Owner's M3, the machine that ran S_13.**
  >   - It runs in the environment `uv.lock` pins, under the same phase and rules (§24.9) and the freeze's
  >     seeds.
  >   - It counts as part of the live pipeline for §24.2's guard.
  >   - S_13's fits took 5,079 s of native fit time there, on one worker. With CP-26's 2× margin, S_14 is
  >     estimated at about 3 hours.
  >   - Its state reaches the runner by the route CP-17c fixes for `k13.json`.
  >   - A delivery day that S_14 serves is not issued until that state is in place. Decision 23's catch-up
  >     then applies.
  >   - If that machine is unavailable, where S_14 runs is a new decision for the Owner.
  > - **Why.** A native search on another machine is not the same arithmetic, and none was measured.
  > - **CP-18 schedules S_14.** It falls after 4.7T's window, so 4.7T is not affected.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.) Confirmed in the file at the
  candidate with `scripts/bar.py check` (below).
- Worktree clean before and after: **yes**. `/Users/djourno/Downloads/PJM/.local/worktrees/cp-18e/critic-1`, detached at
  the candidate; `git status --porcelain` empty at the start, at the resume and at the end; `HEAD` unchanged. No Git
  write was made to the worktree or to the product repository. The worktree is left in place for `critic-close`.
- **Pause.** The review was paused by the usage limit from about 14:41 UTC (just after the live-days run finished,
  14:41:31 UTC) to about 16:41 UTC, and resumed on the same candidate. At the resume the worktree was re-checked clean
  at `61d3fd1f…` (also `gauntlet/cp-18e`'s tip). The rehearsal's and the live days' outputs written before the pause
  were read, not rerun; only CP-18a's forced days (base and candidate) were run after the resume.
- Isolation: cooperative and procedural only (no read-only mount). I read the brief, the decision record, the
  candidate's code, tests, records and report; I did not read the Lead's ledger, drafts, validation folder or any
  conversation.

## Commands actually run

Environment for every Python command: `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1
CP17_PROJECT_ROOT=/Users/djourno/Downloads/PJM`, the five BLAS variables at 1 for the tests, the rehearsal and the
forced days; interpreter `/Users/djourno/Downloads/PJM/.venv/bin/python` (CPython 3.13.15) with
`PYTHONPATH=<W>/src`, from `W` (= the critic worktree). Scratch: `/Users/djourno/Downloads/PJM/.local/tmp/cp-18e/critic/`
(removed at the end). Times are UTC.

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief cp-18e` | 0 | this assignment |
| 2 | `git -C W status --porcelain`; `git -C W rev-parse HEAD main`; `git -C W log --oneline 08e6dcd2..HEAD`; `git -C W diff --stat 08e6dcd2 HEAD` | 0 | empty; `61d3fd1f…`, `08e6dcd2…`; 6 commits (`4dfa981e` brief … `61d3fd1f`); 19 files, +5608/−31 |
| 3 | `shasum -a 256` of the packaged brief, decisions 33–34, the anchor, and the canonical `.local/artifacts/cp-18e/issued-brief.md` | 0 | `49b66354…` (packaged = canonical; equals `progress.md`'s record at the base), `73d64e47…`, `80341681…` |
| 4 | `git show main:scripts/bar.py \| python3 -I - check W/docs/track-b/evidence/cp-18e/issued-brief.md --source capstone_v21.md@61d3fd1f… --source docs/PUBLISH_RULES.md@61d3fd1f…` | 0 | five `ok:` lines (lines 149–188, 192–205, 209–238, 242–257 in the anchor; 261–274 in PUBLISH_RULES) |
| 5 | `bar.py check` of this assignment's H4 excerpt against `capstone_v21.md@61d3fd1f…`; `bar.py identity`/`bar … --at 61d3fd1f…` of the section | 0 | `ok: lines 1–14 (884 bytes)`; section 14 lines, 885 bytes, SHA-256 `ad374e1d…` (identity line exact) |
| 6 | The brief's 18 execution-input hashes at `5133b02c` (decisions at `08e6dcd2`), and at the candidate | 0 | all 18 match at the base; unchanged at the candidate except the 9 `src/cp18` files the round edits |
| 7 | `git -C W diff --stat 08e6dcd2 HEAD -- live .github src/cp17 src/cp17b src/cp17c src/cp17probe src/cp17cprobe src/cp26 docs/index.html README.md capstone_v21.md docs/PUBLISH_RULES.md progress.md AGENTS.md docs/track-b/evidence/cp-17 docs/track-b/evidence/cp-17b docs/track-b/evidence/cp-17c reports/cp18a reports/cp18b reports/cp18c reports/cp18d docs/track-b/evidence/cp-18c docs/track-b/evidence/cp-18d tests/cp18a tests/cp18b tests/cp18c tests/cp18d tests/pres5_landed_code.py` | 0 | empty |
| 8 | `grep -rn "serving_search\|search_file\|load_ensemble\|causes.S14" src/cp18`; `git grep -n -e "pipeline\.run" -e "serving=" -- ':!tests' ':!docs'`; `grep -rn "serving_search\|search_day\|K13\|search" src/cp17*` | 0 | traced (checklist A1, A2) |
| 9 | Base-hash search: for each changed file, its `08e6dcd2` SHA-256 prefix and blob id with `git grep` over the candidate tree | 0 | one hit only: `causes.py`'s base hash in `docs/track-b/evidence/cp-18d/issued-brief.md` (an input table, not a binding); `main.js` cited nowhere |
| 10 | Freeze manifests' governance pins (each `copy` file's SHA-256 against `sha256`), and every changed path searched in the three freeze manifests, `src/cp26/harness.py`, `tests/pres5_landed_code.py` | 0 | cp-17b 8/8 and cp-17c 12/12 governance copies match; no changed path named |
| 11 | CP-26 `PINS`: each pinned file at `08e6dcd2` and at `HEAD`; `harness.git_blob_sha256(., ANCHOR_COMMIT, 'capstone_v21.md') == PINS[...]` | 0 | all 25 pinned files byte-identical base→candidate; anchor at `ANCHOR_COMMIT` matches |
| 12 | Re-derivation: every day 2000-01-01..2045-12-31, `cp18.serving.LIVE(d)` and `.record(d)` against `cp26.search.serving_search(d)` | 0 | 0 mismatches through 2027-01-05 (`LIVE == schedule`, `record == {}`); from 2027-01-06, 0 mismatches (`LIVE == 13`, field names the schedule's k ≥ 14 and decision 33); S_13 = 2026-07-08, S_14 = 2027-01-06; 4.7T's window 2026-09-07..12-05 is {13} under both |
| 13 | `pytest -q -p no:cacheprovider tests/cp18e` | 0 | `12 passed in 20.26s` |
| 14 | `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json --root .` | 0 | `verified` |
| 15 | `pytest -q -p no:cacheprovider --basetemp=<scratch>/pytest-tmp -rfs tests/cp18a tests/cp18b tests/cp18c tests/cp18d tests/cp18e tests/test_24_live_namespace_is_walled_off.py` (14:08–14:22) | 1 | `1 failed, 769 passed, 20 skipped in 886.33s`; the failure is `tests/cp18a/test_forced.py::test_each_cause_is_forced_and_recorded`, only `{'2026-09-03': 'chain'} != {'2026-09-03': 'inputs'}`, the other five days identical. Skips: 1 superseded (`cp18a/test_rules.py:43`), 19 for absent local Space inputs (`cp18b/test_space_build.py` ×7, `cp18c/test_space_live.py` ×7, `cp18d/test_space_d.py` ×5) |
| 16 | `python -m cp18.serving_rehearsal --project /Users/djourno/Downloads/PJM --work <scratch>/rehearsal-work --out <scratch>/r.json` (14:23–14:35) | 0 | all ten checks `True`, `as expected: True`; 757 s wall, legs 381/381/375/132 s |
| 17 | `python -m cp18.serving_rehearsal --live-days --refit 2026-11-20 --project /Users/djourno/Downloads/PJM --work <scratch>/live-work --out <scratch>/l.json` (14:36–14:41) | 0 | ten days `as expected`, refit `True`, `as expected: True`; 334 s (two legs of 260 s, then the refit) |
| 18 | Comparison scripts: my `r.json` and `l.json` against `reports/cp18e/rehearsal.json` and `live-days.json`; the store's issued artifacts' `lineage.inputs` against the records and `l.json`; live store runs scanned for `s14` / `search_state_missing` | 0 | see A3; all equal apart from run ids, times and the store head of each throwaway rehearsal origin |
| 19 | (after the resume, 16:41–16:45, two workers) `git -C W archive 08e6dcd2 src` into scratch; `python -m cp18.forced --candidate W --project … --work <scratch>/forced-base` with `PYTHONPATH=<scratch>/base-src/src`, and the same with `PYTHONPATH=W/src` | 1, 1 | both: 08-31 `h2`, 09-01 `no_run`, **09-02 `s14`**, 09-03 `chain` (expected `inputs`), 09-04 `chain`, 09-05 `chain`; `found`, `gate_a`, `issued`, `inputs_2026_09_03.shown` (True) and `gate_b.passed` equal between base and candidate |
| 20 | `brew list --pinned`; `node --version` | 0 | `node` pinned; v26.7.0 at `/opt/homebrew/bin/node` |
| 21 | Pattern scan of the new files for token/secret/password shapes; value scan against `/Users/djourno/Downloads/PJM/.env` | 0 | no pattern hit; no `.env` exists, so no value scan was possible here |

## Evidence actually inspected

- `docs/track-b/evidence/cp-18e/issued-brief.md` (whole), `docs/track-b/owner-decisions-2026-11-19.md` (whole),
  `reports/cp18e/report.md` (whole, as a claim).
- The whole source diff `08e6dcd2..61d3fd1f` of `src/cp18/{serving.py, pipeline.py, live/payloads.py, bundle.py,
  store.py, __main__.py, live_claims.py, causes.py, inputs.py, live_inputs.py, live/__init__.py, live/build.py}`,
  `space-product/app/main.js`; `src/cp18/serving_rehearsal.py` (whole); `tests/cp18e/test_serving_rule.py` (whole).
- Unchanged code read for the trace: `src/cp18/live/build.py::build_day`, `inputs.py::pinned_search`/`search_file`,
  `live_inputs.py::build`, `forced.py` (`setup`, `run`, `EXPECTED`), `__main__.py::cmd_run`,
  `cp26/search.py` (`search_day`, `serving_search`, `member_seeds`, `validate_ensemble`), `cp17/dailyfit.py`,
  `cp17/issue.py::_training`, `cp17/tools/payloads.py`, `cp17probe/native.py`, `cp17/tools/refreeze17c.py`,
  `.githooks/pre-commit`, `cp26/harness.py` (`PINS`, `identities`).
- `reports/cp18e/rehearsal.json` and `reports/cp18e/live-days.json` (summarised field by field and compared with my runs).
- `live/store/ledger.jsonl` (kinds and causes), the 17 run records under `live/store/runs/`, the ten
  `live/store/issued/*/record.json` and `artifact.json`; the cp-17/17b/17c freeze manifests (governance pins,
  `state_route.k13`); `docs/track-b/evidence/cp-17c/freeze-manifest.json` `k13` against the project's file
  (`17ade451…`, content `6090f4ab…`, k 13, 2026-07-08).
- `capstone_v21.md` §16.2 (its "public wording" sentence) for further item 5.

## Checklist verdict

### A. The assignment's "What to check above all"

| # | Item | Verdict | Evidence |
|---|---|---|---|
| A1 | No live day can be served by any search but S_13, or carry "S_14's state not in place" | PASS | Every live call site now asks `cp18.serving`: `pipeline.run`'s default `serving = serving or S.LIVE`; `live.payloads.load_ensemble` and `a1_payload` import `cp18.serving.serving_search` (= `LIVE`); `bundle.Payloads` rebuild likewise; `store.record_search` and `verify` refuse k > 13; `cmd_search` refuses k > 13 before opening the store (exit 2). `LIVE` = `min(schedule, 13)` (12 above). The S14 cause is set in only two places in `pipeline.py`, both guarded by `k > S.LAST`, which `LIVE` never yields. Only `src/cp18/forced.py` (CP-18a's forced days, development dates) and `serving_rehearsal.py` pass `serving=`; `cmd_run` (the live command and the workflow's) passes none. The live store holds no `search` entry; its 17 runs and 8 not-issued entries carry no `s14` and no `search_state_missing`. |
| A2 | The frozen package does not tie a day to the schedule on the live path; `src/cp17*`, `src/cp26/` unchanged | PASS (agree: not BLOCKED) | Diff over those paths empty (7). In `src/cp17*`, `serving_search` is called only by `cp17/tools/payloads.py` (CP-17c's development builder) and `cp17probe/{payload,native}.py`; no `cp18` module imports either (imports listed from `src/cp18`). `cp17.dailyfit` passes `meta['search']` through and fits the payload's own member seeds; `cp17.issue::_training` copies `result['search']`; `cp17.daily`, `shadow`, `hostcheck`, `schema` and the browser host do not mention the search. So a day from 2027-01-06 needs no edit there. |
| A3 | Nothing before 2027-01-06 changes, byte for byte | PASS | Re-derived (12): `min(k,13) == k` and `record == {}` for every day through 2027-01-05. Code: the k ≤ 13 branch asks `inputs.search_file(k)` as before, and `**rule` is `{}`, so the record and run item are unchanged. **Rehearsal (16):** `new_vs_old` payload files equal (A1 `98b6b24f…`), `quantiles_sha256` `75d86a3b…` in all three issued legs, artifact differs only at its own measured fields, record and run item differ only at run fields; same as the committed record field by field. **Live days (17):** for all ten days schedule = old rule = new rule = record `search.k` = 13; old vs new payload files byte-identical and the build records equal apart from timings/paths; recomputed payload hashes equal the records' and the artifacts' `lineage.inputs`; no `serving_rule`; the only differences from the issued records are decision 31's four labels absent from the five CP-18c records and 11-06's `…Z` notation, alike in both codes; refit of 2026-11-20 `7fb7c988…` = the issued artifact's, members' params equal; store head `227cb8fc…` in both codes. My run equals the committed `live-days.json` on every compared field. **The one stated change** (pinned S_13 state absent → the inputs cause with a note, not the S14 cause): needed by decision 33 ("which no live day can now have"), since under the base code a live day without `k13.json` would have taken the S14 cause; it is a failure path no recorded day took (no `s14`, no `search_state_missing` in any live run), and the inputs cause is already the code's cause for a day from which no payload can be built. |
| A4 | The controls, one per rule, run as tests | PASS | `tests/cp18e` 12 passed (13): store refusal naming decision 33 with ledger byte-identical, `cp18 search --k 14` exit 2, a hand-written k = 14 entry failing `verify`; `a1_payload` refusing a well-formed S_14 state, S_13 relabelled as 12, and S_13 with one seed changed, for a 2027 day; the rule before decision 33 leaving 2027-01-06 open with "S_14's state not in place", search 14, nothing built or recorded; the default rule issuing it from S_13 with the field. The rehearsal's `control` leg reproduced it end to end (open, `s14`, search 14, no record, exit 1). |
| A5 | The Space: two sentences, through the claim layer, no hand-typed number, no new style; where it sits | PASS | `live_network_choice` in `_common` (both modes, identical): "Each day's refit trains the networks again, with the configurations a DDNN-2 search chose. The development evaluation re-ran that search every 182 days; the live product keeps the 2026-07-08 search's choice for every later day (the Owner's decision 33)." 182 from `SEARCH_SPACING_DAYS`, 2026-07-08 from `serving.search_day(13)`, 33 from `serving.DECISION`. One `dt`/`dd` row in the existing `dl.kv` after "Last training", before "Data refresh"; no CSS change, the `data-network-choice` attribute is unstyled. No prior Space surface described the network choice (searched `main.js` and the claims). The row label "Network configurations" is typed in `main.js` like the panel's other labels; it carries no number. Not checked: the rendered page, since the Space build tests skip without the local Space inputs (15); the Owner owns the visual layer. |
| A6 | Freeze, CP-26, red line: `verified`; `PINS` and governance pins hold; no file under `live/`, `.github/workflows/`, `src/cp17*`, `src/cp26/`, the report or README changed | PASS | `refreeze verify` → `verified` (14). Governance copies 8/8 and 12/12 (10). All 25 `PINS` files byte-identical base→candidate and the anchor at `ANCHOR_COMMIT` matches (11); two pinned paths differ from the working tree identically at base and candidate (the anchor, checked by the harness at its commit; `docs/track-b/evidence/cp-26/continuation-v21-r14/authority.json`, absent from the tree at both), so nothing here moves them. Protected-path diff empty (7). |

### B. The brief's Observable outcome

| # | Item | Verdict | Evidence |
|---|---|---|---|
| B1 | The live serving rule: one rule in `src/cp18/`; the pinned `K13` validated with `validate_ensemble(..., 13, 'nominal')`, its own seeds, never relabelled; no live day with the S14 cause (forced days' retention stated); `cp18 search --k 14` refused naming decision 33; BLOCKED condition | PASS | A1, A2, A4. Payload `meta['search'] = 13`, `search_day` 2026-07-08 from the ensemble; the rehearsal's `decision33` record names `file_sha256` `17ade451…` (= freeze manifest `state_route.k13`) and the artifact lineage search 13. The retention of `causes.S14` is stated in `causes.py`, `serving.py` and the report (CP-18a's recorded forced days, the negative control, a store holding it still verifies). BLOCKED condition does not arise. |
| B2 | Nothing before 2027-01-06 changes (development days and the ten issued days); `live/` untouched | PASS | A3; `live/` diff empty. |
| B3 | A day from 2027-01-06 rehearsed on a development day by the injection point: issued from S_13, record names S_13 and decision 33; negative control open with the S14 cause | PASS | My rehearsal (16): `decision33` issued A1 on 2026-08-31 with the schedule giving it to S_14, `search.k` 13, pinned file, `serving_rule` {search 13, scheduled 14, 2027-01-06, decision 33, text}; record and run item differ from `old` only by `serving_rule`; `control` open with "S_14's state not in place". Only development days; nothing retrieved. |
| B4 | The record names the serving search and, for a later day, decision 33 (field proposed, Orchestrator rules); the Space's sentences; report and README not edited | PASS | `inputs.search` kept for every day; `serving_rule` at top level and in the run item only when the schedule's k > 13 (proposal for the Orchestrator's ruling). Space: A5. `docs/index.html`, `README.md` unchanged (7). |
| B5 | Negative control for each rule; CP-18a–d tests stay green (changes stated beside the test); `verified`; `PINS` and governance pins | PASS | A4, A6. No CP-18a–d test changed (7). Suite: 769 passed, 20 skipped, 1 failed: `test_forced`, which fails identically at the base (19): same six causes in both codes, 2026-09-03 `chain` instead of `inputs` because decision 31 (CP-18d) now issues a day whose load forecast came after the cutoff (`inputs_2026_09_03.shown` True in both), and 2026-09-02 keeps "S_14's state not in place". Pre-existing, outside decision 33, unchanged by CP-18e. |
| B6 | The packet's table for the Orchestrator's steps after the LAND | NOT CHECKED (by design) | It belongs to the Lead's return, written after this review. |

### C. The brief's Further items

| # | Item | Verdict | Evidence |
|---|---|---|---|
| C1 | 4.7T exactly as registered; its window S_13's under both rules; no 4.7T issuance, store, score or audit | PASS | Window 2026-09-07..12-05 → {13} under schedule and `LIVE` (12); no 4.7T path in the diff. |
| C2 | A1 frozen; no frozen file changes; `verified` | PASS | A2, A6. |
| C3 | CP-26 as it is | PASS | `src/cp26/` and its evidence untouched; `PINS` files identical. |
| C4 | The red line | PASS | The rehearsal plans only 2026-08-31 under the development guard; the live-days recomputation reads the committed archive with a refusing transport and writes only under its scratch copy; CP-18a/b red-line scans and the live-transport lint passed in the suite; no post-boundary date literal in the new `src/cp18` code (grep). |
| C5 | §16.2's public wording: outcome item 4 | PASS | A5; the sentences say what decision 33's "public wording" bullet requires. |
| C6 | Critic and return per templates §§2–3 | PASS for this verdict | This file follows §2's form; the return (§3) is the Lead's. |

### D. Applicable constraints

| # | Item | Verdict | Evidence |
|---|---|---|---|
| D1 | Homebrew `node` pinned and installed | PASS | (20) |
| D2 | Credentials: none needed; none printed or committed; telemetry off | PASS (limited) | No pattern hit in the new files; no `.env` to value-scan here; my runs exported both variables. The Lead's own runs are not observable to me. |
| D3 | Allowed paths | PASS | The 19 changed paths are all in `src/cp18/`, `tests/cp18e/`, `space-product/`, `reports/cp18e/`, `docs/track-b/evidence/cp-18e/`; none of the forbidden paths changed (7). |
| D4 | No earlier evidence binds a changed file's bytes (`PINS`, `tests/pres5_landed_code.py`, freeze manifests' governance pins, CP-18c/d evidence) | PASS | (9)–(11). The only citation of a base hash is `causes.py` in CP-18d's brief's input table, an input record that no test re-checks (suite green apart from the pre-existing failure). `reports/cp18c/evidence/space-build-2026-11-12.json`'s `claims_sha256` records a past build already superseded by CP-18d's claims; nothing re-derives it. |
| D5 | Tools: gauntlet start, worktree, critic-open/brief/close, return | PARTIAL, as far as visible | This worktree was opened detached at the candidate and the critic brief prints from `main`'s `scripts/gauntlet.py`; `start`, `critic-close` and `return` are outside what I can observe. |
| D6 | Memory directory not opened | PASS for this review | I did not open it. |
| D7 | Owner-facing Git commands non-interactive | NOT CHECKED (by design) | They are in the packet (B6). |
| D8 | First commit copies the canonical brief byte for byte | PASS | `4dfa981e` adds only the brief, parent `08e6dcd2`; packaged = canonical = `49b66354…` (3). |

### E. The bar sections

| # | Bar | Verdict | Evidence |
|---|---|---|---|
| E1 | §24.13 H4 (quoted above), superseded for the live product by decision 33 | PASS | H4's route (`cp18 search --k 14`, the store's `search` entries) is closed with decision 33 named. No S_14 is scheduled, and no day waits for its state. H4 stays in the plan text and is not edited (the anchor records decision 33 at its next revision). |
| E2 | §24.9 (S_14's schedule superseded for the live product only) | PASS | `cp26.search`'s schedule and the development searches S_0..S_13 are untouched. The live rule caps at S_13. |
| E3 | §24.13 "For CP-18" (the S14 cause superseded for live days; the other causes and the runner's red line stand) | PASS | The other four causes are unchanged (`causes.ORDER` keeps all five for recorded evidence). The workflow is unchanged. |
| E4 | §24.14 "What stays exactly as registered" | PASS | C1, C2. |
| E5 | PUBLISH_RULES 1.5 A9 maintenance (claim layer, no second source, no hand-typed numbers) | PASS | A5. |

### Observations (not gaps)

- The deviation from the brief's exact pytest commands is `-p no:cacheprovider` and `--basetemp` in scratch, so that
  nothing is written in `W`. The counts are the brief's expected ones.
- 19 of the 20 skips are the Space build/render tests, which need local Space inputs that are absent here. The new
  row was checked in source and in the claim layer, not in a rendered page.
- The report's machine-hours and the ceilings ledger are the Lead's; I did not read that ledger. My own runs used
  about 0.9 machine-hours in all, summed over workers' wall time, with at most two concurrent workers.

## On FAIL only
- Single largest meaningful gap: n/a (PASS).
- Exact next acceptance test: n/a.
