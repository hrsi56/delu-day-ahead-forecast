# Verdict — PRES-1 — Independent check — FAIL

- Candidate SHA: 9ae76f468cc9c3f6c6654261460fe5453186d1f8
- Plan / version / bar: `docs/track-b/presentation-and-tracking-plan-2026-09-24.md`, revision 3 (SHA-256 `281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`, confirmed), §12 "Phases, order and acceptance", Acceptance column for phases 0, A, B, C, D1 and D2; with the §6 invariants and the §9.5 test table (brief §8). Brief / section: `docs/track-b/pres-1-brief-2026-09-24.md` (SHA-256 `7cb672f2ffa960908723e55e114442be4f8286e718892935acad3e6e0965ebb4`, confirmed), §9 "Independent check", "What its assignment covers".
- Verbatim bar excerpt:
  > **0: Demo diagnosis** … Diagnosis recorded. The demo states (§7.11) go ahead in any case.
  > **A: Content** … Every statement has a claim ID and a file/row source. No withheld phrasing. No v2+ content after 2026-04-07.
  > **B: Evidence layer** … Tests green, negative controls included. No typed research number in any generator.
  > **C: MLflow preparation, local only** … The rehearsal's verifier passes. An interrupted upload resumes without duplicates. The deliberate faults are caught. No public write.
  > **D1: Visual specimen** … **Ready to extend when:** the Owner approves both the desktop and the phone composition; the hierarchy of result, limitation and evidence is clear; no scientific meaning depends on colour or hover; real content fits; and the reader tasks show no confusion between research progress and the released product.
  > **D2: Full page and surfaces** … Tests 17–34 green. `make verify`. No fetches. The size budget holds. The §11.3 report checks pass locally.

  > - **The data:** every rendered research number is re-derived from its source record.
  > - **The claims:** the claim maps; the withheld phrases; the labels; the exact H−P endpoint; v1's label.
  > - **The charts:** units, direction and intervals; scales; mobile variants; the meaning survives without colour or hover.
  > - **The links:** internal anchors, the repaired link checker and the MLflow routes.
  > - **The reading experience:** the six reader tasks in plan §11.4.

  (The excerpt is the citation. Each line above was confirmed with `grep -F` in its file at the candidate SHA; the brief's nested bullets are joined here for length and appear verbatim, one per line, at brief lines 219–232. Plan §12 is at line 1341; any line number is a courtesy and is non-binding.)
- Worktree clean before and after: yes. `git status --porcelain` empty and `HEAD` = `9ae76f468cc9c3f6c6654261460fe5453186d1f8` at the start and after the last command. `reports/cp3/link_check.json`, rewritten by the link checker, was restored with `git checkout --`. Gitignored byproducts only: `.venv/`, `app/public/`, `dist/space-wasm/`. The worktree `.local/worktrees/pres-1/check-1` is left in place for the Lead, whose lifecycle owns it (the brief made this check read-only).

Approximate elapsed: 0.5 h (wall clock 23:08–23:40 IDT, 2026-09-27). No write to any public or network destination. Credential values were never displayed. Files not read: `progress.md`, `orchestrator-role.md`, the syllabus, and the uncommitted Owner D1 review in the Lead's checkout.

## Commands actually run

Everything ran in `<repo>/.local/worktrees/pres-1/check-1` unless stated otherwise. Outputs are under `<repo>/.local/tmp/pres-1/check-1-out/` (called `OUT` below).

| # | Command | Exit | Observed output |
|---|---|---|---|
| 1 | `git -C <wt> status --porcelain`; `git -C <wt> rev-parse HEAD` | 0 | empty; `9ae76f468cc9c3f6c6654261460fe5453186d1f8` |
| 2 | `shasum -a 256 <plan> <brief>` | 0 | `281193740a25…812c` and `7cb672f2ffa9…ebb4`: both match the assignment |
| 3 | `uv sync --frozen` | 0 | "Using CPython 3.13.15 · Creating virtual environment at: .venv"; about 1.6 s |
| 4 | `uv run --frozen python scripts/build_wasm_payload.py` | 0 | "payload: 15,363,807 bytes across 14 files … wrote reports/cp3b/payload.json". Tree unchanged. |
| 5 | `uv run --frozen pytest -q` | 0 | `733 passed, 7 skipped in 137.52s` |
| 6 | `uv run --frozen python scripts/verify_release.py` (the `make verify` target) | 0 | Item 5 cross-surface table all "yes", "disagreements: none"; "scanned docs/index.html (1,520,336 bytes) · fetching references to an external origin: 0"; "gated DagsHub UI links on any surface: none"; final line "PASS — every bound claim agrees on every surface; the static page fetches nothing" |
| 7 | `uv run --frozen python scripts/rebuild_presentation.py`, then `git status --porcelain` | 0 | README research block, CP-3 section, MLflow export, static page and checks all "ok"; "rebuilt every presentation surface in 10.6 s". `git status` empty. |
| 8 | `uv run --frozen python scripts/mlflow_export.py --check` | 0 | `the committed export is current` |
| 9 | `uv run --frozen python scripts/mlflow_publish.py --dry-run` | 0 | `dry run: 23 runs, 6928 metric points, 55 artifacts; outbound scan clean; export current at 9ae76f468cc9`. Separately, inside a process: `secret_guard.credentials()` loaded 5 non-empty values for the scan. Only the count and names were printed. |
| 10 | `uv run --frozen python scripts/check_links.py`; then `git checkout -- reports/cp3/link_check.json` | 0 | 18 destinations, all `200`, including `…mlflow/#/experiments/0`, `…mlflow/#/models`, the GitHub blobs at `evidence/cp-15`, `evidence/cp-16` and `evidence/cp-20`, both Integration verdicts on `main`, Pages, `…/#journey`, the Space and the static app. Gated paths: four `302 -> /user/login`. "failed destinations: none". Record restored; copy at `OUT/link_check.rerun.json`. |
| 11 | `check_links.main()` on a scratch surface holding Pages plus a real missing page `…/no-such-page-check-1.html` plus `http://127.0.0.1:8820` (live probe, no mock) | 1 | `404` recorded as `HTTPError 404: Not Found` in `failed_destinations`; `127.0.0.1:8820` classified `local` and not fetched; `exit: 1` |
| 12 | `PLAYWRIGHT_BROWSERS_PATH=… …/playwright/bin/python scripts/check_reader_paths.py screens docs/index.html --width 1440 --width 390 --out OUT/screens --record OUT/screens.json` | 0 | `index @ 1440: overflow=False smallest chart text=12 px (v1-replay)`; `index @ 390: overflow=False …12 px` |
| 13 | the same with `--open-all` (`OUT/screens-open`) | 0 | the same two lines; scrollWidth = clientWidth at both widths |
| 14 | `… check_reader_paths.py charts docs/index.html --out OUT/charts --record OUT/charts.json` | 0 | "no overlap, clipping, text under 12 px or horizontal overflow". 66 chart captures at 1440, 390, 360 and 320 px, closed and open: 0 overlaps, 0 clipped, smallest text 12 px (v1 replay), overflow 0 px at every width |
| 15 | `… check_reader_paths.py route docs/index.html --out OUT/route --record OUT/route.json` | 0 | At 390, 360 and 320: "Explore this forecast" opens the archive at `#forecast`; the replay draws at its width with 12 px text; 95% shows `0.9398`; the ×1.02 scenario caveat is shown; the archive's Results link stays in v1 |
| 16 | `… check_reader_paths.py a11y docs/index.html --engine chrome --engine webkit --record OUT/a11y.json` | 0 | Chrome 153.0.8010.54 and WebKit 26.6 both: contrast 0 of 2,171 (1440) and 0 of 2,162 (390) text elements below threshold; touch targets 0 of 85 under 44 px; keyboard: first stop "Skip to the content", 40 stops in document order, none without visible focus, Enter toggles summaries, an anchor into a closed disclosure opens it; 200% zoom (1440 and 1280) and 320 px reflow: 0 px overflow, closed and open |
| 17 | My own viewport capture (`OUT/work/viewports.py`, Chrome, fresh context) at 1440×900 and 390×844, disclosures closed | 0 | 12 and 19 screens, in `OUT/viewports/`, plus landmark positions (`viewports.json`) |
| 18 | `uv run --frozen python scripts/build_wasm_space.py`; `git status`; `git diff --stat` | 0 | "assembled dist/space-wasm: 738 files, 42,164,586 bytes"; `space-wasm/README.md` and `reports/cp3b/space_wasm_bundle.json` rewritten byte-identically (no diff); `sha256(dist/space-wasm/index.html)` = `93cfd632…d6a5` = the committed `index_html_sha256`; `startup_findings()` = `[]` |
| 19 | `python3 -m http.server 8791 --bind 127.0.0.1` over `dist/space-wasm`, then `… check_reader_paths.py states --engine chrome --url http://127.0.0.1:8791/ --out OUT/states.json`; server stopped | 0 | A blocked app script gives state `failure`, with visible "The demo did not start … Retry" and a report link to `https://hrsi56.github.io/delu-day-ahead-forecast/`. A runtime-reported failure gives `failure`. A hang goes from `loading` to `failure` after the deadline. Retry reaches `ready`. |
| 20 | `uv run --frozen pytest -q -rs tests/test_17…test_34` (after the Space build) | 0 | `382 passed in 28.32s`, 0 skipped |
| 21 | `uv run --frozen python scripts/build_pages.py --final` | 1 | `final build refused: unpublished destinations remain: ['mlflow:cp16', 'mlflow:cp20', 'mlflow:experiment', 'mlflow:overview']`. Nothing written. |
| 22 | `uv run --frozen python scripts/build_pages.py --specimen OUT/specimen` | 0 | writes `index.html`, `stress-7.html`, `token-sheet.html` and `demo-states.html` outside the worktree |
| 23 | A fresh loopback MLflow 3.5.1 server (`.local/tools/mlflow-3.5.1`, SQLite store and artifacts under `OUT/rehearsal`, port 5051, MLflow credential variables unset for the process), then `env -u MLFLOW_TRACKING_USERNAME -u MLFLOW_TRACKING_PASSWORD uv run --frozen python scripts/verify_mlflow_mirror.py rehearse --store … --artifacts … --out OUT/rehearsal/rehearsal-record.json`; server stopped | 0 | Interrupted upload exits 3 ("deliberate interruption after 115 write operations"). Verification then fails with 34 problems, as expected. The resumed upload exits 0 ("23 runs … 13 created, 2 resumed, 8 already complete; 595 write operations"). Verification: 23 of 23 found, 6,928 points, passed. The idempotent re-run passes. Deliberate faults: "cp20/HG: metric fold_mae_eur history differs (1 missing…)" and "cp20/HG: artifact summary.json digest differs", both caught; `passed=True`. SQLite: 23 `delu.run_key` values, at most 1 run each, 23 runs, 4 parents `package_complete=true`. |
| 24 | Read-only anonymous REST: `experiments/get?experiment_id=0`, `registered-models/get?name=delu-day-ahead-champion`, `experiments/get-by-name?experiment_name=delu-generations`, `/version` | 0 | `delu-cp2 active`; `[('champion','1')]`; `{"error_code":"RESOURCE_DOES_NOT_EXIST"}`; `3.5.1` |
| 25 | Playwright (Chrome, fresh context) opens `…mlflow/#/experiments/0` and `…mlflow/#/models` | 0 | Both render anonymously ("delu-cp2" and "delu-day-ahead-champion" in the page text), with no sign-in prompt |
| 26 | `curl` of the raw `uncertainty.csv` at `evidence/cp-20` (GitHub), line 12, piped to `git hash-object`; the same for `v2-causal/uncertainty.csv` at `evidence/cp-16`, line 32 | 0 | L12 = `equal_fold,HG,H0,MAE,-0.07831150099532369,-0.10059575155295458,-0.05703087928591252,…`; public blob `aa3028f1…0207` = the registered blob. L32 = `equal_fold,V2-H,V2-P,MAE,-0.0016954464559965077,-0.003623724975937509,3.857628092332211e-06,…` |
| 27 | For all 32 `research.SOURCES`: `git rev-parse <tag>:<path>` against `HEAD:<path>` and the recorded blob | 0 | 32 OK, 0 mismatches |
| 28 | `OUT/work/verify_values.py`: every `data-record` on the page (HTML `<data>` and SVG `<text>`), its cell read from `git show <evidence tag>:<path>`, compared with the `value` attribute and the displayed rounding (and CI endpoints) | 0 | 665 bound values; 664 match. The one flagged is `cp2…relative_improvement_pct` = −28.580190296810432, shown as "28.58% worse". It is correct: the sign is carried by the word. |
| 29 | `OUT/work/verify_geometry.py`: every bound SVG mark's x-position read through its axis's labelled ticks, against the source value | 0 | 14 chart variants (overview, v2 charts 1 and 2, C2a, C2b, C4, C6; each desktop and phone): 0 marks off-scale |
| 30 | A zero-line check on every "no difference" chart | 0 | The reference line sits on the 0 tick in C2a, C2b and v2 chart 2, desktop and phone |
| 31 | `research.validate_all()`; a date scan of the 394 records the page uses | 0 | `[]`; none has `window.last` after 2026-04-07 (8 have no window: counts and settings) |
| 32 | `withheld_findings` and `stale_findings` on the page text, `README.md`, both Space cards and `app/public/claims.json`; my own regex and grep for W10, W12, W13 and W16, "peer", "significan", "equivalen", "guarantee" and "confirmatory" | 0 | README, cards, claims.json: none. Page: one pattern hit ("coverage guarantee"), inside the preserved v1 archive's CQR text (protected by invariant 24; not a v2+ claim). Every "confirmatory" is "confirmatory-style, not power-qualified" or "never confirmatory". |
| 33 | A scan of the generators (`build_pages.py`, `readme_research.py`, `mlflow_export.py`, `research_claims.py`, `cp3_readme.py`, the publish and verify scripts) for the 387 distinct rendered research numbers | 0 | `mlflow_export.py:75` "79/408 to 131/408"; `:92` "10,747 development hours"; `:223` "448 represented development days"; `build_pages.py:2609` "−0.0783 headline value" (D1 token sheet). The other hits are CSS or section numbers. |
| 34 | Final `git status --porcelain`; `git rev-parse HEAD` | 0 | empty; `9ae76f468cc9c3f6c6654261460fe5453186d1f8` |

Output hashes (`.local/tmp/pres-1/check-1-out/`):

```
016b6129f23f0b30ffda73db4c581f3cda1f703b155b20bbbeb38f3a92a0213f  charts.json
9447d5995c6c5684457cde3560937f80eb91b1c0989f097311ab7215ae214928  a11y.json
29ac5f27133ac816b90c5501efacb9edd1e1443dc27fa3079674f39d833abe2a  route.json
53e6d38d5a82d6d8fde9d44d438919076ecd54bcc21adc8e4801d3a36cdb9a94  states.json
05fe8a4d64ebe59c3129ce5b16abde803ece883d0aca4eab01811741729b8592  rehearsal/rehearsal-record.json
eaaae3ffa87f516da195d33b733103bc38a0935bf0476334ba6000ed66f46834  viewports/viewports.json
b56aafda727e4d759b8dd6d7d7e43fdddcc0fc5973223cc56545afd449784d54  link_check.rerun.json
9b85c28296c5289e2fd21b1cef50c756f727b9dfd401a68d3856374151a636cc  pytest.log
```

## Evidence actually inspected

**Governance and bar documents.** `AGENTS.md`; `engineering-role.md` (Integration Critic protocol); the plan in full; the brief in full.

**Phase records.**
- `reports/presentation/release-checks/2026-09-24-demo.json`: the diagnosis (P0-1, blank static HTML), the fix plan, runs on Chrome, WebKit and the built-in Chromium, and the Owner's device test (outcome "passed", device and browser not supplied).
- `…/2026-09-25-demo-local.json`, `…/2026-09-25-space-states-local.json`, `…/2026-09-25-rebuild.json` (9.6 s) and `…/2026-09-27.json` (the §11.3 record, including `not_checked_here`).
- `reports/presentation/d1/specimen.md` (including "The Owner's Stop 1 decisions") and `layout-measurements.json`.
- `docs/track-b/evidence/pres-1/reader-tasks-d1.md`.
- `reports/presentation/mlflow-capabilities.json`: the public read-only probe of 2026-09-24 and the rehearsal of 2026-09-27, `passed: true`.
- `reports/presentation/mlflow-export/manifest.json`: the counts `{parents 4, children 19, total 23}` and the run keys, which match plan §10.3 exactly. `cp15/B1` carries `delu.v1_record_run=83e475627b6646c885c70f9010c8cf2e`; the provenance tags are separate (`model_code_sha`, `evidence_ref`, `source_blobs`); every metric name carries its unit.
- `reports/cp3/pages_build.json`: 1,520,336 bytes, `final: false`, 4 unpublished markers.
- `reports/cp3b/space_wasm_bundle.json`: `startup_states.injected: true`.
- `reports/cp3/mlflow_registration.json`: `tags_applied` unchanged, with no edited claim among them.

**Content and code.**
- `cp20-claims.md`, `cp15-cp16-claims.md` and the head of `cp20-update.md`.
- `src/delu_forecast/research.py` (SOURCES, records, rederive), `research_claims.py` (the withheld and stale guards) and the `claims.py` diff: only the §8.7 reconciliation, `delu-generations` and GFS licensing.
- `scripts/check_links.py`, `mlflow_publish.py` (dry-run path, preconditions, scan), `verify_mlflow_mirror.py` (rehearse), `build_wasm_space.py` (state injection), `build_pages.py` (main, `--final`, specimen), `rebuild_presentation.py`.
- Tests 23 (extension), 29–34 (every test name; the negative controls cover wrong row, policy, aggregation, unit and revision, a mixed-unit axis, a post-boundary window, a missing claim, an undeclared numeral, a table outside `.scroll`, a duplicate id, an unlabelled series, missing or duplicated or reversed README markers, a mocked 404 and an unreachable URL, and a fake credential).
- The diff `e8025cc..HEAD`: no locked file, `pyproject.toml`, `uv.lock`, `models/`, `data/` or `DATA-LICENSE.md` touched.

**Numbers recomputed by hand** from the committed files at their evidence tags (`git show evidence/cp-20:…`, `evidence/cp-16:…`, `evidence/cp-15:…`, `evidence/cp-2:…`), each with its displayed rounding.

*Opening and overview comparison.* Source: `weather-ablation/metrics.csv` L44–50 (equal-fold) and pooled rows L2, L8, L14, L20, L26, L32, L38. Plan §8.2's table has the same values.

| Policy | S_MAE (source → shown) | S_WIS (source → shown) | Pooled MAE, EUR/MWh | Pooled WIS, EUR/MWh |
|---|---|---|---|---|
| HG | 0.5657606 → **0.5658** | 0.5322187 → **0.5322** | 18.25889 → 18.26 | 10.66591 → 10.67 |
| H0 | 0.6440721 → 0.6441 | 0.6160300 → 0.6160 | 20.23 | 12.05 |
| B2 | 0.6578109 → 0.6578 | 0.6389910 → 0.6390 | 20.98 | 12.66 |
| A1 | 0.6722908 → 0.6723 | 0.6460151 → 0.6460 | 20.71 | 12.45 |
| B3 | 0.7841364 → 0.7841 | 0.7399052 → 0.7399 | 26.32 | 15.17 |
| B1 | 1.0518451 → **1.0518** | 0.9856367 → **0.9856** | 41.74348 → 41.74 | 25.25 |
| B0 | 1.0000 | 1.0000 | 32.81010 → 32.81 | 20.02 |

- Limits (`criteria.csv` L2–3): 0.5920298 → 0.59203; 0.5750919 → 0.57509.

*F07 note.*
- `cp2/dm_development.json` point test: statistic 1.6228252 → +1.6228; p 0.94769 → 0.948; `relative_improvement_pct` −28.580190 → "28.58% worse"; `n_days` 448.
- `development_pooled_metrics.csv` L8 (naive 32.452299 → 32.45) and L4 (41.743482 → 41.74).

*v3 chapter.* Source: `weather-ablation/uncertainty.csv`.
- C2a, ΔS_MAE (L12): −0.0783115 → **−0.0783**, 95% CI [−0.1005958, −0.0570309] → **[−0.1006, −0.0570]**.
- C2a, ΔS_WIS (L13): −0.0838113 → −0.0838, [−0.1043827, −0.0655398] → [−0.1044, −0.0655].
- C2b, all 10 rows (L2–11) with their intervals. Fold 3 MAE (L6): −3.1782372 [−6.0898293, +0.0368770] → **−3.18 [−6.09, +0.037]**. Fold 5 WIS (L11): −1.9804 [−2.4352, −1.2768] → −1.98 [−2.44, −1.28].
- C3, all 30 values (`metrics.csv` L9–13, L33–37, L39–43), for example fold 3 MAE: v1 140.99285 → 140.99, v2 51.21362 → 51.21, v3 48.03539 → 48.04.
- C4:
  - v1 275.25954 → 275.26 with 79 hits (`cp15/peak.csv` L8);
  - A1 49.87670 → 49.88 with 378 hits (L2);
  - v2 52.50980 → 52.51 (`criteria.csv` L10), 377 hits (`diagnostics.csv` L837);
  - v3 47.52144 → 47.52 (L31), 383 hits (L977);
  - the coverage cross-check: 0.9240196 × 408 = 377 and 0.9387255 × 408 = 383.
- C5 (`diagnostics.csv` L768 and L908), fold 3, hour 12: v2 67.30804 → 67.31, v3 61.02706 → 61.03.
- C6 (pooled rows): coverage 0.3645, 0.4993, 0.4937, 0.6281, 0.7906, 0.7914, 0.8452, 0.9389, 0.9377; width 41.53, 29.46, 27.14, 75.47, 65.78, 58.81, 130.86, 124.64, 106.24.
- "Narrower in every period": HG's width is below H0's at 50%, 80% and 95% in all five folds.
- "Slightly lower coverage": HG's 95% coverage is below H0's in folds 2–5.
- Cost: 2,476 runs and 123,800 messages (`report.md` L150); 136.0 GiB, 40.09 h and $0 (`resource-final.json`).

*v2 chapter.* Source: `v2-causal/uncertainty.csv` L32–37.
- H−P ΔS_MAE −0.0016954 [−0.0036237, 3.857628092332211e-06] → **−0.0017 [−0.0036, +0.000003857628092332211]**. The endpoint is printed in full, never rounded, in the chart note, the interpretation, the values table and the README.
- H−P ΔS_WIS: −0.0127 [−0.0156, −0.0109].
- H−B2: −0.0137 [−0.0236, −0.0053] and −0.0230 [−0.0337, −0.0118].
- P−B2: −0.0120 [−0.0213, −0.0036] and −0.0103 [−0.0201, +0.00067] (0.000670395).
- V2-P (`metrics.csv` L50): 0.6457676 → 0.6458 and 0.6287218 → 0.6287.
- CP-10 (`cp10/peak_windows.csv` L2 and L4): 0.1936275 → 19.36% and 0.3210784 → 32.11%.

*v1 chapter.* `cp15/peak.csv` L8: bias −269.44881 → −269.45; level MAE 269.45; shape MAE 66.87932 → 66.88. The holdout values come from `claims.py`, bound by `verify_release`.

*Records outside the evidence layer.*
- 20.4 s: `2026-09-24-demo.json`, Chrome 153.0.8010.53 at 1440.
- 9.6 s: `2026-09-25-rebuild.json`.
- Both are marked `data-release-check`.

**Rendered page.**
- Visible text in reading order (`OUT/work/page.txt`).
- 31 viewport screenshots and chart captures at 1440 and 390 (C2a, C2b, C3, C4, C5, C6, v2 charts, overview; desktop and phone).
- The token contrasts, recomputed from hex: text 17.72, text-2 7.73, accent 6.70, v1 7.58, v2 7.10, v3 5.47 and ref 4.83 against white; generation pairs 1.07, 1.38 and 1.30.
- The preview's 80% band (`#475569` at 0.18 opacity) renders at about `#DEE0E4`: **1.32:1** against the panel.

## Reader tasks (plan §11.4)

Read as a first-time visitor, every disclosure closed, in Chrome at 1,440 × 900 (12 screens, 10,228 px) and 390 × 844 (19 screens, 15,655 px). Screen *n* covers pixels [(n−1)·height, n·height). I cannot measure seconds, so the screen count stands in for time.

| # | Task | My answer | First appeared, 1440 × 900 | First appeared, 390 × 844 |
|---|---|---|---|---|
| 1 | Find the product | An hourly day-ahead price forecast for DE-LU with prediction intervals. The released v1 runs in the browser through "Try the v1 demo ↗" (the Hugging Face Space, about 57 MB). The page shows a labelled "Historical forecast · v1" replay. | Screen 1: primary action, "Demo v1 · Released model", preview | Screen 1: action and status card; preview on screen 2 (875 px) |
| 2 | Released and research versions | Released: **v1** (LightGBM, the model the demo runs). Research: **v3 · weather features**, "Development · post-selection", "Adopted in research · not in the demo". | Screen 1 (status pair) | Screen 1 |
| 3 | Explain the main improvement | v3 keeps v2's model and adds day-ahead weather forecasts (wind at 10 m and 100 m, solar radiation) as inputs. On the same 10,747 historical hours, both the point error and the interval score fell relative to v2. The normalized differences are about −0.08 each, and both 95% intervals lie below zero. This is development evidence on known periods, not a test on new data, and the crisis fold is less certain. | Screen 2 (qualitative "Latest research", 1,063 px); quantified on screen 5 (C2a) | Screen 2 (1,495 px); C2a on screen 8, finding on screen 9 |
| 4 | Find a rejected idea | Recalibrating v1's intervals without refitting (CP-10): "Not adopted · recalibrating v1 was not enough". Its numbers (19.36% → 32.11% crisis coverage) sit in the closed "The two branches before v2" disclosure; the v2 "Problem" text restates it on screen 7. | Screen 2 (lineage branch card) | Screen 3 |
| 5 | Name a remaining uncertainty | "Performance on future data is still to be evaluated". Also: fold 3's MAE interval crosses zero, and the gain cannot be attributed to a single weather feature. | Screen 2; details on screens 5–6 | Screen 2 |
| 6 | Open the evidence for one claim | v3's evidence row, "View source values", leads to `reports/weather-ablation/uncertainty.csv#L12` at `evidence/cp-20`. I opened it: line 12 is the equal-fold HG−H0 MAE row, −0.07831… [−0.10060…, −0.05703…], and its public blob equals the registered blob. "Read the review" leads to the CP-20 Integration verdict (HTTP 200). | Screen 4 (overview evidence row); v3's row on screen 5 | Screen 6 (overview row); v3's row on screen 9 |

**Points of confusion.**
1. "The plan's diagnostic limits" in the overview: a public reader does not know which plan.
2. Vocabulary in the overview: "seven evaluated policies", "post-selection", S_MAE and LEAR. LEAR is first defined only in the v2 chapter.
3. The released v1 sits at 1.0518, worse than the naive, in the overview. The one-line note and the closed "Definitions" disclosure reconcile it, but a newcomer may briefly doubt the product.
4. "Compare experiment runs (link added when the runs are published)" appears four times and reads as unfinished. This is expected until F4.
5. The desktop rail keeps "v1" highlighted while the reader is in "How the system works", "Contribution" and "Terms".
6. In the README (not the page), the research block says "The exact values and intervals are shown in the chart", but the README has no chart.

**Research progress against the released product: no confusion.** "Released model", "Adopted in research · not in the demo" and "The demo continues to run v1" are explicit. The lineage line ends at v3, but the label beside it rules out reading v3 as the product.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | **Phase 0**: diagnosis recorded; the demo states go ahead in any case | PASS | `2026-09-24-demo.json` holds the diagnosis (P0-1), the fix plan and the Owner's device-test outcome (device and browser not supplied, as recorded). The states are built (`build_wasm_space.py`); my rebuild reproduces the committed card and bundle record byte-identically, `index_html_sha256` matches and `startup_findings` is empty. I forced failure, hang and retry on a loopback server, and each showed the static state with a route back to the report (rows 18–19). Extended `test_23` passes, 25 tests. |
| 2 | **Phase A**: every statement has a claim ID and a file/row source; no withheld phrasing; no v2+ content after 2026-04-07 | PASS | All 23 `data-claim` IDs on the page exist in the two maps. A sample of row citations resolves to the stated rows (C69/C70 → U20 L12–13; C73 → L6; C74 → M20 L44–50; C79 → PK15 L2 and L8, C20 L10 and L31, D20 L837 and L977; C34 → U16 L32; P12 → PW10 L2 and L4; P09 → PM2 L4 and L8). W1–W21 are clean on the page, README, cards and claims.json (row 32). No record the page uses ends after 2026-04-07, and `validate_all()` returns `[]`. `cp20-update.md`, `cp20-claims.md` and W17–W21 exist; the §8.6 planned items are all present, unscored and "subject to the active plan". *Observation:* the page-copy claims P01, P02 and P15 cite "REV", the Owner's D1 review, which is not committed; `specimen.md` records its SHA-256 and the Owner's approval. |
| 3 | **Phase B**: tests green, negative controls included; **no typed research number in any generator** | **FAIL** | Tests 29–32 are green with their negative controls (row 20). But `scripts/mlflow_export.py`, a generator that plan §9.1 names as a consumer of the evidence layer, types research numbers into the committed export: line 75 "crisis-window 95% coverage rose from 79/408 to 131/408", line 92 "the same 10,747 development hours" and line 223 "448 represented development days". These are the CP-10 note, the CP-15 note and a step description, carried into `mlflow.note.content` and published at F1. `scripts/build_pages.py:2609` types "−0.0783 headline value" in the D1 token sheet. The values are correct (PW10 `covered_95` 79 and 131; `n_hours` 10,747; `n_days` 448), but they are not bound to records. This contradicts plan §9.1 ("No generator contains a typed research number") and invariant 17. `test_34` checks metric values only, not notes. |
| 4 | **Phase C**: the rehearsal's verifier passes; an interrupted upload resumes without duplicates; the deliberate faults are caught; no public write | PASS | The recorded rehearsal `passed: true`. My independent rerun on a fresh 3.5.1 loopback store also passed: an interruption at 115 writes; a resume with 13 created, 2 resumed and 8 already complete; 23 of 23 verified; an idempotent re-run; 1 run per `run_key` (SQLite); both faults caught (row 23). The export is exactly 23 runs (4 parents, 19 children), `--check` is current and the dry run is clean. `delu-generations` does not exist on DagsHub (`RESOURCE_DOES_NOT_EXIST`); there is no `mlflow_index.json` and no upload log. The spec document and test 34 exist. |
| 5 | **Phase D1**: the Owner approves the desktop and phone compositions; hierarchy clear; no meaning by colour or hover; real content fits; reader tasks show no research-versus-product confusion | PASS (on the record; I cannot re-perform the approval) | `specimen.md` "The Owner's Stop 1 decisions" records "D1 approved", the heading correction, the contribution wording, the public name and the device-test outcome. The page matches: "Performance during the 2022 price peak", the byline "Led by Yarden Viktor Dejorno · Contribution" linked to `#contribution`, the signed statement, `#research-results` separate from the archive's `#results`, the phone header "DE-LU" and the "[−0.0036, see below]" row. The specimen regenerates, including the seven-generation stress case, the token sheet and the demo states. Round 2 of the reader-task record reports no confusion, and my own read agrees. Content fits: 0 overflow and 0 clipping. |
| 6 | **Phase D2**: tests 17–34 green; `make verify`; no fetches; size budget; **§11.3 report checks pass locally** | **FAIL** | Tests 17–34: 382 passed. `verify_release`: PASS. Zero-fetch: 0 external references. Size: 1,520,336 ≤ 2,000,000 bytes. The §11.3 report checklist, however, names "Desktop Chrome and Safari; iPhone Safari". The committed record `release-checks/2026-09-27.json`, and my rerun, cover only Chrome 153 and Playwright's WebKit 26.6. The record lists "Desktop Safari and iPhone Safari themselves" and "screen-reader announcements" under `not_checked_here`. The contrast probe measures text only ("text_elements"), so non-text contrast (chart marks and state-carrying elements at 3:1, §7.12 and §11.3) was never measured on the rendered page. The preview's 80% interval band renders at 1.32:1. Every check that was run passes, and I reproduced it (rows 12–16). No iOS simulator is installed here, and enabling Safari automation would change a system setting, so I could not close this gap myself. |
| 7 | **Data**: every rendered research number re-derived from its source record | PASS | 665 of 665 bound values (HTML and SVG) match their source cell at the evidence tag, with correct rounding and CI endpoints (row 28). More than 80 values recomputed by hand, including the exact endpoint and seven confidence intervals. All 32 source blobs equal their tag blobs, and the public GitHub copy of `uncertainty.csv` has the registered blob. Unbound numerals outside the archive are only SVG accessible titles, the structural dates and versions, the attribution and the two release-record figures. |
| 8 | **Claims: the claim maps** | PASS | All 23 page claim IDs are in `cp20-claims.md` or `cp15-cp16-claims.md`; no W-ID is rendered; the sampled row citations resolve (item 2). |
| 9 | **Claims: the withheld phrases** | PASS | Guards and my own scans clean on every surface (row 32). The one pattern hit is v1's preserved archive text on CQR, protected by invariant 24. The review is described as "independent Integration review within this project's process", never as peer review. |
| 10 | **Claims: the labels** | PASS | "Development · post-selection" sits next to the v3 and v2 results; `NOT_DEMONSTRATED` is in the v2 branches; "This is not equivalence." is next to H−P; "a development diagnostic, not a product qualification"; there are no economics; the stale phrases (`delu-m4`, "the planned v2", and others) are absent from every surface. |
| 11 | **Claims: the exact H−P endpoint** | PASS | `+0.000003857628092332211` equals U16 L32 `3.857628092332211e-06` in full, in the chart note (desktop and phone), the interpretation, the values table and the README; never rounded and never in a tooltip. |
| 12 | **Claims: v1's label** | PASS | The badge reads "Confirmatory-style, not power-qualified" and the text "confirmatory-style, not power-qualified", next to the holdout result. `holdout_dm_label` agrees on all five surfaces (verify_release). |
| 13 | **Charts: units, direction and intervals** | **FAIL (minor)** | Units: one per axis, with separate panels for normalized scores and EUR/MWh (C2a against C2b). Intervals are labelled "paired 95% confidence interval", and the fairness disclosure says they are not forecast intervals. Direction is stated on the overview, C2a, C2b, v2 charts 1 and 2, C3, C4's MAE panel and C6. **C5, "MAE by local hour", states no better direction.** Its caption is "x: local delivery hour … y: MAE, EUR/MWh · each fold on its own scale", which misses §7.5's "Every chart states which direction is better". (C4's hit-count panel also gives none; that is defensible, since more hits are not simply better, but it could say "closer to nominal".) Fold 3's zero crossing is not cropped (the axis runs to +1). |
| 14 | **Charts: scales** | PASS | Every bound mark in 14 chart variants sits on its labelled scale (row 29), and every "no difference" line sits on the 0 tick (row 30). Comparable panels share a scale (overview 0.5–1.1; C2b −7 to 1; v2 chart 2 −0.04 to 0.01). C3 and C5 per-fold scales are labelled ("Each fold has its own scale"), with C2b as the paired view (G12). |
| 15 | **Charts: mobile variants** | PASS | Every new chart (preview, overview, C2a–C6, v2 charts 1 and 2) has a separate phone SVG (`data-variant="m"`) carrying the same values, labels, direction text and full endpoint. At 390, 360 and 320 px the text is at least 12 px, with no overlap, clipping or overflow (row 14). |
| 16 | **Charts: meaning survives without colour or hover** | PASS | Every mark has a direct value label. Generations have distinct markers (v1 triangle, v2 square, v3 circle; references a diamond; study an open circle; C5 dashed with squares against solid with circles). Values also appear in "View values" tables. There are no value-bearing `title=` tooltips. |
| 17 | **Links: internal anchors** | PASS | 111 ids, all unique. All 22 distinct internal `href="#…"` targets resolve, including the `#development-update` alias and the archive's own anchors. An anchor into a closed disclosure opens it in Chrome and WebKit (row 16). |
| 18 | **Links: the repaired link checker** | PASS | It exits 0 on the real surfaces (18 of 18 destinations 200) and exits 1 on a real 404 (row 11). Its mocked negative controls pass (test 33); local and example URLs are classified and not fetched. |
| 19 | **Links: MLflow routes** | PASS | The page advertises only `delu-cp2` routes (`#/experiments/0`, `#/models`, the root): REST resolves experiment 0 as `delu-cp2`, the registry holds `champion → 1`, and both render anonymously in a browser (rows 24–25). New-experiment links are shown as "(link added when the runs are published)", with no `href`. `--final` refuses to build while the four markers remain (row 21). |
| 20 | **Reading experience: the six reader tasks (§11.4)** | PASS | All six answered: tasks 1, 2, 3 (qualitative), 4 and 5 by screen 2 on desktop, and by screens 1–3 on phone; task 6 on screen 4 or 5 (desktop) and 6 or 9 (phone). No confusion between research progress and the released product; minor points listed above. |
| 21 | **Plan §6 invariants** | FAIL (invariant 17 only) | Invariants 1–16 and 18–26 hold, including: zero fetches; `make verify`; the rebuild reproduces committed bytes; v1's honesty statements exact; the `.mlflow` host only; GFS attribution on all four surfaces; the endpoint; the date guard; `pyproject.toml` and `uv.lock` untouched; no retired-tooling text; the placeholder guard; the README markers once each; demo states; planned work unscored. **Invariant 17** is breached by the typed numbers in `mlflow_export.py` (item 3). |
| 22 | **Plan §9.5 test table** | PASS | Tests 29–34 and the extended `test_23` exist with the listed checks and negative controls; tests 17–34: 382 passed with 0 skipped once the local Space build existed. |

**Non-blocking observations.**
- **The `delu-generations` note is in the present tense before the experiment exists.** The archive's "Tracking after v1" note (from `claims.MLFLOW_NEXT_NOTE`, also in `README.md` and `app/public/claims.json`) says the experiment exists with every policy. It will not exist until F1. The Phase F order (F1 before F6 and F7) protects it, but no mechanical guard does; the placeholder guard covers links only.
- **The rebuild check depends on the date.** `reports/cp3/pages_build.json` stamps `built_on` with today's date, a behaviour that predates PRES-1. The rebuild-equality check therefore passes only on the build date.
- **The keyboard probe is partial.** It checks the first 40 tab stops.
- **The preview's 80% band has low contrast.** It is conveyed by a legend, but its 1.32:1 contrast is the kind of non-text element §7.12 asks to check.

## On FAIL only

- **Single largest meaningful gap:** D2's "The §11.3 report checks pass locally" is not demonstrated for the browsers the checklist names. Desktop Safari and iPhone Safari were never run. Disclosure announcement with a screen reader, and non-text contrast of rendered chart marks (the preview band is 1.32:1), were never checked. Only Chrome and Playwright's WebKit engine were run.
- **Exact next acceptance test:** at a new candidate, a committed `reports/presentation/release-checks/<date>.json` must record the §11.3 Report row passing on Desktop Safari and iPhone Safari, with VoiceOver announcing the disclosures and rendered non-text elements at 3:1 or better (or an Owner decision recorded for the band). The same candidate needs a test that fails on any typed research numeral in `scripts/mlflow_export.py` and `scripts/build_pages.py`, with the export notes rendered from evidence records and `mlflow_export.py --check` still passing. C5 also needs a stated direction ("lower is better").
