"""One-off restart-test harness: SIGTERM the extraction monitor after 5 completed runs (max 30 min)."""
import os, signal, sys, time, json
from pathlib import Path
runs = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/weather/runs')
pid = int(sys.argv[1]); t0 = time.time()
while time.time() - t0 < 1800:
    done = [p for p in runs.glob('*.json') if json.loads(p.read_text()).get('status') == 'complete']
    if len(done) >= 5:
        os.kill(pid, signal.SIGTERM)
        print('SIGTERM sent after', len(done), 'complete runs', sorted(p.stem for p in done), round(time.time()-t0), 's'); break
    try: os.kill(pid, 0)
    except ProcessLookupError: print('monitor exited before trigger'); break
    time.sleep(5)
