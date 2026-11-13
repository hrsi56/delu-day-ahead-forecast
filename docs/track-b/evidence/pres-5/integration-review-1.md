# Verdict — PRES-5 — Integration — FAIL

- Candidate SHA: `b866e996f4fa2b0026cc14097de3833f92b88ade` (`gauntlet/pres-5`; base `main` = `3c8e158c9895f5b3fed13db794b0ddd5fb80c56f`)
- Plan / version / bar:
  - the brief `docs/track-b/evidence/pres-5/issued-brief.md`, SHA-256 `9eb2a58433f41739fc22744854c4c55b099cc05ca729b677e9b3b5ccef87ebc3` (it controls);
  - the publication anchor `docs/PUBLISH_RULES.md` revision 1.5, SHA-256 `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`, in full;
  - the research constraint anchor `capstone_v21.md` v21-r20, SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`, §24.14 (section 115 lines, 7,426 bytes, SHA-256 `5d38de24b3c68ec01e2f5c4e6eaf368c253485107549fc2d85c3c71ccf2f5349`).
- Verbatim bar excerpt (extracted with `bar.py bar … --at b866e996… --quote`; identical to the brief's; the excerpt is the citation, any line number is a courtesy and is non-binding):

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

- Worktree clean before and after: yes. `git -C …/critic-1 status --porcelain` printed nothing at the start, after every
  generator run and after the test suite; `HEAD` stayed `b866e996f4fa2b0026cc14097de3833f92b88ade`. Byproducts were
  ignored files only (`.venv/`, `app/public/`). The review was paused once by a usage limit (2026-11-12 about 21:10 to
  2026-11-13 01:50, Asia/Jerusalem) and resumed on the same worktree, unchanged.
- Isolation: cooperative and procedural. No Builder checkout, uncommitted diff or Builder conversation was read; the
  Lead's worktree was used only to run `critic-brief`. No Git write of any kind and no network use: the secret scan and
  every check below ran locally, and `uv` ran offline.
- Reviewer: the Integration Critic. I authored none of PRES-5. I did not open the Claude memory directory,
  `progress.md`, any syllabus, Track A or C material, or `docs/track-b/orchestrator-role.md`. No credential value was
  read, printed or typed.

## Commands actually run

All in `/Users/djourno/Downloads/PJM/.local/worktrees/pres-5/critic-1` (abbreviated `W`), with
`MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 UV_OFFLINE=1` exported. Logs are kept outside the worktree under
`/Users/djourno/Downloads/PJM/.local/artifacts/pres-5/critic-1/logs/`.

| # | Command | Exit | Observed output |
|---|---|---|---|
| 1 | `git -C W status --porcelain`; `git -C W rev-parse HEAD 3c8e158c main` | 0 | nothing; `b866e996…88ade`; `3c8e158c…c56f` twice (`main` is the base) |
| 2 | `shasum -a 256` on `capstone_v21.md`, `docs/PUBLISH_RULES.md`, the brief, `owner-decisions-2026-11-05.md` and the brief's 18 execution inputs | 0 | every value equals the brief's (`80341681…`, `1bc0c523…`, `9eb2a584…`, `4daa5617…`, and all 18 rows of its inputs table); `3c8e158c:docs/index.html` is `54708134…37ce`, 1,996,267 bytes; `3c8e158c:README.md` is `c816972a…315fc` |
| 3 | `git show main:scripts/bar.py \| python3 -I - bar capstone_v21.md "### 24.14 Publishing and going live before 4.7T (v21-r20)" --at b866e996… --quote` | 0 | stderr: `sha256 80341681…30e6; section 115 lines, 7426 bytes, sha256 5d38de24…f5349`; the quoted text equals the brief's excerpt byte for byte |
| 4 | `uv run python -m delu_forecast.final_candidate --check` | 0 | `{"identical_to_committed": {"metrics.csv": true, "parity.json": true, "preview-day.csv": true, "ratio-intervals.csv": true, "summary.json": true, "uncertainty.csv": true}}` |
| 5 | `uv run python -m delu_forecast.compact_figures --check` | 0 | `{"pixel_identical": true, "problems": []}` |
| 6 | my own script, `.venv/bin/python -I <scratchpad>/recompute_v6.py W`, which reads the parquet rows and recomputes MAE and seven-quantile WIS per fold and the equal-fold ratios without the project's scoring code | 0 | v5's keys 10,747 over 448 days (folds 2,160/2,159/2,112/2,160/2,156); A1 missing keys 0, day mismatches 0, quantile crossings 0; B0 on all 10,747 keys with the same `y_true`; A1 S_MAE 0.4928063413559065, S_WIS 0.4373719802748803; v5 0.5223212760431432, 0.4936627890811673 (= CP-24's committed equal-fold row); A1/v5 − 1 = −5.651% and −11.403%; A1/B0 − 1 = −50.72% and −56.26%; per-fold MAE 4.5178, 7.0506, 43.1925, 13.0924, 13.3715; max difference from `reports/pres5/a1-in-v5/metrics.csv` 7e-15; A1's stored forecasts end 2026-09-06 |
| 7 | `uv run python scripts/build_pages.py`, then `git status --porcelain` | 0 | `wrote …/docs/index.html (1,847,871 bytes)` and `reports/cp3/pages_build.json`; status empty (the page and build record are reproducible) |
| 8 | `uv run python scripts/readme_research.py`, then `git status --porcelain` | 0 | `regenerated the glance and generations blocks`; status empty |
| 9 | `uv run python scripts/mlflow_export.py --check` | 0 | `the committed export is current` |
| 10 | `uv run python scripts/mlflow_export.py --diff-against 3c8e158c` | 0 | `runs 44 -> 105` (the 61 `cp26…` and `cp28…` keys added); `identity changes on 0 runs; substantive changes: none; only_identity=True` |
| 11 | `uv run python scripts/lint_publication.py` | 0 | `page: 0 finding(s)`, `readme: 0`, `templates: 0`, `PASS` |
| 12 | `shasum -a 256 docs/index.html; wc -c docs/index.html` | 0 | `2fcb53acd9adb086f9add95aefa3d7c20843cd6e4ad3c2b00ac790da6270d9ca`, 1,847,871 bytes (= `1d0f453e:docs/index.html`) |
| 13 | a Python cross-check of the O34 record: each recorded copy's SHA-256 against `reports/rebaseline/harness-log.json` `landed_code`, its git blob against `git rev-parse 61658c7:<path>`, and its bytes against `git show 3c8e158c:<path>` | 0 | `True` on all four checks for all five modules; the changed files pinned in `landed_code` are exactly those five |
| 14 | the SHA-256 and git blob of every file the candidate modifies, at `3c8e158c`, searched with `git grep -F -f` across the candidate tree | 0 | old hashes appear in `reports/rebaseline/harness-log.json` (O34), `reports/cp17c/inputs.json` (the five presentation modules), `reports/ddnn2/base-tree.json` (`scripts/cp3_readme.py`, `tests/test_30…`), PRES-4's records and their preserved copies. `cp17c/inputs.json` is the scratch repository's file list, read by `cp17c.records` only for `references`; `docs/track-b/evidence/cp-17c/freeze-manifest.json` names none of the changed paths; `base-tree.json`'s consumer `tests/cp24/test_draft_export.py` skips by design when `scripts/mlflow_export.py` changed |
| 15 | `git diff --name-only 3c8e158c b866e996` filtered for `src/cp*`, `space-product`, `live/`, `.github`, `docs/PUBLISH_RULES.md`, `capstone*`, `AGENTS.md`, `CLAUDE.md`, the role files, `gauntlet-templates.md`, `rule-inventory.md`, `cp-0-defects.md`, `backup-register.md`, `exposure-ledger*`, `scripts/build_product_space.py`, `tests/cp18c`, `reports/cp18c`, `docs/track-b/evidence/cp-18c`, `pyproject.toml`, `uv.lock`, `.claude` | 0 | no path |
| 16 | `printf 'refs/heads/gauntlet/pres-5 b866e996… refs/heads/gauntlet/pres-5 0000…\n' \| python3 -I scripts/secret_guard.py pre-push origin "$(git remote get-url origin)"` | 0 | no `BLOCKED` line; 11 outgoing commits scanned (`git rev-list b866e996 --not --remotes=origin`) |
| 17 | `git -C W --no-pager diff --cached --quiet 3c8e158c --pathspec-from-file=<file>` and `git -C W --no-pager diff --quiet 3c8e158c HEAD --pathspec-from-file=<file>` (read-only), to test packet §8.2's "(main moved)" command | 129, 129 | `usage: git diff [<options>] …`: git 2.50.1 (Apple Git-155) has no `--pathspec-from-file` for `diff` |
| 18 | `HOMEBREW_NO_AUTO_UPDATE=1 brew list --pinned`; `node --version` | 0 | `node`; `v26.7.0` |
| 19 | `uv run pytest -q -p no:cacheprovider` (the whole suite, Python 3.13.15, 20 min 28 s) | 1 | `5 failed, 3221 passed, 10 skipped, 12 errors`. Two failures are CP-18a's push tests (`test_dry_run.py::test_a_real_dry_run_then_the_fallback_finds_the_day_claimed`, `test_forced.py::test_each_cause_is_forced_and_recorded`): `publication-guard: BLOCKED - … reports/cp3/pages_build.json is a non-final build record (final: false)`, by design until the `--final` build. The other 3 failures and 12 errors are all `tests/test_22_wasm_equivalence.py`: `app/public/ is absent … make wasm-payload`, the CI step that runs before pytest |
| 19a | `uv run python scripts/build_wasm_payload.py` (the `make wasm-payload` recipe; writes ignored `app/public/`), then `uv run pytest -q -p no:cacheprovider tests/test_22_wasm_equivalence.py tests/test_50_pres5_publication.py`, then `git status --porcelain` | 0, 0, 0 | payload built (fixture 54 days / 1,296 rows); `48 passed`; status empty. With the payload, the only failures left are CP-18a's two, as the packet's §7 states |
| 20 | `git show main:scripts/bar.py \| python3 -I - check <this verdict> --source capstone_v21.md@b866e996f4fa2b0026cc14097de3833f92b88ade` | 0 | `ok: lines 10–124 (7425 bytes) appear in capstone_v21.md@b866e996f4fa` |
| 21 | `git -C W status --porcelain`; `git -C W rev-parse HEAD`, at the end | 0 | nothing; `b866e996f4fa2b0026cc14097de3833f92b88ade` |

## Evidence actually inspected

- **The brief** in full; **the bar**: `capstone_v21.md` §24.14 (via `bar.py`); `docs/PUBLISH_RULES.md` §§1–16 in full,
  with `publication-standard-v1.md` §4 (numbers and words); the packet template's headings.
- **The packet** `docs/track-b/evidence/pres-5/publication-packet.md`, all 665 lines (§§1–10).
- **The diff** `3c8e158c..b866e996` (61 files): the full diffs of `publication_lint.py`, tests 24, 29, 30, 34–39, 43, 45,
  49, the two CP-26 tests and `tests/pres5_landed_code.py`; `src/delu_forecast/final_candidate.py` in full; the opening
  branch of `scripts/build_pages.py` (lines 1700–1780), `Audit`/`EVIDENCE_TAGS`, `research_claims.py`'s PRES-5 blocks
  (lines 825–850), `derived.display`; the README diff in full; the O34 record
  `docs/track-b/evidence/pres-5/cp26-landed-presentation-code/manifest.json`; `test_50`'s O34 tests.
- **Records:** `reports/pres5/a1-in-v5/{metrics.csv, ratio-intervals.csv, uncertainty.csv, summary.json}`;
  `reports/cp28/owner-summary.json` (A1's ratios to the control and their intervals, Holm, `passes_all_four`),
  `reports/cp28/report.md`, `reports/cp28/forecast/manifest.json` (it pins `hourly.parquet` `f5cb02a1…`);
  `reports/cp18b/acceptance.json` (its cold-start checks) and `docs/track-b/cp-18b-landing-2026-11-05.md`;
  `docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md` (§§1, 2, 4–8, the wording at its end);
  `reports/presentation/mlflow-export/{cp26,cp28,manifest}.json` (run names, kinds, statuses, the experiment note,
  the metric-unit additions) and `cp24.json`/`cp15.json` for the naming convention;
  `reports/presentation/release-checks/pres-5-export-diff.json`, `pres-5-local-release.json` (`passed`, placements in
  both engines and every width, discovery) and `pres-5-pre-final-2-prerelease.json` (`head` `1d0f453e`, its three
  unexpected steps); `reports/cp3/pages_build.json`.
- **The rendered page** `docs/index.html` (2,107 lines of extracted text, read from the opening through the product
  documentation, the comparison, the every-day panel, the transitions, v6's chapter, the freeze and 4.7T, v1's chapter,
  the archive's lead-in, the planned list, the system section, reproduction, tracking and attribution); every date after
  2026-09-06 on the page, by context; every `A1` on the page, by context.
- **The reviews**, read after my findings were formed: `editorial.md` (V1–V12, R1–R18, the A8 note) and
  `fresh-reader.md` (answers 1–6 and the confusions).

## Checklist verdict

### The brief's observable outcome

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | A1 in v5's comparison, on v5's own population, from CP-28's stored forecasts; other rows CP-24's; paired comparisons against v5 and B0 at the rule's levels; never adopted; every value derived | PASS | Commands 4 and 6: 10,747 of 10,747 hours, native forecasts on all 448 days, no fallback; my independent recomputation equals the committed rows to 7e-15; v5's and B0's recomputed scores equal CP-24's (`parity.json` 0.0). The information-set differences and the coverage are stated on the reading path (`v6.caveat.information`, `v6.method.*`). The page says "v5's adoption rule was not re-run, and it adopts nothing here" |
| 2 | CP-26 on every development day, beside and never pooled with the five periods | PASS, with finding F4 | `#everyday`: 2,068 days, 2020-12-29 to 2026-09-06, "never pooled with the five periods above · development, post-selection"; v5 − v4 −0.66% [−1.41%, +0.94%] and −0.50% [−1.20%, +1.03%] (`cp26.audit.v5-v4.*`) display as whole percents; GFS +6 h +13.99% [+10.3%, +16.1%] and +15.46% [+12.1%, +17.6%] display as +14% [+10%, +16%] and +15% [+12%, +18%] |
| 3 | CP-28's selection: arms, rule, result, why A1 | PASS | The arms table matches `owner-summary.json`: A1 −6.90% [−9.07%, −5.14%] and −10.93% [−12.85%, −8.96%] against v5; all seven pass all four analyses; A1's interval error 9.68 against A6's 10.13; Holm-adjusted p 0.0042; the conditional Holm control is disclosed |
| 4 | The freeze and 4.7T's registered terms, as a pre-registration | PASS | `#v6-freeze` and `#v6-fresh-test` agree with the protocol: window 2026-09-07 to 2026-12-05, control v5, reference B0, references v3/v4/v1 reported only, the 0.995 margin, compound p ≤ 0.05, 7-day blocks with 10,000 replicates, ≥ 60 of 90 dates, no runner-up, the window spent; identity `720fc581`; the issuing host; what a pass and a fail mean |
| 5 | The product: the opening pairs v6 with the product; the Space linked and described; v1 at `/history/`; no live number and nothing after 2026-09-06 | PASS for these points (the §7.1 metadata beside the action fails: F1) | The opening's status pair "Live product · v6 · DDNN-2 alone" and "Final candidate · pending 4.7T"; "The Space runs v6 · DDNN-2 alone daily, frozen, … prospective evaluation in progress"; v1's historical demo at `…static.hf.space/history/`. Every later date on the page is a decision, freeze, label or 4.7T term date; the preview is 2026-04-07; the report reads no `live/` or CP-18c path |
| 6 | The model identity under §4 and O30 | PASS (note F5) | "v6 · DDNN-2 alone", a generation; "A1 in the frozen records" beside the identity; the six arms named without codes, "Not selected". MLflow names carry the code in parentheses, as every earlier run does (`cp24.json`, `cp15.json`) |
| 7 | MLflow: prepared exactly as authorized (the upload follows a PASS) | PASS as prepared | Commands 9–10: the export is current; 44 → 105, no identity or substantive change; the packet's `--authorized-runs` list is exactly the 61 added keys (set equality checked), `--authorized-experiment-tags mlflow.note.content` only; `mlflow_publish.py` (unchanged) refuses before the first write outside them; precheck first |
| 8 | The page budget | PASS | 1,847,871 bytes ≤ 2,000,000, by the pixel-identical re-encoding (command 5) |
| 9 | The independent check passes at the candidate | **FAIL** | This verdict: F1 (and F2, F3, F4) |
| 10 | The packet's §8: exact payloads and ready-to-run commands for the LAND, the push, the public checks and A12 | **FAIL** (F2) | The unmoved-`main` path, the push, the secret scan, the guard, the receipt and the browser commands use flags the scripts define. The "(main moved)" variant, the likely one with CP-18c landing beside PRES-5, exits 129 (command 17). It fails closed: the check prints nothing and the commit is not reached |

### The complete authoritative checkpoint bar

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| B1 | PUBLISH_RULES §1.1–§1.3: authority, the four identities, categories | PASS | Hashes pinned and verified (command 2); the generation (v6, final candidate), the product status and the artifact identities are kept apart |
| B2 | §2 reader contract, A1 (metrics named), A2 (measured placements) | PASS | Each headline percentage is followed by "in point error"/"in interval error", with "as shares of v5's, with descriptive 95% intervals"; terms directly beneath. The release record (both engines, every width): headline bottom 800.6/801.3 px at 1440×900 and 628.6/628.7 px at 390×844; finding 1,672.6/1,673.3 px against 1,744 and 2,394.5/2,394.3 px against 2,420; the product line beside the action, outside disclosures |
| B3 | §3.1 evidence classes; W1–W53 | PASS | "Development · post-selection" on every v6, CP-26 and CP-28 number; nothing live, prospective or 4.7T's; the selection's conditionality and the earlier DDNN-2 result disclosed on the reading path ("after DDNN-2 alone had already scored best there") |
| B4 | §3.2 scores, comparisons, uncertainty | PASS except F4 | The verdict with its rule, date and N; changes as shares of the comparator with 95% intervals from the checkpoints' own draws (and 97.5%); absolute MAE with the stress period apart; one population per comparison. F4: "v5 and v4 are level there" asserts equivalence from a null result |
| B5 | §3.3 counting | PASS | CP-28's N = 7 is its rule's; the 13 chart rows are distinguished from the 25-policy target census; kinds distinct |
| B6 | §3.4 provenance and formatting | PASS (the typed startup size is part of F1) | Command 11; whole percents, one decimal EUR/MWh, four significant figures; every research number a record |
| B7 | §4 registry, transitions, branches; A3; A10 | PASS; A10 not applicable | One registry; v6 a generation with a dated final-candidate status and no adoption event; "From v5 to v6" with predecessor, change, comparator, result, limits, decision and route; CP-28's six arms and CP-26's routes as study arms |
| B8 | §5 page architecture; A4 | PASS | A4's order; "How the product works" documents v6 with the twelve subjects (O26/O29) |
| B9 | §5 / A8 product-first order | Not graded | Open item 1 with a proposed ruling. The Lead's reading (A8's trigger is the Owner's final-product designation, which decision 21 ties to 4.7T, while v1 stays released) is defensible; it is the Orchestrator's to rule |
| B10 | §5.1 the twelve subjects; §5.2 grammar and budget | PASS | Each subject supported or "not evaluated in this report" with a route; v6's chapter fills every slot (`test_38`); budget as outcome 8 |
| B11 | §6 charts and A5 discovery | PASS | v6's main chart with direct labels and both levels; the comparison with v6 first; 48 routes in each engine from the closed page (release record `discovery`, all `passed`) |
| B12 | §7.1 the product contract beside the action | **FAIL** (F1) | Size only; no measured cold-start time, device/browser, date or last verification |
| B13 | §7.2 / A7 live presentation | Not applicable to the report | The report shows no live panel or number; `test_24`'s wall admits only the name, the status and "prospective evaluation in progress" |
| B14 | §7.3 / A9 the final-product Space | Not this block's surface | CP-18c's |
| B15 | §8 surfaces and evidence links | PASS, with F3 open | Report, README and MLflow agree on identity and status (`test_39`); audit links labelled by type and date; F3: `evidence/pres-5`'s label date is hard-coded and stale |
| B16 | §9 browser and accessibility matrix | PASS (on the record) | `pres-5-local-release.json` `passed` true: Chrome 157.0.8103.51 and WebKit 26.6, every width, accessibility trees, keyboard, touch, contrast, zoom and reflow, no console error or failed request. Not re-run by me (optional in the brief); the record names `docs/index.html` but not its hash |
| B17 | §10.1–§10.2 independence; the fresh reader | PASS | `editorial.md` and `fresh-reader.md`: independent authors; the six questions unchanged; closed-state screens; answers 1–5 agree with the records |
| B18 | §10.3 / A6, §10.5 / A12 | Prepared (after deployment) | Packet §8.5–§8.6 |
| B19 | §11 packet and order; no non-final build on `main` | PASS | Build → editorial → fresh reader → this check; `pages_build.json` `final: false` and the guard refuses it until `--final` |
| B20 | §12 baseline coverage: invariant 10 (2026-09-06), 13 (`pyproject.toml`, `uv.lock` unchanged), 14, 24 (the archive) | PASS | No research number on a later day; neither dependency file in the diff; the archive equals `af0abb0`'s with the figures put back (`test_38`) |
| B21 | §13 acceptance record | PASS except its Product row (F1) | Packet §9.2 |
| B22 | §14 pending triggers; A11 | PASS | "Before final-candidate test" decided by decisions 20–21 and O27/O30 |
| B23 | The runbook, every applicable touchpoint | PASS | Packet §9.3, spot-checked in code: `_ENTRIES`, `CHECKPOINTS`, `EVIDENCE_TAGS`, `RULES`, `COMPARISON_ORDER`, `CLAIM_MAPS`, `PRES5_EXPORTS`, the tests |
| B24 | The packet template, every section | PASS | §§1–8 with 5a–5d all present, plus §§9–10 |
| B25 | r20 §24.14 | PASS | Research numbers on development days only (item 6, P1); no live record read (item 2); A1's freeze untouched (no `src/cp17*` change, the freeze manifest names no changed path); 4.7T's terms unchanged and quoted; "final candidate · pending 4.7T" (O13); "prospective evaluation in progress"; development displays end by 2026-09-06 (item 5) |

### The task-specific extract, the constraints, the authorized actions and the rulings

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| T1 | CP-18c's paths never touched | PASS | Command 15 |
| T2 | The Space's address | PASS | `https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast` on the page and the README |
| T3 | The red line for research | PASS | As B25 |
| T4 | The ceilings and their ledger | Not in the candidate | Due in the return ("Name the machine-hours used") |
| T5 | Presentation tokens (O16) | PASS | v6's `#18181B` hexagon, disclosed as the Owner's choice |
| T6 | Tests: the new `test_50` and the changed tests 24, 29, 30, 34–39, 43, 45, 49 and CP-26's two | PASS, with one weakening noted | Commands 19–19a: green apart from CP-18a's two by-design refusals. The changed assertions follow PRES-5's state and keep their negative controls (moved to v7, v6's rows or new controls). Two loosen a guard: `test_43`'s F03 accepts the incomplete startup line (F1), and `test_37` accepts the page-wide "A1" allowance (F5) |
| C1 | Homebrew's `node` pinned | PASS | Command 18 |
| C2 | Credentials | PASS | Command 16; no credential read in the presentation code |
| C3 | Allowed paths | PASS, with O34's exception | Every changed path is the page, README, their build and tests, the claim maps, the registry and its drafts (`mlflow_export.py` is runbook §2.17's touchpoint), `reports/pres5/` or `docs/track-b/evidence/pres-5/`, except the two CP-26 tests and their helper (O34) |
| C4 | No earlier evidence binds an edited file's bytes | PASS | Command 14: CP-26's harness log handled by O34; the other pins are historical records not compared with the working tree |
| C5 | Owner-facing Git commands non-interactive | PASS | `--no-pager`, `commit -F`, no editor |
| A | The MLflow upload: prepared as authorized; nothing else | PASS | As outcome 7; the candidate pushes, tags and uploads nothing |
| O25 | The archive's seven figures pixel-identical | PASS | Command 5; `test_38` puts the originals back and matches `af0abb0` |
| O26/O29 | "How the product works" documents v6; never implies the Space runs v1 now | PASS | The product section names v6; v1's chapter links "v1's original report" and its demo "under the Space's History"; the archive's lead-in note says the root now runs the live product |
| O27 | The hero and v1's status | PASS | v6 "Final candidate · pending 4.7T" with CP-28's verdict and the badge; v1 "Released · September 2026", "the last released generation" |
| O30 | The public name, generation, frozen label, six arms "not selected" without codes | PASS (F5) | As outcome 6 |
| O34 | CP-26's two landed-code tests, under its four conditions | PASS | Command 13: the five modules checked against recorded bytes bound by SHA-256 and git blob (= the log and `61658c7`); every other landed file still against the working tree; negative controls in `test_50` (a changed copy, a copy re-hashed to differ from the log, another landed file changed); the two new modules named outside the landed set. One assertion changed in each test |

## Findings (PUBLISH_RULES §10.1)

### Existing-rule violations

**F1 (medium-high; decides this verdict). The live product's startup metadata beside its action is incomplete.**
- **Clause:** PUBLISH_RULES 1.5 §7.1: "Beside the demo action, outside a disclosure, show download size, measured
  cold-start time, device/browser/date and last verification date." Also §12's surviving plan detail "startup metadata
  beside the action (§7.11)" and §13's Product row ("startup metadata, cold start"). The packet's §9.1 itself marks §7.1
  "yes, changed".
- **Observation:** beside "Open the live product", `p.startup[data-block="product.live.startup"]` reads only "It opens
  with about 0.55 MB, measured on development data; the training window loads on request." It has no measured start
  time, no device or browser, no measurement date and no last-verified date, and it does not say that they are missing.
  The size is typed in the template as a structural numeral (`{s:size:0.55}`), not bound to a record. v1's line, which
  this branch replaces, bound all five fields to records.
- **Why it is not a timing impossibility:** a committed measurement of the product's cold start exists:
  `reports/cp18b/acceptance.json`, "demo: fresh anonymous cold start reaches the ready state", 1.86 s in Chromium and in
  WebKit, with its machine and dates, beside the first-visit size CP-18b recorded (551,515 bytes,
  `docs/track-b/cp-18b-landing-2026-11-05.md`). The size line already relies on CP-18b's measurement.
- **History:** the editorial review found it (V4); it was not repaired. The packet carries it as open item §10.3 (4)
  with a proposed deferral to the next publication, and `test_43`'s F03 test was changed to accept the incomplete line
  when a final candidate exists. A proposed ruling is not a repair, and §1.1 does not let a brief or review relax the
  standard.
- **Impact:** the published opening would carry an incomplete product contract until the next publication (4.7T's, in
  December).

**F2 (medium). Packet §8.2's "(main moved)" LAND check cannot run.**
- **Clause:** the brief's outcome 10 ("ready-to-run commands" for the landing); PUBLISH_RULES §11 (the runbook's exact
  commands).
- **Observation:** `git --no-pager diff --cached --quiet <evidence_tip_sha> --pathspec-from-file=…` exits 129 with
  `usage: git diff …` on this Mac's git 2.50.1 (command 17): `git diff` has no `--pathspec-from-file`. This is the
  variant the Orchestrator needs if CP-18c lands first, which the packet expects as possible.
- **Impact:** it fails closed (no marker line, no commit), so nothing wrong is published, but the landing stalls at that
  step.

**F3 (medium-low). The `evidence/pres-5` audit label carries a stale, unchecked date.**
- **Clause:** PUBLISH_RULES §8 ("Audit-grade links belong in the evidence row, labelled by type and freeze date");
  Standard v1 §7.
- **Observation:** `registry.py` `EVIDENCE_TAGS["evidence/pres-5"] = ("", "2026-11-06")` renders "The final candidate's
  raw CSV rows, frozen 2026-11-06" on the page and in the README. The tag will be created on an evidence tip dated
  2026-11-12 or later; the rows were committed on 2026-11-05. Nothing checks the date: no test, no `--final` check, and
  no step in packet §6 or §8 (the only mention is R9's disposition, "set at the final build").
- **Impact:** a wrong freeze date on an audit link unless someone remembers to change it.

**F4 (low). The every-day panel reads a null result as equivalence.**
- **Clause:** PUBLISH_RULES §3.2: "A null result does not demonstrate equivalence."
- **Observation:** the panel's heading says "v5 and v4 are level there", from −1% [−1%, +1%] on both scores
  (−0.66% [−1.41%, +0.94%] and −0.50% [−1.20%, +1.03%]). C603, its claim, says only that the five-period gain does not
  carry over.
- **Repair:** for example "v5 shows no demonstrated difference from v4 there".

### Packet accuracy and product recommendations (not violations)

- **F5. The lint's allowance for "A1" is page-wide, not "beside v6's identity" as the packet says (§2, §10.2).**
  `publication_lint.code_denylist()` drops every frozen label from the denylist, so "A1" anywhere on the reading path no
  longer produces a finding, CP-15's normalized LEAR included. Today every reading-path "A1" sits beside v6's identity
  (checked by context), so nothing is violated. Scope the allowance (for example, admit "A1" only in "A1 in the frozen
  records" and "arm A1, now v6"), or correct the packet's wording.
- The GFS attribution still reads "The v3 research model's weather data"; v4–v6 and the live product read GFS too
  (editorial R11).
- The README's CP-3 table is now introduced as describing "the surfaces at v1's release", while its first row was
  rewritten to the present ("How the product works … a forecast replay").
- The overview's value table gives the code "A1" to two policies (v6 and normalized LEAR) (editorial R6).
- `pres-5-local-release.json` records its page as `docs/index.html` without its SHA-256; the packet's claim that it
  measured `2fcb53ac…` rests on timing and the commit, not on the record.

### Not graded

- A8's product-first order (packet §10.3 item 1): an open applicability question for the Orchestrator.

### Comparison with the earlier reviews (read after these findings)

- The editorial review's V4 is F1. Its fix accepted a deferral; I do not, because the measurement already exists in a
  committed record and §10.4 allows no PASS while a violation remains.
- The editorial review's R9 is F3. Its disposition ("set at the final build") has no step or check behind it.
- F2 and F4 are new. Neither earlier review ran the packet's commands or graded the every-day heading against §3.2.
- The fresh reader's confusion on "what is actually in production" bears on F1's surroundings, not on its rule.

## On FAIL only

- **Single largest meaningful gap:** the live product's startup line beside "Open the live product" omits the measured
  cold-start time, device/browser, measurement date and last-verified date that PUBLISH_RULES §7.1 requires, although
  CP-18b's committed `acceptance.json` already holds a measured cold start, and its size is typed rather than bound to a
  record.
- **Exact next acceptance test:** at the next candidate, `p.startup[data-block="product.live.startup"]`, beside the
  primary action and outside any disclosure, renders the download size, the measured cold-start time, the browser and
  machine, the measurement date and the last-verified date, each bound to a committed record (CP-18b's
  `acceptance.json` and landing record, labelled as that reviewed bundle served locally, or a new release-check record
  of the public Space). `tests/test_43_publish_rules_migration.py::test_f03_the_measured_start_is_beside_the_action_outside_any_disclosure`
  asserts all five in the final-candidate branch, with a negative control that removes one. With it: packet §8.2's
  "(main moved)" check rewritten so that it runs on git 2.50.1 (shown by a dry run on a scratch index), a check or
  explicit step that sets and verifies `EVIDENCE_TAGS["evidence/pres-5"]`'s date against the evidence tip, and F4's
  wording. If the Owner instead decides that §7.1's timing may wait for the public Space, that decision, cited in the
  packet, replaces the first part.
