"""Steady-state-only OG-USA run (baseline or fiscal-stance reform).

Usage: python run_ss.py --out OUTPUT_DIR [--dalphaT 0.02] [--cit 0.32]
       [--payroll 0.025]
Uses OG-USA shipped default calibration (ogusa_default_parameters.json),
Calibration with NO estimation (shipped eta/zeta/e only), num_workers=1,
execute.runner(time_path=False) -> SS only.
"""
import argparse, json, os, time, resource, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--dalphaT", type=float, default=0.0)
    ap.add_argument("--cit", type=float, default=None)
    ap.add_argument("--payroll", type=float, default=None)
    args = ap.parse_args()

    t0 = time.time()
    import importlib.resources
    from ogcore.parameters import Specifications
    from ogcore import execute
    from ogusa.calibrate import Calibration
    from distributed import Client, LocalCluster

    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    p = Specifications(
        baseline=args.baseline,
        num_workers=1,
        baseline_dir=os.path.abspath("OUTPUT_BASELINE"),
        output_base=out,
    )
    with importlib.resources.open_text(
        "ogusa", "ogusa_default_parameters.json"
    ) as f:
        defaults = json.load(f)
    p.update_specifications(defaults)

    reform = {}
    if args.dalphaT:
        reform["alpha_T"] = [[v + args.dalphaT] for v in
                             [row[0] if isinstance(row, list) else row
                              for row in defaults["alpha_T"]]]
        # defaults alpha_T is a flat list; handle both shapes
        if not isinstance(defaults["alpha_T"][0], list):
            reform["alpha_T"] = [v + args.dalphaT for v in defaults["alpha_T"]]
    if args.cit is not None:
        reform["cit_rate"] = [[args.cit]]
    if args.payroll is not None:
        reform["tau_payroll"] = [[args.payroll]]
    if reform:
        print("REFORM UPDATES:", reform if "alpha_T" not in reform else
              {k: (v[:2] + ["..."] if k == "alpha_T" else v)
               for k, v in reform.items()})
        p.update_specifications(reform)

    c = Calibration(p)  # no estimation: shipped defaults only
    d = c.get_dict()
    keep = {k: v for k, v in d.items() if k in ("eta", "zeta", "e")}
    p.update_specifications(keep)
    print("Calibration dict keys applied:", list(keep.keys()))
    print("SS alpha_T[-1] =", float(p.alpha_T[-1]),
          " alpha_G[-1] =", float(p.alpha_G[-1]),
          " cit_rate =", float(p.cit_rate.flatten()[0]),
          " tau_payroll[0,0] =", float(p.tau_payroll.flatten()[0]),
          " tau_b[0] =", p.tau_b.flatten()[:3],
          " debt_ratio_ss =", float(p.debt_ratio_ss))

    cluster = LocalCluster(n_workers=1, threads_per_worker=1,
                           dashboard_address=None)
    client = Client(cluster)
    try:
        execute.runner(p, time_path=False, client=client)
    finally:
        client.close(); cluster.close()

    from ogcore.utils import safe_read_pickle
    ss = safe_read_pickle(os.path.join(out, "SS", "SS_vars.pkl"))
    keys = ["Y", "K", "L", "C", "w", "r", "r_p", "TR", "G", "D",
            "total_tax_revenue", "business_tax_revenue",
            "personal_tax_revenue", "I", "BQ", "agg_pension_outlays",
            "UBI_outlays", "I_g", "new_borrowing", "debt_service"]
    agg = {}
    for k in keys:
        if k in ss:
            try:
                agg[k] = float(ss[k])
            except Exception:
                agg[k] = str(type(ss[k]))
    Y = agg.get("Y")
    if Y:
        for num, name in [("total_tax_revenue", "rev_GDP"),
                          ("G", "G_GDP"), ("TR", "TR_GDP"),
                          ("D", "D_GDP"), ("C", "C_GDP"),
                          ("agg_pension_outlays", "pension_GDP")]:
            if num in agg:
                agg[name] = agg[num] / Y
        if "G_GDP" in agg and "TR_GDP" in agg:
            agg["GplusTR_GDP"] = agg["G_GDP"] + agg["TR_GDP"]
    agg["wall_seconds"] = time.time() - t0
    agg["peak_rss_MB_self"] = resource.getrusage(
        resource.RUSAGE_SELF).ru_maxrss / 1024.0
    agg["ss_keys"] = sorted(ss.keys())
    with open(os.path.join(out, "ss_aggregates.json"), "w") as f:
        json.dump(agg, f, indent=1)
    print(json.dumps(agg, indent=1))

if __name__ == "__main__":
    main()
