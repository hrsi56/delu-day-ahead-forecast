# CP-17-probe Lead CI record — history-free single-commit copy

Runner: `.local/tmp/cp-17-probe/validation-runner.py` (CP-28's runner, adapted: offline from the first sync, `UV_OFFLINE=1` throughout; in CI mode `CP17_PROBE_PROJECT_ROOT` points at an absent folder, so the probe's local-only inputs are hidden as on a CI runner). Each mode: `git archive <candidate>` into `.local/tmp/cp-17-probe/`, `git init -b main`, the repository's `.githooks` installed, one commit whose tree equals the candidate's, an invalid `.git` sentinel at `<copy>/.local/tmp/.git`, a fresh copy-local `.venv`, `UV_PYTHON=3.12`, `UV_PYTHON_DOWNLOADS=never`, the project-local uv cache, `.venv/bin` first on PATH, credentials removed from the subprocess environment, `MLFLOW_DISABLE_TELEMETRY=true`, `DO_NOT_TRACK=1`. No retrieval.

## ci312 — CI=true, Python 3.12: the workflow's seven steps, then the stress collection

Candidate `4f1c0d7c08d2f51010279b75de566eb9e57e502e`, tree `beb5c04bf5e26fccebbdf1e727d26c53713d9606`; complete=True, scratch removed=True.

| step | command | exit | seconds | last line | log sha256 |
|---|---|---|---|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.725 |  + zipp==4.1.0 | `556dfd25a452f08d5c3a8b9bb2b55c56f8d001fd99fb1febe7e71337023e4c8f` |
| 01a-direct-version | `python3 --version` | 0 | 0.007 | Python 3.12.14 | `f1c67c1448ff23fd0f52f688e6adf2c0bca784f816df3de9f6972f308180b782` |
| 01b-uv-version | `uv run python --version` | 0 | 0.068 | Python 3.12.14 | `d8166eb859451afd048d762dfaaad4460426fc96f41842f318ffba9898b43853` |
| 02-python | `uv run python scripts/build_wasm_payload.py` | 0 | 84.84 | wrote /Users/djourno/Downloads/PJM/.local/tmp/cp-17-probe/lead-ci312/reports/cp3b/payload.json | `01edb79afa12146f232ac81e0c63a48f45302c456466d9f92df5286aac34647f` |
| 03-pytest | `uv run pytest -q` | 0 | 447.337 | 2256 passed, 38 skipped in 445.55s (0:07:25) | `1486f07377c9cf2b3f7dba9f2c4efdacea5abd8551de4a5928cdb18ca5bce656` |
| 04-pytest | `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | 0.6 | 8 passed in 0.02s | `d422fbe2e481c669d2a194187dfb0c2645911525c10285beb12e2357a270487d` |
| 05-python | `uv run python scripts/verify_release.py` | 0 | 1.039 | PASS — every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces | `b69996cb1e6d2b04eb0f3d50e3f0b8042b311f24afd9bf21d58358e7078e7e79` |
| 06-pytest | `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | 2.062 | 15 passed in 1.63s | `3ca84310e4747e612d4e6bfed67733382b7da26a87145d9af1fb19f06761de8e` |
| 07-tree | `python3 scripts/publication_guard.py tree` | 0 | 0.024 | publication-guard: the tree carries no placeholder and a final build record | `0276e41830b4da6da62d212ddb8a243dc7e082d39156d50c033411e0e1025322` |
| 08-collection | `uv run pytest --collect-only -m stress -q` | 0 | 2.793 | 17/2293 tests collected (2276 deselected) in 2.10s | `2b9bb5f666d7ea1dafd55b85742bc2070b0eed995c929e2959d8318b548b097c` |

## stress — CI unset, Python 3.12: `uv run pytest -m stress -q`

Candidate `4f1c0d7c08d2f51010279b75de566eb9e57e502e`, tree `beb5c04bf5e26fccebbdf1e727d26c53713d9606`; complete=True, scratch removed=True.

| step | command | exit | seconds | last line | log sha256 |
|---|---|---|---|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.354 |  + zipp==4.1.0 | `01be8d68fe3233f0f2cd5315e01ff7feae9d2d5976ea54a54864436046139fea` |
| 01a-direct-version | `python3 --version` | 0 | 0.006 | Python 3.12.14 | `f1c67c1448ff23fd0f52f688e6adf2c0bca784f816df3de9f6972f308180b782` |
| 01b-uv-version | `uv run python --version` | 0 | 0.065 | Python 3.12.14 | `d8166eb859451afd048d762dfaaad4460426fc96f41842f318ffba9898b43853` |
| 02-stress | `uv run pytest -m stress -q` | 0 | 266.013 | 17 passed, 1 skipped, 2276 deselected in 248.74s (0:04:08) | `0fc28a236105affcc6a9a0597901509bb185e6ca64e9898a671f5a13929004b6` |

## The probe's tests in each mode

- **ci312:** the probe's units and its committed-record recomputation ran and passed; the real-input tests skipped with "CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent", and the browser test with "the pinned Pyodide 0.28.0, Playwright 1.63.0 browsers and probe payloads (.local/, never committed) are absent" (from `03-pytest.log`). The stress collection lists the probe's browser test (17 stress tests).
- **stress:** 17 passed and 1 skipped; the run took 72 s longer than CP-28's stress run, the length of one browser fit.
- **The browser test alone,** in the Lead worktree at the candidate, CI unset: `pytest -p no:cacheprovider -m stress tests/cp17probe/test_probe_browser.py -rA` — `PASSED tests/cp17probe/test_probe_browser.py::test_one_browser_measurement_reproduces_the_committed_record`, 1 passed in 76.54 s (the rerun matched the committed Chromium record bit for bit).
- **The real-input tests,** in the Lead worktree with BLAS at one thread: 4 passed (A1 for 2026-09-06 bitwise equal to CP-26's stored forecast and selections; the payload embargo and its controls; the D−2 refusal; the boundary refusal).

