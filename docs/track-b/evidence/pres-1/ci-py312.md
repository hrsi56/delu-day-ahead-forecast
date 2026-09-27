# PRES-1: clean Python 3.12 CI-equivalent run (brief §8; plan §12 E)

- **Candidate:** `9ae76f468cc9c3f6c6654261460fe5453186d1f8`
- **Where:** a clean detached worktree at that SHA,
  `.local/worktrees/pres-1/ci-1` (created for this run and removed afterwards). `git status
  --porcelain` was empty before and after, and `uv.lock` and `pyproject.toml` were unchanged.
- **Interpreter:** CPython 3.12.14, uv's managed build, installed under `.local/tools/python`.
  `UV_PYTHON=3.12` was set for every step, as `astral-sh/setup-uv` does with
  `python-version: "3.12"` in `.github/workflows/tests.yml`.
- **When:** 2026-09-27, on this Mac (arm64, Darwin 25.5.0). CI itself runs on `ubuntu-latest`; this
  is the same job on a different OS, not a CI run.

## The job's steps, in the workflow's order

| Step (from `.github/workflows/tests.yml`) | Exit | Observed |
|---|---|---|
| `uv sync --locked --dev` | 0 | the lock resolved as committed |
| `uv run python --version` | 0 | Python 3.12.14 |
| `uv run python scripts/build_wasm_payload.py` | 0 | payload built; MLflow warns once that the champion was saved under Python 3.13.15, as expected on 3.12 |
| `uv run pytest -q` | 0 | 733 passed, 7 skipped in 142.00 s |
| `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | 8 passed |
| `uv run python scripts/verify_release.py` | 0 | "PASS — every bound claim agrees on every surface; the static page fetches nothing" |
| `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | 15 passed (the bitwise model-identity gate) |

The local Python 3.13 environment gave the same suite result at the same tree: 733 passed,
7 skipped.
