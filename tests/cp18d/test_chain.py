"""The daily operation as a self-dispatching chain (the Orchestrator's ruling O54; `src/cp18/chain.py`).

1. The chain's decisions: the acquisition from 5.5 h before the cutoff until it shows the forecast or reaches the
   cutoff's margin, the run after the cutoff, the retries and their backoffs, a dispatch by hand.
2. A simulation of 60 days of links (dispatch at once, the jobs' own durations): every day is acquired before its
   cutoff and run after it, exactly once each, every job inside GitHub's 6-hour limit.
3. The argument for the chain over the hourly gate, from the probe's measured delays (6 h 11 min to 7 h 36 min on its
   first night, growing): an hourly event through the gate covers any delay up to 12 hours only while events keep
   arriving; when the scheduler drops most of a day's events, days go uncovered. The chain does not wait for the
   scheduler, and any one seed, however late, restarts a broken chain.
4. The seed and the dispatch, with a mocked GitHub API (no network).
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import random

import pytest

from cp18 import chain as C, window as W
from cp25 import guard

UTC = timezone.utc
ROOT = Path(__file__).resolve().parents[2]
DAY = date(2026, 11, 18)                     # its cutoff: 2026-11-17 10:00 UTC (winter)
CUTOFF = datetime(2026, 11, 17, 10, 0, tzinfo=UTC)


def at(h, m=0, day=17):
    return datetime(2026, 11, day, h, m, tzinfo=UTC)


def ran(target, exit_code=0, finished=None, status=None):
    return {'run_id': 'r', 'target_day': str(target), 'exit': exit_code, 'started_utc': None,
            'finished_utc': finished, 'target_status': status or ('issued' if exit_code == 0 else 'open')}


# ------------------------------------------------------------------------------------------------ 1. decisions
def test_before_the_acquisition_start_it_sleeps_until_it_and_never_longer_than_its_limit():
    d = C.decide(at(23, 0, 16), None, [ran(date(2026, 11, 17))])
    assert d['action'] == 'none' and d['sleep_seconds'] == int((at(4, 30) - at(23, 0, 16)).total_seconds())
    far = C.decide(at(11, 0, 16), None, [ran(date(2026, 11, 17))])
    assert far['action'] == 'none' and far['sleep_seconds'] == int(W.MAX_SLEEP_HOURS * 3600)


def test_inside_the_window_it_acquires_and_after_the_forecast_waits_for_the_cutoff():
    assert C.decide(at(4, 30), None, [ran(date(2026, 11, 17))])['action'] == 'acquire'
    shown = {'action': 'acquire', 'day': str(DAY), 'result': 'success', 'shown': True, 'at': '2026-11-17T09:12:00Z'}
    d = C.decide(at(9, 12), shown, [ran(date(2026, 11, 17))])
    assert d['action'] == 'none' and d['sleep_seconds'] == int((CUTOFF + C.RUN_DELAY - at(9, 12)).total_seconds())
    assert C.decide(CUTOFF + C.RUN_DELAY, shown, [ran(date(2026, 11, 17))]) | {} and \
        C.decide(CUTOFF + C.RUN_DELAY, shown, [ran(date(2026, 11, 17))])['action'] == 'run'


def test_an_acquisition_that_reached_its_stop_by_is_continued_and_one_at_the_margin_is_not():
    handed = {'action': 'acquire', 'day': str(DAY), 'result': 'success', 'shown': False, 'stopped': 'its stop-by',
              'at': '2026-11-17T09:40:00Z'}
    assert C.decide(at(9, 41), handed, [ran(date(2026, 11, 17))])['action'] == 'acquire'
    margin = dict(handed, stopped='margin')
    assert C.decide(at(9, 58), margin, [ran(date(2026, 11, 17))])['action'] == 'none'
    failed = dict(handed, result='failure')
    assert C.decide(at(9, 45), failed, [ran(date(2026, 11, 17))])['action'] == 'none'            # backoff
    assert C.decide(at(9, 50), failed, [ran(date(2026, 11, 17))])['action'] == 'acquire'


def test_the_run_and_its_retries():
    target = date(2026, 11, 18)
    assert C.decide(CUTOFF + C.RUN_DELAY, None, [ran(date(2026, 11, 17))])['action'] == 'run'
    open_once = [ran(target, 1, '2026-11-17T10:30:00Z')]
    assert C.decide(at(12, 0), None, open_once)['action'] == 'none'                              # 3 h after it
    assert C.decide(at(13, 31), None, open_once)['action'] == 'run'
    thrice = [ran(target, 1, f'2026-11-17T{h}:30:00Z') for h in (10, 13, 16)]
    assert C.decide(at(20, 0), None, thrice)['action'] == 'none'                                 # at most three
    assert C.decide(at(20, 0), None, [ran(target, 0, '2026-11-17T10:30:00Z')])['action'] == 'none'
    # the target day issued while an older day of the lookback stays open: exit 1, and the run is still done
    assert C.decide(at(13, 31), None, [ran(target, 1, '2026-11-17T10:30:00Z', 'issued')])['action'] == 'none'
    failed = {'action': 'run', 'day': str(target), 'result': 'failure', 'at': '2026-11-17T10:20:00Z'}
    assert C.decide(at(11, 0), failed, [])['action'] == 'none'                                   # 2 h backoff
    assert C.decide(at(12, 21), failed, [])['action'] == 'run'


def test_a_dispatch_by_hand_acts_at_once():
    assert C.decide(at(15, 0), None, [], force='run') | {} and C.decide(at(15, 0), None, [], force='run')['action'] == 'run'
    assert C.decide(at(15, 0), None, [], force='acquire')['day'] == '2026-11-19'


def test_the_tick_reads_the_stores_run_records_on_main():
    runs = C.runs_on_main(ROOT / 'live/store')
    assert runs and all(set(r) == {'run_id', 'target_day', 'exit', 'target_status', 'started_utc', 'finished_utc'}
                        for r in runs)
    assert C.target_day(datetime(2026, 11, 15, 10, 30, tzinfo=UTC)) == date(2026, 11, 16)
    assert C.target_day(datetime(2026, 11, 15, 9, 59, tzinfo=UTC)) == date(2026, 11, 15)


# ------------------------------------------------------------------------------------------------ 2. the simulation
def simulate(first: date, days: int, publish=timedelta(minutes=63), dispatch_seconds=20, seed=7):
    """Links of the chain from a seed at noon before `first`'s cutoff day, each started `dispatch_seconds` after the
    last one ended. The acquisition sees the forecast `publish` before the cutoff (09:03 UTC in winter by default),
    takes 8 min of setup, and polls every 5 min; the run takes 20 min and issues its target day."""
    rng = random.Random(seed)
    now = W.cutoff(first) - timedelta(hours=22)
    last, runs, log = None, [], []
    acquired, issued = {}, {}
    end = W.cutoff(first + timedelta(days=days))
    while now < end:
        d = C.decide(now, last, runs)
        tick = timedelta(seconds=d['sleep_seconds'])
        if d['sleep_seconds']:
            d2 = C.decide(now + tick, last, runs)
            d = d2 if d2['sleep_seconds'] == 0 else dict(d2, action='none')
        start = now + tick
        assert tick <= timedelta(hours=W.MAX_SLEEP_HOURS)
        if d['action'] == 'acquire':
            day = date.fromisoformat(d['day'])
            cutoff = W.cutoff(day)
            begin = start + timedelta(minutes=8)
            seen = cutoff - publish
            stop_by = start + timedelta(minutes=340)
            if begin >= seen:
                finish, shown, stopped = begin, True, 'shown'
            else:
                polls = (seen - begin) // timedelta(minutes=5) + 1
                finish = begin + polls * timedelta(minutes=5)
                shown, stopped = finish <= min(stop_by, cutoff - timedelta(minutes=2)), 'shown'
                if not shown:
                    finish, stopped = min(stop_by, cutoff - timedelta(minutes=2)), (
                        'its stop-by' if stop_by < cutoff - timedelta(minutes=2) else 'margin')
            assert finish - start <= timedelta(hours=6)
            acquired.setdefault(d['day'], []).append(shown)
            last = {'action': 'acquire', 'day': d['day'], 'result': 'success', 'shown': shown, 'stopped': stopped,
                    'at': C._z(finish)}
            now = finish
        elif d['action'] == 'run':
            finish = start + timedelta(minutes=20)
            runs.append(ran(d['day'], 0, C._z(finish)))
            issued[d['day']] = issued.get(d['day'], 0) + 1
            last = {'action': 'run', 'day': d['day'], 'result': 'success', 'at': C._z(finish)}
            now = finish
        else:
            now = start
        log.append((start, d['action'], d['day']))
        now += timedelta(seconds=dispatch_seconds + rng.randint(0, 40))
    return acquired, issued, log


@pytest.mark.parametrize('first', [date(2026, 11, 18), date(2027, 3, 20), date(2027, 6, 1), date(2027, 10, 25)])
def test_sixty_days_of_links_acquire_each_day_before_its_cutoff_and_issue_it_once(first):
    summer = guard.issue_time(first).astimezone(UTC).hour == 9
    acquired, issued, log = simulate(first, 60, publish=timedelta(minutes=57 if not summer else 52))
    for k in range(60):
        day = str(first + timedelta(days=k))
        assert acquired.get(day) == [True], (day, acquired.get(day))       # one acquisition, the forecast shown
        assert issued.get(day) == 1, day                                     # one run, after its cutoff
    runs = [t for t, a, d in log if a == 'run']
    for t, a, d in log:
        if a == 'run':
            assert t >= W.cutoff(date.fromisoformat(d))
        if a == 'acquire':
            assert t < W.cutoff(date.fromisoformat(d))
    assert len(log) / 60 < 12                                                # about 7 links a day


def test_a_forecast_published_after_the_margin_leaves_the_day_to_the_copy_after_the_cutoff_and_the_run_issues_it():
    acquired, issued, _ = simulate(date(2026, 11, 18), 3, publish=timedelta(minutes=-30))   # 10:30, after the cutoff
    for k in range(3):
        day = str(date(2026, 11, 18) + timedelta(days=k))
        assert acquired[day][-1] is False and issued[day] == 1


# ------------------------------------------------------------------------------------------------ 3. the argument
#: The probe's first night (cron hour UTC → the run's creation): 6 h 11 min to 7 h 36 min late, growing.
PROBE = {0: (6, 11), 1: (6, 37), 2: (7, 6), 3: (7, 36)}


def gate_covers(arrivals: list[datetime], day: date) -> bool:
    """Whether some event through the hourly gate starts `day`'s acquisition in time."""
    for t in arrivals:
        p = W.plan(t)
        if p['go'] and p['day'] == str(day):
            return True
    return False


def hourly_arrivals(day: date, delay, keep=lambda k: True) -> list[datetime]:
    start = datetime.combine(day - timedelta(days=3), datetime.min.time(), tzinfo=UTC)
    return [start + timedelta(hours=k, minutes=20) + delay(k) for k in range(96) if keep(k)]


def test_the_gate_covers_the_probes_delays_and_any_delay_up_to_12_hours_while_events_keep_coming():
    measured = [timedelta(hours=h, minutes=m) for h, m in PROBE.values()]
    growth = (measured[-1] - measured[0]) / 3                                 # about 28 min an hour
    for day in (date(2026, 11, 18), date(2027, 7, 1)):
        # the probe's delay, growing as measured, capped at 12 hours
        assert gate_covers(hourly_arrivals(day, lambda k: min(measured[0] + growth * (k % 24), timedelta(hours=12))), day)
        for hours in (0, 3, 6, 7.6, 9, 12):
            assert gate_covers(hourly_arrivals(day, lambda k: timedelta(hours=hours)), day), hours


def test_the_gate_alone_leaves_days_uncovered_when_most_events_are_dropped_so_the_chain_is_chosen():
    rng = random.Random(31)
    days = [date(2026, 11, 18) + timedelta(days=k) for k in range(200)]
    uncovered = 0
    for day in days:
        kept = {k for k in range(96) if rng.random() < 0.15}                 # 85 % of the events dropped
        if not gate_covers(hourly_arrivals(day, lambda k: timedelta(hours=7), lambda k: k in kept), day):
            uncovered += 1
    assert uncovered > 10                                                    # whole days lost: not robust enough
    # the chain: a seed only restarts a broken chain; with the same drops, one surviving seed in a day suffices,
    # and the chain then acquires and runs every day without the scheduler (the simulation above)
    seeds_per_day = [sum(1 for k in range(24) if rng.random() < 0.15) for _ in range(200)]
    assert sum(1 for n in seeds_per_day if n == 0) < uncovered


# ------------------------------------------------------------------------------------------------ 4. the API
class FakeApi:
    def __init__(self, runs=(), fail=0):
        self.runs, self.fail, self.calls = list(runs), fail, []

    def request(self, method, path, body=None):
        self.calls.append((method, path, body))
        if method == 'GET':
            return {'workflow_runs': self.runs}
        if self.fail:
            self.fail -= 1
            raise RuntimeError('GitHub API POST: HTTP 502')
        return None


def run_item(i, status, title):
    return {'id': i, 'status': status, 'display_title': title}


def test_a_seed_starts_a_chain_only_when_none_is_alive():
    api = FakeApi([run_item(1, 'completed', 'daily chain'), run_item(2, 'in_progress', 'daily dry-run')])
    value = C.seed(api)
    assert value['seeded'] and value['dispatched']
    (post,) = [c for c in api.calls if c[0] == 'POST']
    assert post[1] == 'actions/workflows/daily.yml/dispatches'
    assert post[2]['ref'] == 'main' and post[2]['inputs']['mode'] == 'chain'
    for status in C.PENDING:
        for title in ('daily chain', 'daily live', 'daily acquire-live'):
            api = FakeApi([run_item(3, status, title)])
            assert not C.seed(api)['seeded'] and not [c for c in api.calls if c[0] == 'POST']
    get = FakeApi().calls
    C.alive(api := FakeApi())
    assert api.calls == [('GET', 'actions/workflows/daily.yml/runs?event=workflow_dispatch&per_page=100', None)]


def test_the_next_link_is_dispatched_once_with_this_links_state_and_retried():
    api = FakeApi(fail=2)
    waits = []
    value = C.dispatch(api, {'action': 'run', 'day': '2026-11-18', 'result': 'success'}, sleep=waits.append)
    assert value == {'dispatched': True, 'attempts': 3, 'errors': ['GitHub API POST: HTTP 502'] * 2}
    assert waits == [30, 60]
    body = [c for c in api.calls if c[0] == 'POST'][-1][2]
    assert json.loads(body['inputs']['last']) == {'action': 'run', 'day': '2026-11-18', 'result': 'success'}
    assert C.dispatch(FakeApi(fail=5), {}, sleep=lambda s: None)['dispatched'] is False


def test_the_token_is_read_from_the_environment_and_never_part_of_any_output(monkeypatch):
    monkeypatch.delenv('GH_TOKEN', raising=False)
    with pytest.raises(RuntimeError, match='no GH_TOKEN'):
        C.Api('o/r').request('GET', 'actions/workflows/daily.yml/runs')


def test_the_chain_and_the_gate_run_without_the_projects_environment():
    import subprocess
    import sys
    done = subprocess.run([sys.executable, '-I', str(ROOT / 'src/cp18/chain.py'), 'tick', '--store',
                           str(ROOT / 'live/store'), '--now', '2026-11-14T23:00:00Z'],
                          capture_output=True, text=True, cwd='/', env={})
    assert done.returncode == 0, done.stderr
    out = dict(line.split('=', 1) for line in done.stdout.strip().splitlines())
    assert out['action'] == 'none' and out['target_day'] == '2026-11-15'
    assert json.loads(out['state'])['now_utc'] == '2026-11-14T23:00:00Z'


def test_only_the_workflows_declared_inputs_are_dispatched():
    """The scratch rehearsal's finding (run 43735265261): an undeclared input (`links`) made GitHub answer 422."""
    import yaml
    declared = set(yaml.safe_load((ROOT / '.github/workflows/daily.yml').read_text())
                   .get('on', {}).get('workflow_dispatch', {}).get('inputs', {}) or
                   yaml.safe_load((ROOT / '.github/workflows/daily.yml').read_text())[True]['workflow_dispatch']['inputs'])
    for state, mode in (({'action': 'run'}, 'chain'), ('2', 'chain-dry-run')):
        api = FakeApi()
        C.dispatch(api, state, mode=mode, sleep=lambda s: None)
        (post,) = [c for c in api.calls if c[0] == 'POST']
        assert set(post[2]['inputs']) <= declared and post[2]['inputs']['mode'] == mode
    assert [c for c in FakeApi().calls] == []
    api = FakeApi()
    C.dispatch(api, '2', mode='chain-dry-run', sleep=lambda s: None)
    assert api.calls[-1][2]['inputs'] == {'mode': 'chain-dry-run', 'last': '2'}
