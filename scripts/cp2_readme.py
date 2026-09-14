"""CP-2 stage 6 -- regenerate the README's CP-2 section from the committed artifacts.

Committed and `make`-able for the same reason the model report is generated: the
section states a dozen numbers and a claim about which folds the champion wins,
and hand-maintained prose is where those drift out of agreement with the data.

    uv run python scripts/cp2_readme.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from delu_forecast.claims import MLFLOW_URL as TRACKING_URL  # noqa: E402
from delu_forecast.claims import build_claims  # noqa: E402

OUT = Path("reports/cp2")
README = Path("README.md")
HEADING = "## CP-2 model, calibration and analysis"
NEXT_HEADING = "## CP-3 showcase and release\n"


def build_section() -> str:
    # Every published number comes from the one claim set the README, the Pages
    # export, the Space card and the MLflow record all render from (CP-3 item 5).
    # Rounding a figure differently here is exactly the drift that item exists to
    # catch, so this file no longer formats any of them itself.
    C = build_claims()
    selection = json.loads((OUT / "catalog_selection.json").read_text())
    per_fold = pd.read_csv(OUT / "development_metrics.csv")
    champion = C["selected_catalog"]

    mae = per_fold.pivot_table(index="fold", columns="model", values="mae_final_p50")
    pinball = per_fold.pivot_table(index="fold", columns="model", values="pinball_final")
    weights = per_fold[per_fold["model"] == champion].set_index("fold")["n_eval"]
    weights = weights / weights.sum()
    contribution = (mae[champion] - mae["similar_day_naive"]) * weights
    tallies = {
        "n_folds": int(len(mae)),
        "mae_wins": int((mae[champion] < mae["similar_day_naive"]).sum()),
        "pinball_wins": int((pinball[champion] < pinball["similar_day_naive"]).sum()),
        "worst_fold": str(contribution.idxmax()),
        "worst_contribution": float(contribution.max()),
        "pooled_gap": float(contribution.sum()),
        "augmented_fold_wins": int(
            (
                per_fold.pivot_table(index="fold", columns="model", values="pinball_raw")
                .loc[:, ["base", "base_plus_residual_load_proxy"]]
                .idxmin(axis=1)
                == "base_plus_residual_load_proxy"
            ).sum()
        ),
    }

    return f"""{HEADING}

**The two-arm comparison, numbers first.** The two frozen catalogs were compared once on raw heads
over the five pinned folds with matched rows, seed, hyperparameters and (zero) tuning budget. Pooled
observation-weighted mean pinball loss, unrounded as stored:

| Arm | Pooled raw-head mean pinball loss |
|---|---|
| `base` | `{C["catalog_base_loss"]}` |
| `base + residual_load_proxy` | `{C["catalog_augmented_loss"]}` |

Percentage difference (augmented vs base): **{C["catalog_pct"]}**.

**Selected catalog: `{champion}`.** The augmented catalog ships only if its unrounded stored pooled
loss is lower; it is not, so the champion ships strict-gate as `base`. The domain feature did not
earn its place on the pooled metric that decides, and that is a reportable result, not a failure.
The fold-level picture is not uniform — the augmented arm is lower on
{tallies["augmented_fold_wins"]} of the {tallies["n_folds"]} folds, and the report gives that table —
but §4.1 fixes the rule as pooled and fixes it before fitting, so the split is disclosed and the
decision is not revisited.

**Development metrics are descriptive post-selection evidence** (`evidence_class =
{C["development_evidence_class"]}`), never confirmatory superiority. The point-accuracy DM on those
folds shows **no evidence of advantage** — p = {C["development_dm_point_p_value"]}, statistic
{C["development_dm_point_statistic"]}, over {C["development_days"]} days — reported here rather than
omitted. The probabilistic daily-vector DM on the same folds reads statistic
{C["development_dm_pinball_statistic"]}, p = {C["development_dm_pinball_p_value"]}. The champion beats the similar-day
naive on mean pinball loss in {tallies["pinball_wins"]} of the {tallies["n_folds"]} evaluation
blocks and on median MAE in {tallies["mae_wins"]} of {tallies["n_folds"]}: the probabilistic win is
broad, the point-accuracy loss is not. The pooled MAE gap of {tallies["pooled_gap"]:+.2f} EUR/MWh
comes almost entirely from **{tallies["worst_fold"]}**, the crisis-peak block, which contributes
{tallies["worst_contribution"]:+.2f} of it alone. The mechanism is measured, not assumed: the model did see the crisis — that fold's training ran to 2022-04-29 and included
5,784 crisis hours at a 173 EUR/MWh mean and a 700 EUR/MWh maximum — but **61.3% of the evaluation
block sits above the 99th percentile of everything it ever saw, while only 2.45% exceeds its
maximum.** So this is shrinkage toward the training level, not an extrapolation wall: a leaf's value
is an average over the training rows that fall in it, and the far more numerous moderate-price rows
pull the prediction down. Persistence has no training distribution at all, so it carries the level
for free. Full tables, both DM
analyses, the three-stage reliability read, SHAP, permutation importance and the regime-stratified
table are in [`docs/cp2-model-report.md`](docs/cp2-model-report.md) and `reports/cp2/`.

**One pre-specified holdout evaluation, opened once.** Champion MAE {C["holdout_mae_champion"]} vs
similar-day naive {C["holdout_mae_naive"]} EUR/MWh
({C["holdout_mae_pct"]}); champion mean pinball loss
{C["holdout_pinball_champion"]} vs {C["holdout_pinball_naive"]}
({C["holdout_pinball_pct"]}); final empirical coverage
{C["holdout_coverage_50"]} / {C["holdout_coverage_80"]} /
{C["holdout_coverage_95"]} at the 50 / 80 / 95 % nominal levels; probabilistic
daily-vector DM statistic {C["holdout_dm_statistic"]}, p = {C["holdout_dm_p_value"]},
standardized effect size {C["holdout_dm_effect_size"]}, over
{C["holdout_days"]} delivery days ({C["holdout_rows"]} rows).

> {C["holdout_dm_label"]}

**{C["shipped_is_evaluated"]}** The frozen artifact is `models/champion/`, a single
`mlflow.pyfunc` wrapping the {C["champion_quantiles"]} quantile heads, the selected catalog's
{C["champion_features"]}-feature pipeline, the four CQR thresholds and the isotonic ordering guard,
fit on {C["champion_fit_rows"]} rows and calibrated on {C["champion_calibration_rows"]}. Its identity
is `artifact_fingerprint_sha256` `{C["champion_fingerprint"]}`, recorded in
`models/champion/champion_card.json` and computed over the catalog, the feature list, the nine
quantiles, the four thresholds and the nine boosters' own serializations; the pickle's own bytes are
not stable, because MLflow stamps a fresh UUID and creation time on every save.
`python_model.pkl` is {C["champion_pkl_bytes"]} bytes = {C["champion_pkl_size"]}; the whole
`models/champion/` directory is {C["champion_dir_bytes"]} bytes = {C["champion_dir_size"]}. The
snapshot it reads is pinned at `sha256` `{C["snapshot_sha256"]}`.

**Four cutoffs, stated separately because they are four different dates:**

| Cutoff | Value |
|---|---|
| `snapshot_cutoff` | {C["snapshot_cutoff"]} |
| `raw_model_fit_cutoff` | {C["raw_model_fit_cutoff"]} |
| `final_calibration_window` | {C["final_calibration_window"]} |
| `holdout_window` | {C["holdout_window"]} |

The raw-model fit cutoff precedes the snapshot cutoff by
{C["staleness_days"]} delivery days (1 + 60 + 1 + 90). That
is what shipping the evaluated model costs, and it is stated plainly rather than apologised for.

**What the post-gate forecast would have been worth.** A controlled ablation, raw heads, neither arm
calibrated: adding the delivery-day A69 forecast and its derivatives moves pooled mean pinball loss
from `{C["benchmark_strict_loss"]}` to `{C["benchmark_a69_loss"]}` — **{C["benchmark_pct"]}**.

> {C["benchmark_limitation"]}

**Experiment records** for every decision-bearing run — the three baselines, both catalog
candidates, both benchmark arms, the champion's final fit and holdout — are public at
<{TRACKING_URL}> with snapshot hash, code SHA, fold spec, feature list, seed, hyperparameters,
metrics and artifact links.

Reproduce with `make cp2` after `uv sync`; every stage runs offline and MLflow logging is skipped
silently when `MLFLOW_TRACKING_URI` is unset.

"""


def main() -> None:
    section = build_section()
    text = README.read_text()
    if HEADING in text:
        head, _, rest = text.partition(HEADING)
        _, _, tail = rest.partition(NEXT_HEADING)
        text = head + section + NEXT_HEADING + tail
    else:
        text = text.replace(NEXT_HEADING, section + NEXT_HEADING, 1)
    README.write_text(text)
    print(f"regenerated the {HEADING!r} section of {README}")


if __name__ == "__main__":
    main()
