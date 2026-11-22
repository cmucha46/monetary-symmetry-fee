"""Run Lane 3: combined-closure coverage surface + CBO exhibit.
Outputs (this directory):
  coverage_surface.csv        -- tau x scenario x mode headline rows
  coverage_annual_<mode>.csv  -- annual tables, all tau x scenario
  cbo_reconciliation.json     -- Task 2 exhibit numbers
  combined_summary.json       -- everything CONSOLIDATION.md cites
"""
import json
from pathlib import Path

import pandas as pd

import consolidation_combined as CC

HERE = Path(__file__).parent
SCENARIOS = ("low", "central", "high_stress")


def main():
    ctx = CC.build_context()
    surface_rows, annual = [], {}
    erosion = {}
    # growing-baseline (no plan) savings per tau, for self-erosion
    base_path = ctx["base_path"]
    avg_base, prev = {}, CC.MARKETABLE_2026
    for t in CC.YEARS:
        avg_base[t] = (prev + float(base_path.loc[t, "baseline_marketable_debt_bn"])) / 2
        prev = float(base_path.loc[t, "baseline_marketable_debt_bn"])
    noplan = {tau: CC.savings_on_path(avg_base, ctx["dys"][tau]) for tau in CC.TAUS}

    for mode in ("growing", "flat"):
        frames = []
        for tau in CC.TAUS:
            for scen in SCENARIOS:
                df = CC.coverage_table(tau, scen, mode, ctx)
                df = df.reset_index().rename(columns={"index": "fy"})
                df.insert(0, "scenario", scen)
                df.insert(0, "mode", mode)
                df.insert(0, "tau", tau)
                frames.append(df)
                fs = CC.first_shortfalls(df.set_index("fy"))
                contrib = float(df["fee_contribution_bn"].sum())
                resid = float(df["mfa_residual_bn"].sum())
                surface_rows.append({
                    "mode": mode, "tau": tau, "scenario": scen,
                    "net_receipts_bn": float(df["net_receipts_bn"].sum()),
                    "gross_collections_bn": float(df["gross_collections_bn"].sum()),
                    "frbus_drag_bn": float(df["frbus_drag_bn"].sum()),
                    "interest_savings_bn": float(df["interest_savings_bn"].sum()),
                    "delta_remittances_bn": float(df["delta_remittances_bn"].sum()),
                    "fee_contribution_bn": contrib,
                    "mfa_residual_bn": resid,
                    "coverage_margin_bn": contrib - resid,
                    "financed": bool(contrib - resid >= 0),
                    "first_cum_negative_year": fs["first_cum_negative_year"],
                    "first_annual_shortfall_year": fs["first_annual_shortfall_year"],
                    "iterations": int(df.attrs.get("iterations", 0)),
                    "combined_debt_2036_bn": (float(df["combined_debt_bn"].iloc[-1])
                                              if mode == "growing" else None),
                })
                if mode == "growing":
                    sav = float(df["interest_savings_bn"].sum())
                    erosion[(tau, scen)] = {
                        "combined_savings_bn": sav,
                        "banked_flat_savings_bn": float(ctx["savings_flat"][tau].sum()),
                        "vs_banked_bn": sav - float(ctx["savings_flat"][tau].sum()),
                        "growing_noplan_savings_bn": float(noplan[tau].sum()),
                        "self_erosion_bn": float(noplan[tau].sum()) - sav,
                    }
        annual[mode] = pd.concat(frames, ignore_index=True)
        annual[mode].to_csv(HERE / f"coverage_annual_{mode}.csv", index=False)

    surface = pd.DataFrame(surface_rows)
    surface.to_csv(HERE / "coverage_surface.csv", index=False)

    exhibit = CC.cbo_exhibit(ctx)
    (HERE / "cbo_reconciliation.json").write_text(json.dumps(exhibit, indent=2))
    summary = {"surface": surface_rows,
               "erosion": {f"tau{tau}_{s}": v for (tau, s), v in erosion.items()},
               "cbo_exhibit": exhibit,
               "baseline_path": ctx["base_path"].reset_index().to_dict("records")}
    (HERE / "combined_summary.json").write_text(json.dumps(summary, indent=2))

    pd.set_option("display.width", 250)
    g = surface[surface["mode"] == "growing"]
    print(g[["tau", "scenario", "fee_contribution_bn", "mfa_residual_bn",
             "coverage_margin_bn", "financed", "first_cum_negative_year",
             "first_annual_shortfall_year"]].round(0).to_string(index=False))
    print("\nEROSION (growing combined vs banked flat; self-erosion vs growing no-plan):")
    for (tau, s), v in sorted(erosion.items()):
        print(f" tau={tau} {s}: combined ${v['combined_savings_bn']:,.0f}B | "
              f"banked ${v['banked_flat_savings_bn']:,.0f}B | vs banked "
              f"${v['vs_banked_bn']:+,.0f}B | no-plan growing "
              f"${v['growing_noplan_savings_bn']:,.0f}B | self-erosion "
              f"${v['self_erosion_bn']:,.0f}B")
    print("\nCBO exhibit:", {k: round(v, 2) for k, v in exhibit.items()})


if __name__ == "__main__":
    main()
