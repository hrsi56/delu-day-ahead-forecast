"""CP-18c item 8: the local fallback (`cp18.local`) and its two launchd agents, written and tested, never installed.

The agents: well-formed (strictly parsed; `plutil -lint` on darwin), no credential, the project named for both
`CP17_PROJECT_ROOT` and `CP26_PROJECT_ROOT`, their exact commands accepted by `cp18.local`'s own parser, and their
Asia/Jerusalem times before (the acquisition) and after (the run) the Berlin cutoff on every day of two years, under
both DST rules. The fallback's helpers: the per-stage environment, the bundle's plan, the records through the claim, the
by-value scan and the ecCodes environment record. Every test that commits sets its own git identity; fake values only.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
import os
from pathlib import Path
import plistlib
import re
import secrets
import shutil
import subprocess
import sys

import pytest

from cp18 import local
from cp18.records import RecordLog

from cp18c.support18c import IDENTITY, at_noon, git, make_origin, run, synthetic_state

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / 'reports/cp18c/launchd'
PROJECT = '/Users/djourno/Downloads/PJM'
CLONE = f'{PROJECT}/.local/live/clone'
ACQUIRE, RUN = AGENTS / 'com.delu.daily-acquire.plist', AGENTS / 'com.delu.daily-run.plist'
BLAS = ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS')
UTC = timezone.utc


def agent(path: Path) -> dict:
    return plistlib.loads(path.read_bytes())           # expat: strict XML (no "--" inside a comment)


# ------------------------------------------------------------------------------------------------ the agents
@pytest.mark.parametrize('path, label, command', [(ACQUIRE, 'com.delu.daily-acquire', 'acquire'),
                                                  (RUN, 'com.delu.daily-run', 'run')])
def test_each_agent_is_well_formed_names_the_project_and_holds_no_credential(path, label, command):
    value = agent(path)
    assert value['Label'] == label and value['RunAtLoad'] is False and value['ProcessType'] == 'Standard'
    args = value['ProgramArguments']
    assert args[:4] == [f'{PROJECT}/.venv/bin/python', '-m', 'cp18.local', command]
    env = value['EnvironmentVariables']
    assert not [k for k in env if local.CREDENTIAL_NAME.search(k)]
    assert env['CP17_PROJECT_ROOT'] == env['CP26_PROJECT_ROOT'] == PROJECT
    assert env['PYTHONPATH'] == f'{CLONE}/src' and value['WorkingDirectory'] == CLONE
    assert all(env[n] == '1' for n in BLAS) and env['MLFLOW_DISABLE_TELEMETRY'] == 'true' and env['DO_NOT_TRACK'] == '1'
    assert env['PATH'].split(':')[0] == f'{PROJECT}/.venv/bin'
    assert value['StandardOutPath'].startswith(f'{PROJECT}/.local/live/logs/')
    text = path.read_text()
    assert 'NOT INSTALLED' in text and 'launchctl bootstrap' in text           # written, with its install step


def test_the_agents_exact_commands_are_accepted_by_the_fallback():
    acquire = local.parser().parse_args(agent(ACQUIRE)['ProgramArguments'][3:])
    assert acquire.cmd == 'acquire' and acquire.window_hours == 3.0 and str(acquire.clone) == CLONE
    assert str(acquire.project) == PROJECT and acquire.out_root is not None and acquire.out is None
    ran = local.parser().parse_args(agent(RUN)['ProgramArguments'][3:])
    assert ran.cmd == 'run' and ran.mode == 'live' and ran.inputs == 'live-http' and ran.publish == 'hub'
    assert ran.now is None and ran.out_root is not None and ran.url == local.PRODUCT_URL
    for command in ('acquire', 'run'):                          # the module the agents run, by its own entry point
        done = subprocess.run([sys.executable, '-m', 'cp18.local', command, '--help'], capture_output=True, text=True,
                              env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')})
        assert done.returncode == 0, done.stderr


@pytest.mark.skipif(sys.platform != 'darwin', reason='plutil and the Owner\'s paths exist on macOS only')
def test_plutil_lints_both_agents_and_their_interpreter_exists_on_the_owners_mac():
    for path in (ACQUIRE, RUN):
        done = subprocess.run(['plutil', '-lint', str(path)], capture_output=True, text=True)
        assert done.returncode == 0 and done.stdout.strip().endswith('OK'), done.stdout
    python = Path(agent(RUN)['ProgramArguments'][0])
    if not python.exists():
        pytest.skip(f'{python} is not on this Mac (not the Owner\'s)')
    assert os.access(python, os.X_OK)


def _times(path: Path) -> list[tuple[int, int]]:
    value = agent(path)['StartCalendarInterval']
    return [(v['Hour'], v['Minute']) for v in (value if isinstance(value, list) else [value])]


def test_the_times_map_before_and_after_the_berlin_cutoff_under_both_dst_rules():
    """The Mac's clock is in Asia/Jerusalem; the cutoff is D-1 11:00 Europe/Berlin. On every day of two years (both DST
    changes, and the two late-March days when Jerusalem is two hours ahead) every acquisition starts between 15 minutes
    and 3 hours before the cutoff (`--window-hours 3`), the first at least 45 minutes before it, and the run starts at
    least 1 hour after it."""
    from zoneinfo import ZoneInfo
    from cp25 import guard
    jerusalem = ZoneInfo('Asia/Jerusalem')
    assert _times(ACQUIRE) == [(11, 10), (11, 40)] and _times(RUN) == [(15, 0)]
    offsets, day = set(), date(2027, 1, 1)
    while day < date(2029, 1, 1):
        cutoff = guard.issue_time(day + timedelta(days=1))
        for i, (hour, minute) in enumerate(_times(ACQUIRE)):
            start = datetime(day.year, day.month, day.day, hour, minute, tzinfo=jerusalem)
            ahead = (cutoff - start) / timedelta(minutes=1)
            assert (45 if i == 0 else 15) <= ahead <= 180, (day, hour, minute, ahead)
        for hour, minute in _times(RUN):
            start = datetime(day.year, day.month, day.day, hour, minute, tzinfo=jerusalem)
            assert (start - cutoff) >= timedelta(hours=1), (day, start)
        offsets.add(start.utcoffset() - start.astimezone(guard.BERLIN).utcoffset())
        day += timedelta(days=1)
    assert offsets == {timedelta(hours=1), timedelta(hours=2)}           # both rules met, the March gap included


def test_cp18as_dry_run_agent_is_superseded_not_edited():
    old = ROOT / 'reports/cp18a/launchd/com.delu.daily-fallback.plist'
    assert old.is_file() and 'REPLACED-AT-ACTIVATION' in old.read_text()
    assert 'com.delu.daily-fallback.plist' in RUN.read_text()


# ------------------------------------------------------------------------------------------------ the helpers
def test_each_stage_gets_only_the_credential_it_uses(monkeypatch):
    fakes = {n: secrets.token_hex(20) for n in local.CREDENTIALS + ('OTHER_API_KEY',)}
    for name, value in fakes.items():
        monkeypatch.setenv(name, value)
    run_env = local.stage_env('ENTSOE_API_TOKEN')
    assert 'ENTSOE_API_TOKEN' in run_env and not ({'HF_TOKEN', 'DAGSHUB_USER_TOKEN', 'OTHER_API_KEY'} & set(run_env))
    publish_env = local.stage_env('HF_TOKEN')
    assert set(publish_env) & set(fakes) == {'HF_TOKEN'}
    assert not set(local.stage_env()) & set(fakes)
    assert run_env['PYTHONPATH'] == str(ROOT / 'src')
    probe = ("import os, sys; sys.exit(0 if os.environ.get('ENTSOE_API_TOKEN') and not os.environ.get('HF_TOKEN') "
             "else 3)")
    assert local.stage('probe', ['-c', probe], keep=('ENTSOE_API_TOKEN',))['exit'] == 0
    assert local.stage('probe', ['-c', probe])['exit'] == 3


def test_the_project_is_named_for_both_the_pins_check_and_the_eccodes_environment(monkeypatch, tmp_path):
    monkeypatch.setenv('CP17_PROJECT_ROOT', '/elsewhere')
    monkeypatch.delenv('CP26_PROJECT_ROOT', raising=False)
    assert local.pin_project(tmp_path) == {'CP17_PROJECT_ROOT': str(tmp_path), 'CP26_PROJECT_ROOT': str(tmp_path)}
    assert os.environ.get('CP17_PROJECT_ROOT') == os.environ.get('CP26_PROJECT_ROOT') == str(tmp_path)


def test_a_live_run_refuses_a_simulated_clock_and_a_dry_run_never_publishes_to_the_space(tmp_path):
    base = ['run', '--clone', str(tmp_path / 'c'), '--project', str(tmp_path), '--out', str(tmp_path / 'o')]
    with pytest.raises(SystemExit, match='real clock'):
        local.main(base + ['--mode', 'live', '--now', '2026-11-05T12:00:00+01:00'])
    with pytest.raises(SystemExit, match='never publishes'):
        local.main(base + ['--now', '2026-08-30T12:00:00+02:00', '--inputs', 'live:x', '--publish', 'hub'])
    with pytest.raises(SystemExit, match='needs --now'):
        local.main(base)
    assert not (tmp_path / 'c').exists()                       # refused before anything is cloned


def test_each_agent_run_gets_a_new_results_folder(tmp_path):
    args = local.parser().parse_args(['run', '--clone', 'c', '--project', 'p', '--out-root', str(tmp_path)])
    first = local.results_folder(args, 'local-1')
    assert first == tmp_path.resolve() / 'local-1' and first.is_dir()
    with pytest.raises(FileExistsError):
        local.results_folder(args, 'local-1')


def _issued_store(tmp_path):
    origin = date(2026, 9, 3)                  # development days: the stand-in run stays inside the development guard
    checkout = make_origin(tmp_path, synthetic_state(origin), origin, origin + timedelta(days=1))
    repo = checkout('runner')
    record = run(repo, tmp_path, at_noon(origin), label='r1')
    assert record['days'][str(origin + timedelta(days=1))]['status'] == 'issued'
    return repo, origin + timedelta(days=1), checkout


def test_the_bundle_plan_takes_this_runs_arrays_else_a_refit_and_builds_once_per_as_of_day(tmp_path):
    repo, day, _ = _issued_store(tmp_path)
    now = at_noon(day - timedelta(days=1)) + timedelta(hours=2)
    runs = tmp_path / 'results/runs'
    plan = local.bundle_plan(repo, runs, now)
    assert plan['build'] and plan['served_day'] == str(day) and plan['how'] == 'refit' and not plan['already']
    (runs / f'A1-{day}-abc').mkdir(parents=True)
    (runs / f'A1-{day}-abc/run-arrays.npz').write_bytes(b'stand-in')
    plan = local.bundle_plan(repo, runs, now)
    assert plan['how'] == 'arrays' and plan['arrays'] == str(runs / f'A1-{day}-abc/run-arrays.npz')
    RecordLog(repo / 'live/bundles').append('bundle', f"{plan['as_of']}/bundle.json", {'stand-in': True})
    plan = local.bundle_plan(repo, runs, now)
    assert plan['already'] and not plan['build'] and 'once per day' in plan['reason']
    lines = subprocess.run([sys.executable, '-m', 'cp18.local', 'bundle-plan', '--root', str(repo), '--runs', str(runs),
                            '--now', now.isoformat()], capture_output=True, text=True,
                           env={**os.environ, 'PYTHONPATH': str(ROOT / 'src')}).stdout.splitlines()
    assert 'build=false' in lines and 'already=true' in lines and f"as_of={plan['as_of']}" in lines


def test_the_bundle_plan_builds_nothing_without_an_issued_day(tmp_path):
    origin = date(2026, 9, 3)
    repo = make_origin(tmp_path, synthetic_state(origin), origin, origin + timedelta(days=1))('runner')
    plan = local.bundle_plan(repo, tmp_path / 'runs', at_noon(origin))
    assert not plan['build'] and plan['reason'].startswith('no bundle:')


def test_the_records_go_through_the_claim_and_a_lost_race_leaves_the_other_hosts(tmp_path):
    repo, day, checkout = _issued_store(tmp_path)
    RecordLog(repo / 'live/bundles').append('bundle', 'x/bundle.json', {'stand-in': True})
    value = local.records(repo, run_id='r1')
    assert value['exit'] == 0 and value['outcome'].startswith('pushed ')
    assert git(tmp_path / 'origin.git', 'log', '-1', '--format=%s', 'main') == \
        'live: the records of run r1 (outcomes, evaluation, bundle, publication)'
    assert git(tmp_path / 'origin.git', 'show', '--stat', '--format=', 'main').split('\n')[0].strip().startswith('live/')
    assert local.records(repo, run_id='r1')['outcome'] == 'nothing to commit'
    other = checkout('other')                                   # another host pushes first
    RecordLog(other / 'live/bundles').append('bundle', 'y/bundle.json', {'theirs': True})
    assert local.records(other, run_id='theirs')['outcome'].startswith('pushed ')
    RecordLog(repo / 'live/bundles').append('bundle', 'z/bundle.json', {'mine': True})
    lost = local.records(repo, run_id='mine')
    assert lost['exit'] == 0 and lost['outcome'].startswith("main moved first")
    assert git(tmp_path / 'origin.git', 'log', '-1', '--format=%s', 'main').endswith('run theirs (outcomes, evaluation, '
                                                                                      'bundle, publication)')


def test_the_records_refuse_without_the_repositorys_hooks(tmp_path):
    repo, _, _ = _issued_store(tmp_path)
    git(repo, 'config', '--unset', 'core.hooksPath')
    RecordLog(repo / 'live/bundles').append('bundle', 'x/bundle.json', {'stand-in': True})
    value = local.records(repo, run_id='r1')
    assert value['exit'] == 2 and 'hooksPath' in value['outcome']


def test_the_scan_finds_a_value_raw_url_or_base64_encoded_and_names_only(monkeypatch, tmp_path, capsys):
    import base64
    import urllib.parse
    value = secrets.token_urlsafe(30) + '/+='
    monkeypatch.setenv('HF_TOKEN', value)
    monkeypatch.setenv('ENTSOE_API_TOKEN', 'short')                 # under 12 characters: not a credential
    monkeypatch.delenv('DELU_PUSH_TOKEN', raising=False)
    (tmp_path / 'clean.json').write_text('{"day": "2026-11-05"}\n')
    assert local.scan(['HF_TOKEN', 'ENTSOE_API_TOKEN', 'DELU_PUSH_TOKEN'], [tmp_path])['clean']
    for i, form in enumerate((value, urllib.parse.quote(value, safe=''), base64.b64encode(value.encode()).decode())):
        (tmp_path / f'leak-{i}.log').write_text(f'x {form} y\n')
    result = local.scan(['HF_TOKEN', 'ENTSOE_API_TOKEN', 'DELU_PUSH_TOKEN'], [tmp_path])
    assert not result['clean'] and sorted(Path(p).name for p in result['found']['HF_TOKEN']) == \
        ['leak-0.log', 'leak-1.log', 'leak-2.log']
    assert result['names_set'] == ['HF_TOKEN'] and result['names_unset'] == ['DELU_PUSH_TOKEN', 'ENTSOE_API_TOKEN']
    code = local.main(['scan', '--name', 'HF_TOKEN', '--out', str(tmp_path / 'out/scan.json'), str(tmp_path)])
    printed = capsys.readouterr().out + (tmp_path / 'out/scan.json').read_text()
    assert code == 1 and value not in printed and 'HF_TOKEN' in printed


def test_the_eccodes_environment_record_compares_the_installed_versions_with_the_pins(tmp_path):
    import importlib.metadata as md
    yaml_version = md.version('PyYAML')
    (tmp_path / 'freeze.txt').write_text(f'pyyaml=={yaml_version}\nnumpy==0.0.1\nnot-a-package==1.0\n')
    value = local.wx_environment(Path(sys.executable), tmp_path / 'freeze.txt')
    assert value['present'] and value['python'] == '.'.join(map(str, sys.version_info[:3]))
    assert value['missing'] == ['not-a-package'] and set(value['different']) == {'numpy'}
    assert value['distributions']['pyyaml']['version'] == yaml_version
    assert len(value['distributions']['pyyaml']['content_sha256']) == 64
    assert 'not-a-package: pinned, not installed' in value['problems']
    absent = local.wx_environment(tmp_path / 'no/python')
    assert absent['present'] is False and absent['problems']


def test_the_pins_are_read_from_cp20s_freeze_file():
    pins = local.pins(ROOT / local.WX_FREEZE)
    assert pins['eccodes'] == '2.48.0' and pins['eccodeslib'] == '2.49.0.30' and pins['eckitlib'] == '2.3.0.30'
    assert pins['numpy'] == '2.5.3' and len(pins) == 41


@pytest.mark.skipif(shutil.which('git') is None, reason='git is required')
def test_a_test_commit_sets_its_own_identity():
    """The runner has no global git identity (CP-18a's landing): the helpers and the claim set their own."""
    assert set(IDENTITY) == {'GIT_AUTHOR_NAME', 'GIT_AUTHOR_EMAIL', 'GIT_COMMITTER_NAME', 'GIT_COMMITTER_EMAIL'}
    from cp18.claim import IDENTITY as CLAIM
    assert set(CLAIM) == set(IDENTITY)
    assert re.search(r'GIT_COMMITTER_EMAIL', (ROOT / 'src/cp18/claim.py').read_text())
