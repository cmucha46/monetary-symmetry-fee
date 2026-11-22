# Combined Study — Monetary Symmetry Fee v2 + Medicare for America under a Spending Closure

**Prepared:** November 22, 2026 · **Assignment:** sponsor's combined-study
authorization of November 22, 2026 (lifting, for this study only, the
§X separation of the November 22, 2026 memo) · **Plan under study:**
ALL budget savings from the Monetary Symmetry Fee — fee receipts **and**
reduced net interest — are directed to Medicare for America
(**H.R.10924, 119th Cong.**, DeLauro). MFA's own financing is as written
in the bill. The fee is the v2 design as delivered: permanent 50/50
(f = IORB after a ≤24-month transition from 0.15%), unified base
(loans + corporate bonds + municipal bonds, Treasuries excluded),
floating design headline, effective October 1, 2027.

> **Standing caveats — read before citing any number.**
> (1) Every figure is a **simulation under stated assumptions** from
> this project's models — not a Federal Reserve, CBO, or JCT forecast.
> (2) **No CBO/JCT/CMS score of H.R.10924 exists.** MFA costs are a
> modeller's construction built from the bill text and CBO baselines
> (Lane 1, verified by exact re-run), presented as ranges with named
> drivers, never as points.
> (3) **τ_long — transmission of the administered-rate decline into
> new-issue Treasury yields beyond one year — is UNESTIMATED.** Results
> are reported as a τ_long surface, never averaged or integrated over.
> The front end (≤1 year) carries no τ: its transmission is 1 **by
> arbitrage** (Sponsor Correction #2; §6, §8).
> (4) The **13% tax-interaction haircut** on fee receipts is **ASSUMED,
> unestimated** (carried from v1); gross collections are shown beside
> net throughout.
> (5) One-ledger rule (memo §III.C): fee receipts, interest savings,
> and Fed-remittance changes are counted once each, on one debt path;
> no channel is double-counted.

---

## Executive summary and coverage verdict

**Question:** under the spending closure, does the fee's net
contribution cover Medicare for America's residual — the incremental
federal cost left after MFA's own financing (premiums, employer
contributions, Title II revenues, displaced federal outlays)?

**Answer, on the consolidated ledger (headline basis, corrected
maturity-dependent τ, growing CBO debt path, banked-ledger closure):**

| MFA scenario | Residual FY28–36 | Verdict | Margin by τ_long = 0 / 0.25 / 0.5 / 0.75 |
|---|---:|---|---|
| Low | −$1,289B | **Financed at every τ_long** — the bill self-finances in-window; the fee is pure surplus | +3,960 / +4,400 / +4,835 / +5,267 ($B) |
| **Central** | **+$2,524B** | **Financed at every τ_long, including τ_long = 0** | **+179 / +634 / +1,085 / +1,532 ($B)** |
| High-stress | +$10,730B | **Not financed at any τ_long** — the fee covers at most ~35% of the residual | −7,960 / −7,470 / −6,984 / −6,503 ($B) |

Three findings drive that verdict, in order of importance:

1. **The front end was mispriced, and correcting it changes the
   central case.** v2 and the first consolidation pass applied a
   single scalar τ to all new-issue yields. But the front-end third of
   the repricing exposure (bills and the ≤1-year maturing share, 33%
   of the marketable stock) is arbitrage-locked to IORB: its yield
   decline is the full administered decline (1.95pp), not τ × 1.95pp.
   Corrected, the interest line under the combined closure is
   **$909B even at τ_long = 0** and $1,816B at τ_long = 0.5 (front
   $901B / long $915B) — and the central case, which the scalar
   treatment financed only at τ ≥ 0.5 (margins −731 / −40 / +641 /
   +1,312), is **financed at every τ_long**. The verdict in the
   central case no longer depends on the unestimated long-segment
   parameter; τ_long now sets only the size of the surplus. The same
   correction restates v2's own banked verdict upward
   ($1,793 → $2,412B at τ_long = 0; $2,731 → $3,041B at 0.5): **v2's
   interest line was understated at every τ** (§6).

2. **In FRB/US, the spending closure reverses the fee's macro
   signature — with a load-bearing caveat.** MFA's demand impulse
   lifts the Taylor rule so far that the combined funds path settles
   at **rff = f = 3.70%, above the conventional baseline**, fee
   receipts rise **+74% to $6,628B** (loan-only basis), and the fee's
   employment drag is more than offset: unemployment deviation at
   2036Q4 is **−0.61pp combined vs +0.77pp fee-only**; cumulative
   Δsurplus is **+$5,153B** (loan-only; ≈ +$7.5T on a first-order
   unified scaling). The caveat: FRB/US has no tax-incidence carrier,
   so Title II's $6.11T enters as **demand-neutral** residual
   receipts — the model sees MFA's spending in full and none of its
   tax-side drag. The in-model combined margin is therefore an
   **upper bound**, and the receipts endogeneity it displays is real
   in direction but overstated in size (§4).

3. **Timing, not the window total, is the central case's binding
   constraint — and high-stress fails on any basis.** The MFA
   residual is back-loaded (75% of the central residual falls in
   2035–36, when the residual-Medicaid switch completes) while the
   fee phases in over the same years. Under the banked-ledger closure
   the cumulative position never goes negative at any τ_long; on a
   strict pay-as-you-go reading, annual shortfalls occur in 2030
   (all τ_long ≤ 0.5; only −$10B at τ_long = 0.5) and in 2035–36.
   The high-stress case — driven by the LTSS entitlement and
   induced-demand stack — is not financed under the consolidation
   (best margin −$6,503B) **or** in FRB/US (Δsurplus −$1,514B despite
   receipts lifted to $8,221B). Both independent bases agree on low
   (financed) and high-stress (not financed); after the τ correction
   they also agree on central (financed), though for different
   reasons and with very different margins (§5.4).

**Interest-savings erosion is small.** Spending the savings on MFA
does erode the interest line — the combined debt path sits above the
banked path — but the effect is ~2% (scalar basis: $26B at τ=0.5
central; corrected basis: the combined-path line of $1,816B vs
$1,858B on the no-plan growing path at τ_long = 0.5). It is dwarfed
(~17×) by the conservatism the growing-path correction removed
(+$221–635B) and by the front-end correction itself (+$220–909B).

**CBO reconciliation.** Priced against CBO's rule of thumb ($379B of
net-interest saving per 0.1pp of sustained curve decline, 2027–36),
the model's implied saving per 0.1pp rises from **$96B** (v2 as
booked: flat debt, scalar τ) to **$143B** (growing debt path) to
**$191B** (maturity-dependent τ) — the two corrections close **33%**
of the gap. The remainder is accounted for, not anomalous: repricing
realization (only ~35% of the headline decline reaches the stock's
average rate inside the window), marketable-only coverage, and the
deliberate Fed-share consolidation (with +$410B returned via
remittances on a separate line). **CBO's figure is used nowhere as an
input** (§7).

---

## 1. The plan, the closure, and the method

**The plan.** Congress enacts both the Monetary Symmetry Fee (v2
specification) and Medicare for America (H.R.10924 as written), and
directs all fee savings — net fee receipts, reduced net interest, and
the change in Fed remittances — to MFA. Per the memo's §X (which this
study's authorization preserves on this point), MFA's appropriation
is **not capped by annual fee receipts**: budget scoring and legal
authority to pay benefits are separate questions, and the Fed must
remain free to cut rates — collapsing fee revenue — in a recession
without threatening benefits. The coverage question is therefore
asked of a **banked ledger over the window**, with year-by-year
shortfalls reported separately (§5.3), not imposed as a constraint.

**MFA as written (bill facts used throughout).** Premiums capped at
8% of income, $0 below 200% FPL (§2204); employer contribution of 8%
of payroll **only** for large non-offering employers (§125(b)) — the
shorthand "8% of all payroll" would overstate this line several-fold;
Title II (§§201–210): sunset of TCJA (P.L. 115-97) and P.L. 119-21
after Dec 31, 2027 (§201), 5% surtax above $500k, stepped-up-basis
repeal, payroll add-on 0.9%→4%, NIIT 3.8%→6.9%, HSA termination,
excises; state Medicaid MOE (§2209) first payment year 2038 — **$0
inside FY2027–36** in every scenario. Enrollment phases: transitional
public option + uninsured auto-enrollment 2028–29 (no displacement —
pure addition), Medicare non-duals switch 2030, large-employer
process from 2031, duals/Medicaid-expansion/CHIP/exchange switch
2033, residual Medicaid 2035.

**Method — three lanes, one ledger.**
- **Lane 1** re-based MFA: exact re-run of the v1 model, annual
  residual paths by scenario (§2).
- **Lane 2** ran FRB/US (Design E) with MFA imposed: MFA-only,
  combined Regime C + MFA, Regime B sensitivity, VAR robustness (§4).
- **Lanes 3–4** built the consolidated coverage arithmetic on an
  endogenous, growing debt path, iterating interest savings to
  consistency with the combined path (§5), then applied Sponsor
  Correction #2 (maturity-dependent τ) and the CBO reconciliation
  (§§6–7). The SFC §IX result from v2 (recycling the receipts flips
  the demand impulse positive at 81/81 grid points) is used only as a
  qualitative cross-check on the FRB/US direction — it is a
  one-period sign experiment and is **not** monetized anywhere in the
  fiscal tables.

**Fee contribution definition (consolidation).** Net fee receipts
(unified base, floating, central turnover, θ = 1.0, erosion 10%):
gross collections $4,625B; net at the skeleton path $3,650B; **net
after the v2 final pass's Regime C fee-path reconciliation $4,050B**;
less the Regime C endogenous FRB/US drag **−$2,667B** (carried as its
own line, as in v2); plus Δ Fed remittances **+$410B**; plus interest
savings computed on the combined debt path (§5). Where Lane 2's
in-model receipts differ (loan-only base; endogenous rate path),
the bases are reported side by side and never blended (§5.4).

---

## 2. Medicare for America, re-based (Lane 1)

### 2.1 Reproduction verdict

The v1 Lane J model (`mfa/mfa_model.py`, stdlib only) was re-run from
a pristine copy; the originals are unmodified (md5s unchanged) and
the re-run's outputs are **byte-identical** to the shipped v1 files.
Every stated headline reproduces to rounding. The v1 residuals are
therefore **verified as the model's own outputs** — which is all
"verified" means here: there is no official score to verify against.

Two discrepancies were found, both in the v1 *narrative*, not the
model: central gross cost in 2035/2036 is **$5.09T / $5.41T**, not
the $5.34T / $5.71T stated in RESULTS_MFA_V1.md §2 (window total
unaffected); the low-case LTSS total is **$0.775T**, not $0.7T.
Neither figure from the v1 text should be cited.

### 2.2 The financing identity and window totals (FY2028–36, $T)

Residual = Gross cost − Displaced federal outlays − Premiums −
Employer contributions − Title II revenues − State MOE ($0).

| Component | Low | Central | High-stress |
|---|---:|---:|---:|
| Gross MFA cost | 18.09 | 24.92 | 36.15 |
| − Displaced outlays (phased 2030/2033/2035) | 12.57 | 13.09 | 13.47 |
| − Premiums (§2204) | 1.35 | 1.93 | 2.61 |
| − Employer contributions (§125, from 2031) | 0.51 | 1.27 | 2.03 |
| − Title II revenues | 4.96 | 6.11 | 7.31 |
| − State MOE (§2209, bill as written) | 0.00 | 0.00 | 0.00 |
| **= RESIDUAL for the fee** | **−1.29** | **+2.52** | **+10.73** |

**Title II itemized (FY28–36, $T)** — the bill's own primary
financing, and the largest single offset:

| Component | Low | Central | High-stress | Status |
|---|---:|---:|---:|---|
| TCJA + P.L. 119-21 repeal (§201) | 3.20 | 3.90 | 4.60 | **ASSUMPTION — extension analogue**: from CBO/JCT estimates of *extending* the expiring TCJA provisions (~$4.6T deficit effect incl. interest); **not a JCT score of this bill** |
| Payroll add-on 0.9%→4% | 0.95 | 1.15 | 1.35 | Arithmetic on the Additional Medicare Tax base |
| NIIT 3.8%→6.9% | 0.38 | 0.47 | 0.56 | Arithmetic |
| 5% surtax >$500k | 0.22 | 0.30 | 0.40 | Arithmetic |
| Step-up repeal | 0.13 | 0.17 | 0.22 | Arithmetic |
| Excises + HSA termination | 0.08 | 0.12 | 0.18 | Arithmetic |
| **Total** | **4.96** | **6.11** | **7.31** | |

Gross-cost drivers (central): per-enrollee core cost anchored to CBO
per-capita spending by origin cohort, grown at 4.8%/yr, multiplied by
a §2205/§2206 rate factor (1.06), an induced-demand factor (1.07),
and a cost-sharing richness factor (1.05); plus dental/vision/hearing,
admin at 3%, the §2206(b)(4) Medicaid rate top-up 2028–33 ($0.22T),
and §124 waiting-list clearance ($35B). **HCBS long-term services —
the new ≥1-ADL entitlement — totals $0.78T / $2.00T / $5.12T across
scenarios and is the widest swing in the build** (a $3.4T range; the
least-anchored number in the model, since MFA's threshold has no
current-program counterpart). Central enrollment reaches 197M by
2036 (992M enrollee-years). The high-stress case stacks the top of
every range and is a bound, not a forecast.

### 2.3 Annual residual paths ($B) — the timing profile

| FY | Low | Central | High-stress |
|---|---:|---:|---:|
| 2028 | −282 | −236 | −108 |
| 2029 | −299 | −256 | −125 |
| 2030 | −36 | +252 | +779 |
| 2031 | −102 | +127 | +677 |
| 2032 | −93 | +197 | +866 |
| 2033 | −212 | +260 | +1,289 |
| 2034 | −243 | +296 | +1,510 |
| 2035 | −4 | +891 | +2,728 |
| 2036 | −18 | +993 | +3,116 |
| **Cumulative** | **−1,289** | **+2,524** | **+10,730** |

All scenarios run **negative residuals in 2028–29** (Title II is
already collecting; MFA is still the transitional option and nothing
is yet displaced). The central residual turns positive with the 2030
Medicare switch, its cumulative crosses zero during 2032, and **75%
of it lands in 2035–36** — the residual-Medicaid switch lifts gross
cost by more than the completed displacement offsets. The residual
the fee must cover is a **late-window** obligation; §5.3 tests the
fee's own (also back-loaded) phase-in against it year by year.

*Annualization assumption (Lane 1, labeled):* v1 carries Title II
only as window totals. Annual Title II paths were constructed by
growing each component at 4.2%/yr (v1's own payroll-growth parameter)
normalized to hit the verified window totals exactly, all components
in effect from FY2028 per §201's timing. A flat split instead would
shift ≤ ±$45B/yr and change neither the totals nor which years are
worst. Timing checks against the bill otherwise pass (employer
contributions from 2031; displacement 2030/2033/2035; MOE $0), with
two minor flags: §§202–210 component effective dates are undocumented
in v1, and the §124 waitlist clearance is spread 2028–30 rather than
the bill's literal 90 days (timing only).

---

## 3. How MFA enters FRB/US (Lane 2) — and what cannot be represented

FRB/US (933 variables) contains **no health variable at all**
(verified by name/definition search of `model.xml`). Each MFA flow
was assigned a documented carrier; the fee side is unchanged from
Lane B (wedges only on `rme`/`rcar`/`rbbb`, scaled by origination
coverage κ; receipts only via `ugfsrp`; closure dfpex=1, dfpdbt=0,
dfpsrp=0; `rff` never imposed; f = rff whole-path fixed point).

| MFA flow | Carrier | Treatment |
|---|---|---|
| Incremental federal outlays (gross − displaced = $11,832B central) | `egfe` exogenised at baseline + flow | Converted to 2012$ on the baseline deflator; the only exogenous final-demand carrier for government-financed services |
| Enrollee premiums ($1,932B) | `ugfsrp`, separately identified MFA component | Residual-receipts routing (Interface §2.2 rules out `tpn`/`tcin` entry); **demand-neutral in-model** |
| Employer contributions ($1,266B) | `ugfsrp`, separately identified | Same routing, same caveat |
| Title II revenues ($6,110B) | `ugfsrp`, separately identified | Same routing, same caveat — **the load-bearing one** |
| Displaced private premiums (~$0.72T cumulative: exchange gross net of PTC + 25% employee share of ESI gross) | `eco_aerr` growth-shift | Moves PCE toward baseline − displaced private premiums, preserving `eco`'s endogenous income response |
| Employer premium savings (~75% of ESI gross) | **No carrier — omitted, flagged** | Would enter wages/profits; no defensible route exists |

**Cannot be represented in FRB/US:** health-sector supply and
capacity constraints; premium and Title II *incidence* (all MFA
receipts are demand-neutral residual entries — the model sees the
spending but not the tax-side drag); LTSS as a distinct entitlement;
the §IX distributional interest-income channel; state MOE; Fed
remittances (carried in the consolidation layer only). Annual MFA
flows were converted to quarterly by FY-GDP-share allocation
(totals exact: Title II $6,110B central / $7,310B high; residuals
$2,523B / $10,730B — matching Lane 1; Lane 1's annual tables use a
4.2%-growth annualization instead — a within-window timing
convention difference only, reconciled in §5).

---

## 4. FRB/US combined runs (Lane 2)

All runs solved (MCE + VAR for MFA-only and Combined C; Combined B
and Combined C high-stress in MCE); fixed points converged in 6–8
iterations, post-sync |f − rff| ≤ 0.003pp. Headline: **MCE, β = 1.0,
loan-only fee basis** (Lane B's documented lower bound — the
consolidation in §5 carries the unified base).

| Run | rff = f, post-sync (%) | Fee receipts FY28–36 ($B) | Δsurplus FY28–36 ($B) | Δdebt held by public, 2036Q4 ($B) | Unemployment dev., 2036Q4 (pp) | GDP trough dev. (%) |
|---|---:|---:|---:|---:|---:|---:|
| Fee-only C (Lane B, reused) | 2.10 | 3,809 | +3,715 | −3,896 | **+0.77** | −1.72 |
| MFA-only (conventional policy) | 5.62 (rff) | — | −1,242 | +1,428 | −2.11 | −0.04 |
| **Combined C + MFA** | **3.70** | **6,628** | **+5,153** | **−5,313** | **−0.61** | −0.41 |
| Combined B + MFA (sensitivity) | 3.61 | 6,658 | +5,200 | −5,366 | −0.61 | −0.77 |
| Combined C + MFA, high-stress | 4.61 | 8,221 | **−1,514** | +1,823 | — | — |

**Does MFA lift the rule, the fee, and receipts? Yes — decisively,
in-model.** MFA-only drives the inertial Taylor rule +2.33pp above
baseline (funds level 5.62% vs 3.29%), because $11.8T of incremental
purchases enter demand while the offsetting receipts are
demand-neutral. The combined fixed point therefore re-solves with
the pair at **3.70% — +0.41pp above the conventional baseline**, not
below it — and cumulative receipts rise to $6,628B vs $3,809B
fee-only: **Δreceipts = +$2,819B (+74%)**. (VAR: fee 3.52%, receipts
$6,295B vs $4,340B, Δ = +$1,956B.) The combined Δsurplus exceeds the
sum of its parts (+$2,473B) by **+$2,680B of interaction**, almost
all of it the enlarged fee take at the MFA-lifted funds path.

**Does the spending closure shrink the fee's employment drag?
In-model, it more than offsets it.** Unemployment deviation at
2036Q4: **−0.61pp combined vs +0.77pp fee-only**; along the combined
MCE path the deviation never exceeds +0.01pp in any quarter, and the
GDP trough deviation shrinks from −1.72% to −0.41%. **This is the
sponsor's §IX intuition confirmed in direction by a second,
independent model — and it must be quoted with its caveat:** the
offset is measured under demand-neutral Title II routing. A run that
routed Title II through the model's tax equations (ruled out by the
interface assessment for contamination reasons) would show a smaller
offset; the honest statement is that the spending closure eliminates
the fee's *measured* employment drag in FRB/US, with the
tax-incidence channel unmodelled and working in the opposite
direction. The SFC §IX experiment — which *does* carry household
incidence — points the same way (recycling flips the impulse
positive at 81/81 points), which supports the direction but not the
FRB/US magnitude.

**The financing mix inverts under the closure.** Combined-run drag
decomposition: Δsurplus (+5,153) = fee receipts (+6,628) + MFA
receipts (+9,308) − incremental outlays (−11,832) + interest saving
(**+192 only**) + endogenous drag (**+856**, positive — the combined
economy runs at or above baseline employment, so endogenous revenues
add to the surplus). The interest-saving engine that powers the
banked-closure case nearly vanishes in-model, because the combined
funds path is *above* baseline; the receipts engine replaces it.
MFA-only shows the mirror image: its static residual cost (+$2,523B)
is overwhelmed by **+$3,547B of in-model interest** on the higher
funds path (Δsurplus −$1,242B). And **high-stress combined is not
financed in-model** (Δsurplus −$1,514B, debt +$1,823B) despite the
highest fee (4.61%) and receipts ($8,221B) of any run — the
procyclical receipts engine cannot outrun a $10.7T residual.

---

## 5. Consolidated financing arithmetic (Lanes 3–4)

### 5.1 Method

**Growing baseline debt path** (constructed, documented): no CBO
debt path existed in the project files, so the path is built from
CBO's February 2026 *Budget and Economic Outlook* anchors — deficits
$1,887B (FY2027) → $3,115B (FY2036), **$24.4T cumulative** — with
deficits interpolated geometrically and rescaled to sum to exactly
$24.4T. Marketable debt starts at the project's MSPD value
**$31,830B** (end-FY2026) and grows by each deficit × 0.9917 (the
marketable share of debt held by public), reaching **$56,029B** at
end-FY2036 (CBO's held-by-public endpoint: $56,152B). Coverage
concept as in v2 throughout: marketable debt only; savings counted
only on the non-Fed-held share (×0.8559); remittances on their own
line.

**Combined path, iterated to consistency.** For each (τ × scenario):
D_t = Baseline_t + cumResidual_t − cumNetReceipts_t − cumDragEffect_t
− cumRemittances_t − cumSavings_t, with interest savings the
**rate effect only** (plan average rate vs 3.57% baseline average
rate, × average combined debt × 0.8559) under bucket repricing (WAM
70 months; new-issue only). Rate-effect-only is what keeps the
ledger single: the debt-*level* effect of receipts and residuals is
already in the path. Savings ↔ path iterated until the maximum
annual savings change is < $0.05B (≤3 iterations in every cell).
One-ledger check: end-FY2036 combined debt at τ_long = 0.5/central
sits exactly the coverage margin below baseline.

### 5.2 Coverage surface — CORRECTED treatment (headline)

Maturity-dependent τ (§6): front end (33% of repricing exposure)
transmits in full by arbitrage; τ_long applies beyond 1 year only.
Growing path, spread change Δspread = 0, $B. Fee contribution =
net receipts 4,050 − drag 2,667 + remittances 410 + interest savings.

| τ_long | Interest (central) | Central margin | Low margin | High-stress margin |
|---|---:|---:|---:|---:|
| 0 | 909 | **+179** ✅ | +3,960 ✅ | −7,960 ❌ |
| 0.25 | 1,365 | **+634** ✅ | +4,400 ✅ | −7,470 ❌ |
| 0.5 | 1,816 | **+1,085** ✅ | +4,835 ✅ | −6,984 ❌ |
| 0.75 | 2,263 | **+1,532** ✅ | +5,267 ✅ | −6,503 ❌ |

Spread sensitivities never flip a verdict (central at τ_long = 0:
+$294B at Δspread = −0.25pp; +$109B at +0.15pp). The cumulative
ledger **never goes negative at any τ_long** (spread 0). Low is
financed in all 36 surface cells; high-stress in none.

**Superseded scalar-τ sensitivity** (Lane 3, same machinery, single
τ on all maturities): central margins −731 / −40 / +641 / +1,312 —
financed iff τ ≥ 0.5. Retained here only to make the correction's
size visible; it is not a co-headline.

**Flat-debt sensitivity** (v2's convention, scalar τ): central
margins −731 / −261 / +208 / +677. The growing path changes no
verdict on either treatment, but roughly triples the central
τ = 0.5 margin (+$208B → +$641B scalar) — the flat-stock convention
was worth **$221B (τ=0.25) / $433B (τ=0.5) / $635B (τ=0.75)** of
conservatism. The flat variant's fee-only totals reproduce v2's
$1,793 / 2,262 / 2,731 / 3,201B exactly.

### 5.3 Timing: annual shortfalls under the financed window

The window verdict assumes the banked-ledger closure (surpluses
carry across years), as the plan specifies. On a strict
pay-as-you-go reading the central case is **not** year-by-year
financed at any τ_long: annual margins are negative in **2030**
(−$45B scalar / −$10B corrected at τ = 0.5; the Medicare-switch year,
when the residual jumps before fee coverage matures) and in
**2035–36** (−$289B / −$326B scalar at τ = 0.5), covered under the
closure by the banked 2028–34 surplus (cumulative position peaks at
+$1,256B in 2034 on the scalar basis). High-stress shortfalls begin
in 2030 on both definitions. This is the arithmetic form of the
memo's §X warning: entitlement outlays are legal obligations on
their own schedule; fee receipts are not, and any real-world version
of this plan needs the banked ledger (or general-revenue bridging)
in 2030 and 2035–36 even where the window balances.

### 5.4 The FRB/US basis, side by side — not averaged

| | Consolidation (corrected, growing) | FRB/US combined (Lane 2) |
|---|---|---|
| Central-case bottom line | Margin **+179 (τ_long=0) … +1,085 (0.5) … +1,532 (0.75)** | Δsurplus **+$5,153B** (loan-only); ≈ **+$7.5T** after first-order unified scaling (×1.347) |
| Fee receipts basis | Unified, fee-only rate path held (ratio 1.1098) | Loan-only, rate path endogenous — receipts +74% |
| Interest line | $909–2,263B (maturity-dependent τ) | +$192B (funds path above baseline) |
| Drag | −$2,667B imposed (fee-only Regime C) | +$856B in-model (combined economy runs hot) |

Three mechanisms explain the divergence: **(1) receipts
endogeneity** — MFA lifts rff to 3.70%, enlarging the fee take by
+$2,819B; the consolidation holds the fee-only path. **(2) Drag
sign** — the consolidation imports the fee-only regime's −$2,667B
drag; the combined FRB/US economy runs at/above baseline employment
and its endogenous term is +$856B — a flip manufactured in part by
demand-neutral Title II routing. **(3) Interest runs opposite** —
the τ-surface books $0.9–2.3T of yield-decline savings; FRB/US,
whose combined path sits above baseline, books $192B. **Both bases
agree on low (financed) and high-stress (not financed).** On
central they now agree on the sign (financed) but not the margin:
the consolidation's thin +$179B at τ_long = 0 is the conservative
bound; the FRB/US figure is an upper bound inflated by unmodelled
tax incidence. Neither basis licenses treating the central margin
as settled to better than ±$1T.

### 5.5 Erosion of the interest line under the spending closure

Spending the savings raises the debt path relative to banking them,
which enlarges the repricing base (augmenting savings) while the
residual's own borrowing adds interest-bearing stock (eroding the
*net* position, already counted in the path). Net self-erosion of
the savings line itself is small: on the scalar basis, combined-path
savings at τ=0.5 central are $1,372B vs $1,397B on the growing
no-plan path — **erosion $26B (1.9%)**, reversing to −$78B
(augmentation) in high-stress, where MFA's added debt enlarges the
base most. On the corrected basis the same comparison is $1,816B
(combined) vs $1,858B (no-plan growing, §7) at τ_long = 0.5 —
**≈ $42B (~2%)**. The often-voiced objection that "you can't spend
the interest savings and still have them" is therefore wrong at the
first order for this plan's magnitudes — but note what does the
work: the erosion is small because the window's *cumulative* debt
difference is small relative to a $32–56T stock, not because the
channel is absent. It would grow with the residual (high-stress)
and with any extension of the window.

---

## 6. Sponsor Correction #2 — maturity-dependent τ (Lane 4)

**Premise (sponsor; verified in §8's exhibit).** The 3-month bill
rate and IORB are arbitrage-locked — bills and reserves are
near-perfect substitutes for the marginal holder — so applying a
scalar τ to front-end yields was wrong. **Treatment:** the repricing
exposure splits at the project's own maturity structure
(`share_maturing_1yr` = 0.33, WAM 70 months):

- **Front end (weight 0.33):** new-issue yield = IORB + spread;
  transmission **1 by arbitrage** — not an assumption and not
  estimated. The decline equals the full administered-path decline
  A_t (verified from the skeleton: 0 before FY2030, **1.95pp from
  FY2030** — Lane 3's 0.975pp headline at τ=0.5 was exactly half of
  it) adjusted by Δspread, the *change* in the bill–IORB spread vs
  baseline, a documented scenario parameter ∈ {−0.25, 0, +0.15}pp
  (observed range ≈ −0.40pp in the 2021 scarcity to +0.15–0.25pp in
  the 2026 surge). Headline Δspread = 0.
- **Long segment (weight 0.67):** dy = −τ_long × A_t, with
  τ_long ∈ {0, 0.25, 0.5, 0.75} — the expectations/term-premium
  transmission of a permanent regime, **unestimated**, relabeled
  everywhere (it is never again a whole-curve τ).

Each segment runs Lane 3's identical bucket recursion on its share
of the stock (exact under the recursion's linearity; split
additivity is test-asserted); the combined fixed point is iterated
as in §5.1.

**Corrected interest line** (combined closure, growing path,
spread 0, cumulative FY27–36, $B): central **909 / 1,365 / 1,816 /
2,263** at τ_long = 0 / 0.25 / 0.5 / 0.75 — vs scalar 0 / 690 /
1,372 / 2,043. **Front/long split at τ_long = 0.5 (central): front
$901B (49.6%) / long $915B (50.4%)** — the front-end third, which no
transmission parameter governs, contributes as much as the entire
long segment at τ_long = 0.5. The front line is nearly
τ_long-invariant ($866–978B across scenarios and the surface): a
floor under the interest line, not a surface.

**Restatement of the v2 verdict (flat/banked variant, spread 0):**

| τ_long | Interest: scalar → corrected | v2 total: scalar → corrected |
|---|---:|---:|
| 0 | 0 → **619** (front 619 + long 0) | 1,793 → **2,412** |
| 0.25 | 469 → **934** (619 + 314) | 2,262 → **2,727** |
| 0.5 | 939 → **1,248** (619 + 629) | 2,731 → **3,041** |
| 0.75 | 1,408 → **1,563** (619 + 943) | 3,201 → **3,355** |

**v2's interest-savings line is understated at every τ, because the
scalar haircut was applied to the front-end third of the stock.**
The understatement is largest where v2 looked weakest: at τ=0 v2
booked zero savings against $619B of arbitrage-locked front-end
savings on the flat stock ($909B growing). The correction also
narrows the v2 verdict's τ-spread from $1,408B to $943B — a third of
v2's apparent τ-sensitivity was front-end mispricing. (v2's $6T
verdict is unchanged in substance: the corrected banked totals,
$2,412–3,355B, remain a ~$2.4–3.4T-class benefit, and no corrected
cell approaches $6T.)

---

## 7. CBO rule-of-thumb reconciliation exhibit

CBO, *How Changes in Economic Conditions Might Affect the Federal
Budget: 2026 to 2036*: all interest rates 0.1pp higher each year →
deficits +$60B in 2036, **+$379B cumulative 2027–36** (symmetric for
lower rates) — i.e., ~$379B of net-interest saving per 0.1pp of
sustained curve decline. **This figure is used only as a comparator.
It appears nowhere in the coverage machinery (a guard test asserts
this in both consolidation lanes).** The rule *prices* a yield
decline; it does not produce one. (The v1 prototype's $3.79T/pp
plug-in, with an invented τ and gross-of-Fed accounting, was killed
by audit for exactly that error; this exhibit exists so the v2
mechanics can be priced against CBO's rule honestly, not to
re-import the plug-in.)

**Model figure, consistent definition** (per 0.1pp of the 0.975pp
headline decline at the τ=0.5 cell; interest only, consolidated):

| Treatment | Model $ per 0.1pp | Cumulative interest ($B) | Share of $283B gap closed |
|---|---:|---:|---:|
| v2 as booked (flat debt, scalar τ) | **96** (112 gross of Fed share) | 939 | — |
| + growing debt path | **143** | 1,397 | 17% |
| + maturity-dependent τ (Lane 4) | **191** | 1,858 (front 922 + long 936) | **33% total** |

**Wedge decomposition** (per 0.1pp, τ=0.5 basis; CBO 379 → model 96
as booked):

| Wedge | Size | Note |
|---|---|---|
| (b) **Repricing path** — largest | realization share **35%** | WAM 70 months, new-issue only, dy = 0 until FY2030 (the administered paths diverge only then). Instant full repricing of the flat stock at 0.975pp for 10 years would book $2,656B consolidated; the model books $939B. Effective average decline realized: **0.34pp**, not 0.975pp |
| (d) **Coverage** | ≈ −$78B/0.1pp (pro-rata attribution, upper bound) | Model prices marketable debt only ($31,830B of $40,100B total = 79%); CBO's net-interest concept spans the whole federal balance sheet incl. new baseline borrowing's own interest. Part of CBO's wider base is intragovernmental and nets out in consolidation |
| (c) **Debt growth + compounding** | +$47B/0.1pp of model figure | Re-running the interest line on the growing path (no MFA) raises savings $939B → $1,397B; CBO's figure also embeds borrow-to-pay-interest compounding on a growing stock, which the flat skeleton omits by construction |
| (a) **Fed-held share / consolidation** | −$16B/0.1pp on the interest line | Savings counted only on the non-Fed-held share (gross $1,097B → consolidated $939B, −$158B window). Partly returned on a separate ledger line: **Δ remittances +$410B** — the IORB-expense channel, not portfolio-yield pass-through, and not part of the $96B |

The wedges are not strictly additive ((b) and (c) interact), and the
table prices each on the model's own arithmetic where a run exists.
**Bottom line:** the model's $96B vs CBO's $379B was never a
contradiction — roughly a third of the gap is repricing realization,
a sixth is debt growth, and the rest is deliberate consolidation and
coverage choices. After both sponsor corrections the model stands
at $191B per 0.1pp — half of CBO's rule — with the remaining
difference identified item by item above.

---

## 8. Empirical exhibit — IORB/IOER vs the 3-month bill (Lane 4)

Data route (i) **succeeded**: FRED fredgraph CSVs (IOER, IORB, DTB3)
fetched 2026-11-22 and saved (`exhibit_data/`); every statistic
below is computed by `exhibit_stats.py` from those files — nothing
is fabricated, and routes (ii)/(iii) were not needed. Merged daily
sample: **4,529 trading days, 2008-10-09 → 2026-11-19** (administered
rate = IOER to 2021-07-28, IORB from 2021-07-29).

- **Full sample: levels correlation 0.995; pass-through β (OLS of
  bill rate on administered rate, levels) = 1.009.**
- **Era β (levels):** 2016–19 hikes **1.11** (ρ 0.989); 2022–24
  hikes **0.89** (ρ 0.990); easing (Sep 2024–present) **0.69**
  (ρ 0.933); Covid ZLB **0.45** (ρ 0.645 — bill scarcity dominates at
  the floor); 2008–15 ZLB **not identified** (administered rate
  pinned at 0.25%; reported as n/a, not regressed).
- **Event windows** (39 administered-rate changes): narrow
  [t−1, t+5] β = 0.11 — bills *anticipate* administered changes, so
  the action precedes the event date; anticipation-inclusive
  [t−20, t+5] β = **0.87**, consistent with the NY Fed event-study
  finding of ~complete pass-through of administered-rate changes to
  money-market rates (Dec 2015–Jun 2023).
- **Spread (bill − administered):** full-sample mean **−10.8bp**,
  median −14.0bp; 2022–24 hikes mean +2.8bp (SD 27.5bp);
  **2026-11-19: +26bp (IORB 3.90%, DTB3 4.16%)** — the sponsor's
  observation confirmed in the fetched data, and inside the model's
  {−0.25, 0, +0.15}pp spread-change scenario range.

The exhibit supports the correction's premise: outside ZLB/scarcity
episodes, the bill rate tracks the administered rate essentially
one-for-one. It does **not** support extending τ=1 beyond the front
end — the exhibit prices bills only, and says nothing about the
long segment, where τ_long remains unestimated.

---

## 9. Critical assessment — where the combined plan's arithmetic is fragile

1. **Title II's demand incidence is unmodelled, and it is the
   largest single threat to the FRB/US basis.** $6.11T of tax
   increases (central) enter FRB/US as demand-neutral residual
   receipts because the model has no incidence carrier the interface
   discipline permits. Every FRB/US combined number — the +74%
   receipts endogeneity, the −0.61pp unemployment deviation, the
   +$5,153B Δsurplus — is therefore an upper bound on the demand
   side. The consolidation basis avoids this by holding the fee-only
   rate path, but pays for it by construction: it cannot see the
   receipts endogeneity at all. The truth for the central margin
   lies between +$179B (consolidation, τ_long = 0) and ≈ +$7.5T
   (FRB/US, unified-scaled), and the width of that interval is
   itself the finding: **the central case is financed on both
   bases, but no existing run pins its margin.**

2. **MFA cost uncertainty dominates everything downstream.** There
   is no official score. The residual's range (−$1.29T to +$10.73T)
   is wider than the entire fee contribution. Three named drivers:
   (a) the **TCJA/P.L. 119-21 repeal analogue** ($3.9T central) is
   an analogy to extension estimates, not a JCT score of repeal —
   and repealing P.L. 119-21 would also restore that law's
   health-spending cuts, raising the Medicaid baseline and hence
   displaced outlays in 2033–35 (flagged in v1, still unmodelled);
   (b) the **LTSS entitlement** ($0.78T / $2.00T / $5.12T) — a
   ±$2.3T one-at-a-time swing on the central residual, resting on a
   ≥1-ADL threshold with no current-program counterpart and on
   HCBS labor supply materializing; (c) **induced demand / woodwork**
   (factor 1.00 / 1.07 / 1.15, a ±$1.5T swing), applied uniformly in
   v1 including to the already-insured Medicare cohort (likely
   overstated there) and possibly understated for the uninsured
   cohort's pent-up demand. If (b) and (c) land at the top of their
   ranges together, no fee setting finances the bill — that is
   precisely the high-stress case.

3. **τ_long remains unestimated — but the correction demoted it.**
   After Correction #2, τ_long no longer decides the central
   verdict in the consolidation basis (financed even at τ_long = 0);
   it still decides the *margin* (±$1.35T across the surface) and
   it fully decides the scalar-basis reading. Nothing in the
   literature estimates the long-segment transmission of a
   *permanent* halved administered path under a fee regime; the
   surface presentation is the honest maximum.

4. **Fee-scale pass-through is uncalibrated.** FRB/US runs use
   β = 1.0 headline (Lane B's grid: β ∈ {0.5, 0.75, 1.0}); the
   empirical levy literature disciplines pass-through only up to
   ~45bp of burden, not the ~200bp synchronized fee. Lower β in
   Lane B paradoxically *raised* receipts (via the f = rff fixed
   point) while worsening borrower incidence — a regime property,
   not a free lunch, and it is not stress-tested in the combined
   runs beyond Lane B's fee-only grid.

5. **Procyclical receipts vs countercyclical health outlays.** The
   fee is chained to IORB: in v2's recession regime it collapses to
   ≈0.11% at the trough and cumulative receipts fall by ~half.
   Health outlays do the opposite. This study's runs are all
   no-shock paths; a recession landing in 2030 or 2035–36 — the
   annual-shortfall years — would open a cash gap the banked ledger
   covers only if the surplus was actually banked in the fat years.
   The memo's §X separation (appropriation not capped by receipts)
   is not a drafting nicety; it is what keeps a rate cut from
   becoming a benefits cut.

6. **Timing mismatch is structural, not incidental.** Fee coverage
   reaches only 19.5% of the unified base in FY2028 (grandfathering)
   while MFA's gross cost is already $383B (central) that year; the
   residual's worst years (2035–36) arrive when displacement is
   complete but the residual-Medicaid switch peaks. Both sides are
   back-loaded, but not in the same years: the plan runs annual
   deficits in 2030 and 2035–36 inside a financed window (§5.3).

7. **The drag import is a modeling seam.** The consolidation
   carries Lane B's fee-only Regime C drag (−$2,667B) unchanged
   into the combined ledger, while Lane 2 shows the combined
   economy's endogenous term flipping to +$856B. The consolidation
   number is therefore conservative in a specific, named way — but
   the seam means the headline margin is not any single model's
   output; it is a ledger assembly with one deliberately
   conservative import, disclosed here rather than smoothed over.

8. **Secondary seams.** Title II annualization (Lane 1's 4.2%
   growth vs Lane 2's GDP-share allocation — totals identical,
   within-year timing differs by ≤ ±$45B/yr); the growing debt path
   is constructed from CBO endpoint anchors, not CBO's own annual
   series; displaced private premiums are only partially carried in
   FRB/US (employer savings omitted); the SFC layer was not re-run
   for the combined closure (its §IX sign result is used
   qualitatively only, as instructed).

## 10. Limitations

- All results are simulations from this project's models (FRB/US
  via PyFRB/US, the cohort/consolidation skeleton, the v1 MFA
  construction). **None is a Fed, CBO, JCT, or CMS forecast**, and
  no official score of H.R.10924 or of the fee exists.
- FRB/US Design E is the conservative end of the rule-response
  interval (outcome-reactive inertial rule); a stance-targeting
  FOMC would offset more of the fee. MCE is the headline; VAR is
  robustness, and VAR combined receipts endogeneity is smaller
  (+$1,956B vs +$2,819B).
- The consolidation's repricing skeleton (bucket shares, WAM 70
  months, 3.57% baseline average rate) is a stylization of the
  actual Treasury maturity structure, not the structure itself.
- Behavioral responses outside the models — loan↔bond substitution
  (the unified base forecloses the statutory margin; elasticities
  remain uncalibrated), offshore migration of credit, provider
  capacity responses to MFA rates, state behavior under §2209's
  post-window MOE — are flagged in the lane reports and carried as
  caveats, not parameters.
- Windows differ by construction and are kept distinct: MFA
  residuals are FY2028–36 (the bill's own start); fee and coverage
  ledgers are FY2027–36 (FY2027 fee flows are zero by construction).

## Appendix — files, code, tests

Lane reports (detail behind every section): `v2/mfa_combined/`
— `MFA_REBASE.md` (Lane 1), `COMBINED_FRBUS.md` (Lane 2),
`CONSOLIDATION.md` (Lane 3), `CORRECTION_TAU_MATURITY.md` and
`tau_maturity_exhibit.md` (Lane 4). Code: `mfa_model.py` /
`mfa_model_annual.py`; `v2/frbus/combined_runs.py`;
`consolidation_combined.py` / `run_combined.py`;
`consolidation_tau_maturity.py` / `run_tau_maturity.py`;
`exhibit_stats.py`. Data: `mfa_rebased_annual.csv`,
`coverage_surface.csv`, `coverage_surface_corrected.csv`,
`coverage_annual_{growing,flat,corrected}.csv`,
`combined_summary.json`, `corrected_summary.json`,
`cbo_reconciliation.json`, `exhibit_stats.json`,
`exhibit_data/fred_{IOER,IORB,DTB3}.csv`,
`v2/frbus/combined_outputs/` (path CSVs, metrics, run log).
All code is copied to `repo/v2/mfa_combined/`. v1 and v2 originals
are unmodified by this study (the two v1 narrative errors in §2.1
are corrected here by note, not by editing the v1 file).
