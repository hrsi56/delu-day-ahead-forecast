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

from delu_forecast.claims import (  # noqa: E402
    build_claims,
    limitation_bullets,
    reproducibility_bullets,
)

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


def card_body(C, deployed: str, limitations: str, reproduction: str) -> str:
    """Everything after a card's introduction, shared by the container card and
    the Static Space card so the two cannot drift in what they claim.

    `deployed` is the one section that genuinely differs: what artifact the card
    describes and how it executes.
    """
    return f"""## The four cutoffs, stated separately because they are four different dates

| Cutoff | Value |
|---|---|
| `snapshot_cutoff` | {C['snapshot_cutoff']} |
| `raw_model_fit_cutoff` | {C['raw_model_fit_cutoff']} |
| `final_calibration_window` | {C['final_calibration_window']} |
| `holdout_window` | {C['holdout_window']} |

{C['shipped_is_evaluated']} The raw-model fit cutoff precedes the snapshot cutoff by
{C['staleness_days']} delivery days; that is what shipping the evaluated model costs, and
it is stated rather than hidden. {C['floor_change']}

{deployed}

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
confirmatory. **{C['development_dm_point_reading']}** The probabilistic win is broad and
the point-accuracy win is not. That is reported here rather than omitted.

## What the post-gate forecast would have been worth

A controlled raw-head ablation, neither arm calibrated: adding the delivery-day A69 VRE
forecast and its named derivatives moves pooled mean pinball loss from
`{C['benchmark_strict_loss']}` to `{C['benchmark_a69_loss']}` — **{C['benchmark_pct']}**.

> {C['benchmark_limitation']}

## Limitations

{limitations}
- **Scenario probes.** {C['sensitivity_probe_label']} They hold every other input fixed, so a
  large perturbation asks the model a question it was never trained on.

> {C['holdout_limitation']}

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

{reproduction}

The DagsHub repository UI is deliberately not linked anywhere: it redirects an anonymous
visitor to a sign-in page, while the `.mlflow` tracking URI above is anonymously readable.
"""


def docker_deployed_section(C) -> str:
    return f"""## What is deployed

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
"""


def build_card() -> str:
    C = build_claims()
    limitations = "\n".join(f"- {bullet}" for bullet in limitation_bullets(C))
    reproduction = "\n".join(f"- {bullet}" for bullet in reproducibility_bullets(C))
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
It is CDN-served and performs zero runtime calls. **This card describes the container
bundle, which is not what Hugging Face hosts.** On 2026-07-08 Hugging Face moved the Docker
SDK behind a paid plan, and a free Docker Space sleeps after inactivity. The hosted
interactive demo is therefore a Static Space built from `app/wasm_showcase.py`, which
cannot sleep; this bundle remains runnable locally and is verified under
`docker run --network none` by `make container-verify`.

> **{C['replay_label']}**

Anything this Space renders over the holdout window {C['holdout_window']} is a replay of
a frozen model against a period it never trained on. It is never presented as a live
forecast, and the demo makes no live API call during a session: the champion and the
data snapshot are **bundled in the image**.

{card_body(C, docker_deployed_section(C), limitations, reproduction)}"""


#: Development prediction frames are CP-2 evidence, not runtime inputs. Only the
#: holdout frame is readable by the showcase, so only it travels.
_RUNTIME_PARQUET = {"holdout_predictions.parquet"}

#: `reports/cp3/` holds this checkpoint's own build records -- including this
#: manifest. Copying it would make `total_bytes` measure its own siblings and the
#: manifest would stop being reproducible; the Space needs none of it.
#: `__marimo__` is the session cache marimo writes beside the notebook when the
#: app runs: gitignored, ~1 MB, and its presence would make the bundle depend on
#: whether anyone had started the app before building it.
#: `reports/cp3b/` is the WASM checkpoint's evidence (network logs, equivalence
#: records) -- it changes on every WASM rebuild and would make this manifest stale
#: for reasons that have nothing to do with the container.
_EXCLUDED_DIRS = {"__pycache__", "__marimo__", "cp3"}

#: ...except the two records `claims.py` reads. The claim set must build wherever
#: the app runs; excluding its inputs crashed the CLI inside the container, and
#: `make container-verify` caught it.
_CP3B_CLAIM_INPUTS = {"network.json", "equivalence.json"}


def _ignore(directory: str, names: list[str]) -> set[str]:
    skipped = {
        name
        for name in names
        # The CP-3B browser payload is the Static Space's, not the container's.
        if (Path(directory).name == "app" and name == "public")
        or name in {".DS_Store"}
        or name.endswith(".pyc")
        or (name in _EXCLUDED_DIRS and Path(directory, name).is_dir())
    }
    skipped |= {
        name for name in names if name.endswith(".parquet") and name not in _RUNTIME_PARQUET
    }
    if Path(directory).name == "cp3b":
        skipped |= {name for name in names if name not in _CP3B_CLAIM_INPUTS}
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
