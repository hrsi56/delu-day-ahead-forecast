"""The whole CP-21 scoring path on a synthetic population (no research data, no capped pass):
validation, hourly losses, tables, the §8 screen, the bootstrap with ratio intervals, the
§17.6 verdict, and a strict JSON write of the summary (undefined values become null, never NaN)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from cp15.scoring import FOLD_WINDOWS, QUANTILES
from cp21 import scoring as S
from cp21.evaluate import clean


def _synthetic(seed=0):
    rng = np.random.default_rng(seed)
    frames = []
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
    for i, policy in enumerate(S.POLICIES):
        central = y + rng.normal(0, 5 + i, len(base))
        spread = np.array([-2, -1.3, -0.7, 0, 0.7, 1.3, 2])[None, :] * (10 + i)
        q = np.sort(central[:, None] + spread + rng.normal(0, 1, (len(base), 1)), axis=1)
        part = base.assign(policy=policy, y_true=y, central=central, scale=scale, level=80.0)
        for j, name in enumerate(QUANTILES):
            part[name] = q[:, j]
        if policy in S.NEW:
            part['scale'] = scale  # the price-only A1 scale of HG, shared
        frames.append(part)
    pred = pd.concat(frames, ignore_index=True)
    expected = base[['fold', 'timestamp_utc', 'delivery_date']].copy()
    return pred, expected


def test_the_scoring_path_runs_end_to_end_and_writes_strict_json():
    pred, expected = _synthetic()
    lineage = {'origins': [{'arm': 'HGL', 'fold': 'fold_1', 'phase': 'evaluation', 'day': '2020-07-01', 'predicted': True,
                            'hour_support': {str(h): {'n': 28, 'distinct_days': 28, 'weight': 28 / 84} for h in range(24)}}]}
    tables = S.evaluate(pred, expected, production=False, replicates=60, lineage=lineage)
    summary = clean(tables['summary'])
    text = json.dumps(summary, allow_nan=False, sort_keys=True)  # must not raise
    back = json.loads(text)
    assert back['adoption']['verdict'] in ('v4', 'Not adopted')
    assert set(back['adoption']['conditions']) == {'1', '2', '3', '4'}
    assert back['block_split']['contrast'] == 'L-R-L-P'
    assert len(tables['replicates']) == len(S.CONTRASTS) * 2 * 60 * 6
    assert set(tables['criteria'].policy) == set(S.CANDIDATES)
    assert set(tables['metrics'].policy) == set(S.POLICIES)
    assert not tables['fallback'].empty
    # NaN limits (criterion 1 has no lower limit) are carried as null, not as a number
    assert any(v is None for rec in back['adoption']['conditions']['2']['values']['not_met'] for v in rec.values()) \
        or back['adoption']['conditions']['2']['met']


def test_clean_maps_undefined_values_to_null():
    assert clean({'a': float('nan'), 'b': [np.float64(1.5), np.inf], 3: np.bool_(True)}) == {'a': None, 'b': [1.5, None], '3': True}
