# CP-15 reproduction — v21-r1

Run from the CP-15 checkout root. Keep `data/snapshot.parquet` and the preserved
CP-2/v1 prediction artifacts available at their recorded paths. `protocol.json`
checks the exact input, inherited-source, governance and dependency-lock hashes
before loading comparison inputs. The snapshot scan projects only the four
permitted fields and filters the 2019-01-01 through 2026-04-07 boundary before
materializing rows. No remote experiment service is required.

The inherited WASM regression tests require the ignored `app/public/` payload.
For detached CP-15 review, the Lead copies it byte-identically from the retained
checkpoint checkout and records the payload file hashes in `validation.json`.
It is an inherited test fixture, not a CP-15 application change. A standalone
clone can obtain this prerequisite using the existing repository's WASM payload
build instructions; keep that setup separate from CP-15 forecast regeneration.

## Frozen core environment and controls

The executed core interpreter is CPython **3.13.15**, macOS arm64. All package
versions resolve from the unchanged `uv.lock`: NumPy 2.4.6, pandas 3.0.3,
PyArrow 25.0.1, scikit-learn 1.9.1 and LightGBM 4.7.0. The separate probe uses
Python 3.12.14 and its own exact requirements freeze.

```sh
uv sync --frozen --offline --python 3.13.15
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=4 uv run --frozen python scripts/cp15_forecasting.py --inspect
CP15_REQUIRE_SAVED_EVIDENCE=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=4 uv run --frozen pytest -q
```

Expected original eligible counts: fold_1=2160, fold_2=2159, fold_3=2112,
fold_4=2160, fold_5=2156. Warm-up starts: 2020-06-02, 2021-03-01,
2022-06-02, 2025-03-30 and 2025-12-10 respectively. The final saved-evidence
environment variable makes missing production evidence a failure; it must not
be omitted for final review. The independent checker re-derives scores,
qualification, original rows, issued residuals and fit lineage without calling
the CP-15 model or score implementation. Synthetic mutation fixtures verify that
the checker catches incorrect evidence. See `validation.json` for actual runs.

## Uncached representative production fits and causal controls

Use new external output paths. These commands never reuse the central cache or
overwrite saved reports. They fit all five statistical components, reconstruct
the eight new central policies, compare every issued hour, and require matching
training, target, normalization and model fingerprints. Center tolerance is
`atol=1e-8, rtol=1e-10`; exact fingerprint matches are separately required.

```sh
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=4 uv run --frozen python -m cp15.reproduce_fit --fold fold_1 --day 2020-07-01 --causal-controls --output /tmp/cp15-fit-control-2020-07-01.json
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=4 uv run --frozen python -m cp15.reproduce_fit --fold fold_3 --day 2022-08-15 --output /tmp/cp15-fit-control-2022-08-15.json
```

The first origin exercises capped expanding history and exact A4 history.
Its negative control masks every price from D onward and changes load strictly
after D; forecasts and fitted-model hashes must stay identical. Its positive
control adds 500 EUR/MWh only to already available D-1 prices; every fitted
policy must respond. The crisis origin exercises the full rolling long window.
Neither command calculates a score or chooses new parameters.

## Full comparison regeneration

This can take hours on the local CPU. A new cache path forces every daily fit;
using the documented existing cache reuses only hash-bound central forecasts and
their original fit records. Each fold has independent chronological feedback.
The actual production execution used two queues (folds 1/3/5 and folds 2/4),
with at most two fold processes concurrent. Sequential execution below is also
valid and gives the same forecasts; wall time and process RSS are not byte-stable.

```sh
for fold in fold_1 fold_2 fold_3 fold_4 fold_5; do
  OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=4 uv run --frozen python scripts/cp15_forecasting.py --fold "$fold" --output /tmp/cp15-full-reproduction --cache /tmp/cp15-new-fit-cache || break
done
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OMP_NUM_THREADS=4 uv run --frozen python scripts/cp15_forecasting.py --score --output /tmp/cp15-full-reproduction
```

All five fold files are required before scoring. Expect nine policies × 10,747
targets = 96,723 prediction rows, 45 policy/fold summaries, nine 408-hour peak
summaries and 240 bootstrap contrasts. Match predictions by policy, fold and
timestamp, comparing numeric outputs at `atol=1e-8, rtol=1e-10` rather than
comparing timing or Parquet container bytes. Saved-score arithmetic is checked
at `atol=rtol=2e-12`. Bootstrap seed 15042; model seed 42; quantiles use linear
empirical interpolation; no output projection or clipping.

## Probe reproduction without changing reviewed evidence

The exact public model revision and Apache-2.0 license were verified before the
free download. Copy the documented ignored `data/cp15-probe-cache/huggingface/`
cache with blobs and symlinks intact. The pinned weight digest is in
`feasibility/model_verification.json` and `feasibility/probe_result.json`.

```sh
uv venv --python 3.12.14 data/cp15-probe-env
uv pip install --offline --python data/cp15-probe-env/bin/python -r reports/cp15/feasibility/requirements.freeze.txt
uv run --frozen python -m cp15.reproduce_probe --python data/cp15-probe-env/bin/python --scratch /tmp/cp15-fresh-probe
```

Expected exit 0 and four identical SHA256 comparisons: context, future load,
input manifest, and unscored forecast CSV. A new external scratch directory is
required. The helper preserves the reviewed evidence. If the public-model cache
is absent, the explicit `--allow-download` option permits only the already
verified pinned read; no paid service, registry write or upload is involved.
The isolated process keeps the same 4 GiB RSS / 600-second ceiling. This is an
API/resource probe, not a model-quality estimate.

## Evidence map

- `protocol.json`: complete pre-run choices and input hashes.
- `folds/*-predictions.parquet`, `predictions.parquet`: actual issued evaluation vectors.
- `folds/*-issued.parquet`: immutable central forecasts and origin scale, including warm-up.
- `folds/*-fits.parquet`: chronological split, row/target/normalization/model hashes, solver records and fit durations.
- `folds/*-feedback.parquet`, `folds/*-origins.json`: one-time delayed releases and exact residual buffers.
- `per_fold.csv`, `pooled.csv`, `hourly_losses.csv`, `daily.csv`, `peak.csv`, `recovery.csv`: complete metrics and diagnostics.
- `relative_scores.csv`, `ranking.csv`, `criteria.csv`, `selection.json`: mechanical selection and screening.
- `bootstrap.csv`, `bootstrap_metadata.json`: exploratory dependence-aware paired uncertainty.
- `resources.csv`, `lineage_summary.csv`: all-arm runtime/memory accounting and warm-up/evaluation history summary.
- `feasibility/`: both required feasibility deliverables, primary-source retrieval and reproduction records.
- `implementation-notes.md`, `validation.json`: actual numerical repairs and executed validation.
- `artifact-manifest.json`: final source/test/report digests, excluding itself and subsequent Integration evidence.
- `attempt-1-preservation.json`: byte-identical history mapping; original FAIL remains distinct.

Only the later fresh Integration verdict can certify the exact final candidate.
Builder checks and passing inherited tests do not substitute for that review.
The candidate's `report.md` therefore labels engineering review as pending.
After review, `docs/track-b/evidence/cp-15/report.md` records the actual engineering
verdict alongside product feasibility and the same reviewed results, binding
the candidate SHA. This status copy and the verdict are evidence-only additions;
the candidate's statistical artifacts remain unchanged.
