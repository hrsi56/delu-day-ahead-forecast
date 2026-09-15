# Lead import verification

All 21 Builder artifact digests matched after import. The two input-boundary tests passed in the core frozen environment (2 passed, 0.10 seconds). The core dependency lock remains unchanged.

The Lead separately reran the exact probe source offline in a new external scratch root using the Builder’s pinned Python environment, via:

```sh
uv run --frozen python -m cp15.reproduce_probe --python /Users/djourno/Downloads/PJM-cp15-feasibility/data/cp15-probe-env/bin/python --scratch /tmp/cp15-lead-probe-reproduction
```

Exit 0. Context, future load, input manifest, and forecast CSV matched all four saved SHA256 digests. Runtime was 5.973 seconds; sampled peak process-tree RSS was 908,820,480 bytes. Original Builder evidence was not overwritten. See `lead-reproduction/`. The new helper copies source/configuration into a new external directory and reuses the ignored model cache; it permits independent reproduction without dirtying a reviewed checkout. Recreate the environment from `requirements.freeze.txt` when the Builder worktree is removed.
