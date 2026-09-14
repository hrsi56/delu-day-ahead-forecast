.PHONY: audit spectral sql test train benchmark holdout diagnostics report readme cp2 \
        pages space register showcase cli container container-verify readme-cp3 verify cp3 \
        wasm-payload wasm wasm-serve cp3b

test:
	uv run pytest -q

audit:
	uv run python scripts/audit_snapshot.py
	uv run python scripts/audit_delivery_day_features.py

spectral:
	uv run python scripts/generate_spectral_artifacts.py

sql:
	uv run python scripts/run_sql_artifact.py

# --- CP-2: model, calibration and analysis --------------------------------
# Run in this order. `holdout` freezes the artifact and opens the 90-day
# evaluation; nothing after it may change a model or a threshold.
train:
	uv run python scripts/cp2_development.py

benchmark:
	uv run python scripts/cp2_benchmark_a69.py

holdout:
	uv run python scripts/cp2_final_holdout.py

diagnostics:
	uv run python scripts/cp2_diagnostics.py

report:
	uv run python scripts/cp2_report.py

readme:
	uv run python scripts/cp2_readme.py

cp2: train benchmark holdout diagnostics report readme

# --- CP-3: showcase and release -------------------------------------------
# Nothing here deploys. `space` assembles the directory the owner pushes; the
# owner pushes it. Pages is enabled by the owner in repository settings.
pages:
	uv run python scripts/build_pages.py

space:
	uv run python scripts/build_space.py

readme-cp3:
	uv run python scripts/cp3_readme.py

# §9.1 registration is NON-GATING: a registry or metadata failure is disclosed
# in reports/cp3/mlflow_registration.json and the release proceeds.
register:
	uv run python scripts/register_champion.py

cli:
	uv run python predict_next_day.py --level 80 --self-check

showcase:
	uv run marimo run app/showcase.py

container:
	docker build -t delu-showcase:latest .
	docker run --rm -p 7860:7860 delu-showcase:latest

# Build the image and exercise it with the network disabled, recording the run
# in reports/cp3/container_check.json rather than describing it.
container-verify:
	uv run python scripts/verify_container.py

# The cross-surface agreement check, the zero-runtime-calls scan and the
# delivery-day boundary controls, printed as the table CP-3 item 5 asks for.
verify:
	uv run python scripts/verify_release.py

cp3: pages space readme-cp3 register verify

# --- M3.5/CP-3B: the WASM showcase ----------------------------------------
# The browser payload is derived from the committed champion, never committed
# itself. `make test` needs it; CI builds it before pytest.
wasm-payload:
	uv run python scripts/build_wasm_payload.py

wasm: wasm-payload
	uv run python scripts/build_wasm_space.py

# Serve the export locally. html-wasm REQUIRES http:// -- file:// cannot work.
wasm-serve:
	@echo "serving dist/space-wasm at http://127.0.0.1:8820 (ctrl-c to stop)"
	cd dist/space-wasm && uv run python -m http.server 8820 --bind 127.0.0.1

cp3b: wasm verify
