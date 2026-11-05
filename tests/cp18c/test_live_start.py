"""The live start (r20 §24.14 item 4), N5, and the bridge-day edge (CP-18c items 3, 9, 11).

- The live store's genesis at the freeze origin, carried to the first live day: the days between are outside the record
  and are never planned, issued or closed; a carry anywhere else is refused, and a store whose carry was moved fails.
- N5: an exception in a day's acquisition or build becomes that day's recorded cause (a live day's inputs that cannot
  be shown to precede its cutoff), never an escaped run; the run's record is still published.
- The 31-December Monday bridge-day edge fails closed, as not issued with its cause.
"""
from __future__ import annotations

from datetime import date, timedelta
import json

import pytest

from cp17.shadow import ShadowStates
from cp18 import boundary, causes
from cp18.live import build as B
from cp18.store import STORE_PATH, LiveStore, StoreRefused

from cp18c.support18c import FREEZE_STATE, Inputs, at_noon, make_origin, run, synthetic_state

ORIGIN, FIRST = date(2026, 9, 6), date(2026, 9, 7)


def test_the_genesis_at_the_freeze_origin_is_carried_to_the_first_live_day(tmp_path):
    if not FREEZE_STATE.is_file():
        pytest.skip('live/pinned is absent in this checkout (the freeze-origin state is committed there)')
    state = ShadowStates.from_dict(json.loads(FREEZE_STATE.read_text()))
    store = LiveStore.init(tmp_path / 'store', state, ORIGIN, 'freeze origin', FIRST)
    assert store.last_closed() is None
    with pytest.raises(StoreRefused):
        store.record_carry(date(2026, 9, 5), date(2026, 11, 3), 'not at the origin')
    with pytest.raises(StoreRefused):
        store.record_carry(ORIGIN, ORIGIN, 'not forward')
    store.record_carry(ORIGIN, date(2026, 11, 3), 'decision 28')
    head = store.verify()
    days = store.days()
    assert min(days) == str(FIRST) and max(days) == '2026-11-02' and len(days) == 57
    assert all(v['status'] == 'outside' and v['note'] == 'decision 28' for v in days.values())
    assert store.last_closed() == date(2026, 11, 2)
    s, _ = store.state()
    assert s.digest() == state.digest()                       # the freeze-origin states are carried unchanged
    assert head['last_day'] is None


def test_a_carry_moved_off_the_genesis_origin_fails_verification(tmp_path):
    store = LiveStore.init(tmp_path / 'store', synthetic_state(ORIGIN), ORIGIN, 'synthetic', FIRST)
    store.record_carry(ORIGIN, date(2026, 11, 3), 'decision 28')
    ledger = (store.folder / 'ledger.jsonl').read_text().splitlines()
    entry = json.loads(ledger[-1])
    entry['last_window_day'] = '2026-09-10'
    from cp17c.store import _canonical, _sha_bytes
    body = {k: v for k, v in entry.items() if k != 'entry_sha256'}
    entry['entry_sha256'] = _sha_bytes(_canonical(body))
    ledger[-1] = json.dumps(entry, sort_keys=True)
    (store.folder / 'ledger.jsonl').write_text('\n'.join(ledger) + '\n')
    with pytest.raises(StoreRefused):
        LiveStore(store.folder).verify()


def test_after_the_carry_the_first_run_plans_the_catch_up_and_never_an_outside_day(tmp_path):
    checkout = make_origin(tmp_path, synthetic_state(ORIGIN), ORIGIN, FIRST, carry_to=date(2026, 11, 3))
    repo = checkout('a')
    with boundary.live(now=at_noon(date(2026, 11, 5))):
        record = run(repo, tmp_path, at_noon(date(2026, 11, 5)), Inputs(hidden=['2026-11-03', '2026-11-04', '2026-11-05']),
                     mode='live')
    assert record['boundary']['mode'] == 'live'
    assert record['target_day'] == '2026-11-06' and record['planned'] == ['2026-11-03', '2026-11-04', '2026-11-05',
                                                                          '2026-11-06']
    assert record['closed'] == [] or all(c['day'] >= '2026-11-03' for c in record['closed'])
    days = LiveStore(repo / STORE_PATH).days()
    assert days['2026-11-06']['status'] == 'issued'
    for d in ('2026-11-03', '2026-11-04', '2026-11-05'):
        assert days[d]['status'] == 'not issued' and days[d]['cause'] == causes.INPUTS
    assert days['2026-11-02']['status'] == 'outside'


def test_n5_an_exception_in_acquisition_or_build_is_a_recorded_cause_never_an_escaped_run(tmp_path):
    checkout = make_origin(tmp_path, synthetic_state(ORIGIN), ORIGIN, FIRST, carry_to=date(2026, 11, 3))
    repo = checkout('a')
    inputs = Inputs(raising=['2026-11-04'], truth_raising=['2026-11-05'])
    with boundary.live(now=at_noon(date(2026, 11, 5))):
        record = run(repo, tmp_path, at_noon(date(2026, 11, 5)), inputs, mode='live')
    assert record['exit'] in (0, 1) and 'outcome' in record
    assert 'TimeoutError' in record['days']['2026-11-04']['error']
    assert 'ConnectionError' in record['days']['2026-11-05']['error']
    days = LiveStore(repo / STORE_PATH).days()
    assert days['2026-11-04']['cause'] == causes.INPUTS and days['2026-11-05']['cause'] == causes.INPUTS
    assert days['2026-11-06']['status'] == 'issued'
    assert len(LiveStore(repo / STORE_PATH).runs()) == 1                        # the run's record is published
    from cp18.claim import Claim
    assert not Claim(repo).git('status', '--porcelain').stdout.strip()          # nothing left uncommitted


def test_the_31_december_monday_bridge_day_edge_fails_closed():
    assert [d for d in (date(2029, 12, 31), date(2035, 12, 31))] and all(
        B.bridge_day_edge(d) for d in (date(2029, 12, 31), date(2035, 12, 31)))
    assert not any(B.bridge_day_edge(date(y, 12, 31)) for y in range(2026, 2029))
    assert not B.bridge_day_edge(date(2029, 12, 30))
    day = date(2029, 12, 31)
    with boundary.live(now=at_noon(day - timedelta(days=1))):
        result = B.build_day(day, archive='/nonexistent', base_end=date(2026, 9, 6), buffers={}, search_dir='/x',
                             out='/x', root='/x')
    assert result['status'] == 'failed' and result['cause'] == B.BRIDGE_DAY_EDGE and not result['payloads']


def test_the_bridge_day_edge_is_recorded_as_not_issued_with_its_cause(tmp_path):
    from cp18.live_inputs import LiveInputs

    class Edge(LiveInputs):
        def __init__(self):
            pass

        def acquire(self, day):
            pass

    inputs = Edge()
    inputs.root = inputs.project = tmp_path
    inputs.base_end, inputs.transport, inputs.acquisitions = date(2026, 9, 6), object(), []
    with boundary.live(now=at_noon(date(2029, 12, 30))):
        out = inputs.build(date(2029, 12, 31), buffers={}, search_file=tmp_path / 'k13.json', out=tmp_path / 'p')
    assert out['shown'] is False and out['build_status'] == 'failed' and out['reasons'] == [B.BRIDGE_DAY_EDGE]
