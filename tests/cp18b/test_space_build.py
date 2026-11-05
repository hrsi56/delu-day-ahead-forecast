"""CP-18b: the final-product Space's build (`scripts/build_product_space.py`), offline, with no browser.

- the build refuses a tampered bundle (and `--allow-refused` stamps such a build as refused);
- the served worker is byte-identical to the frozen runner (`src/cp17/browser/worker.js`, CP-17c's hash);
- no `http://` or `https://` URL to another origin appears in any served page, script, style or record of the
  product, except the explicit external report link and the History note;
- the limitations come only from the claims, and every `live_` text the page shows is in the claims;
- the page's sources carry no hand-typed date, hash or claim sentence;
- the size budget adds up, and the build is deterministic (the same inputs give the same bytes).

The inputs are local (the pinned Pyodide folder, the frozen package zip and a dated bundle under `.local/`); where they
are absent, as on CI, every test that builds is skipped with that reason (the source scan still runs). `CP18B_SPACE_BUNDLE` names another bundle folder.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import shutil
import sys

import pytest

from cp17 import runtime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
PROJECT = Path(runtime.project_root(ROOT))
BUNDLE = Path(os.environ.get('CP18B_SPACE_BUNDLE') or PROJECT / '.local/tmp/cp-18b/try1/bundle')
LOCAL = (PROJECT / runtime.PYODIDE_DIR / 'pyodide.asm.wasm', PROJECT / '.local/artifacts/cp-17c/bundle/src.zip',
         BUNDLE / 'manifest.json')
SOURCE = ROOT / 'space-product'
REPORT = 'https://hrsi56.github.io/delu-day-ahead-forecast/'

needs_local = pytest.mark.skipif(not all(p.exists() for p in LOCAL),
                                reason='the local Space inputs are absent (the pinned Pyodide folder, the frozen package '
                                       'zip or a dated bundle under .local/)')


def build(out: Path, **kw):
    import build_product_space as B
    return B.build(BUNDLE, out, **kw)


@pytest.fixture(scope='module')
def built(tmp_path_factory):
    folder = tmp_path_factory.mktemp('space')
    history = folder / 'v1'
    (history / 'assets').mkdir(parents=True)
    (history / 'index.html').write_text('<!doctype html><title>v1</title>\n')
    (history / 'assets/app.js').write_text('// v1\n')
    out = folder / 'dist'
    record = build(out, history=history, history_note='a local stand-in for v1\'s export, for this test')
    return out, record


@needs_local
def test_the_build_refuses_a_tampered_bundle(tmp_path, capsys):
    import build_product_space as B
    bundle = tmp_path / 'bundle'
    shutil.copytree(BUNDLE, bundle)
    target = bundle / 'issued-forecasts.json'
    data = bytearray(target.read_bytes())
    i = data.index(b'"quantiles":[[') + len(b'"quantiles":[[')
    data[i] = ord('2') if data[i] != ord('2') else ord('3')          # one served byte, after the manifest
    target.write_bytes(bytes(data))
    with pytest.raises(B.Refused):
        B.build(bundle, tmp_path / 'dist')
    assert B.main(['--bundle', str(bundle), '--out', str(tmp_path / 'dist')]) == 1
    assert 'REFUSED' in capsys.readouterr().out
    record = B.build(bundle, tmp_path / 'dist-refused', allow_refused=True)
    assert record['refused'] is True and record['gate']['publishable'] is False
    assert json.loads((tmp_path / 'dist-refused/app/space-build.json').read_text())['refused'] is True
    assert 'refused' in (tmp_path / 'dist-refused/README.md').read_text()


@needs_local
def test_the_served_worker_is_byte_identical_to_the_frozen_one(built):
    out, record = built
    frozen = (ROOT / 'src/cp17/browser/worker.js').read_bytes()
    assert (out / 'app/worker.js').read_bytes() == frozen
    manifest = json.loads((ROOT / 'docs/track-b/evidence/cp-17c/freeze-manifest.json').read_text())
    assert record['frozen_worker']['sha256'] == manifest['policy_identity']['code']['runner_files_sha256']['cp17/browser/worker.js']
    assert (out / 'app/glue/spaceglue.py').read_bytes() == (ROOT / 'src/cp18/spaceglue.py').read_bytes()
    assert record['zip']['sha256'] == manifest['policy_identity']['code']['zip_sha256']
    assert len(record['pyodide']['files']) == len(manifest['policy_identity']['issuing_host']['pyodide']['files_sha256'])


def served_product_files(out: Path):
    """The product's own served text: the page, its scripts, styles and records (not the pinned runtime, the frozen
    package, the bundle's data or v1's history)."""
    for path in sorted(out.rglob('*')):
        rel = path.relative_to(out).as_posix()
        if path.is_file() and not rel.startswith(('pyodide/', 'bundle/', 'payloads/', 'history/')) and path.suffix in (
                '.html', '.js', '.css', '.json', '.py', '.md'):
            yield rel, path.read_text(encoding='utf-8')


@needs_local
def test_no_url_to_another_origin_except_the_report_and_the_history_note(built):
    out, record = built
    note = record['history']['note'] or ''
    found = {}
    for rel, text in served_product_files(out):
        for url in re.findall(r'https?://[^\s"\'<>()\]]+', text):
            if url.startswith(REPORT) or url in note:
                continue
            found.setdefault(rel, []).append(url)
    assert not found, found


@needs_local
def test_the_limitations_come_only_from_the_claims(built):
    from cp18.live_claims import build_live_claims, text
    out, _ = built
    claims = json.loads((out / 'app/claims.json').read_text())
    days = sorted(d['delivery_day'] for d in json.loads((BUNDLE / 'issued-forecasts.json').read_text())['days'])
    live = build_live_claims(ROOT, rehearsal_days=(days[0], days[-1]))
    assert claims['limitations'] == [{'label': label, 'key': key, 'text': text(live, key)} for label, key in live['limitations']]
    main = (SOURCE / 'app/main.js').read_text()
    view = main[main.index('RENDER.limitations'):main.index('RENDER.history')]
    assert 'S.claims.limitations' in view
    sources = {p: p.read_text() for p in SOURCE.rglob('*') if p.is_file()}
    for item in claims['limitations']:
        for path, body in sources.items():
            assert item['text'][:48] not in body, f'{path} copies the limitation {item["key"]} by hand'


@needs_local
def test_every_live_text_the_page_shows_is_in_the_claims(built):
    out, _ = built
    claims = json.loads((out / 'app/claims.json').read_text())
    main = (SOURCE / 'app/main.js').read_text()
    used = set(re.findall(r"\bL\('([a-z0-9_]+)'\)", main))
    assert used and all(k.startswith('live_') for k in used)
    assert used <= set(claims['values']), used - set(claims['values'])
    assert set(re.findall(r"\bshared\('([a-z0-9_]+)'\)", main)) <= set(claims['shared'])
    # every live_ name anywhere in the page's sources is read through the claims, never spelled out as text
    for path in SOURCE.rglob('*'):
        if path.is_file():
            names = set(re.findall(r'\blive_[a-z0-9_]+', path.read_text())) - {'live_claims'}   # the module's name
            assert names <= set(claims['values']), (path, names - set(claims['values']))
    # no claim sentence is copied into the sources by hand
    for key, value in claims['values'].items():
        if len(value) > 40 and not value.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            for path in SOURCE.rglob('*'):
                if path.is_file():
                    assert value[:40] not in path.read_text(), (path, key)


def test_the_page_sources_hold_no_hand_typed_date_or_hash():
    for path in SOURCE.rglob('*'):
        if path.is_file():
            text = path.read_text()
            assert not re.search(r'\b\d{4}-\d{2}-\d{2}\b', text), path
            assert not re.search(r'\b[0-9a-f]{40,64}\b', text), path


@needs_local
def test_the_size_budget_adds_up(built):
    out, record = built
    size = record['size']
    first = size['first_visit']['files']
    assert set(first) == {'index.html', 'app/style.css', 'app/charts.js', 'app/main.js', 'app/claims.json', 'app/space-build.json',
                          'payloads/manifest.json', 'payloads/issued-forecasts.json', 'payloads/outcomes.json',
                          'payloads/evaluation.json', 'payloads/artifact.json'}
    assert first['app/space-build.json'] == (out / 'app/space-build.json').stat().st_size
    for rel, n in first.items():
        assert n == (out / rel).stat().st_size, rel
    train = size['actions']['train_it_yourself']
    assert train['bytes'] == sum(train['parts'].values())
    stem = train['stem']
    assert train['parts']['training_window'] == sum((out / 'payloads' / f'{stem}.{e}').stat().st_size for e in ('json', 'npz'))
    listed = {f['path']: f for f in record['files']}
    assert 'app/space-build.json' not in listed and 'app/worker.js' in listed and 'app/history-files.json' in listed
    history = json.loads((out / 'app/history-files.json').read_text())['files']
    assert {f['path'] for f in history} == {'history/index.html', 'history/assets/app.js'}


@needs_local
def test_the_build_is_deterministic(tmp_path, built):
    first, _ = built
    second = tmp_path / 'dist'
    history = tmp_path / 'v1'
    (history / 'assets').mkdir(parents=True)
    (history / 'index.html').write_text('<!doctype html><title>v1</title>\n')
    (history / 'assets/app.js').write_text('// v1\n')
    build(second, history=history, history_note='a local stand-in for v1\'s export, for this test')

    def tree(root):
        return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob('*')) if p.is_file()}
    a, b = tree(first), tree(second)
    assert a.keys() == b.keys()
    assert [k for k in a if a[k] != b[k]] == []
