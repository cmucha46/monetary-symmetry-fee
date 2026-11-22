"""Run Lane 4: maturity-dependent tau correction.
Outputs (this directory):
  coverage_surface_corrected.csv  -- tau_long x scenario x spread (growing)
  coverage_annual_corrected.csv   -- annual tables, headline spread cells +
                                     spread sensitivities (central)
  corrected_summary.json          -- everything CORRECTION_TAU_MATURITY.md cites
"""
import json
from pathlib import Path

import pandas as pd

import consolidation_combined as CC
import consolidation_tau_maturity as CT

HERE = Path(__file__).parent
SCENARIOS = ("low", "central", "high_stress")


def main():
    ctx = CT.build_context_corrected()
    rows, annual_frames = [], []
    annual_by_cell = {}
    for tau_long in CT.TAU_LONGS:
        for scen in SCENARIOS:
            for ds in CT.SPREADS:
                df = CT.coverage_table_corrected(tau_long, ds, scen, ctx)
                fs = CC.first_shortfalls(df)
                contrib = float(df["fee_contribution_bn"].sum())
                resid = float(df["mfa_residual_bn"].sum())
                rows.append({
                    "mode": "growing", "tau_long": tau_long,
                    "spread_change_pp": ds, "scenario": scen,
                    "net_receipts_bn": float(df["net_receipts_bn"].sum()),
                    "frbus_drag_bn": float(df["frbus_drag_bn"].sum()),
                    "delta_remittances_bn": float(df["delta_remittances_bn"].sum()),
                    "front_savings_bn": float(df["front_savings_bn"].sum()),
                    "long_savings_bn": float(df["long_savings_bn"].sum()),
                    "interest_savings_bn": float(df["interest_savings_bn"].sum()),
                    "fee_contribution_bn": contrib,
                    "mfa_residual_bn": resid,
                    "coverage_margin_bn": contrib - resid,
                    "financed": bool(contrib - resid >= 0),
                    "first_cum_negative_year": fs["first_cum_negative_year"],
                    "first_annual_shortfall_year": fs["first_annual_shortfall_year"],
                    "iterations": int(df.attrs.get("iterations", 0)),
                    "combined_debt_2036_bn": float(df["combined_debt_bn"].iloc[-1]),
                })
                if ds == 0.0 or scen == "central":
                    d2 = df.reset_index().rename(columns={"index": "fy"})
                    d2.insert(0, "scenario", scen)
                    d2.insert(0, "spread_change_pp", ds)
                    d2.insert(0, "tau_long", tau_long)
                    annual_frames.append(d2)
                if ds == 0.0:
                    annual_by_cell[f"tauL{tau_long}_{scen}"] = (
                        df.reset_index().to_dict("records"))
    surface = pd.DataFrame(rows)
    surface.to_csv(HERE / "coverage_surface_corrected.csv", index=False)
    pd.concat(annual_frames, ignore_index=True).to_csv(
        HERE / "coverage_annual_corrected.csv", index=False)

    restate = CT.v2_restatement(ctx)
    cbo = CT.cbo_corrected(ctx)
    summary = {"surface": rows, "v2_restatement": restate, "cbo_corrected": cbo,
               "w_front": CT.W_FRONT, "annual_headline": annual_by_cell}
    (HERE / "corrected_summary.json").write_text(json.dumps(summary, indent=2))

    h = surface[surface["spread_change_pp"] == 0.0]
    print(h[["tau_long", "scenario", "front_savings_bn", "long_savings_bn",
             "interest_savings_bn", "fee_contribution_bn",
             "coverage_margin_bn", "financed"]].round(0).to_string(index=False))
    print("\nSPREAD SENSITIVITY (central):")
    c = surface[surface["scenario"] == "central"]
    print(c[["tau_long", "spread_change_pp", "interest_savings_bn",
             "coverage_margin_bn", "financed"]].round(0).to_string(index=False))
    print("\nV2 RESTATEMENT (flat):")
    for r in restate:
        print(f" tau_long={r['tau_long']}: interest {r['v2_scalar_interest_bn']:,.0f} "
              f"-> {r['corrected_interest_bn']:,.0f} (front {r['corrected_front_bn']:,.0f} "
              f"+ long {r['corrected_long_bn']:,.0f}); total {r['v2_total_scalar_bn']:,.0f} "
              f"-> {r['v2_total_corrected_bn']:,.0f}")
    print("\nCBO corrected:", {k: round(v, 2) for k, v in cbo.items()})


if __name__ == "__main__":
    main()
