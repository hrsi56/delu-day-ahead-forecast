"""Exact calibration oracles and discriminating CP-10 controls, before data runs."""
from datetime import date, timedelta
from fractions import Fraction

import numpy as np
import pandas as pd
import pytest

from delu_forecast.calibration_comparison import (
    CANDIDATES, GAMMA_GRID, SELECTION_FOLDS, aci_predict, falsification,
    fit_scaled, fully_observed_days, head_spread, predict_scaled, price_volatility,
    select_candidate,
)
from delu_forecast.conformal import PAIR_ALPHAS, UndersizedCalibrationSet
from delu_forecast.metrics import crossing_violations
from delu_forecast.postprocess import apply_cqr_thresholds, isotonic_last


def scaled_fixture():
    # Normalised scores are j-11, despite variable EUR scales. Hand-derived
    # ranks {20,19,17,11} therefore give {8,7,5,-1} in normalised units.
    scale = np.arange(1., 21.)
    raw = np.tile([100,100,100,100,120,140,140,140,140], (20,1)) * scale[:,None]
    truth = (111 - np.arange(20)) * scale
    return raw, truth, scale


@pytest.mark.parametrize('estimator', ['spread', 'volatility'])
def test_scaled_exact_rank_and_multiply_back(estimator):
    raw, y, scale = scaled_fixture()
    if estimator == 'spread':
        scale = head_spread(raw)  # 40 * original scale
        expected = np.array([.2,.175,.125,-.025])
    else:
        expected = np.array([8,7,5,-1])
    thresholds = fit_scaled(raw, y, scale)
    np.testing.assert_array_equal(list(thresholds.values()), expected)
    output = predict_scaled(np.array([[100,100,100,100,120,140,140,140,140.]]), thresholds,
                            np.array([80. if estimator == 'spread' else 2.]))
    np.testing.assert_array_equal(output, [[84,86,90,102,120,138,150,154,156]])
    # A missing division or missing prediction-time multiplication fails this fixture.
    wrong = predict_scaled(np.array([[100,100,100,100,120,140,140,140,140.]]),
                           fit_scaled(raw, y, np.ones(20)), np.array([1.]))
    assert np.max(np.abs(output-wrong)) > 0


def test_spread_is_raw_and_floor_is_explicit():
    raw = np.array([[0,9,2,3,4,5,6,1,8.], [0,1,2,3,4,5,6,9,10.]])
    np.testing.assert_array_equal(head_spread(raw), [1,8])
    assert head_spread(np.sort(raw, axis=1))[0] != head_spread(raw)[0]
    raw[0,7] = 19
    assert head_spread(raw)[0] == 10  # positive control on the floor


def test_volatility_exact_window_mask_and_positive_control():
    day = date(2025,2,1)
    boundary = pd.Timestamp(day, tz='Europe/Berlin').tz_convert('UTC')
    idx = pd.date_range(end=boundary+pd.Timedelta(hours=23), periods=192, freq='h')
    price = pd.Series(np.arange(192.), index=idx)
    # sample variance of consecutive integers 0..167 is 168*169/12.
    expected = np.sqrt(168*169/12)
    np.testing.assert_array_equal(price_volatility(price, pd.Index([day]*24)), np.repeat(expected,24))
    masked = price.copy(); masked.loc[masked.index >= boundary] = np.nan
    np.testing.assert_array_equal(price_volatility(price, pd.Index([day])), price_volatility(masked,pd.Index([day])))
    positive = price.copy(); positive.loc[boundary-pd.Timedelta(hours=1)] += 10000
    assert price_volatility(positive,pd.Index([day]))[0] > expected
    broken = price.drop(boundary-pd.Timedelta(hours=1))
    with pytest.raises(ValueError, match='incomplete'):
        price_volatility(broken,pd.Index([day]))
    assert np.isfinite(price_volatility(price,pd.Index([day]))).all()


@pytest.mark.parametrize('day, hours', [(date(2025,3,30),23),(date(2025,10,26),25)])
def test_feedback_completeness_counts_dst_hours(day,hours):
    idx = pd.date_range(pd.Timestamp(day,tz='Europe/Berlin'),pd.Timestamp(day+timedelta(days=1),tz='Europe/Berlin'),freq='h',inclusive='left').tz_convert('UTC')
    assert len(idx) == hours
    series = pd.Series(1.,index=idx)
    assert fully_observed_days(series) == {day}
    assert fully_observed_days(series.iloc[:-1]) == set()


def aci_fixture(n_days=5):
    # Large exact score grid makes even the smallest frozen gamma observable.
    cal_raw = np.zeros((100000,9)); cal_y = np.arange(100000.)
    days = pd.Index([date(2025,1,1)+timedelta(days=i) for i in range(n_days)])
    raw = np.zeros((n_days,9)); truth = np.full(n_days, 1e6)
    return cal_raw,cal_y,raw,days,truth


@pytest.mark.parametrize('gamma', GAMMA_GRID)
def test_aci_exact_fixture_every_frozen_gamma(gamma):
    cal,cy,raw,days,y = aci_fixture(3)
    out, trace = aci_predict(cal,cy,raw,days,y,gamma=gamma,observed_days=set(days))
    np.testing.assert_array_equal(out[:2], np.tile([-95000,-90000,-80000,-50000,0,50000,80000,90000,95000],(2,1)))
    # One released miss from D-2: c95=.95+gamma*.95. All arithmetic below
    # uses rational constants and math.ceil, independently of production rank.
    import math
    levels = [Fraction(95,100),Fraction(9,10),Fraction(4,5),Fraction(1,2)]
    qs = [math.ceil(100001*(level + Fraction(gamma)*level))-1 for level in levels]
    np.testing.assert_array_equal(out[2], [-qs[0],-qs[1],-qs[2],-qs[3],0,qs[3],qs[2],qs[1],qs[0]])
    assert trace.n_feedback.tolist() == [0,0,1]
    assert trace.coverage_state_95.iloc[2] == float(levels[0]*(1+Fraction(gamma)))
    assert out[2,8] >= out[1,8]  # miss widens; a hit must move the state the other way
    hit_y = np.zeros(3)
    hit, hit_trace = aci_predict(cal,cy,raw,days,hit_y,gamma=gamma,observed_days=set(days))
    assert hit_trace.coverage_state_95.iloc[2] < trace.coverage_state_95.iloc[0]
    assert np.max(abs(hit[2]-out[2])) > 0


@pytest.mark.parametrize('gamma', GAMMA_GRID)
def test_aci_masks_d_and_d_minus_1_but_d_minus_2_moves_output(gamma):
    cal,cy,raw,days,y = aci_fixture()
    base,trace = aci_predict(cal,cy,raw,days,y,gamma=gamma,observed_days=set(days))
    # Target is last day. Unavailable future labels may be NaN, not merely
    # replaced by another finite value that happens to leave hit unchanged.
    masked = y.copy(); masked[-2:] = np.nan
    negative,_ = aci_predict(cal,cy,raw,days,masked,gamma=gamma,observed_days=set(days))
    assert np.max(np.abs(base[-1]-negative[-1])) == 0.0
    positive_y = y.copy(); positive_y[-3] = 0.
    positive,_ = aci_predict(cal,cy,raw,days,positive_y,gamma=gamma,observed_days=set(days))
    assert np.max(np.abs(base[-1]-positive[-1])) > 0.0
    # A deliberately D-1 leak (shift feedback labels one day) is detected.
    leak_y = np.roll(y,-1); leak_y[-3] = 0.
    leaked,_ = aci_predict(cal,cy,raw,days,leak_y,gamma=gamma,observed_days=set(days))
    assert np.max(np.abs(base[-1]-leaked[-1])) > 0
    assert trace.n_feedback.tolist() == [0,0,1,2,3]  # no duplicate replay


def test_aci_incomplete_day_is_not_feedback_and_positive_control():
    cal,cy,raw,days,y = aci_fixture(3)
    base,_ = aci_predict(cal,cy,raw,days,y,gamma='0.00002',observed_days=set(days))
    skip,trace = aci_predict(cal,cy,raw,days,y,gamma='0.00002',observed_days=set(days[1:]))
    np.testing.assert_array_equal(skip[0],skip[-1])
    assert trace.n_feedback.tolist() == [0,0,0]
    assert np.max(abs(base[-1]-skip[-1])) > 0


def test_aci_does_not_clip_out_of_range_ranks():
    cal,cy,raw,days,y = aci_fixture(3)
    with pytest.raises(UndersizedCalibrationSet):
        aci_predict(cal,cy,raw,days,y,gamma='0.1',observed_days=set(days))
    assert np.isfinite(aci_predict(cal,cy,raw,days,y,gamma='0.00002',observed_days=set(days))[0]).all()


def test_isotonic_is_last_and_crossing_detector_has_control():
    raw=np.array([[0,1,2,3,4,5,6,7,8.]])
    thresholds={pair:q for (pair,_),q in zip(PAIR_ALPHAS,[-10,20,-30,40])}
    shifted=apply_cqr_thresholds(raw,thresholds)
    assert crossing_violations(shifted)>0
    output=predict_scaled(raw,thresholds,np.ones(1))
    np.testing.assert_array_equal(output,isotonic_last(shifted))
    assert crossing_violations(output)==0
    assert crossing_violations(apply_cqr_thresholds(isotonic_last(raw),thresholds))>0


def selection_fixture():
    return pd.DataFrame([{'candidate':c,'fold':f,'n_obs':n,'mean_pinball':2.}
                         for c in CANDIDATES for f,n in zip(SELECTION_FOLDS,(1,2,3,20))])


def test_fold3_excluded_ties_fixed_and_selection_can_move():
    rows=selection_fixture()
    chosen,_=select_candidate(rows)
    assert chosen==CANDIDATES[0]
    diagnostic=pd.DataFrame([{'candidate':c,'fold':'fold_3','n_obs':10**10,'mean_pinball':-1e9 if c==CANDIDATES[-1] else 1e9} for c in CANDIDATES])
    assert select_candidate(pd.concat([rows,diagnostic]))[0]==chosen
    rows.loc[rows.candidate.eq(CANDIDATES[-1]),'mean_pinball']=1.
    assert select_candidate(rows)[0]==CANDIDATES[-1]


def test_selection_is_observation_weighted_and_requires_complete_grid():
    rows=selection_fixture()
    rows.loc[rows.candidate.eq(CANDIDATES[0]),'mean_pinball']=[0,0,0,3]
    chosen,scores=select_candidate(rows)
    assert scores[CANDIDATES[0]] == 60/26
    assert chosen==CANDIDATES[1]  # unweighted mean would wrongly choose C-1a
    assert rows.loc[rows.candidate.eq(CANDIDATES[0]),'mean_pinball'].mean()<2
    with pytest.raises(ValueError, match='incomplete'):
        select_candidate(rows.iloc[1:])
    assert select_candidate(rows)[0]==chosen


def test_rule5_reports_both_outcomes_and_exact_boundary():
    failed=falsification(np.nextafter(.394,0))
    assert failed['result']=='the fix did not work'
    assert failed['recommended_frozen_artifact']=='v1'
    assert falsification(.394)['fix_worked'] is True
    assert falsification(.8)['fix_worked'] is True
