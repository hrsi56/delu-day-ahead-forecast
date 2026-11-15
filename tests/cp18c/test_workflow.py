"""CP-18c item 8: `daily.yml`, live-ready. Parsed with PyYAML; the jobs' conditions evaluated for every event.

What is checked: the schedule (acquisitions before the cutoff and runs after it, on every day of two years, both DST
rules), the job each event selects, the secrets only on the steps that use them, `contents: write` only on the jobs
that push, `timeout-minutes` on every job, actions pinned by commit SHA, the bundle step before the deletion of
`*-arrays.npz`, the live commands, the ecCodes environment, the dry run's set-aside of the live record, and the
statement on GitHub's 60-day rule with its keep-alive. History-free; no platform requirement.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import json
from pathlib import Path
import re

import pytest
import yaml

from cp25 import guard

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / '.github/workflows/daily.yml'
TEXT = WORKFLOW.read_text()
WF = yaml.safe_load(TEXT)
ON = WF.get('on', WF.get(True))
JOBS = WF['jobs']
# CP-18d (item 2): was ['40 7 * * *', '20 8 * * *', '20 9 * * *'], now one event every hour, through the gate job
ACQUIRE_CRONS = ['20 * * * *']
RUN_CRONS = ['40 10 * * *', '40 13 * * *']
PRODUCT = 'hrsi56/delu-day-ahead-forecast'
UTC = timezone.utc


def steps(job: str) -> list[dict]:
    return JOBS[job]['steps']


def step(job: str, needle: str) -> tuple[int, dict]:
    """The one step of `job` whose run script holds `needle`."""
    found = [(i, s) for i, s in enumerate(steps(job)) if needle in (s.get('run') or '')]
    assert len(found) == 1, (job, needle, [s.get('name') for _, s in found])
    return found[0]


# ------------------------------------------------------------------------------------------------ conditions
def evaluate(expression: str, ctx: dict) -> bool:
    """GitHub's expression syntax as this workflow uses it, translated to Python and evaluated on `ctx`."""
    e = expression.strip()
    if e.startswith('${{'):
        e = e[3:-2]
    names = {'github.event_name': ctx['event'], 'github.event.schedule': ctx.get('schedule', ''),
             'github.repository': ctx['repository'], 'vars.DAILY_SCHEDULE': ctx.get('var', ''),
             'inputs.mode': ctx.get('mode', ''),
             # CP-18d (item 2): the acquisition follows the gate job; its condition is the gate's answer
             'needs.gate.outputs.go': ctx.get('go', 'true')}
    for name, value in sorted(names.items(), key=lambda kv: -len(kv[0])):
        e = e.replace(name, repr(value))
    e = re.sub(r"fromJSON\('(.*?)'\)", lambda m: repr(json.loads(m.group(1))), e)
    e = re.sub(r"contains\((\[.*?\]),\s*('.*?')\)", r'(\2 in \1)', e)
    e = e.replace('&&', ' and ').replace('||', ' or ')
    assert re.fullmatch(r"[\s\w'\"\[\]\(\),*=!./:-]*", e), e
    return bool(eval(e, {}))


def selected(**ctx) -> set[str]:
    ctx.setdefault('repository', PRODUCT)
    chosen = {name for name, job in JOBS.items() if evaluate(str(job['if']), ctx)}
    # CP-18d (item 2): a job that `needs` another runs only if that one runs (GitHub skips it otherwise)
    return {name for name in chosen if all(n in chosen for n in ([JOBS[name]['needs']] if isinstance(
        JOBS[name].get('needs'), str) else JOBS[name].get('needs', [])))}


def test_the_triggers_are_the_schedule_and_the_dispatch():
    assert set(ON) == {'schedule', 'workflow_dispatch'}
    assert [c['cron'] for c in ON['schedule']] == ACQUIRE_CRONS + RUN_CRONS
    mode = ON['workflow_dispatch']['inputs']['mode']
    # CP-18d (item 5): was ['dry-run', 'live', 'acquire-live'], now the acquisition rehearsal's mode added
    assert mode['type'] == 'choice' and mode['options'] == ['dry-run', 'live', 'acquire-live', 'acquire-dry-run']
    assert mode['default'] == 'dry-run'
    assert not any(i.get('required') for i in ON['workflow_dispatch']['inputs'].values())


@pytest.mark.parametrize('cron', ACQUIRE_CRONS)
def test_an_acquisition_cron_starts_the_acquisition_only(cron):
    # CP-18d (item 2): was {'acquire'}, now the gate and, when it says go, the acquisition after it
    assert selected(event='schedule', schedule=cron, var='enabled') == {'gate', 'acquire'}
    assert selected(event='schedule', schedule=cron, var='enabled', go='false') == {'gate'}


@pytest.mark.parametrize('cron', RUN_CRONS)
def test_a_run_cron_starts_the_run_and_the_retry_the_keep_alive(cron):
    assert selected(event='schedule', schedule=cron, var='enabled') == (
        {'run', 'keep-alive'} if cron == '40 13 * * *' else {'run'})


# CP-18d (item 2): acquire-live was {'acquire'}, now {'gate', 'acquire'} (a dispatch passes the gate at once)
@pytest.mark.parametrize('mode, jobs', [('dry-run', {'dry-run'}), ('live', {'run'}), ('acquire-live', {'gate', 'acquire'})])
def test_a_dispatch_starts_the_job_of_its_mode(mode, jobs):
    assert selected(event='workflow_dispatch', mode=mode) == jobs


def test_the_schedule_does_nothing_until_enabled_and_never_outside_the_product():
    for cron in ACQUIRE_CRONS + RUN_CRONS:
        assert selected(event='schedule', schedule=cron, var='') == set()
        assert selected(event='schedule', schedule=cron, var='enabled', repository='hrsi56/delu-pipeline-dryrun') == set()
    # the public scratch repository runs the dry run only, whatever is dispatched
    for mode in ('live', 'acquire-live'):
        assert selected(event='workflow_dispatch', mode=mode, repository='hrsi56/delu-pipeline-dryrun') == set()
    assert selected(event='workflow_dispatch', mode='dry-run', repository='hrsi56/delu-pipeline-dryrun') == {'dry-run'}


def _cron_time(cron: str, day: date) -> datetime:
    minute, hour = (int(x) for x in cron.split()[:2])
    return datetime(day.year, day.month, day.day, hour, minute, tzinfo=UTC)


def test_on_every_day_of_two_years_two_acquisitions_precede_the_cutoff_and_the_runs_follow_it():
    """D's cutoff is D-1 11:00 Berlin (`cp25.guard.issue_time`): 10:00 UTC in winter, 09:00 UTC in summer. On every day
    (the DST changes included) at least two acquisition events can start D's acquisition before it, and both run crons
    fall after it.

    CP-18d (item 2): was "at least two of the three daily crons fall 30-180 min before the cutoff"; now the event is
    hourly and passes the gate (`src/cp18/window.py`), so the assertion is that at least two hourly events in the 3 h
    before the cutoff (at least 30 min ahead) are started by the gate, and that a run cron follows the cutoff."""
    from cp18 import window as W
    day = date(2027, 1, 1)
    while day < date(2029, 1, 1):
        cutoff = guard.issue_time(day + timedelta(days=1))          # the cutoff that falls on `day`
        assert cutoff.astimezone(UTC).date() == day
        hourly = [datetime(day.year, day.month, day.day, h, 20, tzinfo=UTC) for h in range(24)]
        ahead = [(cutoff - t) / timedelta(minutes=1) for t in hourly]
        started = [t for t, m in zip(hourly, ahead) if 30 <= m <= 180 and W.plan(t)['go']]
        assert len(started) >= 2, (day, ahead)
        for c in RUN_CRONS:
            assert _cron_time(c, day) > cutoff, (day, c)
        day += timedelta(days=1)


def test_the_concurrency_group_keeps_live_runs_apart_and_never_cancels_one():
    group = WF['concurrency']['group']
    assert WF['concurrency']['cancel-in-progress'] is False
    assert "'dry-run'" in group and "'live'" in group and 'inputs.mode' in group


# ------------------------------------------------------------------------------------------------ permissions
def test_permissions_contents_write_only_on_the_jobs_that_push():
    assert WF['permissions'] == {}
    assert JOBS['acquire']['permissions'] == {'contents': 'write'}
    assert JOBS['run']['permissions'] == {'contents': 'write'}
    assert JOBS['dry-run']['permissions'] == {'contents': 'read'}
    assert JOBS['keep-alive']['permissions'] == {'actions': 'write'}
    for name, job in JOBS.items():
        pushes = any('DELU_PUSH_TOKEN' in (s.get('env') or {}) and 'scan' not in (s.get('run') or '')
                     for s in job['steps'])
        assert pushes == (job['permissions'].get('contents') == 'write'), name


def test_the_pipeline_jobs_run_on_the_issuing_hosts_runner():
    # carried from CP-18a's dispatch-only test (superseded by brief item 8, the Orchestrator's O36): runs-on macos-26
    for name in ('dry-run', 'acquire', 'run'):
        assert JOBS[name]['runs-on'] == 'macos-26', name


def test_every_job_has_a_time_limit():
    for name, job in JOBS.items():
        assert 'timeout-minutes' in job, name
    # CP-18d (item 2): was acquire <= 180, now <= 360 (the in-job wait, inside GitHub's 6-hour job limit)
    assert JOBS['acquire']['timeout-minutes'] <= 360 and JOBS['run']['timeout-minutes'] <= 180
    assert JOBS['keep-alive']['timeout-minutes'] <= 10
    assert 'inputs.minutes' in str(JOBS['dry-run']['timeout-minutes'])


def test_actions_are_pinned_by_commit_and_the_checkout_keeps_no_credential():
    for name, job in JOBS.items():
        for s in job['steps']:
            if 'uses' in s:
                assert re.fullmatch(r'[\w-]+/[\w-]+@[0-9a-f]{40}', s['uses']), (name, s['uses'])
            if s.get('uses', '').startswith('actions/checkout'):
                assert s['with']['persist-credentials'] is False


# ------------------------------------------------------------------------------------------------ secrets
def _secret_steps() -> dict[str, list[tuple[str, str]]]:
    out: dict[str, list[tuple[str, str]]] = {}
    for name, job in JOBS.items():
        for s in job['steps']:
            for key, value in (s.get('env') or {}).items():
                for found in re.findall(r'secrets\.(\w+)|github\.(token)', str(value)):
                    out.setdefault(found[0] or 'github.token', []).append((name, s.get('name', '')))
                    assert key in ('ENTSOE_API_TOKEN', 'HF_TOKEN', 'DELU_PUSH_TOKEN', 'GH_TOKEN')
    return out


def test_secrets_are_read_only_inside_the_steps_that_use_them():
    assert 'env' not in JOBS['run'] and 'env' not in JOBS['acquire']
    assert not any('secrets.' in str(v) or 'github.token' in str(v) for v in WF['env'].values())
    for name, job in JOBS.items():
        assert 'secrets.' not in json.dumps({k: v for k, v in job.items() if k != 'steps'}), name
        for s in job['steps']:
            assert '${{' not in (s.get('run') or ''), (name, s.get('name'))   # never interpolated into a script
    used = _secret_steps()
    assert set(used) == {'ENTSOE_API_TOKEN', 'HF_TOKEN', 'github.token'}           # DAGSHUB_USER_TOKEN is not used
    entsoe = {(j, n.split(' (')[0]) for j, n in used['ENTSOE_API_TOKEN']}
    assert entsoe == {('acquire', 'The acquisition before the cutoff'), ('run', 'The pipeline'),
                      ('acquire', 'No credential in any result'), ('run', 'No credential in any result')}
    hf = {(j, n.split(',')[0].split(' (')[0]) for j, n in used['HF_TOKEN']}
    assert hf == {('run', 'The publication to the Hugging Face Space'), ('acquire', 'No credential in any result'),
                  ('run', 'No credential in any result')}
    token = {(j, n.split(' (')[0].split(',')[0]) for j, n in used['github.token']}
    assert token == {('acquire', 'The acquisition before the cutoff'), ('acquire', 'No credential in any result'),
                     ('run', 'The pipeline'), ('run', "The day's records"), ('run', 'No credential in any result'),
                     ('keep-alive', 'Re-enable this workflow through GitHub\'s own API')}
    assert not any(j == 'dry-run' for uses in used.values() for j, _ in uses)        # the dry run uses no secret


def test_a_push_authenticates_only_where_a_step_holds_the_token():
    _, claim = step('run', 'credential.https://github.com.helper')
    assert 'git config core.hooksPath .githooks' in claim['run'] and '${DELU_PUSH_TOKEN:?}' in claim['run']
    assert 'env' not in claim
    _, scan = step('run', 'cp18.local scan')
    assert scan['if'] == 'always()'
    upload = [s for s in steps('run') if s.get('uses', '').startswith('actions/upload-artifact')]
    assert upload and 'steps.scan.outcome' in upload[0]['if']       # a found value uploads nothing


# ------------------------------------------------------------------------------------------------ the sequence
@pytest.mark.parametrize('job', ['dry-run', 'run'])
def test_the_bundle_runs_before_the_arrays_are_deleted_then_the_space_publication_and_records(job):
    i_run, _ = step(job, '-m cp18 run ')
    i_plan, plan = step(job, 'cp18.local bundle-plan')
    i_bundle, bundle = step(job, '-m cp18.bundle ')
    i_space, _ = step(job, 'scripts/build_product_space.py')
    i_pub, _ = step(job, '-m cp18.publish ')
    i_rec, rec = step(job, 'cp18.local records')
    i_del, _ = step(job, "-name '*-arrays.npz' -delete")
    assert i_run < i_plan < i_bundle < i_space < i_pub < i_rec < i_del
    assert '--runs "$RESULTS/run/runs"' in plan['run']
    assert 'arrays) how=(--arrays "$ARRAYS")' in bundle['run'] and 'refit) how=(--refit)' in bundle['run']
    assert '--commit-records' in bundle['run'] and '--run-id "gh-$GITHUB_RUN_ID-$GITHUB_RUN_ATTEMPT"' in bundle['run']
    assert bundle['if'] == "steps.plan.outputs.build == 'true'"
    assert steps(job)[i_space]['if'] == "steps.bundle.outputs.publishable == 'true'"
    assert steps(job)[i_pub]['if'] == "steps.space.outcome == 'success'"
    assert 'steps.run.outcome' in rec['if'] and '!cancelled()' in rec['if']


def test_the_live_run_is_the_live_mode_with_the_claim_on_origin():
    _, prep = step('run', '-m cp18 prepare')
    assert '--pinned live/pinned' in prep['run']
    _, run = step('run', '-m cp18 run ')
    for part in ('--host runner', '--mode live', '--inputs live-http', '--remote origin',
                 '--run-label "gh-$GITHUB_RUN_ID-$GITHUB_RUN_ATTEMPT"'):
        assert part in run['run']
    assert '--now' not in run['run']
    _, bundle = step('run', '-m cp18.bundle ')
    assert '--mode live' in bundle['run']
    _, space = step('run', 'scripts/build_product_space.py')
    assert '--live live' in space['run'] and '--history "$SPACE_HISTORY"' in space['run']
    _, pub = step('run', '-m cp18.publish ')
    assert '--hub "$SPACE_HUB"' in pub['run'] and '--live live' in pub['run'] and '--target' not in pub['run']
    assert WF['env']['SPACE_HUB'] == 'Yarden-Viktor/delu-day-ahead-forecast'
    _, rec = step('run', 'cp18.local records')
    assert '--remote origin' in rec['run']
    _, acq = step('acquire', '-m cp18 acquire')
    # CP-18d (item 2): was '--window-hours 3', now '--window-hours 6' (the earlier starts wait in their job)
    assert '--remote origin' in acq['run'] and '--window-hours 6' in acq['run']


def test_the_dry_run_sets_the_live_record_aside_and_never_touches_github():
    i_store, store = step('dry-run', 'seed-store')
    assert store['run'].index('git rm -r -q --ignore-unmatch -- live') < store['run'].index('rm -rf live') < \
        store['run'].index('seed-store')
    _, run = step('dry-run', '-m cp18 run ')
    assert '--remote dryrun' in run['run'] and '--now "$NOW"' in run['run']
    _, rec = step('dry-run', 'cp18.local records')
    assert '--remote dryrun' in rec['run']
    _, pub = step('dry-run', '-m cp18.publish ')
    assert '--target "$RUNNER_TEMP/served"' in pub['run'] and '--hub' not in pub['run']
    _, prep = step('dry-run', '-m cp18 prepare')
    assert '--pinned reports/cp18a/dryrun/pinned' in prep['run']
    _, decode = step('dry-run', 'cp18.local decode-check')
    assert '--archived reports/cp18a/dryrun/recorded/gfs' in decode['run']
    assert (ROOT / 'reports/cp18a/dryrun/recorded/gfs/runs/2026-09-05.npz').is_file()
    assert ON['workflow_dispatch']['inputs']['decode_run']['default'] == '2026-09-05'


@pytest.mark.parametrize('job', ['dry-run', 'acquire', 'run'])
def test_the_eccodes_environment_is_cp20s_pinned_one_where_cp18_live_gfs_finds_it(job):
    _, wx = step(job, 'cp18.local wx-env')
    assert 'wx="$CP26_PROJECT_ROOT/.local/artifacts/cp-20/wx-venv"' in wx['run']
    assert '-r "$WX_FREEZE"' in wx['run'] and '--freeze "$WX_FREEZE"' in wx['run']
    assert WF['env']['WX_FREEZE'] == 'reports/weather-admission/scripts/requirements.freeze.txt'
    assert (ROOT / WF['env']['WX_FREEZE']).is_file()
    # CP-18d (item 2): was step(job, 'GITHUB_ENV'), now its RESULTS line (the acquire job's STOP_BY step writes it too)
    _, uv = step(job, '"RESULTS=$RUNNER_TEMP/results" >> "$GITHUB_ENV"')
    assert 'echo "CP17_PROJECT_ROOT=$GITHUB_WORKSPACE"' in uv['run']
    assert 'echo "CP26_PROJECT_ROOT=$GITHUB_WORKSPACE"' in uv['run']
    pins = dict(line.split('==') for line in (ROOT / WF['env']['WX_FREEZE']).read_text().split())
    assert pins['eccodes'] == '2.48.0' and pins['eccodeslib'] == '2.49.0.30'


def test_the_keep_alive_statement_and_job():
    header = TEXT.split('\nname: daily')[0]
    assert '60 days' in header and 'every live run, acquisition included, pushes a data-only commit to main' in header
    assert 'keep-alive' in header
    job = JOBS['keep-alive']
    assert job['runs-on'].startswith('ubuntu-') and job['runs-on'] != 'ubuntu-latest'
    (only,) = job['steps']
    assert 'gh api -X PUT "repos/$GITHUB_REPOSITORY/actions/workflows/daily.yml/enable"' in only['run']
    assert only['env'] == {'GH_TOKEN': '${{ github.token }}'}


def test_every_live_run_pushes_through_the_claim():
    """The 60-day rule is met by the pushes: the acquisition publishes `live/inputs/` and the run publishes its run
    record whatever it did (`cp18.acquire`, `cp18.pipeline`); both run with the repository's guards active."""
    acquire = (ROOT / 'src/cp18/acquire.py').read_text()
    pipeline = (ROOT / 'src/cp18/pipeline.py').read_text()
    assert 'claim.publish([INPUTS_PATH]' in acquire
    assert "f'live: run {run_id} ({record[\"outcome\"]})'" in pipeline
    for job in ('acquire', 'run'):
        i_claim, _ = step(job, 'credential.https://github.com.helper')
        i_push = next(i for i, s in enumerate(steps(job)) if 'DELU_PUSH_TOKEN' in (s.get('env') or {}))
        assert i_claim < i_push
