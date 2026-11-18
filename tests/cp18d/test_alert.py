"""The daily operation's alert (the Orchestrator's ruling O54; `src/cp18/alert.py`), driven through its own command
(`alert.main`, which computes its start date from `--now` as the workflow runs it), across consecutive links on a store
that evolves, with a recorded issues API in memory (nothing touches the network).

The first Integration review's three findings (critic-1, FAIL) are reproduced here as tests: an issue closes in the
first healthy link after a later day is issued with all inputs before the cutoff, however recent its own day; a failed
tick's issue is dated and closes the same way; a later day is reported even when its date already appears in the issue
(as an earlier copy's fetch time).
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import shutil

import pytest

from cp18 import alert as A, inputclass

ROOT = Path(__file__).resolve().parents[2]
RUN = 'https://github.com/hrsi56/delu-day-ahead-forecast/actions/runs/{}'
NOT_ISSUED = "a live day's inputs that cannot be shown to precede its cutoff"


class Issues:
    """GitHub's issues API, in memory: open and closed issues, comments, and the calls received."""

    def __init__(self):
        self.issues, self.comments, self.calls, self.n = {}, {}, [], 0

    def request(self, method, path, body=None):
        self.calls.append((method, path, body))
        if method == 'GET' and path.startswith('issues?state=all'):
            page = int(re.search(r'[?&]page=(\d+)', path).group(1))
            items = [dict(i) for i in self.issues.values()]
            return items[(page - 1) * 100:page * 100]
        if method == 'GET' and '/comments' in path:
            return [{'body': b} for b in self.comments.get(int(path.split('/')[1]), [])]
        if method == 'POST' and path == 'issues':
            self.n += 1
            self.issues[self.n] = {'number': self.n, 'title': body['title'], 'body': body['body'], 'state': 'open',
                                   'user': {'login': A.BOT}}
            return {'number': self.n}
        if method == 'POST' and path.endswith('/comments'):
            self.comments.setdefault(int(path.split('/')[1]), []).append(body['body'])
            return {}
        if method == 'PATCH':
            self.issues[int(path.split('/')[1])]['state'] = body['state']
            return {}
        raise AssertionError((method, path))

    def by_title(self, kind):
        return [i for i in self.issues.values() if i['title'] == A.TITLES[kind]]

    def text(self, number):
        return '\n'.join([self.issues[number]['body']] + self.comments.get(number, []))


class Store:
    """A store folder with only what the alert reads: the ledger's day entries and each issued day's record."""

    def __init__(self, folder: Path):
        self.folder, self.entries = folder, []

    def issued(self, day, cls=inputclass.BEFORE, fetched=None):
        rel = f'issued/{day}/record.json'
        (self.folder / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.folder / rel).write_text(json.dumps({'day': day, **inputclass.label(cls, fetched)}))
        self.entries.append({'kind': 'issuance', 'day': day, 'issued_policy': 'A1', 'record_file': rel})
        return self

    def not_issued(self, day, cause=NOT_ISSUED):
        self.entries.append({'kind': 'not_issued', 'day': day, 'cause': 'inputs', 'cause_text': cause})
        return self

    def write(self):
        self.folder.mkdir(parents=True, exist_ok=True)
        (self.folder / 'ledger.jsonl').write_text(''.join(json.dumps(e) + '\n' for e in self.entries))
        return self.folder


@pytest.fixture
def api(monkeypatch):
    issues = Issues()
    monkeypatch.setattr(A, 'API', lambda repo: issues)
    return issues


def link(store: Store, now: str, run: int, *failed: str, day: str = ''):
    args = ['--repo', 'o/r', '--store', str(store.write()), '--run-url', RUN.format(run), '--now', now, '--day', day]
    for job in failed:
        args += ['--failed', job]
    assert A.main(args) == 0


def test_a_day_not_issued_closes_in_the_first_healthy_link_after_a_later_clean_day_and_is_never_repeated(api, tmp_path):
    store = Store(tmp_path / 'store').issued('2026-11-15').not_issued('2026-11-16')
    link(store, '2026-11-17T11:00:00Z', 1)                                   # target 2026-11-18
    (issue,) = api.by_title('not_issued')
    assert issue['state'] == 'open' and f'- 2026-11-16: not issued ({NOT_ISSUED}). Run: {RUN.format(1)}' in issue['body']
    link(store, '2026-11-17T15:00:00Z', 2)                                   # nothing new, no later clean day yet
    assert issue['state'] == 'open' and not api.comments
    store.issued('2026-11-17')                                               # a later day, every input before the cutoff
    link(store, '2026-11-18T11:00:00Z', 3)                                   # 2026-11-16 is still recent: it closes anyway
    assert api.issues[issue['number']]['state'] == 'closed'
    assert api.comments[issue['number']][-1] == f'Closed: 2026-11-17 was issued with all inputs before the cutoff. Run: {RUN.format(3)}'
    store.issued('2026-11-18')
    link(store, '2026-11-19T11:00:00Z', 4)                                   # the closed issue remembers 2026-11-16
    assert len(api.by_title('not_issued')) == 1 and len(api.issues) == 1


def test_a_failed_tick_is_dated_by_the_target_day_and_closes_the_same_way(api, tmp_path):
    store = Store(tmp_path / 'store').issued('2026-11-15')
    link(store, '2026-11-17T11:00:00Z', 1, 'tick')                           # no day of its own: the target day
    (issue,) = api.by_title('failed')
    assert f'- 2026-11-18: the tick job failed. Run: {RUN.format(1)}' in issue['body']
    store.issued('2026-11-18')
    link(store, '2026-11-18T11:00:00Z', 2)                                   # 2026-11-18 is not later than the failure's day
    assert api.issues[issue['number']]['state'] == 'open'
    store.issued('2026-11-19')
    link(store, '2026-11-19T11:00:00Z', 3, 'run', day='2026-11-20')          # a failed link closes nothing
    assert api.issues[issue['number']]['state'] == 'open'
    assert f'- 2026-11-20: the run job failed. Run: {RUN.format(3)}' in api.comments[issue['number']][0]
    store.issued('2026-11-20').issued('2026-11-21')
    link(store, '2026-11-21T11:00:00Z', 4)
    assert api.issues[issue['number']]['state'] == 'closed'


def test_a_later_day_is_reported_even_when_its_date_already_appears_as_an_earlier_copys_fetch_time(api, tmp_path):
    store = Store(tmp_path / 'store').issued('2026-11-15').issued('2026-11-16', inputclass.AFTER, '2026-11-17T09:00:00Z')
    link(store, '2026-11-17T11:00:00Z', 1)
    (issue,) = api.by_title('fetched_after_cutoff')
    assert ('- 2026-11-16: issued with the load forecast fetched after the cutoff, at 2026-11-17T09:00:00Z (UTC). '
            f'Run: {RUN.format(1)}') in issue['body']
    store.issued('2026-11-17', inputclass.AFTER, '2026-11-17T12:00:00Z')    # "2026-11-17" is already in the issue's text
    link(store, '2026-11-17T13:00:00Z', 2)
    assert api.comments[issue['number']] == [
        f'- 2026-11-17: issued with the load forecast fetched after the cutoff, at 2026-11-17T12:00:00Z (UTC). '
        f'Run: {RUN.format(2)}']
    store.issued('2026-11-18')
    link(store, '2026-11-18T11:00:00Z', 3)
    assert api.issues[issue['number']]['state'] == 'closed'


def test_a_problem_after_a_closed_issue_opens_a_new_one(api, tmp_path):
    store = Store(tmp_path / 'store').issued('2026-11-15').not_issued('2026-11-16').issued('2026-11-17')
    link(store, '2026-11-17T11:00:00Z', 1)                                   # opened, and 2026-11-17 is later: no close in
    (first,) = api.by_title('not_issued')                                    # the same link that reported it
    assert first['state'] == 'open'
    link(store, '2026-11-17T15:00:00Z', 2)
    assert api.issues[first['number']]['state'] == 'closed'
    store.not_issued('2026-11-18')
    link(store, '2026-11-19T11:00:00Z', 3)
    assert [i['state'] for i in api.by_title('not_issued')] == ['closed', 'open']


def test_older_days_never_alert_and_issues_by_others_are_left_alone(api, tmp_path):
    api.issues[7] = {'number': 7, 'title': A.TITLES['not_issued'], 'body': "a person's issue", 'state': 'open',
                     'user': {'login': 'someone'}}
    api.n = 7
    store = Store(tmp_path / 'store').not_issued('2026-11-13').issued('2026-11-15')
    link(store, '2026-11-18T11:00:00Z', 1)                                   # target 2026-11-19: from 2026-11-15 on
    assert len(api.issues) == 1
    store.not_issued('2026-11-16')
    link(store, '2026-11-18T12:00:00Z', 2)
    assert api.issues[7]['body'] == "a person's issue" and 7 not in api.comments and len(api.issues) == 2


def test_the_texts_name_the_retrieval_and_carry_no_credential(api, tmp_path, monkeypatch):
    monkeypatch.setenv('GH_TOKEN', 'ghs_' + 'x' * 36)
    store = Store(tmp_path / 'store').issued('2026-11-16', inputclass.AFTER, '2026-11-15T11:17:20Z').not_issued('2026-11-17')
    link(store, '2026-11-17T11:00:00Z', 1, 'run', day='2026-11-18')
    text = json.dumps(api.calls).lower()
    assert not re.search(r'\blate\b|\btimely\b', text) and 'ghs_' not in text and 'token' not in text


def test_the_facts_are_the_stores_on_main_including_a_day_fetched_after_the_cutoff(tmp_path):
    from cp18d.fixture_after_cutoff import relabel
    shutil.copytree(ROOT / 'live/store', tmp_path / 'live/store')
    relabel(tmp_path / 'live', '2026-11-14', '2026-11-13T10:21:07Z')
    value = A.facts(tmp_path / 'live/store')
    by = {i['day']: i for i in value['issued']}
    assert by['2026-11-14']['input_class'] == inputclass.AFTER
    assert by['2026-11-14']['fetched_utc'] == '2026-11-13T10:21:07Z'
    assert by['2026-11-15']['input_class'] == inputclass.BEFORE
    assert {d['day'] for d in value['not_issued']} >= {'2026-11-09', '2026-11-13'}


def test_the_alert_runs_without_the_projects_environment():
    import subprocess
    import sys
    done = subprocess.run([sys.executable, '-I', str(ROOT / 'src/cp18/alert.py'), '--help'], capture_output=True,
                          text=True, cwd='/', env={})
    assert done.returncode == 0 and '--run-url' in done.stdout
