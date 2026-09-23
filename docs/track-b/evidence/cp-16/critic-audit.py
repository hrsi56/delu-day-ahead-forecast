from pathlib import Path
import json, hashlib, subprocess
import pandas as pd
root=Path.cwd()
assert str(root)=='/Users/djourno/Downloads/PJM/.local/worktrees/cp-16/critic'
def read(p):return json.loads((root/p).read_text())
def digest(p):return hashlib.sha256((root/p).read_bytes()).hexdigest()
p=read('reports/v2-causal/protocol.json');m=read('reports/v2-causal/input-manifest.json');a=read('reports/v2-causal/artifact-manifest.json');l=read('reports/v2-causal/lineage.json')
for label,items in [('artifacts',a['artifact_sha256']),('implementation',p['implementation_sha256']),('inputs',p['input_sha256'])]:
    checked=0; skipped=[]; mismatches=[]
    for name,want in items.items():
        if ':' in name or name=='docs/track-b/cp-15-resumption-brief.md':skipped.append(name);continue
        got=digest(name);checked+=1
        if got!=want:mismatches.append(name)
    print(label,{'checked':checked,'mismatches':mismatches,'not_opened_outside_assignment':skipped})
    assert not mismatches
assert digest('reports/v2-causal/input-manifest.json')==p['input_manifest_sha256']
anchor=(root/'capstone_v21.md').read_text();bar=anchor.split('### 14.8 Complete CP-16 acceptance checklist\n\n')[1].split('\n### 14.9')[0].strip()
assignment=Path('/Users/djourno/Downloads/PJM/.local/tmp/cp-16/integration-assignment.md').read_text();quoted=assignment.split('## Verbatim bar excerpt\n')[1].split('\n## What to verify')[0].strip()
assert bar==quoted
print('bar_exact_match',True)
prior=subprocess.check_output(['git','show',p['prior_protocol']['commit']+':reports/v2-causal/protocol.json'])
assert hashlib.sha256(prior).hexdigest()==p['prior_protocol']['sha256']
print('prior_protocol_hash_match',True)
keys=pd.read_parquet(root/'reports/cp15/predictions.parquet',columns=['fold','timestamp_utc','delivery_date'],filters=[('policy','==','B0')])
counts=keys.groupby('fold').size().to_dict(); print('original_key_counts',counts,'total',len(keys),'duplicates',int(keys.duplicated(['fold','timestamp_utc']).sum()))
assert list(counts.values())==[2160,2159,2112,2160,2156] and len(keys)==10747 and not keys.duplicated(['fold','timestamp_utc']).any()
print('manifest_top_fields',list(m))
for f in m['folds']:
    print('manifest_fold',{k:(len(v) if isinstance(v,list) else v) for k,v in f.items()})
print('lineage_summary',{k:(len(v) if isinstance(v,(list,dict)) else v) for k,v in l.items()})
print('cache_reproduction',l['cache_reproduction'])
print('admission_dates',[(x['fold'],x['day'],x['n_hours']) for x in l['admission']])
print('missing_required_artifacts',[x for x in ['predictions.parquet','metrics.csv','diagnostics.csv','uncertainty.csv','criteria.csv'] if not (root/'reports/v2-causal'/x).exists()])
print('raw_interrupted_lineage_matches',digest('reports/v2-causal/lineage.json')==digest('docs/track-b/evidence/cp-16/interrupted-admission-lineage.json'))
print('resource_counts',read('reports/v2-causal/resources.json')['counts'])
