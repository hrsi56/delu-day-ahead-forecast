"""CP-15 preflight only. Exit 2 records missing archive support, not model failure."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from cp15.preflight import audit  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preflight', action='store_true', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    allowed = ROOT / 'reports/cp15'
    if ROOT == output or (ROOT in output.parents and output != allowed and allowed not in output.parents):
        raise ValueError('repository output must be under reports/cp15')
    # Audit before creating any output, and never overwrite a protocol.
    summary, windows = audit(ROOT)
    output.mkdir(parents=True, exist_ok=True)
    (output / 'preflight.json').write_text(json.dumps(summary, indent=2, sort_keys=True, allow_nan=False) + '\n')
    windows.to_csv(output / 'history-windows.csv', index=False)
    print(json.dumps({k: summary[k] for k in ('engineering_status', 'product_feasibility', 'model_fit_count')}))
    return 2 if summary['engineering_status'] == 'BLOCKED' else 0


if __name__ == '__main__':
    raise SystemExit(main())
