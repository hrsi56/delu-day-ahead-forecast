"""Identify the LAND tree without touching any worktree or its real Git index.

The candidate result is checked against round 1's actual curated worktree tree.
The evidence tip then adds evidence only. Both delta and complete-tree lists
are emitted, preserving file modes and blob identities from Git.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path('/Users/djourno/Downloads/PJM')
LEAD = ROOT / '.local/worktrees/cp-26/lead'
EXCLUSION = ROOT / '.local/artifacts/cp-26-landing/exclusion-rule.txt'
EXCLUSION_SHA = '7cbd68734f864d78a076800ecb1db273a8b8e50ba00f0bf79b76d24ac72af565'


def git(*args, env=None, data=None):
    return subprocess.run(['git', '--no-pager', *args], cwd=LEAD, env=env,
                          input=data, capture_output=True, check=True).stdout


def identify(candidate, out):
    out = out.resolve()
    assert out.is_relative_to(ROOT / '.local')
    out.mkdir(parents=True, exist_ok=True)
    main = git('rev-parse', 'main').decode().strip()
    candidate = git('rev-parse', candidate + '^{commit}').decode().strip()
    raw = EXCLUSION.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == EXCLUSION_SHA
    rules = [s.strip() for s in raw.decode().splitlines() if s.strip() and not s.startswith('#')]
    excluded = lambda p: any(p.startswith(r) if r.endswith('/') else p == r for r in rules)
    names = [p.decode() for p in git('diff', '--name-only', '--no-renames', '-z', main, candidate).split(b'\0') if p]
    paths = [p for p in names if not excluded(p)]
    deleted = [p.decode() for p in git('diff', '--diff-filter=D', '--name-only', '-z', main, candidate).split(b'\0') if p]
    assert not set(paths).intersection(deleted)
    entries = {}
    for entry in git('ls-tree', '-r', '-z', candidate).split(b'\0'):
        if entry:
            meta, path = entry.split(b'\t', 1)
            mode, kind, oid = meta.split()
            assert kind == b'blob'
            entries[path.decode()] = mode + b' ' + oid + b'\t' + path + b'\0'
    env = os.environ.copy()
    env['GIT_INDEX_FILE'] = str(out / 'curation.index')
    git('read-tree', main, env=env)
    git('update-index', '-z', '--index-info', env=env,
        data=b''.join(entries[p] for p in paths))
    tree = git('write-tree', env=env).decode().strip()
    files = [p.decode() for p in git('ls-tree', '-r', '--name-only', '-z', tree).split(b'\0') if p]
    (out / 'curated-paths.txt').write_text(''.join(p + '\n' for p in paths))
    (out / 'tree-paths.txt').write_text(''.join(p + '\n' for p in files))
    result = {'main': main, 'candidate': candidate, 'tree': tree,
              'tree_files': len(files), 'curated_paths': len(paths),
              'excluded_paths': len(names) - len(paths), 'exclusion_sha256': EXCLUSION_SHA,
              'curated_paths_sha256': hashlib.sha256((out / 'curated-paths.txt').read_bytes()).hexdigest(),
              'tree_paths_sha256': hashlib.sha256((out / 'tree-paths.txt').read_bytes()).hexdigest(),
              'isolated_index': str(out / 'curation.index')}
    (out / 'curated-tree.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    identify(args.candidate, args.out)
