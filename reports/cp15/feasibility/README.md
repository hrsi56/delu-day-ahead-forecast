# Chronos-2 and structural-input feasibility — CP-15

**Result: actual local load and inference completed, unscored.** This is an API/resource feasibility result on one admissible historical origin. It is not a CP-15 candidate, neural benchmark, accuracy result or ranking. All computed outputs are `development_post_selection`.

Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0.

## What ran

- **Model:** `amazon/chronos-2`, exact public revision `29ec3766d36d6f73f0696f85560a422f50e8498c`. Hugging Face metadata and its revision-specific card were checked **before** weights were downloaded: public, ungated, Apache-2.0. See `model_verification.json`. [Pinned model card](https://huggingface.co/amazon/chronos-2/blob/29ec3766d36d6f73f0696f85560a422f50e8498c/README.md).
- **Access:** inherited `HF_TOKEN` and `HUGGINGFACE_HUB_TOKEN` were absent. Anonymous public metadata and weight reads succeeded. No credential lookup, authentication workaround, purchase, remote inference, logging service, or upload was needed. The worker disables implicit tokens and HF telemetry.
- **Hardware/environment:** macOS 26.5.2 arm64, local Apple M3 / 16 GiB machine; Python 3.12.14, CPU float32; Torch 2.8.0 with two intra-op threads and one inter-op thread; Chronos Forecasting 2.2.2. `requirements.freeze.txt` pins all 45 installed distributions. `installed_distribution_hashes.json` hashes their METADATA/RECORD files (these are installed-distribution inventory hashes, not downloaded-wheel hashes).
- **Bound:** one 168-hour context, one 24-hour forecast, and one synthetic external-covariate positive control. The supervisor checks process-tree RSS every 0.1 seconds and terminates beyond 4 GiB or 600 seconds. It records failure instead of leaving a stale success result. No training or fine-tuning.
- **External-input path:** `Chronos2Pipeline.predict_df(history, future_df=future, prediction_length=24, quantile_levels=[.1,.5,.9], batch_size=4, context_length=168, cross_learning=False)`. Both context and future frames contain `load_forecast_mw`; only the historical frame contains `target`. Multiplying only future load by 1.2 changed the predicted numeric outputs by up to **41.912918 EUR/MWh**. This is a synthetic API positive control, not an accuracy comparison or estimated effect of load on market prices.

## Information boundary

The fixed delivery day is **2020-04-01**, inside `fold_1.proper_training`. Its inherited forecast origin is **2020-03-31 11:00 UTC** (12:00 fixed CET). Context prices cover **2020-03-24 22:00 UTC through 2020-03-31 21:00 UTC**, exactly the preceding 168 canonical hours; D-1 day-ahead prices are already known from the prior auction even where their delivery is after this forecast origin. The 24 output timestamps run from **2020-03-31 22:00 UTC through 2020-04-01 21:00 UTC**.

Arrow filters and column projections apply before pandas materialization. The future scan requests only timestamp and load; it never requests target-day price, realized generation, A69, or any outer-fold/reserved outcomes. Both context boundaries and delivery day must remain in fold-1 proper training. The snapshot and partition digests must match the committed CP-15 protocol. The UTC hourly sequence crosses Berlin's spring DST change without inventing or dropping an hour. Naive timestamps in the Chronos frame explicitly mean UTC.

Load retains the protocol's inherited A65 known-future assumption. The snapshot does **not** independently prove the original issue vintage. The model’s pretraining corpus may overlap historical electricity data; the probe cannot be described as historically unseen or as a leakage-free foundation-model performance estimate. `input_manifest.json`, `context.csv`, and `future_load.csv` make the exact admitted input reviewable.

## Measured resources

| Measurement | Initial download/run | Offline reproduction |
|---|---:|---:|
| Process wall time including imports, download/cache, hashing and inference | 24.286 s | 4.908 s |
| Peak sampled process-tree RSS | 912,818,176 bytes (0.850 GiB) | 897,204,224 bytes (0.836 GiB) |
| Weight download / cache lookup | 16.279 s | 0.000055 s |
| `from_pretrained` call | 0.0519 s | 0.0513 s |
| First `predict_df` call | 0.1075 s | 0.0935 s |
| Synthetic covariate control | 0.0392 s | 0.0417 s |
| Exit code | 0 | 0 |

Loading uses the library's normal memory-mapped/lazy behavior: the short `from_pretrained` time is not a cold end-to-end start. Full process wall time is reported separately. RSS samples can miss brief peaks and do not measure the whole machine's unified-memory pressure. No MPS run or full-fold throughput claim is made.

Both runs emitted **identical CSV bytes**, SHA-256 `c19601e65f775236f6c570cadc10747ffbb6f60b088f0e81f30598deafc45fe6`. The initial result/log/resources are retained with the `initial_` prefix. The final result binds the hardened source used for offline reproduction; subsequent changes between these runs added source-input/model hash checks and failure-status handling, without changing model inputs or forecasting arguments. No parameter was tuned using outcomes.

## Reproduction (repository root)

Use the isolated environment; do not change the core `pyproject.toml` or `uv.lock`.

```sh
uv venv --python 3.12.14 data/cp15-probe-env
uv pip install --python data/cp15-probe-env/bin/python -r reports/cp15/feasibility/requirements.freeze.txt
# With the documented cache copied from the Builder:
data/cp15-probe-env/bin/python src/cp15/feasibility_probe.py --offline
# Or permit the already verified exact public model download:
data/cp15-probe-env/bin/python src/cp15/feasibility_probe.py
# Standalone input-boundary controls, isolated from core-suite dependencies:
PYTHONPATH=src data/cp15-probe-env/bin/python -m pytest -q -c /dev/null -p no:cacheprovider --confcutdir=tests/cp15 tests/cp15/test_feasibility.py
# Optional read-only refresh of research documentation (no observation acquisition):
python3 reports/cp15/feasibility/refresh_sources.py
```

Actual environment installation initially requested Chronos 2.2.2, Torch 2.8.0, pandas 2.3.3, PyArrow 22.0.0, psutil 7.2.2, pytest 9.0.2, then froze the resolved closure. No core dependencies changed. The two standalone tests passed in 0.58 seconds. An initial test command without `--confcutdir` hit the core suite's `holidays` import, which is intentionally absent from this isolated environment; rerunning with the correct standalone boundary succeeded. This is not a failure or a claimed run of the core regression suite. NumPy/pandas timedelta and library `torch_dtype` deprecation warnings are retained in logs; there were no inference failures or non-finite forecasts.

## Artifacts and cache handoff

- `probe_result.json`, `resources.json`, `probe_execution.log`: final successful offline execution; `initial_*` preserves initial download/run evidence.
- `input_manifest.json`, input CSVs and `probe_predictions_unscored.csv`: exact selected training-only inputs and output, without outcome scores.
- `model_verification.json`, requirements freeze and distribution hashes: revision/license/access and environment identity.
- `structural_inputs.md`, source manifest, `refresh_sources.py`: detailed current-source feasibility assessment and read-only refresh command.
- `artifact_hashes.json`: digest inventory of source/tests/reports, excluding itself.
- `ignored_cache_manifest.json`: paths and sizes for the large ignored environment/model/document caches.

Copy **`data/cp15-probe-cache/huggingface/` with symlinks and blobs intact** into a clean Critic checkout for offline reproduction. Weight file SHA-256 is `ddcda3c7508bf2528087723e98a20707cc04b7f370ae275a9fd88078ddba4f42`, size **477,930,472 bytes**; config/card hashes are in the result. The whole cache is ignored under `data/*`. The environment is recreatable from the freeze; no source installation points at another checkout. Do not publish model caches or research-source bytes as part of this task.

## Structural-input outcome

See `structural_inputs.md`. Sixteen current primary-source pages/documents were successfully fetched (HTTP 200), with dated hashes. The sheet separates source visibility, forecast-origin availability, historical revisions, reuse rights, coverage and missingness. It preserves the inherited data license and refuses post-gate renewable/cross-border products, revised-outage hindsight, pre-2019 modeling inputs and retrospective weather substitutions. Unverified historical vintages and source-specific redistribution rights are explicit gaps; no fundamental model or improvement claim was produced.
