"""Local CP-16 driver; every compute command is run through --monitor."""
from __future__ import annotations
import argparse
import os
from pathlib import Path
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
for name in ('OPENBLAS_NUM_THREADS','VECLIB_MAXIMUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[name]='1'
from cp16.budget import Budget, atomic, CAPS


def checkpoint_bytes(paths):
    """Atomic evidence renames may remove a file after directory enumeration."""
    total=0
    for base in paths:
        if not base.exists():continue
        for path in base.rglob('*'):
            try:
                if path.is_file() and not path.is_symlink():total+=path.stat().st_size
            except FileNotFoundError:
                continue
    return total


def monitor(args):
    import psutil
    budget=Budget(args.ledger)
    if not args.command: raise ValueError('missing command to monitor')
    command=args.command[1:] if args.command[0]=='--' else args.command
    ledger=budget.read() if args.ledger.exists() else None
    if ledger and any(x.get('running') for x in ledger['jobs']):
        raise RuntimeError('unreconciled job: refuse restart rather than erase accounting')
    began=time.monotonic();started=time.time()
    with budget.transaction() as state:
        if state['counts'].get('machine_seconds',0)>=CAPS['machine_seconds']:raise RuntimeError('machine cap exhausted')
        state['jobs'].append({'command':command,'start_epoch':started,'running':True})
        job_index=len(state['jobs'])-1
    args.log.parent.mkdir(parents=True,exist_ok=True)
    peak=0;disk_peak=0;reason=None;last_tick=began;supervisor_error=None
    try:
        with args.log.open('w') as log:
            proc=subprocess.Popen(command,cwd=ROOT,env={**os.environ,'PYTHONPATH':str(ROOT/'src'),
                'CP16_LEDGER':str(args.ledger),'PYTHONDONTWRITEBYTECODE':'1'},stdout=log,stderr=subprocess.STDOUT,
                start_new_session=True)
            parent=psutil.Process(proc.pid)
            while True:
                now=time.monotonic();delta=now-last_tick;last_tick=now
                with budget.transaction() as state:
                    state['counts']['machine_seconds']=state['counts'].get('machine_seconds',0)+delta
                    state['jobs'][job_index]['charged_seconds']=now-began
                    elapsed=now-began
                    if state['counts']['machine_seconds']>=CAPS['machine_seconds']:reason='machine_seconds'
                    # Conservative wall-clock upper bound also protects the active-effort ceiling.
                    if time.time()-state['created_epoch']>=CAPS['active_seconds']:reason='active_seconds'
                try:
                    processes=[parent,*parent.children(recursive=True),psutil.Process()]
                    rss=sum(p.memory_info().rss for p in processes if p.is_running())
                    peak=max(peak,rss)
                    if rss>=CAPS['rss_bytes']:reason='rss_bytes'
                except psutil.NoSuchProcess:pass
                if args.project_root:
                    # Counting the entire pre-existing Git store is conservative;
                    # it includes every byte of new candidate/evidence history.
                    paths=[args.project_root/'.git',args.project_root/'.local/worktrees/cp-16',args.project_root/'.local/artifacts/cp-16',args.project_root/'.local/tmp/cp-16']
                    disk=checkpoint_bytes(paths)
                    disk_peak=max(disk_peak,disk)
                    if disk>=CAPS['additional_disk_bytes']:reason='additional_disk_bytes'
                if reason:
                    import signal
                    os.killpg(proc.pid,signal.SIGTERM)
                    try:proc.wait(timeout=5)
                    except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
                    break
                if proc.poll() is not None:break
                time.sleep(.2)
    except BaseException as exc:
        supervisor_error=repr(exc)
        # A failed monitor must not leave a fit running without resource guards.
        if 'proc' in locals() and proc.poll() is None:
            import signal
            os.killpg(proc.pid,signal.SIGTERM)
            try:proc.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
        raise
    finally:
        with budget.transaction() as state:
            state['counts']['machine_seconds']=state['counts'].get('machine_seconds',0)+time.monotonic()-last_tick
            state['jobs'][job_index].update(running=False,exit_code=proc.returncode if 'proc' in locals() else None,
                elapsed_seconds=time.monotonic()-began,peak_process_tree_rss_bytes=peak,
                peak_checkpoint_disk_bytes=disk_peak,abort_reason=reason,supervisor_error=supervisor_error,log=str(args.log))
    print({'exit_code':proc.returncode,'elapsed_seconds':time.monotonic()-began,'peak_rss_bytes':peak,'abort_reason':reason},flush=True)
    return proc.returncode if not reason else 3


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--monitor',action='store_true');ap.add_argument('--ledger',type=Path,required=True)
    ap.add_argument('--project-root',type=Path);ap.add_argument('--log',type=Path)
    ap.add_argument('--job',choices=['preflight','admission','comparison','score','controls','verify'])
    ap.add_argument('--output',type=Path,default=ROOT/'reports/v2-causal')
    ap.add_argument('--scratch',type=Path);ap.add_argument('command',nargs=argparse.REMAINDER)
    args=ap.parse_args()
    if args.monitor:return monitor(args)
    if args.job=='preflight':
        from cp16.preflight import run
        run(ROOT,args.output);return 0
    from cp16.execution import execute
    execute(ROOT,args);return 0

if __name__=='__main__':raise SystemExit(main())
