"""Lead-only round-3 preparation and round-1 suite reproduction.

Stress/CI commands reuse the immutable round-2 stress_check.py. All scratch commits
use the repository's mandatory secret hooks and a message file; none bypasses a hook.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

PROJECT = Path('/Users/djourno/Downloads/PJM')
HERE = Path(__file__).resolve()
spec = importlib.util.spec_from_file_location('round2', HERE.parents[1] / 'landing-repair-2/stress_check.py')
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)


def git(*args, cwd=PROJECT):
    return subprocess.run(['git', '--no-pager', *args], cwd=cwd, check=True,
                          capture_output=True, text=True).stdout


def prepare(args):
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    candidate = git('rev-parse', f'{args.candidate}^{{commit}}').strip()
    main = git('rev-parse', 'main').strip()
    status = [line.split('\t', 1) for line in git('diff', '--name-status', '--no-renames', main, candidate).splitlines()]
    rule = R.exclusion_rule()
    paths = [p for _, p in status if not R.excluded(p, rule)]
    assert not any(s == 'D' and p in paths for s, p in status)
    listing = out / 'curated-paths.txt'
    listing.write_text(''.join(p + '\n' for p in paths))
    curated = out / 'curated'
    git('worktree', 'add', '--detach', str(curated), main)
    git('checkout', candidate, f'--pathspec-from-file={listing}', cwd=curated)
    tree = git('write-tree', cwd=curated).strip()
    copies = []
    for name in ('copy312', 'copy313'):
        copy = out / name
        copy.mkdir()
        archive = subprocess.Popen(['git', 'archive', tree], cwd=PROJECT, stdout=subprocess.PIPE)
        subprocess.run(['tar', '-x', '-C', str(copy)], stdin=archive.stdout, check=True)
        archive.stdout.close()
        assert archive.wait() == 0
        git('init', '-q', '-b', 'main', cwd=copy)
        # Enable the exact mandatory hooks for this new, history-free repository.
        git('config', 'core.hooksPath', str(PROJECT / '.githooks'), cwd=copy)
        git('add', '-A', cwd=copy)
        message = out / f'{name}-commit.txt'
        message.write_text('ci\n')
        git('-c', 'user.name=ci', '-c', 'user.email=ci@localhost', '-c', 'commit.gpgsign=false',
            'commit', '-q', '-F', str(message), cwd=copy)
        actual = git('rev-parse', 'HEAD^{tree}', cwd=copy).strip()
        assert actual == tree and not git('status', '--porcelain=v1', cwd=copy)
        assert git('rev-list', '--all', '--count', cwd=copy).strip() == '1'
        assert not git('tag', '--list', cwd=copy)
        copies.append({'path': str(copy), 'tree': actual, 'commits': 1, 'clean': True,
                       'hooks': git('config', '--get', 'core.hooksPath', cwd=copy).strip()})
    record = {'candidate': candidate, 'main': main, 'tree': tree,
              'tree_files': len(git('ls-tree', '-r', '--name-only', tree).splitlines()),
              'curated_paths': len(paths), 'excluded_paths': len(status) - len(paths),
              'curated_paths_sha256': hashlib.sha256(listing.read_bytes()).hexdigest(),
              'copies': copies, 'curated_worktree': str(curated)}
    (out / 'copy.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))


def suite(args):
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    env = R.environment(args.env.resolve(), '3.12')
    tree = args.tree.resolve()
    record = {'candidate': args.candidate, 'tree': git('write-tree', cwd=tree).strip(),
              'head': git('rev-parse', 'HEAD', cwd=tree).strip(), 'steps': []}
    for label, command in (
        ('sync', ['uv', 'sync', '--locked', '--dev']),
        ('payload', ['uv', 'run', 'python', 'scripts/build_wasm_payload.py']),
        ('suite', ['uv', 'run', 'pytest', '-q', '-p', 'no:cacheprovider'])):
        result = R.run_logged(command, tree, env, out / f'{label}.log')
        result['step'] = label
        record['steps'].append(result)
        print(json.dumps(result), flush=True)
        if result['exit_code']:
            break
    record['green'] = len(record['steps']) == 3 and all(s['exit_code'] == 0 for s in record['steps'])
    (out / 'suite.json').write_text(json.dumps(record, indent=2) + '\n')
    return 0 if record['green'] else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='action', required=True)
    p = sub.add_parser('prepare')
    p.add_argument('--candidate', required=True)
    p.add_argument('--out', type=Path, required=True)
    s = sub.add_parser('suite')
    for name in ('tree', 'env', 'out'):
        s.add_argument(f'--{name}', type=Path, required=True)
    s.add_argument('--candidate', required=True)
    args = ap.parse_args()
    return prepare(args) if args.action == 'prepare' else suite(args)


if __name__ == '__main__':
    sys.exit(main())
