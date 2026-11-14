import pytest

from monetary_symmetry.config import NET_RECEIPTS_FACTOR
from monetary_symmetry.score import run_grid, run_scenario


def test_combined_total_identity():
    res = run_scenario(0.75, 0.88)
    t = res["totals"]
    assert t["net_fee_10yr"] == pytest.approx(t["gross_fee_10yr"] * NET_RECEIPTS_FACTOR)
    assert t["combined_total_10yr"] == pytest.approx(
        t["net_fee_10yr"] + t["consolidated_interest_saving_10yr"])
    assert t["consolidated_interest_saving_10yr"] == pytest.approx(
        t["public_yield_saving_10yr"] + t["iorb_remit_saving_10yr"])


def test_grid_shape_and_ordering():
    grid = run_grid()
    assert len(grid) == 9
    totals = {(g["totals"]["s"], g["totals"]["beta"]): g["totals"] for g in grid}
    # combined benefit rises with the dial at fixed beta (algebra, as in the
    # prototype -- reported as a property of the design, not a finding)
    for beta in (0.70, 0.88, 1.00):
        assert totals[(0.90, beta)]["combined_total_10yr"] > totals[(0.50, beta)]["combined_total_10yr"]


def test_lower_beta_raises_fee_at_fixed_dial():
    # Lower pass-through -> IORB solved down less? No: r = d/(1+beta*k); lower
    # beta leaves IORB HIGHER, and f = k*r is therefore higher.
    lo = run_scenario(0.75, 0.70)["totals"]
    hi = run_scenario(0.75, 1.00)["totals"]
    assert lo["gross_fee_10yr"] > hi["gross_fee_10yr"]
