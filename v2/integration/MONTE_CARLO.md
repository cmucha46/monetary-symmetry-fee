# MONTE_CARLO.md — MSF v2 grid enumeration over documented uncertainties

**Base: UNIFIED (loans + corporate bonds + municipal bonds), headline** —
per the Nov 22, 2026 sponsor decision. The loans-only sensitivity surface
is in §4.

## 1. What this is — and what it is not

This is **discrete grid enumeration**, not Monte Carlo sampling from
calibrated distributions. The decisive parameters of this design —
pass-through at fee scale, substitution/erosion rates, and τ — are
**UNCALIBRATED** in the published literature (LITERATURE.md §5). Drawing
them from invented distributions and reporting percentiles would fabricate
precision, so instead every documented grid combination is run once, with
equal weight:

| Dimension | Values | Source |
|---|---|---|
| Turnover | low / central / high | Cohort lane δ cases (DATA.md §2) |
| Fee design | floating / locked | Memo §II.D (both designs modeled) |
| Pass-through θ | 0.5 / 0.75 / 1.0 / 1.15 | LITERATURE.md §2.3 grid (fee scale UNCALIBRATED) |
| Erosion E (year-5, at θ=1) | 0 / 10% / 25% / 40% | LITERATURE.md §3.2–3.3 grids, overlap-adjusted into a single slot |
| Deposit β | 0.45 / 0.55 / 0.65 | LITERATURE.md §4.1 — **inert in this layer** (see §3) |

3 × 2 × 4 × 4 × 3 = **288 combinations per τ**, each evaluated at
τ ∈ {0, 0.25, 0.5, 0.75} and **reported only per τ**. The means, medians
and ranges below summarize a conditional simulation grid. **They are not
confidence intervals, not posterior distributions, and not forecasts.**

## 2. Ten-year consolidated net benefit by τ ($B, unified base)

| τ | Mean | Median | p25 | p75 | Min | Max |
|---|---|---|---|---|---|---|
| 0 | 3,510 | 3,502 | 3,024 | 3,962 | 1,995 | 4,916 |
| 0.25 | 3,979 | 3,971 | 3,494 | 4,432 | 2,464 | 5,386 |
| 0.5 | 4,449 | 4,440 | 3,963 | 4,901 | 2,933 | 5,855 |
| 0.75 | 4,918 | 4,910 | 4,432 | 5,370 | 3,403 | 6,324 |

Reading: the grid spread at fixed τ (~$2.9T min-to-max) is roughly twice
the τ spread of the medians (~$1.4T from τ=0 to τ=0.75) — the behavioral
grid (turnover × design × erosion) moves the answer more than the
yield-transmission parameter the literature cannot discipline. The $6T
hypothesis is exceeded **only** at the grid's extreme corner (τ=0.75,
max $6,324B: high turnover + floating + zero erosion + θ=0.5); the median
at τ=0.75 is $4,910B and the central case (FISCAL_PROJECTION.md) is
$5,467B. $6T is a tail outcome of jointly favorable assumptions, not a
central result, on either base.

## 3. Attribution — median 10-year consolidated net by dimension ($B, unified)

**By fee design** (floating beats locked at every τ — locked vintages keep
origination-era rates while the synchronized rate rises above them):

| Design | τ=0 | τ=0.25 | τ=0.5 | τ=0.75 |
|---|---|---|---|---|
| Floating | 3,893 | 4,363 | 4,832 | 5,301 |
| Locked | 3,237 | 3,706 | 4,175 | 4,644 |

**By turnover case** (phase-in speed is worth ~$820B of median benefit):

| Turnover | τ=0 | τ=0.25 | τ=0.5 | τ=0.75 |
|---|---|---|---|
| Low | 3,099 | 3,568 | 4,038 | 4,507 |
| Central | 3,520 | 3,989 | 4,459 | 4,928 |
| High | 3,917 | 4,386 | 4,856 | 5,325 |

**By erosion E** (the widest single behavioral lever):

| Erosion (yr-5) | τ=0 | τ=0.25 | τ=0.5 | τ=0.75 |
|---|---|---|---|---|
| 0% | 4,026 | 4,496 | 4,965 | 5,434 |
| 10% | 3,741 | 4,210 | 4,680 | 5,149 |
| 25% | 3,304 | 3,774 | 4,243 | 4,712 |
| 40% | 2,846 | 3,316 | 3,785 | 4,254 |

**β (deposit beta) attribution: none — deliberately.** β takes all three
grid values in the run file, and the results are identical across them
(verified: within every identical combination of the other dimensions,
the consolidated total is unique across β), because the Fed remittance
identity (portfolio income − IORB × reserves − opex) contains no
deposit-beta term. β operates on *bank funding costs and deposit
spreads* — the SFC layer's territory. It is carried in the run schema so
the later SFC pass can wire it in without re-specifying the grid;
reporting a β "effect" here would require inventing a channel. θ likewise
enters *only* through the erosion slot (θ scales the erosion rate;
statutory collections do not depend on who bears the fee).

## 4. Sensitivity — loans-only base

Ten-year consolidated net by τ ($B), full grid on the loans-only base:

| τ | Mean | Median | p25 | p75 | Min | Max |
|---|---|---|---|---|---|---|
| 0 | 2,722 | 2,713 | 2,375 | 3,052 | 1,606 | 3,736 |
| 0.25 | 3,191 | 3,182 | 2,844 | 3,522 | 2,075 | 4,206 |
| 0.5 | 3,660 | 3,652 | 3,314 | 3,991 | 2,545 | 4,675 |
| 0.75 | 4,129 | 4,121 | 3,783 | 4,460 | 3,014 | 5,144 |

Base breadth (unified vs. loans-only) shifts the median by ~$790B at
every τ — material, but smaller than the erosion dimension's spread.
Machine-readable: `outputs/monte_carlo_summary_loans_only.csv`,
`outputs/monte_carlo_runs_loans_only.csv`.

## 5. Where the central case sits

The FISCAL_PROJECTION.md central case (central turnover, floating,
θ=1.0, E=10%, unified) totals $4,059B / $4,529B / $4,998B / $5,467B at
τ = 0 / .25 / .5 / .75 — above the grid median at each τ, because the
median run averages in the locked design and the 25–40% erosion cells.
Neither the central case nor the median is "the" answer; the surface is
the answer, per τ, until the FRB/US and SFC lanes replace the scenario
IORB paths with modeled ones.

Machine-readable: `outputs/monte_carlo_runs.csv` (1,152 rows),
`outputs/monte_carlo_summary.csv`, `outputs/monte_carlo_by_*.csv`.
