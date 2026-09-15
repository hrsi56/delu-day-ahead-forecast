# Deployment — owner-only

Nothing in this repository publishes anything. Every step below is the owner's, and each is
reversible.

**Current state (M3.5/CP-3B).** GitHub Pages is **live** at
<https://hrsi56.github.io/delu-day-ahead-forecast/> — the primary link, which fetches nothing and
cannot fail when a CDN does. The interactive demo is **built and verified locally** as a Hugging Face
**Static** Space and awaits the one step below.

Why Static: on 2026-07-08 Hugging Face moved the Docker and Gradio SDKs behind a paid plan, and a free
Docker Space sleeps. A Static Space executes nothing on the server — the champion runs in the
visitor's browser under Pyodide — so there is nothing to put to sleep. The container remains runnable
locally as verified evidence (`make container-verify`); it is not what gets hosted.

---

## The one remaining step — create and upload the Static Space (about ten minutes, mostly upload)

The account is **`Yarden-Viktor`**. Every surface already links
`https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast`, so the owner and name below
must match exactly.

### 1. The Space already exists — confirm it

As of 2026-09-15 00:37 UTC, `Yarden-Viktor/delu-day-ahead-forecast` exists on Hugging Face as a
**Static**, **public** Space holding only Hugging Face's template files (`.gitattributes`,
`README.md`, `index.html`, `style.css`). This checkpoint did not create it — nothing here calls
Hugging Face. Confirm it is still Static and public:

```bash
curl -s https://huggingface.co/api/spaces/Yarden-Viktor/delu-day-ahead-forecast | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['sdk'], 'private' if d['private'] else 'public')"
```

It should print `static public`. If the Space was deleted, recreate it at
<https://huggingface.co/new-space>: owner `Yarden-Viktor`, name `delu-day-ahead-forecast`, SDK
**Static**, **Public**.

The upload below replaces the template's `index.html` and `README.md` and adds everything else;
`style.css` from the template is unused and harmless.

### 2. Build the directory

```bash
make wasm
```

That regenerates the browser payload from the committed champion, re-proves the model-identity gate,
exports the notebook with `marimo export html-wasm`, and assembles **`dist/space-wasm/`** — about 38 MB
uncompressed across ~740 files (served uncompressed — Hugging Face does not compress Static Spaces, so the nine boosters ship gzipped at rest): `index.html`, marimo's `assets/`, `public/` (the nine boosters, the row
slice, the equivalence fixture, `browser_champion.py`), the Space card as `README.md` with
`sdk: static`, and `.gitattributes` routing binary assets through LFS. It exits non-zero if the bundle
is malformed, if the shipped module differs from the verified one, or if any internal file leaked into
it.

Optional but worth thirty seconds — see it work before uploading:

```bash
make wasm-serve
```

and open <http://127.0.0.1:8820>. It must be served over HTTP; `file://` cannot run a WASM notebook.
First load takes a while: it downloads the Python runtime.

### 3. Upload it

The simplest route handles LFS for you:

```bash
hf auth login
hf upload Yarden-Viktor/delu-day-ahead-forecast dist/space-wasm . --repo-type space
```

Or with git, from inside `dist/space-wasm`:

```bash
git init -b main
git lfs install
git add -A
git commit -m "Deploy the DE-LU day-ahead champion as a Static Space"
git remote add origin https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast
git push -u origin main
```

Authenticate with a Hugging Face **write** token when asked. Agents never enter tokens.

**The URL that then exists:**

> <https://huggingface.co/spaces/Yarden-Viktor/delu-day-ahead-forecast>

A Static Space has no build step, so it is live as soon as the upload finishes.

### 4. Check it

Two URLs will work: the Space page, which wraps the app in Hugging Face's own chrome, and the app
itself at <https://yarden-viktor-delu-day-ahead-forecast.static.hf.space/>, which loads nothing but
the app.

Open it in a private window. Within about a minute the page should show the fan chart, both controls
should respond, the *historical out-of-sample replay* label should sit above the chart, and the
identity panel should read **bitwise identical** with a maximum absolute deviation of **0.0** over 54
delivery days. The download table at the bottom reports what the visit cost.

Then:

```bash
uv run python scripts/check_links.py
```

should report `unresolved: []`.

---

## What does **not** need doing

- **No secret, anywhere.** The Static Space needs no token, no tracking URI, no API key. It makes no
  call to ENTSO-E, SMARD or any model registry.
- **No keep-alive, on any platform** — and none would help: a Static Space has nothing to keep alive.
- **No refresh schedule.** The release is frozen.
- **No MLflow step.** The champion is already registered as `delu-day-ahead-champion` version 1 under
  the `champion` alias, anonymously readable at
  <https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow>.

## After the Space is live

The README's CP-3 section says the Space "awaits the owner's deploy". Update that sentence in
`scripts/cp3_readme.py` — the generator, never `README.md` itself — then `make readme-cp3 verify`.

## Link discipline, one warning

Link the experiment tracking **only** as <https://dagshub.com/hrsi56/delu-day-ahead-forecast.mlflow>.
The DagsHub repository root, `/experiments`, `/models` and `/src/main` all redirect an anonymous visitor
to a sign-in page. `make verify` fails if one appears on any surface in this repository — but it cannot
see the CV or LinkedIn.
