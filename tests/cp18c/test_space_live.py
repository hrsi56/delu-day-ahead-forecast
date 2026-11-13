"""CP-18c: the final-product Space from the live record (`scripts/build_product_space.py --live`), offline, no browser.

- the live record (`cp18.live_claims.live_record`) on the committed store: verified, every issued day's cutoff-based
  issue time and actual run (N7, O18), the days not issued with their causes, the outside days as one range, and no
  local path or market value;
- the live claims (O13, O14, O29, O30, O33): "v6 · DDNN-2 alone", "final candidate · pending 4.7T", v1 the last
  released generation, O14's sentence unchanged, the running wording from `cp18.running`; no late, timely, confidence
  or percentage-correct wording; the wall of `test_24` holds for the live mode too;
- the page sources: no hand-typed "A1 · DDNN-2 alone" or "Issued at", and every claim the page reads exists in both
  modes;
- History: v1's deployed files and its `.gitattributes`, byte for byte, bound by the deployed listing; a changed byte
  refuses the build;
- the build with `--live` (where the local inputs exist): `app/live-record.json` bound in the build record and loaded
  at start, equal to the record and to `cp18.running` on the bundle's windows; the claims in the live mode; refused
  against a store whose issued days are not the bundle's; deterministic;
- the browser acceptance's committed record (`reports/cp18c/acceptance/acceptance.json`), where it exists.

History-free (`CI=true`): the store and History's files are committed; the build tests skip with their reason where the
pinned Pyodide folder, the frozen package zip or a live bundle matching the committed store is absent.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys

import pytest

from cp17 import runtime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts'))
PROJECT = Path(runtime.project_root(ROOT))
LIVE = Path(os.environ.get('CP18C_SPACE_LIVE') or ROOT / 'live')
BUNDLE = Path(os.environ.get('CP18C_SPACE_BUNDLE') or PROJECT / '.local/tmp/cp-18c/bundle1/bundle')
HISTORY = ROOT / 'reports/cp18c/history-v1'
SOURCE = ROOT / 'space-product'
ACCEPTANCE = ROOT / 'reports/cp18c/acceptance/acceptance.json'
LOCAL = (PROJECT / runtime.PYODIDE_DIR / 'pyodide.asm.wasm', PROJECT / '.local/artifacts/cp-17c/bundle/src.zip',
         BUNDLE / 'manifest.json')
BANNED = re.compile(r'\blate\b|\btimely\b|% correct|confiden', re.I)

needs_store = pytest.mark.skipif(not (LIVE / 'store/ledger.jsonl').is_file(),
                                 reason=f'no live store in this checkout ({LIVE}/store is absent)')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@pytest.fixture(scope='module')
def record():
    from cp18.live_claims import live_record
    return live_record(LIVE)


@pytest.fixture(scope='module')
def live_claims(record):
    from cp18.live_claims import build_live_claims, live_summary
    return build_live_claims(ROOT, live=live_summary(record))


# ------------------------------------------------------------------ the live record (N7)
@needs_store
def test_the_live_record_names_each_issuances_cutoff_based_time_and_actual_run(record):
    from cp18.store import LiveStore
    store = LiveStore(LIVE / 'store')
    assert record['issued'], 'the live store holds no issued day'
    for item in record['issued'] + record['failed']:
        artifact = json.loads((store.folder / f"issued/{item['day']}/artifact.json").read_text())
        assert item['cutoff_utc'] == artifact['issue_utc'], item['day']          # the nominal time is the cutoff
        assert item['run_started_utc'] <= item['issuance_started_utc'] <= item['issuance_finished_utc'], item['day']
        assert item['host_kind'] in ('local', 'runner') and item['run_id']
        assert item['artifact_sha256'] == artifact['artifact_sha256']
    days = store.days()
    assert sorted(d['day'] for d in record['issued']) == sorted(d for d, v in days.items() if v['status'] == 'issued')
    for item in record['not_issued']:
        assert days[item['day']] == {**days[item['day']], 'status': 'not issued', 'cause': item['cause']}
    outside = sorted(d for d, v in days.items() if v['status'] == 'outside')
    if outside:
        assert [(o['first_day'], o['last_day'], o['days']) for o in record['outside']] == [(outside[0], outside[-1], len(outside))]


@needs_store
def test_the_live_record_holds_no_local_path_and_no_market_value(record):
    text = json.dumps(record)
    assert '/Users/' not in text and '.local/' not in text
    assert '"price"' not in text and 'quantiles' not in text


@needs_store
def test_the_live_record_refuses_an_altered_store(tmp_path):
    from cp18.live_claims import live_record
    shutil.copytree(LIVE / 'store', tmp_path / 'store')
    day = sorted((tmp_path / 'store/issued').iterdir())[-1]
    target = day / 'record.json'
    value = json.loads(target.read_text())
    value['run_started_utc'] = '2000-01-01T00:00:00+00:00'
    target.write_text(json.dumps(value))
    with pytest.raises(Exception):
        live_record(tmp_path)


# ------------------------------------------------------------------ the live claims (O13, O14, O29, O30, O33)
@needs_store
def test_the_live_wording_is_o30_o13_and_o29s(live_claims):
    v = live_claims['values']
    assert v['live_product_name'] == 'v6 · DDNN-2 alone'
    assert v['live_product_record_name'] == 'v6 (A1 in the frozen records)'
    assert v['live_product_status'] == 'final candidate · pending 4.7T'
    released = v['live_released_product']
    assert 'v6 is the product now, before 4.7T' in released and 'v1 is the last released generation' in released
    assert 'on a failed or inconclusive 4.7T, v1 is the product again' in released
    assert 'last released generation' in v['live_history_wording'] and 'not the product this Space presents' in v['live_history_wording']
    assert v['live_prospective_label'] == 'prospective evaluation in progress'
    assert 'not yet scored' in v['live_hero_rule'] and "nothing in the live record is 4.7T's issuance or score" in v['live_hero_rule']
    assert all('A1 · DDNN-2 alone' not in t for t in v.values())


@needs_store
def test_o14_and_the_running_wording_are_read_from_their_sources(live_claims):
    from cp18 import running
    from cp18.live_claims import build_live_claims
    v = live_claims['values']
    assert v['live_retrain_wording'] == build_live_claims(ROOT)['values']['live_retrain_wording']
    assert v['live_retrain_wording'].endswith("by up to 0.082 EUR/MWh (A1's p2.5 on 2026-03-30), the largest difference "
                                              'observed, not a bound.')
    assert v['live_running_wording'] == running.WORDING == '95% interval of the mean daily error over {n} scored days'
    assert v['live_running_before_minimum'] == running.BEFORE_MINIMUM == 'interval from 14 scored days'


@needs_store
def test_n7s_labels_and_both_modes_carry_the_same_keys(live_claims):
    from cp18.live_claims import build_live_claims
    v = live_claims['values']
    assert v['live_issue_time_label'] == 'cutoff-based issue time'
    assert 'information cutoff' in v['live_issue_time_note'] and 'not when the run happened' in v['live_issue_time_note']
    assert 'local fallback' in v['live_host_local'] and 'runner' in v['live_host_runner']
    assert set(v) == set(build_live_claims(ROOT, rehearsal_days=('2026-08-31', '2026-09-05'))['values'])


@needs_store
def test_no_live_text_says_late_timely_confidence_or_publication_before_the_auction(live_claims):
    for key, value in live_claims['values'].items():
        low = value.lower()
        assert not BANNED.search(low), key
        assert 'before the auction' not in low or 'no forecast is claimed' in low, key
    for label, key in live_claims['limitations']:
        assert not BANNED.search(label)


@needs_store
def test_the_live_limitations_name_the_live_record_and_its_outside_range(live_claims, record):
    from cp18.live_claims import LIMITATION_ORDER, text
    keys = [k for _, k in live_claims['limitations']]
    assert keys[:len(LIMITATION_ORDER)] == [f'live_limitation_{t}' for t in LIMITATION_ORDER]
    rehearsal = text(live_claims, 'live_limitation_rehearsal')
    assert record['store']['first_live_day'] in rehearsal and "Nothing here is 4.7T's issuance or score" in rehearsal
    for o in record['outside']:
        assert f"{o['first_day']} to {o['last_day']}" in rehearsal
    assert 'no forecast is claimed' in text(live_claims, 'live_limitation_operation')


@needs_store
def test_no_record_surface_renders_a_live_mode_claim(live_claims):
    from delu_forecast.surfaces import load_surfaces
    surfaces = [s for s in load_surfaces() if s.name in ('README', 'Space card', 'Static Space card', 'Pages export')]
    rendered = sorted((s.name, k) for s in surfaces for k, v in live_claims['values'].items() if s.carries(k, v))
    assert not rendered


# ------------------------------------------------------------------ the page sources
def test_the_page_sources_type_neither_the_old_name_nor_a_bare_issued_at():
    for path in SOURCE.rglob('*'):
        if path.is_file():
            body = path.read_text()
            assert 'A1 · DDNN-2 alone' not in body, path
            assert 'Issued at' not in body, path
            assert not re.search(r'\b\d{4}-\d{2}-\d{2}\b', body), path


@needs_store
def test_every_claim_the_page_reads_exists_in_the_live_mode(live_claims):
    main = (SOURCE / 'app/main.js').read_text()
    used = set(re.findall(r"\bL\('([a-z0-9_]+)'\)", main))
    assert used and used <= set(live_claims['values']), used - set(live_claims['values'])


# ------------------------------------------------------------------ History (O17)
def test_history_is_v1s_deployed_files_and_gitattributes_byte_for_byte(tmp_path):
    import build_product_space as B
    out = tmp_path / 'dist'
    info = B.copy_history(HISTORY / 'files', out, HISTORY / 'gitattributes', HISTORY / 'listing.json')
    assert (out / 'history/.gitattributes').read_bytes() == (HISTORY / 'gitattributes').read_bytes()
    listing = json.loads((HISTORY / 'listing.json').read_text())
    copied = {p.relative_to(out / 'history').as_posix(): p for p in (out / 'history').rglob('*') if p.is_file()}
    assert set(copied) == {f['path'] for f in listing['files']}
    for f in listing['files']:
        assert sha(copied[f['path']].read_bytes()) == f['sha256'] and copied[f['path']].stat().st_size == f['bytes']
    assert info['deployed_listing']['matches'] and info['deployed_listing']['files'] == len(listing['files'])
    assert info['gitattributes']['sha256'] == sha((HISTORY / 'gitattributes').read_bytes())


def test_history_refuses_a_file_that_is_not_the_deployed_one(tmp_path):
    import build_product_space as B
    files = tmp_path / 'files'
    shutil.copytree(HISTORY / 'files', files)
    target = files / 'index.html'
    target.write_bytes(target.read_bytes() + b'\n')
    with pytest.raises(B.Refused):
        B.copy_history(files, tmp_path / 'dist', HISTORY / 'gitattributes', HISTORY / 'listing.json')


# ------------------------------------------------------------------ the build with --live (local inputs)
def _matching() -> str | None:
    if not all(p.exists() for p in LOCAL):
        return 'the local Space inputs are absent (the pinned Pyodide folder, the frozen package zip or a live bundle under .local/)'
    if not (LIVE / 'store/ledger.jsonl').is_file():
        return f'no live store at {LIVE}'
    from cp18.live_claims import live_record
    ours = sorted((d['day'], d['artifact_sha256']) for d in live_record(LIVE)['issued'])
    theirs = sorted((d['delivery_day'], d['issuing_artifact_sha256'])
                    for d in json.loads((BUNDLE / 'issued-forecasts.json').read_text())['days'])
    if ours != theirs:
        return (f'the live bundle {BUNDLE} is not the record of the store at {LIVE} (set CP18C_SPACE_BUNDLE and '
                'CP18C_SPACE_LIVE to a matching pair)')
    return None


def _skip_reason():
    try:
        return _matching()
    except Exception as exc:                        # noqa: BLE001 - an unreadable local input is a skip, with its reason
        return f'the local inputs could not be read: {type(exc).__name__}'


SKIP = _skip_reason()
needs_build = pytest.mark.skipif(SKIP is not None, reason=SKIP or '')


@pytest.fixture(scope='module')
def built(tmp_path_factory):
    import build_product_space as B
    out = tmp_path_factory.mktemp('space-live') / 'dist'
    record = B.build(BUNDLE, out, live=LIVE, history=HISTORY / 'files', history_gitattributes=HISTORY / 'gitattributes',
                     history_listing=HISTORY / 'listing.json')
    return out, record


@needs_build
def test_the_live_record_is_served_bound_and_loaded_at_start(built):
    out, record = built
    data = (out / 'app/live-record.json').read_bytes()
    listed = {f['path']: f for f in record['files']}
    assert listed['app/live-record.json']['sha256'] == sha(data) == record['live']['sha256']
    assert 'app/live-record.json' in record['size']['first_visit']['files']
    value = json.loads(data)
    assert value['bundle_manifest_sha256'] == record['bundle']['manifest_sha256']
    from cp18.live_claims import live_record
    assert value['record'] == json.loads(json.dumps(live_record(LIVE)))


@needs_build
def test_n7_the_live_records_cutoff_is_each_issued_forecasts_issue_time(built):
    out, _ = built
    value = json.loads((out / 'app/live-record.json').read_text())
    forecasts = {d['delivery_day']: d for d in json.loads((out / 'payloads/issued-forecasts.json').read_text())['days']}
    assert {d['day'] for d in value['record']['issued']} == set(forecasts)
    for item in value['record']['issued']:
        assert item['cutoff_utc'] == forecasts[item['day']]['issue_utc']
        assert item['issuance_started_utc'] and item['issuance_finished_utc'] and item['run_started_utc']


@needs_build
def test_the_running_intervals_are_cp18_runnings_on_the_served_windows(built):
    from cp18 import running
    out, _ = built
    value = json.loads((out / 'app/live-record.json').read_text())
    windows = json.loads((out / 'payloads/evaluation.json').read_text())['windows']
    assert value['running'] == json.loads(json.dumps(running.running(windows)))
    for series in value['running']['series'].values():
        for point in series:
            assert (point['lower'] is None) == (point['n'] < running.MINIMUM_DAYS)


@needs_build
def test_the_claims_are_the_live_modes_and_the_card_names_v6(built):
    from cp18.live_claims import build_live_claims, live_record, live_summary
    out, record = built
    claims = json.loads((out / 'app/claims.json').read_text())
    assert claims['mode'] == 'live' and record['claims_mode'] == 'live' and claims['rehearsal_days'] == []
    assert claims['values'] == build_live_claims(ROOT, live=live_summary(live_record(LIVE)))['values']
    card = (out / 'README.md').read_text()
    assert 'v6 · DDNN-2 alone' in card and 'A1 · DDNN-2 alone' not in card


@needs_build
def test_history_is_in_the_build_and_its_listing(built):
    out, record = built
    listing = json.loads((HISTORY / 'listing.json').read_text())
    served = {f['path']: f for f in json.loads((out / 'app/history-files.json').read_text())['files']}
    assert set(served) == {'history/' + f['path'] for f in listing['files']}
    for f in listing['files']:
        assert served['history/' + f['path']]['sha256'] == f['sha256']
    assert record['history']['gitattributes']['path'] == 'history/.gitattributes'
    assert record['history']['deployed_listing']['matches'] is True


@needs_build
def test_the_build_refuses_a_store_whose_issued_days_are_not_the_bundles(tmp_path):
    import build_product_space as B
    other = tmp_path / 'live'
    other.mkdir()
    shutil.copytree(ROOT / 'reports/cp18b/dryrun/store', other / 'store')         # the dry runs' development store
    with pytest.raises(B.Refused):
        B.build(BUNDLE, tmp_path / 'dist', live=other)


@needs_build
def test_the_live_build_is_deterministic(tmp_path, built):
    import build_product_space as B
    first, _ = built
    second = tmp_path / 'dist'
    B.build(BUNDLE, second, live=LIVE, history=HISTORY / 'files', history_gitattributes=HISTORY / 'gitattributes',
            history_listing=HISTORY / 'listing.json')

    def tree(root):
        return {p.relative_to(root).as_posix(): sha(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()}
    a, b = tree(first), tree(second)
    assert a.keys() == b.keys() and [k for k in a if a[k] != b[k]] == []


# ------------------------------------------------------------------ the browser acceptance's record
@pytest.mark.skipif(not ACCEPTANCE.is_file(), reason=f'no committed browser acceptance record ({ACCEPTANCE} is absent)')
def test_the_committed_browser_acceptance_has_no_failure_and_a_retrain_to_its_status():
    value = json.loads(ACCEPTANCE.read_text())
    assert value['summary']['failed'] == 0 and value['summary']['passed'] > 0
    assert {'chromium', 'webkit'} <= set(value['engines'])
    runs = [r for r in value['train_runs'] if r['bundle'] == 'main']
    assert any(r['engine'] == 'chromium' and r['status'] == 'identical bit for bit' for r in runs)
