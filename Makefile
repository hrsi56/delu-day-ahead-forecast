.PHONY: audit spectral sql test

test:
	uv run pytest -q

audit:
	uv run python scripts/audit_snapshot.py

spectral:
	uv run python scripts/generate_spectral_artifacts.py

sql:
	uv run python scripts/run_sql_artifact.py
