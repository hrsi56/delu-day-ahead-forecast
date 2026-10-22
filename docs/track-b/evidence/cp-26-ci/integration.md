# Verdict — CP-26-CI — Integration — PASS

- Candidate SHA: `9b6a0c38edbdecee202c33fe610c7c4475cf7cfc`
- Candidate tree: `f10e29c9790aecaf45866786912dd94c59aab6bc`
- Plan / version / bar: `capstone_v21.md`, v21-r17, §24.2, “The short path, the development boundary and the red line.”
- Research anchor SHA-256: `3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc`.
- Complete maintenance authority: `docs/track-b/evidence/cp-26-ci/issued-brief.md`, SHA-256 `3b6c63fe0ca65c91b999b0de6d579bae6930fd0b7dbc22ad86745ea70881c0d0`.
- Worktree clean before and after: yes, at the unchanged full candidate SHA. The dedicated detached checkout was `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26-ci/critic-1`.
- Isolation was cooperative and procedural. I ran no direct Git mutation command and made no tracked edit in that checkout. Reproduction ran only in the two Lead-prepared history-free copies.

## Verbatim research invariant excerpt

> ### 24.2 The short path, the development boundary and the red line
>
> **The short path (Owner, 2026-10-12).** No new data source is collected, tested or admitted in this
> programme. Stage 3's shortlist (`docs/track-b/data-source-research-2026-10-11.md`) stays a
> documented finding: a possible extension after the final product. No enquiry, registration or
> purchase follows from it.
>
> **Development data:** delivery days 2019-01-01 to 2026-09-06, the existing snapshot's span.
>
> - **The period 2026-04-08 to 2026-09-06 joins development by this revision** (Owner, 2026-10-12).
>   - The research never used it: the earlier boundary was `data/partitions.json`'s `eda_cutoff`,
>     2026-04-07.
>   - v1 used it for its CQR calibration (2026-04-09 to 2026-06-07) and its one-shot holdout
>     (2026-06-09 to 2026-09-06), whose results are published (`docs/cp2-model-report.md` §4).
>   - It therefore cannot serve as a fresh test, and serves as development data instead.
> - **v1's historical records stay unchanged,** and so do `data/partitions.json` and
>   `data/snapshot.parquet` (§1). CP-25 writes a new partition specification beside them. v1's
>   holdout results stay v1's record, while the days themselves are development data.
> - **Displays and publication.** Before the final test, no research number, chart or choice uses
>   data after 2026-09-06. That replaces §19.8's 2026-04-07, and PUBLISH_RULES invariant 10 moves
>   with it (PUBLISH_RULES 1.5).
>
> **The red line.** Delivery days from 2026-09-07 stay closed until 4.7T opens (§24.9).
>
> - **Data on disk.** Every downloader refuses any row whose Europe/Berlin delivery day is after
>   2026-09-06, in code.
>   - **For GFS, the guard tests the run's initialization, not its valid time.** A run serves the
>     delivery day after its run date. The guard refuses any run initialized at or after 2026-09-06
>     00 UTC, and any lead outside §15.2's f021–f048. A forecast's valid time after the boundary is
>     not an outcome.
>   - **Tests:**
>     - the instants 2026-09-06 21:00 and 22:00 UTC, for rows;
>     - the 2026-09-06 00 UTC run, which is refused;
>     - the 2026-09-05 00 UTC run's f048 message, which serves delivery day 2026-09-06 and is
>       admitted.
> - **The boundary moves only twice.** The 4.7T gate moves it to 2026-12-05. After 4.7T, CP-18's
>   brief retires the guard for the live pipeline only.
> - **Reading.** No agent reads reports, news, analyses or prices about market events after
>   2026-09-06.
> - **The window.** 4.7T's window is fixed now (§24.3) and is never extended after a result.
>
> **The exposure ledger** lives in `docs/track-b/exposure-ledger.md`. The Orchestrator keeps it,
> seeds it with the entries below at ratification, and adds every later exposure. Known entries:
>
> 1. **2026-09-08, the snapshot pull** (`data/source_manifest.json`). The first review found no
>    committed row after 2026-09-06; the audit verifies the pull's request bounds.
> 2. **2026-09-15, CP-15's retrieval of smard.de pages**
>    (`reports/cp15/feasibility/source_retrieval_manifest.json`).
> 3. **2026-10-11, stage 3's retrieval of provider pages:** documentation and metadata only, by its
>    report. Its only data query was Elia's record counts, bounded at 2026-04-07 Brussels.
> 4. **2026-10-12, the stage 4 research agent** reported that a search showed it an excerpt from
>    after 2026-04-07, which it discarded. It left no raw material, and the Orchestrator did not look
>    for the excerpt.
>
> **Their impact assessment** is recorded in the ledger before CP-26's first score, and CP-26's
> Integration Critic reviews it. For entry 4, the assessment considers whether any value adopted
> from the stage 4 memo could carry a market outcome.
>
> **The audit standard (for §24.9):**
>
> - **The test:** no outcome after 2026-09-06 entered any fit, tuning, selection, registration or
>   recorded Owner decision.
> - **Incidental exposures** are listed, each with an impact assessment. They block 4.7T only if they
>   could have informed a registered choice.
> - **The Owner declares in the audit** that his decisions used no information after 2026-09-06:
>   the tier ruling (§24.5), the CP-28 decision, the margin rulings, and CP-17.
> - **The CP-28 decision:** the Owner's confirmation of CP-28 may rest only on CP-26's report, its
>   resources and this section.
>
> **The boundary governs development only.** The live product, once running, trains on all the data
> available to it.

The excerpt is the citation; line numbers are non-binding. Canonical excerpt: 71 lines, 4,394 bytes, SHA-256 `408828ccbf4dd9647e8d07e915835b80d56ec7a6b7b5da4748bc3942e3ad2137`.

## Complete six-item maintenance bar — verbatim

> ## Complete authoritative checkpoint bar
> The Owner's decision of 2026-10-21 ("(א), עם הסימון stress. עכשיו."), as these items:
>
> 1. **The `stress` marker.**
>    - **Which tests:** every CP-26 test that starts real CP-26 monitors (`real_monitor`,
>      `three_real_monitors`, `arriving_admin_monitor`, or the same through the CLI) with concurrent
>      children whose timing the test asserts, at least the rich-admin test above. The return lists
>      each marked test and the one-line reason it qualifies. Tests that use no real monitor are not
>      marked.
>    - **Where they skip:** only when `CI=true` (GitHub sets it) and `RUN_STRESS` is not `1`. The
>      reason is shown in pytest's output: CP-26 supervision stress test, run locally because a
>      4-vCPU CI runner cannot host it reliably, `RUN_STRESS=1` forces it.
>    - **Elsewhere they run by default,** with no environment variable. `pytest -m stress` selects
>      exactly them.
>    - **No marked test's body or assertion changes.**
> 2. **A living exposure ledger.**
>    - **The frozen copy:** commit a byte-identical copy of `61658c7:docs/track-b/exposure-ledger.md`
>      as CP-26 evidence, under `docs/track-b/evidence/cp-26/`.
>    - **What the tests check instead:**
>      - that copy's SHA-256 equals `PINS['docs/track-b/exposure-ledger.md']`;
>      - the live ledger still holds every row of the copy's table, verbatim and in order. Rows may
>        be added after them, and the prose above the table may change.
>    - **What does not change:** `src/cp26/harness.py` and `PINS`.
>    - **Every test that reads the live ledger's bytes for an identity** (pinned-file loops, input
>      fingerprints) uses the frozen copy, which the return lists.
> 3. **Proven both ways,** in a scratch copy of the candidate:
>    - append a synthetic row to the live ledger, and the full suite passes;
>    - alter one row that existed at CP-26, and at least one named test fails.
>
>    The scratch copy is removed afterwards and nothing of it is committed.
> 4. **The suite, three ways,** each on a history-free single-commit copy of the candidate's tree:
>    - with `CI=true` the workflow's seven steps are green under Python 3.12 and 3.13, and the
>      stress tests show as skipped with the reason;
>    - without `CI`, the full suite is green under Python 3.12 on a quiet machine, stress tests
>      included;
>    - `RUN_STRESS=1 CI=true` runs them.
> 5. **Scope:**
>    - `git diff --stat main <candidate> -- reports/ src/ data/ scripts/ .github/ pyproject.toml uv.lock`
>      is empty;
>    - the anchors, the amendment records, `AGENTS.md`, the role files, the backup register and the
>      live exposure ledger are unchanged;
>    - `tests/conftest.py` may change only to register the marker and the skip. Check first that no
>      committed evidence binds its bytes, and say so.
> 6. **One fresh focused Integration Critic,** from a clean detached checkout of the candidate. It
>    checks items 1–5, and reruns item 3 and the `CI=true` Python 3.12 sequence.

The complete excerpt is the citation. Canonical maintenance section: 45 lines, 2,983 bytes, SHA-256 `80e99d6a53777c090366910260b878cacc3deb33250030d4314511046560c4b5`.

## Commands actually run

Every shell entry point explicitly selected the detached checkout as its working directory. The table records actual child commands and their copy-specific working directories. The executable driver was:

- `python3 /Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/reproduce.py ci312`
- `python3 /Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/reproduce.py mutation`
- Driver SHA-256: `a9f916860be7c56ad44c4863e1f48f0034f40541d912c06fa15e54982ae40f68`.

The two invocations ran serially after the Lead explicitly released the quiet machine. Both started with a fresh `.venv`; `UV_PYTHON=3.12`, `UV_PYTHON_DOWNLOADS=never`, the project-local shared uv cache, copy-local `UV_PROJECT_ENVIRONMENT`, `PYTHONPATH`, `TMPDIR`, pytest basetemp and caches were explicit. `PYTHONDONTWRITEBYTECODE` and `VIRTUAL_ENV` were removed. Actual credential variables and the inherited tracking URI were removed inside the consuming subprocess environment, without inspecting or emitting values. `MLFLOW_DISABLE_TELEMETRY=true` and `DO_NOT_TRACK=1` were set. After sync, `UV_OFFLINE=1`; `.venv/bin` headed PATH so direct `python3` and uv both reported Python 3.12.14. The invalid temporary-root `.git` sentinels remained present.

CI mode used exactly `CI=true`, with `RUN_STRESS` absent. Mutation mode removed both. The unchanged seven workflow commands ran in their issued order; version and topology observations were supplementary.

| Copy / command | Exit | Observed output | Raw log / SHA-256 |
|---|---|---|---|
| critic-ci312: `git rev-list --count HEAD` | 0 | 1 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/00-history.log`; `9869a1f704351f6e7f5af6f9ffc758eb0a85c33e5baf9806bb5ff035fcc54641` |
| critic-ci312: `git rev-parse 'HEAD^{tree}'` | 0 | f10e29c9790aecaf45866786912dd94c59aab6bc | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/00-tree.log`; `84a44a8f821981283ff47e4aaa660ff009ee89c75eac61be978fc523c06a04b1` |
| critic-ci312: `uv sync --locked --dev` | 0 |  + zipp==4.1.0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/01-sync.log`; `cec5ab515c1b7ff28590938674d4406b2b15ce16d8ef8b2b2571dc086f3f84c6` |
| critic-ci312: `python3 --version` | 0 | Python 3.12.14 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/01-direct-python-version.log`; `f1c67c1448ff23fd0f52f688e6adf2c0bca784f816df3de9f6972f308180b782` |
| critic-ci312: `uv run python --version` | 0 | Python 3.12.14 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/01-python-version.log`; `d8166eb859451afd048d762dfaaad4460426fc96f41842f318ffba9898b43853` |
| critic-ci312: `uv run python scripts/build_wasm_payload.py` | 0 | wrote /Users/djourno/Downloads/PJM/.local/tmp/cp-26-ci/critic-ci312/reports/cp3b/payload.json | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/02-payload.log`; `3fb4eaf35bba5bdb18d3cd9b820c9cbc90f13c796bbd68d9b3e5177660e91d25` |
| critic-ci312: `uv run pytest -q` | 0 | 2190 passed, 32 skipped; exactly 16 stress skips show the required reason. | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/03-suite.log`; `46e472bfb0a8a4ca18ed066cdbacdc779effdc9139beff47957370cf3d086ac7` |
| critic-ci312: `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | 8 passed in 0.02s | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/04-cqr.log`; `d422fbe2e481c669d2a194187dfb0c2645911525c10285beb12e2357a270487d` |
| critic-ci312: `uv run python scripts/verify_release.py` | 0 | PASS — every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/05-release.log`; `b69996cb1e6d2b04eb0f3d50e3f0b8042b311f24afd9bf21d58358e7078e7e79` |
| critic-ci312: `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | 15 passed in 1.13s | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/06-wasm.log`; `6e7905f6f7987a2e82158fd795aa37eb45700053a8f159729b6e6056f80cc0b2` |
| critic-ci312: `python3 scripts/publication_guard.py tree` | 0 | publication-guard: the tree carries no placeholder and a final build record | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/07-publication.log`; `0276e41830b4da6da62d212ddb8a243dc7e082d39156d50c033411e0e1025322` |
| critic-ci312: `uv run pytest --collect-only -m stress -q` | 0 | 16/2221 tests collected (2205 deselected) in 1.87s | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/ci312/08-stress-collect.log`; `da656b8cfe8cc13459a621bc451ca8ae9f28543cbb89c063790658ad05cb86c2` |
| critic-mutation: `git rev-list --count HEAD` | 0 | 1 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/mutation/00-history.log`; `9869a1f704351f6e7f5af6f9ffc758eb0a85c33e5baf9806bb5ff035fcc54641` |
| critic-mutation: `git rev-parse 'HEAD^{tree}'` | 0 | f10e29c9790aecaf45866786912dd94c59aab6bc | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/mutation/00-tree.log`; `84a44a8f821981283ff47e4aaa660ff009ee89c75eac61be978fc523c06a04b1` |
| critic-mutation: `uv sync --locked --dev` | 0 |  + zipp==4.1.0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/mutation/01-sync.log`; `b29f635d46fb2f269e53548796cb64a5f42f5a37c1a42745d50e44ff50782519` |
| critic-mutation: `python3 --version` | 0 | Python 3.12.14 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/mutation/01-direct-python-version.log`; `f1c67c1448ff23fd0f52f688e6adf2c0bca784f816df3de9f6972f308180b782` |
| critic-mutation: `uv run python --version` | 0 | Python 3.12.14 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/mutation/01-python-version.log`; `d8166eb859451afd048d762dfaaad4460426fc96f41842f318ffba9898b43853` |
| critic-mutation: `uv run python scripts/build_wasm_payload.py` | 0 | wrote /Users/djourno/Downloads/PJM/.local/tmp/cp-26-ci/critic-mutation/reports/cp3b/payload.json | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/mutation/02-payload.log`; `4d6ce64d1b5b0cb86e6fd7e95d4d4c64a8d12c7d9ef01ccad869f6eccf7ac94d` |
| critic-mutation: `uv run pytest -q` | 0 | 2206 passed, 16 skipped; the 16 stress cases ran with the synthetic ledger row and changed preceding prose. | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/mutation/03-appended-suite.log`; `0451ee2a6ae9e30ec486d391053c80e5579de38b1005e7147c1bd1d57199515c` |
| critic-mutation: `uv run pytest tests/test_cp26_exposure_ledger.py::test_live_exposure_ledger_preserves_frozen_cp26_rows -q` | 1 | Expected negative control: 1 failed, specifically historical row preservation at test_cp26_exposure_ledger.py:16. | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/mutation/04-altered-row.log`; `0558f0be5f233c5e069dd6c205018e426ee2e2b0ded8a608e5ad02fb504a0850` |

The synthetic row contained no market information. The positive control also changed preceding prose. For the negative control I first restored the original ledger, then changed its first historical row identifier from `| 1 |` to `| 1 changed |`. The named preservation test failed on the expected row comparison, not on a setup or identity error. The original live-ledger bytes were restored in a `finally` block; their SHA-256 remains `375fef5d200c400b79840dcc9977ab3d63a95ed85af603c8add3b9a9210d98a6`. No scratch changes were committed.

## Static verification and evidence actually inspected

I read root `AGENTS.md`, `engineering-role.md` and templates §2. I inspected the entire candidate diff against main and each changed artifact, all real-monitor helpers/call sites and the marked assertions, the harness pins and identity loops, the two migrated historical identity tests, the unchanged workflow, the frozen ledger and its original Git object, and the canonical brief/contract. I read no program-state, Orchestrator, syllabus, Track A/C, Claude-memory or subsequent-checkpoint material. No market source was retrieved.

The final named static driver was `python3 /Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/review_static.py` (exit 0), SHA-256 `64f6cfac5a5892c712c758b03220f136e2b5957a978818f4731ac645d34eedcc`. Its exact Git commands and output hashes follow. Source reads were hashed and AST inspection independently confirmed decorator-only test changes.

| Actual command | Exit | Raw log / SHA-256 |
|---|---|---|
| `git rev-parse HEAD` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/head.log`; `1e11cbfa4a279b923e72f228c0615cfeacb3d80c5a8e157611b0d1827cecdea0` |
| `git status --porcelain` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/clean.log`; `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `git rev-parse 'HEAD^{tree}'` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/tree.log`; `27bbb7c23999d153e3a3d45396b56afec92ad7f13b83de2f2eafa0e3136fb543` |
| `git diff --name-status main 9b6a0c38edbdecee202c33fe610c7c4475cf7cfc` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/all-changed-paths.log`; `1dd71aea73117c5300a252a29ec5b3694ace33b4e85f98fb7f8c3ab81b46e129` |
| `git diff --name-only main 9b6a0c38edbdecee202c33fe610c7c4475cf7cfc` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/changed-name-only.log`; `f0bf07f2f02ff9af4604efb386849f3cbba32ead2aed9cd084ba2435a08e1873` |
| `git diff --stat main 9b6a0c38edbdecee202c33fe610c7c4475cf7cfc -- reports/ src/ data/ scripts/ .github/ pyproject.toml uv.lock AGENTS.md CLAUDE.md engineering-role.md orchestrator-role.md notebooklm-role.md docs/track-b/gauntlet-templates.md docs/track-b/backup-register.md docs/track-b/exposure-ledger.md 'capstone*.md' 'syllabus*.md' program-stage-sequence.md 'docs/track-b/*amendments.md' .claude/` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/forbidden-diff.log`; `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `git diff --exit-code main 9b6a0c38edbdecee202c33fe610c7c4475cf7cfc -- docs/track-b/evidence ':(exclude)docs/track-b/evidence/cp-26-ci/issued-brief.md' ':(exclude)docs/track-b/evidence/cp-26-ci/test-contract.md' ':(exclude)docs/track-b/evidence/cp-26/exposure-ledger-frozen.md'` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/earlier-evidence-diff.log`; `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `git show 61658c7:docs/track-b/exposure-ledger.md` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/historical-ledger.log`; `375fef5d200c400b79840dcc9977ab3d63a95ed85af603c8add3b9a9210d98a6` |
| `git show main:tests/conftest.py` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/main-conftest.log`; `ae50b3a26ff4a39235a1d0fb5665ca7b5ac51e0e39bc6d6534531b20b552aefd` |
| `git grep -n -F -e ae50b3a26ff4a39235a1d0fb5665ca7b5ac51e0e39bc6d6534531b20b552aefd -e 080759376f1d56b9ce991285cd37f5167746ac95 main -- docs/track-b/evidence` | 1 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/conftest-hash-reference.log`; `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `git grep -n -F tests/conftest.py main -- docs/track-b/evidence` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/conftest-path-references.log`; `2f491a9cf8a00781db92136ab98ad69ad2977a1ee0ff097789ae1ad8b7c3b06e` |
| `git show main:tests/test_cp26_monitor.py` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/test_cp26_monitor-main.log`; `7ddddfd576db79011703e9160c84925b9e30380e62b9e376d4a4bfdca02039f0` |
| `git show main:tests/test_cp26_supervision.py` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/test_cp26_supervision-main.log`; `59ee4a2e68e75914ba34ceb08a1d7276584a45cbc0892a168ba99a45a0613dfb` |
| `git show main:tests/test_cp26_ledger_liveness.py` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/static-final/test_cp26_ledger_liveness-main.log`; `319c4b657e6d7cc5bb25d91bb495dc5a3d8b8c71fdc2ecf3c293202b707969f6` |

`git grep` exit 1 above means neither the original conftest SHA-256 nor its full Git blob ID appears in main’s committed evidence. Its existing path references were inspected and are inspection records, tracebacks or path listings; none binds its bytes. The baseline SHA-256 was `ae50b3a26ff4a39235a1d0fb5665ca7b5ac51e0e39bc6d6534531b20b552aefd`, blob `080759376f1d56b9ce991285cd37f5167746ac95`. The candidate conftest additions only register the marker, apply the exact skip predicate and expose its reason in the unchanged quiet workflow output.

The scope diff contains exactly eleven files, all under `tests/` or the three new evidence paths. Existing evidence is unchanged. Reports, source, data, scripts, workflow, dependencies, anchors, amendment records, governance, agent configuration, backup register and the live ledger are unchanged. `src/cp26/harness.py` and `PINS` are unchanged.

The frozen evidence is 4,001 bytes, byte-identical to `61658c70520b880d844b1bb54af9973cf2851d9d:docs/track-b/exposure-ledger.md`; SHA-256 `375fef5d200c400b79840dcc9977ab3d63a95ed85af603c8add3b9a9210d98a6`, equal to the unchanged harness ledger pin. The new test compares the complete frozen table (including header/separator) with the live table prefix, preserving rows verbatim and in order while permitting later rows and changed preceding prose.

The complete historical-identity migrations are:

- `tests/test_cp26_r15.py::test_r15_authority_does_not_relabel_scientific_plan_or_parity`
- `tests/test_cp26_repair_contract.py::test_anchor_commit_and_landed_base_are_distinct_and_explicit`

Both resolve only the ledger key to the frozen copy through `tests/cp26_ledger_snapshot.py`; other identities, historical fingerprint keys and recorded hashes are preserved. The unchanged historical runtime harness still pins its scientific inputs; this maintenance authorizes no scientific rerun.

An early inventory search accidentally passed a literal `tests/test_cp26*` filename to rg (exit 2); the corrected `rg -g test_cp26*.py ... tests` exited 0. A read-only topology probe of already-removed `lead-ci313` exited 128; preparation was then verified from the supplied execution artifact as described below. Neither diagnostic failure is represented as a passing reproduction.

## Checked stress inventory

These fifteen functions collect as exactly sixteen cases. The SIGSTOP function contributes `[False]` and `[True]`; no other function is selected. Removing only `@pytest.mark.stress` from each of the three changed monitor modules reproduces its main bytes exactly, proving no body or assertion changed.

| Module under `tests/` | Function | Why it qualifies |
|---|---|---|
| test_cp26_monitor.py | test_outer_monitor_hard_death_retains_independent_failed_job_receipt | Launcher death after active accounting must retain independently observed completion and elapsed charge. |
| test_cp26_monitor.py | test_supervisor_hard_death_gets_independent_bound_ending_receipt | Live supervisor death must trigger watchdog termination and positive observed runtime. |
| test_cp26_monitor.py | test_registered_detached_worker_is_not_lost_when_parent_exits | Parent completion must trigger orphan detection and termination while the detached worker remains active. |
| test_cp26_supervision.py | test_sigstop_supervisor_stops_verified_worker_even_after_launcher_loss | Both parameter cases require stale-heartbeat takeover, worker termination and independent elapsed accounting. |
| test_cp26_supervision.py | test_supervisor_stopped_inside_ledger_lock_is_killed_before_receipt | A stalled lock must cause termination before a terminal receipt is issued. |
| test_cp26_supervision.py | test_stopped_watchdog_is_detected_by_supervisor | Shutdown after watchdog stoppage must remain within the declared exposure bound. |
| test_cp26_supervision.py | test_launcher_shutdown_receipts_workers_and_watchdog | Launcher termination must complete concurrent worker and watchdog shutdown. |
| test_cp26_supervision.py | test_launcher_enforces_when_both_accounting_loops_are_stopped | The launcher must take over after both accounting loops stop and independently charge terminal duration. |
| test_cp26_ledger_liveness.py | test_three_jobs_keep_fresh_supervision_with_full_future_history | Three concurrent monitors must retain freshness, sampler advancement and bounded lock telemetry. |
| test_cp26_ledger_liveness.py | test_wedged_supervisor_lock_still_gets_independent_ending_receipt | Real lock timeout must lie between the ledger and heartbeat deadlines, followed by independent termination. |
| test_cp26_ledger_liveness.py | test_supervisor_startup_accounting_wait_uses_declared_poll_cadence | The actual startup accounting wait must request the declared 0.2-second poll cadence. |
| test_cp26_ledger_liveness.py | test_duplicate_live_request_refuses_before_spawn_and_preserves_original_clock_and_receipt | A concurrent rejected replay must leave the original observer sequences advancing before normal completion. |
| test_cp26_ledger_liveness.py | test_fast_terminal_job_allows_read_only_late_launcher_binding_and_same_receipt | A patched CLI launch forces completion before launcher binding and requires the same receipt and elapsed charge. |
| test_cp26_ledger_liveness.py | test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history | Three busy owners plus an arriving admin must retain freshness, sampler advancement and bounded lock telemetry. |
| test_cp26_ledger_liveness.py | test_actual_search_accounting_timeout_aborts_without_fit_or_failed_trial_cache | A monitored child with a concurrent lock holder must time out before any fit or failed-trial cache write. |

The only other direct real-monitor test, `test_real_denied_detached_worker_never_reaches_computation`, stays unmarked: it asserts denial, absent computation and cleanup; its wait timeout is harness patience. The global real-monitor/CLI search found no omitted qualifying test, and synthetic/mock-only tests are unmarked. The independently collected sixteen node IDs match this inventory exactly.

## Lead raw artifacts independently verified

These are verified execution artifacts, distinct from commands I reran. I opened the raw outputs, recomputed every SHA-256 listed below, checked the candidate/tree identities, interpreter evidence and complete/removal fields, and inspected each relevant full-suite, selection and negative-control output. All bind the same candidate tree.

Preparation is evidenced by the supplied `validation-runner.py`, SHA-256 `9b80a18e06cbda9e2e1037a78de57041ae7e60a9f89c9477a3d3c33f3b3308d2`: `run_mode` calls `prepare` before creating results or starting a command; `prepare` archives the supplied candidate, creates one commit with the secret hooks, and asserts tree equality, one-commit history and clean state. The completed results show that preflight returned. No separate raw preparation stdout was retained for the removed copies, and I do not claim otherwise. I additionally read the still-running Lead mutation copy’s Git topology: one commit and exact tree `f10e29c9790aecaf45866786912dd94c59aab6bc`; its sole tracked difference was the intended live-ledger mutation. My two own copies’ one-commit topology and tree equality were directly checked before reproduction.

| Mode | Verified result | results.json SHA-256 |
|---|---|---|
| ci312 | Original run: uv Python 3.12.14; direct final guard interpreter unverified. Seven commands exit 0; 2190 passed / 32 skipped; all 16 stress skip reasons visible; exact 16-case collection. Complete=true; scratch removed=true. | `24694f825c982107cc8fae0daaefbc2cb1d25562d7ccec9707b7af64d204a427` |
| ci313 | Original run: uv Python 3.13.15; direct final guard interpreter unverified. Seven commands exit 0; 2190 passed / 32 skipped; all 16 stress skip reasons visible; exact 16-case collection. Complete=true; scratch removed=true. | `befbfd6ff01715083ccb0e173f643ebc3b62420707474d60f9794bf5068a175e` |
| local | Python 3.12.14, CI and RUN_STRESS absent: 2206 passed / 16 preexisting skips; the 16 stress cases ran. Complete=true; scratch removed=true. | `2b414c4f984b91e53d813ba3e5f026eb07110f77003f02e4f63301f5d10f42cc` |
| force | Python 3.12.14, CI=true RUN_STRESS=1: 16 passed, 1 unrelated module skip, 2205 deselected. Complete=true; scratch removed=true. | `b624f80f522c290076b859d6c2a6057dc3ecda726f39a46da05e9a5603a22d12` |
| mutation | Python 3.12.14, synthetic append and changed preceding prose: 2206 passed / 16 skips; historical-row alteration: expected exit 1 in the named preservation test. Complete=true; scratch removed=true. | `06ef00782068e83361e3a1883347e0398649c2a5d3bdfab32da7a2ba52e80e2b` |

The CI total includes sixteen preexisting skips for unavailable optional evidence/dependencies/history plus the sixteen stress cases. The force run’s unrelated module skip is the existing unavailable eccodes import, outside the selected stress inventory. All Lead scratch directories were independently observed absent after completion.

The following raw command records are preserved here so the result is durable without relying on a prose summary. Logs are rooted at `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/validation-final/`.

| Mode / actual command | Exit | Relative log | Verified SHA-256 |
|---|---|---|---|
| ci312: `uv sync --locked --dev` | 0 | `ci312/01-sync.log` | `f9c96ba3828c9d3c03fcaa70852812221240b39b65699b0bcd5019117006f050` |
| ci312: `uv run python scripts/build_wasm_payload.py` | 0 | `ci312/02-python.log` | `572bb8c8e7fe30a813b7a150691a2c0cf6eb08f1c8e8eb17f7ad6b139924d160` |
| ci312: `uv run pytest -q` | 0 | `ci312/03-pytest.log` | `39be4073c7534cffec70e9f4c109020b748d3212acc5a35d5b05fb80d329071e` |
| ci312: `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | `ci312/04-pytest.log` | `d422fbe2e481c669d2a194187dfb0c2645911525c10285beb12e2357a270487d` |
| ci312: `uv run python scripts/verify_release.py` | 0 | `ci312/05-python.log` | `b69996cb1e6d2b04eb0f3d50e3f0b8042b311f24afd9bf21d58358e7078e7e79` |
| ci312: `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | `ci312/06-pytest.log` | `7058e7bb6cb8f85b8bdfdde1b01a6e5f0c8c102358e0c76b3eec24b262ed2450` |
| ci312: `python3 scripts/publication_guard.py tree` | 0 | `ci312/07-tree.log` | `0276e41830b4da6da62d212ddb8a243dc7e082d39156d50c033411e0e1025322` |
| ci312: `uv run pytest --collect-only -m stress -q` | 0 | `ci312/08-collection.log` | `4fa0679cfc302533136b45eb2c92475b5c8f816c1e47aaaa00f6c8e8cf12759a` |
| ci313: `uv sync --locked --dev` | 0 | `ci313/01-sync.log` | `96b59b7d8c48f41d120368e26b66b4aeeac4dcccb688f557ac64d35ec1950bf7` |
| ci313: `uv run python scripts/build_wasm_payload.py` | 0 | `ci313/02-python.log` | `af35701118a3eb344ca4b579beb53874ee6a7288922cae5d4d03954f79e9506a` |
| ci313: `uv run pytest -q` | 0 | `ci313/03-pytest.log` | `e77f3994e2d2769fc4e0fdc983072b54eec2682be779537038a5a953f7113d79` |
| ci313: `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | `ci313/04-pytest.log` | `9b2377638cd5c1cbeabcc9b16e4072bece7b08cb2e15879d6243d07a47532d77` |
| ci313: `uv run python scripts/verify_release.py` | 0 | `ci313/05-python.log` | `b69996cb1e6d2b04eb0f3d50e3f0b8042b311f24afd9bf21d58358e7078e7e79` |
| ci313: `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | `ci313/06-pytest.log` | `d6db7245efd1ebf3edd201c879379c7a85118e658a2e12f355ca3c01d941b1c1` |
| ci313: `python3 scripts/publication_guard.py tree` | 0 | `ci313/07-tree.log` | `0276e41830b4da6da62d212ddb8a243dc7e082d39156d50c033411e0e1025322` |
| ci313: `uv run pytest --collect-only -m stress -q` | 0 | `ci313/08-collection.log` | `131ae27d6b1c0555a87659103e953a29114c2518dfebe82b09ed2e2a17ae1259` |
| local: `uv sync --locked --dev` | 0 | `local/01-sync.log` | `1320414b0981b5e96c535766c8d0ccbc97dc7a81cc4071fcf4125c7c2453dc35` |
| local: `uv run python scripts/build_wasm_payload.py` | 0 | `local/02-wasm.log` | `615160d122b6985759ba8855b6079b961e53e5154f03bff87f4652e3251f630f` |
| local: `uv run pytest -q` | 0 | `local/03-full-suite.log` | `8849bd6f568685b5c46d4933092ed2df62bab5cea81a433e03f06b689e1eeded` |
| force: `uv sync --locked --dev` | 0 | `force/01-sync.log` | `c1f4f0c94d65c55ce64f4952d1ca2379d44934b452acc55e68cf82bbaaa0ee69` |
| force: `uv run pytest -m stress -q` | 0 | `force/02-force-stress.log` | `874a674f80d06e41a5100220f9f9c74c342fdfdad492992b47a64acf352b817e` |
| mutation: `uv sync --locked --dev` | 0 | `mutation/01-sync.log` | `521ef936bab008d7c27cec7a643005e19af24ba74e65ad08e1bb5ae6768bd513` |
| mutation: `uv run python scripts/build_wasm_payload.py` | 0 | `mutation/02-wasm.log` | `08eb9ee26be4e9c05cd2af2955b7ff8f8c824b6ce8a16511869dc748467a4e95` |
| mutation: `uv run pytest -q` | 0 | `mutation/03-full-suite.log` | `df242c46ece8162e5e44512feadc41f4164fa4da93a14cce38f99efae1efc4b4` |
| mutation: `uv run pytest tests/test_cp26_exposure_ledger.py::test_live_exposure_ledger_preserves_frozen_cp26_rows -q` | 1 | `mutation/04-changed-row.log` | `d1c9cdd6964443e218d705d2507f4b2dd3bfb7b5ef96e4d81182a8397caf8bb1` |

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Stress marker: complete qualifying inventory, exact skip environment/reason, default execution, exact selection, unchanged bodies/assertions. | PASS | Fifteen functions / sixteen cases above; direct helper and CLI inventory, decorator-only byte comparisons, exact conftest predicate; independent CI skip/selection, Lead local default run and forced run. The unmarked real denial test has no timing assertion. |
| 2 | Living exposure ledger: historical frozen bytes and pin, live historical rows preserved verbatim/in order, prose/appends allowed, unchanged harness/PINS, every identity read migrated. | PASS | Exact historical Git-object comparison and SHA-256; new prefix-preservation test; two complete identity migrations listed above; unchanged source; independently reproduced positive/negative controls. |
| 3 | Scratch positive and negative controls, nothing committed, scratch removed afterwards. | PASS | Independently reran full suite after a synthetic append plus preceding-prose change: 2206 passed / 16 skipped. Changing a preexisting row produced the required named-test failure, exit 1. Original bytes restored. Lead’s matching controls and removed scratch are verified; my two prepared copies are intentionally left for the Lead’s required post-verdict cleanup, per assignment. |
| 4 | History-free single-commit candidate copies: seven CI steps on Python 3.12/3.13, quiet local Python 3.12 full suite with stress, forced stress under CI. | PASS | Direct copy count/tree checks for both independent copies; preparation execution artifact and direct Lead mutation topology check; fresh environments. Strict seven-step acceptance binds the independently version-checked CI 3.12 run and the corrected version-checked CI 3.13 run detailed below. Original Lead CI direct guards have unverified interpreters; verified local and force runs use uv. Reproductions were serialized after explicit quiet-machine release. |
| 5 | Test/new-evidence-only scope; protected artifacts unchanged; conftest only marker/skip after checking byte bindings. | PASS | Eleven-path diff; empty forbidden-path and earlier-evidence diffs; unchanged live ledger and harness/PINS; canonical anchor/brief/publication hashes checked; original conftest SHA/blob absent from committed evidence bindings. Its original fixture is unchanged. |
| 6 | One fresh focused Integration Critic from a clean detached exact candidate; items 1–5 checked; independent mutation and CI 3.12 reruns. | PASS | This review, exact candidate/tree, clean initial/final status, complete six-row verdict and both independent reproductions. No candidate edit or direct Git mutation. Isolation is cooperative. |

## Retained reproduction material and handoff

The two Lead-prepared copies and their fresh `.venv` environments remain for Lead cleanup after this verdict, exactly as instructed:

- `/Users/djourno/Downloads/PJM/.local/tmp/cp-26-ci/critic-ci312`
- `/Users/djourno/Downloads/PJM/.local/tmp/cp-26-ci/critic-mutation`

No other temporary repository, worktree or environment was created by this Critic. The detached checkout remains for Lead `critic-close`. The external verdict and per-command logs/drivers remain under `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/` as review evidence. Post-return reads: none.

## Corrected Python 3.13 seven-step evidence

The original Lead runner bound uv commands through `UV_PYTHON` but did not prepend its fresh environment to PATH. Its final direct `python3 scripts/publication_guard.py tree` therefore has an unverified interpreter in both original CI modes. Those raw records are preserved above, with that limitation. Strict Python 3.12 seven-step acceptance binds my independently version-checked run. Strict Python 3.13 seven-step acceptance binds the distinct corrected run below, rather than either original direct-guard result.

The supplied corrected execution artifact `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck.py`, SHA-256 `42c27f05645ef54d2bf32e090f88c430c05348d7a82e8fa05dab6a982c38789c`, prepends the fresh copy’s `.venv/bin` to PATH and verifies both direct and uv Python immediately after sync. I inspected that source and independently rehashed/opened every corrected raw log. This is Lead-run evidence, not another test sequence I claim to have executed. No candidate or original artifact changed.

The corrected results record candidate `9b6a0c38edbdecee202c33fe610c7c4475cf7cfc`, candidate and scratch tree `f10e29c9790aecaf45866786912dd94c59aab6bc`, scratch commit `505c8fdcbbddbbb668e1097dc55ae2538923b62e`, commit count `1`, empty initial tracked status, `CI=true`, `RUN_STRESS` absent and `UV_PYTHON=3.13`. Both interpreter observations are `Python 3.13.15`. All seven workflow commands exited 0 in the required order. The full suite had 2190 passed / 32 skipped, including the required 16 reasoned stress skips; CQR had 8 passed, WASM 15 passed, and release/publication checks passed. Stress collection again matched the exact 16-case inventory. The results report completion and scratch removal, and I independently observed the scratch path absent.

Corrected results: `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/results.json`, SHA-256 `3598e31ef66c8824986a290a999d38049b726eed3e2940437f68962003d0f320`.

| Actual corrected command | Exit | Raw log | Verified SHA-256 |
|---|---|---|---|
| `uv sync --locked --dev` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/01-workflow.log` | `935bf31d91c9af8f326b6026a5c0a573c2ce6e9538aa3758580fdca9d4fa6df6` |
| `python3 --version` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/01a-direct-version.log` | `7ea00df840c8e624bff08369bb67e5a89ad17f7e0a8447147ac134f93ba33031` |
| `uv run python --version` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/01b-uv-version.log` | `73e47872a1b8e90c4b7e65d37f111afd49c1dedac965cc50ce0a2abefdd8ae63` |
| `uv run python scripts/build_wasm_payload.py` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/02-workflow.log` | `bc0b99d9e4ee7c09d6bd2237f246027d4acb41e5edd18cb8e602c1cce06f6f1f` |
| `uv run pytest -q` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/03-workflow.log` | `38e3084534b077c34ee6db91f807eeee8f8c838ad66b616eb31cad9fc365bf2c` |
| `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/04-workflow.log` | `9b2377638cd5c1cbeabcc9b16e4072bece7b08cb2e15879d6243d07a47532d77` |
| `uv run python scripts/verify_release.py` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/05-workflow.log` | `b69996cb1e6d2b04eb0f3d50e3f0b8042b311f24afd9bf21d58358e7078e7e79` |
| `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/06-workflow.log` | `4449b5bd5681b688024e384efd382186100335db8ce5dd879049a2660668af2e` |
| `python3 scripts/publication_guard.py tree` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/07-workflow.log` | `0276e41830b4da6da62d212ddb8a243dc7e082d39156d50c033411e0e1025322` |
| `uv run pytest --collect-only -m stress -q` | 0 | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/ci313-interpreter-recheck/08-collection.log` | `a955651f73f18418e863ff1cc3258e7338998e098f5262b928340437781b6e20` |

## Final verification observations

Both independent copies remained single-commit repositories with the exact candidate tree and clean tracked state after reproduction; their configured hooks point to `/Users/djourno/Downloads/PJM/.githooks`. Their final read-only command records are in `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/copies-final-state.json`, SHA-256 `30818adeca5a99afe4ef2d50fc41255f3ce920bca7e713aae472c3b3e58c0fb1`. The mutation ledger was independently rehashed to the original pin after restoration. Both environments and temporary-root sentinels remain for Lead cleanup.

Quote fidelity was checked with `git show main:scripts/bar.py | python3 -I - check /Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/integration.md --source capstone_v21.md@9b6a0c38edbdecee202c33fe610c7c4475cf7cfc --source docs/track-b/evidence/cp-26-ci/issued-brief.md@9b6a0c38edbdecee202c33fe610c7c4475cf7cfc` (exit 0). Both complete quoted blocks appeared verbatim in their respective candidate sources. Raw output: `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/sealed-bar-check.log`, SHA-256 `e8de5b9997d23456d285bae9b5d4344cb55293977e93a24d7cc4bf9085732573`.

Final read-only state commands:

| Command | Exit | Observed output | Raw log / SHA-256 |
|---|---|---|---|
| `git rev-parse HEAD` | 0 | 9b6a0c38edbdecee202c33fe610c7c4475cf7cfc | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/sealed-final-head.log`; `1e11cbfa4a279b923e72f228c0615cfeacb3d80c5a8e157611b0d1827cecdea0` |
| `git status --porcelain` | 0 | (empty; clean) | `/Users/djourno/Downloads/PJM/.local/artifacts/cp-26-ci/critic-1/logs/sealed-final-clean.log`; `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
