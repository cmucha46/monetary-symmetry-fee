# MONTE CARLO V2 — Parameter uncertainty over the fiscal module (Lane I)

**Status: conditional simulation ranges under judgemental priors — NOT
confidence intervals, NOT a forecast, NOT a dial estimate.** This layer
samples the fiscal module's own parameters and re-runs the unchanged
deterministic machinery (`cohort.run_cohorts` + `sfc.run_ledger_pair`,
the same code behind RESULTS_V1/V2). It contains no macro model and no
Fed-discretion dial: s is fixed per scenario at 50 / 75 / 90%, exactly
as in the deterministic grid. Code: `src/monetary_symmetry/montecarlo.py`,
runner `python3 run_montecarlo.py` (seed **20261114**, **10,000 draws**,
~11 s). Tests: `tests/test_montecarlo.py` (full suite **56 passed**).

Machine-readable outputs:

| File | Contents |
|---|---|
| `results/montecarlo_v2.csv` | Per-dial summary: mean / median / p10 / p90 for every fiscal line, P(≥$6T), deterministic reference, τ bounds, flow-channel output |
| `results/montecarlo_annual_v2.csv` | Per-dial, per-year distributions of every annual line |
| `results/montecarlo_draws_v2.csv` | All 10,000 stored draws (parameters + per-dial totals) behind the regressions below |
| `results/montecarlo_sensitivity_v2.csv` | Standardised regression coefficients + Spearman ρ, per dial |

## 1. Method

Each parameter draw is evaluated at **all three dials** (common random
numbers), so within-draw dial differences are pure design comparisons
and the sensitivity regressions share one parameter sample. Per draw,
the sampled stance path is used as *both* the baseline stance and the
scenario's desired stance: the fee rate and both interest channels are
driven by the **same** IORB shock — fee and interest are never sampled
independently. The MC runner is proven (test) to reproduce
`score.run_scenario` totals to 1e-9 when every parameter sits at its
deterministic default; seed reproducibility is exact, and the SFC
accounting identities (consolidated = public-yield + IORB/remittance;
combined = net fee + consolidated) hold on every sampled draw tested.

## 2. Priors — every one judgemental, none estimated

Provenance: **(P)** = prototype prior (audit §2 of
`../audit/PROTOTYPE_AUDIT.md`), re-centred where this module's
structure differs; **(A)** = analyst choice made in this lane;
**(L)** = Lane F/H structure carried in.

| Parameter | Prior | Provenance / note |
|---|---|---|
| β pass-through | clipped N(0.88, 0.11) on [0.55, 1.00] | (P) prototype #6 verbatim. 13.8% of draws pile at the 1.00 clip (audit found 13.3% in the prototype); β > 1 (over-shifting) is excluded by construction — a known, disclosed restriction |
| τ yield transmission | clipped N(0.32, 0.13) on [0.07, 0.65] | (P) prototype #7, now acting through the SFC repricing schedule, not a plug-in. **Exactly linear** in the coupon term — see §5 |
| Covered base variant | discrete: central `loans_plus_securitized` 50% / strict `loans_only` 30% / `lane_e_proxy` 20% | (A) weights are analyst choices, not data; (L) the three variants are Lane F's sourced definitions. Replaces the prototype's single invented covered-share draw (#1) |
| Turnover, per category | relative factor clipped N(1.00, 0.125) on [0.75, 1.25], independent per category, × config defaults | (A) ±25% relative around this module's per-category placeholder defaults; prototype had one invented aggregate (#2) |
| Avoidance per fee pp | one draw clipped N(0.065, 0.035) on [0.01, 0.16]; category defaults scaled by draw/0.065 | (P) prototype #5 centre/support; scaling preserves the config's cross-category relativities |
| Tax-interaction haircut | clipped N(0.13, 0.055) on [0.02, 0.33]; net = gross × (1 − haircut) | (P) support matches prototype #4's implied 2–33%; centred on v1's 13% placeholder. **Unestimated** — no JCT score for this instrument exists |
| IORB desired-stance path | baseline path + AR(1) deviations: ρ = 0.7, stationary sd 0.5 pp, floored at 0.05 pp | (A) ρ and sd are analyst choices. One shock path drives fee + interest jointly (see §1) |
| Private debt growth | clipped N(0.038, 0.012) on [0.005, 0.075] | (P) prototype #15 verbatim |
| Creditor MPC / multiplier | U(0.10, 0.40) / U(1.0, 1.5) | (L) Lane H's labelled ranges, sampled — used **only** for the §6 flow-channel output; null-verified to not touch fiscal totals (§4) |

**Not sampled (held at v1 placeholders, a stated gap):** the public-debt
stock path and repricing shares inside `LedgerParams`, reserve stock,
Fed balance-sheet yields, the 2028/29 phase-in schedule, and fixed/
floating cohort shares. Sampling them would widen the ranges further.

## 3. Results — FY2027–36, $T (10,000 draws)

Combined = net fee + consolidated interest saving. "P(≥$6T)" is
**prior mass above $6T under the priors in §2 — not a calibrated
probability** (the prototype audit's verdict on its own 34% figure
applies here word for word).

### s = 50%

| Line | Mean | Median | p10 | p90 |
|---|---|---|---|---|
| Gross fee | 3.53 | 3.52 | 2.66 | 4.41 |
| Net fee | 3.07 | 3.05 | 2.29 | 3.88 |
| Public-yield saving | 0.84 | 0.83 | 0.39 | 1.30 |
| IORB/remittance saving | 0.34 | 0.34 | 0.29 | 0.40 |
| Consolidated interest | 1.19 | 1.17 | 0.72 | 1.67 |
| **Combined** | **4.26** | **4.22** | **3.32** | **5.24** |

P(combined ≥ $6T) = **1.7%** · P(net fee ≥ $6T) = **0.0%** · deterministic $4.44T

### s = 75% (centre dial)

| Line | Mean | Median | p10 | p90 |
|---|---|---|---|---|
| Gross fee | 5.28 | 5.22 | 3.91 | 6.69 |
| Net fee | 4.59 | 4.52 | 3.36 | 5.88 |
| Public-yield saving | 1.34 | 1.31 | 0.63 | 2.07 |
| IORB/remittance saving | 0.54 | 0.54 | 0.47 | 0.62 |
| Consolidated interest | 1.88 | 1.85 | 1.15 | 2.64 |
| **Combined** | **6.47** | **6.40** | **4.99** | **8.03** |

P(combined ≥ $6T) = **63.2%** · P(net fee ≥ $6T) = **8.3%** · deterministic $6.71T

### s = 90%

| Line | Mean | Median | p10 | p90 |
|---|---|---|---|---|
| Gross fee | 6.33 | 6.23 | 4.62 | 8.15 |
| Net fee | 5.51 | 5.40 | 3.97 | 7.15 |
| Public-yield saving | 1.67 | 1.65 | 0.79 | 2.58 |
| IORB/remittance saving | 0.68 | 0.68 | 0.58 | 0.77 |
| Consolidated interest | 2.35 | 2.32 | 1.44 | 3.30 |
| **Combined** | **7.86** | **7.76** | **6.01** | **9.84** |

P(combined ≥ $6T) = **90.1%** · P(net fee ≥ $6T) = **32.1%** · deterministic $8.12T

**Reading.** The deterministic verdict survives the parameter cloud in
direction but not in comfort: at the 50% floor $6T is effectively dead
(1.7% of prior mass, p90 only $5.24T); at 75% it is a coin-flip weighted
to yes (63%); at 90% it is likely (90%) but the p10 ($6.01T) sits on the
line. The fee alone almost never reaches $6T net (0 / 8 / 32%) — the
interest channels are load-bearing at every dial, which is precisely
where the weakest priors (τ, stance path) live.

**Annual shape** (s = 75%, medians): gross fee is $0.01T in 2028 (intro
year), $0.48T in 2030, $0.88T in 2036 — the phase-in artefact documented
since v1 persists under sampling; the 10-year totals are first-decade
numbers, not steady-state run rates. Full annual distributions in
`results/montecarlo_annual_v2.csv`.

## 4. What moves the total — sensitivity ranking

Standardised OLS coefficients on the stored draws (combined total;
Spearman ρ in `results/montecarlo_sensitivity_v2.csv` tells the same
story). Signs: variant_loans_only is a dummy vs the central base.

| Rank | s = 50% | s = 75% | s = 90% |
|---|---|---|---|
| 1 | stance path **+0.53** | stance path **+0.49** | stance path **+0.45** |
| 2 | variant: loans-only **−0.45** | τ **+0.44** | τ **+0.43** |
| 3 | τ **+0.44** | variant: loans-only **−0.43** | variant: loans-only **−0.41** |
| 4 | debt growth +0.33 | debt growth +0.31 | avoidance −0.37 |
| 5 | haircut −0.25 | avoidance −0.31 | debt growth +0.30 |
| 6 | avoidance −0.21 | haircut −0.24 | β −0.28 |
| 7 | β −0.09 | β −0.21 | haircut −0.23 |
| 8 | turnover +0.11 | turnover +0.10 | turnover +0.10 |

Three findings:

1. **The stance path is the single largest driver at every dial.**
   Because the fee is a multiple of IORB and both interest channels
   scale with the IORB drop, the (invented, symmetric) ±0.5 pp AR(1)
   stance uncertainty moves the 10-year total more than any
   behavioural parameter. Any future narrowing of these ranges has to
   start with the rate path, not the loan book.
2. **τ is the largest *structural* lever** (see §5), and the covered-base
   definition (loans-only dummy −0.41…−0.45) is nearly its equal —
   Lane F's data question and the yield-transmission assumption jointly
   decide whether s = 75% clears $6T.
3. **β's grip grows with the dial** (−0.09 → −0.28): at s = 90% the
   pass-through assumption matters as much as the haircut. Turnover —
   the parameter the cohort machinery most elaborately models — is
   nearly irrelevant (±25% moves the total by ~0.10 sd). MPC and
   multiplier coefficients on fiscal totals are 0.000–0.001 at every
   dial: the designed null holds, confirming the flow-channel output
   cannot leak into the fiscal score.

## 5. τ sensitivity — explicit, with the bounding cases

In `sfc.py` the scenario new-issue yield falls by τ × (IORB drop), and
every downstream object (repriced public yield, interest on public
debt) is affine in that yield. The public-yield saving is therefore
**exactly linear in τ** (tested: effect at τ = 0.64 is 2× that at
0.32, to 1e-6; at τ = 0 it is exactly 0). Consequences, deterministic
(all other parameters at defaults):

| s | Combined at τ = 0 | at τ = 0.32 (default) | at τ = 1 | Public-yield at τ = 1 |
|---|---|---|---|---|
| 50% | 3.59 | 4.44 | 6.24 | 2.65 |
| 75% | 5.37 | 6.71 | 9.56 | **4.19** |
| 90% | 6.44 | 8.12 | 11.67 | 5.23 |

Each +0.10 of τ is worth ≈ +$0.42T of combined total at s = 75%.
τ = 0 alone — yields simply do not follow IORB down — kills $6T at
s = 75% ($5.37T) even with every other parameter at its centre, while
τ = 1 nearly doubles the interest line. Lane H independently computed
the same τ = 1 coupon figure ($4.19T) from the flow side; the two
modules agree because they share the ledger — treat that as a
consistency check, not independent confirmation. **τ is a placeholder
prototype prior. Nothing in this project estimates it.** The MC range
for τ ([0.07, 0.65] support) is narrower than the [0, 1] bound, so the
MC p10/p90 understate the full τ exposure; read the table above
alongside §3.

## 6. Flow-channel variant-(i) demand adjustment — SECONDARY, kept separate

Per Lane H's method with MPC and multiplier *sampled* (creditor MPC
U(0.10, 0.40); multiplier U(1.0, 1.5); foreign holders' 30% share of
the coupon term excluded from US demand): the fee regime's demand
effect relative to conventional, variant (i) (fee used for deficit
reduction). Negative = fee regime more contractionary. **This is a
potency offset, not revenue; it is never added to §3.**

| s | 2030–36 mean annual effect, % GDP: mean | median | p10 | p90 | 2036 median |
|---|---|---|---|---|---|
| 50% | −0.39 | −0.37 | −0.62 | −0.19 | −0.43 |
| 75% | −0.59 | −0.56 | −0.93 | −0.28 | −0.63 |
| 90% | −0.71 | −0.67 | −1.13 | −0.34 | −0.76 |

Consistency with Lane H: at s = 75%, Lane H's deterministic
range-of-ranges for 2036 was [−1.34%, −0.22%] of GDP (extremes of MPC
× multiplier stacked); the sampled p10–p90 [−1.07%, −0.32%] sits
inside it, as it must. Under Treasury-use variant (ii) (fee spent on
Medicare benefits) the sign of the fee term flips — see FLOW_CHANNEL.md;
that variant is not re-run here.

## 7. Why the MC median sits below the deterministic centre — the skew, explained

At every dial the MC median is ~4–5% below the deterministic combined
total (s = 75%: $6.40T vs $6.71T). This is **not** model drift; it is
the covered-base mixture. The deterministic score conditions on the
central variant; the MC median draw is a mixture draw. Conditional on
variant (s = 75%):

| Variant (weight) | Median combined | Mean | P(≥ $6T) |
|---|---|---|---|
| loans_plus_securitized (50%) | **6.67** | 6.73 | 74.1% |
| loans_only (30%) | 5.57 | 5.63 | 31.9% |
| lane_e_proxy (20%) | 6.97 | 7.07 | 82.2% |

Conditional on the central base, the median is within 0.6% of the
deterministic $6.71T — the priors are centred where they claim to be,
and the residual gap is the small net of the β clip pile-up (13.8% at
β = 1.00, pulling the fee down at high dials), stance-path convexity
near the floor, and Jensen effects in the avoidance exponential.
**Quote the mixture numbers as the headline (they encode the base
definition uncertainty), and the conditional numbers when comparing
against RESULTS_V2_BASE.md.**

## 8. Honest label

These are **conditional simulation ranges**: the spread you get when
this fiscal module's judgemental priors are propagated through its own
accounting. They are not confidence intervals (no parameter is
estimated, no sampling distribution is calibrated), and P(≥$6T) is
prior mass, not probability in any frequentist or calibrated-Bayesian
sense. The dominant uncertainties are, in order: the future IORB path
itself, τ, the statutory covered-base definition, and the dial —
which this lane deliberately does not distribute. A reader who
believes τ ≈ 0, or that coverage is loans-only, or that the Fed would
sit at the 50% floor, should read this report as saying $6T fails;
under the centred priors at s = 75–90%, it survives. That conditional
structure — not any single number — is the result.
