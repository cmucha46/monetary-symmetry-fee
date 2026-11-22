"""
Monetary Symmetry Fee v2 -- federal fiscal skeleton.

Two accounting blocks, deliberately kept free of behavioral claims:

1. TREASURY REPRICING. Marketable debt sits in maturity buckets (MSPD,
   Sep 30 2026). Each bucket reprices (matures and is refinanced) at an
   assumed annual fraction. Given an EXOGENOUS new-issue yield shift
   (dy, in decimal, vs. the conventional baseline -- this is where a future
   transmission parameter tau would enter; it is an INPUT here, never an
   output), the module computes the path of the average rate on the stock
   and the interest-cost delta vs. baseline. No yield response is asserted.

2. FEDERAL RESERVE. Remittance accounting identity:
       earnings = portfolio_yield * securities
                  - IORB * reserve_balances - opex/dividends
   Positive earnings first rebuild the deferred asset (remittances due,
   -$232.5B at Oct 2026) before any cash remittance resumes. IORB expense
   falls mechanically if the 50/50 regime halves IORB -- but that saving
   accrues to the consolidated government only through this identity, and
   this module reports the Treasury and consolidated views separately to
   prevent the double-counting the memo (sec. III.C) warns against.

Debt stock is held flat (refinancing only) unless a deficit path is passed;
this is a repricing skeleton, not a debt projection.
"""

from __future__ import annotations

import pandas as pd

from data import FED_BASELINE, TREASURY


def treasury_repricing(years=range(2027, 2037), dy: float = 0.0,
                         base_rate: float | None = None) -> pd.DataFrame:
    """Average-rate and interest path of the marketable stock under a
    parallel new-issue yield shift dy (decimal; negative = lower yields).

    Each bucket is a single pool with legacy average rate = base_rate;
    the maturing fraction refinances at base_rate + dy. The pool average
    rate converges geometrically to base_rate + dy.
    """
    base_rate = TREASURY["avg_rate_marketable"] if base_rate is None else base_rate
    buckets = dict(TREASURY["buckets_bn"])
    mat = TREASURY["bucket_annual_maturity"]
    total = sum(buckets.values())
    rates = {b: base_rate for b in buckets}
    rows = []
    for t in years:
        repriced = 0.0
        interest = 0.0
        for b, bal in buckets.items():
            m = mat[b] * bal
            repriced += m
            rates[b] = (rates[b] * (bal - m) + (base_rate + dy) * m) / bal
            interest += rates[b] * bal
        rows.append({"fy": t, "marketable_bn": total,
                     "repriced_share": repriced / total,
                     "avg_rate": interest / total, "interest_bn": interest})
    return pd.DataFrame(rows)


def treasury_interest_delta(dy: float, years=range(2027, 2037)) -> pd.DataFrame:
    """Interest under yield shift dy minus interest at dy=0, by FY ($B).
    Negative = saving. Pure repricing arithmetic; dy is an input."""
    shifted = treasury_repricing(years, dy=dy).set_index("fy")
    base = treasury_repricing(years, dy=0.0).set_index("fy")
    out = (shifted["interest_bn"] - base["interest_bn"]).rename("interest_delta_bn")
    return out.reset_index()


def fed_remittances(iorb_path: dict[int, float],
                    reserves_bn: float | None = None,
                    securities_bn: float | None = None) -> pd.DataFrame:
    """Fed earnings / deferred-asset / cash-remittance path under an IORB
    path. Reserves and securities held flat at H.4.1 Nov 2026 levels unless
    overridden. Returns Treasury-view and consolidated-view columns."""
    fb = FED_BASELINE
    reserves = fb["reserve_balances_bn"] if reserves_bn is None else reserves_bn
    securities = fb["securities_held_outright_bn"] if securities_bn is None else securities_bn
    deferred = fb["deferred_asset_bn"]  # negative: remittances due < 0
    rows = []
    for t in sorted(iorb_path):
        income = fb["portfolio_yield_assumed"] * securities
        iorb_expense = iorb_path[t] * reserves
        earnings = income - iorb_expense - fb["opex_dividends_bn"]
        cash_remit = 0.0
        if earnings >= 0:
            # Earnings first extinguish the deferred asset.
            offset = min(earnings, -deferred) if deferred < 0 else 0.0
            deferred += offset
            cash_remit = earnings - offset
        else:
            deferred += earnings  # deferred asset grows (more negative)
        rows.append({"fy": t, "iorb": iorb_path[t],
                     "interest_income_bn": income,
                     "iorb_expense_bn": iorb_expense,
                     "net_earnings_bn": earnings,
                     "cash_remittance_bn": cash_remit,
                     "deferred_asset_bn": deferred})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pd.set_option("display.width", 120)
    print("=== Treasury repricing check (dy=0) ===")
    print(treasury_repricing().round(4).to_string(index=False))
    print("\n=== Interest delta, dy = -100bp (illustrative input only) ===")
    d = treasury_interest_delta(-0.01)
    print(d.round(1).to_string(index=False))
    print(f"cumulative FY27-36: ${d['interest_delta_bn'].sum():,.0f}B")
    base = {y: 0.0390 for y in range(2027, 2037)}
    ms = {y: (0.0390 if y < 2030 else 0.0195) for y in range(2027, 2037)}
    print("\n=== Fed remittances, baseline IORB 3.90% flat ===")
    print(fed_remittances(base).to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
    print("\n=== Fed remittances, 50/50 IORB (1.95% from FY2030) ===")
    print(fed_remittances(ms).to_string(index=False, float_format=lambda v: f"{v:,.3f}"))
