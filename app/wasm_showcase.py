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
champion bitwise over 43 delivery days spanning all three regimes and a DST
transition — max |deviation| 0.0.

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

    return json, mo, np, read_json, read_text


@app.cell
def _(read_json, read_text):
    # The heavy cell: nine boosters, ~31 MB of text over the wire (far less
    # compressed). Everything else is small.
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
        label: lgb.Booster(model_str=read_text(f"boosters/{label}.txt"))
        for label in META["quantile_labels"]
    }
    CHAMPION = BrowserChampion(BOOSTERS, META, SERIES, CALENDAR)
    return CHAMPION, CLAIMS, FIXTURE, META


@app.cell
def _(CLAIMS, META, mo):
    mo.md(
        f"""
        # DE-LU day-ahead price forecasting — running in your browser

        Every number below is computed **here**, by the champion itself: nine LightGBM
        quantile heads, CQR calibration, isotonic last, executing in WebAssembly. There
        is no server. Nothing is precomputed and replayed at you.

        > **{CLAIMS['replay_label']}**

        This page is the interactive deep dive. The
        [static report]({CLAIMS['pages_url']}) is the primary entry point; the decision
        trail is public at [MLflow on DagsHub]({CLAIMS['mlflow_url']}).

        **The four cutoffs, stated separately because they are four different dates:**

        | Cutoff | Value |
        |---|---|
        | `snapshot_cutoff` | {CLAIMS['snapshot_cutoff']} |
        | `raw_model_fit_cutoff` | {CLAIMS['raw_model_fit_cutoff']} |
        | `final_calibration_window` | {CLAIMS['final_calibration_window']} |
        | `holdout_window` | {CLAIMS['holdout_window']} |

        {CLAIMS['shipped_is_evaluated']} Its raw-model fit cutoff precedes the snapshot
        cutoff by {CLAIMS['staleness_days']} delivery days.

        The artifact running above you fingerprints to
        `{META['artifact_fingerprint_sha256']}` — the same value in
        `models/champion/champion_card.json`, in the one-shot holdout report, and on the
        registered `champion` alias.
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
        label="Load-forecast scenario (× the delivery day's A65 vector)",
        show_value=True,
    )
    mo.hstack([level, load_scale], justify="start", gap=2)
    return level, load_scale


@app.cell
def _(np):
    PAIRS = {50: ("p25", "p75"), 80: ("p10", "p90"), 95: ("p025", "p975")}

    def fan_svg(hours, low, mid, high, actual=None, width=920, height=380):
        """Inline SVG, built here rather than by matplotlib.

        matplotlib's wheel is several megabytes in Pyodide and this page already
        asks a visitor to download nine boosters. A fan chart is two polylines
        and a polygon; it does not justify the dependency.
        """
        ml, mr, mt, mb = 58, 16, 20, 34
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
            ticks.append(round(float(value), 2))
            value += step

        parts = [f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
                 f'role="img" aria-label="Quantile fan chart" style="width:100%;height:auto;'
                 f'background:#fff;border:1px solid #d7dee6;border-radius:8px">']
        for tick in ticks:
            colour = "#9aa7b4" if tick == 0 else "#eceff3"
            parts.append(f'<line x1="{ml}" x2="{width-mr}" y1="{Y(tick):.1f}" y2="{Y(tick):.1f}" '
                         f'stroke="{colour}" stroke-width="{1.2 if tick == 0 else 1}"/>')
            parts.append(f'<text x="{ml-8}" y="{Y(tick)+4:.1f}" text-anchor="end" '
                         f'fill="#5a6a7a" font-size="11">{tick:g}</text>')
        for i in range(0, n, 2):
            parts.append(f'<text x="{X(i):.1f}" y="{height-12}" text-anchor="middle" '
                         f'fill="#5a6a7a" font-size="11">{hours[i]}</text>')
        band = [f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(high) if v == v]
        band += [f"{X(i):.1f},{Y(v):.1f}" for i, v in reversed(list(enumerate(low))) if v == v]
        parts.append(f'<polygon points="{" ".join(band)}" fill="#3a6ea5" fill-opacity="0.22"/>')
        line = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(mid) if v == v)
        parts.append(f'<polyline points="{line}" fill="none" stroke="#1b3a5c" stroke-width="2.2"/>')
        if actual is not None:
            obs = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(actual) if v == v)
            parts.append(f'<polyline points="{obs}" fill="none" stroke="#b03a2e" '
                         f'stroke-width="1.6" stroke-dasharray="6 4"/>')
        parts.append(f'<text x="{ml}" y="{mt-6}" fill="#5a6a7a" font-size="11">'
                     f'EUR/MWh · local hour (Europe/Berlin)</text></svg>')
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

    mo.vstack([
        mo.Html(fan_svg(_hours, _low, _mid, _high, _actual)),
        mo.md(_note),
        mo.md(
            f"Recomputed in your browser just now: {int(np.isfinite(_final).all(axis=1).sum())} "
            f"hours × 9 quantiles, {len(_labels)} heads, CQR then isotonic."
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
    _verdict = "bitwise identical" if (_worst == 0.0 and _nulls == 0) else f"DIVERGED by {_worst}"
    mo.md(
        f"""
        ## Is this really the model the holdout evaluated?

        `mlflow.pyfunc` does not load under Pyodide, so what runs here is a
        re-implementation: the same nine boosters, the same preprocessing, the same four
        CQR thresholds, the same isotonic step. That makes the claim *"the shipped model
        is exactly the model the holdout evaluated"* something to prove rather than
        repeat — so the check runs in your browser, now, against outputs recorded from
        the frozen artifact before this page existed.

        | | |
        |---|---|
        | Delivery days compared | **{len(_days)}** |
        | Rows | **{_rows}** |
        | Quantile values compared | **{_cells}** |
        | Regimes covered | {", ".join(_regimes)} |
        | Rows the frozen model left undefined, reproduced as undefined | **{_nulls == 0}** |
        | **Maximum absolute deviation** | **{_worst}** |
        | Verdict | **{_verdict}** |

        Zero is not a rounding of something small — it is float64 equality on every one
        of those values. The two undefined rows are the spring-forward day, where the
        D−1 calendar-day lag has no source hour and the pipeline fails closed instead of
        inventing a price; this page reproduces the gap rather than filling it.

        The boosters were trained with LightGBM on macOS ARM and are executing here under
        a WebAssembly build with OpenMP disabled. That they agree bitwise is a measured
        result, not an assumption — it was the first thing established, because it was
        the one thing that could have made this page impossible.
        """
    )
    return


@app.cell
def _(mo):
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
                "Sizes from " + ", ".join(f"`{h}`" for h in _opaque) + " are small wheel "
                "requests the browser will not size for a cross-origin response; they are "
                "measured out-of-band and reported in the repository."
            )
        _network_md = "\n".join(_lines)

    _intro = (
        "## What this page downloaded\n\n"
        "The [static report](https://hrsi56.github.io/delu-day-ahead-forecast/) fetches "
        "**nothing** — it is the first-touch link precisely because it cannot fail when a "
        "CDN does. This page is the opposite trade: it downloads a Python runtime and the "
        "nine gradient-boosted models so the inference is real rather than replayed, and "
        "the honest thing to do with that cost is print it.\n\n"
    )
    _outro = (
        "\n\nMeasured in this browser session, from the Python runtime's own Resource "
        "Timing entries. The notebook interface is served from this Space alongside the "
        "page and is counted separately. A repeat visit is served from your browser cache."
    )
    mo.md(_intro + _network_md + _outro)
    return


@app.cell
def _(CLAIMS, mo):
    # Flat markdown for the same reason as the table above: an indented block
    # interpolated into an indented f-string defeats marimo's dedent.
    _limits = "\n".join(f"- {CLAIMS[k]}" for k in sorted(CLAIMS) if k.startswith("limitation_"))
    _repro = "\n".join(f"- {CLAIMS[k]}" for k in sorted(CLAIMS) if k.startswith("repro_"))
    mo.md(
        "## Honest limitations\n\n"
        + _limits
        + f"\n- {CLAIMS['floor_change']}\n\n"
        + f"> {CLAIMS['holdout_dm_label']}\n\n"
        + f"> {CLAIMS['holdout_limitation']}\n\n"
        + "## Reproducibility\n\n"
        + _repro
        + f"\n\n{CLAIMS['attribution']}\n"
    )
    return


if __name__ == "__main__":
    app.run()
