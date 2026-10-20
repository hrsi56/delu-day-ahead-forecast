"""Versioned presentation correction over an immutable CP-26 report.

The original scientific code identity and every numeric field stay intact.
This renderer has its own identity; it does not pretend to have generated the
completed scores, inference or diagnostics. No scientific entry point is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from cp26 import reporting as R
from cp26.state import _save, digest

SOURCES = {
    'docs/track-b/cp-25-rulings-2026-10-12.md':
        'c7af67f88157277aafd8dd2b1b49e12a1d9ff4b747ca5bdf178fac664fba53c1',
    'docs/track-b/cp-25-landing-2026-10-12.md':
        'f33f58985a85803aed04ef48bf9c55db0d7738fac0a7d81db2a9c02d31b11b56',
}
DISCLOSURES = (
    ('load_revision', '1',
     'The day-ahead load forecast is tier 3: the historical snapshot has no original vintages. '
     'The main evaluation retains it under the recorded Owner exception and retains revision risk. '
     'The no-load variant is a descriptive bound, not a replacement control.'),
    ('target_price_updates', '2',
     'The target price is tier 2. SMARD states that later updates of published prices are possible; '
     'this update-possible caveat remains despite the sampled ENTSO-E agreement.'),
    ('structural_margin_risks', '3',
     'The structural margins of prices +24 hours, GFS +24 hours and load +1 hour are accepted '
     'disclosed operational risks, not proven safe margins. They remain to be measured in the '
     'CP-18 live trial. The GFS +6-hour sensitivity does not establish their safety.'),
    ('never_scored_overlap', '4',
     'The "never scored" mask includes historical training-only inner-validation overlap from '
     'CP-15, CP-21 and CP-22. It is a descriptive reporting subset, gates nothing, and does not '
     'establish that those days were unused.'),
)
REVISION_FIELDS = {'limitations', 'reporting_disclosures', 'presentation_revision', 'content_sha256'}


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read_signed(path):
    value = json.loads(Path(path).read_bytes())
    if value.get('content_sha256') != digest({k: v for k, v in value.items() if k != 'content_sha256'}):
        raise ValueError('source content signature mismatch')
    return value


def records():
    return [{'id': identity, 'text': text, 'source': {
        'path': next(iter(SOURCES)), 'sha256': next(iter(SOURCES.values())), 'section': section}}
        for identity, section, text in DISCLOSURES]


def disclosure_lines():
    return [f"{row['text']} Source: CP-25 rulings §{row['source']['section']} "
            '(docs/track-b/cp-25-rulings-2026-10-12.md).'
            for row in records()]


def qualify(original, provenance):
    if original.get('schema') != 'cp26-report-v1' or 'presentation_revision' in original:
        raise ValueError('expected original completed scientific report')
    revised = {**original, 'limitations': [*original['limitations'], *disclosure_lines()],
               'reporting_disclosures': records(), 'presentation_revision': provenance}
    revised.pop('content_sha256', None)
    return revised


def validate_disclosures(report, packet, rendered_report, rendered_packet):
    """Fail closed if a qualification or its source binding disappears on any surface."""
    if report.get('reporting_disclosures') != records() or packet.get('reporting_disclosures') != records():
        raise ValueError('missing or altered source-bound reporting disclosure')
    for text in disclosure_lines():
        if (text not in report.get('limitations', []) or
                text not in packet.get('slots', {}).get('limitations', []) or
                text not in rendered_report or text not in rendered_packet):
            raise ValueError('missing reporting qualification on a report/packet surface')


def assert_science_unchanged(original, revised):
    before = {k: v for k, v in original.items() if k not in REVISION_FIELDS}
    after = {k: v for k, v in revised.items() if k not in REVISION_FIELDS}
    if before != after or revised['limitations'] != original['limitations'] + disclosure_lines():
        raise ValueError('presentation revision altered scientific fields or original limitations')
    return digest(before)


def regenerate(root, source, output):
    root, source, output = Path(root).resolve(), Path(source).resolve(), Path(output).resolve()
    if not source.is_relative_to(root / 'reports/rebaseline') or not output.is_relative_to(root / 'reports/rebaseline'):
        raise ValueError('report inputs/outputs must remain inside rebaseline outputs')
    if output.exists():
        raise ValueError('versioned output already exists; preserve it')
    for path, expected in SOURCES.items():
        if sha(root / path) != expected:
            raise ValueError('CP-25 reporting authority bytes changed')
    original = read_signed(source / 'report.json')
    original_packet = read_signed(source / 'publication-packet.json')
    original_export = read_signed(source / 'MLflow-export.json')
    names = ('report.json', 'report.md', 'publication-packet.json', 'publication-packet.md', 'MLflow-export.json')
    original_hashes = {name: sha(source / name) for name in names}
    provenance = {'schema': 'cp26-presentation-revision-v1', 'scope': 'reporting disclosures only',
        'source_report_content_sha256': original['content_sha256'],
        'source_outputs': {str((source / name).relative_to(root)): value for name, value in original_hashes.items()},
        'authority_sources': SOURCES,
        'renderer': {'path': str(Path(__file__).resolve().relative_to(root)), 'sha256': sha(__file__)},
        'scientific_code_identity_unchanged': True, 'scientific_rerun': False}
    report = qualify(original, provenance)
    science_sha = assert_science_unchanged(original, report)
    streams = sorted({row['stream'] for row in report['primary']})
    packet, export = R._packet(report, streams)
    # Independently preserve every packet/export field except disclosed presentation metadata.
    expected_packet = {k: v for k, v in original_packet.items() if k != 'content_sha256'}
    expected_packet['slots'] = {**expected_packet['slots'], 'limitations': report['limitations']}
    if packet != expected_packet or export != {k: v for k, v in original_export.items() if k != 'content_sha256'}:
        raise ValueError('regeneration changed a packet or export field beyond the limitations')
    for artifact in (packet, export):
        artifact['reporting_disclosures'] = records()
        artifact['presentation_revision'] = provenance
    report_md, packet_md = R._render_report(report), R._render_packet(packet)
    validate_disclosures(report, packet, report_md, packet_md)
    output.mkdir(parents=True)
    for name, artifact in (('report.json', report), ('publication-packet.json', packet), ('MLflow-export.json', export)):
        artifact['content_sha256'] = digest(artifact)
        _save(output / name, artifact)
    (output / 'report.md').write_text(report_md, encoding='utf-8')
    (output / 'publication-packet.md').write_text(packet_md, encoding='utf-8')
    if original_hashes != {name: sha(source / name) for name in names}:
        raise ValueError('an original output changed during presentation rendering')
    manifest = {'schema': 'cp26-presentation-manifest-v1', 'status': 'COMPLETE',
        'provenance': provenance, 'unchanged_scientific_fields_sha256': science_sha,
        'source_scientific_fingerprint': original['candidate_fingerprint'],
        'disclosure_ids': [row['id'] for row in records()],
        'artifacts': {name: {'path': str((output / name).relative_to(root)),
                             'bytes': (output / name).stat().st_size, 'sha256': sha(output / name)} for name in names}}
    manifest['content_sha256'] = digest(manifest)
    _save(output / 'presentation-manifest.json', manifest)
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    value = regenerate(Path.cwd(), args.source, args.output)
    print(json.dumps({'status': value['status'], 'content_sha256': value['content_sha256'],
                      'disclosure_ids': value['disclosure_ids']}))
