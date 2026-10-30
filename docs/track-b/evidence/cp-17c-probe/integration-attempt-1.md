# Verdict — CP-17c-probe — Integration — FAIL

- Candidate SHA: 7ee1cf07a39f3cd7853a9687fc4b2e5788095079 (`gauntlet/cp-17c-probe`; base `main` =
  b903aefe239ff7db91784b4653d2da6ac47f57aa)
- Plan / version / bar: `capstone_v21.md`, v21-r18 (SHA-256
  `9caf83393a08df6851f7e829722583a142ebc2354ee99a3bbaa015d929f3d401` at the candidate), §24.12 "A1's freeze and
  4.7T's registered terms (v21-r18)" — section 268 lines, 22,423 bytes, SHA-256
  `33ec9b4221acbf9a26cafa3d3af323480dfb192a375fb436da16a6cb04647cba` (`bar.py bar … --at 7ee1cf07…`) — as the
  measurement standard: the issuing host, its resources and its runtime rule; with the Owner's decision 24
  (`docs/track-b/owner-decisions-2026-10-30.md`, SHA-256
  `1286548362b5618e3fb01c616d673c0af83dd79effeaf102bb9727ac219aabab`). Controlling brief:
  `docs/track-b/evidence/cp-17c-probe/issued-brief.md`, SHA-256
  `e0528d5c81ede078003cbc76ee4b7d8b0d3caa1a573b9f16ab3d95a3c2d4c3c1`.
- Verbatim bar excerpt (each block below appears byte for byte in `capstone_v21.md` at 7ee1cf07…; the excerpt is
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

- Worktree clean before and after: yes — `git status --porcelain` empty and `HEAD` = 7ee1cf07a39f3cd7853a9687fc4b2e5788095079 before and after; the only byproducts inside the worktree are git-ignored `__pycache__/` folders under `src/`.

**Summary.** The measurement itself reproduces completely: every comparison recomputes byte for byte from the
runners' downloaded zips, both runners are bit-identical to the frozen host on all 75 fits each (re-derived
independently, not only through `compare.py`), the buffers and final states match, the local-control day reruns
bit for bit, the inputs rebuild byte for byte, nothing frozen changed, and the scope and red line hold. The FAIL
is confined to the committed report's statement of the `macos-26` host identity, which contradicts the committed
measurement on an item the brief makes a recorded deliverable (image version per runner); see "On FAIL only".

## Commands actually run

All from the critic worktree `/Users/djourno/Downloads/PJM/.local/worktrees/cp-17c-probe/critic-1` (or with
`git -C` on it) unless stated; every output written under
`/Users/djourno/Downloads/PJM/.local/artifacts/cp-17c-probe/critic-1/` (below, `<C>`). Environment for every Python
command: `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src
CP17_PROJECT_ROOT=/Users/djourno/Downloads/PJM` and the five `*_NUM_THREADS=1`; Python
`/Users/djourno/Downloads/PJM/.venv/bin/python` (3.13.15). No `gh` command, no network call, no Git write in the
project repository.

1. `git show main:scripts/gauntlet.py | python3 -I - critic-brief cp-17c-probe` (primary checkout) — exit 0; the
   assignment above.
2. `git -C <worktree> status --porcelain` — exit 0, empty; `git rev-parse HEAD` — `7ee1cf07a39f3cd7853a9687fc4b2e5788095079`.
3. `shasum -a 256 docs/track-b/evidence/cp-17c-probe/issued-brief.md capstone_v21.md docs/track-b/owner-decisions-2026-10-30.md`
   — `e0528d5c…c1`, `9caf8339…01`, `12865483…ab`: all three equal the hashes the brief and assignment name.
4. `cmp .local/artifacts/cp-17c-probe/issued-brief.md <worktree>/docs/track-b/evidence/cp-17c-probe/issued-brief.md`
   — exit 0 (byte-equal to the canonical brief); `git show 7930f082 --stat` — the first candidate commit, parent
   `b903aefe`, adds only that file.
5. `git diff --name-only b903aefe 7ee1cf07…` — exit 0, 20 paths, all under `src/cp17cprobe/`, `tests/cp17cprobe/`,
   `reports/cp17c-probe/`, `docs/track-b/evidence/cp-17c-probe/`; `git diff --name-only --diff-filter=DMRT b903aefe
   7ee1cf07…` — empty (no modified, deleted, renamed or retyped file); `git ls-tree -r -l 7ee1cf07 | awk '$4>52428800'`
   — empty (largest new file `reports/cp17c-probe/measurement.json`, 283,342 bytes); `git diff b903aefe 7ee1cf07 --
   capstone_v21.md` — empty.
6. `git show main:scripts/bar.py | python3 -I - bar capstone_v21.md "### 24.12 A1's freeze and 4.7T's registered
   terms (v21-r18)" --at 7ee1cf07…` — exit 0; `plan capstone_v21.md at 7ee1cf07…: sha256 9caf8339…; section 268
   lines, 22423 bytes, sha256 33ec9b42…` (equal to the generated assignment).
7. `bar.py check issued-brief.md --source capstone_v21.md@7ee1cf07… --source docs/track-b/owner-decisions-2026-10-30.md@7ee1cf07…`
   — exit 1: the brief joins non-contiguous extracts into one quote block with blank `>` lines. Split at those lines,
   each of its five chunks was found verbatim (a short script): the four §24.12 chunks in `capstone_v21.md` at both
   `782a1979` and `7ee1cf07`, decision 24 in `owner-decisions-2026-10-30.md` at `7ee1cf07`. Form only; not a defect
   of the candidate's content.
8. `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17b/freeze-manifest.json` — exit 0, output
   `verified` (no problem, no unchecked file); the manifest's SHA-256 is `1fe07bdd…5502`, as §24.12 records. Run twice
   (once under `/usr/bin/time`: 3.65 s, 252 MB).
9. `python3 /Users/djourno/Downloads/PJM/.local/artifacts/cp-17c-probe/ci-runner.py critic 7ee1cf07a39f3cd7853a9687fc4b2e5788095079 ci312`
    (read in full first) under `/usr/bin/time -l` — exit 0; 714.6 s real, 1.27 GB peak. It `git archive`d the candidate
    into `.local/tmp/cp-17c-probe/critic-ci312/` (tree `d290953e…` = the candidate's tree, one commit, made by the
    runner in that throwaway folder, not in the project repository), synced offline, ran with `CI=true`, Python
    3.12.14 and the local inputs hidden, and removed the folder (`scratch_removed: true`). Logs and `results.json` in
    `.local/artifacts/cp-17c-probe/critic-validation/ci312/`. Steps:
    `uv sync --locked --dev` 0; `uv run python scripts/build_wasm_payload.py` 0; `uv run pytest -q` 0 —
    **2444 passed, 46 skipped** in 597.6 s, the probe's four local-material tests skipping with their stated reasons
    ("the reference runs are local material (CP-17b's .local/artifacts), absent on CI" ×3; "the downloaded runner
    results and the local control are local material, absent on CI" ×1); `uv run pytest tests/test_10_cqr_order_statistic.py -q`
    0 (8 passed); `uv run python scripts/verify_release.py` 0 (PASS); `uv run pytest tests/test_22_wasm_equivalence.py -q`
    0 (15 passed); `python3 scripts/publication_guard.py tree` 0; and `uv run pytest --collect-only -m stress -q` 0
    (19 stress tests collected). The seven steps match `.github/workflows/tests.yml`.
10. The official binary, checked before use: `shasum -a 256 .local/tools/node-v26.7.0-official/dl/*` —
    `SHASUMS256.txt` `4533f0a4…2fb2e` (2,943 bytes); tarball `7ee659a7…15d4`, equal to its line in `SHASUMS256.txt`;
    `bin/node` `a9bd0630…71df`, equal to `reports/cp17c-probe/retrieval-local.json`'s binary hash, and equal to the
    same member read straight from the tarball (`tar -xOzf … bin/node | shasum -a 256`); `node --version` `v26.7.0`.
    Homebrew's `/opt/homebrew/Cellar/node/26.7.0/bin/node` is still `1ef99ea2…d040`.
11. Local control: `python -m cp17cprobe.run parity --node /Users/djourno/Downloads/PJM/.local/tools/node-v26.7.0-official/node-v26.7.0-darwin-arm64/bin/node --pyodide /Users/djourno/Downloads/PJM/.local/tools/pyodide-0.28.0 --zip /Users/djourno/Downloads/PJM/.local/artifacts/cp-17b/bundle/src.zip --payloads /Users/djourno/Downloads/PJM/.local/artifacts/cp-17b/runs/native-parity/payloads --stems A1-2026-09-06 --out <C>/control`
    under `/usr/bin/time -l` — exit 0; printed `A1-2026-09-06 ok 93.1s 682 MiB 4e6abb02fbb02aa8`; 93.77 s real.
    - The attempt: status `ok`, resources `wall_seconds 93.136`, `peak_bytes 716,062,720` (683 MiB), limits 900 s and
      4 GiB; `node_execpath` the official binary.
    - Quantiles SHA-256 `4e6abb02fbb02aa8ef202207f21b76bc33b34c37d025a0a93a491135ea43cea5` = `reports/cp17b/host-parity.json`'s
      `issued_quantiles_sha256` for `A1-2026-09-06`; payload `63ce7f45…43a4` = the reference's.
    - `cp17.retrain.compare('A1', reference, mine)` against
      `.local/artifacts/cp-17b/runs/host-parity/nodes/node-A1-2026-09-06.json` (SHA-256 `8e23a17e…4129`, as
      `inputs.json` binds it) — status `identical bit for bit`, `selections_match True`, `bitwise_equal True`,
      `max_abs_eur 0.0`; and independently, the 24×7 float64 quantile arrays are byte-equal.
12. The runners' zips: a short script read each of the 10 zips under `.local/artifacts/cp-17c-probe/downloads/`,
    checked its SHA-256 against `artifacts.json`'s `zip_sha256` and GitHub's `digest` (all 10 equal), copied it to
    `<C>/downloads/<run id>/<artifact>.zip` (rehashed, equal), ran `zipfile.testzip()` (no bad member) and unpacked it
    beside its zip. The Lead's unpacked folders were not used.
13. `python -m cp17cprobe.compare compare --inputs reports/cp17c-probe/inputs.json --artifacts reports/cp17c-probe/artifacts.json --downloads <C>/downloads --local /Users/djourno/Downloads/PJM/.local/artifacts/cp-17c-probe/runs/local-control --retrieval reports/cp17c-probe/retrieval-local.json --out <C>/measurement.json`
    — exit 0; printed `macos-26 fits 75 bit-identical 75 ceilings True shadow days 14 buffers True max wall 228.92…`,
    `ubuntu-24.04 fits 75 bit-identical 75 ceilings True shadow days 14 buffers True max wall 284.57…`,
    `local-control fits 19 bit-identical 19 ceilings True …`. `cmp <C>/measurement.json reports/cp17c-probe/measurement.json`
    — byte-equal (and equal as JSON).
14. Independent re-derivation, `<C>/independent_check.py` (standard library and NumPy only, no `cp17cprobe` import;
    output `<C>/independent-check.json`) — exit 0. Over every fit of all six measured jobs, not a sample:
    - each job's `results-sha256.txt` rechecked file by file (28, 41, 33, 28, 41, 33 files; none differs, none on disk
      unlisted);
    - each reference record rehashed against `inputs.json`'s `record_sha256` (75/75 per runner), and its quantiles'
      SHA-256 recomputed and matched to a committed CP-17b report where one records it: `host-parity.json` (parity),
      `partial-days.json` (F1's four), `reports/cp17b/shadow-run.json` (v4, v2, B0 on the 14 shadow days), and
      `host-parity.json` again for A1 on 2026-08-31…09-06, whose payloads are the parity ones — 68/75 per runner bound,
      0 contradicted;
    - `python.result.quantiles` of each runner record against the reference record's, as float64 bytes:
      **ubuntu-24.04 75/75 byte-equal, macos-26 75/75 byte-equal, largest difference 0.0**; each record's own
      quantiles hash equals its claim (75/75); payload identity equal (75/75); errors 0; every attempt ≤ 900 s and
      ≤ 4 GiB (longest 284.57 s Linux, 228.92 s macOS; largest peak 885,088,256 B Linux, 961,953,792 B macOS);
    - every shadow day's buffers in each runner's `shadow.json` against the reference source record
      `.local/artifacts/cp-17b/runs/shadow-host/shadow-run.json` (SHA-256 `ccbb681e…48e5`, equal to the source the
      committed `reports/cp17b/shadow-run.json` cites), `days.<day>.buffers.<policy>.sha256`: 42/42 per runner
      (14 days × v4, v2, B0).
15. Run 1's superseded records (a short script over `<C>/downloads/40974770649/`): results hashes clean; 14/14 fits
    byte-equal to the references; CPUs 10 × AMD EPYC 9V45, 2 × AMD EPYC 7763, 2 × Apple M2 Pro (Virtual).
16. Both local-control folders (`runs/local-control/`, `runs/local-control-first/`), against the references by float64
    bytes: 19/19 and 19/19, both with the official binary.
17. `python -m cp17cprobe.report --measurement reports/cp17c-probe/measurement.json --proposals reports/cp17c-probe/proposals.md --out <C>/report.md`
    — exit 0; `cmp` with `reports/cp17c-probe/report.md` — byte-equal. Rendering from `<C>/measurement.json` instead
    — also byte-equal.
18. `python -m cp17cprobe.inputs --project /Users/djourno/Downloads/PJM --out <C>/scratch --record <C>/inputs.json`
    under `/usr/bin/time -l` — exit 0; printed `271 files 180651424 bytes; largest 13258840 ; dry replay True`;
    27.4 s, 1.32 GB peak. `<C>/inputs.json` byte-equal to the committed `reports/cp17c-probe/inputs.json` (dry replay
    true at all 14 origins); `<C>/scratch/inputs-files.json` byte-equal to
    `git -C .local/tmp/cp-17c-probe/scratch show ff458082:inputs-files.json`; the whole rebuilt tree identical to
    `git -C .local/tmp/cp-17c-probe/scratch archive ff458082` (`diff -rq`, no difference); the three `states/*.json`
    byte-equal to the committed ones. The scratch clone's log: `e7b99a45` (run 1) then `ff458082` (runs 2 and 3), as
    `scratch-repository.json` and `artifacts.json` record; each job's `GITHUB_SHA` agrees.
19. Red-line scan of all 20 new files for any date after 2026-09-06 (ISO and 8-digit forms). Found only: the brief's
    issue date 2026-10-30 and S_14's 2027-01-06; GitHub run timestamps 2026-10-29/30 in `artifacts.json` and
    `scratch-repository.json`; runner image versions `20261013…`/`20261026…`; the CP-26 folder name
    `cold-rerun-2026-10-15`; the retrieval date 2026-10-30 (`retrieval-local.json`, `run.py`'s comment,
    `measurement.json`); and digit runs inside floating-point numbers in `states/*.json`. No delivery day: the state
    files' day keys end 2026-08-29, `truth.json`'s keys end 2026-09-04, and the shipped payloads' days end 2026-09-06.
20. `python -m pytest tests/cp17cprobe -q -rs -p no:cacheprovider --basetemp=<C>/pytest-local` (with the local
    references present) — exit 0, `21 passed`.
21. `brew list --pinned` — `node` (read only); `/opt/homebrew/Cellar/node/` holds `26.7.0` only.
22. `git -C <worktree> status --porcelain` and `rev-parse HEAD` after the review — exit 0, empty; `7ee1cf07a39f3cd7853a9687fc4b2e5788095079`.
23. `git show main:scripts/bar.py | python3 -I - check <C>/integration.md --source capstone_v21.md@7ee1cf07…` (this
    verdict's four quote blocks) — exit 0, `ok` for each block.

## Evidence actually inspected

- The candidate's whole diff list and every new source file read in full: `src/cp17cprobe/run.py`, `compare.py`,
  `inputs.py`, `probe.yml`; `tests/cp17cprobe/test_probe.py`, `fake_node.py` (mode 100755).
- `reports/cp17c-probe/`: `report.md` (whole), `proposals.md` (as rendered in it), `measurement.json` (per-job hosts,
  summaries, minutes), `artifacts.json` (runs, jobs, steps, artifacts, billable), `inputs.json`,
  `retrieval-local.json`, `scratch-repository.json`, `compute-ledger.jsonl`, `states/`.
- The 10 downloaded zips and their unpacked contents in `<C>/downloads/` (`host.json`, `node-retrieval.json`,
  `uv-retrieval.json`, `uv-freeze.txt`, `project-sha256.txt`, `inputs-verified.json`, `parity.json`, `shadow.json`,
  every `run.json`).
- References: `reports/cp17b/host-parity.json`, `partial-days.json`, `shadow-run.json`, `f1-2026-03-30.json`; the local
  source `.local/artifacts/cp-17b/runs/shadow-host/shadow-run.json` and `host-parity/host-parity.json` (hashes equal to
  the committed reports' citations); every reference run record the comparison uses.
- `reports/rebaseline/cold-rerun-2026-10-15/cost-projection.json` (search 13: `complete_historical_fit_price_seconds`
  5,079.07, 813 fits; searches 3–13 nominal 3,376–5,079 s; `cold_margin` 2.0).
- `src/cp17/daily.py` and `src/cp17/tools/hosts.py` (`NODE` = Homebrew's path), `src/cp17/tools/refreeze.py` (k13
  from the local `evidence/cp-26` extract; absent local files reported unchecked).
- `.github/workflows/tests.yml` (the seven steps, Python 3.12), and the CI runner script
  `.local/artifacts/cp-17c-probe/ci-runner.py`, read before running it.
- Not used: the Lead's unpacked download folders, `critic-assignment.md`, the Lead's logs and any Lead narrative.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| O1a | Runner measurement: a standard GitHub-hosted Linux x64 runner and a standard macOS Apple-silicon runner, each named by its image label | PASS | `ubuntu-24.04` (x86_64, ImageOS ubuntu24) and `macos-26` (arm64, ImageOS macos26), standard labels in `probe.yml` and in every job's `host.json`/`artifacts.json` labels |
| O1b | … with its image version, CPU, cores and memory recorded | **FAIL** (report) / PASS (record) | `measurement.json` records each job: ubuntu-24.04 — ImageVersion 20261026.354.1, AMD EPYC 7763, 2 cores, 8,317,935,616 B, all three jobs; macos-26 — **parity job 20261013.0424.1 (CPython 3.13.16), both shadow jobs 20261026.0455.2 (CPython 3.13.17)**, Apple M2 Pro (Virtual), 5 cores, 15,032,385,536 B. The committed `report.md` hosts table gives macos-26 one image, `macos26 20261013.0424.1`, and CPython 3.13.16 (the first job's host only: `compare.runner`'s `out['host']`, which `report.py` uses for every row but CPU), and Proposal 1 states "One image version per OS was observed: `ubuntu24 20261026.354.1` and `macos26 20261013.0424.1`" — contradicted by the measurement for 56 of the 75 macos-26 fits |
| O1c | What runs: `cp17.daily` with the frozen package, the pinned Pyodide files, the official Node.js v26.7.0 binary for the platform; CPython in the environment `uv.lock` pins | PASS | `run.py` uses `cp17.daily.Host(...).run` / `issue_day` with `node=` passed in; every record's executed files equal the freeze manifest (`all_executed_files_match_package` true); Pyodide's 23 files equal the manifest on every job (recomputed in `compare`); Node binaries `ad19784f…` (linux-x64) and `a9bd0630…` (darwin-arm64), each tarball equal to its `SHASUMS256.txt` line; `uv sync --locked`, `project-sha256.txt` on every job = the candidate's `uv.lock` `5d2aecc3…` and `pyproject.toml` `aa35326a…`; numpy 2.4.6 = the lock |
| O1d | The days, in the brief's priority | PASS | No subset was needed: on both runners all 15 parity stems of `host-parity.json`, F1's four, and all 14 shadow days with the three shadows (75 fits each) |
| O1e | Recorded per runner, day and policy: bit identity by SHA-256; if not, the largest difference per quantile and the selections; the buffers' SHA-256; wall time and peak memory against 15 min and 4 GB; the payload identity | PASS | `measurement.json` fit rows carry `bit_identical`, `status`, `max_abs_eur(_by_level)`, `selections_match`, `wall_seconds`, `peak_bytes`, `within_ceilings`, `payload_identity_equal`; shadow days carry `buffers_equal_reference` and `buffers_equal_payload`; recomputed byte-equal (command 13) and re-derived independently (command 14): 75/75 bit-identical per runner, 42/42 buffers, all within ceilings |
| O2 | Local control: the official darwin-arm64 binary on the parity origins and F1's day | PASS | `measurement.json` `local_control`: 19/19 bit-identical, binary `a9bd0630…` ≠ Homebrew's `1ef99ea2…`; my rerun of A1-2026-09-06 bit-identical (command 11); both local runs 19/19 by bytes (command 16) |
| O3a | Proposal: which runner passes cleanly, compared on time, memory, stability | PASS, with the misstatement in O1b | Both pass; figures checked: 349–366 / 270–284 / 197–212 s per issuance, 284.6 s = 32% of 900 s, A1 2025-10-26 146.8 s (EPYC 9V45) vs 284.6 s (EPYC 7763), peaks < 0.92 GiB — all the measurement's. Not from any record: "Linux's standard fleet is GitHub's largest", "In a public repository, standard runners cost nothing", "A public repository's standard Linux runner is a different class" (external statements). The "one image version per OS" line is false (O1b) |
| O3b | Proposal: what CP-17c must re-freeze — binary and retrieval, host identity, where `refreeze verify` runs, the runtime check before issuing | PASS, with one misstatement | Tarball 62,014,253 B `bd6b6c31…`, `bin/node` 147,870,928 B `ad19784f…`, `SHASUMS256.txt` 2,943 B `4533f0a4…`, darwin-arm64 57,622,243 B / `a9bd0630…` — all the records'; Pyodide 23 files 44,962,352 B (≈43 MiB), largest 13,258,840 B; Homebrew `NODE` defaults, `.local/tools/pyodide-0.28.0` and the local k13 extract confirmed in `src/cp17/`; canary 137.3 s Linux / 98.8 s macOS and B0 7.1–12.3 s are the tables'. "Retrieval took 0.5 s" approximates the records (tarball + `SHASUMS256.txt` 0.35–0.42 s on the Linux jobs). **"The probe's runners got 3.13.17 (Linux) and 3.13.16 (macOS)" is incomplete: both macOS shadow jobs got 3.13.17** (measurement) |
| O3c | Proposal: daily cost per issuance and for decision 23's four | PASS, one range off | Table arithmetic reproduces from 30 s setup + 366/284 s per issuance + 137/99 s canary (≈9/7, 27/21 job-minutes; ×10 macOS; ×30 days); chain steps per day 274.8–279.0 s Linux, 151.0–154.8 s macOS (`artifacts.json`); 566.6 s max day sum. "A job's setup before the chain took 19–30 s" does not match `artifacts.json`: the measured jobs' setup was 17–30 s (macOS shadow jobs 17 and 18 s) |
| O3d | Proposal: estimate of S_14 against hosted job limits | PASS | 5,079 s / 813 fits, 3,376–5,079 s, ×2 cold margin (`cost-projection.json`); Pyodide/native 3.27–5.61, median 4.59 (`host-parity.json`); parity wall ratios 1.69 / 1.20 (`measurement.json`); table arithmetic reproduces. "GitHub's documented 6 hours per job" is external, not from a record (stated as untested) |
| O4 | If no runner reproduces, PASS with the numbers; BLOCKED only if unmeasurable | N/A | Both runners reproduced |
| F1 | Development data only; no delivery day after 2026-09-06 read | PASS | Shipped payload days 2025-10-26 … 2026-09-06; `truth.json` keys end 2026-09-04; state day keys end 2026-08-29; `inputs.py` refuses payload days after the boundary (command 19) |
| F2 | Retrieval software only, recorded with URL, version, bytes, SHA-256 | PASS (observation) | Node.js `SHASUMS256.txt` and both tarballs, and the uv wheels, each with URL, version, bytes, SHA-256 per job (`node-retrieval.json`, `uv-retrieval.json`) and for this Mac (`retrieval-local.json`, rehashed); Pyodide uploaded and verified by the manifest's hashes; the Python packages by `uv.lock` (`5d2aecc3…`, which carries their URLs and hashes); actions pinned by commit SHA. Observation: `actions/setup-python`'s interpreter is recorded by version only (3.13.16 / 3.13.17), not by URL/bytes/hash |
| F3a | No committed file over 50 MB | PASS | Largest new file 283,342 B (command 5); test `test_inputs_fit_a_github_repository` |
| F3b | The workflow's seven steps green on a history-free single-commit copy, `CI=true`, Python 3.12 | PASS | Command 9: every step exit 0 on a history-free one-commit copy of the candidate's tree, `CI=true`, Python 3.12.14; 2444 passed, 46 skipped; the probe's local-material tests skip with stated reasons |
| F3c | Tests needing the runtimes or GitHub skip with a stated reason; timing-sensitive tests carry `stress` | PASS | `need_reference()` and the measurement test skip with stated reasons when `.local` material is absent; no probe test is timing-sensitive (none needs `stress`); locally, with the references present, 21 passed (command 20) |
| F4 | No pinned file and no landed code changes; new paths only; nothing under `.github/` | PASS | Command 5: 20 added files, none modified or deleted, none under `.github/`, `src/cp17/`, other `src/`, `data/`, earlier `reports/`, anchors, `pyproject.toml`, `uv.lock`; `refreeze verify` `verified` (command 8) |
| F5 | The Critic reruns one local-control day, the whole suite in CI mode, and recomputes every comparison from the downloads, verified by their hashes; runs nothing on GitHub | PASS (performed) | Commands 9, 11–18; no `gh`, no network |
| C1 | Red line (§24.2) | PASS | Command 19 |
| C2 | Files that never change | PASS | Command 5; the freeze check (command 8) |
| C3 | Homebrew's `node` stays pinned and installed | PASS | `brew list --pinned` lists `node`; `Cellar/node/26.7.0` present; binary `1ef99ea2…` |
| C4 | Credentials and telemetry: no secret anywhere; telemetry off | PASS (from records) | `probe.yml` references no `secrets.`, `permissions: contents: read`, `persist-credentials: false`, `MLFLOW_DISABLE_TELEMETRY`/`DO_NOT_TRACK` set; `scratch-repository.json`: private, 0 secrets, 0 variables, default workflow permissions `read` (a record; not re-read online, as item 5 forbids) |
| C5 | Tools: `gauntlet.py start`, the worktree, one focused Critic through `critic-open`/`critic-brief`/`critic-close`, `return` | PASS so far | This review was opened by `critic-open` (worktree present, clean, at the candidate) and briefed by `critic-brief`; `critic-close` and `return` follow this verdict |
| C6 | Memory directory untouched; Owner-facing Git commands non-interactive | N/A to the candidate | Nothing in the candidate touches either |
| X1 | Workflow: GitHub's own actions only, pinned by commit SHA; `contents: read`; no secret; standard labels; minute limits | PASS | `actions/checkout@3d3c42e5…`, `actions/setup-python@5fda3b95…`, `actions/upload-artifact@cf430e03…` (40-hex each); step limits below job limits; worst case of the defaults 235 + 124×10 = 1,475 ≤ 1,500 |
| X2 | The minutes (863 counted, of 1,500) | PASS | Recomputed from `artifacts.json` job times: run 1 6+7+5 Linux + 7×10 macOS = 88; run 2 38+29+38 + 29×10 = 395; run 3 (16+22)×10 = 380; total 863 (GitHub's billable figures are 0 ms for every job, as the report says) |
| X3 | Scratch repository and the runs it made | PASS | Rebuilt tree = `ff458082` (command 18); runs 2 and 3 at `ff458082`, run 1 at `e7b99a45`, per `artifacts.json` and each job's `GITHUB_SHA` |
| X4 | Every figure in the proposals is the measurement's or a cited committed record's | **FAIL** | As O1b, O3b and O3c: the macOS image version and CPython claims contradict `measurement.json`; the setup range 19–30 s does not match `artifacts.json` (17–30 s); four statements are external, not from any record (O3a, O3d) |

**Observations (not gaps):**
- For A1 on 2026-08-24 … 08-30, the reference records are bound to CP-17b only by payload identity and executed files
  (`inputs.references`), because neither `reports/cp17b/shadow-run.json` nor its source records A1's issued quantile
  hash on shadow days; the other 68 references per runner are bound by a committed quantile hash.
- `reports/cp17c-probe/compute-ledger.jsonl` totals 3,268.5 s (0.91 machine-hours) and omits the Lead's later CI runs.
- The runner jobs run Python 3.13.16/3.13.17 against this host's 3.13.15, with identical results; Proposal 2 already
  asks CP-17c to pin one patch version.

**Critic's own compute:** about 0.24 machine-hours (CI-mode suite 714.6 s, local-control fit 93.8 s, inputs rebuild 27.4 s, freeze checks, comparisons, tests and re-renders about 35 s); at most 2 concurrent workers (the control fit and the inputs rebuild overlapped the CI run); largest single peak 1.32 GB; within the 1.0 machine-hour, 4-worker and 12 GB limits.

## On FAIL only

- **Single largest meaningful gap:** the committed report misstates the `macos-26` host identity, the item the
  brief makes a recorded deliverable. Its hosts table gives one image version (`macos26 20261013.0424.1`) and
  CPython 3.13.16, and Proposal 1 says "One image version per OS was observed". But `measurement.json` records that
  both macOS shadow jobs (run 40978681906, 56 of the 75 macOS fits) ran on image `20261026.0455.2` with CPython
  3.13.17. The cause: `compare.runner` keeps the first job's host as the runner's `host`, and `report.py` renders
  every hosts-table row from it except the CPU row. The measurement itself is correct and complete.
- **Exact next acceptance test:** a new candidate whose `measurement.json`, `artifacts.json` and `inputs.json` are
  byte-identical to 7ee1cf07's, and whose `report.md`, re-rendered by `cp17cprobe.report` from them, shows every
  job's image version and CPython per runner:
  - macos-26: 20261013.0424.1 / 3.13.16 (parity), 20261026.0455.2 / 3.13.17 (both shadow jobs);
  - ubuntu-24.04: 20261026.354.1 / 3.13.17 (all three).

  Its `proposals.md` must state the image versions and CPython versions as measured, and the setup range as 17–30 s,
  with a test that fails if the hosts table omits a job. `tests/cp17cprobe` and the CI-mode suite must stay green.
