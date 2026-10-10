# 4.6L′ — DDNN-2 provenance record (CP-24), an addendum to CP-23's record

- **Checkpoint:** CP-24, under `capstone_v21.md` v21-r11 §23.7 (4.6L′), with §18.2–§18.4 and §21.3.
- **Extends:** CP-23's 4.6L record,
  [`reports/distribution-challenger/licence-admission.md`](../distribution-challenger/licence-admission.md)
  (SHA-256 bound by CP-23's artifact manifest and the blob at `evidence/cp-23`). Everything that
  record establishes stands unchanged: the user and the research setup (§1), the data licences
  behind the outputs (§4) and the use table with its two unresolved delivery uses (§5). This
  addendum records only what CP-24 adds or changes.
- **Check date:** 2026-10-05 (Asia/Jerusalem). The package licences below were read on that date
  from the installed packages' own metadata.
- **Effort:** under half an active hour, inside the 2-hour cap.
- **Result: PASS.** Provenance is established and no reference licence is unresolved, so DDNN-2 is
  admitted to the §23.7 correctness checks and 4.6R′. This record grants no operation, publication or
  delivery authority.

## 1. Provenance of the DDNN-2 implementation

**The code is original.** DDNN-2 is written from scratch in this repository, under the repository's
MIT licence ([`LICENSE`](../../LICENSE)), in two NumPy-only modules:

- `src/cp24/ddnn2.py`: the day-level network with 24 Johnson SU heads, the masked likelihood, the
  pinball loss through the Johnson SU quantile function, L1 and L2, input dropout, the analytic
  gradients, Adam, the training loop with random whole-week early stopping, the target transforms
  and their inverses, the cap and the per-level median ensemble;
- `src/cp24/sampler.py`: the search procedure (the space, the seeded random sampler, the
  validation-batch tiling, successive halving, the ranking and the ensemble choice).

Both import NumPy and the Python standard library only (§23.3, §18.2); the import audit
(`tests/cp24/test_numpy_only.py`, `src/cp24/audit.py`) checks both, with fixtures that fail it.
CP-23's `src/cp23/ddnn.py` is not modified and not imported by the model code; DDNN-2 reuses its
Johnson SU parameterisation (§23.3) as a written-down formula.

**Nothing third-party was copied.** No third-party DDNN or DNN code was copied or adapted — not the
epftoolbox code, not any Keras or Optuna code — and no pretrained weights are used: every network
starts from a seeded random initialisation and is trained at its own origin or batch. The
implementation follows the published methods below, not any code. No hyperparameter-optimisation
library is used: the random search and successive halving are written in NumPy.

**Method sources** (in addition to CP-23's record, §2):

| Element | Source |
|---|---|
| Day-level multi-output DDNN, whole-day input vectors, input-group flags, batch-rolling validation, random 20% early-stopping holdout, an ensemble of tuned configurations | G. Marcjasz, M. Narajewski, R. Weron, F. Ziel (2023). *Distributional neural networks for electricity price forecasting.* Energy Economics 125, 106843 |
| Day-level DNN with whole-day vectors; early stopping on randomly selected weeks so the most recent data is trained on | J. Lago, G. Marcjasz, B. De Schutter, R. Weron (2021). *Forecasting day-ahead electricity prices: a review of state-of-the-art algorithms, best practices and an open-access benchmark.* Applied Energy 293, 116983 |
| Median/MAD standardisation and the asinh variance-stabilising transform | B. Uniejewski, R. Weron, F. Ziel (2018). *Variance stabilizing transformations for electricity spot price forecasting.* IEEE Transactions on Power Systems 33(2), 2219–2229 |
| Random search | J. Bergstra, Y. Bengio (2012). *Random search for hyper-parameter optimization.* JMLR 13, 281–305 |
| Successive halving | K. Jamieson, A. Talwalkar (2016). *Non-stochastic best arm identification and hyperparameter optimization.* AISTATS |
| Quantile (pinball) loss as a proper score; minimum-score estimation | T. Gneiting, A. E. Raftery (2007). *Strictly proper scoring rules, prediction, and estimation.* JASA 102(477), 359–378; T. Gneiting (2011). *Quantiles as optimal point forecasts.* IJF 27(2), 197–207 |
| Robust (median) combination of member quantiles | K. C. Lichtendahl, Y. Grushka-Cockayne, R. L. Winkler (2013), as in CP-23's record |
| Dropout | N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever, R. Salakhutdinov (2014). *Dropout: a simple way to prevent neural networks from overfitting.* JMLR 15, 1929–1958 |
| L1 and L2 penalties, ReLU, softplus and tanh activations | Standard textbook material (e.g. I. Goodfellow, Y. Bengio, A. Courville (2016). *Deep Learning.* MIT Press) |

**Inputs.** DDNN-2's design matrix comes from the project's admitted feature pipeline: CP-15's
prepared inputs and LEAR day design (`src/cp15/data.py`, with its DST convention), CP-15's LightGBM
price statistics and calendar set, and CP-20's three frozen GFS columns with their missing
indicators — exactly v4's sources (§23.3). The pipeline glue (`src/cp24/design.py`,
`src/cp24/member.py`) is outside the NumPy-only rule (§18.2 item 3).

## 2. How the test-only reference is reused

- **The reference is CP-23's, unchanged.** PyTorch 2.14.1 (CPU) is CP-23's test-only reference,
  pinned in CP-23's separate test-only uv project `tests/cp23/torch-reference/` (`uv.lock` SHA-256
  `b3164a375e871396e685d0e887972b092fcd0c24a7fe0047167e8fc41c25dfed`, as the brief and §23.7 pin).
  No new lock is created under `tests/cp24/`. The root `pyproject.toml` and `uv.lock` are not changed.
- **No download.** The pinned packages are already installed in the project's environment from that
  lock (CP-23's install of 2026-10-04). CP-24 downloads nothing; the one permitted download is unused.
- **How it runs.** Only inside the explicitly invoked `tests/cp24/torch_reference_checks.py`, by the
  monitored `reference-checks` job, on fixed synthetic inputs (no research data). It never trains a
  scored model, emits a forecast or enters evidence (§18.3). A missing PyTorch fails that step and is
  never a skip; CI installs only the root lock and collects only the committed record's test.
- **Licences, as installed (checked 2026-10-05), unchanged from CP-23's record §3:**

| Package | Version | Licence (installed metadata) |
|---|---|---|
| torch | 2.14.1 | Apache-2.0 AND Apache-2.0 WITH LLVM-exception AND BSD-2-Clause AND BSD-3-Clause |
| sympy | 1.14.0 | BSD |
| mpmath | 1.3.0 | BSD |
| networkx | 3.7 | BSD-3-Clause |
| fsspec | 2026.9.0 | BSD-3-Clause |
| filelock | 4.0.10 | MIT |
| setuptools | 84.0.0 | MIT |

  Every licence permits local use, none restricts the outputs of code that merely imports the
  package, and no PyTorch file is redistributed or enters an artifact. **No reference licence is
  unresolved.**

## 3. Uses

CP-23's use table (§5 of its record) applies to DDNN-2's outputs unchanged: research and local
comparison, and local retention, are permitted under the stated conditions; publication, local
prospective operation and public demonstration are permitted by the licences but **not authorized by
CP-24** (publication follows the Owner's LAND, §23.12); the hosted service and the product stay
**unresolved** and are carried to 4.7 and 4.10.

## 4. Disposition

**PASS.** Provenance is established, no third-party code or weights were copied, and the reference's
licences are resolved. The route continues to the §23.7 correctness checks, then 4.6R′.
