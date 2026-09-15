#!/usr/bin/env python3
"""Build the static GitHub Pages export -- the primary recruiter URL (§9.2, §10).

**Why this is not `marimo export html`.** §9.2 names that as the build path and
provides a fallback "if any §10 element degrades in static export". Measured on
2026-09-14 with marimo 0.24.2, the export is worse than degraded for this bar: it
emits 181 external references to `cdn.jsdelivr.net` -- the frontend JS bundle,
its CSS, and five web fonts -- so the page cannot render at all without network,
and CP-3 item 3 requires **zero runtime calls** to the Space or any external
service. The measurement is recorded in `reports/cp3/pages_build.json`; this
script is the plan's purpose-built fallback, assembled from the same committed
figures and the same claim set.

Everything the page needs is inlined: CSS in a `<style>` block, figures as
base64 `data:` URIs, the interactive fan chart's data as a JSON literal, and the
chart renderer as an inline `<script>`. No stylesheet link, no font, no script
src, no image src, no iframe, no beacon, no fetch. The two controls are served by
a **one-dimensional lookup** (§9.2): the nine quantiles are precomputed at each
load-scale point, and the level selector chooses which two of those nine to draw.

`tests/test_19_static_page_is_offline.py` asserts the property on the built file
and carries a positive control that reintroduces one CDN reference and requires
the scanner to catch it.
"""

from __future__ import annotations

import base64
import html
import json
import re
import sys
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from delu_forecast.claims import (  # noqa: E402
    build_claims,
    limitation_bullets,
    reproducibility_bullets,
)
from delu_forecast.postprocess import QUANTILE_LABELS  # noqa: E402
from delu_forecast.showcase import (  # noqa: E402
    INTERVAL_LEVELS,
    actuals_for_day,
    default_target_day,
    forecast_delivery_day,
    load_champion,
    load_snapshot,
)

OUTPUT = ROOT / "docs" / "index.html"
BUILD_RECORD = ROOT / "reports" / "cp3" / "pages_build.json"

#: One dimension, eleven points. The level selector is not a second dimension:
#: it reads two of the nine quantiles already stored at each point.
LOAD_SCALES: tuple[float, ...] = tuple(round(0.90 + 0.02 * index, 2) for index in range(11))

#: Only the bullets' own `**lead-in.**` and `backticks` become markup.
BOLD = re.compile(r"\*\*(.+?)\*\*")
CODE = re.compile(r"`([^`]+)`")


def data_uri(path: Path) -> str:
    return "data:image/png;base64," + base64.b64encode(path.read_bytes()).decode()


def esc(value: object) -> str:
    return html.escape(str(value), quote=False)


def table(frame: pd.DataFrame, *, float_format: str = "{:.4g}") -> str:
    head = "".join(f"<th>{esc(column)}</th>" for column in frame.columns)
    rows = []
    for _, row in frame.iterrows():
        cells = []
        for value in row:
            if isinstance(value, float) and value == value:
                cells.append(f"<td class='n'>{float_format.format(value)}</td>")
            elif value != value:
                cells.append("<td class='n'></td>")
            else:
                cells.append(f"<td>{esc(value)}</td>")
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return f"<div class='scroll'><table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table></div>"


def build_chart_payload() -> dict:
    """Precompute the nine quantiles per hour at each load-scale point."""
    champion = load_champion()
    snapshot = load_snapshot()
    target = default_target_day(snapshot)
    actual = actuals_for_day(snapshot, target)

    series: dict[str, list[list[float]]] = {}
    for scale in LOAD_SCALES:
        forecast = forecast_delivery_day(champion, snapshot, target, load_scale=scale)
        series[f"{scale:.2f}"] = [
            [float(row[label]) for label in QUANTILE_LABELS] for _, row in forecast.iterrows()
        ]
        if scale == 1.00:
            hours = [int(value) for value in forecast["local_hour"]]

    flat = [value for rows in series.values() for row in rows for value in row]
    flat += [float(value) for value in actual.to_numpy()]
    low, high = min(flat), max(flat)
    pad = (high - low) * 0.06
    return {
        "delivery_day": target.isoformat(),
        "hours": hours,
        "labels": list(QUANTILE_LABELS),
        "levels": {str(level): list(pair) for level, pair in INTERVAL_LEVELS.items()},
        "scales": [f"{scale:.2f}" for scale in LOAD_SCALES],
        "series": series,
        "actual": [float(value) for value in actual.to_numpy()],
        "domain": [low - pad, high + pad],
    }


CSS = """
:root{--ink:#16202b;--mute:#5a6a7a;--rule:#d7dee6;--band:#3a6ea5;--warn:#8a4b2a;--bg:#fbfcfd;--card:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font:16px/1.62 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:960px;margin:0 auto;padding:32px 20px 96px}
h1{font-size:2.05rem;line-height:1.2;margin:.2em 0 .3em}
h2{font-size:1.32rem;margin:2.4em 0 .5em;padding-top:.5em;border-top:1px solid var(--rule)}
h3{font-size:1.05rem;margin:1.6em 0 .4em;color:var(--mute);text-transform:uppercase;letter-spacing:.04em}
p,li{max-width:74ch}
a{color:#1d4e89}
code,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.88em}
.lede{font-size:1.08rem;color:var(--mute)}
.card{background:var(--card);border:1px solid var(--rule);border-radius:10px;padding:16px 20px;margin:18px 0}
.label{background:#fff5ec;border-left:4px solid var(--warn);padding:12px 16px;margin:18px 0;border-radius:0 8px 8px 0}
.label strong{color:var(--warn)}
blockquote{margin:18px 0;padding:12px 18px;border-left:4px solid var(--band);background:#f2f6fb;
 border-radius:0 8px 8px 0;color:#243546}
blockquote p{margin:.3em 0}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:14px 0}
table{border-collapse:collapse;font-size:.87rem;min-width:100%}
th,td{border-bottom:1px solid var(--rule);padding:6px 12px;text-align:left;white-space:nowrap}
th{background:#f0f4f8;font-weight:600}
td.n{text-align:right;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
figure{margin:20px 0}
figure img{width:100%;height:auto;border:1px solid var(--rule);border-radius:8px;background:#fff}
figcaption{font-size:.85rem;color:var(--mute);margin-top:6px}
.figrow{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:16px}
.controls{display:flex;flex-wrap:wrap;gap:22px;align-items:center;margin:16px 0 6px}
.controls fieldset{border:1px solid var(--rule);border-radius:8px;padding:8px 14px;margin:0}
.controls legend{font-size:.78rem;color:var(--mute);text-transform:uppercase;letter-spacing:.05em}
.controls label{margin-right:12px;font-size:.92rem;white-space:nowrap}
#chart{width:100%;height:auto;background:#fff;border:1px solid var(--rule);border-radius:8px}
.kv{display:grid;grid-template-columns:max-content 1fr;gap:4px 18px;font-size:.92rem}
.kv dt{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;color:var(--mute)}
.kv dd{margin:0}
footer{margin-top:48px;padding-top:18px;border-top:1px solid var(--rule);font-size:.86rem;color:var(--mute)}
.toc{font-size:.92rem;columns:2;column-gap:32px}
.toc a{display:block;padding:2px 0}
@media (max-width:620px){.toc{columns:1}main{padding:20px 14px 64px}}
"""

CHART_JS = """
(function(){
 var D=window.__FAN__,W=960,H=380,ML=58,MR=16,MT=18,MB=34;
 var n=D.hours.length,dom=D.domain;
 var svg=document.getElementById('chart');
 function X(i){return ML+(W-ML-MR)*(n<2?0.5:i/(n-1));}
 function Y(v){return MT+(H-MT-MB)*(1-(v-dom[0])/(dom[1]-dom[0]));}
 function state(){
  var lv=document.querySelector('input[name=lvl]:checked').value;
  var sc=D.scales[parseInt(document.getElementById('scale').value,10)];
  return {lv:lv,sc:sc};
 }
 function ticks(){
  var span=dom[1]-dom[0],raw=span/6,mag=Math.pow(10,Math.floor(Math.log(raw)/Math.LN10));
  var step=[1,2,2.5,5,10].map(function(m){return m*mag;}).filter(function(s){return s>=raw;})[0]||mag*10;
  var out=[],v=Math.ceil(dom[0]/step)*step;
  for(;v<=dom[1];v+=step){out.push(Math.round(v*100)/100);}
  return out;
 }
 function el(tag,attrs,text){
  var e=document.createElementNS('http://www.w3.org/2000/svg',tag);
  for(var k in attrs){e.setAttribute(k,attrs[k]);}
  if(text!==undefined){e.textContent=text;}
  return e;
 }
 function draw(){
  var s=state(),pair=D.levels[s.lv],rows=D.series[s.sc];
  if(!pair||!rows){throw new Error('fan chart lookup miss: level '+s.lv+', scale '+s.sc);}
  var li=D.labels.indexOf(pair[0]),hi=D.labels.indexOf(pair[1]),mi=D.labels.indexOf('p50');
  while(svg.firstChild){svg.removeChild(svg.firstChild);}
  ticks().forEach(function(t){
   svg.appendChild(el('line',{x1:ML,x2:W-MR,y1:Y(t),y2:Y(t),stroke:t===0?'#9aa7b4':'#eceff3','stroke-width':t===0?1.2:1}));
   svg.appendChild(el('text',{x:ML-8,y:Y(t)+4,'text-anchor':'end',fill:'#5a6a7a','font-size':11},t));
  });
  for(var i=0;i<n;i+=2){
   svg.appendChild(el('text',{x:X(i),y:H-12,'text-anchor':'middle',fill:'#5a6a7a','font-size':11},D.hours[i]));
  }
  var up=[],down=[];
  for(var j=0;j<n;j++){up.push(X(j)+','+Y(rows[j][hi]));}
  for(var k=n-1;k>=0;k--){down.push(X(k)+','+Y(rows[k][li]));}
  svg.appendChild(el('polygon',{points:up.concat(down).join(' '),fill:'#3a6ea5','fill-opacity':.22}));
  var med=[];
  for(var m=0;m<n;m++){med.push(X(m)+','+Y(rows[m][mi]));}
  svg.appendChild(el('polyline',{points:med.join(' '),fill:'none',stroke:'#1b3a5c','stroke-width':2.2}));
  if(s.sc==='1.00'){
   var act=[];
   for(var a=0;a<n;a++){act.push(X(a)+','+Y(D.actual[a]));}
   svg.appendChild(el('polyline',{points:act.join(' '),fill:'none',stroke:'#b03a2e','stroke-width':1.6,'stroke-dasharray':'6 4'}));
  }
  svg.appendChild(el('text',{x:ML,y:MT-4,fill:'#5a6a7a','font-size':11},
   'EUR/MWh  ·  local hour (Europe/Berlin)  ·  delivery day '+D.delivery_day));
  document.getElementById('scaleval').textContent='\\u00d7 '+s.sc;
  document.getElementById('cov').textContent=window.__COV__[s.lv];
  document.getElementById('scenario').style.display=(s.sc==='1.00')?'none':'block';
  document.getElementById('legend-actual').style.display=(s.sc==='1.00')?'inline':'none';
 }
 Array.prototype.forEach.call(document.querySelectorAll('input[name=lvl]'),function(r){r.addEventListener('change',draw);});
 document.getElementById('scale').addEventListener('input',draw);
 draw();
})();
"""


def build_html() -> str:
    C = build_claims()
    payload = build_chart_payload()
    regime = pd.read_csv(ROOT / "reports/cp2/regime_table.csv")
    shap_top = pd.read_csv(ROOT / "reports/cp2/shap_ranking.csv").head(10)
    perm_top = pd.read_csv(ROOT / "reports/cp2/permutation_importance.csv").head(10)
    pooled = pd.read_csv(ROOT / "reports/cp2/development_pooled_metrics.csv")
    reliability = pd.read_csv(ROOT / "reports/cp2/reliability_three_stage.csv")

    coverage = {str(level): C[f"holdout_coverage_{level}"] for level in INTERVAL_LEVELS}
    # §10 item (11): one shared set, rendered onto every surface. The bullets
    # arrive with a `**bold**` lead-in; only that lead-in becomes markup, so the
    # limitation sentence itself reaches the page byte-identical to the other
    # surfaces and the agreement check compares like with like.
    limitations = "\n".join(
        "<li>" + BOLD.sub(r"<strong>\1</strong>", esc(bullet)) + "</li>"
        for bullet in limitation_bullets(C)
    )
    # §10 item (12): the same treatment, so no surface can carry a partial
    # reproducibility statement. `CODE` turns the bullets' own backticks into
    # <code>, after escaping, so the sentence itself stays byte-identical to
    # the Markdown surfaces once markup is stripped.
    reproduction = "\n".join(
        "<li>" + CODE.sub(r"<code>\1</code>", BOLD.sub(r"<strong>\1</strong>", esc(bullet))) + "</li>"
        for bullet in reproducibility_bullets(C)
    )
    level_inputs = "".join(
        f"<label><input type='radio' name='lvl' value='{level}'"
        f"{' checked' if level == 80 else ''}> {level}&nbsp;%</label>"
        for level in sorted(INTERVAL_LEVELS)
    )

    figures = {
        "welch": data_uri(ROOT / "reports/fig_welch_periodogram.png"),
        "regime_spectrum": data_uri(ROOT / "reports/fig_per_regime_periodogram.png"),
        "acf": data_uri(ROOT / "reports/fig_acf_24_168.png"),
        "shap": data_uri(ROOT / "reports/cp2/fig_shap_summary.png"),
        "dep24": data_uri(ROOT / "reports/cp2/fig_shap_dependence_price_lag_24h.png"),
        "dep168": data_uri(ROOT / "reports/cp2/fig_shap_dependence_price_lag_168h.png"),
        "reliability": data_uri(ROOT / "reports/cp2/fig_reliability_three_stage.png"),
    }

    cutoff_table = f"""
    <div class='scroll'><table><thead><tr><th>Cutoff</th><th>Value</th></tr></thead><tbody>
    <tr><td><code>snapshot_cutoff</code></td><td class='n'>{C['snapshot_cutoff']}</td></tr>
    <tr><td><code>raw_model_fit_cutoff</code></td><td class='n'>{C['raw_model_fit_cutoff']}</td></tr>
    <tr><td><code>final_calibration_window</code></td><td class='n'>{C['final_calibration_window']}</td></tr>
    <tr><td><code>holdout_window</code></td><td class='n'>{C['holdout_window']}</td></tr>
    </tbody></table></div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>DE-LU day-ahead price forecasting — probabilistic, strict-gate, one-shot evaluated</title>
<meta name="description" content="A probabilistic day-ahead electricity price forecast for the German-Luxembourg bidding zone: LightGBM nine-quantile ensemble, CQR calibration, isotonic last, evaluated once on a pre-specified 90-day holdout.">
<style>{CSS}</style>
</head>
<body>
<main>

<h1>DE-LU day-ahead price forecasting</h1>
<p class="lede">A probabilistic forecast of the next delivery day's hourly German–Luxembourg
day-ahead electricity price, with calibrated 50 / 80 / 95&nbsp;% prediction intervals.
<strong>Strict-gate by construction:</strong> the shipped model uses no input published after the
12:00&nbsp;CET day-ahead auction gate. Evaluated exactly once, on a holdout pinned before
development.</p>

<div class="card">
<p><strong>{esc(C['shipped_is_evaluated'])}</strong></p>
<p>This page is static. It renders from files committed in the repository and makes
<strong>no runtime call</strong> to any external service — no analytics, no fonts, no CDN, no call
to the interactive Space. Everything below, including the chart, works with the network off.</p>
<p class="toc">
<a href="#data">1 · The data</a><a href="#regimes">2 · Three regimes</a>
<a href="#catalog">3 · Feature catalog</a><a href="#spectral">3b · Spectral view</a>
<a href="#method">4 · Validation design</a><a href="#results">5 · Results</a>
<a href="#shap">6–7 · Explainability</a><a href="#regime-table">8 · Regime-stratified error</a>
<a href="#reliability">9 · Reliability</a><a href="#forecast">10 · Next-day forecast</a>
<a href="#limitations">11 · Honest limitations</a><a href="#repro">12 · Reproducibility</a>
</p>
</div>

<h3>The four cutoffs, stated separately because they are four different dates</h3>
{cutoff_table}
<p>The raw-model fit cutoff precedes the snapshot cutoff by <strong>{C['staleness_days']} delivery
days</strong> (1 + 60 + 1 + 90). That is what shipping the evaluated model costs, stated plainly
rather than apologised for; the deployed demo applies a <strong>frozen</strong> model and there is
no scheduled refresh.</p>

<h2 id="data">1 · The data</h2>
<p>One committed Parquet snapshot: <strong>67,343</strong> continuous UTC-indexed hourly rows,
delivery 2019-01-01 through {C['snapshot_cutoff']}, carrying the day-ahead price (A44), the
day-ahead load forecast (A65/A01), the benchmark-only day-ahead VRE forecast (A69) and aggregate
actual generation (A75). Quarter-hourly feeds aggregate to hours from exactly four complete bins,
never a partial one; the 2025-10-01 switch to a 15-minute price product is handled as the mean of
four quarter-hour prices. The snapshot is pinned by SHA-256
<code>{C['snapshot_sha256']}</code> and ships inside the container, so the demo never pulls a feed
while you use it.</p>
<p>{esc(C['attribution'])}</p>

<h2 id="regimes">2 · Three regimes in one series</h2>
<p>The annual mean price swept from about <strong>€30/MWh</strong> in 2020 to about
<strong>€235/MWh</strong> in 2022 and back to about <strong>€89/MWh</strong> in 2025 — a crisis
and a normalization inside one training set. Underneath it, the solar build-out pushed
negative-price hours from <strong>139</strong> (2021) → <strong>69</strong> (2022) →
<strong>301</strong> (2023) → <strong>457</strong> (2024) → <strong>576</strong> (2025).</p>
<p>The 2025 count is measured on this snapshot's hourly series. From 2025-10-01 an hour is the mean
of four quarter-hour prices, so any hour-level tally depends on that averaging choice and a
quarter-hour tally differs. The price is routinely negative and has touched the −500&nbsp;€/MWh
floor, which is why no log or Box-Cox transform is applied to the target: pinball loss, the CQR
score and monotone rearrangement are all location-equivariant and behave correctly through zero.</p>
<p>Two consequences the whole design follows from. Evaluation is stratified across all three
regimes rather than collapsed into a recent tail. And exchangeability — the assumption CQR's
coverage guarantee rests on — is mildly violated by construction, which is disclosed rather than
assumed away.</p>

<h2 id="catalog">3 · Feature catalog — frozen before fitting</h2>
<p>Two catalogs were frozen before any model ran. <code>base</code>: calendar and regime features,
the A65 load forecast, calendar-day-matched price lags at D−1 / D−2 / D−7, and D-1-frozen rolling
price statistics. <code>base + residual_load_proxy</code> adds exactly one domain feature — a
residual-load proxy built from a 42-complete-delivery-day trailing mean of actual wind and solar
generation ending at D−2, which clears the 12:00 gate with a wide margin.</p>
<p>Pooled observation-weighted <em>raw-head</em> mean pinball loss over the five pinned development
folds, matched on rows, seed, hyperparameters and (zero) tuning budget, unrounded as stored:</p>
<div class="scroll"><table><thead><tr><th>Arm</th><th>Pooled raw-head mean pinball loss</th></tr></thead>
<tbody>
<tr><td><code>base</code></td><td class="n">{C['catalog_base_loss']}</td></tr>
<tr><td><code>base + residual_load_proxy</code></td><td class="n">{C['catalog_augmented_loss']}</td></tr>
</tbody></table></div>
<p>Percentage difference (augmented vs base): <strong>{C['catalog_pct']}</strong>.
<strong>Selected catalog: <code>{C['selected_catalog']}</code>.</strong> The rule was fixed before
fitting — the augmented catalog ships only if its unrounded stored pooled loss is lower. It is not,
so the domain feature did not earn its place and the champion ships strict-gate. That is a
reportable result, not a failure, and the comparison was designed so that "no improvement" was a
publishable answer.</p>

<h2 id="spectral">3b · Why these seasonal features? (spectral view)</h2>
<div class="figrow">
<figure><img alt="Welch periodogram of the detrended DE-LU day-ahead price, with 24h, 168h and 12h labels" src="{figures['welch']}"><figcaption>Welch periodogram — Hann window, 50&nbsp;% overlap.</figcaption></figure>
<figure><img alt="Per-regime Welch periodogram overlay for pre-crisis, crisis and normalization" src="{figures['regime_spectrum']}"><figcaption>Per-regime overlay.</figcaption></figure>
<figure><img alt="Autocorrelation of the detrended price with 24h and 168h reference lines" src="{figures['acf']}"><figcaption>ACF cross-check, time domain.</figcaption></figure>
</div>
<p>The Welch periodogram shows pronounced price energy at the 24-hour and 168-hour cycles with a
visible 12-hour harmonic, which is what justifies the catalog's hour-of-day and day-of-week
structure rather than an assumption that electricity "should" be daily-seasonal. The per-regime
overlay shows an elevated broadband floor and altered seasonal amplitude during the crisis: the
spectrum itself is not stationary across regimes, which supports reporting performance across all
three rather than collapsing them into one recent-tail summary. The ACF cross-check confirms the
same daily and weekly recurrence in the time domain, so the conclusion does not rest on a single
estimator. These are price diagnostics only — they neither validate nor justify retaining
<code>residual_load_proxy</code>, which the frozen two-arm comparison alone decides.</p>

<h2 id="method">4 · Validation design</h2>
<p>Expanding-window walk-forward CV with five development folds, each carrying a
<strong>one-complete-delivery-day embargo</strong> — 23, 24 or 25 rows as DST requires, never
hard-coded to 24 — and a 90-day evaluation block, anchored so the blocks span pre-crisis, the
crisis peak and the post-crisis negative-price era. Five tail partitions were pinned before any
EDA: fold&nbsp;5, Embargo&nbsp;A, a 60-day final-calibration slice, Embargo&nbsp;B, and the final
90-day holdout.</p>
<p><strong>The target is D+1, anchored at the 12:00 CET gate</strong>, because that is what the
day-ahead auction clears. That makes the availability rule stricter than it first looks: the model
emits the whole next-day curve at once, so a row-wise <code>t−1</code> boundary would admit the
target curve into its own features. The binding rule is per delivery day — for a forecast of day
<code>D</code>, every price-derived feature may consume only prices whose delivery date is earlier
than <code>D</code>, rolling statistics are frozen at the D−1 boundary for the whole curve, and an
unavailable or ambiguous calendar-day match fails closed to null rather than reaching for a
same-day price.</p>
<p><strong>Strict gate.</strong> The day-ahead wind and solar forecast (A69) is not published until
after the 12:00 gate, so rather than use it as-archived and disclose that, this project excludes it
from the shipped model entirely. Delivery-day A69 is rejected by the champion's runtime schema.
What the exclusion costs is then measured, in section&nbsp;5, instead of being waved at.</p>
<p><strong>Two disclosed assumptions, stated as assumptions rather than as measurements:</strong></p>
<ul>
<li>{esc(C['assumption_a65'])}</li>
<li>{esc(C['assumption_a75'])}</li>
</ul>

<h2 id="results">5 · Results</h2>
<h3>Development folds — descriptive post-selection evidence</h3>
<p><code>evidence_class = {C['development_evidence_class']}</code>. These folds were also used for
catalog selection and model development, so their p-values are descriptive, never confirmatory, and
no result gates anything.</p>
<div class="scroll"><table><thead><tr><th>Analysis</th><th>Comparator</th><th>Statistic</th><th>p-value</th><th>N days</th></tr></thead>
<tbody>
<tr><td>Probabilistic daily-vector pinball</td><td>similar-day naive</td><td class="n">{C['development_dm_pinball_statistic']}</td><td class="n">{C['development_dm_pinball_p_value']}</td><td class="n">{C['development_days']}</td></tr>
<tr><td>Point median absolute error</td><td>similar-day naive</td><td class="n">{C['development_dm_point_statistic']}</td><td class="n">{C['development_dm_point_p_value']}</td><td class="n">{C['development_days']}</td></tr>
</tbody></table></div>
<p><strong>The point-accuracy test does not merely fail to show an advantage — it shows a
deficit.</strong> The test is one-sided (reject if DM &lt; −1.645) and the statistic is
<em>+{C['development_dm_point_statistic_abs']}</em>, p = {C['development_dm_point_p_value']}: the champion's median is
{C['development_dm_point_relative']} against the naive over the development folds. Reported here rather than
omitted or reframed. The
probabilistic win is broad and the point-accuracy win is not: the pooled MAE gap comes almost
entirely from the crisis-peak fold. The mechanism is measured, not assumed: the model did see the
crisis (that fold's training included 5,784 crisis hours at a €173 mean and a €700 maximum), but
<strong>61.3% of the evaluation block sits above the 99th percentile of everything it ever saw while
only 2.45% exceeds its maximum</strong> — shrinkage toward the training level, not an extrapolation
wall. Persistence has no training distribution and carries the level for free. Note also that
a point forecast scored on pinball is structurally disadvantaged against a nine-quantile model, so
the pinball margin is largely the value of <em>having</em> a predictive distribution.</p>
{table(pooled)}

<h3>The one-shot holdout — opened exactly once</h3>
<p>After the catalog, hyperparameters and every implementation choice were frozen, the nine raw
heads were fit on every eligible row strictly before Embargo&nbsp;A, the four CQR thresholds were
estimated once on the 60-day calibration slice, isotonic-last was attached, and that complete
artifact was frozen. Only then was the holdout opened.</p>
<div class="scroll"><table><thead><tr><th>Metric</th><th>Champion</th><th>Similar-day naive</th><th>Difference</th></tr></thead>
<tbody>
<tr><td>MAE (EUR/MWh)</td><td class="n">{C['holdout_mae_champion']}</td><td class="n">{C['holdout_mae_naive']}</td><td class="n">{C['holdout_mae_pct']}</td></tr>
<tr><td>Mean pinball loss</td><td class="n">{C['holdout_pinball_champion']}</td><td class="n">{C['holdout_pinball_naive']}</td><td class="n">{C['holdout_pinball_pct']}</td></tr>
</tbody></table></div>
<p>Final empirical coverage over {C['holdout_rows']} rows on {C['holdout_days']} delivery days:
<strong>{C['holdout_coverage_50']}</strong> / <strong>{C['holdout_coverage_80']}</strong> /
<strong>{C['holdout_coverage_95']}</strong> at the 50 / 80 / 95&nbsp;% nominal levels.
Probabilistic daily-vector Diebold–Mariano against the similar-day naive: statistic
<strong>{C['holdout_dm_statistic']}</strong>, p-value <strong>{C['holdout_dm_p_value']}</strong>,
standardized effect size <strong>{C['holdout_dm_effect_size']}</strong>.</p>
<blockquote><p>{esc(C['holdout_dm_label'])}</p></blockquote>
<p>The result supports a probabilistic-skill claim against the similar-day naive on this window and
nothing wider. It is not a gate, and no superiority claim beyond what it supports is made anywhere
on this page.</p>

<h3>What the post-gate forecast would have been worth</h3>
<p>A controlled ablation on raw quantile heads, neither arm calibrated, identical in every respect
except the added delivery-day A69 forecast and its named derivatives: pooled mean pinball loss
moves from <code>{C['benchmark_strict_loss']}</code> to <code>{C['benchmark_a69_loss']}</code> —
<strong>{C['benchmark_pct']}</strong>. So the project ships an honest model and puts a number on the
value of the information it chose not to use.</p>
<blockquote><p>{esc(C['benchmark_limitation'])}</p></blockquote>

<h2 id="shap">6–7 · Explainability</h2>
<figure><img alt="SHAP summary plot for the p50 head of the champion catalog" src="{figures['shap']}"><figcaption>SHAP summary, p50 head, scored out of sample on fold 5's evaluation block.</figcaption></figure>
<div class="figrow">
<figure><img alt="SHAP dependence plot for price_lag_24h" src="{figures['dep24']}"><figcaption><code>price_lag_24h</code></figcaption></figure>
<figure><img alt="SHAP dependence plot for price_lag_168h" src="{figures['dep168']}"><figcaption><code>price_lag_168h</code></figcaption></figure>
</div>
<div class="figrow">
<div><h3>Top 10 by mean |SHAP|</h3>{table(shap_top)}</div>
<div><h3>Top 10 by permutation importance</h3>{table(perm_top)}</div>
</div>
<p>SHAP on the p50 head explains central tendency, not interval width — width is driven by the
inter-quantile spread and the CQR shift. Neither ranking is the incremental-value test; that is the
frozen two-arm comparison in section&nbsp;3, which selected <code>{C['selected_catalog']}</code>.
The two rankings agree at the top and disagree in the middle, which is the ordinary difference
between attribution in expectation and degradation under shuffling.</p>

<h2 id="regime-table">8 · Regime-stratified error</h2>
<p><code>n_obs</code> on every row. Thin subsets carry day-block bootstrap 95&nbsp;% confidence
intervals — days, not hours, because the rows of one delivery day share a day effect — and are read
qualitatively.</p>
{table(regime)}
<p>Coverage collapses on the crisis stratum and on negative-price hours. The bounded target
truncates the lower conformity residuals near the floor, so the lowest intervals under-cover
conditionally. This is disclosed rather than engineered around: a floor-aware tail would reopen
scope this project deliberately closed.</p>

<h2 id="reliability">9 · Reliability — three stages</h2>
<figure><img alt="Three-stage reliability diagram: raw LightGBM, post-CQR, and final post-isotonic" src="{figures['reliability']}"><figcaption>Raw heads → CQR → isotonic last, at all three nominal levels.</figcaption></figure>
{table(reliability)}
<p>The finite-sample, distribution-free per-interval marginal guarantee attaches to the
<strong>post-CQR / pre-isotonic</strong> output only. Isotonic is a monotone rearrangement applied
last; whenever it moves an endpoint it perturbs the interval, so the final output's coverage is
reported as <strong>empirical</strong>. No joint or simultaneous coverage across the four intervals
is claimed.</p>
<p>The one retained hard gate is a correctness property, not a favourable number: zero
quantile-crossing violations after the full pipeline. On the selected
<code>{C['selected_catalog']}</code> catalog's development evaluation rows, the raw heads cross on
{C['crossings_development_raw']} adjacent pairs and still cross on
{C['crossings_development_post_cqr']} after CQR; after isotonic the count is
{C['crossings_development_final']}, and {C['crossings_holdout_final']} on the holdout. That CQR
alone leaves thousands of crossings is exactly why isotonic is unconditionally last.</p>
<blockquote><p>{esc(C['exchangeability'])}</p></blockquote>

<h2 id="forecast">10 · Next-day forecast</h2>
<div class="label">
<p><strong>{esc(C['replay_label'])}</strong> The delivery day below, {payload['delivery_day']},
falls inside the pinned holdout window {C['holdout_window']}. The dashed line is the price that
actually cleared — an outcome, never a model input.</p>
</div>
<div class="controls">
<fieldset><legend>Prediction-interval level</legend>{level_inputs}</fieldset>
<fieldset><legend>Load-forecast scenario <span id="scaleval" class="mono">&times; 1.00</span></legend>
<input id="scale" type="range" min="0" max="{len(LOAD_SCALES) - 1}" step="1" value="{LOAD_SCALES.index(1.00)}"
 style="width:220px" aria-label="load forecast scenario multiplier">
</fieldset>
</div>
<svg id="chart" viewBox="0 0 960 380" role="img" aria-label="Quantile fan chart for the selected delivery day"></svg>
<p><span class="mono" style="color:#1b3a5c">——</span> median forecast &nbsp;
<span class="mono" style="color:#3a6ea5">▇</span> selected interval &nbsp;
<span id="legend-actual"><span class="mono" style="color:#b03a2e">– –</span> cleared price (outcome)</span></p>
<p>Nominal level selected above; the frozen champion's own empirical coverage at that level over
the {C['holdout_days']}-day holdout was <strong id="cov">{C['holdout_coverage_80']}</strong>.</p>
<div class="label" id="scenario" style="display:none">
<p><strong>{esc(C['sensitivity_probe_label'])}</strong> The scenario holds every other input fixed,
including the price history the lags and rolling statistics are built from, so a large perturbation
asks the model a question it was never trained on. The cleared-price line is hidden while a
scenario is active, because the outcome belongs to the unperturbed day.</p>
</div>
<p class="lede">Want to drive the model yourself? The
<a href="{C['space_url']}">{esc(C['space_link_label'])}</a> runs the champion's own boosters in
your browser, proved bitwise equal to the frozen artifact over {C['wasm_fixture_days']} delivery days.
This page stays the first touch because it downloads nothing and cannot fail when a CDN does.</p>

<h2 id="limitations">11 · Honest limitations</h2>
<ul>
{limitations}
</ul>
<p>{esc(C['floor_change'])}</p>
<blockquote><p>{esc(C['holdout_limitation'])}</p></blockquote>

<h2 id="repro">12 · Reproducibility</h2>
<dl class="kv">
<dt>artifact_fingerprint_sha256</dt><dd><code>{C['champion_fingerprint']}</code></dd>
<dt>snapshot_sha256</dt><dd><code>{C['snapshot_sha256']}</code></dd>
<dt>catalog</dt><dd><code>{C['selected_catalog']}</code>, {C['champion_features']} features,
{C['champion_quantiles']} quantile heads, four CQR thresholds, isotonic last</dd>
<dt>fit / calibration rows</dt><dd>{C['champion_fit_rows']} raw-fit rows,
{C['champion_calibration_rows']} calibration rows</dd>
<dt>artifact size</dt><dd><code>python_model.pkl</code> {C['champion_pkl_bytes']} bytes =
{C['champion_pkl_size']}; the whole <code>models/champion/</code> directory
{C['champion_dir_bytes']} bytes = {C['champion_dir_size']}</dd>
<dt>compute</dt><dd>Apple M3, 16&nbsp;GB, CPU only, no GPU, $0 run rate</dd>
</dl>
<p>The pickle's bytes are deliberately <em>not</em> the identity to check: MLflow stamps a fresh
UUID and creation time into <code>MLmodel</code> on every save and cloudpickle is not
byte-reproducible, so <code>models/champion/</code> changes while the model does not. The
fingerprint is computed over the catalog, the feature list, the nine quantiles, the four thresholds
and the nine boosters' own serializations.</p>
<ul>
{reproduction}
<li><strong>Run it yourself.</strong> Clone
<a href="{C['github_url']}">{C['github_url']}</a>, then <code>uv sync</code>, then
<code>uv run python predict_next_day.py --level 80 --self-check</code> forecasts a delivery day
offline from the bundled snapshot and re-proves the gate boundary as it goes;
<code>make test</code> runs the invariant suite including the CQR order-statistic fixture;
<code>make sql</code> runs the DuckDB queries; and
<code>docker build -t delu-showcase . &amp;&amp; docker run -p 7860:7860 delu-showcase</code>
builds and serves the same image the Space runs, champion and snapshot bundled inside it.</li>
<li><strong>Compute.</strong> Apple M3, 16&nbsp;GB, CPU only, no GPU, $0 run rate; the whole
pipeline — development, benchmark, final fit and diagnostics — runs in well under an hour.</li>
</ul>

<footer>
<p>{esc(C['attribution'])}</p>
<p>Built from the committed artifacts at snapshot <code>{C['snapshot_sha256'][:16]}…</code>.
This page is static and self-contained: every figure is embedded, and it performs zero runtime
calls.</p>
</footer>

</main>
<script>
window.__FAN__={json.dumps(payload, separators=(",", ":"))};
window.__COV__={json.dumps(coverage, separators=(",", ":"))};
</script>
<script>{CHART_JS}</script>
</body>
</html>
"""


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = build_html()
    OUTPUT.write_text(document)
    (OUTPUT.parent / ".nojekyll").write_text("")

    BUILD_RECORD.parent.mkdir(parents=True, exist_ok=True)
    BUILD_RECORD.write_text(
        json.dumps(
            {
                "output": str(OUTPUT.relative_to(ROOT)),
                "bytes": len(document.encode()),
                "load_scale_points": len(LOAD_SCALES),
                "build_path": "purpose-built static assembly (§9.2 fallback)",
                "marimo_export_html_rejected_because": (
                    "measured 2026-09-14 with marimo 0.24.2: `marimo export html` emits 181 "
                    "external references to cdn.jsdelivr.net (frontend JS bundle, CSS and five "
                    "web fonts), so the page cannot render without network. CP-3 item 3 requires "
                    "zero runtime calls."
                ),
                "marimo_export_external_reference_count": 181,
                "marimo_export_external_hosts": ["cdn.jsdelivr.net"],
                "built_on": date.today().isoformat(),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    print(f"wrote {OUTPUT} ({len(document):,} bytes) and {OUTPUT.parent / '.nojekyll'}")
    print(f"wrote {BUILD_RECORD}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
