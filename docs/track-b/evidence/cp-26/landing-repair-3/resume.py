"""Continue verification after correcting project-contained pytest temp discovery."""
import json,os,re,subprocess,sys,time
from pathlib import Path
ROOT=Path('/Users/djourno/Downloads/PJM');OUT=ROOT/'.local/tmp/cp-26-landing-repair-3';CLEAN=OUT/'final-check';PREP=OUT/'prepared'
PY=ROOT/'.venv/bin/python';STRESS=CLEAN/'docs/track-b/evidence/cp-26/landing-repair-2/stress_check.py';CHECK=CLEAN/'docs/track-b/evidence/cp-26/landing-repair-3/check.py'
CAND='c7829b3687ed7e295f1aeac3738e4d1a257a81aa';record=json.loads((OUT/'run.json').read_text());record.pop('finished_utc',None)
E={k:v for k,v in os.environ.items() if not re.match(r'CP\d+[A-Z]?_',k) and k not in ('PYTHONPATH','VIRTUAL_ENV','PYTHONDONTWRITEBYTECODE','PYTHONPYCACHEPREFIX')}
TMP=OUT/'tmp';barrier=TMP/'.git'
# This path is outside every real test copy/worktree. Never overwrite an existing Git artifact.
with barrier.open('x') as f:f.write('gitdir: '+str(TMP/'absent-git-discovery-boundary')+'\n')
record['temp_discovery_correction']={'initial_failure':'tests/test_47_session_start_hook.py::test_the_hook_never_fails_outside_a_repository','cause':'Project-contained TMPDIR exposed the outer PJM Git repository; the fixture strips all GIT_* ceiling settings.','barrier':str(barrier),'contents':barrier.read_text(),'semantics':'No discoverable valid repository. Hook error handling is exercised via an invalid gitdir rather than the usual filesystem-root not-a-repository error. Valid nested test repositories find their own .git first.','source_and_test_changes':False}
E.update(MLFLOW_DISABLE_TELEMETRY='true',DO_NOT_TRACK='1',UV_CACHE_DIR=str(ROOT/'.local/cache/uv'),UV_OFFLINE='1',UV_PYTHON_DOWNLOADS='never',UV_NO_PROGRESS='1',TMPDIR=str(TMP),CP26_PROJECT_ROOT=str(ROOT))
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):E[key]='1'
sys.path.insert(0,str(CLEAN/'src'));os.environ.update({k:E[k] for k in ('MLFLOW_DISABLE_TELEMETRY','DO_NOT_TRACK','CP26_PROJECT_ROOT')})
from cp26.budget import Budget,resource_summary
def snapshot():
 s=Budget().read();return {'jobs':len(s['jobs']),'total_seconds':resource_summary(s)['total_seconds'],'running':[j['name'] for j in s['jobs'] if j['running']]}
def save():(OUT/'run.json').write_text(json.dumps(record,indent=2)+'\n')
def command(label,child,envbin=None):
 cmd=[str(PY),'-B',str(CLEAN/'scripts/cp26_rebaseline.py'),'monitor','--name','landing-repair-3-'+label,'--workers','4','--',*map(str,child)]
 env=E.copy()
 if envbin is not None:env['PATH']=str(envbin)+os.pathsep+env['PATH']
 began=time.time();log=OUT/(label+'-outer.log')
 with log.open('w') as f:rc=subprocess.run(cmd,cwd=CLEAN,env=env,stdout=f,stderr=subprocess.STDOUT).returncode
 item={'label':label,'command':cmd,'cwd':str(CLEAN),'exit_code':rc,'wall_seconds':round(time.time()-began,3),'outer_log':str(log),'monitored':True,'path_prepend':str(envbin) if envbin else None}
 record['commands'].append(item);save();print(json.dumps(item),flush=True);return rc
save()
try:
 assert command('hook-boundary',[PY,STRESS,'pytest','--copy',PREP/'copy312','--env',OUT/'env-ci3.12','--out',OUT/'results','--label','hook-boundary','--emulation','quiet','tests/test_47_session_start_hook.py'])==0
 for version,name,label in [('3.12','copy312','ci3.12-rerun'),('3.13','copy313','ci3.13')]:
  env=OUT/('env-'+label)
  assert command(label,[PY,STRESS,'ci','--copy',PREP/name,'--env',env,'--python',version,'--out',OUT/'results','--label',label],env/'bin')==0
 for label,tree in [('curated',PREP/'curated'),('full',CLEAN)]:
  assert command(label+'-suite',[PY,CHECK,'suite','--candidate',CAND,'--tree',tree,'--env',OUT/('env-'+label),'--out',OUT/(label+'-suite')])==0
 record['green']=True
finally:
 record['ledger_after']=snapshot();record['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());save()
 # Keep the barrier until all the temp fixtures are removed by Lead cleanup.
