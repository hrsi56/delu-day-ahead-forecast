"""Synthetic CP-28 ledgers for the causal-control and unit tests: no stored input is read."""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

from cp28 import engine, states
from cp28.reader import Day, canonical_hours

OFFSETS = np.array([-30.0, -15.0, -6.0, 0.0, 6.0, 15.0, 30.0])


def price_series(first: date, last: date, seed: int = 7) -> pd.Series:
    """Hourly prices with a daily shape and noise, from a year before ``first`` (for the states)."""
    rng = np.random.default_rng(seed)
    keys = []
    day = first - timedelta(days=400)
    while day <= last:
        keys.extend(canonical_hours(day))
        day += timedelta(days=1)
    index = pd.DatetimeIndex(keys)
    hours = np.asarray(index.tz_convert('Europe/Berlin').hour, float)
    values = 50 + 15 * np.sin(hours / 24 * 2 * np.pi) + rng.normal(0, 8, len(index))
    values[rng.random(len(index)) < 0.01] = -5.0
    return pd.Series(values, index=index, name='price')


def ledger(first: date, days: int, prices: pd.Series, *, scored_from: date | None = None, seed: int = 11,
           missing_member: dict | None = None, no_scale: set | None = None) -> list[Day]:
    """Members are noisy views of the outcome (a stand-in for issued forecasts); v5/B0 quantiles are fixed offsets."""
    rng = np.random.default_rng(seed)
    out = []
    for k in range(days):
        d = first + timedelta(days=k)
        index = canonical_hours(d)
        y = prices.reindex(index).to_numpy(float)
        members = {'c_HG': y + rng.normal(0, 4, len(y)), 'L': y + rng.normal(1, 6, len(y)), 'D2': y + rng.normal(-1, 5, len(y))}
        if missing_member and d in missing_member:
            members[missing_member[d]] = None
        d2q = None if members['D2'] is None else members['D2'][:, None] + OFFSETS
        v5 = (2 / 3) * members['c_HG'] + members['L'] / 6 + members['D2'] / 6 if all(v is not None for v in members.values()) else y
        scored = scored_from is not None and d >= scored_from
        out.append(Day(day=d, issue_utc='', index=index, scoring_index=index, scored=scored, complete=True,
                       members=members, member_status={}, d2_quantiles=d2q,
                       scale=None if no_scale and d in no_scale else np.full(len(y), 10.0),
                       v5_source='native', v5_quantiles=v5[:, None] + OFFSETS * 1.1,
                       b0_source='native', b0_quantiles=y[:, None] * 0 + 50 + OFFSETS * 2))
    return out


def run(days, prices, *, minimum=10, full=20, state_frame=None, **kwargs):
    frame = state_frame if state_frame is not None else states.issue_states(prices, [d.day for d in days])
    return engine.run(days, prices, frame, config=engine.Config(minimum=minimum, full=full), **kwargs)


def by(result, arm, day):
    return next(i for i in result.issues if i.arm == arm and i.day == day)
