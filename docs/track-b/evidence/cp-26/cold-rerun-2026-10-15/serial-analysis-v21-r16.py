"""Run the four existing CP-26 analysis jobs in their original serial order.

This is one supervised worker, with no pool, retry or scientific override.
Each original job retains its complete-ledger gate and durable outputs.
"""
from pathlib import Path
import hashlib
import json
import os
import runpy
import subprocess
import sys
import time


def main():
    root = Path.cwd().resolve()
    own = Path(__file__).resolve()
    relative = str(own.relative_to(root))
    raw = own.read_bytes()
    if subprocess.check_output(['git', 'show', f'HEAD:{relative}'], cwd=root) != raw:
        raise RuntimeError('serial analysis entry point must be committed')
    if len(sys.argv) != 1 or not os.environ.get('CP26_MONITORED_JOB'):
        raise RuntimeError('serial analysis requires one registered supervised worker')
    entry = root / 'scripts/cp26_rebaseline.py'
    original_args = sys.argv
    try:
        for stage in ('scores', 'inference', 'diagnostics', 'report'):
            began = time.monotonic()
            print(json.dumps({'status': 'SERIAL_ANALYSIS_STAGE_BEGIN', 'stage': stage,
                              'entry_point_sha256': hashlib.sha256(raw).hexdigest()}), flush=True)
            sys.argv = [str(entry), 'job', stage]
            try:
                runpy.run_path(str(entry), run_name='__main__')
            except SystemExit as exc:
                if exc.code not in (None, 0):
                    raise
            if own.read_bytes() != raw:
                raise RuntimeError('serial analysis entry point changed during execution')
            print(json.dumps({'status': 'SERIAL_ANALYSIS_STAGE_COMPLETE', 'stage': stage,
                              'wall_seconds': time.monotonic() - began}), flush=True)
    finally:
        sys.argv = original_args


if __name__ == '__main__':
    main()
