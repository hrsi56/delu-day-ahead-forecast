"""Actual CP-26 iterator/RNG fixtures; no experimental outcomes or mock kernels."""
from datetime import date, timedelta
import math

import numpy as np
import pandas as pd
import pytest

from cp26 import inference as I


STREAMS = ('nominal/v4', 'nominal/B0', 'nominal/v3')  # deliberately not lexical
COMPARISONS = (('nominal/v3', 'nominal/B0'), ('nominal/v4', 'nominal/B0'),
               ('nominal/v4', 'nominal/v3'))
MASKS = ('all_eligible', 'never_scored', 'old_fold_2_5', 'newly_opened')
VARIANTS = (('primary14', 14, True), ('sensitivity7', 7, True),
            ('sensitivity28', 28, True), ('unstratified14', 14, False))
CELLS = (('overall', 'overall'), *(('year', year) for year in range(2020, 2027)),
         *(('season', season) for season in ('DJF', 'MAM', 'JJA', 'SON')))
FIXTURE_REPLICATES = 3
SEED = 20261012


def synthetic_daily():
    days = [date(2020, 12, 29)+timedelta(days=i) for i in range(3)]
    for first in (date(2021, 1, 1), date(2021, 4, 1), date(2021, 7, 1), date(2021, 10, 1)):
        days.extend(first+timedelta(days=i) for i in range(35))
    for year in range(2022, 2026):
        days.extend(date(year, 1, 1)+timedelta(days=i) for i in range(8))
    days.extend(date(2026, 4, 8)+timedelta(days=i) for i in range(9))
    days = sorted(days)
    t = np.arange(len(days), dtype=float)
    losses = {'nominal/B0': 3.+.15*np.sin(t/3)+.002*t,
              'nominal/v3': 2.+.2*np.cos(t/5)+.001*t,
              'nominal/v4': 2.5+.12*np.sin(t/7)+.0015*t}
    constant = {'nominal/B0': 1., 'nominal/v3': 2., 'nominal/v4': 3.}
    rows = []
    for stream in STREAMS:
        for i, day in enumerate(days):
            missing = stream == 'nominal/v3' and day == date(2021, 4, 5)
            rows.append({'stream': stream, 'delivery_date': day,
                         'MAE': np.nan if missing else constant[stream],
                         'WIS': np.nan if missing else losses[stream][i],
                         'all_eligible': True, 'never_scored': day.year == 2026,
                         'old_fold_2_5': 2021 <= day.year <= 2025, 'newly_opened': day.year == 2026,
                         'year': day.year,
                         'season': {12: 'DJF', 1: 'DJF', 2: 'DJF', 3: 'MAM', 4: 'MAM', 5: 'MAM',
                                    6: 'JJA', 7: 'JJA', 8: 'JJA', 9: 'SON', 10: 'SON', 11: 'SON'}[day.month]})
    return pd.DataFrame(rows)


def expected_identities():
    """Independent registry: comparisons, masks, cells, metrics, then streams."""
    rows = []
    for variant, _, _ in VARIANTS:
        for left, right in COMPARISONS:
            for mask in MASKS:
                for group, value in CELLS:
                    for metric in ('MAE', 'WIS'):
                        rows.append(('paired_comparison', variant, left, right, mask, group, value, metric))
        for stream in sorted(STREAMS):
            for mask in MASKS:
                for group, value in CELLS:
                    for metric in ('MAE', 'WIS'):
                        rows.append(('own_raw_loss', variant, stream, None, mask, group, value, metric))
        for stream in sorted(STREAMS):
            for mask in MASKS:
                for group in ('season', 'year'):
                    for metric in ('MAE', 'WIS'):
                        rows.append(('secondary_mean_ratio', variant, stream, None, mask, group, None, metric))
    return rows


def identity(row):
    return (row['kind'], row['variant'], row.get('left', row.get('stream')), row.get('right'),
            row['mask'], row['group'], row.get('value'), row['metric'])


def manual_pair(daily, endpoint):
    """Select the shared fixture calendar without invoking paired_losses."""
    kind, _, left, right, mask, group, value, metric = endpoint
    right = left if kind == 'own_raw_loss' else 'nominal/B0' if kind == 'secondary_mean_ratio' else right
    a = daily[daily.stream.eq(left)].set_index('delivery_date').sort_index()
    b = daily[daily.stream.eq(right)].set_index('delivery_date').sort_index()
    assert a.index.equals(b.index)
    selected = a[mask].to_numpy(dtype=bool, copy=True)
    if kind != 'secondary_mean_ratio' and group != 'overall':
        selected &= a[group].eq(value).to_numpy()
    available = np.isfinite(a[metric].to_numpy()) & np.isfinite(b[metric].to_numpy())
    pair = pd.DataFrame({'delivery_date': a.index[selected & available],
                         'a': a[metric].to_numpy()[selected & available],
                         'b': b[metric].to_numpy()[selected & available]})
    if kind == 'secondary_mean_ratio' and group == 'year':
        pair = pair[pair.delivery_date.map(lambda day: 2021 <= day.year <= 2025)].reset_index(drop=True)
    return pair


def manual_plan(dates, *, block_days, stratified, rng, replicates):
    """Independent full noncircular starts, run counts and right truncation."""
    dates = list(dates)
    runs = []
    start = 0
    for i, day in enumerate(dates):
        stratum = max(2021, day.year) if stratified else 0
        if i and (day-dates[i-1] != timedelta(days=1) or
                  stratum != (max(2021, dates[i-1].year) if stratified else 0)):
            runs.append((start, i))
            start = i
    if dates:
        runs.append((start, len(dates)))
    highs, columns = [], []
    for begin, end in runs:
        length = min(block_days, end-begin)
        blocks = math.ceil((end-begin)/length)
        columns.append((len(highs), len(highs)+blocks))
        highs.extend([end-begin-length+1]*blocks)
    starts = rng.integers(0, np.array(highs, dtype=np.int64),
                          size=(replicates, len(highs)), dtype=np.int32)
    indices = np.empty((replicates, len(dates)), dtype=np.int32)
    for (begin, end), (first, last) in zip(runs, columns):
        length = min(block_days, end-begin)
        for j, col in enumerate(range(first, last)):
            count = min(length, end-begin-j*length)
            indices[:, begin+j*length:begin+j*length+count] = begin+starts[:, col, None]+np.arange(count)[None, :]
    return starts, indices


def group_labels(pair, group):
    if group == 'year':
        return np.array([day.year for day in pair.delivery_date]), tuple(range(2021, 2026))
    labels = {12: 'DJF', 1: 'DJF', 2: 'DJF', 3: 'MAM', 4: 'MAM', 5: 'MAM',
              6: 'JJA', 7: 'JJA', 8: 'JJA', 9: 'SON', 10: 'SON', 11: 'SON'}
    return np.array([labels[day.month] for day in pair.delivery_date]), ('DJF', 'MAM', 'JJA', 'SON')


def assert_equal_result(actual, expected):
    """Every retained scalar, array, draw label and degeneracy is restart-equal."""
    if isinstance(expected, np.ndarray):
        np.testing.assert_array_equal(actual, expected)
    elif isinstance(expected, dict):
        assert set(actual) == set(expected)
        for key, value in expected.items():
            assert_equal_result(actual[key], value)
    elif isinstance(expected, (tuple, list)):
        assert len(actual) == len(expected)
        for a, b in zip(actual, expected):
            assert_equal_result(a, b)
    elif isinstance(expected, (float, np.floating)) and np.isnan(expected):
        assert np.isnan(actual)
    else:
        assert actual == expected


@pytest.fixture(scope='module')
def actual_results():
    daily = synthetic_daily()
    # The production iterator, registry, selector and numeric kernels remain
    # real. Only the documented fixture replicate override is used.
    return daily, list(I.iter_inference(daily, replicates=FIXTURE_REPLICATES, production=False))


def test_actual_iterator_preserves_registered_order_and_empty_endpoints(actual_results):
    daily, rows = actual_results
    expected = expected_identities()
    assert len(expected) == len(rows) == 2496
    assert [identity(row) for row in rows] == expected
    assert len({I.endpoint_identity(row) for row in rows}) == len(rows)
    assert tuple(I.comparison_registry(daily.stream.unique())) == COMPARISONS
    unavailable = [row for row in rows if row['kind'] == 'paired_comparison' and row['calendar_dates'] == 0]
    assert unavailable and all(row['paired_dates'] == row['n_dates'] == 0 for row in unavailable)
    assert all(row['difference_p_value'] == 1. and row['draw_starts'].size == 0 for row in unavailable)
    assert all(np.isnan(row['difference_ci95']).all() and np.isnan(row['ratio_ci95']).all() for row in unavailable)
    missing = next(row for row in rows if identity(row) == ('paired_comparison', 'primary14', 'nominal/v3',
                                                          'nominal/B0', 'all_eligible', 'overall', 'overall', 'WIS'))
    assert missing['left_missing_dates'] == missing['either_missing_dates'] == 1
    assert missing['right_missing_dates'] == 0 and missing['paired_dates'] == len(daily)//3-1


def test_actual_iterator_uses_variant_seed_reset_and_one_ordered_shared_rng(actual_results):
    daily, rows = actual_results
    expected = expected_identities()
    first_draw = {}
    for variant, block_days, stratified in VARIANTS:
        rng = np.random.default_rng(SEED)
        for row, endpoint in zip(rows, expected):
            if endpoint[1] != variant:
                continue
            pair = manual_pair(daily, endpoint)
            assert row['n_dates'] == len(pair)
            if endpoint[0] == 'secondary_mean_ratio':
                labels, levels = group_labels(pair, endpoint[5])
                # Constant MAE and B0/B0 ratios have exactly zero influence;
                # unsupported secondary groups must never consume a draw.
                should_draw = endpoint[-1] == 'WIS' and endpoint[2] != 'nominal/B0' and set(labels) == set(levels)
            else:
                # All nonempty WIS fixture cells have variable raw losses;
                # constant MAE has no defined variance in any endpoint.
                should_draw = endpoint[-1] == 'WIS' and len(pair) >= 2
            if not should_draw:
                assert row['draw_starts'].size == 0 and row['draw_metadata'] is None
                continue
            starts, indices = manual_plan(pair.delivery_date, block_days=block_days, stratified=stratified,
                                          rng=rng, replicates=FIXTURE_REPLICATES)
            np.testing.assert_array_equal(row['draw_starts'], starts)
            assert row['draw_starts'].shape[0] == FIXTURE_REPLICATES
            first_draw.setdefault(variant, (row, starts))
            ar, br = pair.a.to_numpy()[indices], pair.b.to_numpy()[indices]
            if endpoint[0] == 'secondary_mean_ratio':
                drawn_labels = labels[indices]
                counts = np.stack([(drawn_labels == level).sum(axis=1) for level in levels], axis=1)
                ratios = np.stack([np.where(drawn_labels == level, ar, 0.).sum(axis=1)/
                                   np.where(drawn_labels == level, br, 0.).sum(axis=1) for level in levels], axis=1)
                np.testing.assert_array_equal(row['replicate_group_counts'], counts)
                np.testing.assert_allclose(row['replicate_group_ratios'], ratios)
                np.testing.assert_allclose(row['replicate_ratios'], ratios.mean(axis=1))
            else:
                np.testing.assert_allclose(row['replicate_left_losses'], ar.mean(axis=1))
                np.testing.assert_allclose(row['replicate_right_losses'], br.mean(axis=1))
                np.testing.assert_allclose(row['replicate_differences'], (ar-br).mean(axis=1))
                if row['ratio_status'] == 'computable':
                    np.testing.assert_allclose(row['replicate_ratios'], ar.mean(axis=1)/br.mean(axis=1))
    assert set(first_draw) == {variant for variant, _, _ in VARIANTS}
    # Primary and unstratified initial populations have the same real runs in
    # this fixture. Exact initial starts independently prove both start at the
    # seed; their later cells remain checked against their own ordered RNG.
    np.testing.assert_array_equal(first_draw['primary14'][1], first_draw['unstratified14'][1])
    own = [row for row in rows if row['kind'] == 'own_raw_loss' and row['metric'] == 'WIS' and row['n_dates'] >= 2]
    assert own and all(row['difference_p_value'] == 1. and row['draw_starts'].shape[0] == FIXTURE_REPLICATES for row in own)
    assert all(row['raw_left_status'] == 'computable' and np.isfinite(row['raw_left_ci95']).all() for row in own)
    assert all(np.isnan(row['difference_ci95']).all() for row in own)


def test_actual_iterator_partial_replay_preserves_all_later_arrays_and_statuses(actual_results):
    daily, rows = actual_results
    prefix = next(i for i, row in enumerate(rows) if row['variant'] == 'sensitivity7' and row['kind'] == 'own_raw_loss')+17
    replay = I.iter_inference(daily, replicates=FIXTURE_REPLICATES, production=False)
    # Replaying stored prefix endpoints advances the actual shared RNG; a
    # resumed caller must not jump straight to a new endpoint/seed.
    for original in rows[:prefix]:
        assert_equal_result(next(replay), original)
    count = 0
    for original, resumed in zip(rows[prefix:], replay):
        assert I.endpoint_identity(resumed) == I.endpoint_identity(original)
        assert_equal_result(resumed, original)
        count += 1
    assert count == len(rows)-prefix
    with pytest.raises(StopIteration):
        next(replay)


def test_actual_iterator_retains_invalid_replicates_without_redraw_or_drop():
    days = [date(2021, 1, 1)+timedelta(days=i) for i in range(20)]
    rows = []
    for stream in ('nominal/v3', 'nominal/B0'):
        for i, day in enumerate(days):
            rows.append({'stream': stream, 'delivery_date': day, 'MAE': 2. if stream == 'nominal/v3' else 1.,
                         'WIS': 5. if stream == 'nominal/v3' and i == 0 else 3.,
                         **{mask: True for mask in MASKS}, 'year': 2021, 'season': 'DJF'})
    daily = pd.DataFrame(rows)
    iterator = I.iter_inference(daily, replicates=24, production=False)
    constant = next(iterator)
    assert constant['metric'] == 'MAE' and constant['draw_starts'].size == 0
    result = next(iterator)
    assert identity(result) == ('paired_comparison', 'primary14', 'nominal/v3', 'nominal/B0',
                                'all_eligible', 'overall', 'overall', 'WIS')
    starts, indices = manual_plan(days, block_days=14, stratified=True,
                                  rng=np.random.default_rng(SEED), replicates=24)
    np.testing.assert_array_equal(result['draw_starts'], starts)
    invalid = (indices != 0).all(axis=1)
    assert 0 < invalid.sum() < 24
    assert result['replicates_required'] == 24 and len(result['replicate_differences']) == 24
    assert result['difference_status'] == 'nonfinite_or_nonpositive_replicate_variance_or_statistic'
    assert result['ratio_status'] == 'undefined_replicate_denominator_variance_or_statistic'
    np.testing.assert_array_equal(np.isnan(result['difference_pivots']), invalid)
    np.testing.assert_array_equal(np.isnan(result['ratio_pivots']), invalid)
    expected_difference = 2.*(indices == 0).mean(axis=1)
    np.testing.assert_allclose(result['replicate_differences'], expected_difference)
    np.testing.assert_allclose(result['replicate_ratios'], 1.+expected_difference/3.)
    assert result['difference_p_value'] == 1.
    assert np.isnan(result['difference_ci95']).all() and np.isnan(result['ratio_ci95']).all()
