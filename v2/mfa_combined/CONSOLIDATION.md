# CONSOLIDATION.md — Combined-closure coverage: Monetary Symmetry Fee v2 + Medicare for America (H.R.10924)

**Lane 3 (consolidated financing arithmetic + CBO reconciliation), Combined Study.**
**Closure:** ALL fee savings — net receipts + reduced net interest + Δ Fed remittances, net of the v2 final pass's FRB/US Regime C feedback — are banked in one non-recycling ledger and directed to MFA. Nothing is re-spent by any fiscal rule.
**Code:** `consolidation_combined.py` (imports `../integration/consolidation.py` unmodified), `run_combined.py`. **Outputs:** `coverage_surface.csv`, `coverage_annual_growing.csv`, `coverage_annual_flat.csv`, `cbo_reconciliation.json`, `combined_summary.json`. **Tests:** 7 new (`tests_combined.py`) + v2 integration suite 23 — **30/30 pass**; v2 originals untouched.

> **Standing caveats.** (1) There is **no CBO/JCT/CMS score of H.R.10924**; MFA residuals are Lane 1's verified modeller's construction. (2) **τ (transmission of the halved administered-rate path into new-issue Treasury yields) is UNESTIMATED** — every result is τ-conditional; nothing is integrated over τ. (3) The **13% tax-interaction haircut is ASSUMED, unestimated** (carried from v1); gross collections are shown beside net everywhere. (4) **Lane 2's load-bearing caveat applies to every FRB/US comparison below:** Title II receipts enter FRB/US via `ugfsrp` and are **demand-neutral in-model** (no tax-incidence carrier exists), so MFA-only and combined demand impulses — and the receipts they induce — are overstated in that basis.

---

## 1. Method in one page

**Fee contribution (annual)** = net fee receipts (unified base, floating, central turnover, θ=1.0, erosion E=0.10) **after** the v2 final pass's Regime C treatment — Lane B fee-path ratio 1.1098 applied, Regime C endogenous drag (−$2,667B cumulative) carried as its own line — **+ Δ remittances + interest savings(τ) on the combined debt path**. Window totals of the τ-independent parts: gross collections **$4,625B**; net receipts at skeleton path $3,650B; net receipts after fee-path reconciliation **$4,050B**; drag **−$2,667B**; Δ remittances **+$410B**.

**Growing baseline debt path (Task 1a).** No CBO debt path existed in the project files (`mfa/data/parameters.csv` carries MFA parameters only; `v2/cohort/fiscal.py` is a flat-stock repricing skeleton), so the path is **constructed from CBO's February 2026 Budget & Economic Outlook** ("By the Numbers": deficit FY2027 **$1,887B**, FY2036 **$3,115B**, cumulative FY2027–36 deficits **$24.4T**, debt held by public $32,095B → $56,152B). Construction: deficits grow geometrically at the rate implied by the two endpoint anchors, rescaled (×0.992) so the window sum is exactly $24,400B (endpoints land at $1,875B / $3,095B, within 1% of published). Marketable debt starts at the project's MSPD value **$31,830B** (end-FY2026) and grows by each deficit × 0.9917 (the marketable share of debt held by public at end-FY2026; nonmarketable held-by-public treated as a stable residual — documented simplification). Result: marketable debt **$33,690B (end-FY2027) → $56,029B (end-FY2036)**, against CBO's $56,152B held-by-public endpoint. Same coverage concept as v2 throughout: marketable debt only, savings on the non-Fed-held share (×0.8559), remittances separate.

**Combined path (Task 1b).** Year by year FY2027–36, per (τ × MFA scenario):
`D_t = Baseline_t + cumResidual_t − cumNetReceipts_t − cumDragEffect_t − cumRemittances_t − cumSavings_t`
(drag is negative, so it adds to debt; a negative MFA residual subtracts). Interest savings are the **rate effect only** — (3.57% baseline average rate − plan average rate) × average combined debt × 0.8559 — with bucket repricing per the cohort skeleton (WAM 70 months; bills/FRN reprice fully each year, notes 13.5%, TIPS 10%, bonds 3.5%; new-issue only; dy_t = −τ×(IORB_base − IORB_ms), zero before FY2030, headline decline **0.975pp at τ=0.5**). Rate-effect-only is what keeps the ledger single: the debt-*level* effect of receipts/residuals is already in the path itself. **Fixed point:** savings ↔ path iterated until max annual savings change < **$0.05B**; convergence in **≤3 iterations** in all 12 growing cells.

**Shortfall definitions.** *First cumulative-negative year* = first year the cumulative plan position (cum contribution − cum residual) goes below zero. *First annual shortfall year* = first year the annual MFA residual exceeds the annual fee contribution. Both are reported; they answer different questions (ledger solvency vs year-by-year cash cover).

---

## 2. Coverage surface — GROWING path (headline), FY2027–36, $B

Fee contribution is identical across scenarios except for interest savings (the MFA scenario moves the debt path, hence the savings base). Net receipts $4,050B, drag −$2,667B, Δ remittances +$410B in every cell.

| τ | Scenario | Interest savings | Fee contribution | MFA residual | **Coverage margin** | Financed? | First cum.-negative yr | First annual shortfall yr |
|---|---|---:|---:|---:|:--|:--|:--|:--|
| 0 | low | 0 | 1,793 | −1,289 | **+3,082** | ✅ | — | — |
| 0 | **central** | 0 | 1,793 | +2,524 | **−731** | ❌ | 2035 | 2030 |
| 0 | high-stress | 0 | 1,793 | +10,730 | **−8,937** | ❌ | 2030 | 2030 |
| 0.25 | low | 667 | 2,459 | −1,289 | **+3,749** | ✅ | — | — |
| 0.25 | **central** | 690 | 2,483 | +2,524 | **−40** | ❌ (break-even) | 2036 | 2030 |
| 0.25 | high-stress | 742 | 2,535 | +10,730 | **−8,195** | ❌ | 2030 | 2030 |
| 0.5 | low | 1,324 | 3,117 | −1,289 | **+4,406** | ✅ | — | — |
| 0.5 | **central** | 1,372 | 3,164 | +2,524 | **+641** | ✅ | — | 2030 |
| 0.5 | high-stress | 1,475 | 3,268 | +10,730 | **−7,463** | ❌ | 2030 | 2030 |
| 0.75 | low | 1,973 | 3,765 | −1,289 | **+5,055** | ✅ | — | — |
| 0.75 | **central** | 2,043 | 3,836 | +2,524 | **+1,312** | ✅ | — | 2035 |
| 0.75 | high-stress | 2,198 | 3,990 | +10,730 | **−6,740** | ❌ | 2030 | 2030 |

**Verdict.** **Low:** financed at every τ — indeed MFA needs no fee contribution at all (residual −$1.29T); the fee ledger is pure surplus. **Central:** financed **iff τ ≳ 0.5** on the growing path (τ=0.25 misses by $40B — a rounding-distance break-even, not a margin; τ=0 misses by $731B). **High-stress:** not financed at any τ (best case −$6.74T at τ=0.75); the fee covers at most 37% of the high-stress residual.

**Timing is the central case's real constraint.** The residual is back-loaded (2035 +$891B, 2036 +$993B = 75% of it) while the fee contribution is comparatively flat, so even where the window is financed the **annual** ledger shortfalls: at τ=0.5 the annual margin is negative in **2030 (−$45B), 2035 (−$289B) and 2036 (−$326B)**, covered by the banked 2028–34 surplus (cumulative position peaks at +$1,256B in 2034 and ends at +$641B). At τ=0.75 only 2035–36 shortfall annually. At τ≤0.25 the cumulative ledger itself goes negative (2035 at τ=0; only in the final year, 2036, at τ=0.25). Under a strict pay-as-you-go reading (no banking across years) the central case is **not** year-by-year financed at any τ; under the stated spending closure (banked ledger) it is financed at τ≥0.5.

### Annual table — central case, growing path, τ=0.5 ($B)

| FY | Gross coll. | Net receipts (FB-adj) | FRB/US drag | Δ remit | Interest savings | **Contribution** | MFA residual | Annual margin | Cum. margin | Baseline debt | Combined debt |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2027 | 0 | 0 | 0 | 0 | 0 | **0** | 0 | 0 | 0 | 33,690 | 33,690 |
| 2028 | 7 | 6 | −1 | 0 | 0 | **6** | −236 | +242 | +242 | 35,656 | 35,414 |
| 2029 | 126 | 116 | −92 | 0 | 0 | **25** | −256 | +281 | +523 | 37,734 | 37,212 |
| 2030 | 370 | 336 | −243 | 9 | 105 | **206** | +252 | −45 | +478 | 39,932 | 39,454 |
| 2031 | 476 | 423 | −336 | 104 | 135 | **327** | +127 | +200 | +678 | 42,255 | 41,578 |
| 2032 | 570 | 496 | −366 | 63 | 165 | **358** | +197 | +161 | +839 | 44,712 | 43,874 |
| 2033 | 656 | 570 | −378 | 59 | 195 | **445** | +260 | +185 | +1,024 | 47,309 | 46,286 |
| 2034 | 735 | 638 | −393 | 59 | 225 | **528** | +296 | +232 | +1,256 | 50,056 | 48,799 |
| 2035 | 808 | 702 | −415 | 59 | 256 | **602** | +891 | −289 | +967 | 52,959 | 51,992 |
| 2036 | 878 | 763 | −444 | 59 | 290 | **667** | +993 | −326 | **+641** | 56,029 | 55,388 |
| **Total** | **4,625** | **4,050** | **−2,667** | **410** | **1,372** | **3,164** | **2,524** | | **+641** | | |

End-FY2036 combined debt at τ=0.5/central is $55,388B — $641B below the CBO baseline path, exactly the coverage margin (one-ledger check). Full annual tables for all 12 cells: `coverage_annual_growing.csv`.

---

## 3. Flat-debt sensitivity — the size of the v2 conservatism

Same table on v2's banked convention (debt held flat at $31,830B; savings from v2's own machinery — the fee-only totals reproduce the banked FINAL numbers **exactly**: $1,793 / $2,262 / $2,731 / $3,201B):

| τ | Central contribution (flat) | Central margin (flat) | Central margin (growing) | **Growing-path effect on margin** |
|---|---:|---:|---:|---:|
| 0 | 1,793 | −731 | −731 | 0 |
| 0.25 | 2,262 | −261 | −40 | **+221** |
| 0.5 | 2,731 | +208 | +641 | **+433** |
| 0.75 | 3,201 | +677 | +1,312 | **+635** |

**The growing path does not change any coverage verdict** — central is financed at τ≥0.5 on both bases, high-stress at none, low at all — but it **roughly triples the central τ=0.5 margin** (+$208B → +$641B) and turns τ=0.25 from a clear miss (−$261B) into a break-even (−$40B). The v2 flat-stock convention was worth **$221–635B of conservatism** across the τ surface. (Full flat surface: `coverage_surface.csv` / `coverage_annual_flat.csv`; flat first-shortfall years are identical to growing except τ=0.25 central, cum.-negative 2036 on both.)

---

## 4. Interest-savings EROSION (required headline)

Two different comparisons, kept separate because they have opposite signs:

**(i) Combined path vs the BANKED (flat) path — negative erosion, i.e. a gain.** Interest savings on the combined growing path **exceed** the banked flat-path savings at every τ, because the repricing base grows from $31.8T toward $56T:

| τ | Banked flat savings | Combined, low | Combined, central | Combined, high-stress | Central Δ vs banked |
|---|---:|---:|---:|---:|---:|
| 0.25 | 469 | 667 | 690 | 742 | **+221** |
| 0.5 | 939 | 1,324 | 1,372 | 1,475 | **+433** |
| 0.75 | 1,408 | 1,973 | 2,043 | 2,198 | **+635** |

**(ii) Self-erosion vs the growing baseline path (no plan) — the true erosion.** The plan's own debt reduction shrinks the stock its savings are computed on. Against savings on the untouched growing baseline ($699B / $1,397B / $2,096B at τ=0.25/0.5/0.75):

| τ | Low | Central | High-stress |
|---|---:|---:|---:|
| 0.25 | +32 (eroded) | +8 | **−44 (augmented)** |
| 0.5 | +73 | **+26** | **−78** |
| 0.75 | +123 | +52 | **−102** |

Self-erosion is **small — $26B (1.9%) at τ=0.5 central** — and **reverses sign in the high-stress case**: MFA's added debt enlarges the repricing base by more than the fee shrinks it, so combined savings *exceed* the no-plan growing-baseline savings. Headline: **the v2 flat-debt conservatism (+$433B at τ=0.5) is ~17× the combined-path self-erosion (−$26B)**; erosion is a second-order correction, debt growth is the first-order one.

---

## 5. The FRB/US tension (Task 1d) — two bases, not averaged

| | Consolidation τ-surface (this lane) | FRB/US in-model combined (Lane 2) |
|---|---|---|
| Fee receipts basis | Unified base; fee path at the **fee-only** fixed point (f≈2.10%), ratio-adjusted: net $4,050B | **Loan-only** κ lower bound; fee path **re-solved with MFA in place**: f = rff = **3.70%**, receipts **$6,628B** |
| Interest effect | τ-surface on the debt stock: **+$939B (flat) / +$1,372B (growing, τ=0.5)** | In-model Δinterest only **+$192B** saving — the combined funds path sits **+0.41pp ABOVE baseline**, so the rate channel nearly vanishes |
| Endogenous drag | Fee-only Regime C drag imposed: **−$2,667B** | Combined endogenous term: **+$856B** (economy runs at/above baseline) |
| MFA residual treatment | Lane 1 static residual +$2,524B charged against the ledger | MFA flows imposed directly; MFA-only Δsurplus is **−$1,242B** despite the +$2,523B static residual, because the MFA-only rate path (+2.33pp) adds **+$3,547B** of in-model interest |
| **Central-case bottom line** | Margin **−$731B (τ=0) … +$641B (τ=0.5, growing) … +$1,312B (τ=0.75)** | Δsurplus **+$5,153B** after MFA (loan-only). First-order unified adjustment (×1.347, the unified/loans-only gross-collections ratio; receipts enter Lane 2's surplus dollar-for-dollar): **≈ +$7.5T** |

**Why they differ — three mechanisms, in size order.**
1. **Receipt endogeneity (+$2,819B loan-only).** In FRB/US the fee is chained to the funds rate, and MFA's $11.8T demand impulse lifts the inertial Taylor rule's path above baseline; the fixed point re-solves at f=3.70% and receipts rise **+74%** over fee-only. The τ-surface holds the fee path at its fee-only fixed point by construction — it prices the *yield* channel (τ) and cannot see the *rate-level* channel. This is the dominant wedge.
2. **The drag sign flip (+$3.5T swing).** The τ-surface charges the combined plan the fee-only drag (−$2,667B). Lane 2's combined endogenous term is **+$856B**, because in-model MFA is close to a pure demand stimulus: its $11.8T of purchases enter demand in full while its $9.3T of receipts (Title II above all) are **demand-neutral residual entries — the load-bearing caveat**. A routing that gave Title II real incidence would move this term back toward (or past) zero; the interface rules that routing out, so the honest statement is that FRB/US's combined drag is an **upper bound** in the favourable direction, just as the fee-only drag was an upper bound in the adverse direction.
3. **Interest (opposite signs, smaller).** FRB/US prices interest off its own rff path — above baseline in the combined run, so saving ≈ $192B and MFA-only actually *pays* $3.5T of extra interest. The τ-surface prices the term-structure/new-issue channel FRB/US does not carry: τ×0.975pp repricing through a 70-month WAM. Both cannot be right about the rate path at once; they are answers to different questions (monetary-rule reaction vs yield-curve transmission), which is why this report **presents both and averages neither**.

**Which mechanism dominates under the spending closure?** In the FRB/US basis, the receipts/demand channel dominates and the plan is comfortably financed in the central case (+$5.2T loan-only) — but that dominance is *manufactured in part by the demand-neutral Title II routing*. In the consolidation basis, the binding margin is τ: the plan is financed centrally only if at least half the administered-rate decline transmits to new-issue yields. The two bases agree on the two robust verdicts — **low: financed; high-stress: not financed** (Lane 2 high-stress Δsurplus −$1,514B even with receipts lifted to $8,221B) — and disagree only on the central case, where the truth depends on two unmodelled/unestimated objects (Title II incidence; τ). Neither basis licenses calling the central case settled.

---

## 6. Task 2 — CBO rule-of-thumb reconciliation exhibit

**CBO rule** ("How Changes in Economic Conditions Might Affect the Federal Budget: 2026 to 2036"): all rates +0.1pp each year → deficits **+$379B** cumulative 2027–36, symmetric for lower rates ⇒ **$379B of net-interest saving per 0.1pp** of sustained curve decline. **Used here only as a comparator — never as an input anywhere in the coverage machinery** (a test asserts the figure appears nowhere outside this exhibit's code path). τ remains unestimated. (The v1 prototype's $3.79T/pp plug-in was killed by audit for exactly the plug-in error; this exhibit exists to price v2's mechanics against CBO's rule, not to import it.)

**Model figure, consistent definition.** At τ=0.5 the skeleton's new-issue decline is **0.975pp** (τ × 1.95pp). v2 booked, on the flat path, **$939B consolidated interest savings + $410B Δ remittances**. Interest only, consolidated: $939B / 9.75 tenths = **$96B per 0.1pp**. Gross (before the Fed-share consolidation): $1,097B ⇒ **$112B per 0.1pp**. Gap vs CBO: **$379B − $96B = $283B per 0.1pp** to explain.

### Wedge table (per 0.1pp of headline decline, τ=0.5 basis, $B)

| # | Wedge | Size | Running figure |
|---|---|---:|---:|
| | CBO rule (unified net interest, full curve, growing debt, compounding) | | **379** |
| (d) | **Coverage**: model prices **marketable debt only** ($31,830B of $40,100B total debt = 79%); CBO's net-interest concept spans the whole federal balance sheet incl. nonmarketable and new baseline borrowing's own interest | ≈ −78 pro-rata (379 × (1 − 0.79)); exhibit attribution, see note | ~301 |
| (c) | **Debt growth + borrow-to-pay-interest compounding**: re-running the model's interest line on the **growing CBO path, no MFA, no plan feedback** raises savings from $939B to **$1,397B** (per-0.1pp: $96B → **$143B**) | **+$47 of model figure; closes 17% of the $283B gap** | model: 143 |
| (b) | **Repricing path**: WAM 70 months, new-issue only, and dy=0 until FY2030 (IORB paths diverge only then). Instant full repricing of the flat stock at 0.975pp for 10 years would book $2,656B consolidated; the model books $939B — a **35% realization share**. Effective average decline actually realized over the window: **0.34pp**, not 0.975pp | factor ×0.35 — the **largest single wedge** | — |
| (a) | **Fed-held share / consolidation**: savings counted only on the non-Fed-held share (×0.8559): gross $1,097B → consolidated $939B, a **−$158B** window wedge (**−$16B per 0.1pp**). Partly returned through the separate remittance ledger: **Δ remittances +$410B** — but that is the IORB-*expense* channel (cheaper reserves), not portfolio-yield pass-through, and it is **not** part of the $96B interest figure | −16 (interest line); +410 carried separately | — |
| | **Model, flat, consolidated (as booked in v2)** | | **96** |
| | **Model, growing path, no plan (wedge (c) removed)** | | **143** |

Note on (d): the −78 is a pro-rata attribution (379 × (1 − 31,830/40,100)); part of CBO's wider base is intragovernmental and nets out in consolidation, so this is an upper-bound attribution, not a model run, and is labeled as such. The wedges are not strictly additive — (b) and (c) interact (repricing applies to a growing stock) — so the table prices each wedge on the model's own arithmetic where a run exists ((a) exact, (c) an actual re-run) and flags the one attribution ((d)) that is arithmetic-on-CBO's side.

**Bottom line of the exhibit.** The model's $96B/0.1pp vs CBO's $379B/0.1pp is **not** a contradiction: ~⅓ of the gap is the repricing realization share (the model's decline reaches only ~35% of the stock's average rate inside the window, and starts in FY2030), ~17% is closed by debt growth alone, ~$16B/0.1pp is the deliberate Fed-share consolidation (with +$410B returned via remittances on a separate line), and the remainder is coverage (marketable-only, no compounding of baseline borrowing). A model that booked CBO's $379B/0.1pp against this fee would be double-counting channels the v2 ledger deliberately separates.

---

## 7. Assumptions ledger (all ASSUMED items, labeled)

| Parameter | Value | Status |
|---|---|---|
| Tax-interaction haircut on fee receipts | 13% | **ASSUMED, unestimated** (v1 carry-over) — first among assumptions; gross shown beside net throughout |
| τ (yield transmission) | {0, 0.25, 0.5, 0.75} surface | **UNESTIMATED** — no published estimate exists; never integrated over |
| Substitution erosion E / θ coupling | E=0.10, θ=1.0, ∝θ, capped 60% | ASSUMED functional form (v2) |
| FRB/US feedback treatment | Regime C ratio 1.1098; drag scaled ∝ receipts | ASSUMED proportionality (v2 final pass) |
| Baseline deficit path shape | Geometric between CBO endpoints, rescaled to $24.4T | CONSTRUCTION on published CBO anchors |
| Marketable share of incremental borrowing | 0.9917, constant | Simplification (end-FY2026 ratio) |
| Bucket maturity fractions | bills/FRN 1.00, notes 0.135, TIPS 0.10, bonds 0.035 | ASSUMED (cohort skeleton; calibrated to published 33% year-1 repricing share) |
| Fed-held share | 4,587.1/31,830 = 14.41% | Published H.4.1/MSPD, held constant |
| Title II annual profile (inside Lane 1 residuals) | 4.2%/yr growth, normalized to window totals | Lane 1's documented assumption |
| Average rate on marketable debt | 3.57% flat | Published Oct 2026; held flat per v2 convention (CBO's baseline avg rate rises — a further conservatism, unquantified here) |

## 8. Files

- `consolidation_combined.py` — engine (imports v2 machinery unmodified); `run_combined.py` — runner.
- `coverage_surface.csv` — 24 rows (τ × scenario × {growing, flat}): itemized contribution, residual, margin, shortfall years, iterations, end-2036 combined debt.
- `coverage_annual_growing.csv` / `coverage_annual_flat.csv` — annual tables, all cells.
- `cbo_reconciliation.json`, `combined_summary.json` — exhibit + everything cited above, machine-readable.
- `tests_combined.py` — 7 tests (baseline anchors; flat = banked totals; τ=0 ⇒ zero savings; ledger identities + convergence; monotonicity; Lane 1 residual totals; CBO exhibit arithmetic + no-plug-in guard). **v2 integration suite: 23/23. Lane 3: 7/7.**
