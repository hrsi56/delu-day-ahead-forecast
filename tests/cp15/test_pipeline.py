from __future__ import annotations
import copy,json
from datetime import date,timedelta
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
from cp15.data import RAW_COLUMNS,prepare,history_start,origin_utc,day_hours,LEVELS
from cp15.models import fit_day
from cp15.residuals import ResidualBuffer,BUFFER_POLICIES
from delu_forecast.schema import BENCHMARK_ADDITIONS,SAME_DAY_ACTUAL_COLUMNS

ROOT=Path(__file__).resolve().parents[2]


def synthetic(start=date(2019,1,1),end=date(2019,5,10)):
    idx=pd.date_range(pd.Timestamp(start,tz='Europe/Berlin'),pd.Timestamp(end,tz='Europe/Berlin'),freq='h',inclusive='left').tz_convert('UTC')
    rng=np.random.default_rng(15042);t=np.arange(len(idx));local=idx.tz_convert('Europe/Berlin')
    price=30+8*np.sin(t/100)+4*np.cos(local.hour/24*2*np.pi)+rng.normal(0,2,len(idx))
    return pd.DataFrame({'timestamp_utc':idx,'delivery_date':local.date,'price_eur_mwh':price,'load_forecast_mw':50000+1000*np.sin(t/100)})


@pytest.fixture(scope='module')
def raw():return synthetic()


@pytest.fixture(scope='module')
def p():
    result=json.loads((ROOT/'reports/cp15/protocol.json').read_text())
    # Smaller synthetic fixture history only; real representative reproduction
    # uses the unchanged committed production protocol and full hyperparameters.
    result['history']['minimum_lear_rows_per_hour_long']=40
    result['history']['minimum_lgbm_training_rows']=100
    result['lgbm']['parameters']['n_estimators']=10
    return result


def test_corrected_history_and_origin_timezone():
    assert history_start(date(2020,7,1),'B2')==date(2019,1,1)
    assert history_start(date(2022,7,1),'A1')==date(2020,7,3)
    assert history_start(date(2020,7,1),'A4')==date(2020,4,8)
    with pytest.raises(ValueError,match='pre-2019'):history_start(date(2019,2,1),'A4')
    for d in (date(2020,1,1),date(2020,7,1)):
        assert origin_utc(d).tz_convert('UTC').hour==11
        assert origin_utc(d).date()==d-timedelta(days=1)


def test_market_boundary_refuses_synthetic_pre2019_row(raw,p):
    assert prepare(raw,p).frame.delivery_date.min()==date(2019,1,1)
    changed=raw.copy()
    changed.loc[0,'delivery_date']=date(2018,12,31)
    changed.loc[0,'timestamp_utc']=pd.Timestamp('2018-12-31',tz='Europe/Berlin').tz_convert('UTC')
    with pytest.raises(ValueError,match='pre-2019 input refused'):
        prepare(changed,p)


def test_exact_row_origin_normalization_and_unit_map(raw,p):
    data=prepare(raw,p)
    for d in (date(2019,3,31),date(2019,4,20)):
        rows=data.rows(d,eligible=False);boundary=day_hours(d)[0]
        ix=pd.date_range(end=boundary-pd.Timedelta(hours=1),periods=168,freq='h')
        y=raw.set_index('timestamp_utc').price_eur_mwh.reindex(ix).to_numpy()
        np.testing.assert_array_equal(data.level[rows],np.full(len(rows),y.mean()))
        np.testing.assert_array_equal(data.scale[rows],np.full(len(rows),max(y.std(ddof=1),1)))
        for name in p['normalization']['lgbm_center_and_scale']:
            j=p['lgbm']['features'].index(name)
            np.testing.assert_allclose(data.lgbm_normalized[rows,j],(data.lgbm_raw[rows,j]-data.level[rows])/data.scale[rows],equal_nan=True)
        for name in p['normalization']['lgbm_scale_only']:
            j=p['lgbm']['features'].index(name)
            np.testing.assert_allclose(data.lgbm_normalized[rows,j],data.lgbm_raw[rows,j]/data.scale[rows],equal_nan=True)
        np.testing.assert_allclose(data.lear_normalized[rows,:96],(data.lear_raw[rows,:96]-data.level[rows,None])/data.scale[rows,None],equal_nan=True)
    assert data.level[data.rows(date(2019,4,20))[0]]!=data.level[data.rows(date(2019,4,21))[0]]
    flat=raw.copy();flat.price_eur_mwh=42
    constant=prepare(flat,p);assert np.all(constant.scale[constant.feature_valid]==1)


@pytest.mark.parametrize('column',list(BENCHMARK_ADDITIONS)+list(SAME_DAY_ACTUAL_COLUMNS)+['target_day_actual_price'])
def test_schema_refusal_has_positive_control(raw,p,column):
    assert prepare(raw,p).frame.columns.tolist()==RAW_COLUMNS
    with pytest.raises(ValueError,match='schema'):prepare(raw.assign(**{column:1}),p)


def test_lear_cross_hour_vectors_and_no_crisis_features(raw,p):
    data=prepare(raw,p);d=date(2019,4,10);rows=data.rows(d)
    previous=raw.loc[raw.delivery_date.eq(d-timedelta(days=3))].price_eur_mwh.to_numpy()
    np.testing.assert_array_equal(data.lear_raw[rows[0],48:72],previous)
    assert data.lear_raw.shape[1]==175
    assert not any('crisis' in c for c in p['lgbm']['features']+p['lear']['features'])
    # Repeated local hour uses both already available canonical observations.
    fall=synthetic(date(2019,9,1),date(2019,11,5));fd=prepare(fall,p)
    values=fall.loc[(fall.delivery_date==date(2019,10,27))&(fall.timestamp_utc.dt.tz_convert('Europe/Berlin').dt.hour==2),'price_eur_mwh']
    assert len(values)==2
    assert fd.lear_raw[fd.rows(date(2019,10,28),eligible=False)[0],2]==values.mean()


@pytest.mark.parametrize('policy',['A4','B3','A2'])
def test_fit_delivery_mask_positive_d1_and_rolling_refit(raw,p,policy):
    d=date(2019,5,7);base=prepare(raw,p);rows=base.rows(d)
    forecast,logs=fit_day(base,d,policy,rows=rows)
    masked=raw.copy();masked.loc[masked.delivery_date>=d,'price_eur_mwh']=np.nan
    masked.loc[masked.delivery_date>d,'load_forecast_mw']=1e8
    control,_=fit_day(prepare(masked,p),d,policy,rows=rows)
    np.testing.assert_array_equal(control,forecast)
    changed=raw.copy();changed.loc[changed.delivery_date.eq(d-timedelta(days=1)),'price_eur_mwh']+=500
    moved,_=fit_day(prepare(changed,p),d,policy,rows=rows)
    assert np.max(np.abs(moved-forecast))>0
    _,next_logs=fit_day(base,d+timedelta(days=1),policy)
    assert logs[0]['train_rows_sha256']!=next_logs[0]['train_rows_sha256']
    assert all(x['latest_training_delivery_date']<str(d) for x in logs)
    if policy=='A4':
        assert all(x['inner_train_end']<x['validation_start']<=x['validation_end']<str(d) for x in logs)
        assert all(x['fit_calls']==5 for x in logs)


def issue(buf,d,center=10.,scale=2.,partial=False):
    ix=day_hours(d)
    if partial:ix=ix[:-1]
    buf.issue(d,ix,{p:np.full(len(ix),center) for p in BUFFER_POLICIES},np.full(len(ix),scale))


@pytest.mark.parametrize('d,n',[(date(2020,3,29),23),(date(2020,10,25),25),(date(2020,7,1),24)])
def test_delayed_complete_feedback_and_once_with_positive_controls(d,n):
    b=ResidualBuffer();issue(b,d)
    assert len(day_hours(d))==n
    seen=[]
    def truth(ix):seen.extend(ix);return np.full(len(ix),14.)
    b.release(d+timedelta(days=1),truth);assert not seen and not b.buffers['A1']
    b.release(d+timedelta(days=2),truth);assert len(seen)==n
    np.testing.assert_array_equal(b.buffers['A1'][0][1],np.full(n,2))
    np.testing.assert_array_equal(b.buffers['B0'][0][1],np.full(n,4))
    before=len(b.trace);b.release(d+timedelta(days=3),truth)
    assert len(seen)==n and len(b.trace)==before
    with pytest.raises(ValueError,match='already'):issue(b,d)
    incomplete=ResidualBuffer();issue(incomplete,d,partial=True)
    incomplete.release(d+timedelta(days=2),truth);assert not incomplete.buffers['A1']
    late=ResidualBuffer();issue(late,d)
    late.release(d+timedelta(days=2),lambda ix:np.full(len(ix),np.nan));assert not late.buffers['A1']
    late.release(d+timedelta(days=3),truth);assert len(late.buffers['A1'])==1


def test_quantile_exact_ties_and_current_scale_and_issued_scale():
    q=np.quantile([0,10,20,30],LEVELS,method='linear')
    np.testing.assert_allclose(q,[.75,3,7.5,15,22.5,27,29.25],atol=1e-14)
    np.testing.assert_array_equal(np.quantile([2,2,2,2],LEVELS,method='linear'),np.full(7,2))
    b=ResidualBuffer();start=date(2020,1,1)
    for offset in range(29):issue(b,start+timedelta(days=offset))
    origin=start+timedelta(days=29)
    b.release(origin,lambda ix:np.full(len(ix),14.))
    assert len(b.buffers['A1'])==28
    pred,stats=b.predict('A1',np.array([100.]),np.array([3.]))
    np.testing.assert_array_equal(pred,np.full((1,7),106.))
    assert stats['buffer_end']==str(origin-timedelta(days=2))
    # Distinguish current scale from the immutable scale at error issuance.
    changed,_=b.predict('A1',np.array([100.]),np.array([6.]))
    np.testing.assert_array_equal(changed,np.full((1,7),112.))
    b.release(origin+timedelta(days=1),lambda ix:np.full(len(ix),14.))
    assert len(b.buffers['A1'])==28 and b.buffers['A1'][0][0]==start+timedelta(days=1)
    with pytest.raises(ValueError,match='28 complete'):ResidualBuffer().predict('B0',np.array([1.]),np.array([1.]))


def test_fixed_tolerance_solver_continuation_and_exhaustion():
    import warnings
    from sklearn.exceptions import ConvergenceWarning
    from cp15.models import _lasso
    class Solver:
        def __init__(self,always=False):self.calls=0;self.always=always;self.n_iter_=20000;self.dual_gap_=1.;self.seen=[]
        def fit(self,x,y):
            self.calls+=1;self.seen.append((self.alpha,id(x),id(y)))
            if self.always or self.calls==1:warnings.warn('fixture did not converge',ConvergenceWarning)
            return self
    x=np.ones((5,2));y=np.arange(5.);settings={'max_iter':20000,'tol':.0001,'selection':'cyclic'}
    solver=Solver();model=_lasso(x,y,.1,settings,solver)
    assert model is solver and model.solver_passes_==2 and model.total_n_iter_==40000
    assert model.seen==[(.1,id(x),id(y))]*2
    failed=Solver(always=True)
    with pytest.raises(RuntimeError,match='10 fixed-budget'):_lasso(x,y,.1,settings,failed)
    assert failed.calls==10


def test_late_truth_cannot_displace_newer_complete_days():
    b=ResidualBuffer();start=date(2020,1,1)
    for offset in range(31):issue(b,start+timedelta(days=offset))
    def late(ix):
        return np.full(len(ix),np.nan if ix[0]==day_hours(start)[0] else 14.)
    b.release(start+timedelta(days=32),late)
    before=[d for d,_ in b.buffers['A1']]
    assert before==[start+timedelta(days=x) for x in range(3,31)]
    b.release(start+timedelta(days=33),lambda ix:np.full(len(ix),18.))
    assert [d for d,_ in b.buffers['A1']]==before
    # Positive: an earlier recovered day still inside the latest 28 is sorted
    # into its date position and supplies the missing buffer day.
    c=ResidualBuffer()
    for offset in range(28):issue(c,start+timedelta(days=offset))
    c.release(start+timedelta(days=30),late);assert len(c.buffers['A1'])==27
    c.release(start+timedelta(days=31),lambda ix:np.full(len(ix),18.))
    assert len(c.buffers['A1'])==28 and c.buffers['A1'][0][0]==start


def test_feedback_origin_cannot_rewind_but_same_and_next_are_valid():
    b=ResidualBuffer();d=date(2020,1,1);issue(b,d)
    read=lambda ix:np.full(len(ix),14.)
    b.release(d+timedelta(days=2),read)
    b.release(d+timedelta(days=2),read)
    assert len(b.buffers['A1'])==1
    with pytest.raises(ValueError,match='backwards'):b.release(d+timedelta(days=1),read)
    b.release(d+timedelta(days=3),read);assert len(b.buffers['A1'])==1
