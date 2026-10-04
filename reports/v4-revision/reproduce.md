# CP-22 reproduction — capstone v21-r9 §20

All commands run from the repository root of the reviewed checkout, on CPU, through the driver
monitor, against the **same cumulative CP-22 ledger** (`.local/artifacts/cp-22/ledger/budget.json`).
Never create a fresh ledger to evade the §20.8 caps: every rerun spends the remaining allowances
(LightGBM fits, component-days, Lasso attempts, policy-days, reference and bootstrap passes,
machine-hours) and is refused before a cap is crossed.

```sh
P=/Users/djourno/Downloads/PJM
PY=$P/.venv/bin/python                 # the inherited uv.lock environment (LightGBM 4.7.0)
A=$P/.local/artifacts/cp-22            # ledger, logs, markers, PN fit and state caches (ignored)
export MLFLOW_DISABLE_TELEMETRY=true DO_NOT_TRACK=1   # no network call from any MLflow import
M="$PY scripts/cp22_revision.py monitor"
```

The monitor sets BLAS/OpenMP threads to 1, charges machine time as wall-clock × declared workers,
samples process-tree and aggregate RSS and added disk, refuses a duplicate instance or more than
four concurrent workers, refuses to start inside the Friday/Shabbat window (Asia/Jerusalem) and
stops a job 20 minutes before it opens, and writes `$A/markers/<job>.DONE.json` or `.FAILED.json`.
Research jobs refuse to run outside the monitor. Jobs run between 2026-10-03 20:33 and 2026-10-04
00:00 IDT were started through `scripts/cp22_owner_calendar_exception.py monitor …`, which runs the
same frozen monitor with only that window's calendar check lifted, on the Owner's explicit written
exception (recorded in the ledger as `owner_calendar_exception_used`).

The inputs CP-22 reuses live outside the repository, as the brief states: CP-20's HG component
cache and weather grids (`.local/artifacts/cp-20/`) and CP-21's retained LightGBM fit cache
(`.local/artifacts/cp-21/fits/`). Every entry is verified before use (step 1).

## 1. Pre-run (before the frozen protocol)

```sh
$PY scripts/cp22_revision.py init-ledger                     # once; refuses to reset an existing ledger
$M --name verify-inputs  --workers 1 --log $A/logs/verify-inputs.log  -- $PY scripts/cp22_revision.py job verify-inputs
$M --name verify-weather --workers 1 --log $A/logs/verify-weather.log -- $PY scripts/cp22_revision.py job verify-weather
$M --name e1             --workers 1 --log $A/logs/e1.log             -- $PY scripts/cp22_revision.py job e1
$M --name benchmark      --workers 4 --log $A/logs/benchmark.log      -- $PY scripts/cp22_revision.py job benchmark
$M --name protocol       --workers 1 --log $A/logs/protocol.log       -- $PY scripts/cp22_revision.py job protocol
git add reports/v4-revision src/cp22 tests/cp22 scripts/cp22_revision.py && git commit   # the pre-run freeze
```

`verify-inputs` checks the issued v21-r9 documents, CP-21's fit identity recomputed from the Git
objects at `evidence/cp-21`, the CP-15/16/20/21 committed artifacts (manifest and evidence-tag
blob), all 638 HG component-cache entries and all 1,908 retained CP-21 L-P/L-N/L-R entries: every
central (warm-up included) equals CP-21's committed lineage hash, and every evaluation-day HG, v4,
L-P, L-N and L-R central equals the committed vector bit for bit. `verify-weather` regenerates the
frozen weather features from the 2,476 retained decoded grids. The benchmark fits on training-only
data and computes no validation loss. The protocol job also runs the synthetic fixtures
(`tests/cp22`) and records their outcome; it is committed before any main fit.

## 2. Training-only stage, then the admission freeze

```sh
$M --name fits-warmup --workers 4 --log $A/logs/fits-warmup.log -- $PY scripts/cp22_revision.py job fits --stage warmup --workers 4
$M --name admission   --workers 1 --log $A/logs/admission.log   -- $PY scripts/cp22_revision.py job admission
git add reports/v4-revision/lineage.json && git commit           # the admission freeze
```

PN is fitted at warm-up and admission origins on data materialised before each fold's first
evaluation day; each origin's eight fits are cached as `$A/fits/<fold>/<day>/PN.json`, bound to the
frozen protocol, inputs and weather design (a verified hit is reused; a miss is a charged fit).

## 3. Outer stage and pass 1 (`cp22-replacement`)

```sh
$M --name fits-evaluation --workers 4 --log $A/logs/fits-evaluation.log -- $PY scripts/cp22_revision.py job fits --stage evaluation --workers 4
$M --name comparison --workers 1 --log $A/logs/comparison.log -- $PY scripts/cp22_revision.py job comparison
git add reports/v4-revision/{predictions.parquet,members.parquet,lineage.json} && git commit   # vectors before scoring
$M --name parity --workers 1 --log $A/logs/parity.log -- $PY scripts/cp22_revision.py job parity
$M --name score-replacement --workers 1 --log $A/logs/score-replacement.log -- $PY scripts/cp22_revision.py job score-replacement
git add reports/v4-revision/{replacement.json,pass1,lineage.json,parity.json} && git commit
```

## 4. Only if a winner W exists: the layer arms and pass 2

```sh
$M --name w-admission  --workers 1 --log $A/logs/w-admission.log  -- $PY scripts/cp22_revision.py job w-admission
git add reports/v4-revision/lineage-w.json && git commit         # the W-arm admission freeze
$M --name w-comparison --workers 1 --log $A/logs/w-comparison.log -- $PY scripts/cp22_revision.py job w-comparison
git add reports/v4-revision/{predictions-w.parquet,lineage-w.json} && git commit
```

## 5. Final tables, controls and diagnostics

```sh
$M --name score         --workers 1 --log $A/logs/score.log         -- $PY scripts/cp22_revision.py job score
$M --name controls      --workers 1 --log $A/logs/controls.log      -- $PY scripts/cp22_revision.py job controls
$M --name reproduce     --workers 1 --log $A/logs/reproduce.log     -- $PY scripts/cp22_revision.py job reproduce
$M --name fit-cost      --workers 1 --log $A/logs/fit-cost.log      -- $PY scripts/cp22_revision.py job fit-cost
$M --name daily-cycle   --workers 4 --log $A/logs/daily-cycle.log   -- $PY scripts/cp22_revision.py job daily-cycle
$M --name investigation --workers 1 --log $A/logs/investigation.log -- $PY scripts/cp22_revision.py job investigation
```

With no winner, `score` makes no further pass: the pass-1 tables are the final tables.

## 6. Packet, draft export and local tracking

```sh
PYTHONPATH=src $PY -m cp22.packet                     # reports/v4-revision/draft-registry.json
$PY scripts/mlflow_export.py --draft cp22             # reports/v4-revision/mlflow-export-draft/cp22.json
$M --name mlflow-local --workers 1 --log $A/logs/mlflow-local.log -- $PY scripts/cp22_revision.py job mlflow-local
PYTHONPATH=src $PY -m cp22.claims                     # the claim map and the publication packet
$M --name finalise --workers 1 --log $A/logs/finalise.log -- $PY scripts/cp22_revision.py job finalise
$PY scripts/mlflow_export.py --check                  # the published export set is unchanged
PYTHONPATH=src $PY -m pytest -q tests/cp22            # fixtures, scoring logic, draft export
```

## 7. Independent review

The Integration Critic works on a clean detached checkout of the final candidate and recomputes
from committed rows through `python -m cp22.review` (charged as review): the scores, intervals and
the three verdicts (one reference and one bootstrap pass), a representative PN selection and
average, and a DL update replayed from the committed admission-freeze states.
