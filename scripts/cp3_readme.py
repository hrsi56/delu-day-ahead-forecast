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

from delu_forecast.claims import (  # noqa: E402
    build_claims,
    limitation_bullets,
    reproducibility_bullets,
)

README = ROOT / "README.md"
HEADING = "## CP-3 showcase and release"
NEXT_HEADING = "## Setup\n"


def build_section() -> str:
    C = build_claims()
    limitations = "\n".join(f"- {bullet}" for bullet in limitation_bullets(C))
    reproduction = "\n".join(f"- {bullet}" for bullet in reproducibility_bullets(C))
    return f"""{HEADING}

**Deployment status.** GitHub Pages is **live** at {C["pages_url"]} — the primary link, and it works
now. **The Hugging Face Space is built and verified locally but is not deployed, and the reason is a
platform change rather than an oversight.** On 2026-07-08 Hugging Face moved the Docker and Gradio
SDKs behind a paid PRO plan; only Static Spaces remain free. This project runs at a ratified $0 rate,
so the containerised showcase is not hosted there. **The container is not hypothetical** — it builds,
and `make container-verify` runs it under `docker run --network none` with every external host
unreachable. Run it yourself with the commands below; that is the same artifact a hosted Space would
have served. Steps, if the decision changes: [`docs/deploy.md`](docs/deploy.md).

**Three surfaces, one bundled artifact.** The champion is loaded from the image alongside the
committed snapshot — there is no registry lookup at runtime, no scheduled refresh, and no live
ENTSO-E/SMARD call during a user session. {C["shipped_is_evaluated"]}

| Surface | What it is | Runtime calls |
|---|---|---|
| **[Static report]({C["pages_url"]})** — the primary link | The full §10 reading order as one self-contained HTML file, CDN-served by GitHub Pages | **zero** |
| **[Interactive Space]({C["space_url"]})** | The marimo app in server mode, Docker SDK, `cpu-basic` | only its own assets |
| **[MLflow on DagsHub]({C["mlflow_url"]})** | Every decision-bearing run, anonymously readable | — |

The static page is the first touch precisely because it cannot sleep. The Space is labelled
*"{C["space_link_label"]}"* wherever it is linked, because the Hugging Face free tier sleeps after
inactivity; that is disclosed, not engineered around, and no keep-alive of any kind runs on any
platform.

**Run it yourself, offline:**

```bash
uv sync
uv run python predict_next_day.py --level 80 --self-check   # bundled snapshot, no network
uv run marimo run app/showcase.py                            # the showcase, server mode
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
point-accuracy DM at p = {C["development_dm_point_p_value"]} — no evidence of advantage. Post-gate
benchmark `{C["benchmark_strict_loss"]}` → `{C["benchmark_a69_loss"]}`, **{C["benchmark_pct"]}**.

> {C["holdout_dm_label"]}

> {C["benchmark_limitation"]}

### The replay label is a truthfulness requirement

> {C["replay_label"]}

Anything the Space or the static page renders over the holdout window {C["holdout_window"]} is that
replay. It is never presented as a live forecast. The one scenario control is likewise labelled:

> {C["sensitivity_probe_label"]}

### Honest limitations, stated here as well as on the page

§7.1 requires this paragraph verbatim in the report, and item 5 requires the surfaces to agree, so
it lives here too rather than in one document only:

> {C["holdout_limitation"]}

§6.2 requires this one verbatim, for the same reason:

> {C["exchangeability"]}

§10 item (11) fixes the complete set, and it is rendered from one place onto every surface — prose
written separately per surface is how a limitation ends up on one page and nowhere else:

{limitations}

And one on the environment: {C["floor_change"]} None of this is engineered around; a floor-aware
tail would reopen scope this project deliberately closed.

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
