"""Rebuild the r14 active-document/supersession manifest; zero model fits/scores."""
from pathlib import Path
import hashlib
import json
import os
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/track-b/evidence/cp-26/repair-v21-r14/active-documents.json'
ANCHOR_COMMIT = '332baeb861cec5a58516c58a29a1a3afe1eec909'
INITIAL = '5cc3cc083c4340fd8d792eeaf6551a007987a877'
ANCHOR_HASH = '3be866bd10af02cc2b0b956ed91be660dca29a62c0b23b00997bf0b415d100c5'


def main():
    if not os.environ.get('CP26_MONITORED_JOB'):
        raise RuntimeError('document manifest requires the cumulative resource monitor')
    def sha(p):
        return hashlib.sha256(p.read_bytes()).hexdigest()
    def blob(commit, name):
        return hashlib.sha256(subprocess.check_output(['git', 'show', f'{commit}:{name}'], cwd=ROOT)).hexdigest()
    if sha(ROOT / 'capstone_v21.md') != ANCHOR_HASH or blob(ANCHOR_COMMIT, 'capstone_v21.md') != ANCHOR_HASH:
        raise ValueError('candidate anchor differs from its noncircular anchor commit')
    brief = 'docs/track-b/evidence/cp-26/issued-brief.md'
    protocol = 'docs/track-b/evidence/cp-26/cp28-frozen-protocol.md'
    for p in (brief, protocol):
        if sha(ROOT / p) != blob(INITIAL, p):
            raise ValueError('original issued document changed')
    rows = [
        {'path': 'capstone_v21.md', 'version': 'v21-r14 candidate', 'sha256': ANCHOR_HASH,
         'commit': ANCHOR_COMMIT, 'status': 'pending_owner_ratification',
         'supersedes': {'version': 'v21-r13', 'commit': INITIAL,
                       'sha256': '173799d818387b9d82db16b9ccd7195afaebbea8e11259809e4a8b704bd525a8'},
         'reason': 'Owner-approved repair contract: search support, native-error recovery, eligibility/state and CP28 consequences'},
        {'path': 'docs/track-b/capstone_v21-r13-to-v21-r14-amendments.md',
         'version': 'r13-to-r14 repair candidate', 'status': 'active_repair_record', 'supersedes': None},
        {'path': 'docs/track-b/evidence/cp-26/issued-repair-brief-v21-r14.md',
         'version': 'Owner repair brief v21-r14', 'status': 'active_repair_only',
         'supersedes': {'path': brief, 'sha256': sha(ROOT / brief)},
         'reason': 'This repair scope replaces stale Jan1/support and blanket fallback-intake execution assumptions; no experiment resumption'},
        {'path': 'docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md',
         'version': 'cp28-stored-forecasts-v21-r14', 'status': 'frozen_registration_candidate',
         'supersedes': {'path': protocol, 'version': 'cp28-stored-forecasts-v1', 'sha256': sha(ROOT / protocol)},
         'reason': 'Continuous native-central H warm-up/recovery and separate three-member learning eligibility; seven-arm decision rules unchanged'},
    ]
    for row in rows:
        row['sha256'] = sha(ROOT / row['path'])
    result = {'schema': 'cp26-repair-active-documents-v1', 'checkpoint': 'cp-26',
              'checkpoint_status': 'INCOMPLETE', 'repair_experiment_authorized': False,
              'landed_code_base': '647d6eb81b2cf6e0cfaf4152f659d689ff973578',
              'documents': rows, 'historical_documents_unchanged': [brief, protocol],
              'freeze_rule': 'commit these documents before any new search/pilot; Owner ratification and continuation brief required',
              'self_identity': 'this manifest has no self hash or self commit; its identity is recorded externally'}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'manifest': str(OUT), 'sha256': sha(OUT), 'documents': len(rows), 'models_fitted': 0}))


if __name__ == '__main__':
    main()
