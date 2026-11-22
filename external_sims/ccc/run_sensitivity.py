import warnings, json; warnings.simplefilter("ignore")
import numpy as np
from ccc.parameters import Specification, DepreciationParams
from ccc.data import Assets
from ccc.calculator import Calculator

p17 = Specification(year=2017)
def v17(k): return float(np.asarray(getattr(p17,k)).flatten()[0])
rev = {}
# Every hand edit (2017 statutory values transplanted into a 2026 Specification;
# 2026 economics -- inflation 2.0%, nominal interest 6.8%, saver parameters -- held constant):
rev['CIT_rate'] = [{'year':2026,'value':0.35}]        # pre-TCJA corporate rate (shipped 2017 value)
rev['CIT_rate_ded'] = [{'year':2026,'value':0.35}]    # same, for deductions
for cl in ['3yr','5yr','7yr','10yr','15yr','20yr']:
    rev[f'BonusDeprec_{cl}'] = [{'year':2026,'value':0.5}]  # pre-TCJA 50% bonus (shipped 2017 values); 25/27.5/39yr = 0.0 in both years, untouched
for k in ['tau_pt','tau_div','tau_int','tau_scg','tau_lcg','tau_td','tau_h']:
    rev[k] = [{'year':2026,'value':v17(k)}]           # shipped 2017 individual-level effective rates (pre-TCJA, no 199A)
# NOT edited (documented non-channels): interest_deduct_haircut_c/pt stays 0.0 (CCC default: Sec.163(j)
# 30%-of-ATI limit assumed non-binding for marginal investment, both laws);
# depreciation rules (incl. R&D 'Expensing') unchanged -- CCC ships one static rules file, and under
# OBBBA current law domestic R&D is expensed again, so the Sec.174 channel is ~zero vs this baseline anyway.
with open('transplant_revision.json','w') as f: json.dump(rev,f,indent=2)
print(json.dumps(rev,indent=1))

p = Specification(year=2026); p.update_specification(rev)
calc_tr = Calculator(p=p, dp=DepreciationParams(), assets=Assets())
for var in ['metr','mettr','ucc']:
    calc_cur = Calculator(p=Specification(year=2026), dp=DepreciationParams(), assets=Assets())
    tbl = calc_cur.summary_table(calc_tr, output_variable=var)
    tbl.to_csv(f'sensitivity_summary_{var}_transplant2017law_at2026.csv', index=False)
    print(f"\n=== SENSITIVITY {var}: baseline 2026 current law vs 2017 statutory params at 2026 economics ===")
    print(tbl.to_string(index=False))
print("DONE")
