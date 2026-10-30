# Verdict — CP-17c-probe — Integration — PASS

- Candidate SHA: 3bba29495db26de28a45a20ab05f09a1d3bcb313 (`gauntlet/cp-17c-probe`; base `main` =
  b903aefe239ff7db91784b4653d2da6ac47f57aa). Second Integration review; the first (FAIL at
  7ee1cf07a39f3cd7853a9687fc4b2e5788095079) is `docs/track-b/evidence/cp-17c-probe/integration-attempt-1.md`.
- Plan / version / bar: `capstone_v21.md`, v21-r18 (SHA-256
  `9caf83393a08df6851f7e829722583a142ebc2354ee99a3bbaa015d929f3d401` at the candidate), §24.12 "A1's freeze and
  4.7T's registered terms (v21-r18)" — section 268 lines, 22,423 bytes, SHA-256
  `33ec9b4221acbf9a26cafa3d3af323480dfb192a375fb436da16a6cb04647cba` (`bar.py bar … --at 3bba2949…`) — as the
  measurement standard: the issuing host, its resources and its runtime rule; with the Owner's decision 24
  (`docs/track-b/owner-decisions-2026-10-30.md`, SHA-256
  `1286548362b5618e3fb01c616d673c0af83dd79effeaf102bb9727ac219aabab`). Controlling brief:
  `docs/track-b/evidence/cp-17c-probe/issued-brief.md`, SHA-256
  `e0528d5c81ede078003cbc76ee4b7d8b0d3caa1a573b9f16ab3d95a3c2d4c3c1`.
- Verbatim bar excerpt (each block below appears byte for byte in `capstone_v21.md` at 3bba2949…; the excerpt is
  the citation, and any line number is a courtesy and non-binding):

> | The issuing host | Pyodide 0.28.0, by its 23 pinned file hashes, in the pinned Node.js v26.7.0 binary (`1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040`), one worker (decision 10). The chain's judgement and the shadow states run in CPython inside `cp17.daily`, from the package's own files, in the environment `uv.lock` pins |
> | The reference runtime (§19.3) | the issuing host, plus Chromium 153.0.8010.12 and WebKit 26.6 through Playwright 1.63.0, on the Apple M3 machine class (8 cores, 16 GB, macOS 26.5.2) |

and

> **"Frozen"** keeps §16.2's meaning. Any change to the policy, its code, its runtime or its state needs
> a new freeze and a new evaluation. Daily fitting changes weights and state within the frozen policy,
> and is not a change to it.

and

> 5. **Resources.** One worker under the issuing host, at most 15 minutes of wall time and 4 GB of peak
>    memory, measured in the attempt's own process. An issued artifact always carries its measurement
>    (N2).

and

>   - **where the pipeline runs.** The issuing host is the pinned files above. Any other binary or
>     machine is a runtime change, which needs a new freeze and a new evaluation (§16.2);

- Worktree clean before and after: yes — `git status --porcelain` empty and `HEAD` =
  3bba29495db26de28a45a20ab05f09a1d3bcb313 before and after (the only byproducts inside the worktree are git-ignored `__pycache__/` folders under `src/` and `tests/cp17cprobe/`).

**Summary.** The first review's gap is closed by its own acceptance test: `measurement.json`, `artifacts.json` and
`inputs.json` are byte-identical to 7ee1cf07's; the re-rendered `report.md` equals the committed one and gives every
job its own row with its own image version and CPython (macos-26: parity 20261013.0424.1 / 3.13.16, both shadow jobs
20261026.0455.2 / 3.13.17; ubuntu-24.04: 20261026.354.1 / 3.13.17 for all three); `proposals.md` states those
versions as measured and the setup range as 17–30 s; a new test fails when the hosts table omits a job (shown by a
negative control against 7ee1cf07's renderer). The measurement itself again reproduces completely from the runners'
downloaded zips, verified by their hashes: both runners are bit-identical to the frozen host on all 75 fits each
(re-derived independently over every fit), the buffers and the final state match, the local-control day reruns bit
for bit with the official binary, the inputs rebuild byte for byte, nothing frozen changed, and the scope and red
line hold. The CI-mode suite is green: every step exit 0, 2446 passed and 46 skipped.

**Disclosure (procedural, not about the candidate).** The assignment forbids opening the Claude memory directory.
Before the assignment had been generated, this session read one file in that directory (a note that does not concern
this checkpoint), and the harness loaded the directory's index into the session's context at start. Nothing from
either informed any check below; no file there was opened after the assignment was read, and none was edited.

## Commands actually run

All from the critic worktree `/Users/djourno/Downloads/PJM/.local/worktrees/cp-17c-probe/critic-2` (or with `git -C`
on it) unless stated; every output written under `/Users/djourno/Downloads/PJM/.local/artifacts/cp-17c-probe/critic-2/`
(below, `<C>`). Environment for every Python command: `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src CP17_PROJECT_ROOT=/Users/djourno/Downloads/PJM` and, for every fit and the
inputs rebuild, the five `*_NUM_THREADS=1`; Python `/Users/djourno/Downloads/PJM/.venv/bin/python` (3.13.15). No `gh`
command, no network call, no Git write in the project repository.

1. `git show main:scripts/gauntlet.py | python3 -I - critic-brief cp-17c-probe` (primary checkout) — exit 0; the
   assignment.
2. `git -C <worktree> status --porcelain` — exit 0, empty; `git rev-parse HEAD` — `3bba29495db26de28a45a20ab05f09a1d3bcb313`;
   `main` = `b903aefe239ff7db91784b4653d2da6ac47f57aa`, an ancestor of the candidate; 10 commits `b903aefe..3bba2949`.
3. `shasum -a 256 docs/track-b/evidence/cp-17c-probe/issued-brief.md capstone_v21.md docs/track-b/owner-decisions-2026-10-30.md`
   — `e0528d5c…c3c1`, `9caf8339…f401`, `12865483…abab`: equal to the hashes the brief and assignment name.
   `cmp .local/artifacts/cp-17c-probe/issued-brief.md <worktree>/docs/track-b/evidence/cp-17c-probe/issued-brief.md` —
   exit 0; `git show 7930f082 --stat` — the first candidate commit, parent `b903aefe`, adds only that file.
4. `git show main:scripts/bar.py | python3 -I - bar capstone_v21.md "### 24.12 A1's freeze and 4.7T's registered terms (v21-r18)" --at 3bba2949…`
   — exit 0; `plan capstone_v21.md at 3bba2949…: sha256 9caf8339…; section 268 lines, 22423 bytes, sha256 33ec9b42…`,
   equal to the generated assignment; the section printed equals the assignment's excerpt.
5. The first review's gap, by its acceptance test:
   - `git show 7ee1cf07:reports/cp17c-probe/<f> | shasum -a 256` against `3bba2949:` for `measurement.json`
     (`5b10bab6…`), `artifacts.json` (`22cb8e12…`), `inputs.json` (`26a2ba8e…`), `retrieval-local.json`,
     `scratch-repository.json` and the three `states/*.json` — all eight SAME.
   - `git diff --stat 7ee1cf07 3bba2949` — 6 files: `integration-attempt-1.md` (new, byte-equal to
     `.local/artifacts/cp-17c-probe/critic-1/integration.md` by `cmp`, committed alone in `ee438155`),
     `compute-ledger.jsonl` (+3 rows), `proposals.md`, `report.md`, `src/cp17cprobe/report.py` (`host_table` now one row
     per job), `tests/cp17cprobe/test_probe.py` (+2 tests). The whole repair diff read.
6. `python3 /Users/djourno/Downloads/PJM/.local/artifacts/cp-17c-probe/ci-runner.py critic2 3bba29495db26de28a45a20ab05f09a1d3bcb313 ci312`
   (read in full first) under `/usr/bin/time -l` — exit 0; 817.53 s real, 1,518,206,976 B peak. It `git archive`d the candidate into
   `.local/tmp/cp-17c-probe/critic2-ci312/` (one commit whose tree `30c3520b…` = `git rev-parse 3bba2949^{tree}`,
   made by the runner in that throwaway folder, not in the project repository), synced offline, ran with `CI=true`,
   Python 3.12.14 and the local inputs hidden, and removed the folder (`complete: true`, `scratch_removed: true`). Logs
   and `results.json` in `.local/artifacts/cp-17c-probe/critic2-validation/ci312/`. Steps: `uv sync --locked --dev` 0;
   `uv run python scripts/build_wasm_payload.py` 0; `uv run pytest -q` 0 — **2446 passed, 46 skipped** in 705.6 s
   (two more passing tests than the first review's 2444: the two new hosts-table tests), the probe's four
   local-material tests skipping with their stated reasons ("the reference runs are local material (CP-17b's
   .local/artifacts), absent on CI" ×3; "the downloaded runner results and the local control are local material,
   absent on CI" ×1); `uv run pytest tests/test_10_cqr_order_statistic.py -q` 0 (8 passed);
   `uv run python scripts/verify_release.py` 0 (PASS); `uv run pytest tests/test_22_wasm_equivalence.py -q` 0
   (15 passed); `python3 scripts/publication_guard.py tree` 0; and `uv run pytest --collect-only -m stress -q` 0
   (19 stress tests collected). The seven steps match `.github/workflows/tests.yml`.
7. The official binary, checked before use: `shasum -a 256 .local/tools/node-v26.7.0-official/dl/*` — `SHASUMS256.txt`
   `4533f0a4…fb2e` (2,943 bytes); tarball `7ee659a7…15d4` (57,622,243 bytes), equal to its line in `SHASUMS256.txt`
   (whose linux-x64 line is `bd6b6c31…28df`); `bin/node` `a9bd0630…71df`, 145,238,560 bytes, equal to
   `reports/cp17c-probe/retrieval-local.json`'s binary hash and bytes, and equal to the same member read straight from
   the tarball (`tar -xOzf … | shasum -a 256`); `node --version` `v26.7.0`. Homebrew's
   `/opt/homebrew/Cellar/node/26.7.0/bin/node` is still `1ef99ea2…d040`.
8. Local control: `python -m cp17cprobe.run parity --node /Users/djourno/Downloads/PJM/.local/tools/node-v26.7.0-official/node-v26.7.0-darwin-arm64/bin/node --pyodide /Users/djourno/Downloads/PJM/.local/tools/pyodide-0.28.0 --zip /Users/djourno/Downloads/PJM/.local/artifacts/cp-17b/bundle/src.zip --payloads /Users/djourno/Downloads/PJM/.local/artifacts/cp-17b/runs/native-parity/payloads --stems A1-2026-09-06 --out <C>/control`
   under `/usr/bin/time -l` — printed `A1-2026-09-06 ok 78.3s 686 MiB 4e6abb02fbb02aa8`; 79.44 s real, 719,667,200 B
   maximum resident set. (The exit code was not captured: the output was piped through `grep` in zsh. `parity`
   returns 0 exactly when every attempt's status is `ok`, and the recorded status is `ok`.)
   - The attempt: status `ok`; resources `wall_seconds 78.315`, `peak_bytes 719,667,200` (686 MiB), limits 900 s and
     4 GiB; errors `[]`; refused requests `[]`; `node_execpath` the official binary.
   - Quantiles SHA-256 `4e6abb02fbb02aa8ef202207f21b76bc33b34c37d025a0a93a491135ea43cea5` = `reports/cp17b/host-parity.json`'s
     `issued_quantiles_sha256` for `A1-2026-09-06`; payload `63ce7f45…43a4` = the reference's.
   - `cp17.retrain.compare('A1', reference, mine)` against
     `.local/artifacts/cp-17b/runs/host-parity/nodes/node-A1-2026-09-06.json` (SHA-256 `8e23a17e…4129`, as
     `inputs.json` binds it) — `identical bit for bit`, `selections_match True`, `bitwise_equal True`,
     `max_abs_eur 0.0`, payload equal; and independently the 24×7 float64 arrays are byte-equal.
9. The runners' zips: a short script (`python -I`) read each of the 10 zips under
   `.local/artifacts/cp-17c-probe/downloads/`, checked its SHA-256 against `artifacts.json`'s `zip_sha256` and GitHub's
   `digest` (10/10 equal), copied it to `<C>/downloads/<run id>/<artifact>.zip` (rehashed, 10/10 equal), ran
   `zipfile.testzip()` (no bad member), refused absolute or `..` member paths (none), and unpacked it beside its zip.
   The Lead's unpacked folders were not used.
10. `python -m cp17cprobe.compare compare --inputs reports/cp17c-probe/inputs.json --artifacts reports/cp17c-probe/artifacts.json --downloads <C>/downloads --local /Users/djourno/Downloads/PJM/.local/artifacts/cp-17c-probe/runs/local-control --retrieval reports/cp17c-probe/retrieval-local.json --out <C>/measurement.json`
    — exit 0; printed `macos-26 fits 75 bit-identical 75 ceilings True shadow days 14 buffers True max wall 228.920186916`,
    `ubuntu-24.04 fits 75 bit-identical 75 ceilings True shadow days 14 buffers True max wall 284.567728198`,
    `local-control fits 19 bit-identical 19 ceilings True shadow days 0 buffers None max wall 153.32…`.
    `cmp <C>/measurement.json reports/cp17c-probe/measurement.json` — exit 0 (byte-equal); equal as JSON too.
11. Independent re-derivation, `<C>/independent_check.py` (`python -I`; standard library and NumPy only, no
    `cp17cprobe` import; output `<C>/independent-check.json`) — exit 0. Over every fit of the six measured jobs, not a
    sample:
    - each job's `results-sha256.txt` rechecked file by file (28, 33, 41 files per macOS job; 28, 33, 41 per Linux
      job): none differs, none on disk unlisted;
    - each reference record rehashed against `inputs.json`'s `record_sha256` (75/75 per runner); its quantile hash
      matched to a committed CP-17b report where one records it (`host-parity.json` for the parity stems and for A1 on
      2026-08-31…09-06, `partial-days.json` for F1's four, `reports/cp17b/shadow-run.json`'s `host.days.<day>.shadows`
      for v4, v2, B0): 68/75 per runner bound, 0 contradicted;
    - `python.result.quantiles` of each runner record against the reference record's, as float64 bytes:
      **ubuntu-24.04 75/75 byte-equal, macos-26 75/75 byte-equal, largest difference 0.0**; each record's quantiles
      hash recomputed from its own array equals its claim (75/75); payload identity equal (75/75); errors 0; executed
      files equal the freeze manifest's (75/75); every attempt ≤ 900 s and ≤ 4 GiB (longest 284.57 s Linux,
      228.92 s macOS; largest peak 885,088,256 B Linux, 961,953,792 B macOS);
    - every shadow day's buffers in each runner's `shadow.json` against the reference source record
      `.local/artifacts/cp-17b/runs/shadow-host/shadow-run.json` (SHA-256 `ccbb681e…48e5`, equal to the source the
      committed `reports/cp17b/shadow-run.json` cites), `days.<day>.buffers.<policy>.sha256`: 42/42 per runner
      (14 days × v4, v2, B0);
    - per job, from `host.json`, `node-retrieval.json` and `project-sha256.txt`: label, image, OS, CPU, cores, memory,
      CPython, NumPy 2.4.6, `GITHUB_SHA` `ff458082…` (all six), the binary equal to the one retrieved, the tarball
      equal to its `SHASUMS256.txt` line, `SHASUMS256.txt` = `4533f0a4…`, Pyodide's 23 files equal to the freeze
      manifest (recomputed), `uv.lock` and `pyproject.toml` equal to the candidate's, `inputs-verified` true.
    - The stitch: both runners' early shadow job's `final-state.json` hashes to `43709563…31e2`, equal to
      `reports/cp17c-probe/states/start-2026-08-30.json`, the late job's start; both late jobs' final digests equal
      the reference source's `final.buffers_sha256` (B0 `cb08e92c…`, v2 `d2def77c…`, v4 `0f79714e…`).
12. Both local-control folders (`runs/local-control/`, `runs/local-control-first/`), against the references by float64
    bytes (a short script): 19/19 and 19/19, both with the official binary; the local control's `host.json` binary
    `a9bd0630…`, CPython 3.13.15.
13. `python -m cp17cprobe.report --measurement reports/cp17c-probe/measurement.json --proposals reports/cp17c-probe/proposals.md --out <C>/report.md`
    — exit 0; `cmp` with `reports/cp17c-probe/report.md` — exit 0 (byte-equal). Rendering from `<C>/measurement.json`
    instead — also byte-equal.
14. `python -m cp17cprobe.inputs --project /Users/djourno/Downloads/PJM --out <C>/scratch --record <C>/inputs.json`
    under `/usr/bin/time -l` — exit 0; printed `271 files 180651424 bytes; largest 13258840 ; dry replay True`;
    25.41 s real, 1,610,989,568 B peak. `cmp <C>/inputs.json reports/cp17c-probe/inputs.json` — exit 0 (dry replay true
    at all 14 origins, 2026-08-24…09-06); `<C>/scratch/inputs-files.json` byte-equal to
    `git -C .local/tmp/cp-17c-probe/scratch show ff458082:inputs-files.json`; the three `states/*.json` byte-equal to the
    committed ones; the whole rebuilt tree identical to `git -C .local/tmp/cp-17c-probe/scratch archive ff458082`
    (`diff -rq`, exit 0). The scratch clone's log: `ff458082` (runs 2 and 3) on `e7b99a45` (run 1), as
    `scratch-repository.json` and `artifacts.json` record.
15. `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17b/freeze-manifest.json` — exit 0, output
    `verified` (no problem, no unchecked file); 2.42 s. The manifest's SHA-256 is `1fe07bdd…5502`, as §24.12 records.
16. Scope: `git diff --name-only b903aefe 3bba2949` — 21 paths, none outside `src/cp17cprobe/`, `tests/cp17cprobe/`,
    `reports/cp17c-probe/`, `docs/track-b/evidence/cp-17c-probe/`; `--diff-filter=DMRTC` — empty (all added);
    `git ls-tree -r -l 3bba2949 | awk '$4>52428800'` — empty (largest new file `reports/cp17c-probe/measurement.json`,
    283,342 B); `git diff --stat` on `.github`, `src/cp17`, `src/delu_forecast`, `src/cp15`…`src/cp28`, `data`,
    `pyproject.toml`, `uv.lock`, `capstone_v21.md`, `AGENTS.md`, `CLAUDE.md`, the role files, `docs/PUBLISH_RULES.md`,
    the backup register, the exposure ledger and `.claude` — empty; no earlier `reports/` path touched.
17. Red-line scan (`python -I`) of all 21 new files for any date after 2026-09-06, ISO and 8-digit forms. Found only:
    the brief's issue date 2026-10-30 and the decisions file's name; S_14's protocol date 2027-01-06; GitHub run and
    job timestamps 2026-10-29/30 in `artifacts.json` and `scratch-repository.json`; the runner image versions
    `20261013.0424.1`, `20261026.0455.2`, `20261026.354.1`; the CP-26 folder name `cold-rerun-2026-10-15`; the
    retrieval date 2026-10-30 (`retrieval-local.json`, `measurement.json`, a comment in `run.py`); and the same items
    quoted in `integration-attempt-1.md`. (`uv`'s build date in the records is 2026-08-25, before the boundary.) No
    delivery day: the shipped payloads are 201 files over 17 days, 2025-10-26 … 2026-09-06; `truth.json` covers
    2026-08-22 … 2026-09-04 (336 keys); the state files' day keys end 2026-08-24 and 2026-08-29.
18. Records against the proposals (`python -I`, from `artifacts.json`, the unpacked `node-retrieval.json` and
    `uv-retrieval.json`, `measurement.json`, `reports/cp17b/host-parity.json` and
    `reports/rebaseline/cold-rerun-2026-10-15/cost-projection.json`): minutes per job and total (863); setup per job;
    chain-step seconds; Node.js retrieval seconds per job (0.338–0.868); each uv wheel's hash equal to the installed
    one (10/10); parity wall-ratio medians (1.695 Linux, 1.204 macOS); A1's fit/native ratios in `host-parity.json`
    (3.27–5.61, median 4.59); S_13's 813 fits and 5,079.07 s, nominal searches 3–13 at 3,376–5,079 s, cold margin 2.0.
19. `python -m pytest tests/cp17cprobe -q -rs -p no:cacheprovider --basetemp=<C>/pytest-local` (with the local
    references present) — exit 0, `23 passed in 2.75s`.
20. Negative control for the new tests, `<C>/negative/run_negative.py` (`python -I`, sys.path set explicitly): the two
    new tests and the report-render test, run against 7ee1cf07's `report.py` (copied with the candidate's other
    `cp17cprobe` files into `<C>/negative/src/`) — **all three FAILED** (`AssertionError`); against the candidate's
    `report.py` — all three PASSED. (A first attempt through `pytest` with `PYTHONPATH=<C>/negative/src:src` reported "3 passed",
    so it evidently imported the candidate's `report.py`, not the old one; it is discarded, and the explicit run above
    is the control.)
21. `brew list --pinned` — `node` (read only); `/opt/homebrew/Cellar/node/` holds `26.7.0` only.
22. `git -C <worktree> status --porcelain` and `rev-parse HEAD` after the review — exit 0, empty; `3bba29495db26de28a45a20ab05f09a1d3bcb313`.
23. `git show main:scripts/bar.py | python3 -I - check <C>/integration.md --source capstone_v21.md@3bba2949…` (this
    verdict's four quote blocks) — exit 0, `ok` for each of the four blocks.

## Evidence actually inspected

- The candidate's whole diff list; every new source file read in full: `src/cp17cprobe/run.py`, `compare.py`,
  `inputs.py`, `report.py`, `probe.yml`; `tests/cp17cprobe/test_probe.py`, `fake_node.py`; and the repair diff
  `7ee1cf07..3bba2949` in full.
- `reports/cp17c-probe/`: `report.md` (whole), `proposals.md` (as rendered in it, and its diff), `measurement.json`
  (per-job hosts, summaries, minutes), `artifacts.json` (runs, jobs, steps, artifacts, billable), `inputs.json`,
  `retrieval-local.json`, `scratch-repository.json`, `compute-ledger.jsonl`, `states/`.
- `docs/track-b/evidence/cp-17c-probe/issued-brief.md` and `integration-attempt-1.md` (whole).
- The 10 downloaded zips and their unpacked contents in `<C>/downloads/` (`host.json`, `node-retrieval.json`,
  `uv-retrieval.json`, `project-sha256.txt`, `inputs-verified.json`, `parity.json`, `shadow.json`, `final-state.json`,
  every `run.json`, `results-sha256.txt`).
- References: `reports/cp17b/host-parity.json`, `partial-days.json`, `shadow-run.json`; the local source
  `.local/artifacts/cp-17b/runs/shadow-host/shadow-run.json`; every reference run record the comparison uses.
- `reports/rebaseline/cold-rerun-2026-10-15/cost-projection.json` (`searches`, `historical_search_cost_basis`).
- `src/cp17/daily.py` (`NODE`, `Host.__init__`), `src/cp17/tools/hosts.py` (`NODE`, `NODE_SHA256`, the Pyodide
  defaults), `src/cp17/tools/refreeze.py` (k13 from the local `evidence/cp-26` extract), `src/cp17/dailyfit.py`
  (`array_hash`).
- `docs/track-b/owner-decisions-2026-10-30.md` decisions 23–24; `.github/workflows/tests.yml` (the seven steps,
  Python 3.12); the CI runner `.local/artifacts/cp-17c-probe/ci-runner.py`, read before running it.
- Not used: the Lead's unpacked download folders, `critic-assignment*.md`, `return-draft.md`, the Lead's logs and any
  Lead narrative.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| G1 | The first review's gap, by its acceptance test: the three records byte-identical to 7ee1cf07's; `report.md` re-rendered from them showing every job's image and CPython per runner; `proposals.md` as measured, setup 17–30 s; a test that fails if the hosts table omits a job; `tests/cp17cprobe` and the CI-mode suite green | PASS | Command 5 (all three records, and five more, SAME); command 13 (re-render byte-equal); the hosts table rows: macos-26-parity `macos26 20261013.0424.1` / 3.13.16, macos-26-shadow-early and -late `macos26 20261026.0455.2` / 3.13.17, ubuntu-24.04 ×3 `ubuntu24 20261026.354.1` / 3.13.17, local control 3.13.15 — each equal to that job's `host.json` (command 11); `proposals.md`: "two runner images … (the parity job, CPython 3.13.16) … (both shadow jobs, CPython 3.13.17)", "3.13.17 (every Linux job and both macOS shadow jobs) and 3.13.16 (the macOS parity job)", "17–30 s in the measured runs" (measured runs' setups 20, 20, 30, 19, 18, 17 s); `test_hosts_table_names_every_job_with_its_own_image_and_cpython` and `test_hosts_table_would_catch_a_missing_job` fail against 7ee1cf07's renderer and pass on the candidate (command 20); command 19; command 6 |
| G2 | The first review's other findings | PASS | Four external statements now labelled "GitHub's published terms, not measured or recorded by this probe" / "by GitHub's published terms and not by any record here" / "GitHub's published limit, not a record of this probe"; "Linux's standard fleet is GitHub's largest" removed. Approximations replaced by records: retrieval "0.34–0.87 s per job" = 0.338–0.868 s over all 10 jobs' `node-retrieval.json`; Pyodide "44,962,352 bytes, … largest 13,258,840" = `inputs.json`. Observations addressed: the seven A1 references bound by payload identity only are stated in the result; `compute-ledger.jsonl` now carries the b18cf4bd and 7ee1cf07 CI runs and the first Critic (total 4,807.9 s = 1.34 machine-hours, as the assignment says) |
| O1a | Runner measurement: a standard GitHub-hosted Linux x64 runner and a standard macOS Apple-silicon runner, each named by its image label | PASS | `ubuntu-24.04` (RUNNER_ARCH X64, ImageOS ubuntu24) and `macos-26` (ARM64, ImageOS macos26): standard labels in `probe.yml`, every job's `host.json` and `artifacts.json` labels |
| O1b | … with its image version, CPU, cores and memory recorded | PASS | Per job, in `measurement.json` and now in the report's hosts table: ubuntu-24.04 — 20261026.354.1, AMD EPYC 7763 64-Core, 2 cores, 8,317,935,616 B (7.7 GiB), Ubuntu 24.04.5 LTS, ×3; macos-26 — parity 20261013.0424.1, shadow ×2 20261026.0455.2, Apple M2 Pro (Virtual), 5 cores, 15,032,385,536 B (14.0 GiB), macOS 26.6.2 (command 11) |
| O1c | What runs: `cp17.daily` with the frozen package, the pinned Pyodide files, the official Node.js v26.7.0 binary for the platform; CPython in the environment `uv.lock` pins | PASS | `run.py` calls `cp17.daily.Host(...).run` and `cp17.daily.issue_day` with `node=` passed in, judged by `cp17.issue.attempt`; executed files equal the freeze manifest 75/75 per runner; Pyodide's 23 files equal the manifest on every job (recomputed); binaries `ad19784f…` (linux-x64) and `a9bd0630…` (darwin-arm64), each tarball equal to its `SHASUMS256.txt` line, `SHASUMS256.txt` pinned `4533f0a4…`; `uv sync --locked`, every job's `uv.lock` `5d2aecc3…` and `pyproject.toml` equal to the candidate's; NumPy 2.4.6 |
| O1d | The days, in the brief's priority | PASS | No subset was needed: on both runners all 15 parity stems of `host-parity.json`, F1's four, and all 14 shadow days with A1 and the three shadows (75 fits each) |
| O1e | Recorded per runner, day and policy: bit identity by SHA-256; if not, the largest difference per quantile and the selections; the buffers' SHA-256; wall time and peak memory against 15 min and 4 GB; the payload identity | PASS | `measurement.json` fit rows carry `bit_identical`, `status`, `max_abs_eur(_by_level)`, `selections_match`, `wall_seconds`, `peak_bytes`, `within_ceilings`, `payload_identity_equal`; shadow days carry `buffers_equal_reference` and `buffers_equal_payload`. Recomputed byte-equal (command 10), re-derived independently (command 11): 75/75 bit-identical per runner, 42/42 buffers, all within ceilings, stitch and final state equal |
| O2 | Local control: the official darwin-arm64 binary on the parity origins and F1's day | PASS | `measurement.json` `local_control`: 19/19 bit-identical, binary `a9bd0630…` ≠ Homebrew's `1ef99ea2…`; my rerun of A1-2026-09-06 bit-identical (command 8); both local runs 19/19 by bytes (command 12) |
| O3a | Proposal: which runner passes cleanly, compared on time, memory, stability | PASS | Both pass; figures checked against the records: one issuance 349.4–366.2 s Linux, 269.9–283.9 s macOS, 197.1–212.2 s M3; 284.6 s = 31.6% of 900 s; A1 2025-10-26 146.8 s (EPYC 9V45, run 1) vs 284.6 s (EPYC 7763); largest peak 961,953,792 B = 0.90 GiB < 0.92; 2 vCPU / 7.7 GiB and 5 cores / 14 GiB; "one Linux image, two macOS images" now true. External statements are labelled as GitHub's published terms (G2) |
| O3b | Proposal: what CP-17c must re-freeze — binary and retrieval, host identity, where `refreeze verify` runs, the runtime check before issuing | PASS | Tarball 62,014,253 B `bd6b6c31…`, `bin/node` 147,870,928 B `ad19784f…`, `SHASUMS256.txt` 2,943 B `4533f0a4…`, darwin-arm64 57,622,243 B `7ee659a7…` / `a9bd0630…` — all the records'; Pyodide 44,962,352 B, largest 13,258,840 B; CPython versions as measured; `cp17.daily.NODE` and `cp17.tools.hosts.NODE` = Homebrew's path, `.local/tools/pyodide-0.28.0` defaults and k13 from the local `evidence/cp-26` extract confirmed in `src/cp17/`; canary A1 2026-09-06 `4e6abb02…` 137.3 s Linux / 98.8 s macOS, B0 2026-09-06 `b12a9972…` 7.1 / 12.3 s — the tables'. One unlabelled external statement (observation 1) |
| O3c | Proposal: daily cost per issuance and for decision 23's four | PASS | From 30 s setup (the measured maximum), 366/284 s per issuance and 137/99 s canary: 533 s ≈ 9 and 413 s ≈ 7 job-minutes; ×10 macOS = 70; four issuances 1,631 s ≈ 27 and 1,265 s ≈ 21; ×10 = 210; ×30 = 270 and 2,100. Chain steps per shadow day 274.8 (1,649/6) – 279.0 (2,232/8) s Linux, 151.0 (906/6) – 154.75 (1,238/8) s macOS (`artifacts.json`); two at once: 30 + 4×279 + 137 = 1,283 s ≈ 21 job-minutes; 566.6 s maximum day sum; decision 23 states "a run takes at most about an hour" |
| O3d | Proposal: estimate of S_14 against hosted job limits | PASS | S_13 813 fits, 5,079.07 s; nominal searches 3–13 3,376–5,079 s; cold margin 2.0 (`cost-projection.json`); A1 fit/native 3.27–5.61, median 4.59 (`host-parity.json`); parity wall-ratio medians 1.695 / 1.204 (`measurement.json`); the table's eight cells reproduce (2.38, 2.38, 1.70, 0.85 h natively; ×4.59 → 10.9, 10.9, 7.8, 3.9 h). The 6-hour limit is labelled as GitHub's published limit, untested |
| O4 | If no runner reproduces, PASS with the numbers; BLOCKED only if unmeasurable | N/A | Both runners reproduced |
| F1 | Development data only; no delivery day after 2026-09-06 read | PASS | Command 17; `inputs.py` refuses any payload day after 2026-09-06 (`BOUNDARY`); the rebuilt inputs equal the shipped tree (command 14) |
| F2 | Retrieval software only, recorded with URL, version, bytes, SHA-256 | PASS (observation 2) | Node.js `SHASUMS256.txt` and both tarballs, and the uv wheels, each with URL, version, bytes and SHA-256 per job (`node-retrieval.json`, `uv-retrieval.json`; the wheel hash equal to the installed one, 10/10) and for this Mac (`retrieval-local.json`, rehashed in command 7); Pyodide uploaded through the scratch repository and verified by the manifest's hashes; the Python packages by `uv.lock` `5d2aecc3…`; actions pinned by commit SHA |
| F3a | No committed file over 50 MB | PASS | Command 16; `test_inputs_fit_a_github_repository` |
| F3b | The workflow's seven steps green on a history-free single-commit copy, `CI=true`, Python 3.12 | PASS | Command 6 |
| F3c | Tests needing the runtimes or GitHub skip with a stated reason; timing-sensitive tests carry `stress` | PASS | `need_reference()` and the measurement test skip with stated reasons when `.local` material is absent (command 6); no probe test is timing-sensitive; locally, with the references present, 23 passed (command 19) |
| F4 | No pinned file and no landed code changes; new paths only; nothing under `.github/` | PASS | Command 16: 21 added files, none modified or deleted, none under `.github/` or any protected path; `refreeze verify` `verified` (command 15) |
| F5 | The Critic reruns one local-control day, the whole suite in CI mode, and recomputes every comparison from the downloads, verified by their hashes; runs nothing on GitHub | PASS (performed) | Commands 6, 8–14; no `gh`, no network |
| C1 | Red line (§24.2) | PASS | Command 17 |
| C2 | Files that never change | PASS | Commands 15–16 |
| C3 | Homebrew's `node` stays pinned and installed | PASS | Command 21; binary still `1ef99ea2…` (command 7) |
| C4 | Credentials and telemetry: no secret anywhere; telemetry off | PASS (from records) | `probe.yml` references no `secrets.`, `permissions: contents: read` with no job-level override, `persist-credentials: false`, `MLFLOW_DISABLE_TELEMETRY`/`DO_NOT_TRACK` set; `scratch-repository.json`: private, 0 secrets, 0 variables, default workflow permissions `read` (a record; not re-read online, as item 5 forbids) |
| C5 | Tools: `gauntlet.py start`, the worktree, one focused Critic through `critic-open`/`critic-brief`/`critic-close`, `return` | PASS so far | This review was opened by `critic-open` (worktree present, clean, at the candidate) and briefed by `critic-brief`; `critic-close` and `return` follow this verdict |
| C6 | Memory directory untouched; Owner-facing Git commands non-interactive | N/A to the candidate | Nothing in the candidate touches either (see the disclosure above about this session) |
| X1 | Workflow: GitHub's own actions only, pinned by commit SHA; `contents: read`; no secret; standard labels; minute limits | PASS | `actions/checkout@3d3c42e5…`, `actions/setup-python@5fda3b95…`, `actions/upload-artifact@cf430e03…` (40 hex each); step limits below job limits; worst case of the defaults 235 + 124×10 = 1,475 ≤ 1,500 |
| X2 | The minutes (863 counted, of 1,500) | PASS | Recomputed from `artifacts.json` job times, each rounded up, macOS ×10: run 1 6+7+5 + 7×10 = 88; run 2 38+29+38 + 29×10 = 395; run 3 (16+22)×10 = 380; total 863. GitHub's billable figures are 0 ms for every job, as the report says |
| X3 | Scratch repository and the runs it made | PASS | Rebuilt tree = `ff458082` (command 14); runs 2 and 3 at `ff458082`, run 1 at `e7b99a45`, per `artifacts.json`, `scratch-repository.json` and each measured job's `GITHUB_SHA`; the committed `run.py`, `__init__.py` and workflow are the shipped ones |
| X4 | Every figure in the proposals is the measurement's or a cited committed record's | PASS (observation 1) | Every figure checked in O3a–O3d traces to `measurement.json`, `artifacts.json`, the job records, `inputs.json`, `host-parity.json` or `cost-projection.json`; GitHub's terms are labelled as such |

**Observations (not gaps):**
1. Proposal 2 says the image version and the CPU model "are GitHub's to change weekly". That cadence is not from any
   record and is not labelled as GitHub's published terms. The records show two macOS images 13 days apart and two
   Linux CPU models, which is consistent with the advice (record, do not pin) but does not establish "weekly". The
   10× macOS rate is GitHub's, applied as the brief's counting rule.
2. `actions/setup-python` takes CPython "3.13" from GitHub's toolcache or its own download, recorded by version only
   (3.13.16 / 3.13.17), not by URL, bytes or hash (carried from the first review). Proposal 2 already asks CP-17c to
   pin one patch version.
3. Seven reference fits per runner (A1, 2026-08-24 … 08-30) are bound to CP-17b by payload identity and executed files
   only; the result now says so.
4. `compute-ledger.jsonl` omits the Lead's CI run at this candidate (about 0.17 machine-hours, as the assignment
   states) and this review.
5. The CI runner (`ci-runner.py`), as assigned, makes one throwaway commit in its own new repository under
   `.local/tmp/cp-17c-probe/critic2-ci312/` (removed afterwards) and rewrites `.local/artifacts/cp-17c-probe/history-free-message.txt`
   with its fixed text. No Git write touched the project repository.

**Critic's own compute:** about 0.27 machine-hours (CI-mode suite 817.5 s, local-control fit 79.4 s, inputs rebuild 25.4 s,
the comparison, re-renders, freeze check, tests, negative control, scans and independent checks about 40 s); at most
2 concurrent workers (the control fit, the inputs rebuild and the checks overlapped the CI run); largest single peak
1.61 GB (the inputs rebuild); within the 1.0 machine-hour, 4-worker and 12 GB limits. With the ledger's 1.34 and the
Lead's CI run at this candidate (about 0.17), the probe's local use is about 1.8 of its 3 machine-hours.

## On FAIL only

Not applicable (PASS).
