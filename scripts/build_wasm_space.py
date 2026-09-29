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
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from build_space import card_body, missing_card_lines, model_line  # noqa: E402

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

#: marimo copies every stylesheet the page links into each widget's shadow root, as a constructed
#: stylesheet built from the rules' text (`copyStyles` in its frontend). A constructed stylesheet
#: resolves relative URLs against the page, not against `assets/`, so WebKit -- which honours
#: `@font-face` inside a shadow root, unlike Chrome -- asked the bundle's root for three fonts that
#: exist only under `assets/`, and got 404 (the Phase 0 and 2026-09-28 demo records). Every target
#: a linked stylesheet names is therefore also shipped at the root (brief W12). Nothing is edited.
_LINK = re.compile(r"<link\b[^>]*>")
_ATTR = re.compile(r'\b(rel|href)="([^"]*)"')
_LOCAL_REF = re.compile(r'\b(?:href|src)="(?!https?:|data:|blob:|mailto:|#|//)([^"]+)"')
_CSS_URL = re.compile(r"""url\(\s*['"]?(?!data:|https?:|blob:|#|/)([^'")]+?)['"]?\s*\)""")


def _local(ref: str) -> str:
    return ref.split("#", 1)[0].split("?", 1)[0]


def linked_stylesheets(page: str) -> list[str]:
    """The stylesheets the page links, in order."""
    sheets = []
    for tag in _LINK.findall(page):
        attrs = dict(_ATTR.findall(tag))
        if "stylesheet" in attrs.get("rel", "").split() and attrs.get("href"):
            sheets.append(_local(attrs["href"]))
    return list(dict.fromkeys(sheets))


def stylesheet_references(bundle: Path) -> list[tuple[str, str]]:
    """(stylesheet, relative URL) for every `url()` in a stylesheet the page links."""
    page = (bundle / "index.html").read_text()
    out = []
    for sheet in linked_stylesheets(page):
        path = bundle / sheet
        if path.is_file():
            out += [(sheet, _local(ref)) for ref in dict.fromkeys(_CSS_URL.findall(path.read_text()))]
    return out


def ship_shadow_root_targets(bundle: Path) -> list[str]:
    """Copy each target a linked stylesheet names to where a shadow-root copy of it resolves."""
    shipped = []
    for sheet, ref in stylesheet_references(bundle):
        source = ((bundle / sheet).parent / ref).resolve()
        target = (bundle / ref).resolve()
        if source.is_file() and target.is_relative_to(bundle.resolve()) and not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            shipped.append(str(target.relative_to(bundle.resolve())))
    return sorted(shipped)


def referenced_asset_problems(bundle: Path) -> tuple[int, list[str]]:
    """Every asset the page's HTML and its linked stylesheets reference exists in the bundle; a
    stylesheet's `url()` is resolved against the stylesheet and against the page (its shadow-root
    copies). Returns how many references were checked, and what is missing."""
    page = (bundle / "index.html").read_text()
    root = bundle.resolve()
    checked, problems = 0, []
    for ref in dict.fromkeys(_local(ref) for ref in _LOCAL_REF.findall(page)):
        checked += 1
        if not (root / ref).resolve().is_file():
            problems.append(f"index.html references {ref}, which the bundle lacks")
    for sheet, ref in stylesheet_references(bundle):
        for base, where in (((root / sheet).parent, "beside the stylesheet"), (root, "at the root, for its shadow-root copies")):
            checked += 1
            if not (base / ref).resolve().is_file():
                problems.append(f"{sheet} references {ref}, which the bundle lacks {where}")
    return checked, problems


def bundle_sha256(bundle: Path) -> str:
    """One hash for the whole bundle: SHA-256 over `<file sha256>  <path>` lines, sorted by path --
    the form `shasum -a 256` prints, so anyone can recompute it from a checkout of the Space."""
    paths = sorted((p.relative_to(bundle).as_posix() for p in bundle.rglob("*") if p.is_file()), key=str.encode)
    lines = [f"{hashlib.sha256((bundle / path).read_bytes()).hexdigest()}  {path}" for path in paths]
    return hashlib.sha256(("\n".join(lines) + "\n").encode()).hexdigest()


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
    return f"""## What is deployed — and why it is the evaluated model

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

The [report]({C['pages_url']}) is a self-contained page with no additional runtime requests.
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

{model_line(C['pages_url'])}

Probabilistic forecasts of the next delivery day's hourly German–Luxembourg day-ahead
electricity price, with calibrated 50 / 80 / 95 % prediction intervals from a LightGBM
nine-quantile ensemble, CQR-calibrated with isotonic monotonicity last.

**The static report is the primary entry point: [{C['pages_url']}]({C['pages_url']}).**
It is a self-contained page with no additional runtime requests. This Space is the interactive deep dive it
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
#: Text marimo's error boundary renders when its runtime fails (for example, Pyodide cannot load):
#: the runtime has reported the failure, so the page says so at once instead of at the deadline.
FAILURE_MARKER = "Something went wrong"
DEADLINE_SECONDS = 240


def startup_css() -> str:
    return """
.delu-status{font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:#18181B;position:fixed;top:0;left:0;right:0;
 z-index:2147483000;margin:0 auto;max-width:760px;padding:12px 16px;box-sizing:border-box}
.delu-card{background:#FFFFFF;border:1px solid #E4E4E7;border-left:4px solid #475569;border-radius:10px;padding:14px 18px;
 box-shadow:0 4px 18px rgba(24,24,27,.12)}
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
/* Ready: the notebook covers the viewport and opens with its own link to the report, so the card
   closes; its text stays in the live region, so a screen reader still hears that the demo is ready. */
.delu-status[data-state=ready]{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;
 clip-path:inset(50%);white-space:nowrap}
.delu-status[data-state=ready] .delu-actions{display:none}
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
   <a href="{report}">View the report</a></p>
 </div>
</div>"""


def startup_js() -> str:
    return """
(function(){
 var box=document.getElementById('delu-status');if(!box){return;}
 var started=Date.now(),done=false;
 function set(state){box.setAttribute('data-state',state);}
 function has(text){return (document.body.innerText||'').indexOf(text)>=0;}
 var timer=setInterval(function(){
  if(has('%s')){set('ready');done=true;clearInterval(timer);}
  else if(has('%s')||Date.now()-started>%d*1000){set('failure');clearInterval(timer);}
 },1000);
 window.addEventListener('error',function(e){
  var t=e.target;if(!done&&t&&(t.tagName==='SCRIPT'||t.tagName==='LINK')){set('failure');}
 },true);
 document.getElementById('delu-retry').addEventListener('click',function(){set('retrying');location.reload();});
})();
""" % (READY_MARKER, FAILURE_MARKER, DEADLINE_SECONDS)


STARTUP_BEGIN = "<!-- delu-startup:start -->"
STARTUP_END = "<!-- delu-startup:end -->"

# -- the framework's controls: names and target sizes (review F01; PUBLISH_RULES 1.0 §7.1, §9) -----------------
#
# marimo renders each widget in an open shadow root. Its slider's visible label points (`<label for>`) at the slider
# root, not at the thumb that carries role="slider", so the thumb had no accessible name; its radio group is named
# only "Radio Group"; and the notebook menu is an icon button with no name and a 31 x 25 px target. The repair names
# each control from its own visible label, inside the same shadow root, names the menu for what it opens, and sizes
# the hit areas to about 44 px. It changes no widget, value, payload or computation.

A11Y_BEGIN = "<!-- delu-a11y:start -->"
A11Y_END = "<!-- delu-a11y:end -->"
#: The notebook menu's name: what the button opens.
MENU_NAME = "Notebook menu"

#: Inside every widget's shadow root: about 44 px targets for the slider track, the radio labels and the accordion
#: triggers. Visual sizes of marks stay close to marimo's own.
A11Y_SHADOW_CSS = (
    'span[dir][data-orientation="horizontal"][id]{min-height:44px}'
    '[role="slider"]{width:22px;height:22px}'
    '[role="radiogroup"] label{display:inline-flex;align-items:center;min-height:44px;padding:0 12px 0 6px;cursor:pointer}'
    '[role="radiogroup"] [role="radio"]{width:20px;height:20px}'
    'button[aria-controls][aria-expanded]{min-height:44px}'
)
#: In the page itself: the notebook menu's and the framework credit link's hit areas.
A11Y_PAGE_CSS = ('[data-testid="notebook-actions-dropdown"]>button{min-width:44px;min-height:44px}'
                 'a[href*="marimo-team/marimo"]{display:inline-flex;align-items:center;min-height:44px}')


def a11y_js() -> str:
    return """
(function(){
 var css=%s,menuName=%s,sheet=null;
 try{sheet=new CSSStyleSheet();sheet.replaceSync(css);}catch(e){sheet=null;}
 function labelFor(root,node){
  // The widget's own visible label: the one pointing at this control's root, or the widget's label part.
  var owner=node.closest('[id]');
  var lab=owner?root.querySelector('label[for="'+owner.id+'"]'):null;
  if(!lab){var part=root.querySelector('[part="label"] label');lab=part||null;}
  if(!lab||!(lab.textContent||'').trim()){return null;}
  if(!lab.id){lab.id=(owner&&owner.id?owner.id:'delu')+'-name';}
  return lab.id;
 }
 function fix(root){
  Array.prototype.forEach.call(root.querySelectorAll('[role="slider"]:not([aria-labelledby])'),function(el){
   var id=labelFor(root,el);if(id){el.setAttribute('aria-labelledby',id);}
  });
  Array.prototype.forEach.call(root.querySelectorAll('[role="radiogroup"]:not([aria-labelledby])'),function(el){
   var id=labelFor(root,el);if(id){el.setAttribute('aria-labelledby',id);}
  });
  if(sheet&&root.adoptedStyleSheets&&root.adoptedStyleSheets.indexOf(sheet)<0){
   root.adoptedStyleSheets=root.adoptedStyleSheets.concat([sheet]);
  }
 }
 var watched=[];
 function sweep(){
  var menu=document.querySelector('[data-testid="notebook-actions-dropdown"] button[aria-haspopup="menu"]');
  if(menu&&!menu.getAttribute('aria-label')){menu.setAttribute('aria-label',menuName);}
  Array.prototype.forEach.call(document.querySelectorAll('*'),function(el){
   if(!el.shadowRoot||el.tagName.indexOf('MARIMO-')!==0){return;}
   fix(el.shadowRoot);
   if(watched.indexOf(el.shadowRoot)<0){
    watched.push(el.shadowRoot);
    new MutationObserver(later).observe(el.shadowRoot,{childList:true,subtree:true});
   }
  });
 }
 var pending=null;
 function later(){if(pending===null){pending=setTimeout(function(){pending=null;sweep();},120);}}
 new MutationObserver(later).observe(document.documentElement,{childList:true,subtree:true});
 later();
})();
""" % (json.dumps(A11Y_SHADOW_CSS), json.dumps(MENU_NAME))


def inject_a11y(html: str) -> str:
    """Put the control repair into the exported page: one stylesheet and one small script at the end of the body."""
    if A11Y_BEGIN in html:
        raise ValueError("the control repair is already in this page")
    close = html.rfind("</body>")
    if close < 0:
        raise ValueError("the export has no </body> to inject into")
    block = f"{A11Y_BEGIN}<style>{A11Y_PAGE_CSS}</style><script>{a11y_js()}</script>{A11Y_END}"
    return html[:close] + block + html[close:]


def a11y_findings(html: str) -> list[str]:
    """What the built page must carry for the control repair; empty when it does (the build and test_23)."""
    if html.count(A11Y_BEGIN) != 1 or html.count(A11Y_END) != 1:
        return ["the control repair is missing or injected twice"]
    block = html[html.index(A11Y_BEGIN):html.index(A11Y_END)]
    problems = []
    for needle, what in (('[role="slider"]', "no slider naming"), ('[role="radiogroup"]', "no radio-group naming"),
                         ("aria-labelledby", "no label reference"), (json.dumps(MENU_NAME), "no menu name"),
                         ("notebook-actions-dropdown", "no menu target sizing"), ("min-height:44px", "no 44 px targets")):
        if needle not in block:
            problems.append(what)
    if re.search(r"\bfetch\(|XMLHttpRequest|import\(", block):
        problems.append("the repair makes a request")
    return problems


def inject_startup(html: str, C) -> str:
    """Put the demo states into the exported page as static HTML (plan §7.11, invariant 25).

    The block opens the body, so the loading message paints before marimo's module scripts run,
    and it stays in place if they never do. The model, its payload and the equivalence gate are
    untouched: this adds markup, a stylesheet and one small inline script."""
    if STARTUP_BEGIN in html:
        raise ValueError("the startup states are already in this page")
    head_close = html.find("</head>")
    if head_close < 0 or not re.search(r"<body[^>]*>", html):
        raise ValueError("the export has no <head>/<body> to inject into")
    html = html[:head_close] + f"<style>{startup_css()}</style>" + html[head_close:]
    body = re.search(r"<body[^>]*>", html)
    block = f"{STARTUP_BEGIN}{startup_markup(C)}<script>{startup_js()}</script>{STARTUP_END}"
    return html[:body.end()] + block + html[body.end():]


def startup_findings(html: str, C) -> list[str]:
    """What the built page must carry; empty when it does. Used by the build and by test_23."""
    problems = []
    if html.count(STARTUP_BEGIN) != 1 or html.count(STARTUP_END) != 1:
        return ["the startup states are missing or injected twice"]
    block = html[html.index(STARTUP_BEGIN):html.index(STARTUP_END)]
    body = re.search(r"<body[^>]*>", html)
    if not body or html.index(STARTUP_BEGIN) != body.end():
        problems.append("the startup states do not open the body")
    if 'data-state="loading"' not in block:
        problems.append("the static state is not the loading state")
    for state in ("loading", "failure", "retrying", "ready"):
        if f'data-show="{state}"' not in block:
            problems.append(f"no {state} state")
    if 'id="delu-retry"' not in block:
        problems.append("no retry control")
    if f'href="{C["pages_url"]}"' not in block:
        problems.append("no route back to the report")
    if READY_MARKER not in block:
        problems.append("the ready check does not look for the forecast panel")
    if FAILURE_MARKER not in block:
        problems.append("the failure check does not listen for the runtime's own error")
    if re.search(r"\d\s?%", re.sub(r"<script>.*?</script>", "", block, flags=re.S)):
        problems.append("a percentage appears in the states (no invented progress)")
    return problems


def demo_states_specimen() -> str:
    """The four states side by side, for the D1 review. The same markup the Space build injects."""
    C = build_claims()
    sections = []
    for state, label in (("loading", "Loading (static HTML, before any script runs; pinned to the top of the window)"),
                         ("failure", "Failure, with retry"), ("retrying", "Retrying")):
        markup = startup_markup(C, state).replace('id="delu-status" ', "").replace('id="delu-retry" ', "")
        sections.append(
            '<section><h2 style="font:600 14px system-ui;color:#52525B;text-transform:uppercase;'
            f'letter-spacing:.05em;margin:24px 16px 0">{label}</h2>{markup}</section>'
        )
    intro = (
        "Specimen of the Space's startup states (plan §7.11). The loading state is static HTML, so it is visible "
        "before the runtime starts and stays visible if initialization fails. No percentage and no timer are "
        "shown as progress. Ready: the card closes, and the notebook opens with its own link to the report; "
        "screen readers hear \u201cThe v1 demo is running in your browser.\u201d"
    )
    return (
        '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" '
        'content="width=device-width,initial-scale=1"><title>PRES-1 D1 demo states</title>'
        f"<style>body{{margin:0;background:#FAFAFA}}{startup_css()}"
        ".delu-status{position:static;margin:16px auto}</style></head><body>"
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

    card = build_card()
    missing = missing_card_lines(card, build_claims()["pages_url"])
    if missing:
        raise SystemExit(f"the card lacks the registry's required lines: {missing}")
    CARD.parent.mkdir(parents=True, exist_ok=True)
    CARD.write_text(card)
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
    shipped_at_root = ship_shadow_root_targets(BUNDLE) if (BUNDLE / "index.html").is_file() else []
    C = build_claims()
    index = BUNDLE / "index.html"
    if index.is_file():
        index.write_text(inject_a11y(inject_startup(index.read_text(), C)))

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
    startup = startup_findings(index.read_text(), C) if index.is_file() else ["index.html missing"]
    problems.extend(f"startup states: {finding}" for finding in startup)
    repair = a11y_findings(index.read_text()) if index.is_file() else ["index.html missing"]
    problems.extend(f"control names and targets: {finding}" for finding in repair)
    references_checked, missing = referenced_asset_problems(BUNDLE) if index.is_file() else (0, [])
    problems.extend(f"referenced assets: {problem}" for problem in missing)
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
                "index_html_sha256": hashlib.sha256(index.read_bytes()).hexdigest() if index.is_file() else None,
                "bundle_sha256": bundle_sha256(BUNDLE),
                "bundle_sha256_method": "SHA-256 of the sorted `<sha256>  <path>` lines of every file in the bundle",
                "startup_states": {
                    "injected": index.is_file() and not startup,
                    "states": ["loading", "failure", "retrying", "ready"],
                    "ready_marker": READY_MARKER,
                    "deadline_seconds": DEADLINE_SECONDS,
                    "report_url": C["pages_url"],
                },
                "control_repair": {"injected": index.is_file() and not repair, "menu_name": MENU_NAME,
                                   "shadow_css": A11Y_SHADOW_CSS, "page_css": A11Y_PAGE_CSS},
                "removed_from_export_root": removed,
                "referenced_assets": {"checked": references_checked, "missing": missing,
                                      "shipped_at_root_for_shadow_roots": shipped_at_root},
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
