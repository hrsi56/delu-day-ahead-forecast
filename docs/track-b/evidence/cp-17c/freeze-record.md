# CP-17c's freeze record: A1 re-frozen under the `macos-26` issuing host, superseding CP-17b's freeze

**The machine-readable freeze** is [`freeze-manifest.json`](freeze-manifest.json). It holds:
- **the policy identity:** SHA-256 `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`. Every issued artifact cites it;
- **the freeze-origin artifact,** reissued under the issuing host below;
- **the canary's frozen quantile hash;**
- **the initial state,** CP-17's, carried by reference, and its file on the states' route;
- **the reference bundle's manifest;**
- **`verification`:** how each hash it records is checked.

Its content digest is `9d82c66b1f8cfd147ba9dd97720996c1122f9e6c6478e67a706c17589c572463`. The file's own SHA-256 is
`ceab430989d0050a2e8c0cf80f9fa22d0929a9dacfde69fc6c98127605752532`.

**Verifying it.**

    python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json

- It dispatches on the manifest's schema to `cp17.tools.refreeze17c`, and recomputes every hash the manifest records.
- It refuses a missing or altered file, a wrong registry version, a wrong set of governance pins, or a broken digest.
- **It prints `verified` only when nothing is unchecked.** It exits 0 in both cases, so a run reads its output.
  - On the issuing machine, every local file is required. That machine is the runner or the Owner's Mac, holding the
    pinned runtime or the states.
  - Elsewhere (CI), each local file is reported unchecked, never passed.
- Its controls are in `tests/cp17c/test_refreeze17c.py`.

**This record is complete on its own,** so that 4.7T's brief and CP-17c's landing record cite one document. Each
section below is either restated with its change, or carried from CP-17b's freeze record unchanged, by that record's
hash.

**What it supersedes.** CP-17b's freeze is superseded, not edited. Its records stay as committed, and this
manifest's verifier checks that they do:

| CP-17b's record | SHA-256 |
|---|---|
| the freeze record `../cp-17b/freeze-record.md` | `aaaa93047dece943db8f5d19f78927ac2f1dfb2da94136425570506e3da1eaca` |
| the freeze manifest `../cp-17b/freeze-manifest.json`, policy identity `439115fb984359c0c68f79b77a6da4b85a5e75677cfbeb24e043876793ca9893` | `1fe07bddda14035ff44e9a8e6571c12bd58320d501395cbacc185d902f855502` |
| the 4.7T protocol `../cp-17b/4-7t-frozen-protocol.md`, whose text does not change | `04aac76a1fc1166a367eb212c19f802abf2b2ba46f7e63345ed72e46508ae22a` |
| the freeze-origin artifact `../cp-17b/artifact-2026-09-06.json` | `c1c3dab694ac828867087d2028c0f5aaeda21b00d58e1e7bf35b2c7c7bbc273d` |
| the Integration verdict `../cp-17b/integration.md` | `a19c4502479d60998d677d587d123cbeaac0654479d6af7b35884d647f1716c1` |
| the landing record `docs/track-b/cp-17b-landing-2026-10-29.md` | `2b64f54261339337c1e372c1ee28a2ad442f14dec8fb99746a4c640ac3bfa72f` |
| CP-17c-probe's landing record `docs/track-b/cp-17c-probe-landing-2026-10-30.md` | `350ff44cc1f72f7f1c18873d8d0cc5a4e4df70ccf9cf3b7881911f10ce15aeff` |

**The superseded checks stay meaningful.**
- **CP-17b's verifier,** run on this tree, reports exactly what CP-17c re-froze, and nothing else:
  - `src/cp17/schema.py` and `src/cp17/daily.py`;
  - the rebuilt package's files, identity and zip, which follow from them.

  An amendment leaves that set unchanged, and any other change adds to it (`tests/cp17b/test_refreeze.py`, seven tests
  superseded, below).
- **CP-17's verifier,** on CP-17b's view, still reports exactly its two files, `issue.py` and `schema.py`.

**Authority:**
- `capstone_v21.md` v21-r19 (`acdeeab1…`; frozen copy `pinned/anchor-capstone-v21-r19.md`): §24.13's "The issuing host
  (decision 24; H1)" and "What CP-17c re-freezes, and what 4.7T then tests", and §24.12 for every term CP-17c keeps;
- the Owner's decisions 22–25 (`12865483…`) and 20–21 (`5bf49634…`), frozen copies in `pinned/`;
- the brief `5f34f3ab…` (`issued-brief.md`, and its frozen copy in `pinned/`).

**"Frozen"** keeps §16.2's meaning. After CP-17c lands, any change to the policy, its code, its runtime or its state
needs a new freeze and a new evaluation. The one exception is a machine that passes the checks before a run's first
issuance (§24.13, H2). Daily fitting changes weights and state within the frozen policy, and is not a change to it.

## 1. What changed, and why (r19 §24.13's list "What CP-17c changes")

| Item | Change | Where |
|---|---|---|
| the issuing host | the official Node.js v26.7.0 darwin-arm64 binary, in place of Homebrew's (`1ef99ea2…`) | §2 |
| how a run gets the binary | each run retrieves the tarball with `SHASUMS256.txt` and checks all three by hash; a failure issues nothing | `cp17.runtime.retrieve`, §2 |
| the binary's path | the defaults `cp17.daily.NODE` and `cp17.tools.hosts.NODE` name the official binary's project-relative path, not Homebrew's | §2 |
| the Pyodide folder | `.local/tools/pyodide-0.28.0`, project-relative, unchanged in name. The 23 files reach the runner at that path, committed in the private scratch repository | §2, §6 |
| `refreeze verify`'s zip check | the zip is compared where the zlib runtime equals the recorded `1.2.12`; the pinned CPython has it on both machines, so the check runs there and passes | §2, §8 |
| where `refreeze verify` runs | on the runner and on the Owner's Mac, as the first H2 check, before the first fit | §3 |
| the states' route | `k13.json`, the freeze-origin states, the canary's payload, the shadows' buffers and the issued records | §6 |
| the CPython patch version | 3.13.15, uv's build, pinned in `cp17.runtime`, without changing the root `uv.lock` or `pyproject.toml` | §2 |
| the image version and CPU model | recorded in each run's check record, which is CP-18's record beside the run's issued artifacts | §3 |
| the checks before each run's first issuance | `cp17.hostcheck`, frozen with the policy identity | §3 |
| R7's `schema.py` defect | fixed on its error path only | §4 |

**The code** (`src/cp17/`). Every change, and why:

| File | In the identity as | Change | Why |
|---|---|---|---|
| `cp17/schema.py` | a package file (shipped) | `verify_bundle` lists a structurally malformed day of a re-hashed issued-forecasts record as a fault, and reads no further into it, where it raised | R7, H3 (§4) |
| `cp17/daily.py` | a pipeline file (never shipped) | `NODE` is the official binary's project-relative path, resolved against the project root when a `Host` is made | the binary's path |
| `cp17/runtime.py` (new) | a pipeline file | the host's pins, the files' project-relative paths, the CPython pin, the machine, the retrieval | H1 |
| `cp17/hostcheck.py` (new) | a pipeline file | the checks before each run's first issuance | H2 |
| `cp17/tools/bundle.py` | a native-only tool | `PIPELINE` lists the two new modules. The closure is measured where LightGBM's native library cannot load, which a `macos-26` runner without `libomp` needs, with a placeholder recorded as `stubbed`; the rebuilt files, identity and zip are compared bit for bit as before | the new pipeline files; `refreeze verify` on the runner |
| `cp17/tools/hosts.py` | a native-only tool | `NODE` and `NODE_SHA256` name the official binary | the binary's path |
| `cp17/tools/refreeze.py` | a native-only tool | `verify` dispatches on the manifest's schema to CP-17c's verifier; CP-17b's own verification is unchanged | one command for both |
| `cp17/tools/refreeze17c.py` (new) | a native-only tool | CP-17c's identity, manifest and verifier | this freeze |

- **No fit, emission, scoring, retrain, attribution or chain module changed.** `dailyfit.py`, `scoring.py`,
  `retrain.py`, `attribution.py`, `issue.py` and `shadow.py` are CP-17b's bytes. So are the runners `host/node_run.mjs`,
  `browser/worker.js` and `browser/index.html`, and the host driver `host/driver.py`.
- **The package** is 34 files, the same names as CP-17b's, with `schema.py` the only changed one:
  - file-list SHA-256 `9a2d961aecd2e90d3ea89308ddabddd687aea592944da7a8faabb6cdd648204c`;
  - deterministic zip, 91,835 bytes, `460a94e1df39dc07ce549828c07da92d16a286b4344df1654772313e7164be94`, under zlib `1.2.12`.
- **The pipeline files, frozen with it and never shipped:**
  - `cp17/daily.py` `2bf49d200ac6dc82e36e8157e8c1ec678a01e34d33fd7c424c82211b3c29911b`;
  - `cp17/runtime.py` `50958ccde1223f343405585062a336392c87e12980e4c7647e9f22b3b1215035`;
  - `cp17/hostcheck.py` `1c721b58aadf4223fea62b9db36f74edbe2d0fb76e6eae147bfde88a8ae7cffc`.
- **Dependencies are unchanged:** the root `uv.lock` `5d2aecc3…` and `pyproject.toml` `aa35326a…`, and the pinned
  runtime's packages.
- **The harness** that ran this round on the runner and on the Owner's Mac is `src/cp17c/`, outside the identity. It
  drives `cp17.daily` and `cp17.hostcheck` unchanged.

## 2. The issuing host (r19 §24.13, H1): restated

| Item | Value |
|---|---|
| The runtime | Pyodide 0.28.0, by its 23 pinned file hashes (CP-17b's, unchanged), at `.local/tools/pyodide-0.28.0`, in the official Node.js v26.7.0 darwin-arm64 binary, one worker |
| The tarball | `node-v26.7.0-darwin-arm64.tar.gz` from `https://nodejs.org/dist/v26.7.0/`, 57,622,243 bytes, SHA-256 `7ee659a7768e641bbfd5360940660b8e8fd0052f77488f365562bac522fc15d4`, listed so in the release's `SHASUMS256.txt` (2,943 bytes, `4533f0a43b9ba7f78a48230a0511b9dd5c931f20c3b3cac281ff9b7a2080fb2e`) |
| `bin/node` | 145,238,560 bytes, SHA-256 `a9bd0630891c2dcdee70de88270fee2cc0c4a9e76495039dd3b4f91c5e6b71df`, at `.local/tools/node-v26.7.0-official/node-v26.7.0-darwin-arm64/bin/node` |
| How a run gets it | `cp17.runtime.retrieve`. It downloads both files, checks `SHASUMS256.txt`, its listing of the tarball, the tarball and the extracted `bin/node` by hash, and moves the binary into place only then. A failure raises, so the run issues nothing |
| CPython | 3.13.15, uv's build for macOS on ARM64 (`cpython-3.13.15-macos-aarch64-none`, as uv 0.12.6 installs it), zlib runtime `1.2.12`. It runs the chain's judgement and the shadow states inside `cp17.daily`, in the environment `uv.lock` pins. The runner and this Mac ran the same interpreter binary, `7710b0490e6af648676d7ad163fa1d54bffb75d8505162609a1c3c9b76e1929d` |
| The machines | **the daily product:** a GitHub-hosted standard runner, label `macos-26` (Apple silicon), `ImageOS` `macos26`; **4.7T and any local run:** the Owner's Apple-silicon Mac. The image version and the CPU model are recorded, not pinned (§3) |
| The reference runtime (§19.3) | the issuing host above, plus Chromium 153.0.8010.12 and WebKit 26.6 through Playwright 1.63.0, on the Apple M3 machine class, measured again on CP-17c's zip (§8) |
| Resources | unchanged: criterion 5's one worker, 15 minutes of wall time and 4 GB of peak memory |
| The rule | a machine that passes the checks below is not a runtime change; any other binary, runtime file, operating system or architecture is (§16.2) |

## 3. The checks before each run's first issuance (r19 §24.13, H2): new

`cp17.hostcheck`, frozen with the identity. They run once per run, on the runner or on the Owner's Mac, in this
order. They run again whenever the machine or the runtime changes within a run.

1. **The pins.** `refreeze verify` against this manifest must print exactly `verified`. That means no problem and no
   unchecked item; the run reads the output, because the command exits 0 either way.
2. **The binary.** The tarball and `bin/node` must match their pinned bytes and hashes.
3. **The machine.** It must be macOS on ARM64. On a GitHub-hosted runner, `ImageOS` must be `macos26`.
   - The image version, CPU model, cores, memory and OS version are recorded in the run's check record, which CP-18
     keeps beside the run's issued artifacts.
4. **A canary fit.** A1 at the freeze origin, 2026-09-06, is reissued under the host in its own fresh process and judged
   as any attempt. Its quantiles must reproduce the frozen SHA-256
   **`4e6abb02fbb02aa8ef202207f21b76bc33b34c37d025a0a93a491135ea43cea5`**.
   - That is CP-17b's value, shown unchanged here: the freeze-origin artifact below carries it.
   - The canary payload is the freeze-origin issuance's, payload identity `63ce7f45…`.

**What a failure means.**
- The first failed check stops the gate. No later check runs, and the run issues nothing, so each of its days is not
  issued.
- For 4.7T, a failure is a blocker, never a day's outcome.

**Each check is tested failing on its own** (`tests/cp17c/test_units.py`). On the runner and on the Owner's M3, one
forced failure of each check was run:
- an altered manifest;
- an altered `bin/node`;
- a runner whose `ImageOS` is not `macos26`;
- a canary payload with one byte changed;
- a canary checked against another hash, after a full fit.

Each stopped at its own check, ran none after it, and issued nothing (§8).

## 4. R7's `schema.py` defect, fixed on its error path only (r19 §24.13, H3): new

- **The defect** (§24.12, R7). A structurally malformed day in an issued-forecasts record, re-hashed in the manifest,
  made `verify_bundle` raise. Schema validation listed the fault, but the partial-record loop and the artifact
  cross-check then indexed the day unguarded.
- **The fix.** Each day is read further only if it validates against the day schema and its date parses. Otherwise it
  is listed as `issued-forecasts.json: day i is malformed, so it is listed and not read (R7)`. A record whose `days`
  is not a list yields no days to read; schema validation lists it.
  - A record that verifies is judged exactly as before, with the same messages in the same order.
  - The schemas are unchanged.
- **Shown** (`reports/cp17c/r7-controls.json`):
  - On CP-17c's reference bundle, six malformed-day controls are listed by CP-17c's `verify_bundle`. CP-17b's
    `schema.py`, checked against its frozen hash, raises on all six.
  - The valid bundle verifies under both.
  - CP-17b's negative controls give identical results under both.
  - Every fit, quantile and artifact field is unchanged: native parity and the issuing host's parity, bit for bit (§8).
- **R7's acceptance and its instruction end at CP-17c's landing** (r19 §24.13).

## 5. The freeze origin and the initial state: restated

**The freeze origin** is the issuance for delivery 2026-09-06 at 2026-09-05 09:00 UTC.

**The freeze-origin artifact** is the issuing host's, reissued under the official binary and citing this freeze's
identity:
- artifact `4aedd5e052f0ee8d3d6aeed47c395c5cb246853e27ed129cdf514dcd9e3bf9b5`, kept in
  [`artifact-2026-09-06.json`](artifact-2026-09-06.json), file SHA-256
  `066064c3d4fd3be1a81184b607c5b8ab997e544dda589f921338afcca16c43cd`;
- displayed as "successful daily fit", the issued policy A1;
- its quantiles hash is the canary's, `4e6abb02…`, and its exported arrays are CP-17b's to the byte
  (`15bf7731c43bd9be164d2bab83e9c5afc30cf4ad412150e5a549d27c3f295fce`);
- **against CP-17b's artifact,** it differs only where it must: its own hash, the identity it cites (policy identity and
  package), and its measurement. It was issued in 82.2 s of wall time and 682 MiB of peak memory, in its own process.
  Every quantile, key, display, time, input and training field is equal (`reports/cp17c/freeze-origin.json`);
- its three shadows reproduced CP-17b's hashes for v4, v2 and B0 at 2026-09-06; with them, the issuance took 239 s;
- **the reference bundle** in the re-frozen kinds verifies, and its negative controls are refused
  (`reports/cp17c/reference-bundle.json`; manifest `84ca760b2c5b8387…`).

**The initial state is CP-17's, carried by reference** (CP-17b's §9).
- It is CP-26's final replay state for v4, v2 and B0, with buffers released 2026-08-08 to 2026-09-04, and v5's.
- **Its file on the states' route** is `.local/artifacts/cp-17c/state/freeze-origin-state.json`
  (`1388d74d7f3b7ec75992b37641b4b8a17f6f0f0d2e2d2cf08d85e51b90fdcfba`).
  - It was built from CP-26's ledger: the state at 2026-09-06 after its release, with CP-26's registrations of 2026-09-05
    and 2026-09-06 pending.
  - Its buffers equal CP-17's recorded ones, bitwise, for v4, v2 and B0.
  - Its buffers, pending registrations and origin equal the final state of CP-17b's native shadow run
    (`reports/cp17c/state-route.json`).
- **For 4.7T,** the shadow states continue from it on 2026-09-07.

## 6. The states' route: new (r19 §24.13)

Every file is at the same project-relative path on the runner and on the Owner's Mac. This manifest records each by
hash, `refreeze verify` checks it (H2's first check), and a run issues nothing without it.

| State | Path | How it is bound | How it reached the runner here |
|---|---|---|---|
| A1's search state S_13 | `.local/artifacts/cp-17/inputs/reports/rebaseline/cold-rerun-2026-10-15/search-results/nominal/k13.json` | file `17ade4513a39dffd…`, content digest `6090f4abaeca028694aa9941ce1240001e12b5965d3d9d0b72fe43cf77ee384f` | committed in the private scratch repository |
| the freeze-origin states of v4, v2 and B0 | `.local/artifacts/cp-17c/state/freeze-origin-state.json` | file `1388d74d…`, buffers CP-17's | committed there; on the runner a store was initialized from it and loaded back (§8) |
| the canary's payload | `.local/artifacts/cp-17c/state/canary/A1-2026-09-06.{json,npz}` | files `32a6ee38…`, `1f353c2d…`; payload identity `63ce7f45…` | committed there |
| Pyodide's 23 files | `.local/tools/pyodide-0.28.0/` | CP-17b's 23 hashes | committed there |
| the binary | `.local/tools/node-v26.7.0-official/` | §2 | retrieved by the run |
| the shadows' buffers and the issued records | a state store (`cp17c.store`) | a hash chain over every state file and issued record | carried day to day, one process per day, across the 14 shadow days |

**The state store** is proposed for CP-18, which builds the persistence:
- one folder per run, with a ledger chained by SHA-256 over every state file and issued record;
- loading checks every hash and the chain, and refuses otherwise;
- one issuance per delivery day, never replaced, and days go forward;
- the genesis entry names where the states started.

The return gives the proposed form between live runs.

## 7. The terms CP-17c keeps: carried unchanged

These sections of CP-17b's freeze record (`aaaa9304…`) stand as written there, with CP-17's sections it carries:
- **§1,** the decisions applied (13–18);
- **§4,** the failure policy and the success definition: the chains, G2, the rules of the chain, the five criteria, the
  driver (N1);
- **§5,** the shadow rule (decision 14), B0 shadow-issued;
- **§6,** the training windows and label rules (decision 16, C1);
- **§7,** F1, with r18's largest observed figure, 0.082 EUR/MWh, stated as an observation and not a bound (§24.12, R3).
  The manifest's identity records it beside CP-17's 0.028 text;
- **§10,** CP-17's sections carried unchanged: the designation, the features and the tier, margin and GFS rulings, S_13's
  eight members and the fixed blends, the seeds, the refit schedule with S_14 = 2027-01-06, the uncertainty layers, the
  registry's local names, §19.5's definitions, §19.3's status rule, τ_eq and §19.7's methods;
- **τ and τ_eq:** 10 and 0.01 EUR/MWh.

The identity's own fields for all of these equal CP-17b's (`tests/cp17c/test_refreeze17c.py`).

## 8. The fit is unchanged, and the host reproduces it, shown

- **Native parity with CP-26** (code identity, since `schema.py` changed). It ran on the Owner's M3 at nine origins for
  five policies: PASS, every check bitwise, and every check, payload identity, quantile hash and ledger hash equal to
  CP-17b's record (`reports/cp17c/native-parity.json`).
- **Chromium and WebKit,** A1 at 2026-09-06 on CP-17c's zip, reproduce the issuing host's `4e6abb02…` bit for bit, as
  CP-17b's browsers did (`reports/cp17c/browser.json`).
- **On the Owner's M3 and on a GitHub-hosted `macos-26` runner** in the private repository `hrsi56/delu-host-refreeze`:
  - `refreeze verify` printed `verified`;
  - the H2 checks passed, with one forced failure of each;
  - A1's parity at the nine origins was bit for bit against `reports/cp17b/host-parity.json`;
  - the 14 shadow days, 2026-08-24 to 2026-09-06, carried by the store, matched `reports/cp17b/shadow-run.json`;
  - every fit was timed and measured against 15 minutes and 4 GB.

  The figures are in `reports/cp17c/measurement.json` and [`report.md`](../../../../reports/cp17c/report.md).

## 9. What 4.7T's brief cites from here

| §24.12's row | Its value from CP-17c's landing |
|---|---|
| The freeze | CP-17c's: `docs/track-b/evidence/cp-17c/freeze-manifest.json` (`ceab4309…2532`), policy identity `720fc581be6206eba8ed303e689e63c09272a189564090a547d93fc9e7db62dc`; this record. It supersedes CP-17b's freeze (policy identity `439115fb…`), whose records stay as committed |
| Where it landed | `land/cp-17c` and `evidence/cp-17c`, as CP-17c's landing record states them |
| The code (§19.2) | the package `src/cp17/`, 34 files, file-list SHA-256 `9a2d961aecd2e90d3ea89308ddabddd687aea592944da7a8faabb6cdd648204c`, zip `460a94e1…`; its pipeline files `cp17.daily` (`2bf49d20…`), `cp17.runtime` (`50958ccd…`) and `cp17.hostcheck` (`1c721b58…`), frozen with it and never shipped |
| The issuing host | §2 above, as r19 §24.13 pins it |
| The freeze origin | the issuance for delivery 2026-09-06 at 2026-09-05 09:00 UTC, artifact `4aedd5e052f0ee8d3d6aeed47c395c5cb246853e27ed129cdf514dcd9e3bf9b5`; canary quantiles `4e6abb02…` |
| The initial state | CP-17's, carried by reference; its file `freeze-origin-state.json` (`1388d74d…`) on the states' route |
| The check that survives amendment | `python -m cp17.tools.refreeze verify docs/track-b/evidence/cp-17c/freeze-manifest.json`, which must print `verified`. It reads the governance documents from frozen copies (`pinned/` here and CP-17b's), so a later anchor revision leaves it green |

## 10. Governance pinned by frozen copies

**`verify` reads the frozen copies, never the live files.** It also checks CP-17b's eight copies in its own
`pinned/`, so the set of pins is twelve.

| Document | Frozen copy | SHA-256 |
|---|---|---|
| the anchor `capstone_v21.md` at v21-r19 | `pinned/anchor-capstone-v21-r19.md` | `acdeeab18a17ecdb83ade83d369a5031f3180f8fdb618a23af5b37836663996e` |
| this brief (`issued-brief.md`) | `pinned/cp-17c-brief-5f34f3ab.md` | `5f34f3ab298cfa619ddefaa9b1dcfd5df207c73a0ae06cbf8ed30454ac559c7d` |
| the Owner's decisions 20–21 (`docs/track-b/owner-decisions-2026-10-29.md`) | `pinned/owner-decisions-2026-10-29.md` | `5bf496341549025c98d42047b3f5c2056ba30dc36df6a036f82e9a118a41aa3f` |
| the Owner's decisions 22–25 (`docs/track-b/owner-decisions-2026-10-30.md`) | `pinned/owner-decisions-2026-10-30.md` | `1286548362b5618e3fb01c616d673c0af83dd79effeaf102bb9727ac219aabab` |

**Computational inputs, code and runtimes stay verified live,** as under CP-17b: the snapshot, the inputs' manifests,
the tier register, the partitions, the margins, the weather features, CP-17-probe's runtime retrieval manifest, CP-15's
protocol, `uv.lock`, `pyproject.toml`, every package, runner and pipeline file, the rebuilt package and zip, and the
schemas. Local runtimes and states are verified on the issuing machine (§6).

## 11. Tests superseded

| Test | Why |
|---|---|
| `tests/cp17b/test_refreeze.py`: `test_the_committed_manifest_verifies_here`, `test_the_copy_verifies_with_its_local_runtimes_unchecked`, `test_a_changed_live_anchor_or_a_new_decisions_record_leaves_it_green`, `test_the_real_runtimes_verify_and_one_altered_file_fails`, `test_an_amendment_leaves_both_verifiers_green` | CP-17b's verifier now reports exactly what CP-17c re-froze; each test asserts that set, and nothing more, where it asserted none |
| `tests/cp17b/test_records.py`: `test_the_identity_holds_the_re_frozen_terms`, `test_the_package_is_the_checkouts_and_its_changes_are_declared` | they compared CP-17b's recorded `daily.py` and package files with the live tree; they now check the recorded value, and that only `schema.py` differs live |

No test in `tests/cp17/` is superseded.
