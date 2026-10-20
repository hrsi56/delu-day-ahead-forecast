"""Retain the complete existing forecast and add bounded new monitor setup."""
import copy
import hashlib
import json
import os
from pathlib import Path
import sys
import time

from cp26 import budget as B, costing as C, execution as E, gates as G

root = Path.cwd()
assert os.environ.get('CP26_MONITORED_JOB') and os.environ.get('CP26_RUN_ID') == G.RUN_ID
label = sys.argv[1]
assert label in ('g05g06', 'g07g08', 'g09g10', 'closure')
directory = root / G.RUN_EVIDENCE
b = B.Budget()
if len(sys.argv) == 3:
    charge = json.loads(Path(sys.argv[2]).read_bytes())
    assert charge['source']['run_id'] == G.RUN_ID
    b.record_charge(charge['charge_id'], charge['seconds'], 'reported', charge['source'])
validation = E._read(directory / 'raw-kernel-ctime-validation-v21-r16.json')
assert validation['status'] == 'PASS' and validation['scientific_code_sha256'] == G.code_identity(root)
base_path = G.OUTPUT / f'cost-projection-state-growth-v21-r16-{label}-close.json'
base = E._read(root / base_path)
C._verify(base, C.SCHEMA)
remaining = copy.deepcopy(base['remaining'])
remaining['raw_kernel_birth_bootstrap_monitor_setup'] = {
    'classification': 'conservative', 'machine_seconds': 160.0,
    'basis': 'Sixty-four remaining monitor bootstraps at2.5seconds each, covering the '
             'normal finite native/replay/analysis/pricing/review calls with duplicate '
             'call contingency. Actual measured monitor setup was below0.012seconds. '
             'Only pre-reservation monitor setup is additional: supervisor/worker '
             'bootstrap time is already inside measured allocated worker wall time. '
             'Every previous fit, replay/state-growth, failure, operation, closing '
             'and review allowance is retained; no timing factor is reduced.',
    'maximum_remaining_calls': 64, 'seconds_per_call': 2.5,
    'maximum_observed_monitor_setup_seconds': validation['maximum_observed_monitor_setup_seconds']}
raw = b.path.read_bytes()
state = json.loads(raw)
priced = B.projected_cost(state, base['searches'], remaining, run_id=G.RUN_ID)
value = {k:v for k,v in copy.deepcopy(base).items() if k != 'content_sha256'}
value.update(priced)
value.update(remaining=remaining, ledger_seconds_at_pricing=B.total_seconds(state),
             ledger_sha256_at_pricing=hashlib.sha256(raw).hexdigest(),
             raw_birth_allowance_source={'path': str(base_path), 'content_sha256': base['content_sha256']},
             process_identity_clock_basis='darwin-raw-kernel-birth-v1',
             raw_birth_bootstrap_sha256=validation['bootstrap_sha256'],
             raw_birth_validation_sha256=validation['content_sha256'],
             pricing_job_id=os.environ['CP26_JOB_ID'], priced_epoch=time.time())
projection = C._signed(value)
path = G.OUTPUT / f'cost-projection-state-growth-v21-r16-{label}-close-raw-birth.json'
C.persist_projection(root, projection, output=path)
live = C.require_projection(projection, b.read())
run = B.scientific_run_summary(b.read(), G.RUN_ID)
prior = E._read(directory / f'admission-state-growth-v21-r16-{label}-close.json')
admission = E._signed({
    'run_id': G.RUN_ID, 'status': 'PASS', 'projection_path': str(path),
    'projection_sha256': projection['content_sha256'],
    'cumulative_actual_hours': live['machine_hours'], 'new_run_actual': run,
    'historical_baseline_hours': run['historical_baseline_hours'],
    'projected_cumulative_completion_hours': live['projected_total_hours'],
    'projected_new_run_completion_hours': live['projected_total_hours'] - run['historical_baseline_hours'],
    'component_hours': {k:v['machine_seconds']/3600 for k,v in remaining.items()},
    'remaining_wall_hours_three_native_workers': prior['remaining_wall_hours_three_native_workers'] + 160/3600,
    'admission_hours': 440.0, 'actual_hard_ceiling_hours': 500.0,
    'process_identity_clock_basis': 'darwin-raw-kernel-birth-v1',
    'raw_birth_bootstrap_sha256': validation['bootstrap_sha256'],
    'raw_birth_validation_sha256': validation['content_sha256'],
    'basis': 'Existing complete sealed-pilot/production-state-growth/closing forecast plus '
             'one bounded bootstrap component. Current actuals include the original65.16212464012295hour '
             'baseline, all failed work and all retained reserves once. Unissued native fit '
             'allowances remain conservative, including prefits; no completed-search price is restored. '
             'The original scientific sources, inputs, seeds and cache identities remain unchanged.'})
E._immutable(directory / f'admission-state-growth-v21-r16-{label}-close-raw-birth.json', admission)
print(json.dumps(admission), flush=True)
