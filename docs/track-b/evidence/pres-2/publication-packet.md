# PRES-2 — Owner landing and publication packet

Everything below is the Owner's to run (AGENTS.md § Git and publication authority; the brief's
"Owner-only actions already authorized: None"). No step here was run by an agent except the
read-only identity reads and the rehearsal in a scratch clone described in §2. The final candidate
and evidence-tip SHAs are named in the checkpoint return and in `integration.md`, since a file cannot
name the commit that contains it; substitute them where this packet writes `<final_candidate_sha>`
and `<evidence_tip_sha>`.

## 1. What would be published

| Surface | Reviewed output | Identity | Now public (read 2026-09-29T05:35:55Z) |
|---|---|---|---|
| Report, GitHub Pages | `docs/index.html` | 1,684,252 bytes, SHA-256 `f36314e28811ed4b7ec41bc73dfd481ddb112815effabfc4e7b3ae74d8edab1d` | 1,560,646 bytes, `d1227c0f64c6a478f6f076e713e2bed2755edf51d0b8f19522c9b978d42fab3d` (PRES-1) |
| README | `README.md` | SHA-256 `3a16a70a4f3a6d89751cdd2e4f9ed373964a8a63defaa91919c2c331ecaddf67` | at `main` `01e394d` |
| Static Space bundle | `dist/space-wasm/` from `make wasm` at the landed tree | `bundle_sha256` `8007f0d2a9c09a8c2c3182745dac6b38956a9a0ad8f58541f32472b674d5bb4e`, 805 files, 44,164,910 bytes; exact copy at `.local/artifacts/pres-2/space-wasm-8007f0d2/` | Space revision `59d941825755bf73eabb7ff20e31124fee305755`, bundle `b046c69b899bb9d5a2b2f9aeb3e5b3eebfdda820a419137ef5cdf8b8ac8f7c3d` (PRES-1) |
| Static Space card | `space-wasm/README.md` (the bundle's `README.md`) | SHA-256 `c92a2666d76255b24d8e0fb159f97bedcbee0a7a948fb6afeac4b02089bb9a67` | PRES-1's card, `6c89e63e…` |
| Space card (container, not hosted) | `space/README.md` | SHA-256 `745bbb932d78afbecdca3964af4885d223fd9301cd628bde1744f08e9f71d553` | repository file only |
| MLflow `delu-generations` | `reports/presentation/mlflow-export/` | tree `3e86afaa21b936ebddf60e001d4bf854aa7ac458`, identical to `main`'s | verified read-only: `pres-2-public-mirror.json`, `pres-2-public-mlflow-routes.json` — **no upload** |

The model, its payload and the v1 claims are unchanged since PRES-1; the bundle differs by the
control-name and target-size repair (F01), the scenario slider's plain label and one card line.

## 2. Landing on `main`

The primary checkout holds uncommitted work that must survive: `M AGENTS.md`, `M progress.md`, and
four untracked files — `docs/PUBLISH_RULES.md`, `docs/track-b/pres-2-execution-brief-2026-09-29.md`,
`docs/track-b/publication-postdeploy-independent-review-2026-09-29.md` and
`docs/track-b/publish-rules-migration-plan-2026-09-29.md`. `gauntlet/pres-2` carries byte-identical
copies of those five governing files (`baseline.md` §3) and never touches `progress.md`.

**Rehearsed in a scratch clone** (`.local/tmp/pres-2/landing-rehearsal`, its remote removed) with the
same porcelain status and the same five hashes:

- A plain `git merge --squash gauntlet/pres-2` **refuses** — "Your local changes to the following
  files would be overwritten by merge: AGENTS.md" and "The following untracked working tree files
  would be overwritten by merge" for the four files — and aborts with nothing changed.
- Staging the five identical files first lets the squash succeed: the staged tree then equals the
  branch tip exactly (`git diff --cached <tip>` empty), and `progress.md` stays an unstaged local
  modification.

The sequence, in the primary checkout on `main`:

```bash
git status --porcelain=v1
```

Expect exactly the six lines above. Then confirm the five files are the reviewed copies (each pair
must match; stop if one does not):

```bash
for f in AGENTS.md docs/PUBLISH_RULES.md docs/track-b/pres-2-execution-brief-2026-09-29.md docs/track-b/publication-postdeploy-independent-review-2026-09-29.md docs/track-b/publish-rules-migration-plan-2026-09-29.md; do echo "$(git hash-object "$f") $(git rev-parse "<evidence_tip_sha>:$f") $f"; done
```

```bash
git add AGENTS.md docs/PUBLISH_RULES.md docs/track-b/pres-2-execution-brief-2026-09-29.md docs/track-b/publication-postdeploy-independent-review-2026-09-29.md docs/track-b/publish-rules-migration-plan-2026-09-29.md
```

```bash
git merge --squash gauntlet/pres-2
```

```bash
git diff --cached --stat <evidence_tip_sha>
```

That last command must print nothing. Review the staged tree (`git diff --cached --stat`), then commit
by hand; `progress.md` is not staged and stays as it is:

```bash
git commit
```

```bash
git tag land/pres-2 HEAD
```

```bash
git tag evidence/pres-2 <evidence_tip_sha>
```

The proposed commit message is in the checkpoint return. `git status` after the commit should show
only ` M progress.md`.

## 3. Publication, in order

1. **Push `main` and both tags.** The pre-push hook runs the credential-value guard, then the
   publication guard (`make publication-guard` passes on the candidate tree). GitHub Pages then serves
   `docs/`.

   ```bash
   git push origin main land/pres-2 evidence/pres-2
   ```

2. **Rebuild the bundle from the landed tree and check it** (no secret is read for use; nothing is
   written remotely):

   ```bash
   make wasm
   ```

   ```bash
   uv run python scripts/deploy_space.py --bundle dist/space-wasm --expect 8007f0d2a9c09a8c2c3182745dac6b38956a9a0ad8f58541f32472b674d5bb4e
   ```

   If the rebuilt hash differs, stop: the exact reviewed copy is in
   `.local/artifacts/pres-2/space-wasm-8007f0d2/`, and a different bundle needs its own review.

3. **Upload the reviewed bundle** (the Owner's credential, read inside the process):

   ```bash
   uv run --with huggingface_hub python scripts/deploy_space.py --bundle dist/space-wasm --expect 8007f0d2a9c09a8c2c3182745dac6b38956a9a0ad8f58541f32472b674d5bb4e --upload --record reports/presentation/release-checks/pres-2-space-deployment.json
   ```

   It uploads against the revision it has just read, compares every remote file with the bundle
   and writes the record. Pages and the Space do not change atomically; run step 3 soon after
   step 1.

4. **No MLflow upload.** The export is unchanged and the public mirror was verified read-only.

## 4. Public checks after publication (P8, A6)

Run from the landed checkout, each writing a new record; keep a first failure beside its retry.

```bash
curl -s https://hrsi56.github.io/delu-day-ahead-forecast/ | shasum -a 256
```

Expect `f36314e28811ed4b7ec41bc73dfd481ddb112815effabfc4e7b3ae74d8edab1d` once Pages has deployed.

```bash
curl -s https://huggingface.co/api/spaces/Yarden-Viktor/delu-day-ahead-forecast | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['sdk'], 'private' if d['private'] else 'public', d['sha'], (d.get('runtime') or {}).get('stage'))"
```

Expect `static public <the revision in pres-2-space-deployment.json> RUNNING`.

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py release https://hrsi56.github.io/delu-day-ahead-forecast/ --shots .local/artifacts/pres-2/public-report --out reports/presentation/release-checks/pres-2-public-report.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py charts https://hrsi56.github.io/delu-day-ahead-forecast/ --out .local/artifacts/pres-2/public-charts --record reports/presentation/release-checks/pres-2-public-charts.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py demo --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/pres-2-public-demo.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py demo-a11y --engine chrome --engine webkit --viewport 1440x900 --viewport 390x844 --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/pres-2-public-demo-a11y.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py states --engine chrome --engine webkit --url https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/ --out reports/presentation/release-checks/pres-2-public-states.json
```

```bash
uv run python scripts/verify_mlflow_mirror.py verify --target public --out reports/presentation/release-checks/pres-2-public-mirror-postdeploy.json
```

```bash
.local/tools/playwright/bin/python scripts/check_reader_paths.py mlflow-routes --mirror-record reports/presentation/release-checks/pres-2-public-mirror-postdeploy.json --shots .local/artifacts/pres-2/public-mlflow-postdeploy --out reports/presentation/release-checks/pres-2-public-mlflow-routes-postdeploy.json
```

```bash
uv run python -c "import sys; from pathlib import Path; sys.path.insert(0, 'scripts'); import check_links; raise SystemExit(check_links.main(record=Path('reports/presentation/release-checks/pres-2-public-links.json')))"
```

The Playwright commands need `PLAYWRIGHT_BROWSERS_PATH=.local/tools/playwright/browsers`. The
states check forces failures by intercepting requests inside the test browser only; it changes
nothing on Hugging Face.

What each finding closes: F01 — `pres-2-public-demo-a11y.json` (named controls and 44 px targets
in both engines' native trees, keyboard operation); F02 — `pres-2-public-report.json` (no HTTP
error and no resource after the document in any view, served by Pages); F03 — the startup line on
the served page, and `pres-2-public-demo.json` for the new bundle's cold start (if it differs
materially from the page's 18.3 s, the page's measurement record is updated in a follow-up
publication, not by editing the served page); F04 — the served page's population line. A new, dated
independent postdeploy review under `docs/track-b/` then records the per-surface identities, these
results and its verdict (plan P8.7); the 2026-09-29 review stays as it is.

## 5. If publication fails

Stop further rollout and identify each affected URL and revision. The preserved identities to restore
are `main` `01e394d475202bb44a226f2ac5403aa084dc5b4c` (Pages `d1227c0f…`) and Space revision
`59d941825755bf73eabb7ff20e31124fee305755` (bundle `b046c69b…`). No force-push, history rewrite or
MLflow change is part of any recovery; a rollback is its own Owner action.

## 6. Open advisories carried with this packet

The editorial advisories E1–E5 (`editorial.md`), the fresh reader's observations and answer 6
(`fresh-reader.md`), and any recommendation in `integration.md`. None is a violation of an
effective rule.
