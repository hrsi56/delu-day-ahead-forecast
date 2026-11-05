"""CP-18b's shared fixtures: the committed dry-run store and the dated bundle built from it.

Everything here is committed (development data through 2026-09-06 only), so the suite runs on a history-free CI copy
with no `.local/`. Tests over local-only material (CP-18a's downloaded run records, CP-26's stored ledger) skip with
a stated reason when it is absent.
"""
from __future__ import annotations

from datetime import datetime
import json
import os
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[2]
STORE = ROOT / 'reports/cp18b/dryrun/store'
BUNDLE = ROOT / 'reports/cp18b/bundle'
RECORDED = ROOT / 'reports/cp18a/dryrun/recorded'
REPLAY = RECORDED / 'replay' / 'smard'
NOW = datetime.fromisoformat('2026-09-05T10:00:00+02:00')
PROJECT = Path(os.environ.get('CP17_PROJECT_ROOT') or '/Users/djourno/Downloads/PJM')
DOWNLOADS = PROJECT / '.local/artifacts/cp-18a/downloads'


import platform

#: Native floating-point results (B0's shadow arithmetic, the committed records' reals) are pinned on the issuing host's
#: platform; a byte-equality test over them runs there only (CP-18a's CI repair, a1625b1a).
issuing_platform = pytest.mark.skipif(
    (platform.system(), platform.machine()) != ('Darwin', 'arm64'),
    reason='the bytes are pinned on the issuing host platform, darwin-arm64 (the macos-26 runner and the Owner\'s Mac); '
           'native floating point elsewhere may differ in the last bit, which the recomputation tolerance covers')


def local_only(path: Path, what: str):
    return pytest.mark.skipif(not Path(path).exists(), reason=f'{what} is local-only ({path} is absent)')


@pytest.fixture
def files() -> dict[str, bytes]:
    from cp18.bundle import read
    return read(BUNDLE)


@pytest.fixture
def live(tmp_path) -> Path:
    """A fresh data-only folder holding a copy of the committed dry-run store."""
    folder = tmp_path / 'live'
    folder.mkdir()
    shutil.copytree(STORE, folder / 'store')
    return folder


def build(live: Path, out: Path, now=NOW, **kwargs) -> dict:
    """The dated bundle from `live`'s store, with the committed bundle's payloads and arrays as the sources."""
    from cp18 import bundle as B
    return B.build(root=ROOT, store_dir=live / 'store', archive=live / 'inputs', outcomes_dir=live / 'outcomes',
                   now=now, out=out, arrays=BUNDLE / 'artifact-arrays.npz', caches=[BUNDLE], project=PROJECT,
                   recorded=RECORDED, **kwargs)


def load(path: Path):
    return json.loads(Path(path).read_text())
