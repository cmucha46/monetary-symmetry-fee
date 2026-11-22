"""
Monetary Symmetry Fee v2 -- fiscal consolidation + tau-surface engine.

Consolidated net fiscal benefit vs. the conventional baseline, per fiscal
year FY2027-36, built ONLY from documented inputs:

    consolidated_net_t(tau) = net_fee_receipts_t
                            + treasury_interest_savings_t(tau)
                            + delta_fed_cash_remittances_t

Components
----------
1. NET FEE RECEIPTS. Gross collections come from the cohort lane's summary
   CSVs (designs: floating / locked; turnover: low / central / high; base:
   unified loans+bonds headline, loans-only sensitivity -- resolved via
   inputs.json, swappable by file change). Two adjustments, both labeled:
     * substitution erosion: e_t = min(0.60, E * theta * ramp_t), where E is
       the literature lane's year-5 covered-base erosion grid value
       {0, .10, .25, .40}, theta is pass-through {0.5, 0.75, 1.0, 1.15}
       (theta reaches collections ONLY through this slot -- statutory
       collections are rate x covered stock regardless of incidence), and
       ramp_t phases erosion in over the first five collection years
       (FY2028 = 0.2 ... FY2032 = 1.0). The multiplicative theta coupling
       is an ASSUMED functional form, not an estimate.
     * tax-interaction haircut h = 0.13, ASSUMED (carried from the v1
       fiscal module, where it was likewise unestimated). No published
       source exists for the income/payroll-tax offset of this fee; gross
       collections are always reported alongside net so the haircut's
       effect is transparent. Fee deductibility (LITERATURE.md sec. 2.3)
       would move this materially and is an open legislative parameter.

2. TREASURY INTEREST SAVINGS -- A TAU-CONDITIONAL SURFACE, NEVER A POINT.
   tau in {0, 0.25, 0.5, 0.75} is the transmission of the halved
   administered-rate path into new-issue yields (LITERATURE.md sec. 4.3:
   UNCALIBRATED; no published estimate exists). dy_t = -tau * (IORB_base_t
   - IORB_ms_t), applied from the first year the skeleton's IORB paths
   diverge (FY2030) through the cohort skeleton's maturity-bucket
   repricing mechanics. CONSOLIDATION (memo sec. III.C): savings are
   counted only on the non-Fed-held share of marketable debt
   (1 - 4587.1/31830 = 0.8559). Interest on Fed-held Treasuries nets to
   zero in consolidation -- Treasury pays less, the Fed earns less,
   remittances fall by the same amount -- and the skeleton's remittance
   identity holds Fed portfolio income constant, so counting the Fed-held
   share in savings as well would double-count it.

3. DELTA FED CASH REMITTANCES. Taken directly from the cohort fiscal
   skeleton (cash basis). The deferred-asset identity is respected:
   halving IORB raises Fed earnings ~$58.5B/yr, but while the deferred
   asset (-$232.5B, Oct 2026) is being extinguished the increment is NOT
   cash to Treasury. Delta cash is $0 in FY2027-29, +$8.8B in FY2030 (the
   year the MS path clears the deferred asset), then the full earnings
   delta. Deposit beta has NO mechanical entry in this identity (Fed
   earnings depend on IORB, reserves, and portfolio yield only); beta is
   carried in the Monte Carlo grid as a documented inert slot whose touch
   point is the SFC bank-funding layer in a later pass.

Known limitations of this pass (stated, not hidden):
  * Debt stock held flat (skeleton convention): no deficit-feedback loop
    (lower deficits -> less issuance -> further savings). Conservative.
  * Fed portfolio size and yield frozen at H.4.1 Nov 2026 levels: the
    remittance delta captures only the IORB-expense channel, not the
    drift of Fed reinvestment yields under a lower rate path.
  * Nonmarketable federal debt is outside the repricing skeleton.
  * FRB/US macro feedback enters through apply_macro_feedback below:
    EMPTY (NaN) unless consolidate() is called with macro_feedback set
    to a Lane B regime (final integration pass, frbus_feedback.py). The
    SFC Section IX slot remains empty by design -- Section IX is a
    one-period sign experiment, not an annual fiscal series.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
COHORT_DIR = HERE.parent / "cohort"
YEARS = list(range(2027, 2037))

# --- Grids (LITERATURE.md sec. 5; nothing here is a calibrated distribution)
TAUS = (0.0, 0.25, 0.5, 0.75)
THETAS = (0.5, 0.75, 1.0, 1.15)
BETAS = (0.45, 0.55, 0.65)          # inert in this layer -- see docstring
EROSIONS = (0.0, 0.10, 0.25, 0.40)  # year-5 covered-base erosion at theta=1
TURNOVERS = ("low", "central", "high")
DESIGNS = ("floating", "locked")

TAX_INTERACTION_HAIRCUT = 0.13  # ASSUMED, unestimated -- see docstring
EROSION_CAP = 0.60

# Fed-held share of marketable Treasury debt (cohort data.py, H.4.1/MSPD).
FED_TREASURY_BN = 4587.1
MARKETABLE_BN = 31830.0
FED_SHARE = FED_TREASURY_BN / MARKETABLE_BN          # 0.14410
PUBLIC_SHARE = 1.0 - FED_SHARE                        # 0.85590


# --------------------------------------------------------------------------
# Input resolution (file-change swap for the unified base)
# --------------------------------------------------------------------------
def load_config() -> dict:
    return json.loads((HERE / "inputs.json").read_text())


def resolve_summary(base: str, design: str, turnover: str,
                    config: dict | None = None) -> Path | None:
    """Locate the cohort summary CSV for (base, design, turnover) using the
    candidate (dir, pattern) list in inputs.json. Returns None if absent."""
    config = config or load_config()
    spec = config["bases"].get(base)
    if spec is None:
        return None
    for cand in spec["candidates"]:
        p = (HERE / cand["dir"] / cand["pattern"].format(
            design=design, turnover=turnover)).resolve()
        if p.exists():
            return p
    return None


def load_summary(base: str, design: str, turnover: str,
                 config: dict | None = None) -> pd.DataFrame | None:
    p = resolve_summary(base, design, turnover, config)
    if p is None:
        return None
    return pd.read_csv(p, index_col="fy").reindex(YEARS)


def base_status(config: dict | None = None) -> dict:
    """Determine which base can serve as headline. The unified base is the
    headline per the Nov 22 2026 sponsor decision; if its outputs are not
    yet present (or fail the provenance check), fall back to loans-only and
    say so loudly in every output."""
    config = config or load_config()
    loans = load_summary("loans_only", "floating", "central", config)
    unified = load_summary("unified", "floating", "central", config)
    status = {"headline": "loans_only", "unified_present": False,
              "sensitivity": None, "note": ""}
    if unified is not None and loans is not None:
        u = float(unified.loc[2027, "eligible_stock_bn"])
        l = float(loans.loc[2027, "eligible_stock_bn"])
        if u > 1.05 * l:
            status.update(headline="unified", unified_present=True,
                          sensitivity="loans_only",
                          note=f"unified eligible stock FY27 ${u:,.0f}B vs "
                               f"loans-only ${l:,.0f}B (provenance check passed)")
            return status
        status["note"] = ("unified candidate file found but FAILED provenance "
                          "check (eligible stock not > loans-only + 5%); "
                          "treated as absent")
    elif unified is not None:
        status.update(headline="unified", unified_present=True,
                      sensitivity=None, note="unified present; loans-only missing")
        return status
    if not status["note"]:
        status["note"] = ("unified-base cohort outputs NOT YET PRESENT; "
                          "headline computed on loans-only base and must be "
                          "re-run when the unified CSVs land (file change "
                          "only -- see inputs.json)")
    status["sensitivity"] = "unified (pending)" if loans is not None else None
    return status


def load_fiscal_skeleton(config: dict | None = None) -> pd.DataFrame:
    config = config or load_config()
    p = (HERE / config["fiscal_skeleton"]).resolve()
    return pd.read_csv(p, index_col="fy").reindex(YEARS)


# --------------------------------------------------------------------------
# Component 2: Treasury repricing with a time-varying yield shift
# --------------------------------------------------------------------------
def treasury_savings_by_year(dy_by_year: dict[int, float]) -> pd.Series:
    """Interest savings ($B, positive = saving) on ALL marketable debt from
    a time-varying new-issue yield shift, using the cohort skeleton's
    bucket repricing mechanics (cohort/data.py TREASURY). Two parallel
    pool recursions (dy and dy=0); validated against cohort fiscal.py for
    the constant-dy case in the test suite."""
    import sys
    sys.path.insert(0, str(COHORT_DIR))
    from data import TREASURY  # noqa: E402

    base_rate = TREASURY["avg_rate_marketable"]
    buckets = dict(TREASURY["buckets_bn"])
    mat = TREASURY["bucket_annual_maturity"]

    def interest_path(dy: dict[int, float]) -> dict[int, float]:
        rates = {b: base_rate for b in buckets}
        out = {}
        for t in YEARS:
            interest = 0.0
            for b, bal in buckets.items():
                m = mat[b] * bal
                rates[b] = (rates[b] * (bal - m)
                            + (base_rate + dy.get(t, 0.0)) * m) / bal
                interest += rates[b] * bal
            out[t] = interest
        return out

    shifted = interest_path(dy_by_year)
    base = interest_path({})
    return pd.Series({t: base[t] - shifted[t] for t in YEARS},
                     name="treasury_savings_gross_bn")


def dy_path_for_tau(tau: float, skeleton: pd.DataFrame) -> dict[int, float]:
    """dy_t = -tau * (IORB_base_t - IORB_ms_t) from the skeleton's paths."""
    return {t: -tau * (float(skeleton.loc[t, "iorb_base"])
                       - float(skeleton.loc[t, "iorb_ms"])) for t in YEARS}


# --------------------------------------------------------------------------
# Component 1: fee receipts with erosion + haircut
# --------------------------------------------------------------------------
def erosion_path(erosion_yr5: float, theta: float) -> dict[int, float]:
    """e_t phases in linearly over the first five collection years
    (FY2028 = year 1 ... FY2032 = year 5), then holds. ASSUMED coupling:
    e_t proportional to theta (see module docstring)."""
    out = {}
    for t in YEARS:
        ramp = min(1.0, max(0.0, (t - 2027) / 5.0))
        out[t] = min(EROSION_CAP, erosion_yr5 * theta * ramp)
    return out


def net_fee_receipts(summary: pd.DataFrame, theta: float,
                     erosion_yr5: float,
                     haircut: float = TAX_INTERACTION_HAIRCUT) -> pd.DataFrame:
    e = erosion_path(erosion_yr5, theta)
    rows = []
    for t in YEARS:
        gross = float(summary.loc[t, "collections_bn"])
        er = e[t]
        rows.append({"fy": t,
                     "eligible_stock_bn": float(summary.loc[t, "eligible_stock_bn"]),
                     "covered_stock_bn": float(summary.loc[t, "covered_stock_bn"]),
                     "fee_rate": float(summary.loc[t, "fee_rate"]),
                     "gross_collections_bn": gross,
                     "erosion_rate": er,
                     "net_fee_receipts_bn": gross * (1.0 - er) * (1.0 - haircut)})
    return pd.DataFrame(rows).set_index("fy")


# --------------------------------------------------------------------------
# Consolidation
# --------------------------------------------------------------------------
def consolidate(base: str, design: str, turnover: str, theta: float,
                erosion_yr5: float, beta: float = 0.55,
                config: dict | None = None,
                macro_feedback: str | None = None) -> dict[float, pd.DataFrame]:
    """Full annual consolidation for one parameter combination, returned as
    {tau: DataFrame}. `beta` is accepted for grid completeness and is
    INERT in this layer (documented in the module docstring).

    `macro_feedback` (final integration pass): None for the pre-feedback
    projection, or a Lane B regime in {"B", "C", "D", "E"} to apply that
    regime's FRB/US feedback -- the fee-path receipts ratio and the
    endogenous fiscal drag (see frbus_feedback.py). Regimes D and E are
    measured against their SHOCKED conventional baselines in Lane B;
    applying them here adjusts only the fee and drag components (the
    savings and remittance components are not re-based to shocked IORB
    paths -- a stated limitation of the final projection)."""
    config = config or load_config()
    summary = load_summary(base, design, turnover, config)
    if summary is None:
        raise FileNotFoundError(f"no cohort summary for base={base} "
                                f"design={design} turnover={turnover}")
    skeleton = load_fiscal_skeleton(config)
    feedback = None
    if macro_feedback is not None:
        from frbus_feedback import regime_feedback
        # Denominator is Lane B's own reference configuration (loans-only,
        # floating, central turnover) regardless of the cell being run:
        # the ratio measures Lane B's fee path against the skeleton path
        # for the SAME configuration Lane B actually consumed.
        loans = load_summary("loans_only", "floating", "central", config)
        if loans is None:
            raise FileNotFoundError("macro feedback needs the loans-only "
                                    "summary for the receipts ratio")
        feedback = regime_feedback(
            macro_feedback,
            skeleton_gross_total=float(loans["collections_bn"].sum()))
    fees = net_fee_receipts(summary, theta, erosion_yr5)
    d_remit = (skeleton["cash_remittance_bn_ms"]
               - skeleton["cash_remittance_bn_base"]).rename("delta_remittances_bn")
    out: dict[float, pd.DataFrame] = {}
    for tau in TAUS:
        savings_gross = treasury_savings_by_year(dy_path_for_tau(tau, skeleton))
        df = fees.copy()
        df["iorb_base"] = skeleton["iorb_base"]
        df["iorb_ms"] = skeleton["iorb_ms"]
        df["treasury_savings_gross_bn"] = savings_gross
        df["treasury_savings_consol_bn"] = savings_gross * PUBLIC_SHARE
        df["delta_remittances_bn"] = d_remit
        df["consolidated_net_bn"] = (df["net_fee_receipts_bn"]
                                     + df["treasury_savings_consol_bn"]
                                     + df["delta_remittances_bn"])
        df["tau"] = tau
        if feedback is None:
            out[tau] = apply_macro_feedback(df)  # slots EMPTY (NaN)
        else:
            out[tau] = apply_macro_feedback(
                df, frbus_drag=feedback["drag_annual_bn"],
                fee_path_ratio=feedback["receipts_ratio"])
    return out


# --------------------------------------------------------------------------
# MACRO FEEDBACK INTERFACE (FRB/US populated in the final pass; SFC empty)
# --------------------------------------------------------------------------
def apply_macro_feedback(table: pd.DataFrame,
                         frbus_drag: pd.Series | None = None,
                         fee_path_ratio: float = 1.0) -> pd.DataFrame:
    """Apply Lane B (FRB/US Design E) macro feedback to a consolidated
    table. Called with no arguments (the pre-feedback projection), this
    adds both slot columns EMPTY (NaN) and changes nothing.

    With feedback (final integration pass):
      * net fee receipts are rescaled by `fee_path_ratio` -- Lane B's
        iterated f = rff fixed-point receipts over the cohort skeleton's
        receipts for the same configuration (frbus_feedback.py). The
        pre-scaling series is preserved in
        `net_fee_receipts_skeleton_bn` and the ratio in `fee_path_ratio`.
        Erosion and the tax-interaction haircut are proportional
        adjustments, so rescaling net receipts rescales gross
        consistently.
      * `frbus_feedback_bn` carries the regime's annual endogenous
        fiscal drag, scaled by the same ratio (ASSUMED proportionality),
        and is added into `consolidated_net_bn`. The drag excludes
        receipts and interest by construction, so nothing is
        double-counted against the tau-surface savings.
      * `sfc_ix_adjustment_bn` remains EMPTY (NaN) BY DESIGN. The SFC
        Section IX experiment is a one-period, first-round sign and
        channel-decomposition result (sfc/SECTION_IX_RESULTS.md); it is
        not an annual fiscal series, and converting it into one would
        fabricate precision. Its fiscal meaning enters the final report
        qualitatively: under this projection's non-recycling closure
        (receipts banked), Section IX finds the fee regime modestly
        MORE contractionary at full pass-through, i.e. the drag
        direction Lane B measures is corroborated, not offset.
    """
    table = table.copy()
    if frbus_drag is None:
        table["frbus_feedback_bn"] = np.nan    # EMPTY SLOT -- no feedback
        table["sfc_ix_adjustment_bn"] = np.nan  # EMPTY SLOT -- see docstring
        return table
    drag = frbus_drag.reindex(table.index).fillna(0.0) * fee_path_ratio
    skeleton_fees = table["net_fee_receipts_bn"].copy()
    table["net_fee_receipts_skeleton_bn"] = skeleton_fees
    table["fee_path_ratio"] = fee_path_ratio
    table["net_fee_receipts_bn"] = skeleton_fees * fee_path_ratio
    table["frbus_feedback_bn"] = drag
    table["consolidated_net_bn"] = (table["consolidated_net_bn"]
                                    + (table["net_fee_receipts_bn"]
                                       - skeleton_fees)
                                    + drag)
    table["sfc_ix_adjustment_bn"] = np.nan  # EMPTY BY DESIGN -- see docstring
    return table
