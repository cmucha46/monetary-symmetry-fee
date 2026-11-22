"""Run the FINAL MSF v2 integration: Lane D consolidation + Lane B
(FRB/US) macro feedback, the Treasuries appendix, and the
feedback-adjusted grid summary.

Usage: python3 run_final.py
Outputs (./outputs):
  final_projection_regime_<R>.csv  -- central case (unified base,
      floating, central turnover, theta=1.0, erosion=0.10) WITH Lane B
      feedback for R in {B, C, D, E}, all taus side by side
  treasuries_appendix.csv          -- holder/issuer-assessed arithmetic
  monte_carlo_feedback_adjusted_*  -- grid enumeration, FLOATING cells
      only (Lane B ran floating), Regime C feedback applied
  final_results.json               -- headline numbers for the report
"""
import json
from pathlib import Path

import pandas as pd

from consolidation import TAUS, consolidate, load_config
from frbus_feedback import regime_feedback
from monte_carlo import run_grid, summarize
from treasuries_appendix import treasuries_appendix

HERE = Path(__file__).parent
OUT = HERE / "outputs"
CENTRAL = dict(turnover="central", theta=1.0, erosion_yr5=0.10, beta=0.55)
REGIMES = ("B", "C", "D", "E")


def wide_table(tables: dict) -> pd.DataFrame:
    wide = None
    for tau in TAUS:
        df = tables[tau]
        if wide is None:
            wide = df.drop(columns=["tau", "treasury_savings_gross_bn",
                                    "treasury_savings_consol_bn",
                                    "consolidated_net_bn"])
        wide[f"treasury_savings_consol_tau{tau}_bn"] = \
            df["treasury_savings_consol_bn"]
        wide[f"consolidated_net_tau{tau}_bn"] = df["consolidated_net_bn"]
    return wide


def main() -> None:
    OUT.mkdir(exist_ok=True)
    config = load_config()
    results = {"central_case": CENTRAL, "regimes": {}}

    # Pre-feedback reference (skeleton fee path, no drag).
    pre = consolidate("unified", "floating", CENTRAL["turnover"],
                      CENTRAL["theta"], CENTRAL["erosion_yr5"],
                      beta=CENTRAL["beta"], config=config)
    results["pre_feedback_totals_10y_bn"] = {
        f"tau{tau}": float(pre[tau]["consolidated_net_bn"].sum())
        for tau in TAUS}
    results["pre_feedback_components_10y_bn"] = {
        "net_fee_receipts": float(pre[0.5]["net_fee_receipts_bn"].sum()),
        "delta_remittances": float(pre[0.5]["delta_remittances_bn"].sum()),
        "gross_collections": float(pre[0.5]["gross_collections_bn"].sum()),
    }
    print("PRE-FEEDBACK central (unified, floating): " + "  ".join(
        f"tau={t}: ${v:,.0f}B" for t, v in
        ((t, results["pre_feedback_totals_10y_bn"][f"tau{t}"]) for t in TAUS)))

    from consolidation import load_summary
    loans_gross = float(load_summary("loans_only", "floating", "central",
                                     config)["collections_bn"].sum())

    for regime in REGIMES:
        fb = regime_feedback(regime, skeleton_gross_total=loans_gross)
        tables = consolidate("unified", "floating", CENTRAL["turnover"],
                             CENTRAL["theta"], CENTRAL["erosion_yr5"],
                             beta=CENTRAL["beta"], config=config,
                             macro_feedback=regime)
        wide_table(tables).to_csv(OUT / f"final_projection_regime_{regime}.csv")
        totals = {f"tau{tau}": float(tables[tau]["consolidated_net_bn"].sum())
                  for tau in TAUS}
        results["regimes"][regime] = {
            "receipts_ratio": fb["receipts_ratio"],
            "lane_b_receipts_bn": fb["receipts_total_bn"],
            "drag_total_bn": fb["drag_total_bn"],
            "drag_scaled_total_bn": fb["drag_scaled_total_bn"],
            "net_fee_receipts_10y_bn":
                float(tables[0.5]["net_fee_receipts_bn"].sum()),
            "frbus_feedback_10y_bn":
                float(tables[0.5]["frbus_feedback_bn"].sum()),
            "totals_10y_bn": totals,
        }
        print(f"REGIME {regime}: ratio={fb['receipts_ratio']:.3f} "
              f"drag=${fb['drag_total_bn']:,.0f}B -> scaled "
              f"${fb['drag_scaled_total_bn']:,.0f}B | final: " + "  ".join(
                  f"tau={t}: ${totals[f'tau{t}']:,.0f}B" for t in TAUS))

    # Treasuries appendix.
    tsy = treasuries_appendix()
    tsy.to_csv(OUT / "treasuries_appendix.csv")
    results["treasuries_appendix_10y_bn"] = {
        "receipts_consol": float(tsy["receipts_consol_bn"].sum()),
        "extra_interest_consol": float(tsy["extra_interest_consol_bn"].sum()),
        "net_consol": float(tsy["net_consol_bn"].sum()),
        "issuer_assessed_net": 0.0,
    }
    print(f"TREASURIES APPENDIX: net (holder-assessed, consolidated) "
          f"${tsy['net_consol_bn'].sum():,.0f}B on receipts "
          f"${tsy['receipts_consol_bn'].sum():,.0f}B; issuer-assessed net $0B")

    # Feedback-adjusted grid (floating cells only; Regime C feedback).
    runs = run_grid("unified", config, macro_feedback="C",
                    designs=("floating",))
    runs.to_csv(OUT / "monte_carlo_feedback_adjusted_runs.csv", index=False)
    summary = summarize(runs)
    summary.to_csv(OUT / "monte_carlo_feedback_adjusted_summary.csv",
                   index=False)
    results["monte_carlo_feedback_adjusted"] = {
        "regime": "C", "designs": ["floating"],
        "summary": summary.to_dict("records")}
    print("\nFeedback-adjusted grid (floating only, Regime C feedback):")
    print(summary.round(0).to_string(index=False))

    (OUT / "final_results.json").write_text(json.dumps(results, indent=2))
    print(f"\nwrote final outputs to {OUT}")


if __name__ == "__main__":
    main()
