import pandas as pd
from frbus import Frbus, load_data
from pathlib import Path
BASE = Path.home() / "workspace/monetary-symmetry"
DATA = BASE / "upstream/official/data_extract/data_only_package/LONGBASE.TXT"
XML = BASE / "upstream/official/pyfrbus_extract/pyfrbus/models/model.xml"
START, END = pd.Period("2027Q1"), pd.Period("2036Q4")
data = load_data(str(DATA))
data.loc[START:END, ["dfpdbt","dfpsrp"]] = 0
data.loc[START:END, "dfpex"] = 1
m = Frbus(str(XML), mce="mcap+wp")
print("poilr endo:", "poilr" in m.endo_names, "| poilr 2027-28:", 
      [round(float(data.loc[pd.Period(q),'poilr']),1) for q in ["2027Q4","2028Q2","2028Q4"]])
wa = m.init_trac(START, END, data)
base = m.solve(START, END, wa)
per = pd.period_range("2028Q1","2028Q4",freq="Q")
for size in [0.5, 1.0]:
    d = wa.copy(); d.loc[per, "picxfe_aerr"] = size
    s = m.solve(START, END, d)
    dev = s.loc[START:END,"picxfe"] - base.loc[START:END,"picxfe"]
    print(f"aerr +{size}: picxfe dev 2027Q4={dev[pd.Period('2027Q4')]:.2f} peak={dev.max():.2f}")
# oil shock: poilr is exo -> impose +50% path for 2028
if "poilr" not in m.endo_names:
    d = wa.copy()
    d.loc[per, "poilr"] = data.loc[per, "poilr"] * 1.5
    s = m.solve(START, END, d)
    for v in ["picxfe","rff","xgdp"]:
        if v == "xgdp":
            dv = 100*(s.loc[START:END,v]/base.loc[START:END,v]-1)
        else:
            dv = s.loc[START:END,v]-base.loc[START:END,v]
        print(f"oil +50% 2028: {v} dev peak/trough = {dv.max():.2f}/{dv.min():.2f}")
