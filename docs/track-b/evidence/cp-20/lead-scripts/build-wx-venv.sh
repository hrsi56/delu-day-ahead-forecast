#!/bin/zsh
set -euo pipefail
L=/Users/djourno/Downloads/PJM/.local
export UV_CACHE_DIR=$L/tmp/cp-20/uvcache
uv venv $L/artifacts/cp-20/wx-venv --python 3.13
uv pip install --python $L/artifacts/cp-20/wx-venv/bin/python -r reports/weather-admission/scripts/requirements.freeze.txt
$L/artifacts/cp-20/wx-venv/bin/python -c "import eccodes,numpy,requests; print('eccodes',eccodes.__version__,eccodes.codes_get_api_version(),'numpy',numpy.__version__,'requests',requests.__version__)"
