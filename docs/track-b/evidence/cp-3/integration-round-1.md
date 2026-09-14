# Verdict — M3/CP-3 — Integration — FAIL

- Candidate SHA: 029a68ca4b499206fd527727120bb9e54f1c7fd8
- Plan / version / bar: capstone_V6_8.md, v6.8, §12 "CP-3 (6 items)"
- Verbatim bar excerpt: confirmed present in `capstone_V6_8.md` at this SHA (line 483 ff., courtesy only):

  > **CP-3 (6 items)**
  > - [ ] Bundled champion, CLI (`predict_next_day.py`), container, and marimo app run locally from a clean setup. The champion is registered as a DagsHub MLflow **model version with the `champion` alias** and release/lineage tags — **non-gating**: a registry or metadata-operation outage does not block release and is disclosed.
  > - [ ] The quantile-level selector and at most one simple load-forecast scenario control work, served by direct local inference or a one-dimensional lookup — with no multidimensional precomputed grid, dynamic SHAP, or per-cell OOD system. Scenario perturbations are labeled sensitivity probes that may be out of distribution.
  > - [ ] Static Pages export carries the §10 reading order, performs **zero runtime calls** to the Space or any external service, and renders every asset and link.
  > - [ ] HF Space deploys the **bundled** champion — the same artifact the holdout evaluated — and renders the same release snapshot. Free-tier sleep is disclosed, not performance-gated. Anything the Space shows over the holdout period is labeled **historical out-of-sample replay** on the page itself, never presented as a live forecast.
  > - [ ] README, Pages, Space metadata and MLflow links agree on the selected catalog, metrics, development evidence class, benchmark limitation, champion identity, and the holdout result with its power-qualification label and the statement that the shipped model is the evaluated model. **All four cutoffs — snapshot, raw-model fit, final calibration, holdout — appear separately and identically on every surface.** Limitations and reproduction instructions are complete.
  > - [ ] **One fresh Integration Critic returns `PASS`** on the final candidate from a clean detached checkout, with a verdict-only delta to the evidence tip.

  (The excerpt is the citation. Any line number is a courtesy and is non-binding.)
- Worktree clean before and after: **yes**. `git -C /tmp/critic-cp-3 status --porcelain` was empty both times; `rev-parse HEAD` = `029a68ca…` unchanged. Only gitignored byproducts were created (`.venv/`, `.pytest_cache/`, `app/__marimo__/`, `__pycache__/`). All scratch work (break-testing, scans) was done outside the worktree.

## Commands actually run

| # | Command | Exit | Observed |
|---|---|---|---|
| 1 | `git -C /tmp/critic-cp-3 status --porcelain` | 0 | empty (before and after) |
| 2 | `git -C /tmp/critic-cp-3 rev-parse HEAD` | 0 | `029a68ca4b499206fd527727120bb9e54f1c7fd8` (before and after) |
| 3 | `uv sync --locked --dev` | 0 | resolved and installed the locked dev set |
| 4 | `uv run pytest -q` | 0 | **`121 passed in 71.42s`** — matches the claim |
| 5 | `MLFLOW_DISABLE_AGENT_HINT=1 uv run python predict_next_day.py --level 80 --self-check` | 0 | 24-hour table printed; `delivery_day: 2026-09-06`, `rows_checked: 24`, `delivery_day_prices_change_nothing: True`, `positive_control_d_minus_1_changes_output: True`, **`max_abs_difference_when_masked: 0.0`**, `max_abs_difference_positive_control: 220.9433340396028`, **`passed: True`** — matches the claim, including a non-zero positive control |
| 6 | `uv run python scripts/verify_release.py` | 0 | agreement table all `yes`; `disagreements: none`; `fetching references to an external origin: 0`; `gated DagsHub UI links on any surface: none`; final line `PASS` |
| 7 | `uv run python scripts/verify_container.py --out /tmp/critic-container.json` | 0 | `passed: true`; steps `build`, `run_offline`, `offline_probe`, `cli_offline`, `marimo_server_mode` all `ok`; image 1.66 GB; under `--network none` the in-container app health is `200 {"status":"healthy"}` while `huggingface.co`, `dagshub.com`, `cdn.jsdelivr.net` and generic outbound are all unreachable; in-container CLI self-check `passed: True` |
| 8 | `uv run marimo run app/showcase.py --headless --port 8891 --no-token` (bg) | serving | `curl http://127.0.0.1:8891/health` → **HTTP 200 `{"status":"healthy"}`** |
| 9 | `curl -s -o /dev/null -w "%{http_code}" https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast` | 0 | **401** |
| 10 | `curl -s "https://huggingface.co/api/spaces?author=hrsi56"` | 0 | **`[]`** — the account owns no Spaces at all |
| 11 | `curl -s -o /dev/null -w "%{http_code}" https://huggingface.co/hrsi56` | 0 | **404** — the HF user account does not exist |
| 12 | `curl -s -o /dev/null -w "%{http_code}" https://hrsi56.github.io/delu-day-ahead-forecast/` | 0 | **404** |
| 13 | `curl -s https://api.github.com/repos/hrsi56/delu-day-ahead-forecast/pages` | 0 | **404 Not Found**; repo API reports `"has_pages": false` (repo itself is public, 200, `default_branch: main`) |
| 14 | `curl -s ".../delu-day-ahead-forecast.mlflow/api/2.0/mlflow/registered-models/alias?name=delu-day-ahead-champion&alias=champion"` (anonymous, no credential) | 0 | model version **`1`**, `"aliases":["champion"]`, `status: READY`, **35 tags** incl. `release_status=portfolio_release`, `source_run_id`, `code_commit`, `snapshot_sha256`, `artifact_fingerprint_sha256` and all four cutoffs |
| 15 | ad-hoc `uv run python` — recompute every holdout metric from `reports/cp2/holdout_predictions.parquet` | 0 | see below; all reproduce |
| 16 | ad-hoc `uv run python` — recompute catalog selection + A69 benchmark from the committed prediction parquets | 0 | reproduce exactly |
| 17 | ad-hoc `uv run python` — recompute `ChampionModel.fingerprint()` from the loaded `models/champion/` pyfunc, and `sha256(data/snapshot.parquet)` | 0 | both match the card and the holdout report |
| 18 | ad-hoc `uv run python` — drive both controls and compare the page's embedded grid against live inference | 0 | max abs difference **0.0** at all 11 scales |
| 19 | scratch copy at `…/scratchpad/break` (outside the worktree), 4 deliberate breaks + `pytest` | — | every break caught; restored copy green (26 passed) |
| 20 | Browser: load `http://127.0.0.1:8892/index.html` (local `python3 -m http.server` over `docs/`), read network + console, drive both controls, re-read network | — | **exactly one network request** (the page itself) before and after interaction; **no console errors** |

## Evidence actually inspected

**Plan.** `capstone_V6_8.md` §12 CP-3 bar (verified verbatim), and the supporting sections §5.2 (delivery-day availability invariant), §6.1/§6.2, §7.1, §7.2, §9.1, §9.2, §9.3, §9.4, §9.6, §10, §10.1.

**Artifacts opened and recomputed.** `models/champion/champion_card.json`, `models/champion/MLmodel`, `models/champion/python_model.pkl` (loaded); `data/snapshot.parquet` (hashed and aggregated); `reports/cp2/holdout_report.json`, `catalog_selection.json`, `a69_benchmark.json`, `dm_development.json`, `holdout_predictions.parquet`, `development_predictions.parquet`, `a69_benchmark_predictions.parquet`, `reliability_three_stage.csv`, `regime_table.csv`, `shap_ranking.csv`, `permutation_importance.csv`; `reports/cp3/link_check.json`, `container_check.json`, `mlflow_registration.json`.

**Recomputation results** (mine, left; committed, right):

| Quantity | Recomputed | Committed |
|---|---|---|
| `champion_mae` | 25.907780440955044 | 25.907780440955044 |
| `similar_day_naive_mae` | 27.75776736111111 | 27.75776736111111 |
| `champion_mean_pinball` | 6.708294915819918 | 6.708294915819919 |
| `similar_day_naive_mean_pinball` | 13.878883680555555 | 13.878883680555557 |
| MAE % diff | −6.66475403474962 | −6.664754034749622 |
| pinball % diff | −51.66545761012248 | −51.66545761012248 |
| final coverage 50/80/95 | 0.44074074/0.75925926/0.93981481 | identical |
| raw & post-CQR coverage | identical | identical |
| crossing violations (final) | **0** | 0 |
| DM statistic / p / LRV / N / lag | −8.67984849081244 / 1.9814819e-18 / 61.4225515 / 90 / 4 | −8.679848490812438 / 1.9814819e-18 / 61.42255149 / 90 / 4 |
| DM effect size | −1.047758 (ddof=1) | −1.0477562158534526 |
| catalog `base` pooled raw-head pinball | 13.015841509664993 | 13.015841509664993 |
| catalog `base+residual_load_proxy` | 13.064197422052183 | 13.064197422052183 |
| A69 benchmark % difference | −19.492607337797907 | −19.492607337797907 |
| `artifact_fingerprint_sha256` from the bundled pyfunc | `57e3ad40a7f48bb7896628ce2e5dec61314dea567da9867aede4bf1b0a10e0fb` | same in `champion_card.json` **and** in `holdout_report.json` |
| `sha256(data/snapshot.parquet)` | `7dd2dc73407706ca6bd3c1ad51d201ac0de35eec5ca129ce320cca639f697f00` | same |
| annual mean price 2020/2022/2025 | 30.47 / 235.45 / 89.32 | page says ~€30 / ~€235 / ~€89 |
| negative-price hours 2021–25 | 139 / 69 / 301 / 457 / **576** | page says 139→69→301→457→**576** and discloses the MTU basis (the plan's §10 narrative still says 573; the page's number is the one that matches the committed snapshot) |

**Figures.** All 7 `<img>` on `docs/index.html` are `data:image/png;base64`, decode to valid PNGs (PIL verify), and each is **bitwise identical** to a committed file: `reports/fig_welch_periodogram.png`, `fig_per_regime_periodogram.png`, `fig_acf_24_168.png`, `reports/cp2/fig_shap_summary.png`, `fig_shap_dependence_price_lag_24h.png`, `fig_shap_dependence_price_lag_168h.png`, `fig_reliability_three_stage.png`.

**Source read.** `src/delu_forecast/showcase.py` (in full), `src/delu_forecast/features.py` (`_calendar_day_lag`, `_daily_price_statistics`, `build_base_features`), `src/delu_forecast/model.py` (`fingerprint`, runtime firewall, `CHAMPION_INPUT_COLUMNS`/`FORBIDDEN_CHAMPION_INPUT_COLUMNS`), `predict_next_day.py`, `app/showcase.py`, `scripts/check_links.py`, `scripts/verify_release.py`, `Makefile`, `tests/test_18_showcase_gate_boundary.py`, `docs/deploy.md`.

**Surfaces read in full.** `README.md`, `space/README.md`, `docs/index.html` (raw HTML, both inline scripts, and extracted text), `docs/cp2-model-report.md`, plus the live MLflow registered-model record.

## Checklist verdict

| # | Checklist item | Verdict | Evidence |
|---|---|---|---|
| 1 | Bundled champion, CLI, container, marimo app run from a clean setup; champion registered as a model version with the `champion` alias and release/lineage tags (non-gating) | **PASS** | `uv sync --locked --dev` exit 0; `pytest -q` → **121 passed**; CLI self-check `passed: True` / `max_abs_difference_when_masked: 0.0` / positive control 220.94; champion loads from `models/champion/` as an `mlflow.pyfunc` (bundled — `showcase.load_champion` has no registry path, and `verify_container` shows the container works with all outbound network unreachable); marimo `/health` → 200; `verify_container.py` → all 5 steps ok, image builds and runs under `--network none`. Registry checked anonymously with no credential: `delu-day-ahead-champion` v1, `aliases:["champion"]`, 35 tags; `artifact_fingerprint_sha256`, `code_commit`, `snapshot_sha256`, `release_status=portfolio_release`, `source_run_id` and all four cutoffs each match `models/champion/champion_card.json` exactly. |
| 2 | Exactly the two permitted controls, working, via direct local inference or a 1-D lookup; no multidimensional grid / dynamic SHAP / per-cell OOD; sensitivity-probe label present | **PASS** | `app/showcase.py` defines exactly two interactive elements — `mo.ui.radio` (50/80/95) and `mo.ui.slider(0.90–1.10)`; the three `mo.ui.table` calls pass `selection=None`. Browser confirms 4 form elements = 3 radios (one selector) + 1 slider. Both **work**: interval mean width 40.06 → 83.04 → 145.93 across levels and the coverage annotation switches 0.4407/0.7593/0.9398; the slider moves the median by up to 7.33 EUR/MWh; `quantile_fan` rejects level 90. The page's lookup is 1-D — 11 scales × 24 hours × 9 quantiles — and is **bitwise identical (max diff 0.0)** to live `forecast_delivery_day` inference at every scale. SHAP is three static PNGs, not recomputed. No OOD machinery anywhere. Label verbatim on page and in the app: "Scenario perturbations are ceteris-paribus sensitivity probes and may be out of distribution." |
| 3 | Static Pages export carries the §10 reading order, performs zero runtime calls, renders every asset and link | **FAIL** | The **export artifact is correct**: headings carry all twelve §10 items (1, 2, 3, 3b, 4, 5, 6–7, 8, 9, 10, 11, 12); **zero runtime calls** verified by my own raw-HTML scan (0 × `<script src>`, `<link>`, `<iframe>`, `@import`, `http-equiv=refresh`, `ping=`, `fetch(`, `XMLHttpRequest`, `WebSocket`, `sendBeacon`, `EventSource`, `importScripts`, `.src=`, `url(http…)`, `<base>`, `<form>`, `srcdoc`, `document.write`; the only `http://` is the SVG namespace in `createElementNS`) **and empirically in a real browser — exactly one network request, the page itself, before and after driving both controls, with no console errors**; all 7 figures decode and match committed PNGs bitwise. **But the page is not published**: GitHub Pages is not enabled (`has_pages: false`, Pages API 404, `https://hrsi56.github.io/delu-day-ahead-forecast/` → 404), so the export is not served at the canonical URL that both the README and the Space card advertise; and one of its three external links — `https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast` — returns **401** and does not render. The candidate's own `reports/cp3/link_check.json` records both as `resolves: false`. |
| 4 | HF Space deploys the bundled champion, renders the same release snapshot; sleep disclosed, not performance-gated; holdout-period content labeled historical out-of-sample replay | **FAIL** | **No HF Space exists.** `https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast` → 401; `https://huggingface.co/api/spaces?author=hrsi56` → `[]`; `https://huggingface.co/hrsi56` → **404 — the Hugging Face account itself does not exist**. `docs/deploy.md` states plainly: "**Nothing was published:** no Space was created, GitHub Pages was not enabled, and nothing was pushed." This is a finding, not a blocked check. The checkable sub-parts do pass: the replay label is verbatim on the page the Space would render and in `space/README.md` ("Historical out-of-sample replay — the frozen champion forecasting a 90-day period it never trained on. This is not a live forecast."), free-tier sleep is disclosed as "~30 s to wake if asleep" with no timing threshold attached, and the **bundled artifact is provably the evaluated artifact** — I recomputed `ChampionModel.fingerprint()` from the loaded `models/champion/` pyfunc as `57e3ad40…e0fb`, identical to both `champion_card.json` and `reports/cp2/holdout_report.json`. The item's central clause is nonetheless unmet. |
| 5 | README / Pages / Space metadata / MLflow agree on every bound claim; all four cutoffs separately and identically on every surface; limitations and reproduction instructions complete | **PASS** | I built the table myself rather than trusting `verify_release.py`: **27 bound claims × 4 surfaces (README.md, space/README.md, docs/index.html, the live MLflow registered-model tags) — zero disagreements**, and every surface carries the *identical* rendering, so no surface rounds a number differently. I separately checked each rendering against the unrounded artifact (e.g. `25.9078` = `f"{25.907780440955044:.4f}"`, `-51.67%` = `f"{-51.66545761012248:.2f}%"`, `+0.371516%`, `-19.4926%`, `0.948`) — all faithful. **All four cutoffs** (`2026-09-06`, `2026-04-07`, `2026-04-09..2026-06-07`, `2026-06-09..2026-09-06`) appear separately and identically on all four surfaces. The §7.1 one-shot-holdout limitation paragraph and the §6.2 exchangeability paragraph are **verbatim** (whitespace-normalised, matched against the text extracted from the plan itself) on README, Space card, Pages export **and** `docs/cp2-model-report.md`; the DM power-qualification label is verbatim on all four surfaces including the MLflow `holdout_dm_label` tag; the "shipped model is the evaluated model" statement likewise. Link discipline holds: all 11 experiment-tracking links on public surfaces are the `.mlflow` URI and no gated DagsHub UI path appears on any surface (the two non-`.mlflow` strings live in `scripts/check_links.py`'s probe template and `scripts/verify_container.py`'s offline target). Reproduction instructions are present and complete on all three human surfaces. *Minor incompleteness, recorded but not gating:* the §10-item-11 "15-min-MTU averaging choice" limitation appears on the Pages export but not in `README.md` or `space/README.md`. |
| 6 | One fresh Integration Critic returns `PASS` from a clean detached checkout | **FAIL** | This is that review, and the verdict it writes is **FAIL**. Performed from the clean detached worktree `/tmp/critic-cp-3` at `029a68ca…`, clean before and after. |

### Additional binding checks the plan requires everywhere

**§5.2 delivery-day availability invariant — holds, and the controls guarding it are real.** `src/delu_forecast/showcase.py` is the single inference path for the CLI, the marimo app and the page builder; `gate_feasible_frame` drops every row dated after `target_day`, masks every `price_eur_mwh` on `target_day` to NaN, and restricts columns to `CHAMPION_INPUT_COLUMNS`, with the model's own runtime firewall rejecting `FORBIDDEN_CHAMPION_INPUT_COLUMNS` again. `_daily_price_statistics` freezes the 168h/720h windows at `local-midnight(D) − 1h` and broadcasts one value per delivery day; `_calendar_day_lag` matches the Berlin calendar day with `ambiguous="NaT", nonexistent="NaT"` — it fails closed. `load_scale` touches only the target day's `load_forecast_mw`, and `load_forecast_day_mean_mw` is derived from it downstream, so the probe is internally consistent. I confirmed the `HISTORY_DAYS=200` truncation reproduces whole-snapshot output bitwise (max diff **0.0**).

I did not accept the green run as evidence. In a scratch copy **outside the worktree** I applied four deliberate breaks and confirmed each is caught:

| Break | Effect | Caught by |
|---|---|---|
| A — rolling window right edge moved from `D−1 23:00` to `D 11:00` | 12 hours of delivery-day price enter the rolling features | **15 failures** across `test_02`, `test_13`, `test_18` |
| B — calendar-day lag replaced by a row-wise `shift(24n−1)` | row-wise boundary reintroduced | **15 failures** across `test_02`, `test_13`, `test_18` |
| C — showcase delivery-day price mask removed | frame no longer honest at the gate | `test_18::test_gate_frame_masks_every_delivery_day_price` (only 1 failure — correctly so: the features genuinely never consume those prices, which is exactly what `test_delivery_day_prices_change_nothing_and_a_d_minus_1_price_does` asserts) |
| D — DST `ambiguous=True, nonexistent="shift_forward"` | fails open instead of closed | **6 failures** in `test_02::test_lag_source_day_itself_is_dst_and_fails_closed` |

Restoring the scratch copy returned it to green (26 passed). The CLI's own positive control is likewise real: `max_abs_difference_positive_control = 220.94`, non-zero.

**Reported metrics vs the committed CP-2 artifacts.** Every metric on every surface traces to a number I recomputed from the committed prediction parquets (table above). No surface states a figure I could not reproduce.

## On FAIL only

- **Single largest meaningful gap:** M3's two public surfaces were built but never deployed. No Hugging Face Space exists — the `hrsi56` HF account itself returns 404 — so item 4's central requirement ("HF Space deploys the bundled champion") is unmet outright, and GitHub Pages is not enabled (`has_pages: false`), so the verified static export is not served at the canonical recruiter URL that the README, the Space card and the MLflow `pages_url` tag all advertise. Everything else in the checkpoint is in good order: the local stack, the container, the controls, the registry record and the four-surface agreement table all verify independently, and the bundled artifact is provably the one the holdout evaluated.
- **Exact next acceptance test:** with the repository otherwise unchanged at this SHA, all of the following must hold from an unauthenticated client:
  1. `curl -s -o /dev/null -w "%{http_code}" https://hrsi56.github.io/delu-day-ahead-forecast/` → **200**, and the served bytes equal the committed `docs/index.html`, with a browser load issuing **exactly one** network request and no console error;
  2. `curl -s -o /dev/null -w "%{http_code}" https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast` → **200**, the Space reaching `RUNNING`, its rendered page showing the verbatim *historical out-of-sample replay* label above the chart, both controls responding, and the deployed image's `models/champion/` reproducing `artifact_fingerprint_sha256 = 57e3ad40a7f48bb7896628ce2e5dec61314dea567da9867aede4bf1b0a10e0fb`;
  3. `uv run python scripts/check_links.py` recording `unresolved: []`;
  4. `uv run python scripts/verify_release.py` still exiting 0 with `disagreements: none` after the README's "Deployment status — read this before clicking" paragraph is deleted (per `docs/deploy.md`);
  5. `uv run pytest -q` still reporting 121 passed.

  Recommended alongside, though not gating: add the §10-item-11 15-minute-MTU averaging limitation to `README.md` and `space/README.md` so all four surfaces carry the full limitations set.
