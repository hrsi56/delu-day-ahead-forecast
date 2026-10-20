"""Bounded synthetic disclosure/kernel fixtures; run only by the Lead monitor."""
from datetime import date, timedelta
from itertools import product
import math

import numpy as np
import pandas as pd
import pytest
from scipy import stats

from cp25.calendar import expected_hours
from cp26 import diagnostics as D
from cp26 import scoring as S
from cp26.inference import calendar_runs, draw_plan


STREAMS = ('nominal/B0', 'nominal/v5')


def daily_rows(days, *, streams=STREAMS):
    rows = []
    for stream in streams:
        for day in days:
            rows.append({'stream': stream, 'delivery_date': day, 'eligible': True,
                         'available': False, 'MAE': np.nan, 'WIS': np.nan,
                         'all_eligible': True, 'never_scored': True,
                         'old_fold_2_5': day.year <= 2025,
                         'newly_opened': day >= date(2026, 4, 8),
                         'season': {12: 'DJF', 1: 'DJF', 2: 'DJF', 3: 'MAM', 4: 'MAM', 5: 'MAM',
                                    6: 'JJA', 7: 'JJA', 8: 'JJA', 9: 'SON', 10: 'SON', 11: 'SON'}[day.month],
                         'year': day.year, 'quarter': str(pd.Period(day, freq='Q')),
                         'weekday_weekend': 'weekend' if day.weekday() >= 5 else 'weekday',
                         'nationwide_holiday': False, 'canonical_hours': len(expected_hours(day)),
                         'stress_2021_2022': day.year in (2021, 2022),
                         'negative_price_risk': 0, 'high_volatility': 0})
    return pd.DataFrame(rows)


def observations(day, stream, y, *, timestamps=None, quantiles=None):
    index = expected_hours(day) if timestamps is None else pd.DatetimeIndex(timestamps)
    y = np.broadcast_to(np.asarray(y, float), (len(index),)).copy()
    q = (np.tile([-3., -2., -1., 0., 1., 2., 3.], (len(index), 1))
         if quantiles is None else np.asarray(quantiles, float))
    rows = pd.DataFrame({'timestamp_utc': index, 'delivery_date': day, 'stream': stream,
                         'local_hour': index.tz_convert('Europe/Berlin').hour, 'y_true': y})
    for name, values in S.hourly_losses(y, q).items():
        rows[name] = values
    for j, name in enumerate(S.QUANTILES):
        rows[name] = q[:, j]
    return rows


def test_registry_contains_every_fixed_calendar_level_independent_of_outcomes():
    cells = S.registered_breakdown_cells()
    assert len(cells) == len(set(cells)) == 49
    assert cells[0] == ('overall', 'overall')
    domains = {name: [value for group, value in cells if group == name] for name in S.DAY_GROUPS}
    assert domains['season'] == ['DJF', 'MAM', 'JJA', 'SON']
    assert domains['year'] == list(range(2020, 2027))
    assert domains['quarter'] == ['2020Q4', *(f'{year}Q{quarter}' for year in range(2021, 2026)
                                            for quarter in range(1, 5)), '2026Q1', '2026Q2', '2026Q3']
    assert domains['weekday_weekend'] == ['weekday', 'weekend']
    assert domains['canonical_hours'] == [23, 24, 25]
    for group in ('nationwide_holiday', 'stress_2021_2022', 'negative_price_risk', 'high_volatility'):
        assert domains[group] == [0, 1]
    full = S.registered_breakdown_cells(include_local_hours=True)
    assert len(full) == 73 and full[:49] == cells
    assert full[49:] == tuple(('local_hour', hour) for hour in range(24))


def test_calibration_retains_registered_empty_groups_streams_and_local_hours():
    day = date(2026, 4, 8)
    daily = daily_rows([day])
    hourly = observations(day, 'nominal/B0', 0., timestamps=expected_hours(day)[:2])
    tables = D.calibration_tables(hourly, daily)
    cells = S.registered_breakdown_cells(include_local_hours=True)
    for name, endpoint, values in (('coverage', 'interval', (50, 80, 95)),
                                   ('quantile_hits', 'quantile', S.QUANTILES),
                                   ('histogram', 'bin', range(8))):
        table = tables[name]
        expected = {(mask, stream, group, value, item)
                    for mask, stream, (group, value), item in product(S.MASKS, STREAMS, cells, values)}
        assert set(table[['mask', 'stream', 'group', 'value', endpoint]].itertuples(index=False, name=None)) == expected
        assert len(table) == len(expected)
    coverage = tables['coverage']
    absent_dst = coverage[coverage['mask'].eq('newly_opened') & coverage.group.eq('canonical_hours') & coverage.value.isin([23, 25])]
    assert absent_dst.status.eq('unavailable').all() and absent_dst.reason.eq('no_calendar_support').all()
    assert absent_dst[['n_hours', 'n_dates', 'calendar_dates']].eq(0).all().all()
    absent_stream = coverage[coverage.stream.eq('nominal/v5') & coverage['mask'].eq('all_eligible') & coverage.group.eq('overall')]
    assert absent_stream.reason.eq('no_emitted_scored_hours').all() and absent_stream.calendar_dates.eq(1).all()
    absent_hour = coverage[coverage.stream.eq('nominal/B0') & coverage['mask'].eq('all_eligible') & coverage.group.eq('local_hour') & coverage.value.eq(12)]
    assert absent_hour.reason.eq('no_emitted_scored_hours').all() and absent_hour.n_hours.eq(0).all()
    for level in (50, 80, 95):
        assert coverage.loc[coverage.interval.eq(level) & coverage.status.eq('unavailable'), f'coverage{level}'].isna().all()
    empty_bins = tables['histogram'][tables['histogram'].status.eq('unavailable')]
    assert empty_bins.observed_probability.isna().all() and empty_bins.observed_over_expected.isna().all()
    assert empty_bins.expected_probability.notna().all()
    empty_hits = tables['quantile_hits'][tables['quantile_hits'].status.eq('unavailable')]
    assert empty_hits[['strict_hit', 'weak_hit', 'tie_rate']].isna().all().all()


def test_wholly_empty_hourly_tables_keep_all_required_cells_without_zero_estimates():
    daily = daily_rows([date(2026, 4, 8)])
    tables = D.calibration_tables(pd.DataFrame(), daily)
    for name, multiplier in (('coverage', 3), ('quantile_hits', 7), ('histogram', 8)):
        table = tables[name]
        assert len(table) == 4*2*73*multiplier
        assert table.status.eq('unavailable').all()
        assert table.n_hours.eq(0).all() and table.n_dates.eq(0).all()
    transitions = D.christoffersen(pd.DataFrame(), daily)
    assert len(transitions) == 4*2*3
    assert transitions.status.eq('insufficient_support').all() and transitions.n_hours.eq(0).all()
    assert transitions[['p_UC', 'p_IND', 'p_CC']].eq(1.).all().all()
    slices = D.realized_outcome_slices(pd.DataFrame(), daily)['slices']
    assert len(slices) == 4*2*2*2
    negative = slices[slices['slice'].eq('negative_realized_hour')]
    assert len(negative) == 4*2*2 and negative.status.eq('unavailable').all()
    assert negative.n_dates.eq(0).all() and negative.n_hours.eq(0).all() and negative.mean_daily_loss.isna().all()


def test_complete_score_breakdowns_and_local_hour_grid_keep_missing_stream():
    day = date(2026, 4, 8)
    daily = daily_rows([day])
    daily.loc[daily.stream.eq('nominal/B0'), ['available', 'MAE', 'WIS']] = [True, 1., 2.]
    summary = S.summaries(daily)
    assert len(summary) == 4*2*49*2
    unavailable = summary[summary['mask'].eq('newly_opened') & summary.group.eq('canonical_hours') & summary.value.eq(23)]
    assert unavailable.reason.eq('no_calendar_support').all() and unavailable.raw_mean_daily_loss.isna().all()
    hourly = observations(day, 'nominal/B0', 1., timestamps=expected_hours(day)[:1])
    local = S.local_hour_summaries(hourly, daily)
    expected = set(product(S.MASKS, STREAMS, range(24), ('MAE', 'WIS')))
    assert set(local[['mask', 'stream', 'local_hour', 'metric']].itertuples(index=False, name=None)) == expected
    assert len(local) == len(expected)
    missing = local[local.stream.eq('nominal/v5')]
    assert missing.status.eq('unavailable').all() and missing.n_hours.eq(0).all()
    assert missing.raw_mean_daily_loss.isna().all() and missing.B0_ratio.isna().all()
    empty = S.local_hour_summaries(pd.DataFrame(), daily)
    assert len(empty) == len(expected) and empty.status.eq('unavailable').all()
    assert empty[['raw_mean_daily_loss', 'paired_B0_loss', 'B0_ratio']].isna().all().all()


def test_supported_calibration_keeps_equal_date_weighting_and_upper_tie_bins():
    spring, autumn = date(2021, 3, 28), date(2021, 10, 31)
    hourly = pd.concat([observations(spring, 'nominal/B0', 1.), observations(autumn, 'nominal/B0', 4.)], ignore_index=True)
    tables = D.calibration_tables(hourly, daily_rows([spring, autumn], streams=('nominal/B0',)))
    overall = tables['coverage'].query("mask == 'all_eligible' and group == 'overall'")
    row = overall[overall.interval.eq(50)].iloc[0]
    assert row.status == 'computable' and pd.isna(row.reason) and row.n_hours == 48 and row.n_dates == 2
    assert row.coverage50 == .5 and row.pooled_hour_coverage50 == pytest.approx(23/48)
    bins = tables['histogram'].query("mask == 'all_eligible' and group == 'overall'").set_index('bin')
    assert bins.at[5, 'observed_probability'] == .5 and bins.at[7, 'observed_probability'] == .5
    assert bins.at[5, 'pooled_hour_probability'] == pytest.approx(23/48)
    hit = tables['quantile_hits'].query("mask == 'all_eligible' and group == 'overall' and quantile == 'p75'").iloc[0]
    assert hit.strict_hit == 0. and hit.weak_hit == .5 and hit.tie_rate == .5


def test_local_hour_duplicates_are_averaged_before_equal_date_and_paired_ratio():
    autumn, normal = date(2021, 10, 31), date(2021, 11, 1)
    rows = []
    for day, values in ((autumn, [2., 6.]), (normal, [8.])):
        index = expected_hours(day)
        index = index[index.tz_convert('Europe/Berlin').hour == 2]
        y = np.array(values)
        rows.append(observations(day, 'nominal/v5', y, timestamps=index))
        baseline = y[:, None]+np.array([-3., -2., -1., 1., 2., 3., 4.])
        rows.append(observations(day, 'nominal/B0', y, timestamps=index, quantiles=baseline))
    local = S.local_hour_summaries(pd.concat(rows, ignore_index=True), daily_rows([autumn, normal]))
    row = local.query("mask == 'all_eligible' and stream == 'nominal/v5' and local_hour == 2 and metric == 'MAE'").iloc[0]
    assert row.raw_mean_daily_loss == 6. and row.B0_ratio == 6.
    assert row.n_hours == 3 and row.n_dates == row.paired_dates == 2
    assert row.status == row.ratio_status == 'computable'


def test_christoffersen_counts_only_exact_utc_adjacency_across_dst_and_gaps():
    spring, autumn = date(2021, 3, 28), date(2021, 10, 31)
    spring_hours = expected_hours(spring).delete(6)
    autumn_hours = expected_hours(autumn)
    assert len(expected_hours(spring)) == 23 and len(autumn_hours) == 25
    assert (autumn_hours.tz_convert('Europe/Berlin').hour == 2).sum() == 2
    pattern = np.array([False, False, True, True, False, True])
    timestamps = spring_hours.append(autumn_hours)
    hits = np.resize(pattern, len(timestamps))
    hourly = pd.concat([observations(spring, 'nominal/B0', np.where(hits[:len(spring_hours)], .5, 4.), timestamps=spring_hours),
                        observations(autumn, 'nominal/B0', np.where(hits[len(spring_hours):], .5, 4.))], ignore_index=True)
    row = D.christoffersen(hourly.sample(frac=1., random_state=31), daily_rows([spring, autumn], streams=('nominal/B0',)))
    row = row.query("mask == 'all_eligible' and interval == 50").iloc[0]
    counts = np.zeros((2, 2), int)
    for prior_t, next_t, prior_hit, next_hit in zip(timestamps[:-1], timestamps[1:], hits[:-1], hits[1:]):
        if next_t-prior_t == pd.Timedelta(hours=1):
            counts[int(prior_hit), int(next_hit)] += 1
    assert row.status == 'computable' and row.transition_counts == counts.tolist()
    assert row.n_adjacent_transitions == int(counts.sum()) == len(timestamps)-3
    def ll(a, b):
        total = a+b
        if not total:
            return 0.
        return (a*math.log(a/total) if a else 0.)+(b*math.log(b/total) if b else 0.)
    n1, n0 = int(hits.sum()), int((~hits).sum())
    uc = 2*(ll(n0, n1)-(n0+n1)*math.log(.5))
    n00, n01, n10, n11 = counts.ravel()
    ind = 2*(ll(n00, n01)+ll(n10, n11)-ll(n00+n10, n01+n11))
    assert row.LR_UC == pytest.approx(uc) and row.LR_IND == pytest.approx(ind)
    assert row.LR_CC == pytest.approx(uc+ind) and row.p_CC == pytest.approx(stats.chi2.sf(uc+ind, 2))


def test_christoffersen_no_gap_bridge_and_bound_tie_unavailability():
    day = date(2021, 1, 1)
    index = expected_hours(day)[[0, 2]]
    daily = daily_rows([day], streams=('nominal/B0',))
    hourly = observations(day, 'nominal/B0', [.5, 4.], timestamps=index)
    rows = D.christoffersen(hourly, daily).query("mask == 'all_eligible'")
    assert rows.status.eq('no_adjacent_transitions').all()
    assert all(counts == [[0, 0], [0, 0]] for counts in rows.transition_counts)
    assert rows[['p_IND', 'p_CC']].eq(1.).all().all()
    hourly.loc[0, 'y_true'] = hourly.loc[0, 'p25']
    tied = D.christoffersen(hourly, daily).query("mask == 'all_eligible' and interval == 50").iloc[0]
    assert tied.status == 'forecast_bound_ties' and tied.bound_ties == 1
    assert tied.p_UC == tied.p_IND == tied.p_CC == 1.


def moment_cell():
    # Two calendar years and one genuine date gap exercise stratum centering
    # and original calendar lags. No experimental forecast or truth is read.
    days = [date(2021, 7, 1)+timedelta(days=i) for i in range(420) if i != 100]
    y = np.random.default_rng(619).choice([-4., -1.5, .5, 1.5, 4.], size=len(days), p=[.1, .15, .45, .15, .15])
    cell = pd.DataFrame({'delivery_date': days, 'y_true': y})
    q = np.tile([-3., -2., -1., 0., 1., 2., 3.], (len(days), 1))
    for j, name in enumerate(S.QUANTILES):
        cell[name] = q[:, j]
    for name, values in S.hourly_losses(y, q).items():
        cell[name] = values
    return cell


def manual_stratum_hac(vectors, runs):
    centered = vectors.copy()
    for stratum in sorted({s for _, _, s in runs}):
        positions = np.array([i for begin, end, s in runs if s == stratum for i in range(begin, end)])
        centered[positions] -= centered[positions].mean(axis=0)
    covariance = centered.T @ centered
    for lag in range(1, 15):
        for begin, end, _ in runs:
            if end-begin > lag:
                term = centered[begin+lag:end].T @ centered[begin:end-lag]
                covariance += (1-lag/15)*(term+term.T)
    return covariance/len(vectors)**2


def test_valid_moment_original_lags_covariance_draws_and_reestimated_replicate():
    cell = moment_cell()
    rng = np.random.default_rng(991)
    result = D.moment_test(cell, interval=50, rng=rng, replicates=8, production=False)
    assert result['status'] == 'computable' and result['n_moment_dates'] >= 180 and result['HAC_lag'] == 14
    hits = dict(zip(cell.delivery_date, cell.coverage50.astype(float)))
    dates = [day for day in cell.delivery_date if day-timedelta(days=1) in hits and day-timedelta(days=7) in hits]
    vectors = np.array([[hits[day]-.5, (hits[day]-.5)*(hits[day-timedelta(days=1)]-.5),
                         (hits[day]-.5)*(hits[day-timedelta(days=7)]-.5)] for day in dates])
    assert result['moment_dates'] == list(map(str, dates))
    np.testing.assert_array_equal(result['moment_vectors'], vectors)
    runs = calendar_runs(dates)
    assert len(runs) > 2 and {s for _, _, s in runs} == {2021, 2022}
    covariance = manual_stratum_hac(vectors, runs)
    np.testing.assert_allclose(result['observed_HAC_covariance_of_mean'], covariance, rtol=1e-12, atol=1e-14)
    mean = vectors.mean(axis=0)
    assert result['statistic'] == pytest.approx(mean @ np.linalg.solve(covariance, mean))
    reference_rng = np.random.default_rng(991)
    plan = draw_plan(dates, rng=reference_rng, replicates=8)
    np.testing.assert_array_equal(result['draw_starts'], plan.starts)
    assert rng.bit_generator.state == reference_rng.bit_generator.state
    sampled = vectors[plan.indices(0, 1)[0]]
    assert np.any(sampled[7:, 1] != sampled[7:, 0]*sampled[6:-1, 0])
    replicate_covariance = manual_stratum_hac(sampled, runs)
    centered_mean = sampled.mean(axis=0)-mean
    expected = centered_mean @ np.linalg.solve(replicate_covariance, centered_mean)
    assert result['replicate_statistics'][0] == pytest.approx(expected)
    count = int((result['replicate_statistics'] >= result['statistic']).sum())
    assert result['upper_tail_count'] == count and result['p_value'] == (1+count)/9
    lower = stats.beta.ppf(.025, count, 9-count) if count else 0.
    upper = stats.beta.ppf(.975, count+1, 8-count) if count < 8 else 1.
    assert result['monte_carlo_probability_ci95'] == pytest.approx((lower, upper))


def test_actual_moment_family_shared_rng_order_unavailable_skip_and_restart_equality():
    base = moment_cell()
    first = base.copy()
    first.loc[0, 'y_true'] = first.loc[0, 'p25']  # unavailable50 only; 80/95 still use shared draws
    first['stream'], first['local_hour'] = 'nominal/B0', 0
    second = base.copy()
    second['stream'], second['local_hour'] = 'nominal/v5', 1
    hourly = pd.concat([first, second], ignore_index=True)
    daily = daily_rows(base.delivery_date.tolist())
    # The actual family selector requires24-hour dates, as in production.
    daily = daily[daily.canonical_hours.eq(24)].copy()
    hourly = hourly[hourly.delivery_date.isin(daily.delivery_date)]
    family = list(D.iter_moment_family(hourly, daily, streams=STREAMS, replicates=4, production=False))
    expected_order = [f'{stream}/hour{hour:02d}/interval{level}' for stream in sorted(STREAMS)
                      for hour in range(24) for level in (50, 80, 95)]
    assert [row['identity'] for row in family] == expected_order
    reference_rng = np.random.default_rng(D.MOMENT_SEED)
    for row in family:
        cell = hourly[hourly.stream.eq(row['stream']) & hourly.local_hour.eq(row['local_hour'])]
        original_state = reference_rng.bit_generator.state
        reference = D.moment_test(cell, interval=row['interval'], rng=reference_rng, replicates=4, production=False)
        assert row['status'] == reference['status']
        np.testing.assert_array_equal(row['draw_starts'], reference['draw_starts'])
        np.testing.assert_array_equal(row['replicate_statistics'], reference['replicate_statistics'])
        if reference['draw_starts'].size == 0:
            assert reference_rng.bit_generator.state == original_state
    assert sum(row['status'] == 'computable' for row in family) == 5
    # Reconstructing the iterator after a durable prefix regenerates exactly
    # the same later draws; it does not seed each available cell separately.
    restart = D.iter_moment_family(hourly, daily, streams=STREAMS, replicates=4, production=False)
    prefix = 74
    for _ in range(prefix):
        next(restart)
    for row, resumed in zip(family[prefix:], restart):
        assert row['identity'] == resumed['identity']
        np.testing.assert_array_equal(row['draw_starts'], resumed['draw_starts'])
        np.testing.assert_array_equal(row['replicate_statistics'], resumed['replicate_statistics'])


def test_production_empty_moment_family_stays936_p1_cells_without_draws():
    daily = daily_rows([date(2026, 4, 8)], streams=S.RESEARCH_STREAMS)
    family = list(D.iter_moment_family(pd.DataFrame(), daily))
    assert len(family) == 936 and all(row['p_value'] == 1. for row in family)
    assert all(row['draw_starts'].size == row['replicate_statistics'].size == 0 for row in family)
    adjusted = D.moment_holm(family)
    assert len(adjusted) == 936 and all(row['family_size'] == 936 and not row['rejected'] for row in adjusted.values())
