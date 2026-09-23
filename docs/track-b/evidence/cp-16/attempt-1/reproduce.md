# CP-16 partial-artifact reproduction

Run from the isolated candidate checkout. Use the existing pinned root interpreter `/Users/djourno/Downloads/PJM/.venv/bin/python`; no download/environment build is needed. Set `PYTHONPATH` to the candidate's `src`. The current input manifest records CPython/package versions and exact input hashes. The final scientific result is absent, intentionally.

Safe bounded checks (no estimator fit or residual replay):

```sh
PYTHONPATH=src /Users/djourno/Downloads/PJM/.venv/bin/python -m pytest tests/cp16/test_monitor.py tests/cp16/test_budget_inputs.py -q -p no:cacheprovider --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-16/review-monitor-tests
PYTHONPATH=src /Users/djourno/Downloads/PJM/.venv/bin/python -m pytest tests/test_02_rolling_closed_left.py tests/test_05_schema_firewall.py tests/test_08_partition_integrity.py tests/test_12_partition_exclusion.py tests/test_24_live_namespace_is_walled_off.py -q -p no:cacheprovider --basetemp=/Users/djourno/Downloads/PJM/.local/tmp/cp-16/review-guard-tests
```

All compute, including review, must be wrapped and charged to the existing shared ledger:

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python scripts/cp16_v2.py --monitor --ledger /Users/djourno/Downloads/PJM/.local/artifacts/cp-16/budget.json --project-root /Users/djourno/Downloads/PJM --log /Users/djourno/Downloads/PJM/.local/artifacts/cp-16/unique-review.log -- <command>
```

Expected repaired monitor/input suite: 7 pass. The complete 49-test pre-run suite passed before admission, but its whole residual control set consumes 1,002 conservative policy-days per rerun and must **not** be repeated under the remaining 770. Earlier partial/admission evidence must not be overwritten or treated as resumable certified state. No automatic retry is implemented.

The exact originally run commands, exits, elapsed charges, source revisions and logs are under `docs/track-b/evidence/cp-16/` and resources.json. The first protocol bytes are reachable in commit e625967e20f3f79f2c4d07c9b414065ff0717d02. `input-manifest.json` enumerates all expected UTC target keys and permitted origins. Preflight itself can be rerun to a fresh project-local scratch output under the same monitor; it takes roughly 40seconds and performs no fits or scoring.

Do not run admission/comparison/score without the required amended authority and sufficient remaining allowance. The current return makes no executable full-evaluation reproducibility claim. The frozen commands and algorithm remain in protocol.json, with the supervision repair separately identified. The Integration Critic must review this incomplete candidate honestly, not certify the Lead's implementation or partial artifacts as PASS.
