# CP-25 rights notice: development inputs

**Licence file.** `DATA-LICENSE.md` is unchanged, and it continues to govern the data in this
directory.

**Prices and load.** These derive from the preserved `data/snapshot.parquet`.

> **Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0.**

**Weather.** `weather-features-gaps.parquet` holds derived regional aggregates of NCEP GFS 0.25°
operational forecasts. They were obtained anonymously and read-only, under the same terms recorded
for CP-20 (`reports/weather-ablation/rights-notice.md`, and the admission's
`reports/weather-admission/rights-and-service-limits.md`), from:
- the NOAA Open Data Dissemination bucket `noaa-gfs-bdp-pds` on AWS;
- for four leads of one run (2022-11-30), the NCAR GDEX archive d084001.

> Weather inputs derived from NCEP GFS 0.25° operational forecasts (NOAA/NWS/NCEP), obtained from
> the NCAR GDEX archive (d084001, doi:10.5065/D65D8PWK) and the NOAA Open Data Dissemination
> program on AWS. Derived and aggregated by this project; not an official NOAA product.

**Modification statement.** The weather values are modified data, produced by CP-20's frozen
conversion:
- time interpolation of the wind components;
- conversion to wind speed;
- DSWRF de-averaging and clipping;
- cos-latitude box averaging.

They imply no endorsement by NOAA, NCEP or NCAR.

**What is committed.**
- Derived features.
- Provenance: URLs without query strings, byte ranges, SHA-256 hashes and decoded GRIB metadata.
- Listing metadata: object sizes and `LastModified` times.
- The request log.

**What is not committed.** No raw GRIB bytes and no decoded grids. The decoded boxes and 7 runs'
raw sample messages stay under `.local/artifacts/cp-25/weather/`.

**No new source.** None was collected (§24.2's short path). The documentation pages read to
establish publication times are listed in `tier-register.md` §6. Only their text was read; no data
was taken from them.
