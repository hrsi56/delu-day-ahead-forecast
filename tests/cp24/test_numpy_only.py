"""The NumPy-only import audit (capstone v21-r11 §23.7): DDNN-2's model code and its search import NumPy
and the standard library only, and a fixture that imports a framework fails the audit."""
from pathlib import Path

from cp24.audit import AUDITED, audit, violations

ROOT = Path(__file__).resolve().parents[2]


def test_ddnn2_and_the_search_import_numpy_and_the_standard_library_only():
    result = audit(ROOT)
    assert set(result['modules']) == set(AUDITED) == {'src/cp24/ddnn2.py', 'src/cp24/sampler.py'}
    assert result['passed'], result
    assert 'numpy' in result['modules']['src/cp24/ddnn2.py']['imports']


def test_a_framework_fixture_fails_the_audit():
    for fixture in ('import torch\n', 'from tensorflow import keras\n', 'import jax.numpy as jnp\n',
                    'def f():\n    import sklearn\n', "import importlib\nimportlib.import_module('optuna')\n",
                    "__import__('pandas')\n", 'from .design import build\n', 'from scipy import special\n'):
        assert violations(fixture), fixture


def test_numpy_the_stdlib_and_the_audited_model_pass():
    assert violations('import math\nimport numpy as np\nfrom statistics import NormalDist\nfrom . import ddnn2\n') == []
