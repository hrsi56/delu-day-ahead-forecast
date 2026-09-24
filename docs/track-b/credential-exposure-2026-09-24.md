# Credential exposure and rotation — 2026-09-24

**A DagsHub user token was published in CP-20 evidence. The Owner regenerated it the same day,
so the exposed value is revoked. No other secret was found in any ref or in history.**

## What was exposed

- **File:** `docs/track-b/evidence/cp-20/integration-attempt-1/logs/critic-guards.log`, in the
  two `KeyError` tracebacks.
- **How:** two CP-16 tests read `os.environ['CP16_LEDGER']` directly. When the variable was
  missing, pytest printed a truncated `environ(...)` repr. Its first visible entry was
  `MLFLOW_TRACKING_USERNAME`, which in this project holds the DagsHub user token.
- **Where it entered history:**
  - `8665926` on the CP-20 branch, now preserved by `evidence/cp-20`;
  - the landing squash `f450bc1`, tagged `land/cp-20`.
- **When:** first pushed with the CP-20 landing, 2026-09-24 at about 11:35 UTC.
- **Scope:** the DagsHub token used for MLflow tracking. No other credential appears in the
  log.

## Detection

A value-based scan found the token later the same day. It compared committed files and history
with the actual values of the local secret variables.

The pre-push scan had searched only for token-like patterns (`securityToken=`, `hf_`, `AKIA`,
`Bearer`, API-key assignments). It missed the token because the token is a bare 40-character
hexadecimal value.

The value-based scan also covered every local branch, tag and remote ref and all history. It
found no ENTSO-E, Hugging Face, ACLED or other local secret.

## Remediation

- **Rotation:** the Owner regenerated the DagsHub token. The exposed value is treated as
  revoked.
- **Local configuration:** every setting that supplies the token now holds the new value. That
  covers the shell profile, the launchd session variables `DAGSHUB_USER_TOKEN`,
  `MLFLOW_TRACKING_USERNAME` and `MLFLOW_TRACKING_PASSWORD`, and cached tool shell snapshots.
- **Where the token is not stored:** no GitHub Actions secret, LaunchAgent, netrc file or git
  credential helper held it. Repository code reads the token only from the environment
  (`delu_forecast/tracking.py`).
- **Processes started before the rotation** keep the old value until they are restarted.
- **No history rewrite, by Owner decision:** the log is not redacted and history is not
  rewritten. The value is revoked, and a rewrite would change the reviewed candidate SHAs that
  the CP-20 Integration verdict binds.

## Prevention

- Before every push, search the outgoing files and history for the actual values of local
  secret variables, not only for token-like patterns.
- Treat any test log that contains an `environ(` repr as sensitive.
- The CP-16 production-verification tests now skip explicitly when their ledger variable is
  missing, instead of raising the `KeyError` that dumped the environment. See the CI repair
  commit that follows this record.
