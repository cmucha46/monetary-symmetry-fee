"""
Monetary Symmetry Fee v2 -- grid "Monte Carlo" layer.

This is DISCRETE GRID ENUMERATION over the literature lane's documented
uncertainty grids -- not sampling from calibrated distributions, because
the key parameters (pass-through at fee scale, substitution rates, tau)
are UNCALIBRATED in the literature (LITERATURE.md sec. 5). Every grid
combination is run once, with equal weight. Reported means / medians /
ranges are summaries of a conditional simulation grid and are explicitly
NOT confidence intervals and NOT posterior distributions.

Grid (288 combinations per tau, per base):
  turnover  {low, central, high}          -- cohort lane delta cases
  design    {floating, locked}            -- fee design on fixed-rate loans
  theta     {0.5, 0.75, 1.0, 1.15}        -- reaches collections only via
                                             the erosion slot (see
                                             consolidation.py docstring)
  erosion   {0, .10, .25, .40}            -- year-5 covered-base erosion
                                             at theta = 1 (lit. sec. 3 grids)
  beta      {0.45, 0.55, 0.65}            -- INERT in this layer: the Fed
                                             remittance identity has no
                                             deposit-beta entry. Carried so
                                             the SFC pass can wire it to
                                             bank funding costs without
                                             changing the run schema.
Results are reported PER TAU in {0, 0.25, 0.5, 0.75}; a tau-integrated
number is never produced (LITERATURE.md sec. 4.3).
"""

from __future__ import annotations

import itertools

import pandas as pd

from consolidation import (BETAS, DESIGNS, EROSIONS, TAUS, THETAS,
                           TURNOVERS, consolidate, load_config)


def run_grid(base: str, config: dict | None = None,
             macro_feedback: str | None = None,
             designs: tuple = DESIGNS) -> pd.DataFrame:
    """Enumerate the full grid for one base. Returns one row per
    (combination, tau) with annual detail collapsed to window totals.

    `macro_feedback` (final pass): a Lane B regime whose fee-path ratio
    and drag are applied to every cell. Lane B ran the FLOATING design
    only, so feedback-adjusted grids must pass designs=("floating",);
    applying floating-derived feedback to locked cells would mislabel
    them."""
    config = config or load_config()
    rows = []
    for turnover, design, theta, erosion, beta in itertools.product(
            TURNOVERS, designs, THETAS, EROSIONS, BETAS):
        tables = consolidate(base, design, turnover, theta, erosion,
                             beta=beta, config=config,
                             macro_feedback=macro_feedback)
        for tau in TAUS:
            df = tables[tau]
            rows.append({
                "base": base, "turnover": turnover, "design": design,
                "theta": theta, "erosion_yr5": erosion, "beta": beta,
                "tau": tau,
                "gross_collections_10y_bn": df["gross_collections_bn"].sum(),
                "net_fee_10y_bn": df["net_fee_receipts_bn"].sum(),
                "treasury_savings_consol_10y_bn":
                    df["treasury_savings_consol_bn"].sum(),
                "delta_remittances_10y_bn": df["delta_remittances_bn"].sum(),
                "frbus_feedback_10y_bn":
                    float(df["frbus_feedback_bn"].sum(min_count=1))
                    if "frbus_feedback_bn" in df else float("nan"),
                "consolidated_net_10y_bn": df["consolidated_net_bn"].sum(),
            })
    return pd.DataFrame(rows)


def summarize(runs: pd.DataFrame) -> pd.DataFrame:
    """Per-tau distribution of the 10-year consolidated total across the
    grid. Conditional simulation summaries -- NOT confidence intervals."""
    out = []
    for tau, g in runs.groupby("tau"):
        s = g["consolidated_net_10y_bn"]
        out.append({"tau": tau, "n_runs": len(g),
                    "mean_bn": s.mean(), "median_bn": s.median(),
                    "p25_bn": s.quantile(0.25), "p75_bn": s.quantile(0.75),
                    "min_bn": s.min(), "max_bn": s.max()})
    return pd.DataFrame(out).sort_values("tau").reset_index(drop=True)


def summarize_by(runs: pd.DataFrame, column: str) -> pd.DataFrame:
    """Attribution: per-tau median 10-year consolidated total by one grid
    dimension (e.g. design or turnover), holding the rest of the grid at
    full enumeration."""
    out = []
    for (tau, val), g in runs.groupby(["tau", column]):
        out.append({"tau": tau, column: val,
                    "median_bn": g["consolidated_net_10y_bn"].median(),
                    "min_bn": g["consolidated_net_10y_bn"].min(),
                    "max_bn": g["consolidated_net_10y_bn"].max()})
    return pd.DataFrame(out)
