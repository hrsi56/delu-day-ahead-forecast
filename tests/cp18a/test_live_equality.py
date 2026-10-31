"""CP-18a item 2, end to end on the local recorded inputs: the live builder equal to the development builder.

* One parity origin (2026-03-29, the spring transition day): the archive for D-7..D is built here, from SMARD
  responses rendered from the committed snapshot (not recorded raw responses) and CP-20's recorded decoded GFS
  runs; `build_day` then writes A1, v4, v2 and B0, which must equal CP-17b's reference payloads byte for byte.
* The GFS client on CP-25's recorded 2026-09-05 run: the listing and index rendered from the recorded values,
  the recorded raw messages served by byte range, decoded by CP-20's decoder in the ecCodes environment, and
  compared with the recorded decoded run and with the committed weather features.

Each skips, with its reason, where the local recorded inputs are absent (for example on a CI runner).
`reports/cp18a/live-equality.json` (`python -m cp18.live.equality`) covers all 9 + 14 days.
"""
from __future__ import annotations

from datetime import date, timedelta
import json
from pathlib import Path

import pytest

from cp18.live import archive as AR
from cp18.live import build, equality, gfs, recorded

ROOT = Path(__file__).resolve().parents[2]
DAY = date(2026, 3, 29)
LOCAL = {'reference payloads': equality.REFERENCE['parity'] / f'A1-{DAY}.json',
         'CP-20 recorded decoded runs': recorded.CP20_WEATHER / 'runs' / f'{DAY - timedelta(days=1)}.npz',
         "A1's search state": equality.SEARCH_DIR / 'k12.json'}


def _missing(paths: dict) -> list[str]:
    return [f'{k} ({v})' for k, v in paths.items() if not Path(v).exists()]


@pytest.mark.skipif(bool(_missing(LOCAL)), reason='local recorded inputs absent: ' + '; '.join(_missing(LOCAL)))
def test_one_parity_origin_is_byte_identical(tmp_path):
    days = [DAY - timedelta(days=k) for k in range(7, -1, -1)]
    snap = recorded.snapshot(ROOT)
    recorded.render_smard(tmp_path / 'replay' / 'smard', snap, recorded.market_days(days))
    arch = AR.Archive(tmp_path / 'archive')
    for x in days:
        item = recorded.archive_day(arch, tmp_path / 'replay', x, ROOT, 'smard')
        assert not item['verify'] and not item['problems']
        assert item['size']['bytes'] < 1_000_000
    ref = equality.REFERENCE['parity']
    r = build.build_day(DAY, archive=arch, base_end=DAY - timedelta(days=8), buffers=equality.reference_buffers(ref, DAY),
                        search_dir=equality.SEARCH_DIR, out=tmp_path / 'out', root=ROOT)
    assert r['status'] == 'built', r['cause']
    assert r['gfs_available'] is True and r['availability']['shown'] is True
    assert {j['data_day'] for j in r['availability']['by_exception']} == {d.isoformat() for d in days}
    for policy in build.POLICIES:
        cmp = equality.compare(ref, tmp_path / 'out', policy, DAY)
        assert cmp['equal'], cmp['stem']
    assert json.loads((tmp_path / 'out' / f'A1-{DAY}.json').read_text())['search'] == 12


GFS_LOCAL = {'the ecCodes environment': gfs.WX_PYTHON,
             "CP-25's retained raw messages": recorded.CP25_WEATHER / 'raw' / '2026-09-05' / 'f021_u10_aws.grib2',
             "CP-25's recorded run": recorded.CP25_WEATHER / 'runs' / '2026-09-05.json'}


@pytest.mark.skipif(bool(_missing(GFS_LOCAL)), reason='local GFS material absent: ' + '; '.join(_missing(GFS_LOCAL)))
def test_gfs_client_reproduces_the_recorded_run(tmp_path):
    out = recorded.gfs_client(date(2026, 9, 5), tmp_path, ROOT)
    assert out['messages_retrieved'] == 50 and out['messages_equal_to_record'] and not out['retrieval_problems']
    assert out['decode']['data_bitwise_equal'] and out['decode']['metadata_equal']
    assert out['archive']['gfs_available'] and out['archive']['features_bitwise_equal_to_committed']
    assert out['archive']['size']['bytes'] < 1_000_000
    assert out['pass']
