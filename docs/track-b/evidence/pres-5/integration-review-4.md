# Verdict — PRES-5 — Integration — PASS

- Candidate SHA: `48f56b0ef7f7bcf3fa16778cd69a7ea8eebae2e2` (`gauntlet/pres-5`; base `main` = `3c8e158c9895f5b3fed13db794b0ddd5fb80c56f`)
- Plan / version / bar: `capstone_v21.md`, v21-r20 (SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`),
  §24.14 "Publishing and going live before 4.7T (v21-r20)" (section 115 lines, 7426 bytes, SHA-256
  `5d38de24b3c68ec01e2f5c4e6eaf368c253485107549fc2d85c3c71ccf2f5349`); with `docs/PUBLISH_RULES.md` revision 1.5
  (`1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`) in full, and the brief
  `docs/track-b/evidence/pres-5/issued-brief.md` (`9eb2a58433f41739fc22744854c4c55b099cc05ca729b677e9b3b5ccef87ebc3`).
- Reviewer: the fourth Integration Critic of PRES-5. I authored none of PRES-5's changes. I worked only in the clean
  detached worktree `/Users/djourno/Downloads/PJM/.local/worktrees/pres-5/critic-4`, made no Git write, and read the
  three earlier Integration reviews, the editorial review and the fresh-reader record only after forming the findings
  below. I did not open the Claude memory directory, `progress.md`, any syllabus, Track A/C material,
  `orchestrator-role.md` or the Lead's notes.
- Worktree clean before and after: yes (`git status --porcelain` empty and `HEAD` = `48f56b0e…` at the start, after
  every rebuild, after the test suite, after the browser checks and before writing this file).
- Verbatim bar excerpt (extracted at the candidate with `scripts/bar.py bar --at 48f56b0e… --quote`, and byte-equal to
  the excerpt in the brief, command 24). The excerpt is the citation. Any line number is a courtesy and is non-binding.

> ### 24.14 Publishing and going live before 4.7T (v21-r20)
>
> **What this section does.** It applies the Owner's decision 28 of 2026-11-05
> (`docs/track-b/owner-decisions-2026-11-05.md`, SHA-256 `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`).
> - It governs where it differs from §24.2, §24.9, §24.10, §24.12's list "For CP-18", §24.13's list "For CP-18" and
>   decision 25's order.
> - Every term below was set without any 4.7T outcome, since none exists.
>
> #### What stays exactly as registered
>
> - **A1's freeze.** CP-17c's policy identity `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`,
>   its manifest and the frozen package stay unchanged. `refreeze verify` guards them, and the live pipeline
>   calls the package without editing it.
> - **4.7T, in every registered term** (§24.12, §24.13):
>   - the window, delivery days 2026-09-07 to 2026-12-05;
>   - the candidate, the comparators, the scores, the pass conditions, the margins and the failure rules;
>   - the vintage terms (the protocol's §3);
>   - the machine (the Owner's Mac, no cloud) and the H2 checks before its first issuance;
>   - the calendar: it opens no earlier than 2026-12-04, after the price for 2026-12-05 is published;
>   - the audit, the Owner's declaration and his retrieval approval.
> - **4.7T issues its window itself.** Its issuance starts from the freeze-origin state, runs on the Owner's Mac
>   under its terms, and keeps its own store. Nothing the live product issues is 4.7T's issuance or score.
> - **No registered term changes from here until 4.7T is scored.** A proposal to change one returns 4.7T to the
>   Owner as BLOCKED.
>
> #### What changes
>
> **1. The order (decision 25).** CP-18's activation and a publication now come before 4.7T:
> - **CP-18c**, the activation: the live product starts and runs daily;
> - **PRES-5**, the publication: the research since v5, A1 in the comparison, and the live product;
> - **then 4.7T** at its date, and the publication of its result.
>
> Decision 25's "one complete publication" becomes these two publications.
>
> **2. The red line, for the live pipeline only.** §24.2's guard retires for the live pipeline at CP-18c, not
> after 4.7T.
> - **The live pipeline downloads all the data through the present** and trains on it, as §24.2's last
>   paragraph allows ("The live product, once running, trains on all the data available to it").
> - **Every research path keeps the guard.** The development downloaders and builders still refuse any row after
>   2026-09-06, and CP-17c's development builder stays as frozen.
> - **Reading.** The live data is handled by code.
>   - An agent that operates the live pipeline may read its logs and records, only to operate it.
>   - No agent uses data after 2026-09-06 for any research number, chart, choice or registration before 4.7T is
>     scored.
>   - §24.2's rule on reports, news and analyses about market events after 2026-09-06 is unchanged.
> - **The exposure ledger.** Its pinned file `docs/track-b/exposure-ledger.md` stays byte for byte. Later entries
>   go in its continuation, `docs/track-b/exposure-ledger-continued.md`, which the audit reads with it.
>   - CP-18c seeds the continuation with decision 28's entry, dated by the live pipeline's first
>     retrieval.
>   - **Its impact assessment:** nothing 4.7T tests can change after it. Everything 4.7T tests was frozen,
>     registered and pushed to the public repository before decision 28: `land/cp-17c`, 2026-10-30, and the
>     protocol at its freeze. `refreeze verify` checks the freeze on every run.
>
> **3. The audit (§24.2's standard) reads with this.**
> - **The live product's daily fits** are the frozen policy's own operation, not research fits. They sit
>   outside the standard's "fit" and are recorded in the continuation.
> - **The standard's test applies unchanged** to everything 4.7T tests.
> - **The Owner's declaration** covers his decisions before 4.7T opens. Decision 28 used no information after
>   2026-09-06.
>
> **4. The live product's start.**
> - **The live store** is seeded at the freeze origin, 2026-09-06, with CP-18a's genesis command. It is carried
>   to the first live day with CP-18a's `carry`.
> - **The days between** are outside the live record and are never issued by the live product.
> - **The live product's forecasts for window days,** from its first live day to 2026-12-05, are its own. Each
>   carries its actual run time, and none is 4.7T's.
> - **After 4.7T** the live store continues. §24.12's carry "from 4.7T's last window day to the first live day"
>   becomes this carry from the freeze origin.
>
> **5. What the live product shows.**
> - **It shows the live record** under PUBLISH_RULES A7 and A9: the issued forecasts, the outcomes as published,
>   and the issued forecasts' prospective scores.
> - **A1's status** reads "final candidate · pending 4.7T" (O13).
> - **The prospective scores** are labelled "prospective evaluation in progress" (§24.9).
> - **No display presents a live score** as 4.7T's, or as a test result.
> - **The development-period displays** stay on days through 2026-09-06.
>
> **6. The publication (PRES-5).** Decision 28 is the separate decision that §24.10 requires for publishing
> CP-26's and CP-28's results.
> - **It covers:**
>   - A1 in the published comparison, on the same data as v5's comparison;
>   - CP-26's re-baseline on every development day;
>   - CP-28's selection;
>   - the freeze, with 4.7T's registered terms;
>   - the live product.
> - **Its research numbers use development data only.**
> - **It runs under PUBLISH_RULES 1.5.**
>
> **7. The runner and the secrets.**
> - **Until the Owner enters the three repository secrets** (decision 25), the daily runs use the local fallback
>   on the Owner's Mac (§24.13), with the credentials used only inside the consuming process.
> - **The `macos-26` schedule is enabled** once the secrets exist.
> - **The issuing host and the H2 checks are unchanged** on either machine.
>
> **8. What this supersedes:**
> - **§24.2:** "After 4.7T, CP-18's brief retires the guard for the live pipeline only" (item 2);
> - **§24.9:** the order of "Then: CP-18 … and site activation" (item 1);
> - **§24.10:** "No publication" (item 6);
> - **§24.12's list "For CP-18":** the carry from 4.7T's last window day (item 4);
> - **§24.13's list "For CP-18":** the item on the red line on the runner (item 2).
>
> S_14 (§24.13, H4) is unchanged.
>
> #### Decisions recorded (v21-r20)
>
> | # | Decision | Who |
> |---|---|---|
> | 28 | Publish and go live now; A1 frozen and untouched; 4.7T exactly as registered | Owner, 2026-11-05 (`docs/track-b/owner-decisions-2026-11-05.md`, SHA-256 `4daa5617e51208b0994eac925d51078ea43481e6fb1017aec3576c0936490215`) |
> | P1 | "All the data" for the published research means every development day. Research numbers on window days wait for 4.7T, so that it stays the one test | Orchestrator, under decision 27 |
> | P2 | The live start: genesis at the freeze origin, carried to the first live day. The live product's window-day forecasts are its own, never 4.7T's | Orchestrator, under decision 27 |
> | P3 | The guard retires for the live pipeline only. The exposure ledger continues in a new file, because its own file is pinned | Orchestrator, applying decision 28 |
> | P4 | The local fallback runs until the repository secrets exist | Orchestrator, under decision 27 |
>
> **The Owner's declaration (§24.2)** covers decision 28. P1–P4 are registrations under §24.2's test, which the
> audit checks, as R1–R7 and H1–H4 are.

## Commands actually run

All from the critic worktree unless stated, with `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1` and `UV_OFFLINE=1`
exported (`MLFLOW_DISABLE_AGENT_HINT=1` from command 10 on). Logs and my own scripts are under this session's
scratchpad, outside the worktree.

| # | Command | Exit | Observed output |
|---|---|---|---|
| 1 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief pres-5` (from the lead worktree, as instructed) | 0 | This review's brief: candidate `48f56b0e…`, worktree `critic-4`, verdict path, the bar's identity line |
| 2 | `git -C …/critic-4 status --porcelain`; `rev-parse HEAD main`; `log --oneline -3`; `diff --stat 3c8e158c 48f56b0e` | 0 | empty; `48f56b0ef7f7…`, `3c8e158c9895…`; 68 files, +42,979 / −333 |
| 3 | `shasum -a 256 capstone_v21.md docs/PUBLISH_RULES.md docs/track-b/evidence/pres-5/issued-brief.md` | 0 | `80341681…30e6`, `1bc0c523…f94e`, `9eb2a584…ebc3`: each equals the brief |
| 4 | `shasum -a 256` of the brief's 18 execution inputs and of `docs/track-b/owner-decisions-2026-11-05.md` | 0 | all 19 equal the brief's values (PRES-4 packet `6c1ec149…` through CP-18b's landing `fe191d89…`; decision 28 `4daa5617…`) |
| 5 | `git show 3c8e158c:docs/index.html \| shasum -a 256`, `\| wc -c`; the same for `README.md` | 0 | `54708134…37ce`, 1,996,267 bytes; README `c816972a…15bc`: the brief's published identities |
| 6 | `uv sync --frozen --offline` | 0 | environment created from the cache; no download |
| 7 | `uv run --frozen python -m delu_forecast.final_candidate --check` | 0 | `{"identical_to_committed": {metrics.csv, parity.json, preview-day.csv, ratio-intervals.csv, summary.json, uncertainty.csv: true}}` |
| 8 | `uv run --frozen python -m delu_forecast.compact_figures --check` | 0 | `{"pixel_identical": true, "problems": []}` |
| 9 | `uv run --frozen python scripts/build_pages.py`, then `git status --porcelain` | 0 | wrote `docs/index.html` (1,848,408 bytes) and `reports/cp3/pages_build.json`; status empty: the page reproduces byte for byte |
| 10 | `uv run --frozen python scripts/readme_research.py`, then `git status --porcelain` | 0 | regenerated the glance and generations blocks; status empty |
| 11 | `uv run --frozen python scripts/mlflow_export.py --check` | 0 | "the committed export is current" |
| 12 | `uv run --frozen python scripts/mlflow_export.py --diff-against 3c8e158c` | 0 | runs 44 → 105, the 61 added are `cp26` + 52 children and `cp28` + `cp28/A1…A7`; checked 362 params, 16,753 metric points, 90 datasets, 107 artifacts (107 digests unchanged); identity changes on 0 runs; substantive changes none; `only_identity=True` |
| 13 | `uv run --frozen python scripts/lint_publication.py` | 0 | page 0, README 0, templates 0 findings; PASS |
| 14 | `uv run --frozen python scripts/build_wasm_payload.py` (for the WASM tests); `git status --porcelain` | 0 | payload 15,363,807 bytes, 14 files; status empty |
| 15 | `uv run --frozen pytest -q -p no:cacheprovider -rfEs` (whole suite, Python 3.13, 21 min 38 s) | 1 | **3,242 passed, 9 skipped, 2 failed.** The two failures are `tests/cp18a/test_dry_run.py::test_a_real_dry_run_then_the_fallback_finds_the_day_claimed` and `tests/cp18a/test_forced.py::test_each_cause_is_forced_and_recorded`, both stopped by the pre-push publication guard: "`reports/cp3/pages_build.json` is a non-final build record (final: false)". That is the packet's §7/§10.3 explanation (they pass only after the `--final` build). Skips: eccodes absent; CP-16 bound to v21-r3; CP-16 production ledger; CP-24 draft export (`mlflow_export.py` changed after CP-24, bound by its artifact manifest); CP-28 GFS note (local CP-26 outputs absent). Same totals as the packet's prerelease record |
| 16 | My own recomputation script (pandas/NumPy only, none of the project's scoring code): v6 (`arm == "A1"`) from `reports/cp28/forecast/hourly.parquet` on v5's 10,747 keys from `reports/ddnn2/attempt-1/predictions.parquet`, B0 from `reports/weather-ablation/predictions.parquet`; MAE of `q50`, WIS = 2 × mean pinball over the seven quantiles; per-fold ratio to B0, equal-fold mean | 0 | 0 A1 keys missing, 0 B0 keys missing, truth equal; **v6 S_MAE 0.4928063413559065, S_WIS 0.4373719802748803; v5 0.5223212760431432, 0.4936627890811674**; ratio −5.6507% (S_MAE), −11.4027% (S_WIS); per-fold MAE v6 4.52, 7.05, 43.19, 13.09, 13.37, v5 4.82, 7.52, 45.50, 13.59, 14.45; pooled 95% coverage v6 0.94473 at width 82.420, v5 0.93952 at 100.248; 0 quantile crossings; 465 negative-price hours on 85 days |
| 17 | The same script, an independent paired bootstrap: CP-20's index construction re-implemented from its definition (seed 15042, `integers(0, 84, (2000, 13)) + arange(7)`, first 90, per fold in order), my own daily sums and counts, equal-fold ratio of means | 0 | S_MAE ratio 95% [−9.0252%, −2.4498%], 97.5% [−9.6425%, −2.1249%]; S_WIS 95% [−14.5403%, −7.8905%], 97.5% [−15.0725%, −7.5243%]; against the naive −50.72% [−53.57%, −46.49%] and −56.26% [−58.94%, −52.28%]; differences −0.029515 [−0.049383, −0.012847] / [−0.052484, −0.010903] and −0.056291 [−0.074719, −0.039022] / [−0.077287, −0.036694]: **every value equals `ratio-intervals.csv` and the chart's values table to the printed digits** |
| 18 | Python reads of `reports/cp28/results/selection.json`, `holm.csv`, `descriptive.json`, `reports/cp28/owner-summary.json` (`gfs_note_headline`), CP-26's `presentation-v21-r16/publication-packet.json` (`headline_quantities.comparisons`) and CP-26's `MLflow-export.json` (all-eligible runs) | 0 | 7 arms, all `passes_all_four`; selected A1, best WIS 9.6825 vs A6 10.1294, tie bound 9.7309; A1's Holm p 0.0041996 (raw = adjusted, last position), the six others 0.0007; A1 ratios MAE 0.93105 [0.90930, 0.94865], WIS 0.89070 [0.87149, 0.91043]; each arm's ratios and intervals round to the arms table; 18 fallback dates per arm (source v5); GFS +6 h +13.99% [1.1034, 1.1611] and +15.46% [1.1208, 1.1758]; v5 vs v4 all-eligible 0.99340 [0.98591, 1.00939] and 0.99497 [0.98803, 1.01025]; every row of the every-day table equals the export's mean daily losses and B0 ratios |
| 19 | Python read of `reports/presentation/mlflow-export/{cp26,cp28}.json`; `shasum -a 256` of the three export files; packet §6's `--authorized-runs` list against the exports' run keys; the same list at `f865ff94` and at the candidate | 0 | `46483ce9…65c4`, `22686399…36d7`, `57216cc6…e16f` (= packet §6 and §8.0); 61 runs, the authorized list 61 unique keys, set-equal; list unchanged since review 3 (both hash `e09cc1cd…`); v6's five runs (`cp28/A1`, `cp26/nominal/D2/*`) `delu.adopted = "false"`, `delu.status = "final candidate 2026-10-30"`, public name "v6 · DDNN-2 alone"; `cp28/A2…A7` study arms "not adopted 2026-10-25" |
| 20 | `uv run --frozen python scripts/mlflow_publish.py --dry-run` | 0 | "dry run: 105 runs, 17003 metric points, 229 artifacts; outbound scan clean; export current at 48f56b0ef7f7"; nothing written |
| 21 | `printf 'refs/heads/gauntlet/pres-5 48f56b0e… refs/heads/gauntlet/pres-5 3c8e158c…\n' \| python3 scripts/secret_guard.py pre-push origin "$(git remote get-url origin)"` (a value-based scan of the candidate's commits; pushes nothing) | 0 | `SECRET-SCAN-CLEAN` |
| 22 | O34: for each of the five modules, `git rev-parse 61658c7:<path>`, `git hash-object <snapshot>`, `git rev-parse 3c8e158c:<path>`; the manifest's SHA-256 against `reports/rebaseline/harness-log.json` `landed_code` | 0 | all five equal on all three (e.g. `derived.py` `e669a65b…`); all five SHA-256 equal the harness log's; the log's landed bases are `src/cp15,16,20,21,22,24,25` and `src/delu_forecast`; the two new modules are not in the log |
| 23 | `git grep -l -F <path> 48f56b0e -- src/cp26/harness.py 'docs/track-b/evidence/cp-17*/*.json' 'reports/cp17*/*.json' 'reports/cp18*/*.json' 'src/cp17/**' 'src/cp18/**' 'reports/rebaseline/*.json'` for every changed non-evidence path | 0 | the five modules only in CP-26's harness log (O34) and `reports/cp17c/inputs.json` (N3, disclosed); `README.md` in `reports/cp17c*/inputs.json` (the same record) and as the Space's own card in `reports/cp18b/space-build.json`; no freeze manifest names a changed file |
| 24 | `git show main:scripts/bar.py \| python3 -I - bar --at 48f56b0e… --quote capstone_v21.md "### 24.14 …"`; `diff` against the brief's excerpt | 0, 0 | identity line `plan capstone_v21.md at 48f56b0e…: sha256 80341681…; section 115 lines, 7426 bytes, sha256 5d38de24…`; `BRIEF-EXCERPT-EQUALS-PLAN-AT-CANDIDATE` |
| 25 | `uv run --frozen python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json` (the page's "Run and check this product" command) | 0 | `verified` (on this machine, with the issuing host's local files) |
| 26 | `git cat-file -e <tag>:<path>` for the page's eight evidence links at `evidence/cp-17`, `evidence/cp-17c`, `evidence/cp-28`, `land/cp-26`; `git log -1 --format=%cs <tag>` | 0 | all eight exist; tag dates 2026-10-28, 2026-10-30, 2026-10-25, 2026-10-21 = `registry.py::EVIDENCE_TAGS` and the page's "frozen <date>" labels; the page uses `land/cp-26`, not the unpushed `evidence/cp-26` |
| 27 | Python scans of `docs/index.html` and its text: internal anchors; dates after 2026-09-06; Space links; `fetch(`; every A1–A7 code in context; sentences naming v6 with "adopt/released/live" | 0 | 99 internal links, 0 missing targets; every post-boundary date is structural (rule, freeze, landing, measurement, window dates); Space links: root ×6, `/history/` ×3, the direct app ×1 (in the archive); no `fetch(`/XHR; `A1` appears only as "A1 in the frozen records", "picked arm A1, now v6", and in the values table's code column; no sentence calls v6 adopted, released or live |
| 28 | `UV_OFFLINE=1 uv run --frozen python -I -c …` min/max delivery days of `reports/cp28/forecast/hourly.parquet` and CP-24's rows; the preview CSV's first row | 0 | CP-28's store 2020-01-01 to 2026-09-06 (408,114 rows); CP-24's rows 2020-07-01 to 2026-04-07; the preview day 2026-04-07 |
| 29 | `PLAYWRIGHT_BROWSERS_PATH=… .local/tools/playwright/bin/python scripts/check_reader_paths.py release docs/index.html --shots <scratchpad> --out <scratchpad>/release.json` (file:) | 0 | passed=True (served over `file:`, as its record says). Chrome 157.0.8103.51 and WebKit 26.6 at 1440×900, 768×1024, 390×844, 360×780, 320×640 and the emulated iPhone 393×659: no console error, failed request, HTTP error or resource after the document; no collapsed space; no overflow with disclosures open; charts 7 checked per view, 0 clipped, 0 overlapping, smallest text 12.38 px (1440), 14.58 px (390), 12.21 px (320); placements: headline bottom 774.6/775.3 px desktop and 628.6/628.7 px phone, finding bottom 1,667.6/1,668.3 px (limit 1,744) and 2,394.5/2,394.3 px (limit 2,420), byline and release rule outside disclosures; accessibility trees passed in both engines at both sizes; keyboard 161 stops in document order, none without visible focus, anchors open closed disclosures; touch targets at 390 px: 229 checked, none under 44 px; contrast: 0 below at 1440 and 390 (text 4,893/4,886 and non-text 827/797 checked); 200% zoom at 1280 and 1440 and 320 px reflow: 0 px overflow; A5 discovery: 48 routes passed in each engine at 1440×900 and 390×844. Identical in every placement figure to the packet's record for the same page hash `fd9887bd…4b3c` |
| 30 | The same over HTTP, as runbook §9 asks: `python3 -m http.server --bind 127.0.0.1 <port> --directory docs`, then `check_reader_paths.py release http://127.0.0.1:<port>/index.html …`, then the server stopped | 0 | passed=True, `served_over` "http(s)" at `http://127.0.0.1:8793/index.html`. The server logged 33 requests, every one `GET /index.html` answered 200: no favicon or other browser-made request. Every view: no console error, failed request, HTTP error, resource after the document, collapsed space or problem; placements identical to command 29 (774.6/775.3 and 628.6/628.7 px; finding 1,667.6/1,668.3 and 2,394.5/2,394.3 px); chart text ≥ 12.38 px at 1440 and 14.58 px at 390, none clipped or overlapping; discovery 48 routes passed in each engine at both sizes; keyboard 161 stops, touch targets none under 44 px, contrast 0 below, in both engines. This closes runbook §9's HTTP condition for this page (B25) |
| 31 | `git status --porcelain`; `git rev-parse HEAD` (final) | 0 | empty; `48f56b0ef7f7bcf3fa16778cd69a7ea8eebae2e2` |
| 32 | `git show main:scripts/bar.py \| python3 -I - check <this verdict> --source capstone_v21.md@48f56b0ef7f7bcf3fa16778cd69a7ea8eebae2e2` (after writing this file) | 0 | `ok: lines 19–133 (7425 bytes) appear in capstone_v21.md@48f56b0ef7f7` |

**Network use, stated.** Commands 6–30 ran offline except command 30's loopback server. One command I issued while
checking tags, `git ls-remote --tags origin | head -0`, contacted `origin` (GitHub) read-only; its output was discarded
unread and nothing was written anywhere. No other network call was made, and no credential value was read or printed
by me (commands 20–21 use the project's guard, which reads the stored values inside its own process).

## Evidence actually inspected

- The brief (`issued-brief.md`) in full; `AGENTS.md`; PUBLISH_RULES 1.5 §§1–15 (A1–A12) in full and §§16–17's headings;
  the incorporated standard v1 §4 (numbers) and §15; the runbook §§1, 4, 5, 7a, 7b, 8, 9; the packet template's
  headings; `capstone_v21.md` §24.14 (extracted) and greps of §24.7, §24.8, §24.12 and the CP-19 rows; decision 28;
  decisions 20–21 (`owner-decisions-2026-10-29.md`); 4.7T's registered protocol in full; CP-17c's and CP-17b's landing
  records (grep); the CP-28 frozen protocol's header.
- The packet (`publication-packet.md`, all 716 lines); the claim map `pres5-claims.md` in full;
  `src/delu_forecast/final_candidate.py` in full; the head of `compact_figures.py`; the diffs of `derived.py`,
  `research.py` (sources), `README.md`, `tests/test_45`, the two CP-26 tests; `tests/pres5_landed_code.py` and the O34
  manifest; `tests/test_50` (the evidence-date test, the Space-runs-v1 check and its negative control, the export
  adoption test and its negative control, W51/W52 controls); `registry.py::adopted_flag`;
  `build_pages.py::live_measurement` and the opening; `mlflow_publish.py::main`; `secret_guard.py::credentials`; the
  options of `publication_receipt.py`, `verify_mlflow_mirror.py`, `check_reader_paths.py`.
- The rendered page's full text (default and disclosure content), extracted to text and diffed sentence by sentence
  against v5's published page; the README diff; `reports/pres5/a1-in-v5/*` (summary, metrics, ratio intervals,
  parity, preview); CP-28's and CP-26's committed records listed in commands 18–19; CP-18b's `acceptance.json` and
  `space-build.json` (the startup line: Chromium 153.0.8010.12 and WebKit 26.6, both cold starts ready at 1.86 s,
  macOS, 2026-11-05; 551,515 bytes); `reports/cp3/pages_build.json`; the release record
  `pres-5-local-release.json` (its keys and `served_over`); PRES-4's release records' `served_over` (HTTP).
- After my findings: the fresh-reader record, Integration reviews 1–3 (their findings, recommendations and
  acceptance tests); not the editorial review's body beyond the packet's §10.4 summary.

## Checklist verdict

### A. The brief's observable outcome, items 1–10

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | v6 (A1) in v5's comparison, done properly: v5's population (10,747 h, 448 days, five periods, equal weights, the naive denominator, the same interval method); A1's forecasts from CP-28's store under its frozen rules; coverage and information-set differences stated; other rows v5's published rows, never recomputed for publication; paired comparisons v6 − v5 and v6 − naive with the rule's intervals; v5's rule not re-run, v6 never "adopted"; every value derived, none typed | PASS | Commands 7, 16, 17: my independent recomputation, without the project's scoring code, equals every published v6 value (S_MAE 0.4928, S_WIS 0.4374; −6% [−9%, −2%] and −11% [−15%, −8%] at 95%; [−10%, −2%] and [−15%, −8%] at 97.5%; −51% [−54%, −46%] and −56% [−59%, −52%] against the naive; the four chart differences; per-period MAE 4.5–13.4 and 43.2; coverage 0.9447 at 82.4 against 0.9395 at 100.2). Coverage 10,747 of 10,747 keys, 448 native days, 0 fallbacks; the first period in CP-26's warm-up is stated on the page; `#v6-information` lists issue time, fitting, search, data identity and the warm-up; `parity.json` 0.0, and the page's v5/naive rows are CP-24's committed rows (overview table values = `reports/ddnn2/attempt-1/metrics.csv`). "A description, not a decision: v5's adoption rule was not re-run, and it adopts nothing here." Lint 0 findings (command 13); no typed numeral in PRES-5's blocks (scan of the `research_claims.py` diff) |
| 2 | CP-26's re-baseline on every development day: question, population, results, evidence class; beside the five periods, never pooled | PASS | `#everyday`: "A separate population: 2,068 eligible days from 2020-12-29 to 2026-09-06, every policy refitted daily under one protocol … never pooled with the five periods above · development, post-selection"; every table value equals CP-26's export (command 18); v5 − v4 −1% [−1%, +1%] (ratios 0.9934 [0.9859, 1.0094], 0.9950 [0.9880, 1.0103]) with "the intervals do not establish that the two are equal"; the GFS and no-load routes as stated. The panel frames its question by its heading ("Every eligible development day, scored separately") rather than as a question sentence; see recommendation R5 |
| 3 | CP-28's selection: arms, rule, result, why A1 was selected | PASS | `#v6-selection`: the rule (margins 0.5%, 2% non-inferiority by year 2021–2025 and season, Holm across seven at 5%, four analyses, lowest interval error wins); "All seven passed every analysis. v6 had the lowest interval error, 9.68 EUR/MWh against the next best's 10.13"; the arms table's every ratio and interval equals `descriptive.json` rounded (command 18); Holm p 0.0042 (A1, last position, raw = adjusted) and 0.0007; the conditional multiplicity note |
| 4 | The freeze and 4.7T's registered terms; what a pass and a fail mean | PASS, with R2 | `#v6-freeze`: CP-17 2026-10-28, CP-17b 2026-10-29, CP-17c 2026-10-30 under the issuing host (Pyodide in Node.js, `macos-26` runner or the Owner's Mac), 58 of 58 fits bit-identical, identity "begins 720fc581" (= CP-17c's landing record). `#v6-fresh-test` against the protocol (read in full): window 2026-09-07 to 2026-12-05, 90 days, opens no earlier than 2026-12-04, never extended/shortened/rolled; control v5, reference B0, v3/v4/v1 descriptive; p50 MAE and WIS; pass at compound p ≤ 0.05 with the 0.995 margin against v5 and against B0; ≥ 60 of 90 dates or inconclusive; no runner-up, window spent, null valid; the two record wordings quoted from §12. Meanings follow decisions 21 and 28 and O29 (a pass keeps v6; a fail or inconclusive result makes v1 the product again). One inaccuracy of wording: "The intervals come from a 7-day block bootstrap with 10,000 draws" — the protocol's bootstrap (§6) gives the one-sided p-values, and no interval is registered (R2) |
| 5 | The product: the opening pairs "final candidate · pending 4.7T" with the product; the report links the live Space and says what it is; v1's historical demo at `/history/`; no live forecast, score or price, no number on a day after 2026-09-06 | PASS | The status pair "Live product · v6 · DDNN-2 alone" / "Final candidate · pending 4.7T · v6 · DDNN-2 alone"; "By the Owner's decision, the Space runs v6 · DDNN-2 alone daily before its one test: prospective evaluation in progress. A pass releases it; otherwise v1, the last released generation, is the product again."; links to the Space ×6 and `/history/` ×3 (command 27); the opening's preview is a stored development forecast for 2026-04-07, labelled "not a live one"; every post-boundary date on the page is structural; every input row ends by 2026-09-06 (command 28) |
| 6 | The model identity (§4): public name and status proposed and ruled; unselected arms as study arms | PASS | "v6 · DDNN-2 alone", a generation, status "final candidate · pending 4.7T", "v6 (A1 in the frozen records)" where the identity is shown (O30); the six other arms named in words, "Not selected", with no code on the page (command 27); CP-26's sensitivity routes are study arms, never eligible |
| 7 | MLflow: CP-26's and CP-28's exports prepared exactly as authorized (upload after this verdict) | PASS (prepared) | Commands 11, 12, 19, 20: the export is current; 44 → 105, exactly the 61 runs of `cp26` and `cp28` added, no identity or substantive change to any published run; the only experiment-tag change is `mlflow.note.content`; the packet's `--authorized-runs` equals the 61 keys and `--authorized-experiment-tags` is that one tag; the publisher's dry run is clean; no run of v6 is tagged adopted. The upload itself is not reviewed here |
| 8 | The page budget: within 2.0 MB by allowed means | PASS | 1,848,408 bytes (command 9; 151,592 to spare), reached by O25's pixel-identical re-encoding of the archive's seven figures (command 8) |
| 9 | Review: the independent check passes at the candidate, then a focused recheck at the final SHA | This verdict | The focused recheck at the final SHA is still required after the upload, the routes, the index and the `--final` build |
| 10 | The packet's §8: exact payloads and ready-to-run commands for the LAND and push, the public checks with `publication_receipt.py`, A12 | PASS | §8.0–§8.7 read in full: non-interactive (`--no-pager`, `-F` message file present at `.local/artifacts/pres-5/land-commit-message.txt`); the untracked-twin check; the staged-tree check for an unmoved and a moved `main` (the `xargs` form); the evidence-date check; the value-based pre-push scan over exactly the pushed refs; `publication_guard.py tree`; the receipt command's options exist (`--landing`, `--bundle`, `--expect`, `--date`); the browser records; A12's two conditions and its useful check (the report's two Space routes after both publications); recovery identities. Placeholders `<evidence_tip_sha>` etc. are filled by the return |

### B. The complete authoritative bar

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| B1 | PUBLISH_RULES §1.1–§1.3: authority, four identities, categories | PASS | Rules 1.5, anchor v21-r20, brief and decision 28 pinned and re-hashed (commands 3–4); the rule revision, the generation (v6, final candidate), the product status (the live Space runs v6; v1 the last released generation) and the artifact identities (policy `720fc581…`, export hashes, page hash) are kept apart on the page, README and export |
| B2 | §2 reader contract and placements; A1 (metric beside each headline number); A2 (measured header) | PASS | Headline "−7% … in point error and −11% … in interval error"; terms directly beneath; placements in both engines (command 29): headline ends 774.6/775.3 px (≤ 900) and 628.6/628.7 px (≤ 844); the finding ends 1,667.6/1,668.3 px (≤ 2×900 − 56 = 1,744) and 2,394.5/2,394.3 px (≤ 3×844 − 2×56 = 2,420); the product identity line beside the action, outside disclosures |
| B3 | §3.1 evidence classes; withheld claims W1–W53 | PASS | Every v6, CP-26 and CP-28 number labelled development, post-selection; nothing live, prospective or 4.7T's; no sentence calls v6 adopted, released or live (command 27); the export agrees (command 19) |
| B4 | §3.2 scores, comparisons, uncertainty | PASS | CP-28's verdict with its dated rule, distance (−7%, −11% with intervals) and N = 7; on v5's population the change as a share of v5's score with the ratio's interval from CP-24's own draws (recomputed, command 17); absolute MAE per period with the stress period apart; CP-26's every-day results a separate population; difference intervals and forecast intervals labelled apart; coverage with width; "the intervals do not establish that the two are equal" |
| B5 | §3.3 counting | PASS | 7 (the rule's N), 13 (the chart's rows, "not that census"), 25 (the targets' census) each labelled; kinds kept distinct |
| B6 | §3.4 provenance and formatting | PASS, with R3 | Whole percents, one-decimal EUR/MWh, four significant figures on the reading path; nothing rounds toward zero across a sign; the lint passes; every number derived (command 13). The values table shows the code `A1` on two different policies' rows (R3) |
| B7 | §4 registry, transitions, branches; A3; A10 | PASS (A10 n/a) | One registry drives page, README and export; "From v5 to v6: DDNN-2 alone" carries predecessor and date, change, comparator set in advance (= predecessor), result with intervals and class, what it does not establish, dated decision and route; A10 not applicable |
| B8 | §5 page architecture; A4; A8 | PASS for A4; A8 not applied — an open ruling | A4's order: opening → "How the product works" (v6) → comparison and fairness note → the every-day panel → journey with transitions → chapters newest first → planned work → system, reproduction. A8's product-first order is not applied; the packet (§10.3 item 1) proposes that it applies at 4.7T's publication. Decision 28 speaks of "the final product", while the registry, decisions 20–21 and O27 keep v6 "final candidate · pending 4.7T" and v1 "released". The trigger is genuinely contested, so I do not grade it a violation; the Orchestrator should rule on item 1 before the final build. A8's identity requirement (one version and policy across opening, documentation and demo) is met: v6 throughout |
| B9 | §5.1 the twelve subjects; product-replacement migration | PASS | Packet §5b's twelve dispositions match the page's twelve topics (attribution and importance "not evaluated in this report", routed to the Space's views, with reasons); v1's manual leaves the product section; v1's chapter keeps its holdout and shortfalls and routes to its archive (O29) |
| B10 | §5.2 chapter grammar; one page; 2.0 MB | PASS | v6's chapter: question, change diagram, main paired-difference chart (both scores, 95% and 97.5%), reading, two "not established", dated decision, evidence row, details (method, per-period with absolute errors, stress period, coverage and width, protocol and review); 1,848,408 bytes |
| B11 | §6 charts, discovery; A5 | PASS | v6's chart: question/finding, metric, comparator, population, class, units, direct labels, hexagon marker, zero reference, values table; chart text ≥ 12.21 px at 320 px and 14.58 px at 390 px, no overlap or clipping; A5 discovery 48 routes in each engine at both sizes by mouse, keyboard and deep link (command 29) |
| B12 | §7.1 product contract | PASS | The opening names what the Space runs and why it runs before its test; beside the action: about 0.55 MB, ready within 1.86 s in Chromium 153 and WebKit 26.6 on a Mac, 2026-11-05, last verified 2026-11-05, "served locally on development data" — each read from CP-18b's committed records (checked against them); the report embeds no runtime |
| B13 | §7.2/A7 live presentation; §7.3/A9 the final-product Space | Not this block's surface | The report shows no live panel or number; the Space is CP-18c's. Cross-surface check owed after both publications: CP-18b's landed `src/cp18/live_claims.py` names the product "A1 · DDNN-2 alone", while O30 and packet §5d say the Space uses "v6 · DDNN-2 alone" (see O-1 below) |
| B14 | §8 surfaces agree; README; MLflow; report self-contained | PASS for PRES-5's surfaces | Report and README agree (glance block = headline; v6's README section = the chapter's blocks); the export's names, statuses and adoption tags agree with the registry; no `fetch`/XHR; evidence links labelled by type and freeze date, all eight resolving at their tags (command 26); the `compare:v6` route is withheld until verified (`links_omitted_until_verified`) |
| B15 | §9 browser and accessibility matrix | PASS | Command 29 (and 30 over HTTP): Chrome 157.0.8103.51 and WebKit 26.6; 1440×900, 768×1024, 390×844, 360×780, 320×640, emulated iPhone 393×659; no console error, failed request, HTTP error or resource after the document; no collapsed space or overflow; accessibility trees passed in both engines; keyboard 161 stops in order with visible focus; touch targets at 390 px none under 44 px; contrast 0 below (text and non-text) at 1440 and 390; 200% zoom and 320 px reflow 0 overflow. No real Safari, iPhone or screen reader (stated) |
| B16 | §10.1 independence and reading order | PASS | This review; the editorial review and the fresh reader were by agents who authored none of the changes (their records) |
| B17 | §10.2 fresh reader | PASS | Six unchanged questions, closed-state screens only, answers kept verbatim; answers 1–5 graded against the records; repairs after the reading and their continued applicability recorded |
| B18 | §10.3/A6 public identity; §10.5/A12 | Prepared; after deployment | Packet §8.5–§8.6 carry the per-surface public checks and A12's two conditions; nothing public is claimed yet |
| B19 | §10.4 verdict categories | — | This verdict |
| B20 | §11 packet and execution order | PASS | Packet complete (B26); order build → editorial → fresh reader → independent check → upload and verification → final build → recheck → the Orchestrator's steps; the build is non-final now, as it must be before the upload |
| B21 | §12 baseline coverage (the invariants that apply) | PASS | 1 no runtime network (B14, B15); 10 date boundary (B3, command 28); 13 `pyproject.toml`/`uv.lock` unchanged (not in the diff); 14 no new retired-governance narrative (the README diff adds none; the page's one pre-existing mention is unchanged); 16 no placeholder reaches `main` (the `--final` build and §8.3's guard); 22 no colour-only meaning (labels, markers); 24 v1's archive text unchanged except the figures' pixel-identical copies (O25) and the demo route (`tests/test_45` reconstruction); 26 planned work unscored and unnumbered |
| B22 | §13 acceptance record | PASS | Packet §9.2, with this review as the exact-candidate check |
| B23 | §14 pending triggers | PASS | "Before final-candidate test" items decided by decisions 20–21 and rulings O27/O30 and applied (badge, wording, headline window, hero); "Before Live" is CP-18c's |
| B24 | A11 work availability | PASS | Disclosed pauses were usage limits only |
| B25 | The runbook's touchpoints for the comparison's addition, CP-26, CP-28 and the freeze | PASS, with one recorded deviation | Packet §9.3's touchpoints exist in code (registry lists, sources, derived records, claim map, blocks, `PINNED_CHARTS`, export constants, tests). Runbook §9 asks for the release checks over HTTP; the Lead's record ran over `file:` (its `served_over` says so, as review 2's R5 and review 3's R2 noted). My command 30 runs them over HTTP at this candidate (result below), so the gap is closed for this page; the final-SHA record should be made over HTTP (R4) |
| B26 | The packet template, every section | PASS | §§1, 2, 3, 4, 5, 5a, 5b, 5c, 5d, 6, 7, 8 present and filled, plus §§9–10 |
| B27 | r20 §24.14 (quoted above) | PASS | What stays: nothing frozen is touched (no `src/cp17*`, `tests/cp17*`, `reports/cp17*` change; `refreeze verify` prints "verified", command 25); 4.7T's terms published as registered. Item 1: PRES-5 is the publication of the research since v5, A1 in the comparison and the live product. Item 2: no research number uses data after 2026-09-06 (command 28); the report reads no live record. Item 5: no display presents a live score; development displays end by 2026-09-06; the status reads "final candidate · pending 4.7T". Item 6: A1 on v5's data, CP-26 on every development day, CP-28's selection, the freeze with 4.7T's terms, the live product, under PUBLISH_RULES 1.5. Items 3, 4, 7 are CP-18c's or the audit's |
| B28 | Templates §§2–3 | §2: this verdict. §3: the Lead's return | — |

### C. The task-specific supporting extract

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| C1 | CP-18c's paths never touched | PASS | None of `src/cp18/`, `space-product/`, `scripts/build_product_space.py`, `.github/workflows/daily.yml`, `live/`, `tests/cp18c/`, `reports/cp18c/`, `docs/track-b/evidence/cp-18c/`, `exposure-ledger-continued.md` is in `git diff --stat 3c8e158c 48f56b0e` |
| C2 | The Space's address and its wording stand before CP-18c publishes | PASS | `https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast`; packet §8.0/§8.4 state that the Space's content is CP-18c's and the public checks follow both publications |
| C3 | The red line for research | PASS | Command 28; no live record is read by the build |
| C4 | The ceilings (10 machine-hours, ≤ 4 workers, CPU) and a ledger | Not evidenced in the candidate | No machine-hour ledger is committed or cited in the packet; the brief requires the return to name the hours (R6) |
| C5 | Presentation: visual choices the Owner's (O16) | PASS | v6's colour and marker listed for the Owner (packet §10.2–§10.3) |

### D. Applicable constraints

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| D1 | Homebrew `node` stays pinned | Not checkable from the candidate | No PRES-5 file touches it |
| D2 | Credentials | PASS | No value in the candidate (command 21, the value-based scan); the upload reads the stored variables inside the process (packet §6) |
| D3 | Allowed paths | PASS | Every changed path is the page, README, the report's build and tests, the registry and its export drafts, `reports/pres5/`, the build and release-check records or `docs/track-b/evidence/pres-5/` — except O34's two CP-26 tests and their helper, disclosed and ruled (E5). No anchor, governance file, PUBLISH_RULES, frozen record or CP-18c path |
| D4 | Pinned bytes checked before editing | PASS | Command 23: CP-26's harness log handled by O34; `reports/cp17c/inputs.json` disclosed (packet §10.2, N3); no freeze manifest pins a changed file |
| D5 | Tools (start, worktree, `critic-open`/`critic-brief`/`critic-close`, `return`) | PASS so far | This review ran from `critic-brief`'s worktree; `return` is the Lead's |
| D6 | Memory directory not opened | PASS (this review) | Not opened by me |
| D7 | Owner-facing Git non-interactive | PASS | Packet §8's commands (B-row 10) |

### E. The Orchestrator's rulings (conformance only)

| Ruling | Verdict | Evidence |
|---|---|---|
| O25 — the seven archive figures as pixel-identical RGB copies | PASS | Command 8; `tests/test_45`'s reconstruction of v1's chapter with the copies swapped back |
| O26/O29 — "How the product works" documents v6; never says or implies the Space runs v1 now | PASS | `#product` "The product the Space runs, v6 · DDNN-2 alone, topic by topic"; `tests/test_50::test_no_surface_says_the_space_runs_v1_now` with its negative control (both passed in command 15); the README's v1 demo paragraph is dated to its release and in the past tense |
| O27 — the hero and v1's status | PASS | v6 "final candidate · pending 4.7T", the headline CP-28's verdict with the "Development · post-selection" badge; v1 "Released · September 2026", "the last released generation", its demo historical at `/history/`, the product again if 4.7T does not pass |
| O30 — "v6 · DDNN-2 alone", a generation; "A1 in the frozen records"; six arms "not selected" without codes | PASS | B7 and command 27 |
| O34 — CP-26's two landed-code tests | PASS | Command 22: the five snapshots' git blobs equal the blobs at `61658c7` and at `3c8e158c`, their SHA-256 equal the harness log's `landed_code`; every other landed file is still compared with the working tree; the two new modules are excluded by name and are absent from the log; the change is one assertion per test plus the helper; both tests pass (command 15) |

### F. The earlier Integration reviews' acceptance tests (read after my findings)

| Review | Verdict | Evidence |
|---|---|---|
| 1 (FAIL at `b866e996`): the five §7.1 fields from committed records with `test_f03` and its negative controls; §8.2's moved-`main` command; a check on the `evidence/pres-5` date; F4's wording | MET | B12 (values checked against CP-18b's records); §8.2's `xargs` form; `test_the_evidence_tags_date_is_the_tips` and §8.2's date step; "the intervals do not establish that the two are equal" |
| 2 (FAIL at `9bb0cff8`): no README or page sentence says the Space runs v1 now, with a guarded test and negative control; packet §3/§5b/§10.1 describe W49–W53 as the map defines them | MET | O26/O29 row; packet §3 lists W49–W53 as the claim map defines them |
| 3 (FAIL at `f865ff94`): no v6 run tagged adopted; status "final candidate 2026-10-30"; a `tests/test_50` test from the status history with a negative control; export current; 44 → 105 with no published change; packet hashes updated, runs list unchanged | MET | Commands 11, 12, 19; `test_no_export_calls_v6_adopted` and `test_negative_control_a_final_candidate_tagged_adopted_is_caught` (passed in command 15) |

## Existing-rule violations

None established at this candidate.

## Open items for the Orchestrator (not violations)

- **O-1. A8's trigger** (B8): rule on packet §10.3 item 1 before the final build.
- **O-2. One product name across surfaces** (B13): after both publications, A12's useful check should confirm that
  CP-18c's Space shows "v6 · DDNN-2 alone" (O30); CP-18b's landed claims still say "A1 · DDNN-2 alone".
- **O-3. The focused recheck at the final SHA**, after the upload, the mirror verification, the routes, the index and
  the `--final` build, including the `evidence/pres-5` label's date (now "2026-11-06"), which §8.2 sets and checks.

## Product recommendations (not violations)

- **R1.** The every-day panel says "v6's forecasts have the lowest error on both scores". That holds among the
  re-baseline's policies in its table, but CP-28's "Fitted blend weights, unshrunk" arm had the lower every-day point
  error on the same days (17.10 against 17.19 EUR/MWh, −7.4% against −6.9% of v5's). Scope the sentence, for example
  "the lowest error of the re-baseline's policies".
- **R2.** `v6.fresh.terms`: "The p-values come from a 7-day block bootstrap with 10,000 draws" would match the protocol
  (§6); no interval is registered for 4.7T. (Review 2's R4 made the same point.)
- **R3.** The comparison's values table shows `A1` for v6 and for CP-15's normalized LEAR, with no experiment beside
  either; name the experiment as the "DDNN member on v4" row does.
- **R4.** Make the final-SHA release record over HTTP, as runbook §9 asks, and bind the page's SHA-256 in it.
- **R5.** Give the every-day panel its question in a sentence (the brief's outcome 2 names it), for example "Do the
  five-period results hold when every eligible day is scored under one daily protocol?".
- **R6.** The return must name the machine-hours used against the 10-hour ceiling; the candidate carries no ledger.
- **R7.** "Either way the live record stays 'prospective evaluation in progress' until at least 90 consecutive days
  are scored": on a fail v1 is the product again, and decision 21 places CP-19's 90 days after a switch; consider
  wording that holds on both branches.
