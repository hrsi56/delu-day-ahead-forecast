#!/usr/bin/env python3
"""Generate the Hugging Face Space card and assemble the deployable bundle (§9.2).

Two outputs:

* `space/README.md` -- the Space's card: HF front-matter plus the body that
  serves as the **Space metadata** surface CP-3 item 5 binds. It is committed, so
  the cross-surface agreement test can check it offline and in CI.
* `dist/space/` -- everything the Space repository needs, assembled from the
  committed tree. Gitignored: it is a copy, not a second source of truth.

Deployment is owner-only. This script builds and verifies; it pushes nothing.
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from delu_forecast.claims import build_claims  # noqa: E402

CARD = ROOT / "space" / "README.md"
BUNDLE = ROOT / "dist" / "space"
MANIFEST = ROOT / "reports" / "cp3" / "space_bundle.json"

#: Everything the image's COPY steps need, plus the card and the LFS rules.
BUNDLE_PATHS: tuple[str, ...] = (
    "Dockerfile",
    ".dockerignore",
    "pyproject.toml",
    "uv.lock",
    "predict_next_day.py",
    "src",
    "app",
    "sql",
    "models/champion",
    "data/snapshot.parquet",
    "data/snapshot.sha256",
    "data/partitions.json",
    "data/README.md",
    "reports",
)

#: `models/champion/python_model.pkl` is ~30 MB and the snapshot ~3 MB; the Hub
#: wants both through LFS.
GITATTRIBUTES = """*.pkl filter=lfs diff=lfs merge=lfs -text
*.parquet filter=lfs diff=lfs merge=lfs -text
"""


def build_card() -> str:
    C = build_claims()
    return f"""---
title: DE-LU Day-Ahead Price Forecasting
emoji: ⚡
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
short_description: Probabilistic DE-LU day-ahead price forecast, strict-gate, one-shot evaluated
tags:
  - energy
  - time-series
  - probabilistic-forecasting
  - conformal-prediction
  - lightgbm
---

# DE-LU day-ahead price forecasting — interactive deep dive

Probabilistic forecasts of the next delivery day's hourly German–Luxembourg day-ahead
electricity price, with calibrated 50 / 80 / 95 % prediction intervals from a LightGBM
nine-quantile ensemble, CQR-calibrated with isotonic monotonicity last.

**The static report is the primary entry point: [{C['pages_url']}]({C['pages_url']}).**
It is CDN-served, cannot sleep, and performs zero runtime calls. This Space is the
interactive deep dive it fronts. On the free tier the Space sleeps after inactivity and
takes roughly 30 s to wake — that is disclosed, not optimised away, and it is never on
the path of a first visit.

> **{C['replay_label']}**

Anything this Space renders over the holdout window {C['holdout_window']} is a replay of
a frozen model against a period it never trained on. It is never presented as a live
forecast, and the demo makes no live API call during a session: the champion and the
data snapshot are **bundled in the image**.

## The four cutoffs, stated separately because they are four different dates

| Cutoff | Value |
|---|---|
| `snapshot_cutoff` | {C['snapshot_cutoff']} |
| `raw_model_fit_cutoff` | {C['raw_model_fit_cutoff']} |
| `final_calibration_window` | {C['final_calibration_window']} |
| `holdout_window` | {C['holdout_window']} |

{C['shipped_is_evaluated']} The raw-model fit cutoff precedes the snapshot cutoff by
{C['staleness_days']} delivery days; that is what shipping the evaluated model costs, and
it is stated rather than hidden. {C['floor_change']}

## What is deployed

The artifact in this image is the **same bundled champion the holdout evaluated** —
`artifact_fingerprint_sha256` `{C['champion_fingerprint']}`: the selected
`{C['selected_catalog']}` catalog's feature pipeline, {C['champion_quantiles']} LightGBM
quantile heads, four CQR thresholds and the isotonic ordering guard, wrapped in one
`mlflow.pyfunc`. `python_model.pkl` is {C['champion_pkl_bytes']} bytes =
{C['champion_pkl_size']}; the whole `models/champion/` directory is
{C['champion_dir_bytes']} bytes = {C['champion_dir_size']}. The frozen snapshot it reads
is pinned at `sha256` `{C['snapshot_sha256']}`.

The pickle's bytes are deliberately not the identity to check — MLflow stamps a fresh
UUID and creation time on every save — so the fingerprint above is computed over the
catalog, the feature list, the nine quantiles, the four thresholds and the nine boosters'
own serializations.

## Selected catalog

| Arm | Pooled raw-head mean pinball loss |
|---|---|
| `base` | `{C['catalog_base_loss']}` |
| `base + residual_load_proxy` | `{C['catalog_augmented_loss']}` |

Percentage difference (augmented vs base): **{C['catalog_pct']}**. **Selected catalog:
`{C['selected_catalog']}`.** The rule was fixed before fitting; the domain feature did not
earn its place, and that is a reportable result rather than a failure.

## The one-shot holdout

| Metric | Champion | Similar-day naive | Difference |
|---|---|---|---|
| MAE (EUR/MWh) | {C['holdout_mae_champion']} | {C['holdout_mae_naive']} | {C['holdout_mae_pct']} |
| Mean pinball loss | {C['holdout_pinball_champion']} | {C['holdout_pinball_naive']} | {C['holdout_pinball_pct']} |

Final empirical coverage over {C['holdout_rows']} rows on {C['holdout_days']} delivery
days: **{C['holdout_coverage_50']}** / **{C['holdout_coverage_80']}** /
**{C['holdout_coverage_95']}** at the 50 / 80 / 95 % nominal levels. Probabilistic
daily-vector DM against the similar-day naive: statistic **{C['holdout_dm_statistic']}**,
p-value **{C['holdout_dm_p_value']}**, standardized effect size
**{C['holdout_dm_effect_size']}**.

> {C['holdout_dm_label']}

## Development evidence, and what it does not say

The five pinned development folds carry `evidence_class =
{C['development_evidence_class']}` — descriptive post-selection evidence, never
confirmatory. The **point-accuracy DM on those folds shows no evidence of advantage**
(p = {C['development_dm_point_p_value']}); the probabilistic win is broad and the
point-accuracy win is not. That is reported here rather than omitted.

## What the post-gate forecast would have been worth

A controlled raw-head ablation, neither arm calibrated: adding the delivery-day A69 VRE
forecast and its named derivatives moves pooled mean pinball loss from
`{C['benchmark_strict_loss']}` to `{C['benchmark_a69_loss']}` — **{C['benchmark_pct']}**.

> {C['benchmark_limitation']}

## Limitations

- {C['exchangeability']}
- {C['holdout_limitation']}
- {C['assumption_a65']}
- {C['assumption_a75']}
- Coverage on the crisis stratum and on negative-price hours is materially worse than
  nominal: the bounded target truncates the lower conformity residuals near the floor.
- {C['sensitivity_probe_label']} They hold every other input fixed, so a large
  perturbation asks the model a question it was never trained on.
- This is a portfolio artifact, not an operations system: no retraining schedule, no
  drift gate, no rollback machinery, no monitoring surface, no multi-day-ahead forecast.

## Reproduction

```bash
git clone {C['github_url']}
cd delu-day-ahead-forecast
uv sync
uv run python predict_next_day.py          # offline, from the bundled snapshot
make test                                   # invariant suite + the CQR fixture
make train && make holdout                  # reproduce the champion and the holdout
docker build -t delu-showcase . && docker run -p 7860:7860 delu-showcase
```

Experiment records: [{C['mlflow_url']}]({C['mlflow_url']}) — the `.mlflow` tracking URI,
which is anonymously readable. The DagsHub repository UI is deliberately not linked: it
redirects an anonymous visitor to a sign-in page.

{C['attribution']}
"""


#: Development prediction frames are CP-2 evidence, not runtime inputs. Only the
#: holdout frame is readable by the showcase, so only it travels.
_RUNTIME_PARQUET = {"holdout_predictions.parquet"}


def _ignore(directory: str, names: list[str]) -> set[str]:
    skipped = {name for name in names if name in {"__pycache__", ".DS_Store"} or name.endswith(".pyc")}
    skipped |= {
        name for name in names if name.endswith(".parquet") and name not in _RUNTIME_PARQUET
    }
    return skipped


def main() -> int:
    CARD.parent.mkdir(parents=True, exist_ok=True)
    CARD.write_text(build_card())
    print(f"wrote {CARD}")

    if BUNDLE.exists():
        shutil.rmtree(BUNDLE)
    BUNDLE.mkdir(parents=True)
    copied: list[str] = []
    for relative in BUNDLE_PATHS:
        source = ROOT / relative
        target = BUNDLE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            shutil.copytree(source, target, ignore=_ignore)
        else:
            shutil.copy2(source, target)
        copied.append(relative)
    shutil.copy2(CARD, BUNDLE / "README.md")
    (BUNDLE / ".gitattributes").write_text(GITATTRIBUTES)

    total = sum(path.stat().st_size for path in BUNDLE.rglob("*") if path.is_file())
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(
            {
                "bundle": str(BUNDLE.relative_to(ROOT)),
                "card": str(CARD.relative_to(ROOT)),
                "paths": [*copied, "README.md", ".gitattributes"],
                "total_bytes": total,
                "app_port": 7860,
                "sdk": "docker",
                "deployment": "owner-only; this script assembles and pushes nothing",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    print(f"assembled {BUNDLE} ({total:,} bytes across {len(list(BUNDLE.rglob('*')))} entries)")
    print(f"wrote {MANIFEST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
