"""Monetary Symmetry Fee model v2 (Lane E): deterministic cohort + SFC fiscal layer.

The macro (FRB/US) layer lives elsewhere; this package is the external
fiscal/cohort/SFC module that FRB/US cannot supply (FRB/US has no loan stock,
no IORB, and no fee-revenue variable).
"""
from .config import CATEGORIES, IORB_BASE, YEARS
from .policy import fee_from_iorb, policy_for
from .cohort import run_cohorts
from .sfc import LedgerParams, run_ledger_pair, settlement_flows
from .score import run_scenario, run_grid

__all__ = ["CATEGORIES", "IORB_BASE", "YEARS", "fee_from_iorb", "policy_for",
           "run_cohorts", "LedgerParams", "run_ledger_pair", "settlement_flows",
           "run_scenario", "run_grid"]
__version__ = "2.0.0-v1"
