"""The committed PyTorch reference record (§23.7): it passed, with nothing skipped, for the current DDNN-2
model code, the frozen tolerances and CP-23's pinned test-only build. The reference itself runs only in
the recorded ``reference-checks`` job; this default-suite test makes a changed ``src/cp24/ddnn2.py``
without a new passing record a red check."""
import json
from pathlib import Path

from cp15.data import sha
from cp24.reference import (CHECK_FILE, EXPECTED_PASSED, LOCK_FILE, LOCK_SHA256, MODEL_FILE, PINNED_TORCH, RECORD,
                            REFERENCE_TOLERANCES, require_passing_record)

ROOT = Path(__file__).resolve().parents[2]


def test_the_reference_passed_for_the_current_model_code_with_nothing_skipped():
    record = require_passing_record(ROOT)
    assert record['passed'] and record['exit_code'] == 0
    counts = record['counts']
    assert counts['passed'] == EXPECTED_PASSED
    assert all(counts[k] == 0 for k in ('failed', 'skipped', 'deselected', 'errors', 'xfailed', 'xpassed'))
    assert record['model_sha256'] == sha(ROOT / MODEL_FILE)
    assert record['check_file_sha256'] == sha(ROOT / CHECK_FILE)
    assert record['tolerances'] == REFERENCE_TOLERANCES
    assert record['versions']['torch'] == PINNED_TORCH
    assert record['torch_lock_sha256'] == LOCK_SHA256 == sha(ROOT / LOCK_FILE)
    assert all(v['max_error_to_bound'] <= 1 for v in record['max_observed_errors'].values())


def test_a_changed_model_or_a_failed_reference_is_refused(tmp_path):
    (tmp_path / 'src/cp24').mkdir(parents=True)
    (tmp_path / RECORD).parent.mkdir(parents=True)
    (tmp_path / RECORD).write_text((ROOT / RECORD).read_text())
    (tmp_path / MODEL_FILE).write_text((ROOT / MODEL_FILE).read_text() + '\n# changed\n')
    try:
        require_passing_record(tmp_path)
    except RuntimeError as exc:
        assert 'changed since' in str(exc)
    else:
        raise AssertionError('a changed DDNN-2 implementation must be refused')
    record = json.loads((ROOT / RECORD).read_text())
    record['passed'] = False
    (tmp_path / RECORD).write_text(json.dumps(record))
    (tmp_path / MODEL_FILE).write_text((ROOT / MODEL_FILE).read_text())
    try:
        require_passing_record(tmp_path)
    except RuntimeError as exc:
        assert 'failed' in str(exc)
    else:
        raise AssertionError('a failed reference must block DDNN-2 results')
