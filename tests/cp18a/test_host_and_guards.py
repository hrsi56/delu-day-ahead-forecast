"""The issuing host's files by hash, and the guards on the pipeline's own commits and pushes (fake credentials only)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil

import pytest

from cp17 import runtime
from cp18 import guarddemo, host

ROOT = Path(__file__).resolve().parents[2]


def test_materialize_copies_each_pinned_state_by_hash_and_refuses_an_altered_one(tmp_path):
    pinned = host.pinned_files(ROOT)
    assert set(pinned) == {runtime.K13, runtime.FREEZE_STATE, f'{runtime.CANARY_DIR}/A1-2026-09-06.json',
                           f'{runtime.CANARY_DIR}/A1-2026-09-06.npz'}
    if not all((ROOT / host.committed_path(rel, host.DRY_RUN_PINNED)).is_file() for rel in pinned):
        pytest.skip('the dry run\'s committed pinned states are absent')
    done = host.materialize(ROOT, tmp_path, host.DRY_RUN_PINNED)
    assert all(v['action'] == 'copied' and runtime.sha256_file(tmp_path / rel) == v['sha256'] for rel, v in done.items())
    assert all(v['action'] == 'already in place' for v in host.materialize(ROOT, tmp_path, host.DRY_RUN_PINNED).values())
    fake_root = tmp_path / 'root'
    shutil.copytree(ROOT / 'docs/track-b/evidence/cp-17c', fake_root / 'docs/track-b/evidence/cp-17c')
    shutil.copytree(ROOT / host.DRY_RUN_PINNED, fake_root / host.DRY_RUN_PINNED)
    target = fake_root / host.committed_path(runtime.FREEZE_STATE, host.DRY_RUN_PINNED)
    target.write_bytes(target.read_bytes() + b' ')
    with pytest.raises(RuntimeError, match='not the pinned file'):
        host.materialize(fake_root, tmp_path / 'other', host.DRY_RUN_PINNED)


def test_pyodide_is_placed_only_after_each_hash_holds(tmp_path):
    files = host.pyodide_files(ROOT)
    assert len(files) == 23
    calls = []

    def fetch_wrong(url, target):
        calls.append(url)
        Path(target).write_bytes(b'not the file')
        return {'url': url, 'bytes': 12, 'sha256': hashlib.sha256(b'not the file').hexdigest(), 'seconds': 0.0}
    with pytest.raises(RuntimeError, match='nothing is placed'):
        host.pyodide(ROOT, tmp_path, retrieve=True, fetch=fetch_wrong)
    assert calls[0].startswith(host.PYODIDE_SOURCE) and not any((tmp_path / runtime.PYODIDE_DIR).glob('*.whl'))
    with pytest.raises(RuntimeError, match='absent'):
        host.pyodide(ROOT, tmp_path, retrieve=False)
    local = Path(runtime.project_root()) / runtime.PYODIDE_DIR
    if not all((local / name).is_file() for name in files):
        pytest.skip('the pinned Pyodide folder is absent on this machine')

    def fetch_local(url, target):
        data = (local / url.removeprefix(host.PYODIDE_SOURCE)).read_bytes()
        Path(target).write_bytes(data)
        return {'url': url, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'seconds': 0.0}
    placed = host.pyodide(ROOT, tmp_path, retrieve=True, fetch=fetch_local)
    assert len(placed) == 23 and all(v['action'] == 'retrieved' for v in placed.values())


def test_fake_values_are_recomputable_and_never_real_shapes_of_a_name():
    a, b = guarddemo.fake_environment('run-1'), guarddemo.fake_environment('run-2')
    assert set(a) == set(guarddemo.NAMES) and a != b and all(len(v) == 40 for v in a.values())
    assert guarddemo.fake_value('HF_TOKEN', 'run-1') == a['HF_TOKEN']


def test_the_guards_block_fake_credentials_on_the_pipelines_own_commits_and_pushes(tmp_path):
    """The repository's own `.githooks`: the secret guard by value, the leak scan by shape, the publication guard."""
    if not (ROOT / 'scripts/leak_scan.py').is_file():
        pytest.skip('the leak scan is not in this tree')
    result = guarddemo.demo(ROOT, tmp_path / 'demo', 'pytest-demo')
    by_case = {c['case']: c for c in result['cases']}
    assert result['all_as_expected'], json.dumps(result['cases'], indent=1)
    assert by_case['a staged file holding a fake ENTSOE_API_TOKEN']['output'][0].endswith('record.json (staged)')
    assert not any(c['value_in_output'] for c in result['cases'])
    found = guarddemo.scan('pytest-demo', [tmp_path / 'demo' / 'staged' / 'record.json'])
    assert found['found'] == {'ENTSOE_API_TOKEN': [str(tmp_path / 'demo' / 'staged' / 'record.json')]}
