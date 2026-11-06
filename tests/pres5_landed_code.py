"""CP-26's landed code as its harness log recorded it, after PRES-5's authorized presentation changes.

CP-26's harness log (`reports/rebaseline/harness-log.json`, `landed_code`) pins the SHA-256 of every `.py` file under
`H.LANDED_CODE`, and the CP-26 tests compared those pins with the working tree. PRES-5's brief allows changes to the
report's build and to the registry, which live in `src/delu_forecast/`: it changed five of those modules and added two.
Their bytes at CP-26's landing are recorded, hash-bound, under `RECORD`; this module proves each pinned entry against
those bytes, not against the branch's Git history (a squash LAND, and CI's depth-1 checkout of it, carry none of it).
Every other landed file is still compared with the working tree, so any other change still fails.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from cp26 import harness as H

RECORD = Path('docs/track-b/evidence/pres-5/cp26-landed-presentation-code')
#: CP-26's landing, where the five recorded modules have the bytes its harness log pins.
CP26_LANDING = '61658c70520b880d844b1bb54af9973cf2851d9d'


def _sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def landed_code(root: Path) -> dict[str, str]:
    """The landed-code map CP-26's harness log must equal: the working tree's files, with PRES-5's recorded bytes in
    place of the modules PRES-5 changed, and without the modules it added."""
    record = json.loads((root / RECORD / 'manifest.json').read_text())
    assert record['commit'] == CP26_LANDING
    assert set(record['files']) == {'src/delu_forecast/derived.py', 'src/delu_forecast/publication_lint.py',
                                    'src/delu_forecast/registry.py', 'src/delu_forecast/research.py',
                                    'src/delu_forecast/research_claims.py'}
    added = set(record['added_by_pres5'])
    assert added == {'src/delu_forecast/compact_figures.py', 'src/delu_forecast/final_candidate.py'}
    out = {}
    for base in H.LANDED_CODE:
        for path in sorted((root / base).rglob('*.py')):
            name = str(path.relative_to(root))
            if name in added:
                continue
            entry = record['files'].get(name)
            if entry is None:
                out[name] = _sha256(path.read_bytes())
                continue
            raw = (root / RECORD / entry['snapshot']).read_bytes()
            assert len(raw) == entry['bytes'] and _sha256(raw) == entry['sha256'], name
            assert hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest() == entry['git_blob'], name
            out[name] = entry['sha256']
    assert set(record['files']) <= set(out)
    return out
