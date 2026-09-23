# CP-16 replay accounting correction

The Lead initially asked the residual Builder to report prediction policy-days. This omitted synthetic warm-up and therefore understated §14.5 usage. This was an engineering accounting error, not an ambiguity used to change the cap. No outer comparison or scoring occurred.

Static reconstruction of the actual test versions (no rerun):

| Job | issue attempts | predict attempts | 2 × all attempts | Additional pending registrations | Conservative debit |
|---|---:|---:|---:|---:|---:|
| Builder run 1: 17 pass/1 fixture failure | 388 | 24 | 824 | 0 | 824 |
| Builder run 2: 18 pass | 389 | 24 | 826 | 0 | 826 |
| Builder run 3: 19 pass | 472 | 27 | 998 | 4 | 1002 |
| Lead pre-run residual suite | 472 | 27 | 998 | 4 | 1002 |
| **Total** | **1721** | **102** | **3646** | **8** | **3654** |

Every warm-up issuance and failed assertion attempt is charged for both arms. No discount is taken for same-day issue/predict overlap. The eight extra policy-days conservatively account for two directly restored pending records in each final-version run, so a persistence refactor receives no discount. Earlier versions restored those records via issue(), already included.

The first immutability fixture failed because pandas already rejects its index mutation; the assertion was corrected to test memory isolation. Run 3 added three 28-day DST prediction populations and one nonfinite-truth test. All three versions included the invalid-persisted-state test. Earlier version counts are the bounded Builder's contemporaneous tool-history reconstruction, not a newly instrumented rerun; this provenance limit is explicit.

Production admission reserved 76 policy-days before interruption. Total conservative debit is **3730/4500**, leaving **770**. The planned full production pass is 1,276; 1,200 remain, already exceeding the allowance by 430 before outstanding controls or independent review. Even omitting the eight extra restoration charges would not make it fit.

The previously recorded 114 Builder plus 42 Lead successful policy-days were replaced with 3,654; the ledger adds 3,498, preserving its earlier event history. No scientific recipe, key set or cap was changed. A full synthetic-suite rerun is not authorized within the remaining allowance. Review may run the monitor/input-budget tests and bounded controls only; any residual execution must reserve its complete warm-up/replay debit first.

The first admission supervisor also failed on a disappearing lineage.json.tmp during atomic rename. The worker survived until the Lead explicitly sent SIGINT; its KeyboardInterrupt log and partial lineage are preserved. The unmonitored tail is charged to a later wall-clock upper bound, including idle time after the confirmed stop. Peak RSS during that gap is unknown and is not reconstructed. This run cannot demonstrate uninterrupted resource enforcement. The repair tolerates disappearing files and kills the process group on any supervisor exception; three regression tests cover the race, fail-closed termination and successful execution.
