"""DST fixtures for DDNN-2's day-level representation (capstone v21-r11 §23.10): the inputs, the loss mask and
the emitted keys on every real transition day from 2019-03-31 to 2026-03-29 (2022-10-30 has no frozen
weather record, so its fixture covers prices, load, the loss mask and the keys), and a synthetic calendar
fixture for 2026-10-25."""
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from cp24 import design as G
from cp24.inputs import load, weather_design
from cp24.member import Keys, emit_rows

ROOT = Path(__file__).resolve().parents[2]


def transitions():
    out = []
    for year in range(2019, 2027):
        for month in (3, 10):
            d = date(year, month, 31)
            d -= timedelta(days=(d.weekday() + 1) % 7)   # the last Sunday
            if date(2019, 3, 31) <= d <= date(2026, 3, 29):
                out.append(d)
    return out


@pytest.fixture(scope='module')
def table():
    data = load(ROOT)
    dd = G.build(data, weather_design(ROOT))
    return data, dd, Keys.from_data(data, dd)


def test_every_real_transition_day_in_range():
    days = transitions()
    assert days[0] == date(2019, 3, 31) and days[-1] == date(2026, 3, 29) and len(days) == 15
    assert date(2022, 10, 30) in days


@pytest.mark.parametrize('day', transitions(), ids=str)
def test_inputs_mask_and_keys_on_a_transition_day(table, day):
    data, dd, keys = table
    i = dd.ix(day)
    ix = np.flatnonzero(data.dates == np.datetime64(day))
    hours = data.hours[ix]
    spring = day.month == 3
    assert len(ix) == (23 if spring else 25)
    # Inputs: the local-hour curves follow the LEAR convention (src/cp15/data.py).
    for h in range(24):
        sel = ix[hours == h]
        if spring and h == 2:
            assert not len(sel) and np.isnan(dd.price[i, h]) and np.isnan(dd.load[i, h])
        else:
            assert np.isclose(dd.price[i, h], data.frame.price_eur_mwh.to_numpy()[sel].mean(), rtol=0, atol=1e-12)
            assert np.isclose(dd.load[i, h], data.frame.load_forecast_mw.to_numpy()[sel].mean(), rtol=0, atol=1e-9)
    if not spring:
        assert (hours == 2).sum() == 2
    # The next day's D-1 inputs are this day's curves.
    nxt = np.array([i + 1])
    C, _, names, _ = G.raw_inputs(dd, nxt, (), 'z-s4')
    d1 = C[0, :24] * dd.scale['s4'][i + 1] + dd.centre['s4'][i + 1]
    assert np.allclose(d1, dd.price[i], equal_nan=True, rtol=0, atol=1e-9)
    # The loss mask: the missing spring slot is masked; the repeated autumn slot is the mean of both observations.
    elig = ix[data.eligible[ix]]
    if spring:
        assert not dd.mask[i, 2]
    else:
        two = elig[data.hours[elig] == 2]
        if len(two) == 2:
            assert dd.mask[i, 2] and np.isclose(dd.y[i, 2], data.y[two].mean(), rtol=0, atol=1e-12)
    # The keys: exactly the day's feature-valid canonical hours; both repeated-hour keys take slot 2.
    rows = keys.of_days(np.array([i]))
    assert np.array_equal(keys.timestamp[rows], data.index[data.rows(day)])
    slots = np.zeros((1, 24, 7))
    slots[0] = np.arange(24)[:, None] + np.zeros(7)
    q = emit_rows(keys, rows, np.array([i]), slots)
    assert np.array_equal(q[:, 0], keys.slot[rows]) and np.array_equal(q[:, 0], data.hours[data.rows(day)])
    # Weather: present for every canonical hour, except on the uncovered 2022-10-30.
    if day == date(2022, 10, 30):
        assert not dd.covered[i] and np.isnan(dd.weather[i]).all()
    else:
        assert dd.covered[i]


def test_synthetic_calendar_fixture_2026_10_25():
    """The autumn transition beyond the data boundary, on synthetic hourly values."""
    days = pd.date_range('2026-10-24', '2026-10-26', freq='D').date
    idx = pd.date_range(pd.Timestamp('2026-10-24', tz='Europe/Berlin'), pd.Timestamp('2026-10-27', tz='Europe/Berlin'),
                        freq='h', inclusive='left').tz_convert('UTC')
    local = idx.tz_convert('Europe/Berlin')
    dates = np.array(local.date, dtype='datetime64[D]')
    hours = local.hour.to_numpy()
    values = np.arange(len(idx), dtype=float)
    assert (dates == np.datetime64('2026-10-25')).sum() == 25
    table = G._local_hour_table(dates, hours, values, np.array(days, dtype='datetime64[D]'))
    rep = values[(dates == np.datetime64('2026-10-25')) & (hours == 2)]
    assert len(rep) == 2 and table[1, 2] == rep.mean()
    assert np.isfinite(table).all()
