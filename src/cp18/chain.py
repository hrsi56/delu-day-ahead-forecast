"""The daily operation as a self-dispatching chain (CP-18d, the Orchestrator's ruling O54): fire and forget, robust to
GitHub's scheduler. Standard library only, run as a file (`python3 src/cp18/chain.py`) on a bare `ubuntu` runner.

**Why a chain.** The schedule probe measured this repository's scheduled runs created 6 h 11 min to 7 h 36 min after
their cron time on its first night, the delay growing by about half an hour an hour; the first runner day had no
scheduled run at all before the cutoff. O54 asks the daily operation to keep acquiring and issuing every day when the
scheduler is late by up to 12 hours or drops most of a day's events. An hourly event through a gate covers any delay
only while some event still arrives in each day's band (about 11 hours before the cutoff): with most events dropped,
whole days go uncovered (`tests/cp18d/test_chain.py` simulates both). So the daily work no longer waits for the
scheduler. Each link of the chain is one workflow run started by `workflow_dispatch`, which GitHub starts at once:

1. **tick** (Linux): reads the store's run records on `main` and the previous link's state, and decides the next
   action and when it is due (`decide`): D's acquisition from 5.5 h before D's cutoff (`window.LEAD_HOURS`), the run for
   the target day 5 min after its cutoff, retries with their backoffs. It sleeps until the action is due, at most 5.75 h
   (`window.MAX_SLEEP_HOURS`, inside GitHub's 6-hour job limit), then decides again: the action, or none.
2. **acquire** or **run** (macOS), when the tick says so: CP-18c's jobs, unchanged in what they do.
3. **alert** (Linux, `issues: write`): `cp18.alert`.
4. **next** (Linux, `actions: write` only): dispatches the next link with this link's state (`next_link`).

**One chain at a time.** Every link runs in one concurrency group, which GitHub keeps to one running run and one pending
run, cancelling the older pending one when another queues: a second chain dies at its next link. Two acquisitions are
never in flight together, so two never write the same day.

**Re-seeding.** The scheduled events are only seeds now (`seed`): each lists the workflow's runs and dispatches a new
chain only when no link is queued or in progress. A chain breaks only if a dispatch fails (`next_link` retries) or a link
is cancelled by hand; any one seed that arrives afterwards, however late, restarts it.

**Not issued is not missing.** A run's records stay the evidence: the run for the target day is the store's run record
on `main` (`live/store/runs/*.json`, its `target_day` and `exit`), read here without the project's environment.

    python3 src/cp18/chain.py tick --store live/store [--last <state JSON>] [--force run|acquire] [--sleep] [--now ISO]
    python3 src/cp18/chain.py next --repo <owner/name> --action A --day D --tick-result R --acquire-result R
        --run-result R [--shown true|false] [--stopped margin|'its stop-by']               (GH_TOKEN in the environment)
    python3 src/cp18/chain.py seed --repo <owner/name>                           (GH_TOKEN in the environment)
"""
from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta, timezone
import json
import os
from pathlib import Path
import sys
import time
import urllib.error
import urllib.request

try:
    from . import window as W
except ImportError:                     # run as a file on a bare runner: the module beside this one
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import window as W                  # type: ignore[no-redef]

UTC = timezone.utc
RUN_DELAY = timedelta(minutes=5)          # the run for D, after D's cutoff
RUN_RETRY_AFTER = timedelta(hours=3)      # a run that left its target day open is retried after this
RUN_ATTEMPTS = 3                          # runs recorded for one target day, at most
RUN_BACKOFF = timedelta(hours=2)          # after a run job that failed before recording its run
ACQUIRE_BACKOFF = timedelta(minutes=10)   # after an acquisition job that failed
MARGIN = timedelta(seconds=W.MARGIN_SECONDS)
MAX_SLEEP = timedelta(hours=W.MAX_SLEEP_HOURS)
WORKFLOW = 'daily.yml'
CHAIN_MODES = ('chain', 'live', 'acquire-live')
PENDING = ('queued', 'in_progress', 'waiting', 'requested', 'pending')
#: A run record's status of its target day that decides it (`cp18.pipeline`): issued, decided by another run or host,
#: closed as not issued by the chain. An `open` target day (its inputs, or S_14, not in place) is retried.
DECIDED = ('issued', 'decided elsewhere', 'not issued', 'lost the claim')
API = 'https://api.github.com'


def _z(value: datetime) -> str:
    return value.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%SZ')


def _instant(text) -> datetime | None:
    if not text:
        return None
    value = datetime.fromisoformat(str(text).replace('Z', '+00:00'))
    return value.astimezone(UTC) if value.tzinfo else None


def target_day(now: datetime) -> date:
    """The latest delivery day whose cutoff has passed (`cp18.plan.target_day`)."""
    return W.next_day(now) - timedelta(days=1)


def runs_on_main(store) -> list[dict]:
    """The store's run records (`live/store/runs/*.json`): each run's target day, its exit, the target day's own status
    in it (a run exits 1 when any day of its lookback stays open, even with its target day issued) and its times."""
    out = []
    for path in sorted(Path(store, 'runs').glob('*.json')):
        value = json.loads(path.read_text())
        target = value.get('target_day')
        out.append({'run_id': value.get('run_id'), 'target_day': target, 'exit': value.get('exit'),
                    'target_status': ((value.get('days') or {}).get(target) or {}).get('status'),
                    'started_utc': value.get('started_utc'), 'finished_utc': value.get('finished_utc')})
    return out


def decide(now: datetime, last: dict | None, runs: list[dict], force: str | None = None) -> dict:
    """The next action of the chain at `now`: `run`, `acquire` or `none`, its delivery day, and how long to sleep first
    (0 when it is due now; at most `MAX_SLEEP`, after which the tick decides again)."""
    now = now.astimezone(UTC)
    last = last or {}
    target = target_day(now)
    nxt = target + timedelta(days=1)
    out = {'now_utc': _z(now), 'target_day': str(target), 'action': 'none', 'day': None, 'sleep_seconds': 0,
           'reason': ''}
    if force in ('run', 'acquire'):
        return dict(out, action=force, day=str(target if force == 'run' else nxt),
                    reason=f'dispatched by hand: {force} at once')
    due = []                                                            # (instant, action, day, reason)
    mine = [r for r in runs if r.get('target_day') == str(target)]
    decided = any(r.get('exit') == 0 or r.get('target_status') in DECIDED for r in mine)
    if not decided:
        at = W.cutoff(target) + RUN_DELAY
        reason = f'the run for {target}, after its cutoff'
        if mine:
            finished = max((_instant(r.get('finished_utc')) or _instant(r.get('started_utc')) or at) for r in mine)
            at, reason = max(at, finished + RUN_RETRY_AFTER), f'{target} left open by its last run: a retry'
            if len(mine) >= RUN_ATTEMPTS:
                at = None
        if at is not None and last.get('action') == 'run' and last.get('day') == str(target) \
                and last.get('result') != 'success':
            at, reason = max(at, (_instant(last.get('at')) or now) + RUN_BACKOFF), 'the last run job failed: a retry'
        if at is not None:
            due.append((at, 'run', target, reason))
    start, limit = W.cutoff(nxt) - timedelta(hours=W.LEAD_HOURS), W.cutoff(nxt) - MARGIN
    finished = (last.get('action') == 'acquire' and last.get('day') == str(nxt) and last.get('result') == 'success'
                and (last.get('shown') or str(last.get('stopped') or '').startswith(('margin', 'the cutoff'))))
    if not finished:
        at, reason = start, f'{nxt}\'s acquisition, before its cutoff'
        if last.get('action') == 'acquire' and last.get('day') == str(nxt) and last.get('result') != 'success':
            at, reason = max(at, (_instant(last.get('at')) or now) + ACQUIRE_BACKOFF), 'the last acquisition failed: a retry'
        if at < limit:
            due.append((at, 'acquire', nxt, reason))
    wake = W.cutoff(nxt) + RUN_DELAY                                    # the next target day's run, at the latest
    ready = sorted((d for d in due if d[0] <= now), key=lambda d: (d[1] != 'run', d[0]))
    if ready:
        _, action, day, reason = ready[0]
        return dict(out, action=action, day=str(day), reason=reason)
    soonest = min([d[0] for d in due] + [wake])
    sleep = min(soonest - now, MAX_SLEEP)
    return dict(out, sleep_seconds=int(sleep.total_seconds()), wake_utc=_z(now + sleep),
                reason=f'nothing due before {_z(soonest)}')


# ------------------------------------------------------------------------------------------------ the GitHub API
class Api:
    """GitHub's REST API with the job's token, read from the environment inside this process and never printed."""

    def __init__(self, repo: str, token_env: str = 'GH_TOKEN', base: str = API):
        self.repo, self.base, self._env = repo, base, token_env

    def request(self, method: str, path: str, body: dict | None = None):
        token = os.environ.get(self._env)
        if not token:
            raise RuntimeError(f'no {self._env} in the environment')
        req = urllib.request.Request(f'{self.base}/repos/{self.repo}/{path.lstrip("/")}', method=method,
                                     data=None if body is None else json.dumps(body).encode(),
                                     headers={'Accept': 'application/vnd.github+json',
                                              'X-GitHub-Api-Version': '2022-11-28',
                                              'Authorization': f'Bearer {token}',
                                              'User-Agent': 'delu-daily-chain'})
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = resp.read()
        except urllib.error.HTTPError as exc:
            raise RuntimeError(f'GitHub API {method} {path}: HTTP {exc.code}') from None
        return json.loads(data) if data else None


def alive(api, exclude: int | None = None) -> list[dict]:
    """The chain's links that are queued or in progress (a `workflow_dispatch` run of a chain mode)."""
    value = api.request('GET', f'actions/workflows/{WORKFLOW}/runs?event=workflow_dispatch&per_page=100')
    out = []
    for run in (value or {}).get('workflow_runs', []):
        title = run.get('display_title') or ''
        if run.get('status') in PENDING and run.get('id') != exclude and \
                any(title == f'daily {m}' or title.startswith(f'daily {m} ') for m in CHAIN_MODES):
            out.append({'id': run.get('id'), 'status': run.get('status'), 'title': title})
    return out


def dispatch(api, state: dict, ref: str = 'main', mode: str = 'chain', extra: dict | None = None,
             attempts: int = 3, sleep=time.sleep) -> dict:
    """The next link: `workflow_dispatch` of this workflow, with this link's state. Retried; never more than one."""
    body = {'ref': ref, 'inputs': {'mode': mode, 'last': json.dumps(state, sort_keys=True), **(extra or {})}}
    errors = []
    for i in range(attempts):
        try:
            api.request('POST', f'actions/workflows/{WORKFLOW}/dispatches', body)
            return {'dispatched': True, 'attempts': i + 1, 'errors': errors}
        except Exception as exc:  # noqa: BLE001 - retried, then recorded; a seed restarts a broken chain
            errors.append(str(exc))
            sleep(30 * (i + 1))
    return {'dispatched': False, 'attempts': attempts, 'errors': errors}


def link_state(action: str, day: str | None, results: dict, shown: str = '', stopped: str = '',
               now: datetime | None = None) -> dict:
    """This link's state for the next one: its action and day, that action's job result (the tick's when it did
    nothing), and, for an acquisition, whether it showed the forecast and why it stopped."""
    result = results.get(action) or results.get('tick') or ''
    state = {'action': action or 'none', 'day': day or None, 'result': result, 'at': _z(now or datetime.now(UTC))}
    if action == 'acquire':
        state.update(shown=shown == 'true', stopped=stopped or None)
    return state


def seed(api, ref: str = 'main') -> dict:
    """A scheduled event: start a chain only if none is queued or in progress."""
    links = alive(api)
    if links:
        return {'seeded': False, 'reason': f'a chain is alive ({len(links)} link(s))', 'links': links}
    return {'seeded': True, **dispatch(api, {'seeded_utc': _z(datetime.now(UTC))}, ref)}


# ------------------------------------------------------------------------------------------------ the command line
def _outputs(value: dict) -> None:
    for key in ('action', 'day', 'sleep_seconds', 'target_day', 'reason'):
        print(f"{key}={'' if value.get(key) is None else value[key]}")
    print('state=' + json.dumps({k: value.get(k) for k in ('action', 'day', 'now_utc')}, sort_keys=True))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='chain.py')
    sub = ap.add_subparsers(dest='cmd', required=True)
    t = sub.add_parser('tick')
    t.add_argument('--store', default='live/store', type=Path)
    t.add_argument('--last', default='')
    t.add_argument('--force', choices=('run', 'acquire'))
    t.add_argument('--sleep', action='store_true', help='sleep until the action is due (at most 5.75 h), then decide again')
    t.add_argument('--now')
    n = sub.add_parser('next')
    n.add_argument('--repo', required=True)
    n.add_argument('--state', help='the state as JSON (a rehearsal); else from the link\'s results below')
    n.add_argument('--action', default='')
    n.add_argument('--day', default='')
    n.add_argument('--tick-result', default='')
    n.add_argument('--acquire-result', default='')
    n.add_argument('--run-result', default='')
    n.add_argument('--shown', default='')
    n.add_argument('--stopped', default='')
    n.add_argument('--ref', default='main')
    n.add_argument('--mode', default='chain')
    n.add_argument('--links', default='')
    s = sub.add_parser('seed')
    s.add_argument('--repo', required=True)
    s.add_argument('--ref', default='main')
    args = ap.parse_args(argv)
    if args.cmd == 'tick':
        last = json.loads(args.last) if args.last.strip() else None
        runs = runs_on_main(args.store) if Path(args.store).is_dir() else []
        now = _instant(args.now) if args.now else datetime.now(UTC)
        value = decide(now, last, runs, args.force)
        print(json.dumps(value, sort_keys=True), file=sys.stderr)
        if args.sleep and value['sleep_seconds'] > 0:
            time.sleep(value['sleep_seconds'])
            now = now + timedelta(seconds=value['sleep_seconds']) if args.now else datetime.now(UTC)
            value = decide(now, last, runs)
            if value['sleep_seconds'] > 0:                  # still nothing due: this link ends, the next one waits
                value = dict(value, action='none')
            print(json.dumps(value, sort_keys=True), file=sys.stderr)
        _outputs(value)
        return 0
    api = Api(args.repo)
    if args.cmd == 'next':
        state = json.loads(args.state) if args.state else link_state(
            args.action, args.day, {'tick': args.tick_result, 'acquire': args.acquire_result, 'run': args.run_result},
            args.shown, args.stopped)
        print(json.dumps({'state': state}, sort_keys=True))
        value = dispatch(api, state, args.ref, args.mode, {'links': args.links} if args.links else None)
    else:
        value = seed(api, args.ref)
    print(json.dumps(value, sort_keys=True))
    return 0 if value.get('dispatched', True) else 1


if __name__ == '__main__':
    raise SystemExit(main())
