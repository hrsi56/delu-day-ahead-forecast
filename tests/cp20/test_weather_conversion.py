"""Frozen section 15.2/15.3 conversion fixtures: each negative assertion has a positive control."""
from datetime import date

import numpy as np
import pandas as pd
import pytest

from cp20 import weather as wx

SHAPE = (5, 10, 34, 41)
NORMAL_BOUNDS = [(l - 3, l) if l % 6 == 3 else (l - 6, l) for l in wx.LEADS]


def base(value=0.0):
    return np.full(SHAPE, value, dtype=float)


def with_leads(field, fn, data=None):
    data = base() if data is None else data
    for k, lead in enumerate(wx.LEADS):
        data[wx.FIELDS.index(field), k] = fn(lead)
    return data


def test_wind_is_linearly_interpolated_per_component_with_exact_endpoints():
    data = with_leads('u10', lambda l: float(l))
    assert np.allclose(wx.interpolate_wind(data[0], data[1], 24), 24.0)          # endpoint, no interpolation
    assert np.allclose(wx.interpolate_wind(data[0], data[1], 22), 22.0)          # 1/3 between 21 and 24
    assert np.allclose(wx.interpolate_wind(data[0], data[1], 46), 46.0)          # 1/3 between 45 and 48
    with pytest.raises(wx.ConversionRefused):
        wx.interpolate_wind(data[0], data[1], 20)                               # no extrapolation


def test_speed_is_per_cell_before_spatial_mean_not_magnitude_of_mean_wind():
    data = base()
    data[0, :, :, :20] = 5.0
    data[0, :, :, 20:] = -5.0
    frame = wx.convert_run(date(2022, 8, 26), data, NORMAL_BOUNDS, [0.01] * 10)
    assert np.allclose(frame.wx_wind10_mean, 5.0)       # per-cell speed averaged
    mean_u = float((wx.weights() * data[0, 1]).sum())
    assert abs(mean_u) < 5.0                            # magnitude-of-mean would differ


def test_cosine_latitude_weights_are_normalised_over_the_fixed_grid():
    w = wx.weights()
    assert w.shape == (34, 41) and np.isclose(w.sum(), 1.0)
    assert np.allclose(w[:, 0] / w[0, 0], np.cos(np.deg2rad(wx.BOX_LATS)) / np.cos(np.deg2rad(55.25)))
    field = np.repeat(wx.BOX_LATS[:, None], 41, axis=1)
    assert (w * field).sum() < field.mean()             # north cells down-weighted


def test_radiation_deaveraging_uses_six_hour_reset_formula():
    # A(18,21)=100, A(18,24)=150 -> block(21,24] = 2*150-100 = 200; A(24,27)=300 used directly.
    means = {21: 100.0, 24: 150.0, 27: 300.0, 30: 250.0, 33: 80.0, 36: 40.0, 39: 0.0, 42: 0.0, 45: 10.0, 48: 20.0}
    data = with_leads('dswrf', lambda l: means[l])
    a = data[wx.FIELDS.index('dswrf')]
    b, log = wx.radiation_block(a, NORMAL_BOUNDS, [10.0] * 10, 24)
    assert np.allclose(b, 200.0) and log['clipped_cells'] == 0
    b, _ = wx.radiation_block(a, NORMAL_BOUNDS, [10.0] * 10, 27)
    assert np.allclose(b, 300.0)
    frame = wx.convert_run(date(2022, 8, 26), data, NORMAL_BOUNDS, [10.0] * 10)
    # 2022-08-26 (CEST) hours start at lead 22: h22,h23 -> block 21-24; h24..h26 -> block 24-27.
    assert list(frame.lead_hour[:5]) == [22, 23, 24, 25, 26]
    assert np.allclose(frame.wx_dswrf_mean[:5], [200.0, 200.0, 300.0, 300.0, 300.0])


def test_wrong_averaging_bounds_are_refused_not_inferred_from_lead_number():
    data = with_leads('dswrf', lambda l: 50.0)
    wrong = list(NORMAL_BOUNDS)
    wrong[1] = (21, 24)
    with pytest.raises(wx.ConversionRefused):
        wx.radiation_block(data[4], wrong, [1.0] * 10, 24)
    wx.radiation_block(data[4], NORMAL_BOUNDS, [1.0] * 10, 24)  # positive control


def test_negative_blocks_within_three_quanta_are_clipped_and_logged_beyond_are_invalid():
    q = 10.0
    data = with_leads('dswrf', lambda l: 0.0)
    a = data[4]
    a[1, 0, 0] = -1.0 * q / 2        # 2A(18,24)-A(18,21) = -q at one cell: allowed, clipped
    b, log = wx.radiation_block(a, NORMAL_BOUNDS, [q] * 10, 24)
    assert b[0, 0] == 0.0 and log['clipped_cells'] == 1 and log['min_block'] == -q
    a[1, 0, 0] = -2.0 * q            # block -4q: conversion failure, no tolerance
    b, log = wx.radiation_block(a, NORMAL_BOUNDS, [q] * 10, 24)
    assert b is None and log['failure'] == 'negative_block_below_minus_3q'
    frame = wx.convert_run(date(2022, 8, 26), data, NORMAL_BOUNDS, [q] * 10)
    bad = frame.lead_hour.isin([22, 23])
    assert frame.loc[bad, list(wx.COLUMNS)].isna().all().all() and (frame.loc[bad, 'status'] == 'invalid_support').all()
    assert frame.loc[~bad, list(wx.COLUMNS)].notna().all().all()


def test_quantum_is_max_of_contributing_messages_and_unknown_quantum_fails():
    data = with_leads('dswrf', lambda l: 0.0)
    data[4, 1, 0, 0] = -0.75        # block -1.5 at f024: allowed only if q >= 0.5
    b, log = wx.radiation_block(data[4], NORMAL_BOUNDS, [0.5 if l == 21 else 0.01 for l in wx.LEADS], 24)
    assert b is not None and log['quantum'] == 0.5
    b, log = wx.radiation_block(data[4], NORMAL_BOUNDS, [0.01] * 10, 24)
    assert b is None
    b, log = wx.radiation_block(data[4], NORMAL_BOUNDS, [None] * 10, 24)
    assert b is None and log['failure'] == 'unknown_quantum'


def test_any_nonfinite_required_cell_makes_all_three_columns_missing_without_renormalisation():
    data = base(1.0)
    frame = wx.convert_run(date(2022, 8, 26), data, NORMAL_BOUNDS, [0.01] * 10)
    assert frame[list(wx.COLUMNS)].notna().all().all()
    data[2, 0, 5, 5] = np.nan          # u100 at f021 only: hours bracketed by f021 lose support
    frame = wx.convert_run(date(2022, 8, 26), data, NORMAL_BOUNDS, [0.01] * 10)
    hit = frame.lead_hour < 24
    assert frame.loc[hit, list(wx.COLUMNS)].isna().all().all()
    assert frame.loc[~hit, list(wx.COLUMNS)].notna().all().all()


@pytest.mark.parametrize('day,n,first,last', [(date(2019, 3, 31), 23, 23, 45), (date(2019, 10, 27), 25, 22, 46),
                                              (date(2019, 1, 2), 24, 23, 46), (date(2022, 8, 26), 24, 22, 45)])
def test_canonical_hour_leads_cover_dst_days(day, n, first, last):
    leads = wx.hour_leads(day)
    assert len(leads) == n and leads[0] == first and leads[-1] == last


def fall_back_features(missing_second=False):
    day = date(2019, 10, 27)
    frame = wx.convert_run(day, with_leads('u10', lambda l: float(l)), NORMAL_BOUNDS, [0.01] * 10)
    frame['timestamp_utc'] = pd.to_datetime(frame.timestamp_utc, utc=True)
    frame['local_hour'] = frame.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour
    if missing_second:
        second = frame.index[frame.local_hour.eq(2)][1]
        frame.loc[second, list(wx.COLUMNS)] = np.nan
    return frame


def test_repeated_autumn_hour_averages_both_canonical_vectors_and_requires_both():
    frame = fall_back_features()
    design = wx.local_hour_design(frame)
    two = frame.loc[frame.local_hour.eq(2), 'wx_wind10_mean']
    assert len(two) == 2 and design.loc[(date(2019, 10, 27), 2), 'n_canonical'] == 2
    assert np.isclose(design.loc[(date(2019, 10, 27), 2), 'wx_wind10_mean'], two.mean())
    design = wx.local_hour_design(fall_back_features(missing_second=True))
    assert design.loc[(date(2019, 10, 27), 2), list(wx.COLUMNS)].isna().all()
    assert design.loc[(date(2019, 10, 27), 3), list(wx.COLUMNS)].notna().all()


def test_spring_gap_stays_absent():
    day = date(2019, 3, 31)
    frame = wx.convert_run(day, base(1.0), NORMAL_BOUNDS, [0.01] * 10)
    frame['timestamp_utc'] = pd.to_datetime(frame.timestamp_utc, utc=True)
    frame['local_hour'] = frame.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour
    design = wx.local_hour_design(frame)
    assert (day, 2) not in design.index and len(design) == 23


def test_only_confirmed_missing_classes_are_imputable_and_unfinished_extraction_refuses(tmp_path):
    frame = wx.missing_day(date(2019, 1, 1), 'structural_missing_pre_2019_run', 'pre-2019 run')
    assert frame[list(wx.COLUMNS)].isna().all().all() and len(frame) == 24
    with pytest.raises(wx.ConversionRefused):
        wx.missing_day(date(2020, 1, 1), 'extraction_failed_after_bounded_attempts', 'network')
    with pytest.raises(wx.ConversionRefused):
        wx.missing_day(date(2020, 1, 1), 'budget_exhausted', 'cap')
    manifest = {'structural_missing': [], 'runs': [{'run_00z': '2020-01-01', 'delivery_day': '2020-01-02', 'version': 'v15.1'}]}
    (tmp_path / 'runs').mkdir()
    with pytest.raises(wx.ConversionRefused, match='unfinished'):
        wx.build_features(manifest, tmp_path)


def test_design_matrix_refuses_rows_without_a_frozen_weather_record():
    frame = fall_back_features()
    design = wx.WeatherDesign.from_features(frame)
    dates = np.array(['2019-10-27', '2019-10-28'], dtype='datetime64[D]')
    hours = np.array([5, 5])
    out = design.matrix(dates, hours, np.array([True, False]))
    assert np.isfinite(out[0]).all() and np.isnan(out[1]).all()
    with pytest.raises(wx.ConversionRefused):
        design.matrix(dates, hours, np.array([True, True]))
