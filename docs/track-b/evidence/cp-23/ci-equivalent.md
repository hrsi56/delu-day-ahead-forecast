# CP-23 — CI-equivalent run at the final candidate

**What ran.** The steps of `.github/workflows/tests.yml`, executed locally. Nothing is pushed, so GitHub CI
does not run for a local candidate.

- **Where:** a clean detached worktree (`.local/worktrees/cp-23/ci`, created and removed by this
  checkpoint) at the final candidate `f9a737eb2bb8ccdb93c0de5cf1449630ee246e90`, 2026-10-04.
- **Environment:** the project environment. It holds the root lock's packages plus the seven test-only
  reference packages, and the default suite imports none of those.

| Step (as in the workflow) | Command | Result |
|---|---|---|
| Browser payload | `python scripts/build_wasm_payload.py` | exit 0; writes only ignored files |
| Full suite | `python -m pytest -q -p no:cacheprovider` | exit 0 — **1363 passed, 8 skipped** in 206.95 s |
| Cross-surface agreement, zero runtime calls | `python scripts/verify_release.py` | exit 0 — "PASS — every bound claim agrees on every surface; the static page fetches nothing" |
| WASM identity gate and CQR fixture | `python -m pytest -q tests/test_22_wasm_equivalence.py tests/test_10_cqr_order_statistic.py` | exit 0 — 23 passed |
| Published MLflow export | `python scripts/mlflow_export.py --check` | exit 0 — "the committed export is current" |

The worktree's `git status --porcelain` was empty after every step. The publication guard step runs only on
`main` and does not apply to a candidate branch.

The independent Integration Critic reran the full suite at the same candidate, with the same counts (1,363
passed, 8 skipped) (`integration.md`).
