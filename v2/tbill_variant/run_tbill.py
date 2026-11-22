"""Run the T-Bill Variant study.
Outputs (this directory):
  migration_path.csv      -- bill stock/share, WAM, bucket balances by FY
                             (central, tau_long=0.5, spread asymptote 0)
  interest_lines.csv      -- Lane 4 base vs engine base vs variant,
                             by tau_long x spread scenario (central)
  spread_grid.csv         -- variant gain by S_inf x tau_long (central)
  coverage_restated.csv   -- combined-study margins + variant increment
                             (central + high-stress, all spread scenarios)
  term_premium.csv        -- SEPARATE exhibit: shortening-only saving
  stress.csv              -- Regime C/D/E interest bill by structure
  tbill_summary.json      -- everything TBILL_VARIANT.md cites
"""
import json
from pathlib import Path

import pandas as pd

import tbill_variant as TV  # first: sets sys.path for the Lane 3/4 imports
import consolidation_combined as CC
import consolidation_tau_maturity as CT

HERE = Path(__file__).parent
TAUS = TV.TAU_LONGS
S_INFS = (0.0, 25.0, 50.0, 100.0)
HEADLINE_S_INF = 50.0


def lane4_margins(ctx):
    """Lane 4 published coverage margins + interest (spread 0, growing)."""
    out = {}
    for tau in TAUS:
        for scen in ("central", "high_stress", "low"):
            df = CT.coverage_table_corrected(tau, 0.0, scen, ctx)
            out[(tau, scen)] = {
                "interest_bn": float(df["interest_savings_bn"].sum()),
                "margin_bn": float(df["cum_margin_bn"].iloc[-1]),
            }
    return out


def main():
    ctx = TV.build_context()
    L4 = lane4_margins(ctx)
    summary = {"lane4": {f"{t}|{s}": v for (t, s), v in L4.items()}}

    # --- 1. Interest lines + spread grid (central) -------------------------
    line_rows, grid_rows = [], []
    gains = {}   # (tau, s_inf, scen) -> gain dict
    for tau in TAUS:
        for scen in ("central", "high_stress"):
            for s in S_INFS:
                g = TV.variant_gain(tau, scen, ctx, s_inf_bp=s)
                gains[(tau, s, scen)] = g
                if scen == "central":
                    grid_rows.append({
                        "tau_long": tau, "s_inf_bp": s,
                        "engine_base_interest_bn": g["base_interest_bn"],
                        "variant_interest_bn": g["variant_interest_bn"],
                        "gain_bn": g["gain_bn"]})
    for tau in TAUS:
        g0 = gains[(tau, 0.0, "central")]
        row = {"tau_long": tau,
               "lane4_interest_bn": L4[(tau, "central")]["interest_bn"],
               "engine_base_interest_bn": g0["base_interest_bn"],
               "engine_vs_lane4_pct": 100.0 * (g0["base_interest_bn"]
                                       / L4[(tau, "central")]["interest_bn"]
                                       - 1.0)}
        for s in S_INFS:
            row[f"variant_interest_s{int(s)}_bn"] = \
                gains[(tau, s, "central")]["variant_interest_bn"]
            row[f"gain_s{int(s)}_bn"] = gains[(tau, s, "central")]["gain_bn"]
        line_rows.append(row)
    pd.DataFrame(line_rows).to_csv(HERE / "interest_lines.csv", index=False)
    pd.DataFrame(grid_rows).to_csv(HERE / "spread_grid.csv", index=False)
    summary["interest_lines"] = line_rows

    # gamma convexity check at S_inf = 50
    g2 = TV.variant_gain(0.5, "central", ctx, s_inf_bp=50.0, gamma=2.0)
    summary["gamma2_check_tau05_s50"] = g2["gain_bn"]

    # --- 2. Migration path (central, tau_long=0.5, S_inf=0) ----------------
    var = gains[(0.5, 0.0, "central")]["variant"]
    mig = var["run"].copy()
    mig.insert(0, "fy", mig.index)
    mig.to_csv(HERE / "migration_path.csv", index=False)
    summary["migration"] = {
        t: {"bill_stock_bn": float(mig.loc[mig.fy == t, "bill_stock_bn"].iloc[0]),
            "bill_share": float(mig.loc[mig.fy == t, "bill_share"].iloc[0]),
            "wam_months": float(mig.loc[mig.fy == t, "wam_months"].iloc[0]),
            "avg_rate_pct": float(mig.loc[mig.fy == t, "avg_rate"].iloc[0]) * 100}
        for t in TV.YEARS}

    # --- 3. Break-even spreads (central) ------------------------------------
    be = {}
    for tau in TAUS:
        be[tau] = TV.breakeven_spread(tau, "central", ctx)
    summary["breakeven_dspread_pp"] = {str(k): v for k, v in be.items()}
    summary["breakeven_level_vs_iorb_bp"] = {
        str(k): -14.0 + v * 100.0 for k, v in be.items()}  # median anchor

    # --- 4. Coverage restatement --------------------------------------------
    cov_rows = []
    for tau in TAUS:
        for scen in ("central", "high_stress"):
            for s in S_INFS:
                gain = gains[(tau, s, scen)]["gain_bn"]
                cov_rows.append({
                    "tau_long": tau, "scenario": scen, "s_inf_bp": s,
                    "lane4_margin_bn": L4[(tau, scen)]["margin_bn"],
                    "variant_gain_bn": gain,
                    "restated_margin_bn": L4[(tau, scen)]["margin_bn"] + gain,
                    "financed": bool(L4[(tau, scen)]["margin_bn"] + gain >= 0)})
    pd.DataFrame(cov_rows).to_csv(HERE / "coverage_restated.csv", index=False)
    summary["coverage_restated"] = cov_rows

    # --- 5. Term-premium exhibit (separate; never in coverage) --------------
    tp_rows = []
    for tp in (50.0, 100.0):
        s = TV.term_premium_exhibit(0.5, "central", ctx, tp)
        tp_rows.append({"tp_bp": tp, "cumulative_bn": float(s.sum()),
                        **{f"fy{t}": float(s[t]) for t in TV.YEARS}})
    pd.DataFrame(tp_rows).to_csv(HERE / "term_premium.csv", index=False)
    summary["term_premium"] = tp_rows

    # --- 6. Stress: Regimes C / D / E (tau_long = 0.5) -----------------------
    stress = {}
    srows = []
    for reg in ("C", "D", "E"):
        st = TV.stress_interest(reg, 0.5, ctx)
        stress[reg] = st
        for name in ("current", "migrated"):
            ic = st[name]["interest_consol_bn"]
            srows.append({"regime": reg, "structure": name,
                          "cum_interest_consol_bn": float(ic.sum()),
                          "peak_year_interest_bn": float(ic.max()),
                          "peak_year": int(ic.idxmax()),
                          **{f"fy{t}": float(ic[t]) for t in TV.YEARS}})
    pd.DataFrame(srows).to_csv(HERE / "stress.csv", index=False)
    d_extra = {name: float(stress["D"][name]["interest_consol_bn"].sum()
                           - stress["C"][name]["interest_consol_bn"].sum())
               for name in ("current", "migrated")}
    e_extra = {name: float(stress["E"][name]["interest_consol_bn"].sum()
                           - stress["C"][name]["interest_consol_bn"].sum())
               for name in ("current", "migrated")}
    summary["stress"] = {"D_extra_vs_C_bn": d_extra, "E_extra_vs_C_bn": e_extra,
                         "rows": srows,
                         "shock_increment_pp": {
                             r: {str(t): v * 100 for t, v in
                                 TV.frbus_shock_increment(r).items()}
                             for r in ("D", "E")},
                         "avg_rate_D_pct": {
                             name: {str(t): float(stress["D"][name]
                                                  ["avg_rate"][t]) * 100
                                    for t in TV.YEARS}
                             for name in ("current", "migrated")},
                         "avg_rate_C_pct": {
                             name: {str(t): float(stress["C"][name]
                                                  ["avg_rate"][t]) * 100
                                    for t in TV.YEARS}
                             for name in ("current", "migrated")}}
    # annual variant savings at the headline spread scenario (tau_long=0)
    g50 = gains[(0.0, HEADLINE_S_INF, "central")]["variant"]
    summary["variant_annual_s50_tau0"] = {
        str(t): float(g50["savings"][t]) for t in TV.YEARS}
    g0 = gains[(0.0, 0.0, "central")]["variant"]
    summary["variant_annual_s0_tau0"] = {
        str(t): float(g0["savings"][t]) for t in TV.YEARS}

    # --- 7. Cadence -----------------------------------------------------------
    summary["cadence_52wk"] = TV.cadence_52wk()
    summary["assumptions"] = TV.ASSUMPTIONS

    (HERE / "tbill_summary.json").write_text(json.dumps(summary, indent=2))

    # --- console digest -------------------------------------------------------
    print("INTEREST LINES (central, $B):")
    _df = pd.DataFrame(line_rows)
    print(_df.round({c: 0 for c in _df.columns if c != "tau_long"})
          .to_string(index=False))
    print("\nBREAK-EVEN dspread (pp):", {k: round(v, 3) for k, v in be.items()})
    print("\nMIGRATION (bill share / WAM mo):")
    for t in TV.YEARS:
        m = summary["migration"][t]
        print(f"  FY{t}: share {m['bill_share']:.3f}  stock "
              f"${m['bill_stock_bn']:,.0f}B  WAM {m['wam_months']:.1f}mo")
    print("\nCOVERAGE (headline S_inf=50):")
    for r in cov_rows:
        if r["s_inf_bp"] == HEADLINE_S_INF:
            print(f"  tau={r['tau_long']} {r['scenario']}: "
                  f"{r['lane4_margin_bn']:+,.0f} -> {r['restated_margin_bn']:+,.0f}")
    print("\nTERM PREMIUM (separate):",
          [(r['tp_bp'], round(r['cumulative_bn'])) for r in tp_rows])
    print("\nSTRESS D extra vs C ($B):", {k: round(v) for k, v in d_extra.items()})
    print("STRESS E extra vs C ($B):", {k: round(v) for k, v in e_extra.items()})
    print("\nCADENCE:", {k: round(v, 3) for k, v in
                          summary['cadence_52wk'].items()})


if __name__ == "__main__":
    main()
