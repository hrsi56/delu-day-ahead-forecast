# Verdict — M3/CP-3 — Integration — FAIL

- Candidate SHA: 9380aace21cec56a15a67ce636794e59c9de6a6f
- Plan / version / bar: capstone_V6_8.md, v6.8, §12 "CP-3 (6 items)"
- Verbatim bar excerpt: (confirmed present in `capstone_V6_8.md` at this SHA; found at lines 483–490 — line numbers a courtesy, the text is the citation)

> **CP-3 (6 items)**
> - [ ] Bundled champion, CLI (`predict_next_day.py`), container, and marimo app run locally from a clean setup. The champion is registered as a DagsHub MLflow **model version with the `champion` alias** and release/lineage tags — **non-gating**: a registry or metadata-operation outage does not block release and is disclosed.
> - [ ] The quantile-level selector and at most one simple load-forecast scenario control work, served by direct local inference or a one-dimensional lookup — with no multidimensional precomputed grid, dynamic SHAP, or per-cell OOD system. Scenario perturbations are labeled sensitivity probes that may be out of distribution.
> - [ ] Static Pages export carries the §10 reading order, performs **zero runtime calls** to the Space or any external service, and renders every asset and link.
> - [ ] HF Space deploys the **bundled** champion — the same artifact the holdout evaluated — and renders the same release snapshot. Free-tier sleep is disclosed, not performance-gated. Anything the Space shows over the holdout period is labeled **historical out-of-sample replay** on the page itself, never presented as a live forecast.
> - [ ] README, Pages, Space metadata and MLflow links agree on the selected catalog, metrics, development evidence class, benchmark limitation, champion identity, and the holdout result with its power-qualification label and the statement that the shipped model is the evaluated model. **All four cutoffs — snapshot, raw-model fit, final calibration, holdout — appear separately and identically on every surface.** Limitations and reproduction instructions are complete.
> - [ ] **One fresh Integration Critic returns `PASS`** on the final candidate from a clean detached checkout, with a verdict-only delta to the evidence tip.

- Worktree clean before and after: **yes** (`git status --porcelain` empty at both ends; `rev-parse HEAD` = 9380aace… unchanged). Gitignored byproducts I created (`__pycache__`, a scratch `.pyc`) were removed; none were tracked.

## Commands actually run

| Command | Exit | Observed |
|---|---|---|
| `git -C /tmp/critic-cp-3 status --porcelain` (before) | 0 | empty |
| `git -C /tmp/critic-cp-3 rev-parse HEAD` | 0 | `9380aace21cec56a15a67ce636794e59c9de6a6f` |
| `uv sync --locked --dev` | 0 | resolved 129 packages, checked 117 |
| `uv run pytest -q` | 0 | **148 passed in 32.45s** |
| `MLFLOW_DISABLE_AGENT_HINT=1 uv run python predict_next_day.py --level 80 --self-check` | 0 | `passed: True`, `max_abs_difference_when_masked: 0.0`, `max_abs_difference_positive_control: 220.9433340396028`, `delivery_day_prices_change_nothing: True`, source `bundled data/snapshot.parquet (no network)` |
| `uv run marimo run app/showcase.py --headless --port 8891 --no-token` + `curl http://127.0.0.1:8891/health` | 200 | `{"status":"healthy"}` |
| `uv run python scripts/verify_container.py --out /tmp/critic-container.json` | 0 | `passed: true`; steps build / run_offline / offline_probe / cli_offline / marimo_server_mode all ok; image 1.66GB; with `--network none`, `dagshub.com`, `huggingface.co`, `cdn.jsdelivr.net`, outbound all unreachable; in-container app `/health` 200 |
| `uv run python scripts/verify_release.py` | 0 | `PASS — every bound claim agrees on all four surfaces; the page fetches nothing`; `disagreements: none`; `gated DagsHub UI links on any surface: none` |
| `curl …/mlflow/api/2.0/mlflow/registered-models/alias?name=delu-day-ahead-champion&alias=champion` (anonymous, no credential) | 0 | version `1`, `"aliases":["champion"]`, `status: READY`, 38 release/lineage tags |
| Generators re-run (`build_pages.py`, `build_space.py`, `cp3_readme.py`, `cp2_readme.py`, `cp2_report.py`) | 0,0,0,0,0 | see idempotence below |
| `git status --porcelain` after regeneration | 0 | ` M reports/cp3/pages_build.json` |
| `git checkout -- .` then `git status --porcelain` | 0 | empty; HEAD unchanged |
| `curl https://hrsi56.github.io/delu-day-ahead-forecast/` | 0 | **HTTP 404** (x2 attempts) |
| `curl https://api.github.com/repos/hrsi56/delu-day-ahead-forecast/pages` | 0 | **404 Not Found** — Pages not enabled |
| `curl https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast` | 0 | **HTTP 401** (x4 attempts) |
| `curl https://hrsi56-delu-day-ahead-forecast.hf.space/` | 0 | **HTTP 404** |
| `curl https://huggingface.co/hrsi56` | 0 | **HTTP 404** — the HF account itself does not exist publicly |
| Network controls | 0 | `pages.github.com` 200, `microsoft.github.io/monaco-editor` 200, `d3js.org` 200, `huggingface.co/spaces/gradio/hello_world` 200, `github.com/hrsi56/delu-day-ahead-forecast` 200 (`"private": false`) |
| Scratch-copy break test (`/tmp/critic-scratch`, own venv) | 1 | 4 tests failed; CLI self-check `passed: False` |

## Evidence actually inspected

- `capstone_V6_8.md` §12 CP-3 bar (lines 483–490), §9.2, §9.3, §10 reading order, §10.1.
- `src/delu_forecast/showcase.py` (all 188 lines of logic read), `src/delu_forecast/model.py` (`validate_runtime_input`, `build_features`, `predict_stages`, `fingerprint`, `CHAMPION_INPUT_COLUMNS`), `src/delu_forecast/claims.py` (size walk, label constants), `src/delu_forecast/features.py` (`_calendar_day_lag`), `predict_next_day.py`.
- `tests/test_18_showcase_gate_boundary.py` (all 151 lines).
- `docs/index.html` — raw HTML parsed by me directly (not via `static_audit.py`): every `src`/`href`/`action`/`srcset`, both `<script>` blocks, all 7 base64 assets decoded, all `id` targets.
- `README.md`, `space/README.md`, `models/champion/champion_card.json`, `reports/cp2/holdout_report.json`, `reports/cp2/holdout_predictions.parquet`, `data/snapshot.parquet`, `.gitignore`, `Dockerfile` context, `app/showcase.py` controls cell.
- DagsHub MLflow registered-model-version JSON (fetched anonymously).

### Independent recomputation (not taken from any document)

Recomputed from `reports/cp2/holdout_predictions.parquet` with my own pinball/MAE/coverage code:

| Metric | Recomputed | Published |
|---|---|---|
| champion mean pinball | 6.7082949158 | 6.7083 |
| naive mean pinball | 13.8788836806 | 13.8789 |
| champion MAE | 25.9077804410 | 25.9078 |
| naive MAE | 27.7577673611 | 27.7578 |
| pinball % diff | −51.6654576101 | −51.67% |
| MAE % diff | −6.6647540347 | −6.66% |
| coverage 50/80/95 | 0.4407407 / 0.7592593 / 0.9398148 | 0.4407 / 0.7593 / 0.9398 |
| crossing violations (final) | 0 | 0 |

Rows 2160, days 90 — both match. **No surface rounds a number differently.**

Champion identity, recomputed from the bundled artifact:
- `ChampionModel.fingerprint()` on `models/champion/` → `57e3ad40a7f48bb7896628ce2e5dec61314dea567da9867aede4bf1b0a10e0fb`
- identical in `champion_card.json`, `reports/cp2/holdout_report.json`, and the DagsHub registry tag. **All four identical** → the bundled artifact *is* the artifact the holdout evaluated.
- `sha256(data/snapshot.parquet)` recomputed → `7dd2dc73…f697f00`, matching the card, `data/snapshot.sha256`, and the registry tag.

### Champion on-disk size — the prior lineage defect, retested

- Pristine walk of `models/champion`: 23 files, **31,623,247 bytes**.
- A **real** `mlflow.pyfunc.load_model()` does create `models/champion/code/delu_forecast/__pycache__`; a naive walk then reads **31,696,865** (+73,618).
- Injecting a 500,000-byte fake `.pyc`: naive walk **32,123,247**.
- In both states the published claim stayed **31,623,247 / 30.2 MiB** — `claims.py` excludes `__pycache__` and `*.pyc` from the walk.
- All three human surfaces and the MLflow record carry the same figure. **Fixed; no surface disagrees.**

### §5.2 invariant — controls proven real, not assumed

`gate_feasible_frame` drops every row dated after the target day, NaNs the target day's own prices, and narrows to `CHAMPION_INPUT_COLUMNS`. Lag features are **rebuilt at inference** from raw columns (`base` = `timestamp_utc, delivery_date, local_hour, price_eur_mwh, load_forecast_mw`), so the mask is substantive rather than vacuous.

I broke it in a **properly isolated** scratch copy (`/tmp/critic-scratch`, its **own** venv — `import delu_forecast` resolves to `/private/tmp/critic-scratch/src/delu_forecast/__init__.py`, not the worktree), changing `price_lag_24h` to a 0-day lag so it reads the delivery day's own price:

- `test_delivery_day_prices_change_nothing_and_a_d_minus_1_price_does` — **FAILED** (the assertion that would otherwise prove nothing)
- plus `test_truncated_history_reproduces_the_whole_snapshot_bitwise`, `test_the_boundary_holds_across_a_run_of_delivery_days`, `test_showcase_output_is_monotone_at_every_level` — **FAILED**
- CLI self-check on the broken build: `delivery_day_prices_change_nothing: False`, `passed: False`

The controls are real. Bundled `models/champion/code/delu_forecast/*.py` is byte-identical to `src/delu_forecast/*.py` for all 15 inference modules.

### Generator idempotence

Re-running all five generators left `docs/index.html`, `README.md` and `space/README.md` **byte-identical** (absent from `git status`). One tracked file moved:

```
 M reports/cp3/pages_build.json
-  "built_on": "2026-09-14",
+  "built_on": "2026-09-15",
```

A build-date stamp only; every content-bearing field (`bytes: 1006064`, `load_scale_points: 11`, `marimo_export_external_reference_count: 181`) was stable, and `stat` confirms `docs/index.html` really is 1,006,064 bytes. This is a genuine but cosmetic non-idempotence — any re-run on a later calendar day dirties the worktree. Restored with `git checkout -- .`; clean before the verdict was written.

### Deployment status of the two public surfaces

| Surface | Advertised URL | Result |
|---|---|---|
| GitHub Pages | `https://hrsi56.github.io/delu-day-ahead-forecast/` | **404** |
| Pages API | `…/repos/hrsi56/delu-day-ahead-forecast/pages` | **404 — Pages not enabled** |
| HF Space | `https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast` | **401** |
| HF direct | `https://hrsi56-delu-day-ahead-forecast.hf.space/` | **404** |
| HF account | `https://huggingface.co/hrsi56` | **404 — account does not exist publicly** |

Controls confirm this is not a network artifact on my side: `pages.github.com`, `microsoft.github.io/monaco-editor`, `d3js.org` and `huggingface.co/spaces/gradio/hello_world` all returned 200 from the same shell, and the GitHub repo itself is public and reachable (200, `"private": false`). The DagsHub registry publicly advertises `pages_url` and `space_url` tags pointing at both dead URLs.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Bundled champion, CLI, container, marimo run locally from clean setup; registered as MLflow model version with `champion` alias and release/lineage tags (non-gating) | **PASS** | `uv sync` 0; 148/148 tests; CLI self-check `passed: True`, loads from `models/champion/` bundled with `source: bundled data/snapshot.parquet (no network)` — no registry path; marimo `/health` 200; `verify_container.py` `passed: true` with all 5 steps ok under `--network none`. Registry read **anonymously with no credential**: version 1, `aliases:["champion"]`, `status: READY`, tags carry `artifact_fingerprint_sha256`, `snapshot_sha256`, `code_commit`, `release_status: portfolio_release`, `source_run_id`, all four cutoffs — all matching `champion_card.json`. |
| 2 | Quantile-level selector + at most one load-forecast scenario control, direct local inference or 1-D lookup; no multidimensional grid, dynamic SHAP, or per-cell OOD; sensitivity-probe label | **PASS** | `app/showcase.py`: exactly two controls — `mo.ui.radio` (50/80/95) and `mo.ui.slider` (0.90–1.10 × the delivery day's A65). Both feed `forecast_delivery_day(..., load_scale=…)` — direct local inference. Pages uses a **one-dimensional** lookup: `window.__FAN__.scales` = 11 scale points, `series` keyed by scale alone. SHAP is static committed PNGs + static CSV tables; no per-cell OOD anywhere. `SENSITIVITY_PROBE_LABEL` ("…ceteris-paribus sensitivity probes and may be out of distribution.") verbatim on README, Pages and Space card. `test_18` proves the probe moves the forecast, touches no other day and no price. |
| 3 | Static Pages export carries §10 reading order, zero runtime calls, renders every asset and link | **FAIL** | Content properties all pass, verified by my own parse of the raw HTML: all twelve §10 items present (1, 2, 3, 3b, 4, 5, 6–7 with separate SHAP and permutation-importance sub-headings, 8, 9, 10, 11, 12); **zero runtime calls** — both `<script>` blocks inline with no `src`, no `<link>`, no CDN/font/fetch/XHR/WebSocket/EventSource/`@import`, the only `http` string being the SVG XML namespace; all 7 embedded PNGs decode with valid signatures and real dimensions; all 12 internal anchors resolve. **But** the page's outbound link to the HF Space returns **401** — "renders every asset and link" is not satisfied, and §10.1 makes the link check explicitly part of what CP-3 verifies. The export is also not published: its own canonical URL 404s and Pages is not enabled on the repo, so it is not "the primary recruiter URL" M3 describes. |
| 4 | HF Space deploys the bundled champion, same release snapshot, sleep disclosed not performance-gated, replay labeled on the page | **FAIL** | **No Space exists.** `huggingface.co/spaces/hrsi56/delu-day-ahead-forecast` → 401 on four attempts; the `.hf.space` host → 404; the HF account `hrsi56` itself → 404, while `gradio/hello_world` returns 200 from the same shell. Nothing is deployed, so the Space cannot serve the bundled champion or render anything. Checkable sub-parts, judged on the committed `space/README.md`, all pass: the replay label is verbatim; free-tier sleep is disclosed in prose and never performance-gated (§9.2 thresholds retired); `SPACE_LINK_LABEL` ("interactive demo — may take ~30 s to wake if asleep") is on README and Pages; and the bundled artifact **is** provably the holdout-evaluated one (fingerprint recomputed, matches all three records). The artifact is release-ready; the deployment has not happened. |
| 5 | README, Pages, Space metadata and MLflow agree on catalog, metrics, evidence class, benchmark limitation, champion identity, holdout result + power-qualification label + shipped-is-evaluated; all four cutoffs separately and identically everywhere; limitations and reproduction complete | **PASS** | I built the table myself. 31 bound claims × README / Pages / Space / MLflow: **zero mismatches** (catalog `base`; MAE 25.9078 / 27.7578 / −6.66%; pinball 6.7083 / 13.8789 / −51.67%; coverage 0.4407 / 0.7593 / 0.9398; DM −8.6798, p 1.98e-18, effect −1.0478; `development_post_selection`; benchmark −19.4926% with its limitation paragraph; catalog +0.371516%; fingerprint; snapshot hash; code SHA). All four cutoffs appear **separately and identically** on every surface. §7.1 holdout-limitation and §6.2 exchangeability paragraphs **verbatim** on all three human surfaces. All 10 §10 item (11) limitation elements verbatim on all three. All §10 item (12) elements (tagged commit, `.mlflow` permalink, `champion` alias, Pages URL, Space link, DuckDB SQL, four cutoffs, CC BY / ENTSO-E / SMARD attribution) present on all three. Every DagsHub URL on every surface is the `.mlflow` tracking URI — **no gated UI path anywhere**. Metrics independently recomputed from the committed CP-2 predictions and match exactly; no surface rounds differently. |
| 6 | One fresh Integration Critic returns `PASS` from a clean detached checkout | **FAIL** | This review is that critic, run from the clean detached worktree `/tmp/critic-cp-3` at `9380aace…` (clean before and after). The verdict I am writing is **FAIL**, so this item is not met. |

## On FAIL only

- **Single largest meaningful gap:** Neither public surface is deployed. The Hugging Face Space does not exist — the `hrsi56` HF account itself 404s — so item 4's "HF Space deploys the bundled champion" is unmet in full, and GitHub Pages is not enabled on the repo, so the static export that M3 designates the primary recruiter URL 404s and the Pages page's own link to the Space is dead. Everything upstream of deployment is in excellent shape: the bundled champion is provably the holdout-evaluated artifact, all 148 tests pass with genuine positive controls I verified by breaking them in an isolated copy, the prior lineage's champion-size drift is properly fixed, and 31 bound claims agree across all four surfaces with zero mismatches.

- **Exact next acceptance test:** With the candidate unchanged, a fresh critic must observe: (a) `curl -sS -o /dev/null -w '%{http_code}' https://hrsi56.github.io/delu-day-ahead-forecast/` → `200`, serving a body byte-identical to the committed `docs/index.html` (1,006,064 bytes, md5 `46b8072874949dba3587d836fb0ace87`); (b) `curl` of the HF Space URL → `200`, the Space reachable and running the Docker SDK image built from this SHA, its page carrying the verbatim replay label and the `champion_fingerprint` `57e3ad40…a0e0fb`, with free-tier sleep disclosed and no performance gate; (c) every outbound link on the Pages export resolving non-4xx, including the Space link; (d) worktree still clean at `9380aace…`. Separately and minor, not release-blocking: make `reports/cp3/pages_build.json` idempotent (its `built_on` stamp changes the file on any re-run on a later calendar day), so that re-running all five generators leaves `git status --porcelain` empty.
