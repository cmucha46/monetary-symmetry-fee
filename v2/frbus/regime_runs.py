"""Monetary Symmetry Fee v2 -- FRB/US regime experiments (Design E).

Implements INTERFACE_ASSESSMENT.md SS6 protocol exactly:
  - Solver: PolicyEngine frbus 0.1.0, official Oct 2026 LONGBASE + official
    model.xml. Expectations: MCE (mcap+wp) headline, VAR robustness.
  - Every run: dfpex=1, dfpdbt=0, dfpsrp=0 (non-recycling fiscal closure).
  - Wedges ONLY on rme / rcar / rbbb, imposed as exogenised LEVEL paths
    (matched-baseline level + wedge). rg5/rg10/rg30 never wedged.
  - Receipts ONLY via exogenised ugfsrp path = matched-baseline ugfsrp
    + receipts_t / xgdpn_t(baseline). gfrecn never touched.
  - rff NEVER exogenised: the inertial Taylor rule (LONGBASE default,
    dmpintay=1) finds the funds path (Design E).
  - wedge_{c,t} = beta * f_t * kappa_{c,t}; kappa keys off ORIGINATION
    coverage (assessment SS1.3); revenue keys off STOCK coverage via the
    cohort model (Component 3), floating design, central turnover.

Synchronisation fixed point: post-transition the statute sets f_t = i_t
(IORB ~ rff). The wedge depends on f while the rule-produced rff depends on
the wedge -- resolved by whole-path fixed-point iteration: solve with the
current f path, rebuild f from the produced rff path (ramp applied to the
produced path), re-derive cohort receipts from the rebuilt f, repeat until
max|df| < 0.02pp and max FY collections change < 1% (max 10 iterations).
Initial guess: f ramps toward 0.5 x baseline rff (the memo's illustrative
halving) -- an initial guess only; the fixed point is what is reported.

SPONSOR DECISION 2026-11-22 (bonds in base): the cohort lane's unified-base
outputs had NOT landed when these runs were executed, so per instruction
the LOAN-ONLY kappa/receipts are used as the documented lower bound:
  kappa_rme = kappa_rcar = 1.0 from the effective date (all new mortgage /
  consumer originations are covered loans under either base).
  kappa_rbbb (loan-only) = covered business-LOAN origination flow /
  total business credit origination flow (loans + bonds), from cohort
  parameters = 0.757 (bond turnover delta=0.09 ASSUMED, ~11y avg maturity).
  A kappa_rbbb = 1.0 sensitivity (the unified-base value) is run for
  regimes B and C at beta=1.0 to bound the difference. Receipts are
  loan-only cohort collections (lower bound; unified base raises them).

Regimes (memo SSVII), window 2027Q1-2036Q4, effective date 2027Q4
(Oct 1, 2027, per cohort lane):
  A  conventional baseline (matched control for each shock state)
  B  fast synchronisation: fee 0.15% at 2027Q4, half-gap at 2028Q1,
     f = rff from 2028Q2 (~2 quarters)
  C  full 24-month synchronisation: linear gap closure over 8 quarters,
     f = rff from 2029Q4
  D  C + severe inflationary shock: picxfe_aerr = +2.0pp, 2028Q1-2028Q4
     (one-year add-factor to the core PCE inflation equation; the model's
     Phillips-curve persistence amplifies the realised overshoot)
  E  C + severe recessionary (financial-conditions) shock:
     reqp_aerr = +3.0pp and rbbbp_aerr = +1.0pp, 2028Q1-2028Q4
D/E fee runs are compared against A + the SAME shock (identical shocks,
memo SSVII). D/E are built on C (the statutory-max transition), documented
in REGIME_RESULTS.md.
"""
from __future__ import annotations

import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path.home() / "workspace/monetary-symmetry"
DATA = BASE / "upstream/official/data_extract/data_only_package/LONGBASE.TXT"
XML = BASE / "upstream/official/pyfrbus_extract/pyfrbus/models/model.xml"
OUT = Path(__file__).parent / "regime_outputs"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(BASE / "v2/cohort"))
from cohort_model import run_model as cohort_run  # noqa: E402

from frbus import Frbus, load_data  # noqa: E402

START, END = pd.Period("2027Q1"), pd.Period("2036Q4")
QUARTERS = pd.period_range(START, END, freq="Q")
EFF = pd.Period("2027Q4")          # effective date: Oct 1, 2027
FEE0 = 0.15                        # statutory initial fee, percent
WEDGED = ["rme", "rcar", "rbbb"]
EXOG = WEDGED + ["ugfsrp"]

# ---------------------------------------------------------------- kappa ---
# Origination coverage. Loans: 1.0 from EFF (all post-enactment originations
# covered). rbbb loan-only: business-loan origination flow share of total
# business credit origination flow (see header). Bond stock/flows from
# cohort DATA.md excluded-stock table (corporate bonds $9,321.4B).
_BIZ_LOAN_FLOW = (0.33 + 0.035) * 6215.3 + (0.14 + 0.03) * 7203.2   # $B/yr
_BOND_FLOW = (0.09 + 0.03) * 9321.4                                  # delta=0.09 ASSUMED
KAPPA_RBBB_LOANONLY = _BIZ_LOAN_FLOW / (_BIZ_LOAN_FLOW + _BOND_FLOW)


def kappa_path(kind: str, rbbb_value: float) -> dict[str, pd.Series]:
    k = {}
    for v in WEDGED:
        s = pd.Series(0.0, index=QUARTERS)
        s.loc[EFF:] = 1.0
        k[v] = s
    k["rbbb"] = k["rbbb"] * rbbb_value
    return k


# ---------------------------------------------------------------- shocks --
def shock_aerr(state: str) -> dict[str, tuple[pd.Period, pd.Period, float]]:
    """Add-factor shocks by shock-state. Applied to solve inputs AFTER
    init_trac (baseline tracs were computed at zero aerr, so the shock
    enters cleanly)."""
    if state == "plain":
        return {}
    if state == "infl":
        return {"picxfe_aerr": (pd.Period("2028Q1"), pd.Period("2028Q4"), 2.0)}
    if state == "rec":
        return {"reqp_aerr": (pd.Period("2028Q1"), pd.Period("2028Q4"), 3.0),
                "rbbbp_aerr": (pd.Period("2028Q1"), pd.Period("2028Q4"), 1.0)}
    raise ValueError(state)


def apply_shocks(df: pd.DataFrame, state: str) -> pd.DataFrame:
    for col, (a, b, val) in shock_aerr(state).items():
        df.loc[a:b, col] = val
    return df


# ------------------------------------------------------------- fee paths --
def ramp_lambda(speed: str) -> pd.Series:
    """Fraction of the (0.15% -> rff) gap closed, by quarter."""
    lam = pd.Series(0.0, index=QUARTERS)
    n = (EFF - START).n  # quarters before EFF stay 0
    for i, q in enumerate(QUARTERS):
        k = i - n  # quarters since EFF (0 at EFF)
        if k < 0:
            lam[q] = 0.0
        elif speed == "B":
            lam[q] = min(k / 2.0, 1.0)          # synced by EFF+2 = 2028Q2
        elif speed == "C":
            lam[q] = min(k / 8.0, 1.0)          # synced by EFF+8 = 2029Q4
        else:
            raise ValueError(speed)
    return lam


def build_fee(rff_prev: pd.Series, speed: str) -> pd.Series:
    lam = ramp_lambda(speed)
    f = pd.Series(0.0, index=QUARTERS)
    f.loc[EFF:] = (1 - lam.loc[EFF:]) * FEE0 + lam.loc[EFF:] * rff_prev.loc[EFF:]
    return f


def fy_avg_fee(f: pd.Series) -> dict[int, float]:
    """FY-average fee (decimal) for the cohort model. FY t = (t-1)Q4..tQ3."""
    out = {}
    for fy in range(2027, 2037):
        qs = [pd.Period(f"{fy-1}Q4")] + [pd.Period(f"{fy}Q{i}") for i in (1, 2, 3)]
        vals = [float(f[q]) if q in f.index else 0.0 for q in qs]
        out[fy] = float(np.mean(vals)) / 100.0
    return out


def cohort_receipts(f: pd.Series) -> tuple[pd.Series, pd.DataFrame]:
    """Run the cohort model (floating, central) at the FY-average fee path;
    return quarterly receipts at annual rate ($B SAAR) + the FY table."""
    fee_path = fy_avg_fee(f)
    df = cohort_run(fee_path=fee_path, design="floating", delta_case="central")
    tot = df[df["category"] == "TOTAL"].set_index("fy")["collections_bn"]
    rec = pd.Series(0.0, index=QUARTERS)
    for q in QUARTERS:
        fy = q.year + (1 if q.quarter == 4 else 0)   # Q4 belongs to next FY
        rec[q] = float(tot.get(fy, tot.get(2036, 0.0)))
    return rec, tot


# ----------------------------------------------------------------- solves -
class Lane:
    """One expectations mode: baseline instance + fee instance, tracs once."""

    def __init__(self, mode: str):
        self.mode = mode
        mce = "mcap+wp" if mode == "mce" else None
        data = load_data(str(DATA))
        data.loc[START:END, "dfpdbt"] = 0
        data.loc[START:END, "dfpsrp"] = 0
        data.loc[START:END, "dfpex"] = 1
        self.data = data
        self.m_base = Frbus(str(XML), mce=mce)
        self.wa_base = self.m_base.init_trac(START, END, data)
        self.m_fee = Frbus(str(XML), mce=mce)
        self.m_fee.exogenize(EXOG)
        self.wa_fee = self.m_fee.init_trac(START, END, data)
        self.baselines: dict[str, pd.DataFrame] = {}

    def baseline(self, state: str) -> pd.DataFrame:
        if state not in self.baselines:
            d = apply_shocks(self.wa_base.copy(), state)
            self.baselines[state] = self.m_base.solve(START, END, d)
        return self.baselines[state]

    def fee_solve(self, base: pd.DataFrame, state: str, f: pd.Series,
                  beta: float, kap: dict[str, pd.Series],
                  receipts: pd.Series) -> pd.DataFrame:
        d = apply_shocks(self.wa_fee.copy(), state)
        for v in WEDGED:
            d.loc[START:END, v] = (base.loc[START:END, v]
                                   + beta * f * kap[v])
        d.loc[START:END, "ugfsrp"] = (base.loc[START:END, "ugfsrp"]
                                      + receipts / base.loc[START:END, "xgdpn"])
        return self.m_fee.solve(START, END, d)


def run_fee_regime(lane: Lane, regime: str, speed: str, state: str,
                   beta: float, rbbb_kappa: float,
                   log: dict) -> tuple[pd.DataFrame, pd.Series, pd.Series, list]:
    base = lane.baseline(state)
    kap = kappa_path("loanonly", rbbb_kappa)
    # initial guess: ramp toward half the baseline funds path (memo SSII.C)
    f = build_fee(0.5 * base.loc[QUARTERS, "rff"], speed)
    receipts, _ = cohort_receipts(f)
    hist = []
    sol = None
    for it in range(10):
        sol = lane.fee_solve(base, state, f, beta, kap, receipts)
        f_new = build_fee(sol.loc[QUARTERS, "rff"], speed)
        receipts_new, _ = cohort_receipts(f_new)
        df_max = float((f_new - f).abs().max())
        dr_max = float((receipts_new - receipts).abs().max())
        hist.append({"iter": it, "max_df_pp": df_max,
                     "max_dreceipts_bn": dr_max})
        f, receipts = f_new, receipts_new
        if df_max < 0.02 and dr_max < 5.0:
            break
    # final solve at the converged inputs (strict consistency)
    sol = lane.fee_solve(base, state, f, beta, kap, receipts)
    resid = float((f.loc[EFF + 8:] - sol.loc[EFF + 8:, "rff"]).abs().max()) \
        if speed == "C" else \
        float((f.loc[EFF + 2:] - sol.loc[EFF + 2:, "rff"]).abs().max())
    log[f"{regime}|{lane.mode}|beta={beta}|krbbb={rbbb_kappa}"] = {
        "iterations": hist, "post_sync_max_|f-rff|_pp": resid}
    return sol, f, receipts, hist


# ---------------------------------------------------------------- output --
KEEP = ["rff", "rme", "rcar", "rbbb", "rccd", "rg10", "xgdp", "xgap2",
        "lur", "picxfe", "gfsrpn", "gfdbtnp", "gfintn"]


def write_run_csv(runid: str, sol: pd.DataFrame, base: pd.DataFrame,
                  f: pd.Series | None, receipts: pd.Series | None):
    df = pd.DataFrame({"period": [str(q) for q in QUARTERS]})
    for v in KEEP:
        df[f"L_{v}"] = sol.loc[QUARTERS, v].to_numpy()
    for v in KEEP:
        if v == "xgdp":
            df[f"D_{v}_pct"] = (100 * (sol.loc[QUARTERS, v]
                                       / base.loc[QUARTERS, v] - 1)).to_numpy()
        else:
            df[f"D_{v}"] = (sol.loc[QUARTERS, v]
                            - base.loc[QUARTERS, v]).to_numpy()
    if f is not None:
        df["fee_f_pct"] = f.to_numpy()
        df["receipts_bn_saar"] = receipts.to_numpy()
    df.to_csv(OUT / f"paths_{runid}.csv", index=False)


def main():
    log: dict = {"kappa_rbbb_loanonly": KAPPA_RBBB_LOANONLY,
                 "biz_loan_flow_bn": _BIZ_LOAN_FLOW, "bond_flow_bn": _BOND_FLOW,
                 "runs": {}, "errors": {}}
    t_start = time.time()
    for mode in ["mce", "var"]:
        lane = Lane(mode)
        # Regime A baselines (plain + both shock states)
        for state in ["plain", "infl", "rec"]:
            b = lane.baseline(state)
            write_run_csv(f"A_{state}_{mode}", b, b, None, None)
            if state != "plain":
                plain = lane.baseline("plain")
                dev = {
                    "xgdp_trough_pct": float((100 * (b.loc[QUARTERS, "xgdp"]
                        / plain.loc[QUARTERS, "xgdp"] - 1)).min()),
                    "lur_peak_dev_pp": float((b.loc[QUARTERS, "lur"]
                        - plain.loc[QUARTERS, "lur"]).max()),
                    "picxfe_peak_dev_pp": float((b.loc[QUARTERS, "picxfe"]
                        - plain.loc[QUARTERS, "picxfe"]).max()),
                    "rff_peak_dev_pp": float((b.loc[QUARTERS, "rff"]
                        - plain.loc[QUARTERS, "rff"]).max()),
                }
                log["runs"][f"A_{state}_{mode}_shocksize"] = dev
                print(f"[{mode}] shock {state}: {dev}", flush=True)
        configs = [
            # runid, regime, speed, state, beta, kappa_rbbb
            ("B_b100", "B", "B", "plain", 1.00, KAPPA_RBBB_LOANONLY),
            ("B_b075", "B", "B", "plain", 0.75, KAPPA_RBBB_LOANONLY),
            ("B_b050", "B", "B", "plain", 0.50, KAPPA_RBBB_LOANONLY),
            ("B_b100_k1", "B", "B", "plain", 1.00, 1.0),
            ("C_b100", "C", "C", "plain", 1.00, KAPPA_RBBB_LOANONLY),
            ("C_b075", "C", "C", "plain", 0.75, KAPPA_RBBB_LOANONLY),
            ("C_b050", "C", "C", "plain", 0.50, KAPPA_RBBB_LOANONLY),
            ("C_b100_k1", "C", "C", "plain", 1.00, 1.0),
            ("D_b100", "D", "C", "infl", 1.00, KAPPA_RBBB_LOANONLY),
            ("D_b075", "D", "C", "infl", 0.75, KAPPA_RBBB_LOANONLY),
            ("E_b100", "E", "C", "rec", 1.00, KAPPA_RBBB_LOANONLY),
            ("E_b075", "E", "C", "rec", 0.75, KAPPA_RBBB_LOANONLY),
        ]
        for runid, regime, speed, state, beta, krbbb in configs:
            t0 = time.time()
            try:
                sol, f, receipts, hist = run_fee_regime(
                    lane, regime, speed, state, beta, krbbb, log["runs"])
                base = lane.baseline(state)
                write_run_csv(f"{runid}_{mode}", sol, base, f, receipts)
                print(f"[{mode}] {runid}: OK in {time.time()-t0:.0f}s, "
                      f"{len(hist)} iterations", flush=True)
            except Exception as exc:  # report honestly, keep going
                log["errors"][f"{runid}_{mode}"] = {
                    "error": repr(exc), "trace": traceback.format_exc()}
                print(f"[{mode}] {runid}: FAILED {exc!r}", flush=True)
    log["wall_seconds"] = time.time() - t_start
    (OUT / "run_log.json").write_text(json.dumps(log, indent=1, default=str))
    print("DONE", log["wall_seconds"])


if __name__ == "__main__":
    main()
