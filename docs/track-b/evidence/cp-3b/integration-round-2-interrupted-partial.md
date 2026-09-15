# Verdict — M3.5/CP-3B — Integration — [IN PROGRESS — leaning FAIL on item 4]

- Candidate SHA: 87598a8dfd898d62adfd107c185c747c2a7a8141
- Plan / version / bar: capstone_V6_8.md, v6.8, §9.2 as amended 2026-09-15; CP-3B six-item bar
- Suspended clause confirmed in §9.2 at this SHA: yes (capstone_V6_8.md line 342)
- Worktree clean before: yes. After: (pending)

## Interim findings (being updated)
- make wasm exit 0; build_space exit 0; no tracked change; pytest 177 passed; verify_release exit 0 (disagreements: none); container 5/5; boundary diff empty.
- Item 2 independent host check: bitwise on fixture (11,628 values, 32,396 feature cells), 8 non-fixture slice days, 9 load scales, and the whole snapshot (2,774 days, 596,592 values); 1-ULP CQR perturbation breaks the gate for each of 4 thresholds; 8 code mutations all break it.
- Item 3 host-side browser module: mask D prices -> 0.0 bitwise on all 54 fixture days; D-1 all-24 +250 -> 220.9433340396028.
- Item 4: live HF Static Spaces serve LFS/Xet-tracked files as 302 (cache-control: no-store) to us.aws.cdn.hf.co with a per-request signed URL; the bundle's own .gitattributes routes png/ico/woff/woff2/ttf/wasm through LFS (9 cold-load requests); measurement assumes same-origin 200 as stored, 4 hosts.
