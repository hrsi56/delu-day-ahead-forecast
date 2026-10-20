"""Exercise persistent accounting liveness without relaxing supervision limits.

Execute this file only through a CP-26 monitor declaring four workers: the pytest
coordinator is counted conservatively alongside the three dedicated stress workers.
The four-inner-job arrival case blocks its controller while all four children can
compute; it validates only after the short admin child has vacated one slot.
The three isolated inner jobs each declare one worker and share their own ledger.
No research fits, data access, or production-ledger writes occur in these tests.
"""
import contextlib
import copy
from datetime import date, timedelta
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

import pytest

from cp26 import budget as B
from cp26 import supervisor as S
from test_cp26_monitor import job_and_receipt, real_monitor, wait_until


#: r15's operational calibration of the ledger and heartbeat deadlines (Owner approval of
#: 2026-10-16, capstone v21-r15 notice), preserved by the r16 authority. It supersedes the r14
#: values these stress tests were first written against: startup 10 s, heartbeat 2 s, ledger 0.5 s.
CALIBRATED_POLICY = {'startup_grace_seconds': 14.0, 'heartbeat_timeout_seconds': 8.0,
                     'poll_seconds': 0.2, 'ledger_timeout_seconds': 3.0}


def calibrated_policy_record():
    """The policy r15's calibration tested, and the limits the r16 authority preserved."""
    evidence = Path(__file__).resolve().parents[1] / 'docs/track-b/evidence/cp-26/cold-rerun-2026-10-15'
    tested = json.loads((evidence / 'calibration-v21-r15.json').read_text())['policy_tested']
    kept = json.loads((evidence / 'authority-v21-r16.json').read_text())['limits_preserved']
    assert kept == {'startup': tested['startup_grace_seconds'], 'heartbeat': tested['heartbeat_timeout_seconds'],
                    'poll': tested['poll_seconds'], 'ledger': tested['ledger_timeout_seconds']}
    return {name: float(tested[name]) for name in CALIBRATED_POLICY}


def history_ledger(budget, *, days=2441, closed_jobs=40):
    """Preserve realistic payload depth, terminal identities, and all task history."""
    budget.initialise()
    members = [f'{route}/native-{member:02d}'
               for route, count in (('nominal', 7), ('noload', 6), ('gfs6', 6))
               for member in range(count)]
    jobs = []
    for index in range(closed_jobs):
        identities = [{'pid': 1_000_000 + index * 20 + offset,
                       'create_time': 1000.0 + index * 30 + offset * 0.001}
                      for offset in range(20)]
        jobs.append({'name': f'historical-{index}', 'job_id': f'history/{index}',
                     'job_index': index, 'running': False, 'workers': 1,
                     'wall_seconds': 10.0 + index, 'charged_wall_seconds': 10.0 + index,
                     'live_rss_bytes': 0, 'peak_rss_bytes': 1024,
                     'worker_identities': identities, 'workers_stopped': True,
                     'group_empty': True, 'exit_code': 0, 'abort_reason': None,
                     'started_epoch': 1000.0 + index * 30,
                     'ended_epoch': 1010.0 + index * 31,
                     'request_sha256': f'{index:064x}'})
    measured = sum(job['wall_seconds'] for job in jobs)
    tasks = []
    for day_index in range(days):
        day = str(date(2019, 1, 1) + timedelta(days=day_index))
        tasks.extend([
            {'id': f'member-day/{"7" * 64}/{day}',
             'evidence': {'fit_identity_sha256': {route: f'{day_index * 3 + i:064x}'
                                                   for i, route in enumerate(('nominal', 'noload', 'gfs6'))},
                          'members': {member: {'cache_sha256': f'{day_index * 19 + i:064x}',
                                             'status': 'failed' if i == 18 and day_index % 97 == 0 else 'ok'}
                                      for i, member in enumerate(members)}},
             'counts': {'completed_native_member_days': 19}},
            {'id': f'issuance/{"7" * 64}/{day}',
             'evidence': {'ledger_sha256': f'{day_index:064x}'},
             'counts': {'completed_daily_issuances': 1}},
        ])
    for first in range(0, days, 28):
        chunk_first = str(date(2019, 1, 1) + timedelta(days=first))
        chunk_last = str(date(2019, 1, 1) + timedelta(days=min(first + 27, days - 1)))
        for route in ('nominal', 'noload', 'gfs6'):
            tasks.append({'id': f'phase/{"7" * 64}/fit-route/{route}/{chunk_first}/{chunk_last}',
                          'evidence': {'phase': 'fit-route', 'route': route,
                                       'first': chunk_first, 'last': chunk_last,
                                       'manifest_sha256': f'{first:064x}', 'status': 'COMPLETE'},
                          'counts': {'completed_execution_phases': 1}})
    with budget.transaction() as state:
        state.update(jobs=jobs, execution_tasks=tasks,
                     accounting={'measured_seconds': measured, 'reported_seconds': 10.0,
                                 'reserved_seconds': 20.0},
                     counts={'machine_seconds': measured + 30.0,
                             'completed_native_member_days': days * 19,
                             'completed_daily_issuances': days,
                             'completed_execution_phases': ((days + 27) // 28) * 3},
                     charges=[{'id': 'history/reported', 'seconds': 10.0, 'kind': 'reported',
                               'source': {'receipt_sha256': 'a' * 64}},
                              {'id': 'history/reserve', 'seconds': 20.0, 'kind': 'reserved',
                               'status': 'authorized', 'source': {'bound_sha256': 'b' * 64}}],
                     reserves=[{'id': 'history/reserve', 'seconds': 20.0, 'kind': 'reserved',
                                'status': 'authorized', 'source': {'bound_sha256': 'b' * 64}}],
                     events=[{'event': 'cp26_execution_task_terminal', 'task_id': task['id'],
                              'evidence_sha256': f'{index:064x}'}
                             for index, task in enumerate(tasks)],
                     nested_history={'rtl_label': 'היסטוריה', 'zero': 0, 'false': False,
                                     'null': None, 'rows': [{'hash': 'c' * 64, 'values': [1, 2.5]}]})
        state['repair_scope'] = {
            'id': 'closed-historical-repair', 'active': False,
            'baseline_seconds': 0.0, 'limit_seconds': B.REPAIR_SECONDS,
            'terminal_candidate_sha': 'd' * 40,
            'terminal_snapshot': {'repair_seconds_used': measured + 30.0,
                                  'total_seconds': measured + 30.0,
                                  'accounting': copy.deepcopy(state['accounting']),
                                  'resources_sha256': 'e' * 64, 'ledger_sha256': 'f' * 64,
                                  'terminal_candidate_sha': 'd' * 40}}
        state['continuation_scope'] = {'id': 'synthetic-continuation',
                                       'authority_sha256': 'a' * 64,
                                       'baseline_seconds': measured + 30.0,
                                       'ceiling_seconds': B.CAPS['machine_seconds']}
    return budget.read()


def assert_preserved_history(state, before, *, appended_tasks=0):
    assert state['jobs'][:len(before['jobs'])] == before['jobs']
    assert state['execution_tasks'][:len(before['execution_tasks'])] == before['execution_tasks']
    assert len(state['execution_tasks']) == len(before['execution_tasks']) + appended_tasks
    for key in ('charges', 'reserves', 'repair_scope',
                'continuation_scope', 'nested_history'):
        assert state[key] == before[key]
    assert state['events'][:len(before['events'])] == before['events']
    assert state['accounting']['reported_seconds'] == before['accounting']['reported_seconds']
    assert state['accounting']['reserved_seconds'] == before['accounting']['reserved_seconds']


def test_compact_transaction_preserves_nested_and_terminal_history(tmp_path):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=7, closed_jobs=3)
    with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS) as state:
        state['counts']['test_receipts'] = 1
    after = budget.read()
    expected = copy.deepcopy(before)
    expected['counts']['test_receipts'] = 1
    assert after == expected
    assert_preserved_history(after, before)
    compact = budget.path.read_bytes()
    pretty = json.dumps(after, indent=1, sort_keys=True, allow_nan=False).encode()
    assert len(compact) < len(pretty) * 0.95
    assert budget.last_transaction['acquired'] and budget.last_transaction['written']
    assert budget.last_transaction['written_bytes'] == len(compact)


@pytest.mark.parametrize('legacy_indented', [False, True])
def test_noop_transaction_preserves_existing_bytes_inode_and_mtime(tmp_path, legacy_indented):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=7, closed_jobs=3)
    if legacy_indented:
        budget.path.write_text(json.dumps(before, indent=1, sort_keys=True) + '\n')
    raw = budget.path.read_bytes()
    stat = budget.path.stat()
    with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS) as state:
        B.require_compute_ready(state)
        assert state['execution_tasks'] == before['execution_tasks']
    assert budget.path.read_bytes() == raw
    after_stat = budget.path.stat()
    assert (after_stat.st_ino, after_stat.st_mtime_ns) == (stat.st_ino, stat.st_mtime_ns)
    metrics = budget.last_transaction
    assert metrics['acquired'] and not metrics['written']
    assert metrics['read_bytes'] == len(raw) and metrics['written_bytes'] == 0


def invalidate_format_cache(budget, kind):
    cache = B._format_path(budget.path)
    if kind == 'missing':
        cache.unlink()
    elif kind == 'corrupt':
        cache.write_bytes(b'{invalid-cache')
    else:
        assert kind == 'mismatch'
        identity = json.loads(cache.read_bytes())
        identity['sha256'] = '0' * 64
        cache.write_text(json.dumps(identity))


def cache_bytes(budget):
    cache = B._format_path(budget.path)
    return cache.read_bytes() if cache.exists() else None


def install_matching_cache(budget, raw):
    # A matching digest accelerates comparison but cannot authorize accounting.
    cache = B._format_path(budget.path)
    identity = json.loads(cache.read_bytes())
    identity['sha256'] = hashlib.sha256(raw).hexdigest()
    cache.write_text(json.dumps(identity))


def test_foreign_compact_noncanonical_noop_keeps_original_representation(tmp_path):
    budget = B.Budget(tmp_path / 'budget.json')
    budget.initialise()
    state = budget.read()
    state['foreign_label'] = 'היסטוריה'
    raw = (json.dumps(state, separators=(',', ':'), ensure_ascii=False) + '\n').encode()
    raw = raw.replace(b'"machine_seconds":0.0', b'"machine_seconds":0e0')
    assert json.loads(raw) == state
    assert raw != B._ledger_json(state).encode()
    budget.path.write_bytes(raw)
    before_cache = cache_bytes(budget)
    stat = budget.path.stat()
    with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS) as loaded:
        B.require_compute_ready(loaded)
    assert budget.path.read_bytes() == raw
    assert cache_bytes(budget) == before_cache
    assert (budget.path.stat().st_ino, budget.path.stat().st_mtime_ns) == (stat.st_ino, stat.st_mtime_ns)
    assert not budget.last_transaction['canonical_input']
    assert not budget.last_transaction['written']


@pytest.mark.parametrize('kind', ['missing', 'corrupt', 'mismatch'])
def test_format_cache_fallback_refreshes_only_after_logical_mutation(tmp_path, kind):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=2, closed_jobs=1)
    invalidate_format_cache(budget, kind)
    raw = budget.path.read_bytes()
    stat = budget.path.stat()
    before_cache = cache_bytes(budget)
    with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS) as state:
        B.require_compute_ready(state)
    assert not budget.last_transaction['canonical_input'] and not budget.last_transaction['written']
    assert budget.path.read_bytes() == raw and cache_bytes(budget) == before_cache
    assert (budget.path.stat().st_ino, budget.path.stat().st_mtime_ns) == (stat.st_ino, stat.st_mtime_ns)
    with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS) as state:
        state['counts']['format_cache_test_receipts'] = 1
    assert not budget.last_transaction['canonical_input'] and budget.last_transaction['written']
    expected = copy.deepcopy(before)
    expected['counts']['format_cache_test_receipts'] = 1
    assert budget.read() == expected
    assert B._recognized_compact(budget.path, budget.path.read_bytes())
    assert_preserved_history(budget.read(), before)
    with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS):
        pass
    assert budget.last_transaction['canonical_input'] and not budget.last_transaction['written']


@pytest.mark.parametrize('kind', ['missing', 'corrupt', 'mismatch', 'matching'])
@pytest.mark.parametrize('violation,match', [
    ('parse', None), ('caps', 'resource contract changed'),
    ('accounting', 'classified accounting disagrees'),
    ('closed', 'closed repair scope is immutable'),
])
def test_format_cache_never_bypasses_ledger_contracts(tmp_path, kind, violation, match):
    budget = B.Budget(tmp_path / 'budget.json')
    state = history_ledger(budget, days=2, closed_jobs=1)
    if violation == 'caps':
        state['caps']['workers'] = 99
    elif violation == 'accounting':
        state['counts']['machine_seconds'] += 1
    raw = b'{invalid-ledger' if violation == 'parse' else B._ledger_json(state).encode()
    budget.path.write_bytes(raw)
    if kind == 'matching':
        install_matching_cache(budget, raw)
        assert B._recognized_compact(budget.path, raw)
    else:
        invalidate_format_cache(budget, kind)
        assert not B._recognized_compact(budget.path, raw)
    before_cache = cache_bytes(budget)
    stat = budget.path.stat()
    with pytest.raises(ValueError, match=match):
        with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS) as loaded:
            if violation == 'closed':
                loaded['repair_scope']['terminal_snapshot']['repair_seconds_used'] += 1
    assert budget.path.read_bytes() == raw and cache_bytes(budget) == before_cache
    assert (budget.path.stat().st_ino, budget.path.stat().st_mtime_ns) == (stat.st_ino, stat.st_mtime_ns)
    assert not budget.last_transaction['written']


@pytest.mark.parametrize('crash', [False, True])
def test_cache_write_failure_after_ledger_commit_preserves_exactly_once_charge(tmp_path, monkeypatch, crash):
    budget = B.Budget(tmp_path / 'budget.json')
    budget.initialise()
    initial_cache = cache_bytes(budget)
    original = B.atomic
    cache_attempts = []

    def failing_cache_write(path, value):
        if Path(path) == B._format_path(budget.path):
            committed = json.loads(budget.path.read_bytes())
            assert B.total_seconds(committed) == 5.0
            assert committed['charges'][0]['id'] == 'cache-write-seam'
            cache_attempts.append(value)
            if crash:
                raise RuntimeError('simulated process death after ledger rename')
            raise OSError('simulated optional-cache write failure')
        return original(path, value)

    monkeypatch.setattr(B, 'atomic', failing_cache_write)
    source = {'receipt_sha256': 'a' * 64}
    if crash:
        with pytest.raises(RuntimeError, match='simulated process death'):
            budget.record_charge('cache-write-seam', 5.0, 'measured', source)
    else:
        assert budget.record_charge('cache-write-seam', 5.0, 'measured', source)
        assert budget.last_transaction['written'] and budget.last_transaction['outcome'] == 'committed'
    assert len(cache_attempts) == 1 and cache_bytes(budget) == initial_cache
    assert B.total_seconds(budget.read()) == 5.0
    raw = budget.path.read_bytes()
    stat = budget.path.stat()
    assert not B._recognized_compact(budget.path, raw)
    restarted = B.Budget(budget.path)
    assert not restarted.record_charge('cache-write-seam', 5.0, 'measured', source)
    assert not restarted.last_transaction['canonical_input'] and not restarted.last_transaction['written']
    assert B.total_seconds(restarted.read()) == 5.0
    assert len(restarted.read()['charges']) == 1
    assert budget.path.read_bytes() == raw and cache_bytes(budget) == initial_cache
    assert (budget.path.stat().st_ino, budget.path.stat().st_mtime_ns) == (stat.st_ino, stat.st_mtime_ns)
    assert len(cache_attempts) == 1


@pytest.mark.parametrize('mutate', [False, True])
def test_recognized_compact_hot_transaction_encodes_full_ledger_only_after_body(tmp_path, monkeypatch, mutate):
    budget = B.Budget(tmp_path / 'budget.json')
    history_ledger(budget, days=2, closed_jobs=1)
    original = B._ledger_json
    encoded = []

    def counting_encoder(state):
        # The separate small closed-scope snapshot is still validated; count
        # only expensive full-ledger encodings containing the resource contract.
        if 'caps' in state:
            encoded.append(copy.deepcopy(state))
        return original(state)

    monkeypatch.setattr(B, '_ledger_json', counting_encoder)
    with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS) as state:
        assert encoded == []
        if mutate:
            state['counts']['hot_test_receipts'] = 1
    assert len(encoded) == 1
    assert encoded[0]['counts'].get('hot_test_receipts') == (1 if mutate else None)
    assert budget.last_transaction['canonical_input']
    assert budget.last_transaction['written'] is mutate


def force_peer_conflict(monkeypatch, budget, *, repeat=False):
    """Commit a real peer change immediately before the candidate's CAS flock."""
    original = B.fcntl.flock
    peer = B.Budget(budget.path)
    conflicts = []
    injecting = False

    def flock(lock, operation):
        nonlocal injecting
        if (operation == (B.fcntl.LOCK_EX | B.fcntl.LOCK_NB)
                and not injecting and (repeat or not conflicts)):
            injecting = True
            try:
                # Legacy transactions use blocking LOCK_EX, avoiding recursive
                # injection while preserving the peer's normal accounting guards.
                with peer.transaction() as state:
                    state['counts']['peer_commits'] = state['counts'].get('peer_commits', 0) + 1
                conflicts.append(peer.read()['counts']['peer_commits'])
            finally:
                injecting = False
        return original(lock, operation)

    monkeypatch.setattr(B.fcntl, 'flock', flock)
    return conflicts


def test_optimistic_update_retries_latest_state_without_duplicate_evidence_or_charge(tmp_path, monkeypatch):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=2, closed_jobs=1)
    conflicts = force_peer_conflict(monkeypatch, budget)
    callback_inputs = []

    def apply(state):
        callback_inputs.append(state['counts'].get('peer_commits', 0))
        state['counts']['logical_commits'] = state['counts'].get('logical_commits', 0) + 1
        B.add_seconds(state, 7.0)
        state['charges'].append({'id': 'optimistic-charge', 'seconds': 7.0, 'kind': 'measured',
                                'source': {'receipt_sha256': 'a' * 64}})
        state['execution_tasks'].append({'id': 'optimistic-task', 'evidence': {'sha256': 'b' * 64},
                                         'counts': {'logical_commits': 1}})
        state['events'].append({'event': 'optimistic-task-terminal', 'task_id': 'optimistic-task'})
        return state['counts']['logical_commits']

    assert budget.update(apply, timeout_seconds=S.LEDGER_TIMEOUT_SECONDS) == 1
    after = budget.read()
    assert conflicts == [1] and callback_inputs == [0, 1]
    assert after['counts']['logical_commits'] == 1 and after['counts']['peer_commits'] == 1
    assert B.total_seconds(after) == B.total_seconds(before) + 7.0
    assert after['charges'][:-1] == before['charges']
    assert sum(row['id'] == 'optimistic-charge' for row in after['charges']) == 1
    assert after['execution_tasks'][:-1] == before['execution_tasks']
    assert sum(row['id'] == 'optimistic-task' for row in after['execution_tasks']) == 1
    assert after['events'][:-1] == before['events']
    assert sum(row.get('task_id') == 'optimistic-task' for row in after['events']) == 1
    assert after['jobs'] == before['jobs'] and after['repair_scope'] == before['repair_scope']
    metrics = budget.last_transaction
    assert metrics['attempts'] == 2 and metrics['conflicts'] == 1
    assert metrics['body_seconds'] >= 0 and metrics['written']
    assert len(budget.telemetry()) <= 17
    assert budget.last_transaction['serialized_fallback']


@pytest.mark.parametrize('violation,match', [
    ('caps', 'resource contract changed'), ('accounting', 'classified accounting disagrees'),
    ('closed', 'closed repair scope is immutable'),
])
def test_optimistic_retry_revalidates_all_candidate_contracts(tmp_path, monkeypatch, violation, match):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=2, closed_jobs=1)
    conflicts = force_peer_conflict(monkeypatch, budget)
    calls = []

    def apply(state):
        calls.append(state['counts'].get('peer_commits', 0))
        state['counts']['logical_commits'] = state['counts'].get('logical_commits', 0) + 1
        if len(calls) == 2:
            if violation == 'caps':
                state['caps']['workers'] = 99
            elif violation == 'accounting':
                state['counts']['machine_seconds'] += 1
            else:
                state['repair_scope']['terminal_snapshot']['repair_seconds_used'] += 1

    with pytest.raises(ValueError, match=match):
        budget.update(apply, timeout_seconds=S.LEDGER_TIMEOUT_SECONDS)
    expected = copy.deepcopy(before)
    expected['counts']['peer_commits'] = 1
    assert conflicts == [1] and calls == [0, 1]
    assert budget.read() == expected
    assert not budget.last_transaction['written']


@pytest.mark.parametrize('violation,match', [
    ('caps', 'resource contract changed'), ('accounting', 'classified accounting disagrees'),
    ('closed', 'closed repair scope is immutable'),
])
def test_foreign_peer_revision_cannot_replace_retry_validation_baseline(tmp_path, monkeypatch, violation, match):
    budget = B.Budget(tmp_path / 'budget.json')
    history_ledger(budget, days=2, closed_jobs=1)
    original = B.fcntl.flock
    foreign = []
    callback_calls = []

    def flock(lock, operation):
        if operation == (B.fcntl.LOCK_EX | B.fcntl.LOCK_NB) and not foreign:
            with budget.path.with_suffix('.lock').open('a') as peer_lock:
                original(peer_lock, B.fcntl.LOCK_EX)
                changed = budget.read()
                if violation == 'caps':
                    changed['caps']['workers'] = 99
                elif violation == 'accounting':
                    changed['counts']['machine_seconds'] += 1
                else:
                    changed['repair_scope']['terminal_snapshot']['repair_seconds_used'] += 1
                # Model a foreign writer bypassing the API; a recognized format
                # cache cannot legitimize this substituted resource contract.
                B._write_ledger(budget.path, B._ledger_json(changed))
                foreign.append(budget.path.read_bytes())
        return original(lock, operation)

    def apply(state):
        callback_calls.append(1)
        state['counts']['logical_commits'] = 1

    monkeypatch.setattr(B.fcntl, 'flock', flock)
    with pytest.raises(ValueError, match=match):
        budget.update(apply, timeout_seconds=S.LEDGER_TIMEOUT_SECONDS)
    assert callback_calls == [1] and len(foreign) == 1
    assert budget.path.read_bytes() == foreign[0]
    assert B._recognized_compact(budget.path, foreign[0])
    assert 'logical_commits' not in budget.read()['counts']
    assert budget.last_transaction['attempts'] == 2 and budget.last_transaction['conflicts'] == 1
    assert not budget.last_transaction['written']


def test_always_conflicting_peer_commits_once_through_bounded_serialized_fallback(tmp_path, monkeypatch):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=2, closed_jobs=1)
    conflicts = force_peer_conflict(monkeypatch, budget, repeat=True)
    calls = []

    def apply(state):
        calls.append(state['counts'].get('peer_commits', 0))
        state['counts']['logical_commits'] = state['counts'].get('logical_commits', 0) + 1
        B.add_seconds(state, 5.0)
        state['charges'].append({'id': 'fallback-charge', 'seconds': 5.0, 'kind': 'measured',
                                'source': {'receipt_sha256': 'a' * 64}})
        return state['counts']['logical_commits']

    started = time.monotonic()
    assert budget.update(apply, timeout_seconds=S.LEDGER_TIMEOUT_SECONDS) == 1
    elapsed = time.monotonic() - started
    after = budget.read()
    assert len(calls) == 2 and calls[0] == 0 and calls[-1] == len(conflicts)
    assert conflicts
    assert after['counts']['peer_commits'] == len(conflicts)
    assert after['counts']['logical_commits'] == 1
    assert B.total_seconds(after) == B.total_seconds(before) + 5.0
    assert after['charges'][:-1] == before['charges']
    assert sum(row['id'] == 'fallback-charge' for row in after['charges']) == 1
    for key in ('jobs', 'execution_tasks', 'events', 'repair_scope', 'continuation_scope', 'reserves'):
        assert after[key] == before[key]
    metrics = budget.last_transaction
    assert metrics['attempts'] == 2 and metrics['conflicts'] == 1
    assert metrics['outcome'] == 'committed' and metrics['written']
    assert metrics['serialized_fallback']
    assert metrics['body_seconds'] >= 0
    assert elapsed < S.LEDGER_TIMEOUT_SECONDS
    assert budget.telemetry()['timeouts'] == 0 and len(budget.telemetry()) <= 17


@pytest.mark.parametrize('phase', ['initial', 'fallback'])
def test_slow_candidate_serialization_refuses_rename_after_overall_deadline(tmp_path, monkeypatch, phase):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=2, closed_jobs=1)
    original = B._ledger_json
    encoded_candidates = []
    calls = []
    conflicts = force_peer_conflict(monkeypatch, budget) if phase == 'fallback' else []

    def encode(state):
        serialized = original(state)
        if 'caps' in state and state['counts'].get('logical_commits') == 1:
            peer_commits = state['counts'].get('peer_commits', 0)
            encoded_candidates.append(peer_commits)
            if (phase == 'initial' and peer_commits == 0) or (phase == 'fallback' and peer_commits == 1):
                time.sleep(S.LEDGER_TIMEOUT_SECONDS + 0.05)
        return serialized

    def apply(state):
        calls.append(state['counts'].get('peer_commits', 0))
        state['counts']['logical_commits'] = 1

    monkeypatch.setattr(B, '_ledger_json', encode)
    started = time.monotonic()
    with pytest.raises(TimeoutError):
        budget.update(apply, timeout_seconds=S.LEDGER_TIMEOUT_SECONDS)
    elapsed = time.monotonic() - started
    expected = copy.deepcopy(before)
    if phase == 'fallback':
        expected['counts']['peer_commits'] = 1
        assert calls == [0, 1] and conflicts == [1] and encoded_candidates == [0, 1]
    else:
        assert calls == [0] and encoded_candidates == [0]
    assert budget.read() == expected
    assert not budget.last_transaction['written'] and budget.last_transaction['outcome'] == 'timeout'
    assert budget.last_transaction['serialized_fallback'] is (phase == 'fallback')
    assert S.LEDGER_TIMEOUT_SECONDS <= elapsed < S.HEARTBEAT_TIMEOUT_SECONDS


def test_transaction_telemetry_measures_wait_and_entire_hold(tmp_path):
    budget = B.Budget(tmp_path / 'budget.json')
    budget.initialise()
    started = time.monotonic()
    with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS) as state:
        time.sleep(0.03)
        state['counts']['test_receipts'] = 1
    elapsed = time.monotonic() - started
    metrics = budget.last_transaction
    assert metrics['acquired'] and metrics['written']
    assert 0 <= metrics['wait_seconds'] < S.LEDGER_TIMEOUT_SECONDS
    assert 0.03 <= metrics['hold_seconds'] < S.LEDGER_TIMEOUT_SECONDS
    assert metrics['wait_seconds'] + metrics['hold_seconds'] <= metrics['total_seconds'] + 0.01
    assert metrics['total_seconds'] <= elapsed + 0.01
    summary = budget.telemetry()
    assert summary['transactions'] >= 1 and summary['timeouts'] == 0
    assert summary['peak_wait_seconds'] >= metrics['wait_seconds']
    assert summary['peak_hold_seconds'] >= metrics['hold_seconds']


@pytest.mark.parametrize('method', ['transaction', 'update', 'resource_update'])
def test_lock_acquisition_timeout_has_bounded_failure_telemetry(tmp_path, method):
    budget = B.Budget(tmp_path / 'budget.json')
    budget.initialise()
    raw = budget.path.read_bytes()
    marker = tmp_path / 'holder.ready'
    holder_code = (
        'import fcntl, time; from pathlib import Path; '
        f'lock=Path({str(budget.path.with_suffix(".lock"))!r}).open("a"); '
        'fcntl.flock(lock, fcntl.LOCK_EX); '
        f'Path({str(marker)!r}).write_text("held"); time.sleep(30)')
    holder = subprocess.Popen([sys.executable, '-B', '-c', holder_code],
                              stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)
    try:
        wait_until(marker.exists, timeout=5)
        started = time.monotonic()
        with pytest.raises(TimeoutError, match='ledger accounting lock did not progress'):
            if method == 'transaction':
                with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS):
                    pytest.fail('held ledger lock admitted another writer')
            else:
                def apply(state):
                    state['counts']['blocked_update_receipts'] = 1
                getattr(budget, method)(apply, timeout_seconds=S.LEDGER_TIMEOUT_SECONDS)
        elapsed = time.monotonic() - started
        metrics = budget.last_transaction
        assert not metrics['acquired'] and not metrics['written']
        assert metrics['hold_seconds'] == 0
        assert S.LEDGER_TIMEOUT_SECONDS - 0.025 <= metrics['wait_seconds'] < S.HEARTBEAT_TIMEOUT_SECONDS
        assert metrics['total_seconds'] <= elapsed + 0.01
        assert elapsed < S.HEARTBEAT_TIMEOUT_SECONDS
        assert budget.telemetry()['timeouts'] == 1
        assert not metrics['serialized_fallback']
        assert budget.path.read_bytes() == raw
    finally:
        # The only signal target is the direct child this test just created.
        if holder.poll() is None:
            holder.kill()
        holder.wait(timeout=5)


def test_existing_positive_completion_clock_is_preserved_and_charged_once(tmp_path):
    state, job, first = job_and_receipt()
    clock = tmp_path / 'completion.json'
    raw = (json.dumps(first, indent=3) + '\n').encode()
    clock.write_bytes(raw)
    stat = clock.stat()
    later = {**first, 'wall_seconds': 999.0, 'ended_epoch': 1099.0, 'exit_code': 0}
    S._commit_completion(state, job, later, clock)
    assert B.total_seconds(state) == 100.0
    assert not job['running'] and job['wall_seconds'] == 25.0 and job['exit_code'] == 7
    S._commit_completion(state, job, later, clock)
    assert B.total_seconds(state) == 100.0
    assert clock.read_bytes() == raw
    assert (clock.stat().st_ino, clock.stat().st_mtime_ns) == (stat.st_ino, stat.st_mtime_ns)


def completion_budget(tmp_path, monkeypatch):
    monkeypatch.setattr(S, 'art', lambda: tmp_path)
    state, job, receipt = job_and_receipt()
    clock = tmp_path / 'completion.json'
    job['completion_clock'] = str(clock)
    budget = B.Budget(tmp_path / 'budget.json')
    budget.initialise()
    with budget.transaction() as saved:
        saved.update(state)
    return budget, receipt, clock


@pytest.mark.parametrize('role', ['supervisor', 'watchdog'])
def test_conflicting_tick_advances_sample_and_charge_once_without_mutating_inputs(tmp_path, monkeypatch, role):
    budget, _, _ = completion_budget(tmp_path, monkeypatch)
    with budget.transaction() as state:
        state['jobs'][0]['accounting_began_monotonic'] = 100.0
    updates = {'worker_identities': [{'pid': 15, 'create_time': 6.0}], 'peak_rss_bytes': 5}
    original_updates = copy.deepcopy(updates)
    conflicts = force_peer_conflict(monkeypatch, budget)
    assert S.tick(budget, 0, 'example-job', 25.0, 5, sample_role=role, **updates) is None
    after = budget.read()
    job = after['jobs'][0]
    assert conflicts == [1] and updates == original_updates
    assert B.total_seconds(after) == 100.0 and job['charged_wall_seconds'] == 25.0
    assert job[f'{role}_sample_sequence'] == job['accounting_sample_sequence'] == 1
    assert len(job['worker_identities']) == 2
    assert {(row['pid'], row['create_time']) for row in job['worker_identities']} == {(12, 3.0), (15, 6.0)}
    # Peer hot fields are merged fresh under flock, without stale whole-blob CAS.
    assert budget.last_transaction['attempts'] == 1 and budget.last_transaction['conflicts'] == 0


def publish_clock_before_first_cas(monkeypatch, budget, clock, raw):
    original = B.fcntl.flock
    published = []

    def flock(lock, operation):
        if operation == (B.fcntl.LOCK_EX | B.fcntl.LOCK_NB) and not published:
            # This peer holds the real accounting lock while publishing a clock,
            # then leaves the ledger unchanged: the clock-before-ledger seam.
            with budget.path.with_suffix('.lock').open('a') as peer_lock:
                original(peer_lock, B.fcntl.LOCK_EX)
                assert B.total_seconds(budget.read()) == 80.0
                clock.write_bytes(raw)
                published.append(raw)
        return original(lock, operation)

    monkeypatch.setattr(B.fcntl, 'flock', flock)
    return published


def test_terminal_clock_appearing_before_cas_reconciles_original_tail_without_idle_charge(tmp_path, monkeypatch):
    budget, receipt, clock = completion_budget(tmp_path, monkeypatch)
    raw = (json.dumps(receipt, indent=3) + '\n').encode()
    published = publish_clock_before_first_cas(monkeypatch, budget, clock, raw)
    # The fresh locked sample sees the new clock before any later wall charge.
    assert S.tick(budget, 0, 'example-job', 1000.0, 0) is None
    state = budget.read()
    job = state['jobs'][0]
    assert published == [raw]
    assert B.total_seconds(state) == 100.0
    assert not job['running'] and job['wall_seconds'] == job['charged_wall_seconds'] == 25.0
    assert job['exit_code'] == receipt['exit_code'] == 7
    assert clock.read_bytes() == raw
    assert budget.last_transaction['attempts'] == 1 and budget.last_transaction['conflicts'] == 0
    S.apply_completion(state, job, receipt)
    assert B.total_seconds(state) == 100.0


@pytest.mark.parametrize('change', ['appearance', 'replacement'])
def test_clock_guard_change_during_resource_merge_stops_before_any_charge(tmp_path, monkeypatch, change):
    budget, receipt, clock = completion_budget(tmp_path, monkeypatch)
    original_raw = (json.dumps(receipt, indent=2) + '\n').encode()
    if change == 'replacement':
        clock.write_bytes(original_raw)
        changed_raw = (json.dumps({**receipt, 'wall_seconds': 26.0, 'ended_epoch': 126.0}, indent=3) + '\n').encode()
    else:
        changed_raw = original_raw
    conflicts = force_peer_conflict(monkeypatch, budget)
    original_guard = S._completion_clock_token
    guard_calls = []

    def clock_token(state, index, job_id):
        guard_calls.append(1)
        if len(guard_calls) == 2:
            # The two calls surround the single fresh resource callback. This
            # foreign writer bypasses flock; legitimate receipt writers wait.
            clock.write_bytes(changed_raw)
        return original_guard(state, index, job_id)

    monkeypatch.setattr(S, '_completion_clock_token', clock_token)
    with pytest.raises(RuntimeError, match='terminal receipt changed during serialized mutation'):
        S.tick(budget, 0, 'example-job', 1000.0, 0)
    state = budget.read()
    assert conflicts == [1] and len(guard_calls) == 2
    assert B.total_seconds(state) == 80.0 and state['jobs'][0]['running']
    assert state['counts']['peer_commits'] == 1
    assert clock.read_bytes() == changed_raw
    assert not budget.last_transaction['written'] and not budget.last_transaction['serialized_fallback']
    assert budget.last_transaction['attempts'] == 1
    if change == 'appearance':
        # A fresh invocation can reconcile the now-present original clock, while
        # the rejected fallback has contributed no wall1000 candidate charge.
        assert S.tick(budget, 0, 'example-job', 1000.0, 0) is None
        assert B.total_seconds(budget.read()) == 100.0
        assert budget.read()['jobs'][0]['wall_seconds'] == 25.0


@pytest.mark.parametrize('field,value', [('request_sha256', 'b' * 64),
                                         ('workers_stopped', False), ('wall_seconds', 19.0)])
def test_invalid_clock_appearing_before_cas_cannot_authorize_later_time_charge(tmp_path, monkeypatch, field, value):
    budget, receipt, clock = completion_budget(tmp_path, monkeypatch)
    raw = (json.dumps({**receipt, field: value}, indent=2) + '\n').encode()
    before = budget.path.read_bytes()
    published = publish_clock_before_first_cas(monkeypatch, budget, clock, raw)
    with pytest.raises(RuntimeError):
        S.tick(budget, 0, 'example-job', 1000.0, 0)
    assert published == [raw] and clock.read_bytes() == raw
    assert budget.path.read_bytes() == before
    assert B.total_seconds(budget.read()) == 80.0 and budget.read()['jobs'][0]['running']
    assert not budget.last_transaction['written']


def test_crash_after_completion_clock_rename_is_recovered_before_any_peer_tick_charge(tmp_path, monkeypatch):
    budget, receipt, clock = completion_budget(tmp_path, monkeypatch)
    before = budget.path.read_bytes()
    original = S.apply_completion

    def crash_after_clock(state, job, value):
        assert json.loads(clock.read_bytes()) == receipt
        raise RuntimeError('simulated process death after completion clock rename')

    monkeypatch.setattr(S, 'apply_completion', crash_after_clock)
    with pytest.raises(RuntimeError, match='simulated process death'):
        with budget.transaction() as state:
            S._commit_completion(state, state['jobs'][0], receipt, clock)
    assert budget.path.read_bytes() == before
    assert B.total_seconds(budget.read()) == 80.0
    raw = clock.read_bytes()
    stat = clock.stat()
    monkeypatch.setattr(S, 'apply_completion', original)
    restarted = B.Budget(budget.path)
    assert S.tick(restarted, 0, 'example-job', 1000.0, 0) is None
    after = restarted.read()
    assert B.total_seconds(after) == 100.0
    assert not after['jobs'][0]['running'] and after['jobs'][0]['wall_seconds'] == 25.0
    assert clock.read_bytes() == raw
    assert (clock.stat().st_ino, clock.stat().st_mtime_ns) == (stat.st_ino, stat.st_mtime_ns)
    S.apply_completion(after, after['jobs'][0], receipt)
    assert B.total_seconds(after) == 100.0


@pytest.mark.parametrize('field,value', [('request_sha256', 'b' * 64),
                                         ('supervisor_identity', {'pid': 11, 'create_time': 99.0}),
                                         ('wall_seconds', -1.0), ('workers_stopped', False),
                                         ('group_empty', False)])
def test_invalid_existing_clock_cannot_be_replaced_by_positive_receipt(tmp_path, field, value):
    state, job, receipt = job_and_receipt()
    invalid = {**receipt, field: value}
    clock = tmp_path / 'completion.json'
    raw = (json.dumps(invalid, indent=2) + '\n').encode()
    clock.write_bytes(raw)
    before = copy.deepcopy(state)
    stat = clock.stat()
    with pytest.raises(RuntimeError):
        S._commit_completion(state, job, receipt, clock)
    assert state == before
    assert clock.read_bytes() == raw
    assert (clock.stat().st_ino, clock.stat().st_mtime_ns) == (stat.st_ino, stat.st_mtime_ns)


@pytest.mark.parametrize('field,value', [
    ('job_id', 'replacement-job'), ('job_index', 9), ('request_sha256', 'b' * 64),
    ('started_epoch', 101.0), ('workers', 3), ('accounting_began_monotonic', 101.0),
    ('supervisor_identity', {'pid': 11, 'create_time': 99.0}),
    ('watchdog_identity', {'pid': 13, 'create_time': 99.0}),
    ('monitor_identity', {'pid': 10, 'create_time': 99.0}),
    ('child_identity', {'pid': 12, 'create_time': 99.0}), ('worker_pgid', 99),
])
def test_completion_observation_refuses_substituted_binding(field, value):
    state, job, _ = job_and_receipt()
    job.update(accounting_began_monotonic=100.0, worker_pgid=12,
               watchdog_identity={'pid': 13, 'create_time': 4.0})
    observed = copy.deepcopy(job)
    S._check_completion_observation(job, observed)
    job[field] = value
    before = copy.deepcopy(state)
    with pytest.raises(RuntimeError, match='binding changed after ending observation'):
        S._check_completion_observation(job, observed)
    assert state == before and job['running'] and B.total_seconds(state) == 80.0


def assert_live_lock_telemetry(summary):
    assert summary['transactions'] >= 1 and summary['timeouts'] == 0
    assert 0 <= summary['wait_seconds'] < S.LEDGER_TIMEOUT_SECONDS
    assert 0 <= summary['hold_seconds'] < S.LEDGER_TIMEOUT_SECONDS
    assert 0 <= summary['peak_wait_seconds'] < S.LEDGER_TIMEOUT_SECONDS
    assert 0 <= summary['peak_hold_seconds'] < S.LEDGER_TIMEOUT_SECONDS
    # A summary stays bounded; repeated samples never become a growing trace.
    assert len(summary) <= 17
    assert isinstance(summary['serialized_fallback'], bool)


@contextlib.contextmanager
def three_real_monitors(tmp_path, budget, commands):
    """Launch exactly three production monitor jobs against one isolated ledger."""
    root = Path(__file__).resolve().parents[1]
    history_count = len(budget.read()['jobs'])
    child_env = os.environ.copy()
    child_env.update(CP26_PROJECT_ROOT=str(tmp_path), CP26_LEDGER=str(budget.path),
                     PYTHONPATH=str(root / 'src'), PYTHONDONTWRITEBYTECODE='1')
    created_names = {f'ledger-liveness-{index}' for index in range(len(commands))}
    processes = []
    try:
        for index, command in enumerate(commands):
            launch = [sys.executable, '-B', str(root / 'scripts/cp26_rebaseline.py'),
                      'monitor', '--name', f'ledger-liveness-{index}', '--workers', '1',
                      '--', *command]
            processes.append(subprocess.Popen(
                launch, cwd=root, env=child_env, stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                start_new_session=True))
        yield processes
    finally:
        # Historical rows contain synthetic identities and are never cleanup targets.
        for job in budget.read()['jobs'][history_count:]:
            if job.get('name') not in created_names:
                continue
            identities = [job.get('child_identity'), *job.get('worker_identities', []),
                          job.get('supervisor_identity'), job.get('watchdog_identity')]
            for identity in identities:
                S.signal_identity(identity, signal.SIGKILL)
        for process in processes:
            if process.poll() is None:
                process.kill()
            process.communicate(timeout=5)


def test_three_jobs_keep_fresh_supervision_with_full_future_history(tmp_path):
    budget = B.Budget(tmp_path / '.local/artifacts/cp-26/ledger/budget.json')
    before = history_ledger(budget)
    day_tasks = before['execution_tasks'][:2441 * 2]
    phase_tasks = before['execution_tasks'][2441 * 2:]
    assert len(day_tasks) == 2441 * 2
    assert len(phase_tasks) == ((2441 + 27) // 28) * 3
    assert all('members' not in task['evidence'] for task in phase_tasks)
    assert all(task['evidence']['phase'] == 'fit-route' for task in phase_tasks)
    assert {task['evidence']['route'] for task in phase_tasks} == {'nominal', 'noload', 'gfs6'}
    assert all(len(task['evidence']['members']) == 19
               for task in day_tasks[::2])
    assert all(set(task['evidence']['fit_identity_sha256']) == {'nominal', 'noload', 'gfs6'}
               for task in day_tasks[::2])
    assert len(before['events']) == len(before['execution_tasks'])
    assert all(len(job['worker_identities']) == 20 for job in before['jobs'])
    assert S.SUPERVISION_POLICY == CALIBRATED_POLICY == calibrated_policy_record()
    assert B.CAPS == {'machine_seconds': 500 * 3600, 'workers': 4, 'rss_bytes': 12 * 10**9,
                      'data_download_bytes': 0, 'remote_writes': 0, 'cost_usd': 0,
                      'gpu_jobs': 0, 'cloud_jobs': 0}
    release = tmp_path / 'workers.release'
    ready = [tmp_path / f'worker-{index}.ready' for index in range(3)]
    commands = []
    for marker in ready:
        code = ('import time; from pathlib import Path; '
                f'Path({str(marker)!r}).write_text("ready"); release=Path({str(release)!r}); '
                'deadline=time.monotonic()+30; '
                '\nwhile not release.exists() and time.monotonic()<deadline: time.sleep(0.025)\n'
                'assert release.exists()\ntime.sleep(8)\n')
        commands.append([sys.executable, '-B', '-c', code])
    with three_real_monitors(tmp_path, budget, commands) as processes:
        wait_until(lambda: all(marker.exists() for marker in ready), timeout=20)
        jobs = budget.read()['jobs'][len(before['jobs']):]
        assert len(jobs) == 3 and all(job['running'] for job in jobs)
        initial = {(job['job_id'], role): job[f'{role}_sample_sequence']
                   for job in jobs for role in ('supervisor', 'watchdog')}
        release.write_text('run')
        deadline = time.monotonic() + 6.0
        observations = 0
        while time.monotonic() < deadline:
            jobs = budget.read()['jobs'][len(before['jobs']):]
            now = time.monotonic()
            assert all(job['running'] for job in jobs)
            for job in jobs:
                for role in ('supervisor', 'watchdog'):
                    assert S.freshness_reason(job, role, now=now) is None
                    assert_live_lock_telemetry(job[f'{role}_ledger_lock_telemetry'])
            observations += 1
            time.sleep(S.POLL_SECONDS)
        assert observations >= 5
        for job in jobs:
            for role in ('supervisor', 'watchdog'):
                assert job[f'{role}_sample_sequence'] >= initial[job['job_id'], role] + 5
        for process in processes:
            stdout, stderr = process.communicate(timeout=20)
            assert process.returncode == 0, (stdout, stderr)
        after = budget.read()
        assert_preserved_history(after, before)
        completed = after['jobs'][len(before['jobs']):]
        assert len(completed) == 3
        for job in completed:
            receipt = json.loads(Path(job['completion_clock']).read_text())
            assert not job['running'] and job['exit_code'] == 0 and not job['abort_reason']
            assert receipt['workers_stopped'] and receipt['group_empty']
            assert receipt['completion_issuer'] == 'supervisor'
            assert receipt['workers'] == job['workers'] == 1
            assert_live_lock_telemetry(receipt['ledger_lock_telemetry'])
        assert B.total_seconds(after) == pytest.approx(
            B.total_seconds(before) + sum(job['wall_seconds'] * job['workers'] for job in completed))


def test_wedged_supervisor_lock_still_gets_independent_ending_receipt(tmp_path):
    executed = tmp_path / 'worker.executed'
    wedged = tmp_path / 'supervisor.wedged'
    worker = ('import time; from pathlib import Path; '
              f'Path({str(executed)!r}).write_text("executed"); time.sleep(30)')
    patch = (
        'import sys, time; from pathlib import Path; from cp26 import supervisor as S; '
        f'executed=Path({str(executed)!r}); wedged=Path({str(wedged)!r}); original=S.tick\n'
        'def tick(budget, *args, **kwargs):\n'
        '    result=original(budget, *args, **kwargs)\n'
        '    if executed.exists():\n'
        '        with budget.transaction(timeout_seconds=S.LEDGER_TIMEOUT_SECONDS):\n'
        '            wedged.write_text("lock held")\n'
        '            time.sleep(30)\n'
        '    return result\n'
        'S.tick=tick\n'
        'raise SystemExit(S.run(Path(sys.argv[1])))\n')
    # real_monitor patches only its created supervisor; the detached watchdog
    # independently imports unmodified production code and keeps the calibrated ledger timeout.
    with real_monitor(tmp_path, [sys.executable, '-B', '-c', worker],
                      workers=1, supervisor_code=patch) as (process, budget):
        wait_until(wedged.exists, timeout=12)
        process.communicate(timeout=12)
        state = budget.read()
        job = state['jobs'][-1]
        receipt = json.loads(Path(job['completion_clock']).read_text())
        assert process.returncode == 70
        assert receipt['completion_issuer'] == 'watchdog'
        assert receipt['abort_reason'].startswith('watchdog_TimeoutError:')
        assert 'ledger accounting lock did not progress' in receipt['abort_reason']
        assert not job['running'] and receipt['workers_stopped'] and receipt['group_empty']
        assert receipt['wall_seconds'] > 0
        assert B.total_seconds(state) == pytest.approx(receipt['wall_seconds'])
        telemetry = receipt['ledger_lock_telemetry']
        assert telemetry['timeouts'] >= 1 and telemetry['outcome'] == 'timeout'
        assert not telemetry['acquired'] and not telemetry['written']
        assert telemetry['hold_seconds'] == 0
        assert S.LEDGER_TIMEOUT_SECONDS - 0.025 <= telemetry['wait_seconds'] < S.HEARTBEAT_TIMEOUT_SECONDS
        assert S.identity_status(job['child_identity']) in ('gone', 'reused')
        assert S.identity_status(job['supervisor_identity']) in ('gone', 'reused')


def test_supervisor_startup_accounting_wait_uses_declared_poll_cadence(tmp_path):
    marker = tmp_path / 'startup-sleep.json'
    patch = (
        'import json, sys; from pathlib import Path; from cp26 import supervisor as S; '
        f'marker=Path({str(marker)!r}); original_sleep=S.time.sleep; original_fresh=S.freshness_reason; '
        'probe={"forced":False,"pending":False}\n'
        'def fresh(job, role, **kwargs):\n'
        '    result=original_fresh(job, role, **kwargs)\n'
        '    if role == "watchdog" and job.get("child_identity") is None and not probe["forced"]:\n'
        '        probe.update(forced=True, pending=True)\n'
        '        return "startup_probe_pending"\n'
        '    return result\n'
        'def sleep(seconds):\n'
        '    if probe["pending"]:\n'
        '        marker.write_text(json.dumps({"seconds":seconds,"policy":S.POLL_SECONDS}))\n'
        '        probe["pending"]=False\n'
        '    original_sleep(seconds)\n'
        'S.freshness_reason=fresh; S.time.sleep=sleep\n'
        'raise SystemExit(S.run(Path(sys.argv[1])))\n')
    command = [sys.executable, '-B', '-c', 'import time; time.sleep(0.2)']
    with real_monitor(tmp_path, command, workers=1, supervisor_code=patch) as (process, budget):
        stdout, stderr = process.communicate(timeout=15)
        assert process.returncode == 0, (stdout, stderr)
        assert json.loads(marker.read_text()) == {'seconds': S.POLL_SECONDS, 'policy': S.POLL_SECONDS}
        assert S.POLL_SECONDS == 0.2
        job = budget.read()['jobs'][-1]
        assert not job['running'] and not job['abort_reason'] and job['exit_code'] == 0


@pytest.mark.parametrize('foreign_pretty', [False, True])
def test_resource_samples_preserve_exact_cold_spans_without_reparse(tmp_path, monkeypatch, foreign_pretty):
    budget = B.Budget(tmp_path / 'budget.json')
    history_ledger(budget, days=7, closed_jobs=3)
    with budget.transaction() as state:
        state['escaped"key}{'] = {'quoted': '\\"},"jobs":[{"running":true}],"caps":{"workers":99}',
                                 'nested': {'jobs': [], 'caps': {'workers': 99}}, 'unicode': 'היסטוריה'}
    before = budget.read()
    if foreign_pretty:
        budget.path.write_text(json.dumps(before, indent=3, ensure_ascii=False) + ' \n')
    raw = budget.path.read_bytes()
    view = budget.resource_read()
    assert set(view) == set(before) & B._RESOURCE_FIELDS
    spans = budget._resource_spans
    cold = {key: value for key, _, value in spans[0] if key not in B._RESOURCE_FIELDS}

    def forbid_full_parse(_):
        raise AssertionError('unchanged cold history must not be decoded on a resource sample')
    monkeypatch.setattr(B, '_resource_layout', forbid_full_parse)
    for number in range(3):
        def sample(state):
            assert 'execution_tasks' not in state and 'events' not in state
            B.add_seconds(state, 3.0)
            state['counts']['resource_samples'] = number + 1
        budget.resource_update(sample, timeout_seconds=S.LEDGER_TIMEOUT_SECONDS)
        assert budget.resource_read()['counts']['resource_samples'] == number + 1
    after = budget.read()
    expected = copy.deepcopy(before)
    B.add_seconds(expected, 9.0)
    expected['counts']['resource_samples'] = 3
    assert after == expected
    assert all(value in budget.path.read_bytes().decode('utf-8') for value in cold.values())
    assert B._resource_match(budget.path.read_bytes(), spans) == budget.resource_read()
    assert raw != budget.path.read_bytes()
    assert budget.last_transaction['attempts'] == 1 and budget.last_transaction['conflicts'] == 0
    assert B._recognized_compact(budget.path, budget.path.read_bytes()) is not foreign_pretty


@pytest.mark.parametrize('foreign_pretty', [False, True])
def test_resource_noop_preserves_authoritative_bytes_and_inode(tmp_path, foreign_pretty):
    budget = B.Budget(tmp_path / 'budget.json')
    history_ledger(budget, days=3, closed_jobs=1)
    if foreign_pretty:
        budget.path.write_text(json.dumps(budget.read(), indent=3, sort_keys=True) + '\n')
    raw = budget.path.read_bytes()
    stat = budget.path.stat()
    assert budget.resource_update(B.require_compute_ready) is None
    assert budget.path.read_bytes() == raw
    assert (budget.path.stat().st_ino, budget.path.stat().st_mtime_ns) == (stat.st_ino, stat.st_mtime_ns)
    assert not budget.last_transaction['written']


@pytest.mark.parametrize('field', ['caps', 'schema', 'reserves', 'repair_scope', 'continuation_scope',
                                    'events', 'execution_tasks', 'charges', 'nested_history'])
def test_resource_callback_cannot_mutate_policy_or_cold_evidence(tmp_path, field):
    budget = B.Budget(tmp_path / 'budget.json')
    history_ledger(budget, days=2, closed_jobs=1)
    raw = budget.path.read_bytes()
    def prohibited(state):
        B.add_seconds(state, 7.0)
        state[field] = {'replacement': True}
    with pytest.raises(ValueError, match='cannot change cold fields or policy'):
        budget.resource_update(prohibited)
    assert budget.path.read_bytes() == raw and not budget.last_transaction['written']


@pytest.mark.parametrize('change', ['growth', 'new_key', 'reorder', 'escaped_key', 'nested_fake_hot'])
def test_authoritative_cold_or_structure_change_requires_full_fresh_validation(tmp_path, monkeypatch, change):
    budget = B.Budget(tmp_path / 'budget.json')
    history_ledger(budget, days=3, closed_jobs=2)
    budget.resource_read()
    full_parse = B._resource_layout
    parses = []
    def track(raw):
        parses.append(raw)
        return full_parse(raw)
    monkeypatch.setattr(B, '_resource_layout', track)
    state = budget.read()
    if change == 'growth':
        state['execution_tasks'].append({'id': 'new-terminal', 'evidence': {'sha256': '9' * 64}})
    elif change == 'new_key':
        state['new_history'] = {'receipt': '8' * 64}
    elif change == 'reorder':
        state = dict(reversed(list(state.items())))
    elif change == 'escaped_key':
        state['a"}:,\\key'] = {'quoted': '"jobs":[],"caps":{"workers":99}'}
    else:
        state['nested_history']['fake'] = {'jobs': [{'running': True}], 'caps': {'workers': 99}}
    foreign = (json.dumps(state, indent=2, ensure_ascii=False) + '\n').encode()
    budget.path.write_bytes(foreign)
    install_matching_cache(budget, foreign)
    view = budget.resource_read()
    assert parses == [foreign] and view == {key: value for key, value in state.items() if key in B._RESOURCE_FIELDS}
    assert budget.path.read_bytes() == foreign
    assert budget.resource_update(lambda fresh: fresh['counts'].update(resource_refreshed=1)) is None
    assert parses == [foreign]
    expected = copy.deepcopy(state)
    expected['counts']['resource_refreshed'] = 1
    assert budget.read() == expected


@pytest.mark.parametrize('literal', ['NaN', 'Infinity', '-Infinity', '1e999'])
@pytest.mark.parametrize('location', ['cold', 'hot'])
def test_resource_view_rejects_nonfinite_authoritative_fields_even_with_matching_disk_cache(
        tmp_path, literal, location):
    budget = B.Budget(tmp_path / 'budget.json')
    history_ledger(budget, days=2, closed_jobs=1)
    with budget.transaction() as state:
        state['nested_history']['nonfinite_probe'] = 'COLD_SENTINEL'
        state['jobs'][0]['nonfinite_probe'] = 'HOT_SENTINEL'
    budget.resource_read()
    state = budget.read()
    sentinel = 'HOT_SENTINEL' if location == 'hot' else 'COLD_SENTINEL'
    foreign = B._ledger_json(state).replace(json.dumps(sentinel), literal).encode()
    budget.path.write_bytes(foreign)
    install_matching_cache(budget, foreign)
    with pytest.raises(ValueError):
        budget.resource_read()
    with pytest.raises(ValueError):
        budget.resource_update(lambda fresh: B.add_seconds(fresh, 1.0))
    assert budget.path.read_bytes() == foreign and not budget.last_transaction['written']


@pytest.mark.parametrize('change', ['duplicate_caps', 'missing_root_close', 'trailing_object', 'broken_cold'])
def test_resource_span_cache_cannot_hide_malformed_or_duplicate_root_json(tmp_path, change):
    budget = B.Budget(tmp_path / 'budget.json')
    history_ledger(budget, days=2, closed_jobs=1)
    budget.resource_read()
    raw = budget.path.read_bytes().rstrip()
    if change == 'duplicate_caps':
        foreign = raw[:-1] + b',"caps":{"workers":99}}'
    elif change == 'missing_root_close':
        foreign = raw[:-1]
    elif change == 'trailing_object':
        foreign = raw + b' {}'
    else:
        foreign = raw.replace(b'"rtl_label":', b'"rtl_label"=', 1)
    budget.path.write_bytes(foreign)
    install_matching_cache(budget, foreign)
    with pytest.raises(ValueError):
        budget.resource_read()
    assert budget.path.read_bytes() == foreign


def test_cold_change_at_lock_boundary_refreshes_outside_lock_and_commits_once(tmp_path, monkeypatch):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=3, closed_jobs=1)
    budget.resource_read()
    original_flock = B.fcntl.flock
    original_parse = B._resource_layout
    injected = []
    parses = []
    calls = []

    def inject(lock, operation):
        if operation == (B.fcntl.LOCK_EX | B.fcntl.LOCK_NB) and not injected:
            state = budget.read()
            state['events'].append({'event': 'cold-peer', 'evidence_sha256': '9' * 64})
            with budget.path.with_suffix('.lock').open('a') as peer_lock:
                original_flock(peer_lock, B.fcntl.LOCK_EX)
                B._write_ledger(budget.path, B._ledger_json(state))
            injected.append(budget.path.read_bytes())
        return original_flock(lock, operation)

    def parse_outside_lock(raw):
        # A separately opened fd cannot acquire flock if the updater retained it.
        with budget.path.with_suffix('.lock').open('a') as probe:
            original_flock(probe, B.fcntl.LOCK_EX | B.fcntl.LOCK_NB)
        parses.append(raw)
        return original_parse(raw)

    def sample(state):
        calls.append(1)
        B.add_seconds(state, 7.0)
        state['counts']['resource_merge'] = 1

    monkeypatch.setattr(B.fcntl, 'flock', inject)
    monkeypatch.setattr(B, '_resource_layout', parse_outside_lock)
    budget.resource_update(sample, timeout_seconds=S.LEDGER_TIMEOUT_SECONDS)
    after = budget.read()
    assert parses == injected and calls == [1]
    expected = copy.deepcopy(before)
    expected['events'].append({'event': 'cold-peer', 'evidence_sha256': '9' * 64})
    B.add_seconds(expected, 7.0)
    expected['counts']['resource_merge'] = 1
    assert after == expected
    metrics = budget.last_transaction
    assert metrics['attempts'] == 2 and metrics['conflicts'] == 1
    assert not metrics['serialized_fallback'] and metrics['written']


def test_continuously_changing_cold_history_is_bounded_and_never_calls_sampler(tmp_path, monkeypatch):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=2, closed_jobs=1)
    budget.resource_read()
    original_flock = B.fcntl.flock
    peers = []
    calls = []

    def inject(lock, operation):
        if operation == (B.fcntl.LOCK_EX | B.fcntl.LOCK_NB):
            state = budget.read()
            state['events'].append({'event': 'cold-peer', 'sequence': len(peers) + 1})
            with budget.path.with_suffix('.lock').open('a') as peer_lock:
                original_flock(peer_lock, B.fcntl.LOCK_EX)
                B._write_ledger(budget.path, B._ledger_json(state))
            peers.append(budget.path.read_bytes())
            time.sleep(0.12)
        return original_flock(lock, operation)

    def sample(state):
        calls.append(1)
        B.add_seconds(state, 7.0)
    monkeypatch.setattr(B.fcntl, 'flock', inject)
    started = time.monotonic()
    with pytest.raises(TimeoutError, match='absolute deadline expired before cold-history refresh'):
        budget.resource_update(sample)
    elapsed = time.monotonic() - started
    after = budget.read()
    assert S.LEDGER_TIMEOUT_SECONDS <= elapsed < S.HEARTBEAT_TIMEOUT_SECONDS
    assert calls == [] and len(peers) > 3
    assert after['events'] == before['events'] + [
        {'event': 'cold-peer', 'sequence': number} for number in range(1, len(peers) + 1)]
    assert B.total_seconds(after) == B.total_seconds(before)
    assert budget.path.read_bytes() == peers[-1] and not budget.last_transaction['written']
    assert budget.last_transaction['attempts'] == budget.last_transaction['conflicts'] == len(peers)
    assert budget.last_transaction['outcome'] == 'timeout'


@pytest.mark.parametrize('mutation', ['resource', 'task'])
def test_five_valid_cold_refreshes_finish_before_deadline_exactly_once(tmp_path, monkeypatch, mutation):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=2, closed_jobs=1)
    budget._task_index_needed = True
    budget.resource_read()
    original_flock = B.fcntl.flock
    peers, calls = [], []

    def inject(lock, operation):
        if operation == (B.fcntl.LOCK_EX | B.fcntl.LOCK_NB) and len(peers) < 5:
            state = budget.read()
            state['events'].append({'event': 'cold-peer', 'sequence': len(peers) + 1})
            with budget.path.with_suffix('.lock').open('a') as peer_lock:
                original_flock(peer_lock, B.fcntl.LOCK_EX)
                B._write_ledger(budget.path, B._ledger_json(state))
            peers.append(budget.path.read_bytes())
        return original_flock(lock, operation)

    def sample(state):
        calls.append(1)
        B.add_seconds(state, 7.0)
        state['counts']['resource_merge'] = state['counts'].get('resource_merge', 0) + 1

    monkeypatch.setattr(B.fcntl, 'flock', inject)
    if mutation == 'resource':
        budget.resource_update(sample)
    else:
        from cp26.execution import record_evidence_once
        assert record_evidence_once(budget, 'five-refresh-task', {'sha256': 'f' * 64}, {'new_task': 1})
    metrics = budget.last_transaction.copy()
    after = budget.read()
    assert metrics['total_seconds'] < S.LEDGER_TIMEOUT_SECONDS
    assert metrics['attempts'] == 6 and metrics['conflicts'] == len(peers) == 5
    assert metrics['outcome'] == 'committed' and metrics['written']
    assert after['events'][:len(before['events']) + 5] == before['events'] + [
        {'event': 'cold-peer', 'sequence': n} for n in range(1, 6)]
    if mutation == 'resource':
        assert calls == [1] and after['counts']['resource_merge'] == 1
        assert B.total_seconds(after) == B.total_seconds(before) + 7.0
        assert after['execution_tasks'] == before['execution_tasks']
    else:
        assert calls == [] and after['counts']['new_task'] == 1
        assert B.total_seconds(after) == B.total_seconds(before)
        assert len(after['execution_tasks']) == len(before['execution_tasks']) + 1
        assert not record_evidence_once(budget, 'five-refresh-task', {'sha256': 'f' * 64}, {'new_task': 1})
        assert budget.read() == after


@pytest.mark.parametrize('phase', ['initial_cold', 'resource_body', 'resource_splice'])
def test_resource_deadline_refuses_slow_preparation_without_partial_charge(tmp_path, monkeypatch, phase):
    budget = B.Budget(tmp_path / 'budget.json')
    history_ledger(budget, days=2, closed_jobs=1)
    if phase != 'initial_cold':
        budget.resource_read()
    raw = budget.path.read_bytes()
    calls = []
    if phase == 'initial_cold':
        original = B._resource_layout
        def slow_parse(value):
            time.sleep(S.LEDGER_TIMEOUT_SECONDS + 0.03)
            return original(value)
        monkeypatch.setattr(B, '_resource_layout', slow_parse)
    elif phase == 'resource_splice':
        original = B._resource_splice
        def slow_splice(layout, state):
            time.sleep(S.LEDGER_TIMEOUT_SECONDS + 0.03)
            return original(layout, state)
        monkeypatch.setattr(B, '_resource_splice', slow_splice)
    def sample(state):
        calls.append(1)
        if phase == 'resource_body':
            time.sleep(S.LEDGER_TIMEOUT_SECONDS + 0.03)
        B.add_seconds(state, 7.0)
    started = time.monotonic()
    with pytest.raises(TimeoutError, match='ledger accounting lock did not progress'):
        budget.resource_update(sample)
    elapsed = time.monotonic() - started
    assert S.LEDGER_TIMEOUT_SECONDS <= elapsed < S.HEARTBEAT_TIMEOUT_SECONDS
    assert calls == ([] if phase == 'initial_cold' else [1])
    assert budget.path.read_bytes() == raw and not budget.last_transaction['written']
    assert budget.last_transaction['outcome'] == 'timeout'


@pytest.mark.parametrize('violation,match', [
    ('caps', 'resource contract changed'), ('accounting', 'classified accounting disagrees'),
    ('closed', 'closed repair scope is immutable')])
def test_fresh_hot_resource_contract_is_checked_before_sampler(tmp_path, monkeypatch, violation, match):
    budget = B.Budget(tmp_path / 'budget.json')
    history_ledger(budget, days=2, closed_jobs=1)
    budget.resource_read()
    state = budget.read()
    if violation == 'caps':
        state['caps']['workers'] = 99
    elif violation == 'accounting':
        state['accounting']['measured_seconds'] += 1
    else:
        state['repair_scope']['terminal_snapshot']['repair_seconds_used'] += 1
    raw = B._ledger_json(state).encode()
    budget.path.write_bytes(raw)
    install_matching_cache(budget, raw)
    calls = []
    with pytest.raises(ValueError, match=match):
        budget.resource_update(lambda fresh: calls.append(fresh))
    assert calls == [] and budget.path.read_bytes() == raw
    assert not budget.last_transaction['written']


def test_legacy_missing_accounting_resource_charge_keeps_full_schema_and_history(tmp_path):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=2, closed_jobs=1)
    # A legacy total is conservatively measured, as in the generic API.
    del before['accounting']
    budget.path.write_text(B._ledger_json(before))
    budget.resource_update(lambda state: B.add_seconds(state, 7.0))
    after = budget.read()
    expected = copy.deepcopy(before)
    B.add_seconds(expected, 7.0)
    assert after == expected
    assert budget.resource_read()['accounting'] == expected['accounting']


def test_fresh_peer_tick_is_merged_without_duplicate_charge_or_sequence(tmp_path, monkeypatch):
    budget, _, _ = completion_budget(tmp_path, monkeypatch)
    with budget.transaction() as state:
        state['jobs'][0]['accounting_began_monotonic'] = 100.0
    budget.resource_read()
    peer = B.Budget(budget.path)
    peer.resource_read()
    original_flock = B.fcntl.flock
    injected = []
    injecting = False

    def inject(lock, operation):
        nonlocal injecting
        if operation == (B.fcntl.LOCK_EX | B.fcntl.LOCK_NB) and not injecting and not injected:
            injecting = True
            try:
                S.tick(peer, 0, 'example-job', 26.0, 7, sample_role='watchdog')
                injected.append(1)
            finally:
                injecting = False
        return original_flock(lock, operation)

    monkeypatch.setattr(B.fcntl, 'flock', inject)
    assert S.tick(budget, 0, 'example-job', 25.0, 5, sample_role='supervisor') is None
    after = budget.read()
    job = after['jobs'][0]
    assert injected == [1]
    assert B.total_seconds(after) == 104.0 and job['charged_wall_seconds'] == 26.0
    assert job['live_rss_bytes'] == 7
    assert job['supervisor_sample_sequence'] == job['watchdog_sample_sequence'] == 1
    assert job['accounting_sample_sequence'] == 2
    assert budget.last_transaction['attempts'] == 1 and budget.last_transaction['conflicts'] == 0


@pytest.mark.parametrize('kind', ['missing', 'corrupt', 'mismatch', 'forged_offsets'])
def test_resource_span_proof_never_trusts_optional_disk_accelerator(tmp_path, monkeypatch, kind):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=2, closed_jobs=1)
    if kind == 'forged_offsets':
        raw = budget.path.read_bytes()
        B._format_path(budget.path).write_text(json.dumps({
            'format': B._COMPACT_LEDGER_FORMAT, 'sha256': hashlib.sha256(raw).hexdigest(),
            'cold_offsets': [[0, len(raw)]], 'jobs': [], 'caps': B.CAPS}))
    else:
        invalidate_format_cache(budget, kind)
    original_parse = B._resource_layout
    parses = []
    def parse(raw):
        parses.append(raw)
        return original_parse(raw)
    monkeypatch.setattr(B, '_resource_layout', parse)
    budget.resource_read()
    assert parses == [budget.path.read_bytes()]
    budget.resource_update(lambda state: B.add_seconds(state, 3.0))
    assert len(parses) == 1
    expected = copy.deepcopy(before)
    B.add_seconds(expected, 3.0)
    assert budget.read() == expected


def test_resource_sample_cache_refresh_crash_keeps_authoritative_charge_exactly_once(tmp_path, monkeypatch):
    budget, _, clock = completion_budget(tmp_path, monkeypatch)
    with budget.transaction() as state:
        state['jobs'][0]['accounting_began_monotonic'] = 100.0
    budget.resource_read()
    original_atomic = B.atomic
    crashed = []
    def crash_format(path, value):
        if path == B._format_path(budget.path) and not crashed:
            crashed.append(1)
            raise RuntimeError('simulated death after resource ledger rename')
        return original_atomic(path, value)
    monkeypatch.setattr(B, 'atomic', crash_format)
    with pytest.raises(RuntimeError, match='simulated death after resource ledger rename'):
        S.tick(budget, 0, 'example-job', 25.0, 5, sample_role='supervisor')
    assert crashed == [1] and not clock.exists()
    committed = budget.read()
    assert B.total_seconds(committed) == 100.0
    assert committed['jobs'][0]['charged_wall_seconds'] == 25.0
    assert not B._recognized_compact(budget.path, budget.path.read_bytes())
    restarted = B.Budget(budget.path)
    S.tick(restarted, 0, 'example-job', 25.0, 5, sample_role='watchdog')
    after = restarted.read()
    assert B.total_seconds(after) == 100.0
    assert after['jobs'][0]['charged_wall_seconds'] == 25.0
    assert after['jobs'][0]['supervisor_sample_sequence'] == after['jobs'][0]['watchdog_sample_sequence'] == 1
    assert after['jobs'][0]['accounting_sample_sequence'] == 2


def test_clock_appearance_during_resource_splice_is_rechecked_before_rename(tmp_path, monkeypatch):
    budget, receipt, clock = completion_budget(tmp_path, monkeypatch)
    before = budget.path.read_bytes()
    original_splice = B._resource_splice
    published = []
    def publish(layout, state):
        candidate = original_splice(layout, state)
        raw = (json.dumps(receipt, indent=2) + '\n').encode()
        clock.write_bytes(raw)
        published.append(raw)
        return candidate
    monkeypatch.setattr(B, '_resource_splice', publish)
    with pytest.raises(RuntimeError, match='terminal receipt changed during serialized mutation'):
        S.tick(budget, 0, 'example-job', 1000.0, 0)
    assert budget.path.read_bytes() == before and published == [clock.read_bytes()]
    assert B.total_seconds(budget.read()) == 80.0 and not budget.last_transaction['written']
    monkeypatch.setattr(B, '_resource_splice', original_splice)
    assert S.tick(budget, 0, 'example-job', 1000.0, 0) is None
    assert B.total_seconds(budget.read()) == 100.0
    assert budget.read()['jobs'][0]['wall_seconds'] == 25.0


def test_startup_hot_mutation_recovers_terminal_clock_and_refuses_admission(tmp_path, monkeypatch):
    budget, receipt, clock = completion_budget(tmp_path, monkeypatch)
    clock.write_text(json.dumps(receipt) + '\n')
    mutations = []
    with pytest.raises(RuntimeError, match='job already ended'):
        S._update_live_job(budget, 0, 'example-job', lambda job: mutations.append(job))
    assert mutations == []
    state = budget.read()
    assert not state['jobs'][0]['running'] and B.total_seconds(state) == 100.0
    assert state['jobs'][0]['wall_seconds'] == 25.0


def test_changed_authoritative_reserve_policy_is_refreshed_and_never_reverted_by_hot_write(tmp_path):
    budget = B.Budget(tmp_path / 'budget.json')
    before = history_ledger(budget, days=2, closed_jobs=1)
    budget.resource_read()
    peer = B.Budget(budget.path)
    source = {'bound_sha256': '9' * 64}
    assert peer.record_charge('new-authorized-reserve', 3.0, 'reserved', source, reserve_status='authorized')
    changed = peer.read()
    assert changed['reserves'] != before['reserves']
    assert budget.resource_read()['reserves'] == changed['reserves']
    budget.resource_update(lambda fresh: B.add_seconds(fresh, 7.0))
    after = budget.read()
    expected = copy.deepcopy(changed)
    B.add_seconds(expected, 7.0)
    assert after == expected
    assert after['reserves'] == changed['reserves']
    assert after['charges'] == changed['charges']


def reserved_start_job():
    return {'job_id': 'single-start', 'job_index': 0, 'running': True, 'phase': 'reserved',
            'request_sha256': 'a' * 64, 'started_epoch': 100.0, 'workers': 1,
            'monitor_identity': {'pid': 10, 'create_time': 1.0},
            'supervisor_identity': None, 'child_identity': None, 'child_pid': None,
            'charged_wall_seconds': 0.0, 'live_rss_bytes': 0,
            'supervision_policy': S.SUPERVISION_POLICY}


@pytest.mark.parametrize('launcher_prebound', [False, True])
def test_supervisor_reserved_start_consumed_once_with_none_or_exact_launcher_identity(launcher_prebound):
    job = reserved_start_job()
    own = {'pid': 11, 'create_time': 2.0}
    if launcher_prebound:
        job.update(supervisor_identity=copy.deepcopy(own), supervisor_pid=own['pid'])
    before = copy.deepcopy(job)
    S._bind_supervisor_start(job, 'a' * 64, own, 1000.0)
    expected = {**before, 'supervisor_identity': own, 'supervisor_pid': 11, 'phase': 'starting',
                'accounting_began_monotonic': 1000.0}
    assert job == expected
    original = copy.deepcopy(job)
    with pytest.raises(RuntimeError, match='startup already consumed'):
        S._bind_supervisor_start(job, 'a' * 64, own, 2000.0)
    assert job == original


@pytest.mark.parametrize('field,value,match', [
    ('supervisor_identity', {'pid': 99, 'create_time': 2.0}, 'startup identity changed'),
    ('supervisor_identity', {'pid': 11, 'create_time': 99.0}, 'startup identity changed'),
    ('supervisor_pid', 99, 'startup identity changed'),
    ('phase', 'starting', 'startup already consumed'),
    ('phase', 'supervising', 'startup already consumed'),
    ('phase', 'closing', 'startup already consumed'),
    ('phase', None, 'startup already consumed'),
    ('accounting_began_monotonic', 1000.0, 'startup already consumed'),
    ('accounting_began_monotonic', None, 'startup already consumed'),
    ('child_identity', {'pid': 12, 'create_time': 3.0}, 'startup already consumed'),
    ('child_pid', 12, 'startup already consumed'),
    ('request_sha256', 'b' * 64, 'request does not bind'),
    ('running', False, 'request does not bind'),
])
def test_supervisor_start_guard_refuses_binding_substitution_before_any_mutation(field, value, match):
    job = reserved_start_job()
    job[field] = value
    before = copy.deepcopy(job)
    with pytest.raises(RuntimeError, match=match):
        S._bind_supervisor_start(job, 'a' * 64, {'pid': 11, 'create_time': 2.0}, 2000.0)
    assert job == before


@pytest.mark.parametrize('own,began', [
    (None, 1000.0), ({'pid': 11}, 1000.0),
    ({'pid': True, 'create_time': 2.0}, 1000.0),
    ({'pid': 11, 'create_time': None}, 1000.0),
    ({'pid': 11, 'create_time': 2.0}, float('nan')),
])
def test_supervisor_start_guard_requires_evidenced_pid_create_time_and_origin(own, began):
    job = reserved_start_job()
    before = copy.deepcopy(job)
    with pytest.raises(RuntimeError, match='startup identity or elapsed origin is not evidenced'):
        S._bind_supervisor_start(job, 'a' * 64, own, began)
    assert job == before


def test_duplicate_live_request_refuses_before_spawn_and_preserves_original_clock_and_receipt(tmp_path):
    root = Path(__file__).resolve().parents[1]
    ready = tmp_path / 'original-worker.ready'
    release = tmp_path / 'original-worker.release'
    rejected = tmp_path / 'replay.rejected.json'
    worker = (
        'import time; from pathlib import Path; '
        f'Path({str(ready)!r}).write_text("ready"); release=Path({str(release)!r}); '
        'deadline=time.monotonic()+30\n'
        'while not release.exists() and time.monotonic()<deadline: time.sleep(0.025)\n'
        'assert release.exists()\n')
    with real_monitor(tmp_path, [sys.executable, '-B', '-c', worker], workers=1) as (process, budget):
        wait_until(ready.exists, timeout=12)
        original_job = budget.resource_read()['jobs'][-1]
        assert original_job['phase'] == 'supervising'
        assert all(S.freshness_reason(original_job, role) is None for role in ('supervisor', 'watchdog'))
        original_clock = Path(original_job['completion_clock'])
        assert not original_clock.exists()
        replay_code = (
            'import copy, hashlib, json, sys; from pathlib import Path; '
            'from cp26 import supervisor as S; '
            f'ledger=Path({str(budget.path)!r}); rejected=Path({str(rejected)!r}); '
            f'clock=Path({str(original_clock)!r}); '
            'original=S._bind_supervisor_start; spawns=[]\n'
            'def bind(job, *args):\n'
            '    before=copy.deepcopy(job); raw=ledger.read_bytes(); existed=clock.exists()\n'
            '    try:\n'
            '        return original(job, *args)\n'
            '    except RuntimeError:\n'
            '        rejected.write_text(json.dumps({"before":before,"after":job,'
            '"ledger_bytes_unchanged":raw==ledger.read_bytes(),'
            '"ledger_sha256":hashlib.sha256(raw).hexdigest(),'
            '"clock_existed_before":existed,"clock_exists_after":clock.exists(),'
            '"spawn_attempts":len(spawns)},sort_keys=True,allow_nan=False))\n'
            '        raise\n'
            'def spawn(*args, **kwargs):\n'
            '    spawns.append(1)\n'
            '    raise AssertionError("duplicate supervisor tried to spawn")\n'
            'S._bind_supervisor_start=bind; S.subprocess.Popen=spawn\n'
            'raise SystemExit(S.run(Path(sys.argv[1])))\n')
        replay_env = os.environ.copy()
        replay_env.update(CP26_PROJECT_ROOT=str(tmp_path), CP26_LEDGER=str(budget.path),
                          PYTHONPATH=str(root / 'src'), PYTHONDONTWRITEBYTECODE='1')
        replay = subprocess.Popen([sys.executable, '-B', '-c', replay_code, original_job['request']],
                                  cwd=root, env=replay_env, stdin=subprocess.DEVNULL,
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                  start_new_session=True)
        try:
            stdout, stderr = replay.communicate(timeout=8)
            assert replay.returncode != 0, (stdout, stderr)
            assert 'startup identity changed; refuse duplicate launch' in stderr
            observation = json.loads(rejected.read_text())
            assert observation['before'] == observation['after']
            assert observation['ledger_bytes_unchanged'] and observation['spawn_attempts'] == 0
            assert not observation['clock_existed_before'] and not observation['clock_exists_after']
            frozen = observation['before']
            for field in ('job_id', 'job_index', 'request_sha256', 'started_epoch', 'workers',
                          'supervisor_identity', 'supervisor_pid', 'watchdog_identity', 'child_identity',
                          'child_pid', 'worker_pgid', 'accounting_began_monotonic', 'phase'):
                assert frozen[field] == original_job[field]
            assert frozen['worker_identities'] == original_job['worker_identities']
            sample_now = max(frozen['accounting_observed_monotonic'],
                             frozen['supervisor_observed_monotonic'], frozen['watchdog_observed_monotonic'])
            assert all(S.freshness_reason(frozen, role, now=sample_now) is None
                       for role in ('supervisor', 'watchdog'))
            # Samples may advance legitimately around the replay, but the locked
            # rejected callback leaves their exact counters/charge bytes intact.
            continued = wait_until(lambda: (
                job if (job := budget.resource_read()['jobs'][-1])['supervisor_sample_sequence']
                > frozen['supervisor_sample_sequence'] and job['watchdog_sample_sequence']
                > frozen['watchdog_sample_sequence'] else None), timeout=5)
            assert continued['supervisor_identity'] == original_job['supervisor_identity']
            assert continued['accounting_began_monotonic'] == original_job['accounting_began_monotonic']
            assert not original_clock.exists()
            release.write_text('finish')
            stdout, stderr = process.communicate(timeout=15)
            assert process.returncode == 0, (stdout, stderr)
            finished = budget.resource_read()['jobs'][-1]
            receipt_raw = original_clock.read_bytes()
            receipt = json.loads(receipt_raw)
            assert not finished['running'] and not finished['abort_reason'] and finished['exit_code'] == 0
            assert finished['accounting_began_monotonic'] == original_job['accounting_began_monotonic']
            for field in ('supervisor_identity', 'watchdog_identity', 'child_identity', 'request_sha256',
                          'started_epoch', 'workers'):
                assert receipt[field] == original_job[field] == finished[field]
            assert receipt['completion_issuer'] == 'supervisor'
            assert receipt['completion_issuer_identity'] == original_job['supervisor_identity']
            assert receipt['workers_stopped'] and receipt['group_empty']
            assert finished['charged_wall_seconds'] == finished['wall_seconds'] == receipt['wall_seconds']
            assert B.total_seconds(budget.read()) == pytest.approx(receipt['wall_seconds'])
            state = budget.read()
            S.apply_completion(state, state['jobs'][-1], receipt)
            assert B.total_seconds(state) == pytest.approx(receipt['wall_seconds'])
            assert original_clock.read_bytes() == receipt_raw
        finally:
            # Only the direct duplicate test process can be signaled here.
            if replay.poll() is None:
                replay.kill()
                replay.wait(timeout=5)


def rich_closed_ledger(budget, *, days=2441, closed_jobs=160):
    """Actual terminal-job field shapes, including both observers' rich telemetry."""
    history_ledger(budget, days=days, closed_jobs=closed_jobs)
    with budget.transaction() as state:
        for index, job in enumerate(state['jobs']):
            monitor = {'pid': 2_000_000 + index * 3, 'create_time': 1000.0 + index * 30}
            supervisor = {'pid': monitor['pid'] + 1, 'create_time': monitor['create_time'] + 0.1}
            watchdog = {'pid': monitor['pid'] + 2, 'create_time': monitor['create_time'] + 0.2}
            observed = 500.0 + index + job['wall_seconds']
            job.update(phase='closing', monitor_identity=monitor, monitor_pid=monitor['pid'],
                       monitor_create_time=monitor['create_time'], supervisor_identity=supervisor,
                       supervisor_pid=supervisor['pid'], watchdog_identity=watchdog,
                       watchdog_pid=watchdog['pid'], child_identity=job['worker_identities'][0],
                       child_pid=job['worker_identities'][0]['pid'],
                       worker_pgid=job['worker_identities'][0]['pid'],
                       registered_worker_identities=copy.deepcopy(job['worker_identities']),
                       denied_worker_identities=[], supervision_policy=copy.deepcopy(S.SUPERVISION_POLICY),
                       request=f'closed-{index}.request.json', progress_clock=f'closed-{index}.progress.json',
                       completion_clock=f'closed-{index}.clock.json', completion_schema='cp26-completion-v2',
                       accounting_began_monotonic=500.0 + index,
                       accounting_observed_monotonic=observed, accounting_sample_sequence=20 + index,
                       cold_ledger_probe={'quoted': '"jobs":[{"running":true}],"caps":{"workers":99}',
                                          'history': [{'sha256': f'{index:064x}', 'values': [None, False, 1.25]}]})
            for role in ('supervisor', 'watchdog'):
                job.update({f'{role}_observed_monotonic': observed,
                            f'{role}_heartbeat_epoch': 1000.0 + index,
                            f'{role}_sample_wall_seconds': job['wall_seconds'],
                            f'{role}_sample_child_identity': copy.deepcopy(job['child_identity']),
                            f'{role}_sample_sequence': 10 + index,
                            f'{role}_ledger_lock_telemetry': {
                                'wait_seconds': 0.002, 'hold_seconds': 0.003, 'total_seconds': 0.006,
                                'acquired': True, 'written': True, 'read_bytes': 850_000,
                                'written_bytes': 850_000, 'canonical_input': True, 'outcome': 'committed',
                                'attempts': 1, 'conflicts': 0, 'body_seconds': 0.0002,
                                'serialized_fallback': False, 'transactions': 10 + index, 'timeouts': 0,
                                'peak_wait_seconds': 0.004, 'peak_hold_seconds': 0.005}})
    return budget.read()


def append_synthetic_live_job(budget, *, name='synthetic-live'):
    index = len(budget.resource_read()['jobs'])
    job = {'name': name, 'job_id': f'live-{index}', 'job_index': index, 'running': True,
           'phase': 'reserved', 'workers': 1, 'started_epoch': 100.0,
           'request_sha256': f'{index:064x}', 'charged_wall_seconds': 0.0, 'live_rss_bytes': 0,
           'monitor_identity': {'pid': 3_000_000 + index, 'create_time': 2000.0},
           'supervisor_identity': None, 'child_identity': None, 'child_pid': None,
           'accounting_began_monotonic': 100.0}
    budget.resource_update(lambda state: state['jobs'].append(copy.deepcopy(job)))
    return index, job


@pytest.mark.parametrize('pretty', [False, True])
def test_closed_job_spans_are_never_decoded_or_encoded_on_hot_samples(tmp_path, monkeypatch, pretty):
    budget = B.Budget(tmp_path / 'budget.json')
    before = rich_closed_ledger(budget, days=7)
    index, _ = append_synthetic_live_job(budget)
    if pretty:
        budget.path.write_text(json.dumps(budget.read(), indent=2, ensure_ascii=False) + '\n')
    view = budget.resource_read()
    assert isinstance(view['jobs'], list) and view['jobs'][:index] == before['jobs']
    spans = budget._resource_spans
    closed_bytes = [entry[1] for entry in spans[3][0][:index]]
    original_decoder = B._RESOURCE_DECODER
    original_dumps = B.json.dumps

    class Decoder:
        def raw_decode(self, text, offset=0):
            value, end = original_decoder.raw_decode(text, offset)
            assert not (isinstance(value, dict) and 'cold_ledger_probe' in value)
            return value, end
    def encode(value, *args, **kwargs):
        if isinstance(value, dict):
            assert 'cold_ledger_probe' not in value
            assert 'jobs' not in value or not any('cold_ledger_probe' in job for job in value['jobs'])
        return original_dumps(value, *args, **kwargs)
    monkeypatch.setattr(B, '_RESOURCE_DECODER', Decoder())
    monkeypatch.setattr(B.json, 'dumps', encode)
    monkeypatch.setattr(B, '_resource_layout', lambda _: pytest.fail('unchanged job/cold spans require no full parse'))
    for count in range(4):
        S.tick(budget, index, f'live-{index}', float(count + 1), 5, sample_role='supervisor')
        assert budget.resource_read()['jobs'][index]['supervisor_sample_sequence'] == count + 1
    after = budget.read()
    assert after['jobs'][:index] == before['jobs']
    assert all(raw in budget.path.read_text() for raw in closed_bytes)
    assert B.total_seconds(after) == pytest.approx(B.total_seconds(before) + 4.0)
    assert B._resource_match(budget.path.read_bytes(), spans) == budget.resource_read()


@pytest.mark.parametrize('mutation', ['top', 'nested_map', 'nested_list', 'builtin_dict', 'builtin_list',
                                      'replace', 'remove', 'reorder', 'active_binding'])
def test_closed_job_cache_is_deeply_immutable_and_rejects_history_mutation_before_commit(tmp_path, mutation):
    budget = B.Budget(tmp_path / 'budget.json')
    before = rich_closed_ledger(budget, days=3, closed_jobs=3)
    index, _ = append_synthetic_live_job(budget)
    view = budget.resource_read()
    raw = budget.path.read_bytes()
    def prohibited(state):
        B.add_seconds(state, 7.0)
        jobs = state['jobs']
        if mutation == 'top':
            jobs[0]['wall_seconds'] = 0.0
        elif mutation == 'nested_map':
            jobs[0]['supervisor_ledger_lock_telemetry']['transactions'] = 0
        elif mutation == 'nested_list':
            jobs[0]['worker_identities'].append({'pid': 1, 'create_time': 0.0})
        elif mutation == 'builtin_dict':
            dict.__setitem__(jobs[0], 'wall_seconds', 0.0)
        elif mutation == 'builtin_list':
            list.__setitem__(jobs[0]['worker_identities'], 0, {})
        elif mutation == 'replace':
            jobs[0] = copy.deepcopy(before['jobs'][0])
        elif mutation == 'remove':
            jobs.pop(0)
        elif mutation == 'reorder':
            jobs[0], jobs[1] = jobs[1], jobs[0]
        else:
            jobs[index]['request_sha256'] = '0' * 64
    with pytest.raises((ValueError, TypeError, AttributeError)):
        budget.resource_update(prohibited)
    assert budget.path.read_bytes() == raw and not budget.last_transaction['written']
    assert budget.resource_read()['jobs'][:index] == before['jobs'] == view['jobs'][:index]


@pytest.mark.parametrize('change', ['closed_field', 'closed_running', 'append', 'reorder', 'nonfinite', 'malformed'])
def test_changed_authoritative_job_items_invalidate_span_cache_and_refresh_outside_lock(tmp_path, monkeypatch, change):
    budget = B.Budget(tmp_path / 'budget.json')
    rich_closed_ledger(budget, days=3, closed_jobs=3)
    budget.resource_read()
    state = budget.read()
    if change == 'closed_field':
        state['jobs'][0]['cold_ledger_probe']['history'][0]['values'].append('new')
    elif change == 'closed_running':
        state['jobs'][0]['running'] = True
    elif change == 'append':
        job = copy.deepcopy(state['jobs'][0])
        job.update(job_id='new-job', job_index=3, running=True)
        state['jobs'].append(job)
    elif change == 'reorder':
        state['jobs'][0], state['jobs'][1] = state['jobs'][1], state['jobs'][0]
    elif change == 'nonfinite':
        state['jobs'][0]['cold_ledger_probe']['value'] = float('nan')
    raw = (json.dumps(state, indent=2) + '\n').encode()
    if change == 'malformed':
        raw = raw.replace(b'"cold_ledger_probe":', b'"cold_ledger_probe"=', 1)
    budget.path.write_bytes(raw)
    install_matching_cache(budget, raw)
    original = B._resource_layout
    original_flock = B.fcntl.flock
    refreshed = []
    def parse(value):
        with budget.path.with_suffix('.lock').open('a') as probe:
            original_flock(probe, B.fcntl.LOCK_EX | B.fcntl.LOCK_NB)
        refreshed.append(value)
        return original(value)
    monkeypatch.setattr(B, '_resource_layout', parse)
    if change in ('nonfinite', 'malformed'):
        with pytest.raises(ValueError):
            budget.resource_read()
    else:
        assert budget.resource_read()['jobs'] == state['jobs']
        budget.resource_update(lambda fresh: fresh['counts'].update(job_refresh=1))
        assert budget.read()['jobs'] == state['jobs']
    assert refreshed == [raw]


def test_active_job_becomes_cached_closed_after_receipt_and_replay_is_read_only(tmp_path, monkeypatch):
    budget, receipt, clock = completion_budget(tmp_path, monkeypatch)
    budget.resource_read()
    assert isinstance(budget.resource_read()['jobs'][0], dict)
    clock.write_text(json.dumps(receipt) + '\n')
    S.tick(budget, 0, 'example-job', 1000.0, 0)
    closed = budget.resource_read()['jobs'][0]
    assert not closed['running'] and not isinstance(closed, dict)
    raw = budget.path.read_bytes()
    assert S.tick(budget, 0, 'example-job', 2000.0, 0) is None
    assert budget.path.read_bytes() == raw and B.total_seconds(budget.read()) == 100.0
    with pytest.raises(TypeError):
        closed['running'] = True


def execution_pair(task_id='task/new', *, evidence=None, counts=None):
    proposed = {'id': task_id, 'evidence': evidence if evidence is not None else {'sha256': '9' * 64},
                'counts': counts if counts is not None else {'new_terminal_tasks': 1}}
    event = {'event': 'cp26_execution_task_terminal', 'task_id': task_id,
             'evidence_sha256': B._execution_evidence_sha256(proposed['evidence'])}
    return proposed, event


@pytest.mark.parametrize('pretty', [False, True])
@pytest.mark.parametrize('missing', ['none', 'tasks', 'both'])
def test_execution_append_preserves_history_and_exact_once_counts_without_duration(tmp_path, pretty, missing):
    budget = B.Budget(tmp_path / 'budget.json')
    before = rich_closed_ledger(budget, days=7, closed_jobs=3)
    if missing != 'none':
        del before['execution_tasks']
    if missing == 'both':
        del before['events']
    budget.path.write_text(json.dumps(before, indent=2 if pretty else None, ensure_ascii=False) + '\n')
    proposed, event = execution_pair(evidence={'quoted': 'היסטוריה "]},"jobs":[]', 'nested': [None, False, 2.5]})
    assert budget.append_execution_task(proposed, event)
    expected = copy.deepcopy(before)
    expected.setdefault('execution_tasks', []).append(proposed)
    expected.setdefault('events', []).append(event)
    expected['counts']['new_terminal_tasks'] = 1
    assert budget.read() == expected and B.total_seconds(expected) == B.total_seconds(before)
    raw = budget.path.read_bytes()
    stat = budget.path.stat()
    assert not budget.append_execution_task(proposed, event)
    assert budget.path.read_bytes() == raw
    assert (budget.path.stat().st_ino, budget.path.stat().st_mtime_ns) == (stat.st_ino, stat.st_mtime_ns)
    assert len([row for row in budget.read()['execution_tasks'] if row['id'] == proposed['id']]) == 1


@pytest.mark.parametrize('peer_mode', ['distinct', 'duplicate', 'conflict'])
def test_peer_cold_append_merges_fresh_accounting_and_deduplicates_under_same_lock(tmp_path, monkeypatch, peer_mode):
    budget = B.Budget(tmp_path / 'budget.json')
    before = rich_closed_ledger(budget, days=7, closed_jobs=3)
    index, _ = append_synthetic_live_job(budget)
    budget.resource_read()
    peer = B.Budget(budget.path)
    proposed, event = execution_pair('task/target')
    other, other_event = execution_pair(
        'task/peer' if peer_mode == 'distinct' else 'task/target',
        evidence={'sha256': '8' * 64} if peer_mode == 'conflict' else proposed['evidence'])
    original_flock = B.fcntl.flock
    injected = []
    injecting = False
    def flock(lock, operation):
        nonlocal injecting
        if operation == (B.fcntl.LOCK_EX | B.fcntl.LOCK_NB) and not injecting and not injected:
            injecting = True
            try:
                S.tick(peer, index, f'live-{index}', 7.0, 5, sample_role='watchdog')
                assert peer.append_execution_task(other, other_event)
                injected.append(1)
            finally:
                injecting = False
        return original_flock(lock, operation)
    monkeypatch.setattr(B.fcntl, 'flock', flock)
    if peer_mode == 'conflict':
        with pytest.raises(ValueError, match='identity was reused with different evidence'):
            budget.append_execution_task(proposed, event)
    else:
        assert budget.append_execution_task(proposed, event) is (peer_mode == 'distinct')
    after = budget.read()
    assert injected == [1]
    assert B.total_seconds(after) == pytest.approx(B.total_seconds(before) + 7.0)
    assert after['jobs'][index]['charged_wall_seconds'] == 7.0
    assert after['jobs'][:index] == before['jobs']
    expected_records = [other, proposed] if peer_mode == 'distinct' else [other]
    expected_events = [other_event, event] if peer_mode == 'distinct' else [other_event]
    assert after['execution_tasks'] == before['execution_tasks'] + expected_records
    assert after['events'] == before['events'] + expected_events
    assert after['counts']['new_terminal_tasks'] == len(expected_records)
    assert budget.last_transaction['attempts'] == 2 and budget.last_transaction['conflicts'] == 1


def test_execution_append_never_full_serializes_cold_arrays_while_holding_lock(tmp_path, monkeypatch):
    budget = B.Budget(tmp_path / 'budget.json')
    rich_closed_ledger(budget, days=30)
    budget.resource_read()
    original_dumps = B.json.dumps
    original_flock = B.fcntl.flock
    held_encodings = []
    def encode(value, *args, **kwargs):
        with budget.path.with_suffix('.lock').open('a') as probe:
            try:
                original_flock(probe, B.fcntl.LOCK_EX | B.fcntl.LOCK_NB)
            except BlockingIOError:
                held_encodings.append(value)
                if isinstance(value, dict):
                    assert 'execution_tasks' not in value and 'events' not in value
                    assert 'cold_ledger_probe' not in value
        return original_dumps(value, *args, **kwargs)
    monkeypatch.setattr(B.json, 'dumps', encode)
    proposed, event = execution_pair()
    assert budget.append_execution_task(proposed, event)
    assert held_encodings
    assert budget.read()['execution_tasks'][-1] == proposed


def test_execution_append_crash_after_ledger_rename_recovers_without_double_counts_or_event(tmp_path, monkeypatch):
    budget = B.Budget(tmp_path / 'budget.json')
    before = rich_closed_ledger(budget, days=7, closed_jobs=3)
    proposed, event = execution_pair()
    original_atomic = B.atomic
    attempts = []
    def crash(path, value):
        if path == B._format_path(budget.path) and not attempts:
            attempts.append(1)
            raise RuntimeError('simulated append writer death after ledger rename')
        return original_atomic(path, value)
    monkeypatch.setattr(B, 'atomic', crash)
    with pytest.raises(RuntimeError, match='simulated append writer death'):
        budget.append_execution_task(proposed, event)
    committed = budget.path.read_bytes()
    restarted = B.Budget(budget.path)
    assert not restarted.append_execution_task(proposed, event)
    assert budget.path.read_bytes() == committed
    after = budget.read()
    assert after['execution_tasks'] == before['execution_tasks'] + [proposed]
    assert after['events'] == before['events'] + [event]
    assert after['counts']['new_terminal_tasks'] == 1
    assert B.total_seconds(after) == B.total_seconds(before)


@pytest.mark.parametrize('violation', ['negative', 'bool', 'machine_duration', 'event_id', 'event_hash', 'nonfinite'])
def test_execution_append_rejects_invalid_counter_or_event_binding_without_changes(tmp_path, violation):
    budget = B.Budget(tmp_path / 'budget.json')
    rich_closed_ledger(budget, days=3, closed_jobs=3)
    proposed, event = execution_pair()
    if violation == 'negative':
        proposed['counts']['new_terminal_tasks'] = -1
    elif violation == 'bool':
        proposed['counts']['new_terminal_tasks'] = True
    elif violation == 'machine_duration':
        proposed['counts'] = {'machine_seconds': 1}
    elif violation == 'event_id':
        event['task_id'] = 'different-task'
    elif violation == 'event_hash':
        event['evidence_sha256'] = '0' * 64
    else:
        proposed['evidence']['value'] = float('nan')
    raw = budget.path.read_bytes()
    with pytest.raises(ValueError):
        budget.append_execution_task(proposed, event)
    assert budget.path.read_bytes() == raw


def test_fast_terminal_job_allows_read_only_late_launcher_binding_and_same_receipt(tmp_path):
    root = Path(__file__).resolve().parents[1]
    # Delay only the launcher's captured-identity return until the dedicated
    # unmodified supervisor/watchdog have durably completed the fast child.
    marker = tmp_path / 'late-binding-observed-closed.json'
    launcher_patch = (
        'import importlib.util, json, sys, time; from pathlib import Path; '
        f'spec=importlib.util.spec_from_file_location("driver",{str(root / "scripts/cp26_rebaseline.py")!r}); '
        'driver=importlib.util.module_from_spec(spec); spec.loader.exec_module(driver); '
        f'marker=Path({str(marker)!r}); original=driver.process_identity\n'
        'def identity(pid=None):\n'
        '    captured=original(pid)\n'
        '    if pid is not None:\n'
        '        budget=driver.Budget(); deadline=time.monotonic()+10\n'
        '        while time.monotonic()<deadline:\n'
        '            job=budget.resource_read()["jobs"][-1]\n'
        '            if not job["running"]:\n'
        '                marker.write_text(json.dumps({"closed":True,"identity_matches":job["supervisor_identity"]==captured}))\n'
        '                break\n'
        '            time.sleep(0.025)\n'
        '        else: raise AssertionError("dedicated fast job did not finish before late bind")\n'
        '    return captured\n'
        'driver.process_identity=identity\n'
        'raise SystemExit(driver.monitor(driver.argparse.Namespace('
        'name="late-bind",workers=1,log=None,command=[sys.executable,"-B","-c","pass"])))\n')
    budget = B.Budget(tmp_path / '.local/artifacts/cp-26/ledger/budget.json')
    budget.initialise()
    child_env = os.environ.copy()
    child_env.update(CP26_PROJECT_ROOT=str(tmp_path), CP26_LEDGER=str(budget.path),
                     PYTHONPATH=str(root / 'src'), PYTHONDONTWRITEBYTECODE='1')
    launcher = subprocess.Popen([sys.executable, '-B', '-c', launcher_patch], cwd=root, env=child_env,
                                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)
    try:
        stdout, stderr = launcher.communicate(timeout=15)
        assert launcher.returncode == 0, (stdout, stderr)
        assert json.loads(marker.read_text()) == {'closed': True, 'identity_matches': True}
        closed = budget.resource_read()['jobs'][-1]
        assert not closed['running'] and closed['exit_code'] == 0 and not closed['abort_reason']
        receipt = json.loads(Path(closed['completion_clock']).read_bytes())
        assert receipt['supervisor_identity'] == closed['supervisor_identity']
        assert receipt['child_identity'] == closed['child_identity']
        assert receipt['workers_stopped'] and receipt['group_empty']
        assert closed['charged_wall_seconds'] == closed['wall_seconds'] == receipt['wall_seconds']
        assert B.total_seconds(budget.read()) == pytest.approx(receipt['wall_seconds'])
    finally:
        for job in budget.read()['jobs']:
            for identity in (job.get('child_identity'), job.get('supervisor_identity'), job.get('watchdog_identity')):
                S.signal_identity(identity, signal.SIGKILL)
        if launcher.poll() is None:
            launcher.kill()
            launcher.wait(timeout=5)


def test_closed_nested_sequences_have_consistent_json_list_equality_and_inequality(tmp_path):
    budget = B.Budget(tmp_path / 'budget.json')
    before = rich_closed_ledger(budget, days=3, closed_jobs=3)
    first = budget.resource_read()['jobs'][0]
    warm = budget.resource_read()['jobs'][0]
    assert first == warm == before['jobs'][0]
    assert not (first != before['jobs'][0])
    for actual, expected in [
        (first['worker_identities'], before['jobs'][0]['worker_identities']),
        (first['cold_ledger_probe']['history'], before['jobs'][0]['cold_ledger_probe']['history']),
        (first['cold_ledger_probe']['history'][0]['values'],
         before['jobs'][0]['cold_ledger_probe']['history'][0]['values']),
    ]:
        assert actual == expected and expected == actual
        assert not (actual != expected) and not (expected != actual)
        assert actual != expected + ['different'] and not (actual == expected + ['different'])
    # The export API remains fully plain and supports normal JSON/deepcopy.
    plain = budget.read()
    assert json.loads(json.dumps(plain, allow_nan=False)) == copy.deepcopy(plain)


@contextlib.contextmanager
def arriving_admin_monitor(tmp_path, budget, command):
    root = Path(__file__).resolve().parents[1]
    child_env = os.environ.copy()
    child_env.update(CP26_PROJECT_ROOT=str(tmp_path), CP26_LEDGER=str(budget.path),
                     PYTHONPATH=str(root / 'src'), PYTHONDONTWRITEBYTECODE='1')
    launch = [sys.executable, '-B', str(root / 'scripts/cp26_rebaseline.py'),
              'monitor', '--name', 'ledger-rich-admin', '--workers', '1', '--', *command]
    process = subprocess.Popen(launch, cwd=root, env=child_env, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                               start_new_session=True)
    try:
        yield process
    finally:
        for job in budget.read()['jobs']:
            if job.get('name') != 'ledger-rich-admin':
                continue
            for identity in [job.get('child_identity'), *job.get('worker_identities', []),
                             job.get('supervisor_identity'), job.get('watchdog_identity')]:
                S.signal_identity(identity, signal.SIGKILL)
        if process.poll() is None:
            process.kill()
        process.communicate(timeout=5)


#: The rich-admin test's patience: harness waits only, never supervision policy. Under a four-burner
#: emulation of a 4-vCPU runner (three busy owners leave about one core), the controller's wait on the
#: admin monitor took up to 28.9 s (a fresh environment's first run; 22.0 s once warm) and each owner
#: needed up to 29.5 s from `ready` to `stop`; the old 15 s wait timed out every time
#: (docs/track-b/evidence/cp-26/landing-repair-2/patience-measurement.json). The bounds allow a runner
#: core 4x slower than this machine's, times 1.3 for variance: 28.9 * 4 * 1.3 = 150 -> 160 s.
RICH_ADMIN_READY_SECONDS = 20
RICH_ADMIN_WAIT_SECONDS = 160
#: Each owner's self-deadline starts when it writes `ready`, so it outlasts the controller's wait for
#: all owners, its wait on the admin, and the checks before `stop` (measured 3.2 s; 20 s allowed).
RICH_ADMIN_OWNER_DEADLINE_SECONDS = RICH_ADMIN_READY_SECONDS + RICH_ADMIN_WAIT_SECONDS + 20


def test_rich_closed_jobs_three_busy_owners_accept_fourth_admin_with_full_future_history(tmp_path):
    """Four compute slots; controller blocks during the four-inner-job overlap."""
    budget = B.Budget(tmp_path / '.local/artifacts/cp-26/ledger/budget.json')
    before = rich_closed_ledger(budget)
    assert len(before['jobs']) == 160
    assert len(before['execution_tasks']) == 2441 * 2 + ((2441 + 27) // 28) * 3
    assert all('supervisor_ledger_lock_telemetry' in job and 'watchdog_ledger_lock_telemetry' in job
               for job in before['jobs'])
    assert S.SUPERVISION_POLICY == CALIBRATED_POLICY == calibrated_policy_record()
    assert B.CAPS == {'machine_seconds': 500 * 3600, 'workers': 4, 'rss_bytes': 12 * 10**9,
                      'data_download_bytes': 0, 'remote_writes': 0, 'cost_usd': 0,
                      'gpu_jobs': 0, 'cloud_jobs': 0}
    busy = tmp_path / 'owners.busy'
    stop = tmp_path / 'owners.stop'
    admin_report = tmp_path / 'admin.report.json'
    ready = [tmp_path / f'busy-owner-{index}.ready' for index in range(3)]
    commands = []
    for marker in ready:
        worker = (
            'import time; from pathlib import Path; '
            f'Path({str(marker)!r}).write_text("ready"); busy=Path({str(busy)!r}); stop=Path({str(stop)!r}); '
            f'deadline=time.monotonic()+{RICH_ADMIN_OWNER_DEADLINE_SECONDS}\n'
            'while not busy.exists() and time.monotonic()<deadline: time.sleep(0.025)\n'
            'assert busy.exists(); value=1\n'
            'while not stop.exists() and time.monotonic()<deadline:\n'
            '    for index in range(20000): value=(value*17+index)%10000019\n'
            'assert stop.exists()\n')
        commands.append([sys.executable, '-B', '-c', worker])
    admin = (
        'import json, os, time; from pathlib import Path; '
        'from cp26.budget import Budget, _execution_evidence_sha256; from cp26 import supervisor as S; '
        f'budget=Budget({str(budget.path)!r}); report=Path({str(admin_report)!r}); observations=[]\n'
        'proposed={"id":"arrival/admin-terminal","evidence":{"synthetic":True,"basis":"fourth-owner admin arrival"},'
        '"counts":{"admin_terminal_tasks":1}}\n'
        'event={"event":"cp26_execution_task_terminal","task_id":proposed["id"],'
        '"evidence_sha256":_execution_evidence_sha256(proposed["evidence"])}\n'
        'assert budget.append_execution_task(proposed,event)\n'
        'deadline=time.monotonic()+2.0\n'
        'while time.monotonic()<deadline:\n'
        '    budget.count(ddnn2_search_fits=1); budget.count(ddnn2_epochs=2)\n'
        '    state=budget.resource_read(); now=time.monotonic()\n'
        '    owners=[job for job in state["jobs"] if job.get("name") in '
        '("ledger-liveness-0","ledger-liveness-1","ledger-liveness-2")]\n'
        '    assert len(owners)==3 and all(job["running"] for job in owners)\n'
        '    assert sum(job["workers"] for job in state["jobs"] if job["running"])==4\n'
        '    sample=[]\n'
        '    for job in owners:\n'
        '        for role in ("supervisor","watchdog"):\n'
        '            assert S.freshness_reason(job,role,now=now) is None\n'
        '            telemetry=job[role+"_ledger_lock_telemetry"]\n'
        # 1c89354 used the then-current 0.5 s ledger timeout; r15's calibration
        # (a57aba5) raised it to 3.0 s. Match the controller's calibrated bound.
        '            assert telemetry["timeouts"]==0 and telemetry["peak_hold_seconds"]<S.LEDGER_TIMEOUT_SECONDS\n'
        '            assert telemetry["peak_wait_seconds"]<S.LEDGER_TIMEOUT_SECONDS\n'
        '            sample.append({"job_id":job["job_id"],"role":role,'
        '"sequence":job[role+"_sample_sequence"]})\n'
        '    observations.append(sample); time.sleep(S.POLL_SECONDS)\n'
        'assert len(observations)>=3\n'
        'budget.event("ddnn2_search_terminal",synthetic=True,observations=len(observations))\n'
        'report.write_text(json.dumps({"observations":observations,"private_peak_workers":state["peaks"]["workers"]},'
        'sort_keys=True,allow_nan=False))\n')
    with three_real_monitors(tmp_path, budget, commands) as owners:
        wait_until(lambda: all(marker.exists() for marker in ready), timeout=RICH_ADMIN_READY_SECONDS)
        original_jobs = budget.resource_read()['jobs'][len(before['jobs']):]
        initial = {(job['job_id'], role): job[f'{role}_sample_sequence']
                   for job in original_jobs for role in ('supervisor', 'watchdog')}
        busy.write_text('compute')
        with arriving_admin_monitor(tmp_path, budget, [sys.executable, '-B', '-c', admin]) as process:
            # No polling, assertions, or workload on this controller while four
            # dedicated inner children may compute. communicate blocks in the OS.
            stdout, stderr = process.communicate(timeout=RICH_ADMIN_WAIT_SECONDS)
            assert process.returncode == 0, (stdout, stderr)
            evidence = json.loads(admin_report.read_text())
            assert evidence['private_peak_workers'] == 4
            assert len(evidence['observations']) >= 3
            for sample in evidence['observations']:
                assert len(sample) == 6
                assert all(row['sequence'] >= initial[row['job_id'], row['role']] for row in sample)
            active = budget.resource_read()['jobs'][len(before['jobs']):]
            admin_job = next(job for job in active if job['name'] == 'ledger-rich-admin')
            assert not admin_job['running'] and admin_job['exit_code'] == 0 and not admin_job['abort_reason']
            now = time.monotonic()
            for job in active:
                if job['name'] == 'ledger-rich-admin':
                    continue
                assert job['running']
                for role in ('supervisor', 'watchdog'):
                    assert S.freshness_reason(job, role, now=now) is None
                    assert job[f'{role}_sample_sequence'] >= initial[job['job_id'], role] + 3
                    assert_live_lock_telemetry(job[f'{role}_ledger_lock_telemetry'])
            stop.write_text('finish')
            for owner in owners:
                stdout, stderr = owner.communicate(timeout=20)
                assert owner.returncode == 0, (stdout, stderr)
        after = budget.read()
        assert_preserved_history(after, before, appended_tasks=1)
        completed = after['jobs'][len(before['jobs']):]
        assert len(completed) == 4 and all(not job['running'] for job in completed)
        assert after['counts']['admin_terminal_tasks'] == 1
        assert after['counts']['ddnn2_search_fits'] == len(evidence['observations'])
        assert after['counts']['ddnn2_epochs'] == len(evidence['observations']) * 2
        terminal_events = [event for event in after['events'] if event['event'] == 'ddnn2_search_terminal']
        assert len(terminal_events) == 1 and terminal_events[0]['observations'] == len(evidence['observations'])
        assert len([task for task in after['execution_tasks'] if task['id'] == 'arrival/admin-terminal']) == 1
        for job in completed:
            receipt = json.loads(Path(job['completion_clock']).read_bytes())
            assert receipt['workers_stopped'] and receipt['group_empty']
            assert job['charged_wall_seconds'] == job['wall_seconds'] == receipt['wall_seconds']
            assert job['exit_code'] == 0 and not job['abort_reason']
            assert_live_lock_telemetry(receipt['ledger_lock_telemetry'])
        assert B.total_seconds(after) == pytest.approx(
            B.total_seconds(before) + sum(job['wall_seconds'] * job['workers'] for job in completed))


def test_owned_execution_appends_prepare_outside_lock_and_advance_index_without_history_reparse(tmp_path, monkeypatch):
    budget = B.Budget(tmp_path / 'budget.json')
    before = rich_closed_ledger(budget, days=30, closed_jobs=3)
    first, first_event = execution_pair('task/first')
    assert budget.append_execution_task(first, first_event)
    original_prepare = B._prepare_execution_append
    original_flock = B.fcntl.flock
    preparations = []
    def outside(layout, records):
        with budget.path.with_suffix('.lock').open('a') as probe:
            original_flock(probe, B.fcntl.LOCK_EX | B.fcntl.LOCK_NB)
        preparations.append(records[0]['id'])
        return original_prepare(layout, records)
    monkeypatch.setattr(B, '_prepare_execution_append', outside)
    monkeypatch.setattr(B, '_execution_index', lambda _: pytest.fail('owned append index must advance without reparse'))
    monkeypatch.setattr(B, '_resource_layout', lambda _: pytest.fail('owned append cold bytes must match advanced layout'))
    second, second_event = execution_pair('task/second', counts={})
    assert budget.append_execution_task(second, second_event)
    assert not budget.append_execution_task(first, first_event)
    assert not budget.append_execution_task(second, second_event)
    assert preparations == ['task/second', 'task/first', 'task/second']
    after = budget.read()
    assert after['execution_tasks'] == before['execution_tasks'] + [first, second]
    assert after['events'] == before['events'] + [first_event, second_event]
    assert after['counts']['new_terminal_tasks'] == 1
    assert B.total_seconds(after) == B.total_seconds(before)


def test_count_and_terminal_event_never_decode_or_encode_closed_history_under_flock(tmp_path, monkeypatch):
    budget = B.Budget(tmp_path / 'budget.json')
    before = rich_closed_ledger(budget, days=30)
    index, _ = append_synthetic_live_job(budget)
    budget.resource_read()
    original_dumps = B.json.dumps
    original_flock = B.fcntl.flock
    original_prepare = B._prepare_cold_append
    prepared = []
    def outside(layout, items, index_update=None):
        with budget.path.with_suffix('.lock').open('a') as probe:
            original_flock(probe, B.fcntl.LOCK_EX | B.fcntl.LOCK_NB)
        prepared.append(set(items))
        return original_prepare(layout, items, index_update)
    def encode(value, *args, **kwargs):
        with budget.path.with_suffix('.lock').open('a') as probe:
            try:
                original_flock(probe, B.fcntl.LOCK_EX | B.fcntl.LOCK_NB)
            except BlockingIOError:
                if isinstance(value, dict):
                    assert 'jobs' not in value and 'events' not in value and 'execution_tasks' not in value
                    assert 'cold_ledger_probe' not in value
        return original_dumps(value, *args, **kwargs)
    monkeypatch.setattr(B.json, 'dumps', encode)
    monkeypatch.setattr(B, '_prepare_cold_append', outside)
    monkeypatch.setattr(B, '_resource_layout', lambda _: pytest.fail('count/event cannot reparse unchanged cold history'))
    budget.count(ddnn2_search_fits=1)
    S.tick(budget, index, f'live-{index}', 7.0, 5, sample_role='watchdog')
    budget.count(ddnn2_epochs=3)
    budget.event('ddnn2_search_terminal', synthetic=True, route='nominal', epochs=3)
    assert prepared == [{'events'}]
    after = budget.read()
    assert after['counts']['ddnn2_search_fits'] == 1 and after['counts']['ddnn2_epochs'] == 3
    assert B.total_seconds(after) == pytest.approx(B.total_seconds(before) + 7.0)
    assert after['jobs'][:index] == before['jobs']
    assert after['execution_tasks'] == before['execution_tasks']
    assert after['events'][:-1] == before['events']
    assert after['events'][-1]['event'] == 'ddnn2_search_terminal'
    assert after['events'][-1]['synthetic'] is True
    assert isinstance(after['events'][-1]['epoch'], float)


def test_count_refuses_duration_misuse_and_operational_errors_use_noncacheable_abort(tmp_path, monkeypatch):
    budget = B.Budget(tmp_path / 'budget.json')
    budget.initialise()
    raw = budget.path.read_bytes()
    with pytest.raises(ValueError, match='classified resource charge'):
        budget.count(machine_seconds=1)
    with pytest.raises(TypeError):
        budget.count(invalid_increment='not numeric')
    assert budget.path.read_bytes() == raw
    cause = TimeoutError('CP-26 ledger accounting lock did not progress')
    def blocked(*args, **kwargs):
        raise cause
    monkeypatch.setattr(budget, 'resource_update', blocked)
    with pytest.raises(B.AccountingAbort) as caught:
        budget.count(ddnn2_search_fits=1)
    assert caught.value.cause is cause and caught.value.__context__ is cause
    assert caught.value.__suppress_context__
    assert not isinstance(caught.value, Exception)
    assert 'TimeoutError: CP-26 ledger accounting lock did not progress' in str(caught.value)
    assert budget.path.read_bytes() == raw


@pytest.mark.parametrize('value', [float('nan'), float('inf'), -float('inf')])
def test_nonfinite_counter_argument_is_refused_before_ledger_access(tmp_path, monkeypatch, value):
    budget = B.Budget(tmp_path / 'argument-counter.json')
    budget.initialise()
    before = budget.path.read_bytes()
    def forbidden(*args, **kwargs):
        raise AssertionError('invalid argument must not access the ledger')
    monkeypatch.setattr(budget, 'resource_update', forbidden)
    with pytest.raises(ValueError, match='finite numbers'):
        budget.count(ddnn2_search_fits=value)
    assert budget.path.read_bytes() == before


@pytest.mark.parametrize('stored', ['corrupt', None, []])
def test_actual_search_corrupt_stored_counter_is_noncacheable_operational_abort(tmp_path, stored):
    from cp26 import search as Search
    from test_cp26_search import plan
    budget = B.Budget(tmp_path / 'corrupt-counter.json')
    budget.initialise()
    with budget.transaction() as state:
        state['counts']['ddnn2_search_fits'] = stored
    before = budget.path.read_bytes()
    cache = Search.TrialCache(tmp_path / 'trial-cache', plan(k=0))
    attempts = []
    def evaluate(*args):
        budget.count(ddnn2_search_fits=1)
        attempts.append('fit')
        raise AssertionError('fit must not run after counter corruption')
    with pytest.raises(B.AccountingAbort) as caught:
        Search.run_search(cache.plan, evaluate, cache=cache)
    assert not isinstance(caught.value, Exception)
    assert isinstance(caught.value.cause, ValueError)
    assert not attempts and not list(cache.root.rglob('*.json'))
    assert budget.path.read_bytes() == before


def test_actual_search_accounting_timeout_aborts_without_fit_or_failed_trial_cache(tmp_path):
    root = Path(__file__).resolve().parents[1]
    cache_root = tmp_path / 'trial-cache'
    holder_ready = tmp_path / 'counter-holder.ready'
    aborted = tmp_path / 'accounting-aborted.json'
    fit_attempt = tmp_path / 'fit-attempted'
    fault_ledger = tmp_path / 'counter-fault/budget.json'
    # The direct holder is a dedicated descendant of the search child. Both are
    # conservatively declared in its two-worker allocation; no model fit occurs.
    worker = (
        'import json, subprocess, sys, time; from pathlib import Path; '
        f'sys.path.insert(0,{str(root / "tests")!r}); '
        'from test_cp26_search import plan; from cp26 import search as Search; '
        'from cp26.budget import Budget, AccountingAbort; '
        f'cache=Search.TrialCache(Path({str(cache_root)!r}),plan(k=0)); '
        f'ready=Path({str(holder_ready)!r}); aborted=Path({str(aborted)!r}); fit=Path({str(fit_attempt)!r}); '
        f'budget=Budget(Path({str(fault_ledger)!r})); budget.initialise(); lock_path=budget.path.with_suffix(".lock")\n'
        'holder_code="import fcntl,time;from pathlib import Path;lock=Path("+repr(str(lock_path))'
        '+").open(\\"a\\");fcntl.flock(lock,fcntl.LOCK_EX);Path("+repr(str(ready))'
        '+").write_text(\\"held\\");time.sleep(30)"\n'
        'holder=subprocess.Popen([sys.executable,"-B","-c",holder_code],stdin=subprocess.DEVNULL,'
        'stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)\n'
        'deadline=time.monotonic()+5\n'
        'while not ready.exists() and time.monotonic()<deadline: time.sleep(0.025)\n'
        'assert ready.exists()\n'
        'def evaluate(*args):\n'
        '    budget.count(ddnn2_search_fits=1)\n'
        '    fit.write_text("fit attempted")\n'
        '    raise AssertionError("fit must not run after accounting failure")\n'
        'try:\n'
        '    Search.run_search(cache.plan,evaluate,cache=cache)\n'
        'except AccountingAbort as exc:\n'
        '    aborted.write_text(json.dumps({"cause_type":type(exc.cause).__name__,'
        '"noncacheable":not isinstance(exc,Exception),"cache_files":len(list(cache.root.rglob("*.json")))}))\n'
        '    raise\n'
        'finally:\n'
        '    if holder.poll() is None: holder.terminate()\n'
        '    holder.wait(timeout=5)\n')
    with real_monitor(tmp_path, [sys.executable, '-B', '-c', worker], workers=2) as (process, budget):
        stdout, stderr = process.communicate(timeout=20)
        assert process.returncode != 0, (stdout, stderr)
        evidence = json.loads(aborted.read_text())
        assert evidence == {'cause_type': 'TimeoutError', 'noncacheable': True, 'cache_files': 0}
        assert not fit_attempt.exists() and not list(cache_root.rglob('*.json'))
        state = budget.read()
        job = state['jobs'][-1]
        receipt = json.loads(Path(job['completion_clock']).read_bytes())
        assert not job['running'] and receipt['workers_stopped'] and receipt['group_empty']
        assert receipt['wall_seconds'] > 0 and receipt['exit_code'] != 0
        assert B.total_seconds(state) == pytest.approx(receipt['wall_seconds'] * 2)


def test_actual_search_numerical_solver_exception_remains_registered_failed_trial_cache(tmp_path):
    from cp26 import search as Search
    from test_cp26_search import plan
    frozen = plan(k=0)
    cache = Search.TrialCache(tmp_path / 'numerical-failure-cache', frozen)
    def evaluate(*args):
        raise ValueError('synthetic numerical solver failure; no fit')
    result = Search.run_search(frozen, evaluate, cache=cache)
    saved = json.loads(cache.path(0, 0).read_bytes())
    assert saved['status'] == 'failed' and 'ValueError: synthetic numerical solver failure' in saved['cause']
    assert result['failed_fits'] > 0 and not result['complete']
