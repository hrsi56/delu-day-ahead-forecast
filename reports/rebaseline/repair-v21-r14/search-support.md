# CP-26 r14 support audit

This reconstruction uses the landed mask and whole-week rule. No training, forecast replay or CP-26 score was computed.

JSON SHA-256: `586525380e8552cce416fe44bb25525413fc936dc281a51160884e1a1d1e7ba8`.

| Route | Retained batch counts k=0..13 |
|---|---|
| nominal | [1, 7, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11] |
| noload | [1, 7, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11] |
| gfs6 | [1, 7, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11] |

| Search k | Date | Route | B | Newest retained batch | min train / min hold |
|---:|---|---|---:|---|---|
| 0 | 2020-01-15 | nominal | 1 | 2019-12-18 | 251 / 46 |
| 0 | 2020-01-15 | noload | 1 | 2019-12-18 | 251 / 46 |
| 0 | 2020-01-15 | gfs6 | 1 | 2019-12-18 | 251 / 46 |
| 1 | 2020-07-15 | nominal | 7 | 2020-06-17 | 398 / 81 |
| 1 | 2020-07-15 | noload | 7 | 2020-06-17 | 398 / 81 |
| 1 | 2020-07-15 | gfs6 | 7 | 2020-06-17 | 398 / 81 |
| 2 | 2021-01-13 | nominal | 11 | 2020-12-16 | 545 / 116 |
| 2 | 2021-01-13 | noload | 11 | 2020-12-16 | 545 / 116 |
| 2 | 2021-01-13 | gfs6 | 11 | 2020-12-16 | 545 / 116 |
| 3 | 2021-07-14 | nominal | 11 | 2021-06-16 | 588 / 140 |
| 3 | 2021-07-14 | noload | 11 | 2021-06-16 | 588 / 140 |
| 3 | 2021-07-14 | gfs6 | 11 | 2021-06-16 | 588 / 140 |
| 4 | 2022-01-12 | nominal | 11 | 2021-12-15 | 588 / 140 |
| 4 | 2022-01-12 | noload | 11 | 2021-12-15 | 588 / 140 |
| 4 | 2022-01-12 | gfs6 | 11 | 2021-12-15 | 588 / 140 |
| 5 | 2022-07-13 | nominal | 11 | 2022-06-15 | 586 / 138 |
| 5 | 2022-07-13 | noload | 11 | 2022-06-15 | 586 / 138 |
| 5 | 2022-07-13 | gfs6 | 11 | 2022-06-15 | 586 / 138 |
| 6 | 2023-01-11 | nominal | 11 | 2022-12-14 | 584 / 136 |
| 6 | 2023-01-11 | noload | 11 | 2022-12-14 | 584 / 136 |
| 6 | 2023-01-11 | gfs6 | 11 | 2022-12-14 | 584 / 136 |
| 7 | 2023-07-12 | nominal | 11 | 2023-06-14 | 581 / 133 |
| 7 | 2023-07-12 | noload | 11 | 2023-06-14 | 581 / 133 |
| 7 | 2023-07-12 | gfs6 | 11 | 2023-06-14 | 581 / 133 |
| 8 | 2024-01-10 | nominal | 11 | 2023-12-13 | 579 / 131 |
| 8 | 2024-01-10 | noload | 11 | 2023-12-13 | 579 / 131 |
| 8 | 2024-01-10 | gfs6 | 11 | 2023-12-13 | 579 / 131 |
| 9 | 2024-07-10 | nominal | 11 | 2024-06-12 | 581 / 133 |
| 9 | 2024-07-10 | noload | 11 | 2024-06-12 | 581 / 133 |
| 9 | 2024-07-10 | gfs6 | 11 | 2024-06-12 | 581 / 133 |
| 10 | 2025-01-08 | nominal | 11 | 2024-12-11 | 582 / 134 |
| 10 | 2025-01-08 | noload | 11 | 2024-12-11 | 582 / 134 |
| 10 | 2025-01-08 | gfs6 | 11 | 2024-12-11 | 582 / 134 |
| 11 | 2025-07-09 | nominal | 11 | 2025-06-11 | 585 / 137 |
| 11 | 2025-07-09 | noload | 11 | 2025-06-11 | 585 / 137 |
| 11 | 2025-07-09 | gfs6 | 11 | 2025-06-11 | 585 / 137 |
| 12 | 2026-01-07 | nominal | 11 | 2025-12-10 | 587 / 139 |
| 12 | 2026-01-07 | noload | 11 | 2025-12-10 | 587 / 139 |
| 12 | 2026-01-07 | gfs6 | 11 | 2025-12-10 | 587 / 139 |
| 13 | 2026-07-08 | nominal | 11 | 2026-06-10 | 587 / 139 |
| 13 | 2026-07-08 | noload | 11 | 2026-06-10 | 587 / 139 |
| 13 | 2026-07-08 | gfs6 | 11 | 2026-06-10 | 587 / 139 |

Admission is min(train) = N minus support of the m heaviest complete weeks; min(hold) = support of the m lightest. The pool excludes the most recent seven days.

The reported B vector reproduces: True. First-window 251/46 reproduces: True.

The future pilot must price all 42 searches, up to 31575 trial/batch fits (excluding daily member fits, failed work and reproduction).

Reproduce under the cumulative monitor:

```sh
python scripts/cp26_rebaseline.py monitor --name repair-r14-support --workers 1 -- python scripts/cp26_search_support.py --lead "$PWD" --output "$PWD/reports/rebaseline/repair-v21-r14/search-support.json"
```
