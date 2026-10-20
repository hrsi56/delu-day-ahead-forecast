"""r14 support admission and synthetic search controls; no model training or CP-26 scores."""
from datetime import date, timedelta
import hashlib
from itertools import combinations
import json
from pathlib import Path
import subprocess
from types import SimpleNamespace

import numpy as np
import pytest

from cp24 import design as G
from cp24 import sampler as SP
from cp26 import search as S


def table(last=date(2026, 7, 8), *, support=True):
    first = date(2019, 1, 1)
    days = np.arange(np.datetime64(first), np.datetime64(last) + 1)
    mask = np.zeros((len(days), 24), bool)
    mask[:, 0] = support
    return SimpleNamespace(days=days, first=first, mask=mask,
                           covered=np.ones(len(days), bool),
                           centre={'s4': np.zeros(len(days)), 'mad': np.zeros(len(days))},
                           scale={'s4': np.ones(len(days)), 'mad': np.ones(len(days))},
                           ix=lambda d: int((np.datetime64(d) - days[0]).astype(int)),
                           date_of=lambda i: first + timedelta(days=int(i)))


def plan(k=2, route='nominal', dd=None):
    return S.make_plan(dd or table(), k, route, {'synthetic': 'no fits'})


def ok(trial, batch, config, seed):
    return {'status': 'ok', 'pinball_sum': float(trial + 1), 'pinball_count': 7,
            'abs_error_sum': float(trial + 1), 'hours': 1, 'n_inputs': 12}


def resign(item):
    item['content_sha256'] = S.digest(item)
    return item


def test_schedule_service_periods_and_continuation_without_loading_future_data():
    assert S.search_day(0) == date(2020, 1, 15)
    assert S.search_day(13) == date(2026, 7, 8)
    assert S.search_day(14) == date(2027, 1, 6)
    assert S.serving_search(date(2020, 1, 14)) is None
    for k in range(14):
        assert S.serving_search(S.search_day(k)) == k
        assert S.serving_search(S.search_day(k + 1) - timedelta(days=1)) == k
        blocks = S.candidate_blocks(k)
        assert blocks[0][1] == S.search_day(k) - timedelta(days=1)
        assert all((last - first).days == 27 and first >= date(2019, 7, 1) for first, last in blocks)
        assert all(blocks[j + 1][1] == blocks[j][0] - timedelta(days=1) for j in range(len(blocks) - 1))


def test_extrema_equal_exhaustive_whole_week_choices_and_recent_week_never_held():
    dd = table(date(2019, 4, 1))
    # Differing per-week support makes the min-train/min-hold distinction observable.
    dd.mask[:, 0] = np.arange(len(dd.days)) % 5 != 0
    origin = date(2019, 3, 12)
    bounds = S.window_support(dd, origin)
    lower, ix, _ = G.window(dd, origin, exclude_uncovered=True)
    pool = S.week_pool(lower, origin)
    m = bounds['selected_heldout_weeks']
    counts = []
    for weeks in combinations(pool, m):
        tr, ho = G.split(dd, ix, list(weeks))
        counts.append((len(tr), len(ho)))
        assert (dd.days[ho] < np.datetime64(origin - timedelta(days=7))).all()
    assert bounds['minimum_possible_train_days'] == min(t for t, h in counts)
    assert bounds['maximum_possible_train_days'] == max(t for t, h in counts)
    assert bounds['minimum_possible_hold_days'] == min(h for t, h in counts)
    assert bounds['maximum_possible_hold_days'] == max(h for t, h in counts)
    for seed in (0, 1, S.trial_fit_seed(0, 0, 0), *S.member_seeds(0)):
        chosen, count = G.holdout_weeks(dd, lower, origin, seed)
        assert count == len(pool) and len(chosen) == m
        assert set(chosen) <= set(pool)


def test_support_mask_uses_landed_statistics_weather_and_partial_target_days():
    dd = table(date(2021, 1, 1))
    origin = date(2020, 6, 1)
    lower, ix, _ = G.window(dd, origin, exclude_uncovered=True)
    baseline = S.window_support(dd, origin)['support_days_before_holdout']
    dd.mask[ix[0]] = False
    dd.centre['mad'][ix[1]] = np.nan
    dd.scale['s4'][ix[2]] = np.nan
    dd.covered[ix[3]] = False
    # A single eligible target slot is the landed day-support mask, not a full-day gate.
    dd.mask[ix[4]] = False
    dd.mask[ix[4], 7] = True
    record = S.window_support(dd, origin)
    assert record['support_days_before_holdout'] == baseline - 4
    assert record['excluded_uncovered_days'] == 1


def test_zero_week_pool_is_ineligible_without_minus_zero_slice(monkeypatch):
    dd = table(date(2019, 1, 15))
    bounds = S.window_support(dd, date(2019, 1, 5))
    assert bounds['whole_week_pool'] == bounds['selected_heldout_weeks'] == 0
    assert bounds['minimum_possible_hold_days'] == bounds['maximum_possible_hold_days'] == 0
    assert bounds['minimum_possible_train_days'] == bounds['support_days_before_holdout']
    assert not bounds['every_possible_split_sufficient']


@pytest.fixture(scope='module')
def local_support_data():
    from cp26 import harness as H
    root = Path(__file__).resolve().parents[1]
    data = H.load(root, H.NEW, before=S.search_day(13))
    return root, data


@pytest.mark.parametrize('route', S.ROUTES)
def test_all_fourteen_search_dates_landed_support_and_first_251_46(route, local_support_data):
    from cp26 import harness as H
    root, data = local_support_data
    settings = H.GFS6 if route == 'gfs6' else H.NEW
    dd = G.build(data, H.weather_design(root, settings))
    counts = []
    for k in range(14):
        support = S.batch_support(dd, k)
        assert support['content_sha256'] == S.digest(support)
        assert all(b['last'] < support['search_day'] for b in support['batches'])
        assert support['batches'] == [b for b in support['candidates'] if b['retained']]
        eligible = [b for b in support['candidates'] if b['every_possible_split_sufficient']]
        assert support['batches'] == eligible[:11]
        assert all(b['minimum_possible_train_days'] >= 250 and b['minimum_possible_hold_days'] >= 14
                   for b in support['batches'])
        counts.append(support['B'])
        if k == 0:
            assert support['B'] == 1
            assert support['batches'][0]['first'] == '2019-12-18'
            assert support['batches'][0]['minimum_possible_train_days'] == 251
            assert support['batches'][0]['minimum_possible_hold_days'] == 46
    assert counts == [1, 7] + [11] * 12


def test_sampler_exact_128_separate_seed_domains_and_no_load_effective_distinctness():
    for k in range(14):
        a, b = S.trials(k, 'nominal'), S.trials(k, 'noload')
        assert len(a) == len(b) == 128 and a == S.trials(k, 'nominal')
        assert all(S.effective_config(x, 'noload') == S.effective_config(y, 'noload') for x, y in zip(a, b))
        assert all(not {'load_d1', 'load_d7'} & set(c['groups']) for c in b)
        fit_seeds = {S.trial_fit_seed(k, t, j) for t in range(128) for j in range(11)}
        assert len(fit_seeds) == 128 * 11
        assert len(set(S.member_seeds(k))) == 8 and not fit_seeds & set(S.member_seeds(k))
        assert all(seed // 100_000 == (26_000_000 + k * 100_000) // 100_000 for seed in fit_seeds)
    left = {**S.trials(0, 'nominal')[0], 'id': 'one', 'groups': ['price_d2', 'load_d1']}
    right = {**left, 'id': 'two', 'groups': ['price_d2', 'load_d7']}
    assert S.effective_key(left, 'noload') == S.effective_key(right, 'noload')
    assert S.effective_key(left, 'nominal') != S.effective_key(right, 'nominal')
    with pytest.raises(ValueError):
        S.trial_fit_seed(0, 128, 0)


def test_halving_runs_landed_43_survivors_and_preserves_ranking_ties():
    p = plan()
    calls = []

    def evaluate(t, b, cfg, seed):
        calls.append((t, b, seed))
        return ok(t, b, cfg, seed)

    result = S.run_search(p, evaluate)
    nb = p['B']
    assert len(calls) == 128 * 4 + 43 * (nb - 4)
    assert len(result['survivors']) == 43
    assert result['complete'] and len(result['members']) == 8
    S.validate_ensemble(result, 2, 'nominal')
    assert result['ranking_all_batches'][:4] == [p['trials'][t]['id'] for t in range(4)]
    tied = S.run_search(p, lambda t, b, c, seed: {**ok(t, b, c, seed), 'pinball_sum': 1.0})
    sizes = {c['id']: SP.n_params(c, 12) for c in p['trials']}
    expected = SP.rank({c['id']: 1.0 for c in p['trials']}, sizes, [c['id'] for c in p['trials']])
    assert tied['survivors'] == expected[:43]


def test_no_resampling_for_effective_duplicates_fewer_than_four_is_registered_failure(monkeypatch):
    base = S.trials(0, 'nominal')[0]

    def duplicate(rng, space, tid):
        return {**base, 'id': tid, 'groups': ['price_d2', 'load_d1' if int(tid[-3:]) % 2 else 'load_d7']}

    monkeypatch.setattr(SP, 'sample', duplicate)
    p = plan(route='noload')
    calls = []
    result = S.run_search(p, lambda t, b, c, seed: (calls.append(t), ok(t, b, c, seed))[1])
    assert len(p['trials']) == 128
    assert set(calls) == set(range(128))
    assert not result['complete'] and result['members'] == []
    assert result['failure_reason'] == 'fewer_than_four_valid_effective_configurations'
    assert not result['older_ensemble_extended']
    assert result['next_search_day'] == str(S.search_day(3))


def test_zero_support_makes_no_fit_and_never_extends_previous_ensemble(tmp_path):
    p = plan(dd=table(support=False))
    result = S.run_search(p, lambda *args: pytest.fail('no fit on zero eligible batches'))
    assert result['B'] == 0 and result['failure_reason'] == 'zero_eligible_batches'
    assert not result['complete'] and result['members'] == []
    with pytest.raises(S.SearchUnavailable):
        S.validate_ensemble(result, 2, 'nominal')
    old = tmp_path / 'nominal/k01/result.json'
    S._atomic(old, S.run_search(plan(k=1), ok))
    with pytest.raises(S.SearchUnavailable, match='no extension'):
        S.load_search_for_origin(tmp_path, S.search_day(2), 'nominal')


def test_any_failed_batch_ranks_trial_last_and_eight_members_is_mandatory():
    p = plan()
    result = S.run_search(p, lambda t, b, c, seed: {'status': 'failed'} if t == 0 and b == 0 else ok(t, b, c, seed))
    assert result['ranking_all_batches'][0] == p['trials'][1]['id']
    assert result['trials'][0]['pinball_all_batches'] is None
    assert result['failed_fits'] == 1
    short = json.loads(json.dumps(result))
    short['members'].pop()
    resign(short)
    with pytest.raises(S.SearchUnavailable, match='exactly eight'):
        S.validate_ensemble(short, 2, 'nominal')
    with pytest.raises(S.SearchUnavailable):
        S.validate_ensemble(result, 3, 'nominal')
    with pytest.raises(S.SearchUnavailable, match='different route'):
        S.validate_ensemble(result, 2, 'gfs6')


def test_resume_reuses_success_and_failure_records_without_new_fit_or_changed_seed(tmp_path):
    p = plan(k=0)
    calls = []
    cache = S.TrialCache(tmp_path, p)

    def evaluate(t, b, c, seed):
        calls.append((t, b, seed))
        return {'status': 'failed', 'cause': 'synthetic'} if t == 0 and b == 0 else ok(t, b, c, seed)

    first = S.run_search(p, evaluate, cache=cache)
    assert len(calls) == 128 * p['B']
    second = S.run_search(p, lambda *args: pytest.fail('resumed cached task fitted again'), cache=cache)
    assert second == first and second['failed_fits'] == 1
    bad = json.loads(cache.path(1, 0).read_text())
    bad['key']['seed'] += 1
    resign(bad)
    S._atomic(cache.path(1, 0), bad)
    with pytest.raises(ValueError, match='mismatched'):
        cache.load(1, 0)


def test_interrupted_search_resumes_same_sampler_seed_and_completed_task_cache(tmp_path):
    p = plan(k=0)
    cache = S.TrialCache(tmp_path, p)
    before, after = [], []

    def interrupted(t, b, cfg, seed):
        if t == 7 and b == 0:
            raise KeyboardInterrupt('synthetic hard stop, no fit')
        before.append((t, b, seed))
        return ok(t, b, cfg, seed)

    with pytest.raises(KeyboardInterrupt):
        S.run_search(p, interrupted, cache=cache)

    def resumed(t, b, cfg, seed):
        after.append((t, b, seed))
        return ok(t, b, cfg, seed)

    resumed_result = S.run_search(p, resumed, cache=cache)
    continuous_result = S.run_search(p, ok)
    assert not set(before) & set(after)
    assert len(before) + len(after) == 128 * p['B']
    # Cached task records add provenance keys; selected members and metrics match.
    assert resumed_result['members'] == continuous_result['members']
    assert resumed_result['ranking_all_batches'] == continuous_result['ranking_all_batches']
    assert [r['pinball_all_batches'] for r in resumed_result['trials']] == [
        r['pinball_all_batches'] for r in continuous_result['trials']]


def test_support_freeze_and_plan_signature_fail_closed_before_any_fit():
    p = plan()
    p['support']['batches'][0]['minimum_possible_train_days'] = 249
    with pytest.raises(ValueError, match='signature'):
        S.run_search(p, lambda *args: pytest.fail('tampered plan fitted'))


def test_search_lineage_changes_when_context_adapter_changes(monkeypatch, tmp_path):
    from cp26 import harness as H
    monkeypatch.setattr(H, 'input_fingerprint', lambda root: 'fixed-inputs')
    for name in S.MODEL_CODE:
        p = tmp_path / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('original')
    # Since r16 (8070238) the operational modules report their original recipe identity from the
    # committed runtime-lineage record, so the fixture commits one for these synthetic sources.
    recipe = {'src/cp26/harness.py': 'a' * 64, 'src/cp26/search.py': 'b' * 64}
    lineage = tmp_path / H.RUNTIME_LINEAGE
    lineage.parent.mkdir(parents=True)
    lineage.write_text(json.dumps({
        'schema': 'cp26-operational-lineage-v21-r16', 'scientific_base_commit': H.SCIENTIFIC_BASE_COMMIT,
        'actual_code_sha256': {name: hashlib.sha256(b'original').hexdigest() for name in recipe},
        'original_recipe_code_sha256': recipe}))
    git = ['git', '-c', 'user.name=cp26', '-c', 'user.email=cp26@localhost', '-c', 'commit.gpgsign=false',
           '-c', 'core.hooksPath=/dev/null']
    for args in (('init', '-q'), ('add', '-A'), ('commit', '-q', '-m', 'synthetic lineage')):
        subprocess.run([*git, *args], cwd=tmp_path, check=True, capture_output=True)
    original = S.search_identity(tmp_path, 0, 'nominal')
    assert {name: original['code_sha256'][name] for name in recipe} == recipe
    (tmp_path / 'src/cp26/members.py').write_text('changed-context-adapter')
    assert S.search_identity(tmp_path, 0, 'nominal') != original


def test_production_fit_gate_requires_subsequent_authorization(monkeypatch):
    monkeypatch.delenv('CP26_EXPERIMENT_AUTHORIZED', raising=False)
    monkeypatch.setenv('CP26_MONITORED_JOB', 'synthetic-repair-test')
    with pytest.raises(RuntimeError, match='subsequent authorized'):
        S.execute_search(Path('.'), Path('unused'), Path('unused'), Path('unused'))
