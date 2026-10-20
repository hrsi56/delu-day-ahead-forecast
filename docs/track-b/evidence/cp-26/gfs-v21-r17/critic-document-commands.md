## Bounded document helper — exact actual commands

All commands ran in `/Users/djourno/Downloads/PJM/.local/worktrees/cp-26/critic-gfs-r17`.

The system-Python probe below exited **1**, after matching all document hashes and frozen-protocol bytes, with `ModuleNotFoundError: No module named 'pyarrow'`. No candidate error or scientific retry occurred; no package was installed.

```sh
python3 - <<'PY'
from pathlib import Path
import hashlib, json, subprocess
base='252725e0431826b6d32f1fc8200cfa3baf3750f6'
validation=json.loads(Path('docs/track-b/evidence/cp-26/gfs-v21-r17/document-validation.json').read_text())
for path, expected in validation['documents'].items():
    observed=hashlib.sha256(Path(path).read_bytes()).hexdigest()
    print(f'{path}: sha256={observed}; validation_match={observed==expected}')
protocol='docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md'
current=Path(protocol).read_bytes()
prior=subprocess.run(['git','show',f'{base}:{protocol}'],check=True,capture_output=True).stdout
print(f'frozen_protocol: sha256={hashlib.sha256(current).hexdigest()}; base_bytes_equal={current==prior}')
import pyarrow.parquet as pq
path='reports/rebaseline/cold-rerun-2026-10-15/scores/summaries.parquet'
table=pq.read_table(path)
print('score_summary_schema:',table.schema)
for row in table.to_pylist():
    if row.get('mask') == 'all_eligible' and row.get('policy') in ('nominal/v4','gfs6/v4','nominal/v5','gfs6/v5'):
        print(row)
PY
```

Existing-environment schema inspection exited **0**:

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python -B - <<'PY'
import pyarrow.parquet as pq
path='reports/rebaseline/cold-rerun-2026-10-15/scores/summaries.parquet'
t=pq.read_table(path)
print('path:',path)
print('schema:', t.schema)
print('rows:',t.num_rows)
print('first_row:',t.slice(0,1).to_pylist())
PY
```

Stored-row inspection and scalar ratios exited **0**. The eight selected all-eligible overall rows each have 2,068 available/paired dates and zero missing pairs. Output ratios, in v4 MAE/WIS and v5 MAE/WIS order: **16.0888767935%, 17.4103737187%, 13.9851417997%, 15.4587716202%**. These are arithmetic from existing summaries, not a new experiment or inferred robustness difference.

```sh
/Users/djourno/Downloads/PJM/.venv/bin/python -B - <<'PY'
import pyarrow.parquet as pq
rows=pq.read_table('reports/rebaseline/cold-rerun-2026-10-15/scores/summaries.parquet').to_pylist()
selected={}
for r in rows:
    if r['mask']=='all_eligible' and r['group']=='overall' and r['stream'] in ('nominal/v4','gfs6/v4','nominal/v5','gfs6/v5'):
        selected[(r['stream'],r['metric'])]=r
        print({k:r[k] for k in ('mask','stream','metric','group','value','raw_mean_daily_loss','raw_available_dates','paired_dates','left_missing_dates','right_missing_dates','row_id')})
for policy in ('v4','v5'):
    for metric in ('MAE','WIS'):
        n=selected[(f'nominal/{policy}',metric)]['raw_mean_daily_loss']
        s=selected[(f'gfs6/{policy}',metric)]['raw_mean_daily_loss']
        print(f'{policy} {metric}: 100*(stored_gfs6_mean/stored_nominal_mean-1)={100*(s/n-1):.10f}%')
PY
```
