# BASE_B.md — The Unified Base (headline), Monetary Symmetry Fee v2

Sponsor decision, 2026-11-22: **"Bonds are absolutely included and
grandfathered in same way as other loans, the memo is wrong on that
part."** The unified base below is therefore the HEADLINE base for all
v2 work. The loans-only base (DATA.md, "Base A") is retained intact as
the comparison/sensitivity; its code and outputs are unchanged. New
code: `unified_data.py`, `unified_model.py`, `run_unified.py`,
`tests/test_unified.py`. Outputs: `outputs/covered_path_unified_*.csv`,
`outputs/summary_unified_*.csv`, `outputs/comparison_unified_vs_loansonly.csv`.

## 1. The organizing principle

**The fee attaches to the ultimate borrower's obligation — loan or
bond, whoever holds it — and coverage follows the obligation through
sale or securitization. Every non-Treasury borrower obligation is
covered exactly once.**

Consequences, all deliberate:

- **Form is irrelevant.** A C&I loan and a corporate bond of the same
  issuer are the same kind of obligation; the base does not reward
  re-papering credit from one form into the other. (The behavioral
  substitution this forecloses is exactly why the sponsor overruled
  the loans-only draft; substitution *elasticities* remain other
  lanes' work — this module is accounting phase-in only.)
- **Holder is irrelevant.** Coverage follows the obligation, so a loan
  sold, participated, or securitized stays covered; a bond traded in
  the secondary market stays covered. There is no holder-based exit.
- **Intermediary funding instruments are not obligations of an
  ultimate borrower** and are not separately covered (see §4 on agency
  debentures and financial-sector bonds): charging them would tax the
  same underlying principal twice.
- **Treasury securities are excluded**: they are the federal
  government's own obligations, and the consolidated-government
  accounting (memo §III.C) nets them in any case.

## 2. What was added — data and verification

| Category | $B | Series / table | Vintage |
|---|---|---|---|
| Nonfinancial business debt securities | 9,321.4 | Fed Z.1 L.102/L.103/L.104, **FL144122005** (= FL104122005 + FL114122005) | Q4 2025, rel. 2026-03-19 |
| State and local government securities | 3,519.6 | Fed Z.1 L.212/L.107, **FL213162005** | Q4 2025, rel. 2026-03-19 |

**Unified eligible stock: $43,714.3B** = loans 30,873.3 + business debt
securities 9,321.4 + municipals 3,519.6.

**Verification of the sponsor's ~$9.3T estimate.** The $9,321.4B figure
Base A had recorded as excluded is verified against the actual series —
with one refinement: $9.3T is *total nonfinancial business debt
securities*, not bonds alone. Composition at Q4 2025 (rel. 2026-03-19
vintage): corporate bonds **FL103163005 = $7,924.1B**; corporate-issued
municipal securities FL103162000 = $651.7B; nonfinancial commercial
paper (residual) ≈ $215B; noncorporate business debt securities
≈ $530.6B. The category is modeled as the full FL144122005 bucket so
that unified = Base A + (exactly what Base A excluded) + munis, with no
residual or overlap. Vintage note: the Sep 2026 Z.1 release revised
FL103163005 at Q4 2025 up to $8,075.3B; the model keeps the
March-2026-release vintage for consistency with the Q4 2025 business
loan categories it sits beside. CP is ~2% of the bucket; its true
turnover is near-total within a quarter, so treating it at the bucket
δ slightly *understates* early coverage of that slice — immaterial,
and conservative.

**Municipal cross-check.** Z.1 L.212 total municipal liabilities
(FL383162005) at Q4 2025 = $4,403.8B = state/local 3,519.6 +
nonprofit-issued 232.5 + corporate-issued 651.7. The corporate-issued
piece is already inside the business debt-securities bucket above;
the state/local piece is the muni category here; the two sum without
overlap. SIFMA's market total ($4.5T, 2Q26) is the same universe on a
different vintage/basis.

**Boundary item — nonprofit-issued municipals ($232.5B, FL163162003).**
Not included: the sponsor's specification was state and local
government securities. Under the §1 principle, nonprofit hospitals and
universities *are* ultimate borrowers, so this is a documented scope
choice, not a principled exclusion; adding the category is a one-line
change if the sponsor directs it.

## 3. Turnover parameters — bonds phase in more slowly

δ = annual exit share of the outstanding stock (maturity + call +
tender + default), replaced by new — covered — issuance. As in DATA.md,
no agency publishes a stock-exit rate; point values are **ASSUMED**
within ranges anchored to published facts:

| Category | δ central (range) | Anchors |
|---|---|---|
| Business debt securities | 0.11 (0.08–0.14) | Average maturity at issuance ≈ 10–11 yrs (SIFMA corporate chartbooks) implies straight-line exit ≈ 0.09–0.10; flow identity — gross nonfinancial issuance ≈ 15% of stock less ≈ 3.5% net growth — implies ≈ 0.11; calls/tenders add in refunding years |
| Municipal bonds | 0.09 (0.07–0.12) | Serial amortization retires principal continuously (average life of a new issue ≈ 10–12 yrs despite 20–30-yr final maturities); flow identity — SIFMA gross issuance ≈ 14% of stock less Z.1 net growth ≈ 4.7% (2025) — implies ≈ 0.09; standard 10-yr par calls add exits when rates fall |

Growth: business debt securities 3.5%/yr (FL103163005 grew ≈ 3.7%/yr
2023–25); munis 3.0%/yr (FL213162005 +4.7% in 2025; longer-run 2–3%).
Fixed-rate shares (reporting only): 0.95 both, ASSUMED (floating-rate
notes and VRDOs are small shares).

**Quantified lag** (covered share, central turnover, floating design):

| FY | Loans-only total | Business bonds | Municipals | Unified total |
|---|---|---|---|---|
| 2028 | 22.1% | 14.0% | 11.7% | 19.5% |
| 2030 | 48.0% | 36.4% | 31.0% | 44.1% |
| 2033 | 68.9% | 59.6% | 52.4% | 65.5% |
| 2036 | 80.4% | 74.3% | 67.2% | 78.0% |

Bond turnover (δ 0.09–0.11) is roughly one-third the business-loan
rate (0.33) and below even business mortgages (0.14): nine collection
years in, munis are the slowest major category in the base, and the
unified covered share trails loans-only by ~2–4 points throughout —
while the unified covered *stock* and collections are larger from
FY2028 onward. One mechanism the constant-δ engine does not capture:
a **refunding** of a grandfathered bond is a new issuance and enters
coverage immediately, so falling-rate refunding waves (the "locked"
design's environment) would accelerate bond phase-in beyond these
paths. That is behavioral and belongs to the other lanes; it is noted
here because for bonds, unlike loans, refunding is the dominant
turnover margin in low-rate years.

## 4. Collection mechanics — issuer assessment vs. lender assessment

**Loans (Base A categories): lender-assessed.** The statutory payer is
the lender (bank or nonbank). In the SFC transactions matrix the fee
flow originates in the *lender sectors*: bank/nonbank net lending
falls, reserves drain to the TGA on payment, and any pass-through to
borrowers appears as a separate loan-rate/spread flow (modeled in the
SFC/FRB-US lanes, not here).

**Bonds (the two new categories): issuer-assessed.** The statutory
payer is the borrower itself — the nonfinancial business (corporates)
or the state/local government (munis) — on outstanding principal of
post-effective-date issues. In the SFC accounts this changes the
originating sector of the fee flow: it is the *borrowing* sector's
financial balance that deteriorates by the amount paid, directly,
with no lender-margin absorption margin in between. Practical
mechanics differ accordingly:

- Assessment is per-issue, on the issuer of record, computed from
  outstanding principal (DTC/registered-holder records identify the
  issue, not the holder — correctly, since liability does not follow
  the holder).
- Remittance can ride the existing paying-agent/trustee
  infrastructure (the same agents that disburse coupon payments) or
  direct issuer filing; either way settlement reaches the TGA through
  the banking system, but the reserve drain is the *issuer's* deposit
  drawdown, not a charge on lender balance sheets.
- Because the payer and the borrower coincide, the fee is a direct
  increment to the issuer's debt-service cost from the first coupon
  date — there is no pass-through elasticity to estimate for the
  *statutory* incidence (economic incidence via new-issue yields is,
  again, the other lanes' question).

**Agency MBS — not a category.** Agency MBS are pass-throughs of
mortgages. The underlying mortgage is the ultimate borrower's
obligation and is already covered at origination (household mortgage
category), with coverage following it into the pool. A separate charge
at the MBS level would tax the same principal twice, violating §1.
**Agency debentures** (Fannie Mae, Freddie Mac, FHLB debt) are the
intermediaries' own funding instruments, not ultimate-borrower
obligations — excluded on the same principle. **Financial-sector bonds**
(bank and nonbank lender issuance) are excluded for the identical
reason: they fund loan books whose obligations are themselves covered;
charging both layers double-counts principal. Both exclusions are
applications of the organizing principle, not ad-hoc carve-outs.

## 5. Municipal inclusion — flagged legal-design risk (sponsor decided)

Including state and local government securities is the sponsor's
decision and is implemented as directed. It is flagged here as the
unified base's largest legal-design exposure:

- **Constitutional posture is defensible but not free from doubt.**
  *South Carolina v. Baker*, 485 U.S. 505 (1988), upheld a federal law
  denying tax exemption to unregistered state bonds against a Tenth
  Amendment / intergovernmental-tax-immunity challenge, and the modern
  doctrine permits nondiscriminatory federal taxes that fall on states
  as they fall on others. An issuer fee of general applicability —
  the same rate schedule as corporate issuers — fits that frame. But
  *Baker* involved a condition on the §103 exemption, not a direct
  per-dollar charge on state borrowing, and a direct charge will be
  litigated as a tax on the borrowing power itself; expect a challenge
  and design for severability (the muni category is a separable module
  in this model precisely so the base survives its loss).
- **§103 interaction.** The fee raises muni issuers' all-in borrowing
  cost and partially capitalizes into lower tax-exempt bond prices /
  higher yields; it also erodes the value of the §103 subsidy the
  federal government simultaneously grants — a policy tension to
  disclose, not a modeling obstacle. (Whether fee payments by issuers
  interact with arbitrage/rebate rules under §148 is a drafting item
  for counsel.)
- **Federalism/political exposure.** The payers are 50 state
  governments and tens of thousands of local issuers; the charge will
  be characterized as a federal levy on state borrowing regardless of
  its legal form. Flagged, per instructions — not excluded.

## 6. Results — headline (unified) vs. sensitivity (loans-only)

Same fee path as Base A (0.15% FY28; 1.00% FY29 blend; 1.95% FY30+),
same two designs, three turnover cases. Gross collections, $B.

**Cumulative gross collections, FY2028–36:**

| Design / turnover | Loans-only (Base A) | **Unified (Base B)** | Bond increment |
|---|---|---|---|
| Floating, low | 3,008 | **4,029** | +1,021 |
| Floating, central | 3,433 | **4,625** | +1,193 |
| Floating, high | 3,824 | **5,180** | +1,356 |
| Locked, low | 2,449 | **3,249** | +800 |
| Locked, central | 2,834 | **3,781** | +947 |
| Locked, high | 3,197 | **4,286** | +1,089 |

**Central case detail (floating design):**

| FY | Eligible: A → B ($B) | Covered share: A → B | Collections: A → B ($B) | of which bonds |
|---|---|---|---|---|
| 2028 | 32,836 → 46,555 | 22.1% → 19.5% | 5.4 → 6.8 | 1.4 |
| 2030 | 34,927 → 49,585 | 48.0% → 44.1% | 285 → 370 | 84 |
| 2033 | 38,323 → 54,511 | 68.9% → 65.5% | 487 → 656 | 169 |
| 2036 | 42,061 → 59,939 | 80.4% → 78.0% | 637 → 878 | 241 |

Reading: adding bonds raises the eligible base by 41.6% ($30.87T →
$43.71T) and central-case cumulative collections by ~35% (floating) /
~33% (locked). The increment is back-loaded — only $1.4B in FY2028,
$241B by FY2036 — because bond turnover is the slowest in the base
(§3). Nothing in these outputs reflects behavioral response: no
substitution between loans and bonds (the margin the sponsor's
decision closes), no yield or spread response, no refunding waves.
Those are supplied, if at all, by the SFC/FRB-US lanes; this module's
outputs are the accounting phase-in those lanes must respect.

## 7. Tests

`tests/test_unified.py` adds 10 tests (conservation, zero
pre-effective coverage incl. bond categories, monotone phase-in,
phase-in lag ordering, unified-vs-loans-only share/collection
relationships, locked-design stock identity, turnover ordering).
Full suite (Base A + unified): **23 passed** (see run log, 2026-11-22).
