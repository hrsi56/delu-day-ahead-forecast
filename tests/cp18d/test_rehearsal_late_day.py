"""The rehearsal's missed acquisition, end to end through the live-input builder (CP-18d, the brief's items 1 and 5):
on development days, a dry run whose day D had no acquisition before its cutoff retrieves D's load forecast at the run's
clock, after the cutoff, from the rehearsal's stand-in (`cp18.rehearsal`), and issues D with that copy, labelled, while
the day before it, all of whose inputs were shown (ruling 1's development exception), is labelled "all inputs before
the cutoff". The store, the Space's live record and the bundle's forecasts all name the class.

The real path: `cp18.live_inputs.LiveInputs` → `cp18.live.build.build_day` → `cp18.live.history.assemble` →
`cp18.pipeline.run` → `cp18.store.LiveStore`. The frozen issuance is CP-18c's stand-in (no Pyodide here; the scratch
rehearsal runs the frozen chain on the runner). A bare `origin` whose checkout reaches the committed development data
by symlinks; the search state is the committed dry-run pin. Development days only; nothing touches the network.
"""
from __future__ import annotations

from datetime import date, datetime
import json
import os
from pathlib import Path
import subprocess

import pytest

from cp17.shadow import ShadowStates
from cp18 import inputclass, pipeline
from cp18.claim import Claim
from cp18.live_claims import live_record
from cp18.live_inputs import LiveInputs
from cp18.rehearsal import StandInLoadForecast, published_before
from cp18.store import STORE_PATH, LiveStore

from cp18c.support18c import IDENTITY, passing_checks, stand_in_issue

ROOT = Path(__file__).resolve().parents[2]
RECORDED = ROOT / 'reports/cp18a/dryrun/recorded'
STATE = ROOT / 'reports/cp18a/dryrun/states/start-2026-08-31.json'
PINNED = ROOT / 'reports/cp18a/dryrun/pinned/local'
NOW = datetime.fromisoformat('2026-08-31T12:00:00+02:00')            # target day 2026-09-01; first day 2026-08-31
LATE = date(2026, 9, 1)

pytestmark = pytest.mark.skipif(not (ROOT / 'data/snapshot.parquet').exists() or not PINNED.exists(),
                                reason='the committed development data or the dry-run pins are absent')


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], check=True, capture_output=True, text=True,
                          env={**os.environ, **IDENTITY}).stdout.strip()


def checkout(tmp_path) -> Path:
    bare, seed = tmp_path / 'origin.git', tmp_path / 'seed'
    subprocess.run(['git', 'init', '--quiet', '--bare', '-b', 'main', str(bare)], check=True)
    subprocess.run(['git', 'init', '--quiet', '-b', 'main', str(seed)], check=True)
    for name in ('pre-commit', 'commit-msg', 'pre-push'):
        hook = seed / '.githooks' / name
        hook.parent.mkdir(exist_ok=True)
        hook.write_text('#!/bin/sh\nexit 0\n')
        hook.chmod(0o755)
    for name in ('data', 'reports', 'docs', 'models'):              # the committed development data, read only
        (seed / name).symlink_to(ROOT / name)
    LiveStore.init(seed / STORE_PATH, ShadowStates.from_dict(json.loads(STATE.read_text())), date(2026, 8, 31),
                   'the dry run\'s development state', date(2026, 8, 31))
    for args in (['add', '-A'], ['commit', '--quiet', '-m', 'seed'], ['push', '--quiet', str(bare), 'HEAD:refs/heads/main']):
        git(seed, *args)
    repo = tmp_path / 'runner'
    subprocess.run(['git', 'clone', '--quiet', str(bare), str(repo)], check=True)
    git(repo, 'config', 'core.hooksPath', '.githooks')
    return repo


def test_a_missed_acquisition_on_a_development_day_is_issued_with_the_copy_fetched_after_the_cutoff(tmp_path):
    repo = checkout(tmp_path)
    project = tmp_path / 'project'
    project.mkdir()
    (project / '.local').symlink_to(PINNED)
    stand_in = StandInLoadForecast(ROOT, lambda: NOW, published_before(LATE, 50))
    inputs = LiveInputs(repo, project, RECORDED, late_days=[LATE], late_transport=stand_in)
    settings = pipeline.Settings(root=repo, project=project, out=tmp_path / 'out', host_kind='runner', mode='dry-run',
                                 run_label='rehearsal-late')
    record = pipeline.run(settings, NOW, claim=Claim(repo, env=IDENTITY), inputs=inputs, checks=passing_checks(),
                          issue=stand_in_issue(), serving=lambda d: 13)
    assert record['planned'] == ['2026-08-31', '2026-09-01'] and record['exit'] == 0, record['outcome']
    before, after = record['days']['2026-08-31'], record['days']['2026-09-01']
    assert before['status'] == 'issued' and before['input_class'] == inputclass.BEFORE
    assert after['status'] == 'issued' and after['input_class'] == inputclass.AFTER
    assert after['input_class_text'] == 'load forecast fetched after the cutoff'
    assert after['load_forecast_fetched_utc'] == '2026-08-31T10:00:00Z'               # the run's clock, after 09:00
    # the evidence: D's load forecast was not admitted against its cutoff; the copy used is the stand-in's
    rec = json.loads((repo / STORE_PATH / 'issued/2026-09-01/record.json').read_text())
    lf = inputclass.required_load_forecast(rec)
    assert not lf['admitted'] and lf['fetched_after_cutoff'] and lf['cutoff_utc'] == '2026-08-31T09:00:00Z'
    assert lf['provenance'] == 'live' and stand_in.sent and stand_in.sent[-1]['published']
    archived = json.loads((repo / 'live/inputs/days/2026-09-01/manifest.json').read_text())['records']
    assert [r['origin'] for r in archived if r['input'] == 'load_forecast'] == [stand_in.origin]   # names the stand-in
    store = LiveStore(repo / STORE_PATH)
    store.verify()
    assert {d: v['input_class'] for d, v in store.days().items()} == {'2026-08-31': inputclass.BEFORE,
                                                                       '2026-09-01': inputclass.AFTER}
    shown = {i['day']: i for i in live_record(repo / 'live')['issued']}
    assert shown['2026-09-01']['load_forecast_fetched_utc'] == '2026-08-31T10:00:00+00:00'
    # published through the claim to the origin, with the late copy's archive
    assert git(tmp_path / 'origin.git', 'log', '--format=%s', 'main').splitlines()[:2] == [
        'live: run rehearsal-late (done)', 'live: 2026-09-01 issued (stand-in issuance)']
