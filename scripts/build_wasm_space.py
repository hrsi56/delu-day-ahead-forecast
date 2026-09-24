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

**This is a Static Space. It executes nothing on Hugging Face's side**, so it cannot sleep: there is
no process to put to sleep. {C['wasm_what_runs_live']} The champion's nine LightGBM boosters run in
Pyodide.

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
- §5.2 holds on the browser path too. {C['wasm_availability_statement']}

### What a first visit costs

{C['wasm_cold_load']} Measured on a cold cache against the way Hugging Face actually serves a
Static Space — files uncompressed, binary files through a redirect to `us.aws.cdn.hf.co`:
{C['wasm_cold_load_bytes']}. Most of it is the Python runtime and its scientific wheels from
`cdn.jsdelivr.net`. The nine boosters come from this Space itself as base64-encoded gzip: the
platform does not compress, and it would serve a binary file through an uncacheable redirect, so
the model ships as compressed text instead. The page prints its own measured download table at the
bottom.

{C['wasm_wrapper_disclosure']}

If you want the report without any download, the [static report]({C['pages_url']}) fetches nothing
at all.
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


# -- demo states (presentation plan §7.11, invariant 25) ----------------------
#
# The exported page shows nothing until marimo's JavaScript has loaded, so a slow or failed start
# looked like a blank page (Phase 0 finding P0-1). These states are static HTML placed before the
# runtime: visible at once, and still visible if initialization fails. The script shows only real
# events -- the forecast panel appearing, a script or stylesheet failing to load, or a generous
# deadline passing with neither -- and never an invented percentage or a timer as progress.

#: Text the notebook renders only after the champion has run in the browser.
READY_MARKER = "Maximum absolute deviation"
DEADLINE_SECONDS = 240


def startup_css() -> str:
    return """
.delu-status{font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#18181B;margin:16px auto;max-width:760px;padding:0 16px}
.delu-card{background:#FFFFFF;border:1px solid #E4E4E7;border-left:4px solid #475569;border-radius:10px;padding:14px 18px}
.delu-title{font-weight:650;margin:0 0 6px}
.delu-body{margin:0 0 10px}
.delu-actions{margin:0;display:flex;flex-wrap:wrap;gap:8px 18px;align-items:center}
.delu-actions a{color:#1D4ED8;min-height:44px;display:inline-flex;align-items:center}
.delu-actions button{min-height:44px;padding:0 18px;border-radius:10px;border:0;background:#18181B;color:#fff;font:inherit;font-weight:650;cursor:pointer}
.delu-actions button:focus-visible,.delu-actions a:focus-visible{outline:2px solid #1D4ED8;outline-offset:2px}
.delu-status [data-show]{display:none}
.delu-status[data-state=loading] [data-show~=loading],.delu-status[data-state=failure] [data-show~=failure],
.delu-status[data-state=retrying] [data-show~=retrying],.delu-status[data-state=ready] [data-show~=ready]{display:block}
.delu-status[data-state=failure] .delu-card{border-left-color:#18181B}
.delu-status[data-state=ready] .delu-card{padding:8px 14px}
"""


def startup_markup(C, state: str = "loading") -> str:
    report = C["pages_url"]
    return f"""<div id="delu-status" class="delu-status" data-state="{state}" role="status" aria-live="polite">
 <div class="delu-card">
  <p class="delu-title" data-show="loading">Starting the v1 demo</p>
  <p class="delu-body" data-show="loading">Forecast calculations run locally in your browser. The first visit
   downloads about {C['wasm_cold_load_mb']} MB, a Python runtime and the model, so it can take a minute or more.</p>
  <p class="delu-title" data-show="failure">The demo did not start</p>
  <p class="delu-body" data-show="failure">A file it needs did not load, or it has not finished starting after
   several minutes. A slow or filtered connection, or a browser that blocks the runtime, can cause this. You can view
   the saved forecast and research results in the report without loading the model.</p>
  <p class="delu-title" data-show="retrying">Retrying</p>
  <p class="delu-body" data-show="retrying">Reloading the demo.</p>
  <p class="delu-body" data-show="ready">The v1 demo is running in your browser.</p>
  <p class="delu-actions"><button type="button" id="delu-retry" data-show="failure">Retry</button>
   <a href="{report}">Read the instant report instead</a></p>
 </div>
</div>"""


def startup_js() -> str:
    return """
(function(){
 var box=document.getElementById('delu-status');if(!box){return;}
 var started=Date.now(),done=false;
 function set(state){box.setAttribute('data-state',state);}
 function ready(){return (document.body.innerText||'').indexOf('%s')>=0;}
 var timer=setInterval(function(){
  if(ready()){set('ready');done=true;clearInterval(timer);}
  else if(Date.now()-started>%d*1000){set('failure');clearInterval(timer);}
 },1000);
 window.addEventListener('error',function(e){
  var t=e.target;if(!done&&t&&(t.tagName==='SCRIPT'||t.tagName==='LINK')){set('failure');}
 },true);
 document.getElementById('delu-retry').addEventListener('click',function(){set('retrying');location.reload();});
})();
""" % (READY_MARKER, DEADLINE_SECONDS)


def demo_states_specimen() -> str:
    """The four states side by side, for the D1 review. The same markup the Space build injects."""
    C = build_claims()
    sections = []
    for state, label in (("loading", "Loading (static HTML, before any script runs)"),
                         ("failure", "Failure, with retry"), ("retrying", "Retrying"),
                         ("ready", "Ready (a slim bar above the running demo)")):
        markup = startup_markup(C, state).replace('id="delu-status" ', "").replace('id="delu-retry" ', "")
        sections.append(
            '<section><h2 style="font:600 14px system-ui;color:#52525B;text-transform:uppercase;'
            f'letter-spacing:.05em;margin:24px 16px 0">{label}</h2>{markup}</section>'
        )
    intro = (
        "Specimen of the Space's startup states (plan §7.11). The loading state is static HTML, so it is visible "
        "before the runtime starts and stays visible if initialization fails. No percentage and no timer are "
        "shown as progress."
    )
    return (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><title>PRES-1 D1 demo states</title>'
        f"<style>body{{margin:0;background:#FAFAFA}}{startup_css()}</style></head><body>"
        f'<p style="font:15px system-ui;max-width:760px;margin:24px auto;padding:0 16px">{intro}</p>'
        + "".join(sections) + "</body></html>"
    )


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

    # The claim set depends on reports/cp3b/equivalence.json, which the gate
    # rewrites after the payload is built. Refresh the page's copy here, last, so
    # the exported page can never render claims older than the evidence behind them.
    (PUBLIC / "claims.json").write_text(
        json.dumps(dict(build_claims().values), indent=1, sort_keys=True) + "\n"
    )

    CARD.parent.mkdir(parents=True, exist_ok=True)
    CARD.write_text(build_card())
    print(f"wrote {CARD}")

    run_export()
    removed = []
    for entry in sorted(BUNDLE.iterdir()):
        if entry.name not in ALLOWED_ROOT:
            removed.append(entry.name)
            shutil.rmtree(entry) if entry.is_dir() else entry.unlink()
    # Nested, not just the root: `public/` is copied wholesale by the export, so
    # bytecode written by any host-side import of the shipped module travels too.
    for cache in list(BUNDLE.rglob("__pycache__")):
        removed.append(str(cache.relative_to(BUNDLE)))
        shutil.rmtree(cache)
    for compiled in list(BUNDLE.rglob("*.pyc")):
        removed.append(str(compiled.relative_to(BUNDLE)))
        compiled.unlink()
    shutil.copy2(CARD, BUNDLE / "README.md")
    (BUNDLE / ".gitattributes").write_text(GITATTRIBUTES)

    # -- structural checks: fail the build, not the visitor ---------------
    problems = []
    if not (BUNDLE / "index.html").is_file():
        problems.append("index.html missing")
    if not (BUNDLE / "assets").is_dir() or not any((BUNDLE / "assets").iterdir()):
        problems.append("assets/ missing or empty")
    boosters = sorted((BUNDLE / "public" / "boosters").glob("*.txt.gz.b64"))
    if len(boosters) != 9:
        problems.append(f"expected 9 boosters, found {len(boosters)}")
    shipped = BUNDLE / "public" / "browser_champion.py"
    source = ROOT / "app" / "browser_champion.py"
    module_sha = hashlib.sha256(shipped.read_bytes()).hexdigest() if shipped.exists() else None
    if module_sha != hashlib.sha256(source.read_bytes()).hexdigest():
        problems.append("public/browser_champion.py differs from app/browser_champion.py")
    # Anything binary under public/ would be stored through Xet and served as a
    # no-store redirect to a signed, per-request URL -- uncacheable, and an extra
    # host. The payload must stay text.
    for payload_file in (BUNDLE / "public").rglob("*"):
        if payload_file.is_file():
            head = payload_file.read_bytes()[:8192]
            try:
                head.decode("utf-8")
                binary = b"\x00" in head
            except UnicodeDecodeError:
                binary = True
            if binary:
                problems.append(f"binary payload file would be redirected through Xet: {payload_file.relative_to(BUNDLE)}")
    if any(p.suffix == ".pyc" or "__pycache__" in p.parts for p in BUNDLE.rglob("*")):
        problems.append("compiled bytecode present in the bundle")
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
