"""The Owner's decision 31 (CP-18d): the input class of an issued live day, and D's load forecast fetched after the
cutoff (`cp18.inputclass`, `cp18.live.history.fetched_after_cutoff`, `cp18.live.build`).

A stand-in transport answers ENTSO-E's A65 with "no data" before a publication instant and with a document after it
(CP-18c's `test_acquire` stand-in). Nothing here touches the network.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
import json
from pathlib import Path

import numpy as np
import pytest

from cp18 import acquire, boundary, inputclass
from cp18.live import acquire as AQ
from cp18.live import history
from cp18.live.archive import Archive
from cp18.live.build import _availability
from cp18.store import INPUTS_PATH, STORE_PATH, LiveStore

from cp18c.test_acquire import Clock, FakeClaim, Transport      # CP-18c's own stand-ins, reused unchanged

UTC = timezone.utc
ROOT = Path(__file__).resolve().parents[2]
DAY = date(2026, 11, 6)
CUTOFF = datetime(2026, 11, 5, 10, 0, tzinfo=UTC)


def acquired(tmp_path, at: datetime, published_at: datetime) -> Archive:
    """D's inputs acquired once at `at` (one retrieval: no polling), the forecast published at `published_at`."""
    clock = Clock(at)
    acquire.run(tmp_path, claim=FakeClaim(), day=str(DAY), transport=Transport(clock, published_at), clock=clock,
                sleep=clock.sleep, poll_seconds=10 ** 6, margin_seconds=0)
    return Archive(tmp_path / INPUTS_PATH)


# ------------------------------------------------------------------------------------------------ the label
def test_the_two_classes_and_their_wording_never_late_or_timely():
    assert inputclass.label(inputclass.BEFORE) == {'input_class': 'before_cutoff',
                                                   'input_class_text': 'all inputs before the cutoff',
                                                   'load_forecast_fetched_utc': None}
    after = inputclass.label(inputclass.AFTER, '2026-11-05T10:30:00+00:00')
    assert after == {'input_class': 'load_forecast_after_cutoff',
                     'input_class_text': 'load forecast fetched after the cutoff',
                     'load_forecast_fetched_utc': '2026-11-05T10:30:00Z'}
    for text in inputclass.TEXT.values():
        assert 'late' not in text.lower() and 'timely' not in text.lower()


@pytest.mark.parametrize('cls, fetched', [('late', None), (inputclass.AFTER, None), (inputclass.AFTER, ''),
                                          (inputclass.BEFORE, '2026-11-05T10:30:00Z')])
def test_an_unknown_or_incomplete_label_is_refused(cls, fetched):
    with pytest.raises(inputclass.LabelMissing):
        inputclass.label(cls, fetched)


def test_the_live_records_issued_before_cp18d_are_derived_from_their_own_evidence():
    store = LiveStore(ROOT / STORE_PATH)
    store.verify()
    issued = {d: v for d, v in store.days().items() if v['status'] == 'issued'}
    assert issued and all(v['input_class'] == inputclass.BEFORE for v in issued.values())
    for day in issued:
        record = json.loads((ROOT / STORE_PATH / 'issued' / day / 'record.json').read_text())
        assert record['schema'] == inputclass.LEGACY_SCHEMA
        assert inputclass.required_load_forecast(record)['admitted']


# ------------------------------------------------------------------------------------------------ the copy
def test_a_missed_acquisition_leaves_a_complete_copy_fetched_after_the_cutoff_which_d31_uses(tmp_path):
    archive = acquired(tmp_path, datetime(2026, 11, 5, 10, 30, tzinfo=UTC), datetime(2026, 11, 5, 9, 0, tzinfo=UTC))
    with boundary.live(now=datetime(2026, 11, 5, 10, 31, tzinfo=UTC)):
        reader = history._Reader(archive, DAY)
        values, chosen, _ = history.market(reader, 'load_forecast', DAY)
        assert values is None and not chosen['admitted']                     # decision 22: not shown before the cutoff
        assert not AQ.load_forecast_shown(archive, DAY)['shown']
        values, j = history.fetched_after_cutoff(reader, DAY)
    assert not np.isnan(values).any() and len(values) == 24
    assert j['fetched_after_cutoff'] and not j['admitted'] and j['fetched_utc'] == '2026-11-05T10:30:00Z'
    assert j['cutoff_utc'] == '2026-11-05T10:00:00Z' and 'not strictly before the cutoff' in j['reason']


def test_a_copy_before_the_cutoff_is_used_as_before_and_needs_no_label(tmp_path):
    archive = acquired(tmp_path, datetime(2026, 11, 5, 9, 30, tzinfo=UTC), datetime(2026, 11, 5, 9, 0, tzinfo=UTC))
    with boundary.live(now=datetime(2026, 11, 5, 9, 31, tzinfo=UTC)):
        values, chosen, _ = history.market(history._Reader(archive, DAY), 'load_forecast', DAY)
        assert chosen['admitted'] and not np.isnan(values).any()
        assert history.fetched_after_cutoff(history._Reader(archive, DAY), DAY) is None


def test_no_copy_at_all_is_no_copy(tmp_path):
    # the source answers "no data" until noon: nothing complete to use, so the day stays open with its cause
    archive = acquired(tmp_path, datetime(2026, 11, 5, 10, 30, tzinfo=UTC), datetime(2026, 11, 5, 12, 0, tzinfo=UTC))
    with boundary.live(now=datetime(2026, 11, 5, 10, 31, tzinfo=UTC)):
        assert history.fetched_after_cutoff(history._Reader(archive, DAY), DAY) is None


def test_the_earliest_complete_copy_after_the_cutoff_is_the_one_used(tmp_path):
    archive = acquired(tmp_path, datetime(2026, 11, 5, 10, 30, tzinfo=UTC), datetime(2026, 11, 5, 9, 0, tzinfo=UTC))
    clock = Clock(datetime(2026, 11, 5, 11, 45, tzinfo=UTC))
    with boundary.live(now=clock()):
        AQ.acquire_market(archive, DAY, Transport(clock, datetime(2026, 11, 5, 9, 0, tzinfo=UTC)), 'load_forecast')
        assert len(archive.records(DAY, 'load_forecast')) == 2
        _, j = history.fetched_after_cutoff(history._Reader(archive, DAY), DAY)
    assert j['fetched_utc'] == '2026-11-05T10:30:00Z'


# ------------------------------------------------------------------------------------------------ the build's label
def _history(copy=None, missing=()):
    h = history.History(DAY, date(2026, 9, 6), None, None, [])
    h.load_forecast_copy, h.missing_required = copy, list(missing)
    return h


def test_the_availability_names_the_class_and_d31_never_rescues_another_input():
    copy = {'record': 'lf@x', 'archive_day': str(DAY), 'fetched_utc': '2026-11-05T10:30:00Z',
            'publication_utc': '2026-11-05T10:30:00Z', 'cutoff_utc': '2026-11-05T10:00:00Z', 'sha256': '0' * 64}
    after = _availability(_history(copy), DAY, [])
    assert after['shown'] and after['input_class'] == inputclass.AFTER
    assert after['load_forecast_fetched_utc'] == '2026-11-05T10:30:00Z' and after['load_forecast_copy'] == copy
    before = _availability(_history(), DAY, [])
    assert before['shown'] and before['input_class'] == inputclass.BEFORE and before['load_forecast_copy'] is None
    # a price that cannot be shown to precede the cutoff keeps decision 22's consequence, the copy notwithstanding
    price = _availability(_history(copy, ['price of 2026-11-05: published after the cutoff']), DAY, [])
    assert not price['shown'] and price['reasons'] == ['price of 2026-11-05: published after the cutoff']
