"""The daily operation's alert (CP-18d, the Orchestrator's ruling O54): nobody has to watch. Standard library only, run
as a file (`python3 src/cp18/alert.py`) by each link of the chain after its work, with `issues: write` and nothing more.

**What opens or comments on an issue** in the product repository (GitHub emails the Owner):
- `failed`: a job of this link (the acquisition, the run, or the chain's own tick) failed;
- `not_issued`: a recent delivery day closed as not issued, with its cause (`cp18.causes`);
- `fetched_after_cutoff`: a recent delivery day issued with its load forecast fetched after the cutoff (the Owner's
  decision 31), with that copy's retrieval time.

**One open issue per problem**, found by its fixed title among the open issues the workflow's own bot opened. A new
occurrence is a comment on it; a day or a run already named in it is not repeated. **It closes itself** (a comment,
then closed) once a later delivery day is issued with all inputs before the cutoff, in a link that itself failed in
nothing. The text carries the day, the cause and the run's link, and nothing else: no credential, and no value derived
from one. Its wording names the load forecast's retrieval, never "late" or "timely" (§24.13).

**The facts** are read from the store on `main` after the link's records were pushed (`live/store`: the ledger, each
issued day's record for its input class, each closed day's cause), without the project's environment. Only recent days
count: a delivery day on or after the target day less `RECENT_DAYS`, so the record's older history never re-alerts.

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
RECENT_DAYS = 5
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
DAY = re.compile(r'\b(20\d\d-\d\d-\d\d)\b')


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


def problems(value: dict, failed: list[str], run_url: str, since: date, day_of_link: str | None) -> list[dict]:
    """This link's problems: each with its kind, day and line of text."""
    out = []
    for job in failed:
        out.append({'kind': 'failed', 'day': day_of_link, 'key': run_url,
                    'line': f"{day_of_link or 'the chain'}: the {job} job failed. Run: {run_url}"})
    for item in value['not_issued']:
        if date.fromisoformat(item['day']) >= since:
            out.append({'kind': 'not_issued', 'day': item['day'], 'key': item['day'],
                        'line': f"{item['day']}: not issued ({item['cause']}). Run: {run_url}"})
    for item in value['issued']:
        if item['input_class'] == 'load_forecast_after_cutoff' and date.fromisoformat(item['day']) >= since:
            out.append({'kind': 'fetched_after_cutoff', 'day': item['day'], 'key': item['day'],
                        'line': (f"{item['day']}: issued with the load forecast fetched after the cutoff, at "
                                 f"{item['fetched_utc']} (UTC). Run: {run_url}")})
    return out


def _text(api, issue: dict) -> str:
    comments = api.request('GET', f"issues/{issue['number']}/comments?per_page=100") or []
    return '\n'.join([issue.get('body') or ''] + [c.get('body') or '' for c in comments])


def alert(api, value: dict, found: list[dict], run_url: str) -> list[dict]:
    """Open, comment on, or close the issues; returns what was done."""
    done = []
    open_issues = [i for i in (api.request('GET', 'issues?state=open&per_page=100') or [])
                   if (i.get('user') or {}).get('login') == BOT and i.get('title') in TITLES.values()
                   and 'pull_request' not in i]
    by_title = {i['title']: i for i in open_issues}
    for kind, title in TITLES.items():
        mine = [p for p in found if p['kind'] == kind]
        issue = by_title.get(title)
        if mine:
            if issue is None:
                body = INTRO[kind] + '\n\n' + '\n'.join(f'- {p["line"]}' for p in mine) + \
                    '\n\nThis issue closes itself once a later delivery day is issued with all inputs before the cutoff.'
                made = api.request('POST', 'issues', {'title': title, 'body': body})
                done.append({'kind': kind, 'did': 'opened', 'number': (made or {}).get('number'),
                             'keys': [p['key'] for p in mine]})
                continue
            text = _text(api, issue)
            new = [p for p in mine if p['key'] not in text]
            if new:
                api.request('POST', f"issues/{issue['number']}/comments",
                            {'body': '\n'.join(f'- {p["line"]}' for p in new)})
                done.append({'kind': kind, 'did': 'commented', 'number': issue['number'],
                             'keys': [p['key'] for p in new]})
            continue
        if issue is None or any(p['kind'] == 'failed' for p in found):
            continue
        # closed once a later day issues with all inputs before the cutoff
        named = [d for d in DAY.findall(_text(api, issue))]
        before = [i['day'] for i in value['issued'] if i['input_class'] == 'before_cutoff']
        latest = max(before) if before else None
        if latest and named and latest > max(named):
            api.request('POST', f"issues/{issue['number']}/comments",
                        {'body': f'Closed: {latest} was issued with all inputs before the cutoff. Run: {run_url}'})
            api.request('PATCH', f"issues/{issue['number']}", {'state': 'closed', 'state_reason': 'completed'})
            done.append({'kind': kind, 'did': 'closed', 'number': issue['number'], 'by': latest})
    return done


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
    since = C.target_day(now) - timedelta(days=RECENT_DAYS)
    value = facts(args.store)
    found = problems(value, [f for f in args.failed if f], args.run_url, since, args.day or None)
    done = alert(C.Api(args.repo), value, found, args.run_url)
    print(json.dumps({'problems': found, 'done': done}, sort_keys=True))
    return 0


if __name__ == '__main__':
    sys.exit(main())
