from pathlib import Path
import json,hashlib,subprocess,re
import numpy as np
import pandas as pd
R=Path.cwd();D=R/'reports/cp15'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((D/'artifact-manifest.json').read_text())
for name,value in m['artifact_sha256'].items(): assert sha(R/name)==value,name
s=pd.read_csv(D/'resources.csv').set_index(['fold','policy']); totals=[]
for i in range(1,6):
 f=f'fold_{i}';fits=pd.read_parquet(D/'folds'/f'{f}-fits.parquet');run=json.loads((D/'folds'/f'{f}-run.json').read_text());origins=json.loads((D/'folds'/f'{f}-origins.json').read_text())
 assert fits.fit_calls.sum()==run['logical_fit_calls'];assert len(fits)==run['model_records'];assert len(origins)==run['origin_count'];assert sum(o['cache_hit'] for o in origins)==run['cache_hits']
 assert run['protocol_sha256']==sha(D/'protocol.json')
 for a in ['B0','B1','B2','B3','A1','A2','A3','A4','A5']:
  own=fits[fits.policy==a];v=s.loc[(f,a)]
  assert v.direct_logical_fit_calls==own.fit_calls.sum();assert v.direct_solver_calls==own.solver_calls.fillna(own.fit_calls).sum()
  np.testing.assert_allclose(v.direct_fit_seconds,own.fit_seconds.sum(),atol=2e-12,rtol=2e-12)
  assert v.shared_process_peak_rss_bytes==run['max_rss_bytes'];assert v.shared_fold_wall_seconds==run['runtime_seconds']
  whole=float(re.search(r'^\s*([0-9.]+)\s+real\s+',(D/'execution'/f'{f}.log').read_text(),re.M)[1]);assert v.shared_full_command_wall_seconds==whole
  comp={'A3':['A1','A2'],'A5':['A1','A2','A4']}.get(a,[]);c=fits[fits.policy.isin(comp)]
  assert v.component_logical_fit_calls==c.fit_calls.sum();np.testing.assert_allclose(v.component_fit_seconds,c.fit_seconds.sum(),atol=2e-12,rtol=2e-12)
  if len(own): assert own.model_sha256.nunique()>1
 totals.append({'fold':f,'origins':len(origins),'records':len(fits),'fit_calls':run['logical_fit_calls'],'cache_hits':run['cache_hits'],'peak_rss':run['max_rss_bytes']})
# These protected paths have identical trees/content to the retained first-attempt tip.
protected=['models/champion','data/snapshot.parquet','data/partitions.json','docs/cp2-model-report.md','reports/cp2','reports/cp10','README.md','docs/index.html','app','spaces','DATA-LICENSE.md']
delta=subprocess.check_output(['git','diff','--name-only','193d9cf48c586b9c4b1f43d7a5677b2d5f400832..HEAD','--',*protected],text=True);assert not delta,delta
result={'manifest_files_verified':len(m['artifact_sha256']),'resources_all_45_rows_verified':True,'folds':totals,'preserved_paths_delta':delta}
Path('/tmp/cp15-critic-provenance.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
