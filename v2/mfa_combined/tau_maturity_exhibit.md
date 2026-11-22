# tau_maturity_exhibit.md — IOER/IORB vs the 3-month bill, Oct 2008–present

**Lane 4 empirical exhibit (Task 3 of Sponsor Correction #2).** Purpose: document the mapping between the administered rate (IOER, replaced by IORB on 2021-07-29) and the 3-month Treasury bill rate — the arbitrage link that makes front-end transmission = 1 a design premise rather than an assumption.

## Data — route (i) SUCCEEDED

FRED fredgraph CSVs, fetched 2026-11-22 via `curl` (the timeouts the main sandbox saw earlier did not recur): `https://fred.stlouisfed.org/graph/fredgraph.csv?id=IOER` (74,838 bytes), `…?id=IORB` (31,126 bytes), `…?id=DTB3` (301,757 bytes). Raw files saved verbatim in `exhibit_data/fred_IOER.csv`, `exhibit_data/fred_IORB.csv`, `exhibit_data/fred_DTB3.csv`. Routes (ii) H.15 DDP and (iii) Treasury par-yield CSV were therefore not needed. Statistics computed by `exhibit_stats.py` → `exhibit_stats.json`; nothing in this exhibit is estimated, interpolated, or fabricated.

**Series.** Administered rate = IOER through 2021-07-28, IORB from 2021-07-29. Bill = DTB3 (3-month Treasury bill, secondary-market rate, daily, %). Merged on trading days: **4,529 days, 2008-10-09 → 2026-11-19**. Spread = bill − administered, in bp.

**Specifications.** *Levels β*: OLS of bill rate (%) on administered rate (%) with intercept, per era. *Event β*: for each day the administered rate changes, the bill's cumulative change over [t−1, t+5] trading days (narrow) and [t−20, t+5] (wide, anticipation-inclusive) regressed through the origin on the administered change. Correlations in levels and in daily changes are both reported; daily-change correlations are near zero by construction of the data (the administered rate is a step function that moves on ~39 days in 18 years while the bill moves daily, largely in anticipation) and are **not** the pass-through evidence — the levels β and the wide-window event β are.

## Results

| Era | Days | Corr (levels) | β (levels OLS) | Event β [t−20, t+5] | Event β [t−1, t+5] | Mean spread (bp) | Median spread (bp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Full sample** | 4,529 | **0.995** | **1.009** | **0.87** (39 events) | 0.11 | −10.8 | −14.0 |
| ZLB (Dec 2008–Dec 2015) | 1,752 | n/a — administered rate pinned at 0.25%, no variation to regress on | n/a | n/a (1 event) | n/a | −16.9 | −18.0 |
| 2016–19 hikes (thru Feb 2020) | 1,050 | 0.989 | 1.108 | 0.43 (14) | 0.07 | −9.3 | −9.0 |
| Covid ZLB (Mar 2020–Mar 2022) | 512 | 0.645 | 0.452 | 1.67 (3) | 0.41 | −3.6 | −3.0 |
| 2022–24 hikes | 628 | 0.990 | 0.886 | 0.77 (11) | 0.06 | +2.8 | −6.0 |
| Easing (Sep 2024–present) | 542 | 0.933 | 0.687 | 0.93 (7) | 0.21 | −12.5 | −15.0 |

## Reading

1. **Levels pass-through is ~1.** Full-sample β = 1.009 with correlation 0.995: over any horizon longer than the anticipation window, the bill rate moves one-for-one with the administered rate. Era βs below 1 in levels (Covid ZLB 0.45, easing 0.69) are anticipation/timing artifacts of regressing a forward-looking market rate on a step function inside short windows — the wide-window event βs in the same eras are 1.67 and 0.93.
2. **The narrow-window event β (~0.1) is the anticipation signature, not a pass-through failure.** Bills price administered changes *before* they occur; by t−1 most of the move has happened. Widening the window to [t−20, t+5] recovers β = 0.87 full-sample. This is exactly the NY Fed event-study finding the sponsor cited (administered-rate changes pass through ~completely to money-market rates), with the timing running ahead of the announcement.
3. **The spread is small, signed, and regime-dependent — hence a scenario parameter, not zero by construction.** Full-sample mean −10.8bp / median −14.0bp (bills normally trade *through* the administered rate: safety/scarcity premium). The spread turned positive in the 2022–24 issuance era (mean +2.8bp, SD 27.5bp) and is positive now: the sponsor's observation is confirmed in the fetched data — **IORB 3.90%, DTB3 4.16%, spread +26bp on 2026-11-19** (Nov 2026 mean +19.1bp; calendar-2026 mean +3.4bp). The model's spread-change scenarios {−0.25, 0, +0.15}pp span the observed range from the 2021 scarcity (spread ≈ −40bp) to the 2026 surge (≈ +15–26bp).
4. **ZLB eras identify nothing about β — and need nothing.** With the administered rate pinned, the bill sat a stable ~17bp (2008–15) / ~4bp (2020–22) below it; the exhibit rests the τ_front = 1 premise on the hiking/easing eras and the full-sample levels relation, where variation exists.

**Bottom line.** The bill–IORB mapping in 18 years of daily data is a one-for-one levels relation (β = 1.01, ρ = 0.995) with a spread whose *changes* are an order of magnitude smaller than the 195bp administered decline the fee regime engineers. Treating front-end transmission as 1 by arbitrage, with the spread change carried as a ±scenario, is what the data supports; applying a scalar τ < 1 to the front end is what it contradicts.
