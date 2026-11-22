"""
Monetary Symmetry Fee v2 -- UNIFIED BASE (Base B) category data.

Sponsor decision, 2026-11-22: bonds are included in the fee base and
grandfathered identically to loans. The unified base is therefore the
HEADLINE base; the loans-only base in data.py (Base A) is retained as the
comparison / sensitivity. data.py is NOT modified: the categories below
are added in a separate dict and merged only by unified_model.py.

Organizing principle (see BASE_B.md): the fee attaches to the ULTIMATE
BORROWER'S OBLIGATION -- loan or bond, whoever holds it -- and coverage
follows the obligation through sale or securitization. Every non-Treasury
borrower obligation is covered exactly once. Issuer-assessed categories
(the two below) are paid by the borrowing sector, not the lender sector.

All values documented in BASE_B.md with series, vintage, and anchors.
Units and conventions match data.py: stocks in USD billions, rates decimal.
"""

from data import CATEGORIES

BOND_CATEGORIES = {
    "biz_bonds": {
        "label": "Nonfinancial business debt securities (corporate bonds, "
                 "issuer-assessed)",
        # The exact bucket Base A excluded (data.py EXCLUDED), so that
        # unified eligible stock = Base A eligible + this + munis, with no
        # residual. Composition, Q4 2025 (Z.1 rel. 2026-03-19 vintage):
        # corporate bonds FL103163005 7,924.1 + corporate-issued municipal
        # securities FL103162000 651.7 + nonfinancial CP (residual ~215)
        # + noncorporate business debt securities ~530.6. The sponsor's
        # "~$9.3T of corporate bonds" verifies as TOTAL nonfinancial
        # business debt securities; bonds-only (FL103163005) is 7,924.1
        # in this vintage (revised to 8,075.3 in the Sep 2026 release).
        "stock_bn": 9321.4,
        # delta anchors (BASE_B.md): average maturity at issuance ~10-11
        # yrs (SIFMA) implies straight-line exit ~0.09-0.10; flow identity
        # (gross nonfinancial issuance ~15% of stock less ~3.5% net
        # growth) implies ~0.11; calls/tenders add in refunding years.
        "delta": 0.11, "delta_low": 0.08, "delta_high": 0.14,
        "growth": 0.035,  # FL103163005 grew ~3.7%/yr 2023-25 (FRED annual)
        "fixed_share": 0.95,  # ASSUMED: floating-rate notes a small share
        "payer": "issuer (nonfinancial business sector)",
        "source": "Fed Z.1 L.102/L.103/L.104 (FL144122005 = FL104122005 + "
                  "FL114122005), Q4 2025, release 2026-03-19 vintage; "
                  "cross-check FL103163005 Q2 2026 ~$9.2T total corporate "
                  "debt securities per Z.1 Recent Developments 2026-09-11",
    },
    "gov_muni_bonds": {
        "label": "State and local government securities (municipal bonds, "
                 "issuer-assessed)",
        "stock_bn": 3519.6,  # FL213162005, Q4 2025 (Z.1 L.212, rel. 2026-03-19)
        # delta anchors (BASE_B.md): serial amortization retires principal
        # continuously; flow identity (gross issuance ~14% of stock less
        # ~4.7% net growth, SIFMA/Z.1 2025-26) implies ~0.09; standard
        # 10-yr par calls add refunding exits when rates fall. No agency
        # publishes a stock-exit rate: ASSUMED within the anchored range.
        "delta": 0.09, "delta_low": 0.07, "delta_high": 0.12,
        "growth": 0.030,  # FL213162005 +4.7% Q4'24-Q4'25; longer-run ~2-3%
        "fixed_share": 0.95,  # ASSUMED: VRDOs/short-term notes a small share
        "payer": "issuer (state and local government sector)",
        "source": "Fed Z.1 L.212 / L.107 (FL213162005), Q4 2025, release "
                  "2026-03-19 vintage (Sep 2026 vintage: 3,527.0). Total "
                  "municipal liabilities FL383162005 4,403.8 = state/local "
                  "3,519.6 + nonprofit-issued 232.5 + corporate-issued "
                  "651.7 (the last already inside biz_bonds above)",
    },
}

# The unified (headline) category set: Base A loans + the two bond
# categories. Base A categories are referenced, not copied or altered.
UNIFIED_CATEGORIES = {**CATEGORIES, **BOND_CATEGORIES}

UNIFIED_TOTAL_BN = sum(c["stock_bn"] for c in UNIFIED_CATEGORIES.values())
# = 30,873.3 (loans) + 9,321.4 (business debt securities) + 3,519.6 (munis)
# = 43,714.3
