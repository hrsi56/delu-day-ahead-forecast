"""The frozen issuance driver `cp17.daily` and the shadow states `cp17.shadow` (CI-safe).

- **N1.** Each attempt runs in its own process with a timeout and a fresh output path. A killed, timed-out,
  non-zero, recordless, unreadable or foreign attempt is a failed fit, and the chain moves on. The process here is
  a real one: a stand-in runner script under this interpreter, in place of Node.js and Pyodide, so the test needs
  neither. A stale record planted where a reused path would find it is never read.
- **Decision 14.** The shadows run every day, whether or not A1 succeeds; a fallback the chain fitted is not fitted
  twice; a day with no forecastable hour fits nothing; v4's shadow is skipped when GFS is unavailable; a shadow is
  registered under CP-26's intake rule and released once, after D-2.
"""
from __future__ import annotations

from datetime import date, timedelta
import json
from pathlib import Path
import sys
import time

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cp17 import daily, dailyfit, issue, schema  # noqa: E402
from cp17.shadow import ShadowStates  # noqa: E402
from cp17b_synthetic import buffer, keys_of, payload, result  # noqa: E402

DAY = date(2026, 9, 6)
IDENTITY = {'policy_identity_sha256': '1' * 64, 'package_sha256': '2' * 64}

RUNNER = r'''
import json, os, signal, sys, time
mode, pyodide, package, payloads, stem, flag, packages, out = sys.argv[1:9]
behaviour = os.environ['CP17B_FAKE']
policy, day = stem.split('-', 1)
record = {'target': stem, 'mode': mode, 'errors': [], 'total_ms': 1500.0, 'process_rss_peak_bytes': 123456789,
          'python': {'result': {'policy': policy, 'day': day, 'index': [], 'quantiles': []}},
          'blocked_non_local_requests': [], 'node': 'v26.7.0', 'pyodide_version': '0.28.0'}
if behaviour == 'sleep':
    time.sleep(60)
elif behaviour == 'selfkill':
    os.kill(os.getpid(), signal.SIGKILL)
elif behaviour == 'die':
    sys.exit(3)
elif behaviour == 'garbage':
    open(out, 'w').write('{"target": ')
elif behaviour == 'foreign':
    record['target'] = 'A1-2026-09-05'
    json.dump(record, open(out, 'w'))
elif behaviour == 'unmeasured':
    record.pop('process_rss_peak_bytes')
    json.dump(record, open(out, 'w'))
elif behaviour == 'nonzero':
    json.dump(record, open(out, 'w'))
    sys.exit(1)
elif behaviour == 'ok':
    json.dump(record, open(out, 'w'))
'''


@pytest.fixture()
def host(tmp_path, monkeypatch):
    script = tmp_path / 'runner.py'
    script.write_text(RUNNER)

    def make(behaviour, timeout=30.0):
        monkeypatch.setenv('CP17B_FAKE', behaviour)
        return daily.Host(tmp_path / 'pyodide', tmp_path / 'src.zip', node=sys.executable, timeout=timeout, runner=script)
    return make


def test_a_process_over_its_timeout_is_killed_and_is_a_failed_attempt(host, tmp_path):
    started = time.perf_counter()
    run = host('sleep', timeout=1.0).run(tmp_path, f'A1-{DAY}', tmp_path / 'out')
    assert time.perf_counter() - started < 30
    assert run['errors'] == ['the issuing-host process exceeded the 1.0 s timeout and was killed']
    assert run['process_rss_peak_bytes'] is None


@pytest.mark.parametrize('behaviour, error', [
    ('selfkill', 'the issuing-host process left no record (exit -9)'),
    ('die', 'the issuing-host process left no record (exit 3)'),
    ('garbage', 'the issuing-host process left an unreadable record (JSONDecodeError)'),
    ('foreign', 'the issuing-host record is of another run'),
    ('unmeasured', 'the issuing-host record lacks its measurement'),
    ('nonzero', 'the issuing-host process exited 1'),
])
def test_a_dead_or_unreadable_attempt_is_a_failed_attempt(host, tmp_path, behaviour, error):
    run = host(behaviour).run(tmp_path, f'A1-{DAY}', tmp_path / 'out')
    assert run['errors'] == [error]


def test_a_stale_record_is_never_read(host, tmp_path):
    out = tmp_path / 'out'
    out.mkdir()
    stale = {'target': f'A1-{DAY}', 'mode': 'fit', 'errors': [], 'total_ms': 1.0, 'process_rss_peak_bytes': 1,
             'python': {'result': result('A1', DAY, keys_of(DAY))}}
    for name in ('run.json', f'node-attempt-A1-{DAY}.json', f'node-A1-{DAY}.json'):
        (out / name).write_text(json.dumps(stale))
    h = host('die')
    first, second = h.run(tmp_path, f'A1-{DAY}', out), h.run(tmp_path, f'A1-{DAY}', out)
    assert first['errors'] == second['errors'] == ['the issuing-host process left no record (exit 3)']
    assert first['folder'] != second['folder'] and Path(first['folder']).parent == out   # a fresh path each time
    ok = host('ok').run(tmp_path, f'A1-{DAY}', out)
    assert not ok.get('errors') and ok['process_rss_peak_bytes'] == 123456789 and ok['folder'] not in (first['folder'], second['folder'])


def test_a_successful_record_must_hold_this_attempts_fit():
    good = {'target': f'v4-{DAY}', 'mode': 'fit', 'total_ms': 1.0, 'process_rss_peak_bytes': 1,
            'python': {'result': {'policy': 'v4', 'day': str(DAY)}}}
    assert daily.record_problems(good, f'v4-{DAY}') == []
    assert daily.record_problems({**good, 'python': {'result': {'policy': 'v2', 'day': str(DAY)}}}, f'v4-{DAY}')
    assert daily.record_problems({**good, 'python': {}}, f'v4-{DAY}')
    assert daily.record_problems({**good, 'errors': ['MemoryError'], 'python': None}, f'v4-{DAY}') == []   # its own failure
    assert daily.record_problems([], f'v4-{DAY}')


# ------------------------------------------------------------------ the day's issuance, with a synthetic host
class SyntheticHost(daily.Host):
    """Returns each attempt's record as the issuing host would, without a process; `dead` policies' processes die."""

    def __init__(self, day, keys, dead=(), wall=80.0):
        super().__init__(Path('pyodide'), Path('src.zip'))
        self.day, self.keys, self.dead, self.wall, self.calls = day, keys, set(dead), wall, []

    def run(self, payloads, stem, out):
        self.calls.append(stem)
        policy = stem.split('-', 1)[0]
        if policy in self.dead:
            return daily._failed(stem, ['the issuing-host process exceeded the 900 s timeout and was killed'],
                                 time.perf_counter(), Path(out))
        base = {'A1': 10.0, 'v4': 20.0, 'v2': 30.0, 'B0': 40.0}[policy]
        return {'target': stem, 'mode': 'fit', 'errors': [], 'total_ms': self.wall * 1000, 'process_rss_peak_bytes': 10 ** 9,
                'python': {'result': result(policy, self.day, self.keys, base)}, 'node': 'v26.7.0',
                'pyodide_version': '0.28.0', 'blocked_non_local_requests': [], 'folder': str(out)}


def _write(folder: Path, day: date, keys):
    for p in ('A1', 'v4', 'v2', 'B0'):
        arrays, meta = payload(p, day, keys)
        from cp17.tools.payloads import write
        write(arrays, meta, folder, f'{p}-{day}')


def _states(day: date) -> ShadowStates:
    return ShadowStates.from_buffers(day, {p: buffer(day) for p in ('v4', 'v2', 'B0')})


def test_a_killed_a1_moves_the_chain_and_the_shadows_still_run(tmp_path):
    _write(tmp_path / 'p', DAY, keys_of(DAY))
    host, states = SyntheticHost(DAY, keys_of(DAY), dead={'A1'}), _states(DAY)
    day = daily.issue_day(DAY, True, tmp_path / 'p', host=host, out=tmp_path / 'runs', identity=IDENTITY, states=states)
    assert [(a['policy'], a['status']) for a in day['decision']['attempts']] == [('A1', 'failed'), ('v4', 'ok')]
    assert 'killed' in day['decision']['attempts'][0]['cause'] and day['decision']['display'] == 'failed fit; fallback v4 issued'
    art = day['artifact']
    assert art['issued_policy'] == 'v4' and issue.verify_artifact(art) == []
    assert schema.validate(json.loads(json.dumps(art)), schema.SCHEMAS['fitted_artifact']) == []
    assert all(row[3] == 20.0 for row in art['quantiles'])                    # v4's own forecast
    assert host.calls == [f'A1-{DAY}', f'v4-{DAY}', f'v2-{DAY}', f'B0-{DAY}']   # v4 fitted once, by the chain
    assert {p: s['fitted_by'] for p, s in day['shadows'].items()} == {'v4': 'chain', 'v2': 'shadow', 'B0': 'shadow'}
    assert {p: s['intake'] for p, s in day['shadows'].items()} == dict.fromkeys(('v4', 'v2', 'B0'), 'registered')


def test_the_shadows_run_on_a_normal_day_and_are_never_the_issued_forecast(tmp_path):
    _write(tmp_path / 'p', DAY, keys_of(DAY))
    host, states = SyntheticHost(DAY, keys_of(DAY)), _states(DAY)
    day = daily.issue_day(DAY, True, tmp_path / 'p', host=host, out=tmp_path / 'runs', identity=IDENTITY, states=states)
    assert day['decision']['issued_policy'] == 'A1' and day['decision']['display'] == 'successful daily fit'
    assert all(row[3] == 10.0 for row in day['artifact']['quantiles'])
    assert host.calls == [f'{p}-{DAY}' for p in ('A1', 'v4', 'v2', 'B0')]
    assert all(s['status'] == 'ok' and s['intake'] == 'registered' and s['role'].startswith('shadow') for s in day['shadows'].values())
    assert day['process_seconds_sum'] == 320.0 and day['artifact']['resources']['wall_seconds'] == 80.0


def test_v4s_shadow_is_skipped_when_gfs_is_unavailable(tmp_path):
    _write(tmp_path / 'p', DAY, keys_of(DAY))
    host = SyntheticHost(DAY, keys_of(DAY))
    day = daily.issue_day(DAY, False, tmp_path / 'p', host=host, out=tmp_path / 'runs', identity=IDENTITY, states=_states(DAY))
    assert day['decision']['display'] == 'skipped fit (GFS late or missing); fallback v2 issued'
    assert day['shadows']['v4']['status'] == 'skipped' and 'intake' not in day['shadows']['v4']
    assert host.calls == [f'v2-{DAY}', f'B0-{DAY}']


def test_a_day_with_no_forecastable_hour_starts_no_process(tmp_path):
    _write(tmp_path / 'p', DAY, [])
    host = SyntheticHost(DAY, [])
    day = daily.issue_day(DAY, True, tmp_path / 'p', host=host, out=tmp_path / 'runs', identity=IDENTITY, states=_states(DAY))
    assert host.calls == [] and day['artifact']['issued_policy'] is None
    assert day['decision']['display'] == f'failed issuance ({issue.NO_FORECASTABLE_HOUR})'
    assert issue.verify_artifact(day['artifact']) == []
    assert all(s['intake'] == 'no intake: the fit failed' for s in day['shadows'].values())


def test_a_partial_day_issues_and_its_shadows_are_not_taken_into_the_buffers(tmp_path):
    day_ = date(2026, 3, 30)
    keys = keys_of(day_)[1:]
    _write(tmp_path / 'p', day_, keys)
    states = _states(day_)
    day = daily.issue_day(day_, True, tmp_path / 'p', host=SyntheticHost(day_, keys), out=tmp_path / 'runs',
                          identity=IDENTITY, states=states)
    assert day['artifact']['partial']['missing_hours'] == ['00:00 Europe/Berlin (2026-03-29T22:00:00+00:00)']
    assert {s['intake'] for s in day['shadows'].values()} == {'no intake: not a complete canonical issuance'}   # CP-26's rule


# ------------------------------------------------------------------ the shadow states
def test_shadow_errors_enter_their_own_buffer_once_after_d_minus_2():
    states = _states(DAY)
    before = states.digest()
    for p, scale in (('v4', 2.0), ('v2', 2.0), ('B0', None)):
        r = result(p, DAY, keys_of(DAY), base=40.0)
        assert states.issue(p, DAY, r) == 'registered'
    assert states.digest() == before                                    # registered before the outcome, not released
    truth = lambda index: np.full(len(index), 50.0)                     # noqa: E731
    states.release(DAY + timedelta(days=1), truth)
    assert states.digest() == before                                    # D-1 < D + 2: not yet released
    states.release(DAY + timedelta(days=2), truth)
    for p in ('v4', 'v2', 'B0'):
        buf = states.buffer(p)
        # the buffer held D-29..D-2; D enters (D-1 was never issued here) and the oldest day, D-29, leaves
        assert len(buf) == 28 and buf[-1]['day'] == str(DAY) and buf[0]['day'] == str(DAY - timedelta(days=28))
        expected = 5.0 if p != 'B0' else 10.0                           # (50 - 40) / scale 2; B0 raw
        assert buf[-1]['errors'] == [expected] * 24
    states.release(DAY + timedelta(days=3), truth)
    assert states.buffer('v4')[-1]['day'] == str(DAY)                   # consumed once
    assert ShadowStates.from_dict(json.loads(json.dumps(states.to_dict()))).digest() == states.digest()


@pytest.mark.parametrize('change, outcome', [
    (lambda r: None, 'no intake: the fit failed'),
    (lambda r: {**r, 'index': r['index'][1:]}, 'no intake: not a complete canonical issuance'),
    (lambda r: {**r, 'central': [float('nan')] + r['central'][1:]}, 'no intake: nonfinite central'),
    (lambda r: {**r, 'scale': [0.5] * len(r['index'])}, 'no intake: invalid issued scale'),
])
def test_the_intake_rule_is_cp26s(change, outcome):
    states = _states(DAY)
    assert states.issue('v4', DAY, change(result('v4', DAY, keys_of(DAY)))) == outcome


def test_a_day_is_registered_once():
    states = _states(DAY)
    assert states.issue('B0', DAY, result('B0', DAY, keys_of(DAY))) == 'registered'
    with pytest.raises(ValueError, match='already registered'):
        states.issue('B0', DAY, result('B0', DAY, keys_of(DAY)))


def test_the_driver_and_the_package_share_the_pinned_packages():
    from cp17.tools import bundle
    assert bundle.PACKAGES == daily.PACKAGES and 'cp17/daily.py' in bundle.PIPELINE
    assert 'cp17.shadow' in bundle.ENTRY and 'cp17.daily' not in bundle.ENTRY        # the driver never ships
    assert daily.TIMEOUT_SECONDS == issue.WALL_LIMIT_SECONDS == 900
    assert dailyfit.FitFailure.__name__ == 'FitFailure'
