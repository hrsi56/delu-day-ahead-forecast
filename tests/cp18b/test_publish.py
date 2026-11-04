"""The publication step (`cp18.publish`), exercised against a local static server only.

A verified bundle and its Space build are uploaded to a local target, read back over HTTP as a visitor reads them,
and the served identity must equal the intended daily artifact. A refused bundle is never uploaded; a served file that
differs fails the publication; the Hugging Face target refuses without the activation's authority.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil

import pytest

from cp18 import controls as C, publish as PB
from cp18.bundle import read
from cp18b.support18b import BUNDLE, ROOT


def space_build(folder: Path, bundle_files: dict[str, bytes]) -> Path:
    """A minimal Space build in the layout `scripts/build_product_space.py` writes: the page, its build record, and the
    bundle at `payloads/`."""
    (folder / 'app').mkdir(parents=True)
    (folder / 'payloads').mkdir()
    (folder / 'index.html').write_text('<!doctype html><title>x</title>\n')
    (folder / 'app' / 'app.js').write_text('// app\n')
    for name, data in bundle_files.items():
        (folder / 'payloads' / name).write_bytes(data)
    files = {str(p.relative_to(folder)): {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'bytes': p.stat().st_size}
             for p in sorted(folder.rglob('*')) if p.is_file() and not str(p.relative_to(folder)).startswith('payloads/')}
    (folder / 'app' / 'space-build.json').write_text(json.dumps({'files': files}))
    return folder


def run(build: Path, bundle: Path, target: Path, corrupt=None):
    class Target(PB.LocalTarget):
        def upload(self, b):
            out = super().upload(b)
            if corrupt:
                corrupt(self.folder)
            return out
    t = Target(target)
    target.mkdir(parents=True, exist_ok=True)
    with PB.local_server(target) as base:
        return PB.publish(build, bundle, t, PB.http_fetch(base), ROOT)


def test_a_verified_bundle_is_published_and_its_served_identity_checked(tmp_path):
    build = space_build(tmp_path / 'build', read(BUNDLE))
    value = run(build, BUNDLE, tmp_path / 'served')
    assert value['published'] and value['served']['served_identity_equal'] and value['gate']['publishable']
    manifest = json.loads((BUNDLE / 'manifest.json').read_text())
    assert value['served']['artifact_sha256'] == manifest['artifact']['artifact_sha256']
    assert value['served']['served_manifest_sha256'] == hashlib.sha256((BUNDLE / 'manifest.json').read_bytes()).hexdigest()
    listed = json.loads((build / 'app' / 'space-build.json').read_text())['files']
    assert value['served']['checked'] == 1 + len(manifest['files']) + len(listed)


def test_a_refused_bundle_is_never_uploaded(tmp_path):
    bad = tmp_path / 'bad'
    C.write(C.mismatch(read(BUNDLE)), bad)
    build = space_build(tmp_path / 'build', read(bad))
    target = tmp_path / 'served'
    value = run(build, bad, target)
    assert not value['published'] and value['stopped'].startswith('the gate refused')
    assert not any(target.rglob('*'))


def test_a_build_that_does_not_carry_the_bundle_is_never_uploaded(tmp_path):
    files = read(BUNDLE)
    build = space_build(tmp_path / 'build', {k: v for k, v in files.items() if k != 'series.json'})
    value = run(build, BUNDLE, tmp_path / 'served')
    assert not value['published'] and 'does not carry exactly this bundle' in value['stopped']


def test_a_served_difference_fails_the_publication(tmp_path):
    build = space_build(tmp_path / 'build', read(BUNDLE))

    def corrupt(folder):
        path = folder / 'payloads' / 'outcomes.json'
        path.write_bytes(path.read_bytes()[:-2] + b' \n')
    value = run(build, BUNDLE, tmp_path / 'served', corrupt=corrupt)
    assert not value['published'] and 'payloads/outcomes.json: not served as the manifest lists it' in value['served']['problems']


def test_the_hub_target_refuses_without_the_activations_authority():
    with pytest.raises(PB.PublicationRefused, match="activation"):
        PB.HubTarget('owner/space')


def test_the_served_identity_is_read_from_a_loopback_host_only():
    with pytest.raises(PB.PublicationRefused):
        PB.http_fetch('https://example.org/')
    assert PB.http_fetch('http://127.0.0.1:9/')
