"""
CCC run: current law (year=2026, TCJA-as-made-permanent by OBBBA per CCC 2.1.1 defaults)
vs pre-TCJA law (year=2017, same shipped default_parameters.json time series).
Primary: year-native Specifications, no hand edits.
Sensitivity: 2017 statutory business parameters transplanted into a 2026 Specification
(holds inflation/economic assumptions at 2026 values), every edit listed in code + notes.
Outputs: summary tables (metr, mettr, ucc) + asset summary tables, saved as CSVs.
"""
import warnings, json
warnings.simplefilter("ignore")
import pandas as pd
from ccc.parameters import Specification, DepreciationParams
from ccc.data import Assets
from ccc.calculator import Calculator

def make_calc(year):
    p = Specification(year=year)
    dp = DepreciationParams()
    assets = Assets()
    return Calculator(p=p, dp=dp, assets=assets)

def make_transplant_calc():
    # Start from 2026 (current law + 2026 economics), overwrite ONLY statutory
    # business-law parameters with their shipped 2017 values.
    p = Specification(year=2026)
    rev = {
        'CIT_rate': {2026: [0.35]},          # pre-TCJA top corporate rate (2017 shipped value)
        'CIT_rate_ded': {2026: [0.35]},      # same, applied to deductions
        # pre-TCJA bonus depreciation was 50% for 3-20yr class property (2017 shipped values);
        # 25/27.5/39yr classes were 0.0 in both years, unchanged.
        'BonusDeprec_3yr': {2026: [0.5]},
        'BonusDeprec_5yr': {2026: [0.5]},
        'BonusDeprec_7yr': {2026: [0.5]},
        'BonusDeprec_10yr': {2026: [0.5]},
        'BonusDeprec_15yr': {2026: [0.5]},
        'BonusDeprec_20yr': {2026: [0.5]},
        # Individual-level effective rates at their shipped 2017 values (pre-TCJA individual law,
        # incl. no Sec.199A): pass-through, dividends, interest, cap gains, tax-deferred, housing.
        'tau_pt': {2026: [0.3309]},   # exact values pulled programmatically below
    }
    # pull exact 2017 tau values from a 2017 specification to avoid transcription error
    p17 = Specification(year=2017)
    for k in ['tau_pt','tau_div','tau_int','tau_scg','tau_lcg','tau_td','tau_h']:
        rev[k] = {2026: [float(__import__('numpy').asarray(getattr(p17, k)).flatten()[0])]}
    rev['tau_pt'] = {2026: [float(__import__('numpy').asarray(p17.tau_pt).flatten()[0])]}
    p.update_specification(rev)
    return Calculator(p=p, dp=DepreciationParams(), assets=Assets()), rev

calc_cur = make_calc(2026)   # baseline in CCC summary_table convention: self=baseline
calc_2017 = make_calc(2017)  # reform = pre-TCJA law

results = {}
for var in ['metr','mettr','ucc']:
    calc_cur = make_calc(2026); calc_2017 = make_calc(2017)
    tbl = calc_cur.summary_table(calc_2017, output_variable=var)
    results[var] = tbl
    tbl.to_csv(f'summary_{var}_current2026_vs_preTCJA2017.csv', index=False)
    print(f"\n=== summary_table {var}: baseline=current law (2026), reform=pre-TCJA law (2017) ===")
    print(tbl.to_string(index=False))

    calc_cur = make_calc(2026); calc_2017 = make_calc(2017)
    atbl = calc_cur.asset_summary_table(calc_2017, output_variable=var, financing='mix')
    atbl.to_csv(f'asset_summary_{var}_current2026_vs_preTCJA2017.csv', index=False)
    print(f"\n=== asset_summary_table {var} (mix financing) ===")
    print(atbl.to_string(index=False))

# Sensitivity: law-only transplant at constant 2026 economics
calc_tr, rev_used = make_transplant_calc()
with open('transplant_revision.json','w') as f:
    json.dump({k:{str(y):v for y,v in d.items()} for k,d in rev_used.items()}, f, indent=2)
for var in ['metr','ucc']:
    calc_cur = make_calc(2026)
    tbl = calc_cur.summary_table(calc_tr, output_variable=var)
    tbl.to_csv(f'sensitivity_summary_{var}_transplant2017law_at2026.csv', index=False)
    print(f"\n=== SENSITIVITY summary_table {var}: 2017 statutory params transplanted into 2026 ===")
    print(tbl.to_string(index=False))
print("\nDONE")
