"""
Monetary Symmetry Fee v2 -- loan-cohort model data.

Every value here is documented in DATA.md (same directory) with its source,
series/table identifier, and vintage. Values marked ASSUMED are parameters
for which no published series exists; each carries a sensitivity range.

Units: stocks in USD billions. Rates as decimals (0.0195 = 1.95%).
Base-stock vintages are the latest published observations available on
2026-11-22 (Z.1 Q2 2026 / Q4 2025, G.19 Sep 2026, H.4.1 Nov 18 2026,
MSPD Sep 30 2026). They are treated as the stock at the assumed effective
date (see ASSUMPTIONS) -- the one year of drift to Oct 2027 is second-order
relative to the turnover uncertainty and is NOT added, deliberately, so the
base remains exactly traceable to published values.
"""

ASSUMPTIONS = {
    # Legislative timing assumption (stated per tasking): enactment during
    # calendar 2027; fee applies to loans ORIGINATED on or after the
    # effective date. Effective date = 2027-10-01, the first day of FY2028.
    # FY2027 therefore has zero covered stock and zero collections by
    # construction. A Jan-1-2028 effective date would shift the phase-in
    # by one quarter; the model is annual, so treat results as +/- 1 quarter.
    "enactment": "calendar 2027 (ASSUMED)",
    "effective_date": "2027-10-01 (ASSUMED; first day of FY2028)",
    "first_collection_fy": 2028,
    "initial_fee_rate": 0.0015,  # 0.15% statutory opening rate (memo sec. II.B)
    # Post-synchronization: f = IORB_MS, where IORB_MS is the IORB path under
    # the 50/50 regime. The DEFAULT scenario holds the conventional-baseline
    # IORB flat at its last observed value (3.90%, 2026-11-19) and splits it
    # 50/50, giving IORB_MS = f = 1.95% from FY2030. This is a scenario input,
    # NOT a forecast and NOT a model result.
    "iorb_baseline_flat": 0.0390,
    "sync_complete_fy": 2030,  # within the 24-month statutory deadline
    # FY2029 is the second transition year; the Board may move IORB and the
    # fee independently. The default blends halfway (ASSUMED path point).
    "fee_fy2029_transition": 0.0100,
}

# ---------------------------------------------------------------------------
# Eligible (potentially coverable) private LOAN stocks, loans only.
# Corporate bonds, commercial paper and other debt securities are EXCLUDED:
# they are securities, not loans. Government lending (federal student loans,
# SBA, FHA/VA-held) is EXCLUDED: not private loans. Coverage follows the
# loan, not the holder, so securitized / nonbank-held loans are INCLUDED.
#
# delta = annual exit rate of the outstanding stock (scheduled amortization
# + prepayment/payoff + charge-off). Each year the exiting share is replaced
# by new originations, which are covered if originated on/after the
# effective date. delta is the single most important phase-in parameter.
# ---------------------------------------------------------------------------
CATEGORIES = {
    "hh_mortgage_1_4": {
        "label": "Household 1-4 family mortgages (excl. HELOCs)",
        "stock_bn": 13517.0,  # 13,977 HH mortgages (Z.1 Q2 2026) - 460 HELOC
        "delta": 0.09, "delta_low": 0.06, "delta_high": 0.13,
        "growth": 0.030,
        "fixed_share": 0.93,
        "source": "Fed Z.1 (rel. 2026-09-11), HH 1-4 family mortgages Q2 2026 "
                  "$13,977B; HELOC $460B (FRBNY HHDC Q2 2026) carved out",
    },
    "heloc_revolving": {
        "label": "Home equity lines of credit (revolving)",
        "stock_bn": 460.0,
        "delta": 0.50, "delta_low": 0.35, "delta_high": 0.65,
        "growth": 0.060,
        "fixed_share": 0.00,
        "source": "FRBNY Household Debt & Credit Q2 2026, HELOC balances",
    },
    "cc_revolving": {
        "label": "Revolving consumer credit (predominantly credit cards)",
        "stock_bn": 1368.5,
        "delta": 0.75, "delta_low": 0.60, "delta_high": 0.90,
        "growth": 0.040,
        "fixed_share": 0.00,
        "source": "Fed G.19 (rel. 2026-11-06), revolving credit, Sep 2026",
    },
    "auto_loans": {
        "label": "Motor vehicle loans",
        "stock_bn": 1589.8,
        "delta": 0.24, "delta_low": 0.20, "delta_high": 0.28,
        "growth": 0.020,
        "fixed_share": 0.95,
        "source": "Fed G.19, motor vehicle loans, Sep 2026 (NSA quarterly detail)",
    },
    "student_private": {
        "label": "Private student loans only (federal loans excluded)",
        "stock_bn": 137.9,
        "delta": 0.10, "delta_low": 0.08, "delta_high": 0.13,
        "growth": 0.035,
        "fixed_share": 0.60,
        "source": "Enterval Analytics / MeasureOne via EducationData, Q2 2026. "
                  "G.19 total student $1,884.6B less federal ~$1,746.7B",
    },
    "consumer_other": {
        "label": "Other nonrevolving consumer credit (personal, other)",
        "stock_bn": 381.6,  # 3,856.0 nonrevolving - 1,884.6 student - 1,589.8 auto
        "delta": 0.30, "delta_low": 0.25, "delta_high": 0.35,
        "growth": 0.020,
        "fixed_share": 0.90,
        "source": "Fed G.19 Sep 2026, residual of nonrevolving credit",
    },
    "biz_loans_nonmortgage": {
        "label": "Nonfinancial business loans excl. mortgages (C&I-type + other loans & advances)",
        "stock_bn": 6215.3,  # 2,869.4 depository loans n.e.c. + 3,345.9 other loans & advances
        "delta": 0.33, "delta_low": 0.25, "delta_high": 0.40,
        "growth": 0.035,
        "fixed_share": 0.35,
        "source": "Fed Z.1 table L.102 (FL143168005 + FL143169005), Q4 2025. "
                  "Includes ~$1.1T private-credit loans (Fed F.4.4, Q2 2026: "
                  "private credit = 7.1% of $15.7T corporate debt)",
    },
    "biz_mortgages_cre_mf": {
        "label": "Nonfinancial business mortgages (CRE + multifamily + farm)",
        "stock_bn": 7203.2,
        "delta": 0.14, "delta_low": 0.11, "delta_high": 0.17,
        "growth": 0.030,
        "fixed_share": 0.55,
        "source": "Fed Z.1 table L.102 (FL143165005), Q4 2025. Cross-check: MBA "
                  "commercial/multifamily debt outstanding $5.1T Q2 2026 covers "
                  "a narrower property/investor universe -- see DATA.md",
    },
}

# Excluded stocks, recorded so the exclusion is auditable (USD bn).
EXCLUDED = {
    "federal_student_loans": {
        "stock_bn": 1746.7,  # G.19 student total 1,884.6 - private 137.9
        "reason": "Government lending, not private loans (G.19 Sep 2026 total "
                  "student loans less private share; cf. FSA portfolio $1,724.5B, "
                  "Jun 2026)",
    },
    "corporate_bonds_and_cp": {
        "stock_bn": 9321.4,  # approx.: corporate debt securities 8,790.8 (L.103) + noncorporate ~530.6, Q4 2025
        "reason": "Debt securities, not loans (Z.1 L.102/L.103, Q4 2025, approx.)",
    },
}

# ---------------------------------------------------------------------------
# Federal fiscal baseline (for fiscal.py)
# ---------------------------------------------------------------------------
TREASURY = {
    "as_of": "2026-09-30 (MSPD, FY2026 year-end)",
    "total_debt_bn": 40100.0,          # Debt to the Penny, 2026-09-30 (FiscalData API)
    "held_by_public_bn": 32420.0,      # approx., Sep 2026
    "marketable_bn": 31830.0,
    "buckets_bn": {                    # MSPD Table 1 via Senate JEC Monthly Debt
        "bills": 7120.0,               # Update (Treasury data), Sep 30 2026
        "notes": 16280.0,
        "bonds": 5550.0,
        "tips": 2140.0,                # residual (ASSUMED split of remainder)
        "frn": 740.0,                  # residual (ASSUMED split of remainder)
    },
    "wam_months": 70.0,                # Treasury/JEC, Sep 2026
    "share_maturing_1yr": 0.33,        # GAO/TBAC Q3 2026
    "share_maturing_3yr": 0.551,       # TBAC Q3 2026 presentation
    "avg_rate_marketable": 0.0357,     # JEC/Treasury, Oct 2026
    # Annual maturity (repricing) fractions per bucket, ASSUMED, chosen so the
    # year-1 portfolio repricing share reproduces the published ~33%:
    # (7120*1.0 + 740*1.0 + 16280*0.135 + 2140*0.10 + 5550*0.035) / 31830 = 0.328
    "bucket_annual_maturity": {
        "bills": 1.00, "frn": 1.00, "notes": 0.135, "tips": 0.10, "bonds": 0.035,
    },
}

FED_BASELINE = {
    "as_of": "H.4.1, week ended 2026-11-18 (release 2026-11-19)",
    "securities_held_outright_bn": 6472.9,
    "treasuries_bn": 4587.1,
    "mbs_bn": 1883.5,
    "reserve_balances_bn": 3001.8,     # Wednesday level, Nov 18 2026
    "on_rrp_bn": 317.0,
    "tga_bn": 892.3,
    "total_assets_bn": 6741.0,
    "iorb": 0.0390,                    # Board implementation note, eff. 2026-09-17
    "deferred_asset_bn": -232.5,       # remittances due to Treasury, H.4.1
                                       # Table 6, 2026-10-28 (negative = deferred
                                       # asset). MEDIUM confidence -- see DATA.md
    "portfolio_yield_assumed": 0.027,  # ASSUMED avg yield on securities portfolio
    "opex_dividends_bn": 12.0,         # ASSUMED annual operating expense + dividends
}
