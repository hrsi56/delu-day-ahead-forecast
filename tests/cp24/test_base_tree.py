"""CP-24 changed no file that existed at its base (§23.13 item 16; §23.14): the public surfaces, the published export
set, `scripts/mlflow_export.py`, the root `pyproject.toml` and `uv.lock`, every earlier checkpoint's code, reports and
evidence, every locked document and `progress.md` are byte-identical to the base commit `522d7ea`."""
import json
from pathlib import Path

from cp24.basetree import CP24_PATHS, PATH, check

ROOT = Path(__file__).resolve().parents[2]


def test_every_base_file_is_unchanged():
    record = json.loads(PATH.read_text())
    assert record['base_commit'] == '522d7ea722b5d215d827d7aed9c56b7a9dec066e' and record['files'] == len(record['sha256'])
    for name in ('scripts/mlflow_export.py', 'pyproject.toml', 'uv.lock', 'README.md', 'docs/index.html', 'progress.md',
                 'capstone_v21.md', 'AGENTS.md', 'reports/presentation/mlflow-export/manifest.json', 'src/cp23/ddnn.py'):
        assert name in record['sha256'], name
    assert not any(name.startswith(CP24_PATHS) for name in record['sha256'])
    assert check(record) == []


def test_a_changed_file_is_caught():
    record = json.loads(PATH.read_text())
    tampered = {**record, 'sha256': {'README.md': '0' * 64}}
    assert check(tampered) == ['changed: README.md']
