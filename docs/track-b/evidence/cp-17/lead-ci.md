# Lead CI — CP-17 (history-free single-commit copy)

Candidate: `ca874204e768fdb2539f9c1e07d87b524c95c7db`. Runner: `.local/artifacts/cp-17/ci-runner.py lead <sha> ci312 stress`
(CP-17-probe's runner, adapted): `git archive` of the candidate into `.local/tmp/cp-17/lead-<mode>/`, one commit with
the same tree (checked), a fresh `.venv` synced offline from the project-local uv cache, the workflow's seven steps with
`CI=true` and Python 3.12 (local-only inputs hidden: `CP17_PROJECT_ROOT` points nowhere), then `pytest -m stress` with CI
unset (local inputs and runtimes visible). The copies were removed afterwards. The one stress skip is
`tests/cp20/test_gfs_eccodes.py` (no `eccodes` module), unrelated to CP-17. This is the Lead's own check, not the review.

## ci312 (Python 3.12; tree `cabbd2f9f56698ac968f86bf2d107bcd7f05cc9b`; complete True; copy removed True)

| Step | Command | Exit | Seconds | Log SHA-256 | Last line |
|---|---|---:|---:|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.5 | `8ab5be03e84c5383…` |  + zipp==4.1.0 |
| 01a-direct-version | `python3 --version` | 0 | 0.0 | `f1c67c1448ff23fd…` | Python 3.12.14 |
| 01b-uv-version | `uv run python --version` | 0 | 0.0 | `d8166eb859451afd…` | Python 3.12.14 |
| 02-python | `uv run python scripts/build_wasm_payload.py` | 0 | 68.8 | `f9699e1933c22514…` | wrote /Users/djourno/Downloads/PJM/.local/tmp/cp-17/lead-ci312/reports/cp3b/payload.json |
| 03-pytest | `uv run pytest -q` | 0 | 476.5 | `19d4845e9e56e74d…` | 2310 passed, 41 skipped in 475.00s (0:07:55) |
| 04-pytest | `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | 0.5 | `d422fbe2e481c669…` | 8 passed in 0.02s |
| 05-python | `uv run python scripts/verify_release.py` | 0 | 1.0 | `b69996cb1e6d2b04…` | PASS — every bound claim agrees on every surface; the static page fetches nothing; the hea |
| 06-pytest | `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | 1.6 | `fe9325b38a894bb3…` | 15 passed in 1.17s |
| 07-tree | `python3 scripts/publication_guard.py tree` | 0 | 0.0 | `0276e41830b4da6d…` | publication-guard: the tree carries no placeholder and a final build record |
| 08-collection | `uv run pytest --collect-only -m stress -q` | 0 | 2.6 | `f6f2133201f9f5c6…` | 19/2350 tests collected (2331 deselected) in 1.96s |

## stress (Python 3.12; tree `cabbd2f9f56698ac968f86bf2d107bcd7f05cc9b`; complete True; copy removed True)

| Step | Command | Exit | Seconds | Log SHA-256 | Last line |
|---|---|---:|---:|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.2 | `3e4ea3eeacc5f962…` |  + zipp==4.1.0 |
| 01a-direct-version | `python3 --version` | 0 | 0.0 | `f1c67c1448ff23fd…` | Python 3.12.14 |
| 01b-uv-version | `uv run python --version` | 0 | 0.0 | `d8166eb859451afd…` | Python 3.12.14 |
| 02-stress | `uv run pytest -m stress -q` | 0 | 404.4 | `2b191251806c023c…` | 19 passed, 1 skipped, 2331 deselected in 386.58s (0:06:26) |

