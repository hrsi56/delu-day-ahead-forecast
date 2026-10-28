# The payload schema and manifest, frozen at CP-17

**Authority:**
- the Space plan §4.12 and §7 step 3 (`final-product-space-plan-2026-09-30.md`, `ad3568c8…`);
- research anchor §19.4 and §19.1;
- the brief's item 7.

**Where the contract lives:**
- **The machine-readable schemas:** [`schemas/`](schemas/), one JSON Schema (draft 2020-12) per kind.
- **Implementation:** `src/cp17/schema.py`, which holds the schemas, the validator for the subset they use,
  the embargo check and `verify_bundle`. The tests require the files in `schemas/` to equal its `SCHEMAS`.

**The reference bundle:** built for the freeze origin by `src/cp17/tools/refbundle.py`. It stays in
`.local/artifacts/cp-17/final/reference-bundle/`. Its manifest and validation are committed in
`reports/cp17/reference-bundle.json`.

Building the daily pipeline that publishes bundles is CP-18's.

## The seven kinds of a dated bundle

| Kind | File(s) | Content | Loaded |
|---|---|---|---|
| `manifest` | `manifest.json` | every other served file with its SHA-256, size and kind; the product (name, designated policy, evidence label); the policy (the policy identity's SHA-256, the package's SHA-256, the issuing host); the daily artifact's identity (its SHA-256, day, issued policy, display); the three times (last training, data refresh, issuance); the freshness state (`fresh`, `stale` or `failed`, as-of day, latest issued day) | at start; the page verifies every hash and shows the served identity |
| `issued_forecasts` | `issued-forecasts.json` | every issued day: delivery day, issue time, issuing artifact's SHA-256, issued policy, display, the 23–25 UTC keys and the seven quantiles per key | at start |
| `outcomes` | `outcomes.json` | published prices per UTC key and delivery day, with source, publication and revision times; a missing price is `null` | at start |
| `evaluation` | `evaluation.json` | the committed metric records (`cp17.scoring.evaluate`), per window (development, 4.7T, prospective), evidence class and policy (the product, or B0 as context) | at start; the Space recomputes and compares them |
| `fitted_artifact` | `artifact.json`, `artifact-arrays.npz` | the issued artifact (`cp17.issue.artifact`): attempts and display, keys, quantiles, times, lineage (parent, policy identity, code, host, inputs, training, state), resources; and the issued fit's arrays (A1: every member's parameters, target centre and scale) | for Explainability, Features and Train it yourself |
| `training_window` | `<policy>-<day>.json`, `.npz` | the fit's shipped payload (`cp17.dailyfit`: A1's day table; v4's and v2's CP-15 rows; B0's prices; the interval buffers) with its arrays' hashes and its identity | only on "Train it yourself", its size disclosed first |
| `series` | `series.json` | hourly prices for the Data view, with first and last day | for Data |

## The rules every bundle meets

These are what `verify_bundle` checks; the reference bundle is tested against them.

1. **The manifest validates** against its schema.
2. **Every file listed exists,** and its SHA-256 and size are the manifest's. The issued forecasts, the
   outcomes, the evaluation records and the artifact the manifest names are always served. A file that fails
   its hash is never opened, and an unreadable file is a refusal, never a crash.
3. **No file is served unlisted.**
4. **Every file is the kind it is listed as,** and every JSON file validates against its kind's schema.
5. **A training window's identity holds:** its arrays have their declared hashes, and the payload digest
   binds the arrays and the meta together.
6. **The embargo holds.** A training window never carries its target day's outcome:
   - A1: D's price row, slot targets and mask are blank;
   - v4 and v2: D's targets are blank;
   - B0: D's prices are blank.

   Every released-error buffer holds complete delivery days ≤ D−2 only.
7. **The artifact verifies** (`cp17.issue.verify_artifact`):
   - its own identity;
   - its quantiles against their hash;
   - its issue time is D−1 11:00 Europe/Berlin.

   The manifest names that artifact, and the issued forecast of its day is the artifact's own, by hash and
   by value.

**The runtime rule is unchanged.** The Space loads its pinned runtime and its own served files only. It never
calls ENTSO-E, SMARD, GFS, the registry or MLflow at runtime. The browser runs block and record any non-local
request; none was made.

**Licensing.** The data are CC BY 4.0, ENTSO-E and Bundesnetzagentur | SMARD.de, with attribution
(`DATA-LICENSE.md`). GFS enters only as the three derived aggregates in the training windows. No raw GRIB and
no credentials are shipped.

## The reference bundle (freeze origin, delivery 2026-09-06)

It is built from development data and the issuing host's artifact, then validated. Contents:
- **Artifact:** the issuing host's A1 artifact for 2026-09-06, and A1's 8 × (parameters, centre, scale)
  arrays.
- **Issued forecasts:** that artifact's day.
- **Outcomes:** the day's 24 published prices, from the development snapshot.
- **Evaluation:** the record of the shipped day.
- **Training window:** A1's payload for 2026-09-06.
- **Series:** the last 31 development days.

**Validation:** it validates with no error. Every negative control is refused:
- one byte of the issued forecasts changed;
- an unlisted file served;
- a listed file missing;
- one bit of the training window flipped.

The record, including the manifest, is `reports/cp17/reference-bundle.json`.

**Publication times.** The development snapshot does not record each price's publication time, so the
reference bundle leaves `published_utc` and `revised_utc` empty, as the schema allows. The live pipeline
(CP-18) records both.

**The Data view.** It shows dates through 2026-09-06 only (§24.2, PUBLISH_RULES 1.5 invariant 10) until
4.7T opens.
