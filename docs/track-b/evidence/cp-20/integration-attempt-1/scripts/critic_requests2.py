import json, collections
A = '/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/weather/requests.jsonl'
mx = 0; kinds = collections.Counter(); mxb = collections.defaultdict(int)
for line in open(A):
    r = json.loads(line)
    if r['range'] is None:
        u = r['url']; k = 'idx' if u.endswith('.idx') else ('listing' if u.endswith('/') or '?' in u or 'catalog' in u else 'other')
        kinds[k] += 1; mxb[k] = max(mxb[k], r.get('body_bytes') or 0)
    else:
        mxb['ranged'] = max(mxb['ranged'], r.get('body_bytes') or 0)
print(json.dumps({'unranged_kinds': dict(kinds), 'max_body_bytes': dict(mxb)}))
