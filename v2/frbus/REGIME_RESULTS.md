# FRB/US Regime Results — Monetary Symmetry Fee v2 (Design E)

**Project:** Monetary Symmetry Fee v2 (memo of 2026-11-22) · **Date:** 2026-11-22 · **Lane:** FRB/US integration
**Companion documents:** `INTERFACE_ASSESSMENT.md` (protocol — followed throughout), cohort lane `../cohort/DATA.md` and `../cohort/outputs/` (κ and receipts inputs). **Scripts:** `regime_runs.py` (main suite), `fix_d_mce.py` (Regime D MCE correction), `diag_shock.py` (shock diagnostic), `analyze.py` (metrics). **Outputs:** `regime_outputs/paths_*.csv` (30 files), `regime_outputs/metrics.json`, `regime_outputs/run_log.json`.

**Window:** 2027Q1–2036Q4, official Oct 2026 LONGBASE, official `model.xml`. **Effective date:** 2027Q4 (Oct 1, 2027, per the cohort lane). **Headline expectations:** MCE (`mcap+wp`); VAR reported as robustness throughout. **Every run** — baselines included — sets the non-recycling fiscal closure `dfpex=1, dfpdbt=0, dfpsrp=0`.

> **Sponsor decision of 2026-11-22 (bonds in the base) — status of these runs.** The fee base is now loans + corporate bonds + municipal bonds (Treasuries excluded), grandfathered identically. The cohort lane's unified-base outputs had **not landed** when this suite was executed, so per instruction these runs use the **loan-only κ and loan-only receipts as the documented lower bound**: κ = 1.0 from the effective date for `rme` and `rcar` (all new mortgage/consumer originations are covered under either base); κ for `rbbb` = covered business-**loan** origination flow ÷ total business-credit origination flow = **0.757** (bond turnover δ = 0.09 assumed, ~11-yr average maturity; derivation in `regime_runs.py`). A κ_rbbb = 1.0 sensitivity — the unified-base wedge value — is run for Regimes B and C at β = 1.0 (§5). **Direction of the pending correction:** the unified base enlarges the wedge coverage on business credit (κ_rbbb 0.757 → 1.0: deeper `rff` offset, somewhat larger macro deviation, slightly *lower* fee level via the fixed point) and enlarges receipts through a larger covered stock (cohort layer; not yet quantified). The in-model receipts used here are therefore a lower bound on the base effect and an upper bound on the rate effect; the two do not cancel in any way this suite can certify. Municipal-bond coverage affects receipts only (FRB/US has no muni rate — assessment §4.9).

---

## 1. Headline results (MCE, β = 1.0, loan-only κ)

Deviations are fee regime minus **matched** baseline (same expectations mode; for D and E, the same shock). "Post" = mean over 2030Q1–2036Q4. Fiscal sums are FY2028–FY2036.

| | **B: fast sync** | **C: 24-mo sync** | **D: C + inflation shock** | **E: C + recession shock** |
|---|---|---|---|---|
| Funds rate offset, post (pp) | **−1.28** | **−1.19** | **−1.25** | −0.36 (min −0.75) |
| Synchronized fee level, post (%) | 2.02 | 2.10 | 1.99 | 0.93 |
| Share of fee offset by the rule | 63% | 57% | 63% | 39% |
| Fee receipts fed in ($B, loan-only) | 3,832 | 3,809 | 3,880 | 1,945 |
| Δ federal surplus, cum. ($B) | **+3,781** | **+3,715** | **+3,765** | **+1,444** |
| Δ federal interest, cum. ($B) | −2,560 | −2,310 | −2,557 | −581 |
| Δ debt held by public, 2036Q4 ($B) | −3,966 | −3,896 | −3,957 | −1,563 |
| Real GDP deviation, trough (%) | −1.77 | −1.72 | −1.88 | −1.19 |
| Unemployment deviation, max (pp) | +0.77 | +0.77 | +0.86 | +0.60 |
| Core PCE inflation dev., max abs post (pp) | 0.28 | 0.26 | 0.27 | 0.12 |
| Inflation dev. at 2036Q4 (pp) | −0.02 | −0.02 | −0.02 | −0.01 |
| Unemployment dev. at 2036Q4 (pp) | **+0.77** | **+0.77** | +0.86 | +0.60 |

**The one-paragraph verdict.** Under Design E — the model's own inertial Taylor rule reacting to outcomes, never told about the fee — synchronization is *absorbable* in every regime, including under both shocks: no solve fails, inflation returns to the baseline path (deviation ≈ −0.02pp by 2036Q4), and the rule autonomously finds a funds path 1.2–1.3pp lower (post-sync mean, β = 1). But the offset is **partial, not complete**: the rule retires only ~57–63% of the fee, covered lending rates sit above the conventional baseline by the full imposed wedge, and the economy runs persistently cooler — unemployment is still +0.77pp above baseline at the end of the window in Regimes B and C. In this model the 50/50 configuration is therefore **not** shown to be equivalent to conventional policy at the same mandate outcomes; it is shown to be a *feasible* configuration that buys a large fiscal dividend (≈ +$3.7–3.8T of cumulative surplus improvement over FY2028–36, in-model, loan-only receipts) at the price of a persistently somewhat tighter effective stance on covered credit. §7 states precisely where the model's design — not the policy — binds that conclusion.

## 2. How the fee was imposed (protocol compliance)

- **Wedges** on `rme`, `rcar`, `rbbb` only, as exogenised **level** paths (matched-baseline level + wedge). `rg5/rg10/rg30` never wedged; their decline is the in-model interest-saving channel. `rccd` never wedged (inherits `rcar` by identity).
- **Wedge** = β · f_t · κ_{c,t}, with κ keyed to **origination** coverage (assessment §1.3): κ = 1.0 from 2027Q4 for mortgages and consumer credit; κ_rbbb = 0.757 loan-only (above). Revenue keys off **stock** coverage via the cohort model — the two κ's are not conflated.
- **Receipts** enter only via an exogenised `ugfsrp` path (matched-baseline + receipts/`xgdpn` from the cohort model, floating design, central turnover, at the run's own iterated fee path). `gfrecn` never touched.
- **Synchronization fixed point.** Post-transition the statute sets f_t = rff_t, but the wedge depends on f while the rule-produced `rff` depends on the wedge. Resolved by whole-path fixed-point iteration (solve → rebuild f from the produced `rff` path with the regime's ramp → re-derive cohort receipts → re-solve), documented here because the brief required the choice stated: whole-path iteration was preferred over lagged-rff because the statute binds contemporaneously and the iteration is a contraction (measured slope ≈ 0.1–0.3). Convergence: 4–7 iterations per run; final post-sync residual |f − rff| ≤ **0.006pp** in every run. Initial guess (ramp toward half the baseline funds path) affects only iteration count.
- **Ramps.** B: fee 0.15% at 2027Q4, half-gap at 2028Q1, f = rff from **2028Q2**. C: linear gap closure over 8 quarters, f = rff from **2029Q4**. D and E are built on C (the statutory-maximum transition — the harder test under stress; the choice is documented here per the brief's "B or C" latitude).
- **One ledger.** All fiscal results are read from the model's own `gfsrpn`/`gfdbtnp`/`gfintn`. Treasury interest is never recomputed externally. The remittance term is absent from FRB/US by construction (assessment §4.2) and is **not** in these numbers — it belongs to the SFC layer.

## 3. Regime A — the control

Regime A is the LONGBASE baseline under the non-recycling closure, solved per expectations mode and per shock state (six baseline files: `paths_A_{plain,infl,rec}_{mce,var}.csv`). The unshocked baseline reproduces the LONGBASE data path exactly (tracking-residual discipline; max deviation 0.0 on the window in the probe). Baseline funds path: 4.15% (2027Q1) gliding to ≈3.21% (2036); core PCE inflation 2.74% → 1.98%; unemployment ≈4.1–4.2%. All fee-regime deviations below are measured against the matched A.

## 4. Regimes B and C — synchronization speed is not the binding margin

**Funds path.** The rule finds a lower path on its own in both regimes. Post-sync mean offset (MCE, β = 1): **B −1.28pp, C −1.19pp**; deepest offsets −1.36/−1.31pp. The synchronized pair settles at rff ≈ f ≈ **2.0–2.1%** against a conventional ≈3.3%. Under VAR the offsets are smaller (−0.94/−0.90pp) — backward-looking expectations mute the anticipated-permanence channel, exactly as the assessment predicted when it reversed v1's expectations practice.

**Transition cost: B ≈ C.** Peak transition-window inflation deviation (MCE, β = 1): B 0.28pp, C 0.26pp. GDP trough deviation: B −1.77%, C −1.72%. Unemployment at 2036Q4: +0.77pp in both. Completing synchronization in ~2 quarters instead of 8 costs essentially nothing measurable in this model, and cumulative receipts are nearly identical (B $3,832B vs C $3,809B) because C's slower ramp leaves `rff` — and hence the synchronized fee itself — slightly higher. **Answer to the memo's synchronization experiment, within this model's limits: the Board could synchronize early; the macro cost of the regime is a level effect of the permanent wedge, not a ramp effect.** The caveat is §7.2: the financial-stability and credit-supply risks of a fast ramp are outside FRB/US entirely, so "absorbable" is a statement about the model's demand/inflation dynamics only.

**Borrower costs (memo Q4, in-model part).** By construction of the protocol, covered new-loan rates deviate from baseline by the imposed wedge: post-sync mean **+2.02pp on `rme` and `rcar`, +1.53pp on `rbbb`** (κ = 0.757) at β = 1, MCE, Regime B. The memo's combined charge p = i + f exceeds the conventional funds rate by **+0.74pp** on post-sync average (B, β = 1) — because the rule offsets only 63% of the fee, the 50/50 pair does **not** reproduce the conventional stance in the model's own accounting; it is tighter. Two protocol facts must accompany these numbers wherever they are cited: (i) the lending-rate deviations are *imposed* (baseline + wedge), so the endogenous decline of the Treasury curve (rg10 −0.23pp post-sync mean) does **not** additionally relieve covered rates in these runs — the protocol is conservative for the equivalence question, maximising measured borrower burden (assessment §1.2); (ii) uncovered rates do get the curve relief (`req` via `rg30`, and the federal borrowing rate), so the *relative* price of covered vs uncovered credit rises by roughly the full wedge — the in-model shadow of the substitution margin the model cannot itself execute (assessment §4.6).

**Persistence.** Inflation returns (deviation −0.02pp by 2036Q4, mildly negative — ≈ −0.2 to −0.3pp — through the middle years), but unemployment does not: the deviation builds through the transition and is still at its maximum (+0.77pp) at the window's end, with real GDP −1.77% at trough (2036Q4 in the MCE path — a slow level effect, still drifting at the horizon, driven by shallower capital accumulation under permanently higher covered-credit costs). This asymmetry — prices re-anchor, quantities do not fully — is the model's central anti-equivalence evidence under Design E, and §7.1 explains how much of it is the rule's design rather than the policy's.

## 5. Pass-through grid and the κ sensitivity

Post-sync means, MCE (VAR in parentheses), Regime B / C:

| β | rff offset B (pp) | rff offset C (pp) | Fee level B (%) | Receipts B ($B) | Δ surplus B ($B) |
|---|---|---|---|---|---|
| 1.00 | −1.28 (−0.94) | −1.19 (−0.90) | 2.02 (2.35) | 3,832 (4,435) | +3,781 (+4,318) |
| 0.75 | −1.05 (−0.76) | −0.98 (−0.72) | 2.24 (2.53) | 4,217 (4,744) | +4,261 (+4,751) |
| 0.50 | −0.78 (−0.56) | −0.72 (−0.52) | 2.51 (2.73) | 4,696 (5,103) | +4,873 (+5,269) |

**The β paradox, stated carefully.** Lower pass-through produces a *higher* synchronized fee and *higher* revenue. This is not an error: it is the f = rff fixed point. With β small, the wedge restrains less, the rule offsets less, `rff` stays closer to the conventional path — and since the fee is chained to `rff`, the fee itself is larger. At β = 0.5 the regime is, in substance, conventional policy at a slightly lower rate with a large fee riding on it; at β = 1.0 it is the genuine 50/50 split of restraint. Revenue comparisons across β are therefore **not** comparisons of the same policy at different efficiencies, and no β should be chosen for its revenue. β remains **uncalibrated** (assessment §1.3); the grid is the honest presentation.

**κ_rbbb sensitivity** (β = 1, MCE): moving κ_rbbb from 0.757 (loan-only) to 1.0 (unified-base wedge) deepens the B offset to −1.36pp, raises the GDP trough deviation to −2.01%, and *lowers* receipts slightly ($3,689B vs $3,832B) through the lower fixed-point fee — the wedge-side preview of the sponsor's base broadening. The receipts-side effect (larger covered stock) arrives with the cohort lane's unified outputs and is expected to dominate; these runs do not quantify it.

## 6. Regimes D and E — synchronization under stress

**Shock designs (documented, identical within each expectations mode).**
- **D (inflationary):** add-factor `picxfe_aerr` = **+2.0pp for 2028Q1–2028Q4** under VAR. Under MCE the same input is unusable — see §8 — and was rescaled to **+0.33** so the *realised* shock matches: peak core-inflation deviation **+4.37pp (MCE) vs +4.46pp (VAR)**; shocked-baseline funds peak deviation +2.60/+2.15pp; GDP trough −2.03%/−1.73%. A one-year burst that takes core inflation to ≈6.5–7% — a 2022-class event, arriving in the middle of the transition.
- **E (recessionary):** financial-conditions shock — `reqp_aerr` = **+3.0pp** and `rbbbp_aerr` = **+1.0pp**, 2028Q1–2028Q4, both modes (no amplification pathology on these channels). Realised shocked baseline: GDP trough **−4.25% (MCE) / −4.55% (VAR)**, unemployment peak deviation +2.05/+2.28pp — a genuine recession, likewise mid-transition.

**Regime D findings.** Synchronization on the full 24-month schedule proceeds through the inflation burst without instability: deviations of the fee regime from the *shocked conventional* baseline are the same order as in the no-shock Regime C (funds offset −1.25pp post; GDP trough deviation −1.88%; unemployment max deviation +0.86pp; post-sync inflation deviation ≤0.27pp, −0.02 by 2036Q4). The fee is at its largest exactly during the fight — **4.28% at 2029Q4** — because it is chained to the shock-elevated funds rate, and the rule retires the usual ~63% of it. In-model, the regime neither amplifies nor cushions the inflation shock relative to conventional policy; it replicates conventional stabilisation at a lower funds path and collects the fee on the way through (receipts $3,880B; Δ surplus vs shocked baseline +$3,765B).

**Regime E findings.** The recession drives the funds rate to its floor region in both the shocked baseline (min 0.125%) and the fee regime (≈0.11–0.13% at the 2030 trough) — and because f = rff, **the fee collapses with it, to ≈0.11% at 2030Q4**. Two consequences, both structural properties of the 50/50 design rather than artefacts: (i) the regime's restraint automatically vanishes in a downturn — a built-in stabiliser that conventional-plus-fixed-levy designs do not have; (ii) fee revenue is strongly procyclical — cumulative receipts fall to **$1,945B** (vs $3,809B in no-shock C) and the cumulative surplus gain to **+$1,444B**. Any fiscal plan that spends the fee must be sized to the recession-state revenue, not the mean. The fee regime's macro deviations from the shocked baseline are the smallest of any regime (GDP trough deviation −1.19%, unemployment max +0.60pp) precisely because the wedge is smallest when the economy is weakest. Synchronization *completes* during the recession (f reaches rff by 2029Q4 at ≈1.06%) — trivially, because there is almost nothing left to synchronize to.

## 7. Findings vs artefacts — where Design E binds

**7.1 The rule's inertia (the big one).** Design E's rule reacts to realised output and inflation gaps with lags and smoothing; it cannot see the fee. The assessment (§3.2) warned this *understates* the offset a real FOMC would deliver if it targeted the combined stance p = i + f directly — the behaviour the memo §II.C/§V expects. The measured offsets (57–63% of the fee at β = 1 under MCE; 38–40% under VAR) are therefore **lower bounds** on the offset, and the persistent unemployment deviation (+0.77pp at 2036Q4) is an **upper bound** on the regime's steady-state employment cost. The opposite bound — a stance-targeting rule that offsets the wedge one-for-one — would show near-equivalence by construction and prove nothing. The defensible statement is the interval between the two, and this suite measures the conservative end of it. What the interval's width means practically: the equivalence question cannot be settled by FRB/US alone; it turns on how the FOMC would actually formulate its reaction function under the statute — an institutional question, not an estimated parameter.

**7.2 What is not in these runs at all.** Per assessment §4, none of the following is represented, and no number here speaks to it: the reserve drain/TGA mechanics; Fed earnings, remittances, and the deferred asset (the fiscal figures are Treasury-side only — the consolidated figure awaits the SFC layer, and the remittance term will *reduce* the net gain relative to these numbers when IORB expense falls by less than Fed earnings); lender margins, credit supply and rationing; the lender-borne adjustable-fee design (§II.D fork — no channel exists); offshore/untaxed substitution (only the κ haircut); debt-supply effects on term premia; and the distribution of interest income by holder — the memo §IX hypothesis, which FRB/US can bound but not test.

**7.3 Smaller artefacts, disclosed.** (i) `rg10` deviations fade toward zero at the window's end (−0.02pp at 2036Q4 vs −0.37pp at 2029Q4 in Regime B) because post-window expectations in the stacked MCE solve anchor to LONGBASE data — a finite-horizon effect; the post-sync *mean* (−0.23pp) is the citable figure. (ii) Receipts are allocated evenly across each fiscal year's quarters and scaled by *baseline* `xgdpn` (deviations <1% make the ratio error negligible). (iii) The cohort receipts use FY-average fee rates; within-year ramp/stock timing differences are second-order (cohort DATA.md §5). (iv) `rff` is the model's single policy rate and stands in for IORB throughout (assessment §4.1); the 2026 funds–IORB spread (≈2bp) is ignored.

## 8. The one failure encountered — and its correction

The original MCE inflation shock (`picxfe_aerr` +2.0) **failed as a design**: it produced a realised peak inflation deviation of **+26.9pp**, a funds deviation of +16.2pp, and a GDP trough of −11.3% — a de-anchoring explosion, not a stress test. Diagnosis (`diag_shock.py`): under `mcap+wp`, the add-factor's realised effect is **linear and ≈13.4× the input, with a one-quarter lead** (+0.5 → +6.6pp peak; +1.0 → +13.3pp) — the fork's model-consistent wage-price block treats the residual in a way this lane measured but did not fully trace internally, and reports as an empirical input-output property of the installed package. Under VAR the identical input behaves conventionally (peak +4.46pp). Correction (`fix_d_mce.py`): the MCE add-factor was rescaled to +0.33 to match the VAR shock's *realised* severity (+4.37pp peak); the MCE shocked baseline and both MCE Regime D runs were recomputed and their CSVs overwritten; the correction is recorded in `run_log.json`. All other runs are as originally executed. No solver (Newton) failures occurred anywhere in the suite (30 headline solves — 6 baselines and 24 fee configurations — plus every fixed-point iteration solve behind them); every fee run's fixed-point iteration converged (residuals in `run_log.json`).

## 9. Solve status — every run

| Run set | Mode | β / κ | Status | Fixed-point iterations |
|---|---|---|---|---|
| A plain / infl / rec baselines | MCE + VAR | — | ✅ all solve; plain reproduces LONGBASE exactly | — |
| B fast sync | MCE + VAR | β = 1.0 / 0.75 / 0.5, κ loan-only | ✅ | 4–7 |
| B fast sync, κ_rbbb = 1.0 | MCE + VAR | β = 1.0 | ✅ | 6–7 |
| C 24-mo sync | MCE + VAR | β = 1.0 / 0.75 / 0.5, κ loan-only | ✅ | 4–7 |
| C 24-mo sync, κ_rbbb = 1.0 | MCE + VAR | β = 1.0 | ✅ | 6–7 |
| D = C + inflation shock | MCE + VAR | β = 1.0 / 0.75 | ✅ (MCE after §8 correction) | 5–7 |
| E = C + recession shock | MCE + VAR | β = 1.0 / 0.75 | ✅ | 4–5 |

Post-sync fixed-point residual |f − rff|: ≤ 0.006pp in all 24 fee configurations. Total wall time ≈ 8.5 min (suite) + ≈ 3 min (D correction).

## 10. Files

- `regime_outputs/paths_A_{plain,infl,rec}_{mce,var}.csv` — Regime A controls (levels; deviations vs self are zero by construction).
- `regime_outputs/paths_{B,C,D,E}_b{100,075,050}[_k1]_{mce,var}.csv` — levels (`L_*`), deviations vs matched baseline (`D_*`; `D_xgdp_pct` in %), the imposed fee path (`fee_f_pct`) and receipts (`receipts_bn_saar`).
- `regime_outputs/metrics.json` — every figure cited above, per run.
- `regime_outputs/run_log.json` — κ derivation inputs, iteration histories, residuals, shock-size diagnostics, the §8 correction record, and the (empty) error log.
- Scripts: `regime_runs.py`, `fix_d_mce.py`, `diag_shock.py`, `analyze.py`, `probe.py` (environment/API probe).

*All figures are FRB/US simulations under the stated protocol — not Fed or CBO forecasts, and not estimates of the unified-base design, whose cohort inputs are pending (see the sponsor-decision note at the head of this report).*
