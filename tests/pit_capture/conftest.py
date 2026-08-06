"""Make `src/pit_capture` importable without touching the shared venv's
editable install (which points at a different repo checkout) or any file
outside this package's own allowlist. Scoped to tests/pit_capture/ only.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[2] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
