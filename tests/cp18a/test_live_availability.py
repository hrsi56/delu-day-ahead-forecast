"""CP-18a item 2: the availability judgement, the cutoff and DST days, ruling 1's scope, the GFS flag basis.

Fast; no local data. No date after the development boundary is written here: where one is needed, it is
computed from `cp25.guard.BOUNDARY` at run time, and never printed.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pytest

from cp18.live import availability as A
from cp25 import guard

UTC = timezone.utc


def _utc(text):
    return datetime.fromisoformat(text.replace('Z', '+00:00'))


@pytest.mark.parametrize('day, expected', [
    (date(2026, 9, 6), '2026-09-05T09:00:00Z'),    # D-1 on CEST
    (date(2026, 1, 15), '2026-01-14T10:00:00Z'),   # D-1 on CET
    (date(2026, 3, 29), '2026-03-28T10:00:00Z'),   # D is the spring transition; D-1 still CET
    (date(2026, 3, 30), '2026-03-29T09:00:00Z'),   # D-1 is the spring transition day: 11:00 is CEST
    (date(2025, 10, 26), '2025-10-25T09:00:00Z'),  # D is the autumn transition; D-1 still CEST
    (date(2025, 10, 27), '2025-10-26T10:00:00Z'),  # D-1 is the autumn transition day: 11:00 is CET
])
def test_cutoff_is_d_minus_1_1100_berlin_with_dsts(day, expected):
    assert A.iso(A.cutoff(day)) == expected


def test_price_publication_is_the_documented_schedule():
    pub = A.price_publication(date(2026, 9, 5))
    assert pub['utc'] == '2026-09-04T11:00:00Z' and pub['basis_id'] == 'documented_schedule'
    j = A.judge('price', date(2026, 9, 6), date(2026, 9, 5), pub, {'id': 'r', 'provenance': 'rendered'})
    assert j['admitted'] and not j['by_exception']


def test_the_target_day_price_is_never_admitted():
    pub = A.price_publication(date(2026, 9, 6))
    j = A.judge('price', date(2026, 9, 6), date(2026, 9, 6), pub, {'id': 'r'})
    assert not j['admitted'] and 'embargo' in j['reason']


def _live(day, retrieved, document=None):
    return A.load_publication(day, provenance='live', retrieved_utc=retrieved, document_time_utc=document,
                              development_snapshot=False)


def test_load_forecast_retrieved_strictly_before_the_cutoff_is_shown():
    day = date(2026, 9, 6)
    pub = _live(day, '2026-09-05T08:59:59Z')
    assert pub['basis_id'] == 'retrieval_time'
    assert A.judge('load_forecast', day, day, pub, {'id': 'r', 'provenance': 'live'})['admitted']


def test_load_forecast_retrieved_exactly_at_the_cutoff_is_not_shown():
    day = date(2026, 9, 6)
    pub = _live(day, '2026-09-05T09:00:00Z')
    j = A.judge('load_forecast', day, day, pub, {'id': 'r', 'provenance': 'live'})
    assert not j['admitted'] and 'not strictly before' in j['reason']


def test_load_forecast_document_time_is_a_vintage_basis():
    day = date(2026, 9, 6)
    pub = _live(day, '2026-09-05T12:00:00Z', document='2026-09-05T08:10:00Z')
    assert pub['basis_id'] == 'document_time' and pub['utc'] == '2026-09-05T08:10:00Z'
    assert A.judge('load_forecast', day, day, pub, {'id': 'r', 'provenance': 'live'})['admitted']
    late = _live(day, '2026-09-05T12:00:00Z', document='2026-09-05T09:30:00Z')
    assert not A.judge('load_forecast', day, day, late, {'id': 'r', 'provenance': 'live'})['admitted']


def test_load_forecast_has_no_documented_schedule_basis():
    day = date(2026, 9, 6)
    pub = {'utc': '2026-09-05T08:00:00Z', 'basis_id': 'documented_schedule', 'basis': 'Art. 6 deadline'}
    j = A.judge('load_forecast', day, day, pub, {'id': 'r', 'provenance': 'live'})
    assert not j['admitted'] and 'tier-3' in j['reason']


def test_ruling_1_admits_the_development_history_and_says_so():
    day = date(2026, 9, 6)
    pub = A.load_publication(day, provenance='rendered', retrieved_utc='2026-09-08T13:34:33Z', document_time_utc=None,
                             development_snapshot=True)
    assert pub['basis_id'] == 'ruling_1_exception'
    assert 'ruling 1' in pub['basis'] and 'development data only' in pub['basis']
    j = A.judge('load_forecast', day, day, pub, {'id': 'r', 'provenance': 'rendered'})
    assert j['admitted'] and j['by_exception']


def test_ruling_1_is_refused_after_the_development_history():
    later = A.RULING_1_LAST_DAY + timedelta(days=1)       # computed, never written
    with pytest.raises(ValueError):
        A.load_publication(later, provenance='rendered', retrieved_utc=None, document_time_utc=None,
                           development_snapshot=True)
    pub = {'utc': None, 'basis_id': 'ruling_1_exception', 'basis': A.BASES['ruling_1_exception']}
    j = A.judge('load_forecast', later, later, pub, {'id': 'r', 'provenance': 'rendered'})
    admitted, reason = j['admitted'], j['reason']
    assert admitted is False
    assert 'development history only' in reason


def test_ruling_1_scope_is_the_boundary_day_but_not_the_guard():
    assert A.RULING_1_LAST_DAY == guard.BOUNDARY


def test_ruling_1_never_admits_a_live_retrieval():
    day = date(2026, 9, 6)
    pub = {'utc': None, 'basis_id': 'ruling_1_exception', 'basis': A.BASES['ruling_1_exception']}
    assert not A.judge('load_forecast', day, day, pub, {'id': 'r', 'provenance': 'live'})['admitted']


def _listing(object_lm='2026-09-05T04:02:56.000Z', index_lm='2026-09-05T04:03:41.000Z'):
    return {f'f{lead:03d}': {'object': {'last_modified': object_lm, 'size': 1}, 'index': {'last_modified': index_lm, 'size': 1}}
            for lead in range(21, 49, 3)}


def test_gfs_published_before_the_cutoff_of_the_day_it_serves():
    pub = A.gfs_publication(_listing(), None)
    assert pub['basis_id'] == 'aws_last_modified' and pub['utc'] == '2026-09-05T04:03:41Z'
    j = A.judge('gfs', date(2026, 9, 6), date(2026, 9, 6), pub, {'id': 'g', 'provenance': 'live'})
    assert j['admitted'] and j['cutoff_utc'] == '2026-09-05T09:00:00Z'


def test_gfs_rewritten_after_the_cutoff_is_late_under_ruling_4():
    pub = A.gfs_publication(_listing(index_lm='2026-09-05T09:00:00.000Z'), None)   # exactly at the cutoff
    assert not A.judge('gfs', date(2026, 9, 6), date(2026, 9, 6), pub, {'id': 'g'})['admitted']
    pub = A.gfs_publication(_listing(object_lm='2026-09-05T15:10:00.000Z'), None)
    assert not A.judge('gfs', date(2026, 9, 6), date(2026, 9, 6), pub, {'id': 'g'})['admitted']


def test_gfs_without_a_complete_listing_falls_back_to_the_schedule_or_nothing():
    partial = _listing()
    del partial['f048']['index']
    recon = {'bracketed': True, 'available_utc': '2026-09-05T03:53:34Z', 'capture_before': '2026-06-14',
             'capture_after': '2026-09-23', 'end_48h_before': '03:52:42', 'end_48h_after': '03:53:34'}
    pub = A.gfs_publication(partial, recon)
    assert pub['basis_id'] == 'documented_schedule'
    assert A.judge('gfs', date(2026, 9, 6), date(2026, 9, 6), pub, {'id': 'g'})['admitted']
    none = A.gfs_publication(partial, None)
    assert none['basis_id'] == 'none'
    assert not A.judge('gfs', date(2026, 9, 6), date(2026, 9, 6), none, {'id': 'g'})['admitted']


def test_a_gfs_run_is_judged_against_its_own_day_not_the_built_day():
    pub = A.gfs_publication(_listing(object_lm='2026-09-04T15:10:00.000Z', index_lm='2026-09-04T15:10:00.000Z'), None)
    j = A.judge('gfs', date(2026, 9, 6), date(2026, 9, 5), pub, {'id': 'g'})
    assert not j['admitted'] and j['cutoff_utc'] == '2026-09-04T09:00:00Z'


def test_strictly_before_rejects_naive_instants():
    with pytest.raises(ValueError):
        A.parse_iso('2026-09-05T08:00:00')
