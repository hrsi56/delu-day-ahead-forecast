"""CP-17's product modules on synthetic inputs (CI-safe): §19.5's definitions, the recomputation check,
§19.3's status rule, the frozen failure policy, the artifact and the payload schema.
"""
from __future__ import annotations

from datetime import date, timedelta
import json

import numpy as np
import pytest

from cp17 import dailyfit, issue, retrain, schema, scoring


def keys_for(day: date) -> list[str]:
    return issue.canonical_hours(day)


def flat(n, base=50.0):
    """Seven ordered quantiles per hour around `base`: -20, -10, -5, 0, +5, +10, +20."""
    return [[base + d for d in (-20, -10, -5, 0, 5, 10, 20)] for _ in range(n)]


# ------------------------------------------------------------------ §19.5
def test_percentage_measure_counts_hours_within_tau_inclusive():
    day = date(2026, 9, 1)
    keys = keys_for(day)
    prices = [50.0 + d for d in [0, 10, -10, 10.000001, -15, 0, 0, 0] + [0] * 16]
    record = scoring.evaluate([{'day': str(day), 'keys': keys, 'quantiles': flat(24), 'canonical_hours': 24}],
                              dict(zip(keys, prices)))
    pct = record['pooled']['percentage']
    assert pct['within_hours'] == 22 and pct['scored_hours'] == 24       # ±10 is inside; 10.000001 and -15 are not
    assert pct['share'] == 22 / 24 and pct['label'] == scoring.PERCENTAGE_LABEL


def test_zero_negative_and_missing_prices():
    day = date(2026, 9, 1)
    keys = keys_for(day)
    prices = {k: (np.nan if i < 4 else (-5.0 if i % 2 else 0.0)) for i, k in enumerate(keys)}
    q = [[v - 1 for v in row] for row in flat(24, 0.0)]
    record = scoring.evaluate([{'day': str(day), 'keys': keys, 'quantiles': q, 'canonical_hours': 24}], prices)
    d = record['days'][0]
    assert d['scored_hours'] == 20 and d['completeness'] == 20 / 24          # missing prices are unscored
    assert record['pooled']['partial_days'] == 1
    mae = np.mean([abs(prices[k] - (-1.0)) for k in keys[4:]])               # zero and negative count as they are
    assert d['mae_eur'] == pytest.approx(mae)


def test_pending_day_is_unscored_and_days_weigh_equally():
    d1, d2, d3 = date(2026, 9, 1), date(2026, 9, 2), date(2026, 9, 3)
    issued = [{'day': str(d), 'keys': keys_for(d), 'quantiles': flat(24), 'canonical_hours': 24} for d in (d1, d2, d3)]
    outcomes = {k: 52.0 for k in keys_for(d1)}
    outcomes.update({k: (60.0 if i == 0 else np.nan) for i, k in enumerate(keys_for(d2))})    # one scored hour
    record = scoring.evaluate(issued, outcomes)
    p = record['pooled']
    assert p['scored_days'] == 2 and p['pending_or_unscored_days'] == 1 and p['scored_hours'] == 25
    assert p['mae_eur'] == pytest.approx((2.0 + 10.0) / 2)                  # equal date weights, not pooled hours


def test_coverage_width_reliability_and_pit_bands():
    day = date(2026, 9, 1)
    keys = keys_for(day)
    # One price in each PIT band position, ties to a quantile in the band it closes.
    prices = [10.0, 30.0, 40.0, 45.0, 50.0, 52.0, 58.0, 65.0, 75.0, 30.0] + [50.0] * 14
    record = scoring.evaluate([{'day': str(day), 'keys': keys, 'quantiles': flat(24), 'canonical_hours': 24}],
                              dict(zip(keys, prices)))
    pit = [b['count'] for b in record['pooled']['pit']]
    # Quantiles 30, 40, 45, 50, 55, 60, 70: 10 and both 30s close band 0; 40 band 1; 45 band 2; 50 and the
    # fourteen 50s band 3; 52 band 4; 58 band 5; 65 band 6; 75 band 7.
    assert pit == [3, 1, 1, 15, 1, 1, 1, 1]
    assert [b['nominal_share'] for b in record['pooled']['pit']] == list(scoring.PIT_NOMINAL)
    rel = record['pooled']['reliability']
    assert [r['level'] for r in rel] == list(scoring.LEVELS)
    y = np.array(prices)
    q = np.array(flat(24))
    assert [r['at_or_below'] for r in rel] == [int((y <= q[:, j]).sum()) for j in range(7)]
    cov = record['pooled']['coverage']
    assert cov['50']['covered_hours'] == int(((y >= 45) & (y <= 55)).sum()) and cov['50']['mean_width_eur'] == 10.0
    assert cov['95']['mean_width_eur'] == 40.0 and cov['80']['nominal'] == 0.8


def test_rolling_window_is_the_last_28_scored_days():
    days = [date(2026, 8, 1) + timedelta(days=i) for i in range(30)]
    issued = [{'day': str(d), 'keys': keys_for(d), 'quantiles': flat(24), 'canonical_hours': 24} for d in days]
    outcomes = {k: 50.0 for d in days for k in keys_for(d)}
    for k in keys_for(days[0]):
        outcomes[k] = 100.0                                                   # day 1 uncovered in every band
    series = scoring.evaluate(issued, outcomes)['rolling']
    assert series[27]['window_days'] == 28 and series[27]['coverage95'] == pytest.approx(27 / 28)
    assert series[28]['window_first_day'] == str(days[1]) and series[28]['coverage95'] == 1.0


def test_recomputation_check_counts_exactly_and_reals_within_1e9():
    committed = {'n': 24, 'share': 0.5, 'mae': 1000.0, 'label': 'x'}
    assert scoring.recompute_check(dict(committed), committed)['match']
    assert scoring.recompute_check({**committed, 'mae': 1000.0 + 5e-7}, committed)['match']        # 5e-10 relative
    assert not scoring.recompute_check({**committed, 'mae': 1000.0 + 2e-6}, committed)['match']
    assert scoring.recompute_check({**committed, 'share': 0.5 + 5e-10}, committed)['match']        # max(1, |b|)
    bad = scoring.recompute_check({**committed, 'n': 25}, committed)
    assert not bad['match'] and bad['blocks_publication'] and bad['mismatches'][0]['path'] == 'n'
    assert not scoring.recompute_check({**committed, 'n': 24.0000001}, committed)['match']          # counts exactly
    assert scoring.recompute_check({**committed, 'n': 24.0}, committed)['match']                    # 24.0 == 24
    assert scoring.recompute_check({**committed, 'share': 1}, {**committed, 'share': 1.0})['match']  # a JSON hop
    assert not scoring.recompute_check({k: v for k, v in committed.items() if k != 'label'}, committed)['match']


# ------------------------------------------------------------------ §19.3's status rule
def _a1(q, epochs=10, payload='p' * 64):
    return {'day': '2026-09-06', 'index': ['k'], 'quantiles': q, 'crossed_rows': 0, 'payload_sha256': payload,
            'members': [{**{f: 0 for f in retrain.A1_SELECTIONS}, **{f: 0 for f in retrain.A1_DIAGNOSTICS},
                         'member': j, 'seed': j, 'best_epoch': epochs} for j in range(8)]}


def test_status_rule():
    q = [[1.0, 2, 3, 4, 5, 6, 7]]
    same = retrain.compare('A1', _a1(q), _a1([list(r) for r in q]))
    assert same['status'] == 'identical bit for bit'
    near = retrain.compare('A1', _a1(q), _a1([[1.0, 2, 3, 4 + 0.01, 5, 6, 7]]))
    assert near['status'] == 'within ±0.01 EUR/MWh' and near['selections_match']
    far = retrain.compare('A1', _a1(q), _a1([[1.0, 2, 3, 4.0101, 5, 6, 7]]))
    assert far['status'] == 'different'
    moved = retrain.compare('A1', _a1(q), _a1([[1.0, 2, 3, 4 + 1e-9, 5, 6, 7]], epochs=11))
    assert moved['status'] == 'different' and not moved['selections_match']   # a selection differs: never "within"
    signed = retrain.compare('A1', _a1([[0.0] * 7]), _a1([[-0.0] + [0.0] * 6]))
    assert signed['status'] == 'within ±0.01 EUR/MWh'                          # equal values, different bits
    other = retrain.compare('A1', _a1(q), _a1([list(r) for r in q], payload='q' * 64))
    assert other['status'] == 'different' and other['measured_status'] == 'identical bit for bit'   # another window
    assert retrain.compare('A1', _a1(q, payload=None), _a1(q, payload=None))['status'] == 'different'


# ------------------------------------------------------------------ the frozen failure policy
def _attempts(outcomes):
    calls = []

    def attempts(policy):
        calls.append(policy)
        status = outcomes.get(policy, 'ok')
        return {'policy': policy, 'status': status, 'cause': None if status == 'ok' else 'synthetic'}
    return attempts, calls


@pytest.mark.parametrize('gfs, outcomes, issued, calls, display', [
    (True, {}, 'A1', ['A1'], 'successful daily fit'),
    (True, {'A1': 'failed'}, 'v4', ['A1', 'v4'], 'failed fit; fallback v4 issued'),
    (True, {'A1': 'failed', 'v4': 'failed'}, 'v2', ['A1', 'v4', 'v2'], 'failed fit; fallback v2 issued'),
    (True, {'A1': 'failed', 'v4': 'failed', 'v2': 'failed'}, 'B0', ['A1', 'v4', 'v2', 'B0'], 'failed fit; fallback B0 issued'),
    (True, {'A1': 'failed', 'v4': 'failed', 'v2': 'failed', 'B0': 'failed'}, None, ['A1', 'v4', 'v2', 'B0'], 'failed issuance'),
    (False, {}, 'v2', ['v2'], 'skipped fit (GFS late or missing); fallback v2 issued'),
    (False, {'v2': 'failed'}, 'B0', ['v2', 'B0'], 'skipped fit (GFS late or missing); fallback B0 issued'),
    (False, {'v2': 'failed', 'B0': 'failed'}, None, ['v2', 'B0'], 'failed issuance'),
])
def test_failure_policy_chains(gfs, outcomes, issued, calls, display):
    attempts, called = _attempts(outcomes)
    decision = issue.decide(date(2026, 9, 6), gfs, attempts)
    assert decision['issued_policy'] == issued and called == calls and decision['display'] == display
    if not gfs:
        assert decision['attempts'][0] == {'policy': 'A1', 'status': 'skipped', 'cause': 'GFS late or missing at the issue time'}
    assert 'v5' not in called                                                   # v5 is not in the product's chain


def test_attempt_records_failures_and_emission():
    day = date(2026, 3, 29)                                                     # 23 hours
    ok = issue.attempt('A1', lambda: {'index': keys_for(day), 'quantiles': flat(23)}, day)
    assert ok['status'] == 'ok'
    short = issue.attempt('A1', lambda: {'index': keys_for(day)[:22], 'quantiles': flat(22)}, day)
    assert short['status'] == 'failed' and short['cause'].startswith('emission')

    def boom():
        raise dailyfit.FitFailure('member 3: TrainingFailure: no kept epoch')
    failed = issue.attempt('A1', boom, day)
    assert failed['status'] == 'failed' and 'no kept epoch' in failed['cause']


def test_issue_time_and_resources():
    assert issue.issue_utc(date(2026, 9, 6)) == '2026-09-05T09:00:00+00:00'      # CEST
    assert issue.issue_utc(date(2026, 1, 6)) == '2026-01-05T10:00:00+00:00'      # CET
    assert issue.issue_utc(date(2026, 3, 30)) == '2026-03-29T09:00:00+00:00'     # D-1 is the spring transition day
    assert issue.resources_ok(899, 4 * 1024 ** 3) == []
    assert len(issue.resources_ok(901, 4 * 1024 ** 3 + 1)) == 2


def _artifact():
    day = date(2026, 9, 6)
    decision = {'day': str(day), 'issued_policy': 'A1', 'route': 'designated', 'display': 'successful daily fit',
                'attempts': [{'policy': 'A1', 'status': 'ok', 'cause': None, 'seconds': 1.0,
                              'result': {'policy': 'A1', 'index': keys_for(day), 'quantiles': flat(24),
                                         'quantiles_sha256': dailyfit.array_hash(np.asarray(flat(24), float)),
                                         'search': 13, 'ensemble_content_sha256': '0' * 64, 'members': []}}]}
    return issue.artifact(decision, identity={'policy_identity_sha256': '1' * 64, 'package_sha256': '2' * 64},
                          payloads={'A1': {'payload_sha256': '3' * 64}}, parent_sha256=None, data_refresh_utc='',
                          host={'runtime': 'pyodide'}, wall_seconds=80.0, peak_bytes=10 ** 9)


def test_artifact_verifies_and_detects_tampering():
    item = _artifact()
    assert issue.verify_artifact(item) == [] and item['display'] == 'successful daily fit'
    assert schema.validate(json.loads(json.dumps(item)), schema.SCHEMAS['fitted_artifact']) == []
    tampered = json.loads(json.dumps(item))
    tampered['quantiles'][0][3] += 0.5
    assert issue.verify_artifact(tampered)
    heavy = issue.artifact({**item, 'attempts': [{'policy': 'A1', 'status': 'ok', 'result': {
        'policy': 'A1', 'index': item['keys'], 'quantiles': item['quantiles'], 'quantiles_sha256': item['quantiles_sha256'],
        'search': 13, 'ensemble_content_sha256': '0' * 64, 'members': []}}], 'day': item['delivery_day']},
        identity={}, payloads={}, parent_sha256=None, data_refresh_utc='', host={}, wall_seconds=1000.0, peak_bytes=1)
    assert heavy['display'] == 'failed fit (resources)' and heavy['resource_check']


# ------------------------------------------------------------------ the schema and its validator
def test_validator_subset():
    s = {'type': 'object', 'required': ['a'], 'additionalProperties': False,
         'properties': {'a': {'type': 'array', 'minItems': 1, 'items': {'enum': [1, 2]}}, 'b': schema.DAY}}
    assert schema.validate({'a': [1, 2]}, s) == []
    assert schema.validate({'a': []}, s) and schema.validate({'a': [3]}, s) and schema.validate({'c': 1, 'a': [1]}, s)
    assert schema.validate({'a': [1], 'b': '2026-9-6'}, s)
    assert schema.validate(float('nan'), {'type': 'number'}) and schema.validate(True, {'type': 'integer'})


def test_payload_identity_binds_arrays_and_meta():
    arrays = {'x': np.arange(4.0)}
    meta = {'schema': dailyfit.SCHEMAS['B0'], 'day': '2026-09-06'}
    meta['payload_sha256'] = dailyfit.payload_digest(arrays, meta)
    dailyfit.check_payload(arrays, meta, 'B0')
    with pytest.raises(ValueError, match='identity'):
        dailyfit.check_payload({'x': np.arange(4.0) + 1}, meta, 'B0')
    with pytest.raises(ValueError, match='identity'):
        dailyfit.check_payload(arrays, {**meta, 'day': '2026-09-05'}, 'B0')


def test_index_hash_is_int64_in_every_runtime():
    ix32, ix64 = np.array([1, 5, 9], dtype=np.int32), np.array([11, 15, 19], dtype=np.int64)
    assert dailyfit.index_hash(ix32, 10) == dailyfit.index_hash(ix64, 0) == dailyfit.array_hash(ix64)


def _bundle():
    """A minimal verified bundle: a manifest and one B0 training window (synthetic values)."""
    import hashlib
    import io
    day = date(2026, 9, 6)
    keys = np.array([np.datetime64(k.replace('+00:00', '')).astype('datetime64[ns]').astype(np.int64)
                     for k in keys_for(day)], dtype=np.int64)
    arrays = {'price_ns': keys, 'price': np.full(24, np.nan), 'key_ns': keys}
    meta = {'schema': dailyfit.SCHEMAS['B0'], 'policy': 'B0', 'day': str(day), 'embargo': 'synthetic', 'b0_buffer': [],
            'array_sha256': {k: dailyfit.array_hash(v) for k, v in sorted(arrays.items())}}
    meta['payload_sha256'] = dailyfit.payload_digest(arrays, meta)
    buf = io.BytesIO()
    np.savez(buf, **arrays)
    files = {f'B0-{day}.json': json.dumps(meta).encode(), f'B0-{day}.npz': buf.getvalue()}
    manifest = {'schema': 'cp17-manifest-v1',
                'product': {'name': 'delu-day-ahead-policy', 'designated_policy': 'A1', 'evidence_label': 'synthetic'},
                'policy': {'policy_identity_sha256': '1' * 64, 'package_sha256': '2' * 64, 'issuing_host': 'test'},
                'artifact': {'artifact_sha256': '3' * 64, 'delivery_day': str(day), 'issued_policy': 'B0', 'display': 'x'},
                'times': {'last_training_utc': '2026-09-05T09:00:00+00:00', 'data_refresh_utc': '',
                          'issuance_utc': '2026-09-05T09:00:00+00:00'},
                'freshness': {'state': 'fresh', 'as_of_day': str(day), 'latest_issued_day': str(day)},
                'files': [{'path': p, 'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b), 'kind': 'training_window'}
                          for p, b in sorted(files.items())]}
    files['manifest.json'] = json.dumps(manifest).encode()
    return files


def test_bundle_verifies_and_refuses_tampering_without_crashing():
    files = _bundle()
    assert schema.verify_bundle(files) == []
    npz = next(k for k in files if k.endswith('.npz'))
    flipped = dict(files)
    blob = bytearray(flipped[npz])
    blob[len(blob) // 2] ^= 0x01
    flipped[npz] = bytes(blob)
    errors = schema.verify_bundle(flipped)                 # a refusal, not a BadZipFile
    assert errors and 'SHA-256' in errors[0]
    leaked = {**files}
    meta = json.loads(leaked['B0-2026-09-06.json'])
    assert schema.check_training_window(meta, {'price_ns': np.zeros(1), 'price': np.ones(1), 'key_ns': np.zeros(1)})
