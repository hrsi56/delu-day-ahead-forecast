"""CP-26 landing repair 2: the history-free curated copy, the runner emulation and CI's seven steps.

Stdlib only. Subcommands:

  copy     build the curated landing tree by round 1's procedure (a detached worktree at main, the
           curated paths checked out from the candidate, `git write-tree`), then the brief's
           history-free copy: `git archive <tree> | tar -x`, `git init -q -b main`, `git add -A`,
           `git commit -q --no-verify -m ci`. With --keep-worktree the curated worktree stays for
           round 1's full-suite procedure; otherwise it is removed.
  burners  start | stop the emulation's four (--count) `while :; do :; done` loops, detached from any
           monitor; the record keeps their PIDs and wall time.
  stress   run one test node N times in the copy, each under its own --basetemp, and read its
           timing from the files the test itself writes (no instrumentation in the test): the
           markers' mtimes and the inner ledger. Used for the rich-admin test.
  pytest   run one pytest selection once in the copy (for example the 452 CP-26 tests).
  ci       run `.github/workflows/tests.yml`'s seven steps in the copy, as the brief lists them.

Every test subprocess gets CI's view: CP<n>_* variables, PYTHONPATH, VIRTUAL_ENV and
PYTHONDONTWRITEBYTECODE are dropped (CI does not set the last; this machine's shell does);
UV_PROJECT_ENVIRONMENT and UV_PYTHON are set; uv runs offline from its cache; MLflow telemetry is
off; CP26_PROJECT_ROOT points at a path that does not exist, as /Users/djourno/Downloads/PJM does
not exist on a runner.

Timing read from a rich-admin run's basetemp (wall-clock mtimes, nanosecond resolution):
  controller_wait_upper   owners.stop - owners.busy. The controller writes `busy`, launches the
                          admin monitor, blocks in communicate(), checks the result, then writes
                          `stop`; so this bounds the controller's wait from above.
  controller_wait_lower   admin.report.json - owners.busy: the admin child writes its report
                          just before it exits, so the wait is at least this.
  owner_span_max          max over owners of owners.stop - busy-owner-<i>.ready. Each owner fixes
                          its self-deadline when it writes `ready`, so this is the span that
                          deadline must cover.
  ready_spread            last ready - first ready.
  owner_exit_after_stop   max owner ended_epoch in the inner ledger - owners.stop (informational,
                          for the controller's 20 s wait on the owners).
  admin_job_wall          the admin job's wall_seconds in the inner ledger.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time
import xml.etree.ElementTree as ET

PROJECT = Path('/Users/djourno/Downloads/PJM')
EXCLUSION = PROJECT / '.local/artifacts/cp-26-landing/exclusion-rule.txt'
EXCLUSION_SHA256 = '7cbd68734f864d78a076800ecb1db273a8b8e50ba00f0bf79b76d24ac72af565'
SCRATCH_GIT = ['git', '-c', 'user.name=ci', '-c', 'user.email=ci@localhost', '-c', 'commit.gpgsign=false']
RICH_ADMIN = ('tests/test_cp26_ledger_liveness.py::'
              'test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history')
OWNERS = ('ledger-liveness-0', 'ledger-liveness-1', 'ledger-liveness-2')


def git(*args: str, cwd: Path = PROJECT) -> str:
    return subprocess.run(['git', *args], cwd=cwd, capture_output=True, check=True, text=True).stdout


def now_utc() -> str:
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


def exclusion_rule() -> list[str]:
    raw = EXCLUSION.read_bytes()
    if hashlib.sha256(raw).hexdigest() != EXCLUSION_SHA256:
        raise SystemExit("exclusion rule differs from round 1's SHA-256")
    return [line.strip() for line in raw.decode().splitlines() if line.strip() and not line.startswith('#')]


def excluded(path: str, rule: list[str]) -> bool:
    return any(path.startswith(r) if r.endswith('/') else path == r for r in rule)


def environment(env_dir: Path, python: str) -> dict:
    env = {k: v for k, v in os.environ.items()
           if not re.match(r'CP\d+[A-Z]?_', k)
           and k not in ('PYTHONPATH', 'VIRTUAL_ENV', 'PYTHONDONTWRITEBYTECODE')}
    env.update(UV_PROJECT_ENVIRONMENT=str(env_dir), UV_PYTHON=python, UV_OFFLINE='1',
               MLFLOW_DISABLE_TELEMETRY='true', DO_NOT_TRACK='1',
               CP26_PROJECT_ROOT=str(env_dir.parent / 'absent-project-root'))
    return env


def run_logged(command: list[str], cwd: Path, env: dict, log: Path) -> dict:
    began = time.time()
    run = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)
    log.write_text(run.stdout + run.stderr)
    lines = [line for line in (run.stdout + run.stderr).splitlines() if line.strip()]
    summary = next((line for line in reversed(lines) if re.search(r'\d+ (passed|failed|error)', line)),
                   lines[-1] if lines else '')
    return {'command': command, 'exit_code': run.returncode, 'seconds': round(time.time() - began, 2),
            'summary': summary, 'log': str(log),
            'failed': [line for line in lines if line.startswith(('FAILED ', 'ERROR '))],
            'timeout_lines': [line for line in lines if 'TimeoutExpired' in line][:4]}


# ---- copy ---------------------------------------------------------------------------------------

def cmd_copy(args) -> int:
    out = args.out.resolve()
    if out.exists():
        raise SystemExit(f'{out} exists')
    out.mkdir(parents=True)
    main_sha = git('rev-parse', '--verify', f'{args.main}^{{commit}}').strip()
    cand = git('rev-parse', '--verify', f'{args.candidate}^{{commit}}').strip()
    rule = exclusion_rule()
    status = [line.split('\t', 1) for line in
              git('diff', '--name-status', '--no-renames', main_sha, cand).splitlines() if line]
    if any(s == 'D' and not excluded(p, rule) for s, p in status):
        raise SystemExit('the candidate deletes a curated path; this tool does not handle that')
    paths = [p for _, p in status if not excluded(p, rule)]
    listing = out / 'curated-paths.txt'
    listing.write_text(''.join(p + '\n' for p in paths))
    worktree = out / 'curated'
    git('worktree', 'add', '--detach', str(worktree), main_sha)
    git('checkout', cand, f'--pathspec-from-file={listing}', cwd=worktree)
    tree = git('write-tree', cwd=worktree).strip()
    files = git('ls-tree', '-r', '--name-only', tree).splitlines()
    copy = out / 'copy'
    copy.mkdir()
    archive = subprocess.Popen(['git', 'archive', tree], cwd=PROJECT, stdout=subprocess.PIPE)
    subprocess.run(['tar', '-x', '-C', str(copy)], stdin=archive.stdout, check=True)
    archive.stdout.close()
    if archive.wait():
        raise SystemExit('git archive failed')
    subprocess.run([*SCRATCH_GIT, 'init', '-q', '-b', 'main'], cwd=copy, check=True)
    subprocess.run([*SCRATCH_GIT, 'add', '-A'], cwd=copy, check=True)
    subprocess.run([*SCRATCH_GIT, 'commit', '-q', '--no-verify', '-m', 'ci'], cwd=copy, check=True)
    copy_tree = git('rev-parse', 'HEAD^{tree}', cwd=copy).strip()
    record = {'schema': 'cp26-landing-repair-2-copy-v1', 'main': main_sha, 'candidate': cand,
              'curated_paths': len(paths), 'excluded_paths': len(status) - len(paths),
              'curated_paths_sha256': hashlib.sha256(listing.read_bytes()).hexdigest(),
              'tree': tree, 'tree_files': len(files), 'copy_tree': copy_tree,
              'copy_tree_matches': copy_tree == tree,
              'copy_commits': int(git('rev-list', '--all', '--count', cwd=copy)),
              'copy_tags': git('tag', cwd=copy).split(), 'created_utc': now_utc()}
    if not args.keep_worktree:
        git('worktree', 'remove', '--force', str(worktree))
        record['curated_worktree'] = 'removed'
    else:
        record['curated_worktree'] = str(worktree)
    (out / 'copy.json').write_text(json.dumps(record, indent=1) + '\n')
    print(json.dumps(record))
    return 0 if record['copy_tree_matches'] else 1


# ---- burners ------------------------------------------------------------------------------------

def cmd_burners(args) -> int:
    record_path = args.record.resolve()
    if args.action == 'start':
        if record_path.exists():
            raise SystemExit(f'{record_path} exists')
        pids = [subprocess.Popen(['/bin/sh', '-c', 'while :; do :; done'], start_new_session=True,
                                 stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                 stderr=subprocess.DEVNULL).pid for _ in range(args.count)]
        record = {'pids': pids, 'count': args.count, 'started_epoch': time.time(), 'started_utc': now_utc()}
        record_path.write_text(json.dumps(record, indent=1) + '\n')
        print(json.dumps(record))
        return 0
    record = json.loads(record_path.read_text())
    for pid in record['pids']:
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    time.sleep(0.2)
    alive = []
    for pid in record['pids']:
        try:
            os.kill(pid, 0)
            alive.append(pid)
        except ProcessLookupError:
            pass
    record.update(stopped_epoch=time.time(), stopped_utc=now_utc(), alive_after_stop=alive)
    record['wall_seconds'] = round(record['stopped_epoch'] - record['started_epoch'], 2)
    record['burner_seconds'] = round(len(record['pids']) * record['wall_seconds'], 2)
    record_path.write_text(json.dumps(record, indent=1) + '\n')
    print(json.dumps(record))
    return 0 if not alive else 1


# ---- stress -------------------------------------------------------------------------------------

def mtime(path: Path) -> float:
    return path.stat().st_mtime_ns / 1e9


def rich_admin_timing(basetemp: Path) -> dict:
    # pytest 9 adds a `<name>current` symlink beside the numbered directory; count each once.
    hits = sorted({Path(p).parent.resolve() for p in glob.glob(str(basetemp / '*' / 'owners.busy'))})
    if len(hits) != 1:
        return {'found': False, 'basetemp_entries': sorted(
            str(p.relative_to(basetemp)) for p in basetemp.glob('*/*'))[:20] if basetemp.is_dir() else None}
    d = hits[0]
    timing: dict = {'found': True}
    ready = [d / f'busy-owner-{i}.ready' for i in range(3)]
    busy, stop, report = d / 'owners.busy', d / 'owners.stop', d / 'admin.report.json'
    if all(p.exists() for p in ready):
        timing['ready_spread'] = round(max(map(mtime, ready)) - min(map(mtime, ready)), 3)
    if report.exists():
        timing['controller_wait_lower'] = round(mtime(report) - mtime(busy), 3)
        timing['admin_observations'] = len(json.loads(report.read_text())['observations'])
    if stop.exists():
        timing['controller_wait_upper'] = round(mtime(stop) - mtime(busy), 3)
        timing['owner_span_max'] = round(max(mtime(stop) - mtime(p) for p in ready), 3)
    ledger = d / '.local/artifacts/cp-26/ledger/budget.json'
    if ledger.exists():
        jobs = json.loads(ledger.read_text())['jobs']
        admin = [j for j in jobs if j.get('name') == 'ledger-rich-admin']
        owners = [j for j in jobs if j.get('name') in OWNERS]
        if admin:
            timing['admin_job_wall'] = round(admin[0].get('wall_seconds') or 0.0, 3)
            timing['admin_exit_code'] = admin[0].get('exit_code')
            timing['admin_abort_reason'] = admin[0].get('abort_reason')
        if owners and stop.exists() and all(j.get('ended_epoch') for j in owners):
            timing['owner_exit_after_stop'] = round(max(j['ended_epoch'] for j in owners) - mtime(stop), 3)
        timing['owner_abort_reasons'] = [j.get('abort_reason') for j in owners]
        # Lifetime peaks of each owner's supervisor and watchdog lock telemetry, as last published
        # (the admin asserts peak wait and hold < 0.5 s while it observes; these bound what it saw).
        peaks = [(j.get(f'{role}_ledger_lock_telemetry') or {}) for j in owners for role in ('supervisor', 'watchdog')]
        if peaks and all(peaks):
            timing['owner_lock_peak_wait_max'] = round(max(p['peak_wait_seconds'] for p in peaks), 4)
            timing['owner_lock_peak_hold_max'] = round(max(p['peak_hold_seconds'] for p in peaks), 4)
            timing['owner_lock_timeouts'] = sum(p['timeouts'] for p in peaks)
    return timing


def junit_time(xml: Path) -> float | None:
    if not xml.exists():
        return None
    case = ET.parse(xml).getroot().find('.//testcase')
    return None if case is None else round(float(case.get('time')), 3)


def sync(copy: Path, env: dict, out: Path, label: str) -> dict:
    result = run_logged(['uv', 'sync', '--locked', '--dev'], copy, env, out / f'{label}-sync.log')
    if result['exit_code']:
        raise SystemExit(f"uv sync failed: {result['summary']}")
    return result


def cmd_stress(args) -> int:
    copy, out = args.copy.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    env = environment(args.env.resolve(), args.python)
    record = {'schema': 'cp26-landing-repair-2-stress-v1', 'label': args.label, 'node': args.node,
              'python': args.python, 'copy_head': git('rev-parse', 'HEAD', cwd=copy).strip(),
              'copy_tree': git('rev-parse', 'HEAD^{tree}', cwd=copy).strip(),
              'emulation': args.emulation, 'started_utc': now_utc(),
              'sync': sync(copy, env, out, args.label), 'runs': []}
    record['interpreter'] = subprocess.run(['uv', 'run', 'python', '-c', 'import sys; print(sys.version)'],
                                           cwd=copy, env=env, capture_output=True, text=True).stdout.strip()
    for index in range(args.runs):
        basetemp = out / f'{args.label}-bt-{index}'
        xml = out / f'{args.label}-{index}.xml'
        result = run_logged(['uv', 'run', 'pytest', '-q', '-p', 'no:cacheprovider', args.node,
                             f'--basetemp={basetemp}', f'--junitxml={xml}'],
                            copy, env, out / f'{args.label}-{index}.log')
        result.update(index=index, test_seconds=junit_time(xml), timing=rich_admin_timing(basetemp))
        del result['command']
        # Keep the inner jobs' own logs (the admin child's stderr lands there, not in pytest's output).
        kept = out / f'{args.label}-{index}-inner-logs'
        for log in {Path(p).resolve() for p in glob.glob(str(basetemp / '*/.local/artifacts/cp-26/logs/*.log'))}:
            kept.mkdir(exist_ok=True)
            shutil.copy2(log, kept / log.name)
        result['inner_logs'] = str(kept) if kept.exists() else None
        record['runs'].append(result)
        print(json.dumps(result), flush=True)
        shutil.rmtree(basetemp, ignore_errors=True)
        xml.unlink(missing_ok=True)
    record['passed'] = sum(1 for r in record['runs'] if r['exit_code'] == 0)
    record['finished_utc'] = now_utc()
    (out / f'{args.label}.json').write_text(json.dumps(record, indent=1) + '\n')
    print(json.dumps({k: record[k] for k in ('label', 'passed', 'emulation', 'copy_tree')}))
    return 0 if record['passed'] == args.runs else 1


# ---- pytest selection and CI's seven steps ------------------------------------------------------

def cmd_pytest(args) -> int:
    copy, out = args.copy.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    env = environment(args.env.resolve(), args.python)
    selection = sorted({p for pattern in args.select for p in glob.glob(pattern, root_dir=copy)})
    record = {'schema': 'cp26-landing-repair-2-pytest-v1', 'label': args.label, 'python': args.python,
              'copy_tree': git('rev-parse', 'HEAD^{tree}', cwd=copy).strip(), 'emulation': args.emulation,
              'files': len(selection), 'started_utc': now_utc(), 'sync': sync(copy, env, out, args.label)}
    record['run'] = run_logged(['uv', 'run', 'pytest', '-q', '-p', 'no:cacheprovider', '-rfE', *selection],
                               copy, env, out / f'{args.label}.log')
    record['run']['command'] = record['run']['command'][:6] + [f'<{len(selection)} files>']
    record['finished_utc'] = now_utc()
    (out / f'{args.label}.json').write_text(json.dumps(record, indent=1) + '\n')
    print(json.dumps({k: v for k, v in record['run'].items() if k != 'command'}))
    return record['run']['exit_code']


def cmd_ci(args) -> int:
    copy, out = args.copy.resolve(), args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    env = environment(args.env.resolve(), args.python)
    plan = [('sync', ['uv', 'sync', '--locked', '--dev']),
            ('payload', ['uv', 'run', 'python', 'scripts/build_wasm_payload.py']),
            ('suite', ['uv', 'run', 'pytest', '-q']),
            ('cqr', ['uv', 'run', 'pytest', 'tests/test_10_cqr_order_statistic.py', '-q']),
            ('verify-release', ['uv', 'run', 'python', 'scripts/verify_release.py']),
            ('wasm', ['uv', 'run', 'pytest', 'tests/test_22_wasm_equivalence.py', '-q']),
            ('publication-guard', ['python3', 'scripts/publication_guard.py', 'tree'])]
    record = {'schema': 'cp26-landing-repair-2-ci-v1', 'label': args.label, 'python': args.python,
              'copy_head': git('rev-parse', 'HEAD', cwd=copy).strip(),
              'copy_tree': git('rev-parse', 'HEAD^{tree}', cwd=copy).strip(),
              'started_utc': now_utc(), 'steps': []}
    for name, command in plan:
        result = run_logged(command, copy, env, out / f'{args.label}-{name}.log')
        result['step'] = name
        result['tracked_changes_after'] = git('status', '--porcelain=v1', '--untracked-files=no',
                                              cwd=copy).splitlines()
        if name == 'sync':
            result['interpreter'] = subprocess.run(
                ['uv', 'run', 'python', '-c', 'import sys; print(sys.version)'],
                cwd=copy, env=env, capture_output=True, text=True).stdout.strip()
        record['steps'].append(result)
        print(json.dumps({k: v for k, v in result.items() if k != 'command'})[:1500], flush=True)
        if result['exit_code']:
            break
    record['green'] = len(record['steps']) == len(plan) and all(s['exit_code'] == 0 for s in record['steps'])
    record['finished_utc'] = now_utc()
    (out / f'{args.label}.json').write_text(json.dumps(record, indent=1) + '\n')
    print(json.dumps({'label': args.label, 'green': record['green']}))
    return 0 if record['green'] else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('copy')
    c.add_argument('--candidate', required=True)
    c.add_argument('--main', default='main')
    c.add_argument('--out', type=Path, required=True)
    c.add_argument('--keep-worktree', action='store_true')
    b = sub.add_parser('burners')
    b.add_argument('action', choices=('start', 'stop'))
    b.add_argument('--record', type=Path, required=True)
    b.add_argument('--count', type=int, default=4, help="the brief's emulation is four; three is a lighter bracket")
    for name in ('stress', 'pytest', 'ci'):
        p = sub.add_parser(name)
        p.add_argument('--copy', type=Path, required=True)
        p.add_argument('--env', type=Path, required=True, help='a fresh UV_PROJECT_ENVIRONMENT')
        p.add_argument('--python', default='3.12')
        p.add_argument('--out', type=Path, required=True)
        p.add_argument('--label', required=True)
        if name in ('stress', 'pytest'):
            p.add_argument('--emulation', choices=('quiet', 'four-burners', 'three-burners'), required=True,
                           help='recorded only; start the burners separately with `burners start`')
        if name == 'stress':
            p.add_argument('--node', default=RICH_ADMIN)
            p.add_argument('--runs', type=int, default=5)
        if name == 'pytest':
            p.add_argument('select', nargs='+')
    args = ap.parse_args()
    return {'copy': cmd_copy, 'burners': cmd_burners, 'stress': cmd_stress,
            'pytest': cmd_pytest, 'ci': cmd_ci}[args.cmd](args)


if __name__ == '__main__':
    sys.exit(main())
