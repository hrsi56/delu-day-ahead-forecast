#!/usr/bin/env python3
"""Print the CP-3 release verification, and exit non-zero if it does not hold.

Three things, in the form the checkpoint asks for them:

1. **Item 5** as a table -- surface by surface and claim by claim, with the four
   cutoffs shown separately -- not as a sentence saying it agrees.
2. **Item 3** as a dependency-closure scan of the built static page.
3. **Link discipline**: no surface may link a gated DagsHub UI path.

`make verify`. The same properties are asserted by tests 17, 19 and 20; this is
the human-readable rendering of them.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from delu_forecast.claims import build_claims  # noqa: E402
from delu_forecast.static_audit import audit_html  # noqa: E402
from delu_forecast.surfaces import (  # noqa: E402
    CUTOFF_KEYS,
    PAGES_PATH,
    agreement_matrix,
    disagreements,
    link_discipline_failures,
    load_surfaces,
    render_matrix,
)


def main() -> int:
    claims = build_claims()
    surfaces = load_surfaces()
    failures: list[str] = []

    print("## Item 5 — cross-surface agreement\n")
    print(render_matrix(agreement_matrix(surfaces)))
    print()
    print("### The four cutoffs, separately\n")
    print(
        render_matrix(agreement_matrix(surfaces, CUTOFF_KEYS)).replace(
            "| Claim |", "| Cutoff |"
        )
    )
    print()
    for key in CUTOFF_KEYS:
        print(f"- `{key}` = `{claims[key]}`")
    problems = disagreements(surfaces)
    failures += problems
    print(f"\ndisagreements: {problems or 'none'}")

    print("\n## Item 3 — zero runtime calls\n")
    findings = audit_html(PAGES_PATH.read_text())
    failures += [str(finding) for finding in findings]
    print(f"scanned {PAGES_PATH.relative_to(ROOT)} ({PAGES_PATH.stat().st_size:,} bytes)")
    print(f"fetching references to an external origin: {len(findings)}")
    for finding in findings:
        print(f"  - {finding}")

    print("\n## Link discipline\n")
    link_failures = link_discipline_failures(surfaces)
    failures += link_failures
    print(f"gated DagsHub UI links on any surface: {link_failures or 'none'}")
    print(f"tracking URI used everywhere: {claims['mlflow_url']}")

    print()
    if failures:
        print(f"FAIL — {len(failures)} problem(s)")
        return 1
    print("PASS — every bound claim agrees on every surface; the static page fetches nothing")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
