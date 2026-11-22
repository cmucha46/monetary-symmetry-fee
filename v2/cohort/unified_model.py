"""
Monetary Symmetry Fee v2 -- UNIFIED BASE (Base B) cohort runs.

The unified base is the headline base per the sponsor's 2026-11-22
decision: Base A loans (data.py) PLUS issuer-assessed corporate debt
securities and municipal bonds (unified_data.py), grandfathered
identically -- only obligations issued/originated on or after the
2027-10-01 effective date are covered.

This module reuses cohort_model.run_category unchanged (same engine,
same fee path, same two designs, same three turnover cases). It does not
modify Base A code or outputs. No behavioral response is modeled here:
accounting phase-in only (see BASE_B.md).
"""

from __future__ import annotations

import pandas as pd

from cohort_model import _delta, run_category, run_model, summary_table
from data import CATEGORIES
from unified_data import BOND_CATEGORIES, UNIFIED_CATEGORIES


def run_unified_model(fee_path=None, design: str = "floating",
                      delta_case: str = "central") -> pd.DataFrame:
    """Run all unified-base categories; long-format DataFrame with a
    TOTAL block (category='TOTAL'), same schema as cohort_model.run_model."""
    from cohort_model import default_fee_path
    fee_path = fee_path or default_fee_path()
    frames = []
    for key, cat in UNIFIED_CATEGORIES.items():
        df = run_category(cat["stock_bn"], _delta(cat, delta_case),
                          cat["growth"], fee_path, design)
        df.insert(0, "category", key)
        frames.append(df)
    long = pd.concat(frames, ignore_index=True)
    total = (long.groupby("fy")
             .agg(eligible_stock_bn=("eligible_stock_bn", "sum"),
                  covered_stock_bn=("covered_stock_bn", "sum"),
                  grandfathered_stock_bn=("grandfathered_stock_bn", "sum"),
                  collections_bn=("collections_bn", "sum"),
                  fee_rate=("fee_rate", "first"))
             .reset_index())
    total["covered_share"] = total["covered_stock_bn"] / total["eligible_stock_bn"]
    total.insert(0, "category", "TOTAL")
    return pd.concat([long, total], ignore_index=True)


def comparison_table(fee_path=None, design: str = "floating",
                       delta_case: str = "central") -> pd.DataFrame:
    """Side-by-side per-FY comparison: loans-only (Base A, sensitivity)
    vs. unified base (Base B, headline). Collections are gross, $B."""
    a = summary_table(run_model(fee_path, design=design, delta_case=delta_case))
    b = summary_table(run_unified_model(fee_path, design=design,
                                        delta_case=delta_case))
    out = pd.DataFrame({
        "loans_only_eligible_bn": a["eligible_stock_bn"],
        "loans_only_covered_bn": a["covered_stock_bn"],
        "loans_only_covered_share": a["covered_share"],
        "loans_only_collections_bn": a["collections_bn"],
        "unified_eligible_bn": b["eligible_stock_bn"],
        "unified_covered_bn": b["covered_stock_bn"],
        "unified_covered_share": b["covered_share"],
        "unified_collections_bn": b["collections_bn"],
    })
    out["bonds_increment_collections_bn"] = (out["unified_collections_bn"]
                                             - out["loans_only_collections_bn"])
    return out


def bond_phase_in(fee_path=None, delta_case: str = "central") -> pd.DataFrame:
    """Covered share by FY for the two bond categories vs. the loans-only
    total -- the phase-in lag table cited in BASE_B.md."""
    df = run_unified_model(fee_path, design="floating", delta_case=delta_case)
    piv = (df[df["category"].isin([*BOND_CATEGORIES, "TOTAL"])]
           .pivot(index="fy", columns="category", values="covered_share"))
    a = summary_table(run_model(fee_path, design="floating",
                                delta_case=delta_case))
    piv["loans_only_total"] = a["covered_share"]
    return piv.rename(columns={"TOTAL": "unified_total"})
