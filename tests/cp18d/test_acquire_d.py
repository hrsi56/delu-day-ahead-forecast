"""The earlier acquisition (CP-18d, decision 31's experiment): the in-job wait ends at the cutoff's margin or at the
job's own stop-by, whichever comes first, and publishes what it found; and the rehearsal's stand-in source on a
development day (`cp18.rehearsal`), which never enters the live boundary.

CP-18c's stand-in transport and claim are reused (`tests/cp18c/test_acquire.py`). Nothing touches the network.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pytest

from cp18 import acquire, boundary, rehearsal
from cp18.live.archive import Archive
from cp18.live.transport import ReplayTransport
from cp18.store import INPUTS_PATH

from cp18c.test_acquire import DAY, Clock, FakeClaim, Transport

UTC = timezone.utc
ROOT = Path(__file__).resolve().parents[2]
RECORDED = ROOT / 'reports/cp18a/dryrun/recorded'


def test_an_early_start_waits_in_its_job_until_its_stop_by_then_publishes_what_it_found(tmp_path):
    clock = Clock(datetime(2026, 11, 5, 5, 0, tzinfo=UTC))
    claim = FakeClaim()
    record = acquire.run(tmp_path, claim=claim, transport=Transport(clock, datetime(2026, 11, 5, 9, 4, tzinfo=UTC)),
                         clock=clock, sleep=clock.sleep, poll_seconds=300, margin_seconds=120, window_hours=6,
                         stop_by=datetime(2026, 11, 5, 6, 0, tzinfo=UTC))
    assert record['day'] == str(DAY) and record['exit'] == 1 and not record['load_forecast']['shown']
    assert record['stopped'].startswith('its stop-by') and record['stop_by_utc'] == '2026-11-05T06:00:00Z'
    assert len(record['attempts']) == 12 and clock() < datetime(2026, 11, 5, 6, 0, tzinfo=UTC)     # 05:00 ... 05:55
    assert claim.published and 'fetched after the cutoff' in record['outcome']      # published; the next start continues


def test_a_start_inside_the_window_waits_until_the_forecast_is_published(tmp_path):
    clock = Clock(datetime(2026, 11, 5, 4, 30, tzinfo=UTC))
    record = acquire.run(tmp_path, claim=FakeClaim(), transport=Transport(clock, datetime(2026, 11, 5, 9, 4, tzinfo=UTC)),
                         clock=clock, sleep=clock.sleep, poll_seconds=300, margin_seconds=120, window_hours=6,
                         stop_by=datetime(2026, 11, 5, 10, 10, tzinfo=UTC))
    assert record['exit'] == 0 and record['stopped'] == 'shown' and record['load_forecast']['shown']
    assert clock() == datetime(2026, 11, 5, 9, 5, tzinfo=UTC)


def test_a_start_further_than_the_window_does_nothing(tmp_path):
    clock = Clock(datetime(2026, 11, 5, 3, 30, tzinfo=UTC))                  # 6.5 h before the cutoff
    claim = FakeClaim()
    record = acquire.run(tmp_path, claim=claim, transport=Transport(clock, clock()), clock=clock, sleep=clock.sleep,
                         window_hours=6)
    assert record['exit'] == 0 and record['outcome'].startswith('not yet') and not claim.published


def test_a_second_start_finds_nothing_missing_and_writes_nothing_twice(tmp_path):
    clock = Clock(datetime(2026, 11, 5, 9, 10, tzinfo=UTC))
    transport = Transport(clock, datetime(2026, 11, 5, 9, 4, tzinfo=UTC))
    acquire.run(tmp_path, claim=FakeClaim(), transport=transport, clock=clock, sleep=clock.sleep)
    with boundary.live(now=clock()):
        first = Archive(tmp_path / INPUTS_PATH).records(DAY, 'load_forecast')
    sent = len(transport.sent)
    record = acquire.run(tmp_path, claim=FakeClaim(), transport=transport, clock=clock, sleep=clock.sleep)
    with boundary.live(now=clock()):
        assert Archive(tmp_path / INPUTS_PATH).records(DAY, 'load_forecast') == first
    lf = [i for i in record['attempts'][0]['items'] if i['input'] == 'load_forecast']
    assert record['exit'] == 0 and lf == [{'input': 'load_forecast', 'skipped': 'already archived'}]
    from cp18.live import entsoe
    assert entsoe.API in transport.sent[:sent] and entsoe.API not in transport.sent[sent:]   # not retrieved again


@pytest.mark.skipif(not (ROOT / 'data/snapshot.parquet').exists(), reason='the development snapshot is absent')
def test_the_rehearsal_stand_in_waits_for_real_on_a_development_day_and_never_enters_the_live_boundary(tmp_path):
    day = date(2026, 9, 4)
    start = datetime(2026, 9, 3, 8, 40, tzinfo=UTC)
    clock = rehearsal.real_time_clock(start)
    stand_in = rehearsal.StandInLoadForecast(ROOT, clock, start + timedelta(seconds=2),
                                             fallback=ReplayTransport(RECORDED / 'replay' / 'smard'))
    record = acquire.run(tmp_path, claim=FakeClaim(), day=str(day), transport=stand_in, clock=clock, poll_seconds=1,
                         margin_seconds=120, live=False, inputs=('price', 'load_forecast'))
    assert record['boundary']['mode'] == 'development' and record['exit'] == 0 and record['load_forecast']['shown']
    assert len(record['attempts']) >= 2 and not stand_in.sent[0]['published'] and stand_in.sent[-1]['published']
    records = Archive(tmp_path / INPUTS_PATH).records(day, 'load_forecast')
    assert all(r['origin'] == rehearsal.ORIGIN for r in records)                   # never passes for a retrieval
    assert not boundary.is_live()


def test_the_stand_in_refuses_a_day_after_the_development_boundary():
    from cp25 import guard
    with pytest.raises(guard.BoundaryRefused):
        rehearsal.published_before(date(2026, 9, 7), 50)
