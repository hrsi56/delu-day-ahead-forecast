"""CP-24's base-tree record and its checkers (§23.13 item 16; §23.14).

That CP-24 changed no file existing at its base `522d7ea` is a property of the candidate commit. It is proved by
`python -m cp24.basetree --check-rev <candidate>` (and `--check` in a checkout of it), which the Lead runs before
the review and the Integration Critic reruns on the final candidate. This default-suite test does not hash the
files the record names: after the LAND, authorized work on `main` changes many of them (`progress.md`, the
anchors, `AGENTS.md`, `README.md`, `docs/index.html`), and a test binding them would make CI red there for good.
It checks the committed record and both checkers, each negative paired with a positive."""
import json
from pathlib import Path
import subprocess

from cp24.basetree import BASE, CP24_PATHS, PATH, build, check, check_rev

ROOT = Path(__file__).resolve().parents[2]
GIT = ['git', '-c', 'user.name=cp24', '-c', 'user.email=cp24@localhost', '-c', 'commit.gpgsign=false',
       '-c', 'core.hooksPath=/dev/null']


def test_the_record_is_the_base_tree():
    record = json.loads(PATH.read_text())
    assert record['schema'] == 'cp24-base-tree-v1' and record['base_commit'] == BASE == '522d7ea722b5d215d827d7aed9c56b7a9dec066e'
    assert record['files'] == len(record['sha256']) == 1322
    for name in ('scripts/mlflow_export.py', 'pyproject.toml', 'uv.lock', 'README.md', 'docs/index.html', 'progress.md',
                 'capstone_v21.md', 'AGENTS.md', 'reports/presentation/mlflow-export/manifest.json', 'src/cp23/ddnn.py',
                 'tests/cp23/torch-reference/uv.lock'):
        assert name in record['sha256'], name
    assert not any(name.startswith(CP24_PATHS) for name in record['sha256'])
    assert all(len(d) == 64 and int(d, 16) >= 0 for d in record['sha256'].values())


def test_the_file_checker_passes_an_unchanged_tree_and_catches_a_change(tmp_path):
    (tmp_path / 'docs').mkdir()
    (tmp_path / 'README.md').write_bytes(b'readme\n')
    (tmp_path / 'docs/index.html').write_bytes(b'<p>page</p>\n')
    import hashlib
    record = {'sha256': {n: hashlib.sha256((tmp_path / n).read_bytes()).hexdigest() for n in ('README.md', 'docs/index.html')}}
    assert check(record, tmp_path) == []
    (tmp_path / 'README.md').write_bytes(b'readme, edited\n')
    (tmp_path / 'docs/index.html').unlink()
    assert check(record, tmp_path) == ['changed: README.md', 'missing: docs/index.html']


def test_the_commit_checker_accepts_only_additions_under_cp24_paths(tmp_path):
    def git(*args):
        return subprocess.run([*GIT, *args], cwd=tmp_path, check=True, capture_output=True, text=True).stdout.strip()

    git('init', '-q')
    (tmp_path / 'progress.md').write_text('state\n')
    (tmp_path / 'src').mkdir()
    (tmp_path / 'src/model.py').write_text('x = 1\n')
    git('add', '-A')
    git('commit', '-q', '-m', 'base')
    base = git('rev-parse', 'HEAD')
    record = build(base, tmp_path)
    assert record['files'] == 2 and check_rev(record, base, tmp_path) == []
    # the positive: a candidate that only adds under CP-24's paths passes
    (tmp_path / 'src/cp24').mkdir()
    (tmp_path / 'src/cp24/new.py').write_text('y = 2\n')
    (tmp_path / 'reports/ddnn2').mkdir(parents=True)
    (tmp_path / 'reports/ddnn2/out.json').write_text('{}\n')
    git('add', '-A')
    git('commit', '-q', '-m', 'candidate')
    assert check_rev(record, 'HEAD', tmp_path) == []
    # the negatives: a changed base file, a removed base file and an addition outside CP-24's paths
    (tmp_path / 'progress.md').write_text('state, edited\n')
    (tmp_path / 'src/model.py').unlink()
    (tmp_path / 'notes.md').write_text('outside\n')
    git('add', '-A')
    git('commit', '-q', '-m', 'bad candidate')
    assert sorted(check_rev(record, 'HEAD', tmp_path)) == ['changed: progress.md', 'missing: src/model.py',
                                                            'outside CP-24 paths: notes.md']
    # a CP-24 path that existed at the base is refused when the record is written
    try:
        build('HEAD', tmp_path)
    except ValueError as exc:
        assert 'a CP-24 path existed at the base' in str(exc)
    else:
        raise AssertionError('a base holding a CP-24 path must be refused')
