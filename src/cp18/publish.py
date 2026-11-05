"""The publication step: a verified bundle and the Space, published to a static host, then the served identity checked.

**Prepared, not run against Hugging Face.** This round exercises it against a local static server only
(`LocalTarget`, served from `127.0.0.1`). The Hugging Face upload is CP-18's activation, with the Owner's `HF_TOKEN`;
`HubTarget` holds that path and refuses to write unless the activation passes `authorized=True` (nothing in this round
does), and it reads the token only inside its one commit, never printing, logging or writing it.

**One publication, in order** (`publish`), failing closed at the first failure:

1. **The gate** (`cp18.bundle.gate`): R7's verification, the frozen identity and the red line, and the native
   recomputation check. A refused bundle is never published: a mismatch is a product failure for that day.
2. **The Space build carries exactly that bundle** at `payloads/`, byte for byte, and its own build record
   (`app/space-build.json`) lists every served file with its SHA-256.
3. **The upload** of the whole build to the target, in one operation.
4. **The served identity** (`verify_served`): the served `payloads/manifest.json` is fetched as a visitor would fetch
   it, and must equal the intended manifest byte for byte; every file it lists, and every file of the Space's build
   record, is fetched and must hash as intended; the served manifest must name the intended daily artifact. Any
   difference fails the publication.

The record of each publication is appended to `live/bundles/` (`cp18.records`).
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import http.server
import json
import os
from pathlib import Path
import shutil
import threading
import urllib.parse
import urllib.request

from .bundle import gate, read
from .records import RecordLog

SCHEMA = 'cp18b-publication-v1'
LOOPBACK = ('127.0.0.1', 'localhost', '[::1]')


class PublicationRefused(RuntimeError):
    pass


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def tree(folder: Path) -> dict[str, bytes]:
    folder = Path(folder)
    return {str(p.relative_to(folder)): p.read_bytes() for p in sorted(folder.rglob('*'))
            if p.is_file() and p.name != '.DS_Store'}


# ------------------------------------------------------------------ targets
class LocalTarget:
    """A static host on this machine: the build is copied into `folder`, which a local server serves."""

    kind = 'local static server'

    def __init__(self, folder):
        self.folder = Path(folder)

    def upload(self, build: Path) -> dict:
        staging = self.folder.with_name(self.folder.name + '.staging')
        if staging.exists():
            shutil.rmtree(staging)
        shutil.copytree(build, staging)
        if self.folder.exists():
            shutil.rmtree(self.folder)
        staging.rename(self.folder)              # one operation: the old build or the new, never a mixture
        return {'target': self.kind, 'files': len(tree(self.folder))}


class HubTarget:
    """The Hugging Face Static Space (CP-18's activation): one Hub commit of the whole build. Refuses unless
    `authorized`; the token is read inside `upload` only, as `os.environ.get`, and is never emitted."""

    kind = 'Hugging Face Static Space'

    def __init__(self, repo: str, *, authorized: bool = False):
        if not authorized:
            raise PublicationRefused('the Hugging Face upload is CP-18\'s activation; nothing was uploaded')
        self.repo = repo

    def upload(self, build: Path) -> dict:              # pragma: no cover - activation only
        token = os.environ.get('HF_TOKEN')
        if not token:
            raise PublicationRefused('HF_TOKEN is unset; no upload was attempted')
        from huggingface_hub import HfApi                  # `uv run --with huggingface_hub`, as scripts/deploy_space.py
        info = HfApi(token=token).upload_folder(repo_id=self.repo, repo_type='space', folder_path=str(build),
                                                commit_message='Daily bundle (data-only)', delete_patterns=['payloads/*'])
        return {'target': self.kind, 'commit': getattr(info, 'oid', None)}


def listed(build: Path) -> dict[str, dict]:
    """Every file the Space's build record lists ({path: {'sha256', 'bytes'}}), with History's own listing when the build
    carries one (`app/history-files.json`, itself listed and so bound by its hash)."""
    record = json.loads((Path(build) / 'app' / 'space-build.json').read_text())
    files = record['files']
    out = {f['path']: f for f in files} if isinstance(files, list) else dict(files)
    history = Path(build) / 'app' / 'history-files.json'
    if 'app/history-files.json' in out and history.is_file():
        out.update({f['path']: f for f in json.loads(history.read_text())['files']})
    return out


# ------------------------------------------------------------------ reading what is served
def http_fetch(base: str):
    """A visitor's GET of `base`/<path>. In this round only a loopback host is allowed."""
    parsed = urllib.parse.urlparse(base)
    if parsed.hostname not in ('127.0.0.1', 'localhost', '::1'):
        raise PublicationRefused(f'{parsed.hostname}: only a local static server is read in this round')

    def get(path: str) -> bytes | None:
        url = base.rstrip('/') + '/' + urllib.parse.quote(path)
        try:
            with urllib.request.urlopen(url, timeout=30) as response:   # noqa: S310 - loopback only
                return response.read()
        except urllib.error.HTTPError:
            return None
    return get


def verify_served(fetch, build: Path, bundle: Path) -> dict:
    """The served identity against the intended build and bundle; every difference is listed."""
    intended = read(bundle)
    problems = []
    served_manifest = fetch('payloads/manifest.json')
    if served_manifest is None:
        return {'served_identity_equal': False, 'problems': ['payloads/manifest.json is not served'], 'checked': 0}
    if served_manifest != intended['manifest.json']:
        problems.append('the served manifest is not the intended one')
    manifest = json.loads(served_manifest)
    want = json.loads(intended['manifest.json'])
    if manifest.get('artifact', {}).get('artifact_sha256') != want['artifact']['artifact_sha256']:
        problems.append('the served manifest names another daily artifact')
    checked = 1
    for f in manifest.get('files', []):
        data = fetch('payloads/' + f['path'])
        checked += 1
        if data is None or sha(data) != f['sha256'] or len(data) != f['bytes']:
            problems.append(f"payloads/{f['path']}: not served as the manifest lists it")
    for path, item in sorted(listed(build).items()):
        data = fetch(path)
        checked += 1
        if data is None or sha(data) != item['sha256']:
            problems.append(f'{path}: not served as the Space build lists it')
    served_artifact = fetch('payloads/artifact.json')
    if served_artifact is None or json.loads(served_artifact).get('artifact_sha256') != want['artifact']['artifact_sha256']:
        problems.append('the served artifact is not the intended daily artifact')
    return {'served_identity_equal': not problems, 'problems': problems[:50], 'checked': checked,
            'served_manifest_sha256': sha(served_manifest), 'intended_manifest_sha256': sha(intended['manifest.json']),
            'artifact_sha256': want['artifact']['artifact_sha256']}


def publish(build: Path, bundle: Path, target, fetch, root=None) -> dict:
    """Gate, check the build carries the bundle, upload, verify the served identity. Never raises for a failed step:
    the record says where it stopped."""
    build, bundle = Path(build), Path(bundle)
    out = {'schema': SCHEMA, 'target': target.kind, 'bundle': str(bundle), 'build': str(build), 'published': False}
    files = read(bundle)
    verdict = gate(files, root)
    out['gate'] = {'publishable': verdict['publishable'], 'reason': verdict['reason'],
                   'verify_problems': verdict['verify']['problems'][:10],
                   'recompute_match': (verdict['recompute'] or {}).get('match')}
    if not verdict['publishable']:
        out['stopped'] = 'the gate refused the bundle: nothing was uploaded'
        return out
    carried = {k: v for k, v in tree(build).items() if k.startswith('payloads/')}
    if carried != {f'payloads/{k}': v for k, v in files.items()}:
        out['stopped'] = 'the Space build does not carry exactly this bundle: nothing was uploaded'
        return out
    built = tree(build)
    if any(sha(built.get(p, b'')) != i['sha256'] for p, i in listed(build).items()):
        out['stopped'] = 'the Space build differs from its own build record: nothing was uploaded'
        return out
    try:
        out['upload'] = target.upload(build)
    except Exception as exc:          # a failed upload is recorded by its type only
        out['stopped'] = f'the upload failed ({type(exc).__name__})'
        return out
    out['served'] = verify_served(fetch, build, bundle)
    out['published'] = out['served']['served_identity_equal']
    if not out['published']:
        out['stopped'] = 'the served identity is not the intended one: the publication failed'
    return out


@contextmanager
def local_server(folder: Path):
    """A static server on 127.0.0.1 for `folder` (WebAssembly with its media type), in a thread."""
    folder = Path(folder)

    class Handler(http.server.SimpleHTTPRequestHandler):
        extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, '.wasm': 'application/wasm',
                          '.mjs': 'text/javascript', '.json': 'application/json'}

        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(folder), **kwargs)

        def log_message(self, *args):
            pass

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_address[1]}/'
    finally:
        server.shutdown()
        server.server_close()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='python -m cp18.publish')
    ap.add_argument('--build', required=True, type=Path, help='the built Space (scripts/build_product_space.py)')
    ap.add_argument('--bundle', required=True, type=Path)
    ap.add_argument('--target', required=True, type=Path, help='the local folder the local static server serves')
    ap.add_argument('--root', default='.', type=Path)
    ap.add_argument('--record', type=Path)
    ap.add_argument('--live', type=Path, help='append the publication to <live>/bundles/')
    args = ap.parse_args(argv)
    target = LocalTarget(args.target)
    args.target.parent.mkdir(parents=True, exist_ok=True)
    args.target.mkdir(exist_ok=True)
    with local_server(args.target) as base:
        value = publish(args.build, args.bundle, target, http_fetch(base), args.root)
        value['served_from'] = base
    if args.live and value['published']:
        manifest = json.loads((args.bundle / 'manifest.json').read_text())
        as_of = manifest['freshness']['as_of_day']
        RecordLog(args.live / 'bundles').append('publication', f'{as_of}/publication.json', value, as_of_day=as_of,
                                                manifest_sha256=value['served']['served_manifest_sha256'])
    if args.record:
        args.record.parent.mkdir(parents=True, exist_ok=True)
        args.record.write_text(json.dumps(value, indent=1, sort_keys=True) + '\n')
    print('published' if value['published'] else f"NOT published: {value.get('stopped')}",
          (value.get('served') or {}).get('checked', 0), 'files checked')
    return 0 if value['published'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
