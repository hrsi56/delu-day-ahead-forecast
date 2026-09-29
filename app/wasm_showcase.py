# /// script
# requires-python = ">=3.11"
# dependencies = ["marimo", "numpy", "lightgbm"]
# ///
"""The WASM showcase (M3.5/CP-3B; §9.2 with its server-mode clause suspended).

Exported with `marimo export html-wasm` and served by a Hugging Face **Static**
Space. The reason is not elegance: Hugging Face moved the Docker SDK behind a
paid plan on 2026-07-08, and a free Docker Space sleeps. A Static Space executes
nothing on the server, so it cannot sleep — the demo is either reachable or the
CDN is down.

The model is not a re-training or a re-fit. It is the same nine boosters, the
same base catalog, the same four CQR thresholds and the same isotonic step,
executing in the browser because `mlflow.pyfunc` does not load under Pyodide.
`tests/test_22_wasm_equivalence.py` proves that composition equals the frozen
champion bitwise over the committed fixture in tests/fixtures/ — the page
reports the size and result it computes, rather than a number typed here.

Two controls only (§9.2): the quantile-level selector, and one load-forecast
scenario probe. Both are served by real local inference in the browser.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", app_title="DE-LU Day-Ahead Forecast — runs in your browser")


@app.cell
def _():
    import json

    import marimo as mo
    import numpy as np

    def _base():
        """Where `public/` lives, in WASM and when run locally."""
        try:
            return str(mo.notebook_location()) + "/public"
        except Exception:
            return "public"

    def read_text(name: str) -> str:
        url = f"{_base()}/{name}"
        try:
            from pyodide.http import open_url

            return open_url(url).read()
        except ImportError:
            from pathlib import Path

            return Path(url).read_text()

    def read_json(name: str):
        return json.loads(read_text(name))

    def read_packed_text(name: str) -> str:
        """Fetch a base64-encoded gzip file as text and return the original text.

        Why this shape: Hugging Face serves Static Spaces uncompressed, so the
        boosters must ship compressed; and it serves binary files through a
        no-store redirect to a signed URL that changes every request, which no
        browser can cache. Base64 keeps the compressed file plain text, served
        directly and cached like the rest of the page.
        """
        import base64
        import gzip

        return gzip.decompress(base64.b64decode(read_text(name))).decode()

    return json, mo, np, read_json, read_packed_text, read_text


@app.cell
def _(read_json, read_packed_text, read_text):
    # The heavy cell: nine boosters, about 15 MB on the wire as base64 gzip and
    # 31 MB of model text once decoded. Everything else is small.
    import lightgbm as lgb

    META = read_json("champion.json")
    CLAIMS = read_json("claims.json")
    SERIES = read_json("series.json")
    CALENDAR = read_json("calendar.json")
    FIXTURE = read_json("fixture.json")

    # The browser executes the exact bytes the host test verified. Not a copy of
    # the logic -- the file itself.
    _module = {}
    exec(read_text("browser_champion.py"), _module)  # noqa: S102
    BrowserChampion = _module["BrowserChampion"]

    BOOSTERS = {
        _label: lgb.Booster(model_str=read_packed_text(f"boosters/{_label}.txt.gz.b64"))
        for _label in META["quantile_labels"]
    }
    CHAMPION = BrowserChampion(BOOSTERS, META, SERIES, CALENDAR)
    return CHAMPION, CLAIMS, FIXTURE, META


@app.cell
def _(CLAIMS, mo):
    mo.md(
        f"""
        # DE-LU day-ahead price forecast · v1

        > **{CLAIMS['replay_label']}**

        Forecast calculations run locally in your browser. The [report]({CLAIMS['pages_url']}) is the
        primary entry point; evidence and reproduction details are at the end of this page.
        """
    )
    return


@app.cell
def _(mo):
    level = mo.ui.radio(
        options={"50 %": 50, "80 %": 80, "95 %": 95},
        value="80 %",
        label="Prediction-interval level",
        inline=True,
    )
    load_scale = mo.ui.slider(
        start=0.90, stop=1.10, step=0.01, value=1.00,
        label="Load-forecast scenario: × the day's load forecast, every other input fixed",
        show_value=True,
    )
    # §9.2: "The page states once that scenario perturbations are ceteris-paribus
    # sensitivity probes". Stated with the control, on first render -- not only
    # after a visitor has already moved it.
    return level, load_scale


@app.cell
def _(CLAIMS, level, load_scale, mo):
    mo.vstack([
        mo.hstack([level, load_scale], justify="start", gap=2, wrap=True),  # the slider drops below on a phone
        mo.md(
            f"*{CLAIMS['sensitivity_probe_label']} The load-forecast control holds every "
            "other input fixed, including the price history, so a large perturbation asks "
            "the model a question it was never trained on.*"
        ),
    ])
    return


@app.cell
def _(np):
    PAIRS = {50: ("p25", "p75"), 80: ("p10", "p90"), 95: ("p025", "p975")}

    def fan_svg(hours, low, mid, high, actual=None, compact=False):
        """Inline SVG, built here rather than by matplotlib.

        matplotlib's wheel is several megabytes in Pyodide and this page already
        asks a visitor to download nine boosters. A fan chart is two polylines
        and a polygon; it does not justify the dependency. `compact` is a separate
        phone drawing, so its text renders at 12 px instead of a shrunk desktop chart.
        """
        width, height = (340, 260) if compact else (920, 380)
        font, hour_step = 12, (4 if compact else 2)
        ml, mr, mt, mb = (40, 10, 22, 30) if compact else (58, 16, 20, 34)
        series = [v for v in list(low) + list(high) if v == v]
        if actual is not None:
            series += [v for v in actual if v == v]
        lo, hi = min(series), max(series)
        pad = (hi - lo) * 0.08 or 1.0
        lo, hi = lo - pad, hi + pad
        n = len(hours)

        def X(i):
            return ml + (width - ml - mr) * (i / (n - 1) if n > 1 else 0.5)

        def Y(v):
            return mt + (height - mt - mb) * (1 - (v - lo) / (hi - lo))

        span = hi - lo
        step = 10 ** np.floor(np.log10(span / 6))
        for mult in (1, 2, 2.5, 5, 10):
            if mult * step >= span / 6:
                step = mult * step
                break
        ticks, value = [], np.ceil(lo / step) * step
        while value <= hi:
            ticks.append(round(float(value), 2) + 0.0)  # + 0.0 turns -0.0 into 0.0, so no "-0" label
            value += step

        parts = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
                 f'role="img" aria-label="Quantile fan chart" style="width:100%;height:auto;'
                 f'background:#fff;border:1px solid #d7dee6;border-radius:8px">']
        for tick in ticks:
            colour = "#9aa7b4" if tick == 0 else "#eceff3"
            parts.append(f'<line x1="{ml}" x2="{width-mr}" y1="{Y(tick):.1f}" y2="{Y(tick):.1f}" '
                         f'stroke="{colour}" stroke-width="{1.2 if tick == 0 else 1}"/>')
            parts.append(f'<text x="{ml-8}" y="{Y(tick)+4:.1f}" text-anchor="end" '
                         f'fill="#5a6a7a" font-size="{font}">{tick:g}</text>')
        for i in range(0, n, hour_step):
            parts.append(f'<text x="{X(i):.1f}" y="{height-10}" text-anchor="middle" '
                         f'fill="#5a6a7a" font-size="{font}">{hours[i]}</text>')
        band = [f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(high) if v == v]
        band += [f"{X(i):.1f},{Y(v):.1f}" for i, v in reversed(list(enumerate(low))) if v == v]
        # the outline carries the band's extent at 3:1 or more; the tint alone does not
        parts.append(f'<polygon points="{" ".join(band)}" fill="#3a6ea5" fill-opacity="0.22" '
                     f'stroke="#3a6ea5" stroke-width="1"/>')
        line = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(mid) if v == v)
        parts.append(f'<polyline points="{line}" fill="none" stroke="#1b3a5c" stroke-width="2.2"/>')
        if actual is not None:
            obs = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(actual) if v == v)
            parts.append(f'<polyline points="{obs}" fill="none" stroke="#b03a2e" '
                         f'stroke-width="1.6" stroke-dasharray="6 4"/>')
        header = "EUR/MWh · local hour" if compact else "EUR/MWh · local hour (Europe/Berlin)"
        parts.append(f'<text x="{ml}" y="{mt-8}" fill="#5a6a7a" font-size="{font}">{header}</text></svg>')
        return "".join(parts)

    return PAIRS, fan_svg


@app.cell
def _(CHAMPION, CLAIMS, META, PAIRS, fan_svg, level, load_scale, mo, np):
    _day = META["default_day"]
    _final, _hours = CHAMPION.predict_day(_day, load_scale=load_scale.value)
    _labels = list(META["quantile_labels"])
    _lo, _hi = PAIRS[level.value]
    _low = _final[:, _labels.index(_lo)]
    _mid = _final[:, _labels.index("p50")]
    _high = _final[:, _labels.index(_hi)]

    _actual = None
    if load_scale.value == 1.0:
        _rows = CHAMPION._rows_for_day[_day]
        _actual = [float(CHAMPION.price[i]) for i in _rows]

    _note = (
        f"**{CLAIMS['replay_label']}** Delivery day **{_day}**, inside the pinned holdout "
        f"window {CLAIMS['holdout_window']}. Nominal {level.value} %; the frozen champion's "
        f"empirical coverage at this level over the {CLAIMS['holdout_days']}-day holdout was "
        f"**{CLAIMS['holdout_coverage_' + str(level.value)]}**."
    )
    if load_scale.value != 1.0:
        _note += (
            f" Scenario active: load forecast × {load_scale.value:.2f}. "
            f"{CLAIMS['sensitivity_probe_label']} The cleared-price line is hidden while a "
            "scenario is active, because the outcome belongs to the unperturbed day."
        )
    else:
        _note += " The dashed line is the price that actually cleared — an outcome, never an input."

    _chart = (
        "<style>.fan-m{display:none}@media (max-width:640px){.fan-d{display:none}.fan-m{display:block}}</style>"
        f'<div class="fan-d">{fan_svg(_hours, _low, _mid, _high, _actual)}</div>'
        f'<div class="fan-m">{fan_svg(_hours, _low, _mid, _high, _actual, compact=True)}</div>'
    )
    mo.vstack([
        mo.Html(_chart),
        mo.md(_note),
        mo.md(
            f"Recomputed in your browser just now: {int(np.isfinite(_final).all(axis=1).sum())} "
            f"hours × {len(_labels)} quantile heads, CQR then isotonic."
        ),
    ])
    return


@app.cell
def _(CHAMPION, FIXTURE, META, mo, np):
    # The identity claim, checked in front of the reader rather than asserted.
    _worst, _rows, _cells, _nulls, _days = 0.0, 0, 0, 0, FIXTURE["days"]
    for _entry in _days:
        _got, _ = CHAMPION.predict_day(_entry["day"])
        _exp = np.array(
            [[np.nan if v is None else v for v in r]
             for r in FIXTURE["expected_final_quantiles"][_entry["day"]]],
            dtype="float64",
        )
        _gn, _en = np.isnan(_got), np.isnan(_exp)
        _nulls += int((_gn != _en).sum())
        _both = ~_gn & ~_en
        if _both.any():
            _worst = max(_worst, float(np.max(np.abs(_got[_both] - _exp[_both]))))
        _rows += len(_got)
        _cells += int(_both.sum())

    _regimes = sorted({e["regime"] for e in _days})

    # Which rows are undefined, and why -- derived from the data, never typed.
    # Round-1 review caught a hand-written sentence here that named the wrong day.
    import datetime as _dt

    _names = list(META["features"])
    _undefined = []
    for _entry in _days:
        _matrix, _hours = CHAMPION.features_for_day(_entry["day"])
        for _i, _hour in enumerate(_hours):
            _missing = [_names[_j] for _j in range(_matrix.shape[1]) if np.isnan(_matrix[_i, _j])]
            for _feature in _missing:
                _back = {"price_lag_24h": 1, "price_lag_48h": 2, "price_lag_168h": 7}.get(_feature)
                if _back is None:
                    _why = "incomplete input"
                else:
                    _source = (_dt.date.fromisoformat(_entry["day"]) - _dt.timedelta(days=_back)).isoformat()
                    _count = len(CHAMPION._rows_for_day.get(_source, []))
                    _why = (
                        f"sources {_source} {_hour:02d}:00, the hour the spring-forward transition removed"
                        if _count == 23 else
                        f"sources {_source} {_hour:02d}:00, the hour the fall-back transition repeated"
                        if _count == 25 else f"sources {_source}, which is not in the shipped slice"
                    )
                _undefined.append(f"{_entry['day']} {_hour:02d}:00 — `{_feature}` {_why}")
    _undefined_md = "\n".join(f"- {_row}" for _row in _undefined) or "- none"
    _verdict = "bitwise identical" if (_worst == 0.0 and _nulls == 0) else f"DIVERGED by {_worst}"
    # Flat markdown: zero-indent list lines inside an indented f-string defeat
    # marimo's dedent and turn the whole panel into a code block.
    _summary = (
        "## Is this the model the holdout evaluated?\n\n"
        "The page checks it now: it recomputes outputs recorded from the frozen champion and compares "
        "them in your browser.\n\n"
        "| | |\n|---|---|\n"
        f"| Delivery days compared | **{len(_days)}** |\n"
        f"| Quantile values compared | **{_cells}** |\n"
        f"| **Maximum absolute deviation** | **{_worst}** |\n"
        f"| Verdict | **{_verdict}** |\n"
    )
    _details = (
        "`mlflow.pyfunc` does not load under Pyodide, so what runs here is a re-implementation: the "
        "same nine boosters, the same preprocessing, the same four CQR thresholds and the same isotonic "
        "step, checked against outputs recorded from the frozen artifact and committed to the "
        "repository.\n\n"
        "| | |\n|---|---|\n"
        f"| Rows | **{_rows}** |\n"
        f"| Regimes and calendar cases covered | {', '.join(_regimes)} |\n"
        f"| Rows the frozen model left undefined, reproduced as undefined | **{_nulls == 0}** |\n\n"
        "Zero is float64 equality on every value compared, not a rounding of something small.\n\n"
        f"**{len(_undefined)} rows are undefined by design**, and are reproduced as undefined here "
        "rather than filled. In each, a calendar-day price lag lands on an hour a daylight-saving "
        "transition removed or repeated, and the pipeline fails closed instead of inventing a "
        "price:\n\n"
        f"{_undefined_md}\n\n"
        "The boosters were trained with LightGBM on macOS ARM and run here under a WebAssembly build "
        "with OpenMP disabled; their bitwise agreement is measured, not assumed."
    )
    mo.vstack([mo.md(_summary), mo.accordion({"How the check works": mo.md(_details)})])
    return


@app.cell
def _(CLAIMS, mo):
    # Flat markdown for the same reason as the table above: an indented block
    # interpolated into an indented f-string defeats marimo's dedent.
    _limits = "\n".join(f"- {CLAIMS[k]}" for k in sorted(CLAIMS) if k.startswith("limitation_"))
    mo.md(
        "## Limitations\n\n"
        + _limits
        + f"\n- {CLAIMS['floor_change']}\n\n"
        + f"> {CLAIMS['holdout_dm_label']}\n\n"
        + f"> {CLAIMS['holdout_limitation']}\n"
    )
    return


@app.cell
def _(CLAIMS, mo):
    # Item 4: this page necessarily reaches a CDN for Pyodide and its wheels, and
    # pulls the nine boosters from its own origin. Rather than describe that, it
    # reads its own Resource Timing entries -- from inside the worker, where the
    # Python packages are actually fetched -- and reports what it just cost you.
    def _network_report():
        try:
            import js
        except ImportError:
            return None
        try:
            entries = js.performance.getEntriesByType("resource")
        except Exception:
            return None
        hosts, requests, transferred = {}, 0, 0
        for entry in entries:
            try:
                name = str(entry.name)
                size = int(entry.transferSize or 0)
            except Exception:
                continue
            host = name.split("/")[2] if "//" in name else "(inline)"
            bucket = hosts.setdefault(host, {"n": 0, "bytes": 0})
            bucket["n"] += 1
            bucket["bytes"] += size
            requests += 1
            transferred += size
        return {"hosts": hosts, "requests": requests, "bytes": transferred}

    _report = _network_report()
    # Built with no leading indentation and passed as a value: an indented block
    # interpolated into an indented f-string breaks marimo's dedent and renders
    # the table as a code block.
    if _report is None:
        _network_md = "*(Network accounting is available only when this page runs in a browser.)*"
    else:
        _lines = ["| Host | Requests | Transferred |", "|---|---|---|"]
        _opaque = []
        for _host, _info in sorted(_report["hosts"].items(), key=lambda kv: -kv[1]["bytes"]):
            if _info["bytes"] == 0:
                # Cross-origin without `Timing-Allow-Origin`: the browser refuses
                # to report the size. Printing 0 B would be a measurement claim
                # nobody made, so say what is actually known.
                _opaque.append(_host)
                _size = "not disclosed by the browser (cross-origin)"
            else:
                _size = f"{_info['bytes']:,} B ({_info['bytes'] / 1048576:.1f} MiB)"
            _lines.append(f"| `{_host}` | {_info['n']} | {_size} |")
        _lines.append(
            f"| **measured total** | **{_report['requests']}** | "
            f"**{_report['bytes']:,} B ({_report['bytes'] / 1048576:.1f} MiB)** |"
        )
        if _opaque:
            _lines.append("")
            _lines.append(
                "The browser will not size cross-origin responses from "
                + ", ".join(f"`{h}`" for h in _opaque)
                + " (no Timing-Allow-Origin header); they are sized out-of-band and reported, "
                "with every other figure here, in the repository's network record."
            )
        _network_md = "\n".join(_lines)

    _intro = (
        f"The [report]({CLAIMS['pages_url']}) is a self-contained page with no additional runtime "
        "requests. This page downloads a Python runtime and the nine gradient-boosted models so the "
        "forecast is computed rather than replayed; the table shows what that cost in this browser "
        "session.\n\n"
    )
    # No claim about repeat visits is made here beyond what the record supports: a
    # repeat visit was not measured, and the figures quoted come from claims.py.
    _outro = (
        "\n\nMeasured in this browser session, from the Python runtime's own Resource "
        "Timing entries; the notebook interface is served from this Space alongside the "
        "page and is counted separately. For a first visit in full: "
        + CLAIMS["wasm_cold_load"]
    )
    mo.accordion({"What this page downloaded": mo.md(_intro + _network_md + _outro)})
    return


@app.cell
def _(CLAIMS, META, mo):
    _repro = "\n".join(f"- {CLAIMS[k]}" for k in sorted(CLAIMS) if k.startswith("repro_"))
    _trail = (
        f"{CLAIMS['wasm_what_runs_live']}\n\n"
        "Every link below was checked from an unauthenticated client. They use the `.mlflow` "
        "tracking host because the DagsHub repository interface sends an anonymous visitor to a "
        "sign-in page.\n\n"
        "| | |\n|---|---|\n"
        f"| [Experiment `{CLAIMS['mlflow_experiment_name']}`]({CLAIMS['mlflow_experiment_url']}) | every v1 run, side by side |\n"
        f"| [Model registry]({CLAIMS['mlflow_models_url']}) | the registered champion and its `champion` alias |\n"
        f"| [Tracking root]({CLAIMS['mlflow_url']}) | if a deep link ever moves, start here |\n"
        f"| [Source]({CLAIMS['github_url']}) | the repository, tests and evidence chain |\n\n"
        f"{CLAIMS['mlflow_next_note']}\n\n"
        "The four cutoffs are four different dates:\n\n"
        "| Cutoff | Value |\n|---|---|\n"
        f"| `snapshot_cutoff` | {CLAIMS['snapshot_cutoff']} |\n"
        f"| `raw_model_fit_cutoff` | {CLAIMS['raw_model_fit_cutoff']} |\n"
        f"| `final_calibration_window` | {CLAIMS['final_calibration_window']} |\n"
        f"| `holdout_window` | {CLAIMS['holdout_window']} |\n\n"
        f"{CLAIMS['shipped_is_evaluated']} Its raw-model fit cutoff precedes the snapshot cutoff by "
        f"{CLAIMS['staleness_days']} delivery days.\n\n"
        f"The artifact running here fingerprints to `{META['artifact_fingerprint_sha256']}`, the same "
        "value as `models/champion/champion_card.json`, the one-shot holdout report and the registered "
        "`champion` alias."
    )
    mo.vstack([
        mo.accordion({"Evidence and tracking": mo.md(_trail), "Reproducibility": mo.md(_repro)}),
        mo.md(CLAIMS["attribution"]),
    ])
    return


if __name__ == "__main__":
    app.run()
