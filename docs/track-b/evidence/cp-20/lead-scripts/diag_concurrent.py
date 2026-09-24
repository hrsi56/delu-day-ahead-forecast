"""Diagnosis only: AWS keep-alive lane concurrent with an NCAR lane, non-target ranges."""
import datetime as dt, json, os, threading, time
from pathlib import Path
from cp20.budget import Budget, GIB
from cp20.gfs import aws_url, ncar_url
from cp20.net import Fetcher
f=Fetcher(Budget(os.environ['CP20_LEDGER']), Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/weather/diag-requests.jsonl'), int(150*GIB))
run=dt.date(2023,5,3); res={'aws':[], 'ncar':[]}
def lane(ep, url):
    for k in range(3):
        t=time.time(); _,_,b=f.get(url, f'diagnosis concurrent {ep} {k}', byte_range=(8_000_000+k*4_000_000, 12_000_000+k*4_000_000-1))
        res[ep].append(round(len(b)/(time.time()-t)/1e6,3))
ts=[threading.Thread(target=lane,args=('aws',aws_url(run,24))), threading.Thread(target=lane,args=('ncar',ncar_url(run,24)))]
[t.start() for t in ts]; [t.join() for t in ts]
out={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'MBps_per_request':res}
print(json.dumps(out)); Path('/Users/djourno/Downloads/PJM/.local/artifacts/cp-20/weather/diag-concurrent-%d.json'%int(time.time())).write_text(json.dumps(out,indent=1))
