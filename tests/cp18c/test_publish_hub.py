"""The Hub publication route (`cp18.publish.HubTarget`, CP-18c item 7) on a recording fake of the Hub: the plan mirrors
the build (v1's root files deleted, `history/` added), one commit against the revision read, the tree checked after;
the refusals; the pinned client in both callers; the host's HTML injection removed, and nothing else accepted."""
from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from cp18 import publish as P

ROOT = Path(__file__).resolve().parents[2]


def _sha1(data: bytes) -> str:
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


class FakeHub:
    def __init__(self, remote: dict[str, bytes], sdk='static', private=False):
        self.trees = {'r0': {k: {'sha1': _sha1(v), 'sha256': None} for k, v in remote.items()}}
        self.sdk, self.private = sdk, private

    def identity(self):
        return {'sdk': self.sdk, 'private': self.private, 'revision': 'r0', 'stage': 'RUNNING'}

    def tree(self, revision):
        return self.trees[revision]


def _build(tmp_path) -> Path:
    b = tmp_path / 'build'
    for rel, data in {'index.html': b'<html><head></head>v6</html>', 'app/main.js': b'x', 'history/index.html': b'v1',
                      'README.md': b'card'}.items():
        (b / rel).parent.mkdir(parents=True, exist_ok=True)
        (b / rel).write_bytes(data)
    return b


def test_the_upload_mirrors_the_build_in_one_commit_against_the_read_revision(tmp_path):
    build = _build(tmp_path)
    hub = FakeHub({'index.html': b'v1 root', 'assets/a.js': b'old', 'README.md': b'card'})
    calls = []

    def committer(b, adds, deletes, parent, message):
        calls.append((adds, deletes, parent))
        hub.trees['r1'] = {p: {'sha1': _sha1((b / p).read_bytes()), 'sha256': None}
                           for p in sorted(str(x.relative_to(b)) for x in b.rglob('*') if x.is_file())}
        return {'commit': 'r1', 'commit_url': 'u'}
    out = P.HubTarget('o/n', authorized=True, hub=hub, committer=committer).upload(build)
    assert calls == [(['app/main.js', 'history/index.html', 'index.html'], ['assets/a.js'], 'r0')]
    assert out['after_revision'] == 'r1' and out['tree']['verified'] and out['planned_deletes'] == ['assets/a.js']


def test_the_route_refuses_without_authorization_and_off_a_public_static_space(tmp_path):
    with pytest.raises(P.PublicationRefused):
        P.HubTarget('o/n')
    for hub in (FakeHub({}, sdk='gradio'), FakeHub({}, private=True)):
        with pytest.raises(P.PublicationRefused):
            P.HubTarget('o/n', authorized=True, hub=hub, committer=lambda *a: None).upload(_build(tmp_path))


def test_a_tree_that_is_not_the_build_after_the_commit_fails(tmp_path):
    hub = FakeHub({})

    def committer(b, adds, deletes, parent, message):
        hub.trees['r1'] = {}
        return {'commit': 'r1'}
    with pytest.raises(P.PublicationRefused):
        P.HubTarget('o/n', authorized=True, hub=hub, committer=committer).upload(_build(tmp_path))


def test_the_html_injection_is_removed_and_nothing_else_is_accepted():
    page = b'<!doctype html><html><head><title>t</title></head></html>'
    want = hashlib.sha256(page).hexdigest()
    injected = page.replace(b'<head>', b'<head><script>window.huggingface={variables:{"A":"1"}};</script>'
                                       b'<meta property="og:title" content="T"><meta name="twitter:card" content="s">')
    assert P.matches('index.html', injected, want) == (True, 'normalized')
    assert P.matches('index.html', page, want) == (True, 'raw')
    assert P.matches('data.json', injected, want)[0] is False
    other = page.replace(b'<head>', b'<head><script>steal()</script>')
    assert P.matches('index.html', other, want)[0] is False
    assert P.space_origin('Yarden-Viktor/delu-day-ahead-forecast') == \
        'https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/'


def test_both_callers_run_the_publication_with_the_pinned_client():
    assert P.HUB_CLIENT == 'huggingface_hub==0.36.2'
    command = P.hub_command(['-m', 'cp18.publish', '--hub', 'o/n'], uv=['uv'])
    assert command == ['uv', 'run', '--frozen', '--no-sync', '--with', P.HUB_CLIENT, 'python', '-m', 'cp18.publish',
                       '--hub', 'o/n']
    workflow = (ROOT / '.github/workflows/daily.yml').read_text()
    step = workflow[workflow.index('The publication to the Hugging Face Space'):]
    step = step[:step.index('- name:', 10)]
    assert f'--with "{P.HUB_CLIENT}"' in step and 'UV_PROJECT_ENVIRONMENT=.venv' in step and '--no-sync' in step
    local = (ROOT / 'src/cp18/local.py').read_text()
    assert 'hub_command(args) if publish == \'hub\'' in local
