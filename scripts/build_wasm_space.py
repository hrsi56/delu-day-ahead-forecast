#!/usr/bin/env python3
"""Assemble the Hugging Face **Static** Space from the WASM export (M3.5/CP-3B).

Three outputs:

* `space-wasm/README.md` -- the Static Space card, committed, rendered from the
  claim set. It is the Space-metadata surface the deployed demo actually carries.
* `dist/space-wasm/` -- `marimo export html-wasm` of `app/wasm_showcase.py` plus
  the payload, the card, and LFS rules. Gitignored: a build product.
* `reports/cp3b/space_wasm_bundle.json` -- what was assembled, with the hash of
  the browser module so the directory can be tied back to the verified bytes.

Deployment is owner-only. This script builds and checks; it pushes nothing.

    uv run python scripts/build_wasm_payload.py && uv run python scripts/build_wasm_space.py
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from build_space import card_body  # noqa: E402

from delu_forecast.claims import (  # noqa: E402
    build_claims,
    limitation_bullets,
    reproducibility_bullets,
)

NOTEBOOK = ROOT / "app" / "wasm_showcase.py"
PUBLIC = ROOT / "app" / "public"
BUNDLE = ROOT / "dist" / "space-wasm"
CARD = ROOT / "space-wasm" / "README.md"
MANIFEST = ROOT / "reports" / "cp3b" / "space_wasm_bundle.json"

#: What a Static Space needs at its root. marimo's export also copied a stray
#: governance file from the repository into the export on 2026-09-15; anything
#: not on this list is removed, so an internal document can never be published
#: by accident.
ALLOWED_ROOT = {
    "index.html", "assets", "public", "README.md", ".gitattributes", ".nojekyll",
    "favicon.ico", "favicon-16x16.png", "favicon-32x32.png", "apple-touch-icon.png",
    "android-chrome-192x192.png", "android-chrome-512x512.png", "logo.png",
    "manifest.json", "site.webmanifest",
}

#: The Hub stores binary files through LFS/Xet. Text -- the boosters, the JSON,
#: the JavaScript -- does not need it.
GITATTRIBUTES = """*.png filter=lfs diff=lfs merge=lfs -text
*.ico filter=lfs diff=lfs merge=lfs -text
*.woff2 filter=lfs diff=lfs merge=lfs -text
*.woff filter=lfs diff=lfs merge=lfs -text
*.ttf filter=lfs diff=lfs merge=lfs -text
*.wasm filter=lfs diff=lfs merge=lfs -text
"""


def static_deployed_section(C) -> str:
    return f"""## What is deployed — and why it is still the evaluated model

**This is a Static Space. It executes nothing on Hugging Face's side**: every number on the page
is computed in your browser, by Pyodide, from the champion's own nine LightGBM boosters. A Static
Space cannot sleep, because there is no process to put to sleep.

{C['wasm_identity']}

That comparison is not a claim printed from a file — **the page runs it in front of you** and
reports the result, against outputs recorded from the frozen `mlflow.pyfunc` champion before the
page existed. The boosters were trained with LightGBM on macOS ARM and execute here under a
WebAssembly build with OpenMP disabled; that the two agree bitwise was the first thing measured,
because it was the one result that could have made this page impossible.

- `artifact_fingerprint_sha256` `{C['champion_fingerprint']}` — the same value in
  `models/champion/champion_card.json`, the one-shot holdout report and the registered `champion`
  alias.
- The snapshot the fixture rows come from is pinned at `sha256` `{C['snapshot_sha256']}`.
- §5.2 holds on the browser path too: masking the delivery day's own prices changes the output by
  exactly 0.0, and mutating a D−1 price moves it by {C['wasm_d_minus_1_control']} EUR/MWh.

### What a first visit costs

{C['wasm_cold_load']} Measured on a cold cache: {C['wasm_cold_load_bytes']}. Most of it is the Python
runtime and its scientific wheels from `cdn.jsdelivr.net`; the nine boosters come from this Space
itself. The page prints its own measured download table at the bottom. If you want the report
without the download, the [static report]({C['pages_url']}) fetches nothing at all.
"""


def build_card() -> str:
    C = build_claims()
    limitations = "\n".join(f"- {bullet}" for bullet in limitation_bullets(C))
    reproduction = "\n".join(f"- {bullet}" for bullet in reproducibility_bullets(C))
    return f"""---
title: DE-LU Day-Ahead Price Forecasting
emoji: ⚡
colorFrom: blue
colorTo: indigo
sdk: static
app_file: index.html
pinned: false
short_description: DE-LU day-ahead price forecast, running in your browser
tags:
  - energy
  - time-series
  - probabilistic-forecasting
  - conformal-prediction
  - lightgbm
  - pyodide
---

# DE-LU day-ahead price forecasting — running in your browser

Probabilistic forecasts of the next delivery day's hourly German–Luxembourg day-ahead
electricity price, with calibrated 50 / 80 / 95 % prediction intervals from a LightGBM
nine-quantile ensemble, CQR-calibrated with isotonic monotonicity last.

**The static report is the primary entry point: [{C['pages_url']}]({C['pages_url']}).**
It is CDN-served and performs zero runtime calls. This Space is the interactive deep dive it
fronts: {C['space_link_label']}.

> **{C['replay_label']}**

Anything this Space renders over the holdout window {C['holdout_window']} is a replay of a frozen
model against a period it never trained on. It is never presented as a live forecast, and the page
makes no call to ENTSO-E, SMARD or any model registry: the rows it forecasts from ship with it.

{card_body(C, static_deployed_section(C), limitations, reproduction)}"""


def run_export() -> None:
    if BUNDLE.exists():
        shutil.rmtree(BUNDLE)
    env = {**os.environ, "MLFLOW_DISABLE_AGENT_HINT": "1"}
    subprocess.run(
        ["marimo", "export", "html-wasm", str(NOTEBOOK), "-o", str(BUNDLE), "--mode", "run"],
        cwd=ROOT, env=env, check=True, capture_output=True, text=True,
    )


def main() -> int:
    if not (PUBLIC / "fixture.json").exists():
        raise SystemExit("app/public/ is absent; run `make wasm-payload` first")

    CARD.parent.mkdir(parents=True, exist_ok=True)
    CARD.write_text(build_card())
    print(f"wrote {CARD}")

    run_export()
    removed = []
    for entry in sorted(BUNDLE.iterdir()):
        if entry.name not in ALLOWED_ROOT:
            removed.append(entry.name)
            shutil.rmtree(entry) if entry.is_dir() else entry.unlink()
    shutil.copy2(CARD, BUNDLE / "README.md")
    (BUNDLE / ".gitattributes").write_text(GITATTRIBUTES)

    # -- structural checks: fail the build, not the visitor ---------------
    problems = []
    if not (BUNDLE / "index.html").is_file():
        problems.append("index.html missing")
    if not (BUNDLE / "assets").is_dir() or not any((BUNDLE / "assets").iterdir()):
        problems.append("assets/ missing or empty")
    boosters = sorted((BUNDLE / "public" / "boosters").glob("*.txt"))
    if len(boosters) != 9:
        problems.append(f"expected 9 boosters, found {len(boosters)}")
    shipped = BUNDLE / "public" / "browser_champion.py"
    source = ROOT / "app" / "browser_champion.py"
    module_sha = hashlib.sha256(shipped.read_bytes()).hexdigest() if shipped.exists() else None
    if module_sha != hashlib.sha256(source.read_bytes()).hexdigest():
        problems.append("public/browser_champion.py differs from app/browser_champion.py")
    for leak in ("CLAUDE.md", "AGENTS.md", ".env"):
        if any(p.name == leak for p in BUNDLE.rglob("*")):
            problems.append(f"{leak} present in the bundle")
    front = (BUNDLE / "README.md").read_text().split("---", 2)[1]
    if "sdk: static" not in front:
        problems.append("the card does not declare sdk: static")

    files = [p for p in BUNDLE.rglob("*") if p.is_file()]
    total = sum(p.stat().st_size for p in files)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(
            {
                "bundle": str(BUNDLE.relative_to(ROOT)),
                "card": str(CARD.relative_to(ROOT)),
                "sdk": "static",
                "files": len(files),
                "asset_files": sum(1 for p in files if "assets" in p.relative_to(BUNDLE).parts),
                "total_bytes_uncompressed": total,
                "boosters": [p.name for p in boosters],
                "browser_champion_sha256": module_sha,
                "removed_from_export_root": removed,
                "problems": problems,
                "deployment": "owner-only; this script assembles and pushes nothing",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    print(f"assembled {BUNDLE}: {len(files)} files, {total:,} bytes uncompressed")
    if removed:
        print(f"removed from the export root (not part of the app): {removed}")
    print(f"wrote {MANIFEST}")
    if problems:
        print("PROBLEMS:\n  " + "\n  ".join(problems))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
