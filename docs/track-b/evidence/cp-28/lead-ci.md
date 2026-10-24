# CP-28 Lead CI record — history-free single-commit copy

Runner: `.local/artifacts/cp-28/validation-runner.py` (CP-26-CI's runner, adapted). Each mode: `git archive <candidate>` into `.local/tmp/cp-28/`, `git init -b main`, the repository's `.githooks` installed, one commit whose tree equals the candidate's, an invalid `.git` sentinel at `<copy>/.local/tmp/.git`, a fresh copy-local `.venv`, `UV_PYTHON=3.12`, `UV_PYTHON_DOWNLOADS=never`, the project-local uv cache, `UV_OFFLINE=1` after the sync, `.venv/bin` first on PATH, credentials removed from the subprocess environment, `MLFLOW_DISABLE_TELEMETRY=true`, `DO_NOT_TRACK=1`. No retrieval.

## ci312 — CI=true, Python 3.12: the workflow's seven steps, then the stress collection

Candidate `91c8aab2793f52bdf110542308f5076b653c889d`, tree `fe733e14404c11bda13d302fcf57a298587a844f`; complete=True, scratch removed=True.

| step | command | exit | seconds | last line | log sha256 |
|---|---|---|---|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 2.556 |  + zipp==4.1.0 | `3376a3f315525dc17dab08c0b34fd2e1bdf743ceb727f1299c00030a54cfeaa1` |
| 01a-direct-version | `python3 --version` | 0 | 0.007 | Python 3.12.14 | `f1c67c1448ff23fd0f52f688e6adf2c0bca784f816df3de9f6972f308180b782` |
| 01b-uv-version | `uv run python --version` | 0 | 0.046 | Python 3.12.14 | `d8166eb859451afd048d762dfaaad4460426fc96f41842f318ffba9898b43853` |
| 02-python | `uv run python scripts/build_wasm_payload.py` | 0 | 79.455 | wrote /Users/djourno/Downloads/PJM/.local/tmp/cp-28/lead-ci312/reports/cp3b/payload.json | `e50720dfd292105ce072671fff08f1f0d1c1c5632229c8bcd6e6f90352f6d662` |
| 03-pytest | `uv run pytest -q` | 0 | 450.488 | 2234 passed, 33 skipped in 448.95s (0:07:28) | `d2fd2d21136f80ab5668c9e9723de1622d375594d33521261661aaea93e3e9e3` |
| 04-pytest | `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | 0.588 | 8 passed in 0.02s | `d422fbe2e481c669d2a194187dfb0c2645911525c10285beb12e2357a270487d` |
| 05-python | `uv run python scripts/verify_release.py` | 0 | 1.03 | PASS — every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces | `b69996cb1e6d2b04eb0f3d50e3f0b8042b311f24afd9bf21d58358e7078e7e79` |
| 06-pytest | `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | 2.09 | 15 passed in 1.66s | `5b52cb0ac5c6771ac8746ce7c6edcc275ebf01f6029957943d5ed56159529aa6` |
| 07-tree | `python3 scripts/publication_guard.py tree` | 0 | 0.024 | publication-guard: the tree carries no placeholder and a final build record | `0276e41830b4da6da62d212ddb8a243dc7e082d39156d50c033411e0e1025322` |
| 08-collection | `uv run pytest --collect-only -m stress -q` | 0 | 2.672 | 16/2266 tests collected (2250 deselected) in 2.02s | `e03d77bc44a122e732fc768a67ad664fb92f216912d135511d64f76ae24c0dcc` |

## stress — CI unset, Python 3.12: `uv run pytest -m stress -q`

Candidate `91c8aab2793f52bdf110542308f5076b653c889d`, tree `fe733e14404c11bda13d302fcf57a298587a844f`; complete=True, scratch removed=True.

| step | command | exit | seconds | last line | log sha256 |
|---|---|---|---|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.623 |  + zipp==4.1.0 | `9a4056bc881ff0f5ebe5f73eb42a505ef30cf6f2503ac99ff2b6af61d6e581ce` |
| 01a-direct-version | `python3 --version` | 0 | 0.006 | Python 3.12.14 | `f1c67c1448ff23fd0f52f688e6adf2c0bca784f816df3de9f6972f308180b782` |
| 01b-uv-version | `uv run python --version` | 0 | 0.061 | Python 3.12.14 | `d8166eb859451afd048d762dfaaad4460426fc96f41842f318ffba9898b43853` |
| 02-stress | `uv run pytest -m stress -q` | 0 | 195.222 | 16 passed, 1 skipped, 2250 deselected in 176.91s (0:02:56) | `1b239389c4b2cd1b1b5c45935740de85b82d5b58e76c987b6384526aa908f244` |

## Earlier attempt, preserved

On candidate `67e34498c1a299153f10495ae2a2787649d87720` the full suite failed one test, `tests/cp28/test_cp28_pipeline.py::test_report_and_packet_render_from_synthetic_results`: the report's fallback-date line read CP-26's committed daily table, which that synthetic tree lacks. (1 failed, 2233 passed, 33 skipped in 457.74s (0:07:37)) The fix (`91c8aab`) makes the line say the table is absent; the committed report is unchanged. Its scratch copy was then removed by hand (a Finder `.DS_Store` reappeared during cleanup). The same race stopped the first run on `91c8aab` after all ten ci312 steps had exited 0 (recorded above, with `cleanup_note`) and before its stress mode; the runner now retries the removal, and the stress mode ran on its own.
