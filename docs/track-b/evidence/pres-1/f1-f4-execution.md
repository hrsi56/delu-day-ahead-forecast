# PRES-1 F1–F4 execution record

## F1 — complete

Authority: Owner D5, 2026-09-28, Publication Standard v1 §17 and conformance brief §7; the Owner's continuation instruction retained this authority and required the repeated independent review before upload.

Gates: `independent-check-4.md` is the fresh independent pre-F1 PASS at `217f4f8bd84a14cbbebb35a26b232678d1197998`. Its evidence-only preservation commit is `c8e8f1096471dff0ed8841cdf5a45ce571c89619`; source/export bytes are identical. The clean export dry run checked 23 runs, 6,928 metric points and 55 artifacts. All five export-file digests remain unchanged. The immediately preceding authenticated no-redirect MLflow GET returned 200 and matched the expected experiment (`f1-precheck.json`); stored credentials were not changed.

Command (using existing environment variables; no credential is in the command):

```sh
MLFLOW_DISABLE_AGENT_HINT=1 TMPDIR=<project>/.local/tmp/pres-1 .venv/bin/python -u scripts/mlflow_publish.py --target public --owner-instruction "Owner D5, 2026-09-28, Publication Standard v1 section 17: the Lead's F1 public MLflow upload, after an independent PASS. Conformance brief section 7 authorizes the upload of the committed export to delu-generations on DagsHub once section 5's gate holds; Owner instructed this Lead to continue F1-F4 after PASS." --log reports/presentation/release-checks/2026-09-28-mlflow-upload.json
```

Exit **0**. The export's 23 runs were created in DagsHub `delu-generations`, experiment ID **1**, with no resumed/skipped runs. Started **2026-09-28T20:27:28+00:00**, finished **2026-09-28T20:54:18+00:00**. The publisher read histories and artifacts back before marking each run/package complete. Dataset calls were recorded as `logged` or `none`, not silently described as public capability proof.

The log reports **710 counted logical write operations**. Its counter excludes the **23 `set_terminated` calls** visible in the successful run-completion log, so 710 is not a complete HTTP-request count. All these writes belong to this single explicitly authorized F1 invocation: experiment creation/tags, run creation/params/tags/metric batches/datasets/artifacts/completion/status, all within `delu-generations`. No public write probe, registry or `delu-cp2` write, Git push, branch/tag publication or Space redeploy was performed. No interrupted/resume or corruption experiment was performed on the public service. The local rehearsal remains its separate evidence.

The log was committed at `db60469` before the index. A successful F1 is not yet a terminal checkpoint PASS.

## F2 and F3 ordering

The index writer requires a passed full mirror record and passed browser checks; runbook §1.5 explicitly orders verification → browser routes → index. The full mirror and route checks therefore supply F2's prerequisites and F3's acceptance evidence. The six route identities are also checked independently over REST so browser work can proceed concurrently; the route seed is explicitly **not** a full mirror verdict. Before writing the index, its route/ID map must equal the completed full mirror's map exactly. After the generated index is committed, F3 records the public capabilities and acceptance against those checks. No measurement timestamp is relabelled as a later rerun.

The completion entries below distinguish the committed index, the acceptance/capability record and the final build.

## Retained F1 artifacts

- `.local/tmp/pres-1/f1-upload.log`: SHA-256 `af79749f2a1529ee9e91cbbc245199a3ee59ac774b8a3dd9ba1ab97af018e767`.
- `.local/tmp/pres-1/pre-f1-export-digests.json`: SHA-256 `71f35277fe79bdba41872d4470a779627f94322d4d44320cf312dab692c64105`.
- `.local/tmp/pres-1/pre-f1-protected-public-state.json`: SHA-256 `c2a402c73bad57a2019fbf14eae039c532176b2d082ff9c0e557480d10f80407`.
- `.local/tmp/pres-1/pre-f1-dry-run.log`: SHA-256 `9a718eefa28c519afef046d73243ddec45a3cd51fb47115f27042b231b7d0d16`.

## F2 — complete

`verify_mlflow_mirror.py verify --target public --out reports/presentation/release-checks/2026-09-28-mlflow-index-prereq-mirror.json` exited 0: 23 expected/found runs, 6,928 metric points, 55 artifact hashes, all params/tags/parents matched, six of six routes passed REST. The parallel browser seed was produced only by `route_checks` from real run IDs, marked route-only, and compared equal to the full mirror's entire route map and every run ID before index creation.

`check_reader_paths.py mlflow-routes --mirror-record <root>/.local/tmp/pres-1/f2-route-seed.json --shots <root>/.local/artifacts/presentation/mlflow-public --out reports/presentation/release-checks/2026-09-28-mlflow-routes.json` exited 0: all six routes passed anonymously in Chromium and WebKit. An additional fresh-context check waited for a Plotly SVG and zero Skeleton elements on all five comparison routes in both engines: 10/10 rendered, no HTTP errors (`2026-09-28-mlflow-charts.json`). This addresses the initial screenshot taken before delayed chart rendering finished; it does not claim that the earlier skeleton screenshot was a completed chart.

`verify_mlflow_mirror.py index --mirror-record reports/presentation/release-checks/2026-09-28-mlflow-index-prereq-mirror.json --browser-record reports/presentation/release-checks/2026-09-28-mlflow-routes.json` exited 0. The verifier generated six advertised routes, zero withheld, and all 23 run IDs. It was committed at **2665381** before F3's capability record and before F4. No index field was hand-edited.

## F3 — complete

The full mirror/REST/browser records above are the F3 verification evidence required to produce F2's verified index (runbook §1.5). After that index commit, fresh anonymous calls additionally checked **39/39 dataset names, digests and context tags**, **23/23 run notes**, **19/19 parent links**, the v3 tag filter (exactly `cp20/HG`), experiment kind and server version. `2026-09-28-mlflow-capability-checks.json` records the results. `delu-cp2` experiment metadata and `delu-day-ahead-champion` registry metadata are byte-for-byte equal as JSON objects to the pre-F1 read-only baseline. This checks metadata; it is not a fabricated full historical artifact census of those protected namespaces.

`reports/presentation/mlflow-capabilities.json` now separates the historical local/probe results from measured public support. All five comparison charts load in both engines. Dataset UI pages and a separate nested-tree interaction are not advertised or claimed as tested. Interruption/resume and deliberate corruption remain local tests; no destructive public probe or redundant upload was made.

The F3 helper used only `Reader` anonymous GETs and POST searches (reads), no authenticated calls or network writes. The retained scripts are `.local/tmp/pres-1/f3-capabilities.py` and `update-capabilities.py`; the mirror verifier and browser driver are committed scripts. The JSON results and capabilities are durable records, not only scratch logs.

- `.local/tmp/pres-1/f3-capabilities.py` — SHA-256 `711791a0e2f25adc527f76bdbf3e45d70448da755955beafcb2f6b24cef2ab10`.
- `.local/tmp/pres-1/update-capabilities.py` — SHA-256 `353b7da67baead592f77ee4a4aad5144d4d0c4fc02af9797eb81764847c7099a`.
- `.local/tmp/pres-1/f3-capabilities.log` — SHA-256 `2753d789439941b84439cbdfc6116af92e4b25cba5bd5cd455d798e84706e470`.
- `.local/tmp/pres-1/f2-route-seed.json` — SHA-256 `c5652ff4afafc0ec1fa555ecf10c122e2537f9b2e1a4e4f0d4e1d0dbf82bdb53`.
- `.local/tmp/pres-1/f2-mirror.log` — SHA-256 `23dd7a1840b421e645617684b9728626a208f2d7a16893af72eb1170637680c8`.
- `.local/tmp/pres-1/f2-browser.log` — SHA-256 `abeb2688294567140234f8ae533dbd15705d92891a93525285de7fe4653ab137`.

## F4 — complete; terminal review still required

`build_pages.py --final` exited 0 with all six verified routes and no omissions. `rebuild_presentation.py` then rebuilt README, cards, export and page; all five steps and cross-surface checks passed. `publication_guard.py tree` exits 0: final record, no placeholder. The final page is **1,560,646 bytes** (the first --final pass was 1,559,769; rebuilding the README/export/surfaces normalized the complete output before release measurements). A second post-bundle rebuild kept the normalized page size; clean-tree determinism is recorded separately with final suite/CI evidence.

The three `make wasm` steps were executed in order using the existing read-only Python 3.13.15 environment and this checkout's source (`PYTHONPATH=src`), with credential-like variables removed and temporary files inside `.local/`: `build_wasm_payload.py`, `verify_wasm_equivalence.py`, `build_wasm_space.py`. All exited 0. This keeps the Python version that produced the reviewed bundle; the normal Lead environment is 3.12.14 and its separate CI-equivalent checks remain required. No dependency, model or inference code changed.

Final Space bundle: **b046c69b899bb9d5a2b2f9aeb3e5b3eebfdda820a419137ef5cdf8b8ac8f7c3d**, **805 files**, **44,162,180 bytes**; 315 referenced assets, none missing. Browser champion source identity remains `9efb73f6bb29a60248ca6a4141b074c81a8ecc6e127396dfce52d4ff4b03df1b`.

Fresh final measurements: `2026-09-29-final-s10.json` passed every standard §10 view/accessibility/keyboard/touch/contrast/zoom check; `check_links.py` found no failed destination. `2026-09-29-final-demo.json` has four fresh-context cold starts on the local final bundle: Chrome and WebKit, 1440×900 and 390×844, ready with zero failed requests and console errors; control responses recorded. `2026-09-29-final-states.json` exercises forced asset failure, runtime failure/hang and successful retry in both engines. These are local final-bundle checks, not a redeploy or a claim about already published Space bytes.

The generated change includes link additions and a tracking sentence changing from future to present tense. Therefore the next independent check is **full**, including the final F1–F4 checks, rather than interpreting it as only a link-target delta. No source, test or research artifact changed after the pre-F1 PASS. The export remains byte-identical to what F1 uploaded. A checkpoint PASS is not inferred from these Lead measurements.

- `.local/tmp/pres-1/run-f4-wasm.py` — SHA-256 `ef559221460c20efd76b918bb8f0f4fa5a9192eb061b68b506b890741a573e0f`.
- `.local/tmp/pres-1/f4-wasm/2.log` — SHA-256 `310d4447d8a35b7e13906aad076f83b2ea994e39c00de6e84a0c82187fb80752`.
- `.local/tmp/pres-1/f4-wasm/3.log` — SHA-256 `654348140e406389a53d3cf796a4ceb18f25c2a907fa2771e3ac061569a591fc`.
- `.local/tmp/pres-1/f4-wasm/1.log` — SHA-256 `9097d6267893098be666de7111c67110b5c863ed15fb2f7de9d88881163a21cf`.
- `.local/tmp/pres-1/f4-wasm/results.json` — SHA-256 `5d22086ec498bc1b0e684105be10674ae42ffac7df5469ffe99747d6469ada17`.
