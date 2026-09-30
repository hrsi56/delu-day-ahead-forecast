# Track B Checkpoint Brief — CP-21 (programme 4.5: three-block LightGBM on top of v3)

## Target
- Repository: DE-LU day-ahead forecasting, `/Users/djourno/Downloads/PJM` (origin
  `hrsi56/delu-day-ahead-forecast`).
- Authorized checkpoint: CP-21, exactly one.
- Ratified plan anchor: `capstone_v21.md`, revision v21-r6, §17, ratified by the Owner on
  2026-09-29, SHA-256 `ee402c4703d176f8181ed82966c978ad84c3c73a0cdb1d3567871f58bc867344`.
  Its amendment record is `docs/track-b/capstone_v21-r5-to-v21-r6-amendments.md`, SHA-256
  `a9086fa1d70ea9cfd9c7fde3733f631bff7b8e372a8990e6cc7a52be3650bedd`. Verify both hashes; you
  need not read the record.

## Orchestrator-reported expected state
- **Branch / commit:** `main` = `origin/main` at the v21-r6 ratification commit. It is a direct
  child of `05587acdcf0536196678b444a4806c7f05c47cb5` and adds five documents:
  - `capstone_v21.md`;
  - the amendment record above;
  - `docs/track-b/cp-21-publication-plan-2026-09-29.md`;
  - `docs/track-b/v3-plan-handoff-2026-09-22.md`;
  - `progress.md`.

  No `gauntlet/*` branch, no worktree besides the primary checkout, no stash.
- **Working tree:** the primary checkout may carry one uncommitted Orchestrator change,
  `שאלות תשובות.docx` (a Q&A entry). It is not CP-21's; leave it untouched. Your ignored
  checkpoint folder holds this brief's canonical copy at `.local/artifacts/cp-21/issued-brief.md`.
- **What already exists:**
  - **CP-20's accepted evidence:** `land/cp-20` = `f450bc1`, `evidence/cp-20` = `a7a9b2e`.
    - `reports/weather-ablation/`, including saved predictions for B0, B1, B2, B3, A1, H0 and HG
      on 10,747 keys, the protocol, the lineage and the frozen weather conversion;
    - CP-16's input manifest of 638 fold/date origins;
    - the CP-15 LightGBM recipe in `reports/cp15/protocol.json`;
    - the code under `src/cp15/`, `src/cp16/` and `src/cp20/`.
  - **Retained local material:** under `.local/artifacts/cp-20/` (see
    `docs/track-b/local-artifacts.md`):
    - decoded GFS box grids for all 2,476 runs;
    - the cached HG component forecasts, by fold.
  - **Tooling:** LightGBM is already pinned. The MLflow exporter is `scripts/mlflow_export.py`,
    the published exports are in `reports/presentation/mlflow-export/`, and the packet template
    is `docs/track-b/publication-packet-template.md`.
- Verify all of this yourself before relying on it, and report any material mismatch.

## Observable outcome
A local, independently reviewed CP-21 evaluation on `gauntlet/cp-21`. When it closes:

- L-P, L-R, L-N and HGL are issued for all 10,747 original keys;
- all eleven policies are scored with the paired, per-fold and ratio uncertainty §17.5 requires;
- §17.6's four-condition rule has been applied mechanically, giving v4 or "Not adopted", with
  the first unmet condition;
- the block-split finding from L-R − L-P is stated, with §17.5's reading;
- the fit-cost and daily-retrain diagnostic is delivered;
- the publication packet and the draft MLflow export are complete;
- one fresh Integration-Critic PASS binds the exact final candidate;
- nothing is on `main`, nothing is pushed and nothing is written publicly.

A complete, valid "Not adopted" result is a successful checkpoint.

## Complete authoritative checkpoint bar
`capstone_v21.md` v21-r6, **§17.10: all thirteen items.** The governing specification is §17.1–
§17.9 and §17.11. It inherits §§2–4, §8's six diagnostics, §9, §§14.1–14.6, §§15.1–15.3 and §16,
as §17.1 states. Every item is mandatory; this brief's extract never narrows it.

## Task-specific supporting extract
A convenience summary only. §17 controls wherever it differs.

**Arms (§17.2):**

| ID | Role | Construction |
|---|---|---|
| HG | Comparator, saved | CP-20's v3 |
| L-P | Attribution | Pooled 24-hour LightGBM, raw target |
| L-R | Attribution | Three-block LightGBM, raw target |
| L-N | Attribution | Three-block LightGBM, §4-normalized target |
| HGL | Sole adoption candidate | Central `(1/3)·A1_w + (1/3)·B2_w + (1/6)·L-N + (1/6)·L-R`, where A1_w and B2_w are HG's own components, bit for bit. HG's H layer is re-estimated on HGL's own errors. |

- **Blocks:** Europe/Berlin local hours: night 22–05, solar 10–16, shoulder/peak 06–09 and
  17–21.
- **LightGBM arms:** every one has exactly HG's information: the inherited 23-feature B3/A2
  recipe, plus the three frozen GFS columns and their missing indicators under §15.3.
- **Capacity grid:** at most 4 configurations per model, the largest 600 trees / 63 leaves.
  Select on each origin's last 28 training days (EUR/MWh MAE; ties go to the smaller
  configuration), then refit. Daily fits; seed 42.
- **Population:** CP-20's: 10,747 keys, five folds, 638 origins, the same warm-up.
- **Scoring:** S_MAE and S_WIS. Bootstrap: seed 15042, 2,000 replicates of 7-calendar-day blocks.
- **Ratio intervals:** from this checkpoint's own draws, with every replicate stored.
- **Stress period:** fold 3; the 17-day peak is descriptive.
- **Contrasts:**
  - primary: HGL − HG;
  - secondary, descriptive: L-R − L-P, L-P − B3, L-N − L-R, and L-P, L-R, L-N each against HG.

**Adoption (§17.6), all four conditions:**

1. Upper 95% endpoint of ΔS_WIS < 0 and of ΔS_MAE ≤ 0 (HGL − HG).
2. All six original §8 diagnostics met.
3. Engineering PASS and every key issued.
4. No fold whose per-fold paired daily-loss 95% interval for HGL − HG lies entirely above zero,
   in MAE or WIS.

**Controls (§17.7).** Positive controls must survive the model's own transforms. Trees ignore
monotone rescaling, and normalization cancels uniform price scaling, so:

- use a non-monotone weather perturbation;
- use a non-uniform D−1 price mutation for L-N.

Also required: pooled–block parity for L-P against L-R, blend and H-layer parity, the
2026-04-07 guard, and byte-exact storage of hash-bound files.

**Write paths (§17.11):**

- `src/cp21/`, `tests/cp21/`, `scripts/cp21_blocks.py`;
- `reports/block-challenger/`, `docs/track-b/evidence/cp-21/`;
- `docs/track-b/research-content/cp21-claims.md`;
- `scripts/mlflow_export.py` and its tests, only for the draft export;
- `pyproject.toml` and `uv.lock`, only if a necessary pin is missing;
- ignored: `.local/{worktrees,artifacts,tmp}/cp-21/` and `.local/mlruns/cp21`.

## Applicable constraints
- **Hardware and cost:** Apple M3, 16 GB, CPU only; BLAS 1; at most 4 concurrent threads across
  all jobs. $0 external cost.
- **Ceilings (§17.8), hard maxima counted from the first job, including controls, failures,
  repairs and independent review:**

  | Item | Maximum |
  |---|---|
  | Policies | 4 new |
  | LightGBM fits | 24,000 main; 35,000 in total |
  | HG components | 1,600 component-day attempts; 192,000 Lasso attempts |
  | Replay | 10,500 new policy-days |
  | Passes | 3 reference passes; 3 bootstrap passes |
  | Compute | 60 aggregate machine-hours |
  | Memory and disk | 10 GiB RSS; 20 GiB added disk |
  | Data and network | 0 bytes downloaded; 0 remote writes |

  Stop before the first exhausted cap and retain the partial evidence. No outcome-driven retry,
  new arm, grid change or scope reduction.
- **Data:**
  - no data retrieval; weather comes only from the retained CP-20 grids through the frozen
    conversion;
  - nothing dated after 2026-04-07 is read, scored, plotted or used for any choice;
  - no spent holdout, reserved tail, post-gate A69 or delivery-day actual.
  - inherited v21 §2 information and forecast-origin rules: origin D−1 11:00 UTC; released
    errors ≤ D−2, consumed once.
- **Evidence class:** every result is `development_post_selection`. There is no promotion, product
  or release claim; v1 remains the released product and demo. No economic run.
- **Before dependent work:** complete §14.6 E1–E4 for CP-21, estimating everything against every
  cap. An insufficient allowance returns a concrete blocker.
- **Calendar: no scheduled work on Friday or Shabbat,** Asia/Jerusalem, from Friday 00:00 to
  Sunday 00:00.
  - No job starts in that window or runs unattended into it.
  - Stop at an atomic checkpoint and resume after Shabbat on the Owner's message; the pause is
    not a terminal return.
  - No long unattended run is authorized.
- **Credentials:** none is needed. MLflow tracking is local only. Never read, print or type a
  credential value, and never bypass the secret guard (`AGENTS.md` § Credentials).
- **Reasoning capture:** name any interview-answer trigger in one line in your return. Do not
  edit the Q&A document.

## Timebox
About **32 active hours**, from orientation through the terminal return, with a hard ceiling of
**40 active hours** (§17.8). Report elapsed hours to the nearest half hour, active and compute
effort separately. Crossing the approximate figure is a scope check, not an automatic stop.
The hard ceiling is a stop.

## Owner-only actions already authorized
The Owner ratified v21-r6 and authorized CP-21 execution on 2026-09-29. The authorization
covers:

- local candidate and evidence commits on the disposable branch `gauntlet/cp-21`, with its
  isolated worktrees under `.local/worktrees/cp-21/`;
- byte-exact packaging of this brief as `docs/track-b/evidence/cp-21/issued-brief.md`, from
  `.local/artifacts/cp-21/issued-brief.md`, recording its SHA-256. Report any difference from
  the brief you were given.

Nothing else is authorized:

- no credential use;
- no destructive operation beyond your own checkpoint worktrees;
- no mainline staging or commit, push, tag, pull request or release;
- no MLflow, Hugging Face or DagsHub write;
- no data or model download;
- no governance edit.

## Publication packet and MLflow step
The landing templates do not yet carry this step, so this brief carries it (§17.9;
PUBLISH_RULES 1.1 §11; Publication Standard v1 §12).

- **Pinned rules:** PUBLISH_RULES 1.1, SHA-256
  `91eea445434718a163f03bcfd82e1db275a9d98311e76eb6cd1365f3707584f3`. It incorporates
  Publication Standard v1 (`01d721c2ba6316ca9a2f707e79da229bef732e91bad22f6ce457fb01e69478cc`)
  and presentation plan revision 3
  (`281193740a256a99a1676d53ef61c9babb5f744a7d0fb038927e305d1149812c`). Verify them.
- **The packet:** `docs/track-b/evidence/cp-21/publication-packet.md`, completing every section
  of `docs/track-b/publication-packet-template.md`
  (`4efb01855ae2d9a6f54b5624607a93046b1fffa881e34af0c6798c513c7829cf`):
  - draft registry entries: HGL as `v4 · <adopted change>` or as the branch "Three-block
    LightGBM on v3", per the rule; L-P, L-R and L-N as study arms; comparator HG; population
    `common-10747h`;
  - the claim map `docs/track-b/research-content/cp21-claims.md`, with the block-split finding
    and the B3 → L-P → L-R → HGL ladder, disclosing that the B3 → L-P step bundles weather with
    capacity selection;
  - the derived headline quantities: the verdict, the rule and its date (2026-09-29), the
    distance from HG, N, the ratio intervals with seed, replicates and block length, and
    per-fold MAE with fold 3 as the stress period;
  - draft slot texts for the outcome the rule yields;
  - §5b and §5d marked not applicable, with their reasons;
  - §8's intended identities for every surface.
- **MLflow:**
  - experiment `delu-generations`;
  - local tracking only, in `.local/mlruns/cp21`: parent `cp21`, children `cp21/HGL`,
    `cp21/L-P`, `cp21/L-R` and `cp21/L-N`;
  - a draft export `reports/block-challenger/mlflow-export-draft/cp21.json`, built through the
    exporter's code path from committed CP-21 evidence and the packet's draft entries. Its
    landing-time identities are explicit pending fields.
  - The published export set and its manifest stay unchanged, and `mlflow_export.py --check`
    passes on them.
- **No public surface changes:** the page, the README's generated blocks, the Space cards and
  bundles, the public registry's rendered entries and the existing exports. CI and
  `make verify` stay green.
- **Acceptance:** the Integration Critic reviews the packet and the draft export like any other
  artifact:
  - every number re-derives from committed rows;
  - names and statuses follow the draft entries and the mechanical verdict;
  - nothing already published changes.

Publication itself is a separate, later block after the Owner's landing.

## Stop and return
Return exactly one of PASS / BLOCKED / INCOMPLETE, using `docs/track-b/gauntlet-templates.md` §3,
with the publication packet attached. Include:

- both terminal SHAs and the verdict-only delta;
- every §17.8 resource total;
- the verdict: v4 or "Not adopted", with its reason;
- the block-split finding;
- branch and worktree accounting.

Do not begin, scaffold or plan the next checkpoint or the publication block. Do not commit to
`main`, publish or push.
