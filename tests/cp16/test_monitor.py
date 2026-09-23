"""Regression for the observed atomic-rename monitor failure."""
import argparse
import importlib.util
from pathlib import Path
import sys
import pytest
from cp16.budget import Budget


def driver():
    path=Path(__file__).resolve().parents[2]/'scripts/cp16_v2.py'
    spec=importlib.util.spec_from_file_location('cp16_driver_test',path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def test_atomic_rename_race_is_tolerated_and_stable_files_counted():
    class Entry:
        def __init__(self,missing=False):self.missing=missing
        def is_file(self):return True
        def is_symlink(self):return False
        def stat(self):
            if self.missing:raise FileNotFoundError('atomic evidence rename')
            return argparse.Namespace(st_size=37)
    class Base:
        def exists(self):return True
        def rglob(self,pattern):return [Entry(True),Entry()]
    assert driver().checkpoint_bytes([Base()])==37


def test_monitor_failure_terminates_child_and_preserves_charge(tmp_path,monkeypatch):
    module=driver()
    def fail(paths):raise RuntimeError('injected monitor failure')
    monkeypatch.setattr(module,'checkpoint_bytes',fail)
    args=argparse.Namespace(ledger=tmp_path/'ledger.json',log=tmp_path/'child.log',
        command=[sys.executable,'-c','import time; time.sleep(10)'],project_root=tmp_path)
    with pytest.raises(RuntimeError,match='injected monitor failure'):module.monitor(args)
    record=Budget(args.ledger).read();job=record['jobs'][0]
    assert not job['running'] and job['exit_code'] is not None
    assert 'injected monitor failure' in job['supervisor_error']
    assert record['counts']['machine_seconds']>0


def test_successful_monitor_has_actual_exit_and_output(tmp_path):
    args=argparse.Namespace(ledger=tmp_path/'ledger.json',log=tmp_path/'child.log',
        command=[sys.executable,'-c','print("monitored-positive-control")'],project_root=tmp_path)
    assert driver().monitor(args)==0
    assert 'monitored-positive-control' in args.log.read_text()
    assert Budget(args.ledger).read()['jobs'][0]['exit_code']==0


def test_resumed_effort_keeps_prior_debit_but_excludes_owner_pause(tmp_path):
    import time
    args=argparse.Namespace(ledger=tmp_path/'ledger.json',log=tmp_path/'child.log',
        command=[sys.executable,'-c','print("resumed")'],project_root=tmp_path)
    b=Budget(args.ledger)
    with b.transaction() as state:
        state['created_epoch']=0
        state['effort']={'historical_upper_bound_seconds':3600,'resumed_epoch':time.time()}
    assert driver().monitor(args)==0
    assert 3600<=b.read()['active_effort_upper_bound_seconds']<3700
