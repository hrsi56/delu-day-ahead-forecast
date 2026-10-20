"""Price the covered workload and state the unresolved admission cost without inventing zero."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import time

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp26 import execution as E, costing as C
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
            if (ROOT / path).read_bytes() != namespaced:
                raise RuntimeError('search timing reuse covers only the declared run-identity change')
        elif sha(ROOT / path) != expected:
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
probes = [E._read(p) for p in sorted((output / 'timing-pilot').glob('*/*/*.json'))]
groups = {(r, k): {} for r in E.ROUTES for k in range(14)}
shared = protocol_identity(ROOT)
protocol_digest = E.digest(shared)
for probe in probes:
    key = probe['key']
    if key.get('protocol_sha256') != protocol_digest:
        raise RuntimeError('fresh timing probe has a different run identity')
    groups[key['route'], key['k']][key['task']] = probe
complete_pairs, slowdown_rows = [], []
daily_maxima = {r: max(row['daily_wall_seconds'] for row in old_pilot['summary'] if row['route'] == r)
                for r in E.ROUTES}
for old_row in old_pilot['summary']:
    route, k = old_row['route'], old_row['k']
    group = groups[route, k]
    daily = {f'daily-{m}' for m in C.DAILY_MEMBERS[route]} | {
        f'daily-D2-r{rank}-s{repeat}' for rank in range(1, 5) for repeat in (1, 2)}
    searches = {f'search-t{t:03d}-b00' for t in range(12)}
    if daily <= set(group):
        daily_maxima[route] = max(daily_maxima[route], sum(group[t]['wall_seconds'] for t in daily))
    if searches <= set(group):
        ratio = sum(group[t]['wall_seconds'] for t in searches) / sum(old_row['search_probe_wall_seconds'])
        slowdown_rows.append({'route': route, 'k': k, 'ratio': ratio})
    if daily | searches <= set(group):
        complete_pairs.append([route, k])
slowdown = max(1., max(r['ratio'] for r in slowdown_rows))
state = Budget().read()
historical_jobs = [j for j in state['jobs'] if j.get('run_id') != RUN_ID and 'search' in j['name']
                   and not any(s in j['name'] for s in ('test', 'support', 'cost', 'pilot'))]
historical_seconds = sum(j.get('charged_wall_seconds', j.get('wall_seconds', 0)) * j['workers'] for j in historical_jobs)
raw_seconds = sum(r['total_recorded_fit_seconds'] for r in coverage['searches'])
overhead = max(1., historical_seconds / raw_seconds)
search_rows = [{**{k: r[k] for k in ('route', 'k', 'fit_records', 'expected_fit_records', 'source', 'sha256')},
                'projected_seconds': 2 * r['total_recorded_fit_seconds'] * overhead * slowdown}
               for r in coverage['searches']]
components = {'all42_cold_searches': sum(r['projected_seconds'] for r in search_rows),
              'all2441_daily_origins_all3_routes': sum(daily_maxima.values()) * 2441 * 1.25}
for name in ('bootstrap', 'diagnostics', 'parity', 'tests'):
    components[name] = benchmark['additional_costs'][name]['machine_seconds']
timing = json.loads((output / 'persistence-timing.json').read_text())
initialization_path = (ROOT / 'docs/track-b/evidence/cp-26/continuation-v21-r14/recovery3-preparation/'
                       'continuation-accounting-3-recovery3-initialization-1.json')
initialization = json.loads(initialization_path.read_text())['timings']['measured_worker_seconds_before_receipt']
n, sample = 2441, timing['source_origins']
growth = 1.5 * n * (n + 1) / (2 * sample)
components['chronological_replay_persistence_exports'] = (growth * (
    4 * max(timing['encode_hash_seconds']) + timing['write_flush_fsync_seconds'])
    + n * 5 * initialization / sample + 2 * initialization * n / sample)
components['scoring_report_draft_packet_review_closure'] = 3600.
components['ordinary_failure_allowance'] = .1 * sum(components.values())
summary = resource_summary(state)
run = scientific_run_summary(state, RUN_ID)
future_seconds = sum(components.values())
record = {'schema': 'cp26-cold-blocked-cost-forecast-v1', 'run_id': RUN_ID, 'admission': 'BLOCKED',
    'observed_epoch': time.time(), 'historical_baseline_hours': run['historical_baseline_hours'],
    'current_cumulative': summary, 'current_new_run': run,
    'priced_components_seconds': components, 'priced_remaining_hours': future_seconds / 3600,
    'priced_cumulative_subtotal_hours': summary['machine_hours'] + future_seconds / 3600,
    'priced_new_run_subtotal_hours': run['machine_hours'] + future_seconds / 3600,
    'complete_conservative_cumulative_hours': None, 'complete_new_run_estimate_hours': None,
    'expected_completion_wall_hours': None, 'priced_part_wall_hours_at_one_worker': future_seconds / 3600,
    'projection_gate_hours': 388, 'actual_ceiling_hours': 485,
    'unpriced_material_component': 'Reliable monitored progress/recovery cost: the unchanged0.5-second ledger '
        'deadline and2-second heartbeat stopped concurrent writers and then the sole writer after1974.772537s. '
        'The complete fresh pilot is missing118 probes; no supported finite allowance resolves this failure.',
    'fresh_pilot': {'probes': len(probes), 'required_probes': 1064, 'missing_probes': 1064 - len(probes),
                    'complete_route_search_pairs': complete_pairs, 'required_pairs': 42},
    'cold_searches': search_rows, 'fresh_old_search_probe_slowdowns': slowdown_rows,
    'search_basis': {'complete_historical_fit_hours': raw_seconds / 3600,
        'all_historical_search_attempt_hours': historical_seconds / 3600,
        'overhead_ratio': overhead, 'observed_slowdown_floor1': slowdown, 'future_cold_margin': 2.0,
        'coverage_sha256': sha(coverage_path), 'historical_charges_added_again': False},
    'daily_basis': {'maximum_complete_origin_seconds': daily_maxima, 'origins': 2441, 'margin': 1.25,
        'coverage': 'All14 sealed historical origins plus each complete fresh route/origin; only timing reused, '
                    'no old forecast, ensemble, fit cache or H/learning object imported.'},
    'analysis_basis': {'source': str((old / 'fixture-benchmark.json').relative_to(ROOT)),
        'sha256': sha(old / 'fixture-benchmark.json'), 'algorithms': 'Statistical bytes unchanged; analysis differs only in two path substitutions.'},
    'persistence_basis': {'source': str(OUTPUT / 'persistence-timing.json'),
        'sha256': sha(output / 'persistence-timing.json'), 'encoding_traversals_per_day': 4,
        'byte_growth_margin': 1.5, 'initialization_source': str(initialization_path.relative_to(ROOT)),
        'initialization_sha256': sha(initialization_path)},
    'contingency_basis': '10percent of all priced future components; current historical/pilot/failure actuals '
        'and2826-second retained reserve already occur once in current balance. Unresolved ledger failure remains unpriced.',
    'full_scientific_workload_started': False, 'new_serving_searches': 0, 'new_forecast_origins': 0,
    'code_sha256': code_identity(ROOT), 'protocol': shared}
atomic(ROOT / RUN_EVIDENCE / 'admission.json', record)
atomic(output / 'cost-forecast-blocked.json', record)
print(json.dumps({k: record[k] for k in ('admission', 'priced_remaining_hours', 'priced_cumulative_subtotal_hours',
    'priced_new_run_subtotal_hours', 'complete_conservative_cumulative_hours', 'fresh_pilot')}), flush=True)
