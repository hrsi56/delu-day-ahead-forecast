"""Protocol §10's causal controls, on synthetic ledgers, each negative control with a positive one.

Proved before any CP-28 run on CP-26's stored forecasts. The production replay uses the same
`cp28.engine.run` with the protocol's 364/728/28 history constants; here 10/20/28 keep it fast.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd
import pytest

import cp28_synthetic as S
from cp16.residuals import SharedResidualState
from cp28 import engine, grid, states

FIRST = date(2020, 3, 1)
LAST = date(2020, 6, 30)
N = 100


@pytest.fixture(scope='module')
def prices():
    return S.price_series(FIRST, LAST)


@pytest.fixture(scope='module')
def base(prices):
    days = S.ledger(FIRST, N, prices, scored_from=date(2020, 4, 20))
    frame = states.issue_states(prices, [d.day for d in days])
    return days, frame, S.run(days, prices, state_frame=frame)


def snapshot(result, day):
    """Everything an origin issues: weights, centrals, emitted quantiles, statuses, fit and features."""
    out = {}
    for issue in result.issues:
        if issue.day == day:
            out[issue.arm] = (issue.record['weights'], None if issue.central is None else issue.central.tobytes(),
                              None if issue.emitted is None else issue.emitted.tobytes(), issue.record['output_source'],
                              issue.record['error_eligible'], issue.record['buffer_latest'] if 'buffer_latest' in issue.record else None)
    fit = next(f for f in result.fits if f['day'] == day)
    out['fit'] = tuple(sorted((k, str(v)) for k, v in fit.items()))
    out['features'] = result.features[day]['features'].tobytes()
    return out


def mutate_prices(prices, day, value=None, seed=3):
    changed = prices.copy()
    keys = changed.index[pd.DatetimeIndex(changed.index).tz_convert('Europe/Berlin').date == day]
    rng = np.random.default_rng(seed)
    changed.loc[keys] = rng.normal(500, 100, len(keys)) if value is None else value
    return changed


D = date(2020, 5, 20)       # an origin with a full H buffer and every learned arm fitted (n >= 20)


def test_target_day_masking_produces_zero_change_and_a_released_change_follows(base, prices):
    days, frame, result = base
    changed = mutate_prices(prices, D)
    after = S.run(days, changed, state_frame=frame)
    for origin in (D - timedelta(days=1), D):
        assert snapshot(after, origin) == snapshot(result, origin)
    # Positive control: once D's outcome is released (D+2), the arms' H and learning use it.
    assert snapshot(after, D + timedelta(days=2)) != snapshot(result, D + timedelta(days=2))


def test_truth_is_never_requested_beyond_d_minus_2(base, prices):
    days, frame, result = base
    assert result.latest_truth_requested == days[-1].day - timedelta(days=2)
    truth = engine.Truth(prices).at(D)
    with pytest.raises(engine.CausalityError):
        truth(S.canonical_hours(D - timedelta(days=1)))
    assert np.isfinite(truth(S.canonical_hours(D - timedelta(days=2)))).all()


def test_available_past_input_mutation_changes_the_forecast(base, prices):
    days, frame, result = base
    changed = [d if d.day != D - timedelta(days=10) else
               S.Day(**{**d.__dict__, 'members': {**d.members, 'L': d.members['L'] + 25.0}}) for d in days]
    after = S.run(changed, prices, state_frame=frame)
    before, now = snapshot(result, D), snapshot(after, D)
    assert now['A3'] != before['A3'] and now['A5'] != before['A5'] and now['fit'] != before['fit']


def test_d_minus_1_error_mutation_produces_zero_change(base, prices):
    days, frame, result = base
    prior = D - timedelta(days=1)
    # Its forecasts change (so its error would), and so does its outcome; the states stay the
    # issue-time predictors they are, computed separately below.
    changed_days = [d if d.day != prior else
                    S.Day(**{**d.__dict__, 'members': {k: v + 40.0 for k, v in d.members.items()}}) for d in days]
    after = S.run(changed_days, mutate_prices(prices, prior), state_frame=frame)
    assert snapshot(after, D) == snapshot(result, D)


def test_d_minus_2_released_error_can_change_learning(base, prices):
    days, frame, result = base
    after = S.run(days, mutate_prices(prices, D - timedelta(days=2)), state_frame=frame)
    before, now = snapshot(result, D), snapshot(after, D)
    assert now['fit'] != before['fit']                     # the newest window date's outcome moved the fits
    assert now['A2'] != before['A2']                       # and A2's own H buffer took the new error


def test_d_minus_1_price_is_a_predictor_not_feedback():
    """The states may use D−1's complete prices (positive) and never D's (negative)."""
    prices = S.price_series(FIRST, LAST)
    base = states.issue_states(prices, [D])
    moved = states.issue_states(mutate_prices(prices, D - timedelta(days=1), value=-100.0), [D])
    assert moved.negative_price_risk.iloc[0] == 1 and moved.negative_latest_day.iloc[0] == D - timedelta(days=1)
    same = states.issue_states(mutate_prices(prices, D, value=-100.0), [D])
    pd.testing.assert_frame_equal(same, base)


def test_duplicate_release_changes_no_buffer(base, prices):
    days, frame, _ = base
    ledger = engine.LearningLedger()
    truth = engine.Truth(prices)
    for d in days[:40]:
        ledger.release(d.day, truth.at(d.day))
        ledger.register(d)
    rows = [r.day for r in ledger.rows]
    ledger.release(days[39].day, truth.at(days[39].day))
    assert [r.day for r in ledger.rows] == rows
    with pytest.raises(ValueError):
        ledger.register(days[39])
    h = SharedResidualState()
    for d in days[:40]:
        h.release(d.day, truth.at(d.day))
        h.issue(d.day, d.index, d.members['c_HG'], d.members['c_HG'], d.scale)
    buffer = [(x, e.tobytes()) for x, e in h._buffer]
    h.release(days[39].day, truth.at(days[39].day))
    assert [(x, e.tobytes()) for x, e in h._buffer] == buffer
    with pytest.raises(ValueError):
        h.issue(days[39].day, days[39].index, days[39].members['c_HG'], days[39].members['c_HG'], days[39].scale)


def test_future_rows_change_no_training_or_scaler_feature(base, prices):
    days, frame, result = base
    later = [d if d.day <= D else S.Day(**{**d.__dict__, 'members': {k: v * 3 for k, v in d.members.items()}}) for d in days]
    changed = prices.copy()
    future = pd.DatetimeIndex(changed.index).tz_convert('Europe/Berlin').date > D
    changed[future] = changed[future] + 300
    after = S.run(later, changed, state_frame=frame)
    for origin in (D - timedelta(days=5), D):
        assert snapshot(after, origin) == snapshot(result, origin)
        assert np.array_equal(after.networks[origin]['mean'], result.networks[origin]['mean'])
        assert np.array_equal(after.networks[origin]['W1'], result.networks[origin]['W1'])


def test_copied_fallback_errors_never_enter_member_or_arm_history(prices):
    gap = date(2020, 5, 10)
    days = S.ledger(FIRST, N, prices, scored_from=date(2020, 4, 20), missing_member={gap: 'D2'})
    result = S.run(days, prices)
    for arm in engine.ARMS:
        issue = S.by(result, arm, gap)
        assert issue.record['output_source'] == 'v5' and np.array_equal(issue.emitted, days[(gap - FIRST).days].v5_quantiles)
        assert not issue.record['error_eligible']
    assert gap not in result.learning_days
    for arm in engine.COMBINED:
        consumed = [t['feedback_day'] for t in result.h_traces[arm] if t['status'] == 'consumed']
        assert str(gap) not in consumed
    # Positive control: the neighbouring native dates do enter.
    assert gap - timedelta(days=1) in result.learning_days and gap + timedelta(days=1) in result.learning_days


def test_valid_native_central_on_h_shortage_dates_enters_once_after_d_minus_2(prices):
    days = S.ledger(FIRST, N, prices, scored_from=FIRST)            # scored from the first date: H is short
    result = S.run(days, prices)
    early = FIRST + timedelta(days=3)
    issue = S.by(result, 'A2', early)
    assert issue.record['output_source'] == 'v5' and 'interval_history_shortage' in issue.record['reasons']
    assert issue.record['native_central_valid'] and issue.record['error_eligible']
    consumed = [t for t in result.h_traces['A2'] if t.get('feedback_day') == str(early) and t['status'] == 'consumed']
    assert len(consumed) == 1 and consumed[0]['origin'] == str(early + timedelta(days=2))
    # The emitted fallback never feeds back: the consumed central is the native one.
    from cp15.data import array_hash
    assert consumed[0]['issued_center_sha256'] == array_hash(issue.central)


def test_hard_central_failures_never_enter(prices, monkeypatch):
    no_scale = date(2020, 5, 12)
    solver_day = date(2020, 5, 15)
    days = S.ledger(FIRST, N, prices, scored_from=date(2020, 4, 20), no_scale={no_scale})
    choose, real_release = grid.choose, engine.LearningLedger.release
    failing = {'on': False}

    def flaky(objective):
        if failing['on']:
            raise FloatingPointError('injected solver failure')
        return choose(objective)

    def release(self, origin, truth):
        failing['on'] = origin == solver_day          # the grid fails at exactly one origin
        return real_release(self, origin, truth)
    monkeypatch.setattr(grid, 'choose', flaky)
    monkeypatch.setattr(engine.LearningLedger, 'release', release)
    result = S.run(days, prices)
    for arm in engine.COMBINED:
        issue = S.by(result, arm, no_scale)
        assert not issue.record['native_central_valid'] and not issue.record['error_eligible']
        assert 'scale_unavailable' in issue.record['reasons'] and issue.record['output_source'] == 'v5'
    a2 = S.by(result, 'A2', solver_day)
    for arm in ('A3', 'A4', 'A6'):
        issue = S.by(result, arm, solver_day)
        assert issue.record['solver_failure'] and not issue.record['error_eligible'] and issue.central is None
        assert issue.record['output_source'] == 'A2:' + a2.record['output_source']
        assert np.array_equal(issue.emitted, a2.emitted)
        consumed = [t['feedback_day'] for t in result.h_traces[arm] if t['status'] == 'consumed']
        assert str(solver_day) not in consumed and str(no_scale) not in consumed
    # Positive control: A5/A7 (the network) were unaffected and entered their own buffers.
    assert S.by(result, 'A5', solver_day).record['error_eligible']


def test_dst_canonical_keys_survive(prices):
    first = date(2020, 9, 1)
    long_prices = S.price_series(first, date(2020, 12, 31))
    days = S.ledger(first, 90, long_prices, scored_from=date(2020, 10, 1))
    result = S.run(days, long_prices)
    autumn = date(2020, 10, 25)
    issue = S.by(result, 'A3', autumn)
    assert len(issue.index) == 25 and len(issue.central) == 25 and issue.emitted.shape == (25, 7)
    hours = engine.local_hours(issue.index)
    assert list(hours).count(2) == 2 and engine.blocks_of(issue.index).count('night') == 9
    assert autumn in result.learning_days
    consumed = [t for t in result.h_traces['A3'] if t.get('feedback_day') == str(autumn) and t['status'] == 'consumed']
    assert consumed and consumed[0]['n'] == 25
    spring_prices = S.price_series(date(2020, 3, 1), date(2020, 5, 31))
    spring_days = S.ledger(date(2020, 3, 1), 60, spring_prices, scored_from=date(2020, 3, 20))
    spring = S.run(spring_days, spring_prices)
    issue = S.by(spring, 'A2', date(2020, 3, 29))
    assert len(issue.index) == 23 and 2 not in set(engine.local_hours(issue.index))


def test_shared_unshrunk_fits_and_deployment_rules(base):
    _, _, result = base
    import json
    fit = next(f for f in result.fits if f['day'] == D)
    deployed = {k: np.array(v) for k, v in json.loads(fit['deployed']).items()}
    fitted = grid.WEIGHTS[fit['A3_index']]
    assert np.array_equal(deployed['A6'][0], fitted)
    assert np.array_equal(deployed['A3'][0], 0.5 * fitted + 0.5 * grid.W0)
    p = result.networks[D]['output']
    assert np.array_equal(deployed['A7'], p) and np.array_equal(deployed['A5'], 0.5 * p + 0.5 * grid.W0)
    blocks = [grid.WEIGHTS[fit[f'A4_{b}_index']] for b in grid.BLOCKS]
    assert np.array_equal(deployed['A4'], np.stack([0.25 * w + 0.75 * deployed['A3'][0] for w in blocks]))
    early = next(f for f in result.fits if f['learning_dates'] == 5)
    early_deployed = json.loads(early['deployed'])
    for arm in ('A3', 'A4', 'A5', 'A6', 'A7'):
        assert np.array_equal(np.array(early_deployed[arm]), np.tile(grid.W0, (3, 1)))
    mid = next(f for f in result.fits if f['learning_dates'] == 15)
    mid_deployed = json.loads(mid['deployed'])
    assert mid_deployed['A4'] == mid_deployed['A3']                      # A4 = A3's deployed before the full window


def test_startup_learned_arm_is_native_not_a_fallback(prices):
    days = S.ledger(FIRST, N, prices, scored_from=date(2020, 4, 5))
    result = S.run(days, prices, minimum=50, full=70)
    startup = [i for i in result.issues if i.arm in ('A3', 'A5', 'A7') and i.record['weight_rule'] == 'startup_w0'
               and i.record['interval_ready']]
    assert startup
    assert all(i.record['output_source'] == 'native' and i.record['startup_equal_to_v5_weights'] for i in startup)
    assert all(np.array_equal(np.array(__import__('json').loads(i.record['weights'])), np.tile(grid.W0, (3, 1))) for i in startup)
