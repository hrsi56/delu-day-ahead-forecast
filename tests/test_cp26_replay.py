"""Synthetic replay/caches and stubbed v1 CQR pipeline: no model training."""
from datetime import date, timedelta
import json
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from cp15.data import day_hours
from cp25.guard import issue_time
from cp26.fits import FitCache
from cp26.replay import central_for, replay_origin
from cp26.state import ReplayState

IDENTITY = {'protocol': 'synthetic-r14', 'inputs': 'synthetic'}


def bundle(day, *, route='nominal', failed=None, scale=2., partial=False, search=0):
    index = day_hours(day)
    if partial:
        index = index[1:]
    members = {}
    for j, name in enumerate(('B0', 'A1', 'B2', 'A1_w', 'B2_w', 'L-N', 'L-R', 'D2', 'v1-R')):
        central = np.full(len(index), j + 1.)
        members[name] = {'status': 'ok', 'central': central, 'cache_content_sha256': f'cache-{route}-{name}-{day}'}
        if name in ('D2', 'v1-R'):
            members[name]['quantiles'] = central[:, None] + np.arange(-3, 4)[None, :]
    if failed:
        members[failed] = {'status': 'failed', 'cause': 'synthetic missing original member'}
    return {'index': index, 'members': members, 'scale': np.full(len(index), scale),
            'issue_utc': issue_time(day), 'identity': IDENTITY, 'search': search}


def truth(index):
    return np.full(len(index), 50.)


def test_landed_blend_weights_and_direct_cqr_policy():
    day = date(2020, 1, 15)
    b = bundle(day)
    m = b['members']
    assert np.array_equal(central_for('v2', m, 24), np.full(24, 2.5))
    assert np.array_equal(central_for('v3', m, 24), np.full(24, 4.5))
    assert np.array_equal(central_for('v4', m, 24), m['A1_w']['central'] / 3 + m['B2_w']['central'] / 3
                          + m['L-N']['central'] / 6 + m['L-R']['central'] / 6)
    assert np.array_equal(central_for('v5', m, 24), m['A1_w']['central'] / 3 + m['B2_w']['central'] / 3
                          + m['L-N']['central'] / 12 + m['L-R']['central'] / 12 + m['D2']['central'] / 6)
    state = ReplayState(IDENTITY)
    rows = replay_origin(state, day, {'nominal': b}, truth, scored=True)
    assert rows['nominal/v1-R']['output_source'] == 'native'
    assert np.array_equal(rows['nominal/v1-R']['emitted_quantiles'], m['v1-R']['quantiles'])
    assert state.policies['nominal/v1-R'].errors is None


def test_restart_matches_continuous_and_survives_search_failures(tmp_path):
    first = date(2020, 1, 1)
    uninterrupted, restart = ReplayState(IDENTITY), ReplayState(IDENTITY)
    snapshot = tmp_path / 'snapshot.json'
    for offset in range(47):
        day = first + timedelta(days=offset)
        k = 0 if offset < 25 else 1
        failed = 'D2' if offset < 14 or offset in (25, 26) else None
        bundles = {route: bundle(day, route=route, failed=failed, search=k) for route in ('nominal', 'noload', 'gfs6')}
        a = replay_origin(uninterrupted, day, bundles, truth, scored=offset >= 20)
        b = replay_origin(restart, day, bundles, truth, scored=offset >= 20)
        assert a == b
        if offset in (13, 24, 25, 30):
            restart.save(snapshot)
            restart = ReplayState.load(snapshot, IDENTITY)
    assert restart.to_dict() == uninterrupted.to_dict()
    assert restart.policies['nominal/v5'].buffer_days == 28
    assert len(restart.learning('nominal').rows) > 28
    assert len(restart.learning('nominal').available(first + timedelta(days=46))) > 28


def test_learning_accepts_three_original_members_despite_h_shortage_or_scale_failure():
    first = date(2020, 1, 15)
    state = ReplayState(IDENTITY)
    rows = replay_origin(state, first, {'nominal': bundle(first, scale=np.nan)}, truth, scored=True)
    assert rows['nominal/v5']['native_central_valid'] and not rows['nominal/v5']['error_eligible']
    assert rows['nominal/v5']['output_source'] == 'missing'
    state.release(first + timedelta(days=2), truth)
    assert state.policies['nominal/v5'].buffer_days == 0 and len(state.learning('nominal').rows) == 1
    second = first + timedelta(days=2)
    rows = replay_origin(state, second, {'nominal': bundle(second)}, truth, scored=True)
    assert rows['nominal/v5']['error_eligible'] and rows['nominal/v5']['reason'] == 'interval_history_shortage'
    state.release(second + timedelta(days=2), truth)
    assert len(state.learning('nominal').rows) == 2 and state.policies['nominal/v5'].buffer_days == 1


def test_partial_day_stays_scored_but_neither_h_nor_learning_grows():
    day = date(2020, 4, 1)
    state = ReplayState(IDENTITY)
    rows = replay_origin(state, day, {'nominal': bundle(day, partial=True)}, truth, scored=True)
    assert len(rows['nominal/v1-R']['emitted_quantiles']) == 23
    assert rows['nominal/v1-R']['scored'] and not rows['nominal/v5']['error_eligible']
    state.release(day + timedelta(days=2), truth)
    assert not state.learning('nominal').rows and state.policies['nominal/v5'].buffer_days == 0


def test_routes_isolate_history_and_d_minus1_outcomes_do_not_affect_issuance():
    first = date(2020, 1, 15)
    a, b = ReplayState(IDENTITY), ReplayState(IDENTITY)
    for offset in range(33):
        day = first + timedelta(days=offset)
        bundles = {'nominal': bundle(day), 'noload': bundle(day, route='noload', failed='D2')}
        def altered(index):
            # A callable may have every outcome, but state requests only ≤D−2.
            delivery = index.tz_convert('Europe/Berlin')[0].date()
            return np.full(len(index), 999_999. if delivery >= day - timedelta(days=1) else 50.)
        assert replay_origin(a, day, bundles, truth, scored=True) == replay_origin(b, day, bundles, altered, scored=True)
    assert a.policies['nominal/v5'].buffer_days == 28
    assert a.policies['noload/v5'].buffer_days == 0
    assert len(a.learning('nominal').rows) > 0 and not a.learning('noload').rows


def test_successful_d2_cache_cannot_exist_without_verified_serving_ensemble(tmp_path):
    from cp26.search import SearchUnavailable
    from cp26.fits import _payload_hash
    from cp15.data import array_hash
    day = date(2020, 1, 15)
    cache = FitCache(tmp_path, 'nominal', IDENTITY)
    central = np.ones(24)
    q = np.ones((24, 7))
    with pytest.raises(SearchUnavailable):
        cache.save(day, 'D2', day_hours(day), issue_time(day),
                   {'status': 'ok', 'central': central, 'quantiles': q})
    cache.save(day, 'D2', day_hours(day), issue_time(day), {'status': 'failed', 'cause': 'no search'})
    path = cache.path(day, 'D2')
    item = json.loads(path.read_text())
    item.update(result={'status': 'ok', 'central': central.tolist(), 'quantiles': q.tolist()},
                central_sha256=array_hash(central), quantiles_sha256=array_hash(q))
    item['content_sha256'] = _payload_hash(item)
    path.write_text(json.dumps(item))
    with pytest.raises(SearchUnavailable):
        cache.load(day, 'D2', day_hours(day), issue_time(day))


def test_fit_cache_refuses_wrong_keys_identity_tamper_and_keeps_failed_member(tmp_path):
    day = date(2020, 1, 15)
    cache = FitCache(tmp_path, 'nominal', IDENTITY)
    native = {'status': 'ok', 'central': np.arange(24, dtype=float)}
    cache.save(day, 'A1', day_hours(day), issue_time(day), native)
    loaded = cache.load(day, 'A1', day_hours(day), issue_time(day))
    assert np.array_equal(loaded['central'], native['central'])
    with pytest.raises(ValueError, match='identity or content'):
        cache.load(day, 'A1', day_hours(day)[1:], issue_time(day))
    path = cache.path(day, 'A1')
    value = json.loads(path.read_text())
    value['result']['central'][0] = 888.
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match='identity or content'):
        cache.load(day, 'A1', day_hours(day), issue_time(day))
    with pytest.raises(FileExistsError):
        cache.save(day, 'A1', day_hours(day), issue_time(day), native)
    failure = {'status': 'failed', 'cause': 'synthetic solver failure', 'seconds': 1.}
    cache.save(day, 'B2', day_hours(day), issue_time(day), failure)
    assert cache.load(day, 'B2', day_hours(day), issue_time(day))['status'] == 'failed'
    with pytest.raises(ValueError, match='requires quantiles'):
        cache.save(day, 'v1-R', day_hours(day), issue_time(day), native)


def test_v1r_nine_heads_then_cqr_then_isotonic_then_seven(monkeypatch):
    """Exercise the real v1-R adapter; stub estimators rather than fitting trees."""
    import delu_forecast.model as model
    import delu_forecast.conformal as conformal
    import delu_forecast.postprocess as post
    from cp26.members import fit_v1r, SEVEN
    labels = post.QUANTILE_LABELS
    assert len(labels) == 9
    trace = []
    class Booster:
        def model_to_string(self):
            return 'synthetic nine-head tree'
    def fit(x, y, *, seed, params):
        trace.append(('heads', len(x), len(labels), params['n_jobs']))
        return {name: SimpleNamespace(booster_=Booster()) for name in labels}
    def predict(heads, x):
        trace.append(('predict', len(x), len(heads)))
        return np.tile(np.arange(9., dtype=float), (len(x), 1))
    def cqr(raw, y):
        trace.append(('cqr', raw.shape, len(y)))
        return {'fixture': 2.}
    def apply(raw, thresholds):
        trace.append(('apply_cqr', raw.shape, thresholds))
        return raw + thresholds['fixture']
    def isotonic(raw):
        trace.append(('isotonic', raw.shape))
        return np.sort(raw, axis=1)
    monkeypatch.setattr(model, 'fit_quantile_heads', fit)
    monkeypatch.setattr(model, 'predict_raw_heads', predict)
    monkeypatch.setattr(conformal, 'fit_cqr_thresholds', cqr)
    monkeypatch.setattr(conformal, 'thresholds_to_json', lambda x: x)
    monkeypatch.setattr(post, 'apply_cqr_thresholds', apply)
    monkeypatch.setattr(post, 'isotonic_last', isotonic)
    day = date(2022, 1, 1)
    days = pd.date_range(day - timedelta(days=800), day).date
    data = SimpleNamespace(dates=np.array(days, dtype='datetime64[D]'), eligible=np.ones(len(days), bool),
                           lgbm_raw=np.ones((len(days), 1)), p={'lgbm': {'features': ['fixture']}},
                           y=np.ones(len(days)), rows=lambda d: np.array([len(days) - 1]))
    result = fit_v1r(SimpleNamespace(data=data), day)
    assert [step[0] for step in trace] == ['heads', 'predict', 'cqr', 'predict', 'apply_cqr', 'isotonic']
    assert trace[0][1] == 666 and trace[0][2:] == (9, 1)
    assert trace[2][1] == (60, 9) and trace[2][2] == 60
    expected9 = np.arange(9., dtype=float)[None, :] + 2.
    expected7 = expected9[:, [labels.index(name) for name in SEVEN]]
    assert np.array_equal(result['quantiles9'], expected9)
    assert np.array_equal(result['quantiles'], expected7)
    assert np.array_equal(result['central'], expected7[:, 3])
    assert result['fits']['lightgbm_heads'] == 9
