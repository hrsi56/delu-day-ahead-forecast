"""The committed PyTorch reference record (§21.3): it passed, with nothing skipped, for the current
DDNN implementation, the frozen tolerances and the pinned test-only build. The reference itself runs
only in the recorded ``reference-checks`` job; this default-suite test makes a changed
``src/cp23/ddnn.py`` without a new passing record a red check."""
import json
from pathlib import Path

from cp15.data import sha
from cp23.reference import CHECK_FILE, DDNN_FILE, EXPECTED_PASSED, RECORD, REFERENCE_TOLERANCES, require_passing_record

ROOT = Path(__file__).resolve().parents[2]


def test_the_reference_passed_for_the_current_ddnn_code_with_nothing_skipped():
    record = require_passing_record(ROOT)
    assert record['passed'] and record['exit_code'] == 0
    counts = record['counts']
    assert counts['passed'] == EXPECTED_PASSED
    assert all(counts[k] == 0 for k in ('failed', 'skipped', 'deselected', 'errors', 'xfailed', 'xpassed'))
    assert record['ddnn_sha256'] == sha(ROOT / DDNN_FILE)
    assert record['check_file_sha256'] == sha(ROOT / CHECK_FILE)
    assert record['tolerances'] == REFERENCE_TOLERANCES
    assert record['versions']['torch'] == '2.14.1'
    assert record['torch_lock_sha256'] == sha(ROOT / 'tests/cp23/torch-reference/uv.lock')
    assert all(v['max_error_to_bound'] <= 1 for v in record['max_observed_errors'].values())


def test_a_changed_ddnn_implementation_is_refused(tmp_path):
    (tmp_path / 'src/cp23').mkdir(parents=True)
    (tmp_path / RECORD).parent.mkdir(parents=True)
    (tmp_path / RECORD).write_text((ROOT / RECORD).read_text())
    (tmp_path / DDNN_FILE).write_text((ROOT / DDNN_FILE).read_text() + '\n# changed\n')
    try:
        require_passing_record(tmp_path)
    except RuntimeError as exc:
        assert 'changed since' in str(exc)
    else:
        raise AssertionError('a changed DDNN implementation must be refused')
    record = json.loads((ROOT / RECORD).read_text())
    record['passed'] = False
    (tmp_path / RECORD).write_text(json.dumps(record))
    (tmp_path / DDNN_FILE).write_text((ROOT / DDNN_FILE).read_text())
    try:
        require_passing_record(tmp_path)
    except RuntimeError as exc:
        assert 'failed' in str(exc)
    else:
        raise AssertionError('a failed reference must block DDNN results')
