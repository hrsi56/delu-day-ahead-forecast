# CP-20 rights notice — weather-derived artifacts

This notice covers only the committed CP-20 weather artifacts in `reports/weather-ablation/`.
The terms are those recorded by the admission on 2026-09-23
(`reports/weather-admission/rights-and-service-limits.md`). Terms can change; this is not legal advice.

## Source

- **Product:** NCEP Global Forecast System (GFS), 0.25°, operational D−1 00 UTC runs, produced by
  NOAA/NWS/NCEP (U.S. Department of Commerce).
- **Via NCAR GDEX dataset d084001** ("NCEP GFS 0.25 Degree Global Forecast Grids Historical Archive").
  The catalog states "Rights: Freely Available", and NCAR asks for citation of
  https://doi.org/10.5065/D65D8PWK.
- **Via the NOAA Open Data Dissemination (NODD) bucket `noaa-gfs-bdp-pds` on AWS.** NODD data are
  open to the public. NOAA asks for attribution for unaltered data, asks users not to imply NOAA
  endorsement, and asks that modified data not be presented as original.

Retrieval was anonymous and read-only. No paid tier, registration, token or negotiated exception
was used. DWD ICON was not admitted and no DWD data were used.

## What is committed, and what is not

| Committed | Content |
|---|---|
| `weather-features.parquet` | CP-20 **derived** regional aggregates: three hourly columns (mean 10 m wind speed, mean 100 m wind speed, mean DSWRF) over a fixed 47–55.25°N × 5.5–15.5°E box, plus status and clipping diagnostics |
| `messages.parquet`, `runs.csv` | Provenance only: source URLs, byte ranges, sha256 of each retrieved message, and decoded GRIB metadata |
| other CSV/JSON tables | Checks, missingness, clipping and hash comparisons |

- **Not committed:** no raw GRIB bytes and no decoded grids. The decoded boxes and retained raw
  sample messages stay under `.local/` and are not redistributed.

## Modification statement

The committed weather values are **modified** data, not original NOAA/NCEP products. They were
produced by:

- time interpolation of wind components;
- conversion to wind speed;
- DSWRF de-averaging and clipping;
- cos-latitude box averaging.

They are a regional proxy, not an official forecast, and no endorsement by NOAA, NCEP or NCAR is
implied.

## Attribution

> Weather inputs derived from NCEP GFS 0.25° operational forecasts (NOAA/NWS/NCEP), obtained from
> the NCAR GDEX archive (d084001, doi:10.5065/D65D8PWK) and the NOAA Open Data Dissemination
> program on AWS. Derived and aggregated by this project; not an official NOAA product.

## Repository licence file

`DATA-LICENSE.md` still covers only the inherited ENTSO-E and SMARD inputs. Per the admission
record, adding weather attribution there is an **Owner decision**. CP-20 does not edit it; this
notice is the CP-20 rights record until the Owner decides.
