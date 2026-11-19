"""CP-18e, the Owner's decision 33: S_13's state serves every live delivery day, and nothing before 2027-01-06 changes.

The controls, one for each rule (the brief's item 5): a later search's state entered into the store is refused; a day
served by another state than S_13's is refused by the live path; the rule before decision 33 leaves a day from
2027-01-06 open with "S_14's state not in place". The pipeline runs use CP-18c's stand-ins (`cp18c.support18c`): a bare
origin with a store, inputs that are shown, and `cp17.issue`'s own artifact around a fixed forecast.
"""
from __future__ import annotations

from datetime import date, timedelta
import json
import os
from pathlib import Path
import re
import subprocess
import sys

import pytest

from cp17 import runtime
from cp18 import boundary, causes, pipeline, serving
from cp18.claim import Claim
from cp18.host import PINNED, committed_path
from cp18.live import payloads as P
from cp18.store import STORE_PATH, LiveStore, StoreRefused
from cp26 import search as S26

from cp18c.support18c import Inputs, at_noon, make_origin, passing_checks, stand_in_issue, synthetic_state

ROOT = Path(__file__).resolve().parents[2]
K13 = ROOT / committed_path(runtime.K13, PINNED)          # the pinned S_13, as the live product commits it
FIRST_LATER = date(2027, 1, 6)                            # S_14's day in CP-26's schedule
RUN_FIELDS = {'run_id', 'run_started_utc', 'issuance_started_utc', 'issuance_finished_utc', 'process_seconds',
              'process_seconds_sum', 'issue_day_seconds', 'gate'}


def days(first: date, last: date):
    d = first
    while d <= last:
        yield d
        d += timedelta(days=1)


# ------------------------------------------------------------------ the rule
def test_the_live_rule_is_the_schedule_on_every_day_through_2027_01_05():
    for d in days(date(2019, 1, 1), FIRST_LATER - timedelta(days=1)):
        assert serving.LIVE(d) == S26.serving_search(d) and serving.LIVE.record(d) == {}, d
    assert serving.LIVE(date(2026, 7, 7)) == 12 and serving.LIVE(date(2026, 7, 8)) == 13
    assert serving.LIVE(date(2020, 1, 14)) is None                      # before S_0, as CP-26's schedule


def test_from_2027_01_06_every_day_is_s13s_and_its_record_names_decision_33():
    for d in days(FIRST_LATER, date(2040, 12, 31)):
        k = S26.serving_search(d)
        rule = serving.LIVE.record(d)['serving_rule']
        assert k > 13 and serving.LIVE(d) == 13, d
        assert rule == {'search': 13, 'search_day': '2026-07-08', 'scheduled_search': k,
                        'scheduled_search_day': str(S26.search_day(k)), 'decision': 33, 'text': serving.TEXT}, d
    assert S26.serving_search(FIRST_LATER) == 14 and serving.LIVE.record(FIRST_LATER)['serving_rule']['scheduled_search'] == 14


def test_the_rule_over_an_injected_schedule_caps_it_and_a_plain_callable_does_not():
    rule = serving.Rule(lambda d: 14)
    assert rule(date(2026, 8, 31)) == 13 and rule.record(date(2026, 8, 31))['serving_rule']['scheduled_search'] == 14
    assert serving.Rule(lambda d: None)(date(2026, 8, 31)) is None


# ------------------------------------------------------------------ the payload: S_13's pinned state, and no other
def _relabelled(value: dict, k: int) -> dict:
    """S_13's state rewritten, self-consistently, as search k: its day, its member seeds and its digest."""
    out = json.loads(json.dumps(value))
    out.update(k=k, search_day=str(S26.search_day(k)))
    for m, seed in zip(out['members'], S26.member_seeds(k)):
        m['seed'] = seed
    out['content_sha256'] = S26.digest(out)
    return out


@pytest.mark.skipif(not K13.is_file(), reason='the pinned k13.json is absent')
def test_the_payload_takes_s13s_pinned_state_for_a_day_from_2027_01_06_and_as_before_for_earlier_days():
    pinned = json.loads(K13.read_text())
    for day in (date(2026, 8, 31), date(2026, 11, 20), FIRST_LATER, date(2027, 7, 6), date(2031, 3, 1)):
        k, path, value = P.load_ensemble(K13.parent, day)
        assert (k, path.name, value) == (13, 'k13.json', pinned), day
    k, path, value = P.load_ensemble(K13.parent, date(2026, 7, 7))      # S_12's day: unchanged, its file absent here
    assert (k, path.name, value) == (12, 'k12.json', None)
    # why the change is needed: under CP-26's schedule, S_13's state is not the state of a day from 2027-01-06
    with pytest.raises(S26.SearchUnavailable):
        S26.validate_ensemble(pinned, S26.serving_search(FIRST_LATER), 'nominal')


@pytest.mark.skipif(not K13.is_file(), reason='the pinned k13.json is absent')
def test_a_day_served_by_another_state_than_s13s_is_refused_by_the_live_path():
    pinned = json.loads(K13.read_text())
    later = _relabelled(pinned, 14)
    S26.validate_ensemble(later, 14, 'nominal')                         # a well-formed state of search 14
    reseeded = json.loads(json.dumps(pinned))
    reseeded['members'][0]['seed'] += 1
    reseeded['content_sha256'] = S26.digest(reseeded)
    day = date(2027, 3, 1)
    with boundary.live(now=at_noon(day - timedelta(days=1))):
        for other in (later, _relabelled(pinned, 12), reseeded):
            with pytest.raises(S26.SearchUnavailable):
                P.a1_payload(None, day, other)
        with pytest.raises(AttributeError):                             # S_13's own state passes, then needs a context
            P.a1_payload(None, day, pinned)


# ------------------------------------------------------------------ the store: a later search never enters
ORIGIN = date(2027, 1, 5)


def _store(tmp_path):
    repo = make_origin(tmp_path, synthetic_state(ORIGIN), ORIGIN, FIRST_LATER)('a')
    return repo, LiveStore(repo / STORE_PATH)


@pytest.mark.skipif(not K13.is_file(), reason='the pinned k13.json is absent')
def test_a_later_search_state_entered_into_the_store_is_refused_naming_decision_33(tmp_path):
    repo, store = _store(tmp_path)
    later = tmp_path / 'k14.json'
    later.write_text(json.dumps(_relabelled(json.loads(K13.read_text()), 14), indent=2, sort_keys=True) + '\n')
    before = (store.folder / 'ledger.jsonl').read_bytes()
    with pytest.raises(StoreRefused, match='decision 33'):
        store.record_search(14, later, 'S_14 from the Owner\'s M3 (H4)')
    assert (store.folder / 'ledger.jsonl').read_bytes() == before and not (store.folder / 'search').exists()
    # the command line, H4's route
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
    done = subprocess.run([sys.executable, '-m', 'cp18', 'search', '--root', str(repo), '--k', '14', '--file', str(later),
                           '--provenance', 'H4'], capture_output=True, text=True, env=env)
    assert done.returncode == 2 and 'decision 33' in done.stdout + done.stderr
    assert (store.folder / 'ledger.jsonl').read_bytes() == before
    # and a later search's entry written around `record_search` does not verify
    target = store.folder / 'search/k14.json'
    target.parent.mkdir(parents=True)
    target.write_bytes(later.read_bytes())
    from cp17c.store import _sha
    store._append({'kind': 'search', 'k': 14, 'search_file': 'search/k14.json', 'search_file_sha256': _sha(target),
                   'content_sha256': json.loads(later.read_text())['content_sha256'], 'provenance': 'by hand',
                   **store._carry_state()}, store._head_now())
    with pytest.raises(StoreRefused, match='decision 33'):
        LiveStore(store.folder).verify()


# ------------------------------------------------------------------ the pipeline
class Asked(Inputs):
    """CP-18c's stand-in inputs, noting which search's state the pipeline asks for."""

    def __init__(self, search=None):
        super().__init__()
        self.asked, self.search = [], search

    def search_file(self, k):
        self.asked.append(k)
        return self.search or super().search_file(k)


def _run(repo, tmp_path, now, inputs, label, mode, **kw):
    settings = pipeline.Settings(root=repo, project=repo, out=tmp_path / 'out' / label, host_kind='local', mode=mode,
                                 run_label=label)
    return pipeline.run(settings, now, claim=Claim(repo), inputs=inputs, checks=passing_checks(),
                        issue=stand_in_issue(), **kw)


def _issued_record(repo, day) -> dict:
    return json.loads((repo / STORE_PATH / 'issued' / str(day) / 'record.json').read_text())


def test_a_live_day_from_2027_01_06_is_issued_from_s13_and_its_record_names_decision_33(tmp_path):
    repo, _ = _store(tmp_path)
    inputs = Asked()
    with boundary.live(now=at_noon(ORIGIN)):
        record = _run(repo, tmp_path, at_noon(ORIGIN), inputs, 'live', 'live')         # the live rule, by default
    item = record['days'][str(FIRST_LATER)]
    assert record['planned'] == [str(FIRST_LATER)] and item['status'] == 'issued' and record['exit'] == 0
    assert inputs.asked == [13] and inputs.built == [str(FIRST_LATER)]
    issued = _issued_record(repo, FIRST_LATER)
    assert issued['serving_rule'] == item['serving_rule'] == serving.LIVE.record(FIRST_LATER)['serving_rule']
    assert issued['serving_rule']['search'] == 13 and issued['serving_rule']['scheduled_search'] == 14
    LiveStore(repo / STORE_PATH).verify()


def test_control_the_rule_before_decision_33_leaves_a_day_from_2027_01_06_open(tmp_path):
    repo, _ = _store(tmp_path)
    inputs = Asked()
    with boundary.live(now=at_noon(ORIGIN)):
        record = _run(repo, tmp_path, at_noon(ORIGIN), inputs, 'old-rule', 'live', serving=S26.serving_search)
    item = record['days'][str(FIRST_LATER)]
    assert item['status'] == 'open' and item['cause'] == causes.S14 and item['search'] == 14
    assert item['cause_text'] == "S_14's state not in place" and record['exit'] == 1
    assert inputs.asked == [] and inputs.built == []                    # the store holds no later search; nothing built
    assert str(FIRST_LATER) not in LiveStore(repo / STORE_PATH).days()


def _two_origins(tmp_path, day):
    """Two separate origins with the same store, so that neither run sees the other's issuance."""
    out = []
    for name in ('x', 'y'):
        (tmp_path / name).mkdir()
        out.append(make_origin(tmp_path / name, synthetic_state(day - timedelta(days=1)), day - timedelta(days=1),
                               day)('a'))
    return out


def test_on_a_development_day_the_injected_schedule_gives_s14_and_the_day_is_issued_from_s13(tmp_path):
    day = date(2026, 8, 31)
    a, b = _two_origins(tmp_path, day)
    issued = _run(a, tmp_path, at_noon(day - timedelta(days=1)), Asked(), 'd33', 'dry-run',
                  serving=serving.Rule(lambda d: 14 if d == day else S26.serving_search(d)))
    assert issued['days'][str(day)]['status'] == 'issued'
    assert _issued_record(a, day)['serving_rule']['scheduled_search'] == 14
    control = _run(b, tmp_path, at_noon(day - timedelta(days=1)), Asked(), 'control', 'dry-run',
                   serving=lambda d: 14 if d == day else S26.serving_search(d))
    assert control['days'][str(day)]['cause'] == causes.S14 and control['exit'] == 1


def test_nothing_before_2027_01_06_changes_in_the_record(tmp_path):
    """A development day under the live rule against the same day under the rule before decision 33 (the schedule
    itself): the same search asked, and the same record apart from the run's own fields; no `serving_rule`."""
    day = date(2026, 8, 31)
    a, b = _two_origins(tmp_path, day)
    ia, ib = Asked(), Asked()
    ra = _run(a, tmp_path, at_noon(day - timedelta(days=1)), ia, 'live-rule', 'dry-run')
    rb = _run(b, tmp_path, at_noon(day - timedelta(days=1)), ib, 'old-rule', 'dry-run', serving=S26.serving_search)
    assert ia.asked == ib.asked == [13]
    one, two = _issued_record(a, day), _issued_record(b, day)
    assert 'serving_rule' not in one and set(one) == set(two)
    assert {k: v for k, v in one.items() if k not in RUN_FIELDS} == {k: v for k, v in two.items() if k not in RUN_FIELDS}
    strip = ('started_utc', 'seconds')
    assert ({k: v for k, v in ra['days'][str(day)].items() if k not in strip} ==
            {k: v for k, v in rb['days'][str(day)].items() if k not in strip})


def test_no_live_day_carries_s14_when_the_pinned_state_is_absent(tmp_path):
    """The live rule names S_13 only; its pinned state absent is an input the day cannot be built from."""
    repo, _ = _store(tmp_path)
    inputs = Asked(search=tmp_path / 'absent' / 'k13.json')
    with boundary.live(now=at_noon(ORIGIN)):
        record = _run(repo, tmp_path, at_noon(ORIGIN), inputs, 'absent', 'live')
    item = record['days'][str(FIRST_LATER)]
    assert item['status'] == 'open' and item['cause'] == causes.INPUTS and item['search'] == 13
    assert 'pinned' in item['note'] and inputs.built == []


# ------------------------------------------------------------------ the Space
def test_the_space_states_decision_33_where_it_describes_the_daily_refit():
    from cp18.live_claims import build_live_claims, live_record, live_summary
    dev = build_live_claims(ROOT)['values']['live_network_choice']
    live = build_live_claims(ROOT, live=live_summary(live_record(ROOT / 'live')))['values']['live_network_choice']
    assert dev == live
    sentences = [s for s in re.split(r'(?<=[.)])\s+', live) if s]
    assert len(sentences) == 2, sentences
    assert f'every {S26.SEARCH_SPACING_DAYS} days' in live and f"the {S26.search_day(13)} search's choice" in live
    assert "the Owner's decision 33" in live and 'development evaluation' in live
    assert not re.search(r'\b(late|timely)\b', live, re.I)
    main = (ROOT / 'space-product/app/main.js').read_text()
    panel = main[main.index('function renderProduct('):main.index('function forecastRows(')]
    assert panel.index("'Last training'") < panel.index("L('live_network_choice')") < panel.index("'Data refresh'")
