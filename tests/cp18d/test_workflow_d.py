"""CP-18d items 2, 4 and 5 in `daily.yml`: static checks, the conditions evaluated as CP-18c's tests evaluate them.

What is checked: the three concurrency groups and the events each one holds; the acquisition's cron list, the same in
`on.schedule` and the acquire job's `if:`, beside the unchanged run crons; each acquisition start and its stop-by
inside GitHub's 6-hour job limit with the timeout, on every day of two years; the rehearsal modes (dispatch only,
`contents: read`, no secret, development days only, their shell checks executed); the runner's artifact keeping the
whole Space build with hidden files, recorded before the fitted arrays are deleted; and what stays as it was (the run
crons, the keep-alive and the 60-day rule, the repository guard, the secrets per step, the dry run's set-aside).
History-free; no platform requirement beyond bash.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import re
import subprocess

import pytest

from cp18c.test_workflow import (ACQUIRE_CRONS, JOBS, ON, PRODUCT, RUN_CRONS, TEXT, WF, _cron_time, evaluate, selected,
                                 step, steps)
from cp25 import guard

HEADER = TEXT.split('\nname: daily')[0]
SCRATCH = 'hrsi56/delu-pipeline-dryrun'
GROUPS = ('dry-run', 'chain-dry-run', 'seed', 'chain')
#: The jobs each group may hold.
MEMBERS = {'dry-run': {'dry-run', 'acquire-dry-run'}, 'chain-dry-run': {'chain-dry-run'}, 'seed': {'seed', 'keep-alive'},
           'chain': {'tick', 'acquire', 'run', 'alert', 'next'}}
UTC = timezone.utc
LIVE_ONLY = ('--late-day', '--rehearse-moved-main', '--rehearsal', '--clock-start', '--published-after-minutes')


def one_line(script: str) -> str:
    """A run script's command with its line continuations joined and its spaces collapsed."""
    return re.sub(r'\s+', ' ', script.replace('\\\n', ' ')).strip()


def fromjson_list(expression: str) -> list[str]:
    (found,) = re.findall(r"fromJSON\('(.*?)'\)", expression)
    return json.loads(found)


# ------------------------------------------------------------------------------------------------ concurrency
def group_of(**ctx) -> str:
    ctx.setdefault('repository', PRODUCT)
    raw = WF['concurrency']['group']
    assert raw.startswith('daily-${{') and raw.endswith('}}'), raw
    inner = raw[len('daily-${{'):-2]
    hits = [g for g in GROUPS if evaluate(f"({inner}) == '{g}'", ctx)]
    assert len(hits) == 1, (ctx, hits)
    return hits[0]


EVENTS = ([({'event': 'workflow_dispatch', 'mode': m, 'var': 'enabled', 'action': a}, g) for m, a, g in
           [('dry-run', '', 'dry-run'), ('acquire-dry-run', '', 'dry-run'), ('chain-dry-run', '', 'chain-dry-run'),
            ('acquire-live', 'acquire', 'chain'), ('live', 'run', 'chain'), ('chain', 'acquire', 'chain'),
            ('chain', 'run', 'chain'), ('chain', 'none', 'chain')]] +
          [({'event': 'schedule', 'schedule': c, 'var': 'enabled'}, 'seed') for c in ACQUIRE_CRONS + RUN_CRONS])


@pytest.mark.parametrize('ctx, group', EVENTS,
                         ids=[f"{c['event']}:{c.get('mode') or c.get('schedule')}:{c.get('action')}" for c, _ in EVENTS])
def test_four_concurrency_groups_and_the_events_each_holds(ctx, group):
    assert WF['concurrency']['cancel-in-progress'] is False
    assert group_of(**ctx) == group
    # the jobs the event starts belong to its group, in the product and in the public scratch repository
    for repository in (PRODUCT, SCRATCH):
        jobs = selected(**ctx, repository=repository)
        assert jobs <= MEMBERS[group], (ctx, repository, jobs)


def test_the_scheduled_events_are_seeds_only_and_name_no_job_of_the_chain():
    crons = [c['cron'] for c in ON['schedule']]
    assert crons == ['20 * * * *', '40 13 * * *'] == ACQUIRE_CRONS + RUN_CRONS
    assert 'reports/cp18d/schedule-probe.json' in TEXT.split('\non:\n')[1].split('\n  workflow_dispatch:')[0]
    for cron in crons:
        assert selected(event='schedule', schedule=cron, var='enabled') == (
            {'seed', 'keep-alive'} if cron == '40 13 * * *' else {'seed'})
    for name in ('tick', 'acquire', 'run', 'alert', 'next'):
        assert 'github.event.schedule' not in str(JOBS[name]['if']), name
    assert WF['run-name'] == ("daily ${{ github.event_name == 'workflow_dispatch' && inputs.mode || "
                              "format('seed {0}', github.event.schedule) }}")


def _files(job: str) -> list[str]:
    (co,) = [s for s in steps(job) if str(s.get('uses', '')).startswith('actions/checkout@')]
    assert re.search(r'@[0-9a-f]{40}$', co['uses']) and co['with']['persist-credentials'] is False
    assert co['with']['sparse-checkout-cone-mode'] is False
    return co['with']['sparse-checkout'].split()


def test_the_chains_jobs_their_runners_their_permissions_and_their_limits():
    seed, tick, alert, nxt, rehearsal = (JOBS[n] for n in ('seed', 'tick', 'alert', 'next', 'chain-dry-run'))
    for job in (seed, tick, alert, nxt, rehearsal):
        assert job['runs-on'].startswith('ubuntu'), job['name']
    assert seed['permissions'] == {'contents': 'read', 'actions': 'write'} and seed['timeout-minutes'] <= 10
    assert tick['permissions'] == {'contents': 'read'} and tick['timeout-minutes'] == 355
    assert alert['permissions'] == {'contents': 'read', 'issues': 'write'} and alert['timeout-minutes'] <= 10
    assert nxt['permissions'] == {'contents': 'read', 'actions': 'write'} and nxt['timeout-minutes'] <= 20
    assert rehearsal['permissions'] == {'contents': 'read', 'actions': 'write'}
    # write permissions only where they are needed
    writes = {n: {k for k, v in j['permissions'].items() if v == 'write'} for n, j in JOBS.items()}
    assert {n for n, w in writes.items() if 'actions' in w} == {'seed', 'next', 'chain-dry-run', 'keep-alive'}
    assert {n for n, w in writes.items() if 'issues' in w} == {'alert'}
    assert {n for n, w in writes.items() if 'contents' in w} == {'acquire', 'run'}
    # each reads only its files; the tick and the alert read main as it is now (after this link's records)
    assert _files('seed') == _files('next') == _files('chain-dry-run') == [
        'src/cp18/chain.py', 'src/cp18/window.py', 'src/cp18/alert.py']
    assert _files('tick') == ['src/cp18/chain.py', 'src/cp18/window.py', 'live/store/runs']
    assert _files('alert') == ['src/cp18/alert.py', 'src/cp18/chain.py', 'src/cp18/window.py',
                               'live/store/ledger.jsonl', 'live/store/issued']
    for name in ('tick', 'alert'):
        (co,) = [s for s in steps(name) if str(s.get('uses', '')).startswith('actions/checkout@')]
        assert co['with']['ref'] == 'main'
    # the chain's order: the tick, then the acquisition or the run, then the alert, then the next link
    assert JOBS['acquire']['needs'] == 'tick' and JOBS['acquire']['if'] == "needs.tick.outputs.action == 'acquire'"
    assert JOBS['run']['needs'] == 'tick' and JOBS['run']['if'] == "needs.tick.outputs.action == 'run'"
    assert alert['needs'] == ['tick', 'acquire', 'run'] and nxt['needs'] == ['tick', 'acquire', 'run', 'alert']
    assert str(alert['if']).startswith('always()') and str(nxt['if']).startswith('always()')
    assert "vars.DAILY_SCHEDULE == 'enabled'" in str(nxt['if'])          # the schedule's variable stops the chain
    assert JOBS['acquire']['outputs'] == {'shown': '${{ steps.outcome.outputs.shown }}',
                                          'stopped': '${{ steps.outcome.outputs.stopped }}'}


def test_the_tick_the_alert_and_the_next_link_run_the_chain_and_alert_commands():
    _, tick = step('tick', 'chain.py tick')
    assert one_line(tick['run']).endswith('python3 src/cp18/chain.py tick --store live/store --last "$LAST" '
                                          '"${force[@]}" --sleep >> "$GITHUB_OUTPUT"')
    assert 'live) force=(--force run)' in tick['run'] and 'acquire-live) force=(--force acquire)' in tick['run']
    assert tick['env'] == {'LAST': '${{ inputs.last }}', 'MODE': '${{ inputs.mode }}'}
    _, alert = step('alert', 'alert.py')
    assert 'python3 src/cp18/alert.py --repo "$GITHUB_REPOSITORY" --store live/store --run-url "$RUN_URL"' in \
        one_line(alert['run'])
    assert alert['env']['GH_TOKEN'] == '${{ github.token }}' and 'secrets.' not in json.dumps(alert)
    _, nxt = step('next', 'chain.py next')
    assert 'sleep 600' in nxt['run'] and nxt['env']['GH_TOKEN'] == '${{ github.token }}'
    _, seed = step('seed', 'chain.py seed')
    assert one_line(seed['run']) == 'python3 src/cp18/chain.py seed --repo "$GITHUB_REPOSITORY"'
    for name in ('seed', 'tick', 'alert', 'next', 'chain-dry-run'):
        assert 'secrets.' not in json.dumps(JOBS[name]), name


def test_a_link_by_hand_acts_at_once_and_the_disabled_schedule_stops_the_chain():
    assert selected(event='workflow_dispatch', mode='live', action='run', var='enabled') == {'tick', 'run', 'alert', 'next'}
    assert selected(event='workflow_dispatch', mode='live', action='run', var='') == {'tick', 'run', 'alert'}
    assert selected(event='workflow_dispatch', mode='chain', action='acquire', var='') == set()
    assert selected(event='workflow_dispatch', mode='chain', action='none', var='enabled') == {'tick', 'alert', 'next'}


def _stop_after(job: str) -> int:
    first = steps(job)[0]
    run = first['run']
    assert 'uses' not in first and '"$GITHUB_ENV"' in run
    assert 'echo "STOP_BY=$(date -u -r "$start" -v+"${STOP_AFTER_MINUTES}"M +%Y-%m-%dT%H:%M:%SZ)" >> "$GITHUB_ENV"' in run
    assert 'echo "JOB_START=$(date -u -r "$start" +%Y-%m-%dT%H:%M:%SZ)" >> "$GITHUB_ENV"' in run
    return int(first['env']['STOP_AFTER_MINUTES'])


def test_each_acquisition_and_its_stop_by_stay_inside_six_hours_with_the_timeout():
    stop = _stop_after('acquire')
    timeout = JOBS['acquire']['timeout-minutes']
    assert stop == 340 and timeout == 355
    assert stop + 10 <= timeout <= 360            # publication, scan and upload after the stop-by, within GitHub's limit
    _, acq = step('acquire', '-m cp18 acquire')
    assert one_line(acq['run']) == ('.venv/bin/python -m cp18 acquire --root . --out "$RESULTS/acquire.json" '
                                    '--remote origin --window-hours 6 --stop-by "$STOP_BY" ${DAY:+--day "$DAY"}')
    # the rehearsal's own stop-by stays inside its own limit
    assert _stop_after('acquire-dry-run') + 10 <= JOBS['acquire-dry-run']['timeout-minutes'] <= 60


def test_on_every_day_of_two_years_any_event_in_the_gates_band_starts_the_acquisition_in_time():
    """D's cutoff (`cp25.guard.issue_time`): 10:00 UTC in winter, 09:00 UTC in summer, DST changes included. For an
    hourly event arriving at any delay, the gate (`src/cp18/window.py`) starts D's acquisition 5.5 h before the cutoff
    (at once if it arrives later, after a sleep if earlier by at most 5.75 h); the acquisition then covers the
    publication (seen first 09:03-09:17 UTC in winter: 43-57 min before the cutoff) up to the cutoff's margin, inside
    its stop-by. So every arrival in the band [cutoff - 11.25 h, cutoff - 7 min] covers the day. Both run crons follow
    the cutoff."""
    from cp18 import window as W
    stop = _stop_after('acquire')
    day = date(2027, 1, 1)
    while day < date(2029, 1, 1):
        target = day + timedelta(days=1)
        cutoff = guard.issue_time(target)
        assert W.cutoff(target) == cutoff and cutoff.astimezone(UTC).date() == day
        for minutes_before in range(8, int(11.25 * 60) + 1, 37):     # arrivals across the band
            now = cutoff - timedelta(minutes=minutes_before)
            p = W.plan(now)
            assert p['go'] and p['day'] == str(target), (day, minutes_before, p)
            begins = now + timedelta(seconds=p['sleep_seconds'])
            assert begins <= cutoff - timedelta(minutes=57) or begins == now          # before the publication, or now
            assert begins + timedelta(minutes=stop) >= cutoff - timedelta(minutes=2) or begins == now
        assert not W.plan(cutoff - timedelta(hours=11.5))['go']                       # earlier: a later event comes
        assert not W.plan(cutoff - timedelta(minutes=5))['go']                        # too close: the run handles it
        for c in RUN_CRONS:
            assert _cron_time(c, day) > cutoff, (day, c)
        day += timedelta(days=1)


def test_the_header_states_the_schedule_and_the_groups():
    for part in ('09:03 and 09:17 UTC', '6 h 11 min to 7 h 36 min', 'the job\'s start + 340 min', 'timeout-minutes 355',
                 "GitHub's 6-hour job limit", 'An acquisition that finds nothing missing commits nothing',
                 'daily-dry-run', 'daily-chain', 'daily-seed', 'cancels an older', 'O47', 'O54',
                 'touch none of the pusher\'s own files', 'refuses otherwise', '10:00 UTC in winter time',
                 '09:00 UTC in summer time', 'the first runner day had none fire', 'late by up to 12 hours',
                 'at most one chain survives', 'however late, restarts it', 'never a credential',
                 'two never write the same day'):
        assert part in ' '.join(line.lstrip('# ') for line in HEADER.splitlines()), part


# ------------------------------------------------------------------------------------------------ rehearsals
def test_the_rehearsal_modes_are_dispatch_only_and_read_only():
    inputs = ON['workflow_dispatch']['inputs']
    assert 'acquire-dry-run' in inputs['mode']['options']
    assert inputs['late_day']['default'] == '' and inputs['published_after']['default'] == '8'
    assert inputs['move_main']['options'] == ['false', 'true'] and inputs['move_main']['default'] == 'false'
    for repository in (PRODUCT, SCRATCH):                      # in any repository, like the dry run
        assert selected(event='workflow_dispatch', mode='acquire-dry-run', repository=repository) == {'acquire-dry-run'}
    for cron in ACQUIRE_CRONS + RUN_CRONS:
        for var in ('enabled', ''):
            assert not selected(event='schedule', schedule=cron, var=var) & {'dry-run', 'acquire-dry-run', 'chain-dry-run'}
    for repository in (PRODUCT, SCRATCH):
        assert selected(event='workflow_dispatch', mode='chain-dry-run', repository=repository) == {'chain-dry-run'}
    job = JOBS['acquire-dry-run']
    assert job['runs-on'] == 'macos-26' and job['permissions'] == {'contents': 'read'}
    assert job['timeout-minutes'] <= 60
    for name in ('dry-run', 'acquire-dry-run'):
        blob = json.dumps(JOBS[name])
        assert 'secrets.' not in blob and 'github.token' not in blob and 'DELU_PUSH_TOKEN' not in blob, name
    # the rehearsal flags never reach the live jobs
    for name in ('acquire', 'run', 'keep-alive'):
        for s in steps(name):
            assert not any(flag in (s.get('run') or '') for flag in LIVE_ONLY), (name, s.get('name'))


def test_the_late_day_rehearsal_adds_the_flag_to_the_dry_runs_pipeline():
    _, run = step('dry-run', '-m cp18 run ')
    assert run['env']['LATE_DAY'] == '${{ inputs.late_day }}'
    command = one_line(run['run'].split('set +e -o pipefail')[1])
    assert command.startswith('.venv/bin/python -m cp18 run ') and '${LATE_DAY:+--late-day "$LATE_DAY"}' in command
    assert '--remote dryrun' in command and '--now "$NOW"' in command


def test_the_moved_main_rehearsal_adds_the_flag_to_the_dry_runs_records():
    _, rec = step('dry-run', 'cp18.local records')
    assert rec['env'] == {'MOVE_MAIN': '${{ inputs.move_main }}'}
    assert '[ "$MOVE_MAIN" != true ] || extra+=(--rehearse-moved-main)' in rec['run']
    assert one_line(rec['run']).endswith('--out "$RESULTS/records.json" "${extra[@]}"')
    _, live = step('run', 'cp18.local records')
    assert 'MOVE_MAIN' not in json.dumps(live)


def test_the_acquisition_rehearsal_is_the_dry_runs_setup_then_the_rehearsed_acquisition():
    names = [s.get('name') or s.get('uses') for s in steps('acquire-dry-run')]
    dry = {json.dumps(s, sort_keys=True) for s in steps('dry-run')}
    i_store, store = step('acquire-dry-run', 'seed-store')
    assert json.dumps(store, sort_keys=True) in dry                         # the dry run's own store step, aliased
    assert store['run'].index('git rm -r -q --ignore-unmatch -- live') < store['run'].index('seed-store')
    i_guard, guard_step = step('acquire-dry-run', 'git config core.hooksPath .githooks')
    i_uv, _ = step('acquire-dry-run', 'pip install --no-deps')
    i_gate, gate = step('acquire-dry-run', 'python3 src/cp18/window.py --now "$NOW"')
    i_env, _ = step('acquire-dry-run', 'uv sync --locked')
    i_acq, acq = step('acquire-dry-run', '-m cp18 acquire')
    i_scan, _ = step('acquire-dry-run', 'cp18.guarddemo scan')
    i_del, _ = step('acquire-dry-run', "-name '*-arrays.npz' -delete")
    assert 0 < i_uv < i_gate < i_env < i_guard < i_store < i_acq < i_scan < i_del, names
    # the gate rehearsed as the live gate decides, its sleep real and bounded; the acquisition only when it says go,
    # its simulated clock continuing from the arrival through the real time since
    assert gate['env'] == {'DAY': '${{ inputs.day }}', 'NOW': '${{ inputs.now }}'} and gate['id'] == 'gate'
    assert '[ "$sleep_s" -le 1200 ]' in gate['run'] and 'sleep "$sleep_s"' in gate['run']
    assert acq['if'] == "steps.gate.outputs.go == 'true'" and 'GATE_EPOCH' in acq['run']
    assert acq['env'] == {'DAY': '${{ inputs.day }}', 'NOW': '${{ inputs.now }}', 'AFTER': '${{ inputs.published_after }}'}
    command = one_line(acq['run'].split('set +e -o pipefail')[1].split(' 2>&1')[0])
    assert command == ('.venv/bin/python -m cp18 acquire --root . --out "$RESULTS/acquire.json" --remote dryrun '
                       '--rehearsal reports/cp18a/dryrun/recorded --day "$DAY" --clock-start "$NOW" '
                       '--published-after-minutes "$AFTER" --poll-seconds 60 --margin-seconds 120 --window-hours 6 '
                       '--stop-by "$STOP_BY"')
    upload = steps('acquire-dry-run')[-1]
    assert upload['uses'].startswith('actions/upload-artifact@') and upload['with']['name'] == 'acquire-dry-run'


def _checks(script: str) -> str:
    """The input checks at the top of a run script: everything before the fake credentials are made."""
    return script.split('# Fake credentials')[0]


@pytest.mark.parametrize('late_day, code', [('', 0), ('2026-09-06', 0), ('2026-08-31', 0), ('2026-09-07', 2),
                                            ('2026-11-15', 2), ('next', 2)])
def test_the_late_day_is_a_development_day(late_day, code):
    _, run = step('dry-run', '-m cp18 run ')
    done = subprocess.run(['bash', '-c', _checks(run['run'])], capture_output=True, text=True,
                          env={'NOW': '2026-09-05T12:30:00+02:00', 'LATE_DAY': late_day, 'PATH': '/usr/bin:/bin'})
    assert done.returncode == code, done.stderr


@pytest.mark.parametrize('day, now, code', [('2026-09-05', '2026-09-04T06:20:00+02:00', 0),
                                            ('2026-09-06', '2026-09-05T06:20:00+02:00', 0),
                                            ('2026-09-07', '2026-09-06T06:20:00+02:00', 2),
                                            ('2026-09-05', '2026-09-07T06:20:00+02:00', 2),
                                            ('', '2026-09-04T06:20:00+02:00', 2), ('2026-09-05', '', 2),
                                            ('tomorrow', '2026-09-04T06:20:00+02:00', 2)])
def test_the_acquisition_rehearsal_runs_on_development_days_only(day, now, code):
    _, gate = step('acquire-dry-run', 'python3 src/cp18/window.py --now "$NOW"')
    done = subprocess.run(['bash', '-c', gate['run'].split('echo "GATE_EPOCH')[0]], capture_output=True, text=True,
                          env={'DAY': day, 'NOW': now, 'PATH': '/usr/bin:/bin'})
    assert done.returncode == code, done.stderr


# ------------------------------------------------------------------------------------------------ the artifact
def test_the_runs_artifact_keeps_the_whole_build_recorded_before_the_arrays_are_deleted():
    run_steps = steps('run')
    assert not any('rm -rf "$RESULTS/space' in (s.get('run') or '') for s in run_steps)
    i_space, _ = step('run', 'scripts/build_product_space.py')
    i_pub, _ = step('run', '-m cp18.publish ')
    i_rec, rec = step('run', 'cp18.runner_artifact record')
    i_scan, _ = step('run', 'cp18.local scan')
    i_del, _ = step('run', "-name '*-arrays.npz' -delete")
    assert i_space < i_pub < i_rec < i_scan < i_del
    assert rec['run'].strip().splitlines()[-1].strip() == (
        '.venv/bin/python -m cp18.runner_artifact record --build "$RESULTS/space" --out "$RESULTS/space-artifact.json"')
    assert "steps.space.outcome == 'success'" in rec['if'] and '!cancelled()' in rec['if']
    assert 'env' not in rec                                                       # no credential
    (upload,) = [s for s in run_steps if s.get('uses', '').startswith('actions/upload-artifact@')]
    assert upload['with']['include-hidden-files'] is True and upload['with']['path'] == '${{ env.RESULTS }}'
    assert 'steps.scan.outcome' in upload['if']


# ------------------------------------------------------------------------------------------------ unchanged
def test_the_live_guarantees_stand():
    for name in ('seed', 'tick', 'keep-alive'):            # the chain's other jobs follow the tick (`needs`)
        assert str(JOBS[name]['if']).startswith(f"github.repository == '{PRODUCT}'"), name
    for name in ('seed', 'keep-alive'):
        assert "vars.DAILY_SCHEDULE == 'enabled'" in str(JOBS[name]['if']), name
    for name in ('alert', 'next'):
        assert f"github.repository == '{PRODUCT}'" in str(JOBS[name]['if']), name
    assert {n for n, j in JOBS.items() if j['permissions'].get('contents') == 'write'} == {'acquire', 'run'}
    keep = JOBS['keep-alive']
    assert "github.event.schedule == '40 13 * * *'" in str(keep['if']) and keep['permissions'] == {'actions': 'write'}
    assert selected(event='schedule', schedule='40 13 * * *', var='enabled') == {'seed', 'keep-alive'}
    assert 'every live run, acquisition included, pushes a data-only commit to main' in HEADER and '60 days' in HEADER
    _, store = step('dry-run', 'seed-store')
    assert 'git rm -r -q --ignore-unmatch -- live' in store['run'] and 'rm -rf live' in store['run']


def test_the_gates_cutoff_and_next_day_are_the_pipelines_on_every_hour_of_two_years():
    from cp18 import acquire, window as W
    t = datetime(2027, 1, 1, 0, 20, tzinfo=UTC)
    while t < datetime(2029, 1, 1, tzinfo=UTC):
        assert W.next_day(t) == acquire.next_day(t), t
        assert W.cutoff(W.next_day(t)) == guard.issue_time(W.next_day(t)), t
        t += timedelta(hours=1)


def test_the_gate_runs_without_the_projects_environment():
    import subprocess
    import sys
    root = Path(__file__).resolve().parents[2]
    done = subprocess.run([sys.executable, '-I', str(root / 'src/cp18/window.py'), '--now', '2026-11-16T23:20:00Z'],
                          capture_output=True, text=True, cwd='/', env={})
    assert done.returncode == 0, done.stderr
    out = dict(line.split('=', 1) for line in done.stdout.strip().splitlines())
    assert out == {'go': 'true', 'sleep_seconds': str(5 * 3600 + 10 * 60), 'day': '2026-11-18',
                   'cutoff_utc': '2026-11-17T10:00:00Z', 'start_utc': '2026-11-17T04:30:00Z',
                   'reason': "sleep until 2026-11-18's acquisition starts (2026-11-17T04:30:00Z)"}
