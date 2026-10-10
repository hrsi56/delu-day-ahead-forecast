"""Compatibility entry point for CP-22; delegates to the ordinary resource monitor.

Work availability is unrestricted under the Owner decision of 2026-10-10.
Historical invocation records remain preserved at their reviewed Git revisions.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys


def main() -> int:
    path = Path(__file__).with_name('cp22_revision.py')
    spec = importlib.util.spec_from_file_location('cp22_revision', path)
    driver = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver)
    sys.argv[0] = str(path)
    return driver.main()


if __name__ == '__main__':
    raise SystemExit(main())
