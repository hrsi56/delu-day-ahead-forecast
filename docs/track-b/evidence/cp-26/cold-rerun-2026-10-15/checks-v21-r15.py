"""Affected r15 gate/provenance tests and three bounded supervision failures."""
from pathlib import Path
import os
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp26.budget import atomic
from cp26.gates import RUN_ID, RUN_EVIDENCE, code_identity, protocol_identity
from cp26.harness import art
import pytest

if os.environ.get('CP26_RUN_ID') != RUN_ID or int(os.environ.get('CP26_WORKERS', '0')) != 4:
    raise RuntimeError('registered four-slot affected test monitor required')
args = ['-q', 'tests/test_cp26_r15.py', 'tests/test_cp26_costing.py',
        'tests/test_cp26_execution.py', 'tests/test_cp26_gates.py',
        'tests/test_cp26_supervision.py::test_sigstop_supervisor_stops_verified_worker_even_after_launcher_loss',
        'tests/test_cp26_supervision.py::test_supervisor_stopped_inside_ledger_lock_is_killed_before_receipt',
        'tests/test_cp26_supervision.py::test_stopped_watchdog_is_detected_by_supervisor',
        'tests/test_cp26_run_accounting.py', '--basetemp', str(art() / 'cold-rerun-2026-10-15/calibration-r15/pytest')]
run_id = os.environ.pop('CP26_RUN_ID')
try:
    result = int(pytest.main(args))
finally:
    os.environ['CP26_RUN_ID'] = run_id
atomic(ROOT / RUN_EVIDENCE / 'checks-v21-r15.json', {
    'status': 'PASS' if result == 0 else 'FAIL', 'exit_code': result,
    'command': ['pytest.main', *args], 'code_sha256': code_identity(ROOT),
    'protocol': protocol_identity(ROOT), 'job_id': os.environ['CP26_JOB_ID'],
    'job_index': int(os.environ['CP26_JOB_INDEX']), 'run_id': RUN_ID,
    'scope': 'Changed admission, operational/scientific lineage, output metadata and independent observer behavior only; no real model fits.'})
raise SystemExit(result)
