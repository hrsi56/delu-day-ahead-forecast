"""Retain complete CP-26 prices under the narrower two-native allocation."""
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time

from cp26 import budget as B, costing as C, execution as E, gates as G

root = Path.cwd()
assert os.environ.get('CP26_MONITORED_JOB') and os.environ.get('CP26_RUN_ID') == G.RUN_ID
label = sys.argv[1]
assert label in ('g05g06', 'g07g08', 'g09g10', 'closure') and len(sys.argv) in (2, 3)
d = root / G.RUN_EVIDENCE
policy = E._read(d / 'two-native-allocation-v21-r16.json')
assert policy['native_workers'] == 2 and policy['canonical_accounting_max_native_workers'] == 1
b = B.Budget()
if len(sys.argv) == 3:
    charge = json.loads(Path(sys.argv[2]).read_bytes())
    assert charge['source']['run_id'] == G.RUN_ID
    b.record_charge(charge['charge_id'], charge['seconds'], 'reported', charge['source'])
    E._immutable(d / 'observation-batch-v21-r16-49.json', E._signed(charge))
base_path = G.OUTPUT / f'cost-projection-state-growth-v21-r16-{label}-close-raw-birth.json'
base = E._read(root / base_path)
C._verify(base, C.SCHEMA)
check = E._read(d / 'raw-kernel-ctime-validation-v21-r16.json')
assert check['scientific_code_sha256'] == G.code_identity(root)
stop = E._read(d / 'native-g07g08-gfs6-deadline-stop-v21-r16.json')
prior = E._read(d / 'native-g07-nominal-completion-v21-r16.json')
assert prior['saved_complete_dates'] == 209
reference_seconds = prior['wall_seconds'] * (stop['preserved_ready_dates'] + len(stop['partial_dates'])) / 209
assert reference_seconds < 5400.0
remaining = copy.deepcopy(base['remaining'])
completion_path = d / 'native-g07g08-gfs6-completion-v21-r16.json'
completion = E._read(completion_path) if completion_path.exists() else None
if completion:
    from cp26.supervisor import check_completion, completion_receipt
    state = b.read()
    job = state['jobs'][completion['job']['job_index']]
    assert job['job_id'] == completion['job']['job_id'] and not job['running']
    clock = completion_receipt(job)
    check_completion(job, clock)
    assert clock['exit_code'] == 0 and not clock['abort_reason']
    assert hashlib.sha256(Path(job['completion_clock']).read_bytes()).hexdigest() == completion['clock_sha256']
    assert completion['native_origins'] == 490 and completion['total_native_origins'] == 1960
remaining['same_window_restart_cache_validation'] = {
    'classification': 'conservative', 'machine_seconds': 0.0 if completion else 5400.0,
    'basis': 'Additional90minutes for this same-window restart. The entire prior3049.3918679169146second '
             '209-saved-date plus36-new-date nominal resumption, including all fresh fitting, '
             'is conservatively scaled to358 saved/partial dates. This is below5400seconds. '
             'The five-member control has fewer cached members per date than that nine-member '
             'reference. Forecast/H state remains at the same980-origin prefix. All original '
             'fit, replay, failure, operation, review, closing and bootstrap margins remain. '
             'Remove only after the complete resumed native phase has a positive bound clock.',
    'reference_whole_job_seconds': prior['wall_seconds'], 'reference_cached_dates': 209,
    'new_saved_or_partial_dates': stop['preserved_ready_dates'] + len(stop['partial_dates']),
    'scaled_whole_job_seconds': reference_seconds, 'stop_evidence_sha256': stop['content_sha256'],
    'completed_evidence': completion['content_sha256'] if completion else None}
raw = b.path.read_bytes()
state = json.loads(raw)
priced = B.projected_cost(state, base['searches'], remaining, run_id=G.RUN_ID)
value = {k:v for k,v in copy.deepcopy(base).items() if k != 'content_sha256'}
value.update(priced)
value.update(remaining=remaining, ledger_seconds_at_pricing=B.total_seconds(state),
             ledger_sha256_at_pricing=hashlib.sha256(raw).hexdigest(),
             two_native_source={'path': str(base_path), 'sha256': base['content_sha256']},
             execution_allocation_sha256=policy['content_sha256'],
             native_workers=2, canonical_accounting_max_native_workers=1,
             pricing_job_id=os.environ['CP26_JOB_ID'], priced_epoch=time.time())
projection = C._signed(value)
path = G.OUTPUT / f'cost-projection-state-growth-v21-r16-{label}-close-raw-birth-two-native.json'
C.persist_projection(root, projection, output=path)
live = C.require_projection(projection, b.read())
run = B.scientific_run_summary(b.read(), G.RUN_ID)
total_remaining_h = (live['remaining_search_seconds'] + live['remaining_other_seconds']) / 3600
daily = remaining['daily_fits']
fraction = (daily['total_origins'] - daily.get('completed_origins', 0)) / daily['total_origins']
route_hours = {row['run']: row['machine_seconds'] * fraction / 3600
               for row in daily['route_costs']}
native_hours = daily['machine_seconds'] / 3600
assert math.isclose(sum(route_hours.values()), native_hours, rel_tol=1e-10, abs_tol=1e-10)
# At most two remaining native waves, separated by the1960-origin replay.
# For two work-conserving workers, each wave's makespan is at most half
# its total plus half its largest task. The sum of the two largest tasks
# is bounded by the two largest route budgets, including a repeated route.
two_native_wall = (total_remaining_h - native_hours + native_hours / 2
                   + sum(sorted(route_hours.values(), reverse=True)[:2]) / 2)
admission = E._signed({
    'run_id': G.RUN_ID, 'status': 'PASS', 'projection_path': str(path),
    'projection_sha256': projection['content_sha256'], 'new_run_actual': run,
    'historical_baseline_hours': run['historical_baseline_hours'],
    'cumulative_actual_hours': live['machine_hours'],
    'projected_cumulative_completion_hours': live['projected_total_hours'],
    'projected_new_run_completion_hours': run['machine_hours'] + total_remaining_h,
    'component_hours': {k:v['machine_seconds']/3600 for k,v in remaining.items()},
    'remaining_cold_search_hours': live['remaining_search_seconds']/3600,
    'remaining_wall_hours_two_native_workers': two_native_wall,
    'remaining_native_route_upper_hours': route_hours,
    'remaining_wall_hours_conservative_serial_envelope': total_remaining_h,
    'wall_basis': 'Two independent one-worker native jobs, with no uncharged coordinator. '
                  'Canonical accounting only with at most one native fit; replay/analysis exclusive. '
                  'Two native waves use the list-scheduling bound: total-native/2 plus '
                  'the two largest route budgets/2. Treat all other work and allowances '
                  'serially. Also retain the complete machine-hour envelope as a serial '
                  'wall ceiling if concurrency must fall to one. No speedup is required '
                  'for machine-hour admission; measured throughput is retained separately.',
    'native_workers': 2, 'canonical_accounting_max_native_workers': 1,
    'admission_hours': 440.0, 'actual_hard_ceiling_hours': 500.0,
    'execution_allocation_sha256': policy['content_sha256'],
    'basis': 'All current actual charges, including the stopped GFS job, are included once. '
             'Every previous margin is retained. The additional future restart allowance '
             'does not alter historical charges, receipts, original admission or scientific rules.'})
E._immutable(d / f'admission-state-growth-v21-r16-{label}-close-raw-birth-two-native.json', admission)
print(json.dumps(admission), flush=True)
