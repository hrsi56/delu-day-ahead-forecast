# PRES-1 final checks before full independent Integration review

Artifact commit: **a05cbc3348cb5a7860a2284cb11f8dbedcf34735**. The next commit adds only this evidence record. These are Lead observations, not an independent terminal verdict.

## Complete local and clean CI-equivalent runs

Python **3.13.15** full suite: **944 passed, 7 skipped in 128.33 s**, exit 0. Command from Lead checkout: `PATH=<project>/.venv/bin:$PATH PYTHONPATH=src PYTHONDONTWRITEBYTECODE=1 TMPDIR=<project>/.local/tmp/pres-1 python3 <project>/.local/tmp/pres-1/nocreds.py <project>/.venv/bin/python -m pytest -q`. The pre-existing root environment was consumed read-only; source resolved to this checkout. No source/test/artifact was edited during this run; final browser records were committed with the same tested bytes.

Python **3.12.14**, fresh clean detached `.local/worktrees/pres-1/ci-8` at the exact artifact SHA: `uv sync --locked --dev` exited 0. All workflow steps, including the normally main-only publication guard, ran and passed. Full suite: **944 passed, 7 skipped in 129.60 s**. This is macOS CI-equivalent execution, not Ubuntu CI. The seven existing deliberate/optional exclusions are described in independent-check-4; no charged research replay was enabled. Pinned dependencies are unchanged. Test environments removed credential-like variables without displaying values; cache/runtime/temp paths were under `.local/`.

| Command | Exit | Observation |
|---|---:|---|
| `uv run python --version` | 0 | Python 3.12.14 |
| `uv run python scripts/build_wasm_payload.py` | 0 |   fixture:  54 days / 1296 rows (4 fail-closed) / regimes ['crisis', 'dst-fall-back', 'dst-spring-forward', 'post-crisis (holdout)', 'post-crisis (holidays, bridge days)', 'pre-crisis']; wrote /Users/djourno/Downloads/PJM/.local/worktrees/pres-1/ci-8/reports/cp3b/payload.json |
| `uv run pytest -q` | 0 | ..............                                                           [100%]; 944 passed, 7 skipped in 129.60s (0:02:09) |
| `uv run pytest tests/test_10_cqr_order_statistic.py -q` | 0 | ........                                                                 [100%]; 8 passed in 0.01s |
| `uv run python scripts/verify_release.py` | 0 | ; PASS — every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces |
| `uv run pytest tests/test_22_wasm_equivalence.py -q` | 0 | ...............                                                          [100%]; 15 passed in 1.18s |
| `make verify` | 0 | ; PASS — every bound claim agrees on every surface; the static page fetches nothing; the headline, names and statuses agree across surfaces |
| `make lint-publication` | 0 | templates: 0 finding(s); PASS — the reading path and the template sources meet the standard's §4 and §5 rules |
| `uv run python scripts/mlflow_export.py --check` | 0 | 2026/09/29 00:12:57 INFO mlflow.agent.hint: Load the `instrumenting-with-mlflow-tracing` skill at /Users/djourno/Downloads/PJM/.local/worktrees/pres-1/ci-8/.venv/lib/python3.12/site-packages/mlflow/assistant/skills/instrumenting-with-mlflow-tracing/SKILL.md before writing any tracing code; it ships with this MLflow install. Set MLFLOW_DISABLE_AGENT_HINT=1 to silence this.; the committed export is current |
| `uv run python scripts/mlflow_publish.py --dry-run` | 0 | 2026/09/29 00:12:59 INFO mlflow.agent.hint: Load the `instrumenting-with-mlflow-tracing` skill at /Users/djourno/Downloads/PJM/.local/worktrees/pres-1/ci-8/.venv/lib/python3.12/site-packages/mlflow/assistant/skills/instrumenting-with-mlflow-tracing/SKILL.md before writing any tracing code; it ships with this MLflow install. Set MLFLOW_DISABLE_AGENT_HINT=1 to silence this.; dry run: 23 runs, 6928 metric points, 55 artifacts; outbound scan clean; export current at a05cbc3348cb |
| `uv run python scripts/rebuild_presentation.py` | 0 | cross-surface agreement and zero-fetch checks: ok (0.5 s); rebuilt every presentation surface in 10.6 s |
| `git status --porcelain=v1` | 0 | Empty stdout: clean tree after rebuild |
| `python3 scripts/publication_guard.py tree` | 0 | publication-guard: the tree carries no placeholder and a final build record |

Clean HEAD and empty status were confirmed before and after. The CI checkout is removed after recording these results; logs are retained. The Lead separately ran a post-commit `rebuild_presentation.py`, then `git status --porcelain=v1`: empty. Page size remains 1,560,646 bytes; `final: true`; six routes expected/published; zero omissions. `git diff --check` is clean.

## Final release surfaces

- `2026-09-29-final-s10.json`: all eleven views, four native-engine accessibility-tree checks, keyboard/touch/contrast/zoom checks pass. Chrome/WebKit headline bottoms: 774.6/775.3 px desktop, 604.6/604.7 px phone; finding bottoms: 1765.6/1767.0 px desktop, 2488.5/2490.1 px phone. These remain inside the standard's floors. No real Safari, iPhone or screen reader used.
- `reports/cp3/link_check.json`: fresh checker exit 0, no failed destination; the six public MLflow routes also have their own REST/browser/settled-chart checks, not just HTTP status.
- `2026-09-29-final-demo.json`: fresh local final-bundle starts in Chrome/WebKit at 1440×900 and 390×844; all four ready, zero failed requests and console errors; both interval and scenario controls change the view on all four runs.
- `2026-09-29-final-states.json`: both engines show failure for forced asset/runtime/hang cases, loading before the deadline, and successful retry to ready. No false progress claimed.
- `reports/cp3b/space_wasm_bundle.json`: final Python 3.13 bundle **b046c69b899bb9d5a2b2f9aeb3e5b3eebfdda820a419137ef5cdf8b8ac8f7c3d**, 805 files, 44,162,180 bytes, all 315 referenced assets present. Three build/identity steps exited 0. The local port-8820 server was stopped after testing; no redeploy was performed.
- Full F1–F4 evidence and network authority: `f1-f4-execution.md`, public upload/mirror/routes/charts/capability records and verifier-generated `mlflow_index.json`. All five export-file hashes still match the exact F1 payload.

## Cold-reader applicability and review scope

The prior two-reader record remains `cold-reader-check.md`. Independent-check-4 confirmed its 58 claim blocks against its original c6dda1f page. A fresh comparison of the final page to that pre-F1 candidate finds all **58 data-block texts identical**; final §1 placements are independently measured above. New tracking links and the future-to-present tracking statement do not change answers 1–5. This is explicit continued applicability, not a fabricated new cold read.

Because the generated change includes that tense update in addition to new links, the next fresh agent receives a **full** final Integration assignment, including F1–F4. No source, tests or model/inference code changed after pre-F1 PASS. The Lead does not infer the terminal verdict from these passing logs.

## Retained local logs

- `.local/tmp/pres-1/ci8-sync.log` — SHA-256 `cac4f3db4f97507406b473a2bef9990202487d62fa787b524378c799494ae2b2`.
- `.local/tmp/pres-1/ci8/results.json` — SHA-256 `cff492f309c33f148b1800f97464fbbd15bdf2b9b6d6a221ff77b0b6c116beed`.
- `.local/tmp/pres-1/run-ci8.py` — SHA-256 `1320376b144398fa2972fceacf3ada7026427a0d14b8024c8b8993945c1ae223`.
- `.local/tmp/pres-1/final-suite313.log` — SHA-256 `22d0584a56190947a81115860254d2bbb0836f86f54602cdb85d925a8c5a5c0d`.
- `.local/tmp/pres-1/final-clean-rebuild.log` — SHA-256 `4e8be4d79aec1b00fe6d4830d501ed2890606255b6a1d43325282082d5ff3a5b`.
- `.local/tmp/pres-1/final-release.log` — SHA-256 `5c139cb406f9a08790f718c6e7416b56028e69bac16c4b5159cf366af323b008`.
- `.local/tmp/pres-1/final-links.log` — SHA-256 `b560671e844b99fec896a94f976e7f6ed8a3718a3087802e05d2b3e8c83bec79`.
- `.local/tmp/pres-1/final-demo.log` — SHA-256 `b94f4adfd67f9b9fab4d4e4036688c8dcabb6f9108e9dd6e5c275b3443128672`.
- `.local/tmp/pres-1/final-states.log` — SHA-256 `24b27097415da6a8fda0a8d2a390801b82e4f0c814f49edd3f60d673c7db4a25`.
- `.local/tmp/pres-1/final-cold-reader-applicability.json` — SHA-256 `97d83cbb0359e04db9bc2e36048f00f98b1ecbf51a5bfa27aeb879aae846d312`.
- `.local/tmp/pres-1/ci8/1.log` — SHA-256 `4c3569f5da09975434dd9fd9a91fadbc4367a91d8f3c3fab59e9241ab9ee4bd8`.
- `.local/tmp/pres-1/ci8/10.log` — SHA-256 `fd2cb21fba4d5862c438ad6cc6bb926f128b45b9b2cf4eb2f8bb71c2acc13d69`.
- `.local/tmp/pres-1/ci8/11.log` — SHA-256 `2011fb4a4db81f79389cbef382f9ea79d2c18cd5575c17c383f30aefe7911969`.
- `.local/tmp/pres-1/ci8/12.log` — SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- `.local/tmp/pres-1/ci8/13.log` — SHA-256 `e097b0ac2609bcbb3ca8d0c3dafe177e4dc56ac9e9ed9d4a1e679145e7510014`.
- `.local/tmp/pres-1/ci8/2.log` — SHA-256 `9c127778e889be1974e80270dd012b8c92d7345ff0c30c7e4a1a7ac7e263fc71`.
- `.local/tmp/pres-1/ci8/3.log` — SHA-256 `1c333d08ffdc2e6d22839f3d0c6272a2e55298917d5496f8aba748c48aae981f`.
- `.local/tmp/pres-1/ci8/4.log` — SHA-256 `71288863ec9567395a647dd0c8fbf0e2048bee72283202612ad6f90a7a526ef3`.
- `.local/tmp/pres-1/ci8/5.log` — SHA-256 `36e89bb7e634f693ace234e64d73cce752d1458e4c1925e3e6fdc8fb80e92fdd`.
- `.local/tmp/pres-1/ci8/6.log` — SHA-256 `d75603f9786468f1512af75d1b71c88f548072b4a5f03f4f6e0bcccba8804844`.
- `.local/tmp/pres-1/ci8/7.log` — SHA-256 `8a59578a3c860053d36ad60a465b9ccf8356bf759e7194ea3ccdaf73400bdf71`.
- `.local/tmp/pres-1/ci8/8.log` — SHA-256 `869ba42374b692ea4e3df8ac31b7557c3b063d7612029d893545e30e5b7e59b7`.
- `.local/tmp/pres-1/ci8/9.log` — SHA-256 `aa1760f890b3585f7a1760231fbb8c2f87dd88832603e38e2616dc5ec1da49e9`.
