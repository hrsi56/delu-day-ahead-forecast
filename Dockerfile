# Multi-stage image for the marimo showcase (§9.2).
#
# Stage 1 resolves the locked dependency set; stage 2 adds the application code,
# the committed data snapshot and the bundled champion. The champion is IN THE
# IMAGE: there is no registry-first runtime path, no DagsHub token as a secret,
# and no live ENTSO-E/SMARD call during a user session. MLflow remains public
# experiment evidence, never a runtime dependency.
#
# marimo runs in SERVER mode (`marimo run`), not WASM.

# ---------- stage 1: locked dependencies ------------------------------------
FROM python:3.13-slim AS deps

COPY --from=ghcr.io/astral-sh/uv:0.12.6 /uv /usr/local/bin/uv

ENV UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /build
COPY pyproject.toml uv.lock ./
# `src/` must exist for the project's own wheel build; the real code arrives in
# stage 2, so only the dependency closure is cached here.
RUN mkdir -p src/delu_forecast src/spike \
 && touch src/delu_forecast/__init__.py src/spike/__init__.py \
 && printf '# placeholder\n' > README.md \
 && uv sync --locked --no-dev --no-editable

# ---------- stage 2: application --------------------------------------------
FROM python:3.13-slim AS app

# libgomp is LightGBM's OpenMP runtime; the slim base does not carry it.
RUN apt-get update \
 && apt-get install -y --no-install-recommends libgomp1 \
 && rm -rf /var/lib/apt/lists/*

# Hugging Face Spaces runs the container as uid 1000. Own the tree so marimo can
# write its own cache without root.
RUN useradd --create-home --uid 1000 showcase

COPY --from=deps --chown=showcase:showcase /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH=/app/src \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MLFLOW_DISABLE_AGENT_HINT=1 \
    MPLCONFIGDIR=/tmp/matplotlib \
    HOME=/home/showcase

WORKDIR /app
COPY --chown=showcase:showcase pyproject.toml uv.lock predict_next_day.py ./
COPY --chown=showcase:showcase src/ ./src/
COPY --chown=showcase:showcase app/ ./app/
COPY --chown=showcase:showcase sql/ ./sql/
# The bundled champion and the frozen snapshot: the two things that make this a
# release rather than a demo that phones home.
COPY --chown=showcase:showcase models/champion/ ./models/champion/
COPY --chown=showcase:showcase data/snapshot.parquet data/snapshot.sha256 data/partitions.json data/README.md ./data/
# Committed figures and metric tables the §10 reading order renders.
COPY --chown=showcase:showcase reports/ ./reports/

USER showcase

# HF Spaces' Docker SDK default. `app_port` in the Space card must match.
EXPOSE 7860

HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
  CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:7860/health', timeout=4).status==200 else 1)"

CMD ["marimo", "run", "app/showcase.py", "--host", "0.0.0.0", "--port", "7860", "--headless", "--no-token"]
