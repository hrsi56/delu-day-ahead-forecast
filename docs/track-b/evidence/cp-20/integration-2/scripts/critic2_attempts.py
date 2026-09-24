"""CP-20 Integration Critic 2 -- per-message attempt accounting and request-log checks (log reads only)."""
from __future__ import annotations

import collections
import json
from pathlib import Path

ART = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20')
W = ART / 'weather'
OUT = ART / 'critic-2/out'
res = {}
outcomes = [json.loads(l) for l in (W / 'attempt-outcomes.jsonl').read_text().splitlines() if l.strip()]
restored = {(r['try_id'], r['run'], r['lead'], r['field']) for r in
            (json.loads(l) for l in (W / 'o2-a1-restored-attempts.jsonl').read_text().splitlines() if l.strip())}
res['outcome_counts'] = collections.Counter(o['outcome'] for o in outcomes)
res['counted_flag_counts'] = collections.Counter(bool(o.get('counted')) for o in outcomes)
tries_all = collections.Counter()
tries_counted = collections.Counter()
tries_response = collections.Counter()   # every try that received a response (success + counted failure kinds)
for o in outcomes:
    key = (o['run'], o['lead'], o['field'])
    tries_all[key] += 1
    is_restored = (o.get('try_id'), o['run'], o['lead'], o['field']) in restored
    if o.get('counted') and not is_restored:
        tries_counted[key] += 1
    if o['outcome'] in ('success', 'validation_failure', 'integrity_failure', 'object_failure'):
        tries_response[key] += 1
succ = collections.Counter((o['run'], o['lead'], o['field']) for o in outcomes if o['outcome'] == 'success')
res['messages_with_outcomes'] = len(tries_all)
res['messages_with_success'] = len(succ)
res['max_success_per_message'] = max(succ.values())
res['dist_all_tries'] = dict(sorted(collections.Counter(tries_all.values()).items()))
res['dist_counted_failures_O2_O2A1'] = dict(sorted(collections.Counter(tries_counted.values()).items()))
res['dist_response_tries'] = dict(sorted(collections.Counter(tries_response.values()).items()))
# retained raw messages: prior review decode (attempt 1) and this review's decode
raw = sorted(p for p in (W / 'raw').rglob('*.grib2'))
eligible = {l.strip() for l in (ART / 'critic-2/eligible-decodes.txt').read_text().splitlines() if l.strip()}
prior = {Path(l.split()[-1]).name for l in []}
per = []
for p in raw:
    lead = int(p.name[1:4])
    field = p.name[5:-6].rsplit('_', 1)[0]
    key = (p.parent.name, lead, field)
    mine = 1 if str(p) in eligible else 0
    per.append({'msg': f'{key}', 'all_tries': tries_all[key], 'response_tries': tries_response[key], 'counted': tries_counted[key],
                'prior_review_decode': 1, 'this_review_decode': mine})
res['retained_messages'] = len(per)
res['retained_eligible'] = sum(r['this_review_decode'] for r in per)
res['retained_max_response_tries_plus_reviews'] = max(r['response_tries'] + r['prior_review_decode'] + r['this_review_decode'] for r in per)
res['retained_max_all_tries_plus_reviews'] = max(r['all_tries'] + r['prior_review_decode'] + r['this_review_decode'] for r in per)
res['retained_over3_response_basis'] = [r for r in per if r['response_tries'] + 2 > 3 and r['this_review_decode']][:5]
res['excluded_are_those_with_2_response_tries'] = all((r['response_tries'] + 1 >= 3) == (r['this_review_decode'] == 0) for r in per)
res['excluded_dist'] = dict((str(k), v) for k, v in collections.Counter((r['response_tries'], r['all_tries']) for r in per if not r['this_review_decode']).items())
res['eligible_dist'] = dict((str(k), v) for k, v in collections.Counter((r['response_tries'], r['all_tries']) for r in per if r['this_review_decode']).items())
over = [(k, v) for k, v in tries_all.items() if v > 3]
res['messages_over_3_all_tries'] = len(over)
res['messages_over_3_all_tries_examples'] = [(str(k), v, tries_response[k], tries_counted[k]) for k, v in over[:10]]
res['messages_over_3_response_tries'] = sum(1 for v in tries_response.values() if v > 3)
res['messages_over_2_counted_failures'] = sum(1 for v in tries_counted.values() if v > 2)
# requests: hosts, largest bodies, unranged requests
hosts, big, unranged, n = collections.Counter(), 0, collections.Counter(), 0
big_unranged, statuses = 0, collections.Counter()
for line in (W / 'requests.jsonl').open():
    r = json.loads(line)
    n += 1
    url = r.get('url', '')
    hosts[url.split('/')[2] if '//' in url else '?'] += 1
    nbytes = r.get('body_bytes') or 0
    big = max(big, nbytes)
    statuses[r.get('status')] += 1
    if r.get('range') is None:
        base = url.rstrip('/').rsplit('/', 1)[-1]
        kind = 'idx' if base.endswith('.idx') else ('listing' if ('?' in url or url.endswith('/') or 'catalog' in url) else base[-12:])
        unranged[kind] += 1
        big_unranged = max(big_unranged, nbytes) if kind in ('idx', 'listing') else big_unranged
        if kind not in ('idx', 'listing'):
            unranged['nonidx_max_bytes'] = max(unranged['nonidx_max_bytes'], nbytes)
res['largest_unranged_idx_or_listing_bytes'] = big_unranged
res['status_counts'] = dict(statuses.most_common(12))
res['requests'] = n
res['request_hosts'] = hosts
res['largest_request_bytes'] = big
res['unranged_by_suffix'] = dict(unranged.most_common(10))
res['request_keys_example'] = list(json.loads(open(W / 'requests.jsonl').readline()).keys())
OUT.mkdir(parents=True, exist_ok=True)
(OUT / 'attempts.json').write_text(json.dumps(res, indent=1, default=str))
print(json.dumps(res, indent=1, default=str)[:4000])
