# Verdict — PRES-5 — Integration — PASS

- Candidate SHA: `300926def8a841848ad02a74c25a5e0291b37f20` (`gauntlet/pres-5`, committed 2026-11-13 22:27:10 +0200).
  Its only parent is `48f56b0ef7f7bcf3fa16778cd69a7ea8eebae2e2`, the candidate that Integration review 4 checked.
- Plan / version / bar: `docs/PUBLISH_RULES.md` at `300926de…`, file SHA-256
  `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`. The bar is "## 13. Acceptance record for a
  future publication": 28 lines, 2,964 bytes, SHA-256 `cb175c9675dc787c060a1cbb0e896a19f2362d390b3e06326522d472b29a507e`.
  I extracted the section at the SHA and hashed it again; the text is byte-equal to the excerpt in my assignment.
- Inputs bound by hash, all re-hashed here:
  - the brief `docs/track-b/evidence/pres-5/issued-brief.md`, `9eb2a58433f41739fc22744854c4c55b099cc05ca729b677e9b3b5ccef87ebc3`;
  - Integration review 4's verdict `/Users/djourno/Downloads/PJM/.local/artifacts/pres-5/critic-4/integration.md`,
    `fce6c28c246b0420b593b6666002d2c23605662260f2617bb7ad7d4364a6a197`, a PASS at `48f56b0e…`.
- Final page identity (the packet's `<final_page_sha256>` slot): `docs/index.html` at `300926de…` is 1,848,925 bytes,
  SHA-256 `2fc5bd0a2946719667624dec1e09932c54457de2660a61946dda53e33eb6e28b`.
- Verbatim bar excerpt (the excerpt is the citation; any line number is a courtesy and is non-binding):

> ## 13. Acceptance record for a future publication
>
> One review record can carry this matrix; duplicate certificates are unnecessary:
>
> | Area | Required record |
> |---|---|
> | Authority | Effective rules/hash; research anchor; brief; applicable clauses and justified N/A triggers |
> | Identity | Local branch/SHA/tree state; final candidate; landing/service revisions; served hashes |
> | Claims | Source rows/hashes, derivations, classes, comparator/population, count census, limitations |
> | Reader | Default path/screens, placements, definitions, unchanged six-question fresh-agent record |
> | Journey | Adopted transitions, rejected branches, plans; no implied unperformed experiment |
> | Content | Twelve active-product subjects, applicability, product-replacement migration, concise research histories, protected archive and approved contribution |
> | Charts | Rendering, semantics, mobile variants, values and discoverable routes under A5 |
> | Product | Actual demo identity, startup metadata, cold start, controls, failure/retry, applicable limitations |
> | Accessibility | Engine/width matrix, keyboard, AX controls, focus, targets, contrast, zoom/reflow, tool gaps |
> | Tracking | Mirror, histories/artifacts, anonymous routes and settled charts; no substituted local proof |
> | Release | Final build, guard/test results, exact-candidate independent check, authorized action record |
> | Public check | Per-surface identity and behaviour, first failures and retries, limitations; and the independent verdict when §10.5 requires it |
> | Follow-up | Violations versus recommendations versus rule proposals; comparison with earlier findings |
> | Final product (A8, conditional) | Owner designation; one product/demo/daily-policy identity; frozen update contract; daily fit/issuance lineage; ordered method/results/business/comparison sections; actual rollout status |
> | Daily panel (A7/A8, conditional) | Today issued-versus-published prices; percentage and MAE derivations including zero/negative/missing outcomes; tomorrow intervals; coverage/width; separate training/issuance timestamps and stale/failure states |
> | Business (A8, conditional) | Reproducible cumulative net value and benchmark when evaluated; explicit unevaluated state otherwise; costs, denominators, risk and simulation/realization labels |
> | Final-product Space (A9, conditional) | Every §7.3 view against its records; recomputation rows on the served bundle; served identity equal to the intended daily artifact; the retrain's measured status; the §9 matrix on views and controls; the listed negative controls |
>
> Preserve screenshots and necessary machine-readable evidence with the review's declared scope.
> Release evidence uses the normal committed evidence locations; task scratch stays in `.local/`.
> For an expressly local-only review, identify retained local evidence honestly and do not claim
> its machine-specific paths are publicly available. Do not overwrite a prior report to claim closure.

- Worktree clean before and after: yes. `git status --porcelain` was empty, and `HEAD` was `300926de…`, at the start,
  after the rebuild, after the payload build, after every test run and before this file was written.
- Reviewer:
  - I am the fifth Integration Critic of PRES-5 (the focused recheck at the final SHA). I authored none of PRES-5's
    changes.
  - I worked only in the clean detached worktree `/Users/djourno/Downloads/PJM/.local/worktrees/pres-5/critic-5` and made
    no Git write.
  - I did not open the Claude memory directory, `progress.md`, any syllabus, Track A/C material or
    `orchestrator-role.md`.
  - Outside the worktree I read four things: review 4's verdict (re-hashed); the issued brief's sections cited in my
    assignment; and two of the Lead's local upload logs, `mlflow-upload.log` and `mlflow-upload-2.log` under
    `.local/worktrees/pres-5/lead/.local/artifacts/pres-5/`. I read the logs only to confirm the refused first attempt
    and the run IDs written, with credential-bearing lines filtered out.
  - I printed no credential value and ran no network command. `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1` were
    exported for every Python run.
- Scope and limits:
  - My assignment's limit allowed seconds-long commands only. Ruling O39, relayed during the review, replaced it: the
    ceiling rose to 12 machine-hours, the rebuild, the release checks and the tests touching the changed files were
    allowed, and the cap stayed at 4 concurrent CPU workers with no fit, no new export or upload and no network.
  - I stayed within that: at most 4 concurrent workers, all checks local.
  - This verdict binds the final SHA. For everything outside the delta it relies on review 4's full-bar PASS. For the
    delta `48f56b0e..300926de` it rests on this recheck.

## Commands actually run

All commands ran in the critic worktree unless a path says otherwise. `uv run` used `--offline` (and `--frozen` from
command 18 on); the first `uv run` created the git-ignored `.venv/` in the worktree.

| # | Command | Exit | Observed output |
|---|---|---|---|
| 1 | `git -C …/critic-5 status --porcelain`; `git rev-parse HEAD`; `git log -1 --format='%H %cs %ci %s'` | 0 | empty; `300926de…`; `2026-11-13 2026-11-13 22:27:10 +0200 PRES-5: cp26 and cp28 uploaded, verified and indexed; the final build` |
| 2 | `git show 300926de…:docs/PUBLISH_RULES.md \| shasum -a 256`, then a Python extraction of `## 13.` to the next `## ` heading | 0 | `1bc0c523…f94e`; 28 lines, 2,964 bytes, `cb175c96…507e`; the printed text equals the brief's excerpt |
| 3 | `git merge-base --is-ancestor 48f56b0e… HEAD`; `git rev-list --count 48f56b0e..HEAD`; `git log --format='%H %P' -1` | 0 | ancestor; 1 commit; parent `48f56b0e…` |
| 4 | `git diff --stat` and `--name-status 48f56b0e… 300926de…` | 0 | 10 files, +2,957 −19: M `README.md`, `docs/index.html`, `docs/track-b/evidence/pres-5/publication-packet.md`, `reports/cp3/pages_build.json`, `reports/presentation/mlflow_index.json`, `src/delu_forecast/registry.py`; A `release-checks/pres-5-mlflow-precheck.json`, `pres-5-mlflow-upload.json`, `pres-5-public-mirror.json`, `pres-5-public-mlflow-routes.json` |
| 5 | `git diff 48f56b0e… 300926de… -- src/delu_forecast/registry.py README.md reports/cp3/pages_build.json docs/track-b/evidence/pres-5/publication-packet.md` | 0 | registry: one line, `"evidence/pres-5": ("", "2026-11-06")` → `("", "2026-11-13")`; README: one line, the date `frozen 2026-11-06` → `2026-11-13` in the evidence label; build record: `bytes` 1,848,408 → 1,848,925, `final` false → true, `links_omitted_until_verified` `["compare:v6"]` → `[]`, `mlflow_index_verified_at_utc` → `2026-11-13T20:03:28+00:00`, `compare:v6` added to `routes_published`; packet: four hunks, all O38 (§5d row, §5 A8 row, the new O38 row in §10.1, §10.3 item 1 "ruled (O38)") |
| 6 | `git show` of both pages to the scratchpad, then a Python line-by-line, character-level diff | 0 | 1,228 lines each; 2 lines differ. Line 492: `2026-11-06` → `2026-11-13` (the `evidence/pres-5` label). Line 539: the same date change and one inserted `<a class="ev external reader" href="https://dagshub.com/…/#/compare-runs?runs=[8 IDs]&amp;experiments=["1"]" data-route="compare:v6">Compare the runs in MLflow</a>` at the head of v6's evidence row. Nothing else |
| 7 | Python reads of `reports/presentation/mlflow_index.json` | 0 | experiment `delu-generations` (id 1); 11 routes; 105 runs (cp10 8, cp15 10, cp16 3, cp20 2, cp21 5, cp22 8, cp23 4, cp24 4, cp26 53, cp28 8); `not_advertised` `{}`; every route `rest: passed`, browser chromium and webkit `passed`; `verified_at_utc` 20:03:28Z, `browser_checked_at_utc` 20:24:08Z; written by `scripts/verify_mlflow_mirror.py index` |
| 8 | `uv run --offline python -B -` importing `delu_forecast.registry` from the worktree's `src`, comparing `expected_routes()` with the index | 0 | 11 expected route names = the index's 11; each route's kind and run keys equal the index's (the registry returns `(kind, keys)` tuples); `EVIDENCE_TAGS["evidence/pres-5"] = ("", "2026-11-13")` |
| 9 | Python: decode each compare URL's `runs=` list and compare with the index's run IDs for its keys | 0 | all 10 compare routes' IDs equal their keys' IDs in order, `experiments=["1"]`; `experiment` route `…/#/experiments/1`; 105 distinct run IDs; every run URL ends in its ID |
| 10 | Python reads of `pres-5-mlflow-upload.json` against `reports/presentation/mlflow-export/cp26.json`, `cp28.json` (unchanged in the delta, `git diff --quiet` exit 0) and both indexes | 0 | see checklist item 2 |
| 11 | Python read of `pres-5-mlflow-precheck.json` | 0 | one `GET …/api/2.0/mlflow/experiments/get?experiment_id=0`, HTTP 200, redirects not allowed, `network_writes: 0`, credential state `set`/`set` (no value), 2026-11-13T15:21:03Z |
| 12 | `shasum -a 256` and `stat` of review 4's verdict; reading its header and checklist | 0 | `fce6c28c…a197`; modified 2026-11-13T17:20:11+0200 (15:20:11Z), before the precheck (15:21:03Z) and the upload's start (15:21:28Z); "Verdict — PRES-5 — Integration — PASS" at `48f56b0e…`; its item 7 "PASS (prepared)", the upload left for this recheck |
| 13 | `grep -v -i -E 'password\|token\|authorization\|secret\|bearer'` over the Lead's `mlflow-upload.log` and `mlflow-upload-2.log`; a Python match of the second log's run IDs | 0 | first attempt: "mlflow-publish: REFUSED - the working tree differs from HEAD; commit or discard first" (no write); second: "published 105 runs to https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow: 61 created, 0 resumed, 44 already complete; 558 write operations", 30 min 46 s; its 61 run IDs = the record's 61 `created` IDs |
| 14 | Python reads of `pres-5-public-mirror.json` | 0 | `passed: true`, `problems: []`, counts expected 105, found 105, metric points 17,003 (= the sum of per-run `points_checked`; 16,753 on the 44 published runs + 250 on the 61 new); 11 routes, each `rest: passed`, `problems: []`, URL and keys equal to the index; run IDs equal to the index; checked 20:03:28Z = the index's `verified_at_utc` |
| 15 | Python reads of `pres-5-public-mlflow-routes.json` | 0 | `passed: true`; client "Playwright, a fresh browser context per route and engine; no cookies, no sign-in"; 11 routes × {chromium 157.0.8103.51, webkit 26.6} = 22 pairs, each `passed: true`, URL = the index's, `final_url` = URL, no missing text, console error, failed request, API error or sign-in redirect; `compare:v6` expects "Comparing 8 Runs", the eight run names and all eight IDs; the `experiment` route expects all ten parent names including "Daily development re-baseline (CP-26)" and "v6 · DDNN-2 alone (CP-28)"; the index's browser fields agree; checked 20:24:08Z = the index's `browser_checked_at_utc` |
| 16 | Python: `reports/cp3/pages_build.json` against the index and the page; `wc -c`, `shasum -a 256` of the page and README | 0 | `final: true`, `links_omitted_until_verified: []`, `routes_expected` = `routes_published` = the 11 index routes, `bytes` 1,848,925 = `wc -c`; each of the 11 routes appears once as a `data-route` link, with the index's exact URL once on the page; every compare link reads "Compare the runs in MLflow"; page `2fc5bd0a…e28b`, README `eb76fabf416c547f29600d2518ba2f0c207646b3cd785a095f9ab74be794cc8c` |
| 17 | `python3 scripts/publication_guard.py tree` | 0 | "publication-guard: the tree carries no placeholder and a final build record" (0.03 s) |
| 18 | `uv run --offline --frozen python scripts/lint_publication.py` | 0 | page 0, readme 0, templates 0 findings; "PASS — the reading path and the template sources meet the standard's §4 and §5 rules" |
| 19 | `uv run --offline --frozen pytest -q -p no:cacheprovider tests/test_50_pres5_publication.py` | 0 | 39 passed in 79.85 s |
| 20 | `uv run --offline --frozen python scripts/rebuild_presentation.py`, then `git status --porcelain`, `shasum -a 256 docs/index.html` | 0, 0 | README research block, README CP-3 section, MLflow export, static page, cross-surface agreement and zero-fetch checks all "ok", 20.0 s; status empty (only the ignored `.DS_Store`, `.venv/`, caches); page hash unchanged `2fc5bd0a…`. The rebuild reproduces the final build byte for byte |
| 21 | `uv run --offline --frozen pytest -q -p no:cacheprovider -rfEs tests/cp18a/test_dry_run.py::test_a_real_dry_run_then_the_fallback_finds_the_day_claimed tests/cp18a/test_forced.py::test_each_cause_is_forced_and_recorded` | 0 | 2 passed in 574.87 s (20:44:07Z–20:53:43Z). These are CP-18a's two push tests, which refused the candidate's non-final build record in review 4 |
| 22 | `uv run --offline --frozen pytest -q -p no:cacheprovider -rfEs` over the 15 files that read a changed file: `tests/cp18a/test_leak_scan.py`, `cp18a/test_red_line.py`, `cp18b/test_publish.py`, `cp18b/test_red_line.py`, `cp18b/test_space_build.py`, `cp24/test_base_tree.py`, `cp28/test_cp28_pipeline.py`, `cp28/test_cp28_results.py`, `test_17`, `test_19`, `test_20`, `test_21`, `test_22`, `test_23`, `test_24` | 1 | 456 passed, 3 failed, 12 errors in 67.55 s. All 15 non-passes are in `tests/test_22_wasm_equivalence.py`, each "app/public/ is absent. It is generated from the committed models/champion/ by make wasm-payload" or a `FileNotFoundError` under `app/public/`. The browser payload is git-ignored and uncommitted by design (the test fails rather than skips); the fresh worktree lacks it. Not a delta defect; resolved by command 23 |
| 23 | `uv run --offline --frozen python scripts/build_wasm_payload.py`; then `uv run --offline --frozen pytest -q -p no:cacheprovider -rfEs tests/test_22_wasm_equivalence.py tests/test_30_research_claims_rendered.py`; then `git status --porcelain` | 0, 0, 0 | payload 15,363,807 bytes across 14 files (fixture 54 days / 1,296 rows, 4 fail-closed), from the committed frozen champion, no fit; it rewrote `reports/cp3b/payload.json` byte-identically (status empty); 540 passed in 3.94 s |
| 24 | `uv run --offline --frozen pytest -q -p no:cacheprovider -rfEs` over the other 17 such files: `tests/test_30`, `31`, `32`, `33`, `34`, `35`, `37`, `38`, `39`, `40`, `41`, `42`, `43`, `44`, `45`, `48`, `49` | 0 | 948 passed, 1 skipped in 48.32 s; the skip is `test_30:348` "app/public/ is built by make wasm-payload", which ran and passed in command 23 |
| 25 | `PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright /Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py release docs/index.html --shots <scratchpad>/release-file --out <scratchpad>/release-file.json` (served over `file:`) | 0 | passed=True, 462.8 s; see checklist item 5 |
| 26 | `python3 -I -m http.server --bind 127.0.0.1 8817 --directory …/critic-5/docs`, then the same release check against `http://127.0.0.1:8817/index.html` (`--shots <scratchpad>/release-http --out <scratchpad>/release-http.json`), then the server stopped | 0 | passed=True, `served_over` "http(s)", 463.8 s (20:53:57Z–21:01:41Z). The server logged 36 requests, every one `GET /index.html` (33 × 200, 3 × 304): no other path. Placements identical to command 25 (headline 774.6/775.3 and 628.6/628.7 px; finding 1,667.6/1,668.3 and 2,394.5/2,394.3 px); no problem in any view; discovery 48 routes passed in each engine at both sizes; keyboard 162 stops, touch targets none under 44 px, contrast 0 below, AX trees passed, in both engines |
| 27 | `git -C …/critic-5 status --porcelain`; `git rev-parse HEAD`; `python3 scripts/publication_guard.py tree` (21:03Z, before the final edit of this file) | 0 | empty; `300926def8a841848ad02a74c25a5e0291b37f20`; "publication-guard: the tree carries no placeholder and a final build record" |
| 28 | `git show main:scripts/bar.py \| python3 -I - check <this file> --source docs/PUBLISH_RULES.md@300926def8a841848ad02a74c25a5e0291b37f20` (run on this file, and again after this row was added) | 0 | "ok: lines 17–44 (2963 bytes) appear in docs/PUBLISH_RULES.md@300926def8a8": the only quoted block is the bar excerpt, byte for byte |

Scratchpad: `/private/tmp/claude-501/-Users-djourno-Downloads-PJM/42e9ff0c-59d6-4c47-9c7c-d02f4609ac41/scratchpad`. The
release records and screenshots there are local-only, as are the Lead's `.local` logs. None is claimed to be publicly
available.

## Evidence actually inspected

- **Plan and governing records:** `docs/PUBLISH_RULES.md` §13 at the SHA. The issued brief's outcomes 7 and 9 and its
  "Owner-only actions already authorized", read in the worktree. Review 4's verdict (header, commands 13–30, items
  1–10, B1–B2).
- **The delta in full:**
  - the registry, README, build-record and packet hunks;
  - both pages, compared character by character;
  - the index's added `compare:v6` route and 61 runs.
- **The four release records**, read in full by structure: `pres-5-mlflow-precheck.json`, `pres-5-mlflow-upload.json`
  (write plan, 105 run rows, owner instruction), `pres-5-public-mirror.json` (105 runs, 11 routes) and
  `pres-5-public-mlflow-routes.json` (22 route-engine results).
- **The exports** `reports/presentation/mlflow-export/cp26.json` (53 runs) and `cp28.json` (8 runs), and the
  candidate's index (44 runs).
- **The packet's O38 places:** §5d, the §5 A8 row, the §10.1 O38 row and §10.3 item 1. I also grepped for "waive",
  "not applied" and every recorded page size.
- **My own results:** the release record from command 25 (per-view placements, discovery, keyboard, touch, contrast,
  zoom, AX trees), the rebuild's output, and the test logs.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | The delta holds only the listed files and nothing else | PASS | Commands 3–6: one commit; exactly the 10 listed paths. The index gains `compare:v6` and the 61 runs; the timestamps change. The build outputs are the page, README and build record. The four release records are new. `registry.py` changes one line (the `evidence/pres-5` date). The packet's four hunks are all O38. No other path |
| 1a | O38 stated as the ruling says, not as a waiver | PASS | The packet's §10.1 row reads "A8: not yet triggered; the product-first order is applied at 4.7T's publication; the final build goes ahead without another review", with its basis: A8's trigger is 4.7T's pass under decision 21, plus P1's red line and A8's ban on fabricated business evaluation. §5d, the §5 A8 row ("not yet triggered", "ruling O38") and §10.3 item 1 ("ruled (O38)") match it. No "waive"/"waiver" anywhere in the packet, and no remaining "not applied" or "proposed ruling" for A8 |
| 2 | The upload stayed inside its authority; complete or partial, with run IDs | PASS — **complete** | Commands 10–13. The record's `owner_instruction` restates the brief's authorization (When, What, How, Limits) and names "Independent check PASS at 48f56b0e…, 2026-11-13, Integration review 4". `export_commit` is `48f56b0e…`, and the exports are unchanged in the delta. The write plan's `authorized` = `to_write` = the 61 run keys of `cp26.json` (53) and `cp28.json` (8), exactly. `authorized_experiment_tags` = `experiment_tags_to_write` = `["mlflow.note.content"]`. `experiment_exists: true`, so no new experiment. The 105 rows: 61 `created` = the authorized keys; 44 `skipped (complete)` = the 44 runs in the write plan as `complete` = the candidate index's 44 runs, whose index entries are unchanged. The record contains no registered-model, deletion or other write: those words occur only inside the quoted limits. The first attempt was refused before any write. The upload ran 15:21:28–15:52:08Z, after review 4's PASS (15:20:11Z) and a read-only precheck. 558 write operations. The 61 run IDs are listed below |
| 3 | Verification and routes: mirror passed (105, 17,003, 0 problems, 11 routes by REST); browser record passed in both engines; index advertises every expected route (11) and withholds none | PASS (on records) | Commands 7–9 and 14–15. Mirror: `passed`, 105/105, 17,003 points (re-summed), `problems: []`, 11 routes `rest: passed` with 0 problems. Browser record: 22 of 22 route-engine pairs passed, anonymous, URLs equal to the index's. Index: 11 routes = `registry.expected_routes()` by name, kind and run keys; `not_advertised: {}`; each route's URL resolves to its keys' run IDs. The network checks themselves were not rerun |
| 4 | The build record is final; `publication_guard.py tree` passes | PASS | Commands 16, 17, 20 and 27. `final: true`; nothing omitted; expected = published = 11 routes; `bytes` = the file; `mlflow_index_verified_at_utc` = the index's. The guard exits 0 both times. A plain rebuild reproduces the build record and every surface byte for byte (`build_pages.py` writes `final` exactly when no route is omitted). CP-18a's two push tests, which the non-final record had stopped, now pass |
| 5 | The page's and README's changes are only the route link and the label's date; page ≤ 2,000,000 bytes; placements unchanged | PASS (measured independently) | Command 6: the page's only changes are the two `evidence/pres-5` dates and the one inserted `compare:v6` link. The link is in v6's chapter, after the finding in document order, outside any disclosure, and has the same text as the other nine compare links. README: the one date. Page 1,848,925 bytes (151,075 to spare). Command 25, Chrome and WebKit: headline bottom 774.6/775.3 px at 1440×900 and 628.6/628.7 px at 390×844; finding bottom 1,667.6/1,668.3 px (limit 1,744) and 2,394.5/2,394.3 px (limit 2,420), identical to review 4's candidate figures. Byline and release rule outside disclosures; header 56 px. No console error, failed request, HTTP error, resource after the document, collapsed space or overflow in any of the 11 views. A5 discovery: 48 routes passed in each engine at both sizes. Keyboard 162 stops (161 at the candidate, +1 for the new link), in order, none without visible focus. Touch targets at 390 px: 230 checked (229 + 1), none under 44 px. Contrast 0 below (4,894/4,887 text, 827/797 non-text checked). 200% zoom and 320 px reflow: 0 px overflow. AX trees passed in all four engine-size pairs. Lint 0 findings; `tests/test_50` 39 passed |
| 6 | The label's date equals the commit's date; the evidence tip the same day | PASS (the label); the tip is a later step | `git log -1 --format=%cs` = `2026-11-13` = `EVIDENCE_TAGS["evidence/pres-5"][1]` = the page's two labels = the README's label. The evidence tip is committed after this verdict, so it cannot be checked here; the Lead's return must show it is dated 2026-11-13 |

**§13 rows this recheck adds to review 4's record:**
- **Identity:** the final candidate `300926de…`, its tree state (clean), and the final page hash `2fc5bd0a…e28b`.
- **Tracking:** the mirror, the anonymous routes and the index, from records made against the public host, not a
  local substitute.
- **Release:** the final build (reproduced), the guard and the tests above, this exact-candidate check, and the
  authorized action's record (item 2).
- **Final product (A8):** "not yet triggered" under O38, stated as the ruling.

The other rows stand as review 4 recorded them for everything outside the delta.

### Run IDs written by the upload (61, all `created`; 0 resumed; the 44 published runs untouched)

`cp26` 057c6013d46549d98c2b77e5be7ab66a · `cp28` 281d3c5c25204a629c056044bdee8b25

CP-28 arms: A1 369c58dae974477b9806baa394e125b6 · A2 b19ab6fb6cc842f3ae11ad53937a1d80 ·
A3 4f4aca1f18bf4af6adcda3262ca1d2e0 · A4 80615e0623c64520992478a04d916231 · A5 65e1793bf4884cd7a4a32691da229e37 ·
A6 c3e74d6b25a4468cbea9b0c4262f65dc · A7 52bc534a5ce2466386556e7e7f340e59

CP-26 children (route/policy/population):

| Route/policy | all_eligible | never_scored | old_fold_2_5 | newly_opened |
|---|---|---|---|---|
| gfs6/v3 | b3906117111047f29a0cc181108c02cd | 8f01d19c962d416195ead4237522448d | e323719f992c490eb8a811bc6760354f | e5b7d8753bd949bb8028a4b80b02d311 |
| gfs6/v4 | f32c1f995aa744e2a21b33a6e218cbf9 | cb3cdcf9e2a740c19cf730e841060f54 | 03eac674ad4e4cab973467b6c5d2202f | ccb005b4c25747f4ae4477a828725c54 |
| gfs6/v5 | 9ae39cbe1dd34b968d30084ed5e2c932 | 4124d2ee4d534eba92497d27be92bafe | 9d542818e1df42d39063ad7c619df8a0 | 31a3c3b43ade48ef9cab8ae1a02f4cd1 |
| noload/v3 | ed0fbe8de7d94ac1875f1f8074ac5b7e | 9f9e12fe2d29403b80a4d255fd8a218f | 7e781d19c9254079890c89824601716b | a41afd1abaf44e039f0a7432cc90e383 |
| noload/v4 | bc998e79731b476b9d82afe60bd4af22 | 1d2a012b97db4a0d9580ef3f52751ddd | 326f907c394444f4a283d94494dd2a87 | 1e600c4e75094df0b1ac0c33ce8b1e99 |
| noload/v5 | d55878f233664feaaa5653c1a45e5e49 | 2e1024c61ee045ed891df67c7ddce0b0 | 2f085ad028a74a53ab0a3e9d6b0764cc | ad1ae1fb992f4d2192caf1a0fe4b3bd7 |
| nominal/B0 | 56d1426a9a6c412aba6791e352d9e75b | 2f667e7ee4c341768ee6f9bfdbd2c4a8 | e57dbc651cde4260b5e0134d8ee9ac87 | 9de5ff0eee4b419a8ae7a8d180e13579 |
| nominal/D2 | 33bcc3b53ab542129274355492bed5be | 20feadfd2ced4ff6926f334227101462 | e96bcb55abbc426da6d57b0193ed8fa4 | c7a7b666a95c456a9cb2511ebf2739b8 |
| nominal/v1-R | 176ae4e43792406c9341efb9586caffa | 169b7ac3d12744508699f1550364c5ca | cc239fc35d1043b799f458ce94470c0a | cdeb79bbe87746b0bb6c472169802b20 |
| nominal/v2 | 8b1776b0015c46f492e3fefeab61c0d4 | 34dc477789154e529c20f5d79ae3dc60 | 8d5b79e7a45f43048fee4cb21df34cf2 | 870123a5aa134a43877262bc924c2c94 |
| nominal/v3 | 3a9eeb36b0fc4da0b3493d7643462edf | 838c0ab8d55544759f1ec7df1a2dc56e | e4901bf4d94847baaf7cf49fb0b242c6 | c466c24286a249f29eb24be862d98e4e |
| nominal/v4 | 0078836f0c2d4f2d95c14ebdea2b7c64 | 8ff57e81fa3448a49a1accfa5f4b2673 | 41f390d93b964ffdae72431768914041 | 304328da343c4876b699a95d57a04ea5 |
| nominal/v5 | 257d7decf5664da78e0da878f5a8f6be | f0e96c58f32a4235a6b7aaf6338cc491 | debfdebb72824294a191f807ab91fd15 | f419b0e833f74582b9ba461fd14acbd5 |

### Checks not rerun here (relied on records)

- **The MLflow upload, the REST mirror verification and the anonymous browser route checks against DagsHub.** I
  ran no network command, so these rest on their committed records (commands 10–15), the Lead's upload log
  (command 13) and their mutual consistency.
- **The full suite, the prerelease, the Python 3.12 CI run, `make verify` and the link check.** These were not run.
  The full suite and the prerelease were run at the candidate (review 4; packet §7). Here I reran every test file
  that reads a changed file (32 files plus `tests/test_50`), CP-18a's two push tests, the rebuild, lint, the guard
  and the local release checks.
- **The public surfaces.** They are not deployed yet; they are the Orchestrator's steps after the return.

### Recommendations (not violations)

- **R1. Stale page size in the packet.** Packet lines 249, 516 and 590 still give the candidate's page size,
  "1,848,408 bytes", "151,592 to spare". They cite `reports/cp3/pages_build.json`, which records 1,848,925 at this
  SHA (151,075 to spare). The budget holds either way, and the packet's identity table (line 274) leaves the final
  page's identity to the return and this verdict. The return should label those figures as the candidate's or carry
  the final ones.
- **R2. Precheck target.** The upload precheck reads `experiment_id=0`, while the target experiment is `1`. The write
  plan's `experiment_exists: true` and the mirror's experiment 1 confirm the target, so nothing was wrong. A future
  precheck could read the target experiment itself.

## On FAIL only

Not applicable (PASS).
