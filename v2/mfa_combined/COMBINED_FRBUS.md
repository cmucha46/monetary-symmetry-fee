# Combined FRB/US Study — Monetary Symmetry Fee v2 + Medicare for America (H.R.10924) under a Spending Closure

**Project:** Monetary Symmetry Fee v2 · **Lane:** 2 (FRB/US combined runs) · **Date:** 2026-11-22
**Design:** Design E throughout (`INTERFACE_ASSESSMENT.md` is binding): wedges only on `rme`/`rcar`/`rbbb` as exogenised level paths scaled by origination κ (loan-only κ, Lane B's documented lower bound; κ_rbbb = 0.757); `rg*` never wedged; fee receipts only via imposed `ugfsrp`; closure `dfpex=1, dfpdbt=0, dfpsrp=0` in every run; `rff` never imposed (inertial Taylor rule, `dmpintay=1`); f = rff by whole-path fixed-point iteration; MCE (`mcap+wp`) headline, VAR robustness; horizon 2027Q1–2036Q4; fee effective 2027Q4. Fee-only results are Lane B's (`regime_outputs/paths_C_b100_*.csv`, `metrics.json`) — **reused, not re-solved**.
**Spending closure:** the combined runs impose the Regime C (or B) fee *and* the MFA flows simultaneously. All fee receipts enter the same non-recycling surplus ledger that MFA draws on; nothing is re-spent by the fiscal rule.
**Script:** `v2/frbus/combined_runs.py` · **Outputs:** `v2/frbus/combined_outputs/` (path CSVs, `metrics.json`, `run_log.json`, `mfa_annual_central.csv`, `mfa_annual_high.csv`).

---

## 1. MFA fiscal paths used (central scenario, FY2028–36)

From `mfa/mfa_model.py` + `mfa/data/annual_detail.csv`: gross cost $24.92T; displaced federal outlays $13.09T; premiums $1.93T; employer contributions $1.27T; Title II $6.11T; residual **+$2.52T**.

**Title II verification (required check):** `mfa_model.py` carries Title II only as window totals by component. Summing the central components (TCJA repeal 3.90 + payroll 1.15 + NIIT 0.47 + surtax 0.30 + step-up 0.17 + excise/HSA 0.12) reproduces **$6.11T exactly**, and the derived annual path (allocated across FY28–36 in proportion to baseline FY nominal GDP, the only annualisation the source supports) sums to $6,110B; the implied residual is $2,523B ≈ $2.52T. High case: Title II $7,310B, residual $10,730B — both exact. No discrepancy beyond rounding; no flag raised.

**Quarterly convention:** FY t = (t−1)Q4..tQ3, so FY2028 begins 2027Q4 — the fee's effective date. Annual $B are spread evenly over the FY's four quarters (quarterly SAAR value = annual $B). The single quarter 2036Q4 belongs to FY2037 (outside the window); it carries the FY2036 flow values, which is Lane B's own fallback convention in `cohort_receipts` — FY28–36 sums are unaffected.

## 2. MFA entry map — how each flow enters FRB/US

FRB/US has **no health variable at all** (verified by name and definition search over all 933 variables in the installed `model.xml`: no variable's definition mentions health, medical, or hospital). Every route below is therefore a carrier choice, stated with its justification.

| # | MFA flow (FY28–36, central) | FRB/US route | Sign & scaling | Justification |
|---|---|---|---|---|
| 1 | Incremental federal health outlays = gross − displaced federal = **+$11,832B** | **`egfe` exogenised at baseline level + flow**, flow converted to 2012$ by the baseline implied federal-purchases deflator (`egfen`/`egfe`, quarter by quarter) | + (raises federal purchases, GDP, and `gfexpn`; surplus falls through the model's own accounts) | `egfe` (federal purchases) is the model's only exogenous final-demand carrier for government-financed services. Exogenised *level* path, per the Lane D/Lane B discipline (never a constant add-factor). Caveat: in the NIPA, Medicare/Medicaid services are recorded in PCE financed by transfers; FRB/US cannot express that split, and the purchases route treats the full incremental outlay as domestic final demand (no import/health-supply leakage beyond the model's generic `egfe` multipliers). |
| 2 | Enrollee premiums (§2204) = **$1,932B** receipts | **`ugfsrp` imposed path — MFA-receipts component**, separately identified from the fee component in the imposing code and in every output CSV (`mfa_receipts_bn_saar` vs `fee_receipts_bn_saar`) | + receipts/`xgdpn` (baseline) added to baseline `ugfsrp` | Premiums are offsetting receipts; FRB/US has no offsetting-receipts variable. `ugfsrp` is the only clean receipts entry (Interface §2.2). One-ledger rule kept: premiums are MFA's own receipts — baseline Medicare premiums are already netted inside the displaced-outlays figure, so nothing is counted twice. |
| 3 | Employer contributions (§125) = **$1,266B** receipts | **`ugfsrp` — same MFA-receipts component** (reported as its own annual line in `mfa_annual_central.csv`) | + receipts/`xgdpn` | A payroll-based federal receipt with no dedicated carrier. The employer labour-cost / incidence side has no channel in FRB/US (no employer health-cost variable) — see §3. |
| 4 | Title II revenues = **$6,110B** (TCJA/P.L.119-21 repeal, payroll add-on, NIIT, surtax, step-up repeal, excises/HSA) | **`ugfsrp` — same MFA-receipts component** | + receipts/`xgdpn` | The bundle spans personal, payroll, investment, corporate (via TCJA repeal) and excise bases; no single rate carrier exists. `trptx` covers only the personal average rate, and Interface §2.2 expressly rules out entering revenue via `tpn`/`tcin` (the `trp` equation's output-gap term would contaminate the experiment). Residual routing is the documented least-bad alternative, with the composition caveat in §3: **the receipts side is demand-neutral in this routing** — no household disposable-income or labour-supply response to Title II is modelled, which flatters the combined run's demand offset (§4 caveat). |
| 5 | Displaced **private** premium spending (households/employers stop paying private premiums) — a demand-composition flow, not a federal one. Central estimate: $0 in FY28–30 (exchange-cohort gross is fully absorbed by displaced PTC in those years), rising to **$207B/yr by FY2036** (cumulative ≈ $0.72T) | **`eco_aerr` growth-shift path** moving real PCE (nondurables + non-housing services, the FRB/US category that contains health services) to baseline − displaced private spending, deflated by the baseline GDP deflator | − on `eco` level, imposed as quarter-by-quarter log-growth add-factors computed from the target path | Amount = (exchange-cohort gross cost − PTC) + 25% employee share of ESI-cohort gross cost, cohort gross rebuilt from `mfa_model` enrollment and cost structure. The add-factor (not exogenised-level) form is deliberate: it shifts the composition of consumption while preserving `eco`'s endogenous response to income — the channel through which freed-up household cash is re-spent. Employer premium savings (the other ~75% of the ESI cohort) have **no carrier** (they would appear as profits / lower labour costs; FRB/US has neither margin) and are not represented. |

**Separately identified, always:** imposed `ugfsrp` = baseline + (fee receipts + MFA receipts)/`xgdpn`, with the two components stored as distinct output columns and distinct annual lines. Fee receipts in combined runs come from Lane B's cohort model re-evaluated at the *combined* run's own iterated fee path.

## 3. What cannot be represented (and the approximation used, if any)

1. **Health-sector supply / capacity** (workforce, HCBS labour, provider capacity constraints behind MFA's induced-demand factor): no sectoral supply block exists. *Approximation:* none — the full incremental outlay is treated as effective final demand from the quarter it is imposed; any capacity-driven price or queue response is outside the model.
2. **Premium incidence detail** (§2204 income-bracket premium schedule; who bears employer contributions): no distributional or labour-cost channel. *Approximation:* premiums and employer contributions enter as lump-sum residual receipts (flow 2–3 above).
3. **Title II behavioural/incidence effects** (TCJA repeal and payroll/NIIT/surtax effects on labour supply, saving, capital income): not modelled under the `ugfsrp` route. *Approximation:* none — receipts are demand-neutral in-model. This is the single largest caveat on the combined demand results.
4. **LTSS as a distinct entitlement** (the widest swing in the MFA build, $0.7–5.1T): inside FRB/US it is indistinguishable from any other federal purchase. *Approximation:* it is simply part of flow 1's `egfe` path (and of the high-stress sensitivity's larger path).
5. **The §IX distributional channel** (interest-income redistribution — the fee memo's core hypothesis): untestable in FRB/US (Interface §4.5), unchanged by adding MFA.
6. **Displaced state Medicaid spending / state MOE** ($0 in-window in the bill as written): no state fiscal sector; nothing imposed, correctly per the bill.
7. **Employer premium savings** (~75% of displaced ESI premiums): no profits/labour-cost carrier; omitted (flow 5 covers only the household-paid share). Direction: understates the private cash-flow relief of MFA.
8. **Fed remittances / IORB expense**: absent from FRB/US by construction (Interface §4.2); all fiscal figures here are Treasury-side, exactly as in Lane B.

## 4. Headline results (MCE, β = 1.0, post-sync = 2030Q1–2036Q4 mean)

| Run | Post rff level (%) | Post fee f (%) | Fee receipts FY28–36 ($B) | Δ surplus cum. FY28–36 ($B) | Δ debt held by public, 2036Q4 ($B) | Unempl. dev. 2036Q4 (pp) | GDP trough dev. (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Baseline (A plain) | 3.29 | — | — | 0 | 0 | 0.00 | — |
| Fee-only C (Lane B) | 2.10 | 2.10 | 3,809 | +3,715 | −3,896 | **+0.77** | −1.72 |
| MFA-only | 5.62 | — | — | −1,242 | +1,428 | −2.11 | −0.04 |
| **Combined C + MFA** | **3.70** | **3.70** | **6,628** | **+5,153** | **−5,313** | **−0.61** | −0.41 |
| Combined B + MFA (sens.) | 3.61 | 3.61 | 6,658 | +5,200 | −5,366 | −0.61 | −0.77 |
| Combined C + MFA, VAR | 3.52 | 3.52 | 6,295 | +4,679 | −4,812 | −0.52 | −0.57 |
| Combined C + MFA high-stress (sens.) | 4.61 | 4.61 | 8,221 | −1,514 | +1,823 | −1.44 | −0.02 |

**Answers to the headline questions.**

- **Does the MFA demand impulse lift the rule's path, and therefore f and receipts? Yes — decisively.** MFA-only drives the inertial Taylor rule **+2.33pp** above baseline (post mean; funds level 5.62% vs 3.29%), because $11.8T of incremental purchases enter demand while the offsetting receipts are demand-neutral residual entries. In the combined run the f = rff fixed point therefore re-solves at a much higher level: post-sync **rff = f = 3.70%**, vs 2.10% fee-only — the combined funds path sits **+0.41pp above the conventional baseline**, not below it. Cumulative fee receipts rise to **$6,628B vs $3,809B fee-only: Δreceipts = +$2,819B (+74%)**. (VAR: fee 3.52%, receipts $6,295B vs $4,340B fee-only VAR, Δ = +$1,956B.)
- **Does the spending closure shrink the fee's employment drag? In-model, it more than offsets it at the horizon.** Unemployment deviation at 2036Q4: **combined −0.61pp vs fee-only +0.77pp** — and in the combined MCE run the unemployment deviation never exceeds +0.01pp at any quarter (max +0.006), against a fee-only path that builds to +0.77pp. The GDP trough deviation shrinks from −1.72% (fee-only) to −0.41% (combined). **Caveat (load-bearing):** this offset is measured under the §3.3 approximation — Title II's $6.11T and the premiums enter as demand-neutral residual receipts, so the model sees MFA's spending in full but none of its tax-side drag. A run that routed Title II through `trptx` would show a smaller offset; the interface assessment rules that route out for contamination reasons, so the honest statement is: *the spending closure eliminates the fee's measured employment drag in FRB/US under residual-receipts routing, with the tax-incidence channel unmodelled and working in the opposite direction.*
- **Fiscal paths.** Cumulative Δsurplus FY28–36: baseline 0; fee-only **+$3,715B**; MFA-only **−$1,242B** (the static +$2,523B residual cost is overwhelmed in-model by **+$3,547B of extra federal interest** on the rule's higher funds path — the model's own `gfintn`, one ledger); combined **+$5,153B**. The combined figure exceeds the sum of its parts (+$2,473B) by **+$2,680B of interaction**, almost all of it the enlarged fee take at the MFA-lifted funds path (+$2,819B) net of interest differences. Debt held by public at 2036Q4 (Δ vs baseline): fee-only −$3,896B; MFA-only +$1,428B; combined **−$5,313B**.
- **Combined-run fiscal drag decomposition** (style of `v2/integration/frbus_feedback.py`, extended for the separately imposed outlays): Δsurplus (+5,153) = fee receipts (+6,628) + MFA receipts (+9,308) − incremental MFA outlays (−11,832) − Δinterest (+192 saving) + **endogenous drag +856**. The residual drag term is *positive* here — endogenous revenues net of cyclical outlays add to the surplus — because the combined economy runs at or above baseline employment throughout, the opposite sign from the fee-only run's drag. (Fee-only C drag on the same formula: Δsurplus 3,715 − receipts 3,809 + Δinterest −2,310 → the fee-only endogenous drag including interest is deeply negative; the interest saving is the fee regime's second fiscal engine, and in the combined run it nearly vanishes — Δinterest cum. only −$192B — because the combined funds path is *above* baseline, not below.)
- **Regime B sensitivity:** as in Lane B, sync speed is not the binding margin — Combined B ≈ Combined C on every headline (fee 3.61% vs 3.70%; Δsurplus +$5,200B vs +$5,153B).
- **High-stress sensitivity (residual +$10.73T):** even with the fee lifted to 4.61% and receipts of $8,221B, the combined run's cumulative Δsurplus is **−$1,514B** and debt is **+$1,823B** above baseline at 2036Q4 — the high-stress MFA case is **not** financed in-model either, consistent with the MFA v1 accounting verdict. (Its unemployment deviation, −1.44pp, reflects the same demand-neutral-receipts caveat at larger scale.)

## 5. Solve status — every run

| Run | Mode | Status | Fixed-point iterations | Post-sync max \|f − rff\| |
|---|---|---|---|---|
| MFA-only (central) | MCE | ✅ solves | — (no fee) | — |
| MFA-only (central) | VAR | ✅ solves | — | — |
| Combined C + MFA | MCE | ✅ solves | 8 | 0.002pp |
| Combined C + MFA | VAR | ✅ solves | 6 | 0.001pp |
| Combined B + MFA | MCE | ✅ solves | 8 | 0.003pp |
| Combined C + MFA high-stress | MCE | ✅ solves | 8 | 0.003pp |

No solver failures, no fixed-point failures; error log empty (`combined_outputs/run_log.json`). Total wall time ≈ 2 × 2.1 min for the two executions of the suite (the second after the §1 boundary-quarter convention was aligned with Lane B's). One implementation note: the combined fixed point converges more slowly than Lane B's fee-only iteration (8 vs 4–7 iterations) because MFA lifts the funds path far from the initial half-baseline guess; the iteration remains a contraction throughout (histories in `run_log.json`).

## 6. Files

- `v2/frbus/combined_runs.py` — run script (entry map implemented as documented in §2).
- `v2/frbus/combined_outputs/paths_{MFAonly,COMB_C,COMB_B,COMB_C_high}_{mce,var}.csv` — levels (`L_*`), deviations vs matched baseline (`D_*`), fee path and **separately identified** `fee_receipts_bn_saar` / `mfa_receipts_bn_saar` / `mfa_incr_outlays_bn_saar` / `mfa_displaced_private_bn_saar`.
- `v2/frbus/combined_outputs/metrics.json` — every figure in §4.
- `v2/frbus/combined_outputs/mfa_annual_{central,high}.csv` — annual MFA flows as imposed (incremental outlays, premiums, employer, Title II, displaced private, receipts, residual).
- `v2/frbus/combined_outputs/run_log.json` — iteration histories, residuals, Title II/residual verification totals, (empty) error log.

*All figures are FRB/US simulations under the stated protocol and the stated MFA entry map — not Fed, CBO, JCT or CMS estimates. The MFA fiscal paths are a modeller's construction (see `mfa/RESULTS_MFA_V1.md`); the fee paths are Lane B's loan-only lower bound on the unified base.*
