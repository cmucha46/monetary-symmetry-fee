"""Summary metrics for REGIME_RESULTS.md from regime_outputs/paths_*.csv."""
import json
from pathlib import Path
import pandas as pd

OUT = Path(__file__).parent / "regime_outputs"
Q = pd.period_range("2027Q1", "2036Q4", freq="Q")


def load(runid):
    df = pd.read_csv(OUT / f"paths_{runid}.csv", index_col="period")
    df.index = pd.PeriodIndex(df.index, freq="Q")
    return df


def fy_sum(series_sa):
    """Sum a SAAR flow deviation over FY2028-FY2036 quarters -> $B."""
    tot = 0.0
    for q, v in series_sa.items():
        fy = q.year + (1 if q.quarter == 4 else 0)
        if 2028 <= fy <= 2036:
            tot += v / 4.0
    return tot


def metrics(runid, baseid):
    d, b = load(runid), load(baseid)
    post = slice(pd.Period("2030Q1"), pd.Period("2036Q4"))
    trans = slice(pd.Period("2027Q4"), pd.Period("2029Q4"))
    m = {}
    m["rff_dev_mean_post"] = float(d.loc[post, "D_rff"].mean())
    m["rff_dev_min"] = float(d["D_rff"].min())
    m["rff_dev_2036Q4"] = float(d.loc[pd.Period("2036Q4"), "D_rff"])
    m["rff_level_min"] = float(d["L_rff"].min())
    if "fee_f_pct" in d:
        f = d["fee_f_pct"]
        m["fee_mean_post_pct"] = float(f.loc[post].mean())
        m["fee_2029Q4_pct"] = float(f.loc[pd.Period("2029Q4")])
        # combined charge p = rff + f vs baseline rff
        p_gap = (d["L_rff"] + f) - b["L_rff"]
        m["combined_charge_gap_mean_post"] = float(p_gap.loc[post].mean())
        m["offset_share_post"] = float(
            (-d.loc[post, "D_rff"]).mean() / f.loc[post].mean())
        m["receipts_total_bn"] = fy_sum(d["receipts_bn_saar"])
    for v in ["rme", "rcar", "rbbb", "rg10"]:
        m[f"{v}_dev_mean_post"] = float(d.loc[post, f"D_{v}"].mean())
    m["picxfe_dev_maxabs_post"] = float(d.loc[post, "D_picxfe"].abs().max())
    m["picxfe_dev_2036Q4"] = float(d.loc[pd.Period("2036Q4"), "D_picxfe"])
    m["picxfe_dev_maxabs_trans"] = float(d.loc[trans, "D_picxfe"].abs().max())
    m["lur_dev_max"] = float(d["D_lur"].max())
    m["lur_dev_2036Q4"] = float(d.loc[pd.Period("2036Q4"), "D_lur"])
    m["xgdp_dev_trough_pct"] = float(d["D_xgdp_pct"].min())
    m["cum_dgfsrpn_bn"] = fy_sum(d["D_gfsrpn"])
    m["cum_dgfintn_bn"] = fy_sum(d["D_gfintn"])
    m["dgfdbtnp_2036Q4_bn"] = float(d.loc[pd.Period("2036Q4"), "D_gfdbtnp"])
    return m


RUNS = [
    ("B_b100", "A_plain"), ("B_b075", "A_plain"), ("B_b050", "A_plain"),
    ("B_b100_k1", "A_plain"),
    ("C_b100", "A_plain"), ("C_b075", "A_plain"), ("C_b050", "A_plain"),
    ("C_b100_k1", "A_plain"),
    ("D_b100", "A_infl"), ("D_b075", "A_infl"),
    ("E_b100", "A_rec"), ("E_b075", "A_rec"),
]
out = {}
for mode in ["mce", "var"]:
    for runid, baseid in RUNS:
        key = f"{runid}_{mode}"
        try:
            out[key] = metrics(f"{runid}_{mode}", f"{baseid}_{mode}")
        except Exception as exc:
            out[key] = {"error": repr(exc)}
(OUT / "metrics.json").write_text(json.dumps(out, indent=1))
pd.set_option("display.width", 250)
for mode in ["mce", "var"]:
    print(f"\n===== {mode.upper()} =====")
    rows = {k: v for k, v in out.items() if k.endswith(mode) and "error" not in v}
    df = pd.DataFrame(rows).T
    cols = ["rff_dev_mean_post", "rff_dev_min", "fee_mean_post_pct",
            "combined_charge_gap_mean_post", "offset_share_post",
            "rme_dev_mean_post", "rcar_dev_mean_post", "rbbb_dev_mean_post",
            "rg10_dev_mean_post", "picxfe_dev_maxabs_post",
            "picxfe_dev_maxabs_trans", "lur_dev_max", "xgdp_dev_trough_pct",
            "cum_dgfsrpn_bn", "cum_dgfintn_bn", "dgfdbtnp_2036Q4_bn",
            "receipts_total_bn"]
    print(df[cols].round(3).to_string())
