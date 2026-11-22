"""Empirical exhibit statistics: IOER/IORB vs 3-month bill (DTB3), FRED
daily data fetched 2026-11-22 from fredgraph CSVs (saved in exhibit_data/).
Administered rate = IOER through 2021-07-28, IORB from 2021-07-29 (the Fed
replaced IOER with IORB on 2021-07-29). Spread = DTB3 - administered (bp).
Beta: OLS of bill rate (levels, %) on administered rate (levels, %) with
intercept, per era. Correlations in levels and in daily changes.
Output: exhibit_stats.json in this directory."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
DATA = HERE / "exhibit_data"

ERAS = [
    ("ZLB (Dec 2008-Dec 2015)", "2008-12-16", "2015-12-15"),
    ("2016-19 hikes (through Feb 2020)", "2015-12-16", "2020-02-29"),
    ("Covid ZLB (Mar 2020-Mar 2022)", "2020-03-01", "2022-03-15"),
    ("2022-24 hikes", "2022-03-16", "2024-09-17"),
    ("Easing (Sep 2024-present)", "2024-09-18", "2100-01-01"),
]


def load() -> pd.DataFrame:
    ioer = pd.read_csv(DATA / "fred_IOER.csv", parse_dates=["observation_date"])
    iorb = pd.read_csv(DATA / "fred_IORB.csv", parse_dates=["observation_date"])
    dtb3 = pd.read_csv(DATA / "fred_DTB3.csv", parse_dates=["observation_date"])
    admin = pd.concat([
        ioer.rename(columns={"IOER": "admin"}),
        iorb.rename(columns={"IORB": "admin"})]).drop_duplicates(
        "observation_date").set_index("observation_date")["admin"]
    bill = dtb3.set_index("observation_date")["DTB3"]
    df = pd.DataFrame({"admin": admin, "bill": bill}).dropna()
    df = df[df.index >= "2008-10-09"]
    df["spread_bp"] = (df["bill"] - df["admin"]) * 100.0
    return df


def _event_beta(full: pd.DataFrame, lo, hi) -> dict:
    """Pass-through around administered-rate changes: for each day the
    administered rate changes, regress the bill's cumulative change over
    [t-1, t+5] trading days on the administered change (no intercept --
    a pure pass-through coefficient)."""
    d = full
    da = d["admin"].diff()
    idx = [i for i in range(1, len(d) - 5)
           if da.iloc[i] != 0 and lo <= d.index[i] <= hi]
    if len(idx) < 3:
        return {"n_events": len(idx), "event_beta_t1_t5": None}
    xs = np.array([da.iloc[i] for i in idx])
    ys = np.array([d["bill"].iloc[i + 5] - d["bill"].iloc[i - 1] for i in idx])
    idx20 = [i for i in idx if i >= 20]
    xs20 = np.array([da.iloc[i] for i in idx20])
    ys20 = np.array([d["bill"].iloc[i + 5] - d["bill"].iloc[i - 20]
                     for i in idx20])
    return {"n_events": len(idx),
            "event_beta_t1_t5": float((xs @ ys) / (xs @ xs)),
            "event_beta_t20_t5": float((xs20 @ ys20) / (xs20 @ xs20)),
            "mean_event_admin_change_bp": float(xs.mean() * 100),
            "mean_event_bill_change_bp": float(ys.mean() * 100)}


def stats(df: pd.DataFrame) -> dict:
    x, y = df["admin"].to_numpy(), df["bill"].to_numpy()
    if float(np.std(x)) < 0.01:  # administered rate effectively constant (ZLB: IOER pinned at 0.25%)
        corr, beta, alpha, corr_ch = None, None, None, None
    else:
        beta, alpha = (float(v) for v in np.polyfit(x, y, 1))
        corr = float(np.corrcoef(x, y)[0, 1])
        corr_ch = float(df["admin"].diff().corr(df["bill"].diff()))
    return {
        "n_days": int(len(df)),
        "start": str(df.index.min().date()), "end": str(df.index.max().date()),
        "corr_levels": corr,
        "corr_daily_changes": corr_ch,
        "beta_levels_ols": beta, "alpha_levels_ols": alpha,
        "mean_spread_bp": float(df["spread_bp"].mean()),
        "median_spread_bp": float(df["spread_bp"].median()),
        "sd_spread_bp": float(df["spread_bp"].std()),
    }


def main():
    df = load()
    out = {"full_sample": stats(df), "eras": {}}
    out["full_sample"].update(_event_beta(df, df.index.min(), df.index.max()))
    for name, a, b in ERAS:
        out["eras"][name] = stats(df.loc[a:b])
        out["eras"][name].update(_event_beta(
            df, pd.Timestamp(a), pd.Timestamp(b)))
    (HERE / "exhibit_stats.json").write_text(json.dumps(out, indent=2))
    for k, v in [("FULL", out["full_sample"]), *out["eras"].items()]:
        print(k, {kk: (round(vv, 3) if isinstance(vv, float) else vv)
                  for kk, vv in v.items()})


if __name__ == "__main__":
    main()
