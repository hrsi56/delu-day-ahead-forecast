"""CP-18d's negative controls for decision 31 (the brief's item 6), through the pipeline, the store, the Space's live
record and the bundle, with CP-18c's stand-ins (a bare `origin`, stand-in inputs and issuance):

- a day issued with the load forecast fetched after the cutoff is labelled so everywhere, and counted as issued;
- a late copy is refused for any input other than the load forecast (`test_input_class.py` holds the build's own case);
- a day issued twice is refused; an issued forecast replaced is refused;
- the label missing is refused: the built inputs without it, a record without it, at write and at verification.

(The fifth control, a moved `main` touching the run's own paths, is in `test_claim_o47.py`.)
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path

import pytest

from cp18 import boundary, causes, inputclass
from cp18.live_claims import live_record
from cp18.store import STORE_PATH, LiveStore, StoreRefused

from cp18c.support18c import Inputs, at_noon, make_origin, run, synthetic_state

ORIGIN, FIRST = date(2026, 9, 6), date(2026, 9, 7)
CARRY = date(2026, 11, 3)


class LabelledInputs(Inputs):
    """CP-18c's stand-in inputs, with decision 31's label: the `after` days were built with D's load forecast fetched
    after the cutoff (at noon UTC of D−1); the `unlabelled` days come back from the build without any class."""

    def __init__(self, after=(), unlabelled=(), **kw):
        super().__init__(**kw)
        self.after, self.unlabelled = {str(d) for d in after}, {str(d) for d in unlabelled}

    def build(self, day, *, buffers, search_file, out):
        built = super().build(day, buffers=buffers, search_file=search_file, out=out)
        if str(day) in self.unlabelled:
            return {k: v for k, v in built.items() if k not in inputclass.FIELDS}
        if str(day) in self.after and built['shown']:
            built.update(inputclass.label(inputclass.AFTER, f'{day - timedelta(days=1)}T12:00:00Z'))
        return built


def origin(tmp_path):
    return make_origin(tmp_path, synthetic_state(ORIGIN), ORIGIN, FIRST, carry_to=CARRY)


def test_a_day_issued_with_the_copy_after_the_cutoff_is_labelled_and_counted_as_issued(tmp_path):
    repo = origin(tmp_path)('a')
    now = at_noon(date(2026, 11, 4))
    with boundary.live(now=now):
        record = run(repo, tmp_path, now, LabelledInputs(after=['2026-11-05']), mode='live', label='r1')
    item = record['days']['2026-11-05']
    assert item['status'] == 'issued' and item['input_class'] == inputclass.AFTER
    assert item['input_class_text'] == 'load forecast fetched after the cutoff'
    assert item['load_forecast_fetched_utc'] == '2026-11-04T12:00:00Z'
    assert record['days']['2026-11-04']['input_class'] == inputclass.BEFORE
    store = LiveStore(repo / STORE_PATH)
    store.verify()
    days = store.days()
    assert days['2026-11-05']['status'] == 'issued' and days['2026-11-05']['input_class'] == inputclass.AFTER
    rec = json.loads((repo / STORE_PATH / 'issued/2026-11-05/record.json').read_text())
    assert rec['schema'] == inputclass.RECORD_SCHEMA and inputclass.of_record(rec)['input_class'] == inputclass.AFTER
    live = live_record(repo / 'live')
    shown = {i['day']: i for i in live['issued']}
    assert shown['2026-11-05']['input_class_text'] == 'load forecast fetched after the cutoff'
    assert shown['2026-11-05']['load_forecast_fetched_utc'] == '2026-11-04T12:00:00+00:00'
    assert {c['input_class']: c['issued'] for c in live['input_classes']} == {inputclass.BEFORE: 2, inputclass.AFTER: 1}


def test_negative_control_the_built_inputs_without_a_label_are_refused_and_the_day_stays_open(tmp_path):
    repo = origin(tmp_path)('a')
    now = at_noon(date(2026, 11, 4))
    with boundary.live(now=now):
        record = run(repo, tmp_path, now, LabelledInputs(unlabelled=['2026-11-05']), mode='live', label='r1')
    item = record['days']['2026-11-05']
    assert item['status'] == 'open' and item['cause'] == causes.INPUTS and item['error'].startswith('LabelMissing')
    assert '2026-11-05' not in LiveStore(repo / STORE_PATH).days()


def test_negative_control_a_record_without_its_label_is_refused_at_write_and_at_verification(tmp_path):
    repo = origin(tmp_path)('a')
    now = at_noon(date(2026, 11, 4))
    with boundary.live(now=now):
        run(repo, tmp_path, now, LabelledInputs(), mode='live', label='r1')
    store = LiveStore(repo / STORE_PATH)
    state, _ = store.state()
    art = json.loads((store.folder / 'issued/2026-11-05/artifact.json').read_text())
    rec = json.loads((store.folder / 'issued/2026-11-05/record.json').read_text())
    unlabelled = {k: v for k, v in rec.items() if k not in inputclass.FIELDS}
    with pytest.raises(inputclass.LabelMissing):
        inputclass.of_record(unlabelled)
    # at write: a later day's record without its label is never written
    later = dict(unlabelled, day='2026-11-06')
    with pytest.raises(StoreRefused, match='input class'):
        store.record_day(date(2026, 11, 6), state, dict(art, delivery_day='2026-11-06'), later, state.digest())
    assert '2026-11-06' not in store.days()
    # at verification: an issued record rewritten without its label (and re-hashed) is refused, wherever it is read
    entries = [json.loads(line) for line in (store.folder / 'ledger.jsonl').read_text().splitlines()]
    entry = next(e for e in entries if e.get('kind') == 'issuance' and e['day'] == '2026-11-05')
    (store.folder / entry['record_file']).write_text(json.dumps(unlabelled))
    with pytest.raises(StoreRefused):
        LiveStore(repo / STORE_PATH).verify()
    with pytest.raises(StoreRefused):
        live_record(repo / 'live')


def test_negative_control_a_label_its_evidence_contradicts_is_refused():
    rec = {'schema': inputclass.RECORD_SCHEMA, 'day': '2026-11-05', 'cutoff_utc': '2026-11-04T10:00:00+00:00',
           'inputs': {'availability': {'records': [
               {'input': 'load_forecast', 'data_day': '2026-11-05', 'required': True, 'admitted': True}]}}}
    assert inputclass.of_record({**rec, **inputclass.label(inputclass.BEFORE)})['input_class'] == inputclass.BEFORE
    with pytest.raises(inputclass.LabelMissing, match='no copy fetched after the cutoff'):
        inputclass.of_record({**rec, **inputclass.label(inputclass.AFTER, '2026-11-04T11:00:00Z')})
    late = {'input': 'load_forecast', 'data_day': '2026-11-05', 'required': True, 'admitted': False,
            'fetched_after_cutoff': True, 'fetched_utc': '2026-11-04T11:00:00Z', 'cutoff_utc': '2026-11-04T10:00:00Z'}
    rec['inputs']['availability']['records'] = [late]
    assert inputclass.of_record({**rec, **inputclass.label(inputclass.AFTER, '2026-11-04T11:00:00Z')})
    for bad in (inputclass.label(inputclass.BEFORE), inputclass.label(inputclass.AFTER, '2026-11-04T11:30:00Z'),
                {**inputclass.label(inputclass.AFTER, '2026-11-04T11:00:00Z'), 'input_class_text': 'late'}):
        with pytest.raises(inputclass.LabelMissing):
            inputclass.of_record({**rec, **bad})
    # a copy fetched after the issuance that used it is refused (the run fetches, then builds)
    with pytest.raises(inputclass.LabelMissing, match='after the issuance'):
        inputclass.of_record({**rec, 'issuance_started_utc': '2026-11-04T10:59:00+00:00',
                              **inputclass.label(inputclass.AFTER, '2026-11-04T11:00:00Z')})
    assert inputclass.of_record({**rec, 'issuance_started_utc': '2026-11-04T11:05:00+00:00',
                                 **inputclass.label(inputclass.AFTER, '2026-11-04T11:00:00Z')})
    rec['inputs']['availability']['records'] = [dict(late, fetched_utc='2026-11-04T09:00:00Z')]
    with pytest.raises(inputclass.LabelMissing, match='before the cutoff'):
        inputclass.of_record({**rec, **inputclass.label(inputclass.AFTER, '2026-11-04T09:00:00Z')})


def test_negative_control_a_day_issued_twice_is_refused(tmp_path):
    checkout = origin(tmp_path)
    repo = checkout('a')
    now = at_noon(date(2026, 11, 4))
    with boundary.live(now=now):
        run(repo, tmp_path, now, LabelledInputs(after=['2026-11-05']), mode='live', label='r1')
        # a second host on the same wall clock: the day is decided, never issued again (with either class)
        other = checkout('b')
        record = run(other, tmp_path, now, LabelledInputs(), mode='live', label='r2')
    assert record['planned'] == [] and record['outcome'] == 'nothing to issue'
    store = LiveStore(repo / STORE_PATH)
    state, _ = store.state()
    art = json.loads((store.folder / 'issued/2026-11-05/artifact.json').read_text())
    rec = json.loads((store.folder / 'issued/2026-11-05/record.json').read_text())
    with pytest.raises(StoreRefused):
        store.record_day(date(2026, 11, 5), state, art, dict(rec, **inputclass.label(inputclass.BEFORE)),
                         state.digest())
    assert [e['day'] for e in store.entries() if e['kind'] == 'issuance'] == ['2026-11-03', '2026-11-04', '2026-11-05']


def test_negative_control_an_issued_forecast_replaced_is_refused(tmp_path):
    repo = origin(tmp_path)('a')
    now = at_noon(date(2026, 11, 4))
    with boundary.live(now=now):
        run(repo, tmp_path, now, LabelledInputs(after=['2026-11-05']), mode='live', label='r1')
    path = repo / STORE_PATH / 'issued/2026-11-05/artifact.json'
    art = json.loads(path.read_text())
    art['quantiles'][0][0] += 1.0                 # a replaced forecast (relabelled or rescored would be the same)
    path.write_text(json.dumps(art))
    with pytest.raises(StoreRefused):
        LiveStore(repo / STORE_PATH).verify()


def test_the_after_cutoff_fixture_is_a_verified_store_copy_and_refuses_a_checkout(tmp_path):
    import shutil
    from cp18d.fixture_after_cutoff import FIXTURE, relabel
    root = Path(__file__).resolve().parents[2]
    shutil.copytree(root / 'live/store', tmp_path / 'live/store')
    relabel(tmp_path / 'live', '2026-11-14', '2026-11-13T10:21:07Z')
    live = live_record(tmp_path / 'live')
    shown = {i['day']: i for i in live['issued']}
    assert shown['2026-11-14']['input_class'] == inputclass.AFTER
    assert shown['2026-11-14']['load_forecast_fetched_utc'] == '2026-11-13T10:21:07+00:00'
    assert shown['2026-11-15']['input_class'] == inputclass.BEFORE
    rec = json.loads((tmp_path / 'live/store/issued/2026-11-14/record.json').read_text())
    assert rec['fixture'] == FIXTURE
    with pytest.raises(SystemExit, match='refused'):
        relabel(root / 'live', '2026-11-14', '2026-11-13T10:21:07Z')
