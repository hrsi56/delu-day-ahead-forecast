"""CP-17c's re-frozen rules on synthetic inputs (CI-safe): R7's narrow fix (H3), the issuing host's pins and its
retrieval, the checks before each run's first issuance (H2), each failing on its own, and the state store.
"""
from __future__ import annotations

from datetime import date
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'cp17b'))
from cp17 import daily, hostcheck, issue, runtime, schema  # noqa: E402
from cp17.tools import bundle, hosts  # noqa: E402
from cp17b_synthetic import keys_of, payload, result  # noqa: E402
from cp17c.store import Store, StoreRefused  # noqa: E402

PLAIN, AFTER_SPRING = date(2026, 9, 6), date(2026, 3, 30)
LEVELS = [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975]


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# ------------------------------------------------------------------ R7 (H3): a malformed day is listed, not raised
def _day(day: date, keys: list[str], partial=None) -> dict:
    return {'delivery_day': str(day), 'issue_utc': issue.issue_utc(day), 'issuing_artifact_sha256': '1' * 64,
            'issued_policy': 'A1', 'display': 'successful daily fit', 'keys': keys,
            'quantiles': [[float(i) for i in range(7)] for _ in keys], 'partial': partial}


def _bundle(days: list) -> dict[str, bytes]:
    """A bundle whose issued-forecasts record is re-hashed in its manifest, so only the record's content can fail."""
    forecasts = json.dumps({'schema': schema.ISSUED_FORECASTS_SCHEMA, 'levels': LEVELS, 'days': days}).encode()
    manifest = {'schema': 'cp17-manifest-v1',
                'product': {'name': 'delu-day-ahead-policy', 'designated_policy': 'A1', 'evidence_label': 'test'},
                'policy': {'policy_identity_sha256': '2' * 64, 'package_sha256': '3' * 64, 'issuing_host': 'test'},
                'artifact': {'artifact_sha256': '1' * 64, 'delivery_day': str(PLAIN), 'issued_policy': 'A1',
                             'display': 'successful daily fit'},
                'times': {'last_training_utc': issue.issue_utc(PLAIN), 'data_refresh_utc': '',
                          'issuance_utc': issue.issue_utc(PLAIN)},
                'freshness': {'state': 'fresh', 'as_of_day': str(PLAIN), 'latest_issued_day': str(PLAIN)},
                'files': [{'path': 'issued-forecasts.json', 'sha256': sha(forecasts), 'bytes': len(forecasts),
                           'kind': 'issued_forecasts'}]}
    assert schema.validate(manifest, schema.SCHEMAS['manifest']) == []
    return {'manifest.json': json.dumps(manifest).encode(), 'issued-forecasts.json': forecasts}


R7 = 'is malformed, so it is listed and not read (R7)'


@pytest.mark.parametrize('break_day', [
    lambda d: d.pop('delivery_day'), lambda d: d.pop('keys'), lambda d: d.update(delivery_day='2026-13-45'),
    lambda d: d.update(keys=5), lambda d: d.update(keys=[3, 4]), lambda d: d.update(delivery_day=None),
])
def test_a_malformed_day_in_a_re_hashed_record_is_listed_not_raised(break_day):
    good, bad = _day(PLAIN, keys_of(PLAIN)), _day(PLAIN, keys_of(PLAIN))
    break_day(bad)
    errors = schema.verify_bundle(_bundle([good, bad]))
    assert f'issued-forecasts.json: day 1 {R7}' in errors
    assert not any('day 0' in e for e in errors)                  # the well-formed day is still judged, and passes


@pytest.mark.parametrize('days', ['garbage', [None], ['a string'], {'days': 1}])
def test_a_malformed_record_structure_is_listed_not_raised(days):
    errors = schema.verify_bundle(_bundle(days))
    assert errors                                                  # never raises, always refuses


def test_a_well_formed_record_is_judged_exactly_as_before():
    """The fix changes the error path only: a well-formed day gets no R7 line; a wrong partial record is still refused
    with CP-17b's own message; a correct partial day passes."""
    keys = keys_of(AFTER_SPRING)[1:]
    right = issue.partial(AFTER_SPRING, keys)
    errors = schema.verify_bundle(_bundle([_day(AFTER_SPRING, keys, right)]))
    assert not any('R7' in e or 'missing hours' in e for e in errors)
    errors = schema.verify_bundle(_bundle([_day(AFTER_SPRING, keys, None)]))
    assert 'issued-forecasts.json: day 0 does not name exactly its missing hours (decision 13)' in errors
    assert not any('R7' in e for e in errors)


def test_the_fix_leaves_the_schemas_unchanged():
    assert schema.DAY_ITEM is schema.SCHEMAS['issued_forecasts']['properties']['days']['items']
    assert schema.ARTIFACT_SCHEMA == 'cp17b-issued-artifact-v2' and schema.ISSUED_FORECASTS_SCHEMA == 'cp17b-issued-forecasts-v2'


# ------------------------------------------------------------------ the issuing host's pins (H1)
def test_the_pins_are_section_24_13s():
    assert runtime.TARBALL == {'name': 'node-v26.7.0-darwin-arm64.tar.gz', 'bytes': 57_622_243,
                               'sha256': '7ee659a7768e641bbfd5360940660b8e8fd0052f77488f365562bac522fc15d4'}
    assert runtime.BINARY == {'bytes': 145_238_560,
                              'sha256': 'a9bd0630891c2dcdee70de88270fee2cc0c4a9e76495039dd3b4f91c5e6b71df'}
    assert runtime.NODE_DIST == 'https://nodejs.org/dist/v26.7.0/'
    assert runtime.CPYTHON == '3.13.15' and runtime.ZLIB_RUNTIME == '1.2.12'
    assert runtime.MACHINE == {'system': 'Darwin', 'machine': 'arm64', 'runner_label': 'macos-26', 'image_os': 'macos26'}
    assert runtime.PYODIDE_DIR == '.local/tools/pyodide-0.28.0'


def test_the_homebrew_defaults_are_replaced_by_the_official_binary():
    assert daily.NODE == runtime.NODE_RELATIVE and not Path(daily.NODE).is_absolute()
    assert '/opt/homebrew' not in daily.NODE and '/opt/homebrew' not in hosts.NODE
    assert hosts.NODE_SHA256 == runtime.BINARY['sha256'] and hosts.NODE.endswith(runtime.NODE_RELATIVE)
    made = daily.Host('/p', '/z')
    assert Path(made.node).is_absolute() and made.node.endswith(runtime.NODE_RELATIVE)
    assert daily.Host('/p', '/z', node='/x/node').node == '/x/node'


def test_the_new_pipeline_modules_are_frozen_and_never_shipped():
    assert bundle.PIPELINE == ('cp17/daily.py', 'cp17/runtime.py', 'cp17/hostcheck.py')
    closure = bundle.closure(Path(__file__).resolve().parents[2] / 'src')['files']
    assert not {'cp17/daily.py', 'cp17/runtime.py', 'cp17/hostcheck.py'} & set(closure)


def _release(tmp: Path, binary: bytes, listed_ok: bool = True):
    """A fake release: SHASUMS256.txt and a tarball holding bin/node, served by a fake fetch."""
    name = runtime.TARBALL['name']
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode='w:gz') as tar:
        info = tarfile.TarInfo(f"{name.removesuffix('.tar.gz')}/bin/node")
        info.size, info.mode = len(binary), 0o755
        tar.addfile(info, io.BytesIO(binary))
    tarball = buf.getvalue()
    sums = f"{sha(tarball) if listed_ok else '0' * 64}  {name}\n{'9' * 64}  other.tar.gz\n".encode()
    served = {runtime.NODE_DIST + 'SHASUMS256.txt': sums, runtime.NODE_DIST + name: tarball}

    def fetch(url, target):
        Path(target).write_bytes(served[url])
        return {'url': url, 'bytes': len(served[url]), 'sha256': sha(served[url]), 'seconds': 0.0}
    pins = {'TARBALL': {**runtime.TARBALL, 'bytes': len(tarball), 'sha256': sha(tarball)},
            'BINARY': {'bytes': len(binary), 'sha256': sha(binary)},
            'SHASUMS': {**runtime.SHASUMS, 'bytes': len(sums), 'sha256': sha(sums)}}
    return fetch, pins


def test_retrieval_places_the_binary_only_when_every_hash_holds(tmp_path, monkeypatch):
    fetch, pins = _release(tmp_path, b'a node binary')
    for k, v in pins.items():
        monkeypatch.setattr(runtime, k, v)
    record = runtime.retrieve(tmp_path, fetch=fetch)
    assert record['binary']['sha256'] == sha(b'a node binary')
    assert runtime.check_binary(tmp_path)['problems'] == []
    (tmp_path / runtime.NODE_RELATIVE).write_bytes(b'a node binary, altered')
    assert runtime.check_binary(tmp_path)['problems']


@pytest.mark.parametrize('broken', ['shasums', 'listing', 'tarball', 'binary'])
def test_a_failed_hash_retrieves_nothing(tmp_path, monkeypatch, broken):
    fetch, pins = _release(tmp_path, b'a node binary', listed_ok=broken != 'listing')
    if broken == 'listing':
        pins['SHASUMS'] = {**pins['SHASUMS']}
    for k, v in pins.items():
        monkeypatch.setattr(runtime, k, v)
    if broken == 'shasums':
        monkeypatch.setattr(runtime, 'SHASUMS', {**pins['SHASUMS'], 'sha256': 'f' * 64})
    elif broken == 'tarball':
        monkeypatch.setattr(runtime, 'TARBALL', {**pins['TARBALL'], 'sha256': 'f' * 64})
    elif broken == 'binary':
        monkeypatch.setattr(runtime, 'BINARY', {**pins['BINARY'], 'sha256': 'f' * 64})
    with pytest.raises(RuntimeError):
        runtime.retrieve(tmp_path, fetch=fetch)
    assert not (tmp_path / runtime.NODE_RELATIVE).exists()


# ------------------------------------------------------------------ H2: each check, failing on its own
def _passing(name):
    return lambda: {'check': name, 'passed': True, 'problems': []}


def _failing(name):
    return lambda: {'check': name, 'passed': False, 'problems': [f'{name} forced']}


@pytest.mark.parametrize('broken', hostcheck.ORDER)
def test_each_check_fails_the_gate_on_its_own_and_nothing_after_it_runs(broken):
    ran = []

    def track(name, fn):
        return lambda: (ran.append(name), fn())[1]
    checks = {n: track(n, _failing(n) if n == broken else _passing(n)) for n in hostcheck.ORDER}
    record = hostcheck.gate(checks)
    i = hostcheck.ORDER.index(broken)
    assert not record['passed'] and record['failed'] == broken
    assert ran == list(hostcheck.ORDER[:i + 1]) and record['not_run'] == list(hostcheck.ORDER[i + 1:])
    assert record['consequence'] == 'nothing in this run is issued'


def test_a_check_that_raises_fails_the_gate():
    def boom():
        raise OSError('no machine')
    record = hostcheck.gate({**{n: _passing(n) for n in hostcheck.ORDER}, 'machine': boom})
    assert record['failed'] == 'machine' and 'OSError' in record['checks'][-1]['problems'][0]


def test_the_run_issues_only_after_every_check_passes(monkeypatch):
    called = []
    for name in hostcheck.ORDER:
        monkeypatch.setattr(hostcheck, name, lambda *a, _n=name, **k: _passing(_n)())
    assert hostcheck.run('.', '.', None, '.', '.', lambda: called.append(1) or 'issued')['issued'] == 'issued'
    monkeypatch.setattr(hostcheck, 'binary', lambda *a, **k: _failing('binary')())
    out = hostcheck.run('.', '.', None, '.', '.', lambda: called.append(2) or 'issued')
    assert out['issued'] is None and called == [1] and out['checks']['failed'] == 'binary'


class _Done:
    def __init__(self, stdout, returncode=0):
        self.stdout, self.returncode = stdout, returncode


@pytest.mark.parametrize('stdout, code, passed', [
    ('verified\n', 0, True),
    ('verified, except 27 local runtime or state files absent on this machine (unchecked, not passed):\nx: absent', 0, False),
    ('src/cp17/schema.py: missing or altered', 1, False),
    ('verified', 1, False),
])
def test_the_pins_check_reads_the_verifiers_output(monkeypatch, stdout, code, passed):
    monkeypatch.setattr(hostcheck.subprocess, 'run', lambda *a, **k: _Done(stdout, code))
    assert hostcheck.pins('.')['passed'] is passed


def test_the_binary_check(tmp_path, monkeypatch):
    (tmp_path / runtime.NODE_RELATIVE).parent.mkdir(parents=True)
    (tmp_path / runtime.TARBALL_RELATIVE).parent.mkdir(parents=True)
    (tmp_path / runtime.NODE_RELATIVE).write_bytes(b'node')
    (tmp_path / runtime.TARBALL_RELATIVE).write_bytes(b'tar')
    assert not hostcheck.binary(tmp_path)['passed']                # not the pinned bytes
    monkeypatch.setattr(runtime, 'BINARY', {'bytes': 4, 'sha256': sha(b'node')})
    monkeypatch.setattr(runtime, 'TARBALL', {**runtime.TARBALL, 'bytes': 3, 'sha256': sha(b'tar')})
    assert hostcheck.binary(tmp_path)['passed']
    (tmp_path / runtime.TARBALL_RELATIVE).unlink()
    assert not hostcheck.binary(tmp_path)['passed']                # a missing tarball fails it too


@pytest.mark.parametrize('described, env, passed', [
    ({'system': 'Darwin', 'machine': 'arm64'}, {}, True),                                         # the Owner's Mac
    ({'system': 'Darwin', 'machine': 'arm64'}, {'GITHUB_ACTIONS': 'true', 'ImageOS': 'macos26'}, True),
    ({'system': 'Darwin', 'machine': 'arm64'}, {'GITHUB_ACTIONS': 'true', 'ImageOS': 'macos15'}, False),
    ({'system': 'Darwin', 'machine': 'arm64'}, {'GITHUB_ACTIONS': 'true'}, False),
    ({'system': 'Darwin', 'machine': 'x86_64'}, {}, False),
    ({'system': 'Linux', 'machine': 'x86_64'}, {'GITHUB_ACTIONS': 'true', 'ImageOS': 'ubuntu24'}, False),
])
def test_the_machine_check(described, env, passed):
    found = {**described, 'runner_env': env}
    record = hostcheck.machine(env, found)
    assert record['passed'] is passed
    if env.get('GITHUB_ACTIONS'):
        assert record['kind'] == 'GitHub-hosted runner'


class _Host:
    def __init__(self, run):
        self._run = run

    def run(self, payloads, stem, out):
        return self._run


def _canary_run(quantiles_ok=True, errors=None):
    keys = keys_of(PLAIN)
    fit = result('A1', PLAIN, keys)
    if errors:
        return {'errors': errors, 'total_ms': 1000.0, 'process_rss_peak_bytes': 10 ** 8}, fit
    return {'python': {'result': fit, 'source_sha256': {}}, 'total_ms': 80_000.0, 'process_rss_peak_bytes': 8 * 10 ** 8,
            'node': 'v26.7.0', 'errors': []}, fit


@pytest.mark.parametrize('case', ['equal', 'other', 'failed', 'over_ceiling'])
def test_the_canary_check(monkeypatch, tmp_path, case):
    from cp17 import dailyfit
    keys = keys_of(PLAIN)
    monkeypatch.setattr(dailyfit, 'load', lambda npz, meta: payload('A1', PLAIN, keys))
    run, fit = _canary_run(errors=['killed'] if case == 'failed' else None)
    if case == 'over_ceiling':
        run['total_ms'] = 901_000.0
    expected = fit['quantiles_sha256'] if case != 'other' else '0' * 64
    record = hostcheck.canary(_Host(run), tmp_path, tmp_path, expected=expected)
    assert record['passed'] is (case == 'equal')
    if case == 'over_ceiling':
        assert 'resources' in record['problems'][0]


def test_an_unreadable_canary_payload_fails_the_check(tmp_path):
    record = hostcheck.canary(_Host({}), tmp_path / 'absent', tmp_path)
    assert not record['passed'] and 'unreadable' in record['problems'][0]


def test_the_canary_is_a1_at_the_freeze_origin():
    assert hostcheck.CANARY_STEM == 'A1-2026-09-06'
    assert hostcheck.CANARY_QUANTILES_SHA256 == '4e6abb02fbb02aa8ef202207f21b76bc33b34c37d025a0a93a491135ea43cea5'
    assert hostcheck.ORDER == ('pins', 'binary', 'machine', 'canary')


# ------------------------------------------------------------------ the state store
class _State:
    """A stand-in for `ShadowStates` with the methods the store uses."""

    def __init__(self, n):
        self.n = n

    def to_dict(self):
        return {'n': self.n}

    def digest(self):
        return {'v4': str(self.n)}


def _artifact(day, parent):
    return {'artifact_sha256': sha(f'{day}'.encode()), 'issued_policy': 'A1', 'display': 'successful daily fit',
            'lineage': {'parent_artifact_sha256': parent}}


def _store(tmp_path, days=3):
    store = Store.init(tmp_path / 's', _State(0), date(2026, 8, 24), 'test')
    head = None
    for i in range(days):
        d = date(2026, 8, 24 + i)
        store.record_day(d, _State(i + 1), _artifact(d, head), {'day': str(d)}, {'v4': str(i)})
        head = sha(f'{d}'.encode())
    return store


def test_the_store_chains_and_verifies(tmp_path):
    store = _store(tmp_path)
    head = store.verify()
    assert head['entries'] == 4 and head['last_day'] == '2026-08-26' and store.issued_days()[-1] == '2026-08-26'
    assert store.last_artifact_sha256() == sha(b'2026-08-26')


@pytest.mark.parametrize('day', [date(2026, 8, 25), date(2026, 8, 20)])
def test_one_issuance_per_day_and_days_go_forward(tmp_path, day):
    store = _store(tmp_path)
    with pytest.raises(StoreRefused):
        store.record_day(day, _State(9), _artifact(day, None), {}, {'v4': '3'})


@pytest.mark.parametrize('tamper', ['state', 'artifact', 'entry', 'head', 'drop'])
def test_a_tampered_store_is_refused(tmp_path, tamper):
    store = _store(tmp_path)
    folder = store.folder
    if tamper == 'state':
        (folder / 'states/2026-08-25.json').write_text('{"n": 99}\n')
    elif tamper == 'artifact':
        (folder / 'issued/2026-08-25/artifact.json').write_text('{}\n')
    elif tamper == 'entry':
        lines = (folder / 'ledger.jsonl').read_text().splitlines()
        entry = json.loads(lines[2])
        entry['issued_policy'] = 'v4'
        lines[2] = json.dumps(entry, sort_keys=True)
        (folder / 'ledger.jsonl').write_text('\n'.join(lines) + '\n')
    elif tamper == 'head':
        head = json.loads((folder / 'head.json').read_text())
        head['entries'] = 2
        (folder / 'head.json').write_text(json.dumps(head))
    else:
        lines = (folder / 'ledger.jsonl').read_text().splitlines()
        (folder / 'ledger.jsonl').write_text('\n'.join(lines[:2] + lines[3:]) + '\n')
    with pytest.raises(StoreRefused):
        store.verify()


def test_a_store_is_never_re_initialized(tmp_path):
    _store(tmp_path, days=1)
    with pytest.raises(StoreRefused):
        Store.init(tmp_path / 's', _State(0), date(2026, 8, 24), 'again')


def test_a_broken_parent_state_is_refused(tmp_path):
    store = _store(tmp_path, days=1)
    store.record_day(date(2026, 8, 30), _State(5), _artifact(date(2026, 8, 30), None), {}, {'v4': 'not the last state'})
    with pytest.raises(StoreRefused):
        store.verify()
