"""CP-17b's product rules on synthetic inputs (CI-safe): decision 13's partial days with their boundary cases,
criterion 4 inside the chain (N3), the resource measurement an issued artifact must carry (N2), the ceiling's
message (N7), the failed issuance's record, and the two re-frozen payload kinds.
"""
from __future__ import annotations

from datetime import date
import json

import numpy as np
import pytest

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cp17 import dailyfit, issue, schema  # noqa: E402
from cp17b_synthetic import FIT, flat, payload, result, keys_of  # noqa: E402

SPRING, AFTER_SPRING, AUTUMN, PLAIN = date(2026, 3, 29), date(2026, 3, 30), date(2025, 10, 26), date(2026, 9, 6)


def _measured(wall=80.0, peak=10 ** 9):
    return lambda: {'wall_seconds': wall, 'peak_bytes': peak}


def _artifact(decision):
    return issue.artifact(decision, identity={'policy_identity_sha256': '1' * 64, 'package_sha256': '2' * 64},
                          payloads={p['policy']: {'payload_sha256': '3' * 64} for p in decision['attempts']},
                          parent_sha256=None, data_refresh_utc='', host={'runtime': 'pyodide'})


def _finalize(decision):
    return _artifact(decision)


# ------------------------------------------------------------------ decision 13: the forecastable hours
@pytest.mark.parametrize('policy', ['A1', 'v4', 'v2', 'B0'])
@pytest.mark.parametrize('day, keep', [
    (PLAIN, range(24)), (SPRING, range(23)), (AUTUMN, range(25)),            # complete 24-, 23- and 25-hour days
    (AFTER_SPRING, [h for h in range(24) if h != 0]),                       # one unforecastable hour after a change
    (AUTUMN, range(1, 25)), (PLAIN, [5]),                                    # 24 of 25; a single forecastable hour
])
def test_the_design_decides_the_forecastable_hours(policy, day, keep):
    keys = [keys_of(day)[i] for i in keep]
    arrays, meta = payload(policy, day, keys)
    assert issue.forecastable_keys(policy, arrays, meta) == keys
    assert issue.check_inputs(policy, arrays, meta) == []


@pytest.mark.parametrize('policy', ['A1', 'v4', 'v2', 'B0'])
def test_a_day_with_no_forecastable_hour_fails_every_policy_at_its_inputs(policy):
    arrays, meta = payload(policy, PLAIN, [])
    assert issue.check_inputs(policy, arrays, meta) == [issue.NO_FORECASTABLE_HOUR]
    called = []
    item = issue.attempt(policy, lambda: called.append(1), PLAIN, arrays, meta, resources=_measured())
    assert item['status'] == 'failed' and item['cause'] == f'inputs: {issue.NO_FORECASTABLE_HOUR}' and not called


def test_a_day_with_no_forecastable_hour_is_a_failed_issuance_and_is_recorded():
    loaded = {p: payload(p, PLAIN, []) for p in ('A1', 'v4', 'v2', 'B0')}
    for gfs in (True, False):
        decision = issue.decide(PLAIN, gfs, lambda p: issue.attempt(p, lambda: None, PLAIN, *loaded[p], resources=_measured()),
                                _finalize)
        assert decision['issued_policy'] is None
        assert decision['display'] == f'failed issuance ({issue.NO_FORECASTABLE_HOUR})'
        art = decision['artifact']
        assert issue.verify_artifact(art) == [] and schema.validate(json.loads(json.dumps(art)), schema.SCHEMAS['fitted_artifact']) == []
        assert art['keys'] is None and art['resources'] is None and art['partial'] is None
        assert len(art['attempts']) == (4 if gfs else 3)       # every failure stays in the record (§16.2)


def test_a_partial_fit_succeeds_on_its_hours_and_names_the_missing_ones():
    keys = keys_of(AFTER_SPRING)[1:]
    arrays, meta = payload('A1', AFTER_SPRING, keys)
    item = issue.attempt('A1', lambda: result('A1', AFTER_SPRING, keys), AFTER_SPRING, arrays, meta, resources=_measured())
    assert item['status'] == 'ok'
    assert item['partial'] == {'issued_hours': 23, 'canonical_hours': 24,
                               'missing_hours': ['00:00 Europe/Berlin (2026-03-29T22:00:00+00:00)']}
    decision = issue.decide(AFTER_SPRING, True, lambda p: item, _finalize)
    assert decision['display'] == 'successful daily fit (partial: 23 of 24 hours; missing 00:00 Europe/Berlin)'
    art = decision['artifact']
    assert art['partial'] == item['partial'] and art['keys'] == keys and issue.verify_artifact(art) == []
    assert schema.validate(json.loads(json.dumps(art)), schema.SCHEMAS['fitted_artifact']) == []
    complete = issue.attempt('A1', lambda: result('A1', PLAIN, keys_of(PLAIN)), PLAIN, *payload('A1', PLAIN, keys_of(PLAIN)),
                             resources=_measured())
    assert complete['partial'] is None


def test_a_fallback_on_a_partial_day_is_displayed_as_both():
    keys = keys_of(AFTER_SPRING)[1:]
    loaded = {p: payload(p, AFTER_SPRING, keys) for p in ('A1', 'v4')}

    def attempts(p):
        fit = (lambda: (_ for _ in ()).throw(dailyfit.FitFailure('nonfinite loss'))) if p == 'A1' else \
            (lambda: result(p, AFTER_SPRING, keys))
        return issue.attempt(p, fit, AFTER_SPRING, *loaded[p], resources=_measured())
    decision = issue.decide(AFTER_SPRING, True, attempts, _finalize)
    assert decision['display'] == 'failed fit; fallback v4 issued (partial: 23 of 24 hours; missing 00:00 Europe/Berlin)'


@pytest.mark.parametrize('emitted, why', [
    (lambda k: k + [keys_of(AFTER_SPRING)[0]], 'an extra hour'),               # emits an hour the design cannot forecast
    (lambda k: k[:-1], 'a missing forecastable hour'),
    (lambda k: k[::-1], 'reordered keys'),
    (lambda k: k[:1] + k[:-1], 'a duplicated hour'),
])
def test_the_emission_must_be_exactly_the_forecastable_hours(emitted, why):
    keys = keys_of(AFTER_SPRING)[1:]
    arrays, meta = payload('A1', AFTER_SPRING, keys)
    item = issue.attempt('A1', lambda: result('A1', AFTER_SPRING, emitted(keys)), AFTER_SPRING, arrays, meta,
                         resources=_measured())
    assert item['status'] == 'failed' and item['cause'].startswith('emission:'), why


def test_a_forecastable_key_outside_the_day_is_refused():
    other = keys_of(PLAIN)[:3]
    assert issue.check_emission(result('A1', AFTER_SPRING, other), AFTER_SPRING, other)[0].startswith('a forecastable key')


def test_the_partial_record_is_checked_by_the_verifier_and_the_bundle_schema():
    keys = keys_of(AFTER_SPRING)[1:]
    decision = issue.decide(AFTER_SPRING, True, lambda p: issue.attempt(
        p, lambda: result(p, AFTER_SPRING, keys), AFTER_SPRING, *payload(p, AFTER_SPRING, keys), resources=_measured()),
        _finalize)
    art = decision['artifact']
    wrong = dict(art, partial=None)
    wrong['artifact_sha256'] = __import__('hashlib').sha256(dailyfit.canonical({k: v for k, v in wrong.items()
                                                                                  if k != 'artifact_sha256'})).hexdigest()
    assert 'the partial-day record does not name exactly the missing hours' in issue.verify_artifact(wrong)
    day = {'delivery_day': str(AFTER_SPRING), 'issue_utc': art['issue_utc'], 'issuing_artifact_sha256': art['artifact_sha256'],
           'issued_policy': 'A1', 'display': art['display'], 'keys': keys, 'quantiles': art['quantiles'],
           'partial': art['partial']}
    forecasts = {'schema': schema.ISSUED_FORECASTS_SCHEMA, 'levels': [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975], 'days': [day]}
    assert schema.validate(forecasts, schema.SCHEMAS['issued_forecasts']) == []
    assert schema.validate({**forecasts, 'days': [{k: v for k, v in day.items() if k != 'partial'}]},
                           schema.SCHEMAS['issued_forecasts'])           # v2 requires the partial record
    assert schema.validate({**forecasts, 'schema': 'cp17-issued-forecasts-v1'}, schema.SCHEMAS['issued_forecasts'])


# ------------------------------------------------------------------ N3: criterion 4 inside the chain
def test_an_artifact_that_does_not_verify_fails_its_fit_and_the_chain_moves_on():
    seen = []

    def finalize(decision):
        seen.append(decision['issued_policy'])
        art = _artifact(decision)
        if decision['issued_policy'] == 'A1':
            art['quantiles_sha256'] = '0' * 64                        # an artifact that does not verify
        return art
    decision = issue.decide(PLAIN, True, lambda p: issue.attempt(p, lambda: result(p, PLAIN, keys_of(PLAIN)), PLAIN,
                                                                 resources=_measured()), finalize)
    assert seen == ['A1', 'v4']
    assert [(a['policy'], a['status']) for a in decision['attempts']] == [('A1', 'failed'), ('v4', 'ok')]
    assert decision['attempts'][0]['cause'].startswith('artifact:') and decision['issued_policy'] == 'v4'
    assert decision['artifact']['issued_policy'] == 'v4' and issue.verify_artifact(decision['artifact']) == []


def test_an_artifact_that_cannot_be_written_fails_its_fit():
    def finalize(decision):
        if decision['issued_policy'] in ('A1', 'v4'):
            raise OSError('disk full')
        return _artifact(decision)
    decision = issue.decide(PLAIN, True, lambda p: issue.attempt(p, lambda: result(p, PLAIN, keys_of(PLAIN)), PLAIN,
                                                                 resources=_measured()), finalize)
    assert [(a['policy'], a['status']) for a in decision['attempts']] == [('A1', 'failed'), ('v4', 'failed'), ('v2', 'ok')]
    assert 'OSError: disk full' in decision['attempts'][0]['cause']


# ------------------------------------------------------------------ N2: an issued artifact carries its measurement
def test_the_native_comparison_can_never_issue():
    native = issue.attempt('A1', lambda: result('A1', PLAIN, keys_of(PLAIN)), PLAIN)
    assert native['status'] == 'ok' and native['resources'] == issue.COMPARISON
    decision = issue.decide(PLAIN, True, lambda p: native)
    with pytest.raises(ValueError, match='resource measurement'):
        _artifact(decision)
    # inside the chain, an unmeasured fit cannot become the issued artifact: every policy fails at criterion 4
    unmeasured = issue.decide(PLAIN, True, lambda p: issue.attempt(p, lambda: result(p, PLAIN, keys_of(PLAIN)), PLAIN),
                              _finalize)
    assert unmeasured['issued_policy'] is None and all(a['cause'].startswith('artifact:') for a in unmeasured['attempts'])


@pytest.mark.parametrize('resources, why', [
    (None, 'absent'), ('not judged: criterion 5 is measured on the issuing host', "CP-17's native label"),
    ({'wall_seconds': 80.0}, 'no peak'), ({'wall_seconds': 900.001, 'peak_bytes': 1}, 'over 900 s'),
    ({'wall_seconds': 1.0, 'peak_bytes': 4 * 1024 ** 3 + 1}, 'over 4 GiB'), ({'wall_seconds': 1.0, 'peak_bytes': True}, 'a bool'),
])
def test_the_schema_and_the_verifier_refuse_an_issued_artifact_without_a_valid_measurement(resources, why):
    art = _artifact(issue.decide(PLAIN, True, lambda p: issue.attempt(p, lambda: result(p, PLAIN, keys_of(PLAIN)), PLAIN,
                                                                      resources=_measured())))
    art['resources'] = resources if not isinstance(resources, dict) else \
        {**resources, 'limits': {'wall_seconds': 900, 'peak_bytes': 4 * 1024 ** 3}}
    art['artifact_sha256'] = __import__('hashlib').sha256(dailyfit.canonical({k: v for k, v in art.items()
                                                                                if k != 'artifact_sha256'})).hexdigest()
    assert issue.verify_artifact(art), why
    assert schema.validate(json.loads(json.dumps(art)), schema.SCHEMAS['fitted_artifact']), why


def test_a_failed_issuance_carries_no_forecast_and_no_measurement():
    decision = issue.decide(PLAIN, True, lambda p: issue.attempt(p, lambda: result(p, PLAIN, keys_of(PLAIN)), PLAIN,
                                                                 resources=_measured(901.0)), _finalize)
    art = decision['artifact']
    assert art['issued_policy'] is None and schema.validate(json.loads(json.dumps(art)), schema.SCHEMAS['fitted_artifact']) == []
    forged = dict(art, keys=keys_of(PLAIN))      # the failed form admits no keys
    assert schema.validate(json.loads(json.dumps(forged)), schema.SCHEMAS['fitted_artifact'])


# ------------------------------------------------------------------ N7: the ceiling's message reports wall time exactly
def test_the_ceiling_message_reports_wall_time_exactly():
    assert issue.resources_ok(900.0, 4 * 1024 ** 3) == []
    assert issue.resources_ok(900.001, 1) == ['wall time 900.001 s over the 900 s (15-minute) ceiling']
    assert issue.resources_ok(900.0000000001, 1)[0].startswith('wall time 900.0000000001 s')
    assert issue.resources_ok(1, 4 * 1024 ** 3 + 1) == [
        'peak memory 4294967297 bytes over the 4294967296-byte (4 GiB) ceiling']


def test_the_artifact_schema_name_is_the_package_constant():
    assert issue.SCHEMA == schema.ARTIFACT_SCHEMA == 'cp17b-issued-artifact-v2'
    assert schema.validate(901, {'type': 'number', 'maximum': 900}) and not schema.validate(900, {'type': 'number', 'maximum': 900})


def test_quantile_helpers_are_shared():
    assert np.asarray(flat(3)).shape == (3, 7) and FIT == (80.0, 10 ** 9)
