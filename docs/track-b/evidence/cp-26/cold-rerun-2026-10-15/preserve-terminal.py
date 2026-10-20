"""Preserve this cold attempt's receipts and verify custody, without repackaging the old run."""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp26.budget import Budget, atomic, resource_summary, scientific_run_summary
from cp26.gates import RUN_ID, RUN_EVIDENCE, OUTPUT, code_identity, protocol_identity
from cp26.supervisor import completion_receipt, identity_status

budget = Budget()
state = budget.read()
if any(j['running'] for j in state['jobs']):
    raise RuntimeError('terminal preservation requires no running job')
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
evidence = ROOT / RUN_EVIDENCE
namespace = json.loads((evidence / 'namespace-and-population.json').read_text())
for name, expected in namespace['old_hashes'].items():
    if sha(ROOT / name) != expected:
        raise RuntimeError('historical scientific artifact changed: ' + name)
if subprocess.check_output(['git', '-C', '/Users/djourno/Downloads/PJM', 'status', '--porcelain=v1']).strip():
    raise RuntimeError('primary tracked checkout is not clean')
if subprocess.check_output(['git', '-C', '/Users/djourno/Downloads/PJM', 'rev-parse', 'HEAD'], text=True).strip() != \
        '647d6eb81b2cf6e0cfaf4152f659d689ff973578':
    raise RuntimeError('main changed')
jobs = []
for job in state['jobs']:
    if job.get('run_id') != RUN_ID:
        continue
    receipt = completion_receipt(job)
    if not receipt.get('workers_stopped') or not receipt.get('group_empty'):
        raise RuntimeError('cold job lacks a complete ending receipt')
    alive = [role for role in ('monitor', 'supervisor', 'watchdog', 'child')
             if identity_status(job.get(role + '_identity')) not in ('gone', 'reused')]
    if alive:
        raise RuntimeError('cold job ownership still live or uncertain: ' + job['name'])
    destination = evidence / 'runs' / job['name']
    destination.mkdir(parents=True, exist_ok=True)
    sources = [job['request'], job['completion_clock'], job['progress_clock'], job['log'],
               str(Path(job['request']).parent / (job['name'] + '.json'))]
    copied = []
    for source in sources:
        source = Path(source)
        if source.exists():
            target = destination / source.name
            if target.exists() and sha(target) != sha(source):
                raise RuntimeError('preserved cold receipt changed')
            if not target.exists():
                shutil.copy2(source, target)
            copied.append({'path': str(target.relative_to(ROOT)), 'sha256': sha(target)})
    jobs.append({'name': job['name'], 'job_id': job['job_id'], 'workers': job['workers'],
                 'wall_seconds': job['wall_seconds'], 'exit_code': job['exit_code'],
                 'abort_reason': job['abort_reason'], 'receipt_files': copied})
local = Path(namespace['local'])
for source in sorted(local.glob('*.launch*.json')) + sorted(local.glob('*.launcher.log')):
    target = evidence / 'launchers' / source.name
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(source, target)
for name in ('preparation-tests.log',):
    source = local / name
    if source.exists():
        shutil.copy2(source, evidence / name)
probes = [{'path': str(p.relative_to(ROOT)), 'sha256': sha(p)}
          for p in sorted((ROOT / OUTPUT / 'timing-pilot').glob('*/*/*.json'))]
atomic(evidence / 'terminal-custody.json', {
    'run_id': RUN_ID, 'jobs': jobs, 'running_jobs': [], 'unknown_or_live_owned_processes': [],
    'historical_hashes_verified': namespace['old_hashes'], 'fresh_timing_probes': probes,
    'fresh_probe_count': len(probes), 'required_probes': 1064,
    'new_search_results': len(list((ROOT / OUTPUT / 'search-results').glob('*/*.json'))),
    'new_forecast_origins': len(list((ROOT / OUTPUT / 'forecast-ledger').glob('*.json'))),
    'primary_main_unchanged': True, 'branches_worktrees_tags_created': [],
    'retained_local': str(local), 'code_sha256': code_identity(ROOT), 'protocol': protocol_identity(ROOT)})
atomic(evidence / 'resources.json', {'authoritative_ledger': str(budget.path),
    'ledger_sha256_at_snapshot': sha(budget.path), 'historical_baseline': state['scientific_runs'][RUN_ID]['cumulative_baseline'],
    'new_run': scientific_run_summary(state, RUN_ID), 'cumulative_cp26': resource_summary(state),
    'closed_repair_seconds': state['repair_scope']['terminal_snapshot']['repair_seconds_used'],
    'historical_reserved_seconds': 2826.0, 'snapshot_is_not_a_second_account': True})
print(json.dumps({'cold_jobs_preserved': len(jobs), 'fresh_probes_preserved': len(probes),
                  'old_scientific_hashes_verified': len(namespace['old_hashes']), 'running': 0,
                  'new_run': scientific_run_summary(state, RUN_ID), 'cumulative_hours': resource_summary(state)['machine_hours']}))
