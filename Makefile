.PHONY: audit spectral sql test train benchmark holdout diagnostics report cp2

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

cp2: train benchmark holdout diagnostics report
