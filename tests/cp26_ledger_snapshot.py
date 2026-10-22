"""Resolve CP-26's historical ledger identity without freezing the living ledger."""
from pathlib import Path


LIVE_LEDGER = 'docs/track-b/exposure-ledger.md'
FROZEN_LEDGER = 'docs/track-b/evidence/cp-26/exposure-ledger-frozen.md'


def identity_path(root, name):
    """The historical harness key stays unchanged; only tests use the evidence copy."""
    return Path(root) / (FROZEN_LEDGER if name == LIVE_LEDGER else name)


def table_rows(raw):
    """Keep exact row bytes (including the header), independent of preceding prose."""
    return [line for line in raw.splitlines() if line.startswith(b'|')]
