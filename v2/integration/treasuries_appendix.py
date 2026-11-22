"""
Monetary Symmetry Fee v2 -- Appendix computation: Treasuries IN the base.

Treasuries are EXCLUDED from the headline base (the federal government's
own obligations; the sponsor has not decided otherwise). This module
shows the arithmetic of the included variant in consolidation, so the
exclusion is a documented result rather than an assumption.

Two assessment designs:

1. ISSUER-ASSESSED (the treatment the unified base applies to corporate
   and municipal bonds). The issuer of a Treasury security is the US
   Treasury. The fee is then a payment from the Treasury to the
   Treasury: gross churn of f_t x covered stock, consolidated net
   EXACTLY ZERO in every year, by identity. No table is needed beyond
   the churn series, which is reported for scale.

2. HOLDER-ASSESSED. Holders pay f_t on covered (post-effective-date)
   principal. Two offsetting consolidated flows:
   * Receipts: f_t x covered_stock_t. The share of the covered stock
     held by the Federal Reserve washes out -- the Fed's fee payments
     reduce its earnings and hence its remittances one-for-one -- so
     consolidated receipts are the non-Fed share (x PUBLIC_SHARE),
     under the ASSUMPTION that the Fed holds the same share of the
     covered stock as of the total marketable stock (14.41%).
   * Extra interest: new issues must compensate holders for the fee.
     Under the ASSUMED full gross-up (g = 1.0), the new-issue yield
     rises by g x f_t at issuance and that coupon is locked for the
     life of the issue (the cohort skeleton's bucket repricing
     mechanics, cohort/data.py TREASURY). Interest paid on the
     Fed-held share also washes through remittances, so consolidated
     extra interest is again the non-Fed share.
   In steady state (fee constant, stock fully turned over) the two
   flows are identical and the net is zero. During the transition the
   fee floats at the CURRENT f_t on all covered stock while coupons
   lock at the ISSUANCE-year fee, so the net is a pure timing residual:
   negative while the fee is rising (coupons locked below the current
   fee on early cohorts is impossible -- coupons lock at the lower
   early fee, so receipts at the later higher fee exceed the locked
   gross-up: net POSITIVE during the ramp), zero once f is constant.
   The residual is second-order against the gross flows.

NOT modelled, flagged: any effect of a holder fee on the Treasury
term premium, foreign official demand (~$9T foreign-held, ~$4T foreign
official), or the safe-asset/collateral premium. Those channels are
one-directional (they would make the net negative) and unquantified;
the appendix's "~0" is therefore a best case for inclusion, before
frictions.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
COHORT_DIR = HERE.parent / "cohort"
sys.path.insert(0, str(COHORT_DIR))
sys.path.insert(0, str(HERE))

from consolidation import (FED_SHARE, PUBLIC_SHARE, YEARS,  # noqa: E402
                           load_summary, treasury_savings_by_year)
from data import TREASURY  # noqa: E402

GROSS_UP = 1.0  # ASSUMED: new-issue yields rise by the full fee


def covered_treasury_stock() -> pd.Series:
    """Covered (post-effective-date) marketable Treasury stock by FY.
    A bucket's covered share is the cumulative fraction repriced since
    the FY2028 effective date under the skeleton's annual maturity
    fractions: share_b(t) = 1 - (1 - mat_b)^(t - 2027). Refinancing a
    covered issue keeps it covered, so the share is cumulative."""
    buckets = TREASURY["buckets_bn"]
    mat = TREASURY["bucket_annual_maturity"]
    out = {}
    for t in YEARS:
        n = max(0, t - 2027)
        out[t] = sum(bal * (1.0 - (1.0 - mat[b]) ** n)
                     for b, bal in buckets.items())
    return pd.Series(out, name="covered_treasury_stock_bn")


def fee_path() -> pd.Series:
    """The skeleton's fee path (unified floating central summary)."""
    s = load_summary("unified", "floating", "central")
    return s["fee_rate"].reindex(YEARS).fillna(0.0)


def treasuries_appendix(gross_up: float = GROSS_UP) -> pd.DataFrame:
    """Annual holder-assessed arithmetic + the issuer-assessed identity.

    Columns ($B): covered stock; gross receipts (all holders); gross
    extra interest (bucket repricing at dy = +gross_up x f_t);
    consolidated receipts and extra interest (non-Fed share);
    consolidated net; issuer-assessed consolidated net (identically 0)
    and its gross churn.
    """
    f = fee_path()
    covered = covered_treasury_stock()
    receipts_gross = f * covered
    # Extra interest via the consolidation's own repricing machinery:
    # savings at dy = +g*f is negative; extra interest is its negation.
    savings = treasury_savings_by_year({t: gross_up * float(f[t])
                                        for t in YEARS})
    extra_gross = -savings
    df = pd.DataFrame({
        "fee_rate": f,
        "covered_stock_bn": covered,
        "receipts_gross_bn": receipts_gross,
        "extra_interest_gross_bn": extra_gross,
        "receipts_consol_bn": receipts_gross * PUBLIC_SHARE,
        "extra_interest_consol_bn": extra_gross * PUBLIC_SHARE,
    })
    df["net_consol_bn"] = (df["receipts_consol_bn"]
                           - df["extra_interest_consol_bn"])
    df["issuer_assessed_net_bn"] = 0.0          # identity, every year
    df["issuer_assessed_churn_bn"] = receipts_gross  # Treasury pays itself
    df.index.name = "fy"
    return df


if __name__ == "__main__":
    pd.set_option("display.width", 160)
    d = treasuries_appendix()
    print(d.round(1).to_string())
    print(f"\ncumulative FY27-36: receipts (consol) "
          f"${d['receipts_consol_bn'].sum():,.0f}B | extra interest (consol) "
          f"${d['extra_interest_consol_bn'].sum():,.0f}B | net "
          f"${d['net_consol_bn'].sum():,.0f}B")
    print(f"Fed share {FED_SHARE:.4f} (wash), gross-up g={GROSS_UP} ASSUMED")
