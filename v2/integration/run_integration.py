"""Run the MSF v2 consolidation + grid Monte Carlo and write outputs.

Usage: python3 run_integration.py
Outputs (./outputs):
  fiscal_projection_central_<design>.csv -- annual table, central case
      (turnover=central, theta=1.0, erosion=0.10, beta=0.55), all taus
  monte_carlo_runs.csv                   -- every grid run, per tau
  monte_carlo_summary.csv                -- per-tau distribution summary
  results.json                           -- base status + headline numbers
Re-running after the unified-base cohort CSVs land (see inputs.json)
regenerates everything on the unified base with no code change.
"""
import json
from pathlib import Path

import pandas as pd

from consolidation import TAUS, base_status, consolidate, load_config
from monte_carlo import run_grid, summarize, summarize_by

HERE = Path(__file__).parent
OUT = HERE / "outputs"

CENTRAL = dict(turnover="central", theta=1.0, erosion_yr5=0.10, beta=0.55)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    config = load_config()
    status = base_status(config)
    headline = status["headline"]
    print(f"BASE STATUS: headline={headline}  unified_present="
          f"{status['unified_present']}  note: {status['note']}")

    # Central-case annual tables, both designs, all taus side by side.
    central_totals = {}
    for design in ("floating", "locked"):
        tables = consolidate(headline, design, CENTRAL["turnover"],
                             CENTRAL["theta"], CENTRAL["erosion_yr5"],
                             beta=CENTRAL["beta"], config=config)
        wide = None
        for tau in TAUS:
            df = tables[tau]
            keep = df.drop(columns=["tau"])
            if wide is None:
                wide = keep.drop(columns=["treasury_savings_gross_bn",
                                          "treasury_savings_consol_bn",
                                          "consolidated_net_bn"])
            wide[f"treasury_savings_consol_tau{tau}_bn"] = \
                df["treasury_savings_consol_bn"]
            wide[f"consolidated_net_tau{tau}_bn"] = df["consolidated_net_bn"]
        wide.to_csv(OUT / f"fiscal_projection_central_{design}.csv")
        central_totals[design] = {
            f"tau{tau}": float(wide[f"consolidated_net_tau{tau}_bn"].sum())
            for tau in TAUS}
        print(f"central case ({design}): " + "  ".join(
            f"tau={tau}: ${v:,.0f}B" for tau, v in
            ((t, central_totals[design][f'tau{t}']) for t in TAUS)))

    # Full grid enumeration.
    runs = run_grid(headline, config)
    runs.to_csv(OUT / "monte_carlo_runs.csv", index=False)
    summary = summarize(runs)
    summary.to_csv(OUT / "monte_carlo_summary.csv", index=False)
    print("\nMonte Carlo (grid enumeration) -- 10y consolidated, by tau:")
    print(summary.round({"mean_bn": 0, "median_bn": 0, "p25_bn": 0,
                         "p75_bn": 0, "min_bn": 0, "max_bn": 0})
          .to_string(index=False))
    for dim in ("design", "turnover", "erosion_yr5"):
        summarize_by(runs, dim).to_csv(
            OUT / f"monte_carlo_by_{dim}.csv", index=False)

    # Sensitivity base (loans-only when the headline is unified): central
    # totals + grid summary, written with a base suffix.
    sensitivity = status.get("sensitivity")
    sens_block = None
    if sensitivity in ("loans_only", "unified"):
        s_totals = {}
        for design in ("floating", "locked"):
            t = consolidate(sensitivity, design, CENTRAL["turnover"],
                            CENTRAL["theta"], CENTRAL["erosion_yr5"],
                            beta=CENTRAL["beta"], config=config)
            s_totals[design] = {
                f"tau{tau}": float(t[tau]["consolidated_net_bn"].sum())
                for tau in TAUS}
        s_runs = run_grid(sensitivity, config)
        s_runs.to_csv(OUT / f"monte_carlo_runs_{sensitivity}.csv",
                      index=False)
        s_summary = summarize(s_runs)
        s_summary.to_csv(OUT / f"monte_carlo_summary_{sensitivity}.csv",
                         index=False)
        sens_block = {"base": sensitivity,
                      "central_totals_10y_bn": s_totals,
                      "monte_carlo_summary": s_summary.to_dict("records")}
        print(f"\nsensitivity base ({sensitivity}) central floating: "
              + "  ".join(f"tau={tau}: ${s_totals['floating'][f'tau{tau}']:,.0f}B"
                          for tau in TAUS))

    results = {"base_status": status, "central_case": CENTRAL,
               "central_totals_10y_bn": central_totals,
               "monte_carlo_summary": summary.to_dict("records"),
               "sensitivity": sens_block}
    (OUT / "results.json").write_text(json.dumps(results, indent=2))
    print(f"\nwrote outputs to {OUT}")


if __name__ == "__main__":
    main()
