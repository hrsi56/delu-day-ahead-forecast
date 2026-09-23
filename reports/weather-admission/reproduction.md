# Reproduction — programme 4.1 weather-archive admission

All commands run from the repository root. Network access is read-only; every request goes
through `reports/weather-admission/scripts/net.py`, which logs it to
`.local/weather-admission/logs/usage.jsonl` and refuses a request that would cross the
3.85 GiB stop line (4 GiB ceiling). Raw caches, sources and logs live in the Git-ignored
`.local/weather-admission/`. Re-running retrieval spends transfer again; the assembly step
alone is offline.

## Environment

```bash
uv venv .local/weather-admission/venv --python 3.13
```

```bash
UV_CACHE_DIR=.local/weather-admission/uvcache uv pip install --python .local/weather-admission/venv/bin/python -r reports/weather-admission/scripts/requirements.freeze.txt
```

`requirements.freeze.txt` pins ecCodes 2.49 (`eccodes`/`eccodeslib`), zarr 2.18.7,
numcodecs 0.15.1, blosc2 4.13.1, ocf-blosc2 0.0.13, numpy 2.5.3, requests 2.34.2.

The Hugging Face token is read from `launchctl` into the child environment only; it is
never printed, logged or written. Replace with any read-only token that has accepted the
`openclimatefix/dwd-icon-eu` gating conditions.

## Discovery and dated sources (already fetched; fingerprints in `sources/fingerprints.csv`)

Dated Wayback captures are fetched in raw mode (`web.archive.org/web/<timestamp>id_/<url>`)
and stored with sha256, URL and retrieval time by `net.save_source`. The capture list and
their parsed values are in `availability/`.

## Frozen sample manifest

`reports/weather-admission/sample-manifest.json` (sha256 in `hashes/report_files.sha256`) was
frozen at 2026-09-23T12:50:58Z before any sample retrieval.

## Decoded sample bundles (one per run)

```bash
cd reports/weather-admission/scripts
```

GFS from NOAA AWS (idx byte ranges), with NCAR byte comparison where listed in the manifest:

```bash
../../../.local/weather-admission/venv/bin/python gfs_sample.py 2022-08-25
```

```bash
../../../.local/weather-admission/venv/bin/python gfs_sample.py 2021-03-23 --compare-ncar
```

GFS from NCAR d084001 (no idx: bounded jump + GRIB2 header hops):

```bash
../../../.local/weather-admission/venv/bin/python gfs_sample.py 2019-01-01 --endpoint ncar
```

OCF ICON-EU (zip central directory + only the chunks covering the Germany box, steps 22–47):

```bash
HF_TOKEN="$(launchctl getenv HF_TOKEN)" ../../../.local/weather-admission/venv/bin/python icon_sample.py 2020-06-03
```

The full list of sampled runs and endpoints is `sample-manifest.json` → `samples`; attempts
(including failures) are in `usage/decode_attempts.csv`.

## Inventories (every required run)

```bash
../../../.local/weather-admission/venv/bin/python gfs_inventory.py ncar
```

```bash
../../../.local/weather-admission/venv/bin/python gfs_inventory.py aws
```

```bash
../../../.local/weather-admission/venv/bin/python gfs_inventory.py idx
```

```bash
../../../.local/weather-admission/venv/bin/python gfs_inventory.py tail
```

`tail` reads the exact size (1-byte range) and last 4 bytes of every NCAR file used as the
chosen endpoint (2019–2020 and 2021-02-02), checking for the GRIB end section `7777`.
THREDDS rejects suffix ranges, so this takes two requests per file.

```bash
HF_TOKEN="$(launchctl getenv HF_TOKEN)" ../../../.local/weather-admission/venv/bin/python icon_inventory.py
```

All inventory runs are resumable (completed keys are skipped).

## Assembly (offline)

```bash
../../../.local/weather-admission/venv/bin/python assemble.py
```

Writes `inventory/`, `availability/`, `decoded/summary.csv`, `verdicts.csv`, `gaps.csv`,
`usage/transfer.json`, `usage/decode_attempts.csv`, `sources/fingerprints.csv` and
`hashes/raw_sample_objects.sha256`. Then:

```bash
../../../.local/weather-admission/venv/bin/python ceilings.py
```

writes `usage/ceilings.md`. `sources/source-extracts.md` was generated once from
`sources/manifest.jsonl` and the `availability/` tables, and `hashes/report_files.sha256`
covers every committed-candidate file in `reports/weather-admission/`.

## Checks a reviewer can repeat cheaply

- Recompute any decoded message hash: `shasum -a 256 .local/weather-admission/cache/gfs/<run>_f024_u10_aws.grib2`
  and compare with `decoded/gfs_<run>.json` → `leads.f024.fields.u10.sha256`.
- Re-decode a cached message without network access: `grib_ls` is not required;
  `python -c "import eccodes; ..."` via `gfs_sample.decode_message(open(path,'rb').read())`.
- Verify a dated source: `shasum -a 256 .local/weather-admission/sources/<name>` against
  `sources/fingerprints.csv`.
