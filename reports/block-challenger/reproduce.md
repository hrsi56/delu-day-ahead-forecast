# CP-21 reproduction — capstone v21-r6 §17

All commands run from the repository root of the reviewed checkout, on CPU, through the driver
monitor, against the **same cumulative CP-21 ledger** (`.local/artifacts/cp-21/ledger/budget.json`).
Never create a fresh ledger to evade the §17.8 caps: every rerun spends the remaining allowances
(LightGBM fits, component-days, Lasso attempts, policy-days, reference and bootstrap passes,
machine-hours) and is refused before a cap is crossed.

```sh
P=/Users/djourno/Downloads/PJM
PY=$P/.venv/bin/python                 # the inherited uv.lock environment (LightGBM 4.7.0)
A=$P/.local/artifacts/cp-21            # ledger, logs, markers, fit and state caches (ignored)
export MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=true   # no network call from any MLflow import
M="$PY scripts/cp21_blocks.py monitor"
```

The monitor sets BLAS/OpenMP threads to 1, charges machine time as wall-clock × declared workers,
samples process-tree and aggregate RSS and added disk, refuses a duplicate instance or more than
four concurrent workers, refuses to start inside the Friday/Shabbat window (Asia/Jerusalem) and
stops a job 20 minutes before it opens, and writes `$A/markers/<job>.DONE.json` or `.FAILED.json`.
Research jobs refuse to run outside the monitor.

## 1. Pre-run (before the frozen protocol)

```sh
$PY scripts/cp21_blocks.py init-ledger                     # once; refuses to reset an existing ledger
$M --name verify-inputs  --workers 1 --log $A/logs/verify-inputs.log  -- $PY scripts/cp21_blocks.py job verify-inputs
$M --name verify-weather --workers 1 --log $A/logs/verify-weather.log -- $PY scripts/cp21_blocks.py job verify-weather
$M --name benchmark      --workers 4 --log $A/logs/benchmark.log      -- $PY scripts/cp21_blocks.py job benchmark
$M --name determinism    --workers 4 --log $A/logs/determinism.log    -- $PY scripts/cp21_blocks.py job determinism
$M --name e1             --workers 1 --log $A/logs/e1.log             -- $PY scripts/cp21_blocks.py job e1
$M --name protocol       --workers 1 --log $A/logs/protocol.log       -- $PY scripts/cp21_blocks.py job protocol
```

`verify-inputs` checks the issued v21-r6 documents, the CP-15/16/20 artifacts, the recomputed CP-20
HG identity and all 638 HG component-cache entries (the 448 evaluation-day centrals equal the
accepted HG central bit for bit). `verify-weather` regenerates the frozen weather features from the
2,476 retained decoded grids through CP-20's frozen conversion. The benchmark and the determinism
check fit on training-only data and compute no validation loss. The protocol (with its E1 origin
table and preflight copies) is committed before any main fit.

## 2. Training-only stage, then the admission freeze

```sh
$M --name fits-warmup --workers 4 --log $A/logs/fits-warmup.log -- $PY scripts/cp21_blocks.py job fits --stage warmup --workers 4
$M --name admission   --workers 1 --log $A/logs/admission.log   -- $PY scripts/cp21_blocks.py job admission
git add reports/block-challenger/lineage.json && git commit      # the admission freeze
```

Warm-up and admission origins are fitted on data materialised before each fold's first evaluation
day. Fits are cached under `$A/fits/<fold>/<day>/<arm>.json`, each bound to the frozen protocol,
inputs and weather design; a verified cache hit is reused, a miss is a charged fit.

## 3. Outer stage

```sh
$M --name fits-evaluation --workers 4 --log $A/logs/fits-evaluation.log -- $PY scripts/cp21_blocks.py job fits --stage evaluation --workers 4
$M --name comparison --workers 1 --log $A/logs/comparison.log -- $PY scripts/cp21_blocks.py job comparison
git add reports/block-challenger/{predictions.parquet,lineage.json} && git commit   # vectors before scoring
$M --name hg-parity  --workers 1 --log $A/logs/hg-parity.log  -- $PY scripts/cp21_blocks.py job hg-parity
$M --name score      --workers 1 --log $A/logs/score.log      -- $PY scripts/cp21_blocks.py job score
$M --name controls   --workers 4 --log $A/logs/controls.log   -- $PY scripts/cp21_blocks.py job controls
$M --name fit-cost   --workers 1 --log $A/logs/fit-cost.log   -- $PY scripts/cp21_blocks.py job fit-cost
$M --name daily-cycle --workers 4 --log $A/logs/daily-cycle.log -- $PY scripts/cp21_blocks.py job daily-cycle
```

`score` is the single metric-only reference pass and the single bootstrap pass of the checkpoint:
it writes `metrics.csv`, `diagnostics.csv`, `uncertainty.csv` (paired, per-fold and ratio
intervals), `replicates.parquet` and `replicate-scores.parquet` (every stored draw), `criteria.csv`,
`fallback.csv` and `adoption.json` (the mechanical §17.6 verdict), and checks that HG's recomputed
§8 rows and the HG − H0 intervals equal CP-20's committed rows. The comparison replay persists each
evaluation day's HGL interval-layer state under `$A/states/`, which the cold daily cycle loads.

## 4. Packet, draft export, local tracking, report

```sh
$M --name packet  --workers 1 --log $A/logs/packet.log  -- $PY -m cp21.packet          # draft-registry.json
$M --name draft-export --workers 1 --log $A/logs/draft-export.log -- $PY scripts/mlflow_export.py --draft cp21
$M --name mlflow-local --workers 1 --log $A/logs/mlflow-local.log -- $PY scripts/cp21_blocks.py job mlflow-local
$M --name claims  --workers 1 --log $A/logs/claims.log  -- $PY -m cp21.claims          # claim map and packet
$M --name finalise --workers 1 --log $A/logs/finalise.log -- $PY scripts/cp21_blocks.py job finalise
$M --name report  --workers 1 --log $A/logs/report.log  -- $PY -m cp21.report
```

## 5. Checks

```sh
$M --name tests-cp21 --workers 1 --log $A/logs/tests-cp21.log -- $PY -m pytest tests/cp21 -q
$M --name export-check --workers 1 --log $A/logs/export-check.log -- $PY scripts/mlflow_export.py --check
$M --name draft-check  --workers 1 --log $A/logs/draft-check.log  -- $PY scripts/mlflow_export.py --draft cp21 --check
$M --name suite --workers 1 --log $A/logs/suite.log -- $PY -m pytest -q      # the CI suite
$M --name verify --workers 1 --log $A/logs/verify.log -- $PY scripts/verify_release.py   # make verify
```

The saved-evidence tests recompute the four new arms' losses from their committed predictions,
re-derive every interval from the stored replicates and re-apply the §17.6 rule to the committed
rows; they never re-run the bootstrap or re-score the saved references, each of which is a capped
pass under §17.8.
