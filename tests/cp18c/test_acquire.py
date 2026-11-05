"""The acquisition before the cutoff (`cp18.acquire`, `cp18.live.acquire`): D's tier-3 load forecast shown only by a
retrieval strictly before D's cutoff, polled while it is not yet published, archived append-only and published.

A stand-in transport answers ENTSO-E's A65 with "no data" before a publication instant and with a document after it;
every other request is a miss (as an unreachable source). Nothing here touches the network.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import numpy as np
import pandas as pd

from cp15.data import day_hours
from cp18 import acquire, boundary
from cp18.claim import ClaimError
from cp18.live import acquire as AQ
from cp18.live import entsoe, history
from cp18.live.archive import Archive
from cp18.live.recorded import render_entsoe_day
from cp18.live.transport import ReplayMiss, Response
from cp18.store import INPUTS_PATH

UTC = timezone.utc
DAY = date(2026, 11, 6)
CUTOFF = datetime(2026, 11, 5, 10, 0, tzinfo=UTC)
ACK = (b'<?xml version="1.0" encoding="utf-8"?><Acknowledgement_MarketDocument xmlns="urn:iec62325.351:tc57wg16:451-1:'
       b'acknowledgementdocument:7:0"><mRID>x</mRID><createdDateTime>2026-11-05T08:00:00Z</createdDateTime><Reason>'
       b'<code>999</code><text>No matching data found</text></Reason></Acknowledgement_MarketDocument>')


class Clock:
    def __init__(self, start):
        self.now = start

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += timedelta(seconds=seconds)


class Transport:
    def __init__(self, clock, published_at):
        self.clock, self.published_at, self.sent = clock, published_at, []

    def send(self, request):
        request.admit()
        self.sent.append(request.url)
        stamp = self.clock().strftime('%Y-%m-%dT%H:%M:%SZ')
        if request.url == entsoe.API and dict(request.params).get('documentType') == 'A65':
            if self.clock() < self.published_at:
                return Response(200, {}, ACK, stamp, 'live')
            hours = day_hours(DAY)
            snap = pd.DataFrame({'load_forecast_mw': np.linspace(40000, 60000, len(hours))}, index=hours)
            body = render_entsoe_day(snap, 'load_forecast', DAY).replace(b'2026-09-08T13:34:33Z', stamp.encode())
            return Response(200, {}, body, stamp, 'live')
        raise ReplayMiss('not served by this stand-in')


class FakeClaim:
    def __init__(self, fail=False):
        self.fail, self.published = fail, []

    def sync(self):
        if self.fail:
            raise ClaimError('the network is down (stand-in)')

    def publish(self, paths, message):
        self.published.append((paths, message))
        return {'pushed': 'abc'}


def go(tmp_path, start, published_at, claim=None):
    clock = Clock(start)
    claim = claim or FakeClaim()
    record = acquire.run(tmp_path, claim=claim, transport=Transport(clock, published_at), clock=clock,
                         sleep=clock.sleep, poll_seconds=300, margin_seconds=120)
    return record, claim, Archive(tmp_path / INPUTS_PATH)


def test_the_next_day_is_the_one_whose_cutoff_is_ahead():
    assert acquire.next_day(datetime(2026, 11, 5, 9, 59, tzinfo=UTC)) == DAY
    assert acquire.next_day(datetime(2026, 11, 5, 10, 0, tzinfo=UTC)) == DAY + timedelta(days=1)
    assert acquire.next_day(datetime(2026, 7, 1, 8, 59, tzinfo=UTC)) == date(2026, 7, 2)     # CEST: 09:00 UTC


def test_it_polls_until_the_load_forecast_is_published_then_publishes_the_archive(tmp_path):
    record, claim, archive = go(tmp_path, datetime(2026, 11, 5, 8, 50, tzinfo=UTC),
                                datetime(2026, 11, 5, 9, 4, tzinfo=UTC))
    assert record['exit'] == 0 and record['day'] == str(DAY) and record['load_forecast']['shown']
    assert len(record['attempts']) == 4                              # 08:50, 08:55, 09:00 no data; 09:05 published
    assert claim.published and claim.published[0][0] == [INPUTS_PATH]
    with boundary.live(now=datetime(2026, 11, 5, 9, 30, tzinfo=UTC)):
        lfs = archive.records(DAY, 'load_forecast')
        assert len(lfs) == 4 and len({r['id'] for r in lfs}) == 4    # append-only, every response kept
        assert archive.verify(DAY) == []
        values, chosen, _ = history.market(history._Reader(archive, DAY), 'load_forecast', DAY)
        assert chosen['admitted'] and chosen['record'] == lfs[-1]['id'] and not np.isnan(values).any()
        assert 'load_forecast' not in AQ.missing(archive, DAY)


def test_a_load_forecast_not_published_before_the_cutoff_is_not_shown(tmp_path):
    record, claim, archive = go(tmp_path, datetime(2026, 11, 5, 9, 50, tzinfo=UTC),
                                datetime(2026, 11, 5, 12, 0, tzinfo=UTC))
    assert record['exit'] == 1 and not record['load_forecast']['shown'] and len(record['attempts']) == 2   # 09:50, 09:55
    assert 'will not be issued' in record['outcome'] and claim.published         # the evidence is published anyway
    with boundary.live(now=datetime(2026, 11, 5, 9, 55, tzinfo=UTC)):
        assert 'load_forecast' in AQ.missing(archive, DAY)


def test_a_retrieval_after_the_cutoff_is_archived_but_never_shown(tmp_path):
    record, _, _ = go(tmp_path, datetime(2026, 11, 5, 10, 30, tzinfo=UTC), datetime(2026, 11, 5, 9, 0, tzinfo=UTC))
    assert record['day'] == str(DAY + timedelta(days=1))                         # the next day by default
    record, _, archive = acquire.run(tmp_path / 'b', claim=FakeClaim(), day=str(DAY),
                                     transport=Transport(Clock(datetime(2026, 11, 5, 10, 30, tzinfo=UTC)),
                                                         datetime(2026, 11, 5, 9, 0, tzinfo=UTC)),
                                     clock=lambda: datetime(2026, 11, 5, 10, 30, tzinfo=UTC),
                                     sleep=lambda s: None), None, Archive(tmp_path / 'b' / INPUTS_PATH)
    assert record['exit'] == 1 and record['load_forecast']['admitted'] is False
    assert 'not strictly before the cutoff' in record['load_forecast']['reason']


def test_a_refused_claim_is_a_recorded_outcome_never_an_escaped_run(tmp_path):
    record, _, _ = go(tmp_path, datetime(2026, 11, 5, 9, 0, tzinfo=UTC), datetime(2026, 11, 5, 9, 0, tzinfo=UTC),
                      claim=FakeClaim(fail=True))
    assert record['exit'] == 2 and record['outcome'].startswith('refused')
