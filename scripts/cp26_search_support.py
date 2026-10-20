"""Replayable r14 support-only audit: 14 search dates x 3 routes; zero fits/scores."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time


def main() -> int:
    began = time.time()
    if not os.environ.get('CP26_MONITORED_JOB'):
        raise RuntimeError('row-count audit requires the cumulative CP-26 resource monitor')
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lead', required=True, type=Path)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    lead = args.lead.resolve()
    output = args.output.resolve()
    allowed = lead / 'reports/rebaseline/repair-v21-r14'
    if not output.is_relative_to(allowed):
        raise ValueError('r14 output must be under reports/rebaseline/repair-v21-r14; historical evidence is immutable')
    for name in ('OPENBLAS_NUM_THREADS', 'VECLIB_MAXIMUM_THREADS', 'OMP_NUM_THREADS',
                 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
        if os.environ.get(name) != '1':
            raise RuntimeError(f'{name} must be 1 before numerical imports')
    sys.path.insert(0, str(lead / 'src'))
    from cp26 import harness as H
    from cp26 import search as S
    from cp24 import design as G
    from cp24 import sampler as SP

    inputs = H.identities(lead)
    H.landed_code(lead)
    designs = {route: H.weather_design(lead, H.GFS6 if route == 'gfs6' else H.NEW) for route in S.ROUTES}
    result = {'schema': 'cp26-search-support-row-count-audit-v2', 'protocol': S.PROTOCOL,
              'started_epoch_seconds': began,
              'started_utc': datetime.fromtimestamp(began, timezone.utc).isoformat(),
              'activity': 'landed target/support mask and all-choice whole-week extrema only; no fits or scores',
              'inputs_sha256': inputs,
              'code_sha256': {name: hashlib.sha256((lead / name).read_bytes()).hexdigest()
                              for name in ('scripts/cp26_search_support.py', 'src/cp26/search.py',
                                           'src/cp24/design.py', 'src/cp24/sampler.py')},
              'search_schedule': {'S_k': '2020-01-15 + 182*k days', 'k': '0..13',
                                  'S_13': str(S.search_day(13)), 'S_14_protocol_only': str(S.search_day(14))},
              'sampler_seed': 'SeedSequence([26,k,0x5A3])',
              'trial_fit_seed': '26_000_000+k*100_000+trial*100+batch; trial=0..127,batch=0..10',
              'ensemble_member_seed': '26_000_000+k*100_000+90_000+10*rank+repeat; rank=1..4,repeat=1..2',
              'minimum_train_days': G.MIN_TRAIN_DAYS, 'minimum_hold_days': G.MIN_HOLD_DAYS,
              'searches': []}
    for k in range(S.SEARCH_COUNT):
        day = S.search_day(k)
        # Filter before materialisation: no delivery day dated S_k or later is read.
        data = H.load(lead, H.NEW, before=day)
        if data.frame.delivery_date.max() >= day or data.frame.delivery_date.max() > H.NEW_BOUNDARY:
            raise RuntimeError('support audit read outside its training-only cutoff')
        for route in S.ROUTES:
            # noload changes fit inputs, not the landed support mask/statistics. GFS6
            # preserves missing-weather records; NaN columns are imputed at fit time.
            dd = G.build(data, designs[route])
            support = S.batch_support(dd, k)
            actual_support = dd.days[dd.mask.any(axis=1)]
            item = {**support, 'route': route,
                    'loaded_first': str(data.frame.delivery_date.min()),
                    'loaded_last': str(data.frame.delivery_date.max()),
                    'first_day_with_eligible_target': str(actual_support[0]) if actual_support.size else None,
                    'calendar_days_in_table': int(len(dd.days)),
                    'eligible_target_days': int(dd.mask.any(axis=1).sum()),
                    'weather_design_sha256': designs[route].sha256,
                    'support_freeze_sha256': support['content_sha256']}
            # These registered-seed checks happen after support is signed and never
            # determine eligibility. No fitting, convergence or loss is inspected.
            verification = []
            for batch in support['batches']:
                b = datetime.fromisoformat(batch['first']).date()
                lower, ix, _ = G.window(dd, b, exclude_uncovered=True)
                observed = []
                for trial in range(S.TRIALS):
                    weeks, pool = G.holdout_weeks(dd, lower, b, S.trial_fit_seed(k, trial, batch['batch']))
                    tr, ho = G.split(dd, ix, weeks)
                    observed.append((len(tr), len(ho)))
                    if pool != batch['whole_week_pool'] or len(weeks) != batch['selected_heldout_weeks'] \
                            or len(tr) < G.MIN_TRAIN_DAYS or len(ho) < G.MIN_HOLD_DAYS:
                        raise RuntimeError('registered seed violates all-choice support admission')
                verification.append({'batch': batch['batch'], 'registered_seeds_checked': S.TRIALS,
                                     'minimum_observed_train_days': min(t for t, h in observed),
                                     'minimum_observed_hold_days': min(h for t, h in observed),
                                     'selection_basis': 'support-only extrema; seed minima never select a batch'})
            item['registered_seed_support_checks'] = verification
            item['content_sha256'] = S.digest(item)
            result['searches'].append(item)
    result['B_by_route'] = {route: [s['B'] for s in result['searches'] if s['route'] == route] for route in S.ROUTES}
    expected = [1, 7] + [11] * 12
    # Algorithms and masks are authoritative; a mismatch is evidence to report.
    result['reported_B_reproduced'] = all(counts == expected for counts in result['B_by_route'].values())
    first = next(s for s in result['searches'] if s['k'] == 0 and s['route'] == 'nominal')
    result['first_window_reported_251_46_reproduced'] = bool(first['B'] and
        first['batches'][0]['minimum_possible_train_days'] == 251 and
        first['batches'][0]['minimum_possible_hold_days'] == 46)
    result['search_fit_counts_at_full_success'] = {
        route: sum(S.TRIALS * min(SP.HALVING_BATCHES, n)
                   + (SP.halving_survivors(S.TRIALS) * (n - SP.HALVING_BATCHES) if n > SP.HALVING_BATCHES else 0)
                   for n in counts) for route, counts in result['B_by_route'].items()}
    result['search_count_for_future_pilot_cost'] = S.SEARCH_COUNT * len(S.ROUTES)
    ended = time.time()
    result.update(ended_epoch_seconds=ended, ended_utc=datetime.fromtimestamp(ended, timezone.utc).isoformat(),
                  wall_seconds=ended - began)
    result['content_sha256'] = S.digest(result)
    S._atomic(output, result)
    md = output.with_suffix('.md')
    lines = ['# CP-26 r14 support audit', '',
             'This reconstruction uses the landed mask and whole-week rule. '
             'No training, forecast replay or CP-26 score was computed.', '',
             f"JSON SHA-256: `{hashlib.sha256(output.read_bytes()).hexdigest()}`.", '',
             '| Route | Retained batch counts k=0..13 |', '|---|---|']
    lines.extend(f"| {route} | {result['B_by_route'][route]} |" for route in S.ROUTES)
    lines += ['', '| Search k | Date | Route | B | Newest retained batch | min train / min hold |',
              '|---:|---|---|---:|---|---|']
    for item in result['searches']:
        b = item['batches'][0] if item['B'] else None
        bounds = f"{b['minimum_possible_train_days']} / {b['minimum_possible_hold_days']}" if b else 'none'
        lines.append(f"| {item['k']} | {item['search_day']} | {item['route']} | {item['B']} | "
                     f"{b['first'] if b else 'none'} | {bounds} |")
    lines += ['', 'Admission is min(train) = N minus support of the m heaviest complete weeks; '
              'min(hold) = support of the m lightest. The pool excludes the most recent seven days.', '',
              f"The reported B vector reproduces: {result['reported_B_reproduced']}. "
              f"First-window 251/46 reproduces: {result['first_window_reported_251_46_reproduced']}.", '',
              f"The future pilot must price all {result['search_count_for_future_pilot_cost']} searches, "
              f"up to {sum(result['search_fit_counts_at_full_success'].values())} trial/batch fits "
              '(excluding daily member fits, failed work and reproduction).', '',
              'Reproduce under the cumulative monitor:', '', '```sh',
              'python scripts/cp26_rebaseline.py monitor --name repair-r14-support --workers 1 -- '
              'python scripts/cp26_search_support.py --lead "$PWD" '
              '--output "$PWD/reports/rebaseline/repair-v21-r14/search-support.json"', '```', '']
    md.write_text('\n'.join(lines))
    print(json.dumps({'result': str(output), 'wall_seconds': result['wall_seconds'],
                      'B_by_route': result['B_by_route'], 'search_count': len(result['searches']),
                      'first_window_251_46': result['first_window_reported_251_46_reproduced'],
                      'model_fits': 0, 'experiment_scores': 0}))
    return 0 if result['reported_B_reproduced'] and result['first_window_reported_251_46_reproduced'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
