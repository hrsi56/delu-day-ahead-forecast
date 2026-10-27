# CP-17-probe Lead CI record — history-free single-commit copy

Runner: `.local/tmp/cp-17-probe/validation-runner.py` (CP-28's runner, adapted: offline from the first sync, `UV_OFFLINE=1` throughout; in CI mode `CP17_PROBE_PROJECT_ROOT` points at an absent folder, so the probe's local-only inputs are hidden as on a CI runner). Each mode: `git archive <candidate>` into `.local/tmp/cp-17-probe/`, `git init -b main`, the repository's `.githooks` installed, one commit whose tree equals the candidate's, an invalid `.git` sentinel at `<copy>/.local/tmp/.git`, a fresh copy-local `.venv`, `UV_PYTHON=3.12`, `UV_PYTHON_DOWNLOADS=never`, the project-local uv cache, `.venv/bin` first on PATH, credentials removed from the subprocess environment, `MLFLOW_DISABLE_TELEMETRY=true`, `DO_NOT_TRACK=1`. No retrieval.

This record is for the final candidate, `b4f2342`. The records for the earlier candidates are `lead-ci-attempt-1.md` (`4f1c0d7`, Integration attempt 1, FAIL on the report's account of the deviation) and `lead-ci-attempt-2.md` (`b242aa2`, attempt 2, FAIL on a member count in the report). All three candidates differ only in `reports/cp17-probe/report.md` and files under `docs/track-b/evidence/cp-17-probe/`.

## ci312 — CI=true, Python 3.12: the workflow's seven steps, then the stress collection

Candidate `b4f23422c60e40fa8f0d3f523c28605f5451d589`, tree `7c6631e1586821ad3fae8a634f223de4e34fa9ba`; complete=True, scratch removed=True.

| step | command | exit | seconds | last line | log sha256 |
|---|---|---|---|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.156 |  + zipp==4.1.0 | `e91621b08e787999ed1b66bff28ba83d74ac3a86877c28189e22a489d76426e3` |
| 01a-direct-version | `python3 --version` | 0 | 0.006 | Python 3.12.14 | `f1c67c1448ff23fd0f52f688e6adf2c0bca784f816df3de9f6972f308180b782` |
| 01b-uv-version | `uv run python --version` | 0 | 0.037 | Python 3.12.14 | `d8166eb859451afd048d762dfaaad4460426fc96f41842f318ffba9898b43853` |
| 02-python | `uv run python scripts/build_wasm_payload.py` | 0 | 69.778 | wrote /Users/djourno/Downloads/PJM/.local/tmp/cp-17-probe/lead-ci312/reports/cp3b/payload.json | `a962b523682b1eb25f34dead06807f9bc85d647f3e0d3765c9d8eabb9924f5a9` |
| 03-pytest | `uv run pytest -q` | 0 | 436.166 | 2256 passed, 38 skipped in 434.85s (0:07:14) | `abd977c6ad33f3df4e1ef22d7e9dd5ec79de9e999eea6b815bdaba653f428491` |
| 04-pytest | `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | 0.419 | 8 passed in 0.02s | `d422fbe2e481c669d2a194187dfb0c2645911525c10285beb12e2357a270487d` |
| 05-python | `uv run python scripts/verify_release.py` | 0 | 0.987 | PASS — every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces | `b69996cb1e6d2b04eb0f3d50e3f0b8042b311f24afd9bf21d58358e7078e7e79` |
| 06-pytest | `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | 1.976 | 15 passed in 1.56s | `5cdb0e721318d37fb7027b5650778c1676a4333cf125f3bf7f9ab98619033273` |
| 07-tree | `python3 scripts/publication_guard.py tree` | 0 | 0.024 | publication-guard: the tree carries no placeholder and a final build record | `0276e41830b4da6da62d212ddb8a243dc7e082d39156d50c033411e0e1025322` |
| 08-collection | `uv run pytest --collect-only -m stress -q` | 0 | 2.45 | 17/2293 tests collected (2276 deselected) in 1.82s | `a43a0891fe7a992dbb533ade0fa011842d509429ae6e6b367b69fb157ea03f42` |

## stress — CI unset, Python 3.12: `uv run pytest -m stress -q`

Candidate `b4f23422c60e40fa8f0d3f523c28605f5451d589`, tree `7c6631e1586821ad3fae8a634f223de4e34fa9ba`; complete=True, scratch removed=True.

| step | command | exit | seconds | last line | log sha256 |
|---|---|---|---|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.076 |  + zipp==4.1.0 | `0cef3ea291b7d0ac0b8df54dc0b4125ccfb652ea04604dd4c362fe3ce3272176` |
| 01a-direct-version | `python3 --version` | 0 | 0.006 | Python 3.12.14 | `f1c67c1448ff23fd0f52f688e6adf2c0bca784f816df3de9f6972f308180b782` |
| 01b-uv-version | `uv run python --version` | 0 | 0.037 | Python 3.12.14 | `d8166eb859451afd048d762dfaaad4460426fc96f41842f318ffba9898b43853` |
| 02-stress | `uv run pytest -m stress -q` | 0 | 264.288 | 17 passed, 1 skipped, 2276 deselected in 246.36s (0:04:06) | `5fc735f3210fc81be7f78ebfa212cd2ca8a90a89db4f22ed48c31684f234c1d0` |

## The probe's tests in each mode

- **ci312:** the probe's units and its committed-record recomputation ran and passed. Its local-only tests skipped with their stated reasons (`03-pytest.log`):

  - `SKIPPED [1] tests/cp17probe/test_probe_browser.py: the pinned Pyodide 0.28.0, Playwright 1.63.0 browsers and probe payloads (.local/, never committed) are absent`
  - `SKIPPED [1] tests/cp17probe/test_probe_real_inputs.py:46: CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent`
  - `SKIPPED [1] tests/cp17probe/test_probe_real_inputs.py:59: CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent`
  - `SKIPPED [1] tests/cp17probe/test_probe_real_inputs.py:71: CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent`
  - `SKIPPED [1] tests/cp17probe/test_probe_real_inputs.py:85: CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent`

- **stress:** 17 passed and 1 skipped. The skip is collection-time and unrelated: `tests/cp20/test_gfs_eccodes.py:11: could not import 'eccodes'` (`pytest --co -m stress -rs`). So the probe's browser test ran and passed in this mode.
- **At the first candidate `4f1c0d7`,** the browser test alone (`pytest -p no:cacheprovider -m stress tests/cp17probe/test_probe_browser.py -rA`) passed in 76.54 s, and the four real-input tests passed with BLAS at one thread; neither the tests nor the code they exercise changed since.

