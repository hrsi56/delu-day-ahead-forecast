# PRES-1 authentication precheck correction

The previous HTTP 403 was an invalid test of the configured MLflow credentials, not evidence
that the stored token needed replacement. DagsHub documents token-as-username authentication
for its MLflow integration, while the general account API describes username/token Basic
authentication. References checked on 2026-09-28: [MLflow authentication](https://dagshub.com/docs/integration_guide/mlflow_tracking/#3-set-up-your-credentials)
and [general API authentication](https://dagshub.com/docs/api/#authentication).

`scripts/mlflow_publish.py --precheck` now sends the existing MLflow Basic pair to the actual
tracking service's read-only `experiments/get?experiment_id=0` route. It requires HTTP 200 and
the expected `delu-cp2` experiment identity, disables redirects, and logs only credential presence,
status and a boolean match. It never writes to `delu-cp2`, returns account data, prints request
headers/exception text or changes stored credentials. The same gate runs immediately before
an authorized public upload. A successful authenticated read establishes service access, not
untested write permission; no write probe is used.

Fresh command:

```sh
.venv/bin/python scripts/mlflow_publish.py --precheck --log docs/track-b/evidence/pres-1/mlflow-precheck-corrected-2026-09-28.json
```

Exit 0, HTTP 200, expected experiment matched, both variables set, network writes 0. The exact
result is in `mlflow-precheck-corrected-2026-09-28.json`. The prior 403 record and blocked return
remain historical evidence; this record supersedes their authentication diagnosis. No credential
was replaced, copied into a command, or displayed.

Tests added to test_34 prove the correct endpoint/auth header, unchanged environment consumption,
no redirect forwarding, missing-variable refusal, wrong-identity refusal, HTTP-error refusal and
exception/body non-disclosure. The old local helper now invokes this committed implementation.
