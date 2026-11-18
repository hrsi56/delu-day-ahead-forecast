"""The daily operation's alert (CP-18d, the Orchestrator's ruling O54): nobody has to watch. Standard library only, run
as a file (`python3 src/cp18/alert.py`) by each link of the chain after its work, with `issues: write` and nothing more.

**What opens or comments on an issue** in the product repository (GitHub emails the Owner):
- `failed`: a job of this link (the acquisition, the run, or the chain's own tick) failed;
- `not_issued`: a recent delivery day closed as not issued, with its cause (`cp18.causes`);
- `fetched_after_cutoff`: a recent delivery day issued with its load forecast fetched after the cutoff (the Owner's
  decision 31), with that copy's retrieval time.

**One issue per problem**, found by its fixed title among the issues the workflow's own bot opened. Each problem has
a line of its own, which starts with its delivery day (`- YYYY-MM-DD: `) and carries its key: the day and what happened
to it, or a failed run's link. A problem whose key is already in any of the bot's alert issues, open or closed, has
been reported and is never reported again; a new one opens the issue (or a new one, if the last was closed) or is a
comment on the open one. **An open issue closes itself** (a comment, then closed) in the first link that reports no new
problem of its kind and has no failed job, once a delivery day later than every day named on its problem lines has
been issued with all inputs before the cutoff. A failed job's line is dated by the link's day, or by the target day when
the link failed before it had one, so it closes the same way. The text carries the day, the cause and the run's link,
and nothing else: no credential, and no value derived from one. Its wording names the load forecast's retrieval, never
"late" or "timely" (§24.13).

**The facts** are read from the store on `main` after the link's records were pushed (`live/store`: the ledger, each
issued day's record for its input class, each closed day's cause), without the project's environment. Only recent days
count: a delivery day on or after the target day less `RECENT_DAYS` (decision 23's lookback and one day, so a day closed
when it leaves the lookback is still reported once), so the record's older history never alerts.

    python3 src/cp18/alert.py --repo <owner/name> --store live/store --run-url <url> [--failed <job> ...]  (GH_TOKEN)
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys

try:
    from . import chain as C
except ImportError:                     # run as a file on a bare runner: the module beside this one
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import chain as C                  # type: ignore[no-redef]

UTC = timezone.utc
BOT = 'github-actions[bot]'
RECENT_DAYS = 4
TITLES = {
    'failed': 'Daily operation: a daily run did not finish',
    'not_issued': 'Daily operation: a delivery day was not issued',
    'fetched_after_cutoff': 'Daily operation: a delivery day was issued with the load forecast fetched after the cutoff',
}
INTRO = {
    'failed': 'A job of the daily operation failed. The chain continues; the next link retries what is still due.',
    'not_issued': ('A delivery day was closed as not issued. It stays shown as not issued, with its cause, on the '
                   'Space and in the store.'),
    'fetched_after_cutoff': ("A delivery day's load forecast was not retrieved before its cutoff (D-1 11:00 "
                             "Europe/Berlin), so by the Owner's decision 31 it was issued with the copy fetched after "
                             'the cutoff, labelled so on the Space; the evaluation reports such days apart.'),
}
LINE_DAY = re.compile(r'^- (20\d\d-\d\d-\d\d): ', re.M)   # a problem line's own day


def facts(store) -> dict:
    """The decided days in the store: each issued day with its input class, each closed day with its cause."""
    store = Path(store)
    issued, not_issued = [], []
    for line in (store / 'ledger.jsonl').read_text().splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        if entry.get('kind') == 'issuance':
            record = json.loads((store / entry['record_file']).read_text())
            cls = record.get('input_class') or 'before_cutoff'      # a CP-18a-c record: before the cutoff (verified)
            if entry.get('issued_policy'):
                issued.append({'day': entry['day'], 'input_class': cls,
                               'fetched_utc': record.get('load_forecast_fetched_utc')})
            else:
                not_issued.append({'day': entry['day'], 'cause': 'a failed issuance by the chain'})
        elif entry.get('kind') == 'not_issued':
            not_issued.append({'day': entry['day'], 'cause': entry.get('cause_text') or entry.get('cause')})
    return {'issued': issued, 'not_issued': not_issued}


def problems(value: dict, failed: list[str], run_url: str, since: date, day_of_link: str) -> list[dict]:
    """This link's problems: each with its kind, its day, its key (unique in the issues' text) and its line."""
    out = []
    for job in failed:
        out.append({'kind': 'failed', 'day': day_of_link, 'key': f'Run: {run_url}',
                    'line': f"- {day_of_link}: the {job} job failed. Run: {run_url}"})
    for item in value['not_issued']:
        if date.fromisoformat(item['day']) >= since:
            key = f"- {item['day']}: not issued"
            out.append({'kind': 'not_issued', 'day': item['day'], 'key': key,
                        'line': f"{key} ({item['cause']}). Run: {run_url}"})
    for item in value['issued']:
        if item['input_class'] == 'load_forecast_after_cutoff' and date.fromisoformat(item['day']) >= since:
            key = f"- {item['day']}: issued with the load forecast fetched after the cutoff"
            out.append({'kind': 'fetched_after_cutoff', 'day': item['day'], 'key': key,
                        'line': f"{key}, at {item['fetched_utc']} (UTC). Run: {run_url}"})
    return out


def _text(api, issue: dict) -> str:
    comments = api.request('GET', f"issues/{issue['number']}/comments?per_page=100") or []
    return '\n'.join([issue.get('body') or ''] + [c.get('body') or '' for c in comments])


def _mine(api) -> list[dict]:
    """The bot's alert issues, open and closed (the memory of what was reported)."""
    out = []
    for page in range(1, 11):
        batch = api.request('GET', f'issues?state=all&per_page=100&page={page}') or []
        out += [i for i in batch if (i.get('user') or {}).get('login') == BOT and i.get('title') in TITLES.values()
                and 'pull_request' not in i]
        if len(batch) < 100:
            break
    return out


def alert(api, value: dict, found: list[dict], run_url: str) -> list[dict]:
    """Open, comment on, or close the issues; returns what was done."""
    done = []
    issues = _mine(api)
    texts = {i['number']: _text(api, i) for i in issues}
    reported = '\n'.join(texts.values())
    before = [i['day'] for i in value['issued'] if i['input_class'] == 'before_cutoff']
    latest = max(before) if before else None
    failed_here = any(p['kind'] == 'failed' for p in found)
    for kind, title in TITLES.items():
        new = [p for p in found if p['kind'] == kind and p['key'] not in reported]
        issue = next((i for i in issues if i['title'] == title and i.get('state') == 'open'), None)
        if new:
            if issue is None:
                body = INTRO[kind] + '\n\n' + '\n'.join(p['line'] for p in new) + \
                    '\n\nThis issue closes itself once a later delivery day is issued with all inputs before the cutoff.'
                made = api.request('POST', 'issues', {'title': title, 'body': body})
                done.append({'kind': kind, 'did': 'opened', 'number': (made or {}).get('number'),
                             'keys': [p['key'] for p in new]})
            else:
                api.request('POST', f"issues/{issue['number']}/comments", {'body': '\n'.join(p['line'] for p in new)})
                done.append({'kind': kind, 'did': 'commented', 'number': issue['number'],
                             'keys': [p['key'] for p in new]})
            continue
        if issue is None or failed_here:
            continue
        named = LINE_DAY.findall(texts[issue['number']])
        if latest and named and latest > max(named):
            api.request('POST', f"issues/{issue['number']}/comments",
                        {'body': f'Closed: {latest} was issued with all inputs before the cutoff. Run: {run_url}'})
            api.request('PATCH', f"issues/{issue['number']}", {'state': 'closed', 'state_reason': 'completed'})
            done.append({'kind': kind, 'did': 'closed', 'number': issue['number'], 'by': latest})
    return done


#: The API the command uses (tests replace it with a recorded one).
API = C.Api


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='alert.py')
    ap.add_argument('--repo', required=True)
    ap.add_argument('--store', default='live/store', type=Path)
    ap.add_argument('--run-url', required=True)
    ap.add_argument('--failed', action='append', default=[], help='a job of this link that failed')
    ap.add_argument('--day', default='', help="the link's delivery day (its action's)")
    ap.add_argument('--now')
    args = ap.parse_args(argv)
    now = C._instant(args.now) if args.now else datetime.now(UTC)
    target = C.target_day(now)
    since = target - timedelta(days=RECENT_DAYS)
    value = facts(args.store)
    found = problems(value, [f for f in args.failed if f], args.run_url, since, args.day or str(target))
    done = alert(API(args.repo), value, found, args.run_url)
    print(json.dumps({'problems': found, 'done': done}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
