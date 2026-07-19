# AWS Extension Spec v1.0 — Cloud Production Backbone for the Flagship DE-LU Capstone

**Status: DRAFT — pending owner ratification.** On ratification this document amends `capstone_V6_2.md` → **v6.3** (additive amendment + one rewritten §13 boundary, same pattern as the v6.2 spectral amendment). Authored 2026-07-19 against capstone v6.2 in full, the 2026-07 SageMaker cost/effort research memo, and progress.md (2026-07-15). All AWS prices are official mid-2026 list rates from that memo unless flagged; a 10-minute re-verification of the pricing table is a mandatory first task of the arc (§10, R-8).

---

## 0. What this spec ratifies (eight decisions)

- **D1 — Scope & placement.** A lean AWS production backbone (train → register → deploy → monitor on SageMaker) is added to the **flagship**, as a new post-G5 milestone **M6 (two phases, AWS-1 / AWS-2)** with checkpoint **CP-6**. The companion mini-capstone is untouched in content and stays stage-gated.
- **D2 — The two-plane invariant.** The recruiter-facing surface has **zero AWS runtime dependency**. AWS is a production backbone that *produces* artifacts; recruiters see evidence of it, never wait on it. Enforced by CP-6 gates (§7).
- **D3 — Inference policy.** Scale-to-zero only: **Batch Transform** (the product path) and one **Serverless Inference endpoint** (the live-serving proof, owner-invoked only). Persistent/always-on real-time endpoints are **forbidden**; a scripted create→demo→destroy real-time endpoint is permitted for live interviews only. **Keep-alive pings of any kind, on any platform, are forbidden.**
- **D4 — Budget amendment.** The flagship budget line changes from "$0 expected run rate" to: **$0 baseline + AWS backbone ≤ $5/month expected (engineering target $1–3/month measured)**; the **$65/month policy ceiling is unchanged**; AWS Budgets alert at **$10** and alarm at **$50** are mandatory day-one infrastructure.
- **D5 — Monitoring is custom-built.** Drift/data-quality monitoring is a scheduled SageMaker **Processing job publishing custom CloudWatch metrics + alarms** — not SageMaker Model Monitor, which **closed to new customers on 2026-07-30** and is unavailable to an account onboarding in 2027. This is a deliberate, defended design choice (§9, Q2), not a workaround.
- **D6 — Region.** `eu-central-1` (Frankfurt) — narrative coherence with the DE-LU market ("the model runs where the market clears"). ~5–15% price premium over us-east-1; immaterial at this scale (worst case ≈ +$0.40/month). Fallback us-east-1 permitted if arc-start price re-verification surfaces a surprise; either region passes every gate in this spec.
- **D7 — Recruiter first-touch becomes a true static page.** The primary portfolio URL becomes a **statically exported HTML report** (marimo `export html` output on **GitHub Pages** — $0, CDN-served, never sleeps, loads in ~1–2 s), containing the full §10 reading-order content plus the new architecture section. The interactive marimo Space remains the deep-dive artifact, linked from the static page with an honest "interactive demo — may take ~30 s to wake if asleep" label. This is the only way to satisfy "no recruiter waits > 5 s" AND "$0" AND "no pings" simultaneously — see §2.2 for why.
- **D8 — Sequencing.** M6 runs in **program Month 6 (≈ Feb 2027)**, immediately after G5. The companion arc shifts to **Months 7–8 (≈ Mar–Apr 2027)**; **G6 moves to ~late-Apr 2027**. Program hours: ~680 → **~740** (+55–75 h). Full cascade in §8.

---

## 1. Direct answers to the owner's constraints

Every constraint from the commissioning message, answered without holes:

**"Minimum cost, including after the two free months."** Steady-state post-free-tier run rate is **≈ $1.20–3.00/month (≈ ₪4–9)**, itemized in §6. The free tier is used tactically, not relied on: the 2-month SageMaker free-tier clock starts at the **first SageMaker resource creation**, so the arc creates its first SageMaker resource on AWS-1 day 1 and the free window covers the entire build — the heaviest-usage period. Everything in this spec is priced **as if the free tier did not exist**; the free tier is upside, not a dependency.

**"No endless hourly-billed compute."** Every compute element in this design is a **bounded job measured in minutes** (training ≈ 3–6 min, batch forecast ≈ 2–5 min, drift job ≈ 3–5 min, ~4–5 runs/month total). The only AWS construct that bills continuously while idle — a persistent real-time endpoint — is **forbidden by D3**. There is no resource in the ratified architecture whose cost grows while nobody is using it, and the `make aws-audit` gate (§5.9) proves it at every session close.

**"No pages that cost money to keep alive, and no cold start [for recruiters]."** The classic warm-cost-vs-cold-start tradeoff only exists when a viewer's page performs live inference. In this architecture **no recruiter-facing surface performs live inference or touches AWS at all** — the static page is pre-rendered HTML, and the interactive Space serves everything from the precomputed lookup bundled in its image (v6.2 §9.2, unchanged). The paradox doesn't need to be balanced; it is dissolved by decoupling. The serverless endpoint's 1–3 s cold start lands only on Yarden's own scripted invocations, never on a recruiter's browser.

**"No pings."** Ratified as a hard rule (D3). No GitHub Actions cron pinging the HF Space (v6.2 §9.2 already distrusted it; this spec deletes the option entirely), no endpoint keep-warm invocations, no scheduled wake-ups anywhere. The <5 s guarantee is carried by architecture (D7), not by heartbeats.

**"No recruiter stuck on a >5 s loading page."** Guaranteed at the only point it can be guaranteed: the **first-touch URL is static HTML on a CDN** — no container, no runtime, no sleep state, ~1–2 s load worldwide. CP-6 makes it a gated, measured property (§7, items 11–12). The interactive Space keeps v6.2's honest CP-5 posture (warm < 5 s; cold ≤ 30 s with a stated disclaimer) — but it is no longer the page a recruiter lands on cold. **Honesty note (the one impossibility, stated plainly):** keeping the *interactive container itself* simultaneously free, never-cold, and unpinged is not possible on any free tier — HF free sleeps after ~48 h idle, and the paid keep-warm (~$22/month CPU Upgrade) plus pings are both rejected. D7 is the correct resolution: recruiters get instant static; the wake cost is paid only by a viewer who explicitly chooses the live demo, with the wait labeled in advance. Nothing is hidden, nothing loads slow unannounced, nothing costs idle money.

**"Prove I can work on AWS."** Proof is delivered on three planes: (i) **public code** — the `infra/` directory with IAM policies, pipeline definition, deploy/teardown scripts, and the parity test, in the public repo; (ii) **evidence artifacts** — architecture diagram, pipeline-DAG screenshot, Model Registry lineage screenshot, CloudWatch drift dashboard, and the monthly bill screenshot, embedded in the static page and README; (iii) **live capability on demand** — a scripted interview demo that trains, registers, and serves in real time (§5.7). A hiring manager can verify the capability in 90 seconds without an AWS login; an interviewer can watch it live.

**"Work against the full capstone, in coordination with it."** §11 is a section-by-section amendment map against v6.2's actual text — every touched section, every preserved invariant, and the one §13 boundary this extension rewrites.

---

## 2. Architecture — the two-plane design

### 2.1 The invariant

> **Plane A (Showcase — what recruiters touch)** never calls **Plane B (Backbone — what AWS runs)** at request time. Coupling is one-way, artifact-level, and human-triggered: the weekly pipeline run *produces* files; Yarden reviews and commits them into Plane A.

```
PLANE B — AWS backbone (eu-central-1)                PLANE A — Showcase (all $0, unchanged + hardened)
─────────────────────────────────────                ─────────────────────────────────────────────────
ENTSO-E/SMARD weekly snapshot (manual pull)          ┌────────────────────────────────────────────┐
        │                                            │ 1. STATIC PAGE  (GitHub Pages)   [NEW, D7] │
        ▼                                            │    marimo `export html` — full reading     │
S3  s3://delu-forecast-prod/                         │    order + architecture section            │
  raw/ features/ models/ lookups/ monitoring/        │    ~1–2 s load, never sleeps, $0           │
        │                                            │            │ links to                      │
        ▼                                            │            ▼                               │
SageMaker Pipeline  (manual weekly trigger)          │ 2. INTERACTIVE marimo Space (HF, v6.2 §9.2)│
  validate → features → train → evaluate-gate        │    precomputed lookup, 3 sliders, OOD flags│
  → register → batch-forecast → drift-metrics        │    warm <5 s; cold ≤30 s, labeled          │
        │                │                           │ 3. DagsHub MLflow public UI (v6.2 §9.1)    │
        ▼                ▼                           │ 4. GitHub repo (incl. infra/)              │
  Model Registry    CloudWatch metrics               └────────────────────────────────────────────┘
  (lineage proof)   + alarms + Budgets                        ▲
        │                                                     │  artifacts committed by Yarden:
        ▼                                            snapshot.parquet, lookup.parquet,
  Serverless endpoint (scale-to-zero,                static HTML, evidence PNGs
  owner-invoked proof; $0 idle)                      (one-way, human-in-loop)
```

### 2.2 Why this is the only shape that satisfies all constraints at once

A recruiter-facing page can be fast in exactly three ways: pay to keep a container warm (rejected: idle cost), ping it awake (rejected: explicitly forbidden, and GH-cron pings self-disable after 60 days of repo inactivity anyway — v6.2 §9.2 already documented this), or **be static**. D7 takes the third. Simultaneously, an AWS deployment can be cheap in exactly one way at this traffic: **scale-to-zero**, which necessarily has cold starts — acceptable only if no recruiter ever experiences them, which the decoupling guarantees. The two constraints that look contradictory ("deployed on AWS" / "nothing slow, nothing idle-billed") are satisfied by putting them on different planes.

### 2.3 The registry duality, stated honestly

DagsHub MLflow remains the **public** experiment-tracking and registry story (free, public read — v6.2 §9.1 unchanged). SageMaker Model Registry is the **cloud-native lineage** story (versioned model packages, approval status, metadata: git SHA, snapshot checksum, eval metrics). The same champion artifact is registered in both; CP-6 item 4 asserts byte-level identity via checksum. Interview framing: "MLflow is my public lab notebook; the SageMaker Registry is the deployment gatekeeper — same artifact, two audiences."

---

## 3. What the backbone actually does — the weekly refresh, before vs. after

The backbone does not invent a new workload; it **productionizes the exact weekly refresh v6.2 §9.2 already mandates** ("snapshot refreshed manually each Monday during the application phase"). Same trigger cadence, same human-in-loop, same outputs — plus lineage, gating, and monitoring.

| Step | Today (v6.2) | After M6 (v6.3) |
|---|---|---|
| Trigger | Manual, Monday | Manual, Monday: `make cloud-refresh` (one command) |
| Snapshot pull | Local script → local parquet | Local script → upload to `s3://…/raw/` (stays out of user sessions, per §13) |
| Features + train | Local `make train` | SageMaker Pipeline: validate → features → **training job** (ml.m5.large, ~3–6 min) |
| Quality gate | Human eyeball | **Automated evaluate-gate step**: re-runs the §7 DM check vs. similar-day naïve + coverage sanity; pipeline **halts registration on failure** (the CP-2/CP-3 logic, now a machine-enforced condition) |
| Register | DagsHub MLflow (manual) | Both registries; SageMaker package `PendingManualApproval` → Yarden approves (human-in-loop preserved) |
| Forecast + lookup | Local precompute | **Batch Transform / pipeline step** emits next-day forecast + slider-lookup grid + static-page HTML to `s3://…/lookups/` |
| Monitoring | None (v6.2 §13 boundary) | **Drift Processing job**: PSI on headline features + price distribution vs. training baseline, data-quality counts (nulls, bin integrity), forecast sanity (quantile monotonicity) → CloudWatch metrics + alarm → email |
| Publish | Commit snapshot to Space | Pull artifacts from S3 → review → commit to Space + Pages (unchanged human step) |

Total cloud compute per refresh: **~10–15 minutes of small-instance time ≈ $0.03–0.06.** The pipeline is triggered manually by design — an EventBridge schedule would cost nothing but is deliberately OFF to preserve the ratified human-in-loop refresh and the "no scheduled retraining" boundary (§11, §13-amended). This also keeps the model-staleness disclosure (v6.2 §9.3) truthful: the *champion* stays frozen at its training cutoff unless Yarden explicitly approves a newly gated candidate.

---

## 4. Component specification

Each component: purpose → concrete configuration → steady-state cost → the evidence artifact it yields.

**4.1 Account, IAM, security.** Root MFA; one IAM admin user (console) + one CLI role; `SageMakerExecutionRole` least-privilege: S3 scoped to the project bucket's prefixes, `cloudwatch:PutMetricData`, ECR pull, logs — no wildcards. Credentials never in the repo (`aws configure` local profile; HF/GitHub secrets not needed — Plane A has no AWS access by design). Cost-allocation tag `project=delu` on every resource. Cost $0. *Evidence:* `infra/iam/*.json` committed; the least-privilege policy is itself an interview artifact.
**4.2 S3.** One bucket `delu-forecast-prod-<suffix>`, prefixes `raw/ features/ models/ lookups/ monitoring/`; versioning on; lifecycle: expire noncurrent versions > 90 days, `raw/` > 180 days. Working set ≈ 2–5 GB → **$0.06–0.13/month**. *Evidence:* bucket layout in the architecture diagram.
**4.3 ECR.** One image, multi-stage (reuses the v6.2 Dockerfile discipline): training + serving in the same pinned environment as local (`uv.lock` is the single source of truth — the reproducibility story extends to the cloud unchanged). ~1–1.5 GB → **$0.10–0.15/month**.
**4.4 Training job.** `ml.m5.large` ($0.115/h us-east-1; ~$0.13/h eu-central-1), billed per-second, ~3–6 min/run, ~4–5 runs/month → **$0.05–0.10/month**. Spot pricing evaluated and **rejected** (saves cents, adds interruption-handling complexity — a micro-optimization with negative ROI at this scale; noted because saying "no" to it is itself a defensible judgment). **Parity gate:** the SageMaker-trained champion must match the local-trained champion on the same snapshot + seeds — mean pinball loss within 0.1% relative, prediction max-abs-diff within float tolerance — asserted by `tests/test_cloud_parity.py`. Guards silent env drift between laptop and cloud.
**4.5 Model Registry.** Package group `delu-forecast`; each version carries git SHA, snapshot SHA-256, eval metrics, approval status. **Free.** *Evidence:* registry lineage screenshot (static PNG).
**4.6 SageMaker Pipeline.** The §3 DAG via the Pipelines SDK; the evaluate-gate is a `ConditionStep` on the DM statistic + coverage sanity. Orchestration **free**; underlying steps as itemized. *Evidence:* DAG screenshot — the single best "I've done MLOps" image in the portfolio.
**4.7 Inference — three modes, one policy.** (a) **Batch Transform** (the product path): emits the forecast + lookup grid; scales to zero; ~$0.02–0.05/run. (b) **Serverless endpoint** (the proof): 2048 MB, max-concurrency 2; invoked by `scripts/invoke_endpoint.py` and a monthly manual smoke test; at owner-only traffic **< $0.20/month**, $0 idle; cold start 1–3 s, owner-facing only. (Pricing-source note from the research memo: official AWS text bills serverless as compute-ms + data only; two credible trackers add $0.20/1k requests — immaterial either way at this traffic; re-check at arc start.) (c) **Interview real-time demo**: `make endpoint-up` → demo → `make endpoint-down`; ml.t3.medium/m5.large ≈ **$0.06–0.12 per session-hour**; the script's exit path *is* the teardown, and `endpoint-up` refuses to run if an endpoint already exists. **Forbidden:** any endpoint outliving its script; autoscaling min > 0; any keep-alive.
**4.8 Monitoring (custom; D5).** Weekly Processing job (same container, ml.m5.large, ~3–5 min): computes drift PSI on `residual_load_deviation_from_normal`, `scarcity_stress`, and the price distribution vs. the frozen training baseline; data-quality counts (nulls, 4-of-4 quarter-hour bin integrity — extending the §9.4 invariant into operations); forecast sanity (zero quantile crossings). Publishes 8 custom CloudWatch metrics (within the 10-metric free tier) + **2 alarms** (PSI breach; pipeline-failure) → SNS email. Cost **≈ $0.02–0.05/run + $0 CloudWatch**. *Evidence:* the drift dashboard PNG, refreshed into the static page — a monitoring screenshot almost no DS portfolio has. Model Monitor / Clarify are unavailable to new accounts (closed 2026-07-30) and would not be chosen anyway — see interview Q2 (§9).
**4.9 Cost guardrails (mandatory, day 1 of AWS-1).** AWS Budgets: $10 alert, $50 alarm → email + SNS. `make aws-audit`: lists any running endpoints/instances/notebooks and non-zero-cost resources; **must return clean at the close of every AWS work session** and is a CP-6 gate. No SageMaker Studio kept running — SDK-first from the laptop; Studio opened only when needed and shut down (the "zombie notebook" trap from the research memo, engineered out). Monthly bill screenshot archived to `docs/aws-bills/` — the FinOps paper trail is itself an interview asset.

---

## 5. (folded into §4 — numbering preserved for cross-references from CP-6)
*Sections 4.1–4.9 above are the component spec; CP-6 references them as §5.x equivalents where the draft circulated — final v6.3 merge will renumber cleanly.*

---

## 6. Cost model and budget amendment

**Steady-state month (post-free-tier, eu-central-1, FX ₪3.02/$ from the research memo — re-check at spend time):**

| Line item | USD/mo | Notes |
|---|---|---|
| S3 (2–5 GB, lifecycle-managed) | 0.06–0.13 | |
| ECR (one image) | 0.10–0.15 | |
| Training jobs (4–5 × ~5 min) | 0.05–0.10 | per-second billing |
| Batch forecast + drift jobs (8–10 × ~4 min) | 0.05–0.10 | |
| Serverless endpoint (owner-only invocations) | < 0.20 | $0 idle |
| CloudWatch + SNS + Budgets | 0.00–0.50 | within free allowances at this volume |
| Data egress (artifact pulls) | 0.00 | first 100 GB/mo free |
| **Steady-state total** | **≈ $1.2–3.0** | **≈ ₪4–9** |
| Interview-heavy month (+6 real-time demo sessions) | + ~0.70 | still < $4 |
| **Ratified expected ceiling (D4)** | **≤ $5.00** | ≈ ₪15 |

**Failure-mode economics (why the guardrails are sized as they are):** the worst realistic mistake — an ml.m5.large endpoint forgotten after an interview — burns ≈ $2.8–3.1/day. The $10 Budgets alert fires within ~3 days, the $50 alarm long before month-end, and `make aws-audit` at session close catches it same-day. The $65 policy ceiling is therefore protected by three independent layers before it is ever approached. **Free-tier discipline (R-7):** the AWS *account*, IAM, S3, and Budgets may be created early (they don't start the SageMaker clock); the **first SageMaker resource is created on AWS-1 day 1 and not before**, so the 2-month window blankets the build.

---

## 7. Milestone M6 and checkpoint CP-6

**Placement:** post-G5, program Month 6. **Effort: ~55–75 h total** (research memo full-pipeline range 43–86 h, tightened for this profile: Docker/Linux/FastAPI transfer directly; first-time IAM and the Pipelines SDK are the two real learning curves; +3–5 h for the D7 static export).

**AWS-1 — Cloud core (~30–40 h).** Account + IAM + S3 + ECR + Budgets/audit tooling (§4.1–4.3, 4.9); container adapted to the SageMaker contract; training job green; **parity test passing**; both registries holding the champion; serverless endpoint live + invoke script; batch-forecast path emitting a lookup consumed by an actual Space rebuild; teardown scripts.
**AWS-2 — Pipeline, monitoring, evidence (~25–35 h).** Pipelines DAG with the evaluate-gate `ConditionStep`; approval flow; drift Processing job + CloudWatch metrics/alarms (alarm fired once deliberately to prove the wire); marimo static export + GitHub Pages live (D7); evidence pack (architecture SVG, DAG/registry/dashboard PNGs, first bill PNG); README + static-page architecture section; interview one-pager (§9).

**CP-6 checklist (outcome-level):**
- [ ] 1. IAM least-privilege roles committed (`infra/iam/`); no wildcard actions; no credentials anywhere in either repo's history.
- [ ] 2. Training job reproduces the local champion — parity test green (pinball Δ < 0.1% rel., prediction max-abs-diff < 1e-6).
- [ ] 3. `make cloud-refresh` executes the full DAG end-to-end: validate → features → train → evaluate-gate → register → batch-forecast → drift-metrics, one command, unattended.
- [ ] 4. Champion registered in **both** registries; SHA-256 identity asserted; SageMaker package approved via the manual-approval flow.
- [ ] 5. Evaluate-gate demonstrated **both ways**: passes on the real snapshot; halts registration on a deliberately corrupted one.
- [ ] 6. Serverless endpoint returns a correct, monotone 9-quantile forecast via `invoke_endpoint.py`; idle cost verified $0 on the bill.
- [ ] 7. Drift job publishes all 8 metrics; both alarms tested by forced breach; email received.
- [ ] 8. Budgets $10/$50 live (test-fired); `project=delu` tag on every resource; `make aws-audit` returns **clean** at arc close.
- [ ] 9. One full post-build calendar month's bill **≤ $5**, screenshot archived in `docs/aws-bills/`.
- [ ] 10. Interview demo script: cold `make endpoint-up` → live scored request → `make endpoint-down` in **< 10 min**, teardown verified by the audit script.
- [ ] 11. **Static page live on GitHub Pages**: full reading order + architecture section; **loads < 3 s** on a cold cache from an independent connection; contains **zero** runtime JS calls to AWS or HF.
- [ ] 12. **Plane-A purity gate:** `grep`-gate proves no `boto3`/`sagemaker`/AWS-SDK reference in the deployed Space bundle; CP-5's load checks **re-pass** on the live Space URL post-integration (warm < 5 s, cold ≤ 30 s, sliders lookup-only).
- [ ] 13. CV / LinkedIn / README updated: static page becomes the primary portfolio URL; Space and MLflow linked beneath it with honest labels (uses the ratified post-M5 CV slot — no new slot consumed).
- [ ] 14. Interview one-pager committed: the §9 Q&A set + the architecture diagram on one page.

---

## 8. Sequencing, envelope impact, and the ratification cascade

**Recommended (D8):** G5 closes ~mid/late-Jan 2027 exactly as ratified (the AWS arc does **not** touch the flagship's pre-G5 critical path — inserting it earlier would delay the deployed showcase, the worst possible trade). **Month 6 (≈ Feb):** M6 at ~12–15 h/wk alongside active applications (~5–8 h/wk) → CP-6 closes ~end-Feb/early-Mar. **Months 7–8 (≈ Mar–Apr):** companion FM0–FM5 as specified in its v1.0 doc, unchanged in content; **G6 → ~late-Apr 2027.** B-Man3 (Kaggle account) shifts from "Month 5" to the Month-6→7 seam; a new **B-Man-AWS** (account + IAM + Budgets, **no SageMaker resource**) lands at AWS-1 day 1. Program envelope ~680 h → **~740 h**.
**Why AWS before the companion:** it reuses red-hot flagship context (same model, same container discipline, same data); it injects the strongest CV delta ("productionized on AWS, < $5/month") into the funnel at its earliest live month; and the companion — whose market story is classification breadth, not infrastructure — loses nothing by shipping eight weeks later, inside an already-active funnel.
**Alternative considered and rejected:** running M6 and the companion in parallel across Months 6–7 (≈ 25–30 h/wk on top of interviews) — rejected as an overload risk exactly when interview performance matters most. It remains available as an owner override if the funnel is quiet in February.
**Ratification cascade (fires only on "yes"):** (1) capstone v6.2 → v6.3 per §11; (2) progress.md — anchors (doc version, envelope dates, budget line), Track B position, Notes; (3) **stage map v4 → v5 rebuild becomes owed** — per the standing rule it runs only on your explicit request, which ratifying D8 constitutes; FM rows shift one month, M6/CP-6/B-Man-AWS rows added; (4) the companion doc itself needs **no edit** (its content is month-agnostic; scheduling lives in the orchestrator layer); (5) `orchestrator-role.md` envelope sentence — owner-edited, flagged here for you to amend.

---

## 9. Interview surface added (the point of the whole arc)

| Component | Question it arms |
|---|---|
| Serverless + batch, no warm endpoint | "Walk me through your deployment. Why serverless?" → *"At portfolio traffic an always-on ml.m5.large is ~$84/month for zero benefit; serverless is ~$0.20 and scales to zero. I priced both and chose with the bill in hand — I'd invert the choice around ~800 K invocations/month or a hard sub-second latency SLA."* |
| Custom drift job → CloudWatch | "How do you monitor a model in production?" → *"PSI on the headline features and the target distribution against a frozen training baseline, plus data-quality invariants, published as CloudWatch metrics with alarms. I built it from primitives — SageMaker's managed monitor closed to new customers in mid-2026, and rolling my own cost a Processing job and taught me exactly what the managed service abstracts."* |
| Two-plane architecture | "Why doesn't your demo call the endpoint live?" → *"Because a recruiter's first impression shouldn't depend on a cold start. The demo serves precomputed artifacts instantly; the endpoint exists to prove serving capability and is invoked on demand. Decoupling the evidence from the runtime is the design decision."* |
| Evaluate-gate ConditionStep | "How do you stop a bad model reaching production?" → *"The pipeline re-runs the same Diebold–Mariano gate and coverage sanity my offline checkpoints use; registration halts on failure, and promotion still requires my manual approval. Statistical gate + human gate."* |
| Parity test | "How do you know cloud training matches local?" → *"A committed test asserts the cloud-trained champion matches the laptop-trained one on identical data and seeds. Environment drift is a bug class you test for, not hope about."* |
| IAM + no-secrets repo | "How do you handle security?" → *"Least-privilege execution role, prefix-scoped S3, no wildcards, credentials never in git, and the showcase plane has no AWS access at all — the blast radius of a compromised demo is zero."* |
| The bill trail | "Biggest constraint you engineered around?" → *"A $65 ceiling I beat by 20×: the whole backbone runs at $1–3 a month, with budget alarms and an audit script as the guardrails. Cost is a first-class requirement, not an afterthought."* |
| eu-central-1 | (color) *"The model runs in Frankfurt — same place the market it forecasts clears."* |

---

## 10. Risk register additions (v6.3 §11, continuing R-1…R-5)

**R-6 — Cost leak (forgotten endpoint / zombie notebook).** *Likelihood* Med, *Impact* Med ($3/day class). **Mitigations:** D3 forbids persistence; teardown lives inside the demo script; `make aws-audit` gated at every session close (CP-6 item 8); Budgets $10/$50; tag-scoped cost explorer. **Trigger:** any Budgets email → same-day audit.
**R-7 — Free-tier clock misfire.** Creating a SageMaker resource early burns the 2-month window before the build. **Mitigation:** hard rule — no SageMaker resource before AWS-1 day 1 (account/IAM/S3/Budgets are safe). **Trigger:** none; it's a sequencing rule.
**R-8 — AWS service/pricing drift.** Model Monitor's closure proves managed services move under you; prices shift. **Mitigations:** custom monitoring is already the design (D5); mandatory 10-min pricing re-verification at AWS-1 day 1; serverless per-request ambiguity pre-noted (immaterial at scale). **Trigger:** any line item re-verifying > 2× the §6 estimate → pause, re-cost, re-confirm D4 before building on.
**R-9 — Plane-A regression (the upgrade becomes the downgrade).** AWS code or assets leak into the recruiter path and slow it. **Mitigations:** CP-6 items 11–12 (grep-gate + CP-5 re-checks + static-page load gate); evidence images size-budgeted (< ~500 KB total additions). **Trigger:** any measured load regression → the AWS-facing change reverts, not the showcase.
**R-10 — Enterprise-MLOps scope creep.** The arc expands into Terraform/CDK, multi-env, Kubernetes, streaming, real-time retraining. **Mitigations:** hard boundary — plain SDK (`boto3`/`sagemaker`) + committed JSON policies; **no IaC framework** (a new §13 boundary, defended: *"Terraform proves platform-engineering fluency; this project proves DS-owned productionization — for a single-dev, single-region, five-resource stack, an IaC framework is ceremony"*); no new AWS service beyond the named set without orchestrator adjudication. **Trigger:** > 75 h elapsed or any unlisted service proposed → stop, ship AWS-1 scope as the deliverable, carry the residual up. **Owner:** learner.

---

## 11. Exact amendment map — capstone v6.2 → v6.3

| v6.2 location | Amendment |
|---|---|
| §1 constraints list (line-item bullets) | Add sixth bullet: the lean AWS backbone (two-plane invariant, scale-to-zero policy, ≤ $5/mo). Amend "Total hosting cost: $0" → "$0 showcase hosting + ≤ $5/month AWS backbone (measured target $1–3)". |
| §1 audience sentence | "cloud-backed experiment tracking" gains "…and a lean AWS production backbone (SageMaker pipeline, registry, serverless serving, custom drift monitoring)". |
| §9 (new **§9.5 — AWS Production Backbone**) | Insert §§2–4 + §6 of this spec essentially verbatim (architecture, components, refresh flow, cost model, guardrails). |
| §9.2 sleep/keep-alive paragraph | Rewrite: the GH-Actions ping **option is deleted** (was already distrusted); the Space keeps its ≤ 30 s cold disclaimer; the **static page (D7) becomes the primary URL** and absorbs the first-touch guarantee. |
| §9.2 lookup provenance sentence | Note the lookup/snapshot are now *produced by the cloud pipeline* and still *bundled statically* — the serving pattern is unchanged. |
| §9.3 reproducibility | Add: the ECR image is built from the same `uv.lock`; the parity test extends reproducibility across environments; bill screenshots archived. |
| §10 reading order | Insert item **(11b) "Production architecture"**: the diagram + three evidence figures + one paragraph — static, no slider (mirrors the §10 (3b) spectral pattern exactly). Item (12) adds the static-page URL as the canonical entry point. |
| §10.1 stranger test | Unchanged in substance; the reviewers now *start* at the static page. Add the < 3 s static-load check alongside it. |
| §11 risk register | Append R-6…R-10 (§10 of this spec). |
| §12 milestones | Append **M6 (AWS-1/AWS-2) + CP-6** (§7 of this spec) after M5; amend the Post-CP-5 companion pointer's timing sentence to the D8 sequencing (pointer discipline itself unchanged). |
| §13 boundary "No enterprise production pipeline or live trading layer" | **Rewritten** (the one substantive boundary change): *"**Lean cloud backbone, not enterprise MLOps.** The project ships a real train→register→deploy→monitor pipeline on SageMaker — serverless, gated, monitored, ≤ $5/month — because productionization is a capability worth proving. It still deliberately excludes scheduled retraining (the weekly trigger is human), live per-visitor inference, rollback machinery, multi-environment promotion, and IaC frameworks: the 20% of MLOps that demonstrates DS-owned production judgment, without the 80% that is platform boilerplate for a single-developer portfolio."* All neighboring §13 boundaries (no trading layer, no DVC, no live per-visitor pulls) **stand verbatim**. |
| §13 (new boundary) | Add: **"No Terraform/CDK, no multi-env, no Kubernetes"** with the R-10 defense. |
| **Unchanged invariants (asserted, not assumed)** | Marimo mandate + three-slider set + OOD flags; precomputed-lookup serving; HF Spaces free tier; DagsHub MLflow as the public registry; committed CC BY snapshot + attribution; no live API pulls in user sessions; single LightGBM + CQR + isotonic-last; walk-forward CV + embargo + pinned folds; DM gates; §9.4 invariant tests + thin CI; stranger-test gate; $65 ceiling; M3/16 GB; every §0 ratified decision. |

**Non-capstone cascade:** progress.md (anchors, Track B, Notes — regenerates on ratification), stage map v4 → v5 (owed on your explicit go), `orchestrator-role.md` envelope sentence (owner edit), CV slot usage per CP-6 item 13.

---

## 12. Ratification checklist (what "yes" means)

Reply approving **D1–D8** (or vetoing specific items) ratifies this spec as the **v6.3 amendment**. Partial ratification is legitimate — e.g., D1–D7 with a different D8 sequencing. On ratification the cascade in §8 fires, starting with the progress.md amendment and your go/no-go on the map rebuild. Until then this file is a flagged, unratified draft under the version-precedence rule.

## Caveats

Prices are official mid-2026 list rates (research memo, 2026-07); the eu-central-1 premium is estimated at 5–15% and re-verified at arc start (R-8). FX ₪3.02/$ is a July-2026 spot rate. Hour estimates are planning figures with the same "completeness over speed" status as every other estimate in the program. The serverless per-request-fee source conflict is documented and immaterial at this traffic. marimo's `export html` static fidelity for the full reading order is asserted from its documented export capability; if any §10 element degrades in static export, the fallback is a purpose-built static page from the same figures — same cost ($0), same gates, ~2 h delta.

*End of AWS Extension Spec v1.0 — DRAFT pending ratification.*
