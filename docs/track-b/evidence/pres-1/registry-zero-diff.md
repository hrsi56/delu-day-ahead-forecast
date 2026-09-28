# PRES-1 conformance W2: the registry's introduction changes nothing a reader sees

**Brief W2 acceptance:** the registry's introduction is proven to change nothing. The rebuilt
`docs/index.html` and README are byte-identical, and the MLflow export differs only in names,
descriptions and tags, shown by a record-level diff in which every metric, history point,
parameter and artifact digest is unchanged.

- **Before:** `af0abb090ad3eba2888c3791ebe3cdcf28409a7f` (the candidate the brief names; `5e84a5b`
  added only the W1 evidence copies).
- **After:** `6f08b95` (the registry, and every surface reading it), with the CP-10 selection notes
  restored to the registry in the commit that records this file.
- **Where:** the lead worktree, clean at the "after" commit; 2026-09-28, local Python 3.13.

## The rendered surfaces: byte-identical

```text
uv run python scripts/rebuild_presentation.py          # exit 0: every surface rebuilt, agreement and zero-fetch checks pass
git diff --quiet af0abb0 -- <file>                     # exit 0 for each file below
```

| File | Git blob after the rebuild | Equal to `af0abb0` |
|---|---|---|
| `docs/index.html` | `22248fc1be25d81a5d52cfc4e103b4502bfa3f0b` | yes |
| `README.md` | `e8e288f63560f079e74e2cd3c2fcf7c5c76bf2e3` | yes |
| `space/README.md` | `fd2c3e71c9b36494de5628239c9c3520b8a8eeb1` | yes |
| `space-wasm/README.md` | `0dc6ca3d3549624ed80f3ec0b7e45a1a4f2a82ac` | yes |
| `reports/cp3/pages_build.json` | `bdc49c2a759330df6c5b3e3471341258143421d0` | yes |

What now reads the registry, on the page: the opening's status pair, the rail, the jump row, the
lineage's nodes and branches, the comparison's rows, the rows of the v2 scores chart and the
crisis-window chart, the per-period and coverage charts' generations, the hour-of-day chart's two
series, the marker key, and the chapter order and headers. In the README: the research block's
headings and its released/research sentence. In the export: every run name, parent name,
description and identity tag. The hand-written maps they replace (`POLICY_NAMES`, `POLICY_ROLES`,
`GENERATION_OF`, `OVERVIEW_ROWS`, the lineage literals, `CHILDREN`, `GENERATION`) are gone. Where
a surface showed an identity by something other than its canonical name, the registry now carries
that context label (`registry.CONTEXT_LABELS`), so the introduction could be byte-identical; the
conformance work then replaces those labels with the canonical names.

## The MLflow export: names, descriptions and tags only

```text
uv run python scripts/mlflow_export.py --diff-against af0abb0 --to 0f93205 \
    --out reports/presentation/release-checks/2026-09-28-registry-export-diff.json
# runs 23 -> 23; checked {'params': 155, 'metric_points': 6928, 'datasets': 39, 'artifacts': 55,
#   'artifacts_digest_unchanged': 9, 'artifacts_old_digest_on_restoring_identity': 46};
# identity changes on 23 runs; substantive changes: none; only_identity=True   (exit 0)
```

`--to 0f93205` compares the export committed at the registry's introduction, so the record stays
reproducible after later commits change the export.

The diff (`scripts/mlflow_export.py`, `diff_exports`) compares the two exports run by run:

| Compared | Result |
|---|---|
| Run keys | the same 23, each once |
| Parents | unchanged on every run |
| Parameters | all 155 unchanged |
| Metric histories | all 6,928 points unchanged by key, step, timestamp and value; units unchanged |
| Datasets | all 39 unchanged |
| Chart artifacts (9 SVG files) | SHA-256 unchanged |
| `summary.json` and `README.md` (46 files) | SHA-256 changed, because each carries the run's identity; with `af0abb0`'s run name and tags put back, each reproduces `af0abb0`'s SHA-256 exactly (46 of 46) |
| Changed | every run name; the tags `delu.public_name`, `delu.generation`, `delu.adopted` and `mlflow.note.content`; the new tags `delu.registry_id`, `delu.kind`, `delu.status` and `delu.comparator`; the experiment's description |

### Byte identity and content preservation

The acceptance asks for an unchanged digest on every artifact, and for changed names, descriptions
and tags. Two kinds of artifact meet it in two different ways, and the record keeps them apart:

- **Byte identity.** Every parameter, metric history point and dataset, and every artifact that
  carries no identity (the 9 chart SVG files): the SHA-256 is unchanged.
- **Content preservation, proven at the digest.** `summary.json` holds the run's name and tags, and
  `README.md` its name as the title line. A renamed run cannot keep their bytes, so their digests
  change by construction. The diff therefore restores the old identity fields into each new
  artifact (`_restored_artifact`) and requires the old SHA-256 back, byte for byte. That shows the
  only bytes that changed are the identity fields' values; removing fields and comparing the rest,
  as the first version of this record did, could not show that. Any other change in either file
  fails, and `tests/test_41_export_zero_diff.py` proves it with negative controls: a number inside
  `summary.json`, the body of `README.md`, a metric point, a parameter and a chart.

The page, the README, both Space cards and `pages_build.json` needed no such distinction: they are
byte-identical (above).

Two identity changes are corrections the registry makes, not accidents of the refactor:
`cp10/v1_reference` is now tagged as v1 (`delu.generation=v1`, `delu.adopted=true`), because the
CP-10 reference is the released v1's own calibration; and the pooled-interval control no longer
carries a version number in its name, because a number is given only on adoption (plan §16
decision 2).

**Final names.** The run names above are the names the public upload (F1) will carry; they are
fixed here, before F1 (brief §5.1). The experiment's description now says the repository is the
source of truth (standard §8).

## The checks that keep it true

- `tests/test_35_registry.py`: every entry carries every §5 field; one identity across codes;
  derived status; and the consistency checks, with negative controls (a generation without its
  chapter or rail entry, an unregistered generation on the page, a missing or unregistered README
  heading, an unregistered or missing run). The README's v1 heading arrived with W9; its positive
  check, a strict expected failure until then, now passes.
- `tests/test_34_mlflow_export.py`: the export matches the registry, with negative controls; it
  replaced the fixed count of 23 runs (W14).
- `tests/test_41_export_zero_diff.py`: a rename is identity-only and restoring it reproduces the old
  digests; negative controls for a changed number inside `summary.json`, a changed `README.md` body,
  a metric point, a parameter and a chart; and the committed record above proves the introduction.
