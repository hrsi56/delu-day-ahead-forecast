"""One real dry run on a development day, through the H2 gate, then the local fallback under the same claim rule.

Real everything: the official binary and the pinned Pyodide folder, the frozen package zip, `cp17.hostcheck`'s four
checks, `cp17.daily.issue_day` with its shadows, the store and the claim through the repository's own `.githooks`.
The store starts from CP-17b's host state before 2026-08-31's release (`reports/cp18a/dryrun/states/`), and the run's
wall clock is simulated at 2026-08-30 12:00 Berlin, so its plan is 2026-08-31 alone. The issued A1 must be bit-identical
to CP-17c's record of that day. The fallback, run at the same wall clock in its own clone, finds the day claimed and
issues nothing. Marked `stress` (local, about five minutes), and skipped where the local runtime is absent.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

from cp17 import runtime

ROOT = Path(__file__).resolve().parents[2]
PROJECT = Path(os.environ.get('CP17_PROJECT_ROOT') or runtime.project_root())
STATE = ROOT / 'reports/cp18a/dryrun/states/start-2026-08-31.json'
PAYLOADS = PROJECT / '.local/artifacts/cp-17b/runs/shadow-host/payloads'
#: CP-17c's A1 at 2026-08-31 (its shadow-late store; CP-17b's host run): the issued quantiles' SHA-256.
A1_2026_08_31 = '75d86a3b3cb9f670'
LOCAL = (PROJECT / runtime.NODE_RELATIVE, PROJECT / runtime.PYODIDE_DIR / 'pyodide.asm.wasm',
         PROJECT / '.local/artifacts/cp-17c/bundle/src.zip', PROJECT / runtime.K13, PAYLOADS / 'A1-2026-08-31.npz')

pytestmark = [pytest.mark.stress,
              pytest.mark.skipif(not all(p.exists() for p in LOCAL), reason='the local runtime, states or payloads are absent')]


def sh(*args, cwd=None, env=None):
    return subprocess.run(list(args), cwd=cwd, env=env, capture_output=True, text=True)


def test_a_real_dry_run_then_the_fallback_finds_the_day_claimed(tmp_path):
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src'), 'CP17_PROJECT_ROOT': str(PROJECT),
           **{n: '1' for n in ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS',
                               'NUMEXPR_NUM_THREADS')}, 'MLFLOW_DISABLE_TELEMETRY': 'true', 'DO_NOT_TRACK': '1',
           'GIT_AUTHOR_NAME': 'delu-daily', 'GIT_AUTHOR_EMAIL': 'd@d', 'GIT_COMMITTER_NAME': 'delu-daily',
           'GIT_COMMITTER_EMAIL': 'd@d'}
    bare, seed = tmp_path / 'origin.git', tmp_path / 'seed'
    assert sh('git', 'init', '--quiet', '--bare', '-b', 'main', str(bare)).returncode == 0
    assert sh('git', 'clone', '--quiet', '--no-local', str(ROOT), str(seed)).returncode == 0
    head = sh('git', '-C', str(ROOT), 'rev-parse', 'HEAD').stdout.strip()
    sh('git', '-C', str(seed), 'checkout', '--quiet', '--detach', head)
    sh('git', '-C', str(seed), 'config', 'core.hooksPath', '.githooks')
    seeded = sh(sys.executable, '-m', 'cp18', 'seed-store', '--root', str(seed), '--genesis', f'{STATE}:2026-08-31',
                env=env)
    assert seeded.returncode == 0, seeded.stderr
    for args in (('add', 'live/store'), ('commit', '--quiet', '-m', 'the store at its start'),
                 ('push', '--quiet', str(bare), 'HEAD:refs/heads/main')):
        done = sh('git', '-C', str(seed), *args, env=env)
        assert done.returncode == 0, done.stderr
    runner = tmp_path / 'runner'
    sh('git', 'clone', '--quiet', str(bare), str(runner))
    sh('git', '-C', str(runner), 'config', 'core.hooksPath', '.githooks')
    now = '2026-08-30T12:00:00+02:00'
    done = sh(sys.executable, '-m', 'cp18', 'run', '--root', str(runner), '--project', str(PROJECT), '--out',
              str(tmp_path / 'out-runner'), '--host', 'runner', '--now', now, '--inputs', f'prebuilt:{PAYLOADS}',
              '--run-label', 'pytest-runner', env=env)
    assert done.returncode == 0, done.stdout + done.stderr
    record = json.loads((tmp_path / 'out-runner/run.json').read_text())
    assert record['gate']['passed'] and [c['check'] for c in record['gate']['checks']] == ['pins', 'binary', 'machine', 'canary']
    assert record['planned'] == ['2026-08-31'] and record['days']['2026-08-31']['status'] == 'issued'
    artifact = json.loads((runner / 'live/store/issued/2026-08-31/artifact.json').read_text())
    assert artifact['issued_policy'] == 'A1' and artifact['quantiles_sha256'].startswith(A1_2026_08_31)
    # the local fallback: its own clone, created from the origin, the same wall clock: the day is already claimed
    fallback = sh(sys.executable, '-m', 'cp18.local', 'run', '--clone', str(tmp_path / 'fallback'), '--url', str(bare),
                  '--project', str(PROJECT), '--out', str(tmp_path / 'out-local'), '--now', now,
                  '--inputs', f'prebuilt:{PAYLOADS}', '--run-label', 'pytest-local', env=env)
    assert fallback.returncode == 0, fallback.stdout + fallback.stderr
    local = json.loads((tmp_path / 'out-local/run.json').read_text())
    assert local['host_kind'] == 'local' and local['planned'] == [] and local['outcome'] == 'nothing to issue'
    prepared = json.loads((tmp_path / 'out-local/local-prepare.json').read_text())
    assert prepared['package']['equal_to_manifest'] and prepared['node'].get('in_place')
    log = sh('git', '-C', str(bare), 'log', '--format=%s', 'main').stdout.splitlines()
    assert log[:3] == ['live: run pytest-local (nothing to issue)', 'live: run pytest-runner (done)',
                       'live: 2026-08-31 issued (successful daily fit)']
