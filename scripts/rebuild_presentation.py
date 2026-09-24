#!/usr/bin/env python3
"""Rebuild every presentation surface from the committed evidence (presentation plan §7.2, "Reproduce").

No fit, no download and no network: the page, the README's research and CP-3 blocks, both Space
cards, the browser's claim file (when the payload exists) and the MLflow export are regenerated
from committed files, then the cross-surface agreement and zero-fetch checks run.

    uv run python scripts/rebuild_presentation.py
    uv run python scripts/rebuild_presentation.py --measure    # also record the runtime

`--measure` writes `reports/presentation/release-checks/<date>-rebuild.json`, which the page reads
to state how long the rebuild took, on which machine and when. A normal run never changes it, so
the page does not change with every rebuild.
"""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

STEPS: tuple[tuple[str, list[str]], ...] = (
    ("README research block", ["scripts/readme_research.py"]),
    ("README CP-3 section", ["scripts/cp3_readme.py"]),
    ("MLflow export", ["scripts/mlflow_export.py"]),
    ("static page", ["scripts/build_pages.py"]),
    ("cross-surface agreement and zero-fetch checks", ["scripts/verify_release.py"]),
)


def cards() -> None:
    """Both Space cards, from the claim set. Only the card writers run: the container bundle and
    the WASM export are separate, heavier builds (`make space`, `make wasm`)."""
    import json as _json

    from build_space import CARD as SPACE_CARD
    from build_space import build_card as space_card
    from build_wasm_space import CARD as WASM_CARD
    from build_wasm_space import PUBLIC
    from build_wasm_space import build_card as wasm_card
    from delu_forecast.claims import build_claims

    SPACE_CARD.write_text(space_card())
    WASM_CARD.write_text(wasm_card())
    if PUBLIC.exists():
        (PUBLIC / "claims.json").write_text(
            _json.dumps(dict(build_claims().values), indent=1, sort_keys=True) + "\n"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--measure", action="store_true", help="record the runtime as a release check")
    args = parser.parse_args()
    timings = {}
    started = time.monotonic()
    step_start = time.monotonic()
    cards()
    timings["Space cards"] = round(time.monotonic() - step_start, 1)
    for name, command in STEPS:
        step_start = time.monotonic()
        result = subprocess.run([sys.executable, *command], cwd=ROOT, capture_output=True, text=True,
                                env={**__import__("os").environ, "MLFLOW_DISABLE_AGENT_HINT": "1"})
        timings[name] = round(time.monotonic() - step_start, 1)
        if result.returncode != 0:
            print(result.stdout[-2000:], result.stderr[-2000:], sep="\n")
            print(f"FAILED: {name}")
            return 1
        print(f"{name}: ok ({timings[name]} s)")
    total = round(time.monotonic() - started, 1)
    print(f"rebuilt every presentation surface in {total} s")
    if args.measure:
        record = {
            "check": "rebuild every presentation surface from committed evidence",
            "command": "uv run python scripts/rebuild_presentation.py",
            "date": date.today().isoformat(),
            "machine": f"{platform.system()} {platform.machine()}, Python {platform.python_version()}",
            "seconds": total,
            "steps_seconds": timings,
        }
        out = ROOT / "reports" / "presentation" / "release-checks" / f"{record['date']}-rebuild.json"
        out.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
