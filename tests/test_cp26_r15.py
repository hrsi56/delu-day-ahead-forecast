"""Small checks for r15 admission, shutdown headroom and operational-only lineage.

The lineage checks read recorded identities, never the branch's Git history: a squash LAND, and
CI's depth-1 checkout of it, carry no gauntlet/cp-26 commit.
"""
import ast
import copy
import hashlib
import json
from pathlib import Path

from cp26 import budget as B
from cp26 import harness as H
from cp26.limits import shutdown_exposure_seconds
from cp26_ledger_snapshot import identity_path

#: The scientific base's four modules, recorded at the landing repair with their hashes.
SCIENTIFIC_BASE = Path('docs/track-b/evidence/cp-26/landing-repair/scientific-base-1e7eb02')


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text())


def scientific_base_source(root, path):
    """`git show <SCIENTIFIC_BASE_COMMIT>:<path>`, from its recorded, hash-bound copy."""
    record = read_json(root / SCIENTIFIC_BASE / 'manifest.json')
    lineage = read_json(root / H.RUNTIME_LINEAGE)
    assert record['commit'] == lineage['scientific_base_commit'] == H.SCIENTIFIC_BASE_COMMIT
    entry = record['files'][path]
    raw = (root / SCIENTIFIC_BASE / entry['snapshot']).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == entry['sha256']
    assert hashlib.sha1(b'blob %d\0' % len(raw) + raw).hexdigest() == entry['git_blob']
    assert lineage['original_recipe_code_sha256'].get(path, entry['sha256']) == entry['sha256']
    return raw


def resource_state(seconds):
    return {'counts': {'machine_seconds': seconds}, 'accounting': {
        'measured_seconds': seconds, 'reported_seconds': 0., 'reserved_seconds': 0.},
        'jobs': [], 'peaks': {}, 'reserves': []}


def test_general_boundary_remains436point5_with500_actual():
    searches = [{'run': r, 'k': k, 'classification': 'conservative', 'basis': 'fixture',
                 'machine_seconds': 1.} for r in ('nominal', 'noload', 'gfs6') for k in range(14)]
    remaining = {k: {'classification': 'conservative', 'basis': 'fixture', 'machine_seconds': 1.}
                 for k in ('daily_fits', 'parity', 'tests', 'bootstrap', 'diagnostics', 'failed_jobs_and_resume')}
    state = resource_state(436.5 * 3600 - 48.)
    assert B.projected_cost(state, searches, remaining)['within_pilot_stop']
    B.add_seconds(state, 1.)
    assert not B.projected_cost(state, searches, remaining)['within_pilot_stop']
    assert B.CAPS['machine_seconds'] == 500 * 3600 and B.admission_hours() == 436.5


def test_shutdown_exposure_is_reserved_headroom_not_another_charge():
    state = resource_state(B.CAPS['machine_seconds'] - 100.)
    state['jobs'] = [{'running': True, 'workers': 4}]
    before = copy.deepcopy(state)
    assert shutdown_exposure_seconds(4) > 100
    assert B.limit_reason(state) == 'machine_hours_cap'
    assert state == before and B.total_seconds(state) < B.CAPS['machine_seconds']
    state['jobs'][0]['running'] = False
    assert B.limit_reason(state) is None


class StripOperationalMetadata(ast.NodeTransformer):
    def visit_Dict(self, node):
        self.generic_visit(node)
        pairs = [(k, v) for k, v in zip(node.keys, node.values)
                 if not isinstance(k, ast.Constant) or k.value != 'operational_lineage']
        node.keys, node.values = [p[0] for p in pairs], [p[1] for p in pairs]
        return node


def test_original_numeric_functions_are_unchanged_by_r15():
    root = Path(__file__).resolve().parents[1]
    skip = {'harness': {'input_fingerprint'}, 'search': {'search_identity', 'execute_search'},
            'parity': {'require_pass'}, 'execution': set()}
    for module, omitted in skip.items():
        path = f'src/cp26/{module}.py'
        old = ast.parse(scientific_base_source(root, path))
        new = ast.parse((root / path).read_text())
        old_functions = {n.name: n for n in old.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        new_functions = {n.name: n for n in new.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        for name, node in old_functions.items():
            if name in omitted:
                continue
            assert ast.dump(StripOperationalMetadata().visit(node), include_attributes=False) == ast.dump(
                StripOperationalMetadata().visit(new_functions[name]), include_attributes=False), (module, name)
        if module == 'search':
            def evaluator(tree):
                outer = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'execute_search')
                return next(n for n in outer.body if isinstance(n, ast.FunctionDef) and n.name == 'evaluate')
            assert ast.dump(StripOperationalMetadata().visit(evaluator(old))) == ast.dump(
                StripOperationalMetadata().visit(evaluator(new)))


def test_r15_authority_does_not_relabel_scientific_plan_or_parity():
    """The run's protocol, inputs, search plans and parity keep the r14 scientific identity.

    The live guards (`continuation_authority`, `protocol_identity`, `input_fingerprint`,
    `search_identity`, `require_pass`) also demand the r16 anchor bytes and branch commits, so they
    refuse once r17 is the active anchor (2026-10-19). This check binds the same identities through
    the committed records instead.
    """
    from cp26.gates import OUTPUT, PROTOCOL, RUN_EVIDENCE, RUN_ID
    from cp26.parity import SOURCES, validate_report
    from cp26.search import MODEL_CODE, PROTOCOL as SEARCH_PROTOCOL
    root = Path(__file__).resolve().parents[1]
    # The r16 operational authority names the r16 anchor commit and keeps r14's scientific anchor
    # and continuation authority; r17 records the same r16 anchor bytes as its base.
    authority = read_json(root / H.AUTHORITY_PATH)
    assert sha256(root / H.AUTHORITY_PATH) == H.PINS[H.AUTHORITY_PATH]
    assert authority['anchor_commit'] == H.ANCHOR_COMMIT
    assert authority['original_scientific_anchor_sha256'] == H.SCIENTIFIC_ANCHOR_SHA256
    assert authority['cumulative_before']['continuation_authority_sha256'] == H.PINS[H.SCIENTIFIC_AUTHORITY_PATH]
    assert all(H.PINS[item['path']] == item['sha256'] for item in authority['ratified_documents'])
    r17 = (root / 'docs/track-b/capstone_v21-r16-to-v21-r17-amendments.md').read_text()
    assert H.PINS['capstone_v21.md'] in r17

    # Protocol: the r14 continuation authority and research anchor, as recorded at r15's admission
    # and r16's checks, not an r15 or r16 relabel.
    manifest = read_json(root / OUTPUT / 'execution-manifest.json')
    protocol = manifest['protocol_identity']
    assert protocol == read_json(root / RUN_EVIDENCE / 'admission-v21-r15.json')['protocol']
    assert protocol == read_json(root / RUN_EVIDENCE / 'checks-v21-r16.json')['protocol']
    assert (protocol['schema'], protocol['document'], protocol['run_id']) == (
        'cp26-execution-protocol-v21-r14', str(PROTOCOL), RUN_ID)
    assert protocol['authority_sha256'] == H.PINS[H.SCIENTIFIC_AUTHORITY_PATH]
    assert protocol['research_sha256'] == H.SCIENTIFIC_ANCHOR_SHA256
    cp28 = 'docs/track-b/evidence/cp-26/cp28-frozen-protocol-v21-r14.md'
    assert protocol['cp28_protocol_sha256'] == H.PINS[cp28] == sha256(root / cp28)
    assert protocol['run_authority_document'] == str(RUN_EVIDENCE / 'registration.json')
    assert protocol['run_authority_sha256'] == sha256(root / RUN_EVIDENCE / 'registration.json')

    # Inputs: r14's scientific identities. Every input file but the superseded anchor and the
    # continuation authority (bound above) keeps its bytes, and so does the landed member code.
    cp25 = read_json(root / 'reports/development-inputs/manifest.json')['outputs_sha256']
    inputs = manifest['inputs']
    assert inputs == {**H.SCIENTIFIC_PINS, **{name: cp25[name] for name in H.CP25_READ}}
    for name, expected in inputs.items():
        if name not in ('capstone_v21.md', H.SCIENTIFIC_AUTHORITY_PATH):
            assert sha256(identity_path(root, name)) == expected, name
    landed = read_json(root / 'reports/rebaseline/harness-log.json')['landed_code']
    assert landed == {str(path.relative_to(root)): sha256(path)
                      for base in H.LANDED_CODE for path in sorted((root / base).rglob('*.py'))}
    fingerprint = hashlib.sha256(json.dumps({'identities': inputs, 'landed_code': landed},
                                            sort_keys=True).encode()).hexdigest()
    assert manifest['input_fingerprint'] == fingerprint

    # Search plans: k13 (nominal) was signed with the original recipe identity, and the current
    # operational sources are exactly those the r16 runtime lineage recorded.
    lineage = read_json(root / H.RUNTIME_LINEAGE)
    assert lineage['scientific_base_commit'] == H.SCIENTIFIC_BASE_COMMIT
    assert all(sha256(root / name) == digest for name, digest in lineage['actual_code_sha256'].items())
    recipe = lineage['original_recipe_code_sha256']
    plan = next(item for item in manifest['searches'] if (item['route'], item['k']) == ('nominal', 13))
    assert plan['identity'] == {'protocol': SEARCH_PROTOCOL, 'run_id': RUN_ID, 'k': 13, 'route': 'nominal',
                                'cp26_input_fingerprint': fingerprint,
                                'code_sha256': {name: recipe.get(name, sha256(root / name)) for name in MODEL_CODE}}

    # Parity: the committed gate passed all 96 checks on the same inputs, code and references.
    parity = read_json(root / OUTPUT / 'parity.json')
    validate_report(parity)
    assert len(parity['checks']) == 96 and parity['input_fingerprint'] == fingerprint
    assert all(digest in (recipe.get(name), sha256(root / name)) for name, digest in parity['code_sha256'].items())
    assert set(parity['reference_custody']) == set(SOURCES)
    for label, source in SOURCES.items():
        custody = parity['reference_custody'][label]
        artifacts = read_json(root / source.manifest)['artifact_sha256']
        assert (custody['evidence_commit'], custody['manifest']) == (source.evidence_commit, source.manifest)
        assert custody['manifest_sha256'] == sha256(root / source.manifest)
        assert custody['files_sha256'] == {name: sha256(root / name) for name in source.files}
        assert custody['files_sha256'] == {name: artifacts[name] for name in source.files}
