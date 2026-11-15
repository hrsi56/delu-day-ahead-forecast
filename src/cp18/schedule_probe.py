"""The schedule probe's measurement (CP-18d item 2): how late GitHub's scheduler starts a run at each probed hour, how
long each runner then queues, and which scheduled starts never came.

    python -m cp18.schedule_probe collect --repo hrsi56/delu-day-ahead-forecast --workflow schedule-probe.yml \\
        --out <raw.json>
    python -m cp18.schedule_probe measure --raw <raw.json> [--raw ...] --out <measurement.json> [--grace-minutes 60]

**collect** reads only, through GitHub's CLI: `gh run list --json <fields> --limit 1000` for the workflow, then each
run's jobs (`gh api repos/<repo>/actions/runs/<id>/jobs?per_page=100`) and the workflow's own record
(`gh api repos/<repo>/actions/workflows/<workflow>`), all GET requests. Every response is saved verbatim, parsed but
unchanged, with the collection's start and end time (UTC) and the exact commands. Nothing is ever written to GitHub.

**measure** works on the saved files alone (no network):

- **Scheduled runs only** (event `schedule`). Each run's cron line is read from its name (`probe <cron line>`, the
  probe's `run-name`); the line must be `M H * * *` with fixed minute and hour.
- **The cron instant** of a run is the latest instant at or before its creation that its cron line names (minute M of
  hour H, UTC). A run created just after midnight for the 23:07 line belongs to the previous day's 23:07.
- **The scheduler delay** is the run's `createdAt` minus its cron instant, in seconds.
- **The queue** of each job is its `started_at` minus the run's `createdAt`, in seconds, per runner label (the job's
  `labels`); a job that has not started has none.
- **Missed starts.** The probe days run from the first scheduled run's cron day through the collection day (UTC). Every
  cron instant of the probed lines on those days that is past at the collection (and after the workflow's creation,
  when its record is known), with no scheduled run, is missed. The probed lines are the runs' own, and any given with
  `--line` or read from `--workflow-file` (so a line that never fired is still counted).
  An instant less than `--grace-minutes` before the collection (default 60) is listed as pending instead: its run may
  still be created. With the workflow's own record, the instants between its creation and the first probe day with no
  run are listed apart, as missed before the first scheduled run.
- **Per cron hour:** the days observed, the runs, the missed starts, the delay's minimum, median, 90th percentile
  (nearest rank) and maximum, and each runner's queue minimum, median and maximum, with the days that had a run.

Several raw files merge by run id (the latest collection's copy of a run wins); the collection time is the latest.
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import sys

RAW_SCHEMA = 'cp18d-schedule-probe-raw-v1'
SCHEMA = 'cp18d-schedule-probe-v1'
UTC = timezone.utc
RUN_FIELDS = ('attempt,conclusion,createdAt,databaseId,displayTitle,event,headBranch,headSha,name,number,startedAt,'
              'status,updatedAt,url,workflowDatabaseId,workflowName')
CRON = re.compile(r'^(\d{1,2}) (\d{1,2}) \* \* \*$')
NAME = re.compile(r'^probe (.+)$')


def utc_now() -> str:
    return datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


def parse_time(text: str) -> datetime:
    """GitHub's ISO 8601 time (`Z` or an offset), as an aware UTC datetime."""
    value = datetime.fromisoformat(text.replace('Z', '+00:00'))
    if value.tzinfo is None:
        raise ValueError(f'{text}: a time without its offset')
    return value.astimezone(UTC)


def stamp(value: datetime) -> str:
    return value.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


# ------------------------------------------------------------------------------------------------ collect
def gh(args: list[str]) -> object:
    """One read-only `gh` call, its JSON output parsed. Only `run list` and GET `api` calls are ever made."""
    listing = args[:2] == ['run', 'list'] and not any(a.startswith(('-X', '--method', '-f', '-F', '--field',
                                                                     '--raw-field', '--input')) for a in args)
    get = len(args) == 2 and args[0] == 'api' and not args[1].startswith('-')       # `gh api <path>` is a GET
    if not (listing or get):
        raise ValueError(f'not a read call: gh {" ".join(args)}')
    done = subprocess.run(['gh', *args], capture_output=True, text=True, check=True)
    return json.loads(done.stdout)


def collect(repo: str, workflow: str, *, limit: int = 1000, call=gh) -> dict:
    started = utc_now()
    commands = []

    def read(args):
        commands.append('gh ' + ' '.join(args))
        return call(args)

    runs = read(['run', 'list', '--repo', repo, '--workflow', workflow, '--json', RUN_FIELDS, '--limit', str(limit)])
    jobs = {}
    for run in runs:
        jobs[str(run['databaseId'])] = read(['api', f"repos/{repo}/actions/runs/{run['databaseId']}/jobs?per_page=100"])
    record = read(['api', f'repos/{repo}/actions/workflows/{workflow}'])
    return {'schema': RAW_SCHEMA, 'repo': repo, 'workflow': workflow, 'collection_started_utc': started,
            'collection_finished_utc': utc_now(), 'limit': limit, 'commands': commands,
            'read_only': 'gh run list and GET gh api calls only; nothing was written to GitHub',
            'runs': runs, 'jobs': jobs, 'workflow_record': record}


# ------------------------------------------------------------------------------------------------ measure
def cron_of(name: str) -> tuple[str, int, int]:
    """The cron line a probe run's name carries, with its minute and hour."""
    m = NAME.match((name or '').strip())
    if not m:
        raise ValueError(f'{name!r}: not a probe run name (probe <cron line>)')
    line = m.group(1).strip()
    c = CRON.match(line)
    if not c:
        raise ValueError(f'{line!r}: only a daily "M H * * *" line is measured')
    minute, hour = int(c.group(1)), int(c.group(2))
    if not (0 <= minute < 60 and 0 <= hour < 24):
        raise ValueError(f'{line!r}: no such minute or hour')
    return line, minute, hour


def cron_instant(minute: int, hour: int, created: datetime) -> datetime:
    """The latest instant at or before `created` that the daily line `minute hour * * *` names (UTC)."""
    created = created.astimezone(UTC)
    candidate = created.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if candidate > created:
        candidate -= timedelta(days=1)
    return candidate


def nearest_rank(values: list[float], q: float) -> float:
    ordered = sorted(values)
    return ordered[max(0, math.ceil(q * len(ordered)) - 1)]


def spread(values: list[float], p90: bool = False) -> dict | None:
    if not values:
        return None
    out = {'n': len(values), 'min': min(values), 'median': statistics.median(values)}
    if p90:
        out['p90'] = nearest_rank(values, 0.9)
    out['max'] = max(values)
    return out


def merge(raws: list[dict]) -> dict:
    """The raw collections merged by run id; the latest collection's copy of a run (and of its jobs) wins."""
    raws = sorted(raws, key=lambda r: r['collection_started_utc'])
    for raw in raws:
        if raw.get('schema') != RAW_SCHEMA:
            raise ValueError(f"not a raw probe collection: {raw.get('schema')!r}")
    if len({(r['repo'], r['workflow']) for r in raws}) != 1:
        raise ValueError('the raw files are not of one repository and workflow')
    runs, jobs, record = {}, {}, None
    for raw in raws:
        for run in raw['runs']:
            runs[str(run['databaseId'])] = run
        jobs.update({str(k): v for k, v in raw['jobs'].items()})
        record = raw.get('workflow_record') or record
    return {'repo': raws[-1]['repo'], 'workflow': raws[-1]['workflow'], 'runs': runs, 'jobs': jobs,
            'workflow_record': record, 'collected': parse_time(raws[-1]['collection_started_utc']),
            'collections': [{'collection_started_utc': r['collection_started_utc'],
                             'collection_finished_utc': r.get('collection_finished_utc'), 'runs': len(r['runs'])}
                            for r in raws]}


def measure_runs(merged: dict) -> tuple[list[dict], list[dict]]:
    measured, skipped = [], []
    for run_id, run in sorted(merged['runs'].items(), key=lambda kv: kv[1]['createdAt']):
        if run.get('event') != 'schedule':
            skipped.append({'run_id': int(run_id), 'event': run.get('event'), 'reason': 'not a scheduled run'})
            continue
        try:
            line, minute, hour = cron_of(run.get('displayTitle') or run.get('name'))
        except ValueError as exc:
            skipped.append({'run_id': int(run_id), 'event': 'schedule', 'reason': str(exc)})
            continue
        created = parse_time(run['createdAt'])
        instant = cron_instant(minute, hour, created)
        queues = {}
        for job in (merged['jobs'].get(run_id) or {}).get('jobs', []):
            labels = job.get('labels') or []
            label = ','.join(labels) if labels else job.get('name', '?')
            started = job.get('started_at')
            queues[label] = {'job_id': job.get('id'), 'name': job.get('name'), 'status': job.get('status'),
                             'conclusion': job.get('conclusion'), 'started_utc': started,
                             'queue_seconds': None if not started or job.get('status') == 'queued'
                             else (parse_time(started) - created).total_seconds()}
        measured.append({'run_id': int(run_id), 'cron': line, 'hour': hour, 'minute': minute,
                         'cron_utc': stamp(instant), 'cron_day': str(instant.date()), 'created_utc': stamp(created),
                         'delay_seconds': (created - instant).total_seconds(), 'attempt': run.get('attempt'),
                         'status': run.get('status'), 'conclusion': run.get('conclusion'), 'jobs': queues})
    return measured, skipped


def measure(raws: list[dict], *, grace_minutes: float = 60.0, lines: list[str] | None = None) -> dict:
    merged = merge(raws)
    collected = merged['collected']
    runs, skipped = measure_runs(merged)
    hours = {line: cron_of('probe ' + line) for line in {r['cron'] for r in runs} | set(lines or [])}
    hours = dict(sorted(hours.items(), key=lambda kv: (kv[1][2], kv[1][1])))
    grace = timedelta(minutes=grace_minutes)
    record = merged['workflow_record'] or {}
    created_wf = parse_time(record['created_at']) if record.get('created_at') else None
    ran = {(r['cron'], r['cron_utc']) for r in runs}

    def instants(first: date, last: date):
        """Every instant of the probed lines on the days `first`..`last` that is past at the collection and after the
        workflow's creation (when its record is known), in order."""
        day = first
        while day <= last:
            for line, (_, minute, hour) in hours.items():
                at = datetime(day.year, day.month, day.day, hour, minute, tzinfo=UTC)
                if at <= collected and (created_wf is None or at > created_wf):
                    yield line, at
            day += timedelta(days=1)

    def sort_out(found, missed, pending):
        for line, at in found:
            if (line, stamp(at)) not in ran:
                (pending if collected - at < grace else missed).append({'cron': line, 'cron_utc': stamp(at)})

    missed, pending, before = [], [], []
    probe_days: list[str] = []
    observed: list[tuple[str, datetime]] = []
    first_day = min(date.fromisoformat(r['cron_day']) for r in runs) if runs else None
    if first_day is not None:
        probe_days = [str(first_day + timedelta(days=i)) for i in range((collected.date() - first_day).days + 1)]
        observed = list(instants(first_day, collected.date()))
        sort_out(observed, missed, pending)
    if created_wf is not None:
        last = first_day - timedelta(days=1) if first_day is not None else collected.date()
        sort_out(instants(created_wf.date(), last), before, pending)

    per_hour = []
    for line, (_, minute, hour) in hours.items():
        mine = [r for r in runs if r['cron'] == line]
        labels = sorted({label for r in mine for label in r['jobs']})
        per_hour.append({
            'cron': line, 'hour_utc': hour, 'minute': minute,
            'days_observed': sum(l == line for l, _ in observed), 'runs': len(mine),
            'missed': sum(m['cron'] == line for m in missed), 'pending': sum(p['cron'] == line for p in pending),
            'missed_before_first_run': sum(b['cron'] == line for b in before),
            'delay_seconds': spread([r['delay_seconds'] for r in mine], p90=True),
            'queue_seconds': {label: spread([r['jobs'][label]['queue_seconds'] for r in mine
                                             if label in r['jobs'] and r['jobs'][label]['queue_seconds'] is not None])
                              for label in labels},
            'days_with_a_run': sorted({r['cron_day'] for r in mine})})
    return {
        'schema': SCHEMA, 'repo': merged['repo'], 'workflow': merged['workflow'],
        'collected_utc': stamp(collected), 'collections': merged['collections'],
        'workflow_created_utc': stamp(created_wf) if created_wf else None,
        'grace_minutes': grace_minutes, 'lines': list(hours),
        'probe_days': probe_days, 'days_with_a_run': sorted({r['cron_day'] for r in runs}),
        'scheduled_runs': len(runs), 'missed': missed, 'pending': pending, 'missed_before_first_run': before,
        'per_hour': per_hour, 'runs': runs, 'skipped': skipped,
        'method': method(merged, grace_minutes),
    }


def method(merged: dict, grace_minutes: float) -> str:
    return (
        'Source: the raw collections listed under "collections", each made with GitHub\'s CLI read calls only '
        '(gh run list and GET gh api; nothing was written to GitHub): '
        f"gh run list --repo {merged['repo']} --workflow {merged['workflow']} --json {RUN_FIELDS} --limit 1000; "
        f"gh api repos/{merged['repo']}/actions/runs/<id>/jobs?per_page=100 for each listed run; "
        f"gh api repos/{merged['repo']}/actions/workflows/{merged['workflow']} (the workflow's own record). "
        'Scheduled runs only (event schedule). Each run\'s cron line is read from its name (probe <cron line>). '
        'Its cron instant is the latest instant at or before the run\'s createdAt that the line names (minute M of '
        'hour H, UTC), so a run created after midnight for the previous evening\'s line belongs to the previous day. '
        'Scheduler delay = run createdAt - cron instant, in seconds. Queue = job started_at - run createdAt, in '
        'seconds, per runner label (the job\'s labels); a job not yet started has none. Missed: the probe days run '
        'from the first scheduled run\'s cron day through the collection day (UTC; the collection time is the latest '
        'collection\'s start); every cron instant of the probed lines on those days that is past at the collection, '
        'after the workflow\'s creation, with no scheduled run is missed, except one less than '
        f'{grace_minutes:g} minutes before the collection, listed as pending (its run may still be created). '
        'Instants between the workflow\'s creation and the first probe day with no run are listed apart '
        '(missed_before_first_run). Per cron hour: days observed (instants past at the collection on the probe days), '
        'runs, missed, pending, delay min / median / p90 (nearest rank) / max, queue min / median / max per runner '
        'label, and the days that had a run. Raw files merge by run id, the latest collection\'s copy winning.')


def lines_of(workflow_file: Path) -> list[str]:
    """The cron lines a workflow file schedules (the probed lines, so that a line with no run is still counted)."""
    import yaml
    value = yaml.safe_load(Path(workflow_file).read_text())
    on = value.get('on', value.get(True)) or {}
    return [str(c['cron']) for c in on.get('schedule') or []]


# ------------------------------------------------------------------------------------------------ the command
def dump(path: Path, value) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=1, sort_keys=True) + '\n')


def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog='python -m cp18.schedule_probe', description=__doc__.split('\n\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('collect', help='read the probe\'s runs and jobs from GitHub (read-only) into a raw file')
    c.add_argument('--repo', required=True)
    c.add_argument('--workflow', required=True)
    c.add_argument('--limit', type=int, default=1000)
    c.add_argument('--out', required=True, type=Path)
    m = sub.add_parser('measure', help='the delays, queues and missed starts from raw files (no network)')
    m.add_argument('--raw', action='append', required=True, type=Path)
    m.add_argument('--grace-minutes', type=float, default=60.0)
    m.add_argument('--line', action='append', default=[], help='a probed cron line to expect even if no run carries it')
    m.add_argument('--workflow-file', type=Path, help="the probe's workflow file: its cron lines are the probed lines")
    m.add_argument('--out', required=True, type=Path)
    return ap


def main(argv=None) -> int:
    args = parser().parse_args(argv)
    if args.cmd == 'collect':
        value = collect(args.repo, args.workflow, limit=args.limit)
        dump(args.out, value)
        print('collected', len(value['runs']), 'runs of', args.workflow, 'at', value['collection_started_utc'])
        return 0
    lines = list(args.line) + (lines_of(args.workflow_file) if args.workflow_file else [])
    value = measure([json.loads(Path(p).read_text()) for p in args.raw], grace_minutes=args.grace_minutes,
                    lines=lines)
    dump(args.out, value)
    print('measured', value['scheduled_runs'], 'scheduled runs |', len(value['probe_days']), 'probe days |',
          len(value['missed']), 'missed |', len(value['pending']), 'pending |', len(value['missed_before_first_run']),
          'missed before the first run')
    return 0


if __name__ == '__main__':
    sys.exit(main())
