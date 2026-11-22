import json, re, pathlib, taxcalc
from taxcalc import Policy

# Load 2017_law reform text, strip // comments for key list
p = pathlib.Path("venv/lib/python3.12/site-packages/taxcalc/reforms/2017_law.json")
txt = p.read_text()
keys=[]
for line in txt.splitlines():
    m=re.match(r'\s*"([^"]+)":', line)
    if m and not line.strip().startswith("//"):
        keys.append(m.group(1))
keys=list(dict.fromkeys(keys))
print("2017_law keys", len(keys), keys)

# Policy with 2017_law applied (from its stated years)
pol17 = Policy()
reform = Policy.read_json_reform(str(p))
pol17.implement_reform(reform)
pol17.set_year(2028)
vals={}
for k in keys:
    if k=="parameter_indexing_CPI_offset":
        continue
    # indexed flag pseudo-params are not attributes
    if k.endswith("-indexed"):
        vals[k]=False
        continue
    try:
        v=getattr(pol17, k)
    except Exception as e:
        print("missing attr", k, e); continue
    # v is numpy array
    import numpy as np
    arr=np.asarray(v)
    if arr.size==1:
        vals[k]=float(arr.flat[0])
    elif arr.size==5:
        vals[k]=[float(x) for x in arr.flat]
    elif arr.size==4:
        vals[k]=[float(x) for x in arr.flat]
    else:
        vals[k]=[float(x) for x in arr.flat]
        print("size",k,arr.shape,vals[k])
    print(k, vals[k])

# Build 2028 reform
reform2028={}
for k,v in vals.items():
    reform2028[k]={"2028": v}
# CPI offset: revert chained indexing prospectively - set as in 2017_law (0.0025) at 2028
# NOTE will test; keep separate flag
reform2028["parameter_indexing_CPI_offset"]={"2028": 0.0025}
# OBBBA removals (2028 only matters for expiring ones; permanent ones set from 2028)
reform2028["TipIncomeDed_c"]={"2028": 0}
reform2028["OvertimeIncomeDed_c"]={"2028": [0,0,0,0,0]}
reform2028["SeniorDed_c"]={"2028": 0}
reform2028["AutoLoanInterestDed_c"]={"2028": 0}
reform2028["ID_Charity_frt"]={"2028": 0}
reform2028["STD_charity_ded_nonitemizers_max"]={"2028": [0,0,0,0,0]}
reform2028["PT_qbid_min_ded"]={"2028": 0}
# Also ensure QBID zero (already via PT_qbid_rt)
# Write with header comments like taxcalc format
header="""// Title: Medicare for America Sec.201 - revert individual TCJA provisions to pre-TCJA 2017 law effective 2028
// Baseline: OBBBA current law (taxcalc 6.8.5 policy_current_law.json)
// Method: 2028 values extracted from a Policy implementing shipped reforms/2017_law.json and set_year(2028),
//         i.e. 2017 nominal values inflation-indexed forward by taxcalc's own unchained CPI-U mechanism
//         (parameter_indexing_CPI_offset=0.0025 in 2017_law). Those extracted 2028 values are set at 2028 here;
//         taxcalc indexing then carries them forward 2029-2036.
// Plus: OBBBA tip/overtime/senior/auto deductions zeroed for 2028, OBBBA charity floor and nonitemizer charity zeroed,
//         OBBBA PT minimum QBID zeroed. SALT cap removed via ID_AllTaxes_c=9e99 (from 2017_law extraction).
"""
pathlib.Path("repeal201_from2028.json").write_text(header+json.dumps(reform2028, indent=2))
print("wrote repeal201_from2028.json with", len(reform2028), "params")
