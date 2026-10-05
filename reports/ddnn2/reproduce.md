# CP-24 — reproduction

**Setup.** Run every command from the repository root on the Owner's M3, CPU only, with BLAS 1 (the monitor sets
it). The inputs CP-24 reuses are CP-20's retained grids and HG component cache and CP-21's fit cache under
`.local/artifacts/cp-20/` and `cp-21/`, read only, under the identities CP-24 verifies. Set `CP24_PROJECT_ROOT`
to the primary checkout when you run from a worktree; the ledger and caches live there. `PY` is the project's
`.venv/bin/python`; `LOG` is `.local/artifacts/cp-24/logs`.

## Environment

```bash
uv sync --locked --dev
uv export --project tests/cp23/torch-reference --frozen --only-group torch-reference --no-emit-project --format requirements-txt -o .local/tmp/cp-24/torch-reference-requirements.txt
uv pip install --python .venv/bin/python --require-hashes -r .local/tmp/cp-24/torch-reference-requirements.txt
```

The last two commands install CP-23's pinned, test-only PyTorch 2.14.1 reference (already installed on the
Owner's machine; CP-24 downloaded nothing). The root `pyproject.toml` and `uv.lock` are unchanged.

## The route, in order (every compute job under the monitor)

```bash
$PY scripts/cp24_ddnn2.py init-ledger
$PY scripts/cp24_ddnn2.py monitor --name verify-weather --workers 1 --log $LOG/verify-weather.log -- $PY scripts/cp24_ddnn2.py job verify-weather
$PY scripts/cp24_ddnn2.py monitor --name verify-inputs --workers 1 --log $LOG/verify-inputs.log -- $PY scripts/cp24_ddnn2.py job verify-inputs
$PY scripts/cp24_ddnn2.py monitor --name v4-parity --workers 4 --log $LOG/v4-parity.log -- $PY scripts/cp24_ddnn2.py job v4-parity --workers 4
$PY scripts/cp24_ddnn2.py monitor --name reference-checks --workers 1 --log $LOG/reference-checks.log -- $PY scripts/cp24_ddnn2.py job reference-checks
$PY scripts/cp24_ddnn2.py monitor --name resource-admission --workers 1 --log $LOG/resource-admission.log -- $PY scripts/cp24_ddnn2.py job resource-admission --workers 1
$PY scripts/cp24_ddnn2.py monitor --name v4-gate --workers 3 --log $LOG/v4-gate.log -- $PY scripts/cp24_ddnn2.py job v4-gate --workers 3
# each pre-fold round r (design committed before its search; search ledger and ensembles committed before its gate)
$PY scripts/cp24_ddnn2.py monitor --name round-design-<r> --workers 1 --log $LOG/round-design-<r>.log -- $PY scripts/cp24_ddnn2.py job round-design --round <r> --before-attempt <k> [--changes <json> --steering <committed answer>]
$PY scripts/cp24_ddnn2.py monitor --name search-r<r> --workers 4 --log $LOG/search-r<r>.log -- $PY scripts/cp24_ddnn2.py job search --round <r> --workers 4
$PY scripts/cp24_ddnn2.py monitor --name gate-r<r> --workers 4 --log $LOG/gate-r<r>.log -- $PY scripts/cp24_ddnn2.py job gate --round <r> --workers 4
$PY scripts/cp24_ddnn2.py monitor --name round-report-<r> --workers 1 --log $LOG/round-report-<r>.log -- $PY scripts/cp24_ddnn2.py job round-report --round <r>
# a scored attempt k, after the S1 answer that freezes round r (committed under steering/)
$PY scripts/cp24_ddnn2.py monitor --name protocol-a<k> --workers 1 --log $LOG/protocol-a<k>.log -- $PY scripts/cp24_ddnn2.py job protocol --attempt <k> --round <r> --steering <committed answer>
$PY scripts/cp24_ddnn2.py monitor --name fits-warmup-a<k> --workers 4 --log $LOG/fits-warmup-a<k>.log -- $PY scripts/cp24_ddnn2.py job fits --attempt <k> --stage warmup --workers 4
$PY scripts/cp24_ddnn2.py monitor --name admission-a<k> --workers 1 --log $LOG/admission-a<k>.log -- $PY scripts/cp24_ddnn2.py job admission --attempt <k>
$PY scripts/cp24_ddnn2.py monitor --name fits-evaluation-a<k> --workers 4 --log $LOG/fits-evaluation-a<k>.log -- $PY scripts/cp24_ddnn2.py job fits --attempt <k> --stage evaluation --workers 4
$PY scripts/cp24_ddnn2.py monitor --name comparison-a<k> --workers 1 --log $LOG/comparison-a<k>.log -- $PY scripts/cp24_ddnn2.py job comparison --attempt <k>
$PY scripts/cp24_ddnn2.py monitor --name score-a<k> --workers 1 --log $LOG/score-a<k>.log -- $PY scripts/cp24_ddnn2.py job score --attempt <k>
$PY scripts/cp24_ddnn2.py monitor --name fit-cost-a<k> --workers 1 --log $LOG/fit-cost-a<k>.log -- $PY scripts/cp24_ddnn2.py job fit-cost --attempt <k>
$PY scripts/cp24_ddnn2.py monitor --name controls-a<k> --workers 1 --log $LOG/controls-a<k>.log -- $PY scripts/cp24_ddnn2.py job controls --attempt <k>
$PY scripts/cp24_ddnn2.py monitor --name daily-cycle-a<k> --workers 4 --log $LOG/daily-cycle-a<k>.log -- $PY scripts/cp24_ddnn2.py job daily-cycle --attempt <k>
$PY scripts/cp24_ddnn2.py monitor --name diagnostics-a<k> --workers 1 --log $LOG/diagnostics-a<k>.log -- $PY scripts/cp24_ddnn2.py job diagnostics --attempt <k>
# the packet, the export, local tracking, the report and the manifest
PYTHONPATH=src $PY -m cp24.packet
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 PYTHONPATH=src $PY -m cp24.export --attempt <deciding k>
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 $PY scripts/cp24_ddnn2.py monitor --name mlflow-local --workers 1 --log $LOG/mlflow-local.log -- $PY scripts/cp24_ddnn2.py job mlflow-local
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 $PY scripts/mlflow_export.py --check
$PY scripts/cp24_ddnn2.py monitor --name finalise --workers 1 --log $LOG/finalise.log -- $PY scripts/cp24_ddnn2.py job finalise
PYTHONPATH=src $PY -m cp24.report
PYTHONPATH=src $PY -m cp24.claims
$PY scripts/cp24_ddnn2.py monitor --name finalise-manifest --workers 1 --log $LOG/finalise-manifest.log -- $PY scripts/cp24_ddnn2.py job finalise --manifest-only
```

## Verification (no fit, no pass)

```bash
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 $PY -m pytest -q tests/cp24
PYTHONPATH=src $PY -m cp24.packet --check
PYTHONPATH=src $PY -m cp24.claims --check
PYTHONPATH=src $PY -m cp24.report --check
PYTHONPATH=src $PY -m cp24.basetree --check
MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1 PYTHONPATH=src $PY -m cp24.export --attempt <deciding k> --check
```

## Independent review (charged as review)

```bash
$PY scripts/cp24_ddnn2.py monitor --name review-reference --workers 1 --log <log outside the checkout> -- $PY -m pytest -q -p no:cacheprovider -rA tests/cp24/torch_reference_checks.py
$PY scripts/cp24_ddnn2.py monitor --name review --workers 1 --log <log outside the checkout> -- $PY -m cp24.review --out <file outside the checkout> --score <k> --gate <r> --trial <r>:<fold>:<trial>:<batch> --ensemble <k>:<fold>:<day> --replay <k>:v5:<fold>:<first>:<last>
```
