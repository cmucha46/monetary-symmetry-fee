"""Configuration for Monetary Symmetry Fee model v2 (Lane E).

DETERMINISTIC ONLY. No random draws anywhere in this package.

Provenance labels used throughout:
  SOURCED    -- anchored to a published figure cited in data_manifest.md
  PLACEHOLDER-- judgmental / illustrative value carried over from the prototype
                or chosen for v1; NOT estimated. Every placeholder is listed
                in README.md and RESULTS_V1.md.
"""
from dataclasses import dataclass

YEARS = list(range(2027, 2037))  # FY2027..FY2036 (Oct-Sep approximated by calendar year; see README)

# Prototype IORB_BASE (model.py L19 in the handoff prototype).
# PLACEHOLDER: described by the prototype as an approximation to the September
# 2026 SEP through 2029 with illustrative convergence thereafter. It is an
# INPUT FILE, not a forecast and not an FRB/US output.
IORB_BASE = [4.10, 3.90, 3.60, 3.40, 3.30, 3.25, 3.20, 3.20, 3.20, 3.20]  # percent

INTRO_FEE_2028_PP = 0.15      # prototype statutory introductory flat fee, pp of principal
PHASE_2029 = 0.5              # prototype half phase-in in 2029; full from 2030
NET_RECEIPTS_FACTOR = 0.87    # PLACEHOLDER: prototype prior mean; a 13% haircut for
                              # tax interactions / admin. UNESTIMATED (audit section 2, #4).
DEBT_GROWTH = 0.038           # PLACEHOLDER: prototype prior mean for nominal private-debt growth


def phase_for_year(year: int) -> float:
    """Statutory phase factor: 2027 none, 2028 intro (sentinel -1), 2029 half, 2030+ full."""
    if year == 2027:
        return 0.0
    if year == 2028:
        return -1.0  # introductory flat-fee year
    if year == 2029:
        return PHASE_2029
    return 1.0


@dataclass(frozen=True)
class Category:
    name: str
    start_stock: float        # $T, end-2026 stock (see data_manifest.md)
    covered_share: float      # PLACEHOLDER share of stock statutorily covered
    fixed_share: float        # PLACEHOLDER share of new cohorts that are fixed-rate
    turnover: float           # PLACEHOLDER annual origination/refinance fraction
    avg_maturity_years: float # PLACEHOLDER, documentation only in v1
    avoidance_per_fee_pp: float  # PLACEHOLDER exponential shrinkage per fee pp


# Starting stocks are Z.1-anchored and mutually exclusive (no double counting):
#   mortgage = household one-to-four-family residential mortgages only;
#   business = ALL nonfinancial business debt (its CRE/business mortgages live
#              inside this category, NOT in `mortgage`);
#   other    = residual household debt (household total - mortgages - consumer).
# See data_manifest.md for series, vintages, and the reconciliation to the
# prototype's $45.4T aggregate.
CATEGORIES = [
    Category("mortgage", start_stock=13.788, covered_share=0.90, fixed_share=0.92,
             turnover=0.18, avg_maturity_years=27.0, avoidance_per_fee_pp=0.050),
    Category("consumer", start_stock=5.099, covered_share=0.85, fixed_share=0.30,
             turnover=0.45, avg_maturity_years=4.0, avoidance_per_fee_pp=0.090),
    Category("business", start_stock=23.292, covered_share=0.70, fixed_share=0.45,
             turnover=0.25, avg_maturity_years=7.0, avoidance_per_fee_pp=0.080),
    Category("other", start_stock=2.045, covered_share=0.60, fixed_share=0.60,
             turnover=0.30, avg_maturity_years=10.0, avoidance_per_fee_pp=0.065),
]
TOTAL_START_STOCK = sum(c.start_stock for c in CATEGORIES)  # 44.224 $T
