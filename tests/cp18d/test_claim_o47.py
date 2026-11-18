"""The claim over a moved `main` (the Orchestrator's O47, CP-18d; `cp18.claim.Claim.publish`).

O47's case, reproduced: a run's records step commits its records; before it pushes, another writer pushes a commit
that touches none of the run's files (on the first runner day, PRES-6's documentation commit). The records are
re-applied on the new `main` and pushed, as a fast-forward, with the other writer's commit kept. And its negative
control: a moved `main` that touches one of the run's own files still refuses, as before (the other writer's record
stands). Local bare repositories only; nothing touches GitHub.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

import pytest

from cp18 import local
from cp18.claim import REAPPLY_ATTEMPTS, Claim, ClaimError

IDENTITY = {'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@t', 'GIT_COMMITTER_NAME': 't', 'GIT_COMMITTER_EMAIL': 't@t'}


def git(repo: Path, *args: str) -> str:
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, check=True,
                          env={**os.environ, **IDENTITY}).stdout.strip()


@pytest.fixture
def origin(tmp_path):
    """A bare `origin` whose main holds pass-through hooks, a document and a live record; and a clone maker."""
    bare = tmp_path / 'origin.git'
    subprocess.run(['git', 'init', '--quiet', '--bare', '-b', 'main', str(bare)], check=True)
    seed = tmp_path / 'seed'
    subprocess.run(['git', 'init', '--quiet', '-b', 'main', str(seed)], check=True)
    for name in ('pre-commit', 'commit-msg', 'pre-push'):
        hook = seed / '.githooks' / name
        hook.parent.mkdir(exist_ok=True)
        hook.write_text('#!/bin/sh\nexit 0\n')
        hook.chmod(0o755)
    (seed / 'docs').mkdir()
    (seed / 'docs/progress.md').write_text('progress\n')
    (seed / 'live/store').mkdir(parents=True)
    (seed / 'live/store/ledger.jsonl').write_text('{"kind": "genesis"}\n')
    for args in (['add', '-A'], ['commit', '--quiet', '-m', 'seed'], ['push', '--quiet', str(bare), 'HEAD:refs/heads/main']):
        git(seed, *args)

    def clone(name: str) -> Path:
        path = tmp_path / name
        subprocess.run(['git', 'clone', '--quiet', str(bare), str(path)], check=True)
        git(path, 'config', 'core.hooksPath', '.githooks')
        return path
    return bare, clone


def push_from(clone: Path, path: str, text: str, message: str) -> str:
    target = clone / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    git(clone, 'add', path)
    git(clone, 'commit', '--quiet', '-m', message)
    git(clone, 'push', '--quiet', 'origin', 'HEAD:refs/heads/main')
    return git(clone, 'rev-parse', 'HEAD')


def records_of_a_run(run: Path) -> list[str]:
    (run / 'live/outcomes').mkdir(parents=True)
    (run / 'live/outcomes/2026-11-15.json').write_text('{"day": "2026-11-15"}\n')
    (run / 'live/evaluation').mkdir(parents=True)
    (run / 'live/evaluation/2026-11-15.json').write_text('{"windows": []}\n')
    return ['live/outcomes', 'live/evaluation']


def test_o47_an_unrelated_commit_during_the_records_step_keeps_the_records(origin):
    bare, clone = origin
    run, other = clone('run'), clone('other')
    claim = Claim(run, env=IDENTITY)
    base = claim.sync()
    paths = records_of_a_run(run)
    moved = []
    result = claim.publish(paths, 'live: the records of run r1',
                           before_push=lambda: moved.append(push_from(other, 'docs/progress.md', 'issued\n', 'docs')))
    tip = git(bare, 'rev-parse', 'main')
    assert result['pushed'] == tip and result['reapplied'] and result['original'] != tip
    assert result['reapplied'][0]['over'] == moved[0] and result['reapplied'][0]['touched'] == ['docs/progress.md']
    # the other writer's commit is kept, unchanged, and the records sit on it as a fast-forward
    assert git(bare, 'rev-parse', 'main^') == moved[0] and git(bare, 'merge-base', '--is-ancestor', base, moved[0]) == ''
    assert git(bare, 'show', 'main:docs/progress.md') == 'issued'
    assert sorted(git(bare, 'diff', '--name-only', 'main^', 'main').split()) == [
        'live/evaluation/2026-11-15.json', 'live/outcomes/2026-11-15.json']
    assert git(bare, 'show', 'main:live/outcomes/2026-11-15.json') == '{"day": "2026-11-15"}'
    assert git(bare, 'log', '-1', '--format=%s', 'main') == 'live: the records of run r1'
    assert git(run, 'rev-parse', 'HEAD') == tip and not git(run, 'status', '--porcelain')


def test_o47_negative_control_a_moved_main_touching_the_runs_own_files_still_refuses(origin):
    bare, clone = origin
    run, other = clone('run'), clone('other')
    claim = Claim(run, env=IDENTITY)
    claim.sync()
    (run / 'live/store/ledger.jsonl').write_text('{"kind": "genesis"}\n{"kind": "issuance", "day": "2026-11-16"}\n')
    theirs = []
    result = claim.publish(['live/store'], 'live: 2026-11-16 issued', before_push=lambda: theirs.append(
        push_from(other, 'live/store/ledger.jsonl', '{"kind": "genesis"}\n{"kind": "issuance", "x": 1}\n', 'theirs')))
    assert result['lost'] and result['theirs'] == theirs[0] and result['overlap'] == ['live/store/ledger.jsonl']
    assert git(bare, 'rev-parse', 'main') == theirs[0]                       # the other host's record stands
    assert git(run, 'rev-parse', 'HEAD') == theirs[0]                        # this commit is dropped
    assert 'x' in (run / 'live/store/ledger.jsonl').read_text()


def test_o47_negative_control_a_file_touched_then_restored_still_counts(origin):
    # every commit's touched files count, not only main's net difference
    bare, clone = origin
    run, other = clone('run'), clone('other')
    claim = Claim(run, env=IDENTITY)
    claim.sync()
    paths = records_of_a_run(run)

    def touch_and_restore():
        push_from(other, 'live/outcomes/2026-11-15.json', 'theirs\n', 'theirs')
        git(other, 'rm', '--quiet', 'live/outcomes/2026-11-15.json')
        git(other, 'commit', '--quiet', '-m', 'restored')
        git(other, 'push', '--quiet', 'origin', 'HEAD:refs/heads/main')
    result = claim.publish(paths, 'live: the records', before_push=touch_and_restore)
    assert result['lost'] and result['overlap'] == ['live/outcomes/2026-11-15.json']


def test_a_commit_outside_live_is_never_reapplied(origin):
    bare, clone = origin
    run, other = clone('run'), clone('other')
    claim = Claim(run, env=IDENTITY)
    claim.sync()
    (run / 'notes.md').write_text('not a live record\n')
    result = claim.publish(['notes.md'], 'a note',
                           before_push=lambda: push_from(other, 'docs/progress.md', 'x\n', 'docs'))
    assert result['lost'] and result['outside'] == ['notes.md'] and 'outside live/' in result['why']
    assert 'notes.md' not in git(bare, 'ls-tree', '--name-only', 'main').split()


def test_it_never_force_pushes_and_stops_after_its_bounded_reapplications(origin, monkeypatch):
    bare, clone = origin
    run, other = clone('run'), clone('other')
    claim = Claim(run, env=IDENTITY)
    claim.sync()
    paths = records_of_a_run(run)
    pushes = []
    real = Claim.git

    def git_spy(self, *args, check=True):
        if args and args[0] == 'push':
            assert not any(a.startswith(('-f', '--force', '+')) for a in args[1:]), args
            pushes.append(args)
            push_from(other, 'docs/progress.md', f'moved {len(pushes)}\n', f'docs {len(pushes)}')   # main always moves
        return real(self, *args, check=check)
    monkeypatch.setattr(Claim, 'git', git_spy)
    result = claim.publish(paths, 'live: the records')
    assert result['lost'] and 'kept moving' in result['why'] and len(result['reapplied']) == REAPPLY_ATTEMPTS
    assert len(pushes) == REAPPLY_ATTEMPTS + 1
    assert 'live/outcomes/2026-11-15.json' not in git(bare, 'ls-tree', '-r', '--name-only', 'main').split()


def test_the_records_step_reports_the_reapplication_and_the_rehearsal_moves_a_local_bare_main(origin):
    bare, clone = origin
    run = clone('run')
    Claim(run, env=IDENTITY).sync()
    records_of_a_run(run)
    value = local.records(run, remote='origin', run_id='r1', rehearse_moved_main=True)
    assert value['exit'] == 0 and value['result']['reapplied'] and 're-applied over a moved main' in value['outcome']
    assert git(bare, 'show', f'main^:{local.MOVED_MAIN_PATH}').startswith('Another writer moved main')
    assert git(bare, 'log', '-1', '--format=%s', 'main').startswith('live: the records of run r1')


def test_the_moved_main_rehearsal_refuses_a_remote_that_is_not_a_local_bare_repository(origin):
    _, clone = origin
    run = clone('run')
    git(run, 'remote', 'add', 'product', 'https://github.com/hrsi56/delu-day-ahead-forecast.git')
    with pytest.raises(ClaimError, match='local bare repository'):
        local.moved_main_rehearsal(run, 'product')
    value = local.records(run, remote='product', run_id='r1', rehearse_moved_main=True)
    assert value['exit'] == 2 and 'local bare repository' in value['outcome']
