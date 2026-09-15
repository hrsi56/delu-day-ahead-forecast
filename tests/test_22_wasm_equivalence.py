"""M3.5/CP-3B item 2 — the hard gate: the browser model IS the frozen champion.

Four public surfaces assert "the shipped model is exactly the model the holdout
evaluated". `mlflow.pyfunc` will not load under Pyodide, so the browser runs the
re-implementation in `app/browser_champion.py`, and that sentence is true only
for as long as the two agree. So it is proved, not asserted, on a committed
fixture spanning all three regimes and a DST transition.

Every assertion here that something *matches* is paired with a control that
makes it stop matching. A tolerance chosen to make a test pass would be a
failure of this item; none is needed — the agreement is bitwise.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

from delu_forecast.claims import REPO_ROOT

APP = REPO_ROOT / "app"
PUBLIC = APP / "public"
sys.path.insert(0, str(APP))

from browser_champion import BASE_FEATURES, BrowserChampion  # noqa: E402


MISSING = (
    "app/public/ is absent. It is generated from the committed models/champion/ by\n"
    "    make wasm-payload\n"
    "and deliberately not committed: 31 MB of boosters derived losslessly from an\n"
    "artifact already in the repository would duplicate it, not preserve it.\n"
    "This is a failure rather than a skip so a green run cannot hide the hard gate."
)


def _load(name: str) -> dict:
    path = PUBLIC / name
    if not path.exists():
        raise AssertionError(MISSING)
    return json.loads(path.read_text())


@pytest.fixture(scope="module")
def payload():
    import lightgbm as lgb

    meta = _load("champion.json")
    for label in meta["quantile_labels"]:
        if not (PUBLIC / "boosters" / f"{label}.txt").exists():
            raise AssertionError(MISSING)
    boosters = {
        label: lgb.Booster(model_str=(PUBLIC / "boosters" / f"{label}.txt").read_text())
        for label in meta["quantile_labels"]
    }
    return meta, boosters, _load("series.json"), _load("calendar.json"), _load("fixture.json")


@pytest.fixture(scope="module")
def browser(payload):
    meta, boosters, series, calendar, _ = payload
    return BrowserChampion(boosters, meta, series, calendar)


def _expected(fixture: dict, day: str) -> np.ndarray:
    return np.array(
        [[np.nan if v is None else v for v in row] for row in fixture["expected_final_quantiles"][day]],
        dtype="float64",
    )


# -- the fixture itself must be worth passing --------------------------------


def test_the_fixture_spans_the_regimes_and_is_large_enough(payload):
    _, _, _, _, fixture = payload
    days = fixture["days"]
    assert len(days) >= 30, f"the bar asks for at least 30 delivery days, got {len(days)}"
    regimes = {entry["regime"] for entry in days}
    assert {"pre-crisis", "crisis"} <= regimes
    assert any("holdout" in regime for regime in regimes)
    assert any("dst" in regime for regime in regimes), "no DST transition in the fixture"
    # A 23-hour day must actually be present, or the DST claim is decorative.
    assert any(entry["rows"] == 23 for entry in days)
    assert sum(entry["rows"] for entry in days) >= 700


def test_the_fixture_was_generated_from_the_frozen_artifact(payload):
    meta, _, _, _, fixture = payload
    card = json.loads((REPO_ROOT / "models/champion/champion_card.json").read_text())
    assert fixture["artifact_fingerprint_sha256"] == card["artifact_fingerprint_sha256"]
    assert meta["artifact_fingerprint_sha256"] == card["artifact_fingerprint_sha256"]
    assert meta["snapshot_sha256"] == card["snapshot_sha256"]
    assert tuple(meta["features"]) == BASE_FEATURES == tuple(card["feature_list"])
    for key, value in meta["cqr_thresholds"].items():
        low, high = key.split("|")
        assert card["cqr_thresholds"][f"{low}_{high}"] == value


# -- THE HARD GATE -----------------------------------------------------------


def test_the_browser_path_equals_the_frozen_champion_bitwise(browser, payload):
    """Zero tolerance. Not 'close enough' — the same float64 bits."""
    _, _, _, _, fixture = payload
    worst, worst_day, null_mismatches, compared = 0.0, None, 0, 0
    for entry in fixture["days"]:
        day = entry["day"]
        got, hours = browser.predict_day(day)
        expected = _expected(fixture, day)
        assert got.shape == expected.shape, day
        assert hours == entry["local_hours"], f"row order differs on {day}"
        got_null, expected_null = np.isnan(got), np.isnan(expected)
        null_mismatches += int((got_null != expected_null).sum())
        both = ~got_null & ~expected_null
        compared += int(both.sum())
        if both.any():
            deviation = float(np.max(np.abs(got[both] - expected[both])))
            if deviation > worst:
                worst, worst_day = deviation, day
    assert null_mismatches == 0, f"{null_mismatches} cells differ in null-ness"
    assert compared >= 9_000, f"only {compared} finite cells compared"
    assert worst == 0.0, f"max deviation {worst} on {worst_day} — the identity claim is broken"


def test_the_fail_closed_rows_are_reproduced_not_filled(browser, payload):
    """On the spring-forward day the D-1 lag has no source hour. The frozen
    pipeline yields null; so must the browser. Inventing a number there would
    pass a naive equality check on the other rows."""
    _, _, _, _, fixture = payload
    total = 0
    for entry in fixture["days"]:
        if not entry["fail_closed_rows"]:
            continue
        got, _ = browser.predict_day(entry["day"])
        expected = _expected(fixture, entry["day"])
        assert np.array_equal(np.isnan(got), np.isnan(expected)), entry["day"]
        total += entry["fail_closed_rows"]
    assert total > 0, "the fixture no longer contains a fail-closed row"


# -- positive controls: the comparison above must be able to fail -------------


def test_positive_control_a_perturbed_cqr_threshold_breaks_equivalence(payload):
    """The control the bar names. Move one threshold by 0.01 and the gate fails."""
    meta, boosters, series, calendar, fixture = payload
    perturbed = json.loads(json.dumps(meta))
    key = next(iter(perturbed["cqr_thresholds"]))
    perturbed["cqr_thresholds"][key] += 0.01
    broken = BrowserChampion(boosters, perturbed, series, calendar)

    day = fixture["days"][0]["day"]
    got, _ = broken.predict_day(day)
    expected = _expected(fixture, day)
    both = ~np.isnan(got) & ~np.isnan(expected)
    deviation = float(np.max(np.abs(got[both] - expected[both])))
    assert deviation > 0.0, "perturbing a CQR threshold changed nothing — the gate proves nothing"
    assert deviation == pytest.approx(0.01, abs=1e-9), deviation


def test_positive_control_a_reordered_catalog_is_refused(payload):
    """Feeding the trees the wrong column would still produce plausible numbers."""
    meta, boosters, series, calendar, _ = payload
    scrambled = json.loads(json.dumps(meta))
    scrambled["features"] = list(reversed(scrambled["features"]))
    with pytest.raises(ValueError, match="catalog order changed"):
        BrowserChampion(boosters, scrambled, series, calendar)


def test_positive_control_one_fewer_tree_breaks_equivalence(payload):
    """Not just the post-processing: the trees themselves are the model.

    599 of the median head's 600 trees is a genuinely different model, which is
    a cleaner control than editing the serialized text — LightGBM's parser
    aborts the process on malformed input rather than raising, so text surgery
    would test the parser instead of the gate.
    """
    meta, boosters, series, calendar, fixture = payload

    class OneTreeShort:
        def __init__(self, booster):
            self._booster = booster

        def predict(self, matrix):
            return self._booster.predict(matrix, num_iteration=599)

    swapped = dict(boosters)
    swapped["p50"] = OneTreeShort(boosters["p50"])
    broken = BrowserChampion(swapped, meta, series, calendar)

    day = fixture["days"][-1]["day"]
    got, _ = broken.predict_day(day)
    expected = _expected(fixture, day)
    both = ~np.isnan(got) & ~np.isnan(expected)
    deviation = float(np.max(np.abs(got[both] - expected[both])))
    assert deviation > 0.0, "dropping a tree changed nothing — the gate proves nothing"


def test_positive_control_a_swapped_head_breaks_equivalence(payload):
    """A wiring error — the right nine boosters in the wrong nine slots."""
    meta, boosters, series, calendar, fixture = payload
    swapped = dict(boosters)
    swapped["p50"], swapped["p25"] = boosters["p25"], boosters["p50"]
    broken = BrowserChampion(swapped, meta, series, calendar)
    day = fixture["days"][-1]["day"]
    got, _ = broken.predict_day(day)
    expected = _expected(fixture, day)
    both = ~np.isnan(got) & ~np.isnan(expected)
    assert float(np.max(np.abs(got[both] - expected[both]))) > 0.0


# -- item 3: §5.2 still holds on the browser path ----------------------------


def test_delivery_day_prices_change_nothing_and_a_d_minus_1_price_does(payload):
    """The CP-3 control, reproduced against the browser's own inputs."""
    meta, boosters, series, calendar, fixture = payload
    day = json.loads((PUBLIC / "champion.json").read_text())["default_day"]
    base = BrowserChampion(boosters, meta, series, calendar)
    reference, _ = base.predict_day(day)

    masked = json.loads(json.dumps(series))
    for index, value in enumerate(masked["delivery_date"]):
        if value == day:
            masked["price_eur_mwh"][index] = float("nan")
    got, _ = BrowserChampion(boosters, meta, masked, calendar).predict_day(day)
    assert np.array_equal(got, reference), (
        "masking the delivery day's own prices moved the forecast — a feature read forward"
    )

    import datetime as dt

    previous = (dt.date.fromisoformat(day) - dt.timedelta(days=1)).isoformat()
    mutated = json.loads(json.dumps(series))
    touched = 0
    for index, value in enumerate(mutated["delivery_date"]):
        if value == previous:
            mutated["price_eur_mwh"][index] += 250.0
            touched += 1
    assert touched > 0, "no D-1 rows in the shipped slice"
    moved, _ = BrowserChampion(boosters, meta, mutated, calendar).predict_day(day)
    difference = float(np.nanmax(np.abs(moved - reference)))
    assert difference > 1.0, (
        f"positive control failed: a D-1 price moved the forecast by only {difference}, "
        "so the equality above proves nothing"
    )


def test_the_scenario_probe_moves_the_forecast_and_touches_only_the_target_day(browser, payload):
    meta, _, _, _, _ = payload
    day = meta["default_day"]
    base, _ = browser.predict_day(day)
    probed, _ = browser.predict_day(day, load_scale=1.10)
    assert not np.array_equal(base, probed), "the load-forecast probe changed nothing"

    plain, _ = browser.features_for_day(day)
    scaled, _ = browser.features_for_day(day, load_scale=1.10)
    columns = list(BASE_FEATURES)
    load_columns = {columns.index("load_forecast_mw"), columns.index("load_forecast_day_mean_mw")}
    for index, name in enumerate(columns):
        if index in load_columns:
            continue
        assert np.array_equal(
            np.nan_to_num(plain[:, index], nan=-1e9), np.nan_to_num(scaled[:, index], nan=-1e9)
        ), f"the probe moved {name}, which is not the load forecast"


def test_browser_output_is_monotone_wherever_it_is_defined(browser, payload):
    """The one retained hard gate, on the surface a visitor actually drives."""
    _, _, _, _, fixture = payload
    for entry in fixture["days"]:
        got, _ = browser.predict_day(entry["day"])
        defined = ~np.isnan(got).any(axis=1)
        if defined.any():
            assert (np.diff(got[defined], axis=1) >= 0).all(), f"crossing on {entry['day']}"


# -- the notebook must execute the bytes this test imported ------------------


def test_the_notebook_fetches_the_module_this_test_verified():
    import hashlib

    source = (APP / "browser_champion.py").read_bytes()
    shipped = (PUBLIC / "browser_champion.py").read_bytes()
    assert source == shipped, (
        "app/public/browser_champion.py has drifted from app/browser_champion.py — "
        "the browser would run code this test never checked. Re-run `make wasm-payload`."
    )
    digest = hashlib.sha256(source).hexdigest()
    manifest = json.loads((REPO_ROOT / "reports/cp3b/payload.json").read_text())
    assert manifest["browser_champion_sha256"] == digest


def test_the_browser_page_renders_from_the_one_claim_set():
    """Item 5 carried into the browser: the WASM surface retypes nothing.

    Every number the page shows comes from this file, and this file is
    `build_claims()` verbatim — so the page cannot round a figure differently
    from the README, the Pages export, the Space card or the MLflow record.
    """
    from delu_forecast.claims import build_claims

    shipped = _load("claims.json")
    assert shipped == dict(build_claims().values), (
        "app/public/claims.json has drifted from claims.py — re-run `make wasm-payload`"
    )
    for key in ("snapshot_cutoff", "raw_model_fit_cutoff", "final_calibration_window",
                "holdout_window", "replay_label", "sensitivity_probe_label",
                "shipped_is_evaluated", "holdout_dm_label"):
        assert shipped[key], key
