"""Pinned CP-15 daily forecast comparison. All writes local to CP-15/cache outputs."""
from __future__ import annotations
import os
os.environ.setdefault('OPENBLAS_NUM_THREADS','1');os.environ.setdefault('OMP_NUM_THREADS','4');os.environ.setdefault('VECLIB_MAXIMUM_THREADS','1')
import argparse,hashlib,json,resource,sys,time
from datetime import date,timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import pandas as pd
from cp15.data import load_inputs,sha,protocol,POLICIES,FIT_POLICIES,LABELS,origin_utc
from cp15.models import fit_day
from cp15.residuals import ResidualBuffer,BUFFER_POLICIES


def dump(path,obj):path.write_text(json.dumps(obj,indent=2,sort_keys=True,allow_nan=False,default=str)+'\n')


def fingerprint():
    files=['src/cp15/data.py','src/cp15/models.py','reports/cp15/protocol.json','uv.lock','data/snapshot.parquet']
    return hashlib.sha256(json.dumps({p:sha(ROOT/p) for p in files},sort_keys=True).encode()).hexdigest()


def day_predictions(data,d,cache,force=False):
    rows=data.rows(d);dest=cache/str(d);result=dest/'central.parquet';record=dest/'fits.json'
    if result.exists() and record.exists() and not force:
        saved=pd.read_parquet(result);meta=json.loads(record.read_text())
        if sha(result)!=meta['central_sha256'] or saved.row_index.tolist()!=rows.tolist():raise ValueError('corrupt/misaligned fit cache')
        return rows,{p:saved[p].to_numpy(float) for p in BUFFER_POLICIES},meta['fits'],True
    centers={'B0':data.naive[rows]};fits=[]
    for p in FIT_POLICIES:
        center,log=fit_day(data,d,p,rows=rows);centers[p]=center;fits.extend(log)
    centers['A3']=(centers['A1']+centers['A2'])/2
    centers['A5']=(centers['A1']+centers['A2']+centers['A4'])/3
    dest.mkdir(parents=True,exist_ok=True)
    pd.DataFrame({'row_index':rows,**centers}).to_parquet(result,index=False)
    dump(record,{'central_sha256':sha(result),'fits':fits})
    return rows,centers,fits,False


def run_fold(data,fold_name,output,cache):
    fold=data.spec.fold(fold_name);start=data.warmup_start(fold.evaluation.start)
    dates=pd.date_range(start,fold.evaluation.end,freq='D').date
    buf=ResidualBuffer();frames=[];issued=[];fits=[];origins=[];began=time.perf_counter()
    truth=pd.Series(data.y,index=data.index)
    ref=data.reference.loc[data.reference.fold.eq(fold_name)]
    cache_hits=0
    for d in dates:
        tick=time.perf_counter()
        buf.release(d,lambda ix:truth.reindex(ix).to_numpy())
        rows,centers,logs,hit=day_predictions(data,d,cache)
        fits.extend([{**x,'fold':fold_name,'phase':'evaluation' if d>=fold.evaluation.start else 'warmup'} for x in logs]);cache_hits+=int(hit)
        buf.issue(d,data.index[rows],centers,data.scale[rows])
        for p,c in centers.items():
            issued.append(pd.DataFrame({'fold':fold_name,'policy':p,'timestamp_utc':data.index[rows],
                'delivery_date':d,'origin_utc':origin_utc(d).tz_convert('UTC'),'central':c,'level':data.level[rows],'scale':data.scale[rows],
                'phase':'evaluation' if d>=fold.evaluation.start else 'warmup'}))
        target=ref.loc[ref.delivery_date.eq(d)]
        stats={}
        if len(target):
            selected=target.row_index.to_numpy(int)
            positions=pd.Index(rows).get_indexer(selected)
            if (positions<0).any():raise ValueError('missing required model forecasts')
            for p in POLICIES:
                if p=='B1':
                    central=target.raw_p50.to_numpy(float)
                    q=target[[f'final_{x}' for x in LABELS]].to_numpy(float)
                    if not np.isfinite(q).all() or (np.diff(q,axis=1)<0).any():raise ValueError('invalid preserved reference')
                else:
                    central=centers[p][positions]
                    q,stats[p]=buf.predict(p,central,data.scale[selected])
                frame=pd.DataFrame({'fold':fold_name,'policy':p,'timestamp_utc':data.index[selected],
                    'delivery_date':d,'origin_utc':origin_utc(d).tz_convert('UTC'),'y_true':data.y[selected],
                    'central':central,'level':data.level[selected],'scale':data.scale[selected]})
                for j,label in enumerate(LABELS):frame[label]=q[:,j]
                frames.append(frame)
        origins.append({'fold':fold_name,'delivery_date':str(d),'origin_utc':str(origin_utc(d).tz_convert('UTC')),
                        'phase':'evaluation' if d>=fold.evaluation.start else 'warmup','issued_hours_per_policy':len(rows),
                        'eligible_evaluation_hours':len(target),'cache_hit':hit,'buffer':stats,
                        'wall_seconds':time.perf_counter()-tick,'max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
        print(f'{fold_name} {d} rows={len(rows)} evaluation={len(target)} cache={hit} seconds={time.perf_counter()-tick:.2f}',flush=True)
    out=output/'folds';out.mkdir(parents=True,exist_ok=True)
    pd.concat(frames,ignore_index=True).to_parquet(out/f'{fold_name}-predictions.parquet',index=False)
    pd.concat(issued,ignore_index=True).to_parquet(out/f'{fold_name}-issued.parquet',index=False)
    pd.DataFrame(fits).to_parquet(out/f'{fold_name}-fits.parquet',index=False)
    pd.DataFrame(buf.trace).to_parquet(out/f'{fold_name}-feedback.parquet',index=False)
    dump(out/f'{fold_name}-origins.json',origins)
    dump(out/f'{fold_name}-run.json',{'fold':fold_name,'warmup_start':str(start),'evaluation_start':str(fold.evaluation.start),
         'evaluation_end':str(fold.evaluation.end),'origin_count':len(dates),'cache_hits':cache_hits,
         'logical_fit_calls':int(sum(x['fit_calls'] for x in fits)),'model_records':len(fits),
         'runtime_seconds':time.perf_counter()-began,'max_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
         'protocol_sha256':sha(ROOT/'reports/cp15/protocol.json'),'central_fingerprint':cache.name,
         'input_sha256':data.p['input_sha256']})


def score(data,output):
    from cp15.scoring import evaluate
    paths=[output/'folds'/f'{f.name}-predictions.parquet' for f in data.spec.development_folds]
    pred=pd.concat([pd.read_parquet(p) for p in paths],ignore_index=True)
    expected=data.reference[['fold','timestamp_utc','delivery_date','y_true']]
    tables=evaluate(pred,expected_keys=expected)
    pred.to_parquet(output/'predictions.parquet',index=False)
    for name,table in tables.items():
        if isinstance(table,pd.DataFrame):table.to_csv(output/f'{name}.csv',index=False)
        else:dump(output/f'{name}.json',table)
    dump(output/'artifact-manifest.json',{'protocol_sha256':sha(ROOT/'reports/cp15/protocol.json'),
        'central_fingerprint':fingerprint(),'artifact_sha256':{str(p.relative_to(output)):sha(p) for p in sorted(output.rglob('*')) if p.is_file() and 'attempt-1' not in p.parts and p.name!='artifact-manifest.json'},
        'evidence_class':'development_post_selection'})


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--fold',choices=[f'fold_{i}' for i in range(1,6)])
    ap.add_argument('--score',action='store_true');ap.add_argument('--inspect',action='store_true');ap.add_argument('--reproduce-day',type=date.fromisoformat)
    ap.add_argument('--output',type=Path,default=ROOT/'reports/cp15');ap.add_argument('--cache',type=Path,default=ROOT/'data/cp15-cache')
    args=ap.parse_args();output=args.output.resolve()
    if ROOT in output.parents and output!=ROOT/'reports/cp15' and ROOT/'reports/cp15' not in output.parents:raise ValueError('output outside CP-15 allowlist')
    output.mkdir(parents=True,exist_ok=True)
    data=load_inputs(ROOT);cache=args.cache.resolve()/fingerprint()
    if args.inspect:
        print(json.dumps({'eligible_counts':data.reference.groupby('fold').size().to_dict(),
            'warmup_start':{f.name:str(data.warmup_start(f.evaluation.start)) for f in data.spec.development_folds}},indent=2));return
    if args.reproduce_day:
        rows,centers,logs,_=day_predictions(data,args.reproduce_day,cache,force=True)
        dump(output/f'reproduction-{args.reproduce_day}.json',{'rows':rows.tolist(),'centers':{p:v.tolist() for p,v in centers.items()},'logs':logs});return
    if args.fold:run_fold(data,args.fold,output,cache)
    elif not args.score:
        for fold in data.spec.development_folds:run_fold(data,fold.name,output,cache)
    if args.score:score(data,output)

if __name__=='__main__':main()
