"""CP-21 §17.3/§17.7: training-only capacity selection, the tie rule, pooled-block parity and
charge-before-fit, on a small synthetic fixture with a reduced grid (no research data; these
fixture fits are synthetic and are not research fits)."""
from __future__ import annotations

from datetime import date, timedelta
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cp21 import lgbm

ROOT = Path(__file__).resolve().parents[2]
SMALL_GRID = ({'id': 'G1', 'n_estimators': 4, 'num_leaves': 3}, {'id': 'G2', 'n_estimators': 8, 'num_leaves': 4},
              {'id': 'G3', 'n_estimators': 12, 'num_leaves': 5}, {'id': 'G4', 'n_estimators': 16, 'num_leaves': 7})


class Synth:
    """The attributes `cp21.lgbm` reads from CP-15's prepared inputs."""

    def __init__(self, days=150, seed=0, constant=None):
        rng = np.random.default_rng(seed)
        start = date(2019, 1, 1)
        calendar = [start + timedelta(days=i) for i in range(days)]
        self.dates = np.repeat(np.array(calendar, dtype='datetime64[D]'), 24)
        self.hours = np.tile(np.arange(24), days)
        n = len(self.dates)
        self.lgbm_raw = rng.normal(size=(n, 5))
        self.lgbm_normalized = self.lgbm_raw * 0.5
        self.level = np.repeat(rng.normal(50, 5, days), 24)
        self.scale = np.repeat(rng.uniform(5, 15, days), 24)
        signal = 40 + 10 * self.lgbm_raw[:, 0] + 5 * np.sin(self.hours / 3)
        self.y = np.full(n, float(constant)) if constant is not None else signal + rng.normal(0, 3, n)
        self.eligible = np.ones(n, bool)
        self.feature_valid = np.ones(n, bool)
        self.p = json.loads((ROOT / 'reports/cp15/protocol.json').read_text())

    def rows(self, d, eligible=True):
        return np.flatnonzero(self.dates == np.datetime64(d))


@pytest.fixture(autouse=True)
def small(monkeypatch):
    monkeypatch.setattr(lgbm, 'GRID', SMALL_GRID)
    monkeypatch.setattr(lgbm, 'MIN_TRAIN_ROWS', {m: 10 * len(h) for m, h in lgbm.MODEL_HOURS.items()})
    monkeypatch.setattr(lgbm, 'MIN_VALIDATION_ROWS', {m: len(h) for m, h in lgbm.MODEL_HOURS.items()})


def _weather(data, seed=5):
    wx = np.random.default_rng(seed).normal(size=(len(data.dates), 3))
    return wx, np.ones(len(data.dates), bool)


def _charge(log):
    return lambda role: log.append(role)


DAY = date(2019, 5, 1)


def test_exact_tie_goes_to_the_smaller_configuration():
    data = Synth(constant=50.0)
    wx, present = _weather(data)
    design = lgbm.arm_design(data, wx, 'L-P')
    pred, records, summary = lgbm.fit_select(data, design, present, DAY, 'L-P', 'pooled', charge=_charge([]))
    assert len(set(summary['validation_mae'].values())) == 1 and summary['tie']
    assert summary['selected'] == 'G1'
    np.testing.assert_array_equal(pred, np.full(24, 50.0))


def test_selection_and_forecast_ignore_outcomes_after_the_origin_but_not_validation_rows():
    data = Synth()
    wx, present = _weather(data)
    base = lgbm.fit_arm(data, wx, present, DAY, 'L-R', charge=_charge([]))
    later = Synth()
    later.y[later.dates >= np.datetime64(DAY)] += 1000.0  # outcomes on and after the origin day
    again = lgbm.fit_arm(later, wx, present, DAY, 'L-R', charge=_charge([]))
    assert np.array_equal(base[0], again[0]) and base[2] == again[2]
    assert [r['model_sha256'] for r in base[1]] == [r['model_sha256'] for r in again[1]]
    inner = Synth()
    window = (inner.dates >= np.datetime64(DAY - timedelta(days=28))) & (inner.dates < np.datetime64(DAY))
    inner.y[window] = inner.y[window] * -2.0  # positive control: the inner-validation rows
    moved = lgbm.fit_arm(inner, wx, present, DAY, 'L-R', charge=_charge([]))
    assert any(moved[2][m]['validation_mae'] != base[2][m]['validation_mae'] for m in lgbm.BLOCKS)


def test_pooled_and_block_models_use_the_same_rows_target_features_and_grid():
    data = Synth()
    wx, present = _weather(data)
    pooled = lgbm.model_rows(data, DAY, 'pooled', present)
    blocks = [lgbm.model_rows(data, DAY, b, present) for b in lgbm.BLOCKS]
    for i in (1, 2, 3, 4):  # window, inner, validation, forecast
        assert np.array_equal(np.sort(np.concatenate([b[i] for b in blocks])), np.sort(pooled[i]))
    assert pooled[0] == blocks[0][0]  # same history start
    lp, lr = lgbm.arm_design(data, wx, 'L-P'), lgbm.arm_design(data, wx, 'L-R')
    assert lp.x is lr.x and np.array_equal(lp.target, lr.target) and not lp.normalized and not lr.normalized
    ln = lgbm.arm_design(data, wx, 'L-N')
    assert ln.normalized and ln.x is data.lgbm_normalized
    np.testing.assert_array_equal(ln.target, (data.y - data.level) / data.scale)
    assert lgbm.ARMS['L-P']['target'] == lgbm.ARMS['L-R']['target'] == 'raw'
    assert lgbm.ARMS['L-R']['models'] == lgbm.ARMS['L-N']['models'] == tuple(lgbm.BLOCKS)


def test_every_fit_is_charged_before_it_runs_and_a_refusal_stops_the_next_fit():
    data = Synth()
    wx, present = _weather(data)
    roles = []
    lgbm.fit_arm(data, wx, present, DAY, 'L-P', charge=_charge(roles))
    assert roles == ['inner'] * 4 + ['final']
    calls = []

    def refuse(role):
        calls.append(role)
        if len(calls) == 3:
            raise RuntimeError('cap')
    with pytest.raises(RuntimeError):
        lgbm.fit_arm(data, wx, present, DAY, 'L-P', charge=refuse)
    assert calls == ['inner'] * 3


def test_normalized_arm_is_inverted_before_validation_and_forecast():
    data = Synth()
    wx, present = _weather(data)
    pred, records, _ = lgbm.fit_arm(data, wx, present, DAY, 'L-N', charge=_charge([]))
    assert np.isfinite(pred).all()
    assert all(r['validation_mae'] is None or np.isfinite(r['validation_mae']) for r in records)
    # forecasts are in EUR/MWh: close to the raw arm's scale, not to the unit-free target's
    raw, _, _ = lgbm.fit_arm(data, wx, present, DAY, 'L-R', charge=_charge([]))
    assert abs(np.mean(pred) - np.mean(raw)) < 20


def test_insufficient_history_or_missing_weather_record_fails_without_substitution(monkeypatch):
    data = Synth()
    wx, present = _weather(data)
    monkeypatch.setattr(lgbm, 'MIN_TRAIN_ROWS', {m: 10**9 for m in lgbm.MODEL_HOURS})
    with pytest.raises(ValueError, match='insufficiency'):
        lgbm.fit_arm(data, wx, present, DAY, 'L-P', charge=_charge([]))
    monkeypatch.setattr(lgbm, 'MIN_TRAIN_ROWS', {m: 10 * len(h) for m, h in lgbm.MODEL_HOURS.items()})
    present[:24] = False
    with pytest.raises(ValueError, match='weather record'):
        lgbm.fit_arm(data, wx, present, DAY, 'L-P', charge=_charge([]))
