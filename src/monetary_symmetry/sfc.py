"""Consolidated Treasury / Federal Reserve SFC ledger.

Sectors: Treasury, Federal Reserve, banks, private (households+business),
rest of world is folded into 'public holders' (debt held by the public
includes foreign holders; they are outside the consolidated US government).

What v1 does, and what it deliberately does not do
---------------------------------------------------
* Federal debt stocks are EXOGENOUS and identical in baseline and scenario
  (PLACEHOLDER CBO-like path, see LedgerParams). Debt-stock feedback (fee
  receipts reducing later borrowing) is EXCLUDED in v1 -- it is listed as a
  pending refinement in RESULTS_V1.md. This makes the interest decomposition
  exact rather than residual-fudged.
* Treasury interest is computed separately on public-held and Fed-held debt.
  CONSOLIDATED net interest counts only:
      interest paid to public holders
      + IORB expense (paid by the Fed to banks -- outside consolidated govt)
      + Fed operating costs
      - Fed income on MBS/agency assets (paid by private borrowers)
  Interest on Fed-held Treasuries is an internal transfer and is EXCLUDED
  from the consolidated view; it appears in the gross (Treasury + Fed
  statements) view, where it is exactly offset by Fed asset income.
  Identity (tested): consolidated == gross_interest_all_debt - fed_net_income.
* Treasury repricing is EXPLICIT: a share `treasury_repricing_share` of the
  public-held stock reprices each year at the new-issue yield (bills reprice
  immediately; average maturity ~6 years motivates ~0.18/yr). The CBO
  $379B/0.1pp sensitivity is NOT used anywhere in this module.
* Fed asset income reprices on its own slower schedule (`fed_asset_roll`):
  existing fixed coupons do NOT reset instantly (the prototype's instant
  30%-of-$4T claw-back is removed).
* DEFERRED ASSET: when Fed net income < 0, cash remittances are 0 and the
  deferred asset grows by the shortfall; when income > 0 it first pays the
  deferred asset down, and only the remainder is remitted. This is real Fed
  practice since September 2022 (see data_manifest.md).
"""
from dataclasses import dataclass

from .config import YEARS


@dataclass(frozen=True)
class LedgerParams:
    public_debt_start: float = 31.0        # $T end-2026, PLACEHOLDER (CBO-scale)
    public_debt_growth_path: tuple = (1.7, 1.7, 1.6, 1.6, 1.5, 1.5, 1.4, 1.4, 1.3, 1.3)  # $T/yr, PLACEHOLDER
    fed_treasuries: float = 4.20           # $T, SOURCED approx: H.4.1 Oct 2025 ($4.196T)
    fed_mbs: float = 2.08                  # $T, SOURCED approx: H.4.1 Oct 2025 ($2.085T)
    reserves_start: float = 2.93           # $T, SOURCED approx: H.4.1 Oct 2025 ($2.933T)
    reserves_growth: float = 0.0           # PLACEHOLDER: reserves held constant in v1
    public_yield_start: float = 3.30       # %, PLACEHOLDER avg effective rate on public debt
    fed_treasury_yield_start: float = 2.40 # %, PLACEHOLDER book yield on Fed Treasuries
    fed_mbs_yield: float = 3.00            # %, PLACEHOLDER book yield on Fed MBS (held fixed)
    term_premium: float = 0.30             # pp, PLACEHOLDER: new-issue yield = stance + this
    treasury_repricing_share: float = 0.18 # /yr, PLACEHOLDER from ~6yr avg maturity + bills
    fed_asset_roll: float = 0.12           # /yr, PLACEHOLDER portfolio roll/repricing share
    yield_transmission: float = 0.32       # PLACEHOLDER: prototype prior mean; fraction of the
                                           # IORB drop that reaches new-issue Treasury yields
    fed_opex: float = 0.020                # $T/yr, PLACEHOLDER simplified operating costs
    deferred_asset_start: float = 0.235    # $T, SOURCED approx: Fed deferred asset early 2026
                                           # (~$230-245B; see data_manifest.md)


def settlement_flows(fee: float, treasury_spend: float) -> dict:
    """Quadruple-entry settlement of a fee collection and Treasury spend-back.

    Fee payment F: private deposits fall F, bank reserves fall F, TGA rises F.
    Treasury spend S: the exact reverse. Returns changes in sector net worth
    and in the reserve/TGA stocks. Banks and the Fed are balance-sheet neutral
    (assets and liabilities move together); the only net-worth transfer is
    private <-> Treasury. Sum of net-worth changes is identically zero, and
    a temporary reserve drain (F collected, not yet spent) is NOT income to
    anyone twice: Treasury's gain is the private sector's loss, once.
    """
    return {
        "treasury_net": fee - treasury_spend,
        "private_net": -fee + treasury_spend,
        "banks_net": 0.0,
        "fed_net": 0.0,
        "reserves_delta": -fee + treasury_spend,
        "tga_delta": fee - treasury_spend,
    }


def _run_one(iorb, new_yield, p: LedgerParams, years):
    rows = []
    public_stock = p.public_debt_start
    fed_ts = p.fed_treasuries
    reserves = p.reserves_start
    y_public = p.public_yield_start
    y_fed_ts = p.fed_treasury_yield_start
    deferred = p.deferred_asset_start
    for j, year in enumerate(years):
        stock_start = public_stock
        # Repricing: a share of the stock moves to the new-issue yield.
        y_public = (1 - p.treasury_repricing_share) * y_public + p.treasury_repricing_share * new_yield[j]
        y_fed_ts = (1 - p.fed_asset_roll) * y_fed_ts + p.fed_asset_roll * new_yield[j]
        interest_public = stock_start * y_public / 100.0
        interest_fedheld = fed_ts * y_fed_ts / 100.0
        fed_income_ts = interest_fedheld            # Fed earns what Treasury pays it
        fed_income_mbs = p.fed_mbs * p.fed_mbs_yield / 100.0
        iorb_expense = reserves * iorb[j] / 100.0
        fed_net_income = fed_income_ts + fed_income_mbs - iorb_expense - p.fed_opex
        # Deferred asset mechanics (cash remittance):
        if fed_net_income < 0:
            remittance = 0.0
            deferred += -fed_net_income
        else:
            paydown = min(deferred, fed_net_income)
            deferred -= paydown
            remittance = fed_net_income - paydown
        gross_interest = interest_public + interest_fedheld
        consolidated = interest_public + iorb_expense + p.fed_opex - fed_income_mbs
        rows.append({
            "year": year, "public_stock": stock_start, "fed_treasuries": fed_ts,
            "reserves": reserves, "y_public": y_public, "y_fed_ts": y_fed_ts,
            "new_yield": new_yield[j], "iorb": iorb[j],
            "interest_public": interest_public, "interest_fedheld": interest_fedheld,
            "fed_income_mbs": fed_income_mbs, "iorb_expense": iorb_expense,
            "fed_opex": p.fed_opex, "fed_net_income": fed_net_income,
            "remittance_cash": remittance, "deferred_asset": deferred,
            "gross_interest_all_debt": gross_interest,
            "treasury_net_interest_gross_view": gross_interest - remittance,
            "consolidated_net_interest": consolidated,
        })
        public_stock += p.public_debt_growth_path[j]
    return rows


def run_ledger_pair(baseline_iorb, scenario_iorb, params: LedgerParams = LedgerParams(),
                    years=None):
    """Run baseline and scenario ledgers; return (base_rows, scen_rows, diff_rows).

    New-issue Treasury yield in BOTH runs is benchmarked to the baseline
    stance; the scenario yield is reduced by
        yield_transmission * (baseline_iorb - scenario_iorb).
    diff_rows carry the consolidated decomposition (positive = saving):
        public_yield_effect  = base interest_public - scen interest_public
        iorb_remit_effect    = base IORB expense - scen IORB expense
                               (in the consolidated view the remittance channel
                               IS the IORB-expense channel; lost Fed income on
                               Treasuries is internal and nets out -- see module
                               docstring. The gross-view remittance change is
                               reported separately as remittance_effect_gross.)
        total                = base consolidated - scen consolidated
                               (== public_yield_effect + iorb_remit_effect exactly,
                               because stocks are identical across runs in v1)
    """
    yrs = years if years is not None else YEARS
    p = params
    base_new_yield = [r + p.term_premium for r in baseline_iorb]
    scen_new_yield = [base_new_yield[j] - p.yield_transmission * (baseline_iorb[j] - scenario_iorb[j])
                      for j in range(len(yrs))]
    base = _run_one(baseline_iorb, base_new_yield, p, yrs)
    scen = _run_one(scenario_iorb, scen_new_yield, p, yrs)
    diffs = []
    for b, sc in zip(base, scen):
        d = {
            "year": b["year"],
            "public_yield_effect": b["interest_public"] - sc["interest_public"],
            "iorb_remit_effect": b["iorb_expense"] - sc["iorb_expense"],
            "remittance_effect_gross": sc["remittance_cash"] - b["remittance_cash"],
            "gross_interest_effect": b["gross_interest_all_debt"] - sc["gross_interest_all_debt"],
        }
        d["consolidated_saving"] = b["consolidated_net_interest"] - sc["consolidated_net_interest"]
        diffs.append(d)
    return base, scen, diffs
