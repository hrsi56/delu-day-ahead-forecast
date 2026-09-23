"""Synthetic controls for resumed admission, cache identity and partition projection."""
import copy
from datetime import date
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pandas as pd
import pytest
from cp15.data import day_hours, origin_utc, array_hash
from cp16.execution import component, component_digest
from cp16.residuals import SharedResidualState


def fixture():
    d=date(2020,7,1);ix=day_hours(d);rows=np.arange(len(ix));scale=np.ones(len(ix))
    data=SimpleNamespace(rows=lambda day:rows,index=ix,scale=scale)
    cache=SimpleNamespace(fold='fold_1',get=lambda day:None)
    entry={'day':str(d),'fold':'fold_1','origin_utc':str(origin_utc(d).tz_convert('UTC')),
           'timestamp_utc':list(map(str,ix)),'input_fingerprint':'fixed-input','protocol_sha256':'fixed-protocol',
           'scale_sha256':array_hash(scale),'central':{'A1':scale.tolist(),'B2':(scale+2).tolist()},'fits':{'A1':[],'B2':[]}}
    entry['content_sha256']=component_digest(entry)
    lineage={'input_fingerprint':'fixed-input','protocol_sha256':'fixed-protocol','new_components':{'fold_1:'+str(d):entry}}
    return d,data,cache,lineage


@pytest.mark.parametrize('field',['central','fits','day','fold','origin_utc','protocol_sha256','input_fingerprint','scale_sha256','timestamp_utc'])
def test_new_component_cache_positive_and_tamper_refusal(field):
    d,data,cache,lineage=fixture()
    rows,centers,source=component(data,cache,d,lineage,None)
    assert source=='verified_cp16_cache' and len(rows)==24 and centers['A1'][0]==1
    bad=copy.deepcopy(lineage);entry=bad['new_components']['fold_1:'+str(d)]
    entry[field]='tampered'
    with pytest.raises(ValueError,match='identity'):component(data,cache,d,bad,None)


def test_resigned_wrong_origin_and_nonfinite_cache_refused():
    d,data,cache,lineage=fixture();entry=lineage['new_components']['fold_1:'+str(d)]
    entry['origin_utc']='wrong';entry['content_sha256']=component_digest(entry)
    with pytest.raises(ValueError,match='origin/protocol'):component(data,cache,d,lineage,None)
    d,data,cache,lineage=fixture();entry=lineage['new_components']['fold_1:'+str(d)]
    entry['central']['A1']=[1.];entry['content_sha256']=component_digest(entry)
    with pytest.raises(ValueError,match='central vector'):component(data,cache,d,lineage,None)


@pytest.mark.parametrize('unit',['s','ms','us','ns'])
def test_restart_timestamp_resolution_cannot_change_complete_day(unit):
    d=date(2020,10,25);ix=day_hours(d).as_unit(unit);one=np.ones(len(ix))
    state=SharedResidualState();state.issue(d,ix,one,one,one)
    restored=SharedResidualState.loads(state.dumps())
    restored.release(date(2020,10,27),lambda ix:np.ones(len(ix))*3)
    assert restored.trace[-1]['status']=='consumed' and restored.trace[-1]['n']==25


def test_cp16_partition_projection_occurs_before_materialization(monkeypatch):
    import cp16.inputs as m
    seen=[];spec=SimpleNamespace(eda_cutoff=date(2026,4,7))
    monkeypatch.setattr(m,'identities',lambda root:({},{}))
    monkeypatch.setattr(m,'load_partition_spec',lambda path:spec)
    def reader(path,*,columns,filters):
        seen.append((columns,filters));return 'filtered-frame'
    monkeypatch.setattr(m.pd,'read_parquet',reader)
    monkeypatch.setattr(m,'prepare',lambda frame,p,s:frame)
    assert m.load(Path('.'),before=date(2020,7,1))[0]=='filtered-frame'
    assert seen==[(['timestamp_utc','delivery_date','price_eur_mwh','load_forecast_mw'],
        [('delivery_date','>=',date(2019,1,1)),('delivery_date','<=',date(2026,4,7)),('delivery_date','<',date(2020,7,1))])]


def test_learned_transforms_fit_training_only_with_positive_control():
    from cp15.models import prepared_linear
    train=np.array([[1.,np.nan],[3.,4.],[5.,8.]])
    other=np.array([[100.,1000.]])
    x,z,fill,scaler=prepared_linear(train,other)
    _,_,fill2,scaler2=prepared_linear(train,other*1000)
    np.testing.assert_array_equal(fill,[3.,6.])
    np.testing.assert_array_equal(fill,fill2)
    np.testing.assert_array_equal(scaler.mean_,scaler2.mean_)
    np.testing.assert_array_equal(scaler.scale_,scaler2.scale_)
    _,_,fill3,scaler3=prepared_linear(train+7,other)
    assert not np.array_equal(fill,fill3) and not np.array_equal(scaler.mean_,scaler3.mean_)
