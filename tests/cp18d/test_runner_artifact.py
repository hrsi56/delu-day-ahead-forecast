"""CP-18d item 4: the runner's Actions artifact holds the Space's whole build (`cp18.runner_artifact`), on a small fake
build whose record is written by the build script's own `listing` (no network, no Pyodide).

What is checked: the record lists every file of the build record, History's listing and the record itself, with the
fitted arrays the results step deletes; it refuses a missing or changed file before the deletion; after the deletion
(the workflow's own `find ... -delete`), `verify` accepts the downloaded results folder and refuses a dropped dotfile,
a changed file, an array left in place, a non-array excused as deleted, and a changed build record; other files of the
results folder are outside the check. The recorded files are the ones the publication reads (`cp18.publish.listed`).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

import pytest

from cp18 import publish
from cp18 import runner_artifact as RA

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location('build_product_space_cp18d', ROOT / 'scripts/build_product_space.py')
BPS = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(BPS)


def fake_build(results: Path) -> Path:
    """A results folder holding a Space build laid out as the build script lays it out, with its own records."""
    build = results / 'space'
    files = {
        'index.html': b'<html><head></head><body>v6</body></html>\n', 'README.md': b'card\n',
        '.gitattributes': BPS.GITATTRIBUTES.encode(), 'app/main.js': b'main();\n', 'app/claims.json': b'{}\n',
        'app/worker.js': b'worker\n', 'pyodide/pyodide.asm.wasm': b'\0asm' * 64, 'bundle/src.zip': b'PK zip',
        'payloads/manifest.json': b'{"artifact": {}}\n', 'payloads/artifact-arrays.npz': b'NUMPY arrays',
        'payloads/artifact.json': b'{}\n', 'history/index.html': b'<html>v1</html>\n',
        'history/.gitattributes': b'*.png filter=lfs\n', 'history/assets/a.png': b'\x89PNG',
    }
    for rel, data in files.items():
        (build / rel).parent.mkdir(parents=True, exist_ok=True)
        (build / rel).write_bytes(data)
    (build / 'app/history-files.json').write_text(BPS.dump({'schema': 'cp18b-space-history-files-v1',
                                                            'files': BPS.listing(build, history=True)}))
    (build / 'app/space-build.json').write_text(BPS.dump({'schema': BPS.SCHEMA, 'files': BPS.listing(build)}))
    (results / 'run').mkdir()
    (results / 'run/run.json').write_text('{}\n')
    (results / 'bundle').mkdir()
    (results / 'bundle/artifact-arrays.npz').write_bytes(b'NUMPY arrays')
    return build


def results_step(results: Path) -> None:
    """The workflow's results step: the fitted arrays deleted, then the results' own hashes."""
    subprocess.run(['find', str(results), '-type', 'f', '-name', '*-arrays.npz', '-delete'], check=True)


def recorded(results: Path) -> dict:
    out = results / RA.RECORD_NAME
    assert RA.main(['record', '--build', str(results / 'space'), '--out', str(out)]) == 0
    return json.loads(out.read_text())


@pytest.fixture()
def results(tmp_path) -> Path:
    folder = tmp_path / 'results'
    fake_build(folder)
    return folder


def test_the_record_lists_the_whole_build_and_the_arrays_to_be_deleted(results):
    value = recorded(results)
    assert value['schema'] == RA.SCHEMA and value['ok'] and value['build_folder'] == 'space'
    paths = {f['path'] for f in value['files']}
    assert {'.gitattributes', 'history/.gitattributes', 'app/space-build.json', 'app/history-files.json',
            'history/assets/a.png', 'payloads/artifact-arrays.npz'} <= paths
    assert paths == set(publish.listed(results / 'space')) | {'app/space-build.json'}
    assert all(f['present'] and f['matches'] for f in value['files'])
    assert value['deleted_arrays'] == [{'path': 'payloads/artifact-arrays.npz', 'recorded': True, 'bytes': 12,
                                        'sha256': hashlib.sha256(b'NUMPY arrays').hexdigest()}]
    build_record = (results / 'space/app/space-build.json').read_bytes()
    assert value['build_record']['sha256'] == hashlib.sha256(build_record).hexdigest()
    assert value['unrecorded'] == []
    # deterministic: the same build gives the same record
    first = (results / RA.RECORD_NAME).read_bytes()
    recorded(results)
    assert (results / RA.RECORD_NAME).read_bytes() == first


@pytest.mark.parametrize('change', ['missing', 'differs', 'history'])
def test_the_record_refuses_a_missing_or_changed_file_before_the_deletion(results, change):
    build = results / 'space'
    if change == 'missing':
        (build / '.gitattributes').unlink()
    elif change == 'differs':
        (build / 'app/main.js').write_bytes(b'changed();\n')
    else:
        (build / 'history/assets/a.png').unlink()
    out = results / RA.RECORD_NAME
    assert RA.main(['record', '--build', str(build), '--out', str(out)]) == 1
    value = json.loads(out.read_text())
    assert not value['ok'] and len(value['problems']) == 1


def test_verify_accepts_the_downloaded_results_after_the_deletion(results, tmp_path):
    recorded(results)
    results_step(results)
    assert not (results / 'space/payloads/artifact-arrays.npz').exists()
    # the download: another folder, the same files (an extra file of the results is outside the check)
    download = tmp_path / 'download'
    shutil.copytree(results, download)
    (download / 'results-sha256.txt').write_text('hashes\n')
    report_file = tmp_path / 'report.json'
    assert RA.main(['verify', '--artifact', str(download), '--out', str(report_file)]) == 0
    report = json.loads(report_file.read_text())
    assert report['ok'] and report['problems'] == [] and report['deleted_absent'] == ['payloads/artifact-arrays.npz']
    assert report['files_verified'] == report['files_recorded'] - 1
    # an unrecorded file in the build is reported, not judged
    (download / 'space/notes.txt').write_text('x\n')
    report = RA.verify(download)
    assert report['ok'] and report['outside_the_check'] == ['notes.txt']


def _broken(results: Path, how: str) -> dict:
    recorded(results)
    results_step(results)
    build = results / 'space'
    record_file = results / RA.RECORD_NAME
    if how == 'dotfile dropped':                     # PRES-6's landing: the upload without hidden files
        (build / '.gitattributes').unlink()
        (build / 'history/.gitattributes').unlink()
    elif how == 'file changed':
        (build / 'payloads/manifest.json').write_bytes(b'{"artifact": {"other": 1}}\n')
    elif how == 'arrays left':
        (build / 'payloads/artifact-arrays.npz').write_bytes(b'NUMPY arrays')
    elif how == 'non-array excused':
        value = json.loads(record_file.read_text())
        value['deleted_arrays'].append({'path': 'app/main.js', 'sha256': '0' * 64, 'bytes': 1, 'recorded': True})
        record_file.write_text(json.dumps(value))
        (build / 'app/main.js').unlink()
    elif how == 'build record changed':
        record = json.loads((build / 'app/space-build.json').read_text())
        record['files'] = [f for f in record['files'] if f['path'] != 'app/main.js']
        (build / 'app/space-build.json').write_text(json.dumps(record))
    elif how == 'pyodide dropped':                   # the old results step's deletion of the large copies
        shutil.rmtree(build / 'pyodide')
    return RA.verify(results)


@pytest.mark.parametrize('how', ['dotfile dropped', 'file changed', 'arrays left', 'non-array excused',
                                 'build record changed', 'pyodide dropped'])
def test_verify_refuses_an_incomplete_or_changed_artifact(results, how):
    report = _broken(results, how)
    assert not report['ok'] and report['problems'], report


def test_verify_refuses_a_missing_or_foreign_record(tmp_path):
    assert not RA.verify(tmp_path)['ok']
    (tmp_path / RA.RECORD_NAME).write_text(json.dumps({'schema': 'other'}))
    assert not RA.verify(tmp_path)['ok']
