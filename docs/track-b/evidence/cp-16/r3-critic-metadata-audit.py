from pathlib import Path
from datetime import date,timedelta
import json,hashlib,subprocess,importlib.metadata,os
root=Path.cwd()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=root).decode().strip()
p=json.loads((root/'reports/v2-causal/protocol.json').read_text())
m=json.loads((root/'reports/v2-causal/artifact-manifest.json').read_text())
for name,h in m['artifact_sha256'].items():assert sha(root/name)==h,name
for name,h in p['implementation_sha256'].items():assert sha(root/name)==h,name
for name,h in p['input_sha256'].items():
    if ':' in name:
        actual=hashlib.sha256(subprocess.check_output(['git','show',name],cwd=root)).hexdigest()
    else:actual=sha(root/name)
    assert actual==h,name
for name,v in p['dependencies'].items():assert importlib.metadata.version(name)==v,name
assert sha(root/'reports/v2-causal/input-manifest.json')==p['input_manifest_sha256']
assert subprocess.check_output(['git','show',m['resumption_protocol_commit']+':reports/v2-causal/protocol.json'],cwd=root)==(root/'reports/v2-causal/protocol.json').read_bytes()
freeze=json.loads(subprocess.check_output(['git','show',m['admission_freeze_commit']+':reports/v2-causal/lineage.json'],cwd=root))
assert freeze['execution_stage']=='training_only_admission_complete_frozen_before_outer_scoring'
assert freeze==json.loads((root/'docs/track-b/evidence/cp-16/r3-admission-lineage.json').read_text())
assert len(freeze['admission'])==35
plan=(root/'capstone_v21.md').read_text()
bar=plan[plan.index('### 14.8'):plan.index('### 14.9')].strip()
assignment=Path('/Users/djourno/Downloads/PJM/.local/tmp/cp-16/resumption/integration-assignment.md').read_text()
assert bar in assignment
base=m['baseline'];changed=git('diff','--name-only',base+'...HEAD').splitlines()
allowed=lambda n:n.startswith(('src/cp16/','tests/cp16/','reports/v2-causal/','docs/track-b/evidence/cp-16/')) or n in ('scripts/cp16_v2.py','capstone_v21.md','docs/track-b/capstone_v21-r1-to-v21-r2-amendments.md','docs/track-b/capstone_v21-r2-to-v21-r3-amendments.md','docs/track-b/cp-16-v2-brief.md')
assert all(allowed(n) for n in changed)
assert not git('diff','--name-only',base+'...HEAD','--','src/cp15','reports/cp15','data','models','reports/cp2')
for ref in (m['historical_candidate'],m['historical_evidence_tip'],m['resumption_protocol_commit'],m['admission_freeze_commit']):
    subprocess.run(['git','merge-base','--is-ancestor',ref,'gauntlet/cp-16'],check=True,cwd=root)
old=m['historical_evidence_tip']
for name in ['protocol.json','report.md','lineage.json','resources.json','input-manifest.json','artifact-manifest.json','reproduce.md','failures.csv']:
    assert subprocess.check_output(['git','show',old+':reports/v2-causal/'+name],cwd=root)==(root/'docs/track-b/evidence/cp-16/attempt-1'/name).read_bytes(),name
for name in ['integration.md','checkpoint-return.md','review-identity.json','resource-final.json','integration-assignment.md']:
    assert subprocess.check_output(['git','show',old+':docs/track-b/evidence/cp-16/'+name],cwd=root)==(root/'docs/track-b/evidence/cp-16/attempt-1'/('evidence-'+name)).read_bytes(),name
manifest=json.loads((root/'reports/v2-causal/input-manifest.json').read_text())
assert not manifest['support_failures']
import pandas as pd
exclusions={}
for f in manifest['folds']:
    start=date.fromisoformat(f['evaluation_start']);end=date.fromisoformat(f['evaluation_end'])
    assert f['date_count']<=150
    assert (start-date.fromisoformat(f['warmup_start'])).days<=60
    assert [x['day'] for x in f['admission']]==[str(start-timedelta(days=x)) for x in range(8,1,-1)]
    keys=pd.to_datetime(f['original_target_keys'],utc=True)
    whole=pd.date_range(pd.Timestamp(start,tz='Europe/Berlin'),pd.Timestamp(end+timedelta(days=1),tz='Europe/Berlin'),freq='h',inclusive='left').tz_convert('UTC')
    missing=whole.difference(keys)
    exclusions[f['fold']]={'eligible':len(keys),'canonical':len(whole),'excluded':len(missing),'excluded_by_day':pd.Series(missing.tz_convert('Europe/Berlin').date).value_counts().astype(int).to_dict()}
    for o in f['origins']:
        d=date.fromisoformat(o['day']);assert pd.Timestamp(o['origin_utc'])==pd.Timestamp(d-timedelta(days=1),tz='UTC')+pd.Timedelta(hours=11)
ledger=json.loads(Path(os.environ['CP16_LEDGER']).read_text())
historical=json.loads((root/'docs/track-b/evidence/cp-16/attempt-1/ledger-before-resumption.json').read_text())
for k,v in historical['counts'].items():assert ledger['counts'][k]>=v
assert historical['counts']['policy_days']==3730
assert all(v<=ledger['caps'][k] for k,v in ledger['counts'].items())
assert ledger['counts']['primitive_fits']==ledger['counts']['inner_fits']+ledger['counts']['final_fits']
result={'artifact_hashes_verified':len(m['artifact_sha256']),'implementation_hashes_verified':len(p['implementation_sha256']),'input_hashes_verified':len(p['input_sha256']),'dependencies_match':True,'bar_matches_assignment':True,'frozen_admission_dates':35,'preserved_historical_artifacts':13,'changes_within_envelope':len(changed),'excluded_original_hours':{k:{**v,'excluded_by_day':{str(d):n for d,n in v['excluded_by_day'].items()}} for k,v in exclusions.items()},'counts_at_audit':ledger['counts'],'main_sha':git('rev-parse','main'),'candidate':git('rev-parse','HEAD'),'clean':not git('status','--porcelain')}
print(json.dumps(result,indent=2))
