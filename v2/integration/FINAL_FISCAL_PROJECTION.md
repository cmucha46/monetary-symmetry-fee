# FINAL_FISCAL_PROJECTION.md — MSF v2 ten-year fiscal projection WITH macro feedback (FY2027–36)

**Status: final integration pass.** This document supersedes the
pre-feedback projection in `FISCAL_PROJECTION.md` (which remains the
record of the Lane D pass). It populates the consolidation's
`frbus_feedback_bn` slot with Lane B's FRB/US Design E results, on the
**unified base** (loans + corporate bonds + municipal bonds; sponsor
decision Nov 22, 2026), central case: floating design, central turnover,
θ = 1.0, erosion E = 0.10, β = 0.55 (inert in the fiscal identity).
All totals remain **τ-conditional** — τ (transmission of the halved
administered-rate path into new-issue Treasury yields) is UNCALIBRATED
and is never integrated over.

> **Everything here is a simulation under stated assumptions — not a
> Fed or CBO forecast.**

## 1. What the feedback pass adds (and what it deliberately does not)

Two objects enter from Lane B (`frbus_feedback.py`; extraction verified
against Lane B's published `metrics.json` to rounding in the test suite):

1. **Fee-path reconciliation (receipts ratio).** Lane B resolved the
   statutory circularity f = rff by whole-path fixed-point iteration:
   the rule finds a lower funds path, and the fee chained to it settles
   at **f ≈ 2.02% (Regime B) / 2.10% (Regime C)** post-sync, vs. the
   cohort skeleton's flat input of 1.95% from FY2030. Lane B's
   cumulative receipts on the loan-only base, relative to the skeleton's
   loan-only gross collections at the skeleton path ($3,433B), give the
   ratio applied proportionally to the unified base's net fee receipts:
   **B 1.116, C 1.110, D 1.130, E 0.567.** The E ratio is the
   procyclicality of the design made quantitative: at the recession
   trough the funds rate hits its floor region and the fee collapses to
   ≈0.11%, halving cumulative receipts.
2. **Endogenous fiscal drag.** From Lane B's own accounts,
   drag_t = Δsurplus_t − receipts_t + Δinterest_t: the revenue loss and
   cyclical outlay increase from output/employment running below the
   matched baseline. Cumulative FY28–36 (β = 1, MCE): **B −$2,610B,
   C −$2,404B, D −$2,672B, E −$1,082B**, scaled by the same receipts
   ratio (ASSUMED proportionality) before entering the consolidation.
   The drag excludes receipts and interest by construction, so it does
   not double-count the τ-surface savings.

**Deliberately not populated:** the `sfc_ix_adjustment_bn` slot stays
empty (NaN). The SFC Section IX experiment is a one-period, first-round
sign/channel result, not an annual fiscal series; monetizing it would
fabricate precision. Under this projection's non-recycling closure its
direction (modestly *more* contractionary at θ = 1) corroborates the
drag's sign rather than offsetting it.

**Interval framing (Lane B §7.1, adopted here).** Design E's rule is
outcome-reactive and cannot see the fee, so its offset (57–63% of the
fee) is a **lower bound** on what a stance-targeting FOMC would deliver,
and its drag is an **upper-bound** drag. The pre-feedback projection is
the opposite end of the interval. The truth, on this project's evidence,
lies between the two tables — and both are reported.

## 2. Final central case — Regime C (statutory 24-month sync), unified base

Annual detail at τ = 0.5 ($B). Fee rate and covered stock are the
skeleton's; net fees are shown at both fee paths.

| FY | Covered stock | Gross | Net fee (skeleton path) | Net fee (Lane B path) | Drag | Δ remit | Savings τ=.5 | **Consolidated net τ=.5** |
|---|---|---|---|---|---|---|---|---|
| 2027 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | **0.0** |
| 2028 | 9,077 | 6.8 | 5.8 | 6.4 | −0.5 | 0.0 | 0.0 | **5.9** |
| 2029 | 16,044 | 125.6 | 104.9 | 116.4 | −91.6 | 0.0 | 0.0 | **24.8** |
| 2030 | 21,874 | 369.7 | 302.3 | 335.5 | −243.1 | 8.8 | 87.3 | **188.6** |
| 2031 | 26,969 | 476.2 | 381.2 | 423.0 | −335.5 | 104.2 | 106.4 | **298.1** |
| 2032 | 31,542 | 570.5 | 446.7 | 495.7 | −365.9 | 62.5 | 123.1 | **315.4** |
| 2033 | 35,726 | 655.9 | 513.5 | 569.9 | −378.4 | 58.5 | 137.7 | **387.7** |
| 2034 | 39,614 | 734.6 | 575.2 | 638.3 | −393.4 | 58.5 | 150.5 | **454.0** |
| 2035 | 43,274 | 808.2 | 632.8 | 702.2 | −415.2 | 58.5 | 161.8 | **507.4** |
| 2036 | 46,757 | 877.8 | 687.3 | 762.8 | −443.7 | 58.5 | 171.8 | **549.3** |
| **Total** | | **4,625** | **3,650** | **4,050** | **−2,667** | **410** | **939** | **2,731** |

Ten-year consolidated net by regime and τ ($B, unified, floating, central):

| Regime | τ=0 | τ=0.25 | τ=0.5 | τ=0.75 |
|---|---|---|---|---|
| Pre-feedback (upper bound of the interval) | 4,059 | 4,529 | 4,998 | 5,467 |
| **B — fast sync (~2 quarters)** | **1,570** | **2,039** | **2,508** | **2,978** |
| **C — 24-month sync** | **1,793** | **2,262** | **2,731** | **3,201** |
| D — C + inflation shock † | 1,515 | 1,984 | 2,453 | 2,923 |
| E — C + recession shock † | 1,865 | 2,334 | 2,804 | 3,273 |

† **D and E are PARTIAL adjustments and are not comparable to B/C as
"benefit under the shock."** Lane B measures D/E against their *shocked*
conventional baselines; this table adjusts only the fee and drag
components and leaves the savings and remittance components on the
unshocked skeleton paths. The fully consistent shocked-baseline figures
are Lane B's own in-model Δsurplus (loan-only receipts, no remittance
term): **D +$3,765B, E +$1,444B** — E's small figure, against C's
+$3,715B on the same basis, is the correct statement of the recession
case: the fee collapse (receipts $1,945B vs $3,809B) plus the collapse
of the in-model interest saving (−$581B vs −$2,310B) removes most of
the benefit precisely when the economy is weakest.

**Bridge, Regime C at τ = 0.5 ($B):** pre-feedback 4,998
+ fee-path reconciliation +400 (net fees 3,650 → 4,050)
− endogenous drag −2,667 → **final 2,731**. Composition of the final
figure: net fees 4,050 + interest savings 939 + Δ remittances 410
− drag 2,667.

**Loans-only sensitivity (final, Regime C feedback):** applying the same
feedback to the loans-only central case gives net fees of
$2,709B × 1.110 = $3,007B and totals of **τ=0: $749B; τ=0.25: $1,219B;
τ=0.5: $1,688B; τ=0.75: $2,157B** (drag identical; savings and
remittances base-independent). Base breadth is worth ~$1,043B of final
benefit at τ = 0.5.

## 3. Feedback-adjusted grid (floating design only)

The pre-feedback grid (288 cells/τ, `MONTE_CARLO.md`) stands as the
upper-bound surface. Applying Regime C feedback mechanically to the
144 floating-design cells (Lane B ran floating only; locked cells are
not adjusted — labeling them with floating-derived feedback would
misstate them):

| τ | Mean | Median | p25 | p75 | Min | Max |
|---|---|---|---|---|---|---|
| 0 | 1,535 | 1,608 | 1,001 | 2,175 | **−38** | 2,744 |
| 0.25 | 2,004 | 2,078 | 1,470 | 2,644 | 431 | 3,213 |
| 0.5 | 2,473 | 2,547 | 1,940 | 3,114 | 901 | 3,682 |
| 0.75 | 2,943 | 3,016 | 2,409 | 3,583 | 1,370 | 4,151 |

No feedback-adjusted cell reaches $6T (max $4,151B at τ = 0.75). One
adverse corner cell (low turnover, 40% erosion, θ = 1.15, τ = 0) is
approximately zero (−$38B): at the joint adverse corner the fiscal
benefit can vanish. Grid summaries remain conditional simulation
summaries — not confidence intervals.

## 4. Reproduction

```
cd ~/workspace/monetary-symmetry/v2/integration
python3 run_final.py              # final tables + appendix + adjusted grid
python3 -m pytest tests/ -q       # 23 tests (11 Lane D + 12 final-pass)
```

Machine-readable: `outputs/final_projection_regime_{B,C,D,E}.csv`,
`outputs/monte_carlo_feedback_adjusted_summary.csv`,
`outputs/final_results.json`.
