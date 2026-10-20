"""CP-26 landing repair: run CI's steps on the curated landing tree or the full candidate tree.

Modes (stdlib only; reads the project repository, writes only under --out and, for `worktree`
and `full`, one temporary detached worktree plus the loose tree object of `git write-tree`):

  worktree  the brief's procedure: a detached worktree at main, the curated paths checked out from
            the candidate (`git checkout <candidate> --pathspec-from-file=<list>`), `git write-tree`;
  scratch   CI's view after a squash LAND: a fresh repository holding main's tree plus the curated
            paths as ONE commit, with no history, no tags and no branch objects (actions/checkout@v4
            clones at depth 1). Its tree hash must equal the worktree mode's `git write-tree`;
  full      a detached worktree at the candidate (the full candidate tree).

Each mode then runs `.github/workflows/tests.yml`'s steps in a fresh uv environment
(UV_PROJECT_ENVIRONMENT=<out>/env, Python 3.12 as CI pins it, offline): `uv sync --locked --dev`,
the browser payload, `pytest -q -p no:cacheprovider`, and, for information, CI's later steps.
The environment drops every CP<n>_* variable and PYTHONPATH, and points CP26_PROJECT_ROOT at a
path that does not exist, as `/Users/djourno/Downloads/PJM` does not exist on a CI runner, so no
test can read or write this machine's CP-26 ledger or artifacts.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tarfile
import time

PROJECT = Path('/Users/djourno/Downloads/PJM')
EXCLUSION = PROJECT / '.local/artifacts/cp-26-landing/exclusion-rule.txt'
EXCLUSION_SHA256 = '7cbd68734f864d78a076800ecb1db273a8b8e50ba00f0bf79b76d24ac72af565'
SCRATCH_GIT = ['git', '-c', 'user.name=land-sim', '-c', 'user.email=land-sim@localhost',
               '-c', 'commit.gpgsign=false', '-c', 'core.hooksPath=/dev/null']


def git(*args: str, cwd: Path = PROJECT, data: bool = False):
    run = subprocess.run(['git', *args], cwd=cwd, capture_output=True, check=True)
    return run.stdout if data else run.stdout.decode()


def exclusion_rule() -> list[str]:
    raw = EXCLUSION.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXCLUSION_SHA256:
        raise SystemExit('exclusion rule differs from the brief\'s SHA-256')
    return [line.strip() for line in raw.decode().splitlines() if line.strip() and not line.startswith('#')]


def excluded(path: str, rule: list[str]) -> bool:
    return any(path.startswith(r) if r.endswith('/') else path == r for r in rule)


def curated(main: str, candidate: str) -> tuple[list[str], list[str]]:
    rule = exclusion_rule()
    status = [line.split('\t', 1) for line in
              git('diff', '--name-status', '--no-renames', main, candidate).splitlines() if line]
    deleted = [p for s, p in status if s == 'D' and not excluded(p, rule)]
    if deleted:
        raise SystemExit(f'the candidate deletes curated paths; this script does not handle that: {deleted[:5]}')
    names = [p for _, p in status]
    return [p for p in names if not excluded(p, rule)], [p for p in names if excluded(p, rule)]


def extract(rev: str, paths: list[str], into: Path) -> None:
    for start in range(0, max(len(paths), 1), 400):
        chunk = paths[start:start + 400]
        data = git('archive', '--format=tar', rev, *chunk, data=True)
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            tar.extractall(into, filter='tar')
        if not paths:
            break


def environment(out: Path) -> dict:
    env = {k: v for k, v in os.environ.items()
           if not re.match(r'CP\d+[A-Z]?_', k) and k not in ('PYTHONPATH', 'VIRTUAL_ENV')}
    env.update(UV_PROJECT_ENVIRONMENT=str(out / 'env'), UV_PYTHON='3.12', UV_OFFLINE='1',
               MLFLOW_DISABLE_TELEMETRY='true', DO_NOT_TRACK='1',
               CP26_PROJECT_ROOT=str(out / 'absent-project-root'))
    return env


def steps(tree: Path, out: Path, informational: bool) -> list[dict]:
    env = environment(out)
    plan = [('sync', ['uv', 'sync', '--locked', '--dev']),
            ('payload', ['uv', 'run', 'python', 'scripts/build_wasm_payload.py']),
            ('suite', ['uv', 'run', 'pytest', '-q', '-p', 'no:cacheprovider', '-rfEs'])]
    if informational:
        plan += [('cqr', ['uv', 'run', 'pytest', '-q', '-p', 'no:cacheprovider', 'tests/test_10_cqr_order_statistic.py']),
                 ('verify-release', ['uv', 'run', 'python', 'scripts/verify_release.py']),
                 ('wasm', ['uv', 'run', 'pytest', '-q', '-p', 'no:cacheprovider', 'tests/test_22_wasm_equivalence.py']),
                 ('publication-guard', ['python3', 'scripts/publication_guard.py', 'tree'])]
    results = []
    for name, command in plan:
        began = time.time()
        run = subprocess.run(command, cwd=tree, env=env, capture_output=True, text=True)
        (out / f'{name}.log').write_text(run.stdout + run.stderr)
        lines = [line for line in (run.stdout + run.stderr).splitlines() if line.strip()]
        results.append({'step': name, 'command': command, 'exit_code': run.returncode,
                        'seconds': round(time.time() - began, 1), 'summary': lines[-1] if lines else '',
                        'failed': [line for line in lines if line.startswith(('FAILED ', 'ERROR '))],
                        'tracked_changes_after': git('status', '--porcelain=v1', '--untracked-files=no',
                                                     cwd=tree).splitlines()})
        print(json.dumps({k: v for k, v in results[-1].items() if k != 'command'})[:1500], flush=True)
        if name == 'sync' and run.returncode:
            break
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--mode', choices=('worktree', 'scratch', 'full'), required=True)
    ap.add_argument('--candidate', required=True)
    ap.add_argument('--main', default='main')
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--informational', action='store_true', help="also run CI's later steps")
    ap.add_argument('--keep', action='store_true', help='keep the tree and environment')
    args = ap.parse_args()
    out = args.out.resolve()
    if out.exists():
        raise SystemExit(f'{out} exists')
    out.mkdir(parents=True)
    main_sha = git('rev-parse', '--verify', f'{args.main}^{{commit}}').strip()
    cand = git('rev-parse', '--verify', f'{args.candidate}^{{commit}}').strip()
    record = {'schema': 'cp26-landing-ci-check-v1', 'mode': args.mode, 'main': main_sha, 'candidate': cand,
              'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    tree = out / 'tree'
    if args.mode in ('worktree', 'scratch'):
        paths, omitted = curated(main_sha, cand)
        (out / 'curated-paths.txt').write_text(''.join(p + '\n' for p in paths))
        record.update(curated_paths=len(paths), excluded_paths=len(omitted),
                      curated_bytes=sum(int(line.split()[3]) for line in
                                        git('ls-tree', '-r', '-l', cand, '--', *paths).splitlines()))
    if args.mode == 'worktree':
        git('worktree', 'add', '--detach', str(tree), main_sha)
        git('checkout', cand, f'--pathspec-from-file={out / "curated-paths.txt"}', cwd=tree)
        record['tree'] = git('write-tree', cwd=tree).strip()
    elif args.mode == 'scratch':
        tree.mkdir()
        extract(main_sha, [], tree)
        extract(cand, paths, tree)
        subprocess.run([*SCRATCH_GIT, 'init', '-q', '-b', 'ci-sim'], cwd=tree, check=True)
        subprocess.run([*SCRATCH_GIT, 'add', '-A', '-f'], cwd=tree, check=True)
        subprocess.run([*SCRATCH_GIT, 'commit', '-q', '-m', f'simulated squash of {cand} onto {main_sha}'],
                       cwd=tree, check=True)
        record['tree'] = git('rev-parse', 'HEAD^{tree}', cwd=tree).strip()
        record['scratch_commits'] = int(git('rev-list', '--count', 'HEAD', cwd=tree))
    else:
        git('worktree', 'add', '--detach', str(tree), cand)
        record['tree'] = git('rev-parse', f'{cand}^{{tree}}').strip()
    record['tree_files'] = len(git('ls-files', cwd=tree).splitlines())
    print(json.dumps(record), flush=True)
    record['steps'] = steps(tree, out, args.informational)
    record['suite_green'] = any(s['step'] == 'suite' and s['exit_code'] == 0 for s in record['steps'])
    record['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    if not args.keep:
        if args.mode == 'scratch':
            shutil.rmtree(tree)
        else:
            git('worktree', 'remove', '--force', str(tree))
        shutil.rmtree(out / 'env', ignore_errors=True)
        record['cleaned'] = True
    (out / 'ci-check.json').write_text(json.dumps(record, indent=1) + '\n')
    print(json.dumps({k: v for k, v in record.items() if k != 'steps'}), flush=True)
    return 0 if record['suite_green'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
