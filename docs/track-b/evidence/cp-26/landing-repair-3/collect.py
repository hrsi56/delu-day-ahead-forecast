"""Collect the completed round's commands, test evidence and preservation checks."""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,sys
ROOT=Path('/Users/djourno/Downloads/PJM'); LEAD=ROOT/'.local/worktrees/cp-26/lead'
OUT=ROOT/'.local/tmp/cp-26-landing-repair-3'; CLEAN=OUT/'final-check'
DEST=LEAD/'docs/track-b/evidence/cp-26/landing-repair-3'
CAND='c7829b3687ed7e295f1aeac3738e4d1a257a81aa'; BASE='5671423b9e73ba8003a17ea9e8eae53332dcaa74'
def git(*args,cwd=LEAD):return subprocess.check_output(['git','--no-pager',*args],cwd=cwd,text=True)
def sha(p):
 with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
r=json.loads((OUT/'run.json').read_text());assert r['green']
records={name:json.loads((OUT/'results'/f'{name}.json').read_text()) for name in ('stress-four','stress-quiet','cp26-four')}
records['ci3.12']=json.loads((OUT/'results/ci3.12-rerun.json').read_text())
records['ci3.13']=json.loads((OUT/'results/ci3.13-rerun.json').read_text())
records['initial_ci3.13_sync_failure']=json.loads((OUT/'results/ci3.13.json').read_text())
records['sync313']=json.loads((OUT/'sync313.json').read_text())
records['initial_ci3.12_failure']=json.loads((OUT/'results/ci3.12.json').read_text())
records['hook-boundary']=json.loads((OUT/'results/hook-boundary.json').read_text())
records.update({name:json.loads((OUT/f'{name}-suite/suite.json').read_text()) for name in ('curated','full')})
assert records['stress-four']['passed']==records['stress-quiet']['passed']==5
assert records['cp26-four']['run']['exit_code']==0
assert all(records[x]['green'] for x in ('ci3.12','ci3.13','curated','full'))
assert git('rev-parse','HEAD',cwd=CLEAN).strip()==CAND
assert subprocess.run(['git','symbolic-ref','-q','HEAD'],cwd=CLEAN,capture_output=True).returncode==1
assert git('status','--porcelain=v1',cwd=CLEAN)==''
assert git('rev-parse','main').strip()==git('rev-parse','origin/main').strip()=='647d6eb81b2cf6e0cfaf4152f659d689ff973578'
assert git('diff','--cached','--name-only',cwd=ROOT)==''
scope={}
for base,paths in [('6f57feb',['reports/']),('5671423',['reports/','data/','src/','AGENTS.md','CLAUDE.md','engineering-role.md','orchestrator-role.md','notebooklm-role.md','docs/track-b/gauntlet-templates.md','capstone_v21.md','pyproject.toml','uv.lock','docs/track-b/exposure-ledger.md'])]:
 delta=git('diff','--name-only',base,CAND,'--',*paths).splitlines();assert not delta
 scope[base+':'+','.join(paths)]=delta
names=git('diff','--name-only','04f00ea',CAND).splitlines()
assert all(p=='tests/test_cp26_ledger_liveness.py' or p.startswith('docs/track-b/evidence/cp-26/') for p in names)
scope['04f00ea_allowed_delta']=names
prior=git('diff','--name-status',BASE,CAND).splitlines()
assert all(line.startswith('A\t') or line.endswith('\ttests/test_cp26_ledger_liveness.py') for line in prior)
scope['round3_delta']=prior
text=git('show',CAND+':capstone_v21.md');section=text.split('### 24.7 ',1)[1].split('### 24.8 ',1)[0];section='### 24.7 '+section
scope['anchor_sha256']=hashlib.sha256(text.encode()).hexdigest();scope['section247_sha256']=hashlib.sha256(section.encode()).hexdigest()
verdicts=['cold-rerun-2026-10-15/integration-final-r16-2-PASS.md','gfs-v21-r17/integration-r17-PASS.md','integration.md','landing-repair/integration-PASS.md']
scope['preserved_verdicts']={}
for p in verdicts:
 path='docs/track-b/evidence/cp-26/'+p
 before=git('rev-parse',BASE+':'+path).strip();after=git('rev-parse',CAND+':'+path).strip();assert before==after
 scope['preserved_verdicts'][path]={'blob':after,'sha256':sha(CLEAN/path)}
for s in ('6f57febe3659b1f902c17f3db31ba41e41136178','f014e5b2f09dc7defa103b3c4ec5796d199c262d','04f00eac5506c550ed4c775b84dc65a41f86c007',BASE,CAND):
 assert subprocess.run(['git','merge-base','--is-ancestor',s,'gauntlet/cp-26'],cwd=LEAD).returncode==0
before=json.loads((OUT/'untracked-before.json').read_text());after={}
for path,old in before.items():
 p=LEAD/path;assert p.is_file();new={'sha256':sha(p),'bytes':p.stat().st_size};assert old==new,path;after[path]=new
scope['untracked_preservation']={'files':len(after),'bytes':sum(x['bytes'] for x in after.values()),'manifest_sha256':sha(OUT/'untracked-before.json'),'all_sha256_and_sizes_unchanged':True,'groups':git('status','--porcelain=v1').splitlines()}
copy=json.loads((OUT/'prepared/copy.json').read_text())
assert git('diff','--name-only',cwd=OUT/'prepared/curated')==''
assert git('write-tree',cwd=OUT/'prepared/curated').strip()==copy['tree']
scope['curated_worktree_after']={'index_tree':copy['tree'],'unstaged_changes':[]}

ledger=json.loads((ROOT/'.local/artifacts/cp-26/ledger/budget.json').read_text())
sys.path.insert(0,str(CLEAN/'src'))
from cp26.budget import resource_summary
assert r['ledger_after']['jobs']==len(ledger['jobs'])
assert abs(r['ledger_after']['total_seconds']-resource_summary(ledger)['total_seconds'])<0.001
assert r['ledger_after']['running']==[] and not any(j['running'] for j in ledger['jobs'])
start=r['ledger_before']['jobs'];jobs=ledger['jobs'][start:]
assert len(jobs)==11 and all(not j['running'] for j in jobs)
assert [j['name'] for j in jobs if j['exit_code']!=0]==['landing-repair-3-ci3.12','landing-repair-3-ci3.13']
r['ledger_jobs']=[{k:j.get(k) for k in ('name','job_index','workers','wall_seconds','charged_wall_seconds','exit_code','abort_reason','running','completion_clock')} for j in jobs]
for offset,job in enumerate(r['ledger_jobs']): job['job_index']=start+offset
r['ledger_delta_seconds']=r['ledger_after']['total_seconds']-r['ledger_before']['total_seconds']
assert abs(r['ledger_delta_seconds']-sum(j['wall_seconds']*j['workers'] for j in jobs))<0.01
r['burners']=json.loads((OUT/'burners.json').read_text());assert not r['burners']['alive_after_stop']
r['historical_monitor_overhead_cores']=0.6
r['monitor_overhead_provenance']='Round 2 measurement; not remeasured in round 3. Four burners plus this independently enforced monitor.'
r['candidate_checkout_clean_after']=True
r['candidate_checkout_detached_after']=True
r['candidate_checkout_head_after']=git('rev-parse','HEAD',cwd=CLEAN).strip()
r['worktree_receipt_before_cleanup']=git('worktree','list','--porcelain')
r['history_free']=copy;r['checks']=records;r['preservation']=scope
r['scratch_branch_heads']={name:records[label]['copy_head'] for name,label in [('copy312/main','ci3.12'),('copy313/main','ci3.13')]}
for label,patterns in [('cp26-four',['tests/test_cp26_*.py','tests/test_rebaseline_disclosures.py']),('hook-boundary',['tests/test_47_session_start_hook.py'])]:
 import glob
 selected=sorted({p for pattern in patterns for p in glob.glob(pattern,root_dir=OUT/'prepared/copy312')})
 records[label]['expanded_selection']=selected
 records[label]['exact_pytest_command']=['uv','run','pytest','-q','-p','no:cacheprovider','-rfE',*selected]
r['section247_hashes']=json.loads((OUT/'section247-preservation.json').read_text())
(DEST/'verification.json').write_text(json.dumps(r,indent=2)+'\n')
shutil.copy2(OUT/'run.py',DEST/'run.py')
shutil.copy2(OUT/'resume.py',DEST/'resume.py')
shutil.copy2(OUT/'resume2.py',DEST/'resume2.py')
shutil.copy2(OUT/'sync313.py',DEST/'sync313.py')
shutil.copy2(OUT/'collect.py',DEST/'collect.py')
shutil.copy2(OUT/'write_return.py',DEST/'write_return.py')
r['section247_hashes']=json.loads((OUT/'section247-preservation.json').read_text())
shutil.copy2(OUT/'prepared/curated-paths.txt',DEST/'candidate-curated-paths.txt')
logs=DEST/'logs';logs.mkdir(exist_ok=True)
for p in sorted((OUT/'results').glob('*.log')):shutil.copy2(p,logs/p.name)
for name in ('curated','full'):
 for p in sorted((OUT/f'{name}-suite').glob('*.log')):shutil.copy2(p,logs/(name+'-'+p.name))
for p in sorted(OUT.glob('*-outer.log')):shutil.copy2(p,logs/p.name)
# Explicitly inherited, unchanged scientific clause evidence; no scientific rerun is claimed.
source=(CLEAN/'docs/track-b/evidence/cp-26/gfs-v21-r17/integration-r17-PASS.md').read_text()
rows=[line for line in source.splitlines() if re.match(r'^\| \d+ — ',line)]
assert len(rows)==111
assert [int(re.match(r'^\| (\d+)',x).group(1)) for x in rows]==list(range(1,112))
rows=[x.replace('**Now:** R1/R2;','**Current round-3 preservation:** verification.json; **Inherited r17 preservation:** R1/R2;') for x in rows]
rows=[x.replace('**Now:**', '**Current round-3 preservation:** verification.json; **Inherited r17 preservation:**') for x in rows]
assert not any('**Now:**' in x for x in rows)
maptext=source.split('## Exact preserved evidence map',1)[1].split('\n## ',1)[0]
maptext=maptext.replace('Each path below was checked to exist in this candidate or its indexed local root.', 'Historical r17 statement: each path below was checked in the r17 candidate or its indexed local root.').replace('R1 independently proves unchanged tracked bytes; R2 covers indexed payload availability/size and selected current hashes.', 'In that historical review, R1 proved unchanged tracked bytes and R2 covered indexed payload availability/size and selected hashes. These custody checks are inherited here.')
(DEST/'inherited-checklist.md').write_text('# CP-26 — all 111 inherited scientific clauses\n\nThe scientific PASS at 6f57feb and r17 preservation PASS at f014e5b are retained, not reissued. This round runs no scientific computation. Current tracked-byte, anchor and verdict checks are in verification.json. R1/R2 and R16 below denote the preserved r17 and scientific reviews, not checks rerun by this Lead. The clause text and prior evidence are copied from the immutable r17 PASS.\n\n## Preserved evidence map\n'+maptext+'\n\n## Complete §24.7 checklist\n\n| # | Checklist item | Status | Direct evidence |\n|---|---|---|---|\n'+'\n'.join(rows)+'\n')
print(json.dumps({'tree':copy['tree'],'tree_files':copy['tree_files'],'new_ledger_jobs':len(jobs),'charged_machine_hours':r['ledger_delta_seconds']/3600,'untracked_files':len(after),'checks':{k:v.get('green',v.get('passed',v.get('run',{}).get('summary'))) for k,v in records.items()}}))
