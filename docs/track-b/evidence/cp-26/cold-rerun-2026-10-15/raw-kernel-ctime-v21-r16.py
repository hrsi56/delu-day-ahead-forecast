"""CP-26-only bootstrap: use psutil's existing clock-stable Darwin birth time.

The core supervisor and scientific sources remain byte-identical. New process
trees use the same raw birth timestamp psutil itself uses to detect PID reuse.
No timestamp tolerance, PID-only match, OS clock setting or dependency file edit
is introduced. The expected bootstrap hash travels in every rewritten command.
"""
import time
BEGAN = time.monotonic()
import hashlib
import importlib
import json
from pathlib import Path
import runpy
import subprocess
import sys

import psutil

SELF = Path(__file__).resolve()
LOCKED_PREFIX = Path('/Users/djourno/Downloads/PJM/.venv')
PINS = {
    '__init__.py': 'd138a5786b163b56ba86ea0b2d5589dfca37e1bcdf8de1057fe1e933d6ab808a',
    '_psosx.py': '89f0ea0e9c1fe38f224b612792bf31d07c8880d79281806e5379c00514f6b3f2',
}


def install(expected_sha):
    assert sys.platform == 'darwin' and Path(sys.prefix) == LOCKED_PREFIX
    assert hashlib.sha256(SELF.read_bytes()).hexdigest() == expected_sha
    for name, digest in PINS.items():
        assert hashlib.sha256((Path(psutil.__file__).parent / name).read_bytes()).hexdigest() == digest
    assert psutil.__version__ == '7.2.2'

    def raw_birth(proc):
        # This is precisely the OSX branch of psutil.Process._get_ident().
        # Read afresh, retaining its native NoSuchProcess/AccessDenied behavior.
        return proc._proc.create_time(monotonic=True)

    psutil.Process.create_time = raw_birth
    parent_popen = subprocess.Popen

    class CP26Popen(parent_popen):
        def __init__(self, args, *positional, **kwargs):
            if (isinstance(args, (list, tuple)) and len(args) >= 4
                    and list(args[1:4]) == ['-B', '-m', 'cp26.supervisor']
                    and Path(args[0]).resolve() == Path(sys.executable).resolve()):
                args = [sys.executable, '-B', str(SELF), '--sha', expected_sha,
                        'module', 'cp26.supervisor', *args[4:]]
            super().__init__(args, *positional, **kwargs)

    # Only the existing CP-26 supervisor-module invocations are rewritten.
    # This adds no processes, scheduler, fit threads or worker allocation.
    subprocess.Popen = CP26Popen


def main():
    args = sys.argv[1:]
    assert len(args) >= 4 and args[0] == '--sha'
    expected, mode, target, rest = args[1], args[2], args[3], args[4:]
    assert mode in ('script', 'module', 'code')
    install(expected)
    print(json.dumps({'status': 'CP26_RAW_KERNEL_BIRTH_BOOTSTRAP',
                      'bootstrap_sha256': expected,
                      'clock_basis': 'darwin-raw-kernel-birth-v1',
                      'entry_mode': mode,
                      'setup_seconds': time.monotonic() - BEGAN}), flush=True)
    if mode == 'module':
        assert target == 'cp26.supervisor'
        sys.path.insert(0, str(Path.cwd() / 'src'))
        sys.argv = [target, *rest]
        supervisor = importlib.import_module(target)
        # Include this bootstrap's setup in the existing supervisor wall clock.
        supervisor._SUPERVISOR_BEGAN = BEGAN
        try:
            return supervisor.main()
        except Exception as exc:
            print(f'{type(exc).__name__}: {supervisor.redact(str(exc))}', file=sys.stderr)
            return 70
    if mode == 'script':
        path = Path(target).resolve()
        assert path.is_relative_to(Path.cwd().resolve()) and path.suffix == '.py'
        sys.argv = [str(path), *rest]
        runpy.run_path(str(path), run_name='__main__')
    else:
        sys.argv = ['-c', *rest]
        exec(compile(target, '<cp26-monitored-code>', 'exec'), {'__name__': '__main__'})
    assert hashlib.sha256(SELF.read_bytes()).hexdigest() == expected
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
