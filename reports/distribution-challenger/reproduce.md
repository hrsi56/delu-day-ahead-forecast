# CP-23 — reproduction

**Setup.** Run every command from the repository root on the Owner's M3, CPU only, with BLAS 1.

- The inputs CP-23 reuses are CP-20's retained grids and HG component cache and CP-21's fit cache under
  `.local/artifacts/cp-20/` and `cp-21/`. They are read only, under the identities CP-23 verifies.
- Set `CP23_PROJECT_ROOT` to the primary checkout when you run from a worktree; the ledger and caches
  live there.

## Environment

```bash
uv sync --locked --dev
uv export --project tests/cp23/torch-reference --frozen --only-group torch-reference --no-emit-project --format requirements-txt -o .local/tmp/cp-23/torch-reference-requirements.txt
uv pip install --python .venv/bin/python --require-hashes -r .local/tmp/cp-23/torch-reference-requirements.txt
```

The second and third commands install the pinned, test-only PyTorch 2.14.1 reference. It adds packages
and changes none (Owner ruling on §21.3).

## The route, in order (every compute job under the monitor)

```bash
python scripts/cp23_ddnn.py init-ledger
python scripts/cp23_ddnn.py monitor --name reference-checks --workers 1 --log .local/artifacts/cp-23/logs/reference-checks.log -- python scripts/cp23_ddnn.py job reference-checks
python scripts/cp23_ddnn.py monitor --name resource-admission --workers 1 --log .local/artifacts/cp-23/logs/resource-admission.log -- python scripts/cp23_ddnn.py job resource-admission
python scripts/cp23_ddnn.py monitor --name verify-inputs --workers 1 --log .local/artifacts/cp-23/logs/verify-inputs.log -- python scripts/cp23_ddnn.py job verify-inputs
python scripts/cp23_ddnn.py monitor --name verify-weather --workers 1 --log .local/artifacts/cp-23/logs/verify-weather.log -- python scripts/cp23_ddnn.py job verify-weather
python scripts/cp23_ddnn.py monitor --name e1 --workers 1 --log .local/artifacts/cp-23/logs/e1.log -- python scripts/cp23_ddnn.py job e1
python scripts/cp23_ddnn.py monitor --name protocol --workers 1 --log .local/artifacts/cp-23/logs/protocol.log -- python scripts/cp23_ddnn.py job protocol
git add reports/distribution-challenger/protocol.json reports/distribution-challenger/preflight && git commit -F <message>
python scripts/cp23_ddnn.py monitor --name select --workers 4 --log .local/artifacts/cp-23/logs/select.log -- python scripts/cp23_ddnn.py job select --workers 4
git add reports/distribution-challenger/selection.json && git commit -F <message>
python scripts/cp23_ddnn.py monitor --name fits-warmup --workers 4 --log .local/artifacts/cp-23/logs/fits-warmup.log -- python scripts/cp23_ddnn.py job fits --stage warmup --workers 4
python scripts/cp23_ddnn.py monitor --name admission --workers 1 --log .local/artifacts/cp-23/logs/admission.log -- python scripts/cp23_ddnn.py job admission
git add reports/distribution-challenger/lineage.json && git commit -F <message>
python scripts/cp23_ddnn.py monitor --name fits-evaluation --workers 4 --log .local/artifacts/cp-23/logs/fits-evaluation.log -- python scripts/cp23_ddnn.py job fits --stage evaluation --workers 4
python scripts/cp23_ddnn.py monitor --name comparison --workers 1 --log .local/artifacts/cp-23/logs/comparison.log -- python scripts/cp23_ddnn.py job comparison
git add reports/distribution-challenger/{predictions.parquet,members.parquet,lineage.json} && git commit -F <message>
python scripts/cp23_ddnn.py monitor --name score --workers 1 --log .local/artifacts/cp-23/logs/score.log -- python scripts/cp23_ddnn.py job score
python scripts/cp23_ddnn.py monitor --name parity --workers 1 --log .local/artifacts/cp-23/logs/parity.log -- python scripts/cp23_ddnn.py job parity
python scripts/cp23_ddnn.py monitor --name reproduce --workers 1 --log .local/artifacts/cp-23/logs/reproduce.log -- python scripts/cp23_ddnn.py job reproduce
python scripts/cp23_ddnn.py monitor --name fit-cost --workers 1 --log .local/artifacts/cp-23/logs/fit-cost.log -- python scripts/cp23_ddnn.py job fit-cost
python scripts/cp23_ddnn.py monitor --name controls --workers 1 --log .local/artifacts/cp-23/logs/controls.log -- python scripts/cp23_ddnn.py job controls
python scripts/cp23_ddnn.py monitor --name daily-cycle --workers 4 --log .local/artifacts/cp-23/logs/daily-cycle.log -- python scripts/cp23_ddnn.py job daily-cycle
python scripts/cp23_ddnn.py monitor --name diagnostics --workers 1 --log .local/artifacts/cp-23/logs/diagnostics.log -- python scripts/cp23_ddnn.py job diagnostics
PYTHONPATH=src python -m cp23.packet
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 python scripts/mlflow_export.py --draft cp23
python scripts/cp23_ddnn.py monitor --name mlflow-local --workers 1 --log .local/artifacts/cp-23/logs/mlflow-local.log -- python scripts/cp23_ddnn.py job mlflow-local
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 python scripts/mlflow_export.py --diff-against a4acd792954c577e60235c427380c82031c4372a --out reports/distribution-challenger/published-export-diff.json
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 python scripts/mlflow_export.py --check
python scripts/cp23_ddnn.py monitor --name finalise --workers 1 --log .local/artifacts/cp-23/logs/finalise.log -- python scripts/cp23_ddnn.py job finalise
PYTHONPATH=src python -m cp23.report
PYTHONPATH=src python -m cp23.claims
python scripts/cp23_ddnn.py monitor --name finalise-manifest --workers 1 --log .local/artifacts/cp-23/logs/finalise-manifest.log -- python scripts/cp23_ddnn.py job finalise --manifest-only
```

## Verification (no fit, no pass)

```bash
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 python -m pytest -q tests/cp23
PYTHONPATH=src python -m cp23.packet --check
PYTHONPATH=src python -m cp23.claims --check
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 python scripts/mlflow_export.py --draft cp23 --check
```

## Independent review (charged as review)

```bash
python scripts/cp23_ddnn.py monitor --name review-reference --workers 1 --log <log outside the checkout> -- python -m pytest -q -p no:cacheprovider -rA tests/cp23/torch_reference_checks.py
python scripts/cp23_ddnn.py monitor --name review --workers 1 --log <log outside the checkout> -- python -m cp23.review --out <file outside the checkout> --score --ddnn fold_3:2022-08-20 --replay v5:fold_4:2025-05-01:2025-05-14
```

What the review commands check:

- **The first command** reruns the PyTorch reference checks directly: 26 checks at the frozen tolerances,
  and a missing PyTorch fails collection. It writes nothing in the checkout.
- **`--score`** recomputes every metric, interval, reading and the verdict from the committed predictions
  (one reference pass and one bootstrap pass).
- **`--ddnn`** refits one origin's four DDNN members and compares D's central forecast, its quantiles and
  each member's weights with the committed rows.
- **`--replay`** replays v5 from the committed admission freeze through the H layer.

Both write only outside the checkout.
