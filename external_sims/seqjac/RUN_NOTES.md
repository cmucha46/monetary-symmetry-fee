# Sequence-Jacobian HANK check of the §IX channel — RUN NOTES

**Honest frame (required):** *Linearized (first-order) MIT-shock comparison in a textbook
one-asset HANK (Y=1, lump-sum ∝-skill taxes, fixed debt stock, no banks/IORB/credit sector).
A sign-and-mechanism check of the §IX ordering, not a score of any policy magnitude.*

## Environment / install

- Python 3.12.3, fresh venv (`venv/` in this directory).
- `pip install sequence-jacobian` installs the wheel **with no declared dependencies**
  (Requires: empty); `numpy scipy numba` were installed separately. **No pins were needed** —
  the modern stack works. Exact freeze (`pip_freeze.txt`):
  - sequence-jacobian 1.0.0, numpy 2.5.5, scipy 1.18.1, numba 0.68.1, llvmlite 0.50.0
- Repo cloned at tag v1.0.0 into `repo/`; `repo/notebooks/hank.ipynb` is the source of truth.
- **Implementation gotcha worth recording:** sequence-jacobian infers block output names by
  regex-parsing the literal `return ...` line of each function. One-line returns such as
  `return div - tax` therefore corrupt the DAG (first attempt failed with `KeyError: 'we'`).
  All helper functions here use the notebook's named-assignment style (`T = div - tax; return T`).
- Full script (`run_hank.py`) runs end-to-end in ~50 s at the shipped grid **nA = 500**, T = 300
  quarters. No grid reduction was needed.

## Steady state (shipped calibration, reproduced)

Calibration (notebook): eis 0.5, frisch 0.5, rho_e 0.966, sd_e 0.5, nE 7, amin 0, amax 150,
nA 500, Y = Z = 1, pi 0, mu 1.2, kappa 0.1, rstar 0.005, phi 1.5, B 5.6.
Solved (solver `hybr`, unknowns beta, vphi; targets asset_mkt, labor_mkt):

| quantity | value |
|---|---|
| **beta (calibrated)** | **0.982244** |
| vphi (calibrated) | 0.786433 |
| r = rstar | 0.005 |
| C | 1.000000 |
| Y | 1.0 |
| A = B | 5.6 (asset_mkt residual −9.8e-15) |
| w | 0.833333 (= Z/mu) |
| Tax = r·B | 0.028 |
| Div | 0.166667 |
| labor_mkt residual | −6.7e-16 |
| goods_mkt (untargeted) | −5.3e-9 |

### MPC distribution (from the steady-state consumption policy)

MPC = ∂c/∂(cash-on-hand) at each (skill, lagged-asset) state (a lump-sum transfer shifts
cash-on-hand 1:1), distribution-weighted by the steady-state distribution D.

- **Aggregate (D-weighted) MPC ≈ 0.118**
- **Hand-to-mouth share (mass at a₋₁ = 0): ≈ 17.4 %**
- By population asset quintile:

| quintile | a up to | mean MPC | wealth share |
|---|---|---|---|
| Q1 (poorest) | 0.053 | **0.479** | 0.01 % |
| Q2 | 1.04 | 0.052 | 1.5 % |
| Q3 | 3.84 | 0.026 | 8.3 % |
| Q4 | 9.66 | 0.018 | 22.8 % |
| Q5 (richest) | 150 | **0.014** | 67.4 % |

- By skill row (D-weighted MPC): 0.443, 0.385, 0.257, 0.030, 0.017, 0.013, 0.011
  (lowest → highest skill). The MPC gradient the §IX mechanism needs is present and steep:
  bottom-quintile MPC ≈ 35× top-quintile MPC, and interest income (∝ assets) accrues
  overwhelmingly to the low-MPC top (67 % of wealth in Q5).

## Experiment construction (adaptation — NOT a shipped experiment)

The shipped notebook has only `rstar` and `Z` shocks; the fiscal contrast is an adaptation,
built as follows (also documented in `run_hank.py` comments). Common gross flow in every run:
**X_t = 0.01 · 0.8^t** (initially 1 % of steady-state Y per quarter), horizon T = 300,
present value at the steady-state rate **PV = Σ X_t/(1.005)^t = 0.049024**.

- **Run A — interest-financed (baseline shipped structure).** `Tax = r·B` charged ∝ skill
  (shipped `transfers` rule); bondholders receive the interest through (1+r)·a₋₁, i.e. ∝ assets.
  Implemented as an `rstar` shock path (amplitude 0.004598, decay 0.8), scaled ex post — exact
  in the linearized model — so the **realized PV of the interest flow Σ dr_t·B/(1+r)^t equals
  0.049024**, identical to B/C. Net aggregate household transfer = 0.
- **Run B — transfer-recycled (tax-financed).** Variant fiscal block `Tax = r·B + GTAX` with
  two added exogenous sequences: `GTAX = X_t` (same shipped ∝-skill tax rule — the *same tax
  side as A*) and `GTR = X_t` paid **flat** (equal per household; T_add(e) = GTR for every
  skill state) via the `transfers` hetinput. Net aggregate household transfer = 0, exactly as
  in A. **B − A is therefore the pure redistribution contrast** (only recipient incidence
  differs: flat vs ∝ assets).
- **Run C — pure recycling (auxiliary decomposition).** `GTR = X_t`, `GTAX = 0`: the same flat
  payout as B, financed *outside* the household sector (the fee-on-the-financial-sector case
  of the actual proposal; this model has no bank sector, so that charge has no household
  counterpart). **C − B is the recycling (aggregate-injection) term.**

Validation: cumulative ΔY − ΔC ≈ 0 in runs A (≈ +3e-6) and B (≈ −2e-7) — goods market clears.
In run C, cumulative ΔY − ΔC = −0.050 ≈ −PV by construction: the injection is an outside-sector
transfer with no goods counterpart inside the model, and its ΔY < 0 is the endogenous-labor
income effect (transfers → less labor supply → lower NE = L = Y), not a coding error.

## Results (linearized GE: endogenous w, pi, Taylor rule phi = 1.5)

Deviations from steady state; C and Y in levels (steady state = 1). Peak = largest quarterly deviation.

| run | peak ΔC | cum. ΔC (Σ₃₀₀) | disc. cum. ΔC | peak ΔY | cum. ΔY (Σ₃₀₀) | peak |Δpi| / |Δr| |
|---|---|---|---|---|---|---|---|
| **A** interest (∝ assets) | −0.004132 (trough) | **−0.015456** | −0.015265 | −0.004132 (trough) | **−0.015453** | 56.1 bp / 56.4 bp |
| **B** flat transfer, tax-financed | +0.000340 | **+0.001411** | +0.001379 | +0.000340 | **+0.001411** | 3.7 bp / 3.7 bp |
| **C** flat transfer, unfinanced | +0.003210 | **+0.018675** | +0.018330 | −0.006920 (trough) | **−0.031324** | 19.4 bp / 19.5 bp |

Decomposition (cumulative ΔC): redistribution **B − A = +0.016866**; recycling **C − B = +0.017264**;
ratio recycling / |redistribution| = **1.02**. (Cumulative ΔY: B − A = +0.016864; C − B = **−0.032735**.)
Level comparison at the same payout: cum. ΔC in C is **13.2×** that in B (peak ΔC 9.4×) —
i.e. ∝-skill tax financing removes ~92 % of the flat transfer's consumption effect.

## Verdict on the §IX claim

1. **Sign/ordering — SURVIVES GE.** At equal present-value charge and with the *same* tax side,
   the interest-incidence run is **contractionary** (cum. ΔC = ΔY ≈ −0.0155) and the
   transfer-recycled run is **expansionary** (cum. ΔC = ΔY ≈ +0.0014). B > A on both C and Y,
   with endogenous wages, inflation and the Taylor rule active. The recycled run is only
   *mildly* expansionary — consistent with "contractionary-to-neutral vs expansionary" being
   an ordering statement, not a promise of a large B.
2. **"Recycling ≫ redistribution" — does NOT cleanly survive; it is metric-dependent.**
   - On cumulative ΔC the two terms are essentially **equal** (ratio 1.02), not ≫.
   - On peak ΔC and on the C-vs-B level ratio (13.2× cumulative), the recycling margin looks
     much larger — tax financing does destroy most of the transfer's effect.
   - On cumulative ΔY the recycling increment is **negative** (−0.0327): in this
     endogenous-labor HANK, an unfinanced flat transfer *lowers* output via the labor-supply
     income effect even as it raises consumption. Any "recycling ≫" claim for *output* fails
     in this model; for *consumption* it is ~1:1 cumulatively.
3. **Caveat on Run A:** implementing the interest channel through `rstar` bundles two things —
   (i) recipient-MPC redistribution toward wealthy asset holders (the §IX mechanism proper)
   and (ii) the real-rate/Taylor tightening that a higher r mechanically is in this model
   (peak Δr 56 bp in A vs 4 bp in B). A's contraction is therefore an upper bound on the pure
   incidence effect; the B − A contrast should be read with that bundle in mind. (There is no
   asset-incidence transfer channel in this framework other than r: the `transfers` hetinput
   is indexed by skill only, not by assets.)

## Artifacts (this directory)

- `run_hank.py` — full runnable script (baseline replication + adaptation, commented).
- `results.json` — steady state, MPC distribution, all headline numbers, decomposition.
- `irf_A_interest_asset_incidence.npz`, `irf_B_transfer_flat_taxfinanced.npz`,
  `irf_C_transfer_flat_unfinanced_recycling.npz` — full IRF paths (C, Y, pi, r, w), 300 quarters.
- `ss_arrays.npz` — steady-state distribution D, policies c/a, grids, MPC array.
- `pip_freeze.txt` — exact installed versions. `repo/` — upstream v1.0.0 clone.
