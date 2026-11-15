"""CP-18d item 2's measurement tool, `cp18.schedule_probe`, on fixture JSON (no network).

What is checked: the cron instant (a run created after midnight for the previous evening's line included), the
scheduler delay, each runner's queue, a missed start and a pending one, the starts missed before the first scheduled run,
the per-hour summary, the merge of several collections, and that collecting makes read calls only.
"""
from __future__ import annotations

from datetime import datetime, timezone
import json

import pytest

from cp18 import schedule_probe as P

UTC = timezone.utc
REPO, WORKFLOW = 'owner/repo', 'schedule-probe.yml'


def run(run_id: int, cron: str, created: str, *, event: str = 'schedule', status: str = 'completed') -> dict:
    return {'databaseId': run_id, 'displayTitle': f'probe {cron}' if event == 'schedule' else 'probe dispatch',
            'name': f'probe {cron}', 'event': event, 'createdAt': created, 'status': status,
            'conclusion': 'success' if status == 'completed' else '', 'attempt': 1}


def jobs(ubuntu: str | None, macos: str | None) -> dict:
    out = []
    for label, started in (('ubuntu-latest', ubuntu), ('macos-26', macos)):
        out.append({'id': len(out) + 1, 'name': f'probe ({label})', 'labels': [label], 'started_at': started,
                    'status': 'completed' if started else 'queued', 'conclusion': 'success' if started else None})
    return {'total_count': len(out), 'jobs': out}


def raw(runs: list[dict], job_map: dict, collected: str, created_wf: str | None = None) -> dict:
    return {'schema': P.RAW_SCHEMA, 'repo': REPO, 'workflow': WORKFLOW, 'collection_started_utc': collected,
            'collection_finished_utc': collected, 'runs': runs, 'jobs': {str(k): v for k, v in job_map.items()},
            'workflow_record': {'created_at': created_wf} if created_wf else None}


# ------------------------------------------------------------------------------------------------ the instant
def test_the_cron_instant_is_the_latest_named_instant_at_or_before_the_creation():
    at = P.cron_instant(7, 3, datetime(2026, 11, 16, 3, 19, 41, tzinfo=UTC))
    assert at == datetime(2026, 11, 16, 3, 7, tzinfo=UTC)
    assert P.cron_instant(7, 3, datetime(2026, 11, 16, 3, 7, tzinfo=UTC)) == datetime(2026, 11, 16, 3, 7, tzinfo=UTC)


def test_a_run_created_after_midnight_belongs_to_the_previous_days_line():
    assert P.cron_instant(7, 23, datetime(2026, 11, 17, 0, 2, 5, tzinfo=UTC)) == datetime(2026, 11, 16, 23, 7, tzinfo=UTC)
    value = P.measure([raw([run(1, '7 23 * * *', '2026-11-17T00:02:05Z')], {1: jobs(None, None)},
                           '2026-11-17T06:00:00Z')])
    (r,) = value['runs']
    assert r['cron_utc'] == '2026-11-16T23:07:00Z' and r['cron_day'] == '2026-11-16'
    assert r['delay_seconds'] == 55 * 60 + 5


def test_the_cron_line_comes_from_the_run_name_and_must_be_daily():
    assert P.cron_of('probe 7 4 * * *') == ('7 4 * * *', 7, 4)
    for bad in ('probe dispatch', 'daily', 'probe */5 * * * *', 'probe 7 4 * * 1', 'probe 61 4 * * *'):
        with pytest.raises(ValueError):
            P.cron_of(bad)


# ------------------------------------------------------------------------------------------------ delay and queue
def test_the_delay_and_each_runners_queue():
    value = P.measure([raw([run(1, '7 4 * * *', '2026-11-16T04:19:30Z')],
                           {1: jobs('2026-11-16T04:19:36Z', '2026-11-16T04:21:00Z')}, '2026-11-16T12:00:00Z')])
    (r,) = value['runs']
    assert r['delay_seconds'] == 12 * 60 + 30
    assert r['jobs']['ubuntu-latest']['queue_seconds'] == 6
    assert r['jobs']['macos-26']['queue_seconds'] == 90


def test_a_job_not_started_has_no_queue():
    value = P.measure([raw([run(1, '7 4 * * *', '2026-11-16T04:19:30Z', status='in_progress')],
                           {1: jobs('2026-11-16T04:19:36Z', None)}, '2026-11-16T04:25:00Z')])
    (r,) = value['runs']
    assert r['jobs']['macos-26']['queue_seconds'] is None and r['jobs']['ubuntu-latest']['queue_seconds'] == 6
    (hour,) = [h for h in value['per_hour'] if h['cron'] == '7 4 * * *']
    assert 'macos-26' not in hour['queue_seconds'] or hour['queue_seconds']['macos-26'] is None


# ------------------------------------------------------------------------------------------------ missed
def test_a_missed_start_and_a_pending_one():
    lines = ['7 4 * * *', '7 5 * * *']
    runs = [run(1, '7 4 * * *', '2026-11-16T04:10:00Z'), run(2, '7 5 * * *', '2026-11-16T05:20:00Z'),
            run(3, '7 4 * * *', '2026-11-17T04:30:00Z'),
            run(9, '', '2026-11-16T10:00:00Z', event='workflow_dispatch')]
    job_map = {i: jobs(None, None) for i in (1, 2, 3, 9)}
    # collected at 05:40 on the 17th: the 05:07 start of the 17th has no run yet, 33 min ago: pending, not missed
    value = P.measure([raw(runs, job_map, '2026-11-17T05:40:00Z')], lines=lines)
    assert value['probe_days'] == ['2026-11-16', '2026-11-17'] and value['scheduled_runs'] == 3
    assert value['missed'] == [] and value['pending'] == [{'cron': '7 5 * * *', 'cron_utc': '2026-11-17T05:07:00Z'}]
    assert value['skipped'] == [{'run_id': 9, 'event': 'workflow_dispatch', 'reason': 'not a scheduled run'}]
    # an hour later it is missed
    later = P.measure([raw(runs, job_map, '2026-11-17T06:20:00Z')], lines=lines)
    assert later['missed'] == [{'cron': '7 5 * * *', 'cron_utc': '2026-11-17T05:07:00Z'}] and later['pending'] == []
    # with no grace, as the brief words it, it is missed at once
    strict = P.measure([raw(runs, job_map, '2026-11-17T05:40:00Z')], lines=lines, grace_minutes=0)
    assert strict['missed'] == [{'cron': '7 5 * * *', 'cron_utc': '2026-11-17T05:07:00Z'}]
    # a line that never ran on any day is still counted when the probed lines are given
    third = P.measure([raw(runs, job_map, '2026-11-17T06:20:00Z')], lines=lines + ['7 6 * * *'])
    assert {m['cron_utc'] for m in third['missed'] if m['cron'] == '7 6 * * *'} == {'2026-11-16T06:07:00Z'}
    assert third['pending'] == [{'cron': '7 6 * * *', 'cron_utc': '2026-11-17T06:07:00Z'}]


def test_the_starts_missed_before_the_first_scheduled_run():
    """The workflow was created at 23:50; its first scheduled run came on the 16th: the 15th's starts after the
    creation are listed apart; none before the creation counts."""
    runs = [run(1, '7 0 * * *', '2026-11-16T00:31:00Z')]
    value = P.measure([raw(runs, {1: jobs(None, None)}, '2026-11-16T03:00:00Z', created_wf='2026-11-15T01:50:37+02:00')],
                      lines=['7 0 * * *', '7 1 * * *'])
    assert value['workflow_created_utc'] == '2026-11-14T23:50:37Z'
    assert value['missed_before_first_run'] == [{'cron': '7 0 * * *', 'cron_utc': '2026-11-15T00:07:00Z'},
                                                {'cron': '7 1 * * *', 'cron_utc': '2026-11-15T01:07:00Z'}]
    assert value['missed'] == [{'cron': '7 1 * * *', 'cron_utc': '2026-11-16T01:07:00Z'}]
    # no scheduled run at all: every start since the creation is missed before the first run (or pending)
    none = P.measure([raw([], {}, '2026-11-15T02:35:28Z', created_wf='2026-11-14T23:50:37Z')],
                     lines=['7 0 * * *', '7 1 * * *', '7 2 * * *'])
    assert none['probe_days'] == [] and none['missed'] == []
    assert [b['cron_utc'] for b in none['missed_before_first_run']] == ['2026-11-15T00:07:00Z', '2026-11-15T01:07:00Z']
    assert none['pending'] == [{'cron': '7 2 * * *', 'cron_utc': '2026-11-15T02:07:00Z'}]


# ------------------------------------------------------------------------------------------------ the summary
def test_the_per_hour_summary():
    delays = [60, 120, 180, 240, 300, 360, 420, 480, 540, 3600]          # seconds after 04:07, ten days
    runs, job_map = [], {}
    for i, d in enumerate(delays):
        created = datetime(2026, 11, 10 + i, 4, 7, tzinfo=UTC).timestamp() + d
        stamp = datetime.fromtimestamp(created, UTC).strftime('%Y-%m-%dT%H:%M:%SZ')
        runs.append(run(i + 1, '7 4 * * *', stamp))
        job_map[i + 1] = jobs(datetime.fromtimestamp(created + 5, UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                              datetime.fromtimestamp(created + 10 * (i + 1), UTC).strftime('%Y-%m-%dT%H:%M:%SZ'))
    value = P.measure([raw(runs, job_map, '2026-11-20T12:00:00Z')])
    (hour,) = value['per_hour']
    assert hour['cron'] == '7 4 * * *' and hour['hour_utc'] == 4 and hour['runs'] == 10
    assert hour['days_observed'] == 11 and hour['missed'] == 1            # the 20th's start never came
    assert hour['delay_seconds'] == {'n': 10, 'min': 60, 'median': 330.0, 'p90': 540, 'max': 3600}
    assert hour['queue_seconds']['ubuntu-latest'] == {'n': 10, 'min': 5, 'median': 5.0, 'max': 5}
    assert hour['queue_seconds']['macos-26'] == {'n': 10, 'min': 10, 'median': 55.0, 'max': 100}
    assert len(hour['days_with_a_run']) == 10 and value['days_with_a_run'] == hour['days_with_a_run']
    assert len(value['probe_days']) == 11
    assert 'only' in value['method'] and 'gh run list' in value['method'] and 'createdAt' in value['method']


def test_collections_merge_by_run_id_the_latest_copy_winning():
    early = raw([run(1, '7 4 * * *', '2026-11-16T04:10:00Z', status='in_progress')], {1: jobs('2026-11-16T04:10:05Z', None)},
                '2026-11-16T04:15:00Z')
    late = raw([run(1, '7 4 * * *', '2026-11-16T04:10:00Z'), run(2, '7 4 * * *', '2026-11-17T04:09:00Z')],
               {1: jobs('2026-11-16T04:10:05Z', '2026-11-16T04:12:00Z'), 2: jobs(None, None)}, '2026-11-17T08:00:00Z')
    value = P.measure([late, early])
    assert value['collected_utc'] == '2026-11-17T08:00:00Z' and value['scheduled_runs'] == 2
    assert value['runs'][0]['status'] == 'completed' and value['runs'][0]['jobs']['macos-26']['queue_seconds'] == 120
    with pytest.raises(ValueError):
        P.measure([late, dict(early, repo='other/repo')])


# ------------------------------------------------------------------------------------------------ collecting
def test_collecting_makes_read_calls_only():
    calls = []

    def fake(args):
        calls.append(args)
        if args[:2] == ['run', 'list']:
            return [run(5, '7 4 * * *', '2026-11-16T04:10:00Z')]
        if args[1].endswith('/jobs?per_page=100'):
            return jobs('2026-11-16T04:10:05Z', '2026-11-16T04:11:00Z')
        return {'created_at': '2026-11-14T23:50:37Z', 'state': 'active'}

    value = P.collect(REPO, WORKFLOW, call=fake)
    assert value['schema'] == P.RAW_SCHEMA and value['runs'][0]['databaseId'] == 5
    assert value['jobs']['5']['jobs'][1]['labels'] == ['macos-26']
    assert value['workflow_record']['state'] == 'active'
    assert [c[:2] for c in calls] == [['run', 'list'], ['api', f'repos/{REPO}/actions/runs/5/jobs?per_page=100'],
                                      ['api', f'repos/{REPO}/actions/workflows/{WORKFLOW}']]
    assert all(c.startswith('gh run list ') or c.startswith('gh api repos/') for c in value['commands'])
    # the read-only guard refuses a write before anything runs
    for write in (['api', '-X', 'POST', f'repos/{REPO}/actions/workflows/{WORKFLOW}/dispatches'],
                  ['api', f'repos/{REPO}/dispatches', '-f', 'event_type=x'], ['run', 'cancel', '1'],
                  ['workflow', 'run', WORKFLOW]):
        with pytest.raises(ValueError):
            P.gh(write)


def test_the_command_line_measures_raw_files(tmp_path):
    path = tmp_path / 'raw.json'
    path.write_text(json.dumps(raw([run(1, '7 4 * * *', '2026-11-16T04:19:30Z')],
                                   {1: jobs('2026-11-16T04:19:36Z', '2026-11-16T04:21:00Z')}, '2026-11-16T12:00:00Z')))
    workflow = tmp_path / 'probe.yml'
    workflow.write_text("on:\n  schedule:\n    - cron: '7 4 * * *'\n    - cron: '7 5 * * *'\n  workflow_dispatch:\n")
    out = tmp_path / 'm.json'
    assert P.main(['measure', '--raw', str(path), '--workflow-file', str(workflow), '--out', str(out)]) == 0
    value = json.loads(out.read_text())
    assert value['schema'] == P.SCHEMA and value['lines'] == ['7 4 * * *', '7 5 * * *']
    assert value['missed'] == [{'cron': '7 5 * * *', 'cron_utc': '2026-11-16T05:07:00Z'}]
