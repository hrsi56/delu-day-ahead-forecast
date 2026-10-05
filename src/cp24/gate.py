"""The pre-fold gate (capstone v21-r11 §23.6, §23.10): v4's members and DDNN-2 at the 280 gate origins.

Each fold f has a gate window G_f = [D0_f - 56, D0_f), none of whose days is a warm-up or evaluation
day of any fold. On each gate day D two sets of forecasts are issued, each from a fresh fit at D's
origin that trains on all history before D (earlier folds' warm-up and evaluation days included);
nothing of fold f on or after D0_f is materialised (the data is loaded before D0_f):

* **v4's members** with their unchanged code (`cp24.v4members`), through the scoped weather-coverage
  wrapper. One pass at the 280 origins, cached and reused across rounds (§23.11), with its parity
  proven at covered origins (`job_v4_parity`) and the unwrapped code's refusal of a fold-4 gate day
  recorded as the paired positive control.
* **DDNN-2** with the round's ensemble for the fold (`job_gate`).

The gate passes if, pooled over the 280 days as point estimates: G0 every forecast is finite and
ordered; G1 v5's central MAE <= v4's central MAE, both built from the gate-day members; G2 D2's MAE
<= 1.10 x L's MAE; G3 the quantile cap binds on fewer than 0.1% of the members' emitted hour-levels.
It is a screen, not a claim: it can only prevent a fold look.
"""
from __future__ import annotations

from datetime import date, timedelta
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import time
import traceback

import numpy as np
import pandas as pd

from cp15.data import array_hash, sha
from cp20.components import HGComponents
from cp21.execution import digest
from cp21.lgbm import hg_central, hgl_central
from cp22.execution import cp21_lineage_hashes
from . import v4members as V4
from .budget import atomic, ledger
from .inputs import hg_identity, input_fingerprint, load, weather_design
from .jobs import art, cp20_art, stamp
from .preflight import fold_table

OUT = Path('reports/ddnn2')
V4_CODE = ('src/cp24/v4members.py', 'src/cp21/components.py', 'src/cp21/lgbm.py', 'src/cp20/components.py',
           'src/cp15/models.py', 'src/cp15/data.py')


def v4_identity(root: Path) -> dict:
    return {'cp24_input_fingerprint': input_fingerprint(root), 'weather_design_sha256': weather_design(root).sha256,
            'code_sha256': {name: sha(root / name) for name in V4_CODE}}


def gate_days(folds: list[dict]) -> list[tuple[str, date, date]]:
    out = []
    for f in folds:
        g0, g1 = f['gate']
        out += [(f['fold'], g0 + timedelta(days=k), f['d0']) for k in range((g1 - g0).days + 1)]
    return out


def v4_path(fold: str, day: date) -> Path:
    return art() / 'v4-gate' / fold / f'{day}.json'


def load_v4(fold: str, day: date, identity: dict) -> dict | None:
    path = v4_path(fold, day)
    if not path.exists():
        return None
    item = json.loads(path.read_text())
    if item.get('content_sha256') != digest(item) or item['fold'] != fold or item['day'] != str(day) \
            or item['identity'] != identity:
        raise ValueError(f'stale or wrong v4 gate entry {fold} {day}')
    return item


# ------------------------------------------------------------------ workers
_worker: dict = {}


def _init_worker(root: str, ledger_path: str):
    os.environ['CP24_LEDGER'] = ledger_path
    root = Path(root)
    _worker.update(root=root, design=weather_design(root), budget=ledger(), data={}, identity=v4_identity(root))


def _data_before(cutoff: date):
    w = _worker
    if cutoff not in w['data']:
        w['data'] = {cutoff: load(w['root'], before=cutoff)}
    return w['data'][cutoff]


def _v4_task(task):
    fold, day_s, cutoff_s = task
    w = _worker
    day = date.fromisoformat(day_s)
    try:
        if load_v4(fold, day, w['identity']) is not None:
            return fold, day_s, 'reused', 0.0, None
    except ValueError:
        pass  # a stale or wrong entry is refitted, never reused (and the pass cap still binds)
    began = time.time()
    try:
        data = _data_before(date.fromisoformat(cutoff_s))
        w['budget'].reserve(v4_gate_origins=1)
        result = V4.fit(data, w['design'], day, w['budget'], 'gate', wrapped=True)
    except Exception as exc:  # recorded, never substituted
        atomic(art() / 'failures' / f'v4-gate_{fold}_{day_s}.json', {'fold': fold, 'day': day_s, 'error': repr(exc),
                                                                     'traceback': traceback.format_exc(), 'written_utc': stamp()})
        return fold, day_s, 'failed', time.time() - began, repr(exc)
    item = {'fold': fold, 'data_cutoff_exclusive': cutoff_s, 'identity': w['identity'], **result, 'written_utc': stamp()}
    item['content_sha256'] = digest(item)
    atomic(v4_path(fold, day), item)
    return fold, day_s, 'fitted', time.time() - began, None


def _pool(root: Path, workers: int):
    if workers > int(os.environ.get('CP24_WORKERS', '1')):
        raise ValueError('more pool workers than the monitor declared')
    return mp.get_context('spawn').Pool(workers, initializer=_init_worker, initargs=(str(root), os.environ['CP24_LEDGER']))


def job_v4_gate(root: Path, rest) -> int:
    """v4's members at the 280 gate origins: one pass, cached, reused across rounds."""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=int(os.environ.get('CP24_WORKERS', '1')))
    args = ap.parse_args(rest)
    folds = fold_table(root)
    tasks = [(fold, str(day), str(d0)) for fold, day, d0 in gate_days(folds)]
    if len(tasks) != 280:
        raise ValueError('the gate has 280 origins')
    budget = ledger()
    budget.event('v4_gate_start', tasks=len(tasks), workers=args.workers)
    failed, t0 = 0, time.time()
    with _pool(root, args.workers) as pool:
        for i, (fold, day, source, seconds, error) in enumerate(pool.imap_unordered(_v4_task, tasks, chunksize=1), 1):
            failed += source == 'failed'
            if i % 20 == 0 or source == 'failed':
                print('v4-gate', fold, day, source, round(seconds, 1), f'{i}/{len(tasks)}', f'{time.time() - t0:.0f}s',
                      error or '', flush=True)
    budget.event('v4_gate_complete', failed=failed)
    print(json.dumps({'tasks': len(tasks), 'failed': failed, 'seconds': time.time() - t0}), flush=True)
    return 0 if not failed else 5


# ------------------------------------------------------------------ the parity proof and its control
PARITY_OFFSETS = (0, 45)
#: Fold 4's first warm-up day: its window starts on 2023-03-25, the first covered day after the gap.
BOUNDARY_ORIGIN = ('fold_4', date(2025, 3, 22))
REFUSAL_ORIGIN = ('fold_4', date(2025, 1, 25))


def parity_origins(root: Path) -> list[tuple[str, date, str]]:
    """Two evaluation origins per fold (offsets 0 and 45 days, the next day with eligible hours), plus
    fold 4's first warm-up day, whose window starts on the first covered day after the gap."""
    out = []
    full = load(root)
    for f in fold_table(root):
        for off in PARITY_OFFSETS:
            d = f['evaluation_start'] + timedelta(days=off)
            while not len(full.rows(d)):
                d += timedelta(days=1)
            out.append((f['fold'], d, 'evaluation'))
    out.append((*BOUNDARY_ORIGIN, 'warmup'))
    return out


def _parity_task(task):
    fold, day_s, phase, cutoff_s = task
    w = _worker
    day = date.fromisoformat(day_s)
    data = _data_before(date.fromisoformat(cutoff_s) if cutoff_s else date(2026, 4, 8))
    w['budget'].reserve(v4_parity_origins=1)
    result = V4.fit(data, w['design'], day, w['budget'], 'parity', wrapped=True)
    return fold, day_s, phase, result


def job_v4_parity(root: Path, rest) -> int:
    """The gate's v4 code path, wrapper included, against the committed fold vectors (bit for bit), and
    the unwrapped code's refusal of a fold-4 gate day (the paired positive control). This is also
    item 2's independent representative HG and v4 slice. Reproducing committed vectors at warm-up or
    evaluation origins reads no outcome that is not already committed (§23.6)."""
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--workers', type=int, default=int(os.environ.get('CP24_WORKERS', '1')))
    args = ap.parse_args(rest)
    folds = {f['fold']: f for f in fold_table(root)}
    origins = parity_origins(root)
    tasks = [(fold, str(d), phase, None if phase == 'evaluation' else str(folds[fold]['evaluation_start']))
             for fold, d, phase in origins]
    members = pd.read_parquet(root / 'reports/distribution-challenger/members.parquet')
    cp21_saved = pd.read_parquet(root / 'reports/block-challenger/predictions.parquet')
    for frame in (members, cp21_saved):
        frame['timestamp_utc'] = pd.to_datetime(frame.timestamp_utc, utc=True)
    hashes = cp21_lineage_hashes(root)
    hg_ident = hg_identity(root)
    results = []
    with _pool(root, args.workers) as pool:
        for fold, day_s, phase, res in pool.imap_unordered(_parity_task, tasks, chunksize=1):
            day = date.fromisoformat(day_s)
            ts = pd.DatetimeIndex(pd.to_datetime(res['timestamp_utc'], utc=True))
            got = {k: np.asarray(v, float) for k, v in res['central'].items()}
            rec = {'fold': fold, 'day': day_s, 'phase': phase, 'excluded_training_days': res['wrapper']['excluded_training_days']}
            if phase == 'evaluation':
                mem = members.loc[members.fold.eq(fold)].set_index('timestamp_utc').loc[ts]
                ln = cp21_saved.loc[cp21_saved.policy.eq('L-N') & cp21_saved.fold.eq(fold)].set_index('timestamp_utc').loc[ts]
                lr = cp21_saved.loc[cp21_saved.policy.eq('L-R') & cp21_saved.fold.eq(fold)].set_index('timestamp_utc').loc[ts]
                committed = {'A1': mem['A1'].to_numpy(float), 'B2': mem['B2'].to_numpy(float),
                             'L-N': ln.central.to_numpy(float), 'L-R': lr.central.to_numpy(float)}
                rec['committed_source'] = ('reports/distribution-challenger/members.parquet (A1, B2); '
                                           'reports/block-challenger/predictions.parquet (L-N, L-R)')
                rec['bitwise_equal'] = {k: bool(np.array_equal(got[k], committed[k])) for k in committed}
                rec['max_abs_difference'] = {k: float(np.max(np.abs(got[k] - committed[k]))) for k in committed}
                rec['HG_bitwise_equal'] = bool(np.array_equal(hg_central(got['A1'], got['B2']), mem['HG'].to_numpy(float)))
                rec['v4_bitwise_equal'] = bool(np.array_equal(
                    hgl_central(got['A1'], got['B2'], got['L-N'], got['L-R']), mem['HGL'].to_numpy(float)))
            else:
                data = load(root, before=folds[fold]['evaluation_start'])
                _, centers, _ = HGComponents(cp20_art() / 'hg-components', fold, data, hg_ident).get(day)
                rec['committed_source'] = ('CP-20 HG component cache (A1, B2), identity-verified; CP-21 committed lineage '
                                           'central_sha256 (L-N, L-R, v4)')
                rec['bitwise_equal'] = {'A1': bool(np.array_equal(got['A1'], centers['A1'])),
                                        'B2': bool(np.array_equal(got['B2'], centers['B2'])),
                                        'L-N': array_hash(got['L-N']) == hashes[('L-N', fold, day_s)],
                                        'L-R': array_hash(got['L-R']) == hashes[('L-R', fold, day_s)]}
                rec['v4_bitwise_equal'] = array_hash(hgl_central(got['A1'], got['B2'], got['L-N'], got['L-R'])) \
                    == hashes[('HGL', fold, day_s)]
                rec['HG_bitwise_equal'] = bool(rec['bitwise_equal']['A1'] and rec['bitwise_equal']['B2'])
            rec['wrapper_changed_nothing'] = not rec['excluded_training_days']
            results.append(rec)
            print('parity', fold, day_s, phase, rec['bitwise_equal'], rec['v4_bitwise_equal'], flush=True)
    # The paired positive control: the unwrapped code refuses a fold-4 gate day; the wrapper does not.
    _init_worker(str(root), os.environ['CP24_LEDGER'])
    fold, day = REFUSAL_ORIGIN
    data = load(root, before=folds[fold]['d0'])
    refusal = V4.refuses_unwrapped(data, _worker['design'], day, _worker['budget'])
    passed = all(all(r['bitwise_equal'].values()) and r['HG_bitwise_equal'] and r['v4_bitwise_equal']
                 and r['wrapper_changed_nothing'] for r in results) and refusal['all_refused'] \
        and len(refusal['excluded_by_wrapper']) > 0
    out = {'schema': 'cp24-v4-parity-v1', 'written_utc': stamp(), 'passed': passed,
           'code_path': 'cp24.v4members.fit (wrapper applied): cp21.components.refit for A1_w/B2_w, cp21.lgbm.fit_arm for '
                        'L-N/L-R -- the gate\'s exact path',
           'origins': sorted(results, key=lambda r: (r['fold'], r['day'])),
           'unwrapped_refuses_fold4_gate_day': {'fold': fold, 'day': str(day), **refusal},
           'reading': 'bitwise parity with the committed vectors at covered origins, where the wrapper leaves out no '
                      'training day; the unwrapped member code refuses a fold-4 gate day whose window reaches the gap'}
    atomic(root / OUT / 'v4-parity.json', out)
    print(json.dumps({'passed': passed, 'refusal': refusal['all_refused'],
                      'n_excluded_at_refusal_day': len(refusal['excluded_by_wrapper'])}), flush=True)
    return 0 if passed else 6
