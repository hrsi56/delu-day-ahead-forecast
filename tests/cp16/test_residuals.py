"""Synthetic controls only: no estimators, external inputs, or policy replay."""
from datetime import date, timedelta
import json

import numpy as np
import pandas as pd
import pytest

from cp15.data import LEVELS, day_hours
from cp16.residuals import SharedResidualState, hour_quantiles


COUNTS = {'successful_policy_days': 0, 'successful_policy_target_rows': 0,
          'prediction_calls_including_rejected': 0}


@pytest.fixture(scope='session', autouse=True)
def resource_counts():
    yield
    print('\nCP16_RESIDUAL_RESOURCE_COUNTS=' + json.dumps(COUNTS, sort_keys=True))


def predict(state, day, a1=10., b2=30., scale=2., index=None):
    index = day_hours(day) if index is None else index
    def vector(x):
        return np.full(len(index), x) if np.ndim(x) == 0 else x
    COUNTS['prediction_calls_including_rejected'] += 1
    result = state.predict(day, index, vector(a1), vector(b2), vector(scale))
    COUNTS['successful_policy_days'] += 2
    COUNTS['successful_policy_target_rows'] += 2 * len(index)
    return result


def issue(state, day, a1=10., b2=30., scale=2., index=None):
    index = day_hours(day) if index is None else index
    def vector(x):
        return np.full(len(index), x) if np.ndim(x) == 0 else x
    state.issue(day, index, vector(a1), vector(b2), vector(scale))


def populated(start=date(2024, 1, 1), count=28, error=lambda ix: np.ones(len(ix))):
    state = SharedResidualState()
    for offset in range(count):
        issue(state, start + timedelta(days=offset))
    origin = start + timedelta(days=count + 1)
    state.release(origin, lambda ix: 20 + 2 * error(ix))
    return state, origin


def test_d1_rejected_d2_accepted_once_and_copy_immutable():
    state = SharedResidualState()
    day = date(2024, 1, 1)
    ix = day_hours(day)
    a1, b2, scale = np.full(len(ix), 10.), np.full(len(ix), 30.), np.full(len(ix), 2.)
    state.issue(day, ix, a1, b2, scale)
    a1[:] = b2[:] = scale[:] = 999
    assert not np.shares_memory(ix.asi8, state._pending[day].index.asi8)
    assert state._pending[day].central[0] == 20
    for values in (state._pending[day].central, state._pending[day].scale):
        with pytest.raises(ValueError):
            values[0] = 100
    calls = []
    def truth(index):
        calls.append(index)
        return np.full(len(index), 26.)
    state.release(day + timedelta(days=1), truth)
    assert calls == [] and state.to_dict()['buffer'] == []
    state.release(day + timedelta(days=2), truth)
    assert len(calls) == 1
    np.testing.assert_array_equal(state.to_dict()['buffer'][0]['errors'], np.full(24, 3.))
    before = state.dumps()
    state.release(day + timedelta(days=2), truth)
    assert len(calls) == 1 and state.dumps() == before
    with pytest.raises(ValueError, match='already registered'):
        issue(state, day)
    with pytest.raises(ValueError, match='backwards'):
        state.release(day, truth)


@pytest.mark.parametrize('day,n', [(date(2024, 3, 31), 23), (date(2024, 3, 30), 24),
                                  (date(2024, 10, 27), 25)])
def test_canonical_dst_identity(day, n):
    state = SharedResidualState()
    ix = day_hours(day)
    assert len(ix) == n and not ix.has_duplicates
    issue(state, day)
    def truth(index):
        assert index.equals(ix)
        return 20 + 2 * np.arange(n)
    state.release(day + timedelta(days=2), truth)
    np.testing.assert_array_equal(state.to_dict()['buffer'][0]['errors'], np.arange(n))
    local_hours = ix.tz_convert('Europe/Berlin').hour
    assert sum(local_hours == 2) == {23: 0, 24: 1, 25: 2}[n]
    other = SharedResidualState()
    with pytest.raises(ValueError, match='canonical'):
        issue(other, day, index=ix[::-1])
    with pytest.raises(ValueError, match='canonical'):
        issue(other, day, index=ix.append(ix[-1:]))
    with pytest.raises(ValueError, match='timezone'):
        issue(other, day, index=ix.tz_localize(None))
    ready, origin = populated(start=day - timedelta(days=29))
    outputs, _ = predict(ready, origin, index=ix)
    assert all(output.shape == (n, 7) for output in outputs.values())


def test_partial_issue_never_admitted_but_complete_positive_control():
    state = SharedResidualState()
    day = date(2024, 1, 1)
    issue(state, day, index=day_hours(day)[:-1])
    issue(state, day + timedelta(days=1))
    calls = []
    state.release(day + timedelta(days=3), lambda ix: calls.append(ix) or np.full(len(ix), 22))
    assert len(calls) == 1
    assert [r['day'] for r in state.to_dict()['buffer']] == ['2024-01-02']
    assert state.trace[0]['status'] == 'incomplete_issued_day'


def test_nonfinite_truth_stays_pending_until_complete_finite_truth():
    state = SharedResidualState()
    day = date(2024, 1, 1)
    issue(state, day)
    origin = day + timedelta(days=2)
    state.release(origin, lambda ix: np.full(len(ix), np.nan))
    assert not state.to_dict()['buffer'] and len(state.to_dict()['pending']) == 1
    state.release(origin, lambda ix: np.full(len(ix), 22.))
    assert len(state.to_dict()['buffer']) == 1 and not state.to_dict()['pending']


def test_partial_truth_retry_and_latest_delivery_dates_not_arrival_order():
    start = date(2024, 1, 1)
    state = SharedResidualState()
    for offset in range(30):
        issue(state, start + timedelta(days=offset))
    oldest, gap = start, start + timedelta(days=20)
    def truth(ix):
        day = ix.tz_convert('Europe/Berlin').date[0]
        return np.full(len(ix) - 1, 22.) if day in (oldest, gap) else np.full(len(ix), 22.)
    origin = start + timedelta(days=31)
    state.release(origin, truth)
    assert len(state.to_dict()['buffer']) == 28
    _, meta = predict(state, origin)
    assert meta['buffer_calendar_span_days'] == 29
    state.release(origin, lambda ix: np.full(len(ix), 24.))
    records = state.to_dict()['buffer']
    assert len(records) == 28
    assert records[0]['day'] == str(start + timedelta(days=2))
    assert records[-1]['day'] == str(start + timedelta(days=29))
    assert str(gap) in [r['day'] for r in records]
    assert str(oldest) not in [r['day'] for r in records]
    assert not state.to_dict()['pending']


def test_no_common_history_fallback_and_released_origin_required():
    state, origin = populated(count=27)
    with pytest.raises(ValueError, match='28 complete'):
        predict(state, origin)
    issue(state, origin - timedelta(days=1))
    state.release(origin, lambda ix: np.full(len(ix), 22))
    with pytest.raises(ValueError, match='28 complete'):
        predict(state, origin)
    state.release(origin + timedelta(days=1), lambda ix: np.full(len(ix), 22))
    with pytest.raises(ValueError, match='release must'):
        predict(state, origin)
    output, _ = predict(state, origin + timedelta(days=1))
    assert output['V2-P'].shape == (24, 7)


def test_row_specific_issuance_scale_current_scale_and_median_shift():
    start = date(2024, 1, 1)
    state = SharedResidualState()
    for offset in range(28):
        day = start + timedelta(days=offset)
        scale = np.arange(1., len(day_hours(day)) + 1)
        issue(state, day, scale=scale)
    origin = start + timedelta(days=29)
    state.release(origin, lambda ix: 20 + 3 * np.arange(1., len(ix) + 1))
    current = np.arange(1., 25.)
    outputs, meta = predict(state, origin, scale=current)
    expected = np.repeat((20 + 3 * current)[:, None], 7, axis=1)
    for output in outputs.values():
        np.testing.assert_array_equal(output, expected)
        assert (output[:, 3] != 20).all()
    changed, _ = predict(state, origin, scale=current * 2)
    np.testing.assert_array_equal(changed['V2-P'], 2 * expected - 20)
    assert meta['buffer_age_days'] == 2 and meta['buffer_oldest_age_days'] == 29
    assert meta['buffer_calendar_span_days'] == 28


def test_hour_shrink_only_difference_and_seven_linear_quantiles():
    state, origin = populated(error=lambda ix: ix.tz_convert('Europe/Berlin').hour.to_numpy(float))
    outputs, meta = predict(state, origin)
    pooled = np.quantile(np.tile(np.arange(24.), 28), LEVELS, method='linear')
    expected_p = np.tile(20 + 2 * pooled, (24, 1))
    expected_h = 20 + 2 * (np.arange(24.)[:, None] / 3 + pooled * (2 / 3))
    np.testing.assert_allclose(outputs['V2-P'], expected_p)
    np.testing.assert_allclose(outputs['V2-H'], expected_h)
    assert not np.array_equal(outputs['V2-H'], outputs['V2-P'])
    assert meta['hour_support']['2'] == {'n': 28, 'distinct_days': 28, 'weight': 1 / 3}
    for output in outputs.values():
        assert np.isfinite(output).all() and (np.diff(output, axis=1) >= 0).all()


@pytest.mark.parametrize('start,expected_n', [(date(2024, 3, 15), 27), (date(2024, 10, 15), 29)])
def test_dst_hour_support_counts_canonical_observations_and_distinct_days(start, expected_n):
    state, origin = populated(start=start, error=lambda ix: np.arange(len(ix), dtype=float))
    _, meta = predict(state, origin)
    support = meta['hour_support']['2']
    assert support['n'] == expected_n
    assert support['distinct_days'] == min(expected_n, 28)
    assert support['weight'] == expected_n / (expected_n + 56)
    assert meta['buffer_hours'] == 28 * 24 + expected_n - 28


def test_sparse_hour_fallback_and_fourteenth_distinct_day_positive_control(monkeypatch):
    pooled = np.arange(7.)
    days = [date(2024, 1, 1) + timedelta(days=k) for k in range(14)]
    original = np.quantile
    def fail_quantile(*args, **kwargs):
        raise AssertionError('hour quantile must not be evaluated under sparse fallback')
    monkeypatch.setattr(np, 'quantile', fail_quantile)
    for errors, represented in (([], []), (np.full(26, 10.), days[:13] * 2)):
        result, support = hour_quantiles(pooled, errors, represented)
        np.testing.assert_array_equal(result, pooled)
        assert support['weight'] == 0
    monkeypatch.setattr(np, 'quantile', original)
    result, support = hour_quantiles(pooled, np.full(14, 10.), days)
    np.testing.assert_allclose(result, .2 * 10 + .8 * pooled)
    assert support['weight'] == .2


def test_linear_quantile_ties_and_equal_arm_positive_control():
    state, origin = populated(error=lambda ix: np.resize([0., 0., 1., 3.], len(ix)))
    outputs, _ = predict(state, origin)
    expected = np.quantile(np.tile([0., 0., 1., 3.], 168), LEVELS, method='linear')
    np.testing.assert_array_equal(outputs['V2-P'][0], 20 + 2 * expected)
    assert expected[3] == .5  # midpoint, not nearest/lower/higher quantile
    equal_state, equal_origin = populated(error=lambda ix: np.full(len(ix), 4.))
    equal, _ = predict(equal_state, equal_origin)
    np.testing.assert_array_equal(equal['V2-H'], equal['V2-P'])


def test_state_json_restart_replay_preserves_pending_scales_and_consume_once(tmp_path):
    state, origin = populated()
    issue(state, origin - timedelta(days=1), scale=4)
    issue(state, origin)
    path = tmp_path / 'residuals.json'
    state.save(path)
    restored = SharedResidualState.load(path)
    assert restored.dumps() == state.dumps()
    for day in (origin, origin + timedelta(days=1), origin + timedelta(days=2)):
        for instance in (state, restored):
            instance.release(day, lambda ix: np.full(len(ix), 28.))
        left, lm = predict(state, day)
        right, rm = predict(restored, day)
        assert lm == rm and state.dumps() == restored.dumps()
        for arm in left:
            np.testing.assert_array_equal(left[arm], right[arm])
    assert restored.to_dict()['buffer'][-2]['errors'] == [2.] * 24
    assert restored.to_dict()['buffer'][-1]['errors'] == [4.] * 24
    serialized = restored.to_dict()
    serialized['buffer'][-1]['errors'][0] = 999.
    assert restored.to_dict()['buffer'][-1]['errors'][0] == 4.


@pytest.mark.parametrize('field,value', [('a1', np.nan), ('b2', np.inf), ('scale', .99)])
def test_nonfinite_components_and_unfloored_scale_refused(field, value):
    day = date(2024, 1, 1)
    with pytest.raises(ValueError):
        issue(SharedResidualState(), day, **{field: value})
    state, origin = populated()
    with pytest.raises(ValueError):
        predict(state, origin, **{field: value})
    good, _ = predict(state, origin)
    assert np.isfinite(good['V2-P']).all()


def test_persisted_invalid_state_refused_with_valid_control():
    state, _ = populated()
    for mutate in (
        lambda s: s.update(schema='other'),
        lambda s: s['buffer'][0]['errors'].pop(),
        lambda s: s['buffer'][0]['errors'].__setitem__(0, float('nan')),
        lambda s: s['buffer'].reverse(),
        lambda s: s.update(last_origin='2024-01-02'),
        lambda s: s['consumed'].clear(),
    ):
        bad = state.to_dict()
        mutate(bad)
        with pytest.raises(ValueError):
            SharedResidualState.from_dict(bad)
    assert SharedResidualState.loads(state.dumps()).dumps() == state.dumps()
