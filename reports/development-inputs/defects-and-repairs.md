# CP-25 defects and repairs

Every repair below was made before any review, and none changes a frozen input. Nothing here
forecasts or scores.

1. **The conversion-identity comparison misreported the keys (control code only).** The first two
   runs of the control reported `keys_identical: false`, while the values were bitwise identical.
   - **First cause:** CP-20's file stores `timestamp_utc` in milliseconds, while a fresh build
     holds seconds, and pandas' `equals` compares the unit.
   - **Second cause:** the structural 2019-01-01 row's `run_00z` is NaN on both sides, and NaN is
     not equal to NaN.
   - **Repair:** compare the instants and the NaN-filled run keys. The third run passed on keys,
     values and status.
   - The gap features are now stored in CP-20's own dtypes: milliseconds, and float
     `dswrf_clipped_cells`. That keeps the two files exactly concatenable.

2. **The redacting request log was added after the extraction ran.**
   - The extraction ran with `GuardedFetcher` admitting each URL only after the boundary and
     credential guard, so no credential-bearing URL could be requested.
   - A test then showed that CP-20's unchanged `Fetcher._once` writes raw exception text into
     `requests.jsonl`, so a credential inside an exception message would reach the log.
     `GuardedFetcher` now routes that log through `guard.redact`.
   - The extraction itself used no credential: both archives are anonymous, no request carried an
     authorization header, and every logged URL drops its query. The credential scan of every
     CP-25 output and log (`scripts/cp25_data_gaps.py scan`) finds no stored value.
   - The extraction was not rerun: completed runs are reused, never refetched.

3. **Two citation line numbers were wrong before the first build.** The cited lines in
   `src/cp20/weather.py` were 149 and 216; the correct lines are 133 and 219. They were caught by
   the citation check, which `tests/cp25/test_outputs.py` now runs on every citation.

4. **The data build stopped once.** The per-run evidence summary called `strftime` on a NumPy
   datetime. The calendar, mask, inventory and margin files had been written before the crash;
   `tier-register.json` had not. The summary was rewritten over Python datetimes, and the next
   build rewrote every file. A later full rebuild (`build all`) reproduced every output byte for byte.

5. **Integrity failures during the extraction (none outstanding).** Run 2022-11-30 failed GRIB
   framing ("missing GRIB2 section 0") on AWS at four leads, which counts as 20 message attempts.
   Its AWS objects and indexes carry afternoon `LastModified` times; a rewrite is the likely cause,
   not a proven one. Under CP-20's rule each of the four leads took its one alternate attempt, on
   NCAR d084001, and each succeeded and validated. The 22 network failures (connection errors and
   one HTTP 500) were retried; under CP-20's rule, network retries are not message attempts.
