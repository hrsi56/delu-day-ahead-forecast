"""The outcomes' reconciliation (`cp18.outcomes`), as the live pipeline runs it, on CP-18a's recorded responses.

A day's prices are pending until their publication time, then reconciled once; a later run reconciles the days whose
outcomes have since been published; a failed retrieval archives nothing and is retried; a later archived record with
other values is a revision; a published price is never withdrawn.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
import json

import numpy as np
import pytest

from cp18 import outcomes as OC
from cp18.live.archive import Archive
from cp18.live.transport import ReplayMiss, ReplayTransport
from cp18b.support18b import RECORDED, REPLAY, ROOT

UTC = timezone.utc


def at(text: str) -> datetime:
    return datetime.fromisoformat(text).astimezone(UTC)


def snapshot_prices(day: date) -> list:
    from cp28 import reader
    series = reader.prices(ROOT)
    return [float(series[k]) for k in OC.canonical_keys(day)]


class Refusing:
    def send(self, request):
        raise ReplayMiss('refused for the test')


def test_pending_until_published_then_reconciled_once(tmp_path):
    log, tr, day = OC.Outcomes(tmp_path), ReplayTransport(REPLAY), date(2026, 9, 5)
    assert log.reconcile(None, [day], at('2026-09-04T12:59:59+02:00'), 'r1', transport=tr) is None    # not published
    assert log.view() == {} and not log.own.has(day)
    entry = log.reconcile(None, [day], at('2026-09-04T13:00:00+02:00'), 'r2', transport=tr)
    item = log.view()[str(day)]
    assert entry['days'] == [str(day)] and item['status'] == 'published'
    assert item['prices'] == snapshot_prices(day)
    assert item['first']['published_utc'] == '2026-09-04T11:00:00+00:00'
    assert item['first']['publication_basis'] == 'documented_schedule' and item['first']['provenance'] == 'rendered'
    assert log.reconcile(None, [day], at('2026-09-05T12:00:00+02:00'), 'r3', transport=tr) is None      # unchanged


def test_a_later_run_reconciles_the_days_published_since(tmp_path):
    log, tr = OC.Outcomes(tmp_path), ReplayTransport(REPLAY)
    first = log.reconcile(None, [date(2026, 9, 3), date(2026, 9, 5)], at('2026-09-03T12:00:00+02:00'), 'r1', transport=tr)
    assert first['days'] == ['2026-09-03']
    assert log.log.read(log.log.verify()[-1])['pending'] == ['2026-09-05']
    later = log.reconcile(None, [date(2026, 9, 3), date(2026, 9, 5)], at('2026-09-04T14:00:00+02:00'), 'r2', transport=tr)
    assert later['days'] == ['2026-09-05'] and len(log.log.verify()) == 2


def test_a_failed_retrieval_archives_nothing_and_is_retried(tmp_path):
    log, day = OC.Outcomes(tmp_path), date(2026, 9, 2)
    assert log.reconcile(None, [day], at('2026-09-03T12:00:00+02:00'), 'r1', transport=Refusing()) is None
    assert not log.own.has(day)
    entry = log.reconcile(None, [day], at('2026-09-03T12:00:00+02:00'), 'r2', transport=ReplayTransport(REPLAY))
    assert entry['days'] == [str(day)]


def test_the_input_archive_serves_outcomes_and_a_later_record_is_a_revision(tmp_path):
    from cp18.live import recorded as R
    archive = Archive(tmp_path / 'inputs')
    for d in (date(2026, 9, 4), date(2026, 9, 5)):
        R.archive_day(archive, RECORDED / 'replay', d, ROOT, 'smard', [RECORDED / 'gfs'])
    day = date(2026, 9, 3)
    # a later archived record of 2026-09-03 with one changed value, as a revised publication would arrive
    later = date(2026, 9, 6)
    R.archive_day(archive, RECORDED / 'replay', later, ROOT, 'smard', [RECORDED / 'gfs'])
    record = next(r for r in archive.records(later, 'price') if str(day) in r['covers'])
    body = json.loads(archive.body(later, record))
    keys = OC.canonical_keys(day)
    first_ms = int(datetime.fromisoformat(keys[5]).timestamp() * 1000)
    hits = [row for row in body['series'] if first_ms <= row[0] < first_ms + 3_600_000]
    for row in hits:
        row[1] = row[1] + 1.0
    revised = dict(record, id='price-smard-bucket-revised', retrieved_utc='2026-09-06T09:00:00Z')
    archive.add(later, revised, body=json.dumps(body).encode())
    log = OC.Outcomes(tmp_path / 'outcomes')
    log.reconcile(archive, [day], at('2026-09-06T12:00:00+02:00'), 'r1')
    item = log.view()[str(day)]
    assert item['status'] == 'published' and item['first']['archive'] == 'input archive'
    base = snapshot_prices(day)
    assert item['prices'][5] == pytest.approx(base[5] + 1.0) and item['prices'][:5] == base[:5]
    assert item['revised_utc'][5] == '2026-09-06T09:00:00Z' and item['revised_utc'][4] == ''
    assert item['revisions'][0]['keys'] == [keys[5]]


def test_a_published_price_is_never_withdrawn(tmp_path):
    log, tr, day = OC.Outcomes(tmp_path), ReplayTransport(REPLAY), date(2026, 9, 1)
    log.reconcile(None, [day], at('2026-09-01T12:00:00+02:00'), 'r1', transport=tr)
    with pytest.raises(ValueError, match='never withdrawn'):
        log.reconcile(None, [day], at('2026-08-30T12:00:00+02:00'), 'r2')


def test_the_bundle_outcomes_hold_every_canonical_key_and_null_for_pending(tmp_path):
    days = [date(2025, 10, 26), date(2026, 3, 29), date(2026, 9, 5)]     # 25, 23 and 24 hours
    value = OC.bundle_outcomes(days, {})
    assert value['schema'] == 'cp17-outcomes-v1' and len(value['prices']) == 25 + 23 + 24
    assert all(p['price'] is None and p['published_utc'] == '' for p in value['prices'])
    assert [OC.day_status(d, value)['state'] for d in days] == ['pending'] * 3
    from cp17.schema import SCHEMAS, validate
    assert validate(value, SCHEMAS['outcomes']) == []


def test_missing_zero_and_negative_prices_count_as_they_are():
    day = date(2026, 9, 5)
    keys = OC.canonical_keys(day)
    prices = [None, 0.0, -5.0] + [10.0] * (len(keys) - 3)
    view = {str(day): {'status': 'partial', 'keys': keys, 'prices': prices, 'revised_utc': [''] * len(keys),
                       'first': {'published_utc': '2026-09-04T11:00:00+00:00'}}}
    value = OC.bundle_outcomes([day], view)
    status = OC.day_status(day, value)
    assert status == {'day': str(day), 'state': 'partial', 'published_hours': 23, 'canonical_hours': 24}
    m = OC.outcome_map(value)
    assert np.isnan(m[keys[0]]) and m[keys[1]] == 0.0 and m[keys[2]] == -5.0
