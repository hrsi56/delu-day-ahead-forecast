# CP-20 reproduction — v21-r4 §15

All commands run from the repository root of the reviewed checkout, on CPU, through the
driver monitor, against the **same cumulative CP-20 ledger**. Never create a fresh ledger to
evade cumulative caps; every rerun spends the remaining §15.5 allowances (transfer, message
attempts, policy-days, component and primitive fits, machine-hours) and is refused before a
cap is crossed.

```sh
P=/Users/djourno/Downloads/PJM
PY=$P/.venv/bin/python                          # modelling environment (inherited uv.lock)
WX=$P/.local/artifacts/cp-20/wx-venv/bin/python # extraction environment (admission freeze pins, ecCodes 2.49)
A=$P/.local/artifacts/cp-20                     # ledger, logs, markers, local caches
```

The monitor (`scripts/cp20_weather.py --monitor`) sets BLAS/OpenMP threads to 1, charges
machine time as wall-clock × declared workers, samples process-tree and aggregate RSS and added
disk, refuses a duplicate instance or more than four concurrent workers, keeps the machine
awake with `caffeinate -i -w`, stops at any cap or stop line and writes
`$A/markers/<job>.DONE.json` (exit 0) or `.FAILED.json` (partial, with `abort_reason`).
`--detach` runs it in its own session so it survives the calling shell.

## 1. Extraction environment (once)

```sh
UV_CACHE_DIR=$P/.local/tmp/cp-20/uvcache uv venv $A/wx-venv --python 3.13
UV_CACHE_DIR=$P/.local/tmp/cp-20/uvcache uv pip install --python $WX -r reports/weather-admission/scripts/requirements.freeze.txt pytest==9.1.1
```

## 2. Frozen run manifest and extraction (resumable)

`reports/weather-ablation/run-manifest.json` (2,476 runs; delivery 2019-01-01 structurally
missing) was built by `cp20.plan.build` from the committed CP-16 origin manifest and the
admission inventory. Extraction, resumable and idempotent (completed runs are revalidated by
sha256 and reused; partial runs are redone and their attempts stay counted):

```sh
PYTHONPATH=src $PY -u src/cp20/chain.py
```

The chain controller (r11 plan) runs one endpoint per job, sequentially (r8): `aws-all` (4 workers,
the four deferred failed days excluded), `retry-aws` (4 workers), then `retry-ncar` (4 workers;
the r10 locator fix is first verified on five previously failing days and the job exits 8 if
that fails). Each phase runs

```sh
$PY scripts/cp20_weather.py --monitor --detach --name gfs-extract --workers 4 --stop-machine-hours 100 --log $A/logs/gfs-extract.log -- $WX -u -m cp20.extract --manifest reports/weather-ablation/run-manifest.json --out $A/weather --admission reports/weather-admission --select all --endpoint <aws|ncar> --workers 4 --stop-transfer-gib 150 --inventory-added [--exclude <days>]
```

and every job appends its git HEAD, dirty paths and implementation sha256 to
`$A/weather/job-code-versions.jsonl` (summarised in `chain-code-versions.json`). Repairs r1–r12
and the Owner decisions (O1, O2 with amendment A1, S1, O3, O4) are recorded in
`extraction-repairs.json`.

Outputs (ignored, local): `$A/weather/runs/<run>.npz` (decoded 5 × 10 × 34 × 41 float64 boxes)
and `<run>.json` (per-message URL, byte range, sha256, endpoint, retrieval time, validated
metadata, packing quantum, locate trace), `requests.jsonl`, `attempts.jsonl`,
`added_inventory.jsonl`, raw target messages of the retained-sample runs under `raw/`.
Durable committed summaries are produced by assembly.

## 3. Assembly, conversion and the pre-fit freeze

```sh
$PY scripts/cp20_weather.py --monitor --name assemble --workers 1 --log $A/logs/assemble.log -- $PY -c "from pathlib import Path; from cp20.assemble import run; print(run(Path('.'), Path('$A/weather')))"
```

writes `messages.parquet`, `runs.csv`, `weather-features.parquet`, `missingness.csv`,
`extended-inventory.csv`, `sample-hash-comparison.csv`, `radiation-clipping.csv`,
`extraction-summary.json`. The pre-fit protocol (`cp20.protocol.write`) binds these and the
implementation hashes; it must be committed before any HG fit (`check_protocol` refuses
otherwise).

## 4. Ordered research jobs

```sh
$PY scripts/cp20_weather.py --monitor --name hg-warmup --workers 4 --log $A/logs/hg-warmup.log -- $PY -u -c "from pathlib import Path; from cp20.execution import components; components(Path('.'), 'warmup', 4)"
$PY scripts/cp20_weather.py --monitor --name admission --workers 1 --log $A/logs/admission.log -- $PY -u -c "from pathlib import Path; from cp20.execution import admission; admission(Path('.'))"
# commit reports/weather-ablation/lineage.json (training-only admission freeze) before continuing
$PY scripts/cp20_weather.py --monitor --name hg-evaluation --workers 4 --log $A/logs/hg-evaluation.log -- $PY -u -c "from pathlib import Path; from cp20.execution import components; components(Path('.'), 'evaluation', 4)"
$PY scripts/cp20_weather.py --monitor --name comparison --workers 1 --log $A/logs/comparison.log -- $PY -u -c "from pathlib import Path; from cp20.execution import comparison; comparison(Path('.'))"
$PY scripts/cp20_weather.py --monitor --name controls --workers 1 --log $A/logs/controls.log -- $PY -u -c "from pathlib import Path; from cp20.controls import run; run(Path('.'))"
$PY scripts/cp20_weather.py --monitor --name controls-supplement --workers 1 --log $A/logs/controls-supplement.log -- $PY -u -c "from pathlib import Path; from cp20.controls_supplement import run; run(Path('.'))"
$PY scripts/cp20_weather.py --monitor --name score --workers 1 --log $A/logs/score.log -- $PY -u -c "from pathlib import Path; from cp20.execution import score; score(Path('.'))"
$PY scripts/cp20_weather.py --monitor --name finalise --workers 1 --log $A/logs/finalise.log -- $PY -u scripts/cp20_finalise.py
```

`controls-supplement` (repair r13) and `scripts/cp20_finalise.py` (formatting only) were added
after the pre-fit freeze; see `post-freeze-repairs.json`.

HG component caches live in `$A/hg-components/<fold>/<day>.json`, each content-hashed and bound
to the input fingerprint, weather-design hash and protocol hash; a stale or wrong entry is
refused and refitted (charged), never reused. Admission refuses an existing lineage and
comparison refuses an uncommitted admission freeze.

## 5. Tests and guards

```sh
$PY scripts/cp20_weather.py --monitor --name tests --workers 1 --log $A/logs/tests.log -- $PY -m pytest tests/cp20 -q -p no:cacheprovider --basetemp=$P/.local/tmp/cp-20/pytest
$PY scripts/cp20_weather.py --monitor --name tests-wx --workers 1 --log $A/logs/tests-wx.log -- $WX -m pytest --noconftest tests/cp20/test_gfs_eccodes.py tests/cp20/test_gfs_locator.py -q -p no:cacheprovider --basetemp=$P/.local/tmp/cp-20/pytest-wx
$PY scripts/cp20_weather.py --monitor --name guards --workers 1 --log $A/logs/guards.log -- $PY -m pytest tests/test_02_rolling_closed_left.py tests/test_05_schema_firewall.py tests/test_08_partition_integrity.py tests/test_12_partition_exclusion.py tests/test_24_live_namespace_is_walled_off.py tests/cp16/test_residuals.py tests/cp16/test_scoring.py -q -p no:cacheprovider --basetemp=$P/.local/tmp/cp-20/guards
```

Synthetic tests use no research data or target messages and carry no policy-day or
message-attempt charge. Tolerances: H0 must equal the accepted CP-16 V2-H vectors bitwise;
component reproduction atol 1e-8 / rtol 1e-10 with fingerprint equality; controls require
exactly 0.0 change for delivery-day/future masks and strictly nonzero change for their
positive controls.
