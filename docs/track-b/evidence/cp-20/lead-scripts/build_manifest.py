import json, sys
from pathlib import Path
from cp20.plan import build
from cp20.budget import atomic
root = Path.cwd()
m = build(root, Path('/Users/djourno/Downloads/PJM/.local/weather-admission/cache/gfs_inventory'))
atomic(root / 'reports/weather-ablation/run-manifest.json', m)
from collections import Counter
print(m['required_runs'], m['target_messages'], m['structural_missing'], len(m['availability_not_bracketed']), m['availability_not_bracketed'][:5])
print(Counter((r['version'], r['primary_endpoint'], r['alternate_endpoint']) for r in m['runs']))
print([ (r['run_00z'], r['availability']['capture_before'], r['availability']['capture_after']) for r in m['runs'] if not r['admission']['inventoried']])
print(sum(r['retain_raw'] for r in m['runs']), sum(r['subset'] for r in m['runs']))
missing_sizes=[r['run_00z'] for r in m['runs'] if r['primary_endpoint']=='ncar' and any(v['ncar'] is None for v in r['object_bytes'].values())]
print('ncar primary without exact size', missing_sizes)
