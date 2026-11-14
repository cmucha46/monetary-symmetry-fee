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
from .config import IORB_BASE, NET_RECEIPTS_FACTOR, YEARS
from .sfc import LedgerParams, run_ledger_pair

DIALS = (0.50, 0.75, 0.90)
BETAS = (0.70, 0.88, 1.00)


def run_scenario(s: float, beta: float, ledger_params: LedgerParams = LedgerParams(),
                 **cohort_kwargs):
    cohort = run_cohorts(s, beta, IORB_BASE, **cohort_kwargs)
    iorb_path = [row["iorb"] for row in cohort["annual"]]
    base, scen, diffs = run_ledger_pair(IORB_BASE, iorb_path, ledger_params, YEARS)
    annual = []
    for crow, drow in zip(cohort["annual"], diffs):
        gross = crow["gross_fee_total"]
        annual.append({
            "year": crow["year"], "s": s, "beta": beta,
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


def sensitivity_runs():
    """Documented one-at-a-time sensitivity switches (s=0.75, beta=0.88 centre)."""
    centre = run_scenario(0.75, 0.88)["totals"]
    alt_phase = run_scenario(0.75, 0.88, phase_lock_mode="no_phase_lock")["totals"]
    alt_refi = run_scenario(0.75, 0.88, refi_elasticity=1.5)["totals"]
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
    grid = run_grid()
    _write_csv(outdir / "deterministic_score_v1.csv", [g["totals"] for g in grid])
    annual_rows = [a for g in grid for a in g["annual"]]
    _write_csv(outdir / "deterministic_annual_v1.csv", annual_rows)
    _write_csv(outdir / "sensitivity_v1.csv", sensitivity_runs())
    for g in grid:
        t = g["totals"]
        print(f"s={t['s']:.2f} beta={t['beta']:.2f} gross={t['gross_fee_10yr']:.3f} "
              f"net={t['net_fee_10yr']:.3f} int={t['consolidated_interest_saving_10yr']:.3f} "
              f"combined={t['combined_total_10yr']:.3f}")
    return grid


if __name__ == "__main__":
    main()
