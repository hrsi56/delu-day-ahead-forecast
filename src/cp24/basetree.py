"""The tree CP-24 started from, file by file (§23.13 items 1 and 16; §23.14's "never written" and "preserve").

`reports/ddnn2/base-tree.json` records the SHA-256 of every file tracked at CP-24's base commit (the issued
`main`, `522d7ea`), read from the Git objects. CP-24 writes only its own paths (`src/cp24/`, `tests/cp24/`,
`scripts/cp24_*.py`, `reports/ddnn2/`, `docs/track-b/evidence/cp-24/`, `docs/track-b/research-content/cp24-claims.md`),
none of which existed at the base, so every recorded file must be byte-identical in the candidate: the public
surfaces, the published export set, `scripts/mlflow_export.py`, the root `pyproject.toml` and `uv.lock`, every
earlier checkpoint's code, reports and evidence, every locked document and `progress.md`.
`tests/cp24/test_base_tree.py` checks it without Git (CI checks out a shallow tree).

Run as ``python -m cp24.basetree`` (writes once) or ``--check``.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = '522d7ea722b5d215d827d7aed9c56b7a9dec066e'
PATH = ROOT / 'reports/ddnn2/base-tree.json'
CP24_PATHS = ('src/cp24/', 'tests/cp24/', 'scripts/cp24_', 'reports/ddnn2/', 'docs/track-b/evidence/cp-24/',
              'docs/track-b/research-content/cp24-claims.md')


def build() -> dict:
    listing = subprocess.check_output(['git', 'ls-tree', '-r', '-z', BASE], cwd=ROOT).split(b'\0')
    entries = []
    for item in filter(None, listing):
        meta, name = item.split(b'\t', 1)
        mode, kind, obj = meta.split()
        if kind != b'blob':
            continue
        name = name.decode('utf-8')
        if name.startswith(CP24_PATHS):
            raise ValueError(f'{name}: a CP-24 path existed at the base')
        entries.append((name, obj.decode()))
    batch = subprocess.run(['git', 'cat-file', '--batch'], cwd=ROOT, input=''.join(f'{o}\n' for _, o in entries).encode(),
                           capture_output=True, check=True).stdout
    out, pos = {}, 0
    for name, obj in entries:
        header_end = batch.index(b'\n', pos)
        size = int(batch[pos:header_end].split()[2])
        content = batch[header_end + 1:header_end + 1 + size]
        pos = header_end + 1 + size + 1
        out[name] = hashlib.sha256(content).hexdigest()
    return {'schema': 'cp24-base-tree-v1', 'base_commit': BASE, 'files': len(out), 'sha256': out}


def check(record: dict) -> list[str]:
    bad = []
    for name, digest in record['sha256'].items():
        p = ROOT / name
        if not p.is_file():
            bad.append(f'missing: {name}')
            continue
        h = hashlib.sha256()
        with p.open('rb') as handle:
            for chunk in iter(lambda: handle.read(1 << 20), b''):
                h.update(chunk)
        if h.hexdigest() != digest:
            bad.append(f'changed: {name}')
    return bad


def main() -> int:
    if '--check' in sys.argv[1:]:
        bad = check(json.loads(PATH.read_text()))
        print(json.dumps({'unchanged': not bad, 'problems': bad[:20]}))
        return 0 if not bad else 1
    if PATH.exists():
        raise SystemExit('base-tree.json exists; it is written once')
    PATH.write_text(json.dumps(build(), indent=1, sort_keys=True) + '\n')
    print(f'wrote {PATH}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
