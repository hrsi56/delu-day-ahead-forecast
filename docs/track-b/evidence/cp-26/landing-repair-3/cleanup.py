"""Remove only the temporary verification contexts created by this round."""
from pathlib import Path
import atexit,hashlib,json,os,shutil,subprocess,time
ROOT=Path('/Users/djourno/Downloads/PJM');LEAD=ROOT/'.local/worktrees/cp-26/lead';OUT=ROOT/'.local/tmp/cp-26-landing-repair-3';ART=ROOT/'.local/artifacts/cp-26-landing-repair-3';D=LEAD/'docs/track-b/evidence/cp-26/landing-repair-3'
def git(*args,cwd=LEAD):return subprocess.check_output(['git','--no-pager',*args],cwd=cwd,text=True)
r=json.loads((D/'verification.json').read_text());assert r['green'] and not r['ledger_after']['running']
receipt={'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'commands':[],'worktrees_before':git('worktree','list','--porcelain')}
ART.mkdir(parents=True,exist_ok=True)
receipt['complete']=False
def save_receipt():
 (D/'cleanup.json').write_text(json.dumps(receipt,indent=2)+'\n')
 (ART/'cleanup.json').write_text(json.dumps(receipt,indent=2)+'\n')
atexit.register(save_receipt)
receipt['lead_preflight_tracked_status']=git('status','--porcelain=v1','--untracked-files=no').splitlines()
assert not receipt['lead_preflight_tracked_status']
assert git('diff','--cached','--name-only',cwd=ROOT)==''
assert git('status','--porcelain=v1',cwd=OUT/'final-check')==''
assert git('diff','--name-only',cwd=OUT/'prepared/curated')==''
assert git('write-tree',cwd=OUT/'prepared/curated').strip()==r['history_free']['tree']
save_receipt()
recovery=ART/'session-records';recovery.mkdir(exist_ok=True)
for p in OUT.iterdir():
 if p.is_file() and p.suffix == '.json':shutil.copy2(p,recovery/p.name)
shutil.copy2(OUT/'cleanup.py',D/'cleanup.py')
for p in (OUT/'final-check',OUT/'prepared/curated'):
 if p.name=='final-check':assert git('status','--porcelain=v1',cwd=p)==''
 else:assert git('write-tree',cwd=p).strip()==r['history_free']['tree']
 cmd=['git','--no-pager','worktree','remove','--force',str(p)]
 done=subprocess.run(cmd,cwd=LEAD,capture_output=True,text=True);assert done.returncode==0,done.stderr
 receipt['commands'].append({'command':cmd,'exit_code':0,'stdout':done.stdout,'stderr':done.stderr,'path_exists_after':p.exists()})
barrier=OUT/'tmp/.git';expected='gitdir: '+str(OUT/'tmp/absent-git-discovery-boundary')+'\n'
assert barrier.read_text()==expected;barrier.unlink()
receipt['barrier_removed']=not barrier.exists();receipt['barrier_path']=str(barrier)
receipt['temporary_entries_removed']=sorted(p.name for p in OUT.iterdir() if p.is_dir())
shutil.rmtree(OUT)
receipt['temporary_root_removed']=not OUT.exists()
receipt['worktrees_after']=git('worktree','list','--porcelain')
assert str(OUT) not in receipt['worktrees_after']
receipt['main']=git('rev-parse','main').strip();receipt['origin_main']=git('rev-parse','origin/main').strip()
receipt['main_index']=git('diff','--cached','--name-only',cwd=ROOT).splitlines()
receipt['main_worktree_status']=git('status','--porcelain=v1',cwd=ROOT).splitlines()
receipt['lead_tracked_status']=git('status','--porcelain=v1','--untracked-files=no').splitlines()
assert receipt['main']==receipt['origin_main']=='647d6eb81b2cf6e0cfaf4152f659d689ff973578'
assert not receipt['main_index'] and not receipt['lead_tracked_status']
receipt['secret_hooks_path']=git('config','--get','core.hooksPath').strip()
assert receipt['secret_hooks_path']==str(ROOT/'.githooks')
receipt['retained_recovery']=str(ART)
receipt['complete']=True
receipt['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
(D/'cleanup.json').write_text(json.dumps(receipt,indent=2)+'\n')
(ART/'cleanup.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt))
