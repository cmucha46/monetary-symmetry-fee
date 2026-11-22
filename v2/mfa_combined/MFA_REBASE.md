# MFA RE-BASE — Medicare for America (H.R.10924, 119th Cong.) annual paths, FY2028–36

**Lane 1 (MFA re-base), Combined Study: Monetary Symmetry Fee v2 + Medicare
for America under a spending closure.** This file re-bases the v1 MFA model
(`~/workspace/monetary-symmetry/mfa/`, Lane J) onto annual paths so the fee
study's later lanes can net the fee against MFA year by year.

> **Standing caveat — read before citing any number here.** There is **NO
> CBO, JCT, or CMS Office of the Actuary score of H.R.10924** (verified in
> Lane C, `research/MEDICARE_FOR_AMERICA_SOURCES.md`). Every figure below is
> a modeller's construction from the bill text, CBO February 2026 baselines,
> and a labelled parameter table — ranges with named drivers, never points.
> The largest single Title II component (TCJA + P.L.119-21 repeal) is an
> **extension-analogue ASSUMPTION, not a JCT score** (see §4).

Units: $B in the annual tables, $T in the window tables. Window: FY2028–36.
Concept: federal outlays, consolidated federal view. State Medicaid MOE
(§2209) = **$0 in-window** in all scenarios (first payment year 2038, bill
as written) and is therefore not a column in the annual file.

---

## 1. Reproduction verdict

**EXACT MATCH on every headline number.** The v1 model was re-run from a
pristine copy in a scratch directory (`python3 mfa_model.py`, stdlib only);
the originals in `~/workspace/monetary-symmetry/mfa/` were not modified
(md5s unchanged). The re-run's three output files are **byte-identical** to
the shipped v1 outputs (`data/annual_detail.csv`,
`data/financing_matrix.csv`, `data/summary.json`).

Window totals, stated vs reproduced ($T, FY2028–36):

| Component | Low stated | Low repro | Central stated | Central repro | High-stress stated | High-stress repro |
|---|---:|---:|---:|---:|---:|---:|
| Gross cost | 18.09 | 18.095 | 24.92 | 24.917 | 36.15 | 36.152 |
| Displaced outlays | 12.57 | 12.571 | 13.09 | 13.085 | 13.47 | 13.471 |
| Premiums | 1.35 | 1.346 | 1.93 | 1.932 | 2.61 | 2.614 |
| Employer contributions | 0.51 | 0.507 | 1.27 | 1.267 | 2.03 | 2.027 |
| Title II revenues | 4.96 | 4.960 | 6.11 | 6.110 | 7.31 | 7.310 |
| State MOE (§2209) | 0.00 | 0.000 | 0.00 | 0.000 | 0.00 | 0.000 |
| **RESIDUAL** | **−1.29** | **−1.289** | **+2.52** | **+2.524** | **+10.73** | **+10.730** |
| Residual w/ accelerated-MOE amendment (not in bill) | −4.35 | −4.354 | −0.54 | −0.541 | +7.67 | +7.665 |

Title II components, stated vs reproduced ($T) — all exact:

| Component | Low | Central | High-stress |
|---|---:|---:|---:|
| TCJA + P.L.119-21 repeal (analogue assumption) | 3.20 | 3.90 | 4.60 |
| Payroll add-on 0.9%→4% | 0.95 | 1.15 | 1.35 |
| NIIT 3.8%→6.9% | 0.38 | 0.47 | 0.56 |
| 5% surtax >$500k | 0.22 | 0.30 | 0.40 |
| Step-up repeal | 0.13 | 0.17 | 0.22 |
| Excises + HSA termination | 0.08 | 0.12 | 0.18 |
| **Total** | **4.96** | **6.11** | **7.31** |

Gross-cost components also reproduce: LTSS $0.78 / $2.00 / $5.12T;
§2206 top-up $0.13 / $0.22 / $0.36T; §124 waitlist $15 / $35 / $60B;
enrollee-years 868 / 992 / 1,114M; 2036 enrollment 175 / 197 / 223M.

### Discrepancies found (both inside the v1 *narrative*, not the model)

1. **RESULTS_MFA_V1.md §2 misstates central gross cost in 2035/36.** The
   text says central gross "rises … to **$5.34T (2035) / $5.71T (2036)**";
   the model (and its own `annual_detail.csv`) produces **$5.09T (2035) /
   $5.41T (2036)**. The window total ($24.92T) is unaffected and correct;
   only those two narrative year figures are wrong (each ~$0.25–0.30T too
   high). Do not cite the $5.34T / $5.71T figures.
2. **LTSS low case is understated in the v1 text.** RESULTS §2 says LTSS
   totals "$0.7T (low)"; the model produces **$0.775T**, which rounds to
   $0.78T, not $0.7T. Central ($2.0T) and high ($5.1T) as stated are correct.

No other stated number failed to reproduce.

---

## 2. Annual paths and residuals

Residual(year) = gross − displaced − premiums − employer − Title II.
Gross components, displaced, premiums and employer values are the v1
model's own (unrounded, then rounded to $0.1B for presentation — they match
`annual_detail.csv`). **Title II annual values are this lane's
annualization** — v1 stores Title II as window totals only; see §3 before
using the annual residuals.

### 2a. Low scenario ($B)

| Year | Gross | Displaced | Premiums | Employer | Title II | Residual | Cumulative residual |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2028 | 208.1 | 0.0 | 25.3 | 0.0 | 464.9 | −282.1 | −282.1 |
| 2029 | 212.0 | 0.0 | 26.7 | 0.0 | 484.4 | −299.0 | −581.2 |
| 2030 | 1,482.9 | 909.7 | 104.0 | 0.0 | 504.7 | −35.5 | −616.7 |
| 2031 | 1,578.6 | 966.7 | 112.0 | 76.0 | 525.9 | −102.0 | −718.7 |
| 2032 | 1,682.0 | 1,027.3 | 120.4 | 79.2 | 548.0 | −92.9 | −811.6 |
| 2033 | 2,601.1 | 1,977.9 | 181.5 | 82.5 | 571.0 | −211.9 | −1,023.5 |
| 2034 | 2,721.5 | 2,091.3 | 192.5 | 86.0 | 595.0 | −243.3 | −1,266.8 |
| 2035 | 3,714.9 | 2,724.9 | 284.8 | 89.6 | 620.0 | −4.4 | −1,271.2 |
| 2036 | 3,893.8 | 2,873.4 | 299.1 | 93.4 | 646.0 | −18.1 | **−1,289.3** |

The low-case residual is **negative in every year**: the bill's own
financing (Title II from 2028, premiums, employer contributions from 2031)
exceeds the phased incremental cost throughout the window. Cumulative
residual **−$1.29T** — MFA needs no fee contribution in this scenario.

### 2b. Central scenario ($B)

| Year | Gross | Displaced | Premiums | Employer | Title II | Residual | Cumulative residual |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2028 | 382.7 | 0.0 | 46.0 | 0.0 | 572.6 | −236.0 | −236.0 |
| 2029 | 389.3 | 0.0 | 48.4 | 0.0 | 596.7 | −255.8 | −491.7 |
| 2030 | 1,957.0 | 938.5 | 145.3 | 0.0 | 621.7 | +251.5 | −240.2 |
| 2031 | 2,121.4 | 997.3 | 159.2 | 190.0 | 647.9 | +127.1 | −113.1 |
| 2032 | 2,303.3 | 1,059.8 | 174.0 | 198.0 | 675.1 | +196.5 | +83.4 |
| 2033 | 3,524.3 | 2,097.5 | 257.4 | 206.3 | 703.4 | +259.6 | +343.0 |
| 2034 | 3,736.9 | 2,216.9 | 276.1 | 215.0 | 733.0 | +296.0 | +639.0 |
| 2035 | 5,090.6 | 2,811.0 | 400.7 | 224.0 | 763.8 | +891.1 | +1,530.1 |
| 2036 | 5,411.4 | 2,964.1 | 424.6 | 233.4 | 795.8 | +993.4 | **+2,523.6** |

Shape: two surplus years (2028–29, when Title II is already collecting but
MFA is only a transitional option), then a positive residual from 2030 on.
The cumulative residual crosses zero during **2032**. The **worst years are
the last two — 2036 (+$993B) and 2035 (+$891B)** — because the 2035 residual-
Medicaid switch lifts gross cost (~+$1.35T in one year) by more than the
completion of Medicaid displacement adds in offsets. 2035–36 alone account
for $1.88T (75%) of the $2.52T cumulative residual: **the central residual
is a late-window phenomenon**, which matters for any fee path that is
itself back- or front-loaded.

### 2c. High-stress scenario ($B) — v1 code name "high"

| Year | Gross | Displaced | Premiums | Employer | Title II | Residual | Cumulative residual |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 2028 | 646.6 | 0.0 | 69.6 | 0.0 | 685.1 | −108.0 | −108.0 |
| 2029 | 662.0 | 0.0 | 72.9 | 0.0 | 713.9 | −124.8 | −232.8 |
| 2030 | 2,668.0 | 957.6 | 187.9 | 0.0 | 743.9 | +778.7 | +545.9 |
| 2031 | 2,986.1 | 1,017.6 | 212.5 | 304.0 | 775.1 | +676.8 | +1,222.7 |
| 2032 | 3,306.9 | 1,081.4 | 235.3 | 316.8 | 807.7 | +865.8 | +2,088.6 |
| 2033 | 5,001.9 | 2,198.7 | 342.7 | 330.1 | 841.6 | +1,288.8 | +3,377.4 |
| 2034 | 5,428.4 | 2,322.9 | 375.2 | 343.9 | 876.9 | +1,509.5 | +4,886.9 |
| 2035 | 7,406.7 | 2,868.4 | 538.6 | 358.4 | 913.8 | +2,727.6 | +7,614.5 |
| 2036 | 8,044.9 | 3,024.6 | 579.0 | 373.4 | 952.1 | +3,115.7 | **+10,730.2** |

Shape: same early surplus, then a residual that is positive from 2030 and
**rises every year** (2031's dip aside), with the worst years again at the
end — **2036 (+$3,116B) and 2035 (+$2,728B)** together are 54% of the
cumulative **+$10.73T**. The high case is a stress bound (top of every
multiplier stacked), not a forecast.

### 2d. Timing profile (all scenarios)

- **2028–29 — pure addition on the cost side, full Title II on the revenue
  side.** MFA is only the transitional public option + uninsured
  auto-enrollment (~20–37M enrolled); displaced outlays are $0. Residuals
  are nevertheless negative in all three scenarios because Title II
  (annualized $465–714B/yr) plus premiums exceed the small early gross cost.
- **2030 — Medicare step.** Non-dual Medicare switches; displacement begins
  at the assumed 70% non-dual share of Medicare net outlays. Gross jumps
  ~4–7×; the central and high residuals turn positive here.
- **2031 — employer contributions begin** (§125(b), 8% of payroll, large
  non-offering employers only) and the ESI opt-in ramp starts.
- **2033 — duals / Medicaid expansion / CHIP / exchanges step.** Medicare
  displacement becomes full; Medicaid+CHIP displacement begins at the
  40/47/54% duals+expansion spending share; PTC displacement begins.
- **2035 — residual Medicaid switches; displacement complete.** Gross and
  displaced both jump; in central and high, gross jumps more — this is the
  single largest residual-worsening step in the window.
- **§2206(b)(4) Medicaid rate top-up runs 2028–33 only; §124 waitlist
  clearance is spread 2028–30** (60/25/15) in the model.

Full annual detail — gross components (core / dental-vision-hearing /
LTSS / admin / §2206 top-up / §124 waitlist), displaced, premiums, employer,
and Title II total **and itemized by component** — is in
`mfa_rebased_annual.csv` (27 rows).

---

## 3. Title II annualization — what is v1 and what is this lane's addition

**v1 contains no annual Title II profile.** `TITLE2` in `mfa_model.py` is a
dict of FY2028–36 window totals; the model subtracts the total once, at
window level. Consequently:

- The **window** residuals in §1 are pure v1 and reproduce exactly.
- The **annual** residuals in §2 depend on an annualization that v1 does
  not supply. The one used here (in `mfa_model_annual.py`, the extended
  copy shipped alongside this file): each component's window total is
  distributed over FY2028–36 in proportion to a **4.2%/yr nominal growth
  path — v1's own payroll-growth assumption (`EMP_GROWTH`)** — normalized
  so each component sums **exactly** to its v1 window total. All components
  are treated as in effect for the full window from FY2028.
- Sensitivity of the *shape* (not the window total) to this choice: a flat
  (equal-ninths) split instead of 4.2% growth would move at most ~±$45B/yr
  of Title II between early and late years in the central case — it does
  not change which years are worst (2035–36 dominate on the cost side in
  every plausible split), and it does not change any window total. But any
  year-specific residual quoted downstream must carry the label
  "Title II annualized at 4.2% growth — modeller's assumption, not in v1."

Annual Title II totals under this annualization ($B): low 465→646;
central 573→796; high-stress 685→952 (2028→2036). Itemized annual values
are in the CSV.

---

## 4. Timing sanity check against the bill (as documented in RESULTS_MFA_V1.md and Lane C)

| Item | Bill / documented timing | v1 model | Verdict |
|---|---|---|---|
| §201 TCJA + P.L.119-21 repeal | Sunset for years beginning **after Dec 31, 2027** → revenue from FY2028 | Title II window totals are defined over FY2028–36; nothing collected pre-2028 | **Consistent** at window level. The model has no intra-window ramp or partial first year — neither confirmed nor contradicted by RESULTS; the 4.2% annualization in §3 preserves the FY2028 start. |
| Other Title II components (§§202–210: surtax, step-up repeal, payroll 0.9%→4%, NIIT 3.8%→6.9%, excises, HSA termination) | RESULTS documents **no separate effective dates** | All treated as full-window (FY2028–36) totals | **No contradiction establishable from RESULTS**, but also **no verification**: the model implicitly assumes every component collects for all nine years. If any component's statutory start is later, its window total — an analogue/arithmetic figure, not a score — would be overstated. Flag for any future bill-text lane. (Lane C notes §206 as drafted zeroes the HSA monthly limit after Dec 31, **2023** — a retroactivity quirk in the text as read; it has no effect on the model's FY2028–36 window.) |
| Employer contributions (§125(b)) | Large non-offering employers; model documents **from 2031** | Exactly $0 in 2028–30; begins 2031 at 8% × $9.5T payroll base × 10/25/40% non-offering share | **Consistent.** |
| MFA costs begin | 2028 (transitional option) | Gross > 0 from 2028; enrollment 2028–29 = transitional option + uninsured only | **Consistent.** |
| Displacement phasing | Medicare 2030 (non-duals) / 2033 (duals, full); Medicaid+CHIP 2033 (duals+expansion) / 2035 (residual, full); exchanges/PTC end 2033 | Exactly this phasing, × compliance 0.95/0.98/1.00 | **Consistent.** Never steady-state inside the window — correctly so. |
| §2206(b)(4) top-up | 2028–33 per RESULTS | 2028–33 only | **Consistent.** |
| §124 waiting-list clearance | Lane C's bill read: HHS appropriated to clear waiting lists **within 90 days of enactment** | Model spreads the $15/35/60B clearance **60/25/15 over 2028–30** | **Timing simplification that contradicts a literal 90-day clearance.** Window total unaffected; annual gross in 2028 is understated and 2029–30 overstated relative to the literal text. Flagged, not corrected (correcting it would change v1). |
| State MOE (§2209) | First payment year **2038** | $0 in-window, all scenarios | **Consistent.** The +$3.07T "accelerated MOE" is a project amendment, not bill text, and is excluded from the residual throughout this file. |
| Premiums (§2204) | $0 below 200% FPL; capped at 8% of income | Bracket model: 33% of enrollees pay $0; payers average $800–4,600/enrollee-yr (2028$) by case/bracket, +4%/yr | Consistent as documented; §2204(b)(1)'s cost-referential premium-setting could imply materially higher receipts — v1 is deliberately conservative here (its own caveat). |

**Net timing verdict:** nothing in v1's timing contradicts the bill on
§201, employer contributions, displacement, top-up, or MOE. Two flags
stand: (i) Title II has **no annual timing in v1 at all** (remedied here by
a labelled assumption, §3) and its full-window treatment of §§202–210 is
unverified against component effective dates; (ii) the §124 waitlist
spread contradicts the literal 90-day clearance in timing only.

---

## 5. Standing caveats (carry with every number)

1. **No official score exists.** No CBO/JCT/CMS estimate of H.R.10924 was
   found (Lane C, verified searches Nov 2026). This is a modeller's
   construction throughout.
2. **TCJA + P.L.119-21 repeal ($3.2 / $3.9 / $4.6T) is an
   extension-analogue ASSUMPTION, not a JCT score** — built from CBO/JCT's
   estimate that *extending* the expiring TCJA provisions would add ~$4.6T
   to deficits over 10 years including ~$0.6–0.8T of interest. It is the
   largest Title II component and carries a $1.4T range across scenarios.
   Unmodelled interaction: repealing P.L.119-21 would also restore that
   law's health-spending cuts, raising the Medicaid baseline and hence
   displaced amounts in 2033–35.
3. **LTSS is the widest swing in the build** — the HCBS Part B entitlement
   (≥1 ADL) totals $0.78 / $2.00 / $5.12T across scenarios, a $4.3T spread,
   and is the least-anchored component (MFA's ≥1-ADL threshold has no
   current-programme counterpart; MACPAC CY2021 HCBS users were 2.6% of
   Medicaid enrollees at >$32k/user under narrower waiver eligibility).
4. **The high-stress case is a bound, not a forecast** — it stacks the top
   of every multiplier and growth range (2036 gross $8.04T).
5. No dynamic/behavioural scoring of Title II; no discounting; no interest
   feedback from MFA-driven deficits/surpluses (that belongs to the
   consolidated layer of the combined study, as does the fee itself —
   **nothing in this file nets the Monetary Symmetry Fee**; the residual
   here is the amount the fee + interest savings would need to cover).
6. Premiums are a simplified income-bracket model; employer contributions
   exclude §125(c) opt-out contributions (conservative); states' saved
   Medicaid share and federal uncompensated-care savings are not counted
   as offsets (conservative).

### Sensitivity — key rows from v1 (one-at-a-time on the central case)

| Change from central | Δ residual ($T) |
|---|---:|
| LTSS parameters → high (8% users × $48k) | **+2.34** |
| LTSS parameters → low (3% × $28k) | −1.10 |
| Induced demand 7% → 15% / → 0% | +1.63 / −1.42 |
| Title II → low range / → high range | +1.15 / −1.20 |
| Per-capita growth 4.8% → 5.8% / → 4.0% | +1.35 / −1.03 |
| ESI opt-in ramp → high / → zero | +0.88 / −1.12 |
| Employer non-offering share 25% → 40% / → 10% | −0.76 / +0.76 |
| §2206 rate factor 1.06 → 1.10 | +0.82 |

Dominant drivers, in order: **(1) LTSS** (take-up × unit cost);
**(2) the per-capita cost stack** (induced demand, growth, rate and
cost-sharing factors compounding over ~992M central enrollee-years);
**(3) the Title II take**, above all the TCJA-repeal analogue.

---

## 6. Files in this directory

- `mfa_rebased_annual.csv` — 27 rows (3 scenarios × FY2028–36): scenario,
  year, gross and its six components, displaced, premiums, employer,
  Title II total and its six components, residual (all $B). Scenario
  "high_stress" is v1's "high".
- `mfa_model.py` — **verbatim copy** of the v1 model (reproduction source;
  the original in `~/workspace/monetary-symmetry/mfa/` is untouched).
- `mfa_model_annual.py` — the extended model used for the annual file:
  imports the verbatim v1 copy and adds only the Title II annualization
  documented in §3. `python3 mfa_model_annual.py` regenerates the CSV and
  prints the window-sum verification.
- `MFA_REBASE.md` — this file.
