# Data licence and the code/data split

[`LICENSE`](LICENSE) is MIT and covers the **code**: `src/`, `scripts/`, `tests/`, `app/`,
`sql/`, the `Makefile`, the `Dockerfile`, and the documentation.

This file covers everything MIT does not.

## The redistributed data stays CC BY 4.0

- `data/snapshot.parquet` and every file derived from it
- the figures and reports computed from it under `reports/` and `docs/`

> **Data: ENTSO-E Transparency Platform; Bundesnetzagentur | SMARD.de — CC BY 4.0.**

Both sources publish under [Creative Commons Attribution 4.0
International](https://creativecommons.org/licenses/by/4.0/). Redistribution is permitted
**with attribution**, which is why that line appears on every public surface of this project
rather than only here.

## Weather-derived research inputs carry their own attribution

The CP-20 research ablation adds weather aggregates under `reports/weather-ablation/`. They are
derived from NCEP GFS 0.25° operational forecasts, obtained from the NCAR GDEX archive and the
NOAA Open Data Dissemination program on AWS.

> **Weather: derived from NCEP GFS 0.25° (NOAA/NWS/NCEP) via NCAR GDEX d084001
> (doi:10.5065/D65D8PWK) and NOAA Open Data Dissemination on AWS. Modified and aggregated by this
> project; not an official NOAA product.**

- The committed values are **modified** regional aggregates, not original NOAA products. They
  imply no endorsement by NOAA, NCEP or NCAR.
- No raw GRIB bytes and no decoded grids are committed.
- The weather inputs are not part of `data/snapshot.parquet` or the v1 champion.

The source terms, the modification statement and the exact scope are in
[`reports/weather-ablation/rights-notice.md`](reports/weather-ablation/rights-notice.md).

## The trained model

`models/champion/` is a **derived work** of the CC BY 4.0 data above. It is released under the
MIT terms in `LICENSE`, with the data attribution carried alongside it — in
`models/champion/champion_card.json`, on the registered `champion` alias, and on every public
surface.

## Why the split is load-bearing rather than administrative

It was a design constraint from the start, not an afterthought. The project's scope record
(`capstone_V6_8.md` §0 item 3) closes a gas-price feature on exactly this ground: **no free,
daily, legally redistributable TTF/THE series exists** — Yahoo's terms prohibit redistribution,
Ember's underlying series is Montel-licensed — and a probe of SMARD's API at the de-risking
spike found gas-fired *generation volume* only, no price series. The pre-committed reopen
condition was adjudicated **NOT MET on 2026-06-12** and the feature was omitted.

The alternative was to build the merit-order signal on data the repository could not legally
ship. **A reproducible open repository that cannot ship its own inputs is not reproducible.**
The omission is recorded, its cost is measured — the §7.2 benchmark prices the unavailable
post-gate VRE forecast at **−19.4926%** on pooled pinball loss — and nothing in the champion
depends on a source that cannot be committed.
