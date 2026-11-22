"""
Lane 3 -- Combined-closure consolidation: Monetary Symmetry Fee v2 +
Medicare for America (H.R.10924) under a spending closure.

ALL fee savings (net receipts + reduced net interest + delta remittances,
net of the v2 final pass's FRB/US Regime C feedback) are directed to MFA.
The question: does the fee contribution cover the Lane 1 MFA residual,
year by year and cumulatively, on a GROWING CBO-baseline debt path?

Design
------
* Imports the v2 consolidation machinery (../integration/consolidation.py)
  UNMODIFIED. Fee receipts / remittances / FRB/US feedback are taken from
  consolidate(base='unified', design='floating', turnover='central',
  theta=1.0, erosion=0.10, macro_feedback='C') -- i.e. the banked v2
  FINAL central case (Regime C, 24-month sync). Net receipts therefore
  already carry: substitution erosion (E=0.10, theta=1.0), the 13%
  tax-interaction haircut (ASSUMED, unestimated -- carried from v1), the
  Lane B fee-path ratio (1.1098), and the Regime C endogenous drag
  (-$2,667B, scaled). The drag is reported as its own line, never folded
  silently into receipts.
* MFA residuals are Lane 1's verified annual paths
  (mfa_rebased_annual.csv; Title II annualized at 4.2%/yr growth,
  Lane 1's documented assumption). Residual is ZERO in FY2027 (MFA
  window is FY2028-36) and ADDS to debt when positive.
* Baseline debt: GROWING marketable-debt path built from CBO's
  February 2026 Budget & Economic Outlook (see cbo_baseline_debt_path).
  The v2 banked pass held marketable debt flat at $31,830B; the flat
  variant is retained here as a labeled sensitivity and reproduces the
  banked totals exactly ($1,793/2,262/2,731/3,201B) by construction.
* Interest savings on a debt path: the cohort skeleton's bucket
  repricing mechanics (WAM 70 months; bucket maturity fractions from
  cohort/data.py TREASURY), generalized so bucket balances scale with
  the year's debt stock. Savings in year t are the RATE effect only --
  (baseline average rate - plan average rate) x average combined debt
  in year t x PUBLIC_SHARE (0.8559, savings counted only on the
  non-Fed-held share; remittances carried separately) -- so there is no
  double count against the receipt/residual flows that move the debt
  LEVEL. dy_t = -tau x (IORB_base - IORB_ms) from the fiscal skeleton,
  exactly as in v2 (dy = 0 before FY2030; headline decline at tau=0.5
  is 0.975pp). tau is UNESTIMATED throughout; the CBO rule of thumb is
  used ONLY in the reconciliation exhibit, never as a plug-in.
* Fixed point: interest savings depend on the combined debt path and
  the path depends on cumulative savings. Iterate from the
  baseline-path savings until max |change in annual savings| < $0.05B
  (max 100 iterations; convergence actually reached in <10).

One ledger throughout; gross shown beside net.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
INTEGRATION = HERE.parent / "integration"
COHORT = HERE.parent / "cohort"
sys.path.insert(0, str(INTEGRATION))
sys.path.insert(0, str(COHORT))

import consolidation as C  # noqa: E402  (v2 machinery, unmodified)

YEARS = list(range(2027, 2037))
TAUS = C.TAUS
PUBLIC_SHARE = C.PUBLIC_SHARE
MARKETABLE_2026 = C.MARKETABLE_BN          # 31,830 (MSPD Sep 30 2026)
BASE_RATE = 0.0357                          # avg rate on marketable debt

CENTRAL_CASE = dict(base="unified", design="floating", turnover="central",
                    theta=1.0, erosion_yr5=0.10)

# ---------------------------------------------------------------------------
# Growing baseline debt path (CBO February 2026 Outlook, constructed)
# ---------------------------------------------------------------------------
# Anchors (CBO, The Budget and Economic Outlook: 2026 to 2036, Feb 2026,
# "By the Numbers" table, retrieved via cbo.gov summary):
#   * unified deficit FY2027 = $1,887B; FY2036 = $3,115B
#   * cumulative deficits FY2027-36 = $24.4T (also AAF highlights summary)
#   * debt held by public: $32,095B (end FY2026) -> $56,152B (end FY2036)
# Construction: deficits grow geometrically from the 2027 anchor at the
# rate implied by the 2036 anchor, then the whole path is rescaled so
# the FY27-36 sum equals CBO's $24,400B exactly (rescale factor 0.992;
# endpoints land within 1% of the published anchors). Marketable debt
# starts at the project's MSPD value $31,830B (end FY2026) and grows by
# each year's deficit x 0.9917 (= 31,830/32,095, the marketable share of
# debt held by public at end FY2026; nonmarketable held-by-public is
# treated as a stable residual -- a documented simplification).
CBO_DEFICIT_TOTAL_27_36 = 24400.0
CBO_DEFICIT_2027, CBO_DEFICIT_2036 = 1887.0, 3115.0
MARKETABLE_SHARE_OF_INCREMENT = MARKETABLE_2026 / 32095.0


def cbo_baseline_debt_path() -> pd.DataFrame:
    g = (CBO_DEFICIT_2036 / CBO_DEFICIT_2027) ** (1 / 9) - 1
    raw = {t: CBO_DEFICIT_2027 * (1 + g) ** (t - 2027) for t in YEARS}
    scale = CBO_DEFICIT_TOTAL_27_36 / sum(raw.values())
    deficits = {t: raw[t] * scale for t in YEARS}
    rows, debt = [], MARKETABLE_2026
    for t in YEARS:
        debt = debt + deficits[t] * MARKETABLE_SHARE_OF_INCREMENT
        rows.append({"fy": t, "baseline_deficit_bn": deficits[t],
                     "baseline_marketable_debt_bn": debt})
    return pd.DataFrame(rows).set_index("fy")


# ---------------------------------------------------------------------------
# MFA residuals (Lane 1)
# ---------------------------------------------------------------------------
def mfa_residuals() -> dict[str, pd.Series]:
    df = pd.read_csv(HERE / "mfa_rebased_annual.csv")
    out = {}
    for scen, name in [("low", "low"), ("central", "central"),
                       ("high_stress", "high_stress")]:
        s = (df[df.scenario == scen].set_index("year")["residual_bn"]
             .reindex(YEARS).fillna(0.0))
        s.index.name = "fy"
        out[name] = s
    return out


# ---------------------------------------------------------------------------
# Fee components from the banked v2 final pass (Regime C feedback)
# ---------------------------------------------------------------------------
def fee_components() -> pd.DataFrame:
    """Annual fee-side flows, tau-independent except savings (added later):
    gross collections, net receipts at skeleton path, net receipts after
    Lane B fee-path reconciliation, FRB/US Regime C drag, delta
    remittances. FY2027 is zero by construction in v2."""
    tables = C.consolidate(macro_feedback="C", **CENTRAL_CASE)
    df = tables[0.5]  # receipts/remit/drag are tau-independent
    out = pd.DataFrame({
        "gross_collections_bn": df["gross_collections_bn"],
        "net_receipts_skeleton_bn": df["net_fee_receipts_skeleton_bn"],
        "net_receipts_bn": df["net_fee_receipts_bn"],
        "frbus_drag_bn": df["frbus_feedback_bn"],
        "delta_remittances_bn": df["delta_remittances_bn"],
    }).reindex(YEARS)
    return out


def banked_savings_flat() -> dict[float, pd.Series]:
    """Interest savings on the FLAT $31,830B path = v2's own machinery
    (reproduces the banked $939B at tau=0.5 by construction)."""
    tables = C.consolidate(macro_feedback="C", **CENTRAL_CASE)
    return {tau: tables[tau]["treasury_savings_consol_bn"].reindex(YEARS)
            for tau in TAUS}


# ---------------------------------------------------------------------------
# Repricing on an arbitrary debt path (rate effect only)
# ---------------------------------------------------------------------------
def _bucket_shares_maturities():
    from data import TREASURY
    total = sum(TREASURY["buckets_bn"].values())
    shares = {b: v / total for b, v in TREASURY["buckets_bn"].items()}
    return shares, TREASURY["bucket_annual_maturity"]


def savings_on_path(avg_debt_by_year: dict[int, float],
                    dy_by_year: dict[int, float]) -> pd.Series:
    """Consolidated interest savings ($B) when bucket balances scale with
    the given average debt stock each year. Rate effect only:
    savings_t = (BASE_RATE - avg_rate_t) * avg_debt_t * PUBLIC_SHARE."""
    shares, mat = _bucket_shares_maturities()
    rates = {b: BASE_RATE for b in shares}
    out = {}
    for t in YEARS:
        debt = avg_debt_by_year[t]
        interest = 0.0
        for b, share in shares.items():
            bal = share * debt
            m = mat[b] * bal
            rates[b] = (rates[b] * (bal - m)
                        + (BASE_RATE + dy_by_year.get(t, 0.0)) * m) / bal
            interest += rates[b] * bal
        avg_rate = interest / debt if debt > 0 else BASE_RATE
        out[t] = (BASE_RATE - avg_rate) * debt * PUBLIC_SHARE
    return pd.Series(out, name="savings_bn")


def dy_paths(skeleton=None) -> dict[float, dict[int, float]]:
    skeleton = skeleton if skeleton is not None else C.load_fiscal_skeleton()
    return {tau: C.dy_path_for_tau(tau, skeleton) for tau in TAUS}


# ---------------------------------------------------------------------------
# Combined fixed point on the growing path
# ---------------------------------------------------------------------------
def combined_growing(tau: float, residual: pd.Series,
                     fees: pd.DataFrame, base_path: pd.DataFrame,
                     dys: dict[float, dict[int, float]],
                     tol: float = 0.05, max_iter: int = 100) -> dict:
    """Iterate savings <-> combined debt path to consistency.

    Combined end-of-year debt:
        D_t = Baseline_t + cumResidual_t - cumNetReceipts_t
              - cumDragImprovement... (drag enters as a flow: drag is
              negative, so -cumDrag ADDS to debt) - cumRemit_t - cumSav_t
    Flows that reduce the surplus (MFA residual, |drag|) add to debt;
    receipts, remittances and savings reduce it. Average debt in year t
    (the stock interest accrues on) = (D_{t-1} + D_t)/2, D_2026 = 31,830.
    """
    base_debt = {t: float(base_path.loc[t, "baseline_marketable_debt_bn"])
                 for t in YEARS}
    net_flow = {t: float(fees.loc[t, "net_receipts_bn"]
                         + fees.loc[t, "frbus_drag_bn"]
                         + fees.loc[t, "delta_remittances_bn"]
                         - residual.get(t, 0.0)) for t in YEARS}
    # initial guess: savings on the baseline path itself
    avg_base = {}
    prev = MARKETABLE_2026
    for t in YEARS:
        avg_base[t] = (prev + base_debt[t]) / 2
        prev = base_debt[t]
    savings = savings_on_path(avg_base, dys[tau])
    iters = 0
    for iters in range(1, max_iter + 1):
        cum_net, cum_sav, D, prev = 0.0, 0.0, {}, MARKETABLE_2026
        D_path = {}
        for t in YEARS:
            cum_net += net_flow[t]
            cum_sav += float(savings[t])
            D_path[t] = base_debt[t] - cum_net - cum_sav
        avg, prev = {}, MARKETABLE_2026
        for t in YEARS:
            avg[t] = (prev + D_path[t]) / 2
            prev = D_path[t]
        new = savings_on_path(avg, dys[tau])
        delta = float((new - savings).abs().max())
        savings = new
        if delta < tol:
            break
    cum_net, cum_sav, D_path, prev = 0.0, 0.0, {}, MARKETABLE_2026
    for t in YEARS:
        cum_net += net_flow[t]
        cum_sav += float(savings[t])
        D_path[t] = base_debt[t] - cum_net - cum_sav
    return {"savings": savings, "debt_path": pd.Series(D_path),
            "iterations": iters, "avg_debt": avg}


def combined_flat(tau: float, residual: pd.Series, fees: pd.DataFrame,
                  savings_flat: pd.Series) -> dict:
    """Flat-debt sensitivity: v2's own convention -- savings computed on
    the flat $31,830B stock regardless of flows (no feedback), so the
    fee-only totals reproduce the banked v2 FINAL numbers exactly."""
    return {"savings": savings_flat}


# ---------------------------------------------------------------------------
# Coverage assembly
# ---------------------------------------------------------------------------
def coverage_table(tau: float, scen: str, mode: str, ctx: dict) -> pd.DataFrame:
    fees, residuals = ctx["fees"], ctx["residuals"]
    residual = residuals[scen]
    if mode == "growing":
        res = combined_growing(tau, residual, fees, ctx["base_path"],
                               ctx["dys"])
        savings, debt_path, iters = res["savings"], res["debt_path"], res["iterations"]
    else:
        savings = ctx["savings_flat"][tau]
        debt_path, iters = pd.Series(dtype=float), 0
    df = fees.copy()
    df["interest_savings_bn"] = savings
    df["fee_contribution_bn"] = (df["net_receipts_bn"] + df["frbus_drag_bn"]
                                 + df["delta_remittances_bn"]
                                 + df["interest_savings_bn"])
    df["mfa_residual_bn"] = residual
    df["annual_margin_bn"] = df["fee_contribution_bn"] - df["mfa_residual_bn"]
    df["cum_contribution_bn"] = df["fee_contribution_bn"].cumsum()
    df["cum_residual_bn"] = df["mfa_residual_bn"].cumsum()
    df["cum_margin_bn"] = df["cum_contribution_bn"] - df["cum_residual_bn"]
    if mode == "growing":
        df["combined_debt_bn"] = debt_path
        df["baseline_debt_bn"] = ctx["base_path"]["baseline_marketable_debt_bn"]
    df.attrs["iterations"] = iters
    return df


def first_shortfalls(df: pd.DataFrame) -> dict:
    neg = df.index[df["cum_margin_bn"] < -1e-9]
    ann = df.index[df["annual_margin_bn"] < -1e-9]
    return {"first_cum_negative_year": (int(neg[0]) if len(neg) else None),
            "first_annual_shortfall_year": (int(ann[0]) if len(ann) else None)}


def build_context() -> dict:
    return {"fees": fee_components(), "residuals": mfa_residuals(),
            "base_path": cbo_baseline_debt_path(),
            "savings_flat": banked_savings_flat(), "dys": dy_paths()}


# ---------------------------------------------------------------------------
# Task 2 -- CBO rule-of-thumb reconciliation exhibit
# ---------------------------------------------------------------------------
def cbo_exhibit(ctx: dict) -> dict:
    """Price v2's mechanics against CBO's rule: +0.1pp on all rates each
    year -> +$379B cumulative deficits FY2027-36 (CBO, 'How Changes in
    Economic Conditions Might Affect the Federal Budget: 2026 to 2036'),
    symmetric for lower rates. The CBO figure is NEVER used as an input;
    tau stays unestimated. All wedges are computed from the model's own
    arithmetic."""
    tau = 0.5
    dy = ctx["dys"][tau]
    headline_pp = -min(dy.values()) * 100 / 1.0  # 0.975 pp (pp units)
    headline_pp = abs(dy[2030]) * 100            # dy in decimal -> pp
    flat_consol = float(ctx["savings_flat"][tau].sum())          # 939
    flat_gross = flat_consol / PUBLIC_SHARE
    per01_consol = flat_consol / (headline_pp * 10)
    per01_gross = flat_gross / (headline_pp * 10)

    # (b) repricing/timing: instant full repricing benchmark on flat debt
    instant = sum(headline_pp / 100 * MARKETABLE_2026 * PUBLIC_SHARE
                  for _ in YEARS)  # every year at full decline
    # effective average decline actually realized (savings-weighted):
    eff_pp = flat_consol / (MARKETABLE_2026 * PUBLIC_SHARE * len(YEARS)) * 100

    # (c) growing path alone: savings on the CBO baseline path, NO MFA,
    # NO plan feedback (balances = baseline averages).
    base_path = ctx["base_path"]
    avg_base, prev = {}, MARKETABLE_2026
    for t in YEARS:
        avg_base[t] = (prev + float(base_path.loc[t, "baseline_marketable_debt_bn"])) / 2
        prev = float(base_path.loc[t, "baseline_marketable_debt_bn"])
    growing_noplan = savings_on_path(avg_base, dy)
    growing_total = float(growing_noplan.sum())
    per01_growing = growing_total / (headline_pp * 10)

    # (a) Fed-held share wedge and remittance offset, at tau=0.5 flat
    remit_total = float(ctx["fees"]["delta_remittances_bn"].sum())
    return {
        "cbo_per_01pp_bn": 379.0,
        "headline_decline_pp": headline_pp,
        "model_flat_consol_total_bn": flat_consol,
        "model_flat_gross_total_bn": flat_gross,
        "model_per_01pp_consol_bn": per01_consol,
        "model_per_01pp_gross_bn": per01_gross,
        "instant_full_repricing_flat_bn": instant,
        "effective_avg_decline_pp": eff_pp,
        "repricing_realization_share": flat_consol / instant,
        "fed_share_wedge_bn": flat_gross - flat_consol,
        "delta_remittances_bn": remit_total,
        "growing_noplan_total_bn": growing_total,
        "growing_per_01pp_bn": per01_growing,
        "growing_uplift_bn": growing_total - flat_consol,
        "gap_consol_bn": 379.0 - per01_consol,
        "gap_closed_by_growth_share": ((per01_growing - per01_consol)
                                       / (379.0 - per01_consol)),
        "marketable_share_of_total_debt": MARKETABLE_2026 / 40100.0,
    }


if __name__ == "__main__":
    ctx = build_context()
    print(ctx["base_path"].round(0).to_string())
    print("\nCBO exhibit:", {k: round(v, 2) for k, v in cbo_exhibit(ctx).items()})
