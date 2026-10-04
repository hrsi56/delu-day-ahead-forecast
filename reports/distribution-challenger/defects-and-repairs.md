# CP-23 — defects, repairs and rulings

Everything here is disclosed; nothing changed a frozen setting after an outcome was seen.

## Owner rulings requested before repository work

**1. The brief omitted the PUBLISH_RULES hash.** `capstone_v21.md` §21.9 pins "PUBLISH_RULES 1.3, at
the hash the issued brief records". The issued brief (SHA-256 `33f6b412…502d0c`) records none.

- **Why there was only one candidate.** Revision 1.3 has had a single identity since `940eb98`:
  `5a660864f8b82943174741320c71087a3d0508f707edeb997cb2c1395c1c73b4`. That is the hash CP-22's brief
  pinned, and it is unchanged on `main`.
- **Ruling (Owner, 2026-10-04):** "Pin 5a660864… and go". The brief stays byte-identical. The pin is in
  `src/cp23/inputs.py`, the protocol's `owner_rulings` and the packet.

**2. §21.3's `uv.lock` pin conflicted with CP-10's committed evidence and with green CI.** §21.3 asks
for PyTorch "pinned in `uv.lock` as a test-only dependency". The root `uv.lock`'s SHA-256
(`5d2aecc3…465a94`) is bound into CP-10's lineage and CP-15's protocol.

- **The probe.** A throwaway worktree at `cb9ba29`, with `uv.lock` changed by one byte, ran the full
  suite. The only test it broke was `tests/test_26_cp10_evidence.py::test_provenance_inputs_sources_and_v1_replay`.
  (`test_22` needs the browser payload, which CI builds first.) Item 14 requires green CI, and §21.11
  gives no write path to that test. The probe worktree was removed.
- **Ruling (Owner, 2026-10-04):** "Separate test-only lock". PyTorch 2.14.1 is pinned and hash-locked in
  its own uv project, `tests/cp23/torch-reference/` (`pyproject.toml` and `uv.lock`, non-default group
  `torch-reference`).
- **What stays unchanged.** The root `pyproject.toml` and `uv.lock` are byte-identical. Every
  historical identity holds, and CP-21's and CP-22's identity code runs unchanged.

## Repairs after a job ran

**3. `daily-cycle.json` cited v4's component cycle as `null`.** The first run read CP-21's
`daily-cycle.json` under a key that schema does not have (`summary`; CP-21 writes
`total_cold_cycle_seconds`).

- **Repair:** `job daily-cycle --beside-only` rewrote only that field from CP-21's committed file. No DDNN
  fit was repeated and no checked value changed.
- **Record:** the ledger event `daily_cycle_beside_repair` and the `repairs` entry in `daily-cycle.json`.

## Design notes (not defects)

**4. The daily cycle refits no LightGBM or LEAR component.** §21.8 caps DDNN member fits only and has no
allowance for other fits. So v5's cold cycle measures the DDNN members, the ensemble, v5's central from
v4's identity-verified cached members, the H layer and issuance. v4's own component cycle is CP-21's
committed measurement, shown beside it.

**5. The independent HG and v4 slice refits A1_w/B2_w and L-N/L-R at two origins.** §21.10 item 6
requires it, as CP-22's §20.10 item 2 did.

- **Where it is charged.** To the ledger's reproduction counters (`component_attempts_reproduction`,
  `lasso_fits_reproduction`, `lgbm_fits_reproduction`), through `cp23.controls.ReproductionCharges`.
- **Why no cap applies.** §21.8 sets no cap for them. They are recorded and inside the machine-hour
  ceiling.

**6. Synthetic fixture fits are not DDNN member fits.** The unit and path tests train networks on
synthetic arrays only (`tests/cp23/`). Following CP-22's practice, they are fixtures, not member fits
on research data, so they are outside the 6,000-fit count. Every fit on research data is charged.

**7. The PyTorch reference ran once and passed.** It passed 26 of 26 checks at the tolerances
committed before it (`cd56434`), with every error at machine precision. No tolerance was ever changed.

**8. Pre-freeze changes.**

- **The PIT diagnostic's member parameters.** Before the protocol froze (`a008c47`), the per-origin cache
  was extended to store each member's Johnson SU parameters, which that diagnostic needs.
- **The column names of one diagnostic table.** The diagnostics module was corrected before its first
  run.
- **`src/cp23/ddnn.py`** is unchanged since its reference record.
