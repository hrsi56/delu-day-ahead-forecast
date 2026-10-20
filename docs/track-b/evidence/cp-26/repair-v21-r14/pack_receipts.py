"""Preserve repair compute receipts/logs and original-output custody, without resetting anything."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil


def main():
    if not os.environ.get('CP26_MONITORED_JOB'):
        raise RuntimeError('receipt packaging requires the resource monitor')
    p = argparse.ArgumentParser()
    p.add_argument('--lead', type=Path, required=True)
    args = p.parse_args()
    lead = args.lead.resolve()
    evidence = lead / 'docs/track-b/evidence/cp-26/repair-v21-r14'
    art = Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-26')
    ledger = json.loads((art / 'ledger/budget.json').read_text())
    rows = []
    for job in ledger['jobs']:
        if not job['name'].startswith('repair-r14-') or job['running']:
            continue
        dest = evidence / 'runs' / job['name']
        dest.mkdir(parents=True, exist_ok=True)
        files = [Path(job['log']), art / 'jobs' / (job['name'] + '.json')]
        files += [Path(job[key]) for key in ('request', 'progress_clock', 'completion_clock') if job.get(key)]
        copied = {}
        for source in files:
            if not source.resolve().is_relative_to(art.resolve()):
                raise ValueError('receipt outside project artifacts')
            if source.exists():
                target = dest / source.name
                shutil.copy2(source, target)
                copied[str(target.relative_to(lead))] = hashlib.sha256(target.read_bytes()).hexdigest()
        rows.append({'name': job['name'], 'workers': job['workers'],
                     'wall_seconds': job['wall_seconds'], 'machine_seconds': job['wall_seconds'] * job['workers'],
                     'exit_code': job['exit_code'], 'abort_reason': job['abort_reason'], 'files_sha256': copied})
    originals = ['capstone_v21.md', 'reports/rebaseline/parity.json', 'reports/rebaseline/harness-log.json',
                 'scripts/cp26_rebaseline.py', 'tests/test_cp26_monitor.py']
    prior = {}
    for name in originals:
        saved = evidence / 'preserved-r13' / name
        prior[name] = {'preserved_path': str(saved.relative_to(lead)),
                       'sha256': hashlib.sha256(saved.read_bytes()).hexdigest()}
    (evidence / 'run-receipts.json').write_text(json.dumps({'schema': 'cp26-repair-run-receipts-v1',
        'completed_runs': rows, 'original_outputs_preserved': prior,
        'rule': 'only ended jobs are packaged; later terminal packaging includes review and archive costs'}, indent=2) + '\n')
    print(json.dumps({'completed_runs_packaged': len(rows), 'fits_beyond_old_parity': 0, 'experimental_scores': 0}))


if __name__ == '__main__':
    main()
