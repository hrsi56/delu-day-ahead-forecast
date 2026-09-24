import json, collections
from urllib.parse import urlparse
A = '/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/weather/requests.jsonl'
n = 0; maxb = 0; norange = 0; hosts = collections.Counter(); tot = 0; keys = set()
for line in open(A):
    r = json.loads(line); n += 1; keys |= set(r)
    br = r.get('byte_range') or r.get('range')
    b = r.get('bytes') or r.get('received_bytes') or r.get('charged_bytes') or 0
    tot += b or 0
    if br is None: norange += 1
    else:
        maxb = max(maxb, br[1] - br[0] + 1)
    hosts[urlparse(r.get('url', '')).netloc] += 1
print(json.dumps({'requests': n, 'max_range_bytes': maxb, 'requests_without_range': norange, 'hosts': dict(hosts), 'keys': sorted(keys)}))
