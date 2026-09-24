import json, collections
from pathlib import Path
ROOT = Path.cwd(); A = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/weather')
out = {}
eps = collections.defaultdict(set); alt_ok = []
rm = {r['run_00z']: r for r in json.loads((ROOT / 'reports/weather-ablation/run-manifest.json').read_text())['runs']}
for line in open(A / 'attempt-outcomes.jsonl'):
    r = json.loads(line); eps[(r['run'], r['lead'], r['field'])].add(r['endpoint'])
multi = {k: v for k, v in eps.items() if len(v) > 1}
bad_ep = [k for k, v in eps.items() if not v <= {rm[k[0]]['primary_endpoint'], rm[k[0]]['alternate_endpoint']}]
out['messages_tried_on_two_endpoints'] = len(multi)
out['messages_tried_on_unlisted_endpoint'] = len(bad_ep)
lin = json.loads((ROOT / 'reports/weather-ablation/lineage.json').read_text())
meta = {}
for o in lin['origins']:
    if o.get('predicted'):
        meta.setdefault((o['fold'], o['day']), {})[o['arm']] = (o['buffer_start'], o['buffer_end'], o['buffer_days'], o['buffer_hours'], json.dumps(o['hour_support'], sort_keys=True))
for a in lin['admission']:
    meta.setdefault((a['fold'], a['day']), {})[a['arm']] = (a['buffer_start'], a['buffer_end'], a['buffer_days'], None, json.dumps(a['hour_support'], sort_keys=True))
diff = [k for k, v in meta.items() if set(v) != {'H0', 'HG'} or (v['H0'][:3] != v['HG'][:3]) or v['H0'][4] != v['HG'][4]]
out['predicted_origins'] = len(meta); out['arm_buffer_date_or_support_differences'] = diff[:10]
srcs = collections.Counter((o['arm'], o['source']) for o in lin['origins'])
out['origin_sources'] = {f'{a}|{s}': n for (a, s), n in srcs.items()}
print(json.dumps(out, indent=1))
json.dump(out, open('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/critic/out/misc.json', 'w'), indent=1)
