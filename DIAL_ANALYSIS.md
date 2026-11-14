# Lane K — Fed Dial Identification Analysis (Monetary Symmetry Fee)

**Question 1 of the project:** Congress authorises the Federal Reserve to set a
public-credit-capture share **s ∈ [50%, 90%]**, with statutory fee
`f = IORB · s/(1−s)` on covered newly-originated loan principal, the Fed
pursuing **maximum employment and price stability only — no revenue
objective**. Where would the Fed actually set s?

**Evidence base:** prototype audit (`audit/PROTOTYPE_AUDIT.md`, Lane A);
FRB/US scenarios (`integration/FRBUS_SCENARIOS.md`, Lane G, building on
Lanes B/D); SFC income-flow channel (`repo/FLOW_CHANNEL.md` +
`repo/results/flow_channel_v1.csv`, Lane H); fiscal Monte Carlo
(`repo/MONTECARLO_V2.md`, Lane I). Cross-reference: MFA residual
(`mfa/RESULTS_MFA_V1.md`, Lane J).

---

## VERDICT (up front)

**The dial is NOT point-identified by the dual mandate.** This is proved
below, not asserted, in three independent ways:

1. **In the prototype** the dial was movable only through invented,
   sign-ambiguous priors (audit §3.3): with all-in borrower cost held
   fixed, s entered the loss only via `gamma_pi`/`gamma_u`, centred at
   −0.025/+0.010 with the *perverse* average sign, only 41% of paths
   drawing the conventional sign, corr(γ_π, dial) = 0.10. The reported
   57.1% is the mean of a bimodal prior-mass distribution whose median,
   mode and modal path are all the 50% floor (§8 corrects it).
2. **In FRB/US** the (π, u) loss either ranks s *adversely* (at fixed
   all-in borrower cost, higher s is strictly less potent and strictly
   higher-loss — §3.1) or does not rank s *at all* (once the episode is
   rescaled to equal macro effect, the loss is equal by construction —
   §3.2). Neither case yields an interior optimum at 57%, 75%, or
   anywhere else. The ranking, where one exists, must be imported from
   **outside** the (π, u) loss: borrower-cost level, the income-flow
   channel, distribution, financial stability, instrument risk.
3. **The omitted flow channel can overturn the FRB/US ranking, but only
   at regime scaling and only under one Treasury use of the receipts**
   (§2b). At FOMC episode scaling (1–3 years) it narrows the potency gap
   by ~5–40% without reversing it. A channel whose sign and size depend
   on the Fed's horizon and on Congress's fiscal choice cannot pin down
   a mandate-driven dial either.

**Defensible forecast (institutional, §5): a newly authorised Fed
plausibly starts at the 50% floor and holds it through its first policy
episodes** — scenario (i) — **with scenario (ii), a slow evidence-
contingent drift upward, the plausible medium-run path.** A rule-based
high share (iii) is the least plausible: it would require importing a
fiscal or quasi-fiscal objective the statute's mandate framing excludes.

**Fiscal consequence:** at the forecast case (s = 50% sustained), the
Monte Carlo v2 combined FY2027–36 total is **mean $4.26T (median $4.22T,
p10–p90 $3.32–5.24T), and the $6T hypothesis fails** (prior mass ≥ $6T:
1.7%). **$6T requires the Fed to choose and sustain s ≥ 75%** (mean
$6.47T, 63.2% prior mass at 75%; $7.86T, 90.1% at 90%) — **a choice the
dual mandate alone does not compel on any channel decomposition this
project has produced.** (Distinct test, §7.2: against Lane J's *central*
MFA residual of +$2.52T, even the 50% case covers — $6T failing and MFA
central-case financing failing are not the same statement.)

---

## 1. What identification would require

For the dual mandate to *determine* s, three conditions must hold
simultaneously:

- **(I1) Differential transmission:** changing s at a given stance must
  change (π, u) outcomes. If s were a pure relabelling of who receives
  the borrower's payment, the loss would be flat in s and *any* s would
  be "optimal."
- **(I2) A signed, sized trade-off:** the differential effect must not be
  uniformly dominated — there must be something higher s does *better*
  on (π, u) to offset what it does worse, else the optimum is a corner
  (the floor), which is a bound, not an identified interior choice.
- **(I3) Stability of the ranking** to the parameters nobody can
  estimate ex ante (pass-through β, yield transmission τ, creditor MPC,
  Treasury's use of receipts). A ranking that flips when τ moves inside
  its plausible range is not identification a policymaker can use.

The prototype satisfied none of these (its differential transmission was
an invented coin-flip). FRB/US satisfies I1 genuinely — the split is
*not* neutral there — but fails I2 in the price channel (higher s is
uniformly weaker, §2a) and fails I3 once the flow channel is admitted
(§2b). The institutional forecast in §5 is therefore a forecast about
behaviour under non-identification, not a disguised optimum.

---

## 2. Channel decomposition

### 2a. Price / term-structure channel (FRB/US) — pressure: toward the FLOOR

Lane G, +100 bp desired tightening for 8 quarters, equal all-in borrower
cost increment q = +1.00 pp, β = 0.88, fiscal closure neutralised
(`dfpex=1, dfpdbt=0, dfpsrp=0`), wedge exogenised on `rcar`/`rbbb` only:

| Scenario | Δrff / wedge (pp) | xgdp trough | lur peak | picxfe min* | Potency vs conventional |
|---|---|---|---|---|---|
| Conventional | 1.000 / 0 | −1.190% | +0.624 pp | −0.104 pp | 100% |
| s = 50% | 0.532 / 0.468 | −0.726% | +0.377 pp | −0.061 pp | **61.0%** |
| s = 75% | 0.275 / 0.725 | −0.541% | +0.272 pp | −0.046 pp | **45.5%** |
| s = 90% | 0.112 / 0.888 | −0.424% | +0.215 pp | −0.037 pp | **35.6%** |

*picxfe minima are window-censored (still declining at 2032Q4); at the
matched 2029Q1 date the fee runs are weaker still (s = 75%: 33% of
conventional).

Mechanism: realised `rcar`/`rbbb` rise *more* in the fee runs, but
`rg10` rises far less (s = 75%: +0.109 vs +0.399 pp mean over the
episode), because only the funds-rate component moves the Treasury
curve, and in FRB/US that channel carries roughly half or more of a
tightening's effect. **Within this channel, higher s is uniformly
dominated: less disinflation and less slack per unit of borrower cost.
Pressure on the loss-minimising s: monotonically toward the floor.**
Sign does not depend on any free parameter inside FRB/US (β = 0.70
sensitivity is *more* contractionary at s = 75%, 48.4%, because lower
pass-through forces a larger funds-rate share — second-order).

Scope limit, stated once and carried throughout: this is FRB/US's
channel structure. The model contains no bank, loan stock, mortgage,
reserve or IORB variable among its 933 equations; the wedge reaches only
auto/BBB-type rates. It is a measurement of the term-structure channel,
not of the real fee's full transmission — which is exactly why §2b–2c
exist.

### 2b. Income-flow channel (SFC ledger) — pressure: depends on scaling AND on Treasury's use

FRB/US structurally omits the channel Carlos identified: conventional
tightening *injects* interest income into the private sector (baseline
consolidated government→private net interest injection: $1.16T/yr in
2027 rising to $1.65T/yr in 2036 — of which the IORB-to-banks leg is
only ~$0.09–0.12T/yr; **coupons to public holders dominate ~10:1**),
while the fee regime *removes* income: at equal borrower cost, lenders'
net loss equals the net fee exactly, and the government's interest
saving is the private sector's lost injection, dollar for dollar
(zero-sum flow table, tested every year; Lane H §1). At s = 75%,
β = 0.88, the 10-year private income removed under deficit-reduction
use is $6.71T — identically the fiscal combined total. **The $6T
benefit and the potency correction are the same dollars.**

Two technical qualifications from Lane H that discipline the intuition:

- The *reserve-stock drain* itself is settlement timing: a collected,
  unspent fee moves reserves into the TGA one-for-one and spending
  reverses it; in the ample-reserves floor system the Fed supplies
  reserves elastically at IORB, so the drain does not mechanically
  tighten lending as it would have pre-2008. The demand-relevant object
  is the **income flow**, not the reserve stock. (This qualifies the
  reserve half of the original critique; the income half is the bigger
  number and survives intact.)
- Cash ≠ accrual at the Fed: at s = 75% the accrual improvement first
  pays down the deferred asset, so cash remittances are unchanged in
  2029 and run +$0.05–0.10T/yr higher only thereafter.

Demand translation (creditor/interest-recipient MPC 0.10–0.40,
multiplier 1.0–1.5, foreign holders' ~30% of the coupon term excluded —
labelled Lane H assumptions; range tops stack highest MPC × highest
multiplier and are bounds, not centrals). **The two scalings are kept
separate; averaging them would be a category error, because they answer
different questions.**

**Episode scaling** (Lane G's +100 bp / 8 quarters; computed at s = 75%
only; per episode-year, fee regime minus conventional, variant (i)
deficit-reduction use):

| Book basis | Additional GDP effect |
|---|---|
| Contemporaneous (2027–28) book | −0.02 to −0.11 %/yr |
| Mature (2032) book | −0.03 to −0.26 %/yr |

Against the FRB/US episode gap at s = 75% (conventional xgdp trough
−1.190% vs split −0.541%, gap 0.649 pp), this **narrows the gap by
roughly 5–40% and does not reverse it** anywhere inside the MPC ×
multiplier ranges (reversal would require creditor MPC ≈ 1). The fee
book is simply too young in an 8-quarter episode: grandfathering means
most principal pays no increment yet (only floating vintages and new
originations reprice; assumed affected share 0.40–0.60 even on the
mature book). **Episode-scale pressure on s: mildly toward the ceiling
(it partially refunds the price channel's penalty on high s), nowhere
near enough to change the §2a ranking.**

**Regime scaling** (permanent fee at the baseline stance, variant (i)
deficit-reduction use; additional GDP effect of the fee regime vs
conventional, % of GDP):

| s | 2030 | 2033 | 2036 |
|---|---|---|---|
| 50% | −0.10 to −0.59 | −0.13 to −0.81 | −0.15 to −0.90 |
| 75% | −0.15 to −0.91 | −0.20 to −1.20 | −0.22 to −1.34 |
| 90% | −0.19 to −1.11 | −0.24 to −1.44 | −0.27 to −1.60 |

(Lane H CSV; MC v2 §6's sampled version at s = 75% — 2030–36 mean
annual effect −0.59% of GDP, p10–p90 −0.93 to −0.28 — sits inside these
bounds, as it must.)

By the mid-2030s the regime flow effect (−0.2 to −1.3 pp of GDP/yr at
s = 75%) is the **same order as, or larger than, the entire FRB/US
episode gap** — so at regime scaling the combined ranking **plausibly
reverses**: a permanent high-s regime, receipts used for deficit
reduction, may be *more* contractionary in total than the conventional
regime it replaces, not less. **Regime-scale pressure on s (deficit-
reduction use): toward the ceiling.** But note what "reversal" means for
identification: it does not produce an interior optimum either — it
flips which corner the combined loss prefers, on the strength of
unestimated MPCs, a placeholder τ, and a fiscal-use assumption.

**Treasury use flips the sign.** Under variant (ii) — the fee spent on
Medicare for America benefits, which is this project's own design —
the net fee returns to recipients with MPC 0.60–0.90 instead of
creditors' 0.10–0.40, and the fee term becomes a redistribution *gain*:
regime effect at s = 75% is **+0.09 to +1.34% of GDP in 2030, +0.13 to
+1.97% in 2036** (more expansionary than conventional); only the
interest-injection removal (E_i + E_p) remains contractionary. Under
the project's intended use, therefore, the flow channel **reinforces**
the price channel's pressure toward the floor: at fixed borrower cost a
high-s tightening is weaker on both channels, and the Fed must impose
still-higher all-in costs to hit its targets. Under variant (iii) (TGA
accumulation) the flow term is timing only — no demand effect.

Parameters the sign/size depend on, explicitly: **Treasury use of
receipts** (Congress's choice, not the Fed's — the Fed takes the fiscal
stance as given, so the *operative* flow channel for a Fed decision is
whichever use is legislated); **creditor MPC** (reversal at episode
scale needs ≈ 1, far outside the 0.10–0.40 range); **τ** (the coupon
leg E_p is exactly linear in τ: $0 at τ = 0 → $4.19T/10yr at τ = 1 vs
$1.34T at the placeholder τ = 0.32, s = 75%); **book maturity**
(grandfathering makes the channel grow ~with the taxable book, which is
why episode ≠ regime).

### 2c. Channels neither model captures

**(1) Bank profitability and capital.** Lower IORB removes bank income
on ~$3T of reserves (E_i = $0.35/0.55/0.68T over 10 years at
s = 50/75/90%), but banks' funding costs also fall with the policy rate
(deposit betas < 1 typically *widen* margins as rates fall from high
levels, compress them near the floor). The fee side cuts the other way:
the lender legally remits the fee, and to the extent pass-through is
incomplete (β < 1), the lender absorbs (1−β)·f — a margin squeeze that
grows with s and falls disproportionately on bank (vs nonbank) lenders.
Net sign for bank capital is genuinely **ambiguous**; the financial-
stability *risk* term, however, is asymmetric — a novel levy of up to
~3–6% of principal (prototype's observed max fee 6.35%) interacting with
bank capital is a tail risk a stability-conscious Fed prices even if the
mean effect is unclear. The prototype capped this entire channel at
0.20 pp of unemployment by assumption (audit §3.5) — a favourable cap,
not a measurement. **Pressure: ambiguous on means, toward the floor on
risk.**

**(2) Borrower composition — the fee taxes the margin, IORB taxes the
stock.** Because of grandfathering, the fee falls only on *new*
borrowers and floating-rate resets: new homebuyers, expanding firms,
revolver-dependent households — the marginal credit formation of the
economy. IORB, by contrast, reprices the entire reserve stock instantly
and, through the curve, much of the existing floating-rate stock. Three
consequences. (a) *Speed:* the fee is a slow instrument — the taxable
book reaches only ~78% of the eligible book by 2036 (prototype cohort
arithmetic; fixed point ~88%) — badly matched to 1–3-year FOMC episodes,
for which the funds rate remains the workhorse at any s. (b) *Potency
per dollar:* marginal borrowers are more rate-sensitive and higher-MPC
than the average creditor/debtor pair in §2b, so the demand effect per
dollar of fee could exceed the average-MPC translation — a HANK-type
effect neither FRB/US (representative transmission) nor the SFC flow
table (average MPCs) captures; direction for *potency* is toward
stronger fee transmission, hence mildly toward the ceiling, but it is
unquantified anywhere in this project (the sequence-Jacobian cross-check
was scoped, never run). (c) *Distribution:* concentrating the stance on
new borrowers while insulating incumbent fixed-rate borrowers is a
visible, cohort-skewed incidence (younger, lower-wealth borrowers pay;
existing homeowners don't) that a committee will hear about — political-
economy pressure toward the floor, and a financial-stability question
(concentrated burdens on the marginal borrowers most likely to default)
pointing the same way. **Net pressure: ambiguous on potency, toward the
floor on speed, distribution and default concentration.**

**(3) Avoidance and substitution, growing over time.** The fee is
avoidable in ways IORB is not: nonbank and foreign lenders, corporate
bond/CP issuance substituting for loans, securitisation structuring,
product redesign. Avoidance grows with f — hence, at a given stance,
with s — and compounds over the regime horizon as market structure
adapts (the historical pattern for every narrow-base financial levy).
Consequences: the covered base and the fee's potency both decay fastest
exactly where s is highest; activity migrates toward the less-regulated
perimeter (a stability cost); and long-run revenue at high s is lower
than static-book arithmetic suggests. In MC v2 the avoidance prior
already carries a standardised sensitivity of −0.21 (s = 50%) to −0.37
(s = 90%) on the combined total — the largest behavioural coefficient at
the ceiling. **Pressure: toward the floor, strengthening with horizon.**
Its size depends on the avoidance elasticity — invented in the prototype
(0.065/pp), carried as a labelled prior in MC v2, estimated nowhere.

**(4) Easing asymmetry / ZLB geometry.** The algebra `f = IORB·s/(1−s)`
with the stance held by construction solves IORB *down* as s rises: at
a ~3.2% desired stance the prototype's fixed-90% regime runs IORB at
~0.35% (94% of path-years below 0.50%). A high-s Fed therefore holds
almost no conventional easing space: in a downturn its fast, broad
instrument is already at the floor, and cutting the fee reaches only
new/floating borrowers, slowly. The option value of keeping IORB away
from the bound is a real, mandate-relevant cost of high s that no
( π, u ) loss computed on a *tightening* episode will ever show.
**Pressure: toward the floor.**

### 2d. Decomposition summary

| Channel | Scaling / condition | Pressure on loss-minimising s | Depends on |
|---|---|---|---|
| Price / term structure (FRB/US) | Episode, any use | **Floor** (monotone) | FRB/US channel structure; β second-order |
| Income flow (SFC) | Episode, deficit-reduction | Ceiling, weakly (closes 5–40% of gap) | Creditor MPC (reversal needs ≈1), book maturity |
| Income flow (SFC) | Regime, deficit-reduction | **Ceiling** (ranking plausibly reverses) | MPC, τ (linear), horizon |
| Income flow (SFC) | Regime, spent on MFA (project design) | **Floor** (sign flips: +0.1 to +2.0% GDP by 2036) | Recipient vs creditor MPC gap |
| Income flow | TGA only | None (timing) | — |
| Bank capital / stability | Any | Ambiguous mean; **floor** on tail risk | (1−β), bank share of covered lending |
| Borrower composition | Episode | **Floor** (speed); ceiling on unquantified HANK potency | Cohort turnover, marginal-borrower MPC |
| Avoidance / substitution | Regime, growing | **Floor** | Avoidance elasticity (unestimated) |
| ZLB / easing option value | Downturn states | **Floor** | Distance of solved IORB from bound |

No row produces an interior optimum. The rows disagree about *which
corner* under *which conditions* — that disagreement, with its
conditions stated, is the complete answer the economics gives.

---

## 3. The Fed loss exercise

Transparent quadratic loss `L = (π − π*)² + λ(u − u*)²`, evaluated on
Lane G's FRB/US responses for the representative episode (+100 bp
conventional-equivalent disinflation, 8 quarters). (λ is left symbolic:
no ranking below depends on it, which is itself part of the result —
contrast the prototype, where the hard-coded 1.6 did quiet work among
invented terms, audit §3.2.)

### 3.1 At fixed all-in borrower cost, the loss ranks s — adversely

Holding q = +1.00 pp for every scenario, the (π, u) deviations shrink
monotonically in s (§2a table: xgdp −0.726/−0.541/−0.424%; lur
+0.377/+0.272/+0.215 pp; picxfe at the matched 2029Q1 date −0.043/
−0.026/−0.014 pp vs conventional −0.077 pp). For any λ ≥ 0, each fee
scenario's loss exceeds conventional's, and loss increases in s. **The
(π, u) loss, fed FRB/US responses at fixed cost, selects the floor of
the authorised range (and would select conventional policy over the
whole fee family).** Adding §2b: at episode scaling the flow channel
offsets 5–40% of that penalty — it does not change the ordering within
the stated MPC ranges under deficit-reduction use, and under the
project's spent-on-MFA use it widens the penalty. Only at regime scaling
under deficit-reduction use could the ordering flip — a statement about
a permanent regime's demand drag, not about an FOMC episode decision.

### 3.2 Equal-effect rescaling — and why the loss then cannot rank s

What all-in cost would each s need to *match* conventional's episode?
Lane G converged this exactly at s = 75%; the 50% and 90% rows are
**factor-based inference** (scale = 1/potency factor, β = 0.88,
`Δrff = q/(1+βk)`, `f_inc = k·Δrff`), validated by the 75% case:
factor inference gives scale 2.20 vs Lane G's actually-converged 2.237
(1.7% error), and the lur/picxfe factors bracket the xgdp factor at
every s (scale ranges across the three target variables: 1.64–1.71 at
50%; 2.20–2.29 at 75%; 2.81–2.91 at 90%).

| Scenario | Scale | All-in cost q (pp) | Δrff (pp) | Incremental fee f_inc (pp of principal) | Wedge (pp) |
|---|---|---|---|---|---|
| Conventional | 1.00 | 1.000 | 1.000 | — | 0 |
| s = 50% | 1.64 | 1.639 | 0.872 | 0.872 | 0.767 |
| s = 75% | 2.24 (converged) | 2.237 | 0.614 | 1.843 | 1.622 |
| s = 90% | 2.81 | 2.809 | 0.315 | 2.834 | 2.494 |

At these rescaled costs the macro outcomes match broadly, not just at
the targeted trough (s = 75% converged run: lur peak +0.597 vs +0.624 pp
conventional; picxfe min −0.101 vs −0.104 pp; xgdp at 2032Q4 −0.834% vs
−0.860%). **Therefore the (π, u) loss at equal effect is equal across s
— by construction, up to second-order timing differences (the fee runs
disinflate later and catch up through persistent slack; at matched early
dates their inflation response is weaker still, which if anything makes
the rescaled loss at high s slightly *worse* on a forward-looking loss
that penalises early misses).** This is the rigorous form of the
identification problem:

> **Once the Fed is free to resize the episode — which it is — the dual-
> mandate loss is (approximately) flat in s along the equal-effect
> locus. Whatever ranks s must come from outside the loss: the level of
> borrower costs itself (borrowers pay 1.64×/2.24×/2.81× the all-in cost
> for the same macro outcome — a real welfare and distribution cost
> FRB/US's loss does not contain), the flow channel (§2b), stability and
> avoidance (§2c), and instrument risk (§5). A model that reports an
> interior "optimal s" from a (π, u) loss alone has smuggled one of
> those outside terms in — in the prototype's case, the γ priors and the
> mis-unit-ed risk/inertia add-ons (audit §§3.3–3.4).**

One more asymmetry the table makes concrete: equal effect at s = 90%
requires an incremental fee of **2.83% of covered principal for a single
100 bp-equivalent episode** — on top of the standing fee the regime
already charges. The borrower-cost bill for mandate-equivalent policy
grows convexly in s (k = s/(1−s) = 1, 3, 9). Even if a committee were
indifferent on (π, u), "same disinflation, nearly triple the private
cost" is a sentence no central bank chooses voluntarily without a
reason outside its mandate.

---

## 4. Combined potency comparison (the honest version)

Per s, at equal all-in borrower cost, episode horizon (the FOMC's
operating horizon), deficit-reduction use — FRB/US price potency plus
flow-channel offset, expressed against the conventional = 100%
benchmark using the s = 75% flow computation as the only directly
computed flow row (episode flow was computed at s = 75% only; other rows
inherit §2a alone, labelled):

- **s = 50%:** price potency 61.0%; flow offset not directly computed at
  episode scale (regime flows at 50% are ~55–65% of the 75% flows, so
  the offset share is of the same order or smaller). Combined: still
  clearly below conventional.
- **s = 75%:** price potency 45.5%; flow offset closes ~5–40% of the
  0.649 pp gap. Combined potency ≈ **50–67%** of conventional — the
  ranking survives, the gap narrows.
- **s = 90%:** price potency 35.6%; flow offset grows with s but from
  the same young book; no computed episode row — directionally a larger
  offset share than at 75%, against a larger gap (0.766 pp). Combined:
  below conventional on every computed or bounded variant.

At **regime horizon**, no such table can be honestly filled in: FRB/US
produced no regime ranking (its result is an 8-quarter episode with
rff exogenised back to baseline — Lane G §5.3), and the flow channel
alone, which does speak at regime scale, points the other way under
deficit-reduction use and the same way under spent use. Anyone quoting
a single "combined potency by dial" number has silently picked a
horizon and a fiscal use. The Fed's decision horizon is the episode;
the fiscal score's horizon is the regime; the two analyses must not be
fused — which is precisely why the dial forecast (§5) and the fiscal
score (§7) are separate statements in this project.

---

## 5. The institutional layer — from non-identification to a forecast

The optimum is not identified; the *forecast* is a different exercise:
what does a real central bank do with a novel, untested, statutorily-
floored instrument whose transmission coefficients (β, avoidance,
incidence) are all unestimated on day one?

**Brainard conservatism.** The classic result (Brainard 1967): under
multiplicative parameter uncertainty, the optimal response through the
uncertain instrument is *attenuated* relative to certainty-equivalence.
The fee is the uncertain instrument here — its β is a prior with a pile-
up at its own cap in the predecessor model, its base erodes by an
unestimated elasticity, its legal incidence (lender remits; borrower
pays β of it) has never been observed. The funds rate is the known
instrument. A loss-minimising committee facing variance, not just mean,
transmission loads the known instrument and rations the unknown one —
which, given the statutory floor, means **s at or near 50%**, with the
fee treated as a complement whose share grows only as its transmission
is measured.

**Reversibility and the familiar tool.** Funds-rate moves are
reversible next meeting, at no structural cost. Dial moves are closer
to regime announcements: loan contracts price off the expected fee path,
avoidance structures are built in response to it, and reversing s after
the market has adapted is neither clean nor quick. Gradualism — the
documented FOMC preference for measured, telegraphed steps in *any*
instrument — applies a fortiori to the less reversible one.

**The statutory floor as focal default.** Congress wrote a range with a
50% floor and no default-setting formula and no fiscal target. In
committee practice, the bound closest to the pre-existing regime
(conventional policy = the limiting case s → the minimum share) is the
status-quo anchor: moving *up* requires an affirmative case, holding at
the floor requires none. The burden of proof inside the institution
sits on the high-dial advocate, and §§2–3 show the mandate evidence
cannot carry that burden.

**Independence and the fiscal-appearance problem.** A central bank that
voluntarily sets a revenue-bearing levy near its maximum will be
described — by Congress, by markets, by litigants — as raising revenue,
whatever its statement says. The Fed's institutional capital is its
perceived mandate purity; it defends that capital jealously (it resists
far smaller fiscal entanglements). Setting s high spends independence
capital for zero mandate benefit (§3.2). Setting it at the floor is the
costless signal that the fee is being operated as a monetary instrument,
not a tax. This is not in any loss function; it is how the institution
actually behaves, and it points one way.

**Financial-stability mandate creep.** The fee would arrive with no
dedicated stability framework, while its stability effects (§2c(1),
(2), (3)) are the least measured of all. Committees do not maximise an
untested instrument's use before its stability monitoring exists; the
post-2008 pattern is to build the framework first and normalise the
instrument inside it slowly.

### Forecast scenarios (qualitative plausibility — no invented percentages)

**(i) 50% default-and-hold — MOST PLAUSIBLE for the first policy
episodes / first years.** The Fed operates the fee at the statutory
floor, conducts stance primarily through IORB as today, and says so.
Requires no affirmative case, preserves ZLB distance and reversibility,
minimises fiscal appearance. This is also the prototype's own median/
modal outcome — reached there by accident of priors, reached here by
institutional reasoning; the agreement of the destination should not be
mistaken for agreement about the route.

**(ii) 50% start, gradual evidence-contingent drift up — PLAUSIBLE as
the medium-run path.** As episode data accumulate — measured β near the
top of its range, avoidance small, flow-channel estimates at episode
scale confirming the offset, no stability incidents — the committee
raises s in small, announced steps, each framed as transmission-neutral
housekeeping. Even on this path the *decade* is mostly low-s: drift is
slow by design, and the fiscal book (§7) accrues at the dial in force
when each cohort originates, so scenario (ii)'s 10-year revenue sits
between the fixed-50% and fixed-75% cases and closer to the former
unless drift is early. What caps the drift: §3.2's borrower-cost
arithmetic does not go away with learning — learning can shrink the
*uncertainty* penalty, not the 2.24× equal-effect cost at 75%.

**(iii) Rule-based high share (75–90% by formula) — LEAST PLAUSIBLE.**
A pre-committed high share requires a rule, and a rule requires an
argument for what the share is *for*. The mandate arguments available
(§§2–3) do not supply one: at best they are condition-dependent corner
arguments. The only coherent rules that select 75–90% are fiscal
(deficit, debt-service, or programme-financing targets) — objectives
the authorising framing expressly denies the Fed, and which the Fed
itself would refuse as a condition of operating the instrument. This
scenario becomes plausible only if Congress rewrites the default —
i.e., if the high dial is chosen *legislatively*, not by the Fed under
its mandate. That is a political forecast, outside this lane's evidence.

---

## 6. What evidence would change the forecast

- **First-episode transmission estimates:** loan-level or market-based
  estimates of β (pass-through of the fee into new-loan rates) near 1
  with tight bounds would retire the Brainard discount and strengthen
  scenario (ii); β measured low or dispersed would entrench (i).
- **Avoidance data:** origination shares migrating to nonbank/foreign/
  bond substitutes in the first 1–2 years. Small migration → drift
  viable; rapid base erosion at the floor's modest fee rates → the
  instrument is weaker than modelled at every s and (i) hardens
  (raising s into an eroding base is self-defeating).
- **Flow-channel measurement at episode scale:** creditor-MPC and
  interest-income demand estimates showing the §2b offset materially
  larger than 40% of the price gap within 1–3-year horizons (i.e.,
  creditor MPC well above 0.40) would weaken the price channel's floor
  pressure for *episodes*, not just regimes.
- **Stability record:** fee-era bank margin/capital data and marginal-
  borrower default performance. A clean record removes §2c's tail-risk
  premium; early stress concentrated in new-borrower cohorts would push
  toward the floor regardless of mandate arithmetic.
- **Treasury use, legislated:** if Congress legislates deficit-reduction
  use *and* the regime-scale flow estimates harden, the long-run
  argument for a higher s strengthens (though it remains a regime
  argument being applied to an episode-deciding institution). If the
  fee is legislated as spent (the project's MFA design), §2b says the
  mandate case for high s weakens further.
- **Statutory change:** Congress setting a higher default or a formula
  would move the forecast mechanically — and would relocate the choice
  from the Fed to the legislature, which is a different claim than "the
  Fed would set it there."

---

## 7. Fiscal consequences of the forecast

### 7.1 The $6T test by dial (MC v2, FY2027–36, combined = net fee +
consolidated interest saving; 10,000 draws, judgemental priors —
"P(≥$6T)" is prior mass, not a calibrated probability)

| s | Mean | Median | p10 | p90 | P(≥ $6T) | Net fee alone ≥ $6T |
|---|---|---|---|---|---|---|
| 50% | $4.26T | $4.22T | $3.32T | $5.24T | **1.7%** | 0.0% |
| 75% | $6.47T | $6.40T | $4.99T | $8.03T | 63.2% | 8.3% |
| 90% | $7.86T | $7.76T | $6.01T | $9.84T | 90.1% | 32.1% |

Read with MC v2's own warnings: the interest channel is load-bearing at
every dial (net fee alone essentially never reaches $6T below the
ceiling); τ = 0 alone — Treasury yields simply not following IORB down
— reduces the s = 75% combined total to $5.37T and kills $6T there too;
the strict loans-only covered base cuts the s = 75% P(≥$6T) to 31.9%
(central base 74.1%).

**Consequence line:** under this lane's forecast case — the Fed at the
50% floor through its first years (scenario (i)), or drifting only
gradually (scenario (ii), whose 10-year total lies between the 50% and
75% rows and nearer the 50% row) — **the combined fiscal benefit is
~$4.3T on MC v2 priors and the $6 trillion hypothesis FAILS.** $6T
survives only in the fixed-75%/90% policy-rule cases — i.e., only if the
Fed *chooses and sustains* a dial the dual mandate does not compel it to
choose. Any presentation of the $6T figure that does not carry the
dial condition on its face is presenting a policy-rule scenario as a
forecast.

### 7.2 Distinct test — do not conflate

$6T is the project's round-number benchmark for the fee package, not
the financing requirement of the healthcare bill. Lane J's modeller's
construction (no CBO score of H.R.10924 exists) puts the MFA residual
after displaced outlays, premiums, employer contributions and the
bill's own Title II at **+$2.52T central** (−$1.29T low / +$10.73T
high-stress). Against that central residual, even the s = 50% forecast
case covers, with ~+$1.9T to spare; against the high-stress residual,
no dial covers. So: **"$6T fails at the forecast dial" and "Medicare
for America is unfunded in the central case" are different statements —
the first is this lane's conclusion, the second does not follow from
it.** Title II, not the fee, does the largest single share of the
bill's own financing work in the central case.

---

## 8. Correction of the prototype's 57.1%

**What it was:** the cross-path *mean* of the discretionary dial in a
16,000-path reduced-form Monte Carlo whose dial was determined by
invented priors — a sign-ambiguous γ channel centred near zero (41% of
paths drawing the perverse sign), a hard-coded 1.6 unemployment weight,
a bank-fragility term capped at 0.20 pp, and risk/inertia penalties
added in bare units to a pp² loss (audit §§3.2–3.5, §9). Its own output
distribution is bimodal: **median and mode 50% in every year 2029–36,
~66% of path-years exactly at the floor, ~9% exactly at the ceiling**;
the mean path plotted in the prototype's charts is a trajectory no
simulated Fed follows, and even the median of path-means (54.3%) is an
artefact of the floor group's identity rotating across years. 57.1% is
prior mass averaged over an unidentified choice — it is not an
estimate, a forecast, or an optimum, and it should not be quoted as
"where the Fed would set the dial."

**What replaces it:** not a better point number — §1 shows none is
available from the mandate — but a three-part statement:

1. **Identification:** the dual mandate does not point-identify s; at
   fixed borrower cost it prefers the floor (FRB/US price channel,
   partially offset at episode scale by the flow channel), and along
   the equal-effect locus it is flat in s (§§2–3).
2. **Forecast:** institutionally, a newly authorised Fed plausibly
   **starts at the 50% floor and holds it through its first episodes**,
   with gradual evidence-contingent drift the plausible medium-run path
   and a rule-based high share implausible absent legislative action
   (§5) — a behavioural forecast with its falsifying evidence listed
   (§6), not a disguised optimum.
3. **Fiscal honesty:** all fiscal totals must be quoted *conditional on
   the dial as a policy-rule assumption* (50 / 75 / 90% rows, §7.1),
   never at a single "expected" dial. At the forecast case the combined
   total is ~$4.3T and $6T fails; at 75–90% sustained it survives on MC
   v2 priors. The dial is the hypothesis's load-bearing assumption, and
   it is the one the mandate does not supply.

---

## 9. Limitations and sources

- FRB/US results measure that model's channel structure (no bank/loan/
  mortgage/reserve variables); the wedge reaches `rcar`/`rbbb` only.
  β = 0.88 and τ = 0.32 are priors, estimated nowhere in this project.
- Flow-channel demand ranges rest on labelled MPC (0.10–0.40 creditor;
  0.60–0.90 health recipients) and multiplier (1.0–1.5) assumptions;
  range tops stack the extremes. Episode flow was computed at s = 75%
  only; §4's other rows are bounded, not computed. Note:
  `repo/FLOW_CHANNEL.md`'s narrative on disk ends inside its §2; all
  flow figures here were taken from the same lane's tested results file
  (`repo/results/flow_channel_v1.csv`) and its summary in
  `repo/MONTECARLO_V2.md` §6, which agree.
- Equal-effect rescales at 50%/90% are factor-based inference from
  Lane G's potency factors (validated at 75%: 2.20 inferred vs 2.237
  converged); they assume the near-pure-scale-factor behaviour Lane G
  verified at 75% holds at the other dials.
- MC v2 totals are conditional simulations under judgemental priors,
  not confidence intervals; several structural parameters (debt path,
  reserve stock, phase-in) were held at placeholders even there.
- The sequence-Jacobian/HANK cross-check on §2c(2)'s marginal-borrower
  potency was scoped in the project plan but never run; that channel
  remains the largest *unquantified* item in the decomposition.
- Institutional §5 is qualitative central-bank practice (Brainard
  attenuation, gradualism, independence protection), argued from the
  structure of the choice; it attaches no numerical probabilities, by
  design.

*Sources: `audit/PROTOTYPE_AUDIT.md` (Lane A); `integration/
FRBUS_SCENARIOS.md` (Lane G); `repo/FLOW_CHANNEL.md` +
`repo/results/flow_channel_v1.csv` (Lane H); `repo/MONTECARLO_V2.md`
(Lane I); `mfa/RESULTS_MFA_V1.md` (Lane J).*
