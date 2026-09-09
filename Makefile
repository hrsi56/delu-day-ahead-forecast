.PHONY: audit spectral sql test

test:
	uv run pytest -q

audit:
	uv run python scripts/audit_snapshot.py
	uv run python scripts/audit_delivery_day_features.py

spectral:
	uv run python scripts/generate_spectral_artifacts.py

sql:
	uv run python scripts/run_sql_artifact.py
