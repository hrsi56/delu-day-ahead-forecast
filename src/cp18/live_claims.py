"""The live claim builder: what the final-product Space says, from the claim layer and the committed records.

`tests/test_24_live_namespace_is_walled_off.py` keeps the wall: every claim built here has a `live_` key, the record
claim set (`delu_forecast.claims.build_claims`) holds none of them, and no surface that speaks for the model of
record renders one. The Space renders its Limitations view, its product status, its badges and its fixed wording from
this builder only, so there is no hand-written limitation copy and no hand-typed number.

Two kinds of entry:

- **`values`** (`live_*`): the live product's own claims. Bare figures the Space serves in its records (τ, the rolling
  window's length, τ_eq) are read there, not repeated here. Every figure is read from a committed record (the CP-17c
  freeze manifest, CP-17's frozen protocol and report, `cp17.scoring` and `cp17.attribution`'s frozen labels); the
  sentences around them are fixed here.
- **`shared`**: record-layer claims that apply unchanged to the live product, rendered verbatim by their record key
  (`build_claims()`): the data attribution, the GFS attribution and the quarter-hour averaging; the Data view takes the price floor's definition from the record sentence's first clause.

**O13** (the Orchestrator's ruling under decision 27, adopting CP-17's protocol §12): A1 is "final candidate · pending
4.7T" until 4.7T is scored; it becomes "live" only at CP-18's activation, which requires a passed 4.7T; on a fail, v1
stays the released product. **O14:** CP-17's proposed visitor wording for "Train it yourself", plus one sentence that
states F1 at its largest observed figure, as §24.12 (R3) records it.

**The live mode (CP-18c; r20 §24.14, decision 28).** `build_live_claims(..., live=<live_summary(record)>)` gives the
live product's claims; without `live` the claims are CP-18b's development rehearsal's, unchanged. The live mode
applies the Orchestrator's rulings: **O30**, the product is "v6 · DDNN-2 alone" (the frozen records keep "A1", so the
served identity reads "v6 (A1 in the frozen records)"); **O13**, its status "final candidate · pending 4.7T"; **O29**,
it is the product now, before 4.7T, v1 is the last released generation, its demo at `/history/` labelled
"Historical", and v1 is the product again on a failed or inconclusive 4.7T; **O18's N7**, the artifact's nominal
D−1 11:00 is labelled the cutoff-based issue time, beside each issuance's actual run time and host from the day's
record; **O33**, the running intervals' wording, read from `cp18.running`. Every key exists in both modes (the page
reads them all), and no text says late or timely (decision 22) or claims publication before the auction.

**The live record** (`live_record(folder)`): what the Space shows of the live store (`cp18.store.LiveStore`, verified
first): every issued day with its cutoff-based issue time and its actual run's start, issuance start and end, run and
host; every failed issuance; every day not issued with its cause; the days outside the live record as one range; the
runs. It holds no market value and no local path.
"""
from __future__ import annotations

import json
from pathlib import Path
import re

MANIFEST = 'docs/track-b/evidence/cp-17c/freeze-manifest.json'
PROTOCOL = 'docs/track-b/evidence/cp-17/4-7t-frozen-protocol.md'
CP17_REPORT = 'reports/cp17/report.md'
SHARED = ('attribution', 'limitation_mtu_averaging')
#: The claim layer's constants that are not record claims of their own (`delu_forecast.claims`), shared verbatim.
SHARED_CONSTANTS = {'gfs_attribution': 'GFS_ATTRIBUTION'}
STATES = ('pending', 'passed', 'failed')
LIMITATION_ORDER = ('evidence', 'rehearsal', 'f1', 'retrain_selections', 'inputs', 'rendered', 'operation')
RECORD_SCHEMA = 'cp18c-space-live-record-v1'
HOSTS = ('local', 'runner')


def _read(root, rel) -> str:
    return (Path(root) / rel).read_text(encoding='utf-8')


def _quoted(text: str, after: str) -> str:
    """The first double-quoted passage after the marker `after`, with its line breaks joined."""
    i = text.index(after)
    m = re.search(r'"(.+?)"', text[i:], re.S)
    return ' '.join(m.group(1).split())


def _f1(root) -> tuple[str, str, str]:
    """F1's largest observed figure, its quantile level and its day, from the freeze manifest's disclosure."""
    identity = json.loads(_read(root, MANIFEST))['policy_identity']
    m = re.search(r'by up to ([0-9.]+) EUR/MWh \((p[0-9.]+), (\d{4}-\d{2}-\d{2})', identity['disclosures']['F1_largest_observed'])
    return m.group(1), m.group(2), m.group(3)


def build_live_claims(root=None, fresh_test: str = 'pending', rehearsal_days: tuple[str, ...] = (),
                      live: dict | None = None) -> dict:
    """{'values': {live_key: text}, 'shared': {record_key: text}, 'limitations': [(label, key)]}. `live` is
    `live_summary(live_record(...))`: the live product's claims (CP-18c); None gives CP-18b's rehearsal claims."""
    from cp17 import scoring
    from cp17.attribution import WORDING
    import delu_forecast.claims as record
    from delu_forecast.claims import REPO_ROOT, build_claims
    root = Path(root or REPO_ROOT)
    if fresh_test not in STATES:
        raise ValueError(f'fresh_test: one of {STATES}')
    identity = json.loads(_read(root, MANIFEST))
    pi = identity['policy_identity']
    protocol = _read(root, PROTOCOL)
    report = _read(root, CP17_REPORT)
    f1, f1_level, f1_day = _f1(root)
    f1_where = f"A1's {f1_level} on {f1_day}"
    status = {'pending': 'final candidate · pending 4.7T', 'passed': 'live',
              'failed': 'tested candidate · did not pass 4.7T'}[fresh_test]
    first, last = (rehearsal_days[0], rehearsal_days[-1]) if rehearsal_days else ('', '')
    values = {
        'live_product_name': 'A1 · DDNN-2 alone',
        'live_product_designation': pi['designation'],
        'live_product_status': status,
        'live_released_product': ('v1 stays the released product until CP-18\'s activation, which requires a passed '
                                  '4.7T' if fresh_test != 'failed' else 'v1 stays the released product'),
        'live_hero_rule': ("A1 is shown as \"final candidate · pending 4.7T\" until 4.7T is scored. It becomes \"live\" "
                           "only at CP-18's activation, which requires a passed 4.7T. On a fail, v1 stays the released "
                           "product."),
        'live_fresh_test_badge': _quoted(protocol, '**The badge:**'),
        'live_fresh_test_wording': _quoted(protocol, '**The wording:**'),
        'live_development_badge': 'development · post-selection',
        'live_prospective_label': 'prospective evaluation in progress',
        'live_rehearsal_badge': ('development rehearsal · CP-18 dry runs on development days'
                                 + (f' {first} to {last}' if first else '') + ' · not prospective and not 4.7T'),
        'live_percentage_label': scoring.PERCENTAGE_LABEL,
        'live_coverage_wording': 'nominal {level}% interval; measured coverage {share} over {window}; mean width {width} EUR/MWh',
        'live_retrained_label': 'your retrained model',
        'live_counterfactual_label': 'counterfactual scenario — not an issued forecast',
        'live_attribution_wording': WORDING,
        'live_explain_wording': 'contributed {value} EUR/MWh to this forecast, relative to the model\'s baseline',
        'live_features_wording': 'how much this fitted model relies on each input',
        'live_retrain_wording': (_quoted(report, '**Proposed wording**') + ' The issued values were computed in the same '
                                 'WebAssembly runtime the visitor runs. On development days that runtime\'s results '
                                 f'differed from native arithmetic by up to {f1} EUR/MWh ({f1_where}), the largest '
                                 'difference observed, not a bound.'),
        'live_policy_identity_sha256': identity['policy_identity_sha256'],
        'live_package_sha256': pi['code']['package_sha256'],
        'live_issuing_host': 'Pyodide 0.28.0 in Node.js v26.7.0',
        'live_reference_runtime': (f"Pyodide {pi['reference_runtime']['pyodide']}; Chromium "
                                   f"{pi['reference_runtime']['chromium']} and WebKit {pi['reference_runtime']['webkit']} "
                                   f"through Playwright {pi['reference_runtime']['playwright']}; "
                                   f"{pi['reference_runtime']['machine_class']}"),
        'live_cutoff': 'D−1 11:00 Europe/Berlin, strictly before',
        # the Data view's definition, from the claim layer's sentence (its first clause; the rest is v1's)
        'live_data_floor': record.FLOOR_CHANGE.split(',')[0] + '.',
        # the limitations, generated
        'live_limitation_evidence': (
            'Every result shown is development evidence on data through 2026-09-06, post-selection and descriptive. '
            'A1 has not yet been tested on fresh data: its one-shot test (4.7T) is registered and not yet scored, and '
            'the prospective record is "prospective evaluation in progress" until CP-19.'),
        'live_limitation_rehearsal': (
            'The issued days in this Space are a development rehearsal: CP-18\'s dry runs of the daily pipeline on '
            + (f'development days {first} to {last}, ' if first else 'development days, ') +
            'with a simulated wall clock. They are not prospective forecasts and not 4.7T, and they are never scored '
            'as either.'),
        'live_limitation_f1': (
            'The issued forecasts come from the frozen package running in WebAssembly (Pyodide), the runtime a '
            'visitor\'s browser runs. On development days its results differed from native arithmetic by up to '
            f'{f1} EUR/MWh ({f1_where}), the largest difference observed and not a bound; a visitor\'s retrain is compared with the '
            'issued artifact, not with native arithmetic.'),
        'live_limitation_retrain_selections': (
            '"Train it yourself" compares the data-driven selections the issued artifact records for each of the '
            'eight members (the seed, the training and held-out day sets and the latest training day) and each '
            'member\'s weights\' hash; the artifact does not record the other selections (early stopping\'s epochs, '
            'the winsorisation and cap activations), so those are not compared.'),
        'live_limitation_inputs': (
            'A live day is issued only if each input can be shown to precede its cutoff (D−1 11:00 Europe/Berlin). '
            'The day-ahead load forecast is admitted by its retrieval before the cutoff; its stored development '
            'history rests on the Owner\'s recorded exception (ruling 1), which covers development days only.'),
        'live_limitation_rendered': (
            'On development days the market inputs and outcomes are the development snapshot\'s values (SMARD, pulled '
            '2026-09-08) rendered in each source\'s response shape, not recorded raw responses, so each price\'s '
            'publication time is the documented schedule\'s (13:00 Europe/Berlin on the day before delivery).'),
        'live_limitation_operation': (
            'Daily operation starts only at CP-18\'s activation. Until then nothing here is published, and no '
            'forecast is claimed to have been published before the auction or before its outcome.'),
    }
    labels = {'evidence': 'Development evidence only', 'rehearsal': 'A development rehearsal, not a live record',
              'f1': 'The issuing runtime against native arithmetic', 'retrain_selections': 'What a retrain compares',
              'inputs': 'Inputs shown to precede the cutoff', 'rendered': 'Rendered development responses',
              'operation': 'Not yet operating'}
    values.update(_common(fresh_test))
    if live is not None:
        values.update(_live_values(live, fresh_test, status))
        labels.update(evidence='Development evidence and the live record', rehearsal='The live record',
                      rendered='Where the prices come from', operation='Issue times and run times')
    claims = build_claims()
    shared = {k: claims[k] for k in SHARED}
    shared.update({k: getattr(record, name) for k, name in SHARED_CONSTANTS.items()})
    limitations = [(labels[t], f'live_limitation_{t}') for t in LIMITATION_ORDER] + [
        ('The 15-minute MTU averaging choice', 'limitation_mtu_averaging'),
        ('Data attribution', 'attribution'),
        ('Weather data attribution', 'gfs_attribution')]
    return {'values': values, 'shared': shared, 'limitations': limitations}


OPEN_DAY_WORDING = ('not issued; attempted, and still inside the three-day lookback, so a later run closes it with '
                    'this cause')


def _common(fresh_test: str) -> dict:
    """The keys both modes carry (the page reads them all): N7's labels, the hosts, the history wording, O33's."""
    from cp18 import running
    from cp18.spaceglue import BOUNDARY
    return {
        'live_product_record_name': 'A1, the designated policy',
        'live_evidence_prefix': 'Evidence, as the manifest states it: ',
        'live_open_day_wording': OPEN_DAY_WORDING,
        # O18's N7: the artifact's nominal D−1 11:00 is the information cutoff, not when the work happened
        'live_issue_time_label': 'cutoff-based issue time',
        'live_issue_time_note': ('the information cutoff, D−1 11:00 Europe/Berlin, which the artifact records as its '
                                 'issue time; it is not when the run happened'),
        'live_run_time_label': 'actual run',
        'live_run_time_absent': ('not in this build: it was built without the live record, so no run time is '
                                 'shown'),
        'live_host_local': "the local fallback (the Owner's Mac)",
        'live_host_runner': 'the scheduled runner (GitHub Actions)',
        'live_outside_wording': ("never issued by the live product: the days between the freeze origin and the first "
                                 "live day (the Owner's decision 28)"),
        'live_history_wording': ("v1's frozen demo, kept as history. It is not the product this Space presents."),
        'live_history_network': ("v1's demo loads its own runtime as v1 shipped it; it is not part of this Space's "
                                 "network rule, which covers the product's pages only."),
        'live_development_scope': (f'development displays: delivery days through {BOUNDARY}, never pooled with the '
                                   'live record'),
        # O32 and O33
        'live_daily_errors_wording': ("each issued day's MAE and interval score (WIS), EUR/MWh, beside the "
                                      'similar-day naive (B0) as a reference, not a target'),
        'live_running_wording': running.WORDING,
        'live_running_before_minimum': running.BEFORE_MINIMUM,
        'live_running_difference': ('the product minus the similar-day naive (B0), on the days both scored; below '
                                    'zero the product\'s daily error was smaller'),
    }


def _live_values(live: dict, fresh_test: str, status: str) -> dict:
    """The live product's claims (CP-18c): O30's name, O13's status, O29's product rule, the live limitations."""
    from cp18.spaceglue import BOUNDARY
    first = live['first_live_day']
    outside = live.get('outside') or []
    gone = ('; '.join(f"{o['first_day']} to {o['last_day']}" for o in outside)) or 'none'
    failed = fresh_test == 'failed'
    return {
        'live_product_name': 'v6 · DDNN-2 alone',
        'live_product_record_name': 'v6 (A1 in the frozen records)',
        'live_evidence_prefix': 'Evidence, as the manifest states it (the frozen records name v6 "A1"): ',
        'live_open_day_wording': OPEN_DAY_WORDING,
        'live_product_status': status,
        'live_released_product': (
            'v1 is the product again: 4.7T did not pass' if failed else
            "v6 is the product now, before 4.7T (the Owner's decision 28); v1 is the last released generation, kept "
            'at History as historical; on a failed or inconclusive 4.7T, v1 is the product again'),
        'live_hero_rule': (
            'v6 is shown as "final candidate · pending 4.7T" until 4.7T is scored: its one-shot fresh-data test is '
            'registered and not yet scored, and nothing in the live record is 4.7T\'s issuance or score. The live '
            'record\'s scores are "prospective evaluation in progress", never a test result.'),
        'live_history_wording': ("v1, the last released generation: its frozen demo, kept as history. It is not the "
                                 'product this Space presents; on a failed or inconclusive 4.7T, v1 is the product '
                                 'again.'),
        'live_run_time_absent': 'not in the live record',
        'live_limitation_evidence': (
            f'The development results shown are development evidence on delivery days through {BOUNDARY}, '
            'post-selection and descriptive. The live record\'s scores are prospective evaluation in progress, on the '
            'live product\'s own issued days: they are not 4.7T\'s, not a test result, and never pooled with '
            'development. v6 has not yet been tested on fresh data: its one-shot test (4.7T) is registered and not '
            'yet scored.'),
        'live_limitation_rehearsal': (
            f"The issued days in this Space are the live product's own, from {first} (the Owner's decision 28); "
            f'the days {gone} are outside the live record and never issued by the live product. Nothing here is '
            '4.7T\'s issuance or score: 4.7T issues its own window under its registered terms.'),
        'live_limitation_rendered': (
            'In the live record each published price names its source and the archive record that served it. The '
            f'development displays read the development snapshot, on delivery days through {BOUNDARY}.'),
        'live_limitation_operation': (
            'Each issued day shows two times: its cutoff-based issue time, the information cutoff (D−1 11:00 '
            'Europe/Berlin) that the artifact records, and its actual run\'s start and end, with where it ran (the '
            'local fallback or the runner). A run can happen after the auction and after the day\'s prices are '
            'published (a catch-up within the lookback); the forecast still rests only on inputs shown to precede its '
            'cutoff, and no forecast is claimed to have been published before the auction or before its outcome.'),
    }


# ------------------------------------------------------------------ the live record the Space shows (CP-18c)
def _when(value) -> str | None:
    """An instant as recorded, restated `...+00:00` when written `...Z` (one notation for the page)."""
    if not isinstance(value, str) or not value:
        return None
    return value[:-1] + '+00:00' if value.endswith('Z') else value


def _runner(record: dict) -> dict | None:
    env = ((record.get('gate') or {}).get('machine') or {}).get('runner_env') or {}
    if not any(env.get(k) for k in ('GITHUB_RUN_ID', 'ImageVersion')):
        return None
    return {'github_run_id': env.get('GITHUB_RUN_ID'), 'image_version': env.get('ImageVersion'),
            'image_os': env.get('ImageOS')}


def live_record(folder) -> dict:
    """The live store's record for the Space: `folder` is the data-only live folder (its `store/`). The store is
    verified first (`cp18.store.LiveStore.verify`, every CP-17c check and CP-18a's); each issued day's record is read
    by the hash its ledger entry holds."""
    import hashlib
    from datetime import date as _date, timedelta
    from cp18 import causes
    from cp18.store import LiveStore, head_sha256, ledger_sha256
    store = LiveStore(Path(folder) / 'store')
    head = store.verify()
    entries = store.entries()
    genesis = entries[0]
    issued, failed, not_issued, outside = [], [], [], []
    for entry in entries:
        kind = entry['kind']
        if kind == 'issuance':
            raw = (store.folder / entry['record_file']).read_bytes()
            if hashlib.sha256(raw).hexdigest() != entry['record_file_sha256']:
                raise ValueError(f"{entry['day']}: the day's record differs from its ledger entry")
            rec = json.loads(raw)
            if rec.get('artifact_sha256') != entry['artifact_sha256'] or rec.get('day') != entry['day']:
                raise ValueError(f"{entry['day']}: the day's record names another artifact or day")
            host = rec.get('host_kind')
            if host not in HOSTS:
                raise ValueError(f"{entry['day']}: the record's host {host!r} is not one of {HOSTS}")
            item = {'day': entry['day'], 'policy': entry.get('issued_policy'), 'display': entry.get('display'),
                    'artifact_sha256': entry['artifact_sha256'], 'record_sha256': entry['record_file_sha256'],
                    'cutoff_utc': _when(rec.get('cutoff_utc')), 'run_id': rec.get('run_id'), 'host_kind': host,
                    'runner': _runner(rec) if host == 'runner' else None,
                    'run_started_utc': _when(rec.get('run_started_utc')),
                    'issuance_started_utc': _when(rec.get('issuance_started_utc')),
                    'issuance_finished_utc': _when(rec.get('issuance_finished_utc')),
                    'data_refresh_utc': _when((rec.get('inputs') or {}).get('data_refresh_utc'))}
            if entry.get('issued_policy'):
                issued.append(item)
            else:
                failed.append(dict(item, cause=causes.CHAIN, cause_text=causes.text(causes.CHAIN)))
        elif kind == 'not_issued':
            not_issued.append({'day': entry['day'], 'cause': entry['cause'], 'cause_text': causes.text(entry['cause']),
                               'attempts': list(entry.get('attempts') or [])})
        elif kind == 'carry':
            last, nxt = _date.fromisoformat(entry['last_window_day']), _date.fromisoformat(entry['first_live_day'])
            if (nxt - last).days > 1:
                outside.append({'first_day': str(last + timedelta(days=1)), 'last_day': str(nxt - timedelta(days=1)),
                                'days': (nxt - last).days - 1, 'first_live_day': str(nxt), 'reason': entry['reason']})
    runs = []
    # The open days (CP-18c): attempted by a run and not issued, still inside decision 23's lookback, so not yet closed
    # in the ledger; each with its latest attempt's cause. A later issuance, or the lookback, closes them.
    decided = set(store.days())
    attempts: dict[str, list] = {}
    for run in store.runs():
        for day, item in sorted((run.get('days') or {}).items()):
            if day not in decided and item.get('status') == 'open' and item.get('cause'):
                attempts.setdefault(day, []).append((run.get('run_id'), item['cause']))
    open_days = [{'day': day, 'cause': tries[-1][1], 'cause_text': causes.text(tries[-1][1]),
                  'attempts': [r for r, _ in tries]} for day, tries in sorted(attempts.items())]
    for run in store.runs():
        runs.append({'run_id': run.get('run_id'), 'host_kind': run.get('host_kind'), 'mode': run.get('mode'),
                     'started_utc': _when(run.get('started_utc')), 'finished_utc': _when(run.get('finished_utc')),
                     'target_day': run.get('target_day'), 'planned': run.get('planned') or [],
                     'outcome': run.get('outcome'), 'exit': run.get('exit')})
    carried = [e for e in entries if e['kind'] == 'carry']
    return {'schema': RECORD_SCHEMA, 'source': 'cp18.store.LiveStore (live/store), verified',
            'store': {'head_sha256': head_sha256(store.folder), 'ledger_sha256': ledger_sha256(store.folder),
                      'entries': len(entries), 'last_entry_sha256': head['entry_sha256'],
                      'origin': genesis.get('origin'), 'first_day': genesis.get('first_day') or genesis.get('origin'),
                      'first_live_day': carried[-1]['first_live_day'] if carried else
                      (genesis.get('first_day') or genesis.get('origin')),
                      'last_day': head.get('last_day')},
            'issued': issued, 'failed': failed, 'not_issued': not_issued, 'open': open_days, 'outside': outside,
            'runs': runs}


def live_summary(record: dict) -> dict:
    """What the live claims need of the live record: its first live day and the days outside it."""
    return {'first_live_day': record['store']['first_live_day'],
            'outside': [{k: o[k] for k in ('first_day', 'last_day', 'days')} for o in record['outside']],
            'issued_days': len(record['issued'])}


def text(claims: dict, key: str) -> str:
    return claims['values'][key] if key.startswith('live_') else claims['shared'][key]
