# Verdict — PRES-5 — Integration (review 3) — FAIL

- **Candidate SHA:** `f865ff94788df4931de9ed78a65c99c94180f80c` (`gauntlet/pres-5`; base `main` = `3c8e158c9895f5b3fed13db794b0ddd5fb80c56f`)
- **Plan / version / bar:** `capstone_v21.md` v21-r20 (SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`),
  §24.14 "Publishing and going live before 4.7T (v21-r20)" (section 115 lines, 7426 bytes, SHA-256
  `5d38de24b3c68ec01e2f5c4e6eaf368c253485107549fc2d85c3c71ccf2f5349`); `docs/PUBLISH_RULES.md` revision 1.5
  (`1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`) in full; the brief
  `docs/track-b/evidence/pres-5/issued-brief.md` (`9eb2a58433f41739fc22744854c4c55b099cc05ca729b677e9b3b5ccef87ebc3`).
- **Verbatim bar excerpt** (the excerpt is the citation; any line number is a courtesy and is non-binding). Extracted
  with `scripts/bar.py bar --at f865ff94… --quote capstone_v21.md "### 24.14 …"` and checked with
  `bar.py check … --source capstone_v21.md@f865ff94…` → `ok: lines 1–115 (7425 bytes) appear in capstone_v21.md@f865ff94788d`.
  The full section, verbatim:

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

- **Worktree clean before and after:** yes. `git -C …/critic-3 status --porcelain` empty and `HEAD` =
  `f865ff94788df4931de9ed78a65c99c94180f80c` before the review, after every rebuild, and after writing this verdict.
  Only ignored byproducts were created (`.venv/`, the browser payload). No Git write of any kind was made.
- **Independence:** I authored none of PRES-5. I formed the findings below before reading `integration-review-1.md`,
  `integration-review-2.md`, `editorial.md` and `fresh-reader.md`. I did not open the Claude memory directory,
  `progress.md`, any syllabus, Track A or C material, or `docs/track-b/orchestrator-role.md`. No credential value was
  read, printed or typed; MLflow telemetry was disabled in every shell (`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1`).

## Commands actually run

All from `/Users/djourno/Downloads/PJM/.local/worktrees/pres-5/critic-3` (W) unless stated; scratch scripts and
outputs in the session scratchpad, outside the worktree.

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief pres-5` (lead worktree) | 0 | This review's brief |
| 2 | `git -C W status --porcelain; git -C W rev-parse HEAD; git -C W diff --stat 3c8e158c f865ff94` | 0 | empty; `f865ff94…`; 66 files, +42,276 / −329 |
| 3 | `git show f865ff94:<f> \| shasum -a 256` for `capstone_v21.md`, `docs/PUBLISH_RULES.md`, the issued brief, `owner-decisions-2026-11-05.md` | 0 | `80341681…30e6`, `1bc0c523…f94e`, `9eb2a584…ebc3`, `4daa5617…0215`: all as pinned |
| 4 | `git show main:scripts/bar.py \| python3 -I - bar --at f865ff94… --quote capstone_v21.md "### 24.14 …"`, then `… check <it> --source capstone_v21.md@f865ff94…` | 0, 0 | identity line `80341681…; section 115 lines, 7426 bytes, 5d38de24…`; `ok: lines 1–115 (7425 bytes) appear` |
| 5 | `shasum -a 256` of the brief's 18 execution inputs (PRES-4 packet, PRES-4 closure, CP-26 landing/report/export, CP-28 landing/report/packet/export draft/forecast manifest, CP-17/17b/17c landings, the 4.7T protocol, runbook, packet template, advisory log, CP-18b landing) | 0 | every hash equals the brief's table |
| 6 | `uv run python -m delu_forecast.final_candidate --check` | 0 | `{"identical_to_committed": {metrics.csv, parity.json, preview-day.csv, ratio-intervals.csv, summary.json, uncertainty.csv: true}}` |
| 7 | Independent recomputation (my own script, `pandas` only, no project scoring code): A1's `q50`/quantiles from `reports/cp28/forecast/hourly.parquet` on v5's keys from `reports/ddnn2/attempt-1/predictions.parquet`, B0 from `reports/weather-ablation/predictions.parquet` | 0 | 0 missing A1 keys of 10,747, 0 missing B0, truth identical; per-fold MAE 4.5178 / 7.0506 / 43.1925 / 13.0924 / 13.3715 and per-fold seven-quantile WIS 2.476356 / 3.972142 / 23.755410 / 7.374746 / 7.569888, equal to `metrics.csv`; S_MAE A1 0.4928063413559065, v5 0.5223212760431432, ratio −5.651%; pooled 95% coverage 0.9447, mean width 82.42 EUR/MWh, pooled MAE 16.1265; 0 quantile crossings in 56,886 non-null rows; store ends 2026-09-06 |
| 8 | `uv run python -m delu_forecast.compact_figures --check` | 0 | `{"pixel_identical": true, "problems": []}` |
| 9 | `uv run python scripts/mlflow_export.py --check` | 0 | `the committed export is current` |
| 10 | `uv run python scripts/mlflow_export.py --diff-against 3c8e158c` | 0 | `runs 44 -> 105` (the 61 cp26/cp28 keys added); params 362, metric points 16,753, datasets 90, artifacts 107 all unchanged; `identity changes on 0 runs; substantive changes: none; only_identity=True`; equals `pres-5-export-diff.json` |
| 11 | `uv run python scripts/build_pages.py`; `git status --porcelain` | 0; empty | `docs/index.html (1,848,377 bytes)`; SHA-256 `409e1708055b3a91d768ab2ebc0bd527ac63384278b3d971b8843180e1641cbe`; `pages_build.json` `final: false`, `links_omitted_until_verified: ["compare:v6"]` |
| 12 | `uv run python scripts/readme_research.py`; `uv run python scripts/cp3_readme.py`; `git status --porcelain` | 0, 0; empty | README SHA-256 `369eefa84ec02158ffa2b9e2a832c18b14165e461258e9b87e49bd9f2c9676a2`, unchanged |
| 13 | `uv run python scripts/lint_publication.py` | 0 | page, readme, templates: 0 findings; `PASS` |
| 14 | `uv run python scripts/build_wasm_payload.py`; `git status --porcelain` | 0; empty | payload written (ignored) |
| 15 | `uv run pytest -q -p no:cacheprovider` (whole suite, Python 3.13.15) | 1 | `2 failed, 3240 passed, 9 skipped in 1294.09s`; the two failures are `tests/cp18a/test_dry_run.py::test_a_real_dry_run_then_the_fallback_finds_the_day_claimed` and `tests/cp18a/test_forced.py::test_each_cause_is_forced_and_recorded`, both `publication-guard: BLOCKED … reports/cp3/pages_build.json is a non-final build record (final: false)`, as the brief predicts; every `tests/test_50` test passed |
| 16 | Python reads of `reports/cp28/publication-packet.json` (`arms`, `headline`), `results/selection.json`, `owner-summary.json` (`holm`), CP-26's `MLflow-export.json` and `presentation-v21-r16/publication-packet.json` | 0 | every arm's ratio and interval, A1's WIS 9.68 against A6's 10.13, tie bound 9.73, all seven `passes_all_four`, Holm-adjusted p 0.0042 (A1) and 0.0007 (others), CP-26's every-day losses and ratios, v5−v4 −0.66% [−1.41%, +0.94%] (MAE): each equals what the page renders, rounded |
| 17 | `git rev-parse 61658c7:<m>`, `git rev-parse 3c8e158c:<m>`, `git hash-object <snapshot>` for the five O34 modules | 0 | all three blobs equal for each module; the snapshots' SHA-256 equal `reports/rebaseline/harness-log.json` `landed_code` |
| 18 | `git diff --stat 3c8e158c f865ff94 -- src/cp26 reports/rebaseline docs/track-b/evidence/cp-26 src/cp17* reports/cp17c tests/cp17c docs/track-b/evidence/cp-17c reports/cp28 docs/track-b/exposure-ledger.md src/cp18 space-product scripts/build_product_space.py .github live tests/cp18c reports/cp18c docs/track-b/evidence/cp-18c docs/track-b/exposure-ledger-continued.md pyproject.toml uv.lock AGENTS.md CLAUDE.md engineering-role.md orchestrator-role.md docs/PUBLISH_RULES.md capstone_v21.md .claude` | 0 | empty: no CP-18c path, frozen record, CP-26/CP-28 record, dependency file, anchor or governance file changed |
| 19 | For every changed non-PRES-5 path, `git grep -l -F <path> f865ff94 -- '*.json' 'src/cp26/harness.py' '*manifest*'`; the CP-17/17b/17c freeze manifests walked for those paths | 0 | binding references only in CP-26's harness log (O34) and `reports/cp17c/inputs.json` (disclosed N3, compared by nothing); no freeze manifest pins any of them |
| 20 | `uv run python scripts/mlflow_publish.py --dry-run` | 0 | `dry run: 105 runs, 17003 metric points, 229 artifacts; outbound scan clean; export current at f865ff94788d` |
| 21 | Packet §6's `--authorized-runs` list, sorted, `diff` against the run keys of `cp26.json` + `cp28.json` | 0 | identical: 61 keys; `--authorized-experiment-tags mlflow.note.content` only; `--precheck` first; `mlflow_publish.py` unchanged since `3c8e158c` |
| 22 | My probe of the export (`delu_forecast.registry`, `research_claims.withheld_findings`) over every run name, tag and param of `cp26.json` and `cp28.json` | 0 | **v6's five runs `cp28/A1`, `cp26/nominal/D2/{all_eligible,never_scored,old_fold_2_5,newly_opened}` carry `delu.adopted = "true"`**; registry v6 status history `[('final candidate', '2026-10-30')]`; `G.adopted_flag(v6)` = `"true"`; no W49–W53 pattern in any export string |
| 23 | Tags of `cp-28/A1` in `reports/cp28/MLflow-export-draft.json`; `grep -i adopt reports/cp28/publication-packet.md` | 0 | the draft carries no adoption tag; CP-28's packet: "Transition: none: CP-28 adopts no generation; the selection is a freeze candidate for CP-17" |
| 24 | `check_links.main(record=None, gated=False)` imported from `scripts/check_links.py` (anonymous, read-only network; the tracked record not written) | 1 | 56 destinations answered 200; 2 answered 404, both `blob/evidence/pres-5/reports/pres5/a1-in-v5/{metrics.csv#L8,uncertainty.csv#L22}` (the tag is not pushed yet; packet §10.3 item 5). Line 8 and line 22 are A1's equal-fold row and A1−v5 MAE row |
| 25 | `xargs git --no-pager diff --quiet <a> <b> -- < paths` with the 66 PRES-5 paths, `a=b=f865ff94` and `a=3c8e158c b=f865ff94`, on git 2.50.1 | 0, 1 | the packet's §8.2 "(main moved)" form parses and fails closed on a difference |
| 26 | `git log -1 --format=%cs -- reports/pres5/a1-in-v5`; `grep '"evidence/pres-5"' src/delu_forecast/registry.py`; `git rev-parse`/`git log -1 --format=%cs` of `land/cp-26`, `evidence/cp-28`, `evidence/cp-17`, `-17b`, `-17c` | 0 | rows 2026-11-05; label date 2026-11-06 (set at the final build, packet §8.2); the five tags' SHAs and dates equal `EVIDENCE_TAGS` |
| 27 | `brew list --pinned` | 0 | `node` pinned |
| 28 | `PLAYWRIGHT_BROWSERS_PATH=… .local/tools/playwright/bin/python scripts/check_reader_paths.py release docs/index.html --shots /Users/djourno/Downloads/PJM/.local/artifacts/pres-5/critic-3/shots --out /Users/djourno/Downloads/PJM/.local/artifacts/pres-5/critic-3/release.json` | 0 | `passed=True` (10:01–10:09 UTC, page `409e1708…1cbe`, served over `file`): Chrome and WebKit at 1440×900, 768×1024, 390×844, 360×780, 320×640; accessibility trees passed in both engines at 1440 and 390; A5 discovery 48 routes in each engine at both sizes; Chrome placements: headline bottom 800.6 px (1440×900) and 628.6 px (390×844), finding 1,672.6 px (A2 limit 1,744) and 2,394.5 px (limit 2,420); smallest chart text 12.38 px (1440), 14.58 px (390); no overflow closed or open, at 200% zoom or at 320 px reflow. Record and screens at `/Users/djourno/Downloads/PJM/.local/artifacts/pres-5/critic-3/{release.json,shots/}` (local only) |

## Evidence actually inspected

- **Governing text:** the brief in full; `capstone_v21.md` §24.14 (extracted), §24.7 "What CP-26 claims", "CP-28's
  frozen protocol", "Outputs, gates and publication", §24.8 in full; `docs/PUBLISH_RULES.md` §§1–14 and A1–A12;
  `docs/track-b/publication-standard-v1.md` §§2–3; the presentation plan's tag list (§10, `delu.adopted`);
  `owner-decisions-2026-11-05.md` (decision 28) and `owner-decisions-2026-10-29.md` (decisions 20–21); the 4.7T
  protocol §§1–8 and its CP-17b revision's diff.
- **The packet** `publication-packet.md` in full (§§1–10.4), against the template's section list.
- **Code:** `src/delu_forecast/final_candidate.py` (all); `derived.py` diff; `registry.py` (`adopted_flag`,
  `final_candidate`, `current_generation`, `EVIDENCE_TAGS`, v6's entry); `research_claims.py::WITHHELD_PATTERNS`
  W49–W53 and the `everyday.*` blocks; `scripts/build_pages.py::live_measurement` and `opening`;
  `scripts/cp3_readme.py` diff; `scripts/mlflow_export.py` (`delu.adopted` sites); `scripts/mlflow_publish.py`
  (docstring, `main`); `scripts/check_links.py`; `tests/pres5_landed_code.py`; the two CP-26 test diffs;
  `tests/test_50_pres5_publication.py` (export, withheld-claim, O34, evidence-date and Space-runs-v1 tests);
  `tests/test_43` F03 tests.
- **Records:** `reports/pres5/a1-in-v5/*` (summary, metrics line 8, uncertainty lines 22–23, parity);
  `reports/cp28/{publication-packet.json, results/selection.json, owner-summary.json, MLflow-export-draft.json,
  publication-packet.md}`; CP-26's `MLflow-export.json` and r16 packet `comparisons`;
  `reports/presentation/mlflow-export/{cp26,cp28,manifest}.json` (names, tags, notes, experiment note);
  `release-checks/pres-5-export-diff.json`, `pres-5-pre-final-4-prerelease.json`, `pres-5-local-release.json` (keys,
  `passed`, `checked_at_utc`, `served_over`); `reports/cp3/pages_build.json` and its diff;
  `docs/track-b/evidence/pres-5/cp26-landed-presentation-code/manifest.json`; `reports/rebaseline/harness-log.json`
  (`landed_code`); the CP-17, CP-17b, CP-17c and CP-18b landing records (identity, host, 58 of 58, first-visit size).
- **Rendered surfaces:** the page's full text with disclosures' contents (my extraction), the opening, the startup
  line's raw markup, every Space link with its context, every `A2`–`A7` occurrence (all inside attributes or CSS, none
  visible), the v6 chapter, the arms table, the every-day panel, the transition and the 4.7T terms; the README diff in
  full.
- **Local only:** `/Users/djourno/Downloads/PJM/.local/artifacts/pres-5/land-commit-message.txt` (named by packet §8.2).

## Checklist verdict

### A. The brief's observable outcome

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | A1 (v6) in v5's comparison: v5's population (10,747 h, 448 days, five periods, equal weights, the naive denominator, the same interval method); A1's forecasts from CP-28's store; coverage and information-set differences stated; other rows v5's published rows, not recomputed; paired comparisons v6−v5 and v6−B0 with the rule's intervals; never "adopted" by v5's rule; every value derived | PASS on the page and README; **the MLflow surface violates "never adopted" (F1)** | Commands 6, 7, 16: my recomputation with no project scoring code equals `metrics.csv` per fold and the equal-fold scores (S_MAE 0.4928063 vs 0.5223213, −5.65%); 10,747/10,747 keys, 448 native days, no fallback; `parity.json` 0.0; CP-20's index set (`index_equals_cp20` true). The page: "−6% [−9%, −2%] … −11% [−15%, −8%] … at 97.5% … [−10%, −2%] and [−15%, −8%]"; naive −51% / −56%; "A description, not a decision: v5's adoption rule was not re-run"; information set and the 2020 warm-up on the reading path. F1 below |
| 2 | CP-26 on every development day: question, population, results, evidence class; beside the five periods, never pooled | PASS | `#everyday`: "A separate population: 2,068 eligible days from 2020-12-29 to 2026-09-06 … never pooled with the five periods above · development, post-selection"; table values equal CP-26's export (command 16); v5−v4 "−1% [−1%, +1%] … the intervals do not establish that the two are equal" |
| 3 | CP-28's selection: arms, rule, result, why A1 | PASS | v6 chapter "How v6 was selected" and the arms table; every value equals CP-28's records (command 16); the conditional Holm control disclosed ("The selection was run only after the Owner saw the re-baseline's report …") |
| 4 | The freeze and 4.7T's registered terms; pass/fail meaning | PASS | `#v6-freeze`, `#v6-fresh-test` against CP-17/17b/17c landings (720fc581, 58 of 58, Pyodide 0.28.0 in Node.js v26.7.0, 2026-10-28/29/30) and protocol §§1–8 (window, control v5 and reference B0 under CP-26's rules, descriptive v3/v4/v1, MAE and WIS, four one-sided endpoints with 0.995·v5, compound ≤ 0.05, 7-day blocks, 10,000 replicates, ≥ 60 of 90, no runner-up, window spent, null valid). CP-17b's revision touches only §3/§11 and additions to §4/§7, none of the quoted terms. Meaning: decisions 20–21 as decision 28 leaves them (O29) |
| 5 | The product: opening pairs A1 "final candidate · pending 4.7T" with the product; links the live Space and says what it is; v1's historical demo at `/history/`; no live number, nothing after 2026-09-06 | PASS | Status pair "Live product · v6 · DDNN-2 alone" / "Final candidate · pending 4.7T"; product line with decision 28's reason; "Open the live product" → `huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast`; "v1's historical demo" → `…static.hf.space/history/`; the preview is the labelled development day 2026-04-07; `test_24`, `test_50` pass |
| 6 | Model identity (§4): public name and status; unselected arms as study arms / branch cards | PASS on the page and README; MLflow's adoption tag is F1 | "v6 · DDNN-2 alone", generation (O30), "final candidate 2026-10-30", "A1 in the frozen records" beside the identity; the six others named in words, "Not selected", no visible code (every `A2`–`A7` on the page is in an attribute or CSS) |
| 7 | MLflow: exports prepared exactly as authorized (export, its diff against the published set, the bounded command); upload after the verdict | **FAIL** (F1) | The mechanics are right: commands 9, 10, 20, 21 (current; 44 → 105, no change to any published run; the 61-key authorized list equals the export; one experiment-tag write). But the export the upload would publish tags v6's five runs `delu.adopted = "true"` (command 22), contradicting W49, the registry's own status history and CP-28's record (command 23). Under the brief's limits a published run cannot be changed afterwards |
| 8 | The page budget | PASS | 1,848,377 bytes ≤ 2,000,000 (command 11), by O25's pixel-identical re-encoding (command 8) |
| 9 | Review: independent check passes at the candidate; focused recheck at the final SHA | FAIL (this verdict) | — |
| 10 | The packet's §8: exact payloads and ready-to-run commands for the LAND, the push, the public checks with `publication_receipt.py`, A12 | PASS | §8.0–§8.7; non-interactive (`--no-pager`, `-F` message file, which exists); the `xargs` form runs on git 2.50.1 (command 25); the date step (F3/N2) fails closed; the secret scan precedes the push; A12's two conditions and its useful check named |

### B. The complete authoritative bar

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| B1 | PUBLISH_RULES §1.1–§1.3: authority, four identities, categories | PASS with F1 | Rules, anchor, brief and decision pinned and verified (commands 3, 5). The four identities are kept apart on the page and README; MLflow's `delu.adopted` conflates "final candidate" with adoption (F1) |
| B2 | §2 reader contract; A1; A2 | PASS | Each headline percentage names its metric ("in point error", "in interval error", "as shares of v5's, with descriptive 95% intervals"); terms directly beneath; placements: command 28 |
| B3 | §3.1 evidence classes; withheld claims (W1–W53) | **FAIL** (F1) | Development · post-selection on every v6, CP-26 and CP-28 number; nothing live or 4.7T's. W49 holds on the page and README (`test_the_withheld_claims_are_guarded`) but not in the MLflow export, which no W-guard reads |
| B4 | §3.2 scores, comparisons, uncertainty | PASS | Pre-specified verdict with rule, date, distance and N = 7; ratio intervals from CP-24's draws at 95% and 97.5%; absolute MAE with the 2022 period apart; separate population for CP-26; null not read as equivalence |
| B5 | §3.3 counting | PASS | N = 7 (the rule's), 13 rows, 25 in the targets' census, each labelled |
| B6 | §3.4 provenance and formatting | PASS | Every number a record (`validate_all`, lint 0 findings, command 13); whole percents; one decimal for EUR/MWh |
| B7 | §4 registry, transitions, branches; A3; A10 (n/a) | PASS on page/README; F1 on MLflow | One registry; "From v5 to v6" with predecessor, change, comparator, result with class, limits, dated decision and route; A10 not applicable |
| B8 | §5 architecture, A4; §5.1 twelve subjects; §5.2 grammar and budget | PASS | A4's order; "How the product works" documents v6 (O26/O29) with all twelve subjects dispositioned (packet §5b checked against the page); v6's chapter fills every slot |
| B9 | §5 A8 product-first order; §5.1a | Not graded (open item) | Packet §10.3 item 1 proposes that A8 applies at 4.7T's release; an applicability question for the Orchestrator under decision 27 (decision 21 makes the release depend on 4.7T) |
| B10 | §6 charts and discovery; A5 | PASS | v6's main chart with both scores at 95% and 97.5% and a values table; routes: command 28 |
| B11 | §7.1 product contract (startup metadata beside the action) | PASS | Size, measured start (1.86 s), Chromium 153 / WebKit 26.6, machine, date and last verification, each bound to CP-18b's records by `data-release-check` pointers, beside "Open the live product", outside any disclosure; `test_43` F03 and its negative controls |
| B12 | §7.2 / A7, §7.3 / A9 | Not this block's surface | The report shows no live panel or number; the Space is CP-18c's |
| B13 | §8 surfaces agree; README; MLflow registry-driven | **FAIL** (F1) | Report and README agree (v6, final candidate, never adopted). MLflow disagrees on status for v6's five runs |
| B14 | §9 browser and accessibility matrix | PASS | Command 28; packet §7's record `pres-5-local-release.json` (passed, both engines, every width) is at this page by its date (`checked_at` 00:07 UTC after `d487b4bd`, page unchanged since) but binds no page hash |
| B15 | §10.1 independence; §10.2 fresh reader; §10.3/A6; §10.4; §10.5/A12 | PASS / after deployment | Editorial, fresh reader and three integration reviews by non-authors; the fresh reader's answers 1–5 agree with the records I re-derived; continued applicability recorded; A6/A12 are the Orchestrator's steps (§8.5–§8.6) |
| B16 | §11 packet and order; no non-final build on main | PASS | The order is followed; the build is non-final and the guard blocks it until `--final` (command 15's two failures) |
| B17 | §12 baseline coverage (invariants 1–26) | PASS | Inv. 10: no research number or chart after 2026-09-06 (CP-28's store ends 2026-09-06; `test_research_numbers_use_development_days_only`); inv. 13: `pyproject.toml`/`uv.lock` unchanged; inv. 14: no retired-governance narrative added (the one "Integration Critic" mention is v1's protected text, present at the base); inv. 3: rebuilds reproduce byte for byte |
| B18 | §13 acceptance record | PASS | Packet §9.2 |
| B19 | §14 pending triggers | PASS | "Before final-candidate test" decided by decisions 20–21 and O27/O30; "Before Live" CP-18c's |
| B20 | A1–A12 one by one | A1 PASS, A2 PASS (command 28), A3 PASS, A4 PASS, A5 PASS (command 28), A6 after deployment, A7 n/a here, A8 open item, A9 CP-18c's, A10 n/a, A11 PASS, A12 named in §8.6 | as above |
| B21 | The runbook, every touchpoint | PASS | `CHECKPOINTS` (CP-26, CP-28), `EVIDENCE_TAGS` (five tags verified against git, command 26), `RULES`, `POPULATIONS`, `COMPARISON_ORDER`, claim map registered, `PRES5_EXPORTS`, `EXPERIMENT_NOTE_CHECKPOINTS`, tests |
| B22 | The packet template, every section | PASS | §§1–8 with 5a–5d present and filled; §§9–10 added |
| B23 | §24.14 items 1–8 and "What stays exactly as registered" | PASS | Item 1 order: PRES-5 publishes beside CP-18c; item 2: no research path or record after 2026-09-06 touched, the exposure ledger untouched (command 18); items 4–5: no live record shown, status "final candidate · pending 4.7T", "prospective evaluation in progress", development displays through 2026-09-06; item 6: all five covered, development data only, under rules 1.5; A1's freeze and 4.7T's terms untouched (command 18) |
| B24 | Templates §§2–3 | PASS | Packet and this verdict follow §2; the return is the Lead's |

### C. Task-specific extract and applicable constraints

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| C1 | CP-18c's paths never touched | PASS | Command 18 |
| C2 | The Space's address and wording | PASS | `https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast` on the page and README |
| C3 | Red line for research; the report reads no live record | PASS | B17; `test_24`; no `live/` or CP-18c record read by the build |
| C4 | Ceilings: ≤ 10 machine-hours, ≤ 4 workers, CPU only, a ledger kept | Not verifiable from the candidate | No ledger is committed; the packet records the prerelease's 46 minutes. The return must name the machine-hours (brief) |
| C5 | Presentation: the existing tokens; visual choices the Owner's | PASS | v6's colour and hexagon recorded as O16 choices (§10.3 item 3) |
| C6 | Homebrew `node` pinned | PASS | Command 27 |
| C7 | Credentials | PASS | No value in any changed file (the publisher's outbound scan clean, command 20; hooks on every commit) |
| C8 | Allowed paths | PASS | All changes are in `docs/index.html`, `README.md`, the report's build and its tests (including the README's generator `scripts/cp3_readme.py`), `docs/track-b/research-content/`, the registry and the export it drives, `reports/pres5/`, the release-check records and `docs/track-b/evidence/pres-5/`; the two CP-26 tests under O34 |
| C9 | Pinned bytes checked before editing | PASS | Command 19: CP-26's harness log handled by O34; `reports/cp17c/inputs.json` disclosed (N3); no freeze manifest pins a changed file |
| C10 | Tools, memory, non-interactive Owner commands | PASS | The candidate chain and review files exist as the tool expects; §8's commands are non-interactive |

### D. The Orchestrator's rulings

| Ruling | Verdict | Evidence |
|---|---|---|
| O25 | PASS | Command 8; `test_a_changed_pixel_is_caught` passed |
| O26/O29 | PASS | "How the product works: The product the Space runs, v6 · DDNN-2 alone"; decision 21's fail branch in `v6.fresh.meaning`; no surface says the Space runs v1 now (`test_no_surface_says_the_space_runs_v1_now` and its negative control pass; the README's CP-3 paragraph is dated and past tense) |
| O27 | PASS | Hero "Final candidate · pending 4.7T" with CP-28's verdict and the development post-selection badge; v1 "Released · September 2026", "the last released generation", its demo at `/history/` |
| O30 | PASS on page and README; F1 on MLflow | The public name, generation kind, "A1 in the frozen records", six arms "Not selected" without visible codes. O30 makes v6 a generation; it does not make it adopted, and W49 withholds that |
| O34 | PASS | Command 17: the five recorded copies equal `61658c7`'s and `3c8e158c`'s blobs and the harness log's SHA-256; every other landed file is still compared with the working tree; negative controls for a changed copy, a copy that no longer matches the log and another landed file; the two new modules excluded by name; no CP-26 record, manifest or harness file changed (command 18) |

### E. The earlier reviews' acceptance tests

| Test | Verdict | Evidence |
|---|---|---|
| Review 1: the startup line's five §7.1 fields from committed records, `test_f03` with negative controls; §8.2's command for a moved `main`; a check on the `evidence/pres-5` date; F4's wording | MET | B11; command 25; `test_the_evidence_tags_date_is_the_tips` and §8.2's date step; the every-day panel: "the intervals do not establish that the two are equal" |
| Review 2: no README sentence saying the Space, its root or its app runs v1 or its champion now; a `test_50` check on README and page with a negative control restoring the sentence; packet §3, §5b and §10.1 describe W49–W53 as the claim map and code define them | MET | Commands 12, 15; the README's CP-3 paragraph reads "At v1's release, the Space could not load … The app alone was then at … v1's demo is now under the Space's History"; packet §3 lists W49–W53 as the claim map does (W53 without the claim map's last clause, which no code guards); §5b and §10.1 cite the separate test, not W53 |

## Findings (PUBLISH_RULES §10.1)

### Existing-rule violations

**F1 (medium; decides this verdict). The MLflow export tags v6, the final candidate, as adopted.**
- **Clauses:** PUBLISH_RULES 1.5 §3.1 ("Preserve withheld claims … through their controlling claim maps"), with PRES-5's
  claim map W49 ("Calling v6 (A1) 'adopted' or 'adopted in research'", `pres5-claims.md`); §8 ("The report, README,
  Space card, direct demo and MLflow must agree on identity, status …"; "MLflow: registry-driven names,
  descriptions, tags and parents"); §1.2 (product status: adopted in research, released, final candidate … kept
  apart); the brief's outcome 1 ("A1 is never 'adopted' by it") and outcome 7.
- **Observation:** `reports/presentation/mlflow-export/cp28.json` run `cp28/A1` and `cp26.json` runs
  `cp26/nominal/D2/all_eligible`, `…/never_scored`, `…/old_fold_2_5`, `…/newly_opened` (registry id `v6`, kind
  `generation`) carry the tag `delu.adopted: "true"` beside `delu.status: "final candidate 2026-10-30"` (command 22).
  The value comes from `registry.py::adopted_flag`, which returns `"true"` for every status except "not adopted" and
  "retired", so the first "final candidate" in the registry inherits it. v6's registry history holds no adoption
  event (packet §2: "No adoption event: v5's rule never ran on it (W49)"); CP-28's own record says "CP-28 adopts no
  generation", and its draft export carries no adoption tag (command 23). The page and README say "selected by its own
  rule, never adopted by v5's". `test_the_withheld_claims_are_guarded` reads only the page and README, and
  `test_the_cp26_and_cp28_exports_mirror_their_drafts` compares metrics, so nothing checks the tags.
- **Impact:** the public tracking record, which the report links as its evidence, would state that v6 was adopted,
  contradicting the report, the README and the claim map. The upload follows this review directly, and the brief
  forbids changing a published run afterwards, so the tag would stay public until a separate authorization.
- **Repair:** make `adopted_flag` (or the export) return not `"true"` for an entry whose status history has no
  adoption event, for example `"false"`, keeping `delu.status` "final candidate 2026-10-30"; regenerate the export;
  add a `tests/test_50` assertion on v6's runs with a negative control.

### Product recommendations (not violations)

- **R1.** "Selected by a rule set before any result" (headline) and "Selection rule: set on 2026-10-12, before any
  result" are true of CP-26's every-day scores, which the rule preceded, but DDNN-2 alone's five-period results (CP-24,
  published 2026-10-11) existed when the arms were set on 2026-10-12. The chapter's precise form, "set on 2026-10-12
  and frozen before the re-baseline's first score", would remove the ambiguity; the post-selection caveats are already
  on the reading path (the fresh reader's observation 7 reached the same point).
- **R2.** `pres-5-local-release.json` still records its page as `docs/index.html` without a SHA-256 (review 1 noted
  this). At the final SHA, bind the page hash in the release record, and run it over HTTP as review 2's R5 asks.
- **R3.** The packet has no machine-hour ledger; the return must name the hours used against the 10-hour ceiling.
- **R4.** Packet §3's W53 omits the claim map's last clause ("or calling the prospective record an evaluation
  result"), which no pattern guards; state that it is a review check, as §2 does for `A1`.

### Not graded

- A8's product-first order (packet §10.3 item 1): the Orchestrator's applicability ruling.

### Comparison with the earlier reviews (read after these findings)

- Neither integration review nor the editorial review examined the export's `delu.adopted` values; review 2 read the
  export's "names, tags, notes" and passed outcome 7 on the mechanics (authorized list, diff), as I do. F1 is new.
- Review 1's and review 2's acceptance tests are met (section E). Their recommendations on the GFS attribution, the
  CP-3 table's row 1 and the v1 Space cards remain recommendations.
- The fresh reader's observation 7 is R1; its disposition ("both are true") is accurate for the every-day scores.

## On FAIL only

- **Single largest meaningful gap:** the MLflow export that the authorized upload would publish tags v6's five runs
  (`cp28/A1` and `cp26/nominal/D2/*`) `delu.adopted = "true"`, although v6 has no adoption event, CP-28 "adopts no
  generation" and the claim map withholds calling v6 adopted (W49); once uploaded, the brief forbids changing those
  runs.
- **Exact next acceptance test:** at the next candidate, no run in `reports/presentation/mlflow-export/cp26.json` or
  `cp28.json` whose registry entry has no adoption event carries `delu.adopted = "true"` (v6's five runs show the
  chosen value, for example `"false"`, with `delu.status` "final candidate 2026-10-30"); a `tests/test_50` test
  asserts this from the registry's status history, with a negative control in which a final candidate without an
  adoption event mapped to `"true"` is caught; `mlflow_export.py --check` reports the export current;
  `mlflow_export.py --diff-against 3c8e158c` still shows 44 → 105, the 61 added, no identity or substantive change to
  any published run and the one experiment-tag change; packet §6 and §8.0 carry the new export hashes, and the
  authorized-runs list is unchanged.
