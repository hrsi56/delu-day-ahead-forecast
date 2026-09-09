#!/usr/bin/env python3
"""Execute the committed DuckDB SQL views and print their quality checks."""

from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    connection = duckdb.connect(database=":memory:")
    connection.execute((ROOT / "sql" / "feature_queries.sql").read_text(encoding="utf-8"))
    print("data_quality_checks")
    print(connection.execute("SELECT * FROM data_quality_checks").fetchdf().to_string(index=False))
    print("source_bin_checks")
    print(connection.execute("SELECT * FROM source_bin_checks").fetchdf().to_string(index=False))
    print("feature_views")
    print(connection.execute("SELECT (SELECT count(*) FROM lag_features) AS lag_rows, (SELECT count(*) FROM rolling_features) AS rolling_delivery_days").fetchdf().to_string(index=False))


if __name__ == "__main__":
    main()
