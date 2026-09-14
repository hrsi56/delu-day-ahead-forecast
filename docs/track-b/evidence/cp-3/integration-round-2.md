# Verdict — M3/CP-3 — Integration — FAIL

- Candidate SHA: 4d0fdb029e762c2f3aa04041a5afcd62f0386913
- Plan / version / bar: capstone_V6_8.md, v6.8, §12 "CP-3 (6 items)"
- Verbatim bar excerpt (confirmed present in `capstone_V6_8.md` at this SHA, §12 → "M3 — Showcase and release"):

  > **CP-3 (6 items)**
  > - [ ] Bundled champion, CLI (`predict_next_day.py`), container, and marimo app run locally from a clean setup. The champion is registered as a DagsHub MLflow **model version with the `champion` alias** and release/lineage tags — **non-gating**: a registry or metadata-operation outage does not block release and is disclosed.
  > - [ ] The quantile-level selector and at most one simple load-forecast scenario control work, served by direct local inference or a one-dimensional lookup — with no multidimensional precomputed grid, dynamic SHAP, or per-cell OOD system. Scenario perturbations are labeled sensitivity probes that may be out of distribution.
  > - [ ] Static Pages export carries the §10 reading order, performs **zero runtime calls** to the Space or any external service, and renders every asset and link.
  > - [ ] HF Space deploys the **bundled** champion — the same artifact the holdout evaluated — and renders the same release snapshot. Free-tier sleep is disclosed, not performance-gated. Anything the Space shows over the holdout period is labeled **historical out-of-sample replay** on the page itself, never presented as a live forecast.
  > - [ ] README, Pages, Space metadata and MLflow links agree on the selected catalog, metrics, development evidence class, benchmark limitation, champion identity, and the holdout result with its power-qualification label and the statement that the shipped model is the evaluated model. **All four cutoffs — snapshot, raw-model fit, final calibration, holdout — appear separately and identically on every surface.** Limitations and reproduction instructions are complete.
  > - [ ] **One fresh Integration Critic returns `PASS`** on the final candidate from a clean detached checkout, with a verdict-only delta to the evidence tip.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.
  For reference only, it sits at lines 483–489 of `capstone_V6_8.md`.)
- Worktree clean before and after: **yes** (`git -C /tmp/critic-cp-3 status --porcelain` empty at both
  ends; `rev-parse HEAD` = `4d0fdb029e762c2f3aa04041a5afcd62f0386913` unchanged). The only additions
  inside the worktree are gitignored byproducts: `.venv/`, `.pytest_cache/`, `app/__marimo__/`,
  `**/__pycache__/`. All scratch work (scratch repo copy, logs, container JSON) was kept outside the
  worktree. `/Users/djourno/Downloads/PJM` was never read, run or inspected.

## Commands actually run

| # | Command | Exit | Observed output |
|---|---|---|---|
| 1 | `git -C /tmp/critic-cp-3 status --porcelain` | 0 | empty (clean) |
| 2 | `git -C /tmp/critic-cp-3 rev-parse HEAD` | 0 | `4d0fdb029e762c2f3aa04041a5afcd62f0386913` |
| 3 | `cd /tmp/critic-cp-3 && uv sync --locked --dev` | 0 | full locked dev env resolved and installed |
| 4 | `uv run pytest -q` | 0 | `136 passed in 82.38s` — matches the claimed 136 |
| 5 | `MLFLOW_DISABLE_AGENT_HINT=1 uv run python predict_next_day.py --level 80 --self-check` | 0 | `passed: True`; `delivery_day_prices_change_nothing: True`; `max_abs_difference_when_masked: 0.0`; `positive_control_d_minus_1_changes_output: True`; `max_abs_difference_positive_control: 220.9433340396028`. Header prints `source : bundled data/snapshot.parquet (no network)` and fingerprint `57e3ad40…` |
| 6 | `uv run python scripts/verify_release.py` | 0 | `PASS — every bound claim agrees on all four surfaces; the page fetches nothing`; `disagreements: none`; `gated DagsHub UI links on any surface: none` |
| 7 | `uv run python scripts/verify_container.py --out /tmp/critic-container.json` | 0 | `passed: true`; all five steps ok: `build`, `run_offline`, `offline_probe`, `cli_offline`, `marimo_server_mode`. Ran with `--network none`: `outbound_network: unreachable (OSError)`, `huggingface.co`/`dagshub.com`/`cdn.jsdelivr.net` all unreachable; in-container `app_health_status: 200`, `{"status":"healthy"}`; in-container CLI self-check `exit_code: 0`, both halves true. Image `delu-showcase:verify`, 1.66 GB, Docker server 29.5.2 |
| 8 | `uv run marimo run app/showcase.py --headless --port 8891 --no-token` | served | `curl http://127.0.0.1:8891/health` → **200** `{"status":"healthy"}`; `GET /` → 200, 24,083 bytes |
| 9 | `curl -s "https://dagshub.com/…delu-day-ahead-forecast.mlflow/api/2.0/mlflow/registered-models/alias?name=delu-day-ahead-champion&alias=champion"` (anonymous, no credential) | 0 | HTTP 200, JSON: `version:"1"`, `status:"READY"`, `aliases:["champion"]`, `run_id:"83e475627b6646c885c70f9010c8cf2e"`, 35 tags |
| 10 | `curl -s -o /dev/null -w "%{http_code}" https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast` | 0 | **401** |
| 11 | `curl -s https://huggingface.co/api/spaces/hrsi56/delu-day-ahead-forecast` | 0 | **401** `{"error":"Invalid username or password."}` |
| 12 | `curl -s "https://huggingface.co/api/spaces?author=hrsi56"` | 0 | HTTP 200, body `[]` — **zero spaces for this author** |
| 13 | `curl -s https://huggingface.co/api/users/hrsi56/overview` | 0 | **404** `{"error":"This user does not exist"}` |
| 14 | `curl -s -o /dev/null -w "%{http_code}" https://huggingface.co/hrsi56` | 0 | **404** |
| 15 | `curl -s -o /dev/null -w "%{http_code}" https://hrsi56-delu-day-ahead-forecast.hf.space/` | 0 | **404** |
| 16 | `curl -s -o /dev/null -w "%{http_code}" "https://hrsi56.github.io/delu-day-ahead-forecast/?cb=…"` | 0 | **404** (also `https://hrsi56.github.io/` → 404) |
| 17 | `curl -s -o /dev/null -w "%{http_code}" https://github.com/hrsi56/delu-day-ahead-forecast` | 0 | 200 |
| 18 | Scratch-copy break A: in a copy **outside** the worktree (`/tmp/critic-scratch`, own `uv sync`), moved the rolling right edge from `boundary - 1h` to `boundary + 22h` in `src/delu_forecast/features.py` (admits delivery-day D prices), then `uv run pytest -q tests/test_18_showcase_gate_boundary.py` | 1 | **4 failed, 5 passed** — `test_delivery_day_prices_change_nothing_and_a_d_minus_1_price_does`, `test_truncated_history_reproduces_the_whole_snapshot_bitwise`, `test_the_boundary_holds_across_a_run_of_delivery_days`, `test_showcase_output_is_monotone_at_every_level` |
| 19 | Scratch-copy break B: injected `<script src="https://cdn.jsdelivr.net/npm/chart.js">` into the scratch `docs/index.html`, then `uv run pytest -q tests/test_19_static_page_is_offline.py` | 1 | **3 failed, 17 passed** — `test_zero_runtime_calls`, `test_the_only_scripts_are_inline` both fail with `Finding(kind='<script src>', detail='https://cdn.jsdelivr.net/npm/chart.js')` |
| 20 | Independent metric recomputation from `reports/cp2/holdout_predictions.parquet` | 0 | every headline number reproduced (table below) |
| 21 | Independent fingerprint recomputation from the loaded pyfunc | 0 | `57e3ad40a7f48bb7896628ce2e5dec61314dea567da9867aede4bf1b0a10e0fb` |
| 22 | Browser load of `docs/index.html` (served at `127.0.0.1:8892`), network + console log read | — | network log: exactly **one** request, `GET /index.html → 200`. Zero further requests, including after driving both controls. Console: no logs, no errors |

Note on command 18: my first attempt at that break was **invalid and I discarded it** — the scratch copy
initially symlinked the worktree `.venv`, whose editable install resolved `delu_forecast` back to
`/tmp/critic-cp-3/src`, so the patched module was never imported and the suite "passed" meaninglessly.
I rebuilt an isolated venv in the scratch copy, confirmed
`delu_forecast.features.__file__ == /private/tmp/critic-scratch/src/delu_forecast/features.py`, and only
then recorded the result above. I am flagging it because a critic who had not checked would have reported
a false negative control.

## Evidence actually inspected

**Plan.** `capstone_V6_8.md` — §12 M3 bar (confirmed verbatim), §5.2 (delivery-day availability
invariant), §6.2 (CQR order, exchangeability paragraph), §7.1 (one-shot holdout, four cutoffs, required
limitation paragraph, DM label), §7.2 (post-gate benchmark), §9.1 (registration, non-gating), §9.2
(bundled champion, controls, replay label, static page), §9.3 (reproducibility, cutoff disclosure),
§9.6 (DuckDB), §10 (twelve-item reading order, item 11 limitations, item 12 reproducibility), §10.1.

**Artifacts.** `models/champion/champion_card.json`; `models/champion/MLmodel`;
`reports/cp2/holdout_report.json`; `reports/cp2/catalog_selection.json`; `reports/cp2/a69_benchmark.json`;
`reports/cp2/dm_development.json`; `reports/cp2/holdout_predictions.parquet` (2,160 rows × 30 cols, read
and recomputed); `reports/cp3/mlflow_registration.json`; `reports/cp3/container_check.json`;
`reports/cp3/pages_build.json`; `reports/cp3/link_check.json`; `reports/cp3/space_bundle.json`.

**Surfaces.** `README.md` (288 lines, read in full); `docs/index.html` (424 lines / 1,004,780 bytes —
raw HTML read directly, plus rendered in a browser); `space/README.md` (142 lines, read in full);
`docs/deploy.md`; the live MLflow registered-model record (fetched anonymously).

**Code.** `src/delu_forecast/showcase.py` (read in full — the single `gate_feasible_frame` enforcement
point), `src/delu_forecast/model.py` (`predict_stages`, `fingerprint`, `CHAMPION_INPUT_COLUMNS`,
runtime firewall), `src/delu_forecast/features.py` (`_daily_price_statistics` D-1 boundary),
`predict_next_day.py` (read in full — both bundled and fresh modes, `self_check`), `app/showcase.py`
(controls, chart cell), `scripts/build_pages.py` (header), `tests/test_18_showcase_gate_boundary.py`
(read in full), `tests/test_19_static_page_is_offline.py`.

**Figures / assets.** All 7 `<img>` on the Pages export confirmed loaded in-browser
(`complete && naturalWidth > 0` for all 7, zero broken); all 7 are `data:image/png;base64` — the three
§4.2 spectral figures, the SHAP summary, two SHAP dependence plots, and the three-stage reliability
diagram. The §10 item (10) fan chart is an inline SVG that drew 23 child nodes.

### Independent metric recomputation (from the committed per-row predictions)

| Quantity | Recomputed by me | `holdout_report.json` | Match |
|---|---|---|---|
| champion MAE | 25.907780440955044 | 25.907780440955044 | yes |
| champion mean pinball | 6.708294915819918 | 6.708294915819919 | yes (1 ulp) |
| similar-day-naive MAE | 27.75776736111111 | 27.75776736111111 | yes |
| similar-day-naive mean pinball | 13.878883680555555 | 13.878883680555557 | yes (1 ulp) |
| MAE % difference | -6.664754034749622 | -6.664754034749622 | yes |
| pinball % difference | -51.66545761012248 | -51.66545761012248 | yes |
| final coverage 50 / 80 / 95 | 0.44074074074074077 / 0.7592592592592593 / 0.9398148148148148 | identical | yes |
| final-stage crossing violations | 0 | 0 | yes |
| rows / days / window | 2,160 / 90 / 2026-06-09..2026-09-06 | identical | yes |
| artifact fingerprint (from loaded pyfunc) | 57e3ad40…a10e0fb | identical in card **and** holdout report | yes |

### Cross-surface agreement table (built by me, not taken from `verify_release.py`)

Every value below was grepped out of each surface independently and checked against the unrounded
committed artifact. **No surface rounds any number differently from any other.**

| Claim | Artifact (unrounded) | README | Pages | Space card | MLflow tag |
|---|---|---|---|---|---|
| selected catalog | `base` | base | base | base | base |
| catalog base loss | 13.015841509664993 | same | same | same | same |
| catalog augmented loss | 13.064197422052183 | same | same | same | same |
| catalog % diff | 0.3715158359241209 | +0.371516% | +0.371516% | +0.371516% | +0.371516% |
| holdout MAE champion / naive | 25.9077804… / 27.7577673… | 25.9078 / 27.7578 | same | same | same |
| holdout MAE % | -6.664754… | -6.66% | -6.66% | -6.66% | -6.66% |
| holdout pinball champion / naive | 6.7082949… / 13.8788836… | 6.7083 / 13.8789 | same | same | same |
| holdout pinball % | -51.665457… | -51.67% | -51.67% | -51.67% | -51.67% |
| coverage 50/80/95 | 0.440740… / 0.759259… / 0.939814… | 0.4407 / 0.7593 / 0.9398 | same | same | same |
| DM statistic / p / effect | -8.6798484… / 1.9814819e-18 / -1.0477562… | -8.6798 / 1.98e-18 / -1.0478 | same | same | same |
| development evidence class | development_post_selection | present | present | present | present |
| development point-DM p | 0.9476866135947211 | 0.948 | 0.948 | 0.948 | 0.948 |
| benchmark strict → A69 loss, % | 13.0158415… → 10.4787146…, -19.492607… | same, -19.4926% | same | same | same |
| benchmark limitation paragraph | verbatim | yes | yes | yes | yes |
| champion fingerprint | 57e3ad40…a10e0fb | yes | yes | yes | yes |
| snapshot sha256 | 7dd2dc73…f697f00 | yes | yes | yes | yes |
| `snapshot_cutoff` | 2026-09-06 | yes | yes | yes | yes |
| `raw_model_fit_cutoff` | 2026-04-07 | yes | yes | yes | yes |
| `final_calibration_window` | 2026-04-09..2026-06-07 | yes | yes | yes | yes |
| `holdout_window` | 2026-06-09..2026-09-06 | yes | yes | yes | yes |
| shipped-is-evaluated statement | — | yes | yes | yes | yes |
| §7.1 power-qualification label | verbatim | yes | yes | yes | yes |
| §7.1 holdout limitation paragraph | **verbatim** | yes | yes | yes | — |
| §6.2 exchangeability paragraph | **verbatim** | yes | yes | yes | — |
| replay label | verbatim | yes | yes | yes | — |
| sensitivity-probe label | verbatim | yes | yes | yes | — |

All four cutoffs appear **separately and identically** on all four surfaces. Both plan-mandated verbatim
paragraphs (§7.1 holdout limitation, §6.2 exchangeability) were matched by exact normalized substring
comparison — not by keyword — and are present on all three human surfaces.

**§10 item (11) limitations — present on all three surfaces, none on only some:** exchangeability under
regime shift; development-versus-one-shot evidence; disclosed assumption (A65 load forecast); disclosed
assumption (A75 generation archive); measured cost of the strict gate; two-sided bounded target live at
the floor; coverage divergence; model staleness with all four cutoffs; the 15-minute MTU averaging
choice; scope. (The Space card additionally carries a "Scenario probes" bullet.) All ten checked by
exact substring on each surface: 10/10 × 3/3.

**Link discipline:** six DagsHub references across the three surfaces, and **all six** are
`https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow`. Zero occurrences of a gated UI path
(`/experiments`, `/models`, `/src`, `/annotations`, or the bare repo root) on any surface. Confirmed
in-browser: the rendered Pages export resolves to exactly three external hosts — the `.mlflow` URI, the
GitHub repo, and the HF Space.

### §5.2 delivery-day availability invariant

`src/delu_forecast/showcase.py` is the single assembly point; `predict_next_day.py` and `app/showcase.py`
both route through `gate_feasible_frame`, which (a) drops every row dated after the target delivery day,
(b) sets every `price_eur_mwh` on the target day to NaN, and (c) projects to the five admissible raw
columns before the model's own runtime firewall re-checks. `_daily_price_statistics` anchors each rolling
window at `midnight(D) Berlin → UTC, minus 1h`, per delivery day, producing one value broadcast to the
whole curve — a D-1 boundary, not a row-wise `t−1`. The scenario probe scales only the target day's
`load_forecast_mw`; derived columns are rebuilt from it, so the probe is internally consistent, and it
touches no price and no other delivery day.

I did not take the green suite as evidence. I verified the two decisive controls are real by breaking a
copy **outside** the worktree (commands 18 and 19): a boundary that reaches into delivery day D makes four
`test_18` assertions fail, and an injected external `<script src>` makes `test_19` fail. Both controls
bite. I also confirmed the CLI self-check is genuinely paired in source, not just in its printed output.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Bundled champion, CLI, container, marimo app run locally from a clean setup; champion registered as a DagsHub MLflow model version with the `champion` alias and release/lineage tags (non-gating) | **PASS** | `uv sync --locked --dev` exit 0; `pytest -q` → 136 passed; CLI self-check exit 0 with `passed: True`, masked diff `0.0`, positive control `220.94`; champion loaded by `mlflow.pyfunc.load_model("models/champion")` — a local directory, no registry call (§9.2 dual path absent from source); marimo `/health` → 200; `verify_container.py` → `passed: true`, all five steps ok, container run with `--network none` and still healthy. Registry checked by me anonymously with no credential: version `1`, `aliases:["champion"]`, `status:"READY"`, 35 tags including `release_status=portfolio_release`, `source_run_id`, `code_commit`, `snapshot_sha256` and all four cutoffs; its `artifact_fingerprint_sha256` tag equals `models/champion/champion_card.json` **and** the fingerprint I recomputed from the loaded pyfunc |
| 2 | Quantile-level selector and at most one scenario control work, by direct local inference or 1-D lookup; no multidimensional grid, dynamic SHAP or per-cell OOD; sensitivity-probe label present | **PASS** | Exactly two controls on each surface and both are the permitted ones. marimo: `mo.ui.radio` (50/80/95) + `mo.ui.slider` (0.90–1.10); the three `mo.ui.table` calls are `selection=None`, non-interactive. Pages: one `name='lvl'` radio group (3 inputs) + one `<input id="scale" type="range" min=0 max=10>`. **They work, not merely exist:** driving inference directly, mean interval width rises strictly 40.06 (50 %) → 83.04 (80 %) → 145.93 (95 %), and `load_scale` 0.90→1.10 moves p50 (mean 67.357 → 68.882); in-browser, both controls redraw the SVG, the coverage readout switches to 0.9398 at 95 %, and the scenario note appears when scaled off 1.00. Pages uses a **one-dimensional** lookup — 11 load-scale keys, each holding the 9 already-computed quantiles; the level selector picks two of those nine, so there is no second precomputed axis. No SHAP computation, no OOD logic and no grid in `app/showcase.py`, `showcase.py` or the page's two inline scripts; SHAP appears only as committed static PNG/CSV. The probe label is verbatim on all three surfaces |
| 3 | Static Pages export carries the §10 reading order, performs zero runtime calls, renders every asset and link | **PASS** (with a publication caveat, below) | All twelve §10 items present as headings: 1 · The data; 2 · Three regimes; 3 · Feature catalog; 3b · Spectral view (three labeled figures + interpretation); 4 · Validation design; 5 · Results (development DM, two-arm comparison, one-shot holdout, post-gate benchmark); 6–7 · Explainability (SHAP summary + top-10 + two dependence plots, and permutation importance); 8 · Regime-stratified error; 9 · Reliability three stages; 10 · Next-day forecast; 11 · Honest limitations; 12 · Reproducibility. **Zero runtime calls verified two independent ways, neither of them `static_audit.py`:** (i) reading the raw HTML — no `<link>`, no `<script src>`, no `<iframe>/<embed>/<object>/<video>/<audio>/<source>`, no `srcset`, no `@import`, no `url(`, no `@font-face`, no `fetch(`/`XMLHttpRequest`/`WebSocket`/`EventSource`/`sendBeacon`/dynamic `import(`; both `<script>` blocks inline; all 7 `<img>` are `data:` URIs; the only `http://` string is the SVG XML namespace; (ii) loading it in a browser — the network log shows exactly one request (the page), and still exactly one after exercising both controls. Assets render: 7/7 images loaded, 0 broken; the fan-chart SVG drew. 16 anchors resolve to three external hosts. **Caveat, not scored against this item:** the export is not actually published — `https://hrsi56.github.io/delu-day-ahead-forecast/` returns 404 — so the recruiter-facing URL §9.2/§10 designate as the canonical entry point does not exist yet. I scored the item on the three properties the bar enumerates, which §10.1 also names as "what CP-3 verifies", and all three hold for the committed artifact |
| 4 | HF Space deploys the **bundled** champion — the same artifact the holdout evaluated — and renders the same release snapshot; free-tier sleep disclosed, not performance-gated; holdout-period content labeled historical out-of-sample replay | **FAIL** | **There is no Hugging Face Space, and no Hugging Face account to hold one.** `https://huggingface.co/api/users/hrsi56/overview` → 404 `{"error":"This user does not exist"}`; `https://huggingface.co/hrsi56` → 404; `https://huggingface.co/api/spaces?author=hrsi56` → 200 with body `[]`; `https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast` → 401; the runtime host `https://hrsi56-delu-day-ahead-forecast.hf.space/` → 404. The repository states this itself in `README.md` ("the Space is not yet created, so the two links below do not resolve yet"), in `docs/deploy.md` §2a, and in `reports/cp3/link_check.json` (`unresolved_reason`). Nothing deploys the champion, so the item's principal clause is unmet. **The sub-parts I could check all hold:** the bundle is assembled (`reports/cp3/space_bundle.json`, 37,097,867 bytes, Docker SDK, port 7860, includes `models/champion` and `data/snapshot.parquet`); the image builds and serves marimo healthily with `--network none`; the bundled artifact **is** the evaluated one — I recomputed the fingerprint from the loaded pyfunc as `57e3ad40a7f48bb7896628ce2e5dec61314dea567da9867aede4bf1b0a10e0fb`, equal to both `champion_card.json` and `reports/cp2/holdout_report.json`; the replay label is verbatim on the Space card and above the chart on both other surfaces; free-tier sleep is disclosed ("~30 s to wake if asleep") and is explicitly not performance-gated (§9.2's timing thresholds are retired, and `verify_container.py` applies no timing gate). The item still fails, because a Space card in the repository is not a deployed Space |
| 5 | README, Pages, Space metadata and MLflow links agree on catalog, metrics, evidence class, benchmark limitation, champion identity, holdout result with power-qualification label and shipped-is-evaluated statement; all four cutoffs separately and identically everywhere; limitations and reproduction instructions complete | **FAIL** (narrowly — one enumerated element missing) | **Everything about agreement passes,** on my own table above and not on `verify_release.py`: 25 claim rows agree across all four surfaces with identical rounding and no surface rounding differently; all four cutoffs separate and identical on all four; both verbatim paragraphs (§7.1, §6.2) matched exactly on all three human surfaces; all ten §10 item (11) limitations present on README **and** Space card **and** Pages, none on only some; all six DagsHub links are the `.mlflow` URI with zero gated UI paths; every metric traced back to a recomputation from the committed per-row predictions. **The one gap:** §10 item (12) enumerates the reproducibility statement's required contents as "tagged commit, DagsHub MLflow permalinks **and the registered `champion` alias**, the static GitHub Pages URL …, the DuckDB SQL queries, the four cutoffs, and CC BY attribution." The registered `champion` alias — and the registered model name `delu-day-ahead-champion` — appear on **none** of the three surfaces (zero matches for "champion alias", "alias", "registered model" or "delu-day-ahead-champion" in `README.md`, `docs/index.html`, `space/README.md`). It exists only in `docs/deploy.md`, which is not a release surface, and in the live registry. Every other item-(12) element is present on the Pages export. This is a narrow, one-line omission and I record it as such, but it is a named, enumerated element of a completeness requirement, and it is absent everywhere the requirement applies |
| 6 | One fresh Integration Critic returns `PASS` on the final candidate from a clean detached checkout, with a verdict-only delta to the evidence tip | **FAIL** | This is that verdict, and it is **FAIL**. Reviewed read-only from the clean detached worktree `/tmp/critic-cp-3` at `4d0fdb029e762c2f3aa04041a5afcd62f0386913`, clean before and after, with no builder's story, diff or summary consulted, and with this file written outside the worktree |

## On FAIL only

- **Single largest meaningful gap.** Item 4 requires a deployed Hugging Face Space serving the bundled
  champion, and no Space exists — the `hrsi56` Hugging Face account itself does not exist, so the Space
  cannot exist. GitHub Pages is likewise not enabled, leaving both published surfaces unreachable. Every
  artifact that *would* be deployed is built, verified, offline-capable and internally consistent; what is
  missing is the publication step, which `docs/deploy.md` correctly identifies as owner-only (account
  creation and credential entry are not steps an agent may perform). A secondary, much smaller gap: the
  registered `champion` alias that §10 item (12) requires in the reproducibility statement is absent from
  all three release surfaces.

- **Exact next acceptance test.** From a fresh clean detached checkout of the new candidate, all of the
  following, with no credential supplied to the critic:
  1. `curl -s -o /dev/null -w "%{http_code}" https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast`
     returns **200**, and `curl -s "https://huggingface.co/api/spaces?author=hrsi56"` returns a non-empty
     array containing `delu-day-ahead-forecast`.
  2. The running Space serves the app, and the fingerprint it reports equals
     `57e3ad40a7f48bb7896628ce2e5dec61314dea567da9867aede4bf1b0a10e0fb` — recomputed from the deployed
     pyfunc, not read from a card — matching `models/champion/champion_card.json` and
     `reports/cp2/holdout_report.json`.
  3. The rendered Space page carries the verbatim string
     `Historical out-of-sample replay — the frozen champion forecasting a 90-day period it never trained on. This is not a live forecast.`
     and the free-tier sleep disclosure, and both controls respond.
  4. `curl -s -o /dev/null -w "%{http_code}" https://hrsi56.github.io/delu-day-ahead-forecast/` returns
     **200**, and that served page is byte-identical to the committed `docs/index.html`, still producing
     exactly one network request when loaded in a browser.
  5. `reports/cp3/link_check.json` re-run reports `unresolved: []`.
  6. The README's "Deployment status — read this before clicking" paragraph is deleted (it asserts the
     links do not resolve, and would contradict 1 and 4).
  7. The registered `champion` alias — `delu-day-ahead-champion`, alias `champion` — appears in the
     reproducibility statement on the README, the Pages export **and** the Space card, per §10 item (12).
  8. `uv sync --locked --dev && uv run pytest -q` still reports 136 passed (or more), the CLI self-check
     still reports `passed: True` with `max_abs_difference_when_masked: 0.0` and a non-zero positive
     control, and `verify_release.py` and `verify_container.py` both still exit 0.
