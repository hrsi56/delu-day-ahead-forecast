"""Negative control (CP-18d, the brief's item 6): decision 31 covers D's own load forecast only. Through the real
history and build (`cp18.live.build.build_day`) on development days, with the dry run's recorded responses:

- a price that cannot be shown to precede D's cutoff leaves D not shown (decision 22's consequence, the INPUTS cause),
  even when D's load forecast is the copy fetched after the cutoff: no copy after the cutoff stands in for a price;
- a GFS run not shown before the cutoff only sets the frozen chain's GFS flag to False (its own fallback, unchanged), and
  the day's class is still named by its load forecast alone.

The availability judgement (`cp18.live.availability.judge`) is the single admission point; the test makes it refuse
one input, as a publication after the cutoff would. Development days only; nothing touches the network.
"""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

import pytest

from cp18 import inputclass
from cp18.live import availability as A
from cp18.live_inputs import LiveInputs
from cp18.rehearsal import StandInLoadForecast, published_before

ROOT = Path(__file__).resolve().parents[2]
RECORDED = ROOT / 'reports/cp18a/dryrun/recorded'
PINNED = ROOT / 'reports/cp18a/dryrun/pinned/local'
DAY = date(2026, 9, 1)
NOW = datetime.fromisoformat('2026-08-31T12:00:00+02:00')

pytestmark = pytest.mark.skipif(not (ROOT / 'data/snapshot.parquet').exists() or not PINNED.exists(),
                                reason='the committed development data or the dry-run pins are absent')


def build(tmp_path, late: bool, refuse=None, monkeypatch=None):
    for name in ('data', 'reports', 'docs', 'models'):
        if not (tmp_path / 'root' / name).exists():
            (tmp_path / 'root').mkdir(exist_ok=True)
            (tmp_path / 'root' / name).symlink_to(ROOT / name)
    project = tmp_path / 'project'
    if not project.exists():
        project.mkdir()
        (project / '.local').symlink_to(PINNED)
    if refuse is not None:
        real = A.judge

        def judge(input_name, for_day, data_day, publication, record, archive_day=None):
            out = real(input_name, for_day, data_day, publication, record, archive_day=archive_day)
            if refuse(input_name, for_day, data_day):
                out = dict(out, admitted=False, by_exception=False,
                           reason=f'published after the cutoff {out.get("cutoff_utc")} (the control)')
            return out
        monkeypatch.setattr(A, 'judge', judge)
    stand_in = StandInLoadForecast(ROOT, lambda: NOW, published_before(DAY, 50))
    inputs = LiveInputs(tmp_path / 'root', project, RECORDED, late_days=[DAY] if late else [], late_transport=stand_in)
    from cp17.shadow import ShadowStates
    import json
    state = ShadowStates.from_dict(json.loads((ROOT / 'reports/cp18a/dryrun/states/start-2026-08-31.json').read_text()))
    state.release(DAY, inputs.truth(DAY))
    return inputs.build(DAY, buffers={p: state.buffer(p) for p in ('v4', 'v2', 'B0')},
                        search_file=inputs.search_file(13), out=tmp_path / 'payloads')


def test_a_price_after_the_cutoff_is_never_rescued_by_the_load_forecasts_copy(tmp_path, monkeypatch):
    built = build(tmp_path, late=True, monkeypatch=monkeypatch,
                  refuse=lambda name, for_day, data_day: name == 'price' and data_day == date(2026, 8, 31))
    assert not built['shown'] and built['build_status'] == 'not_shown'
    assert any(r.startswith('price of 2026-08-31') for r in built['availability']['reasons'])
    assert 'input_class' not in built or built.get('input_class') is None          # nothing built, nothing labelled


def test_a_gfs_run_after_the_cutoff_only_clears_the_frozen_flag_and_names_no_class_of_its_own(tmp_path, monkeypatch):
    built = build(tmp_path, late=False, monkeypatch=monkeypatch,
                  refuse=lambda name, for_day, data_day: name == 'gfs' and data_day == DAY)
    assert built['shown'] and built['gfs_available'] is False                      # the chain's own GFS fallback
    assert built['input_class'] == inputclass.BEFORE and built['load_forecast_fetched_utc'] is None


def test_the_load_forecasts_copy_after_the_cutoff_alone_is_labelled(tmp_path):
    built = build(tmp_path, late=True)
    assert built['shown'] and built['input_class'] == inputclass.AFTER
    assert built['load_forecast_fetched_utc'] == '2026-08-31T10:00:00Z' and built['gfs_available'] is True
