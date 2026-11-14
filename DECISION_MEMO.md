# DECISION MEMO — Monetary Symmetry Fee: Full Macroeconomic Simulation

**Project:** Monetary Symmetry Fee (MSF) + Medicare for America financing test
**Date:** 2026-11-13 · **Status:** Final deliverable, Lanes A–K consolidated
**Repo:** https://github.com/cmucha46/monetary-symmetry-fee
**Companion document:** `DIAL_ANALYSIS.md` (Lane K — the full dial-identification proof)

> **No number in this memo is an official CBO, JCT, CMS or Federal Reserve
> estimate.** No official score of H.R.10924 (Medicare for America) exists —
> CBO, JCT and CMS-OACT have never estimated any version of the bill (Lane C).
> FRB/US results are model results on an illustrative baseline (LONGBASE is
> not an FOMC or staff forecast). Monte Carlo ranges are conditional
> simulations under judgemental priors — prior mass, not calibrated
> probabilities or confidence intervals. Negative and contradictory results
> are reported alongside favourable ones, per the brief.

---

## 1. Executive verdict

### Q1 — Where would the Fed set the public-credit-capture dial s ∈ [50%, 90%]?

**NOT point-identified by the dual mandate.** This is a proved result of the
project, not a modelling failure (proof: `DIAL_ANALYSIS.md` §§1–3):

1. In the prior ChatGPT prototype the dial moved only through invented,
   sign-ambiguous priors (Lane A audit).
2. In FRB/US, at fixed all-in borrower cost the (π, u) loss ranks s
   *adversely and monotonically* — higher s is strictly less potent (§5
   below) — and once episodes are rescaled to equal macro effect the loss
   is equal across s *by construction*. Neither framing yields an interior
   optimum at 57%, 75%, or anywhere else.
3. The income-flow channel FRB/US omits (Lane H) flips the ranking with
   horizon and with Congress's use of the receipts — a ranking that flips
   on variables outside the mandate cannot identify a mandate-driven dial.

**Institutional forecast (the defensible substitute for a point estimate):**

| Fed behaviour | Plausibility | Fiscal consequence (MC v2, §2) |
|---|---|---|
| **(i) 50% floor — default and hold** through first policy episodes | **Most plausible** (Brainard attenuation under an unestimated β, reversibility, ZLB/easing option value, fiscal-appearance / independence protection) | Combined ≈ **$4.26T** mean; $6T fails (1.7% prior mass) |
| (ii) 50% start + gradual evidence-contingent drift upward | Plausible medium-run path; capped by equal-effect borrower-cost arithmetic (§5) | 10-yr total between the 50% and 75% rows, nearer the 50% row |
| (iii) Rule-based high share (75–90%) | **Implausible** without Congress legislating a fiscal or quasi-fiscal objective into the instrument; only fiscal rules select it | $6T survives (63–90% prior mass) — as a *policy-rule scenario*, not a forecast |

**Correction of the prototype's 57.1%:** 57.1% was the cross-path *mean* of
a bimodal distribution whose **median, mode and modal path are all the 50%
floor in every year 2029–36** (~66% of path-years exactly at 50%, ~9% at
90%; even the median of path-means, 54.3%, is an artefact of the floor
group's identity rotating across years). It is prior mass averaged over an
unidentified choice — not an estimate, a forecast, or an optimum — and
should not be quoted as where the Fed would set the dial.

### Q2 — Fee revenue, FY2027–36

Net fee receipts (after the 13% placeholder haircut for tax interactions /
admin; gross = net ÷ 0.87), β = 0.88, from the cohort + SFC module
(Lanes E/F/I):

| Dial s | Deterministic, central base (loans + securitised once) | Deterministic, strict loans-only base | MC v2 net fee: mean (p10–p90) | MC v2 gross fee: mean |
|---|---|---|---|---|
| 50% | **$3.25T** | $2.50T | $3.07T ($2.29–3.88T) | $3.53T |
| 75% | **$4.82T** | $3.71T | $4.59T ($3.36–5.88T) | $5.27T |
| 90% | **$5.76T** | $4.44T | $5.51T ($3.97–7.15T) | $6.33T |

**Net fee alone reaches $6T in essentially no draws at any dial**
(prior mass ≥ $6T: 0.0% at 50%, 8.3% at 75%, 32.1% at 90%).
The $6T hypothesis therefore *requires* the interest channel at every dial.
Revenue is phase-in-bound: grandfathering keeps the taxable book at ~78% of
the eligible book by 2036 (fixed point ~88%), so the 10-year take is
materially a ramp artefact (2028: $0.011T; 2036 at s=75%: $0.82T/yr).

### Q3 — Consolidated net interest decline, FY2027–36

Consolidated = interest on **public-held** debt only (interest on Fed-held
Treasuries nets against Fed income) + IORB/remittance effect, from the SFC
ledger with explicit 18%/yr Treasury repricing — **not** the prototype's
CBO-sensitivity plug-in (Lane A §4). β = 0.88:

| Dial s | Public-yield saving | IORB / remittance saving | **Consolidated total** | MC v2 mean (p10–p90) |
|---|---|---|---|---|
| 50% | $0.85T | $0.35T | **$1.20T** | $1.19T ($0.72–1.67T) |
| 75% | $1.34T | $0.55T | **$1.89T** | $1.88T ($1.15–2.64T) |
| 90% | $1.67T | $0.68T | **$2.35T** | $2.35T ($1.44–3.30T) |

- **No double counting:** the reserve drain is settlement timing (reserves →
  TGA on collection, reversed on spending) and is counted **zero** times as
  revenue; fee revenue is counted once; the Fed deferred-asset mechanism is
  modelled (baseline remittances are $0 in 2027–29 while the ~$0.20T+
  deferred asset pays down).
- **τ linearity — the load-bearing caveat:** the public-yield term is
  *exactly linear* in the yield-transmission placeholder τ = 0.32. At
  s = 75%: coupon saving is $0 at τ = 0, $1.34T at τ = 0.32, $4.19T at
  τ = 1. MC v2 sensitivity: **+$0.42T of combined total per +0.10 of τ**;
  at **τ = 0 the s=75% combined total falls to $5.37T and $6T fails at
  that dial too**. τ is estimated nowhere in this project.

### Combined fiscal benefit (Q2 + Q3)

| Dial s | Deterministic combined (central / strict base) | MC v2 mean | MC v2 median | p10–p90 | Prior mass ≥ $6T |
|---|---|---|---|---|---|
| 50% | $4.44T / $3.70T | $4.26T | $4.22T | $3.32–5.24T | **1.7%** |
| 75% | $6.71T / $5.60T | $6.47T | $6.40T | $4.99–8.03T | 63.2% (central base 74.1%, strict 31.9%, proxy 82.2%) |
| 90% | $8.12T / $6.79T | $7.86T | $7.76T | $6.01–9.84T | 90.1% |

### Medicare for America financing test (H.R.10924, Lane J construction)

Modeller's construction — **no CBO score exists** — FY2028–36, bill's own
terms (state MOE = $0; displacement phased per bill text: Medicare 2030/33,
Medicaid/CHIP 2033/35, exchanges 2033):

| MFA case | Gross cost | − Displaced | − Premiums | − Employer | − Title II (bill's own taxes) | − MOE (bill) | **= Residual for the fee** |
|---|---|---|---|---|---|---|---|
| Low | $18.09T | $12.57T | $1.35T | $0.51T | $4.96T | $0 | **−$1.29T** (bill over-covers; no fee needed) |
| Central | $24.92T | $13.09T | $1.93T | $1.27T | $6.11T | $0 | **+$2.52T** |
| High stress | $36.15T | $13.47T | $2.61T | $2.03T | $7.31T | $0 | **+$10.73T** |

Financing matrix (fee total − residual; deterministic fee cases):

| Residual case | s=50% central $4.44T | s=75% strict $5.60T | s=75% central $6.71T | s=90% central $8.12T |
|---|---|---|---|---|
| Low (−$1.29T) | +$5.73T ✓ | +$6.89T ✓ | +$8.00T ✓ | +$9.41T ✓ |
| **Central (+$2.52T)** | **+$1.92T ✓** | +$3.08T ✓ | +$4.19T ✓ | +$5.59T ✓ |
| High stress (+$10.73T) | −$6.29T ✗ | −$5.13T ✗ | −$4.02T ✗ | −$2.61T ✗ |
| High stress + accelerated-MOE amendment (residual +$7.67T) | −$3.23T ✗ | −$2.07T ✗ | −$0.96T ✗ | **+$0.45T ✓** |

- **Central case is financed at every dial** — including the forecast
  50% floor. **High-stress case is financed at no dial.**
- **Title II does more work than the fee.** In the central case the bill's
  own tax title contributes $6.11T against the residual — more than the fee
  at 50% or 75%-strict. Correct framing: the fee covers a *residual*; it
  does not "finance" the $24.9T gross cost of Medicare for America.
- **State MOE is $0 in FY2027–36 under the bill as written** (§2209 first
  payment year 2038). The +$3.07T "accelerated MOE" line above is a
  **project amendment to H.R.10924, labelled as such** — it is not in the
  bill, and even with it only s=90% central closes the high-stress case.
- **Indefinite appropriation:** the project's design (benefits financed by
  permanent indefinite appropriation, not capped by fee receipts) is also a
  **project modification** — H.R.10924 as introduced funds a unified Trust
  Fund (§2207) with further sums only *authorised* to be appropriated
  (Lane C §1.10). Both modifications are modelled as specified; neither is
  attributed to DeLauro's text.

### $6 TRILLION VERDICT

> **The $6T hypothesis FAILS at the forecast dial and survives only as a
> policy-rule scenario.**
>
> - At the institutionally forecast dial (50% floor, scenario (i)) the
>   combined benefit is **~$4.26T mean (median $4.22T, p90 $5.24T)** with
>   **1.7% prior mass ≥ $6T**. Under gradual drift (scenario (ii)) the
>   total lies between the 50% and 75% rows, nearer the 50% row — still
>   short.
> - $6T survives **only if the Fed chooses and sustains s ≥ 75%**
>   (63.2% prior mass at 75%; 90.1% at 90%) — a choice the dual mandate
>   does not compel on any channel decomposition this project produced.
> - **Conditions that must ALL hold for $6T:** (1) dial ≥ 75% sustained
>   for the full phase-in, not merely reached; (2) covered base at the
>   central (loans + securitised-once) definition or better — strict
>   loans-only cuts the 75% prior mass to 31.9%; (3) yield transmission
>   τ materially > 0 — at τ = 0, $6T fails even at 75% ($5.37T);
>   (4) the IORB stance path at or above the placeholder baseline (the
>   stance path is MC v2's #1 sensitivity — fee and interest terms move
>   together with it).
> - **Do not conflate the two verdicts:** "$6T fails at the forecast dial"
>   is TRUE. "Medicare for America is unfunded in the central case" is
>   **FALSE** — the central residual (+$2.52T) is covered even at the 50%
>   floor, with ~$1.9T to spare, because the bill's own Title II financing
>   carries the largest share. The $6T figure is the project's round-number
>   benchmark for the fee package, not the bill's financing requirement.

---

## 2. Evidence tiers — what supports what

| Tier | Contents |
|---|---|
| **Strongly supported by public models / primary sources** | FRB/US cross-validated: PolicyEngine `frbus` 0.1.0 and official PyFRB/US 1.1.1 agree to max diff **1.2×10⁻⁹** on the same Oct 2026 LONGBASE + byte-identical model.xml (Lane D). Cohort arithmetic: partition conserves principal, no double-assessment (Lane A §5, repo tests). SFC identities: sector balances sum to zero every year; consolidated == gross interest − Fed net income, tested (Lanes E/H). Flow identity: lenders' net loss at equal borrower cost = net fee exactly; interest saving = private income removed, dollar for dollar (Lane H). Bill-text facts: H.R.10924 premiums capped 8% of income ($0 <200% FPL); employer 8% of payroll only for non-offering *large* employers, $0 for small; displacement dates 2030/2033/2035; MOE first year 2038 = $0 in window; no CBO/JCT/CMS score exists (Lane C). Fed deferred-asset remittance mechanism (real since Sep 2022). Prototype reproduction: exact to ~4×10⁻¹⁵ (Lane A). |
| **Depends on chosen assumptions (labelled, switchable)** | Pass-through **β** (0.70/0.88/1.00 grid; central 0.88 is a prior, estimated nowhere). Yield transmission **τ = 0.32** (placeholder; combined total exactly linear in τ). **13%** tax-interaction/admin haircut (prototype prior mean, unestimated). Covered-base variant (central = loans + securitised once, $32.54T eligible; strict loans-only $24.89T; Lane E proxy upper bound). Avoidance elasticity, refi elasticity (default 0), category turnover/fixed shares. Stance path IORB_BASE (SEP-anchored placeholder, not a forecast). MFA: LTSS entitlement size, per-capita cost stack (induced demand, cost growth), Title II take by analogy, employer/premium take-up, enrolment ramps. Flow-channel MPC ranges (creditor 0.10–0.40; health recipients 0.60–0.90) × multiplier 1.0–1.5. |
| **Cannot presently be estimated reliably** | **The dial as a point** (proved non-identified, §1 — any point figure is a smuggled assumption). **β empirically** — the fee has never existed; no loan-level pass-through data. **τ empirically** within this project (estimable from yield data in principle; not done). **HCBS LTSS take-up** under MFA's ≥1-ADL threshold — no current-programme counterpart; widest swing in the MFA residual (+$2.34T at high parameters). **Title II revenue take** — no JCT score; analogy-based ±$1.2T. **Marginal-borrower (HANK) potency** of the fee — the sequence-Jacobian cross-check was scoped and **not run** (§6). Long-run avoidance/market-structure adaptation at high fee rates. |

---

## 3. Annual projections (deterministic v2, β = 0.88, central covered base)

Desired IORB = placeholder stance path (SEP-anchored input, Lane E config —
**not** an FRB/US output and not a forecast). Scenario IORB is solved from
`r = desired / (1 + β·s/(1−s))`; fee rate `f = r·s/(1−s)` (2028: statutory
0.15% introductory flat fee; 2029: half phase-in). Net fee and interest
saving in $T/yr. Full series: `repo/results/deterministic_annual_v2.csv`;
MC annual means: `repo/results/montecarlo_annual_v2.csv`.

| Year | Desired IORB (%) | s=50%: IORB / fee / net fee / int. saving | s=75%: IORB / fee / net fee / int. saving | s=90%: IORB / fee / net fee / int. saving |
|---|---|---|---|---|
| 2027 | 4.10 | 4.10 / 0.00% / $0.000T / $0.000T | 4.10 / 0.00% / $0.000T / $0.000T | 4.10 / 0.00% / $0.000T / $0.000T |
| 2028 | 3.90 | 3.77 / 0.15% / $0.011T / $0.006T | 3.77 / 0.15% / $0.011T / $0.006T | 3.77 / 0.15% / $0.011T / $0.006T |
| 2029 | 3.60 | 2.50 / 1.25% / $0.185T / $0.056T | 1.55 / 2.33% / $0.311T / $0.103T | 0.73 / 3.27% / $0.403T / $0.143T |
| 2030 | 3.40 | 1.81 / 1.81% / $0.290T / $0.100T | 0.93 / 2.80% / $0.439T / $0.160T | 0.38 / 3.43% / $0.530T / $0.202T |
| 2031 | 3.30 | 1.76 / 1.76% / $0.349T / $0.125T | 0.91 / 2.72% / $0.520T / $0.197T | 0.37 / 3.33% / $0.623T / $0.246T |
| 2032 | 3.25 | 1.73 / 1.73% / $0.400T / $0.146T | 0.89 / 2.68% / $0.591T / $0.230T | 0.36 / 3.28% / $0.704T / $0.286T |
| 2033 | 3.20 | 1.70 / 1.70% / $0.443T / $0.166T | 0.88 / 2.64% / $0.653T / $0.260T | 0.36 / 3.23% / $0.775T / $0.322T |
| 2034 | 3.20 | 1.70 / 1.70% / $0.485T / $0.183T | 0.88 / 2.64% / $0.712T / $0.287T | 0.36 / 3.23% / $0.843T / $0.354T |
| 2035 | 3.20 | 1.70 / 1.70% / $0.523T / $0.200T | 0.88 / 2.64% / $0.767T / $0.311T | 0.36 / 3.23% / $0.907T / $0.384T |
| 2036 | 3.20 | 1.70 / 1.70% / $0.560T / $0.214T | 0.88 / 2.64% / $0.819T / $0.333T | 0.36 / 3.23% / $0.968T / $0.410T |
| **10-yr** | — | **net fee $3.25T / interest $1.20T / combined $4.44T** | **net fee $4.82T / interest $1.89T / combined $6.71T** | **net fee $5.76T / interest $2.35T / combined $8.12T** |

Note the ZLB geometry the table makes visible: at s = 90% the solved IORB
sits at ~0.36% — the Fed would hold almost no conventional easing space
(Lane K §2c(4)).

Charts: `charts/a_combined_by_dial.png`, `charts/b_annual_s75.png`,
`charts/c_mfa_financing.png`, `charts/d_potency_by_dial.png`.

---

## 4. Inflation & employment effects

**FRB/US episode (Lane G):** +100bp desired tightening, 8 quarters
(2027Q1–2028Q4), equal all-in borrower cost q = +1.00pp, β = 0.88,
fiscal closure neutralised (`dfpex=1, dfpdbt=0, dfpsrp=0` — under the
standard fiscal rule 70–139% of a receipts windfall is recycled into tax
cuts, Lane D; all fee runs use the neutralised closure):

| Scenario | Δrff / wedge (pp) | GDP (xgdp) trough | Unemployment (lur) peak | Core PCE (picxfe) min* | Potency vs conventional |
|---|---|---|---|---|---|
| Conventional | 1.000 / 0 | −1.190% | +0.624pp | −0.104pp | 100% |
| s = 50% | 0.532 / 0.468 | −0.726% | +0.377pp | −0.061pp | 61.0% |
| s = 75% | 0.275 / 0.725 | −0.541% | +0.272pp | −0.046pp | 45.5% |
| s = 90% | 0.112 / 0.888 | −0.424% | +0.215pp | −0.037pp | 35.6% |

*picxfe minima are window-censored (still declining at 2032Q4); at the
matched 2029Q1 date fee runs are weaker still (s=75%: 33% of conventional).
Mechanism: realised private rates rise *more* in fee runs, but rg10 rises
far less (s=75%: +0.109 vs +0.399pp) — only the funds-rate component moves
the Treasury curve. **This ranking is FRB/US's channel structure** (the
model has no loan/mortgage/bank/reserve variable among its 933 variables);
it is not a measurement of the real fee — see the flow channel below and
Carlos's critique, answered in Lane H/K.

**Equal-effect rescales** — all-in cost needed at each dial to match
conventional's episode (75% converged in FRB/US; 50%/90% factor-inferred,
validated to 1.7% at 75%):

| Scenario | Scale | All-in cost q | Δrff | Incremental fee |
|---|---|---|---|---|
| Conventional | 1.00× | 1.00pp | 1.00pp | — |
| s = 50% | **1.64×** | 1.64pp | 0.87pp | 0.87pp of principal |
| s = 75% | **2.24×** | 2.24pp | 0.61pp | 1.84pp |
| s = 90% | **2.81×** | 2.81pp | 0.32pp | 2.83pp |

**Flow channel (Lane H) — the channel FRB/US omits.** Conventional
tightening *injects* interest income (baseline government→private net
interest injection $1.16T/yr in 2027 → $1.65T/yr in 2036; coupons to public
holders dominate IORB-to-banks ~10:1); the fee *removes* income (at s=75%,
$6.71T of private income over 10 years — identically the fiscal combined
total: **the $6T benefit and the potency correction are the same
dollars**). The reserve-stock drain itself is settlement timing and does
not mechanically tighten in an ample-reserves floor system; the *income
flow* is the demand-relevant object. Demand translation (MPC × multiplier
ranges, Lane H assumptions):

- **Episode scaling:** −0.02 to −0.11% GDP/yr (contemporaneous book),
  −0.03 to −0.26%/yr (mature book) vs the 0.649pp FRB/US gap at s=75% —
  **narrows the gap 5–40%, does not reverse it** (reversal needs creditor
  MPC ≈ 1). Combined episode potency at s=75% ≈ 50–67% of conventional.
- **Regime scaling, variant (i) deficit-reduction use:** additional
  −0.2 to −1.3% GDP/yr by the mid-2030s at s=75% (2036 range across dials:
  −0.15 to −0.90% at 50%, −0.22 to −1.34% at 75%, −0.27 to −1.60% at 90%)
  — same order as or larger than the whole FRB/US episode gap, so the
  ranking **plausibly reverses** at regime scale. FRB/US never produced a
  regime ranking (its result is an 8-quarter episode).
- **Regime scaling, variant (ii) fee spent on Medicare (the project's
  design):** sign flips — **+0.09 to +1.34% of GDP in 2030, +0.13 to
  +1.97% in 2036 at s=75%** (low-MPC creditors → high-MPC health
  recipients). Under the intended use the flow channel *reinforces* the
  price channel's pressure toward the floor. Variant (iii) (TGA
  accumulation): timing only, no demand effect.

**Bottom line on macro effects:** at the Fed's operating (episode) horizon,
a fee-split tightening is weaker than conventional per unit of borrower
cost on every computed or bounded variant; at the permanent-regime horizon
the answer depends on Treasury's use of the receipts, which is Congress's
choice, not the Fed's. Anyone quoting a single "combined potency by dial"
number has silently picked a horizon and a fiscal use.

---

## 5. Gap list — what would change the answers

1. **Empirical β.** The pass-through of a principal-based lending fee into
   borrower rates has never been observed. Loan-level evidence from
   analogous levies (or a statutory pilot) would move every revenue and
   potency number; β is currently a labelled prior (0.70–1.00).
2. **Empirical τ.** The yield-transmission placeholder (0.32) is exactly
   linear in the interest term and is MC v2's #2 sensitivity. Estimating
   IORB→Treasury-yield pass-through from yield data is feasible and would
   convert the τ=0 kill-condition from a bound into a finding.
3. **Sequence-Jacobian / HANK cross-check — NOT RUN.** It was scoped to
   test the marginal-borrower channel (the fee taxes new/floating
   borrowers, who are more rate-sensitive and higher-MPC than average —
   potency per dollar could exceed the average-MPC translation). This
   remains the largest *unquantified* channel in the decomposition.
4. **OG-USA long-run cross-check — NOT RUN.** Scoped as optional in the
   brief; no long-run tax/general-equilibrium validation exists.
5. **Official scores do not exist.** A CBO cost estimate of H.R.10924 and
   a JCT revenue estimate of its Title II would replace Lane J's
   modeller's construction and its analogy-based Title II take (±$1.2T) —
   the MFA residual, especially the high-stress case, is the softest
   number in this memo.
6. **LTSS design evidence.** MFA's ≥1-ADL HCBS entitlement has no
   current-programme counterpart; take-up evidence would narrow the
   $0.7–5.1T LTSS range that dominates the residual's uncertainty.
7. **A legislated dial default.** If Congress wants ≥75%, the analysis
   says it must legislate the default (or a fiscal objective) — the dual
   mandate will not deliver it. Conversely, evidence that a real FOMC
   weighted borrower-cost levels or distribution *inside* its loss would
   change the institutional forecast's basis (Lane K §6 lists falsifying
   evidence for each scenario).
8. **FRB/US stance path.** The fiscal module's desired-IORB input is a
   placeholder path, not the FRB/US baseline-E path integrated end-to-end;
   MC v2's #1 sensitivity is exactly this path.

---

## 6. Methods & reproducibility

**Repository:** https://github.com/cmucha46/monetary-symmetry-fee
(local consolidation commit for this memo: see repo `git log` — Lane L
commit; prior lane commits: 7c2fb9f v1 fiscal module, f202680 covered-base
variants, 8d194d2 flow channel, 365346b Monte Carlo v2.)

**Models & data vintages**

| Item | Version / vintage |
|---|---|
| Official FRB/US (PyFRB/US) | **1.1.1** (Feb 2026 package, public domain); data package **Oct 2026** (LONGBASE) |
| PolicyEngine FRB/US | `frbus` 0.1.0, commit **0fe79e89** (MIT); model.xml byte-identical to official |
| Validation tolerance | Cross-solver max diff **1.2×10⁻⁹** (100bp shock, common LONGBASE) |
| Private credit stocks | Federal Reserve Z.1 (eligible principal: central $32.54T / strict $24.89T) |
| Fed balance sheet anchors | H.4.1 (reserves ~$2.93T; Fed Treasuries $4.20T, MBS $2.08T) |
| MFA baseline | CBO Feb 2026 baseline (Medicare net subsidies $15.0T 2027–36) |
| Bill text | **H.R.10924, 119th Congress** (introduced Oct 29, 2026), GovInfo text |
| Prior prototype | ChatGPT 16,000-path Monte Carlo, seed 20261113 (audited, Lane A) |
| Fiscal MC v2 | 10,000 draws, seed 20261114, common random numbers across dials |

**One-command runners**

```bash
cd repo && python3 -m pytest            # full suite: 56 tests
cd repo && python3 run_score.py         # deterministic scores (v1 + v2 base variants)
cd repo && python3 run_flow_channel.py  # Lane H flow table -> results/flow_channel_v1.csv
cd repo && python3 run_montecarlo.py    # Lane I MC v2 -> results/montecarlo_v2.csv (see MONTECARLO_V2.md for exact entry point)
python3 mfa/mfa_model.py                # Lane J MFA residual + financing matrix (in repo/mfa/)
```

**Tests:** repo suite **56 passed** (cohort conservation, SFC zero-sum,
consolidated-vs-gross identity, fee formula/ZLB, deferred asset,
flow-channel zero-sum, Monte Carlo identities). MFA module reproduces its
financing matrix exactly on re-run.

**Lane map:** A prototype audit (`audit/PROTOTYPE_AUDIT.md`) · B tooling
(`upstream/TOOLING_VERIFICATION.md`) · C MFA sources
(`research/MEDICARE_FOR_AMERICA_SOURCES.md`) · D validation + wedge POC
(`validation/VALIDATION_AND_WEDGE_POC.md`) · E fiscal module v1 · F
covered base v2 · G FRB/US scenarios (`integration/FRBUS_SCENARIOS.md`) ·
H flow channel (`repo/FLOW_CHANNEL.md`) · I Monte Carlo v2
(`repo/MONTECARLO_V2.md`) · J MFA cost/residual (`mfa/RESULTS_MFA_V1.md`) ·
K dial analysis (`DIAL_ANALYSIS.md`) · L this memo.

**Reporting discipline:** the model was built to challenge the proposal,
not defend it. The prototype's $5.60T was treated as a hypothesis and did
not survive as a forecast (it survives only as the 75–90% policy-rule
range); the 57.1% dial did not survive at all. All fiscal totals are
quoted conditional on the dial as a policy-rule assumption — never at a
single "expected" dial.
