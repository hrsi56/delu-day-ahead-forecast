from pathlib import Path
import json,hashlib
import pandas as pd
r=Path.cwd();m=json.loads((r/'reports/v2-causal/input-manifest.json').read_text());l=json.loads((r/'reports/v2-causal/lineage.json').read_text())
raw=(r/'docs/track-b/evidence/cp-16/interrupted-admission-lineage.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()==l['interrupted_original_lineage_sha256']
x=json.loads(raw)
assert all(l[k]==x[k] for k in x if k!='execution_stage')
print('raw_interrupted_prefix_preserved_except_labeled_status',True)
k=pd.read_parquet(r/'reports/cp15/predictions.parquet',columns=['fold','timestamp_utc'],filters=[('policy','==','B0')])
for f in m['folds']:
    want=pd.DatetimeIndex(k.loc[k.fold.eq(f['fold']),'timestamp_utc']).sort_values()
    got=pd.DatetimeIndex(pd.to_datetime(f['original_target_keys'],utc=True)).sort_values()
    print(f["fold"], str(got.dtype), str(want.dtype)); assert got.as_unit("ns").equals(want.as_unit("ns"))
print('all_manifest_UTC_target_keys_match_original',True)
ledger=json.loads(Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-16/budget.json').read_text())
print('current_resource_counts',ledger['counts'])
