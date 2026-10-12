# Reproducing CP-25

Run everything from the repository root.
- `PY` is the locked root environment, `.venv/bin/python`.
- `WX` is CP-20's pinned ecCodes environment, built from
  `reports/weather-admission/scripts/requirements.freeze.txt` (CP-20's
  `docs/track-b/evidence/cp-20/lead-scripts/build-wx-venv.sh`). In this checkout it is
  `.local/artifacts/cp-20/wx-venv/bin/python`, used read-only with `PYTHONDONTWRITEBYTECODE=1`.

Every compute job is charged to the CP-25 ledger, `.local/artifacts/cp-25/ledger.json`.

## Without the network: verify the frozen outputs

```
PY -m pytest -q -p no:cacheprovider tests/cp25
```

The tests run without the network. They:
- check the guard (§24.2's named instants and runs) and the credential handling;
- check every missing-input citation against its line;
- rebuild the margin classes from `margin-days.csv`;
- check that the calendar's exclusions equal the snapshot's null-load days plus January 2019;
- rebuild the never-scored mask from its four sources;
- check that the gap features have CP-20's columns and dtypes and complete coverage;
- check the targeted checks, the retrieval log against the guard, and every manifest hash.

To rebuild every output from the extraction directory and the preserved inputs:

```
PY scripts/cp25_data_gaps.py build all          # weather features, provenance, calendar, masks, inventory, tiers
PY scripts/cp25_data_gaps.py identity           # CP-20 conversion identity, 2,476 runs, bitwise
PY scripts/cp25_data_gaps.py resources
PY scripts/cp25_data_gaps.py manifest
```

`build all` needs `.local/artifacts/cp-25/weather/` (the decoded regional boxes, which are never
committed). `identity` needs CP-20's retained grids in `.local/artifacts/cp-20/weather/`. To leave
a checkout untouched, rebuild into a scratch directory and compare:

```
PY scripts/cp25_data_gaps.py build all --out <scratch>
diff <(cd <scratch> && shasum -a 256 *) <(cd reports/development-inputs && shasum -a 256 $(cd <scratch> && ls))
```

The scratch rebuild covers every file except the hand-written documents (`*.md`), the run
manifest, `conversion-identity.json`, `resources.json` and `manifest.json`.

## With the network: the retrieval (Owner-approved, anonymous, $0)

```
PY scripts/cp25_data_gaps.py init-ledger                       # once; never reset
PY scripts/cp25_data_gaps.py runs-manifest                     # the 329 runs (deterministic)
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src OMP_NUM_THREADS=1 WX -u -m cp25.extract \
  --manifest reports/development-inputs/gfs-run-manifest.json \
  --out .local/artifacts/cp-25/weather --admission reports/weather-admission \
  --ledger .local/artifacts/cp-25/ledger.json --select all --workers 4
```

The extraction resumes. A run whose `runs/<run>.json` and `.npz` match their hashes is reused,
never refetched. A single-run check, for example of the boundary run, is
`--select 2026-09-05 --workers 1` into a scratch `--out` with a scratch ledger.

## Independent reconstruction from retained raw messages

Seven runs' raw messages are kept under `.local/artifacts/cp-25/weather/raw/<run>/`: 2022-09-28,
2022-10-29, 2022-12-31, 2023-03-23, 2026-04-07, 2026-06-20 and 2026-09-05. To reconstruct one:
1. Check each message's SHA-256 against `gfs-messages.parquet`.
2. Decode it with `cp20.gfs.decode` in `WX`.
3. Compare the box with `runs/<run>.npz`.
4. Convert it with `cp20.weather.convert_run`, and compare the result with
   `weather-features-gaps.parquet`.
