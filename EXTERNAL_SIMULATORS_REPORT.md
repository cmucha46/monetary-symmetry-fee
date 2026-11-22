# External Simulators Mission — Report

**Date:** 2026-11-22 · **Sponsor:** Carlos · **Prepared by:** Gus fleet (6 scout workers, 5 run lanes, coordinator synthesis)
**Scope:** Find other open-source economic simulators on GitHub, verify them against their actual repositories, run the Monetary Symmetry + Medicare for America package (or its honestly representable components) through the suitable ones, and reconcile the results against the project's existing numbers.
**Companion artifacts:** `external_sims/` in this repository (scripts, reform files, results, per-lane RUN_NOTES.md, pip freezes).

**Labels discipline (applies throughout):** a *static* microsimulation number, a *conventional* (elasticity-adjusted) number, a *steady-state general-equilibrium* number, and a *linearized impulse-response* number are four different objects. They are reported side by side and reconciled; they are never blended or averaged.

---

## 1. Executive summary

1. **The mission's highest-value check succeeded.** The combined study's largest unverified input — Medicare for America §201's whole-law repeal of the TCJA, carried at **$3.9T** (central, FY28–36) as an extension-analogue *assumption* — was scored independently in Tax-Calculator and bounded from published JCT/CBO figures. **Implied full §201 range: ≈ $3.3–4.4T, midpoint ≈ $3.85T.** The $3.9T assumption sits inside the range, near its midpoint. It survives as a central assumption — corroborated in range, not confirmed as a score. A behavior-adjusted band (taxable-income elasticity on the individual side) runs lower: ≈ $2.7–3.7T.
2. **The §IX channel's sign is corroborated twice externally; its magnitudes are not.** In a general-equilibrium HANK (sequence-jacobian), an interest-incidence charge is contractionary and the same charge recycled as flat transfers is mildly expansionary — the project's ordering survives wages, inflation, and a Taylor rule. But the project's "recycling dominates redistribution by an order of magnitude" does **not** replicate on cumulative consumption (the two terms are ≈ equal, ratio 1.02), and in HARK the borrower-side MPC range (0.50–1.00) holds only for the ~2% of households at the borrowing constraint, not as a group average (poorest-quintile mean MPC 0.393). The creditor range (0.05–0.20) **is** corroborated by both checks (asset-weighted MPC 0.112 in HARK; aggregate MPC 0.118 in the HANK steady state).
3. **OG-USA prices the package's fiscal stance, and the price is real.** A steady-state comparison (the only OG mode this sandbox can honestly run) of a budget-neutral stance — transfers/spending +2.66pp of GDP financed by +2.77pp of GDP revenue through a capital/payroll-heavy mix — yields steady-state output **−2.69%**, capital **−5.18%**, consumption **−1.76%**. This is a neoclassical long-run supply cost of raising the revenue with conventional distortionary instruments; it answers a different question from the project's demand-side FRB/US runs, and §5.3 explains the disagreement rather than averaging it.
4. **The package's three most novel numbers have no external witness — and that is a finding.** The symmetry fee's revenue, the T-bill variant's interest savings, and the transaction tax's revenue cannot be represented in *any* verified open-source simulator: the models lack banks/credit classes, Treasury maturity structure, and trading volume respectively, and CBO publishes no scoring engine for any of them (§2.6). Those numbers remain single-source.
5. **The corporate side of the TCJA repeal is the dominant residual uncertainty** ($0.5–1.5T of the §201 range), and the mission's discovery lane found the right instrument for its *behavioral* channel: PSLmodels' Cost-of-Capital-Calculator shows repealing TCJA's business provisions raises the overall marginal effective tax rate from 6.95% to 15.01% and the user cost of capital by ~5% — implying the business-side revenue is more likely over-stated than under-stated once investment responds. No open-source scorer for corporate *revenue* exists (Business-Taxation is dormant, PUF-gated, and carries its author's "not for publications" warning).

---

## 2. Simulators found and verified

All facts below were verified against the live repositories on 2026-11-22 (releases, LICENSE files, docs, parameter sets) — not from catalog memory.

### 2.1 PSLmodels/OG-Core + OG-USA — verified, maintained, RUN (steady state)

| Fact | Value |
|---|---|
| Canonical home | github.com/PSLmodels/OG-Core (engine) + /OG-USA (US calibration). The rumored move to "OpenSourceEconomics" is false — that GitHub org is the unrelated Bonn group; OG lives at PSLmodels. |
| Versions | ogcore **0.24.6** (PyPI 2026-11-16), ogusa **0.6.2** (2026-10-13); weekly-to-monthly release cadence; OG-USA defaults updated to the August 2025 CBO baseline |
| License | **CC0-1.0** (both) |
| Install | `pip install ogcore ogusa`; Python ≥3.12 (ogusa <3.14) — sandbox Python 3.12.3 qualifies |
| Data | Default calibration ships complete (S=80 ages, J=10 income groups, T=320, start_year 2026); CPS microdata public; IRS PUF restricted and not needed for a shipped-calibration run |
| Cost reality | Maintainers warn a full baseline+reform transition-path pair takes **>2 hours on multi-core hardware** (~23 min per TPI at reduced J=7 on a maintainer's machine). Sandbox: ~1.5 shared CPUs → full TPI is a many-hours-to->1-day job. Steady state: minutes. |

### 2.2 PSLmodels/Tax-Calculator (+ Behavioral-Responses) — verified, maintained, RUN

| Fact | Value |
|---|---|
| Canonical home | github.com/PSLmodels/Tax-Calculator; docs taxcalc.pslmodels.org |
| Versions | Upstream **6.9.1** (2026-11-11), but 6.9.x dropped Python 3.12; the sandbox index tops out at **6.8.5**, which is what ran (Python 3.12.3). 6.8.x already contains the behavioral-response functions. |
| License | **CC0-1.0** |
| Data | **CPS (`cps.csv`) is the only fully public file and ships with the package.** PUF and the newer TMD file are IRS-restricted. CPS is weighted to SOI targets but under-represents high-income filing units and lacks some PUF variables — every CPS number in this report carries that caveat. |
| Behavioral-Responses | Standalone repo frozen at 0.11.0 (2020-09-22); its functionality was **absorbed into taxcalc 6.8.1** (`taxcalc.behresp`, `response()`), which is what the run lane used. |
| **Pivotal scouting fact** | **The baseline moved.** OBBBA (signed July 4, 2025) made the TCJA permanent; since taxcalc 5.2.0, OBBBA *is* current-law policy. There is no "TCJA expires" baseline left to flip. A §201 score in 2028+ is an **active reform**: revert parameters to pre-TCJA 2017 law against an OBBBA baseline, and undo OBBBA's own additions in the same universe. The project's $3.9T was framed in the older extension/expiration world; §4.1 shows the analogue nevertheless lands centrally, and why. |

### 2.3 shade-econ/sequence-jacobian — verified, dormant-stable, RUN

v1.0.0 (PyPI Jan 2022), **MIT**, last commit 2024-09-09 — mature, effectively dormant, not archived. Deps are numpy/scipy/numba only (no JAX). Ships one-asset and two-asset HANK notebooks; the one-asset model's fiscal block is literally `Tax = r·B` — the §IX financing identity in miniature — which made a faithful adaptation possible (§4.4).

### 2.4 econ-ark/HARK — verified, maintained, RUN

0.17.2 (2026-05-01), **Apache-2.0**, `pip install econ-ark`, requires Python ≥3.12. Actively developed. Ships the buffer-stock machinery (IndShock) and the cstwMPC research design (β-distribution calibrated to wealth inequality) that the §IX ingredient check needs (§4.5).

### 2.5 PSLmodels/Cost-of-Capital-Calculator — discovery addition, verified, maintained, RUN

Found by the discovery sweep; not on the mission's original list. **2.1.1**, **CC0-1.0**, updated Apr 2026, `pip install cost-of-capital-calculator`. Computes marginal effective tax rates and the cost of capital by asset/industry/entity/financing from a year-indexed parameter file (2013–2035) — which makes a pre-TCJA (2017) vs current-law (2026) comparison constructible from shipped parameters alone (§4.2). It produces **no revenue numbers**, and none are attributed to it.

**Examined and rejected — PSLmodels/Business-Taxation:** exists ("USA Corporate and Pass-Through Business Tax Model", 2017), but dormant since ~2019, in a self-declared "major refactoring", requires the restricted IRS PUF, and its README states the code "should not be used for publications, journal articles or research purposes." Recorded here so the mission does not treat a corporate-revenue scorer as existing: on this sweep, **none does**.

### 2.6 US-CBO GitHub — full census, nothing scoreable for this package

The org (github.com/US-CBO) has **36 repositories**; the scout fetched and read every one on 2026-11-22. All carry "Other (NOASSERTION)" licenses. The census, in one paragraph: ~26 narrow runnable models (CapTax — capital-tax EMTRs; a conventional tariff model, CTAM; a permitting/investment model; an EV demand model; a hepatitis-C microsim; a Medicaid *labor-supply* module; a one-fee-schedule Medicare Excel workbook; credit-subsidy and trust-fund workbooks; macro-uncertainty simulations), plus replication packages, data pipelines that run only inside CBO/CMS enclaves, and the `cbo-data` open-data repository. Several are expressly non-scoring ("not a cost estimate", "should not be used for policy simulations"). **CBO publishes no general tax microsimulation, no health-program spending model (HISIM2 is not published anywhere), and no debt-service model.** The only pieces even peripheral to this package: CapTax (duplicates CCC's channel, narrower), CTAM (a template for conventional no-feedback transaction-type revenue — for customs tariffs), and the budgetary-feedback / rules-of-thumb models, which translate *already-estimated* changes into budget sensitivities against CBO's Feb 2026 baseline. **No CBO run lane was dispatched: there is nothing applicable to run.** The project's numbers cannot be checked against CBO's actual models because CBO's actual models are not public — the published scores and decompositions used in §4.1's bound are the only CBO/JCT evidence available to anyone outside the building.

### 2.7 Dynare — verified, feasible, NOT run (deliberately)

Dynare **7.2** (2026-09-11), GPL-3.0-or-later. Its home is its own GitLab (git.dynare.org); the GitHub `DynareTeam/dynare` mirror is dead (404 — "this project has moved"). In this sandbox the route is `apt install dynare octave` (expect Dynare 6.x; Octave carries a documented performance loss vs MATLAB, immaterial at textbook scale). A textbook New Keynesian model with a credit wedge and alternative revenue-recycling rules would run in seconds and could check the *direction* of the fee/recycling story. It was not run: the mission's run priorities were the scorers and the §IX checks, and a representative-agent toy model's ceiling is a labeled consistency illustration that could not move any number in the package. Recorded as scouted-feasible, available if the sponsor wants it.

### 2.8 Also verified in passing

- **QuantEcon** — confirmed a methods library (numerical plumbing), not a fiscal model.
- **PyFRB/US** — the Fed's public model the project already uses; its modern wrappers are the same model, not a second witness. No other credible public Fed simulator surfaced.

### 2.9 Representability matrix (verified, component × simulator)

| Package component | Tax-Calculator | OG-USA | sequence-jacobian | HARK | CCC | CBO GitHub |
|---|---|---|---|---|---|---|
| §201 TCJA repeal (individual side) | **Direct — scored** | Via taxcalc reform → tax functions (not used; see §6) | No | No | No | No |
| §201 TCJA repeal (corporate/estate side) | **No** (no corporate or estate module) | Partial, aggregate only | No | No | **Incentive channel only (METR/UCC)** | No |
| MFA Title II other items | Partial (see §5.5 audit) | Aggregate parameters | Reduced form (transfers) only | No | No | No |
| MFA spending | No | Aggregates (α_G, α_T, η) | Transfers sequence only | Household response only | No | No (HISIM2 unpublished) |
| Symmetry fee | No | **Revenue-equivalent only** (τ_b) | No (demand consequence only, assuming incidence) | No | No | No |
| T-bill maturity variant | No | **No** (single one-period debt instrument; only "mapping" is imposing the saving) | No | No | No | No |
| Transaction tax | No | Revenue-equivalent wedge only (not used) | No | No | No | No (CTAM is tariffs) |
| §IX MPC/recycling channel | No | Translated neoclassical cousin only | **Yes — adapted HANK experiment** | **Yes — PE ingredient check** | No | No |

---

## 3. Selection decisions

**Ran (5 lanes):** Tax-Calculator (§201 individual side — the mission's priority 1); Cost-of-Capital-Calculator (§201 business-investment channel); OG-USA (package fiscal stance, steady state — priority 2, at the scope the sandbox honestly supports); sequence-jacobian (§IX in general equilibrium); HARK (§IX's MPC ingredient in partial equilibrium).

**Not run, with reasons recorded in §6:** OG-USA transition path; Dynare; any CBO repository; Business-Taxation; two-asset HANK; the HAFiscal REMARK.

**Excluded from simulators that cannot represent them (per mission rule):** the T-bill variant was excluded everywhere — no verified model has a Treasury maturity structure, and the only available "mapping" (imposing a lower government rate path in OG-USA) would type the conclusion in as an assumption. The symmetry fee and the transaction tax entered OG-USA only as labeled revenue equivalents, and nowhere else.

---

## 4. Runs

### 4.1 Tax-Calculator — the §201 TCJA-repeal score (priority 1)

**Setup.** taxcalc **6.8.5**, Python 3.12.3, CPS public data only (`Records.cps_constructor()`); PUF/TMD not attempted (restricted). Baseline = OBBBA current law. Artifacts: `external_sims/taxcalc/` (reform file, scripts, results CSV/JSON, RUN_NOTES.md with the full parameter mapping table).

**Reform construction (`repeal201_from2028.json`, 92 parameters, all effective tax year 2028).** The shipped `2017_law.json` (83 parameters) was inspected rather than blindly reused (upstream issue #2610 warns it goes stale against a moving baseline): it was implemented in a Policy, its **2028 values extracted** — 2017 nominal values indexed forward by taxcalc's own CPI-U mechanism — and set against the OBBBA baseline, plus explicit OBBBA-undo patches (tip/overtime/senior/auto-loan deductions zeroed; OBBBA charity provisions zeroed; SALT phase-down rate zeroed). One forced fix, documented: OBBBA's `ID_reduction_rate` had to be zeroed because the engine asserts Pease limitation and OBBBA cannot both be in effect — substantively correct for a pre-TCJA revert. Coverage: individual rates 10–39.6% and brackets with pass-through mirrors; §199A repealed (`PT_qbid_rt` = 0); standard deduction $9,246/$18,493 (2028 dollars); personal exemption restored at $5,897; AMT reverted; SALT cap removed; Pease restored; CTC/ACTC back to $1,000 non-indexed; ODC zeroed; excess-business-loss limit repealed; EITC reset.

**Not revertible via parameters (documented, bounded in §4.1.3 instead):** estate tax (no module in taxcalc), corporate §11 rate, §174, §163(j), corporate expensing, international provisions (GILTI/FDII/BEAT), mortgage-cap and alimony vintage grandfathering, the individual mandate.

#### 4.1.1 Static result — individual side

| Tax year | 2028 | 2029 | 2030 | 2031 | 2032 | 2033 | 2034 | 2035 | 2036 | **2028–36** |
|---|---|---|---|---|---|---|---|---|---|---|
| Revenue raised ($B) | 310 | 298 | 275 | 281 | 286 | 292 | 297 | 302 | 307 | **2,647** |

(Reform − baseline aggregate individual income tax, CPS-weighted.) The 2030 dip is mechanical, not economic: in the baseline, OBBBA's SALT cap falls back to $10k in 2030 and the tip/senior deductions expire after 2028, so the baseline itself raises more revenue those years and the repeal's increment shrinks.

#### 4.1.2 Behavioral variant (reported separately, never blended)

With taxcalc's absorbed Behavioral-Responses at an assumed taxable-income substitution elasticity of 0.25 (the Recipe-2 convention): **$2,027B** — a ~23% erosion of the static figure. Label: *conventional, assumed elasticity 0.25*. JCT/CBO conventional scores embed micro-responses of this family, so this variant is arguably the more official-comparable of the two; the elasticity is an assumption, disclosed as such.

#### 4.1.3 The remainder — bounded from published figures (not model output)

Verified live during the run: **CBO, *Budgetary Outcomes Under Alternative Assumptions* (May 2024, pub. 60114, Table 2)** — for FY2025–34, extending the expiring provisions would cost: individual **$3,256B**, estate **$167B**, investment provisions $378B, business-maintained $172B. **CRS R48286** (2025-01-17) confirms the $3.3T / $167B / $551B decomposition and cites ~$249B/10yr for §174 + §163(j) restoration. **JCT JCX-67-17** (the original TCJA score) carries the crucial nuance for the permanent corporate side: the §11 rate cut alone was −$1,349B gross (FY18–27), **but the international provisions were a +$324B revenue raiser**, so total corporate provisions netted to only ≈ −$398B. Repealing "the entire TCJA" therefore does *not* yield the gross rate figure — repeal also repeals the raisers.

Bound for tax years 2028–36, scaled and labeled crude: estate **+$0.17–0.23T**; corporate + international net **+$0.5–1.5T**; **total remainder ≈ $0.7–1.7T**. Explicit caveat: §201's universe (the entire TCJA including permanent provisions, from 2028) is larger than the "expiring provisions" universe those tables describe; the corporate scaling is the dominant uncertainty in the whole §201 stack.

#### 4.1.4 Implied full §201

| Basis | Individual (model) | Remainder (bound) | **Full §201** |
|---|---|---|---|
| Static | $2.65T | $0.7–1.7T | **≈ $3.3–4.4T, midpoint ≈ $3.85T** |
| With behavioral variant | $2.03T | $0.7–1.7T | ≈ $2.7–3.7T |

**Honest label (carried in the lane's RUN_NOTES):** "Static microsimulation estimate, Tax-Calculator 6.8.5, CPS public-use data (cps.csv), author's calculations. Individual income and pass-through provisions only; excludes estate, corporate, and international provisions of TCJA. CPS data under-represent high-income filing units; an independent model estimate, not a JCT or CBO score."

### 4.2 Cost-of-Capital-Calculator — the business-investment channel of the repeal

**Setup.** CCC **2.1.1**, Python 3.12.3 (pandas pinned to 2.3.3 — the resolver's pandas 3.1.1 turns CCC's own warnings-as-errors into a hard failure on repeated calls; headline values identical under both where both ran). The comparison is constructible from CCC's shipped year-indexed parameter file with **no hand edits in the primary run**: evaluate at **2017** (pre-TCJA: CIT 35%, bonus depreciation 50% for 3–20-year classes) vs **2026** (current law: CIT 21%, bonus restored to 100% in 2025 by OBBBA). Artifacts: `external_sims/ccc/`.

**Not constructible in CCC (zero by construction, documented):** §163(j) (CCC's interest haircut is 0.0 in all years — its own note assumes the 30%-of-ATI limit non-binding for marginal investment) and §174 (the depreciation-rules file is static; R&D is expensed in both arms — in any case ≈ neutral against an OBBBA baseline, OBBBA having restored domestic R&D expensing).

**Results (pre-TCJA minus current law, mixed financing):**

| Measure | Current law | Pre-TCJA law | Δ |
|---|---|---|---|
| Overall METR | 6.95% | 15.01% | **+8.06 pp** |
| — corporate METR | 3.73% | 14.50% | +10.77 pp |
| — pass-through METR | 25.01% | 29.28% | +4.27 pp |
| Overall user cost of capital | 10.44% | 11.00% | **+0.56 pp (+5.3% relative)** |
| — corporate UCC | — | — | +0.72 pp |
| — pass-through UCC | — | — | +0.37 pp |

By asset (corporate METR Δ): equipment +11.28 pp, structures +9.97 pp, intellectual property +3.86 pp. One offsetting channel: **debt-financed** corporate METR *falls* 5.99 pp under pre-TCJA law (interest deductibility is worth more at a 35% rate, and §163(j) is non-binding in CCC) — the METR increase is equity-financed-driven. Cross-checks bound the headline: a law-only transplant sensitivity (2017 statutory values written into a 2026 specification, 2026 economics held constant, every edit in `transplant_revision.json`) gives METR +6.62 pp / UCC +4.3% relative; a year-native by-asset path gives corporate METR +9.27 pp with identical UCC. Disclosed quirk: CCC's `summary_table` recomputes reform METR using baseline saver-return parameters; the user cost is unaffected.

**Interpretation (the lane's, labeled as not CCC output):** a +4.3% to +5.3% relative rise in the user cost of capital, run through the standard literature user-cost elasticity range (−0.5 to −1.0), implies a long-run capital stock / investment level roughly **2–5% smaller**, concentrated in equity-financed corporate investment — which shrinks the business tax base relative to any static estimate. Direction of bias for §5.1: on the business side, a static repeal figure is more likely **over-stated** than under-stated once behavior responds.

### 4.3 OG-USA — the package as an aggregate fiscal stance (steady state)

**Setup.** ogcore **0.24.6** / ogusa **0.6.2** / taxcalc 6.8.5, Python 3.12.3, `num_workers=1`. Default calibration (S=80, J=10, start_year 2026), shipped tax functions, **no recalibration**. Validation: the shipped full example is not in the wheel (repo-only; documented at >2 h; a git clone timed out), so the lane substituted OG-Core's own unit tests with hard-coded expected values — **151 passed** — plus clean steady-state convergence (max Euler error ≈ 8×10⁻¹³, resource constraint ≈ 0). Baseline steady state: **346.5 s**, peak RSS ≈ 1.03 GB. Artifacts: `external_sims/ogusa/`.

**A closure finding that shaped the run:** under OG-USA's default fiscal rule, steady-state G is a *budget residual* at fixed debt-to-GDP (α_G does not set steady-state G; the solver itself warns when G < 0 — baseline G/GDP prints at −0.26%). The stance was therefore driven through transfers (α_T) and revenue, per the model's own semantics.

**Mapping table (package → OG-USA):**

| Package component | OG-USA entry | Size | Status / what is lost |
|---|---|---|---|
| MFA net new spending | α_T (transfers), all years | +0.024 (SS transfers 10.02% → 12.42% of GDP) | Aggregate stance only — no health sector, no insurance, no provider prices exist in the model |
| Fee + FTT + Title II corporate share (revenue) | `cit_rate` (business tax rate) | 0.21 → 0.44; business revenue/GDP 1.14% → 2.40% (+1.26 pp) | **Revenue-equivalent only.** A conventional corporate rate is a cruder, more distortionary instrument than an IORB-linked levy; incidence, credit-supply, and securitization mechanics are all lost |
| MFA payroll add-on (a real Title II item) | `tau_payroll` | 0 → 0.027 (+1.51 pp of GDP in income+payroll revenue) | Direct parameter, correct family |
| Title II individual provisions incl. §201 | — | folded into the two levers above | ETR/MTR-function rescaling judged not straightforward in the Specification; documented simplification (a taxcalc-driven recalibration is the proper route — §6) |
| T-bill variant | — | **excluded** | No maturity structure exists; the only entry would impose the claimed saving as an assumption |
| Symmetry fee *mechanics* (IORB link, Fed collection, pass-through) | — | **excluded** | No banks, no central bank, no IORB in the model |

Resulting stance: revenue/GDP **+2.77 pp** vs (G+transfers)/GDP **+2.66 pp** — gap +0.11 pp, inside the pre-set tolerance and the +2.5–3.0% of GDP band (the combined study's scale: MFA residual $2.52T + Title II $6.11T ≈ $8.6T over 9 years ≈ 3% of GDP/yr of new federal flows).

**Steady-state comparison:**

| Aggregate | Baseline SS | Reform SS | Δ |
|---|---|---|---|
| Output Y | 0.3946 | 0.3840 | **−2.69%** |
| Capital K | 1.3061 | 1.2384 | **−5.18%** |
| Labor L | 0.1895 | 0.1873 | −1.13% |
| Consumption C | 0.2902 | 0.2851 | −1.76% |
| Wage w | 1.2912 | 1.2708 | −1.58% |
| Interest rate r | 0.0614 | 0.0604 | −1.61% |
| Revenue / GDP | 16.63% | 19.40% | +2.77 pp |
| Debt / GDP | 1.900 | 1.900 | 0 (by construction) |

Two results deserve plain statement. First, the cost is concentrated in capital: a financing mix that leans on the business/capital side taxes the capital stock, and steady-state output follows it down. Second, **r falls** (−1.61%) — the business-tax wedge on the after-tax return dominates the capital-scarcity effect in this calibration. Reported as the model produced it; §5.3 puts it next to the project's own rate results and explains why they differ.

**TPI probe — documented stopping point.** A reduced transition-path probe (T truncated 320 → 50, baseline only) ran ~9.3 minutes: the steady-state stage converged, then TPI crashed immediately with an `IndexError` in `aggregates.get_RM` — the shipped time-path arrays are built for T=320 (fiscal-rule arrays sized tG2=256), so **a reduced TPI is not obtainable by truncation**, and a full TPI is not viable in this sandbox within any reasonable time box (maintainers: >2 h for the pair on multi-core hardware; this box has ~1.5 shared CPUs). Finding recorded: OG-USA transition dynamics for this package require a genuinely multi-core machine.

**Lane label (verbatim):** "Steady-state comparison in OG-USA 0.6.2 default calibration. The package enters as an aggregate fiscal stance (spending/transfers level + revenue mix); the symmetry fee and transaction tax are revenue equivalents only, the T-bill variant is excluded as unrepresentable, and no number here verifies any component revenue estimate."

### 4.4 sequence-jacobian — §IX in general equilibrium

**Setup.** sequence-jacobian **1.0.0** with numpy 2.5.5 / scipy 1.18.1 / numba 0.68.1 on Python 3.12.3 — no pins needed (one real gotcha, recorded: SSJ regex-parses literal `return` lines for output names, so the notebook's named-assignment style is required). The shipped one-asset HANK was reproduced at its **full shipped grid** (nA=500, T=300); the whole script runs in ~50 s. Artifacts: `external_sims/seqjac/`.

**Steady state / MPC structure.** Calibrated β = 0.982244, vphi = 0.786433; C = Y = 1, A = B = 5.6, r = 0.005, Tax = r·B = 0.028. **Aggregate MPC ≈ 0.118; hand-to-mouth share ≈ 17.4%.** MPC by population asset quintile falls steeply — **0.479 / 0.052 / 0.026 / 0.018 / 0.014** — while the top quintile's wealth share reaches 67.4%. The gradient the §IX mechanism needs is present in the model's own calibration.

**Experiment (an adaptation of the shipped notebook — not a shipped experiment — constructed and documented by the lane).** A common gross flow X_t = 0.01·0.8^t (present value 0.049024, ≈ 4.9% of one year's output) is imposed three ways, each net-zero unless stated:
- **Run A — interest incidence (the shipped structure):** an `rstar` path scaled ex post (exact under linearization) so the realized PV of interest dr_t·B equals the common PV. Taxes ∝ skill; interest ∝ assets. 
- **Run B — flat transfers, tax-financed:** two added exogenous sequences, GTAX = X_t (same ∝-skill tax rule) and GTR = X_t paid flat per household. **B − A is the pure redistribution contrast.**
- **Run C — flat transfers, unfinanced (auxiliary):** GTR alone. **C − B is the recycling term.** Validation: cumulative ΔY − ΔC ≈ 0 in A and B (goods market clears); in C it equals −PV by construction (an outside-sector injection), and C's negative ΔY is the endogenous-labor income effect.

| Run | Peak ΔC | Cumulative ΔC (Σ, 300 qtrs) | Cumulative ΔY |
|---|---|---|---|
| A — interest (∝ assets) | −0.00413 (trough) | **−0.01546** | −0.01545 |
| B — flat transfer, tax-financed | +0.00034 | **+0.00141** | +0.00141 |
| C — flat transfer, unfinanced | +0.00321 | **+0.01867** | −0.03132 |

**Verdicts.**
- **The §IX ordering survives general equilibrium.** A is contractionary, B is (mildly) expansionary, B > A on both consumption and output — with endogenous wages, inflation, and the Taylor rule active. 
- **"Recycling ≫ redistribution" does not survive on the cumulative-consumption metric.** Redistribution (B − A) = **+0.01687**; recycling (C − B) = **+0.01726**; ratio **1.02** — essentially equal, not an order of magnitude. The ≫ impression survives only in peak/level framing (C's cumulative ΔC is 13.2× B's; tax financing destroys ~92% of the transfer's consumption effect). On cumulative *output*, the recycling increment is **negative** (−0.0327), because unfinanced transfers reduce labor supply in this model.
- **Caveat (in the lane's notes):** Run A bundles the pure incidence effect with the real-rate/Taylor tightening inherent in paying interest through a higher r (peak Δr 56 bp in A vs 4 bp in B), so A's contraction is an **upper bound** on the pure incidence effect; the framework offers no asset-indexed transfer channel other than r (the `transfers` hetinput is skill-indexed only).

**Lane label (verbatim):** "Linearized (first-order) MIT-shock comparison in a textbook one-asset HANK (Y=1, lump-sum ∝-skill taxes, fixed debt stock, no banks/IORB/credit sector). A sign-and-mechanism check of the §IX ordering, not a score of any policy magnitude."

### 4.5 HARK — §IX's MPC ingredient in partial equilibrium

**Setup.** econ-ark **0.17.2**, Python 3.12.3 (install needed two attempts — a truncated statsmodels wheel; retry succeeded). 14,000 simulated agents (2,000 × 7 types), 300 periods. Artifacts: `external_sims/hark/`.

**Calibration provenance — stated without varnish:** **no parameter is cstwMPC's estimated value.** The β side is a documented *approximation* of the cstwMPC design — 7 equal-share types, β ∈ [0.93, 0.99], centered on HARK's default 0.96 with spread ±0.03 (cstwMPC's estimated (β̄, ∇) are not in the HARK 0.17.2 package and were not ported within the time box). Everything else is HARK's `init_idiosyncratic_shocks` default (Sabelhaus–Song-style income process; PermShkStd/TranShkStd 0.10/0.10, unemployment prob. 0.05, CRRA 2, Rfree 1.03, LivPrb 0.98, PermGroFac 1.01). Even un-estimated, the simulated distribution is strongly unequal: the top wealth quintile holds **70.4%** of assets.

**MPC by wealth quintile (mean MPC):**

| Q1 (poorest) | Q2 | Q3 | Q4 | Q5 (richest) |
|---|---|---|---|---|
| **0.393** | 0.248 | 0.199 | 0.157 | **0.100** (median 0.063) |

Population aggregate MPC (derivative) 0.219. Only **1.88%** of households sit at the borrowing constraint — and exactly that 1.88% have MPC > 0.9 (2.12% have MPC > 0.5).

**The incidence contrast** (same total shock — 10% of mean permanent income per capita — exact nonlinear ΔC from the solved consumption function):
- (a) **Pro-rata to assets** (interest-income-like): aggregate MPC **0.112**
- (b) **Uniform per capita** (recycled-transfer-like): aggregate MPC **0.200**
- Ratio **0.56** — asset-incidence dollars produce ~56% of the consumption response of uniform dollars.

**Verdicts on the project's assumed ranges.** Creditor MPC 0.05–0.20: **supported** — the asset-weighted figure (0.112) lands inside it, as does the top-quintile mean (0.100). Borrower MPC 0.50–1.00: **not supported as a group average** — no wealth quintile's mean reaches 0.50 (the poorest is 0.393); the range describes only the ~1.9% of households at the borrowing constraint. If §IX's "borrowers" means constrained/hand-to-mouth households specifically, the range is plausible; as an average for low-wealth households, this calibration says ~0.25–0.39. Model caveat: HARK's IndShock world has no imposed hand-to-mouth or indebted-household class — MPC ≈ 1 arises only at the constraint, endogenously and rarely, which is itself informative about how much of the population a 0.50–1.00 average would require.

**Scope (lane's words):** this disciplines only the MPC-asymmetry ingredient, in partial equilibrium — no interest rates, no general equilibrium, no fee is modeled.

---

## 5. Reconciliation against the project's numbers

Differences are explained, never averaged away. Each item names the project figure, the external figure, and the most likely reason(s) for the gap.

### 5.1 §201 TCJA repeal — project assumption $3.9T (central) vs external range $3.3–4.4T

**Verdict: the assumption survives as a central value.** The project's single largest unverified input now has an independent microsimulation underneath its dominant component and published bounds around the rest. It should be re-labeled in the project's documents from "extension-analogue assumption, not a score" to "corroborated in range by Tax-Calculator 6.8.5 (individual side) + CBO/JCT published bounds (remainder); not an official score" — with the range, not just the point, carried forward.

Why the external build does not simply read "$3.9T confirmed":
- **Baseline law changed underneath the assumption.** The $3.9T was constructed as an extension analogue in a world where TCJA was scheduled to expire. OBBBA made it permanent and added its own provisions (a $40k SALT schedule 2025–29, tip/overtime/senior deductions). The Tax-Calculator run is therefore a *repeal of permanent law against an OBBBA baseline*, including undoing OBBBA's additions in the TCJA universe — a different, in places larger, reform than "letting it expire." That the analogue still lands near the midpoint is partly good fortune: for the individual side, repealing permanent law ≈ −(extension cost) to first order.
- **The model piece is biased down; behavior pushes down too; they do not cancel by construction.** CPS under-represents high-income filing units, so the provisions whose revenue concentrates at the top (SALT-cap removal, §199A repeal, AMT) are under-measured — the true static individual figure is likely above $2.65T. In the other direction, the conventional variant (elasticity 0.25) erodes the individual side by ~23% (to $2.03T), and CCC's investment channel erodes the business side dynamically (§4.2). The honest carry-forward is the range with both bands visible: **static-anchored $3.3–4.4T; behavior-adjusted ≈ $2.7–3.7T.**
- **The remainder is the uncertainty.** Estate ($0.17–0.23T) is well-bounded. Corporate + international ($0.5–1.5T) is a crude scaling of published tables whose universe (expiring provisions, FY25–34) differs from §201's (entire TCJA incl. permanent provisions, 2028–36) — and JCX-67-17 shows the netting trap explicitly: the corporate title of TCJA netted to ≈ −$398B at enactment because the international provisions *raised* revenue. Any future refinement of the $3.9T should spend its effort here, not on the individual side.
- **Downstream consequence.** Title II's $6.11T central total inherits this verdict: its largest component is now range-corroborated, so the combined study's MFA residuals (low −$1.29T / central +$2.52T / high-stress +$10.73T) carry a §201-driven uncertainty of roughly ±$0.5T around the central case from this component alone. The combined study's qualitative verdicts (central financed at every τ_long on the consolidation basis; high-stress financed at none) are not overturned by a ±$0.5T movement in a $2.52T residual — but the thin τ_long = 0 central margin (+$179B) is thinner than this uncertainty, and the project's documents should say so.

### 5.2 The §IX channel — sign corroborated, magnitudes revised down

**Project claim (from its one-period SFC experiment):** at equal combined charge, receipts banked/interest-incidence is contractionary, transfers and government purchases flip the impulse expansionary *everywhere* on its grid, and the recycling term is an order of magnitude larger than the redistribution term; assumed MPCs: creditors 0.05–0.20, borrowers 0.50–1.00.

**External evidence:**
- **Sign/ordering: corroborated in GE.** sequence-jacobian's HANK, with wages, inflation, and a Taylor rule endogenous: interest incidence −0.0155 cumulative ΔC; flat-transfer recycling +0.0014. The flip is real and survives general equilibrium.
- **MPC asymmetry: corroborated in direction, smaller in size.** HARK: asset-incidence dollars deliver 0.56× the consumption response of uniform dollars (0.112 vs 0.200). The project's assumed endpoints imply a ratio nearer 0.1–0.4. The creditor endpoint is fine (0.112 in range; HANK aggregate MPC 0.118; HANK top-quintile MPCs 0.014–0.052, HARK top-quintile mean 0.100 — different MPC concepts, same neighborhood). The borrower endpoint is the problem: 0.50–1.00 is a *constrained-household* value (~2% of HARK's population; HANK's bottom asset quintile reaches 0.479), not a low-wealth average (~0.25–0.39 in HARK).
- **"Recycling ≫ redistribution": not corroborated as stated.** In the HANK decomposition the two terms are ≈ equal on cumulative consumption (ratio 1.02), and the recycling increment on cumulative *output* is negative. 

**Most likely reasons for the magnitude gap** (structural, not anyone's arithmetic error): the project's SFC experiment is a **one-period, first-round** accounting experiment — by construction it has (i) no labor-supply margin, so transfers cannot reduce earnings (the HANK's C-run shows exactly this cost: cum. ΔY −0.0313); (ii) no monetary-policy response, so the interest-incidence arm is not tightened by a Taylor rule (in the HANK, that tightening is bundled into Run A and makes A an *upper bound* on pure incidence — this cuts in the project's favor); (iii) government purchases entering demand at an effective MPC of 1 by construction, which mechanically inflates the "recycling" arm relative to any model where spending leaks into imports, prices, or labor responses; and (iv) endpoint MPCs imposed rather than generated (see above). **Net reconciliation:** §IX should be carried as a *sign-and-mechanism* result with a smaller, metric-dependent quantitative edge — incidence ratio ≈ 0.56 (HARK, partial equilibrium), redistribution ≈ recycling on cumulative consumption in GE — not as an order-of-magnitude dominance. The combined study's use of §IX (its spending closure more than offsets the fee's employment drag in FRB/US) rests on FRB/US's own demand dynamics, not on the SFC magnitudes, and is not directly disturbed; but any future appeal to "recycling is 10× redistribution" should be retired.

### 5.3 The package's macro stance — OG-USA's steady-state cost vs the project's FRB/US results

**The disagreement, stated plainly.** OG-USA's steady state says financing this stance with conventional distortionary taxes costs **−2.69% of output and −5.18% of capital in the long run**, with the interest rate *falling* 1.61%. The project's FRB/US combined run says the package's policy rate settles *higher* (rff = fee ≈ 3.70%, above baseline) and unemployment ends *lower* (−0.61 pp by 2036Q4) — a demand-side benefit. These are not two estimates of one quantity and must not be averaged:

- **Different questions.** OG-USA is a flexible-price, supply-determined steady state: there is no demand channel in it to flip, no unemployment, and no transition. It prices the *long-run supply cost of the financing mix*. FRB/US is a demand-driven transition model: it traces the *path* of a spending expansion and a rate rule. A package can honestly have both a positive transition demand impulse and a negative long-run supply cost; the models are reporting different halves of that sentence.
- **Different instruments.** OG-USA's financing leaned on `cit_rate` 0.21 → 0.44 — a textbook corporate income tax, among the most capital-distorting instruments available — as a *revenue equivalent* for a package whose actual centerpiece is an IORB-linked levy on credit (whose incidence the project models as falling substantially on creditor rents and bank spreads, not on the marginal return to new capital) plus a TCJA repeal whose own METR signature CCC measured at +8 pp (§4.2). OG's capital response is therefore best read as an **upper-bound-flavored cost of raising ≈2.8% of GDP with conventional taxes**, not as an estimate of the fee's effect. The mission could not do better inside OG-USA: the fee has no native representation there (§2.9), and pretending otherwise would violate the mission's own rule.
- **The rate signs differ for mechanical reasons.** In OG-USA, r is the after-tax return on capital: a bigger business-tax wedge lowers it directly, swamping capital scarcity. In the project's combined run, the policy rate is set by a Taylor rule responding to MFA's demand impulse. Both are internally correct; neither contradicts the other once the object named "r" is kept straight.
- **What OG-USA does add that the project lacked:** an independent, mainstream warning that the *financing mix* is not free — if the package's revenue were in fact raised by conventional capital taxation at this scale, the long-run level cost is on the order of 2–3% of output. That is a reason the project's design choices (fee incidence on rents/spreads; TCJA repeal's measured METR path) matter, and a bound the project's documents should acknowledge rather than a number they must adopt.

### 5.4 The three numbers with no external witness

Fee revenue (project: $2,412–3,355B restated, Regime C, unified/floating), T-bill-variant interest savings ($3,765B at zero spread; all-in bound $6,085–6,831B), and transaction-tax revenue ($1,175B at JCT's offset / $1,431B at the corrected offset) were **not** checked by any external simulator, because none can represent them (§2.9): no verified open model has a banking/credit-origination sector with an IORB-linked levy, a Treasury maturity/auction structure, or taxable trading volume — and CBO's corresponding internal models are unpublished (§2.6). The assembled dynamic total (≈ +$3,408B central after funding MFA, headline spread) therefore remains what it was: an assembly of project-model components, of which exactly one (the §201 component inside Title II) gained external corroboration in this mission, and one (the §IX closure logic) gained a sign check with revised magnitudes. The report flags this rather than papering over it: **the mission narrowed the package's uncertainty; it did not distribute it evenly.**

### 5.5 Audit note — the rest of Title II in Tax-Calculator

From the Tax-Calculator scout's verified parameter audit (no runs — an expressibility census for future work): the **payroll add-on** (Additional Medicare Tax / HI rate parameters) is expressible; the **NIIT increase** (3.8% → 6.9%) is expressible (rate parameter exists; CPS top-tail data makes its score among the least reliable); the **5% surtax above $500k** is *not* natively expressible in current taxcalc (the AGI-surtax parameters were removed in 6.9.0; only a top-bracket proxy on taxable income exists); **step-up basis repeal** is *not* expressible (the model taxes realized gains and carries no basis/unrealized-gain data); **HSA termination** is *not* natively expressible (no parameter set). Consequence: a complete Title II microsimulation is **not currently constructible** in the only public microsim — §201 was the right slice to score, and the remaining ~$2.2T of Title II (central) stays at the project's Lane-J standard (published-estimate analogues) until a scorer exists.

---

## 6. What remains unrun, and why

| Item | Status | Reason |
|---|---|---|
| OG-USA transition path (TPI) | **Stopped at a documented point** | Full TPI is a >2 h multi-core job per the maintainers; sandbox has ~1.5 shared CPUs. Reduced TPI by truncating T is **dimensionally inconsistent** with the shipped arrays (probe crashed: `IndexError` in `aggregates.get_RM`; fiscal arrays sized for T=320). Requires a multi-core machine. |
| OG-USA with §201-driven tax functions | Not attempted | The proper route (Tax-Calculator reform → `get_micro_data` → re-estimated ETR/MTR functions) re-estimates from CPS microdata in-box: memory-risky under Dask here, coarser at the top than the direct microsim, and duplicative of §4.1's score. The steady-state lane used scalar levers instead, documented. |
| Dynare NK method check | Scouted feasible, not run | `apt install dynare octave` (6.x) would run a textbook NK wedge/recycling check in seconds, but its ceiling is a labeled toy illustration; it could not move any package number. Available on request. |
| CBO repositories (36) | Census only | No published repo can score any package component (§2.6); HISIM2 and CBO's tax microsim are unpublished. CapTax duplicates CCC's channel more narrowly; CTAM is tariffs; the feedback/rules-of-thumb models only translate exogenous changes. |
| Business-Taxation | **Examined and rejected** | Dormant (~2019), mid-refactor, PUF-gated, author's own "not for publications" warning. |
| sequence-jacobian two-asset HANK | Deferred | ~5–10× the one-asset cost; the §IX sign check does not need it (MPC-by-wealth already generated in one-asset). |
| HAFiscal (HARK REMARK) | Not run | A stimulus-policy analogy in a separate replication repo (checks vs UI vs payroll-tax cuts), not MFA; the core-HARK ingredient check (§4.5) is the honest scope. |
| cstwMPC *estimated* β-distribution in HARK | Approximated, disclosed | The estimated (β̄, ∇) are not in the HARK 0.17.2 package; the lane used a documented β-spread approximation centered on HARK defaults (§4.5). Porting the REMARK's estimated parameters is future work. |

---

## 7. Reproducibility

**Versions that produced the numbers:** taxcalc 6.8.5 · cost-of-capital-calculator 2.1.1 (pandas 2.3.3) · ogcore 0.24.6 + ogusa 0.6.2 · sequence-jacobian 1.0.0 (numpy 2.5.5, scipy 1.18.1, numba 0.68.1) · econ-ark 0.17.2 — all on Python 3.12.3 in per-lane virtualenvs; each lane's `pip_freeze.txt` is committed with its artifacts.

**Artifact map (this repo, `external_sims/`):**
- `taxcalc/` — `repeal201_from2028.json` (the 92-parameter reform), `build_reform.py`, `run_score.py`, `run_beh.py`, `results_static.csv/.json`, `results_behresp_sub025.csv/.json`, `RUN_NOTES.md` (full mapping table + honest label), logs, `pip_freeze.txt`.
- `ccc/` — `run_ccc.py`, `run_sensitivity.py`, `verify_asset.py`, METR/METTR/UCC summary + by-asset CSVs (current vs pre-TCJA + transplant sensitivity), `transplant_revision.json`, `RUN_NOTES.md`, `pip_freeze.txt`.
- `ogusa/` — `run_ss.py`, `run_tpi_probe.py`, `OUTPUT_BASELINE/`, `OUTPUT_REFORM/` (steady-state outputs), `OUTPUT_REFORM1/` (first stance iteration), `RUN_NOTES.md` (mapping table, timings, TPI stopping point), `pip_freeze.txt`. *Excluded from the commit:* `model_params.pkl` files (>2 MB parameter dumps, reproducible from `run_ss.py` + the freeze).
- `seqjac/` — `run_hank.py`, `results.json`, steady-state and IRF arrays (.npz), `RUN_NOTES.md`, `pip_freeze.txt`. *Excluded:* the lane's upstream clone of sequence-jacobian (vendoring upstream code into this repo would be wrong; the pip package at the frozen version is the source).
- `hark/` — `run_experiment.py`, `results.json`, `run_log.txt`, `RUN_NOTES.md`, `pip_freeze.txt`.
- Virtualenvs are excluded throughout (rebuild from the freezes).

**Method note.** Six scout workers verified every simulator claim against live repositories on 2026-11-22 before any run lane was briefed; run lanes inherited scout findings and re-verified at install time (which is how the taxcalc 6.9.x/Python-3.13 trap and the OBBBA-baseline fact were caught *before* they could contaminate a score). Failures encountered are reported in-line above as results, per mission rules: the OG-USA TPI dimensional crash, the HARK truncated-wheel install failure (retried, succeeded), the CCC pandas-3 incompatibility (pinned, disclosed), the SSJ return-line parsing gotcha, and the Pease/OBBBA assertion in the §201 reform build (fixed by a substantively-correct zeroing, disclosed in §4.1).

*End of report.*
