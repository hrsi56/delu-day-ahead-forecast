"""The daily operation's alert (the Orchestrator's ruling O54; `src/cp18/alert.py`): one GitHub issue per problem,
opened or commented on, closed by itself once a later day is issued with all inputs before the cutoff. A mocked API
holds the issues in memory; nothing touches the network.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
import json
from pathlib import Path
import shutil

import pytest

from cp18 import alert as A, inputclass

ROOT = Path(__file__).resolve().parents[2]
RUN = 'https://github.com/hrsi56/delu-day-ahead-forecast/actions/runs/1'
UTC = timezone.utc


class Issues:
    """GitHub's issues API, in memory, with the calls it received."""

    def __init__(self):
        self.issues, self.comments, self.calls, self.n = {}, {}, [], 0

    def request(self, method, path, body=None):
        self.calls.append((method, path, body))
        if method == 'GET' and path.startswith('issues?state=open'):
            return [dict(i) for i in self.issues.values() if i['state'] == 'open']
        if method == 'GET' and path.startswith('issues/') and '/comments' in path:
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


def facts(issued=(), not_issued=()):
    return {'issued': [{'day': d, 'input_class': c, 'fetched_utc': f} for d, c, f in issued],
            'not_issued': [{'day': d, 'cause': c} for d, c in not_issued]}


SINCE = date(2026, 11, 13)
AFTER = ('2026-11-16', inputclass.AFTER, '2026-11-15T11:13:56Z')


def test_a_day_fetched_after_the_cutoff_opens_one_issue_then_comments_then_closes():
    api = Issues()
    value = facts([('2026-11-15', inputclass.BEFORE, None), AFTER])
    done = A.alert(api, value, A.problems(value, [], RUN, SINCE, None), RUN)
    assert [d['did'] for d in done] == ['opened']
    issue = api.issues[1]
    assert issue['title'] == A.TITLES['fetched_after_cutoff']
    assert '2026-11-16: issued with the load forecast fetched after the cutoff, at 2026-11-15T11:13:56Z (UTC)' in issue['body']
    assert RUN in issue['body']
    # the same day again: nothing repeated
    again = A.alert(api, value, A.problems(value, [], RUN, SINCE, None), RUN)
    assert again == [] and 1 not in api.comments
    # another such day: one comment on the same issue, no second issue
    value2 = facts([('2026-11-15', inputclass.BEFORE, None), AFTER, ('2026-11-17', inputclass.AFTER, '2026-11-16T10:40:00Z')])
    run2 = RUN[:-1] + '2'
    done = A.alert(api, value2, A.problems(value2, [], run2, SINCE, None), run2)
    assert [d['did'] for d in done] == ['commented'] and len(api.issues) == 1
    assert '2026-11-17' in api.comments[1][0] and run2 in api.comments[1][0]
    # a later day issued with every input before the cutoff closes it
    value3 = facts(value2['issued'] and [(i['day'], i['input_class'], i['fetched_utc']) for i in value2['issued']]
                   + [('2026-11-18', inputclass.BEFORE, None)])
    run3 = RUN[:-1] + '3'
    found = [p for p in A.problems(value3, [], run3, date(2026, 11, 18), None)]
    done = A.alert(api, value3, found, run3)
    assert [d['did'] for d in done] == ['closed'] and api.issues[1]['state'] == 'closed'
    assert api.comments[1][-1] == f'Closed: 2026-11-18 was issued with all inputs before the cutoff. Run: {run3}'


def test_a_day_not_issued_and_a_failed_job_each_have_their_own_issue_and_a_failure_closes_nothing():
    api = Issues()
    value = facts([('2026-11-15', inputclass.BEFORE, None)],
                  [('2026-11-16', "a live day's inputs that cannot be shown to precede its cutoff")])
    found = A.problems(value, ['run'], RUN, SINCE, '2026-11-16')
    done = A.alert(api, value, found, RUN)
    assert sorted(d['kind'] for d in done) == ['failed', 'not_issued'] and len(api.issues) == 2
    titles = {i['title']: i for i in api.issues.values()}
    assert "2026-11-16: not issued (a live day's inputs that cannot be shown to precede its cutoff)" in \
        titles[A.TITLES['not_issued']]['body']
    assert f'2026-11-16: the run job failed. Run: {RUN}' in titles[A.TITLES['failed']]['body']
    # a later healthy day, but in a link that itself failed: nothing closes
    value2 = facts([('2026-11-15', inputclass.BEFORE, None), ('2026-11-17', inputclass.BEFORE, None)],
                   value['not_issued'] and [(i['day'], i['cause']) for i in value['not_issued']])
    run2 = RUN[:-1] + '2'
    A.alert(api, value2, A.problems(value2, ['acquire'], run2, SINCE, '2026-11-18'), run2)
    assert all(i['state'] == 'open' for i in api.issues.values())
    # a healthy link afterwards closes what a later day answers: the day not issued (2026-11-16) by 2026-11-17; the
    # failures stay open, the last one being 2026-11-18's acquisition
    run3 = RUN[:-1] + '3'
    done = A.alert(api, value2, A.problems(value2, [], run3, date(2026, 11, 17), None), run3)
    assert [(d['kind'], d['did']) for d in done] == [('not_issued', 'closed')]
    assert titles[A.TITLES['failed']]['state'] == 'open' or api.issues[1]['state'] == 'open'
    value3 = facts([(i['day'], i['input_class'], i['fetched_utc']) for i in value2['issued']]
                   + [('2026-11-19', inputclass.BEFORE, None)])
    done = A.alert(api, value3, A.problems(value3, [], run3, date(2026, 11, 19), None), run3)
    assert [(d['kind'], d['did']) for d in done] == [('failed', 'closed')]
    assert all(i['state'] == 'closed' for i in api.issues.values())


def test_older_days_never_alert_and_issues_by_others_are_left_alone():
    api = Issues()
    api.issues[7] = {'number': 7, 'title': A.TITLES['not_issued'], 'body': 'a person\'s issue', 'state': 'open',
                     'user': {'login': 'someone'}}
    api.n = 7
    value = facts([('2026-11-15', inputclass.BEFORE, None)], [('2026-11-03', 'no run within the lookback')])
    assert A.problems(value, [], RUN, SINCE, None) == []
    value = facts([], [('2026-11-16', 'no run within the lookback')])
    A.alert(api, value, A.problems(value, [], RUN, SINCE, None), RUN)
    assert api.issues[7]['body'] == 'a person\'s issue' and 7 not in api.comments and len(api.issues) == 2


def test_the_texts_name_the_retrieval_and_carry_no_credential(monkeypatch):
    monkeypatch.setenv('GH_TOKEN', 'ghs_' + 'x' * 36)
    api = Issues()
    value = facts([AFTER], [('2026-11-17', 'no run within the lookback')])
    A.alert(api, value, A.problems(value, ['run'], RUN, SINCE, '2026-11-17'), RUN)
    import re
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
    found = A.problems(value, [], RUN, date(2026, 11, 10), None)
    assert {(p['kind'], p['day']) for p in found} == {('fetched_after_cutoff', '2026-11-14'), ('not_issued', '2026-11-10'),
                                                      ('not_issued', '2026-11-11'), ('not_issued', '2026-11-12'),
                                                      ('not_issued', '2026-11-13')}


def test_the_alert_runs_without_the_projects_environment(tmp_path):
    import subprocess
    import sys
    done = subprocess.run([sys.executable, '-I', str(ROOT / 'src/cp18/alert.py'), '--help'], capture_output=True,
                          text=True, cwd='/', env={})
    assert done.returncode == 0 and '--run-url' in done.stdout
