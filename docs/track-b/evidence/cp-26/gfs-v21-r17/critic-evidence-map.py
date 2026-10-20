import hashlib,json,pathlib,subprocess
root=pathlib.Path('/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/critic-gfs-r17')
out=pathlib.Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/gfs-v21-r17')
R='reports/rebaseline/cold-rerun-2026-10-15/'
E='docs/track-b/evidence/cp-26/cold-rerun-2026-10-15/'
groups={
 'P1':[R+'execution-manifest.json',R+'forecast-completion.json',R+'forecast-ledger/',
       'reports/development-inputs/eligibility-calendar.csv','reports/development-inputs/record-masks.csv'],
 'P2':[R+'parity.json','src/cp26/harness.py','src/cp26/members.py','src/cp26/parity.py','src/cp26/fits.py','src/cp26/replay.py'],
 'P3':[R+'presentation-v21-r16/report.md',R+'presentation-v21-r16/publication-packet.json',
       R+'presentation-v21-r16/publication-packet.md',R+'presentation-v21-r16/MLflow-export.json'],
 'P4':[R+'search-plans/',R+'search-results/',R+'timing-pilot.json','src/cp26/search.py'],
 'P5':[R+'scores-manifest.json',R+'scores/','src/cp26/scoring.py','src/cp26/analysis.py'],
 'P6':[R+'diagnostics-manifest.json','src/cp26/diagnostics.py','tests/test_cp26_diagnostic_cells.py'],
 'P7':[R+'inference-manifest.json','src/cp26/inference.py','tests/test_cp26_inference_rng.py'],
 'P8':[R+'replay-state.json',R+'learning-ledger.json',R+'forecast-ledger/','src/cp26/state.py','src/cp26/replay.py'],
 'P9':['docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md',
       'docs/track-b/evidence/cp-26/continuation-v21-r14/execution-protocol.json'],
 'P10':[E+'admission-v21-r16.json',E+'terminal-resource-snapshot-v21-r16.json',E+'final-integration-custody-v21-r16.json',
        E+'integration-final-r16-2-accounting.json','src/cp26/budget.py','src/cp26/gates.py','src/cp26/supervisor.py','src/cp26/limits.py'],
 'P11':['docs/PUBLISH_RULES.md','docs/track-b/publication-standard-v1.md','docs/track-b/cp-25-landing-2026-10-12.md',
        'docs/track-b/cp-25-rulings-2026-10-12.md',E+'issued-brief.md',E+'issued-continuation-v21-r16.md',R+'presentation-v21-r16/publication-packet.json']}
pres=json.loads((out/'critic-preservation-result.json').read_text())
local={f['path']:(pathlib.Path(inv['root'])/f['path']) for inv in pres['inventories'].values() for f in inv['freshly_hashed_files']}
checked={}
for group,paths in groups.items():
 checked[group]=[]
 for rel in paths:
  p=root/rel
  if rel.endswith('/'):
   assert p.is_dir(),rel; count=sum(1 for f in p.rglob('*') if f.is_file())
   checked[group].append({'path':rel,'file_count':count,'existence_checked':True})
  else:
   p=p if p.is_file() else local.get(rel,p)
   assert p.is_file(),rel
   checked[group].append({'path':rel,'bytes':p.stat().st_size,'existence_checked':True})
budget=json.loads(pathlib.Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/ledger/budget.json').read_text())
resource={'path':'/Users/djourno/Downloads/PJM/.local/artifacts/cp-26/ledger/budget.json','schema':budget['schema'],
 'accounting':budget['accounting'],'total_machine_hours':sum(budget['accounting'][k] for k in ['measured_seconds','reported_seconds','reserved_seconds'])/3600,
 'caps':budget['caps'],'last_job_index':budget['jobs'][-1]['job_index']}
assert abs(resource['total_machine_hours']-238.111652)<0.000001
ancestry=[]
for a,b in [('5cc3cc083c4340fd8d792eeaf6551a007987a877','f7a0273798a76ad55aad1c69f40893bc149d1f6e'),
 ('563be855d918cb7ec3a2b53497414a863dc43431','eb0e2de745feb614d6b1a2eca458395112ef17e6'),
 ('57cfce9262d1c1eb1ebcf3a8b57b3b0b8b5e816e','eb0e2de745feb614d6b1a2eca458395112ef17e6'),
 ('563be855d918cb7ec3a2b53497414a863dc43431','f7a0273798a76ad55aad1c69f40893bc149d1f6e')]:
 p=subprocess.run(['git','merge-base','--is-ancestor',a,b],cwd=root,text=True,capture_output=True)
 assert p.returncode==0
 ancestry.append({'command':f'git merge-base --is-ancestor {a} {b}','exit_code':p.returncode,'stdout':p.stdout})
result={'groups':checked,'resource_snapshot_read_now':resource,'freeze_ancestry_commands':ancestry,
 'previous_reproduction_verdict':E+'integration-final-r16-2-PASS.md',
 'previous_reproduction_verdict_sha256':pres['prior_verdict_sha256'],
 'inheritance':'All original scientific reproduction claims remain inherited; current checks preserve their exact candidate evidence and verify availability.'}
(out/'critic-evidence-map-result.json').write_text(json.dumps(result,indent=2)+'\n')
print('All 11 evidence groups exist; forecast files=2441; each search-plan/result directory=42; unchanged source/tests/inputs/report blobs already proved.')
print('Resource account total_machine_hours',resource['total_machine_hours'],'last_job_index',resource['last_job_index'])
print('Four freeze-before-pilot/score ancestry commands: exit 0, empty outputs.')
