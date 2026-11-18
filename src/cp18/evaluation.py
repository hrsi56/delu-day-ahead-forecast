"""The committed evaluation records: `cp17.scoring.evaluate`, per window and per policy (the product, and B0 as context).

**The three windows never pool (§19.6).** Each record is one window, one evidence class and one policy:

| Window | Evidence class | Computed from | In the Space |
|---|---|---|---|
| development | development · post-selection, per development window | CP-26's stored nominal forecasts (A1's D2, B0's native) and the development snapshot's prices, as CP-17's scoring check computed them (`cp17.tools.scorecheck`) | static, from evidence |
| development | development rehearsal (CP-18 dry runs) | the store's issued days on development dates, the reconciled outcomes, and B0's shadow forecasts from its served training windows | recomputed |
| 4.7T | one-shot fresh-data test · not yet scored | empty until 4.7T is scored | recomputed (empty) |
| prospective | prospective · evaluation in progress until CP-19 | the issued days after the development boundary; none yet | recomputed (empty) |

The dry runs' issued days (2026-08-31 to 2026-09-05) are a development rehearsal: labelled so everywhere, and never
shown or scored as prospective or as 4.7T (`cp18.spaceglue.window_days` puts no development date in either).

The prospective record per input class (the Owner's decision 31, CP-18d) is `class_sets`: the days whose inputs all
precede the cutoff on their own, all issued days beside them, each with its count. It is computed at the Space's build
and served in the Space's live record, not in the bundle, whose files keep the frozen schema.

**The static development records** are computed once (`python -m cp18.evaluation development`, which reads CP-26's
stored ledger from the local-only `evidence/cp-26` extract) and committed at `DEVELOPMENT_FILE`; their summaries must
equal CP-17's committed scoring check (`reports/cp17/scoring-check.json`) exactly. CP-18's activation places the file
once at `live/pinned/evaluation/development.json`.

**The daily record** (`live/evaluation/<as-of day>.json`, `cp18.records`) holds the recomputed windows and names the
static file by hash, so a day's commit stays small; the bundle's `evaluation.json` is the static records followed by
the day's.
"""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path

import numpy as np

from . import spaceglue as G
from .records import EVALUATION_PATH, RecordLog, dump_bytes

DEVELOPMENT_FILE = 'reports/cp18b/evaluation/development.json'
PINNED_DEVELOPMENT_FILE = 'live/pinned/evaluation/development.json'
SCHEMA = 'cp18b-development-evaluation-v1'
DAILY_SCHEMA = 'cp18b-daily-evaluation-v1'
POLICY_NAME = {'A1': 'product', 'B0': 'B0'}


def development(root) -> dict:
    """CP-17's two development windows, A1 and B0, as committed records (local-only inputs: CP-26's stored ledger)."""
    from cp17 import scoring
    from cp17.tools import scorecheck
    issued, outcomes = scorecheck.windows(Path(root))
    truth = {k: (np.nan if v is None else v) for k, v in outcomes.items()}
    windows, summaries = [], {}
    for name, items in issued.items():
        window, policy = name.split('/')
        first, last = scorecheck.WINDOWS[window]
        record = scoring.evaluate(items, truth)
        windows.append({'window': 'development', 'policy': POLICY_NAME[policy], 'record': record,
                        'evidence_class': f"{G.DEVELOPMENT} · CP-26's stored nominal forecasts · {window} ({first} to {last})"})
        p = record['pooled']
        summaries[name] = {'days': p['scored_days'], 'hours': p['scored_hours'], 'partial_days': p['partial_days'],
                           'mae_eur': p['mae_eur'], 'wis_eur': p['wis_eur'], 'percentage': p['percentage']['share'],
                           'coverage': {b: c['share'] for b, c in p['coverage'].items()}}
    return {'schema': SCHEMA, 'source': ("cp17.tools.scorecheck.windows: CP-26's stored nominal forecasts (A1's D2 "
                                         "quantiles; B0's native quantiles) on CP-25's frozen eligible keys, with the "
                                         "development snapshot's prices"),
            'evidence_class': 'development_post_selection', 'windows': windows, 'summaries': summaries}


def matches_scoring_check(value: dict, root) -> list[str]:
    """The committed summaries against CP-17's scoring check, item by item (exact)."""
    check = json.loads((Path(root) / 'reports/cp17/scoring-check.json').read_text())['summary']
    problems = []
    for name, s in value['summaries'].items():
        theirs = check.get(name)
        if theirs is None:
            problems.append(f'{name}: not in the scoring check')
            continue
        for key, v in s.items():
            if theirs.get(key) != v:
                problems.append(f'{name}/{key}: {v!r} against the scoring check\'s {theirs.get(key)!r}')
    return problems


def load_development(root, path: str = DEVELOPMENT_FILE) -> tuple[list[dict], str]:
    data = (Path(root) / path).read_bytes()
    value = json.loads(data)
    if value.get('schema') != SCHEMA:
        raise ValueError(f'{path}: not the static development records')
    return value['windows'], hashlib.sha256(data).hexdigest()


def empty(window: str, evidence_class: str, policy: str) -> dict:
    from cp17 import scoring
    return {'window': window, 'evidence_class': evidence_class, 'policy': policy, 'record': scoring.evaluate([], {})}


def daily_windows(forecasts: dict, outcomes: dict, b0: list[dict]) -> list[dict]:
    """The recomputed windows, product then B0 in each: the rehearsal, 4.7T (empty until scored), the prospective
    record. `b0` holds B0's forecasts of the issued days (`spaceglue.b0_items`). Their schema is the frozen one
    (the frozen verifier, through `cp18.r7`): decision 31's sets are `class_sets`, outside the bundle."""
    from cp17 import scoring
    truth = G.outcome_map(outcomes)
    days = sorted(d['delivery_day'] for d in forecasts['days'])
    out = []
    for window, label in (('development', G.REHEARSAL), ('4.7T', G.FRESH_TEST), ('prospective', G.PROSPECTIVE)):
        for policy in ('product', 'B0'):
            entry = {'window': window, 'evidence_class': label, 'policy': policy}
            entry['record'] = scoring.evaluate(_items(policy, forecasts, b0, G.window_days(entry, days)), truth)
            out.append(entry)
    return out


def _items(policy: str, forecasts: dict, b0: list[dict], chosen: list[str]) -> list[dict]:
    if policy == 'product':
        return G.product_items(forecasts, chosen)
    return [{k: v for k, v in it.items() if k != 'quantiles_sha256'} for it in b0 if it['day'] in chosen]


#: The prospective record per input class (the Owner's decision 31, CP-18d): the issued days whose inputs all precede
#: the cutoff on their own, and all issued days beside them, each with its count.
SETS = (('before_cutoff', 'issued days with every input before the cutoff'), ('all', 'all issued days'))


def class_sets(files: dict[str, bytes], classes: dict[str, str]) -> dict:
    """Decision 31's evaluation sets, computed at the Space's build from the served bundle (its issued forecasts,
    outcomes and B0's served training windows) and each issued day's class from the live store (`classes`). The
    `all` set must equal the bundle's own prospective windows (`evaluation.json`), or it is refused. Outside the
    bundle: the bundle's files keep the frozen schema."""
    import json
    from cp17 import scoring
    forecasts = json.loads(files['issued-forecasts.json'])
    truth = G.outcome_map(json.loads(files['outcomes.json']))
    served = {(w['window'], w['policy']): w for w in json.loads(files['evaluation.json'])['windows']
              if w['window'] == 'prospective'}
    days = sorted(d['delivery_day'] for d in forecasts['days'])
    missing = [d for d in G.window_days({'window': 'prospective', 'evidence_class': G.PROSPECTIVE}, days)
               if d not in classes]
    if missing:
        raise ValueError(f'issued days without an input class (decision 31): {missing}')
    out = []
    for subset, label in SETS:
        entry = {'window': 'prospective', 'evidence_class': G.PROSPECTIVE, 'subset': subset}
        chosen = G.window_days(entry, days, classes)
        windows = []
        for policy in ('product', 'B0'):
            absent = []
            if policy == 'product':
                items = G.product_items(forecasts, chosen)
            else:
                items, absent = G.b0_items(files, chosen)       # as the recomputation does: absent days are named
            record = scoring.evaluate([{k: v for k, v in it.items() if k != 'quantiles_sha256'} for it in items], truth)
            if subset == 'all' and ('prospective', policy) in served:
                check = scoring.recompute_check(record, served[('prospective', policy)]['record'])
                if not check['match']:
                    raise ValueError(f'the all-days set of {policy} differs from the bundle\'s prospective window')
            windows.append({'policy': policy, 'record': record,
                            **({'absent_days': absent} if policy == 'B0' and absent else {})})
        out.append({'set': subset, 'label': label, 'evidence_class': f'{G.PROSPECTIVE} · {label}',
                    'issued_days': len(chosen), 'days': chosen, 'windows': windows})
    return {'schema': 'cp18d-evaluation-sets-v1', 'source': ('cp17.scoring.evaluate on the served bundle\'s issued '
            'forecasts and outcomes, per input class (cp18.inputclass), computed at the build'), 'sets': out}


def evaluation_bundle(static: list[dict], daily: list[dict]) -> dict:
    return {'schema': 'cp17-evaluation-bundle-v1', 'windows': list(static) + list(daily)}


def commit_daily(live, as_of: date, daily: list[dict], static_sha256: str, run_id: str) -> dict:
    """The day's committed record under `<live>/evaluation/` (`live/evaluation/` on `main`), once per as-of day."""
    value = {'schema': DAILY_SCHEMA, 'as_of_day': str(as_of), 'run_id': run_id, 'static_development_sha256': static_sha256,
             'windows': daily}
    return RecordLog(Path(live) / Path(EVALUATION_PATH).name).append('evaluation', f'{as_of}.json', value, as_of_day=str(as_of),
                                                          run_id=run_id)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='python -m cp18.evaluation')
    sub = ap.add_subparsers(dest='cmd', required=True)
    d = sub.add_parser('development', help="the static development records, from CP-26's stored ledger (local only)")
    d.add_argument('--root', default='.', type=Path)
    d.add_argument('--out', default=Path(DEVELOPMENT_FILE), type=Path)
    args = ap.parse_args(argv)
    value = development(args.root)
    problems = matches_scoring_check(value, args.root)
    if problems:
        print('\n'.join(problems[:20]))
        return 1
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(dump_bytes(value))
    print('development records', len(value['windows']), 'windows; equal to the scoring check;',
          hashlib.sha256(args.out.read_bytes()).hexdigest()[:16])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
