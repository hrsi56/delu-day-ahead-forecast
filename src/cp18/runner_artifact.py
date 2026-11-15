"""The runner's Actions artifact holds the Space's whole build (CP-18d item 4), so that a public check can verify a
runner-published Space from the artifact alone, without assembling it.

    python -m cp18.runner_artifact record --build "$RESULTS/space" --out "$RESULTS/space-artifact.json"
    python -m cp18.runner_artifact verify --artifact <the downloaded results folder> [--out <report.json>]

**Why.** The daily workflow's results step deletes every fitted-arrays file (`*-arrays.npz`) before the results are
uploaded, and PRES-6's landing found the artifact held only the changed files, without the dotfile `.gitattributes`.
The `run` job now keeps the whole build in its results (uploaded with hidden files) and, before the deletion, records
what the build is and which arrays the deletion removes on purpose.

**record** reads the build's own record, `app/space-build.json` (every served file but itself, with its SHA-256 and
bytes), and `app/history-files.json` when the build carries it (History's files, bound by its hash in the build
record). It lists every recorded file, and the build record itself, with its path, bytes, SHA-256, whether it is
present in the build folder and whether it matches; and every `*-arrays.npz` under the build (the fitted arrays the
results step deletes) with its path, bytes and SHA-256. It refuses (exit 1, the record written with its problems) when
a recorded file is missing or differs, before anything is deleted. No timestamp: the same build gives the same bytes.

**verify** reads the record from the downloaded results folder (`space-artifact.json`, the build in the folder it
names): the build record and History's listing in the artifact must hash as recorded and list exactly the recorded
files; every recorded file is present with its SHA-256 and bytes, except exactly the listed deleted arrays, which are
fitted-arrays files and must be absent. Nothing else counts: other files of the results folder, and any unrecorded
file in the build, are outside the check (the latter are reported, not judged). Exit 0 verified, 1 not, with a JSON
report.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import sys

SCHEMA = 'cp18d-runner-artifact-v1'
VERIFY_SCHEMA = 'cp18d-runner-artifact-verify-v1'
BUILD_RECORD = 'app/space-build.json'
HISTORY_LISTING = 'app/history-files.json'
ARRAYS = '*-arrays.npz'
RECORD_NAME = 'space-artifact.json'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def is_arrays(path: str) -> bool:
    return fnmatch.fnmatch(Path(path).name, ARRAYS)


def recorded_files(build: Path) -> tuple[dict[str, dict], list[str]]:
    """{path: {'sha256', 'bytes', 'listed_in'}} for every file the build's own record lists, History's listing and the
    build record itself; and the problems found reading them."""
    build = Path(build)
    problems = []
    record_path = build / BUILD_RECORD
    if not record_path.is_file():
        return {}, [f'{BUILD_RECORD}: the build record is missing']
    data = record_path.read_bytes()
    try:
        record = json.loads(data)
        rows = record['files']
        rows = rows if isinstance(rows, list) else [{'path': k, **v} for k, v in rows.items()]
    except (ValueError, KeyError, TypeError, AttributeError) as exc:
        return {}, [f'{BUILD_RECORD}: not a build record ({type(exc).__name__})']
    files = {BUILD_RECORD: {'sha256': sha(data), 'bytes': len(data), 'listed_in': 'itself'}}
    for row in rows:
        files[row['path']] = {'sha256': row['sha256'], 'bytes': row['bytes'], 'listed_in': BUILD_RECORD}
    history = build / HISTORY_LISTING
    if history.is_file():
        if HISTORY_LISTING not in files:
            problems.append(f'{HISTORY_LISTING} is in the build but its record does not list it')
        else:
            try:
                for row in json.loads(history.read_bytes())['files']:
                    if row['path'] in files:
                        problems.append(f"{row['path']}: listed twice")
                    files[row['path']] = {'sha256': row['sha256'], 'bytes': row['bytes'], 'listed_in': HISTORY_LISTING}
            except (ValueError, KeyError, TypeError) as exc:
                problems.append(f'{HISTORY_LISTING}: not a listing ({type(exc).__name__})')
    return files, problems


def present_files(build: Path) -> list[str]:
    build = Path(build)
    return sorted(p.relative_to(build).as_posix() for p in build.rglob('*') if p.is_file())


def record(build: Path, out: Path) -> dict:
    """The record of the build before the results step deletes its fitted arrays; `ok` False refuses."""
    build, out = Path(build).resolve(), Path(out).resolve()
    files, problems = recorded_files(build)
    rows = []
    for path, want in sorted(files.items()):
        target = build / path
        row = {'path': path, 'sha256': want['sha256'], 'bytes': want['bytes'], 'listed_in': want['listed_in'],
               'present': target.is_file()}
        if row['present']:
            data = target.read_bytes()
            row['matches'] = sha(data) == want['sha256'] and len(data) == want['bytes']
            if not row['matches']:
                problems.append(f'{path}: differs from the build record')
        else:
            row['matches'] = False
            problems.append(f'{path}: recorded, missing from the build')
        rows.append(row)
    here = present_files(build)
    arrays = []
    for path in here:
        if is_arrays(path):
            data = (build / path).read_bytes()
            arrays.append({'path': path, 'sha256': sha(data), 'bytes': len(data), 'recorded': path in files})
    try:
        folder = Path(os.path.relpath(build, out.parent)).as_posix()
    except ValueError:                     # another drive (never on the runner): the build's own name
        folder = build.name
    return {
        'schema': SCHEMA, 'ok': not problems, 'problems': problems,
        'build_folder': folder,
        'build_record': {'path': BUILD_RECORD, **{k: files[BUILD_RECORD][k] for k in ('sha256', 'bytes')}}
        if BUILD_RECORD in files else None,
        'history_listing': {'path': HISTORY_LISTING, 'sha256': files[HISTORY_LISTING]['sha256'],
                            'bytes': files[HISTORY_LISTING]['bytes']} if HISTORY_LISTING in files else None,
        'files': rows, 'deleted_arrays': arrays,
        'unrecorded': sorted(p for p in here if p not in files and not is_arrays(p)),
        'note': ('every file of the build record (and the record itself) with its hash; the fitted arrays listed under '
                 'deleted_arrays are removed by the results step on purpose before the upload, and a public check '
                 'verifies the served copies of those against these hashes'),
    }


def verify(artifact: Path, record_file: Path | None = None) -> dict:
    """The downloaded results folder against its record: the whole build but exactly the deleted arrays."""
    artifact = Path(artifact)
    record_file = Path(record_file) if record_file else artifact / RECORD_NAME
    report = {'schema': VERIFY_SCHEMA, 'artifact': str(artifact), 'record': str(record_file), 'ok': False,
              'problems': []}
    problems = report['problems']
    try:
        rec = json.loads(record_file.read_text())
    except (OSError, ValueError) as exc:
        problems.append(f'{record_file.name}: unreadable ({type(exc).__name__})')
        return report
    if rec.get('schema') != SCHEMA:
        problems.append(f"{record_file.name}: schema {rec.get('schema')!r}, expected {SCHEMA}")
        return report
    if not rec.get('ok'):
        problems.append(f'{record_file.name}: the record itself refused the build ({len(rec.get("problems") or [])} '
                        'problems)')
    build = (record_file.parent / rec['build_folder']).resolve()
    report['build'] = str(build)
    files, read_problems = recorded_files(build)
    problems += read_problems
    recorded = {r['path']: r for r in rec.get('files') or []}
    if rec.get('build_record') is None or files.get(BUILD_RECORD, {}).get('sha256') != rec['build_record']['sha256']:
        problems.append(f'{BUILD_RECORD}: not the recorded build record')
    if (rec.get('history_listing') or {}).get('sha256') != (files.get(HISTORY_LISTING) or {}).get('sha256'):
        problems.append(f'{HISTORY_LISTING}: not the recorded History listing')
    mine = {p: (v['sha256'], v['bytes']) for p, v in files.items()}
    theirs = {p: (r['sha256'], r['bytes']) for p, r in recorded.items()}
    if mine != theirs:
        problems.append(f'the record lists {len(theirs)} files, the build record in the artifact {len(mine)}: '
                        f'{len(set(theirs) ^ set(mine))} differ by path, '
                        f'{sum(theirs[p] != mine[p] for p in set(theirs) & set(mine))} by hash')
    deleted = {a['path']: a for a in rec.get('deleted_arrays') or []}
    for path, a in sorted(deleted.items()):
        if not is_arrays(path):
            problems.append(f'{path}: listed as deleted but not a fitted-arrays file ({ARRAYS})')
        elif (build / path).exists():
            problems.append(f'{path}: listed as deleted but present')
        if path in files and (files[path]['sha256'], files[path]['bytes']) != (a['sha256'], a['bytes']):
            problems.append(f'{path}: the deleted copy\'s hash is not the build record\'s')
    checked = 0
    for path, want in sorted(files.items()):
        if path in deleted:
            continue
        target = build / path
        if not target.is_file():
            problems.append(f'{path}: missing')
            continue
        data = target.read_bytes()
        if sha(data) != want['sha256'] or len(data) != want['bytes']:
            problems.append(f'{path}: differs')
            continue
        checked += 1
    here = present_files(build) if build.is_dir() else []
    report.update(ok=not problems, files_recorded=len(files), files_verified=checked,
                  deleted_absent=sorted(p for p in deleted if not (build / p).exists()),
                  outside_the_check=sorted(p for p in here if p not in files),
                  rule=('every file of the build record (and the record itself, and History\'s listing) present with '
                        'its SHA-256 and bytes, except exactly the deleted fitted arrays, which must be absent; '
                        'nothing else counts'))
    return report


def dump(path: Path, value) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=1, sort_keys=True) + '\n')


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='python -m cp18.runner_artifact', description=__doc__.split('\n\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('record', help='the build and the arrays the results step deletes, before the deletion')
    r.add_argument('--build', required=True, type=Path)
    r.add_argument('--out', required=True, type=Path)
    v = sub.add_parser('verify', help='a downloaded results folder against its record')
    v.add_argument('--artifact', required=True, type=Path)
    v.add_argument('--record', type=Path, help=f'the record (default: <artifact>/{RECORD_NAME})')
    v.add_argument('--out', type=Path)
    args = ap.parse_args(argv)
    if args.cmd == 'record':
        value = record(args.build, args.out)
        dump(args.out, value)
        print('runner artifact |', len(value['files']), 'files recorded |', len(value['deleted_arrays']),
              'fitted arrays to be deleted |', 'ok' if value['ok'] else 'REFUSED: ' + '; '.join(value['problems'][:3]),
              flush=True)
        return 0 if value['ok'] else 1
    value = verify(args.artifact, args.record)
    if args.out:
        dump(args.out, value)
    print(json.dumps(value, indent=1, sort_keys=True))
    return 0 if value['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
