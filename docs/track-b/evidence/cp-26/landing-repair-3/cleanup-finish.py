"""Finish the owned temp-root removal after a Finder .DS_Store creation race."""
from pathlib import Path
import json
import shutil
import subprocess
import time

ROOT = Path('/Users/djourno/Downloads/PJM')
LEAD = ROOT / '.local/worktrees/cp-26/lead'
OUT = ROOT / '.local/tmp/cp-26-landing-repair-3'
ART = ROOT / '.local/artifacts/cp-26-landing-repair-3'
D = LEAD / 'docs/track-b/evidence/cp-26/landing-repair-3'


def git(*args, cwd=LEAD):
    return subprocess.check_output(['git', '--no-pager', *args], cwd=cwd, text=True)


r = json.loads((D / 'cleanup.json').read_text())
assert len(r['commands']) == 2 and all(c['exit_code'] == 0 for c in r['commands'])
assert r['barrier_removed'] and str(OUT) not in git('worktree', 'list', '--porcelain')
r['initial_cleanup_error'] = {
    'type': 'OSError', 'errno': 66, 'reason': 'Directory not empty',
    'path': str(OUT / 'env-full/lib/python3.12/site-packages'),
    'observed_remaining_entry': '.DS_Store',
    'verification_processes_remaining': False,
}
for attempt in range(5):
    try:
        if OUT.exists():
            shutil.rmtree(OUT)
        break
    except OSError:
        if attempt == 4:
            raise
        time.sleep(0.2)
r['temporary_root_removed'] = not OUT.exists()
assert r['temporary_root_removed']
r['worktrees_after'] = git('worktree', 'list', '--porcelain')
r['main'] = git('rev-parse', 'main').strip()
r['origin_main'] = git('rev-parse', 'origin/main').strip()
r['main_index'] = git('diff', '--cached', '--name-only', cwd=ROOT).splitlines()
r['main_worktree_status'] = git('status', '--porcelain=v1', cwd=ROOT).splitlines()
r['lead_tracked_status'] = git('status', '--porcelain=v1', '--untracked-files=no').splitlines()
assert r['main'] == r['origin_main'] == '647d6eb81b2cf6e0cfaf4152f659d689ff973578'
assert not r['main_index'] and not r['lead_tracked_status']
r['secret_hooks_path'] = git('config', '--get', 'core.hooksPath').strip()
assert r['secret_hooks_path'] == str(ROOT / '.githooks')
r['retained_recovery'] = str(ART)
r['complete'] = True
r['finished_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
for p in (D / 'cleanup.json', ART / 'cleanup.json'):
    p.write_text(json.dumps(r, indent=2) + '\n')
print(json.dumps(r))
