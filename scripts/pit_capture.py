#!/usr/bin/env python
"""Point-in-time capture instrument (capstone_V6_5.md Section 3 / M0.5 CP-0).

Standalone entry point. Requires only ENTSOE_API_TOKEN for the live path;
--replay-xml needs no token at all.

    python scripts/pit_capture.py capture --at-utc 2026-08-05T08:30:00Z
    python scripts/pit_capture.py verify
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pit_capture.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
