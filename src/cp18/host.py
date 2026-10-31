"""The issuing host's files, in place before the H2 gate: the pinned files materialized by hash, the binary, the zip.

The product repository commits the files the freeze manifest pins but GitHub cannot retrieve by hash, at
`live/pinned/<path>`, mirroring each one's project-relative runtime path with its leading `.local/` written `local/`:
- Pyodide 0.28.0's 23 files (`cp17.runtime.PYODIDE_DIR`);
- A1's search state S_13 (`cp17.runtime.K13`), the freeze-origin states of v4, v2 and B0 (`cp17.runtime.FREEZE_STATE`)
  and the canary's payload (`cp17.runtime.CANARY_DIR`), which decisions 26 and 27 let the public repository hold.

`materialize` copies each to its runtime path and checks it against the freeze manifest's hash; any absent or altered
file refuses the run before the gate. The binary is never committed: each run retrieves the tarball and
`SHASUMS256.txt` and checks all three by hash (`cp17.runtime.retrieve`). The package zip is rebuilt from `src/` and
compared with the manifest (`cp17.tools.bundle.build`). The H2 gate then checks all of it again, independently.
"""
from __future__ import annotations

import json
from pathlib import Path
import shutil

PINNED = 'live/pinned'
MANIFEST = 'docs/track-b/evidence/cp-17c/freeze-manifest.json'
PACKAGE_ZIP = '.local/artifacts/cp-17c/bundle/src.zip'


def pinned_files(root) -> dict[str, str]:
    """{runtime path: frozen SHA-256} for every pinned local file the manifest names."""
    from cp17 import runtime
    identity = json.loads((Path(root) / MANIFEST).read_text())['policy_identity']
    route = identity['state_route']
    files = {f'{runtime.PYODIDE_DIR}/{name}': sha for name, sha in identity['issuing_host']['pyodide']['files_sha256'].items()}
    files[route['k13']['path']] = route['k13']['file_sha256']
    files[route['freeze_origin_state']['path']] = route['freeze_origin_state']['file_sha256']
    files.update({f"{route['canary_payload']['path']}/{name}": sha for name, sha in route['canary_payload']['files_sha256'].items()})
    return dict(sorted(files.items()))


def committed_path(runtime_path: str) -> str:
    if not runtime_path.startswith('.local/'):
        raise ValueError(f'{runtime_path}: a pinned runtime file lives under .local/')
    return f"{PINNED}/local/{runtime_path.removeprefix('.local/')}"


def materialize(root, project) -> dict:
    """Copy each committed pinned file to its runtime path in `project`, checked by hash. Raises on any mismatch."""
    from cp17 import runtime
    root, project = Path(root), Path(project)
    out = {}
    for rel, sha in pinned_files(root).items():
        source, target = root / committed_path(rel), project / rel
        if target.is_file() and runtime.sha256_file(target) == sha:
            out[rel] = {'sha256': sha, 'action': 'already in place'}
            continue
        if not source.is_file() or runtime.sha256_file(source) != sha:
            raise RuntimeError(f'{committed_path(rel)}: absent or not the pinned file')
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if runtime.sha256_file(target) != sha:
            raise RuntimeError(f'{rel}: the copy is not the pinned file')
        out[rel] = {'sha256': sha, 'action': 'copied', 'from': committed_path(rel)}
    return out


def package(root, project) -> dict:
    """Rebuild the frozen package zip from `src/` and compare it with the manifest."""
    from cp17.tools import bundle
    root, project = Path(root), Path(project)
    built = bundle.build(root / 'src', project / PACKAGE_ZIP)
    code = json.loads((root / MANIFEST).read_text())['policy_identity']['code']
    equal = built['zip_sha256'] == code['zip_sha256'] and built['package_sha256'] == code['package_sha256']
    return {'zip_sha256': built['zip_sha256'], 'package_sha256': built['package_sha256'], 'zip_bytes': built['zip_bytes'],
            'equal_to_manifest': equal}


def node(project, retrieve: bool) -> dict:
    """The official binary: retrieved and checked by hash (`retrieve=True`, the runner), or checked in place."""
    from cp17 import runtime
    if retrieve:
        return runtime.retrieve(project)
    found = runtime.check_binary(project)
    if found['problems']:
        raise RuntimeError('the official binary is not in place: ' + '; '.join(found['problems']))
    return {'version': runtime.NODE_VERSION, 'in_place': True, 'node': found['node']}
