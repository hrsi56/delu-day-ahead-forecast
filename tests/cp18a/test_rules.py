"""R7's rule, the workflow's shape, the fallback's agent file, and the activity that keeps a schedule enabled."""
from __future__ import annotations

from pathlib import Path
import plistlib
import re


from cp18 import r7

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / '.github/workflows/daily.yml'
PLIST = ROOT / 'reports/cp18a/launchd/com.delu.daily-fallback.plist'


# ---- R7 ----------------------------------------------------------------------------------------------------------

def test_r7_a_raised_error_is_a_refused_record():
    def raising(files):
        raise KeyError('delivery_day')
    result = r7.verify({'manifest.json': b'{}'}, verifier=raising)
    assert result == {'accepted': False, 'raised': 'KeyError',
                      'problems': ['the verifier raised KeyError: the record is refused (R7)']}


def test_r7_listed_faults_refuse_and_a_clean_list_accepts():
    assert r7.verify({}, verifier=lambda files: ['x: absent'])['accepted'] is False
    assert r7.verify({}, verifier=lambda files: [])['accepted'] is True
    real = r7.verify({'manifest.json': b'not json'})           # the frozen verifier on garbage: refused either way
    assert real['accepted'] is False


def test_the_pipeline_calls_verify_bundle_only_through_r7():
    sources = sorted((ROOT / 'src/cp18').rglob('*.py'))
    direct = [str(p.relative_to(ROOT)) for p in sources
              if p.name != 'r7.py' and re.search(r'\bverify_bundle\b', p.read_text())]
    assert direct == []


# ---- the workflow ------------------------------------------------------------------------------------------------

def test_the_workflow_is_dispatch_only_with_its_permissions_scoped():
    text = WORKFLOW.read_text()
    import yaml
    value = yaml.safe_load(text)
    triggers = value.get('on', value.get(True))
    assert list(triggers) == ['workflow_dispatch'] and 'schedule' not in text.split('\non:')[1].split('\npermissions')[0]
    assert value['permissions'] == {}
    job = value['jobs']['pipeline']
    assert job['runs-on'] == 'macos-26' and job['permissions'] == {'contents': 'write'}
    assert 'timeout-minutes' in job
    uses = [s['uses'] for s in job['steps'] if 'uses' in s]
    assert uses and all(re.fullmatch(r'[\w-]+/[\w-]+@[0-9a-f]{40}', u) for u in uses)
    assert all(s.get('with', {}).get('persist-credentials') is False for s in job['steps']
               if s.get('uses', '').startswith('actions/checkout'))
    assert '${{ secrets.' not in text                                  # this round creates and uses no secret
    run = next(s for s in job['steps'] if s.get('name', '').startswith('The pipeline'))
    assert run['env'] == {'NOW': '${{ inputs.now }}', 'INPUTS': '${{ inputs.inputs }}'}   # never interpolated into the script
    assert '${{' not in run['run']


def test_the_fallback_agent_file_is_well_formed_and_carries_no_credential():
    value = plistlib.loads(PLIST.read_bytes())
    assert value['Label'] == 'com.delu.daily-fallback' and value['RunAtLoad'] is False
    assert value['ProgramArguments'][1:4] == ['-m', 'cp18.local', 'run']
    names = ('ENTSOE_API_TOKEN', 'HF_TOKEN', 'DAGSHUB_USER_TOKEN', 'MLFLOW_TRACKING_PASSWORD')
    assert not any(n in value['EnvironmentVariables'] for n in names)
    assert value['StartCalendarInterval'] == {'Hour': 13, 'Minute': 30}
