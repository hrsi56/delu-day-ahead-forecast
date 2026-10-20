"""Produce reviewable diffs and a per-file inventory for a fixed repair candidate.

Run through the cumulative monitor. This writes only repair evidence/reports and
does not mutate Git or any programme-state document.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

START = '5cc3cc083c4340fd8d792eeaf6551a007987a877'
MAIN = '647d6eb81b2cf6e0cfaf4152f659d689ff973578'


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def reason(name):
    exact = {
        'capstone_v21.md': 'Owner-authorized candidate r14: support-only search phase, native recovery, eligibility and continuation dates.',
        'docs/track-b/capstone_v21-r13-to-v21-r14-amendments.md': 'Record exact bounded amendment, provenance, pending ratification and retained research rules.',
        'scripts/cp26_rebaseline.py': 'Preserve inherited work; supervise resource-accounted jobs and reconcile resumptions without idle charges.',
        'scripts/cp26_search_support.py': 'Reproduce all 42 support schedules without model training or experimental scores.',
        'scripts/cp26_repair_manifest.py': 'Build non-circular version/supersession identities after the anchor-only commit.',
        'src/cp26/search.py': 'Qualified signed support windows, fixed sampler/halving/seeds, effective diversity, strict ensemble and search cache.',
        'src/cp26/state.py': 'Separate native/interval/output/full-error eligibility, D-2 recovery, historical scales and persistent isolated buffers/ledger.',
        'src/cp26/replay.py': 'Chronological synthetic replay adapters and route-specific persistent state with immutable measured outputs.',
        'src/cp26/fits.py': 'Fresh native fit adapters and signed per-origin cache lineage, including failed fits.',
        'src/cp26/members.py': 'Route production D2 through verified CP26 ensembles; strict eight members; retain old-settings parity fixtures.',
        'src/cp26/harness.py': 'Pin candidate anchor, new active protocols/manifest, while keeping landed-code baseline fixed.',
        'src/cp26/budget.py': 'Classify measured/reported/reserved expense, preserve history, enforce repair/cumulative limits and price all 42 future searches.',
        'src/cp26/supervisor.py': 'Independent completion/worker identity accounting, safe bound termination, fail-closed uncertain endings and worker ceilings.',
        'reports/rebaseline/parity.json': '96 current old-settings parity comparisons; original output preserved before replacement.',
        'reports/rebaseline/harness-log.json': 'Current input/pin/base verification; original log preserved before replacement.',
        'docs/track-b/evidence/cp-26/issued-repair-brief-v21-r14.md': 'Active bounded repair contract with supersession; original issued brief remains unchanged.',
        'docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md': 'Candidate registration of native arm errors and separate learning ledger; original protocol retained; no arms executed.',
    }
    if name in exact:
        return exact[name]
    if name.startswith('tests/test_cp26_'):
        return 'Focused synthetic regression/contract acceptance evidence for the bounded repair.'
    if '/runs/' in name:
        return 'Preserve exact monitored argv, completion/progress evidence, outcome or log, including failed checks.'
    if '/preserved-r13/' in name or name.endswith(('initial-inventory.json', 'inherited-uncommitted.patch')):
        return 'Byte-exact custody of prior anchor/output and inherited uncommitted material.'
    if name.startswith('reports/rebaseline/repair-v21-r14/search-support.'):
        return 'Support-only exhaustive week extrema and signed common schedules for all dates/routes.'
    if name.startswith('reports/rebaseline/repair-v21-r14/'):
        return 'Fixed-candidate review diff/status artifact; reproducible from the reachable Git commits.'
    if name.startswith('docs/track-b/evidence/cp-26/repair-v21-r14/'):
        return 'Durable repair provenance, identities, review, resource/lifecycle bookkeeping or reproducible packaging command.'
    raise ValueError('changed path outside explained repair inventory: ' + name)


def main():
    if not os.environ.get('CP26_MONITORED_JOB'):
        raise RuntimeError('handover preparation requires cumulative resource supervision')
    parser = argparse.ArgumentParser()
    parser.add_argument('--lead', type=Path, required=True)
    parser.add_argument('--candidate', required=True)
    args = parser.parse_args()
    root = args.lead.resolve()
    candidate = git(root, 'rev-parse', args.candidate).decode().strip()
    if git(root, 'rev-parse', 'main').decode().strip() != MAIN:
        raise RuntimeError('main baseline moved; disclose before relying on it')
    evidence = root / 'docs/track-b/evidence/cp-26/repair-v21-r14'
    reports = root / 'reports/rebaseline/repair-v21-r14'
    artifacts = {}
    for name, argv in {
        'repair-candidate-full.diff': ['diff', '--binary', START, candidate],
        'repair-candidate-source.diff': ['diff', START, candidate, '--', 'capstone_v21.md',
            'docs/track-b/capstone_v21-r13-to-v21-r14-amendments.md',
            'docs/track-b/evidence/cp-26/issued-repair-brief-v21-r14.md',
            'docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md', 'src/cp26', 'scripts/cp26_*.py', 'tests/test_cp26_*.py'],
        'repair-candidate-stat.txt': ['diff', '--stat', START, candidate],
        'main-to-candidate-stat.txt': ['diff', '--stat', MAIN, candidate],
    }.items():
        target = reports / name
        target.write_bytes(git(root, *argv))
        artifacts[str(target.relative_to(root))] = {'sha256': hashlib.sha256(target.read_bytes()).hexdigest(), 'bytes': target.stat().st_size}
    names = set(git(root, 'diff', '--name-only', START, 'HEAD').decode().splitlines())
    names.update(git(root, 'ls-files', '--others', '--exclude-standard').decode().splitlines())
    names.update(git(root, 'diff', '--name-only').decode().splitlines())
    rows = [{'path': name, 'reason': reason(name)} for name in sorted(names)]
    (evidence / 'files-changed.json').write_text(json.dumps({'schema': 'cp26-repair-file-reasons-v1',
        'initial_head': START, 'landed_code_base': MAIN, 'repair_candidate_sha': candidate,
        'scope': 'all task changes including preserved inherited material; terminal evidence additions are listed at final return',
        'files': rows}, ensure_ascii=False, indent=2) + '\n')
    (evidence / 'candidate-diffs.json').write_text(json.dumps({'repair_candidate_sha': candidate,
        'initial_head': START, 'landed_code_base': MAIN, 'artifacts': artifacts,
        'terminal_rule': 'candidate is reviewed; later changes are evidence only. Full terminal diff is git diff --binary INITIAL FINAL, supplied in local handover and reproducible from retained commits.'}, indent=2) + '\n')
    print(json.dumps({'candidate': candidate, 'files_explained': len(rows), 'diffs': artifacts}))


if __name__ == '__main__':
    main()
