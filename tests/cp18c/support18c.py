"""Shared helpers for CP-18c's tests: a bare `origin` with a store, stand-in inputs and issuance (after CP-18a's)."""
from __future__ import annotations

from datetime import date, datetime, timedelta
import os
from pathlib import Path
import subprocess

import numpy as np

from cp17 import issue as cp17issue
from cp17.dailyfit import array_hash
from cp17.shadow import ShadowStates
from cp18 import pipeline
from cp18.claim import Claim
from cp18.store import STORE_PATH, LiveStore
from cp25 import guard

BERLIN = guard.BERLIN
IDENTITY = {'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@t', 'GIT_COMMITTER_NAME': 't', 'GIT_COMMITTER_EMAIL': 't@t'}
REPO = Path(__file__).resolve().parents[2]
FREEZE_STATE = REPO / 'live/pinned/local/artifacts/cp-17c/state/freeze-origin-state.json'


def at_noon(day: date) -> datetime:
    """Noon in Berlin on `day`: the target day is the day after."""
    return datetime(day.year, day.month, day.day, 12, 0, tzinfo=BERLIN)


def synthetic_state(origin: date) -> ShadowStates:
    rng = np.random.default_rng(7)
    days = [origin - timedelta(days=2 + i) for i in range(28)][::-1]
    buffers = {p: [{'day': str(d), 'errors': rng.normal(size=24).round(6).tolist()} for d in days]
               for p in ('v4', 'v2', 'B0')}
    return ShadowStates.from_buffers(origin, buffers)


def git(repo: Path, *args: str) -> str:
    # The identity is explicit: a GitHub-hosted runner has no global Git identity (CP-18a's landing).
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, check=True,
                          env={**os.environ, **IDENTITY}).stdout.strip()


def make_origin(tmp_path: Path, state: ShadowStates, origin: date, first_day: date, carry_to: date | None = None):
    """A bare `origin` whose main holds a store (genesis at `origin`, first day `first_day`, optionally carried to
    `carry_to`), and a function giving a fresh checkout of it with its own pass-through hooks."""
    bare = tmp_path / 'origin.git'
    subprocess.run(['git', 'init', '--quiet', '--bare', '-b', 'main', str(bare)], check=True)
    seed = tmp_path / 'seed'
    subprocess.run(['git', 'init', '--quiet', '-b', 'main', str(seed)], check=True)
    hooks = seed / '.githooks'
    hooks.mkdir()
    for name in ('pre-commit', 'commit-msg', 'pre-push'):
        (hooks / name).write_text('#!/bin/sh\nexit 0\n')
        (hooks / name).chmod(0o755)
    store = LiveStore.init(seed / STORE_PATH, state, origin, 'test state', first_day)
    if carry_to is not None:
        store.record_carry(origin, carry_to, 'test carry (decision 28)')
    for args in (['add', '-A'], ['commit', '--quiet', '-m', 'seed'], ['push', '--quiet', str(bare), 'HEAD:refs/heads/main']):
        subprocess.run(['git', '-C', str(seed), *args], check=True, env={**os.environ, **IDENTITY})

    def checkout(name: str) -> Path:
        path = tmp_path / name
        subprocess.run(['git', 'clone', '--quiet', str(bare), str(path)], check=True)
        git(path, 'config', 'core.hooksPath', '.githooks')
        return path
    return checkout


class Inputs:
    """Shown inputs, except the days named in `hidden`; `raising` days raise in `build`, `truth_raising` in `truth`."""

    def __init__(self, hidden=(), raising=(), truth_raising=()):
        self.hidden = {str(d) for d in hidden}
        self.raising = {str(d) for d in raising}
        self.truth_raising = {str(d) for d in truth_raising}
        self.built = []

    def truth(self, day):
        if str(day) in self.truth_raising:
            raise ConnectionError('SMARD unreachable (stand-in)')
        return lambda keys: np.full(len(keys), np.nan)

    def search_file(self, k):
        return Path(__file__)

    def build(self, day, *, buffers, search_file, out):
        self.built.append(str(day))
        if str(day) in self.raising:
            raise TimeoutError('the ENTSO-E request timed out (stand-in)')
        shown = str(day) not in self.hidden
        return {'payloads': str(out), 'gfs_available': True, 'shown': shown,
                'reasons': [] if shown else ['the load forecast was retrieved after the cutoff'],
                'data_refresh_utc': '', 'availability': []}


def stand_in_issue():
    """`cp17.issue`'s own artifact around a fixed B0 forecast."""
    def issue(day, gfs_available, payloads, *, settings, parent_sha256, data_refresh_utc, states):
        keys = cp17issue.canonical_hours(day)
        q = np.sort(np.linspace(-1, 1, 7)[None, :] + np.arange(len(keys))[:, None], axis=1)
        result = {'policy': 'B0', 'index': keys, 'quantiles': q.tolist(), 'quantiles_sha256': array_hash(q),
                  'source_day': str(day - timedelta(days=1))}
        attempts = [{'policy': 'B0', 'status': 'ok', 'result': result,
                     'resources': {'wall_seconds': 1.0, 'peak_bytes': 1}}]
        decision = {'day': str(day), 'issued_policy': 'B0', 'route': 'a1_failed', 'attempts': attempts,
                    'display': 'stand-in issuance'}
        art = cp17issue.artifact(decision, identity={'policy_identity_sha256': '0' * 64, 'package_sha256': '0' * 64},
                                 payloads={}, parent_sha256=parent_sha256, data_refresh_utc=data_refresh_utc,
                                 host={'runtime': 'stand-in'})
        decision['artifact'] = art
        return {'artifact': art, 'decision': decision, 'shadows': {}, 'process_seconds': {}, 'process_seconds_sum': 0.0,
                'total_seconds': 0.0, 'blocked_non_local_requests': []}
    return issue


def passing_checks():
    ok = {'passed': True, 'problems': []}
    return {name: (lambda name=name: {'check': name, **ok}) for name in ('pins', 'binary', 'machine', 'canary')}


def run(repo, tmp_path, now, inputs=None, label=None, mode='dry-run'):
    settings = pipeline.Settings(root=repo, project=repo, out=tmp_path / 'out' / (label or 'r'), host_kind='local',
                                 mode=mode, run_label=label or '')
    return pipeline.run(settings, now, claim=Claim(repo), inputs=inputs or Inputs(), checks=passing_checks(),
                        issue=stand_in_issue(), serving=lambda d: 13)
