"""O33's running intervals (`cp18.running`): the frozen estimator, the minimum, the wording, the live window only."""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pytest

from cp17.tools import fresh_test as F
from cp18 import running as R
from cp28 import inference as I


def _dates(first: date, n: int, gaps=()) -> list[date]:
    out, d = [], first
    while len(out) < n:
        if d not in gaps:
            out.append(d)
        d += timedelta(days=1)
    return out


@pytest.mark.parametrize('first,n,gaps', [(date(2026, 6, 1), 30, ()),
                                          (date(2025, 12, 20), 26, (date(2025, 12, 28), date(2026, 1, 3)))])
def test_bit_identical_to_cp28s_test_endpoint_on_development_dates(first, n, gaps):
    dates = _dates(first, n, gaps)
    d = np.random.default_rng(5).normal(0.3, 2.0, size=n)
    ours = R.studentized(d, dates, replicates=2000)
    theirs = I.test_endpoint(d, dates, block_days=F.BLOCK_DAYS, stratified=True, rng=np.random.default_rng(F.SEED),
                             required_cell=False, replicates=2000)
    assert R.calendar_runs(dates) == I.calendar_runs(dates)
    assert ours['mean'] == theirs['mean'] and ours['variance'] == theirs['variance']
    assert np.array_equal(ours['stats'], theirs['replicate_statistics'])


def test_it_admits_live_dates_which_cp28s_own_entry_refuses():
    dates = _dates(date(2026, 11, 6), 20)
    d = np.random.default_rng(1).normal(size=20)
    with pytest.raises(ValueError):
        I.calendar_runs(dates)                       # cp25.guard refuses a day after 2026-09-06
    point = R.interval(d, dates, replicates=500)
    assert point['lower'] < point['mean'] < point['upper']


def test_the_interval_appears_from_14_scored_days_with_its_wording():
    assert R.MINIMUM_DAYS == 14 == 2 * F.BLOCK_DAYS and F.BLOCK_DAYS == 7
    dates = _dates(date(2026, 11, 6), 14)
    d = np.random.default_rng(2).normal(10, 3, size=14)
    before = R.interval(d[:13], dates[:13], replicates=200)
    assert before['lower'] is None and before['interval'] == 'interval from 14 scored days'
    at = R.interval(d, dates, replicates=200)
    assert at['interval'] == '95% interval of the mean daily error over 14 scored days' and at['lower'] is not None
    text = ' '.join([R.WORDING, R.BEFORE_MINIMUM, R.LABEL]).lower()
    assert 'confidence' not in text and '%' not in text.replace('95%', '') and '4.7t' not in text


def _window(policy, days, window='prospective'):
    return {'window': window, 'policy': policy, 'evidence_class': 'x',
            'record': {'days': [{'day': str(d), 'mae_eur': m, 'wis_eur': w} for d, m, w in days]}}


def test_the_series_use_the_prospective_window_only_and_pair_against_b0():
    days = _dates(date(2026, 11, 6), 16)
    product = [(d, 10.0 + i, 5.0 + i) for i, d in enumerate(days)]
    naive = [(d, 12.0 + i, 6.0 + i) for i, d in enumerate(days) if i != 3]
    dev = [(date(2026, 8, 1) + timedelta(days=i), 999.0, 999.0) for i in range(20)]
    out = R.running([_window('product', product), _window('B0', naive), _window('product', dev, 'development'),
                     _window('product', dev, '4.7T')], replicates=200)
    assert out['label'] == 'prospective evaluation in progress'
    assert [p['n'] for p in out['series']['mae']] == list(range(1, 17))
    assert out['series']['mae'][-1]['mean'] == np.mean([m for _, m, _ in product])
    assert len(out['series']['mae_vs_B0']) == 15 and out['series']['mae_vs_B0'][-1]['mean'] == -2.0
    assert all(p['mean'] < 999 for s in out['series'].values() for p in s)
    assert out['series']['mae'][12]['lower'] is None and out['series']['mae'][13]['lower'] is not None
