#!/usr/bin/env python3
"""A stand-in for the Node.js binary in `cp17.daily.Host.command`: it hands back the reference run's own record.

Invoked as `fake_node.py <runner> fit <pyodide> <zip> <payloads> <stem> <attribution> <packages> <out.json>`.
`CP17C_FAKE_RECORDS` names a JSON {stem: record path}. The harness's bookkeeping, the chain's judgement and the
shadow states then run for real on the reference's results, in seconds and with no runtime present.
"""
import json
import os
import shutil
import sys

args = sys.argv[1:]
if args[:1] == ['-p']:          # `node -p 'JSON.stringify(process.versions)'`
    print(json.dumps({'node': '26.7.0', 'v8': 'fake', 'uv': 'fake'}))
    raise SystemExit(0)
stem, out = args[5], args[8]
records = json.loads(open(os.environ['CP17C_FAKE_RECORDS']).read())
shutil.copyfile(records[stem], out)
print('fit', stem, 'ok (stand-in)')
