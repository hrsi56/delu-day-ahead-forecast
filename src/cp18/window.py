"""The acquisition's gate (CP-18d, decision 31's experiment): when a scheduled event that arrived at `now` should start
D's acquisition. Standard library only, run as a file (`python3 src/cp18/window.py`) on a bare `ubuntu` runner before
any environment is installed, so an event that arrives too early costs a sleeping Linux job, not a macOS runner.

**Why.** The Orchestrator's schedule probe measured GitHub's scheduler starting this repository's jobs 6 h 11 min to
7 h 36 min after their cron time overnight on 2026-11-15, the delay growing by about half an hour each hour
(`reports/cp18d/schedule-probe.json`). No fixed cron time can then be placed before D's cutoff. So the acquisition is
scheduled every hour, and each arriving event passes this gate:

- D is the next delivery day whose cutoff (D−1 11:00 Europe/Berlin, `cp25.guard.issue_time`) is still ahead.
- **Start** = D's cutoff less `lead_hours` (5.5 h: 04:30 UTC in winter, 03:30 UTC in summer). From the start, one
  acquisition polls through the load forecast's publication (seen first between 09:03 and 09:17 UTC on the live
  record's winter days) until the cutoff's margin, inside GitHub's 6-hour job limit.
- An event arriving **after the start** (and before the cutoff's margin) starts the acquisition at once.
- An event arriving **before the start, by at most `max_sleep_hours`** (5.75 h) sleeps in its gate job until the start,
  then starts the acquisition.
- An event arriving **earlier still** does nothing ("not yet"); a later event will come.

So any one event arriving in a band of about 11 hours before D's cutoff starts D's acquisition in time, whatever the
scheduler's delay: the schedule is robust to a delay that keeps growing, as long as the scheduler still delivers some
event in that band. The acquisitions run one at a time (the workflow's concurrency group), and an acquisition that
finds nothing missing writes nothing, so a later event inside the band does no harm.

    python3 src/cp18/window.py [--now <ISO 8601 with offset>] [--lead-hours 5.5] [--max-sleep-hours 5.75]

prints `go=true|false`, `sleep_seconds=N`, `day=…`, `cutoff_utc=…`, `start_utc=…`, `reason=…` (for `$GITHUB_OUTPUT`).
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

UTC = timezone.utc
BERLIN = ZoneInfo('Europe/Berlin')
LEAD_HOURS = 5.5
MAX_SLEEP_HOURS = 5.75
MARGIN_SECONDS = 120 + 300          # the acquisition's cutoff margin and one poll: no start closer than this


def cutoff(day: date) -> datetime:
    """D−1 11:00 Europe/Berlin, as UTC (the same instant as `cp25.guard.issue_time(day)`)."""
    return datetime.combine(day - timedelta(days=1), time(11, 0), tzinfo=BERLIN).astimezone(UTC)


def next_day(now: datetime) -> date:
    """The next delivery day whose cutoff is still ahead of `now` (as `cp18.acquire.next_day`)."""
    day = now.astimezone(BERLIN).date()
    while cutoff(day) <= now:
        day += timedelta(days=1)
    while cutoff(day - timedelta(days=1)) > now:
        day -= timedelta(days=1)
    return day


def plan(now: datetime, lead_hours: float = LEAD_HOURS, max_sleep_hours: float = MAX_SLEEP_HOURS) -> dict:
    if now.tzinfo is None:
        raise ValueError('a naive instant')
    now = now.astimezone(UTC)
    day = next_day(now)
    limit = cutoff(day)
    start = limit - timedelta(hours=lead_hours)
    out = {'now_utc': _z(now), 'day': str(day), 'cutoff_utc': _z(limit), 'start_utc': _z(start), 'go': False,
           'sleep_seconds': 0, 'reason': ''}
    if limit - now <= timedelta(seconds=MARGIN_SECONDS):
        out['reason'] = f'{day}\'s cutoff is too close to poll; the run after it handles the day'
    elif now >= start:
        out.update(go=True, reason=f'inside {day}\'s acquisition window: start now')
    elif start - now <= timedelta(hours=max_sleep_hours):
        out.update(go=True, sleep_seconds=int((start - now).total_seconds()),
                   reason=f'sleep until {day}\'s acquisition starts ({_z(start)})')
    else:
        out['reason'] = f'not yet: {day}\'s acquisition starts at {_z(start)}, more than {max_sleep_hours:g} h away'
    return out


def _z(value: datetime) -> str:
    return value.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='window.py')
    ap.add_argument('--now', help='the instant (default: the real clock)')
    ap.add_argument('--lead-hours', type=float, default=LEAD_HOURS)
    ap.add_argument('--max-sleep-hours', type=float, default=MAX_SLEEP_HOURS)
    args = ap.parse_args(argv)
    now = datetime.fromisoformat(args.now.replace('Z', '+00:00')) if args.now else datetime.now(UTC)
    value = plan(now, args.lead_hours, args.max_sleep_hours)
    for key in ('go', 'sleep_seconds', 'day', 'cutoff_utc', 'start_utc', 'reason'):
        item = value[key]
        print(f"{key}={str(item).lower() if isinstance(item, bool) else item}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
