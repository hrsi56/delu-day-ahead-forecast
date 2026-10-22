"""CP-26's evidence is immutable while the Orchestrator's exposure ledger grows."""
import hashlib
from pathlib import Path

from cp26 import harness as H
from cp26_ledger_snapshot import FROZEN_LEDGER, LIVE_LEDGER, table_rows


def test_live_exposure_ledger_preserves_frozen_cp26_rows():
    root = Path(__file__).resolve().parents[1]
    frozen = (root / FROZEN_LEDGER).read_bytes()
    assert hashlib.sha256(frozen).hexdigest() == H.PINS[LIVE_LEDGER]
    rows = table_rows(frozen)
    assert rows and len(rows) >= 3  # A header, separator and at least one historical entry.
    live_rows = table_rows((root / LIVE_LEDGER).read_bytes())
    assert live_rows[:len(rows)] == rows, 'CP-26 exposure rows must remain verbatim and in order'
