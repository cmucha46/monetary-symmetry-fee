# FISCAL_PROJECTION.md — MSF v2 ten-year fiscal projection (FY2027–36)

**A τ-conditional surface, never a single headline number.** Every total in
this document is stated at a named τ (transmission of the halved
administered-rate path into new-issue Treasury yields). τ is UNCALIBRATED —
no published estimate exists for this regime (LITERATURE.md §4.3) — so a
τ-integrated figure would be a fabricated number and none is produced.

> **BASE.** Headline = **UNIFIED base** (loans + corporate bonds +
> municipal bonds; sponsor decision, Nov 22, 2026, superseding the memo's
> loans-only §II.D). Eligible stock FY2027: **$45,112B** (loans-only:
> $31,839B; the ≈$13,273B difference is the bond component). The
> **loans-only base is reported as the labeled sensitivity** in §3. The
> unified cohort outputs (`summary_unified_<design>_<turnover>.csv`) were
> picked up through the `inputs.json` candidate paths with **no code
> change** — the swap mechanism documented there is exactly how they
> landed — and passed the engine's provenance check (unified eligible
> stock exceeds loans-only by >5%; actual: +42%).

## 1. The consolidation identity (memo §III.C)

For each fiscal year, consolidated net fiscal benefit vs. the conventional
baseline is:

**consolidated net = net fee receipts + Treasury interest savings (τ) + Δ Fed cash remittances**

- **Net fee receipts** = cohort gross collections × (1 − substitution
  erosion) × (1 − tax-interaction haircut). Gross collections are the
  cohort lane's (grandfathered phase-in on the unified base; FY2027 = 0 by
  construction — effective date Oct 1, 2027). Erosion:
  `e_t = min(0.60, E·θ·ramp_t)`, E ∈ {0, .10, .25, .40} the literature
  lane's year-5 covered-base erosion grid, θ pass-through (θ reaches
  collections *only* through this slot — statutory collections are rate ×
  covered stock regardless of incidence; the θ coupling is an **ASSUMED**
  functional form). Haircut **h = 0.13, ASSUMED and unestimated** (carried
  from v1; no published source exists; fee deductibility — an open
  legislative parameter, LITERATURE.md §2.3 — would move it). Gross is
  always shown next to net.
- **Treasury interest savings (τ)** = the cohort skeleton's maturity-bucket
  repricing (bills/FRNs reprice in year 1; notes 13.5%/yr; TIPS 10%/yr;
  bonds 3.5%/yr; year-1 repricing share 32.9% vs. published 33%) driven by
  `dy_t = −τ × (IORB_base − IORB_MS)`: zero before FY2030 (the skeleton's
  paths diverge only at synchronization), −τ × 195bp thereafter.
  **Consolidation adjustment:** savings are counted only on the
  non-Fed-held share of marketable debt (×0.8559; Fed holds $4,587B of
  $31,830B). Interest on Fed-held Treasuries nets to zero in consolidation
  — Treasury pays less, the Fed earns less, remittances fall equally — and
  the skeleton holds Fed income constant, so counting that share here too
  would double-count it (tested in the suite). Savings are identical on
  both bases (they do not depend on the fee base).
- **Δ Fed cash remittances** come straight from the skeleton, **cash
  basis, deferred-asset identity respected**: halving IORB raises Fed
  earnings by $58.5B/yr, but the increment first extinguishes the
  −$232.5B deferred asset. Δ cash is **$0 in FY2027–29**, +$8.8B in FY2030
  (the year the MS path clears the deferred asset), +$104.2B in FY2031,
  then +$62.5B / +$58.5B/yr as the baseline path's own remittances resume.
  Ten-year Δ cash remittances: **+$410B** — far less than 10 × $58.5B,
  precisely because of the deferred-asset rebuild.

## 2. Central case — annual table (UNIFIED base, headline)

Central case: turnover = central, design = floating, θ = 1.0, erosion
E = 0.10, β = 0.55 (inert here — see §5). IORB paths are the cohort
skeleton's scenario input (baseline flat 3.90%; MS halves to 1.95% at
synchronization in FY2030), **not** a forecast.

| FY | IORB base | IORB MS | Fee rate | Covered stock $B | Gross $B | Net fee $B | Δ remit $B |
|---|---|---|---|---|---|---|---|
| 2027 | 3.90% | 3.90% | 0.00% | 0 | 0.0 | 0.0 | 0.0 |
| 2028 | 3.90% | 3.90% | 0.15% | 9,077 | 6.8 | 5.8 | 0.0 |
| 2029 | 3.90% | 3.90% | 1.00% | 16,044 | 125.6 | 104.9 | 0.0 |
| 2030 | 3.90% | 1.95% | 1.95% | 21,874 | 369.7 | 302.3 | 8.8 |
| 2031 | 3.90% | 1.95% | 1.95% | 26,969 | 476.2 | 381.2 | 104.2 |
| 2032 | 3.90% | 1.95% | 1.95% | 31,542 | 570.5 | 446.7 | 62.5 |
| 2033 | 3.90% | 1.95% | 1.95% | 35,726 | 655.9 | 513.5 | 58.5 |
| 2034 | 3.90% | 1.95% | 1.95% | 39,614 | 734.6 | 575.2 | 58.5 |
| 2035 | 3.90% | 1.95% | 1.95% | 43,274 | 808.2 | 632.8 | 58.5 |
| 2036 | 3.90% | 1.95% | 1.95% | 46,757 | 877.8 | 687.3 | 58.5 |
| **Total** | | | | | **4,625.2** | **3,649.7** | **409.7** |

Interest savings and consolidated net, by τ ($B):

| FY | Savings τ=0 | Savings τ=.25 | Savings τ=.5 | Savings τ=.75 | Net τ=0 | Net τ=.25 | Net τ=.5 | Net τ=.75 |
|---|---|---|---|---|---|---|---|---|
| 2027 | 0 | 0 | 0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |
| 2028 | 0 | 0 | 0 | 0 | 5.8 | 5.8 | 5.8 | 5.8 |
| 2029 | 0 | 0 | 0 | 0 | 104.9 | 104.9 | 104.9 | 104.9 |
| 2030 | 0 | 43.7 | 87.3 | 131.0 | 311.2 | 354.9 | 398.5 | 442.2 |
| 2031 | 0 | 53.2 | 106.4 | 159.6 | 485.4 | 538.6 | 591.8 | 645.0 |
| 2032 | 0 | 61.5 | 123.1 | 184.6 | 509.2 | 570.8 | 632.3 | 693.8 |
| 2033 | 0 | 68.8 | 137.7 | 206.5 | 572.1 | 640.9 | 709.8 | 778.6 |
| 2034 | 0 | 75.3 | 150.5 | 225.8 | 633.7 | 709.0 | 784.2 | 859.5 |
| 2035 | 0 | 80.9 | 161.8 | 242.7 | 691.3 | 772.2 | 853.1 | 934.0 |
| 2036 | 0 | 85.9 | 171.8 | 257.6 | 745.9 | 831.7 | 917.6 | 1,003.5 |
| **Total** | **0** | **469.3** | **938.6** | **1,407.9** | **4,059.4** | **4,528.7** | **4,998.0** | **5,467.3** |

**Ten-year consolidated net, central case (unified base):**

| Design | τ=0 | τ=0.25 | τ=0.5 | τ=0.75 |
|---|---|---|---|---|
| Floating | $4,059B | $4,529B | $4,998B | $5,467B |
| Locked | $3,386B | $3,855B | $4,324B | $4,793B |

Decomposition at τ=0.5, floating: net fee $3,650B + interest savings
$939B + Δ remittances $410B = $4,998B. The fee is ~73% of the benefit at
τ=0.5 (90% at τ=0); the interest channel is the τ-dependent remainder.

**Memo Question 6, answered on this pass's evidence:** the central case
does **not** reach the $6T hypothesis at any τ ≤ 0.75 on either base
(unified central maximum: $5,467B at τ=0.75, floating). Across the full
grid (MONTE_CARLO.md), $6T is exceeded only in the extreme corner at
τ=0.75 (grid max $6,324B: high turnover + floating design + zero erosion
+ θ=0.5). The honest statement is: ~$4.1–5.5T central on the unified base,
τ-conditional, with $6T a tail outcome of jointly favorable assumptions —
not a central expectation. Final verdict awaits the FRB/US and SFC passes
(§6), which can move the IORB paths themselves.

Machine-readable: `outputs/fiscal_projection_central_floating.csv`,
`outputs/fiscal_projection_central_locked.csv` (all τ columns, plus the
two EMPTY placeholder columns of §6).

## 3. Sensitivity — loans-only base (memo §II.D as written)

Same central case, loans-only collections (eligible $31,839B):

| Design | τ=0 | τ=0.25 | τ=0.5 | τ=0.75 |
|---|---|---|---|---|
| Floating | $3,119B | $3,589B | $4,058B | $4,527B |
| Locked | $2,641B | $3,111B | $3,580B | $4,049B |

Gross collections (floating, central): $3,433B loans-only vs. $4,625B
unified — including bonds in the base is worth ~$940B of ten-year
consolidated benefit in the central case (the difference is entirely in
the fee component; savings and remittances are base-independent).
Grid distributions for the sensitivity are in MONTE_CARLO.md §4 and
`outputs/monte_carlo_summary_loans_only.csv`.

## 4. What is NOT in these numbers (limitations, stated)

1. **No deficit-feedback loop.** Debt stock is held flat (skeleton
   convention); lower deficits do not reduce issuance and compound the
   savings. Conservative direction.
2. **Fed portfolio frozen** at H.4.1 Nov 2026 size and an ASSUMED 2.7%
   yield: the remittance Δ captures only the IORB-expense channel, not
   reinvestment at lower yields (which would reduce Fed earnings and
   remittances later in the window).
3. **Nonmarketable debt excluded** from repricing (~$7–8T of
   intragovernmental and nonmarketable securities sit outside the
   skeleton).
4. **No macro feedback**: collections and debt do not yet respond to
   FRB/US output/employment paths or to the Section IX interest-income
   experiment — see the EMPTY placeholder interface, §6.
5. **IORB paths are scenario inputs** (flat 3.90% baseline, halved at
   FY2030), inherited from the cohort lane. Regimes B–E paths from the
   FRB/US lane will replace them through the same interface.

## 5. Flagged assumptions (consolidated list)

| Assumption | Value | Status |
|---|---|---|
| Tax-interaction haircut on fee receipts | 13% | **ASSUMED**, unestimated (v1 carry-over); deductibility open |
| Erosion θ-coupling `e = E·θ·ramp` | linear, cap 60% | **ASSUMED** functional form; E grid itself is the lit lane's |
| Erosion phase-in | linear over FY28–32 | ASSUMED |
| Consolidation share for interest savings | ×0.8559 (non-Fed-held) | Accounting identity given skeleton conventions |
| Deposit β in remittances | no entry | Identity has no β term; β's touch point is the SFC bank layer (later pass) |
| Deferred asset | −$232.5B | Cohort lane: MEDIUM confidence (secondary retrieval) |
| Fed portfolio yield / opex | 2.7% / $12B/yr | ASSUMED (cohort lane, pending audited statements) |

## 6. Placeholder interface — FRB/US + SFC Section IX (EMPTY)

`consolidation.apply_macro_feedback(table, frbus_paths=None,
sfc_section_ix=None)` is the documented entry point for the later pass:
`frbus_paths` will carry FY-indexed FRB/US series (regime IORB/fee paths,
macro deviations feeding collections and debt dynamics) and
`sfc_section_ix` the SFC layer's interest-income adjustments. In this pass
it adds the columns `frbus_feedback_bn` and `sfc_ix_adjustment_bn`
**empty (NaN)** to every output table and changes nothing. The slots are
present so the later pass is a data delivery, not a schema change. **No
values have been fabricated for them.**

## 7. Reproduction

```
cd ~/workspace/monetary-symmetry/v2/integration
python3 run_integration.py        # writes outputs/*.csv + results.json
python3 -m pytest tests/ -q       # 11 sanity tests
```
