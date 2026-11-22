# OG-USA Run Notes — Monetary Symmetry Package as an Aggregate Fiscal Stance

**Label (required):** Steady-state comparison in OG-USA 0.6.2 / OG-Core 0.24.6 default calibration. The package enters as an aggregate fiscal stance (spending/transfers level + revenue mix); the symmetry fee and transaction tax are revenue equivalents only, the T-bill variant is excluded as unrepresentable, and no number here verifies any component revenue estimate.

## Environment & versions
- Python 3.12.3, venv at `./venv`, `num_workers=1` throughout.
- Sandbox: ~1.5 shared CPUs, ~7.9 GB RAM total (other tenants active; 0.8–2.0 GB available at various checks). Peak RSS of the SS driver process ≈ 1.03 GB (baseline) / 0.99 GB (reform).
- Installed: `ogcore==0.24.6`, `ogusa==0.6.2` (exactly the scout-verified versions), `taxcalc==6.8.5`, `numpy==2.5.5`, `pandas==3.1.1`, `scipy==1.18.1`, `numba==0.67.0`, `pytest==9.2.0` (validation only). Full list: `pip_freeze.txt`.
- Install note: first `pip install` failed with "No space left on device" because `/tmp` is a 512 MB tmpfs at 91% (other tenants' pip temp dirs). Fixed by setting `TMPDIR` and `PIP_CACHE_DIR` inside this work dir; second install succeeded cleanly (`install2.log`).

## Validation
- The shipped full example (`examples/run_ogcore_example.py`, baseline + reform, SS **and** TPI) is **not in the PyPI wheel or sdist** for 0.24.6 — it is repo-only, the docs themselves say a full example run takes **>2 hours** on real hardware, and a `git clone` of OG-Core timed out at 300 s in this sandbox. It was therefore **not run**, and no expected-output CSV diff was possible. This is a documented limitation, not a silent skip.
- Substitute validation actually performed: OG-Core's own shipped unit tests that carry hard-coded expected values and do not depend on the sdist-excluded `tests/test_io_data/` files — `tests/test_aggregates.py`, `tests/test_tax.py`, `tests/test_firm.py`: **151 passed in 233.6 s** (`validation_tests.log`). (Several other test files cannot even be collected from the sdist because `test_io_data/` and `testing_params.json` are excluded from the sdist — a packaging fact, recorded here.)
- Strongest functional validation: the OG-USA default-calibration steady state below converged with max Euler errors ≈ 8×10⁻¹³ and resource-constraint error ≈ 6×10⁻¹⁷ (baseline) / 0.0 (reform).

## Method
- `Specifications(baseline=…, num_workers=1)` → `update_specifications(ogusa_default_parameters.json)` (shipped defaults: S=80, J=10, T=320, start_year 2026) → `ogusa.calibrate.Calibration(p)` with **no estimation** (only shipped η/ζ/e updates applied) → `ogcore.execute.runner(p, time_path=False)` = **steady state only**. No CPS re-estimation, no PUF, no tax-function re-estimation, no taxcalc reform (§201 is inside Title II's $6.11T and is another lane's job).
- Script: `run_ss.py`. Logs: `baseline_ss.log`, `reform_ss.log` (iteration 1: `reform1_ss.log`, `OUTPUT_REFORM1/`).

## Baseline steady state (default calibration)
Wall time **346.5 s** (cold; includes numba JIT). Peak RSS ≈ 1,026 MB.

| Aggregate | Value |
|---|---|
| Y | 0.39459 |
| K | 1.30612 |
| L | 0.18947 |
| C | 0.29022 (73.55% of GDP) |
| w | 1.29122 |
| r (net) | 0.06137 |
| r_p (portfolio) | 0.04264 |
| Total tax revenue / GDP | 16.63% (business 1.14%, income+payroll 14.76%, consumption 0.74%) |
| Transfers TR / GDP | 10.02% (= α_T[−1] = 0.10017, by construction) |
| G / GDP | **−0.26%** (see closure note below) |
| (G + TR) / GDP | 9.76% |
| Pensions / GDP | 8.50% |
| Debt D / GDP | 1.900 (fixed by `debt_ratio_ss`) |

**Closure note (important):** under OG-USA's default fiscal rule (`budget_balance=False`, `baseline_spending=False`), SS transfers are exogenous (TR = α_T[−1]·Y) and **G is the budget residual** at the fixed SS debt ratio; α_G (SS value 0.0498) does **not** set SS G. The baseline residual G ≈ −0.26% of GDP is an artifact of that closure (revenues − pensions − transfers − debt service + new borrowing ≈ 0), not a claim that US government consumption is zero. Consequently the reform drives the spending side through α_T and lets residual G absorb the remainder — exactly the model's own semantics, per the task instruction to follow them.

## Mapping table — package → OG-USA parameters

| Package component | OG parameter | Size | Justification | What is lost |
|---|---|---|---|---|
| MFA net new federal flows (gross new federal health flows ≈ residual $2.52T + Title II $6.11T ≈ $8.6T/9yr ≈ 3% of GDP/yr, most of it transfers-like) | `alpha_T` (all years) | **+0.024** (SS: 0.10017 → 0.12417; TR/GDP +2.40pp) | Transfers are the model's transfers-like spending channel; central stance ≈ +2.8% of GDP combined, of which residual G supplies the rest (below) | MFA is health-specific purchasing/transfers to a sector; the model has no health sector, no insurance value, no provider prices. All of that is lost — only the aggregate transfer level survives |
| Same, residual spending share | `alpha_G` — **not used as an SS lever**; SS G is the budget residual | Residual G/GDP −0.26% → +0.01% (**+0.26pp**) | Model's own closure (see note above); combined (G+TR)/GDP rises **+2.66pp**, inside the instructed +2.5 to +3.0 band | Cannot independently set G and TR in SS under the default rule; the G/TR split of the stance is the model's, not the package's |
| Symmetry fee on loans+bonds (~$2.7T/window ≈ 1.0% GDP/yr, project model) + FTT 0.10% (~$1.2–1.4T ≈ 0.45% GDP/yr) + corporate share of Title II | `cit_rate` (drives `tau_b` = cit_rate × c-corp share × CIT adjustment factor) | **0.21 → 0.44**; business tax revenue/GDP 1.14% → 2.40% (**+1.26pp**) | **Revenue equivalent only.** A doubled effective business-tax take is the model's only native capital-side revenue lever of the needed size | Everything structural: the fee is on loan/bond *stocks* intermediated by banks, the FTT on *transaction volumes*; the model has **no banks, no IORB, no maturity structure, no transaction volumes**. Incidence, avoidance, volume elasticity, and the fee's interest-income channel are all absent. The 0.44 rate is a calibrated revenue stand-in, **not** a proposed corporate rate |
| MFA payroll add-on (real Title II item) + individual Title II provisions (incl. §201 TCJA repeal, which is inside Title II's $6.11T) folded in | `tau_payroll` | **0.000 → 0.027**; income+payroll revenue/GDP 14.76% → 16.26% (**+1.51pp** combined) | MFA's payroll add-on is genuinely a payroll tax. A clean level shift of `etr_params` was judged **not** straightforward (they are estimated tax-function coefficients by period×age, (320,80,2) in the shipped JSON — scaling them is not a rate shift), so per instructions the individual share is folded into this lever and `cit_rate`, and the simplification is documented here | Distributional detail of Title II's individual provisions and of §201 entirely; payroll taxation is flat in this lever while Title II is not. (Internal accounting note: within the household side, the split between `iit_revenue` and `payroll_tax_revenue` shifted between runs; only the combined +1.51pp is interpretable) |
| **T-bill maturity variant** | — | **EXCLUDED entirely** | Its only entry would be imposing its interest saving as an assumed rate path — typing in the conclusion, not a mapping | — (exclusion is deliberate and total) |
| §201 TCJA repeal as a standalone reform | — | **Not built** | It is inside Title II's $6.11T; a separate Tax-Calculator lane scores it. No taxcalc reform, no tax-function recalibration in this lane | — |

**Budget-neutrality check (SS stance):** revenue/GDP +2.77pp vs (G+TR)/GDP +2.66pp → gap **+0.11pp of GDP**, within the ~0.3pp tolerance. Two SS iterations were run; iteration 1 (α_T +0.020, cit 0.42, payroll 0.024) gave revenue +2.49pp / (G+TR) +2.39pp / gap +0.10pp but (G+TR) below the +2.5 band, so iteration 2 (above) is the reported reform. SS debt/GDP is 1.900 in both runs **by construction** (`debt_ratio_ss`), so it cannot differ and verifies nothing about debt dynamics.

## Steady-state comparison (final reform)

| Aggregate | Baseline | Reform | % change |
|---|---|---|---|
| Y | 0.39459 | 0.38398 | **−2.69%** |
| K | 1.30612 | 1.23842 | **−5.18%** |
| L | 0.18947 | 0.18733 | **−1.13%** |
| C | 0.29022 | 0.28512 | **−1.76%** |
| w | 1.29122 | 1.27083 | **−1.58%** |
| r (net) | 0.06137 | 0.06038 | **−1.61%** |
| r_p | 0.04264 | 0.04171 | −2.18% |
| Revenue / GDP | 16.63% | 19.40% | +2.77pp |
| (G+TR) / GDP | 9.76% | 12.42% | +2.66pp |
| Debt / GDP | 1.900 | 1.900 | 0 (by construction) |

Reform SS wall time 89.7 s (warm JIT + baseline SS used as initial guess, the model's standard reform path); peak RSS ≈ 994 MB.

## Interpretation
What OG-USA says: financing roughly +2.7% of GDP of new transfers/spending with a capital-side-heavy revenue mix costs, in steady state, about **−5.2% capital, −2.7% output, −1.1% labor, −1.8% consumption, −1.6% wages**. Note the interest rate **falls** (−1.6%), contrary to the naive "less K → higher r" prior: the doubled business-tax wedge (τ_b) cuts the *net* return to capital by more than capital scarcity raises the gross return, and labor falls alongside capital. What this does **not** speak to: fee mechanics or its interest-income/interest-saving channel, any component revenue estimate (fee, FTT, Title II, §201), the T-bill variant, FTT behavioral/volume responses, health-sector effects of MFA, and the §IX demand channel — OG-USA is a supply-side, flexible-price model, so any demand-side offset in the combined plan is invisible here by construction. This is a stance cost estimate, not a package score.

## TPI probe (reduced, baseline only, strictly time-boxed ≤45 min)
Attempted (`run_tpi_probe.py`, `tpi_probe.log`): OG-USA defaults with T shortened 320 → 50, baseline only, 1 worker. Total probe wall ≈ 9.3 min (well inside the box; it failed fast rather than timing out).
- The probe's SS stage **converged** (iteration 1, distance 1.6×10⁻¹¹; SS.py also printed its own warning that SS government spending is negative to satisfy the budget — corroborating the closure note above).
- The TPI stage then **crashed on its first aggregate call** with `IndexError: index 130 is out of bounds for axis 0 with size 130` in `ogcore/aggregates.py::get_RM` (`rho_vec[t - p.tG1] * p.alpha_RM_T * Y[t]`): the shipped calibration's time-path fiscal arrays are built for T=320 (regime breakpoints tG1=20, tG2=256), so naively truncating T is dimensionally inconsistent with them.
- **Finding:** a reduced TPI is *not* obtainable by T-truncation alone in this sandbox; it would require the maintainers' reduced recalibration (re-derived time-path arrays / smaller J), and a full T=320 TPI at 1 worker was not attempted — the maintainers document >2 h for a baseline+reform TPI pair on multi-core hardware and ~23 min per TPI even at reduced J=7 on a maintainer's Mac, against ~6 min for one cold SS solve here. TPI viability for the full calibration in this sandbox: **not demonstrated; treat as not viable within mission time boxes.** (An earlier probe attempt also failed instantly due to a missing `__main__` guard in the probe script interacting with dask's spawn — a script bug, fixed; the result above is from the fixed script.)

## Limitations
- Steady state only (plus the probe below); no transition path for the reform, so no statement about the FY28–36 window path, phase-ins, or welfare by cohort.
- SS debt/GDP is a calibration constant (1.9), not an outcome.
- SS G is a budget residual (≈0 in baseline); the G/TR split is model-determined.
- Revenue equivalents are calibrated to hit aggregate revenue/GDP targets; their parameter values (cit 0.44, payroll 0.027) are not policy proposals and must not be quoted as such.
- Full OG-Core example not run (repo-only, >2 h documented, clone timed out) — validation rests on the 151 shipped unit tests + clean SS convergence diagnostics above.
