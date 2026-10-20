"""The full-run price must retain failed probes, identities and cumulative charges."""
import copy
from datetime import date, timedelta
import hashlib
import json

import pytest

from cp26 import budget as B
from cp26 import costing as C


def sign(value):
    unsigned = {k: v for k, v in value.items() if k != 'content_sha256'}
    raw = json.dumps(unsigned, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    return {**unsigned, 'content_sha256': hashlib.sha256(raw).hexdigest()}


def basis(name, seconds=10.0):
    return {'classification': 'conservative', 'machine_seconds': seconds,
            'basis': f'{name}: independently identified fixture upper bound', 'evidence_sha256': 'f' * 64}


def refresh_summary(pilot):
    summaries = []
    for k in range(14):
        for route in C.ROUTES:
            rows = [p for p in pilot['probes'] if (p['key']['route'], p['key']['k']) == (route, k)]
            summaries.append({'route': route, 'k': k, 'origin': C.ORIGINS[k],
                'daily_wall_seconds': sum(p['wall_seconds'] for p in rows if p['key']['task'].startswith('daily-')),
                'search_probe_wall_seconds': [p['wall_seconds'] for p in rows if p['key']['task'].startswith('search-')],
                'failed_probes': sum(p['status'] == 'failed' for p in rows),
                'probe_sha256': [p['content_sha256'] for p in rows]})
    pilot['summary'] = summaries
    return sign(pilot)


@pytest.fixture
def evidence():
    raw = json.dumps({'schema': 'cp26-execution-protocol-v21-r14', 'authority_sha256': 'a' * 64,
        'research_sha256': 'b' * 64,
        'calendar': {'first': '2020-01-01', 'last': '2026-09-06', 'origins': 2441, 'routes': list(C.ROUTES)},
        'pilot': {'origins': list(C.ORIGINS), 'projection': {'ceiling_hours': 485, 'stop_hours': 388}}},
        sort_keys=True).encode()
    protocol = {'schema': 'cp26-execution-protocol-v21-r14', 'document': 'execution-protocol.json',
                'document_sha256': hashlib.sha256(raw).hexdigest(), 'authority_sha256': 'a' * 64,
                'research_sha256': 'b' * 64, 'cp28_protocol_sha256': 'd' * 64}
    code = {'src/cp26/search.py': 'c' * 64}
    plans, references, probes = [], [], []
    for k in range(14):
        for route in C.ROUTES:
            count = 1 if k == 0 else 7 if k == 1 else 11
            origin = date.fromisoformat(C.ORIGINS[k])
            batches = [{'first': str(origin - timedelta(days=28 * (b + 1))),
                        'every_possible_split_sufficient': True} for b in range(count)]
            support = sign({'B': count, 'k': k, 'search_day': str(origin), 'batches': batches})
            identity = {'route': route, 'k': k, 'protocol': 'cp26-ddnn2-search-v21-r14', 'code_sha256': code}
            trials = [{'id': f't{trial}', 'depth': trial + 1} for trial in range(128)]
            seeds = [26_000_000 + k * 100_000 + 90_000 + 10 * rank + repeat
                     for rank in range(1, 5) for repeat in (1, 2)]
            plan = sign({'schema': 'cp26-search-plan-v2', 'protocol': 'cp26-ddnn2-search-v21-r14',
                         'route': route, 'k': k, 'B': count, 'search_day': str(origin), 'identity': identity,
                         'support': support, 'trials': trials, 'member_seeds': seeds})
            plans.append(plan)
            references.append({'route': route, 'k': k, 'B': count, 'search_day': str(origin),
                               'identity': identity, 'content_sha256': plan['content_sha256']})
            common = {'route': route, 'k': k, 'identity': identity,
                      'protocol_sha256': C.digest(protocol), 'plan_sha256': plan['content_sha256']}
            keys = [{**common, 'task': f'daily-{member}', 'member': member, 'origin': str(origin)}
                    for member in C.DAILY_MEMBERS[route]]
            keys += [{**common, 'task': f'daily-D2-r{rank}-s{repeat}', 'rank': rank, 'repeat': repeat,
                      'trial': rank - 1, 'config': trials[rank - 1], 'seed': seeds[2 * (rank - 1) + repeat - 1],
                      'origin': str(origin)} for rank in range(1, 5) for repeat in (1, 2)]
            keys += [{**common, 'task': f'search-t{trial:03d}-b00', 'trial': trial, 'batch': 0,
                      'config': trials[trial], 'seed': 26_000_000 + k * 100_000 + trial * 100,
                      'origin': batches[0]['first']} for trial in range(12)]
            for index, key in enumerate(keys):
                wall = (0.5 if key['task'].startswith('search-') else 2.0) + k / 100 + index / 1000
                probes.append(sign({'schema': 'cp26-timing-probe-v1', 'key': key, 'wall_seconds': wall,
                                    'seconds': wall / 100, 'status': 'failed' if index in (0, len(keys) - 1) else 'ok'}))
    manifest = sign({'schema': 'cp26-execution-manifest-v1', 'protocol_identity': protocol,
                     'protocol_sha256': C.digest(protocol), 'searches': references})
    pilot = refresh_summary({'schema': 'cp26-timing-pilot-v1', 'protocol_identity': protocol, 'protocol': protocol,
        'execution_manifest_sha256': manifest['content_sha256'], 'origins': list(C.ORIGINS),
        'routes': list(C.ROUTES), 'probes': probes, 'evaluation_scores_computed': False,
        'serving_ensembles_created': False})
    state = {'counts': {'machine_seconds': 350.0},
             'accounting': {'measured_seconds': 100.0, 'reported_seconds': 50.0, 'reserved_seconds': 200.0},
             'jobs': [], 'peaks': {}, 'reserves': [{'status': 'authorized', 'seconds': 200.0}]}
    return {'state': state, 'pilot': pilot, 'plans': plans, 'execution_manifest': manifest,
            'protocol_bytes': raw, 'protocol': protocol, 'code_sha256': code,
            'additional_costs': {name: basis(name) for name in C.ADDITIONAL}}


def price(evidence):
    return C.price_pilot(**evidence)


def test_every_search_uses_its_failed_inclusive_outer_wall_and_frozen_fit_count(evidence):
    unchanged = copy.deepcopy(evidence['state'])
    result = price(evidence)
    assert len(result['searches']) == 42
    by_summary = {(r['route'], r['k']): r for r in evidence['pilot']['summary']}
    for row in result['searches']:
        summary = by_summary[row['run'], row['k']]
        expected_count = 128 if row['k'] == 0 else 641 if row['k'] == 1 else 813
        assert row['halving_fit_count'] == expected_count
        assert row['machine_seconds'] == max(summary['search_probe_wall_seconds']) * expected_count * 1.5
        assert row['failed_probes'] == 2 and row['plan_sha256']
        assert row['classification'] == 'conservative' and row['basis']
    assert result['pilot_sha256'] == C.digest(evidence['pilot'])
    assert evidence['state'] == unchanged


def test_daily_each_route_uses_all_fourteen_origins_and_keeps_cumulative_classes(evidence):
    result = price(evidence)
    daily = result['remaining']['daily_fits']
    assert daily['total_origins'] == 2441 and len(daily['route_costs']) == 3
    for row in daily['route_costs']:
        maximum = max(s['daily_wall_seconds'] for s in evidence['pilot']['summary'] if s['route'] == row['run'])
        assert row['machine_seconds'] == maximum * 2441 * 1.25
        assert row['maximum_origin'] == C.ORIGINS[-1]
    assert result['projected_total_seconds'] == pytest.approx(
        350 + sum(r['machine_seconds'] for r in result['searches']) + daily['machine_seconds'] + 50)
    assert result['measured_seconds'] == 100 and result['reported_seconds'] == 50 and result['reserved_seconds'] == 200


@pytest.mark.parametrize('damage', ['missing_summary', 'duplicate_summary', 'corrupt_probe', 'summary_wall',
                                   'summary_failure', 'probe_seed', 'probe_plan', 'plan_code', 'protocol_hash'])
def test_missing_corrupt_or_unbound_evidence_cannot_price(evidence, damage):
    if damage == 'missing_summary':
        evidence['pilot']['summary'].pop()
    elif damage == 'duplicate_summary':
        evidence['pilot']['summary'][-1] = evidence['pilot']['summary'][0]
    elif damage == 'corrupt_probe':
        evidence['pilot']['probes'][0]['wall_seconds'] *= 2
    elif damage == 'summary_wall':
        evidence['pilot']['summary'][0]['daily_wall_seconds'] += 1
    elif damage == 'summary_failure':
        evidence['pilot']['summary'][0]['failed_probes'] = 0
    elif damage in ('probe_seed', 'probe_plan'):
        probe = next(p for p in evidence['pilot']['probes'] if p['key']['task'].startswith('search-'))
        probe['key']['seed' if damage == 'probe_seed' else 'plan_sha256'] = 1 if damage == 'probe_seed' else 'e' * 64
        index = evidence['pilot']['probes'].index(probe)
        evidence['pilot']['probes'][index] = sign(probe)
        evidence['pilot'] = refresh_summary(evidence['pilot'])
    elif damage == 'plan_code':
        evidence['code_sha256'] = {'src/cp26/search.py': 'e' * 64}
    else:
        evidence['protocol_bytes'] += b' '
    evidence['pilot'] = sign(evidence['pilot'])
    with pytest.raises((ValueError, TypeError)):
        price(evidence)


@pytest.mark.parametrize('value', [0, -1, True, float('inf'), float('nan')])
def test_additional_cost_cannot_be_zero_unidentified_or_nonfinite(evidence, value):
    evidence['additional_costs']['bootstrap']['machine_seconds'] = value
    with pytest.raises(ValueError):
        price(evidence)


def test_missing_identified_cost_basis_blocks_projection(evidence):
    evidence['additional_costs']['tests'].pop('evidence_sha256')
    with pytest.raises(ValueError, match='identified'):
        price(evidence)


def test_no_support_keeps_positive_prepriced_overhead(evidence):
    plan = evidence['plans'][0]
    route, k = plan['route'], plan['k']
    plan['B'] = 0
    plan['support'] = sign({**plan['support'], 'B': 0, 'batches': []})
    plan = sign(plan)
    evidence['plans'][0] = plan
    ref = evidence['execution_manifest']['searches'][0]
    ref.update(B=0, content_sha256=plan['content_sha256'])
    evidence['execution_manifest'] = sign(evidence['execution_manifest'])
    revised = []
    for probe in evidence['pilot']['probes']:
        if (probe['key']['route'], probe['key']['k']) == (route, k):
            if probe['key']['task'].startswith('search-'):
                continue
            probe['key']['plan_sha256'] = plan['content_sha256']
            probe = sign(probe)
        revised.append(probe)
    evidence['pilot'].update(probes=revised, execution_manifest_sha256=evidence['execution_manifest']['content_sha256'])
    evidence['pilot'] = refresh_summary(evidence['pilot'])
    with pytest.raises(ValueError, match='zero-support'):
        price(evidence)
    evidence['zero_support_overheads'] = {(route, k): basis('B0 explicit admission/failure record overhead', 7.0)}
    result = price(evidence)
    row = result['searches'][0]
    assert row['halving_fit_count'] == 0 and row['machine_seconds'] == 7
    assert row['zero_support_overhead']['evidence_sha256'] == 'f' * 64


def test_projection_gate_actually_raises_and_reprices_new_ledger_charges(evidence):
    result = price(evidence)
    current = C.require_projection(result, evidence['state'])
    assert current['within_pilot_stop']
    B.add_seconds(evidence['state'], 436.5 * B.HOUR, 'reported')
    with pytest.raises(B.CapExceeded, match='436.5-hour cumulative admission line'):
        C.require_projection(result, evidence['state'])


def test_expensive_projection_is_retained_before_gate_refuses(evidence, tmp_path):
    evidence['additional_costs']['bootstrap'] = basis('registered bootstrap upper bound', 436.5 * B.HOUR)
    result = price(evidence)
    assert not result['within_pilot_stop']
    path = C.persist_projection(tmp_path, result)
    assert json.loads(path.read_text()) == result
    with pytest.raises(B.CapExceeded):
        C.require_projection(result, evidence['state'])
    assert C.persist_projection(tmp_path, result) == path
    changed = sign({**result, 'pilot_sha256': 'e' * 64})
    with pytest.raises(ValueError, match='frozen pilot projection differs'):
        C.persist_projection(tmp_path, changed)


def test_projection_rejects_ledger_regression_and_external_output(evidence, tmp_path):
    result = price(evidence)
    evidence['state']['accounting']['measured_seconds'] = 0
    evidence['state']['counts']['machine_seconds'] = 250
    with pytest.raises(RuntimeError, match='regressed'):
        C.require_projection(result, evidence['state'])
    with pytest.raises(ValueError, match='reports/rebaseline'):
        C.persist_projection(tmp_path, result, output=tmp_path.parent / 'external.json')
