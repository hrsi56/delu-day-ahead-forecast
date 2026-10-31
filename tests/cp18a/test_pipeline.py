"""The pipeline's rules, on synthetic states and a stand-in issuance (no Pyodide, no local inputs, no network).

Each test builds a bare repository standing in for the product's `origin`, one or two checkouts of it with their own
`.githooks`, and a store whose genesis is a synthetic state. The issuance is `cp17.issue`'s own artifact and verifier
around a fixed forecast, so everything the pipeline decides (the plan, the claim, the causes, the store) is real.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess

import numpy as np
import pytest

from cp17 import issue as cp17issue
from cp17.dailyfit import array_hash
from cp17.shadow import ShadowStates
from cp18 import causes, pipeline, plan
from cp18.claim import Claim, ClaimError
from cp18.store import STORE_PATH, LiveStore, StoreRefused
from cp25 import guard

FIRST = date(2026, 8, 24)
BERLIN = guard.BERLIN


def at_noon(day: date) -> datetime:
    """Noon in Berlin on `day`: the target day is the day after."""
    return datetime(day.year, day.month, day.day, 12, 0, tzinfo=BERLIN)


def synthetic_state(origin: date) -> ShadowStates:
    rng = np.random.default_rng(7)
    days = [origin - timedelta(days=2 + i) for i in range(28)][::-1]
    buffers = {p: [{'day': str(d), 'errors': rng.normal(size=24).round(6).tolist()} for d in days] for p in ('v4', 'v2', 'B0')}
    return ShadowStates.from_buffers(origin, buffers)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, check=True).stdout.strip()


@pytest.fixture
def origin(tmp_path):
    """A bare `origin` whose main holds a store at FIRST, and a function giving a fresh checkout of it."""
    bare = tmp_path / 'origin.git'
    subprocess.run(['git', 'init', '--quiet', '--bare', '-b', 'main', str(bare)], check=True)
    seed = tmp_path / 'seed'
    subprocess.run(['git', 'init', '--quiet', '-b', 'main', str(seed)], check=True)
    hooks = seed / '.githooks'
    hooks.mkdir()
    for name in ('pre-commit', 'commit-msg', 'pre-push'):
        (hooks / name).write_text('#!/bin/sh\nexit 0\n')
        (hooks / name).chmod(0o755)
    LiveStore.init(seed / STORE_PATH, synthetic_state(FIRST), FIRST, 'synthetic test state', FIRST)
    env = {'GIT_AUTHOR_NAME': 't', 'GIT_AUTHOR_EMAIL': 't@t', 'GIT_COMMITTER_NAME': 't', 'GIT_COMMITTER_EMAIL': 't@t'}
    for args in (['add', '-A'], ['commit', '--quiet', '-m', 'seed'], ['push', '--quiet', str(bare), 'HEAD:refs/heads/main']):
        subprocess.run(['git', '-C', str(seed), *args], check=True, env={**__import__('os').environ, **env})

    def checkout(name: str) -> Path:
        path = tmp_path / name
        subprocess.run(['git', 'clone', '--quiet', str(bare), str(path)], check=True)
        git(path, 'config', 'core.hooksPath', '.githooks')
        return path
    return checkout


class Inputs:
    """Shown inputs, except the days named in `hidden`; truth is NaN (no shadow is registered here)."""

    def __init__(self, hidden=()):
        self.hidden, self.built = {str(d) for d in hidden}, []

    def truth(self, day):
        return lambda keys: np.full(len(keys), np.nan)

    def search_file(self, k):
        return Path(__file__)                   # any existing file stands for the pinned S_13

    def build(self, day, *, buffers, search_file, out):
        self.built.append(str(day))
        assert set(buffers) == {'v4', 'v2', 'B0'} and all(len(b) == 28 for b in buffers.values())
        shown = str(day) not in self.hidden
        return {'payloads': str(out), 'gfs_available': True, 'shown': shown,
                'reasons': [] if shown else ['the load forecast was retrieved after the cutoff'],
                'data_refresh_utc': '', 'availability': []}


def stand_in_issue(fail=()):
    """`cp17.issue`'s own artifact around a fixed B0 forecast; a failed issuance for the days in `fail`."""
    fail = {str(d) for d in fail}

    def issue(day, gfs_available, payloads, *, settings, parent_sha256, data_refresh_utc, states):
        keys = cp17issue.canonical_hours(day)
        if str(day) in fail:
            attempts = [{'policy': p, 'status': 'failed', 'cause': 'stand-in failure'} for p in ('A1', 'v4', 'v2', 'B0')]
            decision = {'day': str(day), 'issued_policy': None, 'route': 'a1_failed', 'attempts': attempts,
                        'display': 'failed issuance'}
        else:
            q = np.sort(np.linspace(-1, 1, 7)[None, :] + np.arange(len(keys))[:, None], axis=1)
            result = {'policy': 'B0', 'index': keys, 'quantiles': q.tolist(), 'quantiles_sha256': array_hash(q),
                      'source_day': str(day - timedelta(days=1))}
            attempts = [{'policy': 'B0', 'status': 'ok', 'result': result,
                         'resources': {'wall_seconds': 1.0, 'peak_bytes': 1}}]
            decision = {'day': str(day), 'issued_policy': 'B0', 'route': 'a1_failed', 'attempts': attempts,
                        'display': 'stand-in issuance'}
        art = cp17issue.artifact(decision, identity={'policy_identity_sha256': '0' * 64, 'package_sha256': '0' * 64},
                                 payloads={}, parent_sha256=parent_sha256, data_refresh_utc=data_refresh_utc,
                                 host={'runtime': 'stand-in'})
        assert cp17issue.verify_artifact(art) == []
        decision['artifact'] = art
        return {'artifact': art, 'decision': decision, 'shadows': {}, 'process_seconds': {}, 'process_seconds_sum': 0.0,
                'total_seconds': 0.0, 'blocked_non_local_requests': []}
    return issue


def passing_checks():
    ok = {'passed': True, 'problems': []}
    return {name: (lambda name=name: {'check': name, **ok}) for name in ('pins', 'binary', 'machine', 'canary')}


def failing_checks(at='machine'):
    checks = passing_checks()
    checks[at] = lambda: {'check': at, 'passed': False, 'problems': ['forced']}
    return checks


def run(repo, tmp_path, now, inputs=None, checks=None, issue=None, serving=None, label=None):
    settings = pipeline.Settings(root=repo, project=repo, out=tmp_path / 'out' / (label or 'r'), host_kind='runner',
                                 run_label=label or '')
    return pipeline.run(settings, now, claim=Claim(repo), inputs=inputs or Inputs(), checks=checks or passing_checks(),
                        issue=issue or stand_in_issue(), serving=serving or (lambda d: 13))


def store_of(checkout_fn, name='verify'):
    repo = checkout_fn(name)
    return LiveStore(repo / STORE_PATH)


# ---- the plan ------------------------------------------------------------------------------------------------------

def test_target_day_turns_at_the_cutoff_including_dst_days():
    for day in (date(2026, 3, 29), date(2026, 10, 25), date(2026, 7, 1), date(2026, 1, 15)):
        cut = plan.cutoff(day)
        assert cut == guard.issue_time(day)
        assert plan.target_day(cut) == day
        assert plan.target_day(cut - timedelta(seconds=1)) == day - timedelta(days=1)
    with pytest.raises(ValueError):
        plan.target_day(datetime(2026, 8, 1, 12))


def test_catch_up_is_three_days_then_the_target_at_most_four_oldest_first():
    target = date(2026, 9, 1)
    assert plan.lookback(target) == [date(2026, 8, 29), date(2026, 8, 30), date(2026, 8, 31)]
    assert plan.plan(target, first_day=FIRST, done=set(), last_closed=None) == \
        [date(2026, 8, 29), date(2026, 8, 30), date(2026, 8, 31), target]
    assert plan.plan(target, first_day=FIRST, done={'2026-08-30'}, last_closed=date(2026, 8, 30)) == \
        [date(2026, 8, 31), target]
    assert plan.to_close(target, first_day=FIRST, done=set(), last_closed=None) == \
        [FIRST + timedelta(days=i) for i in range(5)]                                     # 08-24 .. 08-28
    assert plan.plan(date(2026, 8, 25), first_day=FIRST, done=set(), last_closed=None) == [FIRST, date(2026, 8, 25)]


def test_the_red_line_refuses_the_whole_plan_and_names_no_day(origin, tmp_path):
    repo = origin('a')
    before = git(repo, 'rev-parse', 'HEAD')
    late = guard.BOUNDARY + timedelta(days=1)
    with pytest.raises(guard.BoundaryRefused):
        plan.admit([guard.BOUNDARY, late])
    record = run(repo, tmp_path, at_noon(guard.BOUNDARY))         # the target day is the day after the boundary
    assert record['exit'] == 3 and record['outcome'] == pipeline.RED_LINE
    assert record['target_day'] is None and record['planned'] == [] and record['days'] == {}
    assert str(late) not in json.dumps(record)
    assert git(repo, 'rev-parse', 'HEAD') == before and not git(repo, 'status', '--porcelain')


# ---- one run, the catch-up and the causes ---------------------------------------------------------------------------

def test_one_issuance_then_a_catch_up_run_of_four_with_a_day_closed_for_no_run(origin, tmp_path):
    repo = origin('a')
    first = run(repo, tmp_path, at_noon(FIRST - timedelta(days=1)), label='r1')
    assert first['exit'] == 0 and first['planned'] == [str(FIRST)]
    assert first['days'][str(FIRST)]['status'] == 'issued'
    second = run(repo, tmp_path, at_noon(date(2026, 8, 28)), label='r2')      # target 08-29, lookback 08-26..08-28
    assert second['planned'] == ['2026-08-26', '2026-08-27', '2026-08-28', '2026-08-29']
    assert [c['day'] for c in second['closed']] == ['2026-08-25']
    assert second['closed'][0]['cause'] == causes.NO_RUN and second['closed'][0]['attempts'] == []
    store = store_of(origin)
    days = store.days()
    assert [d for d, v in days.items() if v['status'] == 'issued'] == \
        ['2026-08-24', '2026-08-26', '2026-08-27', '2026-08-28', '2026-08-29']
    assert days['2026-08-25'] == {'status': 'not issued', 'policy': None, 'cause': causes.NO_RUN, 'attempts': []}
    assert [r['run_id'] for r in store.runs()] == ['r1', 'r2']
    # each issuance's parent is the artifact before it, and its record keeps the run's own times
    entries = [e for e in store.entries() if e['kind'] == 'issuance']
    assert all(e['parent_artifact_sha256'] == p['artifact_sha256'] for p, e in zip(entries, entries[1:]))
    record = json.loads((store.folder / 'issued/2026-08-27/record.json').read_text())
    assert record['run_id'] == 'r2' and record['issuance_started_utc'] and record['cutoff_utc'] == plan.cutoff(date(2026, 8, 27)).isoformat()


def test_a_failed_h2_check_issues_nothing_and_its_cause_closes_the_day(origin, tmp_path):
    repo = origin('a')
    failed = run(repo, tmp_path, at_noon(FIRST - timedelta(days=1)), checks=failing_checks('machine'), label='h2')
    assert failed['gate']['failed'] == 'machine' and failed['gate']['not_run'] == ['canary']
    assert failed['days'][str(FIRST)] == {'status': 'open', 'cause': causes.H2, 'cause_text': causes.text(causes.H2),
                                          'check': 'machine'}
    store = store_of(origin, 'v1')
    assert [e['kind'] for e in store.entries()] == ['genesis', 'run']        # nothing issued, the run recorded
    later = run(repo, tmp_path, at_noon(date(2026, 8, 27)), label='later')    # 08-24 has left the lookback
    closed = {c['day']: c for c in later['closed']}
    assert list(closed) == [str(FIRST)]
    assert closed[str(FIRST)]['cause'] == causes.H2 and closed[str(FIRST)]['attempts'] == ['h2']
    assert failed['exit'] == 1 and later['exit'] == 0


def test_inputs_not_shown_leave_the_day_open_and_a_later_issuance_closes_it(origin, tmp_path):
    repo = origin('a')
    hidden = Inputs(hidden=[date(2026, 8, 25)])
    record = run(repo, tmp_path, at_noon(date(2026, 8, 25)), inputs=hidden, label='inp')    # plan 08-24 .. 08-26
    assert record['planned'] == ['2026-08-24', '2026-08-25', '2026-08-26']
    assert record['days']['2026-08-25']['status'] == 'open' and record['days']['2026-08-25']['cause'] == causes.INPUTS
    assert [c['day'] for c in record['closed']] == ['2026-08-25']            # closed before 08-26 was issued
    days = store_of(origin).days()
    assert days['2026-08-25']['cause'] == causes.INPUTS and days['2026-08-26']['status'] == 'issued'


def test_s14_not_in_place_leaves_the_day_open(origin, tmp_path):
    repo = origin('a')
    record = run(repo, tmp_path, at_noon(FIRST - timedelta(days=1)), serving=lambda d: 14, label='s14')
    item = record['days'][str(FIRST)]
    assert item['status'] == 'open' and item['cause'] == causes.S14 and item['search'] == 14
    assert record['exit'] == 1 and record['outcome'] == f'done; not issued: {FIRST}'


def test_a_failed_chain_is_the_days_record_and_closes_it_at_once(origin, tmp_path):
    repo = origin('a')
    record = run(repo, tmp_path, at_noon(FIRST - timedelta(days=1)), issue=stand_in_issue(fail=[FIRST]), label='chain')
    assert record['days'][str(FIRST)]['status'] == 'not issued' and record['days'][str(FIRST)]['cause'] == causes.CHAIN
    days = store_of(origin).days()
    assert days[str(FIRST)]['status'] == 'not issued' and days[str(FIRST)]['cause'] == causes.CHAIN
    again = run(repo, tmp_path, at_noon(FIRST - timedelta(days=1)), label='again')      # never retried
    assert again['planned'] == [] and again['outcome'] == 'nothing to issue'


def test_every_cause_is_one_of_the_five():
    assert set(causes.TEXT) == set(causes.ORDER) and len(causes.ORDER) == 5
    with pytest.raises(ValueError):
        causes.text('late')


# ---- the claim -------------------------------------------------------------------------------------------------------

def test_the_push_race_loser_discards_its_own_issuance(origin, tmp_path):
    runner, local = origin('runner'), origin('local')
    winner = {}

    def racing_issue(*args, **kwargs):
        # While the local fallback is issuing, the runner issues the same day and pushes first.
        winner['record'] = run(runner, tmp_path, at_noon(FIRST - timedelta(days=1)), label='runner')
        return stand_in_issue()(*args, **kwargs)
    loser = run(local, tmp_path, at_noon(FIRST - timedelta(days=1)), issue=racing_issue, label='local')
    assert winner['record']['days'][str(FIRST)]['status'] == 'issued'
    assert loser['days'][str(FIRST)]['status'] == 'lost the claim'
    assert loser['outcome'].startswith('lost the claim') and loser['exit'] == 0
    store = store_of(origin)
    issued = [e for e in store.entries() if e['kind'] == 'issuance']
    assert len(issued) == 1 and issued[0]['artifact_sha256'] == winner['record']['days'][str(FIRST)]['artifact_sha256']
    assert [r['run_id'] for r in store.runs()] == ['runner']
    assert git(local, 'rev-parse', 'HEAD') == git(runner, 'rev-parse', 'HEAD')         # the loser is on the winner's main
    assert not git(local, 'status', '--porcelain')


def test_a_day_decided_elsewhere_is_never_issued_again(origin, tmp_path):
    runner, local = origin('runner'), origin('local')
    assert run(runner, tmp_path, at_noon(FIRST - timedelta(days=1)), label='runner')['exit'] == 0
    record = run(local, tmp_path, at_noon(FIRST - timedelta(days=1)), label='local')    # fetches first: nothing to do
    assert record['planned'] == [] and record['outcome'] == 'nothing to issue'
    assert len([e for e in store_of(origin).entries() if e['kind'] == 'issuance']) == 1


def test_publication_needs_the_repositorys_hooks_and_a_clean_synchronized_tree(origin, tmp_path):
    repo = origin('a')
    git(repo, 'config', 'core.hooksPath', '/dev/null')
    claim = Claim(repo)
    claim.sync()
    (repo / 'x.txt').write_text('x')
    with pytest.raises(ClaimError, match='hooksPath'):
        claim.publish(['x.txt'], 'x')
    with pytest.raises(ClaimError, match='uncommitted'):
        claim.sync()


def test_a_guard_refusal_is_not_a_lost_race_and_publishes_nothing(origin, tmp_path):
    repo = origin('a')
    marker = tmp_path / 'block-pushes'
    hook = repo / '.githooks' / 'pre-push'
    hook.write_text(f'#!/bin/sh\nif [ -f "{marker}" ]; then echo blocked >&2; exit 1; fi\nexit 0\n')
    git(repo, 'commit', '--quiet', '-am', 'a pre-push guard that refuses while the marker exists')
    git(repo, 'push', '--quiet', 'origin', 'HEAD:refs/heads/main')
    marker.write_text('')
    record = run(repo, tmp_path, at_noon(FIRST - timedelta(days=1)), label='blocked')
    assert record['exit'] == 2 and record['outcome'].startswith('publication refused')
    assert [e['kind'] for e in store_of(origin).entries()] == ['genesis']


# ---- the store -------------------------------------------------------------------------------------------------------

def test_the_store_keeps_cp17cs_head_binding_and_refuses_tampering(origin, tmp_path):
    repo = origin('a')
    run(repo, tmp_path, at_noon(date(2026, 8, 25)), label='r')
    folder = repo / STORE_PATH
    LiveStore(folder).verify()
    head = json.loads((folder / 'head.json').read_text())
    # F1: a head repointed at another state, day or artifact fails, even with its entry hash intact
    for key, value in (('last_day', '2026-08-24'), ('last_artifact_sha256', '0' * 64), ('state_file', 'states/genesis-2026-08-24.json')):
        (folder / 'head.json').write_text(json.dumps({**head, key: value}))
        with pytest.raises(StoreRefused):
            LiveStore(folder).verify()
    (folder / 'head.json').write_text(json.dumps(head))
    LiveStore(folder).verify()
    record = folder / 'runs/r.json'
    original = record.read_bytes()
    record.write_bytes(original.replace(b'"runner"', b'"RUNNER"'))
    with pytest.raises(StoreRefused, match='absent or altered'):
        LiveStore(folder).verify()
    record.write_bytes(original)
    with pytest.raises(StoreRefused):
        LiveStore(folder).record_not_issued(date(2026, 8, 24), causes.NO_RUN, [])       # days go forward
    with pytest.raises(ValueError):
        LiveStore(folder).record_not_issued(date(2026, 8, 30), 'late', [])


def test_a_store_that_does_not_verify_issues_nothing(origin, tmp_path):
    repo = origin('a')
    folder = repo / STORE_PATH
    head = json.loads((folder / 'head.json').read_text())
    (folder / 'head.json').write_text(json.dumps({**head, 'state_sha256': {'v4': '0' * 64}}))
    git(repo, 'commit', '--quiet', '-am', 'tamper')
    git(repo, 'push', '--quiet', 'origin', 'HEAD:refs/heads/main')
    record = run(repo, tmp_path, at_noon(FIRST - timedelta(days=1)), label='t')
    assert record['exit'] == 2 and 'StoreRefused' in record['outcome'] and record['days'] == {}


def test_a_carry_across_a_gap_resumes_bit_for_bit(origin, tmp_path):
    """4.7T's stand-in issues two days; the store is carried (pushed, then cloned elsewhere); the first live day,
    after a gap, is issued from the carried store and equals the same day issued in place."""
    window = origin('window')
    run(window, tmp_path, at_noon(date(2026, 8, 24)), label='w')                       # 08-24, 08-25
    store = LiveStore(window / STORE_PATH)
    store.record_carry(date(2026, 8, 25), date(2026, 8, 29), "between 4.7T's last window day and the first live day")
    git(window, 'add', '-A')
    git(window, 'commit', '--quiet', '-m', 'carry')
    git(window, 'push', '--quiet', 'origin', 'HEAD:refs/heads/main')
    carried, in_place = origin('carried'), origin('in-place')
    assert (carried / STORE_PATH / 'head.json').read_bytes() == (window / STORE_PATH / 'head.json').read_bytes()
    days = LiveStore(carried / STORE_PATH).days()
    assert [days[str(date(2026, 8, 26) + timedelta(days=i))]['status'] for i in range(3)] == ['outside'] * 3
    a = run(carried, tmp_path, at_noon(date(2026, 8, 28)), label='live')               # target 08-29
    assert a['planned'] == ['2026-08-29'] and a['closed'] == []
    b_store = LiveStore(in_place / STORE_PATH)
    state, _ = b_store.state()
    art = stand_in_issue()(date(2026, 8, 29), True, None, settings=None, parent_sha256=b_store.last_artifact_sha256(),
                           data_refresh_utc='', states=state)['artifact']
    assert art['artifact_sha256'] == a['days']['2026-08-29']['artifact_sha256']
