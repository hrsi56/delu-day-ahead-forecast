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

F2, F3 and F4 are pending at this record's initial write; the completion entries below will record the actual outcomes before terminal review.

## Retained F1 artifacts

- `.local/tmp/pres-1/f1-upload.log`: SHA-256 `af79749f2a1529ee9e91cbbc245199a3ee59ac774b8a3dd9ba1ab97af018e767`.
- `.local/tmp/pres-1/pre-f1-export-digests.json`: SHA-256 `71f35277fe79bdba41872d4470a779627f94322d4d44320cf312dab692c64105`.
- `.local/tmp/pres-1/pre-f1-protected-public-state.json`: SHA-256 `c2a402c73bad57a2019fbf14eae039c532176b2d082ff9c0e557480d10f80407`.
- `.local/tmp/pres-1/pre-f1-dry-run.log`: SHA-256 `9a718eefa28c519afef046d73243ddec45a3cd51fb47115f27042b231b7d0d16`.
