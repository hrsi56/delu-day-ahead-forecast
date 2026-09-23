# Service limits and free-use / redistribution terms

Observed and documented on 2026-09-23. Source fingerprints are in `sources/fingerprints.csv`.
No paid tier, purchase, negotiated exception or new registration was used. The only
account involvement was the Owner's existing Hugging Face token for the gated OCF dataset.
This page is not legal advice. It records the terms as published, and those terms can change.

## NCEP GFS 0.25° via NCAR GDEX d084001

- **Access.** Anonymous HTTPS through THREDDS `fileServer`, with byte ranges honoured
  (HTTP 206). NCSS subsetting and OPeNDAP also exist but were used only for one
  variable-list probe. No login was needed for any request made here.
- **Rights.** The THREDDS catalog metadata says "Rights: Freely Available". NCAR asks
  users to cite DOI 10.5065/D65D8PWK. The data are NCEP operational products.
- **Coverage stated on the landing page.** 2015-01-15 00Z to "2026-10-07 12:00", which is
  a future upper timestamp. The page also warns: "the RDA will stop updating this dataset
  early 2026" and points to AWS.
  - Observed catalog: 2026 days run through 2026-09-22, and that day's `f000` file was
    modified 2026-09-23 12:32Z. The archive was still updating when checked.
  - Continuation is not assumed. Live suitability belongs to 4.9.
- **Service behaviour observed.**
  - Latency was 0.2–5.6 s per request and throughput about 0.64 MB/s for a 4 MB range.
  - THREDDS rejects suffix ranges (`bytes=-N`) with HTTP 400; explicit ranges work.
  - One NCAR file is a truncated copy: 2024-09-15 00Z f039, 251,945,463 bytes against
    540,827,964 on AWS, with no GRIB end section.
  - NCAR has no `.idx` files, so every target message had to be located by reading
    GRIB2 headers.
  - The daily catalog pass took the longest of all inventory steps.
- **Retrieval time is not publication time.** NCAR catalog `modified` times fall about
  1.5 days after initialisation (for example, the 2019-01-01 00Z files were modified
  2019-01-02 13:30Z). They show when NCAR ingested the files, not when NCEP published
  them, and are not used as availability evidence.

## NCEP GFS 0.25° via NOAA NODD on AWS (`noaa-gfs-bdp-pds`)

- **Access.** Anonymous S3 over HTTPS: ListObjectsV2, GET and Range, with a per-file
  `.idx` inventory.
  - Coverage in the bucket starts 2021-01-01. Before 2021-03-22 12Z the files have no
    `atmos/` path segment.
  - Neither NCAR nor AWS holds the pre-2019 runs this task would need, and the
    2019 floor forbids using them anyway.
- **Licence (AWS registry entry).** "NOAA data disseminated through NODD are open to the
  public and can be used as desired." NOAA asks for attribution for unaltered data. Users
  must not imply NOAA endorsement, and modified data may not be presented as original.
- **Service behaviour observed.**
  - Typical latency was 0.2–0.4 s, with transient stalls. One sample request hung for
    more than 4 minutes and was aborted and retried.
  - Throughput was about 1.2 MB/s under concurrent load.

## DWD ICON-EU via Open Climate Fix on Hugging Face (`openclimatefix/dwd-icon-eu`)

- **Access.** The dataset is gated (auto-approval). The Owner reports accepting the
  conditions.
  - Verified: the token authenticates as user `Yarden-Viktor` (fine-grained token), and a
    1-byte ranged read of a gated file returned HTTP 206.
  - Reads were pinned to dataset revision `d3dea71c0edcb04e08e396ab4bf55afd1fdcfcf5`
    (repo lastModified 2026-04-24).
- **Licence (dataset card).** CC BY 4.0. The card quotes DWD's legal notice: DWD geodata
  "may be reused under the terms of the Creative Commons BY 4.0 … provided the source is
  acknowledged." Attribution to DWD and the dataset curators is required.
- **Status.** The card says "This HF dataset is no longer being updated". The last file is
  2025-08-09 18Z. There are 6,401 run files, one zipped Zarr store per run of 3–21 GB.
  - All are Zarr v2 except the 2025-03-07 00Z run, which is Zarr v3.
  - 15 files are stubs under 1 MB, not readable zips; 7 of them are required 00Z runs in
    March 2024.
- **Structure limits.**
  - Chunks are 37 steps × 326 × 350 grid points, compressed with Blosc2/zstd, so the
    smallest retrievable unit covering Germany for steps 22–47 is 4 chunks per field,
    about 25–37 MB each.
  - That makes about 110–128 MB per run for the four supported fields.
  - Hub-height wind is not in the archive: it holds 10 m winds and isobaric winds only
    (6 levels before March 2023, 20 levels after).
- **Provenance statements on the card.**
  - The data are "an archive of the publicly available data from
    https://opendata.dwd.de/weather/nwp/ … No other processing of the data is performed".
  - Collection happens "around 6-8 hours after forecast initialization time".
  - Early files carry a `history` attribute showing they were converted to Zarr in 2023
    from OCF's stored GRIB files. That is a format conversion, not a re-forecast.
- **Service behaviour observed.**
  - Ranged reads worked on the resolve URL, which redirects to a signed CDN URL.
  - Throughput was about 2.5 MB/s. No rate-limit responses were received.

## DWD open-data server (evidence only; not a retrieval endpoint here)

- DWD removes GRIB files after about 24 hours, so historical ICON-EU is available only
  from third-party archives.
- Publication times were read from dated Wayback captures of DWD's own directory
  listings.

## Consequences for a later full extraction (not authorized here)

- Attribution lines would be needed for NOAA/NCEP (via NCAR/NODD) and DWD (CC BY 4.0,
  via OCF).
- `DATA-LICENSE.md` currently covers ENTSO-E and SMARD only. Any committed weather-derived
  artefact would need its attribution added there, which is an Owner decision.
- Raw archive bytes stay in `.local/` and are not redistributed by this task.
