"""
Monetary Symmetry Fee v2 -- loan-cohort phase-in model.

Grandfathering rule (memo sec. II.D, tasking): loans outstanding before the
effective date are NEVER covered. Only originations on/after the effective
date enter the covered stock. The covered share of any category therefore
phases in at the speed at which the pre-enactment stock exits and is
replaced -- the category's turnover (exit) rate delta.

Mechanics, per category i and fiscal year t (annual steps, FY ending Sep 30):
    S_i(t)  = S_i(t-1) * (1 + g_i)                      eligible stock
    exits   = delta_i * S_i(t-1)                        payoff/amort/default
    origin. = exits + g_i * S_i(t-1)                    all post-effective-date
                                                        originations are covered
    C_i(t)  = C_i(t-1) * (1 - delta_i) + originations   covered stock
    G_i(t)  = S_i(t) - C_i(t)                           grandfathered stock,
                                                        decays geometrically
Collections use the within-year average covered stock: f * (C(t-1)+C(t))/2.

Two fixed-rate fee designs (memo sec. II.D):
  design="floating"  -- every covered loan bears the CURRENT fee rate f_t
                        (the fee floats with IORB after synchronization;
                        transmission reaches fixed-rate cohorts through the
                        lender's fee obligation repricing).
  design="locked"    -- each vintage bears the fee rate in effect in its
                        origination year, for life (lender absorbs later
                        changes; borrower contract untouched). Implemented
                        with an explicit vintage matrix per category.

Turnover sensitivity: delta_case in {"low","central","high"} scales every
category to its documented delta range (data.py). Nothing in this module is
calibrated toward any revenue total; outputs are whatever the published
stocks and turnover parameters imply.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from data import ASSUMPTIONS, CATEGORIES

FY_START, FY_END = 2027, 2036


def default_fee_path() -> dict[int, float]:
    """Illustrative fee-rate path (scenario input, NOT a forecast).

    FY2027: pre-effective, 0. FY2028: statutory initial rate 0.15%.
    FY2029: transition year 2, ASSUMED blend 1.00%. FY2030+: synchronized,
    f = IORB_MS = half the flat 3.90% baseline IORB = 1.95%.
    """
    a = ASSUMPTIONS
    path = {2027: 0.0, 2028: a["initial_fee_rate"], 2029: a["fee_fy2029_transition"]}
    for fy in range(2030, FY_END + 1):
        path[fy] = a["iorb_baseline_flat"] / 2.0
    return path


def _delta(cat: dict, case: str) -> float:
    return {"low": cat["delta_low"], "central": cat["delta"],
            "high": cat["delta_high"]}[case]


def run_category(stock0: float, delta: float, growth: float,
                 fee_path: dict[int, float], design: str = "floating",
                 years=range(FY_START, FY_END + 1)) -> pd.DataFrame:
    """Simulate one category. Returns per-FY eligible/covered/grandfathered
    stocks (year-end, $B), covered share, and gross collections ($B)."""
    years = list(years)
    eff_idx = years.index(ASSUMPTIONS["first_collection_fy"])
    S_prev, C_prev = stock0, 0.0
    # Vintage matrix for the locked design: vintage year -> balance.
    vintages: dict[int, float] = {}
    rows = []
    for t in years:
        f = fee_path[t]
        if t < ASSUMPTIONS["first_collection_fy"]:
            S, C = S_prev * (1 + growth), 0.0
            collections, avg_cov = 0.0, 0.0
        else:
            exits = delta * S_prev
            originations = exits + growth * S_prev
            S = S_prev * (1 + growth)
            C = C_prev * (1 - delta) + originations
            avg_cov = 0.5 * (C_prev + C)
            if design == "floating":
                collections = f * avg_cov
            elif design == "locked":
                # Decay existing vintages, add this year's vintage at rate f,
                # collect each vintage at its locked rate on average balance.
                collections = 0.0
                new_vintages: dict[int, float] = {}
                for vy, bal in vintages.items():
                    avg_bal = 0.5 * (bal + bal * (1 - delta))
                    collections += fee_path[vy] * avg_bal
                    new_vintages[vy] = bal * (1 - delta)
                # New vintage exists only for the part of the year after
                # origination; approximate with half-year average balance.
                collections += f * 0.5 * originations
                new_vintages[t] = originations
                vintages = new_vintages
                # Invariant check: vintage balances must sum to C.
                assert abs(sum(vintages.values()) - C) < 1e-6 * max(C, 1.0)
            else:
                raise ValueError(f"unknown design {design!r}")
        rows.append({
            "fy": t, "eligible_stock_bn": S, "covered_stock_bn": C,
            "grandfathered_stock_bn": S - C,
            "covered_share": (C / S) if S > 0 else 0.0,
            "fee_rate": f, "collections_bn": collections,
        })
        S_prev, C_prev = S, C
    return pd.DataFrame(rows)


def run_model(fee_path: dict[int, float] | None = None,
              design: str = "floating", delta_case: str = "central") -> pd.DataFrame:
    """Run all categories; return long-format DataFrame with a TOTAL block
    (category='TOTAL')."""
    fee_path = fee_path or default_fee_path()
    frames = []
    for key, cat in CATEGORIES.items():
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


def summary_table(df: pd.DataFrame) -> pd.DataFrame:
    """Wide table of the TOTAL block: the headline phase-in path."""
    tot = df[df["category"] == "TOTAL"].set_index("fy")
    return tot[["eligible_stock_bn", "covered_stock_bn", "grandfathered_stock_bn",
                "covered_share", "fee_rate", "collections_bn"]]


if __name__ == "__main__":
    pd.set_option("display.width", 120)
    for design in ("floating", "locked"):
        df = run_model(design=design)
        st = summary_table(df)
        print(f"\n=== design={design}, central turnover ===")
        print(st.round(3).to_string())
        print(f"cumulative collections FY2028-36: "
              f"${st['collections_bn'].sum():,.0f}B")
