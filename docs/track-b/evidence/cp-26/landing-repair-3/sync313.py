"""Only network-allowed operation: populate the project-local cache from the lock."""
import importlib.util,json,sys
from pathlib import Path
OUT=Path('/Users/djourno/Downloads/PJM/.local/tmp/cp-26-landing-repair-3');CLEAN=OUT/'final-check'
p=CLEAN/'docs/track-b/evidence/cp-26/landing-repair-2/stress_check.py'
spec=importlib.util.spec_from_file_location('round2',p);R=importlib.util.module_from_spec(spec);spec.loader.exec_module(R)
env=R.environment(OUT/'env-sync313','3.13');env['UV_OFFLINE']='0'
result=R.run_logged(['uv','sync','--locked','--dev'],OUT/'prepared/copy313',env,OUT/'results/sync313.log')
result['network_scope']='uv sync --locked --dev only; Python downloads disabled; cache inside project'
(OUT/'sync313.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
sys.exit(result['exit_code'])
