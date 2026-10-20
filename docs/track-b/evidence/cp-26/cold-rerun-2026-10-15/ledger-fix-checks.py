"""Affected refresh/deadline/once-only/receipt checks in one supervised process."""
from pathlib import Path
import json
import os
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp26.budget import atomic
from cp26.gates import RUN_ID, RUN_EVIDENCE, code_identity, protocol_identity
from cp26.harness import art
import pytest

if os.environ.get('CP26_RUN_ID') != RUN_ID or int(os.environ.get('CP26_WORKERS', '0')) != 4:
    raise RuntimeError('registered four-slot test monitor required by the liveness test module')
names = [
    'test_five_valid_cold_refreshes_finish_before_deadline_exactly_once',
    'test_continuously_changing_cold_history_is_bounded_and_never_calls_sampler',
    'test_resource_deadline_refuses_slow_preparation_without_partial_charge',
    'test_peer_cold_append_merges_fresh_accounting_and_deduplicates_under_same_lock',
    'test_execution_append_preserves_history_and_exact_once_counts_without_duration',
    'test_resource_sample_cache_refresh_crash_keeps_authoritative_charge_exactly_once',
    'test_clock_appearance_during_resource_splice_is_rechecked_before_rename',
    'test_startup_hot_mutation_recovers_terminal_clock_and_refuses_admission',
]
args = ['-q', *['tests/test_cp26_ledger_liveness.py::' + name for name in names],
        'tests/test_cp26_run_accounting.py', '--basetemp', str(art() / 'cold-rerun-2026-10-15/ledger-fix/pytest')]
run_id = os.environ.pop('CP26_RUN_ID')
try:
    result = int(pytest.main(args))
finally:
    os.environ['CP26_RUN_ID'] = run_id
atomic(ROOT / RUN_EVIDENCE / 'ledger-fix-tests.json', {
    'status': 'PASS' if result == 0 else 'FAIL', 'exit_code': result,
    'command': ['pytest.main', *args], 'code_sha256': code_identity(ROOT),
    'protocol': protocol_identity(ROOT), 'job_id': os.environ['CP26_JOB_ID'],
    'job_index': int(os.environ['CP26_JOB_INDEX']), 'run_id': RUN_ID,
    'scope': 'Only changed resource refresh handling and existing directly affected invariants; no scientific test relabelling.'})
raise SystemExit(result)
