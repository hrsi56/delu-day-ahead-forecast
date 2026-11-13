"""The open days (the Integration review's FAIL on the first candidate): days a run attempted and could not issue, still
inside the lookback after the last issued day, are shown as not issued with their cause — in the live record the Space
reads and in the bundle's not-issued list — and close with that cause once a later day is issued."""
from __future__ import annotations

from datetime import date, datetime, timezone

from cp18 import boundary, bundle as B, causes
from cp18.live_claims import OPEN_DAY_WORDING, live_record
from cp18.store import STORE_PATH, LiveStore

from cp18c.support18c import Inputs, at_noon, make_origin, run, synthetic_state

ORIGIN, FIRST = date(2026, 9, 6), date(2026, 9, 7)


def test_days_left_open_after_the_last_issued_day_are_named_with_their_cause(tmp_path):
    checkout = make_origin(tmp_path, synthetic_state(ORIGIN), ORIGIN, FIRST, carry_to=date(2026, 11, 3))
    repo = checkout('a')
    with boundary.live(now=at_noon(date(2026, 11, 5))):
        run(repo, tmp_path, at_noon(date(2026, 11, 5)), Inputs(hidden=['2026-11-03', '2026-11-04', '2026-11-05']),
            mode='live', label='r1')
    # a later run after a gap: every planned day is attempted and none can be shown
    with boundary.live(now=at_noon(date(2026, 11, 12))):
        record = run(repo, tmp_path, at_noon(date(2026, 11, 12)),
                     Inputs(hidden=['2026-11-10', '2026-11-11', '2026-11-12', '2026-11-13']), mode='live', label='r2')
    assert record['planned'] == ['2026-11-10', '2026-11-11', '2026-11-12', '2026-11-13']
    store = LiveStore(repo / STORE_PATH)
    assert store.days()['2026-11-09']['cause'] == causes.NO_RUN
    live = live_record(repo / 'live')
    opened = {d['day']: d for d in live['open']}
    assert sorted(opened) == ['2026-11-10', '2026-11-11', '2026-11-12', '2026-11-13']
    assert all(d['cause'] == causes.INPUTS and d['attempts'] == ['r2'] for d in opened.values())
    now = datetime(2026, 11, 12, 18, 0, tzinfo=timezone.utc)
    gaps = {g['day']: g for g in B.not_issued(store, B.freshness(store, now))}
    for day in opened:
        assert gaps[day]['status'] == 'not issued' and gaps[day]['cause'] == causes.INPUTS, day
        assert causes.text(causes.INPUTS) in gaps[day]['text'] and 'lookback' in gaps[day]['text']
    assert gaps['2026-11-09']['cause'] == causes.NO_RUN
    assert 'lookback' in OPEN_DAY_WORDING and 'issued' in OPEN_DAY_WORDING
