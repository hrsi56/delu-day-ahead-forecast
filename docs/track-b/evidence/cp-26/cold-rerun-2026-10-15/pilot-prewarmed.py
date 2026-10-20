"""One registered pilot shard, with its existing ledger index prepared before fits."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / 'src'))
from cp26.budget import Budget
from cp26.gates import RUN_ID, ExecutionGate, authorize_consuming_process, protocol_identity
from cp26 import execution as E

parser = argparse.ArgumentParser()
parser.add_argument('--shard', type=int, choices=range(4))
args = parser.parse_args()
relative = str(Path(__file__).resolve().relative_to(ROOT))
if subprocess.check_output(['git', 'show', f'HEAD:{relative}']) != Path(__file__).read_bytes():
    raise RuntimeError('pilot entry point must be committed')
if os.environ.get('CP26_RUN_ID') != RUN_ID or not os.environ.get('CP26_MONITORED_JOB'):
    raise RuntimeError('registered cold-run supervision required')
authorize_consuming_process(ROOT)
budget = Budget()
# This is the same authoritative-byte cache/index the first evidence append builds.
# Prepare it before that append's unchanged bounded fresh transaction. The independent
# sampler/watchdog remain active throughout; no timer, lock deadline or cap changes.
budget._task_index_needed = True
budget.resource_read()
pairs = ([(r, k) for k in range(14) for i, r in enumerate(E.ROUTES)
          if (k * 3 + i) % 4 == args.shard] if args.shard is not None else None)
result = E.timing_pilot(ROOT, protocol_identity(ROOT), gate=ExecutionGate(ROOT),
                        pairs=pairs, budget=budget)
print(json.dumps(result if pairs is not None else {'status': 'SEALED_PILOT_COMPLETE',
                 'probes': len(result['probes']), 'summaries': len(result['summary'])}), flush=True)
