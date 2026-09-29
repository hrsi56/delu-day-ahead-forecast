#!/usr/bin/env python3
"""Regenerate the README's CP-3 section from the one claim set (CP-3 item 5).

This section is the README's half of the cross-surface agreement bar. It carries
the claims item 5 binds, and the two paragraphs §7.1 and §6.2 require **verbatim**
in the report -- which lived only in `docs/cp2-model-report.md` until CP-3. Item 5
requires agreement across surfaces, and a claim that exists on one surface only
does not satisfy it.

    uv run python scripts/cp3_readme.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from delu_forecast import registry as G  # noqa: E402
from delu_forecast.claims import (  # noqa: E402
    MLFLOW_RUN_NAMES,
    build_claims,
    reproducibility_bullets,
)

README = ROOT / "README.md"
HEADING = "## CP-3 showcase and release"
NEXT_HEADING = "## Setup\n"


def build_section() -> str:
    C = build_claims()
    RUN_TABLE = "| Run name | What it decided |\n|---|---|\n" + "\n".join(
        f"| `{name}` | {what} |" for name, what in MLFLOW_RUN_NAMES
    )
    reproduction = "\n".join(f"- {bullet}" for bullet in reproducibility_bullets(C))
    released = G.released()
    return f"""{HEADING}

### Three public surfaces

Each one answers a different question, and each stands on its own. The static report is the primary link.

| | Surface | Answers | Cost to open |
|---|---|---|---|
| **1** | **[📄 Static report]({C["pages_url"]})**<br>the primary link | *Can they reason, and will they tell me what went wrong?* How the released model works, topic by topic — data, regimes, inputs, validation, results, explanations, failures, interval reliability, a forecast replay, limitations and how to run it — then the research history, newest first, and v1's original report preserved as an archive | One self-contained file with no additional runtime requests after it loads |
| **2** | **[⚡ Interactive Space]({C["space_url"]})**<br>[direct app]({C["space_app_url"]}) | *Does the thing actually run?* The champion's own boosters, running in your browser under Pyodide | about {C["wasm_cold_load_mb"]} MB first visit, {C["wasm_cold_load_requests"]} requests, {C["wasm_cold_load_hosts"]} hosts; ~1 MB after. A Static Space has no server-side process to sleep |
| **3** | **[🔬 MLflow on DagsHub]({C["mlflow_url"]})** | *Is the decision trail real, or is the README the only evidence?* Every decision-bearing run of v1, anonymously readable — no sign-in | — |

{C["wasm_identity"]} {C["wasm_wrapper_disclosure"]}

**Deployment.** {released.version} was released to GitHub Pages and the Static Space in {G.month(released.status.date)}. On 2026-07-08 Hugging
Face moved the Docker and Gradio SDKs behind a paid PRO plan and only Static Spaces stayed free, so
the containerised path could not be hosted at this project's ratified $0 rate. **The container is not
abandoned and not hypothetical** — it builds, and `make container-verify` runs it under
`docker run --network none` with every external host unreachable.

#### The decision trail, addressed directly

Every link below was checked from an **unauthenticated** client. The DagsHub *repository* UI redirects
an anonymous visitor to a sign-in page; the `.mlflow` tracking host does not, which is why every link
here uses it.

| | |
|---|---|
| **[Experiment `{C["mlflow_experiment_name"]}`]({C["mlflow_experiment_url"]})** | every v1 run, side by side |
| **[Model registry]({C["mlflow_models_url"]})** | the registered champion and its `champion` alias |
| **[Tracking root]({C["mlflow_url"]})** | if a deep link ever moves, start here |

Runs are named rather than linked by id, because several decision-bearing runs were reproduced and no
single id is canonical — the name is what to search for:

{RUN_TABLE}

**Tracking after v1.** {C["mlflow_next_note"]} [Generations, newest first](#generations-newest-first)
summarizes it.

**Run it yourself, offline:**

```bash
uv sync
uv run python predict_next_day.py --level 80 --self-check   # bundled snapshot, no network
uv run marimo run app/showcase.py                            # the container's showcase, server mode
make wasm && make wasm-serve                                 # the Static Space, at http://127.0.0.1:8820
docker build -t delu-showcase . && docker run -p 7860:7860 delu-showcase
make pages                                                   # rebuild docs/index.html
```

`--self-check` is not decoration: it re-runs the delivery day with its own prices masked and
requires bitwise-identical output, then mutates an in-window D−1 price and requires the output to
**move**. A boundary check that can only ever report "nothing changed" is satisfied by a broken
model, so the positive control is part of the check.

### What the shipped model is

`artifact_fingerprint_sha256` `{C["champion_fingerprint"]}` — the `{C["selected_catalog"]}` catalog's
{C["champion_features"]}-feature pipeline, {C["champion_quantiles"]} LightGBM quantile heads, four
CQR thresholds and isotonic last, in one `mlflow.pyfunc`. Snapshot `sha256`
`{C["snapshot_sha256"]}`. `python_model.pkl` is {C["champion_pkl_bytes"]} bytes =
{C["champion_pkl_size"]}; the whole `models/champion/` directory is {C["champion_dir_bytes"]} bytes
= {C["champion_dir_size"]}.

**The four cutoffs, identical on every surface:** snapshot `{C["snapshot_cutoff"]}` · raw-model fit
`{C["raw_model_fit_cutoff"]}` · final calibration `{C["final_calibration_window"]}` · holdout
`{C["holdout_window"]}`.

**The one-shot holdout, as published everywhere else:** MAE {C["holdout_mae_champion"]} vs
{C["holdout_mae_naive"]} ({C["holdout_mae_pct"]}); mean pinball {C["holdout_pinball_champion"]} vs
{C["holdout_pinball_naive"]} ({C["holdout_pinball_pct"]}); coverage {C["holdout_coverage_50"]} /
{C["holdout_coverage_80"]} / {C["holdout_coverage_95"]}; DM statistic {C["holdout_dm_statistic"]},
p {C["holdout_dm_p_value"]}, effect {C["holdout_dm_effect_size"]}. Selected catalog
`{C["selected_catalog"]}` (`{C["catalog_base_loss"]}` vs `{C["catalog_augmented_loss"]}`,
{C["catalog_pct"]}). Development evidence class `{C["development_evidence_class"]}`, with the
point-accuracy DM at p = {C["development_dm_point_p_value"]} — a deficit, not merely no advantage
({C["development_dm_point_relative"]}). Post-gate
benchmark `{C["benchmark_strict_loss"]}` → `{C["benchmark_a69_loss"]}`, **{C["benchmark_pct"]}**.

> {C["holdout_dm_label"]}

> {C["benchmark_limitation"]}

### The replay label is a truthfulness requirement

> {C["replay_label"]}

Anything the Space or the static page renders over the holdout window {C["holdout_window"]} is that
replay. It is never presented as a live forecast. The one scenario control is likewise labelled:

> {C["sensitivity_probe_label"]}

### Honest limitations

v1's limitations -- the two verbatim paragraphs and the complete set -- are in its section under
[Generations, newest first](#v1s-limitations), where every surface that presents v1 carries them
(Publication Standard v1 §8). None of this is engineered around; a floor-aware tail would reopen
scope this project deliberately closed.

### Reproducibility statement

§10 item (12) fixes what a complete one contains, and it too is rendered from one place onto every
surface:

{reproduction}

### Link discipline

Every link to the experiment tracking is the `.mlflow` URI. Verified from an unauthenticated client
on 2026-09-14: the DagsHub repository root, `/experiments`, `/models` and `/src/main` all answer
`302 → /user/login` for a connected repository, while <{C["mlflow_url"]}> serves real MLflow content
and live runs anonymously. A link to the repository UI would land a reader on a sign-in page, so
`tests/test_17_cross_surface_agreement.py` fails the build if one reappears on any surface.

"""


def main() -> int:
    section = build_section()
    text = README.read_text()
    if HEADING in text:
        head, _, rest = text.partition(HEADING)
        _, _, tail = rest.partition(NEXT_HEADING)
        text = head + section + NEXT_HEADING + tail
    else:
        text = text.replace(NEXT_HEADING, section + NEXT_HEADING, 1)
    README.write_text(text)
    print(f"regenerated the {HEADING!r} section of {README}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
