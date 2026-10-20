"""Complete forecast from the retained full pilot, preserving all rejected forecasts."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp26 import execution as E, costing as C, harness as H
from cp26.budget import Budget, atomic, resource_summary, scientific_run_summary
from cp26.gates import OUTPUT, RUN_ID, RUN_EVIDENCE, code_identity, protocol_identity

if os.environ.get('CP26_RUN_ID') != RUN_ID or not os.environ.get('CP26_MONITORED_JOB'):
    raise RuntimeError('registered resource accounting required')
old = ROOT / 'reports/rebaseline/continuation-v21-r14-accounting-3'
output = ROOT / OUTPUT
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
old_pilot = E._read(old / 'timing-pilot.json')
benchmark = E._read(old / 'fixture-benchmark.json')
coverage_path = ROOT / RUN_EVIDENCE / 'historical-timing-coverage.json'
coverage = json.loads(coverage_path.read_text())
if not coverage['all42_complete_fit_timing_coverage'] or len(coverage['searches']) != 42:
    raise RuntimeError('incomplete historical cold-search resource coverage')
for row in coverage['searches']:
    for path, expected in row['model_code_sha256'].items():
        if path == 'src/cp26/search.py':
            original = subprocess.check_output(['git', 'show', f'7b11c8cea6f0815a2034000325076238024f4122:{path}'])
            if hashlib.sha256(original).hexdigest() != expected:
                raise RuntimeError('historical search implementation differs')
            namespaced = original.replace(b"    return {'protocol': PROTOCOL, 'k': k, 'route': _route(route),",
                b"    from .gates import RUN_ID\n    return {'protocol': PROTOCOL, 'run_id': RUN_ID, 'k': k, 'route': _route(route),")
            if hashlib.sha256(namespaced).hexdigest() != H.recipe_code_sha256(ROOT, path):
                raise RuntimeError('search timing reuse covers only the declared run-identity change')
        elif H.recipe_code_sha256(ROOT, path) != expected:
            raise RuntimeError('historical model timing no longer covers current code: ' + path)
for name in ('inference', 'diagnostics', 'scoring'):
    path = f'src/cp26/{name}.py'
    if sha(ROOT / path) != benchmark['code_sha256'][path]:
        raise RuntimeError('statistical algorithm changed')
original = subprocess.check_output(['git', 'show', '7b11c8cea6f0815a2034000325076238024f4122:src/cp26/analysis.py'])
namespaced = original.replace(b"OUTPUT = Path('reports/rebaseline/continuation-v21-r14-accounting-3')",
    b'from .gates import OUTPUT, LOCAL_NAME').replace(b"art() / 'continuation-v21-r14/analysis-recovery'",
    b"art() / LOCAL_NAME / 'analysis-recovery'")
if (hashlib.sha256(original).hexdigest() != benchmark['code_sha256']['src/cp26/analysis.py']
        or (ROOT / 'src/cp26/analysis.py').read_bytes() != namespaced):
    raise RuntimeError('analysis reuse covers only the two explicit namespace substitutions')
from cp26.budget import projected_cost
from cp26.gates import PROTOCOL
import copy

shared = protocol_identity(ROOT)
paths = E.Paths.build(ROOT)
pilot = E._read(output / 'timing-pilot.json')
plans = [E._read(paths.plan(r, k)) for r in E.ROUTES for k in range(14)]
manifest = E.manifest_for(paths, shared)
budget = Budget()
state = budget.read()
continuation = next(j for j in state['jobs'] if j['name'] == 'cold-r15-pilot-assembly-1')
if continuation['running'] or continuation['exit_code'] != 0 or continuation['abort_reason']:
    raise RuntimeError('no successful supervised single-worker pilot completion')
if len(pilot['probes']) != 1064 or len(pilot['summary']) != 42:
    raise RuntimeError('full retained pilot required')
authority = json.loads((ROOT / RUN_EVIDENCE / 'authority-v21-r15.json').read_text())
if not all(sha(ROOT / p) == expected for p, expected in authority['initial_probe_hashes'].items()):
    raise RuntimeError('pre-existing1013 probe bytes changed')
# This validates every raw probe, plan, sampler, seed, route, summary, and source
# identity using the existing complete costing implementation. It also retains
# the original maximum-probe search margin as a floor for the complete-history
# estimator below. No smaller price is chosen merely to meet admission.
standard = C.price_pilot(state, pilot, plans=plans, execution_manifest=manifest,
    protocol_bytes=(ROOT / PROTOCOL).read_bytes(), protocol=shared,
    code_sha256=code_identity(ROOT), additional_costs=benchmark['additional_costs'],
    recipe_code_sha256={name: H.recipe_code_sha256(ROOT, name) for name in ('src/cp26/harness.py', 'src/cp26/search.py')})
old_rows = {(r['route'], r['k']): r for r in old_pilot['summary']}
new_rows = {(r['route'], r['k']): r for r in pilot['summary']}
slowdowns = [{'route': r, 'k': k, 'ratio': sum(new_rows[r, k]['search_probe_wall_seconds']) /
             sum(old_rows[r, k]['search_probe_wall_seconds'])} for r in E.ROUTES for k in range(14)]
slowdown = max(1., max(row['ratio'] for row in slowdowns))
historical_jobs = [j for j in state['jobs'] if j.get('run_id') != RUN_ID and 'search' in j['name']
                  and not any(s in j['name'] for s in ('test', 'support', 'cost', 'pilot'))]
historical_seconds = sum(j.get('charged_wall_seconds', j.get('wall_seconds', 0)) * j['workers']
                         for j in historical_jobs)
raw_seconds = sum(r['total_recorded_fit_seconds'] for r in coverage['searches'])
overhead = max(1., historical_seconds / raw_seconds)
covered = {(r['route'], r['k']): r for r in coverage['searches']}
searches = copy.deepcopy(standard['searches'])
for row in searches:
    resource = covered[row['run'], row['k']]
    history_price = 2 * resource['total_recorded_fit_seconds'] * overhead * slowdown
    row['original_maximum_probe_price_seconds'] = row['machine_seconds']
    row['complete_historical_fit_price_seconds'] = history_price
    row['machine_seconds'] = max(row['machine_seconds'], history_price)
    row['basis'] += ('; also bounded below by2×complete all-batch historical fit resource time '
        '×all-attempt allocated overhead ×maximum whole12-probe fresh/historical slowdown; '
        'no resumed-tail runtime is used as a cold-search price')
    row['historical_resource'] = {k: resource[k] for k in ('source', 'sha256', 'fit_records', 'expected_fit_records')}
remaining = copy.deepcopy(standard['remaining'])
daily = remaining['daily_fits']
for row in daily['route_costs']:
    route = row['run']
    maximum = max([r['daily_wall_seconds'] for r in old_pilot['summary'] if r['route'] == route] +
                  [r['daily_wall_seconds'] for r in pilot['summary'] if r['route'] == route])
    row['maximum_old_or_fresh_origin_seconds'] = maximum
    row['machine_seconds'] = maximum * 2441 * 1.25
daily['machine_seconds'] = sum(r['machine_seconds'] for r in daily['route_costs'])
daily['basis'] = ('Maximum complete route/origin across all14 historical and all14 fresh sealed origins '
    '×2441×1.25, never below the previous historical/fresh maximum basis. All warmup and three routes included.')
timing = json.loads((output / 'persistence-timing.json').read_text())
initialization_path = (ROOT / 'docs/track-b/evidence/cp-26/continuation-v21-r14/recovery3-preparation/'
                       'continuation-accounting-3-recovery3-initialization-1.json')
initialization = json.loads(initialization_path.read_text())['timings']['measured_worker_seconds_before_receipt']
n, sample = 2441, timing['source_origins']
growth = 1.5 * n * (n + 1) / (2 * sample)
persistence_seconds = (growth * (4 * max(timing['encode_hash_seconds']) + timing['write_flush_fsync_seconds'])
    + n * 5 * initialization / sample + 2 * initialization * n / sample)
def cost(seconds, basis, evidence):
    return {'classification': 'conservative', 'machine_seconds': seconds,
            'basis': basis, 'evidence_sha256': sha(evidence)}
remaining['chronological_replay_persistence_exports'] = cost(persistence_seconds,
    'Four measured encode/hash traversals and write/fsync per origin,1.5×linear byte growth from575-origin '
    '79MB resource sample;5×per-origin initialization-derived replay allowance;one startup/final export pair. '
    'Original old state was used only for resource serialization, not imported into new scientific state.',
    output / 'persistence-timing.json')
remaining['scoring_report_draft_packet_review_closure'] = cost(3600.,
    'Preserved1h future worker allocation for scoring, draft packet, final report, independent final Integration '
    'review and closure, in addition to the separately retained parity/test equivalents and measured full statistical workloads.',
    ROOT / RUN_EVIDENCE / 'admission.json')
preparation_max = max(j.get('charged_wall_seconds', 0) * j['workers'] for j in state['jobs']
                      if j.get('run_id') == RUN_ID and j['name'].startswith('cold-prepare-plans'))
remaining['operational_startup_supervision_and_custody'] = cost(12 * preparation_max,
    'Twelve future serial monitored stage/start/review/closure equivalents, each at the maximum whole '
    '337s cold plan-preparation job allocation; includes startup/input context copies,supervision,ledger '
    'refresh and custody. Fitting prices already retain per-fit overhead. Selected independent route fits and chronological replay '
    'uses the calibrated bounded allocation; the wall forecast also states a conservative serial bound.',
    ROOT / RUN_EVIDENCE / 'terminal-custody.json')
remaining['remaining_pricing_and_terminal_packaging'] = cost(300.,
    'Five-minute future worker allowance beyond the current live balance for this pricing tail and final '
    'local bookkeeping; actual already charged preparation and pilot time is not added again.',
    ROOT / RUN_EVIDENCE / 'authority-v21-r15.json')
from cp26.limits import shutdown_exposure_seconds
remaining['extended_detection_shutdown_and_closing_exposure'] = cost(12 * shutdown_exposure_seconds(4),
    'Twelve future monitored stage/failure groups at the full4-slot maximum153.6sallocated shutdown exposure per group,including detection,ledger/poll jitter,termination/kill confirmation and closing accounting. Distinct from10%lost-work allowance and not another historical reserve charge.', ROOT / RUN_EVIDENCE / 'selected-limits-v21-r15.json')
subtotal = sum(r['machine_seconds'] for r in searches) + sum(
    row['machine_seconds'] for name, row in remaining.items() if name != 'failed_jobs_and_resume')
remaining['failed_jobs_and_resume'] = cost(.1 * subtotal,
    'Preserved10% of every future priced component, including all42searches,all2441daily origins, '
    'analysis,persistence,operational startup,custody,report/review/closure. Actual failures and2826s '
    'historical reserve are already included once in the cumulative balance.',
    ROOT / RUN_EVIDENCE / 'ledger-fixed-concurrency-observation.json')
estimate = projected_cost(state, searches, remaining)
projection = C._signed({**{k: v for k, v in standard.items() if k != 'content_sha256'},
    'searches': searches, 'remaining': remaining, **estimate,
    'pilot_completion_job': continuation['job_id'], 'chosen_compute_workers': 4,
    'operational_lineage': H.runtime_lineage(ROOT),
    'historical_search_cost_basis': {'complete_fit_hours': raw_seconds / 3600,
        'all_historical_attempt_hours': historical_seconds / 3600, 'overhead_ratio': overhead,
        'maximum_fresh_old_probe_slowdown': slowdown, 'cold_margin': 2.},
    'fresh_old_probe_slowdowns': slowdowns})
run = scientific_run_summary(state, RUN_ID)
components = {'all42_cold_searches': sum(r['machine_seconds'] for r in searches),
              **{k: r['machine_seconds'] for k, r in remaining.items()}}
future = sum(components.values()) / 3600
wall_components = {'route_search_makespan': max(sum(r['machine_seconds'] for r in searches if r['run'] == route) for route in E.ROUTES) / 3600,
    'route_fit_makespan': max(r['machine_seconds'] for r in daily['route_costs']) / 3600,
    'chronological_replay': remaining['chronological_replay_persistence_exports']['machine_seconds'] / 3600,
    'serial_analysis_review_and_overhead': sum(v['machine_seconds'] for k,v in remaining.items() if k not in ('daily_fits','chronological_replay_persistence_exports','failed_jobs_and_resume')) / 3600,
    'failure_allowance_at_one_worker': remaining['failed_jobs_and_resume']['machine_seconds'] / 3600}
expected_wall = sum(wall_components.values())
record = {'schema': 'cp26-admission-v21-r15', 'run_id': RUN_ID,
    'observed_epoch': time.time(), 'admission': 'PASS' if estimate['within_pilot_stop'] else 'BLOCKED',
    'projection_gate_hours': 436.5, 'actual_ceiling_hours': 485,
    'current_cumulative': resource_summary(state), 'current_new_run': run,
    'historical_baseline_hours': run['historical_baseline_hours'],
    'remaining_components_seconds': components, 'remaining_hours': future,
    'complete_conservative_cumulative_hours': estimate['projected_total_hours'],
    'complete_new_run_estimate_hours': run['machine_hours'] + future,
    'shortfall_hours': max(0., estimate['projected_total_hours'] - 436.5),
    'expected_remaining_wall_hours_at_chosen_concurrency': expected_wall,
    'wall_forecast_components_hours': wall_components, 'maximum_compute_workers': 4,
    'expected_concurrency_basis': 'Three independent route-search jobs; then three independent route-fit workers and one chronological cache-only replay worker,each single-threaded. Existing route APIs permit these independent fits; replay and H updates stay chronological. No additional reserved coordinator. Memory pressure may drain concurrency at safe boundaries; the serial bound is also reported.',
    'serial_remaining_wall_upper_hours': future,
    'fresh_pilot': {'probes': 1064, 'pairs': 42, 'initial1013_hashes_unchanged': True,
        'completion_job_id': continuation['job_id'], 'sha256': sha(output / 'timing-pilot.json')},
    'prior_rejected_admission': {'path': str(RUN_EVIDENCE / 'admission.json'),
        'sha256': sha(ROOT / RUN_EVIDENCE / 'admission.json'), 'unchanged': True},
    'cost_projection': {'path': str(OUTPUT / 'cost-projection.json'), 'canonical_object_sha256': C.digest(projection)},
    'supported_operational_assumption': 'Measured calibrated ledger/observer limits and49affectedchecks passed; all1064existing pilot probes completed. Actual guard failure still halts compute. Future overhead,38.4sper-slot stop exposure and10%failed-work allowance are separately priced; original2826shistorical reserve remains once in current balance.',
    'code_sha256': code_identity(ROOT), 'protocol': shared,
    'operational_lineage': H.runtime_lineage(ROOT),
    'calibration_document': str(RUN_EVIDENCE / 'calibration-v21-r15.json'),
    'full_scientific_workload_started': False}
C.persist_projection(ROOT, projection, output=OUTPUT / 'cost-projection.json')
record = E._signed(record)
E._immutable(ROOT / RUN_EVIDENCE / 'admission-v21-r15.json', record)
E._immutable(output / 'admission-v21-r15.json', record)
print(json.dumps({k: record[k] for k in ('admission', 'remaining_hours',
    'complete_conservative_cumulative_hours', 'complete_new_run_estimate_hours', 'shortfall_hours')}), flush=True)
