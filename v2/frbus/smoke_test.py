"""v2 smoke test: endogenous-rff FRB/US solve with a constant private-rate wedge.

Design (differs from v1 Lane G on purpose):
  - rff is NOT exogenised: the model's own rule (LONGBASE default) sets it,
    so any lower funds path is found by the model, not imposed.
  - Wedge: rcar, rbbb, rme exogenised at baseline level + 0.50pp for
    2027Q1-2028Q4 (8q), baseline level thereafter (whole-solve exogenisation,
    Lane G discipline: level paths, never constant *_aerr).
  - Fiscal closure in both runs: dfpex=1, dfpdbt=0, dfpsrp=0.
  - No fee revenue fed in (ugfsrp untouched): this tests the credit-pricing
    leg only.
Window: 2027Q1-2031Q4 (20q), official Oct 2026 LONGBASE + official model.xml.
"""
import time, json
from pathlib import Path
import pandas as pd
from frbus import Frbus, load_data

BASE = Path.home() / "workspace/monetary-symmetry"
DATA = BASE / "upstream/official/data_extract/data_only_package/LONGBASE.TXT"
XML = BASE / "upstream/official/pyfrbus_extract/pyfrbus/models/model.xml"
START, END = pd.Period("2027Q1"), pd.Period("2031Q4")
TIGHT = slice(START, START + 7)
WEDGE = 0.50

t0 = time.time()
data = load_data(str(DATA))
data.loc[START:END, "dfpdbt"] = 0
data.loc[START:END, "dfpsrp"] = 0
data.loc[START:END, "dfpex"] = 1

# --- diagnostics: rule switches + key coefficients from LONGBASE
diag_cols = ["dmpintay", "dmptay", "dmptlr", "dmpalt", "dmprr", "dmpex", "rffmin",
             "y_rcar_4", "y_rcar_5", "y_rcar_6",
             "y_rme_1", "y_rme_2", "y_rme_3", "y_rme_4", "y_rme_5",
             "y_rbbbp_1", "y_rbbbp_2", "y_rbbbp_3",
             "y_ugfsrp_1", "y_ugfsrp_2",
             "y_rgw_1", "y_rgw_2", "y_rgw_3", "y_rgw_4"]
diag = {c: (float(data.loc[START, c]) if c in data.columns else None) for c in diag_cols}
print("DIAG", json.dumps(diag, indent=1))

# --- baseline: everything endogenous except nothing; rff from the rule
m_base = Frbus(str(XML))
wa = m_base.init_trac(START, END, data)
base = m_base.solve(START, END, wa)
print("baseline solved", round(time.time() - t0, 1), "s")

# --- wedge run: exogenise the three private rates at baseline + wedge
m_w = Frbus(str(XML)); m_w.exogenize(["rcar", "rbbb", "rme"])
wa2 = m_w.init_trac(START, END, data)
d = wa2.copy()
for v in ["rcar", "rbbb", "rme"]:
    d.loc[START:END, v] = base.loc[START:END, v]
    d.loc[TIGHT, v] = base.loc[TIGHT, v] + WEDGE
wed = m_w.solve(START, END, d)
print("wedge solved", round(time.time() - t0, 1), "s")

rows = []
for p in pd.period_range(START, END, freq="Q"):
    r = {"period": str(p)}
    for v in ["rff", "xgdp", "lur", "picxfe", "rg10", "rcar", "rbbb", "rme", "rccd"]:
        b, w = float(base.loc[p, v]), float(wed.loc[p, v])
        r[v + "_dev"] = (100.0 * (w / b - 1.0)) if v == "xgdp" else (w - b)
    rows.append(r)
df = pd.DataFrame(rows)
pd.set_option("display.width", 250)
print(df.round(3).to_string(index=False))
summ = {
    "rff_dev_mean_8q_pp": float(df["rff_dev"].iloc[:8].mean()),
    "rff_dev_min_pp": float(df["rff_dev"].min()),
    "xgdp_trough_pct": float(df["xgdp_dev"].min()),
    "lur_peak_pp": float(df["lur_dev"].max()),
    "picxfe_min_pp": float(df["picxfe_dev"].min()),
    "rg10_dev_mean_8q_pp": float(df["rg10_dev"].iloc[:8].mean()),
    "rccd_dev_mean_8q_pp": float(df["rccd_dev"].iloc[:8].mean()),
}
print("SUMMARY", json.dumps(summ, indent=1))
df.to_csv(Path(__file__).parent / "smoke_test_deviations.csv", index=False)
print("wall", round(time.time() - t0, 1), "s")
