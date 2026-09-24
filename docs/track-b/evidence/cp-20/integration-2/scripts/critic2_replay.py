"""CP-20 Integration Critic 2 -- independent causal H-layer replay for both arms (own implementation of v21 14.2).

Inputs read directly (no cp15/cp16/cp20 state or replay code): truth and the A1 scale from data/snapshot.parquet,
H0 components from reports/cp15/folds/*-issued.parquet + reports/v2-causal/lineage.json new_components,
HG components from the content-hashed .local HG cache. One continuous replay per fold and arm from the frozen
warm-up start to the evaluation end (the candidate restarted from saved state at the admission boundary).
Charges 1,276 policy-days (638 origins x 2 arms) before replaying.
"""
from __future__ import annotations

from datetime import date, timedelta
import hashlib
import json
import os
from pathlib import Path
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path.cwd() / 'src'))
from cp20.budget import Budget  # noqa: E402  (ledger only)

ROOT = Path.cwd()
ART = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20')
OUT = ART / 'critic-2/out'
WA = ROOT / 'reports/weather-ablation'
LV = np.array([.025, .10, .25, .50, .75, .90, .975])
Q = ['p025', 'p10', 'p25', 'p50', 'p75', 'p90', 'p975']
BER = 'Europe/Berlin'

man = json.loads((ROOT / 'reports/v2-causal/input-manifest.json').read_text())
n_days = sum(len(pd.date_range(f['warmup_start'], f['evaluation_end'])) for f in man['folds'])
assert n_days == 638, n_days
b = Budget(os.environ['CP20_LEDGER'])
print('reserved', b.reserve(policy_days=2 * n_days), flush=True)

snap = pd.read_parquet(ROOT / 'data/snapshot.parquet', columns=['timestamp_utc', 'delivery_date', 'price_eur_mwh'])
snap = snap[(snap.delivery_date >= date(2019, 1, 1)) & (snap.delivery_date <= date(2026, 4, 7))]
price = pd.Series(snap.price_eur_mwh.to_numpy(float), index=pd.DatetimeIndex(snap.timestamp_utc).tz_convert('UTC').as_unit('ns'))
assert price.index.is_unique and price.index.is_monotonic_increasing


def hours_of(d):
    return pd.date_range(pd.Timestamp(d, tz=BER), pd.Timestamp(d + timedelta(days=1), tz=BER), freq='h', inclusive='left').tz_convert('UTC').as_unit('ns')


def scale_of(d):
    start = pd.Timestamp(d, tz=BER).tz_convert('UTC')
    hrs = pd.date_range(end=start - pd.Timedelta(hours=1), periods=168, freq='h').as_unit('ns')
    v = price.reindex(hrs).to_numpy(float)
    return max(float(np.std(v, ddof=1)), 1.0)


def ahash(a):
    return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()


# component sources
cp16new = json.loads((ROOT / 'reports/v2-causal/lineage.json').read_text())['new_components']
issued = {}
for f in man['folds']:
    x = pd.read_parquet(ROOT / f"reports/cp15/folds/{f['fold']}-issued.parquet", filters=[('policy', 'in', ['A1', 'B2'])])
    x['ts'] = pd.DatetimeIndex(x.timestamp_utc).tz_convert('UTC').as_unit('ns')
    issued[f['fold']] = {(p, d): g.sort_values('ts') for (p, d), g in x.groupby(['policy', 'delivery_date'])}


def h0_source(fold, day, ts):
    a = issued[fold].get(('A1', day))
    if a is not None:
        bb = issued[fold][('B2', day)]
        if not (pd.DatetimeIndex(a.ts).equals(ts) and pd.DatetimeIndex(bb.ts).equals(ts)):
            raise ValueError(f'H0 CP-15 rows differ {fold} {day}')
        return a.central.to_numpy(float), bb.central.to_numpy(float), a.scale.to_numpy(float), 'cp15'
    item = cp16new.get(f'{fold}:{day}')
    if item is None:
        raise ValueError(f'no H0 source {fold} {day}')
    if not pd.DatetimeIndex(pd.to_datetime(item['timestamp_utc'], utc=True)).as_unit('ns').equals(ts):
        raise ValueError(f'H0 CP-16 rows differ {fold} {day}')
    return np.asarray(item['central']['A1'], float), np.asarray(item['central']['B2'], float), None, 'cp16'


def hg_source(fold, day):
    item = json.loads((ART / 'hg-components' / fold / f'{day}.json').read_text())
    body = {k: v for k, v in item.items() if k != 'content_sha256'}
    if hashlib.sha256(json.dumps(body, sort_keys=True, allow_nan=False, default=str).encode()).hexdigest() != item['content_sha256']:
        raise ValueError('HG cache digest')
    ts = pd.DatetimeIndex(pd.to_datetime(item['timestamp_utc'], utc=True)).as_unit('ns') if item['timestamp_utc'] else pd.DatetimeIndex([], tz='UTC').as_unit('ns')
    if not len(ts):
        return ts, None, None, item
    return ts, np.asarray(item['central']['A1'], float), np.asarray(item['central']['B2'], float), item


class H:
    """Own reading of section 14.2: 28 most recent complete released delivery days (<= D-2), consumed once."""

    def __init__(self):
        self.pending, self.consumed, self.buffer, self.log = {}, set(), [], []

    def release(self, d):
        for day in sorted(self.pending):
            if day > d - timedelta(days=2):
                break
            ts, c, s = self.pending[day]
            if not ts.equals(hours_of(day)):
                self.consumed.add(day)
                self.log.append((str(d), str(day), 'incomplete_day_never_buffered'))
                continue
            yv = price.reindex(ts).to_numpy(float)
            if not np.isfinite(yv).all():
                self.log.append((str(d), str(day), 'truth_unavailable_pending'))
                continue
            self.buffer = sorted(self.buffer + [(day, (yv - c) / s, ts.tz_convert(BER).hour.to_numpy())], key=lambda x: x[0])[-28:]
            self.consumed.add(day)
        for day in self.consumed:
            self.pending.pop(day, None)

    def predict(self, d, ts, c, s):
        if len(self.buffer) != 28:
            raise ValueError(f'{d}: buffer {len(self.buffer)}')
        e = np.concatenate([x[1] for x in self.buffer])
        hh = np.concatenate([x[2] for x in self.buffer])
        dd = np.concatenate([[x[0]] * len(x[1]) for x in self.buffer])
        pooled = np.quantile(e, LV, method='linear')
        layer, support = {}, {}
        for h in range(24):
            sel = hh == h
            n, nd = int(sel.sum()), len(set(dd[sel]))
            w = n / (n + 56) if nd >= 14 else 0.0
            layer[h] = w * np.quantile(e[sel], LV, method='linear') + (1 - w) * pooled if w else pooled.copy()
            support[str(h)] = {'distinct_days': nd, 'n': n, 'weight': w}
        out = c[:, None] + s[:, None] * np.asarray([layer[h] for h in ts.tz_convert(BER).hour])
        return out, {'buffer_days': len(self.buffer), 'buffer_start': str(self.buffer[0][0]), 'buffer_end': str(self.buffer[-1][0]),
                     'hour_support': support, 'vector_sha256': ahash(out), 'buffer_sha256': ahash(e)}

    def issue(self, d, ts, c, s):
        assert d not in self.pending and d not in self.consumed
        self.pending[d] = (ts, c, s)


pred = pd.read_parquet(WA / 'predictions.parquet')
pred = pred[pred.policy.isin(['H0', 'HG'])].copy()
pred['ts'] = pd.DatetimeIndex(pred.timestamp_utc).tz_convert('UTC').as_unit('ns')
lin = json.loads((WA / 'lineage.json').read_text())
adm_rec = {(r['arm'], r['fold'], r['day']): r for r in lin['admission']}
res = {'scale_mismatch_rows': 0, 'scale_checked_days': 0, 'h0_source_counts': {}, 'eval_rows': 0,
       'eval_bitwise_equal_rows': 0, 'eval_max_abs': 0.0, 'central_bitwise_equal': True, 'admission_vectors_matched': 0,
       'admission_meta_matched': 0, 'admission_total': 0, 'eval_meta_matched': 0, 'eval_meta_total': 0, 'failures': [],
       'fallback_hour_cells': 0, 'hour_cells': 0, 'buffer_dates_equal_between_arms': True, 'incomplete_or_pending_events': [],
       'hg_cache_scale_sha_equal': True, 'eval_origin_meta_by_arm': {}}
lin_orig = {(r['arm'], r['fold'], r['day'], r['phase']): r for r in lin['origins']}
for f in man['folds']:
    fold = f['fold']
    first, end = date.fromisoformat(f['evaluation_start']), date.fromisoformat(f['evaluation_end'])
    adm_days = {x['day'] for x in f['admission']}
    states = {'H0': H(), 'HG': H()}
    frames = {'H0': [], 'HG': []}
    for d in pd.date_range(f['warmup_start'], end).date:
        ts, a1g, b2g, item = hg_source(fold, d)
        n = len(ts)
        if n:
            s_d = scale_of(d)
            s = np.full(n, s_d)
            res['scale_checked_days'] += 1
            if ahash(s) != item['scale_sha256']:
                res['hg_cache_scale_sha_equal'] = False
            a1h, b2h, sc15, src = h0_source(fold, d, ts)
            res['h0_source_counts'][src] = res['h0_source_counts'].get(src, 0) + 1
            if sc15 is not None and not np.array_equal(sc15, s):
                res['scale_mismatch_rows'] += int((sc15 != s).sum())
            cents = {'H0': a1h / 2 + b2h / 2, 'HG': a1g / 2 + b2g / 2}
        predict = n and (str(d) in adm_days or d >= first)
        phase = 'training_only' if d < first else 'evaluation'
        metas = {}
        for arm in ('H0', 'HG'):
            st = states[arm]
            st.release(d)
            if predict:
                try:
                    out, meta = st.predict(d, ts, cents[arm], s)
                except ValueError as exc:
                    res['failures'].append((arm, fold, str(d), repr(exc)))
                    out, meta = None, None
                if meta:
                    metas[arm] = meta
                    res['hour_cells'] += 24
                    res['fallback_hour_cells'] += sum(v['weight'] == 0 for v in meta['hour_support'].values())
                    if phase == 'training_only':
                        res['admission_total'] += 1
                        r = adm_rec.get((arm, fold, str(d)))
                        if r and r['vector_sha256'] == meta['vector_sha256']:
                            res['admission_vectors_matched'] += 1
                        if r and all(r[k] == meta[k] for k in ('buffer_days', 'buffer_start', 'buffer_end', 'hour_support')) and lin_orig[(arm, fold, str(d), 'training_only')].get('buffer_sha256') == meta['buffer_sha256']:
                            res['admission_meta_matched'] += 1
                    else:
                        frames[arm].append(pd.DataFrame(out, columns=Q).assign(ts=ts, central=cents[arm], scale=s))
                        r = lin_orig.get((arm, fold, str(d), 'evaluation'))
                        res['eval_meta_total'] += 1
                        if r and r.get('vector_sha256') == meta['vector_sha256'] and all(r[k] == meta[k] for k in ('buffer_days', 'buffer_start', 'buffer_end', 'hour_support', 'buffer_sha256')):
                            res['eval_meta_matched'] += 1
            if n:
                st.issue(d, ts, cents[arm], s)
        if len(metas) == 2 and (metas['H0']['buffer_start'], metas['H0']['buffer_end'], metas['H0']['hour_support']) != \
                (metas['HG']['buffer_start'], metas['HG']['buffer_end'], metas['HG']['hour_support']):
            res['buffer_dates_equal_between_arms'] = False
    for arm in ('H0', 'HG'):
        res['incomplete_or_pending_events'] += [(arm, fold, *x) for x in states[arm].log]
        mine = pd.concat(frames[arm], ignore_index=True).sort_values('ts').reset_index(drop=True)
        cand = pred[(pred.policy == arm) & (pred.fold == fold)].sort_values('ts').reset_index(drop=True)
        if not (len(mine) == len(cand) and pd.DatetimeIndex(mine.ts).equals(pd.DatetimeIndex(cand.ts))):
            res['failures'].append((arm, fold, 'key mismatch', len(mine), len(cand)))
            continue
        a, c = mine[Q].to_numpy(float), cand[Q].to_numpy(float)
        res['eval_rows'] += len(mine)
        res['eval_bitwise_equal_rows'] += int((a == c).all(axis=1).sum())
        res['eval_max_abs'] = max(res['eval_max_abs'], float(np.max(np.abs(a - c))))
        if not (np.array_equal(mine.central.to_numpy(), cand.central.to_numpy()) and np.array_equal(mine.scale.to_numpy(), cand.scale.to_numpy())):
            res['central_bitwise_equal'] = False
    print(fold, json.dumps({k: v for k, v in res.items() if k not in ('incomplete_or_pending_events', 'eval_origin_meta_by_arm')}), flush=True)
    # final state comparison with the candidate's persisted per-fold states (buffer days and errors)
    for arm in ('H0', 'HG'):
        cand_state = lin['states'][fold][arm]
        cb = [(x['day'], x['errors']) for x in cand_state['buffer']]
        mb = [(str(dd), e.tolist()) for dd, e, _ in states[arm].buffer]
        res.setdefault('final_state_buffer_equal', {})[f'{arm}:{fold}'] = cb == mb
res['incomplete_or_pending_events'] = res['incomplete_or_pending_events'][:40]
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'replay.json').write_text(json.dumps(res, indent=1, default=str))
print(json.dumps(res, indent=1, default=str)[:5000])
