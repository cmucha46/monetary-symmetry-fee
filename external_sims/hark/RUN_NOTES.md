# HARK §IX Channel Check — RUN NOTES

Date: 2026-11-22. Lane: RUN (partial equilibrium only). Script: `run_experiment.py`; raw output: `results.json`, `run_log.txt`; environment: `pip_freeze.txt`.

## Versions
- Python 3.12.3; econ-ark (HARK) 0.17.2; sympy 1.14.0 (installed pre-emptively per scout quirk); numpy 2.5.5; scipy 1.18.1; numba 0.68.1; quantecon 0.13.1. Full freeze in `pip_freeze.txt`.
- Install note: first `pip install` attempt failed on a truncated statsmodels wheel download (network `incomplete-download`); second attempt with `--resume-retries 20` succeeded cleanly. No other install/solve failures (one API fix: HARK 0.17 requires `T_sim` set before `initialize_sim()`).

## Design
`IndShockConsumerType` (buffer-stock, infinite horizon, `cycles=0`), solved separately for each of 7 discount-factor types, then simulated 300 periods, 2,000 agents per type (14,000 total), seed 12345 (+100 per type). The final-period cross-section is used as the stationary population (with LivPrb 0.98, deaths/newborns keep the simulated distribution stationary). MPC per agent = symmetric finite difference (ε=0.001) of that type's solved `cFunc` at the agent's normalized market resources mNrm.

Incidence contrast (exact, nonlinear — re-evaluating `cFunc`, not derivative-linearised): one total transitory shock = 0.10 × mean permanent income per capita (total 2,640.72 in model units, N=14,000), applied (a) pro-rata to end-of-period assets `aLvl` (interest-income-like incidence) and (b) uniform per capita (recycled-transfer-like incidence). Aggregate MPC = total first-period ΔC / total shock.

## Calibration and provenance
**One-line provenance: NO parameter is taken directly from cstwMPC's estimated values — the β-distribution centre/spread and all other parameters are HARK defaults / a documented approximation of the cstwMPC design (see below).**

| Parameter | Value | Source |
|---|---|---|
| CRRA | 2.0 | HARK `init_idiosyncratic_shocks` default |
| Rfree | 1.03 | HARK default |
| LivPrb | 0.98 | HARK default |
| PermGroFac | 1.01 | HARK default |
| PermShkStd / TranShkStd | 0.10 / 0.10 | HARK default income process (the Sabelhaus–Song-style process HARK ships as default) |
| UnempPrb / IncUnemp | 0.05 / 0.30 | HARK default |
| BoroCnstArt | 0.0 | HARK default |
| DiscFac (β) types | 0.93, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99 (equal population shares) | **Approximation (this run):** uniform 7-point grid centred on HARK's default β=0.96 with spread ±0.03, mimicking cstwMPC's uniform β-distribution (β̄, ∇) design. cstwMPC's own estimated (β̄, ∇) were NOT readily available — they are not in the installed HARK 0.17.2 package, and the REMARK repo's estimation code was not ported for this time-boxed run — so no cstwMPC estimated number is claimed here. |
| aXtraMax / aXtraCount | 30 / 48 | aXtraMax raised from default 20 to accommodate the most patient type; count is HARK default |
| AgentCount / periods | 2,000 per type / 300 | This run |

Sanity check on the approximation: despite not being estimated to match wealth inequality, the simulated distribution is strongly unequal in the cstwMPC direction — the top wealth quintile holds 70.4% of assets and the most patient type (β=0.99) holds mean assets 5.13 vs 0.62 for the least patient (β=0.93). Mean MPC falls monotonically in β: 0.333 (β=0.93) → 0.059 (β=0.99).

## MPC by wealth quintile (wealth = aLvl, final-period cross-section)

| Quintile | aLvl range | Mean aLvl | Wealth share | Mean MPC | Median MPC | Share MPC>0.9 |
|---|---|---|---|---|---|---|
| Q1 (poorest) | 0.000–0.305 | 0.177 | 2.2% | **0.393** | 0.342 | 9.4% |
| Q2 | 0.305–0.518 | 0.408 | 5.0% | **0.248** | 0.252 | 0.0% |
| Q3 | 0.518–0.836 | 0.659 | 8.1% | **0.199** | 0.191 | 0.0% |
| Q4 | 0.836–1.669 | 1.161 | 14.3% | **0.157** | 0.147 | 0.0% |
| Q5 (richest) | 1.669–225.30 | 5.723 | 70.4% | **0.100** | 0.063 | 0.0% |

Population aggregate MPC (derivative, uniform-weighted): **0.219**. Share of households at the borrowing constraint (aLvl < 1e-6): **1.88%** — and exactly that 1.88% have MPC > 0.9 (share with MPC > 0.5: 2.12%).

## The incidence contrast (same aggregate dollars, two distributions)

| Incidence | Aggregate ΔC (first period) | Aggregate MPC |
|---|---|---|
| (a) Pro-rata to assets | 296.13 | **0.112** |
| (b) Uniform per capita | 528.96 | **0.200** |

Ratio (a)/(b) = **0.56**; difference = **−0.088**. Distributing the same dollars as asset-proportional income produces only ~56% of the first-period consumption response of distributing them uniformly — the §IX asymmetry is present and quantitatively large in this PE model, driven by the negative wealth–MPC gradient above.

## Verdict vs the project's assumed ranges (§IX: creditor 0.05–0.20 / borrower 0.50–1.00)
- **Creditor side: SUPPORTED.** Asset-pro-rata incidence yields aggregate MPC 0.112, inside 0.05–0.20. The asset-weighted population is dominated by the top quintile (70% of assets, mean MPC 0.100, median 0.063), also inside the range.
- **Borrower side: NOT supported as a population average; supported only at the constraint.** No wealth quintile's *mean* MPC reaches 0.50 — even the poorest quintile averages 0.393. MPCs in the 0.50–1.00 range exist almost exclusively for the ~1.9% of households at the borrowing constraint (MPC ≈ 1). So if §IX's "borrower MPC 0.50–1.00" is meant as the MPC of *constrained / hand-to-mouth* households specifically, it is plausible; if it is meant as the average MPC of borrowers / lower-wealth households generally, this calibration says it is too high — ~0.25–0.39 for the bottom two quintiles is the model's answer. (Caveat: this model's "borrowers" are low-asset buffer-stock savers; it has no separate indebted-household sector, no housing, and no hand-to-mouth type imposed by construction — a two-agent or HANK model with an explicit HtM share would mechanically produce a higher low-end average.)

## What this does and does not establish
Does: disciplines ONE ingredient — the sign and rough magnitude of the MPC asymmetry between asset-incidence and uniform-incidence dollars — in partial equilibrium, under a buffer-stock model whose simulated wealth distribution is strongly unequal. The creditor-range number (≈0.11) survives; the borrower-range number survives only for the constrained minority.
Does not: say anything about interest rates, general equilibrium, the symmetry fee itself, its revenue, or welfare. No rates move, no GE feedback, no fee is modelled. The β spread is an approximation of cstwMPC's design, not cstwMPC's estimated distribution, so magnitudes (especially the extreme top tail, max aLvl 225 from the near-impatience-limit β=0.99 type) should be read as indicative, not as replication of Carroll–Slacalek–Tokuoka–White (2017).

## Limitations
1. β (β̄=0.96, ±0.03 uniform) is chosen, not estimated to match US wealth moments; a true cstwMPC estimation (higher β̄, quarterly timing) would shift levels.
2. Annual HARK-default timing/parameters throughout; cstwMPC's original model is estimated on its own timing and income process.
3. Final-period cross-section of one simulation (seed 12345); no seed-sensitivity run.
4. Asset-pro-rata incidence gives zero to zero-asset households by construction — realistic for interest income, but it is an assumption of the contrast, not a result.
5. Shock size is 10% of mean permanent income per capita; exact ΔC uses the nonlinear cFunc, but larger shocks would compress the contrast (concavity).
