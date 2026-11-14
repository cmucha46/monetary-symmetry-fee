"""Deterministic fiscal score v1: s in {0.50, 0.75, 0.90} x beta in {0.7, 0.88, 1.0}.

NO Monte Carlo, NO Fed-discretion dial (that requires an identified Fed
reaction function -- a separate analysis; the prototype's dial was shown by
the audit to be unidentified).

Combined total per scenario =
    net fee receipts (gross x NET_RECEIPTS_FACTOR, a PLACEHOLDER 13% haircut)
    + consolidated net-interest saving vs the no-fee baseline, split into
      (a) public-held yield effect and (b) IORB/remittance effect.
The reserve drain is never added: it is a settlement stock movement, not
revenue (see sfc.settlement_flows).
"""
import csv
from pathlib import Path

from .cohort import run_cohorts
from .config import (COVERED_BASE_VARIANTS, DEFAULT_COVERED_BASE_VARIANT,
                     IORB_BASE, NET_RECEIPTS_FACTOR, YEARS,
                     categories_for_variant)
from .sfc import LedgerParams, run_ledger_pair

DIALS = (0.50, 0.75, 0.90)
BETAS = (0.70, 0.88, 1.00)


def run_scenario(s: float, beta: float, ledger_params: LedgerParams = LedgerParams(),
                 covered_base_variant: str = DEFAULT_COVERED_BASE_VARIANT,
                 **cohort_kwargs):
    if "categories" not in cohort_kwargs:
        cohort_kwargs["categories"] = categories_for_variant(covered_base_variant)
    cohort = run_cohorts(s, beta, IORB_BASE, **cohort_kwargs)
    iorb_path = [row["iorb"] for row in cohort["annual"]]
    base, scen, diffs = run_ledger_pair(IORB_BASE, iorb_path, ledger_params, YEARS)
    annual = []
    for crow, drow in zip(cohort["annual"], diffs):
        gross = crow["gross_fee_total"]
        annual.append({
            "year": crow["year"], "s": s, "beta": beta,
            "covered_base_variant": covered_base_variant,
            "iorb": crow["iorb"], "fee_rate": crow["fee_rate"],
            "gross_fee": gross, "net_fee": gross * NET_RECEIPTS_FACTOR,
            **{f"gross_fee_{k}": v for k, v in crow["gross_fee_by_cat"].items()},
            "taxable_book": crow["taxable_book_total"],
            "public_yield_effect": drow["public_yield_effect"],
            "iorb_remit_effect": drow["iorb_remit_effect"],
            "consolidated_interest_saving": drow["consolidated_saving"],
            "remittance_cash_scenario": [r for r in scen if r["year"] == crow["year"]][0]["remittance_cash"],
            "deferred_asset_scenario": [r for r in scen if r["year"] == crow["year"]][0]["deferred_asset"],
        })
    totals = {
        "covered_base_variant": covered_base_variant,
        "s": s, "beta": beta,
        "gross_fee_10yr": sum(a["gross_fee"] for a in annual),
        "haircut_rate": 1.0 - NET_RECEIPTS_FACTOR,
        "net_fee_10yr": sum(a["net_fee"] for a in annual),
        "public_yield_saving_10yr": sum(a["public_yield_effect"] for a in annual),
        "iorb_remit_saving_10yr": sum(a["iorb_remit_effect"] for a in annual),
        "consolidated_interest_saving_10yr": sum(a["consolidated_interest_saving"] for a in annual),
        "combined_total_10yr": sum(a["net_fee"] for a in annual)
                               + sum(a["consolidated_interest_saving"] for a in annual),
        "taxable_book_2036": annual[-1]["taxable_book"],
    }
    return {"annual": annual, "totals": totals, "base": base, "scen": scen, "diffs": diffs}


def run_grid(**kwargs):
    return [run_scenario(s, b, **kwargs) for s in DIALS for b in BETAS]


def run_grid_all_variants():
    """The v2 grid: every covered-base variant x the same s x beta grid."""
    return [run_scenario(s, b, covered_base_variant=v)
            for v in COVERED_BASE_VARIANTS for s in DIALS for b in BETAS]


def sensitivity_runs():
    """Documented one-at-a-time sensitivity switches (s=0.75, beta=0.88 centre)."""
    # Pinned to lane_e_proxy: this file documents the v1 centre scenario.
    centre = run_scenario(0.75, 0.88, covered_base_variant="lane_e_proxy")["totals"]
    alt_phase = run_scenario(0.75, 0.88, covered_base_variant="lane_e_proxy",
                             phase_lock_mode="no_phase_lock")["totals"]
    alt_refi = run_scenario(0.75, 0.88, covered_base_variant="lane_e_proxy",
                            refi_elasticity=1.5)["totals"]
    rows = [
        {"switch": "centre (lock_phase, refi_eta=0)", **centre},
        {"switch": "phase_lock_mode=no_phase_lock", **alt_phase},
        {"switch": "refi_elasticity=1.5", **alt_refi},
    ]
    return rows


def _write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main(outdir=None):
    outdir = Path(outdir) if outdir else Path(__file__).resolve().parents[2] / "results"
    # v1 files are regenerated from the lane_e_proxy variant; their values
    # are identical to RESULTS_V1.md (replication check for Lane F) -- the
    # only format change is the added covered_base_variant column.
    grid_v1 = run_grid(covered_base_variant="lane_e_proxy")
    _write_csv(outdir / "deterministic_score_v1.csv", [g["totals"] for g in grid_v1])
    annual_rows = [a for g in grid_v1 for a in g["annual"]]
    _write_csv(outdir / "deterministic_annual_v1.csv", annual_rows)
    _write_csv(outdir / "sensitivity_v1.csv", sensitivity_runs())
    # v2: all covered-base variants on the same s x beta grid.
    grid_v2 = run_grid_all_variants()
    _write_csv(outdir / "deterministic_score_v2.csv", [g["totals"] for g in grid_v2])
    _write_csv(outdir / "deterministic_annual_v2.csv",
               [a for g in grid_v2 for a in g["annual"]])
    for g in grid_v2:
        t = g["totals"]
        print(f"variant={t['covered_base_variant']} s={t['s']:.2f} beta={t['beta']:.2f} "
              f"gross={t['gross_fee_10yr']:.3f} net={t['net_fee_10yr']:.3f} "
              f"int={t['consolidated_interest_saving_10yr']:.3f} "
              f"combined={t['combined_total_10yr']:.3f}")
    return grid_v2


if __name__ == "__main__":
    main()
