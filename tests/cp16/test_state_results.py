"""Independent real-data residual oracle; run only under the shared CP-16 monitor."""
from datetime import date, timedelta
import json, os
from pathlib import Path
import numpy as np
import pandas as pd
from cp16.budget import Budget

ROOT=Path(__file__).resolve().parents[2]
LEVELS=np.array([.025,.1,.25,.5,.75,.9,.975])
LABELS=['p025','p10','p25','p50','p75','p90','p975']


def canonical(day):
    return pd.date_range(pd.Timestamp(day,tz='Europe/Berlin'),pd.Timestamp(day+timedelta(days=1),tz='Europe/Berlin'),freq='h',inclusive='left').tz_convert('UTC').as_unit('ns')


def test_independent_all_origin_residual_replay():
    budget=Budget(os.environ['CP16_LEDGER'])
    manifest=json.loads((ROOT/'reports/v2-causal/input-manifest.json').read_text())
    lineage=json.loads((ROOT/'reports/v2-causal/lineage.json').read_text())
    predictions=pd.read_parquet(ROOT/'reports/v2-causal/predictions.parquet')
    # Predicate and projection are supplied before opening any research outcomes.
    raw=pd.read_parquet(ROOT/'data/snapshot.parquet',columns=['timestamp_utc','delivery_date','price_eur_mwh'],
        filters=[('delivery_date','>=',date(2019,1,1)),('delivery_date','<=',date(2026,4,7))])
    truth=raw.set_index('timestamp_utc').price_eur_mwh
    original={(x['fold'],x['day']):x for x in lineage['origins']}
    admission={(x['fold'],x['day']):x for x in lineage['admission']}
    observed=0;max_difference=0.
    import hashlib
    digest=lambda a:hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
    for fold in manifest['folds']:
        name=fold['fold'];issued=pd.read_parquet(ROOT/f'reports/cp15/folds/{name}-issued.parquet',filters=[('policy','in',['A1','B2'])])
        pending={};consumed=set();buffer={}
        for origin in fold['origins']:
            budget.reserve(policy_days=2)
            d=date.fromisoformat(origin['day'])
            for released in sorted(pending):
                if released>d-timedelta(days=2):continue
                ix,c,s=pending[released]
                if not ix.equals(canonical(released)):
                    consumed.add(released);continue
                y=truth.reindex(ix).to_numpy()
                if not np.isfinite(y).all():continue
                buffer[released]=(y-c)/s;consumed.add(released)
            pending={d:v for d,v in pending.items() if d not in consumed}
            buffer={d:buffer[d] for d in sorted(buffer)[-28:]}
            new=lineage['new_components'].get(name+':'+str(d))
            if new:
                ix=pd.to_datetime(new['timestamp_utc'],utc=True).as_unit('ns')
                c=np.asarray(new['central']['A1'])/2+np.asarray(new['central']['B2'])/2
                preceding=pd.date_range(end=canonical(d)[0]-pd.Timedelta(hours=1),periods=168,freq='h')
                s=np.full(len(ix),max(np.std(truth.reindex(preceding).to_numpy(),ddof=1),1.))
                assert digest(s)==new['scale_sha256']
            else:
                a=issued.loc[issued.delivery_date.eq(d)&issued.policy.eq('A1')].sort_values('timestamp_utc')
                b=issued.loc[issued.delivery_date.eq(d)&issued.policy.eq('B2')].sort_values('timestamp_utc')
                ix=pd.DatetimeIndex(a.timestamp_utc).as_unit('ns');c=a.central.to_numpy()/2+b.central.to_numpy()/2;s=a.scale.to_numpy()
                assert len(a)==len(b)
            assert len(ix)==original[(name,str(d))]['n_hours']
            if not len(ix):continue
            is_eval=d>=date.fromisoformat(fold['evaluation_start'])
            meta=admission.get((name,str(d))) if not is_eval else original[(name,str(d))]
            if meta:
                assert len(buffer)==28
                errors=np.concatenate(list(buffer.values()));hours=np.concatenate([canonical(x).tz_convert('Europe/Berlin').hour for x in buffer])
                days=np.concatenate([np.repeat(str(x),len(v)) for x,v in buffer.items()])
                pooled=np.quantile(errors,LEVELS,method='linear');hourly={}
                for h in range(24):
                    mask=hours==h;n=int(mask.sum());distinct=len(set(days[mask]));w=n/(n+56) if distinct>=14 else 0
                    hourly[h]=w*np.quantile(errors[mask],LEVELS,method='linear')+(1-w)*pooled if w else pooled
                    assert meta['hour_support'][str(h)]=={'n':n,'distinct_days':distinct,'weight':w}
                q={'V2-H':c[:,None]+s[:,None]*np.array([hourly[h] for h in ix.tz_convert('Europe/Berlin').hour]),'V2-P':c[:,None]+s[:,None]*pooled}
                assert meta['buffer_sha256']==digest(errors) and meta['central_sha256']==digest(c) and meta['scale_sha256']==digest(s)
                assert meta['buffer_start']==str(min(buffer)) and meta['buffer_end']==str(max(buffer))
                assert max(buffer)<=d-timedelta(days=2)
                for policy,vector in q.items():
                    if is_eval:
                        saved=predictions.loc[predictions.fold.eq(name)&predictions.policy.eq(policy)&predictions.delivery_date.eq(d)].sort_values('timestamp_utc')
                        actual=saved[LABELS].to_numpy();np.testing.assert_allclose(actual,vector,atol=1e-10,rtol=1e-12)
                        max_difference=max(max_difference,float(np.max(np.abs(actual-vector))));observed+=len(actual)
                    else:assert digest(vector)==meta['vector_sha256'][policy]
            pending[d]=(ix,c,s)
        persisted=lineage['states'][name]
        assert set(persisted['consumed'])==set(map(str,consumed))
        for item in persisted['buffer']:np.testing.assert_array_equal(item['errors'],buffer[date.fromisoformat(item['day'])])
    assert observed==21494
    print({'independent_H_P_rows':observed,'max_abs_difference':max_difference,'policy_days':1276})


def test_real_state_restart_and_saved_cache_refusals():
    from cp16.inputs import load, SavedComponents
    from cp16.residuals import SharedResidualState
    budget=Budget(os.environ['CP16_LEDGER'])
    # Conservatively charge all 37 reconstructed warm-up dates plus the evaluated date.
    budget.reserve(policy_days=76)
    frozen=json.loads((ROOT/'docs/track-b/evidence/cp-16/r3-admission-lineage.json').read_text())
    data,_=load(ROOT);cache=SavedComponents(ROOT,'fold_1',data);d=date(2020,7,1)
    rows,centers,_=cache.get(d)
    baseline=SharedResidualState.from_dict(frozen['states']['fold_1'])
    replay=SharedResidualState.loads(baseline.dumps())
    truth=pd.Series(data.y,index=data.index)
    for state in (baseline,replay):state.release(d,lambda ix:truth.reindex(ix).to_numpy())
    q,meta=baseline.predict(d,data.index[rows],centers['A1'],centers['B2'],data.scale[rows])
    other,othermeta=replay.predict(d,data.index[rows],centers['A1'],centers['B2'],data.scale[rows])
    assert meta==othermeta
    pred=pd.read_parquet(ROOT/'reports/v2-causal/predictions.parquet')
    for policy in q:
        np.testing.assert_array_equal(q[policy],other[policy])
        saved=pred.loc[pred.fold.eq('fold_1')&pred.policy.eq(policy)&pred.delivery_date.eq(d)].sort_values('timestamp_utc')
        np.testing.assert_allclose(q[policy],saved[LABELS],atol=1e-10,rtol=1e-12)
    import pytest
    original=cache.issued.copy()
    mask=cache.issued.delivery_date.eq(d)
    for column,value,match in [('origin_utc',pd.Timestamp('2000-01-01',tz='UTC'),'origin'),('scale',999.,'scale')]:
        cache.issued=original.copy();cache.issued.loc[mask,column]=value
        with pytest.raises(ValueError,match=match):cache.get(d)
    cache.issued=original.copy();cache.issued=cache.issued.drop(cache.issued.loc[mask].index[0])
    with pytest.raises(ValueError,match='target identity'):cache.get(d)
    cache.issued=original;cache.fits.loc[cache.fits.delivery_date.eq(str(d)),'train_target_sha256']='wrong'
    with pytest.raises(ValueError,match='training identity'):cache.get(d)
    print('Real admission-state restart matches issued first evaluation vectors; wrong origin/scale/keys/training cache refused')
