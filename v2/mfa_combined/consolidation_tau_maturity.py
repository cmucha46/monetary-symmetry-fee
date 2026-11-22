"""
Lane 4 -- Maturity-dependent transmission correction (SPONSOR CORRECTION #2).

SUPERSEDES the scalar-tau treatment of the interest-savings line used in
v2 and in Lane 3. Everything else in Lane 3 is kept identical (net
receipts $4,050B after the 1.1098 fee-path ratio, FRB/US Regime C drag
-$2,667B as its own line, delta remittances +$410B, 13% haircut ASSUMED),
so the correction is isolated and attributable.

Design premise (sponsor, evidence-supported): the 3-month bill rate and
IORB are arbitrage-locked -- bills and reserves are near-perfect
substitutes for the marginal holder. A scalar tau applied to ALL
new-issue yields is therefore wrong at the front end.

Two segments, using the maturity structure already in the project
(cohort/data.py TREASURY: WAM 70 months; share_maturing_1yr = 0.33):

(a) FRONT END -- weight W_FRONT = 0.33 of the repricing exposure (bills
    plus the share of the stock repricing within <=1 year). Transmission
    is 1 BY ARBITRAGE, not by assumption. The front-end new-issue yield
    is modeled as IORB + spread; the spread term is the CHANGE in the
    bill-IORB spread relative to baseline, a documented scenario
    parameter in {-0.25, 0, +0.15} pp (observed range: ~-0.40pp in the
    2021 scarcity to ~+0.15-0.25pp in the 2026 issuance surge). Headline
    at spread change = 0. Hence, with A_t the administered-path decline
    (IORB_base - IORB_ms; 1.95pp from FY2030, zero before):
        dy_front_t = -A_t + dspread   (dspread applied from FY2030,
                                       when the administered paths
                                       diverge; zero before, as A_t is)
(b) BEYOND 1 YEAR -- weight 1 - W_FRONT = 0.67. The existing surface
    {0, 0.25, 0.5, 0.75} applies ONLY to this segment and is RELABELED
    everywhere in Lane 4 outputs as tau_long, the LONG-SEGMENT
    transmission (expectations / term-premium channel) -- never as a
    whole-curve tau:
        dy_long_t = -tau_long * A_t

Mechanics: Lane 3's bucket-repricing recursion (savings_on_path) is
linear in the dy path for a fixed debt path and linear in the debt
stock, so segment savings are computed by running the identical
recursion on each segment's share of the stock with its own dy path;
front + long = total exactly, with no interaction term. The combined
fixed point (savings <-> combined debt path) is iterated exactly as in
Lane 3 (tolerance $0.05B, max 100 iterations).

The CBO rule-of-thumb figure is used ONLY inside cbo_corrected() as an
exhibit comparator -- never as a plug-in anywhere in the coverage
machinery (guard test mirrors Lane 3's).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import consolidation_combined as CC  # noqa: E402  (Lane 3, unmodified)

YEARS = CC.YEARS
TAU_LONGS = CC.TAUS                     # relabeled: long-segment transmission
SPREADS = (-0.25, 0.0, 0.15)            # pp change in bill-IORB spread
PUBLIC_SHARE = CC.PUBLIC_SHARE
MARKETABLE_2026 = CC.MARKETABLE_2026
BASE_RATE = CC.BASE_RATE


def _front_weight() -> float:
    shares, _ = CC._bucket_shares_maturities()
    from data import TREASURY
    return float(TREASURY["share_maturing_1yr"])


W_FRONT = _front_weight()               # 0.33
W_LONG = 1.0 - W_FRONT                  # 0.67


# ---------------------------------------------------------------------------
# Segment dy paths
# ---------------------------------------------------------------------------
def administered_decline(skeleton=None) -> dict[int, float]:
    """A_t = IORB_base - IORB_ms from the fiscal skeleton (decimal).
    0 before FY2030; 0.0195 (1.95pp) from FY2030 at the synchronized pair."""
    import consolidation as C
    skeleton = skeleton if skeleton is not None else C.load_fiscal_skeleton()
    return {t: float(skeleton.loc[t, "iorb_base"] - skeleton.loc[t, "iorb_ms"])
            for t in YEARS}


def dy_front(dspread_pp: float = 0.0, skeleton=None) -> dict[int, float]:
    """Front-end dy: full administered decline (transmission = 1 by
    arbitrage) plus the bill-IORB spread change (pp -> decimal), the
    spread change carried on the synchronized path (from FY2030)."""
    A = administered_decline(skeleton)
    ds = dspread_pp / 100.0
    return {t: -A[t] + (ds if A[t] > 0 else 0.0) for t in YEARS}


def dy_long_segment(tau_long: float, skeleton=None) -> dict[int, float]:
    """Long-segment dy: tau_long (long-segment transmission) x decline."""
    A = administered_decline(skeleton)
    return {t: -tau_long * A[t] for t in YEARS}


# ---------------------------------------------------------------------------
# Segment savings on an arbitrary debt path (rate effect only, as Lane 3)
# ---------------------------------------------------------------------------
def segment_savings_on_path(avg_debt_by_year: dict[int, float],
                            tau_long: float, dspread_pp: float = 0.0,
                            skeleton=None) -> tuple[pd.Series, pd.Series]:
    """(front, long) consolidated savings ($B). Each segment runs Lane 3's
    identical bucket recursion on its share of the debt stock."""
    front = CC.savings_on_path(avg_debt_by_year,
                               dy_front(dspread_pp, skeleton)) * W_FRONT
    long_ = CC.savings_on_path(avg_debt_by_year,
                               dy_long_segment(tau_long, skeleton)) * W_LONG
    front.name, long_.name = "front_savings_bn", "long_savings_bn"
    return front, long_


def corrected_savings_on_path(avg_debt_by_year, tau_long, dspread_pp=0.0,
                              skeleton=None) -> pd.Series:
    f, l = segment_savings_on_path(avg_debt_by_year, tau_long, dspread_pp,
                                   skeleton)
    return (f + l).rename("savings_bn")


# ---------------------------------------------------------------------------
# Combined fixed point on the growing path (Lane 3 iteration, corrected dy)
# ---------------------------------------------------------------------------
def combined_growing_corrected(tau_long: float, dspread_pp: float,
                               residual: pd.Series, fees: pd.DataFrame,
                               base_path: pd.DataFrame,
                               tol: float = 0.05, max_iter: int = 100) -> dict:
    base_debt = {t: float(base_path.loc[t, "baseline_marketable_debt_bn"])
                 for t in YEARS}
    net_flow = {t: float(fees.loc[t, "net_receipts_bn"]
                         + fees.loc[t, "frbus_drag_bn"]
                         + fees.loc[t, "delta_remittances_bn"]
                         - residual.get(t, 0.0)) for t in YEARS}
    avg_base, prev = {}, MARKETABLE_2026
    for t in YEARS:
        avg_base[t] = (prev + base_debt[t]) / 2
        prev = base_debt[t]
    front, long_ = segment_savings_on_path(avg_base, tau_long, dspread_pp)
    savings = front + long_
    iters = 0
    for iters in range(1, max_iter + 1):
        cum_net, cum_sav, D_path = 0.0, 0.0, {}
        for t in YEARS:
            cum_net += net_flow[t]
            cum_sav += float(savings[t])
            D_path[t] = base_debt[t] - cum_net - cum_sav
        avg, prev = {}, MARKETABLE_2026
        for t in YEARS:
            avg[t] = (prev + D_path[t]) / 2
            prev = D_path[t]
        f2, l2 = segment_savings_on_path(avg, tau_long, dspread_pp)
        new = f2 + l2
        delta = float((new - savings).abs().max())
        front, long_, savings = f2, l2, new
        if delta < tol:
            break
    cum_net, cum_sav, D_path = 0.0, 0.0, {}
    for t in YEARS:
        cum_net += net_flow[t]
        cum_sav += float(savings[t])
        D_path[t] = base_debt[t] - cum_net - cum_sav
    return {"savings": savings, "front": front, "long": long_,
            "debt_path": pd.Series(D_path), "iterations": iters,
            "avg_debt": avg}


def coverage_table_corrected(tau_long: float, dspread_pp: float, scen: str,
                             ctx: dict) -> pd.DataFrame:
    fees, residual = ctx["fees"], ctx["residuals"][scen]
    res = combined_growing_corrected(tau_long, dspread_pp, residual, fees,
                                     ctx["base_path"])
    df = fees.copy()
    df["front_savings_bn"] = res["front"]
    df["long_savings_bn"] = res["long"]
    df["interest_savings_bn"] = res["savings"]
    df["fee_contribution_bn"] = (df["net_receipts_bn"] + df["frbus_drag_bn"]
                                 + df["delta_remittances_bn"]
                                 + df["interest_savings_bn"])
    df["mfa_residual_bn"] = residual
    df["annual_margin_bn"] = df["fee_contribution_bn"] - df["mfa_residual_bn"]
    df["cum_contribution_bn"] = df["fee_contribution_bn"].cumsum()
    df["cum_residual_bn"] = df["mfa_residual_bn"].cumsum()
    df["cum_margin_bn"] = df["cum_contribution_bn"] - df["cum_residual_bn"]
    df["combined_debt_bn"] = res["debt_path"]
    df["baseline_debt_bn"] = ctx["base_path"]["baseline_marketable_debt_bn"]
    df.attrs["iterations"] = res["iterations"]
    return df


# ---------------------------------------------------------------------------
# V2 restatement: corrected savings on the FLAT (banked) $31,830B path
# ---------------------------------------------------------------------------
def flat_corrected_savings(tau_long: float, dspread_pp: float = 0.0) -> tuple[pd.Series, pd.Series]:
    """(front, long) consolidated savings on v2's flat stock, using v2's
    own treasury_savings_by_year machinery with segment dy paths."""
    import consolidation as C
    front = (C.treasury_savings_by_year(dy_front(dspread_pp))
             * PUBLIC_SHARE * W_FRONT)
    long_ = (C.treasury_savings_by_year(dy_long_segment(tau_long))
             * PUBLIC_SHARE * W_LONG)
    return front.reindex(YEARS), long_.reindex(YEARS)


def v2_restatement(ctx: dict) -> list[dict]:
    fees = ctx["fees"]
    base_flows = float((fees["net_receipts_bn"] + fees["frbus_drag_bn"]
                        + fees["delta_remittances_bn"]).sum())
    rows = []
    for tau_long in TAU_LONGS:
        f, l = flat_corrected_savings(tau_long, 0.0)
        corr_sav = float(f.sum() + l.sum())
        scalar_sav = float(ctx["savings_flat"][tau_long].sum())
        rows.append({
            "tau_long": tau_long,
            "v2_scalar_interest_bn": scalar_sav,
            "corrected_front_bn": float(f.sum()),
            "corrected_long_bn": float(l.sum()),
            "corrected_interest_bn": corr_sav,
            "interest_delta_bn": corr_sav - scalar_sav,
            "v2_total_scalar_bn": base_flows + scalar_sav,
            "v2_total_corrected_bn": base_flows + corr_sav,
        })
    return rows


# ---------------------------------------------------------------------------
# CBO gap update (exhibit only -- the comparator never enters coverage)
# ---------------------------------------------------------------------------
def cbo_corrected(ctx: dict) -> dict:
    """Corrected per-0.1pp figure on the growing path, NO MFA, no plan
    feedback (baseline-path balances), at tau_long=0.5, spread 0 --
    comparable to Lane 3's wedge decomposition. Lane 3's denominator
    convention is kept: per 0.1pp of the headline decline at the
    tau=0.5 cell (0.975pp), so the maturity correction and the growth
    effect are measured on the same scale Lane 3 used."""
    cbo_per01 = 379.0
    base_path = ctx["base_path"]
    avg_base, prev = {}, MARKETABLE_2026
    for t in YEARS:
        avg_base[t] = (prev + float(base_path.loc[t, "baseline_marketable_debt_bn"])) / 2
        prev = float(base_path.loc[t, "baseline_marketable_debt_bn"])
    front, long_ = segment_savings_on_path(avg_base, 0.5, 0.0)
    total = float(front.sum() + long_.sum())
    headline_pp = 0.975  # Lane 3 headline decline at tau=0.5 (pp)
    per01 = total / (headline_pp * 10)
    scalar = CC.cbo_exhibit(ctx)
    flat_per01 = scalar["model_per_01pp_consol_bn"]
    return {
        "cbo_per_01pp_bn": cbo_per01,
        "corrected_growing_noplan_total_bn": total,
        "corrected_front_bn": float(front.sum()),
        "corrected_long_bn": float(long_.sum()),
        "corrected_per_01pp_bn": per01,
        "lane3_flat_scalar_per_01pp_bn": flat_per01,
        "lane3_growing_scalar_per_01pp_bn": scalar["growing_per_01pp_bn"],
        "gap_bn": cbo_per01 - flat_per01,
        "gap_closed_total_share": (per01 - flat_per01) / (cbo_per01 - flat_per01),
        "gap_closed_by_growth_share_lane3": scalar["gap_closed_by_growth_share"],
        "effective_weighted_decline_pp_tauL05": (W_FRONT * 1.95
                                                 + W_LONG * headline_pp),
    }


def build_context_corrected() -> dict:
    return CC.build_context()


if __name__ == "__main__":
    ctx = build_context_corrected()
    print("A_t:", {t: round(v, 4) for t, v in administered_decline().items()})
    print("W_FRONT:", W_FRONT)
    for r in v2_restatement(ctx):
        print({k: (round(v, 1) if isinstance(v, float) else v)
               for k, v in r.items()})
    print("CBO:", {k: round(v, 3) for k, v in cbo_corrected(ctx).items()})
