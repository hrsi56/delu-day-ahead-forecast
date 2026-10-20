"""One monitored affected r16 boundary/transition check; no model work."""
import os,sys,json
from pathlib import Path
ROOT=Path.cwd();sys.path.insert(0,str(ROOT/'src'))
from cp26 import budget as B,gates as G,harness as H
import pytest
assert os.environ.get('CP26_RUN_ID') == G.RUN_ID
args=['-q','tests/test_cp26_r16.py','tests/test_cp26_gates.py','tests/test_cp26_costing.py',
      'tests/test_cp26_r15.py::test_general_boundary_remains436point5_with500_actual',
      'tests/test_cp26_r15.py::test_shutdown_exposure_is_reserved_headroom_not_another_charge',
      '--basetemp',str(H.art()/G.LOCAL_NAME/'r16/pytest')]
run_id=os.environ.pop('CP26_RUN_ID')
try: result=int(pytest.main(args))
finally: os.environ['CP26_RUN_ID']=run_id
if not result:
    H.identities(ROOT);H.runtime_lineage(ROOT)
    from cp26.parity import require_pass
    require_pass(ROOT,output=G.OUTPUT/'parity.json')
record={'status':'PASS' if result==0 else 'FAIL','exit_code':result,'command':['pytest.main',*args],
        'code_sha256':G.code_identity(ROOT),'protocol':G.protocol_identity(ROOT),
        'job_id':os.environ['CP26_JOB_ID'],'job_index':int(os.environ['CP26_JOB_INDEX']),
        'run_id':G.RUN_ID,'prior_checks_reused':'49 r15 affected checks and96 parity checks; unchanged calibrated supervision'}
B.atomic(ROOT/G.RUN_EVIDENCE/'checks-v21-r16.json',record)
B.atomic(ROOT/G.OUTPUT/'preparation-tests-v21-r16.json',record)
raise SystemExit(result)
