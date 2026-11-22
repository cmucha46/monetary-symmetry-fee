import taxcalc, json, csv, pathlib, sys
from taxcalc import Policy, Records, Calculator

# Test reform implementation
pol_base = Policy()
pol_reform = Policy()
reform = Policy.read_json_reform("repeal201_from2028.json")
print("reform dict keys", len(reform))
pol_reform.implement_reform(reform)
print("warnings:", pol_reform.parameter_warnings if hasattr(pol_reform,'parameter_warnings') else 'n/a')
print("errors:", pol_reform.parameter_errors if hasattr(pol_reform,'parameter_errors') else 'n/a')
pol_reform.set_year(2028)
print("reform STD 2028", pol_reform.STD, "II_em", pol_reform.II_em, "SALT", pol_reform.ID_AllTaxes_c)

recs = Records.cps_constructor()
print("records start year", recs.current_year)

results=[]
for year in range(2028, 2037):
    # fresh calculators each year using advance pattern: create calc, advance
    calc_base = Calculator(policy=Policy(), records=Records.cps_constructor())
    calc_reform = Calculator(policy=pol_reform if False else None, records=None) if False else None
    # Simpler: build reform policy fresh each loop
    pr = Policy(); pr.implement_reform(Policy.read_json_reform("repeal201_from2028.json"))
    calc_reform = Calculator(policy=pr, records=Records.cps_constructor())
    calc_base.advance_to_year(year); calc_base.calc_all()
    calc_reform.advance_to_year(year); calc_reform.calc_all()
    # iitax is individual income tax liability; use weighted sum
    import numpy as np
    base = (calc_base.array("iitax") * calc_base.array("s006")).sum()
    ref = (calc_reform.array("iitax") * calc_reform.array("s006")).sum()
    # also combined? keep iitax only, note payroll separate unchanged
    diff = ref - base
    print(year, f"base=${base/1e9:.1f}B reform=${ref/1e9:.1f}B diff=${diff/1e9:.1f}B")
    results.append({"year": year, "baseline_iitax_billions": base/1e9, "reform_iitax_billions": ref/1e9, "diff_revenue_billions": diff/1e9})
    sys.stdout.flush()

with open("results_static.json","w") as f: json.dump(results,f,indent=2)
with open("results_static.csv","w",newline="") as f:
    w=csv.DictWriter(f, fieldnames=list(results[0].keys())); w.writeheader(); w.writerows(results)
print("TOTAL 2028-36 diff $B", sum(r["diff_revenue_billions"] for r in results))

# Behavioral response variant: Recipe 2 pattern using behresp
# taxcalc.behresp.response / Calculator with behresp? In 6.8, use taxcalc.behresp.response(calc_base, calc_reform, sub=0.25 ...)
try:
    from taxcalc import behresp
    print("behresp functions:", [x for x in dir(behresp) if not x.startswith('_')])
    # Inspect signature
    import inspect; print(inspect.signature(behresp.response))
    beh=[]
    for year in range(2028, 2037):
        cb = Calculator(policy=Policy(), records=Records.cps_constructor())
        pr = Policy(); pr.implement_reform(Policy.read_json_reform("repeal201_from2028.json"))
        cr = Calculator(policy=pr, records=Records.cps_constructor())
        cb.advance_to_year(year); cr.advance_to_year(year)
        # behresp.response returns calc with adjusted income? Follow recipe: 
        cr_beh = behresp.response(cb, cr, {"sub": [0.25]})
        cb.calc_all(); cr_beh.calc_all()
        import numpy as np
        base = (cb.array("iitax") * cb.array("s006")).sum()
        ref = (cr_beh.array("iitax") * cr_beh.array("s006")).sum()
        diff = ref-base
        print("BEH", year, f"diff=${diff/1e9:.1f}B")
        beh.append({"year": year, "baseline_iitax_billions": base/1e9, "reform_behresp_iitax_billions": ref/1e9, "diff_revenue_billions": diff/1e9})
        sys.stdout.flush()
    with open("results_behresp_sub025.json","w") as f: json.dump(beh,f,indent=2)
    with open("results_behresp_sub025.csv","w",newline="") as f:
        w=csv.DictWriter(f, fieldnames=list(beh[0].keys())); w.writeheader(); w.writerows(beh)
    print("BEH TOTAL $B", sum(r["diff_revenue_billions"] for r in beh))
except Exception as e:
    import traceback; traceback.print_exc()
    pathlib.Path("behresp_error.txt").write_text(traceback.format_exc())
