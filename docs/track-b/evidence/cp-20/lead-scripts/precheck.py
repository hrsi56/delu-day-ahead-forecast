"""Lead's internal pre-review check of a candidate in a clean checkout (read-only)."""
import hashlib, json, subprocess, sys
from pathlib import Path
root = Path.cwd()
sha = lambda p: hashlib.sha256((root / p).read_bytes()).hexdigest()
p = json.loads((root / 'reports/weather-ablation/protocol.json').read_text())
m = json.loads((root / 'reports/weather-ablation/artifact-manifest.json').read_text())
bad = [(k, f) for k, d in (('frozen', p['frozen_inputs_sha256']), ('impl', p['implementation_sha256']), ('manifest', m['artifact_sha256']))
       for f, h in d.items() if sha(f) != h]
print('hash mismatches:', bad)
from cp20.execution import check_protocol
check_protocol(root); print('check_protocol: OK')
same = subprocess.run(['git', 'diff', '--quiet', 'a7943fb6262c1a50b729bd92fe701c8be9428038', 'HEAD', '--',
                       'reports/weather-ablation/protocol.json', 'reports/weather-ablation/predictions.parquet',
                       'reports/weather-ablation/metrics.csv', 'reports/weather-ablation/uncertainty.csv',
                       'reports/weather-ablation/lineage.json', 'reports/weather-ablation/criteria.csv']).returncode
print('results byte-identical to a7943fb:', same == 0)
allowed = ('src/cp20/', 'tests/cp20/', 'scripts/cp20_weather.py', 'reports/weather-ablation/', 'docs/track-b/evidence/cp-20/', 'pyproject.toml', 'uv.lock')
changed = subprocess.check_output(['git', 'diff', '--name-only', '88c68cf', 'HEAD'], text=True).split()
outside = [f for f in changed if not f.startswith(allowed)]
print('changed files vs main:', len(changed), 'outside 15.7:', outside)
sys.exit(1 if bad or same or outside else 0)
