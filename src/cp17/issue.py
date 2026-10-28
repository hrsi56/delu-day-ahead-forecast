"""The product's daily issuance: the frozen failure policy, the success definition, and the issued artifact.

**The failure policy** (the Owner's decisions 11 and 12, 2026-10-28):

- GFS late or missing at the issue time: A1's fit is recorded as skipped for an unavailable input, and the
  chain is v2, then B0, then a failed issuance;
- A1's own fit fails while the weather is available: v4, then v2, then B0, then a failed issuance;
- a fallback whose own fit fails passes to the next one in its chain;
- A1 issues whenever its own fit succeeds; the validity of other policies' members never triggers a fallback;
- every fallback is complete: no subset of members is renormalized and no quantile is manufactured;
- a failed or skipped fit is displayed as such, even when a fallback issues (§16.2).

**A successful daily fit** (§16.2, as the brief fixes it), for delivery day D issued at D-1 11:00
Europe/Berlin, is one that passes all of:

1. *inputs*: the payload's identity verifies; the target day's outcome is absent (the embargo); released
   errors in any interval buffer are from complete delivery days <= D-2; training targets end before D;
2. *training*: the policy's members train under the frozen rules with no guard refusal and no non-finite
   value (a `dailyfit` exception is a failed fit);
3. *emission*: all seven quantiles for every delivery hour of D (23, 24 or 25), finite and ordered;
4. *the artifact*: written with its training window, labels, seeds, timestamps and parent, input and state
   hashes, and its manifest verifies (`artifact`, `verify_artifact`);
5. *resources*: on the issuing host, one worker, within 15 minutes of wall time and 4 GB of peak memory.

Anything else is a failed fit. A fallback forecast never counts as a successful A1 fit.
"""
from __future__ import annotations

from datetime import date, timedelta
import hashlib
import json
import time
import traceback

import numpy as np

from .dailyfit import FitFailure, array_hash, canonical

PRODUCT = 'delu-day-ahead-policy'
DESIGNATED = 'A1'
CHAINS = {'gfs_unavailable': ('v2', 'B0'), 'a1_failed': ('v4', 'v2', 'B0')}
WALL_LIMIT_SECONDS = 15 * 60
MEMORY_LIMIT_BYTES = 4 * 1024 ** 3
SCHEMA = 'cp17-issued-artifact-v1'


def issue_utc(day: date) -> str:
    """D-1 11:00 Europe/Berlin as UTC (§24.4), by the landed `cp25.guard.issue_time`."""
    from cp25.guard import issue_time
    return issue_time(day).isoformat()


def canonical_hours(day: date) -> list[str]:
    import pandas as pd
    local = pd.date_range(pd.Timestamp(day, tz='Europe/Berlin'), pd.Timestamp(day + timedelta(days=1), tz='Europe/Berlin'),
                          freq='h', inclusive='left')
    return [t.isoformat() for t in local.tz_convert('UTC')]


def check_inputs(policy: str, arrays: dict, meta: dict) -> list[str]:
    """Criterion 1 on the shipped payload; returns the failed checks (empty when it passes)."""
    from .dailyfit import payload_digest
    day = date.fromisoformat(meta['day'])
    problems = []
    if meta.get('payload_sha256') != payload_digest(arrays, {k: v for k, v in meta.items() if k != 'payload_sha256'}):
        return ['the payload differs from its recorded identity']
    if policy == 'A1':
        if np.isfinite(arrays['price'][-1]).any() or np.isfinite(arrays['y'][-1]).any() or arrays['mask'][-1].any():
            problems.append("the target day's outcome is present in the day table")
        if int(arrays['days'][-1]) != (day - date(1970, 1, 1)).days:
            problems.append('the day table does not end at the target day')
    elif policy in ('v2', 'v4'):
        on_day = arrays['dates'] == (day - date(1970, 1, 1)).days
        if np.isfinite(arrays['y'][on_day]).any():
            problems.append("the target day's outcome is present in the rows")
    elif policy == 'B0':
        if np.isfinite(arrays['price'][np.isin(arrays['price_ns'], arrays['key_ns'])]).any():
            problems.append("the target day's prices are present")
    for key in ('h_buffer', 'b0_buffer'):
        if key in meta and any(date.fromisoformat(b['day']) > day - timedelta(days=2) for b in meta[key]):
            problems.append(f'{key}: an error day is not released under the complete D-2 rule')
    return problems


def check_emission(result: dict, day: date) -> list[str]:
    q = np.asarray(result['quantiles'], float)
    problems = []
    if result['index'] != canonical_hours(day):
        problems.append(f"the keys are not every delivery hour of {day} ({len(result['index'])} of "
                        f"{len(canonical_hours(day))})")
    if q.ndim != 2 or q.shape[1] != 7 or q.shape[0] != len(result['index']):
        problems.append('not seven quantiles per key')
    elif not np.isfinite(q).all() or (np.diff(q, axis=1) < 0).any():
        problems.append('the quantiles are not finite and ordered')
    return problems


def attempt(policy: str, fit, day: date, arrays: dict | None = None, meta: dict | None = None) -> dict:
    """One policy's fit at the day, judged by criteria 1-3; `fit()` returns the `dailyfit` result."""
    started = time.perf_counter()
    item = {'policy': policy, 'status': 'failed', 'cause': None}
    try:
        if arrays is not None and meta is not None:
            problems = check_inputs(policy, arrays, meta)
            if problems:
                item['cause'] = 'inputs: ' + '; '.join(problems)
                return item
        result = fit()
        problems = check_emission(result, day)
        if problems:
            item['cause'] = 'emission: ' + '; '.join(problems)
            item['result'] = result
            return item
        item.update(status='ok', result=result)
    except Exception as exc:     # a failed fit is recorded with its cause, never retried with other settings
        item['cause'] = f'training: {type(exc).__name__}: {exc}'
        item['traceback'] = traceback.format_exc(limit=4)
    finally:
        item['seconds'] = time.perf_counter() - started
    return item


def decide(day: date, gfs_available: bool, attempts) -> dict:
    """Walk the frozen chain. `attempts(policy)` returns `attempt(...)`'s record; it is called only for the
    policies the chain reaches, in order, so a normal day fits A1 alone."""
    record = []
    if not gfs_available:
        record.append({'policy': 'A1', 'status': 'skipped', 'cause': 'GFS late or missing at the issue time'})
        chain, reason = CHAINS['gfs_unavailable'], 'gfs_unavailable'
    else:
        first = attempts('A1')
        record.append(first)
        if first['status'] == 'ok':
            return {'day': str(day), 'issued_policy': 'A1', 'route': 'designated', 'attempts': record,
                    'display': 'successful daily fit'}
        chain, reason = CHAINS['a1_failed'], 'a1_failed'
    for policy in chain:
        item = attempts(policy)
        record.append(item)
        if item['status'] == 'ok':
            head = 'skipped fit (GFS late or missing)' if reason == 'gfs_unavailable' else 'failed fit'
            return {'day': str(day), 'issued_policy': policy, 'route': reason, 'attempts': record,
                    'display': f'{head}; fallback {policy} issued'}
    return {'day': str(day), 'issued_policy': None, 'route': reason, 'attempts': record, 'display': 'failed issuance'}


def resources_ok(wall_seconds: float, peak_bytes: int) -> list[str]:
    problems = []
    if wall_seconds > WALL_LIMIT_SECONDS:
        problems.append(f'wall time {wall_seconds:.0f} s over the 15-minute ceiling')
    if peak_bytes > MEMORY_LIMIT_BYTES:
        problems.append(f'peak memory {peak_bytes} bytes over the 4 GB ceiling')
    return problems


def artifact(decision: dict, *, identity: dict, payloads: dict, parent_sha256: str | None, data_refresh_utc: str,
             host: dict, wall_seconds: float, peak_bytes: int) -> dict:
    """The issued artifact (criterion 4), with criterion 5 applied: over the ceiling, the designated fit fails."""
    day = date.fromisoformat(decision['day'])
    issued = next((a for a in decision['attempts'] if a.get('policy') == decision['issued_policy']), None)
    over = resources_ok(wall_seconds, peak_bytes)
    if over and decision['issued_policy'] == 'A1':
        decision = {**decision, 'display': 'failed fit (resources)', 'resource_failure': over}
    result = issued['result'] if issued else None
    attempts = [{k: v for k, v in a.items() if k not in ('result', 'traceback')} for a in decision['attempts']]
    body = {
        'schema': SCHEMA, 'product': PRODUCT, 'designated_policy': DESIGNATED, 'delivery_day': str(day),
        'issue_utc': issue_utc(day), 'issued_policy': decision['issued_policy'], 'route': decision['route'],
        'display': decision['display'], 'attempts': attempts, 'resource_check': over,
        'keys': result['index'] if result else None, 'quantiles': result['quantiles'] if result else None,
        'quantiles_sha256': result['quantiles_sha256'] if result else None,
        'times': {'last_training_utc': issue_utc(day), 'data_refresh_utc': data_refresh_utc, 'issuance_utc': issue_utc(day)},
        'lineage': {'parent_artifact_sha256': parent_sha256, 'policy_identity_sha256': identity.get('policy_identity_sha256'),
                    'code_sha256': identity.get('package_sha256'), 'host': host,
                    'inputs': {p: payloads[p].get('payload_sha256') for p in payloads},
                    'training': _training(result) if result else None,
                    'state': _state(result) if result else None},
        'resources': {'wall_seconds': wall_seconds, 'peak_bytes': peak_bytes, 'limits': {
            'wall_seconds': WALL_LIMIT_SECONDS, 'peak_bytes': MEMORY_LIMIT_BYTES}}}
    body['artifact_sha256'] = hashlib.sha256(canonical(body)).hexdigest()
    return body


def _training(result: dict) -> dict:
    if result['policy'] == 'A1':
        return {'search': result['search'], 'ensemble_content_sha256': result['ensemble_content_sha256'],
                'seeds': [m['seed'] for m in result['members']],
                'members': [{k: m[k] for k in ('member', 'seed', 'train_days_sha256', 'holdout_days_sha256',
                                               'latest_training_day', 'params_sha256')} for m in result['members']]}
    if result['policy'] in ('v2', 'v4'):
        return {'train_rows': result['train_rows'], 'seeds': {'lear': None, 'lightgbm_random_state': 42}}
    return {'source_day': result.get('source_day')}


def _state(result: dict) -> dict | None:
    return result.get('h_layer') or result.get('b0_layer')


def verify_artifact(item: dict) -> list[str]:
    """The artifact's own identity; its keys and quantiles; its timestamps. Empty when it verifies."""
    problems = []
    body = {k: v for k, v in item.items() if k != 'artifact_sha256'}
    if hashlib.sha256(canonical(body)).hexdigest() != item.get('artifact_sha256'):
        problems.append('artifact identity differs')
    if item.get('issued_policy') is not None:
        q = np.asarray(item['quantiles'], float)
        if q.shape != (len(item['keys']), 7) or array_hash(q) != item['quantiles_sha256']:
            problems.append('quantiles differ from their recorded hash')
    if item.get('issue_utc') != issue_utc(date.fromisoformat(item['delivery_day'])):
        problems.append('the issue time is not D-1 11:00 Europe/Berlin')
    return problems
