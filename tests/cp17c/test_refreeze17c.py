"""CP-17c's freeze manifest and its verifier (`cp17.tools.refreeze17c`, through `refreeze verify`), CI-safe.

The controls run on a copy of exactly the files `verify` reads, in a temporary root:
- **governance changes leave it green:** a changed live anchor (a later revision), changed live decisions records,
  and a new decisions record;
- **every other change fails it:** a computational input, a code file of each group (package, runner, the three
  pipeline modules), a schema, a frozen governance copy (CP-17c's or CP-17b's), CP-17b's superseded evidence, the
  freeze-origin artifact, the manifest itself;
- **local files:** absent on CI, they are reported unchecked, never passed; present (the issuing machine), each is
  required and checked by hash, the CPython patch version with them.

CP-17b's verifier on this tree reports exactly what CP-17c re-froze (`CP17B_EXPECTED`), and CP-17's still reports
its two files, so both superseded checks stay meaningful.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import zlib

import pytest

from cp17 import hostcheck, runtime
from cp17.tools import freeze, ledger, refreeze, refreeze17c

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / refreeze17c.EVIDENCE / 'freeze-manifest.json'


@pytest.fixture(scope='module')
def manifest():
    return json.loads(MANIFEST.read_text())


def _read_by_verify(m: dict) -> list[str]:
    identity = m['policy_identity']
    paths = [g['copy'] for g in identity['governance'].values()]
    paths += list(identity['computational_sha256']) + list(identity['schemas_sha256'])
    paths += [r['path'] for r in identity['supersedes']['records'].values()]
    paths += [m['freeze_origin']['artifact_path'], refreeze.PROTOCOL]
    return paths


@pytest.fixture()
def tree(tmp_path, manifest):
    root = tmp_path / 'root'
    for rel in _read_by_verify(manifest):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, root / rel)
    shutil.copytree(ROOT / 'src', root / 'src', ignore=shutil.ignore_patterns('__pycache__'))
    return root


def _verify(m, root, **kw):
    return refreeze17c.verify(m, root, project=root.parent / 'no-local-files', **kw)


def _append(path: Path, text: str = '\n# changed\n') -> None:
    path.write_bytes(path.read_bytes() + text.encode())


def _local_unchecked(result: dict) -> list[str]:
    return [p for p in result['unchecked'] if p.endswith(': absent')]


def test_the_manifest_holds_its_own_digests(manifest):
    assert manifest['schema'] == 'cp17c-freeze-manifest-v1'
    assert manifest['policy_identity_sha256'] == freeze.digest(manifest['policy_identity'])
    assert manifest['content_sha256'] == freeze.digest({k: v for k, v in manifest.items() if k != 'content_sha256'})
    assert manifest['verification'] == refreeze17c.COVERAGE


def test_the_copy_verifies_with_its_local_files_unchecked(manifest, tree):
    result = _verify(manifest, tree)
    assert result['problems'] == []
    absent = _local_unchecked(result)
    # 23 Pyodide files, bin/node, k13.json, the freeze-origin states and the canary's two payload files
    assert len(absent) == 23 + 1 + 1 + 1 + 2
    other = [p for p in result['unchecked'] if p not in absent]
    assert all(p.startswith(('the package zip: zlib', 'CPython ')) for p in other)
    assert (platform.python_version() != runtime.CPYTHON) == any(p.startswith('CPython ') for p in other)
    assert (zlib.ZLIB_RUNTIME_VERSION != runtime.ZLIB_RUNTIME) == any(p.startswith('the package zip') for p in other)
    required = _verify(manifest, tree, require_local=True)['problems']
    assert len([p for p in required if p.endswith(': absent')]) == len(absent)    # required, they are absences


def test_the_committed_manifest_verifies_here(manifest):
    result = refreeze17c.verify(manifest, ROOT)
    assert result['problems'] == []
    assert all(p.endswith(': absent') or p.startswith(('the package zip: zlib', 'CPython ')) for p in result['unchecked'])


def test_refreeze_verify_dispatches_and_prints_verified_only_when_nothing_is_unchecked(manifest, tree):
    shutil.copyfile(MANIFEST, tree / refreeze17c.EVIDENCE / 'freeze-manifest.json')
    env = {'PATH': '/usr/bin:/bin', 'PYTHONPATH': str(tree / 'src'), 'CP17_PROJECT_ROOT': str(tree.parent / 'none')}
    done = subprocess.run([sys.executable, '-m', 'cp17.tools.refreeze', 'verify',
                           str(tree / refreeze17c.EVIDENCE / 'freeze-manifest.json'), '--root', str(tree)],
                          capture_output=True, text=True, env=env, cwd=tree)
    assert done.returncode == 0
    assert done.stdout.startswith('verified, except ')                   # local files absent here: not "verified"
    assert hostcheck.pins.__doc__ and 'verified' in hostcheck.pins.__doc__


def test_an_amendment_leaves_it_green(manifest, tree):
    (tree / 'capstone_v21.md').write_text((ROOT / 'capstone_v21.md').read_text() + '\n## r20 (a simulated amendment)\n')
    for rel in ('docs/track-b/owner-decisions-2026-10-30.md', 'docs/track-b/owner-decisions-2026-10-29.md',
                'docs/track-b/cp-17-owner-decisions-2026-10-28.md', 'docs/track-b/pre-cp-17-rulings-2026-10-25.md'):
        (tree / rel).parent.mkdir(parents=True, exist_ok=True)
        (tree / rel).write_text((ROOT / rel).read_text() + '\namended\n')
    (tree / 'docs/track-b/owner-decisions-new.md').write_text('26. a new decision\n')
    assert _verify(manifest, tree)['problems'] == []


@pytest.mark.parametrize('rel', ['data/snapshot.parquet', 'reports/development-inputs/tier-register.json',
                                 'reports/weather-ablation/weather-features.parquet', 'uv.lock', 'pyproject.toml',
                                 'reports/cp17-probe/retrieval-manifest.json'])
def test_a_changed_computational_input_fails_it(manifest, tree, rel):
    _append(tree / rel, '\n')
    assert f'{rel}: missing or altered' in _verify(manifest, tree, rebuild=False)['problems']


@pytest.mark.parametrize('rel', ['src/cp17/dailyfit.py', 'src/cp17/schema.py', 'src/cp24/member.py',
                                 'src/cp17/host/node_run.mjs', 'src/cp17/daily.py', 'src/cp17/runtime.py',
                                 'src/cp17/hostcheck.py'])
def test_a_changed_code_file_fails_it(manifest, tree, rel):
    _append(tree / rel, '\n// changed\n' if rel.endswith('.mjs') else '\n# changed\n')
    assert f'{rel}: missing or altered' in _verify(manifest, tree, rebuild=False)['problems']


def test_a_changed_package_fails_its_rebuild(manifest, tree):
    _append(tree / 'src/cp17/issue.py')
    problems = _verify(manifest, tree)['problems']
    assert "the rebuilt package's files differ from the recorded ones" in problems
    assert "the rebuilt package's identity differs from the recorded one" in problems


@pytest.mark.parametrize('name', ['anchor_v21_r19', 'decisions_22_25', 'anchor_v21_r17', 'decisions_13_19'])
def test_a_changed_governance_copy_fails_it(manifest, tree, name):
    rel = manifest['policy_identity']['governance'][name]['copy']
    _append(tree / rel)
    assert f'{rel}: the frozen governance copy is missing or altered' in _verify(manifest, tree, rebuild=False)['problems']


def test_a_changed_pin_set_fails_it(manifest, tree):
    fewer = copy.deepcopy(manifest)
    fewer['policy_identity']['governance'].pop('cp17c_brief_5f34f3ab')
    assert 'the governance pins are not the frozen set' in _verify(fewer, tree, rebuild=False)['problems']


@pytest.mark.parametrize('key', ['freeze_record', 'freeze_manifest', 'artifact', 'landing_record'])
def test_cp17bs_superseded_evidence_must_stay_as_committed(manifest, tree, key):
    rel = refreeze17c.CP17B[key][0]
    _append(tree / rel, ' ')
    assert f'{rel}: missing or altered' in _verify(manifest, tree, rebuild=False)['problems']


def test_the_freeze_origin_artifact_and_the_canary(manifest, tree):
    _append(tree / manifest['freeze_origin']['artifact_path'], ' ')
    assert any('freeze-origin artifact is missing or altered' in p for p in _verify(manifest, tree, rebuild=False)['problems'])
    wrong = copy.deepcopy(manifest)
    wrong['freeze_origin']['canary_quantiles_sha256'] = '0' * 64
    wrong['content_sha256'] = freeze.digest({k: v for k, v in wrong.items() if k != 'content_sha256'})
    shutil.copyfile(ROOT / manifest['freeze_origin']['artifact_path'], tree / manifest['freeze_origin']['artifact_path'])
    assert 'the freeze-origin artifact does not verify against the manifest' in _verify(wrong, tree, rebuild=False)['problems']


def test_a_changed_runtime_or_state_file_fails_it_where_local_files_are_present(manifest, tree, tmp_path):
    project = tmp_path / 'project'
    identity = manifest['policy_identity']
    for rel in refreeze17c._local(project, identity):
        (project / rel).parent.mkdir(parents=True, exist_ok=True)
        (project / rel).write_bytes(b'not the pinned file')
    problems = refreeze17c.verify(manifest, tree, project=project, rebuild=False)['problems']
    assert sum(p.endswith(': altered') for p in problems) == 28
    assert f'{runtime.K13}: its content digest is not the recorded search state' in problems
    assert refreeze17c.issuing_machine(project)


@pytest.mark.skipif(not refreeze17c.issuing_machine(ledger.project_root(ROOT))
                    or not all((ledger.project_root(ROOT) / rel).exists() for rel in
                               refreeze17c._local(ledger.project_root(ROOT), json.loads(MANIFEST.read_text())['policy_identity'])),
                    reason="the issuing host's local files (Pyodide, bin/node, the states) are absent here")
@pytest.mark.skipif(platform.python_version() != runtime.CPYTHON, reason='not the pinned CPython')
def test_the_real_local_files_verify_and_one_altered_file_fails(manifest, tree, tmp_path):
    real = ledger.project_root(ROOT)
    assert refreeze17c.verify(manifest, tree, project=real, rebuild=False) == {'problems': [], 'unchecked': []}
    project = tmp_path / 'project'
    for rel in refreeze17c._local(real, manifest['policy_identity']):
        (project / rel).parent.mkdir(parents=True, exist_ok=True)
        (project / rel).symlink_to(real / rel)
    rel = runtime.FREEZE_STATE
    (project / rel).unlink()
    (project / rel).write_bytes((real / rel).read_bytes() + b' ')
    assert refreeze17c.verify(manifest, tree, project=project, rebuild=False)['problems'] == [f'{rel}: altered']


def test_the_identity_states_its_changes_and_carries_cp17bs_other_terms(manifest):
    identity = manifest['policy_identity']
    cp17b = json.loads((ROOT / refreeze17c.CP17B_MANIFEST).read_text())['policy_identity']
    carried = ('availability', 'definitions', 'designated_policy', 'designation', 'failure_policy', 'lock_price_policy',
               'product', 'refit_schedule', 'retrain', 'seeds', 'shadow', 'success_definition', 'uncertainty', 'windows',
               'schemas_sha256')
    assert all(identity[k] == cp17b[k] for k in carried)
    assert {k: v for k, v in identity['hyperparameters'].items() if k != 'A1_search'} == \
        {k: v for k, v in cp17b['hyperparameters'].items() if k != 'A1_search'}
    assert {k: v for k, v in identity['hyperparameters']['A1_search'].items() if k != 'file'} == \
        {k: v for k, v in cp17b['hyperparameters']['A1_search'].items() if k != 'file'}
    assert identity['hyperparameters']['A1_search']['file'] == runtime.K13
    assert identity['computational_sha256'] == cp17b['computational_sha256']
    assert identity['issuing_host']['pyodide']['files_sha256'] == cp17b['issuing_host']['pyodide']['files_sha256']
    assert identity['code']['runner_files_sha256'] == cp17b['code']['runner_files_sha256']
    changed = {k for k in identity['code']['files_sha256'] if identity['code']['files_sha256'][k] != cp17b['code']['files_sha256'].get(k)}
    assert changed == {'cp17/schema.py'} and set(identity['code']['files_sha256']) == set(cp17b['code']['files_sha256'])
    assert set(identity['code']['pipeline_files_sha256']) == {'cp17/daily.py', 'cp17/runtime.py', 'cp17/hostcheck.py'}
    assert identity['code']['zip_zlib_runtime'] == runtime.ZLIB_RUNTIME
    assert identity['supersedes']['policy_identity_sha256'] == refreeze17c.CP17B_POLICY_IDENTITY
    assert identity['changes_from_cp17b'] == refreeze17c.CHANGES and 'R7' in identity['defects_fixed']
    host = identity['issuing_host']
    assert (host['node']['sha256'], host['node']['tarball']['sha256'], host['node']['path']) == \
        (runtime.BINARY['sha256'], runtime.TARBALL['sha256'], runtime.NODE_RELATIVE)
    assert host['cpython'] == {**host['cpython'], 'version': '3.13.15', 'zlib_runtime': '1.2.12'}
    assert host['checks']['order'] == list(hostcheck.ORDER)
    assert host['checks']['canary']['quantiles_sha256'] == hostcheck.CANARY_QUANTILES_SHA256
    assert identity['registry'] == {**cp17b['registry'], 'state': identity['registry']['state']}


def test_the_freeze_origin_is_cp17bs_reissued(manifest):
    art = json.loads((ROOT / manifest['freeze_origin']['artifact_path']).read_text())
    old = json.loads((ROOT / refreeze17c.CP17B['artifact'][0]).read_text())
    same = ('quantiles', 'quantiles_sha256', 'keys', 'display', 'issued_policy', 'route', 'partial', 'times', 'delivery_day',
            'issue_utc', 'designated_policy', 'product', 'schema')
    assert all(art[k] == old[k] for k in same)
    assert {k: v for k, v in art['lineage'].items() if k not in ('code_sha256', 'policy_identity_sha256')} == \
        {k: v for k, v in old['lineage'].items() if k not in ('code_sha256', 'policy_identity_sha256')}
    assert art['lineage']['policy_identity_sha256'] == manifest['policy_identity_sha256']
    assert manifest['freeze_origin']['artifact_arrays_sha256'] == \
        json.loads((ROOT / refreeze17c.CP17B_MANIFEST).read_text())['freeze_origin']['artifact_arrays_sha256']
    assert art['quantiles_sha256'] == hostcheck.CANARY_QUANTILES_SHA256 == manifest['freeze_origin']['canary_quantiles_sha256']


def test_cp17bs_verifier_reports_exactly_what_cp17c_re_froze(manifest):
    problems = refreeze17c.cp17b_superseded(ROOT)
    expected = list(refreeze17c.CP17B_EXPECTED)
    if zlib.ZLIB_RUNTIME_VERSION != '1.2.12':
        expected.remove("the rebuilt package's zip differs from the recorded one")
    assert problems == expected


def test_the_pinned_copies_hold(manifest):
    for name, (source, copy_name, digest) in refreeze17c.GOVERNANCE.items():
        assert freeze.sha256_file(ROOT / refreeze17c.PINNED / copy_name) == digest
        assert manifest['policy_identity']['governance'][name]['copy'] == f'{refreeze17c.PINNED}/{copy_name}'
