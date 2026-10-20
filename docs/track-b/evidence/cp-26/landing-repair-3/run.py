"""Serial Lead verification driver; runs only tests and CI checks under the existing monitor."""
import importlib.util,json,os,re,subprocess,sys,time
from pathlib import Path
ROOT=Path('/Users/djourno/Downloads/PJM')
OUT=ROOT/'.local/tmp/cp-26-landing-repair-3'
CLEAN=OUT/'final-check'
CAND='c7829b3687ed7e295f1aeac3738e4d1a257a81aa'
CHECK=CLEAN/'docs/track-b/evidence/cp-26/landing-repair-3/check.py'
STRESS=CLEAN/'docs/track-b/evidence/cp-26/landing-repair-2/stress_check.py'
PREP=OUT/'prepared'
PY=ROOT/'.venv/bin/python'
E={k:v for k,v in os.environ.items() if not re.match(r'CP\d+[A-Z]?_',k) and k not in ('PYTHONPATH','VIRTUAL_ENV','PYTHONDONTWRITEBYTECODE','PYTHONPYCACHEPREFIX')}
TMP=OUT/'tmp';TMP.mkdir(exist_ok=True)
E.update(MLFLOW_DISABLE_TELEMETRY='true',DO_NOT_TRACK='1',UV_CACHE_DIR=str(ROOT/'.local/cache/uv'),UV_OFFLINE='1',UV_PYTHON_DOWNLOADS='never',UV_NO_PROGRESS='1',TMPDIR=str(TMP),CP26_PROJECT_ROOT=str(ROOT))
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'): E[key]='1'
sys.path.insert(0,str(CLEAN/'src'))
os.environ.update({k:E[k] for k in ('MLFLOW_DISABLE_TELEMETRY','DO_NOT_TRACK','CP26_PROJECT_ROOT')})
from cp26.budget import Budget,resource_summary
record={'candidate':CAND,'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'commands':[],'ledger_before':{},'ledger_after':{}}
def snapshot():
 s=Budget().read()
 return {'jobs':len(s['jobs']),'total_seconds':resource_summary(s)['total_seconds'],'running':[j['name'] for j in s['jobs'] if j['running']]}
def save(): (OUT/'run.json').write_text(json.dumps(record,indent=2)+'\n')
def command(label,child,monitored=True):
 cmd=([str(PY),'-B',str(CLEAN/'scripts/cp26_rebaseline.py'),'monitor','--name','landing-repair-3-'+label,'--workers','4','--'] if monitored else [])+list(map(str,child))
 began=time.time();log=OUT/(label+'-outer.log')
 with log.open('w') as f: rc=subprocess.run(cmd,cwd=CLEAN,env=E,stdout=f,stderr=subprocess.STDOUT).returncode
 item={'label':label,'command':cmd,'cwd':str(CLEAN),'exit_code':rc,'wall_seconds':round(time.time()-began,3),'outer_log':str(log),'monitored':monitored}
 record['commands'].append(item);save();print(json.dumps(item),flush=True)
 return rc
record['ledger_before']=snapshot();save()
assert record['ledger_before']['running']==[]
base=[str(PY),str(STRESS)]
copy=PREP/'copy312';env=OUT/'env-stress312';res=OUT/'results';res.mkdir(exist_ok=True)
burn=OUT/'burners.json'
try:
 assert command('burners-start',base+['burners','start','--record',str(burn)],False)==0
 try:
  assert command('stress-four',base+['stress','--copy',copy,'--env',env,'--out',res,'--label','stress-four','--emulation','four-burners','--runs','5'])==0
  assert command('cp26-four',base+['pytest','--copy',copy,'--env',env,'--out',res,'--label','cp26-four','--emulation','four-burners','tests/test_cp26_*.py','tests/test_rebaseline_disclosures.py'])==0
 finally:
  assert command('burners-stop',base+['burners','stop','--record',str(burn)],False)==0
 assert command('stress-quiet',base+['stress','--copy',copy,'--env',env,'--out',res,'--label','stress-quiet','--emulation','quiet','--runs','5'])==0
 for version,c in [('3.12','copy312'),('3.13','copy313')]:
  assert command('ci'+version,base+['ci','--copy',PREP/c,'--env',OUT/('env-ci'+version),'--python',version,'--out',res,'--label','ci'+version])==0
 for label,tree in [('curated',PREP/'curated'),('full',CLEAN)]:
  assert command(label+'-suite',[str(PY),str(CHECK),'suite','--candidate',CAND,'--tree',tree,'--env',OUT/('env-'+label),'--out',OUT/(label+'-suite')])==0
 record['green']=True
finally:
 record['ledger_after']=snapshot();record['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());save()
