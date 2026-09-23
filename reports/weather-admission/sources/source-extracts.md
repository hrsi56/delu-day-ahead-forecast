# Source extracts and dated fingerprints

Raw copies are in `.local/weather-admission/sources/` (not committed). Every row below gives the source URL, sha256 of the exact bytes retrieved, and retrieval time; `fingerprints.csv` lists all of them. Extracts are short factual values or brief quotations; the parsed tables are in `../availability/`.

## Archive documentation

- **NCAR d084001 landing page** — https://gdex.ucar.edu/datasets/d084001/ — `9973c82928656d793e39bba6a76cf958ee30308534312efcf6517d7862e311a7` · retrieved 2026-09-23T12:35:21Z · 66874 bytes. Temporal range stated "2015-01-15 00:00 +0000 to 2026-10-07 12:00 +0000"; notice that the RDA "will stop updating this dataset early 2026" and points to the AWS copy. Grids "3 hourly interval from 0 to 240".
- **NCAR d084001 data-access page** — `d3cc1f5047f4a172505f3bdbe861f8f08837349cb0d03f286dc446fc68d9d087` · retrieved 2026-09-23T12:35:39Z · 55407 bytes. Links THREDDS catalog `tds.gdex.ucar.edu/thredds/catalog/catalog_d084001.html` and Globus.
- **NCAR THREDDS catalog** — `b08b778691b6e5010324d94f97538aa573cfb0f2e8f66653dee7f169d5e53943` · retrieved 2026-09-23T12:35:45Z · 2984 bytes. Services include fileServer, NetcdfSubset, OpenDAP; `Rights: Freely Available`.
- **AWS Open Data registry, NOAA GFS** — https://registry.opendata.aws/noaa-gfs-bdp-pds/ — `2f91e0826ab5a10d99af921c99adf40b1d52e27d05f6770762d6d2a269cc8885` · retrieved 2026-09-23T13:10:29Z · 15298 bytes. Licence: NOAA NODD data "are open to the public and can be used as desired"; attribution requested; no implied endorsement.
- **EMC GFS implementations** — `dd39586d075880d3b48bcbf6a84c213282e096002982c031ba6ea3bce2e982c9` · retrieved 2026-09-23T12:44:40Z · 145713 bytes. "GFS v16 - implementated on March 22, 2021, 12 UTC"; "GFS v15.1 - implementated on June 12th, 2019 12 UTC"; GSM v14.0.0 scheduled July 19, 2017.
- **NCO operational code listing** — `2d3287a7ad422d99e61eeda59fbcad1827129a4727e01ceccab3173970226782` · retrieved 2026-09-23T12:50:02Z · 3608 bytes. Current GFS package directory `gfs.v16.3.33/`.
- **OCF ICON-EU dataset card @ d3dea71** — `e6a440c13e41171499879195f875979640fe40bd1d8eff678682e627c38a3111` · retrieved 2026-09-23T12:37:22Z · 12038 bytes. "This HF dataset is no longer being updated"; early archive "contains a subset of the ICON-EU variables"; "collected every day, around 6-8 hours after forecast initialization time"; "No other processing of the data is performed"; licence CC BY 4.0 citing DWD's legal notice.
- **DWD ICON Database Reference v2.5.6 (2026)** — https://www.dwd.de/DWD/forschung/nwv/fepub/icon_database_main.pdf — `ef804f22bb4d72bf62d226a78c931afa51042a1ef0e702b2aafcc2e088dcfe41` · retrieved 2026-09-23T12:44:39Z · 9070839 bytes. Describes run structure (hourly output to 78 h) but states no open-data dissemination clock times; searched and recorded as not found.

## GFS dissemination evidence — NCEP production status (00 UTC GFS)

| Capture date | 48hr PRODUCTS avg end (UTC) | Forecast range / avg end | sha256 |
|---|---|---|---|
| 2017-05-06 | 03:44:02 | F00-F240 04:40:11 | `90241feacf57147d…` |
| 2019-01-21 | 03:42:34 | F00-F240 04:35:27 | `57fdfe0f32bb0198…` |
| 2019-04-24 | 03:42:29 | F00-F240 04:35:29 | `0a266c7ab228acfb…` |
| 2019-06-17 | 03:43:26 | F000-F384 04:42:00 | `9536ec17a09c0fb9…` |
| 2019-08-18 | 03:43:48 | F000-F384 05:04:59 | `0e0f30f2e15e6138…` |
| 2020-10-31 | 03:45:31 | F000-F384 05:05:43 | `0ba7fd11837dff00…` |
| 2021-04-08 | 03:56:44 | F000-F384 05:12:00 | `1756d4263827f3bd…` |
| 2021-12-06 | 03:57:43 | F000-F384 05:11:30 | `6fea1d94869b591d…` |
| 2022-05-28 | 03:59:02 | F000-F384 05:12:36 | `cc8af9d8ea552cf8…` |
| 2022-09-26 | 03:58:43 | F000-F384 05:12:08 | `cf537fcd1c9ac8dc…` |
| 2023-04-19 | 03:56:12 | F000-F384 05:08:18 | `b89c63f176495430…` |
| 2024-05-16 | 03:57:45 | F000-F384 05:10:24 | `706dc3446db18d60…` |
| 2024-11-28 | 04:00:09 | F000-F384 05:12:31 | `f487d3626e2e3ea8…` |
| 2025-03-07 | 03:52:37 | F000-F384 05:11:50 | `6825d6fc1dae81e6…` |
| 2025-07-18 | 03:56:47 | F000-F384 05:16:04 | `fc2681cbdd3025a3…` |
| 2026-01-08 | 03:51:30 | F000-F384 05:11:27 | `d2d7c95b864709cc…` |
| 2026-06-14 | 03:52:42 | F000-F384 05:12:22 | `3285422a86f52726…` |
| 2026-09-23 | 03:53:34 | F000-F384 05:13:59 | `b3fc96e28e02ffd3…` |

Page legend (captured): "The average start and stop times are based upon a 30-day running average." The 2017-05-06 capture predates GFS v14 and is context only.

## ICON-EU dissemination evidence — DWD open-data listings (00 UTC run)

| Capture date | Listing | Run | Steps 21–48 listed | First / last publication (listing time) | sha256 |
|---|---|---|---|---|---|
| 2020-01-22 | root |  | 0 | root dirs latest 21-Jan-2020 03:44 | `fb27a15ac7da3d8b…` |
| 2022-03-08 | tot_prec | 2022030800 | 28 | 02:56:00 / 03:16:00 | `68743571af3c2dad…` |
| 2022-05-16 | t_2m | 2022051600 | 28 | 02:55:00 / 03:16:00 | `2ef3861f61e2caf4…` |
| 2022-08-16 | t_g | 2022081600 | 28 | 02:52:00 / 03:13:00 | `282eac93e5dd315d…` |
| 2022-12-04 | u | 2022120400 | 28 | 02:48:00 / 03:16:00 | `8933cbd771557bdb…` |
| 2023-01-04 | aswdifd_s | 2023010400 | 28 | 02:53:00 / 03:11:00 | `65a51b3c2a8d3553…` |
| 2023-01-04 | aswdir_s | 2023010400 | 28 | 02:53:00 / 03:10:00 | `ad9a96c9040f023e…` |
| 2023-01-04 | v_10m | 2023010400 | 28 | 02:53:00 / 03:10:00 | `e982789a83631791…` |
| 2023-07-03 | t_2m | 2023070300 | 28 | 02:56:00 / 03:13:00 | `13f558758f3fac12…` |
| 2024-06-22 | aswdifd_s | 2024062200 | 28 | 02:52:00 / 03:08:00 | `fcff9c8ec0d1299f…` |
| 2024-06-22 | aswdir_s | 2024062200 | 28 | 02:52:00 / 03:08:00 | `87d41bd4a37cb945…` |
| 2024-06-22 | u_10m | 2024062200 | 28 | 02:52:00 / 03:08:00 | `99f78ead57a92c0e…` |
| 2024-06-22 | v_10m | 2024062200 | 28 | 02:52:00 / 03:08:00 | `8a03b63ee6bdde51…` |
| 2025-03-25 | aswdifd_s | 2025032500 | 28 | 02:52:38 / 03:08:57 | `4907f218e0581d21…` |
| 2025-04-28 | aswdir_s | 2025042800 | 28 | 02:52:18 / 03:08:42 | `363c7e08760741fb…` |
| 2025-04-28 | u_10m | 2025042800 | 28 | 02:52:17 / 03:08:42 | `74ad655407124675…` |
| 2025-04-30 | v_10m | 2025043000 | 28 | 02:52:40 / 03:09:30 | `cb3f6e5dbd1828f2…` |
| 2025-11-14 | aswdifd_s | 2025111400 | 28 | 02:52:41 / 03:09:45 | `6cf1a5561cd07782…` |
| 2025-12-12 | u_10m | 2025121200 | 28 | 02:57:00 / 03:14:08 | `3978d8d91ce0e42b…` |

Discovery aids (Wayback CDX lists, search results) are logged in `usage.jsonl` but are not evidence.
