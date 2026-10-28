"""CP-17b's re-freeze: the policy identity and freeze manifest that supersede CP-17's, and their verifier.

**What is pinned, and how** (the Owner's decision 19; brief item 4):

- **Governance documents** are bound by frozen copies under `docs/track-b/evidence/cp-17b/pinned/`, each with its
  SHA-256: the anchor at v21-r17, CP-17's two briefs and CP-17b's, both decisions records, and the CP-25 and
  CP-26 GFS rulings. `verify` checks the copies, never the live files, so an anchor amendment (r18) or a new
  decisions record leaves it green.
- **Computational inputs and code** are verified live: the snapshot, CP-25's and CP-26's manifests, CP-28's
  selection, the tier register, the margin tables, the weather features, `uv.lock`, `pyproject.toml`, every
  package, runner and pipeline file, and the payload schemas.
- **Local runtimes and state** are verified live wherever present, and required on the issuing machine: the 23
  Pyodide files, the Node.js binary, and the A1 search state (`k13.json` in the `evidence/cp-26` extract). On a
  machine without them (CI), they are listed as unchecked, never passed silently.

**CP-17's freeze is superseded, not edited:** its manifest stays verifiable by `cp17.tools.freeze` against
CP-17's own records.

    PYTHONPATH=src python -m cp17.tools.refreeze pin
    PYTHONPATH=src python -m cp17.tools.refreeze identity --bundle-manifest <src.json> --protocol-from <v2 payload json> \\
        --browser <browser-results.json> --out <policy-identity.json>
    PYTHONPATH=src python -m cp17.tools.refreeze manifest --identity ... --issuance ... --bundle ... --states ... --out ...
    PYTHONPATH=src python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17b/freeze-manifest.json
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

from .. import issue, retrain, schema, scoring, shadow
from . import freeze, ledger

PINNED = 'docs/track-b/evidence/cp-17b/pinned'
SCHEMAS_DIR = 'docs/track-b/evidence/cp-17b/schemas'
ARTIFACT_PATH = 'docs/track-b/evidence/cp-17b/artifact-2026-09-06.json'
GOVERNANCE = {
    'anchor_v21_r17': ('capstone_v21.md', '3124451da84c3cd99fae728c371207aace6ae537474f7769d0ff6333ee53e4fc'),
    'cp17_brief_second': ('docs/track-b/evidence/cp-17/issued-brief-v1-9e522b9a.md',
                          '9e522b9a42ea3c02574bd2cde4fad97266bdfd8dc38a104c13566e05c80164fa'),
    'cp17_brief_amended': ('docs/track-b/evidence/cp-17/issued-brief.md',
                           '9f235cf84876db4975930f1fce8fb62dbe188b8be4130e692eda9b5b7e1b1a73'),
    'cp17b_brief': ('docs/track-b/evidence/cp-17b/issued-brief.md',
                    'b9aeeee4131cadd060d35e05d8d0c04f114a8ec764b5c141dc893863fdd75034'),
    'decisions_1_12': ('docs/track-b/pre-cp-17-rulings-2026-10-25.md',
                       'd29b0abc6a17dcb6bca2cbd464c1dcc5858c50e2b653a42e646d3dc66ea8f6b0'),
    'decisions_13_19': ('docs/track-b/cp-17-owner-decisions-2026-10-28.md',
                        '4d049770e51a37a806c52a4ae681f70aae62ac1847a67c7c0c3109385da3ac37'),
    'cp25_rulings': ('docs/track-b/cp-25-rulings-2026-10-12.md', None),
    'cp26_gfs_ruling': ('docs/track-b/cp-26-gfs-ruling-2026-10-19.md', None),
}
COMPUTATIONAL = ('data/snapshot.parquet', 'reports/development-inputs/manifest.json',
                 'reports/rebaseline/cold-rerun-2026-10-15/scores-manifest.json', 'reports/cp28/results/selection.json',
                 'reports/development-inputs/tier-register.json', 'reports/development-inputs/partitions-development.json',
                 'reports/development-inputs/margin-days.csv', 'reports/development-inputs/margin-table.csv',
                 'reports/weather-ablation/weather-features.parquet',
                 'reports/development-inputs/weather-features-gaps.parquet', 'uv.lock', 'pyproject.toml')
CP17 = {'freeze_manifest': ('docs/track-b/evidence/cp-17/freeze-manifest.json',
                            '4af62410c2d08442b85cd11cd271f0eb367bfb019196784d1e048a46a908a544'),
        'freeze_record': ('docs/track-b/evidence/cp-17/freeze-record.md',
                          '4a47623718441cca1eb7210dfa3b47dcfcc5c421b8e3a57b858282281b5e0cec'),
        'protocol': ('docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md',
                     '337a102d6bbbf6d9335fe6ed701a4c80ea1b9172344ffc0f63909b155b567c58'),
        'integration': ('docs/track-b/evidence/cp-17/integration.md',
                        '7083bfb7176a9b7fbb4bfc4e03d00317f0c5601ec5360c006de1a2b4e066319d'),
        'landing_record': ('docs/track-b/cp-17-landing-2026-10-28.md',
                           '7f90cb87c8d64ec3faecb0b8a45ab2d5e027ace3cc1824785bcbffa5f1ff267b')}


def pin(root: Path) -> dict:
    """Copy each governance document, at its pinned identity, into `PINNED`; returns the record."""
    root = Path(root)
    (root / PINNED).mkdir(parents=True, exist_ok=True)
    out = {}
    for name, (source, expected) in GOVERNANCE.items():
        data = (root / source).read_bytes()
        actual = freeze.sha256_file(root / source)
        if expected is not None and actual != expected:
            raise ValueError(f'{source}: {actual} is not the pinned {expected}')
        copy = f'{PINNED}/{Path(source).name}'
        target = root / copy
        if target.exists() and target.read_bytes() != data:
            raise ValueError(f'{copy} exists with other bytes')
        target.write_bytes(data)
        out[name] = {'source_at_freeze': source, 'copy': copy, 'sha256': actual}
    return out


def export_schemas(root: Path) -> dict:
    folder = Path(root) / SCHEMAS_DIR
    folder.mkdir(parents=True, exist_ok=True)
    out = {}
    for kind, value in schema.SCHEMAS.items():
        path = folder / f'{kind}.schema.json'
        path.write_text(json.dumps(value, indent=1, sort_keys=True, ensure_ascii=False) + '\n')
        out[f'{SCHEMAS_DIR}/{kind}.schema.json'] = freeze.sha256_file(path)
    return out


def reference_runtime(browser_results: Path | None) -> dict:
    """The browser part of the reference runtime (CP-17's review, N6), as measured."""
    out = {'pyodide': '0.28.0', 'node': 'v26.7.0', 'machine': 'Apple M3, 8 cores, 16 GB, macOS 26.5.2',
           'chromium': '153.0.8010.12', 'webkit': '26.6', 'playwright': '1.63.0'}
    if browser_results is not None:
        record = json.loads(Path(browser_results).read_text())
        seen = {r['browser']: r.get('browser_version') for r in record['runs'] if not r.get('errors')}
        if seen.get('chromium') != out['chromium'] or seen.get('webkit') != out['webkit'] or record['playwright'] != out['playwright']:
            raise ValueError(f'the measured browsers differ from the reference runtime: {seen}, {record["playwright"]}')
        out.update(measured_platform=record['platform'], cpu_count=record['cpu_count'])
    return out


def policy_identity(root: Path, bundle_manifest: dict, protocol: dict, governance: dict, schemas_sha256: dict,
                    runtime: dict) -> dict:
    base = freeze.policy_identity(root, bundle_manifest, protocol)
    base.pop('pinned_files')
    base.pop('contracts_sha256')
    base['schema'] = 'cp17b-policy-identity-v1'
    base['governance'] = governance
    base['computational_sha256'] = {p: freeze.sha256_file(Path(root) / p) for p in COMPUTATIONAL}
    base['code']['pipeline_files_sha256'] = bundle_manifest['pipeline_files_sha256']
    base['schemas_sha256'] = schemas_sha256
    base['reference_runtime'] = runtime
    base['supersedes'] = {'checkpoint': 'CP-17', 'policy_identity_sha256': 'b304d6479a8628a26014422c6682f1e6543bd0d9ff656ad34b2d87b163bc254e',
                          'records': {k: {'path': p, 'sha256': h} for k, (p, h) in CP17.items()}}
    base['success_definition'] = {
        'wall_seconds': issue.WALL_LIMIT_SECONDS, 'peak_bytes': issue.MEMORY_LIMIT_BYTES,
        'criteria': ['inputs (no forecastable hour fails here)', 'training',
                     'emission on every forecastable hour (decision 13; partial days displayed as partial)',
                     'artifact, judged inside the chain', 'resources, per attempt in its own process'],
        'labels': 'released errors from complete delivery days <= D-2; training targets the days before D published '
                  'strictly before the issue time (decision 16)'}
    base['failure_policy'].update({
        'decisions': '11, 12 and 15 (the chains stay); 17 (GFS missing in the training window fails A1 and v4, so v2 issues)',
        'partial_days': 'decision 13', 'gfs_disclosure': 'item 1: v2 +2.27% MAE, +6.68% WIS against A1 GFS +6 h'})
    base['shadow'] = {'decision': 14, 'policies': list(shadow.POLICIES),
                      'rule': 'v4, v2 and B0 issue every day as shadows, never published; their own complete-day errors '
                              'enter their own buffers once after D-2; B0 is shadow-issued because a rebuild from prices '
                              'alone does not equal CP-26 (36 days whose B0 keys were partial)'}
    base['disclosures'] = {'F1': 'at the DST origin 2025-10-26, A1 under the issuing host differs from native by up to '
                                 '0.028 EUR/MWh with every selection identical; tau_eq unchanged (decision 18)'}
    base['retrain'] = {'tau_eq_eur': retrain.TAU_EQ, 'status': list(retrain.STATUS),
                       'binding': 'the retrain must run on the issued fit\'s training window (payload identity) first'}
    base['definitions'] = {'tau_eur': scoring.TAU_EUR, 'rolling_days': scoring.ROLLING_DAYS,
                           'recompute_relative_tolerance': scoring.RELATIVE_TOLERANCE, 'levels': list(scoring.LEVELS)}
    return base


def manifest(identity: dict, issuance: dict, bundle_manifest_path: Path | None, states_record: dict) -> dict:
    out = freeze.freeze_manifest(identity, issuance, bundle_manifest_path, states_record)
    out.pop('content_sha256')
    out['schema'] = 'cp17b-freeze-manifest-v1'
    out['freeze_origin']['artifact_path'] = ARTIFACT_PATH
    out['content_sha256'] = freeze.digest({k: v for k, v in out.items() if k != 'content_sha256'})
    return out


def _local(project: Path, identity: dict) -> dict[str, str]:
    """The local-only files the identity records: path -> expected SHA-256."""
    out = {}
    for name, h in identity['issuing_host']['pyodide']['files_sha256'].items():
        out[str(project / freeze.RUNTIME_DIR / name)] = h
    out[identity['issuing_host']['node']['path']] = identity['issuing_host']['node']['sha256']
    search = identity['hyperparameters']['A1_search']
    out[str(project / '.local' / ledger.INPUTS / search['file'])] = search['file_sha256']
    return out


def verify(manifest_value: dict, root: Path, project: Path | None = None, require_local: bool | None = None) -> dict:
    """{'problems': [...], 'unchecked': [...]}: every recorded hash recomputed (CP-17's review, N4)."""
    root = Path(root)
    project = ledger.project_root(root) if project is None else Path(project)
    problems, unchecked = [], []
    if manifest_value.get('schema') != 'cp17b-freeze-manifest-v1':
        problems.append('not a CP-17b freeze manifest')
    if manifest_value.get('content_sha256') != freeze.digest({k: v for k, v in manifest_value.items() if k != 'content_sha256'}):
        problems.append('the manifest\'s own content digest does not hold')
    identity = manifest_value.get('policy_identity', {})
    if manifest_value.get('policy_identity_sha256') != freeze.digest(identity):
        problems.append('the policy identity differs from its recorded digest')
    registry = identity.get('registry', {})
    if registry.get('version') != 1 or registry.get('registered_model') != issue.PRODUCT:
        problems.append('wrong or missing registry name or version')
    for name, item in identity.get('governance', {}).items():
        path = root / item['copy']
        if not path.exists() or freeze.sha256_file(path) != item['sha256']:
            problems.append(f'{item["copy"]}: the frozen governance copy is missing or altered')
    if set(identity.get('governance', {})) != set(GOVERNANCE):
        problems.append('the governance pins are not the frozen set')
    checks = {**identity.get('computational_sha256', {}), **identity.get('schemas_sha256', {})}
    code = identity.get('code', {})
    for group in ('files_sha256', 'runner_files_sha256', 'pipeline_files_sha256'):
        if not code.get(group):
            problems.append(f'the code group {group} is empty')
        checks.update({f'src/{rel}': h for rel, h in code.get(group, {}).items()})
    for rel, expected in checks.items():
        path = root / rel
        if not path.exists() or freeze.sha256_file(path) != expected:
            problems.append(f'{rel}: missing or altered')
    for kind, value in schema.SCHEMAS.items():
        rel = f'{SCHEMAS_DIR}/{kind}.schema.json'
        if rel not in identity.get('schemas_sha256', {}) or not (root / rel).exists() \
                or json.loads((root / rel).read_text()) != json.loads(json.dumps(value)):
            problems.append(f'{rel}: does not hold the package\'s schema')
    local = _local(project, identity) if identity.get('issuing_host') else {}
    present = any(Path(p).exists() for p in local)
    required = present if require_local is None else require_local
    for path, expected in local.items():
        if not Path(path).exists():
            (problems if required else unchecked).append(f'{path}: absent')
        elif freeze.sha256_file(Path(path)) != expected:
            problems.append(f'{path}: altered')
    origin = manifest_value.get('freeze_origin', {})
    path = root / origin.get('artifact_path', ARTIFACT_PATH)
    if not path.exists() or freeze.sha256_file(path) != origin.get('artifact_file_sha256'):
        problems.append(f'{origin.get("artifact_path", ARTIFACT_PATH)}: the freeze-origin artifact is missing or altered')
    else:
        art = json.loads(path.read_text())
        if art.get('artifact_sha256') != origin.get('artifact_sha256') or issue.verify_artifact(art) \
                or art.get('lineage', {}).get('policy_identity_sha256') != manifest_value.get('policy_identity_sha256'):
            problems.append('the freeze-origin artifact does not verify against the manifest')
    return {'problems': problems, 'unchecked': unchecked}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('pin').add_argument('--root', default='.', type=Path)
    a = sub.add_parser('identity')
    a.add_argument('--root', default='.', type=Path)
    a.add_argument('--bundle-manifest', required=True, type=Path)
    a.add_argument('--protocol-from', required=True, type=Path)
    a.add_argument('--browser', type=Path)
    a.add_argument('--out', required=True, type=Path)
    b = sub.add_parser('manifest')
    b.add_argument('--identity', required=True, type=Path)
    b.add_argument('--issuance', required=True, type=Path)
    b.add_argument('--bundle', type=Path)
    b.add_argument('--states', required=True, type=Path)
    b.add_argument('--out', required=True, type=Path)
    c = sub.add_parser('verify')
    c.add_argument('manifest', type=Path)
    c.add_argument('--root', default='.', type=Path)
    args = ap.parse_args(argv)
    if args.cmd == 'pin':
        print(json.dumps(pin(args.root), indent=1))
    elif args.cmd == 'identity':
        governance = pin(args.root)
        value = policy_identity(args.root, json.loads(args.bundle_manifest.read_text()),
                                json.loads(args.protocol_from.read_text())['protocol'], governance,
                                export_schemas(args.root), reference_runtime(args.browser))
        args.out.write_text(json.dumps(value, indent=1, sort_keys=True) + '\n')
        print('policy identity', freeze.digest(value))
    elif args.cmd == 'manifest':
        value = manifest(json.loads(args.identity.read_text()), json.loads(args.issuance.read_text()), args.bundle,
                         json.loads(args.states.read_text()))
        args.out.write_text(json.dumps(value, indent=1, sort_keys=True) + '\n')
        print('freeze manifest', value['content_sha256'])
    else:
        result = verify(json.loads(args.manifest.read_text()), args.root)
        print('verified' if not result['problems'] else '\n'.join(result['problems']))
        if result['unchecked']:
            print('unchecked here (absent on this machine):', len(result['unchecked']))
        return 1 if result['problems'] else 0
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
