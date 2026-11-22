# Monetary Symmetry Fee v2 — Literature Review for Behavioral Parameters

**Purpose.** This review assembles the empirical evidence for the behavioral parameters the
stock-flow-consistent (SFC) simulation needs, organized by the four literatures specified in the
commissioning memo (Carlos A. Mucha, Nov. 22, 2026). Every quantitative claim carries a source.
Where the literature genuinely supports a range, we give a **calibrated range** the model can use.
Where it does not — in particular, where no one has ever estimated the response to *this* instrument
(a principal-based fee on lenders, statutorily tied 1:1 to IORB) — we write **UNCALIBRATED** and
propose the sensitivity grid the simulation should sweep instead of a point value.

**A standing warning that applies to all four sections.** Almost every estimate below is for an
*adjacent* instrument: liability-based bank levies of 2–30 bp (not a fee that reaches 200+ bp at
synchronization), conventional policy-rate changes (not a halved policy rate paired with a fee),
or bank-specific capital/liquidity shocks (not a universal, permanent, announced regime change).
Extrapolating a 20 bp levy estimate linearly to a 200 bp fee is the single most likely way this
project produces a false number. Where we extrapolate, we say so and bound it.

---

## 1. The interest-income channel of monetary policy

### 1.1 Theory and the sufficient-statistic result

The organizing framework is Auclert (2019), "Monetary Policy and the Redistribution Channel,"
*American Economic Review* 109(6): 2333–2367. Auclert decomposes the aggregate consumption
response to a real-rate change into (i) intertemporal substitution, (ii) an aggregate income
effect, and (iii) three redistribution channels — earnings heterogeneity, the Fisher (inflation)
channel, and the **interest-rate exposure channel**. The exposure channel is governed by a
sufficient statistic: the covariance across households between their **unhedged interest rate
exposure (URE)** — assets maturing within the period minus liabilities maturing within the
period — and their marginal propensity to consume (MPC). Using Italian and U.S. data, Auclert
finds all three redistribution channels are likely to *amplify* conventional transmission: rate
hikes transfer cash flow from high-MPC borrowers (whose URE is negative) toward lower-MPC
savers, so redistribution reinforces, rather than offsets, the contraction. Kaplan, Moll and
Violante (2018), "Monetary Policy According to HANK," *American Economic Review* 108(3):
697–743, reach the complementary result that in a heterogeneous-agent model the *direct*
substitution effect of a rate change on aggregate consumption is small and most transmission
runs through indirect general-equilibrium income effects — which is precisely why who receives
interest income, and what they do with it, matters at first order.

Auclert, Rognlie and Straub (2018; rev. 2024), "The Intertemporal Keynesian Cross," formalize
the sequence-space version of the same point: the aggregate MPC out of a transfer and the
distribution of exposures jointly determine the multiplier on any income redistribution the
policy engineers.

**Implication for the fee design.** Under conventional tightening, the interest paid by
borrowers does not vanish — much of it re-enters the economy as interest income to depositors,
money-fund holders, bondholders and bank shareholders. Under Monetary Symmetry, roughly half
of the policy-sensitive charge is instead remitted to Treasury. If Treasury recycles it
(spending, transfers, or lower other taxes), the demand effect depends on the MPC of the
*recipient of the recycling*, not on the MPC of the interest-income recipient who was displaced.
If Treasury uses it for deficit reduction, the demand effect is the negative of the displaced
recipients' MPC-weighted spending. The model must therefore treat the fiscal recycling rule as
a separate, explicit assumption — it is not pinned down by the monetary literature.

### 1.2 Who actually receives the interest income — concentration evidence

The offsetting-income story is only as strong as the spending propensity of the people who
receive it, and the recipients are heavily concentrated at the top of the wealth distribution:

- Federal Reserve, **Distributional Financial Accounts (DFA)**: the top 1% of households hold
  roughly 30–31% of total household net worth and the top 10% roughly two-thirds (DFA, recent
  vintages); the top 10% hold on the order of 85–90% of corporate equities and mutual-fund
  shares. Fixed-income holdings (bonds, loans) are similarly top-heavy, though **deposits are
  much less concentrated** — checkable deposits and money-market shares are the one
  interest-bearing asset class with substantial holdings in the middle of the distribution.
  (Federal Reserve, Distributional Financial Accounts of the United States; Saez & Zucman
  (2016), *Quarterly Journal of Economics* 131(2): 519–578, and the World Inequality Lab
  Technical Note 2020/07 reconciling their series to the DFA, find the top 1% hold ~22–25% of
  their own portfolios in fixed-income claims — i.e., interest income accrues overwhelmingly to
  households whose MPC out of transitory income is low.)
- MPC heterogeneity by wealth is among the best-measured objects in this literature.
  Fagereng, Holm and Natvik (2021), "MPC Heterogeneity and Household Balance Sheets,"
  *American Economic Journal: Macroeconomics* 13(4): 1–54, using Norwegian lottery winnings,
  estimate an average first-year MPC of roughly 0.5, falling steeply with liquid wealth —
  households with little liquidity spend most of a windfall within the year; wealthy households
  spend very little. Kaplan and Violante (2014), *Econometrica* 82(4): 1199–1239, estimate a
  quarterly MPC of about 0.25 for the ~30% of U.S. households that are hand-to-mouth
  (including "wealthy hand-to-mouth" who hold illiquid assets).

**Calibrated implication.** The MPC out of *interest income received by the households who hold
most interest-bearing assets* is at the **low end** of the MPC distribution. The simulation
should use:

| Parameter | Calibrated range | Basis |
|---|---|---|
| MPC (annual, out of interest income), top-decile asset holders | **0.05–0.20** | Fagereng–Holm–Natvik (2021) MPC-by-liquidity gradient applied to DFA concentration |
| MPC (annual), median depositor / money-fund holder | **0.20–0.40** | Kaplan–Violante (2014); Auclert (2019) sufficient statistics |
| MPC (annual), hand-to-mouth / borrower households losing cash flow | **0.50–1.00** | Fagereng–Holm–Natvik (2021); Kaplan–Violante (2014) |

The asymmetry between the first and third rows *is* the Auclert result: redistribution from
row 3 to row 1 amplifies tightening; the fee's redirection to Treasury interrupts the row-1
receipt, and what happens next depends entirely on the recycling assumption (§1.1).

### 1.3 The 2022–24 cycle: the income offset was large in levels

The most recent tightening cycle produced the cleanest aggregate demonstration that interest
income is a first-order offset:

- BEA personal interest income rose from **$1,573B (2022) to $2,079B (2023)** — an increase of
  roughly **$507B in a single year** — and to $2,241B in 2024 (BEA, Personal Income, via FRED
  series A064RC1A027NBEA). The narrower *monetary* interest received by persons rose from
  **$681B (2022) to $1,076B (2023)**, +$395B (BEA via FRED B1138C1A027NBEA). For scale, BEA's
  2026 benchmark revisions *raised* measured net interest income by a further $281B for 2023
  and $402B for 2024 relative to prior vintages — i.e., the income channel was even larger
  than real-time data showed.
- The Federal Reserve's own staff and outside central banks flagged the mechanism in real
  time. Norges Bank Governor Ida Wolden Bache's 2024 Jackson Hole remarks ("The cash-flow
  channel of monetary policy") document that net-interest cash-flow effects were quantitatively
  important but **much weaker in the U.S. than in floating-rate economies**, because more than
  90% of U.S. mortgages are fixed-rate (Federal Reserve / SCF evidence cited therein: ~92% of
  U.S. mortgaged households hold fixed-rate loans), so U.S. households' *payments* barely rose
  while their interest *receipts* did — the configuration in which the income offset to
  tightening is strongest. BNP Paribas Economic Research (2024), "US: economic resilience
  despite higher rates — the role of household finances," reaches the same conclusion from
  aggregate data: rising financial income "largely shielded households" from higher
  non-mortgage interest payments, and the household debt-service ratio stayed roughly flat
  through the tightening.

**Calibrated implication for the baseline (Regime A).** In the U.S. institutional
configuration — fixed-rate mortgages, concentrated asset holdings, low recipient MPCs — the
interest-income channel in 2022–24 was a **partial, not dominant, offset**: it plausibly
blunted tightening at the margin but did not reverse it, consistent with Auclert's finding
that redistribution *amplifies* on net once borrowers' losses are counted. Any calibration in
which the income channel makes conventional tightening *expansionary* in aggregate is outside
the supported range and should be treated as a model artifact, not a finding.

### 1.4 What is NOT calibrated here

- **UNCALIBRATED:** the MPC out of *Treasury-recycled* fee revenue. This depends on the
  congressional use of funds (transfers vs. spending vs. deficit reduction), which is a policy
  choice, not a behavioral parameter. **Sensitivity grid:** recycle to (a) deficit reduction
  (effective MPC 0), (b) uniform household transfers (MPC 0.25–0.50), (c) government purchases
  (multiplier per the standard fiscal literature), (d) Medicare-for-America financing — run
  all four; do not average them.
- **UNCALIBRATED:** any *differential* MPC for interest income vs. other income of the same
  household (mental-accounting effects). The literature estimates MPCs out of income generally.
  Grid: apply a salience discount factor of 0.5 / 0.75 / 1.0 to interest-income MPCs.

---

## 2. Bank levy pass-through

### 2.1 The evidence base — all of it is for small liability levies

Every credibly identified estimate in this literature concerns post-crisis European levies on
bank *liabilities* (typically excluding insured deposits and equity), at statutory rates of
roughly **0.02%–0.3%** of the levy base. The Monetary Symmetry fee is levied on *loan principal*
and reaches **IORB itself** at synchronization — 2%+ in the memo's illustrative configuration,
an order of magnitude larger. The estimates below therefore identify the *sign, incidence
pattern, and moderating factors* of pass-through far better than its *level* at fee scale.

### 2.2 The three core studies

**Kogler (2019)**, "On the incidence of bank levies: Theory and evidence," *International Tax
and Public Finance* 26(4): 677–718. Bank-level data, 2,987 banks, 23 EU countries, 2007–2013.
Building on the Monti–Klein model, Kogler finds levies are shifted **mainly forward to
borrowers**: lending rates rise by an estimated **20–24 basis points** in response to levy
introduction (against levy burdens that were themselves only a few tens of basis points of
liabilities — i.e., pass-through at or above 100% of the average burden for affected banks is
within his estimates), net interest margins widen, and deposit rates *also* rise modestly where
deposits are partly exempt from the base (banks bid for the exempt funding source).
Pass-through is **stronger in concentrated markets** and for banks with high loan-to-deposit
ratios, and **weaker for well-capitalized banks**. Non-deductibility of the levy (Germany, UK)
strengthens pass-through relative to deductible regimes.

**Buch, Hilberg and Tonzer (2016)**, "Taxing banks: An evaluation of the German bank levy,"
*Journal of Banking & Finance* (Bundesbank Discussion Paper 38/2014). The German levy (2011)
was small — high exemption threshold (€300M of relevant liabilities) left ~77% of banks exempt
and revenue minimal. For the *average* bank they find **no significant effect** on loan volume
or rates; for the **most-affected banks**, lending growth is lower, lending rates on new loans
are higher, and deposit rates on new deposits are *lower* (note the sign conflict with Kogler
on deposits — Kogler's deposit result is driven by exemption design; where deposits are in the
base or the bank is funding-constrained, the sign flips). Lesson: at trivial levy sizes, most
banks absorb or ignore the cost; incidence concentrates in the most-exposed institutions.

**Devereux, Johannesen and Vella (2019)**, "Can taxes tame the banks? Evidence from the
European bank levies," *Economic Journal* 129(624): 3058–3091. Their focus is balance-sheet
composition rather than pricing: levies induced banks to **reduce (taxed) borrowing and
leverage**, but to **increase portfolio risk** (riskier assets per unit of assets). The
funding-risk reduction dominates for well-capitalized banks and is *exactly offset* by added
portfolio risk for weakly capitalized banks. For the fee simulation, this is the key
composition warning: a charge on loan principal gives banks a margin to respond on the
*asset* side — shifting toward exempt assets (government securities) or toward riskier
covered loans whose yields can carry the fee — not only on price.

Supporting/adjacent evidence: Ceponis, Kuslys and Sarapovas (2021), *Engineering Economics*
32(3): 210–220, estimate Poland's asset-based bank tax raised lending margins by an average of
**~0.39 percentage points** — the largest clean pricing estimate in the literature, from a
levy of 0.0366%/month (~0.44%/yr) on assets, i.e. pass-through of roughly 85–90% of the
statutory burden into margins in a concentrated banking market. Capelle-Blancard and
Havrylchyk (2017), "The impact of the French securities transaction tax on market liquidity"
and related levy work, and the Monti–Klein comparative statics in Kogler both predict
pass-through rises as loan-demand elasticity falls — i.e., pass-through should be **highest
precisely where borrowers have no substitute** (mortgages for most households, small-business
credit), which links this section to §3.

### 2.3 Calibrated range — with the extrapolation warning attached

| Parameter | Range | Status |
|---|---|---|
| Pass-through of a levy cost (per unit of loans) into new-loan rates, competitive/concentrated mix | **0.5 – 1.0+** of the per-loan cost | Calibrated *at levy scale* (≤ ~45 bp burden): Kogler (2019); Ceponis et al. (2021) |
| Pass-through into deposit rates | **−0.2 to +0.3** of cost, sign depends on whether deposits are exempt from the base | Contested sign: Kogler (2019) vs. Buch–Hilberg–Tonzer (2016) |
| Volume response at levy scale | Small; significant only for most-exposed banks | Buch–Hilberg–Tonzer (2016) |
| Asset-composition response | Shift toward exempt assets; risk-shifting by weakly capitalized banks | Devereux–Johannesen–Vella (2019) — qualitative, robust |

**UNCALIBRATED at fee scale.** No observation exists of a principal-based charge anywhere near
200 bp, universal across lenders, and *expected to move one-for-one with the policy rate*.
Three scale effects could break linearity in either direction: (i) at 200 bp the fee is large
relative to typical net interest margins (~3%), so absorption is arithmetically impossible for
the average bank — pass-through or exit must occur; (ii) a universal fee, unlike the European
levies, leaves no untaxed domestic bank competitor, which in Monti–Klein logic *raises*
pass-through toward (or beyond) full; (iii) but the binding outside option becomes nonbank and
bond finance (§3), which caps pass-through segment by segment.
**Sensitivity grid for pass-through θ (share of fee appearing in the borrower's rate):**
θ ∈ {0.5, 0.75, 1.0, 1.15} overall, and segment-specific: mortgages {0.75, 1.0, 1.15},
small business {0.75, 1.0, 1.15}, large corporate {0.25, 0.5, 0.75} (capped by bond-market
outside option). Report results conditional on θ; do not report a θ-averaged headline.

**Design interaction the model must include:** if the fee is *deductible* against corporate
income tax, the effective burden falls by the CIT rate (~21% federal) and Kogler's
non-deductibility result implies measurably lower pass-through. The memo does not specify
deductibility — flag as an open legislative parameter with a first-order effect.

---

## 3. Loan-to-bond and offshore substitution (leakage)

### 3.1 Loan-to-bond substitution: strong for firms that have the option

Becker and Ivashina (2014), "Cyclicality of credit supply: Firm level evidence," *Journal of
Financial Economics* 112(2): 244–262 (NBER WP 17392). Conditional on a U.S. firm raising new
debt at all (1990–2010, DealScan + bond issuance data), the *composition* of that debt shifts
systematically from loans to bonds when bank credit supply tightens — tight SLOOS standards,
high bank NPLs, low bank equity values, tight monetary policy. The substitution is large
enough that their loan–bond composition index tracks bank credit conditions across five
decades, and — critically — the switching behavior of the large, bond-market-access firms
*predicts* deteriorating credit and investment outcomes for small firms that cannot switch.
Kashyap, Stein and Wilcox (1993), *American Economic Review* 83(1): 78–98, established the
aggregate version: commercial-paper issuance rises relative to bank loans when monetary policy
tightens.

**Interpretation for the fee.** Substitution is a *relative-price* response. The fee raises
the relative cost of (covered) loans versus bonds; the Becker–Ivashina evidence says
bond-access firms will exercise that option elastically and quickly (within the issuance
cycle, i.e., quarters, not years). But note what bonds do *not* escape in this design: bond
yields are priced off the Treasury curve and the policy path, so if the fee lets the Fed run
IORB at half the conventional level, the all-in cost of bond finance *falls* relative to the
conventional baseline — substitution toward bonds is then partly a feature (aggregate
borrowing costs still restrained via the loan segment) and partly a leak (the restraint and
the revenue both shrink). The SFC model must track the loan/bond mix endogenously for the
large-corporate segment; treating the covered base as fixed overstates both revenue and
restraint, by an amount that grows over the ten-year window as refinancing rolls the stock.

### 3.2 Segment-by-segment leakage assessment

**Large corporates — HIGH leakage.** Full bond and CP market access (Becker–Ivashina 2014);
also direct access to foreign-bank and offshore dollar credit (§3.3). Expect the covered share
of large-corporate debt to erode fastest. Calibrated direction, **UNCALIBRATED rate** — no
study estimates substitution in response to a *permanent, announced* loan/bond cost wedge of
this size. **Grid:** covered-base erosion for large corporates of 10% / 25% / 40% of new
issuance share by year 5.

**Small business — LOW leakage on price, HIGH exposure on quantity.** No bond access, thin CP
access; the outside option is not a substitute instrument but *not borrowing*. Becker–
Ivashina's out-of-sample result is the warning: when large firms vacate bank balance sheets,
small-firm outcomes still worsen if banks' overall supply contracts — but under this design
banks are not capital-impaired, merely cost-shifted, so the relevant margin is pass-through
(§2: highest where demand is inelastic — small business is the textbook case). Model small
business as: θ near the top of the grid, quantity response via loan demand elasticity, no
instrument substitution.

**Mortgages — LOW offshore/bond leakage, but a domestic securitization design question.**
U.S. mortgages are overwhelmingly securitized domestically through the GSEs (Fannie Mae /
Freddie Mac) and Ginnie Mae; the "bond substitution" margin for a household is not available —
a household cannot issue a bond. The leakage question for mortgages is instead *definitional
and institutional*: (i) does the fee attach at origination, at the servicer/holder, or to the
MBS holder — and are agency MBS (government-sponsored, arguably "government securities")
exempt? (ii) If agency securitization is exempt and portfolio/bank-held or private-label
loans are covered, origination will migrate toward the agency channel — a large, fast,
purely domestic leak that no elasticity in the literature measures. **UNCALIBRATED — treat as
a legislative-design fork, not a parameter:** run the simulation both ways (agency channel
covered via originator-paid fee vs. exempt) and report the revenue difference as a design
cost, not an uncertainty band. (iii) The cash-flow channel for existing borrowers is weak by
construction (92% fixed-rate, §1.3), so mortgage transmission runs through *new* origination
pricing — consistent with the memo's grandfathering design.

### 3.3 Offshore / cross-border dollar credit: the stock is big, the marginal elasticity is unmeasured

BIS locational banking statistics (LBS): cross-border claims of BIS-reporting banks on the
United States totaled **$9.43 trillion at Q4 2025** (all sectors and instruments, residence
basis), up ~74% since Q4 2019; consolidated (nationality-basis) international claims on the
U.S. were $5.85T, led by Japanese ($1.95T), UK ($1.09T) and Canadian ($0.75T) banking systems
(BIS LBS/CBS via BIS Data Portal). Most of that stock is interbank, official-sector and
securities holdings, **not** loans to U.S. nonfinancial borrowers — the directly substitutable
margin (foreign banks lending cross-border to U.S. corporates, bypassing U.S.-booked loans)
is a subset, historically on the order of $1–1.5T of dollar credit to U.S. non-banks booked
outside the U.S. (McCauley, McGuire and Sushko (2015), "Global dollar credit," *Economic
Policy* 30(82): 187–229, document the scale and rate-sensitivity of offshore dollar credit
globally). Two structural facts bound the leak: (a) foreign banks' **U.S. branches and
subsidiaries** are U.S. lenders — if the fee attaches to U.S.-originated loans regardless of
parent nationality, that (large) channel is covered, and only *true cross-border* booking
escapes; (b) true cross-border corporate lending is concentrated in large, rated borrowers —
the same segment as §3.2's bond substituters, so the two leaks overlap rather than add.

**UNCALIBRATED:** the elasticity of cross-border booking to a U.S. loan-cost wedge.
**Grid:** assume 5% / 15% / 30% of large-corporate *new* borrowing migrates offshore by year
5 (in addition to, and partially overlapping with, the bond-substitution grid in §3.2 — the
model must not double-count the same migrating dollar in both grids).

---

## 4. Deposit and funding responses to a halved administered rate

The design's fiscal arithmetic leans on a specific funding claim: if IORB runs at ~2% instead
of ~4% for the same restraint, banks' funding costs fall, Treasury yields fall, and the
consolidated government saves interest. The deposit literature says the first link is
**not one-for-one**, and the size of the shortfall is measurable.

### 4.1 Deposit betas are well below one, and state-dependent

- Drechsler, Savov and Schnabl (2017), "The deposits channel of monetary policy," *Quarterly
  Journal of Economics* 132(4): 1819–1876, and Drechsler, Savov, Schnabl and Wang (2021),
  "Banking on deposits: Maturity transformation without interest rate risk," *Journal of
  Finance* 76(3): 1091–1143: banks hold deposit market power; when the policy rate rises,
  deposit rates rise **less than one-for-one** (the deposit spread widens), deposits flow out
  to money funds, and lending contracts. The deposit franchise is thus a hedge whose value
  *rises* with rates — running the policy rate at half the conventional level mechanically
  **shrinks bank deposit-franchise income**, a distributional effect inside the banking
  sector the SFC accounts will show whether or not the model "believes" in it.
- Measured cumulative betas, 2022–23 cycle (FFIEC Call Reports, bank-level implied rates on
  interest-bearing deposits): **median bank beta ≈ 0.31; asset-weighted beta ≈ 0.49** over
  2022Q1–2023Q3, versus medians of 0.38 (2004–06 cycle) and 0.24 (2015–19 cycle). Betas build
  slowly — asset-weighted cumulative beta ground from 0.17 (2022Q2) to 0.49 (2023Q3) — and are
  widely dispersed (top-ten banks: 0.26 to 0.75). Industry Call Report aggregates tell the
  same story: median community-bank cost of funds rose ~160 bp against a 525 bp policy move
  (beta ≈ 0.30).
- **Heterogeneity that matters for incidence:** Usenko (2026), "Large depositors, retail
  depositors, and the deposits channel of monetary policy" (working paper): pass-through on
  **large deposits (>$250k) is more than double that on small deposits (beta ≈ 0.7 vs. ≈ 0.3)**;
  large deposits are ~1% of accounts but ~50% of balances (2024) and account for essentially
  all aggregate deposit *flow* response. Small retail deposits are sticky in both price and
  quantity.
- **Level-dependence (the key question for a 4%→2% halving):** the "variable deposit beta"
  evidence (e.g., recent work building on Drechsler et al. 2021 and Wang et al. 2022;
  *Journal of Financial Stability*, 2025, "Variable deposit betas and bank exposure to
  interest rate risk") finds betas are **lower at low rate levels** — near the zero bound, cash
  competes with deposits and banks pass through little; at high levels, money-fund competition
  forces higher pass-through. Symmetrically, on the way *down* from 4% to 2%, deposit rates
  should fall by **more than the low-level beta but less than one-for-one**: the relevant
  object is the *decreasing-rate beta over the 2–4% range*, for which the 2022–23 *rising*
  betas are an imperfect guide (deposit pricing is asymmetric — banks cut deposit rates
  faster than they raise them, the standard "rockets and feathers" pattern in retail banking).

**Calibrated range for the simulation:**

| Parameter | Range | Basis |
|---|---|---|
| Deposit beta, easing 4%→2%, small retail deposits | **0.3–0.5** | Usenko (2026) small-deposit beta ≈0.3, adjusted up for easing asymmetry |
| Deposit beta, easing 4%→2%, large/wholesale deposits | **0.6–0.9** | Usenko (2026) ≈0.7 rising-rate; wholesale near money-market pricing |
| Blended system beta (balance-weighted) | **0.45–0.65** | Asset-weighted 2022–23 beta 0.49 (FFIEC), eased-range adjustment |
| Lag to full repricing | **4–8 quarters** | Cumulative-beta build-up path, FFIEC Call Reports |

**Direct consequence the fiscal model must not assume away:** if IORB halves (−200 bp) and
the blended deposit beta is ~0.5, bank deposit costs fall only ~100 bp — the other ~100 bp is
a *widening of the deposit spread captured by banks* on the way down (mirror image of the
deposits channel). That is a transfer from depositors to bank equity, partially offsetting
banks' fee burden in the SFC accounts — and it means "lower IORB ⇒ proportionally lower bank
funding costs ⇒ proportionally lower loan rates" overstates transmission by roughly the
(1 − beta) share on the deposit-funded portion of balance sheets.

### 4.2 The money-fund / T-bill margin

Deposit outflows in 2022–23 went predominantly to money market funds and direct T-bill
holdings: roughly **$1 trillion of deposits left the banking system** from 2022Q1 to mid-2023
while about **$700B flowed into money funds** (Allen & Baig et al., "Deposit Runs," *Review of
Pacific Basin Financial Markets and Policies*, 2026, accepted); total U.S. money-fund assets
reached ~$6 trillion by December 2023, up >60% from December 2019 (Investment Company
Institute, via T. Rowe Price 2024 outlook). OFR's 2023 Annual Report documents the mechanism:
the cost of interest-bearing deposits was ~0.75% at end-2022 against 5%+ money-fund yields,
and outflows accelerated as the gap widened. The margin is **yield-gap driven with a lag of
months**, and it is two-sided: at IORB = 2%, government money funds (which hold T-bills, repo
and the ON RRP) yield ~2%, the deposit–MMF gap compresses toward its low-rate norm, and the
2022–23 outflow pressure reverses — deposits become *more* stable and *cheaper relative to
wholesale funding* than in the 4% baseline. For the SFC model: treat the deposit/MMF split as
a function of the deposit-spread (policy rate minus deposit rate) with the 2022–23 episode as
the calibration anchor; **the elasticity of the split to the spread is only loosely pinned
(one episode, confounded by the March 2023 bank failures) — flag as partially calibrated,
grid the flow elasticity at 0.5× / 1× / 2× the 2022–23 implied value.**

### 4.3 Treasury yields — the link with no direct evidence

**UNCALIBRATED.** Nothing in the deposit literature, or anywhere else, estimates how much of a
200 bp reduction in the *administered-rate path* (undertaken because a fee does the rest of
the restraint) transmits into the Treasury term structure. The term premium, the path of
expected future short rates, and inflation expectations all re-price on the *regime*, not on
IORB mechanically. FRB/US-style term-structure equations will generate *a* number; it is an
assumption wearing a model's clothing. **Grid:** τ (share of the IORB reduction appearing in
the 10-year Treasury yield, averaged over the window) ∈ {0, 0.25, 0.5, 0.75} — and recall from
the v1 audit that τ is the single highest-leverage parameter in the entire fiscal arithmetic
(each +0.10 of τ was worth roughly +$0.42T over ten years in the v1 Monte Carlo). The
literature review's honest contribution is to state that no published estimate disciplines τ
for this regime change, and results must be reported as a τ-conditional surface, never a
τ-integrated point estimate with a fabricated confidence interval.

---

## 5. Summary: parameter table for the simulation

| # | Parameter | Value / range | Status |
|---|---|---|---|
| 1 | MPC out of interest income, top-decile holders | 0.05–0.20 /yr | Calibrated (§1.2) |
| 2 | MPC, median depositor | 0.20–0.40 /yr | Calibrated (§1.2) |
| 3 | MPC, borrower households (cash-flow loss) | 0.50–1.00 /yr | Calibrated (§1.2) |
| 4 | MPC of Treasury recycling of fee revenue | 0 / transfers / purchases — scenario fork | **UNCALIBRATED** (policy choice) (§1.4) |
| 5 | Levy pass-through θ to loan rates (at ≤45 bp scale) | 0.5–1.0+ | Calibrated at wrong scale (§2.3) |
| 6 | Pass-through θ at fee scale (~200 bp), by segment | Grid: overall {0.5, 0.75, 1.0, 1.15}; large corp {0.25, 0.5, 0.75} | **UNCALIBRATED** (§2.3) |
| 7 | Deposit-rate response to levy | −0.2 to +0.3 of cost; sign design-dependent | Contested (§2.2) |
| 8 | Loan→bond substitution, large corporates | Direction certain; erosion grid 10/25/40% of new-issuance share by yr 5 | **UNCALIBRATED rate** (§3.2) |
| 9 | Offshore migration, large corporates | Grid 5/15/30% of new borrowing by yr 5 (overlap-adjusted vs. #8) | **UNCALIBRATED** (§3.3) |
| 10 | Mortgage leakage | Legislative fork (agency channel covered vs. exempt), not a parameter | Design decision (§3.2) |
| 11 | Deposit beta, easing 4%→2% (blended) | 0.45–0.65, 4–8 qtr lag | Calibrated (§4.1) |
| 12 | Deposit/MMF flow elasticity to spread | 0.5×/1×/2× of 2022–23 implied | Partially calibrated (§4.2) |
| 13 | Treasury-yield transmission τ of lower IORB path | {0, 0.25, 0.5, 0.75} — report as surface | **UNCALIBRATED** (§4.3) |

## 6. The strongest evidence on each side (per the commissioning standard)

**For the proposal's mechanism:** (i) Auclert's sufficient statistics confirm that *who
receives* policy-driven interest flows is a first-order transmission variable, not a footnote
— redirecting the flow is a real lever (Auclert 2019). (ii) The 2022–24 data show the income
flow is enormous ($507B increase in personal interest income in one year, BEA) — even at
top-decile MPCs of 0.05–0.20, the aggregate demand at stake is tens of billions per year, and
the flow to *Treasury* under the fee is larger still. (iii) Levy pass-through evidence
(Kogler; Ceponis et al.) shows principal/liability charges on lenders *do* reach borrower
rates at roughly full incidence — the fee can in principle substitute for rate transmission,
which is the design's core requirement.

**Against / cautioning:** (i) The same pass-through evidence is the strongest warning: if θ ≈ 1
and the Fed halves IORB, covered borrowers face comparable costs *only if* the fee is passed
through as a clean per-loan charge — the European evidence shows pass-through is uneven across
banks (capital, concentration, loan-to-deposit ratio), so the "comparable borrowing costs"
outcome will hold on average while failing bank-by-bank and segment-by-segment. (ii)
Devereux–Johannesen–Vella: banks respond on the asset side too — expect migration toward
exempt assets and risk-shifting that no pricing parameter captures. (iii) Deposit betas near
0.5 mean the funding-cost relief from halving IORB is roughly half the naive figure, with the
residual captured as bank deposit-spread income — muting both the borrower benefit and (via
remittances and bank taxes) part of the fiscal gain. (iv) The leakage margins (bonds, offshore)
are real, fast for exactly the borrowers with the largest balances, and unmeasured at this
wedge size — the covered base in year 10 will be materially smaller than the covered base in
year 1, and every revenue path that ignores this is biased upward. (v) τ — the parameter the
fiscal case most depends on — has no empirical estimate at all.

## References (primary sources cited)

- Auclert, A. (2019). "Monetary Policy and the Redistribution Channel." *American Economic
  Review* 109(6), 2333–2367.
- Auclert, A., Rognlie, M., Straub, L. (2018; rev. 2024). "The Intertemporal Keynesian Cross."
- Becker, B., Ivashina, V. (2014). "Cyclicality of credit supply: Firm level evidence."
  *Journal of Financial Economics* 112(2), 244–262.
- Buch, C., Hilberg, B., Tonzer, L. (2016). "Taxing banks: An evaluation of the German bank
  levy." *Journal of Banking & Finance* (Bundesbank DP 38/2014).
- Ceponis, P., Kuslys, M., Sarapovas, T. (2021). "The impact of bank tax on lending margin."
  *Engineering Economics* 32(3), 210–220.
- Devereux, M., Johannesen, N., Vella, J. (2019). "Can taxes tame the banks? Evidence from the
  European bank levies." *Economic Journal* 129(624), 3058–3091.
- Drechsler, I., Savov, A., Schnabl, P. (2017). "The deposits channel of monetary policy."
  *Quarterly Journal of Economics* 132(4), 1819–1876.
- Drechsler, I., Savov, A., Schnabl, P., Wang, O. (2021). "Banking on deposits: Maturity
  transformation without interest rate risk." *Journal of Finance* 76(3), 1091–1143.
- Fagereng, A., Holm, M., Natvik, G. (2021). "MPC heterogeneity and household balance sheets."
  *American Economic Journal: Macroeconomics* 13(4), 1–54.
- Kaplan, G., Moll, B., Violante, G. (2018). "Monetary policy according to HANK." *American
  Economic Review* 108(3), 697–743.
- Kaplan, G., Violante, G. (2014). "A model of the consumption response to fiscal stimulus
  payments." *Econometrica* 82(4), 1199–1239.
- Kashyap, A., Stein, J., Wilcox, D. (1993). "Monetary policy and credit conditions: Evidence
  from the composition of external finance." *American Economic Review* 83(1), 78–98.
- Kogler, M. (2019). "On the incidence of bank levies: Theory and evidence." *International
  Tax and Public Finance* 26(4), 677–718.
- McCauley, R., McGuire, P., Sushko, V. (2015). "Global dollar credit: Links to US monetary
  policy and leverage." *Economic Policy* 30(82), 187–229.
- Saez, E., Zucman, G. (2016). "Wealth inequality in the United States since 1913." *Quarterly
  Journal of Economics* 131(2), 519–578.
- Usenko, Y. (2026). "Large depositors, retail depositors, and the deposits channel of monetary
  policy." Working paper.
- Federal Reserve, Distributional Financial Accounts of the United States; Financial Accounts
  (Z.1).
- BEA, Personal Income (via FRED A064RC1A027NBEA; B1138C1A027NBEA).
- BIS, Locational and Consolidated Banking Statistics (Data Portal), Q4 2025.
- FFIEC Call Reports, bank-level deposit betas, 2022–23 cycle (FFIEC CDR).
- Office of Financial Research (2023), *Annual Report to Congress*.
- Bache, I. W. (2024), "The cash-flow channel of monetary policy," Jackson Hole remarks,
  Norges Bank.
