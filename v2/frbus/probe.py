import time, json
import pandas as pd
from frbus import Frbus, load_data
from pathlib import Path

BASE = Path.home() / "workspace/monetary-symmetry"
DATA = BASE / "upstream/official/data_extract/data_only_package/LONGBASE.TXT"
XML = BASE / "upstream/official/pyfrbus_extract/pyfrbus/models/model.xml"
START, END = pd.Period("2027Q1"), pd.Period("2036Q4")

data = load_data(str(DATA))
data.loc[START:END, "dfpdbt"] = 0
data.loc[START:END, "dfpsrp"] = 0
data.loc[START:END, "dfpex"] = 1

m = Frbus(str(XML))
print("reqp endo:", "reqp" in m.endo_names, "| rbbbp endo:", "rbbbp" in m.endo_names,
      "| picxfe endo:", "picxfe" in m.endo_names, "| ugfsrp endo:", "ugfsrp" in m.endo_names)

t0 = time.time()
wa = m.init_trac(START, END, data)
base = m.solve(START, END, wa)
t_var = time.time() - t0
print(f"VAR baseline 40q: {t_var:.1f}s")
chk = {}
for v in ["rff", "picxfe", "lur", "xgdpn"]:
    chk[v] = float((base.loc[START:END, v] - data.loc[START:END, v]).abs().max())
print("max |solve - data| on window:", chk)

# shock mechanics: picxfe_aerr +2 for 2028 (post-init_trac injection)
d2 = wa.copy()
per = pd.period_range("2028Q1", "2028Q4", freq="Q")
d2.loc[per, "picxfe_aerr"] = 2.0
t0 = time.time()
shk = m.solve(START, END, d2)
print(f"VAR shocked solve: {time.time()-t0:.1f}s")
dev = pd.DataFrame({
    "picxfe_dev": shk.loc[START:END, "picxfe"] - base.loc[START:END, "picxfe"],
    "rff_dev": shk.loc[START:END, "rff"] - base.loc[START:END, "rff"],
    "lur_dev": shk.loc[START:END, "lur"] - base.loc[START:END, "lur"],
})
print(dev.loc["2027Q4":"2029Q4"].round(3).to_string())

# MCE timing
t0 = time.time()
mm = Frbus(str(XML), mce="mcap+wp")
wam = mm.init_trac(START, END, data)
basem = mm.solve(START, END, wam)
t_mce = time.time() - t0
print(f"MCE baseline 40q (incl. trac): {t_mce:.1f}s")
print("MCE vs VAR rff max dev:", float((basem.loc[START:END,'rff']-base.loc[START:END,'rff']).abs().max()))
print("MCE vs VAR picxfe max dev:", float((basem.loc[START:END,'picxfe']-base.loc[START:END,'picxfe']).abs().max()))
