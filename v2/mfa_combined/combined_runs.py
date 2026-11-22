"""Monetary Symmetry Fee v2 + Medicare for America (H.R.10924) -- COMBINED
FRB/US runs (Lane 2). Design E discipline per INTERFACE_ASSESSMENT.md,
infrastructure reused from regime_runs.py (Lane class, kappa paths,
whole-path f = rff fixed-point solver). Fee-only runs are NOT re-solved;
comparisons read regime_outputs/paths_C_b100_*.csv.

SPENDING CLOSURE: all fee savings are directed to MFA -- i.e. the combined
run imposes the Regime C fee (wedges + ugfsrp fee receipts) AND the MFA
fiscal flows simultaneously, with the non-recycling closure
dfpex=1, dfpdbt=0, dfpsrp=0 in every run (the surplus is the residual
ledger; nothing is re-spent by the fiscal rule).

MFA ENTRY MAP (see v2/mfa_combined/COMBINED_FRBUS.md for full text):
  (1) Incremental federal health outlays (gross - displaced federal):
      egfe EXOGENISED at baseline level + flow converted to 2012$ with
      the baseline implied federal-purchases deflator (egfen/egfe).
      FRB/US has NO health variable (verified by name/definition search
      of model.xml); egfe (federal purchases) is the only exogenous
      final-demand carrier for government-financed services.
  (2) Enrollee premiums, (3) employer contributions, (4) Title II taxes:
      imposed ugfsrp path, as a SEPARATELY IDENTIFIED MFA-receipts
      component (premiums + employer + Title II), distinct from the fee
      component in every imposed path and output column. No rate carrier
      exists for this bundle (trptx covers only the personal average
      rate; INTERFACE_ASSESSMENT SS2.2 rules out tpn/tcin entry), so the
      residual route is used with the composition caveat stated.
      Title II annual path: mfa_model.py gives window totals only
      (central $6.11T -- reproduced exactly); allocated across FY28-36
      in proportion to baseline FY nominal GDP (xgdpn).
  (5) Displaced PRIVATE premium spending: eco_aerr growth-shift path
      that moves real PCE (nondurables + non-housing services) to
      baseline - displaced private health spending, where displaced
      private = (exchange-cohort gross - PTC) + 25% employee share of
      ESI-cohort gross (cohort gross rebuilt from mfa_model). The aerr
      form (not exogenisation) preserves eco's endogenous income
      response. Employer premium savings have NO carrier (profits /
      labour-cost channel absent) -- not represented.

Quarterly convention: FY t = (t-1)Q4..tQ3 (FY2028 starts 2027Q4, the fee
effective date). Annual $B spread evenly over the FY's four quarters, so
the quarterly SAAR value equals the annual $B figure.

Runs (beta=1.0, loan-only kappa as in Lane B):
  MFAonly_{mce,var}      MFA flows only, conventional policy
  COMB_C_{mce,var}       Regime C fee (fixed point RE-SOLVED with MFA
                         in place) + MFA flows
  COMB_B_mce             Regime B fee + MFA (sensitivity)
  COMB_C_high_mce        Regime C fee + MFA HIGH-STRESS scenario
                         (residual +$10.73T; sensitivity)
"""
from __future__ import annotations

import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
BASE = Path.home() / "workspace/monetary-symmetry"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(BASE / "mfa"))
import regime_runs as rr  # noqa: E402  (Lane B infrastructure)
import mfa_model as mm  # noqa: E402

from frbus import Frbus, load_data  # noqa: E402

START, END, QUARTERS, EFF = rr.START, rr.END, rr.QUARTERS, rr.EFF
OUT = HERE / "combined_outputs"
OUT.mkdir(exist_ok=True)
EXOG2 = rr.EXOG + ["egfe"]


# ------------------------------------------------------------ MFA flows --
def fy_of(q: pd.Period) -> int:
    return q.year + (1 if q.quarter == 4 else 0)


def cohort_private_gross(case: str) -> dict[int, float]:
    """Gross MFA cost ($B/yr) of the privately-financed cohorts:
    exchange (net of PTC) + 25% employee share of ESI opt-in cohort.
    Rebuilt from mfa_model enrollment + gross-cost structure; topup and
    waiting-list clearance are Medicaid (public) items, excluded."""
    p = mm.CASES[case]
    enr = mm.enrollment(case)
    ptc = {y: mm.PTC_OUTLAYS[i] for i, y in enumerate(mm.YEARS)}
    out = {}
    for i, y in enumerate(mm.YEARS):
        mult = p["rate"] * (1 + p["induced"]) * p["cs"]
        growth = (1 + p["g"]) ** (y - 2028)

        def cohort_gross(k):
            core = enr[k][i] * mm.CORE_2028[k] / 1000.0 * mult * growth
            dvh = enr[k][i] * p["dvh"] / 1000.0 * growth
            ltss = (enr[k][i] * mm.LTSS_NEW_FACTOR[k] / 1000.0
                    * p["ltss_sh"] * p["ltss_c"] * growth)
            return (core + dvh + ltss) * (1 + p["admin"])

        out[y] = max(cohort_gross("exchange") - ptc[y], 0.0) \
            + 0.25 * cohort_gross("esi")
    return out


def mfa_annual(case: str, base: pd.DataFrame) -> pd.DataFrame:
    """Annual MFA flows ($B) by FY: incremental outlays, premiums,
    employer contributions, Title II (GDP-share allocation of the
    mfa_model window total), MFA receipts total, displaced private."""
    det = pd.read_csv(BASE / "mfa/data/annual_detail.csv")
    det = det[det["case"] == case].set_index("year")
    t2_total = sum(mm.TITLE2[case].values()) * 1000.0  # $B
    # FY nominal GDP shares from the matched baseline solution
    xg = base.loc[QUARTERS, "xgdpn"]
    fy_gdp = {fy: float(xg[[q for q in QUARTERS if fy_of(q) == fy]].sum())
              for fy in mm.YEARS}
    tot_gdp = sum(fy_gdp.values())
    priv = cohort_private_gross(case)
    rows = {}
    for y in mm.YEARS:
        incr = float(det.loc[y, "gross_B"] - det.loc[y, "displaced_B"])
        rows[y] = {
            "incr_outlays_bn": incr,
            "premiums_bn": float(det.loc[y, "premiums_B"]),
            "employer_bn": float(det.loc[y, "employer_B"]),
            "title2_bn": t2_total * fy_gdp[y] / tot_gdp,
            "displaced_private_bn": priv[y],
        }
    df = pd.DataFrame.from_dict(rows, orient="index")
    df["mfa_receipts_bn"] = (df["premiums_bn"] + df["employer_bn"]
                             + df["title2_bn"])
    df["residual_bn"] = (df["incr_outlays_bn"] - df["mfa_receipts_bn"])
    return df


def mfa_quarterly(ann: pd.DataFrame, base: pd.DataFrame) -> dict:
    """Quarterly imposed paths (SAAR $B unless noted) + eco_aerr +
    egfe real add-on (2012$ B)."""
    def qseries(col):
        # 2036Q4 belongs to FY2037 (outside the FY28-36 window): hold the
        # FY2036 value for that single quarter, Lane B's own fallback
        # convention in cohort_receipts -- FY-window sums are unaffected.
        return pd.Series({q: float(ann.loc[fy_of(q), col])
                          if fy_of(q) in ann.index
                          else (float(ann.loc[2036, col])
                                if fy_of(q) == 2037 else 0.0)
                          for q in QUARTERS})
    incr_q = qseries("incr_outlays_bn")
    rec_q = qseries("mfa_receipts_bn")
    priv_q = qseries("displaced_private_bn")
    # egfe add-on in real terms via baseline implied deflators
    defl_fed = base.loc[QUARTERS, "egfen"] / base.loc[QUARTERS, "egfe"]
    egfe_add = incr_q / defl_fed
    # eco_aerr: growth shift moving eco to baseline - displaced private
    # (real, deflated by baseline GDP deflator xgdpn/xgdp)
    defl_gdp = base.loc[QUARTERS, "xgdpn"] / base.loc[QUARTERS, "xgdp"]
    eco_base = base.loc[QUARTERS, "eco"]
    target = eco_base - priv_q / defl_gdp
    aerr = pd.Series(0.0, index=QUARTERS)
    prev_t, prev_b = None, None
    for q in QUARTERS:
        if q >= EFF:
            if prev_t is None:  # first imposed quarter: level shift
                aerr[q] = np.log(target[q] / eco_base[q])
            else:
                aerr[q] = (np.log(target[q] / prev_t)
                           - np.log(eco_base[q] / prev_b))
        prev_t, prev_b = target[q], eco_base[q]
    return {"incr_q": incr_q, "mfa_rec_q": rec_q, "priv_q": priv_q,
            "egfe_add": egfe_add, "eco_aerr": aerr}


# ------------------------------------------------------------- lane ------
class CombinedLane(rr.Lane):
    """Lane B lane + egfe exogenised on the fee instance."""

    def __init__(self, mode: str):
        self.mode = mode
        mce = "mcap+wp" if mode == "mce" else None
        data = load_data(str(rr.DATA))
        data.loc[START:END, "dfpdbt"] = 0
        data.loc[START:END, "dfpsrp"] = 0
        data.loc[START:END, "dfpex"] = 1
        self.data = data
        self.m_base = Frbus(str(rr.XML), mce=mce)
        self.wa_base = self.m_base.init_trac(START, END, data)
        self.m_fee = Frbus(str(rr.XML), mce=mce)
        self.m_fee.exogenize(EXOG2)
        self.wa_fee = self.m_fee.init_trac(START, END, data)
        self.baselines: dict[str, pd.DataFrame] = {}

    def solve_mfa(self, base, mfa, f=None, beta=1.0, kap=None,
                  fee_receipts=None):
        d = self.wa_fee.copy()
        if f is not None:  # fee wedges (Regime B/C)
            for v in rr.WEDGED:
                d.loc[START:END, v] = (base.loc[START:END, v]
                                       + beta * f * kap[v])
        else:
            fee_receipts = pd.Series(0.0, index=QUARTERS)
            for v in rr.WEDGED:  # exogenised at baseline level (no wedge)
                d.loc[START:END, v] = base.loc[START:END, v]
        d.loc[START:END, "egfe"] = (base.loc[START:END, "egfe"]
                                    + mfa["egfe_add"])
        d.loc[START:END, "ugfsrp"] = (
            base.loc[START:END, "ugfsrp"]
            + (fee_receipts + mfa["mfa_rec_q"]) / base.loc[START:END, "xgdpn"])
        d.loc[START:END, "eco_aerr"] = mfa["eco_aerr"]
        return self.m_fee.solve(START, END, d)


def run_combined_fee(lane, speed, mfa, log, tag):
    """Regime B/C fixed point RE-SOLVED with MFA flows in place."""
    base = lane.baseline("plain")
    kap = rr.kappa_path("loanonly", rr.KAPPA_RBBB_LOANONLY)
    f = rr.build_fee(0.5 * base.loc[QUARTERS, "rff"], speed)
    receipts, _ = rr.cohort_receipts(f)
    hist = []
    for it in range(10):
        sol = lane.solve_mfa(base, mfa, f, 1.0, kap, receipts)
        f_new = rr.build_fee(sol.loc[QUARTERS, "rff"], speed)
        receipts_new, _ = rr.cohort_receipts(f_new)
        df_max = float((f_new - f).abs().max())
        dr_max = float((receipts_new - receipts).abs().max())
        hist.append({"iter": it, "max_df_pp": df_max,
                     "max_dreceipts_bn": dr_max})
        f, receipts = f_new, receipts_new
        if df_max < 0.02 and dr_max < 5.0:
            break
    sol = lane.solve_mfa(base, mfa, f, 1.0, kap, receipts)
    n = 8 if speed == "C" else 2
    resid = float((f.loc[EFF + n:] - sol.loc[EFF + n:, "rff"]).abs().max())
    log[tag] = {"iterations": hist, "post_sync_max_|f-rff|_pp": resid}
    return sol, f, receipts


# ------------------------------------------------------------- output ----
KEEP = rr.KEEP + ["eco", "egfe"]


def write_csv(runid, sol, base, f, fee_rec, mfa):
    df = pd.DataFrame({"period": [str(q) for q in QUARTERS]})
    for v in KEEP:
        df[f"L_{v}"] = sol.loc[QUARTERS, v].to_numpy()
    for v in KEEP:
        if v == "xgdp":
            df[f"D_{v}_pct"] = (100 * (sol.loc[QUARTERS, v]
                                       / base.loc[QUARTERS, v]
                                       - 1)).to_numpy()
        else:
            df[f"D_{v}"] = (sol.loc[QUARTERS, v]
                            - base.loc[QUARTERS, v]).to_numpy()
    if f is not None:
        df["fee_f_pct"] = f.to_numpy()
        df["fee_receipts_bn_saar"] = fee_rec.to_numpy()
    df["mfa_receipts_bn_saar"] = mfa["mfa_rec_q"].to_numpy()
    df["mfa_incr_outlays_bn_saar"] = mfa["incr_q"].to_numpy()
    df["mfa_displaced_private_bn_saar"] = mfa["priv_q"].to_numpy()
    df.to_csv(OUT / f"paths_{runid}.csv", index=False)


def fy_sum(s: pd.Series) -> float:
    return float(sum(v / 4.0 for q, v in s.items()
                     if 2028 <= fy_of(q) <= 2036))


def metrics(sol, base, f, fee_rec, mfa):
    post = slice(pd.Period("2030Q1"), pd.Period("2036Q4"))
    d = sol.loc[QUARTERS] - base.loc[QUARTERS]
    m = {"rff_dev_mean_post": float(d.loc[post, "rff"].mean()),
         "rff_level_mean_post": float(sol.loc[post, "rff"].mean()),
         "lur_dev_2036Q4": float(d.loc[pd.Period("2036Q4"), "lur"]),
         "lur_dev_max": float(d["lur"].max()),
         "xgdp_dev_trough_pct": float(
             (100 * (sol.loc[QUARTERS, "xgdp"]
                     / base.loc[QUARTERS, "xgdp"] - 1)).min()),
         "picxfe_dev_2036Q4": float(d.loc[pd.Period("2036Q4"), "picxfe"]),
         "cum_dgfsrpn_bn": fy_sum(d["gfsrpn"]),
         "cum_dgfintn_bn": fy_sum(d["gfintn"]),
         "dgfdbtnp_2036Q4_bn": float(d.loc[pd.Period("2036Q4"), "gfdbtnp"]),
         "mfa_receipts_total_bn": fy_sum(mfa["mfa_rec_q"]),
         "mfa_incr_outlays_total_bn": fy_sum(mfa["incr_q"])}
    if f is not None:
        m["fee_mean_post_pct"] = float(f.loc[post].mean())
        m["fee_receipts_total_bn"] = fy_sum(fee_rec)
        # endogenous fiscal drag, frbus_feedback.py style, extended:
        # drag = Dsurplus - imposed receipts + imposed outlays + Dinterest
        m["drag_bn"] = (m["cum_dgfsrpn_bn"] - m["fee_receipts_total_bn"]
                        - m["mfa_receipts_total_bn"]
                        + m["mfa_incr_outlays_total_bn"]
                        + m["cum_dgfintn_bn"])
    else:
        m["drag_bn"] = (m["cum_dgfsrpn_bn"] - m["mfa_receipts_total_bn"]
                        + m["mfa_incr_outlays_total_bn"]
                        + m["cum_dgfintn_bn"])
    return m


def main():
    log: dict = {"runs": {}, "errors": {}}
    allm: dict = {}
    t0 = time.time()
    for mode in ["mce", "var"]:
        lane = CombinedLane(mode)
        base = lane.baseline("plain")
        ann_c = mfa_annual("central", base)
        mfa_c = mfa_quarterly(ann_c, base)
        if mode == "mce":
            ann_c.to_csv(OUT / "mfa_annual_central.csv")
            log["title2_central_total_bn"] = float(ann_c["title2_bn"].sum())
            log["residual_central_bn"] = float(ann_c["residual_bn"].sum())
        # (ii) MFA-only
        try:
            sol = lane.solve_mfa(base, mfa_c)
            write_csv(f"MFAonly_{mode}", sol, base, None, None, mfa_c)
            allm[f"MFAonly_{mode}"] = metrics(sol, base, None, None, mfa_c)
            print(f"[{mode}] MFAonly OK", flush=True)
        except Exception as exc:
            log["errors"][f"MFAonly_{mode}"] = {
                "error": repr(exc), "trace": traceback.format_exc()}
            print(f"[{mode}] MFAonly FAILED {exc!r}", flush=True)
        # (iii) Combined Regime C
        try:
            sol, f, rec = run_combined_fee(lane, "C", mfa_c, log["runs"],
                                           f"COMB_C_{mode}")
            write_csv(f"COMB_C_{mode}", sol, base, f, rec, mfa_c)
            allm[f"COMB_C_{mode}"] = metrics(sol, base, f, rec, mfa_c)
            print(f"[{mode}] COMB_C OK", flush=True)
        except Exception as exc:
            log["errors"][f"COMB_C_{mode}"] = {
                "error": repr(exc), "trace": traceback.format_exc()}
            print(f"[{mode}] COMB_C FAILED {exc!r}", flush=True)
        if mode == "mce":
            # (iv) Combined Regime B sensitivity
            try:
                sol, f, rec = run_combined_fee(lane, "B", mfa_c,
                                               log["runs"], "COMB_B_mce")
                write_csv("COMB_B_mce", sol, base, f, rec, mfa_c)
                allm["COMB_B_mce"] = metrics(sol, base, f, rec, mfa_c)
                print("[mce] COMB_B OK", flush=True)
            except Exception as exc:
                log["errors"]["COMB_B_mce"] = {
                    "error": repr(exc), "trace": traceback.format_exc()}
                print(f"[mce] COMB_B FAILED {exc!r}", flush=True)
            # high-stress sensitivity: Regime C + MFA high case
            try:
                ann_h = mfa_annual("high", base)
                ann_h.to_csv(OUT / "mfa_annual_high.csv")
                mfa_h = mfa_quarterly(ann_h, base)
                log["title2_high_total_bn"] = float(ann_h["title2_bn"].sum())
                log["residual_high_bn"] = float(ann_h["residual_bn"].sum())
                sol, f, rec = run_combined_fee(lane, "C", mfa_h,
                                               log["runs"], "COMB_C_high_mce")
                write_csv("COMB_C_high_mce", sol, base, f, rec, mfa_h)
                allm["COMB_C_high_mce"] = metrics(sol, base, f, rec, mfa_h)
                print("[mce] COMB_C_high OK", flush=True)
            except Exception as exc:
                log["errors"]["COMB_C_high_mce"] = {
                    "error": repr(exc), "trace": traceback.format_exc()}
                print(f"[mce] COMB_C_high FAILED {exc!r}", flush=True)
    log["wall_seconds"] = time.time() - t0
    (OUT / "run_log.json").write_text(json.dumps(log, indent=1, default=str))
    (OUT / "metrics.json").write_text(json.dumps(allm, indent=1))
    print(json.dumps(allm, indent=1))
    print("DONE", log["wall_seconds"])


if __name__ == "__main__":
    main()
