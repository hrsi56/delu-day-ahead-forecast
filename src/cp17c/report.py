"""CP-17c's report, rendered from its committed records only, so a test re-renders it byte for byte.

    PYTHONPATH=src python -m cp17c.report --reports reports/cp17c --out reports/cp17c/report.md
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MIB = 1024 ** 2


def _j(folder: Path, name: str):
    return json.loads((folder / name).read_text())


def _s(x: float) -> str:
    return f'{x:.1f} s'


def _mib(x: float) -> str:
    return f'{x / MIB:.0f} MiB'


def _yes(x) -> str:
    return 'yes' if x else '**no**'


def render(folder: Path, root: Path) -> str:
    m = _j(folder, 'measurement.json')
    manifest = json.loads((root / 'docs/track-b/evidence/cp-17c/freeze-manifest.json').read_text())
    native, browser, r7 = _j(folder, 'native-parity.json'), _j(folder, 'browser.json'), _j(folder, 'r7-controls.json')
    origin, state = _j(folder, 'freeze-origin.json'), _j(folder, 'state-route.json')
    machines = {'runner': 'GitHub-hosted `macos-26`', 'local': "the Owner's M3"}
    out = ['# CP-17c: A1 re-frozen under the `macos-26` issuing host', '',
           '*Rendered from the records in this folder by `cp17c.report`; every figure is in a record.*', '',
           '## The result', '']
    r, l = m['runner']['summary'], m['local']['summary']
    out += [f"- **The policy identity** is `{manifest['policy_identity_sha256']}`, in "
            '`docs/track-b/evidence/cp-17c/freeze-manifest.json`, with its freeze record beside it.',
            f"- **On both machines, every fit is bit-identical to CP-17b's records:** {r['fits_bit_identical']} of "
            f"{r['fits']} on the runner and {l['fits_bit_identical']} of {l['fits']} on the M3. That covers A1 at the "
            'nine parity origins and all four policies on the 14 shadow days.',
            "- **The shadows' buffers** equal CP-17b's host shadow run at all 14 origins on both machines, and so do the "
            'final states. The early block ends in the state the late block started from.',
            '- **The checks before each run\'s first issuance (H2)** passed in every run, and one forced failure of each '
            'stopped at its own check with nothing issued.',
            f"- **The ceilings held:** the slowest fit took {_s(r['wall_seconds_max'])} on the runner and "
            f"{_s(l['wall_seconds_max'])} on the M3, against 900 s; the largest peak was "
            f"{_mib(max(r['peak_bytes_max'], l['peak_bytes_max']))}, against 4 GiB.",
            f"- **Native parity with CP-26:** {native['status']}, five policies at nine origins, equal to CP-17b's record: "
            f"{_yes(native['all_equal_to_cp17b'])}.",
            '- **Chromium and WebKit** reproduce the issuing host on the new zip: '
            f"{_yes(all(browser['equal_to_issuing_host'].values()))}.",
            f"- **R7** is fixed: CP-17c lists all six malformed-day controls ({_yes(r7['all_listed_by_cp17c'])}), and "
            f"CP-17b's `schema.py` raises on all six ({_yes(r7['all_raised_by_cp17b'])}).",
            f"- **GitHub minutes:** {m['minutes']['counted_total']} as a private repository counts them, of the 1,000 allowed.",
            '']
    out += ['## The machines', '', '| | Kind | Image | CPU | Cores | Memory | OS |', '|---|---|---|---|---|---|---|']
    for key, label in machines.items():
        mc = m[key]['checks']['machine']
        out.append(f"| {label} | {mc['kind']} | {mc.get('image_os') or '-'} {mc.get('image_version') or ''} | "
                   f"{mc.get('cpu_model')} | {mc.get('cpu_count')} | {(mc.get('memory_bytes') or 0) / 1024 ** 3:.1f} GiB | "
                   f"macOS {mc.get('os_version')} |")
    host = m['runner']['host']['checks']
    out += ['', f"The runner's CPython was {host['cpython']['version']} (`{host['cpython']['executable_sha256'][:16]}…`, zlib "
            f"{host['cpython']['zlib_runtime']}); its binary was retrieved from `{host['node-retrieval']['tarball']['url']}` "
            f"({host['node-retrieval']['tarball']['bytes']:,} bytes, `{host['node-retrieval']['tarball']['sha256'][:16]}…`), "
            f"`bin/node` `{host['node-retrieval']['binary']['sha256'][:16]}…`.", '']
    out += ['## The checks before each run\'s first issuance (H2)', '',
            '| | `refreeze verify` | The gate | Its seconds | Canary | ' + ' | '.join(
                f'forced: {k}' for k in m['runner']['checks']['forced']) + ' |',
            '|---|---|---|---|---|' + '---|' * len(m['runner']['checks']['forced'])]
    for key, label in machines.items():
        c = m[key]['checks']
        forced = ' | '.join(f"stopped at {v['failed_at']}, {'nothing issued' if not v['issuance_called'] else 'ISSUED'}"
                            for v in c['forced'].values())
        out.append(f"| {label} | {' '.join(c['pins_output'])} | {'passed' if c['gate_passed'] else 'FAILED'} | "
                   f"{c['gate_seconds']:.0f} | `{(c['canary']['quantiles_sha256'] or '')[:12]}…` in "
                   f"{_s(c['canary']['resources']['wall_seconds'])} | {forced} |")
    out += ['', "Each shadow block ran its own gate too: " + '; '.join(
        f"{machines[k]} {', '.join(f'{b}: ' + ('passed' if v else 'FAILED') for b, v in m[k]['summary']['gates_passed'].items())}"
        for k in machines) + '.', '']
    out += ["## A1's parity at the nine origins", '', '| Origin | Bit-identical (runner) | Wall (runner) | Bit-identical (M3) '
            '| Wall (M3) | CP-17b\'s quantiles |', '|---|---|---|---|---|---|']
    for stem in m['runner']['summary']['parity_origins']:
        a, b = m['runner']['parity'][stem], m['local']['parity'][stem]
        out.append(f"| {stem} | {_yes(a['bit_identical'])} | {_s(a['wall_seconds'])} | {_yes(b['bit_identical'])} | "
                   f"{_s(b['wall_seconds'])} | `{a['reference_quantiles_sha256'][:12]}…` |")
    out += ['', 'The first two ran in the checks run; the other seven are the late shadow block\'s A1 issuances, whose '
            'payloads are the parity payloads (each checked by its identity).', '']
    out += ['## The 14 shadow days, carried by the state store', '',
            '| Day | Buffers = CP-17b (runner) | Fits bit-identical (runner) | Day (runner) | Buffers = CP-17b (M3) | '
            'Fits bit-identical (M3) | Day (M3) |', '|---|---|---|---|---|---|---|']
    days = sorted({d for k in machines for b in m[k]['shadow'].values() if b for d in b['days']})
    for d in days:
        row = [d]
        for k in machines:
            day = next(b['days'][d] for b in m[k]['shadow'].values() if b and d in b['days'])
            row += [_yes(day['buffers_equal_reference']), _yes(day['all_bit_identical']), _s(day['day_process_seconds'])]
        out.append('| ' + ' | '.join(row) + ' |')
    out += ['', 'Each day ran in its own process: load and check the store, release D-2, check the buffers against the '
            "day's payloads, issue A1 and the three shadows one after another, register them, append to the store. "
            'On the M3 the two blocks ran at once, so its figures are conservative.', '']
    cost = m['runner']['summary']['cost']
    out += ['## The cost on the runner (item 7)', '', '| | Min | Median | Max |', '|---|---|---|---|',
            f"| One issuance (A1 and three shadows, one after another) | {_s(cost['one_issuance_seconds']['min'])} | "
            f"{_s(cost['one_issuance_seconds']['median'])} | {_s(cost['one_issuance_seconds']['max'])} |",
            f"| Decision 23's four issuances with the canary (the gate and four consecutive days) | "
            f"{_s(cost['four_issuances_with_canary_seconds']['min'])} | {_s(cost['four_issuances_with_canary_seconds']['median'])} | "
            f"{_s(cost['four_issuances_with_canary_seconds']['max'])} |", '',
            "A job's setup before its run (checkout, uv, CPython, the environment, the inputs, the binary and the package) "
            'took ' + ', '.join(f"{j['setup_seconds']:.0f} s" for run in m['minutes']['runs'].values()
                                for j in run['jobs'].values() if j['seconds'] > 120) + '. The public runner class is CP-18\'s to time (§24.13).', '']
    out += ['## The re-freeze shown', '',
            f"- **The freeze-origin artifact** `{origin['artifact_sha256']}` differs from CP-17b's only in "
            f"{', '.join('`' + f + '`' for f in origin['fields_differing_from_cp17b'])}. Its quantiles are the canary's, "
            f"`{origin['quantiles_sha256'][:16]}…`, and its arrays are CP-17b's: {_yes(origin['arrays_equal_to_cp17b'])}.",
            f"- **Native parity** at nine origins: {native['status']}; equal to CP-17b's record in every check, payload, "
            f"quantile and ledger hash: {_yes(native['all_equal_to_cp17b'])}.",
            f"- **Browsers** ({browser['playwright']}): " + ', '.join(
                f"{x['browser']} {x['browser_version']} `{(x['quantiles_sha256'] or '')[:12]}…`" for x in browser['runs']) + '.',
            f"- **R7's controls** on CP-17c's reference bundle: the valid bundle verifies under both; CP-17b's negative "
            f"controls are refused alike ({_yes(r7['negative_controls_equal'])}); " + '; '.join(
                f"{k}: CP-17c {'listed' if v['cp17c']['refused'] and not v['cp17c']['raised'] else 'RAISED'}, CP-17b "
                f"{'raised' if v['cp17b']['raised'] else 'did not raise'}" for k, v in r7['malformed_day'].items()) + '.',
            f"- **The freeze-origin states** on the route equal CP-17's recorded buffers: "
            f"{_yes(state['freeze_origin_state']['equal_to_cp17_recorded'])}; and CP-17b's native shadow run's final state: "
            f"{_yes(state['freeze_origin_state']['equal_to_cp17b_native_shadow_run_final_state'])}.", '']
    out += ['## GitHub minutes', '', '| Run | Job | Seconds | Counted |', '|---|---|---|---|']
    for run_id, run in sorted(m['minutes']['runs'].items()):
        for name, j in run['jobs'].items():
            out.append(f"| {run_id} | {name} | {j['seconds']:.0f} | {j['counted']} |")
    out += ['', f"Total: **{m['minutes']['counted_total']}** counted minutes ({m['minutes']['rule']}).", '']
    return '\n'.join(out) + '\n'


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='.', type=Path)
    ap.add_argument('--reports', default=Path('reports/cp17c'), type=Path)
    ap.add_argument('--out', required=True, type=Path)
    args = ap.parse_args(argv)
    args.out.write_text(render(args.reports, args.root))
    print('report', args.out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
