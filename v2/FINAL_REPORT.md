# Monetary Symmetry Fee v2 — Final Report

**Prepared:** November 22, 2026 · **Assignment:** Carlos A. Mucha's memo
of November 22, 2026 (permanent 50/50 design; `MEMO-2026-11-22-INPUT.md`)
**Status of the design evaluated:** fee rate f_t = IORB i_t after a
transition of at most 24 months; fee opens at 0.15%; **unified base** —
loans + corporate bonds + municipal bonds, Treasuries excluded, existing
obligations grandfathered (sponsor decision of Nov 22, 2026, superseding
the memo's loans-only §II.D; loans-only carried throughout as the
labeled sensitivity). **Effective date assumed: October 1, 2027**
(enactment during calendar 2027).

> **Every number in this report is a simulation under stated
> assumptions, produced by this project's models. Nothing here is a
> Federal Reserve or CBO forecast, and no figure was calibrated to
> reproduce the earlier exploratory model's results (memo §XII).**

---

## A. Executive summary

**The proposal survives testing as a feasible, fiscally positive
reform — at roughly half the scale of the $6 trillion hypothesis, and
with a real macroeconomic cost that the $6T framing did not carry.**

1. **Fiscal headline (central case, unified base, floating design).**
   The ten-year consolidated net fiscal benefit, FY2027–36, is
   **τ-conditional** (τ = transmission of the halved rate path into
   new-issue Treasury yields; unestimated in the literature, reported
   as a surface, never averaged):

   | | τ=0 | τ=0.25 | τ=0.5 | τ=0.75 |
   |---|---|---|---|---|
   | Before macro feedback (upper bound) | $4,059B | $4,529B | $4,998B | $5,467B |
   | **With FRB/US feedback, Regime C (24-mo sync)** | **$1,793B** | **$2,262B** | **$2,731B** | **$3,201B** |
   | With FRB/US feedback, Regime B (fast sync) | $1,570B | $2,039B | $2,508B | $2,978B |

   **The central case does not reach $6T after macro feedback — at any
   τ ≤ 0.75, in any regime, on either base.** Before feedback, $6T
   appeared only at the extreme corner of the parameter grid (τ = 0.75,
   high turnover, zero erosion, θ = 0.5: $6,324B). After feedback, no
   grid cell reaches $6T (maximum $4,151B). The honest headline is a
   **~$2–3T-class central benefit** under the conservative
   macro-feedback bound, inside an interval whose optimistic end is
   ~$4.1–5.5T. Section B.6 identifies exactly which assumptions fail.

2. **Why the feedback pass halves the answer.** FRB/US (Design E: the
   model's own inertial Taylor rule, never told about the fee) offsets
   only **57–63%** of the fee. The 50/50 configuration therefore runs
   *tighter* than conventional policy — covered lending rates sit the
   full wedge (+~2.0pp) above baseline, real GDP troughs −1.7% below
   baseline, unemployment is still **+0.77pp** above baseline at
   2036Q4 — and the resulting endogenous fiscal drag (lost revenue,
   cyclical outlays) costs **−$2.4 to −2.7T** over the window. Inflation,
   by contrast, fully re-anchors (deviation −0.02pp by 2036Q4 in every
   regime). Design E is the *conservative* end of the rule-response
   interval (a stance-targeting FOMC would offset more); the report
   carries both ends rather than choosing.

3. **Synchronization is feasible, and speed is not the binding margin.**
   The rule absorbs synchronization in ~2 quarters (Regime B) about as
   well as over 24 months (Regime C): peak transition inflation
   deviation 0.28 vs 0.26pp. Synchronization also completes through a
   2022-class inflation shock (Regime D) and, trivially, through a
   recession (Regime E). The cost of the regime is a *level* effect of
   the permanent wedge, not a ramp effect.

4. **Revenue is procyclical by construction.** Because f = IORB, the
   fee collapses to ≈0.11% at the recession trough; cumulative receipts
   fall from $3,809B to $1,945B (loan-only, FRB/US paths). Any fiscal
   plan built on the fee must be sized to the recession state, not the
   mean — the memo's §X separation of entitlement financing from annual
   receipts is not optional, it is load-bearing.

5. **The Section IX hypothesis survives only conditionally.** At equal
   borrower cost (full pass-through) with receipts banked, redirecting
   the policy-sensitive charge from low-MPC creditors to Treasury is
   more contractionary at 27/27 grid points — but the effect is small
   (−3.0% of the interest flows rerouted, median), because banks
   recapture ~(1−β) of the IORB halving as deposit spread and return
   part of it to the same creditors as dividends. If Congress *spends*
   the receipts — transfers or purchases — the impulse flips positive
   at 81/81 grid points (+14.9% / +20.0% medians). **The hypothesis is
   a property of the fee plus a decision to bank the receipts.**

6. **Treasuries stay out — on arithmetic, not preference.** Included
   issuer-assessed, the fee is the Treasury paying itself: net exactly
   $0. Included holder-assessed, receipts ($2,350B consolidated over
   the window) are offset by the new-issue yield gross-up ($2,091B),
   leaving a +$259B *timing* residual that reverses in falling-fee
   states — before any term-premium or foreign-demand cost, which are
   one-directional and unquantified (Appendix E).

---

## B. The eight questions, answered numerically

### Q1 — Synchronization: how fast, and along what paths?

As fast as ~2 quarters after the October 1, 2027 effective date, at no
measurable extra transition cost in-model. FRB/US Design E (β = 1, MCE;
the inertial Taylor rule finds the path — it is never imposed):

| | B: fast sync | C: 24-month sync |
|---|---|---|
| f = rff reached | 2028Q2 | 2029Q4 |
| Post-sync funds-rate offset vs baseline | −1.28pp | −1.19pp |
| Synchronized pair (rff ≈ f) | ≈2.02% | ≈2.10% |
| Conventional baseline funds rate (same years) | ≈3.3% | ≈3.3% |
| Share of the fee the rule offsets | 63% | 57% |
| Peak transition inflation deviation | +0.28pp | +0.26pp |

Under stress: in Regime D (inflation shock mid-transition) sync
completes on the C schedule with the fee peaking at **4.28% (2029Q4)**
chained to the shock-elevated funds rate; in Regime E (recession) sync
completes at ≈1.06% by 2029Q4 and the pair then falls to ≈0.11% at the
2030 trough. VAR-expectations robustness: offsets −0.94pp (B) / −0.90pp
(C) — smaller, same qualitative picture. Caveat (Lane B §7.2): the
financial-stability and credit-supply risks of a fast ramp are outside
FRB/US; "absorbable" is a statement about demand/inflation dynamics.

### Q2 — Fee revenue: annual, cumulative, and the eligible-stock path

Unified base, floating design, central turnover, cohort skeleton fee
path (0.15% FY28; 1.00% FY29 blend; 1.95% FY30+). Gross collections are
rate × covered stock; net = gross × (1 − erosion) × (1 − 13% haircut,
ASSUMED). Full annual table in `integration/FINAL_FISCAL_PROJECTION.md`
§2. Headline figures:

- **Gross cumulative FY28–36: $4,625B** (unified) vs $3,433B loans-only.
  Annual gross rises $6.8B (FY28) → $877.8B (FY36) as the covered stock
  phases in: $9,077B (FY28) → $46,757B (FY36) of an eligible stock
  growing $45,112B → ~$59,900B. The phase-in is grandfathering, working
  as designed: covered share reaches only 78.0% by FY36 (bonds phase
  in slowest — munis 67.2% — because bond turnover δ ≈ 0.09–0.11 is a
  third of the business-loan rate).
- **Net fee receipts (skeleton path): $3,650B.** At Lane B's iterated
  fee paths the receipts scale by **×1.116 (B) / ×1.110 (C) / ×1.130
  (D) / ×0.567 (E)** — the fixed point settles the fee slightly above
  the skeleton's 1.95%, and the recession state roughly halves revenue.
- Locked design (fee fixed at origination): gross $3,781B unified —
  floating beats locked at every τ because locked vintages keep
  origination-era rates while the synchronized rate rises above them.

### Q3 — Treasury interest savings, net of the Fed

Two independent measurements, on different bases, bracketing the
channel:

- **Consolidation (τ-surface, repricing mechanics on the actual
  maturity structure** — $31,830B marketable, MSPD Sep 30 2026; WAM 70
  months; 32.9% repricing in year 1**):** cumulative consolidated
  savings FY27–36 = **$0 / $469B / $939B / $1,408B at τ = 0 / 0.25 /
  0.5 / 0.75**, counted only on the non-Fed-held share (×0.8559; the
  Fed-held share nets to zero in consolidation — counting it would
  double-count against remittances). Savings are back-loaded by the
  maturity structure: at τ = 0.5, $87B in FY30 rising to $172B by FY36.
- **FRB/US endogenous:** the 10-year Treasury yield falls −0.23pp
  (post-sync mean, Regime B) and in-model federal interest payments
  fall **$2,560B** cumulatively — a larger figure on a different basis
  (unconsolidated, endogenous debt path, loan-only κ); it is *not*
  added to the consolidation (one-ledger rule), it is the cross-check
  that the yield channel is real inside a full macro model.
- **Net of remittances:** halving IORB raises Fed earnings ~$58.5B/yr,
  but the increment first extinguishes the −$232.5B deferred asset
  (H.4.1, Nov 2026). **Δ cash remittances are $0 through FY29, +$8.8B
  in FY30, and +$410B cumulatively** — the deferred-asset identity is
  why the remittance channel is a minor term despite the large earnings
  delta.

### Q4 — Private credit conditions: comparable costs? Who bears it? Does credit migrate?

**Not comparable at full pass-through under Design E — the regime is
tighter than conventional policy, by +0.74pp on the combined charge**
(post-sync mean, Regime B). Covered new-loan rates sit above baseline
by the full imposed wedge: **+2.02pp on mortgages (`rme`) and consumer
credit (`rcar`), +1.53pp on business credit (`rbbb`, κ = 0.757
loan-only)** — because the rule retires only ~63% of the fee. Two
protocol facts bound the reading: the wedge is *imposed* on covered
rates (the endogenous Treasury-curve relief, rg10 −0.23pp, does not
additionally relieve them in these runs — conservative for the
equivalence question), and uncovered rates *do* get the curve relief,
so the relative price of covered vs uncovered credit rises by roughly
the full wedge — the in-model shadow of the substitution margin.

Incidence across borrowers (cohort + literature lanes):

- **Mortgages** are covered from day one (κ = 1 on originations) and
  cannot migrate offshore; the household mortgage stock is the slowest
  to phase in (67–80% covered by FY36) but new borrowers bear the full
  wedge immediately.
- **Bond-market access is the dividing line for business borrowers.**
  Firms that can substitute loans ↔ bonds (Becker–Ivashina elasticity)
  face κ < 1 effective coverage and a grossed-up but partially
  avoidable charge; **small businesses have no substitute** — no bond
  market, no offshore lender — and bear the full pass-through. The
  incidence is regressive across firm size.
- **Migration/offshore:** the substitutable margin is ~$1–1.5T of the
  $9.43T BIS cross-border claims on the US. In the consolidation this
  enters as the erosion grid: year-5 covered-base erosion of 40%
  (vs 0%) cuts the grid median benefit by ~$1.2T at every τ — the
  widest single behavioral lever in the model.

### Q5 — Stabilization: comparable, better, or worse? Whose spending behavior decides?

**Inflation: comparable. Employment: worse, at the conservative bound.**
Inflation returns to baseline in every regime (−0.02pp deviation by
2036Q4; mildly negative, −0.2 to −0.3pp, mid-window). Unemployment does
not: **+0.77pp above baseline at 2036Q4** in Regimes B and C (MCE),
real GDP trough −1.77%. Under VAR expectations the employment cost is
smaller and receding (+0.50pp at horizon). Per Lane B §7.1 this is an
interval, not a point: Design E's outcome-reactive rule is the
conservative end; a stance-targeting FOMC that offsets the wedge
one-for-one would show near-equivalence by construction and prove
nothing. The width of that interval is itself a finding — equivalence
turns on how the FOMC would formulate its reaction function under the
statute, an institutional question no estimated parameter settles.

**Dependence on creditor vs debtor behavior is decisive, and it runs
through Congress, not just households.** The SFC experiment (Section
IX, Q7 below): with receipts banked, the outcome depends on the MPC
asymmetry (creditors 0.05–0.20 vs debtors 0.50–1.00) and on pass-through
θ; with receipts spent, the recycling term is an order of magnitude
larger than the monetary redistribution term and the stabilization
sign flips. Stabilization properties cannot be stated for the fee
alone — only for the fee plus a fiscal-recycling rule.

### Q6 — Fiscal outcome: positive? Does it approach $6T? Which assumptions fail?

**Positive, robustly; $6T, no.** Final central case (Regime C
feedback): **$1,793B / $2,262B / $2,731B / $3,201B at τ = 0 / 0.25 /
0.5 / 0.75**; Regime B: $1,570–2,978B. The feedback-adjusted grid
(floating cells) has medians $1,608–3,016B across τ and a maximum of
$4,151B; one joint-adverse corner cell is ≈$0 (−$38B). The benefit is
positive in every central configuration computed, but $6T is not
approached once macro feedback is included, and was a tail outcome
even before it.

**Which assumptions fail** (relative to the exploratory model that
produced ~$5.6T under the superseded discretionary design):

1. **The omitted macro drag.** Accounting-only consolidation counts
   receipts, savings, and remittances but not the endogenous revenue
   loss from running the economy cooler. In FRB/US that term is
   −$2.4 to −2.7T — the single largest correction in v2.
2. **Equivalence was assumed; it does not hold at the conservative
   bound.** The rule offsets 57–63% of the fee, not 100%. The residual
   tightness is what generates the drag. ($6T arithmetic implicitly
   required restraint to be fully offset so that only the fiscal
   transfers remained.)
3. **The fixed point binds revenue.** Because f = rff and rff falls,
   the fee settles at ~2.0–2.1%, not at a rate chosen for revenue; and
   in recession states it collapses (receipts ratio 0.567). Revenue
   sized off a constant ~2% on a growing stock overstates the
   recession-inclusive path.
4. **Grandfathering is expensive.** Only 78% of the unified eligible
   stock is covered by FY36; the naive rate × full-stock calculation
   overstates early revenue by the entire phase-in gap (FY28 gross is
   $6.8B, not ~$700B).
5. **τ does the remaining work and τ is unknown.** Even granting every
   other favorable assumption, the interest channel contributes
   $0–1,408B across the τ surface; there is no published estimate to
   narrow it, and v2 reports the surface rather than inventing one.

### Q7 (§IX) — The interest-income feedback channel: tested

Tested in the SFC layer at **equal combined charge** (IORB 4% vs
IORB 2% + fee 2%), households split into creditor (MPC 0.05–0.20) and
debtor (MPC 0.50–1.00) sub-sectors, deposit β ∈ {0.45, 0.55, 0.65},
θ ∈ {0.5, 0.75, 1.0}; 243 regime pairs, all closing under the full
stock-flow identities. Net demand impulse, Regime B − Regime A, as %
of Regime A's loan-interest flows ($1,045B illustrative):

- **Deficit reduction (receipts banked): hypothesis survives at
  θ = 1 only** — negative at 27/27 grid points, median −3.0% (central
  point −$30B: creditor interest −$12B, creditor dividends −$1B,
  debtor cash flow −$17B). With the credit-volume response off, the
  pure income channels favor the hypothesis at every θ (medians
  −0.7% / −1.8% / −3.0%). The mechanism's sign is as predicted; its
  size is small because banks recapture ~(1−β) of the IORB halving as
  deposit spread and pay part back to the same creditors as dividends.
- **Transfers to debtor households: flips everywhere** — positive at
  81/81, median **+14.9%**.
- **Government purchases: flips everywhere** — positive at 81/81,
  median **+20.0%**.
- **Key fragility:** if the grandfathered book repriced with IORB (the
  all-adjustable sensitivity), the debtor windfall on the ~$13T
  pre-enactment stock flips even the θ = 1 / deficit case (+7.6% at
  center). The result is partly a bet on the ~92% fixed-rate US
  mortgage stock.

Verdict: the channel is real, correctly signed, and **second-order**;
the fiscal-recycling decision is first-order. Full results:
`sfc/SECTION_IX_RESULTS.md`. (One-period, first-round experiment —
signs and channel rankings, not FRB/US-comparable magnitudes.)

### Q8 (§X) — Healthcare

**Separated, as the memo directs.** No Medicare for America
optimization, costing update, or financing application was performed
in v2; the fee verdict above was reached independently of any use of
the proceeds. The v1 Medicare for America study (central residual
+$2.52T FY28–36 after Title II offsets, on H.R.10924 as written)
stands as prior, separate work and was not revised. Two v2 findings
bear on any subsequent application and are recorded here without
applying them: (i) the final fee benefit (~$1.8–3.2T central, with
feedback) is materially smaller than the v1 dial-based figures the
earlier comparison used; (ii) fee revenue is procyclical by
construction (Regime E), which is precisely the contingency memo §X
anticipates — appropriations must not be capped by annual receipts.

---

## C. Fiscal projection and Monte Carlo — summary

Full tables: `integration/FINAL_FISCAL_PROJECTION.md` (final) and
`integration/FISCAL_PROJECTION.md` + `MONTE_CARLO.md` (pre-feedback
record). Central-case bridge at τ = 0.5, Regime C ($B):

| Component | Pre-feedback | Final |
|---|---|---|
| Net fee receipts | 3,650 | 4,050 (×1.110 fee-path ratio) |
| Treasury interest savings (τ = 0.5) | 939 | 939 |
| Δ Fed cash remittances | 410 | 410 |
| FRB/US endogenous drag | — | −2,667 |
| **Consolidated net** | **4,998** | **2,731** |

Grid enumeration (288 cells/τ pre-feedback; 144 floating cells with
Regime C feedback) — medians by τ: pre-feedback $3,502 / $3,971 /
$4,440 / $4,910B; feedback-adjusted $1,608 / $2,078 / $2,547 / $3,016B.
These are conditional simulation-grid summaries, **not confidence
intervals**: the decisive parameters (pass-through at fee scale,
erosion, τ) are uncalibrated in the literature, so the grid is
enumerated, not sampled. Attribution (pre-feedback medians): erosion
is the widest behavioral lever (E = 0 → 40% moves the median by
~$1.2T); turnover/phase-in speed ~$0.8T; floating beats locked by
~$0.66T; base breadth (unified vs loans-only) ~$0.79T of median,
~$1,043B in the final central case at τ = 0.5. Deposit β is inert in
the fiscal identity by construction (its action is in the SFC bank
layer) and is reported as such rather than assigned an invented effect.

---

## D. Critical assessment

**Strongest evidence for the proposal.**

- The accounting is sound and conservative: every lane reconciles
  (SFC identities hold in all 243 Section IX regime pairs; the
  consolidation's one-ledger rule is test-enforced), grandfathering
  and the deferred-asset identity are respected, and gross is always
  shown beside net. The benefit does not depend on any single heroic
  parameter: it is positive at τ = 0 (no yield transmission at all),
  on the loans-only base, and in every central configuration.
- Synchronization is absorbable in a full macro model under normal
  conditions *and* under both stress shocks, at either speed, with
  inflation fully re-anchoring. The regime never produces instability
  in any of the 30 Lane B solves.
- The design has a genuine automatic stabilizer no conventional-plus-
  levy design has: restraint (and revenue) vanish at the zero lower
  bound by construction, because f = IORB.
- The Section IX mechanism — the proposal's most original claim — has
  the predicted sign at every grid point where the comparison is
  clean (θ = 1, receipts banked, volume response off at all θ).

**Strongest evidence against.**

- **Equivalence fails at the conservative bound.** The 50/50 pair is
  +0.74pp tighter than conventional policy in FRB/US; unemployment is
  still +0.77pp at the ten-year horizon. If the FOMC in fact behaves
  like Design E's rule, the proposal buys its fiscal dividend with a
  persistently cooler economy — a trade, not a free lunch. The
  proposal's central marketing claim ("same restraint, different
  incidence") is *not* established; it holds only if the FOMC targets
  the combined stance, which the statute cannot compel it to do in
  the model's terms.
- **Pass-through at fee scale is uncalibrated.** Every published levy
  estimate is for burdens ≤ ~45bp; the synchronized fee is ~200bp.
  The θ grid {0.5, 0.75, 1.0, 1.15} spans the plausible range but no
  evidence selects within it, and both the fiscal drag and the
  Section IX verdict move materially across it.
- **τ is unestimated.** The interest channel is worth $0–1.4T across
  the surface and there is no published estimate for this regime.
  Anyone quoting a single total for this proposal is quoting a τ they
  chose not to disclose.
- **Revenue procyclicality.** Receipts roughly halve in the recession
  regime. A Congress that pre-commits the mean path of receipts to
  permanent spending builds a structural deficit into every downturn.
- **The Section IX dividend requires banked receipts.** The
  disinflationary refinement exists only under deficit-reduction
  recycling; the politically likely recyclings (transfers, purchases)
  reverse it. The proposal's monetary refinement and its fiscal
  popularity pull in opposite directions.

**Circumstances under which the proposal fails.**

1. Pass-through materially below 1 *combined with* an outcome-reactive
   FOMC: covered credit stays expensive, the drag grows, and the joint
   adverse grid corner already shows the fiscal benefit ≈ $0.
2. Substitution faster than the erosion grid's top (40% by year 5) —
   e.g., a rapid build-out of exempt or offshore channels; the unified
   base closes the loan↔bond margin but not the offshore or
   exempt-instrument margins.
3. A shift of the household stock toward adjustable-rate credit, which
   reverses the Section IX sign (the grandfathered-repricing
   sensitivity) and weakens the fixed-rate anchor the design leans on.
4. τ near 0 *and* a low-turnover world: phase-in is slow, the interest
   channel is absent, and the benefit reduces to the fee on a slowly
   growing covered stock minus the drag — the low grid cells
   ($901B–$1,370B minima after feedback) describe this world.
5. Legal failure of the municipal component (flagged in
   `cohort/BASE_B.md` §5): the base is modular and survives its loss,
   but ~$3.5T of eligible stock and its collections leave with it.

---

## E. Appendix — Treasuries in the base (netting arithmetic)

Treasuries are excluded from the headline base. The included variant,
in consolidation (marketable stock $31,830B; bucket repricing per
`cohort/data.py`; fee path as in the headline; full computation in
`integration/treasuries_appendix.py`, outputs in
`integration/outputs/treasuries_appendix.csv`):

- **Issuer-assessed** (the unified base's treatment for other bonds):
  the Treasury pays the fee to itself. Gross churn reaches ~$440B/yr
  at full phase-in; **consolidated net = $0 in every year, exactly.**
- **Holder-assessed:** consolidated receipts FY27–36 = **$2,350B**;
  consolidated extra interest from the new-issue gross-up (g = 1.0,
  ASSUMED) = **$2,091B**; **net = +$259B**, which is purely a
  transition-timing residual — receipts float at the current fee on
  all covered stock while gross-up coupons lock at issuance-year fees,
  so the residual is positive while the fee ramps up and **reverses in
  falling-fee states** (in Regime E's world, locked gross-ups persist
  while receipts collapse). In steady state the net is zero.
  Assumptions labeled: gross-up g = 1.0; Fed holds 14.41% of the
  covered stock (its payments wash through remittances); no
  term-premium, foreign-official-demand (~$9T foreign-held), or
  safe-asset/collateral response — all one-directional against
  inclusion and unquantified.

**Conclusion:** inclusion adds ≈0 in steady state and at best a
~$0.26T timing residual over the window, against unquantified
market-function risks to the world's benchmark asset. Exclusion is
the arithmetic answer, not a modeling convenience.

---

## F. Limitations and integrity disclosures

1. **Lane B's loan-only lower bound — where it still binds.** Lane B
   ran before the unified cohort outputs landed, so its wedges and
   receipts are loan-only (κ_rbbb = 0.757). The final projection
   corrects the *stock* side through the cohort layer (unified
   collections × Lane B's fee-path ratio — an ASSUMED proportionality)
   and takes the *drag* from the loan-only-κ runs. Lane B's κ = 1.0
   sensitivity previews the unified wedge: drag deepens ~6%
   (B: −$2,610B → −$2,761B) and receipts fall ~4% through the lower
   fixed-point fee. The final drag is therefore, if anything,
   understated on this channel; the direction is disclosed, the
   correction is not fabricated.
2. **MCE inflation-shock rescaling (Lane B §8).** The original Regime
   D shock (add-factor +2.0) realized +26.9pp of inflation under MCE —
   a measured ≈13.4× linear amplification in the installed package's
   wage-price block, a design failure, not a solver failure. It was
   rescaled to +0.33 to match the VAR shock's realized severity
   (+4.37pp vs +4.46pp peak); the MCE shocked baseline and both D runs
   were recomputed; the correction is logged in
   `frbus/regime_outputs/run_log.json`. All other runs are as
   originally executed; no solver failures occurred anywhere.
3. **The v1 `rme` correction.** V1 concluded FRB/US had no mortgage
   rate because no variable *name* contains "mort"; `rme` is the
   conventional mortgage rate. V1 therefore never wedged mortgages and
   implicitly *cut* mortgage rates (via falling rg10) while raising
   others. **V1's FRB/US potency/non-equivalence factors (0.61 / 0.46
   / 0.36) are compromised and are not carried into v2 anywhere.**
   The other two prongs of the v1 dial verdict stand; the v1 dial
   design itself is superseded by the memo in any case.
4. **Regimes D/E in the consolidation are partial adjustments** (fee +
   drag only; savings/remittances not re-based to shocked paths) and
   are labeled as such wherever they appear; Lane B's in-model
   Δsurplus is the consistent shocked-baseline figure.
5. **ASSUMED / unestimated parameters (complete list).** Tax-
   interaction haircut 13% (v1 carry-over; fee deductibility is an
   open legislative parameter that would move it); erosion θ-coupling
   `e = E·θ·ramp`, cap 60%, linear FY28–32 phase-in; τ ∈ {0, .25, .5,
   .75} (no published estimate exists); FRB/US pass-through β
   (uncalibrated at fee scale; headline β = 1); drag ∝ receipts-ratio
   proportionality (this pass); receipts ratio applied across bases
   (this pass); Fed portfolio yield 2.7% and opex $12B/yr (cohort
   skeleton); deferred asset −$232.5B (MEDIUM confidence, secondary
   retrieval); Treasury bucket split TIPS $2,140B / FRN $740B
   (residual, assumed) and bucket maturity fractions (calibrated to
   the published 33% one-year share); bond turnover δ (corporates
   0.11, munis 0.09, anchored to issuance/maturity facts, not a
   published series); Section IX dividend payout ratios, credit-volume
   semi-elasticity ε, wage split (flagged in its own file); Treasuries
   appendix gross-up g = 1.0 and Fed covered-share = overall share.
6. **Structural simplifications.** Debt stock held flat in the
   consolidation (no deficit-feedback loop — conservative); Fed
   portfolio size/yield frozen at H.4.1 Nov 2026; nonmarketable debt
   outside the repricing skeleton; FRB/US receipts allocated evenly
   across quarters and scaled by baseline GDP (deviations <1%);
   `rff` stands in for IORB (the ~2bp funds–IORB spread ignored);
   the SFC layer is a one-period accounting/behavioral experiment on
   illustrative stocks, not a calibrated dynamic model.
7. **What would change the verdict.** An empirical estimate of τ; any
   evidence on pass-through at ~200bp scale (the NZ Mortgage Interest
   Levy — the closest institutional precedent — was analyzed by NZ
   officials at ≤50bp of OCR relief per 100bp of levy and was never
   enacted; `SOURCE_VERIFICATION.md`); an FOMC reaction-function
   commitment to stance-targeting; or a HANK-class model that can test
   Section IX dynamically. Until then, the interval — not a point —
   is the result.

---

## G. Deliverables map (memo §XI)

| Deliverable | Location |
|---|---|
| A. Reproducible repository | GitHub `cmucha46/monetary-symmetry-fee`, `v2/` (v1 preserved untouched); tests: cohort 23, SFC 35, integration 23 — all passing |
| B. SFC model + reconciliation tests | `v2/sfc/` (`sfc_core.py`, `MATRICES.md`, 23 skeleton tests incl. negative tests that must fail on a phantom dollar) |
| C. Macro simulation, common shocks | `v2/frbus/REGIME_RESULTS.md` + `regime_outputs/` (30 path CSVs, metrics, run log) |
| D. Ten-year fiscal projection | `v2/integration/FINAL_FISCAL_PROJECTION.md` (+ pre-feedback `FISCAL_PROJECTION.md`) |
| E. Monte Carlo (grid enumeration) | `v2/integration/MONTE_CARLO.md` + feedback-adjusted summary in the final projection §3 |
| F. Critical assessment | §D above |
| G. Executive summary | §A above |

*All figures are simulations from this project's models under the
stated assumptions — not Federal Reserve or CBO forecasts.*
