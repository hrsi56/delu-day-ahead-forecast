"""Authorized monitors run across the former calendar boundary, retaining resource caps."""
from datetime import datetime
import importlib
import importlib.util
import json
from pathlib import Path
import signal
import subprocess
import sys
import time
from types import SimpleNamespace
from zoneinfo import ZoneInfo

import pytest

ROOT = Path(__file__).resolve().parents[2]
DRIVERS = [(24, 'cp24_ddnn2')]

@pytest.fixture(params=DRIVERS, ids=[f'cp{cp}' for cp, _ in DRIVERS])
def monitored(request, tmp_path, monkeypatch):
    cp, name = request.param
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / f'{name}.py')
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    budget_module = importlib.import_module(f'cp{cp}.budget')
    ledger = budget_module.Budget(tmp_path / 'budget.json')
    ledger.initialise({'git_bytes': 0})
    monkeypatch.setattr(driver, 'ART', tmp_path)
    monkeypatch.setattr(driver, 'ledger_path', lambda: ledger.path)
    monkeypatch.setattr(driver, 'measure_disk', lambda baseline: (0, {}))
    monkeypatch.setattr(driver, 'TICK', 0.01)
    # Keep the real child/monitor lifecycle; replace only the macOS sleep inhibitor.
    original_popen = subprocess.Popen
    inhibitors = []

    def popen(command, **kwargs):
        if command[0] == '/usr/bin/caffeinate':
            proc = original_popen([sys.executable, '-c', 'import time; time.sleep(30)'], **kwargs)
            inhibitors.append(proc)
            return proc
        return original_popen(command, **kwargs)

    monkeypatch.setattr(driver, 'subprocess', SimpleNamespace(
        Popen=popen, DEVNULL=subprocess.DEVNULL, STDOUT=subprocess.STDOUT,
        TimeoutExpired=subprocess.TimeoutExpired))
    handlers = {sig: signal.getsignal(sig) for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP)}
    args = SimpleNamespace(name='availability', workers=1, log=tmp_path / 'job.log',
                           expected_minutes=120,
                           command=[sys.executable, '-c', 'import time; time.sleep(0.08)'])
    yield driver, budget_module, ledger, args
    for sig, handler in handlers.items():
        signal.signal(sig, handler)
    for proc in inhibitors:
        proc.terminate()
        proc.wait(timeout=5)


def set_clock(monkeypatch, driver, budget_module, ledger, start, end=None):
    """Exercise admission at start and every live-monitor tick at end (if supplied)."""
    current = [start]
    proxy = SimpleNamespace(**{key: getattr(time, key) for key in dir(time) if not key.startswith('_')})
    proxy.time = lambda: current[0]
    original_sleep = time.sleep

    def sleep(seconds):
        if end is not None:
            current[0] = end
        original_sleep(seconds)

    proxy.sleep = sleep
    monkeypatch.setattr(driver, 'time', proxy)
    monkeypatch.setattr(budget_module, 'time', proxy)
    with ledger.transaction() as state:
        state['effort']['session_start_epoch'] = start


@pytest.mark.parametrize('start,end', [
    ('2026-10-08T23:50', '2026-10-09T00:01'),
    ('2026-10-09T00:00', None),
    ('2026-10-10T12:00', None),
    ('2026-10-10T19:59', '2026-10-10T20:01'),
    ('2026-10-10T23:59', '2026-10-11T00:01'),
    ('2026-10-11T12:00', None),
])
def test_monitors_admit_and_complete_at_any_time(monitored, monkeypatch, start, end):
    driver, budget_module, ledger, args = monitored
    def epoch(value):
        return datetime.fromisoformat(value).replace(tzinfo=ZoneInfo('Asia/Jerusalem')).timestamp()
    set_clock(monkeypatch, driver, budget_module, ledger, epoch(start), epoch(end) if end else None)
    assert driver.monitor(args) == 0
    marker = json.loads((driver.ART / 'markers/availability.DONE.json').read_text())
    assert marker['status'] == 'success' and marker['abort_reason'] is None
    state = ledger.read()
    assert state['counts']['machine_seconds'] > 0
    assert state['jobs'][0]['running'] is False


@pytest.mark.parametrize('cap', ['machine_seconds', 'active_seconds', 'workers'])
def test_resource_admission_limits_remain_enforced(monitored, monkeypatch, cap):
    driver, budget_module, ledger, args = monitored
    now = datetime(2026, 10, 10, 12, tzinfo=ZoneInfo('Asia/Jerusalem')).timestamp()
    set_clock(monkeypatch, driver, budget_module, ledger, now)
    with ledger.transaction() as state:
        if cap == 'machine_seconds':
            state['counts'][cap] = budget_module.CAPS[cap]
        elif cap == 'active_seconds':
            state['effort']['session_start_epoch'] = now - budget_module.CAPS[cap]
        else:
            args.workers = budget_module.CAPS[cap] + 1
    with pytest.raises(SystemExit, match='cap exhausted|hard stop|workers would exceed'):
        driver.monitor(args)
    assert ledger.read()['jobs'] == []


def test_running_job_still_stops_at_resource_cap(monitored, monkeypatch):
    driver, budget_module, ledger, args = monitored
    now = datetime(2026, 10, 10, 12, tzinfo=ZoneInfo('Asia/Jerusalem')).timestamp()
    set_clock(monkeypatch, driver, budget_module, ledger, now)
    args.command = [sys.executable, '-c', 'import time; time.sleep(5)']
    monkeypatch.setattr(driver, 'tree_rss', lambda pid: (budget_module.CAPS['rss_bytes'], 0.0))
    assert driver.monitor(args) != 0
    marker = json.loads((driver.ART / 'markers/availability.FAILED.json').read_text())
    assert marker['abort_reason'] == 'aggregate_rss_cap'
    assert ledger.read()['jobs'][0]['running'] is False
