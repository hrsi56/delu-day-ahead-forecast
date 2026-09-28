# PRES-1 W3/W5 repair: checks before independent review

Code candidate: `1d80bbdb89c1eee824c6f5acddba45b0bb5a68df`. Date: 2026-09-28. The next evidence-only commit adds this record; it does not change the tested artifact. These are Lead checks, not an independent PASS.

## Full suites and CI-equivalent execution

Local Python 3.13.15: `PATH=/Users/djourno/Downloads/PJM/.venv/bin:$PATH PYTHONPATH=src python3 .local/tmp/pres-1/nocreds.py /Users/djourno/Downloads/PJM/.venv/bin/python -m pytest -q`, from the Lead checkout (wrapper path resolved against project root): **944 passed, 7 skipped, 123.39 s**, exit 0. The environment is reused read-only; imports resolve to this checkout's `src`. The first run lacked the environment's bin directory on PATH: 943 passed, 7 skipped, one `marimo` launcher failure. Correcting PATH passed all 20 test_19 cases and then the complete suite above. No repository fix was needed for that launcher failure.

Clean detached `.local/worktrees/pres-1/ci-7`, same SHA, Python 3.12.14. `uv sync --locked --dev` exited 0; every applicable step in `.github/workflows/tests.yml` followed. This is a macOS CI-equivalent execution, not an Ubuntu CI claim. All test processes had credential-like variables removed without printing them. Pinned dependency files were unchanged; no new dependencies. Temporary files, cache and runtime were under project `.local/`.

| Command | Exit | Observation |
|---|---:|---|
| `uv run python --version` | 0 | Python 3.12.14 |
| `uv run python scripts/build_wasm_payload.py` | 0 |   fixture:  54 days / 1296 rows (4 fail-closed) / regimes ['crisis', 'dst-fall-back', 'dst-spring-forward', 'post-crisis (holdout)', 'post-crisis (holidays, bridge days)', 'pre-crisis']; wrote /Users/djourno/Downloads/PJM/.local/worktrees/pres-1/ci-7/reports/cp3b/payload.json |
| `uv run pytest -q` | 0 | ..............                                                           [100%]; 944 passed, 7 skipped in 125.71s (0:02:05) |
| `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | ........                                                                 [100%]; 8 passed in 0.01s |
| `uv run python scripts/verify_release.py` | 0 | ; PASS — every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces |
| `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | ...............                                                          [100%]; 15 passed in 1.08s |
| `make verify` | 0 | ; PASS — every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces |
| `make lint-publication` | 0 | templates: 0 finding(s); PASS — the reading path and the template sources meet the standard's §4 and §5 rules |
| `uv run python scripts/mlflow_export.py --check` | 0 | 2026/09/28 23:14:19 INFO mlflow.agent.hint: Load the `instrumenting-with-mlflow-tracing` skill at /Users/djourno/Downloads/PJM/.local/worktrees/pres-1/ci-7/.venv/lib/python3.12/site-packages/mlflow/assistant/skills/instrumenting-with-mlflow-tracing/SKILL.md before writing any tracing code; it ships with this MLflow install. Set MLFLOW_DISABLE_AGENT_HINT=1 to silence this.; the committed export is current |
| `uv run python scripts/mlflow_publish.py --dry-run` | 0 | 2026/09/28 23:14:21 INFO mlflow.agent.hint: Load the `instrumenting-with-mlflow-tracing` skill at /Users/djourno/Downloads/PJM/.local/worktrees/pres-1/ci-7/.venv/lib/python3.12/site-packages/mlflow/assistant/skills/instrumenting-with-mlflow-tracing/SKILL.md before writing any tracing code; it ships with this MLflow install. Set MLFLOW_DISABLE_AGENT_HINT=1 to silence this.; dry run: 23 runs, 6928 metric points, 55 artifacts; outbound scan clean; export current at 1d80bbdb89c1 |
| `uv run python scripts/rebuild_presentation.py` | 0 | cross-surface agreement and zero-fetch checks: ok (0.5 s); rebuilt every presentation surface in 10.2 s |
| `git status --porcelain=v1` | 0 | Empty stdout: clean tree after rebuild |
| `python3 scripts/publication_guard.py tree` | 1 | Expected pre-F4 refusal: final: false; this CI step is main-only |

Seven skips remain the existing deliberate exclusions; no research replay was enabled. The payload command reported the expected saved-model Python 3.13 / runtime 3.12 warning, and the identity gate passed. HEAD remained unchanged; status was empty before/after the rebuild. The checkpoint-created CI checkout was removed after this record, retaining logs below.

## Browser, links and cold readers

`check_reader_paths.py release docs/index.html --shots <root>/.local/artifacts/presentation/repair-w3-w5 --out reports/presentation/release-checks/2026-09-28-w3-w5-s10.json` exited 0, `passed: true`: all eleven views and four engine accessibility-tree checks passed, with keyboard, touch, contrast and zoom checks. Engines: Chrome 153 and Playwright WebKit 26.6. No real Safari, iPhone or screen reader used. The Lead also inspected the fresh desktop screen showing v3 limitations → dated decision → evidence → disclosures. Final visual approval remains delegated to the Orchestrator.

`check_links.py` exited 0, no failed destinations; result `reports/cp3/link_check.json`. The existing two-reader §11 record remains `cold-reader-check.md`. The first 95,668 bytes through the opening, lineage and comparison, before the chapters, are identical to the reviewed `49cc9ac` page: SHA-256 `0bd0a11cd7096a69ef1f0fe3570302a526adfb386e6a8d2b5a59a23dcf310659`. These are the placements used for answers 1–5. Chapter wording is unchanged; only the evidence row moves after its decision. This is explicit continued applicability of the prior cold read, not a new human/agent cold read. New §10 measurements independently pass.

The W12 demo sources/card inputs and bundle are unchanged by this repair; the prior four-engine/viewport cold-start record remains applicable. F4 will rebuild the bundle with verified links and requires fresh final checks.

## Auth and controls

`authentication-correction.md` and `mlflow-precheck-corrected-2026-09-28.json` record the fresh authenticated MLflow GET: HTTP 200, expected experiment matched, no network writes, unchanged stored credentials. The unrelated account-API 403 is preserved as historical evidence and does not establish an invalid token.

Focused tests 34/36/38: **76 passed**. New controls exercise decision-date counts 5/7/8, policy permutation, corrupted count/first flags, earlier passing source and simultaneous decisions; actual evidence-row order and misplaced-row failures; correct MLflow read endpoint, redirect refusal, missing/wrong identity/error handling and safe logging. The full suite includes these controls.

## Retained local reproduction artifacts

- `.local/tmp/pres-1/repair-suite313.log` — SHA-256 `3702a3cea8f78744d2af3e42c405dc6ff534ca4816d88518c474f9c8cf2a04e3`.
- `.local/tmp/pres-1/repair-suite313-corrected.log` — SHA-256 `7d419e3b68b8ce90057678d82583da81ce0b256e21e3190f303bfe3e821d596a`.
- `.local/tmp/pres-1/repair-release.log` — SHA-256 `8a072e3c20e443a3a5f8dbdc4a17c1ea3be7614e2d8c081d5e09c764359011c9`.
- `.local/tmp/pres-1/repair-links.log` — SHA-256 `1fd52d8d88a84f8c716efa643db3b0c6c8760f7d8e113209436bc8811c86d11b`.
- `.local/tmp/pres-1/ci7-sync.log` — SHA-256 `1f3911a9f7790fcf35eaf034dcefb593b44b97b98d2a52bbb9ef98ec0a4d0be3`.
- `.local/tmp/pres-1/run-ci7.py` — SHA-256 `a5c58fb940cbebc7f744de61126978d965c30fda51d4d3b8314ee45e845cd744`.
- `.local/tmp/pres-1/ci7/results.json` — SHA-256 `366057dbe4a0bb68c0627f5c7b8abbcc164b1bfab1552a3d128bc8122eeead33`.
- `.local/tmp/pres-1/ci7/1.log` — SHA-256 `4c3569f5da09975434dd9fd9a91fadbc4367a91d8f3c3fab59e9241ab9ee4bd8`.
- `.local/tmp/pres-1/ci7/10.log` — SHA-256 `7d126130a7dd44e2a21eba75950d2d2bf8a44465f066a785c6a97d610916f598`.
- `.local/tmp/pres-1/ci7/11.log` — SHA-256 `8e0743034a62b29f1674dbca8f152fb4f74d0f5c89084f2e5b60b9d614270dc2`.
- `.local/tmp/pres-1/ci7/12.log` — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `.local/tmp/pres-1/ci7/13.log` — SHA-256 `5ecdd2cccfa4eeba12f0ca0c44bfef4c026b13ec143feeb7ce549f5ebf54d21b`.
- `.local/tmp/pres-1/ci7/2.log` — SHA-256 `82b5fbcfecf56c2c27339a017079c2dc141e0c1fd69eeb5b3f12c17307b3f8d4`.
- `.local/tmp/pres-1/ci7/3.log` — SHA-256 `bd75b382ddb7ea1ed882be06bc3c0c7a2558713e8c3aadc5f34928f490386b1b`.
- `.local/tmp/pres-1/ci7/4.log` — SHA-256 `71288863ec9567395a647dd0c8fbf0e2048bee72283202612ad6f90a7a526ef3`.
- `.local/tmp/pres-1/ci7/5.log` — SHA-256 `3a3b2cb0f48f694bb0518dcce770634f8b39392be5f691603e156104ed6309bf`.
- `.local/tmp/pres-1/ci7/6.log` — SHA-256 `5d7a346f561b984c9a88eec17d5cd0552a18fd1d8f53c5bab363e29a4eeff852`.
- `.local/tmp/pres-1/ci7/7.log` — SHA-256 `7b3414fbfa2424e47b19c3bd407fcbfe6efd87410e59258d05ac25aa34b1502b`.
- `.local/tmp/pres-1/ci7/8.log` — SHA-256 `869ba42374b692ea4e3df8ac31b7557c3b063d7612029d893545e30e5b7e59b7`.
- `.local/tmp/pres-1/ci7/9.log` — SHA-256 `f90f1474e9890c2436b31bc6dffe2d569f0e8199ccc036bb4130ad83407c2283`.
