"""Production scheduling with physical fits stubbed; no training or evaluation scores."""
from contextlib import contextmanager
from datetime import date, timedelta
import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

from cp15.data import day_hours
from cp24 import design as G
from cp26 import execution as E
from cp26 import fits as F
from cp26 import harness as H
from cp26 import members as M
from cp26 import search as S
from cp26.state import ReplayState

IDENTITY = {'documents': {'protocol': 'synthetic-frozen-r14'}, 'choices': {'calendar': 'registered'}}


class Ledger:
    def __init__(self):
        self.state = {'counts': {}, 'events': []}

    @contextmanager
    def transaction(self):
        yield self.state

    def count(self, **increments):
        for key, value in increments.items():
            self.state['counts'][key] = self.state['counts'].get(key, 0) + value

    def event(self, name, **fields):
        self.state['events'].append({'event': name, **fields})

    def read(self):
        return self.state

    def append_execution_task(self, proposed, event):
        records = self.state.setdefault('execution_tasks', [])
        previous = next((record for record in records if record['id'] == proposed['id']), None)
        if previous is not None:
            if previous != proposed:
                raise ValueError('execution task identity was reused with different evidence')
            return False
        records.append(proposed)
        self.count(**proposed['counts'])
        self.state['events'].append(event)
        return True


def table(last=date(2026, 7, 8)):
    first = date(2019, 1, 1)
    days = np.arange(np.datetime64(first), np.datetime64(last) + 1)
    return SimpleNamespace(days=days, first=first, mask=np.ones((len(days), 24), bool),
                           covered=np.ones(len(days), bool),
                           centre={'s4': np.zeros(len(days)), 'mad': np.zeros(len(days))},
                           scale={'s4': np.ones(len(days)), 'mad': np.ones(len(days))},
                           ix=lambda d: int((np.datetime64(d) - days[0]).astype(int)),
                           date_of=lambda i: first + timedelta(days=int(i)))


def search_identity(root, k, route):
    return {'protocol': S.PROTOCOL, 'k': k, 'route': route,
            'cp26_input_fingerprint': 'synthetic-inputs', 'code_sha256': {'synthetic-code': 'fixed'}}


def metric(trial, batch, config, seed):
    return {'status': 'ok', 'pinball_sum': float(trial + 1), 'pinball_count': 7,
            'abs_error_sum': float(trial + 1), 'hours': 1, 'n_inputs': 12}


@pytest.fixture
def authorized(monkeypatch):
    monkeypatch.setenv('CP26_MONITORED_JOB', 'synthetic-execution-test')
    monkeypatch.setenv('CP26_EXPERIMENT_AUTHORIZED', '1')
    for name in H.BLAS:
        monkeypatch.setenv(name, '1')
    monkeypatch.setattr(H, 'input_fingerprint', lambda root: 'synthetic-inputs')
    monkeypatch.setattr(H, 'identities', lambda root: {'reports/development-inputs/tier-register.json': 'synthetic-tier'})
    monkeypatch.setattr(S, 'search_identity', search_identity)
    monkeypatch.setattr(H, 'runtime_lineage', lambda root: {'synthetic-operational-provenance': True})
    return lambda stage: None


def test_production_search_one_prior_fit_forecasts_28_days_without_refit(tmp_path, monkeypatch, authorized):
    """Exercise execute_search and its real halving/cache engine, not a replacement evaluator."""
    import cp24.member as member
    import cp26.budget as budget_module
    dd = table()
    plan = S.make_plan(dd, 0, 'nominal', search_identity(tmp_path, 0, 'nominal'))
    plan_path = tmp_path / 'plan.json'
    S._atomic(plan_path, plan)
    budget, calls, emits = Ledger(), [], []
    monkeypatch.setattr(budget_module, 'Budget', lambda: budget)
    monkeypatch.setattr(S.subprocess, 'check_output', lambda *args, **kwargs: plan_path.read_bytes())
    keys = SimpleNamespace(of_days=lambda days: np.arange(len(days) * 24),
                           eligible=np.ones(28 * 24, bool), y=np.zeros(28 * 24))
    ctx = SimpleNamespace(dd=dd, keys=keys, data=object(), noload_active=False)
    def build(root, settings, route, *, before):
        assert before == S.search_day(0)
        return ctx
    monkeypatch.setattr(M.Context, 'build', build)
    def physical_fit(dd, origin, config, seed, forecast_days, *, exclude_uncovered, charge):
        lower, window, _ = G.window(dd, origin, exclude_uncovered=exclude_uncovered)
        assert (dd.days[window] < np.datetime64(origin)).all()
        assert origin in {date.fromisoformat(b['first']) for b in plan['support']['batches']}
        assert len(forecast_days) == 28
        assert dd.date_of(int(forecast_days[0])) == origin
        assert dd.date_of(int(forecast_days[-1])) == origin + timedelta(days=27)
        weeks, _ = G.holdout_weeks(dd, lower, origin, seed)
        charge()
        calls.append((config['id'], seed, origin, tuple(forecast_days)))
        q = np.broadcast_to(np.arange(7.), (28, 24, 7)).copy()
        return {'eur': q, 'member': {'epochs_run': 1}, 'n_inputs': 12, 'seconds': 1.,
                'maxrss_bytes': 1, 'preprocessor': {}, 'guards': {},
                'window': {'start': str(lower), 'end_exclusive': str(origin),
                           'held_out_weeks': [str(d) for d in weeks]}}
    def emit(keys, rows, days, values):
        emits.append(tuple(days))
        return values.reshape(-1, 7)[rows]
    monkeypatch.setattr(member, 'fit_member', physical_fit)
    monkeypatch.setattr(member, 'emit_rows', emit)
    result_path = tmp_path / 'result.json'
    result = S.execute_search(tmp_path, plan_path, tmp_path / 'tasks', result_path)
    assert result['complete'] and len(result['members']) == 8
    expected_fits = 128 * min(4, plan['B']) + (43 * max(0, plan['B'] - 4) if plan['B'] > 4 else 0)
    assert len(calls) == len(emits) == expected_fits
    assert len({(config, seed, origin) for config, seed, origin, _ in calls}) == expected_fits
    assert all(b['forecast_days'] == 28 and b['internal_refits'] == 0
               and b['latest_training_delivery_day'] < b['training_target_cutoff']
               for r in result['trials'] for b in r['batches'])
    assert S.execute_search(tmp_path, plan_path, tmp_path / 'tasks', result_path) == result
    assert len(calls) == expected_fits
    monkeypatch.setattr(S, 'search_identity', lambda *args: {**plan['identity'], 'code_sha256': {'changed': 'code'}})
    with pytest.raises(ValueError, match='current lineage'):
        S.execute_search(tmp_path, plan_path, tmp_path / 'tasks', result_path)
    assert len(calls) == expected_fits


class Fixture:
    def __init__(self, root, monkeypatch, through):
        self.root, self.monkeypatch, self.through = root, monkeypatch, through
        self.budget, self.calls = Ledger(), []
        monkeypatch.setattr(H, 'art', lambda: root / '.local/artifacts/cp-26')
        self.paths = E.Paths.build(root)
        dd = table()
        def prepare(root, k, route, path):
            value = S.make_plan(dd, k, route, search_identity(root, k, route))
            S._atomic(path, value)
            return value
        monkeypatch.setattr(S, 'prepare_search', prepare)
        self.manifest = E.prepare(root, IDENTITY, gate=lambda stage: None)
        for route in E.ROUTES:
            plan = json.loads(self.paths.plan(route, 0).read_text())
            S._atomic(self.paths.result(route, 0), S.run_search(plan, metric))
        index = day_hours(H.WARMUP_START)
        for day in E.calendar(H.WARMUP_START + timedelta(days=1), through):
            index = index.append(day_hours(day))
        dates = index.tz_convert('Europe/Berlin').date
        data = SimpleNamespace(index=index, dates=np.asarray(dates), y=np.full(len(index), 50.),
                               scale=np.full(len(index), 2.), eligible=np.ones(len(index), bool),
                               rows=lambda day: np.flatnonzero(np.asarray(dates) == day))
        self.contexts, self.caches = {}, {}
        for route in E.ROUTES:
            ctx = SimpleNamespace(root=root, variant=route, restore=False, data=data,
                                  settings=H.GFS6 if route == 'gfs6' else H.NEW)
            identity = {'protocol': IDENTITY, 'inputs': 'synthetic-inputs', 'code': {'stubbed-member': 'fixed'},
                        'route': route, 'settings': ctx.settings.name, 'restore': False}
            self.contexts[route] = ctx
            self.caches[route] = F.FitCache(self.paths.local / 'fits', route, identity)
        monkeypatch.setattr(F, 'frozen_fit_identity', lambda ctx, protocol: self.caches[ctx.variant].identity)
        def fit(ctx, day, members, *, ensemble=None, k=None):
            out = {}
            for name in members:
                self.calls.append((ctx.variant, day, name))
                if name == 'D2' and ensemble is None:
                    out[name] = {'status': 'failed', 'cause': 'no native D2 before S0', 'seconds': 0.}
                    continue
                central = np.full(len(data.rows(day)), 2. + list(M.FITTERS).index(name))
                result = {'status': 'ok', 'central': central, 'seconds': 1., 'fits': {'synthetic_physical': 1},
                          'lineage': {'issue_utc': H.issue_instant(day, ctx.settings).isoformat(),
                                      'training_target_cutoff': str(day)}}
                if name in ('D2', 'v1-R'):
                    result['quantiles'] = central[:, None] + np.arange(-3, 4)[None, :]
                out[name] = result
            return out
        monkeypatch.setattr(M, 'fit_members', fit)

    def run(self):
        self.monkeypatch.setattr(H, 'art', lambda: self.root / '.local/artifacts/cp-26')
        self.monkeypatch.setattr(F, 'frozen_fit_identity', lambda ctx, protocol: self.caches[ctx.variant].identity)
        return E.run_forecasts(self.root, IDENTITY, {}, gate=lambda stage: None, through=self.through,
                               budget=self.budget, contexts=self.contexts, caches=self.caches)


def test_gate_reconciles_saved_artifacts_before_repricing_without_fits(tmp_path, monkeypatch, authorized):
    from cp26 import gates
    fixture = Fixture(tmp_path, monkeypatch, date(2020, 1, 2))
    fixture.run()
    original_tasks = list(fixture.budget.state['execution_tasks'])
    # Production refreshes the durable export only at slice boundaries. A
    # crash after local state/day save leaves this older export behind.
    ReplayState(IDENTITY).save(fixture.paths.output / 'replay-state.json')
    missing_id = f'issuance/{E.digest(IDENTITY)}/2020-01-02'
    fixture.budget.state['execution_tasks'] = [r for r in original_tasks if r['id'] != missing_id]
    fixture.budget.state['counts']['completed_daily_issuances'] -= 1
    original_calls = list(fixture.calls)
    gates.reconcile_terminal_evidence(tmp_path, fixture.paths.output, IDENTITY, fixture.budget)
    assert fixture.calls == original_calls
    assert set(r['id'] for r in fixture.budget.state['execution_tasks']) == set(r['id'] for r in original_tasks) | {
        f'search/{E.digest(IDENTITY)}/{route}/0' for route in E.ROUTES}
    assert fixture.budget.state['counts']['completed_daily_issuances'] == 2
    fixture.budget.state['execution_tasks'] = [r for r in fixture.budget.state['execution_tasks'] if r['id'] != missing_id]
    value = E._read(fixture.paths.day(date(2020, 1, 2)))
    value['policies']['nominal/v2']['fallback_cause'] = 'changed original issuance'
    E._save(fixture.paths.day(date(2020, 1, 2)), E._signed({k: v for k, v in value.items() if k != 'content_sha256'}))
    with pytest.raises(RuntimeError, match='differs from saved issuance'):
        gates.reconcile_terminal_evidence(tmp_path, fixture.paths.output, IDENTITY, fixture.budget)


def test_saved_before_export_resume_equals_uninterrupted_and_never_refits(tmp_path, monkeypatch, authorized):
    through = date(2020, 2, 16)
    complete = Fixture(tmp_path / 'complete', monkeypatch, through)
    # Each fixture's physical fit stub is deliberately rebound for the run.
    complete.run()
    complete_state = ReplayState.load(complete.paths.state(IDENTITY), IDENTITY)
    expected = complete_state.to_dict()
    resumed = Fixture(tmp_path / 'resumed', monkeypatch, through)
    original = E.materialize_day
    stopped = date(2020, 1, 20)
    def interruption(paths, state, day, *args, **kwargs):
        if day == stopped:
            assert paths.state(IDENTITY).exists()
            assert ReplayState.load(paths.state(IDENTITY), IDENTITY).last_origin == stopped
            raise KeyboardInterrupt('synthetic save-before-export crash')
        return original(paths, state, day, *args, **kwargs)
    monkeypatch.setattr(E, 'materialize_day', interruption)
    with pytest.raises(KeyboardInterrupt):
        resumed.run()
    first_calls = list(resumed.calls)
    assert not resumed.paths.day(stopped).exists()
    monkeypatch.setattr(E, 'materialize_day', original)
    resumed.run()
    actual = ReplayState.load(resumed.paths.state(IDENTITY), IDENTITY)
    assert actual.to_dict() == expected
    assert len(resumed.calls) == len(set(resumed.calls))
    assert all(day > stopped for _, day, _ in resumed.calls[len(first_calls):])
    assert resumed.budget.state == complete.budget.state
    for day in E.calendar(last=through):
        assert json.loads(resumed.paths.day(day).read_text()) == json.loads(complete.paths.day(day).read_text())
    before = list(resumed.calls)
    resumed.run()
    assert resumed.calls == before
    assert actual.policies['nominal/v5'].buffer_days == 28
    assert set(actual.ledgers) == set(E.ROUTES)


def test_missing_terminal_search_stops_before_any_daily_fit(tmp_path, monkeypatch, authorized):
    fixture = Fixture(tmp_path, monkeypatch, date(2020, 1, 15))
    fixture.paths.result('gfs6', 0).unlink()
    with pytest.raises(RuntimeError, match='no terminal result'):
        fixture.run()
    assert not fixture.calls


def test_failed_daily_d2_subset_is_retained_and_never_refitted(tmp_path, monkeypatch, authorized):
    import cp24.execution as landed
    real_fit_members = M.fit_members
    fixture = Fixture(tmp_path, monkeypatch, date(2020, 1, 15))
    monkeypatch.setattr(M, 'fit_members', real_fit_members)
    ctx = fixture.contexts['nominal']
    ctx.dd, ctx.keys, ctx.noload_active = table(), object(), False
    ensemble = json.loads(fixture.paths.result('nominal', 0).read_text())
    calls = []
    def incomplete(dd, keys, data, day, members, charge, *, uncovered_fails):
        calls.append(day)
        for _ in range(7):
            charge()
        return {'members': [{} for _ in range(7)]}
    monkeypatch.setattr(landed, 'fit_origin', incomplete)
    day, cache = date(2020, 1, 15), fixture.caches['nominal']
    first = F.fit_members_cached(ctx, day, cache, ensemble=ensemble, k=0, members=('D2',))['D2']
    assert first['status'] == 'failed' and 'no subset median' in first['cause']
    second = F.fit_members_cached(ctx, day, cache, ensemble=ensemble, k=0, members=('D2',))['D2']
    assert second == first and calls == [day]
    wrong = {**ensemble, 'identity': {**ensemble['identity'], 'code_sha256': {'stale': 'code'}}}
    wrong['content_sha256'] = S.digest(wrong)
    with pytest.raises(ValueError, match='identity or content'):
        cache.load(day, 'D2', day_hours(day), H.issue_instant(day, H.NEW), ensemble=wrong)


def test_protocol_identity_and_saved_calendar_cannot_be_replaced(tmp_path, monkeypatch, authorized):
    fixture = Fixture(tmp_path, monkeypatch, date(2020, 1, 2))
    with pytest.raises(ValueError, match='protocol/calendar'):
        E.manifest_for(fixture.paths, {**IDENTITY, 'changed': True})
    fixture.run()
    state = ReplayState.load(fixture.paths.state(IDENTITY), IDENTITY)
    state.policies['nominal/v5'].records.pop(str(H.WARMUP_START))
    with pytest.raises(ValueError, match='omits a calendar'):
        E._validate_state_calendar(state)


def test_frozen_key_mismatch_and_missing_date_fail_closed():
    day = H.SCORED_START
    bundle = {'scoring_index': day_hours(day)}
    with pytest.raises(ValueError, match='explicit entry'):
        E._keys_for(day, bundle, {})
    with pytest.raises(ValueError, match='differ'):
        E._keys_for(day, bundle, {str(day): day_hours(day)[1:]})
    assert E._keys_for(day, {'scoring_index': day_hours(day)[:0]}, {str(day): []}).empty
    for day in (date(2021, 3, 28), date(2021, 10, 31)):
        assert E._keys_for(day, {'scoring_index': day_hours(day)}, {day: day_hours(day)}).equals(day_hours(day))


def test_idempotent_evidence_keeps_failure_and_rejects_changed_identity():
    budget = Ledger()
    evidence = {'cache_sha256': 'original', 'status': 'failed'}
    assert E.record_evidence_once(budget, 'native-task', evidence, {'failed_member_cache_records': 1})
    assert not E.record_evidence_once(budget, 'native-task', evidence, {'failed_member_cache_records': 1})
    assert budget.state['counts']['failed_member_cache_records'] == 1
    with pytest.raises(ValueError, match='different evidence'):
        E.record_evidence_once(budget, 'native-task', {**evidence, 'cache_sha256': 'replacement'})


def test_gate_rejection_precedes_context_build_or_fit(tmp_path, monkeypatch, authorized):
    called = []
    monkeypatch.setattr(E, 'contexts_and_caches', lambda *args: called.append('compute'))
    def reject(stage):
        raise RuntimeError('projection exceeds 388 hours')
    with pytest.raises(RuntimeError, match='388'):
        E.run_forecasts(tmp_path, IDENTITY, {}, gate=reject)
    assert not called


def test_timing_pilot_uses_only_frozen_probes_and_retains_failed_compute(tmp_path, monkeypatch, authorized):
    import cp24.member as physical
    dd, budget, calls = table(), Ledger(), []
    monkeypatch.setattr(H, 'art', lambda: tmp_path / '.local/artifacts/cp-26')
    paths = E.Paths.build(tmp_path)
    def prepare(root, k, route, path):
        plan = S.make_plan(dd, k, route, search_identity(root, k, route))
        S._atomic(path, plan)
        return plan
    monkeypatch.setattr(S, 'prepare_search', prepare)
    E.prepare(tmp_path, IDENTITY, gate=authorized)
    monkeypatch.setattr(M.Context, 'build', lambda root, settings, route: SimpleNamespace(
        dd=dd, settings=settings, noload_active=route == 'noload'))
    monkeypatch.setattr(S.subprocess, 'check_output', lambda command, cwd:
                        (Path(cwd) / command[2].split(':', 1)[1]).read_bytes())
    monkeypatch.setattr(E, 'fit_members', lambda ctx, origin, members: {
        members[0]: {'status': 'ok', 'fits': {'synthetic_physical': 1}, 'lineage': {'origin': str(origin)}}})
    def fit(dd, origin, config, seed, forecast_days, *, exclude_uncovered, charge):
        lower, window, _ = G.window(dd, origin, exclude_uncovered=True)
        assert (dd.days[window] < np.datetime64(origin)).all()
        charge()
        calls.append((origin, config, seed, tuple(forecast_days)))
        if seed == S.trial_fit_seed(0, 0, 0):
            raise ValueError('synthetic retained timing failure')
        return {'eur': np.ones((len(forecast_days), 24, 7)), 'window': {'end_exclusive': str(origin)},
                'seconds': 1., 'maxrss_bytes': 1, 'member': {'epochs_run': 1}}
    monkeypatch.setattr(physical, 'fit_member', fit)
    report = E.timing_pilot(tmp_path, IDENTITY, gate=authorized, budget=budget)
    assert len(report['summary']) == 42 and len(calls) == 42 * (8 + 12)
    assert report['origins'] == [str(S.search_day(k)) for k in range(14)]
    assert not report['evaluation_scores_computed'] and not report['serving_ensembles_created']
    text = json.dumps(report)
    assert all(term not in text for term in ('pinball_sum', 'validation_mae', '"central"', '"quantiles"'))
    for row in report['summary']:
        assert len(row['search_probe_wall_seconds']) == 12
        own = [p for p in report['probes'] if p['key']['route'] == row['route'] and p['key']['k'] == row['k']]
        search = [p for p in own if p['key']['task'].startswith('search-')]
        assert [p['key']['trial'] for p in search] == list(range(12))
        assert all(p['key']['seed'] == S.trial_fit_seed(row['k'], p['key']['trial'], 0) for p in search)
        daily = [p for p in own if p['key']['task'].startswith('daily-D2')]
        assert [p['key']['seed'] for p in daily] == S.member_seeds(row['k'])
        assert all(p['forecast_days'] == 1 for p in daily)
        assert all(p.get('forecast_days', 28) == 28 for p in search)
    assert sum(p['status'] == 'failed' for p in report['probes']) == 3
    count = len(calls)
    assert E.timing_pilot(tmp_path, IDENTITY, gate=authorized, budget=budget) == report
    assert len(calls) == count


def test_b0_provenance_uses_landed_weekday_source_and_issue_time():
    day = date(2022, 1, 4)
    data = SimpleNamespace(rows=lambda day: np.arange(24), naive=np.ones(24))
    result = M.fit_b0(SimpleNamespace(data=data, settings=H.NEW), day)
    assert result['records']['source_delivery_day'] == '2022-01-03'
    assert result['lineage']['issue_utc'] == H.issue_instant(day, H.NEW).isoformat()
    assert result['lineage']['seeds']['random_seed'] is None
