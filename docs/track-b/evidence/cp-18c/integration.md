# Verdict — CP-18c — Integration — PASS

- Candidate SHA: `3513057858b08726dcb5752c64e7e8ca441a9567` (tree `3096ed2751d9ff071d01eb0e2c9097071f47f7d9`), on
  `gauntlet/cp-18c`, base `main` = `3c8e158c9895f5b3fed13db794b0ddd5fb80c56f` (merge-base confirmed; 42 commits; the
  first, `5ddbd7a4`, packages the brief byte for byte, `ed5ddeb1…` equal to `.local/artifacts/cp-18c/issued-brief.md`).
- Plan / version / bar: `capstone_v21.md`, v21-r20 (SHA-256 `80341681e4473a9315c1102dc74e3b3caec6f924b4165ebba6088bc15bc330e6`,
  recomputed in the worktree), §24.14 "Publishing and going live before 4.7T (v21-r20)"; with the brief's further
  quoted bar (§24.13's four parts, §24.12's "Open", §19.4, `docs/PUBLISH_RULES.md` 1.5 §7.2, §7.3 (A9), A6; PUBLISH_RULES
  SHA-256 `1bc0c52351656c5a499291bf15ccb82b0ae8b4e6475d1879b0a4d307daaef94e`, recomputed).
- Worktree clean before and after: yes. `git -C …/critic-4 status --porcelain` printed nothing at the start, after every
  step that ran inside it, and at the end; `HEAD` stayed `3513057858b08726dcb5752c64e7e8ca441a9567`.
- Isolation: cooperative (procedural). No Git write of any kind; nothing written inside the worktree; scratch under
  `.local/tmp/cp-18c/critic/c4/`; no credential value read or printed; network requests only the anonymous HTTPS reads
  of the public Space that the assignment names.
- Verbatim bar excerpt (the excerpt is the citation; any line number is a courtesy and is non-binding):

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

All variables below: `P=/Users/djourno/Downloads/PJM`, `W=$P/.local/worktrees/cp-18c/critic-4`,
`S=$P/.local/tmp/cp-18c/critic/c4`. Every Python shell exported `MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1` and
`OPENBLAS_NUM_THREADS=VECLIB_MAXIMUM_THREADS=OMP_NUM_THREADS=MKL_NUM_THREADS=NUMEXPR_NUM_THREADS=1`, and
`PYTHONDONTWRITEBYTECODE=1` for runs from the worktree.

## Commands actually run

| # | Command | Exit | Observed output |
|---|---|---|---|
| 0 | `git show main:scripts/gauntlet.py \| python3 -I - critic-brief cp-18c` | 0 | this assignment |
| 0a | `git -C $W status --porcelain`; `git -C $W rev-parse HEAD`; `git merge-base <sha> main`; `git rev-parse gauntlet/cp-18c` | 0 | empty; `3513057858…`; `3c8e158c…`; `3513057858…` |
| 1 | `git show main:scripts/bar.py \| python3 -I - check $W/docs/track-b/evidence/cp-18c/issued-brief.md --source capstone_v21.md@3513057858… --source docs/PUBLISH_RULES.md@3513057858…` | 0 | ten lines, every one `ok`: brief lines 178–292 (7425 bytes), 296–368, 372–410, 414–430, 434–463, 467–519, 523–530 in `capstone_v21.md@3513057858b0`; 534–602, 606–657, 661–675 in `docs/PUBLISH_RULES.md@3513057858b0` |
| 1a | `shasum -a 256` of the brief, `capstone_v21.md`, `docs/PUBLISH_RULES.md` in `$W` | 0 | `ed5ddeb1…`, `80341681…`, `1bc0c523…`, as the brief names them |
| 2 | `cd $W && CP17_PROJECT_ROOT=$P PYTHONPATH=src $P/.venv/bin/python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json` | 0 | exactly `verified` |
| 3 | `git -C $W diff --stat 3c8e158c HEAD -- src/cp17 src/cp17c src/cp25 src/delu_forecast src/cp15 src/cp16 src/cp20 src/cp21 src/cp24 src/cp26 src/cp28 space-wasm space data reports/development-inputs pyproject.toml uv.lock docs/index.html README.md docs/PUBLISH_RULES.md capstone_v21.md AGENTS.md docs/track-b/exposure-ledger.md docs/track-b/backup-register.md` | 0 | empty |
| 3a | `git diff --name-status 3c8e158c HEAD` filtered against the brief's allowed paths | 0 | 2,703 A, 27 M, 0 D; outside the allowed paths only `tests/cp18a/test_dry_run.py` and `tests/cp18a/test_rules.py`, each `+1 −0`, the exact lines O35 and O36 quote; `tests/test_24_live_namespace_is_walled_off.py` `+48 −0` (additions only); no other checkpoint's `reports/` or evidence touched |
| 3b | for each of the 27 modified files: SHA-256 of its base bytes, `git grep -F` of the full hash and its 12-hex prefix at `3c8e158c` | 0 | no freeze manifest, `PINS` or evidence names any of them, except `reports/cp18b/space-build.json`, CP-18b's historical build record, which lists the base hashes of `space-product/{index.html,app/main.js,app/charts.js}`; no test reads that record (`grep`), and `space-product/` is an allowed path. `tests/cp18a/test_dry_run.py` base `a6e56482…` and `test_rules.py` base `f839d52f…`, named nowhere, as the report states |
| 3c | `git ls-tree -r -l HEAD` (sizes) | 0 | no file over 50 MB (largest `models/champion/python_model.pkl` 30,830,306, pre-existing); committed `live/` 1,847 files, **53,909,152 bytes**; its largest file `live/pinned/…/k13.json` 20,230,545, the same blob (`604eec26…`) as `reports/cp18a/dryrun/pinned/…/k13.json`; `live/` holds only `.gz` (1,610), `.json` (164), `.jsonl` (4), `.npz` (69) |
| 4 | `python3 $P/.local/artifacts/cp-18c/ci-runner.py critic4 3513057858… ci312 stress` (label `critic4` instead of `critic`, so the earlier critic's logs under `critic-validation/` were not overwritten; the label only names the scratch folder and the log folder) | 0 | history-free single commit, tree `3096ed27…` = the candidate's; ci312: leak-scan 0 ("clean (F1 skipped, F2, F3; allowlist 4 entries)"), `uv sync --locked --dev` 0, `build_wasm_payload.py` 0, **`pytest -q` 0: 3128 passed, 71 skipped** (753 s), `test_10_cqr_order_statistic.py` 0 (8 passed), `verify_release.py` 0 ("PASS — every bound claim agrees on every surface…"), `test_22_wasm_equivalence.py` 0 (15 passed), `publication_guard.py tree` 0, stress collection 0 (22/3198); **stress: `pytest -m stress` 0: 20 passed, 3 skipped** (459 s); both scratch trees removed. Logs: `$P/.local/artifacts/cp-18c/critic4-validation/{ci312,stress}/` |
| 5 | `cd $W && CP17_PROJECT_ROOT=$P PYTHONPATH=src $P/.venv/bin/python -m pytest -p no:cacheprovider --basetemp=$S/pt-guard2 -q tests/cp18c/test_guard_two_sides.py` | 0 | 10 passed |
| 5a | `$S/guard_by_hand.py`, `$S/guard_by_hand2.py` (by hand, `PYTHONPATH=src`) | 0 | `cp25.guard.admit_delivery_day(2026-09-07)` refused ("after the development boundary 2026-09-06"), 2026-09-06 admitted; inside `cp18.boundary.live()` (present 2026-11-13T15:37Z): 2026-09-07 admitted, horizon 2026-11-15 admitted, **2026-11-16 refused** ("after the present (2026-11-15 is the last admitted day)"), a GFS run initialized tomorrow refused; inside the block `cp25.guard.admit_delivery_day(2026-09-07)` and **`cp17.tools.payloads.admit(2026-09-07)` still refused**; outside the block `cp18.boundary.admit_delivery_day(2026-09-07)` refused; fixed presents 2026-11-13T10:30Z → horizon 2026-11-15, 09:30Z → 2026-11-14 (the 11:00 Berlin cutoff) |
| 6 | `cp -R $W/live $S/live`; `cd $W && PYTHONPATH=src $P/.venv/bin/python -m cp18.bundle --mode live --root $W --project $P --live $S/live --out $S/bundle --refit --no-retrieval --record $S/bundle-record.json` | 0 | `bundle 40d71955ce14471d stale as of 2026-11-13 \| latest issued 2026-11-08 \| publishable \| first visit 389488 bytes`; 209 s wall, peak 1.06 GB. Gate: identity problems none, recompute match (6 recomputed windows), served artifact `3e046a00…` refit "within the frozen recomputation tolerance (1.1e-13 EUR/MWh)" |
| 6a | key-by-key comparison of `$S/bundle-record.json` with `$W/reports/cp18c/evidence/bundle-record-2026-11-12.json` (`7d2ae84c…`) | 0 | equal: `gate`, `served_artifact`, `days`, `daily_windows`, `store_head`, `series_last_day`, `static_development_sha256`, `b0_equal_to_shadow`, `schema`. Different only by the as-of day: built on **2026-11-13**, not 2026-11-12, so `freshness` (as of 11-13, target 11-14 "not decided yet"), `manifest_sha256` (`40d71955…` vs `7d2ae84c…`), `not_issued` (the same 8 days with the same causes, plus 2026-11-14 "not decided yet"), the reconciliation entry's file name, `now`, `out`, `run_id`, `payload_sources` (rebuilt by the live-input builder here, cached there), manifest size +51 bytes |
| 7 | `cd $W && PYTHONPATH=src $P/.venv/bin/python -m cp18.controls --bundle $S/bundle --record $S/controls.json --root $W` | 0 | `controls 20 all refused \| served bundle publishable: True` (manifest state `late`, missing file, unhashed byte, unreadable JSON/NPZ, unlisted file, schema, wrong kind, training-window flip and meta, target-day price leak, B0 release after D−2, artifact identity, issued ≠ artifact, other artifact, package, policy, R7 verifier raise, recompute mismatch, research window past the boundary) |
| 8a | `PYTHONPATH=src $P/.venv/bin/python $W/scripts/build_product_space.py --bundle $S/bundle --out $S/dist --live $S/live --history $W/reports/cp18c/history-v1/files` | 0 | `bundle 40d71955ce14471d stale \| publishable \| first visit 574329 bytes \| on request 50118577 bytes \| live record db2f0c2b8254ee34 \| history 805 files` |
| 8b | `PYTHONPATH=src $P/.venv/bin/python $W/tests/cp18c/space_acceptance.py --prepare $S/variants --bundle $S/bundle --live $S/live --project $P` | 0 | variants built: tampered, mismatch, seed, prices, pending, stale, failed (+ live-pending/stale/failed stores), running display (20 scored dev days, 7) |
| 8c | `PLAYWRIGHT_BROWSERS_PATH=$P/.local/tools/ms-playwright $P/.local/tools/playwright/bin/python $W/tests/cp18c/space_acceptance.py --dist $S/dist --scratch $S/accept --live $S/live --variants $S/variants --build-python $P/.venv/bin/python --engines chromium,webkit` | 0 | **591 passed, 0 failed, 1 not run** (Chromium 153.0.8010.12: 298 passed; WebKit 26.6: 293 passed, 1 not run — "accessibility tree: disclosures expose expanded/collapsed", WebKit's `<details>` state, as CP-18b). **"Train it yourself": Chromium "identical bit for bit" (83.6 s), WebKit "identical bit for bit" (77.7 s), the changed-seed variant "different".** Zero non-local requests on the product page, every view and the demo states; v1's demo, opened from the page's own link `history/index.html`, would request `cdn.jsdelivr.net` (blocked, recorded, outside the product's rule). One `BrokenPipeError` traceback from the local test server during the demo's cancel check (the browser aborting a cancelled download); every check passed. Record: `$S/accept/acceptance.json` |
| 9 | `LiveStore('$W/live/store').verify()`, `.days()`, `.first_day()`, `.last_closed()` | 0 | verifies: 14 entries, head entry `03094253…`, last day 2026-11-08; genesis origin 2026-09-06, first day 2026-09-07; carry 2026-09-06 → first live day **2026-11-03**, reason naming decision 28 (`4daa5617…`) and r20 §24.14 item 4; 2026-09-07..11-02 `outside`; 11-03..05 not issued `inputs`; 11-06, 11-07, 11-08 issued by A1; 11-09 not issued `no_run` |
| 9a | `cd $W && … pytest -q -rs tests/cp18c/test_live_record.py` | 0 | 2 passed |
| 9b | `Archive('$W/live/inputs').verify()` on every day and `acquire.load_forecast_shown` for 11-03..13, inside `boundary.live()` | 0 | 68 archive days (2026-09-07..11-13), no problem; load forecast published strictly before the cutoff for 11-06 (09:17:52Z < 10:00Z), 11-07 (09:07:44Z), 11-08 (09:07:45Z); after it for 11-03..05 (2026-11-05T08:25Z) and 11-10..13 (2026-11-12T13:56–14:02Z) |
| 9c | each issued day's `record.json` availability records, summarized | 0 | 11-06/07/08: every price, load-forecast and GFS record admitted and published before the day's cutoff; prices up to D−1 only (target-day embargo: `max data_day` 11-05/11-06/11-07); bases `documented_schedule` (tier 2), `document_time`, `aws_last_modified`; none by exception |
| 9d | issued days' `artifact.json`/`record.json`, run records | 0 | each carries its actual run: 11-06 run 21:52:20Z, issuance 21:54:19–21:57:41Z; 11-07 10:21:35–10:24:44Z; 11-08 10:21:35–10:24:42Z (all UTC), host M3 arm64 Darwin, `local`; the artifact's `issuance_utc` is the cutoff (N7). H2 gate of `local-20261105-first-live` failed at `pins` (28 local files unchecked; binary, machine, canary not run; nothing issued); of `-second-live` and `-2026-11-12-after-the-gap`: pins `verified`, binary `a9bd0630…`/tarball pinned, machine, **canary quantiles `4e6abb02…` = expected**. After-gap run: planned 11-10..13, none issued (`inputs`), 11-09 closed `no_run` |
| 10 | read `$W/.github/workflows/daily.yml` (444 lines) and its history; `git diff bd52db99 544b5ff7 -- .github/workflows/daily.yml`; `grep -n '${{'` outside `if:`/`timeout`/`group`/`env`/`path`; `plutil -lint $W/reports/cp18c/launchd/*.plist`; `launchctl list \| grep -i delu`; `ls ~/Library/LaunchAgents \| grep -i delu` | 0 / 0 / 0 / 1 / 1 | checked against item 8 (below); no interpolation into a script; both plists `OK`; **no `launchd` agent installed** (both greps empty, exit 1); the rehearsed workflow (`755dfd7a…`, imported at `bd52db99`) differs from the candidate's (`2168e42c…`) only in the publication step's `uv run --frozen --no-sync --with huggingface_hub==0.36.2` overlay |
| 11 | read `$W/docs/track-b/exposure-ledger-continued.md`; `grep '^\| [0-9]+ \|' docs/track-b/exposure-ledger.md` | 0 | the pinned ledger ends at entry 5; the continuation's one row is entry **6**, dated 2026-11-05 by the first retrieval (the Lead's probe 08:13:02Z; the pipeline 08:15:09Z; first archived 08:17:13Z = `retrievals.json`'s `first_retrieval_utc`); impact assessment as §24.14 states it; no market value |
| 12 | `env -u HF_TOKEN … python -c` constructing `cp18.publish.HubTarget(repo)` and calling `HubTarget(repo, authorized=True, hub=object()).commit(…)` | 0 | "the Hugging Face upload is CP-18's activation; nothing was uploaded"; "HF_TOKEN is unset; no upload was attempted" |
| 13 | `printf 'refs/heads/gauntlet/cp-18c 3513057858… refs/heads/gauntlet/cp-18c 0000…\n' \| python3 -I scripts/secret_guard.py pre-push origin x` (in `$W`) | 0 | no finding over the 42 candidate commits not on `origin`'s refs (every blob and message); the guard loaded 5 credential values (names only: ACLED_PASSWORD, CLAUDE_CODE_MESSAGING_TOKEN, DAGSHUB_USER_TOKEN, ENTSOE_API_TOKEN, HF_TOKEN; no value seen) |
| 14 | `curl` (anonymous HTTPS) of `https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/`: `/`, `/history/`, `/history/index.html`, `/payloads/manifest.json`, `/app/space-build.json`, `/app/live-record.json`, `/app/{style.css,charts.js,main.js}` | 0 | `/` 302 → `/index.html`; **`/history/` 302 → `https://huggingface.co/history`** (as disclosed); `/history/index.html` 200, title v1's; served manifest SHA-256 `127d5bb5…` = `publication-2.json`'s intended and served; `style.css` and `charts.js` equal the candidate's; public `main.js` differs from the candidate's by exactly line 1381, `href: '/history/'` → `'history/index.html'` (the fix, not yet published) |
| 15 | `brew list --pinned \| grep -x node`; `ls /opt/homebrew/Cellar/node/` | 0 | `node` pinned; `26.7.0` |
| 16 | `git -C $W status --porcelain` and `rev-parse HEAD` at the end | 0 | empty; `3513057858…` |

## Evidence actually inspected

- The brief (`docs/track-b/evidence/cp-18c/issued-brief.md`, in full), the rulings file (`orchestrator-rulings-as-relayed.md`,
  in full), `reports/cp18c/report.md` (in full, as a claim), `AGENTS.md`.
- The diff `3c8e158c..HEAD`: the name/status list, the two O35/O36 lines, `tests/test_24…` (additions),
  `src/cp18/boundary.py` (in full), `src/cp18/store.py`'s diff, `src/cp18/publish.py` (`HubTarget`, `main`),
  `src/cp18/live/build.py` (the bridge-day edge), `src/cp18/live_claims.py` (both claim modes), `src/cp18/running.py`
  (constants), `src/cp18/local.py` (`bundle_plan`), `src/cp18/live/transport.py` (credential and TLS lines), the diff
  `de73d2ca..HEAD` (9 files: `main.js` one line, `space_acceptance.py`'s History route, `public_check.py` new, records).
- `.github/workflows/daily.yml` (in full); `tests/cp18c/test_workflow.py`'s names and its two-year timing test.
- `live/store/` (ledger, head, issued days' `artifact.json`/`record.json` metadata, the five run records' gate and plan),
  `live/inputs/` (via `Archive.verify`, availability records' times and bases only), `live/outcomes/`, `live/evaluation/`
  and `live/bundles/` ledgers (metadata only; no market value read).
- `reports/cp18c/evidence/{retrievals,compute-ledger,controls-2026-11-12,bundle-record-2026-11-12,space-build-2026-11-12}.json`,
  `reports/cp18c/rehearsal/*.json`, `reports/cp18c/acceptance/acceptance.json` (summary),
  `reports/cp18c/history-v1/listing.json` (805 files, 44,164,910 bytes, each SHA-256 and size equal to the committed
  copies), v1's `index.html` (relative asset paths only), `docs/track-b/evidence/cp-18c/publication-{1,2}.json`.
- My own outputs: `$S/bundle-record.json`, `$S/controls.json`, `$S/dist/app/{space-build,live-record,claims}.json`,
  `$S/accept/acceptance.json`, the CI logs.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| O1 | The guard retired for the live pipeline only; research paths still refuse after 2026-09-06; both sides tested; frozen/pinned files routed around in `src/cp18/` | PASS | Cmd 5, 5a, 3. `src/cp25/guard.py` is in CP-17c's freeze manifest and unchanged; the route is `src/cp18/boundary.py` (a context-scoped live mode; outside it every check is `cp25.guard`'s). `cp17.tools.payloads` refuses even inside the block. The live horizon is the next day whose cutoff is ahead |
| O2 | All the data through the present: inputs archived with URL, time, size, SHA-256, vintage; availability by publication time; pinned ecCodes on Mac and runner; builder on darwin-arm64; credentials in-process | PASS | Cmd 9b, 9c, 3c; `retrievals.json` (5,010 requests, 3,138,995,845 bytes, 2026-11-05T08:17:13Z..11-12T14:04:38Z); archive verifies (68 days); ecCodes 2.49.0 on the Mac and on `macos-26` (`wx-env-*.json`, `decode-check-*.json`: 50/50 messages byte-equal); ENTSO-E token read with `os.environ.get` in the transport only, errors redacted, TLS verified against `certifi`. The darwin-arm64 restriction is operational (H2's machine check, the bundle's payload-identity check), not a code guard in the builder |
| O3 | Live store: genesis at 2026-09-06 with CP-18a's genesis, carried with decision 28 as the reason; days between outside, never issued | PASS | Cmd 9; `verify()` refuses a first carry off the genesis origin (store.py diff; `test_live_start.py`) |
| O4 | First live issuances on the Mac after H2; target day and catch-up with actual run times; every day not issued recorded | PASS | Cmd 9d: 11-06/07/08 issued after a passing H2 (canary `4e6abb02…`); 11-03..05 `inputs`; 11-09 `no_run`; 11-10..13 open with `inputs`, attempted. The first run's pins failure issued nothing and is recorded and disclosed. O31's first live day (the earliest inside the lookback before the 11-06 target) matches |
| O5 | Outcomes and evaluation, live; each price names its archive (N1); prospective only, never pooled, nothing labelled 4.7T | PASS | Outcomes ledger (2 reconciliations), evaluation and bundle ledgers chained; `test_live_bundle.py` (N1, red line, no 4.7T, never pooled) in the CI pass; acceptance O32 checks "one window per chart, never pooled" |
| O6 | Dated bundle and Space from the live record; gate passes; red line on research windows only; v1 at `/history/` unchanged; the required wording; acceptance in Chromium and WebKit | PASS | Cmd 6, 6a, 7, 8a–8c. The Space shows "v6 · DDNN-2 alone", "final candidate · pending 4.7T", "prospective evaluation in progress", N7's cutoff-based issue time beside each actual run (10 N7 checks), O14's sentence (0.082 EUR/MWh, `limitations[2]`, the Limitations view equal to the claims in order), development displays through 2026-09-06 only (Data last day 2026-09-06; O32 "development days through the boundary only"), nothing live labelled 4.7T, no "A1 · DDNN-2 alone". v1's 805 files equal the committed listing. The History link names `history/index.html` and opens v1 |
| O7 | Publication to Hugging Face after the PASS (by design after this review): the step and its target exist and refuse without authorization | PASS (as scoped) | Cmd 12; `cp18.publish --hub`, `HubTarget` with one `create_commit` against the read revision and a tree check. See observation 1 on the two recorded publications |
| O8 | `daily.yml`: schedule after the cutoff and acquisition before it; live mode; claim on `origin`; bundle before the arrays are deleted; Space and publication steps; secrets only in using steps; `contents: write` only where it writes; the 60-day rule; rehearsal with fake credentials; `launchd` written, tested, not installed | PASS | Cmd 10. Crons 07:40/08:20/09:20 (acquire) and 10:40/13:40 (run), selected by `github.event.schedule`, gated by `vars.DAILY_SCHEDULE == 'enabled'` and the product repository; `cp18 run --mode live --remote origin`; `bundle-plan` takes `$RESULTS/run/runs/A1-<day>-*/run-arrays.npz`, deleted only in the final hashes step; Space build and `cp18.publish --hub`; `ENTSOE_API_TOKEN` in acquire/run (and the by-value scan), `HF_TOKEN` in the publication (and the scan), `DAGSHUB_USER_TOKEN` unused; `permissions: {}` top-level, `contents: write` on acquire and run only, dry-run `read`, keep-alive `actions: write`; every job has `timeout-minutes`; actions SHA-pinned, `persist-credentials: false`. 60 days: a data-only push every live run plus the keep-alive job. Rehearsal runs 42221640423 and 42223428846 succeeded, fake credentials, 0.272 of 6 job-hours, scans clean |
| O9 | N5, N1, N7, the 31-December Monday bridge-day edge fails closed, rulesets written | PASS | `bridge_day_edge` = month 12, day 31, Monday, checked before any build (`build.py`); tests for N5, bridge edge, N1, N7 passed in CI; `reports/cp18a/rulesets/` present, unapplied |
| O10 | Exposure ledger continuation: decision 28's entry dated by the first retrieval, §24.14's impact assessment, no market value | PASS | Cmd 11; the pinned ledger unchanged (cmd 3) |
| O11 | Tests: guard sides, carry, N5, bridge edge, source labels, issue-time labels; CP-18b's controls refused on the live bundle | PASS | 97 tests in `tests/cp18c/` named for each; cmd 4 (all pass); cmd 7 (20 of 20 refused) |
| O12 | The return's table for the Orchestrator's steps after the LAND | Not checked (by design) | The return follows this review |
| F1 | 4.7T exactly as registered; no 4.7T issuance, store or score; nothing live labelled 4.7T's | PASS | No 4.7T store or run in the diff; `refreeze verify`; the bundle's control "a window labelled 4.7T may hold no scored day"; the acceptance's "not 4.7T's" wording checks |
| F2 | The research boundary holds | PASS | Cmd 5a, 3; `static_development_sha256` unchanged in my rebuild; Data and development windows end 2026-09-06; `test_24` extension: no record surface renders a live prospective figure. Whether any agent read news or analyses is not checkable from the artifact |
| F3 | GitHub-landable; no file over 50 MB; live archive data only, size disclosed | PASS | Cmd 3c; the report's 53.9 MB matches |
| F4 | CI-ready: history-free, `CI=true`, Python 3.12, global Git config hidden; `pytest -m stress`; committing tests set their identity; platform byte tests skip off darwin-arm64; live-data tests skip with a reason when absent | PASS (macOS) | Cmd 4. Linux (GitHub's ubuntu CI) cannot be reproduced here; because `live/` is committed, the live-record tests will run there, not skip (observation 6) |
| F5 | What never changes | PASS | Cmd 3, 3a, 3b; O35 and O36 lines exact; `src/cp17`, `src/cp17c` unchanged |
| F6 | The Critic's reruns: CI and stress; guard sides; one live bundle with recompute; controls; Space in Chromium and WebKit with a retrain to its status; `refreeze verify` | PASS | Cmd 2, 4, 5, 6, 7, 8c |
| AC1 | Homebrew `node` stays pinned and installed | PASS | Cmd 15 |
| AC2 | Credentials per `AGENTS.md`; nothing printed; no secret created; telemetry off | PASS | Cmd 13; credential reads with `os.environ.get` inside the consuming code; no value in any candidate commit; the workflow scans results by value before upload |
| AC3 | Value-based secret scan before every scratch push and before the upload | PASS (records) | Rehearsal records `scans` clean for fake and Owner values; `publication-2.json` `credential_guard: passed`. The pushes themselves are not re-observable |
| AC4 | Allowed paths (+ O35, O36) | PASS | Cmd 3a |
| AC5 | Ceilings: 16 local machine-hours, 4 workers, 6 GitHub job-hours, one Hugging Face publication | PASS with observation 1 | `compute-ledger.json`: about 6.0 machine-hours before the reviews, 0.272 job-hours. Two Hub commits are recorded (see observation 1) |
| AC6 | Tools and process: the gauntlet, the worktree, one Critic via critic-open/brief/close, the return check | Partly checkable | This review ran through `critic-brief`; the worktree exists. The start/return steps are outside the artifact |
| AC7 | Memory directory not opened; owner-facing Git commands non-interactive | Not checkable from the artifact | I did not open it |
| O29 | One product, A1 = v6 now, "final candidate · pending 4.7T"; v1 the last released generation, historical | PASS | `live_claims._live_values`; acceptance O30/O13 checks; History "Historical" |
| O30 | Public name "v6 · DDNN-2 alone", "v6 (A1 in the frozen records)" | PASS | Same; "no 'A1 · DDNN-2 alone' anywhere rendered" passed in both engines (the old name remains only in CP-18b's dry-run claim mode) |
| O31 | First live day = earliest inside the lookback; catch-up then target; earlier issued days shown against prices | PASS | Carry to 11-03; run planned 11-03..06; acceptance's panel and Forecast checks |
| O32 | Per-day MAE and interval score, live beside development, A9's breakdown, never pooled, no %-correct or confidence | PASS | Acceptance O32 checks (both engines), "Matches the stored value · per day" |
| O33 | Running means and paired difference with the frozen CP-28 interval method, from 14 scored days; wording | PASS | `cp18.running` (`MINIMUM_DAYS = 2 * BLOCK_DAYS`, 10,000 replicates, the frozen seed); `test_running.py` bit-identical to `cp28`'s `test_endpoint`; acceptance O33 checks incl. the display-only 20-day build |
| O35 | One line in `tests/cp18a/test_dry_run.py`; parallels in `forced.py` and `daily.yml`'s dry run; stress passes | PASS | Cmd 3a, 4; `daily.yml` dry run `git rm -r -q --ignore-unmatch -- live` |
| O36 | One skip line in `tests/cp18a/test_rules.py`; the old properties asserted in `test_workflow.py` | PASS | Cmd 3a; `test_permissions_contents_write_only_on_the_jobs_that_push`, `test_actions_are_pinned_by_commit…`, `test_secrets_are_read_only_inside_the_steps_that_use_them`, `test_every_job_has_a_time_limit` (all passed in cmd 4) |
| I-11-12 | The gap recorded in the store; acquisitions before the cutoff; no `launchd` | PASS | Cmd 9, 9d, 10 |

## Observations (non-blocking; for the Orchestrator)

1. **Two Hugging Face publications are recorded, and the second rests on a ruling the candidate does not carry.** The
   brief authorizes "one Hugging Face publication" and its ceiling is one publication (`compute-ledger.json` repeats it).
   The candidate records publication 1 (`0331088…` → `2fcd91cd…`) and a daily update, publication 2 (`2fcd91cd…` →
   `8f6a9d9f…`, 2026-11-13T14:59Z). The report attributes both to "O37", which is not in
   `orchestrator-rulings-as-relayed.md`, so I could not check its text. Publication 2 also served data from the local
   claim (2026-11-14 issued), beyond the candidate's committed `live/`, and its one-commit mirror deleted the previous
   day's `payloads/A1-2026-11-08.*` from the Space's tree (still in the Space's Git history).
2. **The public Space still links `/history/`, which the static host sends to an unrelated profile.** I confirmed the 302
   to `https://huggingface.co/history`. The candidate fixes the link; it takes effect at the next publication.
3. **The committed evidence predates the fix in two places.** `reports/cp18c/evidence/space-build-2026-11-12.json` was
   built with the old `main.js`. The committed acceptance (591/0/1) ran on a build from the local claim as of 11-13,
   not the candidate's `live/`. My run on the candidate's own record independently gives 591/0/1.
4. **`reports/cp18c/history-v1/listing.json` records SHA-256 and size only, not the Hub's blob ids.** The report's
   "each matching the Hub's blob id" could not be checked without a request to `huggingface.co`, which this review was
   not given. The copies match the listing, and the public `history/index.html` serves v1's title.
5. **The Hub client is pinned by version only.** `huggingface_hub==0.36.2` is resolved through `uv run --with` at run
   time, with no hash. Its workflow step was not rehearsed on a runner; the report discloses this.
6. **GitHub's Linux CI is not reproduced.** Because `live/` is committed, `test_live_record.py`, `test_live_start.py`
   and the store-dependent `test_space_live.py` tests run on GitHub, not skip. They passed on macOS here. Read the first
   GitHub CI after the push before closing.
7. `reports/cp18b/space-build.json` (CP-18b's historical build record) names the pre-change hashes of three
   `space-product/` files. No test binds it.

## On FAIL only
- Single largest meaningful gap: not applicable (PASS).
- Exact next acceptance test: not applicable.
