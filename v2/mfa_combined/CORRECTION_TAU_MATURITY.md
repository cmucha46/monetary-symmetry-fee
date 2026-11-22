# CORRECTION_TAU_MATURITY.md — Maturity-dependent τ correction (Lane 4, Sponsor Correction #2)

**This correction SUPERSEDES the scalar-τ treatment of the interest-savings line in v2 and in Lane 3.** All other Lane 3 elements are held identical — net receipts **$4,050B** (after the 1.1098 fee-path ratio), FRB/US Regime C drag **−$2,667B** as its own line, Δ remittances **+$410B**, 13% haircut **ASSUMED** — so every delta below is attributable to the τ correction alone. **Code:** `consolidation_tau_maturity.py`, `run_tau_maturity.py`. **Outputs:** `coverage_surface_corrected.csv` (τ_long × scenario × spread), `coverage_annual_corrected.csv`, `corrected_summary.json`. **Tests:** Lane 3's 7 + Lane 4's 10 — **17/17 pass**. Lane 3 files, `v2/integration/`, and `v2/cohort/` are unmodified.

> **Relabeling (applies everywhere in Lane 4 outputs).** The surface {0, 0.25, 0.5, 0.75} is now **τ_long — the long-segment transmission** (expectations / term-premium channel beyond 1 year). It is never a whole-curve τ. The front end has no τ: its transmission is 1 **by arbitrage**.

---

## 1. Method

**Premise (sponsor, evidence-supported).** The 3-month bill rate and IORB are arbitrage-locked — bills and reserves are near-perfect substitutes for the marginal holder — so a scalar τ applied to all new-issue yields is wrong at the front end. The empirical exhibit (§5) verifies the premise in 18 years of daily data: levels β = 1.01, ρ = 0.995.

**Two segments** (weights from the project's own maturity structure, `cohort/data.py` TREASURY: WAM 70 months, `share_maturing_1yr` = 0.33):

- **Front end — weight 0.33** (bills plus the share of the stock repricing within ≤1 year). New-issue yield = IORB + spread. With A_t the administered-path decline (IORB_base − IORB_ms from the fiscal skeleton — **verified: 0 before FY2030, 1.95pp from FY2030**, so Lane 3's 0.975pp headline at τ=0.5 is exactly half of it):
  `dy_front = −A_t + Δspread`, where Δspread ∈ {−0.25, 0, +0.15}pp is the *change* in the bill–IORB spread vs baseline (observed range ≈ −0.40pp in the 2021 scarcity to +0.15–0.25pp in the 2026 surge), carried on the synchronized path from FY2030. **Headline at Δspread = 0**, giving a front-end yield decline of the full **1.95pp**.
- **Long segment — weight 0.67.** `dy_long = −τ_long × A_t`, τ_long ∈ {0, 0.25, 0.5, 0.75}.

**Mechanics.** Lane 3's bucket-repricing recursion is linear in the dy path and in the debt stock, so each segment runs the *identical* recursion on its share of the stock with its own dy; front + long = total exactly (test-asserted). The combined fixed point (savings ↔ growing combined debt path; baseline marketable $31,830B → $56,029B, deficits $24.4T cumulative) is iterated as in Lane 3 (tolerance $0.05B; convergence ≤3 iterations in all 36 cells).

---

## 2. Corrected interest line — combined closure, GROWING path, spread = 0 ($B, FY2027–36 cumulative)

| τ_long | Scenario | Front-end savings | Long-segment savings | **Corrected interest** | Lane 3 scalar interest | Δ vs scalar |
|---|---|---:|---:|---:|---:|---:|
| 0 | low | 878 | 0 | **878** | 0 | +878 |
| 0 | **central** | 909 | 0 | **909** | 0 | **+909** |
| 0 | high-stress | 978 | 0 | **978** | 0 | +978 |
| 0.25 | low | 874 | 444 | **1,318** | 667 | +651 |
| 0.25 | **central** | 905 | 459 | **1,365** | 690 | **+674** |
| 0.25 | high-stress | 974 | 494 | **1,468** | 742 | +725 |
| 0.5 | low | 870 | 883 | **1,753** | 1,324 | +429 |
| 0.5 | **central** | 901 | 915 | **1,816** | 1,372 | **+444** |
| 0.5 | high-stress | 969 | 984 | **1,953** | 1,475 | +478 |
| 0.75 | low | 866 | 1,319 | **2,185** | 1,973 | +212 |
| 0.75 | **central** | 897 | 1,366 | **2,263** | 2,043 | **+220** |
| 0.75 | high-stress | 965 | 1,469 | **2,434** | 2,198 | +236 |

**Front vs long split at τ_long = 0.5 (central): front $901B (49.6%) / long $915B (50.4%)** — the front-end third of the repricing exposure, transmitting in full, contributes as much as the entire long segment at τ_long = 0.5. The front-end line is nearly τ_long-invariant ($866–978B across the surface; it moves only through the debt-path feedback) — it is a floor under the interest line, not a surface.

**Annual corrected interest, central, τ_long = 0.5 ($B):** 2027–29: 0; 2030: 140 (front 69 / long 70); 2031: 180; 2032: 219; 2033: 258; 2034: 298; 2035: 339; 2036: 383 (front 190 / long 193). Full annuals: `coverage_annual_corrected.csv`.

**Spread sensitivity (central margins, §3):** Δspread = −0.25pp adds ≈ +$113–115B to interest; +0.15pp subtracts ≈ −$68–69B — second-order vs the correction itself, and it never flips a verdict below.

---

## 3. Corrected coverage surface — GROWING path, spread = 0 ($B)

Margin = fee contribution − MFA residual. Residuals: low −$1,289B, central +$2,524B, high-stress +$10,730B.

| τ_long | Low margin | **Central margin** | High-stress margin | Central financed? |
|---|---:|---:|---:|:--|
| 0 | +3,960 | **+179** | −7,960 | ✅ |
| 0.25 | +4,400 | **+634** | −7,470 | ✅ |
| 0.5 | +4,835 | **+1,085** | −6,984 | ✅ |
| 0.75 | +5,267 | **+1,532** | −6,503 | ✅ |

(Full surface incl. spreads: at Δspread = −0.25pp central margins are +294 / +748 / +1,198 / +1,644; at +0.15pp, +109 / +565 / +1,017 / +1,465. Low is financed in all 36 cells; high-stress in none.)

### Verdict — the central case CHANGES

Lane 3 (scalar τ): central financed **iff τ ≥ 0.5**; margins **−731 / −40 / +641 / +1,312**. Corrected: **the central case is financed at every τ_long, including τ_long = 0** — margins **+179 / +634 / +1,085 / +1,532**. The binding constraint Lane 3 reported was an artifact of haircutting the front end: even if the long segment transmits *nothing* (τ_long = 0), arbitrage-locked front-end repricing alone contributes $909B of interest savings and carries the central case by +$179B. The verdict no longer depends on the unestimated long-segment parameter at all in the central case; τ_long now determines only the *size* of the surplus. Timing caveat survives in milder form: the annual ledger still shortfalls in 2030 at τ_long ≤ 0.5 (annual margin −$10B at τ_long = 0.5, vs −$45B scalar) and in 2035–36, covered by the banked surplus under the spending closure (cumulative margin never goes negative at any τ_long, spread 0 — Lane 3 had cumulative-negative years at τ ≤ 0.25). **Low: financed everywhere (unchanged). High-stress: financed nowhere (unchanged)** — best case −$6,503B at τ_long = 0.75.

---

## 4. V2 restatement — FLAT/banked variant (spread = 0, $B)

Applying the same maturity-dependent treatment to Lane 3's flat variant (which reproduces the v2 verdict) restates v2's own totals:

| τ_long | v2 scalar interest | Corrected front | Corrected long | **Corrected interest** | Interest Δ | v2 total (scalar) | **v2 total (corrected)** |
|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 619 | 0 | **619** | +619 | 1,793 | **2,412** |
| 0.25 | 469 | 619 | 314 | **934** | +465 | 2,262 | **2,727** |
| 0.5 | 939 | 619 | 629 | **1,248** | +310 | 2,731 | **3,041** |
| 0.75 | 1,408 | 619 | 943 | **1,563** | +155 | 3,201 | **3,355** |

**v2's interest line was understated at every τ because the scalar haircut was applied to the front-end third of the stock.** The understatement is largest exactly where v2 looked weakest: at τ=0 v2 booked *zero* interest savings, when the arbitrage-locked front end alone — which no transmission parameter governs — was worth $619B on the flat stock ($909B on the growing path). Corrected v2 totals: **$2,412 / $2,727 / $3,041 / $3,355B** (vs $1,793 / $2,262 / $2,731 / $3,201B). The correction narrows the τ-spread of the v2 verdict from $1,408B to $943B — a third of v2's apparent τ-sensitivity was front-end mispricing.

---

## 5. CBO gap update

Lane 3: model **$96B per 0.1pp** (flat, scalar) vs CBO's **$379B per 0.1pp** — a $283B gap, of which debt growth alone closed 17% ($96B → $143B). Recomputed under the maturity-dependent treatment (growing path, no MFA, baseline-path balances, τ_long = 0.5, spread 0; Lane 3's denominator convention retained — per 0.1pp of the 0.975pp headline decline at the τ=0.5 cell — so the two corrections stack on Lane 3's own scale):

| | Per-0.1pp ($B) | Cumulative interest ($B) | Share of $283B gap closed |
|---|---:|---:|---:|
| Lane 3 model, flat, scalar | 96 | 939 | — |
| + debt growth (Lane 3) | 143 | 1,397 | 17% |
| **+ maturity-dependent τ (Lane 4)** | **191** | **1,858** (front 922 + long 936) | **33% total** |

**The corrected treatment closes 33% of the CBO gap in total** — debt growth's 17% plus a further ~17 points from the front-end correction. The remaining gap is unchanged in kind (repricing realization share, marketable-only coverage, Fed-share consolidation with +$410B returned via remittances — Lane 3 §6) and is still not a contradiction. The CBO figure remains an **exhibit benchmark only — never a plug-in**; the guard test (the figure appears nowhere in either lane's coverage machinery) passes for Lane 4 as it did for Lane 3.

---

## 6. Empirical exhibit summary (full exhibit: `tau_maturity_exhibit.md`)

Data route (i) **succeeded**: FRED fredgraph CSVs for IOER, IORB, DTB3 fetched 2026-11-22 (raw files in `exhibit_data/`; routes (ii)/(iii) not needed). Merged daily sample: 4,529 trading days, 2008-10-09 → 2026-11-19; administered = IOER to 2021-07-28, IORB from 2021-07-29.

- **Full sample: levels correlation 0.995; pass-through β (OLS, bill on administered, levels) = 1.009.** Era βs: 2016–19 hikes 1.11 (ρ 0.989); 2022–24 hikes 0.89 (ρ 0.990); easing 0.69 (ρ 0.933); Covid ZLB 0.45 (ρ 0.645); 2008–15 ZLB not identified (administered rate pinned at 0.25%).
- **Event windows:** narrow [t−1, t+5] β = 0.11 (bills anticipate administered changes); anticipation-inclusive [t−20, t+5] β = **0.87** over 39 administered-rate changes.
- **Spread (bill − administered):** full-sample mean **−10.8bp**, median −14.0bp; ZLB −16.9bp; 2022–24 hikes +2.8bp (SD 27.5bp); **2026-11-19: +26bp (IORB 3.90%, bill 4.16%)** — the sponsor's observation, confirmed in the fetched data, and inside the model's {−0.25, 0, +0.15}pp spread-change scenario range.

No statistic in the exhibit was fabricated: every number is computed by `exhibit_stats.py` from the saved FRED files (`exhibit_stats.json`).

---

## 7. Assumptions ledger (Lane 4 additions only; Lane 3's ledger otherwise stands)

| Parameter | Value | Status |
|---|---|---|
| Front-end transmission | 1 | **BY ARBITRAGE** (design premise; exhibit §6) — not an assumption, not estimated |
| Front-end weight | 0.33 of repricing exposure | Project's own `share_maturing_1yr` (TREASURY, MSPD Sep 2026) |
| Spread change Δspread | {−0.25, 0, +0.15}pp; headline 0 | SCENARIO parameter, documented observed range; applied from FY2030 with the synchronized administered path |
| τ_long (long-segment transmission) | {0, 0.25, 0.5, 0.75} | **UNESTIMATED** — surface only, never integrated over |
| Segment split mechanics | Identical bucket recursion per segment share | Exact under the recursion's linearity in dy and in the stock (test-asserted) |

## 8. Files

- `consolidation_tau_maturity.py` — corrected engine (imports Lane 3 unmodified); `run_tau_maturity.py` — runner.
- `coverage_surface_corrected.csv` — 36 rows (τ_long × scenario × spread, growing): front/long split, contribution, margin, shortfall years, iterations, end-2036 combined debt.
- `coverage_annual_corrected.csv` — annual tables (all headline-spread cells + central spread sensitivities).
- `corrected_summary.json` — surface + v2 restatement + CBO update + headline annuals, machine-readable.
- `tau_maturity_exhibit.md`, `exhibit_stats.py`, `exhibit_stats.json`, `exhibit_data/fred_{IOER,IORB,DTB3}.csv` — empirical exhibit and its raw data.
- `tests_tau_maturity.py` — 10 tests (front weight; front-end τ=1 identity; administered decline verified at 1.95pp; spread sign + long-segment invariance; corrected ≥ scalar at every τ_long on growing and flat; τ_long=0 still saves; split additivity; CBO guard; CBO figure). **Lane 3: 7/7. Lane 4: 10/10.**
