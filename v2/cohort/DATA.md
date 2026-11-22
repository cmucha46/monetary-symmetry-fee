# DATA.md — Monetary Symmetry Fee v2, loan-cohort + fiscal skeleton

Built 2026-11-22. All stocks are **published values**, retrieved 2026-11-22
(Fed/FiscalData pages read directly; where the sandbox proxy blocked bulk
downloads, values were taken from the releasing agency's release text as
republished — each entry names its route). **Nothing is calibrated toward
any revenue total.** Parameters without a published series are labeled
**ASSUMED** with the sensitivity range used in the model.

## Stated timing assumption

Enactment during calendar 2027; **effective date October 1, 2027** (first
day of FY2028). Loans originated before that date are grandfathered
forever; only originations on/after it are covered. FY2027 collections are
zero by construction. Fee path (scenario input, not a forecast): FY2028 =
0.15% (statutory initial rate); FY2029 = 1.00% (ASSUMED mid-transition
blend); FY2030+ = 1.95% = IORB after 50/50 synchronization, holding the
conventional-baseline IORB flat at its last observed value (3.90%).

## 1. Eligible private loan stocks (loans only)

Total eligible stock at base vintage: **$30,873B**. Debt securities
(corporate bonds ≈ $9,321B, Z.1 L.102/L.103 Q4 2025) are excluded — not
loans. Federal student loans ($1,746.7B) are excluded — government lending.

| Category | $B | Series / table | Vintage |
|---|---|---|---|
| Household 1-4 family mortgages (excl. HELOCs) | 13,517.0 | Fed Z.1, households & nonprofits 1-4 family mortgages **$13,977B** (Q2 2026) minus HELOCs carved out below | Z.1 release 2026-09-11, data thru 2026-06-30 |
| HELOCs (revolving) | 460.0 | FRBNY Household Debt & Credit, HELOC balances | Q2 2026 |
| Revolving consumer credit (mostly cards) | 1,368.5 | Fed G.19, series TOTALSL revolving component | Sep 2026 (G.19 rel. 2026-11-06) |
| Motor vehicle loans | 1,589.8 | Fed G.19 quarterly detail (NSA) | Sep 2026 |
| Private student loans | 137.9 | Enterval Analytics / MeasureOne (via EducationData.org compilation of FSA + lender data). G.19 total student = 1,884.6; federal ≈ 1,746.7 (cf. FSA federal portfolio $1,724.5B, Jun 2026) | Q2 2026 |
| Other nonrevolving consumer credit | 381.6 | G.19 residual: 3,856.0 nonrevolving − 1,884.6 student − 1,589.8 auto | Sep 2026 |
| Nonfinancial business loans excl. mortgages | 6,215.3 | Fed Z.1 **L.102**: FL143168005 depository institution loans n.e.c. 2,869.4 + FL143169005 other loans & advances 3,345.9 | Q4 2025 (Z.1 rel. 2026-03-19) |
| Nonfinancial business mortgages (CRE + multifamily + farm) | 7,203.2 | Fed Z.1 **L.102**: FL143165005 mortgages | Q4 2025 |

Notes and known seams:

- **Nonbank / private-credit share.** Coverage follows the loan, not the
  holder, so no holder split is needed for collections. For the record:
  the Fed's new F.4.4 table (Z.1, Q2 2026) puts private-credit loans at
  **7.1% of nonfinancial corporate debt ($15,698.6B, FRED BCNSDODNS)**,
  ≈ $1.1T, sitting inside "other loans & advances" above. MBA holder data
  for commercial/multifamily mortgages (Q2 2026): banks 38%, agency/GSE
  portfolios & MBS 23%, life insurers 15%, CMBS/ABS 13%.
- **Business-mortgage definitional gap (weak point).** Z.1 L.102 business
  mortgages ($7,203B, borrower-sector basis, incl. farm and noncorporate
  multifamily) vs. MBA commercial/multifamily debt outstanding **$5.1T**
  (Q2 2026, property/investor basis). The $2.1T gap is definitional
  (sector vs. property universe), not an error in either source; the model
  uses the Z.1 borrower basis for consistency with the other categories.
- **Home-equity seam (weak point).** Z.1's household mortgage line includes
  closed-end home-equity loans inside the $648.6B all-sector home-equity
  total; only the $460B HELOC (revolving) piece is carved out here, using
  the FRBNY credit-panel measure. Closed-end HE loans therefore remain in
  the mortgage category with mortgage turnover — acceptable, but the split
  is approximate.
- Mixed vintages (Q4 2025 for business, Q2/Sep 2026 for household) reflect
  the latest published tables on the build date; the model grows each
  category from its base, and FY2027 applies one year of growth with zero
  coverage.

## 2. Turnover (exit-rate) parameters δ — the phase-in driver

δ = share of the outstanding stock exiting per year (scheduled amortization
+ prepayment/payoff + charge-off), replaced by new (covered) originations.
Published anchors are cited; the point values used are **ASSUMED** within
documented ranges, because no agency publishes a single stock-exit rate per
category. This is the model's dominant uncertainty and is why every run is
produced at low/central/high δ.

| Category | δ central (range) | Anchor |
|---|---|---|
| HH mortgages | 0.09 (0.06–0.13) | Origination volume ≈ $1.6–2.0T/yr on a ~$14T stock (MBA) implies gross replacement ≈ 12%/yr incl. cash-out churn; net stock exit is lower in a high-rate (lock-in) regime — 2023–24 payoff speeds were historically slow, 2020–21 historically fast |
| HELOCs | 0.50 (0.35–0.65) | ASSUMED: revolving lines redraw/repay continuously; no published stock-exit series |
| Cards/revolving | 0.75 (0.60–0.90) | Monthly payment rates on card balances ≈ 20–30% (Fed/bank data) imply rapid balance turnover; balances attributable to post-enactment draws treated as covered originations (drafting simplification — see §5) |
| Auto | 0.24 (0.20–0.28) | Average auto-loan life ≈ 3.5–4 yrs on 60–72-month terms with trade-in prepayment |
| Private student | 0.10 (0.08–0.13) | Standard 10-year repayment terms |
| Consumer other | 0.30 (0.25–0.35) | ASSUMED blend of personal-loan terms (2–5 yrs) |
| Business non-mortgage loans | 0.33 (0.25–0.40) | C&I median maturity ≈ 3–4 yrs (DealScan/SLOOS literature); revolvers roll continuously; "other loans & advances" includes longer private-credit terms (5–7 yrs), pulling the blend down |
| Business mortgages | 0.14 (0.11–0.17) | MBA maturity survey: $652B of C/MF mortgages mature in 2027 alone (≈13% of the MBA-basis stock) plus amortization/prepayment |

## 3. Fixed vs. adjustable shares (of outstanding stock)

Used for reporting and for the SFC/FRB-US lanes' transmission work; the
cohort engine itself tracks fee design, not borrower rate type.

| Category | Fixed share | Source/basis |
|---|---|---|
| HH mortgages | 0.93 | FHFA National Mortgage Database: ARM share of outstanding 1-4 family balances ≈ 7% |
| HELOCs / cards | 0.00 | Prime-indexed by construction |
| Auto | 0.95 | Predominantly fixed-rate installment |
| Private student | 0.60 | ASSUMED (fixed/variable mix in lender disclosures) |
| Business non-mortgage | 0.35 | ≈65–70% of C&I loans float with SOFR/prime (DealScan-based literature); private credit predominantly floating |
| Business mortgages | 0.55 | ASSUMED: agency/CMBS fixed vs. bank CRE floating blend (MBA holder mix) |

## 4. Federal fiscal baseline

**Treasury (MSPD, Sep 30, 2026; FiscalData Debt to the Penny).** Total debt
$40,710B (Nov 19, 2026 API pull; $40,100B at Sep 30, 2026). Marketable debt
**$31,830B**: bills $7,120B (22.4%), notes $16,280B, bonds $5,550B, and a
residual $2,880B of TIPS + FRNs — the TIPS/FRN split ($2,140B / $740B) is
an **ASSUMED** allocation of the published residual. Weighted average
maturity **70 months** (Treasury via Senate JEC Monthly Debt Update, Sep
2026). **33% of marketable debt matures within 12 months; 55.1% within 3
years** (GAO-26-107529 / TBAC Q3 2026). Average rate on marketable debt
**3.57%** (Oct 2026). The fiscal skeleton's per-bucket annual maturity
fractions (bills 1.00, FRN 1.00, notes 0.135, TIPS 0.10, bonds 0.035) are
ASSUMED and calibrated only to reproduce the published year-1 repricing
share (model: 32.9% vs. published 33% — verified by test).

**Federal Reserve (H.4.1, week ended Nov 18, 2026, released Nov 19, 2026).**
Securities held outright **$6,472.9B** (Treasuries $4,587.1B; MBS
$1,883.5B; agency debt $2.3B); total assets $6,741B; reserve balances
**$3,001.8B** (Wednesday level); ON RRP $317.0B; TGA $892.3B. **IORB =
3.90%** (Board implementation note effective 2026-09-17; target range
3.75–4.00%, EFFR 3.88%). Baseline IORB expense run-rate ≈ 3.90% × $3,002B
≈ **$117B/yr**. **Deferred asset: remittances due to Treasury −$232.5B as
of Oct 28, 2026** (H.4.1 Table 6) — MEDIUM confidence: retrieved via a
secondary graphic citing that table, not yet read off the release PDF
directly; the fiscal skeleton treats it as a parameter, and its exact
value affects only the year remittances resume, not any fee result.
Portfolio yield (2.7%) and Fed opex+dividends ($12B/yr) in fiscal.py are
**ASSUMED** round values pending the Fed's audited financial statements.

## 5. Modeling choices and open seams

1. **Revolving credit coverage.** Draws under credit lines opened before
   enactment: the model treats post-enactment *balances* as covered
   (δ-driven). A statute could instead grandfather the line itself. This
   choice moves card/HELOC collections by tens of $B over the window and
   is a drafting decision for counsel, flagged here.
2. **Collections timing.** Collections = fee rate × within-year *average*
   covered stock. No delinquency/collection haircut is applied (gross
   receipts); charge-offs exit via δ.
3. **No behavioral response.** Originations, growth, and δ are held at
   baseline: no credit-demand elasticity, no migration to bonds/offshore,
   no spread absorption by lenders. Those belong to the SFC/FRB-US lanes;
   this module's job is the accounting phase-in they must respect.
4. **Fee-rate path is an input.** The default path halves a *flat* 3.90%
   IORB. Any FRB/US-produced IORB path can be dropped into
   `default_fee_path()`'s place without touching the cohort engine.
5. **Locked-design approximation.** In design="locked", a year's
   originations are charged on a half-year average balance in year one;
   thereafter vintages decay at the category δ. Vintage balances are
   asserted to sum to the covered stock every year (in-code invariant).

## 6. Weakest data points (ranked)

1. **δ for HELOCs and "consumer other"** — no published stock-exit series;
   pure assumption within wide ranges (mitigated: small stocks).
2. **Z.1-vs-MBA business mortgage gap ($2.1T definitional)** — largest
   single stock uncertainty; resolved by basis choice, not by evidence.
3. **Fed deferred asset (−$232.5B)** — secondary-source retrieval; verify
   against H.4.1 Table 6 PDF before any external use.
4. **Business-loan vintage (Q4 2025)** — one release behind the household
   data; Q2 2026 L.102 will revise the base by ~1–2%.
5. **Private student loan stock ($137.9B)** — industry-compiled
   (Enterval/MeasureOne), not an agency series; small stock, low stakes.
6. **TIPS/FRN split of the MSPD residual** — assumed; affects only the
   fiscal skeleton's repricing detail at the margin.
