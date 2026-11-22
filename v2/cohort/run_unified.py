"""Run the UNIFIED BASE (Base B, headline) across designs x turnover
cases and write CSVs alongside the Base A outputs.

Usage: python3 run_unified.py [output_dir]
Outputs (default ./outputs):
  covered_path_unified_<design>_<case>.csv -- long format, all unified
                                              categories + TOTAL
  summary_unified_<design>_<case>.csv      -- unified TOTAL block, wide
  comparison_unified_vs_loansonly.csv      -- per-FY Base A vs. Base B
                                              for every design x case
Base A outputs (covered_path_*.csv, summary_*.csv) are NOT touched.
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from cohort_model import default_fee_path  # noqa: E402
from unified_model import comparison_table, run_unified_model  # noqa: E402
from cohort_model import summary_table  # noqa: E402


def main(out_dir: str = "outputs") -> None:
    out = Path(__file__).parent / out_dir
    out.mkdir(parents=True, exist_ok=True)
    fee = default_fee_path()
    comp_frames = []
    for design in ("floating", "locked"):
        for case in ("low", "central", "high"):
            df = run_unified_model(fee, design=design, delta_case=case)
            df.to_csv(out / f"covered_path_unified_{design}_{case}.csv",
                      index=False)
            st = summary_table(df)
            st.to_csv(out / f"summary_unified_{design}_{case}.csv")
            print(f"UNIFIED {design:8s} turnover={case:7s} "
                  f"cum collections FY28-36 ${st['collections_bn'].sum():>8,.0f}B   "
                  f"covered share FY36 {st.loc[2036, 'covered_share']:.1%}")
            comp = comparison_table(fee, design=design, delta_case=case)
            comp.insert(0, "delta_case", case)
            comp.insert(0, "design", design)
            comp_frames.append(comp.reset_index(names="fy"))
    pd.concat(comp_frames, ignore_index=True).to_csv(
        out / "comparison_unified_vs_loansonly.csv", index=False)
    print("comparison_unified_vs_loansonly.csv written")


if __name__ == "__main__":
    main(*sys.argv[1:])
