"""Point-in-time completion pricing from existing production replay receipts.

No fit, new timing pilot, source/cache migration or resource charge is performed.
Always rebase from the original sealed projection, never a discounted update.
The unchanged execution gate remains necessary; this adds a stronger Lead check.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp26 import budget as B, costing as C, execution as E, gates as G

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('label')
args = parser.parse_args()
if not re.fullmatch(r'g\d{2}g\d{2}|closure', args.label):
    raise ValueError('unregistered completion-pricing label')
relative = str(Path(__file__).resolve().relative_to(ROOT))
if subprocess.check_output(['git', 'show', f'HEAD:{relative}']) != Path(__file__).read_bytes():
    raise RuntimeError('completion-pricing caller is not committed')
G.authorize_consuming_process(ROOT)
directory = ROOT / 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15'
output = ROOT / G.OUTPUT
reference_path = directory / 'state-growth-cost-reference-v21-r16.json'
b = B.Budget()
base = E._read(output / G.PROJECTION_NAME)
C._verify(base, C.SCHEMA)

if not reference_path.exists():
    completion = json.loads((directory / 'replay-g02-completion-v21-r16.json').read_bytes())
    clock_path = Path(completion['job']['completion_clock'])
    clock_raw = clock_path.read_bytes()
    clock = json.loads(clock_raw)
    assert hashlib.sha256(clock_raw).hexdigest() == completion['clock_sha256']
    assert clock['exit_code'] == 0 and clock['workers'] == 1 and clock['workers_stopped']
    assert completion['through'] == '2021-05-04' and completion['cache_only']
    # Byte counts/hashes only: the historical H/learning state is never loaded.
    state_path = output / 'replay-state.json'
    historical = ROOT / 'reports/rebaseline/continuation-v21-r14-accounting-3/replay-state.json'
    state_raw = state_path.read_bytes()
    ratio = max(1., (len(state_raw)/490) / (historical.stat().st_size/575))
    reference = E._signed({'schema': 'cp26-replay-growth-cost-reference-v1',
        'run_id': G.RUN_ID, 'clock_path': str(clock_path),
        'clock_sha256': completion['clock_sha256'], 'wall_seconds': clock['wall_seconds'],
        'new_origins': 245, 'minimum_state_origins': 245,
        'maximum_state_origins': 490, 'state_path_at_reference': str(state_path),
        'state_bytes_at_reference': len(state_raw),
        'state_raw_sha256_at_reference': hashlib.sha256(state_raw).hexdigest(),
        'historical_resource_only_bytes': historical.stat().st_size,
        'historical_resource_only_origins': 575, 'bytes_per_origin_ratio_floor_one': ratio,
        'margin': 1.5,
        'basis': 'Whole successful245-new-origin production replay clock, including '
                 'startup, prior-history validation, persistence and closing. Normalize '
                 'by its smallest245-origin state rather than its larger mean state. '
                 'Scale over every remaining state size and retain1.5x margin; '
                 'increase for observed bytes/origin growth, never decrease. No old state imported.'})
    E._immutable(reference_path, reference)
reference = E._read(reference_path)
assert reference['run_id'] == G.RUN_ID
assert hashlib.sha256(Path(reference['clock_path']).read_bytes()).hexdigest() == reference['clock_sha256']

searches, remaining = G.outstanding_projection(base, output, b.read())
completed = remaining['daily_fits'].get('completed_origins', 0)
total = remaining['daily_fits']['total_origins']
assert total == 2441 and 490 <= completed <= total
weighted_states = (completed + 1 + total) * (total - completed) / 2
growth_bound = (reference['wall_seconds'] * reference['margin']
                * reference['bytes_per_origin_ratio_floor_one'] * weighted_states
                / (reference['new_origins'] * reference['minimum_state_origins']))
original_replay = remaining['chronological_replay_persistence_exports']['machine_seconds']
remaining['measured_replay_state_growth_supplement'] = {
    'classification': 'conservative', 'machine_seconds': max(0., growth_bound-original_replay),
    'basis': 'Supplement only: original retained replay allowance plus this row equals '
             'at least the measured-production remaining-growth bound. All earlier work '
             'is already in cumulative charges; no remaining date at/before the completed '
             'prefix is priced again by the new growth calculation.',
    'reference_sha256': reference['content_sha256'], 'completed_origins': completed,
    'remaining_weighted_state_origins': weighted_states,
    'remaining_growth_bound_seconds': growth_bound}
assert remaining['failed_jobs_and_resume'] == base['remaining']['failed_jobs_and_resume']
raw = b.path.read_bytes()
state = json.loads(raw)
priced = B.projected_cost(state, searches, remaining, run_id=G.RUN_ID)
value = {k: v for k, v in copy.deepcopy(base).items() if k != 'content_sha256'}
value.update(priced)
value.update(searches=searches, remaining=remaining,
    ledger_seconds_at_pricing=B.total_seconds(state),
    ledger_sha256_at_pricing=hashlib.sha256(raw).hexdigest(),
    repricing_source={'path': str(output / G.PROJECTION_NAME), 'sha256': base['content_sha256']},
    point_in_time_remaining_estimates=True,
    reprice_instruction='Always regenerate from repricing_source; never discount this snapshot again.',
    growth_cost_reference_sha256=reference['content_sha256'],
    pricing_job_id=os.environ.get('CP26_JOB_ID'), priced_epoch=time.time())
projection = C._signed(value)
projection_path = G.OUTPUT / f'cost-projection-state-growth-v21-r16-{args.label}.json'
C.persist_projection(ROOT, projection, output=projection_path)
current = B.projected_cost(b.read(), searches, remaining, run_id=G.RUN_ID)
run = B.scientific_run_summary(b.read(), G.RUN_ID)
fraction = (total-completed)/total
routes = {row['run']: row['machine_seconds']*fraction/3600
          for row in base['remaining']['daily_fits']['route_costs']}
serial_other = sum(row['machine_seconds'] for key, row in remaining.items()
                   if key not in ('daily_fits', 'chronological_replay_persistence_exports',
                                  'measured_replay_state_growth_supplement'))/3600
replay_hours = max(original_replay, growth_bound)/3600
admission = E._signed({'schema': 'cp26-completion-admission-update-v1', 'run_id': G.RUN_ID,
    'status': 'PASS' if current['within_pilot_stop'] else 'BLOCKED',
    'projection_path': str(projection_path), 'projection_sha256': projection['content_sha256'],
    'cumulative_actual_hours': current['machine_hours'], 'new_run_actual': run,
    'historical_baseline_hours': run['historical_baseline_hours'],
    'projected_cumulative_completion_hours': current['projected_total_hours'],
    'projected_new_run_completion_hours': run['machine_hours']
        + (current['remaining_search_seconds']+current['remaining_other_seconds'])/3600,
    'component_hours': {key: row['machine_seconds']/3600 for key, row in remaining.items()},
    'remaining_cold_search_hours': current['remaining_search_seconds']/3600,
    'remaining_wall_hours_four_native_workers': max(routes['nominal']/2, routes['noload'], routes['gfs6'])
        + replay_hours + serial_other,
    'remaining_wall_hours_three_native_worker_fallback': max(routes.values())+replay_hours+serial_other,
    'wall_basis': 'Existing route pilot maxima/margins; four independent native workers '
                  '(two disjoint nominal windows), then exclusive one-worker replay and serial '
                  'analysis. All failure/operational/closure allowances treated serially; '
                  'three-worker fallback retained. No speedup is needed for machine-hour admission.',
    'admission_hours': 440., 'actual_hard_ceiling_hours': 500.,
    'history': 'Original sealed pilot/initial439.821h admission and all rejected records unchanged. '
               'All base margins retained; new production evidence only increases the replay bound. '
               'This is a forecast using the existing ledger/calculator, not another resource account.'})
E._immutable(directory / f'admission-state-growth-v21-r16-{args.label}.json', admission)
C.require_projection(projection, b.read())
print(json.dumps(admission), flush=True)
