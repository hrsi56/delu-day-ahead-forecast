"""Small synthetic inference fixtures; never a CP-26 experimental finding."""
from datetime import date, timedelta
import hashlib
import json

import numpy as np
import pandas as pd
import pytest

from cp26.inference import (calendar_runs, draw_plan, hac_variance_mean, holm,
                           paired_bootstrap, giacomini_white, model_confidence_set,
                           secondary_ratio_bootstrap, write_result_artifact)
from cp26.diagnostics import christoffersen, moment_test


def pair(n=70):
    t = np.arange(n, dtype=float)
    return pd.DataFrame({'delivery_date': [date(2021, 1, 1)+timedelta(days=i) for i in range(n)],
                         'a': 2.+.01*t+.2*np.sin(t/3), 'b': 3.+.015*t+.15*np.cos(t/5)})


def test_runs_break_real_gaps_and_years_but_join_2020_to_2021():
    dates = [date(2020, 12, 31), date(2021, 1, 1), date(2021, 1, 3), date(2021, 12, 31), date(2022, 1, 1)]
    assert calendar_runs(dates) == ((0, 2, 2021), (2, 3, 2021), (3, 4, 2021), (4, 5, 2022))
    assert calendar_runs(dates, stratified=False) == ((0, 2, 0), (2, 3, 0), (3, 5, 0))


def test_non_circular_draws_preserve_run_counts_and_short_run_whole_length():
    dates = [date(2021, 1, 1)+timedelta(days=i) for i in range(17)] + [date(2021, 2, i) for i in (1, 2, 3)]
    plan = draw_plan(dates, block_days=14, replicates=8)
    indices = plan.indices()
    assert indices.shape == (8, 20)
    assert (indices[:, :17] < 17).all()
    np.testing.assert_array_equal(indices[:, 17:], np.tile([17, 18, 19], (8, 1)))
    assert plan.starts[:, :2].max() <= 3 and plan.starts[:, 2].max() == 0
    replay = draw_plan(dates, block_days=14, replicates=8)
    np.testing.assert_array_equal(plan.starts, replay.starts)


def test_calendar_hac_has_fixed_lag14_and_global_demeaning_without_gap_pairs():
    d = np.array([1., 3., 2., 8., 5.])
    runs = ((0, 3, 2021), (3, 5, 2021))
    z = d-d.mean()
    expected = z @ z
    for lag in range(1, 15):
        expected += 2*(1-lag/15)*sum(z[begin+lag:end] @ z[begin:end-lag]
                                        for begin, end, _ in runs if end-begin > lag)
    assert hac_variance_mean(d, runs) == pytest.approx(expected/len(d)**2)


def test_studentized_difference_ratio_shared_draws_and_manual_pivot_recomputation():
    p = pair()
    result = paired_bootstrap(p, replicates=20, production=False)
    assert result['difference_status'] == result['ratio_status'] == 'computable'
    plan = draw_plan(p.delivery_date, replicates=20)
    np.testing.assert_array_equal(plan.starts, result['draw_starts'])
    indices = plan.indices(0, 1)[0]
    a, b = p.a.to_numpy()[indices], p.b.to_numpy()[indices]
    d = a-b
    pivot = (d.mean()-result['difference'])/np.sqrt(hac_variance_mean(d, plan.runs))
    assert result['difference_pivots'][0] == pytest.approx(pivot)
    ratio = a.mean()/b.mean()
    influence = (a-ratio*b)/b.mean()
    ratio_pivot = (ratio-result['ratio'])/np.sqrt(hac_variance_mean(influence, plan.runs))
    assert result['ratio_pivots'][0] == pytest.approx(ratio_pivot)
    upper = np.quantile(result['ratio_pivots'], .975, method='linear')
    assert result['ratio_ci95'][0] == pytest.approx(result['ratio']-upper*np.sqrt(result['ratio_variance']))


def test_degenerate_observation_consumes_no_draw_and_no_floor_or_rescue():
    p = pair()
    p['a'] = p.b
    rng = np.random.default_rng(101)
    original = rng.bit_generator.state
    result = paired_bootstrap(p, rng=rng, replicates=10, production=False, include_raw=False)
    assert result['difference_p_value'] == 1.
    assert result['draw_starts'].size == 0 and rng.bit_generator.state == original
    assert result['difference_status'] == 'nonpositive_or_nonfinite_observed_variance'
    raw = paired_bootstrap(p, replicates=10, production=False)
    assert raw['raw_left_status'] == 'computable'
    assert np.isfinite(raw['raw_left_ci95']).all() and raw['ratio'] == 1.
    assert not np.isfinite(raw['ratio_ci95']).any()
    p['b'] = 0.
    result = paired_bootstrap(p, replicates=10, production=False)
    assert result['ratio_status'] == 'zero_or_nonfinite_denominator'


def test_replication_override_is_fixture_only():
    with pytest.raises(ValueError, match='10,000'):
        paired_bootstrap(pair(), replicates=5)
    with pytest.raises(ValueError, match='100,000'):
        moment_test(pd.DataFrame(), interval=50, replicates=5)


def test_holm_keeps_unavailable_cells_and_stops_at_first_failure():
    result = holm({'a': .01, 'b': .025, 'c': 1.})
    assert result['a']['rejected'] and result['b']['rejected'] and not result['c']['rejected']
    assert result['a']['adjusted_p_value'] == pytest.approx(.03)
    assert result['b']['adjusted_p_value'] == pytest.approx(.05)
    assert result['c']['family_size'] == 3


def test_gw_keeps_unknown_volatility_with_disclosed_support_and_exact_lag1():
    p = pair(60)
    states = pd.DataFrame({'delivery_date': p.delivery_date, 'negative_price_risk': (np.arange(60)%3 == 0).astype(int),
                           'high_volatility': np.zeros(60, int), 'volatility_unknown': np.ones(60, int)})
    result = giacomini_white(p, states)
    assert result['n_dates'] == 59 and result['volatility_unknown_dates'] == 59
    assert result['status'] == 'unavailable_covariance_or_support'  # fifth instrument is constant zero
    p = p.drop(index=20)
    result = giacomini_white(p, states)
    assert result['n_dates'] == 57 and result['excluded_instrument_dates'] == 2


def test_mcs_undefined_pair_preserves_remaining_set_and_history():
    p = pair(35)
    x = pd.DataFrame({'z': p.a.to_numpy(), 'a': p.a.to_numpy()}, index=p.delivery_date)
    result = model_confidence_set(x, mask='all_eligible', metric='MAE', replicates=8, production=False)
    assert result['status'] == 'unavailable_pair_variance' and result['remaining'] == ['a', 'z']
    assert result['replicate_means'].shape == (8, 2) and result['draw_starts'].shape[0] == 8


def test_moment_ties_or_insufficient_support_are_p1_without_draws():
    p = pair(10)
    h = pd.DataFrame({'delivery_date': p.delivery_date, 'y_true': 1., 'p025': 0., 'p10': 0., 'p25': 0.,
                      'p50': .5, 'p75': 2., 'p90': 2., 'p975': 2., 'coverage50': True})
    result = moment_test(h, interval=50, replicates=8, production=False)
    assert result['status'] == 'fewer_than_180_complete_moment_dates' and result['p_value'] == 1.
    h.loc[0, 'y_true'] = h.loc[0, 'p25']
    result = moment_test(h, interval=50, replicates=8, production=False)
    assert result['status'] == 'forecast_bound_ties' and result['draw_starts'].size == 0


def test_secondary_requires_all_groups_and_recomputes_counts_ratios_influence():
    missing = secondary_ratio_bootstrap(pair(70), group='season', replicates=8, production=False)
    assert missing['status'] == 'missing_or_undefined_registered_group'
    dates = [date(2021, 1, 1)+timedelta(days=i) for i in range(365)]
    t = np.arange(365, dtype=float)
    p = pd.DataFrame({'delivery_date': dates, 'a': 2.+np.sin(t/9), 'b': 4.+np.cos(t/7)})
    result = secondary_ratio_bootstrap(p, group='season', replicates=8, production=False)
    assert result['status'] == 'computable'
    assert result['group_counts'].tolist() == [90, 92, 92, 91]
    assert result['replicate_group_counts'].sum(axis=1).tolist() == [365]*8
    assert result['ratio'] == pytest.approx(np.mean(result['group_ratios']))
    years = secondary_ratio_bootstrap(p, group='year', replicates=8, production=False)
    assert years['status'] == 'missing_or_undefined_registered_group'


def test_numeric_artifact_preserves_arrays_hashes_and_refuses_overwrite(tmp_path):
    result = {'kind': 'fixture', 'variant': 'primary14', 'mask': 'all_eligible', 'metric': 'MAE',
              'pivots': np.array([1., np.nan]), 'ci95': (np.nan, 3.)}
    record = write_result_artifact(tmp_path, 'reports/rebaseline/fixture/endpoint', result)
    metadata_path, arrays_path = tmp_path/record['metadata_path'], tmp_path/record['arrays_path']
    assert hashlib.sha256(metadata_path.read_bytes()).hexdigest() == record['metadata_sha256']
    assert hashlib.sha256(arrays_path.read_bytes()).hexdigest() == record['arrays_sha256']
    metadata = json.loads(metadata_path.read_text())
    assert metadata['result']['ci95'] == [None, 3.]
    with np.load(arrays_path, allow_pickle=False) as arrays:
        np.testing.assert_array_equal(arrays[metadata['result']['pivots']['array']], [1., np.nan])
    with pytest.raises(ValueError, match='overwriting'):
        write_result_artifact(tmp_path, 'reports/rebaseline/fixture/endpoint', result)
