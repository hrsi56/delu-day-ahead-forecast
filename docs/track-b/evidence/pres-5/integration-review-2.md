# Verdict — PRES-5 — Integration — FAIL

- Candidate SHA: `9bb0cff8578757854a3008f5bb6537d2ce367026` (`gauntlet/pres-5`; base `main` = `3c8e158c9895f5b3fed13db794b0ddd5fb80c56f`; the page `docs/index.html` at it: `409e1708055b3a91d768ab2ebc0bd527ac63384278b3d971b8843180e1641cbe`, 1,848,377 bytes; `README.md`: `5f50309c523eda9123ebcdf40f313bdb085147880c2c76fc9ee7b5d481501e16`).
- Plan / version / bar: `capstone_v21.md`, v21-r20 (file SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`), `### 24.14 Publishing and going live before 4.7T (v21-r20)` (115 lines, 7,426 bytes, SHA-256 `5d38de24b3c68ec01e2f5c4e6eaf368c253485107549fc2d85c3c71ccf2f5349`). Publication anchor: `docs/PUBLISH_RULES.md` revision 1.5, `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`. The brief: `docs/track-b/evidence/pres-5/issued-brief.md`, `9eb2a58433f41739fc22744854c4c55b099cc05ca729b677e9b3b5ccef87ebc3`.
- Verbatim bar excerpt (extracted with `scripts/bar.py bar --at 9bb0cff8… --quote` from `main`; checked against the file at the candidate with `scripts/bar.py check`):

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

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: yes. `git -C /Users/djourno/Downloads/PJM/.local/worktrees/pres-5/critic-2 status --porcelain` printed nothing at the start, after every build and test step, and at the end; `HEAD` stayed `9bb0cff8578757854a3008f5bb6537d2ce367026` throughout. Ignored byproducts only (`.venv/`, `app/public/`, `.pytest_cache/`).
- Reviewer: a fresh Integration Critic that authored none of PRES-5. Cooperative isolation only: no sandbox, read-only by procedure. No Git write of any kind. I did not open the Claude memory directory, `progress.md`, any syllabus, Track A or C material, `docs/track-b/orchestrator-role.md`, or any Lead working note (the session scratchpad already held files from before this review; I opened none of them). No credential was read, printed or used, and no network call was made.
- Reading order (§10.1, §10.3): the brief, the bar, PUBLISH_RULES 1.5, the runbook, the template, the packet, the code, the records and the generated surfaces first; my findings were formed before I read `editorial.md`, `fresh-reader.md` and `integration-review-1.md`.

## Commands actually run

All from `/Users/djourno/Downloads/PJM/.local/worktrees/pres-5/critic-2`, with `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1` (and `MLFLOW_DISABLE_AGENT_HINT=1`) exported. Outputs went to the session scratchpad outside the worktree.

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git status --porcelain`; `git rev-parse HEAD`; `git merge-base HEAD main` | 0 | empty; `9bb0cff8578757854a3008f5bb6537d2ce367026`; `main` = merge base = `3c8e158c9895f5b3fed13db794b0ddd5fb80c56f` |
| 2 | `git show main:scripts/bar.py \| python3 -I - bar --at 9bb0cff8… capstone_v21.md "### 24.14 …"` (and `--quote`); `… identity --at 9bb0cff8… capstone_v21.md` and `docs/PUBLISH_RULES.md` | 0 | "section 115 lines, 7426 bytes, sha256 5d38de24…2f5349"; file `80341681…30e6`, "# Capstone v21-r20 — publishing and going live before 4.7T"; PUBLISH_RULES "Revision: 1.5", `1bc0c523…f94e` |
| 3 | `shasum -a 256` over the brief, decision 28 and the brief's 18 execution inputs | 0 | every hash equals the brief's (brief `9eb2a584…ebc3`, decision 28 `4daa5617…0215`, PRES-4 packet `6c1ec149…`, …, CP-18b landing `fe191d89…efe2`) |
| 4 | `uv sync --frozen` | 0 | environment from the lockfile |
| 5 | `uv run python -m delu_forecast.final_candidate --check` | 0 | `{"identical_to_committed": {"metrics.csv": true, "parity.json": true, "preview-day.csv": true, "ratio-intervals.csv": true, "summary.json": true, "uncertainty.csv": true}}` |
| 6 | `uv run python -m delu_forecast.compact_figures --check` | 0 | `{"pixel_identical": true, "problems": []}` |
| 7 | `uv run python scripts/mlflow_export.py --check` | 0 | "the committed export is current" |
| 8 | `uv run python scripts/mlflow_export.py --diff-against 3c8e158c` | 0 | "runs 44 -> 105 (added [cp26 and its 52 children, cp28, cp28/A1 … cp28/A7]); checked {params 362, metric_points 16753, datasets 90, artifacts 107, artifacts_digest_unchanged 107, …}; identity changes on 0 runs; substantive changes: none; only_identity=True" |
| 9 | `uv run python scripts/build_pages.py`, then `git status --porcelain` | 0 | "wrote …/docs/index.html (1,848,377 bytes)"; status empty (the page and `reports/cp3/pages_build.json` reproduce byte for byte) |
| 10 | `uv run python scripts/readme_research.py`, then `git status --porcelain` | 0 | "regenerated the glance and generations blocks"; status empty |
| 11 | `uv run python scripts/lint_publication.py` | 0 | "page: 0 finding(s) / readme: 0 finding(s) / templates: 0 finding(s) / PASS" |
| 12 | `uv run python scripts/build_wasm_payload.py`, then `git status --porcelain` | 0 | "payload: 15,363,807 bytes across 14 files"; status empty |
| 13 | `uv run pytest -q -rfEs` (whole suite, Python 3.13, 20 min 18 s) | 1 | **3,237 passed, 9 skipped, 2 failed**: `tests/cp18a/test_dry_run.py::test_a_real_dry_run_then_the_fallback_finds_the_day_claimed` and `tests/cp18a/test_forced.py::test_each_cause_is_forced_and_recorded`, both "publication-guard: BLOCKED … reports/cp3/pages_build.json is a non-final build record (final: false)" — the by-design refusal the brief names. Skips: eccodes absent; CP-16 identity/ledger (6); CP-24 draft export bound to its manifest; CP-28 GFS note needs local CP-26 outputs |
| 14 | `shasum -a 256 docs/index.html README.md`; `wc -c docs/index.html`; `cat reports/cp3/pages_build.json` | 0 | page `409e1708055b3a91d768ab2ebc0bd527ac63384278b3d971b8843180e1641cbe`, 1,848,377 bytes; README `5f50309c…1e16`; build record `final: false`, `links_omitted_until_verified: ["compare:v6"]` |
| 15 | `python3 -I <scratch>/pagetext.py docs/index.html …` (and on `3c8e158c:docs/index.html`), then `diff` of the two texts from v5's chapter on | 0 | visible text with closed-disclosure depth marked; v5–v1 chapters and the archive unchanged apart from v1's chapter links (`#v1-archive`, `/history/`, a note outside the archive), the planned list and the system section |
| 16 | `git diff --name-status 3c8e158c HEAD`; path families against the brief's allowed paths and CP-18c's paths | 0 | 64 paths (37 added, 27 modified, none deleted); none outside the allowed families except O34's `tests/test_cp26_r15.py`, `tests/test_cp26_repair_contract.py` and `tests/pres5_landed_code.py`; no CP-18c path; no anchor, governance, `PUBLISH_RULES` or frozen record |
| 17 | For each modified file: its SHA-256 and blob at `3c8e158c`, `git grep` for them at `HEAD` outside `evidence/pres-5` | 0 | the five `src/delu_forecast` modules are pinned in `reports/rebaseline/harness-log.json` (O34), its preserved r13 copy, and `reports/cp17c/inputs.json`; README/page/export hashes only in PRES-4's historical records; nothing in `src/cp26/harness.py::PINS` or any freeze manifest |
| 18 | `python3` over `docs/track-b/evidence/cp-17c/freeze-manifest.json` | 0 | 54 named paths; none under `src/delu_forecast`, `scripts/`, `README.md` or `docs/index.html` |
| 19 | O34: for the five recorded copies, SHA-256 of the snapshot, of `git show 61658c70…:<path>`, of `git show 3c8e158c:<path>`, and the harness log's `landed_code` entry; `git diff --quiet 3c8e158c HEAD -- reports/rebaseline src/cp26 docs/track-b/evidence/cp-26` | 0 | all four equal for each module (`6e084403…`, `9f562771…`, `38df896b…`, `d9c3ca61…`, `b8bc3018…`); the log has 146 entries and neither new module; "CP-26 records/harness unchanged" |
| 20 | `uv run python -c` over `reports/pres5/a1-in-v5/summary.json`, `metrics.csv`, `ratio-intervals.csv` | 0 | coverage 10,747/10,747 keys, 448 days, `output_source` native 448, `fallback_days` 0, per fold 2,160/2,159/2,112/2,160/2,156; bootstrap seed 15042, 2,000 replicates, 7-day blocks, `index_equals_cp20` true; parity `max_abs_difference` 0.0; ratios A1−v5 MAE −0.05651 [−0.09025, −0.02450] (97.5%: −0.09643, −0.02125), WIS −0.11403 [−0.14540, −0.07891] (97.5%: −0.15073, −0.07524); A1−B0 −0.50719 [−0.53571, −0.46495], −0.56263 [−0.58938, −0.52281]; per-fold MAE 4.518, 7.051, 43.193, 13.092, 13.371 |
| 21 | `uv run python -c` over `reports/cp28/results/selection.json`, `holm.csv`, `owner-summary.json` | 0 | 7 arms, all pass all four; selected A1, WIS 9.6825 (next A6 10.1294, tie bound 9.7309); A1 MAE ratio 0.93105 [0.90930, 0.94865], WIS 0.89070 [0.87149, 0.91043]; Holm primary A1 raw = adjusted 0.0041996; GFS +6 h MAE +13.99% [1.1034, 1.1611], WIS +15.46% [1.1208, 1.1758]; 18 fallback dates per arm |
| 22 | `uv run python -c` over `derived.get(...)` and `derived.display(...)`; `derived.validate_all()` | 0 | `cp26.v5-v4` MAE −0.660 [−1.409, +0.939] → "−1% [−1%, +1%]", WIS −0.503 [−1.197, +1.025] → "−1% [−1%, +1%]"; `noload-v5` +0.066 / +1.097; `cp26.v6-v5` −6.895 / −10.930; `validate_all()` → `[]` |
| 23 | `python3 -I` over the reports/cp18b records | 0 | `acceptance.json`: Chromium 153.0.8010.12, WebKit 26.6, macOS, 2026-11-05T03:14:33Z → 03:24:32Z, both "fresh anonymous cold start" checks pass with `ready` true at 1.86 s; `space-build.json` first visit 551,515 bytes |
| 24 | `python3 -I` decoding the page's seven `data:image/png` URIs against `reports/pres5/compact-figures/*.png` and two originals | 0 | all seven compact copies embedded; neither original embedded |
| 25 | `grep` of every `YYYY-MM-DD` after 2026-09-06 in the page text and inside every `<script>` | 0 | text: decision, freeze, label, 4.7T-term and measurement dates only; scripts: none |
| 26 | `RC.withheld_findings(...)` on 12 probe sentences | 0 | W51 fires on "…pooled with the five (test) periods" and not on "never pooled with the five periods above"; W52 on "the prospective score of 4.7T", "4.7T's result was a pass"; W53 on "v6 is released", "A1 became live"; W50 on "the same information set as v5"; **no guard fires on "The Space runs v1 now" or "the demo runs the released model, v1"** |
| 27 | `git diff --name-only 3c8e158c HEAD > <scratch>/pres5-paths.txt`; `xargs git --no-pager diff --quiet HEAD HEAD -- < …`; `xargs git --no-pager diff --quiet 3c8e158c HEAD -- < …`; `git diff … --pathspec-from-file=…` | 0 / 1 / 129 | the packet §8.2 "(main moved)" form: equal trees exit 0, differing trees exit non-zero (fails closed); the old form prints `usage: git diff …` on git 2.50.1 |
| 28 | Packet §6's `--authorized-runs` list against the export's run keys; `grep add_argument scripts/mlflow_publish.py` | 0 | 61 = 61, identical sets; `--precheck`, `--target public`, `--owner-instruction`, `--authorized-runs`, `--authorized-experiment-tags` (requires `--authorized-runs`), `--log` exist |
| 29 | `grep add_argument/add_parser` in `publication_receipt.py`, `verify_mlflow_mirror.py`, `check_reader_paths.py`, `publication_guard.py`, `secret_guard.py` | 0 | every flag and subcommand packet §8.2–§8.6 uses exists (`--landing --bundle --expect --date`; `verify --target`, `index --mirror-record --browser-record`; `release`, `mlflow-routes --mirror-record --shots --out`; `tree`; `pre-push`) |
| 30 | `brew list --pinned`; `brew list --versions node` | 0 | `node` pinned; node 26.7.0 |
| 31 | `PLAYWRIGHT_BROWSERS_PATH=/Users/djourno/Downloads/PJM/.local/tools/ms-playwright /Users/djourno/Downloads/PJM/.local/tools/playwright/bin/python scripts/check_reader_paths.py release docs/index.html --shots <scratch>/shots --out <scratch>/release-critic2.json` (05:01–05:09 UTC) | 0 | "passed=True"; served over `file:`; every view as in B16 |
| 32 | `python3 -I -m http.server 8793 --bind 127.0.0.1 --directory docs` (stopped afterwards), then the same `release http://127.0.0.1:8793/index.html --shots <scratch>/shots-http --out <scratch>/release-critic2-http.json` (05:10–05:18 UTC) | 0 | "passed=True"; served over HTTP; placements identical to command 31; the server log holds 33 requests, every one `GET /index.html` |
| 33 | `uv run python scripts/rebuild_presentation.py`, then `git status --porcelain` | 0 | README research block, README CP-3 section, MLflow export, static page, "cross-surface agreement and zero-fetch checks: ok"; status empty (README line 454 is the generator's current output) |
| 34 | `git show main:scripts/bar.py \| python3 -I - check <this verdict> --source capstone_v21.md@9bb0cff8578757854a3008f5bb6537d2ce367026` | 0 | "ok: lines 7–121 (7425 bytes) appear in capstone_v21.md@9bb0cff85787" |
| 35 | `git status --porcelain`; `git rev-parse HEAD` (end) | 0 | empty; `9bb0cff8578757854a3008f5bb6537d2ce367026` |

## Evidence actually inspected

- **Governing text:** the brief (all of it); `capstone_v21.md` §24.14 (extracted); `docs/PUBLISH_RULES.md` 1.5, all sections and A1–A12; `docs/track-b/publication-standard-v1.md` §4 (precision, near-zero); `docs/track-b/publication-runbook.md` (all); `docs/track-b/publication-packet-template.md` (all); `docs/track-b/gauntlet-templates.md` §2; `docs/track-b/owner-decisions-2026-11-05.md` (decision 28); `AGENTS.md`.
- **The packet** `docs/track-b/evidence/pres-5/publication-packet.md` (all 687 lines) and the claim map `docs/track-b/research-content/pres5-claims.md` (all).
- **Code:** `src/delu_forecast/final_candidate.py` (all); `compact_figures.py` (`check`); the `derived.py` diff; `research_claims.py::WITHHELD_PATTERNS` W49–W53; `scripts/build_pages.py` (`live_measurement`, `opening`, `PRES5_TAG`, `main`, the v6 chapter's audit row); `registry.py::EVIDENCE_TAGS`; `scripts/cp3_readme.py` and its diff; `scripts/mlflow_publish.py::main`; `tests/pres5_landed_code.py`; the diffs of tests 24, 35, 37, 43 and the two CP-26 tests; `tests/test_50_pres5_publication.py` (lines 192–422); `src/cp18/live_claims.py` lines 55–95 (read only, a CP-18c-owned path).
- **Records:** `reports/pres5/a1-in-v5/*`; `reports/cp28/results/{selection.json,holm.csv}`, `owner-summary.json`; `reports/cp18b/{acceptance.json,space-build.json}`; `reports/presentation/mlflow-export/{cp26,cp28}.json` (names, tags, notes), `release-checks/pres-5-export-diff.json`, `pres-5-local-release.json` (header, views, discovery) and the `served_over` field of every PRES-2–5 local release record; `docs/track-b/evidence/pres-5/cp26-landed-presentation-code/manifest.json`; `reports/rebaseline/harness-log.json` (`landed_code`); `reports/cp17c/inputs.json` (`files`); `docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md` §§1, 2, 5–8; `docs/track-b/cp-17c-landing-2026-10-30.md` (identity, host, 58 of 58).
- **Surfaces:** `docs/index.html` at the candidate, as text with every disclosure's depth marked, opening to attribution; the same for `3c8e158c`; `README.md` (the full diff against `3c8e158c`, and lines 225–240, 440–470, 555–570).
- **Earlier reviews, after my findings:** `editorial.md`, `fresh-reader.md`, `integration-review-1.md`.

## Checklist verdict

### A. The brief's observable outcome

| # | Item | Verdict | Evidence |
|---|---|---|---|
| 1 | A1 (v6) in v5's comparison: v5's population, A1's stored forecasts, v5's rows unrecomputed, paired comparisons v6−v5 and v6−naive with the rule's intervals, never "adopted", every value derived | PASS | Commands 5, 20: CP-28's stored A1 forecasts (`hourly.parquet` pinned `f5cb02a1…`, manifest `f092140e…`) cover 10,747/10,747 hours and 448/448 days, all native, none a fallback; scored by `cp22.scoring` with CP-20's index set (`index_equals_cp20` true), seed 15042, 2,000 replicates, 7-day blocks; B0/HG/v5 recomputed only for pairing, parity 0.0 against `reports/ddnn2/attempt-1/metrics.csv`, and the page's v5–naive rows are CP-24's. The information-set differences and the 2020 warm-up are stated on the reading path (`v6.caveat.information`) and in `#v6-information`. Page: "−6% [−9%, −2%] … −11% [−15%, −8%] … at 97.5% … [−10%, −2%] and [−15%, −8%]"; naive "−51% [−54%, −46%] … −56% [−59%, −52%]"; "A description, not a decision: v5's adoption rule was not re-run". All equal command 20's values rounded; `validate_all()` empty |
| 2 | CP-26 on every development day: question, population, results, class; beside, never pooled | PASS | `#everyday`: "A separate population: 2,068 eligible days from 2020-12-29 to 2026-09-06, every policy refitted daily under one protocol · … · never pooled with the five periods above · development, post-selection". The table's EUR/MWh and ratios equal `owner-summary.json` (v6 17.2/0.4974, 9.7/0.4580; v5 18.5/0.5342, 10.9/0.5142; naive 34.6, 21.1). v5−v4 "−1% [−1%, +1%]" on both, "the intervals do not establish that the two are equal" (§3.2). GFS +6 h "+14% [+10%, +16%]", "+15% [+12%, +18%]"; no-load "barely moved … +1%, point comparisons". The question is carried by the heading and the validation topic rather than as a sentence; adequate |
| 3 | CP-28's selection: arms, rule, result, why A1 | PASS | `#v6-selection`: the rule in words, set 2026-10-12; "All seven passed every analysis. v6 had the lowest interval error, 9.68 EUR/MWh against the next best's 10.13"; p 0.0042 (raw maximum = Holm-adjusted for A1, command 21); the arms table, six named in words, "Not selected"; the Holm conditionality (`v6.holm.note`). Decision slot on the reading path names the six others |
| 4 | The freeze and 4.7T's registered terms; what pass and fail mean | PASS | `#v6-freeze`: 2026-10-28, 10-29, 10-30, "all 58 fits came out identical bit for bit", "begins 720fc581", host "Pyodide in Node.js on a macOS runner or the Owner's Mac" (CP-17c landing: 58 of 58, Pyodide 0.28.0 in Node.js v26.7.0). `#v6-fresh-test` against protocol §§1, 2, 5–8: window 2026-09-07 to 2026-12-05, not before 2026-12-04, never extended/shortened/rolled; control v5, reference naive, v3/v4/v1 descriptive; daily p50 MAE and WIS; largest of four one-sided p ≤ 0.05 with the 0.995 margin; 7-day blocks, 10,000 replicates; ≥ 60 of 90, else inconclusive; no runner-up, window spent, null valid. Meaning per decisions 20–21/28 and O29. (Wording note R4 below) |
| 5 | The product: opening pairs A1 with the product; Space linked and described; v1 at `/history/`; no live number; nothing after 2026-09-06 | PASS on the report; see G1 for the README | Opening: "Live product · v6 · DDNN-2 alone" / "Final candidate · pending 4.7T · v6 · DDNN-2 alone"; "Open the live product" → `https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast`; "By the Owner's decision, the Space runs v6 · DDNN-2 alone daily before its one test: prospective evaluation in progress…"; "v1's historical demo" → `…static.hf.space/history/`. No `live*` record on the page (`test_the_report_shows_no_live_number`); command 25. The README's line 454 still says the Space runs v1's boosters (G1) |
| 6 | Model identity (§4): public name and status; CP-26's and CP-28's unselected arms as study arms | PASS | "v6 · DDNN-2 alone", kind generation, status "final candidate 2026-10-30"; "A1 in the frozen records" beside the identity (every reading-path "A1" checked, 7 occurrences, all beside v6); CP-28's six others `study arm`, "not adopted 2026-10-25", named without codes on the page; CP-26's six sensitivity routes study arms |
| 7 | MLflow prepared exactly as authorized (export, its diff, the bounded command) | PASS | Commands 7, 8, 28: the export is current; 44 → 105, the 61 cp26/cp28 runs added, no identity or substantive change, one experiment-tag change `mlflow.note.content`; packet §6's `--authorized-runs` equals the 61 exported keys exactly, `--authorized-experiment-tags mlflow.note.content` only, `--precheck` first, `--target public` needs `--owner-instruction`. The upload itself comes after a PASS |
| 8 | The page budget | PASS | 1,848,377 bytes ≤ 2,000,000 (command 14), by embedding pixel-identical RGB copies of the archive's seven figures (commands 6, 24; O25) |
| 9 | Review: the check passes at the candidate | **FAIL** | This verdict (G1) |
| 10 | Packet §8: payloads and ready-to-run commands for the LAND, push, public checks and A12 | PASS, with packet note N2 | Commands 27–29: the "(main moved)" check now runs on git 2.50.1 and fails closed; every flag exists; the secret-scan stdin follows the pre-push format; A12's two conditions and its useful check (the two Space routes) are named. N2: the evidence-date step verifies but nothing sets the date |

### B. The complete authoritative checkpoint bar — PUBLISH_RULES 1.5

| # | Clause | Verdict | Evidence |
|---|---|---|---|
| B1 | §1.1–§1.3 authority, four identities, categories | PASS | Hashes verified (command 3); rule revision, generation, product status and artifact identities kept apart in packet §1 and on the page |
| B2 | §2 reader contract and placements; A1; A2 | PASS | Each headline value names its metric ("in point error", "in interval error"); terms directly beneath; placements, my runs (commands 31, 32), Chrome / WebKit: the headline block ends at 800.6 / 801.3 px of 900 (1440 × 900) and 628.6 / 628.7 px of 844 (390 × 844); the finding at 1,672.6 / 1,673.3 px against A2's 1,744 (h = 56 px) and 2,394.5 / 2,394.3 px against 2,420 — equal to the Lead's record |
| B3 | §3.1 evidence classes, withheld claims | PASS (note N1) | "Development · post-selection" on every v6, CP-26 and CP-28 number; nothing live or 4.7T's; W49–W53 find nothing on page or README (`test_50`) |
| B4 | §3.2 scores, comparisons, uncertainty | PASS | Verdict with rule, date and N (7); changes as shares of the comparator with the ratio's interval from CP-24's own draws at 95% and 97.5%; absolute MAE with the stress period apart; every-day results as their own population; "descriptive 95% intervals" vs "95% confidence intervals" labelled; the null v5−v4 not read as equivalence |
| B5 | §3.3 counting | PASS | N = 7 (the rule's); 13 rows distinguished from the 25-policy census and from v6's own rule ("8 of them were tested against the targets … v6 … was tested by its own selection rule") |
| B6 | §3.4 provenance, formatting, negative controls | PASS (note N1) | Every number a record (`validate_all()` empty; lint 0 findings); whole percents, one decimal EUR/MWh, ≤ 4 significant figures; values re-derive (command 5) |
| B7 | §4 registry, transitions (A3), branches | PASS | One registry; v6 a generation with its dated final-candidate status and no adoption event; "From v5 to v6: DDNN-2 alone" with predecessor, change, comparator (also the predecessor), result with class, limits, dated decision and route; six arms study arms |
| B8 | §4 A10 | N/A | No generation revised in place |
| B9 | §5 A4 order; §5.1 twelve subjects | PASS | Opening → How the product works (v6, twelve topics, attribution and importance "not evaluated in this report" with routes) → comparison → lineage → chapters → planned → depth → contribution/terms |
| B10 | §5 A8 product-first order | Not graded | Open item, packet §10.3 (1), consistent with O27 (v1 stays released until 4.7T) |
| B11 | §5.2 chapter grammar; 2.0 MB | PASS | `slot_problems(a1_slots())` empty (`test_50`); 1,848,377 bytes |
| B12 | §6 charts, discovery, A5 | PASS | v6's chart: four labelled rows, hexagon marker, zero line "no difference", values table; A5 discovery, my runs: 48 routes in each engine at 1440 × 900 and 390 × 844, by mouse, keyboard and deep link, all passed |
| B13 | §7.1 product contract beside the action | PASS | "About 0.55 MB on a first visit; ready within 1.86 s in Chromium 153 and WebKit 26.6 on a Mac, served locally on development data, 2026-11-05; last verified 2026-11-05", beside "Open the live product", outside any disclosure; each value read from CP-18b's records (command 23) |
| B14 | §7.2/A7, §7.3/A9 | N/A here | The Space is CP-18c's; the report shows no live panel or number (§24.14 item 5) |
| B15 | §8 surfaces and evidence links | **FAIL** (G1) | Report, README glance/generation blocks and MLflow agree (`test_39`); audit links typed and dated; MLflow names registry-driven. README line 454 contradicts the README's own product line (G1) |
| B16 | §9 browser and accessibility matrix | PASS | Commands 31–32: Chrome 157.0.8103.51 and WebKit 26.6 at 1440 × 900, 768 × 1024, 390 × 844, 360 × 780, 320 × 640 and the emulated iPhone 393 × 659; accessibility trees pass in both engines; 161 keyboard stops in document order, none without visible focus, anchors open closed disclosures; touch targets at 390 px: 229 checked, none under 44 px; contrast: no text (4,893 / 4,886 checked) or non-text mark (827 / 797) below threshold; 200% zoom and 320 px reflow without overflow; chart text at least 12.21 px; no chart overlap or clipping, collapsed space, console error, failed request, HTTP error or resource after the document. No real Safari, iPhone or screen reader was used |
| B17 | §10.1 independence | PASS | Editorial, fresh reader and this check authored none of PRES-5 |
| B18 | §10.2 fresh reader | PASS | Six unchanged questions, closed screens only, answers kept; answers 1–5 graded against the records; the six-arms gap repaired |
| B19 | §10.3/A6, §10.5/A12 | After deployment | Packet §8.5–§8.6 name the receipt, the browser records, A12's two conditions and the useful check |
| B20 | §11 packet and order | PASS (notes N1–N3) | Build → editorial → fresh reader → independent check → upload → final build → recheck → Orchestrator; the packet carries every §11 item |
| B21 | §12 baseline coverage; invariant 10 | PASS | No research number, chart or choice uses a day after 2026-09-06 (command 25); the archive's text unchanged |
| B22 | §13 acceptance record | PASS | Packet §9.2 |
| B23 | §14 pending triggers | PASS | "Before final-candidate test" items decided by decisions 20–21 and O27/O30; "Before Live" is CP-18c's |
| B24 | A11 | PASS | Pauses disclosed in packet §10.2 |
| B25 | The runbook's touchpoints | PASS | Packet §9.3; `tests/test_42_publication_runbook.py` green in command 13 |
| B26 | The packet template, every section | PASS | §§1–8 present and filled; §5d defers the live-operation fields to CP-18c with reasons; `<…>` only for post-review identities |
| B27 | r20 §24.14: A1 frozen and untouched; 4.7T terms unchanged; research numbers on development data only (P1); PUBLISH_RULES 1.5 | PASS | No `src/cp17*`, `src/cp28`, `src/cp26` or freeze record changed; the freeze manifest names no changed path (command 18); command 25 |
| B28 | Templates §§2–3 | PASS | This verdict follows §2 |

### C. Task-specific extract and applicable constraints

| # | Item | Verdict | Evidence |
|---|---|---|---|
| C1 | CP-18c's paths never touched | PASS | Command 16 |
| C2 | The Space's address and wording | PASS | The brief's URL on both actions; wording stands if CP-18c has not published |
| C3 | The red line for research; the report reads no live record | PASS | Command 25; no `live/` path or record read by the build |
| C4 | Ceilings | Not graded here | The return names machine-hours |
| C5 | Presentation: tokens; visual choices the Owner's | PASS | v6's colour and hexagon carried as an open item (packet §10.3 (3)) |
| C6 | Homebrew `node` pinned and installed | PASS | Command 30 |
| C7 | Credentials | PASS (no value seen) | No credential read; the export's outbound scan and the secret guard are the Lead's records |
| C8 | Allowed paths; no anchor, governance, `PUBLISH_RULES`, frozen record | PASS | Command 16; the O34 exception below |
| C9 | No earlier evidence binds an edited file's bytes | PASS (note N3) | Command 17: the harness log (O34); `reports/cp17c/inputs.json` records the five modules as files of CP-17c's scratch tree, and nothing re-verifies it against the working tree (suite green; command 18) |
| C10 | Tools, memory, non-interactive owner commands | PASS | Packet §8 commands use `--no-pager` and `-F <file>`; no editor or pager |

### D. Integration review 1's acceptance test

| # | Test | Verdict | Evidence |
|---|---|---|---|
| D1 | The line beside "Open the live product" shows all five §7.1 fields, each read from a committed record | PASS | B13; `live_measurement()` reads `reports/cp18b/acceptance.json` and `space-build.json`, refuses a failed or one-engine start; each value carries `data-release-check` pointers (`#size`, `#checks`, `#engines`, `#started_utc`, `#finished_utc`) |
| D2 | `test_f03` checks all five with a negative control | PASS | `test_f03_the_measured_start_is_beside_the_action_outside_any_disclosure` asserts each field and each pointer; `test_f03_negative_control_a_failed_or_one_engine_start_is_refused` (a failed start; WebKit removed) |
| D3 | A working §8.2 command for a moved `main` | PASS | Command 27 |
| D4 | A check on the `evidence/pres-5` date | PASS (note N2) | §8.2 step "Expect the same date on both lines … stop"; `test_the_evidence_tags_date_is_the_tips` |
| D5 | New wording for F4 | PASS | "v5's gain over v4 is not shown there"; "the intervals do not establish that the two are equal" |
| D6 | F5's packet wording | PASS | Packet §2 and §10.2 now say the lint does not check placement; every reading-path "A1" sits beside v6 (checked) |

### E. The Orchestrator's rulings

| Ruling | Verdict | Evidence |
|---|---|---|
| O25 | PASS | Commands 6, 24; `test_a_changed_pixel_is_caught` |
| O26/O29 | PASS on the report; the README breaks its intent (G1) | "How the product works": "The product the Space runs, v6 · DDNN-2 alone"; v1's manual in its chapter and archive; decision 21's fail branch in `v6.fresh.meaning`; nothing on the page says the Space runs v1 now |
| O27 | PASS | Hero "Final candidate · pending 4.7T", CP-28's verdict with the development post-selection badge; v1 "Released · September 2026", "the last released generation", demo at `/history/`, the product again if 4.7T does not pass |
| O30 | PASS | B7, outcome 6; MLflow names carry codes in parentheses, as earlier runs do |
| O34 | PASS | Its four conditions hold: (1) the five recorded copies equal `61658c7`'s and `3c8e158c`'s bytes and the harness log's entries, bound by SHA-256 and git blob (command 19); (2) every other landed file is still compared with the working tree (`pres5_landed_code.landed_code`, `test_any_other_landed_file_is_still_compared_with_the_working_tree`); (3) negative controls for a changed copy, a copy that no longer matches the log, and another landed file (`test_50` lines 362–406); (4) the two new modules are named and excluded explicitly. No CP-26 record, manifest or harness file changed. The CP-26 scientific code does not import the five modules |

## Findings (PUBLISH_RULES §10.1)

### Existing-rule violations

**G1 (medium; decides this verdict). The README still says the Space runs v1's champion, directly under the line that says it runs v6; the editorial review's V5 named this sentence and the packet records V5 as repaired.**
- **Clause:** PUBLISH_RULES 1.5 §8: "The report, README, Space card, direct demo and MLflow must agree on identity, status, applicable limitations and claims"; "README: … v1's historical read belongs under its v1 heading. No hand-written current-state claims." The brief's outcome 5 ("v1 is the historical demo, reached at the Space's `/history/`") and outcome 10's packet; §10.3: "identify … claims of closure that the new evidence does not support".
- **Observation:** `README.md` line 446 (generated by `scripts/cp3_readme.py::_since_release`) reads "The table describes the surfaces at v1's release. The Space's root now runs the live product, v6 · DDNN-2 alone, and the report documents it; v1's demo, which the second row describes, is under its History." Line 454, the paragraph right after the table, still reads, in the present tense: "The Space cannot load the packaged `mlflow.pyfunc`, so it runs the champion's own nine boosters, base-catalog preprocessing, four CQR thresholds and isotonic step in the browser — and … its output equals the frozen artifact bitwise". The dated line scopes "the table" only. The same README's product line (line 19) says "the Space runs v6 · DDNN-2 alone daily". Whichever state the Space is in, one of the two README sentences is false; after CP-18c publishes, line 454 is.
- **History:** the editorial review's V5 cites "README lines 448–449, 452 and 538"; at `b20ee9d1` line 452 is this sentence (`git show b20ee9d1:README.md`). Packet §10.4 reports V5 repaired ("a dated line says the table describes the surfaces at v1's release …; the replay sentence names v1's demo") and §7 says all twelve violations were repaired in `1d0f453e`. Lines 448–449 and 538 were addressed; line 452 (now 454) was not. Packet §3 and §5b present "v1 presented as what the Space runs now" as withheld claim W53, guarded with negative controls; no such guard exists (the code's and the claim map's W53 is "v6 given the status live or released"), and no guard fires on "The Space runs v1 now" (command 26). That is why nothing caught it.
- **Impact:** the README, a published surface, contradicts itself and the report on what the product runs. The report is unaffected.
- **Repair:** in `scripts/cp3_readme.py`, put the paragraph in the past or name its subject, for example "At v1's release the Space could not load the packaged `mlflow.pyfunc`, so v1's demo, now under the Space's History, runs the champion's own nine boosters …"; regenerate (`scripts/rebuild_presentation.py`).

### Packet accuracy (not violations by themselves)

- **N1. The withheld claims W50–W53 are described wrongly in packet §3, and two have no negative control.** Packet §3 lists W50 "a live, prospective or 4.7T result", W51 "the same protocol as v5", W52 "pooling …", W53 "v1 presented as what the Space runs now". The claim map and `research_claims.py::WITHHELD_PATTERNS` define W50 = same protocol or information as v5, W51 = pooling with the five periods, W52 = a live record as 4.7T's result, W53 = v6 "live" or "released". §5b and §10.1 (O26/O29) cite "W53" as the guard that the page never implies the Space runs v1 now; no guard does that. §3 says each of W49–W53 has negative controls in `tests/test_50`; `test_the_withheld_claims_are_guarded` has positive cases for W49, W50 and W53 only, and does not assert which guard fired, unlike PRES-3's and PRES-4's per-guard parametrized controls (`test_45` line 549, `test_49` line 481). My probes (command 26) show W51 and W52 do fire, so §3.4's substance holds; the packet overstates it.
- **N2. Nothing sets the `evidence/pres-5` date.** `registry.py` hard-codes `"evidence/pres-5": ("", "2026-11-06")`, so the page and README label v6's raw rows "frozen 2026-11-06", while the tip will be dated 2026-11-13 or later. Packet §8.2 says the registry date is the one "the `--final` build set to the tip's date", and the registry's comment says "the final build and the return check" it; `build_pages.py --final` only checks route coverage (`main`, lines 4592–4596). §8.2's date step fails closed, so no wrong label can land, but as written the LAND will stop there unless the Lead edits the date before the final build. State that edit as an explicit step (or have `--final` take the date), and recheck it at the final SHA.
- **N3. `reports/cp17c/inputs.json` also records the five modules' pre-PRES-5 hashes** (as files of CP-17c's private scratch tree). Nothing compares that record with the working tree, the freeze manifest names none of them, and the suite is green, so A1's freeze is untouched; the packet's O34 entry does not mention it.

### Product recommendations

- **R1.** GFS attribution still reads "The v3 research model's weather data" on the page and in the README; v4–v6 and the live product read GFS too (editorial R11, not taken).
- **R2.** The README's CP-3 table row 1 now says "How the product works … a forecast replay" under a line that dates the table to v1's release; and row 2's links reach the Space root. Either date the whole section or link `/history/`.
- **R3.** `src/cp18/live_claims.py` (CP-18c's path, landed by CP-18b) names the product "A1 · DDNN-2 alone", while O30 says the Space uses "v6 · DDNN-2 alone". After both publications, the public checks (§8.5, and A12's useful check in §8.6) should compare the Space's served name and status with the report's.
- **R4.** `v6.fresh.terms` says "The intervals come from a 7-day block bootstrap with 10,000 draws"; in the protocol (§6) that bootstrap gives the test's one-sided p-values. "The p-values come from …" would match it.
- **R5.** The local release records ran over `file:` (PRES-2–4's ran over HTTP, as runbook §9 asks), so browser-made requests were not observable there. My HTTP run (command 32) closes that for this candidate: 33 requests, all `GET /index.html`, no favicon or other asset, nothing failed. Run the release record over HTTP at the final SHA.
- **R6.** The repository's v1 Space cards (`space/README.md` line 22, `space-wasm/README.md` line 23; outside PRES-5's allowed paths and not deployed by it) still say "How the released model works, topic by topic: [the report's product documentation](…#product)", and `#product` now documents v6. If any later bundle reuses them, regenerate them first.

### Not graded

- A8's product-first order (packet §10.3 (1)): an applicability question for the Orchestrator; consistent with O27.

### Comparison with the earlier reviews (read after these findings)

- **The editorial review's V5 is G1.** Its location list included this sentence; the repair covered the table's lead-in and line 538, and the packet records V5 closed. That closure is not supported for line 452/454.
- **Integration review 1:** its acceptance test is met (section D). Its F3 disposition now has a check but still no setting step (N2). Its notes on the GFS attribution and the CP-3 table recur as R1 and R2. It did not raise line 454 or the W-numbering.
- **The fresh reader:** answers 1–5 agree with the records I re-derived; its observation on "what is actually in production" bears on G1's subject on the README, not on the report.
- **Editorial recommendations not taken** (R6, R8–R13, R15, R18) remain recommendations; R9 is N2, R11 is R1.

## On FAIL only

- **Single largest meaningful gap:** the README's CP-3 section still states, in the present tense, that "The Space … runs the champion's own nine boosters … in the browser" and that "The app alone is at" the Space's root, immediately under the generated line saying the Space's root now runs v6. The editorial review named this sentence in V5, and the packet records V5 as repaired; it was not, and the guard the packet cites for it (its "W53") does not exist.
- **Exact next acceptance test:** at the next candidate, `README.md` (regenerated by `scripts/rebuild_presentation.py`, `git status` empty afterwards) contains no sentence saying that the Space, its root or its app runs the champion, its boosters or v1 now: the CP-3 paragraph names v1's demo under the Space's History or is dated to v1's release. A test in `tests/test_50_pres5_publication.py` enforces this on the README and the page, with a negative control that re-inserts the current line 454 and is caught. Packet §3, §5b and §10.1 describe W49–W53 exactly as `pres5-claims.md` and `WITHHELD_PATTERNS` define them, and claim only the negative controls that exist. With it (not deciding): packet §8 or §6 states who sets `EVIDENCE_TAGS["evidence/pres-5"]` to the evidence tip's date, and when (N2).
