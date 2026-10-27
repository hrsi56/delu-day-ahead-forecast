# CP-17-probe Lead CI record — history-free single-commit copy

Runner: `.local/tmp/cp-17-probe/validation-runner.py` (CP-28's runner, adapted: offline from the first sync, `UV_OFFLINE=1` throughout; in CI mode `CP17_PROBE_PROJECT_ROOT` points at an absent folder, so the probe's local-only inputs are hidden as on a CI runner). Each mode: `git archive <candidate>` into `.local/tmp/cp-17-probe/`, `git init -b main`, the repository's `.githooks` installed, one commit whose tree equals the candidate's, an invalid `.git` sentinel at `<copy>/.local/tmp/.git`, a fresh copy-local `.venv`, `UV_PYTHON=3.12`, `UV_PYTHON_DOWNLOADS=never`, the project-local uv cache, `.venv/bin` first on PATH, credentials removed from the subprocess environment, `MLFLOW_DISABLE_TELEMETRY=true`, `DO_NOT_TRACK=1`. No retrieval.

This record is for the second candidate, `b242aa2` (Integration attempt 2, FAIL on a member count in the report). The record for the first candidate, `4f1c0d7` (Integration attempt 1, FAIL on the report's account of the deviation), is `lead-ci-attempt-1.md`; the two candidates differ only in `reports/cp17-probe/report.md` and two evidence files.

## ci312 — CI=true, Python 3.12: the workflow's seven steps, then the stress collection

Candidate `b242aa2923a4a3055ddc8c2654689ee9b783607d`, tree `962274935c45ae2aed713239aa2279cf98da595c`; complete=True, scratch removed=True.

| step | command | exit | seconds | last line | log sha256 |
|---|---|---|---|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.638 |  + zipp==4.1.0 | `8ab8bb393551c6af85fc890555325b4bbe376a3f2c95bbddac87846015f2ed2d` |
| 01a-direct-version | `python3 --version` | 0 | 0.006 | Python 3.12.14 | `f1c67c1448ff23fd0f52f688e6adf2c0bca784f816df3de9f6972f308180b782` |
| 01b-uv-version | `uv run python --version` | 0 | 0.04 | Python 3.12.14 | `d8166eb859451afd048d762dfaaad4460426fc96f41842f318ffba9898b43853` |
| 02-python | `uv run python scripts/build_wasm_payload.py` | 0 | 75.821 | wrote /Users/djourno/Downloads/PJM/.local/tmp/cp-17-probe/lead-ci312/reports/cp3b/payload.json | `8f7acae0535b455d402e01bcac6173af287878cd7dbda6f39f1fcb49bd44b963` |
| 03-pytest | `uv run pytest -q` | 0 | 451.762 | 2256 passed, 38 skipped in 449.85s (0:07:29) | `43dcccd3e2275ed7d2ea2a63ad8e2abef904c0788b052153758c9583a8100983` |
| 04-pytest | `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | 0.774 | 8 passed in 0.03s | `4e844fdf7b72be48aa0db69931fe8c85e47ad85cbef87bef63830c89da1cc63b` |
| 05-python | `uv run python scripts/verify_release.py` | 0 | 1.325 | PASS — every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces | `b69996cb1e6d2b04eb0f3d50e3f0b8042b311f24afd9bf21d58358e7078e7e79` |
| 06-pytest | `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | 2.763 | 15 passed in 2.17s | `3a9f81f7f8f852d3cb5803630686075e1fcaa50d032e5f31002f73bc0d95649d` |
| 07-tree | `python3 scripts/publication_guard.py tree` | 0 | 0.027 | publication-guard: the tree carries no placeholder and a final build record | `0276e41830b4da6da62d212ddb8a243dc7e082d39156d50c033411e0e1025322` |
| 08-collection | `uv run pytest --collect-only -m stress -q` | 0 | 3.028 | 17/2293 tests collected (2276 deselected) in 2.25s | `9b697137bb007d069ad6426987afc17b4e6df4de4c9c83d0c0c5a7dead974cfb` |

## stress — CI unset, Python 3.12: `uv run pytest -m stress -q`

Candidate `b242aa2923a4a3055ddc8c2654689ee9b783607d`, tree `962274935c45ae2aed713239aa2279cf98da595c`; complete=True, scratch removed=True.

| step | command | exit | seconds | last line | log sha256 |
|---|---|---|---|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.381 |  + zipp==4.1.0 | `7a7212fdd64a567a562954f673b211ad6dfa7e6814e40ec6b64b1957aaa8e34a` |
| 01a-direct-version | `python3 --version` | 0 | 0.007 | Python 3.12.14 | `f1c67c1448ff23fd0f52f688e6adf2c0bca784f816df3de9f6972f308180b782` |
| 01b-uv-version | `uv run python --version` | 0 | 0.042 | Python 3.12.14 | `d8166eb859451afd048d762dfaaad4460426fc96f41842f318ffba9898b43853` |
| 02-stress | `uv run pytest -m stress -q` | 0 | 294.562 | 17 passed, 1 skipped, 2276 deselected in 276.13s (0:04:36) | `dd09b27c43867a914c1813dbd847e230e66aa310a75242a19ceea375187abe05` |

## The probe's tests in each mode

- **ci312:** the probe's units and its committed-record recomputation ran and passed. Its local-only tests skipped with their stated reasons (`03-pytest.log`):

  - `SKIPPED [1] tests/cp17probe/test_probe_browser.py: the pinned Pyodide 0.28.0, Playwright 1.63.0 browsers and probe payloads (.local/, never committed) are absent`
  - `SKIPPED [1] tests/cp17probe/test_probe_real_inputs.py:46: CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent`
  - `SKIPPED [1] tests/cp17probe/test_probe_real_inputs.py:59: CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent`
  - `SKIPPED [1] tests/cp17probe/test_probe_real_inputs.py:71: CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent`
  - `SKIPPED [1] tests/cp17probe/test_probe_real_inputs.py:85: CP-26's local-only stored state (evidence/cp-26 extract and fit cache) is absent`

- **stress:** 17 passed and 1 skipped. The skip is collection-time and unrelated: `tests/cp20/test_gfs_eccodes.py:11: could not import 'eccodes'` (`pytest --co -m stress -rs` at the candidate). So the probe's browser test ran and passed in this mode.
- **At the first candidate `4f1c0d7`,** the browser test alone (`pytest -p no:cacheprovider -m stress tests/cp17probe/test_probe_browser.py -rA`) passed in 76.54 s, and the four real-input tests passed with BLAS at one thread; neither the tests nor the code they exercise changed since.

