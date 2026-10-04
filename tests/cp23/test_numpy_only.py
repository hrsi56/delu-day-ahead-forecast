"""§21.3 import audit: DDNN's model code imports NumPy and the standard library only, and a fixture
that imports a framework fails the audit (the positive control)."""
from pathlib import Path

import pytest

from cp23.audit import AUDITED, audit, violations

ROOT = Path(__file__).resolve().parents[2]


def test_ddnn_imports_numpy_and_the_standard_library_only():
    result = audit(ROOT)
    assert result['passed'], result
    assert set(AUDITED) == set(result['modules'])
    assert 'numpy' in result['modules']['src/cp23/ddnn.py']['imports']


@pytest.mark.parametrize('source, offender', [
    ('import torch\n', 'torch'),
    ('from torch import nn\n', 'torch'),
    ('import numpy as np\ndef f():\n    import tensorflow\n', 'tensorflow'),
    ('import importlib\nimportlib.import_module("jax.numpy")\n', 'jax'),
    ('x = __import__("keras")\n', 'keras'),
    ('import scipy.stats\n', 'scipy'),
    ('from . import helpers\n', '.helpers'),
])
def test_a_framework_or_other_numerical_import_fails_the_audit(source, offender):
    assert violations(source) == [offender]


def test_numpy_and_standard_library_imports_pass():
    assert violations('from __future__ import annotations\nimport math, hashlib\nfrom statistics import NormalDist\n'
                      'import numpy as np\n') == []
