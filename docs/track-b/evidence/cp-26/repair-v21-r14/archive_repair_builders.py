from pathlib import Path
import hashlib,json,shutil,subprocess,time
root=Path('/Users/djourno/Downloads/PJM')
packet=root/'.local/artifacts/cp-26/repair-v21-r14/builders'
owned={
 'repair-search':['src/cp26/search.py','scripts/cp26_search_support.py','tests/test_cp26_search.py'],
 'repair-state':['src/cp26/state.py','src/cp26/replay.py','src/cp26/fits.py','tests/test_cp26_state.py','tests/test_cp26_replay.py'],
 'repair-budget':['src/cp26/budget.py','src/cp26/supervisor.py','scripts/cp26_rebaseline.py','tests/test_cp26_monitor.py']}
prior=json.loads((packet/'inventory.json').read_text()) if (packet/'inventory.json').exists() else {'worktrees':[]}
rows={row['purpose']:row for row in prior['worktrees']}
for name,paths in owned.items():
 source=root/'.local/worktrees/cp-26'/name
 if not source.exists(): continue
 dest=packet/name
 row={'path':str(source),'seed_sha':'5cc3cc083c4340fd8d792eeaf6551a007987a877','purpose':name,'files':{}}
 for relative in paths:
  p=source/relative; q=dest/relative; q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
  row['files'][relative]={'builder_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
    'lead_sha256':hashlib.sha256((root/'.local/worktrees/cp-26/lead'/relative).read_bytes()).hexdigest()}
 row['status_before_removal']=subprocess.check_output(['git','status','--porcelain=v1'],cwd=source,text=True)
 row['recovery_packet']=str(dest)
 rows[name]=row
(packet/'inventory.json').write_text(json.dumps({'worktrees':list(rows.values())},indent=2)+'\n')
print(json.dumps({'preserved_builder_packets':len(rows),'recovery_root':str(packet)}))
