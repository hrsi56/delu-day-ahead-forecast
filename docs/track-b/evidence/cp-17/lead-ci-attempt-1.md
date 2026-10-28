# Lead CI — CP-17 attempt 1 (history-free single-commit copy; candidate reviewed FAIL by integration-attempt-1.md)

Candidate: `dc78e209b05ebab39e5000d5ac812f9eee035316`. Runner: `.local/artifacts/cp-17/ci-runner.py lead <sha> ci312 stress`
(CP-17-probe's runner, adapted): `git archive` of the candidate into `.local/tmp/cp-17/lead-<mode>/`, one commit with
the same tree (checked), a fresh `.venv` synced offline from the project-local uv cache, the workflow's seven steps with
`CI=true` and Python 3.12 (local-only inputs hidden: `CP17_PROJECT_ROOT` points nowhere), then `pytest -m stress` with CI
unset (local inputs and runtimes visible). The copies were removed afterwards. This is the Lead's own check, not the review.

## ci312 (Python 3.12; tree `744994cf81ce86fbd314c90684173315069dc219`; complete True; copy removed True)

| Step | Command | Exit | Seconds | Log SHA-256 | Last line |
|---|---|---:|---:|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.6 | `8ca25861c0ea69a9…` |  + zipp==4.1.0 |
| 01a-direct-version | `python3 --version` | 0 | 0.0 | `f1c67c1448ff23fd…` | Python 3.12.14 |
| 01b-uv-version | `uv run python --version` | 0 | 0.1 | `d8166eb859451afd…` | Python 3.12.14 |
| 02-python | `uv run python scripts/build_wasm_payload.py` | 0 | 76.1 | `e84abb226d7015be…` | wrote /Users/djourno/Downloads/PJM/.local/tmp/cp-17/lead-ci312/reports/cp3b/payload.json |
| 03-pytest | `uv run pytest -q` | 0 | 471.8 | `731ec143479fec73…` | 2303 passed, 41 skipped in 470.37s (0:07:50) |
| 04-pytest | `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | 0.5 | `d422fbe2e481c669…` | 8 passed in 0.02s |
| 05-python | `uv run python scripts/verify_release.py` | 0 | 1.0 | `b69996cb1e6d2b04…` | PASS — every bound claim agrees on every surface; the static page fetches nothing; the hea |
| 06-pytest | `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | 1.6 | `6dbff1a0d1ed1c21…` | 15 passed in 1.19s |
| 07-tree | `python3 scripts/publication_guard.py tree` | 0 | 0.0 | `0276e41830b4da6d…` | publication-guard: the tree carries no placeholder and a final build record |
| 08-collection | `uv run pytest --collect-only -m stress -q` | 0 | 2.6 | `a803fc364f00ad7f…` | 19/2343 tests collected (2324 deselected) in 1.98s |

## stress (Python 3.12; tree `744994cf81ce86fbd314c90684173315069dc219`; complete True; copy removed True)

| Step | Command | Exit | Seconds | Log SHA-256 | Last line |
|---|---|---:|---:|---|---|
| 01-sync | `uv sync --locked --dev` | 0 | 1.2 | `6c795166053a625f…` |  + zipp==4.1.0 |
| 01a-direct-version | `python3 --version` | 0 | 0.0 | `f1c67c1448ff23fd…` | Python 3.12.14 |
| 01b-uv-version | `uv run python --version` | 0 | 0.1 | `d8166eb859451afd…` | Python 3.12.14 |
| 02-stress | `uv run pytest -m stress -q` | 0 | 412.2 | `68e9f1d855e3335d…` | 19 passed, 1 skipped, 2324 deselected in 392.91s (0:06:32) |

