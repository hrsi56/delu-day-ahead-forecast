"""Synthetic scoring-contract fixtures; executed only by the Lead's monitor."""
from copy import deepcopy
from datetime import date

import numpy as np
import pandas as pd
import pytest

from cp25.guard import issue_time
from cp25.calendar import expected_hours
from cp26.scoring import (FrozenPopulation, hourly_losses, paired_losses,
                          population_from_records, score_records, score_released_frame, QUANTILES)
from cp26.diagnostics import calibration_tables, known_price_states


def population(days, *, omitted=(), excluded=()):
    cal, masks = [], []
    for day in days:
        hours = expected_hours(day)
        removed = [ts for ts in omitted if ts in hours]
        eligible = day not in excluded
        cal.append({'delivery_date': day, 'canonical_hours': len(hours), 'eligible': eligible,
                    'landed_eligible_hours': len(hours)-len(removed) if eligible else 0,
                    'ineligible_hours_on_eligible_day': len(removed) if eligible else 0})
        masks.append({'delivery_date': day, 'eligible': eligible, 'never_scored': True, 'old_fold_2_5': False})
    omitted_frame = pd.DataFrame({'timestamp_utc': pd.DatetimeIndex(omitted, tz='UTC') if not omitted else omitted,
                                 'delivery_date': [ts.tz_convert('Europe/Berlin').date() for ts in omitted]})
    return population_from_records(pd.DataFrame(cal), pd.DataFrame(masks), omitted_frame,
                                   evidence={'synthetic_fixture': True})


def fixture_records(pop, *, errors=None, missing=(), fallback=()):
    errors = {} if errors is None else errors
    records, truth = [], pop.keys.copy()
    truth['y_true'] = 0.
    for stream in ('nominal/B0', 'nominal/v5'):
        for day, index in pop.keys_by_day().items():
            error = errors.get((stream, day), 1.)
            q = np.full((len(index), 7), error)
            source = 'missing' if (stream, day) in missing else 'B0' if (stream, day) in fallback else 'native'
            records.append({'day': str(day), 'route': 'nominal', 'policy': stream.split('/')[1],
                            'issue_utc': issue_time(day).isoformat(), 'scored': True,
                            'scoring_index': [ts.isoformat() for ts in index],
                            'emitted_quantiles': None if source == 'missing' else q.tolist(), 'output_source': source,
                            'native_central_valid': source == 'native', 'interval_ready': source == 'native',
                            'error_eligible': False, 'reason': None})
    return records, truth


def test_exact_wis_and_components_and_emitted_p50():
    y = np.array([-4., 0., 9.])
    q = np.tile([-2., -1., 0., 1., 2., 3., 4.], (3, 1))
    loss = hourly_losses(y, q)
    expected = .5*np.abs(y-q[:, 3])
    for alpha, lo, hi in ((.5, 2, 4), (.2, 1, 5), (.05, 0, 6)):
        interval_score = q[:, hi]-q[:, lo]+2/alpha*(np.maximum(q[:, lo]-y, 0)+np.maximum(y-q[:, hi], 0))
        expected += alpha/2*interval_score
    np.testing.assert_array_equal(loss['MAE'], np.abs(y-1))
    np.testing.assert_allclose(loss['WIS'], expected/3.5)
    np.testing.assert_allclose(loss['WIS'], loss['WIS_dispersion']+loss['WIS_underprediction']+loss['WIS_overprediction'])


def test_partial_dst_keys_remain_exact_and_days_weight_equally():
    spring, autumn = date(2021, 3, 28), date(2021, 10, 31)
    omitted = (expected_hours(autumn)[2],)
    pop = population([spring, autumn], omitted=omitted)
    assert [len(v) for v in pop.keys_by_day().values()] == [23, 24]
    records, truth = fixture_records(pop, errors={('nominal/v5', spring): 2., ('nominal/v5', autumn): 4.})
    result = score_records(records, truth, pop, streams=('nominal/B0', 'nominal/v5'), production=False)
    row = result['summaries'].query("stream == 'nominal/v5' and metric == 'MAE' and group == 'overall' and mask == 'all_eligible'").iloc[0]
    assert row.raw_mean_daily_loss == 3.
    assert row.B0_ratio == 3.
    modified = deepcopy(records)
    modified[-1]['scoring_index'].insert(2, omitted[0].isoformat())
    with pytest.raises(ValueError, match='frozen CP-25'):
        score_records(modified, truth, pop, streams=('nominal/B0', 'nominal/v5'), production=False)


def test_zero_key_exclusions_are_in_explicit_mapping_and_daily_accounting():
    d1, d2 = date(2021, 1, 1), date(2021, 1, 2)
    pop = population([d1, d2], excluded=(d2,))
    assert len(pop.keys_by_day()[d2]) == 0
    assert pop.verify_key_mapping(pop.keys_by_day())[d2].tz is not None
    records, truth = fixture_records(pop)
    result = score_records(records, truth, pop, streams=('nominal/B0', 'nominal/v5'), production=False)
    excluded = result['daily'][result['daily'].delivery_date.eq(d2)]
    assert len(excluded) == 2 and not excluded.available.any() and excluded.MAE.isna().all()


def test_missing_day_pairs_and_fallback_immutable_output():
    days = [date(2021, 1, i) for i in (1, 2, 3)]
    pop = population(days)
    records, truth = fixture_records(pop, missing=(('nominal/B0', days[1]), ('nominal/v5', days[1])),
                                     fallback=(('nominal/v5', days[2]),))
    result = score_records(records, truth, pop, streams=('nominal/B0', 'nominal/v5'), production=False)
    pair, counts = paired_losses(result['daily'], 'nominal/v5', 'nominal/B0', metric='MAE')
    assert pair.delivery_date.tolist() == [days[0], days[2]]
    assert counts['calendar_dates'] == 3 and counts['paired_dates'] == 2 and counts['either_missing_dates'] == 1
    assert result['fallbacks'].set_index('stream').at['nominal/v5', 'fallback_dates'] == 1
    broken = deepcopy(records)
    broken[-1]['emitted_quantiles'][0][0] = .5
    with pytest.raises(ValueError, match='fallback differs'):
        score_records(broken, truth, pop, streams=('nominal/B0', 'nominal/v5'), production=False)


def test_population_does_not_trust_regenerated_keys_or_masks():
    pop = population([date(2021, 1, 1)])
    with pytest.raises(ValueError, match='caller scoring keys'):
        pop.verify_keys(pop.keys.iloc[:-1])
    masks = pop.masks.copy()
    masks['never_scored'] = False
    with pytest.raises(ValueError, match='caller masks'):
        pop.verify_masks(masks)
    records, truth = fixture_records(pop)
    with pytest.raises(ValueError, match='verified committed'):
        score_records(records, truth, pop, streams=('nominal/B0', 'nominal/v5'))


def test_histogram_ties_upper_bin_and_quantile_strict_weak_bounds():
    pop = population([date(2021, 1, 1)])
    records, truth = fixture_records(pop, errors={('nominal/B0', date(2021, 1, 1)): 0.,
                                                ('nominal/v5', date(2021, 1, 1)): 0.})
    result = score_records(records, truth, pop, streams=('nominal/B0', 'nominal/v5'), production=False)
    diagnostics = calibration_tables(result['hourly'], result['daily'])
    histogram = diagnostics['histogram'].query("stream == 'nominal/v5' and group == 'overall' and mask == 'all_eligible'")
    assert histogram.set_index('bin').at[7, 'observed_probability'] == 1.
    hits = diagnostics['quantile_hits'].query("stream == 'nominal/v5' and group == 'overall' and mask == 'all_eligible'")
    assert hits.strict_hit.eq(0).all() and hits.weak_hit.eq(1).all() and hits.tie_rate.eq(1).all()


def test_price_states_skip_partial_day_and_reject_future_or_unreleased_inputs():
    days = [date(2021, 1, i) for i in range(1, 11)]
    rows = []
    for day in days:
        for j, ts in enumerate(expected_hours(day)):
            if day == days[5] and j == 0:
                continue
            rows.append({'timestamp_utc': ts, 'delivery_date': day, 'price_eur_mwh': -1. if day == days[0] else 1.,
                         'available_utc': pd.Timestamp(issue_time(day+pd.Timedelta(days=2).to_pytimedelta()))})
    history = pd.DataFrame(rows)
    origin = date(2021, 1, 10)
    state = known_price_states(history, [origin]).iloc[0]
    assert state.negative_price_risk == 1 and state.negative_support_dates == 6
    assert state.high_volatility == 0 and state.volatility_unknown == 1
    future_mutation = history.copy()
    future_mutation.loc[future_mutation.delivery_date.ge(date(2021, 1, 8)), 'price_eur_mwh'] = -999.
    pd.testing.assert_frame_equal(known_price_states(history, [origin]), known_price_states(future_mutation, [origin]))


def test_released_reference_preserves_original_identity_and_missing_or_stale_keys():
    day = date(2026, 6, 9)
    pop = population([day])
    truth = pop.keys.copy()
    truth['y_true'] = np.arange(len(truth), dtype=float)
    historical = truth.copy()
    saved = truth[['delivery_date', 'y_true']].copy()
    for name in QUANTILES:
        saved[f'final_{name}'] = truth.y_true+1
    result = score_released_frame(saved, historical, pop, truth, metadata={'artifact_sha256': 'original'})
    assert result['daily'].iloc[0].MAE == 1.
    assert result['daily'].iloc[0].output_source == 'released_artifact'
    assert result['reference_metadata']['artifact_sha256'] == 'original'
    assert not result['reference_metadata']['CP26_native_or_refit']
    missing = score_released_frame(saved.iloc[:-1], historical, pop, truth, metadata={})
    assert not missing['daily'].iloc[0].available
    assert missing['daily'].iloc[0].reason == 'historical_row_to_key_mapping_unavailable'
    assert missing['key_differences'].iloc[0].unresolved_requested_hours == len(truth)
    stale = saved.copy()
    stale.loc[0, 'y_true'] += 1
    with pytest.raises(ValueError, match='stale released'):
        score_released_frame(stale, historical, pop, truth, metadata={})


def test_actual_b0_feature_valid_selector_scores_partial_dst_without_h_or_learning_intake():
    from datetime import timedelta
    from types import SimpleNamespace
    from cp15.data import Inputs
    from cp26 import harness as H
    from cp26.members import fit_b0
    from cp26.replay import replay_origin
    from cp26.state import ReplayState

    day = date(2021, 10, 31)
    full = expected_hours(day)
    valid = np.ones(len(full), bool)
    valid[2] = False
    naive = np.arange(len(full), dtype=float)
    naive[2] = np.nan
    empty = np.empty((len(full), 0))
    # The real landed Inputs.rows selector is used, with an omitted canonical
    # hour that has an invalid base feature and an undefined naive forecast.
    inputs = Inputs(pd.DataFrame(), None, full, np.full(len(full), np.datetime64(day)),
                    full.tz_convert('Europe/Berlin').hour.to_numpy(), np.zeros(len(full)),
                    valid.copy(), valid, np.zeros(len(full)), np.ones(len(full)),
                    empty, empty, empty, empty, naive, {})
    fit = fit_b0(SimpleNamespace(data=inputs, settings=H.NEW), day)
    native_index = inputs.index[inputs.rows(day)]
    assert len(full) == 25 and len(native_index) == 24 and fit['status'] == 'ok'
    np.testing.assert_array_equal(fit['central'], naive[valid])
    identity = {'fixture': 'actual-partial-b0-selector'}

    def bundle(origin, index, b0=None):
        members = {}
        for name in ('B0', 'A1', 'B2', 'A1_w', 'B2_w', 'L-N', 'L-R', 'D2', 'v1-R'):
            central = b0 if name == 'B0' and b0 is not None else np.ones(len(index))
            members[name] = {'status': 'ok', 'central': central,
                             'cache_content_sha256': f'fixture-{origin}-{name}'}
            if name in ('D2', 'v1-R'):
                members[name]['quantiles'] = central[:, None]+np.arange(-3, 4)[None, :]
        return {'index': index, 'scoring_index': index, 'members': members,
                'scale': np.ones(len(index))*2, 'issue_utc': issue_time(origin), 'identity': identity}

    state = ReplayState(identity)
    released_truth = lambda index: np.zeros(len(index))
    for offset in range(33):
        origin = day-timedelta(days=33-offset)
        replay_origin(state, origin, {'nominal': bundle(origin, expected_hours(origin))}, released_truth, scored=False)
    rows = replay_origin(state, day, {'nominal': bundle(day, native_index, fit['central'])}, released_truth, scored=True)
    pop = population([day], omitted=(full[2],))
    truth = pop.keys.assign(y_true=0.)
    result = score_records(rows.values(), truth, pop, streams=tuple(rows), production=False)
    assert result['daily'].available.all() and result['daily'].scoring_hours.eq(24).all()
    assert len(rows['nominal/B0']['emitted_quantiles']) == 24
    assert not rows['nominal/B0']['error_eligible'] and not rows['nominal/v5']['error_eligible']
    state.release(day+timedelta(days=2), released_truth)
    assert day not in state.learning('nominal').pending and day not in state.learning('nominal').rows
    assert day not in state.policies['nominal/B0'].errors.consumed
    assert day not in state.policies['nominal/v5'].errors._consumed
