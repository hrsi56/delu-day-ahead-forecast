"""Carry forward the complete sealed estimate under r16; no timing or model reruns."""
from pathlib import Path
import copy
import hashlib
import json
import os
import sys
import time

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp26 import budget as B, costing as C, execution as E, gates as G, harness as H

assert os.environ.get('CP26_RUN_ID') == G.RUN_ID
G.authorize_consuming_process(ROOT)
gate = G.ExecutionGate(ROOT)
gate('pilot')
output = ROOT / G.OUTPUT
prior_path = output / 'cost-projection.json'
prior_raw = prior_path.read_bytes()
prior = json.loads(prior_raw)
C._verify(prior, C.SCHEMA)
custody = json.loads((ROOT / G.RUN_EVIDENCE / 'terminal-custody-v21-r15.json').read_bytes())
assert len(custody['fresh_timing_probes']) == 1064
assert all(hashlib.sha256((ROOT / row['path']).read_bytes()).hexdigest() == row['sha256']
           for row in custody['fresh_timing_probes'])
pilot = E._read(output / 'timing-pilot.json')
assert len(pilot['probes']) == 1064 and len(pilot['summary']) == 42
assert prior['pilot_sha256'] == E.digest(pilot)
protocol = G.protocol_identity(ROOT)
assert protocol == prior['protocol']
b = B.Budget()
state = b.read()
current = B.projected_cost(state, prior['searches'], prior['remaining'], run_id=G.RUN_ID)
projection = copy.deepcopy(prior)
projection.pop('content_sha256')
projection.update(current)
projection.update(code_sha256=G.code_identity(ROOT), operational_lineage=H.runtime_lineage(ROOT),
                  ledger_seconds_at_pricing=B.total_seconds(state), ledger_sha256_at_pricing=E.digest(state),
                  carried_forward_from={'path': str(prior_path.relative_to(ROOT)),
                      'sha256': hashlib.sha256(prior_raw).hexdigest(),
                      'content_sha256': prior['content_sha256'],
                      'estimates_and_margins_unchanged': True,
                      'basis': 'All42 cold searches,2441 origins/three routes,controls,replay,state growth,'
                              'analysis,diagnostics,review,closure and failure allowance retained. '
                              'R16 completed transition/checks are in live charges once. Remaining '
                              'startup/supervision1.124366h,tail0.512h,packaging300s and review/closure1h '
                              'remain future allowances; no additional unpriced material work.'})
projection = C._signed(projection)
C.persist_projection(ROOT, projection, output=G.OUTPUT / G.PROJECTION_NAME)
prior_admission = json.loads((ROOT / G.RUN_EVIDENCE / 'admission-v21-r15.json').read_bytes())
remaining = (current['remaining_search_seconds'] + current['remaining_other_seconds']) / 3600
record = E._signed({'schema': 'cp26-admission-v21-r16', 'run_id': G.RUN_ID,
    'observed_epoch': time.time(), 'admission': 'PASS' if current['within_pilot_stop'] else 'BLOCKED',
    'projection_gate_hours': 440, 'general_admission_hours': 436.5, 'actual_ceiling_hours': 500,
    'current_cumulative': B.resource_summary(state), 'current_new_run': B.scientific_run_summary(state, G.RUN_ID),
    'historical_baseline_hours': 65.16212464012295,
    'complete_conservative_cumulative_hours': current['projected_total_hours'],
    'complete_new_run_estimate_hours': B.scientific_run_summary(state, G.RUN_ID)['machine_hours'] + remaining,
    'remaining_hours': remaining,
    'remaining_components_seconds': {'all42_cold_searches': current['remaining_search_seconds'],
                                   **{k: v['machine_seconds'] for k, v in prior['remaining'].items()}},
    'cost_projection': str(G.OUTPUT / G.PROJECTION_NAME), 'projection_sha256': projection['content_sha256'],
    'pilot_probes_preserved': 1064, 'fresh_pilot': False, 'full_scientific_workload_started': False,
    'maximum_compute_workers': 4,
    'expected_remaining_wall_hours_at_chosen_concurrency': prior_admission['expected_remaining_wall_hours_at_chosen_concurrency'],
    'expected_concurrency_basis': prior_admission['expected_concurrency_basis'],
    'wall_forecast_components_hours': prior_admission['wall_forecast_components_hours'],
    'prior_rejected_admission': str(G.RUN_EVIDENCE / 'terminal-admission-recheck-v21-r15.json'),
    'operational_lineage': H.runtime_lineage(ROOT), 'protocol': protocol,
    'post_pricing_guard': 'Reprice against live charges before dispatch; retain all caps and shutdown headroom.'})
B.atomic(ROOT / G.RUN_EVIDENCE / 'admission-v21-r16.json', record)
assert prior_path.read_bytes() == prior_raw
C.require_projection(projection, b.read())
print(json.dumps({k: record[k] for k in ('admission', 'complete_conservative_cumulative_hours',
                 'complete_new_run_estimate_hours', 'expected_remaining_wall_hours_at_chosen_concurrency')}), flush=True)
