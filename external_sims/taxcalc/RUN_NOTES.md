# RUN NOTES — Medicare for America §201 (TCJA repeal from 2028): Tax-Calculator score of the expressible part

**Date of run:** 2026-11-22 (America/New_York)
**Work dir:** `~/workspace/monetary-symmetry/external_sims/taxcalc/`

> **Honest label (required):** "Static microsimulation estimate, Tax-Calculator 6.8.5, CPS public-use data (cps.csv), author's calculations. Individual income and pass-through provisions only; excludes estate, corporate, and international provisions of TCJA. CPS data under-represent high-income filing units; an independent model estimate, not a JCT or CBO score."
> The behavioral variant is reported separately and is never blended with the static score.

## 1. Setup — versions actually installed

- Python 3.12.3 (system python3, only version in sandbox). Venv at `venv/`.
- **`taxcalc==6.8.5`** installed successfully on first approach (pip index tops out at 6.8.5 here; upstream 6.9.x drops Python 3.12). `import taxcalc; taxcalc.__version__` → `6.8.5`.
- Full `pip freeze` in `pip_freeze.txt`: numpy 2.5.5, pandas 3.1.1, numba 0.67.0, llvmlite 0.49.0, paramtools 0.20.0, bokeh 3.10.2, etc.
- Behavioral response is in-package: `taxcalc.behresp.response()` (added upstream in 6.8.1). In 6.8.5 its API differs from older recipes: elasticities are **scalars** (`{"sub": 0.25}`, not `[0.25]`) and it **returns two DataFrames** `(df1, df2)`, already calculated — see `run_beh.py`. The first attempt with the old list form failed with `TypeError: '>=' not supported between instances of 'list' and 'float'` (saved in `behresp_error.txt` / `run_score.log`); corrected and re-run cleanly.
- Data: `Records.cps_constructor()` only — the public CPS file (`cps.csv.gz`, ships with the package). PUF/TMD are IRS-restricted and were **not** attempted.

## 2. Baseline and reform design

- **Baseline = OBBBA current law** as encoded in taxcalc 6.8.5 `policy_current_law.json` (taxcalc ≥5.2 treats OBBBA, signed July 4, 2025, as current law). There is no "TCJA expires" baseline: OBBBA made most TCJA individual provisions permanent, raised the standard deduction further (2028: $16,993 single / $33,985 joint), set a SALT schedule of $40,000 (2025) +1%/yr through 2029 ($41,212 in 2028) reverting to $10,000 in 2030+, and added temporary tip/overtime/senior/auto deductions for 2025–2028.
- **Reform = active repeal:** `repeal201_from2028.json`, effective tax year **2028**, reverting individual-side parameters to pre-TCJA 2017 law.

### How the 2028 values were obtained (indexing provenance)

The shipped `taxcalc/reforms/2017_law.json` (listed at install time; 83 parameters, authors Holmer/Kallen) was **inspected, not blindly reused**: per upstream issue #2610 it layers on an old baseline, sets values in 2017/2018, and does not by itself undo OBBBA-only parameters. Instead:

1. A `Policy` implementing shipped `2017_law.json` was advanced to 2028 (`build_reform.py`). That policy's 2028 values are exactly the 2017 nominal values inflation-indexed forward by taxcalc's own historical mechanism — 2017_law switches indexing to **unchained CPI-U** via `parameter_indexing_CPI_offset = 0.0025` (2017).
2. Those extracted 2028 values were written into `repeal201_from2028.json` at year 2028 (92 parameters total); taxcalc's indexing then carries them forward 2029–2036.
3. OBBBA-only parameters that 2017_law cannot know about were patched in separately (see §3, "OBBBA undo" rows).

**One forced patch (documented deviation):** restoring the pre-TCJA Pease limitation (`ID_ps`/`ID_prt`) crashed the first run with
`AssertionError: 'Pease and OBBBA cannot both be in effect'` (`calcfunctions.py`, ItemDed).
Fix: `ID_reduction_rate = 0` from 2028 — i.e. OBBBA's top-bracket itemized-deduction reduction (5.4054% in baseline) is switched off, which is substantively correct for a pre-TCJA revert. `ID_AllTaxes_c_po_rate = 0` was also set (OBBBA SALT phase-down rate; moot once the cap is removed, set for cleanliness).

## 3. Parameter mapping table (2028 values in the reform file; 2017 provenance = shipped 2017_law.json nominal 2017/2018 values, indexed as in §2)

| Provision | Parameters set at 2028 | 2028 reform value (headline) | 2017 provenance |
|---|---|---|---|
| Individual rates | `II_rt1`–`II_rt7` | 10 / 15 / 25 / 28 / 33 / 35 / **39.6%** | Pre-TCJA schedule (2017_law §1) |
| Individual brackets | `II_brk1`–`II_brk6` (`II_brk7`=∞ in law) | e.g. brk1 $13,578 / $27,157 / $13,578 / $19,439 / $27,157 (single/joint/sep/head/widow) | 2017 brackets $9,325/$18,650/… indexed |
| Capital-gains brackets | `CG_brk1–3`, `AMT_CG_brk1–3`, `CG_ec` | brk1 = II_brk2 values; brk3 = ∞; ec 0 | 2017_law §9 |
| Standard deduction | `STD` | **$9,246 / $18,493** / $9,246 / $13,615 / $18,493 | 2017: $6,350/$12,700 indexed |
| Std-ded supplements | `STD_Dep`, `STD_Aged` | $1,529; aged $2,257/$1,820… | 2017 values indexed |
| Personal exemptions | `II_em`, `II_em_ps` | **$5,897 restored**; phaseout start $380,779/$456,935… | 2017: $4,050; ps $261,500/$313,800 indexed |
| §199A QBID (repeal) | `PT_qbid_rt`, `PT_qbid_taxinc_thd/gap`, `PT_qbid_w2_wages_rt`, `PT_qbid_alt_w2_wages_rt`, `PT_qbid_alt_property_rt`, `PT_qbid_min_ded` | rt **0**; thresholds 0; gap 1 | Pre-TCJA: no QBID (2017_law §2) |
| Child tax credit | `CTC_c`, `CTC_c-indexed`, `CTC_ps` | **$1,000, not indexed**; ps $75,000/$110,000… | Pre-TCJA CTC |
| Additional CTC | `ACTC_c`, `ACTC_c-indexed`, `ACTC_Income_thd` | $1,000, not indexed; threshold $3,000 | Pre-TCJA ACTC |
| Other dependent credit | `ODC_c` | **0** | No ODC pre-TCJA |
| AMT | `AMT_em`, `AMT_em_ps`, `AMT_em_pe`, `AMT_brk1`, `AMT_child_em` | em $79,068/$123,043…; ps $175,755/$234,292…; pe $363,233 | 2017: em $54,300/$84,500 indexed |
| SALT cap (remove) | `ID_AllTaxes_c` (+ `ID_StateLocalTax_c`, `ID_RealEstate_c` = ∞) | **9e99 (no cap)** vs baseline $41,212 (2028) / $10,000 (2030+) | 2017 itemized treatment, no cap |
| Itemized / Pease | `ID_ps`, `ID_c`, `ID_prt`, `ID_crt` | Pease restored: ps $380,779…; prt 3%; crt 80% | 2017 Pease |
| Itemized categories | `ID_Medical_frt` (10%), `ID_Medical_c`, `ID_InterestPaid_c`, `ID_Charity_c`, `ID_Casualty_c/hc`, `ID_Miscellaneous_c/hc`, `ID_Charity_crt_all` (50%) | Medical floor back to **10%** (from 7.5%); misc & casualty deductions restored (hc 0); caps ∞ | Pre-TCJA itemized rules |
| Excess business losses | `ALD_BusinessLosses_c` | **9e99 (limit repealed)** vs baseline ≈$270k/$540k | No §461(l) limit pre-TCJA |
| Alimony | `ALD_AlimonyPaid_hc`, `AlimonyReceived_frac_in_AGI` | hc 0 (deductible); fraction 1 (includible) | Pre-TCJA alimony regime (note: TCJA's alimony change applied by divorce-instrument date; a parameter model cannot reproduce that grandfathering — see §4) |
| Other ALD | `ALD_DomesticProduction_hc`, `ALD_Dependents_Child_c`, `ALD_Dependents_Elder_c` | 0 / 0 / 0 | 2017_law §7/§9 |
| EITC (TCJA barely touched it; values reset to 2017_law's indexed path) | `EITC_c`, `EITC_ps`, `EITC_ps_addon_MarriedJ`, `EITC_InvestIncome_c` | c $743/$4,951/$8,178/$9,200 | 2017: $510/$3,400/$5,616/$6,318 indexed |
| Indexing | `parameter_indexing_CPI_offset` | 0.0025 at 2028 (prospective switch toward unchained CPI-U indexing, mirroring 2017_law) | TCJA made chained CPI-U permanent; §201 repeal restores CPI-U |
| Misc 2017_law §9 resets | `II_credit*`, `CTC_new_ps`, `ETC_pe_*`, `FST_AGI_thd_*`, `AGI_surtax_thd`, `UBI_*` | All as extracted (mostly 0 / ∞ / 2017 values) | Parameters TCJA did not change except via indexing |
| **OBBBA undo** (not TCJA items strictly, but in the same parameter universe; zeroed so the 2028 reform year is a clean pre-TCJA state) | `TipIncomeDed_c`=0, `OvertimeIncomeDed_c`=0, `SeniorDed_c`=0, `AutoLoanInterestDed_c`=0, `ID_Charity_frt`=0, `STD_charity_ded_nonitemizers_max`=0, `ID_reduction_rate`=0, `ID_AllTaxes_c_po_rate`=0 | All zero from 2028 | These are OBBBA (2025) additions, **not** TCJA provisions. Tip/overtime/senior/auto already expire after 2028 in the baseline, so zeroing affects only 2028. The OBBBA charity floor and non-itemizer charity deduction are permanent in baseline, so zeroing affects all years — flagged here because a strict "TCJA-only" reading of §201 would leave them in place; their revenue effect is small relative to the total but is inside this score. |

## 4. What could NOT be reverted via parameters (with reason)

| Provision | Why not in the model |
|---|---|
| Estate & gift tax exemption (§2010/§2505) | Tax-Calculator models the **income** tax only; no estate-tax module exists. Bounded from published figures in §6. |
| Corporate rate §11 (21% → 35%), corporate AMT repeal | No corporate tax model in Tax-Calculator. Bounded in §6. |
| §174 R&D amortization, §163(j) business-interest limit (corporate side), bonus depreciation / corporate expensing | Corporate-side cost recovery is not parameterized in the individual model. (Pass-through income *levels* in CPS are taken as given.) Bounded in §6. |
| International: GILTI / FDII / BEAT / territorial system / §965 | Not parameterized. Bounded in §6 (JCX-67-17 international package was a net **raiser**, +$324B/10yr — repealing it *loses* revenue). |
| Mortgage-interest cap details ($750k vs $1M acquisition debt, grandfathering) | Tax-Calculator has a single `ID_InterestPaid_c` (=∞ in both regimes); the CPS does not split mortgage debt by vintage. The 2017_law file likewise treats this via the ∞ cap. Effect is inside the itemized-deduction aggregate only to the extent CPS mortgage interest is reported. |
| Alimony grandfathering by instrument date | See §3 note — parameter is a single haircut; pre-2019 instruments' treatment cannot be separated in CPS. |
| Moving-expense, bicycle, and other small TCJA suspensions; §199A *specified-service* details beyond the QBID parameters | Either no distinct parameter or no CPS variable to bite on; QBID itself is fully zeroed. |
| Individual mandate penalty ($0 since 2019) | A TCJA provision, but it is an ACA penalty, not an income-tax parameter in this model, and restoring it is not an income-tax-liability item in `iitax`. Excluded; likely not intended as a §201 revenue item. |

## 5. Results — model output (tax years; `iitax` × CPS weights `s006`; reform − baseline)

### 5a. Static (headline) — `results_static.csv` / `.json`, script `run_score.py`

| Year | Baseline $B | Reform $B | **Diff $B** |
|---:|---:|---:|---:|
| 2028 | 2,227.1 | 2,537.5 | **310.3** |
| 2029 | 2,341.4 | 2,639.3 | **297.9** |
| 2030 | 2,476.2 | 2,750.8 | **274.6** |
| 2031 | 2,584.4 | 2,865.2 | **280.8** |
| 2032 | 2,696.9 | 2,983.1 | **286.2** |
| 2033 | 2,810.4 | 3,102.0 | **291.7** |
| 2034 | 2,930.0 | 3,227.1 | **297.1** |
| 2035 | 3,054.3 | 3,356.4 | **302.1** |
| 2036 | 3,163.1 | 3,469.7 | **306.6** |
| **2028–36 total** | | | **$2,647.4B ≈ $2.65T** |

Year pattern explained: the 2030 dip is mechanical — the OBBBA baseline SALT cap falls from ~$41.6k (2029) to $10,000 (2030), raising baseline revenue and shrinking the repeal gain; the OBBBA tip/overtime/senior deductions also expire in the baseline after 2028, removing that part of the 2028-only gain. Growth thereafter is nominal CPS extrapolation growth.

**Cross-check:** CBO/JCT's cost of *extending* the expiring individual provisions was $3,256B over FY2025–34 (Table 2, §6), i.e. roughly $355–434B/yr in 2028–34 on a fiscal-year, PUF-based JCT model. This CPS static run gives $275–310B/yr on a tax-year basis against an **OBBBA** baseline (which is more generous than the pre-OBBBA baseline JCT used — bigger standard deduction and the 2028–29 SALT schedule — mechanically shrinking the repeal gain). Same order of magnitude; the gap is consistent with (i) baseline difference, (ii) CPS under-representation of high-income units, and (iii) tax-year vs fiscal-year timing. It is not evidence either figure is wrong.

### 5b. Behavioral variant — REPORTED SEPARATELY, NEVER BLENDED

**Conventional, assumed taxable-income elasticity 0.25** — `taxcalc.behresp.response(calc1, calc2, {"sub": 0.25})`, substitution effect only, no income/capital-gains effects. Files: `results_behresp_sub025.csv` / `.json`, script `run_beh.py`.

| Year | Diff $B (behresp) |
|---:|---:|
| 2028 | 253.8 |
| 2029 | 238.4 |
| 2030 | 210.2 |
| 2031 | 214.1 |
| 2032 | 216.9 |
| 2033 | 219.4 |
| 2034 | 222.2 |
| 2035 | 224.6 |
| 2036 | 227.2 |
| **Total** | **$2,026.8B ≈ $2.03T** |

The behavioral response erodes ≈23% of the static gain — in line with a 0.25 taxable-income elasticity applied to a broad rate increase.

## 6. Bounding the rest — PUBLISHED-FIGURE BOUND, NOT MODEL OUTPUT

Sources verified live on 2026-11-22:

1. **CBO, *Budgetary Outcomes Under Alternative Assumptions About Spending and Revenues*, May 2024 (publication 60114), Table 2** (JCT estimates, FY2025–2034, primary-deficit effect of *extending* the expiring provisions — the mirror image of repealing them):
   - Individual income tax provisions: **$3,256B** (year values 2028–34: 355, 364, 374, 387, 403, 419, 434).
   - Higher estate & gift exemptions: **$167B** (2028–34: 17, 18, 20, 21, 22, 24, 25 — ≈$21B/yr and rising).
   - Investment-cost (bonus depreciation) extension: **$378B**.
   - Certain business provisions maintained: **$172B**. (Business subtotal $378+$172 = $550B ≈ the $551B cited in CRS.)
   - URL: https://www.cbo.gov/system/files/2024-05/60114-Budgetary-Outcomes.pdf
2. **CRS R48286, *Expiring Provisions of P.L. 115-97 (TCJA): Economic Issues* (updated Jan. 17, 2025)**, Summary / Revenue Effects: confirms the same JCT figures — individual $3.3T, estate $167B, business $551B, total ≈$4.0T, FY2025–34 — and notes a separate estimate that restoring §174 R&D expensing + the EBITDA base for §163(j) would cost **$249B/10yr** (a piece of the corporate remainder; do not double-count with item 3 below).
3. **JCT, JCX-67-17 (Dec. 18, 2017), original TCJA score, FY2018–27:** total −$1,456B; individual reform −$1,126B; business reform −$654B; international reform **+$324B** (a net raiser). The corporate rate cut **alone** was **−$1,349B** gross (corroborated in Lyon & McBride's JCX-67-17-derived table: rate −$1,348.5B, cost recovery +$466.1B, international +$324.4B, total corporate provisions ≈ −$398B). **Key implication:** the permanent corporate/international package was mostly *paid for within itself* at enactment — repealing "the entire TCJA" corporate side does **not** yield the gross $1.35T rate figure; it yields the gross rate gain *minus* the revenue lost by repealing TCJA's own corporate raisers (§163(j), NOL limits, §174 amortization from 2022, GILTI/BEAT, etc.).

### Remainder bound for FY2028–36 (9 years, the §201 window)

| Component | Bound | Basis |
|---|---:|---|
| Estate & gift exemption reversion | **+$0.17T to +$0.23T** | CBO Table 2 estate row: ≈$147B in 2028–34 alone, ~$25B/yr and growing ~5%/yr → ≈$0.19T for 2028–36, rounded to a range |
| Corporate + international permanent provisions, **net** (§11 rate, §174, §163(j), expensing, GILTI/FDII/BEAT, corporate AMT) | **+$0.5T to +$1.5T** (wide, crude) | Gross rate reversion at 2028–36 scale: JCX-67-17's −$1,349B (FY18–27) scaled by nominal corporate-receipts growth (≈1.6–1.9×) ⇒ ≈$2.2–2.6T gross; minus repeal of TCJA corporate raisers, which were +$0.95T-class in original terms (cost recovery +$466B, international +$324B, interest/NOL/compensation items) and scale similarly ⇒ net ≈$0.5–1.5T. This is a scaled published-figure bound, **not** a score. |
| **Total remainder** | **≈ +$0.7T to +$1.7T** | Sum of the two rows |

**Universe warning (explicit):** §201's universe — the *entire* TCJA including permanent provisions, from 2028 — is **larger** than the "expiring provisions" universe of CBO Table 2 / CRS R48286 ($4.0T, FY25–34). Those tables contain **no** corporate-rate, §174, §163(j), or international amounts at all (except the $249B §174/§163(j) restoration note in CRS), which is why the corporate row above has to be built from the 2017 JCX-67-17 score instead, with all the scaling caveats stated.

## 7. Implied full §201 vs the project's $3.9T assumption

| | FY2028–36 (9 tax years) |
|---|---:|
| Individual + pass-through (this run, static, CPS) | $2.65T |
| Remainder bound (published figures) | $0.7T – $1.7T |
| **Implied full §201 range** | **≈ $3.3T – $4.4T, midpoint ≈ $3.85T** |
| Project's carried assumption (central, FY28–36) | $3.9T |
| If the behresp variant were used for the individual part instead (never blended above) | ≈ $2.7T – $3.7T |

**Verdict:** the project's $3.9T central assumption sits **inside** the implied range and very close to its midpoint — it survives this check as a *central* assumption, but it is **not** confirmed as a score: (i) the model piece ($2.65T) is a CPS tax-year estimate against an OBBBA baseline, biased down by CPS high-income under-representation; (ii) roughly a third of the total rests on the crude corporate scaling in §6, which is the dominant uncertainty; (iii) window honesty — all figures here are tax years 2028–36 (9 years); the CBO/CRS anchors are FY2025–34 (10 fiscal years) and JCX-67-17 is FY2018–27, and no figure has been silently re-windowed without saying so.

## 8. Artifacts

- `repeal201_from2028.json` — the reform file (92 parameters, all at 2028)
- `build_reform.py` — extraction of 2028 values from shipped `2017_law.json`
- `run_score.py` / `run_score2.log` — static run (log includes the Pease/OBBBA assertion from the first attempt)
- `run_beh.py` / `run_beh.log` — behavioral run; `behresp_error.txt` — the superseded API error
- `results_static.csv` / `.json`; `results_behresp_sub025.csv` / `.json`
- `pip_freeze.txt`; this file, `RUN_NOTES.md`
- Installed reforms directory listing (from `taxcalc/reforms/` in the venv): `2017_law.json`, `TCJA.json`, `ARPA.json`, `CARES.json`, `BrownKhanna.json`, `Larson2019.json`, `Renacci.json`, `SandersDeFazio.json`, `Trump2016/2017.json`, `ConsolidatedAppropriationsAct2021.json`, `ext.json`, `ptaxes0–3.json`, `archive/`, plus `.out.csv` expected-output files and `REFORMS.md`.
