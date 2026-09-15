from pathlib import Path
import json,hashlib,subprocess
import numpy as np
import pandas as pd
R=Path.cwd(); out=Path('/tmp/cp15-critic-arithmetic.json'); D=R/'reports/cp15'
p=pd.read_parquet(D/'predictions.parquet'); p['delivery_date']=pd.to_datetime(p.delivery_date)
Q=['p025','p10','p25','p50','p75','p90','p975']; policies=['B0','B1','B2','B3','A1','A2','A3','A4','A5']; folds=[f'fold_{i}' for i in range(1,6)]
assert set(p.policy)==set(policies) and len(p)==96723
assert not p.duplicated(['policy','timestamp_utc']).any()
assert np.isfinite(p[Q+['central','y_true','scale']]).all().all()
assert (np.diff(p[Q].to_numpy(),axis=1)>=0).all()
base=p[p.policy=='B0'].sort_values('timestamp_utc')
for a in policies:
 x=p[p.policy==a].sort_values('timestamp_utc')
 pd.testing.assert_frame_equal(x[['fold','timestamp_utc','delivery_date','y_true']].reset_index(drop=True),base[['fold','timestamp_utc','delivery_date','y_true']].reset_index(drop=True))
assert base.groupby('fold').size().tolist()==[2160,2159,2112,2160,2156]
def metrics(x):
 y=x.y_true.to_numpy(); f=x.p50.to_numpy(); raw=x.central.to_numpy(); e=f-y
 wis=.5*abs(e); result={'n_hours':len(x),'n_days':x.delivery_date.nunique(),'MAE':abs(e).mean(),'RMSE':np.sqrt((e**2).mean()),'raw_central_MAE':abs(raw-y).mean(),'centering_effect':abs(e).mean()-abs(raw-y).mean(),'bias':e.mean()}
 daily=x.groupby('delivery_date')[['y_true','p50']].mean()
 result['daily_mean_level_MAE']=abs(daily.p50-daily.y_true).mean()
 means=x.groupby('delivery_date')[['y_true','p50']].transform('mean')
 result['within_day_shape_MAE']=abs((x.p50-means.p50)-(x.y_true-means.y_true)).mean()
 for nominal,alpha,lo,hi in [(50,.5,'p25','p75'),(80,.2,'p10','p90'),(95,.05,'p025','p975')]:
  l=x[lo].to_numpy(); u=x[hi].to_numpy(); width=u-l
  below=y<l; above=y>u
  wis+=alpha/2*width+np.maximum(l-y,0)+np.maximum(y-u,0)
  result.update({f'coverage{nominal}':(~(below|above)).mean(),f'hit_count{nominal}':int((~(below|above)).sum()),f'lower_miss_count{nominal}':int(below.sum()),f'upper_miss_count{nominal}':int(above.sum()),f'mean_width{nominal}':width.mean(),f'median_width{nominal}':np.median(width),f'p95_width{nominal}':np.quantile(width,.95)})
 result['WIS']=wis.mean()/3.5
 return result
pf=pd.DataFrame([dict(policy=a,fold=f,**metrics(x)) for (a,f),x in p.groupby(['policy','fold'])]).set_index(['policy','fold'])
peak=pd.DataFrame([dict(policy=a,**metrics(x[x.delivery_date.between('2022-08-15','2022-08-31')])) for a,x in p.groupby('policy')]).set_index('policy')
pooled=pd.DataFrame([dict(policy=a,**metrics(x)) for a,x in p.groupby('policy')]).set_index('policy')
maxdiff={}
for name,t in [('per_fold',pf),('peak',peak),('pooled',pooled)]:
 s=pd.read_csv(D/f'{name}.csv').set_index(t.index.names).reindex(t.index)
 for c in t.columns: np.testing.assert_allclose(t[c],s[c],atol=2e-12,rtol=2e-12)
 maxdiff[name]=float(abs(t-s[t.columns]).max().max())
assert peak.n_hours.eq(408).all() and peak.n_days.eq(17).all()
scores={a:{m:float(np.mean([pf.loc[(a,f),m]/pf.loc[('B0',f),m] for f in folds])) for m in ['MAE','WIS']} for a in policies}
failed={}
for a in policies[4:]:
 checks={1:scores[a]['MAE']<=.9*min(scores[b]['MAE'] for b in policies[:4]),2:scores[a]['WIS']<=.9*min(scores[b]['WIS'] for b in policies[:4]),3:pf.loc[a].coverage95.between(.9,.98).all(),4:peak.loc[a,'coverage95']>=.9 and all(peak.loc[a,m]<=peak.loc[policies[:4],m].min() for m in ['MAE','WIS']),5:all(pf.loc[(a,f),m]<=1.05*min(pf.loc[(b,f),m] for b in ['B2','B3']) for f in folds for m in ['MAE','WIS']),6:True}
 failed[a]=[k for k,v in checks.items() if not v]
rank=sorted(policies[4:],key=lambda a:(scores[a]['MAE'],scores[a]['WIS'],policies.index(a)))
selection=json.loads((D/'selection.json').read_text()); assert selection['failed_criteria']==failed; assert selection['best_observed_policy']==rank[0]; assert selection['qualified_policy'] is None
sha=lambda b:hashlib.sha256(b).hexdigest()
protocol=json.loads((D/'protocol.json').read_text())
for name,expected in protocol['input_sha256'].items(): assert sha((R/name).read_bytes())==expected,name
prereg='bb5e67882fcfdf65b963d25ce785a3999816dfc2'
assert subprocess.check_output(['git','show',f'{prereg}:reports/cp15/protocol.json'])==(D/'protocol.json').read_bytes()
assert subprocess.check_output(['git','show',f'{prereg}:capstone_v21.md'])==(R/'capstone_v21.md').read_bytes()
old=json.loads((D/'attempt-1-preservation.json').read_text())
for name,item in old['mapping'].items():
 content=(R/item['preserved_at']).read_bytes(); assert sha(content)==item['sha256']; assert subprocess.check_output(['git','show',f"{old['evidence_tip']}:{name}"])==content
validation=json.loads((D/'validation.json').read_text())
for name,expected in validation['inherited_ignored_regression_payload']['sha256'].items(): assert sha((R/name).read_bytes())==expected
manifest=json.loads((D/'artifact-manifest.json').read_text())
print('manifest keys',manifest.keys())
result={'rows':len(p),'per_policy':p.groupby('policy').size().to_dict(),'fold_counts':base.groupby('fold').size().to_dict(),'quantile_crossings':0,'finite':True,'maximum_absolute_metric_difference':maxdiff,'relative_scores':scores,'ranking':rank,'failed_criteria':failed,'peak_hits':peak.hit_count95.to_dict(),'peak_denominator':408,'preregistration_bytes_match':True,'attempt1_bytes_match_original_git_objects':True,'input_and_inherited_payload_hashes_match':True}
out.write_text(json.dumps(result,indent=2)+'\n');print(out.read_text())
