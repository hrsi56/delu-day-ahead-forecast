# Deployment — owner-only, two steps

CP-3 built and verified every release artifact locally. **Nothing was published:**
no Space was created, GitHub Pages was not enabled, and nothing was pushed. Both
steps below are the owner's, and each is reversible.

Do them in this order. Pages first, because the Space card links it.

---

## Step 1 — enable GitHub Pages (about one minute)

The page is already committed at [`docs/index.html`](index.html), together with a
`docs/.nojekyll` so GitHub serves the file as-is instead of running Jekyll over it.

1. Open <https://github.com/hrsi56/delu-day-ahead-forecast/settings/pages>.
2. **Source:** *Deploy from a branch*.
3. **Branch:** `main`, **folder:** `/docs`. Save.
4. Wait for the green check on the Pages deployment (usually under a minute).

**The URL that then exists:**

> <https://hrsi56.github.io/delu-day-ahead-forecast/>

This is the primary recruiter URL — the one on the CV and LinkedIn. It is static,
CDN-served, cannot sleep, and performs zero runtime calls.

**Check after deploying:** open it in a private window and confirm the fan chart
renders and both controls respond. If anything looks wrong, the same file opens
locally with `open docs/index.html` — what you see there is what Pages serves.

---

## Step 2 — create and push the Hugging Face Space (about ten minutes, mostly upload)

### 2a. Create the Space

1. Open <https://huggingface.co/new-space>.
2. **Owner:** `hrsi56`. **Space name:** `delu-day-ahead-forecast`.
3. **SDK:** *Docker* → *Blank*. **Hardware:** *CPU basic* (free). **Visibility:** *Public*.
4. Create. Leave it empty; the next step fills it.

### 2b. Build the bundle

```bash
make space
```

That writes `dist/space/` (gitignored — it is a copy of committed files, never a
second source of truth): the `Dockerfile`, the Space card as `README.md` with its
front-matter, `src/`, `app/`, `sql/`, `predict_next_day.py`, `models/champion/`,
`data/snapshot.parquet` and the committed `reports/` figures and tables. About
37 MB.

### 2c. Push it

`models/champion/python_model.pkl` is ~30 MB, so the Hub wants it through LFS.
`make space` already writes the matching `.gitattributes` into the bundle.

```bash
cd dist/space
git init -b main
git lfs install
git add -A
git commit -m "Deploy the frozen DE-LU day-ahead champion"
git remote add origin https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast
git push -u origin main
```

Authenticate with a Hugging Face **write** token when prompted (username
`hrsi56`, password = the token), or run `huggingface-cli login` first.

**The URL that then exists:**

> <https://huggingface.co/spaces/hrsi56/delu-day-ahead-forecast>

The first build takes roughly 10–15 minutes — it installs the locked dependency
set and copies the bundled model. Watch the **Logs** tab; the Space is up when
marimo prints `URL: http://0.0.0.0:7860`.

**Check after deploying:** the app loads, the quantile-level selector switches
between 50 / 80 / 95 %, the load-forecast slider redraws the fan, and the
*historical out-of-sample replay* label is visible above the chart.

---

## What does **not** need doing

- **No secret, on either platform.** The champion and the snapshot are bundled in
  the image. The Space needs no DagsHub token, no ENTSO-E token, and no MLflow
  tracking URI; it never queries the registry and makes no live API call during a
  user session.
- **No keep-alive, on any platform.** The free tier sleeps after inactivity and
  takes about 30 s to wake. That is disclosed wherever the Space is linked and is
  never on the path of a first visit, because the static page carries the first
  touch and cannot sleep.
- **No refresh schedule.** The release is frozen. A future manual refresh is
  permitted but never required.
- **No MLflow step.** The champion is already registered as
  `delu-day-ahead-champion` version 1 with the `champion` alias and 35
  release/lineage tags, and it is anonymously readable at
  <https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow>.

## After both steps

Both URLs are already written into the README, the static page and the Space
card, so nothing needs editing once they resolve — except the one
**Deployment status** line in the README's CP-3 section, which says they are not
yet live. Delete that line.

Then rebuild and re-verify, which should report no change:

```bash
make verify
```

## Link discipline, one warning

Link the experiment tracking **only** as
<https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow>. Verified from an
unauthenticated client on 2026-09-14: the DagsHub repository root, `/experiments`,
`/models` and `/src/main` all answer `302 → /user/login` for a connected
repository. A link to any of those lands a hiring manager on a sign-in page.
`make verify` and `tests/test_17_cross_surface_agreement.py` fail if one appears
on any surface — including on the CV and LinkedIn, which the tests cannot see.
