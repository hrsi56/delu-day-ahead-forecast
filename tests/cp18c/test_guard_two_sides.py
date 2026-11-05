"""The guard, retired for the live pipeline only (r20 §24.14 item 2; CP-18c item 1): both sides.

- **The research side** still refuses any delivery day, row or GFS run after 2026-09-06: `cp25.guard` itself (frozen,
  byte for byte as CP-17c's manifest binds it), CP-17c's development builder (`cp17.tools.payloads`), CP-25's GFS
  downloader (`cp25.extract`'s `GuardedFetcher` route through `cp25.guard.admit_url`), CP-18's development inputs
  (`cp18.inputs.SnapshotTruth`) and every `cp18.boundary` check outside a `live()` block (dry runs, rehearsals).
- **The live side** (`cp18.boundary.live()`) admits days through the present, never after it; a GFS run only up to the
  present; and keeps the live red line: each day's own cutoff, the target-day embargo and ruling 1's scope.
"""
from __future__ import annotations

from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path

import pytest

from cp18 import boundary, plan
from cp18.live import availability as A
from cp18.live import entsoe, smard
from cp18.live.archive import Archive
from cp18.live.transport import Request
from cp25 import guard

REPO = Path(__file__).resolve().parents[2]
UTC = timezone.utc
PRESENT = datetime(2026, 11, 5, 9, 30, tzinfo=UTC)
AFTER = date(2026, 9, 7)


def aws(run: date, lead: int, listing: bool = False) -> str:
    stem = f'gfs.{run:%Y%m%d}/00/atmos/gfs.t00z.pgrb2.0p25.f{lead:03d}'
    if listing:
        return f'https://{guard.AWS_HOST}/?list-type=2&prefix={stem}'
    return f'https://{guard.AWS_HOST}/{stem}'


def _find(value, key):
    if isinstance(value, dict):
        for k, v in value.items():
            if k == key:
                return v
            found = _find(v, key)
            if found is not None:
                return found
    elif isinstance(value, list):
        for v in value:
            found = _find(v, key)
            if found is not None:
                return found
    return None


# ---- the research side -------------------------------------------------------------------------------------------

def test_the_frozen_guard_is_unchanged_and_still_refuses_after_the_boundary():
    manifest = json.loads((REPO / 'docs/track-b/evidence/cp-17c/freeze-manifest.json').read_text())
    pinned = _find(manifest, 'cp25/guard.py')
    assert pinned and hashlib.sha256((REPO / 'src/cp25/guard.py').read_bytes()).hexdigest() == pinned
    assert guard.BOUNDARY == date(2026, 9, 6)
    with pytest.raises(guard.BoundaryRefused):
        guard.admit_delivery_day(AFTER)
    with pytest.raises(guard.BoundaryRefused):
        guard.admit_url(aws(date(2026, 9, 6), 21))
    guard.admit_url(aws(date(2026, 9, 5), 48))          # the last admitted run, as before


def test_cp17cs_development_builder_refuses_after_the_boundary_even_inside_the_live_block():
    from cp17.tools import payloads
    for scope in (boundary.live(now=PRESENT), _nothing()):
        with scope:
            with pytest.raises((guard.BoundaryRefused, ValueError)):
                payloads.admit(AFTER)
            payloads.admit(date(2026, 9, 6))


def test_cp25s_gfs_downloader_route_refuses_after_the_boundary_even_inside_the_live_block():
    from cp25 import extract
    assert 'guard.admit_url(url)' in Path(extract.__file__).read_text()     # its GuardedFetcher's only admission
    with boundary.live(now=PRESENT):
        with pytest.raises(guard.BoundaryRefused):
            guard.admit_url(aws(date(2026, 11, 4), 21))


def test_cp18s_development_inputs_refuse_after_the_boundary_even_inside_the_live_block():
    from cp18.inputs import SnapshotTruth
    truth = SnapshotTruth(REPO)
    with boundary.live(now=PRESENT):
        with pytest.raises(guard.BoundaryRefused):
            truth(AFTER)


def test_outside_the_live_block_every_cp18_check_is_the_guards():
    assert boundary.mode() == 'development'
    with pytest.raises(guard.BoundaryRefused):
        boundary.admit_delivery_day(AFTER)
    with pytest.raises(guard.BoundaryRefused):
        plan.admit([date(2026, 9, 5), AFTER])
    with pytest.raises(guard.BoundaryRefused):
        boundary.admit_url(aws(date(2026, 11, 4), 21))
    with pytest.raises(guard.BoundaryRefused):
        Request('GET', smard.ROOT + '/x.json', scope=('market', '2026-09-06', '2026-09-07')).admit()
    with pytest.raises(guard.BoundaryRefused):
        Archive(Path('/nonexistent')).day_dir(AFTER)
    assert boundary.describe()['mode'] == 'development'


def test_the_live_block_ends_with_its_scope():
    with boundary.live(now=PRESENT):
        assert boundary.is_live()
        boundary.admit_delivery_day(date(2026, 11, 6))
    assert not boundary.is_live()
    with pytest.raises(guard.BoundaryRefused):
        boundary.admit_delivery_day(date(2026, 11, 6))


# ---- the live side -----------------------------------------------------------------------------------------------

def test_the_live_side_admits_through_the_present_and_never_after_it():
    with boundary.live(now=PRESENT):
        assert boundary.horizon() == date(2026, 11, 6)
        for d in (AFTER, date(2026, 11, 5), date(2026, 11, 6)):
            assert boundary.admit_delivery_day(d) == d
        with pytest.raises(guard.BoundaryRefused):
            boundary.admit_delivery_day(date(2026, 11, 7))
        with pytest.raises(guard.BoundaryRefused):
            boundary.admit_delivery_day(date(2018, 12, 31))       # the 2019 floor stays
        plan.admit([date(2026, 11, 3), date(2026, 11, 4), date(2026, 11, 5), date(2026, 11, 6)])


def test_the_live_side_admits_a_gfs_run_only_up_to_the_present():
    with boundary.live(now=PRESENT):
        assert boundary.admit_url(aws(date(2026, 11, 5), 21))['run'] == date(2026, 11, 5)
        boundary.admit_url(aws(date(2026, 11, 5), 48, listing=True))
        with pytest.raises(guard.BoundaryRefused):
            boundary.admit_url(aws(date(2026, 11, 6), 21))              # initialized after the present
        with pytest.raises(guard.BoundaryRefused):
            boundary.admit_url(aws(date(2026, 11, 5), 51))              # outside f021-f048
        with pytest.raises(guard.BoundaryRefused):
            boundary.admit_url(aws(date(2026, 11, 5), 21).replace('t00z', 't06z').replace('/00/', '/06/'))
        with pytest.raises(guard.BoundaryRefused):
            boundary.admit_url('https://tds.gdex.ucar.edu/thredds/catalog/files/g/d084001/2026/20261104/catalog.xml')
        with pytest.raises(guard.CredentialRefused):
            boundary.admit_url(aws(date(2026, 11, 5), 21) + '?token=x')


def test_a_live_market_request_may_not_start_after_the_present():
    with boundary.live(now=PRESENT):
        week = smard.bucket_request('load_forecast', 'quarterhour', 1793574000000)     # 2026-11-02 00:00 Berlin
        assert week.days()[0] == date(2026, 11, 2) and week.days()[-1] > boundary.horizon()
        week.admit()
        with pytest.raises(guard.BoundaryRefused):
            smard.bucket_request('load_forecast', 'quarterhour', 1793574000000 + 7 * 86_400_000).admit()   # 11-09
        entsoe.request('load_forecast', [date(2026, 11, 6)]).admit()
        with pytest.raises(guard.BoundaryRefused):
            entsoe.request('load_forecast', [date(2026, 11, 7)]).admit()


def test_the_live_red_line_is_each_days_own_cutoff_the_embargo_and_ruling_1s_scope():
    day = date(2026, 11, 6)
    with boundary.live(now=PRESENT):
        before = {'utc': '2026-11-05T09:59:59Z', 'basis_id': 'retrieval_time', 'basis': 'x'}
        at = {'utc': '2026-11-05T10:00:00Z', 'basis_id': 'retrieval_time', 'basis': 'x'}
        assert A.judge('load_forecast', day, day, before, {'provenance': 'live'})['admitted']
        assert not A.judge('load_forecast', day, day, at, {'provenance': 'live'})['admitted']     # strictly before
        own = {'utc': '2026-11-04T12:00:00Z', 'basis_id': 'documented_schedule', 'basis': 'x'}
        assert not A.judge('price', day, day, own, {'provenance': 'live'})['admitted']           # the embargo
        ruling_1 = {'utc': None, 'basis_id': 'ruling_1_exception', 'basis': 'x'}
        assert not A.judge('load_forecast', day, day, ruling_1, {'provenance': 'rendered'})['admitted']
        assert A.RULING_1_LAST_DAY == date(2026, 9, 6)


class _nothing:
    def __enter__(self):
        return self

    def __exit__(self, *exc):
        return False
