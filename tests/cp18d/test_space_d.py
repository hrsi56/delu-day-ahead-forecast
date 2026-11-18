"""CP-18d: the final-product Space's surfaces of the Owner's decision 31, the schedule's wording and v1's preview tags
(`space-product/`, `scripts/build_product_space.py`), offline, no browser.

- **the page sources** render each label path (static checks in the style of CP-18c's `test_space_live.py`): every
  issue-times block, the panel's served day and counts, the record tables, the Forecast picker, the Validation per-day
  table, the per-day chart's distinct markers, tooltips and legend, the cumulative section per set, the Reliability
  view, Explainability and Features; the note once per view; the schedule where the live record lists its days; and
  every wording read from the claims;
- **the claims** decision 31's surfaces need, in both modes, never "late" or "timely";
- **the build's refusals** (its own `Refused`): an issued day without its input class, a label that is not its class's,
  counts that are not the issued days', a running record or evaluation sets without both sets;
- **v1's preview tags**: inserted once into `history/index.html`'s head, never matched by `cp18.publish.HF_META_RUN`,
  so the served page's normalization still finds exactly the host's one run, wherever the host puts it; the deployed
  page is the served one without the recorded span;
- **the build** (where the local inputs exist; skipped with the reason otherwise): `app/live-record.json` carries the
  evaluation sets and the running sets with the live record's counts, `app/history-files.json` records the one changed
  file with its note, every other v1 file is byte for byte the deployed one, the card names the served day's label,
  and the build is deterministic.

The local build inputs: `CP18D_SPACE_BUNDLE` (a live bundle) and `CP18D_SPACE_LIVE` (a copy of a live folder whose
store is that bundle's record, e.g. one relabelled by `tests/cp18d/fixture_after_cutoff.py`).
"""
from __future__ import annotations

from datetime import date, timedelta
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
SOURCE = ROOT / 'space-product'
MAIN = (SOURCE / 'app/main.js').read_text()
CHARTS = (SOURCE / 'app/charts.js').read_text()
HISTORY = ROOT / 'reports/cp18c/history-v1'
SCRATCH = PROJECT / '.local/tmp/cp-18d/builder-space'
BUNDLE = Path(os.environ.get('CP18D_SPACE_BUNDLE') or SCRATCH / 'after/bundle')
LIVE = Path(os.environ.get('CP18D_SPACE_LIVE') or SCRATCH / 'after1021/live')
LOCAL = (PROJECT / runtime.PYODIDE_DIR / 'pyodide.asm.wasm', PROJECT / '.local/artifacts/cp-17c/bundle/src.zip',
         BUNDLE / 'manifest.json', LIVE / 'store/ledger.jsonl')
BANNED = re.compile(r'\blate\b|\btimely\b', re.I)
NEW_KEYS = ('live_input_class_fetched', 'live_input_class_counts', 'live_sets_same', 'live_history_preview_title',
            'live_history_preview_description')
HOST_SCRIPT = b'<script>window.huggingface={variables:{"SPACE_CREATOR_USER_ID":"0"}};</script>'
HOST_RUN = ('<meta property="og:title" content="v6 · DDNN-2 alone"><meta property="og:image" '
            'content="https://example.invalid/t.png"><meta name="twitter:card" content="summary_large_image">'
            '<meta name="twitter:image" content="https://example.invalid/t.png">').encode('utf-8')


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def between(text: str, start: str, end: str) -> str:
    i = text.index(start)
    return text[i:text.index(end, i + len(start))]


# ------------------------------------------------------------------ the page sources: each label path
def test_every_issue_times_block_shows_the_days_inputs():
    block = between(MAIN, 'function issueTimes(', '// ------------------------------------------------------------------ start-up')
    assert "'data-input-class': c ? c.cls : ''" in block and "'data-time-kind': 'inputs'" in block and 'classSpan(day)' in block
    # issueTimes is how today, tomorrow, yesterday, the Forecast view's day and Train it yourself show an issued day
    assert MAIN.count('issueTimes(') >= 4


def test_the_label_is_the_claims_wording_with_the_copys_retrieval_time():
    block = between(MAIN, 'function classText(', 'function classSpan(')
    assert "L('live_input_class_before_cutoff')" in block and "L('live_input_class_load_forecast_after_cutoff')" in block
    assert "fill(L('live_input_class_fetched'), {time: c.fetched.slice(0, 19).replace('T', ' ')})" in block
    source = between(MAIN, 'function classOf(', 'function isAfter(')
    # the live record first; without one, the served forecasts when they carry the label (development rehearsal)
    assert 'issuanceOf(day)' in source and 'forecastOf(day)' in source and 'load_forecast_fetched_utc' in source


def test_the_panel_shows_the_served_days_inputs_the_counts_the_note_and_the_schedule():
    panel = between(MAIN, 'function renderProduct(', 'function forecastRows(')
    assert "classSpan(a.delivery_day)" in panel and "'data-time': 'inputs'" in panel
    assert 'countsText(counts)' in panel and 'counts.m ? classNote() : null' in panel
    assert "L('live_schedule')" in panel and panel.index("L('live_schedule')") < panel.index("'Days not issued'")
    assert "'Days not issued'" in panel and "'Outside the live record'" in panel             # still listed, with causes


def test_the_record_tables_the_picker_and_the_forecast_view_name_each_day():
    table = between(MAIN, 'function recordTable(', 'function panelWindow(')
    assert "labelled ? td(classSpan(d) || '—') : null" in table and "labelled ? 'Inputs' : null" in table
    forecast = between(MAIN, 'RENDER.forecast', '// ------------------------------------------------------------------ Validation')
    assert "isAfter(classOf(d)) ? ` · ${L('live_input_class_load_forecast_after_cutoff')}` : ''" in forecast
    assert 'countsText(counts)' in forecast and 'if (anyAfter()) panel.appendChild(classNote());' in forecast
    assert forecast.index("h('h3', {}, 'Days not issued')") < forecast.index("L('live_schedule')") < forecast.index('data-not-issued-list')


def test_train_explainability_and_features_name_the_served_days_inputs():
    train = between(MAIN, 'RENDER.train', 'function renderRetrain(')
    assert 'issueTimes(day, a.issue_utc' in train and 'if (isAfter(classOf(day))) panel.appendChild(classNote());' in train
    for view in ('RENDER.explainability', 'RENDER.features'):
        body = between(MAIN, view, 'glueAction(box,')
        assert 'servedInputs(panel, a.delivery_day);' in body, view


def test_the_per_day_errors_mark_the_days_fetched_after_the_cutoff():
    per = between(MAIN, 'function perDay(', 'function fillPerDay(')
    assert "markers: labelled ? after.map(x => (x ? 'diamond' : null)) : null" in per
    assert 'titles: labelled ? days.map(d =>' in per and 'classText(classOf(d.day))' in per
    assert 'legendExtra: after.some(Boolean)' in per and 'caption: counts ? `${cap(countsText(counts))}.`' in per
    assert "labelled ? td(classSpan(d.day) || '—') : null" in per and "labelled ? 'Inputs' : null" in per
    assert 'if (labelled && after.some(Boolean)) holder.appendChild(classNote());' in per
    # the chart helper draws a point's own marker always (never thinned away), with its tooltip, and the legend entry
    lines = between(CHARTS, 'function lines(', '// ---------------------------------------------------------------- running means')
    assert "(i % step !== 0 && !own)" in lines and "el('title', {}, mk)" in lines and 'opts.legendExtra' in lines


def test_the_prospective_record_and_the_cumulative_section_report_both_sets_with_their_counts():
    validation = between(MAIN, 'RENDER.validation', '// ------------------------------------------------------------------ Reliability')
    assert "g.window === 'prospective' ? evaluationSets() : null" in validation
    assert 'setHead(sets.all)' in validation and 'setHead(sets.before)' in validation and 'setsQual(sets)' in validation
    # the before-cutoff rows carry no data-index: the recomputation and CP-18c's checks count evaluation.json's rows only
    before = between(validation, 'setHead(sets.before)', 'sec.appendChild(table(')
    assert 'data-index' not in before
    sets = between(MAIN, 'function evaluationSets(', 'function runningSection(')
    assert 'S.live.evaluation_sets' in sets and "L('live_sets_same')" in sets and "L('live_sets_wording')" in sets
    assert '(n = ${set.issued_days} issued days)' in sets
    running = between(MAIN, 'function runningSection(', 'RENDER.validation')
    assert "const same = !!(before && all && before.issued_days === all.issued_days);" in running
    assert 'if (before && all && !same) runningSet(outer, r, before, false);' in running
    assert "fill(L('live_sets_same'), {n: all.issued_days})" in running
    # the all-days set keeps CP-18c's marks (data-running, the series ids, the method) for its acceptance
    assert "'data-running': isAll ? '1' : null" in running and 'if (isAll) box.appendChild' in running


def test_the_reliability_view_reports_the_before_cutoff_set_beside_the_record():
    rel = between(MAIN, 'RENDER.reliability', '// ------------------------------------------------------------------ Explainability')
    assert 'sets && !sets.same' in rel and 'sets.before.evidence_class' in rel and "fill(L('live_sets_same')" in rel


def test_the_page_checks_every_issued_day_carries_its_label_at_start():
    start = between(MAIN, 'async function start()', 'function startFailed(')
    assert "issued days without their input class (the Owner's decision 31)" in start
    assert 'd.input_class_text !== texts[d.input_class]' in start


def test_the_page_sources_never_say_late_or_timely_and_type_no_label_by_hand():
    from cp18 import inputclass
    for path in SOURCE.rglob('*'):
        if path.is_file():
            body = path.read_text()
            assert not BANNED.search(body), path
            for text in inputclass.TEXT.values():
                assert f"'{text}'" not in body and f'"{text}"' not in body, (path, text)


# ------------------------------------------------------------------ the claims
def test_the_new_claims_exist_in_both_modes_and_never_say_late_or_timely():
    from cp18.live_claims import build_live_claims, live_record, live_summary
    dev = build_live_claims(ROOT)['values']
    live = build_live_claims(ROOT, live=live_summary(live_record(ROOT / 'live')))['values']
    for key in NEW_KEYS:
        assert dev[key] == live[key] and not BANNED.search(live[key]), key
    used = set(re.findall(r"\bL\('([a-z0-9_]+)'\)", MAIN))
    assert {'live_input_class_note', 'live_input_class_fetched', 'live_input_class_counts', 'live_sets_same',
            'live_sets_wording', 'live_schedule', 'live_input_class_before_cutoff',
            'live_input_class_load_forecast_after_cutoff'} <= used <= set(live)
    assert live['live_input_class_counts'].format(n=5, k=4, m=1) == ('5 issued days: 4 with every input before the cutoff, '
                                                                    '1 with the load forecast fetched after the cutoff')


# ------------------------------------------------------------------ the build's refusals (decision 31)
DAYS = [date(2026, 11, 3) + timedelta(days=i) for i in range(6)]
AFTER = {date(2026, 11, 5)}


def synthetic() -> dict[str, bytes]:
    """A served bundle's evaluation inputs on live days (the Lead's `test_evaluation_sets` shape), with a manifest."""
    from cp17.issue import canonical_hours
    from cp18 import evaluation as EV, outcomes as OC
    forecasts = {'schema': 'cp17b-issued-forecasts-v2', 'levels': [0.025, 0.1, 0.25, 0.5, 0.75, 0.9, 0.975], 'days': []}
    view = {}
    for i, d in enumerate(DAYS):
        keys = canonical_hours(d)
        q = [[10.0 * k + j * 3 + i for j in range(7)] for k in range(len(keys))]
        forecasts['days'].append({'delivery_day': str(d), 'issue_utc': '', 'issuing_artifact_sha256': f'{i:064d}',
                                  'issued_policy': 'A1', 'display': '', 'keys': keys, 'quantiles': q, 'partial': None})
        view[str(d)] = {'status': 'final', 'keys': keys, 'prices': [10.0 * k + 8 for k in range(len(keys))],
                        'revised_utc': [''] * len(keys), 'first': {'published_utc': ''}}
    out = OC.bundle_outcomes(DAYS, view)
    ev = EV.evaluation_bundle([], EV.daily_windows(forecasts, out, []))
    return {'issued-forecasts.json': json.dumps(forecasts).encode(), 'outcomes.json': json.dumps(out).encode(),
            'evaluation.json': json.dumps(ev).encode(), 'manifest.json': b'{}'}


def record() -> dict:
    from cp18 import inputclass
    issued = []
    for i, d in enumerate(DAYS):
        label = (inputclass.label(inputclass.AFTER, f'{d - timedelta(days=1)}T10:21:07Z') if d in AFTER
                 else inputclass.label(inputclass.BEFORE))
        if label['load_forecast_fetched_utc']:
            label['load_forecast_fetched_utc'] = label['load_forecast_fetched_utc'][:-1] + '+00:00'
        issued.append({'day': str(d), 'artifact_sha256': f'{i:064d}', **label})
    return {'issued': issued, 'failed': [], 'input_classes': [
        {'input_class': c, 'input_class_text': inputclass.TEXT[c], 'issued': sum(1 for x in issued if x['input_class'] == c)}
        for c in inputclass.ORDER]}


@pytest.fixture()
def fake_store(monkeypatch):
    """`live_data` over the synthetic bundle, with the live store's record replaced by `record()` (or a changed one)."""
    import cp18.live_claims as LC
    value = {'record': record()}
    monkeypatch.setattr(LC, 'live_record', lambda folder: json.loads(json.dumps(value['record'])))
    return value


def test_the_live_data_carries_both_sets_with_the_records_counts(fake_store, tmp_path):
    import build_product_space as B
    out = B.live_data(tmp_path, synthetic(), refused=False)
    assert out['schema'] == 'cp18d-space-live-v1'
    assert [(s['set'], s['issued_days']) for s in out['running']['sets']] == [('before_cutoff', 5), ('all', 6)]
    assert [(s['set'], s['issued_days']) for s in out['evaluation_sets']['sets']] == [('before_cutoff', 5), ('all', 6)]
    assert '2026-11-05' not in out['evaluation_sets']['sets'][0]['days']
    assert 'outside the bundle' in out['evaluation_sets_source'] or 'not part of the bundle' in out['evaluation_sets_source']


@pytest.mark.parametrize('change', ['no class', 'unknown class', 'text', 'after without its time', 'before with a time',
                                    'counts', 'failed without its class'])
def test_negative_control_the_build_refuses_an_issued_day_without_decision_31s_label(fake_store, tmp_path, change):
    import build_product_space as B
    rec = fake_store['record']
    after = next(i for i in rec['issued'] if i['input_class'] == 'load_forecast_after_cutoff')
    before = rec['issued'][0]
    if change == 'no class':
        del before['input_class']
    elif change == 'unknown class':
        before['input_class'] = 'fetched_late'
    elif change == 'text':
        before['input_class_text'] = 'timely'
    elif change == 'after without its time':
        after['load_forecast_fetched_utc'] = None
    elif change == 'before with a time':
        before['load_forecast_fetched_utc'] = '2026-11-02T10:21:07+00:00'
    elif change == 'counts':
        rec['input_classes'][0]['issued'] += 1
    else:
        rec['failed'] = [{'day': '2026-11-09', 'artifact_sha256': '9' * 64}]
    with pytest.raises(B.Refused):
        B.live_data(tmp_path, synthetic(), refused=False)
    with pytest.raises(B.Refused):                  # a refused bundle built for a control is no exemption
        B.live_data(tmp_path, synthetic(), refused=True)


@pytest.mark.parametrize('which', ['running', 'evaluation sets'])
@pytest.mark.parametrize('how', ['one set', 'no set', 'counts'])
def test_negative_control_the_build_refuses_a_record_without_both_sets(fake_store, monkeypatch, tmp_path, which, how):
    import build_product_space as B
    from cp18 import evaluation, running
    target, name = (running, 'running') if which == 'running' else (evaluation, 'class_sets')
    real = getattr(target, name)

    def broken(*args, **kwargs):
        value = real(*args, **kwargs)
        sets = value['sets']
        if how == 'one set':
            value['sets'] = [s for s in sets if s['set'] == 'all']
        elif how == 'no set':
            value['sets'] = []
        else:
            sets[0]['issued_days'] += 1
        return value
    monkeypatch.setattr(target, name, broken)
    with pytest.raises(B.Refused):
        B.live_data(tmp_path, synthetic(), refused=False)


def test_negative_control_an_issued_day_of_the_bundle_without_a_class_refuses(fake_store, monkeypatch, tmp_path):
    """The running intervals and the evaluation sets raise on a prospective day without a class: the build's Refused."""
    import build_product_space as B
    import cp18.live_claims as LC
    rec = record()
    monkeypatch.setattr(B, 'labels', lambda r: {i['day']: i['input_class'] for i in rec['issued'][1:]})
    monkeypatch.setattr(LC, 'live_record', lambda folder: rec)
    with pytest.raises(B.Refused, match='input class'):
        B.live_data(tmp_path, synthetic(), refused=True)


# ------------------------------------------------------------------ v1's preview tags
@pytest.fixture()
def history(tmp_path):
    import build_product_space as B
    from cp18.live_claims import build_live_claims
    out = tmp_path / 'dist'
    B.copy_history(HISTORY / 'files', out, HISTORY / 'gitattributes', HISTORY / 'listing.json')
    values = build_live_claims(ROOT)['values']
    info = B.history_preview(out, values, required=True)
    return out, values, info


def test_v1s_page_carries_its_own_preview_tags_once_in_its_head(history):
    out, values, info = history
    page = (out / 'history/index.html').read_bytes()
    deployed = (HISTORY / 'files/index.html').read_bytes()
    head = page[page.index(b'<head>'):page.index(b'</head>')]
    title, desc = values['live_history_preview_title'], values['live_history_preview_description']
    assert 'v1' in title and 'historical' in title and 'v6' not in title and 'v6' not in desc
    for attr, key, value in (('property', 'og:title', title), ('property', 'og:description', desc),
                             ('name', 'twitter:title', title), ('name', 'twitter:description', desc)):
        tag = f'<meta content="{value}" {attr}="{key}" />'.encode('utf-8')
        assert head.count(tag) == 1, key
    assert page.count(b'og:title') == 1 and page.count(b'twitter:title') == 1
    # the one change is the recorded span: without it the page is v1's deployed page, byte for byte
    at, n = info['inserted_at_byte'], info['inserted_bytes']
    assert page[:at] + page[at + n:] == deployed and sha(deployed) == info['deployed_sha256']
    assert sha(page[at:at + n]) == info['inserted_sha256'] and sha(page) == info['sha256']
    assert page[:at].endswith(b'<meta charset="utf-8" />\n')            # the charset declaration stays first


@pytest.mark.parametrize('where', ['after the host script', 'before </head>'])
def test_the_served_pages_normalization_still_finds_exactly_the_hosts_run(history, where):
    from cp18 import publish as P
    out, _, info = history
    page = (out / 'history/index.html').read_bytes()
    i, e = page.index(b'<head>') + len(b'<head>'), page.index(b'</head>')
    served = (page[:i] + HOST_SCRIPT + HOST_RUN + page[i:] if where == 'after the host script'
              else page[:i] + HOST_SCRIPT + page[i:e] + HOST_RUN + page[e:])
    assert P.matches('history/index.html', served, info['sha256'], info['bytes']) == (True, 'normalized')
    body, removed = P.normalized('history/index.html', served)
    assert body == page and removed == HOST_SCRIPT + HOST_RUN
    assert len(list(P.HF_META_RUN.finditer(served))) == 1                # v1's own tags are never part of a run
    # a second run the host might add elsewhere is still ambiguous, compared as served (CP-18c's rule, unchanged)
    twice = served.replace(b'</head>', HOST_RUN + b'</head>') if where == 'after the host script' else \
        served[:i] + HOST_RUN + served[i:]
    assert P.matches('history/index.html', twice, info['sha256'])[0] is False


def test_the_preview_tags_escape_their_text_and_never_match_the_hosts_run():
    import build_product_space as B
    from cp18 import publish as P
    tags = B.preview_tags('a "quoted" <b> & title', 'd')
    assert b'&quot;quoted&quot; &lt;b&gt; &amp; title' in tags and not P.HF_META_RUN.search(tags)
    assert tags.count(b'<meta content=') == 4 and tags.count(b' />') == 4


def test_a_deployed_v1_without_a_head_refuses_and_a_stand_in_is_left_as_it_is(tmp_path):
    import build_product_space as B
    from cp18.live_claims import build_live_claims
    values = build_live_claims(ROOT)['values']
    (tmp_path / 'history').mkdir()
    (tmp_path / 'history/index.html').write_text('<!doctype html><title>v1</title>\n')
    with pytest.raises(B.Refused):
        B.history_preview(tmp_path, values, required=True)
    info = B.history_preview(tmp_path, values, required=False)
    assert info['added'] is False and (tmp_path / 'history/index.html').read_text() == '<!doctype html><title>v1</title>\n'


# ------------------------------------------------------------------ the build (local inputs)
def _skip() -> str | None:
    if not all(p.exists() for p in LOCAL):
        return ('the local Space inputs are absent (the pinned Pyodide folder, the frozen package zip, a live bundle at '
                f'{BUNDLE} and a live copy at {LIVE}; set CP18D_SPACE_BUNDLE and CP18D_SPACE_LIVE)')
    try:
        from cp18.live_claims import live_record
        ours = sorted((d['day'], d['artifact_sha256']) for d in live_record(LIVE)['issued'])
        theirs = sorted((d['delivery_day'], d['issuing_artifact_sha256'])
                        for d in json.loads((BUNDLE / 'issued-forecasts.json').read_text())['days'])
    except Exception as exc:                        # noqa: BLE001 - an unreadable local input is a skip, with its reason
        return f'the local inputs could not be read: {type(exc).__name__}'
    return None if ours == theirs else f'the bundle {BUNDLE} is not the record of the store at {LIVE}'


SKIP = _skip()
needs_build = pytest.mark.skipif(SKIP is not None, reason=SKIP or '')


@pytest.fixture(scope='module')
def built(tmp_path_factory):
    import build_product_space as B
    out = tmp_path_factory.mktemp('space-d') / 'dist'
    return out, B.build(BUNDLE, out, live=LIVE, history=HISTORY / 'files', history_gitattributes=HISTORY / 'gitattributes',
                        history_listing=HISTORY / 'listing.json')


@needs_build
def test_the_live_build_serves_decision_31s_sets_with_the_records_counts(built):
    out, rec = built
    value = json.loads((out / 'app/live-record.json').read_text())
    issued = value['record']['issued']
    k = sum(1 for i in issued if i['input_class'] == 'before_cutoff')
    want = [('before_cutoff', k), ('all', len(issued))]
    assert [(s['set'], s['issued_days']) for s in value['running']['sets']] == want
    assert [(s['set'], s['issued_days']) for s in value['evaluation_sets']['sets']] == want
    assert rec['live']['running_sets'][0]['issued_days'] == k and rec['live']['input_classes'] == value['record']['input_classes']
    assert rec['schema'] == 'cp18d-space-build-v1' and value['schema'] == 'cp18d-space-live-v1'
    # the bundle's files keep the frozen schema: no label and no subset in them
    forecasts = json.loads((out / 'payloads/issued-forecasts.json').read_text())
    windows = json.loads((out / 'payloads/evaluation.json').read_text())['windows']
    assert not any('input_class' in d for d in forecasts['days']) and not any('subset' in w for w in windows)


@needs_build
def test_the_build_records_v1s_one_changed_file_with_its_note(built):
    out, rec = built
    listing = {f['path']: f for f in json.loads((HISTORY / 'listing.json').read_text())['files']}
    value = json.loads((out / 'app/history-files.json').read_text())
    assert value['schema'] == 'cp18d-space-history-files-v1' and value['changed'] == ['history/index.html']
    rows = {f['path']: f for f in value['files']}
    assert set(rows) == {'history/' + p for p in listing}
    for path, f in listing.items():
        row = rows['history/' + path]
        assert row['sha256'] == sha((out / 'history' / path).read_bytes())
        if path == 'index.html':
            assert row['deployed_sha256'] == f['sha256'] and row['deployed_bytes'] == f['bytes'] != row['bytes']
            assert "v1's deployed page with its own preview tags added (CP-18d)" in row['note']
            assert row['change']['inserted_bytes'] == row['bytes'] - row['deployed_bytes']
        else:
            assert row['sha256'] == f['sha256'] and 'note' not in row, path
    preview = rec['history']['preview_tags']
    assert preview['added'] and preview['sha256'] == rows['history/index.html']['sha256'] == rec['history']['index_sha256']
    assert rec['history']['deployed_listing']['matches'] is True


@needs_build
def test_the_card_names_the_served_days_inputs(built):
    from cp18 import inputclass
    out, rec = built
    value = json.loads((out / 'app/live-record.json').read_text())
    day = rec['bundle']['artifact']['delivery_day']
    item = next(i for i in value['record']['issued'] if i['day'] == day)
    card = (out / 'README.md').read_text()
    assert f'({day}; {inputclass.TEXT[item["input_class"]]}' in card and not BANNED.search(card)


def rechain(folder: Path, day: str, value: dict) -> None:
    """Write `day`'s record in a store copy and re-chain its ledger, as the Lead's fixture does, so that the copy's
    chain verifies and only the record's content is in question."""
    from cp17c.store import _canonical, _sha_bytes, _write
    entries = [json.loads(line) for line in (folder / 'ledger.jsonl').read_text().splitlines()]
    index = next(i for i, e in enumerate(entries) if e.get('kind') == 'issuance' and e['day'] == day)
    entries[index]['record_file_sha256'] = _write(folder / entries[index]['record_file'], value)
    for i in range(index, len(entries)):
        entry = {k: v for k, v in entries[i].items() if k != 'entry_sha256'}
        entry['previous_entry_sha256'] = entries[i - 1]['entry_sha256'] if i else None
        entry['entry_sha256'] = _sha_bytes(_canonical(entry))
        entries[i] = entry
    (folder / 'ledger.jsonl').write_text(''.join(json.dumps(e, sort_keys=True, allow_nan=False) + '\n' for e in entries))
    head = json.loads((folder / 'head.json').read_text())
    head['entry_sha256'] = entries[-1]['entry_sha256']
    _write(folder / 'head.json', head)


@needs_build
def test_the_build_refuses_a_store_copy_whose_day_lost_its_label(tmp_path):
    import build_product_space as B
    from cp18.store import LiveStore
    live = tmp_path / 'live'
    shutil.copytree(LIVE / 'store', live / 'store')
    store = LiveStore(live / 'store')
    day = sorted(d for d, v in store.days().items() if v['status'] == 'issued')[-1]
    value = json.loads((live / f'store/issued/{day}/record.json').read_text())
    for key in ('input_class', 'input_class_text', 'load_forecast_fetched_utc'):
        value.pop(key, None)
    value['schema'] = 'cp18d-day-record-v1'
    rechain(live / 'store', day, value)
    from cp17c.store import StoreRefused
    with pytest.raises(StoreRefused, match='label is missing'):   # the chain re-verifies; the store refuses the record
        LiveStore(live / 'store').verify()
    with pytest.raises(B.Refused, match='label is missing'):
        B.build(BUNDLE, tmp_path / 'dist', live=live)


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
