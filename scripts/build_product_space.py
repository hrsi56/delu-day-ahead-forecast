#!/usr/bin/env python3
"""Assemble the final-product Space (A9; CP-18b) from `space-product/`, the pinned runtime and one dated bundle.

    PYTHONPATH=src python scripts/build_product_space.py --bundle <dated bundle> --out <dist> [--live <live folder>] \\
        [--history <v1 build dir> [--history-note TEXT] [--history-gitattributes FILE] [--history-listing FILE]] \\
        [--allow-refused]

The served layout is fixed by the frozen "Train it yourself" worker (`src/cp17/browser/worker.js`, served byte for
byte at `/app/worker.js`): `/index.html`, `/app/...`, `/pyodide/<the 23 pinned files>`, `/bundle/src.zip` (the frozen
package), `/payloads/<the dated bundle>` and, when given, `/history/` (v1's demo as it is).

**It refuses** (exit 1, with the reason) unless `cp18.r7.verify` accepts the bundle and `cp18.bundle.gate` finds it
publishable; `--allow-refused` builds anyway for the acceptance's negative controls and stamps the build record
`refused`. It also refuses any Pyodide file, the package zip or the frozen worker that differs from the CP-17c freeze
manifest's hashes.

**What it writes besides the copies:**

- `app/claims.json`: the live claims (`cp18.live_claims.build_live_claims`, with the bundle's first and last issued day),
  the shared record sentences and the limitations as label, key and text. The page reads every status, badge, wording
  and limitation sentence from here.
- `app/space-build.json`: every served file with its SHA-256 and bytes (all but this record itself); the glue's and the
  frozen worker's SHA-256; the bundle manifest's SHA-256 and the gate's verdict; the Pyodide and zip checks; the
  reference measurements (`reports/cp17/host-parity.json`'s A1 browser runs); and the size budget: what the page loads
  at start against what loads on request, by action.
- `README.md`: the Hugging Face Static Space card, its text from the live claims. Written, never published.
- `.gitattributes`: Git LFS rules for the binary files (a Space repository needs them for files over 10 MB).

**With `--live <live folder>` (CP-18c)** the build reads the live store (`cp18.store.LiveStore`, verified) through
`cp18.live_claims.live_record` and writes `app/live-record.json`, loaded at start and listed with its hash: every issued
day's cutoff-based issue time and its actual run (start, issuance start and end, run and host), every failed issuance,
every day not issued with its cause, the days outside the live record as one range, the runs; and O33's running means
with their 95% intervals, computed here natively by `cp18.running.running` on the bundle's evaluation windows (the
page draws them and never recomputes them). The claims are then the live product's (`build_live_claims(live=...)`).
The issued days and artifacts of the live record must be the bundle's, or the build refuses. Without `--live` the build
is CP-18b's, unchanged.

**History (O17, CP-18c):** `--history` is copied as it is to `history/`; `--history-gitattributes` (default: a
`gitattributes` file beside the `--history` folder) is placed byte for byte at `history/.gitattributes`; and when a
listing of the deployed files is given (`--history-listing`, default: a `listing.json` beside the folder), every copied
file must equal it, path, bytes and SHA-256, or the build refuses. `app/history-files.json` binds them all.

**Decision 31 (CP-18d).** A live build also writes, in `app/live-record.json`, the evaluation per input class
(`cp18.evaluation.class_sets`: the prospective record's issued days with every input before the cutoff on their own,
and all issued days beside them, each with its count) and the running intervals per set
(`cp18.running.running(..., classes=)`), both computed here from the served bundle and each issued day's class in the
live store; the bundle's own files keep the frozen schema. It refuses (`Refused`) a live record whose issued day has no
input class, or whose label is not its class's, a running record without both sets, and evaluation sets without both
sets or whose counts are not the record's.

**v1's preview tags (CP-18d; PRES-5's A12 review, R3).** The static host injects one run of Open Graph and Twitter tags
naming the Space card ("v6 · DDNN-2 alone") into every served page. After the copy is checked against the deployed
listing, the build adds v1's own preview tags to `history/index.html`'s head (the claims' `live_history_preview_title`
and `live_history_preview_description`), written so that `cp18.publish.HF_META_RUN` never matches them (`content`
first, ` />`), so the served page's normalization still finds exactly the host's run. Nothing else of v1 changes:
`app/history-files.json` lists `index.html` with its new hash, its deployed hash and bytes, and the one inserted span
(its byte offset, bytes and SHA-256), so the deployed page is the served page without that span.

The output is deterministic: no timestamps, sorted listings, the same inputs give the same bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

SCHEMA = 'cp18d-space-build-v1'                    # CP-18d: v1's preview tags in the history record; decision 31's data
SOURCE = ROOT / 'space-product'
FROZEN_WORKER = ROOT / 'src/cp17/browser/worker.js'
GLUE = ROOT / 'src/cp18/spaceglue.py'
FREEZE_MANIFEST = ROOT / 'docs/track-b/evidence/cp-17c/freeze-manifest.json'
HOST_PARITY = ROOT / 'reports/cp17/host-parity.json'
#: The files the page itself loads at start, beside the bundle's start records (`cp18.bundle.START_FILES`).
PAGE_START = ('index.html', 'app/style.css', 'app/charts.js', 'app/main.js', 'app/claims.json', 'app/space-build.json',
              'app/live-record.json')
LIVE_RECORD = 'app/live-record.json'
LIVE_SCHEMA = 'cp18d-space-live-v1'                 # CP-18d: with `evaluation_sets` and the running intervals per set
HISTORY_SCHEMA = 'cp18d-space-history-files-v1'     # CP-18d: index.html carries v1's own preview tags, recorded
HISTORY_PAGE = 'history/index.html'
#: The two sets of decision 31, in the order the records carry them (`cp18.evaluation.SETS`, `cp18.running.SETS`).
SETS = ('before_cutoff', 'all')
#: The runtime files Pyodide's loader fetches (pyodide.mjs is served with the release and never loaded by a worker).
RUNTIME_LOADED = ('pyodide.js', 'pyodide.asm.js', 'pyodide.asm.wasm', 'python_stdlib.zip', 'pyodide-lock.json')
GITATTRIBUTES = ''.join(f'*.{ext} filter=lfs diff=lfs merge=lfs -text\n'
                        for ext in ('wasm', 'whl', 'zip', 'npz', 'png', 'ico', 'woff2', 'woff', 'ttf'))
REPORT_URL = 'https://hrsi56.github.io/delu-day-ahead-forecast/'


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dump(value) -> str:
    return json.dumps(value, indent=1, sort_keys=True, ensure_ascii=False, allow_nan=False) + '\n'


class Refused(Exception):
    pass


# ------------------------------------------------------------------ inputs
def project_root() -> Path:
    from cp17 import runtime
    return Path(runtime.project_root(ROOT))


def check_bundle(files: dict[str, bytes]) -> dict:
    """R7's verification, then the publication gate (which repeats R7 and recomputes natively)."""
    from cp18 import bundle, r7
    verified = r7.verify(files)
    verdict = bundle.gate(files)
    recompute = verdict.get('recompute') or {}
    return {'r7_accepted': verified['accepted'], 'r7_problems': verified['problems'],
            'publishable': bool(verified['accepted'] and verdict['publishable']), 'reason': verdict.get('reason'),
            'gate_problems': verdict['verify']['problems'],
            'recompute': None if not recompute else {
                'match': recompute.get('match'), 'blocks_publication': recompute.get('blocks_publication'),
                'recomputed_windows': recompute.get('recomputed_windows'), 'error': recompute.get('error')}}


def pyodide_files(folder: Path, freeze: dict) -> dict:
    expected = freeze['policy_identity']['issuing_host']['pyodide']['files_sha256']
    checks = {}
    for name in sorted(expected):
        path = folder / name
        if not path.is_file():
            raise Refused(f'pyodide: {name} is absent from {folder}')
        got = sha(path.read_bytes())
        if got != expected[name]:
            raise Refused(f'pyodide: {name} hashes {got[:16]}..., the freeze manifest records {expected[name][:16]}...')
        checks[name] = {'sha256': got, 'bytes': path.stat().st_size, 'matches_freeze_manifest': True}
    return checks


def loaded_packages(folder: Path, packages: list[str]) -> list[str]:
    """The package files `loadPackage(packages)` fetches: the named packages and their dependencies, by the lock."""
    lock = json.loads((folder / 'pyodide-lock.json').read_text())['packages']
    seen, order = set(), []

    def add(name):
        name = name.lower()
        if name in seen:
            return
        seen.add(name)
        for dep in lock[name].get('depends', []):
            add(dep)
        order.append(lock[name]['file_name'])
    for name in packages:
        add(name)
    return sorted(order)


def reference_measurements(claims: dict) -> dict:
    """The A1 browser runs of CP-17's host parity, read as recorded; the measurement date from the visitor wording."""
    parity = json.loads(HOST_PARITY.read_text())
    m = re.search(r'measured (\d{4}-\d{2}-\d{2})', claims['values']['live_retrain_wording'])
    runs = [{'browser': r['browser'], 'browser_version': r['browser_version'], 'stem': r['stem'],
             'fit_seconds': r['time_seconds']['fit'], 'total_in_worker_seconds': r['time_seconds']['total_in_worker'],
             'payload_bytes_raw': r['payload_bytes']['raw'], 'runtime': r['runtime'],
             'status_vs_issuing_host': r['status_vs_issuing_host']}
            for r in parity['browser_runs'] if r['policy'] == 'A1']
    return {'source': 'reports/cp17/host-parity.json (browser_runs, policy A1)', 'runs': runs,
            'measured_date': m.group(1) if m else None,
            'measured_date_source': 'live_retrain_wording', 'machine': parity['browser_host']}


def issued_days(files: dict[str, bytes]) -> list[str] | None:
    """The bundle's issued days; None when its issued forecasts do not parse (a refused bundle, built for a control)."""
    try:
        return sorted(d['delivery_day'] for d in json.loads(files['issued-forecasts.json'])['days'])
    except (ValueError, KeyError, TypeError):
        return None


def claims_for(files: dict[str, bytes], live: dict | None = None) -> dict:
    from cp18.live_claims import build_live_claims, live_summary, text
    days = issued_days(files) or []
    if live is None:
        claims = build_live_claims(ROOT, rehearsal_days=(days[0], days[-1]) if days else ())
    else:
        claims = build_live_claims(ROOT, live=live_summary(live))
        days = []                                   # the live record is not a rehearsal
    return {'schema': 'cp18b-space-claims-v1', 'source': 'cp18.live_claims.build_live_claims',
            'mode': 'development rehearsal' if live is None else 'live',
            'rehearsal_days': [days[0], days[-1]] if days else [],
            'values': claims['values'], 'shared': claims['shared'],
            'limitations': [{'label': label, 'key': key, 'text': text(claims, key)} for label, key in claims['limitations']]}


def labels(record: dict) -> dict[str, str]:
    """Decision 31 (CP-18d): every issued and failed day of the live record names its input class, with its class's
    text, and a day labelled "load forecast fetched after the cutoff" names that copy's retrieval time; the counts per
    class are the issued days'. Returns each issued day's class; refuses anything else."""
    from cp18 import inputclass
    for item in record.get('issued', []) + record.get('failed', []):
        day = item.get('day')
        cls = item.get('input_class')
        if cls not in inputclass.TEXT:
            raise Refused(f'the live record\'s day {day} has no input class (decision 31\'s label is missing): {cls!r}')
        if item.get('input_class_text') != inputclass.TEXT[cls]:
            raise Refused(f'the live record\'s day {day}: its label text is not its class\'s')
        fetched = item.get('load_forecast_fetched_utc')
        if (cls == inputclass.AFTER) != bool(isinstance(fetched, str) and fetched):
            raise Refused(f'the live record\'s day {day}: a day labelled {inputclass.TEXT[inputclass.AFTER]!r} needs '
                          'its copy\'s retrieval time, and only such a day has one')
    counts = {c.get('input_class'): c.get('issued') for c in record.get('input_classes') or []}
    want = {c: sum(1 for i in record.get('issued', []) if i['input_class'] == c) for c in inputclass.ORDER}
    if counts != want:
        raise Refused(f'the live record\'s counts per input class {counts} are not its issued days\' {want}')
    return {item['day']: item['input_class'] for item in record.get('issued', [])}


def check_sets(record: dict, intervals: dict | None, sets: dict | None) -> None:
    """Decision 31 (CP-18d): the running record and the evaluation sets each carry both sets, before the cutoff then
    all, with the live record's counts of issued days (None: not computed, only for a refused bundle's control)."""
    from cp18 import inputclass
    issued = record.get('issued', [])
    want = {'before_cutoff': sum(1 for i in issued if i['input_class'] == inputclass.BEFORE), 'all': len(issued)}
    if intervals is not None:
        got = [s.get('set') for s in intervals.get('sets') or []]
        if got != list(SETS):
            raise Refused(f'the running intervals do not carry both sets of decision 31 ({got}, not {list(SETS)})')
        for s in intervals['sets']:
            if s.get('issued_days') != want[s['set']]:
                raise Refused(f"the running set {s['set']} counts {s.get('issued_days')} issued days, the record "
                              f"{want[s['set']]}")
    if sets is None:
        return
    got = [s.get('set') for s in sets.get('sets') or []]
    if got != list(SETS):
        raise Refused(f'the evaluation sets do not carry both sets of decision 31 ({got}, not {list(SETS)})')
    for s in sets['sets']:
        if s.get('issued_days') != want[s['set']] or len(s.get('days') or []) != want[s['set']]:
            raise Refused(f"the evaluation set {s['set']} counts {s.get('issued_days')} issued days, the record "
                          f"{want[s['set']]}")
        if [w.get('policy') for w in s.get('windows') or []] != ['product', 'B0']:
            raise Refused(f"the evaluation set {s['set']} does not hold the product's and B0's records")


def live_data(live_folder: Path, files: dict[str, bytes], refused: bool) -> dict:
    """`app/live-record.json`: the live store's record (`cp18.live_claims.live_record`), O33's running intervals
    (`cp18.running.running` on the bundle's evaluation windows) and, by the Owner's decision 31 (CP-18d), the
    evaluation per input class (`cp18.evaluation.class_sets`) and the running intervals per set, from each issued
    day's class in the live store. The record's issued days and artifacts must be the bundle's (a refused bundle, built
    for a control, is checked as far as it parses); decision 31's label and both sets are required either way."""
    from cp18 import evaluation, running
    from cp18.live_claims import live_record
    try:
        record = live_record(live_folder)
    except Exception as exc:                        # an unverifiable store is never shown
        raise Refused(f'the live store does not verify: {type(exc).__name__}: {exc}') from None
    classes = labels(record)
    ours = {d['day']: d['artifact_sha256'] for d in record['issued']}
    try:
        forecasts = json.loads(files['issued-forecasts.json'])
        theirs = {d['delivery_day']: d['issuing_artifact_sha256'] for d in forecasts['days']}
    except (KeyError, ValueError, TypeError):
        theirs = None
    if theirs is None and not refused:
        raise Refused('the bundle\'s issued forecasts do not parse')
    if theirs is not None and theirs != ours:
        raise Refused('the live record and the bundle name different issued days or artifacts: '
                      f'record {sorted(ours.items())[-3:]}, bundle {sorted(theirs.items())[-3:]}')
    try:
        windows = json.loads(files['evaluation.json'])['windows']
        intervals = running.running(windows, classes=classes)
    except (KeyError, ValueError, TypeError) as exc:
        if not refused or 'input class' in str(exc):
            raise Refused(f'the running intervals could not be computed: {type(exc).__name__}: {exc}') from None
        intervals = None
    try:
        sets = evaluation.class_sets(files, classes)
    except (KeyError, ValueError, TypeError) as exc:
        if not refused or 'input class' in str(exc):
            raise Refused(f'the evaluation per input class could not be computed: {type(exc).__name__}: {exc}') from None
        sets = None
    check_sets(record, intervals, sets)            # both are always computed for a publishable bundle
    return {'schema': LIVE_SCHEMA, 'bundle_manifest_sha256': sha(files['manifest.json']),
            'record': record, 'running': intervals, 'evaluation_sets': sets,
            'running_source': ('cp18.running.running(evaluation.json windows, classes=the live store\'s input classes), '
                               'computed at build time'),
            'evaluation_sets_source': ('cp18.evaluation.class_sets(the served bundle, the live store\'s input classes), '
                                       'computed at build time; not part of the bundle, whose files keep the frozen '
                                       'schema')}


def copy_history(history: Path, out: Path, gitattributes: Path | None, listing_file: Path | None) -> dict:
    """v1's deployed files, as they are, to `out/history/`; its `.gitattributes` byte for byte; checked against the
    deployed listing when one is given."""
    skipped = []
    for path in sorted(Path(history).rglob('*')):
        rel = path.relative_to(history)
        if path.name == '.DS_Store':
            skipped.append(rel.as_posix())
            continue
        if path.is_file():
            target = out / 'history' / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
    info = {}
    if gitattributes is not None:
        target = out / 'history/.gitattributes'
        if target.exists() and target.read_bytes() != Path(gitattributes).read_bytes():
            raise Refused('history: the folder holds a .gitattributes that is not the given one')
        target.write_bytes(Path(gitattributes).read_bytes())
        info['gitattributes'] = {'path': 'history/.gitattributes', 'sha256': sha(target.read_bytes()),
                                 'bytes': target.stat().st_size, 'source_sha256': sha(Path(gitattributes).read_bytes())}
    if listing_file is not None:
        listing = json.loads(Path(listing_file).read_text())
        want = {f['path']: (f['sha256'], f['bytes']) for f in listing['files']}
        have = {p.relative_to(out / 'history').as_posix(): (sha(p.read_bytes()), p.stat().st_size)
                for p in (out / 'history').rglob('*') if p.is_file()}
        if have != want:
            extra, missing = sorted(set(have) - set(want)), sorted(set(want) - set(have))
            differ = sorted(k for k in set(have) & set(want) if have[k] != want[k])
            raise Refused(f'history: the files are not the deployed listing ({len(extra)} extra {extra[:3]}, '
                          f'{len(missing)} missing {missing[:3]}, {len(differ)} differ {differ[:3]})')
        info['deployed_listing'] = {'source_sha256': sha(Path(listing_file).read_bytes()), 'files': len(want),
                                    'space': listing.get('space'), 'revision': listing.get('revision'),
                                    'matches': True}
    info['skipped'] = skipped or None
    return info


def _attr(text: str) -> str:
    return text.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def preview_tags(title: str, description: str, indent: str = '    ') -> bytes:
    """v1's own preview tags (CP-18d): `content` first and ` />`, so `cp18.publish.HF_META_RUN` (the host's run, written
    `<meta property|name="og:|twitter:..." content="...">`) never matches one of them."""
    from cp18.publish import HF_META_RUN
    rows = [f"{indent}<!-- v1's own preview tags, added by the product Space's build (CP-18d); the page is otherwise "
            "v1's deployed page -->"]
    for attr, key, value in (('property', 'og:title', title), ('property', 'og:description', description),
                             ('name', 'twitter:title', title), ('name', 'twitter:description', description)):
        rows.append(f'{indent}<meta content="{_attr(value)}" {attr}="{key}" />')
    data = ('\n'.join(rows) + '\n').encode('utf-8')
    if HF_META_RUN.search(data):
        raise Refused("v1's preview tags would be taken for the host's injection (cp18.publish.HF_META_RUN)")
    return data


def history_preview(out: Path, values: dict, required: bool) -> dict:
    """Add v1's own preview tags to `history/index.html`'s head, after its charset declaration when that opens the head
    (else right after `<head>`). `required` (a deployed listing was given): a page without a head refuses the build;
    otherwise (a local stand-in) the page is left as it is and the record says so."""
    page = out / HISTORY_PAGE
    data = page.read_bytes() if page.is_file() else b''
    i = data.find(b'<head>')
    if i < 0 or data.find(b'</head>') < i:
        if required:
            raise Refused(f'{HISTORY_PAGE} has no <head>: v1\'s preview tags cannot be added')
        return {'added': False, 'reason': f'{HISTORY_PAGE} has no <head> (a local stand-in): no preview tags added'}
    at = i + len(b'<head>')
    charset = re.compile(rb'[ \t]*\n?[ \t]*<meta charset="[^"]*"\s*/?>[ \t]*\n').match(data, at)
    if charset:
        at = charset.end()
    tags = preview_tags(values['live_history_preview_title'], values['live_history_preview_description'],
                        indent='    ' if charset else '')
    served = data[:at] + tags + data[at:]
    page.write_bytes(served)
    return {'added': True, 'path': HISTORY_PAGE, 'deployed_sha256': sha(data), 'deployed_bytes': len(data),
            'sha256': sha(served), 'bytes': len(served), 'inserted_at_byte': at, 'inserted_bytes': len(tags),
            'inserted_sha256': sha(tags), 'tags': tags.decode('utf-8'),
            'claims': ['live_history_preview_title', 'live_history_preview_description'],
            'note': ("v1's deployed page with its own preview tags added (CP-18d): the one change is the span of "
                     "`inserted_bytes` bytes at byte `inserted_at_byte`; without it the page is the deployed one "
                     "(`deployed_sha256`). Every other v1 file is byte for byte the deployed one.")}


# ------------------------------------------------------------------ outputs
def label_text(item: dict | None, values: dict) -> str | None:
    """An issued day's input class as the page words it (decision 31): the claims' label, and for a day with the load
    forecast fetched after the cutoff, that copy's retrieval time (UTC, to the second)."""
    if not item or not item.get('input_class'):
        return None
    if item['input_class'] == 'load_forecast_after_cutoff':
        when = item['load_forecast_fetched_utc'][:19].replace('T', ' ')
        return (f"{values['live_input_class_load_forecast_after_cutoff']}, "
                + values['live_input_class_fetched'].replace('{time}', when))
    return values['live_input_class_before_cutoff']


def card(claims: dict, manifest: dict, refused: bool, record: dict | None = None) -> str:
    v, s = claims['values'], claims['shared']
    day = manifest['artifact']['delivery_day']
    served = label_text(next((i for i in (record or {}).get('issued', []) if i['day'] == day), None), v)
    lines = ['---', f"title: {json.dumps(v['live_product_name'], ensure_ascii=False)}", 'sdk: static',
             'app_file: index.html', 'pinned: false', '---', '', f"# {v['live_product_name']}", '',
             f"**Status:** {v['live_product_status']}. {v['live_released_product']}.", '',
             f"**{v['live_prospective_label']}.** {v['live_hero_rule']}", '',
             f"**Evidence:** {manifest['product']['evidence_label']}", '',
             f"**Served identity:** policy identity `{manifest['policy']['policy_identity_sha256']}`, package "
             f"`{manifest['policy']['package_sha256']}`, issuing host {manifest['policy']['issuing_host']}, daily "
             f"artifact `{manifest['artifact']['artifact_sha256']}` ({day}" + (f'; {served}' if served else '') + ').', '',
             f"The static report: [{REPORT_URL}]({REPORT_URL}) (external).", '']
    if refused:
        lines += ['**This build is refused:** its bundle did not pass the publication gate; it exists for an '
                  'acceptance check only.', '']
    lines += ['## Limitations', '']
    lines += [f"- **{item['label']}.** {item['text']}" for item in claims['limitations']]
    lines += ['', s['attribution'], '']
    return '\n'.join(lines)


def size_budget(out: Path, start_records: tuple, packages: list[str], artifact: dict, record_bytes: int) -> dict:
    def b(rel):
        return (out / rel).stat().st_size if rel != 'app/space-build.json' else record_bytes

    def group(names):
        items = {n: b(n) for n in sorted(names) if (out / n).exists() or n == 'app/space-build.json'}
        return {'bytes': sum(items.values()), 'files': items}
    payloads = sorted(p.name for p in (out / 'payloads').iterdir())
    train_stem = f"{artifact['issued_policy']}-{artifact['delivery_day']}" if artifact.get('issued_policy') else None
    first = group(list(PAGE_START) + [f'payloads/{n}' for n in start_records])
    runtime = group([f'pyodide/{n}' for n in RUNTIME_LOADED])
    pk = group([f'pyodide/{n}' for n in packages])
    code_train = group(['bundle/src.zip', 'app/worker.js'])
    code_product = group(['bundle/src.zip', 'app/glue/spaceglue.py', 'app/product-worker.js'])
    training = group([f'payloads/{n}' for n in payloads if train_stem and n.startswith(train_stem + '.')])
    arrays = group(['payloads/artifact-arrays.npz'] if 'artifact-arrays.npz' in payloads else [])
    b0 = group([f'payloads/{n}' for n in payloads if n.startswith('B0-')])
    series = group(['payloads/series.json'] if 'series.json' in payloads else [])
    product_runtime = runtime['bytes'] + pk['bytes'] + code_product['bytes']
    on_request = {'runtime': runtime, 'packages': pk, 'code_train': code_train, 'code_product': code_product,
                  'training_window': training, 'fitted_arrays': arrays, 'b0_windows': b0, 'series': series}
    seen = set()
    for g in on_request.values():
        seen |= set(g['files'])
    return {
        'unit': 'bytes, uncompressed, as served',
        'first_visit': first,
        'on_request': on_request,
        'on_request_bytes': sum(b(n) for n in seen),
        'actions': {
            'train_it_yourself': {'bytes': runtime['bytes'] + pk['bytes'] + code_train['bytes'] + training['bytes'],
                                  'parts': {'runtime': runtime['bytes'], 'packages': pk['bytes'],
                                            'code': code_train['bytes'], 'training_window': training['bytes']},
                                  'stem': train_stem},
            'product_runtime': {'bytes': product_runtime,
                                'parts': {'runtime': runtime['bytes'], 'packages': pk['bytes'],
                                          'code': code_product['bytes']},
                                'note': 'loaded once per visit, by the first in-browser computation'},
            'recompute_data': {'bytes': b0['bytes']},
            'explain_data': {'bytes': arrays['bytes'] + training['bytes']},
            'data_view': {'bytes': series['bytes']},
        },
        'served_not_loaded': sorted(f'pyodide/{n}' for n in
                                    set(p.name for p in (out / 'pyodide').iterdir()) - set(RUNTIME_LOADED) - set(packages)),
        'not_counted': ('history/ (v1\'s demo, outside the product Space\'s network rule) and its listing '
                        'app/history-files.json, README.md and .gitattributes'),
    }


def listing(out: Path, history: bool = False) -> list[dict]:
    """Every served file with its SHA-256 and bytes: the product's (all but the build record itself), or history/'s."""
    rows = []
    for path in sorted(out.rglob('*')):
        rel = path.relative_to(out).as_posix()
        if not path.is_file() or rel == 'app/space-build.json' or rel.startswith('history/') != history:
            continue
        data = path.read_bytes()
        rows.append({'path': rel, 'sha256': sha(data), 'bytes': len(data)})
    return rows


def build(bundle_dir: Path, out: Path, *, history: Path | None = None, history_note: str | None = None,
          allow_refused: bool = False, pyodide: Path | None = None, package_zip: Path | None = None,
          live: Path | None = None, history_gitattributes: Path | None = None,
          history_listing: Path | None = None) -> dict:
    from cp17 import runtime
    from cp18 import bundle as B
    from cp18.host import PACKAGE_ZIP
    project = project_root()
    pyodide = Path(pyodide or project / runtime.PYODIDE_DIR)
    package_zip = Path(package_zip or project / PACKAGE_ZIP)
    files = B.read(bundle_dir)
    if 'manifest.json' not in files or 'issued-forecasts.json' not in files:
        raise Refused(f'{bundle_dir}: not a dated bundle (no manifest.json or issued-forecasts.json)')
    gate = check_bundle(files)
    if not gate['publishable'] and not allow_refused:
        raise Refused('the bundle is refused: ' + (gate['reason'] or '; '.join(gate['r7_problems'][:3])) +
                      (' -- ' + '; '.join(gate['gate_problems'][:3]) if gate['gate_problems'] else ''))
    freeze = json.loads(FREEZE_MANIFEST.read_text())
    code = freeze['policy_identity']['code']
    checks_pyodide = pyodide_files(pyodide, freeze)
    zip_bytes = package_zip.read_bytes()
    if sha(zip_bytes) != code['zip_sha256']:
        raise Refused(f"the package zip hashes {sha(zip_bytes)[:16]}..., the freeze manifest records {code['zip_sha256'][:16]}...")
    worker = FROZEN_WORKER.read_bytes()
    frozen_worker_sha = code['runner_files_sha256']['cp17/browser/worker.js']
    if sha(worker) != frozen_worker_sha:
        raise Refused('src/cp17/browser/worker.js differs from the frozen runner file')

    if out.exists():
        shutil.rmtree(out)
    (out / 'app/glue').mkdir(parents=True)
    for path in sorted(SOURCE.rglob('*')):
        if path.is_file() and path.name != '.DS_Store':
            target = out / path.relative_to(SOURCE)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
    (out / 'pyodide').mkdir()
    for name in checks_pyodide:
        (out / 'pyodide' / name).write_bytes((pyodide / name).read_bytes())
    (out / 'bundle').mkdir()
    (out / 'bundle/src.zip').write_bytes(zip_bytes)
    (out / 'app/worker.js').write_bytes(worker)
    if (out / 'app/worker.js').read_bytes() != FROZEN_WORKER.read_bytes():
        raise Refused('the served worker is not byte-identical to the frozen one')
    (out / 'app/glue/spaceglue.py').write_bytes(GLUE.read_bytes())
    (out / 'payloads').mkdir()
    for name, data in sorted(files.items()):
        (out / 'payloads' / name).write_bytes(data)
    history_info = {'present': False, 'note': history_note}
    copied = copy_history(Path(history), out, history_gitattributes, history_listing) if history is not None else None

    live_value = live_data(Path(live), files, not gate['publishable']) if live is not None else None
    claims = claims_for(files, live_value['record'] if live_value else None)
    if copied is not None:
        # v1's own preview tags (CP-18d), after the copy is checked against the deployed listing
        preview = history_preview(out, claims['values'], required=history_listing is not None)
        hist = [p for p in (out / 'history').rglob('*') if p.is_file()]
        history_info = {'present': True, 'note': history_note, 'files': len(hist),
                        'bytes': sum(p.stat().st_size for p in hist),
                        'index_sha256': sha((out / HISTORY_PAGE).read_bytes())
                        if (out / HISTORY_PAGE).is_file() else None, **copied, 'preview_tags': preview}
    if live_value and live_value['running'] and (
            live_value['running']['wording'] != claims['values']['live_running_wording']
            or live_value['running']['before_minimum'] != claims['values']['live_running_before_minimum']):
        raise Refused('the running intervals\' wording is not the claims\'')
    (out / 'app/claims.json').write_text(dump(claims), encoding='utf-8')
    if live_value is not None:
        (out / LIVE_RECORD).write_text(dump(live_value), encoding='utf-8')
    manifest = json.loads(files['manifest.json'])
    try:
        artifact = json.loads(files['artifact.json'])
    except (KeyError, ValueError):
        artifact = {}
    (out / 'README.md').write_text(card(claims, manifest, not gate['publishable'],
                                        live_value['record'] if live_value else None), encoding='utf-8')
    (out / '.gitattributes').write_text(GITATTRIBUTES, encoding='utf-8')

    packages = loaded_packages(pyodide, code['pyodide_packages'])
    record = {
        'schema': SCHEMA,
        'refused': not gate['publishable'],
        'gate': gate,
        'bundle': {'manifest_sha256': sha(files['manifest.json']), 'freshness': manifest['freshness'],
                   'artifact': manifest['artifact'], 'files': len(files),
                   'start_records': list(B.START_FILES[1:])},
        'identity': {'policy_identity_sha256': freeze['policy_identity_sha256'],
                     'package_sha256': code['package_sha256'], 'zip_sha256': code['zip_sha256']},
        'pyodide': {'version': freeze['policy_identity']['issuing_host']['pyodide']['version'],
                    'packages': code['pyodide_packages'], 'package_files': packages, 'files': checks_pyodide},
        'zip': {'path': 'bundle/src.zip', 'sha256': sha(zip_bytes), 'bytes': len(zip_bytes),
                'matches_freeze_manifest': True},
        'glue': {'path': 'app/glue/spaceglue.py', 'sha256': sha(GLUE.read_bytes()),
                 'source': 'src/cp18/spaceglue.py'},
        'frozen_worker': {'path': 'app/worker.js', 'sha256': sha(worker), 'frozen_sha256': frozen_worker_sha,
                          'byte_identical_to_source': True, 'source': 'src/cp17/browser/worker.js'},
        'claims_sha256': sha((out / 'app/claims.json').read_bytes()),
        'claims_rehearsal_days': claims['rehearsal_days'] or None,
        'claims_mode': claims['mode'],
        'live': None if live_value is None else {
            'path': LIVE_RECORD, 'sha256': sha((out / LIVE_RECORD).read_bytes()),
            'bytes': (out / LIVE_RECORD).stat().st_size, 'schema': live_value['schema'],
            'record_schema': live_value['record']['schema'], 'store': live_value['record']['store'],
            'issued_days': [d['day'] for d in live_value['record']['issued']],
            'running_schema': (live_value['running'] or {}).get('schema'),
            'running_points': None if not live_value['running'] else
            {k: len(v) for k, v in live_value['running']['series'].items()},
            # decision 31 (CP-18d): each issued day's class, and the two sets with their counts
            'input_classes': live_value['record']['input_classes'],
            'running_sets': None if not live_value['running'] else
            [{k: s[k] for k in ('set', 'issued_days', 'scored_days', 'paired_days')} for s in live_value['running']['sets']],
            'evaluation_sets': None if not live_value['evaluation_sets'] else
            [{'set': s['set'], 'issued_days': s['issued_days'], 'days': s['days']}
             for s in live_value['evaluation_sets']['sets']]},
        'reference': reference_measurements(claims),
        'history': history_info,
        'report_url': REPORT_URL,
        'files_note': ('every served file but this record itself; history/\'s files are listed in '
                       'app/history-files.json, which is listed here with its SHA-256'),
    }
    if history_info['present']:
        # v1's ~800 files are listed in their own record, bound here by its hash, so the first visit stays small;
        # CP-18d: index.html carries v1's own preview tags, and its row says so with the deployed hash and the change
        rows = listing(out, history=True)
        preview = history_info['preview_tags']
        if preview['added']:
            row = next(r for r in rows if r['path'] == HISTORY_PAGE)
            row.update(note=preview['note'], deployed_sha256=preview['deployed_sha256'],
                       deployed_bytes=preview['deployed_bytes'],
                       change={'inserted_at_byte': preview['inserted_at_byte'],
                               'inserted_bytes': preview['inserted_bytes'],
                               'inserted_sha256': preview['inserted_sha256']})
        (out / 'app/history-files.json').write_text(dump({
            'schema': HISTORY_SCHEMA, 'files': rows,
            'changed': [HISTORY_PAGE] if preview['added'] else [],
            'unchanged': ("every other file is v1's deployed file byte for byte" +
                          (' (checked against the deployed listing at the build)' if 'deployed_listing' in history_info
                           else ''))}), encoding='utf-8')
        history_info['listing'] = 'app/history-files.json'
    record['files'] = listing(out)
    # the record's own size is part of the first visit: settle it at a fixed point
    size = 0
    for _ in range(8):
        record['size'] = size_budget(out, B.START_FILES, packages, artifact, size)
        text = dump(record)
        if len(text.encode('utf-8')) == size:
            break
        size = len(text.encode('utf-8'))
    else:
        raise RuntimeError('the build record size did not settle')
    (out / 'app/space-build.json').write_text(text, encoding='utf-8')
    return record


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog='build_product_space.py')
    ap.add_argument('--bundle', required=True, type=Path)
    ap.add_argument('--out', required=True, type=Path)
    ap.add_argument('--history', type=Path, help="v1's build directory, copied as it is to <out>/history/")
    ap.add_argument('--history-note', help='a note the page and the build record show beside the History route')
    ap.add_argument('--history-gitattributes', type=Path,
                    help="v1's .gitattributes, placed at history/.gitattributes (default: a 'gitattributes' file beside "
                         'the --history folder, when there is one)')
    ap.add_argument('--history-listing', type=Path,
                    help="the deployed listing of v1's files the copy must equal (default: a 'listing.json' beside "
                         'the --history folder, when there is one)')
    ap.add_argument('--live', type=Path, help='the live data-only folder (its store/): the live record (CP-18c)')
    ap.add_argument('--allow-refused', action='store_true',
                    help='build a refused bundle anyway (negative controls only); the build record says refused')
    ap.add_argument('--pyodide', type=Path, help='the pinned Pyodide folder (default: the project\'s)')
    ap.add_argument('--zip', type=Path, help='the frozen package zip (default: the project\'s)')
    args = ap.parse_args(argv)
    gitattributes, listing = args.history_gitattributes, args.history_listing
    if args.history is not None:
        beside = args.history.resolve().parent
        if gitattributes is None and (beside / 'gitattributes').is_file():
            gitattributes = beside / 'gitattributes'
        if listing is None and (beside / 'listing.json').is_file():
            listing = beside / 'listing.json'
    try:
        record = build(args.bundle.resolve(), args.out.resolve(), history=args.history, history_note=args.history_note,
                       allow_refused=args.allow_refused, pyodide=args.pyodide, package_zip=args.zip,
                       live=args.live.resolve() if args.live else None, history_gitattributes=gitattributes,
                       history_listing=listing)
    except Refused as exc:
        print('REFUSED:', exc)
        return 1
    s = record['size']
    print('built', args.out, '| bundle', record['bundle']['manifest_sha256'][:16],
          record['bundle']['freshness']['state'], '| REFUSED (allowed)' if record['refused'] else '| publishable',
          '| first visit', s['first_visit']['bytes'], 'bytes | on request', s['on_request_bytes'], 'bytes',
          '| live record', record['live']['sha256'][:16] if record['live'] else 'none',
          '| history', record['history'].get('files', 0), 'files')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
