#!/usr/bin/env python3
"""The publication lint (Publication Standard v1 §4, §5): rule families over the reading path.

It reads the built page and the README's generated top block the way a reader receives them --
the reading path is the rendered page minus the bodies of closed disclosures and the value tables,
counting only the desktop variant of each chart -- and the template sources the generators write
from. The families:

* **codes** -- checkpoint codes, claim IDs, section references, underscore identifiers and every
  experiment code in the registry (a generated denylist, never a hand-kept list);
* **precision** -- every numeral bound to a record, shown in its unit's precision, one precision
  per chart, a value near zero keeping its sign;
* **percentages** -- a `%` only as a derived relative change, a structural level or an exempt v1
  statement;
* **status words** -- over the template sources: "current", "latest", "still", "now", "the demo
  runs" and their synonyms reach a surface only through a registry token.

    uv run python scripts/lint_publication.py        # exit 1 on any finding

`tests/test_37_publication_lint.py` runs it in CI, with a negative control for each family.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from delu_forecast import publication_lint as L  # noqa: E402

PAGE = ROOT / "docs" / "index.html"


def run() -> dict[str, list[str]]:
    import readme_research

    return L.lint(ROOT, PAGE.read_text(), readme_research.build_glance("html"))


def main() -> int:
    results = run()
    total = 0
    for surface, findings in results.items():
        print(f"{surface}: {len(findings)} finding(s)")
        for finding in findings:
            print(f"  - {finding}")
        total += len(findings)
    print("PASS — the reading path and the template sources meet the standard's §4 and §5 rules" if not total
          else f"FAIL — {total} finding(s)")
    return 0 if not total else 1


if __name__ == "__main__":
    raise SystemExit(main())
