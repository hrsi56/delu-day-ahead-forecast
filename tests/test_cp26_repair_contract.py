"""Identity/custody and repair boundaries; no model fits or experiment scores.

Identities are read from the committed records, never from the branch's Git history: a squash
LAND, and CI's depth-1 checkout of it, carry none of the commits named here.
"""
from pathlib import Path
import hashlib
import json

from cp26 import harness as H

ROOT = Path(__file__).resolve().parents[1]
INITIAL = '5cc3cc083c4340fd8d792eeaf6551a007987a877'
ACTIVE = 'docs/track-b/evidence/cp-26/repair-v21-r14/active-documents.json'
#: SHA-256 of `5cc3cc0:capstone_v21.md` (r13, SHA-256 173799d8…) from '## 1. ' up to '## 24. ',
#: recorded at the landing repair (2026-10-20) from that commit and from main 647d6eb's copy.
R13_SECTIONS_1_TO_23_SHA256 = '1d5406a3df529929ce6a662af97d7fcfeecc40726906b5a994548140d6f1a872'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def recorded(path):
    """A committed record, at the bytes CP-26's harness pins."""
    assert sha256(ROOT / path) == H.PINS[path], path
    return json.loads((ROOT / path).read_text())


def test_anchor_commit_and_landed_base_are_distinct_and_explicit():
    # r16 (8070238) moved the active anchor commit to 4766a61 and kept r14's 332baeb as the
    # scientific anchor commit; the r16 authority records both, and r17 (2026-10-19) records the
    # r16 anchor bytes it supersedes.
    assert H.BASE_COMMIT == '647d6eb81b2cf6e0cfaf4152f659d689ff973578'
    assert H.ANCHOR_COMMIT == '4766a61cb0c836573406f5a9729997d1b6ee9862'
    assert H.SCIENTIFIC_ANCHOR_COMMIT == '332baeb861cec5a58516c58a29a1a3afe1eec909'
    assert len({H.BASE_COMMIT, H.ANCHOR_COMMIT, H.SCIENTIFIC_ANCHOR_COMMIT, INITIAL}) == 4
    authority = recorded(H.AUTHORITY_PATH)
    assert authority['anchor_commit'] == H.ANCHOR_COMMIT
    assert authority['original_scientific_anchor_commit'] == H.SCIENTIFIC_ANCHOR_COMMIT
    assert authority['original_scientific_anchor_sha256'] == H.SCIENTIFIC_ANCHOR_SHA256
    assert {item['path']: item['sha256'] for item in authority['ratified_documents']}['capstone_v21.md'] \
        == H.PINS['capstone_v21.md']
    assert H.PINS['capstone_v21.md'] in (ROOT / 'docs/track-b/capstone_v21-r16-to-v21-r17-amendments.md').read_text()
    active = recorded(ACTIVE)
    anchor = next(item for item in active['documents'] if item['path'] == 'capstone_v21.md')
    assert (anchor['commit'], anchor['sha256']) == (H.SCIENTIFIC_ANCHOR_COMMIT, H.SCIENTIFIC_ANCHOR_SHA256)
    # Every other pinned identity keeps its bytes; the continuation authority is bound through the
    # r16 authority's record of it.
    assert authority['cumulative_before']['continuation_authority_sha256'] == H.PINS[H.SCIENTIFIC_AUTHORITY_PATH]
    for name, expected in H.PINS.items():
        if name not in ('capstone_v21.md', H.SCIENTIFIC_AUTHORITY_PATH):
            assert sha256(ROOT / name) == expected, name
    cp25 = json.loads((ROOT / 'reports/development-inputs/manifest.json').read_text())['outputs_sha256']
    assert all(sha256(ROOT / name) == cp25[name] for name in H.CP25_READ)
    cp15 = json.loads((ROOT / 'reports/cp15/artifact-manifest.json').read_text())['artifact_sha256']
    assert cp15['reports/cp15/protocol.json'] == H.PINS['reports/cp15/protocol.json']
    # The landed member code is the code at the landed base, as the harness log recorded it.
    assert active['landed_code_base'] == H.BASE_COMMIT
    landed = json.loads((ROOT / 'reports/rebaseline/harness-log.json').read_text())['landed_code']
    assert landed == {str(path.relative_to(ROOT)): sha256(path)
                      for base in H.LANDED_CODE for path in sorted((ROOT / base).rglob('*.py'))}


def test_original_documents_and_sections_1_through_23_stay_historical():
    active = recorded(ACTIVE)
    original = {item['supersedes']['path']: item['supersedes']['sha256']
                for item in active['documents'] if (item.get('supersedes') or {}).get('path')}
    assert active['historical_documents_unchanged'] == ['docs/track-b/evidence/cp-26/issued-brief.md',
                                                        'docs/track-b/evidence/cp-26/cp28-frozen-protocol.md']
    for path in active['historical_documents_unchanged']:
        assert sha256(ROOT / path) == original[path]
    anchor = next(item for item in active['documents'] if item['path'] == 'capstone_v21.md')
    assert anchor['supersedes'] == {'commit': INITIAL, 'version': 'v21-r13',
                                    'sha256': '173799d818387b9d82db16b9ccd7195afaebbea8e11259809e4a8b704bd525a8'}
    candidate = (ROOT / 'capstone_v21.md').read_text()
    def earlier(text):
        # Keep every research section before24 verbatim, independently of candidate header.
        return text[text.index('## 1. '):text.index('## 24. ')]
    assert hashlib.sha256(earlier(candidate).encode()).hexdigest() == R13_SECTIONS_1_TO_23_SHA256


def test_registration_keeps_seven_arms_and_exact_decision_sections():
    old = (ROOT / 'docs/track-b/evidence/cp-26/cp28-frozen-protocol.md').read_text()
    new = (ROOT / 'docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md').read_text()
    for start, end in (('## 3.', '## 4.'), ('## 4.', '## 5.'), ('## 5.', '## 6.'),
                       ('## 8.', '## 9.'), ('## 9.', '## 10.')):
        assert old[old.index(start):old.index(end)] == new[new.index(start):new.index(end)]
    assert 'H-history fallback dates do enter after D−2 once' in new
    assert 'no promised activation date' in new
    anchor = (ROOT / 'capstone_v21.md').read_text()
    assert 'candidate for Owner review and ratification' in anchor
    assert 'S_14 = 2027-01-06' in anchor and 'S_13 = 2026-07-08' in anchor
