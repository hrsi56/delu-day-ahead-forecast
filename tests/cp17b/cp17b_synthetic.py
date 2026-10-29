"""Synthetic payloads and fits for CP-17b's CI-safe tests: each policy's payload with a chosen set of forecastable
hours, carrying exactly the arrays `cp17.issue.check_inputs` and `forecastable_keys` read, bound by its identity.
"""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

from cp17 import dailyfit, issue

FIT = (80.0, 10 ** 9)
EPOCH = date(1970, 1, 1)


def keys_of(day: date) -> list[str]:
    return issue.canonical_hours(day)


def flat(n: int, base: float = 50.0) -> list[list[float]]:
    return [[base + d for d in (-20, -10, -5, 0, 5, 10, 20)] for _ in range(n)]


def _ns(keys) -> np.ndarray:
    return np.asarray([pd.Timestamp(k).value for k in keys], dtype=np.int64)


def buffer(day: date) -> list[dict]:
    """28 released zero-error days ending at D-2."""
    days = [day - timedelta(days=d) for d in range(29, 1, -1)]
    return [{'day': str(d), 'errors': [0.0] * len(keys_of(d))} for d in days]


def _finish(arrays: dict, meta: dict) -> tuple[dict, dict]:
    meta['array_sha256'] = {k: dailyfit.array_hash(v) for k, v in sorted(arrays.items())}
    meta['payload_sha256'] = dailyfit.payload_digest(arrays, meta)
    return arrays, meta


def payload(policy: str, day: date, keys: list[str]) -> tuple[dict, dict]:
    """`policy`'s payload for `day` whose forecastable hours are `keys` (the target day's outcome blanked)."""
    meta = {'schema': dailyfit.SCHEMAS[policy], 'policy': policy, 'day': str(day), 'embargo': 'synthetic'}
    if policy == 'A1':
        e = (day - EPOCH).days
        arrays = {'days': np.array([e - 1, e], dtype=np.int64), 'price': np.array([[1.0] * 24, [np.nan] * 24]),
                  'y': np.array([[1.0] * 24, [np.nan] * 24]), 'mask': np.zeros((2, 24), np.int8),
                  'key_ts': _ns(keys), 'key_slot': np.arange(len(keys), dtype=np.int64)}
        return _finish(arrays, meta)
    if policy == 'B0':
        hours = [k for d in range(7, -1, -1) for k in keys_of(day - timedelta(days=d))]
        price = np.where(np.isin(_ns(hours), _ns(keys_of(day))), np.nan, 50.0)
        meta['b0_buffer'] = buffer(day)
        return _finish({'price_ns': _ns(hours), 'price': price, 'key_ns': _ns(keys)}, meta)
    rows = keys_of(day - timedelta(days=1)) + keys_of(day)
    n, today = len(rows), np.array([k in set(keys_of(day)) for k in rows])
    dates = np.array([(day - EPOCH).days if t else (day - EPOCH).days - 1 for t in today], dtype=np.int64)
    arrays = {'index_ns': _ns(rows), 'dates': dates, 'hours': np.arange(n) % 24, 'y': np.where(today, np.nan, 1.0),
              'eligible': np.ones(n, np.int8), 'feature_valid': np.array([not t or r in set(keys) for t, r in zip(today, rows)],
                                                                         dtype=np.int8),
              'level': np.ones(n), 'scale': np.ones(n), 'lear_raw': np.zeros((n, 1)), 'lear_normalized': np.zeros((n, 1))}
    meta.update(dates_dtype='datetime64[D]', protocol={}, offset=0, h_buffer=buffer(day))
    return _finish(arrays, meta)


def result(policy: str, day: date, keys: list[str], base: float = 50.0) -> dict:
    """A fit's result as `cp17.dailyfit` returns it, on `keys`."""
    q = flat(len(keys), base)
    out = {'policy': policy, 'day': str(day), 'index': list(keys), 'quantiles': q,
           'quantiles_sha256': dailyfit.array_hash(np.asarray(q, float)), 'central': [base] * len(keys)}
    if policy == 'A1':
        out.update(search=13, ensemble_content_sha256='0' * 64, members=[])
    elif policy in ('v2', 'v4'):
        out.update(train_rows={}, scale=[2.0] * len(keys))
    else:
        out.update(source_day=str(day - timedelta(days=7)))
    return out
