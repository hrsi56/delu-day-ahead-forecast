"""Synthetic causal state controls; no model fit, experiment score or data read."""
from datetime import date, timedelta
import json

import numpy as np
import pandas as pd
import pytest

from cp15.data import day_hours
from cp25.guard import issue_time
from cp26.state import LearningLedger, PolicyState, ReplayState

IDENTITY = {'protocol': 'synthetic-r14', 'inputs': 'synthetic'}


def truth(index):
    return np.full(len(index), 10.)


def issue(policy, day, *, central=2., scale=2., scored=False, fallback=None, index=None, **kwargs):
    index = day_hours(day) if index is None else index
    policy.release(day, truth)
    return policy.issue(day, index, np.full(len(index), central), issue_utc=issue_time(day),
                        scale=np.full(len(index), scale), scored=scored, fallback=fallback, **kwargs)


def test_recovery_d2_historical_scale_consume_once_and_scored_output_immutable():
    policy = PolicyState('v5', 'nominal', IDENTITY)
    first = date(2020, 1, 15)
    fallback = {'index': [x.isoformat() for x in day_hours(first)], 'quantiles': np.full((24, 7), 99.).tolist()}
    original = issue(policy, first, scored=True, fallback=fallback)
    assert original['native_central_valid'] and not original['interval_ready']
    assert original['output_source'] == 'B0' and original['error_eligible']
    requested = []
    policy.release(first + timedelta(days=1), lambda keys: requested.append(keys) or truth(keys))
    assert requested == [] and policy.buffer_days == 0
    policy.release(first + timedelta(days=2), truth)
    assert policy.buffer_days == 1
    assert np.array_equal(policy.errors._buffer[0][1], np.full(24, 4.))
    saved = policy.errors.dumps()
    policy.release(first + timedelta(days=2), lambda keys: np.full(len(keys), 1_000_000.))
    assert policy.errors.dumps() == saved
    for offset in range(2, 31):
        issue(policy, first + timedelta(days=offset), scale=100.)
    assert policy.buffer_days == 28
    recovered = policy.records[str(first + timedelta(days=30))]
    assert recovered['interval_ready'] and recovered['output_source'] == 'native'
    assert policy.records[str(first)] == original
    assert recovered['buffer']['calendar_span_days'] >= 28


@pytest.mark.parametrize('failure', ['member', 'identity', 'scale', 'solver'])
def test_failure_never_creates_h_native_intake(failure):
    policy = PolicyState('v5', 'nominal', IDENTITY)
    kwargs = {'central_failure': failure} if failure in ('member', 'solver') else {'identity_valid': False} if failure == 'identity' else {}
    row = issue(policy, date(2020, 2, 1), scale=np.nan if failure == 'scale' else 2., **kwargs)
    assert not row['error_eligible'] and not policy.errors._pending
    assert row['native_central_valid'] == (failure == 'scale')
    policy.release(date(2020, 2, 3), truth)
    assert policy.buffer_days == 0


def test_h_numeric_failure_not_confused_with_history_shortage(monkeypatch):
    policy = PolicyState('v4', 'nominal', IDENTITY)
    first = date(2020, 1, 15)
    for offset in range(30):
        issue(policy, first + timedelta(days=offset))
    day = first + timedelta(days=30)
    def broken(*args, **kwargs):
        raise ValueError('synthetic H construction failure')
    monkeypatch.setattr(policy.errors, 'predict', broken)
    row = issue(policy, day, scored=True)
    assert row['native_central_valid'] and row['reason'] == 'interval_numeric_failure'
    assert not row['error_eligible'] and day not in policy.errors._pending


@pytest.mark.parametrize('warm_days', [0, 30])
def test_subnormal_h_identity_uses_scored_fallback_without_own_error(warm_days):
    policy = PolicyState('v5', 'nominal', IDENTITY)
    first = date(2020, 1, 15)
    for offset in range(warm_days):
        issue(policy, first + timedelta(days=offset))
    day = first + timedelta(days=warm_days)
    fallback = {'index': [t.isoformat() for t in day_hours(day)],
                'quantiles': np.full((24, 7), 99.).tolist()}
    row = issue(policy, day, central=np.nextafter(0., 1.), scored=True, fallback=fallback)
    assert row['native_central_valid'] and not row['interval_ready']
    assert row['reason'] == 'h_identity_numeric_failure'
    assert row['output_source'] == 'B0' and row['emitted_quantiles'] == fallback['quantiles']
    assert not row['error_eligible'] and day not in policy.errors._pending
    policy.release(day + timedelta(days=2), truth)
    assert day not in policy.errors._consumed


def test_numeric_h_registration_failure_falls_back_but_duplicate_guard_stays_hard(monkeypatch):
    policy = PolicyState('v5', 'nominal', IDENTITY)
    day = date(2020, 1, 15)
    fallback = {'index': [t.isoformat() for t in day_hours(day)],
                'quantiles': np.full((24, 7), 99.).tolist()}
    def numerical_failure(*args):
        raise FloatingPointError('synthetic own-error construction failure')
    monkeypatch.setattr(policy.errors, 'issue', numerical_failure)
    row = issue(policy, day, scored=True, fallback=fallback)
    assert row['output_source'] == 'B0' and row['reason'] == 'interval_numeric_failure'
    assert not row['error_eligible'] and not policy.errors._pending
    other = PolicyState('v5', 'nominal', IDENTITY)
    other.release(day, truth)
    other.errors.issue(day, day_hours(day), np.ones(24), np.ones(24), np.ones(24))
    with pytest.raises(ValueError, match='already registered'):
        other.issue(day, day_hours(day), np.ones(24), issue_utc=issue_time(day), scale=np.ones(24),
                    scored=True, fallback=fallback)
    assert str(day) not in other.records


def test_b0_raw_errors_missing_scored_quantiles_and_no_self_fallback():
    policy = PolicyState('B0', 'nominal', IDENTITY, 'B0')
    first = date(2020, 1, 1)
    fallback = {'index': [x.isoformat() for x in day_hours(first)], 'quantiles': np.full((24, 7), 99.).tolist()}
    row = issue(policy, first, scale=np.nan, scored=True, fallback=fallback)
    assert row['native_central_valid'] and row['error_eligible']
    assert row['native_scale_valid'] is None and row['output_source'] == 'missing'
    policy.release(first + timedelta(days=2), truth)
    assert np.array_equal(policy.errors.buffer[0][1], np.full(24, 8.))
    for offset in range(2, 31):
        issue(policy, first + timedelta(days=offset), scale=np.nan)
    assert np.array_equal(np.asarray(policy.records[str(first + timedelta(days=30))]['native_quantiles']), np.full((24, 7), 10.))


def test_partial_scored_keys_do_not_create_full_errors():
    policy = PolicyState('v3', 'nominal', IDENTITY)
    day = date(2020, 5, 1)
    index = day_hours(day)[1:]
    fallback = {'index': [x.isoformat() for x in day_hours(day)], 'quantiles': np.full((24, 7), 99.).tolist()}
    row = issue(policy, day, index=index, scored=True, fallback=fallback)
    assert len(row['scoring_index']) == 23 and len(row['emitted_quantiles']) == 23
    assert row['output_source'] == 'B0' and not row['error_eligible']
    policy.release(day + timedelta(days=2), truth)
    assert policy.buffer_days == 0


@pytest.mark.parametrize('day,n', [(date(2020, 3, 29), 23), (date(2020, 10, 25), 25)])
def test_full_dst_canonical_day_is_error_eligible(day, n):
    policy = PolicyState('v2', 'nominal', IDENTITY)
    row = issue(policy, day)
    assert row['full_canonical_issuance'] and row['error_eligible'] and len(row['index']) == n
    policy.release(day + timedelta(days=2), truth)
    assert policy.buffer_days == 1 and len(policy.errors._buffer[0][1]) == n


def test_full_native_day_can_have_a_separate_partial_scoring_mask():
    policy = PolicyState('v2', 'nominal', IDENTITY)
    day = date(2020, 2, 1)
    row = issue(policy, day, scoring_index=day_hours(day)[2:], scored=True)
    assert len(row['scoring_index']) == 22 and row['error_eligible']


def test_learning_ledger_is_separate_from_h_and_requires_native_three_members():
    day = date(2020, 1, 15)
    ledger = LearningLedger('nominal', IDENTITY)
    members = {name: np.full(24, 2.) for name in ledger.MEMBERS}
    assert ledger.issue(day, day_hours(day), members, issue_utc=issue_time(day), scale=np.full(24, np.nan))
    ledger.release(day + timedelta(days=1), truth)
    assert not ledger.rows
    ledger.release(day + timedelta(days=2), truth)
    assert len(ledger.rows) == 1 and ledger.rows[day]['issued_scale'] is None
    saved = ledger.to_dict()
    ledger.release(day + timedelta(days=2), lambda keys: np.full(len(keys), -999.))
    assert ledger.to_dict() == saved
    ledger.release(day + timedelta(days=3), truth)
    assert not ledger.issue(day + timedelta(days=3), day_hours(day + timedelta(days=3))[:-1], members,
                            issue_utc=issue_time(day + timedelta(days=3)))
    ledger.release(day + timedelta(days=4), truth)
    assert not ledger.issue(day + timedelta(days=4), day_hours(day + timedelta(days=4)), {'D2': np.full(24, 2.)},
                            issue_utc=issue_time(day + timedelta(days=4)))


def test_learning_cannot_register_a_historical_forecast_after_outcome_release():
    day = date(2020, 1, 15)
    ledger = LearningLedger('nominal', IDENTITY)
    ledger.release(day + timedelta(days=2), truth)
    with pytest.raises(ValueError, match='current origin'):
        ledger.issue(day, day_hours(day), {name: np.ones(24) for name in ledger.MEMBERS}, issue_utc=issue_time(day))
    assert not ledger.pending and not ledger.rows


def test_historical_learning_view_does_not_include_late_released_truth():
    day = date(2020, 1, 15)
    ledger = LearningLedger('nominal', IDENTITY)
    assert ledger.issue(day, day_hours(day), {name: np.ones(24) for name in ledger.MEMBERS}, issue_utc=issue_time(day))
    ledger.release(day + timedelta(days=2), lambda keys: np.full(len(keys), np.nan))
    ledger.release(day + timedelta(days=10), truth)
    assert ledger.available(day + timedelta(days=2)) == []
    assert len(ledger.available(day + timedelta(days=10))) == 1


def test_restore_checks_pending_central_scale_and_consumed_error_provenance():
    day = date(2020, 1, 15)
    policy = PolicyState('v5', 'nominal', IDENTITY)
    issue(policy, day)
    snapshot = policy.to_dict()
    snapshot['errors']['pending'][0]['central'][0] = 99.
    with pytest.raises(ValueError, match='pending central'):
        PolicyState.from_dict(snapshot)
    snapshot = policy.to_dict()
    snapshot['errors']['pending'][0]['scale'][0] = 99.
    with pytest.raises(ValueError, match='pending scale'):
        PolicyState.from_dict(snapshot)
    policy.release(day + timedelta(days=2), truth)
    snapshot = policy.to_dict()
    snapshot['errors']['buffer'][0]['errors'][0] = 99.
    with pytest.raises(ValueError, match='residual buffer'):
        PolicyState.from_dict(snapshot)
    snapshot = policy.to_dict()
    snapshot['records'] = {}
    with pytest.raises(ValueError, match='native eligible issuances'):
        PolicyState.from_dict(snapshot)


def test_exact_issue_instant_and_snapshot_tamper_refusal(tmp_path):
    day = date(2020, 3, 29)
    state = ReplayState(IDENTITY)
    policy = state.policy('nominal', 'v5')
    state.release(day, truth)
    with pytest.raises(ValueError, match='frozen CP-26 issue instant'):
        policy.issue(day, day_hours(day), np.ones(23), issue_utc=pd.Timestamp(issue_time(day)) + pd.Timedelta(minutes=1),
                     scale=np.ones(23))
    issue(policy, day)
    path = tmp_path / 'state.json'
    state.save(path)
    assert ReplayState.load(path, IDENTITY).to_dict() == state.to_dict()
    value = json.loads(path.read_text())
    value['policies']['nominal/v5']['records'][str(day)]['issued_scale'][0] = 500.
    path.write_text(json.dumps(value))
    with pytest.raises(ValueError, match='identity/schema'):
        ReplayState.load(path, IDENTITY)
