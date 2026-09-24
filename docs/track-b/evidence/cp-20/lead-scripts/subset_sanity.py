import json, glob
from datetime import date
from pathlib import Path
import pandas as pd
from cp20.weather import convert_run, load_run
from cp20.assemble import messages_table, sample_hashes
W = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/weather')
m = json.loads(Path('reports/weather-ablation/run-manifest.json').read_text())
done = sorted(p.stem for p in (W/'runs').glob('*.json'))
frames=[]
for r in m['runs']:
    if r['run_00z'] in done and json.loads((W/'runs'/f"{r['run_00z']}.json").read_text()).get('status')=='complete':
        _, data, bounds, quanta = load_run(W, r['run_00z'])
        f = convert_run(date.fromisoformat(r['delivery_day']), data, bounds, quanta); f['version']=r['version']; frames.append(f)
        print(r['run_00z'], r['version'], 'bounds', bounds[:3], 'quanta', sorted(set(round(q,5) for q in quanta)))
F = pd.concat(frames)
print(F.groupby('version')[['wx_wind10_mean','wx_wind100_mean','wx_dswrf_mean']].describe().T.round(2).to_string())
print(F.status.value_counts().to_dict(), 'clipped cells', int(F.dswrf_clipped_cells.sum()), 'min block', F.dswrf_min_block.min())
msgs, runs = messages_table(W, {'runs':[r for r in m['runs'] if r['run_00z'] in done]})
s = sample_hashes(msgs, Path('reports/weather-admission'))
print('sample hash comparisons', len(s), 'identical', int(s.identical.sum()) if len(s) else 0)
print(msgs.groupby(['version','field']).packing_quantum.agg(['min','max']).to_string())
