# CP-20 pre-review evidence

These are copies of local run evidence from `.local/artifacts/cp-20/` (not committed there),
taken at the final candidate before the Integration review:

- `logs/`: every monitored job log (extraction chain, assembly, protocol, HG components,
  admission, comparison, controls, scoring, tests, guards).
- `markers/`: DONE/FAILED markers, including superseded ones.
- `ledger-snapshot-before-review.json`: the cumulative section 15.5 ledger before review.
- `chain-status.run{1,2,3}.json`: the three extraction chain runs.
- `job-code-versions.jsonl`: the code version each extraction job recorded itself.
- `failures.jsonl`: classified extraction failure records. Every affected run later completed,
  and none was imputed.
- `o2-a1-restored-attempts.jsonl`: locator-defect attempts restored under Owner decision O2-A1.
- `prerun_replacement_attempts.jsonl`: Owner decision O1 replacement attempts.

Not copied because of size, and kept locally:

- `attempt-outcomes.jsonl` (27 MB) and `requests.jsonl` (87 MB), summarised in
  `reports/weather-ablation/resources.json`.
- The decoded run boxes and retained raw samples, which are not redistributed; see
  `reports/weather-ablation/rights-notice.md`.

The Integration assignment, verdict, final resources and the checkpoint return are added
afterwards as an evidence-only delta.
