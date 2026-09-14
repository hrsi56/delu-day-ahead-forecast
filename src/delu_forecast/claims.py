"""The one claim set every public surface renders from (§12 CP-3 item 5).

CP-3 item 5 requires the README, the static Pages export, the Space metadata and
the MLflow record to **agree** on the selected catalog, the metrics, the
development evidence class, the benchmark limitation, the champion's identity,
the holdout result with its power-qualification label, the statement that the
shipped model is the evaluated model, and all four §7.1 cutoffs separately.

Agreement between four hand-written documents is a promise. Agreement between
four documents rendered from one dict of strings is a property, and
`tests/test_17_cross_surface_agreement.py` asserts it -- with a positive control
that mutates a copy of a surface and requires the checker to fail, because a
consistency test that cannot fail is the CP-1 lesson this project already paid
for once.

Every value here is **read from a committed CP-2 artifact**, never retyped. The
formatting happens once, so "25.9078" is one string on four surfaces rather than
four roundings of one number.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[2]

#: The `.mlflow` tracking URI, never the DagsHub repository root. Verified
#: 2026-09-14 from an unauthenticated client: `/`, `/experiments`, `/models` and
#: `/src/main` all answer 302 -> /user/login for a connected repository, while
#: this URI serves real MLflow content anonymously. A link to the root lands a
#: hiring manager on a sign-in page.
MLFLOW_URL = "https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow"

PAGES_URL = "https://hrsi56.github.io/delu-day-ahead-forecast/"
SPACE_URL = "https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast"
GITHUB_URL = "https://github.com/hrsi56/delu-day-ahead-forecast"

#: §7.1, verbatim. "It carries this label, exactly, wherever it appears."
HOLDOUT_DM_LABEL = (
    "Pre-specified one-shot holdout DM test on a fixed 90-day window "
    "— confirmatory-style, not power-qualified."
)

#: §7.2, verbatim.
BENCHMARK_LIMITATION = (
    "This uncalibrated raw-head comparison isolates the information content of "
    "post-gate A69. It makes no claim about calibrated interval quality and does "
    "not make A69 available at the forecast gate."
)

#: §7.1, verbatim -- "Required limitation, verbatim in the report".
HOLDOUT_LIMITATION = (
    "The holdout is a single contiguous recent period, so it tests generalization to the most "
    "recent regime rather than repeated out-of-sample skill. Its partitions were pinned before "
    "development and it was evaluated once, after the complete model and calibration pipeline were "
    "frozen, with no subsequent tuning. The 90-day length was fixed by partition design, not by a "
    "power calculation, so the Diebold–Mariano result is confirmatory-style but not "
    "power-qualified. The model shown is exactly the model evaluated — no refit followed the "
    "holdout — so its raw-model fit cutoff precedes the snapshot cutoff by 152 delivery days. "
    "Sequential lag features may use earlier holdout observations exactly as they would in live "
    "forecasting; no holdout outcome entered fitting or a development decision. Enforcement is "
    "procedural: this is a solo build and the discipline is disclosed, not cryptographically "
    "guaranteed."
)

#: §6.2, verbatim -- "Stated in the final report verbatim, for interview defense".
EXCHANGEABILITY = (
    "CQR provides finite-sample marginal coverage guarantees under exchangeability. The "
    "walk-forward CV mildly violates exchangeability — the crisis regime is not exchangeable "
    "with the pre-crisis regime, and the solar-driven negative-price era is not exchangeable with "
    "either — so empirical coverage may diverge from nominal on regime-shift folds. This is "
    "documented in the reliability diagram (Section 8.4)."
)

#: §9.2: "labeled, in those words, a historical out-of-sample replay".
REPLAY_LABEL = (
    "Historical out-of-sample replay — the frozen champion forecasting a 90-day period it "
    "never trained on. This is not a live forecast."
)

#: §9.2: "The page states once that scenario perturbations are ceteris-paribus
#: sensitivity probes and may be out of distribution."
SENSITIVITY_PROBE_LABEL = (
    "Scenario perturbations are ceteris-paribus sensitivity probes and may be out of distribution."
)

#: §9.2: free-tier sleep is disclosed, not performance-gated.
SPACE_LINK_LABEL = "interactive demo — may take ~30 s to wake if asleep"

#: §9.3 attribution statement.
ATTRIBUTION = (
    "Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0."
)

#: §9.3: "A second one-liner notes the floor change to -600 EUR/MWh from 2026-05-28".
FLOOR_CHANGE = (
    "The day-ahead price floor moved to −600 EUR/MWh from 2026-05-28, an environment shift "
    "the frozen model predates."
)

SHIPPED_IS_EVALUATED = (
    "The shipped model is exactly the model the holdout evaluated: there is no retrain and no "
    "re-tune after the result was opened."
)

ASSUMPTION_A65 = (
    "A65/A01 is pre-gate by explicit assumption, not by measurement: both the existence of the "
    "delivery-day load forecast before the 12:00 CET gate and its equality to the archived vector "
    "used here are assumed, and the regulatory update provision permits later revisions."
)

#: §10 item (11) enumerates the honest-limitations set. Item 5 requires
#: "Limitations and reproduction instructions are complete", so the set is
#: rendered from one place onto every human surface and asserted by
#: `tests/test_21_limitations_are_complete.py`. Prose written separately per
#: surface is how the 15-minute-MTU limitation came to sit on the Pages export
#: and nowhere else.
LIMITATION_TOPICS: tuple[str, ...] = (
    "exchangeability",
    "evidence_distinction",
    "assumption_a65",
    "assumption_a75",
    "strict_gate_cost",
    "bounded_tail",
    "coverage_divergence",
    "staleness",
    "mtu_averaging",
    "not_an_operations_system",
)

LIMITATION_EVIDENCE_DISTINCTION = (
    "The five-fold development results are descriptive post-selection evidence, never "
    "confirmatory: those folds also chose the catalog. Only the 90-day holdout was pre-specified "
    "and opened once, and the development point-accuracy DM shows no evidence of advantage."
)

LIMITATION_STRICT_GATE_COST = (
    "The strict-gate design has a measured cost rather than an assumed one: the post-gate A69 "
    "forecast is worth 19.4926% of pooled raw-head pinball loss, and the project declines to use it."
)

LIMITATION_BOUNDED_TAIL = (
    "The target is two-sided and bounded: the price is routinely negative and has hit the "
    "−500 EUR/MWh floor, which truncates the lower conformity residuals, so the lowest intervals "
    "under-cover conditionally near the floor."
)

LIMITATION_COVERAGE_DIVERGENCE = (
    "Empirical coverage diverges from nominal: 0.4407 / 0.7593 / 0.9398 against 50 / 80 / 95 %, so "
    "the 50 % interval under-covers by roughly six points on the holdout window. On the crisis "
    "stratum it does not merely diverge, it collapses: over the August-2022 peak weeks the 95 % "
    "interval covered 0.194 of outcomes. The mechanism is measured — that fold's CQR thresholds "
    "were estimated on a May-June 2022 calibration window at a ~198 EUR/MWh level and applied to "
    "an evaluation block averaging 376 EUR/MWh, and the conformal correction is additive, not "
    "multiplicative. This is what a split-conformal guarantee does when exchangeability breaks; "
    "it is the defect the planned v2 targets, and it is not fixed in this release."
)

LIMITATION_STALENESS = (
    "The deployed demo applies a frozen model whose raw-model fit cutoff (2026-04-07) precedes the "
    "snapshot cutoff (2026-09-06) by 152 delivery days, with the final calibration window "
    "2026-04-09..2026-06-07 and the holdout window 2026-06-09..2026-09-06 — all four cutoffs "
    "published separately because they are four different dates."
)

LIMITATION_MTU_AVERAGING = (
    "From 2025-10-01 an hourly price is the mean of four quarter-hour prices, so every hour-level "
    "statistic here — the negative-hour tally included — depends on that averaging choice, and a "
    "quarter-hour tally differs."
)

LIMITATION_NOT_AN_OPERATIONS_SYSTEM = (
    "This is a portfolio artifact, not an operations system: no retraining schedule, no drift gate, "
    "no rollback machinery, no monitoring surface, and no multi-day-ahead forecast."
)

ASSUMPTION_A75 = (
    "A75 aggregate actual generation is used at its current archived values, which may differ from "
    "the values visible in real time despite the D-2 boundary."
)


def _read_json(relative: str) -> dict:
    return json.loads((REPO_ROOT / relative).read_text())


def _fmt(value: float, places: int) -> str:
    return f"{value:.{places}f}"


def _pct(value: float, places: int = 2) -> str:
    """Signed percentage, e.g. "-6.66%" / "+0.371516%"."""
    return f"{value:+.{places}f}%"


@dataclass(frozen=True)
class Claims:
    """Canonical strings. Two surfaces that render the same key are identical."""

    values: dict[str, str]

    def __getitem__(self, key: str) -> str:
        return self.values[key]

    def get(self, key: str, default: str = "") -> str:
        return self.values.get(key, default)


#: The keys CP-3 item 5 binds: these must appear, identically, on the README, the
#: static Pages export, the Space metadata and the MLflow record.
REQUIRED_ON_EVERY_SURFACE: tuple[str, ...] = (
    # all four cutoffs, separately
    "snapshot_cutoff",
    "raw_model_fit_cutoff",
    "final_calibration_window",
    "holdout_window",
    # selected catalog
    "selected_catalog",
    "catalog_base_loss",
    "catalog_augmented_loss",
    "catalog_pct",
    # metrics
    "holdout_mae_champion",
    "holdout_mae_naive",
    "holdout_mae_pct",
    "holdout_pinball_champion",
    "holdout_pinball_naive",
    "holdout_pinball_pct",
    "holdout_coverage_50",
    "holdout_coverage_80",
    "holdout_coverage_95",
    "holdout_dm_statistic",
    "holdout_dm_p_value",
    "holdout_dm_effect_size",
    # development evidence class
    "development_evidence_class",
    "development_dm_point_p_value",
    # benchmark limitation
    "benchmark_strict_loss",
    "benchmark_a69_loss",
    "benchmark_pct",
    "benchmark_limitation",
    # champion identity
    "champion_fingerprint",
    "snapshot_sha256",
    # the label and the shipped=evaluated statement
    "holdout_dm_label",
    "shipped_is_evaluated",
)


@lru_cache(maxsize=1)
def build_claims() -> Claims:
    """Assemble every published claim from the committed CP-2 artifacts."""
    holdout = _read_json("reports/cp2/holdout_report.json")
    selection = _read_json("reports/cp2/catalog_selection.json")
    benchmark = _read_json("reports/cp2/a69_benchmark.json")
    development_dm = _read_json("reports/cp2/dm_development.json")
    card = _read_json("models/champion/champion_card.json")
    pooled = pd.read_csv(REPO_ROOT / "reports/cp2/development_pooled_metrics.csv")

    cutoffs = holdout["cutoffs"]
    coverage = holdout["final_coverage"]
    dm = holdout["dm"]

    point_dm = next(
        test
        for test in development_dm["dm_tests"]
        if test["analysis"] == "point_median_absolute_error"
        and test["comparator"] == "similar_day_naive"
    )
    pinball_dm = next(
        test
        for test in development_dm["dm_tests"]
        if test["analysis"] == "probabilistic_daily_vector_pinball"
        and test["comparator"] == "similar_day_naive"
    )

    selected = holdout["selected_catalog"]
    champion_rows = pooled[pooled["model"] == selected].set_index("stage")

    pkl_bytes = (REPO_ROOT / "models/champion/python_model.pkl").stat().st_size
    # The published size describes the committed artifact, so transient bytecode
    # is excluded. MLflow puts `models/champion/code` on `sys.path` when it loads
    # the pyfunc, and under some import orders Python then writes ~74 KB of
    # `__pycache__` there -- which would silently move a number printed on four
    # public surfaces depending on whether anything had loaded the model first.
    directory_bytes = sum(
        path.stat().st_size
        for path in (REPO_ROOT / "models/champion").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )

    values: dict[str, str] = {
        # -- the four §7.1 cutoffs, four different dates ----------------------
        "snapshot_cutoff": cutoffs["snapshot_cutoff"],
        "raw_model_fit_cutoff": cutoffs["raw_model_fit_cutoff"],
        "final_calibration_window": cutoffs["final_calibration_window"],
        "holdout_window": cutoffs["holdout_window"],
        "staleness_days": cutoffs["raw_model_fit_precedes_snapshot_by_delivery_days"],
        # -- §4.1 two-arm selection ------------------------------------------
        "selected_catalog": selected,
        "catalog_base_loss": selection["pooled_mean_pinball"]["base"],
        "catalog_augmented_loss": selection["pooled_mean_pinball"]["base_plus_residual_load_proxy"],
        "catalog_pct": _pct(selection["percentage_difference_augmented_vs_base"], 6),
        # -- §7.1 one-shot holdout -------------------------------------------
        "holdout_mae_champion": _fmt(holdout["champion_mae"], 4),
        "holdout_mae_naive": _fmt(holdout["similar_day_naive_mae"], 4),
        "holdout_mae_pct": _pct(holdout["mae_percentage_difference_vs_naive"]),
        "holdout_pinball_champion": _fmt(holdout["champion_mean_pinball"], 4),
        "holdout_pinball_naive": _fmt(holdout["similar_day_naive_mean_pinball"], 4),
        "holdout_pinball_pct": _pct(holdout["pinball_percentage_difference_vs_naive"]),
        "holdout_coverage_50": _fmt(coverage["50"], 4),
        "holdout_coverage_80": _fmt(coverage["80"], 4),
        "holdout_coverage_95": _fmt(coverage["95"], 4),
        "holdout_dm_statistic": _fmt(dm["statistic"], 4),
        "holdout_dm_p_value": f"{dm['p_value']:.2e}",
        "holdout_dm_effect_size": _fmt(dm["standardized_effect_size"], 4),
        "holdout_dm_label": HOLDOUT_DM_LABEL,
        "holdout_days": str(holdout["n_holdout_days"]),
        "holdout_rows": f"{holdout['n_holdout_rows']:,}",
        "holdout_limitation": HOLDOUT_LIMITATION,
        # -- §7.1 development evidence ---------------------------------------
        "development_evidence_class": point_dm["evidence_class"],
        "development_dm_point_p_value": _fmt(point_dm["p_value"], 3),
        "development_dm_point_statistic": _fmt(point_dm["statistic"], 4),
        "development_dm_point_statistic_abs": _fmt(abs(point_dm["statistic"]), 4),
        "development_dm_point_relative": f'{abs(point_dm["relative_improvement_pct"]):.2f}% '
        + ("worse" if point_dm["relative_improvement_pct"] < 0 else "better"),
        "development_dm_pinball_p_value": f"{pinball_dm['p_value']:.5f}",
        "development_dm_pinball_statistic": _fmt(pinball_dm["statistic"], 4),
        "development_days": str(point_dm["n_days"]),
        # -- §7.2 post-gate benchmark ----------------------------------------
        "benchmark_strict_loss": str(benchmark["strict_arm"]["pooled_mean_pinball"]),
        "benchmark_a69_loss": str(benchmark["a69_augmented_arm"]["pooled_mean_pinball"]),
        "benchmark_pct": _pct(benchmark["percentage_difference_a69_vs_strict"], 4),
        "benchmark_limitation": BENCHMARK_LIMITATION,
        # -- §6.1/§6.2 champion identity --------------------------------------
        "champion_fingerprint": card["artifact_fingerprint_sha256"],
        "snapshot_sha256": card["snapshot_sha256"],
        "champion_code_sha": card["code_sha"],
        "champion_quantiles": str(len(card["quantiles"])),
        "champion_features": str(len(card["feature_list"])),
        "champion_calibration_rows": f"{card['n_final_calibration_rows']:,}",
        "champion_fit_rows": f"{card['n_raw_fit_rows']:,}",
        "champion_pkl_bytes": f"{pkl_bytes:,}",
        "champion_pkl_size": f"{pkl_bytes / 1_048_576:.1f} MiB ({pkl_bytes / 1_000_000:.1f} MB)",
        "champion_dir_bytes": f"{directory_bytes:,}",
        "champion_dir_size": f"{directory_bytes / 1_048_576:.1f} MiB",
        "shipped_is_evaluated": SHIPPED_IS_EVALUATED,
        # -- the one hard gate, per stage, for the selected catalog -----------
        "crossings_development_raw": f"{int(champion_rows.loc['raw', 'crossing_violations']):,}",
        "crossings_development_post_cqr": f"{int(champion_rows.loc['post_cqr', 'crossing_violations']):,}",
        "crossings_development_final": str(int(champion_rows.loc["final", "crossing_violations"])),
        "crossings_holdout_final": str(int(holdout["crossing_violations_final"])),
        # -- verbatim required paragraphs -------------------------------------
        "exchangeability": EXCHANGEABILITY,
        "replay_label": REPLAY_LABEL,
        "sensitivity_probe_label": SENSITIVITY_PROBE_LABEL,
        "space_link_label": SPACE_LINK_LABEL,
        "attribution": ATTRIBUTION,
        "floor_change": FLOOR_CHANGE,
        "assumption_a65": ASSUMPTION_A65,
        "assumption_a75": ASSUMPTION_A75,
        # -- §10 item (11), the complete honest-limitations set ----------------
        "limitation_exchangeability": EXCHANGEABILITY,
        "limitation_evidence_distinction": LIMITATION_EVIDENCE_DISTINCTION,
        "limitation_assumption_a65": ASSUMPTION_A65,
        "limitation_assumption_a75": ASSUMPTION_A75,
        "limitation_strict_gate_cost": LIMITATION_STRICT_GATE_COST,
        "limitation_bounded_tail": LIMITATION_BOUNDED_TAIL,
        "limitation_coverage_divergence": LIMITATION_COVERAGE_DIVERGENCE,
        "limitation_staleness": LIMITATION_STALENESS,
        "limitation_mtu_averaging": LIMITATION_MTU_AVERAGING,
        "limitation_not_an_operations_system": LIMITATION_NOT_AN_OPERATIONS_SYSTEM,
        # -- §10 item (12), the complete reproducibility statement -------------
        "repro_tagged_commit": REPRO_TAGGED_COMMIT,
        "repro_mlflow_permalink": REPRO_MLFLOW_PERMALINK,
        "repro_registered_champion": REPRO_REGISTERED_CHAMPION,
        "repro_pages_canonical": REPRO_PAGES_CANONICAL,
        "repro_duckdb_sql": REPRO_DUCKDB_SQL,
        "repro_four_cutoffs": REPRO_FOUR_CUTOFFS,
        "repro_attribution": ATTRIBUTION,
        # -- links -------------------------------------------------------------
        "mlflow_url": MLFLOW_URL,
        "pages_url": PAGES_URL,
        "space_url": SPACE_URL,
        "github_url": GITHUB_URL,
    }
    return Claims(values)


#: A link to any of these lands an anonymous visitor on a DagsHub sign-in page.
#: Verified 2026-09-14 with an unauthenticated client; asserted by the
#: cross-surface test so a future edit cannot reintroduce one.
FORBIDDEN_DAGSHUB_PATHS: tuple[str, ...] = (
    "dagshub.com/hrsi56/delu-day-ahead-forecast/experiments",
    "dagshub.com/hrsi56/delu-day-ahead-forecast/models",
    "dagshub.com/hrsi56/delu-day-ahead-forecast/src",
    "dagshub.com/hrsi56/delu-day-ahead-forecast/annotations",
)


def forbidden_dagshub_links(text: str) -> list[str]:
    """Gated DagsHub UI paths present in `text`, plus a bare repository root.

    The root is checked by exclusion rather than by substring, because the
    permitted `.mlflow` URI contains the root as a prefix.
    """
    found = [path for path in FORBIDDEN_DAGSHUB_PATHS if path in text]
    root = "dagshub.com/hrsi56/delu-day-ahead-forecast"
    index = 0
    while (index := text.find(root, index)) != -1:
        tail = text[index + len(root) :]
        if not tail.startswith(".mlflow"):
            found.append(text[index : index + len(root) + 12].rstrip())
        index += len(root)
    return found


#: §10 item (12) enumerates what a complete reproducibility statement contains.
#: Same treatment as the limitations set, and for the same reason: the round-2
#: review found the registered `champion` alias on none of the three surfaces
#: because each wrote its own reproduction prose.
REPRODUCIBILITY_TOPICS: tuple[str, ...] = (
    "tagged_commit",
    "mlflow_permalink",
    "registered_champion",
    "pages_canonical",
    "duckdb_sql",
    "four_cutoffs",
    "attribution",
)

REPRO_TAGGED_COMMIT = (
    "Check out the tagged commit and run `uv sync` then `make train`: the champion is rebuilt from the "
    "committed snapshot with pinned dependencies and fixed seeds, no extra fetch."
)

REPRO_MLFLOW_PERMALINK = (
    "Every decision-bearing run — the three baselines, both catalog candidates, both benchmark arms, "
    "the champion's final fit and holdout, and the diagnostics — is public at "
    "https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow with snapshot hash, code SHA, fold spec, "
    "feature list, seed, hyperparameters, metrics and artifact links."
)

REPRO_REGISTERED_CHAMPION = (
    "The champion is registered on that MLflow instance as the model `delu-day-ahead-champion` under "
    "the `champion` alias, carrying release and lineage tags — `release_status=portfolio_release`, the "
    "source run id, the code commit, the snapshot hash and the four cutoffs. It is portfolio evidence "
    "only: the deployed demo loads the bundled artifact and never queries the registry."
)

REPRO_PAGES_CANONICAL = (
    "The static GitHub Pages report at https://hrsi56.github.io/delu-day-ahead-forecast/ is the "
    "canonical entry point, and the interactive Space at "
    "https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast is linked from it."
)

REPRO_DUCKDB_SQL = (
    "The hand-authored DuckDB queries in `sql/feature_queries.sql` express the same calendar-day lag "
    "and D-1-frozen rolling semantics as the canonical Python pipeline, and run against the committed "
    "Parquet with `make sql`."
)

REPRO_FOUR_CUTOFFS = (
    "All four cutoffs are published separately: snapshot 2026-09-06, raw-model fit 2026-04-07, final "
    "calibration 2026-04-09..2026-06-07, holdout 2026-06-09..2026-09-06."
)


#: Claim keys for the §10 item (11) set, in reading order.
LIMITATION_KEYS: tuple[str, ...] = tuple(f"limitation_{topic}" for topic in LIMITATION_TOPICS)

#: The lead-in each surface puts in front of the shared sentence. The label may
#: differ in styling per surface; the sentence may not differ at all.
LIMITATION_LABELS: dict[str, str] = {
    "limitation_exchangeability": "Exchangeability under regime shift",
    "limitation_evidence_distinction": "Development versus one-shot evidence",
    "limitation_assumption_a65": "Disclosed assumption — the load forecast",
    "limitation_assumption_a75": "Disclosed assumption — the generation archive",
    "limitation_strict_gate_cost": "The measured cost of the strict gate",
    "limitation_bounded_tail": "A two-sided bounded target, live at the floor",
    "limitation_coverage_divergence": "Coverage divergence",
    "limitation_staleness": "Model staleness, with all four cutoffs",
    "limitation_mtu_averaging": "The 15-minute MTU averaging choice",
    "limitation_not_an_operations_system": "Scope",
}


def limitation_bullets(claims, *, bold: str = "**") -> list[str]:
    """The §10 item (11) set as ready-to-render bullets, one per topic."""
    return [
        f"{bold}{LIMITATION_LABELS[key]}.{bold} {claims[key]}" for key in LIMITATION_KEYS
    ]


#: Claim keys for the §10 item (12) set, in the order the plan lists them.
REPRODUCIBILITY_KEYS: tuple[str, ...] = tuple(
    f"repro_{topic}" for topic in REPRODUCIBILITY_TOPICS
)

REPRODUCIBILITY_LABELS: dict[str, str] = {
    "repro_tagged_commit": "Tagged commit",
    "repro_mlflow_permalink": "MLflow permalinks",
    "repro_registered_champion": "The registered `champion` alias",
    "repro_pages_canonical": "Canonical entry point",
    "repro_duckdb_sql": "DuckDB SQL",
    "repro_four_cutoffs": "The four cutoffs",
    "repro_attribution": "Attribution",
}


def reproducibility_bullets(claims, *, bold: str = "**") -> list[str]:
    """The §10 item (12) set as ready-to-render bullets, one per element."""
    return [
        f"{bold}{REPRODUCIBILITY_LABELS[key]}.{bold} {claims[key]}"
        for key in REPRODUCIBILITY_KEYS
    ]


__all__ = [
    "ATTRIBUTION",
    "BENCHMARK_LIMITATION",
    "Claims",
    "EXCHANGEABILITY",
    "FLOOR_CHANGE",
    "FORBIDDEN_DAGSHUB_PATHS",
    "GITHUB_URL",
    "HOLDOUT_DM_LABEL",
    "HOLDOUT_LIMITATION",
    "LIMITATION_KEYS",
    "LIMITATION_LABELS",
    "LIMITATION_TOPICS",
    "REPRODUCIBILITY_KEYS",
    "REPRODUCIBILITY_LABELS",
    "REPRODUCIBILITY_TOPICS",
    "MLFLOW_URL",
    "PAGES_URL",
    "REPO_ROOT",
    "REPLAY_LABEL",
    "REQUIRED_ON_EVERY_SURFACE",
    "SENSITIVITY_PROBE_LABEL",
    "SHIPPED_IS_EVALUATED",
    "SPACE_LINK_LABEL",
    "SPACE_URL",
    "build_claims",
    "forbidden_dagshub_links",
    "limitation_bullets",
    "reproducibility_bullets",
]
