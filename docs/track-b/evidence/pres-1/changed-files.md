# PRES-1 complete file accounting

Whole checkpoint: `git diff --name-only main...<evidence_tip_sha>`. The candidate and evidence-tip SHAs are in `return.md` and the terminal handoff. This table covers inherited phases 0–E, conformance, repairs, actual F1–F4 and final evidence; it does not claim every file was newly authored in this continuation.

| File | Reason |
|---|---|
| `.githooks/pre-push` | Add the fail-closed publication guard after the unchanged secret guard. |
| `.github/workflows/tests.yml` | Add the publication guard as the main-branch CI backstop. |
| `Makefile` | Expose build, verification, lint and guard commands. |
| `README.md` | Generate the headline and generation sections and reconcile v1 surface descriptions. |
| `app/wasm_showcase.py` | Owner-authorized text/layout changes to expose controls and keep evidence in disclosures; no calculation change. |
| `docs/index.html` | Generated one-page research report, preserving the v1 archive. |
| `docs/track-b/evidence/pres-1/authentication-correction.md` | Explain why the account-API Basic probe was wrong and document the service-specific correction with unchanged stored credentials. |
| `docs/track-b/evidence/pres-1/changed-files.md` | Account for every changed file in the complete checkpoint with its purpose. |
| `docs/track-b/evidence/pres-1/ci-py312.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/cold-reader-check.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/conformance-checks.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/f1-f4-execution.md` | Record actual F1 authority/writes, verified index/mirror/browser ordering, public capabilities and final bundle. |
| `docs/track-b/evidence/pres-1/f1-precheck.json` | Preserve the successful read-only authentication gate immediately before authorized public F1. |
| `docs/track-b/evidence/pres-1/final-audit-matrix.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/final-checks.md` | Record final two-version suites, every CI step, deterministic build and browser/demo/cold-reader evidence before final review. |
| `docs/track-b/evidence/pres-1/independent-check-1.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/independent-check-2.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/independent-check-3.md` | Preserve the fresh FAIL on the interrupted candidate, with actionable W3 and W5 findings. |
| `docs/track-b/evidence/pres-1/independent-check-4.md` | Preserve the independent pre-F1 PASS and complete source/numeric/browser review, with explicit pending public steps. |
| `docs/track-b/evidence/pres-1/independent-check-5.md` | Preserve the fresh final Integration verdict at the exact final candidate, including public mirror/routes and F4 acceptance. |
| `docs/track-b/evidence/pres-1/mlflow-precheck-corrected-2026-09-28.json` | Record the fresh authenticated MLflow GET result without credentials, headers, response data or exception text. |
| `docs/track-b/evidence/pres-1/owner-decisions.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/owner-hand-checks.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/pres-1-conformance-brief-2026-09-28.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/presentation-d1-editorial-review-2026-09-25.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/presentation-final-editorial-audit-2026-09-28.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/publication-standard-v1.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/reader-tasks-d1.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/reader-tasks-final.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/registry-zero-diff.md` | Preserve the named approval, review, verification or provenance record for PRES-1. |
| `docs/track-b/evidence/pres-1/resumption-preflight-2026-09-28.json` | Preserve original repository-state verification and the historically incorrect account-endpoint 403 diagnostic. |
| `docs/track-b/evidence/pres-1/return-blocked-1.md` | Preserve the previous stopped return byte-for-byte; the authentication diagnosis is corrected separately, never rewritten as history. |
| `docs/track-b/evidence/pres-1/return.md` | Provide the complete terminal two-SHA return, acceptance maps, authority/resources, disposition handoff and W16 proposals. |
| `docs/track-b/evidence/pres-1/w3-w5-pre-review-checks.md` | Record repaired-candidate pre-F1 test and browser gates, including the corrected launcher run and retained-record applicability. |
| `docs/track-b/mlflow-tracking-spec.md` | Document registry-driven export, publisher, verification and reader routes. |
| `docs/track-b/publication-advisory-log.md` | Keep nonblocking findings and amendment proposals separate from the acceptance bar. |
| `docs/track-b/publication-packet-template.md` | Specify the evidence packet future publications consume. |
| `docs/track-b/publication-runbook.md` | Map every publication touchpoint to the actual registry, renderer and workflow. |
| `docs/track-b/research-content/cp15-cp16-claims.md` | Reconcile mapped v2 claims and withheld language for publication. |
| `docs/track-b/research-content/cp15-cp16-update.md` | Prepare the v2 publication narrative from existing evidence. |
| `docs/track-b/research-content/cp20-claims.md` | Map v3 claims and limits to committed evidence. |
| `docs/track-b/research-content/cp20-update.md` | Prepare the v3 publication narrative from existing evidence. |
| `docs/track-b/research-content/publication-claims.md` | Map derived publication claims to sources, including corrected contemporaneous 5/7/8 policy-count semantics. |
| `reports/cp3/link_check.json` | Record required destination verification. |
| `reports/cp3/pages_build.json` | Record page size, verified route coverage and the non-final publication state. |
| `reports/cp3b/space_wasm_bundle.json` | Record the built bundle identity and referenced-asset checks. |
| `reports/presentation/d1/layout-measurements.json` | Preserve the approved D1 specimen and measured layout evidence. |
| `reports/presentation/d1/specimen.md` | Preserve the approved D1 specimen and measured layout evidence. |
| `reports/presentation/mlflow-capabilities.json` | Separate historical rehearsal/probe results from measured public support, fallbacks and protected-metadata comparison. |
| `reports/presentation/mlflow-export/cp10.json` | Deterministic committed export of registry identities and unchanged research evidence for MLflow. |
| `reports/presentation/mlflow-export/cp15.json` | Deterministic committed export of registry identities and unchanged research evidence for MLflow. |
| `reports/presentation/mlflow-export/cp16.json` | Deterministic committed export of registry identities and unchanged research evidence for MLflow. |
| `reports/presentation/mlflow-export/cp20.json` | Deterministic committed export of registry identities and unchanged research evidence for MLflow. |
| `reports/presentation/mlflow-export/manifest.json` | Deterministic committed export of registry identities and unchanged research evidence for MLflow. |
| `reports/presentation/mlflow_index.json` | Preserve the verifier-generated map of all 23 public runs and six routes after exact mirror and anonymous two-browser checks. |
| `reports/presentation/release-checks/2026-09-24-demo.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-25-demo-local.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-25-rebuild.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-25-space-states-local.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-27.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-28-demo-local.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-28-demo-w12.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-28-export-diff-f1-candidate.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-28-mlflow-capability-checks.json` | Record fresh anonymous dataset/notes/parent/filter/server checks and unchanged protected public metadata. |
| `reports/presentation/release-checks/2026-09-28-mlflow-charts.json` | Record all five public comparison charts reaching a rendered state in both engines, with zero HTTP errors. |
| `reports/presentation/release-checks/2026-09-28-mlflow-index-prereq-mirror.json` | Record anonymous equality of every public run, parameter/tag, metric history, artifact hash and REST route against the export. |
| `reports/presentation/release-checks/2026-09-28-mlflow-routes.json` | Record intended content on all six public routes anonymously in Chromium and WebKit. |
| `reports/presentation/release-checks/2026-09-28-mlflow-upload.json` | Record the actual authorized public upload, source commit, per-run outcomes, times and counted write operations. |
| `reports/presentation/release-checks/2026-09-28-registry-export-diff.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-28-space-states-local.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-28-standard-s10.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-28-w3-w5-s10.json` | Preserve final or repaired-candidate release measurements, placements and accessibility evidence. |
| `reports/presentation/release-checks/2026-09-28.json` | Record the named local release check or record-level export comparison. |
| `reports/presentation/release-checks/2026-09-29-final-demo.json` | Record final-bundle cold start and both control changes in four fresh engine/viewport contexts, including errors/failed requests. |
| `reports/presentation/release-checks/2026-09-29-final-s10.json` | Preserve final or repaired-candidate release measurements, placements and accessibility evidence. |
| `reports/presentation/release-checks/2026-09-29-final-states.json` | Record forced final-bundle asset/runtime/hang failures and successful retry in both engines. |
| `scripts/build_pages.py` | Generate source-bound charts and registry-driven chapters in the required slot order, preserve v1 archive, and publish only verifier-indexed MLflow links. |
| `scripts/build_space.py` | Owner-authorized shared registry model line and required-line validation for Space cards. |
| `scripts/build_wasm_space.py` | Generate Space states/cards, package referenced assets and hash the bundle. |
| `scripts/check_links.py` | Fail on required broken destinations and classify non-destination examples. |
| `scripts/check_reader_paths.py` | Measure report/demo behavior, layouts, accessibility and anonymous MLflow routes. |
| `scripts/cp3_readme.py` | Reconcile v1 surface descriptions without hand-editing generated output. |
| `scripts/lint_publication.py` | Provide the publication-lint CLI. |
| `scripts/mlflow_export.py` | Export deterministic source-bound metrics and registry identities, with record-level comparisons. |
| `scripts/mlflow_publish.py` | Publish the committed, secret-scanned registry export idempotently; use the actual MLflow read endpoint for a safe credential precheck. |
| `scripts/publication_guard.py` | Reject placeholders and non-final page builds before publication. |
| `scripts/readme_research.py` | Generate README glance and generation sections from shared claims/registry. |
| `scripts/rebuild_presentation.py` | Reproduce every generated presentation surface from committed evidence. |
| `scripts/verify_mlflow_mirror.py` | Verify mirror content/routes and generate the verified route index. |
| `scripts/verify_release.py` | Extend surface agreement to the registry, headline and model lines. |
| `space-wasm/README.md` | Generated Static Space card with registry model identity and links. |
| `space/README.md` | Generated container card with registry model identity and links. |
| `src/delu_forecast/claims.py` | Owner-authorized v1 status, attribution and display-copy reconciliation. |
| `src/delu_forecast/derived.py` | Compute typed headline quantities and date-bounded policy counts; independently re-derive count/first-to-meet values from fresh source rows. |
| `src/delu_forecast/publication_lint.py` | Enforce mechanical reading-path rules, status-source discipline and parity. |
| `src/delu_forecast/registry.py` | Provide one source for policy identity, status, ordering, comparability and routes. |
| `src/delu_forecast/research.py` | Load typed hash-bound evidence records from preserved research outputs. |
| `src/delu_forecast/research_claims.py` | Render mapped research claims with derived values and registry tokens. |
| `tests/test_21_limitations_are_complete.py` | Re-scope limitations per model as standard §15 requires. |
| `tests/test_23_static_space.py` | Verify all bundle-referenced assets and startup states, including negative controls. |
| `tests/test_29_research_evidence.py` | Re-derive records with source/row/unit/revision negative controls. |
| `tests/test_30_research_claims_rendered.py` | Verify claim binding, numeric provenance, date/unit guards and final-route coverage. |
| `tests/test_31_page_structure.py` | Verify semantic chart/table/anchor/axis/marker contracts. |
| `tests/test_32_readme_ownership.py` | Verify generated-block ownership and difference labeling without content pins. |
| `tests/test_33_check_links_gate.py` | Prove a required missing destination fails the gate. |
| `tests/test_34_mlflow_export.py` | Check registry export/publishing contracts and safe service-specific precheck, including redirects, missing/wrong credentials or identity, and non-disclosure controls. |
| `tests/test_35_registry.py` | Check registry consistency with missing/unregistered surface negative controls. |
| `tests/test_36_derived_records.py` | Check derived arithmetic, date-bound counts, row-order invariance, corrupted count/first flags, earlier success and simultaneous-decision controls. |
| `tests/test_37_publication_lint.py` | Exercise codes, precision, percentages and status rule families with negative controls. |
| `tests/test_38_page_architecture.py` | Check page grammar, actual evidence-row order with misplaced-row controls, archive identity, system stack and evidence tiers. |
| `tests/test_39_cross_surface_parity.py` | Require shared headline/identity/model lines, with removal negative controls. |
| `tests/test_40_publication_guard.py` | Reject placeholders/non-final records and preserve hook ordering. |
| `tests/test_41_export_zero_diff.py` | Prove identity-only changes restore original artifact digests; reject substantive mutations. |
| `tests/test_42_publication_runbook.py` | Resolve runbook touchpoints and compare its contracts with code. |
