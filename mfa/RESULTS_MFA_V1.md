# RESULTS MFA V1 — Medicare for America gross cost & residual financing

**This is a modeller's construction, not a score.** No official CBO, JCT or CMS
Office of the Actuary estimate of any version of Rosa DeLauro's Medicare for
America Act exists — that was verified against KFF, CHRT and CBO's own
catalogue in Lane C (`research/MEDICARE_FOR_AMERICA_SOURCES.md`), and nothing
found in this lane changes it. Everything below is built in the open from the
bill text of **H.R.10924 (119th Cong., "Medicare for America Act of 2026")**,
CBO's February 2026 baselines, and a parameter table in which every entry is
labelled **SOURCED**, **ANCHORED** (derived from a sourced aggregate),
**ARITHMETIC-ESTIMATE** or **ASSUMPTION** (`data/parameters.csv`). Treat the
outputs as ranges with named drivers, never as points. Code: `mfa_model.py`
(stdlib only; `python3 mfa_model.py` reproduces every table). Annual detail:
`data/annual_detail.csv`. One-page financing table: `financing_table.csv`.

Window: **FY2028–36** (MFA costs begin in 2028 under the bill). Federal
**outlays** concept throughout, consolidated federal view. Fee-side totals are
FY2027–36 from the fee project — the extra FY2027 on the fee side is immaterial
(fee collections begin 2028 and are ~$0.01–0.02T in the phase-in year).

---

## 1. The financing identity (Lane C §4, followed exactly)

> Residual for the Monetary Symmetry Fee + interest savings
> = Gross new federal MFA spending
> − Displaced federal outlays (phased 2030 / 2033 / 2035 — never steady-state)
> − Enrollee premiums (§2204) − Employer contributions (§125)
> − State Medicaid MOE (§2209: **$0 in-window**) − Title II revenues (the bill's own)

| $T, FY2028–36 | Low | Central | High (stress) |
|---|---:|---:|---:|
| **Gross MFA cost** | **18.09** | **24.92** | **36.15** |
| − Displaced outlays | 12.57 | 13.09 | 13.47 |
| = Incremental cost before MFA's own offsets | 5.52 | 11.83 | 22.68 |
| − Premiums | 1.35 | 1.93 | 2.61 |
| − Employer contributions | 0.51 | 1.27 | 2.03 |
| − Title II revenues | 4.96 | 6.11 | 7.31 |
| − State MOE (bill as written) | 0.00 | 0.00 | 0.00 |
| **= RESIDUAL for fee + interest savings** | **−1.29** | **+2.52** | **+10.73** |
| Residual if accelerated-MOE *amendment* added (not in the bill) | −4.35 | −0.54 | +7.67 |

A negative residual means the bill's own financing more than covers the
incremental cost in-window, before any Monetary Symmetry Fee.

---

## 2. Gross cost build

Enrollment is built by **origin cohort** from CBO Feb 2026 baseline populations
(Medicare Part A 73.1M in 2028 → 80.5M in 2036; Medicaid average monthly 79M →
73M; uninsured ~31.5M → 37M — note this *updates* the ~26M uninsured figure in
older project briefs: CBO's post‑P.L.119‑21 baseline has uninsurance rising to
~37M), switched into MFA on the bill's own dates:

- **2028–29:** transitional public option (take-up 25/40/55% of the exchange
  population) + uninsured auto-enrollment (50/70/85% take-up). Enrollment
  ~29M. **No displacement yet — these years are pure addition**, plus the
  §2206(b)(4) top-up and §124 waiting-list clearance.
- **2030:** Medicare non-duals switch (~61M). **2031:** large-employer process
  begins; ESI opt-in ramp starts. **2033:** duals, Medicaid expansion adults,
  CHIP and the exchange population switch (exchanges terminate). **2035:**
  residual Medicaid switches. Central enrollment reaches **197M by 2036**
  (868–1,114M enrollee-years over the window across cases).

Per-enrollee core cost (2028$, plan-paid, anchored to CBO per-capita spending:
Medicare non-dual $17,500; duals $32,000; Medicaid non-dual $11,500; exchange
$7,800; uninsured $6,800; ESI opt-in $8,600) is grown at 4.0/4.8/5.8% per year
(CBO baselines imply ~4.5–4.9% per-enrollee growth) and multiplied by three
explicit §2205/§2206 factors: a **rate factor** 1.03/1.06/1.10 (higher-of
Medicare/Medicaid, hospitals ≥110%, +30% primary/behavioural RVUs, net of
site-neutral payment), an **induced-demand/capacity factor** 1.00/1.07/1.15,
and a **cost-sharing richness factor** 1.02/1.05/1.08 (plan pays 80%/100%, no
deductible, OOP caps, vs. baseline cost-sharing). On top:

- **Dental/vision/hearing:** $400/$650/$900 per enrollee-year.
- **HCBS long-term services (Part B entitlement, ≥1 ADL):** users = 3/5/8% of
  enrollment at $28k/$36k/$48k per user (MACPAC CY2021: HCBS users were 2.6% of
  Medicaid enrollees at >$32k per user under *narrower* waiver eligibility;
  I/DD participants ~$55k). A "new-cost factor" (Medicaid origin 0.35, duals
  0.40, others 1.00) avoids charging MFA for HCBS the baseline already funds.
  **LTSS totals $0.7T (low) / $2.0T (central) / $5.1T (high)** — the single
  widest swing in the build.
- **Admin:** 2/3/5% of benefits.
- **§2206(b)(4) Medicaid rate top-up, 2028–33:** 3/5/8% of federal Medicaid
  outlays (~$0.13–0.36T total). **§124 waiting-list clearance:** $15/$35/$60B
  spread over 2028–30.

Central gross cost rises from $0.38T (2028) to **$5.34T (2035) / $5.71T
(2036)** — about $27.5k per enrollee in 2036, at the level of baseline
Medicare gross per-capita spending, reflecting a late-window mix dominated by
the Medicare/Medicaid cohorts plus LTSS. The **high case is a stress bound**,
not a central tendency: it stacks the top of every multiplier and growth range
(2036: $8.04T, ~84% of projected national health expenditure) and is presented
to bound the residual, not as a forecast.

## 3. Offsets — all phased, none steady-state

- **Displaced outlays ($12.6–13.5T, remarkably case-insensitive):** Medicare
  net outlays displaced from 2030 (non-dual spending share 70% assumed) and in
  full from 2033; federal Medicaid+CHIP from 2033 (duals+expansion share
  40/47/54% of spending) and in full from 2035; marketplace premium tax
  credits from 2033 (CBO PTC baseline: $88B in 2026 → $116B in 2036). Medicare
  is displaced on a **net-outlay** basis (baseline premiums already netted);
  MFA premiums below are MFA's own new receipts, so nothing is counted twice.
  **Not counted** (conservative): states' saved Medicaid share (~$335B/yr by
  the late window — that is state fiscal relief, and it is also the economic
  source from which any future MOE would be paid), federal uncompensated-care
  savings, and §125(c) employer opt-out contributions.
- **Premiums ($1.35–2.61T):** simplified income-bracket model (labelled as
  such): 33% of enrollees <200% FPL pay $0; brackets 200–400 / 400–600 /
  >600% FPL pay on average $1,100 / $2,400 / $3,900 per enrollee-year (2028$,
  central), grown at 4%. Caveat: §2204(b)(1)'s cost-referential
  premium-setting could imply materially higher full premiums above 600% FPL;
  the model is deliberately conservative there.
- **Employer contributions ($0.51–2.03T, from 2031 only):** 8% of payroll ×
  large-employer payroll base ($9.5T in 2031, +4.2%/yr — assumption) ×
  non-offering share 10/25/40%. Small employers owe $0 (verified). Employers
  offering qualifying plans pay the Trust Fund nothing — the common shorthand
  "8% of all payroll" would overstate this line several-fold.
- **Title II revenues ($4.96–7.31T) — the bill's primary financing, and the
  largest offset.** Components (FY28–36): TCJA + P.L.119‑21 repeal, tax side
  only: $3.2/3.9/4.6T — an **analogue**, from CBO/JCT's estimate that extending
  the expiring TCJA provisions would add ~$4.6T to deficits over 10 years
  including ~$0.6–0.8T of interest; it is **not** a JCT score of H.R.10924,
  and repealing P.L.119‑21 would also restore that law's health-spending cuts
  (raising baseline Medicaid and hence displaced amounts — an interaction
  flagged here, not modelled). Payroll add-on 0.9%→4%: $0.95–1.35T
  (arithmetic on the existing Additional Medicare Tax base). NIIT 3.8%→6.9%:
  $0.38–0.56T (arithmetic). 5% surtax >$500k: $0.22–0.40T. Stepped-up-basis
  repeal: $0.13–0.22T. Excises + HSA termination: $0.08–0.18T.
- **State MOE: $0** in every case (bill as written; first payment year 2038,
  §2209). The **accelerated-MOE variant** (+$3.07T, from FY2030 on the FY2024
  state own-spending base of $334.7B, Pew/CMS‑64, +3%/yr) is a *project
  amendment*, not bill text — and it carries a real caveat: in 2030–32 states
  would pay MOE while still carrying their full Medicaid obligations, a double
  burden the bill's own post-2036 timing avoids.

## 4. Financing verdict matrix

Fee cases are the fee project's combined totals (net fee + consolidated
interest saving, FY27–36, Lane F corrected covered base, β=0.88): **s=50%
central $4.44T · s=75% strict-base $5.60T · s=75% central $6.71T · s=90%
central $8.12T**. Cell = fee total − residual ( **+ = financed with surplus /
− = shortfall** ), $T:

| MFA residual case | s=50% $4.44T | s=75% strict $5.60T | s=75% central $6.71T | s=90% central $8.12T |
|---|---:|---:|---:|---:|
| **Low (residual −$1.29T)** | +5.73 ✓ | +6.89 ✓ | +8.00 ✓ | +9.41 ✓ |
| **Central (residual +$2.52T)** | +1.92 ✓ | +3.08 ✓ | +4.19 ✓ | +5.59 ✓ |
| **High stress (residual +$10.73T)** | −6.29 ✗ | −5.13 ✗ | −4.02 ✗ | −2.61 ✗ |
| High stress + accelerated-MOE amendment (residual +$7.67T) | −3.23 ✗ | −2.07 ✗ | −0.96 ✗ | **+0.45 ✓** |

**Plainly stated:**

1. **In the low case, Medicare for America is financed without the fee at
   all** — its own Title II taxes, premiums and employer contributions exceed
   the phased incremental cost by ~$1.3T in-window. Any fee revenue is surplus
   on top.
2. **In the central case, it is financed at every dial in the fee grid** —
   even the 50% statutory floor ($4.44T against a $2.52T residual, a $1.92T
   margin). But be clear about *what is doing the work*: Title II contributes
   $6.11T, more than the fee itself at s=75% ($6.71T combined, of which the
   pure fee is ~$4.8T net). The fee covers the *residual*; it does not
   "finance Medicare for America" in the gross sense — gross cost is $24.9T
   and no fee case comes within a factor of three of that. Claims in either
   direction that skip Title II or compare the fee to gross cost misstate the
   arithmetic (Lane C §4, points 5–6).
3. **In the high-cost stress case, it is not financed at any dial** —
   shortfalls of $2.6–6.3T. Even adding the (non-bill) accelerated-MOE
   amendment, only s=90% closes the gap, by $0.45T. The stress case is driven
   mainly by the LTSS and induced-demand stack (§5), so the honest summary is:
   **financing holds unless the new LTSS entitlement and utilisation response
   come in at the top of their plausible ranges — in which case no setting of
   the Monetary Symmetry dial within its statutory 50–90% range finances the
   bill, and the gap would fall on the §2207(b)(3) authorised appropriations
   (i.e., general revenue / borrowing), exactly as the bill's own text
   contemplates.**

## 5. What drives the answer — sensitivity (one-at-a-time on the central case)

| Change from central | Δ residual ($T) |
|---|---:|
| LTSS parameters → high (8% users × $48k) | **+2.34** |
| LTSS parameters → low (3% × $28k) | −1.10 |
| Induced demand 7% → 15% / → 0% | +1.63 / −1.42 |
| Title II → low range / → high range | +1.15 / −1.20 |
| Per-capita growth 4.8% → 5.8% / → 4.0% | +1.35 / −1.03 |
| ESI opt-in ramp → high / → zero | +0.88 / −1.12 (gross effect; high ramp also raises premiums) |
| Employer non-offering share 25% → 40% / → 10% | −0.76 / +0.76 |
| §2206 rate factor 1.06 → 1.10 | +0.82 |

**The two or three dominant parameters**, as expected: **(1) the HCBS LTSS
entitlement** (take-up × unit cost — a $3.4T swing across its range, and the
least-anchored number in the build because MFA's ≥1‑ADL threshold has no
current-programme counterpart); **(2) the per-capita cost stack** (induced
demand, cost growth, rate and cost-sharing factors compound over 990M
enrollee-years — together a ±$3–4T swing); **(3) the Title II take**, above
all the TCJA/P.L.119‑21 repeal analogue ($1.4T range on that component alone,
and it rests on analogy, not a JCT score). Employer-population enrollment
matters mainly through (2); it is not independently decisive.

## 6. Known weaknesses (read before citing any number above)

1. **No dynamic/behavioural scoring.** TCJA repeal and the payroll/NIIT
   increases would change GDP, wages and their own bases; JCT would net some
   of that. The model's Title II range is wide partly to absorb this.
2. **Induced demand is applied uniformly**, including to the
   already-fully-insured Medicare cohort, where the true response is likely
   smaller; conversely the uninsured cohort's pent-up demand may exceed 15%
   in early years. Direction of net bias is unknown.
3. **§2204 premium-setting** is cost-referential in the text; if HHS set
   community premiums near full cost for unsubsidised enrollees, premium
   receipts could be far above the model's conservative bracket figures —
   but opt-out into qualifying employer coverage would then also rise,
   cutting enrollment. The model holds both at central values.
4. **Capacity constraints are a parameter, not a model.** A 15% utilisation
   response assumes supply (workforce, HCBS labour) materialises; §2206
   rate reviews "for access" could push the rate factor above 1.10 if it
   does not.
5. **P.L.119‑21 repeal interaction** (Title II, §3 above) is flagged, not
   modelled: it would raise the Medicaid baseline, increasing both gross-era
   overlap and displaced outlays in 2033–35.
6. **Displacement compliance** (state waivers up to 2 years, MA-for-America
   leakage) is a single 95–100% factor; slower real-world transitions would
   shift displaced amounts right, worsening early-window residuals while
   leaving the 10-year total less changed.
7. Nothing here is discounted, and no interest feedback from MFA-driven
   deficits/surpluses is included — that belongs to the consolidated SFC
   layer, as does any GDP feedback from the fee itself (Lane H's flow
   channel: if fee receipts are *spent* on MFA rather than held against
   deficits, the demand sign flips positive — the financing verdict above is
   an accounting identity, not a macro outcome).

## 7. Files

- `mfa_model.py` — the model (parameters in-code, mirrored in
  `data/parameters.csv` with labels and sources).
- `data/annual_detail.csv` — year-by-year enrollment, gross components,
  displaced, premiums, employer contributions, accelerated-MOE variant.
- `data/financing_matrix.csv`, `data/summary.json` — machine-readable outputs.
- `financing_table.csv` — the one-page financing table (identity + matrix).

*Sources retrieved/used in this lane: CBO Medicare and Medicaid Baselines
(Feb 2026); CBO, Federal Subsidies for Health Insurance (Feb 2026, May 2026
presentation — Medicare $16.1T and Medicaid/CHIP $8.4T subsidy concepts,
PTC+related $1.227T 2026–36, coverage averages incl. uninsured 36.1M);
CBO/JCT TCJA-extension estimates (~$4.6T deficit / ~$4.0T revenue, via CBO
and Tax Policy Center summaries); MACPAC, Spending and Utilization for
Medicaid HCBS (July 2025 — >$32k per HCBS user CY2021, users 2.6% of
Medicaid enrollees); USAFacts/MACPAC Medicaid spending per enrollee
($10,760, FY2024); Pew/CMS-64 state Medicaid own-spending ($334.7B,
FY2024); bill text and all §-level facts from Lane C's verified read of
H.R.10924.*
