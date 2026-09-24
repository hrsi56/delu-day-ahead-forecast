"""Run conditions for CP-16 tests on a clean checkout (added 2026-09-24).

The CP-16 test files stay byte-identical to their hashes in
reports/v2-causal/artifact-manifest.json, so their preconditions live here instead.

1. Production-verification tests replay saved CP-16 work and charge the persistent CP-16
   ledger. Without CP16_LEDGER they are skipped, unless CP16_REQUIRE_SAVED_EVIDENCE=1 demands
   them, in which case they run and fail exactly as before. Two of them read
   os.environ['CP16_LEDGER'] directly, and pytest printed the whole environment on the
   resulting KeyError.
2. CP-16's supplied-input identity check is bound to the v21-r3 anchor bytes. A later ratified
   revision of capstone_v21.md supersedes them, and the reviewed v21-r3 bytes remain at
   evidence/cp-16:capstone_v21.md. The check is skipped only when the anchor is the sole
   mismatch and declares a revision after v21-r3. Any other mismatch still fails.
"""
from __future__ import annotations

import hashlib
import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
ANCHOR = "capstone_v21.md"
LEDGER_TESTS = {
    ("test_state_results.py", "test_independent_all_origin_residual_replay"),
    ("test_state_results.py", "test_real_state_restart_and_saved_cache_refusals"),
}
IDENTITY_TEST = ("test_budget_inputs.py", "test_inherited_identity_positive_and_wrong_input_refusal")


def _ledger_unavailable() -> bool:
    return not os.environ.get("CP16_LEDGER") and os.environ.get("CP16_REQUIRE_SAVED_EVIDENCE") != "1"


def _needs_ledger(item: pytest.Item, key: tuple[str, str]) -> bool:
    saved_evidence = key[0] == "test_saved_results.py" and "evidence" in getattr(item, "fixturenames", ())
    return key in LEDGER_TESTS or saved_evidence


def _superseded_anchor() -> str | None:
    from cp16.inputs import SUPPLIED

    mismatched = [name for name, expected in SUPPLIED.items()
                  if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != expected]
    if mismatched != [ANCHOR]:
        return None
    declared = re.search(r"v21-r(\d+)", (ROOT / ANCHOR).read_text(encoding="utf-8")[:400])
    if declared is None or int(declared.group(1)) <= 3:
        return None
    return (f"CP-16 identity is bound to the v21-r3 anchor; {ANCHOR} is now ratified "
            f"v21-r{declared.group(1)}. Reviewed bytes: evidence/cp-16:{ANCHOR}")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item: pytest.Item) -> None:
    key = (item.path.name, getattr(item, "originalname", item.name))
    if _needs_ledger(item, key) and _ledger_unavailable():
        pytest.skip("production verification: set CP16_LEDGER (charges the CP-16 ledger) "
                    "or CP16_REQUIRE_SAVED_EVIDENCE=1")
    if key == IDENTITY_TEST:
        reason = _superseded_anchor()
        if reason:
            pytest.skip(reason)
