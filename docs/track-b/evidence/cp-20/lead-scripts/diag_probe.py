"""Diagnosis only: idle interface baseline, then one fresh-connection 4 MB non-target range per endpoint."""
import datetime as dt, json, os, socket, subprocess, time
from pathlib import Path
from cp20.budget import Budget, GIB
from cp20.gfs import aws_url, ncar_url
from cp20.net import Fetcher
def rx():
    f=subprocess.check_output(['netstat','-ib','-I','en0']).decode().splitlines()[1].split(); return int(f[6])
a=rx(); t=time.time(); time.sleep(5); idle=(rx()-a)/(time.time()-t)/1e6
out={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'idle_en0_rx_MBps':idle,
     'dns_aws':sorted({x[4][0] for x in socket.getaddrinfo('noaa-gfs-bdp-pds.s3.amazonaws.com',443)}),'tests':[]}
f=Fetcher(Budget(os.environ['CP20_LEDGER']), Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/weather/diag-requests.jsonl'), int(150*GIB))
run=dt.date(2023,5,2)
for ep,url in (('aws',aws_url(run,24)),('ncar',ncar_url(run,24)),('aws',aws_url(run,27))):
    t=time.time(); _,_,b=f.get(url,f'diagnosis {ep} fresh single connection',byte_range=(8_000_000,12_000_000-1)); e=time.time()-t
    out['tests'].append({'endpoint':ep,'bytes':len(b),'seconds':e,'MBps':len(b)/e/1e6})
    f._local.session=None
print(json.dumps(out)); Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/weather/diag-probe-%d.json'%int(time.time())).write_text(json.dumps(out,indent=1))
