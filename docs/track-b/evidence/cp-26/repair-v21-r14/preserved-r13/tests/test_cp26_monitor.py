"""A restart must never represent a dead worker's later idle gap as measured compute."""
import importlib.util
import json
from pathlib import Path

import pytest


@pytest.fixture
def driver():
    path = Path(__file__).resolve().parents[1] / 'scripts/cp26_rebaseline.py'
    spec = importlib.util.spec_from_file_location('cp26_resource_driver', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_dead_monitor_without_end_evidence_stops_without_charging_idle_time(driver, tmp_path, monkeypatch):
    monkeypatch.setattr(driver, 'art', lambda: tmp_path)
    job = {'started_epoch': 100.0, 'last_charge_epoch': 120.0, 'charged_wall_seconds': 20.0,
           'workers': 4, 'job_index': 0}
    with pytest.raises(RuntimeError, match='runtime is uncertain'):
        driver.reconciled_tail(job)
    assert job['charged_wall_seconds'] == 20.0


def test_completion_clock_reconciles_only_actual_duration_and_binds_the_job(driver, tmp_path, monkeypatch):
    monkeypatch.setattr(driver, 'art', lambda: tmp_path)
    clock = tmp_path / 'clock.json'
    job = {'job_index': 3, 'started_epoch': 100.0, 'charged_wall_seconds': 20.0, 'workers': 4,
           'completion_clock': str(clock)}
    receipt = {'job_index': 3, 'started_epoch': 100.0, 'wall_seconds': 25.0}
    clock.write_text(json.dumps(receipt))
    assert driver.reconciled_tail(job) == 20.0
    receipt['job_index'] = 2
    clock.write_text(json.dumps(receipt))
    with pytest.raises(RuntimeError, match='does not identify'):
        driver.reconciled_tail(job)
    receipt['job_index'] = 3
    receipt['wall_seconds'] = 19.0
    clock.write_text(json.dumps(receipt))
    with pytest.raises(RuntimeError, match='already measured'):
        driver.reconciled_tail(job)


def test_clock_outside_project_artifacts_is_refused(driver, tmp_path, monkeypatch):
    monkeypatch.setattr(driver, 'art', lambda: tmp_path / 'artifacts')
    with pytest.raises(ValueError, match='inside primary'):
        driver.reconciled_tail({'completion_clock': str(tmp_path / 'outside.json')})
