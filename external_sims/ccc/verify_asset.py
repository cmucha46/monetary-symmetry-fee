import warnings; warnings.simplefilter("ignore")
from ccc.parameters import Specification, DepreciationParams
from ccc.data import Assets
from ccc.calculator import Calculator
for yr in (2026,2017):
    c=Calculator(p=Specification(year=yr), dp=DepreciationParams(), assets=Assets())
    df=c.calc_by_asset()
    sub=df[(df['asset_name']==df['major_asset_group']) | (df['asset_name']=='Overall')]
    print(f"\n--- year {yr}: calc_by_asset major groups ---")
    print(sub[['asset_name','tax_treat','metr_mix','mettr_mix','ucc_mix','rho_mix','delta']].to_string(index=False))
