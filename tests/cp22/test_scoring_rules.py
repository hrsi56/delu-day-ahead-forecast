"""CP-22 §20.5-§20.6 logic on synthetic data (no research data, no capped pass): the shared index
set, the §20.5 contrast set, and the three mechanical rules with their first unmet conditions."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from cp15.scoring import FOLD_WINDOWS, QUANTILES
from cp22 import scoring as S
from cp22.evaluate import clean

ALL = list(S.SAVED + S.FIXED_NEW + S.W_ARMS)


def _daily(effects=None, seed=0, policies=ALL):
    rng = np.random.default_rng(seed)
    effects = effects or {}
    frames = []
    for fold, (start, end) in FOLD_WINDOWS.items():
        dates = pd.date_range(start, end)
        base_mae = rng.uniform(10, 30, len(dates))
        hours = np.full(len(dates), 24)
        if fold == 'fold_3':
            hours[19] = 0
        for policy in policies:
            f = effects.get(policy, 1.0)
            f = f if isinstance(f, dict) else {'MAE': f, 'WIS': f}
            noise = rng.normal(1, 0.02, len(dates))
            frames.append(pd.DataFrame({'policy': policy, 'fold': fold, 'delivery_date': dates, 'n_hours': hours,
                                        'MAE': np.where(hours > 0, base_mae * f['MAE'] * noise, np.nan),
                                        'WIS': np.where(hours > 0, base_mae * .6 * f['WIS'] * noise, np.nan)}))
    return pd.concat(frames, ignore_index=True)


def _criteria(policies, failing=()):
    return pd.DataFrame([dict(policy=p, criterion=c, metric='x', scope='s', actual=1.0, lower_limit=None, upper_limit=None,
                              comparator=None, status='not_met' if (p in failing and c == 3) else 'met',
                              passed=not (p in failing and c == 3)) for p in policies for c in range(1, 7)])


def test_index_set_is_cp20s_and_contrasts_cover_section_20_5():
    rows, draws, scores, meta = S.bootstrap(_daily(), ALL, S.contrasts('R'), replicates=2000)
    assert meta['index_sha256'] == S.CP20_INDEX_SHA256 and meta['index_equals_cp20']
    pairs = {(c, b) for c, b, _ in S.contrasts('R')}
    for needed in (('R', 'HGL'), ('M', 'HGL'), ('W+DL', 'R'), ('R', 'M'), ('A-PN-sel', 'M'), ('R', 'A-PN-sel'),
                   ('A-PN-sel', 'A-LP'), ('A-LN', 'HGL'), ('W+ACI', 'R'), ('W+DL', 'W+ACI'), ('W+DLF', 'W+DL'),
                   ('v4+DL', 'HGL'), ('v3+DL', 'HG'), ('HGL', 'HG'), ('W+DLF', 'HG'), ('R', 'HG'), ('M', 'HG')):
        assert needed in pairs
    assert not any('W' in c and c.startswith('W') for c, _, _ in S.contrasts(None))
    assert len(draws) == len(S.contrasts('R')) * 2 * 2000 * 6


def test_replacement_sequence_R_then_M_then_none():
    pols = list(S.SAVED + S.FIXED_NEW)
    crit = _criteria(pols)
    rows, *_ = S.bootstrap(_daily({'R': 0.95, 'M': 0.95}, policies=pols), pols, S.contrasts(None), replicates=400)
    assert S.replacement(rows, crit, keys_complete=True)['winner'] == 'R'
    v = S.replacement(rows, _criteria(pols, failing=('R',)), keys_complete=True)
    assert v['winner'] == 'M' and v['first_unmet_condition'] == {'R': 2, 'M': None}
    rows, *_ = S.bootstrap(_daily({'R': 1.2, 'M': 1.2}, policies=pols), pols, S.contrasts(None), replicates=400)
    v = S.replacement(rows, crit, keys_complete=True)
    assert v['winner'] is None and v['first_unmet_condition'] == {'R': 1, 'M': 1} and 4 in v['candidates']['R']['unmet_conditions']
    # non-inferiority: a tie (no interval entirely above zero) passes condition 1, unlike joint improvement
    rows, *_ = S.bootstrap(_daily({}, seed=3, policies=pols), pols, S.contrasts(None), replicates=400)
    v = S.replacement(rows, crit, keys_complete=True)
    assert v['candidates']['R']['conditions'][1]['met']
    assert S.replacement(rows, crit, keys_complete=False)['candidates']['R']['first_unmet_condition'] in (3, 4)


def _metrics(cov):
    return pd.DataFrame([dict(policy=p, scope='pooled', fold='all', coverage95=c) for p, c in cov.items()])


def test_dynamic_layer_and_fast_component_rules():
    crit = _criteria(ALL)
    rows, *_ = S.bootstrap(_daily({'W+DL': {'MAE': 1.0, 'WIS': 0.9}, 'W+DLF': {'MAE': 1.0, 'WIS': 0.85}}), ALL,
                           S.contrasts('R'), replicates=400)
    dl = S.dynamic_layer(rows, crit, _metrics({'R': .93, 'W+DL': .945}), 'R')
    assert dl['adopted'] and dl['first_unmet_condition'] is None
    fast = S.fast_component(rows, crit, dl)
    assert fast['applies'] and fast['adopted']
    # coverage farther from 0.95 than W's -> condition 4 unmet
    dl2 = S.dynamic_layer(rows, crit, _metrics({'R': .95, 'W+DL': .93}), 'R')
    assert not dl2['adopted'] and dl2['first_unmet_condition'] == 4
    assert not S.fast_component(rows, crit, dl2)['applies']
    # no WIS gain -> condition 1 unmet
    rows, *_ = S.bootstrap(_daily({}, seed=5), ALL, S.contrasts('R'), replicates=400)
    assert S.dynamic_layer(rows, crit, _metrics({'R': .93, 'W+DL': .945}), 'R')['first_unmet_condition'] == 1
    none = S.dynamic_layer(None, None, None, None)
    assert not none['applies'] and not S.fast_component(None, None, none)['applies']


def _synthetic(policies, seed=0):
    rng = np.random.default_rng(seed)
    keys = []
    for fold, (start, _end) in FOLD_WINDOWS.items():
        days = list(pd.date_range(start, periods=4)) + ([pd.Timestamp('2022-08-16'), pd.Timestamp('2022-08-17')]
                                                       if fold == 'fold_3' else [])
        for day in days:
            index = pd.date_range(day.tz_localize('Europe/Berlin'), periods=24, freq='h').tz_convert('UTC')
            keys += [(fold, t, day) for t in index]
    base = pd.DataFrame(keys, columns=['fold', 'timestamp_utc', 'delivery_date'])
    y = rng.normal(80, 30, len(base))
    scale = rng.uniform(5, 20, len(base))
    frames = []
    for i, policy in enumerate(policies):
        central = y + rng.normal(0, 5 + i % 7, len(base))
        spread = np.array([-2, -1.3, -0.7, 0, 0.7, 1.3, 2])[None, :] * (10 + i % 5)
        q = np.sort(central[:, None] + spread + rng.normal(0, 1, (len(base), 1)), axis=1)
        part = base.assign(policy=policy, y_true=y, central=central, scale=scale, level=80.0)
        for j, name in enumerate(QUANTILES):
            part[name] = q[:, j]
        frames.append(part)
    return pd.concat(frames, ignore_index=True), base[['fold', 'timestamp_utc', 'delivery_date']].copy()


def test_the_scoring_path_runs_end_to_end_with_and_without_a_winner():
    for policies, w in ((list(S.SAVED + S.FIXED_NEW), None), (ALL, 'M')):
        pred, expected = _synthetic(policies)
        tables = S.evaluate(pred, expected, policies, w, production=False, replicates=60)
        back = json.loads(json.dumps(clean(tables['summary']), allow_nan=False, sort_keys=True))
        assert back['replacement']['winner'] in ('R', 'M', None)
        assert set(back['contrasts']) == {f'{c}-{b}' for c, b, _ in S.contrasts(w)}
        assert back['dynamic_layer']['applies'] == (w is not None)
        assert set(tables['criteria'].policy) == {p for p in policies if p not in S.SAVED} | {'HG', 'HGL'}
        assert set(tables['metrics'].policy) == set(policies)
        assert {'peak', 'stress', 'recovery', 'hour', 'block'} <= set(tables['diagnostics'].scope)
