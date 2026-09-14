"""CP-2 stage 6 -- regenerate the README's CP-2 section from the committed artifacts.

Committed and `make`-able for the same reason the model report is generated: the
section states a dozen numbers and a claim about which folds the champion wins,
and hand-maintained prose is where those drift out of agreement with the data.

    uv run python scripts/cp2_readme.py
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

OUT = Path("reports/cp2")
README = Path("README.md")
HEADING = "## CP-2 model, calibration and analysis"
NEXT_HEADING = "## Setup\n"
TRACKING_URL = "https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow"


def build_section() -> str:
    selection = json.loads((OUT / "catalog_selection.json").read_text())
    holdout = json.loads((OUT / "holdout_report.json").read_text())
    benchmark = json.loads((OUT / "a69_benchmark.json").read_text())
    per_fold = pd.read_csv(OUT / "development_metrics.csv")
    cutoffs = holdout["cutoffs"]
    champion = selection["selected_catalog"]

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
| `base` | `{selection["pooled_mean_pinball"]["base"]}` |
| `base + residual_load_proxy` | `{selection["pooled_mean_pinball"]["base_plus_residual_load_proxy"]}` |

Percentage difference (augmented vs base): **{selection["percentage_difference_augmented_vs_base"]:+.4f}%**.

**Selected catalog: `{champion}`.** The augmented catalog ships only if its unrounded stored pooled
loss is lower; it is not, so the champion ships strict-gate as `base`. The domain feature did not
earn its place on the pooled metric that decides, and that is a reportable result, not a failure.
The fold-level picture is not uniform — the augmented arm is lower on
{tallies["augmented_fold_wins"]} of the {tallies["n_folds"]} folds, and the report gives that table —
but §4.1 fixes the rule as pooled and fixes it before fitting, so the split is disclosed and the
decision is not revisited.

**Development metrics are descriptive post-selection evidence** (`evidence_class =
development_post_selection`), never confirmatory superiority. The champion beats the similar-day
naive on mean pinball loss in {tallies["pinball_wins"]} of the {tallies["n_folds"]} evaluation
blocks and on median MAE in {tallies["mae_wins"]} of {tallies["n_folds"]}: the probabilistic win is
broad, the point-accuracy loss is not. The pooled MAE gap of {tallies["pooled_gap"]:+.2f} EUR/MWh
comes almost entirely from **{tallies["worst_fold"]}**, the crisis-peak block, which contributes
{tallies["worst_contribution"]:+.2f} of it alone — an expanding-window model trained only on
pre-crisis data cannot follow an August-2022 level shift, and persistence can. Full tables, both DM
analyses, the three-stage reliability read, SHAP, permutation importance and the regime-stratified
table are in [`docs/cp2-model-report.md`](docs/cp2-model-report.md) and `reports/cp2/`.

**One pre-specified holdout evaluation, opened once.** Champion MAE {holdout["champion_mae"]:.2f} vs
similar-day naive {holdout["similar_day_naive_mae"]:.2f} EUR/MWh
({holdout["mae_percentage_difference_vs_naive"]:+.1f}%); champion mean pinball loss
{holdout["champion_mean_pinball"]:.3f} vs {holdout["similar_day_naive_mean_pinball"]:.3f}
({holdout["pinball_percentage_difference_vs_naive"]:+.1f}%); final empirical coverage
{holdout["final_coverage"]["50"]:.3f} / {holdout["final_coverage"]["80"]:.3f} /
{holdout["final_coverage"]["95"]:.3f} at the 50 / 80 / 95 % nominal levels; probabilistic
daily-vector DM statistic {holdout["dm"]["statistic"]:.2f}, p = {holdout["dm"]["p_value"]:.2g},
standardized effect size {holdout["dm"]["standardized_effect_size"]:.2f}, over
{holdout["dm"]["n_days"]} delivery days.

> {holdout["dm_label"]}

**The shipped model is exactly the model the holdout evaluated.** There is no retrain and no re-tune
after the result was opened. The frozen artifact is `models/champion/`, a single `mlflow.pyfunc`
wrapping the nine quantile heads, the selected catalog's feature pipeline, the four CQR thresholds
and the isotonic ordering guard. Its identity is the `artifact_fingerprint_sha256` recorded in
`models/champion/champion_card.json`; the pickle's own bytes are not stable, because MLflow stamps a
fresh UUID and creation time on every save.

**Four cutoffs, stated separately because they are four different dates:**

| Cutoff | Value |
|---|---|
| `snapshot_cutoff` | {cutoffs["snapshot_cutoff"]} |
| `raw_model_fit_cutoff` | {cutoffs["raw_model_fit_cutoff"]} |
| `final_calibration_window` | {cutoffs["final_calibration_window"]} |
| `holdout_window` | {cutoffs["holdout_window"]} |

The raw-model fit cutoff precedes the snapshot cutoff by
{cutoffs["raw_model_fit_precedes_snapshot_by_delivery_days"]} delivery days (1 + 60 + 1 + 90). That
is what shipping the evaluated model costs, and it is stated plainly rather than apologised for.

**What the post-gate forecast would have been worth.** A controlled ablation, raw heads, neither arm
calibrated: adding the delivery-day A69 forecast and its derivatives lowers pooled mean pinball loss
by {abs(benchmark["percentage_difference_a69_vs_strict"]):.2f}%
(`{benchmark["strict_arm"]["pooled_mean_pinball"]}` → `{benchmark["a69_augmented_arm"]["pooled_mean_pinball"]}`).

> {benchmark["limitation"]}

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
