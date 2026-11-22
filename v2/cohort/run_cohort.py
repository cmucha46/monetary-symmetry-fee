"""Run the cohort model across designs x turnover cases and write CSVs.

Usage: python3 run_cohort.py [output_dir]
Outputs (default ./outputs):
  covered_path_<design>_<case>.csv  -- long format, all categories + TOTAL
  summary_<design>_<case>.csv       -- TOTAL block only, wide
  fiscal_skeleton.csv               -- Treasury repricing + Fed remittance
                                       accounting under the default scenario
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from cohort_model import default_fee_path, run_model, summary_table  # noqa: E402
import fiscal  # noqa: E402


def main(out_dir: str = "outputs") -> None:
    out = Path(__file__).parent / out_dir
    out.mkdir(parents=True, exist_ok=True)
    fee = default_fee_path()
    for design in ("floating", "locked"):
        for case in ("low", "central", "high"):
            df = run_model(fee, design=design, delta_case=case)
            df.to_csv(out / f"covered_path_{design}_{case}.csv", index=False)
            st = summary_table(df)
            st.to_csv(out / f"summary_{design}_{case}.csv")
            print(f"{design:8s} turnover={case:7s} "
                  f"cum collections FY28-36 ${st['collections_bn'].sum():>8,.0f}B   "
                  f"covered share FY36 {st.loc[2036, 'covered_share']:.1%}")
    # Fiscal skeleton under the default scenario: IORB halves from FY2030.
    years = range(2027, 2037)
    iorb_ms = {y: (0.0390 if y < 2030 else 0.0195) for y in years}
    iorb_base = {y: 0.0390 for y in years}
    fed_ms = fiscal.fed_remittances(iorb_ms).set_index("fy").add_suffix("_ms")
    fed_b = fiscal.fed_remittances(iorb_base).set_index("fy").add_suffix("_base")
    delta = fiscal.treasury_interest_delta(-0.01).set_index("fy")
    pd.concat([fed_b, fed_ms, delta], axis=1).to_csv(out / "fiscal_skeleton.csv")
    print("fiscal_skeleton.csv written (dy=-100bp is an illustrative INPUT, "
          "not a modeled yield response)")


if __name__ == "__main__":
    main(*sys.argv[1:])
