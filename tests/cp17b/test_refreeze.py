"""Item 4 and N4: the re-frozen manifest's verifier (`cp17.tools.refreeze.verify`), CI-safe.

The positive and negative controls run on a copy of exactly the files `verify` reads, in a temporary root:
- **governance changes leave it green:** a changed live anchor (as r18 will make), a changed live decisions record,
  and a new decisions record;
- **every other change fails it:** a computational input, a code file of each group (package, runner, driver), a
  schema, a runtime file, a frozen governance copy, CP-17's superseded evidence, the freeze-origin artifact, the
  manifest itself.

Local runtimes are absent on CI, so `verify` reports them unchecked there; a project root holding altered runtime
files shows that a changed runtime file fails it wherever runtimes are present.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil

import pytest

from cp17.tools import freeze, ledger, refreeze

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / refreeze.EVIDENCE / 'freeze-manifest.json'


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
    """A root with the files `verify` reads, `src/` whole (the package is rebuilt from it), and nothing else."""
    root = tmp_path / 'root'
    for rel in _read_by_verify(manifest):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, root / rel)
    shutil.copytree(ROOT / 'src', root / 'src', ignore=shutil.ignore_patterns('__pycache__'))
    return root


def _verify(m, root, **kw):
    return refreeze.verify(m, root, project=root.parent / 'no-local-runtimes', **kw)


def _append(path: Path, text: str = '\n# changed\n') -> None:
    path.write_bytes(path.read_bytes() + text.encode())


def test_the_committed_manifest_verifies_here(manifest):
    result = refreeze.verify(manifest, ROOT)
    assert result['problems'] == []
    # CI: no local runtime here, so they are reported, never passed; and the zip where zlib is not the freeze's
    assert all(p.endswith(': absent') or p.startswith('the package zip: zlib') for p in result['unchecked'])


def test_the_copy_verifies_with_its_local_runtimes_unchecked(manifest, tree):
    result = _verify(manifest, tree)
    names = set(manifest['policy_identity']['issuing_host']['pyodide']['files_sha256'])
    assert result['problems'] == []
    absent = [p for p in result['unchecked'] if p.endswith(': absent')]
    assert {Path(p.removesuffix(': absent')).name for p in absent} >= names | {'k13.json'}
    assert len(absent) in (24, 25)                       # Node.js too, where it is not installed
    assert len(result['unchecked']) - len(absent) in (0, 1)   # the zip, where zlib is not the freeze's
    assert _verify(manifest, tree, require_local=True)['problems']               # required, they are absences


def test_a_changed_live_anchor_or_a_new_decisions_record_leaves_it_green(manifest, tree):
    (tree / 'capstone_v21.md').write_text('# capstone v21, revision r18 (an amendment)\n')
    decisions = tree / 'docs/track-b'
    (decisions / 'cp-17-owner-decisions-2026-10-28.md').write_text('amended\n')
    (decisions / 'pre-cp-17-rulings-2026-10-25.md').write_text('amended\n')
    (decisions / 'cp-17b-owner-decisions-new.md').write_text('20. a new decision\n')
    assert _verify(manifest, tree)['problems'] == []


@pytest.mark.parametrize('rel', ['data/snapshot.parquet', 'reports/development-inputs/tier-register.json',
                                 'reports/development-inputs/margin-table.csv', 'reports/weather-ablation/weather-features.parquet',
                                 'reports/development-inputs/manifest.json',
                                 'reports/rebaseline/cold-rerun-2026-10-15/scores-manifest.json', 'uv.lock', 'pyproject.toml'])
def test_a_changed_computational_input_fails_it(manifest, tree, rel):
    _append(tree / rel, '\n')
    assert f'{rel}: missing or altered' in _verify(manifest, tree, rebuild=False)['problems']


@pytest.mark.parametrize('rel', ['src/cp17/dailyfit.py', 'src/cp17/shadow.py', 'src/cp24/member.py',
                                 'src/cp17/host/node_run.mjs', 'src/cp17/daily.py'])
def test_a_changed_code_file_fails_it(manifest, tree, rel):
    _append(tree / rel, '\n// changed\n' if rel.endswith('.mjs') else '\n# changed\n')
    assert f'{rel}: missing or altered' in _verify(manifest, tree, rebuild=False)['problems']


def test_a_changed_package_fails_its_rebuild(manifest, tree):
    _append(tree / 'src/cp17/issue.py')
    problems = _verify(manifest, tree)['problems']
    assert 'src/cp17/issue.py: missing or altered' in problems
    assert "the rebuilt package's files differ from the recorded ones" in problems
    assert "the rebuilt package's identity differs from the recorded one" in problems


def test_a_changed_runtime_file_fails_it(manifest, tree, tmp_path):
    project = tmp_path / 'project'
    runtime = project / freeze.RUNTIME_DIR
    runtime.mkdir(parents=True)
    for name in manifest['policy_identity']['issuing_host']['pyodide']['files_sha256']:
        (runtime / name).write_bytes(b'not the pinned runtime')
    problems = refreeze.verify(manifest, tree, project=project, rebuild=False)['problems']
    assert sum(p.endswith(': altered') and freeze.RUNTIME_DIR in p for p in problems) == 23
    assert any('k13.json: absent' in p for p in problems)        # present runtimes make every local file required


@pytest.mark.skipif(not (ledger.project_root(ROOT) / freeze.RUNTIME_DIR).exists()
                    or not ledger.available(ROOT), reason='the pinned Pyodide runtime or the evidence/cp-26 extract is absent')
def test_the_real_runtimes_verify_and_one_altered_file_fails(manifest, tree, tmp_path):
    real = ledger.project_root(ROOT)
    assert refreeze.verify(manifest, tree, project=real, rebuild=False)['problems'] == []
    project = tmp_path / 'project'
    shutil.copytree(real / freeze.RUNTIME_DIR, project / freeze.RUNTIME_DIR)
    (project / '.local' / 'artifacts').mkdir(parents=True)
    (project / '.local' / 'artifacts' / 'cp-17').symlink_to(real / '.local' / 'artifacts' / 'cp-17')
    assert refreeze.verify(manifest, tree, project=project, rebuild=False)['problems'] == []
    _append(project / freeze.RUNTIME_DIR / 'pyodide.mjs', '\n// changed\n')
    assert refreeze.verify(manifest, tree, project=project, rebuild=False)['problems'] == [
        f"{project / freeze.RUNTIME_DIR / 'pyodide.mjs'}: altered"]


def test_a_changed_governance_copy_or_a_changed_pin_set_fails_it(manifest, tree):
    copy_rel = manifest['policy_identity']['governance']['anchor_v21_r17']['copy']
    _append(tree / copy_rel)
    assert f'{copy_rel}: the frozen governance copy is missing or altered' in _verify(manifest, tree, rebuild=False)['problems']
    fewer = copy.deepcopy(manifest)
    fewer['policy_identity']['governance'].pop('decisions_13_19')
    assert 'the governance pins are not the frozen set' in _verify(fewer, tree, rebuild=False)['problems']


def test_cp17s_superseded_evidence_must_stay_as_committed(manifest, tree):
    rel = 'docs/track-b/evidence/cp-17/freeze-record.md'
    _append(tree / rel)
    assert f'{rel}: missing or altered' in _verify(manifest, tree, rebuild=False)['problems']


def test_a_schema_file_must_be_the_packages(manifest, tree):
    rel = f'{refreeze.SCHEMAS_DIR}/fitted_artifact.schema.json'
    value = json.loads((tree / rel).read_text())
    value['required'].remove('resources')
    (tree / rel).write_text(json.dumps(value))
    problems = _verify(manifest, tree, rebuild=False)['problems']
    assert f'{rel}: missing or altered' in problems and f"{rel}: does not hold the package's schema" in problems


def test_the_freeze_origin_artifact_and_the_manifests_own_digests(manifest, tree):
    art = tree / manifest['freeze_origin']['artifact_path']
    _append(art, ' ')
    assert any('freeze-origin artifact is missing or altered' in p for p in _verify(manifest, tree, rebuild=False)['problems'])
    wrong = copy.deepcopy(manifest)
    wrong['policy_identity']['registry']['version'] = 2
    problems = _verify(wrong, tree, rebuild=False)['problems']
    assert 'wrong or missing registry name or version' in problems and any('digest' in p for p in problems)
    other = copy.deepcopy(manifest)
    other['freeze_origin']['artifact_sha256'] = 'f' * 64
    assert "the manifest's own content digest does not hold" in _verify(other, tree, rebuild=False)['problems']


def test_the_manifest_states_how_each_hash_is_checked(manifest):
    assert manifest['verification'] == refreeze.COVERAGE
    identity = manifest['policy_identity']
    assert set(identity['governance']) == set(refreeze.GOVERNANCE)
    assert {g['sha256'] for g in identity['governance'].values()} == {v[2] for v in refreeze.GOVERNANCE.values()}
    assert identity['supersedes']['policy_identity_sha256'] == refreeze.CP17_POLICY_IDENTITY


# ------------------------------------------------------------------ r18, simulated, against both verifiers
@pytest.fixture()
def amended(tree):
    """The tree with r18 simulated: the anchor amended, two decisions records edited, a new one added; and CP-17's
    superseded manifest and its freeze-origin artifact, which CP-17's own check reads."""
    shutil.copyfile(ROOT / 'docs/track-b/evidence/cp-17/artifact-2026-09-06.json',
                    tree / 'docs/track-b/evidence/cp-17/artifact-2026-09-06.json')
    (tree / 'capstone_v21.md').write_text((ROOT / 'capstone_v21.md').read_text() + '\n## r18 (a simulated amendment)\n')
    for rel in ('docs/track-b/pre-cp-17-rulings-2026-10-25.md', 'docs/track-b/cp-17-owner-decisions-2026-10-28.md',
                'docs/track-b/cp-25-rulings-2026-10-12.md'):
        (tree / rel).parent.mkdir(parents=True, exist_ok=True)
        (tree / rel).write_text((ROOT / rel).read_text() + '\namended\n')
    (tree / 'docs/track-b/cp-17b-owner-decisions-new.md').write_text('20. a new decision\n')
    return tree


def _cp17_check(root: Path, tmp: Path) -> list[str]:
    cp17 = json.loads((root / refreeze.CP17['freeze_manifest'][0]).read_text())
    return sorted(freeze.verify(cp17, refreeze.cp17_view(root, tmp)))


REFROZEN = ['src/cp17/issue.py: missing or altered', 'src/cp17/schema.py: missing or altered']


def test_cp17s_governance_pins_all_have_frozen_copies():
    sources = {source for source, _, _ in refreeze.GOVERNANCE.values()}
    assert refreeze.cp17_governance_live(ROOT) and set(refreeze.cp17_governance_live(ROOT)) <= sources


def test_an_amendment_leaves_both_verifiers_green(manifest, amended, tmp_path):
    """The first Integration review's acceptance case: r18 changes the anchor and adds a decisions record."""
    assert _verify(manifest, amended)['problems'] == []
    assert _cp17_check(amended, tmp_path / 'view') == REFROZEN        # tests/cp17's superseded check holds


@pytest.mark.parametrize('rel', ['reports/development-inputs/tier-register.json', 'data/snapshot.parquet',
                                 'src/cp17/dailyfit.py', 'src/cp17/retrain.py', 'src/cp24/member.py'])
def test_a_real_change_still_fails_both_verifiers(manifest, amended, tmp_path, rel):
    _append(amended / rel, '\n# changed\n' if rel.endswith('.py') else '\n')
    assert f'{rel}: missing or altered' in _verify(manifest, amended, rebuild=False)['problems']
    assert any(p in (f'{rel}: altered', f'{rel}: missing or altered') for p in _cp17_check(amended, tmp_path / 'view'))
