# CCC RUN NOTES — Business-investment channel of a full TCJA repeal (§201 sunset)

**Lane:** PSLmodels Cost-of-Capital-Calculator (CCC) only. CCC produces METRs and the
user cost of capital — **no revenue numbers are produced or implied by this lane.**

## 1. Environment / versions
- Python 3.12.3 (sandbox), venv at `~/workspace/monetary-symmetry/external_sims/ccc/venv/`
- **cost-of-capital-calculator 2.1.1** (installed from PyPI; license CC0-1.0)
- Full freeze: `pip_freeze.txt`. Key pins: pandas **2.3.3** (see §6), numpy 2.5.5,
  paramtools 0.20.0, taxcalc 6.8.5 (dependency only — never called; `call_tc=False`,
  CCC's shipped `tau_*` rates are used).
- Scripts: `run_ccc.py` (primary), `run_sensitivity.py` (transplant), `verify_asset.py`
  (year-native cross-check). Raw console output: `run_output.txt`, `verify_asset_output.txt`.

## 2. What comparison is constructible — parameter provenance
CCC ships **one** year-indexed parameter file, `ccc/default_parameters.json`
(years 2013–2035, values carry forward), plus one **static** depreciation-rules file,
`ccc/tax_depreciation_rules.json` (all entries dated 2013; no year variation).
There is no separate "2017 law" file — pre-TCJA law is obtained by evaluating the
shipped time series at **year = 2017**, and current law at **year = 2026**
(CCC's `DEFAULT_START_YEAR`). **No hand edits in the primary run.**

Shipped values at the two years (the comparison actually computed):

| Parameter | 2017 (pre-TCJA) | 2026 (current law) |
|---|---|---|
| CIT_rate / CIT_rate_ded | 0.35 | 0.21 |
| BonusDeprec 3–20yr classes | 0.50 | 1.00 (0.8 in 2023, 0.6 in 2024, restored to 1.0 in 2025 — the OBBBA full-expensing restoration, carried into 2026) |
| BonusDeprec 25 / 27.5 / 39yr | 0.0 | 0.0 |
| tau_pt (pass-through owners) | 0.3309 | 0.3101 |
| tau_div / tau_int / tau_lcg | 0.1571 / 0.3087 / 0.1802 | 0.1807 / 0.3184 / 0.1915 |
| inflation_rate | 0.017 | 0.020 |
| nominal_interest_rate | 0.068 | 0.068 |

So "current law (2026)" = TCJA corporate provisions as made permanent / restored by
OBBBA **as encoded in CCC 2.1.1's defaults** (21% rate, 100% bonus from 2025).
Caveat: CCC's `tau_*` series is a precomputed Tax-Calculator-vintage series shipped
in the JSON; whether its post-2025 values fully reflect OBBBA's individual-side
permanence cannot be verified from inside CCC — but the business-side parameters
(rate, bonus) that drive this lane do reflect it.

**Channels NOT constructible in CCC (both arms identical, delta = 0 by construction):**
- **§163(j) interest limit:** `interest_deduct_haircut_c/pt = 0.0` in all years. CCC's
  own parameter note: the 30%-of-ATI limit is *assumed non-binding for the marginal
  investment*. Repealing §163(j) therefore shows no effect here; no haircut was
  invented to force one.
- **§174 R&D amortization:** the depreciation-rules file is static — most R&D assets
  (RD* codes) are `Expensing` in both arms, so CCC cannot represent TCJA's 2022–2025
  §174 amortization. Against an **OBBBA baseline this channel is ≈0 anyway** (OBBBA
  restored domestic R&D expensing), so the omission does not bias this comparison.
- Depreciation lives/methods generally: static 2013 rules file, same in both arms;
  all depreciation differences come through the bonus-depreciation parameters above.

## 3. Method
Documented CCC default workflow, default assets/industries, no custom asset database:
`Calculator(p=Specification(year=Y), dp=DepreciationParams(), assets=Assets())`,
compared with CCC's own `summary_table` / `asset_summary_table`
(baseline = current law 2026; "reform" = pre-TCJA law 2017). Fresh Calculator
objects per table (CCC's `calc_base()` is not safely re-runnable on one object —
see §6). Averages are CCC's asset-stock-weighted aggregates (`wavg` by `assets`),
land and inventories included, financing = CCC's typical mix unless labeled.

**Known CCC quirk (disclosed, affects METR/METTR only):** `summary_table` recomputes
the reform column's METR/METTR using the *baseline* Specification's saver-return
parameters (`r_prime`, `s`, inflation). The UCC column is unaffected (UCC depends
only on ρ and δ, and matches the year-native path exactly). Two cross-checks bound
the METR effect of this quirk — see §5.

## 4. Results — CCC outputs (primary run, summary_table convention)

### METR — Marginal Effective Tax Rate (business-level, %), mix financing
| | Current law 2026 | Pre-TCJA 2017 | Δ (pp) |
|---|---|---|---|
| **Overall** | **6.95** | **15.01** | **+8.06** |
| Corporations | 3.73 | 14.50 | +10.77 |
| — equity financed | 11.70 | 24.83 | +13.13 |
| — debt financed | −25.22 | −31.21 | −5.99 |
| Pass-through entities | 25.01 | 29.28 | +4.27 |
| — equity financed | 26.76 | 30.38 | +3.62 |
| — debt financed | 16.98 | 24.52 | +7.54 |

### METTR — Marginal Effective *Total* Tax Rate (%), mix financing
| | Current law 2026 | Pre-TCJA 2017 | Δ (pp) |
|---|---|---|---|
| **Overall** | **20.51** | **27.39** | **+6.88** |
| Corporations | 17.76 | 26.96 | +9.20 |
| Pass-through entities | 25.01 | 29.28 | +4.27 |

### User Cost of Capital (%), mix financing
| | Current law 2026 | Pre-TCJA 2017 | Δ (pp) | Δ (relative) |
|---|---|---|---|---|
| **Overall** | **10.44** | **11.00** | **+0.56** | **+5.3%** |
| Corporations | 11.85 | 12.57 | +0.72 | +6.0% |
| — equity financed | 12.73 | 13.88 | +1.15 | |
| — debt financed | 10.00 | 9.82 | −0.18 | |
| Pass-through entities | 8.76 | 9.13 | +0.37 | +4.2% |

### By major asset group (mix financing; corporate / pass-through)
| Group | METR corp Δpp | METR pt Δpp | UCC corp Δpp | UCC pt Δpp |
|---|---|---|---|---|
| Equipment | −9.10 → 2.18 (**+11.28**) | −2.43 → 12.73 (**+15.16**) | 19.56 → 20.14 (+0.58) | 20.12 → 20.90 (+0.78) |
| Structures | 4.46 → 14.44 (**+9.97**) | 22.93 → 26.81 (**+3.88**) | 8.98 → 9.65 (+0.67) | 8.45 → 8.77 (+0.32) |
| Intellectual Property | −9.10 → −5.24 (**+3.86**) | −2.43 → 5.58 (**+8.01**) | 22.67 → 22.85 (+0.18) | 23.04 → 23.42 (+0.38) |
| Inventories | +12.91 | +2.77 | +1.22 | +0.30 |
| Land | +12.20 | +3.44 | +1.05 | +0.33 |

(IP METR ≈ equipment METR under current law is real, not a typo: at 100% bonus /
expensing, z ≈ 1 for both, so ρ — and hence METR — coincide; they separate in 2017
on the year-native path: IP corp −7.08% vs equipment +0.47%.)

CSVs: `summary_{metr,mettr,ucc}_current2026_vs_preTCJA2017.csv`,
`asset_summary_{metr,mettr,ucc}_current2026_vs_preTCJA2017.csv`.

## 5. Cross-checks (bounding the §3 quirk and the economics confound)
1. **Year-native `calc_by_asset`** (each law with its own shipped saver/inflation
   parameters): corporate METR 3.73% → 13.00% (**+9.27pp**); pass-through
   25.01% → 27.11% (**+2.09pp**); UCC identical to §4 to the basis point.
   (`verify_asset_output.txt`)
2. **Law-only transplant sensitivity** (`run_sensitivity.py`,
   `transplant_revision.json`): 2017 statutory values (CIT 0.35, bonus 0.50 for
   3–20yr classes, 2017 `tau_*` set) written into a 2026 Specification via
   `update_specification` in paramtools list-of-{year,value} format — **every edit
   is listed in `transplant_revision.json`**; 2026 economics (inflation 2.0%,
   interest 6.8%, saver params) held constant. Result: overall METR
   6.95% → 13.57% (**+6.62pp**), corporate +9.45pp, pass-through +2.94pp;
   overall UCC 10.44% → 10.89% (**+0.45pp, +4.3% relative**).
   (`sensitivity_summary_{metr,mettr,ucc}_transplant2017law_at2026.csv`)

All three paths agree: **repeal raises the overall METR by roughly +6.6 to +8.1pp
and the user cost of capital by roughly +0.45 to +0.56pp (+4.3% to +5.3% relative).**
The one offsetting channel: **debt-financed corporate** investment gets *cheaper*
(METR −5.99pp primary; UCC −0.18pp) because interest deductibility is worth more at
a 35% rate and CCC assumes no binding §163(j) limit — the increase is driven by
equity-financed investment.

## 6. Limitations / execution notes
- CCC is a steady-state, marginal-investment calculator: no transition path, no
  revenue, no GE/wage feedback, no §163(j) or §174 channels (see §2). It compares
  two *law regimes*, not a 2028-effective sunset timeline.
- pandas: the resolver initially installed pandas 3.1.1, under which CCC's
  `wavg()` (`warnings.filterwarnings("error")`) turns pandas' `inplace`
  deprecation into a hard error on repeated `calc_base()` calls. Pinned
  **pandas==2.3.3**; headline METR/UCC values were identical under both pandas
  versions where both ran. Side effect: pip warns taxcalc 6.8.5 declares
  pandas>=3 — immaterial here because CCC never invokes Tax-Calculator in this
  workflow (`call_tc=False`).
- CCC's aggregates are asset-stock-weighted over its default BEA asset/industry
  database; absolute METR levels (e.g. negative debt-financed corporate METR) are
  CCC-model constructs — the **deltas** are the usable output.

## 7. Interpretation — NOT CCC output (separated per instructions)
CCC says the repeal raises the overall user cost of capital by ~+4.3% to +5.3%
in relative terms. Applying the standard literature convention for the elasticity
of capital/investment with respect to the user cost, **−0.5 to −1.0** (a
convention, not a CCC estimate), the implied long-run response is on the order of
a **~2% to ~5% smaller capital stock / lower investment level** than under current
law, concentrated in equity-financed corporate investment, partly offset for
debt-financed investment. A smaller capital stock means a smaller business tax
base (and lower labor productivity/wages feeding the individual side), so any
*dynamic* revenue estimate of the repeal would collect **less** than a purely
static estimate on the business side. **Direction: the project's static $3.9T
assumption is more likely over-stated than under-stated once business-investment
behavior responds** — CCC alone cannot say by how many dollars, and no dollar
figure is claimed here.
