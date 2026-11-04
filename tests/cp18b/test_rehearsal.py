"""The delivery rehearsal: two runs in one data-only folder, as the daily pipeline will run them.

Run 1 at 2026-09-04 12:00 Europe/Berlin, before 2026-09-05's prices are published (13:00): that day is pending. Run 2
at 2026-09-05 10:00 reconciles it. The committed records (`reports/cp18b/rehearsal/`) are what the two runs write to
the data-only paths on `main` (`live/outcomes/`, `live/evaluation/`, `live/bundles/`); they are rebuilt here byte for
byte, and run 2's bundle is the committed bundle.
"""
from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path

from cp18 import bundle as B, evaluation as EV
from cp18.records import RecordLog
from cp18b.support18b import issuing_platform, BUNDLE, ROOT, build

REHEARSAL = ROOT / 'reports/cp18b/rehearsal'
RUNS = (('run-1', '2026-09-04T12:00:00+02:00'), ('run-2', '2026-09-05T10:00:00+02:00'))


def tree(folder: Path) -> dict[str, bytes]:
    return {str(p.relative_to(folder)): p.read_bytes() for p in sorted(folder.rglob('*')) if p.is_file()}


@issuing_platform
def test_the_rehearsal_reproduces_its_committed_records(live, tmp_path):
    for run, now in RUNS:
        value = build(live, tmp_path / run, now=datetime.fromisoformat(now), run_id=f'dry-run-{run}')
        verdict = B.gate(B.read(tmp_path / run), ROOT)
        assert verdict['publishable']
        EV.commit_daily(live, datetime.fromisoformat(now).date(), value['daily_windows'],
                        value['static_development_sha256'], f'dry-run-{run}')
        B.record(live, value, verdict)
    for name in ('outcomes', 'evaluation', 'bundles'):
        assert tree(live / name) == tree(REHEARSAL / name), name
    assert B.read(tmp_path / 'run-2') == B.read(BUNDLE)


def test_a_later_run_reconciles_the_day_published_since():
    log = RecordLog(REHEARSAL / 'outcomes')
    entries = log.verify()
    assert [e['days'] for e in entries] == [['2026-08-31', '2026-09-01', '2026-09-02', '2026-09-03'], ['2026-09-05']]
    assert log.read(entries[0])['pending'] == ['2026-09-05'] and log.read(entries[1])['pending'] == []
    for name in ('evaluation', 'bundles'):
        assert [e['as_of_day'] for e in RecordLog(REHEARSAL / name).verify()] == ['2026-09-04', '2026-09-05']
    bundles = [RecordLog(REHEARSAL / 'bundles').read(e) for e in RecordLog(REHEARSAL / 'bundles').verify()]
    assert all(b['publishable'] and b['recompute_match'] for b in bundles)
    first = json.loads((REHEARSAL / 'evaluation/2026-09-04.json').read_text())
    day = next(w for w in first['windows'] if w['policy'] == 'product' and w['window'] == 'development')
    pending = next(d for d in day['record']['days'] if d['day'] == '2026-09-05')
    assert not pending['scored'] and pending['scored_hours'] == 0
