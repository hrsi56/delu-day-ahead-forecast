"""Synthetic controls: only the weather columns differ between arms; HG cache identity;
HG-H0 paired joint rule, H0 tie order and parity checks. No real data, fits or replay."""
from dataclasses import fields, replace
from datetime import date
import json

import numpy as np
import pandas as pd
import pytest

from cp15.data import Inputs, LABELS
from cp20 import components as comp
from cp20 import scoring
from cp20 import weather as wx


def tiny_inputs(n_days=3):
    idx = pd.date_range('2022-08-25 22:00', periods=24 * n_days, freq='h', tz='UTC')
    local = idx.tz_convert('Europe/Berlin')
    dates = np.array(local.date, dtype='datetime64[D]')
    n = len(idx)
    rng = np.random.default_rng(0)
    lear = rng.normal(size=(n, 175))
    return Inputs(frame=pd.DataFrame(), spec=None, index=idx, dates=dates, hours=local.hour.to_numpy(),
                  y=rng.normal(size=n), eligible=np.ones(n, bool), feature_valid=np.ones(n, bool),
                  level=np.zeros(n), scale=np.ones(n), lgbm_raw=np.zeros((n, 2)), lgbm_normalized=np.zeros((n, 2)),
                  lear_raw=lear, lear_normalized=lear * 2, naive=np.zeros(n), p={})


def design_for(data, missing_day=None):
    rows = []
    for t, d, h in zip(data.index, pd.to_datetime(data.dates).date, data.hours):
        v = [np.nan] * 3 if d == missing_day else [float(h), float(h) + 1, 10.0 * h]
        rows.append({'delivery_date': d, 'timestamp_utc': t, 'local_hour': h, **dict(zip(wx.COLUMNS, v))})
    return wx.WeatherDesign.from_features(pd.DataFrame(rows))


def test_augment_changes_only_the_two_lear_designs_by_three_appended_columns():
    data = tiny_inputs()
    aug, present = comp.augment(data, design_for(data))
    assert present.all()
    for f in fields(Inputs):
        if f.name in ('lear_raw', 'lear_normalized'):
            a, b = getattr(aug, f.name), getattr(data, f.name)
            assert a.shape == (b.shape[0], b.shape[1] + 3) and np.array_equal(a[:, :175], b)
            assert np.array_equal(a[:, 175:], aug.lear_raw[:, 175:])  # same unnormalised weather in both
        elif isinstance(getattr(data, f.name), np.ndarray):
            assert getattr(aug, f.name) is getattr(data, f.name)
        else:
            assert getattr(aug, f.name) is getattr(data, f.name) or getattr(aug, f.name) == getattr(data, f.name)
    assert np.allclose(aug.lear_raw[:, 175], data.hours)


def test_missing_weather_stays_nan_for_training_only_imputation():
    data = tiny_inputs()
    day = pd.to_datetime(data.dates).date[30]
    aug, _ = comp.augment(data, design_for(data, missing_day=day))
    rows = pd.to_datetime(data.dates).date == day
    assert np.isnan(aug.lear_raw[rows, 175:]).all() and np.isfinite(aug.lear_raw[~rows, 175:]).all()
    from cp15.models import prepared_linear
    train, other = aug.lear_raw[:40], aug.lear_raw[40:]
    xt, xo, fill, _ = prepared_linear(train, other)
    assert xt.shape[1] == 2 * 178  # three extra values + three extra indicators
    expected = np.nanmedian(train[:, 175:], axis=0)
    assert np.allclose(fill[175:], np.where(np.isfinite(expected), expected, 0.0))


def test_hg_cache_refuses_tampered_or_wrong_identity(tmp_path):
    data = tiny_inputs()
    day = pd.to_datetime(data.dates).date[30]
    identity = {'input_fingerprint': 'a', 'weather_design_sha256': 'b', 'protocol_sha256': 'c'}
    rows = data.rows(day)
    item = {'day': str(day), 'fold': 'fold_3', 'origin_utc': str(comp.origin_utc(day).tz_convert('UTC')),
            'timestamp_utc': list(map(str, data.index[rows])), 'scale_sha256': comp.array_hash(data.scale[rows]),
            **identity, 'central': {'A1': [1.0] * len(rows), 'B2': [2.0] * len(rows)}, 'fits': {}, 'weather_rows': {},
            'source': 'fresh_hg_components'}
    item['content_sha256'] = comp.digest(item)
    cache = comp.HGComponents(tmp_path, 'fold_3', data, identity)
    cache.save(item)
    assert cache.get(day)[2] == 'verified_cp20_hg_cache'
    with pytest.raises(ValueError):
        comp.HGComponents(tmp_path, 'fold_3', data, {**identity, 'weather_design_sha256': 'x'}).get(day)
    tampered = json.loads(cache.path(day).read_text())
    tampered['central']['A1'][0] = 9.0
    cache.path(day).write_text(json.dumps(tampered))
    with pytest.raises(ValueError):
        cache.get(day)
    with pytest.raises(ValueError, match='cache miss'):
        cache.get(pd.to_datetime(data.dates).date[0])


def synthetic_predictions(delta_hg=0.0, rng_seed=1):
    rng = np.random.default_rng(rng_seed)
    rows = []
    for fold, (start, end) in scoring.FOLD_WINDOWS.items():
        for d in pd.date_range(start, end)[:90]:
            for h in (10, 11):
                t = pd.Timestamp(d, tz='Europe/Berlin') + pd.Timedelta(hours=h)
                y = rng.normal(50, 10)
                for policy in scoring.POLICIES:
                    shift = {'B0': 8.0, 'HG': 2.0 + delta_hg}.get(policy, 2.0)
                    c = y + rng.normal(0, shift)
                    rows.append({'fold': fold, 'policy': policy, 'timestamp_utc': t.tz_convert('UTC'),
                                 'delivery_date': pd.Timestamp(d.date()), 'y_true': y, 'central': c, 'scale': 5.0,
                                 'level': 40.0, **{l: c + q for l, q in zip(LABELS, (-10, -6, -3, 0, 3, 6, 10))}})
    frame = pd.DataFrame(rows)
    expected = frame.loc[frame.policy.eq('B0'), ['fold', 'timestamp_utc', 'delivery_date']]
    return frame, expected


def test_hg_h0_is_the_only_contrast_and_rule_uses_upper_endpoints():
    frame, expected = synthetic_predictions(delta_hg=-1.5)
    out = scoring._evaluate(frame, expected, production=False, replicates=200)
    u = out['uncertainty']
    assert set(zip(u.candidate, u.baseline)) == {('HG', 'H0')}
    eq = u.loc[u.scope.eq('equal_fold')].set_index('metric')
    joint = eq.loc['WIS', 'ci_upper'] < 0 and eq.loc['MAE', 'ci_upper'] <= 0
    assert out['summary']['joint_conclusions']['HG-H0'] == ('observed joint improvement' if joint else 'no demonstrated joint preference')
    assert out['summary']['primary_contrast'] == 'HG-H0' and out['summary']['secondary_contrasts'] == []
    worse, expected = synthetic_predictions(delta_hg=+3.0)
    assert scoring._evaluate(worse, expected, production=False, replicates=200)['summary']['joint_conclusions']['HG-H0'] \
        == 'no demonstrated joint preference'


def test_exact_ties_rank_h0_first_and_parity_requires_same_scale_and_truth():
    frame, expected = synthetic_predictions()
    tie = frame.copy()
    hg = tie.policy.eq('HG')
    tie.loc[hg, ['central', *LABELS]] = tie.loc[tie.policy.eq('H0'), ['central', *LABELS]].to_numpy()
    assert scoring._evaluate(tie, expected, production=False, replicates=50)['summary']['ranking'] == ['H0', 'HG']
    bad = frame.copy()
    bad.loc[bad.policy.eq('HG'), 'scale'] = 6.0
    with pytest.raises(ValueError, match='parity'):
        scoring._evaluate(bad, expected, production=False, replicates=50)


def test_bootstrap_index_set_is_the_frozen_cp16_one():
    from cp16 import scoring as cp16
    a, b = scoring._indices(2000), cp16._indices(2000)
    assert all(np.array_equal(a[f], b[f]) for f in scoring.FOLDS)
