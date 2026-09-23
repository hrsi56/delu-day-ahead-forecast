"""E1 pre-run feasibility: measured subset costs extrapolated against every section 15.5 cap.

Estimates are planning numbers, not guarantees. Inputs: the cumulative ledger, the
extraction request log and completed subset runs (actual measurements), CP-16's
measured per-component-day fitting cost, and the frozen origin/run manifests.
"""
from __future__ import annotations

import json
from pathlib import Path

from .budget import CAPS, GIB, HOUR, Budget


def estimate(root: Path, weather: Path, ledger: Path, workers: int) -> dict:
    manifest = json.loads((root / 'reports/weather-ablation/run-manifest.json').read_text())
    runs = {r['run_00z']: r for r in manifest['runs']}
    done = []
    for path in (weather / 'runs').glob('*.json'):
        rec = json.loads(path.read_text())
        if rec.get('status') == 'complete':
            done.append(rec)
    by = {'ncar': [], 'aws': []}
    for rec in done:
        endpoint = runs[rec['run_00z']]['primary_endpoint']
        payload = sum(m['bytes'] for m in rec['messages'])
        by[endpoint].append((rec['elapsed_s'], payload, rec['run_00z']))
    requests = [json.loads(l) for l in (weather / 'requests.jsonl').read_text().splitlines()]
    charged = {'ncar': 0, 'aws': 0}
    for r in requests:
        charged[r['endpoint']] += r['charged_bytes']
    n_total = {'ncar': sum(r['primary_endpoint'] == 'ncar' for r in manifest['runs']),
               'aws': sum(r['primary_endpoint'] == 'aws' for r in manifest['runs'])}
    state = Budget(ledger).read()
    used = state['counts']
    out = {'measured_subset': {}, 'projection': {}}
    for ep in ('ncar', 'aws'):
        if not by[ep]:
            continue
        secs = sorted(x[0] for x in by[ep])
        mean_s = sum(secs) / len(secs)
        # Charged bytes per completed run: all requests to that endpoint (incl. failures/windows/idx bounds).
        per_run_charged = charged[ep] / len(by[ep])
        remaining = n_total[ep] - len(by[ep])
        out['measured_subset'][ep] = {'runs': len(by[ep]), 'mean_worker_seconds_per_run': mean_s,
                                      'max_worker_seconds_per_run': secs[-1],
                                      'mean_payload_bytes_per_run': sum(x[1] for x in by[ep]) / len(by[ep]),
                                      'charged_bytes_per_completed_run_upper': per_run_charged}
        out['projection'][ep] = {'remaining_runs': remaining,
                                 'worker_hours': remaining * mean_s / HOUR,
                                 'wall_hours_at_workers': remaining * mean_s / HOUR / workers,
                                 'charged_transfer_gib': remaining * per_run_charged / GIB}
    extraction_worker_hours = sum(v['worker_hours'] for v in out['projection'].values())
    extraction_transfer = sum(v['charged_transfer_gib'] for v in out['projection'].values())
    # CP-16 measured ~9 s per fresh component-day (690 s admission job / ~76 fresh component-days);
    # weather adds 3+3 design columns; a 2x allowance covers the larger design and continuations.
    fit_s = 18.0
    fits = {'hg_main_component_days': 2 * 638, 'controls_component_days': 28, 'review_reserve_component_days': 60}
    fit_hours = sum(fits.values()) * fit_s / HOUR
    policy_days = {'paired_pass_admission_plus_comparison': 2 * 638, 'controls': 14,
                   'independent_review_replay_reserve': 2 * 638 + 100}
    other_hours = {'assembly_protocol_tests_scoring': 2.0, 'critic_review_reserve': 8.0,
                   'extraction_failures_retries_margin': 0.15 * extraction_worker_hours}
    total_machine = used.get('machine_seconds', 0) / HOUR + extraction_worker_hours + fit_hours + sum(other_hours.values())
    total_transfer = used.get('transfer_bytes', 0) / GIB + extraction_transfer + 2.0
    out.update({
        'fits': {**fits, 'assumed_seconds_per_component_day': fit_s, 'machine_hours': fit_hours,
                 'primitive_fits_nominal': sum(fits.values()) * 24 * 5},
        'policy_days': policy_days, 'other_machine_hours': other_hours,
        'totals_vs_caps': {
            'machine_hours': [total_machine, CAPS['machine_seconds'] / HOUR],
            'transfer_gib': [total_transfer, CAPS['transfer_bytes'] / GIB],
            'component_attempts': [used.get('component_attempts', 0) + sum(fits.values()), CAPS['component_attempts']],
            'main_component_attempts': [fits['hg_main_component_days'], CAPS['main_component_attempts']],
            'primitive_fits_nominal': [sum(fits.values()) * 120, CAPS['primitive_fits']],
            'policy_days': [sum(policy_days.values()), CAPS['policy_days']],
            'message_attempts': [used.get('message_attempts', 0) + 50 * (n_total['ncar'] + n_total['aws'] - len(done)) * 1.05
                                 + 600 + 50 * 23, CAPS['message_attempts']],
            'decoded_box_disk_gib_upper': [2476 * 0.6e6 / GIB + 1.2, CAPS['additional_disk_bytes'] / GIB],
            'rss_gib_upper': [4 * 1.2 + 0.5, CAPS['rss_bytes'] / GIB]},
        'active_hours_so_far_upper_bound': Budget.active_seconds(state) / HOUR,
        'workers_for_extraction': workers,
        'verdict': None})
    ok = all(a <= b for a, b in out['totals_vs_caps'].values())
    out['verdict'] = 'feasible_within_all_caps_with_reserves' if ok else 'INSUFFICIENT_ALLOWANCE'
    return out
