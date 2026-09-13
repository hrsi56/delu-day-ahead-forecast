"""The nine-head LightGBM quantile ensemble and the frozen champion pyfunc (§6.1).

One monolithic model: nine native quantile heads, the selected catalog's feature
pipeline, the four CQR thresholds and the isotonic ordering guard, wrapped in a
single `mlflow.pyfunc.PythonModel` with one `predict`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

import mlflow.pyfunc
import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor

from .conformal import Pair, thresholds_from_json, thresholds_to_json
from .features import build_feature_catalog
from .ingest import BERLIN
from .metrics import QUANTILES
from .postprocess import QUANTILE_LABELS, apply_cqr_thresholds, isotonic_last
from .schema import BENCHMARK_ADDITIONS, catalog_columns, validate_champion_runtime_schema

SEED: int = 42

#: One frozen configuration, used by every LightGBM arm in CP-2. There is no
#: hyperparameter search: §4.1 and §7.2 both require a *matched* tuning budget
#: across arms, and a budget of zero is the only one that is matched by
#: construction rather than by bookkeeping.
LGBM_PARAMS: dict[str, Any] = {
    "objective": "quantile",
    "n_estimators": 600,
    "learning_rate": 0.05,
    "num_leaves": 63,
    "min_child_samples": 40,
    "subsample": 0.8,
    "subsample_freq": 1,
    "colsample_bytree": 0.8,
    "reg_lambda": 1.0,
    "max_bin": 255,
    "n_jobs": 4,
    "deterministic": True,
    "force_row_wise": True,
    "verbose": -1,
}

#: Post-gate A69 columns and the one actual-value column that is never a champion
#: input. `vre_actual_mw` and its components are deliberately absent: they are LAG
#: inputs, admitted only through the D-2-bounded trailing window (§5.2, §9.4-5).
FORBIDDEN_CHAMPION_INPUT_COLUMNS: frozenset[str] = frozenset(BENCHMARK_ADDITIONS) | {"actual_load_mw"}


def head_label(index: int) -> str:
    return QUANTILE_LABELS[index]


def fit_quantile_heads(
    features: pd.DataFrame,
    target: np.ndarray,
    *,
    seed: int = SEED,
    params: dict[str, Any] | None = None,
) -> dict[str, LGBMRegressor]:
    """Fit one independent LightGBM head per quantile level."""
    settings = dict(LGBM_PARAMS if params is None else params)
    heads: dict[str, LGBMRegressor] = {}
    for label, tau in zip(QUANTILE_LABELS, QUANTILES, strict=True):
        model = LGBMRegressor(alpha=tau, random_state=seed, **settings)
        model.fit(features, target)
        heads[label] = model
    return heads


def predict_raw_heads(heads: dict[str, LGBMRegressor], features: pd.DataFrame) -> np.ndarray:
    """Raw (possibly crossing) nine-quantile matrix, in canonical label order."""
    columns = [heads[label].predict(features) for label in QUANTILE_LABELS]
    return np.column_stack(columns).astype("float64")


@dataclass(frozen=True)
class Cutoffs:
    """The four §7.1 cutoffs, which are four different dates by construction."""

    snapshot_cutoff: date
    raw_model_fit_cutoff: date
    final_calibration_start: date
    final_calibration_end: date
    holdout_start: date
    holdout_end: date

    def to_dict(self) -> dict[str, str]:
        return {
            "snapshot_cutoff": self.snapshot_cutoff.isoformat(),
            "raw_model_fit_cutoff": self.raw_model_fit_cutoff.isoformat(),
            "final_calibration_window": f"{self.final_calibration_start.isoformat()}..{self.final_calibration_end.isoformat()}",
            "holdout_window": f"{self.holdout_start.isoformat()}..{self.holdout_end.isoformat()}",
            "raw_model_fit_precedes_snapshot_by_delivery_days": str(
                (self.snapshot_cutoff - self.raw_model_fit_cutoff).days
            ),
        }


class ChampionModel(mlflow.pyfunc.PythonModel):
    """The frozen artifact: heads + catalog pipeline + CQR thresholds + isotonic.

    `predict` takes a raw snapshot-shaped frame (`timestamp_utc`, `price_eur_mwh`,
    `load_forecast_mw`, and `vre_actual_mw` when the augmented catalog is selected)
    holding history *and* target rows, and returns one nine-column row per input
    row -- NaN where the catalog is not computable. Feeding it a frame that still
    contains delivery-day D prices is safe by construction, because no feature for
    D consumes a price dated D or later; that property is not asserted here, it is
    proved per delivery day by the sequential-equivalence check in
    `scripts/cp2_final_holdout.py`.
    """

    def __init__(
        self,
        heads: dict[str, LGBMRegressor],
        catalog: str,
        thresholds: dict[Pair, float],
        cutoffs: Cutoffs,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.heads = heads
        self.catalog = catalog
        self.thresholds = thresholds
        self.cutoffs = cutoffs
        self.metadata = dict(metadata or {})

    # -- runtime firewall -------------------------------------------------
    @staticmethod
    def validate_runtime_input(frame: pd.DataFrame, catalog: str) -> None:
        forbidden = sorted(FORBIDDEN_CHAMPION_INPUT_COLUMNS & set(frame.columns))
        if forbidden:
            raise ValueError(
                "champion runtime input rejects post-gate A69 and same-day actual columns: " f"{forbidden}"
            )
        required = {"timestamp_utc", "price_eur_mwh", "load_forecast_mw"}
        if catalog == "base_plus_residual_load_proxy":
            required.add("vre_actual_mw")
        missing = sorted(required - set(frame.columns))
        if missing:
            raise ValueError(f"champion runtime input is missing {missing}")

    def build_features(self, frame: pd.DataFrame) -> pd.DataFrame:
        self.validate_runtime_input(frame, self.catalog)
        features = build_feature_catalog(frame, self.catalog)
        validate_champion_runtime_schema(features.columns, self.catalog)
        return features

    # -- inference --------------------------------------------------------
    def predict_stages(self, frame: pd.DataFrame) -> dict[str, np.ndarray]:
        """Raw, post-CQR and final matrices, for the three-stage reliability read."""
        features = self.build_features(frame)
        complete = features.notna().all(axis=1).to_numpy()
        raw = np.full((len(features), len(QUANTILE_LABELS)), np.nan)
        if complete.any():
            raw[complete] = predict_raw_heads(self.heads, features.loc[complete])
        shifted = np.full_like(raw, np.nan)
        final = np.full_like(raw, np.nan)
        if complete.any():
            shifted[complete] = apply_cqr_thresholds(raw[complete], self.thresholds)
            final[complete] = isotonic_last(shifted[complete])
        return {"raw": raw, "post_cqr": shifted, "final": final, "complete": complete}

    def predict(self, context: Any, model_input: pd.DataFrame, params: dict | None = None) -> pd.DataFrame:  # noqa: ARG002
        stages = self.predict_stages(model_input)
        index = pd.DatetimeIndex(
            model_input["timestamp_utc"] if "timestamp_utc" in model_input.columns else model_input.index
        )
        return pd.DataFrame(stages["final"], columns=list(QUANTILE_LABELS), index=index)

    # -- provenance -------------------------------------------------------
    def describe(self) -> dict[str, Any]:
        return {
            "catalog": self.catalog,
            "feature_list": list(catalog_columns(self.catalog)),
            "quantiles": list(QUANTILES),
            "cqr_thresholds": thresholds_to_json(self.thresholds),
            "cutoffs": self.cutoffs.to_dict(),
            "lgbm_params": {**LGBM_PARAMS, "random_state": SEED},
            **self.metadata,
        }


def target_series(snapshot: pd.DataFrame) -> pd.Series:
    frame = snapshot.set_index("timestamp_utc") if "timestamp_utc" in snapshot.columns else snapshot
    return pd.Series(
        frame["price_eur_mwh"].to_numpy(dtype="float64"), index=pd.DatetimeIndex(frame.index).tz_convert("UTC")
    )


def truncate_history(snapshot: pd.DataFrame, through: date, history_days: int = 800) -> pd.DataFrame:
    """Rows for delivery days in [through - history_days, through].

    Used by the sequential-equivalence check: every champion feature is a bounded
    backward window (720 hourly rows, or 43 delivery days for the proxy), so a
    truncated frame must reproduce the vectorized values exactly. If it does not,
    something read forward.
    """
    dates = pd.Index(snapshot["delivery_date"].to_numpy())
    lower = through - timedelta(days=history_days)
    mask = (dates >= lower) & (dates <= through)
    return snapshot.loc[mask].reset_index(drop=True)


def dump_json(path: str, payload: Any) -> None:
    with open(path, "w") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True, default=str)
        handle.write("\n")


__all__ = [
    "BERLIN",
    "ChampionModel",
    "Cutoffs",
    "FORBIDDEN_CHAMPION_INPUT_COLUMNS",
    "LGBM_PARAMS",
    "SEED",
    "dump_json",
    "fit_quantile_heads",
    "head_label",
    "predict_raw_heads",
    "target_series",
    "thresholds_from_json",
    "truncate_history",
]
