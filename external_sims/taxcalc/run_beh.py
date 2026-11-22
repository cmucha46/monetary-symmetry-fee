import json, csv
from taxcalc import Policy, Records, Calculator, behresp
beh=[]
for year in range(2028,2037):
    cb = Calculator(policy=Policy(), records=Records.cps_constructor())
    pr = Policy(); pr.implement_reform(Policy.read_json_reform("repeal201_from2028.json"))
    cr = Calculator(policy=pr, records=Records.cps_constructor())
    cb.advance_to_year(year); cr.advance_to_year(year)
    df1, df2 = behresp.response(cb, cr, {"sub": 0.25})
    base=(df1["iitax"]*df1["s006"]).sum()
    ref=(df2["iitax"]*df2["s006"]).sum()
    print("BEH",year,f"base=${base/1e9:.1f}B reform_beh=${ref/1e9:.1f}B diff=${(ref-base)/1e9:.1f}B",flush=True)
    beh.append({"year":year,"baseline_iitax_billions":base/1e9,"reform_behresp_iitax_billions":ref/1e9,"diff_revenue_billions":(ref-base)/1e9})
json.dump(beh, open("results_behresp_sub025.json","w"), indent=2)
with open("results_behresp_sub025.csv","w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=list(beh[0].keys())); w.writeheader(); w.writerows(beh)
print("BEH TOTAL $B", sum(r["diff_revenue_billions"] for r in beh))
