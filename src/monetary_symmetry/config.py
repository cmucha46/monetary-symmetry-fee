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

# ---------------------------------------------------------------------------
# Lane F (v2): corrected covered-base variants.
#
# Interpretation adopted (brief, Statutory counterfactual): the fee falls on
# outstanding principal of newly originated covered PRIVATE LOANS; the lender
# remits. Debt securities (corporate bonds, commercial paper, municipal
# securities issued by businesses) are NOT loans and are NOT covered.
# Securitisation does NOT remove principal from the base in the central
# interpretation: the originating/servicing lender remits ONCE on the loan;
# the MBS/ABS holder is not charged again (brief: "prevent double taxation
# of the same principal"). The strict variant instead reads coverage as
# portfolio loans only and excludes securitised pools. Loans held by the
# FEDERAL GOVERNMENT as lender (e.g. Direct student loans in G.19) are not
# private credit and are excluded in both corrected variants.
#
# Stocks below are LOAN-INSTRUMENT totals by borrower bucket (mutually
# exclusive, as in v1: business mortgages sit inside `business`, NOT in
# `mortgage`; `mortgage` is household-sector mortgages only). Source for all
# corrected figures: Federal Reserve Z.1, release of March 19, 2026 (data
# through 2025-12-31) and G.19 release of November 6, 2026 (2025 annual).
# Full sourcing table: RESULTS_V2_BASE.md and data_manifest.md (v2 addendum).
#
#   mortgage stock 14.356 = household-sector mortgages, Z.1 L.217 line 7
#                           (FL153165005, $14,356.4B, 2025)
#   consumer stock  5.099 = G.19 total consumer credit owned & securitised,
#                           2025 ($5,098.8B); private-holder portion
#                           $3,520.9B (depository 2,074.2 + finance cos 713.6
#                           + credit unions 721.3 + nonprofit 11.8); the
#                           federal-government holder portion ($1,578.0B,
#                           mostly Direct student loans) is excluded via
#                           covered_share = 3520.9/5098.8 = 0.69057
#   business stock 13.419 = nonfinancial business LOANS, Z.1 L.102 line 29
#                           (FL144123005, $13,418.5B, 2025) = depository
#                           loans n.e.c. 2,869.4 + other loans & advances
#                           3,345.9 + business mortgages 7,203.2. Excluded
#                           from the v1 stock: debt securities $8,790.8B
#                           (corporate bonds 7,924.1 + CP 215.0 + munis
#                           651.7, L.102 lines 25-28) and FDI debt 316.6.
#   other stock     1.247 = ANCHORED residual: household loans total
#                           $20,702.1B (Z.1 L.214 line 12, FL154123005)
#                           - household mortgages 14,356.4 - consumer 5,098.8
#
# Strict (loans_only) covered shares additionally remove:
#   mortgage: agency- & GSE-backed mortgage pools $3,209.9B (L.217 line 37,
#             overwhelmingly household 1-4-family backed; borrower split of
#             pools not published in the retrieved table -- approximation,
#             labelled in RESULTS_V2_BASE.md)
#   business: the whole "other loans and advances" bucket $3,345.9B (holder
#             split into direct nonbank loans vs ABS/CLO and federal
#             programmes not retrieved) plus ABS issuers' mortgage assets
#             $1,099.3B (L.217 line 43, allocated to business as an
#             approximation -- CRE/multifamily dominate ABS mortgage pools)
#   consumer/other: no further removal (G.19 footnote 1: securitised pools
#             mostly remain on originator balance sheets; FRED series
#             DTCNLHDNM shows depositories' securitised consumer credit of
#             only ~$15.4B in Aug 2026 -- gap labelled in RESULTS_V2_BASE.md)
_BEHAVIOUR = {  # per-category behavioural params, identical across variants
    c.name: (c.fixed_share, c.turnover, c.avg_maturity_years, c.avoidance_per_fee_pp)
    for c in CATEGORIES
}


def _variant_category(name, stock, covered):
    fixed, turnover, maturity, avoidance = _BEHAVIOUR[name]
    return Category(name, start_stock=stock, covered_share=covered,
                    fixed_share=fixed, turnover=turnover,
                    avg_maturity_years=maturity, avoidance_per_fee_pp=avoidance)


COVERED_BASE_VARIANTS = {
    # v1 exactly (upper bound / replication): total business debt x 0.70 proxy.
    "lane_e_proxy": list(CATEGORIES),
    # CENTRAL (recommended): all private loan principal, securitised loans
    # counted once, federal-government-held consumer credit excluded.
    "loans_plus_securitized": [
        _variant_category("mortgage", 14.356, 1.0),
        _variant_category("consumer", 5.099, 0.69057),
        _variant_category("business", 13.419, 1.0),
        _variant_category("other", 1.247, 1.0),
    ],
    # LOW / strict: portfolio loans only; securitised pools and the
    # unsplittable nonbank "other loans" bucket excluded (see notes above).
    "loans_only": [
        _variant_category("mortgage", 14.356, (14356.4 - 3209.9) / 14356.4),
        _variant_category("consumer", 5.099, 0.69057),
        _variant_category("business", 13.419, (13418.5 - 3345.9 - 1099.3) / 13418.5),
        _variant_category("other", 1.247, 1.0),
    ],
}
DEFAULT_COVERED_BASE_VARIANT = "loans_plus_securitized"


def categories_for_variant(variant: str = DEFAULT_COVERED_BASE_VARIANT):
    """Category list for a covered-base variant (default: Lane F central)."""
    try:
        return COVERED_BASE_VARIANTS[variant]
    except KeyError:
        raise ValueError(
            f"unknown covered_base_variant {variant!r}; "
            f"choose from {sorted(COVERED_BASE_VARIANTS)}") from None


def eligible_base(variant: str = DEFAULT_COVERED_BASE_VARIANT) -> dict:
    """Eligible (covered) starting principal by category, $T."""
    return {c.name: c.start_stock * c.covered_share
            for c in categories_for_variant(variant)}
